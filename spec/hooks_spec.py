from expects import *
from doublex import Spy

from mamba import runnable
from mamba.reporter import Reporter
from mamba.example import Example

from spec.object_mother import *

with description('Hooks'):

    with before.each:
        self.reporter = Spy(Reporter)
        self.parent = an_example_group()

        self.execution_context = runnable.ExecutionContext()
        self.execution_context.calls = []

    with it('executes before_each hook before executing an example'):
        self.parent.hooks['before_each'] = [lambda ctx: ctx.calls.append('before_each')]
        self.parent.append(Example(lambda ctx: ctx.calls.append('example')))

        self.parent.execute(self.reporter, self.execution_context)

        expect(self.execution_context.calls).to(equal(['before_each', 'example']))

    with it('executes after_each hook before executing an example'):
        self.parent.hooks['after_each'] = [lambda ctx: ctx.calls.append('after_each')]
        self.parent.append(Example(lambda ctx: ctx.calls.append('example')))

        self.parent.execute(self.reporter, self.execution_context)

        expect(self.execution_context.calls).to(equal(['example', 'after_each']))

    with it('executes before_all only once before executing examples'):
        self.parent.hooks['before_all'] = [lambda ctx: ctx.calls.append('before_all')]
        self.parent.append(Example(lambda ctx: ctx.calls.append('example_1')))
        self.parent.append(Example(lambda ctx: ctx.calls.append('example_2')))

        self.parent.execute(self.reporter, self.execution_context)

        expect(self.execution_context.calls).to(equal(['before_all', 'example_1', 'example_2']))

    with it('executes after_all only once after executing examples'):
        self.parent.hooks['after_all'] = [lambda ctx: ctx.calls.append('after_all')]
        self.parent.append(Example(lambda ctx: ctx.calls.append('example_1')))
        self.parent.append(Example(lambda ctx: ctx.calls.append('example_2')))

        self.parent.execute(self.reporter, self.execution_context)

        expect(self.execution_context.calls).to(equal(['example_1', 'example_2', 'after_all']))

    with context('when having nested contexts'):
        with it('executes first the before_all and later the before_each for every parent, in declaration order'):
            self.parent.hooks['before_all'] = [lambda ctx: ctx.calls.append('before_all_parent')]
            self.parent.hooks['before_each'] = [lambda ctx: ctx.calls.append('before_each_parent')]

            child = an_example_group()
            child.hooks['before_each'] = [lambda ctx: ctx.calls.append('before_each_child')]

            child.append(Example(lambda ctx: ctx.calls.append('example')))
            self.parent.append(child)

            child.execute(self.reporter, self.execution_context)

            expect(self.execution_context.calls).to(equal(['before_all_parent', 'before_each_parent', 'before_each_child', 'example']))
