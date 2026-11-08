
# Reflect report: POST (UC-2) audit of the issue-watch poller (issue 331)

- **Work audited:** commit `26f551f41edece1f05c07a3c02d78325e365f6d1` on top of BASE `e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b` (one commit, 379 files, all additions): the `superclaude issue-watch` package, its registration in `main.py`, the `tests/issue_watch` suite, the owner runbook, and the task package under `.dev/tasks`.
- **Driving documents:** `docs/designs/issue-watcher.md`, the executed task file `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md` (Open Questions OQ-1..OQ-51 and the decision register DF-01..DF-60 are the authorizing artifacts).
- **Run id:** `reflect-post-20261108T0410Z-issuewatch331` (tier 2, depth deep, `--remediate`).

## Verdict

**FAIL, status needs_human_decision.** One Regression of severity LOW is blocking (R-1). Six more Regression-class rows are non-blocking (four are document amendments, one is test hygiene, one is effectively unreachable). The work is otherwise in good order: the verdict becomes PASS-with-deviations once R-1 is fixed and its test lands.

| Item | Result |
|---|---|
| Blocking | R-1: a launch can start after the 120 s cutoff if the durable pending save crosses it (design line 647, AC-19). Compatible fix and verifier are in the register and in Recommendation R-001. |
| Non-blocking Regression-class rows | R-2 (exit 1 `cycle_crashed`), R-3 (59 reason names against 57/52), R-4 (`valid_operation_id` import), R-5 (five skip sites), R-6 (500-byte stderr cap vs operation-unknown marker), R-7 (retry list edge, effectively unreachable) |
| Drift | D-1 runbook/design exit and platform facts, D-2 `cli` -> `cycle.format_utc`, D-3 duplicated login regex and UTC format in `cycle`, D-4 wall-clock read in `stderr_fallback` |
| Necessary | N-1 local copies forced by the import rules, N-2 day-cap test reading, N-3 `launch._ORCA_CLIS` access |
| Authorized | A-1..A-5 (task Step 4.1a imports, runner duration clock, five proposed reasons, CI-only full suite, eager registration) |
| Advisory gaps (never gate) | 17 rows, see below |
| Grounding gaps | 16 rows (6 runtime-surface DEGRADE, one per Click symbol; 6 judge evidence gaps; 4 reuse maybe-related), so `needs_human_decision: true` |

## What was verified independently

- The orchestrator ran the suite: `pytest tests/issue_watch` gave 2635 passed, 0 failed, 0 errors, 0 skipped on Python 3.11.15; `ruff check` and `ruff format --check` were clean (`verify-logs/invocations.yaml`).
- Coverage matrix (Wave 1B helper, then re-checked by the reviewers): 68 rows (29 FR, 14 NFR, 25 AC): 63 covered, 3 partial (NFR-008, AC-19, NFR-014), 2 gate-only (NFR-012, AC-23), 0 gaps. Tasklist: 207 of 209 items checked; the two open items are Step 10.6 (this run) and Step 10.7 (Done).
- Safety properties held under a three-reviewer audit and a fault-finder probe (12 findings, 0 HIGH unaddressed): durable pending record before the spawn, integer-only prompt, no GitHub write, no shell, fail-closed reads, kill switch, day cap. At-most-once holds within one store; two stores on one login break it, which the design already names as residual risk R12.
- Required-capability reachability (SKILL step 5.6a): 5 of 5 capabilities reachable, none unreachable or unproven. The spec has no `durable_sink:` annotation, so the durable-sink gate (step 5.6) is advisory only.
- Executor claims that did not hold: 6 fixture files were added after the Step 10.1 text says 13 (19 on disk); the reason table has 59 names while the task body still says 57; Python 3.10 and markdownlint were found although the task text says they do not exist locally. All are disclosed or minor.

## Run integrity notes

- Reviewer independence: three fresh read-only `reflect-reviewer` agents on different model classes (sonnet, haiku, opus); the executor's model class could not be resolved (`executor_class_resolved: false`), so the executor-vs-reviewer partition is unverified.
- Calibrator diversity is degraded: all three Anthropic classes are reviewers, so the highest-capability class (opus) calibrated; vendor diversity is single.
- The adversarial judge is the same class as one reviewer and one advocate (`judge_class_collision: true`).
- Two reviewer cards carried wrong line numbers (`cycle.py:335-337`, `cycle.py:308`, and `src/superclaude/main.py`); the blind calibration and the merge corrected them and the evidence-validator re-read every citation below.
- The neighbour (reuse) search ran without auggie, so every reuse finding is capped at advisory.
- The `/sc:impact` call returned `graph:stale` and `graph:unresolved` and mapped 30 of about 400 new symbols (protocol cap).

