---
spec_source: extraction.md
complexity_score: 0.45
primary_persona: architect
---

# Roadmap: Pipeline Progress Tracking for Unified Audit Gating (v3.0)

## 1. Executive Summary

This roadmap delivers **observable pipeline execution** for `superclaude roadmap run` by adding a crash-safe JSON progress file that records step outcomes, gate verdicts, timing, and step-specific metadata after each pipeline step completes.

**Scope**: 1 new module (`progress.py`), 3 modified modules (`commands.py`, `executor.py`, `gates.py` constants only), plus tests. No changes to gate enforcement logic. The dependency direction is strictly downward: `commands.py → executor.py → progress.py → models.py/gates.py`.

**Key architectural decisions**:
- Post-step callback hook on the existing `execute_pipeline()` — no new threads, observers, or async patterns.
- Atomic JSON rewrite (`write-to-tmp` + `os.replace()`) guarantees crash safety.
- Sequential callback invocation even for parallel steps prevents file corruption without locking.

**Blocking prerequisite**: GAP-002 (deviation sub-entry schema) must be resolved before Phase 4.2 begins.

**Complexity**: 0.45 (moderate). Single-sprint scope: 24 tasks across 5 phases with clear dependency ordering and identified parallelism opportunities.

---

## 2. Phased Implementation Plan

### Phase 1 — Data Model & Core Writer (Foundation)

**Goal**: Establish `progress.py` with data models, atomic write capability, and gate summary support.

| # | Task | Files | Depends On | FR Coverage |
|---|------|-------|------------|-------------|
| 1.1 | Define `PipelineProgress` dataclass (`spec_file`, `started_at` ISO 8601, `steps` list, `completed` bool) | `roadmap/progress.py` (new) | — | FR-8 |
| 1.2 | Define `StepProgress` dataclass (`step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`, `metadata` dict) | `roadmap/progress.py` | 1.1 | FR-9, FR-1 |
| 1.3 | Implement atomic JSON writer: serialize → write to tmp file → `os.replace()` | `roadmap/progress.py` | 1.1 | FR-7, NFR-2 |
| 1.4 | Implement `record_step()` method — appends `StepProgress` to steps list and calls atomic write | `roadmap/progress.py` | 1.2, 1.3 | FR-1 |
| 1.5 | Add `summary()` method to gate constant instances in `roadmap/gates.py` (additive, no signature changes) | `roadmap/gates.py` | — | FR-10, NFR-4 |

**Milestone**: `progress.py` importable with zero I/O side effects (NFR-3). Unit tests pass for serialization and atomic write.

**Acceptance criteria**:
- `import superclaude.cli.roadmap.progress` creates no files
- `PipelineProgress.to_dict()` produces valid JSON with ISO 8601 timestamps
- Atomic write survives simulated interruption (file remains valid JSON after partial write)
- `summary()` returns dict with keys: `step`, `gate_tier`, `required_fields`, `semantic_checks`

---

### Phase 2 — CLI Integration & Dry-Run

**Goal**: Wire `--progress-file` into the CLI and implement dry-run gate summary table.

| # | Task | Files | Depends On | FR Coverage |
|---|------|-------|------------|-------------|
| 2.1 | Add `--progress-file` Click option to `roadmap run` (default: `{output_dir}/progress.json`) | `roadmap/commands.py` | — | FR-2 |
| 2.2 | Validate parent directory exists before pipeline starts; overwrite existing file on fresh run | `roadmap/commands.py` | 2.1 | FR-2 |
| 2.3 | Implement dry-run Markdown table output using gate `summary()` methods | `roadmap/commands.py` or `roadmap/executor.py` | 1.5 | FR-3 |
| 2.4 | Mark conditional steps (remediate, certify) with `(conditional)` in dry-run output | Same as 2.3 | 2.3 | FR-3 |

