# Tier-1 reflection card (UC-1, inline orchestrator, refactor cycle 1)

Spec: .dev/tasks/to-do/TASK-WF-specR1-20261023-031725/source.md (82 lines: the original spec plus "## Review Feedback (reflect cycle 1)" at lines 49-82)
Tasklist: .dev/tasks/to-do/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md (9 tasks, 4 phases)
Coverage matrix: artifacts/coverage-matrix.yaml (Pass 1 parsed 0; Pass 2 inferred 69, quotes verbatim; union 59/69 = 0.8551; S_dev_density 0.1449)
Author note: the orchestrator running this reflect also wrote the plan (opus class). The prior cycle's report is .dev/reflect/pre-TASK-WF-spec-20261022-211556-20261022211900/REPORT.md; check that each of its 18 findings is actually fixed, not just reworded.

## Coverage section (semantic read of the 10 unmapped rows)

- INF-001 (source:3, sync goal): lexical miss; Goal line and Task 6.
- INF-003 (source:7, ./artifacts/): lexical miss; Constraints bullet 2.
- INF-023 (source:24, no backslash before a backtick): covered by the fenced grep in Task 5's Render bullet.
- INF-037 (source:38, every bullet fails on a wrong edit): plan-wide property; reviewers must test it task by task.
- INF-040 (source:39, positive greps): Task 9 positive-check bullet.
- INF-042 (source:40, no numbered or checkbox lines): structural; gate grep found none.
- INF-045 (source:47, raise the path-filter question): Task 3 quote plus Task 9 leftovers item; the question itself was raised in the planning session.
- INF-050 (source:57, whole-document comparison): Task 6 "Whole document" bullet and Task 7 second bullet.
- INF-057 (source:69, Task 7 writes its own note): Task 7 body (./artifacts/t7-codecov-note.md) and its third bullet.
- INF-062 (source:76, fenced backslash check): Task 5 fenced command.

## Plan-logic section (claims)

- C1 (Task 9, Constraints "Necessary deviation"): the tooling-output exclusion (`.dev/reflect/`, `.dev/troubleshoot/`, `.dev/workflow/`) departs from source:39 ("only .github/workflows/, scripts/README.md and the plan package folder may differ"). It is disclosed with a reason, as source:70 asked. Check that it cannot hide a real product edit (those roots hold no product files). Severity low.
- C2 (Task 1, Task 9): converting `git status --porcelain -uall -z` to "one path per line" is underspecified for renames, where -z emits two NUL-separated paths. Severity low.
- C3 (Task 5 Warning bullet): the acceptance check requires the literal word `advisory` on the `::warning` line, but the instruction only says "advisory wording". A correct reword without that word fails. Severity low.
- C4 (Task 6, "the file contains no `<` placeholder"): wording is ambiguous; the intended check is that the edited workflow contains no `<` character (base has 0). Severity low.
- C5 (Task 6 stub run (d)): the push runs before `gh pr list`, so a failing `gh` leaves the branch pushed with no pull request but the step red. The spec's intent (fail closed, visible) is met; check the reviewers agree. Severity low.
- C6 (Depends on lines): Task 6 -> Task 3, Task 7 -> Task 2, Task 8 -> Task 7, Task 9 -> Task 8; Task 9 also needs Task 3's artifact and Task 8 needs Tasks 5 and 6, stated in the bodies with the "number order" rule in Constraints. Check this satisfies source:40 and source:82.
- C7 (Prior findings): spot-check that M-01..M-18 of the prior merged verdict are each addressed (M-07 durable record, M-08 fail-closed, M-09 run (b), M-10 whole document, M-06 Decision line, M-05 scope parsing).

## Risk section

- Fix 1 and Fix 3 remain UNVERIFIED until GitHub runs; named as user steps (Task 6 notes, Task 7 note).
- Task 5's render uses real repository history (latest commit touching merge.py and its parent); both exist on base a88f100b.
