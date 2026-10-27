# Refactoring Plan: Merged Delta Analysis Review

## Overview

- **Base variant**: Variant 2 (opus:analyzer — Forensic Analyst Validation)
- **Incorporated variants**: Variant 1 (opus:architect), Variant 3 (sonnet:scribe)
- **Planned changes**: 12
- **Rejected changes**: 3
- **Overall risk**: Medium (additive changes to base structure; no base-weakening modifications)

---

## Planned Changes

### Change #1: Add NR-3 reclassification
- **Source**: Variant 1, Section "NR-3 -- deviation-analysis as audit prerequisite" + Round 3 INV-005 resolution
- **Target**: Base Section 2 (Severity Classification) and new Appendix section
- **Rationale**: Round 3 invariant probe (INV-005) confirmed no §5.1-§5.3 rule references deviation-analysis.md. Architect's position prevailed (92% confidence). NR-3 must be downgraded from core finding to recommended spec amendment.
- **Integration approach**: Add severity reclassification row for NR-3. Add new "Recommended Spec Amendments" appendix section at end of document.
- **Risk**: Low (additive)

### Change #2: Add NR-5/NR-6 merge note
- **Source**: Variant 1, "NR-5/NR-6 duplicate identification" + Round 2 convergence
- **Target**: Base Sections covering NR-5 and NR-6
- **Rationale**: All three advocates agreed (90% confidence) these describe the same requirement from different angles. Architect identified correctly; Analyzer conceded in R2.
- **Integration approach**: Add consolidation note indicating these should be treated as one finding with two implementation facets (reactive invalidation + proactive binding).
- **Risk**: Low (annotation only)

