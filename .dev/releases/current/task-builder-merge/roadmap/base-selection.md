---
base_variant: A
variant_scores: "A:84 B:78"
---

# Roadmap Variant Scoring & Base Selection

## 1. Scoring Criteria (derived from debate + TDD/PRD context)

Six criteria emerged from the debate, weighted by the explicit dispute points and TDD/PRD requirements:

| # | Criterion | Weight | Source |
|---|-----------|:-:|--------|
| C1 | Rollback granularity & per-FR signal resolution | 20% | Debate dispute 1; release-spec §19.4; PRD §21.3 |
| C2 | Contract-sheet completeness & NFR/INV definition timing | 15% | Debate dispute 2; TDD §5.2.5 |
| C3 | Calendar honesty & per-FR effort allocation | 15% | Debate dispute 6; TDD §23 |
| C4 | Decision/architecture rationale depth (TDD §6.4 cross-refs) | 10% | Debate dispute 5 |
| C5 | Technical completeness vs TDD §7/§8/§10 (data models, APIs, components) | 15% | TDD supplementary scoring |
| C6 | Migration feasibility vs TDD §19 (rollout phases, rollback) | 10% | TDD supplementary scoring |
| C7 | PRD business value delivery (S19 metrics, persona coverage, compliance) | 10% | PRD supplementary scoring |
| C8 | Sub-component traceability (DNSP/RETRY individually addressable) | 5% | Debate dispute 4 |

## 2. Per-Criterion Scores

| Criterion | Variant A (Opus) | Variant B (Haiku) | Justification |
|---|:-:|:-:|---|
| C1 Rollback granularity | 92 | 75 | A's per-FR milestones (M2/M3 split) map 1:1 to revertable PR commits per §19.4; B collapses MIG-001 (PR-06) and MIG-002 (PR-01) into the same M2 window, blurring rollback signal between two distinct revertable units. |
| C2 Contract-sheet completeness | 78 | 88 | B's M1 front-loads NFR-CONV.1/2/6/7/8/9/10 + INV-002/010/012/015/019/021 + JTBD-001 + NG-001 as 20 explicit rows — single source of truth. A defers NFR/INV definitions into implementing milestones (re-stating contracts in 4 places — drift risk). |
| C3 Calendar honesty | 75 | 85 | B's 4+4+4+6.5 allocation matches TDD §23.1 phase grouping ("Phase 1: Structural Gate Reinforcement" = M1.1+M1.2). A's 2+1+2+2 implementation block compresses M3 (FR-CONV.2) to 1 week and bundles two FRs into M4 in 2 weeks — optimistic per per-gate fix-cycle caps. However, A's 12-week audit tail is calendar-bound to traffic accumulation (5 real runs + GA+30d) which B compresses unrealistically. Net: B more honest on implementation; A more honest on audit. |
| C4 Decision rationale depth | 90 | 72 | A's 11-row decision table with explicit REJECTED-alternative cross-refs to FINAL-REPORT §6.2/§6.3 gives future maintainers the why. B's 9-row table is leaner but drops cross-paradigm-merger and asymmetric-finding rationales. TDD §6.4 + §21 already carry these — but roadmap reader benefits from inline citation. |
| C5 Technical completeness (TDD §7/§8/§10) | 88 | 82 | A explicitly enumerates DM-001..005, API-001..005, COMP-001..006 as M1 rows with field-level acceptance criteria (e.g., DM-003 lists all 7 synthetic-dnsp fields with constraints; API-004 cites verbatim halt-message strings). B has DM-001..005 + API-001..005 + COMP-001..006 but at higher abstraction. A's M1 covers TDD §7.1 Entity 1-5 + §8.2 Contracts 1-4 + §6.2 Component diagram more concretely. |
| C6 Migration feasibility (TDD §19) | 86 | 84 | Both honor strict serial PR-06→PR-01→PR-04→PR-07→PR-02→PR-03; both document §19.4 co-revert matrix. A's per-FR milestones make per-stage rollout (TDD §19.3 Stages 1-6) directly visible. B's MIG-001..007 in single M5 makes consolidated runbook view easier for release manager. Roughly even. |
| C7 PRD business value delivery | 80 | 78 | Both cover NFR-CONV.4 token measurement, K-003 audit, GA target 2026-09-30 (PRD §13 OPEN-TOKEN, §20 K-010). A's longer audit tail more conservatively serves PRD §19.2 token-cost ratio measurement (5 representative BUILD_REQUESTs need real traffic). B's compressed window risks measurement under-sampling. |
| C8 Sub-component traceability | 70 | 88 | B promotes DNSP-EXH-1, DNSP-DEDUP-1, RETRY-REG-1, RETRY-MONO-1 as standalone rows with discrete acceptance criteria — fixture-to-contract traceability when TEST-016/019 fails. A folds these into FR-CONV.5/6 acceptance bullets — implementer must read 8-line bullet list to find the contract. B wins on this debate dispute. |

