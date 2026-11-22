# QA Report - Gate 3 structural verification, cycle 2

**Phase:** report-validation verification (structural), cycle 2
**Date:** 2026-11-20
**Status:** Complete
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md
**Previous BLOCKING list:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/qa/qa-consolidated-findings-c2.md (N-1)
**Fix log:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/qa/qa-fix-cycle2-report.md
**Fix authorization:** false

## Previously BLOCKING findings

| ID | Location | FIXED-OK/STILL-OPEN | Evidence |
|----|----------|---------------------|----------|
| N-1 (place 1) | document L354, 2.4 row 6 | FIXED-OK | Row now reads "every other `orca` verb off the allow-list is blocked, except a short help call (`<verb words> --help` or `-h`, at most four words counting from `orca`, no glob character; `orca list --help` and `orca agent launch -h` pass)"; evidence cell cites `launch-level-guard.sh:487-490` and `tests/hooks/test_launch_level_guard_worker.py:226-230`. Snapshot `launch-level-guard.sh:487-490` read: `*) case ${ws[last]} in --help or -h) { LL_GLOB = 0 and (words - i) <= 4 } or ESCAPE ;; *) ESCAPE`, comment "help only on a short call". Test lines 226-227 (`orca list --help`, `orca agent launch -h`), def at 230, read. Row still has the same pipe count as its neighbours. |
| N-1 (place 2) | document L1258, 5.3 G2 rule 2 paragraph | FIXED-OK | Now "every other orca call is ESCAPE (`GD:480-491`), except a short help call: ... last word `--help` or `-h`, no glob character, at most four words counting from `orca` ... allowed (`GD:487-490`; pinned by `test_the_read_only_orca_forms_stay_allowed_for_a_bound_worker` ... `T/hooks/test_launch_level_guard_worker.py:226-230`)". Matches code and test as read. |
| N-1 (place 3) | document L1448, 8.1 guard-stack row | FIXED-OK | Now "every other `orca` call is ESCAPE, except a short help call (`<verb words> --help` or `-h`, at most four words counting from `orca`, no glob character)"; evidence cell adds `:487-490` and `:226-230`. Consistent with code. |
| N-1 (place 4, repeat found by the fix agent) | document L2241, Appendix A.2 `test_launch_level_guard_worker.py` row | FIXED-OK | Now "orca verbs off the allow-list blocked (a short `--help` or `-h` call stays allowed, `:226-230`)". Test file read: 300 lines, 11 tests (defs at 51, 74, 79, 97, 187, 213, 230, 243, 249, 262, 273), matching the row's "300 / 11". |
| N-1 (any other universal claim) | whole document | FIXED-OK | `grep "every other"`: only L1911 ("every other contradicted or stale row") and L2214 ("every other pair raises TransitionError") remain, both unrelated. Greps of `orca ... blocked/ESCAPE/denied` and of `bound worker/session ... only/cannot/never` show no remaining universal statement beyond the corrected places (L1168, L2186, L2360, L1356 speak about send/ask and `--to` only, which is true). |

## New BLOCKING findings

| ID | Location | Problem | Evidence | carried-over/new | previously-rated-PASS yes/no |
|----|----------|---------|----------|------------------|------------------------------|
| (none) | - | - | - | - | - |

Number of BLOCKING findings: 0.

## Notes (MINOR, not rechecked in later rounds)

- L1258 lists the G2 send/ask ESCAPE argument cases as "a bare word or a lone `--`"; the code comment at `launch-level-guard.sh:532` also names "a short -x option" (same `*) LL_SBAD=1` arm). The sentence is incomplete, not false. Pre-existing text, not touched by cycle 2.
- The fix report cites the test as `:226-230`; the params sit on 226-227 and the def on 230. Acceptable range.

## Structural integrity after the fixes

