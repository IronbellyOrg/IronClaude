# Calibration Report

**Card under calibration**: tier1-hypothesis.md (this directory)
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-04T15:37:28Z
**Provenance**: confidence-calibrator agent; persisted by the parent on receipt (justifications condensed, scores and verdict verbatim)

## Per-dimension scores

Frontmatter: `claim_class: runtime_behavior`, `evidence_class: runtime_repro`, `verdict_direction: AFFIRM` (all declared, consistent).

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | Every citation re-read and matches: install_user_setup.py:175-178 (statement at :177), :297, :341-345, :41; user_settings_defaults.json:36; tests/cli/test_install_user_setup.py:139. |
| Runtime check | 1.0 | Cell (runtime_behavior, runtime_repro) = 1.0; parent-captured failing-arm stdout in tier1-observation.md shows the exact state; card discloses install_plugins itself was not run. |
| Symptom coverage | 1.0 | Covers the chain: merge writes true (:175-178) → selected (:297) → installed (:341-345). |
| Reproducibility fit | 1.0 | Deterministic; repro run and matches. |
| Fix directness | 1.0 | Edits the producer statement; two lines plus a constant; reads old key only. |
| Domain coherence | 1.0 | Single-domain logic defect; the card's self-score 0.5 ("rename map is Ponytail-specific") is not a second domain. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 1.00 | |
| gate_M1: evidence_grounding + 0.30 | 1.30 | does not bind |
| gate_M2: runtime_check + 0.30 | 1.30 | does not bind |
| gated_min | 1.00 | |
| verdict_cap | none | M3a not binding (runtime_check 1.0) |
| **calibrated** | 1.00 | no structural cap fired |
| spot_check_unverifiable | none | repro script no longer on disk; captured output is the record |
| structural_flags | none | C1-C7 not fired; C8 skipped |

## Confidence

- **Self-reported (in card)**: 0.92 (not an input)
- **Calibrated (this report)**: 1.00
- **Formula applied**: min(1.00, 1.30, 1.30) = 1.00
- **Delta**: +0.08 (Domain coherence 0.5 → 1.0)

## Escalation recommendation

- **Verdict**: `STOP`
- **Reason**: `none`
- **Rubric rule fired**: Rule 4 default: confidence ≥ 0.85 AND single-domain AND reproducible → STOP at Tier 1 (rules 1-3 checked, none matched).
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | calibrated 1.00 ≥ 0.50; headline has no enum token |
| C2 | no | — | — | tier1-hypothesis.md "No exclusion claimed" |
| C3 | no | — | — | no control arm cited |
| C3b | no | — | — | execution-locus.md SAME-ENV: yes |
| C4 | no | — | — | diagnosability-tasklist.md has no measurement or pending rows |
| C5 | no | — | — | card Timestamp 15:37:04Z ≤ card_mtime 15:37:23Z + 5 min |
| C6 | no | — | — | headline asserts no numeric threshold |
| C7 | no | — | — | no environment property asserted |
| C8 | skipped | — | — | input absent: behaviour_definitions_path |

## Notes

- Sensitivity: with Domain coherence 0.5 (the card's value) calibrated = 0.92 and rubric rule 3 (domain coherence ≤ 0.5 → ESCALATE multi_domain) would fire. The orchestrator accepts the calibrator's reading: the cause sits in one function; tests and docs are the fix footprint, not a second domain.
- Falsification test not yet run; the caller (sc:pr-submit) runs it after applying the fix.
- Out-of-scope risk carried to the report: a workspace that already ran the unmerged branch keeps a saved `ponytail@ironclaude: true`.
