# Tier 1 reflection card (UC-1, pre-execution)

Source: inline orchestrator card (hypothesis_source: inline-orchestrator; UC-1 has no mapped Wave 1C agent).
Spec: .dev/tasks/to-do/TASK-WF-detachTheCcsessi-20261102-034618/source.md (delegates to .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md)
Tasklist: .dev/tasks/to-do/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md

## Coverage (deterministic matcher, artifacts/coverage-matrix.tsv)

Pass 1 parsed IDs: 0 (`coverage_pct: null`). Pass 2 inferred rows: 44 (INF-001..044, artifacts/inferred-rows.tsv). Containment matching against the five `## Task` bodies: 31/44 matched, `coverage_pct_union: 0.7045`. `coverage_degraded: parsed-sparse` (44 inferred > 0 parsed).

The 13 unmatched rows, checked by reading the tasklist (not by the matcher, which only compares against Task bodies):

| id | requirement | where the tasklist actually covers it | verdict |
|---|---|---|---|
| INF-006 | "scope: exactly these, nothing else" (R:9) | Constraints bullet 1 (tasklist line 19) | covered by Constraints |
| INF-022 | reply 200 + `message_stop`, health still same pid (R:14) | Task 1 Acceptance criteria bullet 1 (tasklist line 32) | covered (matcher ratio 0.55, wording differs) |
| INF-026 | both tests fail before and pass after (R:16) | Task 1 AC bullet 2, Task 2 AC bullet 1 (fail before); Task 3 AC bullet 1 and Task 4 AC bullet 1 (pass after) | covered across tasks |
| INF-028 | AC1 same as INF-026 (R:21) | as INF-026 | covered across tasks |
| INF-029 | AC2 named test files + related test files pass (R:22) | Task 3 AC bullet 2; Task 5 AC bullet 2 | covered |
| INF-030 | never the full suite or tests/cli/eval/ (R:22) | Constraints bullet 4 (tasklist line 22) | covered by Constraints |
| INF-035 | nothing under ~/.claude, ~/.ccsession, running config edited (R:25) | Constraints bullet 2 (tasklist line 20) | covered by Constraints |
| INF-038 | script path stays in argv (R:26) | Constraints bullet 3 (tasklist line 21); Task 3 body "argv and env unchanged" | covered |
| INF-039 | env inherited (R:26) | Constraints bullet 3; Task 3 body | covered |
| INF-040 | no setsid binary (R:26) | Constraints bullet 3 | covered by Constraints |
| INF-041 | logging stays opt-in (R:26) | Constraints bullet 3 | covered by Constraints |
| INF-043 | HC1: replay through real ccsession launch + descendant kill, positive witness from AC1/AC3 (R:35) | Task 1 body (real ccsession, descendant SIGTERM/SIGKILL); Task 4 AC live check | covered |
| INF-044 | HC5: off-path review required (PR reviewers and /sc:reflect --mode post) (R:35) | not in the tasklist | GAP (process step after /sc:implement; not a code task) |

Effective coverage after reading Constraints: 43/44; one gap (INF-044).

## Deviations from the spec (UC-1 categories)

| item | category | rationale |
|---|---|---|
| Task 5 carries the AC2/AC4 checks (related tests, `make lint`, `make verify-sync`) inside the CHANGELOG task | Refinement | remediation-source lists them as plan-level ACs; the workflow template forbids verification-only tasks, so they ride on the last task |
| Task 4 carries the AC3 live check and the live-shim pid check | Refinement | same reason; live check needs the Task 4 change |
| Task 2 asserts both `getsid` and `getpgid` differ | Aligned | matches R:15 exactly |
| Order: tests first (Tasks 1-2), then fixes (Tasks 3-4) | Aligned | matches AC1 "fail before, pass after" |

## Risks

- Task 3 AC expects `test_shim_outlives_the_terminal_that_started_it` to keep failing until Task 4: correct only if `os.setsid()` alone does not take the shim out of the terminal's descendant tree. It does not (parent pid is unchanged), so the expectation holds; an executor could misread a Task 3 failure as a defect.
- Task 1 relies on tier mode to route `claude-gw-tier2` to `muse-spark-1.3`; the task says "Mirror `_real_launch`", which sets `AIDEV_AI_DEFAULTS_PATH` (test_ccsession_tiers.py:1360). If the executor drops that env var the stream never reaches the paused model.
- Detached shims outlive every test: the test's cleanup must kill by pid AND `pkill -f` the per-test copy path, as Task 1 states; a leak would leave a process on a random port.
- HC5 (independent review) is not in the plan; if nobody runs `/sc:reflect --mode post` or the PR review, the hardening closure stays advisory.

## Recommendations

- Add HC5 to the post-implementation steps outside this plan: run `/sc:reflect --mode post --spec <REPORT.md> --tasklist <pkg>/<id>.md --diff <baseline_ref>` and open the PR through `/sc:pr-submit` (owner: whoever runs /sc:implement). Verifier: a reflect-post report path and a PR URL.
- Executor note for Task 3: expect the Task 1 test to fail until Task 4 (already stated in Task 3 AC bullet 2).
