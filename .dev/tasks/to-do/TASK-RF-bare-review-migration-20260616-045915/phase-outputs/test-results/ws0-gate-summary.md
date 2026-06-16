# WS-0 STRICT Gate Summary (Step 2.10)

**Status: Complete**
**Date:** 2026-06-16
**Verdict: PASS**
**Raw output:** `ws0-gate.txt`

## pytest — `uv run pytest tests/swarm/ -q`

| Metric | Baseline | WS-0 | Delta |
|--------|----------|------|-------|
| Passed | 2212 | **2215** | +3 |
| Failed | 0 | **0** | 0 |
| Skipped | 26 | 26 | 0 |

**No new regressions.** Every test passing at baseline still passes (verified: the
one transient failure during the gate — `test_no_claude_isms` flagging a comment
that capitalized "Grep" — was fixed by lowercasing the comment to "grep-friendly",
which is what the pre-WS-0 stub used; re-run is fully green).

The +3 are the WS-0 net-new tests:
- `test_reviewers_flag_overrides_worker_count` (B-1 — `--reviewers 4` dispatches 4)
- `test_reviewers_flag_rejects_out_of_range` (B-1 — out-of-[2,4] → EXIT_USAGE)
- `test_quickstart_emits_normalized_artifacts` (G-3 — inline run emits contract + 3 bodies)

The flipped/updated tests (`test_quickstart_does_not_emit_done_sentinel`,
`test_quickstart_lens_bare_review_emits_observability_artifacts`) are renames of
existing tests, so they do not change the count.

`test_bare_review_parity.py` (17) and `test_recipe_bare_review.py` (16) still PASS
(legacy script still present — WS-C deletion is Phase 5).

## ruff — path-scoped (`commands.py normalize.py reduce.py dispatch.py preflight.py test_e2e_user_guide.py`)

2 errors, **both PRE-EXISTING** (confirmed against start commit `02582ca0`):
- `commands.py:1712` — `F821 Undefined name 'Logger'` (forward-ref string annotation; `Logger` imported lazily inside the function). Present pre-WS-0.
- `normalize.py:73` — `I001` (import block un-sorted/un-formatted). Present pre-WS-0 (NOT touched by WS-0). [Corrected per PG2 C3 — this was mislabeled as `F821 Logger` in an earlier draft; the real code is `I001`.]

`reduce.py`, `dispatch.py`, `preflight.py`, `test_e2e_user_guide.py` — clean.

**No NEW ruff issues introduced on any touched file.**

## Overall: WS-0 PASS

Inline `swarm run --lens bare-review --transport stub` now runs the full Wave 1→2→3
pipeline (4 new CLI flags + assembled prompt + worker_spec + per-reviewer path-stamping
+ normalize_wave2 + reduce_wave3), emitting `return-contract.yaml` + normalized
per-reviewer bodies + `merged.md`. The resume branch is unchanged. Ready for Phase Gate 2.
