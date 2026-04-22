---
title: "Chunk 5: Cross-Cutting Concerns -- Path A/B Refactoring Analysis"
chunk: cross-cutting
spec_sections: "5, 6, 14"
generated: 2026-04-03
---

# Cross-Cutting Concerns -- Refactoring Analysis

## Executive Summary

The v3.7 spec's cross-domain dependency analysis (Section 5), implementation ordering (Section 6), and open questions (Section 14) all assume a single execution path -- Path B's `build_prompt()` in `process.py`. When Path A (`_run_task_subprocess()` in `executor.py:1064-1068`) is brought into scope, three structural changes are needed:

1. **Section 5 dependency analysis gains a fourth domain.** The existing three-way analysis (Checkpoint x TUI x Naming) omits executor.py's per-task loop entirely. Path A enrichment touches `executor.py` (same file as Checkpoint and TUI) and `models.py` (same file as Checkpoint and TUI data model changes), creating new file-level merge conflicts.

2. **Section 6 implementation order requires one insertion.** Path A prompt enrichment should slot between Naming Consolidation and Checkpoint W1, because Checkpoint W1 adds prompt instructions to `build_prompt()` -- the equivalent Path A enrichment must exist first so that checkpoint prompt parity can be verified in the same wave.

3. **Section 14 open questions: 4 are resolved, 3 are reframed, 1 is new.** The Path A analysis directly answers TUI-Q8 (per-task prompt preview), CE-Q3 (context pressure), CE-Q4 (mid-phase checkpoint gate timing), and CE-Q6 (`_check_checkpoint_pass` consolidation). Three additional questions are reframed by the dual-path perspective.

Net spec changes: 12 additions/modifications across Sections 5, 6, and 14.


## Revised Cross-Domain Dependencies

### New Domain: Path A Enrichment

The existing Section 5 analyzes dependencies among three domains: Checkpoint Enforcement, Sprint TUI v2, and Naming Consolidation. Path A Enrichment is a fourth domain that shares files with the first two.

**New shared-file conflicts introduced by Path A:**

| File | Path A Changes | Existing Domain Changes | Conflict Risk |
|------|---------------|------------------------|---------------|
| `executor.py` | `_run_task_subprocess()` prompt rewrite (lines 1064-1068); `_extract_task_block()` new function; `TaskResult` construction fix (`output_path` wiring, line 1017-1025) | Checkpoint (Waves 1-3: warning, gate, manifest); TUI (SummaryWorker, PhaseResult population) | **HIGH** -- three domains now modify `executor.py`. Path A changes are localized to lines 1017-1092 (per-task loop internals), while Checkpoint and TUI changes operate on the post-phase flow (lines 1200-1460). Merge risk is moderate because the line ranges do not overlap, but structural understanding requires awareness of all three. |
| `models.py` | `TaskResult.output_path` default fix; potential `enforcement_tier` field on `TaskEntry` | Checkpoint (Wave 2-3: enum, `CheckpointEntry`); TUI (MonitorState, PhaseResult, SprintResult fields) | **LOW** -- additive changes to different dataclasses. |
| `config.py` | `_extract_task_block()` may use `parse_tasklist` block boundaries | TUI (pre-scan integration, see TUI-Q10) | **LOW** -- both read from `parse_tasklist` but do not modify it. |

### Revised Dependency: Section 5.1 (Checkpoint <-> TUI)

No change. The functional dependency on `PASS_MISSING_CHECKPOINT` display remains. Path A does not alter this interaction because `PASS_MISSING_CHECKPOINT` is a phase-level status set after the per-task loop completes.

### Revised Dependency: Section 5.2 (Naming <-> Checkpoint)

**Minor revision.** The spec notes that Checkpoint W1 and Naming both modify `build_prompt()` in `process.py:170`. Path A enrichment does NOT touch `process.py` -- it modifies `executor.py:1064-1068` instead. However, if Path A prompt enrichment includes a `/sc:task` invocation (the post-naming canonical name), then the naming consolidation must complete before Path A enrichment to avoid embedding a deprecated command name.

