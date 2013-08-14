# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
import inspect

from mamba import error


class Example(object):

    def __init__(self, test, parent=None, pending=False):
        self.test = test
        self.parent = parent
        self.pending = pending
        self._error = None
        self._elapsed_time = timedelta(0)

    def run(self, reporter):
        reporter.example_started(self)
        try:
            self._begin = datetime.utcnow()
            if self.pending:
                reporter.example_pending(self)
            else:
                self._run_inner_test(reporter)
        except Exception as exception:
            self._elapsed_time = datetime.utcnow() - self._begin
            self._set_failed()
            reporter.example_failed(self)

    def _run_inner_test(self, reporter):
        self.run_hook('before_each')
        self.test()
        self.run_hook('after_each')
        self._elapsed_time = datetime.utcnow() - self._begin
        reporter.example_passed(self)

    def _set_failed(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)

    def run_hook(self, hook):
        for parent in self._parents:
            parent.run_hook(hook)

    @property
    def _parents(self):
        parents = []
        parent = self.parent
        while parent:
            parents.append(parent)
            parent = parent.parent

        return reversed(parents)

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @property
    def name(self):
        return self.test.__name__

    @property
    def source_line(self):
        return inspect.getsourcelines(self.test)[1]

    @property
    def failed(self):
        return self.error is not None

    @property
    def pending(self):
        if self.parent:
            return self._pending or self.parent.pending
        return self._pending

    @pending.setter
    def pending(self, value):
        self._pending = value

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

    @property
    def depth(self):
        if self.parent is None:
            return 0

        return self.parent.depth + 1
