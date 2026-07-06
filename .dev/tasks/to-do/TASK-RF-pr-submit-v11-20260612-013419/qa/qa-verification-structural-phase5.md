# Phase 5 — Structural Verification (fix-cycle re-check, HIGHEST-RISK)

**Phase:** fix-cycle (structural verification of Step 5.G6 fixes)
**fix_authorization:** false (verify only — nothing modified)
**Stance:** adversarial. Every claim re-checked against source, not against the fix doc's prose.
**Date:** 2026-06-12

---

## Overall Verdict: PASS

All 4 ACTIONABLE fixes (F2, F3, F4, F5) landed and are correct. **INV-001 is preserved
verbatim**: the S5→S2 `rereview_attributed` edge is byte-identical, the `>=` gate is unchanged,
and there is EXACTLY ONE `round_counter += 1` site. The F2 state-materialization did NOT introduce
a second increment, alter the increment site, or leak a non-terminal state into a returned result.
Deferred findings F1/F6/F7 are documented, not dropped. No `gh`/`git` executable token introduced.
`pytest tests/pr_submit/` = **172 passed**.

---

## (a) Each fix landed

| Fix | Claim | Verified | Evidence (file:line) |
|---|---|---|---|
| F2 | `result.state = S5B_AUGGIE_FALLBACK` at `_run_fallback` entry | PASS | fsm.py:753 (with explanatory comment 751–752: "terminal selector below overwrites … but this materializes the topology entry") |
| F2 | `result.state = S5A_RETRIGGER_REVIEW` at the re-trigger step | PASS | fsm.py:968, inside the `if result.applied_edits > 0:` branch (964) — the applied_edits>0 branch as the fix doc claims |
| F3 | "attributed"→"rereview_attributed" mapping comment | PASS | fsm.py:978–981: documents the `"attributed"` OUTCOME token (run_skill vocab) vs transition()'s `"rereview_attributed"` EDGE event as "two deliberately distinct vocabularies … NOT the same string by design" |
| F4 | `test_transition_v11_edges` exists, exercises 6 edges + INV-001 edge | PASS | test_auggie_fallback.py:231–261 — see breakdown below |
| F5 | auggie strict-once test calls `_run_fallback` twice + fresh control | PASS | test_auggie_fallback.py:93–126 — see breakdown below |

**F4 edge coverage (test_auggie_fallback.py:231–261):**
- L235 RESOLVING/resolved → S5A_RETRIGGER_REVIEW (MOD)
- L237 S5A/retriggered → S5_AWAITING_REREVIEW (ADD)
- **L239 S5_AWAITING_REREVIEW/rereview_attributed → S2_CLASSIFY (PRESERVED INV-001 edge)** ✓
- L241 S5/timeout → TERMINAL_TIMEOUT (preserved sibling)
- L243 S5/declined → S5B_AUGGIE_FALLBACK (ADD)
- L244 S2/declined → S5B_AUGGIE_FALLBACK (ADD)
- L246 S5B/fallback_findings → S2_CLASSIFY (ADD)
- L248 + L249–256 S5B/fallback_skip → TERMINAL_CLEAN / HALT_MAX_ROUNDS residual selector (ADD)
- L258–261 needs_human pre-gate short-circuit AHEAD of V1.1 routing
Count = 6 new V1.1 edges + the INV-001 edge + pre-gate. Exceeds the "6 edges + INV-001" bar.

**F5 strict-once strengthening (test_auggie_fallback.py:93–126):**
- L112 first engagement via `run_skill`; L113–114 assert invoked + `len(calls)==1`.
- L117 **second `_run_fallback(result, config)` on the SAME result**; L118–120 assert `len(calls)==1`
  (strict-once guard held across re-entry — the cross-entry double-invoke the flag exists to block).
- L124–126 **fresh control** `SkillResult()` → `_run_fallback` → `len(calls)==2`, proving the guard is
  the cause, not an inert recorder. Both required components present.

## (b) INV-001 PRESERVED VERBATIM (the critical check)

