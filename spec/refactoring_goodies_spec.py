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
