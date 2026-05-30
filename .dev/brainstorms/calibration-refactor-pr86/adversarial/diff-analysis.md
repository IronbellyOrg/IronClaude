# Diff Analysis: Calibration Refactor Variants

## Metadata
- Generated: 2026-05-26T20:45:00Z
- Variants compared: 3 (V1 opus:analyzer, V2 sonnet:architect, V3 haiku:qa)
- Total differences found: 14
- Categories: structural (3), content (5), contradictions (2), unique (3), shared assumptions (1)

## Structural Differences

| # | Area | V1 (analyzer) | V2 (architect) | V3 (qa) | Severity |
|---|------|---------------|----------------|---------|----------|
| S-001 | Section count | 3 file changes | 3 file changes (schema-level rewrites) | 6 changes (3 same as V1 + SKILL.md + new eval-cases file + pytest hookup) | Medium |
| S-002 | Card schema framing | additive (claim_class added, no version bump) | versioned (Schema v2.0, mandatory verdict_direction field, evidence-kind table) | additive (identical to V1) | High |
| S-003 | Calibrator instruction structure | extends existing Responsibilities | rewrites Responsibilities with explicit input-filter pre-step (M3c) and Stage 1/2 trace | extends existing Responsibilities (identical to V1) | Medium |

## Content Differences

| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity |
|---|-------|-------------|-------------|-------------|----------|
| C-001 | M1 fix formula | gated-min: `min(mean, evidence_grounding + 0.30, runtime_check + 0.30 if runtime_behavior)` | two-stage: raw_mean → gated_min (both M1+M2 gates always apply, no claim_class exemption) → verdict cap | adopts V1's formula by reference | Medium |
| C-002 | M2 fix shape | 6th dimension "Runtime check" added; Evidence grounding OR-clause tightened to snippet-match | "Source citation" + "Runtime verification" replace old "Evidence grounding" (schema rename); typed evidence-kind table in card | adopts V1's shape | High |
| C-003 | M3a verdict-direction cap | table form: REFUTE+runtime ≤ 0.70, AFFIRM+runtime ≤ 0.84 | same caps, but mandatory `verdict_direction` frontmatter field (calibrator rejects malformed cards) | adopts V1's table | Low |
| C-004 | M3c (anchoring) handling | rejected — too expensive; defer | input filter masking the self-reported confidence field; orchestrator-side byte-stripping flagged as follow-up | property test P5 (anchoring variance bound) — soft assertion in pin tests | High |
| C-005 | confidence-check/SKILL.md scope | explicitly excluded from minimal-change subset | not directly addressed | 5-line scope-annotation correction (Change 4) | Medium |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|-------------------|-------------|-------------|-------------|--------|
| X-001 | Should claim_class default be `runtime_behavior` (fail-safe) or reject malformed cards? | default to runtime_behavior | reject as `status: malformed` (mandatory frontmatter) | default to runtime_behavior (adopts V1) | Medium — affects migration cost |
| X-002 | Is touching confidence-check/SKILL.md required for M2 closure? | NO — wrong layer, leave it | not addressed | YES — kills the cultural-prior recursion (~5 lines) | Low — cheap edit, low risk either way |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V2 | Typed evidence-item table in card (`source_citation` | `executed_reproducer` | `test_assertion` | `documentation` | `log_artifact`) — makes the kind explicit at data layer instead of inferred by calibrator | High |
| U-002 | V2 | Mandatory `verdict_direction` frontmatter field + calibrator rejection of malformed cards | Medium |
| U-003 | V3 | Full pin-test corpus (`calibrator-eval-cases.md`) with 6 fixtures + 5 property tests + PR-check hookup | **High** — directly closes M4 |

## Shared Assumptions

| # | Assumption | Source Agreement | Impact | Status |
|---|------------|------------------|--------|--------|
| A-001 | "Tier 1 calibrator's `tools: Read` constraint stays" — none of V1/V2/V3 propose giving the calibrator Bash | All three variants | High — preserves the structural blindness that motivated the rubric/card/calibrator triple-fix path | UNSTATED → promoted to debate point. Validity: high — granting Bash is RCE-equivalent risk. The dimension-level scoring is the right anchor. |

## Summary

- Total structural differences: 3 (1 High, 1 Medium, 1 Medium)
- Total content differences: 5 (1 High, 2 Medium, 1 Low, 1 Medium)
- Total contradictions: 2 (1 Medium, 1 Low)
- Total unique contributions: 3 (2 High, 1 Medium)
- Total shared assumptions: 1 UNSTATED, promoted
- Highest-severity items: S-002 (schema versioning), C-002 (M2 fix shape), C-004 (M3c handling), U-001 (typed evidence table), U-003 (pin-test corpus)
