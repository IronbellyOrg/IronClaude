# Agent D1 Coverage Report — Domain: wiring_e2e_tests

**Agent**: D1
**Domain**: wiring_e2e_tests
**Spec**: v3.3-requirements-spec.md
**Roadmap**: v3.3-TurnLedger-Validation/roadmap.md
**Date**: 2026-03-23

---

## Coverage Assessments

### REQ-001: Goal — every wiring point has ≥1 E2E test exercising real production code
- Spec source: v3.3-requirements-spec.md § FR-1 (preamble)
- Spec text: "Every wiring point from the brainstorm test matrix has at least one E2E test that exercises the real production code path."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2, §2A header and Executive Summary
  - Roadmap text: "Write all E2E tests covering wiring points, TurnLedger lifecycle, gate modes, and remaining QA gaps." and "All required wiring points are reachable and exercised (FR-1, SC-1)"
- Confidence: HIGH

---

### REQ-002: Constraint — no mocking gate functions; _subprocess_factory only acceptable injection
- Spec source: v3.3-requirements-spec.md § FR-1 (preamble constraint)
- Spec text: "Tests MUST NOT mock gate functions or core orchestration logic. The `_subprocess_factory` injection point in `execute_phase_tasks()` is acceptable because it replaces the external `claude` binary, not internal logic."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 4 §4.2; Executive Summary §Architectural Priorities #1; Appendix A §A.1
  - Roadmap text (Phase 4.2): "Grep-audit: confirm no `mock.patch` on gate functions or orchestration logic across all v3.3 test files"; (Exec Summary): "satisfy NFR-1 by testing real orchestration and gate behavior end-to-end, limiting injection to `_subprocess_factory` only"; (A.1): "Sole allowed injection seam under NFR-1; all test harnesses must standardize on it."
- Confidence: HIGH

---

### REQ-003: FR-1.1 — TurnLedger construction (initial_budget, reimbursement_rate, constructed before phase loop)
- Spec source: v3.3-requirements-spec.md § FR-1.1
- Spec text: "Invoke `execute_sprint()` with a minimal config. Assert: `ledger.initial_budget == config.max_turns * len(config.active_phases)`, `ledger.reimbursement_rate == 0.8`, Ledger is constructed BEFORE the phase loop begins"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.1
  - Roadmap text: "FR-1.1 – FR-1.4 | 4 tests: Construction validation for `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, `SprintGatePolicy`"
- Confidence: HIGH

---

### REQ-004: FR-1.2 — ShadowGateMetrics constructed before phase loop
- Spec source: v3.3-requirements-spec.md § FR-1.2
- Spec text: "Assert `ShadowGateMetrics()` is constructed before phase loop."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.1
  - Roadmap text: "FR-1.1 – FR-1.4 | 4 tests: Construction validation for `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, `SprintGatePolicy`"
- Confidence: HIGH

---

### REQ-005: FR-1.3 — DeferredRemediationLog constructed with persist_path under results_dir
- Spec source: v3.3-requirements-spec.md § FR-1.3
- Spec text: "Assert `DeferredRemediationLog` is constructed with `persist_path` under `results_dir`."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.1
  - Roadmap text: "FR-1.1 – FR-1.4 | 4 tests: Construction validation for `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, `SprintGatePolicy`"
- Confidence: HIGH

---

### REQ-006: FR-1.4 — SprintGatePolicy(config) constructed with correct config
- Spec source: v3.3-requirements-spec.md § FR-1.4
- Spec text: "Assert `SprintGatePolicy(config)` is constructed and receives the correct config."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.1
  - Roadmap text: "FR-1.1 – FR-1.4 | 4 tests: Construction validation for `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, `SprintGatePolicy`"
- Confidence: HIGH

---

### REQ-007: FR-1.5 — Phase delegation task-inventory path
- Spec source: v3.3-requirements-spec.md § FR-1.5
- Spec text: "Create a phase file with `### T01.01` headings. Assert `execute_phase_tasks()` is called (not ClaudeProcess). Verification: Task results contain expected task IDs from the inventory."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.2; Appendix A §A.2
  - Roadmap text (2A.2): "FR-1.5 – FR-1.6 | 2 tests: Phase delegation — task-inventory path vs freeform fallback"; (A.2): "`execute_phase_tasks()` task-inventory path for phases with `### T01.01` headings; `ClaudeProcess` freeform fallback path"
