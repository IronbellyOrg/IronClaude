<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (Option A, original) -->
<!-- Merge date: 2026-10-30 -->
# Recommendation: replacement for Serena memory (Option A, amended)

Evidence labels E1-E10 refer to `diff-analysis.md` in the `adversarial/adversarial/` folder. Point IDs (C-, A-, X-, S-) refer to the same file and to `debate-transcript.md`.

## Decision
<!-- Source: Base (original, modified) - Change #3 replaces the claim "prompts change by tool name only" -->
Replace each Serena memory tool call with a native tool on `<project>/.superclaude/memory/<name>.md`: Write for write_memory, Read for read_memory, Glob for list_memories, Edit for edit_memory. The store keeps Serena's shape (flat markdown, topics as subfolders). `/sc:save` and `/sc:load` stay as commands; their descriptions say "file memory" instead of Serena. The crash-recovery investigator reads `.superclaude/memory/` instead of `.serena/memories/`.

- Pros: zero dependency, portable to every project and harness, offline, testable, works with only `~/.claude` primitives installed.
- Cons: per-project, not cross-project; no schema or index (list = Glob); one store per worktree by default (see Root rule and Open decision).
- Scope: this is a rewrite of the memory calls plus a deletion of the Serena-only calls, not a pure rename (see Removed, not renamed).

## Storage layout
<!-- Source: Base (original, modified) - Change #1 resolves the open "or" for the tracked reflect file; all three advocates (C-004, 92%) -->
- Session state and handoffs: `<project>/.superclaude/memory/<name>.md` (ignored by git).
- Reflect cold-start calibration: `reflect/deviation-patterns-<slug>.md` goes to the tracked folder `<project>/docs/memory/reflect/`, created on first write. Today the file is git-tracked at `.serena/memories/reflect/deviation-patterns-IronClaude.md` and shared across worktrees through git (E5); a gitignored home would lose that.
- Existing `docs/memory/*.md` files (`pm_context.md`, `last_session.md`, `next_actions.md`) stay untouched (E6).

## Rules
<!-- Source: Base (original, modified) - grouping heading for the rules added by Changes #2, #4, #5, #6, #9 -->

### Root
<!-- Source: Variant 1 / advocate and Variant 2 / advocate, Change #2 (C-003, A-003) -->
Every primitive resolves `<project>` the same way: the git top-level of the current directory, or the current directory outside git. Sessions run in `.dev/worktrees/<name>/`, so the default is one store per worktree. Sharing one store through the main checkout is not adopted (see Open decision).

### Concurrency
<!-- Source: Variant 1 / advocate, Variant 2 / advocate and Variant 3 / advocate, Change #4 (A-002) -->
Keys with one owner (`pm_context`, `last_session`, `next_actions`) are overwritten whole. Keys that parallel sessions may write (`checkpoint`, `decision`, handoffs) use the name `<key>-<session-or-timestamp>.md` and are never edited in place.

### Ignore guard
<!-- Source: Base (original, modified) - Change #5 restricts "`.superclaude/` is already gitignored" to this repo (orchestrator probe M-001) -->
`.gitignore:114` ignores `.superclaude/` only in IronClaude (E5). On first write in any project, create `<project>/.superclaude/.gitignore` containing `*` if it does not exist.

### Empty store
<!-- Source: Variant 1 / advocate, Change #9 (orchestrator probe M-005) -->
A missing `.superclaude/memory/` folder or an empty Glob result is the normal cold-start state, not an error. sc-reflect `--onboard` keys off the absence of `memory_maintenance.md`.

### Legacy fallback
<!-- Source: Base (original, modified) - Change #6 appends to the `/sc:load` sentence (A-004) -->
For one release, `/sc:load` reads `.serena/memories/<name>.md` when `.superclaude/memory/<name>.md` is absent. It never writes there and tells the user that the legacy folder is read-only history.

## Removed, not renamed
<!-- Source: Variant 1 / advocate, Variant 2 / advocate and Variant 3 / advocate, Change #3 (A-001, X-004) -->
Memory tool calls are renamed. Serena-only calls have no file-tool equivalent and are deleted or replaced by plain checks:
- pm-agent: `think_about_task_adherence`, `think_about_collected_information`, `think_about_whether_you_are_done` (E1).
- `save.md`: `summarize_changes` (E10).
- sc-reflect Steps 0.7 and 0.7b: `activate_project`, `onboarding`, the empty-`list_memories` gate and `prepare_for_new_conversation` (E9). Example plain check: "does `.superclaude/memory/memory_maintenance.md` exist" instead of parsing the activation message.

