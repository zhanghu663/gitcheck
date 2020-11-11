# coding=utf-8
from test_printer.comm import MachineCom
from test_printer.handers import SerialLogHandler
from test_printer.printer_event import event_manager


class CxswPrinter(object):

    def __init__(self):
        pass

    def build_connection(self, port=None, baudrate=None):
        # 与打印机建立连接
        printer_event = 'Connecting'
        event_manager().fire(event=printer_event)
        SerialLogHandler.on_open_connection()
        MachineCom(port, baudrate, callbackObject=self, printerProfileManager=None)

