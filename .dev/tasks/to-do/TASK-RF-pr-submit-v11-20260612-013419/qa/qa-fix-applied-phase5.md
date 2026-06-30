# Phase 5 — Fix Applied (Step 5.G6)

Single serial writer (executor, I20). 4 ACTIONABLE fixes; INV-001 NOT touched.

| Finding | Fix | Files |
|---|---|---|
| F2 (MINOR) S5A/S5B states never materialized | run_skill sets `result.state = S5A_RETRIGGER_REVIEW` at the re-trigger step (applied_edits>0 branch); `_run_fallback` sets `result.state = S5B_AUGGIE_FALLBACK` at entry — the imperative surface now visibly enters the new states (overwritten by the terminal; topology-faithful) | fsm.py |
| F3 (MINOR) namespace drift "attributed" vs "rereview_attributed" | Added a comment documenting the mapping (outcome token vs FSM edge name — deliberately distinct vocabularies) | fsm.py |
| F4 (MINOR) dead transition() edges + dual-surface drift risk | Added `test_transition_v11_edges` exercising transition()'s 6 V1.1 edges + the byte-identical INV-001 edge + the fallback_skip residual selector (pins both surfaces; catches future transition()-side drift) | test_auggie_fallback.py |
| F5 (IMPORTANT, test-quality) auggie strict-once mislabel | Strengthened `test_t_auggie_at_most_once` to call `_run_fallback` TWICE on the same SkillResult (asserts invoke fires exactly once across re-entry) + a fresh-result control (proves the guard, not an inert recorder) | test_auggie_fallback.py |

## Deferred / no-fix (documented in consolidated findings)
- F1 forked fallback pipeline → by-design (run_skill is the existing imperative
  run-to-terminal driver that does NOT call transition(); refactoring is high-risk in the
  highest-risk phase + out of scope). Mitigated by F4's dual-surface test.
- F6 fence-post matrix non-discrimination of `>=` gate → the `>=` gate is directly guarded
  by `test_gate_uses_ge_not_gt` + `test_fallback_round_counter_cap_one`. No change.
- F7 recovery.py "unchanged" wording → semantics correct.

## Verification
- EXACTLY ONE `round_counter += 1` (`grep -cE '[^_]round_counter \+= 1'` = 1). INV-001 edge
  byte-identical; `>=` gate untouched; the 9 INV-001 fence-post tests UNCHANGED + green.
- `pytest tests/pr_submit/` = **172 passed** (was 171; +1 transition test).
- `ruff check` + `ruff format --check` green on fsm.py + test_auggie_fallback.py.
- NFR-6: no new gh/git/subprocess token (the F2/F3 changes are state assignments + a comment).
