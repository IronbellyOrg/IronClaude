---
spec_source: "eval-spec.md"
complexity_score: 0.45
adversarial: true
---

# Roadmap: Progress Reporting & Dry-Run Gate Summary for Roadmap Pipeline

## 1. Executive Summary

This roadmap delivers **pipeline progress reporting** and **dry-run gate summaries** for the `superclaude roadmap run` command. The feature adds structured JSON observability into pipeline execution — crash-safe via atomic writes — and exposes gate metadata through a `--dry-run` summary table.

**Scope**: 17 requirements (12 functional, 5 non-functional) across 4 domains (backend, CLI, observability, testing). Complexity is MEDIUM (0.45) — integration-heavy but architecturally straightforward, touching 3 existing files and creating 1 new module (`progress.py`).

**Architectural approach**: All progress logic is contained in a single new file integrated via the existing `on_step_complete` callback — no new threads, watchers, or observer patterns. Gate visibility is additive-only via a `summary()` method on `GateCriteria`.

**Critical path**: Phase 0 resolves blocking open questions (OQ-001, OQ-002, OQ-004) before integration work begins. Phase 1 → Phase 2 → Phase 4 → Phase 5 → Phase 6 is the critical path. Phase 3 runs in parallel with Phase 2.

**Key technical note**: `StepResult` lives in `cli/pipeline/models.py`, not `cli/roadmap/models.py` — the extraction document's dependency table is misleading on this point.

---

## 2. Phased Implementation Plan

### Phase 0 — Specification Closure (0.5 day)

**Goal**: Eliminate ambiguity blockers before code changes. Gates Phase 2 entry.

| # | Task | Requirements | Deliverable |
|---|------|-------------|-------------|
| 0.1 | Resolve OQ-001: deviation sub-entry schema — decide nesting structure for convergence iteration entries | Blocks FR-009 | Decision record: schema shape |
| 0.2 | Resolve OQ-002: "significant findings" threshold for remediation trigger | Blocks FR-010 | Decision record: threshold definition |
| 0.3 | Resolve OQ-004: resume-vs-overwrite semantics — confirm `--resume` appends, fresh run overwrites, or defer `--resume` from scope | FR-007 | Decision record: scope ruling |
| 0.4 | Freeze progress JSON shape: top-level pipeline structure, step entry shape, conditional-step representation | FR-001 | Approved schema document |

**Validation gate**: Written decision records for OQ-001, OQ-002, OQ-004. Schema decisions require architectural review — schema approval gates Phase 2 entry.

**Recommended defaults if stakeholder unavailable**:
- OQ-001: Nest as `sub_steps: list[StepProgress]` within parent spec-fidelity entry
- OQ-002: Use `severity == "HIGH"` as threshold (matches Section 3 comment)
- OQ-004: `--resume` appends; fresh run overwrites. Both behaviors are useful; if `--resume` is out of scope, overwrite-only and document the deferral.

---

### Phase 1 — Foundation: Data Model & Atomic Writer (1 day)

**Goal**: `StepProgress` / `PipelineProgress` dataclasses + atomic JSON writer.
**Milestone**: `progress.py` passes tests for serialization and crash safety.

| # | Task | Requirements | Files |
|---|------|-------------|-------|
| 1.1 | Define `StepProgress` dataclass with 5 required fields (`step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`) plus `metadata: dict` | FR-001, FR-002, SC-002 | `progress.py` (new) |
| 1.2 | Define `PipelineProgress` dataclass wrapping `list[StepProgress]` with `to_json()` / `from_json()` | FR-001, FR-003 | `progress.py` |
| 1.3 | Implement atomic writer: `write_progress(path, progress)` using `tempfile` + `os.replace()` | FR-003, NFR-002, SC-008 | `progress.py` |
| 1.4 | Implement overwrite-on-start behavior (per Phase 0 decision on resume semantics) | FR-007 | `progress.py` |
| 1.5 | Verify zero import-time side effects | NFR-003, SC-009 | `progress.py` |
| 1.6 | Write tests: serialization round-trip, atomic write crash simulation, import-time I/O check | SC-001, SC-008, SC-009 | `tests/roadmap/test_progress.py` |

**Validation gate**: All Phase 1 tests green. `import superclaude.cli.roadmap.progress` produces no filesystem I/O.

---

### Phase 2 — Pipeline Integration: Callback Wiring & CLI Option (1.5 days)

