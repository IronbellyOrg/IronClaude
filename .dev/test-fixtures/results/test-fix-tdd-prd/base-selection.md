---
base_variant: "A (Opus-Architect)"
variant_scores: "A:79 B:74"
---

## 1. Scoring Criteria (Derived from Debate)

Seven criteria extracted from the debate disputes, weighted by their impact on project success:

| # | Criterion | Weight | Source Disputes |
|---|-----------|--------|-----------------|
| C1 | Phase structure & risk gating | 15% | D-01, D-03 |
| C2 | Testing strategy robustness | 15% | D-03 |
| C3 | Spec fidelity & PRD coverage | 15% | D-07, D-05/D-06 |
| C4 | Stakeholder communication (FTE, confidence, revenue) | 10% | D-08, D-09, D-12 |
| C5 | Technical completeness (task detail, integration wiring) | 15% | D-10, D-11 |
| C6 | Compliance & OQ handling | 15% | D-05/D-06, D-14 |
| C7 | Business value delivery & persona coverage (PRD-derived) | 15% | PRD S7, S17, S19 |

## 2. Per-Criterion Scores

### C1: Phase Structure & Risk Gating (15%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | **82** | 72 |

**Evidence:** The debate convergence assessment (D-01, D-03) favored Opus's testing isolation as more robust to schedule pressure — Haiku's own 65% confidence rating at Week 6 undermines its shift-left argument. Opus's 5-phase structure provides unambiguous go/no-go gates. Haiku's valid rebuttal that Opus's Phase 3 (API + frontend + integration in 2 weeks) is under-allocated costs Opus points, but the dedicated testing gate is the stronger structural choice per debate consensus.

### C2: Testing Strategy Robustness (15%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | **85** | 68 |

