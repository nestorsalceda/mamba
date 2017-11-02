# -*- coding: utf-8 -*-

import sys
from datetime import timedelta

from mamba import error


class ExecutionContext(object):
    pass


class Runnable(object):

    def __init__(self):
        self.elapsed_time = timedelta(0)
        self.error = None

    def execute(self, reporter, context):
        raise NotImplementedError

    def failed(self):
        return self.error is not None

    def fail(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)
