# Tier-1 reflection card (UC-1, inline orchestrator)

Spec: .dev/tasks/to-do/TASK-WF-spec-20261022-211556/source.md (47 lines)
Tasklist: .dev/tasks/to-do/TASK-WF-spec-20261022-211556/TASK-WF-spec-20261022-211556.md (9 tasks, 4 phases, 10 Constraint bullets)
Coverage matrix: artifacts/coverage-matrix.yaml (Pass 1 parsed 0; Pass 2 inferred 45, all quotes verbatim on their cited line; union coverage 38/45 = 0.8444; S_dev_density 0.1556)
Author note: the orchestrator running this reflect also wrote the plan (opus class). Treat every claim below as possibly self-confirming.

## Coverage section (semantic read of the 7 unmapped rows)

- INF-001 (source.md:3, goal "sync job stops pushing unreviewed upstream content to master"): lexical miss. Task 6 replaces the push (tasklist line 99 onward); Goal line of the tasklist restates it.
- INF-003 (source.md:7, "Evidence files go under ./artifacts/"): lexical miss. Constraint bullet 2 (tasklist line 20) and every task writes ./artifacts/.
- INF-037 (source.md:38, "Every acceptance bullet must fail on a wrong edit"): plan-wide quality property, not a task. Partially met; see claims C2, C4, C5.
- INF-040 (source.md:39, "positive greps showing the expected edits happened"): lexical miss. Task 9 positive-check bullet (tasklist line 158 area) plus per-task greps in Tasks 5, 6, 8.
- INF-041 (source.md:40, "Depends on: lines name one task each; make real chains"): structural. Every Depends on names one task, but the chain is a single line 1 to 9; see C6.
- INF-042 (source.md:40, "No numbered or checkbox lines"): structural; gate grep found none.
- INF-045 (source.md:47, "Do not add a task; raise it to me as a question"): correctly has no task; the question belongs to the session report, not the plan.

## Deviation / plan-logic section (claims)

- C1 (Task 9, tasklist lines 19 and 146-156): the plan defines the scripts/README.md "one paragraph" as lines 7-12 (sentence plus its bullet list) and leaves lines 3, 14, 16-28, 39 and the Upload Failures section unchanged as listed leftovers. The spec says "Change nothing else in that file" (source.md:35). After the edit, line 3 ("handled by the GitHub Actions workflow described below") and the Required Secrets / Release steps sections will contradict the new paragraph. Interpretation is defensible but the result is an internally inconsistent README; it needs a user decision. Severity medium.
- C2 (Task 5, tasklist line 94): the backslash-before-backtick check is written as inline code containing a backtick (`grep -c '\\`'`), which breaks the Markdown code span and is ambiguous to an executor. Severity medium.
- C3 (Task 6, tasklist line 114): the stub run says "`git` push and `gh` replaced by PATH stubs". The step body also runs `git config`, `git add`, `git diff --cached`, `git commit`; a PATH stub named git must delegate every non-push subcommand to the real git or the run fails for the wrong reason. Not specified. Severity medium.
- C4 (Task 5, tasklist lines 88 and 91): header comment check uses fixed `sed -n '19,20p'`; if the reworded comment changes the line count, the check reads the wrong lines and can pass or fail spuriously. Same for "the two lines starting at 3. **PR-review discipline**". Severity low.
- C5 (Tasks 5-9, tasklist lines 87, 112, 125, 144, 156): `<t1-head>` is a placeholder the executor must replace with the content of ./artifacts/t1-head.txt; not stated explicitly. Severity low.
- C6 (tasklist lines 43, 53, 65, 75, 101, 119, 132, 148): a single linear chain makes Task 3 depend on Task 2, Task 4 on Task 3, Task 6 on Task 5 although they are independent. Spec asks for "real chains where order matters" (source.md:40). Real orders: Task 7 needs Task 2; Task 8 needs Tasks 5, 6, 7; Task 9 needs all. One-name-per-line forces some linearisation, but Task 3 to Task 2 and Task 4 to Task 3 are spurious. Severity low.
- C7 (Task 7, tasklist line 117 onward): the spec offers an alternative "delete the step and its README mentions" if the fork does not use Codecov (source.md:30); "Decisions taken as defaults" (source.md:44) fixes the token path, so no alternative branch is needed. Confirmed covered.
- C8 (Fix 1 consequences, source.md:14): stated verbatim in Constraint bullet 9 and repeated into ./artifacts/t6-fix1-notes.md by Task 6. Covered.
- C9 (Task 3): `can_approve_pull_request_reviews` is the field the workflow-permissions API returns for the "Allow GitHub Actions to create and approve pull requests" setting [INFERRED from API knowledge; Task 3 itself records the raw JSON].

## Risk section

- Fix 1 and Fix 3 cannot be proven locally; the plan marks both UNVERIFIED and names user steps (Task 6 notes, Task 7 note). Covered.
- Scope baseline (Task 1) is taken at execution time; this reflect run's output dir (.dev/reflect/) will already exist then, so it is in the baseline and cannot trip Task 9. Covered.
