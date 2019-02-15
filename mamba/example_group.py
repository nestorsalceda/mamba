# -*- coding: utf-8 -*-

import copy
from datetime import datetime

from mamba import runnable
from mamba.example import PendingExample


class ExampleGroup(runnable.Runnable):

    def __init__(self, description, parent=None, tags=None):
        super(ExampleGroup, self).__init__(parent=parent, tags=tags)

        self.description = description
        self.examples = []
        self.hooks = {
            'before_each': [],
            'after_each': [],
            'before_all': [],
            'after_all': []
        }
        self.helpers = {}
        self._before_all_executed = False

    def __iter__(self):
        return iter(self.examples)

    def execute(self, reporter, execution_context, tags=None):
        if not self.included_in_execution(tags):
            return

        self._start(reporter)
        try:
            self.execute_hook('before_all', execution_context)

            for example in self:
                example_execution_context = copy.copy(execution_context)
                self._bind_helpers_to(example_execution_context)
                example.execute(reporter,
                                example_execution_context,
                                tags=tags)

            self.execute_hook('after_all', execution_context)
        except Exception:
            self.fail()

        self._finish(reporter)

    def included_in_execution(self, tags):
        if any(example.included_in_execution(tags) for example in self):
            return True

        return super(ExampleGroup, self).included_in_execution(tags)

    def _start(self, reporter):
        self._begin = datetime.utcnow()
        reporter.example_group_started(self)

    def _bind_helpers_to(self, execution_context):
        for name, method in self.helpers.items():
            setattr(execution_context,
                    name,
                    method.__get__(execution_context))

    def execute_hook(self, hook, execution_context):
        if hook.endswith('_all') and not self.hooks.get(hook):
            return

        if self.parent is not None and hook.startswith("before") and not hook.endswith("_all"):
            self.parent.execute_hook(hook, execution_context)

        for registered in self.hooks.get(hook, []):
            try:
                if hasattr(registered, 'im_func'):
                    registered.im_func(execution_context)
                elif callable(registered):
                    registered(execution_context)
            except Exception:
                self.fail()

        if self.parent is not None and hook.startswith("after") and not hook.endswith("_all"):
            self.parent.execute_hook(hook, execution_context)


    def _finish(self, reporter):
        self.elapsed_time = datetime.utcnow() - self._begin
        reporter.example_group_finished(self)

    @property
    def name(self):
        return self.description.split('--')[0]

    def append(self, example):
        self.examples.append(example)
        example.parent = self

    def failed(self):
        return any(example.failed() for example in self.examples)

    def fail(self):
        super(ExampleGroup, self).fail()

        for example in self.examples:
            example.fail()


class PendingExampleGroup(ExampleGroup):

    def execute(self, reporter, execution_context, tags=None):
        reporter.example_group_pending(self)

        for example in self:
            example.execute(reporter, copy.copy(execution_context))

    def append(self, example):
        if not type(example) in [PendingExample, PendingExampleGroup]:
            raise TypeError('A pending example or example group expected')

        super(PendingExampleGroup, self).append(example)


class SharedExampleGroup(ExampleGroup):
    def execute(self, reporter, execution_context, tags=None):
        pass
