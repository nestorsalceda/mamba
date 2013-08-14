from mamba import describe, context, before
from sure import expect
from doublex import *

from spec.object_mother import *

from mamba import reporter
from mamba.example import Example


with describe(Example) as _:

    @before.each
    def create_new_example_and_reporter():
        _.was_run = False
        _.example = an_example(_)
        _.reporter = Spy(reporter.Reporter)

    with context('when run'):
        @before.each
        def run_example():
            _.example.run(_.reporter)

        def it_should_run_the_example():
            expect(_.was_run).to.be.true

        def it_should_calculate_elapsed_time():
            expect(_.example.elapsed_time.total_seconds()).to.be.greater_than(0)

        def it_notifies_is_started():
            assert_that(_.reporter.example_started, called().with_args(_.example))

        def it_notifies_is_passed():
            assert_that(_.reporter.example_passed, called().with_args(_.example))

    with context('when run failed'):
        @before.each
        def create_and_run_failing_example():
            _.example = a_failing_example()

            _.example.run(_.reporter)

        def it_should_be_marked_as_failed():
            expect(_.example.failed).to.be.true

        def it_should_keep_the_error_if_example_failed():
            expect(_.example.error).to.not_be.none

        def it_notifies_is_failed():
            assert_that(_.reporter.example_failed, called().with_args(_.example))

