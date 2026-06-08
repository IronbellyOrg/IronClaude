---
fixture: sprint_executor_vacuous_gate_case
master_recurrence_row: 21
deferred: true
---

# Recurrence #21 — Sprint Executor Ignores Deps / Vacuous Gates (DEFER stub, out of scope)

> **Documented incident** (master:§Recurrence Matrix row #21):
> *"Sprint executor ignores task dependencies; reuses roadmap gates vacuously;
> no feedback loop back to roadmap."*
> Partition findings: `A11:F-A11-023`, `A12:F-A12-13`.

`A11:F-A11-023`: the sprint executor ignored task dependencies. `A12:F-A12-13`:
sprint reused `ANTI_INSTINCT_GATE` vacuously (the gate passes trivially when
applied to sprint-stage inputs it was not designed for).

This row is **explicitly OUT of scope** per BUILD-REQUEST §Scope: the
roadmap-pipeline rewrite (R0/R1) does not touch `sprint/executor.py`. It is a
sprint-layer recurrence outside the R0/R1 boundaries. §Scope tension recorded:
no fixture is constructed because the component lives outside the rewrite's
surface. Retained as an auditable stub.
