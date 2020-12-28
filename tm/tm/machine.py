from .state import State
import sys

class Machine:
    def __init__(self, alphabet, states):
        self.alphabet = alphabet
        self.states = states
    
    def printMachine(self, output = sys.stdout):
        output.write(self.alphabet + '\n')
        for state in self.states:
            state.printState(output)

    """
    Parse a Turing Machine file.
    The first state in the file must be the START state.
    If alphabet is not given as an argument, it needs to be specified on the first line of the file as a list of characters

    Returns a list of states and the alphabet
    """
    @staticmethod
    def parseMachine(path, alphabet = None):
        def getStateName(line):
            colonLoc = line.find(":")

            stateName = line[:colonLoc]

            return stateName

        def getDefaultDirection(line):
            colonLoc = line.find(":")

            direction = line[(colonLoc + 1):].strip()

            return direction
        
        def getDefaultState(line):
            semisplit = line.split(';')
            if len(semisplit) == 1:
                return None
            else:
                return semisplit[1].split()[0]

        with open(path, "r") as inp:
            tmLines = inp.readlines()
            
        # Get alphabet
        if not alphabet:
            alphabet = tmLines[0][:-1]

        listOfRealStates = []

        # Parse states
        for line in tmLines[1:]:
            if line != "\n": # not a blank line
                lineSplit = line.split()

                currentStateBeingModified = listOfRealStates[-1] if listOfRealStates else None

                if lineSplit[0] == "START":
                    stateName = getStateName(line[6:])
                    defaultDirection = getDefaultDirection(line[6:])
                    defaultState = getDefaultState(line[6:])
                    startState = State(stateName, alphabet, defaultDirection, defaultState)
                    listOfRealStates.append(startState)
                    startState.isStartState = True

                elif not lineSplit[0] in alphabet:
                    stateName = getStateName(line)
                    defaultDirection = getDefaultDirection(line)
                    defaultState = getDefaultState(line)
                    state = State(stateName, alphabet, defaultDirection, defaultState)
                    listOfRealStates.append(state)

                else:
                    try:
                        symbol = lineSplit[0]
                        stateName = lineSplit[2][:-1]
                        headMove = lineSplit[3][:-1]
                        write = lineSplit[4]

                        currentStateBeingModified.setNextState(symbol, stateName)
                        currentStateBeingModified.setHeadMove(symbol, headMove)
                        currentStateBeingModified.setWrite(symbol, write)
                    except Exception as e:
                        print(f"Exception while parsing line; current state being modified is {currentStateBeingModified if not isinstance(currentStateBeingModified, State) else currentStateBeingModified.stateName}")
                        raise e
        
        return Machine.createFromRawStates(alphabet, listOfRealStates)
    
    @staticmethod
    def createFromRawStates(alphabet, states, ignoreErrors=False):
        stateDictionary = {"ACCEPT": State("ACCEPT", alphabet),
        #    "REJECT": State("REJECT", alphabet),
            "ERROR": State("ERROR", alphabet),
        #    "HALT": State("HALT", alphabet),
        #    "OUT": State("OUT", alphabet)
        }
        for s in stateDictionary.values():
            s.isSimpleState = True
        stateDictionary.update(dict((s.stateName, s) for s in states))

        # Replace state names with references
        for state in states:
            for symbol in alphabet:
                if not isinstance(state.getNextState(symbol), State):
                    try:
                        state.setNextState(symbol, stateDictionary[state.getNextState(symbol)])
                    except Exception as e:
                        if ignoreErrors:
                            state.setNextState(symbol, stateDictionary['ERROR'])
                        else:
                            print(f"Exception while expanding successor state for {state.stateName, symbol}")
                            raise e
        
        return Machine(alphabet, states)