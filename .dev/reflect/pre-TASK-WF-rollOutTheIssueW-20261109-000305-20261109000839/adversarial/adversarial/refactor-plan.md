# Refactoring Plan: Merge into Base (Variant B)

## Overview
- Base: Variant B (haiku:qa)
- Incorporating strengths from: Variant A (sonnet:analyzer), both rebuttals, invariant probe
- Planned changes: 4
- Risk level: Medium

## Planned Changes
### Change 1: Qualify base findings (Variant B and Round 2)
- Source: Variant B F2, QA-02, QA-03, QA-04; both Round 2 rebuttals.
- Target: merged review findings (replace wording and normalize IDs while retaining aliases).
- Rationale: debate C-001/C-003 favors B, but both advocates retract overclaims.
- Integration point: F2 remains medium verification gap, no established leak; QA-02 becomes medium and separates gate contradiction from unverified matrix allegation (drop the latter); QA-03 remains medium, specifically consumed raw field, not all stderr layouts; QA-04 remains medium expected-value omission, not forbidden edits or certain failure for every capture. Do not call source effort estimate a specification exception.
- Risk: Medium, qualifications could disappear during paraphrase; preserve explicit negatives.

### Change 2: Add A's supported findings (Variant A)
- Source: A F1 and F4; Round 2 withdrawals of F3/F5.
- Target: merged review findings (append F1 medium, F4 low) and disposition notes.
- Rationale: C-002 favors A; F1 is a literal acceptance blocker, F4 a real low-severity map omission.
- Integration point: restrict F1 recommendation to reason-column extraction; F4 updates the section map, without treating the section title as a blocker. F3 count is already implied; F5 is navigation advice. Keep withdrawals visible but not in required-fix count.
- Risk: Low, additive; retain original finding aliases for traceability.

### Change 3: Preserve evidence and confidence discipline (Variant A plus calibrations)
- Source: A self_audit, A calibrated .74, B calibrated .72; debate C-004.
- Target: merged review metadata, provenance, checked-negative notes.
- Rationale: self-confidence .88/.95 is not calibrated confidence.
- Integration point: record both calibrations and conservative merged confidence .72; do not claim complete coverage. Use source-card and rebuttal provenance comments per section. Cite snapshot evidence, not future line numbers.
- Risk: Low, metadata only; a self-audit is not execution evidence.

### Change 4: Carry probe residuals and owner boundaries (invariant probe)
- Source: invariant-probe.md, especially INV-009, INV-011 and INV-001.
- Target: merged review limitations (append).
- Rationale: no HIGH UNADDRESSED invariant blocks convergence, but two MEDIUM residuals remain.
- Integration point: state Task 3 has no full row-by-row builder/preservation review; conditional pre-existing CRLF framing can interact with test normalization, so capture format must be examined before labelling failure a production-parser mismatch. No actual capture or runtime failure is established. Preserve false configuration and owner-only live test, shadow run, lock/restart tests, cron, record and enablement. Any parser mismatch remains follow-up scope.
- Risk: Medium, warning could be misreported as observed defect; explicitly mark conditional.

## Changes NOT Being Made (with rationale)
| Diff point | Non-base approach | Disposition |
|---|---|---|
| S-003 | Original QA-02 high severity | Reject: medium after calibration and rebuttals |
| U-002 | F3 as required defect | Reject: two occurrences already implied |
| U-004 | F5 as required defect | Reject: navigation advice only |
| A-001 | Source ambiguity based on effort estimate | Reject: both advocates retracted it |
| A-003 | Run live actions or flip enabled | Never authorized; boundary retained |

This merge writes review artifacts only. It never edits the gated workflow plan or repository source, tests or documentation.

## Risk Summary
| Change | Risk | Impact if failed | Rollback |
|---|---|---|---|
| 1 | Medium | Overstates defects or weakens every-fixture requirement | Restore qualified rebuttal wording |
| 2 | Low | Omits acceptance blocker or promotes advice to defect | Restore A F1/F4 and withdrawal notes |
| 3 | Low | Inflates confidence or implies complete review | Restore calibrator values and limitations |
| 4 | Medium | Claims unobserved failure or crosses owner boundary | Restore conditional warning and explicit prohibitions |

Rollback refers only to generated review artifacts; no implementation rollback is involved.

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-09T01:31:59Z
- Analytical review: PASS
- Blocking findings: none. This verdict approves the four-change review-artifact merge plan only, not the gated workflow plan or rollout readiness.
- Evidence — Change 1: matches the final base selection and both Round 2 qualifications: F2 is a verification gap, QA-02 is medium with the matrix allegation dropped, QA-03 concerns the consumed raw field, and QA-04 concerns capture-dependent expected values, not forbidden edits or universal failure. The effort estimate does not weaken “every”.
- Evidence — Change 2: retains A's acceptance-blocking F1 and low F4; withdraws F3/F5 from required fixes, as both rebuttals and INV-002/003/008 require.
- Evidence — Change 3: retains checked-negative evidence, snapshot provenance and calibrated rather than self-reported confidence without claiming completeness. The conservative merged .72 is review metadata, not a new measurement or execution evidence.
- Evidence — Change 4: preserves INV-009's unreviewed Task 3 fidelity, INV-011's conditional CRLF interaction, and INV-001's false configuration/owner-only boundary; neither residual is presented as an observed runtime defect.
- Minor note: the integration wording could state INV-005/010's limits more explicitly: a token-pattern scan cannot establish complete redaction, and raw-field/expected-value changes cannot guarantee a test or suite passes. Carry those limits into the merged review; no contradictory success claim currently requires blocking this plan.
- Self-audit: compared only the requested review artifacts against Section 4 of the governing template; no repository-source exploration, network, Git, tests, real captures, other agents or merge execution. Existing evidence and confidence were assessed for faithful synthesis, not independently revalidated against implementation. Only this Review Status section was changed.
