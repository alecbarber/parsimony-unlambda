import pyparsing as pp

def TmxParser():

    def MatchKeywords(keywords):
        return pp.Or(map(lambda x: pp.Keyword(x).setResultsName('type'), keywords))

    # Build grammar
    KEYWORDS_3ARG = 'step'
    KEYWORDS_4ARG_WRITE = 'write write2'
    KEYWORDS_4ARG = 'wind wind2'
    KEYWORDS_45ARG = 'shuffle shuffle2'
    KEYWORDS_5ARG = 'fill fill2'
    KEYWORDS_6ARG = 'copy'
    KEYWORD_MATCH = 'match'
    KEYWORD_ENDMATCH = 'endmatch'
    KEYWORDS = map(pp.Keyword, (' '.join([KEYWORDS_4ARG, KEYWORDS_4ARG_WRITE, KEYWORDS_45ARG, KEYWORDS_5ARG, KEYWORD_MATCH, KEYWORD_ENDMATCH])).split())
    
    RESERVED_STATES = map(pp.Keyword, 'ACCEPT ERROR HALT REJECT OUT'.split())

    COMMENT_CHAR = '%%'

    WHITESPACE = ' \t\r'

    STEP_DIRECTION = 'L R'

    pp.ParserElement.setDefaultWhitespaceChars(WHITESPACE)

    # Comments and blank lines
    whitespace = pp.White(ws=WHITESPACE).suppress()
    comment = pp.Word(COMMENT_CHAR) + pp.ZeroOrMore(pp.Word(pp.printables, excludeChars='\n'))
    newlines = pp.Group(pp.OneOrMore((comment + pp.LineEnd()) | pp.LineEnd())).setName('new line(s)').suppress()
    # State tags
    state_tag = pp.NotAny(pp.Or(KEYWORDS)) + pp.Word(pp.printables, min=2, excludeChars=':\n')
    state_tag_named = pp.NotAny(pp.Or(KEYWORDS)) + pp.Word(pp.printables, min=2, excludeChars=':\n').setResultsName('name')
    state_definition_tag = pp.NotAny(pp.Or(RESERVED_STATES)) + state_tag_named
    # Words and characters in alphabet
    language_word = pp.Word(pp.printables, excludeChars='\n')
    language_character = pp.Word(pp.printables, exact=1, excludeChars='\n')
    # Direction indicator
    direction_character = pp.oneOf(STEP_DIRECTION, asKeyword=True).setName('direction indicator').setResultsName('direction')
    # Direction arrow for match
    match_arrow = pp.oneOf('-> -<', asKeyword=True)

    # 3-argument single line commands
    single_line_command_keyword_3 = MatchKeywords(KEYWORDS_3ARG.split())

    # 4-argument single line commands
    single_line_command_keyword_4 = MatchKeywords(KEYWORDS_4ARG.split())

    # 4-argument single line commands which accept a WORD as 3rd arg
    single_line_command_keyword_4_write = MatchKeywords(KEYWORDS_4ARG_WRITE.split())

    single_line_command_keyword_45 = MatchKeywords(KEYWORDS_45ARG.split())

    # 5-argument single line commands
    single_line_command_keyword_5 = MatchKeywords(KEYWORDS_5ARG.split())

    # 6-argument single line commands
    single_line_command_keyword_6 = MatchKeywords(KEYWORDS_6ARG.split())

    jump_target = pp.Forward().setResultsName("jump_target")

    # Single line expression
    single_line_expr = pp.Group ((
        (single_line_command_keyword_3 + direction_character) |
        (single_line_command_keyword_4 + direction_character + language_character.setResultsName("stop")) | 
        (single_line_command_keyword_4_write + direction_character + language_word.setResultsName("write") + whitespace) |
        (single_line_command_keyword_45 + direction_character + language_character.setResultsName("stop") + whitespace
            + pp.Optional(language_character.setResultsName("write") + whitespace)) |
        (single_line_command_keyword_5 + direction_character + language_character.setResultsName("stop") + whitespace
            + language_character.setResultsName("write") + whitespace) |
        (single_line_command_keyword_6 + direction_character + language_character.setResultsName("start") + whitespace
            + language_character.setResultsName("target") + whitespace
            + language_character.setResultsName("stop") + whitespace)) +
        jump_target)

    jump_target << (single_line_expr | state_tag)

    match_target = pp.Group(language_word.setResultsName("match_string") + match_arrow.setResultsName("direction") + pp.Optional(language_character.setResultsName("write") + ';') + jump_target)

    match_expr = pp.Group(
        pp.Keyword(KEYWORD_MATCH).setResultsName("type") + direction_character + pp.Optional(jump_target) + newlines +
        pp.ZeroOrMore(match_target + newlines).setResultsName("match_targets") +
        pp.Keyword(KEYWORD_ENDMATCH)
    )
    
    state_definition = pp.Group((newlines + state_definition_tag.setName('state tag') + ':' + newlines + (single_line_expr.setResultsName("expr") | match_expr.setResultsName("expr")).setName('state definition'))).setName('state')

    alphabet = language_word.setName('alphabet').setResultsName("alphabet")

    document = alphabet + pp.ZeroOrMore(state_definition).setResultsName("states") + pp.ZeroOrMore(newlines)

    return document