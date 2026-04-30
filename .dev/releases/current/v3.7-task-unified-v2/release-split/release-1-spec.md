---
release: 1
parent-spec: .dev/releases/backlog/v3.7-task-unified-v2/v3.7-UNIFIED-RELEASE-SPEC-merged.md
split-proposal: .dev/releases/backlog/v3.7-task-unified-v2/release-split/split-proposal-final.md
scope: Pipeline Reliability & Naming — Checkpoint enforcement (Waves 1-3) + naming consolidation
status: draft
---

# Release 1 — v3.7a Pipeline Reliability & Naming

## Objective

Make the Sprint CLI pipeline deterministically reliable by implementing three-layer checkpoint enforcement (Prevention, Detection, Remediation) and resolving the three-layer naming collision. Every sprint run after this release will have enforced checkpoint verification (initially in shadow mode), and all command/protocol references will use canonical names.

## Scope

### Included

#### Naming Consolidation (~100 LOC, ~21 files)

1. **N1** — Delete legacy deprecated command (`task.md` with `deprecated: true`)
   From: [parent-spec] Section 4.3, Task N1
2. **N2** — Rename `task-unified.md` to `task.md`, verify frontmatter `name: task` unchanged
   From: [parent-spec] Section 4.3, Task N2
3. **N3** — Rename skill directory `sc-task-unified-protocol/` to `sc-task-protocol/`
   From: [parent-spec] Section 4.3, Task N3
4. **N4** — Update skill frontmatter name to `sc:task-protocol`
   From: [parent-spec] Section 4.3, Task N4
5. **N5** — Update Sprint CLI prompt in `process.py:170` (`/sc:task-unified` -> `/sc:task`)
   From: [parent-spec] Section 4.3, Task N5
6. **N6** — Update 5 prompt builders in `cleanup_audit/prompts.py`
   From: [parent-spec] Section 4.3, Task N6
7. **N7** — Update 12 references in `sc-tasklist-protocol/SKILL.md`
   From: [parent-spec] Section 4.3, Task N7
8. **N8** — Update command cross-references (`tasklist.md`, `help.md`, others)
   From: [parent-spec] Section 4.3, Task N8
9. **N9** — Update other protocol cross-refs (`sc-roadmap-protocol`, `sc-cli-portify-protocol`, `sc-validate-tests-protocol`, `sc-release-split-protocol`)
   From: [parent-spec] Section 4.3, Task N9
10. **N10** — Update core docs (`COMMANDS.md`, `ORCHESTRATOR.md`)
    From: [parent-spec] Section 4.3, Task N10
11. **N11** — Run `make sync-dev` to propagate to `.claude/`
    From: [parent-spec] Section 4.3, Task N11
12. **N12** — Confirm `task-mcp.md` deprecated status, clean up or remove
    From: [parent-spec] Section 4.3, Task N12

**Dependency order**: N1 -> N2 -> N3 -> N4 -> N5+N6 (parallel) -> N7+N8+N9+N10 (parallel) -> N11

#### Checkpoint Enforcement Wave 1 — Prompt-Level (~60 LOC, 2 files)

13. **T01.01** — Add `## Checkpoints` section to `build_prompt()` in `process.py`
    From: [parent-spec] Section 4.1 Phase 1, Task T01.01
14. **T01.02** — Add `_warn_missing_checkpoints()` helper to `executor.py`
    From: [parent-spec] Section 4.1 Phase 1, Task T01.02

#### Checkpoint Enforcement Wave 2 — Post-Phase Gate (~120 LOC, 4 files)

15. **T02.01** — Create `checkpoints.py` with `extract_checkpoint_paths()` and `verify_checkpoint_files()`
    From: [parent-spec] Section 4.1 Phase 2, Task T02.01
16. **T02.02** — Add `PASS_MISSING_CHECKPOINT` to `PhaseStatus` enum, `checkpoint_gate_mode` to `SprintConfig`
    From: [parent-spec] Section 4.1 Phase 2, Task T02.02
17. **T02.03** — Add `write_checkpoint_verification()` to `logging_.py`
    From: [parent-spec] Section 4.1 Phase 2, Task T02.03
18. **T02.04** — Wire `_verify_checkpoints()` into `executor.py` phase completion flow
    From: [parent-spec] Section 4.1 Phase 2, Task T02.04
