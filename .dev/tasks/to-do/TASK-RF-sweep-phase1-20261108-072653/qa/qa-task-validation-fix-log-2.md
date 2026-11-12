# Fix log: task validation fix cycle 2 (A.10 cycle 2, A.10.25 cycle 1)

**Task file:** TASK-RF-sweep-phase1-20261108-072653.md
**Date:** 2026-11-08
**Sources:** `qa/qa-task-validation-verify-1.md` (V-01, V-02), `qa/qa-task-research-alignment-report.md` (I-1 to I-4)

## Findings

| Finding | Item(s) changed | Result | Notes |
|---|---|---|---|
| V-01 (verify-1) | 14.8 | FIXED | The Branch (B) `blocker_reason` now says the coordinator saves to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx.txt`, the same path as Branch (A) and the Output field. A grep for a bare `artifacts/sweep-help-pipx` without the task folder prefix returns nothing. |
| V-02 (verify-1) | 9.5 to 9.12 (new 9.12), 9.13 to 9.21 (renumbered from 9.12 to 9.20) | FIXED | Added item 9.12, an `rf-qa-qualitative` failure-path lens with the report-only preamble and the lens prompt embedded in full, output `qa/impl-cli/qa-failure-path-report.md`. The gate is now 5 rf-qa (4 plus the read-only and allowlist safety domain lens) and 3 rf-qa-qualitative, which meets I22 at full intensity. Titles say "of 8"; every parallel-spawn range says "9.5 to 9.12"; the sizing sentence says 8 agents with the split; the consolidation item (now 9.13) says "eight reports", lists the eighth report name, and checks for 8 reports. The old items 9.12 to 9.20 moved to 9.13 to 9.21, and every item reference inside Phase 9 moved with them (37 references). No item outside Phase 9 referred to 9.5 to 9.20. |
| I-1 (alignment) | 5.1, 5.3, 5.11, 5.12 | FIXED | Checked at HEAD: `grep -n 'WC-14' docs/designs/orchestrator-mode.md` hits lines 5 and 13 (section 1), 812 (section 13), 835 (section 14), 988 and 989 (section 17), none owned by any item. Item 5.3 now covers sections 1, 12, 13, 14, 15, 16 and 17: it renames lines 5, 13, 988 and 989 to WC-16, and at 812 and 835 keeps `WC-14` (it names the SPEC and REPORT drafts) and appends "(WC-16 in this design)". Item 5.1 adds the third hit class `historical name (keep)` for those two lines only. Items 5.3 and 5.12 accept that class; 5.12 expects WC-16 hits in sections 1, 8, 9, 10, 12, 13, 14, 15, 16 and 17; the 5.11 revision-log text lists the new sections. 5.3 also checks the open-item total stays 23. |
| I-2 (alignment) | 2.7 | FIXED | The pass rule is now per section, matching what research/04 edits 1 to 9 and the 2.3 fixtures write: 7.2, 2.2 and 18 hold all four model names; 7.1 holds `first_record_ts`; 11 holds `first_record_ts` and the three `dispatch_*` names from the copied fixture expectations; 15.1 and 17 hold the three dotted Orca source names. A second grep for the dotted names was added, the matrix has a column per source name, and the seven checks are listed by number so the "seven checks" verification is concrete. No DESIGN edit was added. |
| I-3 (alignment) | 8.3, 8.4 | FIXED | 8.3 Context now names the model fields `dispatch_started: datetime | None`, `dispatch_ended: datetime | None` and `dispatch_status: str | None`, parsed from the `worker-show` paths `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` (research/04:87), and `first_record_ts: datetime | None` (research/04:88). 8.3 Verification adds a `grep -c` for each of the four typed fields, each expected to return 1. 8.4 Context now states the full window rule from research/04:90, including the `dispatch_status` condition (`pending` or `dispatched` when `dispatch_ended` is None) and the no-window note `Dispatch time window not observable`. |
| I-4 (alignment) | 5.7 | FIXED | 5.7 now writes research/09's four points (research/09:113-115) into DESIGN: the `gh` state line (MERGED, `2327fbd3`), the `2327fbd3` ancestor check, the `495eb96d` non-ancestor check, and the re-read note. These are the same four points item 7.19 records, so 7.19 was left unchanged. The dropped points (15 P2 conversions, 31 `UNATTENDED_EXPECT` entries) stay in 5.7 Context as background and in item 5.8, which records the 31 count as a master constraint. 5.7 also keeps research/09's rule that the gate on step 1.17 stays and is satisfied once the record is written; its Verification forbids the old "wait for", "follow-up PR", "rebase" and "if #422 is open" wording and checks the entry names `2327fbd3`, `495eb96d` and the re-read note. |

## Constraint checks

- Phase order, HALT behaviour and scope: unchanged. The new item 9.12 is one more report-only lens in an existing gate.
- POST reflect runner prompt: not touched (no edit in Phase 14 except the 14.8 path).
- No commit, push or merge item was added.
- Numbering: item ids are unique (351 ids, no duplicates), and every `item N.M` reference in the file resolves to an existing id.
- Em dashes: none added to the fix log. Task file em-dash count is unchanged apart from the new 9.12 title, which uses the same separator as every other item title.

## Counts

- Fixed: 6. Not fixed: 0.
- Task file: 2863 lines (was 2856), 351 items (was 350).

Status: COMPLETE
