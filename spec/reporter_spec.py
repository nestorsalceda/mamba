from expects import *
from doublex_expects import have_been_called_with
from doublex import Spy

from spec.object_mother import *

from mamba import reporter, formatters, example_group


with description(reporter.Reporter):

    with before.each:
        self.example = an_example()
        self.formatter = Spy(formatters.Formatter)
        self.reporter = reporter.Reporter(self.formatter)
        self.reporter.start()

    with context('when event started'):
        with before.each:
            self.reporter.example_started(self.example)

        with it('notifies event example started to listeners'):
            expect(self.formatter.example_started).to(have_been_called_with(self.example))

        with it('increases example counter'):
            expect(self.reporter.example_count).to(equal(1))

    with context('when event passed'):
        with it('notifies event example passed to listeners'):
            self.reporter.example_passed(self.example)

            expect(self.formatter.example_passed).to(have_been_called_with(self.example))

    with context('when event failed'):
        with before.each:
            self.reporter.example_failed(self.example)

        with it('notifies event example failed to listeners'):
            expect(self.formatter.example_failed).to(have_been_called_with(self.example))

        with it('increases failed counter'):
            expect(self.reporter.failed_count).to(equal(1))

        with it('keeps failed example'):
            self.reporter.example_failed(self.example)

            expect(self.reporter.failed_examples).to(contain(self.example))

    with context('when event pending'):
        with it('notifies event pending to listeners'):
            self.reporter.example_pending(self.example)

            expect(self.formatter.example_pending).to(have_been_called_with(self.example))

        with it('increases pending counter when example started'):
            self.reporter.example_pending(self.example)

            expect(self.reporter.pending_count).to(equal(1))

    with context('when reporting events for an example group'):
        with before.each:
            self.example_group = an_example_group()

        with it('notifies event example group started to listeners'):
            self.reporter.example_group_started(self.example_group)

            expect(self.formatter.example_group_started).to(have_been_called_with(self.example_group))

        with it('notifies event example group finished to listeners'):
            self.reporter.example_group_finished(self.example_group)

            expect(self.formatter.example_group_finished).to(have_been_called_with(self.example_group))

        with it('notifies exent example group pending to listeners'):
            self.example_group = a_pending_example_group()

            self.reporter.example_group_pending(self.example_group)

            expect(self.formatter.example_group_pending).to(have_been_called_with(self.example_group))

    with context('when finishing'):
        with it('notifies summary to listeners'):
            self.reporter.finish()

            expect(self.formatter.summary).to(have_been_called_with(
                self.reporter.duration,
                self.reporter.example_count,
                self.reporter.failed_count,
                self.reporter.pending_count))


        with it('notifies failed examples to listeners'):
            self.reporter.finish()

            expect(self.formatter.failures).to(have_been_called_with(self.reporter.failed_examples))

