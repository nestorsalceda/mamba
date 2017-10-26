# -*- coding: utf-8 -*-

import inspect
import types

from mamba.example_group import ExampleGroup, PendingExampleGroup
from mamba.example import Example, PendingExample
from mamba.infrastructure import is_python3


class Loader(object):
    def load_examples_from(self, module):
        example_groups = []
        ignore_rest = False

        for klass in self._example_groups_for(module):
            if '__ignore_rest' in klass.__name__:
                example_groups = list(map(self._mark_all_as_pending, example_groups))
                example_groups.append(self._a_potentially_pending_klass(klass))
                ignore_rest = True
            elif ('__pending' in klass.__name__) or ignore_rest:
                example_groups.append(self._a_potentially_pending_klass(klass, True))
            else:
                example_groups.append(self._a_potentially_pending_klass(klass))

        loaded = self._create_example_groups_from(example_groups)

        return loaded

    def _example_groups_for(self, module):
        return [klass for name, klass in inspect.getmembers(module, inspect.isclass) if self._is_example_group(name)]

    def _is_example_group(self, class_name):
        return class_name.endswith('__description')

    def _subject(self, example_group):
        subject = getattr(example_group, '_subject_class', example_group.__name__
            .replace('__description', '')
            .replace('__pending', '')
            .replace('__ignore_rest', ''))
        if isinstance(subject, str):
            return subject[10:]
        else:
            return subject

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
        examples = []
        ignore_rest = False

        for example in self._examples_in(klass):
            if self._is_ignore_rest_example(example):
                examples = list(map(self._mark_all_as_pending, examples))
                examples.append(self._a_potentially_pending_klass(example))
                ignore_rest = True
            elif self._is_pending_example(example) or self._is_pending_example_group(example_group) or ignore_rest:
                examples.append(self._a_potentially_pending_klass(example, True))
            else:
                examples.append(self._a_potentially_pending_klass(example))

        self._create_examples_from(examples, example_group)

    def _examples_in(self, example_group):
        return [method for name, method in self._methods_for(example_group) if self._is_example(method)]

    def _methods_for(self, klass):
        return inspect.getmembers(klass, inspect.isfunction if is_python3() else inspect.ismethod)

    def _is_example(self, method):
        return method.__name__[10:].startswith('it') or self._is_pending_example(method) or self._is_ignore_rest_example(method)

    def _is_pending_example(self, example):
        return example.__name__[10:].startswith('_it')

    def _is_pending_example_group(self, example_group):
        return isinstance(example_group, PendingExampleGroup)

    def _is_ignore_rest_example(self, example):
        return example.__name__[10:].startswith('focus_it')

    def _load_nested_example_groups(self, klass, example_group):
        example_groups = []
        ignore_rest = False

        for nested in self._example_groups_for(klass):
            if isinstance(example_group, PendingExampleGroup):
                example_groups.append(self._a_potentially_pending_klass(nested, True))
            else:
                if '__ignore_rest' in nested.__name__:
                    example_groups = list(map(self._mark_all_as_pending, example_groups))
                    example_groups.append(self._a_potentially_pending_klass(nested))
                    ignore_rest = True
                elif ('__pending' in nested.__name__) or ignore_rest:
                    example_groups.append(self._a_potentially_pending_klass(nested, True))
                else:
                    example_groups.append(self._a_potentially_pending_klass(nested))
        
        self._create_example_groups_from(example_groups, example_group, example_group.execution_context)

    def _load_helper_methods_to_execution_context(self, klass, execution_context):
        helper_methods = [method for name, method in self._methods_for(klass) if not self._is_example(method)]

        for method in helper_methods:
            if is_python3():
                setattr(execution_context, method.__name__, types.MethodType(method, execution_context))
            else:
                setattr(execution_context, method.__name__, types.MethodType(method.im_func, execution_context, execution_context.__class__))

    def _create_example_groups_from(self, example_groups_model_list, example_groups=None, execution_context=None):
        if example_groups is None:
            example_groups = []

        for example_group_model in example_groups_model_list:
            example_group = self._create_example_group(example_group_model, execution_context=execution_context)
            self._add_hooks_examples_and_nested_example_groups_to(example_group_model['klass'], example_group)
            example_groups.append(example_group)

        return example_groups

    def _create_example_group(self, klass, execution_context=None):
        if klass['pending']:
            return PendingExampleGroup(self._subject(klass['klass']), execution_context=execution_context)
        return ExampleGroup(self._subject(klass['klass']), execution_context=execution_context)

    def _create_examples_from(self, examples_model, example_group):
        for example in examples_model:
            example_group.append(self._create_example(example))

    def _create_example(self, example_model):
        if example_model['pending']:
            return PendingExample(example_model['klass'])
        return Example(example_model['klass'])

    def _mark_all_as_pending(self, klass):
        klass['pending'] = True
        return klass

    def _a_potentially_pending_klass(self, klass, pending=None):
        if pending is None:
            pending = False

        return {
            "klass": klass,
            "pending": pending
        }

