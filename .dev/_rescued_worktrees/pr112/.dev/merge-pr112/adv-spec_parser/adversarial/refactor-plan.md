# Refactoring Plan

## Overview
- Base variant: V1 (proposed_hybrid)
- Incorporated variants: none required (V1 already unions V2's SoT table + V3's span-aware dedup)
- Change count: 0 structural changes to base; this is a confirmation that V1 IS the merged artifact
- Overall risk: Low

## Planned Changes
None. The selected base (V1) already represents the optimal union. No content from V2 or V3 needs to be
merged in, because:
- V2's only differentiator (`_MD_TRAILING_D_RE` + value-global dedup) is a defect and is deliberately
  EXCLUDED.
- V3's differentiator (span-aware dedup) is already present in V1.
- V3's hardcoded table is rejected in favor of V1's contracts-sourced table (byte-identical patterns,
  superior SoT posture).

## Changes NOT Being Made (rejected alternatives)

| Diff Point | Rejected approach | Rationale |
|------------|-------------------|-----------|
| S-001 | V3 hardcoded 6-pattern table | Duplicates contract bodies → SoT drift risk (Contract #8). V1's comprehension compiles to identical patterns. |
| C-001 | V2 value-global dedup | Drops legitimate standalone `D01`; fails master test `test_md_family_does_not_collapse_bare_d`. |
| C-002 | Keep V2's `_MD_TRAILING_D_RE` helper | Unnecessary once span-aware dedup is adopted; it re-derives the `D-?\d+` body as a local literal. |

## Risk Summary

| Item | Risk | Impact | Mitigation |
|------|------|--------|------------|
| A-001 dependency on `"MD"` key in `ID_PATTERNS` | Low | KeyError if MD removed from contracts | Fail-loud is desired (master:§Flaw 4 no fail-open); `id_registry` shares the same coupling |
| Test pinning old (value-global) semantics | DISCHARGED | n/a | Verified: master test asserts span-aware behavior; V1 passes both MD tests empirically |

## Review Status
Auto-approved (non-interactive).
