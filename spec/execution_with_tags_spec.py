from mamba import description, before, context, it

from doublex import Spy
from expects import expect, be_true, be_false

from mamba import reporter, runnable
from mamba.example import Example

from spec.object_mother import an_example_group

with description('Example execution using tags') as self:
    with before.each:
        self.reporter = Spy(reporter.Reporter)
        self.example = Example(lambda x: x, parent=an_example_group(),
                               tags=['focus'])
        self.other_example = Example(lambda x: x, parent=an_example_group())

    with context('when tag is included in example tags'):
        with it('executes example'):
            self.example.execute(self.reporter,
                                 runnable.ExecutionContext(),
                                 tags=['focus'])

            expect(self.example.was_run).to(be_true)

    with context('when tag is not included in example tags'):
        with it('does not execute example'):
            self.other_example.execute(self.reporter,
                                       runnable.ExecutionContext(),
                                       tags=['focus'])

            expect(self.other_example.was_run).to(be_false)
