# Phase 3 Consolidated QA Findings

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-06
**Inputs:**
- `qa-phase3-completeness-report.md` — PASS (0 blocking, 4 MINOR)
- `qa-phase3-seam-report.md` — PASS (7/7, 0 defects, 1 INFO)
- `qa-phase3-actionability-report.md` — FAIL (2 IMPORTANT, 4 MINOR)

## Overall Consolidated Verdict: FAIL

FAIL because the actionability lens reported issues. Completeness and seam-fidelity each PASSed. No CRITICAL findings; the ceiling is IMPORTANT and no finding produces a false-GREEN verdict (the computed assertions are sound).

## Deduplicated Findings

| ID | Severity | Lens | Location | Finding | Required Fix |
|---|---|---|---|---|---|
| P3-ACT-001 | IMPORTANT | actionability | `test_ensemble_fallback_stub.py` `_config` | The `dataclasses.replace(config, tier2_fallback_enabled=True)` "force ON" flip is inert: `run_fallback_ladder` never reads `tier2_fallback_enabled` (the enable-gate lives in `run_tier2_ensemble`, which neither test calls). Nothing tests that enabling engages the ladder or disabling skips it. | Add an ensemble-level integration test that drives the REAL `run_tier2_ensemble` on the stub lane with a primary-failure `transport_for_slot`, asserting the ladder engages (t2_fallback present, certified_with_fallback True, tier_reached 2) when `tier2_fallback_enabled=True`, and is byte-skipped (t2_fallback absent, degraded-tier1) when False. This also exercises the real `resolve_t1_fallback_factory` stub arm (P3-ACT-005) and real `_stamp_worker_paths` (P3-ACT-004). |
| P3-ACT-002 | IMPORTANT | actionability | `test_ensemble_fallback_stub.py` incident test | `assert outcome.metadata["primary_failures_preserved"]` is truthy-only — a regression preserving the wrong/partial failure set still passes. | Assert exact contents (the eligible-failure attempt ids for the fixture). |
| P3-ACT-003 | MINOR | actionability | `test_ensemble_fallback_stub.py` `_incident_primaries` | Index arrangement diverges from design §8 (survivor at index 0 vs §8's index 1). | Align survivor to index 1 with failures `[primary:00, primary:02]`, OR soften "replay" to "reproduce the §8 shape". Combined with P3-ACT-002 exact-id assert this self-documents. |
| P3-ACT-004 | MINOR | actionability | `test_ensemble_fallback_stub.py` `_stamp` | Injected `_stamp` differs from prod `_stamp_worker_paths`; F2 never exercises the real stamp. | Covered by the new ensemble-level integration test (P3-ACT-001), which wires the real `stamp=_stamp_worker_paths` through `run_tier2_ensemble`. |
| P3-ACT-005 | MINOR | actionability | `test_ensemble_fallback_stub.py` `_trivial_factory` | The real `resolve_t1_fallback_factory("stub")` arm and the `_T1_PROXY_BINDING`-gated openai_compat arm are never integration-tested. | The stub arm is covered by the new ensemble test (P3-ACT-001). Add a small unit asserting the gated openai_compat factory raises `TransportEnvError` (folds to `fallback_config_missing`). |
| P3-ACT-006 | MINOR | actionability | `test_ensemble_fallback_stub.py` incident test | Incident case omits `engaged`/`fallback_attempt_count`/`exhausted` asserts the counter-case has. | Add `engaged is True`, `fallback_attempt_count == 1`, `exhausted is False`. |
| P3-COMP-MINOR-1 | MINOR (non-blocking) | completeness | `fallback.py` `run_fallback_ladder` | `env` param accepted but unreferenced (mirrors design §2.1). | Leave as-is (aligns seam signature with the design) — no fix required. |
| P3-COMP-MINOR-2 | MINOR (non-blocking) | completeness | `make_fallback_slot_factory` / `resolve_t1_fallback_factory` | F1 name→distinct-model factory binding is staged but not wired into the live openai_compat arm (Phase 4/5 scope behind the HALT). | Authorized deferral. Carry into Phase 4. |
| P3-COMP-MINOR-3 | MINOR (non-blocking) | completeness | `ensemble.py` `_gated_factory` | Unreachable second `raise` documented as a Phase 4 placeholder. | No Phase 3 action. |
| P3-SEAM-INFO-1 | INFO (non-blocking) | seam-fidelity | `select_contributing_set` | Enabled happy path with ≥3 diverse healthy primaries returns the smallest 2-subset → `reviewer_count` reports 2 rather than the raw success count. Intended minimal-certifying-set design (matches design §4.2 rule 3 + the Phase 1 `test_smallest_passing_set` unit test); production-unreachable today (stub OFF, openai_compat HALT-gated). | No remediation. Recorded for Phase 5 confirmation. |

## Fix Routing

Consolidated verdict is FAIL. Step 3.G6 must run exactly ONE serialized fix agent (I20) with `fix_authorization: true` to address P3-ACT-001..006. All fixes are test-only additions/tightenings; no source change, `contract.py` must stay byte-unchanged, and the disabled path must stay byte-equivalent. The completeness/seam MINOR/INFO items require no fix (carried forward as notes).