**Parallelism**: Tasks 2.1–2.2 (CLI option) can run concurrently with Phase 1 since they don't depend on `progress.py`.

**Milestone**: `superclaude roadmap run spec.md --dry-run` prints gate summary table. `--progress-file` accepted and validated.

**Acceptance criteria**:
- `--progress-file /nonexistent/dir/p.json` fails with clear error before pipeline starts
- Default path is `{output_dir}/progress.json`
- Dry-run table has columns: Step, Gate Tier, Required Fields, Semantic Checks
- Conditional steps show `(conditional)` marker

---

### Phase 3 — Executor Wiring & Callback Integration

**Goal**: Connect progress tracking to the live pipeline execution path.

| # | Task | Files | Depends On | FR Coverage |
|---|------|-------|------------|-------------|
| 3.1 | Add `on_step_complete` callback parameter to `execute_pipeline()` (`Optional[Callable]`, default `None`) | `pipeline/executor.py` | Phase 1 | FR-12 |
| 3.2 | Wire callback invocation — sequential even for parallel steps (invoke after each step joins) | `pipeline/executor.py` | 3.1 | FR-12 |
| 3.3 | Create progress callback in `roadmap/executor.py` that constructs `StepProgress` and calls `record_step()` | `roadmap/executor.py` | 3.1, Phase 1 | FR-1 |
| 3.4 | Ensure parallel steps (generate-A, generate-B) produce independent entries with per-step wall-clock timing | `roadmap/executor.py` | 3.3 | FR-1 |
| 3.5 | Set `PipelineProgress.completed = True` and write final state after last step | `roadmap/executor.py` | 3.3 | FR-8 |

**Milestone**: Full pipeline run produces valid `progress.json` with entries for all executed steps.

**Acceptance criteria**:
- `progress.json` is valid JSON after every step, including mid-pipeline interruption
- Parallel steps have independent `duration_ms` values reflecting actual wall time
- Write latency < 50ms per step (NFR-1)
- Existing callers of `execute_pipeline()` (sprint pipeline) unaffected (`None` default)

---

### Phase 4 — Extended Metadata & Resume

**Goal**: Enrich progress entries with step-specific metadata and implement resume behavior.

| # | Task | Files | Depends On | FR Coverage |
|---|------|-------|------------|-------------|
| 4.1 | Populate wiring step `metadata` with `unwired_count`, `orphan_count`, `blocking_count`, `rollout_mode`; gate verdict reflects `WIRING_GATE` semantic checks | `roadmap/executor.py` | Phase 3 | FR-6 |
| 4.2 | Implement deviation sub-entry recording: `metadata.deviation_iterations` list on spec-fidelity step entry (**contingent on GAP-002 resolution**) | `roadmap/executor.py` + `roadmap/progress.py` | Phase 3, GAP-002 | FR-4 |
| 4.3 | Implement remediation trigger fields: `metadata.trigger_reason`, `metadata.finding_count` (only when remediation executes) | `roadmap/executor.py` | Phase 3 | FR-5 |
| 4.4 | Add `metadata.validates_step_id` to certification entry referencing the remediation step_id | `roadmap/executor.py` | 4.3 | FR-5 |
| 4.5 | Implement `--resume` append behavior: load existing progress, skip completed steps, append new entries | `roadmap/executor.py` + `roadmap/progress.py` | Phase 3 | FR-11 |

**Milestone**: All step types produce correct metadata. Resume preserves prior entries.

**Acceptance criteria**:
- Wiring entry contains all four count fields plus `rollout_mode`
- Wiring gate verdict correctly reflects `WIRING_GATE` semantic check results
- Remediation entry only written when remediation actually executes
- Certification entry includes `validates_step_id` pointing to the remediation step
- Deviation iterations captured per-pass with `pass_number`, `verdict`, `duration_ms`
- `--resume` on a partially-completed run appends without overwriting prior entries

---

### Phase 5 — Testing & Documentation

