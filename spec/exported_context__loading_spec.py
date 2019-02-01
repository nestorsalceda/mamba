from mamba import description, context, it, before, _context
from expects import expect, be_true, have_length, equal, be_a, have_property, be_none

import os
import inspect

from mamba import example, example_group, loader
from mamba.example_collector import ExampleCollector

def spec_abspath(name):
    return os.path.join(os.path.dirname(__file__), 'fixtures', name)

def example_names(examples):
    return [example.name for example in examples]


EXPORTED_CONTEXT_PATH = spec_abspath('with_exported_context/exported.py')
IMPORTED_CONTEXT_PATH = spec_abspath('with_exported_context/imported.py')
EXPORTED_INCLUDED_CONTEXT_PATH = spec_abspath('with_exported/exported_included.py')
IMPORTED_EXPORTED_INCLUDED_CONTEXT_PATH = spec_abspath('with_exported/imported_exported_included.py')

def _load_modules(paths):
    example_collector = ExampleCollector(paths)
    return list(example_collector.modules())

with context('when a exported context is loaded'):
    with it('mark context as exported'):
        module = _load_modules([EXPORTED_CONTEXT_PATH])[0]
        examples = loader.Loader().load_examples_from(module)
        expect(examples).to(have_length(1))
        expect(examples[0]).to(be_a(example_group.ExportedExampleGroup))

with description('including an exported_context') as self:
    with context('correctly ordered'):
        with before.each:
            self.modules = _load_modules([EXPORTED_CONTEXT_PATH, IMPORTED_CONTEXT_PATH])
            self.examples = loader.Loader().load_examples_from(self.modules[1])

        with it('inserts a normal example group'):
            expect(self.examples[0]).to(have_length(1))
            expect(self.examples[0].examples[0]).to(be_a(example_group.ExampleGroup))

        with it('inserts the examples of the shared context'):
            expect(self.examples[0]).to(have_length(1))
            included_context = self.examples[0].examples[0]
            expect(example_names(included_context.examples)).to(equal(['it exported example', 'it added example']))

    with _context('reverse ordered'):
        with before.each:
            self.modules = _load_modules([IMPORTED_CONTEXT_PATH, EXPORTED_CONTEXT_PATH])
            self.examples = loader.Loader().load_examples_from(self.modules[1])

        with it('inserts a normal example group'):
            expect(self.examples[0]).to(have_length(1))
            expect(self.examples[0].examples[0]).to(be_a(example_group.ExampleGroup))

        with it('inserts the examples of the shared context'):
            expect(self.examples[0]).to(have_length(1))
            included_context = self.examples[0].examples[0]
            expect(example_names(included_context.examples)).to(
                equal(['it exported example', 'it added example']))

    with _context('including each other'):
        with before.each:
            self.modules = _load_modules([EXPORTED_CONTEXT_PATH, EXPORTED_INCLUDED_CONTEXT_PATH, IMPORTED_EXPORTED_INCLUDED_CONTEXT_PATH])
            self.examples = loader.Loader().load_examples_from(self.modules[2])

        with it('inserts a normal example group'):
            expect(self.examples[0]).to(have_length(1))
            expect(self.examples[0].examples[0]).to(be_a(example_group.ExampleGroup))

        with it('inserts the examples of the shared context'):
            expect(self.examples[0]).to(have_length(1))
            included_context = self.examples[0].examples[0]
            expect(example_names(included_context.examples)).to(
                equal(['it exported example', 'it new exported example', 'it added example']))