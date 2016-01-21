# -*- coding: utf-8 -*-

import ast
import functools

from expects import expect, raise_error, be_an, have_length, equal, be, match, be_none, be_true

from mamba.syntax.transformer import (
    WithStatement,
    HookDeclarationToMethodDeclaration,
    ExampleDeclarationToMethodDeclaration,
    ExampleGroupDeclarationToClassDeclaration
)
from mamba.syntax.declarations import NotARelevantNode
from mamba.infrastructure import is_python3

from .helpers import top_level_nodes_of_ast_of_fixture_file_at
top_level_nodes_of_ast_of_fixture_file_at = functools.partial(top_level_nodes_of_ast_of_fixture_file_at, __file__)


with description('the HookDeclarationToMethodDeclaration class'):
    with context('when given a `with` statement which does not match the hook declaration syntax'):
        with it('raises an error'):
            for with_statement_but_not_a_hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('with_statement_but_not_a_hook_declaration.py'):
                expect(lambda: HookDeclarationToMethodDeclaration(WithStatement(with_statement_but_not_a_hook_declaration))).to(
                    raise_error(NotARelevantNode)
                )

    with context('transforms the `with` statement into a method definition'):
        with it('represents the method as a function definition node'):
            for hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py'):
                method_declaration = HookDeclarationToMethodDeclaration(WithStatement(hook_declaration)).transform()

                expect(method_declaration).to(be_an(ast.FunctionDef))

        with it('names the method after the hook'):
            hook_names = ['before_all', 'before_each', 'after_each', 'after_all']

            for hook_name, hook_declaration in zip(hook_names, top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py')):
                method_declaration = HookDeclarationToMethodDeclaration(WithStatement(hook_declaration)).transform()

                expect(method_declaration.name).to(equal(hook_name))

        with it('includes only one parameter'):
            for hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py'):
                method_declaration = HookDeclarationToMethodDeclaration(WithStatement(hook_declaration)).transform()
                function_parameters = method_declaration.args.args

                expect(function_parameters).to(have_length(1))

        with it('the first parameter is named `self`'):
            for hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py'):
                method_declaration = HookDeclarationToMethodDeclaration(WithStatement(hook_declaration)).transform()
                function_parameters = method_declaration.args.args
                first_parameter = function_parameters[0]
                name_of_first_parameter = _retrieve_name_of_parameter(first_parameter)

                expect(name_of_first_parameter).to(equal('self'))

        with it('uses the original body of the `with` statement'):
            for hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py'):
                method_declaration = HookDeclarationToMethodDeclaration(WithStatement(hook_declaration)).transform()

                expect(method_declaration.body).to(be(hook_declaration.body))


with description('the ExampleDeclarationToMethodDeclaration class'):
    with context('when given a `with` statement which does not match the example declaration syntax'):
        with it('raises an error'):
            for with_statement_but_not_an_example_declaration in top_level_nodes_of_ast_of_fixture_file_at('with_statement_but_not_an_example_declaration.py'):
                expect(lambda: ExampleDeclarationToMethodDeclaration(WithStatement(with_statement_but_not_an_example_declaration))).to(
                    raise_error(NotARelevantNode)
                )

    with context('transforms the `with` statement into a method definition'):
        with it('represents the method as a function definition node'):
            for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                method_declaration = ExampleDeclarationToMethodDeclaration(WithStatement(example_declaration)).transform()

                expect(method_declaration).to(be_an(ast.FunctionDef))

        with it('includes only one parameter'):
            for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                method_declaration = ExampleDeclarationToMethodDeclaration(WithStatement(example_declaration)).transform()
                function_parameters = method_declaration.args.args

                expect(function_parameters).to(have_length(1))

        with it('the first parameter is named `self`'):
            for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                method_declaration = ExampleDeclarationToMethodDeclaration(WithStatement(example_declaration)).transform()
                function_parameters = method_declaration.args.args
                first_parameter = function_parameters[0]
                name_of_first_parameter = _retrieve_name_of_parameter(first_parameter)

                expect(name_of_first_parameter).to(equal('self'))

        with it('uses the original body of the `with` statement'):
            for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                method_declaration = ExampleDeclarationToMethodDeclaration(WithStatement(example_declaration)).transform()

                expect(method_declaration.body).to(be(example_declaration.body))

        with context('with a name composed of three parts:'):
            with it('at the beginning, an 8-digit identification number representing execution order'):
                for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                    method_declaration = ExampleDeclarationToMethodDeclaration(WithStatement(example_declaration)).transform()
                    first_eight_digits_of_method_name = method_declaration.name[:8]

                    expect(first_eight_digits_of_method_name).to(match('^[0-9]{8}$'))

            with it('the "it" word'):
                for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                    method_declaration = ExampleDeclarationToMethodDeclaration(WithStatement(example_declaration)).transform()

                    expect(method_declaration.name).to(match('it'))

            with it('the example wording included in the example declaration'):
                example_wordings = [
                    'does something',
                    'does something else, but this test will be skipped'
                ]

                for example_wording, example_declaration in zip(example_wordings, top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py')):
                    method_declaration = ExampleDeclarationToMethodDeclaration(WithStatement(example_declaration)).transform()

                    expect(method_declaration.name).to(match(example_wording))



def _retrieve_name_of_parameter(function_parameter_node):
    if is_python3():
        return function_parameter_node.arg
    return function_parameter_node.id


with description('the ExampleGroupDeclarationToClassDeclaration class'):
    with context('when given a `with` statement which does not match the example group declaration syntax'):
        with it('raises an error'):
            for with_statement_but_not_an_example_group_declaration in top_level_nodes_of_ast_of_fixture_file_at('with_statement_but_not_an_example_group_declaration.py'):
                expect(lambda: ExampleGroupDeclarationToClassDeclaration(WithStatement(with_statement_but_not_an_example_group_declaration))).to(
                    raise_error(NotARelevantNode)
                )

    with context('transforms the `with` statement into a class definition'):
        with it('represents the class as a class definition node'):
            for example_group_declaration in top_level_nodes_of_ast_of_all_sample_example_group_fixture_files():
                class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()

                expect(class_declaration).to(be_an(ast.ClassDef))

        with it('lists no explicit base classes, keyword parameters, or any kind of starred parameters'):
            for example_group_declaration in top_level_nodes_of_ast_of_all_sample_example_group_fixture_files():
                class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()

                expect(class_declaration.decorator_list).to(equal([]))
                expect(class_declaration.bases).to(equal([]))
                expect(class_declaration.keywords).to(equal([]))
                expect(class_declaration.starargs).to(be_none)
                expect(class_declaration.kwargs).to(be_none)

        with context('with a name which always includes:'):
            with it('at the beginning, an 8-digit identification number representing execution order'):
                for example_group_declaration in top_level_nodes_of_ast_of_all_sample_example_group_fixture_files():
                    class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()
                    first_eight_digits_of_class_name = class_declaration.name[:8]

                    expect(first_eight_digits_of_class_name).to(match('^[0-9]{8}$'))

            with context('for active example groups'):
                with it('at the end, the "__description" marker'):
                    for example_group_declaration in top_level_nodes_of_ast_of_all_sample_active_example_group_fixture_files():
                        class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()

                        expect(class_declaration.name.endswith('__description')).to(be_true)

            with context('for pending example groups'):
                with it('at the end, the "__pending__description" marker'):
                    for example_group_declaration in top_level_nodes_of_ast_of_all_sample_pending_example_group_fixture_files():
                        class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()

                        expect(class_declaration.name.endswith('__pending__description')).to(be_true)



        with context('when a wording is provided in the example group declaration'):
            with it('the class name includes the wording provided'):
                example_group_wordings = [
                    'given...',
                    'when...',
                    'my subject under test',
                    'some behaviour, but this whole group will be skipped',
                    'grouping related tests, but this whole group will be skipped',
                    'my subject under test, but this whole group will be skipped'
                ]

                for example_group_wording, example_group_declaration in zip(example_group_wordings, top_level_nodes_of_ast_of_all_sample_example_groups_with_wording_fixture_files()):
                    class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()

                    expect(class_declaration.name).to(match(example_group_wording))

            with it('the class body is the same as the body of the with statement'):
                for example_group_declaration in top_level_nodes_of_ast_of_all_sample_example_groups_with_wording_fixture_files():
                    class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()

                    expect(class_declaration.body).to(be(example_group_declaration.body))

        with context('when a name (a Python identifier) is provided in the example group declaration'):
            with it('the class name includes the provided name'):
                provided_names = [
                    'MyUnitUnderTest',
                    'MyOtherUnitUnderTest',
                    'SomeClass',
                    'MyPendingUnitUnderTest',
                    'MyOtherPendingUnitUnderTest',
                    'SomePendingClass'
                ]

                for name, example_group_declaration in zip(provided_names, top_level_nodes_of_ast_of_all_sample_example_groups_with_name_fixture_files()):
                    class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()

                    expect(class_declaration.name).to(match(name))

            with it('the class body is the same as the body of the with statement, but including an assignment of a variable to the provided name'):
                provided_names = [
                    'MyUnitUnderTest',
                    'MyOtherUnitUnderTest',
                    'SomeClass',
                    'MyPendingUnitUnderTest',
                    'MyOtherPendingUnitUnderTest',
                    'SomePendingClass'
                ]
                for name, example_group_declaration in zip(provided_names, top_level_nodes_of_ast_of_all_sample_example_groups_with_name_fixture_files()):
                    class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()

                    first_node = class_declaration.body[0]
                    expect(first_node).to(be_an(ast.Assign))
                    expect(first_node.value).to(be_an(ast.Name))
                    expect(first_node.value.id).to(equal(name))

                    remaining_nodes = class_declaration.body[1:]
                    expect(remaining_nodes).to(equal(example_group_declaration.body))

        with context('when an attribute lookup is provided in the example group declaration'):
            with it('the class name includes the name being looked up'):
                looked_up_names = [
                    'MyUnitUnderTest',
                    'MyOtherUnitUnderTest',
                    'SomeClass',
                    'MyPendingUnitUnderTest',
                    'MyOtherPendingUnitUnderTest',
                    'SomePendingClass'
                ]

                for name, example_group_declaration in zip(looked_up_names, top_level_nodes_of_ast_of_all_sample_example_groups_with_attribute_lookup_fixture_files()):
                    class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()

                    expect(class_declaration.name).to(match(name))

            with it('the class body is the same as the body of the with statement, but including an assignment of a variable to the provided attribute lookup'):
                looked_up_names = [
                    'MyUnitUnderTest',
                    'MyOtherUnitUnderTest',
                    'SomeClass',
                    'MyPendingUnitUnderTest',
                    'MyOtherPendingUnitUnderTest',
                    'SomePendingClass'
                ]

                for name, example_group_declaration in zip(looked_up_names, top_level_nodes_of_ast_of_all_sample_example_groups_with_attribute_lookup_fixture_files()):
                    class_declaration = ExampleGroupDeclarationToClassDeclaration(WithStatement(example_group_declaration)).transform()

                    first_node = class_declaration.body[0]
                    expect(first_node).to(be_an(ast.Assign))
                    expect(first_node.value).to(be_an(ast.Attribute))
                    expect(first_node.value.attr).to(equal(name))

                    remaining_nodes = class_declaration.body[1:]
                    expect(remaining_nodes).to(equal(example_group_declaration.body))


def top_level_nodes_of_ast_of_all_sample_example_group_fixture_files():
    return \
        top_level_nodes_of_ast_of_all_sample_active_example_group_fixture_files() + \
        top_level_nodes_of_ast_of_all_sample_pending_example_group_fixture_files()

def top_level_nodes_of_ast_of_all_sample_active_example_group_fixture_files():
    return \
        top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/active_with_wording.py') + \
        top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/active_with_name.py') + \
        top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/active_with_attribute_lookup.py')


def top_level_nodes_of_ast_of_all_sample_pending_example_group_fixture_files():
    return \
        top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/pending_with_wording.py') + \
        top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/pending_with_name.py') + \
        top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/pending_with_attribute_lookup.py')

def top_level_nodes_of_ast_of_all_sample_example_groups_with_wording_fixture_files():
    return \
        top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/active_with_wording.py') + \
        top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/pending_with_wording.py')

def top_level_nodes_of_ast_of_all_sample_example_groups_with_name_fixture_files():
    return \
        top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/active_with_name.py') + \
        top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/pending_with_name.py')

def top_level_nodes_of_ast_of_all_sample_example_groups_with_attribute_lookup_fixture_files():
    return top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/active_with_attribute_lookup.py') + \
           top_level_nodes_of_ast_of_fixture_file_at('sample_example_group_declarations/pending_with_attribute_lookup.py')
