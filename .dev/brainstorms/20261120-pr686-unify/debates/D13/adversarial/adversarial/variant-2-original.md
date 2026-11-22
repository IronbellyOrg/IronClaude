# Position CLAY: D13 closeout, worktree cleanup, PR log versus issue 339 duties

## Claim

Clay's three pieces are complementary, not duplicates, and each fills a gap that issue 339 lists but nobody built. Keep all three. `/sc:closeout` (PR 683, merged) becomes the coordinator's wave 8 step; the cleanup (issue 687, a full spec, nothing built) becomes the safe removal that 339's `sc:close` asks for; the PR log (PR 670, merged by the owner) is a separate reporting tool. Removal is a script run by an opt-in automation with no agent, not by the orchestrator, because removal cannot be undone and a script with nine mechanical rules is safer than a session's judgment.

## Mechanism

- Closeout runs after a merge: a script reads PR state (`branch-landed.sh`, three-dot diff, never commit ancestry), the session judges whether the issue is done, and scripts write the closing note, the work-report entry and the Orca task status. It never deletes anything.
- Cleanup (issue 687) is `scripts/worktree_cleanup.py` with verbs `list`, `archive`, `retire`, `prune`, dry run by default. A worktree goes only when all nine rules hold: its PR merged (judged by the closeout landed check), nothing added after it, issue closed, nothing using it, idle 7 days, and `.dev/` workflow files saved and verified in a private evidence repo first. Never `--force`, never `git branch -D`, never `rm`.
- PR log (PR 670) is a stdlib script that writes a daily digest of merged PRs per person to a ClickUp Doc. No orchestration.

## Cited facts

1. PR 683 (merged by `clayphi`, 2026-11-20 01:16): adds `/sc:closeout` and `sc-closeout-protocol`; PR body reports a full suite of 22864 passed and 2 failed (both a missing `ruff` in the venv); the spec `docs/designs/sc-closeout.md` and the PR body say the owner approved the spec and the adoption of Jay Wedgeworth's skill.
2. `src/superclaude/skills/sc-closeout-protocol/SKILL.md` Will Not Do: never "Merge, push, commit, stage or delete a branch or a worktree". It settles three items (issue, work-report entry, Orca task) read-then-write, with escalations.
3. `docs/designs/orchestrator.md` wave 8 (line 603): the orchestrator calls `Skill sc:closeout-protocol <PR>`, then the audit, then `report-entry`. Closeout is already a coordinator step in the merged design; issue 339 mentions `sc:close` but never defines this settle step.
4. Issue 339 status review 2026-11-17 (owner): "the acting half (resume, close, cleanup, orchestrator-mode report) is not built". Clay's work is the only specified path to those duties.
5. Issue 687 body: on 2026-11-20 git knew 53 worktrees (49.4 GB), Orca listed 26; 13 removable (3.1 GB); sixteen workspaces were removed by hand and two belonged to open issues (#354, #419), which is why "issue closed" is a rule. This is the "rigid and strict validation" the owner asked for on 2026-11-05.
6. Issue 687 rulings: "A worktree whose issue is still open is never removed"; "Never --force, never git branch -D, never rm"; opt-in schedule; dry run default. Its landed check reuses closeout's `branch-landed.sh` (issue 687 "Related Issues/PRs"), so both tools share one truth check.
7. PR 670 body: "nothing to do with the daily work report or the orchestrator"; merged by `ironbelly`, so the owner accepted it. It has no counterpart among 339's duties.
8. Deleting branches is human-only: `docs/designs/orchestrator.md` line 139 (ADD5, "never `--delete-branch` (deleting branches is human-only, rule 1)") and line 628. Clay's design keeps removal out of any model session.
9. `/sc:sweep` (PR 539) is read-only and recommends nothing (issue 339 status review 2026-11-17), so it does none of closeout's writes or cleanup's removals, and none of Clay's pieces repeat the hourly sweep.

## What it costs

- Two tools share one landed check, so a change to `branch-landed.sh` touches both.
- 687 is not built; the cleanup duty stays unmet until it is.
- The "orchestrator never removes worktrees" rule departs from the owner's wording of 2026-11-05.

## What it risks

- Closeout decides "done" by a model reading criteria (spec D18, Clay's ruling 32); a wrong `done` closes half-done work (spec section 12.1).
- Owner approval of the cleanup design is not on record; issue 687 has no `ironbelly` comment (FULL-REPORT.md).

## What it gets right

- Safety: the nine rules are mechanical, tested with fake `gh`, `git` and `orca`, and fail closed.
- Reuse: closeout's landed check, the PR-log opt-in and Orca automation pattern, `/sc:sweep` kept for sweeping.
- One job per tool: settle (closeout), remove (cleanup), report (log).