19. **T02.05** — Unit tests for `checkpoints.py` and `PASS_MISSING_CHECKPOINT` integration
    From: [parent-spec] Section 4.1 Phase 2, Task T02.05

#### Checkpoint Enforcement Wave 3 — Manifest, CLI & Auto-Recovery (~200 LOC, 4 files)

20. **T03.01** — Add `CheckpointEntry` dataclass to `models.py`
    From: [parent-spec] Section 4.1 Phase 3, Task T03.01
21. **T03.02** — Extend `checkpoints.py` with `build_manifest()` and `write_manifest()`
    From: [parent-spec] Section 4.1 Phase 3, Task T03.02
22. **T03.03** — Add `recover_missing_checkpoints()` to `checkpoints.py`
    From: [parent-spec] Section 4.1 Phase 3, Task T03.03
23. **T03.04** — Add `verify-checkpoints` CLI subcommand to `commands.py`
    From: [parent-spec] Section 4.1 Phase 3, Task T03.04
24. **T03.05** — Wire manifest build/verify into `executor.py` sprint lifecycle
    From: [parent-spec] Section 4.1 Phase 3, Task T03.05
25. **T03.06** — Unit + integration tests for manifest, recovery, and CLI
    From: [parent-spec] Section 4.1 Phase 3, Task T03.06

#### Data Model Changes (checkpoint domain)

26. **PhaseStatus.PASS_MISSING_CHECKPOINT** enum value (`is_failure` = False)
    From: [parent-spec] Section 7.5
27. **SprintConfig.checkpoint_gate_mode** field (default: `"shadow"`)
    From: [parent-spec] Section 7.4
28. **CheckpointEntry** dataclass (phase, name, expected_path, exists, recovered, recovery_source)
    From: [parent-spec] Section 7.6

#### Configuration Changes

29. **Gate mode behavior**: off/shadow/soft/full progression
    From: [parent-spec] Section 9.2, Section 13.2
30. **CLI subcommand**: `superclaude sprint verify-checkpoints <dir>` with `--recover` and `--json`
    From: [parent-spec] Section 13.3

### Excluded (assigned to Release 2)

1. **TUI Features F1-F10** — All rendering, display, and UX changes
   Deferred to: Release 2, TUI v2 scope
2. **MonitorState new fields** (8 fields: activity_log, turns, errors, etc.)
   Deferred to: Release 2, Data Model scope
3. **PhaseResult new fields** (turns, tokens_in, tokens_out)
   Deferred to: Release 2, Data Model scope
4. **SprintResult new properties** (total_turns, total_tokens_in, etc.)
   Deferred to: Release 2, Data Model scope
5. **SprintConfig.total_tasks** field
   Deferred to: Release 2, Data Model scope
6. **summarizer.py** module (PhaseSummary, PhaseSummarizer, SummaryWorker)
   Deferred to: Release 2, Summary Infrastructure scope
7. **retrospective.py** module (ReleaseRetrospective, RetrospectiveGenerator)
   Deferred to: Release 2, Summary Infrastructure scope
8. **Tmux 3-pane layout** changes
   Deferred to: Release 2, Tmux Integration scope
9. **Checkpoint Wave 4** — Tasklist-level checkpoint normalization (T04.01-T04.03)
   Deferred to: Next release cycle (per original spec — breaking change)

## Dependencies

### Prerequisites

None — this is the first release in the split sequence.

### External Dependencies

- Python >=3.10, UV for execution
- `make sync-dev` for component propagation
- Existing test infrastructure (`uv run pytest`)

### Intra-Release Ordering Constraints

**Naming must complete before Checkpoint Wave 1**: Both modify `process.py`. Naming changes the prompt string (`/sc:task-unified` -> `/sc:task`); Wave 1 adds the `## Checkpoints` section to the same function. Naming first reduces merge friction.

**Checkpoint waves are sequential**:
- Wave 1 must be code-complete before Wave 2 begins (Wave 2's `_verify_checkpoints()` replaces Wave 1's `_warn_missing_checkpoints()`)
- Wave 2 must be code-complete before Wave 3 begins (Wave 3 extends `checkpoints.py` created in Wave 2)

From: [parent-spec] Section 4.1, wave dependencies; Section 5.2, naming-checkpoint interaction

