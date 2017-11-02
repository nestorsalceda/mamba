# -*- coding: utf-8 -*-

import sys
from datetime import datetime

from mamba import error, runnable


class Example(runnable.Runnable):

    # TODO: Remove parent parameter, it's only used for testing purposes
    def __init__(self, test, parent=None):
        self.test = test
        self.parent = parent
        self.error = None
        self.was_run = False

    def execute(self, reporter, execution_context):
        assert self.parent is not None

        self._start(reporter)

        if self.error is None:
            self.parent.execute_hook('before_each', execution_context)

        if self.error is None:
            self._execute_test(execution_context)

        if self.error is None:
            self.parent.execute_hook('after_each', execution_context)

        self.was_run = True
        self._finish(reporter)

    def _start(self, reporter):
        self._begin = datetime.utcnow()
        reporter.example_started(self)

    def _execute_test(self, execution_context):
        try:
            if hasattr(self.test, 'im_func'):
                self.test.im_func(execution_context)
            else:
                self.test(execution_context)
        except Exception:
            self._set_failed()

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

    @property
    def name(self):
        return self.test.__name__[10:]

    @property
    def failed(self):
        return self.error is not None


class PendingExample(Example):
    def execute(self, reporter, execution_context):
        reporter.example_pending(self)
