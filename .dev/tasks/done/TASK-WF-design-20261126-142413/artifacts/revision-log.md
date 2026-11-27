# Revision 1 log

- old package: TASK-WF-design-20261126-131233
- new package: TASK-WF-design-20261126-142413
- old plan sha256: eb72c524a239d0484dce61cb4094c0e58560e4c718c2bd140171127342da0555
- review report: .dev/reflect/pre-TASK-WF-design-20261126-131233-20261126131756/REPORT.md
- finding_counts: {"blocking": 3, "label_high": 0, "medium": 3, "note": 1}

## Fix map

# Fix map of the surgical repair (reviser output, saved by the coordinator)

The reviser (`workflow-reviser`, Read/Edit/Grep/Glob only) made eight Edit calls on the copy of the plan and repaired only the blocking findings M1, M2 and M3 of the review report `.dev/reflect/pre-TASK-WF-design-20261126-131233-20261126131756/REPORT.md`. Its own size estimate was about 17,900 bytes before and about 20,600 after; the measured sizes are 18,035 before and 20,110 after. Its per-finding byte estimates (not measured): M1 about +2,030 and -400, M2 about +900 and -190, M3 about +270 and -0.

Checks the coordinator ran after the reviser returned: the original plan, the review report and a content digest of the whole checkout are byte-identical to their values before the reviser started; no numbered or checkbox line, no absolute path and no finding id appears in the plan text.

## Fix map

```fixmap-v1
{"id": "M1", "action": "applied", "reason": "Deleted the Task 2 mutation bullet, added the no-argument sentence to Task 2, and added the in-memory nine-case mutation bullet to Task 7."}
{"id": "M2", "action": "applied", "reason": "Rewrote the Constraints format-fix wording, extended Task 1's body and first bullet to record the ruff baseline, and replaced Task 7's ruff bullet with the baseline-relative wording."}
{"id": "M3", "action": "applied", "reason": "Appended the blocked sentence to the commit Constraints bullet and added the named blocked line instruction to Task 7's body."}
```
