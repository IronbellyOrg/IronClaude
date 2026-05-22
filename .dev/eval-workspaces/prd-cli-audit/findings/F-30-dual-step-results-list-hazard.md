# F-30: Dual `step_results` list maintenance hazard

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P8
**Identified by**: A-14
**File:line**: `src/superclaude/cli/prd/executor.py:463-467, 792-802`

## Evidence

Both `self._step_results` and `result.step_results` are maintained as parallel lists with separate append sites at every callsite (run loop, `_execute_stage_b`, `_execute_qa_fix_cycle`, `_execute_parallel_steps`).

## Trace

- `_execute_step` does NOT internally append; the caller is responsible for appending to both lists.
- Any future callsite that appends to only one list drifts silently.
- `_step_results` feeds diagnostics and TUI; `result.step_results` feeds the final pipeline result.
- Not an active bug today (Agent A retracted the duplicate-append claim), but a recognized P8 anti-pattern.

## Reproduction sketch

Add a new callsite that appends to only `result.step_results` -- diagnostics and TUI based on `self._step_results` silently undercount.

## Confidence (aggregated)

0.70 -- Agent A identified this as a maintenance risk, not an active defect.

## Cross-agent corroboration

- **Agent A** identified the dual-list pattern and retracted the duplicate-append claim after careful re-reading, but flagged the structural risk: two lists with no invariant enforcement.
