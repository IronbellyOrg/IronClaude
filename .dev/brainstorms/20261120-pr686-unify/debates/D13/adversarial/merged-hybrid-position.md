<!-- Provenance: merged output of the adversarial pipeline for D13 (closeout, worktree cleanup, PR log versus issue 339 duties) -->
<!-- Base: Variant 2 (CLAY), adversarial/variant-2-original.md -->
<!-- Incorporated: Variant 1 (OURS) facts 1 to 4 and its risk, the debate transcript, and the orchestrator-verified facts on WORKER-CONTRACT.md lines 236, 237, 241 and 289 -->
<!-- Plan: adversarial/refactor-plan.md, Changes 1 to 6, executed 2026-11-20 -->

# Position HYBRID: D13 closeout, worktree cleanup, PR log versus issue 339 duties

<!-- Source: Base (original, modified) - Claim replaced with the agreed hybrid per Change #1; first-use glosses and "coordinator" wording per Change #5 -->
## Claim

Clay's three pieces are complementary, not duplicates, and none is retired. Closeout and the cleanup fill duties that issue 339 lists and that the owner's status review says are not built (fact 10). The coordinator is the accountable owner of the whole close chain (sweep, settle, cleanup), as the owner's issue 339 comment of 2026-11-05 says (fact 2). In this paper "coordinator" means the role that the design of PR 681 calls "orchestrator"; open item 1 asks for the written mapping between the names.

- `/sc:closeout` (PR 683, merged) is a coordinator step: wave 8 of the orchestrator design, the step that runs after a merge (closeout, then the audit, then the report entry; fact 9).
- Removal of worktrees is done by the nine-rule script of issue 687, not by the free judgment of a session. The coordinator runs it: the list or dry run on each cycle, and the apply step only under a grant (open items 2 and 3). Removal cannot be undone, and a script with nine mechanical rules is safer than a session's judgment.
- Deleting a branch stays a local `git branch -d` inside the script; deleting a remote branch stays human-only. Whether the script may delete local branches is not settled (fact 14).
- The PR log (PR 670, merged by the owner) stays a separate reporting tool, unrelated to the close chain.
- Reading the pieces under issue 339 is not a reason to delay issue 687.

<!-- Source: Base (original, modified) - Orca glossed on first use per Change #5 -->
## Mechanism

- Closeout runs after a merge: a script reads PR state (`branch-landed.sh`, three-dot diff, never commit ancestry), the session judges whether the issue is done, and scripts write the closing note, the work-report entry and the Orca task status (Orca is the worktree and task manager). It never deletes anything.
- Cleanup (issue 687) is `scripts/worktree_cleanup.py` with verbs `list`, `archive`, `retire`, `prune`, dry run by default. A worktree goes only when all nine rules hold: its PR merged (judged by the closeout landed check), nothing added after it, issue closed, nothing using it, idle 7 days, and `.dev/` workflow files saved and verified in a private evidence repo first. Never `--force`, never `git branch -D`, never `rm`.
- PR log (PR 670) is a stdlib script that writes a daily digest of merged PRs per person to a ClickUp Doc. No orchestration.

<!-- Source: Base (original, modified) - new facts 1 to 6 inserted at the top per Changes #2 and #3, base facts renumbered 7 to 15, "coordinator" wording per Change #5 -->
## Cited facts

