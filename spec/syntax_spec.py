# -*- coding: utf-8 -*-

import ast
import functools

from expects import expect, be_false, be_an, have_length, equal, be, match, be_none, be_true

from mamba.syntax.transformer import (
    WithStatement,
    HookToMethod,
    ExampleToMethod,
    ExampleGroupToClass
)
from mamba.infrastructure import is_python3

from .helpers import top_level_ast_nodes_of_fixture_at
top_level_ast_nodes_of_fixture_at = functools.partial(top_level_ast_nodes_of_fixture_at, __file__)


with description('the HookToMethod class'):
    with context('when given a `with` statement which does not match the hook declaration syntax'):
        with it('''can't transform it'''):
            for node in negative_examples_of_hook_declarations():
                expect(
                    HookToMethod(WithStatement(node)).can_transform
                ).to(be_false)

    with context('transforms the `with` statement into a method definition'):
        with it('represents the method as a function definition node'):
            for node in supported_hook_declarations():
                method_declaration = HookToMethod(WithStatement(node)).transform()

                expect(method_declaration).to(be_an(ast.FunctionDef))

        with it('names the method after the hook'):
            hook_names = ['before_all', 'before_each', 'after_each', 'after_all']

            for name, node in zip(hook_names, supported_hook_declarations()):
                method_declaration = HookToMethod(WithStatement(node)).transform()

                expect(method_declaration.name).to(equal(name))

        with it('includes only one parameter'):
            for node in supported_hook_declarations():
                method_declaration = HookToMethod(WithStatement(node)).transform()
                function_parameters = method_declaration.args.args

                expect(function_parameters).to(have_length(1))

        with it('the first parameter is named `self`'):
            for node in supported_hook_declarations():
                method_declaration = HookToMethod(WithStatement(node)).transform()
                function_parameters = method_declaration.args.args
                first_parameter = function_parameters[0]
                name_of_first_parameter = _retrieve_name_of_parameter(first_parameter)

                expect(name_of_first_parameter).to(equal('self'))

        with it('uses the original body of the `with` statement'):
            for node in supported_hook_declarations():
                method_declaration = HookToMethod(WithStatement(node)).transform()

                expect(method_declaration.body).to(be(node.body))

def _retrieve_name_of_parameter(function_parameter_node):
    if is_python3():
        return function_parameter_node.arg
    return function_parameter_node.id



with description('the ExampleToMethod class'):
    with context('when given a `with` statement which does not match the example declaration syntax'):
        with it('''can't transform it'''):
            for node in negative_examples_of_example_declarations():
                expect(
                    ExampleToMethod(WithStatement(node)).can_transform
                ).to(be_false)

    with context('transforms the `with` statement into a method definition'):
        with it('represents the method as a function definition node'):
            for node in supported_example_declarations():
                method_declaration = ExampleToMethod(WithStatement(node)).transform()

                expect(method_declaration).to(be_an(ast.FunctionDef))

        with it('includes only one parameter'):
            for node in supported_example_declarations():
                method_declaration = ExampleToMethod(WithStatement(node)).transform()
                function_parameters = method_declaration.args.args

                expect(function_parameters).to(have_length(1))

        with it('the first parameter is named `self`'):
            for node in supported_example_declarations():
                method_declaration = ExampleToMethod(WithStatement(node)).transform()
                function_parameters = method_declaration.args.args
                first_parameter = function_parameters[0]
                name_of_first_parameter = _retrieve_name_of_parameter(first_parameter)

                expect(name_of_first_parameter).to(equal('self'))

        with it('uses the original body of the `with` statement'):
            for node in supported_example_declarations():
                method_declaration = ExampleToMethod(WithStatement(node)).transform()

                expect(method_declaration.body).to(be(node.body))

        with context('with a name composed of three parts:'):
            with it('at the beginning, an 8-digit identification number representing execution order'):
                for node in supported_example_declarations():
                    method_declaration = ExampleToMethod(WithStatement(node)).transform()
                    first_eight_digits_of_method_name = method_declaration.name[:8]

                    expect(first_eight_digits_of_method_name).to(match('^[0-9]{8}$'))

            with it('the "it" word'):
                for node in supported_example_declarations():
                    method_declaration = ExampleToMethod(WithStatement(node)).transform()

                    expect(method_declaration.name).to(match('it'))

            with it('the example wording included in the example declaration'):
                example_wordings = [
                    'does something',
                    'does something else, but this test will be skipped'
                ]

                for wording, node in zip(example_wordings, supported_example_declarations()):
                    method_declaration = ExampleToMethod(WithStatement(node)).transform()

                    expect(method_declaration.name).to(match(wording))


