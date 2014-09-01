# -*- coding: utf-8 -*-

import inspect
import types

from mamba.example_group import ExampleGroup, PendingExampleGroup
from mamba.example import Example, PendingExample
from mamba.infrastructure import is_python3


class Loader(object):
    def load_examples_from(self, module):
        loaded = []
        example_groups = self._example_groups_for(module)

        for klass in example_groups:
            example_group = self._create_example_group(klass)
            self._add_hooks_examples_and_nested_example_groups_to(klass, example_group)

            loaded.append(example_group)

        return loaded

    def _example_groups_for(self, module):
        return [klass for name, klass in inspect.getmembers(module, inspect.isclass) if self._is_example_group(name)]

    def _is_example_group(self, class_name):
        return class_name.endswith('__description')

    def _create_example_group(self, klass, execution_context=None):
        if '__pending' in klass.__name__:
            return PendingExampleGroup(self._subject(klass), execution_context=execution_context)
        return ExampleGroup(self._subject(klass), execution_context=execution_context)

    def _subject(self, example_group):
        return getattr(example_group, '_subject_class', example_group.__name__.replace('__description', '').replace('__pending', ''))

    def _add_hooks_examples_and_nested_example_groups_to(self, klass, example_group):
        self._load_hooks(klass, example_group)
        self._load_examples(klass, example_group)
        self._load_nested_example_groups(klass, example_group)
        self._load_helper_methods_to_execution_context(klass, example_group.execution_context)

    def _load_hooks(self, klass, example_group):
        for hook in self._hooks_in(klass):
            example_group.hooks[hook.__name__].append(hook)

    def _hooks_in(self, example_group):
        return [method for name, method in self._methods_for(example_group) if self._is_hook(name)]

    def _is_hook(self, method_name):
        return method_name.startswith('before') or method_name.startswith('after')

    def _load_examples(self, klass, example_group):
        for example in self._examples_in(klass):
            if self._is_pending_example(example) or self._is_pending_example_group(example_group):
                example_group.append(PendingExample(example))
            else:
                example_group.append(Example(example))

    def _examples_in(self, example_group):
        return [method for name, method in self._methods_for(example_group) if self._is_example(method)]

    def _methods_for(self, klass):
        return inspect.getmembers(klass, inspect.isfunction if is_python3() else inspect.ismethod)

    def _is_example(self, method):
        return method.__name__.startswith('it') or self._is_pending_example(method)

    def _is_pending_example(self, example):
        return example.__name__.startswith('_it')

    def _is_pending_example_group(self, example_group):
        return isinstance(example_group, PendingExampleGroup)

    def _load_nested_example_groups(self, klass, example_group):
        for nested in self._example_groups_for(klass):
            if isinstance(example_group, PendingExampleGroup):
                nested_example_group = PendingExampleGroup(self._subject(nested), execution_context=example_group.execution_context)
            else:
                nested_example_group = self._create_example_group(nested, execution_context=example_group.execution_context)

            self._add_hooks_examples_and_nested_example_groups_to(nested, nested_example_group)
            example_group.append(nested_example_group)

    def _load_helper_methods_to_execution_context(self, klass, execution_context):
        helper_methods = [method for name, method in self._methods_for(klass) if not self._is_example(method)]

        for method in helper_methods:
            if is_python3():
                setattr(execution_context, method.__name__, types.MethodType(method, execution_context))
            else:
                setattr(execution_context, method.__name__, types.MethodType(method.im_func, execution_context, execution_context.__class__))

