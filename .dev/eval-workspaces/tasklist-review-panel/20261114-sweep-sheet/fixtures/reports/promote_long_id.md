review: 1 of 3

One item has an unusually long id. Notes follow.

## Ledger

```ledger-v1
{"item": "S123456789012345", "verdict": "PROBLEM", "quote_plan": "The purge step keys on `legal_hold` and leaves such reports in place.", "quote_other": "The purge step must skip a report whose `legal_hold` flag is set.", "problem": "The task keeps held reports but no criterion tests it.", "ran": "compared task and source 2.3"}
```

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "A deletion notice must name the report id, state the expiry date, and give the appeal address.", "refs": [], "claim": "The notice task never names the appeal address."}
```

verdict: FAIL
