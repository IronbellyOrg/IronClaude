# Check (e) — Verification Command Pattern Review

**Verdict:** PASS
**Date:** 2026-05-27

## Verification command line (L276, verbatim)

> `Verification command (run before publishing): for each `tier2-*-hypothesis.md` (excluding `*-calibration.md`), assert a matching `*-calibration.md` exists and contains the Calibration Report markers (`# Calibration Report`, `## Per-dimension scores`, `## Confidence`, `## Escalation recommendation`, `**Verdict**: STOP|ESCALATE`, `**Calibrated (this report)**:` with a parseable float) — failure triggers the three-step ladder above.`

## Required components checklist

| Component | Required | Present? |
|-----------|----------|---------|
| Paragraph starts with `Verification command (run before publishing)` | yes | ✓ |
| Appears exactly once inside the new subsection | yes | ✓ (single match at L276) |
| Iterates over `tier2-*-hypothesis.md` (excluding `*-calibration.md`) | yes | ✓ |
| Asserts matching `*-calibration.md` sibling exists | yes | ✓ |
| Failure triggers the three-step ladder above | yes | ✓ |

## Calibration Report markers checklist (research-02 §8)

| # | Marker | Present in line? |
|---|--------|-----------------|
| 1 | `# Calibration Report` | ✓ |
| 2 | `## Per-dimension scores` | ✓ |
| 3 | `## Confidence` | ✓ |
| 4 | `## Escalation recommendation` | ✓ |
| 5 | `**Verdict**: STOP\|ESCALATE` | ✓ |
| 6 | `**Calibrated (this report)**:` with parseable float | ✓ |

All 6 markers are present (5 mandatory + 1 with parseable-float check); minimum threshold of 5 is exceeded.

## Conclusion

PASS — verification command paragraph present, iteration / assertion / failure-handling all encoded, and all 6 Calibration Report markers enumerated.
