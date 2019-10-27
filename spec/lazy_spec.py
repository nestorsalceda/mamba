from mamba import description, it, context, before, lazy
from expects import expect, equal

with description('Lazy'):

    with before.each as self:
        self.lazy_calls_count = 0

    with lazy.my_awesome_dict as self:
        self._my_awesome_dict = dict(number=self.my_awesome_number())

    with lazy.my_awesome_number as self:
        self.lazy_calls_count = self.lazy_calls_count + 1
        self._my_awesome_number = 1

    with it('should call once') as self:
        expect(self.lazy_calls_count).to(equal(0))
        expect(self.my_awesome_number()).to(equal(1))
        expect(self.lazy_calls_count).to(equal(1))
        expect(self.my_awesome_dict()).to(equal(dict(number=1)))
        expect(self.lazy_calls_count).to(equal(1))

    with context('sub context'):
        with lazy.my_awesome_number as self:
            self.lazy_calls_count = self.lazy_calls_count + 1
            self._my_awesome_number = 2

        with it('should call once') as self:
            expect(self.lazy_calls_count).to(equal(0))
            expect(self.my_awesome_number()).to(equal(2))
            expect(self.lazy_calls_count).to(equal(1))
            expect(self.my_awesome_dict()).to(equal(dict(number=2)))
            expect(self.lazy_calls_count).to(equal(1))
