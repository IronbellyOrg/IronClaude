<!-- Merged review card. Base: variant 1 (reviewer 1, analyzer, sonnet class). Merge date: 2026-11-16T19:44Z. Refactor plan: adversarial/refactor-plan.md, changes PC-01 to PC-10. Merge log: adversarial/merge-log.md. -->

# Merged review card: third review of the stage 1 plan

<!-- Source: Base (original, modified) - alias line extended with STAGE3, STAGE4 and other files per PC-04, PC-05 and PC-10; reviewer metadata header of variant 1 replaced by the merge header -->

`PLAN:n` = line n of `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`; `SPEC:n` = line n of `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`; `STAGE2:n`, `STAGE3:n` and `STAGE4:n` = line n of the stage 2, stage 3 and stage 4 plans (`TASK-WF-blockerStage2-20261116-030156`, `TASK-WF-blockerStage3-20261116-030158`, `TASK-WF-blockerStage4-20261116-030206`, each under `.dev/tasks/to-do/<id>/<id>.md`). Other files are named by their path from the repository root. Finding ids are `N-F1` to `N-F11`; every cited line was re-read on 2026-11-16 during the merge.

## Findings

<!-- Source: Base (original, modified) - finding set renumbered N-F1 to N-F11 and extended with variant 2 and 3 findings per PC-02 to PC-05 and PC-10 -->

### N-F1 | blocking: yes (closest call of the review)

<!-- Source: Base (original, modified) - variant 1 R1-F1 kept for claim and consequence; repair replaced per PC-01 (INV-001, INV-002, C-001, X-001); REQ-02 citation from Variant 3, finding R3-F4 -->

