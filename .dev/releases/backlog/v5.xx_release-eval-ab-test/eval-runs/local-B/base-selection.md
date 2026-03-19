---
base_variant: A
variant_scores: "A:81 B:74"
---

# Scoring: Opus (A) vs Haiku (B) Roadmap Variants

## 1. Scoring Criteria (Derived from Debate)

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Technical Precision | 20% | D-08 (import path), D-03 (separation of concerns) |
| C2 | Task Actionability | 15% | D-11 (task granularity), sprint-readiness |
| C3 | Risk Management | 15% | D-01 (spec closure), D-07 (resume), D-04 (parallelization) |
| C4 | Phase Structure & Gating | 15% | D-02/D-06 (phase count), D-03 (reporting location) |
| C5 | Timeline & Estimation | 10% | D-05 (qualitative vs quantitative) |
| C6 | Requirement Traceability | 10% | D-11 (FR/NFR mapping per task) |
| C7 | Process Completeness | 10% | D-06 (release readiness), D-10 (staffing) |
| C8 | Parallelization Awareness | 5% | D-04 (Phase 3 independence) |

## 2. Per-Criterion Scores

| Criterion | A (Opus) | B (Haiku) | Justification |
|-----------|----------|-----------|---------------|
| **C1: Technical Precision** | 90 | 72 | Opus catches `StepResult` import path error (D-08, conceded by Haiku). Opus correctly identifies `metadata: dict` as schema-independent (D-01 rebuttal). Haiku references `roadmap/models.py` for `StepResult` — the wrong path. |
| **C2: Task Actionability** | 88 | 65 | Opus provides numbered tasks (1.1–5.3) with per-task requirement mapping. Haiku uses prose descriptions requiring decomposition before sprint execution (D-11, conceded by Haiku). |
| **C3: Risk Management** | 75 | 82 | Haiku elevates resume behavior (D-07) and spec closure as explicit risks. Opus dismisses resume as "non-blocking" despite spec contradiction. Haiku's Phase 0 checkpoint prevents mid-implementation pivots. However, Opus's risk table is more structured with severity/probability ratings. |
| **C4: Phase Structure** | 78 | 76 | Opus's 5-phase plan isolates advanced reporting cleanly (Phase 4), preventing Phase 2 from becoming ungated. Haiku bundles convergence/remediation/wiring into Phase 2, creating a massive phase that's harder to gate. Haiku's Phase 0 and Phase 5 add process value but also overhead. |
| **C5: Timeline & Estimation** | 68 | 80 | Haiku provides concrete day estimates (5.5 days total) that serve planning. Opus uses qualitative sizing only. The debate showed both have merit, but a roadmap consumed by sprint tooling benefits from numeric estimates. |
| **C6: Requirement Traceability** | 90 | 60 | Opus maps every task to specific FR/NFR/SC codes. Haiku's requirement coverage is implicit in prose — you have to infer which tasks satisfy which requirements. |
| **C7: Process Completeness** | 70 | 82 | Haiku's Phase 0 (spec closure) and Phase 5 (release readiness) cover last-mile tasks that Opus leaves to engineering discipline. The staffing model, while aspirational, serves as a review checklist. |
| **C8: Parallelization** | 85 | 65 | Opus explicitly calls out Phase 3 parallelization opportunity with dependency analysis. Haiku sequences everything linearly. |

## 3. Overall Scores

**Variant A (Opus): 81/100**
- Strengths: Technical accuracy, sprint-ready task decomposition, requirement traceability, parallelization awareness
- Weaknesses: No timeline estimates, dismisses legitimate spec ambiguity risks, no release readiness phase

**Variant B (Haiku): 74/100**
- Strengths: Process discipline, timeline estimates, risk elevation for spec ambiguities, release readiness coverage
- Weaknesses: Wrong `StepResult` import path, prose-only task descriptions, oversized Phase 2, no requirement traceability per task

## 4. Base Variant Selection Rationale

**Selected base: Variant A (Opus)**

The merge will produce a tasklist via sprint tooling. Opus's numbered tasks with requirement mapping (1.1–5.3) are directly consumable by `superclaude sprint run` without an intermediate decomposition step. Rebuilding Haiku's prose into this structure would require rewriting most of the roadmap, whereas grafting Haiku's process improvements onto Opus's skeleton requires only additive changes.

Opus's technical precision (correct import path, accurate `metadata: dict` analysis, separation of wiring vs content concerns) means fewer implementation errors. The 7-point gap is driven primarily by Opus's structural advantages in actionability and traceability — the properties that matter most for downstream execution.

## 5. Improvements to Incorporate from Haiku (B)

| Improvement | Source | Integration Point |
|-------------|--------|-------------------|
| **Add Phase 0 checkpoint** | D-01, Haiku's spec closure phase | Insert as Phase 0 (0.5 day) gating Phase 2 entry on OQ-001/OQ-002 resolution. Lighter than Haiku's full phase — just decision records, not a staffing exercise. |
| **Add day estimates** | D-05, Haiku's timeline table | Augment Opus's qualitative sizing with Haiku's numeric estimates in the Phase 6 timeline table. |
| **Elevate resume behavior** | D-07, Haiku's risk identification | Add OQ-004 resolution to Phase 0 checkpoint. Opus correctly notes the two modes aren't contradictory, but the scope decision should be explicit before Phase 1. |
| **Add Phase 5 release readiness** | D-06, Haiku's Phase 5 | Add a lightweight release phase: `make verify-sync`, representative validation run, release notes. Half-day, not ceremonial. |
| **Resume risk in risk table** | D-07 | Add as RISK-005 in Opus's risk assessment section with medium severity. |
| **Staffing as review checklist** | D-10 rebuttal | Add a note in Phase 0 or Section 4: "Schema decisions require architectural review; crash-safety testing benefits from independent validation." Not a staffing model — a review expectation. |
