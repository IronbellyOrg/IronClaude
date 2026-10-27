---
high_severity_count: 2
medium_severity_count: 5
low_severity_count: 4
total_deviations: 11
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Spec §12 lists 8 recommended new tests (Crispin, Round 3) but the roadmap only includes 6 new tests. Two tests are missing: `test_timeout_at_100_turns` (NFR-004 verification) and the split boundary tests `test_rate_boundary_zero` / `test_rate_boundary_near_one` which were consolidated into a single `test_rate_boundary_validation` without covering all specified scenarios.
- **Spec Quote**: "| `test_timeout_at_100_turns` | Unit | Verify timeout = 12,300s | P2 |" and "| `test_rate_boundary_zero` | Boundary | rate=0.0 → zero reimbursement, all tasks cost full turns | P2 |" and "| `test_rate_boundary_near_one` | Boundary | rate=0.99 → high reimbursement but still decays | P2 |"
- **Roadmap Quote**: The roadmap's Phase 4 deliverables (D3.5–D3.10) list only 6 new tests. `test_timeout_at_100_turns` is entirely absent. The two boundary tests are merged into D3.10 `test_rate_boundary_validation` with "rate=0.0, 0.99, 1.0(rejected), -0.1(rejected)".
- **Impact**: NFR-004 (`phase timeout SHALL be 12,300s`) has no corresponding test deliverable in the roadmap. The timeout computation is a key behavioral change (6,300s → 12,300s) and omitting its verification test risks shipping an unvalidated NFR. The boundary test consolidation is acceptable (covers the same cases) but the timeout test is a genuine omission.
- **Recommended Correction**: Add D3.11 `test_timeout_at_100_turns` to Phase 4 deliverables, verifying `100 × 120 + 300 = 12,300s`. Update total new tests from 6 to 7. Update total_deliverables in frontmatter from 33 to 34.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: The spec's §6.5 specifies 3 Tier 4 spec documentation edits, but the roadmap's M4 deliverable D4.3 omits the spec §3.4 title change from "The 90% Reimbursement Rate" to "The 80% Reimbursement Rate".
- **Spec Quote**: "| `unified-spec-v1.0.md` | §3.4 title | 'The 90% Reimbursement Rate' | 'The 80% Reimbursement Rate' |"
- **Roadmap Quote**: "| D4.2 | Update `unified-spec-v1.0.md` §3.1 → `rate = 0.80` | Line 178 corrected |" and "| D4.3 | Update `unified-spec-v1.0.md` §3.4 proof → rate=0.80 math | Lines 225-235 corrected with 4 turns/task, 184 drain |" — no deliverable for the §3.4 title change.
- **Impact**: The roadmap has 2 deliverables covering 3 spec edits, but the section title rename is not explicitly tracked. An implementer following the roadmap would update the math but leave the section titled "The 90% Reimbursement Rate", creating spec-internal inconsistency — the exact kind of drift this release is meant to fix.
- **Recommended Correction**: Either add D4.5 for the §3.4 title change, or expand D4.3's acceptance criteria to explicitly include "§3.4 title updated to 'The 80% Reimbursement Rate'".

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: The spec §5 defines 5 safety constraints (SC-001 through SC-005) but the roadmap's Success Criteria section reuses the ID namespace `SC-001` through `SC-007` for success criteria, creating an ID collision with the spec's safety constraints.
- **Spec Quote**: "| SC-001 | `reimbursement_rate` MUST be in range `(0.0, 1.0)` exclusive | Runtime validation in TurnLedger (existing) |"
- **Roadmap Quote**: "| SC-001 | All 12 source edits applied and verified | M1, M2, V1 | Yes | 3 |"
- **Impact**: Ambiguity when referencing "SC-001" — it could mean the safety constraint (rate range validation) or the roadmap success criterion (source edits verified). Could cause confusion during implementation reviews and traceability audits.
- **Recommended Correction**: Rename the roadmap's success criteria to use a distinct prefix (e.g., `RC-001` through `RC-007` for "Release Criteria") to avoid collision with the spec's `SC-NNN` safety constraints.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: The spec §9 Guard Condition Boundary Table identifies 3 gap findings (FR-GAP-001, FR-GAP-002, FR-GAP-003) requiring verification or documentation, but the roadmap does not include explicit deliverables to address FR-GAP-001 (verify SC-001 enforcement) or FR-GAP-002 (negative rate validation).
- **Spec Quote**: "**MAJOR (FR-GAP-001)**: `reimbursement_rate` valid range `(0.0, 1.0)` exclusive should be enforced at construction time. SC-001 states this but enforcement must be verified." and "**MAJOR (FR-GAP-002)**: Negative `reimbursement_rate` and `rate > 1.0` produce incorrect behavior. Validation needed."
- **Roadmap Quote**: The roadmap includes R-009 ("rate=1.0 boundary not enforced strictly") and D3.10 (`test_rate_boundary_validation`) which partially addresses this, but there is no explicit deliverable to *verify* that existing SC-001 enforcement is correct, nor to add validation for negative rates if it's missing.
- **Impact**: The boundary test (D3.10) tests rate=0.0, 0.99, 1.0, -0.1 — which covers the test side. However, if the runtime validation in TurnLedger doesn't actually reject these values, the test would reveal the gap but the roadmap has no deliverable to *fix* it. The spec's FR-GAP findings imply verification + potential remediation.
- **Recommended Correction**: Add a verification deliverable in Phase 3 (V1) or Phase 4 (M3) to confirm TurnLedger constructor validates `0.0 < rate < 1.0`. If validation is missing, add a remediation deliverable.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: The spec §5 SC-005 recommends adding documentation noting the 3.4hr max per phase, marked as "NEW RECOMMENDATION". The roadmap mentions documenting timeout in CHANGELOG (R-002 mitigation) but has no explicit deliverable for SC-005.
- **Spec Quote**: "| SC-005 | Phase timeout MUST NOT exceed system-configured maximum | **NEW RECOMMENDATION**: Add documentation noting 3.4hr max per phase |"
- **Roadmap Quote**: "| R-002 | Phase timeout at 3.4h may surprise users | M4 | Low | Low | Document in CHANGELOG and release notes | scribe |" — risk mitigation only, no tracked deliverable.
- **Impact**: The timeout documentation may be implicitly covered by the CHANGELOG entry (D4.1), but it's not an explicit acceptance criterion. An implementer could write the CHANGELOG without mentioning the timeout change.
- **Recommended Correction**: Add acceptance criteria to D4.1 requiring the CHANGELOG entry to mention the phase timeout increase (6,300s → 12,300s / 3.4 hours).

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: The spec §10 provides a specific recommended note text for the spec-implementation alignment update, but the roadmap's D4.2/D4.3 deliverables don't reference this note or include it as an acceptance criterion.
- **Spec Quote**: "**Recommendation**: Update the spec to reflect 0.8 as the **current implemented value**. Add a note: `NOTE: The original design target was 0.90 (v1.0 spec). The implementation shipped at 0.50 due to conservative initial calibration...`"
- **Roadmap Quote**: "| D4.2 | Update `unified-spec-v1.0.md` §3.1 → `rate = 0.80` | Line 178 corrected |" — no mention of the recommended contextual note.
- **Impact**: Without the historical context note, future readers of the spec won't understand why 0.80 was chosen over the original 0.90 design target. The panel consensus was unanimous that this context is important.
- **Recommended Correction**: Add acceptance criteria to D4.2 or D4.3 requiring the historical context note from §10 to be included in the spec update.

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: The spec §8 Round 3 (Janet Gregory) recommends including a test matrix in the CHANGELOG showing before/after behavior for three scenarios (rate=0.5, 0.8, 0.9). The roadmap's D4.1 acceptance criteria only says "Entry matches spec §11 template" but §11 doesn't include a test matrix.
- **Spec Quote**: "**Recommendation**: Include a test matrix in the CHANGELOG showing before/after behavior for the three key scenarios (46-task sprint at 0.5, 0.8, 0.9)."
- **Roadmap Quote**: "| D4.1 | CHANGELOG entry for v2.0.0 with migration guide | Entry matches spec §11 template |"
- **Impact**: The Gregory recommendation is a SHOULD-level quality practice, not a MUST. However, the spec §11 CHANGELOG template already includes a "Budget Guidance" section, so the roadmap's acceptance criteria would pass without the test matrix. Minor quality gap.
- **Recommended Correction**: Add the test matrix to D4.1 acceptance criteria or note it as optional enhancement.

