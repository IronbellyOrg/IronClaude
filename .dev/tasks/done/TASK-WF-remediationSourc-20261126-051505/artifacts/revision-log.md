# Revision 1 log

- old package: TASK-WF-remediationSourc-20261126-040738
- new package: TASK-WF-remediationSourc-20261126-051505
- old plan sha256: 64c60cd1d108e48ac0875a87d896c6e37cdf8a71cc869df077d96d0eaf99b383
- review report: /home/coder/workspaces/worktrees/IronClaude/issue-393/.dev/reflect/pre-TASK-WF-remediationSourc-20261126-040738-20261126041149/REPORT.md
- finding_counts: {"blocking": 3, "label_high": 0, "medium": 7, "note": 6}

## Fix map

# Fix map (workflow-reviser, cycle 1)

Blocking findings repaired: M-1, M-2, M-3 (from `.dev/reflect/pre-TASK-WF-remediationSourc-20261126-040738-20261126041149/REPORT.md`). Medium and Note findings were left alone, as the remediation rule requires.

The reviser measured no byte totals (no shell). Hand-counted per finding, bytes added and deleted: M-1 2363 and 331; M-2 371 and 35; M-3 202 and 0. The coordinator measures the real sizes with `wc -c` (see `revision-log.md` after placement).

Reviser note on M-1: changing `opus` to `sonnet` inside "is `opus` for every adviser" necessarily fails both the exact-phrase pin and the `sonnet` count pin, so the plan lists both pins for that mutation instead of claiming a single failure.

```fixmap-v1
{"id": "M-1", "action": "applied", "reason": "Task 3 now fixes the exact sentence and Task 6 pins the phrase, the sonnet/haiku/fable count, the region anchors, the no-model-id check, the line 181 words and five mutation checks, with one mutation (opus to sonnet in the rule) listing two pins because pins (a) and (b) both see it."}
{"id": "M-2", "action": "applied", "reason": "Task 6 adds a source field to the record, checks that no record's source is T2Model01 without comparing ids, adds the third negative control, and says three wherever it counted controls."}
{"id": "M-3", "action": "applied", "reason": "Task 6 acceptance now requires uv run mypy on the new test file with no new diagnostics, a typed record and a not-None check on regex matches."}
```
- measured sizes: plan 20352 bytes before, 22926 bytes after (+2574; the reviser's hand count was +2570); the reviser could not measure sizes (no shell)
