---
artifact: merge-log
pipeline: sc:adversarial
date: 2026-03-20
base_variant: V3
---

# Merge Execution Log

## Execution Summary

| Metric | Value |
|--------|-------|
| Base variant | V3 (turnledger-refactor-proposal-agent3.md) |
| Planned incorporations | 8 (INC-01 through INC-08) |
| Incorporations applied | 8 |
| Incorporations failed | 0 |
| Rejected alternatives | 6 (REJ-01 through REJ-06) |
| Unresolved conflicts | 0 |
| Provenance annotations | 28 (<!-- Source: ... --> comments) |

---

## Applied Changes

### INC-01: Cost Constant Calibration Framework (V1 -> V3 Section 4.5f)

**Status**: Applied.

**Location in merged output**: Section 4.5f ("Cost constant calibration"), under Section 4.5 Sprint Integration.

**What was done**: Added a new subsection defining wiring-specific cost constants (WIRING_ANALYSIS_TURNS, WIRING_REMEDIATION_TURNS) and derived budget ranges (MIN/STD/MAX_WIRING_BUDGET) following V1's NR-3 pattern. Values were adapted from V1's convergence-specific constants to wiring-gate-appropriate values. Preserved V1's architectural decision that constants are module-level integers, not config fields.

**Structural impact**: Additive. No existing V3 sections modified.

---

### INC-02: Dual-Guard Invariant Pattern (V1 -> V3 Sections 3.3, 7)

**Status**: Applied.

**Location in merged output**: Section 3.3 (Data Flow, final paragraph) and Section 7 (Risk Assessment, invariant note).

**What was done**: Added dual-guard invariant documentation at two locations: (1) inline in the data flow section where the guards are first encountered, (2) in the risk assessment section as a formal invariant statement. Both state that `wiring_gate_enabled` (structural) and `ledger.can_run_wiring_gate()` (economic) are independent guards.

**Structural impact**: Additive paragraphs within existing sections.

---

### INC-03: Pipeline Separation Analysis (V2 -> V3 Section 7.5)

**Status**: Applied.

**Location in merged output**: New Section 7.5 ("TurnLedger Sections That Do Not Affect Wiring Gate").

**What was done**: Created a boundary table modeled on V2's Section 7 format, adapted for wiring gate context. Lists 6 TLD sections that are irrelevant to the wiring gate with per-section rationale. Added a summary sentence directing implementers to the 4 relevant TLD sections.

**Structural impact**: New subsection under Section 7.

---

### INC-04: Enforcement Tier Dual-Mode Semantics (V2 -> V3 Sections 4.5g, 5 C2 resolution)

**Status**: Applied.

**Location in merged output**: New Section 4.5g ("Enforcement tier semantics") and enriched C2 resolution in Section 5.

**What was done**: Added a note articulating the intrinsic-vs-runtime distinction for enforcement tiers. The gate definition's enforcement properties are intrinsic; the runtime mode is determined by `resolve_gate_mode()`. This framing from V2's CONFLICT-01 resolution was applied to V3's C2 resolution as well, enriching the existing `enforcement_mode_label` mapping with architectural context.

**Structural impact**: New subsection 4.5g. Modified C2 resolution paragraph in Section 5.

---

### INC-05: Remediation Retry Model Distinction (V2 -> V3 Section 4.5e, NEW-2)

**Status**: Applied.

**Location in merged output**: Section 4.5e ("Remediation path") and NEW-2 in Section 3.

**What was done**: Added explicit statement that `attempt_remediation()` re-runs the upstream task subprocess, not the deterministic gate check. This is V2's key architectural insight from CONFLICT-02 resolution. Applied in two locations: the sprint integration section (4.5e) and the new sections summary (NEW-2).

**Structural impact**: New subsection 4.5e under Sprint Integration. Additional paragraph in NEW-2.

---

### INC-06: GateCriteria Canonical Location (V2 -> V3 Sections 4.4, 11)

**Status**: Applied.

**Location in merged output**: Section 4.4 (Gate Definition) and Section 11 (Dependency Map).

**What was done**: Added canonical type location notes confirming `GateCriteria`, `SemanticCheck`, and `gate_passed()` live in `pipeline/gates.py`. Gate instances import from there. Applied to both the gate definition section and the dependency map section.

**Structural impact**: Additive notes within existing sections.

---

### INC-07: Line-Level Evidence Citations (V1 -> V3 Conflicts C1-C5)

**Status**: Applied.

**Location in merged output**: Sections 4 (Conflicts C1-C5) and corresponding Section 9.2 (C3).

**What was done**: Added "Evidence" lines to each conflict citing specific sections and line references in both the original spec and design.md. Follows V1's pattern of structured evidence citations per conflict.

**Structural impact**: Additional lines within existing conflict descriptions.

---

### INC-08: DeferredRemediationLog Awareness (V2 -> V3 Section 4.5e, NEW-2)

**Status**: Applied.

**Location in merged output**: Section 4.5e and NEW-2.

**What was done**: Added a brief note that unresolved wiring gate failures are recorded in `DeferredRemediationLog` for cross-phase persistence, resume recovery, and KPI feed. Kept as a pointer to TLD Section 4 rather than a full specification.

**Structural impact**: Additional sentence in 4.5e and NEW-2.

---

## Structural Integrity Validation

### Section Count

| Section | Present | Consistent Numbering |
|---------|---------|---------------------|
| Overview | Yes | -- |
| 1. Section-by-Section Diff Summary | Yes | OK |
| 2. Exact Section/Requirement IDs Affected | Yes | OK |
| 3. New Sections Introduced | Yes | OK |
| 4. Risks and Conflicts | Yes | OK |
| 5. Recommended Resolutions | Yes | OK |
| 6. Implementation Order | Yes | OK |

### New Subsections Added

| Subsection | Parent | Source |
|------------|--------|--------|
| 3.3 dual-guard paragraph | Section 3.3 | V1 U-002 |
| 4.4 canonical location note | Section 4.4 | V2 CONFLICT-04 |
| 4.5e (Remediation path) | Section 4.5 | V2 CONFLICT-02, V2 U-005 |
| 4.5f (Cost constant calibration) | Section 4.5 | V1 NR-3 |
| 4.5g (Enforcement tier semantics) | Section 4.5 | V2 CONFLICT-01 |
| 7 invariant note | Section 7 | V1 U-002 |
| 7.5 (Pipeline boundary) | Section 7 | V2 Section 7 |
| 11 canonical location note | Section 11 | V2 CONFLICT-04 |

### Cross-Reference Integrity

All internal references checked:
- C1 through C5 in Section 4 have corresponding resolutions in Section 5: OK
- SC-012 through SC-015 in Section 10 map to TurnLedger capabilities in Sections 4.5, NEW-1 through NEW-5: OK
- Task IDs (T01b, T01c, T06b, T07b, T10b) in Section 12 have descriptions and dependency chains: OK
- Critical path references all task IDs in correct dependency order: OK
- Section 7.5 references point to TLD sections that exist in design.md: OK

### Provenance Coverage

All 8 incorporations have at least one `<!-- Source: ... -->` annotation in the merged output. Total provenance comments: 28. All V3 base sections also have provenance annotations.
