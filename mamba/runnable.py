# -*- coding: utf-8 -*-

import sys
from datetime import timedelta

from mamba import error


class ExecutionContext(object):
    pass


class Runnable(object):

    def __init__(self, parent=None, tags=None):
        self.elapsed_time = timedelta(0)
        self.error = None
        self.parent = parent
        self.tags = tags or []
        self._included_in_execution = None

    def execute(self, reporter, context, tags=None):
        raise NotImplementedError()

    def included_in_execution(self, tags):
        if self._included_in_execution is None:
            self._included_in_execution = tags is None or any(tag in self.tags for tag in tags)

            if self.parent is not None:
                self._included_in_execution = self.parent.included_in_execution(tags) or self._included_in_execution

        return self._included_in_execution

    def _do_execute(self, context, tags=None):
        raise NotImplementedError()

    def failed(self):
        return self.error is not None

    def fail(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)
