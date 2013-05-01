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
        @before.each
        def append_spect_to_suite_and_set_skipped():
            test = Spec(_test)
            _.suite.append(test)
            _.suite.skipped = True

        def it_should_not_run_its_children():
            _.suite.run()

            expect(_.was_run).to.be.false

        def it_should_propagate_to_its_children():
            expect(all(spec.skipped for spec in _.suite.specs)).to.be.true

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

    with context('when before all hook raises an error'):
        @before.each
        def append_failing_before_all_hook_and_run():
            def _raise_error():
                raise ValueError()
            _.suite.hooks['before_all'] = _raise_error


        with context('when has only specs as children'):
            @before.each
            def append_a_spec_and_run():
                _.suite.append(Spec(_test))

                _.suite.run()

            def it_should_mark_failed_all_children_specs():
                expect(_.suite.specs[0].failed).to.be.true

            def it_should_propagate_error_to_all_children_specs():
                expect(_.suite.specs[0].exception).to.be.a(ValueError)

            def it_should_not_execute_any_spec():
                expect(_.was_run).to.be.false

        with context('when has contexts as children'):
            @before.each
            def append_a_context_with_a_spec_and_run():
                _.suite.append(Suite(IRRELEVANT_SUBJECT))
                _.suite.specs[0].append(Spec(_test))

                _.suite.run()

            def it_should_mark_failed_all_children_contexts():
                expect(_.suite.specs[0].failed).to.be.true

            def it_should_propagate_error_to_all_children_contexts():
                expect(_.suite.specs[0].exception).to.be.a(ValueError)
