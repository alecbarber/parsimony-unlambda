from tm import TmCreator
from tm.tm import SingleTapeTuringMachine

def run_tests():
    EXPANSION_MAP = { '_': '0000', '`': '1000', 'k': '1001', 's': '1010', 'i': '1011', '[': '1100', '^': '0100', 'K': '0101', 'S': '0110', 'I': '0111', '$': '0001', '*': '0010', '!': '0011' }

    print("Testing squares are small program...")

    machine = TmCreator('tm/unlambda-ltr-13.tmx', expansion_map=EXPANSION_MAP).createTmForUnxFile('tm/squaresaresmall.unx')
    
    runner = SingleTapeTuringMachine(machine)
    numSteps = 100000000
    while not runner.run(numSteps=numSteps, quiet=True):
        numSteps *= 10
        runner = SingleTapeTuringMachine(machine)
    
    expected = (EXPANSION_MAP['$'] + EXPANSION_MAP['i'] + EXPANSION_MAP['*']).strip('0')
    
    if runner.getTapeState() != expected:
        print(f"FAILED; expected {expected}, got {runner.getTapeState()}")
        return False
    print("PASSED")
    return True