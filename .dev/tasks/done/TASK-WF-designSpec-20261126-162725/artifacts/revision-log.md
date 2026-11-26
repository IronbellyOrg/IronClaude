# Revision 2 log

- old package: TASK-WF-designSpec-20261126-152817
- new package: TASK-WF-designSpec-20261126-162725
- old plan sha256: cac5150528c4f8a7f3911dda2f543df6a8068c597a11f4f5cb4123a806c35b28
- review report: .dev/reflect/pre-designSpec-20261126153331/REPORT.md
- finding_counts: {"blocking": 3, "label_high": 0, "medium": 11, "note": 7}

## Fix map

# Fix map (reviser output, saved by the coordinator)

Brief: repair the blocking findings M-1, M-2, M-3 of `.dev/reflect/pre-designSpec-20261126153331/REPORT.md`, plus M-11 and M-12 on the owner's explicit instruction (not blocking findings; the owner's instruction of 2026-11-26 covers them). Bytes: before 36948, after 39026, added 2268, deleted 190 (net +2078, confirmed by the coordinator with `wc -c`).

```fixmap-v1
{"id": "M-1", "action": "applied", "reason": "Task 6's systemic-signal bullet now states zero posts for KeyMissing and for the spend_bound refusal, one post each for 401 and model_mismatch, an injected budget_exhausted stop, and a rerun-not-stop timeout."}
{"id": "M-2", "action": "applied", "reason": "The six-definitions reading step is added in Task 7's procedure text, as the README step immediately before gate.py freeze-corpus, and as a new Task 8 acceptance bullet, with no refusal added to freeze-corpus."}
{"id": "M-3", "action": "applied", "reason": "freeze-table and freeze-rule now state the refusal when the manifest already holds their keys, and the Task 4 acceptance bullet names a second freeze-table and a second freeze-rule."}
{"id": "M-11", "action": "applied", "reason": "The README keyscan step now states the JEV_API_KEY from TYPESAFE_API_KEY mapping inside one subshell command with no printing or writing of the key, and a Task 8 acceptance bullet requires it."}
{"id": "M-12", "action": "applied", "reason": "A Constraints bullet makes the four command-line modules insert jevlib and the experiment folder into sys.path as probe.py does, and a Task 8 acceptance bullet requires a --help script run from an unrelated directory."}
```
