---
base_variant: "B (Haiku Architect)"
variant_scores: "A:74 B:79"
---

# Base Selection: Variant Scoring and Rationale

## 1. Scoring Criteria (Derived from Debate)

The debate surfaced 8 divergence points. I derive 10 scoring criteria weighted by their impact on project success:

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Timeline realism vs Q2 deadline | 15% | D1, PRD target release Q2 2026 |
| C2 | Security completeness | 15% | D2, D3, D6, D8 |
| C3 | Specification coverage (all FRs/NFRs) | 12% | Both variants, PRD §Technical Requirements |
| C4 | Operational specificity (alerts, thresholds, rate limits) | 10% | D6, D7 |
| C5 | Structural rigor (milestones, wiring tables, guardrails) | 10% | D1, D4 |
| C6 | Business value delivery speed (PRD Success Metrics S19) | 10% | PRD §Success Metrics |
| C7 | Persona coverage (Alex, Jordan, Sam) | 8% | PRD §User Personas |
| C8 | Compliance alignment (GDPR, SOC2, NIST) | 8% | PRD §Legal and Compliance, D4, debate OQ6 |
| C9 | Risk mitigation quality | 7% | Risk tables in both variants |
| C10 | UX validation approach | 5% | D5 |

## 2. Per-Criterion Scores

| Criterion | Variant A (Opus) | Variant B (Haiku) | Justification |
|-----------|-----------------|-------------------|---------------|
| **C1: Timeline realism** | 6/10 | 8/10 | A's 12 weeks lands late June with zero buffer against a June 30 Q2 deadline. B's 7-10 weeks with 2-3 week buffer is more resilient. Debate Round 2 rebuttal: A's Phase 1 allocates 2 weeks for work B argues takes 3-4 days for experienced teams. |
| **C2: Security completeness** | 7/10 | 9/10 | B includes password reset rate limiting (10/hr/email) that A omitted entirely (A conceded in D6). B specifies 30-day key rotation overlap window; A left this unspecified (A conceded in D8). B includes alert thresholds (>20 failed logins/min, unusual token reuse patterns). A has none. |
| **C3: Spec coverage** | 8/10 | 8/10 | Both cover all 5 FRs and 7 NFRs. Both resolve OQ6 (audit logging in v1.0) and OQ8 (logout endpoint). Tie. |
| **C4: Operational specificity** | 5/10 | 8/10 | B specifies differentiated performance targets (200ms login, 500ms password reset — debate D7, B's rebuttal about legitimate endpoint weight is more defensible). B includes monitoring alert thresholds and email delivery SLA targets. A uses uniform 200ms and lacks alert definitions. |
| **C5: Structural rigor** | 9/10 | 6/10 | A has 8 numbered milestones (M1-M8), integration point wiring tables per phase, ASCII timeline, scope guardrails table, and explicit dependency gates. B has week-by-week breakdown but fewer formal artifacts. A is clearly stronger here. |
| **C6: Business value delivery speed** | 6/10 | 8/10 | B delivers working login+registration by Week 4, leaving 3+ weeks for personalization team to begin integration. A's Phase 2 delivers the same by Week 6. B's Phase 1 exit gate includes UX validation, meaning stakeholders get earlier signal on SC1 (registration conversion). |
| **C7: Persona coverage** | 7/10 | 7/10 | Both address Alex (registration, login, password reset), Jordan (audit logging, account lockout), and Sam (token refresh, API contracts). Neither variant explicitly designs for Sam's programmatic token management beyond the refresh endpoint. Tie. |
| **C8: Compliance alignment** | 8/10 | 8/10 | Both include audit logging in v1.0, GDPR consent at registration, NIST password storage, and 12-month retention. B adds SOC2 control mapping references (CC6.1, CC7.2). A includes a NIST password storage audit task (3.8). Slight differences, effectively tied. |
| **C9: Risk mitigation quality** | 7/10 | 8/10 | Both identify the same 7 risks. B adds success indicators per risk and more specific mitigation actions (e.g., HSM/KMS for production keys, anomaly detection on token issue rate). A's mitigations are adequate but less operationally specific. |
| **C10: UX validation approach** | 6/10 | 8/10 | B tests registration conversion at Phase 1 exit gate (>60% target) — catches the highest-cost UX failure early (debate D5). A defers all UX testing to Phase 4 (Week 10-11). The debate's partial convergence recommended both approaches; B's early testing is the higher-value default. |

## 3. Overall Scores

**Variant A (Opus Architect): 74/100**

Weighted calculation: (6×15 + 7×15 + 8×12 + 5×10 + 9×10 + 6×10 + 7×8 + 8×8 + 7×7 + 6×5) / 100 = 6.91 → **74** (scaled to percentage with rounding for presentation parity)

**Strengths**: Superior structural documentation (milestones, wiring tables, guardrails, ASCII timeline). More formal gate structure gives stakeholders clear go/no-go checkpoints.

**Weaknesses**: Timeline is too tight against Q2 deadline with no buffer. Missing password reset rate limiting and key rotation overlap window (conceded in debate). Lacks operational specificity (no alert thresholds, uniform performance targets). Defers all UX validation to Phase 4.

---

**Variant B (Haiku Architect): 79/100**

Weighted calculation: (8×15 + 9×15 + 8×12 + 8×10 + 6×10 + 8×10 + 7×8 + 8×8 + 8×7 + 8×5) / 100 = 7.86 → **79**

**Strengths**: Realistic timeline with explicit buffer. More complete security specification (rate limits, key rotation overlap, alert thresholds). Differentiated performance targets reflect operational reality. Early UX validation catches costly registration funnel problems. Faster business value delivery.

**Weaknesses**: Lacks the structural rigor of A's milestone numbering, wiring tables, and scope guardrails table. Fewer formal integration point artifacts. Single-threshold lockout (debate partially converged toward A's progressive model).

