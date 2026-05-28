# Merge Log

## Inputs

- variant-1-opus-analyzer.md
- variant-2-opus-architect.md
- variant-3-sonnet-security.md
- variant-4-haiku-devops.md
- variant-5-sonnet-scribe.md

## Operations Performed

1. Selected Variant 4 (devops) as merge base — see `base-selection.md`.
2. Folded Variant 1 telemetry hardening into Foundation wave (Week 0-1 parallel lane).
3. Folded Variant 2 key-id-in-header design + PCI board submission into Foundation wave; deployment lands Week 4-5.
4. Folded Variant 3 PCI scope-mapping table + artifact repository discipline into Foundation wave as compliance-infra lane.
5. Folded Variant 5 three artifact skeletons + single-comms-channel cadence into Foundation wave as comms-infra lane.
6. Reconciled key-rotation timeline: hotfix (Variant 4) Week 0; durable key-id-in-header (Variant 2) Week 4-5 supersedes hotfix.
7. Deferred per-merchant circuit breaker (Variant 2) to Q2 — out of program scope.
8. Deferred HPA pin-up duration question to Q2 with explicit revisit checkpoint.
9. Deferred key-id-in-header opt-in-vs-transparent technical question to PCI board.
10. Synthesized Risk Register from all 5 variants' "Risks Foregrounded" sections, deduplicated.

## Conflicts Resolved

- **C1 — Stabilization timing:** V1 (post-RCA) vs. V4 (Week 0). Resolved in favor of V4 because the 14-day validation window cannot close before the Mar 28 change-freeze under V1's sequencing. V1's evidence concern is addressed by overlaying telemetry hardening in parallel Week 0-1.
- **C2 — Key-rotation depth:** V2 (key-id-in-header) vs. V4 (hotfix). Resolved as both/and: hotfix Week 0 as transitional measure; durable Week 4-5 deployment.
- **C3 — Per-merchant circuit breaker:** in-scope (V2) vs. deferred (V1+V4). Resolved as deferred to Q2 — not part of mandated control set.
- **C4 — RCA artifact maturity Week 3:** skeleton + evidence-drafts (V1+V5 agree) vs. nearly-final (V4 implicit). Resolved in favor of V5's "populate as evidence arrives" pattern with weekly engineering reviews.

## Conflicts Deferred (not resolved in this merge)

- **D1 — HPA pin-up permanence:** 4-week temporary (V4) vs. permanent (V2). Deferred to Q2 planning with explicit revisit checkpoint at program close.
- **D2 — Key-id-in-header opt-in vs. transparent:** V2 favors opt-in (safer for legacy verifiers); V4 favors transparent dual-acceptance. Deferred to PCI secure-change-review board's technical scoping.

## Convergence Score

**0.79** — exceeds the 0.75 target. Agreement on spine + overlay structure; remaining tensions are scoping deferrals, not contradictions on the core program structure.
