import ast.value
import ast.error

import ast.mixins.node
import ast.mixins.typed

import ast.types.groups


class RangeLimit(ast.mixins.node.Node, ast.value.Value):
    def __init__(self):
        super().__init__()

    def __contains__(self, value: ast.value.Value):
        return False


class RangeUpperLimit(RangeLimit):
    def __init__(self):
        super().__init__()

    def __contains__(self, value: ast.value.Value) -> bool:
        assert isinstance(value, ast.value.Value)
        return self.get_value() <= value.get_value()


class RangeLowerLimit(RangeLimit):
    def __init__(self):
        super().__init__()

    def __contains__(self, value: ast.value.Value) -> bool:
        assert isinstance(value, ast.value.Value)
        return self.get_value() >= value.get_value()


class Range(ast.mixins.node.Node, ast.mixins.typed.Typed):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        (start, end) = ('', '')

        for child in self.get_children():
            if isinstance(child, RangeUpperLimit):
                end = str(child)
            elif isinstance(child, RangeLowerLimit):
                start = str(child)

        return '[%s .. %s]' % (start, end)

    def __contains__(self, value: ast.value.Value) -> bool:
        for child in self.get_children():
            if value not in child:
                return False

        return True

    def set_end(self, value: RangeUpperLimit) -> None:
        assert None is next([x for x in self.get_children() if isinstance(x, RangeUpperLimit)], None)
        assert isinstance(value, RangeUpperLimit)

        self.add_child(value)

    def get_end(self) -> RangeUpperLimit:
        end = next([x for x in self.get_children() if isinstance(x, RangeUpperLimit)], None)
        assert end is not None

        return end

    def set_start(self, value: RangeLowerLimit) -> None:
        assert None is next([x for x in self.get_children() if isinstance(x, RangeLowerLimit)], None)
        assert isinstance(value, RangeLowerLimit)

        self.add_child(value)

    def get_start(self) -> RangeLowerLimit:
        end = next([x for x in self.get_children() if isinstance(x, RangeLowerLimit)], None)
        assert end is not None

        return end

    def check(self):
        super().check()

        for child in self.get_children():
            if self.has_type():
                if not self.has_same_type(child):
                    raise ast.error.IncompatibleTypesError(self, child, self)
            else:
                self.set_type(child.get_type())
