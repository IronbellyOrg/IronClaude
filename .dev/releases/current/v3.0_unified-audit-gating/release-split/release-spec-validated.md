---
parent-spec: .dev/releases/current/v3.0_unified-audit-gating/spec-refactor-plan-merged.md
split-analysis: "no-split-recommended"
rationale: "Document refactoring plan with 11 interleaved sections; no valid architectural seam for splitting"
status: validated
date: 2026-03-18
---

# Unified Audit Gating Spec Refactor Plan — Validated (Single Release)

## Why This Release Stays Intact

The spec refactoring plan merges two analytical streams (Plan A: behavioral gate extensions; Plan B: foundation/scope hardening) into a single coherent editing plan for `unified-audit-gating-release-spec.md`. Adversarial analysis by two independent agents (opus:architect at 0.88 confidence, haiku:analyzer at 0.90 confidence) unanimously confirmed that splitting is not warranted because:

1. **11 of 28 sections are interleaved** — 8 contain A+B-merged content and 3 contain synthesized conflict resolutions that fuse both streams into indivisible structures
2. **The synthesized sections are load-bearing** — SS10.1 (Phase Plan), SS10.2 (File-Level Change Map), and SS12.3 (Blocker List) are the architectural spine; splitting would require re-authoring them twice
3. **Real-world validation is implementation-gated** — meaningful validation (executor behavior, artifact production, shadow-mode KPIs) depends on code work, not on document completeness
4. **Internal prioritization already exists** — the dependency order, Phase 0-4 structure, and implementation waves achieve staged risk reduction without formal splitting

## Risks Addressed Without Splitting

| Risk | Strategy |
|------|----------|
| Reviewer fatigue (28 sections) | **Prioritized review**: Apply Phase 0 blocking changes first (SS2.1, SS4.1, SS1.1, SS9.3, SS12.3, SS12.4, Open Decisions), review and approve, then proceed to Phase 1 structural changes |
| Delayed feedback on behavioral extensions | **Immediate implementation**: P0-B (SilentSuccessDetector) and P0-C (D-03/D-04) are explicitly marked as "no dependency, deployable immediately" — begin code work before spec editing completes |
| Scope creep from behavioral extensions | **Explicit exclusions**: SS1.3 already excludes D-01, D-05, and developer utility subcommands; scope boundary is drawn |
| Big-bang spec approval risk | **Decision-first checkpoint**: Close blockers 5-9 (branch(b) owner/deadline, reimbursement_rate fate, S2 calibration, mock-llm scope, P0-A scheduling) as an interim milestone before full approval |

## Validation Strategy

### Phase 0 — Decision Checkpoint (before editing begins)

Validate that all prerequisite decisions are closable:
- Branch (b) locked decision: assign owner + UTC deadline
- Per-task artifact addressability (C3): confirm or escalate
- S2 calibration methodology: Reliability Owner commitment
- `--mock-llm` scope: define check matrix

This is a **real checkpoint** — it produces owner/deadline assignments that are actionable artifacts.

### Spec Editing — Single Pass with Dependency Order

Apply all 28 changes in the documented dependency order (lines 1209-1232 of the plan):

1. **Phase 0 blocking** (7 sections): SS2.1 → SS4.1 → SS1.1 → SS9.3 → SS12.3 → SS12.4 → Open Decisions
2. **Phase 1 structural** (15 sections): SS3.1, SS1.3, SS2.2, SS2.3, SS4.4, SS5.1, SS5.2, SS6.1, SS7.2 → SS8.5, SS8.3, SS9.2, SS10.1 → SS10.2 → SS10.3, SS11, New SS13, Top 5 Immediate
3. **Any time** (1 section): Top 5 Deferred

### Post-Edit Verification — 29-Point Checklist

Run the full verification checklist (lines 1240-1279 of the plan) covering:
- Plan B invariants (11 checks)
- Plan A invariants (16 checks)
- Cross-plan consistency invariants (5 checks)

### Implementation Wave Validation

After spec editing is approved, validate through implementation:

| Wave | Items | Real-World Validation |
|------|-------|----------------------|
| Wave A (immediate) | P0-B: SilentSuccessDetector, P0-C: D-03/D-04 | `test_no_op_pipeline_scores_1_0` against real broken executor; `test_run_deterministic_inventory_cli_portify_case` against real v2.25 artifacts |
| Wave B (after P0-A) | P0-A defect fixes → G-012 smoke gate | Real cli-portify run against smoke fixture; intermediate artifact production verified |
| Wave C (Phase 1-2) | AuditWorkflowState, transitions, runtime controls | Deterministic replay stability; timeout/retry path termination; shadow-mode data collection |
| Wave D (Phase 3-4) | TUI, command surface, rollout | Shadow → Soft → Full promotion with real KPI data; rollback drill success |

## Original Spec Updates

The following improvements were identified during the split analysis and should be incorporated:

1. **Add review order guidance**: Include the Phase 0 → Phase 1 → Any Time review ordering as an explicit recommendation in the plan header, so reviewers know which sections to prioritize
2. **Add decision-first checkpoint**: Formalize the decision closure for blockers 5-9 as a named checkpoint before spec editing begins
3. **Clarify implementation independence**: Strengthen the existing notes about P0-B and P0-C having no spec dependency — make this a top-level callout so implementation teams don't wait for spec approval to begin

## Traceability

All 28 section changes from the original plan are preserved in the single-release approach:

| Source | Sections | Count | Status |
|--------|----------|-------|--------|
| UNIQUE-A | SS1.3, SS2.2, SS5.1, SS8.3, New SS13, Implementation Order | 6 | PRESERVED |
| UNIQUE-B | SS2.1, SS3.1, SS4.1, SS4.4, SS7.2, SS8.5, SS9.2, SS9.3, Top 5 Deferred, Open Decisions | 10 (note: SS2.1 is counted in B's 11 unique) | PRESERVED |
| A+B-merged | SS1.1, SS2.3, SS5.2, SS6.1, SS10.3, SS11, SS12.4, Top 5 Immediate | 8 | PRESERVED |
| Synthesized | SS10.1, SS10.2, SS12.3 | 3 | PRESERVED |
| Unchanged | SS0, SS1.2, SS3.2, SS4.2, SS4.3, SS5.3, SS6.2-6.4, SS7.1, SS7.3, SS8.1-8.2, SS8.4, SS9.1, SS12.1-12.2 | 17 | NOT MODIFIED |
| **Total** | | **28 changes + 17 unchanged** | **100% coverage** |
