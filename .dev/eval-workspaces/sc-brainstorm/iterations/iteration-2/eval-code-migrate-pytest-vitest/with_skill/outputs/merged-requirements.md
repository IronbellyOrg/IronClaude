---
spec_type: requirements
domain: code
strategy: systematic
adversarial_status: pass
convergence_score: 0.84
proposal_count: 2
source_proposals: [proposal-1-refactorer, proposal-2-qa]
debate_transcript: ./adversarial/debate-transcript.md
source_seed: ./seed-brief.md
agents: "sonnet:refactorer:'focus on minimal-risk transformation and existing-asset reuse',haiku:qa:'focus on equivalence gates, drift detection, and regression risk'"
---

# Merged Requirements: pytest → vitest Migration (Frontend Slice)

## Problem Statement

The frontend test slice (~400 React+TS component tests under `frontend/tests/`) is invoked through a pytest-shell-playwright bridge (`scripts/run-frontend-tests.sh` + `frontend/conftest.py`) that runs ~9 minutes on CI (6× a native runner's expected time), blocks JS-native dev affordances (Vitest UI, watch mode, in-IDE debugging), and produces coverage in a format requiring a custom merge step. Migrate this slice to Vitest while keeping CI green at every commit, preserving the combined coverage report, and not breaking Storybook's resolution of shared fixtures.

## Constraints

- **C1** — CI must stay green at every commit during migration (no big-bang). *(seed Q3)*
- **C2** — Combined LCOV coverage report must continue to merge cleanly via `scripts/merge-coverage.py`. *(seed Q3)*
- **C3** — `frontend/tests/fixtures/` must remain importable from Storybook stories. *(seed Q3, enrichment)*
- **C4** — Frontend CI wall-clock target ≤ 2 minutes p95 (down from ~9 min). *(seed Q4)*
- **C5** — Playwright integration tests (`frontend/tests/integration/*.spec.ts`) are out of scope; they continue under `@playwright/test`. *(enrichment)*
- **C6** — Bridge deletion is gated on equivalence-checker green ≥5 consecutive CI runs over ≥10 calendar days. *(debate Tension 1, QA win)*

## Functional Requirements

- **FR1** — Add `vitest`, `@vitest/coverage-istanbul`, `@testing-library/react`, `@testing-library/jest-dom`, and `jsdom` to `frontend/package.json`. Configure vitest via `defineConfig` extension of the existing `frontend/vite.config.ts` (no separate `vitest.config.ts`). *(refactorer Wave 0; debate Tension 2 consensus)*
- **FR2** — Migrate component tests in directory-sized batches in this order: `atoms` → `molecules` → `organisms` → `hooks` → `utils`. Each batch is one PR; each PR updates the vitest `include` glob and removes the batch directory from the pytest-shell bridge's input. *(refactorer Wave 2)*
- **FR3** — Per-batch equivalence gate: vitest test count for the migrated directory must equal the pytest-shell baseline count (±0 tests). PR is blocked if not. *(QA AC-Q1; debate Tension 1)*
- **FR4** — Coverage provider is `@vitest/coverage-istanbul` (NOT `v8`), producing LCOV at `coverage/frontend/lcov.info` — same path/format as today's `nyc` output. *(refactorer + QA consensus; debate Tension 2)*
- **FR5** — During the first month post-cutover, vitest CI runs use `--isolate` to match Jest's per-file isolation semantics. After the month, the team evaluates disabling for the speed win. *(QA failure mode 3; debate Tension 3)*
- **FR6** — Pre-migration Wave-0 check: grep for `toMatchSnapshot` usage. If non-zero, capture a snapshot baseline before any batch flips; equivalence then includes snapshot-file diff = empty. If zero, the snapshot AC is dropped. *(debate Tension 5)*
- **FR7** — Bridge deletion (Wave 4) removes `scripts/run-frontend-tests.sh`, `frontend/conftest.py`, the `pytest frontend/tests/` line from the `Makefile`, and the legacy CI step. The wrapper is *renamed* to `scripts/legacy-frontend-tests.sh` and retained frozen for 2 weeks per the rollback plan, then deleted. *(refactorer Wave 4 + seed brief Q5)*

## Non-Functional Requirements

- **NFR1** — Frontend CI job wall-clock p95 < 2 minutes over 20 consecutive runs post-cutover. *(C4, QA AC-Q3)*
- **NFR2** — Coverage parity: post-cutover combined LCOV total-line-coverage is within −1% of the pre-cutover baseline. Any single file dropping >5% line coverage gets an issue filed. *(QA AC-Q2)*
- **NFR3** — Storybook build succeeds post-cutover (proves fixtures alias still resolves). *(C3, QA AC-Q6)*
- **NFR4** — Test isolation: with `--isolate` enabled, zero pre-existing tests change pass/fail status vs. the pytest-shell baseline. *(FR5, QA failure mode 3)*

## Acceptance Criteria

- **AC1** — All 400 component tests run via `pnpm test` (vitest) with exit 0 and ≥99% pass-rate match against the pytest-shell baseline; the ≤1% delta (if any) is documented per-test as a known flake or assertion-semantic diff. *(seed brief success criteria; QA AC-Q1)*
- **AC2** — `scripts/merge-coverage.py` produces a single combined LCOV with no schema changes required to the merge script. *(C2)*
- **AC3** — Equivalence-checker (`scripts/compare-test-counts.sh`, new ~20 LOC) is green for ≥5 consecutive CI runs over ≥10 calendar days before `Wave 4` deletes the bridge. *(C6, QA AC-Q4)*
- **AC4** — Coverage-diff script (`scripts/coverage-diff.py`, new ~30 LOC) reports total-line-coverage delta within −1% and no single file dropping >5%. *(NFR2)*
- **AC5** — Frontend CI p95 wall-clock < 2 min over 20 runs post-cutover. Pre-cutover baseline (20 runs) captured and stored for comparison. *(NFR1, QA AC-Q3)*
- **AC6** — Storybook smoke build succeeds in a post-cutover CI step. *(NFR3)*

## Risks

- **R1** (severity: MEDIUM) — **Assertion-semantic diffs.** `expect(x).toBe(y)` semantics differ at edge cases (NaN, Symbol, deep equality on Maps) between Jest and vitest. *Mitigation*: each batch PR's template enumerates any test that changed assertion shape; equivalence checker catches count diffs but not subtle pass→pass-with-different-reason shifts. Budget +2 days for the `hooks/` batch (most deep-equality usage). *(QA risk R-Q1)*
- **R2** (severity: MEDIUM) — **Premature bridge deletion.** If Wave 4 fires before the 5-consecutive-green gate, a silent test-skip regression could ship. *Mitigation*: gate is encoded in `scripts/compare-test-counts.sh` failing the CI step; PR description template requires linking the last 5 runs. *(QA risk R-Q2; debate Tension 1)*
- **R3** (severity: LOW) — **Co-location creep.** Mid-migration, someone proposes co-locating tests next to source files. *Mitigation*: scope is explicit in this spec — co-location is a separate follow-up, not part of this work. Refused at PR-review time. *(refactorer position; carried as OQ1)*
- **R4** (severity: LOW) — **Coverage-provider drift.** If a future PR swaps `istanbul` → `v8` for the speed win, instrumentation differences (~1-2% on arrow functions / computed properties) will surface as a coverage cliff. *Mitigation*: documented in this spec; any future provider swap is its own change with its own equivalence gate. *(QA risk R-Q3)*

## Open Questions

- **OQ1** — Test co-location (`Component.test.tsx` next to `Component.tsx`) vs. centralized `frontend/tests/` tree. Deferred to a follow-up after vitest is stable. *(seed Q open + debate Tension 4)*
- **OQ2** — Long-term coverage provider: stay on `istanbul`, or migrate to `v8` once accuracy delta is characterized? Decision deferred ≥1 month post-cutover. *(R4)*
- **OQ3** — Should the integration-test slice (Playwright, currently out of scope) eventually run inside vitest via `@vitest/browser`? Out of scope here; flagged for future architecture discussion.

## Provenance

| Requirement | Origin |
|---|---|
| FR1 (vite.config extension) | Refactorer Wave 0; debate Tension 2 consensus |
| FR2 (batch order) | Refactorer Wave 2 |
| FR3 (per-batch equivalence) | QA AC-Q1; debate Tension 1 |
| FR4 (istanbul provider) | Refactorer + QA consensus |
| FR5 (--isolate for first month) | QA failure mode 3; debate Tension 3 |
| FR6 (snapshot precheck) | Debate Tension 5, QA addition |
| FR7 (bridge deletion sequence) | Refactorer Wave 4 + seed brief Q5 |
| NFR1 (CI wall-clock) | Seed brief Q4 (firm); QA AC-Q3 |
| NFR2 (coverage parity) | QA AC-Q2 |
| NFR3 (Storybook smoke) | Seed brief Q3; QA AC-Q6 |
| NFR4 (isolation parity) | QA failure mode 3 |
| AC1 (vitest exit 0 + pass-rate) | Seed brief success criteria |
| AC2 (LCOV merge) | C2; refactorer Wave 3 |
| AC3 (5-run gate) | QA AC-Q4; debate Tension 1 |
| AC4 (coverage diff) | QA AC-Q2 |
| AC5 (wall-clock baseline + p95) | QA AC-Q3 |
| AC6 (Storybook smoke) | QA AC-Q6 |
| R1 (assertion-semantic diffs) | QA failure mode 2 + risk R-Q1 |
| R2 (premature deletion) | Debate Tension 1 resolution |
| R3 (co-location creep) | Refactorer scope discipline |
| R4 (provider drift) | QA risk R-Q3 |
| OQ1 (co-location) | Carried from seed brief |
| OQ2 (long-term provider) | New, from R4 |
| OQ3 (Playwright in vitest) | New, scope-fencing |
