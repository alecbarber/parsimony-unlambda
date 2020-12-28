01

START:
  0 -> state2; R; 0
  1 -> state2; R; 1

state2:
  0 -> state3; R; 0
  1 -> state3; R; 1

state3:
  0 -> state4; R; 0
  1 -> state4; R; 1

state4:
  0 -> state3-2; L; 0
  1 -> state3-2; L; 1

state3-2:
  0 -> state2-2; L; 0
  1 -> state2-2; L; 1

state2-2:
  0 -> START; L; 0
  1 -> START; L; 1