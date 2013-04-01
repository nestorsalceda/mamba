from mamba import describe, context
from sure import expect

from mamba.spec import Spec


with describe('Spec') as _:

    def _test():
        _.was_run = True

    def it_should_have_same_name_than_test():
        test = Spec(_test)

        expect(test.name).to.be.equals('_test')

    def it_should_have_depth_zero_without_parent():
        test = Spec(_test)

        expect(test.depth).to.be.equal(0)

    with context('#run'):

        def it_should_run_the_test():
            test = Spec(_test)

            test.run()

            expect(_.was_run).to.be.true

        def it_should_calculate_elapsed_time():
            test = Spec(_test)

            test.run()

            expect(test.elapsed_time.total_seconds()).to.be.greater_than(0)

    with context('#run failed'):
        def it_should_keep_the_error_if_test_failed():
            test = Spec(_failing_test)

            test.run()

            expect(test.exception_caught()).to.not_be.none

        def _failing_test():
            raise ValueError()

