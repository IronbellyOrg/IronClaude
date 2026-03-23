# M15 Remediation Proposal — Exact Criteria for `status: success | partial | failed`

## Issue

The current `/sc:spawn` v2 spec defines a return contract with:

- `status: success | partial | failed`

but does not define concrete thresholds for when each value applies.

That leaves these questions unresolved:

1. Is one failed task enough to make the run `partial`?
2. When does `partial` become `failed`?
3. How should `manual` tasks be counted?
4. Should Standard Mode and Pipeline Mode use the same rules?
5. How should STOP conditions interact with aggregate counts?

This proposal defines exact, deterministic rules for both modes.

---

## Design Goal

The status field should answer one question consistently:

**How complete was the requested execution, from the orchestrator's point of view?**

That means:

- `success` = everything required by the selected mode completed without unresolved execution debt
- `partial` = some useful work completed, but the requested execution was not fully completed
- `failed` = the requested execution did not produce a sufficiently completed run, or execution hit a blocking stop condition before meaningful completion

The status must be computable from runner-observed outcomes, not agent self-interpretation.

---

## Core Principle

Use **terminal unit accounting**:

- In **Standard Mode**, the counted units are **delegated tasks**.
- In **Pipeline Mode**, the counted units are **pipeline phases**.

Each unit ends in one of these normalized outcomes:

- `completed`
- `failed`
- `manual`
- `skipped`
- `not_started`

For status calculation:

- `completed` counts as successful completion.
- `failed` counts as unsuccessful attempted completion.
- `manual` counts as unsuccessful attempted completion that produced handoff debt.
- `skipped` counts as non-completed and only contributes to `failed` when the skip was caused by upstream failure or STOP logic.
- `not_started` counts as non-completed.

For top-level status, **`manual` is treated as incomplete work, not success**.

---

## Exact Definitions

### `success`

Return `status: success` only when **all required execution units completed successfully**.

#### Standard Mode
Return `success` iff all of the following are true:

1. At least one task was created unless `--dry-run`/`--no-delegate` intentionally prevents execution.
2. `completed_count == total_required_tasks`
3. `failed_count == 0`
4. `manual_count == 0`
5. `not_started_count == 0`
6. No blocking STOP condition occurred at the command level.

Plain language:

- Every delegated task finished.
- Nothing failed.
- Nothing was deferred to manual handling.
- Nothing required by the decomposition was left unfinished.

#### Pipeline Mode
Return `success` iff all of the following are true:

1. At least one phase was scheduled.
2. `completed_phase_count == total_required_phases`
3. `failed_phase_count == 0`
4. `manual_phase_count == 0`
5. `not_started_phase_count == 0`
6. No pipeline-level STOP condition occurred.
7. No downstream phase was skipped because an upstream dependency failed.

Plain language:

- Every phase in the DAG that belongs to the run completed.
- No phase failed.
- No phase ended in manual handoff.
- No dependency break prevented execution.

---

### `partial`

Return `status: partial` when the run produced **some completed useful execution**, but **not full completion**.

This is the mixed-outcome state.

#### Standard Mode
Return `partial` iff all of the following are true:

1. `completed_count >= 1`
2. At least one of the following is true:
   - `failed_count >= 1`
   - `manual_count >= 1`
   - `not_started_count >= 1`
3. No top-level STOP condition invalidated the run before any meaningful completion.

Equivalent threshold:

- **One failed task is enough for `partial` if at least one other task completed.**
- **One manual task is enough for `partial` if at least one other task completed.**

Examples:

- 5 completed, 1 failed → `partial`
- 5 completed, 1 manual → `partial`
- 3 completed, 2 not started due to dependency fallout → `partial`
- 1 completed, 9 manual → `partial`

#### Pipeline Mode
Return `partial` iff all of the following are true:

1. `completed_phase_count >= 1`
2. At least one of the following is true:
   - `failed_phase_count >= 1`
   - `manual_phase_count >= 1`
   - `not_started_phase_count >= 1`
   - one or more downstream phases were skipped because dependencies did not complete
3. The pipeline did not fully collapse before any phase completed.

Equivalent threshold:

- **One failed phase is enough for `partial` if at least one other phase completed.**
- **One manual phase is enough for `partial` if at least one other phase completed.**

Examples:

- analyze completed, design failed, test not started → `partial`
- analyze completed, design manual after retry exhaustion, test blocked → `partial`
- phase group of 4: 3 completed, 1 failed → `partial`

---

### `failed`

Return `status: failed` when the run did **not achieve any completed execution unit**, or when a top-level blocking condition stops the run before meaningful completion can be claimed.

