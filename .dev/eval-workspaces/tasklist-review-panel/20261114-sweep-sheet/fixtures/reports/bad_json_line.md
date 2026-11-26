review: 1 of 3

Two plan texts disagree about held reports. Notes follow.

## Ledger

```ledger-v1
{"item": "S1", "verdict": "PROBLEM", "quote_plan": "The purge step keys on `legal_hold` and leaves such reports in place.", "quote_other": "The purge step must skip a report whose `legal_hold` flag is set.", "problem": "The task keeps held reports but no criterion tests it.", "ran": "compared task and source 2.3"}
{"item": "S2", "verdict": "PROBLEM", "quote_plan": "Every module under `src/exporter/` returns an empty result for an empty report.", "quote_other": "The exporter package has no network access.", "problem": "broken line below", "ran": "compared the two texts"
{"item": "S3", "verdict": "PROBLEM", "quote_plan": "No remaining `3 report formats` text exists in `docs/guide.md`.", "quote_other": "docs/guide.md:14: The exporter writes 3 report formats to disk.", "problem": "The grep still finds the old count text.", "ran": "ran git grep on the guide"}
```

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "missing-requirement", "anchor": "The purge step keys on `legal_hold` and leaves such reports in place.", "refs": [], "claim": "An implementer who follows the stated text as written builds a purge that keeps held reports, and that is wrong because no criterion tests it.", "probe": "S1"}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "missing-requirement", "anchor": "Every module under `src/exporter/` returns an empty result for an empty report.", "refs": [], "claim": "An implementer who follows the stated text as written builds a module that returns an empty result, and that is wrong because no criterion tests it.", "probe": "S2"}
{"id": "F3", "severity": "CRITICAL", "blocking": true, "category": "missing-requirement", "anchor": "No remaining `3 report formats` text exists in `docs/guide.md`.", "refs": [], "claim": "An implementer who follows the stated text as written builds a guide that still shows the old count, and that is wrong because no criterion tests it.", "probe": "S3"}
```

verdict: FAIL
