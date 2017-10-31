# -*- coding: utf-8 -*-

import sys, copy
from datetime import datetime

from mamba import error, runnable


class Example(runnable.Runnable):

    # TODO: Remove parent parameter, it's only used for testing purposes
    def __init__(self, test, parent=None):
        self.test = test
        self.parent = parent
        self._error = None
        self.was_run = False

    def execute(self, reporter):
        self._start(reporter)

        try:
            self.parent.run_hook('before_each')
            self._execute_test(self.parent.execution_context)
            self.parent.run_hook('after_each')
        except Exception:
            self._set_failed()

        self.was_run = True
        self._finish(reporter)

    def _start(self, reporter):
        self._begin = datetime.utcnow()
        reporter.example_started(self)

    def _execute_test(self, execution_context):
        if hasattr(self.test, 'im_func'):
            self.test.im_func(execution_context)
        else:
            self.test(execution_context)

    def _set_failed(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)

    def _finish(self, reporter):
        self.elapsed_time = datetime.utcnow() - self._begin
        if self.failed:
            reporter.example_failed(self)
        elif self.was_run:
            reporter.example_passed(self)
        else:
            reporter.example_pending(self)

    def run(self, reporter):
        self._start(reporter)
        try:
            if not self.failed:
                self._run_inner_test(reporter)
        except Exception:
            self.was_run = True
            if self.error is None:
                self._set_failed()
        finally:
            self._finish(reporter)

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

    @property
    def _parents(self):
        parents = []
        parent = self.parent
        while parent:
            parents.append(parent)
            parent = parent.parent

        return reversed(parents)

    @property
    def name(self):
        return self.test.__name__[10:]

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
    def execute(self, reporter):
        reporter.example_pending(self)

    def run(self, reporter):
        self.execute(reporter)
