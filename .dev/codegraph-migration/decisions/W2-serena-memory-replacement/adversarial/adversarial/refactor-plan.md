# Refactoring Plan

## Overview
- Base variant: Variant 1 (Option A, `variant-1-original.md`), final score 0.6664
- Incorporated from: V2 advocate (concurrency and root-resolution amendments), V3 advocate (roadmap fallback, delete-not-port rule, test inventory), all three advocates (tracked reflect home), orchestrator probe (M-001 gitignore guard, M-005 empty store)
- Planned changes: 9
- Rejected alternatives documented: 6
- Overall risk: Medium (all changes add or tighten text; none change the base's core decision)
- Output of the merge: a decision recommendation document, `merged-recommendation.md`, one level above the `adversarial/` artifacts folder

## Planned Changes

### Change #1: Split storage into session state and tracked calibration
- Source: all three advocates (C-004, 92%); repo evidence E5, E6
- Target in base: last sentence of paragraph 1 ("Tracked `.serena/memories/reflect/deviation-patterns-IronClaude.md` moves to `.superclaude/memory/reflect/` (or docs/memory/ if it must be shared via git)")
- Integration approach: replace (resolves the open "or")
- Rationale: the calibration file is git-tracked today and shared across worktrees through git (E5). A gitignored home loses that. `docs/memory/` is already a tracked repo-scoped memory folder with `pm_context.md`, `last_session.md`, `next_actions.md` (E6)
- New text: session state and handoffs go to `<project>/.superclaude/memory/<name>.md` (ignored); the reflect cold-start calibration file `reflect/deviation-patterns-<slug>.md` goes to tracked `<project>/docs/memory/reflect/` (created on first write); existing `docs/memory/*.md` files stay untouched
- Risk: Medium (modifies an existing statement)

### Change #2: Resolve the project root once
- Source: V1 and V2 advocates (C-003, A-003)
- Target: new paragraph after the tool-mapping paragraph
- Integration approach: insert
- Rationale: sessions run in `.dev/worktrees/<name>/` (project CLAUDE.md), and the crash-recovery bootstrap resolves its own root. One rule avoids writing to the wrong folder
- New text: every primitive resolves `<project>` the same way, by the git top-level of the current directory (fall back to the current directory outside git). Default is one store per worktree. Sharing one store through the main checkout is an open decision (see Changes Not Being Made, item 5)
- Risk: Low (additive)

### Change #3: Remove, do not rename, the Serena-only calls
- Source: all three advocates (A-001, X-004); evidence E1, E9, E10
- Target: replaces the base claim "so prompts change by tool name only"
- Integration approach: replace
- Rationale: pm-agent uses `think_about_task_adherence`, `think_about_collected_information`, `think_about_whether_you_are_done`; save.md uses `summarize_changes`; sc-reflect Steps 0.7/0.7b use `activate_project`, `onboarding`, the empty-`list_memories` gate and `prepare_for_new_conversation`. These have no file-tool equivalent
- New text: memory tool calls are renamed; Serena-only calls are deleted or replaced by plain checks (for example "does `.superclaude/memory/memory_maintenance.md` exist" instead of the activation-message parse)
- Risk: Medium (changes the size estimate of the follow-on work)

### Change #4: Concurrent-writer convention
- Source: all three advocates (A-002)
- Target: new bullet in the pros/cons area
- Integration approach: insert
- New text: keys with one owner (`pm_context`, `last_session`, `next_actions`) are overwritten whole; keys that parallel sessions may write (`checkpoint`, `decision`, handoffs) use a `<key>-<session-or-timestamp>.md` name and are never edited in place
- Risk: Low

### Change #5: Guard the ignore rule outside this repo
- Source: orchestrator probe M-001 (HIGH, unaddressed by every variant)
- Target: the base statement "`.superclaude/` is already gitignored"
- Integration approach: restrict and append
- Rationale: `.gitignore:114` ignores `.superclaude/` only in IronClaude (E5). In other projects the folder would appear as untracked files
- New text: on first write, create `<project>/.superclaude/.gitignore` containing `*` if it does not exist
- Risk: Low

### Change #6: One-release legacy read fallback
- Source: V1 and V2 advocates (QUALIFY), V3 advocate (ACCEPT) (A-004)
- Target: the `/sc:load` sentence
- Integration approach: append
- New text: `/sc:load` reads `.serena/memories/<name>.md` when `.superclaude/memory/<name>.md` is absent, never writes there, and tells the user that the legacy folder is read-only history
- Risk: Low

### Change #7: Roadmap needs only a default flip
- Source: V3 advocate; verified in `sc-roadmap-protocol/SKILL.md` lines 326, 419, 443
- Target: new bullet in the consumers list
- Integration approach: insert
- New text: sc-roadmap already writes `<output_dir>/.session-memory.md` when Serena is unavailable; that path becomes the default and the "Serena unavailable" branches go away
- Risk: Low

### Change #8: Edit inventory for the follow-on work (A-005)
- Source: V3 advocate and the E2/E3 evidence
- Target: new section "Follow-on edit inventory"
- Integration approach: append
- Content: 14 files with 121 memory-tool hits under `src/superclaude` (E2); `src/superclaude/core/HOW-WE-WORK.md` lines 237, 327, 329 (and its byte-for-byte copy at `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` plus the level table in `core/CLAUDE.md`, per project CLAUDE.md); tests `tests/core/test_how_we_work_routing_table.py` lines 1074-1076, `tests/recommend/fixtures/routing_refresh_cases.json`, `tests/sc-roadmap/integration/test_wave5_completion.py` lines 69-78; `sc-crash-recovery` `scripts/bootstrap_scan.sh` lines 146-147 and `refs/investigators.md` section 3; `docs/mcp/*`, `docs/user-guide/session-management.md`; `/sc:save` and `/sc:load` command text. This is more than 5 edits across more than one source file, so the project rule requires a written plan (`/sc:workflow`, then `/sc:implement`); it is not a direct edit
- Risk: Low (documentation only)

### Change #9: Empty or missing store means "no memory"
- Source: orchestrator probe M-005 (replaces the `list_memories` empty gate)
- Target: new bullet
- Integration approach: insert
- New text: a missing `.superclaude/memory/` folder or an empty Glob result is the normal cold-start state, not an error; sc-reflect `--onboard` keys off the absence of `memory_maintenance.md`
- Risk: Low

## Changes NOT Being Made
1. Adopt Option B (native auto-memory) as the store. Rejected: C-001 (covers 3 of 14 consumer files), C-002 (85%: can be turned off with `autoMemoryEnabled` or `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, not an API for structured state, E7), C-006 (slug derivation in bash). Its worktree-sharing advantage is real (E7, X-001) but is covered by Change #1 for the one state that must be shared.
2. Mirror the memory index into auto-memory (V2 amendment). Rejected: harness-specific, adds a second store, outside the "smallest change" rule. Can be added later without changing the base.
3. Option C, delete `/sc:save`, `/sc:load` and the pm-agent lifecycle. Rejected: S-002 (70%), breaking removal, E3 test and routing churn is similar to editing; V3's own advocate conceded the reflect gap and the false "no gap" claim (X-002). Its useful parts were taken (Changes #3, #7, #8).
4. Put session state in the tracked `docs/memory/last_session.md` and `next_actions.md`. Rejected: tracked churn and merge conflicts between worktrees; those legacy files stay untouched.
5. Shared store through the main checkout by default (C-003, unresolved split). Not adopted: raises the concurrent-write risk (A-002) and is not needed once the calibration file is tracked. Left as an open decision for the owner.
6. Auto-load at session start (C-007, V2 won 62%). Not adopted: capped at 200 lines or 25KB and Claude Code only (E7); pm-agent keeps its explicit session-start read.

## Risk Summary
| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| #1 | Medium | Calibration file unreadable in projects without `docs/` | Create the folder on first write; revert to `.superclaude/memory/reflect/` |
| #2 | Low | Wrong root in a nested worktree | Edit the one shared rule |
| #3 | Medium | Edit count underestimated again | The inventory in #8 lists the files |
| #4 | Low | Extra file names | Rename convention |
| #5 | Low | Folder not ignored | Add the line manually |
| #6 | Low | Stale legacy data read | Drop the fallback after one release |
| #7 | Low | Roadmap resume wording | Revert text |
| #8 | Low | Missed file | `grep` for the old names before merge |
| #9 | Low | Reflect cold-start differs | Revert text |

## Review Status
Auto-approved (non-interactive run). Timestamp: 2026-10-30.
