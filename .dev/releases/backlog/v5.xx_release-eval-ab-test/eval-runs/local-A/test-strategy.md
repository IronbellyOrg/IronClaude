---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 4
work_milestones: 4
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
spec_source: eval-spec.md
generated: "2026-03-19T17:15:42.161370+00:00"
generator: superclaude-roadmap-executor
---

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | Stop-and-fix immediately | Blocks current phase |
| MAJOR | Stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

---

## 1. Validation Milestones Mapped to Roadmap Phases

| Validation Milestone | After Phase | What It Validates |
|---------------------|-------------|-------------------|
| **V1** | Phase 1 (Requirements Closure) | All OQs resolved, acceptance contract frozen, traceability matrix complete |
| **V2** | Phase 2 (Data Models & CLI) | `progress.json` produced end-to-end, atomic writes work, CLI option functional |
| **V3** | Phase 3 (Gate Summary & Special Steps) | Dry-run table correct, all special-step metadata populated, parallel timing accurate |
| **V4** | Phase 4 (Validation & Release) | All 7 success criteria pass, performance budget met, sync verified |

### Interleaving Schedule (1:2 ratio)

Since complexity is MEDIUM, every two implementation phases get one dedicated validation milestone. Phases 1–2 share V2 as the validation gate; Phases 3–4 share V4. V1 and V3 are lightweight checkpoints.

```
Phase 1 → V1 (document review, no code)
Phase 2 → V2 (first real validation gate — code must work)
Phase 3 → V3 (validation gate — enriched metadata must work)
Phase 4 → V4 (final validation gate — all SC pass)
```

---

## 2. Test Categories

### Unit Tests
Target: `progress.py` internals in isolation.

| Test | Requirement | Priority |
|------|-------------|----------|
| `StepProgress` serialization round-trip | FR-010 | HIGH |
| `PipelineProgress.to_json()` produces valid JSON | FR-002 | HIGH |
| Atomic write: temp file created then replaced | NFR-002 | HIGH |
| Zero import-time side effects | NFR-003, SC-007 | HIGH |
| `GateCriteria.summary()` returns correct counts | NFR-005 | MEDIUM |
| Path validation rejects missing parent dir | FR-005 | MEDIUM |
| Overwrite semantics on fresh run | FR-005 | MEDIUM |

### Integration Tests
Target: `progress.py` wired into executor, gates, convergence, wiring.

| Test | Requirement | Priority |
|------|-------------|----------|
| Executor callback produces `StepProgress` entries | FR-001, SC-001 | HIGH |
| Parallel steps get independent `duration_ms` | FR-003, SC-004 | HIGH |
| Convergence loop produces sub-entries per iteration | FR-007 | HIGH |
| Remediation entry includes `trigger_reason`, `finding_count` | FR-008 | MEDIUM |
| Remediation entry absent when remediation doesn't execute | FR-008 | MEDIUM |
| Certification entry references remediation step | FR-008 | MEDIUM |
| Wiring entry includes `unwired_count`, `orphan_count`, `blocking_count`, `rollout_mode` | FR-009 | MEDIUM |
| `--progress-file` Click option registered and passed through | FR-004 | HIGH |
| Callback is additive — no existing behavior changes | NFR-004 | HIGH |

### End-to-End (CLI Eval) Tests
Target: Real `superclaude roadmap run` invocations producing inspectable artifacts.

| Test | Requirement | Priority |
|------|-------------|----------|
| Full pipeline → parse `progress.json` → all fields present | SC-001 | CRITICAL |
| Kill mid-step → `progress.json` is valid JSON | SC-002 | CRITICAL |
| `--dry-run` outputs complete gate table | SC-003 | HIGH |
| Parallel timing: generate-A/B have distinct durations | SC-004 | HIGH |
| `--progress-file /tmp/custom.json` writes correctly | SC-005 | HIGH |
| Write overhead < 50ms per step | SC-006 | MEDIUM |
| Multi-iteration convergence produces nested sub-entries | FR-007 | HIGH |
| Wiring metadata populated from `WiringReport` | FR-009 | MEDIUM |

### Acceptance Tests
Target: Third-party verifiable artifact inspection.

| Test | Criterion |
|------|-----------|
| `progress.json` is valid JSON parseable by `jq` | SC-001, SC-002 |
| All step IDs present in output match pipeline step inventory | SC-001 |
| Dry-run table row count matches `ALL_GATES` + `WIRING_GATE` count | SC-003 |
| Timing values are non-negative integers | SC-004 |
| No regressions in existing roadmap test suite | NFR-004 |

