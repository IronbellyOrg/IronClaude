# Phantom-ID High-Severity Spec-Fidelity Recurrence Case (master:§Recurrence #1)

**Documented incident:** master report row #1 — *Spec-fidelity LLM-only / non-deterministic / phantom-ID gate (high_severity_count binary halt; LLM-judged severity; no programmatic spec↔roadmap ID cross-ref)*. Partition findings `A4:F-A4-005` (5 spec-fidelity runs on identical input produced 3H/9M/5L → 3H/8M/5L → 1H/6M/3L → 3H/8M/4L → 0H/7M/3L) and `A12:F-A12-01` (TUIBBS v1-MVP: 54 `phantom_id` HIGH findings from the `\bD-?\d+\b` lenient extractor vs strict comparator).

The pre-fix failure shape: the spec-fidelity gate sent the roadmap to an LLM that emitted a non-deterministic `high_severity_count`. Phantom IDs (roadmap IDs never declared in the spec) were the dominant driver of HIGH findings, but the binary `high_severity_count == 0` halt could not distinguish "structurally fabricated ID" from "LLM mood swing." Contract #4/#9 replaces the LLM-judged severity step with a deterministic, programmatic `roadmap_ids ⊆ spec_ids ∪ accepted_deviations` set-containment check (`_roadmap_ids_within_spec` against the `SpecIdRegistry` sidecar) that runs BEFORE any severity classification — so a phantom-ID roadmap fails deterministically and identically on every run.

This fixture bundles a minimal "spec excerpt" (H2 `## spec`) and an LLM-generated "roadmap excerpt" (H2 `## roadmap`) in a single document; the test slices by heading, builds the `SpecIdRegistry` from `## spec`, and runs `_roadmap_ids_within_spec` against `## roadmap`. The phantom IDs here reproduce the A12 driver: the roadmap fabricates FR/NFR/SC IDs absent from the spec, which historically inflated the HIGH count.

---

## spec

Canonical authority. Declares two FR, one NFR, one SC, one G, and two D-family deviations.

- **FR-1** — Account onboarding flow.
- **FR-2** — Session lifecycle management.
- **NFR-1** — p99 latency budget < 150ms.
- **SC-1** — 95% of onboarding completes in < 3 steps.
- **G-1** — Reduce support tickets by 20%.
- **D1** — Defer SSO integration to v2.
- **D3** — Accept third-party analytics opt-out gap until legal review.

(Intentionally minimal — only the five identifiers above are declared; no higher-numbered FR/NFR/SC identifiers and no further D-family deviations appear in this section.)

## roadmap

LLM-generated merged roadmap. References the spec's known IDs **plus** fabricated phantom IDs that the historical LLM-judged gate flagged as HIGH post-hoc.

| # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |
|---|----|-------|-------------|------|------|----|-----|-----|
| 1 | FR-1 | Account onboarding | Signup + verify | backend | - | unit | M | H |
| 2 | FR-2 | Session lifecycle | Token issue/refresh | backend | FR-1 | unit | M | H |
| 3 | NFR-1 | Latency budget | p99 < 150ms | backend | FR-2 | benchmark | M | M |
| 4 | SC-1 | Onboarding success | 95% in <3 steps | product | FR-1 | metric | S | M |
| 5 | G-1 | Support reduction | -20% tickets | product | - | metric | S | L |
| 6 | FR-3 | **PHANTOM** — never declared in spec | Fabricated by generator | backend | - | - | M | L |
| 7 | NFR-2 | **PHANTOM** — never declared in spec | Fabricated by generator | backend | - | - | M | L |
| 8 | SC-2 | **PHANTOM** — never declared in spec | Fabricated by generator | product | - | - | S | L |
| 9 | D-1 | Defer SSO | Hyphenated variant of spec D1 | backend | - | integ | S | L |
| 10 | D5 | **PHANTOM** — never declared in spec | Fabricated by generator | ops | - | - | M | L |

**Phantom IDs in this roadmap (vs the literal R0.1 set-containment registry):** `FR-3`, `NFR-2`, `SC-2`, `D-1`, `D5` — five IDs not in `spec_ids ∪ accepted_deviations`.

**Note on D-family canonicalization (same as `id_containment/spec_roadmap_drift_case`):** the spec writes `D1, D3` (no hyphen); the roadmap writes `D-1` (with hyphen). The R0.1 comparator is literal exact-string set-containment and does NOT canonicalize, so `D-1` ≠ `D1` and `D-1` is reported as a phantom. The `.expected.json` captures the exact literal violation set the live `_roadmap_ids_within_spec` produces.
