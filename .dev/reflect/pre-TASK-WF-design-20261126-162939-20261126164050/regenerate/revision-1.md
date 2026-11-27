

## Revision 1: review findings the plan must fix (added by the plan repair step; the design above is unchanged)

The first plan generated from this design (package TASK-WF-design-20261126-162939, now archived) was reviewed by `/sc:reflect --mode pre` (report `.dev/reflect/pre-TASK-WF-design-20261126-162939-20261126164050/REPORT.md`). It had 11 blocking findings. The new plan must not repeat them. Where a repair departs from a decision or a requirement above, the plan records an explicit override instead of silently following the design.

### Blocking findings to fix

- M-01: the plan Constraint that said "No code or text uses `--no-verify`, `-n` on commit, `SKIP=`, `commit-tree` or `--amend`" contradicted the tasks that must write those tokens into the deny-list and its tests. Reword it to ban running or recommending them and allow deny-lists, refusal text and tests of refusals.
- M-02: the `/sc:git` command task edited fixture S23 and ran the routing test before the skill file existed (the test also fails while S23 stays `self-contained` and the command has an Activation section). Move both the S23 edit and the routing-test run into the task that creates the skill file.
- M-03: the repo-wide "only file that runs a branch deletion" check cannot pass (existing cleanup tests run branch deletions, in list-form argv). Scope the check to the files this work adds (requirement FR-081 says "No new code").
- M-04: a plain file delete does not change `git ls-files` output. The retirement check for `commands/sc-git.md` uses `test ! -e` and a work-tree count.
- M-05: plugin copies of the implement files were left to the last task, but existing byte-parity tests run earlier. Each task that changes an implement file copies and compares its own plugin twin; the last task only verifies.
- M-06: new `E-RESUME-NEEDED` reasons conflict with an existing test pin of four transient reasons (`_TRANSIENT`). List the two new reasons in `refs/commit-step.md` only, which that test does not scan.
- M-07: new halt, Ruling or `E-ARCHIVE-BLOCKED` lines in scanned implement files match no entry of the allow-list in `tests/skills/test_implement_severity_static.py`. Keep new wording in `refs/commit-step.md`; for the archive-gate refusal that must sit in `refs/managed-workspace.md` step 1, add the allow-list entry in the same task and record the override of requirement T-16 / NFR-005.
- M-08: the ledger reader must copy nine line patterns (`_HEADER` and `_ARCH` as well as the seven the design lists), so a header-only ledger and a ledger ending in `ARCHIVE: failed` are not refused. Record the override of DD-8.
- M-09: the `skipped` settlement (empty boundary, mixed-authorization boundary) needs a `record-skipped` action in the derive-state table, a case in the reconcile tests, and a procedure step.
- M-10: the executor-side cases of tests T-04 (refused line, no same-run retry) and T-21 (crash after the resolution append, two resumes, surviving pins, no-key reply, redisplay when disclosure changes) must be in the acceptance of the helper tasks and pinned statically in the ref text.
- M-11: the staging path rules must exclude paths under `.dev/implement/` (not gitignored), with a case in the path-mode and ledger-mode tests.

### Findings the new plan must not repeat (Medium, fixed where cheap)

- M-12: no task realized the stop-rather-than-wait rule for credential or authentication prompts, and the runner did not drop inherited `GIT_*` variables or set `GIT_TERMINAL_PROMPT=0`.
- M-13: the managed archive gate called `vcs reconcile` even when no `commits.md` exists (requirement NFR-018).
- M-14: `add -A` is forbidden for printed argv but required by the private-index snapshot method; say when it is allowed.
- M-15: the "`--commit-tasks` appears only in primitives" scan must not cover docs and plan packages.
- M-16: the 15-line net growth budget for the implement skill file was shared by two tasks and measured with insertions plus deletions.
- M-17: the staging-checks task listed seven refusal tokens, said "five" and tested two.
- M-18: "unchanged against `origin/integration`" checks drift; compare to a recorded merge-base commit.
- M-19: person-only commit authority had no static assertion.
- M-20: the design's test-first order inside each phase was not carried into the plan.
- M-21: `refs/retry.md` also deletes the Q0 pin at `complete`; amend it with the ledger and skill sentences.
- M-22: the helper allow-list had no `version` form although preflight reports the git version.
- M-23: the edited `SKILL.md` Q0 sentence already has a worker-contract classification row; keep its category and re-key it.
- M-24: the final gate must allow recorded baseline failures and skipped real-framework hook tests.
- M-25: open item O1 (DD-11 reading) awaits the owner; keep the reading the design chose and say so.
