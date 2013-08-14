# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
import inspect

from mamba import error


class ExampleGroup(object):

    def __init__(self, subject, parent=None, pending=False, context=None):
        self.subject = subject
        self.examples = []
        self.parent = parent
        self.pending = pending
        self.context = context
        self.hooks = {'before_each': [], 'after_each': [], 'before_all': [], 'after_all': []}
        self._elapsed_time = timedelta(0)

    def run(self, reporter):
        self._register_subject_creation_in_before_each_hook()
        self._run_examples(reporter)

    def _register_subject_creation_in_before_each_hook(self):
        if self._can_create_subject():
            self.hooks['before_each'].insert(0, self._create_subject)

    def _can_create_subject(self):
        if not self.subject_is_class:
            return False

        try:
            self.subject()
            return True
        except:
            return False

    def _create_subject(self):
        try:
            self.context.subject = self.subject()
        except:
            pass

    def _run_examples(self, reporter):
        reporter.example_group_started(self)
        try:
            begin = datetime.utcnow()
            self._run_inner_examples(reporter)
        except Exception as exception:
            self._set_failed()
        finally:
            self._elapsed_time = datetime.utcnow() - begin
            reporter.example_group_finished(self)

    def _run_inner_examples(self, reporter):
        self.run_hook('before_all')
        for example in self.examples:
            example.run(reporter)
        self.run_hook('after_all')

    def run_hook(self, hook):
        for registered in self.hooks.get(hook, []):
            if callable(registered):
                registered()

    def _set_failed(self):
        type_, value, traceback = sys.exc_info()
        self.error = error.Error(value, traceback)

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @property
    def name(self):
        if self.subject_is_class:
            return self.subject.__name__
        return self.subject

    def append(self, example):
        self.examples.append(example)
        example.parent = self

    @property
    def failed(self):
        return any(example.failed for example in self.examples)

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

        for example in self.examples:
            example.error = value

    @property
    def subject_is_class(self):
        return inspect.isclass(self.subject)

    @property
    def depth(self):
        if self.parent is None:
            return 0

        return self.parent.depth + 1

    @property
    def source_line(self):
        return float('inf')
