---
schema_version: "1.0"
source_seed_brief_path: ".dev/eval-workspaces/sc-brainstorm/live-runs/eval-code-migrate-pytest-vitest/seed-brief.md"
domain: code
strategy: systematic
adversarial_status: pass
convergence_score: 0.82
fit_to_intent: pass
unresolved_conflicts: []
---

# Merged Requirements — pytest → vitest migration

## Functional Requirements

1. **FR-1 — pytest characterization gate**: Before any vitest scaffolding work begins, produce a written characterization of the existing pytest suite: test count, file count, fixture catalog (with scope and autouse usage), plugin list, marker registry, parametrize patterns, async-test usage, snapshot/golden-file usage, and the current coverage baseline (line + branch).
2. **FR-2 — vitest scaffold PR**: Land a single PR that adds `package.json`, `vitest.config.ts` (or `.js`), `setupFiles`, coverage configuration (c8 or istanbul), and a trivial "hello-world" vitest test that runs in CI as an informational (non-blocking) job.
3. **FR-3 — pytest-to-vitest concept-map doc**: Commit and maintain a one-page concept-map document covering every pytest concept observed in FR-1: fixtures → `test.extend` / `beforeEach`, parametrize → `test.each`, markers → describe filters or vitest config, conftest hooks → `setupFiles`, plus worked examples for each pattern actually in use. This doc stays in-repo permanently as the reference for future test authors.
4. **FR-4 — Per-suite migration PRs**: Migrate suites in dependency order (leaf-most modules first), one suite per PR. Each PR has both pytest and vitest green. Target PR size: ≤ 500 LOC of test diff per PR.
5. **FR-5 — Vitest gate flip**: Once vitest covers ≥ pytest baseline (test count parity AND coverage parity per FR-1 / NFR-2), flip the vitest CI job from informational to blocking.
6. **FR-6 — Config-only cutover PR**: The cutover PR is a single config-only PR that (a) removes the pytest CI job, (b) removes pytest config files, (c) removes pytest plugin invocations. It MUST be revertible cleanly in a single revert.
7. **FR-7 — Dep-prune PR**: A post-cutover PR removes `pytest`, `pytest-cov`, and all `pytest-*` plugin entries from `pyproject.toml` (or the dependency manifest in use), within one release of the cutover PR.

## Non-Functional Requirements

- **NFR-1 — CI green continuously**: CI MUST remain green throughout the migration window. No extended red period. A migration PR is blocked if it would red the gate.
- **NFR-2 — Coverage non-regression**: Coverage MUST NOT regress at any point. Every PR runs a coverage-delta check against the pytest baseline (FR-1). Line-coverage is the comparable metric across pytest-cov and c8/istanbul; branch-coverage is tracked but not regression-gated until both runners report it consistently.
- **NFR-3 — Bounded parallel-run window**: The parallel-run window has an explicit calendar end-date target AND a single named owner accountable for the cutover decision. End-date is set at FR-2 scaffolding time and tracked in the concept-map doc (FR-3).
- **NFR-4 — Migration visibility**: A tracking section in the concept-map doc lists migrated suites, remaining suites, and updates per PR. This is the public progress signal.
- **NFR-5 — Revertibility**: Each migration PR is independently revertible. The cutover PR (FR-6) is config-only and revertible without code changes.
- **NFR-6 — Rollback plan**: If vitest blocks a release within one week of cutover, the cutover PR is reverted and pytest is re-enabled as the gate. This rollback path is exercised at least once in a non-prod CI environment before cutover.

## Acceptance Criteria

