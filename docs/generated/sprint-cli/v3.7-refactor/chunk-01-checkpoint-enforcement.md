---
title: "Chunk 1: Checkpoint Enforcement — Path A/B Refactoring Analysis"
chunk: checkpoint-enforcement
spec_sections: "3.1, 4.1 (Waves 1-4)"
generated: 2026-04-03
---

# Checkpoint Enforcement -- Refactoring Analysis

## Executive Summary

The checkpoint enforcement feature (17 tasks across 4 waves) is predominantly phase-level infrastructure that already works for both paths. The one significant exception is Wave 1's T01.01, which adds checkpoint instructions exclusively to Path B's `build_prompt()` -- the very function that only fires for malformed tasklists. Path A's per-task subprocess model changes the checkpoint problem fundamentally: individual task workers cannot write end-of-phase checkpoints because they have no phase-level awareness. The executor (orchestrator layer) is the correct checkpoint actor for Path A, making Wave 2's detection gate the primary defense for production sprints and Wave 1's prompt instructions irrelevant to Path A.

## Per-Task Analysis

### T01.01 -- Add checkpoint instructions to build_prompt() in process.py

- **Current target**: Path B (`process.py:build_prompt()`)
- **Path A applicability**: NONE. Path A spawns isolated per-task subprocesses via `_run_task_subprocess()` at `executor.py:1064-1068`. Each worker executes a single task. No individual task worker should write end-of-phase checkpoint reports because: (a) it does not know if it is the last task, (b) checkpoint writing after "all tasks complete" is a phase-level concern, not a task-level concern, and (c) subprocess isolation means the orchestrator controls phase lifecycle. Injecting "scan the phase file for checkpoint sections" into a per-task prompt would produce unpredictable behavior -- early tasks would skip it, the last task might or might not execute it, and the boundary is fragile.
- **Recommendation**: LEAVE PATH B ONLY
- **Rationale**: In Path A, the executor (orchestrator) is the correct actor for checkpoint enforcement, not the per-task worker. Wave 2's `_verify_checkpoints()` gate (T02.04) handles this at the right architectural layer. Adding checkpoint prompt instructions to per-task prompts would create confused responsibility -- the orchestrator already has a post-phase hook site. Path B needs these instructions because a single subprocess runs all tasks and must self-manage its lifecycle including checkpoints.

### T01.02 -- Add _warn_missing_checkpoints() helper to executor.py

- **Current target**: Both paths (operates at executor phase-completion level)
- **Path A applicability**: FULL. This function runs in the executor after `determine_phase_status()` returns PASS, regardless of which execution path produced the phase result. The executor's phase completion flow is shared between Path A and Path B.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Already targets the correct layer (executor, post-phase). The function checks checkpoint file existence on disk after a phase completes -- this is path-agnostic. It is later replaced by T02.04's full gate, but its initial wiring establishes the call site for both paths.

### T02.01 -- Create checkpoints.py with extract_checkpoint_paths()

- **Current target**: Both paths (shared utility module)
- **Path A applicability**: FULL. The module provides parsing utilities consumed by the executor-level gate (T02.04) and the CLI verify command (T03.04). Neither consumer is path-specific.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Pure utility module with no path coupling. `extract_checkpoint_paths()` reads phase tasklist markdown files and returns expected checkpoint paths. This is consumed by executor-level infrastructure that runs identically for both paths.

### T02.02 -- Add PASS_MISSING_CHECKPOINT to PhaseStatus enum in models.py

- **Current target**: Both paths (phase-level status)
- **Path A applicability**: FULL. `PhaseStatus` is set by the executor after phase completion, not by the worker subprocess. Both paths converge to the same `determine_phase_status()` call in the executor.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Phase status is an orchestrator-level concept. The new enum variant and `checkpoint_gate_mode` config field are path-agnostic.

### T02.03 -- Add write_checkpoint_verification() to logging_.py

