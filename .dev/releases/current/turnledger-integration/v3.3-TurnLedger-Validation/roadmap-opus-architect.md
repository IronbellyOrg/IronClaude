---
spec_source: v3.3-requirements-spec.md
complexity_score: 0.82
primary_persona: architect
---

# v3.3 TurnLedger Validation — Project Roadmap

## Executive Summary

v3.3 is a **validation-focused release** that proves the wiring correctness of the TurnLedger economic model, gate rollout modes, and convergence pipeline built across v3.0–v3.2. The scope is primarily test authoring (50+ E2E scenarios) with three targeted production code changes: a 0-files-analyzed assertion fix (FR-5.1), an impl-vs-spec fidelity checker (FR-5.2), and a new AST-based reachability eval framework (FR-4). All tests must exercise real production code paths — the only acceptable injection point is `_subprocess_factory`.

**Key architectural concerns**: The reachability analyzer (FR-4) is the only novel component and carries the highest technical risk. The E2E test volume is large but structurally repetitive — tests follow a common pattern of config → execute → assert wiring state. The audit trail infrastructure (FR-7) is cross-cutting and must be established early as all tests depend on it.

---

## Phased Implementation Plan

### Phase 1: Foundation — Audit Trail + Reachability Analyzer

**Duration**: ~3 days
**Objective**: Build the two cross-cutting infrastructure pieces that all subsequent phases depend on.

#### 1A: Audit Trail Infrastructure (FR-7)

| Task | Requirement | Deliverable |
|------|-------------|-------------|
| 1A.1 | FR-7.1 | JSONL audit record writer — `tests/audit-trail/audit_writer.py` with 8-field schema: `test_id`, `spec_ref`, `timestamp`, `assertion_type`, `inputs`, `observed`, `expected`, `verdict`, `evidence` |
| 1A.2 | FR-7.3 | `audit_trail` pytest fixture — session-scoped, opens JSONL in `results_dir`, provides `record()` method, auto-flushes on session end |
| 1A.3 | FR-7.3 | Summary report generation at session end: total/passed/failed/wiring coverage |
| 1A.4 | FR-7.2 | Verification test: confirm JSONL output meets 4 third-party verifiability properties (real timestamps, spec-traced, runtime observations, explicit verdict) |

**Integration point**: The `audit_trail` fixture registers as a `conftest.py` plugin at `tests/v3.3/conftest.py` and `tests/roadmap/conftest.py`. All subsequent test phases import and use this fixture.

#### 1B: AST Reachability Analyzer (FR-4)

| Task | Requirement | Deliverable |
|------|-------------|-------------|
| 1B.1 | FR-4.1 | Wiring manifest YAML schema — `entry_points` section listing callable entry points, `required_reachable` section listing target symbols with spec references |
| 1B.2 | FR-4.2 | AST call-chain analyzer module — `src/superclaude/cli/audit/reachability.py`: `ast.parse()` → call graph construction → BFS/DFS reachability; cross-module import resolution; lazy import handling |
| 1B.3 | FR-4.2 | Documented limitations in module docstring: dynamic dispatch (`getattr`, `**kwargs`) → false negatives; `TYPE_CHECKING` conditionals excluded; lazy imports inside functions included (NFR-6) |
| 1B.4 | FR-4.1 | Initial wiring manifest YAML for executor.py entry points — `tests/v3.3/wiring_manifest.yaml` |
| 1B.5 | FR-4.4 | Unit tests for AST analyzer in isolation — `tests/v3.3/test_reachability_eval.py` |

**Milestone 1**: Audit trail fixture produces valid JSONL; AST analyzer resolves cross-module imports and detects reachability for known-good and known-bad cases.

---

### Phase 2: Core E2E Test Suites (FR-1, FR-2, FR-3, FR-6)

**Duration**: ~5 days
**Objective**: Write all E2E tests covering wiring points, TurnLedger lifecycle, gate modes, and remaining QA gaps. This is the largest phase by volume.
**Hard dependency**: Phase 1A (audit trail fixture must exist).

#### 2A: Wiring Point E2E Tests (FR-1)

**File**: `tests/v3.3/test_wiring_points_e2e.py`