| Check | Result | Evidence |
|-------|--------|----------|
| 16 template sections present and in order | PASS | `grep '^## '` shows 1 to 16 at L183, 224, 364, 444, 655, 1368, 1397, 1403, 1512, 1579, 1651, 1698, 1747, 1876, 2025, 2148, in order, then Appendix A L2203, Appendix B L2279, Document History L2426 |
| Subsection headers named in the ToC exist | PASS | 5.1.1 to 5.1.9 (L695-970), 14.1.1/14.1.2, 14.2.1, 14.3.1/14.3.2, 15.1 to 15.6, A.1 to A.4, B.1 to B.9 all found by header grep |
| ToC anchors match headers | PASS | e.g. `#8-api--integration-points`, `#10-error-handling--edge-cases`, `#appendix-b-removed-on-2026-11-20`, `#document-history` match GitHub slugs of the headers |
| No placeholder text | PASS | grep for TODO, TBD, FIXME, `[fill`, `{{` returned nothing |
| Tables not broken in edited rows | PASS | awk pipe count on L354, 1448, 2241 equals 6, the same as neighbouring rows (347, 358, 1445, 1449, 2235, 2242) |
| Appendix A row count equals its closing statement | PASS | Counted A.1 = 21, A.2 = 11, A.3 = 9, A.4 = 7 = 48; closing line L2275 says "48 rows (A.1 21, A.2 11, A.3 9, A.4 7)" |
| PR 686 / rewrite-design out-of-scope sentence exactly once | PASS | `grep 686` minus the line ranges 685-686, 654-686, 669-686, 673-686 leaves only L218 ("PR 686 and the rewrite design are out of scope for this reference."); "rewrite design" appears nowhere else; PR numbers elsewhere are #682 (removal commit) |
| Internal cross-references from the edited text | PASS | "Section 5.3" (L1157) and "Section 14 D-25" (L1976 row) exist; "D-18" exists at L1969 |

## Citations re-verified against the snapshot (20)

1. `launch-level-guard.sh:457` `orca)` case arm - matches.
2. `:480-484` allow-list words (status, help, --version, worktree current/list/show, terminal list/show/read, orchestration check/inbox/run-current/task-list/worker-show) - matches L1258 and L1448 lists.
3. `:484` glob turns read verbs into ESCAPE - matches.
4. `:485` `LL_SA=1` for orchestration send/ask - matches.
5. `:486` `'- -'` ESCAPE - consistent.
6. `:487-490` short help branch - matches the new text (last word `--help` or `-h`, glob 0, at most four words from `orca`).
7. `:442-443` `LL_GLOB` set once per command from `* ? [ {` - consistent with "no glob character".
8. `:496-537` G2 rule 2 block - starts at the comment L496, ends `fi` L537.
9. `:507, 511` 8192 bytes and 64 arguments - matches L1258 and L1448.
10. `:524, 527, 532` `--to`, `--run`, `--environment`, `--pairing-code`, prefix of `--to`/`--run`, bare word or lone `--` - matches (with the minor -x omission).
11. `tests/hooks/test_launch_level_guard_worker.py:74` - `test_a_bound_worker_may_send_and_ask_its_coordinator`.
12. `:187` - `test_a_bound_worker_cannot_address_another_worker_or_a_group`.
13. `:213` - `test_every_other_orca_word_stays_blocked_for_a_bound_worker`; its params include `orca * --help` and `orca agent launch --name w --help` (blocked), consistent with the glob and four-word limits.
14. `:226-230` - allowed forms `orca list --help`, `orca agent launch -h`; def `test_the_read_only_orca_forms_stay_allowed_for_a_bound_worker` at 230.
15. `:262` - `test_a_forged_release_from_the_workers_own_session_is_blocked_as_tampering`.
16. `:287` - the `pending` subprocess call (test caller of `orca_worktree.py pending`).
17. `src/superclaude/core/WORKER-CONTRACT.md:66` - "Messages carry no `--to`" bullet.
18. `tests/skills/test_worker_contract.py:423-431` - `messages-carry-no-to` pin; file is 3220 lines as the doc states (L2259).
19. `launch-level-guard.sh` is 808 lines (doc L213, L1165) - matches `wc -l`.
20. `launch-level-guard.sh:449, 457` basename `b=${w##*/}` then `orca)` - supports the "command word `orca` only, not `orca-ide`" statement in the edited row 6.

## Checks performed

- Read the Step 6.11 prompt block, the consolidated c2 findings and the cycle 2 fix log.
- Read the document header, ToC, 2.3, 2.4, 5.3 (whole), 7, 8.1, 15.1/15.2, Appendix A (whole), the end of Appendix B and Document History.
- Grep of the document for "every other", "686", placeholders, header levels and G2 rule 2 mentions; awk column counts on edited rows.
- Read the snapshot guard script (lines 440-540) and the worker test file; nothing under the snapshot was written; nothing was written outside this report.
- Confidence: Verified 8 structural checks plus 5 N-1 rows plus 20 citations; Unverifiable 0; Unchecked 0. Tool engagement: Read 10 | Grep 9 | Glob 0 | Bash 3.

## Verdict: PASS

Status: Complete
