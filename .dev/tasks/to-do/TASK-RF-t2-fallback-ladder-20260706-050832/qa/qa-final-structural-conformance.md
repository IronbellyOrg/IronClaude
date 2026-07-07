# QA Report — Task Integrity (Step 6.G2: Template-Conformance / Spec-Coverage Lens)

**Topic:** Reflect Tier-2 Fallback Model Ladder — structural conformance vs design §9/§10
**Date:** 2026-07-07
**Phase:** task-integrity (structural conformance, report-only)

## Overall Verdict: PASS (with 1 MINOR + 1 INFO)

The change set is fully conformant with design §10 (change map) and §9 (test surface). Every mandated file change is present, both no-change guardrails hold at 0 diff lines, all 9 §9 test rows map to real green tests, and tests are in the correct directories.

## Items Reviewed (15/15 PASS)

- §10 `fallback.py` NEW with all pure helpers + `run_fallback_ladder` — PASS.
- §10 `ensemble.py` controller insert + `t2_fallback=` kwarg + F4 deadline + `resolve_t1_fallback_factory` — PASS.
- §10 `models.py` 3 defaulted fields — PASS.
- §10 `contract.py` NONE (0-diff) — PASS.
- §10 `commands.py` flag wiring (decl/param/forward/tmux) — PASS.
- §10 `swarm/config.py` T1 slot family + `_collect_models` generalization — PASS.
- §10 `openai_compat.py` `read_env_for_pool` + thin `read_env` — PASS.
- §10 `swarm/commands.py` resolver parameterized — PASS.
- §10 `swarm/models.py` NONE (0-diff) — PASS.
- §9 classify/plan/select/slot-factory/contract/stub tests exist — PASS.
- §9 verdict-unchanged F6 in `test_verdict_mapping.py` — PASS.
- §9 swarm `test_config.py` T1 + `test_openai_compat.py` F3 extended — PASS.
- Tests at `tests/cli/reflect/` + `tests/swarm/`, NOT `tests/cli/swarm/` (absent) — PASS.
- Tests run & green: 145 passed over 12 files — PASS.
- F1 slot-factory binding asserted — PASS.

## Issues Found

| # | Severity | Location | Issue | Fix decision |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `tests/cli/reflect/fixtures/pass_with_t2_fallback.yaml` | Orphan fixture: zero references in `tests/`/`src/`. Its sibling `pass_no_t2_fallback.yaml` IS consumed by `test_verdict_mapping.py`; this populated-block counterpart is never asserted against `derive_verdict`. | FIX: add a `test_verdict_mapping.py` case that loads `pass_with_t2_fallback.yaml` and asserts the verdict is unchanged (still PASS) — closing the additive-only proof symmetrically and using the orphan. Preferred over deletion. |
| 2 | INFO | test-count nomenclature | §9 defines 6 new reflect test files; the change set has 8 (the 2 extra — `test_ensemble_fallback_engage.py`, `test_fallback_config.py` — are documented authorized additions). Over-delivery, not a gap. | None. |

## Adversarial Note

The "assume ≥10 missing elements" mandate did not surface structural gaps. 9/9 §10 rows verified (both NONE guardrails at literal 0-diff), no misplaced tests, no stubbed/skipped test (145 passed, 0 skipped), authorized additions each documented with rationale. The only genuine defect is the orphan fixture (MINOR).

## Recommendation

Wire `pass_with_t2_fallback.yaml` into a verdict-unchanged assertion (or remove it) so no dead test artifact ships. No action on the INFO count-nuance.
