import ast.value
import ast.qualifier


class Qualified(object):
    def __init__(self):
        super().__init__()

        self.__qualifiers = ast.qualifier.TypeQualifierList()

    def add_qualifier(self, qualifier: ast.qualifier.TypeQualifier) -> None:
        assert isinstance(qualifier, ast.qualifier.TypeQualifier)

        self.__qualifiers.add_qualifier(qualifier)

    def set_value(self, value: ast.value.Value) -> None:
        assert isinstance(value, ast.value.Value)

        self.__qualifiers.set_value(value)

        if hasattr(super(), 'set_value'):
            super().set_value(value)
