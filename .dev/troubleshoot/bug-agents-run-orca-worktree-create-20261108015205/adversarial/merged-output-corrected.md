<!-- Corrected from merged-output.md after self-review FAIL (self-review.md: B-1 blocking, M-1..M-4 minor). Written 2026-11-08T02:56Z. -->

# Corrected Fix: Close the plain first terminal after an own-use bare create; route hand-offs to --agent

## Problem statement
A bare `orca worktree create` (no `--agent`) makes Orca open a plain first terminal (Orca help: "By default this creates the worktree and its first terminal"; IronOrca runtime-local-worktree-terminal-startup.ts:202-214). The repo rule (CLAUDE.md:307-320) requires that bare create and no instruction says what to do with the terminal. 17 of 18 hand-typed creates were bare; 11 were followed by the same session working in the checkout itself; 5 handed work to a new tab (tier1-observation.md N1, N8). The installed ~/.claude/CLAUDE.md lacks the "Orca session launches" section (N12).

## Proposed change
1. `src/superclaude/core/CLAUDE.md`: APPEND a new paragraph after the existing "Orca session launches" paragraph (which ends at line 53, before `## Key Docs` at line 55). Do not change lines 45-53. Text:
   "A `worktree create` without `--agent` also opens a plain first terminal. If you will work in that new checkout from your current session, close it right after the create with `orca terminal close --worktree path:<path> --all`, only when you created it with no setup script (`--setup skip` or none configured), the repo opens no default tabs, and you have started nothing in it; never run this on a worktree you did not just create. To hand work to a new Claude session, use `worktree create --agent` instead of a bare create; `/sc:issue` and supervised workers keep their own launch steps."
2. `src/superclaude/skills/ccsession-tag/README.md`: APPEND the same paragraph after its "Orca session launches" paragraph (ends at line 237, before `#### The one question rule` at line 239). Do not change lines 228-237.
3. Project `CLAUDE.md`: insert one bullet as the first list item, at line 312 (before the existing "Never create a project worktree..." bullet):
   "- A create without `--agent` also opens a plain first terminal. If you will work in the checkout from your own session, close it right after the create with `orca terminal close --worktree path:<path> --all`, only with no setup script and no default tabs and before anything is started there; never on a worktree you did not just create. If the checkout is for a new Claude session, put `--agent` on the create instead (see "Orca session launches" in `~/.claude/CLAUDE.md`). `/sc:issue` and supervised workers keep their own launch steps."
   And in the example block (318-324), after the create line, add: `# If you will work in it yourself: orca terminal close --worktree path:<path> --all`
4. `make sync-dev`, `make verify-sync`. After the change is merged (or with an editable install), run `superclaude update` (plain `superclaude install` keeps the existing ~/.claude/CLAUDE.md, install_core.py:70-72; `update` forces, main.py:365). Then `grep -c 'Orca session launches' ~/.claude/CLAUDE.md` must print 1.
5. Leave `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` unchanged; file a separate backlog issue (its bare create + `agent launch` likely leaves the same tab; unobserved, N11; its argv is pinned by `test_fo18_exact_commands_and_no_forbidden_flag`).

## Risks
- `--all` stops every terminal in the worktree and removes its tabs, layouts and resume records (N3); the guards limit it to a worktree just created for own use with no setup script and no default tabs. Variant 2 dissent: a single-handle close would bound the damage if the guards are misjudged.
- Opening the worktree in the Orca UI later re-seeds a shell (worktree-activation.ts:275): user-driven, acceptable.
- Compliance is unproven: the test proves the text exists, not that agents follow it.
- `superclaude update` overwrites local edits to ~/.claude/*.md.

## Test plan
- `tests/core/test_orca_session_launch_guidance.py`: add pinned phrases `orca terminal close --worktree` (plain text, no backticks) and `worktree you did not just create` to the list checked in both copies; the 12 existing phrases unchanged.
- New small test (tests/core/): the project CLAUDE.md section from `### Parallel Development with Git Worktrees` to the first following `\n## ` heading contains `orca terminal close --worktree`.
- `uv run pytest tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py tests/skills/test_issue_orca_worktree.py -v` (the last file unchanged and passing).
- Live V-CLOSE (pending; needs a create): after a bare own-use create and the close, `orca terminal list --worktree path:<p> --json` lists no terminals and the worktree is still in `orca worktree list`.

## Documented constraints to honor
(verbatim from doc-context.md; unchanged from merged-output.md)
- `CLAUDE.md:307` — "every project worktree is created through Orca"
- `CLAUDE.md:312` — "Never create a project worktree with raw `git worktree add` ..."
- `CLAUDE.md:314` / `:54` — never pass `--issue`, `--pr` or other Orca link flags for this repo
- `src/superclaude/core/CLAUDE.md:47-52` — new Claude session = Claude (CLI) / `worktree create --agent` / `agent launch`; `worker-start` stays authoritative for supervised workers
- `src/superclaude/core/WORKER-CONTRACT.md:62` — workers never call `worktree create --agent` or `agent launch`
- `src/superclaude/skills/sc-issue-protocol/SKILL.md:176` and tests/skills/test_issue_orca_worktree.py:264-279 — `--agent` is forbidden on /sc:issue's create step
- tests/core/test_orca_session_launch_guidance.py:10-31 — 12 phrases pinned in both copies of "Orca session launches"
