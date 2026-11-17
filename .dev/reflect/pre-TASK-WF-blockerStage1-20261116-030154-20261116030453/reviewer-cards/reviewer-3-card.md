persona: refactorer
model_class: opus
model: opus (requested alias pin; the resolved model id is not visible to the orchestrator)
model_observed: claude-gw-tier1a (Claude, opus-class) (reviewer self-report)

## Verdict
NEEDS-REVISION. Two acceptance checks cannot pass as written: the stoprule family has no file in the repository, and a later task in this package makes Task 7's grep false.

## Findings
F1 | MAJOR | blocking true | unpassable-check | Task 3 needs every one of the 12 scale-map rows to name a file in the repository, and T4 needs each row's file to exist, without reading `~/.claude`. The stoprule rubric and `finding-grader` exist only in installed copies; neither is under src/ or plugins/. OD10 is undecided, so an executor cannot bring them into the repo. | cites: .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:62-62 "each naming a defining file that exists in the repository" ; .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:209-209 "T4 (each scale-map row names an existing file and a label present in it)" ; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:145-145 "`~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md`, installed only" ; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:880-880 "today installed only [V]"

F2 | MAJOR | blocking true | contradiction | Task 7's grep line has no "until Task N" end point. Task 10 tells the executor to import Task 7's reader into `classifier_inputs.py`, which is not "command wiring", so the grep line is false by the final review. Matches in `__pycache__/*.pyc` also show up in the grep. The plan's own rule and the spec require an end point here. | cites: .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:115-115 "shows only the new module and its command wiring" ; .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:148-148 "Reuse the reader of Task 7 for ledger rows" ; .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:24 "carries its end point (\"until Task N\")" ; .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:17-17 "get an end point (\"until Task N\")"

F3 | MINOR | blocking false | other | The T2 reverse scan covers every file under `src/`. Task 14 has to parse digest fences from installed carriers, so `doctor.py` may contain the fence-opener text and has no registry row. The plan does not say whether code files are exempt. | cites: .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:209-209 "holds the old definition sentence or a fence opener and has no registry row" ; .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:197-197 "compares the digest versions held by the installed carriers"

F4 | MINOR | blocking false | other | The plan does not say where the "agrees with the sketch" check lives. A committed test that imports the sketch from `.dev/tasks/to-do/...` breaks when the program folder is archived, and ruff excludes `.dev/`. | cites: .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:139-139 "`verdict` agrees with the sketch on all 6,400 combinations" ; pyproject.toml:179-180 "extend-exclude = ["

## Checked
- The old definition sentence appears in exactly 11 files under src/ and none under plugins/. This matches the 11 digest rows in Task 6.
- None of the 11 carriers contains `src/superclaude`, so the T3 check passes at legacy.
- pragmatic.md:227 holds the cap sentence word for word.
- card_convert.py:82 maps `important` and `medium` to non-blocking; rf-qa.md:111 treats IMPORTANT as blocking.
- auggie SKILL.md:228 holds the expected text.
- origin_repo.py exists. The sketch gives 4*5*5*4*4*4 = 6,400 cases.
- pyproject has pyyaml as a dependency and the wheel packages src/.
- `_has_corresponding_command("sc-review-severity")` returns False, because no commands/review-severity.md exists.
- test_review_cli.py:44-48 is not affected by a new `classify` subcommand. lint_cmd.py and estimate_cmd.py are absent, but their import is optional.
- The banned-phrase scans in test_review_severity_rule.py found no hits in the spec text that Task 2 copies.
- The earlier review's findings F3, F4, F5, F9, F12, F13 and F15 are resolved in Tasks 2, 3, 5, 6 and 15. F6 is only partly resolved (see F2).

## Self-report
confidence: 0.82
reviewer_model_self_report: claude-gw-tier1a (Claude, opus-class)

I did not check whether the "7 lines" claim about the tasklist skill still holds, or Task 1's stage-ledger check. I did not run any test.

## Calibration (blind, opus-class; written by the orchestrator from the calibrator's report)
calibrated_C: 0.76
calibration:
  per_finding:
    F1: 0.72
    F2: 0.75
    F3: 0.55
    F4: 0.50
