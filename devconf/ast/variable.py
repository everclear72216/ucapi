import ast.map
import ast.error
import ast.value
import ast.filter
import ast.constant

import ast.mixins.node
import ast.mixins.typed
import ast.mixins.named
import ast.mixins.expression


class DefaultValue(ast.mixins.node.Node, ast.value.Value):
    def __init__(self):
        super().__init__()


class VariableDescriptionSet(ast.mixins.node.Node, ast.mixins.typed.Typed):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return '%s' % ' '.join(str(x) for x in self.get_children())

    def check_value(self, value) -> bool:
        for child in self.get_children():
            if isinstance(child, ast.filter.DenyFilter):
                if value in child:
                    return False

            if isinstance(child, ast.filter.AllowFilter):
                if value not in child:
                    return False

        return True

    def has_default_value(self) -> bool:
        return None is not next((x for x in self.get_children() if isinstance(x, DefaultValue)), None)

    def get_default_value(self) -> ast.value.Value or None:
        return next((x for x in self.get_children() if isinstance(x, DefaultValue)), None)

    def get_mapped_value(self, key, default):
        mapping = next((x for x in self.get_children() if isinstance(x, ast.map.Map)), None)

        if mapping is None:
            return default
        else:
            return mapping.get_value(key, default)

    def set_mapping_list(self, mapping: ast.map.Map) -> None:
        assert None is next((x for x in self.get_children() if isinstance(x, ast.map.Map)), None)
        assert isinstance(mapping, ast.map.Map)

        self.add_child(mapping)

    def set_deny_filter(self, deny: ast.filter.DenyFilter) -> None:
        assert None is next((x for x in self.get_children() if isinstance(x, ast.filter.DenyFilter)), None)
        assert isinstance(deny, ast.filter.DenyFilter)

        self.add_child(deny)

    def set_allow_filter(self, allow: ast.filter.AllowFilter) -> None:
        assert None is next((x for x in self.get_children() if isinstance(x, ast.filter.AllowFilter)), None)
        assert isinstance(allow, ast.filter.AllowFilter)

        self.add_child(allow)

    def set_constant_list(self, constants: ast.constant.ConstantList) -> None:
        assert None is next((x for x in self.get_children() if isinstance(x, ast.constant.ConstantList)), None)
        assert isinstance(constants, ast.constant.ConstantList)

        self.add_child(constants)

    def set_default_value(self, default):
        assert None is next((x for x in self.get_children() if isinstance(x, DefaultValue)), None)
        assert isinstance(default, DefaultValue)

        self.add_child(default)


class Variable(ast.mixins.expression.LValueExpression, ast.mixins.named.Named):
    def __init__(self):
        super().__init__()

    def has_default(self) -> bool:
        desc = next((x for x in self.get_children() if isinstance(x, VariableDescriptionSet)), None)
        if desc is None:
            return False
        else:
            return desc.has_default_value()

    def get_default(self) -> ast.value.Value or None:
        desc = next((x for x in self.get_children() if isinstance(x, VariableDescriptionSet)), None)
        if desc is None:
            return False
        else:
            return desc.get_default_value()

    def set_value(self, value):
        if self._description is not None:
            assert self._description.check_value(value)

        if self.has_type():
            if self.has_same_type(value):
                super().set_value(value)

            else:
                raise ast.error.IncompatibleTypesError(self, value.get_type(), self.get_type())

        else:
            self.set_type(value.get_type())
            super().set_value(value)

    def set_description(self, description: VariableDescriptionSet):
        assert isinstance(description, VariableDescriptionSet)

        if self.has_type():
            if self.has_same_type(description):
                self._description = description
                self.add_child(description)

            else:
                raise ast.error.IncompatibleTypesError(self, description.get_type(), self.get_type())

        else:
            self.set_type(description.get_type())
            self._description = description
            self.add_child(description)

    def get_mapped_value(self, key, default):
        if self._description is not None:
            return self._description.get_mapped_value(key, default)

        else:
            return default
