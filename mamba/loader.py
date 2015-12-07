# -*- coding: utf-8 -*-

import inspect
import types

from mamba.example_group import ExampleGroup, PendingExampleGroup
from mamba.example import Example, PendingExample
from mamba.infrastructure import is_python3


class Loader(object):
    def load_examples_from(self, module):
        loaded = []

        for klass in self._top_level_classes_in(module):
            example_group = self._create_example_group(klass)
            self._add_hooks_examples_and_nested_example_groups_to(klass, example_group)

            loaded.append(example_group)

        return loaded

    def _top_level_classes_in(self, an_object):
        return [klass for class_name, klass in self._classes_in(an_object) if self._is_name_of_example_group(class_name)]

    def _classes_in(self, an_object):
        return inspect.getmembers(an_object, inspect.isclass)

    def _is_name_of_example_group(self, class_name):
        return class_name.endswith('__description')

    def _create_example_group(self, klass, execution_context=None):
        if '__pending' in klass.__name__:
            return PendingExampleGroup(self._subject(klass), execution_context=execution_context)
        return ExampleGroup(self._subject(klass), execution_context=execution_context)

    def _subject(self, example_group):
        return getattr(
            example_group,
            '_subject_class',
            self._generate_default_subject(example_group)
        )

    def _generate_default_subject(self, example_group):
        return example_group.__name__.replace('__description', '').replace('__pending', '')[10:]

    def _add_hooks_examples_and_nested_example_groups_to(self, klass, example_group):
        self._load_hooks(klass, example_group)
        self._load_examples(klass, example_group)
        self._load_nested_example_groups(klass, example_group)
        self._load_helper_methods_to_execution_context(klass, example_group.execution_context)

    def _load_hooks(self, klass, example_group):
        for hook in self._hooks_in(klass):
            example_group.hooks[hook.__name__].append(hook)

    def _hooks_in(self, klass):
        return [method for name, method in self._methods_in(klass) if self._is_name_of_hook(name)]

    def _methods_in(self, klass):
        return inspect.getmembers(klass, inspect.isfunction if is_python3() else inspect.ismethod)

    def _is_name_of_hook(self, method_name):
        return method_name.startswith('before') or method_name.startswith('after')

    def _load_examples(self, klass, example_group):
        for example in self._examples_in(klass):
            if self._is_pending_example(example) or self._is_pending_example_group(example_group):
                example_group.append(PendingExample(example))
            else:
                example_group.append(Example(example))

    def _examples_in(self, klass):
        return [method for name, method in self._methods_in(klass) if self._is_example(method)]

    def _is_example(self, method):
        return method.__name__[10:].startswith('it') or self._is_pending_example(method)

    def _is_pending_example(self, example):
        return example.__name__[10:].startswith('_it')

    def _is_pending_example_group(self, example_group):
        return isinstance(example_group, PendingExampleGroup)

    def _load_nested_example_groups(self, klass, example_group):
        for nested_class in self._top_level_classes_in(klass):
            if self._is_pending_example_group(example_group):
                nested_example_group = PendingExampleGroup(self._subject(nested_class), execution_context=example_group.execution_context)
            else:
                nested_example_group = self._create_example_group(nested_class, execution_context=example_group.execution_context)

            self._add_hooks_examples_and_nested_example_groups_to(nested_class, nested_example_group)
            example_group.append(nested_example_group)

    def _load_helper_methods_to_execution_context(self, klass, execution_context):
        for helper_method in self._helper_methods_in(klass):
            self._add_method_to_execution_context(helper_method, execution_context)

    def _helper_methods_in(self, klass):
        return [method for name, method in self._methods_in(klass) if self._is_helper_method(method)]

    def _is_helper_method(self, method):
        return not self._is_example(method)

    def _add_method_to_execution_context(self, method, execution_context):
        setattr(execution_context, method.__name__, self._create_method_bound_to_object(method, execution_context))

    def _create_method_bound_to_object(self, method, an_object):
        if is_python3():
            return types.MethodType(method, an_object)
        else:
            return types.MethodType(method.im_func, an_object, an_object.__class__)
