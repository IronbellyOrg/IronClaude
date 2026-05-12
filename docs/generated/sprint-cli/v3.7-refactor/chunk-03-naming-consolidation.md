---
title: "Chunk 3: Naming Consolidation — Path A/B Refactoring Analysis"
chunk: naming-consolidation
spec_sections: "3.3, 4.3"
generated: 2026-04-03
---

# Naming Consolidation — Refactoring Analysis

## Executive Summary

The naming consolidation (N1-N12) is almost entirely a mechanical rename that affects file/directory names, frontmatter, cross-references, and two hardcoded prompt strings. Of the 12 tasks, only N5 touches a runtime prompt (Path B at `process.py:170`). Path A at `executor.py:1064-1068` is unaffected by the rename because it does not invoke any skill command at all. The naming consolidation should NOT be the vehicle for wiring `/sc:task` into Path A -- that is a separate, higher-stakes change that belongs in the Path A Enrichment chunk.

## The Central Question: Should Path A Invoke /sc:task?

### The Architectural Divide

Path B's prompt at `process.py:170` begins with `/sc:task-unified Execute all tasks in @{phase_file}`. This invocation activates a full skill protocol: compliance classification, tier-aware execution strategy, checkpoint instructions, result file contracts, and stop-on-STRICT-fail behavior. The entire prompt is structured around the skill's behavioral contract.

Path A's prompt at `executor.py:1064-1068` is three lines of plain English: task ID, phase file path, description. It deliberately avoids protocol activation. The subprocess receives a single task and relies on subprocess isolation rather than prompt-level control flow.

### Arguments FOR Wiring /sc:task into Path A

1. **Consistency**: Both paths would use the same skill protocol, ensuring identical task execution semantics regardless of which path fires.
2. **Tier awareness**: The `/sc:task` protocol includes compliance classification (`STRICT`, `STANDARD`, `LIGHT`, `EXEMPT`) that influences execution depth. Path A workers currently have no tier-aware behavior.
3. **Quality signal**: The skill protocol includes validation steps and structured output that the orchestrator could eventually parse.

### Arguments AGAINST Wiring /sc:task into Path A

1. **Protocol mismatch**: `/sc:task` (nee `/sc:task-unified`) is designed for multi-task execution within a single subprocess. Its instructions say "Execute tasks in order", "If a STRICT-tier task fails, STOP and report -- do not continue to next task." These multi-task flow-control semantics are meaningless when the subprocess receives exactly one task. The debate rulings explicitly rejected stop-on-STRICT-fail for Path A (Ruling 5, AGAINST 0.795 vs FOR 0.64).
2. **Result file contract redundancy**: The skill protocol instructs the worker to write `EXIT_RECOMMENDATION: CONTINUE` or `HALT`. The debate rulings explicitly rejected result file contracts for Path A (Ruling 3, AGAINST won 4-3). Post-task hooks and exit codes are the intended signal mechanism.
3. **Token cost**: Skill invocation loads the full SKILL.md protocol (~2,000-4,000 tokens per subprocess). Across 10+ tasks per phase, that is 20,000-40,000 tokens of protocol overhead for instructions that are architecturally unnecessary due to subprocess isolation.
4. **Scope contamination risk**: The skill protocol includes instructions about reading the full phase file, which the debate rulings explicitly cautioned against (Ruling 1: extract task block, do NOT preload full file).
5. **The debates already answered this**: The three components that SHOULD go into Path A (per-task block extraction, scope boundary, sprint context) were identified as ~280 tokens of targeted prompt enrichment. This is fundamentally different from loading a multi-thousand-token skill protocol.

### Verdict

**Path A should NOT invoke `/sc:task`.** The skill protocol was designed for Path B's single-subprocess-executes-all-tasks architecture. Its flow-control semantics (ordered execution, halt-on-STRICT, result file) are either redundant or counterproductive in Path A's subprocess-per-task architecture. The debate rulings validated three specific, lightweight prompt enrichments for Path A that achieve the same quality goals without protocol overhead. Wiring `/sc:task` into Path A would be force-fitting a Path B pattern onto a fundamentally different execution model, violating Principle 2 from the gap analysis.

The correct vehicle for Path A improvements is the Path A Enrichment chunk (not in the current spec), not the naming consolidation.

## Per-Task Analysis

### N1 -- Delete legacy deprecated command
- **Path affected**: Neither (file deletion only)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Deletes `.claude/commands/sc/task.md` and `src/superclaude/commands/task.md` (the old deprecated stub). This is pure housekeeping. Neither Path A nor Path B references these files at runtime; they are command definitions loaded by Claude Code's command registry. No path-specific concerns.