1. Issue 339 body (owner, `ironbelly`): an hourly `sc:sessionsweep`; `sc:close` is defined as "full worktree and branch cleanup and deletion process. Must validate no files of value are left uncommitted and that all commits have been pushed before deletion." (read with `gh issue view 339 --repo IronbellyOrg/IronClaude`). <!-- Source: Variant 1 (OURS), fact 1 - merged per Change #2 -->
2. Issue 339 comment 2026-11-05 13:43Z (owner): "Work tree and Branch clean up should be part of this roles responsibilities after work is complete with extra rigid and strict validation and safety protocols"; the orchestrator "keeps polling indefinitely until sessions are completely finished, cleanup has been commenced and the session has been closed". <!-- Source: Variant 1 (OURS), fact 2 - merged per Change #2 -->
3. Issue 339 status review 2026-11-17 (owner): `sc:close` is not built; "Keep the issue open until at least the `sc:close` item is built or explicitly dropped." <!-- Source: Variant 1 (OURS), fact 3 - merged per Change #2 -->
4. `/sc:sweep` was merged by PR 539 (2026-11-14). Rule WC-16 (`src/superclaude/core/WORKER-CONTRACT.md` line 289; also `H-design681-map.md` row 1.3) has the coordinator run `/sc:sweep` on each wake. `/sc:sweep` "recommends nothing: no stop, retry, release, merge or removal. The coordinator decides and performs any action under those rules." <!-- Source: Variant 1 (OURS), fact 4 - merged per Change #3 -->
5. `src/superclaude/core/WORKER-CONTRACT.md` lines 236 and 237 (master snapshot, re-read by the orchestrator during the debate): after a child worktree's result is admitted, the coordinator may merge the child branch, remove the child with `orca worktree rm` and delete its branch. It may not remove "a worktree or branch that holds unmerged commits, an open PR, uncommitted changes, an unfinished `/sc:implement` ledger, or a report it has not read, without the user's instruction". So the contract already gives the coordinator a bounded removal duty for the child worktrees it creates. It does not cover the issue worktrees of merged work, which is the gap issue 687 fills. <!-- Source: Debate transcript, orchestrator note (verified in the master snapshot) - merged per Change #3 -->
6. `src/superclaude/core/WORKER-CONTRACT.md` line 241: the coordinator performs git and GitHub outward actions only when the user's instruction names the action. <!-- Source: Debate transcript, orchestrator note and advocate 2 (verified in the master snapshot) - merged per Change #3 -->
7. PR 683 (merged by `clayphi`, 2026-11-20 01:16): adds `/sc:closeout` and `sc-closeout-protocol`; PR body reports a full suite of 22864 passed and 2 failed (both a missing `ruff` in the venv); the spec `docs/designs/sc-closeout.md` and the PR body say the owner approved the spec and the adoption of Jay Wedgeworth's skill. <!-- Source: Base (original) -->
8. `src/superclaude/skills/sc-closeout-protocol/SKILL.md` Will Not Do: never "Merge, push, commit, stage or delete a branch or a worktree". It settles three items (issue, work-report entry, Orca task) read-then-write, with escalations. <!-- Source: Base (original) -->
9. `docs/designs/orchestrator.md` wave 8 (line 603): the coordinator (called the orchestrator in that design) calls `Skill sc:closeout-protocol <PR>`, then the audit, then `report-entry`. Closeout is already a coordinator step in the merged design; issue 339 mentions `sc:close` but never defines this settle step. <!-- Source: Base (original, modified) - "coordinator" wording per Change #5 -->
10. The same status review as fact 3 says: "the acting half (resume, close, cleanup, orchestrator-mode report) is not built". Clay's work is the only specified path to those duties. <!-- Source: Base (original, modified) - cross-reference to fact 3, which now carries the review -->
11. Issue 687 body: on 2026-11-20 git knew 53 worktrees (49.4 GB), Orca listed 26; 13 removable (3.1 GB); sixteen workspaces were removed by hand and two belonged to open issues (#354, #419), which is why "issue closed" is a rule. This is the "rigid and strict validation" the owner asked for on 2026-11-05. <!-- Source: Base (original) -->
12. Issue 687 rulings: "A worktree whose issue is still open is never removed"; "Never --force, never git branch -D, never rm"; opt-in schedule; dry run default. Its landed check reuses closeout's `branch-landed.sh` (issue 687 "Related Issues/PRs"), so both tools share one truth check. <!-- Source: Base (original) -->
13. PR 670 body: "nothing to do with the daily work report or the orchestrator"; merged by `ironbelly`, so the owner accepted it. It has no counterpart among 339's duties. <!-- Source: Base (original) -->
14. Branch deletion in the orchestrator design: `docs/designs/orchestrator.md` line 139 (ADD5, the design rule that bans `--delete-branch` on `gh pr merge`) reads "never `--delete-branch` (deleting branches is human-only, rule 1)". Line 628 sits in wave 9 and says the issue worktree is left in place; it is a statement about one wave of one design, not an owner ruling. The contract (fact 5) lets the coordinator remove a child worktree and delete its branch under conditions. Whether ADD5 or the owner's comment of 2026-11-05 governs local branch deletion is not verified. Clay's design keeps the removal decision out of any model session's judgment. <!-- Source: Base (original, modified) - narrowed per Change #1 and the plan's "Changes NOT Being Made" item 3, so it no longer reads as a blanket ban -->
15. `/sc:sweep` (PR 539, fact 4) is read-only and recommends nothing (issue 339 status review 2026-11-17), so it does none of closeout's writes or cleanup's removals, and none of Clay's pieces repeat the hourly sweep. <!-- Source: Base (original, modified) - cross-reference to fact 4 -->

<!-- Source: Base (original, modified) - third bullet narrowed per Change #1 -->
## What it costs

- Two tools share one landed check, so a change to `branch-landed.sh` touches both.
- 687 is not built; the cleanup duty stays unmet until it is.
- The base position's blanket rule that the orchestrator never removes worktrees departed from the owner's wording of 2026-11-05 (fact 2). It is narrowed here: no session decides a removal by its own judgment, and the nine-rule script that the coordinator runs performs it. The sentence at `docs/designs/orchestrator.md` line 628 must then be limited in the design to wave 9's issue worktree, or rewritten; that is a design change (fact 5).

<!-- Source: Base (original, modified) - glosses and mitigations per Change #5; third risk appended per Change #6 -->
## What it risks

- Closeout decides "done" by a model reading criteria (the closeout spec's item D18, and Clay's ruling 32); a wrong `done` closes half-done work (spec section 12.1). Mitigation: closeout's own `unclear` escalation and `left_open` hand-back: a `not_done` verdict leaves the issue open with one note, and an unclear case is escalated (`src/superclaude/skills/sc-closeout-protocol/SKILL.md` lines 20, 85 and 86). These do not catch a wrong `done`; they cover the cases the model marks `not_done` or cannot decide.
- Owner (`ironbelly`) approval of the cleanup design is not on record; issue 687 has no `ironbelly` comment (FULL-REPORT.md). Mitigation: the owner's decision on the cleanup design, given in chat.
- If the coordinator (a model session) may delete worktrees on its own judgment, a defect in its checks can destroy unpushed work. Issue 687 shows the danger is real: on 2026-11-20 sixteen workspaces were removed by hand and two belonged to open issues (#354, #419). This position avoids it by having the nine-rule script, not the session, decide each removal. <!-- Source: Variant 1 (OURS), risks - merged per Change #6 -->

<!-- Source: Debate transcript, A-001 to A-003 (both advocates answered QUALIFY) - merged per Change #4 -->
## Open items before adoption

Both advocates answered QUALIFY on these three unstated assumptions. Each must be settled before this position is adopted.

1. A written mapping of the three names for one role: "orchestrator" in issue 339 (the role that manages all sessions of a worktree), "orchestrator" in the design of PR 681, and "coordinator" in the contract (`src/superclaude/core/WORKER-CONTRACT.md` line 70 defines the coordinator as the Orca session the person opened). They are one role by function only after this mapping is written. <!-- Source: Debate transcript, A-001 - merged per Change #4 -->
2. The nine-rule script counts as the coordinator's act only if the automation is opt-in and the coordinator owns the schedule, the grant and the report. It does not count if the script becomes a way around the coordinator, or if the coordinator picks targets by judgment. The debate asked for an owner ruling on this. <!-- Source: Debate transcript, A-002 - merged per Change #4 -->
3. Closeout's writes need a named grant row, because the coordinator performs outward git and GitHub actions only when the user's instruction names the action (fact 6, `WORKER-CONTRACT.md` line 241). <!-- Source: Debate transcript, A-003 - merged per Change #4 -->

<!-- Source: Base (original) -->
## What it gets right

- Safety: the nine rules are mechanical, tested with fake `gh`, `git` and `orca`, and fail closed.
- Reuse: closeout's landed check, the PR-log opt-in and Orca automation pattern, `/sc:sweep` kept for sweeping.
- One job per tool: settle (closeout), remove (cleanup), report (log).
