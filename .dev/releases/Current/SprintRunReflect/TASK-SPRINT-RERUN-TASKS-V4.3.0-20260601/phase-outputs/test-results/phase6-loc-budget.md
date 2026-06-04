# Phase 6 — recovery.py / rerun_tasks.py LOC Budget (Step 6.5)

**Date:** 2026-06-02 · **Raw:** `phase6-loc-raw.txt`
**Command:** `wc -l src/superclaude/cli/sprint/recovery.py src/superclaude/cli/sprint/rerun_tasks.py`

| File | Actual (wc -l) | TDD budget | Delta | Assessment |
|------|----------------|------------|-------|------------|
| `recovery.py` | 687 | ~250 (TDD line 209) | **+175%** | EXCEEDS +40% — INVESTIGATE |
| `rerun_tasks.py` | 1425 | ~280 (TDD line 210) | **+409%** | EXCEEDS +40% — INVESTIGATE |
| **Total** | 2112 | ~530 | +298% | — |

## Assessment

Both new modules substantially exceed the TDD's ~250/~280 LOC estimates (the ±20% PASS band would be ~200–300 / ~224–336). `wc -l` counts include docstrings, blank lines, and section banners, so raw LOC overstates pure code; nonetheless the overage is large enough to flag as **INVESTIGATE** (per the >40%-over threshold), not a silent pass.

**Likely drivers of the growth (for the structural QA to weigh):**
- `rerun_tasks.py` hosts ~26 functions (verified via `def` grep), including the full `run_rerun_tasks` orchestrator (~230+ lines on its own), all 7 mandatory TDD §T8 failure-mode defenses (SHA abort, retry-cap, stash/restore, lock, bundle-suffix, abort auto-restore, forensic rename), the transcript legacy fallback, dependency walker with transitive closure, checkbox flip/restore/finalize trio, and extensive docstrings.
- `recovery.py` hosts the `RecoveryBundle`/`RecoveryBundleRef`/`RecoveryStatus`/`Nominator` (×3 impls) surface, the 7-step `merge_recovery_bundle` engine, audit-log writer, SHA + lock helpers, and `__all__` re-exports.

**Verdict:** The estimate appears to have under-counted the defense + helper + docstring surface rather than indicating dead code or scope creep — but the magnitude (especially rerun_tasks.py at ~5×) warrants the post-completion structural QA (Step 6.6) confirming there is no duplication / unused code / TB-Add-5 XL-item violation. Flagged accordingly; not treated as a silent pass.
