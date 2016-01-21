import ast

from ..infrastructure import is_python3


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
        if not self._is_string(self._right_hand_side):
            return self._right_hand_side
        return ast.Name(id=self._right_hand_side, ctx=ast.Load())

    if is_python3():
        def _is_string(self, value):
            return isinstance(value, str)
    else:
        def _is_string(self, value):
            return isinstance(value, basestring)
