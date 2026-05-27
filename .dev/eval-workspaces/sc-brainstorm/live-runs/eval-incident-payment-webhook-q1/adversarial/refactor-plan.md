# Refactor Plan — Variant 4 Base + Overlays from V1/V2/V3/V5

## Goal

Produce a single coherent Q1 Incident-Response Program specification that:

- Uses Variant 4 (devops) as the stabilization spine.
- Overlays Variant 1 (analyzer) telemetry-hardening as a parallel Week 0-1 lane.
- Overlays Variant 2 (architect) key-id-in-header as the durable Week 4-5 deployment, submitted to PCI board Week 0.
- Adopts Variant 3 (security) PCI scope mapping + artifact repository discipline.
- Adopts Variant 5 (scribe) artifact templates + single-comms-channel cadence.

## Refactor Operations

1. **Reframe Variant 4 Week 0-1 as a "Wave 0 — Foundation" containing four parallel lanes** (stabilization, telemetry, compliance-infra, comms-infra). This eliminates the variant-internal contradiction where Variant 4 implicitly deprioritises non-stabilization work.
2. **Insert Variant 1's telemetry-hardening checklist** into the Foundation wave's telemetry lane. Trim items that overlap with Variant 4's basic SLO dashboard.
3. **Insert Variant 2's PCI board submission as a Foundation deliverable** rather than a Week 2 event. Key-id-in-header design doc must land Day 3 to clear 2-week lead time.
4. **Add Variant 3's artifact repository + PCI scope-class table** as a Foundation deliverable. Owner: security engineering lead.
5. **Add Variant 5's three artifact skeletons** (RCA narrative, merchant comms, steerco status) as Foundation deliverables. Owner: incident commander.
6. **Reconcile stabilization timing:** Variant 4 stabilization (HPA pin, retry-budget, connection-pool, key-rotation hotfix) lands Week 0-2. Validation window per Variant 4 starts Week 3 latest, must close before Mar 28 change-freeze.
7. **Resolve key-rotation tension:** Variant 4 hotfix (cache-flush + 30s grace window) is the Week 0 intervention. Variant 2 key-id-in-header is the Week 4-5 durable deployment that supersedes the hotfix. Both are in scope; the hotfix is explicitly transitional.
8. **Defer per-merchant circuit breaker (Variant 2)** to Q2 — out of program scope. Document as recommended follow-up in the merged spec.
9. **Defer permanent vs. temporary HPA pin-up question** to Q2 — current spec adopts Variant 4's 4-week temporary measure with explicit revisit checkpoint.
10. **Defer key-id-in-header opt-in-vs-transparent technical question** to the PCI board's secure-change-review process — current spec commits to the policy that the change is non-breaking from the merchant perspective by default.

## Section-by-Section Mapping

| Merged Section | Source |
|---|---|
| Background / Problem Statement | Seed brief Problem Statement |
| Goals + Success Criteria | Seed brief Success Criteria + Variant 3 Apr 12 gate emphasis |
| Constraints | Seed brief Constraints (verbatim) |
| Program Structure (waves) | Variant 4 spine + Variant 1/2/3/5 overlays per ops above |
| Mandated Preventive Controls | Seed brief Success Criteria (per-merchant SLO alerting + key-rotation safety harness) + Variant 2 key-id-in-header as the durable substrate |
| Comms + Artifact Discipline | Variant 3 PCI scope-mapping + Variant 5 templates + cadence |
| Risk Register | Synthesized from all 5 "Risks Foregrounded" sections |
| Open Questions / Deferred Decisions | Three open tensions from debate Round 3 + seed brief Open Questions |

## Convergence Validation

All 5 variant authors would endorse the merged spec on the spine + overlay model — no variant content is overruled in a way that contradicts its core stance; the merge respects each variant's load-bearing claim.
