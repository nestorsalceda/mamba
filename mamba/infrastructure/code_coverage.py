# -*- coding: utf-8 -*-

import coverage


class CodeCoverage(object):

    def __init__(self, code_coverage_file):
        self.coverage = coverage.coverage(data_file=code_coverage_file)

    def __enter__(self):
        self.coverage.start()

    def __exit__(self, type_, value, traceback):
        self.coverage.stop()
        self.coverage.save()
