# Refactor Plan — merge into V4 base

## Overview
- Base: variant-4 (gate-placement). Incorporated: V2, V5, V1 (selective). Lost lens compensated: refactorer/simplicity → §Simplicity-Guard.
- Change count: 7 incorporations, 3 rejections, 2 deferrals.
- Overall risk: Low (all grafts are additive to a correct spine).

## Planned Changes

| # | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|--------|----------------|----------|------------------------------|------|
| 1 | V2 §1 (CFP) | base §6 overlap definition | replace thin formula with 6-facet Capability Fingerprint; keep V4's cap+skel-dominant weighting | S-003 winner 80%; only variant with a worked proof | Low |
| 2 | V2 §1.3 | merged §worked-example | import the Ω=0.88 calculation verbatim as the canonical acceptance example | U-003; proves the metric fires where naming fails | Low |
| 3 | V2 §2.2 | merged §evidence-discipline | every neighbour re-Read at file:line before citation; unverifiable hit → discard (`reuse_hit_unverified`) | rides existing §6.2; C4 | Low |
| 4 | V5 §2.5 + §3 | merged §thresholds | add per-dimension floors C_cap≥0.80 ∧ C_shape≥0.70 atop S_reuse≥0.82; 3-tier (confident/maybe/distinct) | C-001 winner 82%; strongest FP guard | Low |
| 5 | V5 §3 + §8 | merged §false-positive-guards | adopt the 7-item exclusion list + confusion matrix verbatim | U-004 | Low |
| 6 | V5 §6.5/§10.6 routing | merged §grounding-gaps | route maybe-related + insufficient-grounding to §10.6 Grounding Gaps (NOT a finding) | U-005; §17.7-sanctioned | Low |
| 7 | V1 §1/§8/§9 | merged §shared-sub-spec | single versioned `refs/reuse-audit.md` both SKILLs reference; named extension points | S-004 winner 85%; dogfoods extract-shared | Low |

## For each base weakness addressed
- Base V4 `overlap` formula was a sketch → fixed by change #1 (V2 CFP).
- Base V4 lacked an explicit exclusion list → fixed by change #5 (V5).
- Base V4 low-confidence handling was "advisory REPORT note" → upgraded to §10.6 Grounding Gaps (change #6), the protocol-sanctioned channel.

## Changes NOT being made (transparency)
- V1 §10.8 counted `reuse_miss` deviation class + §14.5.2 cond-4b → **REJECTED** (X-001 / §17.7 L1742). The merge uses V4's modifier-maps-to-Drift/Regression instead; output-contract fields are *finding/advisory* counts, never a `deviation_count_by_class` key.
- V5 pre-stage hard-block carve-out → **REJECTED**; pre-stage stays advisory (advisory-strong max).
- V1 ×1.1 advisory→blocking bridge multiplier → **DEFERRED** (INV-003). Post-stage re-detects independently; bridge needs a persistence channel that does not yet exist.

## Simplicity-Guard (compensating for the lost refactorer lens)
The three opus variants trend toward elaborate machinery. The merge deliberately keeps **only load-bearing** mechanism and marks the rest deferred:
- KEEP: one mandatory auggie capability-query per new symbol; composite signal w/ two floors; map to Drift/Regression; Grounding-Gaps for low-confidence; 4-verdict vocab w/ mechanical NFR downgrade; pre=advisory/post=block@L3.
- DEFER (named in merged spec §Deferred): version-contract minor-bump ceremony, ×1.1 bridge multiplier, the 5-item extension-point catalogue (keep 2: open verdict enum + pluggable import-legality source), `superclaude reuse-audit` CLI.
- The merged spec must catch the ground-truth case with the KEEP set alone (verified: Ω=0.88 → confident-duplicate → extract-shared → Drift@post → blocks §14.5.2 cond-4). Anything not needed for that is deferred.

## Review status: auto-approved (non-interactive).
