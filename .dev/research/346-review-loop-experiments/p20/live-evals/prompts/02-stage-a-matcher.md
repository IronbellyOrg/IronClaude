# Prompt 02: map one reviewer report to ledger defects (blind matcher; use Sonnet)

Directory: P17=<repo>/.dev/research/346-review-loop-experiments/p17

Files (read only these):
- Ledger: `$P17/score/ledger-blind.json` (44 defects D01-D44 in the original spec, each with a description and an `is_fixed_when` test)
- Original spec: `$P17/spec-original.md`
- Report to match: `{{REPORT_PATH}}` (a first-round review report; its `findings-v1` block lists the findings)

You do not know which model wrote the report and must not try to find out.

For EVERY finding in the report's findings block, decide which ledger defect it is about:
- `defect`: the single best-matching ledger id (D01-D44) when the finding, as written, points at the same flaw (same place and same wrong behaviour; a finding that merely mentions the right area does not count), else `null`
- `also`: a second ledger id when the finding clearly covers two defects, else `null`
- `confidence`: `high` | `medium` | `low`; `note`: one sentence quoting the finding text and the ledger text that match

Write valid JSON to `{{OUT_PATH}}`:
`{"model": "{{MODEL}}", "rep": {{REP}}, "findings": [{"fid": "F1", "heading": "...", "severity_claimed": "blocking|...", "defect": "D07|null", "also": null, "confidence": "high", "note": "..."}, ...]}`
One entry per finding, in the report's order. The `model` field is copied from the run manifest by the coordinator, not from the report. Final reply: `DONE <path>` and the number of findings and of matched findings.
