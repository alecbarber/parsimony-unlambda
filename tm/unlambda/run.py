def run_unlambda(unl, quiet = False, step=False, direction = 'rtl'):
    def _identity(x):
        return x

    if not quiet:
        print("Evaluating", unl)

    if direction == 'rtl':
        evaluate = evaluate_unl_rtl
    elif direction == 'ltr':
        evaluate = evaluate_unl_ltr 
    else:
        raise RuntimeError(f"Unknown evaluation direction {direction}")
    while True:
        new_unl = evaluate(unl)
        if new_unl == unl:
            return unl
        (input if step else print if not quiet else _identity)(new_unl)
        unl = new_unl


def find_block_end(unl, idx):
    counter = 1
    end = idx
    while counter:
        if unl[end] == '`':
            counter += 1
        else:
            counter -= 1
        end += 1
    return end

def evaluate_unl_rtl(unl):
    # Pad with space so code is 1-indexed
    unl = ' ' + unl

    # States for state machine
    STATE_MATCHED_NONE = 0
    STATE_MATCHED_I = 10
    STATE_MATCHED_K = 20
    STATE_MATCHED_K_TICK = 21
    STATE_MATCHED_S = 30
    STATE_MATCHED_S_TICK = 31
    STATE_MATCHED_S_TICK_TICK = 32

    # Initial state
    state = STATE_MATCHED_NONE
    idx = len(unl) - 1
    finished = False

    while idx and not finished:
        if unl[idx] == 'i':
            state = STATE_MATCHED_I
        elif unl[idx] == 'k':
            state = STATE_MATCHED_K
        elif unl[idx] == 's':
            state = STATE_MATCHED_S
        elif unl[idx] == '`':
            if state == STATE_MATCHED_K:
                state = STATE_MATCHED_K_TICK
            elif state == STATE_MATCHED_S:
                state = STATE_MATCHED_S_TICK
            elif state == STATE_MATCHED_S_TICK:
                state = STATE_MATCHED_S_TICK_TICK
            elif state == STATE_MATCHED_I:
                unl = unl[:idx] + unl[idx + 2:]
                finished = True
            elif state == STATE_MATCHED_K_TICK:
                x_start = idx + 3
                y_start = find_block_end(unl, x_start)
                y_end = find_block_end(unl, y_start)
                X = unl[x_start : y_start]
                unl = unl[:idx] + X + unl[y_end:]
                finished = True
            elif state == STATE_MATCHED_S_TICK_TICK:
                x_start = idx + 4
                y_start = find_block_end(unl, x_start)
                z_start = find_block_end(unl, y_start)
                z_end = find_block_end(unl, z_start)
                X = unl[x_start : y_start]
                Y = unl[y_start : z_start]
                Z = unl[z_start : z_end]
                unl = unl[:idx] + '``' + X + Z + '`' + Y + Z + unl[z_end:]
                finished = True
        else:
            state = STATE_MATCHED_NONE

        idx -= 1

    return unl[1:]

def evaluate_unl_ltr(unl):
    # Initial state
    ticks_matched = 0
    idx = 0

    while idx < len(unl):
        ticks_matched_new = ticks_matched
        if unl[idx] == '`':
            ticks_matched_new += 1
        else:
            ticks_matched_new = 0
        
        if ticks_matched and unl[idx] == 'i':
            return unl[:idx - 1] + unl[idx + 1:]
        elif ticks_matched > 1 and unl[idx] == 'k':
            x_start = idx + 1
            y_start = find_block_end(unl, x_start)
            y_end = find_block_end(unl, y_start)
            X = unl[x_start : y_start]
            return unl[:idx - 2] + X + unl[y_end:]
        elif ticks_matched > 2 and unl[idx] == 's':
            x_start = idx + 1
            y_start = find_block_end(unl, x_start)
            z_start = find_block_end(unl, y_start)
            z_end = find_block_end(unl, z_start)
            X = unl[x_start : y_start]
            Y = unl[y_start : z_start]
            Z = unl[z_start : z_end]
            return unl[:idx - 3] + '``' + X + Z + '`' + Y + Z + unl[z_end:]
        
        ticks_matched = ticks_matched_new
        idx += 1
    
    return unl
