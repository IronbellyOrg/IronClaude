---
spec_source: "eval-spec.md"
complexity_score: 0.45
primary_persona: architect
---

# Roadmap: Progress Reporting & Dry-Run Gate Summary for Roadmap Pipeline

## 1. Executive Summary

This roadmap covers the implementation of **pipeline progress reporting** and **dry-run gate summaries** for the `superclaude roadmap run` command. The feature adds observability into pipeline execution by writing structured JSON progress entries after each step, crash-safe via atomic writes, and exposes gate metadata through a `--dry-run` summary table.

**Scope**: 17 requirements (12 functional, 5 non-functional) across 4 domains (backend, CLI, observability, testing). Complexity is MEDIUM (0.45) — the work is integration-heavy but architecturally straightforward, touching 3 existing files and creating 1 new module.

**Critical path**: Resolve two blocking open questions (OQ-001: deviation sub-entry schema, OQ-002: "significant findings" threshold) before Phase 2 implementation begins.

**Key architectural decision**: All progress logic is contained in a single new file (`progress.py`) integrated via the existing `on_step_complete` callback — no new threads, watchers, or observer patterns.

---

## 2. Phased Implementation Plan

### Phase 1 — Foundation: Data Model & Atomic Writer
**Goal**: `StepProgress` / `PipelineProgress` dataclasses + atomic JSON writer.
**Milestone**: `progress.py` passes unit tests for serialization and crash safety.

| # | Task | Requirements | Files |
|---|------|-------------|-------|
| 1.1 | Define `StepProgress` dataclass with 5 required fields (`step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`) plus `metadata: dict` | FR-001, FR-002, SC-002 | `progress.py` (new) |
| 1.2 | Define `PipelineProgress` dataclass wrapping `list[StepProgress]` with `to_json()` / `from_json()` | FR-001, FR-003 | `progress.py` |
| 1.3 | Implement atomic writer: `write_progress(path, progress)` using `tempfile` + `os.replace()` | FR-003, NFR-002, SC-008 | `progress.py` |
| 1.4 | Verify zero import-time side effects | NFR-003, SC-009 | `progress.py` |
| 1.5 | Write tests: serialization round-trip, atomic write crash simulation, import-time I/O check | SC-001, SC-008, SC-009 | `tests/roadmap/test_progress.py` |

**Validation gate**: All Phase 1 tests green. `import superclaude.cli.roadmap.progress` produces no filesystem I/O.

---

### Phase 2 — Pipeline Integration: Callback Wiring & CLI Option
**Goal**: Progress file is written during real pipeline execution.
**Milestone**: `superclaude roadmap run --progress-file /tmp/p.json` produces valid progress output.

**Prerequisite**: OQ-001 and OQ-002 resolved (or deferred with documented defaults).

| # | Task | Requirements | Files |
|---|------|-------------|-------|
| 2.1 | Add `--progress-file` Click option to `roadmap run` command with `click.Path` type, default `{output_dir}/progress.json` | FR-005, FR-006, SC-003, SC-004 | `commands.py` |
| 2.2 | Add path validation: fail fast if parent directory does not exist | FR-006, SC-003 | `commands.py` |
| 2.3 | Implement overwrite-on-exists behavior (not append) | FR-007 | `progress.py` |
| 2.4 | Create `progress_callback(step, result) -> None` that maps `StepResult` → `StepProgress` and calls `write_progress()` | FR-001, FR-004, NFR-004 | `progress.py` |
| 2.5 | Wire `progress_callback` into `execute_pipeline()` alongside existing `_print_step_complete` in `executor.py` | FR-001, FR-002 | `executor.py` (lines ~1325, ~1535) |
| 2.6 | Handle parallel steps: verify `on_step_complete` sequential invocation guarantees correct per-step timing | FR-004, NFR-004, RISK-002 | `executor.py` (verify only) |
| 2.7 | Write integration tests: CLI option parsing, path validation, overwrite behavior | SC-003, SC-004 | `tests/roadmap/test_progress.py` |

**Validation gate**: End-to-end `--dry-run` produces progress file with correct structure. Parallel generate steps produce independent entries.

