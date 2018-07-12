from mamba import description, it, context
from expects import expect, equal


RETURN_VALUE = '42'

with description('Refactoring goodies') as self:

    def a_method(self, return_value=RETURN_VALUE):
        return return_value

    with it('uses methods defined inside its context'):
        expect(self.a_method()).to(equal(RETURN_VALUE))

    with context('when using nested contexts'):

        with it('uses methods defined inside its parent'):
            expect(self.a_method()).to(equal(RETURN_VALUE))

    with describe('Execution context of methods'):
        with context('When the value is defined in a before all hook of the same context'):

            def method_with_context(self):
                return self.context_value

            with before.all:
                self.context_value = RETURN_VALUE

            with it('returns the value defined in the before all hook'):
                expect(self.method_with_context()).to(equal(RETURN_VALUE))

        with context('When the value is defined in a before all hook of a nested context'):

            def method_with_context(self):
                return self.context_value

            with context('nested'):
                with before.all:
                    self.context_value = RETURN_VALUE

                with it('returns the value defined in the before all hook'):
                    expect(self.method_with_context()).to(equal(RETURN_VALUE))

        with context('When the value is defined in a before each hook of the same context'):

            def method_with_context(self):
                return self.context_value

            with before.each:
                self.context_value = RETURN_VALUE

            with it('returns the value defined in the before each hook'):
                expect(self.method_with_context()).to(equal(RETURN_VALUE))

        with context('When the value is defined in the example itself'):

            def method_with_context(self):
                return self.context_value

            with it('returns the value defined in the before each hook'):
                self.context_value = RETURN_VALUE
                expect(self.method_with_context()).to(equal(RETURN_VALUE))
