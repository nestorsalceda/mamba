# -*- coding: utf-8 -*-

import sys
import imp
import inspect
import contextlib

from mamba import example, example_group


class _Factory(object):

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
        self.factory = _Factory()

    def __enter__(self):
        frame = inspect.currentframe().f_back
        self.locals_before = set(frame.f_locals.keys())

        if not self._is_initialized(frame):
            self._initialize(frame)

        if self._is_root_example(frame):
            self._create_root_example_and_make_it_current(frame)
        else:
            self._create_inner_example_group_and_make_it_current(frame)

        return self.context

    def _is_initialized(self, frame):
        return 'examples' in frame.f_locals

    def _initialize(self, frame):
        frame.f_locals['examples'] = []
        frame.f_locals['current_example'] = None

    def _is_root_example(self, frame):
        return frame.f_locals['current_example'] is None

    def _create_root_example_and_make_it_current(self, frame):
        frame.f_locals['current_example'] = self.factory.create_root_example_group(self.subject, self.context, self._marked_as_pending)
        frame.f_locals['examples'].append(frame.f_locals['current_example'])

    @property
    def _marked_as_pending(self):
        return getattr(self, 'pending', False)

    def _create_inner_example_group_and_make_it_current(self, frame):
        current = self.factory.create_example_group(self.subject, self.context, frame.f_locals['current_example'], self._marked_as_pending)

        frame.f_locals['current_example'].append(current)
        frame.f_locals['current_example'] = current

    def __exit__(self, type, value, traceback):
        frame = inspect.currentframe().f_back

        self._load_examples_or_hooks(frame)
        self._sort_loaded_examples(frame)
        self._make_parent_as_current_example(frame)

    def _load_examples_or_hooks(self, frame):
        current = frame.f_locals['current_example']

        for function in self._get_examples_or_hooks_from(frame):
            code = frame.f_locals[function]
            if self._is_hook(code):
                self._load_hooks(function, code, current)
            else:
                self._load_example(code, current)

    def _get_examples_or_hooks_from(self, frame):
        possible_examples = set(frame.f_locals.keys()) - self.locals_before

        return [example for example in possible_examples if self._is_example_or_hook(example, frame)]

    def _is_example_or_hook(self, example, frame):
        return self._is_public_function(example, frame.f_locals[example]) and not self._is_already_loaded(frame.f_locals[example])

    def _is_public_function(self, function, code):
        return callable(code) and not function.startswith('_')

    def _is_already_loaded(self, code):
        return getattr(code, '_loaded', False)

    def _is_hook(self, function):
        return getattr(function, 'hook', [])

    def _load_hooks(self, function, code, current):
        current.hooks['%s_%s' % (code.hook['where'], code.hook['when'])].append(code)
        self._mark_as_loaded(code)

    def _mark_as_loaded(self, code):
        code._loaded = True

    def _load_example(self, code, current):
        current.append(self.factory.create_example(code, current))
        self._mark_as_loaded(code)

    def _sort_loaded_examples(self, frame):
        frame.f_locals['current_example'].examples.sort(key=lambda x: x.source_line)

    def _make_parent_as_current_example(self, frame):
        frame.f_locals['current_example'] = frame.f_locals['current_example'].parent


context = describe

