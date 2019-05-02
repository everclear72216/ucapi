import ast.error
import ast.mixins.node


class TypeQualifier(ast.mixins.node.Node):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'type-qualifier'

    def set_value(self, value):
        pass


class TypeQualifierList(object):
    def __init__(self):
        self._qualifiers = []

    def add_qualifier(self, qualifier):
        self._qualifiers.append(qualifier)

    def set_value(self, value):
        for q in self._qualifiers:
            q.set_value(value)


class ConstQualifier(TypeQualifier):
    def __init__(self):
        super().__init__()

        self._assigned = False

    def __str__(self):
        return 'const-qualifier'

    def set_value(self, value):
        if self._assigned:
            raise ast.error.ConstAssignmentError(self)

        self._assigned = True
        return True
