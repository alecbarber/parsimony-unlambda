_`^sSkKvViI$[*

START START:
  _ -> START; R; _
  ` -> START; R; `
  ^ -> START; R; ^
  s -> START; R; s
  S -> START; R; S
  k -> START; R; k
  K -> START; R; K
  v -> START; R; v
  V -> START; R; V
  i -> START; R; i
  I -> START; R; I
  $ -> START; R; $
  [ -> START; R; [
  * -> remove_whitespace; L; *

remove_whitespace:
  _ -> synthetic_0_wind_R_*_remove_ws_shuffle; R; $
  ` -> remove_whitespace; L; `
  ^ -> remove_whitespace; L; ^
  s -> remove_whitespace; L; s
  S -> remove_whitespace; L; S
  k -> remove_whitespace; L; k
  K -> remove_whitespace; L; K
  v -> remove_whitespace; L; v
  V -> remove_whitespace; L; V
  i -> remove_whitespace; L; i
  I -> remove_whitespace; L; I
  $ -> synthetic_2_wind2_R_*_next_action; R; $
  [ -> remove_whitespace; L; [
  * -> remove_whitespace; L; *

remove_ws_shuffle:
  _ -> remove_ws_shuffle; L; _
  ` -> remove_ws_shuffle_`; L; _
  ^ -> remove_ws_shuffle_^; L; _
  s -> remove_ws_shuffle_s; L; _
  S -> remove_ws_shuffle_S; L; _
  k -> remove_ws_shuffle_k; L; _
  K -> remove_ws_shuffle_K; L; _
  v -> remove_ws_shuffle_v; L; _
  V -> remove_ws_shuffle_V; L; _
  i -> remove_ws_shuffle_i; L; _
  I -> remove_ws_shuffle_I; L; _
  $ -> START; L; _
  [ -> remove_ws_shuffle_[; L; _
  * -> remove_ws_shuffle_*; L; _

remove_ws_shuffle_`:
  _ -> remove_ws_shuffle; L; `
  ` -> remove_ws_shuffle_`; L; `
  ^ -> remove_ws_shuffle_^; L; `
  s -> remove_ws_shuffle_s; L; `
  S -> remove_ws_shuffle_S; L; `
  k -> remove_ws_shuffle_k; L; `
  K -> remove_ws_shuffle_K; L; `
  v -> remove_ws_shuffle_v; L; `
  V -> remove_ws_shuffle_V; L; `
  i -> remove_ws_shuffle_i; L; `
  I -> remove_ws_shuffle_I; L; `
  $ -> START; L; `
  [ -> remove_ws_shuffle_[; L; `
  * -> remove_ws_shuffle_*; L; `

remove_ws_shuffle_^:
  _ -> remove_ws_shuffle; L; ^
  ` -> remove_ws_shuffle_`; L; ^
  ^ -> remove_ws_shuffle_^; L; ^
  s -> remove_ws_shuffle_s; L; ^
  S -> remove_ws_shuffle_S; L; ^
  k -> remove_ws_shuffle_k; L; ^
  K -> remove_ws_shuffle_K; L; ^
  v -> remove_ws_shuffle_v; L; ^
  V -> remove_ws_shuffle_V; L; ^
  i -> remove_ws_shuffle_i; L; ^
  I -> remove_ws_shuffle_I; L; ^
  $ -> START; L; ^
  [ -> remove_ws_shuffle_[; L; ^
  * -> remove_ws_shuffle_*; L; ^

remove_ws_shuffle_s:
  _ -> remove_ws_shuffle; L; s
  ` -> remove_ws_shuffle_`; L; s
  ^ -> remove_ws_shuffle_^; L; s
  s -> remove_ws_shuffle_s; L; s
  S -> remove_ws_shuffle_S; L; s
  k -> remove_ws_shuffle_k; L; s
  K -> remove_ws_shuffle_K; L; s
  v -> remove_ws_shuffle_v; L; s
  V -> remove_ws_shuffle_V; L; s
  i -> remove_ws_shuffle_i; L; s
  I -> remove_ws_shuffle_I; L; s
  $ -> START; L; s
  [ -> remove_ws_shuffle_[; L; s
  * -> remove_ws_shuffle_*; L; s

remove_ws_shuffle_S:
  _ -> remove_ws_shuffle; L; S
  ` -> remove_ws_shuffle_`; L; S
  ^ -> remove_ws_shuffle_^; L; S
  s -> remove_ws_shuffle_s; L; S
  S -> remove_ws_shuffle_S; L; S
  k -> remove_ws_shuffle_k; L; S
  K -> remove_ws_shuffle_K; L; S
  v -> remove_ws_shuffle_v; L; S
  V -> remove_ws_shuffle_V; L; S
  i -> remove_ws_shuffle_i; L; S
  I -> remove_ws_shuffle_I; L; S
  $ -> START; L; S
  [ -> remove_ws_shuffle_[; L; S
  * -> remove_ws_shuffle_*; L; S

remove_ws_shuffle_k:
  _ -> remove_ws_shuffle; L; k
  ` -> remove_ws_shuffle_`; L; k
  ^ -> remove_ws_shuffle_^; L; k
  s -> remove_ws_shuffle_s; L; k
  S -> remove_ws_shuffle_S; L; k
  k -> remove_ws_shuffle_k; L; k
  K -> remove_ws_shuffle_K; L; k
  v -> remove_ws_shuffle_v; L; k
  V -> remove_ws_shuffle_V; L; k
  i -> remove_ws_shuffle_i; L; k
  I -> remove_ws_shuffle_I; L; k
  $ -> START; L; k
  [ -> remove_ws_shuffle_[; L; k
  * -> remove_ws_shuffle_*; L; k

remove_ws_shuffle_K:
  _ -> remove_ws_shuffle; L; K
  ` -> remove_ws_shuffle_`; L; K
  ^ -> remove_ws_shuffle_^; L; K
  s -> remove_ws_shuffle_s; L; K
  S -> remove_ws_shuffle_S; L; K
  k -> remove_ws_shuffle_k; L; K
  K -> remove_ws_shuffle_K; L; K
  v -> remove_ws_shuffle_v; L; K
  V -> remove_ws_shuffle_V; L; K
  i -> remove_ws_shuffle_i; L; K
  I -> remove_ws_shuffle_I; L; K
  $ -> START; L; K
  [ -> remove_ws_shuffle_[; L; K
  * -> remove_ws_shuffle_*; L; K

remove_ws_shuffle_v:
  _ -> remove_ws_shuffle; L; v
  ` -> remove_ws_shuffle_`; L; v
  ^ -> remove_ws_shuffle_^; L; v
  s -> remove_ws_shuffle_s; L; v
  S -> remove_ws_shuffle_S; L; v
  k -> remove_ws_shuffle_k; L; v
  K -> remove_ws_shuffle_K; L; v
  v -> remove_ws_shuffle_v; L; v
  V -> remove_ws_shuffle_V; L; v
  i -> remove_ws_shuffle_i; L; v
  I -> remove_ws_shuffle_I; L; v
  $ -> START; L; v
  [ -> remove_ws_shuffle_[; L; v
  * -> remove_ws_shuffle_*; L; v

remove_ws_shuffle_V:
  _ -> remove_ws_shuffle; L; V
  ` -> remove_ws_shuffle_`; L; V
  ^ -> remove_ws_shuffle_^; L; V
  s -> remove_ws_shuffle_s; L; V
  S -> remove_ws_shuffle_S; L; V
  k -> remove_ws_shuffle_k; L; V
  K -> remove_ws_shuffle_K; L; V
  v -> remove_ws_shuffle_v; L; V
  V -> remove_ws_shuffle_V; L; V
  i -> remove_ws_shuffle_i; L; V
  I -> remove_ws_shuffle_I; L; V
  $ -> START; L; V
  [ -> remove_ws_shuffle_[; L; V
  * -> remove_ws_shuffle_*; L; V

remove_ws_shuffle_i:
  _ -> remove_ws_shuffle; L; i
  ` -> remove_ws_shuffle_`; L; i
  ^ -> remove_ws_shuffle_^; L; i
  s -> remove_ws_shuffle_s; L; i
  S -> remove_ws_shuffle_S; L; i
  k -> remove_ws_shuffle_k; L; i
  K -> remove_ws_shuffle_K; L; i
  v -> remove_ws_shuffle_v; L; i
  V -> remove_ws_shuffle_V; L; i
  i -> remove_ws_shuffle_i; L; i
  I -> remove_ws_shuffle_I; L; i
  $ -> START; L; i
  [ -> remove_ws_shuffle_[; L; i
  * -> remove_ws_shuffle_*; L; i

remove_ws_shuffle_I:
  _ -> remove_ws_shuffle; L; I
  ` -> remove_ws_shuffle_`; L; I
  ^ -> remove_ws_shuffle_^; L; I
  s -> remove_ws_shuffle_s; L; I
  S -> remove_ws_shuffle_S; L; I
  k -> remove_ws_shuffle_k; L; I
  K -> remove_ws_shuffle_K; L; I
  v -> remove_ws_shuffle_v; L; I
  V -> remove_ws_shuffle_V; L; I
  i -> remove_ws_shuffle_i; L; I
  I -> remove_ws_shuffle_I; L; I
  $ -> START; L; I
  [ -> remove_ws_shuffle_[; L; I
  * -> remove_ws_shuffle_*; L; I

remove_ws_shuffle_$:
  _ -> remove_ws_shuffle; L; $
  ` -> remove_ws_shuffle_`; L; $
  ^ -> remove_ws_shuffle_^; L; $
  s -> remove_ws_shuffle_s; L; $
  S -> remove_ws_shuffle_S; L; $
  k -> remove_ws_shuffle_k; L; $
  K -> remove_ws_shuffle_K; L; $
  v -> remove_ws_shuffle_v; L; $
  V -> remove_ws_shuffle_V; L; $
  i -> remove_ws_shuffle_i; L; $
  I -> remove_ws_shuffle_I; L; $
  $ -> START; L; $
  [ -> remove_ws_shuffle_[; L; $
  * -> remove_ws_shuffle_*; L; $

remove_ws_shuffle_[:
  _ -> remove_ws_shuffle; L; [
  ` -> remove_ws_shuffle_`; L; [
  ^ -> remove_ws_shuffle_^; L; [
  s -> remove_ws_shuffle_s; L; [
  S -> remove_ws_shuffle_S; L; [
  k -> remove_ws_shuffle_k; L; [
  K -> remove_ws_shuffle_K; L; [
  v -> remove_ws_shuffle_v; L; [
  V -> remove_ws_shuffle_V; L; [
  i -> remove_ws_shuffle_i; L; [
  I -> remove_ws_shuffle_I; L; [
  $ -> START; L; [
  [ -> remove_ws_shuffle_[; L; [
  * -> remove_ws_shuffle_*; L; [

remove_ws_shuffle_*:
  _ -> remove_ws_shuffle; L; *
  ` -> remove_ws_shuffle_`; L; *
  ^ -> remove_ws_shuffle_^; L; *
  s -> remove_ws_shuffle_s; L; *
  S -> remove_ws_shuffle_S; L; *
  k -> remove_ws_shuffle_k; L; *
  K -> remove_ws_shuffle_K; L; *
  v -> remove_ws_shuffle_v; L; *
  V -> remove_ws_shuffle_V; L; *
  i -> remove_ws_shuffle_i; L; *
  I -> remove_ws_shuffle_I; L; *
  $ -> START; L; *
  [ -> remove_ws_shuffle_[; L; *
  * -> remove_ws_shuffle_*; L; *

next_action:
  _ -> next_action; L; _
  ` -> next_action; L; `
  ^ -> next_action; L; ^
  s -> next_action; L; s
  S -> next_action; L; S
  k -> next_action; L; k
  K -> next_action; L; K
  v -> next_action_v; L; v
  V -> next_action; L; V
  i -> next_action_i; L; i
  I -> next_action; L; I
  $ -> ACCEPT; R; $
  [ -> next_action; L; [
  * -> next_action; L; *

next_action_v:
  _ -> next_action; L; _
  ` -> evaluate_v; R; v
  ^ -> next_action; L; ^
  s -> next_action; L; s
  S -> next_action; L; S
  k -> next_action; L; k
  K -> next_action; L; K
  v -> next_action_v; L; v
  V -> next_action; L; V
  i -> next_action_i; L; i
  I -> next_action; L; I
  $ -> ACCEPT; R; $
  [ -> next_action; L; [
  * -> next_action; L; *

next_action_i:
  _ -> next_action; L; _
  ` -> evaluate_i; R; _
  ^ -> next_action; L; ^
  s -> next_action; L; s
  S -> next_action; L; S
  k -> next_action; L; k
  K -> next_action; L; K
  v -> next_action_v; L; v
  V -> next_action; L; V
  i -> next_action_i; L; i
  I -> next_action; L; I
  $ -> ACCEPT; R; $
  [ -> next_action; L; [
  * -> next_action; L; *

evaluate_i:
  _ -> ERROR; R; _
  ` -> ERROR; R; `
  ^ -> ERROR; R; ^
  s -> ERROR; R; s
  S -> ERROR; R; S
  k -> ERROR; R; k
  K -> ERROR; R; K
  v -> ERROR; R; v
  V -> ERROR; R; V
  i -> START; R; _
  I -> ERROR; R; I
  $ -> ERROR; R; $
  [ -> ERROR; R; [
  * -> ERROR; R; *

evaluate_v:
  _ -> ERROR; R; _
  ` -> ERROR; R; `
  ^ -> ERROR; R; ^
  s -> ERROR; R; s
  S -> ERROR; R; S
  k -> ERROR; R; k
  K -> ERROR; R; K
  v -> match_expression; R; [
  V -> ERROR; R; V
  i -> ERROR; R; i
  I -> ERROR; R; I
  $ -> ERROR; R; $
  [ -> ERROR; R; [
  * -> ERROR; R; *

match_expression:
  _ -> match_expression; R; _
  ` -> match_expression_`; R; `
  ^ -> match_expression; R; ^
  s -> START; R; s
  S -> match_expression; R; S
  k -> START; R; k
  K -> match_expression; R; K
  v -> START; R; v
  V -> match_expression; R; V
  i -> START; R; i
  I -> match_expression; R; I
  $ -> match_expression; R; $
  [ -> match_expression; R; [
  * -> ERROR; R; *

match_expression_`:
  _ -> match_expression_`; R; _
  ` -> match_expression_`; R; `
  ^ -> match_expression_`; R; ^
  s -> match_expression_`l; R; s
  S -> match_expression_`; R; S
  k -> match_expression_`l; R; k
  K -> match_expression_`; R; K
  v -> match_expression_`l; R; v
  V -> match_expression_`; R; V
  i -> match_expression_`l; R; i
  I -> match_expression_`; R; I
  $ -> match_expression_`; R; $
  [ -> match_expression_`; R; [
  * -> ERROR; R; *

match_expression_`l:
  _ -> match_expression_`l; R; _
  ` -> match_expression_`; R; `
  ^ -> match_expression_`l; R; ^
  s -> match_expression_update_tick; L; S
  S -> match_expression_`l; R; S
  k -> match_expression_update_tick; L; K
  K -> match_expression_`l; R; K
  v -> match_expression_update_tick; L; V
  V -> match_expression_`l; R; V
  i -> match_expression_update_tick; L; I
  I -> match_expression_`l; R; I
  $ -> match_expression_`l; R; $
  [ -> match_expression_`l; R; [
  * -> ERROR; R; *

match_expression_update_tick:
  _ -> match_expression_update_tick; L; _
  ` -> synthetic_4_wind2_L_[_match_expression; L; ^
  ^ -> match_expression_update_tick; L; ^
  s -> match_expression_update_tick; L; s
  S -> match_expression_update_tick; L; S
  k -> match_expression_update_tick; L; k
  K -> match_expression_update_tick; L; K
  v -> match_expression_update_tick; L; v
  V -> match_expression_update_tick; L; V
  i -> match_expression_update_tick; L; i
  I -> match_expression_update_tick; L; I
  $ -> match_expression_update_tick; L; $
  [ -> match_expression_update_tick; L; [
  * -> match_expression_update_tick; L; *

synthetic_0_wind_R_*_remove_ws_shuffle:
  _ -> synthetic_0_wind_R_*_remove_ws_shuffle; R; _
  ` -> synthetic_0_wind_R_*_remove_ws_shuffle; R; `
  ^ -> synthetic_0_wind_R_*_remove_ws_shuffle; R; ^
  s -> synthetic_0_wind_R_*_remove_ws_shuffle; R; s
  S -> synthetic_0_wind_R_*_remove_ws_shuffle; R; S
  k -> synthetic_0_wind_R_*_remove_ws_shuffle; R; k
  K -> synthetic_0_wind_R_*_remove_ws_shuffle; R; K
  v -> synthetic_0_wind_R_*_remove_ws_shuffle; R; v
  V -> synthetic_0_wind_R_*_remove_ws_shuffle; R; V
  i -> synthetic_0_wind_R_*_remove_ws_shuffle; R; i
  I -> synthetic_0_wind_R_*_remove_ws_shuffle; R; I
  $ -> synthetic_0_wind_R_*_remove_ws_shuffle; R; $
  [ -> synthetic_0_wind_R_*_remove_ws_shuffle; R; [
  * -> remove_ws_shuffle; R; *

synthetic_2_wind2_R_*_next_action:
  _ -> synthetic_2_wind2_R_*_next_action; R; _
  ` -> synthetic_2_wind2_R_*_next_action; R; `
  ^ -> synthetic_2_wind2_R_*_next_action; R; ^
  s -> synthetic_2_wind2_R_*_next_action; R; s
  S -> synthetic_2_wind2_R_*_next_action; R; S
  k -> synthetic_2_wind2_R_*_next_action; R; k
  K -> synthetic_2_wind2_R_*_next_action; R; K
  v -> synthetic_2_wind2_R_*_next_action; R; v
  V -> synthetic_2_wind2_R_*_next_action; R; V
  i -> synthetic_2_wind2_R_*_next_action; R; i
  I -> synthetic_2_wind2_R_*_next_action; R; I
  $ -> synthetic_2_wind2_R_*_next_action; R; $
  [ -> synthetic_2_wind2_R_*_next_action; R; [
  * -> next_action; L; *

synthetic_4_wind2_L_[_match_expression:
  _ -> synthetic_4_wind2_L_[_match_expression; L; _
  ` -> synthetic_4_wind2_L_[_match_expression; L; `
  ^ -> synthetic_4_wind2_L_[_match_expression; L; ^
  s -> synthetic_4_wind2_L_[_match_expression; L; s
  S -> synthetic_4_wind2_L_[_match_expression; L; S
  k -> synthetic_4_wind2_L_[_match_expression; L; k
  K -> synthetic_4_wind2_L_[_match_expression; L; K
  v -> synthetic_4_wind2_L_[_match_expression; L; v
  V -> synthetic_4_wind2_L_[_match_expression; L; V
  i -> synthetic_4_wind2_L_[_match_expression; L; i
  I -> synthetic_4_wind2_L_[_match_expression; L; I
  $ -> synthetic_4_wind2_L_[_match_expression; L; $
  [ -> match_expression; R; [
  * -> synthetic_4_wind2_L_[_match_expression; L; *

