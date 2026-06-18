# Reflect REPORT — POST / deep (Tier 2)

**Target:** FR-028 fix — `fix(swarm): thread per-worker status into recipe normalize` (commit `d2ad3cbd`, branch `fix/swarm-normalize-perworker-status-fr028`; diff `e89e40ce..d2ad3cbd`, 3 files +121/-1).
**Mode:** post · **Tier:** 2 (forced by `--depth deep`) · **Status: SUCCESS** · **Calibrated confidence: 0.88**
**Date:** 2026-06-17

## Why this target
The migration itself was already audited twice by the PC.5 reflect gate (content-clean both times). The **un-audited** work is the FR-028 remediation — a delegated change to **shared** `normalize_wave2` (inline + `--resume` paths + every lens recipe), exactly the high-blast-radius surface that warrants an independent deep audit.

## Verdict: the fix is SOUND — no defects, no regressions
Two heterogeneous reviewers (sonnet/analyzer + haiku/qa) ran adversarially; both returned **sound/PASS**. The third reviewer (fable/refactorer) was **unavailable** (Fable 5 access-gated) → `t2_model_class_diversity: degraded` (N=2 floor, valid).

**Grounded correctness evidence:**
- The injection `args = {**args, "status": worker.status}` (`normalize.py:448`) is placed AFTER the timeout/proxy_error hard-failure short-circuit (so only `success`/`parse_error` workers reach it) and BEFORE `recipe.normalize` + the salvage decision — so a recoverable `parse_error` worker now enters the §7.4 salvage branch and is promoted to `success`.
- **Determinism preserved:** status-only is injected; `elapsed_ms`/timing is deliberately NOT threaded, so the frozen-golden byte-equality holds — `test_bare_review_parity.py` → **16 passed**. For a `success` worker the injection equals the old default (no-op), so existing golden bytes are unchanged.
- **Shared dict unmutated:** `args = {**args, …}` builds a per-worker copy; no cross-worker bleed (verified + the mixed-batch test asserts it).
- **No regression in shared infrastructure:** full swarm suite **2215 passed / 27 skipped / 0 failed** (+3 new tests vs the 2212 baseline); the 119 other-lens recipe tests (findings-table / hypothesis-table / verdict-only) **pass** unchanged.
- **TDD evidence:** the 3 new tests in `test_recipe_bare_review.py` drive the REAL shared-args path (`status` omitted from `recipe_args`) — recoverable→promoted, unrecoverable→stays `parse_error`, mixed batch resolves per-worker; `test_normalize.py::test_recipe_args_forwarded` correctly updated.

## Deviation classification
| Class | Count | Notes |
|-------|-------|-------|
| Authorized | 1 | The FR-028 fix is an explicitly **user-authorized** remediation. |
| Necessary | 0 | |
| Drift | 0 | |
| **Regression** | **0** | Verified via the §6.1 verification triangle (suite + parity + other-lens tests), not self-report. |

## Findings (2 — both LOW, non-blocking, evidence-validated GROUNDED, 0 dropped)

**LOW-1 (doc drift, analyzer) — stale parity-test comments.** `tests/swarm/test_bare_review_parity.py:181-208` (on the migration branch) still states the live CLI salvage promotion "does not fire on the CLI path. This is a documented FR-028 divergence tracked as a follow-up." FR-028 now FIXES that divergence, so these comments are stale. *Recommendation:* when the FR-028 branch merges, update the parity test's `salvage-promoted` scenario comments (the divergence no longer exists); the gate's behavior is unaffected (it drives salvage as 3 plain-success reviewers, which remains valid).

**LOW-2 (test coverage, qa) — other lens recipe tests don't exercise the shared-args shape.** `tests/swarm/test_recipe_verdict_only.py` (L234/316/343) and `test_recipe_findings_table.py` (L193/234) pass `status` explicitly inside `recipe_args`, testing the overwrite-pass-through path rather than the production shared-args shape (where `normalize_wave2` injects per-worker status). These 119 tests still pass; the observation is that the FR-028 shared-args coverage was added for `bare-review` only. *Recommendation (LOW):* add shared-args variants for the other lens recipes for parity, if/when those lenses gain salvage semantics.

## Ensemble / anti-bias posture (§11.0 conditional sufficiency)
- Heterogeneous reviewers: **2 of 3** classes (sonnet + haiku; fable unavailable) → anti-confirmation guarantee is **degraded**, not full. Both reviewers converged on "sound" independently, which is corroborating but weaker than a 3-class agreement.
- Calibrator: inline (no disjoint 3rd non-reviewer class available with fable down) → `calibrator_diversity: degraded`.
- Vendor diversity: single (Anthropic) — warn-only in v1.
- Net: the SOUND verdict rests on **grounded verification evidence** (suite/parity/other-lens all green, re-run independently by the reviewers) more than on ensemble agreement — appropriate given the degraded ensemble.

## Promotion
`not-applicable` — the FR-028 fix is a branch commit, not a `.dev/tasks/to-do/TASK-*` work-unit, so no Wave-7 promotion adapter applies.

## Recommendation
**Ship the FR-028 fix** — it is correct, regression-free, determinism-preserving, and TDD-covered. Address LOW-1 (stale parity comment) at FR-028 merge time. LOW-2 is optional. No Tier-3 remediation needed.
