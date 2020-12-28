01

START:
  0 -> branch1; R; 0
  1 -> branch2; R; 1

branch1:
  0 -> branch1a; R; 0
  1 -> branch1b; R; 1

branch1a:
  0 -> ERROR; R; 0
  1 -> branch1c; R; 1

branch1b:
  0 -> branch1c; R; 0
  1 -> branch1c; R; 1

branch1c:
  0 -> ACCEPT; R; 0
  1 -> branch1; R; 1

branch2:
  0 -> branch2a; R; 0
  1 -> branch2b; R; 1

branch2a:
  0 -> ERROR; R; 0
  1 -> branch2c; R; 1

branch2b:
  0 -> branch2c; R; 0
  1 -> branch2c; R; 1

branch2c:
  0 -> ACCEPT; R; 0
  1 -> branch2; R; 1