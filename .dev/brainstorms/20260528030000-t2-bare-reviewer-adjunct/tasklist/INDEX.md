---
tasklist_id: TL-T2-BARE-REVIEWER
spec_source: /config/workspace/IronClaude/.dev/brainstorms/20260528030000-t2-bare-reviewer-adjunct/merged-requirements.md
spec_version: 1.3.0-draft
generated: 2026-05-28T05:50Z
status: ready-for-execution
phases: 6
sprint_cli_compatible: true
---

# Tasklist — T2 Bare-Reviewer Adjunct

## Overview

This tasklist converts the v1.3.0-draft spec into a Sprint-CLI-compatible execution sequence. IMM-1..IMM-6 blockers are resolved at the spec layer; tasks below assume v1.3 spec semantics.

## Dependency Graph

```
phase-1 (sc-bare-review v1.0 core)
  ├─→ phase-1.5 (c7-enrichment skill)
  └─→ phase-2 (/sc:adversarial --suspect-source extension)
        ↑
        └─ phase-1.5 ─┐
                      ↓
                   phase-3 (caller plumbing — 5 callers)
                      ↓
                   phase-4 (docs + tests + telemetry)
                      ↓
                   phase-5 (optional MCP transport — DEFERRED)

parallel-stream-A: ab-test-harness preparation (no dependency on Phase 1; can run anytime)
```

## Phase Summary

| Phase | Title | Depends on | Est. effort (LOC) | Compliance tier |
|-------|-------|------------|-------------------|------------------|
| 1 | sc-bare-review v1.0 core | — | ~450 new | STANDARD |
| 1.5 | c7-enrichment skill + integration | 1 | ~430 new + ~50 modified | STANDARD |
| 2 | /sc:adversarial --suspect-source | 1 | ~500 new + ~200 modified | STRICT |
| 3 | Caller plumbing × 5 | 1.5, 2 | ~200 modified | STANDARD |
| 4 | Docs + tests + telemetry | 1.5, 2, 3 | ~250 new | STANDARD |
| 5 | MCP transport adapter (optional) | 1 | ~250 new | STANDARD — DEFERRED |

**Total estimated:** ~1830 LOC new + ~450 modified (vs spec estimate of ~1450 new + ~300 modified — slight overshoot expected for spec-gap addressing in Phase 1.5).

## Spec Gaps to Address (folded into Phase 1.5 work)

Per `reflect-validation-2026-05-28.md` — three gaps surfaced during c7-enrichment SKILL.md drafting:

1. **Gap-A:** §18.3 `--libs` flag semantics (skips vs augments auto-detect) — Phase 1.5 task SG-A
2. **Gap-B:** `failure_stage` field missing from §18.5 return contract — Phase 1.5 task SG-B
3. **Gap-C:** AC-1.32 metrics ownership unclear (skill/caller/shim) — Phase 1.5 task SG-C

These can be addressed inline during Phase 1.5 OR rolled into a v1.4 spec amendment first. Recommended: address inline; document decisions in commit messages.

## Parallel Stream

The A/B test harness (`ab-test-harness-spec.md`) is independent of implementation phases. Population selection, fixture preparation, and measurement-protocol scripting can begin immediately and run in parallel with Phase 1-2. Test execution itself requires Phase 1+1.5+2 complete to compare arms.

## Compliance Tier Routing

| Tier | Phases | Why |
|------|--------|-----|
| STANDARD | 1, 1.5, 3, 4, 5 | Single-skill scope; modest cross-cutting; well-bounded |
| STRICT | 2 | Multi-file changes to existing /sc:adversarial protocol; validator-semantic alteration; cross-skill contract changes |

## Acceptance Gate Per Phase

Each phase MUST clear its phase ACs before downstream phases begin. See per-phase task files.

| Phase | Gate ACs | Test fixture required |
|-------|----------|----------------------|
| 1 | AC-1.1..AC-1.12 + AC-1.5 (v1.3 IMM-3 rewording) + Wave-B empty-target guard | Single-target bare-review fixture |
| 1.5 | AC-1.24..AC-1.32 + Spec-Gaps SG-A/B/C | Caller-agnostic c7 fixture (sc-bare-review + 1 non-bare-review caller) |
| 2 | AC-2.1..AC-2.13 + IMM-1 (corroboration) + IMM-2 (semantic-match) | 3-variant adversarial fixture with suspect tagging |
| 3 | AC-3.1..AC-3.7 (per-caller) | Per-caller integration fixture |
| 4 | AC-4.1..AC-4.4 + failure-mode matrix from §8 (now 12 rows including v1.3 IMM-6) | Docs review + test pass |
| 5 | AC-5.1..AC-5.2 (optional) | MCP adapter integration test |

## Out of Scope for This Tasklist

- T2 proxy infrastructure standup (operational; tracked separately)
- Per-caller default-value decisions (driven by A/B test results, not spec)
- v1.4 spec amendment addressing gaps SG-A/B/C if user prefers spec-first over inline-fix

## Files in This Bundle

| File | Purpose |
|------|---------|
| `INDEX.md` | This file |
| `phase-1.md` | sc-bare-review v1.0 core implementation |
| `phase-1.5.md` | c7-enrichment skill + integration + spec-gap fixes |
| `phase-2.md` | /sc:adversarial --suspect-source extension |
| `phase-3.md` | Caller plumbing (5 commands) |
| `phase-4.md` | Docs + tests + telemetry |
| `phase-5.md` | MCP transport adapter (optional/deferred) |
