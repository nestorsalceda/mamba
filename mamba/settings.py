# -*- coding: utf-8 -*-


class Settings(object):

    def __init__(self):
        self._slow_test_threshold = .075
        self._enable_code_coverage = False
        self._enable_file_watcher = False
        self._format = 'documentation'

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

    @property
    def slow_test_threshold(self):
        return self._slow_test_threshold

    @slow_test_threshold.setter
    def slow_test_threshold(self, value):
        self._slow_test_threshold = value

    @property
    def enable_code_coverage(self):
        return self._enable_code_coverage

    @enable_code_coverage.setter
    def enable_code_coverage(self, value):
        self._enable_code_coverage = value

    @property
    def enable_file_watcher(self):
        return self._enable_file_watcher

    @enable_file_watcher.setter
    def enable_file_watcher(self, value):
        self._enable_file_watcher = value
