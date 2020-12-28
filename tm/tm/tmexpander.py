from .state import State
from .machine import Machine

class TmExpander:

    """
    Expand a Turing machine from n-character alphabet to a 2-character machine. If the alphabet is already
    of size 2, ensures that the alphabet is "01"
    """
    def expand(self, machine: Machine, mapping = None):
        def binaryStringLen(alphabet):
            length = 1
            letters = 2
            while letters < len(alphabet):
                length += 1
                letters *= 2
            return length

        def getExpandedNameForPrefix(name, prefix):
            return name + '_EXPANDED_' + prefix if prefix else name
        
        def getStepStateNameForDepth(name, sym, depth):
            return name + '_STEP_' + sym + '_' + str(depth)
        
        def getReturnStateNameForDepth(name, sym, depth):
            return name + '_RETURN_' + sym + '_' + str(depth)

        stringLen = binaryStringLen(machine.alphabet)
        print("Bitstring length is", stringLen)
        if mapping:
            bitstrings = mapping
        else:
            bitstrings = {}
            for i in range(len(machine.alphabet)):
                bitstrings[machine.alphabet[i]] = f'{i:0{stringLen}b}'

        expanded_states = []
        for state in machine.states:
            new_state_dict = {}
            rewind_states = []
            new_state_dict[""] = State(state.stateName, "01")
            if state.isStartState:
                new_state_dict[""].isStartState = True
            if state.isSimpleState:
                new_state_dict[""].isSimpleState = True
            # Build internal state tree (v. inefficient)
            for sym in machine.alphabet:
                for depth in range(stringLen):
                    prefix = bitstrings[sym][:depth]
                    if prefix not in new_state_dict:
                        new_state_dict[prefix] = State(getExpandedNameForPrefix(state.stateName, prefix), "01", defaultdirection='R')
                    for nxt in "01":
                        new_state_dict[prefix].setNextState(nxt, getExpandedNameForPrefix(state.stateName, prefix + nxt))
            # Build leaf nodes
            for sym in machine.alphabet:
                char = bitstrings[sym][-1]
                prev_prefix = bitstrings[sym][:-1]
                nextState = state.getNextState(sym).stateName
                direction = state.getHeadMove(sym)
                write = state.getWrite(sym)
                # We write the new bitstring in reverse
                write_bitstring = bitstrings[write][::-1]
                needs_rewind = direction != 'R' or write != sym

                if not needs_rewind:
                    new_state_dict[prev_prefix].setNextState(char, nextState)
                    continue
                
                step_states = []

                # Set write and move for final bit
                new_state_dict[prev_prefix].setWrite(char, write_bitstring[0])
                new_state_dict[prev_prefix].setHeadMove(char, direction)
                # Intermediate step states
                for depth in range(1, stringLen):
                    s = State(getStepStateNameForDepth(state.stateName, sym, depth), "01", defaultdirection='L', defaultstate=getStepStateNameForDepth(state.stateName, sym, depth+1))
                    for c in "01":
                        s.setWrite(c, write_bitstring[depth])
                    step_states.append(s)
                # Set direction for final step state
                if step_states:
                    for c in "01":
                        step_states[-1].setHeadMove(c, direction)

                # Wind to the start of the next symbol
                wind_states = [State(getReturnStateNameForDepth(state.stateName, sym, depth), "01", defaultdirection=direction, defaultstate=getReturnStateNameForDepth(state.stateName, sym, depth+1)) for depth in range(1, stringLen)]

                extra_states = []

                # Link step states to wind states
                if wind_states and step_states:
                    for c in "01":
                        step_states[-1].setNextState(c, wind_states[0].stateName)
                extra_states = step_states + wind_states

                # Link prefix matching to rewinding
                if extra_states:
                    new_state_dict[prev_prefix].setNextState(char, extra_states[0].stateName)
                    new_state_dict[prev_prefix].setHeadMove(char, 'L')
                    for c in "01":
                        extra_states[-1].setNextState(c, nextState)
                else:
                    new_state_dict[prev_prefix].setNextState(char, nextState)
                rewind_states = rewind_states + extra_states
            expanded_states = expanded_states + list(map(lambda x: x[1], sorted(new_state_dict.items()))) + rewind_states


        result = Machine.createFromRawStates("01", expanded_states, ignoreErrors=True)
        print("Expanded", len(machine.states), "states to", len(expanded_states), "states.")
        print("Symbol mapping:\n\t" + '\n\t'.join(s + ' -> ' + bitstrings[s] for s in machine.alphabet))
        return result