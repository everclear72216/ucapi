import ast.types
import ast.error
import ast.variable

import ast.mixins.node
import ast.mixins.named
import ast.mixins.typed


class Member(ast.mixins.node.Node, ast.mixins.typed.Typed, ast.mixins.named.Named):
    def __init__(self):
        super().__init__()

        self._description: ast.variable.VariableDescriptionSet or None = None

    def set_description(self, description: ast.variable.VariableDescriptionSet):
        assert isinstance(description, ast.variable.VariableDescriptionSet)

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

    def get_description(self) -> ast.variable.VariableDescriptionSet:
        assert isinstance(self._description, ast.variable.VariableDescriptionSet)

        return self._description


class MemberList(ast.mixins.node.Node):
    def __init__(self):
        super().__init__()

    def get_members(self) -> list:
        return self.get_children()

    def add_member(self, member: Member):
        self.add_child(member)


class StructInstance(ast.mixins.node.Node, ast.mixins.typed.Typed, ast.mixins.named.Named):
    def __init__(self):
        super().__init__()

    def get_members(self) -> list:
        return self.get_children()

    def add_member_struct(self, struct: 'StructInstance') -> None:
        assert isinstance(struct, StructInstance)

        self.add_child(struct)

    def add_member_variable(self, variable: ast.variable.Variable) -> None:
        assert isinstance(variable, ast.variable.Variable)

        self.add_child(variable)

    def get_member(self, name: str) -> ast.variable.Variable or 'StructInstance':
        m = next((x for x in self.get_children() if x.get_name() == name), None)

        assert isinstance(m, ast.variable.Variable) or isinstance(m, StructInstance)

        return m


class Struct(ast.mixins.node.Node, ast.types.Type):
    def __init__(self):
        super().__init__()

        self._member_list: MemberList or None = None

    def set_members(self, member_list: MemberList):
        assert isinstance(member_list, MemberList)

        self._member_list = member_list

    def create_instance(self) -> StructInstance:
        struct = StructInstance()
        struct.set_type(self)

        if self._member_list is not None:
            assert isinstance(self._member_list, MemberList)

            for member in self._member_list.get_members():
                if isinstance(member.get_type(), Struct):
                    m = member.get_type().create_instance()
                    m.set_name(member.get_name())
                else:
                    m = ast.variable.Variable()
                    m.set_name(member.get_name())
                    m.set_type(member.get_type())
                    m.set_description(member.get_description())

                struct.add_child(m)

        return struct