- claim: Task 3 does not say what outcome the `lens-scale` row gives CRITICAL, IMPORTANT and MINOR, and the stage 2 plan needs those values. The spec row says "the label is information; the outcome comes from the three conditions" (SPEC:737). Task 3's own grammar uses `Conditional` for "a label whose outcome depends on a condition the table cannot test" (PLAN:62). An executor following both would write `Conditional` for all three labels.
- consequence: `ReviewerJudge` returns UNSET for a `Conditional` outcome (PLAN:151). Stage 2 `write` takes a row's tier from this row ("the shared outcome that the lens-scale row of `refs/scale-map.md` gives its native label", STAGE2:57) and gives no rule for a `Conditional` outcome. No imported row would get a tier. No Task 3 acceptance line checks these three values; the only `Conditional` check is spec-panel MAJOR (PLAN:71).
- why three fixed values do not repair it (INV-001, INV-002): the one `labels` cell has two readers that need different answers. The stage 2 importer reads it as a tier (STAGE2:57). `ReviewerJudge` and the Task 12 disagreement matrix read it as the reviewer's blocking call (PLAN:151, PLAN:192), and the spec reads an rf-qa IMPORTANT as blocking (SPEC:211, SPEC:592; Task 3 records the same for `card_convert.py` at PLAN:73). `src/superclaude/agents/rf-qa.md` line 111 also lets a reviewer grade an IMPORTANT finding minor ("a finding labelled IMPORTANT that is only wording is minor").
  - `IMPORTANT=Blocking`: a reviewer-minor IMPORTANT row is dropped, because the importer never writes Blocking rows (STAGE2:57).
  - `IMPORTANT=Medium` (variant 1's original repair): the shadow comparison reads IMPORTANT as non-blocking, the reading SPEC:592 forbids, and a reviewer-blocking IMPORTANT row arrives without `why not blocking` and is refused by the writer (STAGE2:57).
  - `MINOR=Note`: every non-blocking MINOR row goes to the Notes table, which holds only `id`, `location`, one line and `status` (SPEC:371): no tags, no `rests_on`, no `why_not_blocking`. Notes are never swept (STAGE2:42), the `consumer-unknown` share of the stage 2 summary cannot see those rows (STAGE2:148), and the `protected-risk-dispute` tag that Task 13 sets (PLAN:206) has no column to land in. `MINOR=Medium` avoids all of this.
- evidence: PLAN:62; PLAN:71; PLAN:73; PLAN:151; PLAN:192; PLAN:206; SPEC:211; SPEC:371; SPEC:592; SPEC:737; SPEC:744; STAGE2:42; STAGE2:57; STAGE2:148; `src/superclaude/agents/rf-qa.md` line 111.
- repair (one owner decision, two forms): Task 3 fixes the three lens-scale labels in the `labels` cell, with a `model` cell that says what the values mean to each reader. Form 1: the values `CRITICAL=Blocking;IMPORTANT=Blocking;MINOR=Medium` for the shadow comparison (REQ-02 at SPEC:211; SPEC:592), together with a stage 2 note that the importer takes blocking or non-blocking from the reviewer's own call (a filled `why not blocking`) and uses the cell only to split non-blocking rows into Medium and Note. Under form 1 no label maps to Note and IMPORTANT holds Blocking, so the owner must also say what a reviewer-minor IMPORTANT row gets (for example Medium, with its `why not blocking` required; recorded in merge-log.md as an open case). Form 2: a second column, so each reader reads its own value. In either form, add a Task 3 acceptance line asserting the chosen pairs. The owner picks the form; the finding stays blocking until one form is in the plan.
- status: the closest call of this review. All three debate advocates graded it blocking, at 55, 76 and 65 percent confidence. This is the third review of this plan.

### N-F2 | blocking: no

<!-- Source: Variant 3, finding R3-F3 (mechanism and repair) with Variant 2, finding R2-F1 (same gap) and the Base R1-F4 note on Task 12 - merged per PC-02 -->

- claim: Task 9 takes the scale-map family key "from the `origin` of the ledger row" (PLAN:151), but the spec defines `origin` as a protocol name plus the original finding id, for example `P3-006` (SPEC:353), not one of Task 3's twelve keys (PLAN:62). The reviewing agent and its native label are in `source` (SPEC:355). Task 12 never says where it gets the key (PLAN:192; see also N-F6).
- consequence: a contract-valid ledger row looks like an unknown family, so `ReviewerJudge` returns UNSET for it and Task 12's matrix counts every such label in the unmapped column. Tests that pass the key directly (PLAN:179) still go green. Not blocking: `ReviewerJudge` feeds no stage 2 figure (STAGE2:28, STAGE2:135) and no stage 1 exit test needs the mapping.
- evidence: PLAN:62; PLAN:151; PLAN:179; PLAN:192; SPEC:353; SPEC:355; STAGE2:28; STAGE2:135.
- repair: Task 3 adds a `reviewers` column (for example `rf-qa`, `rf-qa-qualitative` → `lens-scale`); Tasks 9 and 12 resolve the family from the reviewing agent in `source`; Task 11 adds a case for an origin that matches no key.
- grade: non-blocking (2 of 3 debate advocates).

### N-F3 | blocking: no

<!-- Source: Variant 2, finding R2-F2 - merged per PC-03 (grade non-blocking after the debate; INV-004) -->

- claim: a SHOW_USER verdict means the reviewer's label stands and the row is tagged `unsettled` (SPEC:369, SPEC:439, SPEC:596). Task 12 writes only the `classifier` column of an existing row (PLAN:192). A grep of the stage plans (`TASK-WF-blockerStage*` under `.dev/tasks/to-do/`) finds `unsettled` once, in the Task 4 reference text (PLAN:87); no task of any stage produces the tag.
- consequence: a Medium row with a SHOW_USER verdict stays an ordinary follow-up and is not counted in `show_user`. Not blocking: no stage 1 requirement or exit test needs the tag (the stage 1 exit tests are listed at SPEC:945). Graded without an owner, the gap is lost (INV-004).
- evidence: PLAN:87; PLAN:192; SPEC:369; SPEC:439; SPEC:596; SPEC:945.
- repair: Task 12 adds `unsettled` through the sole writer without clearing existing tags (the Task 7 acceptance line at PLAN:130 already requires that later writes keep tags), or the stage 2 revision owns it. Carried as a note; it has no owner today.

### N-F4 | blocking: no

<!-- Source: Base (original) - variant 1 R1-F2 -->

- claim: no task supplies the NA marker for C. For M, Task 10 supplies NA only for a kind with no required-item list, and asks M only when an item is `absent-by-name` (PLAN:166). `run_questions` gives every other question UNSET (PLAN:151).
- consequence: REQ-18 lifts any U or UNSET on M or C to SHOW_USER (SPEC:543). So a finding without constraint lines, or one that does not name a missing item, comes out SHOW_USER or BLOCKING at best, and FOLLOW_UP and NOTE are almost unreachable. Stage 2 Task 7 would then evaluate a near-trivial classifier. This is shadow only, so no gate changes.
- evidence: PLAN:151; PLAN:166 (NA marker for M only); SPEC:528 (REQ-19 allows NA for M and for C); SPEC:543.
- repair: Task 10 also returns a "kind declared to have no constraint list" marker. Add one sentence saying what verdict an unasked M or C is expected to give, or record it in the Task 16 owner summary as a known limit.

### N-F5 | blocking: no

<!-- Source: Base (original, modified) - variant 1 R1-F3; repair per PC-07; link to N-F7 per INV-003 -->

- claim: no task owns the consent and offer logic of REQ-11. Task 8 builds only the Filings table (PLAN:137), and Task 7 lists no Offers table (PLAN:124). Yet Task 8's tests include "a resume asks again" and "a changed set is filed without new consent" (PLAN:137), Task 8's acceptance line requires each T8 failure condition to be covered (PLAN:140), and T8 is a stage 1 exit test (SPEC:923, SPEC:945). There is no plan-defined function for those tests to call.
- evidence: PLAN:124; PLAN:137; PLAN:140; the Offers table, with `set_digest`, `answer` and `state`, at SPEC:375; the Filings table at SPEC:377; the consent rules at SPEC:421-428; SPEC:923; SPEC:945. A grep for `set_digest`, `REQ-11` and `Offers table` across the stage plans finds only the Task 4 reference text (PLAN:82) and the stage 2 owner summary (STAGE2:148).
- linked: N-F7 comes from the same gap; no task builds or writes the Offers table (INV-003).
- repair: add to Task 8: filing is refused unless an Offers row with an explicit filing answer and a matching `set_digest` exists; a resume returns the pending offer without asking; a changed set or a changed body digest needs a new offer.
- grade: non-blocking. T8 can still be met if consent is built into the filing code.

### N-F6 | blocking: no

<!-- Source: Base (original, modified) - variant 1 R1-F4; family-key part moved to N-F2 per PC-02 -->

- claim: Task 12 names no inputs for its command: the findings file layout, the judge-answers file format, the deliverable path and kind per finding, the family key (N-F2), and where the ledger path and its `expected_revision` come from (PLAN:192). Task 10 needs a deliverable file and a kind per finding (PLAN:166). `update_field` needs an `expected_revision` (PLAN:124). The tests are the plan's own, so they will pass, but the executor invents the interface. Stage 2 `safety --judge-answers` reads recorded answers through the stage 1 `FixtureJudge` (STAGE2:57), and the stage 2 evaluation records its answers in fixture files (STAGE2:135); no stage 1 task defines that file format.
- evidence: PLAN:124; PLAN:166; PLAN:192 ("reads findings plus a judge answers file"); STAGE2:57; STAGE2:135.
- repair: name the options (`--findings`, `--judge-answers`, `--deliverable`, `--kind`, `--ledger`, `--out`). Say in Task 9 that `FixtureJudge` reads a JSON map of finding id to question id to a probability or a state.

### N-F7 | blocking: no

<!-- Source: Base (original, modified) - variant 1 R1-F5; repair widened per PC-08 (Variant 2/3 confirmation) -->

- claim: PLAN:124 asks for a test that `earlier_decisions` "does not return a `pending` row". `pending` is a state of the Offers table (SPEC:375), not an item state (SPEC:381-390). The executor must guess.
- evidence: PLAN:124; SPEC:375; SPEC:381-390.
- repair: say "a `recorded` or `offered` row"; `pending` is an Offers state. See N-F5 for the shared cause.

### N-F8 | blocking: no

<!-- Source: Base (original, modified) - variant 1 R1-F6 merged with Variant 3, finding R3-F6 - merged per PC-09 -->

- claim: two stage 2 sentences describe stage 1 text or output in a way that is already wrong or will be wrong after stage 1 runs. STAGE2:27 refers to a "stage 1 acceptance line saying that only the new module and its command wiring mention `follow_ups`"; no such line exists now, because PLAN:129 lets other files list it from Task 10 on. STAGE2:57 says `__init__.py` "registers nine subcommand modules today"; it holds nine names today (`src/superclaude/cli/review/__init__.py` lines 19-29) and will hold ten once Task 12 adds `classify_cmd` (PLAN:192). Both are harmless.
- evidence: STAGE2:27; STAGE2:57; PLAN:129; PLAN:192; `src/superclaude/cli/review/__init__.py` lines 19-29.
- repair: reword the two stage 2 sentences: from Task 10 on stage 1 lists `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`; the tuple holds ten names after stage 1.

### N-F9 | blocking: no

<!-- Source: Variant 3, finding R3-F1 - merged per PC-04 -->

- claim: Task 14 can make Task 15's T2 test fail inside this same package. Task 14 adds a digest-version reader to `src/superclaude/cli/doctor.py` (PLAN:222), an existing source file (`run_doctor` is at line 17; the file holds no `review-severity:digest` text today), and nothing stops that reader from holding the literal fence text `review-severity:digest`. T2 scans the tracked `src/` tree and fails on any file that holds a fence opener and has no registry row (PLAN:234, SPEC:917). `doctor.py` will never have a row, because Task 6 fixes the registry at 19 rows (PLAN:113). The acceptance line "passes with all `digest` rows at `legacy`" (PLAN:238) would then fail, and an executor who gives `doctor.py` a row breaks Task 6's count of 19. The stage 4 plan already expects this literal in `doctor.py` (STAGE4:114).
- evidence: PLAN:113; PLAN:222; PLAN:234; PLAN:238; SPEC:917; STAGE4:114 ("for example a string in `src/superclaude/cli/doctor.py`, which stage 1 extends to read digest versions"); `src/superclaude/cli/doctor.py` line 17.
- repair: in Task 14, build the marker from parts, and add the acceptance line "`grep -n "review-severity:digest" src/superclaude/cli/doctor.py` prints nothing", valid until stage 4.

### N-F10 | blocking: no

<!-- Source: Variant 3, finding R3-F2 - merged per PC-05 -->

- claim: Task 15 names the `STRICT_T2` constant (`False` in this phase, set to `True` by stage 4) but never says what turning it on changes, and no acceptance line shows the switch has any effect (PLAN:234). The stage 4 plan assumes a meaning: with the switch on, a file that holds the old sentence fails even when it has a registry row (STAGE4:114, STAGE4:119), the spec's "from stage 4, any legacy definition sentence remains" (SPEC:917). Stage 4 also still says stage 1 "did not name the switch" (STAGE4:114). A no-op constant would pass stage 1, and stage 4's case (b) would then fail on a file stage 4 did not write.
- evidence: PLAN:234; SPEC:917; STAGE4:114; STAGE4:119.
- repair: add to Task 15: "with `STRICT_T2` True, a registered file that holds the old sentence also fails", and a temporary-tree case that shows both modes. Note for stage 4: drop its "did not name the switch" sentence.

### N-F11 | blocking: no

<!-- Source: Variant 3, finding R3-F5 - merged per PC-05 -->

- claim: the new skill text is never checked against the repository-wide banned-phrase scans during stage 1. `tests/skills/test_review_severity_rule.py` builds its file set from `git ls-files` over the scanned trees (lines 28 and 36-51) and runs the any-severity scan over tracked `src/`, `plugins/`, `commands/` and `agents/` files (lines 172-176). The plan's staging instruction names `.dev/tasks/` only (PLAN:30), so the new `src/superclaude/skills/sc-review-severity/` files are not seen by that scan while stage 1 runs. The banned list holds "regardless of severity" (line 117), a phrase the spec's REQ-30 FAIL-trigger list also names (SPEC:849), and Task 3's L6 sentence (PLAN:66) could copy it. A hit would first show in a stage 2 run of that test (STAGE2:88, STAGE2:102).
- evidence: `tests/skills/test_review_severity_rule.py` lines 28, 36-51, 117, 172-176; PLAN:30; PLAN:66; SPEC:849; STAGE2:88; STAGE2:102.
- repair: add to Task 5 one acceptance check that greps the `BANNED_SEVERITY_PHRASES` and `SWEEP_PHRASES` lists of that test file (lines 112 and 390) over `src/superclaude/skills/sc-review-severity` and must print nothing.

## Run notes (not plan findings)

<!-- Source: Variant 2, finding R2-F3 - merged per PC-06; INV-006 and INV-007 from invariant-probe.md -->

- Audit-artifact omission (C-012). This run's `artifacts/coverage-matrix.yaml` has Pass 2 rows for source line 53 only (INF-081 and INF-082, lines 508-527 of that file) and none for source lines 51 and 52 or for the threshold-name part of line 53 (`.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md` lines 51-53). The plan holds those requirements, so this is a gap in the review's coverage record, not a plan defect. Supplemental rows (carried here; `artifacts/inferred-table.md` was not edited by this merge):

| Source line | Requirement | Plan line |
|---|---|---|
| 51 | Task 1 runs its go and stage 0 summary checks before it creates `SKILL.md` | PLAN:36 |
| 52 | `verify` is now `verify-citations` in Task 12 | PLAN:192 |
| 52 | T3 wording for `installed-only` rows (not checked by T3) in Task 15 | PLAN:234 |
| 52 | Task 2's grep line says "prints nothing" | PLAN:52 |
| 52 | tasklist Medium line count is 9 on 2026-11-16 | PLAN:72 |
| 53 | Task 9's constant is not named `THRESHOLDS` or `CONVERGENCE_THRESHOLDS` | PLAN:151 |
| 53 | Tasks 9, 10, 12 and 13 gain a `make lint` acceptance line (INF-082 matched it to Task 7) | PLAN:160, PLAN:173, PLAN:200, PLAN:213 |

- INV-006. The T2 reverse scan of Task 15 reads tracked files, and the existing scan helper builds its set from `git ls-files` (`tests/skills/test_review_severity_rule.py` lines 36-39). With only `.dev/tasks/` named for staging (PLAN:30), the scan sees the tracked `doctor.py` but not the new `rule.md`, `scale-map.md` or `registry.yaml`; "the reverse scan accepts `refs/rule.md`" (PLAN:240) is meaningful only in a temporary tree, which that line already uses.
- INV-007. Task 3 spells `defining file` paths without the `src/superclaude/` prefix (PLAN:62), while Task 6 requires "a source path that exists" (PLAN:113) with no spelling rule. The folder grep at PLAN:115 catches a wrong spelling, so the cost is a retry.

## Earlier findings check

<!-- Source: Base (original, modified) - F4 line corrected from PLAN:122 to PLAN:124; F8 citation PLAN:115 replaced by PLAN:192 after re-read; R3-Fk ids renamed to N-F ids per PC-10 -->

- First review F1 (Task 7 grep end point): fixed, PLAN:129.
- First review F2 (stoprule row): fixed, PLAN:64 and PLAN:70.
- First review F3 (allow-list): fixed, PLAN:66 and PLAN:74.
- First review F4 (ledger mapping decision): fixed, PLAN:124.
- First review F5 (scale-map shape; Tasks 9, 12, 15 depend on Task 3): fixed, PLAN:62, PLAN:149, PLAN:190, PLAN:232.
- First review F6 (Task 10 depends on Task 7): fixed, PLAN:164.
- First review F7 (`run_questions` and `questions_to_ask` assigned): fixed, PLAN:151 and PLAN:166.
- First review F8 (full path in the Task 2 grep; "present today"): fixed, PLAN:56 and PLAN:192. The review subcommand modules on disk are the seven the plan lists, and `lint_cmd` and `estimate_cmd` do not exist.
- First review F9 (`sweep-flagged`): fixed, PLAN:82 and PLAN:88.
- M-F1 (`--include='*.py'` and "lists no file other than"): fixed, PLAN:129. A search of `src/superclaude` finds no file that mentions `follow_ups` today.
- M-F2 (grammar, key, `Conditional`, ` + `): fixed in text, PLAN:62 and PLAN:151. N-F1 is a remaining gap in the values.
- M-F3 (REQ-09 owner): fixed, `earlier_decisions` at PLAN:124. The test wording is N-F7.
- M-F4 (M precheck and D input): fixed, PLAN:166 and PLAN:192. N-F4 is the consequence of the unasked M.
- M-F5 (`update_field`, results file): fixed, PLAN:124 and PLAN:192. The inputs gap is N-F6.
- M-F6 (resolver injected, loaded by path): fixed, PLAN:137. `read_origin` and `ClaimError` exist in `origin_repo.py` at lines 156 and 77.
- M-F7 (no `.dev/` or `src/superclaude` in Tasks 4 and 5): fixed, PLAN:82, PLAN:90, PLAN:99-100, PLAN:115.
- M-F8 (Task 1 gate before creating files): fixed, PLAN:36.
- M-F9 (nits): fixed. `verify-citations` is at PLAN:192, the tasklist count is 9 at PLAN:72 (live `grep -c -i` also gives 9), and "prints nothing" is at PLAN:52.
- M-F10 (end point; `THRESHOLDS`): fixed, PLAN:129 and PLAN:151. Both constants exist in `contracts/__init__.py` (lines 93 and 129).

All of F1 to F9 and M-F1 to M-F10 are fixed.

## Checked and found clean

<!-- Source: Base "Other checks" (original, modified) merged with Variant 3 "Checked and found clean" - merged per PC-10; brief-decision line rebased on the stage ledger after re-read -->

- Task numbering is 1 to 16, and every `Depends on:` points to a lower number. Task 8's mention of Task 9 (PLAN:137) is a pattern reference, not a code dependency.
- The 14 worked cases, the 12 scale-map families, the 11 `digest` carriers and the cap sentence match the spec and `pragmatic.md`: the cap sentence quoted at PLAN:49 equals `src/superclaude/output-styles/pragmatic.md` line 227, and the counts were re-checked by the invariant probe (INV-005).
- Exactly 11 files under `src/superclaude` hold the old definition sentence, and they are the 11 `digest` rows of PLAN:109. None of them contains `src/superclaude`, so Task 15's T3 and T2 checks can be met on the current repository. No file under `plugins/` holds the sentence, and no file under `src/superclaude` or `plugins/` holds a `review-severity:digest` fence today.
- Every allow-list path of PLAN:66 exists, as do `origin_repo.py`, `agents/reuse-auditor.md`, `skills/sc-bare-review`, the PF sketch files (`02-brainstorm/blocker_truth_table_sketch.py`, `07-classifier/truth_table.py`) and the tests that Tasks 12 and 14 name. The stoprule skill folder and `finding-grader.md` are absent from `src/superclaude`, which matches their `installed-only` row (PLAN:64).
- The live review subcommand modules are seven, including `verify_cmd.py`, whose command name is `verify-citations` (line 76).
- Stage 3 takes `rf-analyst.md` (STAGE3:189), and its scan reads the allow-list from the Task 3 section (STAGE3:240).
- The revision 2 decisions recorded in the stage ledger (`.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md` lines 38-41: retired carriers, `/sc:implement` final review as carrier, no plugin surface, separate follow-up ledger) are honoured at PLAN:24, PLAN:25, PLAN:26 and PLAN:124.
- The stage 1 gate in Task 1 will halt today: the stage ledger row 1 has an empty "Owner go" cell (`stage-requests/README.md` line 18). This is the intended behaviour.

## Not checked

<!-- Source: Variant 3 "Not checked" line (original, modified) - extended per PC-10 with A-002 and A-003 of diff-analysis.md -->

- No test, build or plan command was run. This is a static read; "can be met" means a counterexample was not found, not that a test passed (A-003).
- The spec section 9.3 defining files were checked only partly: `agents/rf-qa.md` and the allow-list files were read or found; the defining files of the other scale-map families were not.
- The stage 2 and stage 4 plans were read as they stand today (A-002). N-F1, N-F6 and N-F8 depend on STAGE2 text that the stage 2 revision may change.

## Verdict

<!-- Source: Base (original, modified) - hedged second verdict removed and ids renamed per PC-10; variant metadata, orchestrator note and calibration block of variant 1 dropped -->

NEEDS-REVISION. Blocking: 1 (N-F1). Non-blocking: 10 (N-F2 to N-F11).

N-F1 is the closest call of this review and is cleared by one owner decision: form 1 or form 2 of its repair, written into Task 3 with an acceptance line. The ten non-blocking findings are cheap to fix in the same revision; N-F9 is the one most likely to stop the executor partway.


<!-- BEGIN REPORT BODY -->
```yaml
contract_version: 1.8.0
status: partial                      # forced by the evidence gate: 7 unfounded report-body items were dropped and corrected (protocol 11.2); no plan finding changed
mode: pre
tier_reached: 2
confidence_calibrated: 0.80          # mean of the three blind reviewer calibrations (0.81, 0.82, 0.77); the T1 card alone calibrated 0.60
citations_total: 311                 # 152 in the merged card, 106 checked in the report body, 53 inferred and supplemental quotes (script-verified verbatim)
citations_revalidated: 311
citations_dropped: 7
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report (pre-execution), third and final review: plan TASK-WF-blockerStage1-20261116-030154

Run folder: `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116185843/`
Plan: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (4 phases, 16 tasks, 254 lines). Source: `source.md` in the same folder (55 lines, a byte copy of `stage-requests/stage1-request.md`, checked with cmp). Spec checked against: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`. `PLAN:n`, `SPEC:n`, `STAGE2:n`, `STAGE3:n`, `STAGE4:n` mean line n of the plan, the spec, and the stage 2, 3 and 4 plans.
Earlier reviews: `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116030453/REPORT.md` (first, findings F1 to F9) and `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116174309/REPORT.md` (second, M-F1 to M-F10). This run is a fresh run in a new folder; the plan, `source.md` and everything under `.dev/tasks/` were read only.
Generated: 2026-11-16. Advisory: reflect never edits the plan.

## Verdict

**NEEDS-REVISION.** A three-reviewer ensemble (sonnet, haiku and opus classes), each card blind-calibrated by an opus-class calibrator and merged by an adversarial debate (25 diff points, 24 of them debated and one stated; every debated point has a majority winner), found 11 defects in the revised plan: 1 blocking and 10 non-blocking.

(a) Earlier findings: all of the first review's F1 to F9 and the second review's M-F1 to M-F10 are fixed in the live plan text, including the blocking `.pyc` grep of Task 7 (`PLAN:129` now reads `grep -rln --include='*.py' --exclude-dir=__pycache__ "follow_ups" src/superclaude/cli/review`, which "lists no file other than `follow_ups.py`" until Task 10, and from Task 10 "until the stage 2 package adds its own importer" may list only `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`). All three reviewers confirmed this independently.
(b) The revisions added no broken numbering (16 tasks, contiguous), no `Depends on:` pointing to a higher task (15 lines, Tasks 2 to 16), no acceptance line that a later task of this package makes false without an end point, no missing path (every backticked path exists or is a file this package creates) and no contradiction with decisions 1, 2, 4 and 5 of the shared brief. The defects found are cross-stage interface gaps and under-specified deliverables.
(c) Against the spec: every stage 1 exit test of SPEC:945 (T1 to T4, T6 to T8, T11 to T13, T17) has a task that builds it.

**C-001, the lens-scale mapping gap between Task 3 and the stage 2 tier (N-F1): final grade BLOCKING, the closest call of the review.** Task 3 never says what outcome the `lens-scale` row gives CRITICAL, IMPORTANT and MINOR (`PLAN:62`), its own grammar defines `Conditional` for a label whose outcome depends on a condition the table cannot test (`PLAN:62`) and the spec says of this row "the label is information; the outcome comes from the three conditions" (`SPEC:737`), while the stage 2 importer sets every row's tier from that cell and has no rule for `Conditional` (`STAGE2:57`). All three debate advocates ended on blocking (55, 76 and 65 percent confidence). The fault-finder showed why a three-value one-liner is not enough: one cell has two readers that need different answers, and `agents/rf-qa.md` line 111 lets a reviewer grade an IMPORTANT finding minor. The repair is therefore one owner decision with two forms (see N-F1 and R-001). Without this finding the verdict would be PASS with notes; the finding is graded by consequence (a missing value the next package needs and no acceptance line checks), not by effort to fix.

## Tier decision

Tier 2, rule 4 fired (the plan touches code, tests, skill Markdown and registry/JSON config: 4 domains); rules 5 (`S_dev_density` 0.3276 above 0.20) and 6 (`C` 0.60 below 0.85) also match. The Step 1B.2b guard fired (inferred 49 > parsed 9), so a Tier-1 stop was forbidden in any case. Blind calibration of the T1 card gave C = 0.60. Reviewer classes: sonnet (analyzer, calibrated 0.81), haiku pin (qa, 0.82) and opus (refactorer, 0.77). Calibrator class: opus; all three Anthropic classes were reviewers, so the disjoint set was empty and `calibrator_diversity: degraded`. Executor class: unknown (pre-execution run), so no class was excluded and the anti-self-confirmation guarantee is weaker than designed. Single vendor: `t2_vendor_diversity: single`. Reviewer 2 (haiku pin) again self-reported an OpenAI model (`identity_mismatch_suspected`). Engine `legacy`; no panel code ran.

## Inferred requirements (Pass 2)

Coverage: `coverage_pct` (parsed only) 0.1111 and `coverage_pct_union` 0.6724 by the mechanical rule. The parsed rows R-001 to R-008 are recommendation labels of the earlier reviews that the ID regex picked up (false positives); only REQ-09 is a real requirement and Task 7 names it. By a manual read every one of the 49 kept rows maps to a task or to the Constraints block, and the 35 rows inside parsed spans (the Revision 2 and Revision 3 bullets) were checked one by one in the revision check below. The numbers are therefore a property of the extractor, not of the plan.

Pass 1 (parsed) rows: 9. Pass 2 rows from the requirements-analyst agent: 84; dropped by the parsed-span dedup rule: 35; kept: 49.

### Parsed rows (Pass 1)

| id | lines in source.md | exact-match tasks | note |
|---|---|---|---|
| R-001 | 26,28,42,44 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-002 | 29,47 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-003 | 30,45 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-004 | 31,46 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-005 | 32,48 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-006 | 33,49 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-007 | 26,34,50 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-008 | 42 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| REQ-09 | 46 | [7] | REQ-09 is a real spec requirement (cross-run match); Task 7 names it |

### Inferred rows kept (Pass 2)

| INF id | Verbatim quote (prefix, 120 characters at most) | Citation | Match result |
|---|---|---|---|
| INF-001 | This stage creates new files only (the skill folder, new CLI modules, new tests, one doctor check); it edits no review-l | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:3 | mechanical: none (task 7, 0.562); manual: PLAN:20 (Constraints, 'One package, one stage': creates new files only) |
| INF-002 | Generate it only after the owner has read the stage 0 package's `./artifacts/stage0-summary-for-owner.md` and said go in | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:3 | mechanical: containment (task 1, 0.818) |
| INF-003 | and after the stage ledger row for stage 0 has the package id | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:3 | mechanical: containment (task 1, 1.0) |
| INF-004 | Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 2, stage 1; found by  | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 9, 0.368); manual: provenance of the base text; no plan line states it; the plan holds Tasks 1 to 15 plus the exit task 16 (PLAN:34-248) |
| INF-005 | Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owner-decision defaults, the not-b | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 1, 0.357); manual: Constraints PLAN:17-30 |
| INF-006 | the classifier facts (M, C and E run only with code-supplied inputs; the "M or C is Y gives BLOCKING" row is never enabl | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: containment (task 12, 0.632) |
| INF-007 | pins by content, `src/superclaude/` as source of truth with `make sync-dev`, UV only | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 9, 0.5); manual: PLAN:27 (pins by content), PLAN:28 (source of truth, make sync-dev), PLAN:29 (UV only) |
| INF-008 | The stage 0 package's evidence (inventory freeze, availability counts, spec reconciliation) is read by package id. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 1, 0.5); manual: PLAN:19 (earlier-stage evidence read by package id) |
| INF-009 | State this package is stage 1: new files only, no carrier edited, every registry `digest` row stays `legacy`. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:11 | mechanical: containment (task 6, 0.769) |
| INF-010 | The next package (stage 2) starts only after the owner's go in chat. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:11 | mechanical: containment (task 16, 0.667) |
| INF-011 | Drop the base plan's Phase 3 to 5 gate prose. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:11 | mechanical: none (task 2, 0.333); manual: plan has 4 phases (PLAN:32, 118, 145, 216) and no gate prose after Phase 4 |
| INF-012 | The "Merge-rule allow-list" section lists files by path and never writes the three merge-rule phrases or the old definit | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:12 | mechanical: containment (task 3, 0.929) |
| INF-013 | At stage 1 it lists the auggie file, `refs/rule.md` and the six stage 4 files. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:12 | mechanical: containment (task 3, 0.9) |
| INF-014 | Say in the task that the plugin mirror is added in stage 4, not here. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:12 | mechanical: containment (task 3, 0.625) |
| INF-015 | `refs/rule.md` holds the GR5 sentence with the phrase `highest severity` (allow-listed) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:13 | mechanical: containment (task 2, 0.875) |
| INF-016 | never quotes the old definition sentence "Grade every review finding as blocking or minor" outside the digest's own fenc | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:13 | mechanical: containment (task 2, 0.8) |
| INF-017 | state this as an acceptance line (`grep` of the old sentence over the skill folder prints nothing) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:13 | mechanical: containment (task 2, 0.8) |
| INF-018 | No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path (acceptance: `grep -rn | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:14 | mechanical: containment (task 5, 0.857) |
| INF-019 | State the M, C and E input rule in words. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:14 | mechanical: containment (task 5, 0.714) |
| INF-020 | Keep exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:15 | mechanical: containment (task 6, 0.923) |
| INF-021 | Say the analysis template is not a carrier row (merge-rule text only in stage 4). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:15 | mechanical: containment (task 6, 0.667) |
| INF-022 | T3's `src/superclaude` check applies to `digest` and `canonical` rows only | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 1.0) |
| INF-023 | `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its poin | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 1.0) |
| INF-024 | the test never reads `~/.claude` | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 1.0) |
| INF-025 | T2 is non-strict (strict only in stage 4). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 0.8) |
| INF-026 | Acceptance includes a temporary-tree test of each exemption. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 11, 0.6) |
| INF-027 | that a later task of the same package makes false get an end point ("until Task N"). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:17 | mechanical: none (task 7, 0.5); manual: PLAN:27 (end-point rule); applied at PLAN:129 ('Until Task 10', 'From Task 10 until') |
| INF-028 | New final task: stage 1 exit summary for the owner. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 0.625) |
| INF-029 | Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and its observed test result (the co | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 0.667) |
| INF-030 | the list of files created | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 1.0) |
| INF-031 | a statement that no carrier was edited (`git diff --stat` over carriers is empty) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 0.75) |
| INF-032 | the open items, and the sentence that the owner's go for stage 2 is given in chat and not by this file | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 1.0) |
| INF-033 | No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT) and | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:22 | mechanical: none (task 4, 0.4); manual: Constraints PLAN:20 and PLAN:22 |
| INF-034 | Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent ta | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:22 | mechanical: none (task 2, 0.364); manual: Constraints PLAN:22 |
| INF-035 | No Jev call, key or account. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:22 | mechanical: none (task 9, 0.5); manual: Constraints PLAN:22 (no Jev call, key or account) |
| INF-060 | Task 3 lists `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md` as `exempt-by-retirement` (p | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:35 | mechanical: containment (task 3, 1.0) |
| INF-061 | the exemption ends when the retirement removes the file | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:35 | mechanical: containment (task 3, 1.0) |
| INF-062 | Task 16's carrier diff adds the task-builder folder. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:35 | mechanical: containment (task 16, 0.625) |
| INF-063 | `/sc:implement`'s final review step records and prints only, the offer stays with the top-level session and the consent- | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:36 | mechanical: containment (task 4, 0.938) |
| INF-064 | `tech-research` writes the ledger and neither sweeps nor offers | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:36 | mechanical: containment (task 4, 1.0) |
| INF-065 | `sc-implement-protocol` joins the not-edited list and the Task 16 diff. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:36 | mechanical: none (task 7, 0.429); manual: Constraints PLAN:20, PLAN:25; Task 16 diff PLAN:248 |
| INF-066 | Task 3 no longer says a plugin mirror comes in stage 4 | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 3, 0.667) |
| INF-067 | Task 6's canonical row has no plugin surface | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 15, 0.857) |
| INF-068 | Task 16 diff adds `plugins`. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 16, 0.8) |
| INF-069 | Registry counts unchanged: 11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 6, 0.846) |
| INF-081 | Task 7's importer list has the end point "until the stage 2 package adds its own importer" | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:53 | mechanical: containment (task 7, 0.917) |
| INF-082 | Tasks 9, 10, 12 and 13 gain a `make lint` acceptance line. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:53 | mechanical: containment (task 7, 0.6) |
| INF-083 | a later `write` or `update_field` never clears a ledger's capture state or a row's tags (the stage 2 package tests it) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:54 | mechanical: containment (task 7, 0.875) |
| INF-084 | Task 15 names the strict switch of T2 as the constant `STRICT_T2` (default `False`); the stage 4 package sets it `True`. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:55 | mechanical: containment (task 15, 0.867) |

