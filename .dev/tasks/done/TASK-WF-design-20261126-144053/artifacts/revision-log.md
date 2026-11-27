# Revision 1 log

- old package: TASK-WF-design-20261126-134817
- new package: TASK-WF-design-20261126-144053
- old plan sha256: efc064767784deab7cfb2f67d769513f87c252aab0b1de601a3a158ab521e11d
- review report: .dev/reflect/pre-TASK-WF-design-20261126-134817-20261126135219/REPORT.md
- finding_counts: {"blocking": 3, "label_high": 0, "medium": 2, "note": 4}

## Fix map

# Fix map (revision 1 of TASK-WF-design-20261126-134817)

Reviser: `workflow-reviser` (Read, Edit, Grep, Glob). Brief: repair only the blocking findings D-1, D-2 and D-3 of `.dev/reflect/pre-TASK-WF-design-20261126-134817-20261126135219/REPORT.md`. The plan grew from 14863 to 16697 bytes (+1834). Medium findings D-4 and D-5 and the Notes were left alone.

Bytes (the reviser's hand count): D-1 +591 -162, D-2 +415 -179, D-3 +1053 -126, shared Constraints bullet +242.

```fixmap-v1
{"id": "D-1", "action": "applied", "reason": "Task 4 now requires exactly one \"is being worked out in\" (the issue 290 card), uses `git diff -U0 HEAD --` before Task 5, and Task 7's deck test is stated to assert that and override source.md line 106."}
{"id": "D-2", "action": "applied", "reason": "Task 7's last bullet is replaced by a stateless root-level check that excludes `.dev`, checks the staged `.claude/` and `.dev/issues/` paths, and limits `.dev/tasks` status to its own paths, with a note on why plain `git status --short` is not used."}
{"id": "D-3", "action": "applied", "reason": "Task 1 now carries the four exact edits that state the handoff exemption, the substring list and the fifteen key phrases in Task 7 were updated (the thirteen tests count kept), Task 3 says to re-copy after later guide edits, and the Constraints block says this plan overrides source.md."}
```