#### Standard Mode
Return `failed` iff either condition set applies:

##### A. Zero-completion failure
1. `completed_count == 0`, and
2. One or more of the following is true:
   - `failed_count >= 1`
   - `manual_count >= 1`
   - `not_started_count == total_required_tasks`
   - decomposition succeeded but delegation/execution never produced a completed task

##### B. Blocking top-level STOP failure
A command-level STOP condition occurs before any task completes, such as:

- missing required input
- decomposition cannot be constructed
- invalid command/agent mapping
- checkpoint resume corruption that prevents execution
- orchestration abort before first task completion

Plain language:

- If nothing completed, the run is `failed`.
- Manual-only outcomes without any completed task are still `failed`, not `partial`.

Examples:

- 0 completed, 2 failed, 4 manual → `failed`
- 0 completed, all tasks manual after retries → `failed`
- no tasks could be executed because setup failed → `failed`

#### Pipeline Mode
Return `failed` iff either condition set applies:

##### A. Zero-completion failure
1. `completed_phase_count == 0`, and
2. One or more of the following is true:
   - `failed_phase_count >= 1`
   - `manual_phase_count >= 1`
   - `not_started_phase_count == total_required_phases`
   - first executable phase failed or went manual, preventing all progress

##### B. Blocking pipeline STOP failure
A pipeline-level STOP condition occurs before any phase completes, such as:

- YAML/shorthand parse failure
- cycle detected in DAG
- missing required `${prompt}` after prompt resolution
- invalid phase type
- `generate-parallel` without `--agents`
- `compare-merge` with fewer than 2 artifacts
- first runnable phase fails in a way that halts all remaining execution

Plain language:

- If no phase completed, the pipeline is `failed`.
- A pipeline that aborts at validation or before first useful phase completion is `failed`.

Examples:

- parse error before execution → `failed`
- first phase failed, all dependents skipped → `failed`
- first phase became manual, no other phase could run → `failed`

---

## Treatment of `manual`

## Normative Rule

A `manual` unit is **not successful completion**.

For top-level contract status:

- `manual` contributes to `partial` when there is also at least one `completed` unit.
- `manual` contributes to `failed` when there are zero `completed` units.

This is the simplest and least ambiguous rule because manual handoff means the orchestrator did not finish the requested work autonomously.

### Why not count `manual` as success?

Because the spec already uses `manual` as a fallback for unresolved execution debt:

- retry exhausted
- sub-agent could not complete
- operator intervention now required

If `manual` counted as success, a run with many unfinished tasks could still claim `success`, which would make the contract misleading.

### Why not make `manual` always `failed`?

Because the run may still have delivered substantial useful output. If some tasks/phases completed and others were handed off, that is exactly what `partial` is for.

---

## Threshold Summary Table

### Standard Mode

| Completed tasks | Failed tasks | Manual tasks | Not started tasks | Top-level status |
|---|---:|---:|---:|---|
| all | 0 | 0 | 0 | `success` |
| >=1 | any >=1 | any | any | `partial` |
| >=1 | any | any >=1 | any | `partial` |
| >=1 | 0 | 0 | any >=1 | `partial` |
| 0 | any >=1 | any | any | `failed` |
| 0 | any | any >=1 | any | `failed` |
| 0 | 0 | 0 | all | `failed` |

### Pipeline Mode

| Completed phases | Failed phases | Manual phases | Blocked/not started phases | Top-level status |
|---|---:|---:|---:|---|
| all | 0 | 0 | 0 | `success` |
| >=1 | any >=1 | any | any | `partial` |
| >=1 | any | any >=1 | any | `partial` |
| >=1 | 0 | 0 | any >=1 | `partial` |
| 0 | any >=1 | any | any | `failed` |
| 0 | any | any >=1 | any | `failed` |
| 0 | 0 | 0 | all | `failed` |

---

## Mode-Specific Clarifications

### Standard Mode Clarification

Standard Mode decomposes a task into delegated work items. Therefore its return status must be based on **delegated task completion**, not on whether decomposition alone succeeded.

So:

- successful planning with zero completed delegated tasks is **not** `success`
- hierarchy document written but no delegated execution completed is **not** `partial`
- it is `failed` unless the command explicitly documents a non-executing mode such as `--dry-run`

### Pipeline Mode Clarification

Pipeline Mode executes an explicit DAG. Therefore its return status must be based on **phase completion across the DAG**, not just manifest creation.

So:

- manifest written but no phase completed is **not** `partial`
- independent branches that complete while one branch fails yield `partial`
- dependency-caused skips count against full completion and therefore prevent `success`

---

## Special Handling for Non-Executing Modes