### New Dependency: Section 5.6 (Path A Enrichment <-> Checkpoint Enforcement)

Checkpoint W1 adds checkpoint instructions to `build_prompt()` (Path B). The equivalent for Path A would be adding checkpoint instructions to the enriched per-task prompt in `_run_task_subprocess()`. These two changes must use identical checkpoint instruction text. **Recommendation:** Extract checkpoint instruction text into a shared constant or helper function in `checkpoints.py` (which already exists as a shared module in the spec), used by both `build_prompt()` and the enriched Path A prompt builder.

### New Dependency: Section 5.7 (Path A Enrichment <-> TurnLedger Bug Fixes)

The three TurnLedger bugs (Deficiency 2 in context-01) are exclusively Path A concerns:
- `turns_consumed` always returns 0 (executor.py:1091)
- `TaskResult.output_path` never set (executor.py:1017-1025)
- `gate_rollout_mode` defaults to "off"

These are internal to the per-task loop and do not conflict with any other domain. They can be fixed in any order relative to Checkpoint, TUI, or Naming. However, the `output_path` fix enables the anti-instinct gate, which produces `GateResult` objects that feed into the TUI's error panel (F4). **Implication:** TUI error panel development should be aware that anti-instinct gate results will start appearing once `output_path` is wired.


## Revised Implementation Order

### Original Order (Section 6.2)

1. Naming Consolidation
2. Checkpoint W1 (Prompt fix)
3. TUI v2 Core (F1-F7)
4. Checkpoint W2 (Gate)
5. TUI v2 Summary (F8-F10)
6. Checkpoint W3 (Manifest + CLI)
7. Checkpoint W4 (Deferred)

### Revised Order

1. **Naming Consolidation** -- unchanged rationale: reduces noise in subsequent diffs
2. **Path A Prompt Enrichment** -- NEW. Must precede Checkpoint W1. Contains:
   - `_extract_task_block()` function (reuses `parse_tasklist` block boundaries from `config.py`)
   - Sprint context header injection (shared format with Path B)
   - Scope boundary addition (~50 tokens)
   - `TaskEntry.description` fallback fix
3. **TurnLedger Bug Fixes** -- NEW. Can be concurrent with step 2 (different lines in executor.py). Contains:
   - `turns_consumed` return value fix (executor.py:1091)
   - `TaskResult.output_path` wiring (executor.py:1017-1025)
   - `gate_rollout_mode` default change to "shadow" (aligns with `checkpoint_gate_mode` default)
4. **Checkpoint W1** (Prompt fix) -- now adds checkpoint instructions to BOTH `build_prompt()` AND the enriched Path A prompt. Uses shared constant from `checkpoints.py`.
5. **TUI v2 Core** (F1-F7) -- unchanged. Now benefits from active gate results (step 3 enables anti-instinct gate, feeding error panel F4).
6. **Checkpoint W2** (Gate) -- unchanged.
7. **TUI v2 Summary** (F8-F10) -- unchanged.
8. **Checkpoint W3** (Manifest + CLI) -- unchanged.
9. **Checkpoint W4** (Deferred) -- unchanged.

### Rationale for Position

Path A Enrichment at position 2 (after Naming, before Checkpoint W1) is motivated by:

- **Naming first:** Path A prompt may include `/sc:task` invocation. Using the post-naming canonical name avoids a rename-then-update cycle.
- **Before Checkpoint W1:** Checkpoint W1 adds prompt instructions. If Path A enrichment does not exist yet, the implementer will add checkpoint instructions only to `build_prompt()` (Path B), perpetuating the asymmetry. Enriching Path A first ensures Checkpoint W1 can target both paths in a single wave.
- **TurnLedger concurrent:** The three bug fixes touch lines 1017-1092 in executor.py. Path A prompt enrichment touches lines 1064-1068. There is overlap at lines 1064-1068 (the prompt builder) but the TurnLedger fixes are below that (1091, 1017-1025). These can be done in the same wave with one developer, or sequentially if split across developers.