| Sub-check | Result | Evidence |
|---|---|---|
| S5→S2 `rereview_attributed` edge byte-identical | PASS | fsm.py:631–632 `if edge == (S5_AWAITING_REREVIEW, "rereview_attributed"): return S2_CLASSIFY` — comment "loop-guard increments at this edge (INV-001)" intact |
| `>=` gate (should_halt_rounds) unchanged | PASS | fsm.py:135–142 delegates to `loop_guard.should_halt`; loop_guard.py:30 `return round_counter >= max_rounds` (`>=` not `>`, INV-5). Single source — no drift. |
| EXACTLY ONE `round_counter += 1` site | PASS | `grep -nE '[^_]round_counter \+= 1' fsm.py` → **1 match: line 1001** (only). The fallback increments the SEPARATE `fallback_round_counter` (lines 782, 828) — confirmed distinct counter, not a second `round_counter` tick. |
| Increment fires only on attributed outcome, post-push | PASS | fsm.py:987–1001: `declined`→fallback+break (987–991), `timeout`→TERMINAL_TIMEOUT+break (992–996), else `attributed` → `result.round_counter += 1` (1001). Site is AFTER push (954–958) and BEFORE the next-iteration top-of-loop `should_halt_rounds` (889) — `max_rounds=N ⇒ N pushes` preserved. |

The F2 state assignments at lines 753 and 968 are pure `result.state` mutations — they do NOT touch
`round_counter`, the gate, or the edge table. INV-001 is structurally untouched by the fix.

## (c) F2 transient states OVERWRITTEN by terminal (no non-terminal leak)

| Site | Transient state | Overwritten before return? | Evidence |
|---|---|---|---|
| fsm.py:753 (`_run_fallback` entry, S5B) | S5B_AUGGIE_FALLBACK | YES — every return path reassigns `result.state` | Reassignments at 771 (HALT_MAX_ROUNDS), 783 (TERMINAL_CLEAN), 788 (HALT_HUMAN), 792 (PROPOSED), 800 (VALIDATION_FAIL), 815 (S4_HALT_BEFORE_PUSH/push_fail_state), 836 (HALT_MAX_ROUNDS), 838 (TERMINAL_CLEAN). No path returns with S5B still set. |
| fsm.py:968 (run_skill re-trigger, S5A) | S5A_RETRIGGER_REVIEW | YES — unconditional reassign one statement later | fsm.py:971 `result.state = S5_AWAITING_REREVIEW` (unconditional, outside the applied_edits>0 guard), then outcome branches at 990/995/1006 set a terminal. S5A never survives to a returned SkillResult. |

Both transient assignments are topology-fidelity markers only; neither leaks a non-terminal state.

## (d) No `gh`/`git` executable token introduced

PASS. `grep -nE '\b(gh|git)\b'` on fsm.py returns no executable-token matches (only benign
substrings like `origin`, `GitHub`, `digit` are excluded). The F2/F3 changes are `result.state`
assignments + a comment. NFR-6 core purity intact. Independently corroborated by the in-suite
`test_static_grep.py` (6 passed).

## (e) Deferred findings F1/F6/F7 documented (not dropped)

PASS — all three present in BOTH artifacts:
- **F1** (forked fallback pipeline → by-design): consolidated findings row F1 + fix-applied
  "Deferred/no-fix" bullet 1. Rationale (run_skill is existing imperative driver; refactor
  high-risk in highest-risk phase; mitigated by F4) recorded.
- **F6** (fence-post matrix non-discrimination of `>=` gate): consolidated F6 + fix-applied bullet 2.
  `>=` gate guarded by `test_gate_uses_ge_not_gt` + `test_fallback_round_counter_cap_one`.
- **F7** (recovery.py "unchanged" wording): consolidated F7 + fix-applied bullet 3. Semantics
  accepted (Branch-A target unperturbed).

---

## Test suite

`cd /config/workspace/IronClaude && unset VIRTUAL_ENV && uv run pytest tests/pr_submit/ -q`
→ **172 passed in 0.24s** (matches fix-applied doc's "172 passed (was 171; +1 transition test)").

## Confidence

- **Verified:** 5/5 spawn-prompt assertions (a–e) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 4 | Grep(Bash): 6 | Glob: 0 | Bash(pytest): 1

## Adversarial notes (probed, found clean)
- Checked the fallback's `fallback_round_counter += 1` (782, 828) is NOT a disguised second
  `round_counter` tick — the `[^_]` grep anchor confirms they are lexically distinct identifiers.
- Confirmed L968 S5A sits in the `applied_edits > 0` branch (964) per the fix doc — not the zero-edit
  path, so it cannot be reached on a no-push cycle that should stay at TERMINAL_TIMEOUT/etc.
- Confirmed the `>=` gate has a SINGLE source (delegation at 142 → loop_guard:30); no inline `>` copy
  was introduced anywhere in fsm.py.

VERDICT: PASS
