# Merge Log

## Metadata
- Base: Variant 1 (C-canonical)
- Executor: in-context (fallback_mode=true)
- Changes applied: 6 + 2 binding preconditions
- Status: success
- Timestamp: 2026-06-20 ~06:15 UTC
- Output: `/config/workspace/IronClaude/.dev/reflect-hardening/adversarial-uc2-reachability-design/decision-canonical-uc2-reachability.md`

## Changes Applied

| # | Change | Provenance tag | Validation |
|---|---|---|---|
| 1 | C retains contract 1.6.0 | Base (original) | ✅ consistent with base-selection 0.880 |
| 2 | B re-pointed off 1.6.0 (1.7.0 or telemetry) | Variant 2, refactored under guard | ✅ resolves M-028; (b) flagged needs_human_decision |
| 3 | Eval id re-allocation | Variant 1 first; Variant 2 rebased | ✅ resolves M-031; INV-003 |
| 4 | B rebases SKILL.md/taxonomy onto post-C baseline | Variant 2, modified | ✅ resolves M-029; INV-004 |
| 5 | C-040 intent → B-side guard | Variant 1 §C-040 → Variant 2 | ✅ resolves M-030 without discard |
| 6 | M-008 debate ownership update | matrix M-008/M-042 | ✅ resolves M-042 |
| P-1 | Precedence invariant (C Regression dominates B degrade) | invariant-probe INV-001 | ✅ incorporated as binding precondition |
| P-2 | Sufficiency closure of #2–#6 | invariant-probe INV-002 | ✅ incorporated as binding precondition |

## Post-Merge Validation
- **Structural integrity:** ✅ decision doc has clear ownership hierarchy (C gate / B advisory).
- **Internal references:** ✅ all matrix rows M-028..M-031, M-042 + INV-001/INV-002 resolved or carried.
- **Contradiction re-scan:** 1 open item by design — B packaging (1.7.0 stable vs telemetry) → `needs_human_decision`. No NEW contradictions introduced.
- **No-discard check:** ✅ neither design discarded.

## Summary
- Planned: 6 + 2 preconditions. Applied: 8. Failed: 0. Skipped: 0.
- Unresolved (by design): 1 — B packaging sub-decision.
