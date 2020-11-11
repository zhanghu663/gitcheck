# coding=utf-8
import queue

_instance = None


def event_manager():
    global _instance
    if _instance is None:
        _instance = PrinterEventManager()
    return _instance


class PrinterEventManager(object):
    def __init__(self):
        self.printer_queue = queue.Queue()

    def fire(self, printer_event):
        self.enqueue(printer_event)

    def enqueue(self, printer_event):
        q = self.printer_queue
        q.put(printer_event)
