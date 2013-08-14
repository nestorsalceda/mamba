# -*- coding: utf-8 -*-

import sys
import imp
import inspect
import contextlib

from mamba import example, example_group


class Factory(object):

    def create_root_example_group(self, subject, context, marked_as_pending):
        if marked_as_pending is False:
            return example_group.ExampleGroup(subject, context=context)

        return example_group.PendingExampleGroup(subject, context=context)

    def create_example_group(self, subject, context, parent, marked_as_pending):
        if self._is_a_pending_example_group(parent, marked_as_pending):
            return example_group.PendingExampleGroup(subject, context=context)

        return example_group.ExampleGroup(subject, context=context)

    def _is_a_pending_example_group(self, parent, marked_as_pending):
        parent_marked_as_pending = isinstance(parent, example_group.PendingExampleGroup)

        return marked_as_pending or parent_marked_as_pending

    def create_example(self, code, parent):
        if self._is_a_pending_example(code, parent):
            return example.PendingExample(code)

        return example.Example(code)

    def _is_a_pending_example(self, code, parent):
        marked_as_pending = getattr(code, 'pending', False)
        parent_marked_as_pending = isinstance(parent, example_group.PendingExampleGroup)

        return marked_as_pending or parent_marked_as_pending

class _Context(object):
    pass


class describe(object):

    def __init__(self, subject):
        self.subject = subject
        self.locals_before = None
        self.context = _Context()
        self.factory = Factory()

    def __enter__(self):
        frame = inspect.currentframe().f_back
        self.locals_before = set(frame.f_locals.keys())

        if 'examples' not in frame.f_locals:
            frame.f_locals['examples'] = []
            frame.f_locals['current_example'] = None

        if frame.f_locals['current_example'] is None:
            frame.f_locals['current_example'] = self.factory.create_root_example_group(self.subject, self.context, self._marked_as_pending)
            frame.f_locals['examples'].append(frame.f_locals['current_example'])
        else:
            current = self.factory.create_example_group(self.subject, self.context, frame.f_locals['current_example'], self._marked_as_pending)
            frame.f_locals['current_example'].append(current)
            frame.f_locals['current_example'] = current

        return self.context

    @property
    def _marked_as_pending(self):
        return getattr(self, 'pending', False)

    def __exit__(self, type, value, traceback):
        frame = inspect.currentframe().f_back

        possible_examples = set(frame.f_locals.keys()) - self.locals_before

        for function in possible_examples:
            code = frame.f_locals[function]

            if self._is_non_private_function(function, code) and not self._is_registered(code):
                self._register(code)
                if self._is_hook(code):
                    self._load_hooks(function, code, frame.f_locals['current_example'])
                else:
                    example = self.factory.create_example(code, frame.f_locals['current_example'])
                    frame.f_locals['current_example'].append(example)

        frame.f_locals['current_example'].examples.sort(key=lambda x: x.source_line)
        frame.f_locals['current_example'] = frame.f_locals['current_example'].parent

    def _is_non_private_function(self, function, code):
        return callable(code) and not function.startswith('_')

    def _is_registered(self, code):
        return getattr(code, '_registered', False)

    def _register(self, code):
        code._registered = True

    def _is_hook(self, function):
        return getattr(function, 'hook', [])

    def _load_hooks(self, function, code, current_example):
        current_example.hooks['%s_%s' % (code.hook['where'], code.hook['when'])].append(code)

context = describe


class Loader(object):

    @contextlib.contextmanager
    def load_from_file(self, path):
        name = path.replace('.py', '')
        try:
            yield imp.load_source(name, path)
        finally:
            if name in sys.modules:
                del sys.modules[name]
