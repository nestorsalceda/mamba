# -*- coding: utf-8 -*-

import inspect
import types

from mamba.example_group import ExampleGroup, PendingExampleGroup
from mamba.example import Example, PendingExample
from mamba.infrastructure import is_python3


class Loader(object):
    def load_examples_from(self, module):
        return [
            self._create_example_group(klass)
            for klass in self._top_level_classes_in(module)
        ]

    def _create_example_group(self, klass):
        example_group = self._create_bare_example_group(klass)
        self._add_hooks_examples_and_nested_example_groups_to(klass, example_group)

        return example_group

    def _create_bare_example_group(self, klass, execution_context=None):
        if '__pending' in klass.__name__:
            return PendingExampleGroup(self._subject_of(klass), execution_context=execution_context)
        return ExampleGroup(self._subject_of(klass), execution_context=execution_context)

    def _subject_of(self, klass):
        return getattr(
            klass,
            '_subject_class',
            self._generate_default_subject(klass)
        )

    def _generate_default_subject(self, klass):
        return klass.__name__.replace('__description', '').replace('__pending', '')[10:]

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
        for method in self._methods_representing_examples_in(klass):
            if self._is_name_of_pending_example(method.__name__) or self._is_pending_example_group(example_group):
                example_group.append(PendingExample(method))
            else:
                example_group.append(Example(method))

    def _methods_representing_examples_in(self, klass):
        return [method for name, method in self._methods_in(klass) if self._is_name_of_example(name)]

    def _is_name_of_example(self, name):
        return name[10:].startswith('it') or self._is_name_of_pending_example(name)

    def _is_name_of_pending_example(self, name):
        return name[10:].startswith('_it')

    def _is_pending_example_group(self, example_group):
        return isinstance(example_group, PendingExampleGroup)

    def _load_nested_example_groups(self, klass, example_group):
        for nested_class in self._top_level_classes_in(klass):
            if self._is_pending_example_group(example_group):
                nested_example_group = PendingExampleGroup(self._subject_of(nested_class), example_group.execution_context)
            else:
                nested_example_group = self._create_bare_example_group(nested_class, example_group.execution_context)

            self._add_hooks_examples_and_nested_example_groups_to(nested_class, nested_example_group)
            example_group.append(nested_example_group)

    def _top_level_classes_in(self, an_object):
        return [klass for name, klass in self._classes_in(an_object) if self._is_name_of_example_group(name)]

    def _classes_in(self, an_object):
        return inspect.getmembers(an_object, inspect.isclass)

    def _is_name_of_example_group(self, name):
        return name.endswith('__description')

    def _load_helper_methods_to_execution_context(self, klass, execution_context):
        for helper_method in self._helper_methods_in(klass):
            self._add_method_to_execution_context(helper_method, execution_context)

    def _helper_methods_in(self, klass):
        return [method for name, method in self._methods_in(klass) if self._is_name_of_helper_method(name)]

    def _is_name_of_helper_method(self, name):
        return not self._is_name_of_example(name)

    def _add_method_to_execution_context(self, method, execution_context):
        setattr(execution_context, method.__name__, self._create_method_bound_to_object(method, execution_context))

    def _create_method_bound_to_object(self, method, an_object):
        if is_python3():
            return types.MethodType(method, an_object)
        return types.MethodType(method.im_func, an_object, an_object.__class__)