### Inferred rows dropped by the parsed-span rule (parsed wins)

Rows whose cited line lies inside the span of a parsed ID (the Revision 2 and Revision 3 bullets that carry R-nnn or REQ-09): INF-036 (line 26), INF-037 (line 26), INF-038 (line 28), INF-039 (line 28), INF-040 (line 29), INF-041 (line 29), INF-042 (line 29), INF-043 (line 30), INF-044 (line 31), INF-045 (line 31), INF-046 (line 31), INF-047 (line 31), INF-048 (line 31), INF-049 (line 32), INF-050 (line 32), INF-051 (line 32), INF-052 (line 33), INF-053 (line 33), INF-054 (line 33), INF-055 (line 33), INF-056 (line 34), INF-057 (line 34), INF-058 (line 34), INF-059 (line 34), INF-070 (line 44), INF-071 (line 45), INF-072 (line 45), INF-073 (line 46), INF-074 (line 46), INF-075 (line 47), INF-076 (line 47), INF-077 (line 48), INF-078 (line 48), INF-079 (line 50), INF-080 (line 50). Their content was checked by hand against the plan (the revision check table in the report).

Supplemental rows (the Pass 2 agent produced none for these requirement-bearing spans of `source.md`, found by the qa reviewer; added by the orchestrator, quotes verbatim):