---

### Phase 3 — Gate Summary & Dry-Run Reporting
**Goal**: `--dry-run` outputs a Markdown table of all gate definitions.
**Milestone**: Dry-run output includes complete gate table with all 13 gates.

| # | Task | Requirements | Files |
|---|------|-------------|-------|
| 3.1 | Add `summary()` method to `GateCriteria` class (additive only — no signature changes) | FR-012, NFR-005, RISK-003 | `gates.py` |
| 3.2 | `summary()` returns dict with keys: `step`, `gate_tier`, `required_fields`, `semantic_checks` | FR-008, SC-005 | `gates.py` |
| 3.3 | Implement dry-run gate table renderer: iterate `ALL_GATES`, call `summary()`, format Markdown table | FR-008, SC-005 | `executor.py` or `commands.py` |
| 3.4 | Mark conditional steps (remediate, certify) explicitly in the table output | FR-008 | Same as 3.3 |
| 3.5 | Write tests: verify table has all 13 gates, conditional marking, column completeness | SC-005 | `tests/roadmap/test_progress.py` |

**Validation gate**: `superclaude roadmap run --dry-run` prints Markdown table with Step, Gate Tier, Required Fields, Semantic Checks for all 13 gates.

---

### Phase 4 — Advanced Reporting: Convergence, Remediation, Wiring
**Goal**: Specialized progress entries for deviation analysis, remediation triggers, and wiring verification.
**Milestone**: All 12 FRs satisfied.

| # | Task | Requirements | Files |
|---|------|-------------|-------|
| 4.1 | Deviation analysis sub-entries: each convergence iteration writes a sub-entry; pass count recorded | FR-009 | `progress.py`, `convergence.py` |
| 4.2 | Remediation trigger reporting: `trigger_reason` + `finding_count` in progress entry; certification references remediation | FR-010 | `progress.py`, `executor.py` |
| 4.3 | Wiring verification entry: include `unwired_count`, `orphan_count`, `blocking_count`, `rollout_mode` | FR-011, SC-006 | `progress.py`, integration with `wiring_gate.py` |
| 4.4 | Write tests: deviation sub-entries, remediation metadata, wiring counts | SC-006 | `tests/roadmap/test_progress.py` |

**Validation gate**: Progress file for a full pipeline run contains correct deviation sub-entries, remediation metadata, and wiring verification fields.

---

### Phase 5 — Performance Validation & Hardening
**Goal**: NFR compliance verified under measurement.
**Milestone**: All 9 success criteria pass.

| # | Task | Requirements | Files |
|---|------|-------------|-------|
| 5.1 | Benchmark progress write latency: measure < 50ms per step | NFR-001, SC-007 | `tests/roadmap/test_progress.py` |
| 5.2 | Crash safety test: kill pipeline mid-write, verify valid JSON | NFR-002, SC-008 | `tests/roadmap/test_progress.py` |
| 5.3 | Full success criteria sweep (SC-001 through SC-009) | All SC-* | Test suite |

**Validation gate**: All 9 success criteria pass. Performance benchmark under 50ms.

---

## 3. Risk Assessment and Mitigation

| Risk | Severity | Probability | Mitigation | Phase |
|------|----------|-------------|------------|-------|
| **RISK-003**: `summary()` method breaks gate constants | High | Low | Additive-only change; no signature modifications. Test all existing gate validation before/after. Write regression test asserting existing `GateCriteria` interface unchanged. | Phase 3 |
| **RISK-004**: Seeded ambiguities propagate as undefined behavior | Medium | High (by design) | **Block Phase 4 tasks 4.1/4.2 until OQ-001 and OQ-002 are resolved.** Document default assumptions if stakeholder unavailable. | Phase 2→4 boundary |
| **RISK-002**: Concurrent generate steps corrupt progress file | Medium | Low | Verify `execute_pipeline()` sequential callback guarantee in Phase 2.6. Add explicit assertion in test. | Phase 2 |
| **RISK-001**: Progress writes slow down pipeline | Low | Very Low | Benchmark in Phase 5. Pipeline steps take minutes; write is < 50ms. No mitigation needed unless benchmark fails. | Phase 5 |
| **Implicit risk**: `StepResult` lives in `pipeline/models.py`, not `roadmap/models.py` | Low | N/A | Import from `superclaude.cli.pipeline.models`, not `roadmap.models`. Extraction document's dependency table entry #3 is misleading — use actual import path. | Phase 1 |

