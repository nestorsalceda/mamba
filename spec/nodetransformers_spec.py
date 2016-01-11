# -*- coding: utf-8 -*-

import ast
import functools

from expects import expect, raise_error, be_an, have_length, equal, be

from mamba.nodetransformers import HookDeclarationToMethodDeclaration, NodeShouldNotBeTransformed
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

            for hook_declaration, hook_name in zip(top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py'), hook_names):
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
                name_of_first_parameter = self._retrieve_name_of_parameter(first_parameter)

                expect(name_of_first_parameter).to(equal('self'))

        def _retrieve_name_of_parameter(self, function_parameter_node):
            if is_python3():
                return function_parameter_node.arg
            return function_parameter_node.id

        with it('uses the original body of the `with` statement'):
            for hook_declaration in top_level_nodes_of_ast_of_fixture_file_at('supported_hook_declarations.py'):
                method_declaration = HookDeclarationToMethodDeclaration(hook_declaration).transform()

                expect(method_declaration.body).to(be(hook_declaration.body))
