import ast

from mamba.infrastructure import is_python3


class MambaIdentifiers(object):
    class EXAMPLE_GROUP(object):
        @property
        def ACTIVE(self):
            return ('description', 'context', 'describe')

        @property
        def PENDING(self):
            return MambaIdentifiers._compute_pending_identifiers(self.ACTIVE)

        @property
        def ALL(self):
            return self.ACTIVE + self.PENDING

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

    @staticmethod
    def _compute_pending_identifiers(identifiers):
        return tuple('_' + identifier for identifier in identifiers)


class MambaSyntaxToClassBasedSyntax(ast.NodeTransformer):
    def __init__(self):
        self._transformer_classes = [
            ExampleDeclarationToMethodDeclaration,
            ExampleGroupDeclarationToClassDeclaration,
            HookDeclarationToMethodDeclaration
        ]

    def visit_With(self, node):
        self._transform_nested_nodes_of(node)

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
        self._body = with_statement.body

        self._create_call_or_raise(with_statement.argument)
        if not self._is_valid():
            raise NotAnExampleDeclaration()

    def _create_call_or_raise(self, argument_to_with_statement):
        try:
            self._call = CallOnANameWhereFirstArgumentIsString(argument_to_with_statement)
        except UnexpectedCallStructure:
            raise NotAnExampleDeclaration()

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


class CallOnANameWithAtLeastOneArgument(object):
    def __init__(self, node):
        self._node = node

        if not self._is_valid():
            raise UnexpectedCallStructure()

    def _is_valid(self):
        return self._is_call_on_a_name() and self._has_at_least_one_argument()

    def _is_call_on_a_name(self):
        return self._is_call() and self._called_expression_is_name()

    def _is_call(self):
        return isinstance(self._node, ast.Call)

    def _called_expression_is_name(self):
        return isinstance(self._node.func, ast.Name)

    def _has_at_least_one_argument(self):
        return len(self._node.args) >= 1

    @property
    def called_name(self):
        return self._node.func.id

    @property
    def first_argument_node(self):
        return self._node.args[0]


class CallOnANameWhereFirstArgumentIsString(CallOnANameWithAtLeastOneArgument):
    def __init__(self, node):
        super(CallOnANameWhereFirstArgumentIsString, self).__init__(node)

        if not self._first_argument_is_string():
            raise UnexpectedCallStructure()

    def _first_argument_is_string(self):
        return isinstance(self.first_argument_node, ast.Str)

    @property
    def first_argument(self):
        return self.first_argument_node.s


class Counter(object):
    _current_number = 0

    @staticmethod
    def get_next():
        next_number = Counter._current_number
        Counter._current_number += 1

        return next_number


class ExampleGroupDeclarationToClassDeclaration(object):
    _ACTIVE_EXAMPlE_GROUP_MARKER = 'description'
    _PENDING_EXAMPLE_GROUP_MARKER = 'pending__' + _ACTIVE_EXAMPlE_GROUP_MARKER

    _NAME_OF_CLASS_VARIABLE_HOLDING_SUBJECT_CLASS = '_subject_class'

    def __init__(self, with_statement_node):
        self._example_group_declaration = ExampleGroupDeclaration(WithStatement(with_statement_node))

    def transform(self):
        return ClassDeclaration(
            self._compute_name_of_class(),
            self._compute_body_of_class()
        ).toAst()

    def _compute_name_of_class(self):
        return '__'.join([
            self._compute_id_of_class(),
            self._example_group_declaration.wording,
            self._compute_marker_for_example_group()
        ])

    def _compute_id_of_class(self):
        return '{0:08d}'.format(Counter.get_next())

    def _compute_marker_for_example_group(self):
        if self._example_group_declaration.is_pending:
            return ExampleGroupDeclarationToClassDeclaration._PENDING_EXAMPLE_GROUP_MARKER
        return ExampleGroupDeclarationToClassDeclaration._ACTIVE_EXAMPlE_GROUP_MARKER

    def _compute_body_of_class(self):
        declared_body = self._example_group_declaration.body
        if not self._example_group_declaration.has_explicit_subject_declaration:
            return declared_body

        return [self._create_assignment_of_subject_name()] + declared_body

    def _create_assignment_of_subject_name(self):
        return AssignmentOfExpressionToName(
            left_hand_side_name=ExampleGroupDeclarationToClassDeclaration._NAME_OF_CLASS_VARIABLE_HOLDING_SUBJECT_CLASS,
            right_hand_side=self._example_group_declaration.subject_node
        ).toAst()


