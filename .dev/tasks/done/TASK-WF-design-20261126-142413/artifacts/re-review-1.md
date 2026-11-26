review: 2 of 3

# Re-review of the repaired plan (workflow Wave 4R, surgical route, fix cycle 1)

Reviewer: `reflect-reviewer` agent (opus), read-only, started by the coordinator. Candidate: `.dev/tasks/to-do/TASK-WF-design-20261126-142413/TASK-WF-design-20261126-142413.md` as it was when the review ran (sha256 f768265117083454d96e07619ca7544b19308f6299d2fed3d8c32bdcc185a401). Baseline: the archived original plan `.dev/tasks/archive/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md` (sha256 eb72c524a239d0484dce61cb4094c0e58560e4c718c2bd140171127342da0555). Prior report: `.dev/reflect/pre-TASK-WF-design-20261126-131233-20261126131756/REPORT.md` (sha256 cb81d5243f6d048a9f12e737b8985df8fa0621653fc0927a09827b9864d1dccc).

Provenance note: the reviewer's first message was cut off by the message size inside its Step 1 evidence block. The BEFORE and AFTER lines of that block are the hunks of `diff -w` between the baseline and the candidate; they are kept in full in `./artifacts/plan.diff`. The reviewer re-sent everything after Step 1, which is recorded below as received. Its summary line said: all three prior blocking findings (M1, M2, M3) are resolved, there is no new blocking finding, and two Medium findings and two Notes are listed as follow-up candidates. Diff hunks it covered: `6c6`, `23,24c23,24`, `32c32`, `35c35`, `49c49`, `62,63d61`, `149c147`, `156c154,155`.

## Part after Step 1, as received

(1) Prior blocking findings
- M1 resolved. The Task 2 bullet is deleted. Task 2 now requires the five functions to take no arguments (candidate:49). The nine-case check that edits the text only in memory now runs in Task 7, after the line-624 edit (candidate:155). I checked its expected results against the live files: each site holds `--depth standard` exactly once, on a line with `sc:workflow` (remediation-handoff.md:72, SKILL.md:374, SKILL.md:624). SKILL.md:363 lies outside the skill region, so only the row-to-deep case fails the review-only test.
- M2 resolved. Task 1 records the ruff baseline (candidate:32, :35). Formatting is now done per edited file, and `make format` is gated (candidate:24). Task 7's format check is now compared with that baseline (candidate:154). It and the `git status --short` list (candidate:157) can now pass together.
- M3 resolved. The Constraints state the rule (candidate:23), matching source.md:106. Task 7 writes the named line into t7-checks.md (candidate:147).

(2) New findings: none is blocking.

(3) Follow-up candidates
- F1 Medium: candidate:24 still says edited Python "must pass" `ruff format --check src/ tests/`. Read as "exits 0", that can never be met here, while Task 7 accepts the files Task 1 listed. The text allows two readings.
- F2 Medium: the gate checks only src/ and tests/. `make format` runs `ruff format .` (Makefile:55), which skips only docs/ and .dev/ (pyproject.toml:177-180). So a clean Task 1 plus an unformatted file in scripts/ would fail candidate:157. This cannot happen here. Whether such files exist is UNVERIFIED.
- F3 Note: no acceptance criterion checks the named line, and the plan says the script is run but never says to write it.
- F4 Note: removing the Task 2 bullet also removed the blank line before `## Task 3:`. Formatting only.

(4) Self-check: the quotes from the revised plan are at candidate:23, :24, :49, :147, :154 and :155. The quotes from the old plan are at baseline:24, :62 and :156. The old plan has neither "blocked" nor "take no arguments", so the two plans were not swapped.

(5) Covered: every hunk of the diff, both plans, the spec including Revision 1, and M1-M3. Also the consistency points named in the brief: the `git status` list, the deselect rule (the mutation script is not a pytest run), the script's location and expected results, and Task 1 against Task 7. Against the spec: the step 7 rule matches, and the step 5 departure is disclosed.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "New or edited Python must pass `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/`", "refs": ["Constraints", "Task 7", "source.md section 5 step 5"], "claim": "Read as an exit-0 requirement, the inherited Constraint can never be met in this worktree, while Task 7 accepts the baseline-listed files, so a reviewer could flag a constraint breach on a correct run."}
{"id": "F2", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "run `make format` only if Task 1's format check exited 0", "refs": ["Constraints", "Task 1", "Task 7", "source.md section 5 step 5"], "claim": "The gate checks only src/ and tests/ but make format rewrites everything except docs/ and .dev/, so with a clean Task 1 an unformatted file in scripts/ or plugins/ would be rewritten and Task 7's git status check would fail."}
{"id": "F3", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Also write the named line", "refs": ["Task 7", "R-07", "source.md section 5 step 7"], "claim": "No Task 7 acceptance criterion checks that t7-checks.md carries the blocked line, and the mutation script is described as run but never as written."}
{"id": "F4", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "## Task 3: Add the verdict case for the retired result attribute", "refs": ["Task 2", "Task 3"], "claim": "Deleting the Task 2 bullet also removed the blank line before the Task 3 heading, which is formatting only."}
{"prior": "M1", "status": "resolved"}
{"prior": "M2", "status": "resolved"}
{"prior": "M3", "status": "resolved"}
```

PASS

## What the coordinator did with the follow-up candidates (not part of the review)

The story that started this run says to fix every gap the advisory check names before implementing, so after the single `mark` call the coordinator edited the placed plan once more, in place, on top of the reviewed text. The repair tool does not allow this inside the loop; it is recorded here so the reviewed text and the final text are not confused. The changes, each small and each a Medium or Note finding that the loop leaves alone by rule:
- M4 (first review, Medium): the deselect sentence in the Constraints is scoped to "From the Task 7 `SKILL.md` edit until the commit, every pytest run this plan orders ..."; the Task 1 baseline and the complete run after the commit include the guard test.
- M5 (first review, Note): Task 7 now reads `Depends on: Task 2, Task 6`.
- T1-F1 (first review, Medium): every task now carries a `Requirement: R-0N` line (Task 1: R-07; Task 2: R-05; Task 3: R-06; Task 4: R-03; Task 5: R-04; Task 6: R-02; Task 7: R-01 and R-07).
- F1 (re-review, Medium): the Constraints line now says `uv run ruff format --check src/ tests/` "must list no file that Task 1 did not list" instead of "must pass".
- F2 (re-review, Medium): Task 1 also records `uv run ruff format --check .` (the scope `make format` has), and `make format` is allowed only if that exited 0.
- F3 (re-review, Note): the mutation bullet says the script is written by Task 7, and a new Task 7 acceptance bullet checks the named line in `t7-checks.md` and the existence of the script and its log.
- F4 (re-review, Note): the blank line before the Task 3 heading is restored.
- M6 (first review, Medium): a gap in the reflect run's own coverage matrix, not in the plan; recorded in `.dev/reflect/pre-TASK-WF-design-20261126-131233-20261126131756/artifacts/coverage-matrix-addendum.md`. No plan change.
