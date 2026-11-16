review: 1 of 3

Notes on F1:
An implementer who follows the stated text as written builds a purge that keeps held reports, and that is wrong because no criterion tests it.
Filler line 1 about the exporter.
Filler line 2 about the exporter.
Filler line 3 about the exporter.
Filler line 4 about the exporter.
Filler line 5 about the exporter.
Filler line 6 about the exporter.
Filler line 7 about the exporter.
Filler line 8 about the exporter.
Filler line 9 about the exporter.
Filler line 10 about the exporter.
Filler line 11 about the exporter.
Filler line 12 about the exporter.
Filler line 13 about the exporter.
Filler line 14 about the exporter.
Filler line 15 about the exporter.
Notes on F2: the empty-report rule is unclear.

## Ledger

```ledger-v1
{"item": "S1", "verdict": "PROBLEM", "quote_plan": "The purge step keys on `legal_hold` and leaves such reports in place.", "quote_other": "The purge step must skip a report whose `legal_hold` flag is set.", "problem": "The task keeps held reports but no criterion tests it.", "ran": "compared task and source 2.3"}
{"item": "S2", "verdict": "PROBLEM", "quote_plan": "Every module under `src/exporter/` returns an empty result for an empty report.", "quote_other": "The exporter package has no network access.", "problem": "A module may need the network to be empty-safe.", "ran": "compared two plan lines"}
```

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "missing-requirement", "anchor": "The purge step keys on `legal_hold` and leaves such reports in place.", "refs": [], "claim": "The purge task and the source disagree about held reports.", "probe": "S1"}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "missing-requirement", "anchor": "Every module under `src/exporter/` returns an empty result for an empty report.", "refs": [], "claim": "The empty-report rule may need the network.", "probe": "S2"}
```

verdict: FAIL
