# TASKLIST INDEX -- Wiring Verification Gate v1.0

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Wiring Verification Gate v1.0 |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-03-20 |
| TASKLIST_ROOT | `.dev/releases/current/v3.2_fidelity-refactor___/` |
| Total Phases | 5 |
| Total Tasks | 27 |
| Total Deliverables | 33 |
| Complexity Class | HIGH |
| Primary Persona | backend |
| Consulting Personas | security, qa, analyzer |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `.dev/releases/current/v3.2_fidelity-refactor___/tasklist-index.md` |
| Phase 1 Tasklist | `.dev/releases/current/v3.2_fidelity-refactor___/phase-1-tasklist.md` |
| Phase 2 Tasklist | `.dev/releases/current/v3.2_fidelity-refactor___/phase-2-tasklist.md` |
| Phase 3 Tasklist | `.dev/releases/current/v3.2_fidelity-refactor___/phase-3-tasklist.md` |
| Phase 4 Tasklist | `.dev/releases/current/v3.2_fidelity-refactor___/phase-4-tasklist.md` |
| Phase 5 Tasklist | `.dev/releases/current/v3.2_fidelity-refactor___/phase-5-tasklist.md` |
| Execution Log | `.dev/releases/current/v3.2_fidelity-refactor___/execution-log.md` |
| Checkpoint Reports | `.dev/releases/current/v3.2_fidelity-refactor___/checkpoints/` |
| Evidence Directory | `.dev/releases/current/v3.2_fidelity-refactor___/evidence/` |
| Artifacts Directory | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/` |
| Validation Reports | `.dev/releases/current/v3.2_fidelity-refactor___/validation/` |
| Feedback Log | `.dev/releases/current/v3.2_fidelity-refactor___/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Core Analysis Engine | T01.01-T01.08 | STRICT: 5, STANDARD: 3 |
| 2 | phase-2-tasklist.md | Sprint Integration | T02.01-T02.08 | STRICT: 5, STANDARD: 2, EXEMPT: 1 |
| 3 | phase-3-tasklist.md | KPI and Deviation Reconciliation | T03.01-T03.02 | STRICT: 1, STANDARD: 1 |
| 4 | phase-4-tasklist.md | Integration Testing and Validation | T04.01-T04.04 | STRICT: 2, STANDARD: 2 |
| 5 | phase-5-tasklist.md | Rollout Validation | T05.01-T05.03 | EXEMPT: 3 |

## Source Snapshot

- Adds a static-analysis wiring verification gate detecting unwired callables, orphan modules, and broken dispatch registries
- Integrates into sprint execution loop via shadow->soft->blocking enforcement model
- New code in `src/superclaude/cli/audit/` (wiring_gate.py, wiring_config.py); modifications to 4 existing files
- Debit-before-analysis budget model with floor-to-zero credit arithmetic
- 23 requirements (15 functional, 8 non-functional), 15 success criteria, 8 risks
- Estimated ~800-1085 LOC across new code, modifications, and tests

## Deterministic Rules Applied

