# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
import inspect

from mamba import error
from mamba.example import Example, PendingExample
from mamba.infrastructure import retrieve_unbound_method_from


class ExecutionContext(object):
    pass

class ExampleGroup(object):

    def __init__(self, subject, parent=None, execution_context=None):
        self.subject = subject
        self._can_instantiate_subject = True
        self.examples = []
        self.parent = parent
        self._hooks = {'before_each': [], 'after_each': [], 'before_all': [], 'after_all': []}
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
        if not self._can_create_subject():
            return

        self._hooks['before_each'].insert(0, lambda execution_context: self._create_subject_in(execution_context))

    def _can_create_subject(self):
        return self._subject_is_class() and self._can_instantiate_subject

    def _subject_is_class(self):
        return inspect.isclass(self.subject)

    def _create_subject_in(self, execution_context):
        try:
            execution_context.subject = self.subject()
        except Exception as exc:
            self._can_instantiate_subject = False
            self._remove_any_existing_subject_from(execution_context)

    def _remove_any_existing_subject_from(self, execution_context):
        if not hasattr(execution_context, 'subject'):
            return

        del execution_context.subject

    def _run_inner_examples(self, reporter):
        self.run_hook('before_all')
        for example in self.examples:
            example.run(reporter)
        self.run_hook('after_all')

    def run_hook(self, name):
        for hook in self._hooks.get(name, []):
            try:
                hook(self.execution_context)
            except Exception as exception:
                self._set_failed()

    def _set_failed(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)

    def _finish(self, reporter):
        self._elapsed_time = datetime.utcnow() - self._begin
        reporter.example_group_finished(self)

    def add_hook(self, name, hook_function):
        self._hooks[name].append(retrieve_unbound_method_from(hook_function))

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
