# Turing Machine simulator based on parsimony

from . state import State

class SingleTapeTuringMachine(object):
    def __init__(self, machine, initialtape = ""):
        self.tape = Tape(None, machine.alphabet[0], initialtape)

        self.startState = machine.states[0]

    def run(self, quiet=False, limited=False, stepSkip = 10000, printStates = [], numSteps=float("Inf"), output=None):

        state = self.startState
        tape = self.tape
        symbol = tape.readSymbol()

        stepCounter = 0
        halted = False
        numSteps = int(numSteps)

        while stepCounter < numSteps:
            try:
                if not quiet and (((stepSkip and stepCounter % stepSkip == 0) or state.stateName in printStates) or (not limited)):
                    self.printTape(state, -2, tape.length() + 2, output)

                stepCounter += 1

                if state.stateName == "ERROR":
                    print("Turing machine threw error!")
                    halted = True
                    break

                if state.stateName == "ACCEPT":
                    print("Turing machine accepted after", stepCounter, "steps.")
                    print(tape.length(), "squares of memory were used.")
                    print("Final state was")
                    self.printTape(state, -2, tape.length() + 2, output)
                    halted = True
                    break

                if state.stateName == "REJECT":
                    print("Turing machine rejected after", stepCounter, "steps.")
                    print(tape.length(), "squares of memory were used.")
                    halted = True
                    break

                if state.stateName == "HALT":
                    print("Turing machine halted after", stepCounter, "steps.")
                    print(tape.length(), "squares of memory were used.")
                    halted = True
                    break

                if state.stateName == "OUT":
                    print("Turing machine execution incomplete: reached out state.")
                    print("Perhaps this Turing machine wants to be melded with another machine.")

                state, write, headmove = state.transitionFunc(symbol)
                symbol = tape.writeSymbolMoveAndRead(write, headmove)
            except Exception as e:
                print(f"Exception while in state {state.stateName}; tape position is {tape.headLoc}")
                raise e

        if not halted:
            print("Turing machine ran for", numSteps, "steps without halting.")

    def printTape(self, state, start, end, output):
        if output == None:

            print(state.stateName)

            self.tape.printTape(start, end)
#           print("--------------------------------------")
        else:
            output.write(state.stateName + "\n")

            self.tape.printTape(start, end, output)
#           output.write("--------------------------------------\n")

class Tape(object):
    # By convention the first symbol in the alphabet is the initial symbol
    def __init__(self, name, initSymbol, initTape):
        self.name = name
        self.headLoc = 0
        self.initSymbol = initSymbol
        self.initSymbolOrd = ord(initSymbol)
        self.tapePos = bytearray(initTape, encoding='utf-8')
        self.tapeNeg = bytearray()

    def length(self):
        return len(self.tapePos) + len(self.tapeNeg)

    def readSymbol(self):
        return self._readSymbol(self.headLoc)

    def readSymbolOrd(self):
        return self._readSymbolOrd(self.headLoc)

    def _readSymbol(self, pos):
        return chr(self._readSymbolOrd(pos))

    def _readSymbolOrd(self, pos):
        try:
            if pos >= 0:
                return self.tapePos[pos]
            else:
                return self.tapeNeg[~pos]
        except IndexError:
            return self.initSymbolOrd

    def writeSymbolOrd(self, ordsymbol):
        # somewhat obsfuscated code for the benefit of CPython
        headLoc = self.headLoc
        tapePos = self.tapePos
        tapeNeg = self.tapeNeg
        initSymbolOrd = self.initSymbolOrd
        if headLoc >= 0:
            while len(tapePos) <= headLoc:
                tapePos.append(initSymbolOrd)
            tapePos[headLoc] = ordsymbol
        else:
            pos = ~headLoc
            while len(tapeNeg) <= pos:
                tapeNeg.append(initSymbolOrd)
            tapeNeg[pos] = ordsymbol

    def writeSymbolMoveAndRead(self, symbol, direction):
        headLoc = self.headLoc

        ordsymbol = ord(symbol)
        # write the symbol
        self.writeSymbolOrd(ordsymbol)
        if direction != 0:
            headLoc += direction
            self.headLoc = headLoc
        return self.readSymbol()

    def printTape(self, start, end, output=None):
        out = self.getTapeOutput(start, end)
        if output == None:
            print(out, end="")
        else:
            output.write(out)

    def getTapeOutput(self, start, end):
        headString = []
        tapeString = []
        for i in range(start, end):
            if i == self.headLoc:
                headString.append("v")
            else:
                headString.append(" ")

            tapeString.append(self._readSymbol(i)[0])

        if not self.name == None:
            tapeString.append(" " + self.name)

        headString = "".join(headString)
        tapeString = "".join(tapeString)
        return headString + "\n" + tapeString + "\n"