| Id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| SUP-001 | Task 1 runs its go and stage 0 summary checks before it creates `SKILL.md` | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:51 | manual: Task 1 (PLAN:36) |
| SUP-002 | `verify` is now `verify-citations` in Task 12 | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:52 | manual: Task 12 (PLAN:192) |
| SUP-003 | Task 2's self-cancelling grep line says "prints nothing" | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:52 | manual: Task 2 (PLAN:52) |
| SUP-004 | Task 9 keeps its constant off the names `THRESHOLDS` and `CONVERGENCE_THRESHOLDS` | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:53 | manual: Task 9 (PLAN:151) |

## Revision check (the dropped rows of Revisions 2 and 3, read against the plan)

| Source bullet | Plan lines that carry it |
|---|---|
| Revision 2 F1 and Revision 3 M-F1 (Task 7 grep) | PLAN:129 |
| F2 (stoprule row `installed-only`) | PLAN:64, PLAN:70, PLAN:234 |
| F3 (allow-list holds `remediate_parser.py`, `fmea_classifier.py`) | PLAN:66, PLAN:74 |
| F4 and decision 5 (separate ledger, audit verdict to the owner) | PLAN:22, PLAN:124, PLAN:248 |
| F5 and M-F2 (scale-map grammar, three rules) | PLAN:62, PLAN:151, PLAN:234 |
| F6 and F7 (Task 10 depends on 7 and 9; `run_questions`, `questions_to_ask`) | PLAN:151, PLAN:164, PLAN:166, PLAN:204 |
| F8 and F9 (full grep path; seven subcommands named; `sweep-flagged`) | PLAN:52, PLAN:82, PLAN:192 |
| Decision 1 (retired carriers `exempt-by-retirement`) | PLAN:24, PLAN:66, PLAN:248 |
| Decision 2 (`/sc:implement` final review step records and prints only) | PLAN:25, PLAN:82 |
| Decision 4 (no plugin surface) | PLAN:26, PLAN:109, PLAN:234, PLAN:248 |
| M-F3 (REQ-09 `earlier_decisions`) | PLAN:124 |
| M-F4 (M precheck, D inputs, `questions_to_ask`) | PLAN:166, PLAN:192 |
| M-F5 (`classifier-results.json`, `update_field`) | PLAN:124, PLAN:192 |
| M-F6 (injected resolver, by-path load) | PLAN:137, PLAN:141 |
| M-F7 (no `.dev/` or `src/superclaude` path in the new refs) | PLAN:82, PLAN:90, PLAN:99, PLAN:100, PLAN:115 |
| M-F8 (entry gate before `SKILL.md`) | PLAN:36 |
| M-F9, M-F10 (nits, `THRESHOLDS`, `make lint` lines) | PLAN:52, PLAN:72, PLAN:131, PLAN:151, PLAN:160, PLAN:173, PLAN:192, PLAN:200, PLAN:213 |
| Stage 2 and stage 4 fix-cycle additions (`write` never clears capture state; `STRICT_T2`) | PLAN:130, PLAN:234 |

