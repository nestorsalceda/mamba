# -*- coding: utf-8 -*-

import coverage


class CodeCoverage(object):

    def __init__(self):
        self.coverage = coverage.coverage()

    def __enter__(self):
        self.coverage.start()

    def __exit__(self, type_, value, traceback):
        self.coverage.stop()
        self.coverage.save()
