# T1 reflection card (UC-1, pre-execution), third review of plan TASK-WF-blockerStage1-20261116-030154

Written inline by the orchestrator (the `root-cause-analyst` fallback of the protocol). Evidence: `artifacts/wave1a-checks.md`. `PLAN:n` = line n of the plan file `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`; `SPEC:n` = line n of `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`; `STAGE2:n` = line n of `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md`.

## Coverage (Step 1B)

Pass 1 found 9 parsed rows: R-001 to R-008 are recommendation labels of the first two reviews (false positives of the ID regex, source.md lines 26 to 50) and REQ-09 is a real spec requirement (Task 7 names it, PLAN:124). Pass 2 (requirements-analyst) gave 84 quote-pinned rows; 35 lie inside a parsed span (parsed wins) and 49 were kept; containment matched 38 of 49; the 11 misses are mapped by hand in `artifacts/inferred-table.md` (every one is a Constraints line or a provenance line). `coverage_pct` (parsed only) 0.1111, `coverage_pct_union` 0.6724, `S_dev_density` 0.3276; the parse-density guard fires (49 inferred > 9 parsed).

## Earlier findings (first review F1 to F9, second review M-F1 to M-F10): all fixed in the live text

| Finding | Where it is fixed now |
|---|---|
| F1, M-F1 (Task 7 grep lists `.pyc`) | PLAN:129: `grep -rln --include='*.py' --exclude-dir=__pycache__ "follow_ups" src/superclaude/cli/review`, "lists no file other than" in both sentences, with the end point "until the stage 2 package adds its own importer" |
| F2, F3 (stoprule row, allow-list) | PLAN:64, 66, 70 (`installed-only` row, 12 keys, allow-list holds `remediate_parser.py` and `fmea_classifier.py`) |
| F4 (ledger decision) | PLAN:124, 248, 22 |
| F5, M-F2 (scale-map grammar) | PLAN:62 (family key, `LABEL=Outcome` pairs, `Conditional` token, ` + ` separator, `none`), PLAN:151 (lookup key, UNSET for unknown family, unlisted label, `Conditional`), PLAN:234 (T4 splits ` + `) |
| F6, F7 (dependencies, `run_questions`, `questions_to_ask`) | PLAN:164 (Depends on 7, 9), PLAN:151, PLAN:166, PLAN:204 (Depends on 7, 9) |
| F8, F9 | PLAN:52 (full path), PLAN:192 (seven subcommands named, `lint` and `estimate` have no module: confirmed), PLAN:82 (`sweep-flagged` as a ninth state) |
| M-F3 (REQ-09) | PLAN:124 (`earlier_decisions`) |
| M-F4 (M and D inputs) | PLAN:166 (`absent-by-name` precheck, decision-basis excerpts, Option Q) |
| M-F5 (verdict store) | PLAN:192 (`classifier-results.json`, `update_field`), PLAN:124 |
| M-F6 (resolver) | PLAN:137, 141 (injected resolver, by-path load; `read_origin` confirmed) |
| M-F7 (paths in new refs) | PLAN:82, 90, 99-100, 115 (greps) |
| M-F8 (Task 1 order) | PLAN:36 |
| M-F9, M-F10 | PLAN:192 (`verify-citations`), PLAN:52, 72 (count 9, matches the live grep), PLAN:151 (name off `THRESHOLDS`), PLAN:131, 160, 173, 200, 213 (`make lint`) |

## Findings of this review (provisional, T1)

- **T1-F1 (non-blocking).** PLAN:124 asks for a test that `earlier_decisions` "does not return a `pending` row", but `pending` is not an item state: the item states are `recorded`, `offered`, `resolving`, `resolved`, `filed`, `declined`, `duplicate`, `superseded` (SPEC:381-390) plus `sweep-flagged` (PLAN:82); `pending` is a state of the Offers table (SPEC:375). The executor must guess which row to use (likely `recorded` or `offered`).
- **T1-F2 (non-blocking).** The consent binding of REQ-11 (SPEC:421-428; Offers table with `set_digest`, `answer`, `state`, SPEC:375) has no code owner. Task 7 (PLAN:124) lists no Offers table logic and Task 8 (PLAN:137) builds only the Filings table, yet Task 8 must test "a resume asks again" and "a changed set is filed without new consent" (T8, SPEC:923). The tests have no function to call unless the executor invents an offer object.
- **T1-F3 (non-blocking).** Task 10 (PLAN:166) supplies the NA marker for M only. REQ-19 (SPEC:528) lets NA stand for M and for C, but no task supplies the "kind declared to have no constraint list" marker, so C is UNSET for every finding without constraint lines, and REQ-18 (SPEC:543) then lifts every such verdict to SHOW_USER; the classifier will say SHOW_USER for most non-spec deliverables in stage 2.
- **T1-F4 (non-blocking).** Task 3 (PLAN:62) names the lens-scale row but gives no outcome values for CRITICAL, IMPORTANT and MINOR, and the spec says only that the label is information (SPEC:737). Stage 2 Task 2 (STAGE2:57) sets the tier of every imported row from that row, and `ReviewerJudge` (PLAN:151) returns UNSET for a `Conditional` label. If the executor writes `Conditional` for all three, stage 2 gets no tier for any row.
- **T1-F5 (minor).** STAGE2:27 still quotes the old stage 1 wording ("only the new module and its command wiring mention `follow_ups`"); PLAN:129 now says something different with an end point. The stage 2 sentence is harmless (it says the line describes the end of stage 1) but quotes text that no longer exists.

No finding rises to blocking: every task is reachable in order, every dependency points to a lower number, every acceptance check I ran can pass on the current repository, and no cross-stage name differs.

## Verdict candidate

PASS with notes, confidence moderate (the plan was fixed twice and the checks I ran agree; reviewers may find defects in the prose of the large tasks that a count-and-grep pass cannot see).