with description('the ExampleGroupToClass class'):
    with context('when given a `with` statement which does not match the example group declaration syntax'):
        with it('''can't transform it'''):
            for node in negative_examples_of_example_group_declarations():
                expect(
                    ExampleGroupToClass(WithStatement(node)).can_transform
                ).to(be_false)

    with context('transforms the `with` statement into a class definition'):
        with it('represents the class as a class definition node'):
            for node in supported_example_group_declarations():
                class_declaration = ExampleGroupToClass(WithStatement(node)).transform()

                expect(class_declaration).to(be_an(ast.ClassDef))

        with it('lists no explicit base classes, keyword parameters, or any kind of starred parameters'):
            for node in supported_example_group_declarations():
                class_declaration = ExampleGroupToClass(WithStatement(node)).transform()

                expect(class_declaration.decorator_list).to(equal([]))
                expect(class_declaration.bases).to(equal([]))
                expect(class_declaration.keywords).to(equal([]))
                expect(class_declaration.starargs).to(be_none)
                expect(class_declaration.kwargs).to(be_none)

        with context('with a name which always includes:'):
            with it('at the beginning, an 8-digit identification number representing execution order'):
                for node in supported_example_group_declarations():
                    class_declaration = ExampleGroupToClass(WithStatement(node)).transform()
                    first_eight_digits_of_class_name = class_declaration.name[:8]

                    expect(first_eight_digits_of_class_name).to(match('^[0-9]{8}$'))

            with context('for active example groups'):
                with it('at the end, the "__description" marker'):
                    for node in supported_active_example_group_declarations():
                        class_declaration = ExampleGroupToClass(WithStatement(node)).transform()

                        expect(class_declaration.name.endswith('__description')).to(be_true)

            with context('for pending example groups'):
                with it('at the end, the "__pending__description" marker'):
                    for node in supported_pending_example_group_declarations():
                        class_declaration = ExampleGroupToClass(WithStatement(node)).transform()

                        expect(class_declaration.name.endswith('__pending__description')).to(be_true)

        with context('when a wording is provided in the example group declaration'):
            with it('the class name includes the provided wording'):
                provided_wordings = [
                    'given...',
                    'when...',
                    'my subject under test',
                    'some behaviour, but this whole group will be skipped',
                    'grouping related tests, but this whole group will be skipped',
                    'my subject under test, but this whole group will be skipped'
                ]

                for wording, node in zip(provided_wordings, supported_example_group_declarations_with_wording()):
                    class_declaration = ExampleGroupToClass(WithStatement(node)).transform()

                    expect(class_declaration.name).to(match(wording))

            with it('the class body is the same as the body of the with statement'):
                for node in supported_example_group_declarations_with_wording():
                    class_declaration = ExampleGroupToClass(WithStatement(node)).transform()

                    expect(class_declaration.body).to(be(node.body))

        with context('when a name (a Python identifier) is provided in the example group declaration'):
            with before.each:
                self.provided_names = [
                    'MyUnitUnderTest',
                    'MyOtherUnitUnderTest',
                    'SomeClass',
                    'MyPendingUnitUnderTest',
                    'MyOtherPendingUnitUnderTest',
                    'SomePendingClass'
                ]

            with it('the class name includes the provided name'):
                for name, node in zip(self.provided_names, supported_example_group_declarations_with_name()):
                    class_declaration = ExampleGroupToClass(WithStatement(node)).transform()

                    expect(class_declaration.name).to(match(name))

            with it('the class body is the same as the body of the with statement, but including an assignment of a variable to the provided name'):
                for name, node in zip(self.provided_names, supported_example_group_declarations_with_name()):
                    class_declaration = ExampleGroupToClass(WithStatement(node)).transform()

                    first_node = class_declaration.body[0]
                    expect(first_node).to(be_an(ast.Assign))
                    expect(first_node.value).to(be_an(ast.Name))
                    expect(first_node.value.id).to(equal(name))

                    remaining_nodes = class_declaration.body[1:]
                    expect(remaining_nodes).to(equal(node.body))

        with context('when an attribute lookup is provided in the example group declaration'):
            with before.each:
                self.looked_up_names = [
                    'MyUnitUnderTest',
                    'MyOtherUnitUnderTest',
                    'SomeClass',
                    'MyPendingUnitUnderTest',
                    'MyOtherPendingUnitUnderTest',
                    'SomePendingClass'
                ]

            with it('the class name includes the name being looked up'):
                for name, node in zip(self.looked_up_names, supported_example_group_declarations_with_attribute_lookup()):
                    class_declaration = ExampleGroupToClass(WithStatement(node)).transform()

                    expect(class_declaration.name).to(match(name))

            with it('the class body is the same as the body of the with statement, but including an assignment of a variable to the provided attribute lookup'):
                for name, node in zip(self.looked_up_names, supported_example_group_declarations_with_attribute_lookup()):
                    class_declaration = ExampleGroupToClass(WithStatement(node)).transform()

                    first_node = class_declaration.body[0]
                    expect(first_node).to(be_an(ast.Assign))
                    expect(first_node.value).to(be_an(ast.Attribute))
                    expect(first_node.value.attr).to(equal(name))

                    remaining_nodes = class_declaration.body[1:]
                    expect(remaining_nodes).to(equal(node.body))




def supported_hook_declarations():
    return top_level_ast_nodes_of_fixture_at('supported_hook_declarations.py')

def negative_examples_of_hook_declarations():
    return top_level_ast_nodes_of_fixture_at('negative_examples/not_hook_declarations.py')


def supported_example_declarations():
    return top_level_ast_nodes_of_fixture_at('supported_example_declarations.py')

def negative_examples_of_example_declarations():
    return top_level_ast_nodes_of_fixture_at('negative_examples/not_example_declarations.py')


def supported_example_group_declarations():
    return supported_active_example_group_declarations() + \
        supported_pending_example_group_declarations()

def supported_active_example_group_declarations():
    return top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/active_with_wording.py') + \
        top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/active_with_name.py') + \
        top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/active_with_attribute_lookup.py')

def supported_pending_example_group_declarations():
    return top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/pending_with_wording.py') + \
        top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/pending_with_name.py') + \
        top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/pending_with_attribute_lookup.py')


def supported_example_group_declarations_with_wording():
    return top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/active_with_wording.py') + \
        top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/pending_with_wording.py')

def supported_example_group_declarations_with_name():
    return top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/active_with_name.py') + \
        top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/pending_with_name.py')

def supported_example_group_declarations_with_attribute_lookup():
    return top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/active_with_attribute_lookup.py') + \
        top_level_ast_nodes_of_fixture_at('supported_example_group_declarations/pending_with_attribute_lookup.py')

def negative_examples_of_example_group_declarations():
    return top_level_ast_nodes_of_fixture_at('negative_examples/not_example_group_declarations.py')
