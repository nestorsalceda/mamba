import ast


def add_attribute_decorator(attr, value):
    def wrapper(function_or_class):
        setattr(function_or_class, attr, value)
        return function_or_class
    return wrapper


class TransformToSpecsNodeTransformer(ast.NodeTransformer):
    PENDING_EXAMPLE_GROUPS = ('_description', '_context', '_describe')
    FOCUSED_EXAMPLE_GROUPS = ('fdescription', 'fcontext', 'fdescribe')
    EXAMPLE_GROUPS = ('description', 'context', 'describe') + PENDING_EXAMPLE_GROUPS + FOCUSED_EXAMPLE_GROUPS
    FOCUSED_EXAMPLE = ('fit', )
    PENDING_EXAMPLE = ('_it', )
    EXAMPLES = ('it',) + PENDING_EXAMPLE + FOCUSED_EXAMPLE
    FOCUSED = FOCUSED_EXAMPLE_GROUPS + FOCUSED_EXAMPLE
    HOOKS = ('before', 'after')

    sequence = 1

    def visit_Module(self, node):
        self.has_focused_examples = False

        super(TransformToSpecsNodeTransformer, self).generic_visit(node)

        node.body.insert(0, ast.ImportFrom(module='mamba.nodetransformers', names=[ast.alias(name='add_attribute_decorator')]))
        node.body.append(ast.Assign(
            targets=[ast.Name(id='__mamba_has_focused_examples', ctx=ast.Store())],
            value=ast.Name(id=str(self.has_focused_examples), ctx=ast.Load())),
        )

        return node

    def visit_With(self, node):
        super(TransformToSpecsNodeTransformer, self).generic_visit(node)

        name = self._get_name(node)

        if name in self.FOCUSED:
            self.has_focused_examples = True

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
                decorator_list=[
                    self._set_attribute('_example_group', True),
                    self._set_attribute('_tags', self._tags_from(self._context_expr_for(node), name)),
                    self._set_attribute('_pending', name in self.PENDING_EXAMPLE_GROUPS)
                ]
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

        description_name = '{0:08d}__{1}'.format(
            self.sequence,
            description_name,
        )

        self.sequence += 1

        return description_name

    def _tags_from(self, context_expr, method_name):
        tags = []
        if method_name in self.FOCUSED:
            tags.append('focus')
        if len(context_expr.args) > 1:
            tags.extend([arg.s for arg in context_expr.args[1:]])

        return ','.join(tags)

    def _transform_to_example(self, node, name):
        context_expr = self._context_expr_for(node)

        example_name = '{0:08d}__{1} {2}'.format(
            self.sequence,
            name,
            context_expr.args[0].s
        )
        self.sequence += 1

        return ast.copy_location(
            ast.FunctionDef(
                name=example_name,
                args=self._generate_argument('self'),
                body=node.body,
                decorator_list=[
                    self._set_attribute('_example', True),
                    self._set_attribute('_tags', self._tags_from(context_expr, name)),
                    self._set_attribute('_pending', name in self.PENDING_EXAMPLE)
                ]
            ),
            node
        )

    def _generate_argument(self, name):
        return ast.arguments(args=[ast.Name(id=name, ctx=ast.Param())], vararg=None, kwarg=None, defaults=[])

    def _transform_to_hook(self, node, name):
        when = self._context_expr_for(node).attr
        return ast.copy_location(
            ast.FunctionDef(
                name=name + '_' + when,
                args=self._generate_argument('self'),
                body=node.body,
                decorator_list=[]
            ),
            node
        )

    def _set_attribute(self, attr, value):
        if isinstance(value, bool):
            val = ast.NameConstant(value=value is True)
        else:
            val = ast.Str(str(value))

        return ast.Call(
            func=ast.Name(id='add_attribute_decorator', ctx=ast.Load()),
            args=[ast.Str(attr), val],
            keywords=[]
        )



class TransformToSpecsPython3NodeTransformer(TransformToSpecsNodeTransformer):

    def _context_expr_for(self, node):
        return node.items[0].context_expr

    def _generate_argument(self, name):
        return ast.arguments(
            args=[ast.arg(arg=name, annotation=None)],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[]
        )
