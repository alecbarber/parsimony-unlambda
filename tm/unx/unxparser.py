import pyparsing as pp

def UnxParser():

    COMMENT_CHAR = '%%'
    WHITESPACE = ' \t\r'

    PRIMITIVES = '`ski'

    VARIABLES = pp.alphas

    VARIABLE_DECL = '^'
    VARIABLE_USE = '$'

    PURE_FUNCTION_START = '<'
    PURE_FUNCTION_END = '>'

    IMPURE_FUNCTION_START = '['
    IMPURE_FUNCTION_END = ']'

    FUNCTION_CHARS = pp.alphanums + '_'

    TYPE_CHARS = FUNCTION_CHARS
    TYPE_ARROW = '->'

    FUNCTION_DEFINITION_SEPARATOR = '::'

    INCLUDE_KEYWORD = 'include'
    INCLUDE_FILE_CHARS = pp.alphanums + '_.'

    pp.ParserElement.setDefaultWhitespaceChars(WHITESPACE)

    # Comments and blank lines
    comment = pp.Literal(COMMENT_CHAR) + pp.ZeroOrMore(pp.Word(pp.printables, excludeChars='\n'))
    newlines = pp.Group(pp.OneOrMore((comment + pp.LineEnd()) | pp.LineEnd())).setName('new line(s)').suppress()

    # Function definition
    pure_function = pp.Group(pp.Char(PURE_FUNCTION_START) + pp.Word(FUNCTION_CHARS).setResultsName('pure_function') + pp.Char(PURE_FUNCTION_END))
    impure_function = pp.Group(pp.Char(IMPURE_FUNCTION_START) + pp.Word(FUNCTION_CHARS).setResultsName('impure_function') + pp.Char(IMPURE_FUNCTION_END))

    function_sep = pp.Literal(FUNCTION_DEFINITION_SEPARATOR).suppress()
    variable_declaration = pp.Literal(VARIABLE_DECL).suppress() + pp.Char(VARIABLES)
    variable_use = pp.Literal(VARIABLE_USE).suppress() + pp.Group(pp.Char(VARIABLES).setResultsName('variable'))
    function_body = pp.ZeroOrMore(variable_declaration).setResultsName('variables') + pp.OneOrMore(pp.Group(pp.Char(PRIMITIVES).setResultsName('primitive')) | pure_function | impure_function | variable_use).setResultsName('body')
    
    type_ = pp.Word(TYPE_CHARS)
    type_arrow = pp.Literal(TYPE_ARROW).suppress()

    function_signature = (type_ + pp.ZeroOrMore(type_arrow + type_)).setResultsName('signature')

    function = pp.Group((pure_function.setResultsName('name') | impure_function.setResultsName('name')) + pp.Optional(function_sep + function_signature) + function_sep + function_body).setResultsName('function')

    # Includes
    include_file = pp.Word(INCLUDE_FILE_CHARS, asKeyword=True)
    include_statement = (pp.Keyword(INCLUDE_KEYWORD).suppress() + pp.OneOrMore(include_file)).setResultsName('includes')

    parser = pp.Optional(pp.Optional(include_statement) + newlines) + (pp.Group(function) + pp.ZeroOrMore(pp.Group(newlines + function))).setResultsName('definitions') + pp.Optional(newlines)

    return parser