### DEV-008
- **ID**: DEV-008
- **Severity**: LOW
- **Deviation**: The spec §13 states total edit count is 19 (7 + 5 + 4 + 3) plus 6 new tests. The roadmap frontmatter states `total_deliverables: 33`. The actual roadmap deliverable count is 7 + 5 + 3 + 10 + 4 + 4 = 33, which matches the frontmatter but doesn't map 1:1 to the spec's 19 edits + 6 tests = 25 work items — the difference is the 8 validation deliverables (V1 and V2 phases) which the spec doesn't count.
- **Spec Quote**: "| **Total** | | **19** | **Low** | Plus 6 new tests to add."
- **Roadmap Quote**: "total_deliverables: 33"
- **Impact**: No correctness issue — the roadmap correctly adds validation deliverables beyond the spec's edit count. The difference is organizational, not functional.
- **Recommended Correction**: None needed. The roadmap's higher count reflects validation phases that are additive to the spec's requirements.

### DEV-009
- **ID**: DEV-009
- **Severity**: LOW
- **Deviation**: The roadmap adds two risks not present in the spec's §7 Risk Register: R-008 (DRY violation in 5-location defaults) and R-009 (rate=1.0 boundary not enforced strictly). These are additive, not contradictory.
- **Spec Quote**: §7 Risk Register contains R-001 through R-007.
- **Roadmap Quote**: Risk Assessment contains R-001 through R-009 with R-008 and R-009 added.
- **Impact**: Positive deviation — the roadmap surfaces risks identified in the panel review (Fowler's DRY observation, Whittaker's boundary attack) that the spec's risk register didn't capture as formal risk entries.
- **Recommended Correction**: None needed. Consider back-porting R-008 and R-009 to the spec for completeness.