## Findings

Severity follows the rule in the reviewer briefs: blocking means an executor following the plan as written cannot meet a stated requirement or acceptance check, or would produce a wrong or missing result, or data loss; minor means wording, format or a real but non-blocking weakness. Full text with all citations: `adversarial/merged-review-card.md`.

| # | Blocking | Finding |
|---|---|---|
| N-F1 | yes | Task 3 gives no outcome values for the `lens-scale` labels (`PLAN:62`, `PLAN:71`); stage 2 sets every imported row's tier from that cell with no `Conditional` rule (`STAGE2:57`). One cell has two readers (the importer and `ReviewerJudge` with the Task 12 matrix); three fixed values do not repair it. One owner decision, two forms |
| N-F2 | no | Task 9 takes the family key from the ledger row's `origin` (`PLAN:151`), a protocol name plus finding id (`SPEC:353`), not one of Task 3's 12 keys |
| N-F3 | no | The `unsettled` tag for a SHOW_USER verdict (`SPEC:369`, `SPEC:596`) has no producer in any plan (only `PLAN:87`) |
| N-F4 | no | No supplier of the NA marker for C (`PLAN:166`, `SPEC:528`); REQ-18 then lifts most verdicts to SHOW_USER (`SPEC:543`) |
| N-F5 | no | REQ-11 consent logic and the Offers table have no owner, yet T8 tests them (`PLAN:137`, `SPEC:375`, `SPEC:923`, `SPEC:945`) |
| N-F6 | no | Task 12 names no inputs for its command (findings layout, judge-answers file format, deliverable and kind, ledger path) (`PLAN:192`) |
| N-F7 | no | `PLAN:124` tests that `earlier_decisions` "does not return a `pending` row", but `pending` is an Offers state, not an item state (`SPEC:375`, `SPEC:381-390`) |
| N-F8 | no | Two stage 2 sentences quote stage 1 text that no longer exists or will go stale (`STAGE2:27`, `STAGE2:57`) |
| N-F9 | no | Task 14 may put the literal fence text into `doctor.py`, which Task 15's T2 then flags (`PLAN:222`, `PLAN:234`, `PLAN:238`, `STAGE4:114`) |
| N-F10 | no | `STRICT_T2` is named but its effect is not stated (`PLAN:234`, `STAGE4:114`) |
| N-F11 | no | The new skill text is not checked against the banned-phrase scans of `tests/skills/test_review_severity_rule.py` during stage 1 (`PLAN:30`, `PLAN:66`) |

