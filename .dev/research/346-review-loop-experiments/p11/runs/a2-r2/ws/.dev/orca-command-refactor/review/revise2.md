# Revision 2: orca-worker-contract-spec.md

Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
Input findings: `.dev/orca-command-refactor/review/round2.md:173-175` (Reviser brief: blocking id B3; S:154 and the rows are not to be edited; do not act on M14 to M18, M1 to M13 or N1 to N12).
Contract kept: only text B3 names was revised (the clause "in the phase its row names" at S:76 and AC-1.1 at S:195); no rule, mechanism or section was added that B3 does not call for; no line was added or removed; no PASS is claimed. Citations to the candidate are `S:N`; to the report `R2:N`.

## Byte accounting

Candidate size (`wc -c`): before 58349 bytes, after 58510 bytes, net +161 (58349 + 161 = 58510). Both figures match `wc -c` run in the sandbox; line count unchanged (285).

| Finding id | Bytes added | Bytes deleted | Net | Lines edited |
|---|---|---|---|---|
| B3 | 534 | 373 | +161 | S:76, S:195 |
| Total | 534 | 373 | +161 | |

Per edit (method as in revision 1: each replaced phrase counts as deleted in full and added in full, measured as `len(s.encode())` on the exact old and new strings): S:76 added 124, deleted 61 (net +63); S:195 added 410, deleted 312 (net +98). The edit-level sums reconcile with the `wc -c` readings. Of the S:76 text, only the clause "; brainstorm and init-lite, whose rows name none, gain it in P1" is new. The other words of the replaced phrase are unchanged.

## Disposition table (one row per finding id)

| Id | Disposition | Where applied (candidate line) | Reason and citation |
|---|---|---|---|
| B3 | Applied, option "phase-scope AC-1.1" | S:76: after "in the phase its row names" added "; brainstorm and init-lite, whose rows name none, gain it in P1". S:195 (AC-1.1): the test asserts the section on every command whose section is due in P1 under section 3 (the rows naming P1, plus brainstorm and init-lite); the sections due in P2, P3 and P4 (the last after D2-D4) are asserted in the check of the phase their row names; the test asserts that `load` and no section-4 command has one. The earlier wording (all of 3.1-3.2 except `load` and the three P4 commands) is replaced. | R2:116-122 (finding and recommendation). The contradiction was that S:76 schedules 15 sections in P2 and 4 in P3 while AC-1.1 asserted them at P1 and S:154 holds P2 closed until P1 passes (R2:117, R2:119, R2:121). Phase-scoping AC-1.1 leaves S:76 and S:154 and every row as they were and removes the mismatch; the other option (delete the clause from S:76) would have put a section for a P2 gate (for example auggie-review's `--no-post-pr` default, S:100) into P1 before the P2 conversion (S:160), so it was not chosen. Result: P1 asserts 14 sections, 8 phase-P1 rows of 3.2 (analyze, build, business-panel, design, document, explain, index, test; S:99-123), 4 P1 fixes of 3.1 (adversarial, cleanup-audit, index-repo, workflow; S:83, S:85, S:86, S:92) and brainstorm and init-lite (S:84, S:87), the pair named in B3 (R2:120). `load` stays excluded in both S:76 and S:195 (S:112, S:265 unchanged). The P4 exemption of implement, post-release and pr-submit from the first revision is kept in substance ("the last after D2-D4"). |
| M14 to M18 | Not acted on | none | R2:175 (Reviser brief). |
| M1 to M13 | Not acted on | none | R2:175. |
| N1 to N12 | Not acted on | none | R2:175. |

## Notes for the next reviewer

- Untouched by design (brief): S:154, S:159 and all rows of sections 3.1, 3.2 and 6. S:159's command list for P1 does not name brainstorm and init-lite; it applies the `--unattended` flag to "every command in sections 3.1 and 3.2", so P1 already touches them. This was left alone.
- Consequence the reviewer may weigh (M18 territory, not acted on): the check that asserts the P4 sections still does not exist among AC-4.1 to AC-4.3, and S:195 now says they are asserted "in the check of the phase their row names". Likewise AC-2.1 and AC-3.1 do not literally say they extend the section assertion. Not changed, because no blocking finding names those lines.
- Candidate sections read for this revision: S:60-204 of the candidate; evidence for phase membership is S:83-92 and S:99-125 in the spec itself. Inventory files were not needed for B3; no citation outside the workspace is made. `rf-qa` and the spec-panel were not run.
