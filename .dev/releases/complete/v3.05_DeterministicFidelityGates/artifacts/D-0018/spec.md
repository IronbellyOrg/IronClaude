# D-0018: RunMetadata with Split HIGH Counts

## Overview

`RunMetadata` dataclass with `run_number`, `timestamp`, `spec_hash`, `roadmap_hash`, `structural_high_count`, `semantic_high_count`, `total_high_count`.

## Implementation

Location: `src/superclaude/cli/roadmap/convergence.py:34-45`

```python
@dataclass
class RunMetadata:
    run_number: int
    timestamp: str
    spec_hash: str
    roadmap_hash: str
    structural_high_count: int = 0
    semantic_high_count: int = 0
    total_high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
```

Run metadata is populated at the end of `merge_findings()` with split counts from active findings.

## Verification

Verified via `TestRegistryStableIDs::test_run_metadata_split_high_counts` and `TestThreeRunSimulation::test_three_run_simulation`.
