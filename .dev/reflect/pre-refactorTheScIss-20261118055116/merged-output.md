<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (opus:refactorer) -->
<!-- Merge date: 2026-11-18T06:05:00Z -->
<!-- Non-base sources incorporated: V1 (changes 3, 4, 5), V2 (change 2) -->

# Merged reflection verdict (UC-1, plan TASK-WF-refactorTheScIss-20261118-054817)

verdict: PASS-WITH-GAPS (no blocking finding; one must-fix and four medium findings) <!-- Source: derived from the merged findings (change 1) -->

## Findings

M1 severity=medium (must-fix before execution) at=plan Task 3 (plan:59) and Task 6 (plan:95) <!-- Source: Variant 3 F1, severity reconciled per Change #1; Variants 1 and 2 -->
claim=Both tasks keep sentences that still say `full` is the default. After the change those sentences are false, so the command file and the user guide give two different answers on the default. evidence=`src/superclaude/commands/issue.md:44` "(an explicit `--pipeline full` is still required, even though `full` is the default)"; `docs/user-guide/commands.md:371` "(write `--pipeline full --submit`, even though `full` is the default)"; Task 3 says keep line 44; Task 6 says keep line 371. fix=In Task 3 drop ", even though `full` is the default" from the issue.md:44 cell; in Task 6 drop the same clause at commands.md:371; keep "an explicit `--pipeline full` is still required" and the STOP rule and its quoted message; add to Task 4 an assertion that the clause is gone from issue.md.

M2 severity=medium at=plan Task 1 (plan:34) and Task 5 (plan:82) <!-- Source: Variant 3 F2 with Variant 1 F3 test shape, Change #4 -->
claim=The new Wave 5 step does not say which rule wins when a bug's complexity or hours cannot be read ("bug gives full" against "unreadable gives worktree"). The planned Task 5 test checks only that each sentence exists and where the step sits. evidence=source.md:1 "bug -> full (all bugs, including complex)" and "if type, complexity or hours cannot be read -> worktree"; `templates/issue-summary.md:7-9`. fix=State in Task 1 that the unreadable check runs first (a bug with an unreadable Type, Complexity or hours gives `worktree`; Type unreadable means no bug rule applies), and have Task 5 assert the index order of the two sentences.

M3 severity=medium at=plan Task 1 (plan:34) <!-- Source: Variant 3 F4 extended; fix text from Variant 1 F2, Change #3 -->
claim=The new `Level:` line is worked out in Wave 5, before the claim knows whether the launch is `already_launched`, a failed worktree or a failed launch. The stored level wins for `already_launched` (`SKILL.md:138`), and the two can differ; the plan says nothing about what prints in these cases. evidence=`refs/claim.md:116-122`, `:145`, `SKILL.md:138`, source.md:1 "the already_launched re-claim path still reports the stored level". fix=In Task 1 say: the `Level:` line is printed with the launch result for `launched` only; for `already_launched` the final output prints the stored level instead; for a failed worktree or a failed launch the final output prints no `Level:` line (the launch result names the failure). Pin one phrase in Task 5.

M4 severity=medium at=plan Task 5 (plan:82) <!-- Source: Variant 2 F1, Change #2 -->
claim=Task 5 pins the `Level:` line in Wave 5 but nothing pins that the final output repeats it; deleting that instruction leaves every planned assertion green. evidence=`tests/skills/test_issue_protocol.py:687-691` checks only the worktree and full continuation wording. fix=Add an assertion on the `launched` item's Level-line instruction and a mutation check that removes it.

M5 severity=medium at=plan Constraints (plan:19) against Tasks 3, 6, 7, 8 (plan:59,95,105,115) <!-- Source: Variant 3 F3, reworded per Change #6 -->
claim=The Constraint says the thresholds are authored once, yet the outcome sentence with the numbers is copied into five more files and nothing checks they stay in step with `refs/claim.md`. This is a drift risk with no test, not a direct contradiction. fix=Reword the Constraint to allow a one-sentence outcome summary with the numbers once per file, and say the full rule lives only in `refs/claim.md`.

M6 severity=note at=plan Task 2 (plan:46) <!-- Source: Variant 3 F5 and Variant 1 coverage note -->
claim=The source names `SKILL.md` line 92; the plan edits lines 17, 89 and 138 and never says line 92 is left alone on purpose. fix=One sentence in Task 2: line 92 already says "`<L>` is the same level as in Wave 5." and needs no change.

M7 severity=note at=plan Task 1 (plan:38) <!-- Source: Variant 1 F4, Change #5 -->
claim=`-k "st7 or st9 or worker_contract"` names one file, so `worker_contract` selects nothing from it. fix=Drop `worker_contract` from the `-k` expression; the worker-contract check is already its own bullet.

M8 severity=note at=`docs/designs/sc-issue-claim-pipeline-flag.md:45` <!-- Source: Variant 3 F6 -->
claim=Decision P4 ("The default stop is an approved plan.") is out of date and gets no amendment note; Task 7 lists lines 21, 43, 66, 78, 274 and 87 only. fix=Add the dated note inside the last cell of the P4 row.

M9 severity=note (follow-up candidate, outside this plan) at=`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` <!-- Source: Variant 3 F7, Change #7 -->
claim=The architecture reference cites `refs/claim.md:<line>` eleven times and some cites are already stale (`:118` for the Wave 8 launch line, now at 120); inserting a Wave 5 step shifts the lines after it again. fix=Leave out of this plan, or refresh the cites in a separate change.

## Coverage

16 of 16 inferred requirements map to a task, with two partly covered units: "also in the final output" (M3, M4) and the rule order (M2). <!-- Source: Variant 3 coverage section; Variant 2's "all 16 covered" not carried over -->

## Checked

Step renumbering is safe (the only numbered reference is `refs/chains.md:27`, "claim Wave 5 step 1", and step 1 does not move; tests find Wave 5 by text). The st7 and st9 pinned wording the plan keeps is the wording the tests assert. The watcher, guard and ship-gate text are only named as files not to touch. Unverified: no test was run by any reviewer; `HOW-WE-WORK.md` plugin mirror was not read by the base variant. <!-- Source: Variant 3 checked list -->
