class TmxPreprocessor:
    def process(self, parser_result):
        raise NotImplementedError

class TmxMapAlphabetPreprocessor(TmxPreprocessor):
    def __init__(self, alphabet_map):
        super().__init__()
        self.alphabet_map = alphabet_map
    
    def _expand(self, node):
        REPLACE_TAGS = ["stop", "write", "start", "target", "match_string"]
        print("Expanding", node)

        if isinstance(node, dict):
            for x in node:
                if x in REPLACE_TAGS:
                    print("Replacing", x, ":", node[x])
                    node[x] = ''.join(self.alphabet_map[c] for c in node[x])
                else:
                    self._expand(node[x])
        elif isinstance(node, list):
            for x in node:
                self._expand(x)

    def process(self, parser_result):
        parser_result['alphabet'] = ''.join(set().union(*(self.alphabet_map[x] for x in parser_result['alphabet'])))

        for state in parser_result['states']:
            self._expand(state)
        
        return parser_result