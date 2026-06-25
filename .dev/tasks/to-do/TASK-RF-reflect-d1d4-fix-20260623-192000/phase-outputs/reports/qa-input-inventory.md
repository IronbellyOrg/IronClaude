# QA input inventory — D1–D4 remediation deliverables

**Date:** 2026-06-24 · Chosen D1 design: **(b) telemetry-honesty narrowing**

## Files under QA (this task's deliverables ONLY)

| Path | Role | Note |
|------|------|------|
| `src/superclaude/cli/reflect/ensemble.py` | D1 code | contract-telemetry branch (`:315-316`) → `"snapshot-children-only"` |
| `src/superclaude/cli/reflect/runner.py` | D1 code | operator-visible write (`:682`) → `"snapshot-children-only"` |
| `src/superclaude/cli/reflect/models.py` | D1 code | `ReflectResult.reviewer_isolation` enum doc comment + new value |
| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` | D1 doc | Step 0.5e item 4 + telemetry line rewritten honestly (synced) |
| `tests/cli/reflect/test_reviewer_swarm_target_grounding.py` | D1 test | NEW falsifier (fail-before→pass-after) + default-OFF guard |
| `tests/cli/reflect/test_reviewer_isolation_gate.py` | D1 test | line-84 assertion updated `"snapshot"`→`"snapshot-children-only"` (sanctioned) |
| `src/superclaude/agents/reflect-reviewer.md` | D3 citation | `:133` "Rationale source" rewritten to worktree-resolvable docs (synced) |
| `phase-outputs/plans/d1-design-decision.md` | D1 decision record | RESOLVED, operator chose (b) |
| `phase-outputs/reports/d2-bookkeeping-reconciliation.md` | D2 note | NON-BLOCKING, out-of-tree |
| `phase-outputs/reviews/d4-invariant-lock-verification.md` | D4 note | NON-BLOCKING, verify-only, PASS |

## Test artifacts (evidence)

- `phase-outputs/test-results/baseline-summary.md` — 143 passed (fail-before baseline)
- `phase-outputs/test-results/d1-failbefore.txt` — new test FAILED pre-fix (`'snapshot' != 'snapshot-children-only'`)
- `phase-outputs/test-results/d1-passafter.txt` / `final-pytest.txt` — 145 passed, 1 xpassed
- `phase-outputs/test-results/final-ruff.txt` — 5 files formatted clean
- `phase-outputs/plans/d1-verify.md`, `phase-outputs/plans/final-static-verify.md` — verdicts

NOT under this gate (parent six-layer task's uncommitted work): `process.py`, `commands.py`, `config.py`, `reviewer-spec.md`, `test_cli_smoke.py`, and the other six-layer test files.
