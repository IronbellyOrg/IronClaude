---
topic: "migrate test suite from pytest to vitest"
domain: code
strategy: systematic
depth: quick
proposal_count: 2
handoff_target: none
created: 2026-05-25T00:00:00Z
---

# Seed Brief: migrate-pytest-to-vitest

## Socratic Dialogue Record

QUICK tier triggers the Clarify batch only — 5 questions targeted at scope and blocking constraints.

### Clarify batch

**Q1. What's the entry point — is the whole suite moving, or just a slice?**
A: A slice. We have ~1,200 pytest tests today. The Python backend tests (~800) stay on pytest. The ~400 tests under `frontend/tests/` (React + TS components, currently driven by pytest+playwright through a shell wrapper) are what's moving to vitest. Goal: get the frontend test runner native to the frontend stack.

**Q2. What's the failure mode you're trying to fix?**
A: Three pains: (a) the pytest-shell-playwright bridge is slow (~9 minutes for the frontend slice, vs ~90s expected from a native runner); (b) JS engineers can't use Vitest UI / watch mode; (c) coverage from the frontend slice doesn't merge with the backend coverage report cleanly because the formats differ.

**Q3. Any non-negotiable constraints from existing code?**
A: Yes. (i) CI must stay green at every commit — no big-bang cutover. (ii) Coverage reporting (currently combined via `coverage.py` + `nyc` merge) must stay merged in the final report. (iii) The shared mocks/fixtures in `frontend/tests/fixtures/` are used by both Storybook stories and tests; if we move them, Storybook must still resolve them.

**Q4. What does "done" look like?**
A: (i) Zero pytest invocations against `frontend/tests/`. (ii) `pnpm test` runs vitest, exits 0, and produces a coverage report that merges with the Python report. (iii) Frontend test wall-clock under 2 minutes on CI. (iv) Old shell wrapper deleted.

**Q5. What's the rollback if this misbehaves?**
A: Keep the pytest-shell wrapper in `scripts/legacy-frontend-tests.sh` for ~2 weeks post-cutover. If vitest produces a false-pass that pytest would have caught, revert to running both for one CI run, diagnose, then re-cut. After 2 weeks, delete the wrapper.

## Problem Statement

The frontend test slice (~400 React+TS tests) currently runs through a pytest-shell-playwright bridge that is 6× slower than a native runner would be, blocks JS-native dev affordances (Vitest UI, watch mode, in-IDE debugging), and produces a coverage format that requires extra merging steps. Migrate this slice to Vitest while keeping CI green throughout, preserving merged coverage reporting, and not breaking Storybook's resolution of shared fixtures.

## Known Context

- Frontend stack: React 19 + TypeScript 5.6, Vite 5.4, pnpm workspaces.
- ~400 tests under `frontend/tests/` — mostly component tests via Testing Library, ~30 integration tests that drive Playwright.
- Existing runner: `pytest frontend/tests/` invokes `scripts/run-frontend-tests.sh` which shells out to a Node child process. Slow (~9 min CI).
- Shared fixtures at `frontend/tests/fixtures/` used by both tests and `frontend/stories/` (Storybook 8).
- Coverage: `coverage.py` (backend) + `nyc` JSON output (frontend) merged via `scripts/merge-coverage.py` into a single LCOV.
- CI: GitHub Actions, ubuntu-latest, single job per stack (backend + frontend split).
- Playwright tests (~30) — out of scope for this migration; they stay on `@playwright/test`. Migration is component-tests only.

## Constraints

- No big-bang: CI must stay green at every commit during the migration.
- Coverage merge into the existing LCOV must keep working (frontend half can change format if `merge-coverage.py` is updated correspondingly).
- Shared fixtures in `frontend/tests/fixtures/` must remain importable from Storybook stories.
- Frontend test wall-clock target: < 2 minutes on CI (down from ~9 min).
- Soft deadline: end of next sprint (2 weeks).

## Success Criteria

- `pnpm test` runs vitest against `frontend/tests/` with exit 0, ≥99% test pass rate match against the pytest-shell baseline (allowing for ≤1% known flakes documented separately).
- Combined coverage report still merges cleanly (single LCOV out of `scripts/merge-coverage.py`).
- CI wall-clock for frontend job ≤ 2 minutes p95.
- Storybook still resolves shared fixtures.
- `scripts/run-frontend-tests.sh` and the `pytest frontend/` invocation are deleted from `Makefile` and CI workflows.

## Open Questions

- Vitest config style: `vitest.config.ts` standalone, or via `defineConfig` extending the existing `vite.config.ts`?
- Coverage provider: `v8` (faster, less accurate) vs `istanbul` (slower, matches current `nyc` output format)?
- Do we co-locate tests next to source files (`Component.test.tsx`) or keep the centralized `frontend/tests/` tree?

## Enrichment Context

Codebase enrichment ran in degraded mode (`fallback_2`, native Glob/Grep). Full output at `enrichment/codebase-context.md`. Key signals folded in:

- `frontend/tests/fixtures/` is dual-used (tests + Storybook); migration must preserve resolution path.
- `scripts/merge-coverage.py` expects LCOV from frontend; `nyc` produces this today, `vitest --coverage.reporter=lcov` produces equivalent output.
- No reliance on pytest-specific features (parametrize, fixtures, conftest) in the frontend slice — confirmed via grep that the tests are JS files run *through* pytest, not pytest tests.

Confidence on enrichment: medium-high. The "no pytest fixtures in frontend tests" finding is the load-bearing one — confirmed by static scan but a semantic pass would tighten it.
