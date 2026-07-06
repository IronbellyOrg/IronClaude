# QA Report — Internal-Consistency Lens (Phase 5: fsm.py)

**Topic:** pr_submit V1.1 — Phase 5 FSM (re-trigger S5a + oversized-PR fallback S5b)
**Date:** 2026-06-12
**Phase:** structural-consistency (internal-consistency lens)
**Fix authorization:** false (report only)
**Stance:** Adversarial — assumed ≥5 inconsistencies and hunted for them by reading every named file.

---

## Overall Verdict: PASS

The five named claims all hold at the level the tests exercise (the `run_skill` integration driver). No PASS-blocking contradiction was found between the seam names, token values, MonitorState members, and the `clamp_max_rounds` call site. Two genuine internal inconsistencies WERE found (a dual-namespace divergence and a dead transition edge), but both are **latent / non-blocking** because the test surface drives `run_skill`, not `transition()`. They are documented below as IMPORTANT/MINOR drift risks, not failures.

---

## Items Reviewed

| # | Claim | Result | Evidence (BOTH sides cited) |
|---|-------|--------|------------------------------|
| 1 | `rereview_outcome` VALUES (`attributed`/`declined`/`timeout`) match what run_skill reads AND what tests inject | PASS | **Reader side:** fsm.py:974 `if outcome == "declined":`, fsm.py:979 `if outcome == "timeout":`, fsm.py:972 default `"attributed"`. **Test side:** test_review_retrigger.py:48 `["attributed"]`, :87 `["timeout"]`, :121 `["attributed","attributed"]`; test_auggie_fallback.py:79 `["declined"]`, :157/:176 `["attributed","declined"]`. Closed set `{attributed,declined,timeout}` on both sides — exact match. |
| 2 | New RunConfig seam names match the names run_skill/_run_fallback read AND the tests pass | PASS | **Decl side:** fsm.py:713 `rereview_outcome`, :718 `fallback_findings`, :719 `fallback_residual_findings`, :733 `do_retrigger`, :734 `invoke_auggie_review`. **Read side:** `rereview_outcome` read fsm.py:969-970; `fallback_findings` read fsm.py:772; `fallback_residual_findings` read fsm.py:829-830; `do_retrigger` called fsm.py:960; `invoke_auggie_review` called fsm.py:761. **Test side (kwargs):** test_review_retrigger.py:49 `do_retrigger=`, :48 `rereview_outcome=`; test_auggie_fallback.py:103/:137 `invoke_auggie_review=`, :63 `fallback_findings=`. All five seam names resolve identically across decl/read/test. |
| 3 | transition() event strings internally consistent with run_skill state-routing | PASS (with documented drift) | transition() edges: fsm.py:627 `"retriggered"`, :631 `"rereview_attributed"`, :633 `"timeout"`, :635 `"declined"`, :643 `"fallback_findings"`, :647 `"fallback_skip"`. run_skill routes the SAME conceptual edges via the `outcome` token namespace: fsm.py:972 `"attributed"`, :974 `"declined"`, :979 `"timeout"`. Same edges, two namespaces (see Issue #1). No contradiction in behavior; consistent at the conceptual-edge level. |
| 4 | `clamp_max_rounds` is actually CALLED at fallback entry in `_run_fallback` | PASS | **Def side:** fsm.py:145 `def clamp_max_rounds(effective, hard=1)`. **Call side:** fsm.py:757 `result.effective_max_rounds = clamp_max_rounds(base)` inside `_run_fallback`. Confirmed live call, not just defined. Test corroboration: test_auggie_fallback.py:121 `effective_max_rounds == 1` (max_rounds=5 clamped), test_loop_guard.py:209 `effective_max_rounds == 1`. |
| 5 | MonitorState members `S5A_RETRIGGER_REVIEW`, `S5B_AUGGIE_FALLBACK` match models.py | PASS | **Def side:** models.py:115 `S5A_RETRIGGER_REVIEW = "S5a_RETRIGGER_REVIEW"`, models.py:116 `S5B_AUGGIE_FALLBACK = "S5b_AUGGIE_FALLBACK"`. **Use side:** fsm.py:626 `return MonitorState.S5A_RETRIGGER_REVIEW`, :627 edge `(MonitorState.S5A_RETRIGGER_REVIEW, "retriggered")`; fsm.py:639/:642/:643/:647 `MonitorState.S5B_AUGGIE_FALLBACK`. Identifier names match exactly; both are defined and imported via fsm.py:26 `from .models import ... MonitorState`. |

---

## Summary

- Checks passed: 5 / 5
- Checks failed: 0
- Blocking contradictions: 0
- Latent (non-blocking) inconsistencies found: 2 (1 IMPORTANT, 1 MINOR) — documented, NOT fixed (report-only)

---

## Issues Found (latent / non-blocking — do NOT gate this PASS)

| # | Severity | Location (BOTH sides) | Issue | Why non-blocking | Recommended fix |
|---|----------|------------------------|-------|------------------|-----------------|
| 1 | IMPORTANT | `transition()`: fsm.py:631 event `"rereview_attributed"` vs `run_skill`: fsm.py:972/:985 outcome token `"attributed"` | Two parallel, unsynchronized string namespaces describe the same S5→S2 attributed edge. `transition()` keys on the literal `"rereview_attributed"`; `run_skill` keys on `"attributed"`. There is no shared constant binding them. A future edit that renames one token will NOT break the other, silently drifting the table away from the driver. | The TEST SURFACE only drives `run_skill` (every test calls `run_skill(...)`; none call `transition(...)` for these V1.1 edges). So the divergence cannot fail any current test. `transition()` is documented (fsm.py:566) as the §5.4 table but is presently an unexercised parallel encoding for the V1.1 edges. | Either (a) derive both from one `EVENT_*` constant set, or (b) add a test that drives `transition(S5_AWAITING_REREVIEW, "rereview_attributed")` and asserts it agrees with the `run_skill` `"attributed"` path, pinning the two namespaces together. |
| 2 | MINOR | `transition()` edge fsm.py:627 `(S5A_RETRIGGER_REVIEW, "retriggered")` and fsm.py:643/:647 `(S5B_AUGGIE_FALLBACK, "fallback_findings"/"fallback_skip")` | These transition-table edges are **dead** with respect to the test surface and `run_skill`: `run_skill` reaches S5b via the inline `_run_fallback(result, config)` call (fsm.py:875, :977), never by emitting a `"fallback_findings"`/`"fallback_skip"` event into `transition()`. Same for the S5a `"retriggered"` edge — `run_skill` sets `result.state = S5_AWAITING_REREVIEW` directly (fsm.py:962) without routing through `S5A_RETRIGGER_REVIEW`. | No behavioral contradiction; the edges are spec-faithful table entries reserved for Phase 6/7 wiring (fsm.py:15-16 docstring says the module "is extended by Phase 6/7"). They are forward-declared, not wrong. | When Phase 6/7 lands, ensure `run_skill` actually transits these states (or delete the dead edges if the inline path is permanent) so the table and the driver stop diverging. |

### Adversarial cross-checks that PASSED (no inconsistency, ruled out)

- **`S5A_RETRIGGER_REVIEW` state is never assigned by `run_skill`.** Confirmed (fsm.py:962 jumps straight to `S5_AWAITING_REREVIEW`). This is NOT an inconsistency with claim 5 — the claim is only that the *member exists and matches models.py*, which it does (models.py:115). The state being table-only is captured as Issue #2, not a claim-5 failure.
- **`fallback_residual_findings` two-sided semantics agree.** `transition()` reads `ctx.get("fallback_residual_findings")` (fsm.py:652) → HALT_MAX_ROUNDS vs TERMINAL_CLEAN; `_run_fallback` reads `config.fallback_residual_findings` (fsm.py:829) → identical terminal selection (fsm.py:831 HALT_MAX_ROUNDS / :833 TERMINAL_CLEAN). The two code paths encode the SAME selector — consistent.
- **`clamp_max_rounds` monotonicity vs test expectation.** `clamp_max_rounds(base)` with default `hard=1` → `min(base,1)`; max_rounds=5 ⇒ 1 (test_auggie_fallback.py:121, test_loop_guard.py:209). The `base` is `effective_max_rounds if not None else config.max_rounds` (fsm.py:752-756), so a re-entry never raises it. Consistent with the "monotone non-increasing" claim in the docstring (fsm.py:751).
- **`rereview_outcome` shorter-than-cycles defaulting.** fsm.py:969-972: index in range → explicit token; out of range with NON-empty list → `"timeout"`; empty list → `"attributed"`. Matches the docstring contract (fsm.py:707-712) and the test `["attributed","declined"]` for 2 cycles (test_auggie_fallback.py:157, test_loop_guard.py:202) — index 0 attributed (tick→1), index 1 declined (no tick, fallback). round_counter==1 asserted (test_loop_guard.py:206) — consistent.
- **`do_retrigger` skipped when `applied_edits == 0`.** fsm.py:959 guards `if result.applied_edits > 0:` before fsm.py:960 `config.do_retrigger(...)`. Test test_review_retrigger.py:153-160 injects `apply_edits=lambda _:0` and asserts `len(retriggers)==0`, `rereview_request_count==0`. Reader-side guard and test-side expectation agree.

---

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 2 | Glob: 0 | Bash: 2
- Every claim was verified by reading BOTH the producer (fsm.py / models.py) and consumer (test) side and citing file:line on each side. Tool-call count (≥5 Read + 2 Grep) ≥ 5 checklist items — not suspect.

## Recommendations

1. PASS is correct for the Phase 5 deliverable as exercised by the tests. The two latent inconsistencies (dual-namespace event tokens; dead transition edges) are forward-declaration drift, explicitly anticipated by the module's Phase 6/7 docstring — do not block on them.
2. Before Phase 6/7 wiring lands, add a single test that drives `transition()` over the new V1.1 edges so the table namespace (`"rereview_attributed"`, `"fallback_findings"`, `"fallback_skip"`) is pinned against the `run_skill` outcome-token namespace (`"attributed"`/`"declined"`/`"timeout"`). This converts Issue #1 from latent to test-guarded.

## QA Complete

VERDICT: PASS
