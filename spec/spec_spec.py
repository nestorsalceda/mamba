from mamba import describe, context, before
from sure import expect
from doublex import *

from mamba import reporters
from mamba.spec import Spec

ANY_REPORTER = Stub()

with describe('Spec') as _:

    @before.each
    def create_new_test():
        def _test():
            _.was_run = True

        _.was_run = False
        _.test = Spec(_test)

    def it_should_have_same_name_than_test():
        expect(_.test.name).to.be.equals('_test')

    def it_should_have_depth_zero_without_parent():
        expect(_.test.depth).to.be.equal(0)

    with context('when pending'):
        def it_should_not_run_the_test():
            _.test.pending = True

            _.test.run(ANY_REPORTER)

            expect(_.was_run).to.be.false

    with context('when run'):
        @before.each
        def run_test():
            _.reporter = Spy(reporters.Reporter)
            _.test.run(_.reporter)

        def it_should_run_the_test():
            expect(_.was_run).to.be.true

        def it_should_calculate_elapsed_time():
            expect(_.test.elapsed_time.total_seconds()).to.be.greater_than(0)

    with context('when run failed'):
        @before.each
        def create_and_run_failing_test():
            def _failing_test():
                raise ValueError()

            _.test = Spec(_failing_test)

            _.test.run(ANY_REPORTER)

        def it_should_be_marked_as_failed():
            expect(_.test.failed).to.be.true

        def it_should_keep_the_error_if_test_failed():
            expect(_.test.exception).to.not_be.none

        def it_should_keep_the_traceback():
            expect(_.test.traceback).to.not_be.none
