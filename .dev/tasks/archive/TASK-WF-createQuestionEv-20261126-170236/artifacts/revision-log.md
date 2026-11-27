# Revision 2 log

- old package: TASK-WF-createQuestionEv-20261126-142533
- new package: TASK-WF-createQuestionEv-20261126-170236
- old plan sha256: 80adb9e26e3b27b64b3fc138be1436c29ec49e222094d1bf059cb934698fec13
- review report: .dev/reflect/pre-createQuestionEv-20261126142850/REPORT.md
- finding_counts: {"blocking": 4, "label_high": 4, "medium": 12, "note": 6}

## Fix map

# Fix map of the surgical repair (saved by the coordinator from the reviser's returned text)

Reviser: workflow-reviser (Read, Edit, Grep, Glob). Candidate: the copy of TASK-WF-createQuestionEv-20261126-142533 placed as TASK-WF-createQuestionEv-20261126-170236. Bytes (reviser's hand count): added 2207, deleted 210, net +1997; measured file size 35249 to 37247 (+1998).

```fixmap-v1
{"id": "B-1", "action": "applied", "reason": "Task 4 now names the dry run's isolated home and configuration directory, the three unset variables, the failing gh stub, the invalid push URL and a probe prompt that never invokes /sc:issue, in a bullet and in an acceptance criterion."}
{"id": "B-2", "action": "applied", "reason": "Task 9 now requires both git diff origin/integration...HEAD -- <the three files> and git diff HEAD -- <the three files> to be empty, and the acceptance line says AC4 shows both diffs empty."}
{"id": "B-3", "action": "applied", "reason": "Task 3 now has the two preserved-flag cases (New material disagreement gives zero questions, changed-flag Contradictions item with flag as passed and a different drafted value gives one), keeping the Wave 2 section sentence check and the Wave 5 step 7 pushback check."}
{"id": "B-4", "action": "applied", "reason": "A Constraints bullet and one line in each of Tasks 4 to 8 route raw run output to a scratch directory outside the repository (named in Task 4), and Task 9 scans it and copies only scanned files into ./artifacts/ without any never-stage-.dev/tasks sentence."}
```
