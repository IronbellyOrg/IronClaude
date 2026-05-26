---
proposal_id: 1
persona: refactorer
model: sonnet
lens: minimal-risk transformation, simplification, leveraging existing assets
---

# Proposal 1 — Refactorer: Strangler-Fig Migration with `vite.config.ts` Extension

## Position

The right shape here is a **strangler-fig migration**: stand up vitest in parallel with the pytest-shell bridge, move tests over in batches by directory, and delete the bridge only when the last batch flips. This keeps CI green at every commit (the explicit constraint) and avoids a single high-risk PR.

## Migration shape

1. **Wave 0 — scaffolding (1 day).** Add `vitest`, `@vitest/coverage-istanbul`, `@testing-library/react`, `@testing-library/jest-dom`, `jsdom` to `frontend/package.json`. Extend `frontend/vite.config.ts` with a `test:` block via `defineConfig` (the standard merge pattern). No tests run through vitest yet.

2. **Wave 1 — bridge in CI (0.5 day).** Add `pnpm test:vitest -- --run` as a second CI step in the `frontend-tests` job. Initially it runs zero tests (empty `include` glob). This proves the runner boots and that `--reporter=junit` output is ingested by GitHub Actions correctly.

3. **Wave 2 — batch migration (5 days).** Move tests in directory-sized batches: `frontend/tests/components/atoms/` first (~80 tests, lowest dependency depth), then `molecules`, `organisms`, `hooks`, `utils`. Each batch is one PR. Per PR: update vitest `include` glob to add the batch directory, remove that directory from the pytest-shell bridge's input list, run both runners in CI for that PR, verify pass counts match, merge.

4. **Wave 3 — coverage cutover (0.5 day).** Once all 400 component tests are on vitest, switch `frontend/.nycrc.json` → `vitest --coverage.provider=istanbul --coverage.reporter=lcov`. Update `scripts/merge-coverage.py` only if the output path changes (it shouldn't — both write to `coverage/frontend/lcov.info`).

5. **Wave 4 — bridge deletion (0.5 day).** Delete `scripts/run-frontend-tests.sh`, `frontend/conftest.py`, the `pytest frontend/tests/` line from the Makefile, and the `frontend-tests-legacy` CI step. Keep `scripts/legacy-frontend-tests.sh` (renamed) frozen for 2 weeks per the seed brief's rollback plan, then delete in a follow-up cleanup.

## Why this shape

**The bridge is fake-pytest, not real pytest.** Enrichment confirmed `frontend/tests/` contains zero `def test_` and zero `@pytest` — pytest is only a *driver* here, not a *runtime*. That means the migration risk is dramatically lower than a real pytest-to-vitest port. We're not rewriting test logic; we're swapping the invocation layer.

**Extend `vite.config.ts`, don't fork.** The Vite config already declares the React plugin, path aliases, and asset handling that tests need. A separate `vitest.config.ts` would duplicate this and drift. Use `defineConfig` with the `test:` extension block — this is the documented Vitest pattern.

**Istanbul coverage provider, not v8.** The seed brief is explicit that coverage must merge with the existing LCOV pipeline. `@vitest/coverage-istanbul` produces output indistinguishable from `nyc`'s. `@vitest/coverage-v8` is faster but produces a different format that would require updating `scripts/merge-coverage.py`. Take the simplification win, not the speed win.

## Co-location decision

**Keep the centralized `frontend/tests/` tree.** Co-location (`Component.test.tsx` next to `Component.tsx`) is fashionable but the seed brief's open question is real — moving 400 files into 400 new locations *during a migration* is a separate risk surface. Defer to a follow-up: once vitest is stable, a second PR can co-locate if the team wants. Don't entangle two refactors.

## Storybook fixtures

The fixtures directory at `frontend/tests/fixtures/` is aliased by Storybook. **Don't move it.** Even if we eventually co-locate tests, fixtures stay where they are because they're cross-cutting (Storybook + tests). The Storybook alias keeps working with zero changes.

## Cost

~7 engineering days total, spread over 2 sprints if we want one batch PR per day. Single-developer-friendly; no specialized vitest experience required because the migration is mechanical.

## What I'd push back on

Any proposal that says "rewrite the tests to use vitest's native fixture API" is solving the wrong problem. These tests aren't pytest tests. They don't have pytest fixtures. The migration is the invocation layer, not the test bodies. Rewriting test bodies introduces real risk for no benefit.
