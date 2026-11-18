# Entry check for stage 3 (read from files, 2026-11-17)

Format per line: condition | file read | what it said | result.

## Task 1 (before any file under src/ or tests/)

1. Stage 0 regrade exists | `.dev/tasks/done/TASK-WF-blockerStage0-20261116-021044/artifacts/stage0c-regrade.md` | the file exists (15583 bytes); the package is in `done/`, which the plan allows ("to-do or done subfolder") | PASS
2. Stage 1 package is done | `.dev/tasks/done/TASK-WF-stage1Request-20261116-221852/progress.md` | the package sits in `done/`, holds a `complete` line for T1 and T2 and a `FINAL: pass` line. The plan text names the id `TASK-WF-blockerStage1-20261116-030154`; that package is archived at `.dev/tasks/archive/to-do/` and superseded, and the ledger row of `stage-requests/README.md` names `TASK-WF-stage1Request-20261116-221852` as the stage 1 package | PASS (read against the real stage 1 package; the plan's id is stale)
3. Spec RT1 row reworded | `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` line 988 | the row reads "Any real blocker found in a Medium list" (capital A). `grep -c -F "any real blocker found in a Medium list"` prints 0 only because of the capital letter; `grep -c -i -F` prints 1 | PASS (case difference only; the words are the plan's)
4. Owner go for stage 3 recorded with a date | `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md` line 20 | the stage 3 row holds "2026-11-17, owner in chat ("Start stage 3")" | PASS

Note: the Task 1 acceptance line says "three entry conditions"; the Constraints name four (regrade, stage 1 done, RT1 row, owner go). All four are listed above.

## Task 2 re-read of the entry conditions (2026-11-17)

Order of events, stated plainly: the four conditions were read at Task 1 a few minutes before the pragmatic.md edit and nothing under them changed in between, but this written re-read was run right after the edit, not before it. The plan asks for the re-read before the edit; that step was done late. The result below is what the same four files say now.

Same four files as Task 1 read again: the stage 0 regrade file exists; the stage 1 package `TASK-WF-stage1Request-20261116-221852` is in `done/` with its `FINAL: pass`; `grep -c -i -F "any real blocker found in a Medium list"` over the spec prints 1 (the spec row has a capital A); `stage-requests/README.md` line 20 holds the go dated 2026-11-17. Result: PASS for all four, so the edit stands.

## Mapping of the REQ-01 block onto the five bullets of pragmatic.md, as applied

- Position 1 (opens "Grade every review finding as blocking or minor."): the REQ-01 sentence "Grade each finding by what changes if the flawed text is corrected", the three conditions inline and named **Decision**, **Missing** and **Safety** with their required wording (the wrong-number acceptance-check sentence and "An unverified safety claim stays open for verification; it is not a Note."), and the sentence "Unknown is not no. If no consumer can be established, keep the reviewer's own label and tag the row `consumer-unknown`."
- Position 2 (opens "Minor findings never fail a review:"): the old first sentence kept, then "Everything else is recorded and never blocks, never starts a fix pass and never appears in a reviser brief", the Medium and Note definitions, the sentence that the label a reviewer used is information and never the grade (apart from the unknown-consumer case), "Only blocking findings produce FAIL." kept, then "Medium and Note findings are not rechecked in later rounds." (spec L5).
- Position 3 (cap bullet): unchanged word for word.
- Position 4 (own-scale bullet): unchanged word for word.
- Position 5 (opens "On a CRITICAL / IMPORTANT / MINOR scale,"): the label is information, an IMPORTANT finding that is only wording is a Note, with the unknown-consumer exception; then the REQ-03 precedence sentence word for word.
- Also changed: the reviewer brief bullet now names the consequence of each defect and no longer says "false claims" (it keeps "never to meet a quota"); the Medium bullet now reads "asks the user once per run, and again at any escalation halt, whether to open an issue for the list" (OD2).

`tests/skills/test_review_severity_rule.py` is red from this task until Task 3 copies the new bullets into the ten carrier files. It was not run here.

## Task 2 re-read of the entry conditions, repeated before the edit is applied again (2026-11-17, fix pass after review r1-1)

The first review found that the re-read above ran after the edit. The fix: `pragmatic.md` was set back to its start-snapshot text (it holds "Blocking is a real defect" again, once), the four conditions were read again, and only after this entry is written is the same edit put back (a byte copy of the first edit, kept at `./artifacts/retries/T2/pragmatic-after-first-edit.md`). Read now: the stage 0 regrade file exists (15583 bytes); the stage 1 package `TASK-WF-stage1Request-20261116-221852` in `done/` holds 2 `complete` lines and 1 `FINAL: pass`; `grep -c -i -F "any real blocker found in a Medium list"` over the spec prints 1; `stage-requests/README.md` line 20 holds "2026-11-17, owner in chat". Result: PASS for all four, written before the edit.
