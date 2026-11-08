# Gate 3 Consolidated Findings: Phase 6, cycle 1

**Report:** `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/RESEARCH-REPORT-pre-push-guard.md` (about 1469 lines after the cycle 0 fix)
**Cycle:** 1 (second Gate 3 review; this is the last fix cycle allowed before escalation)
**Date:** 2026-11-08
**Inputs (repeat cycle):**
- `qa/qa-fix-verification-cycle0.md` (rf-qa, FAIL). All 20 cycle 0 blocking findings are confirmed fixed. It raises new IMPORTANT issues N-A and N-B, and MINOR notes M-1 to M-5.
- `qa/qa-fix-verification-qualitative-cycle0.md` (rf-qa-qualitative, FAIL). All 20 cycle 0 blocking findings pass. It raises new IMPORTANT issues NEW-1 and NEW-2, and MINOR notes m-1 to m-6.

**Rules applied:**
- Each finding appears once. Duplicates are merged and list every source.
- No severity was lowered.
- MINOR findings are notes and do not block.
- The cycle 0 findings #1-#20 are closed; they appear here only as context.

## Blocking findings (CRITICAL and IMPORTANT)

| # | Severity | Source lens | Affected section | Finding | Proposed fix |
|---|---|---|---|---|---|
| 1 | IMPORTANT | rf-qa N-A; qualitative NEW-2 | §8 steps 1.2, 2.1, 2.5, 4.1, 4.2; SC-18, SC-24, SC-31; §7 bypass table (lines 1042-1058); 5.1 token rationale | The cycle 0 fix for #1 added `<hooks-dir>/pre-push.uv-dir` as a new trust input. The hook puts the directory named in that file **first** on PATH before it calls `identify`. The file is mode 0644. No step checks its owner, mode or content, or the named directory and its `uv`. Step 2.5 checks only `pre-push`. Step 4.2 returns `("present-owned", None)` without checking it. Step 2.1 reports only a stale file. A same-user writer can therefore point the file at a fake `uv` that answers `ordinary`. The tampering survives every pre-launch recheck (4.1). Also, 4.2 lists `uv-dir-missing` in its closed set, but no step makes `l2_status` check the file, so SC-24 has no implementing step. | Extend 2.5 and 4.2, and SC-18, SC-24 and SC-31, to check `pre-push.uv-dir` on every launch: <ul><li>a regular file opened with `O_NOFOLLOW`</li><li>owned by the current user</li><li>not group- or other-writable</li><li>content equal to the value recorded at install</li><li>the named directory and its `uv` owned by the user or root and not group- or other-writable</li></ul>Map each failure to `uv-dir-missing` or `not-owned`. Add the file to the §7 bypass table and the 5.1 token rationale. Alternatively, state it in §7 and §9 as an accepted limit with the reason, and make SC-24 match. |
| 2 | IMPORTANT | rf-qa N-B; qualitative NEW-1 | §4.1 G-44 (line 698) vs the severity rule (line 649), L1-5 (line 728), the §7 wrapper row (line 1046), §8.9 | G-44 is rated Important. Its own note says the example form carries `--no-verify`, which removes L2, and passes L1. That meets the line-649 Critical definition: a governed push to main succeeds with no layer refusing it, using an ordinary command. L1-5 is the same bypass class (an underscore prefix) and is rated Critical. | Rate G-44 Critical and reword its parenthesis. Make §8.8 and §8.9 and any other rating of G-44 agree. Alternatively, state why the line-649 rule does not apply. |

Blocking count: 2

## Notes (MINOR, non-blocking)

| # | Severity | Source lens | Affected section | Finding | Proposed fix |
|---|---|---|---|---|---|
| N1 | MINOR | rf-qa M-1; qualitative m-4 | Step 2.8 vs 2.1 and §8.10 (line 1292) | The 2.8 upgrade uses `rename`, but 2.1 and §8.10 say "never `rename`". There is an unnamed window between the hash re-read and the `rename`. | Name the exception in 2.1 and §8.10, and name the window. |
| N2 | MINOR | rf-qa M-2 | Tag key (line 27) | `[OBSERVED 2.47.3]` is now also used for the QA fix runs X1-X4. | Extend the key. |
| N3 | MINOR | rf-qa M-3 | L-2 row (line 556) | Does not cite fix run X1. | Cite X1. |
| N4 | MINOR | rf-qa M-4 | `qa/qa-fix-log.md` lines 14-21 | The X1-X4 commands are abridged, and `run.sh` is gone. | Note it only. |
| N5 | MINOR | rf-qa M-5; qualitative m-6 | §10.4, §10.5 (line 1467) | The Evidence Trail does not list the Gate 3 QA files that are now cited. It counts 43 gaps, but G-45 exists. | Add the files, and note that G-44 and G-45 were added at Gate 3. |
| N6 | MINOR | qualitative m-1 | SC-18 (line 589), step 2.1 | The order of the uv-dir write relative to the `pre-push` link is not stated. | Write the uv-dir file only after the link succeeds, or exempt it in SC-18. |
| N7 | MINOR | qualitative m-2 | G-44, §7 (line 1046), step 5.3, SC-28, §9 row 8 | `chrt 0 git ...` does not run git: `chrt 0 true` gave rc 1, "unsupported priority value". | Use `chrt -o 0` or `taskset 1` in the example. |
| N8 | MINOR | qualitative m-3 | SC-25 (line 596) | `ll_deny` is at lines 135-139, not 135-138. | Use 135-139. |
| N9 | MINOR | qualitative m-5 | Step 4.4 vs 4.3a | The refusal call does not pass the `l2=` field. | Pass `l2={...}`. |

Total: 0 CRITICAL, 2 IMPORTANT, 9 MINOR notes. The two verification reports raised 4 new IMPORTANT and 11 MINOR items; these merge into 2 blocking findings and 9 notes.
