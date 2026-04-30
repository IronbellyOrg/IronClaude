# Split Boundary Rationale

## Split Point

The boundary falls between **pipeline infrastructure** (checkpoint enforcement + naming) and **presentation layer** (Sprint TUI v2). Release 1 makes the sprint pipeline deterministically reliable and consistently named. Release 2 makes the sprint pipeline visible and informative.

## Why This Boundary

1. **One-directional dependency**: Naming and Checkpoint are foundation layers that TUI consumes. TUI never feeds back into Checkpoint. This classic layered dependency is the natural seam.

2. **Different risk profiles**: R1 is low-risk (string additions, enum values, shared module, CLI subcommand — all deterministic). R2 is medium-high risk (background threading with Lock, subprocess calls to Haiku with 30s timeout, tmux pane management, real-time rendering updates).

3. **Different validation modalities**: R1 is validated by inspecting logs and JSONL events (automated, deterministic). R2 is validated by visual inspection and interactive testing (manual, subjective). Combining them means neither gets focused attention.

4. **Urgency asymmetry**: Checkpoint enforcement addresses a known production incident (OntRAG R0+R1 missing Phase 3 checkpoints, discovered 24 hours late). Every sprint between R1 and R2 benefits from enforcement. TUI features are improvements, not fixes.

5. **Rollback isolation**: If R2's SummaryWorker threading introduces issues, rolling back does not lose checkpoint enforcement. In a monolithic release, rollback removes both.

## Release 1 Delivers

- **Deterministic checkpoint enforcement**: Three-layer defense (Prevention via prompt, Detection via post-phase gate, Remediation via manifest + CLI + auto-recovery)
- **Clean naming**: `/sc:task` as canonical command, `sc-task-protocol` as canonical skill, no deprecated files in command surface
- **Data contracts for R2**: PhaseStatus.PASS_MISSING_CHECKPOINT enum, CheckpointEntry dataclass, checkpoint_gate_mode config
- **Operational tooling**: `verify-checkpoints` CLI for retroactive and ongoing checkpoint auditing
- **Observable pipeline**: JSONL `checkpoint_verification` events for every phase

## Release 2 Builds On

- **R1's data contracts**: TUI renders PASS_MISSING_CHECKPOINT with styled display (yellow/amber)
- **R1's executor state**: SummaryWorker.submit() is called after R1's _verify_checkpoints() in the post-phase hook ordering
- **R1's stable codebase**: executor.py, models.py, process.py are stable after R1, providing a clean base for TUI changes
- **R1's naming resolution**: All command references in R2's files use canonical names

## Cross-Release Dependencies

| Release 2 Item | Depends On (Release 1) | Type | Risk if R1 Changes |
|----------------|----------------------|------|---------------------|
| STATUS_STYLES[PASS_MISSING_CHECKPOINT] | PhaseStatus.PASS_MISSING_CHECKPOINT enum | Hard | Enum name change requires R2 dict key update |
| STATUS_ICONS[PASS_MISSING_CHECKPOINT] | PhaseStatus.PASS_MISSING_CHECKPOINT enum | Hard | Same as above |
| summary_worker.submit() call site | _verify_checkpoints() in executor.py | Hard | Hook ordering must be preserved |
| Post-phase hook ordering (Section 6.4) | _verify_checkpoints() + manifest update | Hard | R2 inserts between existing R1 hooks |
| TUI gate column rendering | checkpoint_gate_mode config | Soft | Only if gate column display depends on mode |
| Clean file references | Naming consolidation complete | Soft | Avoids double-rename |

## Integration Points

1. **executor.py post-phase flow**: R1 adds `_verify_checkpoints()` and manifest update. R2 adds `summary_worker.submit()` between them. The ordering is: (1) `_verify_checkpoints()` — blocking, (2) `summary_worker.submit()` — non-blocking, (3) manifest update — lightweight, blocking.

2. **models.py PhaseStatus**: R1 adds `PASS_MISSING_CHECKPOINT`. R2's TUI must render it in `STATUS_STYLES` and `STATUS_ICONS` dicts.

3. **models.py dataclasses**: R1 adds `CheckpointEntry` and `checkpoint_gate_mode` to `SprintConfig`. R2 adds `MonitorState` fields, `PhaseResult` fields, `SprintResult` properties, `total_tasks` to `SprintConfig`. No overlap — different fields in different or shared dataclasses.

4. **process.py**: R1 modifies `build_prompt()` twice (naming: prompt string, W1: checkpoint section). R2 does not modify process.py.

## Handoff Criteria

Before Release 2 planning begins, Release 1 must demonstrate:

1. Checkpoint write rate: 100% over at least 2 real sprint runs
2. Zero false positives in checkpoint gate over 2 sprint cycles
3. `/sc:task` resolves correctly in Claude Code sessions
4. `verify-checkpoints` CLI produces accurate manifest against OntRAG output
5. `make test` passes with no regressions
6. Zero remaining `sc:task-unified` references in `src/superclaude/` (except historical artifacts)

## Reversal Cost

If the split decision needs to be reversed (merge R1 and R2 back into a single release):

- **Before R1 ships**: Zero cost. Discard split specs, use original merged spec.
- **After R1 ships, before R2 begins**: Low cost. R2 spec becomes the remaining work for the combined release.
- **After R2 development begins**: Medium cost. Merge R2 branch into R1's codebase state. Primary friction: executor.py changes may need manual integration. Models changes are additive and clean.
- **After both ship**: N/A — both releases are already delivered.

The reversal cost is low at every stage, which validates the split as a safe decision.
