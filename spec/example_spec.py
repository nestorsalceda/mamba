from expects import *
from doublex_expects import have_been_called_with
from doublex import Spy

from spec.object_mother import *

from mamba import reporter, infrastructure
from mamba.infrastructure import total_seconds


with description(Example):

    with before.each:
        self.reporter = Spy(reporter.Reporter)
        self.example = an_example()

    with it('runs the example'):
        self.example.run(self.reporter)

        expect(self.example.was_run).to(be_true)

    with it('calculates elapsed time'):
        self.example.run(self.reporter)

        expect(total_seconds(self.example.elapsed_time)).to(be_above(0))

    with it('notifies when is started'):
        self.example.run(self.reporter)

        expect(self.reporter.example_started).to(have_been_called_with(self.example))

    with it('notifies when passed'):
        self.example.run(self.reporter)

        expect(self.reporter.example_passed).to(have_been_called_with(self.example))

    with context('when run failed'):
        with before.each:
            self.example = a_failing_example()

            self.example.run(self.reporter)

        with it('runs the example'):
            expect(self.example.was_run).to(be_true)

        with it('is marked as failed'):
            expect(self.example.failed).to(be_true)

        with it('keeps the error'):
            expect(self.example.error).not_to(be_none)

        with it('notifies its failure'):
            expect(self.reporter.example_failed).to(have_been_called_with(self.example))