## Post-Phase vs Post-Task Hook Interactions

### The Two Hook Layers

The sprint executor has two distinct hook execution points that the spec conflates:

**Layer 1: Per-Task Hooks (Path A only, executor.py:1027-1036)**

After each task subprocess completes:
1. `run_post_task_wiring_hook()` -- structural code integrity check
2. `run_post_task_anti_instinct_hook()` -- semantic output quality check
3. TUI per-task update (executor.py:1042-1048)

These hooks operate on individual `TaskResult` objects and feed `GateResult` objects into the phase-level aggregation.

**Layer 2: Post-Phase Hooks (Both paths, executor.py:1222-1233 for Path A, 1432-1454 for Path B)**

After all tasks in a phase complete (or the single Path B subprocess exits):
1. `run_post_phase_wiring_hook()` -- aggregate wiring analysis
2. `sprint_result.phase_results.append(phase_result)`
3. `logger.write_phase_result()`
4. TUI phase-complete update

### Where the Spec's New Hooks Insert

The spec (Section 6.4) proposes three new post-phase hooks:
1. `_verify_checkpoints()` -- blocking, checkpoint gate evaluation
2. `summary_worker.submit()` -- non-blocking, background thread
3. Manifest update (Wave 3) -- lightweight, blocking

### Interaction Analysis

**For Path B** (single subprocess, lines 1420-1454): The new hooks insert cleanly after `PhaseResult` construction (line 1420) and before `sprint_result.phase_results.append()` (line 1439). The proposed order works:

```
PhaseResult constructed (line 1420)
  -> run_post_phase_wiring_hook() (existing, line 1432)
  -> _verify_checkpoints() (new, Section 6.4 step 1)
  -> summary_worker.submit() (new, Section 6.4 step 2)
  -> manifest update (new, Section 6.4 step 3)
  -> sprint_result.phase_results.append() (line 1439)
```

**For Path A** (per-task loop, lines 1204-1233): The flow is structurally different. Per-task hooks have already run inside `execute_phase_tasks()`. The post-phase flow at lines 1217-1233 is:

```
PhaseResult constructed (line 1217)
  -> run_post_phase_wiring_hook() (existing, line 1222)
  -> sprint_result.phase_results.append() (line 1229)
  -> logger.write_phase_result() (line 1230)
  -> TUI update (line 1232)
  -> continue (line 1233)
```

**Critical observation:** Path A's post-phase flow is more compact and uses `continue` to skip the Path B code block. The new checkpoint/summary/manifest hooks must be inserted into BOTH the Path A post-phase block (lines 1222-1233) AND the Path B post-phase block (lines 1432-1454). The spec only describes one insertion point.

### Hook Ordering Conflicts

There are no functional conflicts between the per-task hooks and the new post-phase hooks. They operate at different granularities:

- Per-task hooks validate individual task outputs (wiring integrity, anti-instinct semantic checks)
- Post-phase hooks validate phase-level invariants (checkpoint file existence, summary generation, manifest)

However, there is a **data flow dependency**: `_verify_checkpoints()` may want to know whether per-task hooks flagged any issues. If all per-task wiring hooks passed but the checkpoint file is missing, that is a different failure mode than if tasks themselves failed. The `task_results` list (returned from `execute_phase_tasks()` at line 1208) contains this information and should be passed to `_verify_checkpoints()` for richer diagnostics.

### Recommended Hook Order for Path A Post-Phase Block

```
task_results returned from execute_phase_tasks()  (line 1208)
PhaseResult constructed                            (line 1217)
  -> run_post_phase_wiring_hook()                  (existing)
  -> _verify_checkpoints(phase, config, task_results)  (new -- receives task results for context)
  -> summary_worker.submit(phase_result, task_results) (new -- receives task results for narrative)
  -> manifest update                               (new)
  -> sprint_result.phase_results.append()
  -> logger.write_phase_result()
  -> TUI update
```