- **AC-1**: Every pytest test is either (a) migrated to vitest with equivalent assertions, or (b) explicitly retired with a written rationale in the concept-map doc.
- **AC-2**: vitest coverage (line) ≥ pytest baseline coverage at cutover, verified by automated check.
- **AC-3**: pytest config, plugins, and CI job are removed in the cutover PR (FR-6); CI remains green after merge.
- **AC-4**: pytest dependencies removed from manifest within one release cycle of cutover (FR-7).
- **AC-5**: Concept-map doc (FR-3) covers every pytest concept actually used in the FR-1 characterization — no unmapped concepts at cutover.
- **AC-6**: Rollback rehearsal (NFR-6) executed and documented before the cutover PR merges.

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Parallel-run window stretches indefinitely. | Medium | NFR-3: explicit end-date target and a single accountable owner; vitest gate flip (FR-5) is the forcing function. |
| pytest plugin behavior has no vitest equivalent (e.g., pytest-xdist sharding, pytest-bdd, certain pytest-asyncio specifics). | Medium | FR-1 characterization gates discovery. For unmappable plugins: written deprecation decision (with rationale) in the concept-map doc OR a vitest shim — never silently drop coverage. |
| Coverage metrics drift between pytest-cov and c8/istanbul. | Medium | NFR-2: normalize on line-coverage; branch-coverage tracked but not regression-gated until both runners report it consistently. |
| The underlying code under test is still Python, making the migration meaningless. | High (open) | FR-1 explicitly checks the language stack of the system under test before scaffolding work proceeds (OQ-1). |
| Review velocity bottlenecks the per-PR migration cadence. | Low-Medium | Designate two reviewers familiar with both pytest and vitest semantics at FR-2 time. |
| pytest dep-prune (FR-7) is forgotten after cutover. | Low | Cutover PR description includes a follow-up checklist that creates the dep-prune issue automatically. |

## Open Questions

- **OQ-1**: Is the underlying code under test already JS/TS, or is the language migration concurrent with the test migration? If the code is still Python, this brainstorm is premature.
- **OQ-2**: What is the size of the current pytest suite (test count, file count, fixture complexity)? This sizes the migration calendar and the parallel-run cost.
- **OQ-3**: Are there pytest plugins in use that have no clean vitest equivalent? (Surfaced by FR-1 characterization; answer required before FR-2 scaffolding.)
- **OQ-4**: What is the team's appetite for parallel-run duration vs. hard cutover? The merged plan defaults to parallel-run but allows the calendar end-date target (NFR-3) to compress it toward hard cutover.
- **OQ-5**: Is there an explicit deadline or release boundary driving this migration?
- **OQ-6**: What is explicitly out of scope (e.g., E2E tests, snapshot strategy, contract tests)? Not captured in the non-interactive seed brief.

## Provenance

- **FR-1** (pytest characterization gate): Variant 1 (architect) §Functional Requirements item 1 + Variant 2 (refactorer) §Functional Requirements item 1. Anchors honored: `pytest characterization required` (seed-brief `must_preserve`).
- **FR-2** (vitest scaffold PR): Variant 2 (refactorer) §Functional Requirements item 2. Anchors honored: `vitest as explicit target` (seed-brief `must_preserve`).
- **FR-3** (concept-map doc): Variant 2 (refactorer) §Functional Requirements item 3 — unique-to-Variant-2, augmented onto base.
- **FR-4** (per-suite migration PRs): Variant 1 (architect) §Functional Requirements item 4 — base proposal.
- **FR-5** (vitest gate flip): Variant 1 (architect) §Functional Requirements item 5.
- **FR-6** (config-only cutover PR): Variant 2 (refactorer) §Functional Requirements item 5, refined onto base.
- **FR-7** (dep-prune PR): Variant 2 (refactorer) §Functional Requirements item 6.
- **NFR-1** (CI green continuously): both variants §Non-Functional Requirements — shared assumption.
- **NFR-2** (coverage non-regression): both variants — shared assumption. Anchor: `migration must not silently drop coverage or invariants` (seed-brief `must_preserve`).
- **NFR-3** (bounded parallel-run window): Variant 1 risk-mitigation + Variant 2 calendar discipline merged.
- **NFR-4** (migration visibility): Variant 1 §Non-Functional Requirements item 3 + Variant 2 §Functional Requirements item 4.
- **NFR-5** (revertibility): Variant 2 §Non-Functional Requirements item 2.
- **NFR-6** (rollback plan): Variant 1 §Risks mitigation, refined with Variant 2's revertibility framing.
- **AC-1 through AC-6**: Synthesis of both variants' Acceptance Criteria sections.
- **Risks**: Union of both variants' risk lists, deduplicated.
- **OQ-1 through OQ-3**: Both variants surfaced these (shared open questions).
- **OQ-4**: Captured from the cadence-policy divergence between the two variants.
- **OQ-5, OQ-6**: Carried verbatim from seed-brief.md `## Open Questions` (non-interactive seed could not resolve these).

### Dropped Anchors

None. All seed-brief `must_preserve` items appear in the merged output.

### Out-of-Scope Promotions

None. The seed-brief `out_of_scope` list was empty (non-interactive quick run); nothing was promoted.

### Fit-to-Intent Issues

(none — see Wave 3 step 6 gate; all `pass` criteria met)
