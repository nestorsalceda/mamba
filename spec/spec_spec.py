from mamba import describe, context
from sure import expect

from mamba.spec import Spec, Suite


with describe('Spec') as _:

    def it_should_run_the_test():
        test = Spec(_test)

        test.run()

        expect(_.was_run).to.be.true

    def _test():
        _.was_run = True

    def it_should_keep_the_error_if_test_failed():
        test = Spec(_failing_test)

        test.run()

        expect(test.exception_caught()).to.not_be.none

    def _failing_test():
        raise ValueError()

    def it_should_calculate_elapsed_time():
        test = Spec(_test)

        test.run()

        expect(test.elapsed_time().total_seconds()).to.be.greater_than(0)

    with context('#depth'):

        def it_should_calculate_its_depth():
            spec = Spec(_test)

            expect(spec.depth()).to.be.equal(0)

        def it_should_calculate_its_depth_if_included_in_suite():
            spec = Spec(_test)
            suite = Suite('subject')
            suite.append(spec)

            expect(spec.depth()).to.be.equal(1)
