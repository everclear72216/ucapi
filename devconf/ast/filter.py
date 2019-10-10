import ast.value
import ast.range
import ast.error

import ast.mixins.node
import ast.mixins.typed
import ast.mixins.expression


class FilterPredicateList(ast.mixins.node.Node, ast.mixins.typed.Typed):
    def __init__(self):
        super().__init__()

    def __str__(self):
        members = ', '.join(str(x) for x in self.get_children())
        return '%s' % members

    def __contains__(self, other: ast.value.Value):
        for child in self.get_children():
            if isinstance(child, ast.mixins.expression.LValueExpression):
                if other == child.get_value():
                    return True

            elif isinstance(child, ast.range.Range):
                if other in child:
                    return True

            else:
                raise TypeError('Argument is neither a range nor a value.')

        return False

    def add_value(self, child: ast.mixins.expression.LValueExpression) -> None:
        assert isinstance(child, ast.mixins.expression.LValueExpression)
        self.add_child(child)

    def add_range(self, child: ast.range.Range) -> None:
        assert isinstance(child, ast.range.Range)
        self.add_child(child)

    def check(self):
        super().check()

        for child in self.get_children():
            if self.has_type():
                if not self.has_same_type(child):
                    raise ast.error.IncompatibleTypesError(self, child, self)
            else:
                self.set_type(child.get_type())


class Filter(ast.mixins.node.Node, ast.mixins.typed.Typed):
    DENY = 'deny'
    ALLOW = 'allow'

    def __init__(self, allow: bool):
        super().__init__()

        self.__allow: bool = allow

    def __str__(self) -> str:
        return '%s {%s};' % (self.__allow, str(self.get_children()))

    def __contains__(self, value) -> bool:
        for child in self.get_children():
            if value not in child:
                return False

        return True

    def get_allow(self) -> bool:
        return self.__allow == Filter.ALLOW

    def set_allow(self, allow: bool) -> None:
        self.__allow = Filter.ALLOW if allow else Filter.DENY

    def set_predicate_list(self, child: FilterPredicateList) -> None:
        assert len(self.get_children()) == 0
        self.add_child(child)

    def check(self):
        super().check()

        for child in self.get_children():
            if self.has_type():
                if not self.has_same_type(child):
                    raise ast.error.IncompatibleTypesError(self, child, self)
            else:
                self.set_type(child.get_type())


class DenyFilter(Filter):
    def __init__(self):
        super().__init__(False)


class AllowFilter(Filter):
    def __init__(self):
        super().__init__(True)
