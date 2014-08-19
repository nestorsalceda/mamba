from expects import *
from doublex_expects import have_been_called_with
from doublex import Spy

from spec.object_mother import *

from mamba import reporter
from mamba.example import PendingExample


with description(PendingExample):

    with before.each:
        self.example = a_pending_example()
        self.reporter = Spy(reporter.Reporter)

    with context('when run'):
        with before.each:
            self.example.run(self.reporter)

        with it('not runs the example'):
            expect(self.example.was_run).to(be_false)

        with it('notifies is pending'):
            expect(self.reporter.example_pending).to(have_been_called_with(self.example))
