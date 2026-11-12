# Documentation Context Card

**Generated**: 2026-11-08T00:02:30Z
**Wave**: 1.5
**Scope**: (none)

## Release context

- **Release**: None found under .dev/releases/. The scoping artifact is the managed package for the earlier fix, TASK-WF-fixIssue412SVeri-20261106-215543.
- **Artifacts**: .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/{source.md, TASK-WF-fixIssue412SVeri-20261106-215543.md, artifacts/final-review.md, artifacts/reflect-pre-20261106-215816/artifacts/orca-discovery.md}
- **Summary**: The #412 fix added a written rule (src/superclaude/core/CLAUDE.md:45-53, ccsession-tag README:228-237): new Claude sessions use Claude (CLI), never New Terminal; `agent launch` / `worktree create --agent`; `terminal create` is for shells. It also repaired the forced guide refresh. Its own final review says these are selection instructions only, with no test of a live agent or UI route; the runtime cause was left UNDETERMINED.
- **Confidence**: 0.9

## Architectural docs consulted

- `docs/designs/sc-issue-claim-pipeline-flag.md` — verdict: `current` — P7 launches Claude with `orca agent launch --agent claude --surface terminal`; D2: worktree create has no `--agent`; warns W-LAUNCH-NOT-CCSESSION.
- `docs/designs/sc-issue-launch-level-hook.md` — verdict: `current` — launch hook assumes `orca agent launch`; `orca terminal send` and `tmux send-keys` are bypass routes.
- `docs/designs/sc-issue-command.md` — verdict: `current` — launch levels; agent starts via `orca agent launch --surface terminal`.
- `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (section 7.7) — verdict: `current` — coordinator and worker model; WC-8; no mention of the Claude CLI versus New Terminal choice.
- `docs/testing/v5.0.0/user/D08-ccsession.md` — verdict: `current` — `ccsession-orca` as Orca's Claude command; orchestrators should pass a prompt or CCSESSION_NAME.
- `CLAUDE.md` (repo root) — verdict: `current` — worktree creation rule with no `--agent` and no session-launch guidance.
- `docs/user-guide/commands.md` — verdict: `current` — one summary line.

> Note: all mtimes equal the checkout time (2026-11-07T20:35:30Z), so "current" rests on the absence of Status markers and on git dates, not on file age.

## Restrictions / decisions that constrain the fix

- `CLAUDE.md:307` (worktree creation) — "ABSOLUTE RULE — every project worktree is created through Orca and lives at Orca's default worktree location."
- `CLAUDE.md:312` (worktree creation) — "Never create a project worktree with raw `git worktree add`, under the retired `.dev/worktrees/` location, or under `.claude/worktrees/`."
- `CLAUDE.md:313` (worktree creation) — "Do **not** use the `EnterWorktree` tool..."
- `src/superclaude/core/CLAUDE.md:47-51` (launching Claude sessions) — "For a new ccsession-backed Claude session, choose **Claude (CLI)**, never **New Terminal**. ... Use `agent launch` in an existing worktree or `worktree create --agent` for a new checkout ... `terminal create` is for shells, not agent sessions."
- `src/superclaude/core/CLAUDE.md:52` (scope limit) — "For supervised workers, keep `worker-start` and the dispatch preamble authoritative; this rule does not replace supervised dispatch or commands' internal Agent-tool subagents."
- `src/superclaude/skills/ccsession-tag/README.md:230-236` — same rule and scope limit.
- Conflict check: no contradiction, one gap. Repo-root CLAUDE.md's worktree rule never mentions `--agent`; the core rule does not say whether `worktree create` without `--agent` is acceptable when a Claude session is also wanted. `orca_worktree.py:27` and the pipeline-flag design D2 deliberately create the worktree without `--agent` and launch Claude in a second call.
- Installed copy: /home/coder/.claude/CLAUDE.md has no "Orca session launches" paragraph (branch C note; confirmed by parent grep, 0 matches).

## Re-frame signals

- The written rule from #412 exists in the repo but is not in the installed global instructions (parent grep: ~/.claude/CLAUDE.md, installed ccsession README, pipx package all have 0 matches), so agents on this host never load it.
- The repo's own worktree rule (CLAUDE.md:308) and the `/sc:issue --claim` design (D2) create worktrees with no `--agent`; each such worktree opens with one default plain terminal. That is documented behaviour, not a bug in itself, and it produces an "empty terminal" even when the Claude session is launched correctly in a second call.
- The #412 package never captured a failing orchestrator transcript, so the reported behaviour (an orchestrator choosing New Terminal) has still never been observed in this repo's evidence.
