review: 1 of 3

Two plan texts disagree about held reports. Notes follow.

## Ledger

```ledger-v1
{"item": "S1", "verdict": "PROBLEM", "quote_plan": "Create `src/exporter/notice.py`. Write the notice body\nexactly as the quote below, with the report id filled in.", "quote_other": "The purge step must skip a report whose `legal_hold` flag is set.", "problem": "The notice text is dictated and also constrained.", "ran": "compared the two texts"}
{"item": "S2", "verdict": "PROBLEM", "quote_plan": "Source sections: 2.1 Acceptance criteria:", "quote_other": "The exporter package has no network access.", "problem": "The criteria block does not follow the source sections line.", "ran": "compared the two texts"}
```

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "missing-requirement", "anchor": "Write the notice body exactly as the quote below", "refs": [], "claim": "An implementer who follows the stated text as written builds a notice with a fixed text, and that is wrong because no criterion tests it.", "probe": "S1"}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "missing-requirement", "anchor": "Source sections: 2.1\nAcceptance criteria:", "refs": [], "claim": "An implementer who follows the stated text as written builds a task with no source, and that is wrong because no criterion tests it."}
```

verdict: FAIL
