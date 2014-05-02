# -*- coding: utf-8 -*-

from expects import expect

class Subject(object):
    pass


class SubjectWithBeforeHook(object):
    pass


class SubjectWithArguments(object):
    def __init__(self, argument):
        pass


class SubjectWithArgumentsAndBeforeEachHook(object):

    def __init__(self, argument):
        pass


with description(Subject):
    with it('is instantiated automatically'):
        expect(self).to.have.property('subject').to.be.a(Subject)

        self.old_subject = self.subject

    with it('is instantiated in every example automatically'):
        expect(self).to.have.property('subject').to.not_be.equal(self.old_subject)

    with description(SubjectWithBeforeHook):
        with before.each:
            self.executed_hook = True

        with it('executes instance creation and before hook'):
            expect(self).to.have.property('subject').to.be.a(SubjectWithBeforeHook)
            expect(self).to.have.property('executed_hook').to.be.true

        with context('when acessing subject in before hook'):
            with before.each:
                self.subject.was_accessed = True

            with it('executes first the instance creation'):
                expect(self.subject).to.have.property('was_accessed').to.be.true

    with description(SubjectWithArguments):
        with it('is not instantiated automatically'):
            expect(self).to.not_have.property('subject')

    with description(SubjectWithArgumentsAndBeforeEachHook):

        with before.each:
            self.created = SubjectWithArgumentsAndBeforeEachHook(None)

        with it('contains a created attribute'):
            expect(self).to.have.property('created').to.be.a(SubjectWithArgumentsAndBeforeEachHook)
