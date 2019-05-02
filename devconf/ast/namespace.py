import ast.mixins.node
import ast.mixins.named


class Content(ast.mixins.node.Node):
    def __init__(self):
        super().__init__()


class Namespace(ast.mixins.node.Node, ast.mixins.named.Named):
    def __init__(self):
        super().__init__()

        self._content: Content or None = None

    def get_content(self) -> Content:
        assert isinstance(self._content, Content)

        return self._content

    def set_content(self, content: Content) -> None:
        assert isinstance(content, Content)

        self._content = content
        self.add_child(content)
