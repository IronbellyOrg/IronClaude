---
adversarial:
  agents:
    - opus:architect
    - opus:analyzer
  convergence_score: 0.83
  base_variant: architect
  artifacts_dir: .dev/releases/backlog/v3.7-task-unified-v2/release-split/
  unresolved_conflicts: 0
  fallback_mode: false
---

# Split Proposal — Final (Adversarially Validated)

**Date**: 2026-04-02
**Source**: v3.7-UNIFIED-RELEASE-SPEC-merged.md
**Verdict**: **SPLIT**
**Merged Confidence**: 0.83

---

## Adversarial Review Summary

### Architect Position (confidence: 0.88)

The spec exhibits a **textbook layered dependency**: Naming and Checkpoint are foundation layers that TUI consumes. TUI never feeds back into Checkpoint. This one-directional dependency is the natural seam. The spec's own Section 6.2 implementation order validates this — infrastructure items form R1, presentation items form R2.

Key argument: R1 establishes the **data contract** (new enum values, checkpoint files on disk, new model fields). R2 builds the **presentation layer** that reads that contract. No dangerous intermediate states exist — the current TUI already renders PhaseStatus values via `.value` string fallback, so `PASS_MISSING_CHECKPOINT` would display as a plain string even before R2's styled rendering.

### Analyzer Position (confidence: 0.78)

Lower confidence because coordination costs are real, but the risk profile still favors splitting. The interleaved implementation order the spec recommends argues for monolithic delivery from a developer-efficiency perspective, but argues FOR splitting from a validation perspective. Splitting forces checkpoint logic to be validated in isolation before TUI touches the same file. A monolithic release means a TUI regression in executor.py could mask a checkpoint enforcement bug.

Key argument: R1 is not "we shipped something." It produces a pipeline with enforceable checkpoints that can be validated against real sprints before TUI complexity lands. Rollback granularity is critical — if SummaryWorker threading introduces a deadlock, rolling back a monolithic release also removes checkpoint enforcement.

### Key Contested Points

| Point | Architect | Analyzer | Resolution |
|-------|-----------|----------|------------|
| Interleaved order disruption | Dismisses — clean seam overrides dev convenience | Notes 1-2 hour context-loading cost | Accept the cost — validation integrity matters more |
| executor.py conflict strategy | Suggests structural placeholder comment | Suggests R2 branches from R1 merge commit | Both valid — use R2 branching from R1 merge AND clear integration markers |
| Confidence level | 0.88 (strong structural evidence) | 0.78 (structural agrees but coordination costs noted) | Merged: 0.83 |

### Verdict: SPLIT

Both agents agree unanimously on: (a) the split decision, (b) the scope assignment, (c) the seam rationale, (d) executor.py as the primary risk. Zero unresolved conflicts. The analyzer's lower confidence is driven by pragmatic cost concerns, not disagreement with the split architecture.

---

## Final Split Specification

### Release 1 — Pipeline Reliability & Naming (~480 LOC)

**Objective**: Make the sprint pipeline deterministically reliable and consistently named.

**Scope**:
1. **Naming Consolidation** (N1-N12, ~100 LOC, ~21 files)
   - Delete legacy deprecated command, rename task-unified.md to task.md
   - Rename sc-task-unified-protocol/ to sc-task-protocol/
   - Update Sprint CLI prompt, cleanup_audit prompts, protocol cross-references
   - `make sync-dev` propagation

2. **Checkpoint Enforcement Waves 1-3** (~380 LOC, 7 files)
   - **Wave 1** (T01.01-T01.02): Prompt-level checkpoint instructions + executor warning
   - **Wave 2** (T02.01-T02.05): checkpoints.py shared module, PASS_MISSING_CHECKPOINT enum, checkpoint_gate_mode config, post-phase gate (shadow mode), structured JSONL events, unit tests
   - **Wave 3** (T03.01-T03.06): CheckpointEntry dataclass, manifest build/write, auto-recovery from evidence, verify-checkpoints CLI subcommand, executor lifecycle integration, unit + integration tests

3. **Data Model (checkpoint domain only)**:
   - PhaseStatus.PASS_MISSING_CHECKPOINT enum value
   - SprintConfig.checkpoint_gate_mode field
   - CheckpointEntry dataclass
   - Gate progression: shadow (default) -> soft -> full

