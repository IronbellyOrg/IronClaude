# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | `none`/`DISABLED` means "no POST item" (gate off), distinct from the manual-HALT item | ADDRESSED | HIGH | X-001; resolved to V1 model (none = no item; halt = manual item). Without the distinction, V2's "DISABLED → manual item" silently changes today's behavior. |
| INV-002 | sufficiency_challenge | "auto + wrapper-absent → Mode 1" is sufficient for a would-be-Mode-2 (high-risk) tasklist | ADDRESSED | HIGH | V1 Gate-0 returns `1` unconditionally when `W=false`. Falsifier: a TCS=72, S6=1 tasklist with the wrapper missing would get a *lightweight inline* audit — the weakest review for the highest-risk work. **Resolution:** resolve the risk-mode FIRST (`S6∨S5∨TCS≥35`), THEN apply the wrapper-availability ladder identically to fixed-2 and auto-2: would-be-Mode-2 + wrapper-absent → **manual-HALT (degraded)**, never inline Mode 1. would-be-Mode-1 needs no wrapper → Mode 1. Unifies the fallback and closes the gap. |
| INV-003 | guard_conditions | Fixed `--reflect 1` on a refactor-class (S6=1) / human-decision (S5>0) tasklist is acceptable without warning | ADDRESSED | MEDIUM | X-003. Operator authority is honored, but a silent weak audit on regression-class work is a footgun. **Resolution:** honor fixed-1 (no STOP) but emit an advisory WARNING when fixed-1 is selected with S6=1 or S5>0 ("auto would have selected Mode 2; Mode 1 is not executor-disjoint"). Recorded, non-blocking. |
| INV-004 | count_divergence | The auto mode choice and the baked `--depth` agree even under the ±4 TCS boundary tiebreaker (:2154) | ADDRESSED | MEDIUM | The auto predicate reads the **resolved** depth band (post-override, post-±4-inference), not raw TCS, so `auto→2 ⟺ resolved depth deep` (or S5/S6). Keeps the single-producer property at the band edge. |
| INV-005 | interaction_effects | Setting the new field AND a legacy alias (e.g. `REFLECT_POST_MODE: none` + `POST_REFLECT_MODE: wrapper`) resolves deterministically | ADDRESSED | LOW | Precedence: explicit `--reflect` flag > `REFLECT_POST_MODE` field > legacy alias map > default 2. New field wins; legacy ignored with a build-log note. |
| INV-006 | collection_boundaries | An empty/GOAL-only BUILD_REQUEST still resolves a mode | ADDRESSED | LOW | Absent `--reflect`/field ⇒ default 2; if `POST_REFLECT_GATE: DISABLED` ⇒ none. Total function over all inputs. |

## Summary
- **Total findings**: 6
- **ADDRESSED**: 6
- **UNADDRESSED**: 0 (HIGH: 0, MEDIUM: 0, LOW: 0)
- Convergence NOT blocked: zero HIGH-severity UNADDRESSED invariants. INV-002 (HIGH) drove the most important merge refinement — the unified wrapper-availability fallback ladder.