- Confidence: HIGH

---

### REQ-008: FR-1.6 — Phase delegation freeform fallback path
- Spec source: v3.3-requirements-spec.md § FR-1.6
- Spec text: "Create a phase file WITHOUT task headings. Assert ClaudeProcess subprocess is spawned."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.2; Appendix A §A.2
  - Roadmap text: "FR-1.5 – FR-1.6 | 2 tests: Phase delegation — task-inventory path vs freeform fallback"
- Confidence: HIGH

---

### REQ-009: FR-1.7 — run_post_phase_wiring_hook() called on BOTH paths
- Spec source: v3.3-requirements-spec.md § FR-1.7
- Spec text: "Verify `run_post_phase_wiring_hook()` is called for: Per-task phases (executor.py:1199-1204); Per-phase/ClaudeProcess phases (executor.py:1407-1412). Verification: Wiring logger emits expected log entries for both paths."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.3; Appendix A §A.3
  - Roadmap text (2A.3): "FR-1.7 | 2 tests: Post-phase wiring hook fires on per-task and per-phase/ClaudeProcess paths"; (A.3): "fires on per-task and per-phase/ClaudeProcess paths"
- Confidence: HIGH

---

### REQ-010: FR-1.21 — check_wiring_report() wrapper called in wiring analysis flow
- Spec source: v3.3-requirements-spec.md § FR-1.21
- Spec text: "Assert `check_wiring_report()` wrapper (wiring_gate.py:1079) is called within the wiring analysis flow. Assert: `run_post_phase_wiring_hook()` or `run_post_task_wiring_hook()` invokes `check_wiring_report()` as part of wiring analysis. Assert: the wrapper delegates to the underlying analysis and returns a valid report structure."
- Status: MISSING
- Match quality: NONE
- Evidence:
  - Roadmap location: ABSENT
  - Roadmap text: ABSENT. The task list in 2A covers FR-1.1 through FR-1.18 only. Task 2A.1 covers FR-1.1–FR-1.4; 2A.2 covers FR-1.5–FR-1.6; 2A.3 covers FR-1.7; 2A.4 covers FR-1.8; 2A.5 covers FR-1.9–FR-1.10; 2A.6 covers FR-1.11; 2A.7 covers FR-1.12; 2A.8 covers FR-1.13; 2A.9 covers FR-1.14; 2A.10 covers FR-1.15–FR-1.16; 2A.11 covers FR-1.17; 2A.12 covers FR-1.18. FR-1.21 is not listed anywhere in the roadmap. Neither the subtotal note ("~21 tests covering SC-1") nor any other roadmap section references `check_wiring_report()` or FR-1.21 explicitly.
- Finding:
  - Severity: HIGH
  - Gap description: FR-1.21 (`check_wiring_report()` wrapper validation) is entirely absent from the 2A task table and from all other phases. The roadmap's 2A subtotal claims "~21 tests covering SC-1" but the 12 listed tasks (2A.1–2A.12) can only produce ~21 tests if FR-1.14's "3 tests" are counted (2A.9 lists "FR-1.14, FR-1.14a–c | 3 tests"). There is no task allocated to FR-1.21.
  - Impact: `check_wiring_report()` wrapper at wiring_gate.py:1079 is a distinct, named wiring point in the spec. Its absence from the roadmap means no test will verify the delegation chain from the wiring hooks into `check_wiring_report()` and back to a valid report structure. SC-1 claims ≥20 wiring E2E tests; without FR-1.21 the count depends on whether 2A.9's 3 tests are included. Even if SC-1 passes numerically, a named wiring point is not exercised.
  - Recommended correction: Add task 2A.13 to Phase 2A: "FR-1.21 | 1 test: Assert `check_wiring_report()` wrapper is invoked from `run_post_phase_wiring_hook()` / `run_post_task_wiring_hook()`; verify wrapper delegates to analysis and returns valid report structure." Update 2A subtotal accordingly.
