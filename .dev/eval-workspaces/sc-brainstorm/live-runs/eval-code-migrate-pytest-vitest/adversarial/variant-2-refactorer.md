---
variant_id: 2
persona: refactorer
model: sonnet
generated: 2026-05-27
---

# Variant 2 — Refactorer: Hard-Cutover Migration Strategy

## Strategy Summary

Treat the migration as a focused, time-boxed refactor: characterize pytest, produce a one-PR vitest scaffold + concept map, mechanically translate suites in a short series of PRs, cut over in a single release. Avoid prolonged dual-runner debt.

## Functional Requirements

1. Pytest characterization: enumerate test count, file count, fixture catalog, plugin list, marker registry, parametrize catalog, async-test usage, snapshot/golden-file usage, coverage baseline.
2. One scaffolding PR adds vitest config, `package.json`, `setupFiles`, coverage config, and a "hello-world" vitest test that runs in CI as informational.
3. A concept-map doc (one page) commits at the same time: pytest concept → vitest equivalent, with examples for each fixture/marker/parametrize pattern actually in use.
4. Translate suites in batches sized to "one reviewable PR" (target: ≤ 500 LOC test diff per PR). Each PR: pytest tests deleted, vitest tests added, coverage report attached, parity asserted in PR description.
5. The cutover PR flips the CI gate to vitest, removes pytest config/plugins, removes pytest job. This PR is intentionally small (config-only).
6. A post-cutover PR removes any pytest-cov/pytest-* dependencies from `pyproject.toml` or equivalent.

## Non-Functional Requirements

- Total migration calendar time is bounded (target: ≤ 4 weeks for a typical mid-size suite).
- Each migration PR is independently revertible — no inter-PR dependencies that break revert.
- Coverage is reported on every PR; PR is blocked if coverage delta < 0 vs baseline.
- The concept-map doc stays in-repo as a permanent reference for future test authors.

## Acceptance Criteria

- pytest characterization doc exists and is accurate (spot-checked against actual fixtures/markers in use).
- Concept-map doc covers every pytest concept used in the actual suite (no unmapped concepts at cutover).
- Every translated suite has equivalent or improved coverage in vitest.
- Cutover PR is single-commit, config-only, and reverts cleanly if vitest blocks a release within the first week.
- All pytest dependencies removed within one release of cutover.

## Risks

- Risk: hard cutover hits a long-tail of pytest plugin behaviors with no vitest equivalent, forcing a stall. Mitigation: characterization is gated — if unmapped plugins are found, escalate to architect for a deferral decision before scaffolding starts.
- Risk: review velocity bottlenecks the PR cadence. Mitigation: designate two reviewers familiar with both pytest and vitest semantics upfront.
- Risk: the underlying code under test is still Python — migration is then meaningless. Mitigation: characterization step explicitly checks the language stack of the system under test before proceeding.

## Open Questions

- What is the team's appetite for a hard cutover vs. extended parallel run?
- Are there pytest fixtures whose semantics (autouse scope, fixture finalization order) have no clean vitest equivalent?

## Provenance (Variant-Local)

- Anchors honored: pytest characterization, vitest target, test-suite-as-unit, coverage non-regression, parallel-run-must-have-end-state (satisfied by hard cutover).
- Out-of-scope: respected — no items promoted.
