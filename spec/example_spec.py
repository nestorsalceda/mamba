from expects import expect
from doublex import Spy

from spec.object_mother import *

from mamba import reporter


with description(Example):

    with before.each:
        self.reporter = Spy(reporter.Reporter)
        self.example = an_example()

    with it('runs the example'):
        self.example.run(self.reporter)

        expect(self.example.was_run).to.be.true

    with it('calculates elapsed time'):
        self.example.run(self.reporter)

        expect(self.example.elapsed_time.total_seconds()).to.be.above(0)

    with it('notifies when is started'):
        self.example.run(self.reporter)

        expect(self.reporter.example_started).to.have.been.called.with_args(self.example)

    with it('notifies when passed'):
        self.example.run(self.reporter)

        expect(self.reporter.example_passed).to.have.been.called.with_args(self.example)

    with context('when run failed'):
        with before.each:
            self.example = a_failing_example()

            self.example.run(self.reporter)

        with it('runs the example'):
            expect(self.example.was_run).to.be.true

        with it('is marked as failed'):
            expect(self.example.failed).to.be.true

        with it('keeps the error'):
            expect(self.example.error).to.not_be.none

        with it('notifies its failure'):
            expect(self.reporter.example_failed).to.have.been.called.with_args(self.example)

