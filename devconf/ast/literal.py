import ast.mixins.expression


class Literal(ast.mixins.expression.RValueExpression):
    def __init__(self):
        super().__init__()

    def set_value(self, value):
        self.set_type(value.get_type())
        super().set_value(value)