- **Current target**: Both paths (structured logging)
- **Path A applicability**: FULL. JSONL events are emitted by the executor, not by worker subprocesses. The logging call site is in `_verify_checkpoints()` which runs post-phase for both paths.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Logging infrastructure has no path coupling.

### T02.04 -- Wire _verify_checkpoints() into executor.py phase completion flow

- **Current target**: Both paths (executor-level gate)
- **Path A applicability**: FULL. This is actually the PRIMARY defense for Path A. Since Path A workers cannot self-manage checkpoint writing (they are isolated per-task subprocesses), the executor-level post-phase gate is the only enforcement mechanism that applies. For Path B, this is a secondary defense behind the prompt instructions (T01.01). For Path A, this IS the defense.
- **Recommendation**: KEEP AS-IS, but add a documentation note
- **Rationale**: The spec correctly places this gate in the executor's phase completion flow, which is shared. However, the spec's framing positions this as "Layer 2 -- Detection" behind "Layer 1 -- Prevention (prompt)." For Path A, this note should clarify: Layer 1 (prompt prevention) does not apply to Path A -- Layer 2 (detection gate) is the primary enforcement mechanism for production sprints. This reframing is important for risk assessment: if the gate is disabled (`checkpoint_gate_mode=off`), Path A has ZERO checkpoint enforcement.
- **Implementation sketch**: Add a comment block or spec note:
  ```
  # NOTE: For Path A (per-task subprocess), this gate is the PRIMARY checkpoint
  # enforcement mechanism. Path A workers are task-scoped and cannot write
  # end-of-phase checkpoints. The prompt-level prevention (T01.01) only applies
  # to Path B (freeform single-subprocess). Default gate mode should be "soft"
  # or "full" for production sprints, not "shadow".
  ```

### T02.05 -- Unit tests for checkpoints.py and PASS_MISSING_CHECKPOINT integration

- **Current target**: Both paths (test infrastructure)
- **Path A applicability**: FULL. Tests should cover the gate behavior regardless of which execution path produced the phase result.
- **Recommendation**: EXTEND TO PATH A
- **Rationale**: The test suite should include a test case that exercises the checkpoint gate after a Path A execution (per-task subprocess loop), not only after Path B. The gate logic is the same, but verifying it fires correctly in the Path A flow ensures no accidental path-specific bypass.
- **Implementation sketch**: Add a test fixture or test case in `test_checkpoints.py` that:
  1. Simulates a Path A phase execution (multiple `TaskResult` objects accumulated)
  2. Verifies `_verify_checkpoints()` is called after `determine_phase_status()` returns PASS
  3. Verifies `PASS_MISSING_CHECKPOINT` status is assigned when checkpoints are missing in `full` mode
  This may already be covered if tests mock at the phase-result level, but explicit Path A flow coverage should be confirmed.

### T03.01 -- Add CheckpointEntry dataclass and manifest types to models.py

- **Current target**: Both paths (data model)
- **Path A applicability**: FULL. Data model is path-agnostic.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Pure data model with no execution path coupling.

### T03.02 -- Extend checkpoints.py with build_manifest() and write_manifest()

- **Current target**: Both paths (manifest infrastructure)
- **Path A applicability**: FULL. Manifest is built from on-disk checkpoint files, not from execution path state. Both paths produce the same filesystem artifacts (or fail to).
- **Recommendation**: KEEP AS-IS
- **Rationale**: Manifest reads the filesystem to determine checkpoint completeness. It does not care which execution path produced (or failed to produce) the checkpoint files.

### T03.03 -- Add recover_missing_checkpoints() to checkpoints.py

- **Current target**: Both paths (post-sprint remediation)
- **Path A applicability**: FULL. Recovery reads evidence artifacts on disk and generates missing checkpoints. This is entirely post-execution and path-agnostic.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Remediation operates on filesystem state, not execution path state. The original failure that motivated this feature (OntRAG Phase 3) could occur in either path.

### T03.04 -- Add verify-checkpoints CLI subcommand to commands.py

