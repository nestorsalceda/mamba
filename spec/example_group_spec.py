from mamba import describe, context, before
from sure import expect
from doublex import *

from mamba import reporter
from mamba.example_group import ExampleGroup
from mamba.example import Example

IRRELEVANT_SUBJECT = 'irrelevant_subject'


with describe(ExampleGroup) as _:

    @before.each
    def create_example_group():
        _.was_run = False
        _.example_group = ExampleGroup(IRRELEVANT_SUBJECT)
        _.reporter = Spy(reporter.Reporter)

    def it_should_have_same_name_than_subject():
        expect(_.example_group.name).to.be.equals(IRRELEVANT_SUBJECT)

    def it_should_have_depth_greater_than_parent():
        example = Example(_test)
        _.example_group.append(example)

        expect(example.depth).to.be.equal(1)

    def _test():
        _.was_run = True

    with context('when pending'):
        @before.each
        def append_example_to_group_and_set_pending():
            example = Example(_test)
            _.example_group.append(example)
            _.example_group.pending = True

        def it_should_not_run_its_children():
            _.example_group.run(_.reporter)

            expect(_.was_run).to.be.false

        def it_should_propagate_to_its_children():
            expect(all(spec.pending for spec in _.example_group.specs)).to.be.true

    with context('when run'):

        @before.each
        def append_examples_and_run_spec_group():
            _.example_group.append(Example(_test))
            _.example_group.append(Example(_test))

            _.example_group.run(_.reporter)

        def it_should_run_the_example():
            expect(_.was_run).to.be.true

        def it_should_calculate_elapsed_time():
            expect(_.example_group.elapsed_time.total_seconds()).to.be.greater_than(0)

        def it_notifies_that_a_example_group_is_started():
            assert_that(_.reporter.example_group_started, called().with_args(_.example_group))

        def it_notifies_that_a_example_group_is_finished():
            assert_that(_.reporter.example_group_finished, called().with_args(_.example_group))

    with context('when run failed'):

        @before.each
        def append_failing_examples_and_run():
            def _failing_test():
                raise ValueError()

            _.example_group.append(Example(_failing_test))

            _.example_group.run(_.reporter)

        def it_should_be_marked_as_failed():
            expect(_.example_group.failed).to.be.true

    with context('when before all hook raises an error'):
        @before.each
        def append_failing_before_all_hook_and_run():
            def _raise_error():
                raise ValueError()
            #TODO: Law of Demeter!
            #_.example_group.add_hook('before_all', _raise_error)
            _.example_group.hooks['before_all'] = []
            _.example_group.hooks['before_all'].append(_raise_error)


        with context('when has only examples as children'):
            @before.each
            def append_an_example_and_run():
                _.example_group.append(Example(_test))

                _.example_group.run(_.reporter)

            def it_should_mark_failed_all_children():
                expect(_.example_group.specs[0].failed).to.be.true

            def it_should_propagate_error_to_all_children():
                expect(_.example_group.specs[0].exception).to.be.a(ValueError)

            def it_should_not_execute_any_example():
                expect(_.was_run).to.be.false

        with context('when has contexts as children'):
            @before.each
            def append_a_context_with_an_example_and_run():
                _.example_group.append(ExampleGroup(IRRELEVANT_SUBJECT))
                _.example_group.specs[0].append(Example(_test))

                _.example_group.run(_.reporter)

            def it_should_mark_failed_all_children_contexts():
                expect(_.example_group.specs[0].failed).to.be.true

            def it_should_propagate_error_to_all_children_contexts():
                expect(_.example_group.specs[0].exception).to.be.a(ValueError)
