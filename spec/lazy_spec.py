from mamba import description, it, context, lazy
from expects import expect, equal

with description('Lazy'):

    with lazy.my_awesome_dict as self:
        # print('the my_awesome_dict method should be called just once')
        self._my_awesome_dict = dict(number=self.my_awesome_number())

    with lazy.my_awesome_number as self:
        # print('the my_awesome_number1 method should be called just once')
        self._my_awesome_number = 1

    with it('should be equal') as self:
        expect(self.my_awesome_number()).to(equal(1))
        expect(self.my_awesome_dict()).to(equal(dict(number=1)))

    with context('sub context'):
        with lazy.my_awesome_number as self:
            # print('the my_awesome_number2 method should be called just once')
            self._my_awesome_number = 2

        with it('should be equal') as self:
            expect(self.my_awesome_number()).to(equal(2))
            expect(self.my_awesome_dict()).to(equal(dict(number=2)))