This preserves the Section 6.4 ordering while adapting it to Path A's available data. The `task_results` parameter is only available in Path A; Path B passes `None` for backward compatibility.


## Open Questions -- Resolved by Path A Analysis

### Resolved

**CE-Q3 (Context pressure mitigation) -- PARTIALLY RESOLVED.**
The spec notes 744KB output as a contributing factor to checkpoint failures and asks "Is there a token budget guard?" Path A's per-task subprocess isolation IS a context pressure mitigation: each task subprocess starts with a fresh context window. The 744KB accumulation problem is specific to Path B, where a single subprocess executes all tasks in a phase. For production sprints (Path A), context pressure is bounded by per-task scope. The remaining concern is whether individual tasks can still exceed context limits, which is addressed by TurnLedger `max_turns` constraints (once the bugs are fixed).

**CE-Q4 (Mid-phase checkpoint gate timing) -- REFRAMED.**
The spec asks about mid-phase checkpoints (e.g., CP-P03-T01-T05) being written mid-execution while the gate only verifies post-phase. In Path A, mid-phase checkpoints are naturally aligned with per-task boundaries. A checkpoint instruction could be injected after every N tasks (e.g., after task T03.05, inject "Write mid-phase checkpoint CP-P03-T01-T05"). This is impossible in Path B's single subprocess. Path A makes mid-phase checkpoints architecturally feasible rather than inference-dependent.

**CE-Q6 (`_check_checkpoint_pass()` consolidation) -- RESOLVED.**
The spec asks whether the old `_check_checkpoint_pass()` (executor.py:1592-1603) should be refactored or removed alongside the new `_verify_checkpoints()`. Answer: the old function is used at executor.py:1802 in a post-sprint summary context. The new `_verify_checkpoints()` is a superset. The old function should be replaced by a call to the new one. This is independent of the Path A/B distinction but is confirmed as safe because `_check_checkpoint_pass()` operates at phase level and both paths converge to the same post-phase block.

**TUI-Q8 (Per-task execution mode prompt preview) -- RESOLVED.**
The spec asks "F5 assumes single-prompt-per-phase. Per-task mode has multiple prompts." With Path A enrichment, each task gets a structured prompt (block extraction + sprint context + scope boundary). The TUI's `prompt_preview` field should display the CURRENT task's prompt, updated after each task subprocess launch. This requires the per-task TUI update block (executor.py:1042-1048) to include prompt text in `MonitorState`. The field should be `last_task_prompt: str` on `MonitorState`, populated from the enriched prompt built in `_run_task_subprocess()`.

### Reframed

**TUI-Q1 (prompt_preview field location) -- REFRAMED.**
Originally asked where `prompt_preview: str` should live. With dual-path awareness, the answer depends on path:
- Path B: Computed once by `build_prompt()`, stored on `Phase` or `SprintConfig`
- Path A: Changes per task, must be on `MonitorState` (updated per-task)
Recommendation: `MonitorState.prompt_preview` is the universal location. Path B sets it once at phase start. Path A updates it per task.

**TUI-Q2 (Task estimation accuracy) -- REFRAMED.**
Originally concerned about `last_task_id` ordinal giving inaccurate counts for out-of-order execution. Path A executes tasks in document order (executor.py:956: `for i, task in enumerate(tasks)`). The estimation is exact for Path A: `completed_tasks = i + 1` after each task. The inaccuracy concern applies only to Path B, where task ordering is inferred from stream-json parsing. The spec should note that Path A estimation is exact and Path B estimation is heuristic.

