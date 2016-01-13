import ast

from mamba.infrastructure import is_python3


class MambaIdentifiers(object):
    @property
    def ACTIVE_EXAMPLE_GROUP(self):
        return ('description', 'context', 'describe')

    @property
    def PENDING_EXAMPLE_GROUP(self):
        return self._compute_pending_identifiers(self.ACTIVE_EXAMPLE_GROUP)

    @staticmethod
    def _compute_pending_identifiers(identifiers):
        return tuple('_' + identifier for identifier in identifiers)

    @property
    def EXAMPLE_GROUP(self):
        return self.ACTIVE_EXAMPLE_GROUP + self.PENDING_EXAMPLE_GROUP

    class EXAMPLE(object):
        @property
        def ACTIVE(self):
            return ('it',)

        @property
        def PENDING(self):
            return MambaIdentifiers._compute_pending_identifiers(self.ACTIVE)

        @property
        def ALL(self):
            return self.ACTIVE + self.PENDING

    class HOOK(object):
        @property
        def RUN_ORDERS(self):
            return ('before', 'after')

        @property
        def SCOPES(self):
            return ('all', 'each')


class MambaSyntaxToClassBasedSyntax(ast.NodeTransformer):
    def __init__(self):
        self._number_of_examples_and_example_groups_processed = 0
        self._MAMBA_IDENTIFIERS = MambaIdentifiers()

        self._transformer_classes = [
            ExampleDeclarationToMethodDeclaration,
            HookDeclarationToMethodDeclaration
        ]

    def visit_With(self, node):
        self._transform_nested_nodes_of(node)

        if not self._is_relevant_with_statement(node):
            return node

        name = self._mamba_identifier_of(node)

        if name in self._MAMBA_IDENTIFIERS.EXAMPLE_GROUP:
            return self._transform_to_example_group(node, name)
        for transformer_class in self._transformer_classes:
            try:
                transformer = transformer_class(node)
            except NodeShouldNotBeTransformed:
                pass
            else:
                return transformer.transform()

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

    def _context_expr_for(self, node):
        return node.context_expr

    def _transform_to_example_group(self, node, name):
        argument_of_example_group = self._context_expr_for(node).args[0]

        if not self._represents_a_string_literal(argument_of_example_group):
            self._insert_subject_registration_assignment(node, argument_of_example_group)

        return ast.copy_location(
            ast.ClassDef(
                name=self._compute_title_of_example_group(argument_of_example_group, name),
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

    def _compute_title_of_example_group(self, argument_of_example_group, name):
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


class MambaSyntaxToClassBasedSyntaxPython3(MambaSyntaxToClassBasedSyntax):
    def _context_expr_for(self, node):
        return node.items[0].context_expr



class HookDeclarationToMethodDeclaration(object):
    def __init__(self, with_statement_node):
        self._hook_declaration = HookDeclaration(WithStatement(with_statement_node))

    def transform(self):
        return MethodDeclaration(
            self._compute_name_of_method(),
            self._hook_declaration.body
        ).toAst()

    def _compute_name_of_method(self):
        return self._hook_declaration.run_order + '_' + self._hook_declaration.scope


class WithStatement(object):
    def __init__(self, with_statement_node):
        self._with_statement_node = with_statement_node

    if is_python3():
        @property
        def argument(self):
            return self._with_statement_node.items[0].context_expr
    else:
        @property
        def argument(self):
            return self._with_statement_node.context_expr

    @property
    def body(self):
        return self._with_statement_node.body


class HookDeclaration(object):
    def __init__(self, with_statement):
        self._HOOK_IDENTIFIERS = MambaIdentifiers.HOOK()
        self._attribute_lookup = AttributeLookupOnAName(with_statement.argument)
        self._body = with_statement.body

        if not self._is_valid():
            raise NotAHookDeclaration(with_statement.argument)

    def _is_valid(self):
        return self._has_valid_run_order() and self._has_valid_scope()

    def _has_valid_run_order(self):
        return self.run_order in self._HOOK_IDENTIFIERS.RUN_ORDERS

    def _has_valid_scope(self):
        return self.scope in self._HOOK_IDENTIFIERS.SCOPES

    @property
    def run_order(self):
        return self._attribute_lookup.name

    @property
    def scope(self):
        return self._attribute_lookup.attribute

    @property
    def body(self):
        return self._body


class AttributeLookupOnAName(object):
    def __init__(self, node):
        self._node = node

        if not self._is_valid():
            raise NotAnAttributeLookupOnAName(node)

    def _is_valid(self):
        return self._is_attribute_lookup() and isinstance(self._node.value, ast.Name)

    def _is_attribute_lookup(self):
        return isinstance(self._node, ast.Attribute)

    @property
    def name(self):
        return self._node.value.id

    @property
    def attribute(self):
        return self._node.attr


class MethodDeclaration(object):
    def __init__(self, name, body):
        self._name = name
        self._body = body

    def toAst(self):
        return ast.FunctionDef(
            name=self._name,
            args=self._generate_empty_parameter_list_for_method(),
            body=self._body,
            decorator_list=[]
        )


    if is_python3():
        def _generate_empty_parameter_list_for_method(self):
            return ast.arguments(
                args=[ast.arg(arg='self', annotation=None)],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[]
            )
    else:
        def _generate_empty_parameter_list_for_method(self):
            return ast.arguments(
                args=[ast.Name(id='self', ctx=ast.Param())],
                vararg=None,
                kwarg=None,
                defaults=[]
            )


class ExampleDeclarationToMethodDeclaration(object):
    def __init__(self, with_statement_node):
        self._example_declaration = ExampleDeclaration(WithStatement(with_statement_node))

    def transform(self):
        return MethodDeclaration(
            self._compute_name_of_method(),
            self._example_declaration.body
        ).toAst()

    def _compute_name_of_method(self):
        return '{0}__{1} {2}'.format(
            self._compute_id_of_method(),
            self._example_declaration.example_identifier,
            self._example_declaration.wording
        )

    def _compute_id_of_method(self):
        return '{0:08d}'.format(Counter.get_next())


class ExampleDeclaration(object):
    def __init__(self, with_statement):
        self._EXAMPLE_IDENTIFIERS = MambaIdentifiers.EXAMPLE()
        self._call = CallOnANameWhereFirstArgumentIsString(with_statement.argument)
        self._body = with_statement.body

        if not self._is_valid():
            raise NotAnExampleDeclaration(with_statement.argument)

    def _is_valid(self):
        return self._call.called_name in self._EXAMPLE_IDENTIFIERS.ALL

    @property
    def example_identifier(self):
        return self._call.called_name

    @property
    def wording(self):
        return self._call.first_argument

    @property
    def body(self):
        return self._body


class CallOnANameWhereFirstArgumentIsString(object):
    def __init__(self, node):
        self._node = node

        if not self._is_valid():
            raise NotACallOnANameWhereFirstArgumentIsString(node)

    def _is_valid(self):
        return self._is_call_on_a_name() and self._first_argument_is_string()

    def _is_call_on_a_name(self):
        return self._is_call() and self._called_expression_is_name()

    def _is_call(self):
        return isinstance(self._node, ast.Call)

    def _called_expression_is_name(self):
        return isinstance(self._node.func, ast.Name)

    def _first_argument_is_string(self):
        return self._has_arguments() and isinstance(self._node.args[0], ast.Str)

    def _has_arguments(self):
        return len(self._node.args) > 0

    @property
    def called_name(self):
        return self._node.func.id

    @property
    def first_argument(self):
        return self._node.args[0].s


class Counter(object):
    _current_number = 0

    @staticmethod
    def get_next():
        next_number = Counter._current_number
        Counter._current_number += 1

        return next_number


class NodeShouldNotBeTransformed(Exception):
    pass

class NotAHookDeclaration(NodeShouldNotBeTransformed):
    def __init__(self, node):
        self.message = 'The node {0} is not a hook declaration: it doesn\'t match the hook declaration syntax'.format(
            node
        )

        super(NotAHookDeclaration, self).__init__(self.message)

class NotAnAttributeLookupOnAName(NodeShouldNotBeTransformed):
    def __init__(self, node):
        self.message = 'The node {0} is not an attribute lookup on a name'.format(
            node
        )

        super(NotAnAttributeLookupOnAName, self).__init__(self.message)

class NotAnExampleDeclaration(NodeShouldNotBeTransformed):
    def __init__(self, node):
        self.message = 'The node {0} is not an example declaration: it doesn\'t match the example declaration syntax'.format(
            node
        )

        super(NotAnExampleDeclaration, self).__init__(self.message)

class NotACallOnANameWhereFirstArgumentIsString(NodeShouldNotBeTransformed):
    def __init__(self, node):
        self.message = 'The node {0} is not a call on a name where the first argument is a string'.format(
            node
        )

        super(NotACallOnANameWhereFirstArgumentIsString, self).__init__(self.message)
