# QA Report — INV-fidelity Domain Lens (INV-R3 monotone-min arithmetic)

**Phase:** 4 (run_log)
**Target:** `src/superclaude/pr_submit/run_log.py` — MAX_ROUNDS_CLAMPED fold in `rebuild_state`
**Stance:** Adversarial (assume ≥1 arithmetic defect). fix_authorization: false (report only).
**Date:** 2026-06-12

---

## Code Under Test (verbatim, lines 183–194 + seed 161)

Seed (line 161): `"effective_max_rounds": None,`

Fold (lines 183–194):
```python
elif (
    et == EventType.MAX_ROUNDS_CLAMPED.value
    and ev.get("effective_max_rounds") is not None
):
    prev = state["effective_max_rounds"]
    clamp = ev["effective_max_rounds"]
    state["effective_max_rounds"] = (
        clamp if prev is None else min(prev, clamp)
    )
```

INV-R3: one-way, monotone non-increasing clamp recorded once; rebuilt value = minimum
seen; `None` = never-clamped.

---

## Worked-Example Traces

| # | Input sequence | Step-by-step | Result | Expected | Verdict |
|---|---------------|--------------|--------|----------|---------|
| 1 | [clamp=1, clamp=3] | seed=None → ev1(1): prev=None → 1 → ev2(3): prev=1 → min(1,3)=1 | **1** | 1 | PASS — later higher (3) never raises |
| 2 | [clamp=3, clamp=1] | seed=None → ev1(3): prev=None → 3 → ev2(1): prev=3 → min(3,1)=1 | **1** | 1 | PASS |
| 3 | [] | no MAX_ROUNDS_CLAMPED event matches → seed untouched | **None** | None | PASS |
| 4 | [clamp=2, clamp=2] | seed=None → ev1(2): prev=None → 2 → ev2(2): prev=2 → min(2,2)=2 | **2** | 2 | PASS — idempotent |

All four worked examples reproduce the expected INV-R3 result against the actual code.

---

## Guard Verification (None / missing effective_max_rounds)

- Branch entry requires BOTH `et == EventType.MAX_ROUNDS_CLAMPED.value` AND
  `ev.get("effective_max_rounds") is not None` (lines 184–186).
- **Missing key:** `ev.get("effective_max_rounds")` → `None` → `is not None` is False →
  branch skipped → `prev`/state untouched. GUARDED.
- **Present-but-None value:** same `ev.get(...) is not None` evaluates False → skipped.
  GUARDED.
- **None on a different event type:** the `et ==` conjunct already excludes non-clamp
  events from this branch regardless of the value. GUARDED.
- Consequence: `clamp = ev["effective_max_rounds"]` (line 191) can never bind `None`,
  so `min(prev, clamp)` and the `prev is None` seed path are never fed a `None` operand.
  No `TypeError`-on-`min(int, None)` path exists.

---

## Monotone Non-Increase Verification (no path raises the value)

- The ONLY assignment to `state["effective_max_rounds"]` inside `rebuild_state` is at
  lines 192–194 (this branch). Confirmed by reading the full method (lines 146–216):
  no other branch writes the field; it is initialized once at line 161 and read at
  line 190.
- Two sub-cases of the write:
  - `prev is None` → result = `clamp` (first observed value seeds it; this is the
    transition from never-clamped, not an increase of a prior numeric).
  - `prev is not None` → result = `min(prev, clamp)` ≤ `prev` for all clamp.
    Strictly non-increasing; equality when `clamp >= prev` (Examples 1 & 4 cover both
    `clamp > prev` and `clamp == prev`).
- Therefore no execution path raises the rebuilt value. INV-R3 monotone non-increasing
  property holds.

---

## Adversarial Findings

Searched for the classic defects in a monotone-min fold:
- `max` instead of `min` — NOT present (line 193 uses `min`).
- Seed wrong (e.g., 0 or a large int instead of `None`) — NOT present (seed is `None`,
  line 161); `None`-seed semantics correctly distinguish never-clamped.
- Inverted seed branch (`prev if prev is None else ...`) — NOT present; the ternary
  correctly yields `clamp` when `prev is None`.
- Unguarded `None` reaching `min` — NOT present (guard at line 185–186).
- Operand swap in `min` — irrelevant (`min` is commutative).
- Field written elsewhere overriding the clamp — NOT present (single writer).

No arithmetic defect found in the INV-R3 fold.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Example 1 [1,3]→1 | PASS | trace above; min(1,3)=1 |
| 2 | Example 2 [3,1]→1 | PASS | trace above; min(3,1)=1 |
| 3 | Example 3 []→None | PASS | no matching event; seed None (L161) |
| 4 | Example 4 [2,2]→2 | PASS | trace above; min(2,2)=2 |
| 5 | None/missing guard | PASS | L185–186 `is not None` conjunct |
| 6 | No path increases value | PASS | single writer L192–194; min ≤ prev; None-seed |

---

## Confidence

Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 1 | Grep: 0 | Glob: 0 | Bash: 0
(Single-file scope per spawn instruction; full method read lines 146–216 to confirm
single-writer claim — no grep needed.)

---

## Overall Verdict

VERDICT: PASS
