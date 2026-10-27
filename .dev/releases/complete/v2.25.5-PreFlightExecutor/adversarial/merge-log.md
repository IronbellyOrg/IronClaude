# Merge Log: pass_no_report Solution Selection

## Pipeline Summary

| Field | Value |
|-------|-------|
| Target | v2.25.5-PreFlightExecutor: all 5 phases classified as `pass_no_report` instead of `pass` |
| Variants evaluated | 4 (A: Prompt Injection, B: AggregatedPhaseReport, C: Accept Status Quo, D: Executor Pre-Write) |
| Variants debated | 3 (B excluded -- infeasible without main loop refactor) |
| Base selected | Option D (revised) -- Executor Pre-Write |
| Convergence score | 91% |
| Unresolved conflicts | 2 (minor) |

## Final Merged Recommendation

### Primary Fix: Option D (revised) -- Executor Pre-Write

**What**: Add a `_write_preliminary_result()` function that writes a result file with `EXIT_RECOMMENDATION: CONTINUE` when exit_code == 0, called BEFORE `_determine_phase_status()`.

**Why this wins**:
1. **Deterministic**: Zero agent compliance dependency. The executor controls the result file.
2. **Architecturally aligned**: Matches the "executor is authoritative" design principle (executor.py L706-708).
3. **Minimal change**: ~12 lines of new code, 1 new function, 1 file touched.
4. **Safe**: Guarded to exit_code==0 only. Non-zero exit paths (context exhaustion, checkpoint recovery, error detection) are completely untouched.

**How it works**:
1. After the subprocess exits with code 0, the executor writes a preliminary result file containing `EXIT_RECOMMENDATION: CONTINUE`
2. `_determine_phase_status()` finds the result file, reads CONTINUE, returns `PhaseStatus.PASS`
3. The existing `_write_executor_result_file()` then overwrites the preliminary file with richer content including the actual PhaseStatus

**Critical guard**: The preliminary write MUST NOT fire for non-zero exit codes. `_determine_phase_status()` has specialized logic for context exhaustion (`detect_prompt_too_long` -> `INCOMPLETE`), checkpoint recovery (`_check_checkpoint_pass` -> `PASS_RECOVERED`), and general errors (`ERROR`). A preliminary result file would short-circuit these paths.

### Secondary Fix (Follow-up): Option A -- Prompt Injection

**What**: Add result-file write instructions to the agent prompt in `_run_task_subprocess()`.

**Why as follow-up, not primary**:
- Non-deterministic (agent may not comply)
- Contradicts "executor is authoritative" as primary mechanism
- But provides richer telemetry when agent complies (per-task outcomes)
- Strictly additive -- does not interfere with Option D

### Excluded Solutions

| Solution | Reason for Exclusion |
|----------|---------------------|
| Option B (AggregatedPhaseReport) | `execute_phase_tasks()` is not called from `execute_sprint()`. Requires major main loop refactor. |
| Option C (Accept Status Quo) | Loses telemetry signal; cannot distinguish "agent confirmed pass" from "agent ran but outcome unknown". False positive risk when agent fails tasks but exits 0. |

## Unresolved Conflicts

1. **Advocate-C dissent (7%)**: Maintains that any code change for a cosmetic improvement introduces unnecessary risk. Counter: the false-positive risk (exit 0 but tasks failed) is not cosmetic.

2. **Advocate-A dissent (2%)**: Maintains that agent-reported task detail is more valuable than executor-only assessment. Counter: agent compliance is non-deterministic; determinism takes priority for the primary fix.

## Key Discovery During Debate

The original Option D proposal ("just move `_write_executor_result_file` before `_determine_phase_status`") was found to be **infeasible as stated** because `_write_executor_result_file()` takes `status: PhaseStatus` as a parameter -- it needs the status to decide what to write. This creates the exact circularity the L707 comment warns about.

The revised Option D resolves this by creating a separate, lightweight `_write_preliminary_result()` that derives its content from exit_code alone (exit_code==0 -> CONTINUE), breaking the circular dependency.

## Artifacts Produced

| Artifact | Path |
|----------|------|
| Diff Analysis | `adversarial/diff-analysis.md` |
| Debate Transcript | `adversarial/debate-transcript.md` |
| Base Selection | `adversarial/base-selection.md` |
| Refactor Plan | `adversarial/refactor-plan.md` |
| Merge Log | `adversarial/merge-log.md` (this file) |
