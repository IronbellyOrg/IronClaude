# Diff Analysis — 5 Variants Compared

## Dimension Matrix

| Dimension | V1 analyzer | V2 architect | V3 security | V4 devops | V5 scribe |
|---|---|---|---|---|---|
| Primary lever | Telemetry-first RCA | Structural controls (key-id, circuit breaker) | Compliance gates | Stabilization quick wins | Narrative + comms artifacts |
| First action (Week 0) | Trace tags, retry-amp metric | Joint design with Q2 team | PCI scope mapping + artifact repo | HPA pin-up, retry-budget tuning | Artifact spine + stakeholder map |
| Stabilization timing | Week 5+ (post-RCA) | Week 2 (parallel) | N/A (gates everything) | Week 0-1 (priority) | N/A (out of scope) |
| Key-rotation fix | Defer to RCA | Key-id-in-header (durable) | Submit Week 0 to clear PCI | Hotfix (cache flush + grace window) | Document in RCA |
| Auditor strategy | Evidence-chain narrative | Architecture-decision-records | Continuous evidence collection | Stabilized-then-explained | Templated artifact spine |
| Merchant comms | Defer until RCA signed | Breaking-change opt-in messaging | Legal-gated, batched | Direct + frequent | Single-channel, weekly cadence |
| Risk if wrong | Slow visible relief | Scope creep past Apr 12 | Engineering starvation | PCI emergency-change abuse | Substance-over-narrative drift |

## Agreement Surface

All 5 endorse:

- Day-0 parallel work (no single-lane sequencing).
- Two mandated preventive controls land before Week 5.
- PCI Level 1 cadence is the binding calendar constraint.
- Single comms channel through legal + customer success.
- 14-day validation window must close before Mar 28 change-freeze.
- "Do nothing structural" steel-man is rejected.

## Divergence Surface

- **Calendar of stabilization:** Week 0-1 (devops, architect) vs. Week 5+ (analyzer); security treats it as PCI-gated; scribe defers to engineering decision.
- **Key-rotation fix depth:** hotfix (devops) vs. key-id-in-header (architect) vs. evidence-deferred (analyzer); security gates the choice on PCI lead time.
- **Per-merchant circuit breaker:** in scope (architect) vs. deferred (analyzer, devops) vs. compliance-neutral (security) vs. scope-irrelevant (scribe).
- **HPA pin-up duration:** 4 weeks temporary (devops) vs. permanent (architect).
- **RCA artifact maturity at week 3:** skeleton + evidence drafts (scribe + analyzer agree) vs. nearly final (devops favors).

## Synthesis Recommendation

Take Variant 4's (devops) Week 0-1 stabilization spine because it addresses the dominant immediate risk (SLA credit run-rate + enterprise renewal threat) while not blocking other workstreams. Layer Variant 1's (analyzer) telemetry hardening in parallel (Week 0-1) because it is the precondition for a defensible RCA without delaying stabilization. Use Variant 2's (architect) key-id-in-header as the durable fix submitted to the PCI board Week 0 — accept that it lands Week 5, not Week 1. Adopt Variant 3's (security) artifact-repo + PCI-scope-mapping discipline as the calendar spine. Adopt Variant 5's (scribe) artifact templates + single-comms-channel cadence to manage the political failure mode.

This is a true synthesis — no single variant wins; the merge takes the load-bearing element from each.