## Consumers
<!-- Source: Base (original, modified) - consumer list made explicit from E1, E2, E8, E10; roadmap row from Change #7 -->
| Consumer | What changes |
|---|---|
| `/sc:save`, `/sc:load` (`save.md`, `load.md`) | Memory calls go to the new store; `save.md` drops `summarize_changes`; `/sc:load` gets the legacy fallback |
| pm-agent (722 lines, 21 memory hits, E1) | Memory calls renamed; `think_about_*` calls deleted; session-start read stays explicit |
| sc-pm-protocol (12 hits), MODE_Task_Management (24 hits), sc-task-protocol (3 hits), sc-validate-roadmap-protocol (15 hits) | Memory calls renamed (E2) |
| sc-reflect-protocol (34 hits) | Steps 0.7/0.7b rewritten as plain checks; calibration file read from `docs/memory/reflect/` |
| sc-roadmap-protocol | Default flip only: it already writes `<output_dir>/.session-memory.md` when Serena is unavailable (`SKILL.md` lines 326, 419, 443). That path becomes the default and the "Serena unavailable" branches go away (Change #7, V3 / advocate) |
| sc-crash-recovery | Path swap: `scripts/bootstrap_scan.sh` lines 146-147, `refs/investigators.md` section 3, `SKILL.md` line 79 (E8) |

## Follow-on edit inventory
<!-- Source: Variant 3 / advocate, Change #8 (A-005; E2, E3) -->
- 14 files with 121 memory-tool hits under `src/superclaude` (E2).
- `src/superclaude/core/HOW-WE-WORK.md` lines 237, 327, 329; its byte-for-byte copy at `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; the level table in `core/CLAUDE.md` (per project CLAUDE.md).
- Tests: `tests/core/test_how_we_work_routing_table.py` lines 1074-1076; `tests/recommend/fixtures/routing_refresh_cases.json`; `tests/sc-roadmap/integration/test_wave5_completion.py` lines 69-78.
- `sc-crash-recovery`: `scripts/bootstrap_scan.sh` lines 146-147 and `refs/investigators.md` section 3.
- Docs: `docs/mcp/*`, `docs/user-guide/session-management.md`; `/sc:save` and `/sc:load` command text.
- This is more than 5 edits across more than one source file, so the project rule requires a written plan (`/sc:workflow`, then `/sc:implement`). It is not a direct edit.

## Rejected alternatives
<!-- Source: Variant 2 / advocate and Variant 3 / advocate, Changes Not Being Made items 1-6 of the refactoring plan -->
1. Option B (native auto-memory) as the store. Rejected: C-001 (covers 3 of 14 consumer files), C-002 (85%: can be turned off, not an API for structured state, E7), C-006 (slug derivation in bash). Its worktree-sharing advantage is real (E7, X-001) and is covered by the tracked calibration file.
2. Mirror the memory index into auto-memory (V2 amendment). Rejected: harness-specific, adds a second store, outside the smallest-change rule. Can be added later without changing this design.
3. Option C, delete `/sc:save`, `/sc:load` and the pm-agent lifecycle. Rejected: S-002 (70%), breaking removal, test and routing churn is similar to editing; V3's advocate conceded the reflect gap and the false "no gap" claim (X-002). Its useful parts were taken (Removed, not renamed; roadmap default flip; edit inventory).
4. Session state in the tracked `docs/memory/last_session.md` and `next_actions.md`. Rejected: tracked churn and merge conflicts between worktrees; those files stay untouched.
5. Shared store through the main checkout by default (C-003). Not adopted: raises the concurrent-write risk (A-002) and is not needed once the calibration file is tracked. See Open decision.
6. Auto-load at session start (C-007, V2 won 62%). Not adopted: capped at 200 lines or 25KB and Claude Code only (E7); pm-agent keeps its explicit session-start read.

## Open decision
<!-- Source: Variant 2 / advocate, Change #2 and Changes Not Being Made item 5 (C-003, unresolved split) -->
Whether all worktrees of a repo should share one store through the main checkout. The default above is one store per worktree. Left as an open decision for the owner.

## Debate result
<!-- Source: Base (original, modified) - result block from base-selection.md and debate-transcript.md -->
- Base scores: Option A 0.6664, Option C 0.6540, Option B 0.5825. Option A won the level 1 tiebreak (9 points to 1 for C) because the margin of 0.0124 was inside the 5% band.
- Convergence: 89.5% (17 of 19 diff points), threshold 80%.
- Unresolved: S-001 (storage location, three-way split) and C-003 (cross-worktree sharing).
- Depth was quick: Rounds 2, 2.5 and 3 were skipped.
