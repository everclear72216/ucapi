import ast.mixins.node


class AstError(Exception):
    def __init__(self, node, text):
        if not isinstance(node, ast.mixins.node.Node):
            raise TypeError('"node" must be of type "Node".')

        if not isinstance(text, str):
            raise TypeError('"text" must be of type "str".')

        self._text = text
        self._line = node.get_line_number()
        self._filename = node.get_file_name()
        self._column = node.get_column_number()

    def __str__(self):
        return 'Error: %s, line %d.%d : %s' % (self._filename, self._line, self._column, self._text)


class ConstAssignmentError(AstError):
    def __init__(self, node):
        text = 'Constants can be assigned to only once.'

        super().__init__(node, text)


class DescriptionSetError(AstError):
    def __init__(self, node, entry, first, second):
        if not isinstance(entry, str):
            raise TypeError('"entry" must be of type "str".')

        if not isinstance(first, ast.mixins.node.Node):
            raise TypeError('"first" must be of type "Node".')

        if not isinstance(second, ast.mixins.node.Node):
            raise TypeError('"second" must be of type "Node".')

        text = 'Multiple %s in description set: First: %s; Second: %s.' % (entry, str(first), str(second))

        super().__init__(node, text)


class IncompatibleTypesError(AstError):
    def __init__(self, node, target, source):
        text = 'Type "%s" is incompatible with type "%s".' % (str(source), str(target))

        super().__init__(node, text)


class InvalidDataType(AstError):
    pass


class UndeclaredDataType(AstError):
    pass


class IncompleteDefinition(AstError):
    pass


class NonNumericRangeMember(AstError):
    def __init__(self, node):
        text = 'Members of a range must be of a numeric type'

        super().__init__(node, text)


class RedeclarationOfDataType(AstError):
    pass
