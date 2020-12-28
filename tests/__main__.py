from . unlambda import run_tests as test_unlambda
from . unx import run_tests as test_unx
from . unx import PythonBackend, TuringMachineBackend

if __name__ == '__main__':
    test_unlambda()
    
    test_unx(PythonBackend())
    test_unx(TuringMachineBackend('tm/unlambda-ltr-13.tmx'), full=False)