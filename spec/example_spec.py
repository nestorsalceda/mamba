from expects import expect
from doublex import Spy, assert_that, called

from spec.object_mother import *

from mamba import reporter
from mamba.example import Example


with description(Example):

    with before('each'):
        self.reporter = Spy(reporter.Reporter)
        self.example = Example(None)

    with it('runs the example'):
        self.example.run(self.reporter)

        expect(self.example.was_run).to.be.true

    with it('calculates elapsed time'):
        self.example.run(self.reporter)

        expect(self.example.elapsed_time.total_seconds()).to.be.above(0)

    with it('notifies when is started'):
        self.example.run(self.reporter)

        assert_that(self.reporter.example_started, called().with_args(self.example))

    with it('notifies when passed'):
        self.example.run(self.reporter)

        assert_that(self.reporter.example_passed, called().with_args(self.example))

    #with context('when run failed'):
    #    @before.each
    #    def create_and_run_failing_example():
    #        _.example = a_failing_example()

    #        _.example.run(_.reporter)

    #    def it_should_be_marked_as_failed():
    #        expect(_.example.failed).to.be.true

    #    def it_should_keep_the_error_if_example_failed():
    #        expect(_.example.error).to.not_be.none

    #    def it_notifies_is_failed():
    #        assert_that(_.reporter.example_failed, called().with_args(_.example))

