---
schema_version: "1.0"
tier: "T2"
suspect: true
reviewer_model_id: ""
reviewer_model_label: ""
target: "<<TARGET>>"
target_checksum: "c8ce0d9b805943cb7aa8b27f36d4c951a92f37648fde216bc89084abc67cecba"
target_truncated: false
generated: "2026-06-01T17:59:55Z"
caller_label: ""
elapsed_ms: 0
finding_count: 4
---

# T2-Bare Review — _review_target

## Findings

| ID | Sev | Claim | Cite | SelfConf |
|----|-----|-------|------|----------|
| F-01 | crit | citation is plain dash | none | 50 |
| F-02 | med | unknown severity maps to med | none |  |
| F-03 | nit | self-conf is non-numeric | none |  |
| F-04 | high | self-conf is 250 (clamped) | src/x.py:9 | 100 |

## Verdict
Edge cases: severity aliasing, empty cites, confidence clamping.
