import collections

import ast.struct
import ast.variable
import ast.constant

import ast.mixins.node

import symbols.table


class BaseGenerator(object):
    def __init__(self, syntax_tree: ast.mixins.node.Node, symbol_table: symbols.table.SymbolTable):
        super().__init__()

        self._syntax_tree = syntax_tree
        self._symbol_table = symbol_table

    def get_syntax_tree(self) -> ast.mixins.node.Node:
        assert isinstance(self._syntax_tree, ast.mixins.node.Node)

        return self._syntax_tree

    def get_symbol_table(self) -> symbols.table.SymbolTable:
        assert isinstance(self._symbol_table, symbols.table.SymbolTable)

        return self._symbol_table

    def generate(self, filename: str) -> None:
        pass


TableElement = collections.namedtuple('TableElement', ['name', 'value'])


class MacroGenerator(BaseGenerator):
    SEPARATOR = '_'

    def __init__(self, syntax_tree: ast.mixins.node.Node, symbol_table: symbols.table.SymbolTable):
        super().__init__(syntax_tree, symbol_table)

    def _handle_constant(self, constant: ast.constant.Constant, path: str, table: list) -> None:
        assert isinstance(constant, ast.constant.Constant)
        assert isinstance(path, str)
        assert isinstance(table, list)

        p = path
        s = self.SEPARATOR
        n = constant.get_name()
        v = constant.get_value()

        table.append(TableElement('%s%s%s' % (p, s, n), v.get_value()))

    def _handle_variable(self, variable: ast.variable.Variable, path: str, table: list) -> None:
        assert isinstance(variable, ast.variable.Variable)
        assert isinstance(path, str)
        assert isinstance(table, list)

        p = path
        s = self.SEPARATOR
        n = variable.get_name()
        v = variable.get_value()
        m = variable.get_mapped_value(v, v)

        table.append(TableElement('%s%s%s%s%s' % (p, s, n, s, 'value'), v.get_value()))
        table.append(TableElement('%s%s%s' % (p, s, n), m.get_value()))

    def _iterate_structure(self, struct: ast.struct.StructInstance, path: str, table: list):
        for m in struct.get_members():
            if isinstance(m, ast.variable.Variable):
                self._handle_variable(m, path, table)

            elif isinstance(m, ast.struct.StructInstance):
                struct_path = '%s%s%s' % (path, self.SEPARATOR, m.get_name())
                self._iterate_structure(m, struct_path, table)

    def _iterate_namespace(self, root, path, table):
        for m in root.get_members():
            if isinstance(m, ast.variable.Variable):
                self._handle_variable(m, path, table)

            elif isinstance(m, ast.constant.Constant):
                self._handle_constant(m, path, table)

            elif isinstance(m, ast.struct.StructInstance):
                struct_path = '%s%s%s' % (path, self.SEPARATOR, m.get_name())
                self._iterate_structure(m, struct_path, table)

    def _iterate_namespaces(self, root, path, table):
        self._iterate_namespace(root, path, table)

        for n in root.get_namespaces():
            namespace_path = '%s%s%s' % (path, self.SEPARATOR, n.get_name())
            self._iterate_namespaces(n, namespace_path, table)

    def generate(self, filename: str) -> None:
        tab = []
        path = 'DC'
        root = self.get_symbol_table().get_root()

        self._iterate_namespaces(root, path, tab)

        with open(filename, 'wt') as outfile:
            outfile.write('\n')

            for entry in tab:
                outfile.write('#define %s %s\n' % (entry.name.upper(), str(entry.value)))
