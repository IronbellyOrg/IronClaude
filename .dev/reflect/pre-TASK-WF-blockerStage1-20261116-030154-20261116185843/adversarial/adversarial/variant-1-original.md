persona: analyzer
model_class: sonnet
model: claude-gw-tier1b[1m]
model_observed: claude-gw-tier1b[1m] (self-report of the reviewer; matches the pin)

`PLAN:n` = line n of `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`; `SPEC:n` = line n of `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`; `STAGE2:n` = line n of `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md`. Card text below is the reviewer's hand-back, saved verbatim (de-indented).

## Findings

**R3-F1** | blocking: yes (closest call of the review)
- claim: Task 3 does not say what outcome the `lens-scale` row gives CRITICAL, IMPORTANT and MINOR, and the stage 2 plan needs those values. The spec says the label is information and the outcome comes from the three conditions. Task 3's own grammar uses `Conditional` for "a label whose outcome depends on a condition the table cannot test". An executor following both would write `Conditional` for all three labels.
- consequence: `ReviewerJudge` returns UNSET for `Conditional` (PLAN:151). Stage 2 `write` takes a row's tier from this row ("the shared outcome that the lens-scale row ... gives its native label") and has no fallback. No imported row would get a tier. No Task 3 acceptance line checks these three values; the only `Conditional` check is spec-panel MAJOR (PLAN:71).
- evidence: PLAN:62; PLAN:71; PLAN:151; SPEC:737 ("the label is information; the outcome comes from the three conditions"); STAGE2 Task 2 body, line 57.
- repair: add `CRITICAL=Blocking; IMPORTANT=Medium; MINOR=Note` to Task 3, with the `model` cell saying these are the default tier for a row a reviewer files as non-blocking. Add an acceptance line asserting the three pairs, and a stage 2 note that a Blocking row is never written.

**R3-F2** | blocking: no
- claim: no task supplies the NA marker for C. For M, Task 10 supplies NA only for a kind with no required-item list, and asks M only when an item is `absent-by-name`. `run_questions` gives every other question UNSET (PLAN:151).
- consequence: REQ-18 lifts any U or UNSET on M or C to SHOW_USER. So a finding without constraint lines, or one that does not name a missing item, comes out SHOW_USER or BLOCKING at best. FOLLOW_UP and NOTE are almost unreachable. Stage 2 Task 7 would then evaluate a near-trivial classifier. This is shadow only, so no gate changes.
- evidence: PLAN:166 (NA marker for M only); PLAN:151; SPEC:528 (REQ-19 allows NA for M and for C); SPEC:543.
- repair: Task 10 also returns a "kind declared to have no constraint list" marker. Add one sentence saying what verdict an unasked M or C is expected to give, or record it in the Task 16 owner summary as a known limit.

**R3-F3** | blocking: no
- claim: no task owns the consent and offer logic of REQ-11. Task 8 builds only the Filings table, and Task 7 lists no Offers table. Yet Task 8's tests include "a resume asks again" and "a changed set is filed without new consent", and T8 is a stage 1 exit test (SPEC:945). There is no plan-defined function for those tests to call.
- evidence: PLAN:137. The Offers table, with `set_digest`, `answer` and `state`, is at SPEC:375 and the Filings table at SPEC:377. Grep for `set_digest`, `REQ-11` and `Offers table` across the four stage plans finds no stage 1 owner. The only hit outside Task 4 is the stage 2 owner summary (STAGE2:148).
- repair: add one sentence to Task 8. Filing is refused unless an Offers row with an explicit filing answer and a matching `set_digest` exists. A resume returns the pending offer without asking. A changed set or a changed body digest needs a new offer.

**R3-F4** | blocking: no
- claim: Task 12 names no inputs for its command. These are the findings file layout, the judge-answers file format, the deliverable path and kind per finding, the family key, and where the ledger path and its `expected_revision` come from. Task 10 needs a deliverable file and a kind per finding. `update_field` needs an `expected_revision`. The tests are the plan's own, so they will pass, but the executor invents the interface. Stage 2 `safety --judge-answers` and the stage 2 recorded fixtures depend on the same `FixtureJudge` file format, which no stage 1 task defines.
- evidence: PLAN:192 ("reads findings plus a judge answers file"); PLAN:166; PLAN:124.
- repair: name the options (`--findings`, `--judge-answers`, `--deliverable`, `--kind`, `--ledger`, `--out`). Say in Task 9 that `FixtureJudge` reads a JSON map of finding id to question id to a probability or a state.

**R3-F5** | blocking: no
- claim: PLAN:124 asks for a test that `earlier_decisions` "does not return a `pending` row". `pending` is a state of the Offers table, not an item state (SPEC:375, SPEC:381-390). The executor must guess.
- evidence: PLAN:124; SPEC:375.
- repair: say "a `recorded` row".

