# Check (c) — 4 MUST / MUST NOT / NEVER Statements Review

**Verdict:** PASS
**Date:** 2026-05-27

## All 4 statements (byte-exact `grep -F` matches)

| # | Statement (verbatim, fixed-string) | Line found | Inside new subsection (L266-L277)? |
|---|-----------------------------------|-----------|------------------------------------|
| 1 | `the orchestrator MUST verify on disk` | 268 | yes ✓ |
| 2 | `MUST exist and parse as a Calibration Report` | 270 | yes ✓ |
| 3 | `the orchestrator MUST NOT publish` (paired with `REPORT.md`) | 271 | yes ✓ |
| 4 | `Self-reported confidence is NEVER passed through unmodified.` | 274 | yes ✓ |

## Scoping verification

The new subsection spans L266 (`#### Tier 2 calibration completeness gate...`) to L277 (last non-blank line before `**Exit criteria**:` at L278). All 4 statement matches fall in the range [L268, L274], strictly inside the new subsection.

## Case sensitivity

`grep -F` (fixed string) used — byte-exact case-sensitive matches:
- `MUST` (all uppercase) appears 2× (L268, L270) ✓
- `MUST NOT` (all uppercase, space-separated) appears 1× (L271) ✓
- `NEVER` (all uppercase) appears 1× (L274) ✓

## Conclusion

PASS — all 4 obligation statements are present verbatim inside the new subsection with correct uppercase semantic markers.