**CE-Q2 (Cross-wave rollback) -- REFRAMED.**
The spec notes that rolling back Wave 2 without re-applying Wave 1 creates inconsistency. With Path A enrichment as a new wave (position 2 in revised order), rollback granularity increases. Rolling back Path A enrichment is safe -- it reverts to the existing 3-line prompt. Rolling back Checkpoint W1 without Path A enrichment leaves Path B without checkpoint instructions but Path A was never going to have them anyway. The cross-wave dependency is: Checkpoint W1 depends on Path A enrichment existing (to add checkpoint instructions to both paths in the same wave). If Path A enrichment is rolled back, Checkpoint W1's Path A additions become dead code but do not break anything.

### Unchanged

The following open questions are unaffected by Path A analysis:
- CE-Q5, CE-Q7, CE-Q8 (concurrent execution, manifest schema, Wave 4 migration)
- TUI-Q3 (resolved), TUI-Q4, TUI-Q5 (resolved), TUI-Q6, TUI-Q7, TUI-Q9, TUI-Q10
- NC-Q1 through NC-Q5 (naming questions are Path B specific)


## New Cross-Cutting Concerns

### Concern 1: Prompt Construction Parity

**Risk: HIGH** | **Type: Maintenance burden**

Path A and Path B will each have their own prompt construction logic:
- Path A: `_run_task_subprocess()` in `executor.py` (per-task prompt)
- Path B: `build_prompt()` in `process.py` (per-phase prompt)

Any future prompt enhancement (checkpoint instructions, new context fields, skill invocations) must be applied to both locations. This is a classic "update one, forget the other" maintenance trap -- exactly the class of bug that created the current Path A deficiency.

**Mitigation:** Extract shared prompt components into a `prompt_builder.py` module or into functions within the existing `process.py`:
- `build_sprint_context(config, phase) -> str` -- shared sprint context header
- `build_checkpoint_instructions(config, phase) -> str` -- shared checkpoint text
- `build_scope_boundary(task) -> str` -- Path A only (Path B uses halt instructions)

Path A's `_run_task_subprocess()` and Path B's `build_prompt()` both call these shared builders. This is the single most important structural change to prevent future drift.

### Concern 2: TurnLedger Activation Side Effects

**Risk: MEDIUM** | **Type: Behavioral change**

Fixing the three TurnLedger bugs (turns_consumed, output_path, gate_rollout_mode) activates an economic feedback loop that has been dormant since v3.1. The 50 existing TurnLedger tests validate correct math on zero inputs. Once inputs are non-zero:
- Reimbursement credits become non-zero (affecting turn budgets for subsequent tasks)
- Anti-instinct gate starts evaluating (may flag legitimate outputs as non-compliant)
- Budget exhaustion halts become possible (a task could be stopped for exceeding budget)

**Mitigation:** The `gate_rollout_mode` default should change to `"shadow"` (not `"soft"` or `"full"`). Shadow mode logs gate evaluations without blocking execution. This allows observation of gate behavior on real workloads before enforcement. Align with `checkpoint_gate_mode` which also defaults to `"shadow"` in the spec (Section 7.4).

### Concern 3: Evidence Verification as a New Hook Layer

**Risk: MEDIUM** | **Type: Architectural gap**

Context-01 identifies Deficiency 3 (no evidence artifact verification). This is not addressed by either the original spec or the Path A enrichment debates. It sits between the per-task hooks (wiring, anti-instinct) and the post-phase hooks (checkpoint, summary, manifest):

- Per-task hooks validate code structure and output format
- Evidence verification would validate task-specific deliverables (files listed in `**Artifacts (Intended Paths):**`)
- Post-phase hooks validate phase-level invariants

Evidence verification is a new cross-cutting concern because:
1. It requires access to `TaskEntry` metadata (artifact paths from the phase file)
2. It requires filesystem checks (do the declared files exist?)
3. Its results should feed into both the TUI error panel (F4) and the post-phase summary (F8)
4. It applies only to Path A (Path B has no per-task artifact declarations)

**Recommendation:** Do not add evidence verification in v3.7. It depends on Path A enrichment (to have structured artifact path data available) and TurnLedger activation (to have a response mechanism). Queue for v3.8 after observing shadow-mode gate behavior.

