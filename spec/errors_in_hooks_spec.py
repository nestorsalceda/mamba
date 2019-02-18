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

        with context('executes teardown only for contexts, which ran their setups'):
            def call_and_raise(self, ctx):
                ctx.calls.append('before_each_parent')
                raise Exception

            with it('executes teardown only for contexts, which ran their setups'):
                
                self.example_group.hooks['before_each'] = [lambda ctx: self.call_and_raise(ctx)]
                self.example_group.hooks['after_each'] = [lambda ctx: ctx.calls.append('after_each_parent')]

                self.parent_example = a_failing_example()
                self.example_group.append(self.parent_example)

                child = an_example_group()
                child.hooks['before_each'] = [lambda ctx: ctx.calls.append('before_each_child')]
                child.hooks['after_each'] = [lambda ctx: ctx.calls.append('after_each_child')]

                self.example = a_failing_example()
                child.append(self.example)
                self.example_group.append(child)

                self.execution_context = runnable.ExecutionContext()
                self.execution_context.calls = []

                self.example_group.execute(self.reporter, self.execution_context)

                expect(self.execution_context.calls).to(equal([
                    'before_each_parent',
                    'after_each_parent',
                    'before_each_parent',
                    'after_each_parent'
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

# from mamba import description, context, it, before, after, shared_context, \
#     included_context
# from expects import be_empty, be_none, expect, equal, have_length, be_false

# with description("D") as self:
#     with before.each:
#         print("D.BeforeEach")
#         raise Exception("asdf")
#     with after.each:
#         print("D.AfterEach")

#     with it("it.D"):
#         print("it.D")

#     with context("C1"):
#         with before.each:
#             print("C1.BeforeEach")
#         with after.each:
#             print("C1.AfterEach")


#         with context("C2"):
#             with before.each:
#                 print("C2.BeforeEach")
#             with after.each:
#                 print("C2.AfterEach")

#             with it("it.C2"):
#                 print("it.C2")
