import ast


class TransformToSpecsNodeTransformer(ast.NodeTransformer):
    def visit_With(self, node):
        super(TransformToSpecsNodeTransformer, self).generic_visit(node)

        func = node.context_expr.func
        name = func.id

        if name in ('description', '_description', 'context', '_context'):
            description_name = self._subject(node)
            if name in ('_description', '_context'):
                description_name += '__pending'
            description_name += '__description'

            body = []
            if not isinstance(node.context_expr.args[0], ast.Str):
                body.append(ast.Assign(targets=[ast.Name(id='_subject_class', ctx=ast.Store())], value=node.context_expr.args[0]))

            body.extend(node.body)

            return ast.copy_location(ast.ClassDef(name=description_name, bases=[], body=body, decorator_list=[]), node)

        if name in ('it', '_it'):
            example = node.context_expr.args[0].s
            return ast.copy_location(ast.FunctionDef(name=name + ' ' + example, args=ast.arguments(args=[ast.Name(id='self', ctx=ast.Param())], vararg=None, kwarg=None, defaults=[]), body=node.body, decorator_list=[]), node)

        if name in ('before', 'after'):
            when = node.context_expr.args[0].s
            return ast.copy_location(ast.FunctionDef(name=name + '_' + when, args=ast.arguments(args=[ast.Name(id='self', ctx=ast.Param())], vararg=None, kwarg=None, defaults=[]), body=node.body, decorator_list=[]), node)
        return node

    def _subject(self, node):
        if isinstance(node.context_expr.args[0], ast.Str):
            return node.context_expr.args[0].s
        if isinstance(node.context_expr.args[0], ast.Attribute):
            return node.context_expr.args[0].attr
        return node.context_expr.args[0].id

