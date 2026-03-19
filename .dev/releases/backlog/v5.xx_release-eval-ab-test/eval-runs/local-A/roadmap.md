---
spec_source: "eval-spec.md"
complexity_score: 0.45
adversarial: true
base_variant: B
variant_scores: "A:74 B:81"
convergence_score: 0.78
rounds_completed: 2
---

## Executive Summary

This roadmap delivers a **crash-safe, additive progress reporting capability** for `superclaude roadmap run` with minimal architectural disruption and strong validation coverage. The feature adds a `progress.json` output file that records per-step execution metadata (status, timing, gate verdicts, step-specific diagnostics) using atomic writes via `os.replace()` for crash safety. The integration surface is narrow: one new module (`progress.py`), three modified modules (`executor.py`, `commands.py`, `gates.py`), and two cross-module read points (`convergence.py`, `wiring_gate.py`).

Complexity is MEDIUM (0.45) — the core callback-and-write pattern is straightforward, but deviation sub-reporting and wiring integration require careful data-model design. The implementation follows a requirements-first structure to eliminate foundational ambiguities before code changes begin, preventing the rework risk identified in adversarial review. Validation uses real CLI-driven evals with third-party verifiable artifacts, consistent with documented project standards.

**Key architectural decisions:**
- Callback-based, not observer-based — no threads, no file watchers
- Atomic JSON writes via `os.replace()` — crash-safe by construction
- Sequential callback invocation even for parallel steps — no concurrency in the writer
- `progress.py` depends on `models.py` and `gates.py`, never the reverse
- In-memory aggregation plus atomic replace, not incremental append

---

## Phased Implementation Plan

### Phase 1 — Requirements Closure and Architectural Alignment

**Goal:** Eliminate open ambiguities that would otherwise create rework across downstream phases. Front-loading OQ resolution prevents the highest-cost failure mode: building on unresolved foundations that affect data model shape and overwrite semantics.

#### Key Actions

1. Resolve **OQ-001**: Define the JSON schema for deviation sub-entries. Recommended: `metadata.convergence_iterations: list[{pass_number, structural_high_count, semantic_high_count, regression_detected}]` mirroring `ConvergenceResult` fields from `convergence.py`.
2. Resolve **OQ-004**: Reconcile overwrite vs. resume contradiction. Recommended: treat as two distinct modes — fresh run overwrites, `--resume` appends. Encode behavior in acceptance tests.
3. Resolve **OQ-002**: Define "significant findings" threshold for remediation triggers. Recommended: HIGH severity only, aligning with `_high_severity_count_zero` semantic check already in `gates.py`.
4. Confirm **OQ-005**: Metadata key conventions — recommend documenting but not enforcing schema constraints on the open dict.
5. Lock acceptance contract: map every FR/NFR/SC to its implementation phase and validation method.

#### Requirements Covered
All OQs; establishes traceability for FR-001 through FR-010, NFR-001 through NFR-005, SC-001 through SC-007.

#### Milestone
**M1:** Spec ambiguities closed and implementation contract frozen.

#### Estimated Effort
0.5–1 day

---

### Phase 2 — Data Models, Atomic Writer, and CLI Integration

**Goal:** Establish the `StepProgress` / `PipelineProgress` data models, the crash-safe file writer in `progress.py`, and wire `--progress-file` into the CLI and executor callback.

#### Key Actions

1. Create `src/superclaude/cli/roadmap/progress.py` containing:
   - `StepProgress` dataclass: `step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`, `metadata` (dict)
   - `PipelineProgress` container with `list[StepProgress]` and `to_json()` serialization
   - Atomic write function: serialize → temp file → `os.replace()` to target path
   - Progress update orchestration (callback sink)
2. Validate zero import-time side effects (NFR-003) — no module-level I/O
3. Add `--progress-file` as `click.Path` option to `run` command in `commands.py`, defaulting to `{output_dir}/progress.json`
4. Add path validation: parent directory must exist; fail fast before pipeline starts (FR-005)
5. Implement `on_step_complete` callback that builds a `StepProgress` entry from `StepResult` and appends to the running `PipelineProgress`
6. Thread the callback through `execute_roadmap()` → `execute_pipeline()` using the existing callback slot (NFR-004)
7. Handle overwrite-on-fresh-run semantics per resolved OQ-004

#### Requirements Covered
FR-001, FR-002, FR-003, FR-004, FR-005, FR-010, NFR-001, NFR-002, NFR-003, NFR-004, SC-001, SC-005