**R3-F6** | blocking: no
- claim: STAGE2:27 refers to a "stage 1 acceptance line saying that only the new module and its command wiring mention `follow_ups`". No such line exists now. PLAN:129 says other files may list it from Task 10 on. Harmless, but it quotes text that is gone.
- evidence: STAGE2:27; PLAN:129.
- repair: reword the stage 2 sentence to say that from Task 10 on stage 1 lists `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`.

## Earlier findings check

- First review F1 (Task 7 grep end point): fixed, PLAN:129.
- First review F2 (stoprule row): fixed, PLAN:64 and PLAN:70.
- First review F3 (allow-list): fixed, PLAN:66 and PLAN:74.
- First review F4 (ledger mapping decision): fixed, PLAN:122.
- First review F5 (scale-map shape; Tasks 9, 12, 15 depend on Task 3): fixed, PLAN:62, PLAN:149, PLAN:190, PLAN:232.
- First review F6 (Task 10 depends on Task 7): fixed, PLAN:164.
- First review F7 (`run_questions` and `questions_to_ask` assigned): fixed, PLAN:151 and PLAN:166.
- First review F8 (full path in the Task 2 grep; "present today"): fixed, PLAN:56 and PLAN:115. The review subcommand modules on disk are the seven the plan lists, and `lint_cmd` and `estimate_cmd` do not exist.
- First review F9 (`sweep-flagged`): fixed, PLAN:82 and PLAN:88.
- M-F1 (`--include='*.py'` and "lists no file other than"): fixed, PLAN:129. A search of `src/superclaude` finds no file that mentions `follow_ups` today.
- M-F2 (grammar, key, `Conditional`, ` + `): fixed in text, PLAN:62 and PLAN:151. R3-F1 is a remaining gap in the values.
- M-F3 (REQ-09 owner): fixed, `earlier_decisions` at PLAN:124. The test wording is R3-F5.
- M-F4 (M precheck and D input): fixed, PLAN:166 and PLAN:192. R3-F2 is the consequence of the unasked M.
- M-F5 (`update_field`, results file): fixed, PLAN:124 and PLAN:192. The inputs gap is R3-F4.
- M-F6 (resolver injected, loaded by path): fixed, PLAN:137. `read_origin` and `ClaimError` exist in `origin_repo.py` at lines 156 and 77.
- M-F7 (no `.dev/` or `src/superclaude` in Tasks 4 and 5): fixed, PLAN:82, PLAN:90, PLAN:99-100, PLAN:115.
- M-F8 (Task 1 gate before creating files): fixed, PLAN:36.
- M-F9 (nits): fixed. `verify-citations` is at PLAN:192, the tasklist count is 9 at PLAN:72 (live `grep -c -i` also gives 9), and "prints nothing" is at PLAN:52.
- M-F10 (end point; `THRESHOLDS`): fixed, PLAN:129 and PLAN:151. Both constants exist in `contracts/__init__.py` (lines 93 and 129).

## Other checks

- Task numbering is 1 to 16, and every `Depends on:` points to a lower number.
- The 14 worked cases, the 12 scale-map families, the 11 `digest` carriers and the cap sentence all match the spec and `pragmatic.md`.
- The old definition sentence is in exactly those 11 files. None of them contains `src/superclaude`, so Task 15's T3 and T2 checks can be met on the current repository.
- The files Tasks 12 and 14 name all exist: the `cli/review` subcommand modules, the three doctor and update test files, `reuse-auditor` and the sketch.
- The stage 1 gate in Task 1 will halt today. `stage-requests/README.md` row 1 has an empty "Owner go" cell (line 18). This is the intended behaviour.

## Verdict

NEEDS-REVISION. confidence 0.6. blocking ids: R3-F1.

If the owner reads R3-F1 as non-blocking, this is PASS with notes R3-F2 to R3-F6, confidence about 0.7.

reviewer_model_self_report: claude-gw-tier1b[1m] (the brief pins model class sonnet)

## Orchestrator note
This reviewer numbered its findings R3-F1 to R3-F6 by mistake; in the merge they are read as R1-F1 to R1-F6 (R1-F1 is the blocking claim on the lens-scale values).

## Calibration (blind, opus class)
```yaml
calibrated_C: 0.81
per_dimension: {citation_grounding: 0.92, coverage_completeness: 0.80, deviation_classification_clarity: 0.60, risk_surface_coverage: 0.85, recommendation_actionability: 0.88}
verified_citations: 18 re-read, all held
blocking_grade_support: {R1-F1: partly}
calibrator_model_class: opus
```
