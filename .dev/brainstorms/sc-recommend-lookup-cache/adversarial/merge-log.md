# Merge Log

## Metadata

- Base: Variant 3 (haiku:analyzer)
- Executor: orchestrator (inline merge, no separate merge-executor agent — see methodology_notes in return-contract.yaml)
- Total planned changes: 10
- Applied: 10
- Failed: 0
- Status: success
- Timestamp: 2026-06-02T14:25:00Z

## Changes Applied

| # | Title | Status | Provenance tag in merged-requirements.md | Validation |
|---|---|---|---|---|
| 1 | Add soft fallback ladder | ✅ applied | `## Eval Methodology — Haiku vs Opus > Failure-mode fallback ladder` (Source: V1 risk-mitigation) | Section added; ladder is the only block under that subheading |
| 2 | Add `prompt_envelope_template` field | ✅ applied | `## MVP Architecture > Storage` (Source: V3 base + V2 graft) | Field present in YAML example; described in row comments |
| 3 | Add JSONL telemetry section | ✅ applied | `## Telemetry (MVP)` (Source: V2 load-bearing) | Section exists; 5 fields documented; kill switch wired in |
| 4 | Add 4K-8K hot-path budget gate | ✅ applied | `## Hot-Path Control Flow > step 8` (Source: V2) | Step 8 is the explicit circuit breaker |
| 5 | Add kill switch | ✅ applied | `## Telemetry > Kill switch` (Source: V2) | 3 bands (≥80%, 60-80%, <60%); <60% disables cache |
| 6 | Add condensed cold-path runbook | ✅ applied | `## Cold-Path Control Flow > step 1` (Source: V1 risk #6) | "~50-line condensed cold-path runbook, NOT the full 225-line SKILL.md" explicit |
| 7 | Add `cache_miss: low_confidence` signal | ✅ applied | `## Hot-Path Control Flow > step 4` (Source: V1) | "NO extra LLM call" explicitly noted |
| 8 | Add `classifier_score_hints` to scaling path | ✅ applied | `## Scaling Path > item 1` (Source: V1) | "when inlined-table tokens > 8K or surface > 200 entries" |
| 9 | Add plugin TTL bands | ✅ applied | `## Plugin Table` body + `## Scaling Path > item 2` (Source: V2) | "24h hosted, 7d community repos" |
| 10 | Add `last_validated_at` field | ✅ applied | `## MVP Architecture > Storage` (Source: V3 + V2 convention) | Field present in YAML example |

## Post-Merge Validation

| Check | Result | Details |
|---|---|---|
| Structural integrity (heading hierarchy) | ✅ pass | No level skips; 9 H2 sections under H1; subsections appropriately nested |
| Internal references resolve | ✅ pass | Cross-references to `convergence.py`, `sc:task-protocol`, eval files, and current `sc-recommend/SKILL.md` all point to extant paths in the worktree |
| Contradiction rescan | ✅ pass | Zero new contradictions introduced by merge; X-001, X-002, X-003 from diff-analysis resolved in the merged spec (gating, telemetry, native-cache) |
| Provenance annotations present | ✅ pass | HTML comments mark base + per-section source attribution for each grafted change |
| R3 (no protocol reimplementation) preserved | ✅ pass | `prompt_envelope_template` is explicitly the hand-off skeleton, NOT a restatement of the target's protocol |

## Summary

- Planned: 10 changes
- Applied: 10 (100%)
- Failed: 0
- Skipped: 0

The base (V3) already represented the smallest viable proposal. All grafts are additive risk-mitigation (fallback ladder), measurement (telemetry, kill switch), or implementation detail (envelope template, validation cross-checks). No restructuring of V3's core control flow was required.
