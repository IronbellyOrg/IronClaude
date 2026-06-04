# Refactor Plan

## Overview

- Base: Variant 3 (haiku:analyzer)
- Incorporating from: V1 (5 changes), V2 (5 changes)
- Total planned changes: 10
- Risk: Low overall — base is already the smallest viable; additions are leaf changes

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale | Risk |
|---|---|---|---|---|---|---|
| 1 | Add soft fallback ladder | V1 risk-mitigation | New `## Failure-Mode Fallback` after Eval Methodology | Append | If Haiku-pure fails eval bar, parent permits Haiku-classify + Opus-pipeline on miss only. Load-bearing if Haiku regresses materially. | Low |
| 2 | Add `prompt_envelope_template` field to schema | V2 schema | `## Table Schema` row template | Append field | Stores hand-off skeleton directly so hot path emits without re-deriving | Low |
| 3 | Add JSONL telemetry section as MVP | V2 (U-009) | Add `## Telemetry` section before `## Eval Methodology` | New section | Required for kill-switch decision (below 60% disable); 5 fields only (timestamp, mode, cache_result, classification_key, duration_ms) | Low |
| 4 | Add 4K-8K hot-path budget gate | V2 (U-008) | `## Hot-Path Control Flow` step 5 | Inline note | Concrete decision criterion: "if hot-path tokens exceed 10K, fall to cold path" | Low |
| 5 | Add kill switch | V2 | `## Telemetry` section | Append | "If rolling 50-invocation hit rate < 60% after 2 weeks of real usage, disable cache and keep only instrumentation. Below 70% but ≥ 60%, keep measuring." | Low |
| 6 | Add condensed cold-path runbook | V1 risk #6 | `## Cold-Path Control Flow` | Append note | Cold-path Haiku must NOT inline full SKILL.md (re-creates the cost the cache removes). Use a ~50-line condensed runbook. | Low |
| 7 | Add `cache_miss: low_confidence` signal | V1 (U-003) | `## Hot-Path Control Flow` between steps 4-5 | Inline | Cheap ambiguity check: if classifier's top-2 categories within 10% score → cache_miss, fall to cold path. NO extra LLM call. | Low |
| 8 | Add `classifier_score_hints` to scaling path | V1 (U-001) | `## Scaling Path` (NEW section) | Append | When surface > 200 entries OR inlined-table tokens > 8K, add O(N) string pre-filter | Low |
| 9 | Add plugin TTL bands to scaling path | V2 (U-007) | `## Scaling Path` | Append | When `--plugin` table arrives in phase 2: 24h hosted, 7d community repos | Low |
| 10 | Add `last_validated_at` to schema | V2 (U-006) | `## Table Schema` row template | Append field | Already present in V3 schema; just standardize the field name with V2's convention | Low |

## Changes NOT Being Made

| Rejected change | Variant | Rationale (citing debate evidence) |
|---|---|---|
| Source-file keying (V1 C-001) | V1 | V3's 46% Auggie cost finding makes request-keying the more efficient cut. V1's keying is recorded as the scaling fallback if classification_key fragmentation becomes a real problem (V1's own risk #3). |
| JSON storage (V2 C-002) | V2 | YAML wins on project-consistency (matches existing `.roadmap-state.json` is the lone JSON; all skill artifacts are YAML/MD). V2's "Haiku parses JSON more deterministically" is real but not load-bearing at ~30-row scale. |
| Explicit confidence threshold gate (V2 X-001) | V2 | V3's argument wins: a separate confidence-score LLM step is bloat. V1's free top-2-within-10% check (planned change #7) gives the same ambiguity detection at zero extra cost. |
| Hand-curated row pre-seeding (V2's MVP step) | V2 | V3's lazy population + cold-path write-back is simpler. Hand-seeding rows before evals run risks bias toward the eval-shaped requests. |
| Full 13-section structure (V2) | V2 | V3's 12-section structure with "Does NOT Do" sharpens scope better than V2's separate "Cost Analysis" + "Unverified Premises" sections. Merging them is cleaner. |
| 24-run eval matrix (V2 C-003) | V2 | V1's 18-run 2×3 (Opus-cold + Haiku-cold + Haiku-warm) gives the same information at 75% the cost. Haiku-cold is the Haiku-capability ceiling; Haiku-warm is the target; Opus-cold is the floor. |

## Risk Summary

All planned changes are additive or annotation-level. No restructuring of V3's core architecture. The merged document grows by approximately 30% (from V3's ~1900 words to ~2500 words) — still well under V1/V2 size.

## Review Status

Auto-approved (no --interactive). Documented for reproducibility.
