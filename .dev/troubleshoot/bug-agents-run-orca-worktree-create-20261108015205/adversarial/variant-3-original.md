# Fix 3: Put the step only in the project rule that forces the bare create (CLAUDE.md:307-324)

Source card: tier2-system-architect-hypothesis.md

## Problem statement
Same diagnosis (tier1-observation.md N1, N2, N8). The rule that forces a tab into existence is the project ABSOLUTE RULE at CLAUDE.md:307-308 (Orca-only, `git worktree add` forbidden at :312). The installed "Orca session launches" section is about starting new Claude sessions, but 11 of 17 bare creates are own-use checkouts, not session launches. Orca has no CLI option to skip the seed (setupOnly is RPC-only and needs a setup hook; IronOrca runtime-worktree-terminal-provisioning.ts:189, :203; rpc/methods/worktree-create-args.ts:87).

## Proposed change
1. Project `CLAUDE.md`, bullet after :310:
   "- A create without `--agent` also opens a plain first terminal. If you will work in the checkout from your own session, close that terminal right after the create, before anything is started there: `orca terminal close --worktree path:<path> --all`. If the checkout is for a new Claude session, put `--agent claude` on the create instead (see "Orca session launches"). `/sc:issue` and supervised workers keep their own launch steps."
2. Add the close line to the example block at :318-324.
3. Files: `CLAUDE.md` only. No pinned-phrase changes.

## Evidence
CLAUDE.md:307-324; IronOrca runtime-local-worktree-terminal-startup.ts:202-210, :264-265; N1, N8, N12 (10 of 11 own-use creates in IronClaude).

## Risks
- `--all` stops every terminal in that worktree; "before anything is started there" is the only guard.
- Only reaches IronClaude sessions on a branch with the fix; misses Coder/IronOrca creates (N12: 1 own-use + 4 hand-offs outside IronClaude) and the 44e7b6ec hand-off pattern.

## Test plan
- New small test in tests/core/: assert the project CLAUDE.md worktree section contains `orca terminal close --worktree`.
- Live V-CLOSE (pending).

## Documented constraints to honor
(verbatim from doc-context.md)

### Restrictions / decisions that constrain the fix

- `CLAUDE.md:307` (worktree creation) — "every project worktree is created through Orca"
- `CLAUDE.md:312` (worktree creation) — "Never create a project worktree with raw `git worktree add` ..."
- `CLAUDE.md:314` / `:54` (link flags) — never pass `--issue`, `--pr` or other Orca link flags for this repo
- `src/superclaude/core/CLAUDE.md:47-52` (session launch) — new Claude session = Claude (CLI) / `worktree create --agent` / `agent launch`; `worker-start` stays authoritative for supervised workers
- `src/superclaude/core/WORKER-CONTRACT.md:62` (workers) — workers never call `worktree create --agent` or `agent launch`
- `src/superclaude/skills/sc-issue-protocol/SKILL.md:176` and tests/skills/test_issue_orca_worktree.py:264-279 — `--agent` is forbidden on /sc:issue's create step
- tests/core/test_orca_session_launch_guidance.py:10-31 — 12 phrases pinned in both copies of "Orca session launches" (core/CLAUDE.md and ccsession-tag/README.md)

### Re-frame signals

- The empty tab is Orca's documented default ("By default this creates the worktree and its first terminal", `orca worktree create --help`, tier1-observation.md N2), and the repo rule tells agents to run exactly that bare create. The defect is the missing instruction for what to do with that first terminal, not a code deviation.
- Adding `--agent` is the wrong fix for most observed cases: 11 of 17 bare creates were followed by the same session cd-ing into the checkout (tier1-observation.md N1), and `--agent` is forbidden for /sc:issue's create step and for supervised workers.
- No doc tells an agent to close or reuse the seeded terminal; that gap is where a fix fits.
