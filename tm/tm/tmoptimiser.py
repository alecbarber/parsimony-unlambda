from .machine import Machine
from .state import State

import sys

from collections import defaultdict as dd

class TmGraph:
    def __init__(self, root, alphabet):
        self.nodes = [root]
        self.node_map = {root.stateName: 0}
        self.edges = []
        self.leaves = {0: root}
        self.alphabet = alphabet

    def immutable_repr(self):
        return tuple(self.edges) + tuple(sorted((k, v.stateName) for k, v in self.leaves.items()))
    
    def could_equal(self, other):
        return self.edges == other.edges

    def add_or_get_node(self, state):
        if state.stateName in self.node_map:
            return self.node_map[state.stateName]
        index = len(self.nodes)
        self.nodes.append(state)
        self.leaves[index] = state
        self.node_map[state.stateName] = index
        return index

    def expand_single_step(self):
        leaf_index = min((k for k, v in self.leaves.items() if not v.isSimpleState), default=None)
        if leaf_index is None:
            return False
        leaf_node = self.leaves.pop(leaf_index)
        for sym in self.alphabet:
            next_node = leaf_node.getNextState(sym)
            index = self.add_or_get_node(next_node)
            self.edges.append((leaf_index, leaf_node.getWrite(sym), leaf_node.getHeadMove(sym), index))
        return True


