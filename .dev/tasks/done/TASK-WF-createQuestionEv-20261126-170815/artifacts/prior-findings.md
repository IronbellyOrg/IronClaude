# Re-review 1 of the surgical repair (reviewer: reflect-reviewer, read-only; text saved by the coordinator)

Candidate: `.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170236/TASK-WF-createQuestionEv-20261126-170236.md`
Baseline: `.dev/tasks/archive/TASK-WF-createQuestionEv-20261126-142533/TASK-WF-createQuestionEv-20261126-142533.md`
Prior report: `.dev/reflect/pre-createQuestionEv-20261126142850/REPORT.md`

Prior blocking findings B-1, B-2, B-3, B-4: all resolved as worded.

## New findings

### NEW-1 (Blocking, Decision): the staging hold conflicts with the Tasks 6 to 8 acceptance checks and with the scope of Task 9's scan

- **Location:** candidate lines 125, 148, 157-158, 167, 178, 188, 191 against lines 28, 106, 131, 152, 173, 188, 202.
- **Evidence:** the run script writes its files into "the output directory" (line 125). Tasks 6, 7 and 8 set each run's output directory under `./artifacts/runs/` (lines 148, 167, 188) and their acceptance criteria require `summary.json`, the event log and the other raw files to exist under `./artifacts/runs/` when the task finishes (lines 157, 158, 178, 191). The repair lines say raw run output goes to the scratch directory instead and that Task 9 (which depends on Tasks 6 to 8) copies it later (lines 152, 173, 188, 202). Both cannot hold. Line 202 now scans only the scratch directory, where the baseline scanned `./artifacts/runs/`. An executor who follows the explicit output-directory arguments puts raw logs under `./artifacts/runs/`, where no scan reaches them, and the standing rule then stages them.
- **Fix (plan text):** say that each run's output directory is the scratch directory's `runs/<run name>` (the scratch directory is named in Task 4); change the Tasks 6, 7 and 8 acceptance checks to read the run files from there; keep Task 9's copy of the scanned runs into `./artifacts/runs/` and add that the evidence matrix cites the copies under `./artifacts/runs/`.
- **Verifier:** no line of Tasks 6 to 8 names `./artifacts/runs/` as a place a run writes to; Task 9 names it only as the destination of scanned copies.

## Follow-ups (never repaired by a fix pass)

- NEW-2 (Medium): the Task 4 dry-run excerpt (line 113) and the Task 5 self-test output (line 134) sit in `./artifacts/` before Task 9's scan, and Task 9's scan covers only the scratch directory (this is M-13).
- NEW-3 (Note): line 82 says the zero-question line names the flag; New material lines carry a source (`templates/draft-notes.md:7`); wording only.

## Findings block

```findings-v1
{"id": "NEW-1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "each with an output directory under `./artifacts/runs/`", "anchor2": "Raw run output goes to the scratch directory of Task 4", "refs": ["B-4", "R-013"], "claim": "Tasks 6 to 8 tell the run script to write raw output under ./artifacts/runs/ and check it there, while the B-4 lines send raw output to scratch and Task 9 scans only scratch, so raw logs can be staged unscanned."}
{"prior": "B-1", "status": "resolved"}
{"prior": "B-2", "status": "resolved"}
{"prior": "B-3", "status": "resolved"}
{"prior": "B-4", "status": "resolved"}
```
