from expects import *
from doublex import Spy

from mamba.reporter import Reporter
from mamba.example import Example

from spec.object_mother import *

with description('Hooks'):

    with before.each:
        self.reporter = Spy(Reporter)
        self.parent = an_example_group()

    with it('executes before_each hook before executing an example'):
        calls = []
        self.parent.hooks['before_each'] = [lambda x: calls.append('before_each')]
        self.parent.append(Example(lambda x: calls.append('example')))

        self.parent.execute(self.reporter)

        expect(calls).to(equal(['before_each', 'example']))

    with it('executes after_each hook before executing an example'):
        calls = []
        self.parent.hooks['after_each'] = [lambda x: calls.append('after_each')]
        self.parent.append(Example(lambda x: calls.append('example')))

        self.parent.execute(self.reporter)

        expect(calls).to(equal(['example', 'after_each']))

    with it('executes  before_all only once before executing examples'):
        calls = []
        self.parent.hooks['before_all'] = [lambda x: calls.append('before_all')]
        self.parent.append(Example(lambda x: calls.append('example_1')))
        self.parent.append(Example(lambda x: calls.append('example_2')))

        self.parent.execute(self.reporter)

        expect(calls).to(equal(['before_all', 'example_1', 'example_2']))

    with it('executes after_all only once after executing examples'):
        calls = []
        self.parent.hooks['after_all'] = [lambda x: calls.append('after_all')]
        self.parent.append(Example(lambda x: calls.append('example_1')))
        self.parent.append(Example(lambda x: calls.append('example_2')))

        self.parent.execute(self.reporter)

        expect(calls).to(equal(['example_1', 'example_2', 'after_all']))

    with it('shares execution context content among *_each hooks and examples'):
        def append_before_each(context):
            context.calls = []
            context.calls.append('before_each')

        self.parent.hooks['before_each'] = [append_before_each]
        example = Example(lambda context: context.calls.append('example'))
        self.parent.append(example)

        self.parent.execute(self.reporter)

        expect(self.parent.execution_context.calls).to(equal(['before_each', 'example']))

    with it('shares execution context content among *_all hooks and examples'):
        def append_before_all(context):
            context.calls = []
            context.calls.append('before_all')

        self.parent.hooks['before_all'] = [append_before_all]
        example = Example(lambda context: context.calls.append('example'))
        self.parent.append(example)

        self.parent.execute(self.reporter)

        expect(self.parent.execution_context.calls).to(equal(['before_all', 'example']))

    with context('when having nested contexts'):
        with it('executes first before_each parent and then before_each from child'):
            calls = []
            self.parent.hooks['before_each'] = [lambda x: calls.append('before_each_parent')]

            child = an_example_group()
            child.hooks['before_each'] = [lambda x: calls.append('before_each_child')]

            child.append(Example(lambda x: calls.append('example')))
            self.parent.append(child)

            child.execute(self.reporter)

            expect(calls).to(equal(['before_each_parent', 'before_each_child', 'example']))

        with it('executes first the before_all and later the before_each for every parent, in declaration order'):
            calls = []
            self.parent.hooks['before_all'] = [lambda x: calls.append('before_all_parent')]
            self.parent.hooks['before_each'] = [lambda x: calls.append('before_each_parent')]

            child = an_example_group()
            child.hooks['before_each'] = [lambda x: calls.append('before_each_child')]

            child.append(Example(lambda x: calls.append('example')))
            self.parent.append(child)

            child.execute(self.reporter)

            expect(calls).to(equal(['before_all_parent', 'before_each_parent', 'before_each_child', 'example']))
