---
title: "Context Document 2: Adversarial Debate Rulings & Recommended Changes"
generated: 2026-04-03
purpose: Synthesis of 5 adversarial debates on what Path B components should be integrated into Path A
source: /sc:adversarial --depth quick, 5 parallel debate agents
---

# Adversarial Debate Rulings

## Overview

Five components from Path B's `build_prompt()` (process.py:123-204) were evaluated for integration into Path A's `_run_task_subprocess()` (executor.py:1064-1068). Each was debated via `/sc:adversarial --depth quick`.

## Ruling 1: Per-Task Block Extraction — INTEGRATE (modified)

**Score**: FOR 0.82 vs AGAINST 0.71 (11.5% margin)
**Full transcript**: `docs/generated/sprint-cli/debates/debate-file-preloading.md`

### Decision
Do NOT preload the full phase file via `@{phase_file}`. Instead, extract the specific task's markdown block from the phase file and inject it inline in the prompt.

### Rationale
- Full-file preload wastes 45,000-135,000 tokens on sibling tasks across 10 subprocesses
- Sibling task visibility causes scope contamination
- `parse_tasklist` in `config.py` already identifies `### T<PP>.<TT>` block boundaries
- Per-task block gives acceptance criteria, steps, validation commands, deliverables, dependencies without noise

### Implementation Sketch
```python
# In _run_task_subprocess or execute_phase_tasks:
task_block = _extract_task_block(phase.file, task.task_id)  # New function
prompt = (
    f"Execute task {task.task_id}: {task.title}\n"
    f"From phase file: {phase.file}\n\n"
    f"{task_block}\n"  # Full task spec inline
)
```

### Secondary Fix
Ensure `TaskEntry.description` never defaults to empty string — fall back to first non-heading paragraph from task block.

## Ruling 2: Scope Boundary — INTEGRATE

**Score**: 83% convergence (5 of 6 points)
**Full transcript**: `docs/generated/sprint-cli/debates/debate-scope-boundary.md`

### Decision
Add positive-framing scope boundary to per-task prompt.

### Rationale
- Per-task prompt includes `From phase file: {path}` which hands the worker the exact path to all tasks
- Worker has `--dangerously-skip-permissions` and full filesystem access
- Implicit scoping (only naming one task) is an unvalidated assumption about model behavior
- Cost: ~50 tokens

### Implementation
```
Execute ONLY task {task_id}. No other tasks.
STOP when {task_id} is complete.
```
Use positive framing — avoid enumerating what NOT to do (which draws attention to it).

## Ruling 3: Result File Contract — REJECT

**Score**: AGAINST won 4-3 (70% convergence)
**Full transcript**: `docs/generated/sprint-cli/debates/debate-result-file-contract.md`

### Decision
Do NOT add per-task result file contract. Exit code + post-task hooks are sufficient.

### Rationale
- Post-task wiring hook and anti-instinct hook perform third-party audit (superior to self-reported results)
- Adding result files creates redundant, inferior signal channel
- N files per phase increases filesystem complexity
- Exit code is reliable enough for individual tasks

### Condition
Wiring hook must be in `soft` or `full` enforcement mode (not `shadow`) for production sprints.

## Ruling 4: Sprint Context — INTEGRATE

**Score**: FOR 0.862 vs AGAINST 0.708 (15.4% margin)
**Full transcript**: `docs/generated/sprint-cli/debates/debate-sprint-context.md`

### Decision
Inject sprint context header into per-task prompt.

### Rationale
- Path B already builds `## Sprint Context` — Path A's omission is an oversight, not a design choice
- Cost: ~80 tokens against per-task budgets of 100+ turns
- TASKLIST_ROOT is a placeholder; `SprintConfig.release_dir` is already computed
- Cross-phase tasks need resolved artifact paths
- Use same `## Sprint Context` header format as Path B

### Implementation
```
## Sprint Context
- Sprint: {sprint_name}
- Phase: {pn} of {total_phases}
- Artifact root: {artifact_root}
- Results directory: {results_dir}
- Prior-phase artifact directories: {prior_dirs}  # if phase > 1
```

## Ruling 5: Stop-on-STRICT-Fail — REJECT

**Score**: AGAINST 0.795 vs FOR 0.64 (15.5% margin)
**Full transcript**: `docs/generated/sprint-cli/debates/debate-strict-halt.md`

### Decision
Do NOT add stop-on-STRICT-fail instructions to per-task prompts.

### Rationale
- Path A's subprocess isolation IS the halt mechanism — each worker sees exactly one task
- Path B needs halt instructions because a single subprocess executes all tasks
- The inconsistency is justified by architectural differences, not a defect

### Recommended Structural Improvements Instead
1. Add `enforcement_tier` field to `TaskEntry` in `models.py:26` — orchestrator currently has no tier awareness
2. Consider per-task `max_turns` scaling by tier via TurnLedger constraints (not prompt instructions)

## Summary: Net Prompt Changes for Path A

**Add (~280 tokens total):**
1. Per-task markdown block extraction from phase file (~variable, ~150 tokens avg)
2. Scope boundary: `"Execute ONLY task {task_id}. STOP when complete."` (~50 tokens)
3. Sprint context header (~80 tokens)

**Don't add:**
4. ~~Result file contract~~ (hooks are better)
5. ~~Stop-on-STRICT-fail~~ (subprocess isolation handles this)
