# Revision log 1 (surgical edit of TASK-WF-implementDocsDes-20261120-005507)

Original plan sha256: d4c233ede3218a6fc00d9ee3bc92f8e65b4696caf0f10772166ef9a4c769d5fa (byte copy in ./old-plan.md; the archived original is unchanged).
Edits were made with the Edit tool on a copy in /tmp, 31 calls, one finding group per call group. Only blocking findings (B1 to B12 of the review report, ./prior-findings.md) and the same-spot Medium wording were touched.

| Finding | Edit |
|---|---|
| B1 plugin command mirror and test | Constraints mirror rule names `commands/workflow.md`; Task 8 mirrors the file, updates `argument-hint`, adds the `cmp` and `tests/commands` criteria |
| B2 git-HEAD tests | Task 2 rewrites the two tests in `test_shadow_skill_contract.py`; new acceptance bullet |
| B3 id recorded before placement | Task 4 gains `reserve`; `archive` and `place` take the reserved id; test for a collision suffix |
| B4 gate on the copy | Task 4 `prepare` renames the copy and rewrites `slug` to the reserved id; Task 5 states the order |
| B5 Task 13 check | Acceptance names the two packages the grep really returns; the 20261116 package has no contract |
| B6 no Agent tool | Task 6 adds the Agent tool to `allowed-tools` and limits the fan-out ban |
| B7 Wave 5 target | Task 6 makes Wave 5 write to the final placed package |
| B8 no writer for fields | Task 4 adds `mark` |
| B9 Revision section and artifacts | Task 4 `place` writes them |
| B10 unknown replacement id | Task 4 `archive --superseded-by none`; Task 13 uses it for six packages |
| B11 lint version | Task 2 accepts 1.8.0 and 1.9.0 |
| B12 plugin mirror of new files | Constraints and Task 6 mirror the new ref and script, creating `scripts/` |
| Mediums folded in | restore undo, stdlib-only script, test-pinned wording in Task 7, `qa.md` STOP list in Task 9, 4.3a sentence in Task 1, panel mapping of medium and note, forced regenerate order, Task 10 dependency on Task 7, counts source in Task 5 |

# Revision log 2 (surgical edit of TASK-WF-implementDocsDes-20261120-020554)

Original (cycle-1) plan sha256 is in ./old-plan.sha256; the cycle-1 plan is ./old-plan.md and the first original is ./plan-1-original.md. The diff of this cycle is ./plan.diff.
Re-review of cycle 1: 11 of 12 prior blockers resolved, B2 partly open (Medium N1), one new blocking finding.

| Finding | Edit |
|---|---|
| N2 (Blocking, Safety): Wave 5 could replace the contract and drop `review_verdict: FAIL` | Task 6 says Wave 5 merges into the contract and keeps the lines `place` and `mark` wrote, and gets a test criterion; Task 7 rewrites the relocation rule to merge |
| N1, N3 to N12 | Medium and Note: not touched (only blocking findings are repaired); listed as follow-up candidates in the final report |

# Revision log 3 (surgical edit of TASK-WF-implementDocsDes-20261120-021216, owner order: fold in the Mediums)

The diff of this cycle is ./plan.diff; the cycle-2 plan is ./old-plan.md. Edits made with the Edit tool on a copy, 16 calls.

| Finding | Edit |
|---|---|
| R1 Task 6 test needs Task 7 wording | Task 6 depends on Task 7 |
| R2, R4 Wave 5 field list and missing contract | Task 6: Wave 5 creates the contract when none exists and fills the missing stable 1.1 fields |
| N1, N12 allowed sections of the rewritten test | Task 2 lists 4.3a, 9.1, 9.4 only if edited, 17.6; Task 1 says the sentence sits in 9.1 |
| N3, R3 duplicate keys | `mark` is the one writer of fix_cycles, review_verdict, open_blockers, superseded_by (and the regenerate link fields), replacing an existing line; `archive` uses the same code; `place` no longer writes fix_cycles |
| N4 unresolved list shape | `archive` edits as text, handles `[]`, absent key, list not last; test added |
| N5 case-insensitive match | `archive` adds no second item when the text says "superseded" in any case; test added |
| N6 test text | Task 4 acceptance says `reserve` picks the suffix, `place` checks the leaf |
| N7 empty leaf left behind | new `release` subcommand and its test |
| N8 order of mark | Task 5: re-review first, then `mark` once |
| N9 regenerate route | `place` is surgical only; `mark --supersedes --route regenerate` links a regenerated package |
| N10, N11 | Task and Agent tool names; the plugin mirror reason |
