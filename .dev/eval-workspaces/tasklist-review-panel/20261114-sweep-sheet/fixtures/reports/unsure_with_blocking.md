review: 1 of 3

Two plan texts disagree about held reports. Notes follow.

## Ledger

```ledger-v1
{"item": "S1", "verdict": "UNSURE", "quote_plan": "The purge step keys on `legal_hold` and leaves such reports in place.", "quote_other": "The purge step must skip a report whose `legal_hold` flag is set.", "problem": "not sure the clause binds", "ran": "compared task and source"}
```

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "missing-requirement", "anchor": "The purge step keys on `legal_hold` and leaves such reports in place.", "refs": [], "claim": "An implementer who follows the stated text as written builds a purge that keeps held reports, and that is wrong because no criterion tests it.", "probe": "S1"}
```

verdict: FAIL
