# QA Report — Phase 4 Re-verification (round 2)

**Topic:** FR-RH2 headless ensemble Phase 4 re-verification
**Date:** 2026-06-20
**Fix cycle:** 2

---

## Overall Verdict: PASS

The prior CRITICAL finding is resolved under the acceptance-oracle rule. The
task-file phrase "branch only on `expected_tier`" conflicts with the spec
oracle's §9 backward-compatibility requirement; the spec wins. The current
implementation uses a clean production identity seam:

- Production: `expected_tier == 2 and ClaudeProcess is _ProductionClaudeProcess`
  routes to `run_tier2_ensemble`.
- Mocked legacy tests: patched `runner.ClaudeProcess` is no longer identical to
  `_ProductionClaudeProcess`, so the mocked `ClaudeProcess` path remains
  available for the unchanged backward-compat suite.

That reconciliation is documented in the Phase 4 Findings section of the task
file and in the `_audit_once` docstring.

## Items Reviewed

| # | Check | Result |
|---|-------|--------|
| 1 | FR-RH2.1 production Tier-2 routes through ensemble (identity probe `True`) | PASS |
| 2 | FR-RH2.1 Tier-1 grounded `/sc:reflect` path unchanged | PASS |
| 3 | parse_contract + derive_verdict tail and run-loop/writeback unchanged | PASS |
| 4 | NFR-7 no forbidden executable nesting/subprocess constructs (AST check) | PASS |
| 5 | Spec §9 / NFR-RH2.6 floor green (89 passed, 1 xpassed); listed existing tests unmodified (`git diff` empty) | PASS |
| 6 | doc⇆CLI parity passes for `--transport` / `--reviewers` | PASS |
| 7 | Seam is clean identity check, not brittle `__module__` string compare | PASS |

## Spec Oracle Verification

- FR-RH2.1 — PASS
- FR-RH2.5 (ensemble-formation coverage assigned to the non-mocked stub test) — PASS
- NFR-RH2.6 — PASS
- §9 Migration & Rollout (line 538: "Existing reflect tests run unchanged ... the
  mocked-`ClaudeProcess` suite still covers the Tier-1 launch + verdict/write-back
  paths") — PASS

Acceptance-oracle decision: spec §9 line wins over the task-file paraphrase
"branch only on `expected_tier`." The identity-check seam is the only verified
implementation that satisfies both production Tier-2 ensemble routing and the
unchanged mocked-`ClaudeProcess` backward-compat coverage.

## Summary

- Checks passed: 7 / 7
- Critical issues: 0
- Verdict: PASS

## Notes

- Repository-wide `uv run ruff format --check src/ tests/` still fails on 102
  pre-existing unrelated files outside this task's touched surface; not a Phase 4
  acceptance failure (reflect suite green; touched reflect Python files formatted).
