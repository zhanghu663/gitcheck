# coding=utf-8


class SerialLogHandler(object):
    def __init__(self):
        pass

    @classmethod
    def on_open_connection(cls):
        cls.do_rollover = True