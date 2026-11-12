# Documentation Context Card

**Generated**: 2026-11-08T01:56Z
**Wave**: 1.5
**Scope**: (none); component paths CLAUDE.md:303-325, src/superclaude/core/CLAUDE.md:45-53, src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, src/superclaude/skills/ccsession-tag/README.md
**Degraded**: all three branches (auggie unavailable; Grep/Read)

## Release context

- **Release**: None found under .dev/releases (fallback hits only)
- **Artifacts**: docs/designs/sc-issue-claim-pipeline-flag.md; .dev/tasks/done/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md
- **Summary**: The /sc:issue design deliberately creates the worktree without --agent (D2, line 370; FO-18, line 333) and launches Claude in a second call. The plan that wrote the CLAUDE.md Orca-only rule (Task 3, lines 80-97) says nothing about --agent, the first terminal, or agents that only cd into the worktree.
- **Confidence**: 0.7

## Architectural docs consulted

- `CLAUDE.md` — verdict: `current` — Orca-only worktree rule; bare create example (307-310, 320); silent on starting a session and on the first terminal.
- `src/superclaude/core/CLAUDE.md` — verdict: `current` — "Orca session launches": `worktree create --agent` for a new checkout when a new Claude session is wanted (47-51).
- `src/superclaude/core/WORKER-CONTRACT.md` — verdict: `current` — workers never call `worktree create --agent` or `agent launch` (62).
- `docs/designs/sc-issue-claim-pipeline-flag.md` — verdict: `current` (Status: Design only) — bare create, then `agent launch --surface terminal` (184, 211, 370).
- `docs/designs/sc-issue-command.md` — verdict: `current` (Status: Design only) — claim launches one agent (13, 43-44).
- `docs/user-guide/commands.md` — verdict: `current` — claim launches one Claude agent (349).

Currency caveat: all mtimes equal checkout time; "current" means fresh relative to code and no deprecated markers, not a verified review date.

## Restrictions / decisions that constrain the fix

- `CLAUDE.md:307` (worktree creation) — "every project worktree is created through Orca"
- `CLAUDE.md:312` (worktree creation) — "Never create a project worktree with raw `git worktree add` ..."
- `CLAUDE.md:314` / `:54` (link flags) — never pass `--issue`, `--pr` or other Orca link flags for this repo
- `src/superclaude/core/CLAUDE.md:47-52` (session launch) — new Claude session = Claude (CLI) / `worktree create --agent` / `agent launch`; `worker-start` stays authoritative for supervised workers
- `src/superclaude/core/WORKER-CONTRACT.md:62` (workers) — workers never call `worktree create --agent` or `agent launch`
- `src/superclaude/skills/sc-issue-protocol/SKILL.md:176` and tests/skills/test_issue_orca_worktree.py:264-279 — `--agent` is forbidden on /sc:issue's create step
- tests/core/test_orca_session_launch_guidance.py:10-31 — 12 phrases pinned in both copies of "Orca session launches" (core/CLAUDE.md and ccsession-tag/README.md)

## Re-frame signals

- The empty tab is Orca's documented default ("By default this creates the worktree and its first terminal", `orca worktree create --help`, tier1-observation.md N2), and the repo rule tells agents to run exactly that bare create. The defect is the missing instruction for what to do with that first terminal, not a code deviation.
- Adding `--agent` is the wrong fix for most observed cases: 11 of 17 bare creates were followed by the same session cd-ing into the checkout (tier1-observation.md N1), and `--agent` is forbidden for /sc:issue's create step and for supervised workers.
- No doc tells an agent to close or reuse the seeded terminal; that gap is where a fix fits.