### Reviewer disagreement, as settled by the debate

- N-F1 (C-001): reviewer 1 graded it blocking (closest call); reviewer 3 graded it non-blocking and its advocate withdrew that in Round 1; reviewer 2 did not raise it, and its advocate called it a qualified additional blocker. Final: blocking, 3 of 3 advocates (55, 76, 65 percent).
- N-F2 (C-002): reviewer 2 graded it blocking; reviewers 1 and 3 non-blocking. Advocate 2 conceded in Round 2 that no named exit test or acceptance line fails and that `ReviewerJudge` feeds no stage 2 figure (`STAGE2:28`, `STAGE2:135`). Final: non-blocking, 2 of 3.
- N-F3 (C-003): reviewer 2 graded it blocking; advocate 1 held non-blocking in both rounds (55, then 68 percent) and advocate 3 moved from blocking (Round 1, 60 percent) to non-blocking (Round 2, 65 percent) because no stage 1 requirement or exit test needs the tag (`SPEC:945`, `SPEC:946`); advocate 2 kept it blocking. Final: non-blocking, 2 of 3; it needs an owner (note).
- N-F5 (C-005): the fault-finder asked for blocking (INV-003); kept non-blocking because T8 can be met by building consent into the filing code, with the repair added.
- Invariant probe (Round 2.5): 8 findings, 2 HIGH unaddressed (INV-001, INV-002, both on the N-F1 repair, cleared by rewriting the repair), 2 MEDIUM (INV-003 into N-F5, INV-004 into N-F3), 4 LOW or addressed.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: 0 / citations_total

