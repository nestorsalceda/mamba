# -*- coding: utf-8 -*-

import os
import sys
import inspect

from mamba import describe, context
from mamba.loader import Loader
from sure import expect

IRRELEVANT_PATH = os.path.join(os.path.dirname(__file__), 'fixtures', 'without_inner_contexts.py')
SKIP_DECORATOR_PATH = os.path.join(os.path.dirname(__file__), 'fixtures', 'with_pending_decorator.py')


with describe(Loader) as _:

    with context('when loading from file'):
        def it_should_loads_the_module():
            with _.subject.load_from_file(IRRELEVANT_PATH) as module:
                expect(inspect.ismodule(module)).to.be.true

        def it_should_unload_module_when_finished():
            with _.subject.load_from_file(IRRELEVANT_PATH) as module:
                name = module.__name__

            expect(sys.modules).to_not.contain(name)

    def it_should_order_by_line_number_without_inner_context():
        spec = os.path.join(os.path.dirname(__file__), 'fixtures', 'without_inner_contexts.py')

        with _.subject.load_from_file(spec) as module:
            expect(module.examples).to.have.length_of(1)
            expect([example.name for example in module.examples[0].examples]).to.be.equal(['first_example', 'second_example', 'third_example'])

    def it_should_put_examples_together_and_groups_at_last():
        spec = os.path.join(os.path.dirname(__file__), 'fixtures', 'with_inner_contexts.py')

        with _.subject.load_from_file(spec) as module:
            expect(module.examples).to.have.length_of(1)
            expect([example.name for example in module.examples[0].examples]).to.be.equal(['first_example', 'second_example', 'third_example', '#inner_context'])

    with context('when a skip decorator loaded'):
        def it_should_mark_example_as_pending():
            with _.subject.load_from_file(SKIP_DECORATOR_PATH) as module:
                expect(module.examples).to.have.length_of(1)
                expect(module.examples[0].examples[0].pending).to.be.true

        def it_should_mark_example_group_as_pending():
            with _.subject.load_from_file(SKIP_DECORATOR_PATH) as module:
                expect(module.examples).to.have.length_of(1)
                expect(module.examples[0].examples[1].pending).to.be.true
