import ast.error

import ast.mixins.node
import ast.mixins.typed


class MapEntry(ast.mixins.node.Node, ast.mixins.typed.Typed):
    def __init__(self):
        super().__init__()

        self._key = None
        self._value = None

    def __str__(self):
        return '%s = %s' % (str(self._key), str(self._value))

    def get_key(self):
        return self._key

    def set_key(self, key):
        self.set_type(key.get_type())
        self._key = key
        self.add_child(key)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        self.add_child(value)


class MapHelper(ast.mixins.node.Node, ast.mixins.typed.Typed):
    def __init__(self):
        super().__init__()


class Map(ast.mixins.node.Node, ast.mixins.typed.Typed):
    def __init__(self):
        super().__init__()
        self._helper: None or MapHelper = None

    def __str__(self):
        return 'map {%s};' % ', '.join((str(x) for x in self.get_children()))

    def _add_entry(self, entry):
        x = next((x for x in self.get_children() if x.get_key() == entry.get_key()), None)
        if x is not None:
            x.set_value(entry.get_value())
        else:
            self.add_child(entry)

    def _get_entry(self, key, default):
        def compare(x, other):
            return x.get_key().get_value() == other

        return next((x for x in self.get_children() if compare(x, key)), default)

    def add_entry(self, entry):
        if self._helper is None:
            self._helper = MapHelper()
            self._helper.set_file_name(self.get_file_name())
            self._helper.set_line_number(self.get_line_number())

        self._add_entry(entry)

    def get_entry(self, key, default):
        return self._get_entry(key, default)

    def get_value(self, key, default):
        x = self._get_entry(key, None)
        if x is None:
            return default
        else:
            var_or_const = x.get_value()
            return var_or_const.get_value()

    def check(self):
        for child in self.get_children():
            if self.has_type():
                if not self.has_same_type(child.get_key()):
                    raise ast.error.IncompatibleTypesError(self, child.get_key(), self)
                if not self._helper.has_same_type(child.get_value()):
                    raise ast.error.IncompatibleTypesError(self, child.get_value(), self)
            else:
                self.set_type(child.get_key().get_type())
                self._helper.set_type(child.get_value().get_type())
