---
fixture: context_window_oom_case
master_recurrence_row: 17
deferred: true
---

# Recurrence #17 — Context-Window / OOM / Max-Turns Collapse (DEFER stub, hard)

> **Documented incident** (master:§Recurrence Matrix row #17):
> *"Context-window exhaustion / sprint phase OOM / max-turns budget collapse
> (exit -9, 'Prompt is too long', first-run-fails-resume-passes)."*
> Partition findings: `A1a:F-A1a-009`, `A6:F-A6-006`.

`A1a:F-A1a-009`: v2.02 Phase 2 exited `-9` silently. `A6:F-A6-006`: cliEval
Phase 5 crash from context-window exhaustion. The failure manifests as exit
`-9`, "Prompt is too long", and first-run-fails-then-resume-passes
non-determinism.

This is a **runtime-resource failure**, not a scanner-input-testable shape: no
deterministic component consumes a fixture to reproduce a context-window/OOM/
max-turns collapse. Hard DEFER. Retained as an auditable stub.
