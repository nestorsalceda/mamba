from expects import *
from doublex_expects import have_been_called_with
from doublex import Spy

from spec.object_mother import *

from mamba import reporter, runnable
from mamba.example_group import ExampleGroup
from mamba.example import Example


with description(ExampleGroup):

    with before.each:
        self.example_group = an_example_group()
        self.reporter = Spy(reporter.Reporter)

    with it('has same name than subject'):
        expect(self.example_group.name).to(be(IRRELEVANT_DESCRIPTION))

    with context('when run'):
        with before.each:
            self.example = an_example()
            self.example_group.append(self.example)

            self.example_group.execute(self.reporter, runnable.ExecutionContext())

        with it('runs the example'):
            expect(self.example.was_run).to(be_true)

        with it('calculates elapsed time'):
            expect(self.example_group.elapsed_time.total_seconds()).to(be_above(0))

        with it('notifies that an example group was started'):
            expect(self.reporter.example_group_started).to(have_been_called_with(self.example_group))

        with it('notifies that an example group is finished'):
            expect(self.reporter.example_group_finished).to(have_been_called_with(self.example_group))

        with it('keeps execution context for examples isolated'):
            foo = []
            def dummy(execution_context):
                foo.append(execution_context)

            self.example_group.append(Example(dummy))
            self.example_group.append(Example(dummy))

            self.example_group.execute(self.reporter, runnable.ExecutionContext())

            expect(foo[0]).not_to(equal(foo[1]))

    with context('when run failed'):

        with it('is marked as failed'):
            self.example_group.append(a_failing_example())

            self.example_group.execute(self.reporter, runnable.ExecutionContext())

            expect(self.example_group.failed()).to(be_true)
