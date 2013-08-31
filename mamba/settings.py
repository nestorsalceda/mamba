# -*- coding: utf-8 -*-


class Settings(object):

    def __init__(self):
        self._slow_test_threshold = .075
        self._enable_code_coverage = False
        self._enable_file_watcher = False

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