## Recommendations

### Recommendation R-001: Fix the lens-scale cell with one owner decision (N-F1)

- **File:** `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`, Task 3 (`PLAN:62`, acceptance `PLAN:69-76`), with a matching sentence in the stage 2 plan Task 2 (`STAGE2:57`)
- **Change:** Task 3 states the values of the `lens-scale` labels in the `labels` cell and a `model` cell saying what they mean to each reader. Form 1: `CRITICAL=Blocking;IMPORTANT=Blocking;MINOR=Medium` plus a stage 2 note that the importer takes blocking or non-blocking from the reviewer's own call (a filled `why not blocking`); under form 1 no label maps to Note and IMPORTANT holds Blocking, so the owner must also say what a reviewer-minor IMPORTANT row gets (for example Medium, with its `why not blocking` required). Form 2: a second column so each reader reads its own value. Add an acceptance line asserting the chosen pairs.
- **Verifier:** `grep` of the finished `refs/scale-map.md` row shows the three pairs; the stage 2 `write` test over a fixture with one MINOR row, one IMPORTANT row the reviewer graded minor and one the reviewer graded blocking gives, for each, the outcome the chosen form states.
- **Linked deviation(s):** N-F1
- **Priority:** P0

### Recommendation R-002: Give Task 8 and Task 7 the consent and Offers behaviour, and fix the `pending` wording (N-F5, N-F7)

