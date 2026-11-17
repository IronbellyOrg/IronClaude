# Round 1: Advocate for Variant 3 (reviewer 3, refactorer, opus class)

- Subject: stage 4 plan `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md` (P4:n = its line n)
- S1 = stage 1 plan `TASK-WF-blockerStage1-20261116-030154/...md`; S3 = stage 3 plan `TASK-WF-blockerStage3-20261116-030158/...md`; SRC = `TASK-WF-blockerStage4-20261116-030206/source.md`
- Every cited line was re-read in this round (2026-11-16).
- Grading rule: blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss; minor = wording or format.

## Position summary

Variant 3 is right on the one defect all three found (C-001, Task 1's audit-window line cannot be met) and adds the only step-by-step walk of Task 6, which surfaces two real Task 6 weaknesses no one else saw (C-013 vacuous reverse-scan claim, C-014 registry row model). Variant 3 missed C-002: after re-reading the mapping test I accept it as blocking, and Variant 3's "files edited by several tasks end up consistent" is too strong for the spec-panel and rules-prompt twins.

## Steelman

### Variant 1 (analyzer, sonnet)
Strongest version: the plan's acceptance lines can all pass while the repository's own pinning tests go red, because Task 5 deletes text that `tests/skills/test_review_severity_mapping.py` pins, and no stage 4 task runs that test. This is the most consequential finding in the three cards and it was found by reading the tests directory, not the plan. V1 also found the byte-identity test for the plugin rules prompt (`tests/skills/test_review_brief_placement.py:134` `assert bundled.read_bytes() == RULES_FILE.read_bytes()`; the two files are byte-identical today, checked with `cmp`), and the case-sensitivity trap in Task 3 (`src/superclaude/skills/tdd/refs/build-request-template.md:125` has only lowercase "after 2 fix cycles"). What it gets right: it reads the plan against live tests, which is the right grounding for a pre-execution review.

### Variant 2 (qa, haiku class, self-reported GPT-5)
Strongest version: the plan was produced out of order. SRC:3 says "Generate it only after the stage 3 package is done ... and the owner's go in chat is recorded in the stage ledger", and the ledger rows for stages 3 and 4 are empty (`stage-requests/README.md:20-21`). V2 also did the only task-by-task comparison against base Tasks 41 to 46 and checked the earlier findings F3 to F13 one by one, and caught that Task 2 has no cap-sentence pin although SRC:12 asks for "the cap sentences kept by content" (the four rule prompts do hold a cap bullet next to the digest area, e.g. `src/superclaude/rules/prompts/automated_qa_workflow_qa_prompt.md:13`). What it gets right: requirement traceability to the request text, which neither V1 nor V3 did.

## Strengths claimed (Variant 3)

1. **C-001 with the right remedy.** P4:37 requires the stage 3 summary to state "that one audit window has passed with no revert trigger tripped". S3:158 tells that same file to "State that the audit window runs after this package" and S3:162 makes it say "no revert trigger can be judged until the audit window has run". The file is written before the window, so the line can never be true. V3 alone names the record that does exist after the window: the owner's go row (P4:36, P4:20 "the owner has read the stage 3 summary and said go in chat"). That turns the finding into a one-line fix (check the go row's text, or a separate window record), not just a complaint.
2. **C-013, the reverse-scan claim tests nothing as ordered.** S1:209 defines T2 as "a reverse scan of the tracked `src/` and `plugins/` trees", and the existing scan in the same test family enumerates files with `git ls-files` (`tests/skills/test_review_severity_rule.py:39`). Task 6 copies a new, untracked folder (P4:99 "copy ... by hand") and runs the tests (P4:99 "then the three tests together") with no staging step; staging is only implied later by P4:105 (`git diff --cached`). So P4:102 "the plugin mirror of `refs/rule.md` is accepted by the reverse scan through its `canonical` row" is green because the scan never sees the file. Once the folder is staged or committed (CI), T2 reads it for the first time, so a wrong `canonical` row (see C-014) would be green locally and red in CI.
3. **C-014, registry row model mismatch.** S1:96 says "Each row has the logical path relative to the install root, a `kind` ..., surfaces (source, installed, project `.claude/`, plugin, ...)". P4:99 adds the plugin mirror "(`plugins/superclaude/skills/sc-review-severity/refs/rule.md`) as a `canonical` row", i.e. a repo path, while the model already has a `plugin` surface value. Two equally valid readings (new row vs. add `plugin` to the existing row's surfaces) leave T1/T2 path resolution to the executor's guess.
4. **Task 6 walk-through (U-006).** The only card that checks the end state step by step: 11 files hold the old sentence today, all under `src/superclaude` and none under `plugins/superclaude` (re-run of the grep this round lists exactly the 11 `digest` carriers of S1:96), `verify-sync` never reads `plugins/` (`Makefile:166` onward has no `plugins` reference; the only hits are lines 20, 39, 65), and the plugin `skills/` holds 4 entries plus `__init__.py` (listed this round). This is what makes P4:103 and P4:104 credible.
5. **C-003 and C-006 agree with V1 independently.** V3 F5 and V1 F3 both found that "the allow-list of the stage 3 scan test" (P4:33, P4:59) is really the "Merge-rule allow-list" section of `refs/scale-map.md` (S1:59, S3:144); V3 F4 and V1 F6 both found that `test_review_severity_rule.py` is never run in stage 4 although S3:122 re-pins it to the registry's `digest` rows, which Task 6 flips to `v2`.

## Weaknesses identified

### In Variant 1
- **F5 (C-005) is a sub-case of F2, not a separate defect.** The grep at P4:89 is file-wide, so it forces an edit at `src/superclaude/commands/spec-panel.md:332` (FR-8). The FR-8 pin at `tests/skills/test_review_severity_mapping.py:101-103` only needs "otherwise it is Medium" and "graded like FR-8", which survive deleting the parenthesis. It belongs under C-002 as one more pinned spot.
- **F2 overstates certainty.** S3:122 re-pins this very test: "the Medium and cadence pins move from 'once per loop' to the once-per-run wording and to assertions on `refs/rule.md` and `refs/scale-map.md`", and the spec's test table (`02-brainstorm/merged-requirements.md:900`) says "literals move to assertions on `refs/rule.md` and `refs/scale-map.md`". If stage 3 is executed that way, the spec-panel literals at test:58 and test:71 may already be gone before stage 4. The defect survives (see Concessions), but it is a dependency on how S3 Task 8 is read, which V1 does not state.
- **F8 (C-008) is minor at most.** The edits land on disk before the go check is read, but nothing is committed or lost; P4:36 still halts the run.

### In Variant 2
- **D1 (C-010) mis-grades a process fact as a plan defect.** The plan cannot change when it was generated, and it already gates execution on the same preconditions (P4:20, P4:36). No executor result is wrong because of the generation time; line anchors are re-read before editing by P4:24. V2's own table says MEDIUM, contradicting its "blocking true" (S-002, X-003).
- **Missed both test-pin defects.** V2 says "No later task here falsifies an earlier task's stated acceptance line" (variant-2:55), which is true of acceptance lines but misses that Task 5 breaks tests no task runs (C-002, X-002).
- **Format.** Deviation-table format with two disagreeing severity labels per row (S-002) makes the merge harder; it also reports a model identity mismatch (variant-2:4).

## Concessions

1. **C-002: Variant 3 missed a blocking defect.** Verified this round:
   - Today both spec-panel files hold `follow-up candidates` in Review Loop bullets 2 and 3 (`src/superclaude/commands/spec-panel.md:259`, `:260`, `:332`; `plugins/superclaude/commands/spec-panel.md:257`, `:258`, `:330`).
   - The mapping test pins it in both files, parametrized over `SPEC_PANELS` (`tests/skills/test_review_severity_mapping.py:24-27`): bullet 2 must contain "otherwise it is Medium (a warning listed under `follow-up candidates`)" (`:58`), bullet 3 must contain "`follow-up candidates`" and "asks the user once per loop" (`:71-72`).
   - Task 5 must make `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` print nothing (P4:89) and applies "the same edits" to the plugin twin (P4:84). That removes the pinned literal from both surfaces, so 4 parametrized cases fail if the pins are still there.
   - No stage 4 task runs this test: P4:41, P4:55, P4:63, P4:74, P4:88 and P4:102 are the only pytest lines and none names it.
   - Does stage 3 remove the pins first? S3:122 moves "the Medium and cadence pins" from "once per loop" to the once-per-run wording and to `refs/rule.md` / `refs/scale-map.md`. It does not say the spec-panel `follow-up candidates` literals leave the test, and S3 edits no spec-panel text (the only spec-panel mention in S1 to S3 is the registry row at S1:96). So an executor of S3 can, and literally should, keep the spec-panel literal pins that still pass at stage 3. In that case Task 5 leaves the suite red, while every stage 4 acceptance line passes. That is a wrong result no check catches: blocking. One-line fix: add `tests/skills/test_review_severity_mapping.py` to P4:88 and have Task 5 re-pin its spec-panel literals to the ledger wording.
   - Variant 3's "Step 7: no failure expected apart from F2 and F3" was scoped to the three tests Task 6 names; it is not wrong about those three, but it is silent on the test that does fail.
2. **X-002: "files edited by several tasks end up consistent" is too strong.** `plugins/superclaude/rules/prompts/document_review_loop_prompts.md` is byte-identical to the source today (`cmp` this round) and `tests/skills/test_review_brief_placement.py:134` requires that. Task 2 edits the source (P4:50); Task 5 hand-edits the plugin twin with "the same edits" next to "edit each file in place and do not copy one over the other" (P4:84), and the brief-placement test is never run. Byte identity is reachable, so this stays minor, but Variant 3 did not check it.
3. **No requirement traceability.** Variant 3 did not compare the plan to SRC or the base tasks; V2's C-011 (SRC:12 cap sentences by content, no pin in P4:53-55) and the Task 7 ordering point (SRC:16 "ending with the sentence"; P4:111 lists the open items after it) are real minor gaps V3 missed.
4. **C-015 is speculative.** Variant 3's own text says a misplaced consumer line would be seen at Task 6 (T1 is in the P4:102 run). It is a late signal, not a missed one: minor.

## Shared assumptions

| A-NNN | Answer | Reason |
|---|---|---|
| A-001 | QUALIFY | A pre-execution review of stage 4 can only read S1 and S3 as the contract, since their tests do not exist yet. But each finding that rests on an S1/S3 text must say so: C-002 depends on how S3:122 is executed, C-013 on S1:209's "tracked", C-014 on S1:96's row model. C-001 rests on S3:158/S3:162, which define the very file P4:37 reads; it changes only if S3 is revised. |
| A-002 | QUALIFY | `/sc:implement` QA does not halt on every literal mismatch: only confirmed blocking findings fail an attempt or halt (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:93`, `:280`), a disputed AC halts as `dispute` (`:281`), and minors are recorded and cleared (`:274`). So literal-case points like C-004 stay minor, while C-001 halts under any reading because the file states the opposite of the check, not a different spelling. |
| A-003 | REJECT | P4:36 and P4:37 are two separate bullets: P4:36 checks the go row, P4:37 checks the stage 3 file and says it "exists and states". The author kept them apart, so P4:37 is meant as a check on the file. Even if the intent was the go row, QA reads the line as written (A-002), so it cannot be met: C-001 stays blocking, and the fix is to repoint it at the go row or a window record. |

## Per-point positions

| Point | Grade in merged review | Evidence |
|---|---|---|
| S-001 | drop | Card format differs (F-lines vs D-table); no effect on the plan's correctness. Merge in the F-line format the brief asks for. |
| S-002 | minor | V2 rows carry "MAJOR; blocking true" next to "Table severity: MEDIUM" (variant-2:21, :23); the merge uses the blocking flag and the grading rule, not the table column. |
| C-001 | blocking | P4:37 "states that one audit window has passed" vs S3:158 "the audit window runs after this package" and S3:162 "no revert trigger can be judged until the audit window has run"; the check cannot be met. Fix: check the owner's go row (P4:36) or a separate window record. |
| C-002 | blocking | `tests/skills/test_review_severity_mapping.py:58` and `:71` pin `follow-up candidates` in spec-panel bullets 2 and 3 of both surfaces (`:24-27`); P4:89 removes it; no stage 4 pytest line (P4:41, :55, :63, :74, :88, :102) runs the test; S3:122 does not drop those spec-panel literals. Red suite with green acceptance. |
| C-003 | minor | P4:33 and P4:59 say "allow-list of the stage 3 scan test"; the list lives in the "Merge-rule allow-list" section of `refs/scale-map.md` (S1:59, S3:144). |
| C-004 | minor | P4:64 quotes "After 2 fix cycles"; `src/superclaude/skills/tdd/refs/build-request-template.md:125` has only "after 2 fix cycles"; QA clears minors (qa.md:274). |
| C-005 | minor | P4:89's file-wide grep also reaches FR-8 at `spec-panel.md:332`; the FR-8 pin (`test_review_severity_mapping.py:101-103`) survives deleting the parenthesis. Fold under C-002. |
| C-006 | minor | `test_review_severity_rule.py` (re-pinned by S3:122 to the `digest` rows Task 6 flips to `v2`) and `test_review_brief_placement.py:134` are never run in stage 4; fix by adding them to the P4:102 run. |
| C-007 | minor | P4:90 expects "the same pointer ... as their source twins", but P4:84 never tells the executor to add a pointer to `spec-panel.md`, and T3 passes a `pointer-only` row without one (S1:211); the acceptance line tells the executor what to add. Also SRC:16 "ending with the sentence" vs P4:111 open items after it. |
| C-008 | minor | The go check (P4:36) is read after the Task 1 edits (P4:33); edits are on disk but uncommitted and the run still halts; no data loss. |
| C-009 | minor | "T1 passes" (P4:39) names no command; "contain the consumer-line instruction" (P4:73) quotes no text; conflicts with P4:24 "Pins are by content". |
| C-010 | minor | SRC:3 "Generate it only after"; ledger cells for stages 3 and 4 empty (`stage-requests/README.md:20-21`). The plan already gates execution on the same conditions (P4:20, P4:36), so no execution result is wrong. |
| C-011 | minor | SRC:12 "the cap sentences kept by content"; P4:53-55 has no cap pin, though the rule prompts hold a cap bullet next to the digest area (`automated_qa_workflow_qa_prompt.md:13`). |
| C-012 | minor | SRC:7 "Earlier stages' evidence is read by package id" is missing from the coverage matrix, but the plan implements it (P4:19). |
| C-013 | minor | S1:209 "reverse scan of the tracked `src/` and `plugins/` trees"; the test family lists files with `git ls-files` (`test_review_severity_rule.py:39`); P4:99 never stages the copied folder, so P4:102's "accepted by the reverse scan" tests nothing locally. Fix: stage `plugins/superclaude/skills/sc-review-severity/` before the test run. |
| C-014 | minor | S1:96 rows are "the logical path relative to the install root" with a `plugin` surface; P4:99 adds a second `canonical` row with a repo path; executor must guess. |
| C-015 | minor | Task 4 edits the MDTM templates after Task 1 placed the digest (P4:68-74) and runs only `test_task_builder_merge.py` (P4:74); a consumer line inside the fence breaks T1, seen only at Task 6 (P4:102). |
| X-001 | blocking | Resolves to C-002: V1 is right; V3's "no failure expected" (variant-3:27) covered only the three tests named at P4:102; V2's remark (variant-2:55) is about acceptance lines, not tests. |
| X-002 | minor | Plugin and source `document_review_loop_prompts.md` are byte-identical today and pinned so (`test_review_brief_placement.py:134`); P4:84 "edit each file in place" plus no run of that test makes divergence possible; V3's "consistent" claim (variant-3:6) is withdrawn for this pair. |
| X-003 | drop | Same defect as S-002 (V2's internal label mismatch); grade it once, under S-002. |
