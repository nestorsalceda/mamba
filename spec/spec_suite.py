from mamba import describe, context, before
from sure import expect

from mamba.spec import Spec, Suite

IRRELEVANT_SUBJECT = 'irrelevant_subject'


with describe('Suite') as _:

    @before.each
    def create_suite():
        _.was_run = False
        _.suite = Suite(IRRELEVANT_SUBJECT)

    def it_should_have_same_name_than_subject():
        expect(_.suite.name).to.be.equals(IRRELEVANT_SUBJECT)

    def it_should_have_depth_greater_than_parent():
        test = Spec(_test)
        _.suite.append(test)

        expect(test.depth).to.be.equal(1)

    def _test():
        _.was_run = True

    with context('when skipped'):
        def it_should_not_run_its_children():
            test = Spec(_test)
            _.suite.append(test)
            _.suite.skipped = True

            _.suite.run()

            expect(_.was_run).to.be.false


    with context('when run'):

        @before.each
        def append_tests_and_run_suite():
            _.suite.append(Spec(_test))
            _.suite.append(Spec(_test))

            _.suite.run()

        def it_should_run_the_test():
            expect(_.was_run).to.be.true

        def it_should_calculate_elapsed_time():
            expect(_.suite.elapsed_time.total_seconds()).to.be.greater_than(0)

    with context('when run failed'):

        @before.each
        def append_failing_tests_and_run():
            def _failing_test():
                raise ValueError()

            _.suite.append(Spec(_failing_test))

            _.suite.run()

        def it_should_be_marked_as_failed():
            expect(_.suite.failed).to.be.true
