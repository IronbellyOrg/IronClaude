# Findings: issue #772 (stage flow through the watcher, what Pipeline Full means, a build step)

Checked 2026-11-24 on worktree HEAD a7ae3dd30 (branch ironbelly/Issuecleanup). origin/master is f2894fc44; the only files in the issue's area that differ between the two are `src/superclaude/cli/issue_watch/dispatch.py` and `first_run.py`, which hold none of the cited rules. The issue is OPEN, label `enhancement`, created 2026-11-24T18:26:51Z by clayphi, 0 comments, no linked PR, no sub-issues, no blockers (gh issue view). `/sc:analyze` report: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g7/772/analyze/analyze-report.md`.

## Verdict

**still-relevant.** Nothing in the issue has been answered or fixed: the owner has not answered questions (a) to (d), no PR references #772, and every claim I re-read in source still holds on this tree.

Evidence (all re-read on the current tree):

- Problem 1 holds. `src/superclaude/cli/issue_watch/cycle.py:982` raises `_Skip("already_dispatched")` for state `claimed` or `pending`. `src/superclaude/cli/issue_watch/record.py:448` defines `_RESETTABLE = {"abandoned", "unknown"}` and `:714` refuses a reset for any other state (the issue says 981-982; the line is 982 here, a one-line drift). `src/superclaude/cli/issue_pipeline/complete.py:55-60` (`END_STATUS`) maps Research, Spec, Plan and Debug all to In review.
- The four relaunch passages still exist: `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt:17`, `src/superclaude/core/WORKER-CONTRACT.md:297` (last sentence), `docs/designs/issue-watcher-status-pipelines.md:65` and `:79`. Strictly the sentences say a relaunch "needs" the Status moved back, which is a necessary condition; for a `claimed` entry it is not sufficient (cycle.py:982, record.py:714), so a reader is misled. A test pins the sentence: `tests/issue_pipeline/test_brief.py:242` (`test_the_brief_says_a_relaunch_needs_the_status_moved_back`); the brief fixture at `:29` repeats it.
- Problem 2 holds. `src/superclaude/commands/issue.md:16` says `full` also implements with no commit or push and `full` with `--submit` also commits, pushes and opens a PR. The watcher design's level table (`docs/designs/issue-watcher-status-pipelines.md`, Research row) says Full is the stage command plus one local commit of the report. `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:28` (full block) says make no commit. `src/superclaude/skills/sc-issue-protocol/refs/claim.md:80` says that with `--stage` step 1 is only the stage command and the stage command never runs `/sc:implement` or `/task`. The issue cites launch-prompt `:27-28`; the full block's no-commit text is on line 28.
- The ship gate is closed: `src/superclaude/cli/issue_watch/launch.py:48` `GOVERNED_LEVELS_ALLOWED = False`; `cycle.py:1029-1036` ends such an issue `level_gated`. #450 is CLOSED (gh issue view). So Worktree, Full and Full Submit do not run through the watcher today; the contradictions are documentation and design debt, not a live failure.
- Problem 3 holds. `launch-prompt.md:25` (worktree block) says a human approves only by running the printed implement command, a prompt starting `/sc:implement`, `/sc:task` or `/task`; `launch-prompt.md:45` (plan block) says never run `/sc:implement` or `/task` for this stage. Both are in the same rendered prompt for Worktree plus `--stage plan`.
- Problem 2, "only the stage command is prose": `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md:12` keeps a step 2 slot; `claim.md:80` is prose. `grep` of `scripts/orca_worktree.py` finds no `next-steps` read (no match in the first lines of the grep, so the issue's claim that the script never reads it is consistent; I did not read the whole script, so treat that as lightly verified). Existing tests that touch `next-steps.md` check template text only (`tests/skills/test_issue_protocol.py:543,553,886-887`).
- No PR addresses this: `gh pr list --search` on the area returned only earlier work (#584, #591, #682, #697, #700, #707), none of which designs stage chaining or fixes the relaunch text.
- UNVERIFIED: what a real stage claim writes into `next-steps.md` (needs one throwaway `--pipeline none --stage research` claim; this task is read-only on GitHub and forbids outward actions).
- UNVERIFIED: the wording of the Pipeline field's option descriptions on the Project board (not read).
- Note from the reviewer (qa.md): the script is `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; a grep for `next-steps` and `next_steps` finds no match, so the issue's claim that it never reads `next-steps.md` is consistent with source.

## Complexity and size

Complexity **medium**, size **M**: the text fixes are small (about 6 files plus 2 test updates) but they wait on four owner decisions, and the optional code check on `next-steps.md` adds a new test and a boundary change.

## Priority

**P2**: the false relaunch guidance and the Full definition conflict mislead readers but cannot bite in production while the ship gate is closed and only level None runs; it blocks no code work, only the owner's answers. (The issue itself asks for High; I weigh it lower because nothing live depends on it.)

## Concrete next steps

1. Owner answers (a) to (d) in #772 in chat; the agent records them (owner never writes a file). Without the answers nothing below should change behaviour.
2. After answer (d): fix the four relaunch passages (worker-brief.txt:17, WORKER-CONTRACT.md:297, design :65 and :79) and update `tests/issue_pipeline/test_brief.py:242` and `tests/skills/test_worker_contract.py::test_the_duties_name_the_status_to_command_table_and_the_brief_at_level_none_only` to pin the new wording. Edit `src/superclaude/core/WORKER-CONTRACT.md` at its source, then run `make sync-dev`.
3. Remove the Worktree-with-Plan conflict in `launch-prompt.md:25` versus `:45` without allowing implement in a Plan stage; add a rendered-prompt test for that case.
4. Pick one meaning of Full and align `commands/issue.md:16`, `refs/claim.md`, `templates/launch-prompt.md` and the design table.
5. If (c) is yes, add a `next-steps.md` check at the claim output boundary with a failing-case test; keep the Spec brainstorm-then-design route allowed.
6. Settle the two UNVERIFIED Problem 2 items only through the owner's real-issue check, within the existing gate.
7. Run `uv run pytest`, `make lint`, `make verify-sync` (not run here; this task forbids uv).

## Dependencies

- Needs: the owner's answers to (a) to (d) in #772. The ship gate (out of scope) depends on #442, #678 and #722, all OPEN.
- Blocks: nothing hard. Any plan to chain stages or add a build step through the watcher depends on these answers; #733 (unattended `/sc:implement`, OPEN) lists an implement row in the issue pipeline brief as out of scope.

## Related issues

#761 (OPEN, list of potential gaps this issue comes from), #733 (OPEN), #734 (OPEN), #442 (OPEN), #678 (OPEN), #722 (OPEN), #689 (CLOSED, not planned per the issue body; state CLOSED confirmed, reason not re-read), #450 (CLOSED).

## Related PRs

#707 (MERGED, the watcher and standing coordinator), #729 (MERGED, records R38: the merged watcher is the design), #591 (MERGED, coordinator handoff, Plan B), #584 (MERGED, approval core). No open PR addresses #772.