### DEV-010
- **ID**: DEV-010
- **Severity**: LOW
- **Deviation**: The spec frontmatter path referenced in the roadmap's YAML frontmatter is incorrect. The roadmap says `spec_source: ".dev/releases/current/unified-audit-gating-v2/..."` but the spec is located at `.dev/releases/complete/unified-audit-gating-v2/...`.
- **Spec Quote**: N/A (file path issue)
- **Roadmap Quote**: `spec_source: ".dev/releases/current/unified-audit-gating-v2/unified-audit-gating-v2.0-spec.md"`
- **Impact**: Broken reference — the spec_source path points to a non-existent location. Tooling that validates spec_source would fail.
- **Recommended Correction**: Update `spec_source` to `.dev/releases/complete/unified-audit-gating-v2/unified-audit-gating-v2.0-spec.md`.

### DEV-011
- **ID**: DEV-011
- **Severity**: LOW
- **Deviation**: The spec §1.2 states "All edits are simple value replacements across 7 source locations and 4 test assertions" but §2 later expands to 12 source locations (after panel review). The roadmap correctly uses the expanded 12 count. The spec's §1.2 is internally inconsistent with its own §6, but the roadmap aligns with the final/complete count.
- **Spec Quote**: "All edits are simple value replacements across 7 source locations and 4 test assertions." (§1.2)
- **Roadmap Quote**: "The release involves 12 source edits across Python and shell files, 4 test assertion updates, 6 new tests" (Executive Summary)
- **Impact**: No roadmap error — this is a spec-internal inconsistency that the roadmap resolves correctly by using the panel-updated count.
- **Recommended Correction**: None for roadmap. The spec's §1.2 should be updated to reflect 12 source locations.

## Summary

| Severity | Count | Details |
|----------|-------|---------|
| HIGH | 2 | Missing `test_timeout_at_100_turns` test (DEV-001); Missing §3.4 title rename deliverable (DEV-002) |
| MEDIUM | 5 | SC-ID collision (DEV-003); FR-GAP verification gaps (DEV-004); SC-005 timeout doc (DEV-005); Missing historical context note (DEV-006); Missing test matrix recommendation (DEV-007) |
| LOW | 4 | Deliverable count difference (DEV-008); Additive risks (DEV-009); Incorrect spec_source path (DEV-010); Spec-internal §1.2 inconsistency (DEV-011) |

**Overall assessment**: The roadmap is a faithful translation of the spec with strong traceability across all 12 FRs and 8 NFRs. The two HIGH deviations are both omissions of spec-required deliverables — `test_timeout_at_100_turns` for NFR-004 and the §3.4 section title rename. Both are straightforward to correct. The MEDIUM deviations are primarily insufficient detail in acceptance criteria rather than fundamental misalignment. The roadmap is **not tasklist-ready** until the two HIGH deviations are resolved.
