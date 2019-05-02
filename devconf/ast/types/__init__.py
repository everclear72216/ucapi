import ast.mixins.named


class Type(ast.mixins.named.Named):
    def __init__(self):
        super().__init__()

    def __eq__(self, other: 'Type'):
        if isinstance(other, Type):
            return self.get_name() == other.get_name()

        else:
            return False

    def __ne__(self, other: 'Type'):
        if isinstance(other, Type):
            return self.get_name() != other.get_name()

        else:
            return True

    def __repr__(self):
        return self.get_name()
