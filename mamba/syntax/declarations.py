import ast


from . import identifiers
from .input_nodes import (
    AttributeLookupOnAName,
    CallOnANameWhereFirstArgumentIsString,
    CallOnANameWhereFirstArgumentIsName,
    CallOnANameWhereFirstArgumentIsAttributeLookup
)


class HookDeclaration(object):
    def __init__(self, with_statement):
        self._HOOK_IDENTIFIERS = identifiers.HOOK
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


class ExampleDeclaration(object):
    def __init__(self, with_statement):
        self._EXAMPLE_IDENTIFIERS = identifiers.EXAMPLE
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


class ExampleGroupDeclaration(object):
    def __init__(self, with_statement):
        self._EXAMPLE_GROUP_IDENTIFIERS = identifiers.EXAMPLE_GROUP
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
