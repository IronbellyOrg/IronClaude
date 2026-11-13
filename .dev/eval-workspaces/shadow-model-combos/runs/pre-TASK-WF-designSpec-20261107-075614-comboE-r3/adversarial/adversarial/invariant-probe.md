# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis (independent fault-finder agent; findings as returned, evidence condensed by the orchestrator)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The fold sets `disabled_cause` for every DISABLED path so `guard_status` can read it | UNADDRESSED | MEDIUM | source.md:200 sets `disabled_cause = already_draft`; source.md:206 (`user_override`) sets only phase and owned_draft; source.md:112 maps "DISABLED with cause user_override" to `user_override`; plan:60 tests `disabled_cause` only for `already_draft`, plan:61 tests the status without saying it is built through the fold |
| INV-002 | guard_conditions | After a failed engage a later engage can still re-engage | UNADDRESSED | HIGH | `settled(draft, failed)` folds to RELEASE_PENDING with owned_draft false (source.md:199); engage row 6 returns `HOLD(ownership_unproven)` (source.md:138) and never ENGAGE; HOLD at engage is undefined (source.md:68 names only HALT for engage failure); resume row 8 acts only on a live draft (source.md:170), so a ready PR gets NOOP; a literal implementer may treat HOLD as "not HALT" and edit on a mergeable PR; plan:70 and plan:73 do not cover this path |
| INV-003 | state_variables | `guard.cycle_id` identifies the cycle whose publication `published` tests | UNADDRESSED | MEDIUM | no fold row sets or updates `cycle_id` (source.md:194-206; plan:56); a later cycle's engage is NOOP(already_held) and writes no request, so `guard.cycle_id` stays at the first cycle; `held_cycle_published` matches on it (source.md:108); resume row 4 sits above rows 5 and 6 (source.md:166-168); `release_decision` takes `cycle_id` but no row uses it (source.md:145-157) |
| INV-004 | guard_conditions | A zero-edit release in a later cycle is safe | UNADDRESSED | MEDIUM | release row 7 (`applied_edits == 0`) precedes row 8 (source.md:156-157); plan:75 requires a zero-edit new cycle to release even when an earlier fixing cycle is on record, without requiring that cycle's push to be confirmed; whether a run continues after a held push is unstated |
| INV-005 | count_divergence | "One retry" and the toggle slack are bounded by a rule in the core | UNADDRESSED | MEDIUM | the retry test asserts "one retry" (source.md:315); `release_decision` has no RETRY row, `RETRY_RELEASE` appears only in engage row 5 and resume row 7 (source.md:137, 169); `failed_mutations` is never decremented (source.md:199, 205) so slack only widens (source.md:119-121); no AC covers either (plan:70, 75) |
| INV-006 | collection_boundaries | `next_cycle_number` returns max+1 over ids of two or more digits | UNADDRESSED | LOW | contract says "1 + the highest `<kind>-<n>`" (source.md:102); only AC uses fix-1 and fix-2 (plan:59); a lexical max would misorder fix-10 and fix-9; a skip-only settle carries a key with no request (source.md:185), so `unsettled` going negative is unspecified |
| INV-007 | interaction_effects | The Wave 0 bullet can carry its required content and pass its own wording test | UNADDRESSED | LOW | plan:137 requires "at L3 with `--merge-guard off`" while plan:137 and plan:140 forbid L3 or `draft` gate wording in the same bullet; source.md:241 repeats the pair; Tasks 5 and 7 both edit `test_static_grep.py` with no ordering between them |
| INV-008 | sufficiency_challenge | The plan, followed literally, yields a correct implementation with no blocking defect | UNADDRESSED | HIGH | falsifiers named: a resume after a halted `draft_guard_unavailable` with a ready PR (INV-002); a `merge_guard` status test on a log from the real fold after a `user_override` skip (INV-001); a two-cycle held-guard resume (INV-003, INV-004); the resume row 4 AC (plan:77) re-enters `release_decision` without defining `target_sha` or `applied_edits`; an import-cycle check at plan:89 only imports from the package first (unverifiable from plan text) |

## Summary

- **Total findings**: 8
- **ADDRESSED**: 0
- **UNADDRESSED**: 8
  - HIGH: 2 (INV-002, INV-008)
  - MEDIUM: 4 (INV-001, INV-003, INV-004, INV-005)
  - LOW: 2 (INV-006, INV-007)

Gate: 2 HIGH UNADDRESSED, so convergence is BLOCKED until addressed in a further round or accepted as risk (see debate-transcript.md "Round 2.5 resolution").
