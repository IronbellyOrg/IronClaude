# Phase 5 — Output Inventory (fsm control flow — HIGHEST-RISK)

Change-set for the Phase 5 M3 lens gate. FR-8.1-8.6, FR-9.1-9.5, FR-10.1-10.5,
INV-001 PRESERVED, INV-R1/R2/R3, EC-17..24.

| File | V1.1 delta | FR / INV / T-ID |
|---|---|---|
| `src/superclaude/pr_submit/fsm.py` | (5.1) `clamp_max_rounds(effective, hard=1)` pure helper. (5.2) RunConfig: `do_retrigger`/`invoke_auggie_review` (`_noop` seams), `rereview_outcome: list[str]`, + input seams `fallback_findings`/`fallback_residual_findings`. (5.3) transition() surface: MOD RESOLVING/resolved→S5A; +5 edges (S5A/retriggered→S5, S5/declined→S5B, S2/declined→S5B, S5B/fallback_findings→S2, S5B/fallback_skip→TERMINAL_CLEAN\|HALT_MAX_ROUNDS). INV-001 edge byte-identical; needs_human short-circuit first; defensive return last. (5.4) run_skill surface: REMOVED optimistic `:793` increment; relocated tick gated on `rereview_outcome[i]=="attributed"` (back-compat: empty→all "attributed"); S5a `do_retrigger` only when applied_edits>0; timeout→no-tick→TERMINAL_TIMEOUT; declined→fallback. (5.5) `_run_fallback` single-shot sub-loop: clamp once (INV-R3), invoke once (INV-R2), cap-1, frozen round_counter, no loop-back. | FR-8/9/10, INV-001, INV-R1/R2/R3 |
| `src/superclaude/pr_submit/recovery.py` | **UNCHANGED** — OQ-1 PENDING human decision (`phase-outputs/plans/oq1-recovery-resume-target.md`) | OQ-1 |
| `tests/pr_submit/test_review_retrigger.py` | NEW, 7 tests (R1): T-1101..T-1106 + T-PUSH-WITHOUT-REREVIEW-NO-TICK | FR-8, INV-R1 |
| `tests/pr_submit/test_auggie_fallback.py` | NEW, 8 tests (R2/R3): T-1110/T-1113/T-1121/T-1122/T-1123/T-1125 + T-AUGGIE-AT-MOST-ONCE + FR-9.4 | FR-9/10, INV-R2/R3 |
| `tests/pr_submit/test_loop_guard.py` | EXTENDED +4 (deferred-increment, INV-R1, INV-R3 independence, fallback cap-1); 9 INV-001 fence-post tests UNCHANGED | INV-001/R1/R3 |
| `tests/pr_submit/fixtures/` | NEW: rereview-attributed.json, rereview-then-decline.json, auggie-fallback-findings.json | — |

**Tests:** 28 Phase-5 targeted + 171 full pr_submit suite (was 138 baseline). EXACTLY one
`round_counter += 1` (fsm.py:987). NFR-6 grep: 4 pre-existing docstring matches, zero executable.

**Dual-surface note:** the `fallback_skip` terminal selector exists on BOTH surfaces and AGREES:
transition() uses `ctx.get("fallback_residual_findings")`; run_skill `_run_fallback` uses
`config.fallback_residual_findings` → both produce TERMINAL_CLEAN (no residual) vs HALT_MAX_ROUNDS.
