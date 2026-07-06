# Phase 8.3 — Post-Completion Fix Verification

**Context:** the spawned verification agent hit a transient "API Overloaded" error; verification was
performed DIRECTLY by the executor via runtime mutation-probing (more reliable than re-spawn).

## A1 — test_t1116 now ISOLATES the verify gate (FR-9.4) — VERIFIED
Runtime probe:
- `verify=lambda _f: False` on a fully-VERIFIED + in-diff fallback finding → `push_count == 0`.
- Control `verify=lambda _f: True` on the SAME finding → `push_count == 1`.
→ The `push_count == 0` is held ONLY by the fallback's verify-before-remediate gate (the control proves
the finding is intrinsically pushable; apply_edits would accept it). The test now fails if the verify
gate is bypassed — it isolates FR-9.4, not the downstream apply_edits filter.

## A2 — test_t1122 now checks the BOUNDARY (INV-R2) — VERIFIED
Runtime probe (worst case: 2 attributed/declined main pushes + 1 fallback push):
- `push_count == 3` (== max_rounds + 1), `fallback_round_counter == 1`.
→ The `== 3` assertion catches a suppressed fallback push (which would yield 2 ≠ 3) — the loose
`<= 3` could not. The fallback is proven to contribute EXACTLY one push.

## Suite
`uv run pytest tests/pr_submit/` = 176 passed; ruff + format clean. INV-001 untouched (test-only fixes).

VERDICT: PASS — both post-completion test-quality findings addressed and mutation-verified non-vacuous.
