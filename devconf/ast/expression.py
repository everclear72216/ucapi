import ast.mixins.expression


class BinaryExpression(ast.mixins.expression.RValueExpression):
    def __init__(self):
        super().__init__()

        self._performed: bool = False
        self._lhs: ast.mixins.expression.LValueExpression or None = None
        self._rhs: ast.mixins.expression.RValueExpression or None = None

    def get_lhs(self) -> ast.mixins.expression.LValueExpression:
        assert isinstance(self._lhs, ast.mixins.expression.LValueExpression)

        return self._lhs

    def set_lhs(self, lhs: ast.mixins.expression.LValueExpression) -> None:
        assert isinstance(lhs, ast.mixins.expression.LValueExpression)

        self._lhs = lhs
        self.add_child(lhs)

    def get_rhs(self) -> ast.mixins.expression.LValueExpression:
        assert isinstance(self._rhs, ast.mixins.expression.LValueExpression)

        return self._rhs

    def set_rhs(self, rhs: ast.mixins.expression.LValueExpression) -> None:
        assert isinstance(rhs, ast.mixins.expression.LValueExpression)

        self._rhs = rhs
        self.add_child(rhs)

    def get_performed(self) -> bool:
        return self._performed

    def set_performed(self) -> None:
        self._performed = True

    def evaluate(self) -> None:
        raise NotImplemented()

    def perform(self) -> None:
        raise NotImplemented()


class AssignmentExpression(BinaryExpression):
    def __init__(self):
        super().__init__()

    def evaluate(self) -> None:
        if not self.get_performed():
            self.perform()
        self.set_value(self.get_lhs().get_value())

    def perform(self) -> None:
        self.get_lhs().set_value(self.get_rhs().get_value())
        self.set_performed()
