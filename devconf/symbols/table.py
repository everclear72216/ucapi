import collections
import ast.mixins.named


class NoNamespaceError(Exception):
    pass


class UndefinedNameError(Exception):
    pass


class NameRedefinitionError(Exception):
    pass


GetSymbolResult = collections.namedtuple('GetSymbolResult', ['symbol', 'namespace'])


class Namespace(ast.mixins.named.Named):
    def __init__(self):
        super().__init__()

        self._parent: 'Namespace' or None = None

        self._members = []
        self._namespaces = []

    def __str__(self):
        members = ', '.join((x.get_name() for x in self._members))
        return 'Namespace[%s]{%s' % (self.get_name('not named yet'), members)

    def __contains__(self, name: str):
        symbol = next((x for x in self._members if x.get_name() == name), None)

        if symbol is None:
            return False

        return True

    def get_parent(self):
        return self._parent

    def set_parent(self, parent: 'Namespace'):
        self._parent = parent

    def _get_symbol(self, name: str) -> ast.mixins.named.Named or None:
        symbol = next((x for x in self._members if x.get_name() == name), None)

        if symbol is not None:
            return symbol

        if self._parent is not None:
            assert isinstance(self._parent, Namespace)

            symbol = self._parent._get_symbol(name)

            if symbol is not None:
                return symbol

            else:
                return None

        else:
            return None

    def get_symbol(self, name: str) -> ast.mixins.named.Named:
        symbol = self._get_symbol(name)

        if symbol is None:
            raise UndefinedNameError()

        return symbol

    def get_members(self) -> list:
        assert isinstance(self._members, list)

        return self._members

    def add_symbol(self, symbol: ast.mixins.named.Named):
        if self._get_symbol(symbol.get_name()) is not None:
            raise NameRedefinitionError()

        self._members.append(symbol)

    def add_namespace(self, namespace: 'Namespace'):
        assert isinstance(namespace, Namespace)

        self._namespaces.append(namespace)

    def get_namespaces(self) -> list:
        assert isinstance(self._namespaces, list)

        return self._namespaces


class SymbolTable(object):
    def __init__(self):
        self._namespaces = []
        self._root: Namespace or None = None
        self._current: Namespace or None = None

    def __str__(self):
        def iterate(ns: Namespace):
            ns_self = str(ns)
            ns_members = ', '.join((iterate(x) for x in self._namespaces if x.get_parent() is ns))

            if ns_members:
                return '%s, %s}' % (ns_self, ns_members)

            else:
                return '%s}' % ns_self

        return iterate(self._root)

    def get_root(self) -> Namespace:
        assert isinstance(self._root, Namespace)

        return self._root

    def pop_namespace(self):
        if self._current is None:
            raise NoNamespaceError()

        old_current = self._current
        self._current = self._current.get_parent()

        if self._current is not None:
            self._current.add_namespace(old_current)

    def push_namespace(self):
        namespace = Namespace()
        self._namespaces.append(namespace)

        if self._root is None:
            # no namespace has been created yet
            namespace.set_name('root')

            self._root = namespace
            self._current = namespace

        else:
            namespace.set_parent(self._current)
            self._current = namespace

    def set_namespace_name(self, name: str):
        self._current.set_name(name)

    def get_symbol(self, name: str, **kwargs) -> GetSymbolResult:
        namespace = kwargs.get('start', self._current)

        assert isinstance(namespace, Namespace)

        # retrieve namespace members
        if name in namespace:
            symbol = namespace.get_symbol(name)

        else:
            symbol = None

        # retrieve namespaces
        def iterate(ns: Namespace) -> Namespace or None:
            assert isinstance(ns, Namespace) or ns is None

            if ns is None:
                return ns

            def check_namespace(_x: Namespace) -> bool:
                assert isinstance(_x, Namespace)

                match = ((_x.get_parent() == ns) and name in _x)

                if _x.has_name():
                    match = match or (_x.get_name() == name)

                return match

            x = next((x for x in self._namespaces if check_namespace(x)), None)

            if x is not None:
                return x

            return iterate(ns.get_parent())

        return GetSymbolResult(symbol, iterate(namespace))

    def add_symbol(self, symbol: ast.mixins.named.Named):
        if self._current is None:
            raise NoNamespaceError()

        self._current.add_symbol(symbol)
