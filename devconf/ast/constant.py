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
        return 'constant(%s = %s)' % (self.get_name(), str(self.get_value()))

    def set_value(self, value: ast.value.Value):
        assert isinstance(value, ast.value.Value)

        self.set_type(value.get_type())
        super().set_value(value)


class ConstantList(ast.mixins.node.Node, ast.mixins.typed.Typed):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'constant-list(%s)' % ', '.join(str(x) for x in self.get_children())

    def add_constant(self, constant: Constant):
        if self.has_type():
            if self.has_same_type(constant):
                self.add_child(constant)

            else:
                raise ast.error.IncompatibleTypesError(self, constant, self)

        else:
            self.set_type(constant.get_type())
            self.add_child(constant)

    def get_constant(self, name: str):
        return next((c for c in self.get_children() if c.get_name() == name), None)