| Task | Requirements Covered | Test Count |
|------|---------------------|------------|
| 2A.1 | FR-1.1 – FR-1.4 | 4 tests: Construction validation for `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, `SprintGatePolicy` |
| 2A.2 | FR-1.5 – FR-1.6 | 2 tests: Phase delegation — task-inventory path vs freeform fallback |
| 2A.3 | FR-1.7 | 2 tests: Post-phase wiring hook fires on per-task and per-phase/ClaudeProcess paths |
| 2A.4 | FR-1.8 | 1 test: Anti-instinct hook return type is `tuple[TaskResult, TrailingGateResult | None]` |
| 2A.5 | FR-1.9 – FR-1.10 | 2 tests: Gate result accumulation across phases; failed gate → remediation log |
| 2A.6 | FR-1.11 | 1 test: KPI report generation with wiring KPI fields |
| 2A.7 | FR-1.12 | 1 test: Wiring mode resolution via `_resolve_wiring_mode()` |
| 2A.8 | FR-1.13 | 1 test: Shadow findings → remediation log with `[shadow]` prefix |
| 2A.9 | FR-1.14, FR-1.14a–c | 3 tests: BLOCKING remediation lifecycle: format → debit → recheck → restore/fail |
| 2A.10 | FR-1.15 – FR-1.16 | 2 tests: Convergence registry 3-arg construction; `merge_findings()` 3-arg call |
| 2A.11 | FR-1.17 | 1 test: `_run_remediation()` dict-to-Finding conversion without AttributeError |
| 2A.12 | FR-1.18 | 1 test: `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` uses 61 |

**Subtotal**: ~21 tests covering SC-1.

##### Dispatch/Wiring Mechanisms Enumerated (FR-1)

- **Named Artifact**: `_subprocess_factory` injection point in `execute_phase_tasks()`
  - **Wired Components**: Test harness injects fake subprocess returning controlled exit codes
  - **Owning Phase**: Exists in production code; Phase 2 tests wire test doubles into it
  - **Cross-Reference**: All FR-1, FR-2, FR-3 tests consume this mechanism

- **Named Artifact**: `run_post_phase_wiring_hook()` dispatch (executor.py:735)
  - **Wired Components**: Calls `run_wiring_analysis()` → `analyze_unwired_callables()` + `analyze_orphan_modules()` + `analyze_registries()`
  - **Owning Phase**: Existing production code; Phase 2A.3 validates it fires on both paths
  - **Cross-Reference**: FR-1.7, FR-3.1a–d consume; Phase 3 FR-4.3 adds reachability gate into this chain

- **Named Artifact**: `run_post_task_anti_instinct_hook()` dispatch (executor.py:787)
  - **Wired Components**: Evaluates `TrailingGateResult`, returns `tuple[TaskResult, TrailingGateResult | None]`
  - **Owning Phase**: Existing production code; Phase 2A.4 validates return type
  - **Cross-Reference**: FR-1.8, FR-3.1a–d consume

- **Named Artifact**: `_resolve_wiring_mode()` strategy resolver (executor.py:421)
  - **Wired Components**: Reads `config.wiring_gate_mode`, applies override logic
  - **Owning Phase**: Existing production code; Phase 2A.7 validates it's called instead of raw config access
  - **Cross-Reference**: FR-1.12, FR-3.1a–d depend on correct resolution

- **Named Artifact**: `_run_checkers()` checker registry (convergence/executor.py:594)
  - **Wired Components**: Structural checker, semantic checker; FR-5.2 adds impl-vs-spec checker
  - **Owning Phase**: Phase 3 (FR-5.2) adds new checker; Phase 2A.10 validates existing merge_findings call
  - **Cross-Reference**: FR-1.15, FR-1.16, FR-5.2

- **Named Artifact**: `DeferredRemediationLog` accumulator (trailing_gate.py:494)
  - **Wired Components**: Fed by `_log_shadow_findings_to_remediation_log()`, blocking remediation failures
  - **Owning Phase**: Existing production code; Phase 2A.5 and 2A.8 validate writes
  - **Cross-Reference**: FR-1.10, FR-1.13, FR-3.1b–d

#### 2B: TurnLedger Lifecycle Tests (FR-2)

**File**: `tests/v3.3/test_turnledger_lifecycle.py`

| Task | Requirement | Description |
|------|-------------|-------------|
| 2B.1 | FR-2.1 | Convergence path (v3.05): `execute_fidelity_with_convergence()` E2E — debit `CHECKER_COST` → run checkers → credit `CONVERGENCE_PASS_CREDIT` → `reimburse_for_progress()`; budget_snapshot recorded |
| 2B.2 | FR-2.2 | Sprint per-task path (v3.1): pre-debit `minimum_allocation` → subprocess → reconcile; post-task hooks fire with ledger |
| 2B.3 | FR-2.3 | Sprint per-phase path (v3.2): `debit_wiring()` → analysis → `credit_wiring()` on non-blocking; `wiring_analyses_count` incremented |
| 2B.4 | FR-2.4 | Cross-path coherence: mixed task-inventory + freeform phases; `available() = initial_budget - consumed + reimbursed` at every checkpoint |

**Subtotal**: 4 tests covering SC-2.

##### Dispatch/Wiring Mechanisms Enumerated (FR-2)

- **Named Artifact**: `TurnLedger.debit_wiring()` / `credit_wiring()` pair (models.py:595–624)
  - **Wired Components**: Called by `run_post_phase_wiring_hook()` for per-phase path
  - **Owning Phase**: Existing production code; Phase 2B.3 validates the full cycle
  - **Cross-Reference**: FR-2.3, FR-3.1b–d budget state assertions

- **Named Artifact**: `reimburse_for_progress()` (convergence.py:42)
  - **Wired Components**: Called after successful convergence run
  - **Owning Phase**: Existing production code; Phase 2B.1 validates integration
  - **Cross-Reference**: FR-2.1, FR-2.4

#### 2C: Gate Rollout Mode Matrix (FR-3)

**File**: `tests/v3.3/test_gate_rollout_modes.py`

| Task | Requirement | Test Count |
|------|-------------|------------|
| 2C.1 | FR-3.1a – FR-3.1d | 8 tests: 4 modes × 2 paths (anti-instinct + wiring). Each verifies: `TaskStatus`/`GateOutcome`, `TurnLedger` state, `DeferredRemediationLog` entries, `ShadowGateMetrics` recording |
| 2C.2 | FR-3.2a – FR-3.2d | 4 tests: Budget exhaustion scenarios — before task launch, before wiring, before remediation, mid-convergence |
| 2C.3 | FR-3.3 | 1 test: Interrupted sprint → KPI report written, remediation log persisted, outcome = INTERRUPTED |

**Subtotal**: 13 tests covering SC-3, SC-6.

#### 2D: Remaining QA Gaps (FR-6)

| Task | Requirement | File | Test Count |
|------|-------------|------|------------|
| 2D.1 | FR-6.1 T07 | `tests/roadmap/test_convergence_wiring.py` | Extend existing 7 tests (verify already present, add any missing) |
| 2D.2 | FR-6.1 T11 | `tests/roadmap/test_convergence_e2e.py` | Extend existing SC-1–SC-6 tests |
| 2D.3 | FR-6.1 T12 | `tests/roadmap/test_convergence_e2e.py` | Add smoke test for convergence path |
| 2D.4 | FR-6.1 T14 | `docs/generated/` | Regenerate wiring-verification artifact + validate |
| 2D.5 | FR-6.2 T02 | `tests/v3.3/test_wiring_points_e2e.py` | Confirming test for `run_post_phase_wiring_hook()` (may overlap 2A.3) |
| 2D.6 | FR-6.2 T17–T22 | `tests/v3.3/test_integration_regression.py` | Integration + regression suite per spec |

**Subtotal**: ~15 tests covering SC-8.

**Milestone 2**: All E2E tests pass. SC-1 through SC-6, SC-8, SC-12 validated. Audit trail JSONL emitted for every test.

---

### Phase 3: Pipeline Fixes + Reachability Gate Integration (FR-4.3, FR-5)

**Duration**: ~2 days
**Objective**: Ship the three production code changes and integrate the reachability gate.
**Hard dependency**: Phase 1B (AST analyzer), Phase 2 (tests exist to validate fixes).

#### 3A: Production Code Changes

| Task | Requirement | File Modified | Change |
|------|-------------|---------------|--------|
| 3A.1 | FR-5.1 | `src/superclaude/cli/audit/wiring_gate.py` (line 673+) | Add assertion: if `files_analyzed == 0` AND source dir non-empty → return FAIL with `failure_reason` |
| 3A.2 | FR-5.2 | New: `src/superclaude/cli/roadmap/fidelity_checker.py` | Impl-vs-spec fidelity checker: reads spec FRs, searches codebase for function/class name evidence, reports gaps |
| 3A.3 | FR-5.2 | `src/superclaude/cli/roadmap/executor.py` (`_run_checkers()`) | Wire `fidelity_checker` into `_run_checkers()` alongside structural and semantic layers |
| 3A.4 | FR-4.3 | `src/superclaude/cli/audit/reachability.py` | Add `GateCriteria`-compatible interface: reads manifest, runs AST analysis, produces structured PASS/FAIL report |

##### Dispatch/Wiring Mechanisms Enumerated (Phase 3)

- **Named Artifact**: `_run_checkers()` checker registry (convergence/executor.py:594)
  - **Wired Components**: Existing structural + semantic checkers; **Phase 3A.3 adds `fidelity_checker`**
  - **Owning Phase**: Phase 3 (this phase) wires the new checker
  - **Cross-Reference**: Phase 2A.10 validates merge_findings; Phase 4 regression tests validate no breakage

- **Named Artifact**: `GateCriteria` integration for reachability gate
  - **Wired Components**: `reachability.py` analyzer + wiring manifest YAML
  - **Owning Phase**: Phase 1B creates analyzer; **Phase 3A.4 adds GateCriteria interface**
  - **Cross-Reference**: Phase 3B.2 validates gate catches known-bad state (SC-7, SC-9)

- **Named Artifact**: `run_wiring_analysis()` 0-files guard (wiring_gate.py:673+)
  - **Wired Components**: Existing analysis pipeline; **Phase 3A.1 adds early-exit FAIL**
  - **Owning Phase**: Phase 3 (this phase)
  - **Cross-Reference**: Phase 3B.1 validates (SC-10); Phase 4 regression validates no breakage

#### 3B: Validation Tests for Pipeline Fixes

| Task | Requirement | Deliverable |
|------|-------------|-------------|
| 3B.1 | FR-5.1, SC-10 | Test: 0-files-analyzed on non-empty dir → FAIL, not silent PASS |
| 3B.2 | FR-4.4, SC-7, SC-9 | Regression test: remove `run_post_phase_wiring_hook()` call → gate detects gap referencing v3.2-T02 |
| 3B.3 | FR-5.2, SC-11 | Test: impl-vs-spec checker finds gap in synthetic test with missing implementation |

**Milestone 3**: All 3 production fixes shipped. Reachability gate catches intentionally broken wiring. Fidelity checker detects missing implementations. SC-7, SC-9, SC-10, SC-11 validated.

---

### Phase 4: Regression Validation + Final Audit (NFR-3, SC-4)

**Duration**: ~1 day
**Objective**: Full regression sweep, audit trail verification, documentation.
**Hard dependency**: All previous phases complete.

| Task | Requirement | Deliverable |
|------|-------------|-------------|
| 4.1 | NFR-3, SC-4 | Full test suite run: confirm ≥4894 passed, ≤3 pre-existing failures, 0 new regressions |
| 4.2 | NFR-1 | Grep-audit: confirm no `mock.patch` on gate functions or orchestration logic across all v3.3 test files |
| 4.3 | FR-7.2, SC-12 | Manual review of JSONL audit trail: confirm third-party verifiability properties |
| 4.4 | NFR-5 | Validate wiring manifest completeness: every known wiring point from FR-1 has a manifest entry |
| 4.5 | — | Generate final wiring-verification artifact (FR-6.1 T14) |
| 4.6 | — | Update `docs/memory/solutions_learned.jsonl` with v3.3 patterns |

**Milestone 4 (Release Gate)**: Zero regressions. Audit trail complete. All 12 success criteria green.

---

## Risk Assessment and Mitigation

| Risk | Severity | Likelihood | Mitigation | Phase Affected |
|------|----------|------------|------------|----------------|
| **R-1**: AST analyzer false negatives on dynamic dispatch | HIGH | MEDIUM | Explicitly handle `from X import Y` inside function bodies; maintain regression test against known lazy imports in executor.py; document limitations per NFR-6 | Phase 1B, 3 |
| **R-2**: E2E test flakiness from subprocess timing | MEDIUM | MEDIUM | All tests use `_subprocess_factory` injection; no real subprocess calls in E2E suite; reserve real subprocess for separate smoke test | Phase 2 |
| **R-3**: Impl-vs-spec checker false positives | MEDIUM | HIGH | Start with exact function-name + class-name matching only; no NLP/fuzzy matching; fail-open on ambiguous matches (log warning, don't block) | Phase 3 |
| **R-4**: Audit trail JSONL grows unbounded | LOW | LOW | One file per test run, timestamped filename; no cross-run accumulation | Phase 1A |
| **R-5**: 0-files-analyzed fix breaks existing tests | LOW | MEDIUM | Investigate the 3 pre-existing failures before patching; ensure the fix adds a new code path (early return) rather than modifying existing logic | Phase 3 |

**Architect recommendation**: R-3 is the most likely to cause friction during Phase 3. Define the matching contract explicitly in the fidelity checker's docstring before implementation begins. Start with an allowlist of known FR→function mappings rather than attempting automatic discovery.

---

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Used By | Risk | Notes |
|------------|---------|------|-------|
| `ast` (stdlib) | FR-4.2 | None | Standard library, no version concern |
| `pytest` ≥7.0.0 | FR-7.3 | None | Already installed |
| `_subprocess_factory` | All FR-1/2/3 tests | Low | Existing injection point; verify it's stable on current branch |
| `GateCriteria` | FR-4.3 | Low | Existing infrastructure in `pipeline/models.py:68` |
| `_run_checkers()` | FR-5.2 | Low | Existing hook in `roadmap/executor.py:594`; must not break structural/semantic checkers |
| `run_wiring_analysis()` | FR-5.1 | Low | `wiring_gate.py:673`; additive change only |
| `v3.0-v3.2-Fidelity` branch | All | Medium | Must be stable; any upstream changes require rebase |
| JSONL format | FR-7 | None | stdlib `json` module; no external dependency |

### New Files Created

| File | Phase | Purpose |
|------|-------|---------|
| `src/superclaude/cli/audit/reachability.py` | 1B | AST-based reachability analyzer |
| `src/superclaude/cli/roadmap/fidelity_checker.py` | 3 | Impl-vs-spec checker |
| `tests/v3.3/conftest.py` | 1A | Audit trail fixture |
| `tests/v3.3/test_reachability_eval.py` | 1B | Reachability analyzer tests |
| `tests/v3.3/test_wiring_points_e2e.py` | 2A | FR-1 wiring E2E tests |
| `tests/v3.3/test_turnledger_lifecycle.py` | 2B | FR-2 lifecycle tests |
| `tests/v3.3/test_gate_rollout_modes.py` | 2C | FR-3 mode matrix tests |
| `tests/v3.3/test_integration_regression.py` | 2D | FR-6.2 gap closure tests |
| `tests/v3.3/wiring_manifest.yaml` | 1B | Reachability manifest |
| `tests/audit-trail/test_audit_writer.py` | 1A | Audit infrastructure tests |

### Files Modified

| File | Phase | Change |
|------|-------|--------|
| `src/superclaude/cli/audit/wiring_gate.py` | 3 | FR-5.1: 0-files-analyzed assertion |
| `src/superclaude/cli/roadmap/executor.py` | 3 | FR-5.2: wire fidelity_checker into `_run_checkers()` |
| `tests/roadmap/test_convergence_wiring.py` | 2D | FR-6.1 T07: extend/verify tests |
| `tests/roadmap/test_convergence_e2e.py` | 2D | FR-6.1 T11/T12: extend tests |

---

## Success Criteria Validation Matrix

| ID | Criterion | Validation Method | Phase | Automated? |
|----|-----------|-------------------|-------|------------|
| SC-1 | ≥20 wiring point E2E tests | Count tests in `test_wiring_points_e2e.py` mapped to FR-1 sub-IDs | 2 | Yes — audit trail count |
| SC-2 | 4/4 TurnLedger paths green | `test_turnledger_lifecycle.py` all pass | 2 | Yes |
| SC-3 | 8+ gate mode scenarios passing | `test_gate_rollout_modes.py` 4 modes × 2 paths | 2 | Yes |
| SC-4 | ≥4894 passed, ≤3 pre-existing | Full `uv run pytest` | 4 | Yes |
| SC-5 | KPI wiring fields match expected | Integration test field comparison in FR-1.11 test | 2 | Yes |
| SC-6 | 4/4 budget exhaustion scenarios | FR-3.2a–d tests pass | 2 | Yes |
| SC-7 | Eval catches known-bad state | FR-4.4 regression test | 3 | Yes |
| SC-8 | All QA gap tests passing | FR-6.1 + FR-6.2 tests green | 2 | Yes |
| SC-9 | Reachability gate detects unreachable | FR-4.4 on intentionally broken wiring | 3 | Yes |
| SC-10 | 0-files → FAIL | FR-5.1 assertion test | 3 | Yes |
| SC-11 | Fidelity checker finds gap | FR-5.2 synthetic test | 3 | Yes |
| SC-12 | Audit trail third-party verifiable | JSONL output review against FR-7.2 properties | 2 | Semi — automated check + manual review |

---

## Timeline Summary

| Phase | Name | Duration | Blocked By | Key Deliverables |
|-------|------|----------|------------|------------------|
| 1 | Foundation | ~3 days | — | Audit trail fixture, AST reachability analyzer, wiring manifest |
| 2 | Core E2E Suites | ~5 days | Phase 1A | 50+ E2E tests across 4 test files; SC-1–6, SC-8, SC-12 |
| 3 | Pipeline Fixes | ~2 days | Phase 1B, Phase 2 | 3 production changes, reachability gate integration; SC-7, SC-9–11 |
| 4 | Regression + Audit | ~1 day | All | Zero-regression validation, audit review; SC-4 |
| **Total** | | **~11 days** | | 13 requirements, 12 success criteria |

**Critical path**: Phase 1A → Phase 2 → Phase 4. Phase 1B can run in parallel with Phase 1A but must complete before Phase 3.

---

## Open Questions (Architect Recommendations)

| # | Question | Recommendation |
|---|----------|----------------|
| 1 | Signal handling for FR-3.3 | Test `SIGINT` only — it's the standard user interrupt. `SIGTERM`/`SIGHUP` are process management signals outside test scope. Use `os.kill(os.getpid(), signal.SIGINT)` in test. |
| 2 | Impl-vs-spec checker granularity | Require exact function-name or class-name match as minimum evidence. Docstring FR-ID citations are bonus evidence, not required. This minimizes R-3 false positives. |
| 3 | Audit trail fixture scope | Session-scoped. One JSONL per `pytest` invocation. Function-scoped would create file-per-test overhead with no benefit. |
| 4 | Wiring manifest location | Standalone `.yaml` file in the release directory (`tests/v3.3/wiring_manifest.yaml`). Not embedded in markdown — YAML parsing from markdown is fragile. |
| 5 | `attempt_remediation()` boundary | v3.3 tests FR-1.14 (the `_recheck_wiring()` path which is the internal mechanism). `attempt_remediation()` is the public API wrapper — defer its full integration test to v3.4. |
| 6 | Checkpoint frequency for FR-2.4 | Assert `available()` invariant after each phase completion — this is where the ledger state is observable and deterministic. Per-task or per-hook is too granular and couples tests to internal sequencing. |
| 7 | Pre-existing 3 failures | Investigate before Phase 3. Run baseline suite, capture the 3 failures, document them. If 2 are wiring-pipeline related (R-5), the FR-5.1 fix may resolve them — reducing pre-existing to 1. |
| 8 | Reachability gate CI placement | Include in standard `uv run pytest` via `tests/v3.3/test_reachability_eval.py`. The gate itself is a library function — testing it doesn't require pipeline context. Pipeline integration is a separate concern for the sprint runner. |
