# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import inspect


class ExampleGroup(object):

    def __init__(self, subject, parent=None, pending=False, context=None):
        self.subject = subject
        self.specs = []
        self.parent = parent
        self.pending = pending
        self.context = context
        self.hooks = {'before_each': [], 'after_each': [], 'before_all': [], 'after_all': []}
        self._elapsed_time = timedelta(0)

    def run(self, reporter):
        self._register_subject_creation_in_before_each_hook()
        self._run_specs(reporter)

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

    def _run_specs(self, reporter):
        reporter.spec_group_started(self)
        try:
            begin = datetime.utcnow()
            self._run_inner_specs(reporter)
        except Exception as exception:
            self.exception = exception
        finally:
            self._elapsed_time = datetime.utcnow() - begin
            reporter.spec_group_finished(self)

    def _run_inner_specs(self, reporter):
        self.run_hook('before_all')
        for spec in self.specs:
            spec.run(reporter)
        self.run_hook('after_all')

    def run_hook(self, hook):
        for registered in self.hooks.get(hook, []):
            if callable(registered):
                registered()

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @property
    def name(self):
        if self.subject_is_class:
            return self.subject.__name__
        return self.subject

    def append(self, spec):
        self.specs.append(spec)
        spec.parent = self

    @property
    def failed(self):
        return any(spec.failed for spec in self.specs)

    @property
    def pending(self):
        if self.parent:
            return self._pending or self.parent.pending
        return self._pending

    @pending.setter
    def pending(self, value):
        self._pending = value

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, value):
        self._exception = value

        for spec in self.specs:
            spec.exception = value

    @property
    def subject_is_class(self):
        return inspect.isclass(self.subject)

    @property
    def depth(self):
        if self.parent is None:
            return 0

        return self.parent.depth + 1
