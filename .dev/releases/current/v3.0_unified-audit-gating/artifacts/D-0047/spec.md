---
deliverable: D-0047
phase: 2
task: T02.01
status: committed
date: 2026-03-19
---

# D-0047: Wiring Whitelist Template

## Artifact
- `src/superclaude/cli/audit/wiring_whitelist.yaml`

## Schema
Three top-level sections: `unwired_callables`, `orphan_modules`, `unwired_registries`.
Each entry requires `symbol` (string) and optional `reason` (string).