## Real-World Validation Requirements

1. **Sprint execution**: Run `superclaude sprint run` against a real tasklist with checkpoint-bearing phases. Verify sprint completes with no regressions.

2. **Checkpoint W1 validation**: Inspect the NDJSON stream output for a running phase. The agent prompt must contain a `## Checkpoints` section with 5 instruction lines. Verify at least one phase agent writes checkpoint files voluntarily (improved from emergent to instructed).

3. **Checkpoint W2 validation**: After a sprint completes, inspect the JSONL event log for `checkpoint_verification` events. Each phase with `Checkpoint Report Path:` sections must have a corresponding event with accurate expected/found/missing counts.

4. **Checkpoint W3 validation**: Run `superclaude sprint verify-checkpoints` against the OntRAG R0+R1 sprint output directory. Verify it identifies the known Phase 3 checkpoint gap (CP-P03-T01-T05 and CP-P03-END missing). Run with `--recover` and verify recovered checkpoint files are generated with `## Note: Auto-Recovered` header and `recovered: true` frontmatter.

5. **Naming validation**: In a fresh Claude Code session, execute `/sc:task`. Verify it resolves to the renamed command file (not legacy). Run `superclaude sprint run` and verify the subprocess prompt contains `/sc:task` (not `/sc:task-unified`). Grep `src/superclaude/` for any remaining `sc:task-unified` references — expect zero.

6. **Gate progression test**: Set `checkpoint_gate_mode` to `"full"` and run a sprint where a phase has checkpoint sections. If the agent fails to write checkpoints, verify the phase status is downgraded to `PASS_MISSING_CHECKPOINT` (not PASS).

7. **Test suite**: `make test` passes. `make lint` passes. `make verify-sync` passes.

## Success Criteria

| Metric | Current | Target |
|--------|---------|--------|
| Checkpoint write rate | 86% (6/7 phases) | 100% (all phases with checkpoints) |
| False positive rate in gate | N/A | 0% over 2 sprint cycles |
| Time to detect missing checkpoint | ~24 hours (manual) | <1 second (automated gate) |
| Time to recover missing checkpoint | ~30 minutes (manual) | <5 seconds (CLI --recover) |
| Root causes addressed | 0/3 | 3/3 (Cause 1: W1, Cause 2: future W4, Cause 3: W2+W3) |
| Naming variants in live source | 3 (task, task-unified, task-unified-protocol) | 2 (task, task-protocol) |
| Deprecated files in command surface | 2 | 0 |

From: [parent-spec] Section 11.1, Section 11.3

## File Inventory

### Checkpoint Enforcement Files

| File | Wave(s) | Action | Purpose |
|------|---------|--------|---------|
| `src/superclaude/cli/sprint/process.py` | 1 | MODIFY | Checkpoint instructions in build_prompt() |
| `src/superclaude/cli/sprint/executor.py` | 1, 2, 3 | MODIFY | Warning, gate, manifest integration |
| `src/superclaude/cli/sprint/checkpoints.py` | 2, 3 | CREATE | Shared path extraction, manifest, recovery |
| `src/superclaude/cli/sprint/models.py` | 2, 3 | MODIFY | PASS_MISSING_CHECKPOINT, checkpoint_gate_mode, CheckpointEntry |
| `src/superclaude/cli/sprint/logging_.py` | 2 | MODIFY | checkpoint_verification JSONL event |
| `src/superclaude/cli/sprint/commands.py` | 3 | MODIFY | verify-checkpoints subcommand |

### Naming Consolidation Files

| File | Action | Change |
|------|--------|--------|
| `src/superclaude/commands/task-unified.md` | RENAME | -> task.md |
| `src/superclaude/commands/task.md` (legacy) | DELETE | Remove deprecated |
| `.claude/commands/sc/task.md` (legacy) | DELETE | Remove deprecated dev copy |
| `src/superclaude/skills/sc-task-unified-protocol/` | RENAME | -> sc-task-protocol/ |
| `src/superclaude/skills/sc-task-protocol/SKILL.md` | MODIFY | Frontmatter name |
| `src/superclaude/cli/sprint/process.py` | MODIFY | Prompt string |
| `src/superclaude/cli/cleanup_audit/prompts.py` | MODIFY | 5 prompt builders |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | MODIFY | 12 references |
| `src/superclaude/commands/tasklist.md` | MODIFY | 8 references |
| `src/superclaude/commands/help.md` | MODIFY | 2 references |
| 10+ additional files | MODIFY | 1-4 references each |