---

## 3. Test-Implementation Interleaving Strategy

### Ratio Justification

MEDIUM complexity (0.45) → **1:2 ratio**. The core pattern (callback + atomic write) is well-understood, but cross-module integration (convergence sub-reporting, wiring metadata) requires validation checkpoints to catch data-model mismatches before they cascade.

### Execution Pattern

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Requirements Closure                               │
│   Implementation: Resolve OQs, lock schema, freeze contract │
│   ─── V1 checkpoint ───                                     │
│   Validate: Review doc, confirm traceability matrix          │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: Data Models & CLI                                  │
│   Implementation: progress.py, CLI option, executor wiring  │
│   ─── V2 gate ───                                           │
│   Validate: Unit tests + first E2E eval (SC-001 basic)      │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: Gate Summary & Special Steps                       │
│   Implementation: summary(), dry-run, convergence, wiring   │
│   ─── V3 gate ───                                           │
│   Validate: Integration tests + E2E evals (SC-003, SC-004)  │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: Full Validation & Release                          │
│   Implementation: Performance tuning, sync, edge cases      │
│   ─── V4 final gate ───                                     │
│   Validate: All SC-001–007, regression suite, sync verify   │
└─────────────────────────────────────────────────────────────┘
```

### Parallel Test Development

Phase 3 tasks 1–4 (gate summary/dry-run) can start in parallel with Phase 2. Their tests can also be written in parallel:
- **Thread A**: Unit tests for `summary()`, dry-run table rendering
- **Thread B**: Unit tests for `StepProgress`, atomic writer, CLI option

---

## 4. Risk-Based Test Prioritization

### Tier 1 — CRITICAL (test first, block on failure)

| Risk | Test Focus | Rationale |
|------|-----------|-----------|
| Crash corrupts progress file | Atomic write unit test + kill-and-parse E2E | NFR-002, SC-002: data integrity is non-negotiable |
| Progress entries missing fields | Full pipeline E2E → field assertion | SC-001: core deliverable |
| Callback alters pipeline behavior | Regression suite before/after | NFR-004: must be zero-impact |

### Tier 2 — HIGH (test before phase gate)

| Risk | Test Focus | Rationale |
|------|-----------|-----------|
| Parallel step timing incorrect | generate-A/B duration comparison | SC-004: correctness under concurrency |
| `summary()` breaks gate constants | Backward-compat unit test | RISK-003: high severity in risk inventory |
| Convergence sub-entries malformed | Integration test with multi-pass run | FR-007: complex nesting |

### Tier 3 — MEDIUM (test before release)

| Risk | Test Focus | Rationale |
|------|-----------|-----------|
| Write latency exceeds 50ms | Benchmark with/without progress | SC-006: performance budget |
| Wiring metadata incomplete | Integration test against `WiringReport` | FR-009: cross-module boundary |
| Resume vs overwrite ambiguity | Mode-specific E2E tests | RISK-005: behavioral correctness |

### Tier 4 — LOW (test if time permits)

| Risk | Test Focus | Rationale |
|------|-----------|-----------|
| Import side effects | Import + I/O monitor | SC-007: defensive, unlikely to fail |
| Custom path edge cases | Path with spaces, symlinks | FR-005: edge cases |

---

## 5. Acceptance Criteria Per Milestone

### V1 — Requirements Closure

- [ ] OQ-001 resolved: deviation sub-entry JSON schema documented with field definitions
- [ ] OQ-002 resolved: "significant findings" threshold defined (recommend: HIGH severity only)
- [ ] OQ-004 resolved: overwrite vs. resume semantics documented as two distinct modes
- [ ] OQ-005 resolved: metadata key conventions documented
- [ ] Traceability matrix: every FR/NFR/SC mapped to implementation phase and validation method
- **Gate**: Document review sign-off. No code required.

### V2 — Data Models & CLI Integration

- [ ] `progress.py` exists at `src/superclaude/cli/roadmap/progress.py`
- [ ] `import superclaude.cli.roadmap.progress` produces zero I/O (SC-007)
- [ ] `StepProgress` and `PipelineProgress` serialize to valid JSON
- [ ] Atomic write uses `os.replace()` — verified by unit test
- [ ] `--progress-file` option appears in `superclaude roadmap run --help`
- [ ] Path validation rejects nonexistent parent directory
- [ ] Full pipeline run produces `progress.json` with one entry per step (SC-001 basic)
- [ ] All core fields populated: `step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`
- [ ] Existing roadmap test suite passes (regression)
- **Gate**: Unit tests pass + basic E2E eval produces valid artifact.

### V3 — Gate Summary & Special Steps

- [ ] `GateCriteria.summary()` returns tier, required field count, semantic check count
- [ ] No existing gate constant signatures changed (backward compat)
- [ ] `--dry-run` outputs Markdown table with all gate entries including conditional steps
- [ ] Parallel steps (generate-A, generate-B) have independent `duration_ms` values (SC-004)
- [ ] Convergence sub-entries record iteration count and per-pass metrics (FR-007)
- [ ] Remediation entry: `metadata.trigger_reason` and `metadata.finding_count` present when executed
- [ ] Remediation entry absent when remediation does not execute
- [ ] Certification entry references remediation step in metadata
- [ ] Wiring entry: `metadata.unwired_count`, `orphan_count`, `blocking_count`, `rollout_mode` populated (FR-009)
- **Gate**: Integration tests pass + E2E evals for SC-003, SC-004.

### V4 — Release Readiness

- [ ] SC-001: Complete `progress.json` with all fields — E2E verified
- [ ] SC-002: Crash-safe JSON — kill-and-parse verified
- [ ] SC-003: Dry-run table complete — E2E verified
- [ ] SC-004: Parallel timing accurate — E2E verified
- [ ] SC-005: Custom path works — E2E verified
- [ ] SC-006: Write overhead < 50ms — benchmark verified
- [ ] SC-007: Zero import side effects — verified
- [ ] Convergence, remediation, certification, wiring metadata — E2E verified
- [ ] `make sync-dev` and `make verify-sync` pass
- [ ] No unintended CLI or API regressions
- [ ] All artifacts third-party inspectable
- **Gate**: All 7 success criteria pass. Feature approved for merge.

---

## 6. Quality Gates Between Phases

### Gate G1: Phase 1 → Phase 2
- **Type**: Document review
- **Pass criteria**: All OQs resolved with written decisions; traceability matrix complete
- **Failure action**: MAJOR — stop-and-fix. Cannot begin implementation on ambiguous foundations.
- **Approver**: Stakeholder sign-off on schema decisions

### Gate G2: Phase 2 → Phase 3
- **Type**: Code + test validation
- **Pass criteria**: V2 acceptance criteria met; unit tests green; basic E2E produces valid `progress.json`
- **Failure action**: 
  - CRITICAL (no progress file produced): stop-and-fix in Phase 2
  - MAJOR (fields missing/wrong): stop-and-fix before Phase 3
  - MINOR (formatting, edge cases): track, fix in Phase 3 or 4
- **Evidence required**: Test run output, sample `progress.json` artifact

### Gate G3: Phase 3 → Phase 4
- **Type**: Integration + E2E validation
- **Pass criteria**: V3 acceptance criteria met; integration tests green; dry-run and parallel timing E2E pass
- **Failure action**:
  - CRITICAL (gate summary breaks existing gates): stop-and-fix, revert `summary()` if needed
  - MAJOR (special-step metadata wrong): stop-and-fix before validation phase
  - MINOR (cosmetic table formatting): track for Phase 4
- **Evidence required**: Dry-run table output, enriched `progress.json` with special-step entries

### Gate G4: Release Gate
- **Type**: Full validation suite
- **Pass criteria**: All V4 acceptance criteria met; all 7 SC pass; sync verified; regression suite green
- **Failure action**:
  - CRITICAL or MAJOR: Block merge. Fix and re-run full validation.
  - MINOR: May merge with tracking issue created
  - COSMETIC: Merge permitted, backlog item created
- **Evidence required**: Complete eval run artifacts, benchmark results, `make verify-sync` output

### Gate Escalation Protocol

```
Issue found during validation
    │
    ├── CRITICAL → Stop immediately. Fix in current phase.
    │              Re-run all tests for current phase before proceeding.
    │
    ├── MAJOR → Complete current test run. Fix before next gate.
    │           Re-run failed tests + regression suite.
    │
    ├── MINOR → Log issue. Continue current phase.
    │           Fix in next sprint. No re-run required.
    │
    └── COSMETIC → Backlog. No action required.
```
