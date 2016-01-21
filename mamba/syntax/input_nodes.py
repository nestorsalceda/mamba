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
