from mamba import describe, context, before
from sure import expect

from mamba.spec import Spec, SpecGroup

IRRELEVANT_SUBJECT = 'irrelevant_subject'


with describe('SpecGroup') as _:

    @before.each
    def create_spec_group():
        _.was_run = False
        _.spec_group = SpecGroup(IRRELEVANT_SUBJECT)

    def it_should_have_same_name_than_subject():
        expect(_.spec_group.name).to.be.equals(IRRELEVANT_SUBJECT)

    def it_should_have_depth_greater_than_parent():
        test = Spec(_test)
        _.spec_group.append(test)

        expect(test.depth).to.be.equal(1)

    def _test():
        _.was_run = True

    with context('when skipped'):
        @before.each
        def append_spect_to_spec_group_and_set_skipped():
            test = Spec(_test)
            _.spec_group.append(test)
            _.spec_group.skipped = True

        def it_should_not_run_its_children():
            _.spec_group.run()

            expect(_.was_run).to.be.false

        def it_should_propagate_to_its_children():
            expect(all(spec.skipped for spec in _.spec_group.specs)).to.be.true

    with context('when run'):

        @before.each
        def append_tests_and_run_spec_group():
            _.spec_group.append(Spec(_test))
            _.spec_group.append(Spec(_test))

            _.spec_group.run()

        def it_should_run_the_test():
            expect(_.was_run).to.be.true

        def it_should_calculate_elapsed_time():
            expect(_.spec_group.elapsed_time.total_seconds()).to.be.greater_than(0)


    with context('when run failed'):

        @before.each
        def append_failing_tests_and_run():
            def _failing_test():
                raise ValueError()

            _.spec_group.append(Spec(_failing_test))

            _.spec_group.run()

        def it_should_be_marked_as_failed():
            expect(_.spec_group.failed).to.be.true

    with context('when before all hook raises an error'):
        @before.each
        def append_failing_before_all_hook_and_run():
            def _raise_error():
                raise ValueError()
            #TODO: Law of Demeter!
            #_.spec_group.add_hook('before_all', _raise_error)
            _.spec_group.hooks['before_all'] = []
            _.spec_group.hooks['before_all'].append(_raise_error)


        with context('when has only specs as children'):
            @before.each
            def append_a_spec_and_run():
                _.spec_group.append(Spec(_test))

                _.spec_group.run()

            def it_should_mark_failed_all_children_specs():
                expect(_.spec_group.specs[0].failed).to.be.true

            def it_should_propagate_error_to_all_children_specs():
                expect(_.spec_group.specs[0].exception).to.be.a(ValueError)

            def it_should_not_execute_any_spec():
                expect(_.was_run).to.be.false

        with context('when has contexts as children'):
            @before.each
            def append_a_context_with_a_spec_and_run():
                _.spec_group.append(SpecGroup(IRRELEVANT_SUBJECT))
                _.spec_group.specs[0].append(Spec(_test))

                _.spec_group.run()

            def it_should_mark_failed_all_children_contexts():
                expect(_.spec_group.specs[0].failed).to.be.true

            def it_should_propagate_error_to_all_children_contexts():
                expect(_.spec_group.specs[0].exception).to.be.a(ValueError)
