# Spec errata: what Task 3 changed in the merged spec

File edited (the only file outside `./artifacts/` that this package edits):
`.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`.
Old text is the file as it stood before Task 3 (saved copy used for the diff: `./artifacts/spec-before-errata.md`, taken from the working tree before the first edit; the file had no uncommitted change, `git status` showed it clean); new text is the file now. Line numbers: "old" lines are before, "new" lines after the edits. Eleven hunks, 12 insertions and 9 deletions by `git diff --stat`.

## Edit list

| # | Where | Edit |
|---|---|---|
| 1 | line 7 (new), directly under the `Date:` line | one line added: "Version 1 scope: see cuts-debate/final-cuts.md in this folder" (the file `cuts-debate/final-cuts.md` exists in the program folder) |
| 2 | section 7.2, new lines 521 to 522 | one sentence: M, C and E are answerable only with code-supplied inputs; cites `08-test/results.md` only |
| 3 | section 7.4 thresholds bullet, old 572 | reworded without a held-out set; the table has 318 rows |
| 4 | section 7.6 "Table" row, old 604 | the table exists: 318 findings, threshold 4, 82 blockers |
| 5 | section 7.6 "Missing table" row, old 609 | not applicable: the table exists, steps 0a and 0c are not skipped |
| 6 | section 12 stage 0 row, old 944 | "only if the table exists" removed at 0a and 0c; "when the table exists," removed from the exit condition |
| 7 | section 12 stage 3 row, old 947 | exit condition now "one audit window (section 8.2) with RT1 not tripped"; "M12 reported" dropped; RT2 not named |
| 8 | section 13.2 RT1 row, old 985 | trigger "Any real blocker found in a Medium list"; detects "a real blocker graded Medium"; the note column is unchanged |
| 9 | section 14 RK8, old 1011 | 30 to 40 rows replaced by the 318 scored rows; mitigation no longer says "held-out half" |
| 10 | section 14 RK15 mitigation, old 1018 | `M10b` dropped from the end of the mitigation |
| 11 | section 17.3, old 1108 | clause "whether a calibration table of 30 or more scored findings will exist in time" removed |

Old and new text of every changed line (normal `diff`: `<` old, `>` new, hunk header = old line then new line):

```diff
6a7
> Version 1 scope: see cuts-debate/final-cuts.md in this folder
519a521,522
> M, C and E can be answered only when code supplies their inputs (the required-item list for M, the constraint lines for C, the verified-or-not mark on the excerpt for E): with only a description and a context line they were at chance in the text-only variant of the 5-run test (`08-test/results.md`).
> 
572c575
< - **Thresholds.** The asymmetry stays: a downgrade needs a higher bar than a confirm (placeholders `tau_down` 0.85 and `tau_block` 0.70 from `jev-uses.md`), fitted on one half of the scored table and checked on the other half. With 30 to 40 rows the held-out half is 15 to 20 rows, so report counts, not percentages alone. In version 1 the thresholds route nothing, because the classifier has no authority (section 7.5); they are measured for OD4.
---
> - **Thresholds.** The asymmetry stays: a downgrade needs a higher bar than a confirm (placeholders `tau_down` 0.85 and `tau_block` 0.70 from `jev-uses.md`), fitted on the scored table (318 rows, panel threshold 4) with no held-out set, so the fit and the check use the same rows; report counts, not percentages alone. In version 1 the thresholds route nothing, because the classifier has no authority (section 7.5); they are measured for OD4.
604c607
< | Table | at least 30 past blocking findings, each scored blind 1 to 5 by three independent agents, averaged, with a minimum blocking threshold [per `00-issue-description.md`] |
---
> | Table | the scored table exists: 318 past blocking findings (`04-historical/master-table.md`), each scored blind 1 to 5 by three independent agents and averaged (`05-scoring/consensus.md`), with a minimum blocking threshold of 4 (mean 4.0 or higher; 82 blockers) |
609c612
< | Missing table | the scored table is produced by another program step and was empty when this spec's inputs were written (`seed-brief.md:25`). If it does not exist at stage 0, steps 0a and 0c are skipped and every classifier stage waits; the rule and loop changes do not depend on it (section 12) |
---
> | Missing table | not applicable: the table exists and scored 318 findings with threshold 4 (`05-scoring/consensus.md`), so steps 0a and 0c are not skipped; the rule and loop changes do not depend on it (section 12) |
944c947
< | 0. Measure (this program, offline) | this spec reviewed | 0a: the scored table and five runs with a fixture or approved judge, only if the table exists. 0b: the retrospective escape test on run 2 (section 8.4). 0c: three blind agents that did not write the rule re-grade the table under the old and the new text, paired, only if the table exists. Inventory freeze: every Grep of section 10 re-run, including the frozen FAIL-trigger Grep (REQ-30), with results stored | a written result: escape estimate with its interval; when the table exists, how many old-blocking rows become non-blocking and the confusion matrix | nothing changed |
---
> | 0. Measure (this program, offline) | this spec reviewed | 0a: the scored table (it exists: 318 rows) and five runs with a fixture or approved judge. 0b: the retrospective escape test on run 2 (section 8.4). 0c: three blind agents that did not write the rule re-grade the table under the old and the new text, paired (the table exists). Inventory freeze: every Grep of section 10 re-run, including the frozen FAIL-trigger Grep (REQ-30), with results stored | a written result: escape estimate with its interval; how many old-blocking rows become non-blocking and the confusion matrix | nothing changed |
947c950
< | 3. Pilot | 0b result written; at least 5 shadow runs observed with zero safety misses and no capture failure (an observation minimum, not a safety claim); seeded recall (section 8.3) met; 0c as well when the table exists; owner go | `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md` move to digest v2 together; the stage 3 merge-rule lines of section 10.3 (task skill, rf-qa, rf-qa-qualitative, rf-analyst; L1); L2 fix-pass checks; L6 for rf-qa, and Rule 6 if OD16 chooses (b), with its test re-pinned in the same change; the cadence pins move | one audit window (section 8.2) with no revert trigger tripped; M12 reported | the three-step revert of the pilot rows to `legacy` |
---
> | 3. Pilot | 0b result written; at least 5 shadow runs observed with zero safety misses and no capture failure (an observation minimum, not a safety claim); seeded recall (section 8.3) met; 0c as well when the table exists; owner go | `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md` move to digest v2 together; the stage 3 merge-rule lines of section 10.3 (task skill, rf-qa, rf-qa-qualitative, rf-analyst; L1); L2 fix-pass checks; L6 for rf-qa, and Rule 6 if OD16 chooses (b), with its test re-pinned in the same change; the cadence pins move | one audit window (section 8.2) with RT1 not tripped | the three-step revert of the pilot rows to `legacy` |
985c988
< | RT1 | Any safety-class escape in the audit or the seeded set, or any confirmed safety finding that ended as a plain follow-up | a Safety finding graded Medium or Note | a single event; needs no sample size; acts through the three-step revert |
---
> | RT1 | Any real blocker found in a Medium list | a real blocker graded Medium | a single event; needs no sample size; acts through the three-step revert |
1011c1014
< | RK8 | Over-fitting the classifier to 30 to 40 rows; circular rubric. | medium | medium | section 7.6 | held-out half; independent scoring rubric; contested rows reported apart |
---
> | RK8 | Over-fitting the classifier to the 318 scored rows (the fit and the check use the same rows); circular rubric. | medium | medium | section 7.6 | counts reported with the fit rows named; independent scoring rubric; contested rows reported apart |
1018c1021
< | RK15 | During stage 3 one reviewer context holds two definitions (the v2 output style and a legacy carrier, or the reverse on a stale install) and the model blends them. | certain during stage 3 | medium | the output style is injected into every subagent [V: LC-09] | precedence sentence (REQ-03); `pragmatic.md` and the rf-qa family switch together; M10b |
---
> | RK15 | During stage 3 one reviewer context holds two definitions (the v2 output style and a legacy carrier, or the reverse on a stale install) and the model blends them. | certain during stage 3 | medium | the output style is injected into every subagent [V: LC-09] | precedence sentence (REQ-03); `pragmatic.md` and the rf-qa family switch together |
1108c1111
< - The 44-defect ledger artifact named as a recall candidate; whether a calibration table of 30 or more scored findings will exist in time; whether templates expose required sections in a form code can read; whether the output-style hook is registered in every environment.
---
> - The 44-defect ledger artifact named as a recall candidate; whether templates expose required sections in a form code can read; whether the output-style hook is registered in every environment.
```

