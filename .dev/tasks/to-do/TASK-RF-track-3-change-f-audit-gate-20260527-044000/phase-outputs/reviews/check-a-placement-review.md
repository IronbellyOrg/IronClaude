# Check (a) — Subsection Placement Review

**Verdict:** PASS
**Date:** 2026-05-27

## Anchor line numbers (from grep)

| Anchor | Line |
|--------|------|
| `### Wave 3: Tier 2 — Parallel Hypotheses` | 230 |
| `4. **Distill candidate fixes**` | 264 |
| `#### Tier 2 calibration completeness gate (hard precondition for report publishing)` | **266** |
| `**Exit criteria**:` (Wave 3's) | 278 |
| `### Wave 4: Tier 2 — Adversarial Fix Debate` | 295 |

## Structural assertions

1. **Inside Wave 3:** L266 > L230 (Wave 3 start) AND L266 < L295 (Wave 4 start) ✓ — the new subsection is structurally nested inside Wave 3.
2. **After Step 4:** L266 > L264 (Step 4) ✓
3. **Before Exit criteria:** L266 < L278 (Wave 3 Exit criteria) ✓
4. **Same Wave 3 Exit criteria intact:** `**Exit criteria**:` still exists at L278 inside Wave 3 (verified by grep — multiple Exit criteria entries in the file, but L278 is the one belonging to Wave 3 by surrounding context).

## Verbatim context (2 lines before/after the new heading)

```
264 | 4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mark them as **competing**. If they all converge on one fix, mark as **consensus**.
265 |
266 | #### Tier 2 calibration completeness gate (hard precondition for report publishing)
267 |
268 | After all Tier 2 hypothesis cards are written and the calibrator subagents have been dispatched, the orchestrator MUST verify on disk:
```

## Conclusion

PASS — placement is correct: structurally inside Wave 3, after Step 4 (Distill candidate fixes) and before Exit criteria.