- Confidence: HIGH

---

### REQ-011: FR-1.8 — anti-instinct hook return type tuple
- Spec source: v3.3-requirements-spec.md § FR-1.8
- Spec text: "Assert `run_post_task_anti_instinct_hook()` returns `tuple[TaskResult, TrailingGateResult | None]`, not a bare `TaskResult`."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.4; Appendix A §A.4
  - Roadmap text (2A.4): "FR-1.8 | 1 test: Anti-instinct hook return type is `tuple[TaskResult, TrailingGateResult | None]`"; (A.4): "Evaluates `TrailingGateResult`, returns `tuple[TaskResult, TrailingGateResult | None]`"
- Confidence: HIGH

---

### REQ-012: FR-1.9 — gate result accumulation across all phases
- Spec source: v3.3-requirements-spec.md § FR-1.9
- Spec text: "Run a sprint with N phases (mix of task-inventory and freeform). Assert `all_gate_results` contains results from ALL phases."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.5
  - Roadmap text: "FR-1.9 – FR-1.10 | 2 tests: Gate result accumulation across phases; failed gate → remediation log"
- Confidence: HIGH

---

### REQ-013: FR-1.10 — failed gate → remediation log
- Spec source: v3.3-requirements-spec.md § FR-1.10
- Spec text: "Configure `gate_rollout_mode=\"full\"`, inject a failing gate. Assert failed `TrailingGateResult` is appended to `remediation_log`."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.5; Appendix A §A.9
  - Roadmap text (2A.5): "FR-1.9 – FR-1.10 | 2 tests: Gate result accumulation across phases; failed gate → remediation log"; (A.9): "Fed by `_log_shadow_findings_to_remediation_log()` and blocking remediation failures"
- Confidence: HIGH

---

### REQ-014: FR-1.11 — KPI report generated with wiring KPI fields
- Spec source: v3.3-requirements-spec.md § FR-1.11
- Spec text: "Run a sprint to completion. Assert: `build_kpi_report()` is called with `all_gate_results`, `remediation_log`, `ledger`; Report file `gate-kpi-report.md` is written to `results_dir`; Report content includes wiring KPI fields: `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost`"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.6; Success Criteria Matrix §SC-5
  - Roadmap text (2A.6): "FR-1.11 | 1 test: KPI report generation with wiring KPI fields"; (SC-5 validation): "KPI wiring fields match expected | Integration test field comparison in FR-1.11 test"
- Confidence: HIGH

---

### REQ-015: FR-1.12 — wiring mode resolution via _resolve_wiring_mode()
- Spec source: v3.3-requirements-spec.md § FR-1.12
- Spec text: "Assert `_resolve_wiring_mode()` is called within `run_post_task_wiring_hook()`, NOT `config.wiring_gate_mode` used directly."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.7; Appendix A §A.5
  - Roadmap text (2A.7): "FR-1.12 | 1 test: Wiring mode resolution via `_resolve_wiring_mode()`"; (A.5): "Authoritative strategy selector; direct config reads are architectural drift."
- Confidence: HIGH

---

### REQ-016: FR-1.13 — shadow findings → remediation log with [shadow] prefix
- Spec source: v3.3-requirements-spec.md § FR-1.13
- Spec text: "Configure `wiring_gate_mode=\"shadow\"`, inject findings. Assert `_log_shadow_findings_to_remediation_log()` creates synthetic `TrailingGateResult` entries with `[shadow]` prefix."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.8; Appendix A §A.9
  - Roadmap text (2A.8): "FR-1.13 | 1 test: Shadow findings → remediation log with `[shadow]` prefix"
- Confidence: HIGH

---

