# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta

from mamba import error


class Example(object):

    def __init__(self, test, parent=None):
        self.test = test
        self.parent = parent
        self._error = None
        self._elapsed_time = timedelta(0)
        self.was_run = False

    def run(self, reporter):
        self._start(reporter)
        try:
            if not self.failed:
                self._run_inner_test(reporter)
        except Exception as exception:
            self.was_run = True
            if self.error is None:
                self._set_failed()
        finally:
            self._finish(reporter)

    def _start(self, reporter):
        self._begin = datetime.utcnow()
        reporter.example_started(self)

    def _run_inner_test(self, reporter):
        self.run_hook('before_each')
        if hasattr(self.test, 'im_func'):
            self.test.im_func(self.parent.execution_context)
        else:
            self.test(self.parent.execution_context)
        self.was_run = True
        self.run_hook('after_each')

    def run_hook(self, hook):
        for parent in self._parents:
            parent.run_hook(hook)

    def _set_failed(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)

    def _finish(self, reporter):
        self._elapsed_time = datetime.utcnow() - self._begin
        if self.failed:
            reporter.example_failed(self)
        elif self.was_run:
            reporter.example_passed(self)
        else:
            reporter.example_pending(self)

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
    def failed(self):
        return self.error is not None

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value


class PendingExample(Example):
    def run(self, reporter):
        reporter.example_pending(self)
