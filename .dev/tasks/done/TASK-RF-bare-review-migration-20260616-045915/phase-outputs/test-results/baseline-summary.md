# Baseline — `tests/swarm/` Pre-Migration State

**Status: Complete**
**Captured:** 2026-06-16 (Step 1.3, before any WS-0 change)
**Command:** `uv run pytest tests/swarm/ -q`
**Raw output:** `baseline-pytest-swarm.txt`

## Overall Result

`2212 passed, 26 skipped in 11.08s` — **GREEN**, no failures, no errors.

| Metric | Count |
|--------|-------|
| Passed | 2212 |
| Failed | 0 |
| Skipped | 26 |
| Errors | 0 |

## Key Test Files Tracked Across the Migration

| File | Baseline state | Notes |
|------|----------------|-------|
| `test_bare_review_parity.py` | **17 passed** (0 skipped) | Currently RUNS because the legacy `scripts/t2_normalize.py` still exists; the `skipif(LEGACY_SCRIPT.exists())` whole-module guard is therefore NOT active. WS-B rebuilds this gate so it survives WS-C deletion; WS-C must keep it at 17 PASS (not SKIPPED). |
| `test_recipe_bare_review.py` | **16 passed** (0 skipped) | Contains the SECOND legacy-coupled test (`test_legacy_vs_recipe_byte_identical` + bare `assert LEGACY_SCRIPT.exists()`) that HARD-FAILS on deletion. WS-C Step 5.2 reworks it. |

## Skipped Tests (26 total)

The 26 skips are pre-existing and NOT bare-review-related. Observed skip clusters in the raw output:
- `test_tmux_detached.py` — `.............ssssss` (6 skips, tmux-dependent environment gating)
- Remaining ~20 skips distributed across the suite (env-gated real-proxy / optional-dependency tests, e.g. `test_e2e_real_proxy.py` `SWARM_REAL_E2E` gating).

None of the skipped tests are `test_bare_review_parity.py` or `test_recipe_bare_review.py` — both of those RUN at baseline.

## Regression-Comparison Contract for Later Phases

Any later phase gate (WS-0 Step 2.10, WS-A Step 3.5, WS-B Step 4.5, WS-C Step 5.11, final PC.2) MUST confirm:
1. Every test passing here (2212) still passes.
2. `test_bare_review_parity.py` and `test_recipe_bare_review.py` RUN and PASS (must NOT become SKIPPED after WS-C deletes `t2_normalize.py` — a SKIP there is a FAIL).
3. New tests added by WS-0/WS-B are net additions on top of this baseline.
