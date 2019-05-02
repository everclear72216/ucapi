import ast.value
import ast.error

import ast.mixins.node
import ast.mixins.typed

import ast.types.groups


class Range(ast.mixins.node.Node, ast.mixins.typed.Typed):
    def __init__(self):
        super().__init__()

        self._end = None
        self._start = None

    def __str__(self) -> str:
        if self._end is not None:
            end = 'end=%s' % str(self._end)

        else:
            end = ''

        if self._start is not None:
            start = 'start=%s' % str(self._start)

        else:
            start = ''

        dt_name = self.get_type().get_name()

        return 'range<%s>(%s, %s)' % (dt_name, start, end)

    def __contains__(self, value) -> bool:
        if self._end is not None:
            if self._end.get_value() < value.get_value():
                return False

        if self._start is not None:
            if self._start.get_value() > value.get_value():
                return False

        return True

    def set_end(self, value: ast.value.Value):
        assert isinstance(value, ast.value.Value)

        if value.get_type() not in ast.types.groups.numeric:
            raise ast.error.NonNumericRangeMember(value)

        if self._start is None:
            self.set_type(value.get_type())
            self._end = value

        elif self.has_same_type(value):
            self._end = value

        else:
            raise ast.error.IncompatibleTypesError(self, value.get_type(), self.get_type())

    def get_end(self):
        return self._end

    def set_start(self, value):
        if value.get_type() not in ast.types.groups.numeric:
            raise ast.error.NonNumericRangeMember(value)

        if self._end is None:
            self.set_type(value.get_type())
            self._start = value

        elif self.has_same_type(value):
            self._start = value

        else:
            raise ast.error.IncompatibleTypesError(self, value.get_type(), self.get_type())

    def get_start(self):
        return self._start
