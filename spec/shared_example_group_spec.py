from mamba import description, before, context, it
from expects import expect, be_false
from doublex_expects import have_been_called_with
from doublex import Spy

from spec.object_mother import *

from mamba import reporter, runnable
from mamba.example_group import SharedExampleGroup


with description(SharedExampleGroup) as self:

    with before.each:
        self.example_group = a_shared_example_group()
        self.reporter = Spy(reporter.Reporter)
        self.example = an_example()

    with context('when run'):
        with before.each:
            self.example_group.append(self.example)

            self.example_group.execute(self.reporter, runnable.ExecutionContext())

        with it('not runs its children'):
            expect(self.example_group.examples[0].was_run).to(be_false)

        with it('does not notify that an example group was started'):
            expect(self.reporter.example_group_started).not_to(have_been_called_with(self.example_group))
