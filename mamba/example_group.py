# -*- coding: utf-8 -*-

import sys
from datetime import datetime

from mamba import error, runnable
from mamba.example import PendingExample


class ExampleGroup(runnable.Runnable):

    def __init__(self, description, parent=None, execution_context=None):
        self.description = description
        self.examples = []
        self.parent = parent
        self.hooks = {
            'before_each': [],
            'after_each': [],
            'before_all': [],
            'after_all': []
        }
        self.execution_context = runnable.ExecutionContext() if execution_context is None else execution_context

    def __iter__(self):
        return iter(self.examples)

    def execute(self, reporter):
        self._start(reporter)

        try:
            for example in iter(self):
                self.execution_context = runnable.ExecutionContext()
                example.execute(reporter)
        except Exception:
            self._set_failed()

        self._finish(reporter)

    def _start(self, reporter):
        self._begin = datetime.utcnow()
        reporter.example_group_started(self)

    def _set_failed(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)

    def _finish(self, reporter):
        self.elapsed_time = datetime.utcnow() - self._begin
        reporter.example_group_finished(self)

    def run(self, reporter):
        self._start(reporter)
        try:
            self._run_inner_examples(reporter)
        except Exception:
            self._set_failed()
        finally:
            self._finish(reporter)

    def _run_inner_examples(self, reporter):
        self.run_hook('before_all')
        for example in iter(self):
            example.run(reporter)
        self.run_hook('after_all')

    def run_hook(self, hook):
        if self.parent is not None:
            self.parent.run_hook(hook)

        for registered in self.hooks.get(hook, []):
            try:
                if hasattr(registered, 'im_func'):
                    registered.im_func(self.execution_context)
                elif callable(registered):
                    registered(self.execution_context)
            except Exception:
                self._set_failed()

    @property
    def name(self):
        return self.description

    def append(self, example):
        self.examples.append(example)
        example.parent = self

    @property
    def failed(self):
        return any(example.failed for example in self.examples)

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

        for example in self.examples:
            example.error = value


class PendingExampleGroup(ExampleGroup):

    def execute(self, reporter):
        reporter.example_group_pending(self)
        for example in iter(self):
            example.execute(reporter)

    def run(self, reporter):
        self.execute(reporter)

    def append(self, example):
        if not type(example) in [PendingExample, PendingExampleGroup]:
            raise TypeError('A pending example or example group expected')

        super(PendingExampleGroup, self).append(example)
