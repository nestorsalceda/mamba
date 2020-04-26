# -*- coding: utf-8 -*-

import inspect

from mamba.example_group import ExampleGroup, PendingExampleGroup, SharedExampleGroup
from mamba.example import Example, PendingExample


class Loader(object):
    def load_examples_from(self, module):
        self.module = module
        loaded = []
        example_groups = self._example_groups_for(module)

        for klass in example_groups:
            example_group = self._create_example_group(klass)
            self._add_hooks_examples_and_nested_example_groups_to(klass, example_group)

            loaded.append(example_group)

        return loaded

    def _example_groups_for(self, module):
        return [klass for name, klass in inspect.getmembers(module, inspect.isclass) if self._is_example_group(klass)]

    def _is_example_group(self, klass):
        return getattr(klass, '_example_group', False)

    def _create_example_group(self, klass):
        name = klass._example_name
        tags = klass._tags

        if klass._pending:
            return PendingExampleGroup(name, tags=tags)
        elif klass._shared:
            return SharedExampleGroup(name, tags=tags)
        return ExampleGroup(name, tags=tags)

    def _add_hooks_examples_and_nested_example_groups_to(self, klass, example_group):
        self._load_hooks(klass, example_group)
        self._load_examples(klass, example_group)
        self._load_helper_methods(klass, example_group)
        self._load_nested_example_groups(klass, example_group)

    def _load_hooks(self, klass, example_group):
        for hook in self._hooks_in(klass):
            example_group.hooks[hook.__name__].append(hook)

    def _hooks_in(self, example_group):
        return [method for name, method in self._methods_for(example_group) if self._is_hook(name)]

    def _is_hook(self, method_name):
        return method_name.startswith('before') or method_name.startswith('after')

    def _load_examples(self, klass, example_group):
        for example in self._examples_in(klass):
            tags = example._tags
            if self._is_pending_example(example) or self._is_pending_example_group(example_group):
                example_group.append(PendingExample(example, tags=tags, module=self.module))
            else:
                example_group.append(Example(example, tags=tags, module=self.module))

    def _examples_in(self, example_group):
        return [method for name, method in self._methods_for(example_group) if self._is_example(method)]

    def _methods_for(self, klass):
        return inspect.getmembers(klass, inspect.isfunction)

    def _is_example(self, method):
        return getattr(method, '_example', False)

    def _is_focused_example(self, example):
        return 'focus' in example._tags

    def _is_pending_example(self, example):
        return example._pending

    def _is_pending_example_group(self, example_group):
        return isinstance(example_group, PendingExampleGroup)

    def _load_nested_example_groups(self, klass, example_group):
        for nested in self._example_groups_for(klass):
            if isinstance(example_group, PendingExampleGroup):
                nested_example_group = PendingExampleGroup(nested._example_name)
            else:
                nested_example_group = self._create_example_group(nested)

            nested_example_group.helpers = dict(example_group.helpers)
            self._add_hooks_examples_and_nested_example_groups_to(nested, nested_example_group)
            example_group.append(nested_example_group)

    def _load_helper_methods(self, klass, example_group):
        helper_methods = [method for name, method in self._methods_for(klass) if not self._is_example(method)]

        for method in helper_methods:
            example_group.helpers[method.__name__] = method
