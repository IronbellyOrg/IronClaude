# WS-C STRICT Gate Summary (Step 5.11) — post-deletion

**Status: Complete**
**Verdict: PASS**
**Date:** 2026-06-16

Raw: `phase-outputs/test-results/ws-c-gate.txt`. Run in the `mms-m8m9` worktree, AFTER `t2_normalize.py` + the other legacy artifacts were deleted (Steps 5.3-5.7).

## The "still asserting after deletion" property — CONFIRMED
`tests/swarm/test_bare_review_parity.py` + `tests/swarm/test_recipe_bare_review.py` → **27 passed, 0 skipped, 0 failed**. Every bare-review parity + recipe test **RAN and PASSED** even though `t2_normalize.py` is now gone. NONE was SKIPPED. This is the definitive proof the migration is safe: the original library-vs-library gate (with its `skipif(LEGACY_SCRIPT.exists())`) would have silently skipped here, evaporating the parity coverage; the rebuilt CLI-vs-frozen-golden gate keeps asserting.

- 16 parity tests (5 invariants × 3 scenarios + injection-guard) — all PASS.
- 11 recipe tests (salvage-flag ×5, registry ×2, dispatcher ×3 incl. `test_dispatcher_promotes_parse_error_via_salvage_flag`, duplicates ×1) — all PASS, with NO legacy-script dependency.

## Full swarm suite — 2212 passed, 27 skipped, 0 failed
Baseline comparison (no new regressions):
| run | passed | skipped | failed |
|-----|--------|---------|--------|
| baseline (pre-migration) | 2212 | 26 | 0 |
| WS-B | 2217 | 27 | 0 |
| **WS-C (post-deletion)** | **2212** | **27** | **0** |

Reconciliation: WS-B 2217 − 5 (WS-C removed the 5 parametrized legacy A/B recipe tests `test_legacy_vs_recipe_byte_identical[*]`, now covered transitively by the CLI-vs-golden parity gate) = 2212. Skipped 27 (regen helper env-gated skip, unchanged). **0 failed at every stage.** Every test passing at baseline still passes.

## src↔mirror + staging hygiene
`make verify-sync` → exit 0. Deletions staged via `git rm` on the `src/` side only; mirror orphans pruned (rm on gitignored `.claude/` — never `git add`ed). `git diff --cached --name-only` carries no `.claude/` entries.

## Overall: WS-C PASS
Legacy retirement complete and proven safe: scripts + orphaned refs deleted from both trees, the reworked recipe test + the permanent parity gate both run-and-pass post-deletion, full suite green with no new regressions.
