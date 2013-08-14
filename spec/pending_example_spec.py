from mamba import describe, context, before
from sure import expect
from doublex import *

from spec.object_mother import *

from mamba import reporter
from mamba.example import PendingExample


with describe(PendingExample) as _:

    @before.each
    def create_pending_example_and_reporter():
        _.was_run = False
        _.example = a_pending_example(_)
        _.reporter = Spy(reporter.Reporter)

    with context('when run'):
        @before.each
        def run_pending_example():
            _.example.run(_.reporter)

        def it_should_not_run_the_example():
            expect(_.was_run).to.be.false

        def it_notifies_is_pending():
            assert_that(_.reporter.example_pending, called().with_args(_.example))
