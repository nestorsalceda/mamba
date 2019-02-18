from mamba import description, before, it, context
from expects import expect, be_none, be_a, be_true, be_false, equal
from doublex import Spy

from mamba import reporter, runnable

from spec.object_mother import *

with description('Errors in hooks') as self:
    with before.each:
        self.reporter = Spy(reporter.Reporter)
        self.example_group = an_example_group()

    with context('when an error was raised in a before.all hook'):
        with before.each:
            self.example_group.hooks['before_all'].append(self._error)

        with it('marks example as failed'):
            self.example = an_example()
            self.example_group.append(self.example)

            self.example_group.execute(self.reporter, runnable.ExecutionContext())

            expect(self.example.error).not_to(be_none)

        with context('when example also launches an error'):
            with context('when before.each also launches an error'):
                with it('keeps the error happened in first hook'):
                    self.example_group.hooks['before_each'].append(self._other_error)
                    self.example = a_failing_example()
                    self.example_group.append(self.example)

                    self.example_group.execute(self.reporter, runnable.ExecutionContext())

                    expect(self.example.error.exception).to(be_a(NotImplementedError))

            with it('keeps the error happened in hook'):
                self.example = a_failing_example()
                self.example_group.append(self.example)

                self.example_group.execute(self.reporter, runnable.ExecutionContext())

                expect(self.example.error.exception).to(be_a(NotImplementedError))

    with context('when an error was raised in a before.each hook'):
        with before.each:
            self.example_group.hooks['before_each'].append(self._error)

        with it('marks example as failed with parent exception'):
            self.example = an_example()
            self.example_group.append(self.example)

            self.example_group.execute(self.reporter, runnable.ExecutionContext())

            expect(self.example.error.exception).to(be_a(NotImplementedError))

        with it('does not executes the example'):
            self.example = a_failing_example()
            self.example_group.append(self.example)

            self.example_group.execute(self.reporter, runnable.ExecutionContext())

            expect(self.example.was_run).to(be_false)

        with context('executes after_each only for contexts, which ran their before_each'):
            def call_and_raise(self, ctx, msg):
                # helper method, because we can't do multiline lambda
                ctx.calls.append(msg)
                raise Exception

            with before.each:
                # Setup the following scenario:
                #
                # with description("describe") as self:
                #     with before.each:
                #         print("describe_before_each")
                #     with after.each:
                #         print("describe_after_each")
                #     with it("describe_example"):
                #         print("describe_example")
                #     with context("context1"):
                #         with before.each:
                #             print("context1_before_each")
                #         with after.each:
                #             print("context1_after_each")
                #         with context("context2"):
                #             with before.each:
                #                 print("context2_before_each")
                #             with after.each:
                #                 print("context2_after_each")
                #             with it("context2_example"):
                #                 print("context2_example")

                self.describe = an_example_group()
                self.describe.hooks['before_each'] = [lambda ctx: ctx.calls.append('describe_before_each')]
                self.describe.hooks['after_each'] = [lambda ctx: ctx.calls.append('describe_after_each')]

                self.context1 = an_example_group()
                self.context1.hooks['before_each'] = [lambda ctx: ctx.calls.append('context1_before_each')]
                self.context1.hooks['after_each'] = [lambda ctx: ctx.calls.append('context1_after_each')]

                context2 = an_example_group()
                context2.hooks['before_each'] = [lambda ctx: ctx.calls.append('context2_before_each')]
                context2.hooks['after_each'] = [lambda ctx: ctx.calls.append('context2_after_each')]

                example_in_describe = an_example()
                self.describe.append(example_in_describe)
                example_in_context2 = an_example()
                context2.append(example_in_context2)

                self.describe.append(self.context1)
                self.context1.append(context2)


            with it('exception in describe block before_each'):
                self.describe.hooks['before_each'] = [lambda ctx: self.call_and_raise(ctx, 'describe_before_each')]

                exec_context = runnable.ExecutionContext()
                exec_context.calls = []

                self.describe.execute(self.reporter, exec_context)

                expect(exec_context.calls).to(equal([
                    'describe_before_each',
                    'describe_after_each',
                    'describe_before_each',
                    'describe_after_each'
                ]))

            with it('exception in context1 block before_each'):
                self.context1.hooks['before_each'] = [lambda ctx: self.call_and_raise(ctx, 'context1_before_each')]

                exec_context = runnable.ExecutionContext()
                exec_context.calls = []

                self.describe.execute(self.reporter, exec_context)

                expect(exec_context.calls).to(equal([
                    'describe_before_each',
                    'describe_after_each',
                    'describe_before_each',
                    'context1_before_each',
                    'context1_after_each',
                    'describe_after_each',
                ]))


    with context('when an error was raised in an after.each hook'):
        with before.each:
            self.example_group.hooks['after_each'].append(self._error)

        with it('marks example as failed'):
            self.example = an_example()
            self.example_group.append(self.example)

            self.example_group.execute(self.reporter, runnable.ExecutionContext())

            expect(self.example.error).not_to(be_none)

        with context('when an error happened in the example'):
            with it('still executes after_each hook'):
                self.example = a_failing_example()
                self.example_group.append(self.example)

                self.example_group.execute(self.reporter, runnable.ExecutionContext())

                expect(isinstance(self.example.error.exception, ValueError)).to(be_false)

    with context('when an error was raised in an after.all hook'):
        with before.each:
            self.example_group.hooks['after_all'].append(self._error)

        with it('marks example as failed'):
            self.example = an_example()
            self.example_group.append(self.example)

            self.example_group.execute(self.reporter, runnable.ExecutionContext())

            expect(self.example.error).not_to(be_none)

        with context('when example also launches an error'):
            with context('when after.each also launches an error'):
                with it('keeps the error happened in last hook'):
                    self.example_group.hooks['after_each'].append(self._other_error)
                    self.example = a_failing_example()
                    self.example_group.append(self.example)

                    self.example_group.execute(self.reporter, runnable.ExecutionContext())

                    expect(self.example.error.exception).to(be_a(NotImplementedError))

            with it('keeps the error happened in last hook'):
                self.example = a_failing_example()
                self.example_group.append(self.example)

                self.example_group.execute(self.reporter, runnable.ExecutionContext())

                expect(self.example.error.exception).to(be_a(NotImplementedError))

    def _error(self, *args):
        raise NotImplementedError()

    def _other_error(self, *args):
        raise IOError()
