# R0.2 Test Summary — Anti-Instinct Allowlist (Contract #10)

**Phase:** 3 (Step 3.6)
**Worktree:** `/config/workspace/IronClaude-RoadmapRewrite/`
**Command:** `uv run pytest tests/roadmap/test_anti_instinct_recurrence.py tests/roadmap/test_obligation_scanner.py tests/roadmap/test_obligation_scanner_meta_context.py tests/roadmap/test_obligation_scanner_extract_component_context.py tests/roadmap/test_anti_instinct_integration.py -v`

## Overall result: PASSED

- Total tests collected: **135** (across 5 files)
- Passed: **134**
- Skipped: **1** (pre-existing skip in `test_obligation_scanner.py`, unrelated to R0.2)
- Failed: **0**

Raw output captured at `phase-outputs/test-results/r0-2-pytest-output.txt`.

## New Contract #10 invariant tests (test_anti_instinct_recurrence.py) — 7 tests total, all PASS

| # | Test | Result | Contract #10 invariant |
|---|---|---|---|
| 1 | `test_multimodelswarm_fp_demoted[case_multimodelswarm_fp_case]` | PASS | MultiModelSwarm L207/L211 `stub transport` + `deterministic stub for tests` allowlist-absorbed |
| 2 | `test_multimodelswarm_fp_demoted[case_stub_worker_parallelism_fp_case]` | PASS | MultiModelSwarm L213 `stub-worker parallelism test` allowlist-absorbed |
| 3 | `test_multimodelswarm_fp_demoted[case_module_path_fp_case]` | PASS | Module path `transports/stub.py` allowlist-absorbed |
| 4 | `test_valid_obligation_still_flagged[valid_obligation_case]` | PASS | Anti-regression — `Build stub authentication module` STILL emits HIGH (allowlist did NOT over-broaden) |
| 5 | `test_allowlist_provenance` | PASS | `_ALLOWLIST_PHRASES` declaration cites BUILD-REQUEST §R0 item 2, Contract #10, master:§Recurrence #6 |
| 6 | `test_is_allowlisted_matches_seed_phrases` | PASS | Every phrase in the allowlist is matched by `_is_allowlisted` in roadmap-table context |
| 7 | `test_is_allowlisted_rejects_unrelated_scaffold_prose` | PASS | Allowlist does NOT match unrelated scaffold prose (Build stub auth module, Replace mocked steps, etc.) |

## Existing Layer 1–5 cascade — preserved (no regression)

| Test file | Passed | Skipped | Failed | Notes |
|---|---|---|---|---|
| `test_obligation_scanner.py` | 49 | 1 | 0 | Two Layer 5 H3-context fixtures updated to use `stub handler` instead of `stub transport` to preserve their original Layer 5 demotion contract (Layer 6 allowlist now takes precedence for `stub transport` per Contract #10) |
| `test_obligation_scanner_meta_context.py` | 46 | 0 | 0 | All Layer 1-4 meta-context detection unchanged |
| `test_obligation_scanner_extract_component_context.py` | 6 | 0 | 0 | Component-context extraction unchanged |
| `test_anti_instinct_integration.py` | 26 | 0 | 0 | Pipeline-level integration unchanged |

## Test-fixture rationalizations (Layer 5 ↔ Layer 6 precedence)

Three pre-existing tests in `test_obligation_scanner.py` used the phrase `Stub transport` in fixtures that exercise Layer 5 (H3-subsection demotion) and Fix 1 (tail-section exclusion). With Layer 6 (R0.2 allowlist) now taking precedence — `stub transport` is documented as a permanent fixture, not a scaffolding obligation — those fixtures needed a different SCAFFOLD-term phrase to keep their intended demotion paths reachable:

| Test | Before | After | Reason |
|---|---|---|---|
| `test_layer5_risk_assessment_h3_demotes_scaffold_to_medium` | `Stub transport drifts from real semantics` | `Stub handler drifts from real semantics` | Allowlist would absorb before Layer 5 fires |
| `test_layer5_h3_context_resets_at_next_h2_milestone` (M2 row) | `Stub transport drifts` | `Stub handler drifts` | Same |
| `test_fix1_tail_section_excluded` | `Stub transport retained as mitigation…` | `Stub handler retained as mitigation…` | Allowlist would absorb before tail-section logic engages; test was passing for the wrong reason |

These edits PRESERVE the original test intent (verifying Layer 5 / tail-section behaviour) while making Layer 6 precedence explicit. The new `test_anti_instinct_recurrence.py` separately covers the Layer 6 allowlist contract.

## Wider regression check — `uv run pytest tests/roadmap/ -q`

Result: **1734 passed, 13 skipped, 12 failed**. The 12 failures are **pre-existing** on this branch — confirmed by re-running with my changes stashed:

- `test_models.py::TestRoadmapConfig::test_default_agents` (pre-existing — branch-level default-agent shape changes)
- `test_gates_data.py::TestGateInstances::test_merge_gate_has_seven_semantic_checks` (pre-existing — R0.1 added Contract #9 semantic check, taking the count from 7 to 8; this test predates R0.1)
- `test_pipeline_integration.py` E2E (pre-existing — step count expectations differ; broader rewrite work)
- `test_integration_v5_pipeline.py` (pre-existing — v2.24 pipeline structural changes)
- `test_validate_unit.py::test_default_agents_two` (pre-existing — default agent expectations)
- `test_cli_contract.py::TestAgentsParsing::test_default_agents_when_not_provided` (pre-existing)
- `test_executor.py::TestIntegrationMockSubprocess::test_full_pipeline_all_pass` (pre-existing)
- `test_eval_gate_rejection.py::TestAllGatesPass::test_passing_fixture_passes[merge-gate6]` (pre-existing — likely related to the R0.1 added Contract #9 check)

None reference `obligation_scanner` / `_ALLOWLIST_PHRASES` / Layer 6 / Contract #10. No new failures introduced by R0.2.

## Contract #10 satisfaction assertion

- [x] **≥3 known-false-positive fixtures from documented historical recurrences** — 3 FP fixtures (multimodelswarm_fp_case, stub_worker_parallelism_fp_case, module_path_fp_case), each tracing to verbatim phrases in MultiModelSwarm halt artifacts + BUILD-REQUEST §R0 item 2.
- [x] **1 valid-obligation fixture (anti-regression guard)** — `valid_obligation_case.md` asserts `Build stub authentication module` STILL emits HIGH undischarged.
- [x] **Provenance comment block** — `_ALLOWLIST_PHRASES` declaration cites BUILD-REQUEST §R0 item 2, Contract #10, master:§Recurrence #6; enforced by `test_allowlist_provenance`.
- [x] **Layer 1-5 cascade preserved** — 134/135 tests in obligation_scanner suites pass (1 skip pre-existing).
- [x] **No new `return True` fragility stubs** — Contract #5 unchanged; `_is_allowlisted` returns a substring-match boolean derived from real data.

**Status:** Step 3.6 complete. Proceeding to Step 3.7 (lint + format).
