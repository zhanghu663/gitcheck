# coding=utf-8
import threading

from test_printer.base_util import CountedEvent


class MachineCom(object):
    def __init__(self, port=None, baudrate=None, callbackObject=None, printerProfileManager=None):
        self._ack_max = settings().getInt(["serial", "ackMax"])
        self._clear_to_send = CountedEvent(name="comm.clear_to_send", minimum=None, maximum=self._ack_max)
        # monitoring thread
        self._monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self.monitor_data, name="comm._monitor")
        self.monitoring_thread.daemon = True

        # sending thread
        self._send_queue_active = True
        self.sending_thread = threading.Thread(target=self.send_data, name="comm.sending_thread")
        self.sending_thread.daemon = True

    def start(self):
        self.monitoring_thread.start()
        self.sending_thread.start()

    def send_data(self):
        """
        The send loop is responsible of sending commands in ``self._send_queue`` over the line, if it is cleared for
        sending (through received ``ok`` responses from the printer's firmware.
        """

        self._clear_to_send.wait()  # 表示子线程阻塞，等待主线程event.set()之后子线程继续运行

        while self._send_queue_active:
            try:
                # wait until we have something in the queue
                try:
                    entry = self._send_queue.get()
                    print("entry:{}".format(entry))
                    if entry[0].startswith('M140'):
                        print("M140")
                except queue.Empty:
                    # I haven't yet been able to figure out *why* this can happen but according to #3096 and SERVER-2H
                    # an Empty exception can fly here due to resend_active being True but nothing being in the resend
                    # queue of the send queue. So we protect against this possibility...
                    continue

                try:
                    # make sure we are still active
                    if not self._send_queue_active:
                        break

                    # sleep if we are dwelling
                    now = monotonic_time()
                    if self._blockWhileDwelling and self._dwelling_until and now < self._dwelling_until:
                        time.sleep(self._dwelling_until - now)
                        self._dwelling_until = False

                    # fetch command, command type and optional linenumber and sent callback from queue
                    command, linenumber, command_type, on_sent, processed, tags = entry

                    if isinstance(command, SendQueueMarker):
                        command.run()
                        self._continue_sending()
                        continue

                    # some firmwares (e.g. Smoothie) might support additional in-band communication that will not
                    # stick to the acknowledgement behaviour of GCODE, so we check here if we have a GCODE command
                    # at hand here and only clear our clear_to_send flag later if that's the case
                    gcode, subcode = gcode_and_subcode_for_cmd(command)

                    if linenumber is not None:
                        # line number predetermined - this only happens for resends, so we'll use the number and
                        # send directly without any processing (since that already took place on the first sending!)
                        self._use_up_clear(gcode)
                        self._do_send_with_checksum(command.encode("ascii"), linenumber)

                    else:
                        if not processed:
                            # trigger "sending" phase if we didn't so far
                            results = self._process_command_phase("sending", command, command_type,
                                                                  gcode=gcode,
                                                                  subcode=subcode,
                                                                  tags=tags)

                            if not results:
                                # No, we are not going to send this, that was a last-minute bail.
                                # However, since we already are in the send queue, our _monitor
                                # loop won't be triggered with the reply from this unsent command
                                # now, so we try to tickle the processing of any active
                                # command queues manually
                                self._continue_sending()

                                # and now let's fetch the next item from the queue
                                continue

                            # we explicitly throw away plugin hook results that try
                            # to perform command expansion in the sending/sent phase,
                            # so "results" really should only have more than one entry
                            # at this point if our core code contains a bug
                            assert len(results) == 1

                            # we only use the first (and only!) entry here
                            command, _, gcode, subcode, tags = results[0]

                        if command.strip() == "":
                            self._logger.info("Refusing to send an empty line to the printer")

                            # same here, tickle the queues manually
                            self._continue_sending()

                            # and fetch the next item
                            continue

                        # handle @ commands
                        if gcode is None and command.startswith("@"):
                            self._process_atcommand_phase("sending", command, tags=tags)

                            # tickle...
                            self._continue_sending()

                            # ... and fetch the next item
                            continue

                        # now comes the part where we increase line numbers and send stuff - no turning back now
                        used_up_clear = self._use_up_clear(gcode)
                        self._do_send(command, gcode=gcode)
                        if not used_up_clear:
                            # If we didn't use up a clear we need to tickle the read queue - there might
                            # not be a reply to this command, so our _monitor loop will stay waiting until
                            # timeout. We definitely do not want that, so we tickle the queue manually here
                            self._continue_sending()

                    # trigger "sent" phase and use up one "ok"
                    if on_sent is not None and callable(on_sent):
                        # we have a sent callback for this specific command, let's execute it now
                        on_sent()
                    self._process_command_phase("sent", command, command_type, gcode=gcode, subcode=subcode,
                                                tags=tags)

                finally:
                    # no matter _how_ we exit this block, we signal that we
                    # are done processing the last fetched queue entry
                    self._send_queue.task_done()

                # now we just wait for the next clear and then start again
                self._clear_to_send.wait()
            except Exception:
                self._logger.exception("Caught an exception in the send loop")
        self._log("Closing down send loop")


