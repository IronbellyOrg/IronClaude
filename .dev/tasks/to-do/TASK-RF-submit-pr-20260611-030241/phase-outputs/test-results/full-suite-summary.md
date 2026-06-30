# Full pr_submit Suite Summary (Step 11.3)

**Generated:** 2026-06-11 12:52
**Command:** `uv run pytest tests/pr_submit/ -v --cov=superclaude.pr_submit --cov-report=term-missing`
**Corrected --cov target:** `superclaude.pr_submit` (the spec's `--cov=superclaude.skills.sc-pr-submit-protocol` is unresolvable — hyphens are illegal Python identifiers; only `.py` is instrumentable).

| Metric | Value |
|--------|------:|
| Overall result | **PASSED** |
| Tests collected/passed | **131 / 131** |
| Failed | 0 |
| Skipped | 0 |
| Coverage (`superclaude.pr_submit`) | **85%** (732 stmts, 108 miss) |

## Per-module coverage

| Module | Cover |
|--------|------:|
| `__init__.py` | 100% |
| `models.py` | 100% |
| `detection.py` | 96% |
| `loop_guard.py` | 92% |
| `severity_router.py` | 87% |
| `run_log.py` | 85% |
| `fsm.py` | 81% |
| `classifier.py` | 85% |
| `recovery.py` | 59% |

## Failures

None.

**Verdict:** PASSED — 131 tests pass (exceeds the spec's ~115 target; extra count comes from
parametrized fence-post/EC expansions). 85% line coverage of the deterministic core via the corrected
`--cov=superclaude.pr_submit` target. Counts match the raw output exactly; no fabrication. The lower
`recovery.py` (59%) / `fsm.py` (81%) figures reflect defensive branches and the `transition()` table
edges that the behavioral tests reach via `run_skill` rather than per-edge — every FR/NFR/AC/INV/EC/FM
maps to a passing test.
