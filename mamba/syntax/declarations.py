import ast

from .identifiers import MambaIdentifiers


class HookDeclaration(object):
    def __init__(self, with_statement):
        self._HOOK_IDENTIFIERS = MambaIdentifiers.HOOK()
        self._body = with_statement.body
        self._attribute_lookup = AttributeLookupOnAName(with_statement.argument)

    def is_valid(self):
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
        self._call = CallOnANameWhereFirstArgumentIsString(with_statement.argument)

    def is_valid(self):
        return self._call.is_valid() and self._call.called_name in self._EXAMPLE_IDENTIFIERS.ALL

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

    def is_valid(self):
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

    def is_valid(self):
        return super(CallOnANameWhereFirstArgumentIsString, self).is_valid() and self._first_argument_is_string()

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
        self._create_call(with_statement.argument)

    def _create_call(self, argument_to_with_statement):
        for type_of_call in self._supported_types_of_calls:
            self._call = type_of_call(argument_to_with_statement)

            if self._call.is_valid():
                return

    def is_valid(self):
        return self._call.is_valid() and self._call.called_name in self._EXAMPLE_GROUP_IDENTIFIERS.ALL

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

    def is_valid(self):
        return super(CallOnANameWhereFirstArgumentIsName, self).is_valid() and self._first_argument_is_name()

    def _first_argument_is_name(self):
        return isinstance(self.first_argument_node, ast.Name)

    @property
    def name_passed_as_first_argument(self):
        return self.first_argument_node.id


class CallOnANameWhereFirstArgumentIsAttributeLookup(CallOnANameWithAtLeastOneArgument):
    def __init__(self, node):
        super(CallOnANameWhereFirstArgumentIsAttributeLookup, self).__init__(node)

    def is_valid(self):
        return super(CallOnANameWhereFirstArgumentIsAttributeLookup, self).is_valid() and self._first_argument_is_attribute_lookup()

    def _first_argument_is_attribute_lookup(self):
        return isinstance(self.first_argument_node, ast.Attribute)

    @property
    def name_passed_as_first_argument(self):
        return self.first_argument_node.attr
