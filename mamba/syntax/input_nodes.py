import ast

from ..infrastructure import is_python3


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
    def is_valid(self):
        return super(CallOnANameWhereFirstArgumentIsString, self).is_valid() and self._first_argument_is_string()

    def _first_argument_is_string(self):
        return isinstance(self.first_argument_node, ast.Str)

    @property
    def first_argument(self):
        return self.first_argument_node.s


class CallOnANameWhereFirstArgumentIsName(CallOnANameWithAtLeastOneArgument):
    def is_valid(self):
        return super(CallOnANameWhereFirstArgumentIsName, self).is_valid() and self._first_argument_is_name()

    def _first_argument_is_name(self):
        return isinstance(self.first_argument_node, ast.Name)

    @property
    def name_passed_as_first_argument(self):
        return self.first_argument_node.id


class CallOnANameWhereFirstArgumentIsAttributeLookup(CallOnANameWithAtLeastOneArgument):
    def is_valid(self):
        return super(CallOnANameWhereFirstArgumentIsAttributeLookup, self).is_valid() and self._first_argument_is_attribute_lookup()

    def _first_argument_is_attribute_lookup(self):
        return isinstance(self.first_argument_node, ast.Attribute)

    @property
    def name_passed_as_first_argument(self):
        return self.first_argument_node.attr
