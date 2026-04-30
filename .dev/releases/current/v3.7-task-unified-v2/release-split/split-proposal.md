# Split Proposal — v3.7 task-unified-v2

**Date**: 2026-04-02
**Source**: v3.7-UNIFIED-RELEASE-SPEC-merged.md
**Recommendation**: **SPLIT** (confidence: 0.82)

---

## Discovery Summary

v3.7 contains three feature domains totaling ~1,480+ LOC:

| Domain | LOC | Files | Risk Profile |
|--------|-----|-------|-------------|
| Checkpoint Enforcement (W1-W3) | ~380 | 7 (1 new, 6 mod) | Low — known patterns, shadow rollout |
| Sprint TUI v2 (W1-W4) | ~800+ | 7 (2 new, 5 mod) | Medium-High — threading, subprocess, tmux |
| Naming Consolidation | ~100 | ~21 | Low — mechanical rename |

Note: Checkpoint Wave 4 is already deferred to next release cycle per the spec.

## Recommendation: Split

### The Seam: "Fix the Pipeline" vs. "Show the Pipeline"

**Release 1 — Pipeline Reliability & Naming** (~480 LOC):
- Naming Consolidation (N1-N12): Clean naming, reduce diff noise
- Checkpoint Enforcement Waves 1-3: Prevention, detection, remediation
- Models changes for checkpoint domain only

**Release 2 — Sprint TUI v2** (~800+ LOC):
- All 10 TUI features (F1-F10) across 4 waves
- New modules: summarizer.py, retrospective.py
- Tmux 3-pane integration
- Depends on R1's `PASS_MISSING_CHECKPOINT` for display

### Why This Split Point

1. **Different risk profiles**: R1 is low-risk (string additions, enum values, shared module, CLI subcommand). R2 is medium-high risk (background threading, subprocess calls to Haiku, tmux pane management).

2. **Independent validation**: R1 can be validated by running real sprints and checking:
   - JSONL `checkpoint_verification` events emitted (Wave 2 shadow mode)
   - `verify-checkpoints` CLI works retroactively on OntRAG output (Wave 3)
   - `/sc:task` resolves correctly after naming migration
   - Sprint pipeline executes with no regressions

3. **R1 improves confidence in R2**: With checkpoint enforcement active, R2 development sprints themselves benefit from the enforcement. The TUI features built in R2 can display checkpoint data that R1 provides.

4. **Different blast radii**: If R1 has issues, rollback is mechanical (revert string changes, delete checkpoints.py). If R2 has issues (threading bugs, Haiku subprocess failures, tmux layout breaks), the blast radius is the entire UX layer.

5. **Time-to-value**: Checkpoint enforcement addresses a known production incident (OntRAG R0+R1 missing Phase 3 checkpoints). Every sprint between R1 and R2 benefits from enforcement.

### Release 1 Scope

| Item | Domain | Source |
|------|--------|--------|
| N1-N12 | Naming | Section 4.3 |
| T01.01-T01.02 | Checkpoint W1 | Section 4.1 Phase 1 |
| T02.01-T02.05 | Checkpoint W2 | Section 4.1 Phase 2 |
| T03.01-T03.06 | Checkpoint W3 | Section 4.1 Phase 3 |
| PASS_MISSING_CHECKPOINT enum | Checkpoint | Section 7.5 |
| CheckpointEntry dataclass | Checkpoint | Section 7.6 |
| checkpoint_gate_mode config | Checkpoint | Section 7.4 |
| checkpoints.py (new) | Checkpoint | Section 8.1 |
| verify-checkpoints CLI | Checkpoint | Section 13.3 |
| Gate progression rollout | Checkpoint | Section 9.2 |

**R1 LOC estimate**: ~480 (Checkpoint ~380 + Naming ~100)

### Release 2 Scope

| Item | Domain | Source |
|------|--------|--------|
| F1-F10 TUI features | TUI v2 | Section 4.2 |
| MonitorState 8 new fields | TUI v2 | Section 7.1 |
| PhaseResult 3 new fields | TUI v2 | Section 7.2 |
| SprintResult 5 properties | TUI v2 | Section 7.3 |
| SprintConfig.total_tasks | TUI v2 | Section 7.4 |
| summarizer.py (new) | TUI v2 | Section 3.2 |
| retrospective.py (new) | TUI v2 | Section 3.2 |
| Tmux 3-pane layout | TUI v2 | Section 4.2 Wave 4 |
| PASS_MISSING_CHECKPOINT display | TUI v2 + Checkpoint | Section 5.4 |
| STATUS_STYLES/STATUS_ICONS update | TUI v2 | Section 5.1 |

**R2 LOC estimate**: ~800+

### Real-World Test Plan for Release 1

1. **Naming validation**: Run `/sc:task` in Claude Code session, verify it resolves to the renamed command. Run `superclaude sprint run` on a test tasklist, verify subprocess prompt contains `/sc:task` (not `/sc:task-unified`).

2. **Checkpoint W1 validation**: Run a sprint with a tasklist containing `### Checkpoint:` sections. Verify the agent's prompt output (visible in NDJSON) contains `## Checkpoints` section.

3. **Checkpoint W2 validation**: After sprint, inspect JSONL events for `checkpoint_verification` entries. Verify expected/found/missing counts are accurate.

4. **Checkpoint W3 validation**: Run `superclaude sprint verify-checkpoints <dir>` against OntRAG R0+R1 output. Verify it identifies the known Phase 3 gap. Run with `--recover` and verify recovered checkpoint is generated with `Auto-Recovered` header.

5. **Regression check**: Full existing test suite passes (`make test`).

### Risks of the Split

| Risk | Severity | Mitigation |
|------|----------|------------|
| executor.py merge conflicts between R1 and R2 | Medium | R1 ships and stabilizes before R2 development begins. R2 builds on R1's executor state. |
| models.py field additions in two passes | Low | Fields are in different dataclasses. No collision. |
| TUI must handle PASS_MISSING_CHECKPOINT in R2 | Low | Trivial addition to two dicts (STATUS_STYLES, STATUS_ICONS). Well-documented in cross-domain dependency analysis. |
| Delayed TUI features | Low | TUI features are UX improvements, not critical fixes. Checkpoint enforcement is the urgent item. |

### Justification: R1 Is Not "Just Easy Work"

R1 is not splitting by effort or cherry-picking easy tasks. The checkpoint enforcement addresses a **known production failure** (triple failure chain from OntRAG R0+R1). The naming consolidation resolves a **systemic confusion** that affects every sprint execution and cross-protocol reference. Both produce independently measurable outcomes (checkpoint write rate, naming consistency) that directly improve R2 development quality.

### R1 Scope Bias

Per `--r1-scope` default (`fidelity-schema`): R1 focuses on planning fidelity (checkpoint enforcement ensures the pipeline produces reliable outputs) and schema hardening (CheckpointEntry, PASS_MISSING_CHECKPOINT, checkpoint_gate_mode establish the data contracts that R2 consumes).

### Smoke Gate Placement

Per `--smoke-gate` default (`r2`): Smoke gate belongs in Release 2. R1 validation is checkpoint-focused (JSONL events, CLI verify, sprint execution). R2 validation includes full TUI smoke testing (visual layout, threading behavior, Haiku subprocess, tmux integration).
