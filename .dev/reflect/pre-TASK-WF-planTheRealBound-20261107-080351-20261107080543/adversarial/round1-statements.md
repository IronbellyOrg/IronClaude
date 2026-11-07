# Round 1 statements (condensed record of the three advocate outputs; positions and concessions kept, prose shortened)

## Advocate for variant 1 (analyzer, sonnet)
Position: V1 is the only card that checks the plan against the merged helper and the live probe; its main claims hold (supervisor waits for descendants, persistence flags block resume, Task 7 has no data source). It rates PASS-unreachable too low, overgeneralizes R1-01, and misses plan-wording gaps V2 and V3 catch.
Steelman of V2: evidence criteria too loose to stop self-deception (QA-5, QA-3); QA-2 right that a second Bash call in a governed session is governed (design:551); QA-4 right that Task 2's same-worktree criterion and Task 7 have no unavailable branch; QA-6 right that design:504 lists the launch wrapper and plan line 114 omits it.
Steelman of V3: the gate is rigged (Task 8 line 119 vs Task 5 line 79); R3-F3, R3-F5, R3-F13, R3-F8, R3-F9/F10 are right.
Weaknesses claimed: V2 never tested the plan against code; QA-3 overstated (plan line 59 already says "stays alive while"); QA-4 partly overreaches (Task 3 line 58, Task 4 line 69, Task 2 subagent/Monitor line 48 already accept unavailable; holds only for Task 2's same-worktree criterion and Task 7); V3's PASS fix collides with R3-F4 and R3-F12; R3-F2 is a partial fix (no run produces depth data); R3-F5 medium is too high; R3-F8/R3-F13 are not defects.
Concessions: R1-01 overgeneralizes (true for the foreground-reparent shape only; run_in_background, setsid and killed-supervisor return); R1-04 should be high; V1 misses QA-5, QA-4, R3-F3/QA-6, R3-F5; five findings typed `other`; R1-10/11/12 are low value; :427 and :102-106 not re-verified.
Shared assumptions: A-001 QUALIFY (literal single-command prompts work, design:563; multi-step prompts in Tasks 3-4 unproven; check hook events); A-002 QUALIFY (Task 2 same-worktree and Task 7 lack an unavailable branch); A-003 ACCEPT.
Positions: X-001 V3 right (high). X-002 R1-03/R3-F4 right, QA-3 an add-on. X-003 both hold. C-001 V3 severity plus V1 fix. C-002 V1 most complete. C-008 V1 right for the reparent shape only; fix is to run identify inside the same governed command.

## Advocate for variant 2 (qa, sonnet)
Position: smallest card, only one testing whether acceptance criteria could pass on fabricated or weaker evidence (QA-3, QA-5) and whether the unavailable path can finish (QA-4); never questions whether the tasks can run.
Steelman of V1: supervisor wait (:16-17, design:555) makes Task 4 reparent and Task 3 keep-alive infeasible; live_probe flags would make resume/fork and subagent/Monitor unavailable by the plan's own doing (R1-02, R1-09); separates verified from inferred.
Steelman of V3: B-CTX fixed at FAIL in advance (R3-F1); R3-F5 settings checksum; R3-F8 overlap with existing tests; R3-F13; R3-F9/F10.
Weaknesses claimed: R1-04/R3-F1 "add a real case" is infeasible for PID reuse and reboot (QA-1's per-case evidence class is more complete); R1-06/R1-07/R3-F9/R3-F10 low value (dead branches harmless; R1-06 medium too high); R1-03 rests on an unverified speculation; R1-11/R3-F6 inferred from the session snapshot; R3-F8 argues against tasks kept on purpose; V1/V3 never ask whether Task 3 could pass without testing the decisive case.
Concessions: QA-3 partly overstated (line 59 names the overlap; the gap is no criterion demands linked proof; "fabricable" too strong); QA-2 is a labelling point (identify classifies the target's kernel session, :219); QA-1 medium arguably too low; QA misses supervisor wait, persistence flags, run cap, tool list, Task 7 dependency; lowest calibration.
Shared assumptions: A-001 QUALIFY; A-002 QUALIFY; A-003 QUALIFY (F2.1/F2.2/F2.6 need observation; F2.3/F2.4 can cite static reading).
Positions: X-001 V3 on effect, plan permits FAIL so hold medium; X-002 all needed; X-003 both hold; C-001 all right, V3 severity, QA-1 fix; C-002 fix needs how-child-stays-alive plus linked overlap capture; C-008 V1 right for foreground-reparent only.

## Advocate for variant 3 (refactorer, sonnet)
Position: best-calibrated top finding (R3-F1) and best plan-versus-source reconciliation; thinner than V1 on run feasibility and than V2 on evidence linkage. Merged review should take V3's severity ordering, V1's feasibility findings and V2's linkage findings.
Steelman of V1: plan's real-run tasks cannot work as written (probe flags, supervisor wait, Task 7 data source). Steelman of V2: ledger holds no selector output (QA-5), no unavailable branch (QA-4), QA-3's overlap-interval tightening is right, QA-6 confirms R3-F3.
Weaknesses claimed: QA-1 miscategorised as "contradiction" (line 119 defines FAIL as fallback; it is a predetermined outcome); QA-3 overstated; V2 miscalibrated (0.94 self vs 0.70); V1 R1-05/R1-06 ask for a second Task 8 state though Task 7 (line 105) already has not-applicable (residual gap: Task 8 line 118 offers only closed/open); R1-12 partly redundant with cleanup logs; V1/V2 miss R3-F13, R3-F5, R3-F6.
Concessions: R3-F4 missed Task 4 (C-008); missed R1-02, R1-09, QA-4, QA-5; R3-F2 weaker than R1-05; R3-F12 should be medium; R3-F6 and R3-F13 partly inferred; no card uses the 4-class taxonomy (own findings informally: Drift R3-F1/F3; Necessary deviation R3-F6; Authorized expansion R3-F8).
Shared assumptions: A-001 QUALIFY (name the hook record as the selector-line source); A-002 QUALIFY; A-003 ACCEPT.
Positions: X-001 V3 right, becomes medium only if the plan states FAIL is expected; X-002 R3-F4 plus R1-03, merge QA-3's linkage; X-003 both hold; C-001 V3 severity; C-002 high on consequence; C-008 V1 right and V3 missed it.

## Round 1 convergence note
All three advocates give the same winner or both-hold on X-001, X-002, X-003, C-001, C-002, C-008. Remaining open: severity of PASS-unreachable (high vs medium), whether QA-4 is complete or partly overreaching, severity of R3-F12, R3-F5 and R1-06, and the value of R3-F8/R3-F13.
