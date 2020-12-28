_`skvi$*

START start:
  $ -> rewind_remove_whitespace; R; $

rewind_remove_whitespace: R
  * -> remove_whitespace; L; *

rewind_next_action: R
  * -> next_action; L; *

rewind_whitespace_shuffle: R
  * -> whitespace_shuffle; R; *

remove_whitespace: L
  _ -> rewind_whitespace_shuffle; R; _
  $ -> rewind_next_action; R; $

whitespace_shuffle: L
  _ -> whitespace_shuffle__; L; `
  ` -> whitespace_shuffle_`; L; `
  s -> whitespace_shuffle_s; L; `
  k -> whitespace_shuffle_k; L; `
  v -> whitespace_shuffle_v; L; `
  i -> whitespace_shuffle_i; L; `
  * -> whitespace_shuffle_*; L; `

whitespace_shuffle_`:
  $ -> rewind; L; `
  ` -> whitespace_shuffle_`; L; `
  s -> whitespace_shuffle_s; L; `
  k -> whitespace_shuffle_k; L; `
  v -> whitespace_shuffle_v; L; `
  i -> whitespace_shuffle_i; L; `
  * -> whitespace_shuffle_*; L; `
whitespace_shuffle_s:
  $ -> rewind; L; s
  ` -> whitespace_shuffle_`; L; s
  s -> whitespace_shuffle_s; L; s
  k -> whitespace_shuffle_k; L; s
  v -> whitespace_shuffle_v; L; s
  i -> whitespace_shuffle_i; L; s
  * -> whitespace_shuffle_*; L; s
whitespace_shuffle_k:
  $ -> rewind; L; k
  ` -> whitespace_shuffle_`; L; k
  s -> whitespace_shuffle_s; L; k
  k -> whitespace_shuffle_k; L; k
  v -> whitespace_shuffle_v; L; k
  i -> whitespace_shuffle_i; L; k
  * -> whitespace_shuffle_*; L; k
whitespace_shuffle_v:
  $ -> rewind; L; v
  ` -> whitespace_shuffle_`; L; v
  s -> whitespace_shuffle_s; L; v
  k -> whitespace_shuffle_k; L; v
  v -> whitespace_shuffle_v; L; v
  i -> whitespace_shuffle_i; L; v
  * -> whitespace_shuffle_*; L; v
whitespace_shuffle_i:
  $ -> rewind; L; i
  ` -> whitespace_shuffle_`; L; i
  s -> whitespace_shuffle_s; L; i
  k -> whitespace_shuffle_k; L; i
  v -> whitespace_shuffle_v; L; i
  i -> whitespace_shuffle_i; L; i
  * -> whitespace_shuffle_*; L; i
whitespace_shuffle_*:
  $ -> rewind; L; *
  ` -> whitespace_shuffle_`; L; *
  s -> whitespace_shuffle_s; L; *
  k -> whitespace_shuffle_k; L; *
  v -> whitespace_shuffle_v; L; *
  i -> whitespace_shuffle_i; L; *
  * -> whitespace_shuffle_*; L; *

next_action: L
  $ -> ACCEPT; R; $
  i -> match_i_application; L; i

match_i_application: L; next_action
  $ -> ACCEPT; R; $
  ` -> apply_i; R; _

apply_i:
  i -> rewind_remove_whitespace; R; _