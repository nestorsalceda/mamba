# -*- coding: utf-8 -*-

import sys
from datetime import timedelta

from mamba import error


class ExecutionContext(object):
    pass


class Runnable(object):

    def __init__(self, tags=None):
        self.elapsed_time = timedelta(0)
        self.error = None
        self.tags = tags or []

    def execute(self, reporter, context, tags=None):
        if not self.included_in_execution(tags):
            return

        self._do_execute(reporter, context, tags)

    def included_in_execution(self, tags):
        return tags is None or any(tag in self.tags for tag in tags)

    def _do_execute(self, context, tags=None):
        raise NotImplementedError()

    def failed(self):
        return self.error is not None

    def fail(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)