**Evidence:** Debate convergence explicitly states "Variant A (Opus)" as the stronger position on testing isolation. Opus's Phase 4 provides a frozen-codebase testing gate. Haiku's distributed testing is "vulnerable to the exact schedule pressure Haiku's own confidence ratings predict" (convergence assessment, dispute #2). However, Haiku's rebuttal that Opus's Phase 4 packs 6 workstreams into 10 days is valid — the Phase 4 scope needs tightening in the merge.

### C3: Spec Fidelity & PRD Coverage (15%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | 72 | **80** |

**Evidence:** The PRD (AUTH-E1) explicitly includes a logout user story. Opus omits the logout endpoint entirely, flagging it as OQ-7. The debate convergence ruled "Variant B (Haiku)" as the stronger position on D-07: "A roadmap that omits a committed feature is incomplete." Haiku also lists OQ-7 as deferred with implementation recommendation (`POST /auth/logout`), while Opus only flags it as blocking. Additionally, Haiku addresses OQ-8 (admin audit log query) with an explicit deferral note, satisfying the Jordan persona's needs acknowledgment.

### C4: Stakeholder Communication (10%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | 60 | **88** |

**Evidence:** Debate convergence favored Haiku on FTE estimates (D-08), revenue framing (D-12), and debt transparency (D-14). Opus's resource section uses team names without counts; Haiku provides specific FTE numbers (6/11/7 per phase), confidence ratings per week, $2.4M revenue framing, and explicit architectural debt acknowledgment. The debate found that "Including FTE estimates is lower-risk than omitting them" and debt transparency "won clearly."

### C5: Technical Completeness (15%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | **88** | 72 |

**Evidence:** Opus provides per-phase integration wiring tables (debate D-10 favors Opus) with named artifacts, types, wired components, owning phases, and consuming phases — 5 tables across 5 phases. Opus includes 58 numbered task rows with explicit IDs versus Haiku's less structured approach. Opus's tasks have tighter dependency chains (e.g., COMP-002 depends on COMP-003, DM-002, OPS-006). Opus also includes API versioning (task #28), API error format standardization (task #29), and success criteria instrumentation (task #48) as separate tasks. Haiku's architecture integration section is narrative rather than tabular, making cross-phase traceability harder.

### C6: Compliance & OQ Handling (15%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | **80** | 76 |

**Evidence:** Split decision per debate. Opus proactively resolves OQ-9 (GDPR consent field) in Phase 1 DM-001 — the debate found this stronger because "the downside of adding it unnecessarily is near zero." Haiku is stronger on OQ-6 (gated resolution rather than assumption). Both identify 12-month retention as the likely answer. Opus includes NFR-COMP-001 through NFR-COMP-004 as separate tasks with acceptance criteria. Haiku defers some compliance validation to Phase 3, which is riskier per the Q3 2026 deadline. Opus's compliance validation checklist (task #47) is more explicit.

### C7: Business Value Delivery & Persona Coverage (PRD-derived) (15%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | 72 | **78** |

**Evidence:** Haiku explicitly maps each phase to personas ("Personas & Value" subsections) — Phase 1 maps to Alex and Sam, Phase 2 adds Jordan, Phase 3 adds compliance team. Opus's executive summary mentions all three personas but doesn't map them to phases. Haiku's revenue framing ($2.4M) directly addresses PRD S19 business rationale. Haiku's "Strategic Value Realization" section maps week-by-week value delivery. However, Haiku omits the logout endpoint from Phase 2 scope (only deferred to OQ-7), which contradicts PRD AUTH-E1's explicit logout story — same gap as Opus but at least acknowledged.

## 3. Overall Scores

| Criterion | Weight | A (Opus) | B (Haiku) |
|-----------|--------|----------|-----------|
| C1: Phase structure | 15% | 82 | 72 |
| C2: Testing robustness | 15% | 85 | 68 |
| C3: Spec fidelity | 15% | 72 | 80 |
| C4: Stakeholder communication | 10% | 60 | 88 |
| C5: Technical completeness | 15% | 88 | 72 |
| C6: Compliance & OQ handling | 15% | 80 | 76 |
| C7: Business value & personas | 15% | 72 | 78 |
| **Weighted Total** | | **78.5** | **75.0** |

**Rounded: A:79, B:75**

**Justification:** Variant A wins on the structural dimensions that determine whether the project *ships correctly* — phase gating, testing isolation, integration wiring, and technical task decomposition. Variant B wins on the communication dimensions that determine whether the project *gets funded and understood* — FTE estimates, confidence ratings, revenue framing, debt transparency, and persona mapping. Since structural correctness is the harder problem to retrofit (adding FTE numbers to a well-structured roadmap is easier than adding structure to a well-communicated one), Variant A is the stronger base.

## 4. Base Variant Selection Rationale

**Selected base: Variant A (Opus-Architect)**

1. **Structural skeleton is harder to retrofit.** Opus's 5-phase structure with entry/exit criteria, per-phase integration wiring tables, and 58 numbered task rows provides the scaffolding that a merge builds on. Adding Haiku's communication elements (FTE, confidence, revenue) to Opus's structure is additive. Restructuring Haiku's 3 phases into 5 would require rewriting task dependencies, renumbering, and re-sequencing — a destructive edit.

2. **Debate consensus supports Opus's core structural choices.** The convergence assessment recommended adopting Opus's 5-phase structure (D-01), dedicated testing gate (D-03), per-phase integration tables (D-10), and isolated load testing (D-11).

3. **Technical task granularity is higher.** Opus has separate tasks for API versioning, error format standardization, and success criteria instrumentation that Haiku omits or embeds implicitly. These are easier to preserve than to reconstruct.

4. **Compliance timeline is tighter with Opus.** Opus's proactive OQ-9 resolution and explicit Phase 4 compliance validation checklist provide more margin before the Q3 2026 SOC2 deadline.

## 5. Specific Improvements to Incorporate from Variant B (Haiku)

| # | Element from Haiku | Target Location in Merged Roadmap | Rationale (Debate Reference) |
|---|-------------------|----------------------------------|------------------------------|
| 1 | **FTE estimates per phase** (6/11/7/TBD/TBD) | New subsection in Resource Requirements | D-08: "Including FTE estimates is lower-risk than omitting them." Add as indicative, not contractual. |
| 2 | **Confidence ratings per week** | Add to Timeline Summary as a column | D-09: Draw, but net-positive for mature teams. Include with caveat that ratings are architect estimates. |
| 3 | **Revenue framing** ($2.4M) | Add to Executive Summary, 1 sentence | D-12: "Answers 'why should we fund this' before anyone asks." Keep brief to avoid accountability misattribution. |
| 4 | **Architectural debt section** | New section after Open Questions | D-14: "Debt transparency won clearly." List: no logout (v1.0), no admin query API (v1.1), no MFA (v1.1+), no social login (v2.0). |
| 5 | **Logout endpoint** (`POST /auth/logout`) | Add as task in Phase 3 with scoping sub-task | D-07: "The PRD commits to logout." Include with explicit scoping AC: single-device, revoke current refresh token, clear AuthProvider state, redirect to /login. |
| 6 | **Persona-to-phase mapping** | Add "Personas & Value" line to each phase header | C7: Haiku's explicit mapping aids stakeholder understanding without adding bulk. |
| 7 | **Post-GA monitoring cadence** | Add to Phase 5 exit criteria | D-13: Daily SLO dashboard, weekly metrics review, monthly post-incident reviews, quarterly compliance audit. |
| 8 | **Retrospective scheduling** | Add as task in Phase 5 | D-13: Schedule retrospective for 2 weeks post-GA. |
| 9 | **Buffer recommendations** | Add as note in Timeline Summary | Haiku's 1-2 week contingency recommendation is honest planning. Opus's flat 11 weeks embeds no explicit buffer. |
| 10 | **OQ-6 gated resolution** (not assumed) | Modify OQ-6 handling: resolve before Phase 1 as blocking gate, don't assume 12-month | D-05/D-06 split: Haiku is stronger on OQ-6 because "the implementation implications of 12 months vs 90 days are non-trivial." |