**Goal**: Progress file is written during real pipeline execution.
**Milestone**: `superclaude roadmap run --progress-file /tmp/p.json` produces valid progress output.

**Prerequisite**: Phase 0 decisions finalized; Phase 1 complete.

| # | Task | Requirements | Files |
|---|------|-------------|-------|
| 2.1 | Add `--progress-file` Click option to `roadmap run` command with `click.Path` type, default `{output_dir}/progress.json` | FR-005, FR-006, SC-003, SC-004 | `commands.py` |
| 2.2 | Add path validation: fail fast if parent directory does not exist | FR-006, SC-003 | `commands.py` |
| 2.3 | Create `progress_callback(step, result) -> None` that maps `StepResult` → `StepProgress` and calls `write_progress()` | FR-001, FR-004, NFR-004 | `progress.py` |
| 2.4 | Wire `progress_callback` into `execute_pipeline()` alongside existing `_print_step_complete` in `executor.py` | FR-001, FR-002 | `executor.py` (lines ~1325, ~1535) |
| 2.5 | Handle parallel steps: verify `on_step_complete` sequential invocation guarantees correct per-step timing | FR-004, NFR-004, RISK-002 | `executor.py` (verify only) |
| 2.6 | Write integration tests: CLI option parsing, path validation, overwrite behavior, parallel step entries | SC-003, SC-004 | `tests/roadmap/test_progress.py` |

**Import note**: `StepResult` lives in `superclaude.cli.pipeline.models`, not `roadmap.models`.

**Validation gate**: End-to-end run produces progress file with correct structure. Parallel generate steps produce independent entries.

---

### Phase 3 — Gate Summary & Dry-Run Reporting (1 day)

**Goal**: `--dry-run` outputs a Markdown table of all gate definitions.
**Milestone**: Dry-run output includes complete gate table with all 13 gates.

**Note**: Phase 3 can run **in parallel with Phase 2** — they share no code dependencies. Both depend only on Phase 1 outputs.

| # | Task | Requirements | Files |
|---|------|-------------|-------|
| 3.1 | Add `summary()` method to `GateCriteria` class (additive only — no signature changes) | FR-012, NFR-005, RISK-003 | `gates.py` |
| 3.2 | `summary()` returns dict with keys: `step`, `gate_tier`, `required_fields`, `semantic_checks` | FR-008, SC-005 | `gates.py` |
| 3.3 | Implement dry-run gate table renderer: iterate `ALL_GATES`, call `summary()`, format Markdown table | FR-008, SC-005 | `executor.py` or `commands.py` |
| 3.4 | Mark conditional steps (remediate, certify) explicitly in the table output | FR-008 | Same as 3.3 |
| 3.5 | Write tests: verify table has all 13 gates, conditional marking, column completeness | SC-005 | `tests/roadmap/test_progress.py` |

**Validation gate**: `superclaude roadmap run --dry-run` prints Markdown table with Step, Gate Tier, Required Fields, Semantic Checks for all 13 gates. Existing gate validation behavior unchanged (regression test).

---

### Phase 4 — Advanced Reporting: Convergence, Remediation, Wiring (1.5 days)

**Goal**: Specialized progress entries for deviation analysis, remediation triggers, and wiring verification.
**Milestone**: All 12 FRs satisfied.

**Prerequisite**: Phase 2 complete. OQ-001 and OQ-002 resolved in Phase 0.

| # | Task | Requirements | Files |
|---|------|-------------|-------|
| 4.1 | Deviation analysis sub-entries: each convergence iteration writes a sub-entry; pass count recorded (per OQ-001 schema decision) | FR-009 | `progress.py`, `convergence.py` |
| 4.2 | Remediation trigger reporting: `trigger_reason` + `finding_count` in progress entry; certification references remediation (per OQ-002 threshold decision) | FR-010 | `progress.py`, `executor.py` |
| 4.3 | Wiring verification entry: include `unwired_count`, `orphan_count`, `blocking_count`, `rollout_mode` | FR-011, SC-006 | `progress.py`, integration with `wiring_gate.py` |
| 4.4 | Write tests: deviation sub-entries, remediation metadata, wiring counts | SC-006 | `tests/roadmap/test_progress.py` |

**Validation gate**: Progress file for a full pipeline run contains correct deviation sub-entries, remediation metadata, and wiring verification fields.