- **Current target**: Both paths (CLI tool, operates post-sprint)
- **Path A applicability**: FULL. CLI tool reads output directory contents.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Entirely decoupled from execution path. Works retroactively on any sprint output.

### T03.05 -- Wire manifest build/verify into executor.py sprint lifecycle

- **Current target**: Both paths (executor-level lifecycle)
- **Path A applicability**: FULL. Sprint start and sprint end events are in the executor's outer loop, shared by both paths.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Manifest building happens at sprint start (before any phase executes) and sprint end (after all phases complete). These are outer-loop events unaffected by per-phase execution path.

### T03.06 -- Unit + integration tests for manifest, recovery, and CLI verify-checkpoints

- **Current target**: Both paths (test infrastructure)
- **Path A applicability**: FULL.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Tests target the manifest/recovery/CLI layer, which is path-agnostic.

### T04.01 -- Update sc-tasklist-protocol SKILL.md checkpoint generation rules

- **Current target**: Both paths (tasklist generation, upstream of execution)
- **Path A applicability**: This is where it gets interesting. Converting `### Checkpoint:` headings to `### T<PP>.<NN> -- Checkpoint:` task entries means Path A's task scanner (`_parse_phase_tasks()`) will now pick up checkpoint tasks as regular tasks. Each checkpoint task will be dispatched to a per-task subprocess, which will write the checkpoint file as its primary deliverable. This ELIMINATES the checkpoint problem for Path A entirely -- checkpoint writing becomes a normal task execution, not an emergent behavior.
- **Recommendation**: EXTEND TO PATH A -- add explicit documentation of the Path A benefit
- **Rationale**: The spec frames T04.01 as addressing "Cause 2 (structural mismatch)" where `### Checkpoint:` headings are invisible to the task scanner. But the spec does not explicitly call out that this fix has a transformative effect on Path A: it converts checkpoints from "something the executor must verify after the fact" to "something a worker subprocess executes as a task." This is arguably the MOST valuable checkpoint improvement for Path A, yet the spec buries it as a future-tasklist normalization concern.
- **Implementation sketch**: Add to the spec's T04.01 rationale:
  ```
  Path A Impact: When checkpoint sections are normalized to T<PP>.<NN> task entries,
  Path A's _parse_phase_tasks() will include them in the per-task loop. Each checkpoint
  task dispatches to a subprocess that writes the checkpoint file as its primary
  deliverable. This converts checkpoint enforcement from a post-phase detection problem
  (Wave 2 gate) to an inline execution guarantee -- the checkpoint is simply another task.
  
  Combined with Wave 2's gate (which now serves as a belt-and-suspenders verification),
  this provides two independent enforcement layers for Path A:
  1. Task execution (Wave 4) -- checkpoint written as a regular task
  2. Post-phase gate (Wave 2) -- verification that the file exists
  ```

### T04.02 -- Add checkpoint task validation to Sprint Compatibility Self-Check

- **Current target**: Both paths (tasklist validation rules, upstream of execution)
- **Path A applicability**: FULL. Validation rules ensure generated tasklists are well-formed for both execution paths. The validation that checkpoint tasks exist and are properly positioned benefits Path A by ensuring `_parse_phase_tasks()` will encounter them.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Upstream validation is path-agnostic by nature.

### T04.03 -- Update deliverable registry guidance for checkpoint deliverables

- **Current target**: Both paths (documentation/convention)
- **Path A applicability**: FULL. Deliverable naming conventions apply regardless of execution path.
- **Recommendation**: KEEP AS-IS
- **Rationale**: Documentation-level change with no execution path coupling.

## Wave-Level Summary

