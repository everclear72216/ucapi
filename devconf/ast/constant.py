import ast.error
import ast.value

import ast.mixins.node
import ast.mixins.typed
import ast.mixins.named
import ast.mixins.expression


class Constant(ast.mixins.expression.RValueExpression, ast.mixins.named.Named):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return '%s = %s' % (self.get_name(), str(self.get_value()))

    def set_value(self, value: ast.value.Value):
        assert isinstance(value, ast.value.Value)

        self.set_type(value.get_type())
        super().set_value(value)


class ConstantList(ast.mixins.node.Node, ast.mixins.typed.Typed):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'const {%s};' % ', '.join(str(x) for x in self.get_children())

    def add_constant(self, constant: Constant):
        self.add_child(constant)

    def check(self):
        super().check()

        for child in self.get_children():
            if self.has_type():
                if not self.has_same_type(child):
                    raise ast.error.IncompatibleTypesError(self, child, self)
            else:
                self.set_type(child.get_type())

    def get_constant(self, name: str):
        return next((c for c in self.get_children() if c.get_name() == name), None)
