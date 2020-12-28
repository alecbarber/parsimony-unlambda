from . unlambda import run_tests as test_unlambda
from . unx import run_tests as test_unx
from . unx import PythonBackend, TuringMachineBackend
from . complete import run_tests as test_complete_machines

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2 or 'unl' in sys.argv:
        test_unlambda()
    
    if len(sys.argv) < 2 or 'unx' in sys.argv:
        test_unx(PythonBackend())
    
    if len(sys.argv) < 2 or 'unx-tm' in sys.argv:
        test_unx(TuringMachineBackend('tm/unlambda-ltr-13.tmx'), full=False)

    if len(sys.argv) < 2 or 'complete' in sys.argv:
        test_complete_machines()