class ExampleGroupDeclaration(object):
    def __init__(self, with_statement):
        self._EXAMPLE_GROUP_IDENTIFIERS = MambaIdentifiers.EXAMPLE_GROUP()
        self._supported_types_of_calls = [
            CallOnANameWhereFirstArgumentIsString,
            CallOnANameWhereFirstArgumentIsName,
            CallOnANameWhereFirstArgumentIsAttributeLookup
        ]
        self._body = with_statement.body

        self._create_call_or_raise(with_statement.argument)
        if not self._is_valid():
            raise NotAnExampleGroupDeclaration()

    def _create_call_or_raise(self, argument_to_with_statement):
        for type_of_call in self._supported_types_of_calls:
            try:
                self._call = type_of_call(argument_to_with_statement)
            except UnexpectedCallStructure:
                pass
            else:
                return

        raise NotAnExampleGroupDeclaration()

    def _is_valid(self):
        return self._call.called_name in self._EXAMPLE_GROUP_IDENTIFIERS.ALL

    @property
    def wording(self):
        if self.has_explicit_subject_declaration:
            return self._call.name_passed_as_first_argument
        return self._call.first_argument

    @property
    def is_pending(self):
        return self._call.called_name in self._EXAMPLE_GROUP_IDENTIFIERS.PENDING

    @property
    def body(self):
        return self._body

    @property
    def has_explicit_subject_declaration(self):
        return hasattr(self._call, 'name_passed_as_first_argument')

    @property
    def subject_node(self):
        return self._call.first_argument_node


class ClassDeclaration(object):
    def __init__(self, name, body):
        self._name = name
        self._body = body

    def toAst(self):
        return ast.ClassDef(
            decorator_list=[],
            name=self._name,
            bases=[],
            keywords=[],
            starargs=None,
            kwargs=None,
            body=self._body
        )


class CallOnANameWhereFirstArgumentIsName(CallOnANameWithAtLeastOneArgument):
    def __init__(self, node):
        super(CallOnANameWhereFirstArgumentIsName, self).__init__(node)

        if not self._first_argument_is_name():
            raise UnexpectedCallStructure()

    def _first_argument_is_name(self):
        return isinstance(self.first_argument_node, ast.Name)

    @property
    def name_passed_as_first_argument(self):
        return self.first_argument_node.id


class AssignmentOfExpressionToName(object):
    def __init__(self, left_hand_side_name, right_hand_side):
        self._left_hand_side_name = left_hand_side_name
        self._right_hand_side = right_hand_side

    def toAst(self):
        return ast.Assign(
            targets=[ast.Name(id=self._left_hand_side_name, ctx=ast.Store())],
            value=self._compute_right_hand_side()
        )

    def _compute_right_hand_side(self):
        if not isinstance(self._right_hand_side, basestring):
            return self._right_hand_side
        return ast.Name(id=self._right_hand_side, ctx=ast.Load())


class CallOnANameWhereFirstArgumentIsAttributeLookup(CallOnANameWithAtLeastOneArgument):
    def __init__(self, node):
        super(CallOnANameWhereFirstArgumentIsAttributeLookup, self).__init__(node)

        if not self._first_argument_is_attribute_lookup():
            raise UnexpectedCallStructure()

    def _first_argument_is_attribute_lookup(self):
        return isinstance(self.first_argument_node, ast.Attribute)

    @property
    def name_passed_as_first_argument(self):
        return self.first_argument_node.attr


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
    pass

class NotAnExampleGroupDeclaration(NodeShouldNotBeTransformed):
    pass

class UnexpectedCallStructure(Exception):
    pass
