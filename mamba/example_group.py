# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
import inspect

from mamba import error
from mamba.example import Example, PendingExample

class ExecutionContext(object):
    pass

class ExampleGroup(object):

    def __init__(self, subject, parent=None, execution_context=None):
        self.subject = subject
        self.examples = []
        self.parent = parent
        self.hooks = {'before_each': [], 'after_each': [], 'before_all': [], 'after_all': []}
        self._elapsed_time = timedelta(0)
        self.execution_context = ExecutionContext() if execution_context is None else execution_context

    def run(self, reporter):
        self._start(reporter)
        try:
            self._run_inner_examples(reporter)
        except Exception as exception:
            self._set_failed()
        finally:
            self._finish(reporter)

    def _start(self, reporter):
        self._register_subject_creation_in_before_each_hook()
        self._begin = datetime.utcnow()
        reporter.example_group_started(self)

    def _register_subject_creation_in_before_each_hook(self):
        if self._can_create_subject():
            self.hooks['before_each'].insert(0, lambda execution_context: self._create_subject(execution_context))

    def _can_create_subject(self):
        return self._subject_is_class()

    def _subject_is_class(self):
        return inspect.isclass(self.subject)

    #TODO: Being executed on every example, instead of try once
    #      Should be optimized
    def _create_subject(self, execution_context):
        try:
            execution_context.subject = self.subject()
        except Exception as exc:
            if hasattr(execution_context, 'subject'):
                del execution_context.subject

    def _run_inner_examples(self, reporter):
        self.run_hook('before_all')
        for example in self.examples:
            example.run(reporter)
        self.run_hook('after_all')

    def run_hook(self, hook):
        for registered in self.hooks.get(hook, []):
            try:
                if hasattr(registered, 'im_func'):
                    registered.im_func(self.execution_context)
                elif callable(registered):
                    registered(self.execution_context)
            except Exception as exception:
                self._set_failed()

    def _set_failed(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)

    def _finish(self, reporter):
        self._elapsed_time = datetime.utcnow() - self._begin
        reporter.example_group_finished(self)

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @property
    def name(self):
        if self._subject_is_class():
            return self.subject.__name__
        return self.subject

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

    def run(self, reporter):
        reporter.example_group_pending(self)
        self._run_inner_examples(reporter)

    def _run_inner_examples(self, reporter):
        for example in self.examples:
            example.run(reporter)

    def append(self, example):
        if not type(example) in [PendingExample, PendingExampleGroup]:
            raise TypeError('A pending example or example group expected')

        super(PendingExampleGroup, self).append(example)
