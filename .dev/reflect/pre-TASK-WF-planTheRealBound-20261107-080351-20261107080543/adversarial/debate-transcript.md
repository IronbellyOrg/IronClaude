# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe (see invariant-probe.md)
- Convergence achieved: 100% on 27 of 27 diff points (see Convergence Assessment; reviewed for sycophancy below)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (one per reviewer card; all three ran as sonnet-class general-purpose agents, so advocate-model diversity is NOT claimed)
- Condensation: Round 1 and Round 2 statements below are condensed records of the agent outputs (positions, concessions, evidence kept); full Round 1 text sat in the orchestrator's context and is summarized in round1-statements.md

## Round 1: Advocate Statements
See round1-statements.md in this folder (advocates for variants 1, 2 and 3; steelman, claimed strengths, weaknesses, concessions, shared-assumption responses, positions on X-001..X-003 and C-001, C-002, C-008). No advocate omitted a shared-assumption response (A-001, A-002, A-003 all answered by all three: A-001 QUALIFY x3, A-002 QUALIFY x3, A-003 ACCEPT/QUALIFY/ACCEPT).

## Round 2: Rebuttals

### Variant 1 advocate (first)
- Concedes C-001 is HIGH (was medium); R1-06 low; R1-07 stands; QA-3 still overstated.
- R1-01 holds only for the foreground-reparent shape (supervisor waits for descendants: launch-job-identity.sh:16-17, design:555); fix = run identify inside the same governed command.
- QA-4 is real for Task 2 criterion 1 (plan:47), Task 7 (plan:104) and Task 6; not for Task 3, Task 4 or Task 2's second criterion (plan:48, 58-59, 69).
- R3-F12 medium (10-14 runs against cap 12); keep R3-F8 for Task 5 only; fold R3-F13 into C-001; Task 8 needs a third state "superseded or not applicable (cite)".
- New evidence: live_probe.py:252 and :237; review-2.md:9, :12; design:563.

### Variant 2 advocate (second)
- Concedes QA-3 in part (line 59 names the overlap) and QA-2 (labelling); accepts recalibration to ~0.70; not conceded: "add a real case" is infeasible for PID reuse and reboot, so QA-1's per-case evidence class is preferred.
- Corrects rebuttal 1 on R3-F8: tests/hooks/test_launch_job_identity.py:1291-1354 already pushes from a governed job and a human in one real-Git clone (log: ordinary and governed, :1342-1354); the test's hook refuses (:1348) while Task 6's hook is log-only (plan:90).
- Final: C-001 high; QA-3 medium (wording: no criterion requires proof the old child stayed alive while the new session started, linked by PIDs and timestamps to run-status); QA-2 low (merge with R3-F11); third Task 8 state yes (low-medium); fold R3-F13 into C-001.

### Variant 3 advocate (last)
- Accepts narrower reading of R3-F1 (predetermined outcome, still a defect); adopts R1-01 for the reparent shape; accepts QA-1's per-case evidence class; R3-F8 holds for Task 6 (test :1291-1354).
- Final: C-001 high (medium if the plan states FAIL is expected); R3-F2 medium (ordering plus missing depth data); R3-F5 low; R3-F6 medium with the baseline requirement (basis INFERRED from the session snapshot); R3-F3 merged with QA-6 (medium); R3-F12 medium (~13 runs); R3-F13 folded into R3-F1; third Task 8 state yes.

## Scoring Matrix
| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | none (cosmetic) | 90% | Id scheme differences have no effect |
| S-002 | V1 | 80% | `verified_true_claims` block separates verified from inferred; V2/V3 accepted it as a strength |
| S-003 | none (all deviate) | 90% | No card uses the 4-class taxonomy; all three advocates conceded |
| C-001 | V3 (severity), V2 (fix) | 90% | All three concede high; fix = state FAIL is expected or define a per-case evidence class (plan:79, :119) |
| C-002 | V1 + V3 merged, with V2 linkage | 85% | Child cannot outlive the first process unless the plan says how (helper:16-17, design:555); QA-3 medium wording |
| C-003 | V1 | 85% | No run produces depth data (plan:31, :44, :104); dependency also wrong (plan:99) |
| C-004 | V1/V3 | 90% | identify() uses kernel session, no ancestry walk (helper:219-223, :253); Task 8 needs a third state (plan:118) |
| C-005 | V1/V3 | 90% | Boot identity compared at helper:234; Task 5 branch (plan:84) dead |
| C-006 | V1 | 85% | 10-14 runs against cap 12 (plan:22); medium |
| C-007 | V2/V3 | 90% | Label only; run identify inside the same governed command; low |
| C-008 | V1 | 90% | Foreground-reparent shape unobservable from a later call (helper:16-17, design:555); only that shape |
| C-009 | V2 (narrowed) | 85% | Real for Task 2 criterion 1, Task 7, Task 6 only |
| C-010 | V2 | 85% | Ledger holds exit status, not selector output (plan:31) |
| C-011 | V1 | 90% | live_probe.py:235-236, :252 disable persistence |
| C-012 | V1 | 90% | live_probe.py:237-240 offers only Bash |
| C-013 | V3 | 80% | Task 6 pusher origin and labelling unspecified; medium |
| C-014 | V3 (medium) | 80% | Baseline of blocked package needed; basis INFERRED (session snapshot) |
| C-015 | V1 | 70% | Orphan sweep; low |
| C-016 | V3 (low) | 75% | Settings checksum in plan:36 only; one clause in plan:120 fixes it |
| C-017 | V3 + V2 merged | 90% | Launch wrapper, hook/Git process trees, auto mode, decisive row missing from plan:114 (design:504) |
| C-018 | V3 (low) | 75% | Tests exist (test_launch_job_identity.py:1291-1354); cite or state what the task adds |
| X-001 | V3 | 90% | high |
| X-002 | merged | 85% | R3-F4 + R1-03 + QA-3 linkage |
| X-003 | both hold | 90% | feasibility (V1, reparent shape) and labelling (V2/V3) |
| A-001 | promoted | 85% | A prompt-driven run may not execute the exact command; source the selector line from the hook record, not the model's report |
| A-002 | stated | 85% | Carry the unavailable branch into Task 2 criterion 1, Task 6 and Task 7 |
| A-003 | stated | 85% | Merged selector (design 19.7) is the specification; F2.3/F2.6 describe the historical probe |

## Convergence Assessment
- Points resolved: 27 of 27 (S-001..S-003, C-001..C-018, X-001..X-003, A-001..A-003)
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 surface covered (S-001 to S-003, wording and labelling), L2 structural covered (C-003, C-004, C-017), L3 state mechanics covered (C-002, C-005, C-008): all three levels covered
- Status: BLOCKED_BY_INVARIANTS (diff-point agreement 100% and all three taxonomy levels covered, but Round 2.5 found 3 HIGH UNADDRESSED invariants: INV-001, INV-002, INV-003; depth standard has no Round 3, so the merge force-selects by score and records non-convergence)
- Unresolved points: none by position; residual severity disagreements settled in Round 2 (C-001 high, R3-F5 low, R1-06 low)
- Sycophancy check: unanimous 100% agreement on 27 points after only two rounds is suspicious by this protocol's own standard. Mitigations observed: the advocates ran as one model class (sonnet), so agreement may reflect shared bias; two advocates verified real files and one corrected the other on a factual point (test lines 1291-1354); several concessions were forced by file evidence (helper:234, helper:253). This is recorded as a limit, not as proof of correctness.
