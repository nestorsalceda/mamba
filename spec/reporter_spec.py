from mamba import describe, context, before
from sure import expect
from doublex import *

from mamba import reporter, formatters, example, example_group

ANY_SPEC = example.Example(None)
ANY_SPEC_GROUP = example_group.ExampleGroup(None)


with describe(reporter.Reporter) as _:

    @before.each
    def create_reporter_and_attach_formatter():
        _.formatter = Spy(formatters.Formatter)
        _.reporter = reporter.Reporter(_.formatter)
        _.reporter.start()

    def it_notifies_event_spec_started_to_listeners():
        _.reporter.spec_started(ANY_SPEC)

        assert_that(_.formatter.spec_started, called().with_args(ANY_SPEC))

    def it_increases_spec_counter_when_spec_started():
        _.reporter.spec_started(ANY_SPEC)

        expect(_.reporter.spec_count).to.be.equal(1)

    def it_notifies_event_spec_passed_to_listeners():
        _.reporter.spec_passed(ANY_SPEC)

        assert_that(_.formatter.spec_passed, called().with_args(ANY_SPEC))

    def it_notifies_event_spec_failed_to_listeners():
        _.reporter.spec_failed(ANY_SPEC)

        assert_that(_.formatter.spec_failed, called().with_args(ANY_SPEC))

    def it_increases_failed_counter_when_spec_failed():
        _.reporter.spec_failed(ANY_SPEC)

        expect(_.reporter.failed_count).to.be.equal(1)

    def it_adds_failed_spec_when_spec_failed():
        _.reporter.spec_failed(ANY_SPEC)

        expect(ANY_SPEC).to.be.within(_.reporter.failed_specs)

    def it_notifies_event_spec_pending_to_listeners():
        _.reporter.spec_pending(ANY_SPEC)

        assert_that(_.formatter.spec_pending, called().with_args(ANY_SPEC))

    def it_increases_pending_counter_when_spec_started():
        _.reporter.spec_pending(ANY_SPEC)

        expect(_.reporter.pending_count).to.be.equal(1)

    def it_notifies_event_spec_group_started_to_listeners():
        _.reporter.spec_group_started(ANY_SPEC_GROUP)

        assert_that(_.formatter.spec_group_started, called().with_args(ANY_SPEC_GROUP))

    def it_notifies_event_spec_group_finished_to_listeners():
        _.reporter.spec_group_finished(ANY_SPEC_GROUP)

        assert_that(_.formatter.spec_group_finished, called().with_args(ANY_SPEC_GROUP))

    with context('when finishing'):
        def it_notifies_summary_to_listeners():
            _.reporter.finish()

            assert_that(_.formatter.summary, called().with_args(
                _.reporter.duration,
                _.reporter.spec_count,
                _.reporter.failed_count,
                _.reporter.pending_count
            ))

        def it_notifies_failed_specs_to_listeners():
            _.reporter.finish()

            assert_that(_.formatter.failures, called().with_args(
                _.reporter.failed_specs
            ))