---

### Phase 5 — Performance Validation & Hardening (1 day)

**Goal**: NFR compliance verified under measurement.
**Milestone**: All 9 success criteria pass.

| # | Task | Requirements | Files |
|---|------|-------------|-------|
| 5.1 | Benchmark progress write latency: measure < 50ms per step | NFR-001, SC-007 | `tests/roadmap/test_progress.py` |
| 5.2 | Crash safety test: kill pipeline mid-write, verify valid JSON | NFR-002, SC-008 | `tests/roadmap/test_progress.py` |
| 5.3 | Full success criteria sweep (SC-001 through SC-009) | All SC-* | Test suite |
| 5.4 | Validate additive-only gate extension: regression test all existing `GateCriteria` consumers | RISK-003 | `tests/roadmap/test_gates.py` |

**Validation gate**: All 9 success criteria pass. Performance benchmark under 50ms. No regressions in existing gate behavior.

---

### Phase 6 — Release Readiness (0.5 day)

**Goal**: Ship safely with low regression risk.

| # | Task | Requirements | Deliverable |
|---|------|-------------|-------------|
| 6.1 | Run `make verify-sync` to confirm `src/superclaude/` ↔ `.claude/` consistency | Release hygiene | Sync verification pass |
| 6.2 | Execute representative validation run against a real roadmap spec | Release validation | Sample progress file + dry-run output |
| 6.3 | Confirm no regression in existing roadmap execution paths | Release safety | Existing test suite green |
| 6.4 | Prepare release notes: new progress reporting, dry-run visibility, operational expectations | Release documentation | Release notes |

**Validation gate**: Sync confirmed, representative run successful, all tests green.

---

## 3. Risk Assessment and Mitigation

| Risk | Severity | Probability | Mitigation | Phase |
|------|----------|-------------|------------|-------|
| **RISK-001**: Progress writes slow down pipeline | Low | Very Low | Pipeline steps take minutes; write is < 50ms. Benchmark in Phase 5. No action unless benchmark fails. | Phase 5 |
| **RISK-002**: Concurrent generate steps corrupt progress file | Medium | Low | Verify `execute_pipeline()` sequential callback guarantee in Phase 2.5. Add explicit assertion in test. Centralize all writes in one callback pathway. | Phase 2 |
| **RISK-003**: `summary()` method breaks gate constants | High | Low | Additive-only change; no signature modifications. Regression test all existing `GateCriteria` usage in Phase 5.4. Review all call sites before merge. | Phase 3, 5 |
| **RISK-004**: Seeded ambiguities propagate as undefined behavior | Medium | High (by design) | Phase 0 resolves OQ-001, OQ-002, OQ-004 before dependent implementation. If stakeholder unavailable, use documented defaults and proceed. | Phase 0 |
| **RISK-005**: Resume semantics conflict with overwrite requirement | Medium | Medium | Phase 0 establishes single rule for standard run vs resumed run. Encode that rule in CLI tests. Avoid implicit behavior based on file existence alone. | Phase 0, 2 |
| **Implicit risk**: `StepResult` import path mismatch | Low | N/A | Import from `superclaude.cli.pipeline.models`, not `roadmap.models`. Extraction document's dependency table entry #3 is misleading — use actual import path. | Phase 1 |

---

## 4. Resource Requirements and Dependencies

### Internal Dependencies (Integration Order)

1. **`cli/pipeline/models.py`** — `StepResult` dataclass (read-only dependency, Phase 1)
2. **`cli/roadmap/gates.py`** — Gate constants; additive `summary()` method (Phase 3)
3. **`cli/roadmap/commands.py`** — Click option registration (Phase 2)
4. **`cli/roadmap/executor.py`** — Callback wiring at lines ~1325 and ~1535 (Phase 2, 4)
5. **`cli/roadmap/convergence.py`** — Deviation analysis loop integration (Phase 4)
6. **`cli/audit/wiring_gate.py`** — `WIRING_GATE` fields for progress entries (Phase 4)

### External Dependencies

- Python `os` stdlib (`os.replace()`)
- Python `json` stdlib
- Python `tempfile` stdlib
- No new third-party packages required

### Blocking Dependencies

- **OQ-001** (deviation sub-entry schema) blocks Phase 4, Task 4.1
- **OQ-002** ("significant findings" threshold) blocks Phase 4, Task 4.2
- **OQ-004** (resume semantics) blocks Phase 1, Task 1.4

