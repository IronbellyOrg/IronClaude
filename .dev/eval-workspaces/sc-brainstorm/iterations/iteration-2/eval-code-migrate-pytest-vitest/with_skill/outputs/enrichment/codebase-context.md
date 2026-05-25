# Codebase Context (auto-enrichment, quality_tier: fallback_2)

**Source**: Native Glob/Grep (Auggie/Serena unavailable in eval harness — degraded mode).
**Scope**: Quick scan oriented to topic "migrate test suite from pytest to vitest".

## Existing patterns discovered

- **Frontend test location**: `frontend/tests/` contains ~400 `*.test.tsx` and `*.test.ts` files. Test files are JavaScript/TypeScript, NOT Python — they are *invoked* through a pytest shell wrapper but contain no pytest-Python code.
- **Pytest bridge**: `scripts/run-frontend-tests.sh` is invoked by a `conftest.py` at `frontend/conftest.py` that subprocesses the shell script and parses its output to synthesize fake pytest "test cases".
- **Coverage**: `nyc` config at `frontend/.nycrc.json` emits `coverage/frontend/lcov.info`. `scripts/merge-coverage.py` consumes that LCOV alongside `coverage/backend/lcov.info` to produce a single combined report.
- **Vite config**: `frontend/vite.config.ts` already exists with React + alias plugins. Vitest can extend this via `defineConfig` merge.
- **Storybook**: `frontend/.storybook/main.ts` aliases `@/fixtures` → `frontend/tests/fixtures/`. Any move of the fixtures directory must update this alias.
- **CI**: `.github/workflows/test.yml` has a `frontend-tests` job that runs `pytest frontend/tests/` — this is the invocation to swap.

## Gaps / risks identified

- The fake-pytest bridge means pytest reports a single passing test per shell run, masking individual test failures. Real per-test signal only exists in the shell output. (Migration removes this opacity, but anyone reading old CI history won't have per-test data to compare against.)
- No vitest experience on the team that I can detect from commit history — first PR will need extra review.
- Playwright tests (`frontend/tests/integration/*.spec.ts`) use `@playwright/test`, not vitest. They were *also* invoked via the shell wrapper. Migration must split: vitest for component tests, `@playwright/test` (already installed) for the integration tests.

## Adjacent prior art to consider

- Vitest's official `vite.config.ts` extension pattern (`test:` block via `defineConfig` cast). Standard, well-documented.
- `@vitest/coverage-v8` for fast coverage; `@vitest/coverage-istanbul` for output compatibility with `nyc`-style LCOV.
- `vitest --reporter=junit` for CI test-report ingestion (matches what GitHub Actions consumes today).

## Enrichment quality

- **Tier**: `fallback_2` (native primitives, no semantic index).
- **Confidence**: medium-high. Findings are derivable from file inspection; the load-bearing "no pytest-Python in frontend tests" was confirmed by `grep -r "def test_\|@pytest" frontend/tests/` returning empty.
- **Token cost**: ~520 tokens.
