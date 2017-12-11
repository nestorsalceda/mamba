import ast


class TransformToSpecsNodeTransformer(ast.NodeTransformer):
    PENDING_EXAMPLE_GROUPS = ('_description', '_context', '_describe')
    EXAMPLE_GROUPS = ('description', 'context', 'describe') + PENDING_EXAMPLE_GROUPS
    EXAMPLES = ('it', '_it')
    HOOKS = ('before', 'after')

    sequence = 1

    def visit_With(self, node):
        super(TransformToSpecsNodeTransformer, self).generic_visit(node)

        name = self._get_name(node)

        if name in self.EXAMPLE_GROUPS:
            return self._transform_to_example_group(node, name)
        if name in self.EXAMPLES:
            return self._transform_to_example(node, name)
        if name in self.HOOKS:
            return self._transform_to_hook(node, name)

        return node

    def _get_name(self, node):
        context_expr = self._context_expr_for(node)

        if isinstance(context_expr, ast.Call):
            if hasattr(context_expr.func, 'value'):
                return context_expr.func.value.id
            return context_expr.func.id

        if isinstance(context_expr, ast.Attribute):
            return context_expr.value.id

    def _context_expr_for(self, node):
        return node.context_expr

    def _transform_to_example_group(self, node, name):
        return ast.copy_location(
            ast.ClassDef(
                name=self._description_name(node, name),
                bases=[],
                keywords=[],
                body=node.body,
                decorator_list=[]
            ),
            node
        )

    def _description_name(self, node, name):
        context_expr = self._context_expr_for(node)
        if isinstance(context_expr.args[0], ast.Str):
            description_name = context_expr.args[0].s
        elif isinstance(context_expr.args[0], ast.Attribute):
            description_name = context_expr.args[0].attr
        else:
            description_name = context_expr.args[0].id

        if name in self.PENDING_EXAMPLE_GROUPS:
            description_name += '__pending'

        description_name = '{0:08d}__{1}--{2}__description'.format(
            self.sequence,
            description_name,
            self._tags_from(context_expr)
        )

        self.sequence += 1

        return description_name

    def _tags_from(self, context_expr):
        tags = ''
        if len(context_expr.args) > 1:
            tags = ','.join([arg.s for arg in context_expr.args[1:]])
        return tags

    def _transform_to_example(self, node, name):
        context_expr = self._context_expr_for(node)

        example_name = '{0:08d}__{1} {2}--{3}'.format(
            self.sequence,
            name,
            context_expr.args[0].s,
            self._tags_from(context_expr)
        )
        self.sequence += 1

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
        when = self._context_expr_for(node).attr
        return ast.copy_location(
            ast.FunctionDef(
                name=name + '_' + when,
                args=self._generate_self(),
                body=node.body,
                decorator_list=[]
            ),
            node
        )


class TransformToSpecsPython3NodeTransformer(TransformToSpecsNodeTransformer):

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