- Phase buckets derived from 5 explicit roadmap phases (Phase 1-5)
- Phase numbering sequential 1-5 with no gaps
- Task IDs use `T<PP>.<TT>` zero-padded format
- Roadmap items merged by milestone when sharing a single deliverable file
- Checkpoint cadence: every 5 tasks + end-of-phase
- Clarification tasks inserted for prerequisites explicitly stated in roadmap (OQ-2, OQ-6)
- Deliverable IDs assigned sequentially D-0001 through D-0033
- Effort computed via keyword scoring (XS/S/M/L/XL)
- Risk computed via keyword scoring (Low/Medium/High)
- Tier classification via compound phrase override + keyword matching + context boosters
- Verification routing matched to computed tier
- MCP requirements assigned per tier
- Traceability matrix links R-### -> T<PP>.<TT> -> D-#### with tier and confidence

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | T01 — WiringFinding dataclass |
| R-002 | Phase 1 | T01 — WiringReport dataclass |
| R-003 | Phase 1 | T01 — WiringConfig dataclass |
| R-004 | Phase 1 | Whitelist schema + loader |
| R-005 | Phase 1 | `analyze_unwired_callables()` |
| R-006 | Phase 1 | `analyze_orphan_modules()` |
| R-007 | Phase 1 | `analyze_unwired_registries()` |
| R-008 | Phase 1 | `emit_report()` |
| R-009 | Phase 1 | `WIRING_GATE` constant |
| R-010 | Phase 1 | 5 semantic check functions |
| R-011 | Phase 1 | Unwired callable tests |
| R-012 | Phase 1 | Orphan module tests |
| R-013 | Phase 1 | Unwired registry tests |
| R-014 | Phase 1 | Report + gate tests |
| R-015 | Phase 1 | Test fixtures |
| R-016 | Phase 2 | OQ-2 — WIRING_ANALYSIS_TURNS and REMEDIATION_COST values must be resolved before Phase 2 |
| R-017 | Phase 2 | OQ-6 — SprintGatePolicy constructor compatibility must be resolved before Phase 2 |
| R-018 | Phase 2 | 3 new fields for TurnLedger |
| R-019 | Phase 2 | `debit_wiring()` method |
| R-020 | Phase 2 | `credit_wiring()` with floor |
| R-021 | Phase 2 | `can_run_wiring_gate()` method |
| R-022 | Phase 2 | 3 SprintConfig fields |
| R-023 | Phase 2 | SprintConfig migration shim with deprecation warning |
| R-024 | Phase 2 | `run_post_task_wiring_hook()` |
| R-025 | Phase 2 | BLOCKING mode path |
| R-026 | Phase 2 | SHADOW mode path |
| R-027 | Phase 2 | SOFT mode path |
| R-028 | Phase 2 | Null-ledger compat |
| R-029 | Phase 2 | Helper functions |
| R-030 | Phase 2 | TurnLedger debit/credit unit tests |
| R-031 | Phase 3 | 6 wiring KPI fields |
| R-032 | Phase 3 | `build_kpi_report()` signature update |
| R-033 | Phase 3 | `_deviation_counts_reconciled()` function |
| R-034 | Phase 4 | cli-portify fixture producing exactly 1 WiringFinding(unwired_callable) |
| R-035 | Phase 4 | Budget Scenario 5 (credit floor) |
| R-036 | Phase 4 | Budget Scenario 6 (BLOCKING remediation) |
| R-037 | Phase 4 | Budget Scenario 7 (null-ledger compat) |
| R-038 | Phase 4 | Budget Scenario 8 (shadow deferred log) |
| R-039 | Phase 4 | Run against actual `cli_portify/` to detect original step_runner=None no-op bug |
| R-040 | Phase 4 | Benchmark on 50-file package, p95 < 5s |
| R-041 | Phase 5 | Shadow mode baseline — activate Goal-5a, collect findings, validate provider_dir_names |
| R-042 | Phase 5 | Soft mode readiness — enable Goal-5b, measure FPR and remediation usefulness |
| R-043 | Phase 5 | Blocking mode authorization — enable Goal-5c only if evidence thresholds met |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001, R-002 | WiringFinding and WiringReport dataclasses in `audit/wiring_gate.py` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0001/spec.md` | M | Medium |
| D-0002 | T01.01 | R-003, R-004 | WiringConfig dataclass and whitelist schema+loader in `audit/wiring_config.py` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0002/spec.md` | M | Medium |
| D-0003 | T01.02 | R-005 | `analyze_unwired_callables()` function in `audit/wiring_gate.py` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0003/spec.md` | M | Medium |
| D-0004 | T01.03 | R-006 | `analyze_orphan_modules()` function in `audit/wiring_gate.py` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0004/spec.md` | M | Medium |
| D-0005 | T01.04 | R-007 | `analyze_unwired_registries()` function in `audit/wiring_gate.py` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0005/spec.md` | S | Low |
| D-0006 | T01.05 | R-008 | `emit_report()` function with 11 required frontmatter fields via `yaml.safe_dump()` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0006/spec.md` | M | Medium |
| D-0007 | T01.05 | R-009, R-010 | `WIRING_GATE` constant and 5 semantic check functions with `(content: str) -> bool` signature | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0007/spec.md` | M | Medium |
| D-0008 | T01.06 | R-011, R-012 | Unit tests for unwired callable and orphan module analyzers (9 tests) | STANDARD | Direct test execution | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0008/evidence.md` | S | Low |
| D-0009 | T01.07 | R-013, R-014 | Unit tests for registry analyzer, report emission, and gate evaluation (5 tests) | STANDARD | Direct test execution | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0009/evidence.md` | S | Low |
| D-0010 | T01.08 | R-015 | Test fixture files in `tests/audit/fixtures/` | STANDARD | Direct test execution | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0010/evidence.md` | S | Low |
| D-0011 | T02.01 | R-016, R-017 | Decision record resolving OQ-2 (budget constants) and OQ-6 (SprintGatePolicy constructor) | EXEMPT | Skip verification | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0011/spec.md` | S | Low |
| D-0012 | T02.02 | R-018, R-019, R-020, R-021 | TurnLedger extensions: 3 new fields, `debit_wiring()`, `credit_wiring()`, `can_run_wiring_gate()` in `sprint/models.py` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0012/spec.md` | M | Medium |
| D-0013 | T02.03 | R-022, R-023 | 3 SprintConfig fields and `__post_init__` migration shim in `sprint/models.py` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0013/spec.md` | M | Medium |
| D-0014 | T02.04 | R-024 | `run_post_task_wiring_hook()` in `sprint/executor.py` with `resolve_gate_mode()` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0014/spec.md` | L | High |
| D-0015 | T02.05 | R-025 | BLOCKING mode path in `sprint/executor.py` (fail + remediate via callable interface) | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0015/spec.md` | M | High |
| D-0016 | T02.06 | R-026 | SHADOW mode path in `sprint/executor.py` (log-only, non-interfering) | STANDARD | Direct test execution | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0016/spec.md` | S | Low |
| D-0017 | T02.07 | R-027, R-028 | SOFT mode path and null-ledger compatibility in `sprint/executor.py` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0017/spec.md` | M | Medium |
| D-0018 | T02.08 | R-029, R-030 | TurnLedger unit tests validating debit/credit/floor-to-zero semantics (3 tests) | STANDARD | Direct test execution | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0018/evidence.md` | S | Low |
| D-0019 | T03.01 | R-031, R-032 | 6 wiring KPI fields and `build_kpi_report()` signature update in `sprint/kpi.py` | STANDARD | Direct test execution | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0019/spec.md` | S | Low |
| D-0020 | T03.02 | R-033 | `_deviation_counts_reconciled()` in `roadmap/gates.py` with merge conflict mitigation | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0020/spec.md` | L | High |
| D-0021 | T04.01 | R-034 | cli-portify fixture integration test producing exactly 1 `WiringFinding(unwired_callable)` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0021/evidence.md` | M | Medium |
| D-0022 | T04.02 | R-035, R-036, R-037, R-038 | Budget scenario integration tests (4 scenarios: credit floor, BLOCKING remediation, null-ledger, shadow deferred) | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0022/evidence.md` | M | High |
| D-0023 | T04.03 | R-039 | Retrospective validation report confirming detection of original `step_runner=None` no-op bug | STANDARD | Direct test execution | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0023/evidence.md` | S | Medium |
| D-0024 | T04.04 | R-040 | Performance benchmark report confirming p95 < 5s on 50-file package | STANDARD | Direct test execution | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0024/evidence.md` | M | Medium |
| D-0025 | T05.01 | R-041 | Shadow mode baseline data: findings volume, whitelist usage, zero-findings anomalies, p95 runtime | EXEMPT | Skip verification | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0025/notes.md` | M | Medium |
| D-0026 | T05.01 | R-041 | Validated `provider_dir_names` and registry patterns against real repository conventions | EXEMPT | Skip verification | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0026/notes.md` | M | Medium |
| D-0027 | T05.02 | R-042 | Soft mode readiness assessment: FPR burden analysis and remediation usefulness evaluation | EXEMPT | Skip verification | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0027/notes.md` | S | Medium |
| D-0028 | T05.03 | R-043 | Blocking mode authorization decision with evidence checklist (SC-009, SC-010, whitelist calibration) | EXEMPT | Skip verification | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0028/notes.md` | M | High |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001, R-002 | T01.01 | D-0001 | STRICT | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0001/spec.md` |
| R-003, R-004 | T01.01 | D-0002 | STRICT | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0002/spec.md` |
| R-005 | T01.02 | D-0003 | STRICT | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0003/spec.md` |
| R-006 | T01.03 | D-0004 | STRICT | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0004/spec.md` |
| R-007 | T01.04 | D-0005 | STRICT | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0005/spec.md` |
| R-008 | T01.05 | D-0006 | STRICT | [█████████░] 85% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0006/spec.md` |
| R-009, R-010 | T01.05 | D-0007 | STRICT | [█████████░] 85% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0007/spec.md` |
| R-011, R-012 | T01.06 | D-0008 | STANDARD | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0008/evidence.md` |
| R-013, R-014 | T01.07 | D-0009 | STANDARD | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0009/evidence.md` |
| R-015 | T01.08 | D-0010 | STANDARD | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0010/evidence.md` |
| R-016, R-017 | T02.01 | D-0011 | EXEMPT | [█████████░] 90% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0011/spec.md` |
| R-018, R-019, R-020, R-021 | T02.02 | D-0012 | STRICT | [█████████░] 85% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0012/spec.md` |
| R-022, R-023 | T02.03 | D-0013 | STRICT | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0013/spec.md` |
| R-024 | T02.04 | D-0014 | STRICT | [█████████░] 90% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0014/spec.md` |
| R-025 | T02.05 | D-0015 | STRICT | [█████████░] 85% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0015/spec.md` |
| R-026 | T02.06 | D-0016 | STANDARD | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0016/spec.md` |
| R-027, R-028 | T02.07 | D-0017 | STRICT | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0017/spec.md` |
| R-029, R-030 | T02.08 | D-0018 | STANDARD | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0018/evidence.md` |
| R-031, R-032 | T03.01 | D-0019 | STANDARD | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0019/spec.md` |
| R-033 | T03.02 | D-0020 | STRICT | [█████████░] 85% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0020/spec.md` |
| R-034 | T04.01 | D-0021 | STRICT | [█████████░] 90% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0021/evidence.md` |
| R-035, R-036, R-037, R-038 | T04.02 | D-0022 | STRICT | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0022/evidence.md` |
| R-039 | T04.03 | D-0023 | STANDARD | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0023/evidence.md` |
| R-040 | T04.04 | D-0024 | STANDARD | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0024/evidence.md` |
| R-041 | T05.01 | D-0025, D-0026 | EXEMPT | [█████████░] 90% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0025/notes.md`, `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0026/notes.md` |
| R-042 | T05.02 | D-0027 | EXEMPT | [█████████░] 90% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0027/notes.md` |
| R-043 | T05.03 | D-0028 | EXEMPT | [████████░░] 80% | `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0028/notes.md` |

