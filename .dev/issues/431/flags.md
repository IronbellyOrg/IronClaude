# Flags decision

- Decided by: issue-worker-t2
- Depth: quick

| Field | Value | Reason |
|---|---|---|
| Mode | bug | The bug template fits an observed supervision defect: weak alive signals left the coordinator waiting on stalled workers; designing a v2 fix does not make the failure a new feature. |
| Type | agent | The defect concerns the coordinator agent's worker supervision and message handling, rather than a demonstrated CLI, hook or command implementation fault. |
| Complexity | simple | Follows depth (quick = simple); this classifies the issue draft, not the effort to implement the eventual orchestrator v2 fix. |
