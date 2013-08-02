# -*- coding: utf-8 -*-

import sys
import imp
import inspect
import contextlib

from mamba import example, example_group


class _Context(object):
    pass


class describe(object):

    def __init__(self, subject):
        self.subject = subject
        self.locals_before = None
        self.context = _Context()

    def __enter__(self):
        frame = inspect.currentframe().f_back
        self.locals_before = set(frame.f_locals.keys())

        if 'examples' not in frame.f_locals:
            frame.f_locals['examples'] = []
            frame.f_locals['current_example'] = None

        if frame.f_locals['current_example'] is None:
            frame.f_locals['current_example'] = example_group.ExampleGroup(self.subject, pending=self._pending, context=self.context)
            frame.f_locals['examples'].append(frame.f_locals['current_example'])
        else:
            current = example_group.ExampleGroup(self.subject, pending=self._pending, context=self.context)
            frame.f_locals['current_example'].append(current)
            frame.f_locals['current_example'] = current

        return self.context

    @property
    def _pending(self):
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
                    frame.f_locals['current_example'].append(example.Example(code, pending=getattr(code, 'pending', False)))

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