### REQ-017: FR-1.14 — BLOCKING remediation lifecycle (format→debit→recheck→restore/fail)
- Spec source: v3.3-requirements-spec.md § FR-1.14
- Spec text: "Configure `wiring_gate_mode=\"full\"`, inject blocking findings with sufficient budget. Assert full cycle: 1. `_format_wiring_failure()` produces non-empty prompt; 2. `ledger.debit(config.remediation_cost)` is called; 3. `_recheck_wiring()` is called; 4. On recheck pass: task status restored to PASS, wiring turns credited; 5. On recheck fail: task status remains FAIL"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.9
  - Roadmap text: "FR-1.14, FR-1.14a–c | 3 tests: BLOCKING remediation lifecycle: format → debit → recheck → restore/fail"
- Confidence: HIGH

---

### REQ-018: FR-1.15 — DeviationRegistry.load_or_create() 3 positional args
- Spec source: v3.3-requirements-spec.md § FR-1.15
- Spec text: "Assert `DeviationRegistry.load_or_create()` receives exactly 3 positional args: `(path, release_id, spec_hash)`."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.10; Appendix A §A.8
  - Roadmap text (2A.10): "FR-1.15 – FR-1.16 | 2 tests: Convergence registry 3-arg construction; `merge_findings()` 3-arg call"; (A.8): "`(path, release_id, spec_hash)` — 3-arg construction"
- Confidence: HIGH

---

### REQ-019: FR-1.16 — registry.merge_findings() 3 args
- Spec source: v3.3-requirements-spec.md § FR-1.16
- Spec text: "Assert `registry.merge_findings()` receives `(structural_list, semantic_list, run_number)` — 3 args, correct positions."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.10; Appendix A §A.7
  - Roadmap text (2A.10): "FR-1.15 – FR-1.16 | 2 tests: Convergence registry 3-arg construction; `merge_findings()` 3-arg call"; (A.7): "Structural findings list, semantic findings list, `run_number` (3-arg signature)"
- Confidence: HIGH

---

### REQ-020: FR-1.17 — _run_remediation() dict→Finding conversion
- Spec source: v3.3-requirements-spec.md § FR-1.17
- Spec text: "Assert `_run_remediation()` converts registry dicts to `Finding` objects without `AttributeError`."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.11
  - Roadmap text: "FR-1.17 | 1 test: `_run_remediation()` dict-to-Finding conversion without AttributeError"
- Confidence: HIGH

---

### REQ-021: FR-1.18 — TurnLedger budget = 61
- Spec source: v3.3-requirements-spec.md § FR-1.18
- Spec text: "Assert `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` uses 61 (not 46)."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2 §2A, task 2A.12
  - Roadmap text: "FR-1.18 | 1 test: `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` uses 61"
- Confidence: HIGH

---

### REQ-022: FR-1.19 — SHADOW_GRACE_INFINITE constant and behavior
- Spec source: v3.3-requirements-spec.md § FR-1.19
- Spec text: "Assert `SHADOW_GRACE_INFINITE` constant value and its effect on shadow mode grace period logic. Assert: `SHADOW_GRACE_INFINITE` is defined in models.py with expected sentinel value. Assert: when `wiring_gate_grace_period` is set to `SHADOW_GRACE_INFINITE`, shadow mode never exits grace period (wiring gate always credits back)."
- Status: MISSING
- Match quality: NONE
- Evidence:
  - Roadmap location: ABSENT
  - Roadmap text: ABSENT. The 2A task table lists tasks 2A.1 through 2A.12. Task 2A.12 explicitly covers FR-1.18 (budget constant). There is no task 2A.13 or any other roadmap entry referencing FR-1.19, `SHADOW_GRACE_INFINITE`, or models.py:293. The 2A subtotal line reads "~21 tests covering SC-1" but the 12 tasks as written can account for at most ~21 tests without FR-1.19 (2A.9 alone counts as 3). FR-1.19 is entirely unaddressed.
