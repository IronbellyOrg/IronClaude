# D-0004: OQ-J Resolution — FR-077 Dual-Budget-Exhaustion Handling

**Task:** T01.04
**Date:** 2026-03-16
**Status:** RESOLVED

---

## FR-077 Description

FR-077 concerns dual-budget-exhaustion: the condition where both the turn budget AND the token budget are exhausted simultaneously (or in rapid succession) during sprint execution. This is distinct from single-budget exhaustion.

---

## v2.26 Placeholder Behavior

**Function:** `_print_terminal_halt()` (sprint executor layer)

In v2.26, `_print_terminal_halt()` does **not** distinguish between single-budget and dual-budget exhaustion. When the sprint halts due to budget exhaustion, the terminal output includes a generic halt message without specific dual-budget diagnostic information.

**Current behavior (v2.26 placeholder):**
- Turn budget exhausted → sprint halts, `_print_terminal_halt()` called with TURN_BUDGET_EXHAUSTED status
- Token budget exhausted → sprint halts, `_print_terminal_halt()` called with TOKEN_BUDGET_EXHAUSTED status
- Both exhausted → whichever triggers first wins; the other condition is not separately reported
- No combined "DUAL_EXHAUSTED" diagnostic output exists

The placeholder behavior is: log whichever budget was exhausted first, halt cleanly, emit resume command. No special dual-exhaustion handling.

---

## v2.26 Deferral Scope

The following FR-077 behaviors are **deferred to v2.26+**:
1. Detecting the dual-exhaustion condition (both budgets exhausted within the same sprint run)
2. Emitting a distinct `DUAL_BUDGET_EXHAUSTED` status in the execution log
3. Providing user-facing recommendations for dual-exhaustion (e.g., "reduce task scope and increase both budgets")
4. Distinguishing dual-exhaustion in the result file (`EXIT_RECOMMENDATION` differentiation)

---

## Phase 4 T04.07 Implementation Note

Phase 4 T04.07 will implement FR-077 dual-budget-exhaustion detection by:
1. Checking both `TurnLedger.available` and token budget remaining after each step
2. If both are ≤ 0 or below threshold simultaneously, set status `DUAL_BUDGET_EXHAUSTED`
3. Modify `_print_terminal_halt()` to accept and render this new status with specific messaging
4. Write `EXIT_RECOMMENDATION: HALT_DUAL_EXHAUSTED` (or similar) to result file

**No Phase 2 or Phase 3 work is blocked by this deferral.**

---

## No Remaining Ambiguity

- v2.26 behavior: placeholder (single-budget-wins logic)
- v2.26 implementation target: T04.07 adds dual-exhaustion detection and distinct output
- All downstream phases can proceed without dependency on FR-077 dual logic