These cases should not use the normal execution-completeness semantics unless the spec explicitly wants them to.

### `--dry-run`

Recommended rule:

- Return `status: success` only if validation/planning completed as intended.
- Include `execution_performed: false` in the return contract.

Rationale:
A dry run intentionally requests planning, not execution. It should be judged against its own objective.

### `--no-delegate`

Recommended rule:

- Return `status: success` only if the hierarchy/delegation plan was fully produced.
- Include `execution_performed: false` and `delegation_suppressed: true`.

Rationale:
This mode intentionally stops before sub-agent execution.

If the team does not want special-case semantics, then these modes must be documented as planning-only and excluded from the normal execution status contract. But they should not silently reuse the same meanings without documentation.

---

## Recommended Computation Algorithm

### Standard Mode

1. Build the full set of required delegated tasks.
2. Normalize each task to one of: `completed`, `failed`, `manual`, `not_started`, `skipped`.
3. Compute:
   - `completed_count`
   - `failed_count`
   - `manual_count`
   - `not_started_count`
4. If a planning-only mode is active, use planning-only status rules.
5. Else if `completed_count == total_required_tasks` and all other non-complete counts are zero, return `success`.
6. Else if `completed_count >= 1`, return `partial`.
7. Else return `failed`.

### Pipeline Mode

1. Build the full set of required phases from the DAG.
2. Normalize each phase to one of: `completed`, `failed`, `manual`, `not_started`, `skipped_due_to_dependency`, `skipped_by_policy`.
3. Treat `skipped_due_to_dependency` as non-complete for top-level status.
4. Compute:
   - `completed_phase_count`
   - `failed_phase_count`
   - `manual_phase_count`
   - `not_started_phase_count`
5. If `completed_phase_count == total_required_phases` and all other non-complete counts are zero, return `success`.
6. Else if `completed_phase_count >= 1`, return `partial`.
7. Else return `failed`.

---

## Proposed Normative Spec Text

Add this under `## Return Contract` in the v2 spec.

```md
### Status computation

The `status` field reports overall execution completeness.

#### Standard Mode
Evaluate status over delegated tasks.

- `success`: all required delegated tasks completed; zero failed, zero manual, zero not-started.
- `partial`: at least one delegated task completed, but full completion was not achieved because one or more tasks failed, became manual, or did not start.
- `failed`: zero delegated tasks completed, or execution stopped before any task completed.

`manual` counts as incomplete work:
- if at least one task completed, `manual` contributes to `partial`
- if zero tasks completed, `manual` contributes to `failed`

#### Pipeline Mode
Evaluate status over pipeline phases.

- `success`: all required phases completed; zero failed, zero manual, zero dependency-blocked/not-started.
- `partial`: at least one phase completed, but full completion was not achieved because one or more phases failed, became manual, or were blocked/not started.
- `failed`: zero phases completed, or pipeline execution stopped before any phase completed.

A single failed or manual unit is sufficient to prevent `success`.
A single failed or manual unit yields `partial` only when at least one other required unit completed.
Otherwise the run is `failed`.
```

---

## Recommended Companion Schema Change

To make the contract auditable, add explicit counts.

### Standard fields

```yaml
status: success|partial|failed
mode: standard|pipeline
completed_count: <int>
failed_count: <int>
manual_count: <int>
not_started_count: <int>
```

### Pipeline-specific extension

```yaml
dependency_blocked_count: <int>
```

This avoids forcing consumers to infer status from a free-form `completion_summary` object.

---

## Acceptance Criteria

1. The spec states whether one failed task is enough for `partial`.
2. The spec states whether one manual task is enough for `partial`.
3. The spec defines the boundary between `partial` and `failed` using a concrete threshold.
4. Standard Mode uses delegated-task counts as the status basis.
5. Pipeline Mode uses phase counts as the status basis.
6. `success` requires zero failed/manual/unstarted required units.
7. `partial` requires at least one completed required unit.
8. `failed` applies whenever zero required units completed or execution stopped before meaningful completion.
9. `manual` is explicitly documented as incomplete work, not success.
10. The return contract includes enough counts for downstream verification.

---

## Final Recommendation

Adopt the following exact policy:

- **`success` = all required units completed, with zero failed/manual/unstarted units.**
- **`partial` = at least one required unit completed, but at least one other required unit failed/manual/unstarted.**
- **`failed` = zero required units completed, or a blocking STOP condition ended execution before any required unit completed.**
- **`manual` never counts as success.** It contributes to `partial` only when there is also at least one completed unit; otherwise it contributes to `failed`.

This rule is concrete, mode-aware, easy to compute, and directly answers the ambiguity raised in M15.