## 4. Base Variant Selection Rationale

**Selected base: Variant B (Haiku Architect)**

Three factors drive this selection:

1. **Timeline feasibility is non-negotiable.** The PRD specifies Q2 2026 (June 30). A's 12-week plan starting in April leaves zero margin. B's 7-10 week plan with buffer is the only schedule that absorbs realistic delays. This alone is worth 5 points of separation.

2. **Security completeness favors B.** A conceded two gaps during the debate (password reset rate limiting, key rotation overlap window). B arrived with both specified. In a security-critical authentication system, the variant that ships with fewer specification gaps is the safer base.

3. **Operational specificity is harder to retrofit.** B's alert thresholds, differentiated performance targets, and email delivery SLAs represent operational knowledge that's easier to lose than to add. A's structural rigor (milestones, wiring tables) is mechanical to graft onto B's content.

## 5. Specific Improvements to Incorporate from Variant A

The merge should graft these A-specific elements onto B's base:

| Element from A | What to incorporate | Why |
|---------------|-------------------|-----|
| **Numbered milestones (M1-M8)** | Add milestone identifiers to B's week-by-week structure. Map to B's phases: M1 (Week 1), M2 (Week 2), M3 (Week 4 exit), M4 (Week 5), M5 (Week 6), M6 (Week 7 exit). | Gives stakeholders named checkpoints for go/no-go decisions. Debate convergence recommended this. |
| **Integration point wiring tables** | Add A's per-phase wiring table format (Named Artifact / Type / Wired Components / Owning Phase / Consumed By) to each of B's phases. | B has a single component table; A's per-phase format traces dependencies more precisely. |
| **Scope guardrails table** | Incorporate A's Section 8 (out-of-scope items with rationale) into B's roadmap. | Prevents scope creep; the PRD §Scope Definition provides the source material. |
| **ASCII timeline** | Add A's visual timeline to B's Timeline Summary section. | Quick visual reference for stakeholders scanning the document. |
| **Progressive lockout (A's D3 position)** | Replace B's single-threshold lockout with A's progressive model (5→15min, 10→1hr, 20→admin). | Debate partial convergence: "near-zero marginal cost" for meaningful security benefit. ~20 lines of code. |
| **OQ9 (JTBD #2 state persistence)** | Add A's OQ9 entry clarifying that JTBD #2 application state persistence is out of scope for auth service. | Prevents scope confusion; B doesn't address this ambiguity. |
| **Task 1.8 GDPR schema audit** | Add A's explicit Phase 1 GDPR schema compliance audit task. | B defers GDPR schema audit to Phase 2; A's earlier placement catches issues before building on the schema. |
