# -*- coding: utf-8 -*-

import ast
import functools

from expects import expect, raise_error, be_an, have_length, equal, be, match

from mamba.nodetransformers import HookDeclarationToMethodDeclaration, NodeShouldNotBeTransformed, ExampleDeclarationToMethodDeclaration
from mamba.infrastructure import is_python3

from .helpers import top_level_nodes_of_ast_of_fixture_file_at
top_level_nodes_of_ast_of_fixture_file_at = functools.partial(top_level_nodes_of_ast_of_fixture_file_at, __file__)


with description('the HookDeclarationToMethodDeclaration class'):
    with context('when given a `with` statement which does not match the hook declaration syntax'):
        with it('raises an error'):
            for with_statement_but_not_a_hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('with_statement_but_not_a_hook_declaration.py'):
                expect(lambda: HookDeclarationToMethodDeclaration(with_statement_but_not_a_hook_declaration)).to(
                    raise_error(NodeShouldNotBeTransformed)
                )

    with context('transforms the `with` statement into a method definition'):
        with it('represents the method as a function definition node'):
            for hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py'):
                method_declaration = HookDeclarationToMethodDeclaration(hook_declaration).transform()

                expect(method_declaration).to(be_an(ast.FunctionDef))

        with it('names the method after the hook'):
            hook_names = ['before_all', 'before_each', 'after_each', 'after_all']

            for hook_name, hook_declaration in zip(hook_names, top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py')):
                method_declaration = HookDeclarationToMethodDeclaration(hook_declaration).transform()

                expect(method_declaration.name).to(equal(hook_name))

        with it('includes only one parameter'):
            for hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py'):
                method_declaration = HookDeclarationToMethodDeclaration(hook_declaration).transform()
                function_parameters = method_declaration.args.args

                expect(function_parameters).to(have_length(1))

        with it('the first parameter is named `self`'):
            for hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py'):
                method_declaration = HookDeclarationToMethodDeclaration(hook_declaration).transform()
                function_parameters = method_declaration.args.args
                first_parameter = function_parameters[0]
                name_of_first_parameter = _retrieve_name_of_parameter(first_parameter)

                expect(name_of_first_parameter).to(equal('self'))

        with it('uses the original body of the `with` statement'):
            for hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py'):
                method_declaration = HookDeclarationToMethodDeclaration(hook_declaration).transform()

                expect(method_declaration.body).to(be(hook_declaration.body))


with description('the ExampleDeclarationToMethodDeclaration class'):
    with context('when given a `with` statement which does not match the example declaration syntax'):
        with it('raises an error'):
            for with_statement_but_not_an_example_declaration in top_level_nodes_of_ast_of_fixture_file_at('with_statement_but_not_an_example_declaration.py'):
                expect(lambda: ExampleDeclarationToMethodDeclaration(with_statement_but_not_an_example_declaration)).to(
                    raise_error(NodeShouldNotBeTransformed)
                )

    with context('transforms the `with` statement into a method definition'):
        with it('represents the method as a function definition node'):
            for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                method_declaration = ExampleDeclarationToMethodDeclaration(example_declaration).transform()

                expect(method_declaration).to(be_an(ast.FunctionDef))

        with it('includes only one parameter'):
            for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                method_declaration = ExampleDeclarationToMethodDeclaration(example_declaration).transform()
                function_parameters = method_declaration.args.args

                expect(function_parameters).to(have_length(1))

        with it('the first parameter is named `self`'):
            for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                method_declaration = ExampleDeclarationToMethodDeclaration(example_declaration).transform()
                function_parameters = method_declaration.args.args
                first_parameter = function_parameters[0]
                name_of_first_parameter = _retrieve_name_of_parameter(first_parameter)

                expect(name_of_first_parameter).to(equal('self'))

        with it('uses the original body of the `with` statement'):
            for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                method_declaration = ExampleDeclarationToMethodDeclaration(example_declaration).transform()

                expect(method_declaration.body).to(be(example_declaration.body))

        with context('with a name composed of three parts:'):
            with it('at the beginning, a 8-digit identification number representing execution order'):
                for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                    method_declaration = ExampleDeclarationToMethodDeclaration(example_declaration).transform()
                    first_eight_digits_of_method_name = method_declaration.name[:8]

                    expect(first_eight_digits_of_method_name).to(match('^[0-9]{8}$'))

            with it('the "it" word'):
                for example_declaration in top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py'):
                    method_declaration = ExampleDeclarationToMethodDeclaration(example_declaration).transform()

                    expect(method_declaration.name).to(match('it'))

            with it('the example wording included in the example declaration'):
                example_wordings = [
                    'does something',
                    'does something else, but this test will be skipped'
                ]

                for example_wording, example_declaration in zip(example_wordings, top_level_nodes_of_ast_of_fixture_file_at('sample_example_declarations.py')):
                    method_declaration = ExampleDeclarationToMethodDeclaration(example_declaration).transform()

                    expect(method_declaration.name).to(match(example_wording))



def _retrieve_name_of_parameter(function_parameter_node):
    if is_python3():
        return function_parameter_node.arg
    return function_parameter_node.id
