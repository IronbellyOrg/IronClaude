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
finding_count: 2
---

# T2-Bare Review — _review_target

## Findings

| ID | Sev | Claim | Cite | SelfConf |
|----|-----|-------|------|----------|
| F-01 | crit | unbounded recursion in tree-walk on cyclic input | tree.py:88 | 90 |
| F-02 | med | missing index on join column slows query 12x | db/queries.py:340 | 70 |

## Verdict
Cyclic-input crash is reproducible; the index gap is real but acceptable until next migration window.
