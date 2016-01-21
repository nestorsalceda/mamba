import ast

from .input_nodes import WithStatement
from .declarations import HookDeclaration, ExampleDeclaration, ExampleGroupDeclaration, NotARelevantNode
from .output_nodes import MethodDeclaration, ClassDeclaration, AssignmentOfExpressionToName


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
                transformer = transformer_class(WithStatement(node))
            except NotARelevantNode:
                pass
            else:
                return transformer.transform()

        return node

    def _transform_nested_nodes_of(self, node):
        super(MambaSyntaxToClassBasedSyntax, self).generic_visit(node)


class HookDeclarationToMethodDeclaration(object):
    def __init__(self, with_statement):
        self._hook_declaration = HookDeclaration(with_statement)

    def transform(self):
        return MethodDeclaration(
            self._compute_name_of_method(),
            self._hook_declaration.body
        ).toAst()

    def _compute_name_of_method(self):
        return self._hook_declaration.run_order + '_' + self._hook_declaration.scope


class ExampleDeclarationToMethodDeclaration(object):
    def __init__(self, with_statement):
        self._example_declaration = ExampleDeclaration(with_statement)

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
        return '{0:08d}'.format(NumberOfExamplesOrExampleGroupsTransformed.get_next())


class NumberOfExamplesOrExampleGroupsTransformed(object):
    _current_number = 0

    @staticmethod
    def get_next():
        next_number = NumberOfExamplesOrExampleGroupsTransformed._current_number
        NumberOfExamplesOrExampleGroupsTransformed._current_number += 1

        return next_number


class ExampleGroupDeclarationToClassDeclaration(object):
    _ACTIVE_EXAMPlE_GROUP_MARKER = 'description'
    _PENDING_EXAMPLE_GROUP_MARKER = 'pending__' + _ACTIVE_EXAMPlE_GROUP_MARKER

    _NAME_OF_CLASS_VARIABLE_HOLDING_SUBJECT_CLASS = '_subject_class'

    def __init__(self, with_statement):
        self._example_group_declaration = ExampleGroupDeclaration(with_statement)

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
        return '{0:08d}'.format(NumberOfExamplesOrExampleGroupsTransformed.get_next())

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
