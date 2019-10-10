import ast.types


class UndefinedTypeError(Exception):
    pass


class RedefinedTypeError(Exception):
    pass


class Typed(object):
    def __init__(self):
        super().__init__()

        self.__type = None

    def __check_type(self, other) -> bool:
        return self.__type is other

    def has_type(self) -> bool:
        return not (self.__type is None)

    def get_type(self) -> ast.types.Type:
        if self.__type is None:
            raise UndefinedTypeError()

        return self.__type

    def set_type(self, _type: ast.types.Type) -> None:
        if isinstance(self.__type, ast.types.Type):
            raise RedefinedTypeError()

        if isinstance(_type, ast.types.Type):
            self.__type = _type

        else:
            raise TypeError()

    def has_same_type(self, other: 'Typed') -> bool:
        if self.__type is None:
            raise UndefinedTypeError()

        if isinstance(other, Typed):
            return self.__check_type(other.get_type())

        raise TypeError()
