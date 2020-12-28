from tm.tm import TmOptimiser, TmExpander, State, Machine
from tm.tmx import TmxCompiler
from tm.unx import UnxCompiler

class TmCreator:
    def __init__(self, intepreter_file, expansion_map = { '_': '0000', '`': '1000', 'k': '1001', 's': '1010', 'i': '1011', '[': '1100', '^': '0100', 'K': '0101', 'S': '0110', 'I': '0111', '$': '0001', '*': '0010', '!': '0011' }):
        self.interpreter = intepreter_file
        self.expansion_map = expansion_map

    def createTmForUnxFile(self, file):
        unl = UnxCompiler().compileFile(file)
        unl = '$' + unl + '*'
        interpreter = TmxCompiler().compileFile(self.interpreter)
        interpreter.states[0].stateName = 'start_interpreter'
        printer_states = [
            State(f'print_{idx}', interpreter.alphabet, defaultdirection='R', defaultstate=f'print_{idx + 1}' if idx < len(unl) - 1 else f'start_interpreter')
            for idx in range(len(unl))
        ]
        for idx in range(len(printer_states)):
            state = printer_states[idx]
            for sym in interpreter.alphabet:
                state.setWrite(sym, unl[idx])
        for state in interpreter.states:
            for sym in interpreter.alphabet:
                state.setNextState(sym, state.getNextState(sym).stateName)
        return TmOptimiser().optimise(TmExpander().expand(Machine.createFromRawStates(interpreter.alphabet, printer_states + interpreter.states), mapping=self.expansion_map))