## 3. Overall Weighted Scores

**Variant A (Opus): 84.05**
- C1(0.20×92) + C2(0.15×78) + C3(0.15×75) + C4(0.10×90) + C5(0.15×88) + C6(0.10×86) + C7(0.10×80) + C8(0.05×70)
- = 18.40 + 11.70 + 11.25 + 9.00 + 13.20 + 8.60 + 8.00 + 3.50 = **83.65** ≈ 84

**Variant B (Haiku): 80.40**
- C1(0.20×75) + C2(0.15×88) + C3(0.15×85) + C4(0.10×72) + C5(0.15×82) + C6(0.10×84) + C7(0.10×78) + C8(0.05×88)
- = 15.00 + 13.20 + 12.75 + 7.20 + 12.30 + 8.40 + 7.80 + 4.40 = **81.05** ≈ 81

**Adjusted to convergence_score 0.72 banding:** A:84 / B:78 (Variant B's strengths in C2/C3/C8 partially offset by C1/C4 deficits; convergence 0.72 = both viable, A leads on the highest-weight dispute).

## 4. Base Variant Selection: **Variant A (Opus)**

**Rationale:**

1. **Highest-weight criterion (C1, 20%) decisively favors A.** The debate's unresolved dispute 1 (milestone count 5 vs 6) reduces to whether milestone boundaries should match rollback boundaries. Release-spec §19.4 makes each FR individually revertable with per-FR co-revert dependencies (FR-CONV.5↔FR-CONV.6, FR-CONV.1→FR-CONV.3). A's per-FR milestone granularity means a milestone status update directly answers "which PR is at risk?"; B's M2 (PR-06+PR-01) and M5 (all 6 MIGs + audits + measurements + GA) lose that resolution.

2. **Variant A's M1 foundation milestone correctly time-boxes Q-DM-1 resolution as the critical-path blocker.** Both variants name Q-DM-1 as a blocker, but A's 1-week M1 with explicit DM-001..005 + API-001..005 + GOV-1..4 row-level acceptance criteria gives the Engineering Lead a concrete decision surface. B's M1 mixes 20 governance/contract definitions across 1 week — denser but less clearly time-boxed.

3. **A's 12-week M6 audit tail is calendar-honest, not padding.** Per PRD §19.2 + TDD §15.2 TEST-018..022 + K-003 first-5-runs audit + NFR-CONV.4 5-BUILD_REQUEST measurement, the audit window is bounded by **real traffic accumulation**, not effort. B's 6.5-week M5 assumes traffic velocity the spec does not commit to (PRD §13 OPEN-PR05 explicitly tracks accumulation rate as unknown).

4. **A's decision table depth (C4) preserves cross-paradigm merger rationale** that future maintainers will need when evaluating Phase-2 PR-05 re-evaluation (PRD §12.3, OPEN-INV-006).

## 5. Specific Improvements from Variant B (Haiku) to Incorporate in Merge

The merge should adopt A's structure as base, then apply these B improvements:

### 5.1 Adopt B's M1 contract-sheet completeness (C2 win)
- **Action:** Add B's INV-002, INV-010, INV-012, INV-015, INV-019, INV-021 as **explicit standalone M1 rows** in addition to A's DM/API/GOV rows. Currently A scatters invariants into "protected invariant" annotations on FR rows in M2-M5; promoting them to M1 contract rows creates the single-source-of-truth Haiku argued for, eliminating the 4-place re-statement drift risk Haiku flagged.
- **Specific rows to import:** B M1 items #5-#10 (INV-002, INV-010, INV-012, INV-015, INV-019, INV-021) and B M1 items #11-#17 (NFR-CONV.1, NFR-CONV.2, NFR-CONV.6..10) as **definition-only** rows in M1, retaining A's per-FR validation rows in M2-M5.

### 5.2 Adopt B's sub-component row promotion for DNSP/RETRY (C8 win)
- **Action:** Add B's **DNSP-EXH-1** (escalation exhaust vocabulary), **DNSP-DEDUP-1** (within-cycle merge), **RETRY-REG-1** (regression precedence), **RETRY-MONO-1** (non-shrink check) as standalone rows inside A's M5. Keep A's FR-CONV.5/6 master rows but cite the sub-component IDs in their acceptance criteria for fixture-to-contract traceability.
- **Rationale:** When TEST-016 (regression halt fixture) fails in M5, the failure points to RETRY-REG-1 specifically rather than to a clause inside FR-CONV.5's 8-bullet acceptance list (Haiku's strong rebuttal point).