#### Milestone
**M2:** A full pipeline run produces a valid `progress.json` with one entry per step, all core fields populated. Module imports cleanly with no side effects.

#### Estimated Effort
2–3 days

---

### Phase 3 — Gate Summary, Dry-Run Table, and Special-Step Metadata

**Goal:** Add gate summary capability, dry-run visibility, and enrich progress entries for all special-case steps (convergence, remediation, certification, wiring verification).

**Note on parallelism:** The gate summary and dry-run work (tasks 1–4) can begin in parallel with Phase 2's executor integration, as it depends only on Phase 1's resolved schema and `gates.py` internals. Coordination cost is low since the gate summary interface is purely additive. The special-step metadata work (tasks 5–9) depends on Phase 2 completion.

#### Key Actions

1. Add `summary()` method to `GateCriteria` — returns tier, required fields count, semantic checks count (NFR-005: purely additive)
2. Verify backward compatibility: no existing gate constant interfaces change, no call-site modifications
3. Implement dry-run table renderer: iterate `ALL_GATES` (including `WIRING_GATE`), output Markdown table with columns: Step, Gate Tier, Required Fields, Semantic Checks
4. Mark conditional steps (remediate, certify) explicitly in the table output
5. Verify parallel step timing: `generate-A` and `generate-B` entries must have independent `duration_ms` values derived from their respective `StepResult.started_at` / `finished_at` (FR-003, SC-004)
6. Integrate convergence loop reporting via `convergence.py`: record each deviation-analysis iteration, include pass/iteration count, align nesting with resolved OQ-001 schema (FR-007)
7. Implement remediation metadata: populate `metadata.trigger_reason` and `metadata.finding_count`; emit entry only when remediation actually executes (FR-008)
8. Implement certification cross-reference: certification entry's `metadata` must reference the remediation step it validates (FR-008)
9. Implement wiring verification metadata: populate `metadata.unwired_count`, `metadata.orphan_count`, `metadata.blocking_count`, `metadata.rollout_mode` from `WiringReport` (FR-009); gate verdict reflects `WIRING_GATE` semantic check results

#### Requirements Covered
FR-003, FR-006, FR-007, FR-008, FR-009, NFR-005, SC-003, SC-004

#### Milestone
**M3:** `--dry-run` outputs a complete gate summary table. All special-step progress entries contain their required metadata fields. Parallel step timings are independently accurate.

#### Estimated Effort
2–3 days

---

### Phase 4 — Validation, Performance, and Release Readiness

**Goal:** Prove the implementation satisfies all success criteria using real CLI-driven evals, measure write latency, confirm crash safety, and ensure sync discipline for merge readiness.

#### Key Actions — Validation

1. **SC-001**: End-to-end CLI eval — full pipeline run → parse `progress.json` → assert all fields present per step. Artifact must be third-party inspectable.
2. **SC-002**: Crash-safety eval — kill pipeline mid-step → parse `progress.json` → must be valid JSON with no truncation.
3. **SC-003**: Dry-run eval — `--dry-run` output contains all gate entries including conditional steps.
4. **SC-004**: Parallel timing eval — verify `generate-A` and `generate-B` have distinct, accurate `duration_ms` values.
5. **SC-005**: Custom path eval — `--progress-file /tmp/custom.json` writes to specified path.
6. **SC-006**: Performance eval — measure per-step write overhead; assert < 50ms.
7. **SC-007**: Import eval — `import superclaude.cli.roadmap.progress` → confirm zero file I/O side effects.
8. Convergence sub-entry eval — multi-iteration convergence run produces correctly nested sub-entries.
9. Remediation/certification conditional behavior eval — entries appear only when executed, with correct metadata linkage.
10. Wiring verification metadata eval — counts and rollout mode correctly populated from `WiringReport`.
11. Run existing roadmap test suite as regression baseline.

#### Key Actions — Release Readiness

12. Verify all source-of-truth changes are in `src/superclaude/`.
13. Run `make sync-dev` and `make verify-sync`.
14. Confirm no unintended API or CLI regressions.
15. Validate sample run output artifacts for maintainability and operator clarity.

#### Requirements Covered
SC-001 through SC-007, NFR-001, all FRs (regression confirmation)

#### Milestone
**M4:** All 7 success criteria pass via real CLI eval runs. Performance budget met. Source and dev copies synced and verified. Feature ready for merge.

#### Estimated Effort
1.5–2.5 days

