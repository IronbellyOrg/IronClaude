---
fixture: truncation_no_detection_case
master_recurrence_row: 20
deferred: true
---

# Recurrence #20 — One-Shot stdout / 64k Cap / No Truncation Detection (DEFER stub)

> **Documented incident** (master:§Recurrence Matrix row #20):
> *"One-shot stdout / 64k token cap / no truncation detection / no template
> enforcement → 49% fewer tasks on TDD+PRD vs spec-only."*
> Partition findings: `A11:F-A11-005`, `A12:F-A12-12`.

`A11:F-A11-005`: one-shot stdout capture truncated at the 64k token cap with no
completeness check, yielding 49% fewer tasks on TDD+PRD vs spec-only.
`A12:F-A12-12`: corrected RCA — format artifact plus no phase-count floor.

This is a **transport/harness truncation concern**: the failure lives in how
agent stdout is captured (one-shot, 64k cap), not in any roadmap-pipeline scanner
that consumes a fixture. R1.4 tool-write mitigates the truncation class
structurally (incremental tool-write instead of one-shot stdout) but there is no
roadmap-scanner fixture input. Retained as an auditable stub.