**What R1 does NOT include**:
- Any TUI rendering changes (F1-F10)
- MonitorState, PhaseResult, SprintResult additions for TUI
- summarizer.py, retrospective.py modules
- Tmux layout changes
- Checkpoint Wave 4 (deferred to next release cycle per original spec)

### Release 2 — Sprint TUI v2 (~800+ LOC)

**Objective**: Surface rich real-time telemetry from Claude's stream-json output into the sprint dashboard.

**Scope**:
1. **TUI Data Infrastructure** (Wave 1):
   - MonitorState: 8 new fields (activity_log, turns, errors, last_assistant_text, total_tasks_in_phase, completed_task_estimate, tokens_in, tokens_out)
   - PhaseResult: 3 new fields (turns, tokens_in, tokens_out)
   - SprintResult: 5 new aggregate properties
   - SprintConfig.total_tasks field
   - Monitor extraction updates for all new signal types

2. **TUI Rendering** (Wave 2):
   - F1: Activity stream (3-line FIFO)
   - F2: Enhanced phase table (Turns/Output columns)
   - F3: Dual progress bar (phase + task)
   - F4: Conditional error panel
   - F5: LLM context lines
   - F6: Enhanced terminal panels
   - F7: Sprint name in title

3. **Summary Infrastructure** (Wave 3):
   - F8: summarizer.py (PhaseSummary, PhaseSummarizer, SummaryWorker with threading.Lock)
   - F10: retrospective.py (ReleaseRetrospective, RetrospectiveGenerator)
   - Haiku narrative subprocess integration
   - Executor integration (SummaryWorker + RetrospectiveGenerator calls)

4. **Tmux Integration** (Wave 4):
   - F9: 3-pane layout (TUI 50% + summary 25% + tail 25%)
   - Summary pane management
   - --no-tmux fallback

5. **Checkpoint Display Integration**:
   - STATUS_STYLES dict entry for PASS_MISSING_CHECKPOINT
   - STATUS_ICONS dict entry for PASS_MISSING_CHECKPOINT
   - Appropriate yellow/amber styling

**Dependencies on R1**:
- PhaseStatus.PASS_MISSING_CHECKPOINT enum (must exist for display)
- Post-phase hook ordering (Section 6.4: _verify_checkpoints() THEN summary_worker.submit())
- executor.py state after R1 checkpoint changes (R2 branches from R1 merge commit)

**Planning Gate**:
> Release 2 roadmap/tasklist generation may proceed only after Release 1 has passed real-world validation and the results have been reviewed.

---

## Real-World Validation Plan for Release 1

1. **Sprint execution test**: Run `superclaude sprint run` against a real tasklist with checkpoint-bearing phases. Verify no regressions.
2. **Checkpoint W1**: Inspect NDJSON output for `## Checkpoints` section in the agent's prompt.
3. **Checkpoint W2**: After sprint, inspect JSONL events for `checkpoint_verification` entries. Verify expected/found/missing counts match reality.
4. **Checkpoint W3**: Run `superclaude sprint verify-checkpoints <dir>` against OntRAG R0+R1 output. Confirm it identifies the known Phase 3 gap. Run `--recover` and verify recovered checkpoint has `Auto-Recovered` header.
5. **Naming validation**: Execute `/sc:task` in a Claude Code session. Verify it resolves to the renamed command (not legacy). Verify sprint subprocess prompt contains `/sc:task`.
6. **Test suite**: `make test` passes with no regressions.

## Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| executor.py merge conflicts R1->R2 | Medium | R2 branches from R1 merge commit. R1 establishes clear hook-ordering structure per Section 6.4. |
| models.py additive collision | Low | All additions are new fields with defaults in different dataclasses. Clean merge. |
| Interleaved order disruption | Low | Accept ~1-2 hour context-loading overhead for validation integrity. |
| PASS_MISSING_CHECKPOINT display gap between R1 and R2 | Low | Current TUI falls back to `.value` string rendering. Functional, not pretty. |
| R2 delayed significantly | Low | Checkpoint enforcement works without TUI visibility. Operators use CLI verify-checkpoints. |
| Coordination overhead for single developer | Medium | Offset by reduced blast radius and cleaner rollback. |
