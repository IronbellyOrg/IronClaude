---
title: "v3.7 Unified Refactoring Recommendation -- Dual-Path Awareness"
generated: 2026-04-03
source: 6 parallel analysis agents + 3 context documents
purpose: Comprehensive recommendation for refactoring v3.7 spec to serve both Path A and Path B
---

# v3.7 Unified Refactoring Recommendation

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Scope of Changes](#1-scope-of-changes)
3. [Unified Implementation Order](#2-unified-implementation-order)
4. [File Impact Matrix](#3-file-impact-matrix)
5. [Dependency Graph](#4-dependency-graph)
6. [Risk Register](#5-risk-register)
7. [Metrics](#6-metrics)
8. [Key Architectural Decisions](#7-key-architectural-decisions)
9. [Appendix: Source Chunk Cross-Reference](#appendix-source-chunk-cross-reference)

---

## Executive Summary

The v3.7 spec invests all prompt-level and data-model improvements into Path B (`build_prompt()` in `process.py`), which is the fallback path for malformed/legacy phase files. Path A (`_run_task_subprocess()` in `executor.py:1064-1068`), which handles every properly structured production sprint, receives none of these improvements. This recommendation merges analysis from 6 domain-specific chunks and 3 context documents to produce a unified refactoring plan. The core changes are: (1) add ~280 tokens of per-task prompt enrichment to Path A validated by adversarial debate, (2) fix 3 compounding TurnLedger bugs that zero out the reimbursement system, (3) adapt 4 of 10 TUI v2 features for Path A's per-task subprocess model, (4) reframe checkpoint enforcement to acknowledge that the post-phase gate is Path A's primary defense, and (5) leave the naming consolidation unchanged since it correctly targets Path B only. The total new work is ~120 LOC added across 8 new tasks (PA-01 through PA-08), with 3 additional data-model tasks (NEW-DM-04 through DM-06, after deduplicating DM-01/02/03 into PA-04/05/06). All existing spec tasks remain valid; none are removed. The refactoring adds a new "Wave 0" for Path A foundation work that unblocks subsequent waves.

---

## 1. Scope of Changes

### 1.1 Tasks to KEEP AS-IS

These tasks need no modification for dual-path awareness. They either operate at the phase/sprint level (above the Path A/B branching point), target only Path B correctly, or are pure mechanical renames.

| Task ID | Description | Justification |
|---------|-------------|---------------|
| T01.01 | Add checkpoint instructions to `build_prompt()` | Correctly targets Path B only. Path A workers are task-scoped subprocesses that cannot write end-of-phase checkpoints. (Chunk 1) |
| T01.02 | Add `_warn_missing_checkpoints()` helper | Operates at executor post-phase level, shared by both paths. (Chunk 1) |
| T02.01 | Create `checkpoints.py` with `extract_checkpoint_paths()` | Pure utility module, path-agnostic. (Chunk 1) |
| T02.02 | Add `PASS_MISSING_CHECKPOINT` to `PhaseStatus` | Phase-level enum, set by executor after completion. (Chunk 1) |
| T02.03 | Add `write_checkpoint_verification()` to `logging_.py` | Logging infrastructure, path-agnostic. (Chunk 1) |
| T03.01-T03.06 | Checkpoint manifest, recovery, CLI verify, tests | Entire Wave 3 operates on filesystem state post-execution. (Chunk 1) |
| T04.02-T04.03 | Checkpoint task validation and deliverable registry | Upstream validation and documentation, path-agnostic. (Chunk 1) |
| N1-N4, N6-N12 | Naming consolidation (all except N5) | Mechanical renames of files, directories, frontmatter, cross-references. No runtime path impact. (Chunk 3) |
| N5 | Update Sprint CLI prompt (`/sc:task-unified` to `/sc:task`) | Correctly targets `process.py:170` (Path B). Path A does not invoke any skill command. (Chunk 3) |
| F7 | Sprint name in TUI title | Reads `release_name` from `SprintConfig`, fully path-agnostic. (Chunk 2) |
| F9 | Tmux summary pane | Display-layer only, consumes F8 output files. (Chunk 2) |
| F10 | Release retrospective | Post-sprint aggregate, consumes F8 summary files. (Chunk 2) |
| 7.3 | `SprintResult` aggregate properties | Pure computation on `PhaseResult` fields. Correct as designed. (Chunk 4) |
| 7.4 | `SprintConfig.total_tasks`, `checkpoint_gate_mode` | Path-agnostic config fields. (Chunk 4) |
| 7.5 | `PhaseStatus.PASS_MISSING_CHECKPOINT` | Phase-level status, path-agnostic. (Chunk 4) |
| 7.7 | `SprintTUI.latest_summary_notification` | UI-level field, path-agnostic. (Chunk 4) |

### 1.2 Tasks to MODIFY

These tasks need path-awareness adjustments to serve both execution paths.

| Task ID | Current Spec | Recommended Change | Rationale |
|---------|-------------|-------------------|-----------|
| T02.04 | Wire `_verify_checkpoints()` as Layer 2 (secondary defense) | Reframe as PRIMARY defense for Path A. Add documentation note. Consider changing default `checkpoint_gate_mode` from `"shadow"` to `"soft"`. | Path A has no Layer 1 (prompt prevention). Layer 2 gate is the only enforcement until Wave 4 ships. (Chunk 1) |
| T02.05 | Unit tests for checkpoint gate | Extend to explicitly cover Path A execution flow (per-task `TaskResult` accumulation). | Ensures gate fires correctly after Path A's multi-subprocess phase. (Chunk 1) |
| T04.01 | Normalize `### Checkpoint:` to `### T<PP>.<NN> -- Checkpoint:` | Add Path A impact documentation: this transforms checkpoints from post-phase detection to inline execution (checkpoint becomes a regular task in Path A's loop). | Most architecturally significant checkpoint improvement for Path A. (Chunk 1) |
| F1 | Activity stream from NDJSON | Use synthetic entries for Path A v3.7 (task ID, status, duration per completed task). Defer per-task OutputMonitor to v3.8. | Path A never starts `OutputMonitor`; all tasks overwrite same output file. (Chunk 2) |
| F2 | Enhanced phase table (running-phase columns) | Wire `MonitorState.turns` and `output_size_display` from accumulated `TaskResult` data in Path A TUI hooks. | Running-phase data unavailable from `MonitorState` under Path A. Requires TurnLedger bug fix first. (Chunk 2) |
| F3 | Task-level progress bar | Set `MonitorState.total_tasks_in_phase = len(tasks)` and `completed_task_estimate = i+1` in Path A TUI hooks. 2-line change. | Path A has exact counts (superior to Path B's regex estimation). (Chunk 2) |
| F4 | Conditional error panel from NDJSON | Use task-level errors for Path A v3.7: `(task_id, "subprocess", exit_code)` from `TaskResult`. | Answers operator's primary question without per-task output file refactor. (Chunk 2) |
| F6 | Enhanced terminal panels | Aggregate `PhaseResult.turns/tokens/output_bytes` from `TaskResult` list after `execute_phase_tasks()`. | Path A builds `PhaseResult` without populating these fields currently. (Chunk 2) |
| F8 | Post-phase summary (Step 1: NDJSON extraction) | `PhaseSummarizer` must accept `list[TaskResult]` as alternative to NDJSON file path. Path A provides structured per-task data (superior for task status, errors). | Path A's output file contains only the last task's NDJSON. (Chunk 2) |
| 7.1 | 8 new `MonitorState` fields | Path A must populate these in TUI update hooks (`executor.py:978-984, 1042-1048`), OR document them as Path B only. `completed_task_estimate` should be exact count on Path A. | Fields are dead code for production sprints without population. (Chunk 4) |
| 7.2 | `PhaseResult.turns/tokens_in/tokens_out` | Document that Path A populates via `sum(TaskResult.field)` aggregation, not from `MonitorState`. Add `tokens_in`/`tokens_out` fields to `TaskResult`. | Different data flow: `TaskResult` -> `PhaseResult` (not `MonitorState` -> `PhaseResult`). (Chunk 4) |
| Sec 5 | Cross-domain dependency analysis (3 domains) | Add Path A Enrichment as 4th domain. Add Sections 5.6 (Path A <-> Checkpoint) and 5.7 (Path A <-> TurnLedger). | `executor.py` and `models.py` now modified by 3+ domains. (Chunk 5) |
| Sec 6.2 | Implementation order (7 steps) | Insert "Path A Prompt Enrichment" at position 2 and "TurnLedger Bug Fixes" at position 3 (concurrent). Total becomes 9 steps. | Path A enrichment must precede Checkpoint W1 so both paths can receive checkpoint instructions in the same wave. (Chunk 5) |
| Sec 6.4 | Post-phase hook insertion (single location) | Hook insertion must happen in BOTH Path A block (lines 1222-1233) AND Path B block (lines 1432-1454). Pass `task_results` to `_verify_checkpoints()` and `summary_worker.submit()`. | Spec only describes one insertion point; Path A has a separate post-phase block. (Chunk 5) |
| Sec 14 | Open questions | Resolve CE-Q3, CE-Q4, CE-Q6, TUI-Q8. Reframe TUI-Q1, TUI-Q2, CE-Q2. Add PA-Q1 (`build_task_context` wiring). | Path A analysis directly answers 4 questions and reframes 3 others. (Chunk 5) |

### 1.3 NEW Tasks (Path A Enrichment)

These tasks are entirely new -- not in the original v3.7 spec. They address the 7 validated deficiencies in Path A.

| Task ID | Description | Priority | LOC | Risk | Source |
|---------|-------------|----------|-----|------|--------|
| PA-01 | Extract and inject per-task markdown block via `_extract_task_block()` | P0 | ~30 added | Low | Chunk 6, Debate Ruling 1 |
| PA-02 | Add scope boundary to per-task prompt (`Execute ONLY task X. STOP when complete.`) | P0 | ~5 | Negligible | Chunk 6, Debate Ruling 2 |
| PA-03 | Add sprint context header to per-task prompt (shared `build_sprint_context_header()`) | P0 | ~25 added, ~15 modified | Low | Chunk 6, Debate Ruling 4 |
| PA-04 | Fix `turns_consumed` to call `count_turns_from_output()` instead of returning 0 | P0 | ~3 | Low | Chunk 6, Chunk 4 (Bug 1) |
| PA-05 | Wire `TaskResult.output_path = str(config.output_file(phase))` | P0 | ~1 | Negligible | Chunk 6, Chunk 4 (Bug 2) |
| PA-06 | Change `gate_rollout_mode` default from `"off"` to `"shadow"` | P1 | ~1 | Low-Medium | Chunk 6, Chunk 4 (Bug 3) |
| PA-07 | Evaluate and wire `build_task_context()` behind `inject_task_context` config flag (default off) | P2 | ~20 | Medium | Chunk 6, Deficiency 4 |
| PA-08 | Post-task deliverable existence check (observability only, no enforcement) | P2 | ~40 | Low | Chunk 6, Deficiency 3 |
| NEW-DM-04 | Implement `extract_token_usage()` in `monitor.py` | P1 | ~25 | Low | Chunk 4 |
| NEW-DM-05 | Add `tokens_in`/`tokens_out` fields to `TaskResult` and wire extraction | P1 | ~5 | Low | Chunk 4 |
| NEW-DM-06 | Add Path A aggregation logic: `TaskResult` list -> `PhaseResult` fields | P1 | ~10 | Low | Chunk 4 |

**Note on deduplication**: Chunks 4 and 6 both propose the TurnLedger bug fixes. The canonical task IDs are **PA-04** (turns_consumed), **PA-05** (output_path), and **PA-06** (gate_rollout_mode). Chunk 4's NEW-DM-01, DM-02, and DM-03 are merged into these. The remaining Chunk 4 tasks (NEW-DM-04 through DM-06) are retained as they cover token extraction and aggregation logic not in Chunk 6.

### 1.4 Features to DEPRIORITIZE

| Feature | Current Priority | Recommended Action | Rationale |
|---------|-----------------|-------------------|-----------|
| F5 (LLM Context Lines) | Medium (TUI v2) | Deprioritize for Path A. Implement for Path B only in v3.7. | Per-task prompt is 3 lines; preview has minimal value. Becomes useful only after PA-01/PA-03 enrichment + potential `/sc:task` invocation. (Chunk 2) |
| Per-task `OutputMonitor` (real-time tool streaming) | Not in spec | Defer to v3.8. Use synthetic entries for v3.7. | Requires per-task output files (`phase-N-task-TPPTT-output.txt`) which is a larger refactor. (Chunk 2) |
| Evidence verification enforcement | Not in spec | Defer enforcement to v3.8. PA-08 adds observability-only check in v3.7. | Depends on Path A enrichment + TurnLedger activation for response mechanism. (Chunk 5, Chunk 6) |
| `build_task_context()` activation | Not in spec | Wire behind config flag (default off) in v3.7, evaluate for default-on in v3.8. | Adds inter-task prompt coupling; needs observation period. (Chunk 5, Chunk 6) |
| Task dependency enforcement | Not in spec | Defer to v3.8. | Parsed but not enforced; low severity (Deficiency 5). (Context 1) |
| Task-level resume | Not in spec | Defer to v3.8+. | Requires per-task JSONL events; larger infrastructure change (Deficiency 6). (Context 1) |

---

## 2. Unified Implementation Order

The original spec defines 7 implementation steps. The refactored order inserts Path A foundation work as Phases 0-1 and adjusts subsequent phases to account for new dependencies.

### Phase 0: Foundation (NEW -- Path A Bug Fixes + Block Extraction)

**Rationale**: These tasks have zero dependencies on existing spec work and unblock everything downstream.

| Task | Description | LOC | Can Parallelize With |
|------|-------------|-----|---------------------|
| PA-04 | Fix `turns_consumed` return value (`executor.py:1091`) | ~3 | PA-05, PA-01 |
| PA-05 | Wire `TaskResult.output_path` (`executor.py:1017`) | ~1 | PA-04, PA-01 |
| PA-01 | Implement `_extract_task_block()` in `config.py` and wire into prompt | ~30 | PA-04, PA-05 |

All three tasks are independent and can execute in parallel. They modify different line ranges in `executor.py` (PA-04: line 1091, PA-05: lines 1017-1025, PA-01: lines 1064-1068) and `config.py` (PA-01 only).

### Phase 1: Path A Prompt Enrichment + Naming Consolidation

**Rationale**: Naming must complete before any prompt that might reference `/sc:task`. Path A enrichment must complete before Checkpoint W1 so both paths can receive checkpoint instructions simultaneously.

| Task | Description | LOC | Dependencies |
|------|-------------|-----|-------------|
| N1-N12 | Naming consolidation (mechanical rename, all 12 tasks) | ~50 | None (can start with Phase 0) |
| PA-02 | Add scope boundary to per-task prompt | ~5 | PA-01 |
| PA-03 | Add sprint context header (shared `build_sprint_context_header()`) | ~25 | PA-01 |
| PA-06 | Change `gate_rollout_mode` default to `"shadow"` | ~1 | PA-04 + PA-05 |
| NEW-DM-04 | Implement `extract_token_usage()` in `monitor.py` | ~25 | None |
| NEW-DM-05 | Add `tokens_in`/`tokens_out` to `TaskResult` | ~5 | NEW-DM-04 |

### Phase 2: Checkpoint Wave 1 (Prompt Prevention) + Data Model Wiring

**Rationale**: With Path A enrichment in place, checkpoint instructions can now target both `build_prompt()` (Path B) and the enriched per-task prompt (Path A) using a shared constant from `checkpoints.py`.

| Task | Description | Dependencies |
|------|-------------|-------------|
| T01.01 | Add checkpoint instructions to `build_prompt()` (Path B) | N5 (naming) |
| T01.01-ext | Add checkpoint instructions to enriched Path A prompt (shared constant) | PA-01, PA-02, PA-03 |
| T01.02 | Add `_warn_missing_checkpoints()` helper | None |
| NEW-DM-06 | Wire Path A aggregation: `TaskResult` list -> `PhaseResult` fields | PA-04, PA-05, NEW-DM-05 |

### Phase 3: TUI v2 Core (F1-F7) + Checkpoint Wave 2

**Rationale**: TUI features now benefit from active gate results (Phase 0-1 enables anti-instinct gate). Implement TUI features in priority order: F7 (trivial) > F3 (2 lines) > F2+F6 (moderate, TurnLedger-dependent) > F4 > F1.

| Task | Description | Path A Adaptation |
|------|-------------|-------------------|
| F7 | Sprint name in title | None needed |
| F3 | Task-level progress bar | 2-line change: `total_tasks_in_phase = len(tasks)`, `completed_task_estimate = i+1` |
| F2 | Enhanced phase table | Wire `MonitorState.turns` from accumulated `TaskResult` data |
| F6 | Enhanced terminal panels | Aggregate from `TaskResult` list post-phase |
| F4 | Conditional error panel | Task-level errors from `TaskResult.status` + `exit_code` |
| F1 | Activity stream | Synthetic entries per completed task |
| T02.01-T02.05 | Checkpoint Wave 2 (detection gate) | Reframe as PRIMARY defense for Path A |

### Phase 4: TUI v2 Summary (F8-F10) + Checkpoint Wave 3

| Task | Description | Path A Adaptation |
|------|-------------|-------------------|
| F8 | Post-phase summary | `PhaseSummarizer` accepts `list[TaskResult]` OR NDJSON path |
| F9 | Tmux summary pane | None (depends on F8) |
| F10 | Release retrospective | None (depends on F8) |
| T03.01-T03.06 | Checkpoint Wave 3 (manifest, recovery, CLI) | None (filesystem-level) |

### Phase 5: Checkpoint Wave 4 (Normalization) + Lower-Priority Path A

| Task | Description | Notes |
|------|-------------|-------|
| T04.01-T04.03 | Checkpoint task normalization | Document Path A benefit: checkpoints become regular tasks |
| PA-07 | Wire `build_task_context()` behind config flag | Medium risk, evaluate after shadow-mode data |
| PA-08 | Post-task deliverable existence check | Observability only |
| F5 | LLM context lines (Path B only in v3.7) | Deprioritized for Path A |

---

## 3. File Impact Matrix

| File | Original Spec Changes | New Path A Changes | Total Modifications | Conflict Risk |
|------|----------------------|-------------------|--------------------|----|
| `executor.py` | Checkpoint W1-W3 (warning, gate, manifest at post-phase hooks); TUI (SummaryWorker, PhaseResult population) | PA-01 (prompt rewrite, lines 1064-1068); PA-04 (turns fix, line 1091); PA-05 (output_path, lines 1017-1025); PA-08 (post-task hook, lines 1027-1036); DM-06 (aggregation, lines 1217-1219) | 5+ distinct modifications across 3 domains | **HIGH** -- 3 domains modify this file. Line ranges do not overlap but structural understanding requires all-domain awareness. |
| `models.py` | Checkpoint (W2-W3: `PhaseStatus` enum, `CheckpointEntry`); TUI (`MonitorState` 8 fields, `PhaseResult` 3 fields, `SprintResult` 5 properties, `SprintConfig` 2 fields) | PA-05 (`TaskResult.output_path` default fix); PA-06 (`gate_rollout_mode` default); DM-05 (`TaskResult.tokens_in/out`); PA-07 (`inject_task_context` flag); PA-08 (`missing_deliverables` field) | Additive changes to 4+ dataclasses | **LOW** -- all additive, different dataclasses. |
| `process.py` | N5 (rename at line 170); Checkpoint W1 (T01.01, `build_prompt()`); PA-03 (refactor to shared `build_sprint_context_header()`) | PA-03 extracts shared helper from lines 129-167 | 3 modifications | **LOW** -- PA-03 refactors existing code for DRY; Checkpoint W1 adds to the same function. Order: N5 first, then PA-03, then T01.01. |
| `config.py` | TUI (pre-scan integration) | PA-01 (`_extract_task_block()` as public utility alongside `parse_tasklist`) | 1 new function | **LOW** -- additive, reads from `parse_tasklist` block boundaries. |
| `monitor.py` | TUI v2 (`OutputMonitor` enhancements) | DM-04 (`extract_token_usage()` new function) | 1 new function | **LOW** -- additive alongside existing `count_turns_from_output()`. |
| `checkpoints.py` (new) | Checkpoint W2-W3 (all checkpoint utilities) | Shared checkpoint instruction constant for PA/PB prompt parity | 1 shared constant | **LOW** -- additive. |
| `tui.py` | TUI v2 (F1-F10 rendering) | No direct changes; Path A adaptations wire data into existing TUI fields | 0 direct | **NONE** -- all Path A adaptations are at the data layer, not the rendering layer. |
| `logging_.py` | Checkpoint (T02.03, structured logging) | No Path A changes | 0 | **NONE** |
| Skill/command files (21 files) | N1-N12 (mechanical renames) | No Path A changes | Mechanical renames only | **NONE** |

---

## 4. Dependency Graph

```
                    ┌──────────────┐
                    │   Phase 0    │
                    │  (parallel)  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              v            v            v
         ┌────────┐  ┌────────┐  ┌────────┐
         │ PA-04  │  │ PA-05  │  │ PA-01  │
         │ turns  │  │ output │  │ block  │
         │  fix   │  │  path  │  │ extract│
         └───┬────┘  └───┬────┘  └───┬────┘
             │            │           │
             └─────┬──────┘     ┌─────┴─────┐
                   v            v           v
              ┌────────┐  ┌────────┐  ┌────────┐
              │ PA-06  │  │ PA-02  │  │ PA-03  │
              │ shadow │  │ scope  │  │ sprint │
              │default │  │boundary│  │context │
              └───┬────┘  └───┬────┘  └───┬────┘
                  │           │           │
                  └─────┬─────┘           │
                        │    ┌────────────┘
                        v    v
                   ┌──────────────┐
                   │  Checkpoint  │
                   │    Wave 1    │
                   │ (both paths) │
                   └──────┬───────┘
                          │
                   ┌──────┴───────┐
                   v              v
              ┌────────┐    ┌─────────┐
              │TUI Core│    │Checkpoint│
              │ F1-F7  │    │  Wave 2  │
              └───┬────┘    └────┬─────┘
                  │              │
                  └──────┬───────┘
                         v
                   ┌──────────┐
                   │TUI Summary│
                   │  F8-F10   │
                   └─────┬─────┘
                         │
                   ┌─────┴──────┐
                   v            v
              ┌────────┐  ┌────────┐
              │Checkpoint│ │ PA-07  │
              │ Wave 3   │ │ PA-08  │
              └─────┬────┘ └────────┘
                    v
              ┌──────────┐
              │Checkpoint│
              │  Wave 4  │
              └──────────┘
```

**Parallelizable work streams**:
- Naming consolidation (N1-N12) can run concurrently with all Phase 0 tasks
- DM-04/DM-05 (token extraction) can run concurrently with PA-01 through PA-03
- Checkpoint Wave 2 and TUI Core can overlap once Phase 2 completes

**Critical path**: PA-01 -> PA-02/PA-03 -> Checkpoint W1 (both paths) -> TUI Core -> F8 -> F9/F10

**TurnLedger chain**: PA-04 + PA-05 -> PA-06 -> DM-06 (aggregation) -> F2/F6 (TUI features that display turn/token data)

---

## 5. Risk Register

| Risk | Severity | Probability | Mitigation | Source |
|------|----------|------------|------------|--------|
| **Per-task output file overwrite** -- all Path A tasks write to `phase-N-output.txt`, losing previous tasks' NDJSON | High | Certain (existing behavior) | Accept for v3.7. Use synthetic TUI entries and `TaskResult`-based extraction. Plan per-task output files for v3.8. | Chunk 2, Chunk 4 |
| **TurnLedger activation side effects** -- fixing 3 bugs activates a dormant economic feedback loop; reimbursement credits become non-zero, anti-instinct gate starts evaluating | Medium | High (once PA-04/05/06 land) | Default `gate_rollout_mode` to `"shadow"` (metrics only, no enforcement). Observe before promoting to `"soft"`. | Chunk 5, Chunk 6 |
| **Prompt construction parity drift** -- Path A and Path B each have their own prompt construction; future enhancements may update one and forget the other | High | Medium (maintenance) | Extract shared prompt components into `build_sprint_context_header()`, `build_checkpoint_instructions()`. Both paths call shared builders. | Chunk 5 |
| **executor.py merge conflicts** -- 3 domains modify the same file (Path A enrichment, Checkpoint, TUI) | Medium | Medium | Line ranges do not overlap: Path A = 1017-1092, Checkpoint/TUI = 1200-1460. Implement in phase order; one developer per domain wave. | Chunk 5 |
| **Checkpoint enforcement gap** -- between Wave 2 (gate in `"shadow"` mode) and Wave 4 (checkpoint-as-task), Path A has only observability-level checkpoint defense | Medium | High (interim period) | Change `checkpoint_gate_mode` default to `"soft"` for Wave 2 ship (log + warning). Promote to `"full"` with Wave 3. | Chunk 1 |
| **`build_task_context()` over-injection** -- if enabled, adds 200-500 tokens per task of inter-task coupling | Low | Low (default off) | Config flag `inject_task_context` defaults to `False`. Enable only after observation. | Chunk 5, Chunk 6 |
| **Anti-instinct gate false positives** -- once gate evaluates real output (PA-05 wires output_path), it may flag legitimate outputs as non-compliant | Medium | Medium | Shadow mode logs but does not block. Review shadow logs before promoting to soft/full. | Chunk 4, Chunk 5 |

---

## 6. Metrics

### LOC Estimates

| Category | LOC Added | LOC Modified | LOC Removed |
|----------|-----------|-------------|-------------|
| Original spec (Checkpoint W1-W4) | ~350 | ~50 | ~10 |
| Original spec (TUI v2 F1-F10) | ~800 | ~80 | ~20 |
| Original spec (Naming N1-N12) | ~10 | ~30 | ~30 |
| Original spec (Data Model Sec 7) | ~120 | ~40 | 0 |
| **Original spec subtotal** | **~1,280** | **~200** | **~60** |
| New: Path A prompt enrichment (PA-01 to PA-03) | ~60 | ~20 | ~15 |
| New: TurnLedger bug fixes (PA-04 to PA-06) | ~5 | ~5 | ~2 |
| New: Dead code activation (PA-07) | ~20 | ~5 | 0 |
| New: Evidence verification (PA-08) | ~40 | ~3 | 0 |
| New: Token extraction + aggregation (DM-04 to DM-06) | ~40 | ~5 | 0 |
| **New tasks subtotal** | **~165** | **~38** | **~17** |
| **Combined total** | **~1,445** | **~238** | **~77** |

### Task Counts

| Category | Count |
|----------|-------|
| Tasks unchanged (KEEP AS-IS) | 25 (T01.02, T02.01-T02.03, T03.01-T03.06, T04.02-T04.03, N1-N12, F7, F9, F10) |
| Tasks modified (path-awareness adjustments) | 15 (T02.04-T02.05, T04.01, F1-F4, F6, F8, 7.1, 7.2, Sec 5, 6.2, 6.4, 14) |
| New tasks added | 11 (PA-01 through PA-08, NEW-DM-04 through DM-06) |
| Tasks/features deprioritized | 6 (F5 for Path A, per-task OutputMonitor, evidence enforcement, build_task_context default-on, task dependency enforcement, task-level resume) |

### Token Budget Impact

| Component | Per-Task Token Cost |
|-----------|-------------------|
| Task block extraction (PA-01) | ~150 avg (variable) |
| Scope boundary (PA-02) | ~50 |
| Sprint context header (PA-03) | ~80 |
| **Total prompt enrichment** | **~280 per task** |
| Prior task context (PA-07, if enabled) | ~100-300 (compressed) |

Against per-task budgets of 100+ turns (each consuming thousands of tokens), the ~280 token enrichment is ~0.02% of typical task budget.

---

## 7. Key Architectural Decisions

### Decision 1: Path A Should NOT Invoke `/sc:task`

**Ruling**: Do not wire `/sc:task` (or `/sc:task-unified`) into Path A's per-task prompt.
**Rationale**: The skill protocol was designed for Path B's single-subprocess-executes-all-tasks model. Its multi-task flow-control semantics (ordered execution, halt-on-STRICT, result file contracts) are either redundant or counterproductive in Path A's subprocess-per-task model. The adversarial debates rejected both result file contracts (Ruling 3, AGAINST 4-3) and stop-on-STRICT-fail (Ruling 5, AGAINST 0.795 vs FOR 0.64). The correct approach is targeted prompt enrichment (~280 tokens) not full protocol loading (~2,000-4,000 tokens per subprocess).
**Source**: Chunk 3, Context 2 (Rulings 3, 5)

### Decision 2: TurnLedger Activation Uses Shadow Mode First

**Ruling**: Fix all 3 bugs (PA-04, PA-05, PA-06) but default `gate_rollout_mode` to `"shadow"` (evaluate + record, no enforcement).
**Rationale**: The economic feedback loop has been dormant since v3.1. Shadow mode allows observation of gate behavior on real workloads before enforcement. The 50+ existing tests validate correct math but on zero inputs. Promoting to `"soft"` after one release cycle of shadow data provides a safe activation ramp.
**Source**: Chunk 4, Chunk 5, Chunk 6

### Decision 3: Checkpoint Gate Is PRIMARY Defense for Path A

**Ruling**: Reframe the "Three-Layer Defense" model: Layer 1 (prompt prevention) applies to Path B only; Layer 2 (detection gate) is the primary defense for Path A.
**Rationale**: Path A workers are isolated per-task subprocesses that cannot write end-of-phase checkpoints. The prompt-level prevention (T01.01) is architecturally irrelevant to Path A. Until Wave 4 ships (checkpoint-as-task normalization), the post-phase gate is the only enforcement mechanism for production sprints.
**Source**: Chunk 1

### Decision 4: Extract Shared Prompt Builders to Prevent Drift

**Ruling**: Create shared functions (`build_sprint_context_header()`, `build_checkpoint_instructions()`) that both Path A and Path B call.
**Rationale**: Two independent prompt construction sites (`build_prompt()` in `process.py` and `_run_task_subprocess()` in `executor.py`) create a maintenance trap. Future improvements must be applied to both. Shared builders enforce parity at the function level.
**Source**: Chunk 5 (Concern 1), Chunk 6 (PA-03)

### Decision 5: Per-Task Output Files Deferred to v3.8

**Ruling**: Accept that all Path A tasks overwrite `phase-N-output.txt` in v3.7. Use synthetic TUI entries and `TaskResult`-based extraction instead of per-task NDJSON parsing.
**Rationale**: Changing to per-task output files (`phase-N-task-TPPTT-output.txt`) unlocks full TUI v2 fidelity but is a larger refactor that touches subprocess management, file naming, and monitor infrastructure. The v3.7 approach (synthetic entries, task-level error reporting, `TaskResult` aggregation) provides 80% of the value at 20% of the cost.
**Source**: Chunk 2, Chunk 4

### Decision 6: `build_task_context()` Wired Behind Config Flag

**Ruling**: Wire the fully-implemented-but-never-called function behind `inject_task_context: bool = False`. Do not enable by default in v3.7.
**Rationale**: Inter-task context adds prompt coupling where none exists today. The function was designed for Path B's single-subprocess model where all prior context is in the same conversation. For Path A, each task starts with a fresh context window -- explicit injection is more valuable but also more expensive. Observation period required.
**Source**: Chunk 5 (Concern 4), Chunk 6 (PA-07)

### Decision 7: Checkpoint-as-Task (Wave 4) Is the Long-Term Path A Solution

**Ruling**: Wave 4's normalization of `### Checkpoint:` headings to `### T<PP>.<NN> -- Checkpoint:` task entries is the most architecturally significant checkpoint improvement for Path A.
**Rationale**: When checkpoints become regular tasks, Path A's `_parse_phase_tasks()` includes them in the per-task loop. Each checkpoint dispatches to a subprocess that writes the checkpoint file as its primary deliverable. This converts checkpoint enforcement from a post-phase detection problem to an inline execution guarantee. Combined with Wave 2's gate (belt-and-suspenders verification), this provides two independent enforcement layers.
**Source**: Chunk 1 (T04.01 analysis)

---

## Appendix: Source Chunk Cross-Reference

| Recommendation | Chunk 1 | Chunk 2 | Chunk 3 | Chunk 4 | Chunk 5 | Chunk 6 | Context 1 | Context 2 | Context 3 |
|---------------|---------|---------|---------|---------|---------|---------|-----------|-----------|-----------|
| Checkpoint gate = primary for Path A | X | | | | X | | | | X |
| Extend T02.05 tests for Path A | X | | | | | | | | |
| T04.01 Path A impact documentation | X | | | | | | | | |
| F1 synthetic entries | | X | | | | | | | |
| F2/F6 TaskResult aggregation | | X | | X | | | | | |
| F3 exact task count | | X | | | | | | | |
| F4 task-level errors | | X | | | | | | | |
| F5 deprioritized for Path A | | X | | | | | | | |
| F8 dual-input PhaseSummarizer | | X | | | | | | | |
| Naming: no Path A changes | | | X | | | | | | |
| Do NOT wire `/sc:task` into Path A | | | X | | | | | X | X |
| TurnLedger bug fixes (PA-04/05/06) | | | | X | X | X | X | | X |
| `TaskResult.tokens_in/out` new fields | | | | X | | X | | | |
| Path A aggregation to PhaseResult | | | | X | | X | | | |
| Path A as 4th cross-domain dependency | | | | | X | | | | |
| Revised implementation order | | | | | X | X | | | |
| Post-phase hooks in both code blocks | | | | | X | | | | |
| Prompt construction parity (shared builders) | | | | | X | X | | | X |
| Per-task block extraction (PA-01) | | | | | | X | X | X | |
| Scope boundary (PA-02) | | | | | | X | X | X | |
| Sprint context header (PA-03) | | | | | | X | X | X | |
| `build_task_context()` conditional wiring | | | | | X | X | X | | |
| Post-task deliverable check (PA-08) | | | | | X | X | X | | |
| Per-task output files deferred to v3.8 | | X | | X | | | | | |
| Shadow mode activation ramp | | | | X | X | X | | | |

---

*This document synthesizes 6 parallel analysis chunks and 3 context documents into a unified refactoring recommendation. It is intended to be used directly for revising the v3.7-UNIFIED-RELEASE-SPEC. Each recommendation traces to at least one source chunk and is grounded in code evidence at specific file paths and line numbers.*
