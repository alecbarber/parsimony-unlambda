class State:
    def __init__(self, stateName, alphabet, defaultdirection = None, defaultstate = None):
        self.stateName = stateName
        self.nextStateDict = {}
        self.headMoveDict = {}
        self.writeDict = {}

        self.alphabet = alphabet

        for symbol in self.alphabet:
            self.nextStateDict[symbol] = (defaultstate if defaultstate else self) if defaultdirection else "ERROR"
            self.headMoveDict[symbol] = defaultdirection if defaultdirection else 'R'
            self.writeDict[symbol] = symbol

        self.isStartState = False
        self.isSimpleState = False

    def setNextState(self, symbol, state):
        self.nextStateDict[symbol] = state
    
    def setHeadMove(self, symbol, move):
        self.headMoveDict[symbol] = move
    
    def setWrite(self, symbol, write):
        self.writeDict[symbol] = write

    def getNextState(self, symbol):
        return self.nextStateDict[symbol]
    
    def getHeadMove(self, symbol):
        return self.headMoveDict[symbol]
    
    def getWrite(self, symbol):
        return self.writeDict[symbol]

    def transitionFunc(self, symbol):
        return self.nextStateDict[symbol], self.writeDict[symbol], (1 if self.headMoveDict[symbol] == 'R' else -1 if self.headMoveDict[symbol] == 'L' else 0)
    
    def printState(self, output = None):
        if self.isSimpleState:
            return
        
        state_tag = ('START ' if self.isStartState else '') + self.stateName + ':'
        transitions = []
        for symbol in self.alphabet:
            nextState, write, direction = self.transitionFunc(symbol)
            transitions.append(
                '  ' +
                symbol + ' -> ' +
                (nextState.stateName if isinstance(nextState, State) else nextState) + '; ' +
                ('R' if direction > 0 else 'L' if direction < 0 else '-') + '; ' +
                write
            )
        full_desc = state_tag + '\n' + '\n'.join(transitions) + '\n'

        if output:
            output.write(full_desc)
        else:
            print(full_desc)