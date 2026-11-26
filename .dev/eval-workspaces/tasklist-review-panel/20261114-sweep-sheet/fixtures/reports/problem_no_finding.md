review: 1 of 3

Two plan texts disagree about held reports, and one item stays open. Notes follow.

## Ledger

```ledger-v1
{"item": "S1", "verdict": "PROBLEM", "quote_plan": "The purge step keys on `legal_hold` and leaves such reports in place.", "quote_other": "The purge step must skip a report whose `legal_hold` flag is set.", "problem": "The task keeps held reports but no criterion tests it.", "ran": "compared task and source 2.3"}
{"item": "S2", "verdict": "OK", "quote_plan": "", "quote_other": "", "problem": "", "ran": "compared both scopes"}
{"item": "S3", "verdict": "UNSURE", "quote_plan": "No remaining `3 report formats` text exists in `docs/guide.md`.", "quote_other": "", "problem": "The count may be spelled out elsewhere.", "ran": "read the guide task"}
```

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "A deletion notice must name the report id, state the expiry date, and give the appeal address.", "refs": [], "claim": "The notice task never names the appeal address."}
```

verdict: FAIL
