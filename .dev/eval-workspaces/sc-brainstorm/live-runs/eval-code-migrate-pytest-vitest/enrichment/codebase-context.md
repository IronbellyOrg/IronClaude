---
source: codebase
topic: migrate from pytest to vitest
quality_tier: fallback_2
---

# Codebase Context — pytest → vitest migration

## Current State Signals

- Repository IS Python-native: `pyproject.toml` at root, no `package.json` at root.
- pytest is the active test runner; multiple `conftest.py` files exist:
  - `./tests/conftest.py`
  - `./tests/roadmap/conftest.py`
  - `./tests/sc-roadmap/conftest.py`
  - `./tests/v3.3/conftest.py`
  - `./tests/pipeline/conftest.py`
- No `vitest.config.*`, `vite.config.*`, or `package.json` at the root level.
- No TypeScript source files at the canonical `src/` paths for a JS/TS project.

## Architecture & Patterns

- Project is Python-first and uses UV for execution. Existing test workflow is pytest-centered: fixtures, parametrize, markers, conftest plugin hooks.
- `.claude/` generated mirrors must not be edited; source-of-truth edits belong under `src/superclaude/`. This brainstorm does NOT modify source components.

## External Framework Notes

- Vitest supports setup files via `test.setupFiles`, coverage via `vitest run --coverage` (c8 or istanbul), and fixtures through `test.extend` with file/worker/automatic/injected scopes.
- pytest provides fixtures, markers (with registration), parametrize, custom CLI options, conftest plugin hooks. These concepts need explicit mapping or deprecation decisions in any migration plan.

## Integration Points

- CI test commands and coverage/reporting gates.
- Test helper modules and fixtures currently shared via pytest conventions.
- Any future JS/TS package configuration (`package.json`, `vitest.config.ts`, Vite config, TypeScript config).

## Constraints Identified

- Vitest cannot directly execute Python tests; migration requires either a JS/TS system under test, a porting strategy, or a dual-run approach.
- pytest plugin hooks and Python fixtures are NOT one-to-one portable to Vitest and require requirement-level decisions before implementation.

## Implication for the Brainstorm

- A literal "migrate the test suite from pytest to vitest" in **this repo** would be ill-defined because there is no JS/TS code under test. The brainstorm treats the topic as a **generic/hypothetical migration strategy** rather than a concrete plan for this specific repo.
- The first open question MUST be: "is the code under test actually JS/TS, or is this a hypothetical?"
- Strategies surfaced (parallel-run vs. hard cutover, parity matrix, coverage gate) generalize to any pytest → vitest migration.

## Enrichment Status

- Codebase: fallback_2 (native Glob, not Auggie — topic is framework-generic, not symbol-specific)
- Research: skipped (no `--research` flag; pytest and vitest are well-known frameworks)
