# TASKLIST INDEX -- v3.1 Anti-Instinct Gate

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | v3.1 Anti-Instinct Gate |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-03-20 |
| TASKLIST_ROOT | `.dev/releases/current/v3.1_Anti-instincts__/` |
| Total Phases | 4 |
| Total Tasks | 20 |
| Total Deliverables | 34 |
| Complexity Class | HIGH |
| Primary Persona | backend |
| Consulting Personas | qa, analyzer |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `.dev/releases/current/v3.1_Anti-instincts__/tasklist-index.md` |
| Phase 1 Tasklist | `.dev/releases/current/v3.1_Anti-instincts__/phase-1-tasklist.md` |
| Phase 2 Tasklist | `.dev/releases/current/v3.1_Anti-instincts__/phase-2-tasklist.md` |
| Phase 3 Tasklist | `.dev/releases/current/v3.1_Anti-instincts__/phase-3-tasklist.md` |
| Phase 4 Tasklist | `.dev/releases/current/v3.1_Anti-instincts__/phase-4-tasklist.md` |
| Execution Log | `.dev/releases/current/v3.1_Anti-instincts__/execution-log.md` |
| Checkpoint Reports | `.dev/releases/current/v3.1_Anti-instincts__/checkpoints/` |
| Evidence Directory | `.dev/releases/current/v3.1_Anti-instincts__/evidence/` |
| Artifacts Directory | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/` |
| Validation Reports | `.dev/releases/current/v3.1_Anti-instincts__/validation/` |
| Feedback Log | `.dev/releases/current/v3.1_Anti-instincts__/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Core Detection Modules & Architecture Decisions | T01.01-T01.09 | STRICT: 3, STANDARD: 5, EXEMPT: 1 |
| 2 | phase-2-tasklist.md | Gate Definition, Executor Wiring & Prompt Hardening | T02.01-T02.04 | STRICT: 3, STANDARD: 1 |
| 3 | phase-3-tasklist.md | Sprint Integration & Rollout Mode | T03.01-T03.03 | STRICT: 2, STANDARD: 1 |
| 4 | phase-4-tasklist.md | Shadow Validation & Graduation | T04.01-T04.04 | STANDARD: 2, EXEMPT: 2 |

## Source Snapshot

- Adds deterministic, zero-LLM anti-instinct gating layer to roadmap and sprint pipelines
- Four pure-Python detection modules: obligation scanner, integration contract extractor, fingerprint coverage checker, spec structural auditor
- Gate slots between `merge` and `test-strategy` in existing pipeline
- Ships with `gate_rollout_mode=off`; shadow validation before enforcement
- 35 functional requirements, 10 non-functional requirements, 12 new files, 5 modified files (~1,200 LOC)
- 4 build phases with 3 validation checkpoints (A: implementation readiness, B: rollout readiness, C: enforcement readiness)

## Deterministic Rules Applied