class TmOptimiser:
    def __init__(self):
        self.redundant_reversal_count = 0

    """
    safe: if True, then ERROR transitions are preserved. Otherwise, ERROR transitions are collapsed to save states.
    """
    def optimise(self, machine: Machine, safe=True, block_size=None):
        original_states = len(machine.states)
        while True:
            """
            machine, removed = self.remove_identical_states(machine, safe)
            if not removed:
                break
            if block_size:
                while True:
                    machine, changed = self.remove_redundant_reversals(machine, block_size)
                    machine, removed = self.remove_unreachable_states(machine)
                    if not changed and not removed:
                        break
                    machine, removed = self.remove_identical_states(machine, safe)
            """
            machine, removed = self.remove_identical_states(machine, safe)
            if not removed:
                break
            machine, removed = self.remove_single_subtree(machine)
            if not removed:
                break
        print("Collapsed", original_states, "to", len(machine.states), "states")
        return machine
    
    """
    Return a machine with all identical states removed
    """
    def remove_identical_states(self, machine: Machine, safe=True):
        """ Get a tuple representation of the state. States x and y have the same tuple representation iff they are equivalent """
        def getStateTuple(state: State):
            return tuple((nextState.stateName, write, direction) for sym in machine.alphabet for nextState, write, direction in [state.transitionFunc(sym)])
        
        """
        def tuples_match(s1, s2):
            return all(x[0] == 'ERROR' or x == y for x,y in zip(s1, s2))
        """

        # Map from state tuple -> state name
        unique_states = {}
        # Reverse map of unique_states
        unique_states_reversed = {}
        # Map from state name -> name of equivalent state
        state_equivalence_map = {}
        # Map from state name -> state object
        state_dict = dict((s.stateName, s) for s in machine.states)

        backtrace_states = dd(set)

        # Construct predecessor graph
        # If a state links to itself, it is excluded from the graph
        for state in machine.states:
            for sym in machine.alphabet:
                next_state = state.getNextState(sym)
                if not next_state.isSimpleState and next_state.stateName != state.stateName:
                    backtrace_states[next_state.stateName].add(state.stateName)

        # Start by trying to eliminate equivalent states from entire machine
        states_to_test = machine.states

        while states_to_test:
            removed_state_names = []

            # Mark non-unique states to be removed
            for state in states_to_test:
                state_tuple = getStateTuple(state)
                if state_tuple not in unique_states:
                    unique_states[state_tuple] = state.stateName
                    unique_states_reversed[state.stateName] = state_tuple
                else:
                    removed_state_names.append(state.stateName)
                state_equivalence_map[state.stateName] = unique_states[state_tuple]
            
            """
            # Remove states which are identical up to ERROR transitions
            if not safe:
                for state_tuple, name in unique_states.items():
                    has_error_transition = any(x[0] == 'ERROR' for x in state_tuple)
                    if has_error_transition:
                        for other_state in unique_states:
                            if other_state != state_tuple and tuples_match(state_tuple, other_state):
                                removed_state_names.append(name)
                                break
            """

            # Relabel predecessors of removed states
            # Note that we don't have to relabel the removed state itself!
            for removed in removed_state_names:
                target = removed
                while state_equivalence_map[target] != target:
                    target = state_equivalence_map[target]
                for prev_state_name in backtrace_states[removed]:
                    prev_state = state_dict[prev_state_name]
                    for sym in machine.alphabet:
                        if prev_state.getNextState(sym).stateName == removed:
                            prev_state.setNextState(sym, state_dict[target])

            # Rerun removal procedure on predecessors of removed states
            state_names_to_test = list(set().union(*(backtrace_states[n] for n in removed_state_names)))
            for s in state_names_to_test + removed_state_names:
                # Remove predecessors from unique states so that we can test them for uniqueness
                tup = unique_states_reversed.pop(s, None)
                if tup:
                    unique_states.pop(tup, None)
            
            # Reconstruct states to test
            states_to_test = [state_dict[s] for s in state_names_to_test]
        
        # Build a new TM using reduced states
        simplified_states = []
        for state in machine.states:
            state_tuple = getStateTuple(state)
            # Only keep states which haven't been mapped to something else
            if state_equivalence_map[state.stateName] == state.stateName:
                s = State(state.stateName, machine.alphabet)
                for sym in machine.alphabet:
                    replace_state_name = state.getNextState(sym).stateName
                    if not state.getNextState(sym).isSimpleState:
                        while state_equivalence_map[replace_state_name] != replace_state_name:
                            replace_state_name = state_equivalence_map[replace_state_name]
                    s.setNextState(sym, replace_state_name)
                    s.setWrite(sym, state.getWrite(sym))
                    s.setHeadMove(sym, state.getHeadMove(sym))
                simplified_states.append(s)
        
        print("Collapsed", len(machine.states), "states to", len(simplified_states), "states")

        return Machine.createFromRawStates(machine.alphabet, simplified_states), len(machine.states) - len(simplified_states)

    def remove_identical_subtrees(self, machine: Machine, output = sys.stdout):
        # Map from state name -> state object
        state_dict = dict((s.stateName, s) for s in machine.states)

        backtrace_states = dd(set)

        removed_states = set()

        # Construct predecessor graph
        for state in machine.states:
            for sym in machine.alphabet:
                next_state = state.getNextState(sym)
                if not next_state.isSimpleState:
                    backtrace_states[next_state.stateName].add(state.stateName)

        while True:
            possibly_equivalent_graphs = [{}]
            for state in machine.states:
                if state.stateName not in removed_states:
                    possibly_equivalent_graphs[0][state.stateName] = TmGraph(state, machine.alphabet)
            
            found_equivalence = None

            depth = 1

            while not found_equivalence and depth < len(machine.states) and possibly_equivalent_graphs:
                print(f"Partitioned into {len(possibly_equivalent_graphs)} groups", file=output)
                # Expand all of the first group of graphs by another 10 states
                for v in possibly_equivalent_graphs[0].values():
                    v.expand_single_step()
                
                # Partition the first group of graphs by possible equivalence
                partition = []
                for k, v in possibly_equivalent_graphs[0].items():
                    found = False
                    for p in partition:
                        if v.could_equal(list(p.values())[0]):
                            p[k] = v
                            found = True
                    if not found:
                        partition.append({k: v})
                
                print(f"Partitioned {len(possibly_equivalent_graphs[0])} items into {len(partition)} groups", file=output)

                # Remove singleton partitions
                partition = [x for x in partition if len(x) > 1]

                # Check first group for true equivalences
                # As soon as we find an equivalence, stop.
                for p in partition:
                    immutable_representations = {}
                    for v in p.values():
                        immutable_v = v.immutable_repr()
                        if immutable_v in immutable_representations:
                            found_equivalence = (immutable_representations[immutable_v], v)
                            print(f"Found match on {immutable_v}", file=output)
                            break
                        else:
                            immutable_representations[immutable_v] = v
                    if found_equivalence:
                        break
                
                # Update partition of possibly equivalent graphs
                possibly_equivalent_graphs = partition + possibly_equivalent_graphs[1:]

                # Update depth counter
                depth += 1

            # If we didn't find any equivalences, stop
            if not found_equivalence:
                break

            # Match equivalent nodes
            for name, index in found_equivalence[1].node_map.items():
                # Update states which point at this node
                target = found_equivalence[0].nodes[index]
                if target.stateName != name:
                    print(f"Mapped {name} to {target.stateName}", file=output)
                    removed_states.add(name)
                    for prev_state_name in backtrace_states[name]:
                        prev_state = state_dict[prev_state_name]
                        for sym in machine.alphabet:
                            if prev_state.getNextState(sym).stateName == name:
                                prev_state.setNextState(sym, target)

            print(f"Removed {len(removed_states)} states", file=output)
        
        return Machine.createFromRawStates(machine.alphabet, [x for x in machine.states if x.stateName not in removed_states and not x.isSimpleState])
    
    def remove_single_subtree(self, machine: Machine):
        # Map from state name -> state object
        state_dict = dict((s.stateName, s) for s in machine.states)

        backtrace_states = dd(set)

        removed_states = set()

        # Construct predecessor graph
        for state in machine.states:
            for sym in machine.alphabet:
                next_state = state.getNextState(sym)
                if not next_state.isSimpleState:
                    backtrace_states[next_state.stateName].add(state.stateName)

        ###
        # Eliminate a subtree
        ###

        possibly_equivalent_graphs = [{}]
        for state in machine.states:
            if state.stateName not in removed_states:
                possibly_equivalent_graphs[0][state.stateName] = TmGraph(state, machine.alphabet)
        
        found_equivalence = None
        depth = 1

        while not found_equivalence and depth < len(machine.states) and possibly_equivalent_graphs:
            # print(f"Partitioned into {len(possibly_equivalent_graphs)} groups")
            # Expand all of the first group of graphs by another 10 states
            for v in possibly_equivalent_graphs[0].values():
                v.expand_single_step()
            
            # Partition the first group of graphs by possible equivalence
            partition = []
            for k, v in possibly_equivalent_graphs[0].items():
                found = False
                for p in partition:
                    if v.could_equal(list(p.values())[0]):
                        p[k] = v
                        found = True
                if not found:
                    partition.append({k: v})

            # Remove singleton partitions
            partition = [x for x in partition if len(x) > 1]

            # Check first group for true equivalences
            # As soon as we find an equivalence, stop.
            for p in partition:
                immutable_representations = {}
                for v in p.values():
                    immutable_v = v.immutable_repr()
                    if immutable_v in immutable_representations:
                        found_equivalence = (immutable_representations[immutable_v], v)
                        print(f"Found match on {immutable_v}")
                        break
                    else:
                        immutable_representations[immutable_v] = v
                if found_equivalence:
                    break
            
            # Update partition of possibly equivalent graphs
            possibly_equivalent_graphs = partition + possibly_equivalent_graphs[1:]

            # Update depth counter
            depth += 1
        
        if not found_equivalence:
            return machine, 0
        
        # Match equivalent nodes
        for name, index in found_equivalence[1].node_map.items():
            # Update states which point at this node
            target = found_equivalence[0].nodes[index]
            if target.stateName != name:
                removed_states.add(name)
                for prev_state_name in backtrace_states[name]:
                    prev_state = state_dict[prev_state_name]
                    for sym in machine.alphabet:
                        if prev_state.getNextState(sym).stateName == name:
                            prev_state.setNextState(sym, target)

        return Machine.createFromRawStates(machine.alphabet, [x for x in machine.states if x.stateName not in removed_states and not x.isSimpleState]), len(removed_states)
    
    def remove_redundant_reversals(self, machine, block_size):
        def _get_start_tapes(depth = 0):
            if block_size <= depth:
                return ['']
            return [sym + tape for tape in _get_start_tapes(depth + 1) for sym in machine.alphabet]
        
        def _simulate_tm(state, tape, pos, max_steps):
            directions = []
            for step in range(max_steps):
                if state.isSimpleState:
                    break
                sym = tape[pos]
                tape = tape[:pos] + state.getWrite(sym) + tape[pos+1:]
                directions.append(state.getHeadMove(sym))
                if directions[-1] == 'R':
                    pos += 1
                else:
                    pos -= 1
                state = state.getNextState(sym)
                if step < max_steps - 1 and (pos not in range(len(tape))):
                    break
            return state, directions, tape, pos
        
        self.redundant_reversal_count += 1
        SUFFIX = f'_REVERSALS_ELIMINATED_{self.redundant_reversal_count}_'

        simulation_steps = (block_size - 1) * 3

        replace_root = None
        # First state in this list is the first replacement state
        replacement_states = []
        for state in machine.states:
            passed = True
            any_opposite_steps = False
            start_tapes = _get_start_tapes()
            end_map = {}
            start_direction = state.getHeadMove(machine.alphabet[0])

            for tape in start_tapes:
                simulation_result = _simulate_tm(state, tape, 0 if start_direction == 'R' else len(tape) - 1, simulation_steps)
                if simulation_result is None:
                    passed = False
                    break
                end_state, directions, end_tape, final_pos = simulation_result
                VALID_FINAL_POSITIONS = [len(tape) - 2, len(tape)] if start_direction == 'R' else [-1, 1]
                if not end_state.isSimpleState and final_pos in VALID_FINAL_POSITIONS:
                    passed = False
                    break
                if ('L' if start_direction == 'R' else 'R') in directions:
                    any_opposite_steps = True
                end_map[tape] = (end_state.isSimpleState, end_state.stateName, end_tape)
            if not any_opposite_steps:
                passed = False
            if not passed:
                continue

            # Generate write transitions for each matched prefix
            prefix_write_map = {}
            for tape, (is_simple, _, target_tape) in end_map.items():
                for i in range(len(tape)):
                    matched_prefix = tape[:i+1]
                    if matched_prefix not in prefix_write_map:
                        prefix_write_map[matched_prefix] = (is_simple, target_tape[i])
                    else:
                        can_replace, current_write = prefix_write_map[matched_prefix]
                        if current_write != target_tape[i]:
                            if not is_simple and not can_replace:
                                passed = False
                                break
                            elif not is_simple:
                                prefix_write_map[matched_prefix] = (False, target_tape[i])
                if not passed:
                    break
            if not passed:
                continue

            # Generate new states
            replace_root = state.stateName
            root_name = state.stateName + SUFFIX
            new_state_map = {}
            for match_prefix, (_, write_char) in prefix_write_map.items():
                state_prefix = match_prefix[:-1]
                match_sym = match_prefix[-1]
                if state_prefix in new_state_map:
                    new_state = new_state_map[state_prefix]
                else:
                    new_state = State(root_name + state_prefix, machine.alphabet, defaultdirection=start_direction)
                    new_state_map[state_prefix] = new_state
                new_state.setWrite(match_sym, write_char)
                if match_prefix in end_map:
                    _, next_state, _ = end_map[match_prefix]
                    new_state.setNextState(match_sym, next_state if next_state != replace_root else root_name)
                else:
                    new_state.setNextState(match_sym, root_name + match_prefix)
            replacement_states = [v for _, v in sorted(new_state_map.items())]
            break

        if replace_root is not None:
            for state in machine.states:
                for sym in machine.alphabet:
                    if state.getNextState(sym).stateName == replace_root:
                        state.setNextState(sym, replacement_states[0].stateName)
                    else:
                        state.setNextState(sym, state.getNextState(sym).stateName)
            print("Removed redundant reversal starting from", replace_root)
            if replace_root == machine.states[0].stateName:
                return Machine.createFromRawStates(machine.alphabet, replacement_states + machine.states), True
            else:
                return Machine.createFromRawStates(machine.alphabet, machine.states + replacement_states), True

        print("No redundant reversals")

        return machine, False
    
    def remove_unreachable_states(self, machine):
        reachable_states = set()
        state_stack = machine.states[:1]
        while state_stack:
            nxt = state_stack.pop()
            if not nxt.isSimpleState and nxt.stateName not in reachable_states:
                reachable_states.add(nxt.stateName)
                for sym in machine.alphabet:
                    state_stack.append(nxt.getNextState(sym))
        
        result = Machine.createFromRawStates(machine.alphabet, [x for x in machine.states if x.stateName in reachable_states])
        removed = len(machine.states) - len(result.states)
        print(f"Removed {removed} unreachable states")
        return result, removed
        
