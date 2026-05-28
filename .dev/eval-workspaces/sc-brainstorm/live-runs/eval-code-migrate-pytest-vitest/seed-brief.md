---
schema_version: "1.0"
topic: "Brainstorm migration of a test suite from pytest to vitest"
domain: code
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
intent_summary: "Plan a structured migration of an existing pytest test suite to vitest, preserving coverage and CI signal during the cutover."
context_anchors:
  - type: concept
    value: "pytest"
    source: topic
    confidence: high
  - type: concept
    value: "vitest"
    source: topic
    confidence: high
  - type: component
    value: "test suite"
    source: topic
    confidence: high
  - type: concept
    value: "migration"
    source: topic
    confidence: high
must_preserve:
  - "pytest (current test framework — must be characterized before removal)"
  - "vitest (target test framework — destination of migration)"
  - "test suite (the artifact being migrated)"
  - "migration must not silently drop coverage or invariants"
out_of_scope:
  - "(none — no explicit out-of-scope statements in topic; non-interactive quick run; surfaced as an open question)"
source_confidence: medium
created: 2026-05-27T00:00:00Z
---

# Seed Brief: code-migrate-pytest-vitest

## Intent Summary

The user wants a structured brainstorm of how to migrate an existing test suite from pytest (Python) to vitest (JavaScript/TypeScript). The migration must preserve test coverage and CI signal throughout the cutover so the team does not lose regression protection mid-migration. Quick-depth scope: surface the two highest-leverage migration strategies and their trade-offs, not exhaustive enumeration.

## Context Anchors

- concept — pytest (topic/high)
- concept — vitest (topic/high)
- component — test suite (topic/high)
- concept — migration (topic/high)

## Must Preserve

- pytest must be characterized (existing test inventory, fixtures, plugins, markers, coverage baseline) before removal
- vitest is the explicit target framework — alternatives are not in scope unless surfaced as an open question
- The test suite as a whole is the migration unit — partial / per-module migration is acceptable but must reach a coherent end state
- Migration must not silently drop coverage or invariants

## Out of Scope

- (none — no explicit out-of-scope statements were captured in the topic; this is a non-interactive quick-depth run, so out-of-scope is left open and surfaced as an open question below)

## Problem Statement

The project currently uses pytest for its test suite. The team wants to migrate to vitest. The hurt: maintaining two test runners is operationally expensive, and a Python-vs-JS/TS toolchain split typically signals the underlying code has migrated (or is migrating) to a JS/TS stack — pytest no longer aligns with what is under test. Risk: a naive rewrite loses coverage, hides regressions, or stalls partway and leaves the team with two half-migrated runners forever.

## Known Context

- pytest is the current framework (Python ecosystem: fixtures, parametrize, markers, conftest, plugins, coverage via pytest-cov)
- vitest is the target framework (JS/TS ecosystem: Vite-based, jest-compatible API, describe/it, vi.mock, c8/istanbul coverage)
- Migration implies the codebase or significant portion is JS/TS (or moving there); if not, the migration is blocked at a more fundamental layer
- Quick-depth brainstorm: focus on the 2-3 highest-leverage migration strategies, not exhaustive enumeration

## Constraints

- Test framework parity: vitest must cover the same behaviors pytest covered (fixtures → setup/teardown, parametrize → test.each, markers → describe filters or vitest config)
- CI must stay green during the migration window (no extended red period)
- Coverage must not silently regress
- Two-runner period (parallel run) must have a defined end-state — never permanent

## Success Criteria

- All pytest tests have an equivalent vitest test (or an explicit decision to drop with rationale captured in provenance)
- CI runs vitest as the canonical test gate at cutover
- Coverage report from vitest meets or exceeds the pytest baseline
- pytest configuration, plugins, and runner are removable from the repo without breaking CI
- Migration plan has a defined cutover criterion and a defined rollback (e.g., re-enable pytest job if vitest blocks a release)

## Open Questions

- Is the underlying code already JS/TS, or is the language migration concurrent with the test migration?
- What is the size of the current pytest suite (test count, file count, fixture complexity)?
- Are there pytest plugins in use that have no vitest equivalent (e.g., pytest-xdist, pytest-bdd, pytest-asyncio specifics)?
- Is there appetite for parallel-run (both runners green in CI) or is a hard cutover acceptable?
- Is there an explicit deadline or release boundary driving this?
- What is explicitly out of scope (e.g., E2E tests, snapshot strategy, contract tests)?