- Finding:
  - Severity: HIGH
  - Gap description: FR-1.19 is absent from all roadmap phases. The `SHADOW_GRACE_INFINITE` constant and its behavioral effect on shadow mode grace period are not validated anywhere in the roadmap's test plan. This is a previously identified missing requirement (noted in agent instructions as "FR-1.19 MISSING in prior run").
  - Impact: A sentinel constant that governs whether shadow mode ever exits its grace period is not tested. If the constant is incorrect or the grace-period logic is broken, shadow mode will silently behave incorrectly. The gap is invisible to the test suite.
  - Recommended correction: Add task 2A.13 (or extend 2A.12) to Phase 2A: "FR-1.19 | 2 tests: (a) Assert `SHADOW_GRACE_INFINITE` is defined in models.py with expected sentinel value; (b) Assert when `wiring_gate_grace_period == SHADOW_GRACE_INFINITE`, shadow mode never exits grace period and wiring gate always credits back." Update 2A subtotal.
- Confidence: HIGH

---

### REQ-023: FR-1.20 — __post_init__() config derivation
- Spec source: v3.3-requirements-spec.md § FR-1.20
- Spec text: "Assert `__post_init__()` correctly derives sprint config fields from input config. Assert: derived fields (`wiring_gate_enabled`, `wiring_gate_grace_period`, `wiring_analyses_count`) are computed from base config values. Assert: invalid or missing base config values produce sensible defaults."
- Status: MISSING
- Match quality: NONE
- Evidence:
  - Roadmap location: ABSENT
  - Roadmap text: ABSENT. The 2A task table covers FR-1.1 through FR-1.18 via tasks 2A.1–2A.12. There is no task referencing FR-1.20, `__post_init__()`, or models.py:338-384. This is confirmed by exhaustive inspection: 2A.1 (FR-1.1–1.4), 2A.2 (FR-1.5–1.6), 2A.3 (FR-1.7), 2A.4 (FR-1.8), 2A.5 (FR-1.9–1.10), 2A.6 (FR-1.11), 2A.7 (FR-1.12), 2A.8 (FR-1.13), 2A.9 (FR-1.14), 2A.10 (FR-1.15–1.16), 2A.11 (FR-1.17), 2A.12 (FR-1.18). FR-1.19, FR-1.20, and FR-1.21 are all absent.
- Finding:
  - Severity: HIGH
  - Gap description: FR-1.20 is absent from all roadmap phases. The `__post_init__()` derivation of `wiring_gate_enabled`, `wiring_gate_grace_period`, and `wiring_analyses_count` from base config values — including sensible-defaults behavior on missing/invalid input — is not tested. This is a previously identified missing requirement (noted in agent instructions as "FR-1.20 MISSING in prior run").
  - Impact: `__post_init__()` at models.py:338-384 is listed in the spec's verified-wired constructs table. If this derivation logic is wrong, every downstream gate behavior that depends on these derived fields will malfunction silently. No test will detect a regression here.
  - Recommended correction: Add task 2A.14 to Phase 2A: "FR-1.20 | 2 tests: (a) Assert `__post_init__()` correctly computes `wiring_gate_enabled`, `wiring_gate_grace_period`, `wiring_analyses_count` from valid base config values; (b) Assert invalid/missing base config values produce sensible defaults without exception." Update 2A subtotal.
- Confidence: HIGH

---

### REQ-SC1: SC-1 — ≥20 wiring point E2E tests
- Spec source: v3.3-requirements-spec.md § Success Criteria
- Spec text: "All 20+ wiring points have ≥1 E2E test | Test count ≥ 20, mapped to FR-1"
- Status: PARTIAL
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Phase 2 §2A (subtotal); Success Criteria Matrix §SC-1
  - Roadmap text (2A subtotal): "~21 tests covering SC-1"; (SC-1 validation): "Count tests in `test_wiring_points_e2e.py` mapped to FR-1 sub-IDs"
