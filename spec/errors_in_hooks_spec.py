from expects import *
from doublex import *

from mamba import reporter

from spec.object_mother import *

with description('Errors in hooks'):
    with before.each:
        self.reporter = Spy(reporter.Reporter)
        self.example_group = an_example_group()

    with context('when an error was raised in a before.all hook'):
        with before.each:
            self.example_group.add_hook('before_all', self._error)

        with it('marks example as failed'):
            self.example = an_example()
            self.example_group.append(self.example)

            self.example_group.run(self.reporter)

            expect(self.example.error).not_to(be_none)

        with context('when example also launches an error'):
            with context('when before.each also launches an error'):
                with it('keeps the error happened in first hook'):
                    self.example_group.add_hook('before_each', self._other_error)
                    self.example = a_failing_example()
                    self.example_group.append(self.example)

                    self.example_group.run(self.reporter)

                    expect(isinstance(self.example.error.exception, NotImplementedError)).to(be_true)

            with it('keeps the error happened in hook'):
                self.example = a_failing_example()
                self.example_group.append(self.example)

                self.example_group.run(self.reporter)

                expect(isinstance(self.example.error.exception, NotImplementedError)).to(be_true)

    with context('when an error was raised in a before.each hook'):
        with before.each:
            self.example_group.add_hook('before_each', self._error)

        with it('marks example as failed'):
            self.example = an_example()
            self.example_group.append(self.example)

            self.example_group.run(self.reporter)

            expect(self.example.error).not_to(be_none)

        with context('when example also launches an error'):
            with it('keeps the error happened in hook'):
                self.example = a_failing_example()
                self.example_group.append(self.example)

                self.example_group.run(self.reporter)

                expect(isinstance(self.example.error.exception, NotImplementedError)).to(be_true)

    with context('when an error was raised in an after.each hook'):
        with before.each:
            self.example_group.add_hook('after_each', self._error)

        with it('marks example as failed'):
            self.example = an_example()
            self.example_group.append(self.example)

            self.example_group.run(self.reporter)

            expect(self.example.error).not_to(be_none)

        with context('when example also launches an error'):
            with it('keeps the error happened in example'):
                self.example = a_failing_example()
                self.example_group.append(self.example)

                self.example_group.run(self.reporter)

                expect(isinstance(self.example.error.exception, ValueError)).to(be_true)

    with context('when an error was raised in an after.all hook'):
        with before.each:
            self.example_group.add_hook('after_all', self._error)

        with it('marks example as failed'):
            self.example = an_example()
            self.example_group.append(self.example)

            self.example_group.run(self.reporter)

            expect(self.example.error).not_to(be_none)

        with context('when example also launches an error'):
            with context('when after.each also launches an error'):
                with it('keeps the error happened in last hook'):
                    self.example_group.add_hook('after_each', self._other_error)
                    self.example = a_failing_example()
                    self.example_group.append(self.example)

                    self.example_group.run(self.reporter)

                    expect(isinstance(self.example.error.exception, NotImplementedError)).to(be_true)

            with it('keeps the error happened in last hook'):
                self.example = a_failing_example()
                self.example_group.append(self.example)

                self.example_group.run(self.reporter)

                expect(isinstance(self.example.error.exception, NotImplementedError)).to(be_true)

    def _error(self, *args):
        raise NotImplementedError()

    def _other_error(self, *args):
        raise IOError()