| Wave | Current Target | Recommended Target | Change Required |
|------|---------------|-------------------|-----------------|
| Wave 1 (Prevention/Prompt) | T01.01: Path B; T01.02: Both | T01.01: Path B only (correct); T01.02: Both (correct) | No code changes. Add spec note clarifying T01.01 is deliberately Path B only and why. |
| Wave 2 (Detection/Gate) | Both (executor-level) | Both -- but reframe as PRIMARY for Path A | Minor: Add documentation that this gate is the primary (not secondary) defense for Path A. Consider changing default `checkpoint_gate_mode` from `"shadow"` to `"soft"` given that production sprints (Path A) have no other enforcement layer until Wave 4 ships. Extend T02.05 tests to explicitly cover Path A flow. |
| Wave 3 (Remediation/CLI) | Both (post-execution) | Both (correct) | None. Entire wave operates on filesystem state, fully path-agnostic. |
| Wave 4 (Normalization) | Both (tasklist generation) | Both -- but add explicit Path A benefit analysis | Minor: Add documentation in T04.01 explaining the transformative effect on Path A (checkpoints become regular tasks in the per-task loop). |

## Net Changes to Spec

1. **T01.01 -- Add spec note (no code change)**: Explicitly state that T01.01 is Path B only by design. Path A workers are task-scoped subprocesses that cannot write end-of-phase checkpoints. The executor-level gate (T02.04) is the correct enforcement mechanism for Path A.

2. **Section 3.1 -- Reframe Layer 1 vs Layer 2 for Path A**: The "Three-Layer Defense" description (Section 3.1) positions Layer 1 (Prevention/Prompt) as the primary defense and Layer 2 (Detection/Gate) as secondary. For Path A, the hierarchy is inverted: Layer 2 is primary, Layer 1 does not apply. Add a subsection or note: "For Path A (per-task subprocess), Layer 2 (Detection) is the primary enforcement mechanism. Layer 1 (Prevention) applies only to Path B (freeform subprocess)."

3. **T02.04 -- Consider changing default `checkpoint_gate_mode`**: The spec sets the default to `"shadow"` (log only, no behavioral change). Since production sprints run exclusively via Path A, and Path A has no Layer 1 prevention, `"shadow"` means production sprints have zero enforced checkpoint defense until a human reads the JSONL logs. Recommend changing default to `"soft"` (log + warning) for Wave 2 ship, with `"full"` (status downgrade) as the target for Wave 3.

4. **T02.05 -- Extend test coverage**: Add explicit test case verifying the checkpoint gate fires correctly in a Path A execution flow (multiple `TaskResult` objects from per-task subprocesses).

5. **T04.01 -- Add Path A impact documentation**: Document that normalizing `### Checkpoint:` to `### T<PP>.<NN> -- Checkpoint:` task entries transforms the checkpoint problem for Path A from a post-phase detection concern to an inline execution guarantee. This is the most architecturally significant change for Path A in the entire checkpoint enforcement feature.

6. **Section 3.1 Solution-to-Root-Cause Coverage Matrix -- Add Path A column**: The existing matrix maps solutions to root causes but does not distinguish which execution path each solution covers. Add a "Path A Coverage" and "Path B Coverage" column to make explicit that Solution 1 (Prompt) covers Path B only, while Solutions 2-4 cover both paths.

## Architectural Observation

The checkpoint enforcement design has an asymmetry that the spec does not call out: **for Path A, the defense layers are temporally ordered as Wave 2 (immediate) then Wave 4 (deferred), with Wave 1 being irrelevant.** This means production sprints shipping after Wave 2 but before Wave 4 rely entirely on the post-phase detection gate in shadow mode -- a monitoring-only posture with no enforcement. The spec's risk assessment ("Very Low" for Wave 1, "Low" for Wave 2) does not account for this: Wave 2's gate is the only production defense and should be treated as a higher-priority, lower-risk-tolerance deliverable than the spec currently frames it.

The recommendation to change the default from `"shadow"` to `"soft"` directly addresses this gap. In `"soft"` mode, missing checkpoints produce visible warnings in the sprint output, providing human-observable enforcement without halting the sprint. This is the correct posture for the interim period between Wave 2 and Wave 4 shipment.
