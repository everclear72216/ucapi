class Node(object):
    def __init__(self):
        super().__init__()

        self.__filename = ''
        self.__children = []
        self.__line_number = 0
        self.__column_number = 0

    def get_children(self) -> list:
        return self.__children

    def add_child(self, child: 'Node') -> None:
        assert isinstance(child, Node)

        self.__children.append(child)

    def get_line_number(self) -> int:
        return self.__line_number

    def set_line_number(self, n: int) -> None:
        self.__line_number = int(n)

    def get_column_number(self) -> int:
        return self.__column_number

    def set_column_number(self, n: int) -> None:
        self.__column_number = int(n)

    def get_file_name(self) -> str:
        return self.__filename

    def set_file_name(self, f: str) -> None:
        self.__filename = str(f)

    def is_leaf(self) -> bool:
        if len(self.__children) == 0:
            return True

        return False
