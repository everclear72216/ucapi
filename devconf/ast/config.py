import ast.mixins.node


class Content(ast.mixins.node.Node):
    def __init__(self):
        super().__init__()


class DeviceConfiguration(ast.mixins.node.Node):
    def __init__(self):
        super().__init__()

        self._content = None

    def get_content(self) -> Content:
        assert isinstance(self._content, Content)

        return self._content

    def set_content(self, content: Content) -> None:
        assert isinstance(content, Content)

        self._content = content
        self.add_child(content)