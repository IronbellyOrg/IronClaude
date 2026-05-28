# Refactor Plan — incorporation-report.md assembly

**Base**: Variant 2 (Quality Engineer).
**Output**: `incorporation-report.md` (the user-facing deliverable) + `merged-output.md` (classifications table).

## Overview

- Base variant: QE (combined score 0.919)
- Incorporated variants: Architect (workload-mismatch framing, REJECT rationale anchoring), Analyzer (frequency-weighted prioritisation, eval-evidence enumeration)
- Change count: 11 (see `merge-log.md`)
- Risk: low (all additive; no architectural conversion required)

## Planned Changes (per-change entries)

See `merge-log.md` for the full per-change log. High-level sequencing:

1. Spine = QE's 5 INCORPORATE + 1 ADAPT roadmap.
2. Executive summary framing from Architect.
3. Ordering principle (frequency-weighted) from Analyzer.
4. Schema-conformance split: audit-log schema (analyzer-driven, eval-evidence) + hypothesis-card/REPORT.md schemas (QE-driven, enforcement).
5. Single ADAPT (single-agent adversarial fallback) unanimous across all three.
6. DEFER list explicit (3 items with defer-until criteria).
7. REJECT list with rationale (14 items, each with workload-mismatch citation).
8. Implementation Gotchas section from Round 2.5 invariant probe (5 MEDIUM items).

## Changes NOT Being Made

- QE's full JSON Schema for output contract — DEFERRED (no observed caller-side parse break).
- QE's stale-codebase detection — DEFERRED (v2 has no resume primitive yet).
- QE's named degradation modes — DEFERRED (per-component error matrix is adequate today).
- Architect's 3-item conservative INCORPORATE list — EXPANDED to 5 (QE's broader scope + Analyzer's audit-log focus).
- Architect's repeat-failure as ADAPT — UPGRADED to INCORPORATE in Round 2 (analyzer's eval-evidence argument convinced architect).
- Analyzer's narrow 4-INCORPORATE list — EXPANDED to 5 (added hypothesis-card/REPORT.md schemas from QE).

## Risk Summary

| Item | Risk | Mitigation |
|---|---|---|
| `test_is_wrong` flag | Low | Additive bool; gotcha INV-001 addressed in detection rule |
| Repeat-failure detection | Low-medium | Gotcha INV-002 (false-positive risk) mitigated by user-overridable notice |
| MCP cap | Low | Gotcha INV-003 (per-server vs per-invocation ambiguity) addressed in change spec |
| Audit-log schema | Low | Schema codifies existing format; normalization is corrective |
| Schema-conformance tests | Low | Test-only; no runtime impact |
| Single-agent adversarial fallback | Low | Additive intermediate step; rare failure path |

## Review Status

Auto-approved (non-interactive Mode B). User can re-invoke `/sc:adversarial` with `--interactive` to gate at the 4 checkpoints.
