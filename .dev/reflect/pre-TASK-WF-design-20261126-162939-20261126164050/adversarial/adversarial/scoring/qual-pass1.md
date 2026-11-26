# Qualitative scoring, PASS 1 (V1, V2, V3 in input order)

Cards: V1 = reviewer 1 (analyzer, 16 rows), V2 = reviewer 2 (qa, 10 rows), V3 = reviewer 3 (refactorer, 15 rows + 1 advisory). Evidence from the cards, the debate files and spot checks of PLAN lines 20-31 and DESIGN:156,192. Claims the debate showed false are not used as MET evidence.

| id | V1 | V2 | V3 |
|----|----|----|----|
| C1 | 1 - "Spec units audited: 38 plan tasks, DD-1 to DD-11, invariants I1 to I9, and the 29 ids" | 1 - "Read all 38 task bodies"; table "Design sections 3 to 8 and 10" maps each to tasks | 0 - "Not checked: FR-024 to FR-029, FR-037, ... NFR-013, NFR-015"; "Not verified: the full text of Tasks 13-18"; no design-section map |
| C2 | 1 - row 4 `reason=empty`/`mixed-authorization` skip; row 11 `git gc --prune=now` between crash and resume | 1 - row 3 crash after resolution append, resume twice; row 7 no-sidecar case | 1 - row 6 header-only ledger and `ARCHIVE: failed` tail at the archive gate |
| C3 | 1 - row 1 Task 19 acceptance needs Task 20's file; row 16 incomplete `Depends on:` lines | 1 - Notes: "F2 confirmed, not a blocker for this executor (source order)" (but it missed the Task 19/20 order defect) | 1 - row 2 Task 19 vs Task 20; row 15 incomplete `Depends on:`; row 12 line anchor shifts after Task 26 |
| C4 | 1 - "Blocking: 4 (rows 1-4)"; row 3 fix check `test ! -e commands/sc-git.md` | 1 - "Reviewer verdict: FAIL (contradictory checks and acceptance gaps)" | 1 - "Reviewer's recommended action: fix rows 1-9 before `/sc:implement`" |
| C5 | 1 - "Unread: `refs/ledger.md` lines 127 and 139 in context"; UNVERIFIED list | 1 - "No tests or commands were run ... UNVERIFIED" | 1 - "Not verified:" list; "Not checked:" ids; "No tests were run" |
| K1 | 0 - row 14 says design 4.3 field list lacks `hooks_path` (DESIGN:192 lists it); "Fully adherent: 23 tasks" overclaimed (Task 9 reader defect missed, conceded) | 0 - FR-109 and T-14/AC-13 called covered (refuted); "no implementation instruction" for the 40-line cap withdrawn | 0 - row 1 premise "early copy ... reserves for Task 38" ignores PLAN:24 (conceded); coverage line says NFR-014 covered by Tasks 4, 29 (conceded false) |
| K2 | 1 - row 2 fix: reword to "no argv the code runs ... deny-lists and refusal tests are allowed" | 1 - row 1 "Limit the prohibition to executing or recommending bypasses" | 1 - recommended action: copy each file to the plugin in the same task; move S23 edit into Task 20 |
| K3 | 0 - "Regression" used for rows 1, 3, 5 (conceded a stretch); non-standard "Regression (internal conflict)" | 0 - six rows "Blocking" with MEDIUM label; "Regression" for PLAN:29 (withdrawn) | 1 - taxonomy used as defined (S-002 voted V3 by all advocates); "Authorized expansion" fits row 13 |
| K4 | 0 - summary "Drift 14 ... Regression 2" but rows 1, 3, 5 are Regression (3); 17 tasks with findings leaves 21, not "23", adherent | 0 - FR-109 "covered" vs its own rows 3, 6, 7 reporting FR-109/T-21/T-04 gaps; "Blocking" text vs MEDIUM label | 0 - Task 17 listed "fully adherent" yet row 11 cites PLAN:213 (Task 17); row 9 "Blocking" with MEDIUM label |
| K5 | 1 - every row has an Evidence cell with file:line (e.g. row 1 `test_routing_refresh.py:101-107`, `:483-496`); unknowns marked UNVERIFIED | 0 - coverage dispositions asserted without evidence, key claims refuted (FR-109, 40-line cap); no existing test read | 1 - evidence per row (e.g. row 3 `test_task_workspace_lifecycle.py:611, 682-688`); "No tests were run" disclosed |
| S1 | 1 - Deviations, Adherence summary, The 29 ids, Notes | 1 - Deviations, Unmapped IDs, Design sections, Summary, Notes | 1 - Deviations, Correctness gaps, Adherence summary, Notes |
| S2 | 1 - H1, H2 sections, one H3 ("The 29 ids") under the summary | 1 - H1 then five H2 sections | 1 - H1 then four H2 sections |
| S3 | 1 - findings table, summary and notes in separate sections | 1 - findings, coverage tables, summary and notes separated | 1 - findings, "Correctness gaps (advisory, non-gating)", summary, notes separated |
| S4 | 1 - numbered rows #1-16; Notes cite "row 2", "row 16" | 1 - numbered rows #1-10; coverage tables cite "row 9", "rows 4, 8" | 1 - numbered rows; "fix rows 1-9"; gap table cross-cites Tasks 3, 15, 16 |
| S5 | 1 - header, `Total deviations`, 6-column table, adherence summary, notes | 1 - same header and table plus verdict and adherence summary | 1 - same header and table plus advisory table and adherence summary |
| L1 | 1 - grade and label agree on all 16 rows (S-003 voted V1); each row names action and fix | 0 - "Blocking" grade against MEDIUM label on rows 5-10 leaves severity unclear | 0 - row 9 "Blocking (Decision)" with MEDIUM label; "Fully adherent: 20 ... mostly checked" |
| L2 | 1 - cites exact lines, tokens, files (e.g. Task 14's seven tokens, "five" in the acceptance) | 1 - cites PLAN/DESIGN lines and names the missing assertion (row 2 person-only authority) | 1 - cites exact tests and lines (`test_workflow_command.py:204-220`) |
| L3 | 1 - each section has a stated job (deviations, adherence, 29 ids, notes) | 1 - each table has a stated job (unmapped IDs, design sections) | 1 - each section has a stated job (deviations, advisory gaps, summary) |
| L4 | 0 - FR-, NFR-, DD-, T-, I-, Q0, S23 ids used without definition; only PLAN/DESIGN/REQ defined | 0 - same undefined ids; only paths defined | 0 - same undefined ids; only paths defined |
| L5 | 1 - "Fix:" in rows 1-3; row 12 suggests merge-base comparison; rows name the affected action | 0 - fix stated only in rows 1 and 5; no action section, only "FAIL" | 1 - "Reviewer's recommended action" lists nine concrete repairs |
| R1 | 1 - rows 1-4 Blocking HIGH, rows 5-13 Medium (grade as impact) | 1 - rows graded Blocking with HIGH/MEDIUM labels | 1 - rows 1-9 Blocking, 10-12 Medium, 13-15 Note |
| R2 | 0 - fix given only for rows 1-3 and 12; rows 4, 5, 7-11, 13 have none | 0 - fix only in rows 1 and 5 | 1 - recommended action gives a repair for every Blocking row 1-9 |
| R3 | 1 - row 1 "Affected action: Task 19's acceptance run and any gate between Tasks 19 and 20" | 0 - no execution-time consequence stated; only "checks pass while text is absent" | 1 - "Affected action: QA verdicts of Tasks 26, 27, 30, 31, 34"; "False failures: a fresh legacy ledger ... at Wave 0 step 6b" |
| R4 | 1 - existing tests, `origin/integration` resolution UNVERIFIED, `.gitignore` entry (row 8) | 1 - `tests/worktree_cleanup/test_git_facts.py:217`; "hook-framework behavior, git version floor and CI submodule behavior remain UNVERIFIED" | 1 - byte-parity, `_TRANSIENT` and ledger tests; `verify-sync` and `--strict-markers` flagged unverified |
| R5 | 1 - row 3 fix check: `test ! -e commands/sc-git.md` plus the work-tree count | 0 - no check named that would show a fix worked | 1 - "use filesystem checks in Task 25"; "add the `_TRANSIENT` test update to Task 31" |
| E1 | 1 - row 4 `reason=empty` boundary and a mixed batch with no recording action | 1 - row 7 no-flag/no sidecar case; row 9 40-line refusal-log cap | 1 - row 6 header-only legacy ledger as a valid last line |
| E2 | 1 - row 9 15-line `SKILL.md` budget spent by Task 26 and again by Task 30; row 12 unchanged-file proofs | 1 - row 3 outside-change pins preserved across crash, resume and both answers; row 5 vs Task 1 reserved files | 1 - row 12 Task 26 inserts shift Task 30's line-129 anchor |
| E3 | 1 - row 8 `.dev/implement/` exclusion unguarded; row 5 allow-list vs private index | 1 - row 4 legacy-path exclusion missing; row 2 authority checks absent | 1 - row 9 archive gate calls `vcs reconcile` with no `commits.md` guard |
| E4 | 1 - row 7 "seven refusal tokens listed ... acceptance says 'each of the five'" (verified in debate) | 0 - no count divergence in the plan reported | 1 - row 14 `README.md:9` "(parity tests check these four)" should name five |
| E5 | 1 - row 5 Task 3 `FORBIDDEN_FLAGS` `-A` vs Task 15's `add -A` private-index snapshot | 1 - row 1 Constraint line 29 vs Tasks 3 and 29 | 1 - Tasks 26-34 byte-parity vs Task 38 copy timing; row 10 Task 34 check vs Task 37 docs |

## Subtotals per dimension

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness (C1-C5, of 5) | 5 | 5 | 4 |
| Correctness (K1-K5, of 5) | 2 | 1 | 3 |
| Structure (S1-S5, of 5) | 5 | 5 | 5 |
| Clarity (L1-L5, of 5) | 4 | 2 | 3 |
| Risk Coverage (R1-R5, of 5) | 4 | 2 | 5 |
| Invariant and Edge Case (E1-E5, of 5) | 5 | 4 | 5 |

## Totals (out of 30)

- V1: 25
- V2: 19
- V3: 25
