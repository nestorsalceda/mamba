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

    def execute(self, reporter, context, tags=None):
        raise NotImplementedError()

    def included_in_execution(self, tags):
        should_execute = tags is None or any(tag in self.tags for tag in tags)

        if self.parent is None:
            return should_execute
        else:
            return self.parent.included_in_execution(tags) or should_execute

    def _do_execute(self, context, tags=None):
        raise NotImplementedError()

    def failed(self):
        return self.error is not None

    def fail(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)
