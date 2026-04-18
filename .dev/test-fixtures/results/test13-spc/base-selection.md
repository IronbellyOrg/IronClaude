---
base_variant: opus-architect
variant_scores: "A(opus):78 B(haiku):70"
---

# Evaluation Report

## 1. Scoring Criteria (Derived from Debate)

| Criterion | Weight | Source in Debate |
|---|---|---|
| C1. Gating discipline / rollback precision | 15% | Divergence #1, #3, #5; Round 1 Opus arg 1 |
| C2. Timeline realism (reliable vs optimistic) | 15% | Round 1 Haiku arg 1; Round 2 Opus rebuttal 1 |
| C3. Dependency ordering correctness | 10% | Round 2 Haiku rebuttal on crypto isolation |
| C4. Refresh/Reset coupling decision | 10% | Round 1 Opus arg 5; Round 2 both sides |
| C5. GAP ownership / v1.1 handoff | 10% | Round 1 Haiku arg 5; Round 2 both sides |
| C6. OI-7 (email provider) gating | 10% | Round 1 Opus arg 6; Round 2 Haiku rebuttal |
| C7. Operational readiness (rollout/APM/runbooks) | 10% | Both M6/M4 rollout content |
| C8. Test coverage granularity | 5% | Convergence assessment |
| C9. Risk register completeness | 10% | Risk tables compared |
| C10. Scope discipline / deliverable specificity | 5% | Artifact counts |

## 2. Per-Criterion Scores

| Criterion | Variant A (Opus) | Variant B (Haiku) | Evidence |
|---|---|---|---|
| C1. Gating | 9 | 6 | A: 6 bounded milestones. B: bundles HIGH-risk M2/M3/M4 |
| C2. Timeline realism | 7 | 6 | A: reliable 12w. B: optimistic 8w with 3 HIGH-risk MLS stacked |
| C3. Dependency ordering | 6 | 8 | B follows conventional primitives→orchestrator; A's crypto-isolation M2 is anomalous (debate LEANS HAIKU) |
| C4. Refresh/Reset coupling | 9 | 6 | A's P0/P1 isolation structurally stronger (debate LEANS OPUS) |
| C5. GAP ownership | 5 | 9 | A uses risk-register only (R4/R5/R12). B creates GAP-1/2/3 owned deliverables (debate LEANS HAIKU) |
| C6. OI-7 gating | 9 | 6 | A gates M5 on OI-7; B accepts in-flight (debate LEANS OPUS for OI-7) |
| C7. Operational readiness | 9 | 7 | A dedicates M6 (APM+PagerDuty+rollout runbook OPS-007). B compresses into M4 |
| C8. Test coverage granularity | 8 | 6 | A: TEST-M1-001…TEST-M6-002 per-MLS. B: TEST-001/002/003 consolidated |
| C9. Risk register | 9 | 6 | A: 13 entries with owners. B: 7 entries |
| C10. Deliverable specificity | 8 | 7 | A: 63 deliverables. B: 40 deliverables |

## 3. Overall Weighted Scores

**Variant A (Opus):** (9×15 + 7×15 + 6×10 + 9×10 + 5×10 + 9×10 + 9×10 + 8×5 + 9×10 + 8×5) / 10 = **78**

**Variant B (Haiku):** (6×15 + 6×15 + 8×10 + 6×10 + 9×10 + 6×10 + 7×10 + 6×5 + 6×10 + 7×5) / 10 = **70**

**Justification:** A wins on structural rigor (C1, C4, C6, C7, C9) where the debate either LEANS OPUS or A demonstrates materially greater content depth. B wins meaningfully only on GAP ownership (C5) and conventional dependency ordering (C3). The unresolved 12w-vs-8w timeline debate does not swing scoring because B's 8w depends on 3 stacked HIGH-risk milestones shipping cleanly — higher variance against the same target.

## 4. Base Variant Selection Rationale

**Selected base: Variant A (Opus, 6-MLS/12w)**

Reasons:
1. **Structural correctness on contested points:** Debate explicitly LEANS OPUS on refresh/reset decoupling and OI-7 gating — two of the six dispute axes. Haiku wins only cosmetic (SEC-IDs) and procedural (GAP ownership) points.
2. **Greater deliverable density:** 63 deliverables, 13 risks, per-milestone test IDs, per-milestone integration tables. Merging from A→B loses specificity; merging B→A only adds specificity.
3. **Dedicated rollout milestone (M6):** OPS-005/OPS-007/NA.1/NA.2/TEST-M6-001/002 form a discrete validation gate. Haiku's M4 mixes hardening with deferred-gap planning, weakening the cutover contract.
4. **Reset isolation preserves P1 escape hatch:** If reset slips, refresh still ships on schedule (Opus arg 5, Round 1).
5. **OI-7 as hard gate matches spec reality:** Email provider selection blocks concrete DEP-003/COMP-010 contract work.

## 5. Specific Improvements to Incorporate from Variant B (Haiku)

| # | Improvement | Source in Haiku | Where to Merge in A |
|---|---|---|---|
| 1 | Convert GAP-1/2/3 from risk-register entries (R4/R5/R12) to **owned planning deliverables** with explicit v1.1 handoff targets | Haiku M4 rows 36–38 (GAP-1/GAP-2/GAP-3 with owners) | Add 3 new deliverables to A's M6 or Risk Assessment section; assign owners (Security, Architect, Product) |
| 2 | Accept **OI-2 (refresh-token cap) as in-flight decision** rather than hard gate | Haiku M4 OI-2 row | Update A's Open Questions table: move OI-2 resolution target to M4 kickoff, not blocking |
| 3 | Add **COMP-017 account suspension hook** as explicit deliverable (forward-compatible with progressive lockout) | Haiku M3 row 28 | Insert into A's M3 as SEC-007 or extend COMP-008 |
| 4 | Add explicit **COMP-016 refresh cookie policy** deliverable (not just acceptance criterion) | Haiku M3 row 27 | Promote A's implicit httpOnly cookie requirement in API-003 AC to a dedicated SEC deliverable in M4 |
| 5 | Add **OI-1 resolution as an M5-kickoff deliverable row**, not just an OQ table entry | Haiku M3 row 30 (OI-1) | Promote OI-1 to a scheduled decision deliverable at M5 entry in A |
| 6 | Strengthen M4/M6 **go-live checklist** as an explicit deliverable with phase-1→phase-2 cutover evidence | Haiku M4 row 40 (OPS-003) | Merge into A's OPS-007 runbook or add OPS-008 go-live checklist |
| 7 | Add **health endpoint + dependency status reflection** (keys/DB/email) as distinct deliverable | Haiku M4 row 39 (COMP-018) | Expand A's OPS-005 AC or add OPS-009 |

## 6. Items Explicitly Rejected from Haiku

- **4-milestone compression:** Rejected. Bundles HIGH-risk M2/M3/M4 and violates reset isolation (debate LEANS OPUS).
- **Foundation+primitives bundling in M1:** Rejected. A's crypto isolation in M2 aligns with OPS-006 rotation-policy ownership; splitting forces rotation policy into foundation work.
- **SEC→COMP ID rename:** Rejected. Debate marks as cosmetic; A's SEC-001…SEC-006 scheme better serves audit traceability even if not objectively superior.
- **8-week timeline:** Rejected. Merge preserves 12-week cadence; B's velocity argument requires stakeholder input not available here.
