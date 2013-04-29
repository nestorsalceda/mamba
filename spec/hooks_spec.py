from mamba import describe, context, before, after
from sure import expect

with describe('Hooks') as _:
    _.calls = []

    @before.all
    def before_all():
        _.calls.append('before_all')

    @after.all
    def after_all():
        _.calls.append('after_all')

    @before.each
    def before_each():
        _.calls.append('before')

    @after.each
    def after_each():
        _.calls.append('after')

    def it_should_be_called_after_before():
        expect(_.calls).to.be.equal(['before_all', 'before'])
        _.calls.append('first')

    def it_should_be_called_before_first_test():
        expect(_.calls).to.be.equal(['before_all', 'before', 'first', 'after', 'before'])
        _.calls.append('second')

    with context('when nested context'):
        @before.each
        def before_nested():
            _.calls.append('before_nested')

        @before.all
        def before_all_nested():
            _.calls.append('before_all_nested')

        @after.all
        def after_all_nested():
            _.calls.append('after_all_nested')

        def it_should_be_called_in_nested_contexts():
            expect(_.calls).to.be.equal(['before_all', 'before', 'first', 'after', 'before', 'second', 'after', 'before', 'third', 'after', 'before_all_nested', 'before', 'before_nested'])

    def it_should_be_called_before_second_test():
        expect(_.calls).to.be.equal(['before_all', 'before', 'first', 'after', 'before', 'second', 'after', 'before'])
        _.calls.append('third')
