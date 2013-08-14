from mamba import describe, context, before, pending
from sure import expect
from doublex import *

from spec.object_mother import *

from mamba import reporter
from mamba.example import PendingExample
from mamba.example_group import PendingExampleGroup


with describe(PendingExampleGroup) as _:

    @before.each
    def create_example_group():
        _.was_run = False
        _.example_group = a_pending_example_group()
        _.reporter = Spy(reporter.Reporter)

    with context('when run'):
        def it_should_not_run_its_children():
            _.example_group.append(a_pending_example(_))

            _.example_group.run(_.reporter)

            expect(_.was_run).to.be.false

    with context('when adding a new examples as children'):

        def it_raises_a_type_error_if_is_not_a_pending_example():
            expect(_.example_group.append).when.called_with(an_example(_)).to.throw(TypeError)

        def it_appends_pending_example():
            pending_example = a_pending_example(_)

            _.example_group.append(pending_example)

            expect(pending_example).to.be.within(_.example_group.examples)


        with context('when adding groups as children'):
            def it_raises_a_type_error_if_is_not_a_pending_example_group():
                expect(_.example_group.append).when.called_with(an_example_group()).to.throw(TypeError)

            def it_appends_pending_example_group():
                pending_example_group = a_pending_example_group()

                _.example_group.append(pending_example_group)

                expect(pending_example_group).to.be.within(_.example_group.examples)

