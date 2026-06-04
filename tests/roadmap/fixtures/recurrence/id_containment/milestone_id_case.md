# Milestone-Prefixed ID Containment Recurrence Case (Contract #9, master:§Recurrence #4)

**Documented incident:** master report row #4 — Spec-fidelity / phantom-ID gate, A12:F-A12-01 TUIBBS v1-MVP. The same v1-MVP roadmap that produced the bare-D drift case (`spec_roadmap_drift_case.md`) used **milestone-prefixed deliverable IDs** of the form `M{n}-D{nn}`. The tokenizer's bare-D regex `\bD-?\d+\b` matched only the trailing `D{nn}` portion of `M1-D01`, collapsing milestone-distinct deliverables (`M1-D01`, `M2-D01`, …) under a single bare-`D` key and emitting 51 HIGH + 3 MEDIUM phantom_id/id_schema_drift false-positives. The R5 fix (PR #111 port, commit `861047c2`) adds an `MD` family to `contracts.ID_PATTERNS`, an MD-aware canonicalizer that preserves the `M{n}-` prefix, and an Explicit-non-references allowlist for the roadmap-internal bare-D sequence indices.

This fixture bundles a minimal milestone spec excerpt and the merged roadmap excerpt (with the canonical Explicit-non-references annotation) so the test drives both `build_id_registry` (from `## spec`) and `_roadmap_ids_within_spec` (from `## roadmap`). Tests slice by H2 heading. Post-fix expected outcome: **0 phantom_id / id_schema_drift findings** — milestone IDs resolve distinctly and the bare-D indices are allowlisted.

---

## spec

This is the canonical authority. It declares five milestone-prefixed deliverables across three milestones plus one FR/NFR pair.

- **FR-1** — Authentication subsystem.
- **NFR-1** — Performance budget: <100ms p99.
- **M1-D01** — Milestone 1 deliverable 1.
- **M1-D02** — Milestone 1 deliverable 2.
- **M2-D01** — Milestone 2 deliverable 1.
- **M2-D02** — Milestone 2 deliverable 2.
- **M3-D01** — Milestone 3 deliverable 1.

(The deliverable IDs are milestone-scoped: `M1-D01` and `M2-D01` are DISTINCT deliverables, not the same `D01`.)

## roadmap

This is the LLM-generated merged roadmap. It implements the spec's milestone deliverables and additionally references the bare deliverable-sequence indices as roadmap-internal annotations — the exact shape that historically tripped the bare-D phantom comparator.

| # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |
|---|----|-------|-------------|------|------|----|-----|-----|
| 1 | FR-1 | Authentication subsystem | Login + session | backend | - | unit | M | H |
| 2 | NFR-1 | Performance budget | <100ms p99 hot path | backend | FR-1 | benchmark | M | M |
| 3 | M1-D01 | Milestone 1 deliverable 1 | reference D01 as roadmap-internal index | backend | - | unit | S | H |
| 4 | M1-D02 | Milestone 1 deliverable 2 | reference D02 as roadmap-internal index | backend | - | unit | S | H |
| 5 | M2-D01 | Milestone 2 deliverable 1 | reference D03 as roadmap-internal index | backend | - | unit | S | H |
| 6 | M2-D02 | Milestone 2 deliverable 2 | reference D04 as roadmap-internal index | ops | - | integ | M | M |
| 7 | M3-D01 | Milestone 3 deliverable 1 | reference D05 as roadmap-internal index | ops | - | integ | M | M |

**Explicit non-references (do not resolve against spec):** the tokens `D01`, `D02`, `D03`, `D04`, `D05` are **roadmap-internal deliverable sequence numbers** ONLY when paired with their milestone prefix.

**Post-fix expectation:** the `MD` family resolves `M1-D01`..`M3-D01` distinctly against the spec (exact matches, no drift), and the bare-D indices `D01..D05` are exempted by the Explicit-non-references allowlist. Net: **0 phantom_id / id_schema_drift findings**. Pre-fix (no MD family, no allowlist), the milestone IDs were mis-tokenized as bare-D phantoms — the recurrence this fixture pins.
