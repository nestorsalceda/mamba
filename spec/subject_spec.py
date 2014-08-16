# -*- coding: utf-8 -*-

from expects import *


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
        expect(self).to(have_property('subject', be_a(Subject)))

        self.old_subject = self.subject

    with it('is instantiated in every example automatically'):
        expect(self).to(have_property('subject', not_(be(self.old_subject))))

    with description(SubjectWithBeforeHook):
        with before.each:
            self.executed_hook = True

        with it('executes instance creation and before hook'):
            expect(self).to(have_property('subject', be_a(SubjectWithBeforeHook)))
            expect(self).to(have_property('executed_hook', be_true))

        with context('when acessing subject in before hook'):
            with before.each:
                self.subject.was_accessed = True

            with it('executes first the instance creation'):
                expect(self.subject).to(have_property('was_accessed', be_true))

    with description(SubjectWithArguments):
        with it('is not instantiated automatically'):
            expect(self).not_to(have_property('subject'))

    with description(SubjectWithArgumentsAndBeforeEachHook):

        with before.each:
            self.created = SubjectWithArgumentsAndBeforeEachHook(None)

        with it('contains a created attribute'):
            expect(self).to(have_property('created', be_a(SubjectWithArgumentsAndBeforeEachHook)))