- Finding:
  - Severity: HIGH
  - Gap description: The roadmap's 2A task list explicitly covers FR-1.1 through FR-1.18 (12 tasks, ~21 tests as counted by the roadmap). However, FR-1.19, FR-1.20, and FR-1.21 are all absent. These are three additional distinct wiring points identified in the spec. The roadmap's claim of "~21 tests" may be numerically plausible if 2A.9 generates 3 tests for FR-1.14 sub-variants — but it relies on counting those sub-variants while omitting three entire FR sub-items. The spec's preamble states "FR-1.1–FR-1.18: Wiring point E2E tests (20 tests)" in the phased plan, which would include FR-1.21 (noted as a late addition), FR-1.19, and FR-1.20 as required additions. SC-1 says "20+ wiring points", but the roadmap leaves FR-1.19, FR-1.20, and FR-1.21 uncovered.
  - Impact: SC-1 validation will pass a count check on the roadmap's test list without covering 3 specified wiring points. Third-party audit against FR-1.19/1.20/1.21 will find no test records.
  - Recommended correction: Add tasks 2A.13, 2A.14, 2A.15 (or equivalent) covering FR-1.19, FR-1.20, FR-1.21 respectively. Update the SC-1 validation to enumerate all covered FR-1.x IDs explicitly, not just a count.
- Confidence: HIGH

---

### REQ-SC5: SC-5 — KPI field VALUES correct (not just present)
- Spec source: v3.3-requirements-spec.md § Success Criteria
- Spec text: "KPI report accuracy validated | Integration test proves field VALUES are correct (not just present): `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost` match computed expectations from test inputs"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Success Criteria Matrix §SC-5
  - Roadmap text: "SC-5 | KPI wiring fields match expected | Integration test field comparison in FR-1.11 test | 2 | Yes"
- Note: The roadmap says "field comparison" which implies value-level comparison rather than presence-only checks, and it cross-references the FR-1.11 test. The FR-1.11 roadmap task (2A.6) says "KPI report generation with wiring KPI fields" — this is slightly less explicit than the spec's "field VALUES are correct (not just present)" language. However, the SC-5 row in the Success Criteria Matrix adds "match expected" precision, and when read together with the FR-1.11 test description, constitutes semantic coverage of the value-correctness requirement.
- Confidence: MEDIUM

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total requirements assessed | 25 |
| COVERED | 20 |
| PARTIAL | 1 (REQ-SC1) |
| MISSING | 3 (REQ-010/FR-1.21, REQ-022/FR-1.19, REQ-023/FR-1.20) |
| CONFLICTING | 0 |
| IMPLICIT | 0 |

---

## Critical Findings Summary

Three requirements are MISSING from the roadmap, all in Phase 2A:

1. **REQ-010 / FR-1.21** (HIGH): `check_wiring_report()` wrapper call validation — no roadmap task. The 2A table jumps from FR-1.18 (2A.12) to a subtotal with no entry for FR-1.21. This was identified as missing in the prior validation run and remains unaddressed.

2. **REQ-022 / FR-1.19** (HIGH): `SHADOW_GRACE_INFINITE` constant and grace-period behavior — no roadmap task. The constant at models.py:293 and its effect on shadow mode are entirely absent from the 2A task list. Previously identified as missing, still absent.

3. **REQ-023 / FR-1.20** (HIGH): `__post_init__()` config derivation — no roadmap task. The derivation of `wiring_gate_enabled`, `wiring_gate_grace_period`, and `wiring_analyses_count` from base config values (including defaults for invalid input) at models.py:338-384 is not tested. Previously identified as missing, still absent.

**Structural pattern**: All three gaps are sequentially numbered FR-1.19, FR-1.20, and FR-1.21. The roadmap's 2A task list was constructed from FR-1.1–FR-1.18 and was not updated when these three requirements were added to the spec. The subtotal claim of "~21 tests" is therefore misleading — it counts sub-variants of FR-1.14 while leaving three distinct wiring points untested.

**REQ-SC1 (SC-1)** is PARTIAL because all three MISSING requirements are wiring-point E2E tests that should count toward the ≥20 threshold. The roadmap may pass a numerical check on count alone while leaving named wiring points uncovered.

**REQ-SC5 (SC-5)** is COVERED, but confidence is MEDIUM because the 2A.6 task description ("KPI report generation with wiring KPI fields") does not explicitly state value-level correctness. The SC-5 matrix row adds "match expected" language that closes the gap, but an implementer reading only the task description could stop at presence checks.

**No-mocking constraint (REQ-002)** is verified by Phase 4 task 4.2's explicit grep-audit against all v3.3 test files.
