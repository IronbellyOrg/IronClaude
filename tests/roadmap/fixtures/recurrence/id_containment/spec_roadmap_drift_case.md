# Spec-Roadmap ID Drift Recurrence Case (Contract #9, master:§Recurrence #4)

**Documented incident:** master report row #4 — Spec-fidelity LLM-only / phantom-ID gate, A12:F-A12-01 TUIBBS v1-MVP. The spec declared a small set of D-family deviations (`D1, D3, D5`); the roadmap referenced a much larger renumbered set (`D01..D54` reduced here to `D-1, D-2, D-3, D-7, D-99` for the minimal reproducer). The historical strict comparator produced 54 `phantom_id` HIGH findings. Contract #9 prevents this by asserting `roadmap_ids ⊆ spec_ids ∪ accepted_deviations` BEFORE any LLM-judged severity step.

This fixture is a single document that bundles a minimal "spec excerpt" and a "merged roadmap excerpt" so the test can drive both `build_id_registry` (from the spec excerpt) and `_roadmap_ids_within_spec` (from the roadmap excerpt) without needing two files. Tests slice by H2 heading.

---

## spec

This is the canonical authority. It declares three D-family deviations and one FR/NFR pair.

- **FR-1** — Authentication subsystem.
- **NFR-1** — Performance budget: <100ms p99.
- **D1** — Accept legacy session token format until v2 cutover.
- **D3** — Skip telemetry collection for embedded-mode users.
- **D5** — Defer audit-log retention policy to operations team.

(Intentionally minimal — no additional FR/NFR/D-family identifiers appear in this section. The roadmap below introduces phantom variant surface forms the historical pipeline failed to reject.)

## roadmap

This is the LLM-generated merged roadmap. It references the spec's known IDs **plus** fabricated phantom IDs that the historical pipeline only caught post-hoc.

| # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |
|---|----|-------|-------------|------|------|----|-----|-----|
| 1 | FR-1 | Authentication subsystem | Login + session | backend | - | unit | M | H |
| 2 | NFR-1 | Performance budget | <100ms p99 hot path | backend | FR-1 | benchmark | M | M |
| 3 | D-1 | Legacy session token | Accept old format (variant ID) | backend | FR-1 | integ | S | L |
| 4 | D-2 | **PHANTOM** — never declared in spec | Fabricated by generator | backend | - | - | S | L |
| 5 | D-3 | Skip embedded telemetry | Variant ID for D3 | backend | - | unit | S | L |
| 6 | D-7 | **PHANTOM** — never declared in spec | Fabricated by generator | ops | - | - | M | L |
| 7 | FR-99 | **PHANTOM** — never declared in spec | Fabricated by generator | backend | - | - | L | L |
| 8 | D-99 | **PHANTOM** — never declared in spec | Fabricated by generator | ops | - | - | XL | L |

**Phantom IDs in this roadmap:** `D-2`, `D-7`, `D-99`, `FR-99` — four IDs not in the spec.
**Note on D-family canonicalization:** the spec writes `D1, D3, D5` (no hyphen); the roadmap writes `D-1, D-3` (with hyphen). The current `_REQUIREMENT_PATTERNS["D"]` regex `\bD-?\d+\b` is lenient and matches both forms, so `D-1` and `D1` are both extracted as the **literal surface form** they appear in. Per Contract #9, the comparison is exact-string set-containment — `D-1` (from the roadmap) is NOT equal to `D1` (from the spec), and so `D-1` is reported as a phantom UNLESS canonicalization is in scope. R0.1 does NOT canonicalize (that is master:§Flaw 4 and a later phase); R0.1 enforces literal set containment.

So the **actual** post-fix violation set this fixture produces against an R0.1-canonical registry is: `{"D-1", "D-2", "D-3", "D-7", "D-99", "FR-99"}` — six surface-form phantoms. The expected.json captures this exactly.
