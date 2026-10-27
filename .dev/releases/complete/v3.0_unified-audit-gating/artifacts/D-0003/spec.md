---
deliverable: D-0003
phase: 2
task: T02.02
status: committed
date: 2026-03-19
---

# D-0003: WiringFinding and WiringReport Dataclasses

## Artifact
- `src/superclaude/cli/audit/wiring_gate.py` (data model section)

## Deliverables
- `WiringFinding` with finding_type, file_path, symbol_name, line_number, detail, severity, suppressed
- `WiringReport` with category lists, derived properties (total_findings, clean, blocking_count)
- Single-source-of-truth invariant: category sum == total_findings
- Blocking semantics per rollout mode (shadow=0, soft=critical, full=critical+major)
