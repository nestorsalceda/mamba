from expects import expect
from doublex import Spy

from spec.object_mother import *

from mamba import reporter
from mamba.example_group import PendingExampleGroup


with description(PendingExampleGroup):

    with before.each:
        self.example_group = a_pending_example_group()
        self.reporter = Spy(reporter.Reporter)

    with context('when run'):
        with before.each:
            self.example_group.append(a_pending_example())

            self.example_group.run(self.reporter)

        with it('not runs its children'):
            expect(self.example_group.examples[0].was_run).to.be.false

        with it('notifies that an example group is pending'):
            expect(self.reporter.example_group_pending).to.have.been.called.with_args(self.example_group)

    with context('when adding a new examples as children'):

        with it('raises a type error if is not a pending example'):
            expect(lambda: self.example_group.append(an_example)).to.raise_error(TypeError)

        with it('appends pending example'):
            pending_example = a_pending_example()

            self.example_group.append(pending_example)

            expect(self.example_group.examples).to.have(pending_example)

        with context('when adding groups as children'):

            with it('raises a type error if is not a pending example group'):
                expect(lambda: self.example_group.append(an_example_group())).to.raise_error(TypeError)

            with it('appends a pending example group'):
                pending_example_group = a_pending_example_group()

                self.example_group.append(pending_example_group)

                expect(self.example_group.examples).to.have(pending_example_group)
