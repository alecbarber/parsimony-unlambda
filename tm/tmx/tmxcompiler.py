from . tmxparser import TmxParser
from tm.tm import Machine, State
import sys

class CompileException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TmxCompiler:

    def __init__(self):
        self.parser = TmxParser()
    
    def compile(self, tmx):
        parser_result = self.parser.parseString(tmx, parseAll=True).asDict()

        self.synthetic_state_count = 0
        self.alphabet = ''.join(parser_result['alphabet'])
        
        if not self.alphabet:
            raise CompileException("Alphabet cannot be empty")

        self.states = {}

        for state in parser_result['states']:
            compiled_states = self._compile_state(state)
            # print(f"Compiled state {state['expr']['name']} to {len(compiled_states)} states")
            for comp_state in compiled_states:
                if comp_state.stateName in self.states:
                    raise CompileException(f"State name '{comp_state.stateName}' is used twice")
                self.states[comp_state.stateName] = comp_state
        
        if 'START' not in self.states:
            raise CompileException("No START state found")

        return Machine.createFromRawStates(self.alphabet, sorted(self.states.values(), key=lambda x: x.stateName == 'START', reverse=True))
    
    def compileFile(self, tmxfile):

        with open(tmxfile, 'r') as infile:
            return self.compile(infile.read())
    
    """
    def compileToExecutable(self, tmx):
        self.compile(tmx)

        self.states.update({
            "ACCEPT": State("ACCEPT", self.alphabet),
            "REJECT": State("REJECT", self.alphabet),
            "ERROR": State("ERROR", self.alphabet),
            "HALT": State("HALT", self.alphabet),
            "OUT": State("OUT", self.alphabet)
        })

        self._match_states(self.states)

        result_states = sorted(self.states.values(), key=lambda x: x.stateName == "START", reverse=True)

        return self.alphabet, result_states
    
    def compileFileToExecutable(self, tmxfile):
        with open(tmxfile, 'r') as infile:
            return self.compileToExecutable(infile.read())

    def _match_states(self, state_dict):
        for s in state_dict.values():
            for c in self.alphabet:
                if not isinstance(s.getNextState(c), State):
                    try:
                        s.setNextState(c, state_dict[s.getNextState(c)])
                    except KeyError:
                        raise CompileException(f"Unknown state '{s.getNextState(c)}' referenced in state '{s.stateName}'")
    """

    def _expand_jump_targets(self, parsed_state):
        result = []
        if isinstance(parsed_state, list):
            for s in parsed_state:
                result += self._expand_jump_targets(s)
        elif isinstance(parsed_state, dict):
            if 'match_targets' in parsed_state:
                result += self._expand_jump_targets(parsed_state['match_targets'])
            if 'jump_target' in parsed_state:
                result += self._expand_jump_targets(parsed_state['jump_target'])
                if isinstance(parsed_state['jump_target'], dict):
                    new_name = f'SYNTHETIC_{self.synthetic_state_count}_{parsed_state["jump_target"]["type"]}'
                    parsed_state['jump_target']['name'] = new_name
                    self.synthetic_state_count += 1
                    result.append(parsed_state['jump_target'])
                    parsed_state['jump_target'] = new_name
        return result

    def _compile_single_state(self, state):
        
        def _opposite_direction(direction):
            return 'L' if direction == 'R' else 'R'

        def _compile_copy(state):
            def _copy_state_name(sym):
                return state['name'] + '_COPY_' + sym

            wind_state_code = {
                'name': state['name'] + '_INTERNAL_wind2' + state['start'],
                'type': 'wind2',
                'direction': 'L',
                'stop': state['start'],
                'jump_target': state['name']
            }
            shuffle_state_code = {
                'name': state['name'] + '_INTERNAL_shuffle' + state['target'],
                'type': 'shuffle',
                'direction': 'R',
                'stop': self.alphabet[0],
                'write': state['target'],
                'jump_target': wind_state_code['name']
            }

            wind_state = _compile_wind(wind_state_code, reverse=True)
            shuffle_state = _compile_shuffle(shuffle_state_code)

            start_state = State(state['name'], self.alphabet, state['direction'])
            for sym in self.alphabet:
                if sym == state['stop']:
                    start_state.setNextState(sym, state['jump_target'])
                else:
                    start_state.setNextState(sym, _copy_state_name(sym))
                    start_state.setWrite(sym, state['start'])
            
            copy_states = []
            for sym in self.alphabet:
                if not sym == state['stop']:
                    s = State(_copy_state_name(sym), self.alphabet, state['direction'])
                    s.setWrite(state['start'], sym)
                    s.setWrite(state['target'], sym)
                    s.setHeadMove(state['target'], _opposite_direction(state['direction']))
                    s.setNextState(state['target'], shuffle_state_code['name'])
                    copy_states.append(s)
            
            return [start_state] + wind_state + shuffle_state + copy_states

        def _compile_match(state):
            def _state_name(prefix):
                return state['name'] if not prefix else state['name'] + '_MATCH_' + prefix

            results = {}

            match_targets = state['match_targets'] if 'match_targets' in state and state['match_targets'] else []
            match_once_only = 'jump_target' in state and state['jump_target']
            jump_target = (state['jump_target'] if match_once_only else
                state['name'] if match_targets else
                'ERROR')

            if state['direction'] == 'L':
                for match in match_targets:
                    match['match_string'] = match['match_string'][::-1]

            results[''] = State(state['name'], self.alphabet, state['direction'], jump_target)

            match_dict = dict((match['match_string'], match) for match in match_targets)
            prefixes = {s[:i] for s in match_dict for i in range(len(s))}

            for prefix in prefixes:
                if prefix:
                    results[prefix] = State(_state_name(prefix), self.alphabet, state['direction'], jump_target)
            
            # Build match graph. Note that the behaviour is undefined for ambiguous match sets.
            for prefix in prefixes:
                last_subprefix_start = 0 if match_once_only else len(prefix)
                for subprefix_start in reversed(range(last_subprefix_start + 1)):
                    for s in self.alphabet:
                        possible_match = prefix[subprefix_start:] + s
                        if possible_match in prefixes:
                            results[prefix].setNextState(s, results[possible_match])
                            results[prefix].setWrite(s, s)
                        elif possible_match in match_dict:
                            match = match_dict[possible_match]
                            results[prefix].setNextState(s, match['jump_target'] if 'jump_target' in match else jump_target)
                            if 'write' in match:
                                results[prefix].setWrite(s, match['write'])
                            if match['direction'] == '-<':
                                results[prefix].setHeadMove(s, _opposite_direction(state['direction']))
            
            return list(results.values())
    
        def _compile_shuffle(state, reverse=False):
            def _get_name_for_sym(sym):
                write_sym = state['write'] if 'write' in state else self.alphabet[0]
                return state['name'] + ('' if sym == write_sym else f'_SHUFFLE_{sym}')
            
            result = []

            for c in self.alphabet:
                s = State(_get_name_for_sym(c), self.alphabet, defaultdirection=state['direction'])
                for nxt in self.alphabet:
                    s.setWrite(nxt, c)
                    if nxt == state['stop']:
                        s.setNextState(nxt, state['jump_target'])
                        if reverse:
                            s.setHeadMove(nxt, _opposite_direction(state['direction']))
                    else:
                        s.setNextState(nxt, _get_name_for_sym(nxt))
                result.append(s)
            
            return result
        
        def _compile_fill(state, reverse=False):
            result = _compile_wind(state, reverse=reverse)
            for c in self.alphabet:
                result[0].setWrite(c, state['write'])
            return result
        
        def _compile_write(state, reverse=False):
            result = []
            write_string = state['write'] if state['direction'] == 'R' else state['write'][::-1]
            for i in range(len(write_string)):
                name = state['name'] + (f'_WRITE_{i}' if i else '')
                next_state = (state['name'] + f'_WRITE_{i+1}') if i < len(write_string) - 1 else state['jump_target']
                result.append(State(name, self.alphabet, defaultdirection=state['direction'], defaultstate=next_state))
                for c in self.alphabet:
                    result[-1].setWrite(c, write_string[i])
            if reverse:
                for c in self.alphabet:
                    result[-1].setHeadMove(c, _opposite_direction(state['direction']))
            return result
        
        def _compile_wind(state, reverse=False):
            s = State(state['name'], self.alphabet, state['direction'])
            s.setNextState(state['stop'], state['jump_target'])
            if reverse:
                s.setHeadMove(state['stop'], _opposite_direction(state['direction']))
            return [s]
        
        def _compile_step(state):
            return [State(state['name'], self.alphabet, defaultdirection=state['direction'], defaultstate=state['jump_target'])]
        
        FUNCTION_MAP = {
            'match': _compile_match,
            'shuffle': _compile_shuffle,
            'fill': _compile_fill,
            'write': _compile_write,
            'wind': _compile_wind,
            'step': _compile_step,
            'copy': _compile_copy
        }

        if state['type'].endswith('2'):
            state_type = state['type'][:-1]
            results = FUNCTION_MAP[state_type](state, reverse=True)
        else:
            results = FUNCTION_MAP[state['type']](state)

        return results

    def _compile_state(self, parsed_state):
        if 'expr' in parsed_state:
            parsed_state['expr']['name'] = parsed_state['name']
            parsed_state = parsed_state['expr']
        
        synthetic_states_uncompiled = self._expand_jump_targets(parsed_state)

        result = self._compile_single_state(parsed_state)
        for synth in synthetic_states_uncompiled:
            result += self._compile_single_state(synth)
        
        return result