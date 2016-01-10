import ast


class MambaIdentifiers(object):
    @property
    def ACTIVE_EXAMPLE_GROUP(self):
        return ('description', 'context', 'describe')

    @property
    def PENDING_EXAMPLE_GROUP(self):
        return self._compute_pending_identifiers(self.ACTIVE_EXAMPLE_GROUP)

    def _compute_pending_identifiers(self, identifiers):
        return tuple('_' + identifier for identifier in identifiers)

    @property
    def EXAMPLE_GROUP(self):
        return self.ACTIVE_EXAMPLE_GROUP + self.PENDING_EXAMPLE_GROUP

    @property
    def ACTIVE_EXAMPLE(self):
        return ('it',)

    @property
    def PENDING_EXAMPLE(self):
        return self._compute_pending_identifiers(self.ACTIVE_EXAMPLE)

    @property
    def EXAMPLE(self):
        return self.ACTIVE_EXAMPLE + self.PENDING_EXAMPLE

    @property
    def HOOKS(self):
        return ('before', 'after')


class MambaSyntaxToClassBasedSyntax(ast.NodeTransformer):
    def __init__(self):
        self._number_of_examples_and_example_groups_processed = 0
        self._MAMBA_IDENTIFIERS = MambaIdentifiers()

    def visit_With(self, node):
        self._transform_nested_nodes_of(node)

        if not self._is_relevant_with_statement(node):
            return node

        name = self._mamba_identifier_of(node)

        if name in self._MAMBA_IDENTIFIERS.EXAMPLE_GROUP:
            return self._transform_to_example_group(node, name)
        if name in self._MAMBA_IDENTIFIERS.EXAMPLE:
            return self._transform_to_example(node, name)
        if name in self._MAMBA_IDENTIFIERS.HOOKS:
            return self._transform_to_hook(node, name)

        return node

    def _transform_nested_nodes_of(self, node):
        super(MambaSyntaxToClassBasedSyntax, self).generic_visit(node)

    def _is_relevant_with_statement(self, node):
        return self._matches_structure_of_example_group_or_example_declaration(node) or self._matches_structure_of_hook_declaration(node)

    def _matches_structure_of_example_group_or_example_declaration(self, node):
        context_expr = self._context_expr_for(node)
        return isinstance(context_expr, ast.Call) and isinstance(context_expr.func, ast.Name)

    def _matches_structure_of_hook_declaration(self, node):
        context_expr = self._context_expr_for(node)
        return isinstance(context_expr, ast.Attribute) and isinstance(context_expr.value, ast.Name)

    def _mamba_identifier_of(self, node):
        if self._matches_structure_of_example_group_or_example_declaration(node):
            return self._context_expr_for(node).func.id

        if self._matches_structure_of_hook_declaration(node):
            return self._context_expr_for(node).value.id

    def _context_expr_for(self, node):
        return node.context_expr

    def _transform_to_example_group(self, node, name):
        argument_of_example_group = self._context_expr_for(node).args[0]

        if not self._represents_a_string_literal(argument_of_example_group):
            self._insert_subject_registration_assignment(node, argument_of_example_group)

        return ast.copy_location(
            ast.ClassDef(
                name=self._description_name(argument_of_example_group, name),
                bases=[],
                keywords=[],
                body=node.body,
                decorator_list=[]
            ),
            node
        )

    def _represents_a_string_literal(self, node):
        return isinstance(node, ast.Str)

    def _insert_subject_registration_assignment(self, node, node_representing_subject):
        node.body.insert(0, self._create_assignment_of_name_to_value('_subject_class', node_representing_subject))

    def _create_assignment_of_name_to_value(self, name, ast_of_value):
        return ast.Assign(targets=[ast.Name(id=name, ctx=ast.Store())], value=ast_of_value)

    def _description_name(self, argument_of_example_group, name):
        if self._represents_a_string_literal(argument_of_example_group):
            description_name = argument_of_example_group.s
        elif isinstance(argument_of_example_group, ast.Attribute):
            description_name = argument_of_example_group.attr
        else:
            description_name = argument_of_example_group.id

        if name in self._MAMBA_IDENTIFIERS.PENDING_EXAMPLE_GROUP:
            description_name += '__pending'

        description_name = '{0:08d}__{1}__description'.format(self._number_of_examples_and_example_groups_processed, description_name)
        self._number_of_examples_and_example_groups_processed += 1

        return description_name

    def _transform_to_example(self, node, name):
        example_name = '{0:08d}__{1} {2}'.format(self._number_of_examples_and_example_groups_processed, name, self._context_expr_for(node).args[0].s)
        self._number_of_examples_and_example_groups_processed += 1
        return ast.copy_location(
            ast.FunctionDef(
                name=example_name,
                args=self._generate_self(),
                body=node.body,
                decorator_list=[]
            ),
            node
        )

    def _generate_self(self):
        return ast.arguments(args=[ast.Name(id='self', ctx=ast.Param())], vararg=None, kwarg=None, defaults=[])

    def _transform_to_hook(self, node, name):
        scope_of_hook = self._context_expr_for(node).attr
        return ast.copy_location(
            ast.FunctionDef(
                name=name + '_' + scope_of_hook,
                args=self._generate_self(),
                body=node.body,
                decorator_list=[]
            ),
            node
        )


class MambaSyntaxToClassBasedSyntaxPython3(MambaSyntaxToClassBasedSyntax):
    def _context_expr_for(self, node):
        return node.items[0].context_expr

    def _generate_self(self):
        return ast.arguments(
            args=[ast.arg(arg='self', annotation=None)],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[]
        )

