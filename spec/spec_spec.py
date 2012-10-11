from mamba import describe, context
from hamcrest import *

from mamba.spec import Spec, Suite


with describe('Spec') as _:

    def it_should_run_the_test():
        test = Spec(_test)

        test.run()

        assert_that(_.was_run, is_(True))

    def _test():
        _.was_run = True

    def it_should_keep_the_error_if_test_failed():
        test = Spec(_failing_test)

        test.run()

        assert_that(test.exception_caught(), is_not(none()))

    def _failing_test():
        raise ValueError()

    def it_should_calculate_elapsed_time():
        test = Spec(_test)

        test.run()

        assert_that(test.elapsed_time().total_seconds(), is_(greater_than(0)))

    with context('#depth'):

        def it_should_calculate_its_depth():
            spec = Spec(_test)

            assert_that(spec.depth(), is_(0))

        def it_should_calculate_its_depth_if_included_in_suite():
            spec = Spec(_test)
            suite = Suite('subject')
            suite.append(spec)

            assert_that(spec.depth(), is_(1))
