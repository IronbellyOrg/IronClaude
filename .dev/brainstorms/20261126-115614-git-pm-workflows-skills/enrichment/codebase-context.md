# Codebase context (Wave 2A, quality_tier: primary)

Source: two `mcp__litellm__augment_code-augment_code_search` queries on `IronbellyOrg/IronClaude`, branch `integration`, plus the prior deep read in `.dev/issues/326/analysis/analyze-git.md`.

## What the scan found

- `/sc:git` exists in four places: `src/superclaude/commands/git.md` (source, 91 lines), `plugins/superclaude/commands/git.md` (identical), `.claude/commands/sc/git.md` (gitignored dev copy) and `commands/sc-git.md` (tracked legacy copy with the doubled prefix `/sc:sc:sc:git`, usage `/sc:sc:git`). Front matter: `category: utility`, `complexity: basic`, no `mcp-servers`, no `personas`, no `argument-hint`. Usage line: `/sc:git [operation] [args] [--smart-commit] [--interactive]`. Sections: Triggers, Usage, Behavioral Flow (5 steps), Tool Coordination, Key Patterns, Examples, Boundaries.
- Newer commands show the structure the developer guide expects: `/sc:implement` (`src/superclaude/commands/implement.md`) has `argument-hint`, a Required Input section with a STOP line, Behavioral Flow limited to parse, STOP, hand off, print; an `## Activation` section that names `Skill sc:implement-protocol`; Codegraph and Boundaries sections. `/sc:brainstorm` and `/sc:issue` add an Options table, STOP rules and an `## Unattended mode` section.
- Command plus protocol skill pattern: skill at `src/superclaude/skills/sc-<name>-protocol/SKILL.md` with `refs/` loaded on demand (`sc-implement-protocol`: `refs/qa.md`, `refs/ledger.md`, `refs/retry.md`, `refs/managed-workspace.md`; `sc-issue-protocol`: `refs/claim.md`, `refs/create.md`, `refs/chains.md`, `scripts/`, `templates/`). There is no `sc-git-protocol` skill today.
- `/sc:implement` loop (Q0-Q8): Q0 snapshots HEAD plus tracked diffs plus untracked files into a tree object through a temporary index `GIT_INDEX_FILE` without staging in the user's index, and pins it as `refs/superclaude/implement/<slug>/T<id>`; on task `complete` the pin is deleted and a `complete` line goes to the ledger (`progress.md` for managed packages). The retry rules need HEAD unchanged during a task. So a commit step belongs after the `complete` line and before the next Q0.
- `/sc:pr-submit` (`sc-pr-submit-protocol`) owns push, PR creation, draft hold (`refs/merge-guard.md`) and submodule handling in `finish-merge.sh`; `src/superclaude/pr_submit/conflicts.py` holds submodule conflict handling.
- Worker contract: `src/superclaude/core/WORKER-CONTRACT.md` fixes the `--unattended` rules, the never-as-worker list (includes `/sc:git`), and says `artifacts` leave out git-ignored paths because every listed path is staged.
- Worktree cleanup (PR 711): `scripts/worktree_cleanup.py`, tests in `tests/worktree_cleanup/` (`test_removal.py` asserts no `--force`, no `-D`, no `--delete`, push only to the evidence repo). Allowed `git branch` forms: `--show-current`, `--list <name>`, `-d <name>`.

## Integration points for the work

1. Edit `src/superclaude/commands/git.md` (and a new `src/superclaude/skills/sc-git-protocol/` if the design adds one), then `make sync-dev`, `make verify-sync`, and the plugin mirror `plugins/superclaude/`.
2. Between-task commit hook: `src/superclaude/skills/sc-implement-protocol/SKILL.md` loop and `refs/ledger.md` / `refs/managed-workspace.md`; `src/superclaude/commands/implement.md` Boundaries ("Auto-commit, open PRs, or release" Will Not).
3. Authorization wording: `src/superclaude/core/HOW-WE-WORK.md` routing row for `/sc:git`; `src/superclaude/core/WORKER-CONTRACT.md` lines on `/sc:git` and per-task commits (K3).
4. Branch cleanup: reuse `scripts/worktree_cleanup.py` and `src/superclaude/commands/worktrees.md`; add no remote deletion.
5. Standards to align with: `docs/developer-guide/git-standards-protocols.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, `docs/developer-guide/branch-protection.md`.
6. Tests: new tests under `tests/` for authorization, commit timing and staged paths; check `tests/skills/test_primitive_dual_surface_lookup.py` and the installed-path rule (no `src/superclaude/...` path inside an installed primitive).
