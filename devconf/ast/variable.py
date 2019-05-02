import ast.map
import ast.error
import ast.value
import ast.filter
import ast.constant

import ast.mixins.node
import ast.mixins.typed
import ast.mixins.named
import ast.mixins.expression


class VariableDescriptionSet(ast.mixins.node.Node, ast.mixins.typed.Typed):
    def __init__(self):
        super().__init__()

        self._deny_filter = None
        self._allow_filter = None
        self._mapping_list = None
        self._constant_list = None
        self._default_value = None

    def __str__(self):
        descriptors = []
        if self._deny_filter is not None:
            descriptors.append(str(self._deny_filter))

        if self._allow_filter is not None:
            descriptors.append(str(self._allow_filter))

        if self._mapping_list is not None:
            descriptors.append(str(self._mapping_list))

        if self._constant_list is not None:
            descriptors.append(str(self._constant_list))

        if self._default_value is not None:
            descriptors.append('default = %s' % str(self._default_value))

        return 'variable-description-set(%s)' % ', '.join(x for x in descriptors)

    def check_value(self, value) -> bool:
        if self._allow_filter is not None:
            if value not in self._allow_filter:
                return False

        if self._deny_filter is not None:
            if value in self._deny_filter:
                return False

        return True

    def has_default_value(self) -> bool:
        return self._default_value is not None

    def get_default_value(self) -> ast.value.Value or None:
        if self._default_value is not None:
            return self._default_value.get_value()

        else:
            return None

    def get_mapped_value(self, key, default):
        if self._mapping_list is not None:
            return self._mapping_list.get_value(key, default)

        return default

    def set_deny_filter(self, deny):
        if self._deny_filter is None:
            if self.has_type():
                if self.has_same_type(deny):
                    self._deny_filter = deny
                    self.add_child(deny)

                else:
                    args = (self, self.get_type(), deny.get_type())
                    raise ast.error.IncompatibleTypesError(*args)

            else:
                self.set_type(deny.get_type())
                self._deny_filter = deny
                self.add_child(deny)

        else:
            args = (self, 'deny', self._deny_filter, deny)
            raise ast.error.DescriptionSetError(*args)

    def set_allow_filter(self, allow):
        if self._allow_filter is None:
            if self.has_type():
                if self.has_same_type(allow):
                    self._allow_filter = allow
                    self.add_child(allow)

                else:
                    args = (self, self.get_type(), allow.get_type())
                    raise ast.error.IncompatibleTypesError(*args)

            else:
                self.set_type(allow.get_type())
                self._allow_filter = allow
                self.add_child(allow)

        else:
            args = (self, 'allow', self._allow_filter, allow)
            raise ast.error.DescriptionSetError(*args)

    def set_mapping_list(self, mapping):
        if self._mapping_list is None:
            if self.has_type():
                if self.has_same_type(mapping):
                    self._mapping_list = mapping
                    self.add_child(mapping)

                else:
                    args = (self, self.get_type(), mapping.get_type())
                    raise ast.error.IncompatibleTypesError(*args)

            else:
                self.set_type(mapping.get_type())
                self._mapping_list = mapping
                self.add_child(mapping)

        else:
            args = (self, 'map', self._mapping_list, mapping)
            raise ast.error.DescriptionSetError(*args)

    def set_constant_list(self, constants):
        if self._constant_list is None:
            if self.has_type():
                if self.has_same_type(constants):
                    self._constant_list = constants
                    self.add_child(constants)

                else:
                    args = (self, self.get_type(), constants.get_type())
                    raise ast.error.IncompatibleTypesError(*args)

            else:
                self.set_type(constants.get_type())
                self._constant_list = constants
                self.add_child(constants)

        else:
            args = (self, 'const', self._constant_list, constants)
            raise ast.error.DescriptionSetError(*args)

    def set_default_value(self, default):
        if self._default_value is None:
            if self.has_type():
                if self.has_same_type(default):
                    self._default_value = default
                    self.add_child(default)

                else:
                    args = (self, self.get_type(), default.get_type())
                    raise ast.error.IncompatibleTypesError(*args)

            else:
                self.set_type(default.get_type())
                self._default_value = default
                self.add_child(default)

        else:
            args = (self, 'default', self._default_value, default)
            raise ast.error.DescriptionSetError(*args)


class Variable(ast.mixins.expression.LValueExpression, ast.mixins.named.Named):
    def __init__(self):
        super().__init__()

        self._description = None

    def has_default(self) -> bool:
        if self._description is not None:
            return self._description.has_default_value()

        else:
            return False

    def get_default(self) -> ast.value.Value or None:
        if self._description is not None:
            return self._description.get_default_value()

        else:
            return None

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
