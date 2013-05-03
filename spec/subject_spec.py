# -*- coding: utf-8 -*-

from mamba import describe, context, before
from sure import expect


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


with describe(Subject) as first_context:
    def it_should_be_instantiated_automatically():
        expect(first_context).to.have.property('subject').to.be.a(Subject)

        first_context.old_subject = first_context.subject

    def it_should_be_a_new_instance_every_time():
        expect(first_context).to.have.property('subject').to.not_be.equal(first_context.old_subject)

    with describe(SubjectWithBeforeHook) as second_context:
        @before.each
        def also_execute_before_hook():
            second_context.executed_hook = True

        def it_should_execute_instance_creation_and_hook():
            expect(second_context).to.have.property('subject').to.be.a(SubjectWithBeforeHook)
            expect(second_context).to.have.property('executed_hook').to.be.true

        with context('when acessing subject in before hook'):
            @before.each
            def access_to_subject_in_hook():
                second_context.subject.was_accessed = True

            def it_should_execute_first_instance_creation():
                expect(second_context.subject).to.have.property('was_accessed').to.be.true

    with describe(SubjectWithArguments) as third_context:

        def it_should_be_not_be_instantiated():
            expect(third_context).to.not_have.property('subject')

    with describe(SubjectWithArgumentsAndBeforeEachHook) as __:

        @before.each
        def create_subject():
            __.created = SubjectWithArgumentsAndBeforeEachHook(None)

        def it_should_contain_created_attribute():
            expect(__).to.have.property('created').to.be.a(SubjectWithArgumentsAndBeforeEachHook)
