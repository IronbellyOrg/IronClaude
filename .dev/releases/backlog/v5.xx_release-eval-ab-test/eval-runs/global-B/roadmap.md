---
spec_source: extraction.md
complexity_score: 0.45
primary_persona: architect
---

# Roadmap: Pipeline Progress Reporting (v3.0 Unified Audit Gating)

## 1. Executive Summary

This roadmap covers adding **progress file reporting** to the `superclaude roadmap run` pipeline. The feature captures per-step results (status, timing, gate verdicts, step-specific metadata) as crash-safe JSON, with dry-run gate summaries and convergence loop sub-reporting.

**Scope**: 1 new file (`progress.py`), modifications to 4 existing files (`commands.py`, `executor.py`, `gates.py`, `models.py`). No new modules, no threading, no streaming.

**Key architectural decisions**:
- Atomic file writes (`write-to-tmp` + `os.replace()`) for crash safety
- Sequential callback invocation even for parallel steps — no concurrency in the reporter
- All step-specific fields go in `StepProgress.metadata` dict, keeping the core dataclass stable
- Wrapped JSON format (full rewrite per step), not JSONL

**Key risk**: Two spec ambiguities (deviation sub-entry schema GAP-002, remediation trigger threshold GAP-003) must be resolved before Phase 5 work begins.

---

## 2. Phased Implementation Plan

### Phase 1 — Foundation: Data Models + Atomic Writer
**Goal**: Establish `progress.py` with core data models and crash-safe write mechanism.

| # | Task | Files | Requirements |
|---|------|-------|-------------|
| 1.1 | Implement `StepProgress` dataclass (`step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`, `metadata: dict`) | `progress.py` (new) | FR-8 |
| 1.2 | Implement `PipelineProgress` dataclass (`spec_file`, `started_at`, `steps`, `completed`) | `progress.py` | FR-8 |
| 1.3 | Implement `ProgressReporter` class with atomic write (`write-to-tmp` + `os.replace()`) | `progress.py` | FR-1, FR-7, NFR-2 |
| 1.4 | Implement `record_step()` method that appends `StepProgress` to `PipelineProgress.steps` and writes | `progress.py` | FR-1 |
| 1.5 | Verify zero I/O at import time | `progress.py` | NFR-3 |

**Milestone**: `progress.py` exists, can be instantiated with a path, records steps, and produces valid JSON after every write. All writes are atomic. Import has no side effects.

**Validation**:
- Unit test: write 10 steps sequentially, verify JSON validity after each write
- Unit test: import module, assert no files created
- Benchmark: write latency < 50ms per step (NFR-1)

---

### Phase 2 — CLI + Gate Summary (parallelizable)
**Goal**: Wire `--progress-file` into the CLI and add `summary()` to gate constants.

These two tasks are independent and can be developed in parallel.

| # | Task | Files | Requirements |
|---|------|-------|-------------|
| 2.1 | Add `--progress-file` option to `roadmap run` command, default `{output_dir}/progress.json`, validate parent directory | `commands.py` | FR-2 |
| 2.2 | Handle overwrite vs. resume: overwrite by default, append when `--resume` is active | `commands.py` | FR-2, FR-11 |
| 2.3 | Add `summary()` method to gate constants for dry-run Markdown table generation | `gates.py` | FR-9, NFR-4 |

**Milestone**: CLI accepts `--progress-file`, validates the path, and the gate summary method exists for dry-run use.

**Validation**:
- CLI test: `--progress-file /tmp/test.json` creates file at specified path
- CLI test: default path resolves to `{output_dir}/progress.json`
- CLI test: invalid parent directory fails before pipeline starts
- Unit test: `summary()` returns expected columns (Step, Gate Tier, Required Fields, Semantic Checks)

---

### Phase 3 — Executor Wiring
**Goal**: Connect `ProgressReporter` to `execute_pipeline()` via post-step callback.

| # | Task | Files | Requirements |
|---|------|-------|-------------|
| 3.1 | Instantiate `ProgressReporter` in `execute_roadmap()` with the resolved progress file path | `executor.py` | FR-10 |
| 3.2 | Wire `reporter.record_step()` as the `on_step_complete` callback | `executor.py` | FR-10, NFR-5 |
| 3.3 | Ensure callback is invoked sequentially even for parallel steps (generate-A, generate-B) | `executor.py` (via `pipeline/executor.py`) | FR-1, NFR-5 |
| 3.4 | Set `PipelineProgress.completed = True` after final step succeeds | `executor.py` | FR-8 |

