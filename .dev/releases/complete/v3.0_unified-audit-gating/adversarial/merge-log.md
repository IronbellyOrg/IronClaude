# Merge Log: Unified Audit Gating v3.0

**Date**: 2026-03-18
**Protocol**: Adversarial debate, complementary-spec mode, standard depth (2 rounds)
**Base variant**: Variant B (Wiring Verification Gate v2.0) -- score 0.860
**Donor variant**: Variant A (Unified Audit Gating v1.2.1) -- score 0.568

---

## Artifacts Produced

| # | Artifact | Path |
|---|----------|------|
| 1 | Diff Analysis | `adversarial/diff-analysis.md` |
| 2 | Debate Transcript | `adversarial/debate-transcript.md` |
| 3 | Base Selection | `adversarial/base-selection.md` |
| 4 | Refactor Plan | `adversarial/refactor-plan.md` |
| 5 | Merged Spec | `adversarial/merged-spec.md` |
| 6 | Merge Log | `adversarial/merge-log.md` (this file) |

---

## Merge Operations Executed

| Op | Description | Source | Target Section | Status |
|----|-------------|--------|----------------|--------|
| W-001 | Add Lifecycle Governance Appendix | Variant A SS 4, 9 | Appendix D | DONE |
| W-002 | Adapt rollout with rollback triggers | Variant A S 7.3 | Section 7, each phase | DONE |
| W-003 | Add calibration methodology | Variant A S 8.2 | Section 7, Phase 2 | DONE |
| W-004 | Add decision tracking section | Variant A S 12.4, 9.3 | Section 15.4 | DONE |
| W-005 | Document GateResult naming resolution | Contradiction X-001 | Section 8.4, Decision D8 | DONE |
| W-006 | Drop stale Variant A content | Multiple sections | N/A | DONE |
| W-007 | Add governance coordination note | Debate synthesis | Section 15.3 | DONE |

---

## Content Dropped from Variant A

| Content | Reason |
|---------|--------|
| `--strictness` vs `--profile` alias resolution (S 3.2) | Implementation detail; premature for spec |
| `GateResult` normative schema (S 6.1) | Conflicts with existing `GateResult` in `audit/evidence_gate.py` |
| `OverrideRecord` schema (S 6.2) | New infrastructure; deferred to lifecycle implementation (v3.1) |
| `GateTransitionEvent` / `GateCheckEvent` schemas (S 6.3) | New infrastructure; deferred |
| Versioning policy (S 6.4) | Premature for first implementation |
| `sc-audit-gate` and `sc-audit-gate-protocol` skill file references (S 10.2) | Nonexistent files in codebase |
| Checklist closure matrix (S 11) | Process state, not spec content |
| KPI metrics M1-M12 definitions | Governance-level; referenced in Appendix D.6 but not detailed |
| Specific profile thresholds and severity mapping decisions | Implementation detail; listed as open decisions |
| Retry/backoff/timeout specific values | Implementation detail; conceptual model preserved in Appendix D.3 |

---

## Content Preserved from Variant A

| Content | Location in Merged Spec |
|---------|------------------------|
| Lifecycle state machine (legal/illegal transitions) | Appendix D.1 |
| Override governance (scope eligibility, approval model) | Appendix D.2 |
| Timeout/retry semantics (lease, heartbeat, bounded budget) | Appendix D.3 |
| Owner responsibilities | Appendix D.4 |
| Decision deadline requirements | Appendix D.5 |
| KPI/SLO framework (calibration methodology) | Appendix D.6, Section 7 Phase 2 |
| Governance-level rollback triggers | Appendix D.7 |
| Rollback triggers adapted for wiring gate | Section 7, each phase |
| Calibration method for FPR/TPR thresholds | Section 7, Phase 2 |
| Decision tracking pattern (owner + deadline + phase) | Section 15.4 |

---

## Content Unchanged from Variant B (Base)

All of Sections 1-6 and 8-13 are taken directly from Variant B with the following minor modifications:

1. Version references changed from `v2.0`/`v2.1` to `v3.0`/`v3.1` to match the unified release numbering
2. Non-Goals section expanded to include lifecycle state machine and `/sc:audit-gate` as explicit non-goals (referencing Appendix D)
3. Section 8.4 added (GateResult naming clarification) per W-005
4. Decision D8 added to Section 14 per W-005
5. Section 15.3 added (relationship to lifecycle governance) per W-007
6. Appendix C "Out of Scope" expanded to reference Appendix D

---

## Validation Checklist

| # | Check | Result |
|---|-------|--------|
| 1 | All substrate references are from Variant B (verified line numbers) | PASS |
| 2 | No nonexistent file references from Variant A remain | PASS |
| 3 | Governance appendix is clearly separated from core sections | PASS -- Appendix D with deferred status note |
| 4 | Rollout section includes adapted rollback triggers | PASS -- each phase has rollback trigger |
| 5 | Decision tracking includes only wiring-gate-specific decisions | PASS -- 4 decisions in Section 15.4 |
| 6 | Tasklist unchanged from Variant B | PASS -- T01-T12 identical |
| 7 | Merged spec can generate tasklist without governance dependency | PASS -- Appendix D explicitly labeled as deferred |
| 8 | GateResult naming collision documented | PASS -- Section 8.4, Decision D8 |
| 9 | YAML frontmatter includes merge provenance | PASS |
| 10 | Both parent specs referenced in parent_analysis | PASS |

---

## Summary

The merged spec is a wiring-verification-gate implementation spec (Sections 1-15) with a governance framework appendix (Appendix D). The implementation is self-contained and can proceed immediately via the T01-T12 tasklist. The governance framework provides architectural context for how the wiring gate fits into the broader lifecycle system, with implementation deferred to v3.1.

The primary architectural insight from this merge is that Variant A and Variant B are not competing designs but different layers of the same system. Variant B is the implementation layer (concrete gate). Variant A is the governance layer (lifecycle transitions). The merged spec makes this relationship explicit and sequences implementation correctly: gate first, governance second.
