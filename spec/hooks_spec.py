from expects import *

with description('Hooks'):

    with before.all:
        self.calls = []
        self.calls.append('before_all')

    with after.all:
        self.calls.append('after_all')

    with before.each:
        self.calls.append('before')

    with after.each:
        self.calls.append('after')

    with it('was called after before hook'):
        expect(self.calls).to(equal(['before_all', 'before']))
        self.calls.append('first')

    with it('was called before first test'):
        expect(self.calls).to(equal(['before_all', 'before', 'first', 'after', 'before']))
        self.calls.append('second')

    with context('when nested context'):
        with before.each:
            self.calls.append('before_nested')

        with before.all:
            self.calls.append('before_all_nested')

        with after.all:
            self.calls.append('after_all_nested')

        with it('was called in nested context'):
            expect(self.calls).to(equal(['before_all', 'before', 'first', 'after', 'before', 'second', 'after', 'before', 'third', 'after', 'before_all_nested', 'before', 'before_nested']))

    with it('was called before second test'):
        expect(self.calls).to(equal(['before_all', 'before', 'first', 'after', 'before', 'second', 'after', 'before']))
        self.calls.append('third')
