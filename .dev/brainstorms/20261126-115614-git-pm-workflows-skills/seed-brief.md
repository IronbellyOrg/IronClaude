---
topic: "Embed more Git and PM related workflows into skills @.dev/issues/326/issue-summary.md"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-11-26T11:57:00Z
---

# Seed Brief: git-pm-workflows-skills

## Problem Statement

`/sc:git` is a 91-line prose command with no options table, no STOP rules, no backing skill and no submodule text, and it has never been functionally changed. `/sc:implement` makes no commit between tasks, so a long plan lands as one unreviewable change and a lost session loses work. The owner's scope of 2 November (confirmed for this work) narrows the issue's old four-session plan to: a modular `/sc:git` refactor that follows the developer guide, an explicitly authorized commit between tasks in `/sc:implement`, submodule operations in `/sc:git`, and only the branch cleanup that PR 711 did not already deliver.

## Known Context

- Source of truth is `src/superclaude/commands/git.md`; copies: `plugins/superclaude/commands/git.md` (identical), `.claude/commands/sc/git.md` (gitignored dev copy), `commands/sc-git.md` (tracked legacy copy with a doubled `/sc:sc:sc:git` prefix). Edit `src/` first, then `make sync-dev` and `make verify-sync`.
- The central relay (every command calls `/sc:git`) is not wanted: commands cannot call another session. `src/superclaude/core/WORKER-CONTRACT.md:23` lists `/sc:git` as never-as-worker. `HOW-WE-WORK.md:293`: a commit needs authorization; no push, merge or PR creation. PRs stay with `/sc:pr-submit`.
- `WORKER-CONTRACT.md:42` parks per-task commits on this issue (K3): only between a task's `complete` line and the next task's start, never inside a parallel batch. `implement.md:100` lists auto-commit as a Will Not today. `sc-implement-protocol/refs/retry.md` needs HEAD unchanged during a task.
- PR 711 delivered `scripts/worktree_cleanup.py` and `/sc:worktrees`: worktree removal plus local branch deletion with `git branch -d` only. Reuse it; no remote branch deletion (decided).
- `integration` is the base branch (PR 824); `master`, `integration` and release tags have rulesets (PR 831). `docs/developer-guide/git-standards-protocols.md` and `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` are the standards.
- Submodule handling exists only in pr-submit, sweep probes, implement retry and workflow remediation; the operations are not yet defined.
- Full evidence: `.dev/issues/326/analysis/analyze-git.md`, `.dev/issues/326/accuracy-check.md`.

## Constraints

- Keep authorization limits: no commit without authorization; `/sc:git` never pushes, merges or opens PRs; destructive operations need confirmation.
- Never stage `.claude/`; always stage `.dev/tasks`; preserve PR 288 (task evidence always staged).
- No installed primitive may name a `src/superclaude/...` path; use installed paths (CLAUDE.md rule).
- A per-task commit step must sit outside the task body and never run in a parallel batch.
- Reuse `scripts/worktree_cleanup.py`; add nothing that deletes a remote branch.
- Behaviour changes need tests (authorization, commit timing, hook refusal, staged paths).

## Success Criteria

- `/sc:git` has a documented, modular structure (options, STOP rules, outputs, boundaries) that matches the developer guide, with source, plugin mirror and dev copy in sync, and the fate of `commands/sc-git.md` decided.
- `/sc:implement` can, only when explicitly authorized, commit between tasks with a conventional message and only the intended paths plus `.dev/tasks`; no commit inside a parallel batch; a refused hook is reported, not bypassed.
- Defined submodule operations (status, update, commit pointer) exist in `/sc:git` with the same authorization rules.
- No second implementation of local branch cleanup; no remote branch deletion anywhere.
- `make verify-sync` and the related tests pass.

## Open Questions

- One structure for `/sc:git`: a command file only, or a command plus protocol skill with refs per operation group?
- How does `/sc:implement` call the commit step without breaking "`/sc:git` is never a worker" and the retry rule that HEAD stays unchanged: inline in the implement protocol, or through a shared script both use?
- Which authorization switch turns on between-task commits: a flag, a plan-level field, or an explicit user instruction in the session?
- Which submodule operations are in scope, and what happens when a submodule is dirty or detached?
- Is `commands/sc-git.md` fixed, removed or left alone?
- Does the "project management" half of the title (status and progress updates) have any residual scope beyond `/sc:closeout` and `/sc:issue`?

## Enrichment Context

Full artifacts: `enrichment/codebase-context.md` (quality_tier: primary, Augment search) and `enrichment/research-deep.md` (quality_tier: primary, deep research via Tavily; the agent could not write the file, the orchestrator saved its report).

- Codebase: `/sc:git` has no protocol skill; newer commands use the command file + `sc-<name>-protocol` skill + `refs/` pattern. In `/sc:implement`, a commit belongs after a task's `complete` ledger line and before the next task's Q0 snapshot. Worktree cleanup tests already forbid `--force`, `-D` and `--delete`.
- Research, commit practice: Aider commits after each edit with Conventional Commits and commits the user's pre-existing changes first; Claude Code's own instructions commit only on request, stage named files, and make a NEW commit after a hook failure (never `--amend`); prompt rules are advisory and agents have been seen using `--no-verify`, so the command needs its own check. Checkpoints (Claude Code, Cline) are not version control.
- Research, submodules: inspect with `git status --porcelain=v2 --ignore-submodules=none` (the 4-character submodule field `S<c><m><u>`) and `git submodule status`; commit inside the submodule on a branch first, then the pointer in the superproject; push the submodule before the superproject (`--recurse-submodules=check`); `submodule.recurse=true` can push submodules as a hidden side effect; a detached-HEAD submodule with new commits is a stop-and-ask case.
- Research, existing plugins: Anthropic's `commit-commands` (commit, commit-push-pr, clean_gone) is a thin prompt with narrow `allowed-tools`; none of it handles hooks, protected branches, submodules or parallel work, and `clean_gone` force-deletes with `-D`. Ideas to reuse: pre-computed git context, narrow tool lists, a written safety protocol, typed confirmation for destructive steps.
- Research, branch cleanup: `git branch -d` refuses squash-merged branches (a safe false negative). `-d`-only is the conservative choice; stronger proof would be an empty `git merge-tree --write-tree` diff against a fresh `origin/<default>`; `[gone]` alone is not proof.
