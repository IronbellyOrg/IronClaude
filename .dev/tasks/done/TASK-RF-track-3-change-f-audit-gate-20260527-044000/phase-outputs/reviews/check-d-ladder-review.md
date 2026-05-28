# Check (d) — 3-Step Retry-Then-Force-Degrade Ladder Review

**Verdict:** PASS
**Date:** 2026-05-27

## Ladder steps (verbatim from L272-L274)

| Step | Line | Required content | Verbatim quote | Present? |
|------|------|------------------|----------------|---------|
| 1 (Log) | 272 | Append `calibration: missing` to `audit.log` with absolute card path | `1. Log \`calibration: missing\` for each missing sibling in \`audit.log\` with the absolute card path.` | yes ✓ |
| 2 (Retry-once) | 273 | One re-dispatch of `confidence-calibrator` `Task`, 2-minute wall-clock wait, explicit no-third-retry | `2. Re-dispatch the \`confidence-calibrator\` \`Task\` once for the missing card with the same inputs. Wait up to 2 minutes wall-clock for completion. If the retry does not produce a parseable Calibration Report within that window, proceed to the force-degrade step. Do not attempt a third retry.` | yes ✓ |
| 3 (Force-degrade) | 274 | `min(self_reported, 0.65)` + `calibration_status: failed_to_calibrate` annotation + handling of missing/null/non-numeric/out-of-range `self_reported` (default `0.0`, clamp into `[0.0, 1.0]` first) | `3. If retry still fails, write the card into \`REPORT.md\` with confidence force-degraded to \`min(self_reported, 0.65)\` ... If \`self_reported\` is missing, null, non-numeric, or outside \`[0.0, 1.0]\`, default to \`0.0\` (the most pessimistic safe value); clamp out-of-range numeric values into \`[0.0, 1.0]\` first, then apply the floor. Annotate \`audit.log\` with \`calibration: force_degraded card=<path> self_reported=<value\|missing\|non-numeric\|out-of-range> floored=0.65 calibration_status=failed_to_calibrate\`. ...` | yes ✓ |

## Order verification (file line order)

- Step 1 at L272 < Step 2 at L273 < Step 3 at L274 ✓ (correct order: log → retry-once → force-degrade)

## Retry cap

Step 2 contains the explicit prohibition `Do not attempt a third retry.` ✓ — satisfies the "one retry only" invariant from research-01 §5.

## Edge-case handling in Step 3

Step 3 explicitly handles ALL four edge cases per research-02 §10:

1. **Missing / null** `self_reported` → default `0.0` ✓
2. **Non-numeric** `self_reported` → default `0.0` ✓
3. **Outside `[0.0, 1.0]`** (out-of-range) → clamp first, then apply floor ✓
4. **In-range numeric** → apply `min(self_reported, 0.65)` directly (implicit; default behavior) ✓

The audit-log annotation `calibration: force_degraded card=<path> self_reported=<value|missing|non-numeric|out-of-range> ...` records which case triggered.

## Conclusion

PASS — all 3 ladder steps present, ordered correctly, retry capped at one, and all edge cases for `self_reported` handled.