## Execution Log Template

**Intended Path:** `.dev/releases/current/v3.2_fidelity-refactor___/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|
| | | | | | | | |

## Checkpoint Report Template

**Template:**

# Checkpoint Report -- <Checkpoint Title>

**Checkpoint Report Path:** `.dev/releases/current/v3.2_fidelity-refactor___/checkpoints/<deterministic-name>.md`

**Scope:** <tasks covered>

## Status
- Overall: Pass | Fail | TBD

## Verification Results
- <bullet 1>
- <bullet 2>
- <bullet 3>

## Exit Criteria Assessment
- <bullet 1>
- <bullet 2>
- <bullet 3>

## Issues & Follow-ups
- List blocking issues; reference `T<PP>.<TT>` and `D-####`

## Evidence
- `.dev/releases/current/v3.2_fidelity-refactor___/evidence/<artifact>`

## Feedback Collection Template

**Intended Path:** `.dev/releases/current/v3.2_fidelity-refactor___/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
| | | | | | | |

## Generation Notes

- 5 explicit phases derived directly from roadmap headings
- Phase 5 (Rollout Validation) classified as EXEMPT — post-merge operational validation milestones
- Roadmap items R-001 through R-004 merged into T01.01 (single data models task) per milestone 1.1 grouping
- Roadmap items R-024 through R-029 split into separate tasks T02.04-T02.07 per Section 4.4 (independently deliverable mode paths)
- T02.01 is a Clarification Task for Phase 2 entry prerequisites (OQ-2, OQ-6)
- Milestone 3.2 coordination strategy preserved in T03.02 notes (shared `roadmap/gates.py` file)
- Risk R6 (provider_dir_names mismatch) flagged as highest-severity across Phase 1, Phase 5