### Concern 4: `build_task_context()` Wiring Decision

**Risk: LOW** | **Type: Dead code**

`build_task_context()` in `process.py:245-307` builds inter-task context (prior results, gate outcomes, remediation history, git diffs). It is fully implemented, extensively tested, and never called. The Path A enrichment debates did not evaluate this function.

**Cross-cutting implication:** If `build_task_context()` is wired into Path A's enriched prompt, it adds ~200-500 tokens per task of prior-task context. This interacts with:
- TurnLedger budget calculations (more input tokens per task)
- Sprint context header (partial overlap with prior-phase artifact directories)
- Scope boundary (context about other tasks may counteract isolation intent)

**Recommendation:** Keep as dead code in v3.7. Evaluate for v3.8 alongside evidence verification. The function's design assumes Path B's single-subprocess model (where all prior task context is in the same conversation). For Path A, each task is a fresh subprocess -- prior task context must be explicitly injected, making `build_task_context()` more valuable but also more expensive.

### Concern 5: Dual-Path Test Coverage

**Risk: MEDIUM** | **Type: Testing gap**

The existing test suite validates Path A and Path B independently. v3.7 improvements that must work for both paths need test cases that verify:
- Checkpoint instructions appear in BOTH `build_prompt()` output AND enriched per-task prompts
- Post-phase hooks fire for BOTH per-task phases (Path A) AND freeform phases (Path B)
- TUI updates work correctly for both per-task updates and single-subprocess stream parsing

The spec's test strategy (Section 12) does not distinguish between paths. Each test task (T02.05, T03.06) should include both-path variants.


## Net Changes to Spec

### Section 5: Cross-Domain Dependencies

| Change | Description |
|--------|-------------|
| ADD Section 5.6 | Path A Enrichment <-> Checkpoint Enforcement dependency (shared checkpoint instruction text) |
| ADD Section 5.7 | Path A Enrichment <-> TurnLedger (output_path enables anti-instinct gate, feeds TUI error panel) |
| MODIFY Section 5.5 table | Add Path A Enrichment as a fourth domain for `executor.py` and `models.py` rows |

### Section 6: Cross-Cutting Concerns

| Change | Description |
|--------|-------------|
| MODIFY Section 6.1 table | Add Path A Enrichment row for `executor.py` and `config.py` |
| MODIFY Section 6.2 order | Insert "Path A Prompt Enrichment" at position 2 and "TurnLedger Bug Fixes" at position 3 (concurrent with 2) |
| ADD Section 6.6 | Prompt Construction Parity -- shared builders to prevent drift |
| MODIFY Section 6.4 | Note that post-phase hook insertion must happen in BOTH the Path A block (lines 1222-1233) and the Path B block (lines 1432-1454); pass `task_results` to `_verify_checkpoints()` and `summary_worker.submit()` in Path A |

### Section 14: Open Questions

| Change | Description |
|--------|-------------|
| RESOLVE CE-Q3 | Path A subprocess isolation bounds context pressure per-task |
| REFRAME CE-Q4 | Mid-phase checkpoints are architecturally feasible in Path A |
| RESOLVE CE-Q6 | Old `_check_checkpoint_pass()` replaced by `_verify_checkpoints()` |
| RESOLVE TUI-Q8 | Per-task prompt preview via `MonitorState.last_task_prompt` |
| REFRAME TUI-Q1 | `MonitorState.prompt_preview` is universal location for both paths |
| REFRAME TUI-Q2 | Path A estimation is exact (`i + 1`); heuristic concern is Path B only |
| REFRAME CE-Q2 | Path A enrichment adds a new rollback dependency to the cross-wave chain |
| ADD new question | **PA-Q1**: Should `build_task_context()` (process.py:245-307) be wired into Path A enriched prompts in v3.7 or deferred to v3.8? Priority: Medium. |
