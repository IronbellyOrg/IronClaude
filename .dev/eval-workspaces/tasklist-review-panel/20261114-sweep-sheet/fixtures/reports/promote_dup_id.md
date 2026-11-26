review: 1 of 3

The reviewer already used both ids that a promoted line could get. Notes follow.

## Ledger

```ledger-v1
{"item": "S1", "verdict": "PROBLEM", "quote_plan": "The purge step keys on `legal_hold` and leaves such reports in place.", "quote_other": "The purge step must skip a report whose `legal_hold` flag is set.", "problem": "The task keeps held reports but no criterion tests it.", "ran": "compared task and source 2.3"}
```

## Findings block

```findings-v1
{"id": "PS1", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "A deletion notice must name the report id, state the expiry date, and give the appeal address.", "refs": [], "claim": "The notice task never names the appeal address."}
{"id": "PS1-2", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "The retention job gets its age limit from one setting.", "refs": [], "claim": "The setting is not named."}
```

verdict: FAIL
