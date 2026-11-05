# Round 1 advocate: Variant A (analyzer card, A-1..A-11)

## Steelman
Card C found the biggest miss on any card: Task 19 has no path to Task 13 (U-001, S:1428). It also gave the only full chain for the shared test file (F-4). Card B found the staging gap's effect (the `.claude/` check at P:307 is vacuous) and the fixed-identity breakage. My card missed CF-17 and CF-22, so I concede coverage to C.

## Severity rule (answers X-005)
Medium when an AC or test executes an artifact outside the task's closure (CF-01, 02, 17, 22). Low when only prose or ordering is affected (CF-03, 04). A's ratings follow this rule.

## Shared assumptions
- **A-001 ACCEPT.** Spec step 3 is Tasks 3+4, but Task 10 depends on Task 3 only (P:184). Task 11 (F10, F12) and Task 18 (S:1345) use Task 4 functions. One edge, Task 10 "Depends on: Task 3, Task 4", closes CF-22 and CF-02. My A-2 caught only the Task 15 instance.
- **A-002 ACCEPT.** My A-2 matched names in task text. Nobody mapped S12 test-case IDs to functions, which is how CF-22 slipped through.
- **A-006 QUALIFY.** The spec column is adequate for text-only references. S:1425 gives the rationale "command lines must match the scripts", which supports a Task 13 edge for refs. It does not support a Task 6 edge on its own.

## Diff points
| Point | Preferred card | Reason |
|---|---|---|
| C-001 (CF-01) | C | Chain 11->12->13. Zero cost, since Task 14 depends on all three. A-1's "optional" was too soft. |
| C-002 (CF-03) | C edges, A severity | Add Task 6 and Task 13 (S:1070 names both). Low: no AC executes them. Adopt B's header-match grep. |
| C-003 (CF-04) | A/B | Low. List 6 and 9 explicitly. C's "9 suffices" is also valid. |
| C-004, C-005 (CF-05, 06) | A fix, C severity | Spec step 3 holds the resume functions; step 7 holds the resume tests (S:1418, 1422). Move the tests to Task 8. This shrinks Task 4 with no new task. C's 4a/4b also works. |
| C-006 (CF-08) | A | Medium. S:1429 and the project rule say stage `.dev/tasks/`; P:27 states the rule but no task does it. Add B's vacuity note. |
| C-007 (CF-11, 12) | A severity, B detail | Low. P:29 cites the "source section 12 preamble" and P:19 says the source wins, so this is ambiguity, not a lost requirement. |
| C-009 (CF-15) | A severity, B/C fix | Task 9 edits only `__init__.py`, and every `tests/pr_submit` test imports it, so import breakage is covered. Still add `test_contract_status_cli.py` to Task 20, since it costs one path. Low. |
| S-002 | A | No High is justified; see the severity rule. |
| U-002 (CF-09) | A | `git ls-files -s` prints nothing for an untracked file, so the AC cannot pass. Use `test -x`. Medium. |
| U-003 (CF-18) | C | Add `test_static_grep.py` to Tasks 11 and 12. Low: Task 14 runs it later. |
| U-004 (CF-20) | C | Missing anchor in Task 17. Low. |
| U-005 (CF-19) | C | `poll-ci-checks.sh:30` exits 2 without `--pr`. Low. |
| U-001 (CF-17) | C | Medium. Add Task 13 (spec-required); add Task 6 and Task 14 because X1 replays ref step 11. |
| A-001 (CF-22) | C (calibrator) | Medium per consumer. Highest fix priority: one edge closes three consumers. |
| X-001 | A | Drift, low. P:93 states the move, but the spec fixes step 7 and nothing forces it; P:19 says the source wins. Task 8 recovery tests mitigate dict drift. |
| X-002 | A on imports, B/C on CLI | Both partly right (see C-009). |
| X-003 | Neither | The spec itself splits E5 and E12 (S:1416, 1426), so "necessary" is wrong. The defect is the missing anchor: drift, low. |
| X-004 | Reject F-10 | Task 5->4 and Task 8->4 are spec-required (step 3 = Tasks 3+4). Only Task 9->6 is stricter. |
| X-005 | A | Consistent under the severity rule. |

## Concessions
- **A-10b withdrawn.** Tasks 8, 17, 18 mirror spec steps 7, 11, 12.
- **A-7 advisory.** The per-task QA reviewer checks phrases, and Tasks 14-16 run `test_static_grep.py`.
- **A-8d reclassified.** `:86-99` is inherited from S:731, and the list ends at `:103` on disk. It is a spec defect, not plan drift.

## Canonical findings (final)
| CF | Sev | Class | Fix |
|---|---|---|---|
| 01 | M | drift | Task 13 on Task 12; Task 12 on Task 11 (minimum Task 10) |
| 02 | M | drift | Task 15 on Task 4, Task 12 |
| 03 | L | drift | Task 16 on Task 2, 6, 13; header-match grep |
| 04 | L | drift | Task 20 on Task 6, 9, 18, 19 |
| 05 | L | drift | Resume tests move to Task 8 |
| 06 | L | drift | Resolved by CF-05; split only if QA objects |
| 07 | n/a | withdrawn | None |
| 08 | M | drift | Staging step in Task 20; AC on `git diff --cached --name-only` |
| 09 | M | drift | `test -x`, or stage first |
| 10 | L | advisory | Optional greps |
| 11 | L | drift | Capability skip in Task 19 |
| 12 | L | drift | Fixed author/committer in P:29 |
| 13 | L | drift | Quote the clause in Task 2 |
| 14 | L | spec defect | Cite `86-103` |
| 15 | L | authorized | Reflect test in Task 20; reword P:19 |
| 16 | L | authorized | None |
| 17 | M | drift | Task 19 on Task 13, 6, 14 |
| 18 | L | drift | `test_static_grep.py` in Tasks 11, 12 |
| 19 | L | drift | C1-C4 run without `--pr`; check stderr |
| 20 | L | drift | Anchors in Task 17 |
| 21 | L | no finding | None |
| 22 | M | drift | Task 10 on Task 3, Task 4 |