---

## 4. Resource Requirements and Dependencies

### Internal Dependencies (Integration Order)

1. **`cli/pipeline/models.py`** — `StepResult` dataclass (read-only dependency, Phase 1)
2. **`cli/roadmap/gates.py`** — Gate constants; additive `summary()` method (Phase 3)
3. **`cli/roadmap/commands.py`** — Click option registration (Phase 2)
4. **`cli/roadmap/executor.py`** — Callback wiring at lines ~1325 and ~1535 (Phase 2)
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

---

## 5. Success Criteria and Validation Approach

| Criterion | Validation Method | Phase |
|-----------|-------------------|-------|
| **SC-001**: Valid JSON after every step | Integration test: run pipeline, parse progress after each step | Phase 2 |
| **SC-002**: 5 required fields per entry | Schema validation test on every `StepProgress` instance | Phase 1 |
| **SC-003**: `--progress-file` accepted and validated | CLI test: valid path passes, missing parent fails | Phase 2 |
| **SC-004**: Default path = `{output_dir}/progress.json` | CLI test: omit option, verify default location | Phase 2 |
| **SC-005**: Dry-run gate table with 13 gates | Output capture test: assert Markdown table structure and row count | Phase 3 |
| **SC-006**: Wiring entry includes 4 fields | Integration test: mock wiring results, verify progress entry | Phase 4 |
| **SC-007**: Write latency < 50ms | Benchmark test: time 100 writes, assert p99 < 50ms | Phase 5 |
| **SC-008**: Crash-safe JSON | Simulated crash test: kill during write, verify valid JSON on disk | Phase 5 |
| **SC-009**: Zero import-time I/O | Import test: `import progress`, assert no files created | Phase 1 |

**Validation approach**: Each phase has its own gate. Tests are eval-style (real CLI invocation, real artifacts) per project conventions — not mocked unit tests on internal functions.

---

## 6. Timeline Estimates per Phase

| Phase | Estimated Effort | Dependencies |
|-------|-----------------|--------------|
| Phase 1 — Foundation | Small (data model + atomic writer) | None |
| Phase 2 — Pipeline Integration | Medium (callback wiring + CLI) | Phase 1 |
| Phase 3 — Gate Summary | Small (additive `summary()` + renderer) | Phase 1 (independent of Phase 2) |
| Phase 4 — Advanced Reporting | Medium (3 specialized integrations) | Phase 2 + OQ-001/OQ-002 resolved |
| Phase 5 — Performance Validation | Small (benchmarks + sweep) | Phases 1–4 |

**Parallelization opportunity**: Phase 3 can run in parallel with Phase 2 — they share no code dependencies.

**Critical path**: Phase 1 → Phase 2 → Phase 4 → Phase 5. Phase 3 is off critical path.

---

## 7. Open Questions — Resolution Plan

| Question | Impact | Recommended Default | Resolution Owner |
|----------|--------|-------------------|------------------|
| **OQ-001**: Deviation sub-entry schema | Blocks Phase 4.1 | Nest as `sub_steps: list[StepProgress]` within parent spec-fidelity entry | Stakeholder |
| **OQ-002**: "Significant findings" threshold | Blocks Phase 4.2 | Use `severity == "HIGH"` as threshold (matches Section 3 comment) | Stakeholder |
| **OQ-003**: Progress file rotation | Non-blocking | Out of scope — each run overwrites | Defer |
| **OQ-004**: Resume behavior contradiction | Non-blocking | `--resume` appends; fresh run overwrites. Both behaviors are useful. | Clarify in spec |
| **OQ-005**: Missing Section 4.3 | Non-blocking | Likely editorial gap — no action needed | Ignore |
| **OQ-006**: Metadata field keys | Non-blocking | Treat as extension point; no mandated keys | Defer |
