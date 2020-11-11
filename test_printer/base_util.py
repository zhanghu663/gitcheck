# coding=utf-8
import threading


class CountedEvent(object):

    def __init__(self, value=0, minimum=0, maximum=None, **kwargs):
        self._counter = 0
        self._min = minimum
        self._max = kwargs.get("max", maximum)
        self._mutex = threading.RLock()
        self._event = threading.Event()
        self._internal_set(value)

    def _internal_set(self, value):
        self._counter = value
        if self._counter <= 0:
            if self._min is not None and self._counter < self._min:
                self._counter = self._min
            self._event.clear()
        else:
            if self._max is not None and self._counter > self._max:
                self._counter = self._max
            self._event.set()
