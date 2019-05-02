import ply.lex

ID = r'([_a-zA-Z]([_a-zA-Z0-9]*))'
float_literal = r'((-?)(([0-9]*(\.[0-9]+))|(\.[0-9]+))([eE]-?[0-9]+)?)'
string_literal = r'\"([^\\\n]|(\\.))*?\"'
integer_literal = r'((0[xX][0-9a-fA-F]*)|(0[oO][0-7]*)|(-?[1-9][0-9]*))|0'


class Lexer(object):
    tokens = [
        'KW_INT',
        'KW_MAP',
        'KW_BOOL',
        'KW_DENY',
        'KW_TRUE',
        'KW_FALSE',
        'KW_FLOAT',
        'KW_ALLOW',
        'KW_CONST',
        'KW_STRUCT',
        'KW_STRING',
        'KW_DEFAULT',
        'KW_NAMESPACE',

        'DIR_LINE',

        'ID',
        'EOS',
        'LCURLY',
        'RCURLY',
        'LSQUARE',
        'RSQUARE',
        'FLOAT_LITERAL',
        'STRING_LITERAL',
        'INTEGER_LITERAL',

        'OP_LIST',
        'OP_RANGE',
        'OP_ASSIGN',
        'OP_MEMBER',
        'OP_NAMESPACE',
    ]

    def __init__(self):
        self.lexer = ply.lex.lex(module=self)

    t_ignore = ' \t'

    def t_KW_INT(self, t):
        r'int'
        return t

    def t_KW_MAP(self, t):
        r'map'
        return t

    def t_KW_BOOL(self, t):
        r'bool'
        return t

    def t_KW_DENY(self, t):
        r'deny'
        return t

    def t_KW_TRUE(self, t):
        r'true'
        return t

    def t_KW_FALSE(self, t):
        r'false'
        return t

    def t_KW_FLOAT(self, t):
        r'float'
        return t

    def t_KW_ALLOW(self, t):
        r'allow'
        return t

    def t_KW_CONST(self, t):
        r'const'
        return t

    def t_KW_STRUCT(self, t):
        r'struct'
        return t

    def t_KW_STRING(self, t):
        r'string'
        return t

    def t_KW_DEFAULT(self, t):
        r'default'
        return t

    def t_KW_NAMESPACE(self, t):
        r'namespace'
        return t

    def t_DIR_LINE(self, t):
        r'\#line'
        return t;

    def t_RCURLY(self, t):
        r'\}'
        return t

    def t_LCURLY(self, t):
        r'\{'
        return t

    def t_RSQUARE(self, t):
        r'\]'
        return t

    def t_LSQUARE(self, t):
        r'\['
        return t

    @staticmethod
    @ply.lex.TOKEN(float_literal)
    def t_FLOAT_LITERAL(t):
        t.value = float(t.value)
        return t

    @ply.lex.TOKEN(string_literal)
    def t_STRING_LITERAL(self, t):
        t.value = str(t.value)
        return t

    @ply.lex.TOKEN(integer_literal)
    def t_INTEGER_LITERAL(self, t):
        t.value = int(t.value, 0)
        return t

    @ply.lex.TOKEN(ID)
    def t_ID(self, t):
        return t

    def t_OP_LIST(self, t):
        r','
        return t

    def t_OP_RANGE(self, t):
        r'\.\.'
        return t

    def t_OP_ASSIGN(self, t):
        r'='
        return t

    def t_OP_MEMBER(self, t):
        r'\.'
        return t

    def t_OP_NAMESPACE(self, t):
        r'::'
        return t

    def t_EOS(self, t):
        r';'
        return t

    def t_eof(self, t):
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print('Illegal character "%s"' % t.value[0])
        t.lexer.skip(1)
