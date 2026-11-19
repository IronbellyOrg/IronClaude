# Reviewer 3 card (persona refactorer, model class opus)

verdict: FAIL, self-reported calibrated_confidence 0.78. One blocking finding. The fix is one clause in each of two tasks; every other spec unit is covered.

## Findings

F1 severity=blocking at=plan:59 (Task 3) and plan:95 (Task 6). claim=Both tasks say to keep sentences that still say `full` is the default. After the change those sentences are false. The command file and the user guide would then give two different answers on the default the spec is changing. evidence=`src/superclaude/commands/issue.md:44` says "(an explicit `--pipeline full` is still required, even though `full` is the default)", and Task 3 says "Keep line 44 (`--submit` row) ... as they are". `docs/user-guide/commands.md:371` says "(write `--pipeline full --submit`, even though `full` is the default)", and Task 6 says "line 371 keep the `E-SUBMIT-NEEDS-FULL` sentence". fix=In Task 3, drop ", even though `full` is the default" from the issue.md:44 cell. In Task 6, drop the same clause at commands.md:371. Keep "an explicit `--pipeline full` is still required" and the STOP rule line unchanged. Add a test assertion that the clause is gone.

F2 severity=medium at=plan:34 (Task 1). claim=The rule does not say which wins when a bug's complexity or hours cannot be read. The spec says "bug -> full (all bugs, including complex)" and also "if type, complexity or hours cannot be read -> worktree". The plan lists the bug case first, so the model following it may pick either. The Task 5 test (plan:82) does not pin which one. evidence=source.md:1 quotes above; the template has separate `Complexity` and `Effort estimate` lines at `templates/issue-summary.md:8-9`. fix=Say in the new step that the unreadable check runs first (or that a readable bug always gives `full`), and have Task 5 assert that order.

F3 severity=medium at=plan:19 against plan:59,95,105,115. claim=The plan contradicts itself. Its Constraint says no other file restates the thresholds, but Tasks 3, 6, 7 and 8 copy "simple or medium feature of 16 hours or less" into issue.md, the user guide, both design notes and HOW-WE-WORK.md. That is five more copies of the thresholds, and no test checks they stay in step with claim.md. evidence=plan:19 says "do not restate the thresholds as a second rule"; plan:62 says "names the 16-hour line only once (in the row)". fix=Either reword the Constraint to allow a one-sentence outcome summary, or have issue.md, the user guide and HOW-WE-WORK.md say "picked from the issue (rule: `refs/claim.md` Wave 5)" without the numbers. Keep the full note only in the dated design-record amendments.

F4 severity=medium at=plan:34 (final output) and `refs/claim.md:145`. claim=On a re-claim, the new Wave 5 step prints a freshly worked-out `Level:` line. But an `already_launched` result reports the stored level (`SKILL.md:138`), and the two can differ (for example, first claim `--pipeline worktree`, re-claim with no flag on a bug). The plan adds the Level line only to the `launched` item. It does not say what the `already_launched` path prints, and it does not cover a failed worktree or a failed launch, even though the spec says "also in the final output". fix=In Task 1, say that for `already_launched` the final output prints the stored level instead of the Wave 5 line. Name what prints when the worktree or launch fails.

F5 severity=note at=plan:46 (Task 2). claim=The spec names SKILL.md line 92; the plan edits line 89 and never says line 92 is left alone on purpose. evidence=`SKILL.md:92` ends "`<L>` is the same level as in Wave 5.", which stays true. fix=One sentence in Task 2 saying line 92 needs no change.

F6 severity=note at=`docs/designs/sc-issue-claim-pipeline-flag.md:45`. claim=Decision P4, "The default stop is an approved plan.", is already out of date and gets no amendment note. Task 7 lists lines 21, 43, 66, 78, 274 and 87 only. fix=Add the new dated note inside the last cell of P4 as well.

F7 severity=note at=plan:34. claim=Moving the later Wave 5 steps down one line shifts claim.md lines after 81. The architecture reference cites `refs/claim.md:<line>` 10 times, and some of those cites are already wrong (it says `:118` for the Wave 8 launch line, which is now at 120). fix=Leave it out of this plan, or have Task 6 refresh those cites.

## Coverage

"also in the final output" (source.md:1) is only partly covered (F4). "bug -> full (all bugs, including complex)" set against "if type, complexity or hours cannot be read -> worktree" (source.md:1) has no order between them (F2). Everything else maps to a task, as the coverage matrix says.

## Checked

Step renumbering: nothing references the plan-boundary or launch-prompt step by number; the only numbered reference is `refs/chains.md:27` ("claim Wave 5 step 1"), and step 1 does not move; tests find Wave 5 by its text (`_wave(claim, 5)`, tests/skills/test_issue_protocol.py:434,447). Pinned tests: the st7 and st9 wording the plan keeps is the wording the tests assert (test_issue_protocol.py:431-468); the three tests expected to fail before they are updated are named correctly (test_issue_command.py:113, :182-194; test_issue_protocol.py:681-691). Return contract: the ten-field yaml at SKILL.md:123-134 is left alone. Wave 8: refs/claim.md:122 already says "`<L>` is the same level as in Wave 5." Watcher, guard, ship gate: only named as files not to touch; guard and ship-gate paragraphs (commands.md:382, refs/claim.md:135) are kept. Architecture reference: line 1557 edited, line 1635 left alone (correct). Design notes: existing "Amended 2026-11-18" notes sit inside the last table cell, so appending keeps the tables intact. Not checked: the plugin mirror file of HOW-WE-WORK.md.

## Calibration (blind, confidence-calibrator, sonnet)

calibrated_confidence: 0.80
self_reported_confidence: 0.78
calibrator_diversity: degraded
(details: ../artifacts/calibration.yaml)