## Re-run of the search for "empty or absent" in section 17 and Appendix A

Command (plain grep, case-insensitive, from the start of section 17 to the end of the file):

```bash
awk 'NR>=1057' .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md | grep -n -i "empty\|absent\|no table\|not exist"
```

Before the edits (spec of that time, run from the saved copy) the command returned two lines, neither about the scored table:

    82:| LC-20 | list skill folders | `sc-review-severity` absent; the plugin holds 4 skills |
    117:| INV-009 | Deferring unknown-consequence findings assumed a final-gate sweep that does not exist | REQ plus OD14, sections 4.1 and 15 | REQ-02: "If no consumer can be established, keep the review

- LC-20 says the skill folder `sc-review-severity` is absent (a check of the repository, not the table). INV-009 says a final-gate sweep does not exist (not the table). Result for the table: none found. The only table statement in section 17 was the 17.3 clause removed by edit 11.

Stale-claim check required by the acceptance criteria, run on the edited spec:

```bash
grep -n "15 to 20\|was empty\|30 to 40 rows\|30 or more scored" .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md
```

Result: no match (grep exit code 1).

## Things left as they are (outside this errata's scope)

- Section 12 stage 3 entry condition still reads "0c as well when the table exists" (now line 950, same row as edit 7). The edit list for this package changes only that row's exit condition, so the entry cell is untouched; it is harmless because the table exists.
- The definitions of M10b and M12 (section 13.1) and the cut machinery stay as written; the new scope line at the top points the reader to the cuts list. No definition, exit number or staging decision was added.
- Two other uses of "held-out" (section 8.3 planted defects in a held-out deliverable, and a behavioural-replay sentence near section 11) mean something else and are unchanged. "About 30 to 40 source files" in section 10 is a size estimate, unchanged.
- Section 15 (owner decisions OD1 to OD17) still shows the earlier recommendations. The coordinator message of 2026-11-16 (21:37 UTC) says `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/OPEN-QUESTIONS.md` is the record of the owner's decisions and supersedes section 15 until this errata edits the spec. This note is where that is recorded; the spec's section 15 was not edited because it is not in this task's edit list. Per that file: decided OD1 (no new folder), OD2, OD5, OD9, OD11, OD12, OD15 (shrunk), OD16 (option b), the Review Panel exit-code numbers, the quorum denominator and the plugin twin copy; deferred OD3 and Jev, OD6, OD7, OD14, per-seat configuration, over-cap behaviour and the post-gate engine; dropped OD4 as a question, OD8, OD10, OD13, OD17, the replace-or-augment ledger question and the ledger version skew.