### N2 -- Rename unified command file
- **Path affected**: Neither (file rename only)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Renames `src/superclaude/commands/task-unified.md` to `task.md`. The command definition file is read by Claude Code's command dispatcher, not by either execution path's Python code. The frontmatter `name: task` is already correct. No runtime impact on either path.

### N3 -- Rename skill directory
- **Path affected**: Neither (filesystem rename only)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Renames `src/superclaude/skills/sc-task-unified-protocol/` to `sc-task-protocol/`. Skill directories are resolved by Claude Code's skill loader at session start, not by the sprint executor. Neither path has hardcoded skill directory paths.

### N4 -- Update skill frontmatter
- **Path affected**: Neither (metadata only)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Changes `name: sc:task-unified-protocol` to `name: sc:task-protocol` in the SKILL.md frontmatter. This affects Claude Code's skill registry. Neither path references the skill's internal name in Python code.

### N5 -- Update Sprint CLI prompt
- **Path affected**: Path B only
- **Recommendation**: KEEP AS-IS
- **Rationale**: Changes `/sc:task-unified` to `/sc:task` at `process.py:170`. This is the only task that touches a runtime prompt, and it targets Path B exclusively. Path A at `executor.py:1064-1068` does not contain any `/sc:task-unified` string to rename. No extension needed.

### N6 -- Update cleanup_audit prompts
- **Path affected**: Neither A nor B (separate CLI tool)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Updates 5 prompt builders in `src/superclaude/cli/cleanup_audit/prompts.py`. The cleanup audit is a separate CLI pipeline (`superclaude cleanup-audit`), not part of the sprint executor. No path applicability.

### N7 -- Update tasklist protocol
- **Path affected**: Neither (skill documentation)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Updates 12 references in `sc-tasklist-protocol/SKILL.md`. This is a skill specification document read by Claude Code's inference layer. It influences how tasklists are generated, not how they are executed. Neither path references this file.

### N8 -- Update command cross-references
- **Path affected**: Neither (command documentation)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Updates references in `tasklist.md` (8), `help.md` (2), and other command files. These are command definitions and help text. No runtime path impact.

### N9 -- Update other protocol cross-refs
- **Path affected**: Neither (skill documentation)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Updates references in `sc-roadmap-protocol`, `sc-cli-portify-protocol`, `sc-validate-tests-protocol`, `sc-release-split-protocol`. All are skill specification documents. No runtime path impact.

### N10 -- Update core docs
- **Path affected**: Neither (documentation)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Updates `COMMANDS.md` and `ORCHESTRATOR.md`. Pure documentation. No runtime impact.

### N11 -- Sync dev copies
- **Path affected**: Both (indirectly, via `.claude/` sync)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Runs `make sync-dev` to propagate `src/superclaude/` changes to `.claude/`. This is a build step that applies to all prior N-tasks. It does not itself modify either path's behavior; it ensures the dev copies match source-of-truth.

### N12 -- Confirm task-mcp.md status
- **Path affected**: Neither (command file audit)
- **Recommendation**: KEEP AS-IS
- **Rationale**: Audits `src/superclaude/commands/task-mcp.md` for deprecated status. `task-mcp` is a separate command variant for MCP-enforced execution. It has no relationship to the Path A/B branching in the sprint executor.

## New Task Recommendation

**No N13 is recommended for the naming consolidation.**

The naming consolidation is a self-contained rename operation. Its scope is correct: rename all references from `task-unified` to `task` across the codebase. Adding Path A skill invocation would violate the task's own execution strategy ("mechanical search-and-replace with dependency ordering") by introducing a behavioral change that requires architectural analysis.

The question of enriching Path A's prompt belongs in a separate chunk -- the **Path A Enrichment** chunk identified in context-03 (Gap 1). That chunk should address:

1. Per-task markdown block extraction (~150 tokens avg, from debate Ruling 1)
2. Scope boundary injection (~50 tokens, from debate Ruling 2)
3. Sprint context header (~80 tokens, from debate Ruling 4)

These three enrichments provide the quality improvements that Path A needs without the protocol overhead of `/sc:task` invocation. They should be specified as new tasks (e.g., A1-A3) in the Path A Enrichment chunk, not grafted onto the naming consolidation.

## Net Changes to Spec

**Zero changes to the naming consolidation tasks (N1-N12).** All 12 tasks are correctly scoped as mechanical renames that primarily affect Path B's prompt and cross-cutting documentation. No task requires extension to address Path A.

**One clarifying note to add to Section 4.3:** After the dependency order line, add:

> **Path A note:** These tasks do not modify `executor.py:1064-1068` (Path A's per-task prompt). Path A does not invoke `/sc:task-unified` and therefore has no string to rename. Enrichment of Path A's prompt is addressed separately in the Path A Enrichment chunk.

This prevents future implementors from wondering whether N5 was supposed to also update `executor.py`.
