from expects import *
from doublex import *

from mamba import reporter

from spec.object_mother import *

with description('Errors in hooks'):

    with context('when an error was raised in a before.each hook'):
        with before.each:
            self.reporter = Spy(reporter.Reporter)
            self.example_group = an_example_group()
            self.example_group.hooks['before_each'].append(self._error)

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

        def _error(self):
            raise NotImplementedError()


