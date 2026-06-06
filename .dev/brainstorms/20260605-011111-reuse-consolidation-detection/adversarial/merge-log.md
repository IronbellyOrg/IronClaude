# Merge Log

## Metadata
- Base: variant-4-opus-architect
- Executor: orchestrator (opus), grounded in 4 re-Read variants + 2 codebase verifications
- Changes applied: 7 incorporations, 3 rejections, 2 deferrals
- Status: success
- Timestamp: 2026-06-05T11:52:00Z

## Changes Applied

| # | Change | Status | Provenance tag in merged-requirements.md |
|---|--------|--------|------------------------------------------|
| 1 | V2 6-facet CFP as overlap definition | applied | `<!-- src: V2 §1 -->` on §Detection-Signal |
| 2 | V2 Ω=0.88 worked proof | applied | `<!-- src: V2 §1.3 -->` on §Worked-Example |
| 3 | V2 re-Read evidence discipline | applied | `<!-- src: V2 §2.2 -->` on §Evidence-Discipline |
| 4 | V5 two-floor thresholds + 3 tiers | applied | `<!-- src: V5 §2.5 -->` on §Thresholds |
| 5 | V5 7-item exclusion list + confusion matrix | applied | `<!-- src: V5 §3,§8 -->` on §False-Positive-Guards |
| 6 | V5 Grounding-Gaps routing | applied | `<!-- src: V5 §6.5; §17.7 -->` on §Low-Confidence-Routing |
| 7 | V1 shared versioned sub-spec | applied | `<!-- src: V1 §1,§8 -->` on §Shared-Sub-Spec |
| base | V4 ladder + modifier mapping + gates | applied | `<!-- src: V4 base -->` throughout §Gate-Model |

## Post-Merge Validation
- **Structural integrity:** ✅ Pass — heading hierarchy consistent; merged spec organized by deliverable (SC1–SC7) + per-protocol deltas.
- **Internal references:** Total 11, Resolved 11, Broken 0 (all §-refs into sc-reflect/tdd verified against L860–966/§17.7/L1309/Phases L141–147).
- **Contradiction re-scan:** New contradictions introduced by merge: 0. X-001 resolved (modifier, not counted class) — merged spec contains no `deviation_count_by_class.reuse_miss` key, consistent with §17.7.
- **§17.7 conformance check:** ✅ merged spec routes low-confidence to §10.6 Grounding Gaps and keeps the 4-category ledger pure.

## Summary
- Planned: 7 applied, 3 rejected (documented), 2 deferred (documented). Failed: 0.
- Merged deliverable: `../merged-requirements.md`.