**Milestone**: Running `superclaude roadmap run --progress-file out.json` produces a valid progress file with entries for every executed step.

**Validation**:
- Integration test: run pipeline end-to-end, verify progress file has entries for all steps
- Integration test: parallel steps produce independent entries with correct timing
- Integration test: kill pipeline mid-run, verify progress file is valid JSON with partial entries

---

### Phase 4 — Dry-Run Enrichment
**Goal**: `--dry-run` outputs a Markdown gate summary table.

| # | Task | Files | Requirements |
|---|------|-------|-------------|
| 4.1 | When `--dry-run` is set, build Markdown table from gate `summary()` output | `commands.py` or `executor.py` | FR-3 |
| 4.2 | Include all steps: regular and conditional (remediate, certify), marking conditional steps explicitly | `commands.py` or `executor.py` | FR-3 |

**Milestone**: `superclaude roadmap run --dry-run` prints a complete gate summary table to stdout.

**Validation**:
- Test: dry-run output contains all pipeline steps
- Test: conditional steps (remediate, certify) are marked as conditional
- Test: table columns match spec (Step, Gate Tier, Required Fields, Semantic Checks)

---

### Phase 5 — Advanced Reporting (Deviation + Remediation + Wiring)
**Goal**: Enrich progress entries with step-specific metadata for convergence loop, remediation, and wiring verification.

**Prerequisite**: GAP-002 (deviation sub-entry schema) must be resolved before task 5.1.

| # | Task | Files | Requirements |
|---|------|-------|-------------|
| 5.1 | Capture deviation analysis iterations as sub-entries in `StepProgress.metadata["iterations"]`; record `pass_count` | `progress.py`, convergence loop call site | FR-4 |
| 5.2 | When remediation executes, populate `metadata["trigger_reason"]` and `metadata["finding_count"]` | remediation call site | FR-5 |
| 5.3 | Certification step entry references remediation via `metadata["remediates_step_id"]` | certification call site | FR-5 |
| 5.4 | Wiring step entry populates `metadata["unwired_count"]`, `metadata["orphan_count"]`, `metadata["blocking_count"]`, `metadata["rollout_mode"]`; gate verdict reflects `WIRING_GATE` results | wiring call site | FR-6 |

**Milestone**: Progress file contains rich metadata for deviation, remediation, and wiring steps.

**Validation**:
- Test: deviation entry contains iteration sub-entries with pass count
- Test: remediation entry has trigger_reason and finding_count only when remediation ran
- Test: certification entry references remediation step_id
- Test: wiring entry contains all four wiring fields; gate verdict matches wiring gate result

---

## 3. Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Mitigation |
|---|------|----------|------------|------------|
| R1 | **GAP-002: Deviation sub-entry schema undefined** | High | Certain | Resolve before Phase 5.1. Propose: `metadata["iterations"]` as list of `{"iteration": int, "score": float, "findings": list}` dicts. Get spec owner sign-off. |
| R2 | **GAP-003: Remediation trigger threshold ambiguous** | Medium | Likely | Implement as `HIGH` severity only (matching workflow diagram Section 2.2). Document the decision. Make threshold configurable if needed later. |
| R3 | **Resume vs. overwrite semantic conflict** | Medium | Certain | Resolve in Phase 2.2: `--resume` flag overrides default overwrite behavior. When `--resume` active, load existing file and append. When absent, overwrite. |
| R4 | **Completed flag semantics undefined** | Low | Certain | Set `completed = True` only when pipeline reaches terminal state without crash. Crash leaves `completed = False` (default). |
| R5 | **Metadata field placement ambiguity** | Low | Certain | Use `metadata` dict for all step-specific fields (trigger_reason, finding_count, wiring counts). Preserves `StepProgress` as a stable, generic dataclass. |
| R6 | **Callback doesn't exist in execute_pipeline()** | Medium | Possible | Verify in prerequisite check. If absent, Phase 3 expands by ~1 effort unit to add the callback mechanism to `pipeline/executor.py`. |
| R7 | **Atomic write performance on network filesystems** | Low | Unlikely | The < 50ms budget is generous for `os.replace()` on local disk. Benchmark in CI. Only becomes a concern on network mounts. |

