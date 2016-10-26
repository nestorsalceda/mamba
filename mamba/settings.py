# -*- coding: utf-8 -*-


class Settings(object):
    def __init__(self):
        self.slow_test_threshold = .075
        self.enable_code_coverage = False
        self.code_coverage_file = '.coverage'
        self.enable_file_watcher = False
        self.format = 'documentation'
        self.no_color = False
