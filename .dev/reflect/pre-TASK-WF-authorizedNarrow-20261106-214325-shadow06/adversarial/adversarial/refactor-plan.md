# Refactor Plan (Step 4)

## Overview
- Base: V3 (refactorer card)
- Incorporated variants: V1 (3 findings), V2 (1 resolution)
- Planned changes: 4
- Risk: Low (additive merges into the base's findings sections; no restructuring)

## Planned Changes
1. Incorporate V1 F2 as merged finding M-002 (constraint without AC): append to base findings with tasklist:21 vs :31 citations, severity MINOR (debate: unanimous U-005->V1), category missing-requirement. Integration: append after base F1. Rationale: V2 conceded "binding constraint establishes coverage, not verification". Risk: Low.
2. Incorporate V1 F1 as merged finding M-004 (bash-only limit unsourced): severity MINOR, category other. Rationale: unanimous both rounds (U-004). Risk: Low.
3. Incorporate V1 F5 as merged finding M-006 (undefined pass criteria): severity LOW->MINOR, category other. Rationale: V2 changed to V1 in R2. Risk: Low.
4. Apply V2's X-001 resolution to base's view of T2.AC5: record as a note (not a finding) that "official updatedInput contract" implies an outside reference the AC does not name; residual severity MINOR under category other (names no reference artifact). V1's circularity claim is withdrawn. Risk: Low.

Severity harmonization (schema): MEDIUM->MAJOR, LOW->MINOR.
Base F1 (plugin mirror steps omitted): stays MAJOR non-blocking (debate-corrected C-001; original card MEDIUM; blocking=false unchanged).
Base F2 (staging wording): MINOR non-blocking (LOW-MEDIUM after tasklist:66 narrowing).
Base F3 (interim verify-sync window): RECORDED-BUT-REJECTED as a defect — debate resolved U-002 to V2 (sequencing, not defect). Kept as a plan note, not a finding.
Base F4 (launcher half): RECORDED-BUT-REJECTED as a defect — U-003 to V2 (plan:15/:79 expressly scope a foundation). Kept as a plan note, not a finding.

## Changes NOT Being Made
- V1's F4 circularity claim: rejected (X-001->V2; "official" implies outside contract; V1 withdrew).
- V2's zero-defect stance: rejected as the merge frame (conceded by V2 in R2 items 1-6).
- U-002 and U-003 as findings: rejected by majority (kept as notes).
- INV-002/003/006/008 (LOW unaddressed invariants): recorded in invariant-probe.md; not merged (no severity change).

## Risk Summary
All changes additive; no base finding weakened; severities only harmonized to the schema vocabulary.

## Review Status
Auto-approved (non-interactive).
