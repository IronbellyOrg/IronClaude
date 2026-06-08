---
fixture: generator_validator_asymmetry_case
master_recurrence_row: 10
deferred: true
---

# Recurrence #10 — Generator/Validator Asymmetry (meta-pattern, DEFER stub)

> **Documented incident** (master:§Recurrence Matrix row #10):
> *"Generator/validator asymmetry; validators deterministic, generators
> non-deterministic; every fix adds a downstream validator, none constrain the
> generator."*
> Partition findings: `A1b:F-A1b-005`, `A12:F-A12-03`.

`A1b:F-A1b-005`: context-window overflow caused Phase 7 ID drift the generator
silently produced and the validator caught post-hoc. `A12:F-A12-03`: the
"multi-release harden-orchestration-around-broken-comparator" anti-pattern —
every release wrapped new validation machinery around the same generator without
constraining it.

This is the **architectural meta-driver**, not a single scanner input: it
describes the *shape* of every other recurrence (each fix adds a downstream
validator; none constrain the non-deterministic generator). R1.4 tool-write
generator-side constraints address it structurally (attested in R1.4 Findings),
not via a fixture. Retained as an auditable stub.