---

## Risk Assessment and Mitigation

| # | Risk | Severity | Phase | Mitigation | Contingency |
|---|------|----------|-------|------------|-------------|
| 1 | Progress writes add latency | Low | 4 | Atomic write < 50ms; pipeline steps take minutes. Performance eval enforces threshold. | Optimize serialization scope before changing architecture. |
| 2 | Parallel steps corrupt progress file | Medium | 2 | `on_step_complete` is invoked sequentially even for parallel steps. No concurrent writes. Explicit tests prove independent entries. | If callback order assumptions weaken, centralize dispatch rather than introducing file locks. |
| 3 | `summary()` breaks gate constants | High | 3 | Method is purely additive. Backward-compat verification included. No existing signatures change. | Move formatting logic outward; keep gates exposing raw data only. |
| 4 | Undefined deviation schema causes churn | Medium | 1 | Resolved before implementation begins (Phase 1). Compact, deterministic nested structure preferred. | If no clarification available, adopt minimal schema with explicit versioned test assertions. |
| 5 | Resume behavior contradiction causes artifact inconsistency | Medium | 1 | Resolved as Phase 1 decision. Separate semantics by mode (fresh: overwrite, resume: append). Encoded in acceptance tests. | Block release rather than ship ambiguous behavior. |

---

## Resource Requirements

### Technical Dependencies (by phase)

- **Phase 1**: Stakeholder availability for OQ resolution
- **Phase 2**: `models.py` (StepResult shape), `gates.py` (type references), `executor.py` (callback slot), `commands.py` (Click option registration)
- **Phase 3**: `gates.py` (GateCriteria, ALL_GATES), `convergence.py` (DeviationRegistry, ConvergenceResult), `wiring_gate.py` (WiringReport, WIRING_GATE), `executor.py` (remediation step metadata)
- **Phase 4**: All prior phases; `make sync-dev`, `make verify-sync`

### External Dependencies

- Python stdlib only: `json`, `os`, `tempfile`, `time`, `dataclasses`
- No new third-party packages required
- All tests and validation must run with `uv`
- Source-of-truth sync discipline: edit `src/superclaude/` first → `make sync-dev` → `make verify-sync`

### Staffing

- 1 primary implementer with code review from someone with roadmap pipeline context.

---

## Success Criteria Validation Matrix

| Criterion | Description | Validated In | Method |
|-----------|-------------|-------------|--------|
| SC-001 | Complete progress.json with all fields | Phase 4 | End-to-end CLI eval → JSON parse → field assertion |
| SC-002 | Crash-safe JSON (valid after interruption) | Phase 4 | Kill-and-parse eval |
| SC-003 | Dry-run gate table with all entries | Phase 4 | `--dry-run` output assertion against gate inventory |
| SC-004 | Independent parallel step timing | Phase 4 | Timing delta comparison for generate-A/B |
| SC-005 | Custom progress-file path works | Phase 4 | `--progress-file /path` eval |
| SC-006 | < 50ms per-step write overhead | Phase 4 | Benchmark with/without progress reporting |
| SC-007 | No import-time side effects | Phase 4 | Import + I/O monitoring |

---

## Timeline Summary

| Phase | Duration | Dependencies | Parallelism | Cumulative |
|-------|----------|-------------|-------------|------------|
| 1: Requirements Closure | 0.5–1 day | None | — | Days 0.5–1 |
| 2: Data Models & CLI Integration | 2–3 days | Phase 1 | Gate summary (Phase 3 tasks 1–4) can start in parallel | Days 1.5–4 |
| 3: Gate Summary & Special-Step Metadata | 2–3 days | Phase 1 (tasks 1–4), Phase 2 (tasks 5–9) | Tasks 1–4 parallel with Phase 2 | Days 3–6 |
| 4: Validation & Release Readiness | 1.5–2.5 days | All prior phases | — | Days 4.5–8.5 |

**Total estimated duration:** 5–8.5 working days

**Critical path:** Phase 1 → Phase 2 → Phase 3 (tasks 5–9) → Phase 4. Phase 3 tasks 1–4 (gate summary/dry-run) can run in parallel with Phase 2, saving ~0.5 days on the critical path.

**Schedule drivers:** Timeline is dominated by ambiguity resolution (Phase 1) and evidence gathering (Phase 4), not coding volume. If open questions are resolved immediately, the lower bound is realistic. If OQ resolution stalls, Phase 1 becomes the gating factor for the entire roadmap.