**Goal**: Comprehensive test coverage and user documentation.

| # | Task | Depends On | Type |
|---|------|------------|------|
| 5.1 | Unit tests: data model serialization, atomic write crash safety, import side-effect check | Phase 1 | Unit |
| 5.2 | Integration tests: full pipeline produces valid progress.json with all step entries | Phase 3 | Integration |
| 5.3 | Integration tests: wiring metadata, deviation sub-entries, remediation triggers, certification reference | Phase 4 | Integration |
| 5.4 | Dry-run output validation tests (table format, conditional step markers) | Phase 2 | Integration |
| 5.5 | Write latency benchmark test (assert < 50ms per step) | Phase 3 | NFR |
| 5.6 | Resume append test: partially-completed run → resume → verify prior entries preserved | Phase 4 | Integration |

**Parallelism**: Tests 5.1 and 5.4 can start as soon as Phases 1 and 2 complete, respectively.

**Milestone**: All tests green. CLI help text updated.

---

## 3. Risk Assessment & Mitigation

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **GAP-002 unresolved** — deviation sub-entry schema undefined | High | Medium | Phase 4.2 is gated on resolution. Proposed default: `metadata.deviation_iterations: [{pass_number, verdict, duration_ms}]` nested on the spec-fidelity `StepProgress` entry. Seek sign-off before implementing. |
| **GAP-003 ambiguity** — "significant findings" threshold unclear | Medium | High | Default to HIGH severity only (consistent with spec-fidelity gate's existing threshold). Document the assumption explicitly. |
| **`--resume` vs overwrite contradiction** (FR-2 vs FR-11) | Medium | Certain | Resolve as: fresh run overwrites, `--resume` triggers append mode. Both behaviors explicitly tested. |
| **Concurrent write corruption** from parallel steps | High | Low | Architecture prevents this: executor serializes `on_step_complete` callbacks post-join. Integration test verifies JSON validity after parallel step group. |
| **Atomic write failure on NFS/network mounts** | Low | Low | `os.replace()` is atomic on POSIX local filesystems. Document that network mounts are unsupported. Fail loudly if `os.replace()` raises `OSError`. |
| **Backward-incompatible change to `execute_pipeline()` signature** | Medium | Low | Callback parameter uses `Optional[Callable]` with `None` default — existing callers (sprint pipeline) unaffected. |
| **Write latency exceeds 50ms** on large progress files | Low | Low | Progress files are small (< 100KB for typical pipelines). Benchmark test enforces constraint. Fallback: incremental JSON patching. |

---

## 4. Resource Requirements & Dependencies

### Files Modified

| File | Change Type | Phase |
|------|-------------|-------|
| `src/superclaude/cli/roadmap/progress.py` | **New** | 1 |
| `src/superclaude/cli/roadmap/gates.py` | Modified (`summary()` method) | 1 |
| `src/superclaude/cli/roadmap/commands.py` | Modified (`--progress-file` option) | 2 |
| `src/superclaude/cli/pipeline/executor.py` | Modified (`on_step_complete` callback) | 3 |
| `src/superclaude/cli/roadmap/executor.py` | Modified (create callback, pass to pipeline) | 3, 4 |

### External Dependencies
- **None**. Uses only Python stdlib: `json`, `os`, `tempfile`, `dataclasses`, `datetime`, `pathlib`.

### Prerequisite Resolutions (before implementation begins)

| ID | Question | Recommended Resolution | Blocks |
|----|----------|----------------------|--------|
| GAP-002 | Deviation sub-entry schema | Nest as `metadata.deviation_iterations: list[dict]` with `{pass_number: int, verdict: str, duration_ms: int}` | Phase 4.2 |
| GAP-003 | "Significant findings" threshold | HIGH severity only (matches spec-fidelity gate) | Phase 4.3 acceptance tests |
| `--resume` contradiction | Fresh run overwrites vs resume appends | Fresh run = overwrite; `--resume` = load + append | Phase 4.5 |
| Certification reference | How certification references remediation | `metadata.validates_step_id: str` on certification entry | Phase 4.4 |
| `metadata` key conventions | Which steps use which keys | Document well-known keys per step type in `progress.py` docstring; `metadata` remains free-form dict | Phase 4 |

### Module Dependency Direction (invariant)

```
commands.py → executor.py → progress.py → models.py / gates.py
```

No circular dependencies permitted.

---

## 5. Success Criteria & Validation

### Per-Requirement Validation

| Requirement | Validation Method | Pass Condition |
|-------------|-------------------|----------------|
| FR-EVAL-001.1 — Progress file writer | Integration test: run pipeline, parse `progress.json` | Valid JSON with correct `step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file` per step |
| FR-EVAL-001.2 — `--progress-file` option | CLI test: custom path + default path | File at specified path; default = `{output_dir}/progress.json`; invalid parent dir → error before pipeline |
| FR-EVAL-001.3 — Dry-run gate summary | CLI test: capture `--dry-run` stdout | Markdown table with 4 columns; all steps listed; conditional steps marked |
| FR-EVAL-001.4 — Deviation sub-reporting | Integration test with convergence loop | `metadata.deviation_iterations` list present; `pass_count` correct |
| FR-EVAL-001.5 — Remediation trigger reporting | Integration test with findings above threshold | `trigger_reason` + `finding_count` present; certification has `validates_step_id` |
| FR-EVAL-001.6 — Wiring verification | Integration test with wiring step | All four count fields + `rollout_mode` in metadata; verdict matches `WIRING_GATE` |
| NFR-EVAL-001.1 — Write latency | Benchmark test | < 50ms per step write |
| NFR-EVAL-001.2 — Crash safety | Kill-during-write test | File is valid JSON after interruption |
| NFR-EVAL-001.3 — No import side effects | Import test | Module import creates no files, no I/O |

### Definition of Done
1. All 6 explicit FRs + 6 implicit FRs + 5 NFRs pass automated tests
2. No modifications to `pipeline/gates.py` enforcement code
3. Module dependency direction maintained (no circular imports)
4. `--resume` and fresh-run behaviors both verified with integration tests
5. `make lint && make format` clean
6. `make verify-sync` passes after `make sync-dev`

---

## 6. Timeline Estimates

| Phase | Tasks | Effort | Parallelizable With |
|-------|-------|--------|---------------------|
| Phase 1 — Data Model & Core Writer | 5 tasks | Small | Phase 2 (tasks 2.1–2.2) |
| Phase 2 — CLI Integration & Dry-Run | 4 tasks | Small | Phase 1 (partially) |
| Phase 3 — Executor Wiring | 5 tasks | Medium | — (depends on Phase 1) |
| Phase 4 — Extended Metadata & Resume | 5 tasks | Medium | — (depends on Phase 3 + GAP resolutions) |
| Phase 5 — Testing & Docs | 6 tasks | Medium | Partially, as earlier phases complete |

### Critical Path

```
Phase 1 (data models) → Phase 3 (executor wiring) → Phase 4 (metadata + resume) → Phase 5 (integration tests)
```

### Parallelism Opportunities

```
          Phase 1: [data models + atomic writer + gate summary()]
         /                                                        \
Phase 2: [CLI option + dry-run]                    Phase 3: [executor callback wiring]
         \                                                        /
          Phase 5.1: [unit tests]         Phase 4: [metadata + resume + deviation]
          Phase 5.4: [dry-run tests]                              |
                                          Phase 5.2-5.3: [integration tests]
                                          Phase 5.5-5.6: [NFR + resume tests]
```

**Total scope**: 25 tasks across 5 phases. Single-sprint delivery given moderate complexity (0.45). The blocking dependency on GAP-002 is the primary schedule risk — if unresolved, Phase 4.2 slips but all other work proceeds.