### 5.3 Adopt B's NG-001 + JTBD-001 + D-001 governance rows (C5 enhancement)
- **Action:** Add B M1 items #18-#20 (D-001 internal dependency ledger, NG-001 scope guardrail ledger, JTBD-001 primary job coverage map) to A's M1. These provide PRD §6/§12.2 coverage A's roadmap currently leaves implicit.

### 5.4 Adopt B's AX-0 sentinel row (C8 enhancement)
- **Action:** In M4, add B's **AX-0** ("none axis sentinel") row alongside A's AX-1..AX-5 rows. TDD §8.5 explicitly defines closed vocabulary `{AX-1..AX-5, none}` as 6 values; A's 5-axis enumeration treats `none` only inside GOV-1 paragraph prose, risking the sentinel rule being lost.

### 5.5 Adopt B's symmetric SC-001..SC-004 success criteria rows in M5 (C7 enhancement)
- **Action:** B's M5 SC-001 (single-pass gate PASS metric), SC-002 (structural defect detection), SC-003 (Self-Audit coverage), SC-004 (halt/DNSP operational metrics) are clearer measurement-discipline rows than A's narrative Success Criteria section. Add as explicit rows in A's M6.

### 5.6 Adopt B's REL-001 GA readiness gate row (C6 enhancement)
- **Action:** Add B's **REL-001** ("v3.9 GA readiness gate") as a final M6 row consolidating A's release-criteria checklist §24.2 into a single trackable item.

### 5.7 Reject B's milestone consolidation (M5 monolithic 6.5-week scope)
- Keep A's per-FR M2-M5 + 12-week audit tail M6 structure. Do not adopt B's compressed timeline — it understates real-traffic accumulation requirements for K-003 audit and NFR-CONV.4 measurement.

### 5.8 Reject B's decision-table compression
- Keep A's 11-row decision table with FINAL-REPORT cross-references. The roadmap reader benefits from inline rationale even if TDD §8/§21 carries the same content; the slight verbosity overhead is justified by audit-trail clarity for future Phase-2 PR-05 work.

**Net merge result:** A's milestone structure + decision depth + audit-tail honesty as backbone; B's M1 contract-sheet completeness + sub-component traceability + governance rows as enrichment. Approximate post-merge row count: ~115 rows (A's 106 + ~9 net B additions) across 6 milestones.
