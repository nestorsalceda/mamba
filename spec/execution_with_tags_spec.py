from mamba import description, before, context, it

from doublex import Spy
from expects import expect, be_true, be_false
from doublex_expects import have_been_called, have_been_called_with

from mamba import reporter, runnable
from mamba.example import Example
from mamba.example_group import ExampleGroup

from spec.object_mother import an_example_group

TAG = 'any_tag'
TAGS = [TAG]

with description('Example execution using tags') as self:
    with before.each:
        self.reporter = Spy(reporter.Reporter)
        self.example_group = an_example_group()
        self.example_with_tags = Example(lambda x: x,
                                         parent=self.example_group,
                                         tags=TAGS)
        self.other_example = Example(lambda x: x, parent=self.example_group)

    with context('when tag is included in example tags'):
        with it('executes example'):
            self.example_with_tags.execute(self.reporter,
                                           runnable.ExecutionContext(),
                                           tags=TAGS)

            expect(self.example_with_tags.was_run).to(be_true)

    with context('when tag is not included in example tags'):
        with it('does not execute example'):
            self.other_example.execute(self.reporter,
                                       runnable.ExecutionContext(),
                                       tags=TAGS)

            expect(self.other_example.was_run).to(be_false)

    with context('when example group does not have tags and silbing one does'):
        with it('skips example group without tags'):
            self.parent = ExampleGroup('any example_group')

            self.child = ExampleGroup('child example_group', tags=TAGS)
            self.example = Example(lambda x: x)
            self.child.append(self.example)

            self.silbing = ExampleGroup('silbing example_group')
            self.silbing.append(Example(lambda x: x))

            self.parent.append(self.child)
            self.parent.append(self.silbing)

            self.parent.execute(self.reporter,
                                runnable.ExecutionContext(),
                                tags=TAGS)

            expect(self.reporter.example_group_started).\
                to(have_been_called.twice)
            expect(self.reporter.example_group_started).\
                to(have_been_called_with(self.parent))
            expect(self.reporter.example_group_started).\
                to(have_been_called_with(self.child))

    with context('when checking if an example has a tag'):
        with context('and example has the tag'):
            with it('returns true'):
                example = Example(lambda x: x, tags=TAGS)

                expect(example.has_tag(TAG)).to(be_true)

        with context('and does not contains the tag'):
            with it('returns false'):
                example = Example(lambda x: x)

                expect(example.has_tag(TAG)).to(be_false)

        with context('and parent example has the tag'):
            with it('returns true'):
                parent = ExampleGroup('any example_group', tags=TAGS)
                example = Example(lambda x: x)

                parent.append(example)

                expect(example.has_tag(TAG)).to(be_true)

        with context('and parent example has not the tag'):
            with it('returns false'):
                parent = ExampleGroup('any example_group')
                example = Example(lambda x: x)

                parent.append(example)

                expect(example.has_tag(TAG)).to(be_false)

    with context('when checking if is included in execution with tags'):
        with context('and has the tag'):
            with it('returns true'):
                parent = ExampleGroup('any example_group', tags=TAGS)

                expect(parent.included_in_execution(TAGS)).to(be_true)

        with context('and does not has the tag'):
            with it('returns false'):
                parent = ExampleGroup('any example_group')

                expect(parent.included_in_execution(TAGS)).to(be_false)

        with context('and children has the tag'):
            with it('return true'):
                parent = ExampleGroup('any example_group')
                example = Example(lambda x: x, tags=TAGS)

                parent.append(example)

                expect(parent.included_in_execution(TAGS)).to(be_true)