- Phase numbering: Sequential 1-4, matching roadmap labels exactly; no gaps
- Task IDs: `T<PP>.<TT>` zero-padded format; appearance order within phases
- Checkpoint cadence: every 5 tasks within a phase + end-of-phase mandatory checkpoint
- Clarification task rule: no clarification tasks needed; all items have sufficient specificity
- Deliverable registry: D-0001 through D-0034, globally unique, artifact paths under TASKLIST_ROOT
- Effort mapping: EFFORT_SCORE computed from text length, splits, domain keywords, dependency words
- Risk mapping: RISK_SCORE computed from security, migration, auth, performance, cross-cutting keywords
- Tier classification: STRICT > EXEMPT > LIGHT > STANDARD priority; compound phrase overrides checked first
- Confidence scoring: base from max tier score, ambiguity penalty, compound phrase boost, vague penalty
- Verification routing: STRICT=sub-agent, STANDARD=direct test, LIGHT=sanity check, EXEMPT=skip
- MCP requirements: STRICT requires Sequential+Serena; STANDARD/LIGHT/EXEMPT flexible
- Multi-file output: index + 4 phase files; phase files contain only their tasks and checkpoints
- R-006 split into 4 tasks (one per independently deliverable test file)

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | 1.0 Day-1 Architecture Decisions: resolve OQ-003, OQ-004, OQ-005, OQ-010 before writing module code |
| R-002 | Phase 1 | 1.1 Obligation Scanner (`obligation_scanner.py`): implement compiled regex vocabulary for 11 scaffold terms |
| R-003 | Phase 1 | 1.2 Integration Contract Extractor (`integration_contracts.py`): implement 7-category dispatch pattern scanner with compiled regexes |
| R-004 | Phase 1 | 1.3 Fingerprint Extraction (`fingerprint.py`): implement three-source extraction: backtick identifiers, code-block def/class, ALL_CAPS constants |
| R-005 | Phase 1 | 1.4 Spec Structural Audit (`spec_structural_audit.py`): implement 7 structural indicator counters |
| R-006 | Phase 1 | 1.5 Unit Tests for All Modules: test_obligation_scanner.py, test_integration_contracts.py, test_fingerprint.py, test_spec_structural_audit.py |
| R-007 | Phase 1 | 1.5.1 Validation Gate (Checkpoint A): SC-001 through SC-005 pass, SC-006 latency, SC-007 backward compat |
| R-008 | Phase 2 | 2.1 Gate Definition in `roadmap/gates.py`: define ANTI_INSTINCT_GATE as GateCriteria with required frontmatter |
| R-009 | Phase 2 | 2.2 Executor Integration in `roadmap/executor.py`: add `_run_structural_audit()` hook, anti-instinct step |
| R-010 | Phase 2 | 2.3 Prompt Modifications in `roadmap/prompts.py`: add INTEGRATION_ENUMERATION_BLOCK and INTEGRATION_WIRING_DIMENSION |
| R-011 | Phase 2 | 2.4 Integration Tests: end-to-end roadmap pipeline run with anti-instinct gate active |
| R-012 | Phase 2 | 2.4.1 Validation Gate: full roadmap pipeline completes, SC-001 regression, SC-006 latency, SC-007 compat |
| R-013 | Phase 3 | 3.1 Sprint Config Extension: add `gate_rollout_mode: Literal["off", "shadow", "soft", "full"]` to SprintConfig |
| R-014 | Phase 3 | 3.2 Sprint Executor Wiring: wrap anti-instinct gate result in TrailingGateResult, implement rollout mode matrix |
| R-015 | Phase 3 | 3.3 Sprint Integration Tests: test rollout mode matrix all 4 modes, None-safe ledger guards |
| R-016 | Phase 3 | 3.3.1 Validation Gate (Checkpoint B): sprint pipeline runs with shadow, SC-008 baseline, SC-009 no conflicts |
| R-017 | Phase 4 | 4.1 Shadow Mode Activation: set gate_rollout_mode=shadow in test sprint configurations, run 5+ sprints |
| R-018 | Phase 4 | 4.2 Threshold Calibration: analyze fingerprint coverage threshold (0.7), structural audit threshold (0.5) |
| R-019 | Phase 4 | 4.3 Open Question Resolution: OQ-002 context window, OQ-008 multi-component false negatives, OQ-007 TurnLedger |
| R-020 | Phase 4 | 4.4 Graduation Criteria (Checkpoint C): ShadowGateMetrics.pass_rate >= 0.90 over 5+ sprints |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | Architecture Decision Record for OQ-003, OQ-004, OQ-005, OQ-010 | EXEMPT | Skip verification | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0001/spec.md` | S | Low |
| D-0002 | T01.01 | R-001 | Merge coordination plan for WIRING_GATE in gates.py | EXEMPT | Skip verification | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0002/notes.md` | S | Low |
| D-0003 | T01.02 | R-002 | `obligation_scanner.py` module with ObligationReport/Obligation dataclasses | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0003/spec.md` | M | Medium |
| D-0004 | T01.03 | R-003 | `integration_contracts.py` module with IntegrationAuditResult dataclass | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0004/spec.md` | M | Medium |
| D-0005 | T01.04 | R-004 | `fingerprint.py` module with three-source extraction and threshold logic | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0005/spec.md` | M | Low |
| D-0006 | T01.05 | R-005 | `spec_structural_audit.py` module with 7 indicator counters | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0006/spec.md` | S | Low |
| D-0007 | T01.06 | R-006 | `test_obligation_scanner.py` with scaffold detection and cli-portify regression tests | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0007/evidence.md` | S | Low |
| D-0008 | T01.07 | R-006 | `test_integration_contracts.py` with 7-category and wiring coverage tests | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0008/evidence.md` | S | Low |
| D-0009 | T01.08 | R-006 | `test_fingerprint.py` with extraction, deduplication, coverage ratio tests | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0009/evidence.md` | S | Low |
| D-0010 | T01.09 | R-006 | `test_spec_structural_audit.py` with 7 indicators and warning-only tests | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0010/evidence.md` | S | Low |
| D-0011 | T02.01 | R-008 | `ANTI_INSTINCT_GATE` definition in `roadmap/gates.py` with 3 semantic checks | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0011/spec.md` | M | Medium |
| D-0012 | T02.02 | R-009 | Anti-instinct step in `roadmap/executor.py` with `_run_anti_instinct_audit()` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0012/spec.md` | L | Medium |
| D-0013 | T02.02 | R-009 | `anti-instinct-audit.md` output artifact with YAML frontmatter | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0013/spec.md` | L | Medium |
| D-0014 | T02.02 | R-009 | Sprint-side integration artifacts: TrailingGateResult, DeferredRemediationLog exports | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0014/spec.md` | L | Medium |
| D-0015 | T02.03 | R-010 | `INTEGRATION_ENUMERATION_BLOCK` in `build_generate_prompt()` | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0015/spec.md` | S | Low |
| D-0016 | T02.03 | R-010 | `INTEGRATION_WIRING_DIMENSION` as dimension 6 in `build_spec_fidelity_prompt()` | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0016/spec.md` | S | Low |
| D-0017 | T02.04 | R-011 | `test_anti_instinct_integration.py` end-to-end pipeline tests | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0017/evidence.md` | M | Medium |
| D-0018 | T03.01 | R-013 | `gate_rollout_mode` field added to `SprintConfig` in `sprint/models.py` | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0018/spec.md` | S | Low |
| D-0019 | T03.02 | R-014 | Rollout mode behavior matrix implementation in `sprint/executor.py` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0019/spec.md` | L | High |
| D-0020 | T03.02 | R-014 | `ShadowGateMetrics.record()` integration for shadow/soft/full modes | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0020/spec.md` | L | High |
| D-0021 | T03.02 | R-014 | TurnLedger credit/remediation logic with None-safe guards | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0021/spec.md` | L | High |
| D-0022 | T03.02 | R-014 | Anti-instinct KPI aggregation in `build_kpi_report()` / `GateKPIReport` | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0022/spec.md` | L | High |
| D-0023 | T03.03 | R-015 | `test_anti_instinct_sprint.py` rollout mode matrix tests (4 modes x pass/fail) | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0023/evidence.md` | M | Medium |
| D-0024 | T03.03 | R-015 | `test_shadow_mode.py` ShadowGateMetrics recording tests | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0024/evidence.md` | M | Medium |
| D-0025 | T03.03 | R-015 | `test_full_flow.py` full pipeline flow with reimbursement path tests | STRICT | Sub-agent (quality-engineer) | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0025/evidence.md` | M | Medium |
| D-0026 | T04.01 | R-017 | Shadow mode configuration applied to test sprint configs | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0026/notes.md` | S | Low |
| D-0027 | T04.01 | R-017 | 5+ sprint run `ShadowGateMetrics` data collection | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0027/evidence.md` | S | Low |
| D-0028 | T04.02 | R-018 | Fingerprint coverage threshold (0.7) calibration analysis | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0028/notes.md` | M | Medium |
| D-0029 | T04.02 | R-018 | Structural audit threshold (0.5) calibration analysis | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0029/notes.md` | M | Medium |
| D-0030 | T04.02 | R-018 | Calibration results document with threshold rationale | STANDARD | Direct test execution | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0030/spec.md` | M | Medium |
| D-0031 | T04.03 | R-019 | OQ-002 resolution: 60-char context window validation results | EXEMPT | Skip verification | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0031/notes.md` | XS | Low |
| D-0032 | T04.03 | R-019 | OQ-007/OQ-008 resolution: TurnLedger reconciliation and multi-component assessment | EXEMPT | Skip verification | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0032/notes.md` | XS | Low |
| D-0033 | T04.04 | R-020 | Graduation decision document with pass_rate evidence | EXEMPT | Skip verification | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0033/spec.md` | XS | Low |
| D-0034 | T04.04 | R-020 | Rollout promotion plan (shadow -> soft -> full) | EXEMPT | Skip verification | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0034/spec.md` | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001, D-0002 | EXEMPT | 85% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0001/`, `D-0002/` |
| R-002 | T01.02 | D-0003 | STRICT | 90% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0003/` |
| R-003 | T01.03 | D-0004 | STRICT | 90% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0004/` |
| R-004 | T01.04 | D-0005 | STRICT | 85% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0005/` |
| R-005 | T01.05 | D-0006 | STANDARD | 80% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0006/` |
| R-006 | T01.06, T01.07, T01.08, T01.09 | D-0007, D-0008, D-0009, D-0010 | STANDARD | 85% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0007/` through `D-0010/` |
| R-007 | -- | -- | -- | -- | Checkpoint A (end-of-phase) |
| R-008 | T02.01 | D-0011 | STRICT | 92% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0011/` |
| R-009 | T02.02 | D-0012, D-0013, D-0014 | STRICT | 92% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0012/` through `D-0014/` |
| R-010 | T02.03 | D-0015, D-0016 | STANDARD | 80% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0015/`, `D-0016/` |
| R-011 | T02.04 | D-0017 | STRICT | 85% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0017/` |
| R-012 | -- | -- | -- | -- | Checkpoint (end-of-phase) |
| R-013 | T03.01 | D-0018 | STANDARD | 80% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0018/` |
| R-014 | T03.02 | D-0019, D-0020, D-0021, D-0022 | STRICT | 92% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0019/` through `D-0022/` |
| R-015 | T03.03 | D-0023, D-0024, D-0025 | STRICT | 85% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0023/` through `D-0025/` |
| R-016 | -- | -- | -- | -- | Checkpoint B (end-of-phase) |
| R-017 | T04.01 | D-0026, D-0027 | STANDARD | 80% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0026/`, `D-0027/` |
| R-018 | T04.02 | D-0028, D-0029, D-0030 | STANDARD | 75% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0028/` through `D-0030/` |
| R-019 | T04.03 | D-0031, D-0032 | EXEMPT | 85% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0031/`, `D-0032/` |
| R-020 | T04.04 | D-0033, D-0034 | EXEMPT | 85% | `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0033/`, `D-0034/` |

## Execution Log Template

**Intended Path:** `.dev/releases/current/v3.1_Anti-instincts__/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|
| | | | | | | | |

## Checkpoint Report Template

**Template:**

```
# Checkpoint Report -- <Checkpoint Title>
**Checkpoint Report Path:** .dev/releases/current/v3.1_Anti-instincts__/checkpoints/<deterministic-name>.md
**Scope:** <tasks covered>
## Status
Overall: Pass | Fail | TBD
## Verification Results
- <bullet 1>
- <bullet 2>
- <bullet 3>
## Exit Criteria Assessment
- <bullet 1>
- <bullet 2>
- <bullet 3>
## Issues & Follow-ups
- <list blocking issues referencing T<PP>.<TT> and D-####>
## Evidence
- <bullet list of evidence paths under .dev/releases/current/v3.1_Anti-instincts__/evidence/>
```

## Feedback Collection Template

**Intended Path:** `.dev/releases/current/v3.1_Anti-instincts__/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
| | | | | | | |
