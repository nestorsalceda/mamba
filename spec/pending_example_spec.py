from mamba import description, before, context, it
from expects import expect, be_false
from doublex_expects import have_been_called_with
from doublex import Spy

from spec.object_mother import *

from mamba import reporter, runnable
from mamba.example import PendingExample


with description(PendingExample) as self:

    with before.each:
        self.example = a_pending_example()
        self.reporter = Spy(reporter.Reporter)

    with context('when run'):
        with before.each:
            self.example.execute(self.reporter, runnable.ExecutionContext())

        with it('not runs the example'):
            expect(self.example.was_run).to(be_false)

        with it('notifies is pending'):
            expect(self.reporter.example_pending).to(have_been_called_with(self.example))
