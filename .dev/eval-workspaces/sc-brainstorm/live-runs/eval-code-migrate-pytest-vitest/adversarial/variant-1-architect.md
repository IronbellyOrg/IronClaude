---
variant_id: 1
persona: architect
model: opus
generated: 2026-05-27
---

# Variant 1 — Architect: Parallel-Run Migration Strategy

## Strategy Summary

Run both pytest and vitest in CI side-by-side until a defined parity gate is hit, then retire pytest. This preserves the green CI signal at all times and lets the team migrate suite-by-suite without a "big bang" rewrite.

## Functional Requirements

1. Establish a pytest characterization baseline: full test inventory (count, names, fixtures used, plugins required, markers, parametrize sets), coverage report, and runtime profile captured before migration starts.
2. Stand up vitest in the repo as a separate CI job; vitest job is non-blocking initially (informational only).
3. Define a pytest → vitest concept map: fixtures → `test.extend` / `beforeEach`, parametrize → `test.each`, markers → describe/test filters or vitest config, conftest hooks → `setupFiles`.
4. Migrate suites in dependency order (leaf-most modules first), one suite per PR, with both pytest and vitest passing.
5. Flip the vitest job to blocking only once it covers ≥ pytest baseline (test count parity + coverage parity).
6. Retire pytest job and remove pytest config/plugins in a final PR once vitest has been the canonical gate for at least one release cycle.

## Non-Functional Requirements

- CI MUST remain green throughout the migration window (no extended red period).
- Coverage MUST NOT regress at any point; a coverage delta check runs on every PR.
- Migration cadence MUST be visible: a tracking doc lists migrated/remaining suites and updates per PR.
- Two-runner cost is bounded: parallel-run window has an explicit end-state and end-date target.

## Acceptance Criteria

- Every pytest test is either (a) migrated to vitest with equivalent assertions, or (b) explicitly retired with a written rationale.
- vitest coverage ≥ pytest baseline coverage at cutover.
- pytest config, plugins, and CI job are removed in the final PR; CI still green after removal.
- One release cycle has passed with vitest as the sole canonical gate.

## Risks

- Risk: parallel-run window stretches indefinitely. Mitigation: explicit end-date and a single owner accountable for the cutover decision.
- Risk: pytest plugin behavior has no vitest equivalent (e.g., pytest-xdist sharding semantics, pytest-bdd). Mitigation: characterize plugin usage upfront; for unmappable plugins, capture a written deprecation decision in the seed brief.
- Risk: coverage tools differ (pytest-cov vs c8/istanbul) and metric definitions drift. Mitigation: normalize on line-coverage as the comparable metric; allow branch-coverage as additive but not regression-gated until both runners report it the same way.

## Open Questions

- Is the underlying code already JS/TS? If not, this migration is a no-op or premature.
- What is the suite size and parallel-run cost ceiling the team will tolerate?

## Provenance (Variant-Local)

- Anchors honored: pytest characterization, vitest target, test-suite-as-unit, coverage non-regression.
- Out-of-scope: respected — no items promoted.
