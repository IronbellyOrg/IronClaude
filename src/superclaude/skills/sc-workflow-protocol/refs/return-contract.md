# Return contract 1.0

Write `<run>/return-contract.yaml`:

```yaml
contract_version: "1.0"
status: success | partial | failed
plan_path: <path> | null
source_path: <path>
strategy: systematic | agile | enterprise
depth: quick | standard | deep
handoff_action: none | design | implement | tasklist
handoff_output_path: <path> | null
unresolved: []
```

STOP before Wave 2 → `status: failed`, `plan_path: null`.
Gate fail → `failed`.
Handoff implement missing skill → `failed` after plan exists (`plan_path` set).
