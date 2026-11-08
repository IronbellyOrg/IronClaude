
## Scoring Matrix

Winner determination by the orchestrator (sonnet class) from the two Round 1 statements and the evidence each cites; "Agreed" = both advocates gave the same answer. No Round 2 exists, so no concession boost applies beyond what the advocates conceded in Round 1.

| Diff point | Advocate 1 | Advocate 2 | Agreed | Winner | Confidence | Evidence summary |
|---|---|---|---|---|---|---|
| S-001 | tie (96) | 2 (55) | no | tie | 60 | section order does not decide any substantive finding |
| S-002 | 2 (99) | 1 (60) | no | tie | 60 | variant 1's "Drift" category violates the brief (reviewer-briefs/reviewer-1.md:3, conceded); variant 2's hedged severities are off the HIGH/MEDIUM/LOW scale (conceded); merged output uses the three-level scale only |
| S-003 | 2 (94) | 2 (85) | yes | variant 2 | 90 | one verdict per Tier 1 defect is auditable; both advocates agree |
| C-001 | tie (95) | tie (55) | yes | tie | 85 | merge A-01's self-check with Q-6's recorded-pid stop |
| C-002 | 1 (98) | 1 (85) | yes | variant 1 | 92 | help file lines 131-132 verified by the calibrators and both advocates |
| C-003 | tie (90) | 2 (60) | no | variant 2 | 70 | Q-1 gives the ordered calls and expected statuses; Q-7 the fork status (help:104-106, helper:435-437); advocate 1 conceded Q-1 is more concrete; A-03's different-controller point is kept |
| C-004 | 1 (96) | 2 (65) | no | tie | 60 | complementary: tree-edge capture (variant 1) and a bounded wrapper/auto-mode observation or "not run" label plus a real governed Git push (variant 2) |
| C-005 | 2 (98) | 2 (75) | yes | variant 2 | 90 | plan:55 and plan:31 produce outcomes that are not a missing interface; a "not observed (reason)" row category is needed |
| C-006 | 1 (91) | 2 (60) | no | tie | 55 | INF-003 Partial (both /clear topology and reparenting unproven); INF-001, INF-002, INF-008 covered with defects tracked as findings |
| X-001 | 1 (99) | 2 (60) | no (conclusions agree) | tie | 75 | both agree thirteen starts are not forced (plan:22 shares four shapes across three starts); both agree the ledger cannot be audited against the cap without a run id; variant 2's one-case-id-per-line reading is plausible but not forced |
| X-002 | 1 (91) | 2 (60) | no | tie | 55 | see C-006 |
| A-002 | QUALIFY | QUALIFY | yes | QUALIFY | 85 | adapter keys on the event's session id (helper:429-437); fork gets a new id (help:104-106); /clear unverified |
| A-003 | REJECT | QUALIFY | no | QUALIFY | 70 | the plan specifies the refusal path (plan:22, :31) but an executor started inside Claude Code risks an empty FAIL (value risk) |
| A-004 | QUALIFY | QUALIFY | yes | QUALIFY | 85 | caps bind the executor; the owner can choose before execution |
| A-005 | REJECT | QUALIFY | no | QUALIFY | 65 | static reading suffices for textual contradictions, not for runtime behaviour |

## Convergence Assessment

- Points resolved: 6 of 15 with an identical advocate answer (S-003, C-001, C-002, C-005, A-002, A-004) = 40.0% strict; counting X-001, where the advocates' substantive conclusions match and only the framing of the "winner" differs, 7 of 15 = 46.7%.
- Threshold: 80%
- Status: NOT_CONVERGED (the depth is quick, so no rebuttal round could close the gaps; no HIGH unaddressed invariant gate applies because Round 2.5 was skipped)
- Unresolved points: S-001, S-002, C-003, C-004, C-006, X-001, X-002, A-003, A-005
- Reading the result: no unresolved pair is mutually exclusive. S-001 and S-002 are presentation; C-004 and C-006/X-002 are complementary or a judgement about what "Partial" means; X-001's facts are agreed. The merged verdict therefore takes the union of the valid findings, with the resolutions in the scoring matrix. A standard-depth run would add rebuttals and the invariant probe; it was not run.