### Architectural Constraints

1. Only one new file: `src/superclaude/cli/roadmap/progress.py`
2. No change to gate validation logic behavior
3. No new third-party packages
4. Python 3.10+ compatible typing and dataclasses only
5. All runs and tests via `uv run`

### Review Expectations

Schema decisions (Phase 0) require architectural review. Crash-safety and benchmark testing (Phase 5) benefit from independent validation to avoid confirmation bias. These are review checkpoints, not staffing requirements — a single engineer can fill all roles.

---

## 5. Success Criteria and Validation Approach

| Criterion | Validation Method | Phase |
|-----------|-------------------|-------|
| **SC-001**: Valid JSON after every step | Integration test: run pipeline, parse progress after each step | Phase 2 |
| **SC-002**: 5 required fields per entry | Schema validation test on every `StepProgress` instance | Phase 1 |
| **SC-003**: `--progress-file` accepted and validated | CLI test: valid path passes, missing parent fails | Phase 2 |
| **SC-004**: Default path = `{output_dir}/progress.json` | CLI test: omit option, verify default location | Phase 2 |
| **SC-005**: Dry-run gate table with 13 gates | Output capture test: assert Markdown table structure and row count | Phase 3 |
| **SC-006**: Wiring entry includes 4 fields | Integration test: verify progress entry contains `unwired_count`, `orphan_count`, `blocking_count`, `rollout_mode` | Phase 4 |
| **SC-007**: Write latency < 50ms | Benchmark test: time 100 writes, assert p99 < 50ms | Phase 5 |
| **SC-008**: Crash-safe JSON | Simulated crash test: kill during write, verify valid JSON on disk | Phase 5 |
| **SC-009**: Zero import-time I/O | Import test: `import progress`, assert no files created | Phase 1 |

**Validation approach**: Each phase has its own gate. Tests are eval-style (real CLI invocation, real artifacts) per project conventions — not mocked unit tests on internal functions. Final acceptance requires evidence mapped to SC-001 through SC-009.

---

## 6. Timeline Estimates

| Phase | Name | Duration | Dependencies | Exit Condition |
|-------|------|----------|-------------|----------------|
| 0 | Specification Closure | 0.5 day | None | Blocking ambiguities resolved, schema approved |
| 1 | Foundation | 1 day | Phase 0 | Atomic progress writer passes tests |
| 2 | Pipeline Integration | 1.5 days | Phase 1 | End-to-end step reporting works |
| 3 | Gate Summary & Dry-Run | 1 day | Phase 1 (parallel with Phase 2) | CLI option and gate table complete |
| 4 | Advanced Reporting | 1.5 days | Phase 2 + Phase 0 decisions | All 12 FRs satisfied |
| 5 | Performance Validation | 1 day | Phases 1–4 | All 9 success criteria pass with evidence |
| 6 | Release Readiness | 0.5 day | Phase 5 | Merge-ready, sync confirmed |

**Total estimated effort**: 7 days (6 days calendar with Phase 2/3 parallelization)

**Critical path**: Phase 0 → Phase 1 → Phase 2 → Phase 4 → Phase 5 → Phase 6 (6 days)

**Parallelization**: Phase 3 runs concurrently with Phase 2, saving 1 calendar day. They share no code dependencies — both depend only on Phase 1 outputs.

---

## 7. Open Questions — Resolution Plan

| Question | Impact | Recommended Default | Resolution Phase |
|----------|--------|-------------------|-----------------|
| **OQ-001**: Deviation sub-entry schema | Blocks Phase 4.1 | Nest as `sub_steps: list[StepProgress]` within parent spec-fidelity entry | Phase 0 |
| **OQ-002**: "Significant findings" threshold | Blocks Phase 4.2 | Use `severity == "HIGH"` as threshold | Phase 0 |
| **OQ-003**: Progress file rotation | Non-blocking | Out of scope — each run overwrites | Defer |
| **OQ-004**: Resume behavior semantics | Blocks Phase 1.4 | `--resume` appends; fresh run overwrites | Phase 0 |
| **OQ-005**: Missing Section 4.3 | Non-blocking | Likely editorial gap — no action needed | Ignore |
| **OQ-006**: Metadata field keys | Non-blocking | Treat as extension point; no mandated keys | Defer |
