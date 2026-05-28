# D-0019 — Spec (T02.04 Publish DM-005-M2 Phase Contract row)

**Task:** T02.04 — Publish DM-005-M2 Phase Contract row
**Roadmap row:** R-037
**Tier:** STRICT
**Deliverables:**
1. DM-005 explicit row published in `src/superclaude/skills/task-builder/SKILL.md` with the 10-field schema.
2. Producer/consumer pairing (rf-qa → rf-qa-qualitative) documented.
3. `schema_version: 1.0.0` baseline asserted as the wire-ABI version for all future inter-agent contracts emitted by this skill.

## 1. Implementation Venue

A new standalone subsection `### A.10.6: DM-005 Phase Contract — rf-qa → rf-qa-qualitative (published row)` was inserted in `src/superclaude/skills/task-builder/SKILL.md` immediately between A.10.5 (runtime implementation site) and A.11 (next pipeline step). The location was chosen because:

- A.10.5 is the runtime consumer of the contract (spawn-prompt injection at orchestrator level).
- Future M3 implementers (FR-CONV.3 / PR-04) consult A.10.5 for wiring; the contract spec must sit adjacent.
- The subsection is **standalone** — its own `###` heading — satisfying the acceptance criterion "row is standalone (not embedded in another section)."

Heading line: `SKILL.md:1171`. Section spans 1171–1228.

## 2. The 10-Field Canonical Row (1.0.0 wire ABI)

Published as a fenced YAML block at `SKILL.md:1190–1204`:

```yaml
# DM-005 — Phase Contract: rf-qa → rf-qa-qualitative
# Frozen: M1 (T01.13 / D-0011 § DM-005)
# Published: M2 (T02.04 / D-0019)
# Consumed: M3 (FR-CONV.3 / PR-04, A.10.5 spawn-prompt injection)
producer: rf-qa
consumer: rf-qa-qualitative
artifact: Inherited Structural Verdict block
schema_version: 1.0.0
delivery_semantics: at-most-once-per-cycle
freshness_rule: INV-002-reinject-NEW
enumeration_rule: INV-010-auto-pick-TB-Add
consumer_obligation: INV-019-Self-Audit
anti_inflation: preserve-766-775-byte-stable
failure_mode: halt-A.10-before-A.10.5
```

The block is followed by a field-by-field semantics table (`SKILL.md:1206–1217`) that explains each wire value, a versioning paragraph asserting `schema_version: 1.0.0` is the M2-through-M6 baseline (`:1221`), and a cross-reference list pointing at A.10.5 (runtime), A.10 (producer side), and `rf-qa-qualitative.md` (consumer side) at `:1224–1228`.

## 3. Conformance to M1-Frozen Contract

The 10 fields and their wire values are field-for-field identical to the M1 contract-freeze published in `.dev/releases/current/task-builder-merge/roadmap.md:111` (DM-005 row) and the M2 implementation row at `roadmap.md:169` (DM-005-M2 row). One cosmetic rendering difference: the `artifact` value is rendered with spaces (`Inherited Structural Verdict block`) where the M1 freeze used hyphens; this is a markdown readability transform with zero semantic impact, and the table row at `:1212` carries the wire-ABI restatement.

## 4. Versioning Baseline

`schema_version: 1.0.0` is declared the wire ABI for the entire M2-through-M6 release window. Any field add, rename, semantic change, or value-type change requires a major version bump (`2.0.0`), a roadmap entry, and a migration note documenting the cycle in which old-version producer artifacts stop being accepted.

This versioning baseline is referenced by the roadmap entry at `roadmap.md:235`:
> `|DM-005 Phase Contract|inter-agent contract|wired-to-orchestrator-spawn-step|M3|All future inter-agent contracts (versioning baseline 1.0.0)|`

## 5. Downstream Consumer Plan

M3 (FR-CONV.3 / PR-04) consumes the published row via:
- API-002-M3 row at `roadmap.md:213` — implements orchestrator-mediated spawn-prompt injection at SKILL.md §A.10.5; cites DM-005 as dependency.
- INV-002 (freshness reinjection) — already documented in A.10.5 narrative; field `freshness_rule` in the published row formalises the contract obligation.
- INV-010 (TB-Add dynamic enumeration) — already documented in A.10.5; field `enumeration_rule` formalises.
- INV-019 (Self-Audit consumer obligation) — to be wired by rf-qa-qualitative output schema in M3; field `consumer_obligation` formalises.

## 6. Acceptance Criteria Mapping

| AC | Criterion | Verification location |
|----|-----------|-----------------------|
| AC1 | `grep -n "schema_version: 1.0.0" src/superclaude/skills/task-builder/SKILL.md` returns the DM-005 row line | `evidence.md` § 2 |
| AC2 | All 10 fields present | `evidence.md` § 3 |
| AC3 | Producer = rf-qa; Consumer = rf-qa-qualitative; explicitly named | `evidence.md` § 4 |
| AC4 | Sub-agent quality-engineer report confirms field-for-field match | `evidence.md` § 6 |
