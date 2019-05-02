import ast.value
import ast.qualifier

import ast.mixins.node
import ast.mixins.typed
import ast.mixins.qualified


class LValueExpression(ast.mixins.node.Node, ast.mixins.typed.Typed, ast.mixins.qualified.Qualified):
    def __init__(self):
        super().__init__()

        self.__value: ast.value.Value or None = None

    def get_value(self) -> ast.value.Value:
        assert isinstance(self.__value, ast.value.Value) or self.has_default()

        if self.__value is None:
            assert self.has_default()

            value = self.get_default()
            assert isinstance(value, ast.value.Value)

            return value

        else:
            assert isinstance(self.__value, ast.value.Value)

            return self.__value

    def set_value(self, value: ast.value.Value) -> None:
        assert isinstance(value, ast.value.Value)

        if hasattr(super(), 'set_value'):
            super().set_value(value)

        self.__value = value

    def has_default(self) -> bool:
        return False

    def get_default(self) -> ast.value.Value or None:
        return None

    def evaluate(self):
        pass


class RValueExpression(LValueExpression):
    def __init__(self):
        super().__init__()

        self.add_qualifier(ast.qualifier.ConstQualifier())
