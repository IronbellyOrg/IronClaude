# Fix 1: Put the "close the seeded tab" step in the installed core rule, scoped to own use, and reinstall

Source card: tier2-root-cause-analyst-hypothesis.md (extends tier1-hypothesis.md)

## Problem statement
A bare `orca worktree create` (no `--agent`) makes Orca open a plain first terminal (IronOrca runtime-local-worktree-terminal-startup.ts:202-214; installed help: "By default this creates the worktree and its first terminal"). No instruction says to use or close it. 17 of 18 hand-typed creates were bare; 11 were followed by the same session `cd`-ing into the checkout; 5 handed work to a new terminal. All 7 checked bare-created worktrees have a daemon `hasCommand=false` row. Creates happened in IronClaude, Coder and IronOrca (tier1-observation.md N12). The installed ~/.claude/CLAUDE.md lacks the "Orca session launches" section entirely (N12: 0 matches).

## Proposed change
1. `src/superclaude/core/CLAUDE.md` "Orca session launches" (lines 45-53): add after line 51:
   "A `worktree create` without `--agent` also opens a plain shell tab; if you will work in the new checkout from your current session, close it right after the create with `orca terminal close --worktree path:<path> --all`; to hand work to a new Claude session, use `worktree create --agent` instead of a bare create."
2. Same sentence in `src/superclaude/skills/ccsession-tag/README.md` (lines 228-237).
3. `make sync-dev`; then reinstall (`superclaude update`, since plain `install` skips existing files per install_core.py:70-72) so ~/.claude/CLAUDE.md gets the section.
4. No project CLAUDE.md change.

## Evidence
tier1-observation.md N1, N2, N3, N7, N8, N12; IronOrca runtime-local-worktree-terminal-startup.ts:202-214, :223-233 (no seeded handle returned), workspace-creation.ts:209 (seed awaited when no setup/default tabs).

## Risks
- `--all` stops every terminal in the worktree: dangerous if reused on an existing worktree or after an agent launch; the sentence limits it to own use right after create.
- Setup hooks / default tabs: provisioning is fire-and-forget, the seed may land after the close.
- Reaches agents only after reinstall.

## Test plan
- Add 13th pinned phrase "`orca terminal close`" to tests/core/test_orca_session_launch_guidance.py (both copies).
- `uv run pytest tests/core/test_orca_session_launch_guidance.py -v`.
- Live V-CLOSE (pending; needs a create).

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
