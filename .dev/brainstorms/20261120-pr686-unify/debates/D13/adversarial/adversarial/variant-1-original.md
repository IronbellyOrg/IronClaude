# Position OURS: D13 closeout, worktree cleanup, PR log versus issue 339 duties

## Claim

Issue 339 (the owner's issue: one orchestrator manages all sessions of a worktree) already defines the duties: an hourly sweep that finds idle sessions, a `sc:close` that does full worktree and branch cleanup with strict validation, and an orchestrator that keeps polling until a session is finished, cleaned up and closed. Clay's closeout, cleanup and PR log must be read under 339's scope, not as a separate duty set with their own rules. The coordinator owns the whole close-out chain, and the one rule that conflicts with the owner (the orchestrator never removes worktrees or branches) must not land.

## Mechanism

- The owner's 2026-11-05 comment on issue 339 says "Work tree and Branch clean up should be part of this roles responsibilities after work is complete with extra rigid and strict validation and safety protocols", and that the orchestrator "keeps polling indefinitely until sessions are completely finished, cleanup has been commenced and the session has been closed".
- The issue body defines `sc:close` as "full worktree and branch cleanup and deletion process. Must validate no files of value are left uncommitted and that all commits have been pushed before deletion."
- `/sc:sweep` (read-only phase 1, PR 539, merged 2026-11-14) is the owner's built answer to the hourly-sweep duty.
- So the close chain belongs inside one owner-defined coordinator role: sweep, then close, then cleanup. Clay's closeout (settle the issue and Orca task), cleanup (worktree removal) and log (reporting) are three separate tools whose link to the coordinator comes only from Clay's rules.

## Cited facts

1. Issue 339 body (owner, `ironbelly`): hourly `sc:sessionsweep`; `sc:close` "has full worktree and branch cleanup and deletion process" (read with `gh issue view 339 --repo IronbellyOrg/IronClaude`).
2. Issue 339 comment 2026-11-05 13:43Z (owner): worktree and branch cleanup is part of the orchestrator role's responsibilities, "extra rigid and strict validation".
3. Issue 339 status review 2026-11-17 (owner): `sc:close` is not built; "Keep the issue open until at least the `sc:close` item is built or explicitly dropped."
4. `/sc:sweep` merged by PR 539 (2026-11-14); rule WC-16 says run it on every coordinator wake (H-design681-map.md row 1.3); Clay's design never mentions sweep.
5. Clay's design says the orchestrator never removes a worktree or branch: `docs/designs/orchestrator.md` line 628 (master snapshot): "removing it, like deleting its branch, is not done by the orchestrator". Issue 687 (Clay) repeats "This cleanup is never run by the orchestrator". This contradicts fact 2.
6. `/sc:closeout` (PR 683) drops Jay Wedgeworth's "Retire the lane" step: `docs/designs/sc-closeout.md` line 106 ("dropped"), and the skill's Will Not Do (`src/superclaude/skills/sc-closeout-protocol/SKILL.md`) lists "delete a branch or a worktree". So closeout is not the `sc:close` that 339 describes.
7. `/sc:closeout` is on the never-as-worker list: `src/superclaude/core/WORKER-CONTRACT.md` line 23. It is coordinator or person only, which fits the owner's role design and lets it become a coordinator step.
8. PR 670 (daily PR log, merged by `ironbelly`) says in its body it "has nothing to do with the daily work report or the orchestrator": no 339 duty overlaps it.
9. On GitHub, `ironbelly` left no comment, review or reaction on 655, 668, 681 to 684, 686, 687 (FULL-REPORT.md item 7), so the owner never ruled on the wave 8 close chain as a coordinator duty. The sc-closeout spec does say "owner approved" for the skill itself.

## What it costs

- Reading Clay's pieces under 339 delays 687 (cleanup is only an issue, nothing built) until the coordinator scope for removal is settled.
- Rewriting the "orchestrator never removes worktrees" sentences in Clay's merged design (line 628) is a design change.

## What it risks

- If the coordinator may delete worktrees and branches, a defect in its checks can destroy unpushed work. Issue 687 shows the danger is real: 16 workspaces were removed by hand on 2026-11-20 and two belonged to still-open issues (#354, #419).
- Treating Clay's tools as duplicates and retiring them would throw away a built, tested closeout and a worked-out 9-rule cleanup design.

## What it gets right

- The owner's duty list is the older, wider definition of who does cleanup. Closeout settles a merged PR; it does not close a session, check for uncommitted files, or remove anything. The owner's words need one accountable role.
- `/sc:sweep` is built and covers the hourly duty.

