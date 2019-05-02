class UnnamedError(Exception):
    pass


class RenamedError(Exception):
    pass


class Named(object):
    def __init__(self):
        super().__init__()

        self.__name: str or None = None

    def has_name(self) -> bool:
        if isinstance(self.__name, str):
            return True

        return False

    def get_name(self, *args) -> str:
        assert len(args) < 2

        if len(args) == 0:
            assert isinstance(self.__name, str)
            return str(self.__name)

        if len(args) == 1:
            if isinstance(self.__name, str):
                return str(self.__name)

            else:
                assert isinstance(args[0], str)
                return args[0]

    def set_name(self, name: str) -> None:
        assert self.__name is None

        self.__name = str(name)
