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
        return 'filter-predicate-list(%s)' % members

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

        if self.has_type():
            if self.has_same_type(child):
                self.add_child(child)

            else:
                raise ast.error.IncompatibleTypesError(self, child.get_type(), self.get_type())

        else:
            self.set_type(child.get_type())
            self.add_child(child)

    def add_range(self, child: ast.range.Range) -> None:
        assert isinstance(child, ast.range.Range)

        if self.has_type():
            if self.has_same_type(child):
                self.add_child(child)

            else:
                raise ast.error.IncompatibleTypesError(self, child.get_type(), self.get_type())

        else:
            self.set_type(child.get_type())
            self.add_child(child)


class Filter(ast.mixins.node.Node, ast.mixins.typed.Typed):
    DENY = 'deny'
    ALLOW = 'allow'

    def __init__(self):
        super().__init__()

        self._allow: bool or None = None
        self._predicate_list: FilterPredicateList or None = None

    def __str__(self) -> str:
        if not self._allow:
            allow = Filter.DENY
        else:
            allow = Filter.ALLOW

        children = str(self.get_children())

        return 'filter(%s, %s)' % (allow, children)

    def __contains__(self, value) -> bool:
        for child in self.get_children():
            if value not in child:
                return False

        return True

    def get_allow(self) -> bool:
        return self._allow

    def set_allow(self, allow: bool) -> None:
        self._allow = allow

    def set_predicate_list(self, child: FilterPredicateList) -> None:
        assert self._predicate_list is None

        if self.has_type():
            if self.has_same_type(child):
                self._predicate_list = child
                self.add_child(child)

            else:
                raise ast.error.IncompatibleTypesError(self, child.get_type(), self.get_type())

        else:
            self.set_type(child.get_type())
            self._predicate_list = child
            self.add_child(child)
