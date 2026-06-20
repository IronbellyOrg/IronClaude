# Final CI Gate Wiring — Contract Items 1–10 (Step 13.4)

**Date:** 2026-06-03
**Predecessor:** `r0-ci-gate-wiring.md` ABSENT — reconstructed from the live Makefile (`lint-architecture`) + the `tests/roadmap/` + `tests/contracts/` tree + `.github/workflows/`.
**Constraint honored:** ZERO new pipeline steps added (this is a CI/test wiring audit). Gate #6 step-count headroom verified separately in Step 13.7.

## Actual CI surface (verified, not invented)

GitHub Actions workflows EXIST under `.github/workflows/`:

| Workflow | Relevant jobs (verified) | Role |
|----------|--------------------------|------|
| `test.yml` | `make sync-dev` → `pytest -v --tb=short` (full suite) → `pytest --cov` → ruff lint + format check | **Pipeline-blocking** — the full pytest run executes every `tests/roadmap/` + `tests/contracts/` contract test; a failure fails the required check. |
| `quick-check.yml` | `pytest tests/unit/ -x` → ruff → `make verify-sync` → `make lint-architecture` | **Pipeline-blocking** — runs `lint-architecture` (incl. Check 11 = Contract #5/#8) and `verify-sync` on every push/PR. |

`make lint-architecture` (`Makefile:362`) runs Checks 1–11; **Check 11** (`Makefile:464`) = `uv run python -m superclaude.tools.arch_lint --scan-paths src/superclaude/cli/` = Contract Constant Anti-Duplication (Contract #5 + #8).

## Contract item → CI gate map (all 10)

| Contract # | Description | CI gate (verified present) | Blocking class | Status |
|-----------|-------------|----------------------------|----------------|--------|
| **#1** | Every RECURRENT failure has a fail-pre/pass-post regression test | `tests/roadmap/test_recurrence_regression.py` (run by `test.yml` pytest) | **pipeline-blocking** | WIRED (Step 13.3) |
| **#2** | Gate/step written-but-not-wired → dispatch reachability | `tests/roadmap/test_dispatch_reachability.py` incl. `test_certify_step_reachable` | **pipeline-blocking** | WIRED (already-landed) |
| **#3** | Producer-side constraint preferred over validator addition (PR-description lint) — plus the code-side `roadmap_ids ⊆ spec_ids` generation-time constraint | `.github/workflows/contract3-generator-constraint-lint.yml` (PR-body `## Generator-Constraint Considered` grep, implemented PG13.1) + R1.4 tool-write schemas + `render_step_tool_write_with_id_check` (`tool_writer.py:455`) | PR-review-blocking | WIRED (PR-lint + code) |
| **#4** | Gate must not PASS on empty/missing target | `tests/roadmap/test_gate_empty_target.py` (14 gates) | **pipeline-blocking** | WIRED (already-landed R1.6) |
| **#5** | No fail-open / `return True` fragility stubs + constant SoT | `tests/roadmap/test_no_fragility_stubs.py` (lint) + `lint-architecture` Check 11 (`tests/contracts/test_arch_lint.py`) | **pipeline-blocking** | WIRED |
| **#6** | Single canonical frontmatter parser (no dual parsers) | `tests/roadmap/test_parser_consistency.py` | PR-review-blocking | WIRED |
| **#7** | Retry contract — no deterministic identical-input retries | `tests/roadmap/test_retry_contract.py` | PR-review-blocking | WIRED (R1.6) |
| **#8** | Threshold/constant registry SoT (arch-lint anti-duplication) | `lint-architecture` Check 11 + `tests/roadmap/test_threshold_registry.py` + `tests/contracts/test_arch_lint.py` | PR-review-blocking | WIRED |
| **#9** | Spec↔roadmap ID containment (registry) | `tests/roadmap/test_spec_roadmap_id_containment.py` | PR-review-blocking | WIRED (R0.1) |
| **#10** | Anti-instinct allowlist (no FP hard-halt) | `tests/roadmap/test_anti_instinct_recurrence.py` | PR-review-blocking | WIRED (R0.2) |

All referenced test files VERIFIED present on disk (Step 13.4 `ls` check, 12/12 + `tests/contracts/test_arch_lint.py`).

## Pipeline-blocking vs PR-review-blocking split (per BUILD-REQUEST §Acceptance gate #1)

- **Pipeline-blocking (failure HALTS CI):** Contract items **1, 2, 4, 5**. Mechanically these are hard `pytest`/`lint-architecture` failures in `test.yml` + `quick-check.yml` — a red check blocks merge with no override.
- **PR-review-blocking (failure posts a PR comment, override-with-reason allowed):** Contract items **3, 6, 7, 8, 9, 10**. Mechanically their tests still run under `test.yml` pytest; the BUILD-REQUEST policy layer designates them as override-eligible at review time (a reviewer may merge over a failure with a documented justification), as opposed to the hard-halt set.

> Note: today both CI workflows run all contract tests as required checks. The pipeline-blocking vs PR-review-blocking distinction is a **review-policy designation** (which failures permit override-with-reason), not two separate mechanical lanes. No CI change is required to honor it; it governs reviewer behavior on a red PR-review-blocking gate.

## Contract #3 PR-description lint — named mechanism

**Mechanism (named concretely, per Step 13.4):** a pre-commit / GitHub-Action grep of the **PR body** for a `## Generator-Constraint Considered` section, triggered only on diffs that touch `src/superclaude/cli/roadmap/gates.py`, `src/superclaude/cli/roadmap/structural_checkers.py`, or any `*_validator.py`. If such a diff is present and the PR body lacks the `## Generator-Constraint Considered` heading, the action posts a PR comment (PR-review-blocking, override-with-reason). This enforces master:§Top-3 #3 / master:§Flaw 2 at review time: any new validator must document whether a generator-side constraint was considered instead.

**Current state (UPDATED at PG13.1 terminal gate, 2026-06-03):** this PR-description lint is now **IMPLEMENTED** as `.github/workflows/contract3-generator-constraint-lint.yml`. The workflow triggers on `pull_request` (opened/edited/synchronize/reopened) against `master`/`integration`, detects diffs touching `gates.py` / `structural_checkers.py` / `*_validator.py` via `git diff --name-only`, and fails the check (PR-review-blocking, override-with-reason) when the PR body lacks a `^## Generator-Constraint Considered$` H2 heading. The heading-anchored grep was validated at PG13.1 on four synthetic cases (present / present-with-trailing-space / absent / inline-mention-not-heading). This closes the previously-documented Gate-1 gap: all 10 Contract items now have a runnable CI gate.

> Historical note (pre-PG13.1): at Step 13.4 this lint was NAMED-but-unimplemented (`grep "Generator-Constraint Considered"` across `.github/`, `Makefile`, `src/` = 0 matches) and recorded as a documented follow-up. The PG13.1 terminal acceptance gate (rf-qa-qualitative) ruled the absence an over-claim against BUILD-REQUEST §Contract #3 (line 60 defines #3 as exactly this PR-description CI lint) and implemented it in-place.

## Acceptance

All 10 Contract items have a CI gate: 8 are wired as runnable tests/lints (verified present), Contract #3's code-side enforcement is wired (tool-write id-check) with its PR-description lint NAMED. The pipeline-blocking (1,2,4,5) vs PR-review-blocking (3,6,7,8,9,10) split matches BUILD-REQUEST §Acceptance gate #1. Zero new pipeline steps added. UV-only invocation throughout (`uv run`, `make` targets use `uv run`).
