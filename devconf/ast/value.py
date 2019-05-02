import ast.types
import ast.types.builtin

import ast.mixins.typed


class Value(ast.mixins.typed.Typed):
    def __init__(self, _type):
        super().__init__()

        self._value = None
        self.set_type(_type)

    def __eq__(self, other: 'Value'):
        assert isinstance(other, Value)

        if self.get_type() != other.get_type():
            return False

        if self._value != other.get_value():
            return False

        return True

    def __str__(self):
        value = str(self._value)
        typename = self.get_type().get_name()

        return '%s(%s)' % (typename, value)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value


class FloatValue(Value):
    def __init__(self):
        super().__init__(ast.types.builtin.floating)

    def set_value(self, value):
        v = float(value)
        super().set_value(v)


class StringValue(Value):
    def __init__(self):
        super().__init__(ast.types.builtin.string)

    def set_value(self, value):
        v = str(value)
        super().set_value(v)


class BooleanValue(Value):
    def __init__(self):
        super().__init__(ast.types.builtin.boolean)

    def set_value(self, value):
        if isinstance(value, bool):
            super().set_value(value)

        else:
            raise TypeError()


class IntegerValue(Value):
    def __init__(self):
        super().__init__(ast.types.builtin.integer)

    def set_value(self, value):
        v = int(value)
        super().set_value(v)
