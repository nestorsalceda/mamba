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
        self._tags = tags or []
        self._included_in_execution = None

    def execute(self, reporter, context, tags=None):
        raise NotImplementedError()

    def has_tag(self, tag):
        if self.parent is None:
            return tag in self._tags

        return tag in self._tags or self.parent.has_tag(tag)

    def included_in_execution(self, tags):
        return tags is None or any(self.has_tag(tag) for tag in tags)

    def failed(self):
        return self.error is not None

    def fail(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)
