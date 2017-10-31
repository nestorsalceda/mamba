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

    # TODO: before_all hook

    with it('shares execution context content among hooks and examples'):
        def append_before_each(context):
            context.calls = []
            context.calls.append('before_each')

        self.parent.hooks['before_each'] = [append_before_each]
        example = Example(lambda context: context.calls.append('example'))
        self.parent.append(example)

        self.parent.execute(self.reporter)

        expect(self.parent.execution_context.calls).to(equal(['before_each', 'example']))

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