---

## 4. Resource Requirements and Dependencies

### Files Modified

| File | Phase | Change Type |
|------|-------|-------------|
| `src/superclaude/cli/roadmap/progress.py` | 1 | **New file** — `StepProgress`, `PipelineProgress`, `ProgressReporter` |
| `src/superclaude/cli/roadmap/commands.py` | 2, 4 | Add `--progress-file` option, dry-run table output |
| `src/superclaude/cli/roadmap/gates.py` | 2 | Add `summary()` method to gate constants |
| `src/superclaude/cli/roadmap/executor.py` | 3 | Wire `ProgressReporter` into `execute_roadmap()` callback |
| `src/superclaude/cli/pipeline/executor.py` | 3 | Verify/ensure sequential callback invocation for parallel steps |

### Internal Dependencies
- `execute_pipeline()` must support `on_step_complete` callback. If not, Phase 3 scope expands.
- `--resume` flag must already exist in CLI. If not, Phase 2 scope expands.
- Gate constants structure in `gates.py` must support adding methods.

### External Dependencies
- None. No new packages or services required.

### Prerequisite Verification (before Phase 1 starts)
1. Confirm `execute_pipeline()` has or can accept a post-step callback parameter
2. Confirm `--resume` flag exists in `commands.py`
3. Confirm gate constants structure in `gates.py` supports adding methods

---

## 5. Success Criteria and Validation Approach

### Acceptance Criteria
1. `superclaude roadmap run` produces a valid `progress.json` after every step, including on crash
2. `--progress-file` overrides default path; `--resume` appends instead of overwriting
3. `--dry-run` outputs a Markdown table covering all steps with gate metadata
4. Deviation analysis iterations appear as sub-entries with pass count
5. Remediation entries include trigger reason and finding count; certification references remediation
6. Wiring entries include all four wiring fields; verdict reflects gate results
7. Write latency < 50ms per step
8. `import progress` creates no files

### Validation Strategy
- **Phase 1-2**: Unit tests covering data models, atomic writes, CLI option parsing, gate summary
- **Phase 3**: Integration tests covering end-to-end pipeline run, crash recovery, parallel step ordering
- **Phase 4**: Output assertion tests covering dry-run table format and completeness
- **Phase 5**: Integration tests with mock convergence/remediation/wiring scenarios
- **All phases**: Eval tests per the v3.0 eval suite pattern — invoke actual CLI, produce real artifacts, verify with third-party tooling (JSON schema validation, file existence checks)

---

## 6. Timeline Estimates

| Phase | Effort | Dependencies | Parallelizable |
|-------|--------|-------------|----------------|
| Phase 1 — Foundation | Small (1 unit) | None | — |
| Phase 2 — CLI + Gate Summary | Small (1 unit) | Phase 1 | 2.1/2.2 ∥ 2.3 |
| Phase 3 — Executor Wiring | Medium (1.5 units) | Phase 1, Phase 2.1 | — |
| Phase 4 — Dry-Run Enrichment | Small (0.5 units) | Phase 2.3, Phase 3 | — |
| Phase 5 — Advanced Reporting | Medium (1.5 units) | Phase 3, GAP-002 resolution | 5.1 ∥ 5.2 ∥ 5.3 ∥ 5.4 |

**Total**: ~5.5 effort units.

**Critical path**: Phase 1 → Phase 2.1 → Phase 3 → Phase 5 (blocked on GAP-002 resolution)

**Parallelism opportunities** reduce wall-clock time to ~4.5 units:
- Phase 2: tasks 2.1/2.2 and 2.3 run in parallel
- Phase 5: tasks 5.1 through 5.4 are largely independent

### Blocking Dependencies
- **GAP-002 resolution** gates Phase 5.1 start. All other phases can proceed without spec clarification.
- **Prerequisite verification** (callback existence) gates Phase 3. If callback doesn't exist, add ~1 unit to Phase 3.
