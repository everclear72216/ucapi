import ast.map
import ast.range
import ast.value
import ast.struct
import ast.filter
import ast.config
import ast.literal
import ast.variable
import ast.constant
import ast.qualifier
import ast.namespace
import ast.expression

import ast.types
import ast.types.builtin

import ply.yacc

import parser.lexer

import symbols.table


class Parser(object):
    tokens = parser.lexer.Lexer.tokens

    precedence = (
        ('left', 'OP_ASSIGN'),
        ('left', 'OP_MEMBER'),
        ('left', 'OP_NAMESPACE'),
    )

    def __init__(self, filename):
        self._symbol_table = None
        self._filename = str(filename)
        self.lexer = parser.lexer.Lexer()
        self.parser = ply.yacc.yacc(module=self)

    def parse(self, text, **kwargs):
        self._symbol_table = symbols.table.SymbolTable()

        syntax_tree = self.parser.parse(text, **kwargs)

        return syntax_tree, self._symbol_table

    def get_file_name(self):
        return self._filename

    def p_device_configuration(self, p):
        """device-configuration : push-scope namespace-content"""

        p[0] = ast.config.DeviceConfiguration()

        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        self._symbol_table.pop_namespace()

    def p_namespace_content_1(self, p):
        """namespace-content : namespace
                             | struct-declaration
                             | struct-instantiation
                             | variable-declaration
                             | assignment-expression"""

        p[0] = ast.namespace.Content()
        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        p[0].add_child(p[1])

    @staticmethod
    def p_namespace_content_2(p):
        """namespace-content : namespace-content namespace
                             | namespace-content struct-declaration
                             | namespace-content struct-instantiation
                             | namespace-content variable-declaration
                             | namespace-content assignment-expression"""

        p[0] = p[1]
        p[0].add_child(p[2])

    def p_namespace_content_3(self, p):
        """namespace-content : line-marker"""

        p[0] = ast.namespace.Content()
        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

    @staticmethod
    def p_namespace_content_4(p):
        """namespace-content : namespace-content line-marker"""

        p[0] = p[1]

    def p_namespace(self, p):
        """namespace : KW_NAMESPACE ID LCURLY push-scope namespace-content RCURLY"""

        p[0] = ast.namespace.Namespace()
        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        p[0].set_name(p[2])
        p[0].set_content(p[5])

        self._symbol_table.set_namespace_name(p[2])
        self._symbol_table.pop_namespace()

    def p_assignment_expression(self, p):
        """assignment-expression : primary-expression OP_ASSIGN rvalue-expression EOS"""

        p[0] = ast.expression.AssignmentExpression()
        p[0].set_line_number(p.lineno(2))
        p[0].set_file_name(self._filename)

        p[0].set_lhs(p[1])
        p[0].set_rhs(p[3])

        p[0].perform()

    @staticmethod
    def p_rvalue_expression(p):
        """rvalue-expression : primary-expression"""

        p[0] = p[1]
        p[0].evaluate()

    @staticmethod
    def p_primary_expression_1(p):
        """primary-expression : literal"""

        p[0] = p[1]

    def p_primary_expression_2(self, p):
        """primary-expression : ID"""

        result = self._symbol_table.get_symbol(p[1])
        p[0] = result.symbol

    @staticmethod
    def p_primary_expression_3(p):
        """primary-expression : struct-access"""

        p[0] = p[1]

    @staticmethod
    def p_primary_expression_4(p):
        """primary-expression : namespace-access"""

        p[0] = p[1].symbol

    def p_struct_access_1(self, p):
        """struct-access : ID OP_MEMBER ID"""

        result = self._symbol_table.get_symbol(p[1])

        p[0] = result.symbol.get_member(p[3])

    @staticmethod
    def p_struct_access_2(p):
        """struct-access : namespace-access OP_MEMBER ID"""

        p[0] = p[1].symbol.get_member(p[3])

    @staticmethod
    def p_struct_access_3(p):
        """struct-access : struct-access OP_MEMBER ID"""

        p[0] = p[1].get_member(p[3])

    def p_namespace_access_1(self, p):
        """namespace-access : OP_NAMESPACE ID"""

        p[0] = self._symbol_table.get_symbol(p[2], start=self._symbol_table.get_root())

    def p_namespace_access_2(self, p):
        """namespace-access : ID OP_NAMESPACE ID"""

        result = self._symbol_table.get_symbol(p[1])
        start = result.namespace

        p[0] = self._symbol_table.get_symbol(p[3], start=start)

    def p_namespace_access_3(self, p):
        """namespace-access : namespace-access OP_NAMESPACE ID"""

        p[0] = self._symbol_table.get_symbol(p[3], start=p[1].namespace)

    def p_struct_declaration(self, p):
        """struct-declaration : KW_STRUCT ID LCURLY push-scope member-declaration-list RCURLY EOS"""

        p[0] = ast.struct.Struct()
        p[0].set_line_number(p.lineno(2))
        p[0].set_file_name(self._filename)

        p[0].set_name(p[2])
        p[0].set_members(p[5])

        self._symbol_table.set_namespace_name(p[2])
        self._symbol_table.pop_namespace()
        self._symbol_table.add_symbol(p[0])

    def p_member_declaration_list_1(self, p):
        """member-declaration-list : member-declaration"""

        p[0] = ast.struct.MemberList()
        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        p[0].add_member(p[1])

    @staticmethod
    def p_member_declaration_list_2(p):
        """member-declaration-list : member-declaration-list member-declaration"""

        p[0] = p[1]
        p[0].add_member(p[2])

    def p_struct_member_declaration(self, p):
        """member-declaration : KW_STRUCT ID ID EOS"""

        result = self._symbol_table.get_symbol(p[2])
        struct = result.symbol

        p[0] = ast.struct.Member()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].set_type(struct)
        p[0].set_name(p[3])

        self._symbol_table.add_symbol(p[0])

    def p_member_declaration_1(self, p):
        """member-declaration : type-name ID EOS"""

        p[0] = ast.struct.Member()
        p[0].set_line_number(p.lineno(2))
        p[0].set_file_name(self._filename)

        p[0].set_type(p[1])
        p[0].set_name(p[2])

        self._symbol_table.add_symbol(p[0])

    def p_member_declaration_2(self, p):
        """member-declaration : type-qualifier type-name ID EOS"""

        p[0] = ast.struct.Member()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].set_type(p[2])
        p[0].set_name(p[3])
        p[0].add_qualifier(p[1])

        self._symbol_table.add_symbol(p[0])

    def p_member_declaration_3(self, p):
        """member-declaration : type-name ID LCURLY push-scope variable-description-set RCURLY EOS"""

        p[0] = ast.struct.Member()
        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        p[0].set_type(p[1])
        p[0].set_name(p[2])
        p[0].set_description(p[5])

        self._symbol_table.set_namespace_name(p[2])
        self._symbol_table.pop_namespace()
        self._symbol_table.add_symbol(p[0])

    def p_member_declaration_4(self, p):
        """member-declaration : type-qualifier type-name ID LCURLY push-scope variable-description-set RCURLY EOS"""

        p[0] = ast.struct.Member()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].set_type(p[2])
        p[0].set_name(p[3])
        p[0].add_qualifier(p[1])
        p[0].set_description(p[6])

        self._symbol_table.set_namespace_name(p[3])
        self._symbol_table.pop_namespace()
        self._symbol_table.add_symbol(p[0])

    def p_struct_instantiation(self, p):
        """struct-instantiation : KW_STRUCT ID ID EOS"""

        result = self._symbol_table.get_symbol(p[2])
        struct = result.symbol

        p[0] = struct.create_instance()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].set_name(p[3])

        self._symbol_table.add_symbol(p[0])

    def p_variable_declaration_1(self, p):
        """variable-declaration : type-name ID EOS"""

        p[0] = ast.variable.Variable()
        p[0].set_line_number(p.lineno(2))
        p[0].set_file_name(self._filename)

        p[0].set_type(p[1])
        p[0].set_name(p[2])

        self._symbol_table.add_symbol(p[0])

    def p_variable_declaration_2(self, p):
        """variable-declaration : type-qualifier type-name ID EOS"""

        p[0] = ast.variable.Variable()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].add_qualifier(p[1])
        p[0].set_type(p[2])
        p[0].set_name(p[3])

        self._symbol_table.add_symbol(p[0])

    def p_variable_declaration_3(self, p):
        """variable-declaration : type-name ID LCURLY push-scope variable-description-set RCURLY EOS"""

        p[0] = ast.variable.Variable()
        p[0].set_line_number(p.lineno(2))
        p[0].set_file_name(self._filename)

        p[0].set_type(p[1])
        p[0].set_name(p[2])
        p[0].set_description(p[5])

        self._symbol_table.set_namespace_name(p[2])
        self._symbol_table.pop_namespace()
        self._symbol_table.add_symbol(p[0])

    def p_variable_declaration_4(self, p):
        """variable-declaration : type-qualifier type-name ID LCURLY push-scope variable-description-set RCURLY EOS"""

        p[0] = ast.variable.Variable()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].set_type(p[2])
        p[0].set_name(p[3])
        p[0].add_qualifier(p[1])
        p[0].set_description(p[6])

        self._symbol_table.set_namespace_name(p[3])
        self._symbol_table.pop_namespace()
        self._symbol_table.add_symbol(p[0])

    def p_variable_descriptions_set_1(self, p):
        """variable-description-set : filter
                                    | variable-description-set filter"""

        if len(p) == 2:
            p[0] = ast.variable.VariableDescriptionSet()
            p[0].set_line_number(p.lineno(1))
            p[0].set_file_name(self._filename)

            f = p[1]

        else:
            p[0] = p[1]

            f = p[2]

        if f.get_allow():
            p[0].set_allow_filter(f)
        else:
            p[0].set_deny_filter(f)

    def p_variable_description_set_2(self, p):
        """variable-description-set : default
                                    | variable-description-set default"""

        if len(p) == 2:
            p[0] = ast.variable.VariableDescriptionSet()
            p[0].set_line_number(p.lineno(1))
            p[0].set_file_name(self._filename)
            p[0].set_default_value(p[1])

        else:
            p[0] = p[1]
            p[0].set_default_value(p[2])

    def p_variable_description_set_3(self, p):
        """variable-description-set : mapping
                                    | variable-description-set mapping"""

        if len(p) == 2:
            p[0] = ast.variable.VariableDescriptionSet()
            p[0].set_line_number(p.lineno(1))
            p[0].set_file_name(self._filename)
            p[0].set_mapping_list(p[1])

        else:
            p[0] = p[1]
            p[0].set_mapping_list(p[2])

    def p_variable_description_set_4(self, p):
        """variable-description-set : constant
                                    | variable-description-set constant"""

        if len(p) == 2:
            p[0] = ast.variable.VariableDescriptionSet()
            p[0].set_line_number(p.lineno(1))
            p[0].set_file_name(self._filename)
            p[0].set_constant_list(p[1])

        else:
            p[0] = p[1]
            p[0].set_constant_list(p[2])

    def p_filter(self, p):
        """filter : filter-type LCURLY filter-list RCURLY EOS"""

        p[0] = ast.filter.Filter()
        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)
        p[0].set_allow(p[1])
        p[0].set_predicate_list(p[3])

    def p_filter_list_1(self, p):
        """filter-list : range"""

        p[0] = ast.filter.FilterPredicateList()

        p[0].add_range(p[1])
        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

    def p_filter_list_2(self, p):
        """filter-list : literal"""

        p[0] = ast.filter.FilterPredicateList()
        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        p[0].add_value(p[1])

    @staticmethod
    def p_filter_list_3(p):
        """filter-list : filter-list OP_LIST range"""

        p[0] = p[1]
        p[0].add_range(p[3])

    @staticmethod
    def p_filter_list_4(p):
        """filter-list : filter-list OP_LIST literal"""

        p[0] = p[1]
        p[0].add_value(p[3])

    def p_numeric_range_1(self, p):
        """range : LSQUARE OP_RANGE numeric-literal RSQUARE"""

        p[0] = ast.range.Range()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].set_end(p[3].get_value())

    def p_numeric_range_2(self, p):
        """range : LSQUARE numeric-literal OP_RANGE RSQUARE"""

        p[0] = ast.range.Range()
        p[0].set_line_number(p.lineno(2))
        p[0].set_file_name(self._filename)

        p[0].set_start(p[2].get_value())

    def p_numeric_range_3(self, p):
        """range : LSQUARE numeric-literal OP_RANGE numeric-literal RSQUARE"""

        p[0] = ast.range.Range()
        p[0].set_line_number(p.lineno(4))
        p[0].set_file_name(self._filename)

        p[0].set_end(p[4].get_value())
        p[0].set_start(p[2].get_value())

    @staticmethod
    def p_mapping(p):
        """mapping : KW_MAP LCURLY mapping-table RCURLY EOS"""

        p[0] = p[3]

    def p_mapping_table_1(self, p):
        """mapping-table : mapping-element"""

        p[0] = ast.map.Map()
        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        p[0].add_entry(p[1])

    @staticmethod
    def p_mapping_table_2(p):
        """mapping-table : mapping-table OP_LIST mapping-element"""

        p[0] = p[1]
        p[0].add_entry(p[3])

    def p_mapping_element_1(self, p):
        """mapping-element : literal OP_ASSIGN literal"""

        p[0] = ast.map.MapEntry()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].set_key(p[1])
        p[0].set_value(p[3])

    def p_mapping_element_2(self, p):
        """mapping-element : literal OP_ASSIGN ID"""

        result = self._symbol_table.get_symbol(p[3])
        value = result.symbol

        p[0] = ast.map.MapEntry()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].set_key(p[1])
        p[0].set_value(value)

    @staticmethod
    def p_constant_list(p):
        """constant : KW_CONST LCURLY constant-list RCURLY EOS"""

        p[0] = p[3]

    def p_constant_list_1(self, p):
        """constant-list : constant-element"""

        p[0] = ast.constant.ConstantList()
        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        p[0].add_constant(p[1])

    @staticmethod
    def p_constant_list_2(p):
        """constant-list : constant-list OP_LIST constant-element"""

        p[0] = p[1]
        p[0].add_constant(p[3])

    def p_constant_declaration_1(self, p):
        """constant-element : ID OP_ASSIGN literal"""

        p[0] = ast.constant.Constant()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].set_name(p[1])
        p[0].set_value(p[3].get_value())

        self._symbol_table.add_symbol(p[0])

    def p_constant_declaration_2(self, p):
        """constant-element : ID OP_ASSIGN ID"""

        result = self._symbol_table.get_symbol(p[3])
        value = result.symbol

        p[0] = ast.constant.Constant()
        p[0].set_line_number(p.lineno(3))
        p[0].set_file_name(self._filename)

        p[0].set_name(p[1])
        p[0].set_value(value.get_value())

        self._symbol_table.add_symbol(p[0])

    @staticmethod
    def p_default_value_1(p):
        """default : KW_DEFAULT OP_ASSIGN literal EOS"""

        p[0] = p[3]

    def p_default_value_2(self, p):
        """default : KW_DEFAULT OP_ASSIGN ID EOS"""

        result = self._symbol_table.get_symbol(p[3])
        p[0] = result.symbol

    @staticmethod
    def p_literal(p):
        """literal : bool-literal
                   | string-literal
                   | numeric-literal"""

        p[0] = p[1]

    @staticmethod
    def p_numeric_literal(p):
        """numeric-literal : float-literal
                           | integer-literal"""

        p[0] = p[1]

    @staticmethod
    def p_type_name_4(p):
        """type-name : KW_INT"""

        p[0] = ast.types.builtin.integer

    @staticmethod
    def p_type_name_1(p):
        """type-name : KW_BOOL"""

        p[0] = ast.types.builtin.boolean
    
    @staticmethod
    def p_type_name_2(p):
        """type-name : KW_FLOAT"""

        p[0] = ast.types.builtin.floating

    @staticmethod
    def p_type_name_3(p):
        """type-name : KW_STRING"""

        p[0] = ast.types.builtin.string

    def p_type_qualifier(self, p):
        """type-qualifier : KW_CONST"""

        p[0] = ast.qualifier.ConstQualifier()

        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

    def p_line_marker(self, p):
        """line-marker : DIR_LINE integer-literal string-literal"""

    def p_bool_literal(self, p):
        """bool-literal : KW_FALSE
                        | KW_TRUE"""

        p[0] = ast.literal.Literal()

        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        value = ast.value.BooleanValue()
        value.set_value(p[1] == 'true')

        p[0].set_value(value)

    def p_float_literal(self, p):
        """float-literal : FLOAT_LITERAL"""

        p[0] = ast.literal.Literal()

        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        value = ast.value.FloatValue()
        value.set_value(p[1])

        p[0].set_value(value)

    def p_string_literal(self, p):
        """string-literal : STRING_LITERAL"""

        p[0] = ast.literal.Literal()

        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        value = ast.value.StringValue()
        value.set_value(p[1])

        p[0].set_value(value)

    def p_integer_literal(self, p):
        """integer-literal : INTEGER_LITERAL"""

        p[0] = ast.literal.Literal()

        p[0].set_line_number(p.lineno(1))
        p[0].set_file_name(self._filename)

        value = ast.value.IntegerValue()
        value.set_value(p[1])

        p[0].set_value(value)

    @staticmethod
    def p_filter_type_deny(p):
        """filter-type : KW_DENY"""

        p[0] = False

    @staticmethod
    def p_filter_type_allow(p):
        """filter-type : KW_ALLOW"""

        p[0] = True

    def p_push_scope(self, _):
        """push-scope :"""

        self._symbol_table.push_namespace()