- **File:** same plan, Task 8 (`PLAN:137`) and Task 7 (`PLAN:124`)
- **Change:** filing is refused unless an Offers row with an explicit filing answer and a matching `set_digest` exists; a resume returns the pending offer without asking; a changed set or body digest needs a new offer; in the `earlier_decisions` test say "a `recorded` or `offered` row".
- **Verifier:** Task 8's tests call a named consent check; `grep -n "pending" ` over Task 7 finds no item-state use.
- **Linked deviation(s):** N-F5, N-F7
- **Priority:** P1

### Recommendation R-003: Guard the doctor literal and name the strict switch (N-F9, N-F10)

- **File:** same plan, Task 14 (`PLAN:222`) and Task 15 (`PLAN:234`, `PLAN:238`)
- **Change:** build the fence marker in `doctor.py` from parts and add the acceptance line `grep -n "review-severity:digest" src/superclaude/cli/doctor.py` prints nothing (valid until stage 4); say that with `STRICT_T2` true a registered file that holds the old sentence also fails, with a temporary-tree case for both modes.
- **Verifier:** the two lines appear in the plan; T2 passes at `legacy`.
- **Linked deviation(s):** N-F9, N-F10
- **Priority:** P1

### Recommendation R-004: Settle the family key and the classifier inputs (N-F2, N-F6, N-F4)

- **File:** same plan, Task 3 (`PLAN:62`), Task 9 (`PLAN:151`), Task 10 (`PLAN:166`), Task 12 (`PLAN:192`)
- **Change:** a `reviewers` column in the scale map (for example `rf-qa` to `lens-scale`) and key resolution from the reviewing agent in `source`; name the Task 12 options (`--findings`, `--judge-answers`, `--deliverable`, `--kind`, `--ledger`, `--out`) and the `FixtureJudge` file format; return a "no constraint list" NA marker for C or record the SHOW_USER consequence in the Task 16 summary.
- **Verifier:** a Task 11 case for an origin that matches no key; the Task 12 help text lists the options.
- **Linked deviation(s):** N-F2, N-F4, N-F6
- **Priority:** P2

### Recommendation R-005: Add the `unsettled` owner and the banned-phrase check (N-F3, N-F11)

- **File:** same plan, Task 12 (`PLAN:192`) and Task 5 (`PLAN:99-103`)
- **Change:** Task 12 adds `unsettled` through the sole writer without clearing tags (or the stage 2 revision owns it); Task 5 gets one acceptance grep of the `BANNED_SEVERITY_PHRASES` and `SWEEP_PHRASES` lists of `tests/skills/test_review_severity_rule.py` over the skill folder that must print nothing.
- **Verifier:** both lines appear in the plan.
- **Linked deviation(s):** N-F3, N-F11
- **Priority:** P2

### Recommendation R-006: Reword the two stale stage 2 sentences (N-F8)

- **File:** stage 2 plan `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md` (`STAGE2:27`, `STAGE2:57`)
- **Change:** say that from Task 10 stage 1 lists `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`, and that the tuple holds ten names after stage 1.
- **Verifier:** a re-read of the two lines.
- **Linked deviation(s):** N-F8
- **Priority:** P2

## Run notes

- Panel: reviewer 1 analyzer/sonnet, reviewer 2 qa/haiku pin, reviewer 3 refactorer/opus, all spawned as the read-only `reflect-reviewer` agent type with a model override; blind calibrators opus class; advocates sonnet, haiku and opus (general-purpose agents); qualitative scorers sonnet class (`judge_class_collision: true`: the judge class overlaps variant 1, the selected base); fault-finder and merge-executor opus class; requirements-analyst for Pass 2.
- Deviations from the protocol: the live `sc-adversarial-protocol` probe was folded into the real Skill call (it loaded, so the F1/F2/F3 fallback did not fire); the T1 card, the diff analysis, the quantitative scoring and the refactor plan were written by the orchestrator (no separate analytical-agent review of the plan); advocate statements are persisted in condensed form under `adversarial/adversarial/debate/` (per-point tables and A-NNN answers kept in full); the orchestrator wrote the reviewer cards, calibration blocks and debate files from agent hand-backs; Wave 1A used targeted reads, two read-only batch scripts, one path scan with `uv run python` and one `codegraph_status`, with no lookup beyond them and no degraded token. A turn of the run stopped on the user's rejection of one tool call and resumed on the owner's approval relayed by the team lead.
- Reviewer-isolation snapshot (`--isolate-reviewers`) was not used: reviewers read the live tree. Input-tree drift guard: the 18-file tree hash `8ed58ea33aa60dd0c0708121023253e8ab23cb743919d047df97be5f2fc78ed7` was recomputed at Wave 5 and is unchanged (audit.log step `5.x-drift-guard`). The context file `OPEN-QUESTIONS.md` (not part of the tree; sha256 `893c56f3...` at the Wave 5 recompute, a different value from the start-of-run hash in the snapshot) changed on disk during the run; the review used the version read at the start.
- Memory: not written. The team lead restricted output to this run folder, so no last-pass note, no deviation-patterns update and no `.dev/reflect/runs.jsonl` append were made.
- The qualitative scoring and base selection rest on sonnet-class scorers (the class of the base variant) and on a keyword-based quantitative layer whose specificity metric saturates; the 2.2 percent margin between variants 1 and 3 was settled by debate points (8 against 5). Treat the ranking as weak evidence: the findings, not the ranking, carry the verdict.

<!-- END REPORT BODY -->
