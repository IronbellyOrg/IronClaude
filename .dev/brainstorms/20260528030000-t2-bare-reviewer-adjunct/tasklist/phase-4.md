---
phase_id: 4
title: Docs + tests + telemetry
depends_on: [1.5, 2, 3]
blocks: [5]
estimated_loc: 250 new
compliance_tier: STANDARD
acceptance_gates: [AC-4.1, AC-4.2, AC-4.3, AC-4.4]
---

# Phase 4 — Docs + tests + telemetry

## Scope

Publishable documentation, full failure-mode test matrix execution, baseline telemetry collection, end-to-end demo reproduction.

## Tasks

### T-4.1 — `docs/t2-proxy-setup.md`
- Reference LiteLLM router setup (most common proxy)
- Alternative: OpenRouter, custom proxy
- Per-vendor quirks documented (DeepSeek system-message handling, Qwen max_tokens defaults, etc.)
- Secret rotation guidance
- LOC: ~80

### T-4.2 — Failure-mode test matrix
- Each row of §8 failure-modes table (now 12 rows including v1.3 IMM-6) verified by a test fixture
- Each row of §16.6 (c7 failure modes) verified
- Each row of §18.9 risks (R-V12-1..5) addressed by test or accepted-risk doc
- LOC: ~100

### T-4.3 — End-to-end demo reproduction
- §13.1 demo (lifecycle on Go file)
- §13.2 demo (spec review, 7.8 case generalized)
- §13.3 demo (auth-broken failure mode)
- §16.7 demo (c7-enabled lifecycle)
- All produce expected output trees + return contracts
- LOC: ~30

### T-4.4 — Telemetry baseline
- Cost telemetry over 1-week window (typical workflow cost per call)
- Separately for `--c7` on/off
- Per-caller cost breakdown
- Validator verdict distribution (Validated / Corroborated / Demoted / Dropped / Contradicted ratios)
- LOC: ~40 (mostly instrumentation, not new logic)

## Acceptance Gate

- **AC-4.1** Setup guide published with verified example shell config
- **AC-4.2** Reference proxy compatibility list (≥3 vendors tested)
- **AC-4.3** Sample run-through doc — end-to-end with output artifacts
- **AC-4.4** Failure-mode test matrix all green (every §8 + §16.6 row reproduced)

## Bonus deliverable

If Phase 1.5 spec gaps (SG-A/B/C) were addressed inline rather than via v1.4 amendment: produce a brief v1.4-CONSOLIDATED.md describing the final canonical contract. Otherwise, file the v1.4 amendment formally.

## Risks

- **Telemetry baseline window too short** — 1 week may not capture rare failure modes; consider 2-week rolling window for V2
- **Per-vendor compatibility drift** — proxy vendors may change schemas; lock test fixtures to specific vendor API versions