### Test Files

| File | Action | Scope |
|------|--------|-------|
| `tests/sprint/test_checkpoints.py` | CREATE | checkpoints.py unit tests |
| `tests/sprint/test_commands.py` | MODIFY | verify-checkpoints integration test |

## Rollout Strategy

```
Day 1:     Naming consolidation (mechanical rename + sync)
           Checkpoint Wave 1 deployed (prompt fix + executor warning)

Day 2-5:   Checkpoint Wave 2 deployed (gate in shadow mode)
           Per-phase verification JSONL logging begins

Day 5-10:  Checkpoint Wave 3 deployed (manifest + CLI + auto-recovery)
           Run retroactively on OntRAG R0+R1 output

Day 10+:   Promote gate from shadow -> soft (after 0 false positives)
```

From: [parent-spec] Section 9.1 (Days 1-10 subset)

## Backward Compatibility

| Domain | Guarantee |
|--------|-----------|
| Checkpoint Waves 1-3 | Fully backward compatible. Shadow default means no behavioral change. |
| Naming | Breaking change for code referencing `/sc:task-unified` directly. Sprint CLI and cleanup_audit updated as part of migration. |

From: [parent-spec] Section 9.3

## Risk Register

| # | Risk | Severity | Likelihood | Mitigation |
|---|------|----------|------------|------------|
| CE-1 | Agent ignores prompt instructions | Medium | Low | Waves 2+3 detect and remediate |
| CE-2 | Path resolution false positives | Medium | Medium | Shadow mode prevents impact |
| CE-4 | Auto-recovery quality | Low | Medium | Auto-Recovered header distinguishes |
| CE-6 | Context pressure skips instructions | Medium | Low | Wave 2 gate catches |
| CE-7 | Downstream consumers break on new enum | Low | Low | Grep for exhaustive matches |
| NC-1 | Missing reference in obscure file | Medium | Medium | Comprehensive grep + test sprint |
| NC-2 | Command resolution ambiguity | Medium | Low | Test resolution after rename |
| NC-4 | task-mcp.md not cleaned up | Low | Medium | Explicitly confirm and remove |

From: [parent-spec] Section 10.1, Section 10.3

## Open Questions (carried from parent spec)

| # | Question | Priority |
|---|----------|----------|
| CE-Q2 | Cross-wave rollback dependencies | Medium |
| CE-Q3 | Context pressure mitigation | Low |
| CE-Q4 | Mid-phase checkpoint gate timing | Medium |
| CE-Q6 | _check_checkpoint_pass() consolidation | Low |
| CE-Q7 | Manifest schema version | Low |
| NC-Q1 | Command resolution order | Medium |
| NC-Q2 | task-mcp.md status | Low |
| NC-Q3 | Classification header stability | Low |
| NC-Q4 | Subprocess resolution | Medium |
| NC-Q5 | .claude/commands/sc/ sync state | Low |

From: [parent-spec] Section 14.1, Section 14.3

## Traceability

| Release 1 Item | Parent Spec Section |
|----------------|-------------------|
| N1-N12 | Section 4.3 |
| T01.01-T01.02 | Section 4.1 Phase 1 |
| T02.01-T02.05 | Section 4.1 Phase 2 |
| T03.01-T03.06 | Section 4.1 Phase 3 |
| PhaseStatus.PASS_MISSING_CHECKPOINT | Section 7.5 |
| SprintConfig.checkpoint_gate_mode | Section 7.4 |
| CheckpointEntry dataclass | Section 7.6 |
| Gate progression | Section 9.2 |
| verify-checkpoints CLI | Section 13.3 |
| Checkpoint risks CE-1 through CE-7 | Section 10.1 |
| Naming risks NC-1 through NC-4 | Section 10.3 |
| Checkpoint metrics | Section 11.1 |
| Naming metrics | Section 11.3 |
| Checkpoint tests | Section 12.1-12.5 |
| Checkpoint open questions | Section 14.1 |
| Naming open questions | Section 14.3 |
