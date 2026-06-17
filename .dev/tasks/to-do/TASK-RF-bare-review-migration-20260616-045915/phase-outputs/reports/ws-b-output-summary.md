# WS-B Output Summary (PG4.1 aggregation)

**Status: Complete**
**Date:** 2026-06-16

## Handoff artifacts
- `phase-outputs/discovery/ws-b-golden-design.md` — design + ground truth (legacy vs CLI schema, CLI-aligned capture, sentinel normalization, scripted-transport mechanism).
- `phase-outputs/plans/golden-capture-verdict.md` — golden well-formedness verdict: **PASS** (3 scenario dirs, all bodies + contracts non-zero).
- `phase-outputs/test-results/golden-inventory.txt` — raw `find`/`ls` of the golden tree.
- `phase-outputs/test-results/ws-b-gate.txt` — raw Step 4.5 gate output.
- `phase-outputs/test-results/ws-b-gate-summary.md` — WS-B gate verdict: **PASS**.

## Deliverables produced by WS-B
| deliverable | path | state |
|-------------|------|-------|
| Frozen golden tree (3 scenarios) | `tests/swarm/fixtures/bare_review_v1/golden/{all-success,partial-with-timeout,salvage-promoted}/` | 13 files: per-reviewer `.md` + `return-contract.yaml` per scenario + `_review_target.py` + `README.md` |
| Env-gated regen helper | `tests/swarm/test_bare_review_golden_regen.py` | `SWARM_REGEN_GOLDEN=1`; skips in CI; runs REAL legacy `t2_normalize.py`; CLI-aligned args |
| Rebuilt parity gate | `tests/swarm/test_bare_review_parity.py` | 795→476 lines; CLI-vs-golden; 16 tests; NO legacy-script runtime dependency |

## Golden inventory
- `all-success/`: `bare-review-0{1,2,3}-m.md` + `return-contract.yaml` (3 bodies, M=3, status=success)
- `partial-with-timeout/`: `bare-review-0{1,2}-m.md` + `return-contract.yaml` (2 bodies — timeout slot none, M=2, status=partial)
- `salvage-promoted/`: `bare-review-0{1,2,3}-m.md` + `return-contract.yaml` (3 bodies, M=3, status=success)

## Rebuilt parity test result
**16 passed, 0 skipped, 0 failed** (Step 4.5):
- 5 invariants × 3 scenarios (byte-equality, aggregate status, per-slot status+M/N, suspect+adversarial handoff, output_files length) — all CLI-driven via `runner.invoke(swarm_group, ["run",...,"--transport","stub"])`.
- Injection-guard suffix assertion (G-2): `system_prompt_fragment` ends with `CANONICAL_INJECTION_GUARD_SENTENCE`; full prompt byte-parity deliberately NOT asserted.

## WS-B gate verdict
**PASS** — byte-equality CLI-vs-golden across all 3 scenarios with NO legacy-script runtime dependency; full swarm suite 2217 passed / 27 skipped / 0 failed (no new regressions vs baseline); touched files ruff-clean.

## Open item for this gate to scrutinize
**FR-028 §7.4 salvage-promotion divergence (HIGH).** The live CLI does NOT promote an upstream `parse_error→success` (shared-`recipe_args` root cause in `normalize_wave2`). The gate is consistent with the frozen golden (salvage driven as 3 successes → success/M=3; body bytes identical). PG4 should assess whether this is acceptable for the migration or requires escalation. Documented inline in the parity test + as a HIGH follow-up.
