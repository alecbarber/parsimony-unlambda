from . unlambda import test_unlambda_execution
from tm.unx import UnxCompiler

class PythonBackend:
    def test(self, program, expected):
        return test_unlambda_execution(program, expected, direction='ltr')

class TuringMachineBackend:
    def __init__(self, tmxfile):
        from tm.tmx import TmxCompiler
        self.machine = TmxCompiler().compileFile(tmxfile)
    
    def test(self, program, expected):
        from tm.tm import SingleTapeTuringMachine
        
        initial_tape = '$' + program + '*'
        print(f"Running Turing Machine with program {initial_tape} ...")
        runner = SingleTapeTuringMachine(self.machine, initialtape=initial_tape)
        steps = 10000
        while not runner.run(numSteps=steps, quiet=True):
            steps *= 10
            runner = SingleTapeTuringMachine(self.machine, initialtape=initial_tape)
        expected_tape = '$' + expected + '*'
        if runner.getTapeState() != expected_tape:
            print(f"FAILED; expected {expected_tape}, got {runner.getTapeState()}")
            return False
        print("PASSED")
        return True

def run_tests(backend, full=True):
    def create_program(main_func, core_library):
        return core_library + '\n' + '[main] :: ' + main_func + '\n'

    with open('tm/core.unx') as infile:
        core_prog = infile.read()
    
    compiler = UnxCompiler()

    PROGRAMS = [
        ('`<not><false>', 'k', False),
        ('`<not><true>', '`ki', False),
        ('``<or><true><true>', 'k', False),
        ('``<or><true><false>', 'k', False),
        ('``<or><false><true>', 'k', False),
        ('``<or><false><false>', '`ki', False),
        ('``<and><true><true>', 'k', False),
        ('``<and><true><false>', '`ki', False),
        ('``<and><false><true>', '`ki', False),
        ('``<and><false><false>', '`ki', False),
        ('`<test><0>', '`ki', False),
        ('`<test><1>', 'k', False),
        ('`<test><10>', 'k', False),
        ('``<leq><0><0>', 'k', False),
        ('``<leq><0><1>', 'k', False),
        ('``<leq><1><0>', '`ki', False),
        ('``<leq><3><6>', 'k', True),
        ('``<leq><7><2>', '`ki', True),
        ('``<lt><0><0>', '`ki', False),
        ('``<lt><0><1>', 'k', False),
        ('``<lt><1><0>', '`ki', False),
        ('``<lt><3><6>', 'k', True),
        ('``<lt><7><2>', '`ki', True),
        ('``<eq><0><0>', 'k', False),
        ('``<eq><0><1>', '`ki', False),
        ('``<eq><1><0>', '`ki', False),
        ('``<eq><3><6>', '`ki', True),
        ('``<eq><7><2>', '`ki', True),
        ('``<gt><0><0>', '`ki', False),
        ('``<gt><0><1>', '`ki', False),
        ('``<gt><1><0>', 'k', False),
        ('``<gt><3><6>', '`ki', True),
        ('``<gt><7><2>', 'k', True),
        ('``<geq><0><0>', 'k', False),
        ('``<geq><0><1>', '`ki', False),
        ('``<geq><1><0>', 'k', False),
        ('``<geq><3><6>', '`ki', True),
        ('``<geq><7><2>', 'k', True),
        # TODO: Test arithmetic functions
    ]

    for program, result, full_only in PROGRAMS:
        if full_only and not full:
            continue
        print(f"Testing program {program} ...")
        unl = compiler.compile(create_program(program, core_prog))
        if not backend.test(unl, result):
            return False
    return True
