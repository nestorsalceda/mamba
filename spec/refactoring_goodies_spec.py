from expects import expect


RETURN_VALUE = '42'

with description('Refactoring goodies'):

    def a_method(self, return_value=RETURN_VALUE):
        return return_value

    with it('uses methods defined inside its context'):
        expect(self.a_method()).to.be.equal(RETURN_VALUE)

    with context('when using nested contexts'):

        with it('uses methods defined inside its parent'):
            expect(self.a_method()).to.be.equal(RETURN_VALUE)

