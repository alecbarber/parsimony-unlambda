from tm.unlambda import run_unlambda

def test_unlambda_execution(program, expected, direction = 'both'):
    def _unlambda_test_wrapper_ltr(prog):
        return run_unlambda(prog, quiet=True, direction='ltr')
    
    def _unlambda_test_wrapper_rtl(prog):
        return run_unlambda(prog, quiet=True, direction='rtl')
    
    passed = True

    if direction in ['both', 'ltr']:
        print("Testing program " + program + " LTR ... ", end='')
        result = _unlambda_test_wrapper_ltr(program)
        this_passed = result == expected
        print("PASSED" if this_passed else f"FAILED; expected {expected}, got {result}")
        passed = this_passed and passed
    if direction in ['both', 'rtl']:
        print("Testing program " + program + " RTL ... ", end='')
        result = _unlambda_test_wrapper_rtl(program)
        this_passed = result == expected
        print("PASSED" if this_passed else "FAILED; expected {expected}, got {result}")
        passed = this_passed and passed
    
    return passed


def run_tests():
    test_unlambda_execution('`is', 's')
    test_unlambda_execution('``kis', 'i')
    test_unlambda_execution('```skis', 's')