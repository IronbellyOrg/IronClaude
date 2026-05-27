# Check (g) — Force-Degrade Math + Annotation Review

**Verdict:** PASS
**Date:** 2026-05-27

## `grep -F` matches

### String 1: `min(self_reported, 0.65)`

**Matches:**
- L274 — `... force-degraded to \`min(self_reported, 0.65)\` ...` (Step 3 of ladder — force-degrade math)
- L274 — Also appears in the Grounding Gaps prose phrasing within the same line — `... — confidence force-degraded to min(self_reported, 0.65); calibration_status: failed_to_calibrate.`
- L276 — Inside the `Verification command` paragraph (referenced indirectly via the three-step-ladder pointer; not directly using the math literal, but the ladder pointer reads "failure triggers the three-step ladder above" which contains it).

**Net match locations inside new subsection (L266-L277):** L274 contains the math literal `min(self_reported, 0.65)` in BOTH the force-degrade instruction AND the Grounding Gaps prose phrasing (both inside Step 3 of the ladder, single line).

### String 2: `calibration_status: failed_to_calibrate`

**Matches:**
- L274 — In the audit-log annotation portion: `... floored=0.65 calibration_status=failed_to_calibrate` (note: `=` separator in audit-log key-value pairs, consistent with research-02 §6 audit-log idiom)
- L274 — In the Grounding Gaps prose: `calibration_status: failed_to_calibrate.` (note: `:` separator in prose form, matching the spec wording)

Both forms (`=` for audit-log key-value, `:` for prose annotation) appear on L274.

## Pairing in Step 3

The force-degrade math (`min(self_reported, 0.65)`) and the `calibration_status: failed_to_calibrate` annotation BOTH appear on **L274**, which is Step 3 of the ladder (the force-degrade step). They are NOT separated across the subsection — they share a single line / paragraph in the same ladder step.

## Surrounding context (L272-L276)

```
272 |   1. Log `calibration: missing` for each missing sibling in `audit.log` with the absolute card path.
273 |   2. Re-dispatch the `confidence-calibrator` `Task` once for the missing card with the same inputs. ... Do not attempt a third retry.
274 |   3. If retry still fails, write the card into `REPORT.md` with confidence force-degraded to `min(self_reported, 0.65)` ... Annotate `audit.log` with `calibration: force_degraded card=<path> self_reported=<value|missing|non-numeric|out-of-range> floored=0.65 calibration_status=failed_to_calibrate`. Add a prose line to the Grounding Gaps section of `REPORT.md` reading `Hypothesis card from <agent> could not be calibrated after one retry — confidence force-degraded to min(self_reported, 0.65); calibration_status: failed_to_calibrate.` Self-reported confidence is NEVER passed through unmodified.
275 |
276 | Verification command (run before publishing): ...
```

Both math and annotation are paired with the force-degrade step (Step 3), not used in unrelated context.

## Conclusion

PASS — `min(self_reported, 0.65)` and `calibration_status: failed_to_calibrate` both appear inside the new subsection (L274), paired in Step 3 of the ladder as required.
