# Return contract 1.0

Write `<run>/return-contract.yaml`:

```yaml
contract_version: "1.0"
status: success | partial | failed
plan_path: <path> | null
source_path: <path> | null
strategy: systematic | agile | enterprise
depth: quick | standard | deep
handoff_action: none | design | implement | tasklist
handoff_output_path: <path> | null
unresolved: []
```

Wave 0 STOPs with no run dir (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-LEGACY`, `E-BAD-FLAG` before mkdir): chat only, **no** yaml.
After a run dir exists: STOP → write yaml `status: failed`, `plan_path: null`, `source_path` set if known else `null`.
Gate fail → `failed`.
Handoff implement missing skill → `failed` after plan exists (`plan_path` set).
