# Phase 5 — fsm tests summary

**Overall:** PASS
**Counts:** 28 passed, 0 failed (0.06s)
`pytest test_review_retrigger.py test_auggie_fallback.py test_loop_guard.py -v`

## Modules
- `test_review_retrigger.py` (NEW, R1): 7 tests — T-1101 one re-trigger/push, T-1102
  attributed ticks, **T-PUSH-WITHOUT-REREVIEW-NO-TICK** (push but timeout → round_counter
  stays 0), T-1103 INV-R1 bound, T-1104 attributed advances, T-1105 core holds no
  hard-coded trigger literal, T-1106 S5a skipped when applied_edits==0.
- `test_auggie_fallback.py` (NEW, R2/R3): 8 tests — T-1110 initial-poll decline→fallback,
  T-1113 S5-poll decline→fallback, **T-AUGGIE-AT-MOST-ONCE** (invoke exactly once),
  T-1122 clamp→1, T-1123 single-shot no-loopback, T-1125 round_counter frozen / two
  independent counters, T-1121 push_count<=max_rounds+1, FR-9.4 verify-before-remediate.
- `test_loop_guard.py` (EXTENDED): +4 V1.1 tests (deferred increment gated on attributed,
  INV-R1 monotone/bounded, INV-R3 clamp + counter independence, fallback cap-1). The 9
  PRE-EXISTING INV-001 fence-post tests (T-626-OFF-BY-ONE, the fence-post matrix,
  should_halt(2,2), user_label(0)==1, T-VANISHED-MONO) are UNCHANGED and still pass.

## INV-001 preservation evidence
- Exactly ONE `round_counter += 1` site (fsm.py:987); the 2 `fallback_round_counter += 1`
  are the SEPARATE fallback counter.
- INV-001 edge `(S5_AWAITING_REREVIEW, "rereview_attributed") → S2_CLASSIFY` byte-identical.
- `max_rounds=N ⇒ N pushes` preserved (fence-post matrix green).
- Two fix-cycle issues caught and fixed in this step: a `auggie review` literal in 2 fsm.py
  COMMENTS (reworded — the token must live only in the script, T-1105), and an `_ff` helper
  kwarg-duplication.

## NFR-6
`phase5-core-purity-grep.txt`: only 4 pre-existing docstring matches; zero executable tokens.
