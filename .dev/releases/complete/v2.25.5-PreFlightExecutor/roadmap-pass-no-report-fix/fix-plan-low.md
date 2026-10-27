# Fix Plan: LOW Severity Deviations (DEV-010, DEV-011)

**Roadmap**: `.dev/releases/current/v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/roadmap.md`
**Spec**: `.dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/pass-no-report-fix-spec.md`
**Fidelity Report**: `.dev/releases/current/v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/spec-fidelity.md`

---

## DEV-010 — Missing "before any code changes" Qualifier in SC-012

### Deviation Summary

The spec's §9 Acceptance Criteria checklist item reads:

> `- [ ] Pre-implementation baseline: \`uv run pytest tests/sprint/ -v\` passes **before any code changes**`

The roadmap's Success Criteria table at line 281 currently reads:

```
| SC-012 | Pre-implementation baseline green | P0 |
```

The temporal qualifier "before any code changes" is absent. This qualifier is semantically load-bearing: it establishes that the baseline must be captured in the pre-change state, not after any edits have been made. Without it, an implementer could run the test suite after beginning implementation and still satisfy the literal text of SC-012. The spec is explicit that this check is a pre-condition, not just a milestone marker.

### Root Cause

SC-012 was written as a shorthand description. The roadmap's prose in Phase 0 does correctly say "Execute `uv run pytest tests/sprint/ -v` and record pass/fail counts" but the success criteria table row dropped the temporal qualifier, creating a minor traceability gap between the table and the spec checklist.

### Recommended Fix

**File**: `roadmap.md`
**Location**: Success Criteria table, line 281
**Change type**: Single-cell text edit — no structural changes

**Before**:
```
| SC-012 | Pre-implementation baseline green | P0 |
```

**After**:
```
| SC-012 | Pre-implementation baseline green: `uv run pytest tests/sprint/ -v` passes before any code changes | P0 |
```

### Rationale

- Adds the "before any code changes" qualifier verbatim from spec §9, making the temporal constraint explicit in the validation table.
- Adds the exact command from the spec for direct traceability — a validator can match the SC-012 row against the spec checklist item without ambiguity.
- Does not alter the "P0" phase assignment, which is already correct (Phase 0 is the baseline validation phase).
- No other rows in the SC table are affected.
- The edit is minimal and self-contained — it only closes the traceability gap identified by DEV-010.

---

## DEV-011 — "phase-days" Timeline Unit Not Present in Spec

### Deviation Summary

The roadmap uses "phase-days" as a timeline estimation unit throughout:

- Phase headers: "Timeline: 0.25 phase-days", "Timeline: 0.5 phase-days", etc.
- Timeline Estimates table: "Total: 2.0 phase-days"

The spec (a patch specification) contains no timeline estimates at all.

### Decision: No Action Required

The spec-fidelity report explicitly states for DEV-011:

> "No action required. This is an acceptable roadmap addition not present in the spec."

This determination is correct for the following reasons:

1. **The spec is not a roadmap.** `pass-no-report-fix-spec.md` is a patch specification that defines what to build and how. It is not responsible for scheduling or effort estimation. A roadmap's role includes translating a spec into a phased plan with timing guidance; timeline estimates are an expected and appropriate roadmap-only artifact.

2. **No contradiction exists.** "Phase-days" does not conflict with any spec requirement. The spec contains no constraint that prohibits or limits timeline expressions in a derived roadmap.

3. **No implementation risk.** Timeline estimates are planning metadata. They do not affect the code to be written, the tests to be added, or the acceptance criteria to be verified. An implementer who ignores them is not non-compliant with the spec.

4. **The unit is self-consistent.** All four phase timelines sum correctly to the stated total (0.25 + 0.50 + 0.25 + 0.25 + 0.75 = 2.0 phase-days). There is no internal inconsistency to correct.

**Action**: None. The roadmap's timeline section is left unchanged.

---

## Implementation Checklist

The following checklist confirms both LOW deviations are addressed after applying the plan above:

- [ ] **DEV-010**: SC-012 row in the roadmap's Success Criteria table updated to read:
  `Pre-implementation baseline green: \`uv run pytest tests/sprint/ -v\` passes before any code changes`
- [ ] **DEV-010**: The "P0" phase assignment in SC-012 is unchanged
- [ ] **DEV-010**: No other rows in the Success Criteria table are modified
- [ ] **DEV-010**: The updated SC-012 text matches the spec §9 checklist item verbatim on the key qualifier ("before any code changes")
- [ ] **DEV-011**: No changes made to any timeline section, timeline table, or phase header in the roadmap
- [ ] **DEV-011**: No-action decision documented with rationale (this file)

### Verification Steps After Applying Fix

1. Search roadmap for `SC-012` — confirm the row contains "before any code changes"
2. Search roadmap for "phase-days" — confirm it still appears (no unintended deletions)
3. Confirm roadmap Success Criteria table has exactly 13 rows (SC-001 through SC-013) — unchanged row count confirms no accidental deletions or additions
4. Re-run spec-fidelity validation on the updated roadmap — DEV-010 and DEV-011 should both clear (DEV-010 resolved by edit; DEV-011 confirmed no-action)
