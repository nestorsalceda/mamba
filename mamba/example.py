# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta

from mamba import error
from mamba.infrastructure import retrieve_unbound_method_from


class Example(object):

    def __init__(self, test, parent=None):
        self._test = retrieve_unbound_method_from(test)
        self.parent = parent
        self.error = None
        self._elapsed_time = timedelta(0)
        self._was_run = False

    def run(self, reporter):
        self._start(reporter)
        try:
            if not self.failed:
                self._run_inner_test(reporter)
        except Exception as exception:
            self._was_run = True
            self._set_failed()
        finally:
            self._finish(reporter)

    def _start(self, reporter):
        self._begin = datetime.utcnow()
        reporter.example_started(self)

    def _run_inner_test(self, reporter):
        self.run_hook('before_each')
        self._test(self.parent.execution_context)
        self._was_run = True
        self.run_hook('after_each')

    def run_hook(self, hook):
        for parent in self._parents:
            parent.run_hook(hook)

    def _set_failed(self):
        if self.failed:
            return

        value, traceback = self._get_value_and_traceback_of_the_exception_currently_being_handled()
        self.error = error.Error(value, traceback)

    def _get_value_and_traceback_of_the_exception_currently_being_handled(self):
        return sys.exc_info()[1:]

    def _finish(self, reporter):
        self._elapsed_time = datetime.utcnow() - self._begin
        if self.failed:
            reporter.example_failed(self)
        elif self._was_run:
            reporter.example_passed(self)
        else:
            reporter.example_pending(self)

    @property
    def _parents(self):
        parents = []
        parent = self.parent
        while parent is not None:
            parents.append(parent)
            parent = parent.parent

        return reversed(parents)

    @property
    def name(self):
        return self._test.__name__[10:]

    @property
    def failed(self):
        return self.error is not None

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @property
    def was_run(self):
        return self._was_run



class PendingExample(Example):
    def run(self, reporter):
        reporter.example_pending(self)
