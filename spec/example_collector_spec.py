# -*- coding: utf-8 -*-

import os
import sys
import inspect

from mamba import describe, context, example, example_group, before
from mamba.example_collector import ExampleCollector
from sure import expect


def spec_relpath(name):
    return os.path.join('spec', 'fixtures', name)


def spec_abspath(name):
    return os.path.join(os.path.dirname(__file__), 'fixtures', name)


IRRELEVANT_PATH = spec_abspath('without_inner_contexts.py')
PENDING_DECORATOR_PATH = spec_abspath('with_pending_decorator.py')
PENDING_DECORATOR_AS_ROOT_PATH = spec_abspath('with_pending_decorator_as_root.py')
WITH_RELATIVE_IMPORT_PATH = spec_abspath('with_relative_import.py')


def _load_module(path):
    example_collector = ExampleCollector([path])
    return list(example_collector.modules())[0]


with describe(ExampleCollector) as _:
    with context('when loading from file'):
        def it_should_load_the_module_from_absolute_path():
            module = _load_module(IRRELEVANT_PATH)

            expect(inspect.ismodule(module)).to.be.true

        def it_should_load_the_module_from_relative_path():
            module = _load_module(spec_relpath('without_inner_contexts.py'))

            expect(inspect.ismodule(module)).to.be.true

        def it_should_unload_module_when_finished():
            module = _load_module(IRRELEVANT_PATH)
            name = module.__name__

            expect(sys.modules).to_not.contain(name)

        def it_should_restore_pythonpath_when_finished_from_absolute_path():
            old_path = list(sys.path)

            module = _load_module(IRRELEVANT_PATH)

            expect(sys.path).to.equal(old_path)

        def it_should_restore_pythonpath_when_finished_from_relative_path():
            old_path = list(sys.path)

            module = _load_module(spec_relpath('without_inner_contexts.py'))

            expect(sys.path).to.equal(old_path)

    def it_should_order_by_line_number_without_inner_context():
        module = _load_module(spec_abspath('without_inner_contexts.py'))

        expect(module.examples).to.have.length_of(1)
        expect([example.name for example in module.examples[0].examples]).to.be.equal(['first_example', 'second_example', 'third_example'])

    def it_should_put_examples_together_and_groups_at_last():
        module = _load_module(spec_abspath('with_inner_contexts.py'))

        expect(module.examples).to.have.length_of(1)
        expect([example.name for example in module.examples[0].examples]).to.be.equal(['first_example', 'second_example', 'third_example', '#inner_context'])

    with context('when a pending decorator loaded'):
        def it_should_mark_example_as_pending():
            module = _load_module(PENDING_DECORATOR_AS_ROOT_PATH)

            expect(module.examples).to.have.length_of(1)
            expect(module.examples[0].examples[0]).to.be.a(example.PendingExample)

        def it_should_mark_example_group_as_pending():
            module = _load_module(PENDING_DECORATOR_AS_ROOT_PATH)

            expect(module.examples).to.have.length_of(1)
            expect(module.examples[0].examples[1]).to.be.a(example_group.PendingExampleGroup)

    with context('when a pending decorator loaded_as_root'):
        def it_should_mark_inner_examples_as_pending():
            module = _load_module(PENDING_DECORATOR_AS_ROOT_PATH)

            expect(module.examples).to.have.length_of(1)
            examples_in_root = module.examples[0].examples

            expect(examples_in_root).to.have.length_of(2)
            expect(examples_in_root[0]).to.be.a(example.PendingExample)
            expect(examples_in_root[1]).to.be.a(example_group.PendingExampleGroup)
            expect(examples_in_root[1].examples[0]).to.be.a(example.PendingExample)

    with context('when loading with relative import'):
        def it_should_load_the_module_and_perform_relative_import():
            module = _load_module(WITH_RELATIVE_IMPORT_PATH)

            expect(module).to.have.property('HelperClass')
