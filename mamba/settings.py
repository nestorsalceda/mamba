# -*- coding: utf-8 -*-


class Settings(object):

    def __init__(self):
        self._slow_test_threshold = .075

    @property
    def slow_test_threshold(self):
        return self._slow_test_threshold

    @slow_test_threshold.setter
    def slow_test_threshold(self, value):
        self._slow_test_threshold = value
