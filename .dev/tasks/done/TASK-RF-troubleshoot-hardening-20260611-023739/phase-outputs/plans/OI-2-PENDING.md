# OI-2 — Human-Decision PENDING Marker

**STATUS: PENDING HUMAN DECISION**

**Date:** 2026-06-11
**Spec source:** RELEASE-SPEC v1.1.0 §11 (Open Items) OI-2; §5.6 H2 Contract Ledger Row schema (`contract_token` field).

## Verbatim OI-2 question (spec §11)

> OI-2 — Which tokens are first-class ledger entries (flags, phase IDs, gate names, verdicts, step IDs, statuses)? — Medium — Roadmap M2; schema seeded in §5.6 `contract_token`.

## Candidate token classes (examples, NOT a closed set)

- flags
- phase-IDs
- gate-names
- verdicts
- step-IDs
- statuses

## Binding instruction to the dependent item (Phase 3 Step 3.2 — `contract-enumeration.md`)

The `contract_token` first-class vocabulary in `contract-enumeration.md` **MUST NOT be finalized to a closed list** until this decision is resolved. Author the H2 ledger `contract_token` field as an **OPEN / extensible enumeration** that lists the candidate classes above as **examples**, and **explicitly defers the authoritative closed set to OI-2**. Do NOT silently ship a default closed vocabulary.

## Resolution state

G1 implementation approval was granted (2026-06-11), but OI-2 (the first-class token vocabulary) was **not** resolved as part of that approval. It remains PENDING. The dependent ref is authored as an open enumeration per the instruction above; no closed vocabulary is shipped.
