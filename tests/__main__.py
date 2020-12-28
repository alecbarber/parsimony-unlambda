from . unlambda import run_tests as test_unlambda
from . unx import run_core_tests, run_math_tests, run_program_tests
from . unx import PythonBackend, TuringMachineBackend
from . complete import run_tests as test_complete_machines

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2 or 'unl' in sys.argv:
        test_unlambda()
    
    if len(sys.argv) < 2 or 'unx' in sys.argv:
        backend = PythonBackend()
        run_core_tests(backend)
        run_math_tests(backend)
        run_program_tests(backend)
    
    if len(sys.argv) < 2 or 'unx-tm' in sys.argv:
        run_core_tests(TuringMachineBackend('tm/unlambda-ltr-13.tmx'), full=False)

    if len(sys.argv) < 2 or 'complete' in sys.argv:
        test_complete_machines()