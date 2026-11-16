review: 1 of 3

Two plan texts disagree about held reports. Notes follow.

## Ledger

```ledger-v1
{"item": "S1", "verdict": "PROBLEM", "quote_plan": "The purge step keys on `legal_hold` and leaves such reports in place.", "quote_other": "The purge step must skip a report whose `legal_hold` flag is set.", "problem": "The task keeps held reports but no criterion tests it.", "ran": "compared task and source 2.3"}
{"item": "S9", "verdict": "PROBLEM", "quote_plan": "No remaining `3 report formats` text exists in `docs/guide.md`.", "quote_other": "The exporter package has no network access.", "problem": "no such item", "ran": "compared the two texts"}
```

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "missing-requirement", "anchor": "The purge step keys on `legal_hold` and leaves such reports in place.", "refs": [], "claim": "An implementer who follows the stated text as written builds a purge that keeps held reports, and that is wrong because no criterion tests it.", "probe": "S1"}
```

verdict: FAIL
