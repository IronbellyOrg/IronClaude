# Phase 4 — Regression Subset Summary

**Date:** 2026-06-04 (Step 4.1)
**Command:** `uv run pytest tests/audit/ tests/skills/test_task_builder_merge.py tests/sprint/test_checkpoints.py tests/audit/test_checkpoint.py -q`
**Raw output:** `phase4-regression-pytest.txt`

## Counts: NOW vs Phase 1 baseline

| Metric | Phase 1 baseline | Phase 4 (post-edit + sync-dev) | Δ |
|---|---|---|---|
| failed | 26 | **7** | −19 (improved) |
| errors | 37 | **21** | −16 (improved) |
| passed | 1233 | **1268** | +35 (improved) |
| skipped | 1 | 1 | 0 |
| distinct failing/erroring nodeids | 63 | **28** | −35 |

## Regression analysis (the decisive test)

- **Green→Red (regressions introduced by the edits): ZERO.** `comm -13 baseline now` over the deduped
  failing/erroring nodeid sets is **empty** — every test failing now was ALSO failing in the Phase 1 baseline.
- **Red→Green (resolved by `make sync-dev`): 35.** These were the stale-`.claude/`-mirror failures the Phase 1
  baseline flagged (byte-identity / mirror-line-number / mirror-exists assertions). Regenerating the mirror in
  Steps 2.14/3.15 fixed them, exactly as predicted in `phase1-baseline.md`.
- **Current 28 failing/erroring nodeids ⊂ baseline 63** (net-new = 0 → all pre-existing).

## What the remaining 28 pre-existing failures are

Grouped by file (all pre-existing, all in baseline):

| Count | File | Nature |
|---|---|---|
| 9 | `tests/audit/test_synthetic_dnsp_dedup_not_regression.py` | `TestCanonicalFixtureParity` — canonical fixture-log parity/load |
| 7 | `tests/audit/test_regression_halt_pass1_fail2.py` | `TestCanonicalFixtureParity` — canonical fixture-log parity/load |
| 6 | `tests/audit/test_slow_shrink_continues.py` | `TestCanonicalFixtureParity` — canonical fixture-log parity/load |
| 5 | `tests/audit/test_monotonicity_halt_F_5_5_5.py` | `TestCanonicalFixtureParity` — canonical fixture-log parity/load |
| 1 | `tests/audit/test_invariant_preservation_NFR_6_through_10.py` | `test_task_id_naming_pattern_preserved` |

All are `TestCanonicalFixtureParity` fixture-load failures (a worktree-state artifact — the canonical
fixture log is absent/stale here; they ERROR at setup) plus one task-ID-naming-pattern test. **None** of them
exercises the markdown content this task edited. The break-risk-surface tests the task flagged
(DNSP-content / TB-Add-8 / INV-002/010/019 / NFR-CONV-6..10 wire-strings / severity-floor / inherited-verdict /
axis-column / monotonicity+regression halt wire-strings) are **GREEN** — the "dnsp"/"monotonicity" filename
matches above are `TestCanonicalFixtureParity` *fixture* tests, not the content-assertion tests, and they were
already failing in baseline.

Note: because the **G-1 path** was taken (no `rf-qa.md` edit), `tests/audit/test_dynamic_enumeration_inv_010.py`
is GREEN (it was among the 35 resolved by sync-dev) — the optional TB-Add-9 `inv_010` re-run is NOT required.

**VERDICT: GREEN-equivalent. Zero regressions introduced; all remaining failures are pre-existing baseline
failures (fixture-parity worktree artifacts), and 35 baseline failures were resolved by sync-dev.**