### Change #3: Incorporate corrected §4.4 replacement language
- **Source**: Variant 3, Section 3.1 (§4.4 Replacement Text — Detailed Critique), all improved language blocks
- **Target**: New section in merged output after the base's Section 3 (Spec Update Language Verification)
- **Rationale**: Variant 3 is the only variant providing directly actionable corrected spec language. Rated HIGH value (U-005). Universal agreement that line citations must be removed; Scribe's corrected versions do this.
- **Integration approach**: Add new "Corrected Spec Language Recommendations" section incorporating all improved §4.4 item texts.
- **Risk**: Medium (requires careful integration to avoid contradicting base's verification findings)

### Change #4: Add missing acceptance criteria catalogue
- **Source**: Variant 3, Section 7 (Missing Acceptance Criteria), full 10-item table
- **Target**: New section in merged output
- **Rationale**: Rated HIGH value (U-006). No other variant provides this systematic catalogue. Directly actionable for spec editors.
- **Integration approach**: Add new "Missing Acceptance Criteria" section with the 10-item table.
- **Risk**: Low (additive)

### Change #5: Add undefined terms list
- **Source**: Variant 3, Section 5.1 and Section 8.2 (6 undefined terms)
- **Target**: New subsection within the merged spec language section
- **Rationale**: Variant 3 systematically identified AuditLease, audit_lease_timeout, max_turns, Critical Path Override, audit_gate_required, audit_attempts as introduced without §3.1 canonical definitions. Universal agreement this is a gap.
- **Integration approach**: Add "Undefined Terms Requiring §3.1 Definitions" subsection.
- **Risk**: Low (additive)

### Change #6: Add missing spec sections to update table
- **Source**: Variant 3, Section 6 (Missing Coverage — §5.2, §7.2, §8, §10.3)
- **Target**: Integrated into base's findings or as a new section
- **Rationale**: Rated MEDIUM value (U-007). Four spec sections affected by delta changes but not in the original update table.
- **Integration approach**: Add "Additional Spec Sections Requiring Updates" subsection.
- **Risk**: Low (additive)

### Change #7: Add §4.4 item 7 placement correction
- **Source**: Variant 3, Section 3.1 (item 7 critique) + Round 2 convergence
- **Target**: Base's NR-4 / reimbursement_rate section
- **Rationale**: All agree §4.4 item 7 is a governance directive misplaced in normative timeout/retry section. Should move to §12.3/§12.4. Confidence: 85%.
- **Integration approach**: Add placement recommendation annotation.
- **Risk**: Low (annotation)

### Change #8: Add NR-1 determinism reframing
- **Source**: Variant 1, "NR-1 -- determinism argument" + Round 1 analysis
- **Target**: Base's NR-1 assessment or severity table
- **Rationale**: Architect correctly identified that "breaks determinism" is wrong — runtime derivation from same inputs is equally deterministic. Real value is auditability/transparency. Confidence: 85%.
- **Integration approach**: Add note qualifying the determinism claim.
- **Risk**: Low (annotation)

### Change #9: Add revised phase ordering proposal
- **Source**: Variant 1 Section 5 + Round 2 convergence + INV-001 resolution
- **Target**: Base's Section 5 (Implementation Feasibility)
- **Rationale**: All three advocates agreed phase ordering is problematic. Architect proposed P0/P1/P2a/P2b/P3. INV-001 adds branch (a)/(b) conditional. Merged ordering needed.
- **Integration approach**: Replace base's Phase Ordering assessment with consensus-derived ordering including branch decision framework.
- **Risk**: Medium (modifies base content rather than adding)

### Change #10: Add MF-1 branch decision framework
- **Source**: Round 3 INV-001 resolution (Scribe's framing adopted)
- **Target**: Base's MF-1 section or new prominent section
- **Rationale**: INV-001 resolution: branch (a) as default, conditional block for branch (b) no-ops. This is the single most important structural addition.
- **Integration approach**: Add "MF-1 Resolution: Branch Decision Framework" as a prominent subsection, listing which findings are conditional on branch (a) vs always-applicable.
- **Risk**: Medium (structural addition that affects interpretation of multiple findings)

### Change #11: Add NR-2 severity upgrade
- **Source**: Variant 3, Section 2.1 (LOW → MEDIUM)
- **Target**: Base's severity table
- **Rationale**: Scribe argued correctly: silent acceptance of stale bundles missing audit_gate_required = correctness risk per §5.2 "Unknown/missing deterministic inputs => failed."
- **Integration approach**: Update severity in base's LOW section.
- **Risk**: Low (single cell change)

### Change #12: Add GateDisplayState characterization correction
- **Source**: Round 2 consensus ("formally a state machine, operationally inert")
- **Target**: Base's Delta 2.7 section
- **Rationale**: All agree "UI ornament" understates the design intent. Transition constraints exist.
- **Integration approach**: Add qualification to base's characterization.
- **Risk**: Low (annotation)

---

## Changes NOT Being Made

### Rejected #1: Variant 1's severity downgrade table (wholesale adoption)
- **Diff point**: C-002, severity classification section
- **Non-base approach**: Architect proposed 6+ severity downgrades across the delta's findings
- **Rationale**: The debate validated some downgrades (NR-3, Delta 2.5 to LOW from spec perspective) but rejected others (Delta 2.1 moved UP to HIGH, Delta 2.6 moved UP to HIGH by Analyzer). Wholesale adoption of Architect's severity table would include invalidated downgrades. Individual corrections are already captured in Changes #1 and #11.

### Rejected #2: Variant 3's removal of NR-7 from requirement list
- **Diff point**: C-009
- **Non-base approach**: Scribe argued NR-7 is "implementation guidance, not a spec requirement"
- **Rationale**: While NR-7's framing as a spec requirement is debatable, the underlying finding (execute_phase_tasks is dead code) is CRITICAL. The Scribe conceded this in Round 2. NR-7 is retained as it connects to MF-1, but reframed as a behavioral requirement rather than a code-location directive.

### Rejected #3: Variant 1's alternative architecture for NR-1 (runtime derivation)
- **Diff point**: C-007
- **Non-base approach**: Architect proposed runtime derivation of audit_gate_required as an alternative to push-model tasklist metadata
- **Rationale**: While the determinism argument was correctly reframed, the architectural choice (push vs pull) is a spec-owner decision, not a delta analysis conclusion. The merged output notes the alternative exists but does not adopt it as a recommendation, preserving the delta's push-model approach as the default per the spec's existing language.

---

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #1 NR-3 reclassification | Low | Moves one finding to appendix | Revert to original classification |
| #2 NR-5/NR-6 merge | Low | Annotation only | Remove annotation |
| #3 Corrected §4.4 language | Medium | New major section | Remove section |
| #4 Missing acceptance criteria | Low | Additive section | Remove section |
| #5 Undefined terms | Low | Additive subsection | Remove subsection |
| #6 Missing spec sections | Low | Additive subsection | Remove subsection |
| #7 §4.4 item 7 placement | Low | Annotation | Remove annotation |
| #8 NR-1 determinism reframing | Low | Annotation | Remove annotation |
| #9 Revised phase ordering | Medium | Modifies base content | Revert to base's original |
| #10 Branch decision framework | Medium | Structural addition | Remove section |
| #11 NR-2 severity upgrade | Low | Single cell | Revert to LOW |
| #12 GateDisplayState correction | Low | Annotation | Remove annotation |

## Review Status

Approval: **Pending user review** (--interactive mode)
Timestamp: 2026-03-17
