import ast

from .identifiers import MambaIdentifiers


class HookDeclaration(object):
    def __init__(self, with_statement):
        self._HOOK_IDENTIFIERS = MambaIdentifiers.HOOK()
        self._body = with_statement.body
        self._attribute_lookup = AttributeLookupOnAName(with_statement.argument)

        if not self._is_valid():
            raise NotAHookDeclaration()

    def _is_valid(self):
        return self._attribute_lookup.is_valid() and self._has_valid_run_order() and self._has_valid_scope()

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

    def is_valid(self):
        return self._is_attribute_lookup() and isinstance(self._node.value, ast.Name)

    def _is_attribute_lookup(self):
        return isinstance(self._node, ast.Attribute)

    @property
    def name(self):
        return self._node.value.id

    @property
    def attribute(self):
        return self._node.attr



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
        except BadNodeStructure:
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
            raise BadNodeStructure()

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
            raise BadNodeStructure()

    def _first_argument_is_string(self):
        return isinstance(self.first_argument_node, ast.Str)

    @property
    def first_argument(self):
        return self.first_argument_node.s


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
            except BadNodeStructure:
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


class CallOnANameWhereFirstArgumentIsName(CallOnANameWithAtLeastOneArgument):
    def __init__(self, node):
        super(CallOnANameWhereFirstArgumentIsName, self).__init__(node)

        if not self._first_argument_is_name():
            raise BadNodeStructure()

    def _first_argument_is_name(self):
        return isinstance(self.first_argument_node, ast.Name)

    @property
    def name_passed_as_first_argument(self):
        return self.first_argument_node.id


class CallOnANameWhereFirstArgumentIsAttributeLookup(CallOnANameWithAtLeastOneArgument):
    def __init__(self, node):
        super(CallOnANameWhereFirstArgumentIsAttributeLookup, self).__init__(node)

        if not self._first_argument_is_attribute_lookup():
            raise BadNodeStructure()

    def _first_argument_is_attribute_lookup(self):
        return isinstance(self.first_argument_node, ast.Attribute)

    @property
    def name_passed_as_first_argument(self):
        return self.first_argument_node.attr


class BadNodeStructure(Exception):
    pass

class NotARelevantNode(Exception):
    pass

class NotAHookDeclaration(NotARelevantNode):
    pass

class NotAnExampleDeclaration(NotARelevantNode):
    pass

class NotAnExampleGroupDeclaration(NotARelevantNode):
    pass

