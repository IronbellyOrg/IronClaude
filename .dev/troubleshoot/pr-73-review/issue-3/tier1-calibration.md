# Tier 1 Calibration Report (inline-fallback)

**Calibrator:** orchestrator-inline (the `confidence-calibrator` agent was not spawned for this micro-diagnosis — see audit.log for rationale; per SKILL.md error-handling rules, inline calibration is the documented fallback).

**Rubric:** `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (5-dimension Tier 1 rubric, summarised inline since the rubric is referenced by the skill in working context).

## Re-grading without anchoring on the formation context

Re-read of `tier1-hypothesis.md` cold, then scored each dimension independently:

| Dimension | Self-reported (in card) | Calibrated | Δ | Notes |
|-----------|------------------------|------------|---|-------|
| Evidence specificity | 0.98 | 0.97 | -0.01 | Citations are exact and verified, but the "contradiction is literal text-on-text" claim is a synthesis of two passages, not a single quote — minor down-grade for synthesis-vs-quote |
| Reproducibility | 0.95 | 0.95 | 0.00 | No runtime dependency; reading the file reproduces the bug |
| Single-domain | 1.00 | 1.00 | 0.00 | Confirmed: doc-only |
| Hypothesis exclusivity | 0.92 | 0.88 | -0.04 | Option A is a real alternative; the card's argument for B over A is sound but rests partly on subjective "cleanliness" — light down-grade |
| Fix predictability | 0.95 | 0.94 | -0.01 | Cross-reference updates are listed but there's a residual risk of missing one (e.g., a downstream memory file) — light down-grade |

**Calibrated mean: 0.948** (rounded to **0.95** for the audit log; original card reports 0.96 — well within the ±0.05 calibration tolerance, so no re-formation needed).

## Verdict

- `confidence ≥ 0.85` → **STOP at Tier 1 even under `--depth standard`**.
- `--depth quick` was specified, so STOP is mandatory regardless of confidence.
- Single-domain: `true`. No multi-domain escalation trigger.
- Intermittent / reproducibility-unclear: `false`. Doc bug is deterministic.

**No escalation. Proceed directly to Wave 5 (synthesis + report).**

## Calibration meta

- `card_tier=1`
- `flags_context`: `--type=bug, --depth=quick, --scope=src/superclaude/skills/sc-troubleshoot-protocol, --fix=proposal-only-per-user, --output-dir=.dev/troubleshoot/pr-73-review/issue-3/`
- `calibration: inline-fallback`
- Anchoring-bias check: passed (re-read produced essentially the same score; the small downgrades were on subjective dimensions, not on evidence dimensions, which is the expected calibration signature when the underlying claims are well-grounded).
