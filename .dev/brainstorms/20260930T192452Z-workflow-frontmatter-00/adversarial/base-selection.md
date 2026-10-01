# Base Selection

## Quantitative Scoring (50% weight)

Deterministic parts computed by `adversarial/_quant.py` (concrete = `path.md:N` citations + backtick spans + integers; vague = the SKILL's vague-indicator list; H2 counted outside code fences).

| Metric | Weight | V1 | V2 | Computation |
|--------|--------|----|----|-------------|
| RC requirement coverage | 0.30 | 1.00 | 1.00 | 8 source items (4 Success Criteria + 4 Open Questions in seed-brief.md) — each answered in both `## Decision` + `## File edits` + `## Gate changes` |
| IC internal consistency | 0.25 | 1.00 | 1.00 | 0 intra-variant contradictions found (V2's ≥1-Phase rule conflicts with template 00:10 — external, scored under Correctness) |
| SR specificity | 0.15 | 1.00 | 1.00 | V1 concrete 334 / vague 0; V2 concrete 290 / vague 0 |
| DC dependency completeness | 0.15 | 1.00 | 1.00 | internal refs ("see Gate changes", "edit 1 and 2", "Decision 4", "see below") all resolve |
| SC section coverage | 0.15 | 1.00 | 1.00 | 8 H2 each / max 8 |
| **quant_score** | | **1.000** | **1.000** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Single orchestrator evaluation (see Position-Bias note). MET requires a cited location.

| Dim | # | Criterion | V1 | V1 evidence | V2 | V2 evidence |
|-----|---|-----------|----|-------------|----|-------------|
| Completeness | 1 | all explicit requirements | MET | Decision 1-4 (V1:12-20) | MET | Decision 1-4 (V2:10-26) |
| | 2 | edge cases / failures | MET | Risks 1,4 (V1:210,213) | MET | Risk 2 numbered steps (V2:202) |
| | 3 | dependencies / prereqs | MET | plugin mirror, sync-dev (V1:146-148,179) | MET | V2:144-147 |
| | 4 | success criteria | MET | Gate changes (V1:191-197) | MET | V2:171-184 |
| | 5 | out of scope | MET | V1:216-224 | MET | V2:214-221 |
| Correctness | 1 | no factual errors | MET | cites verified (SKILL.md:40-44, quality-gates.md:3-30) | MET | same |
| | 2 | feasible under constraints | MET | honors `00:10` (≥1 Task only) | NOT MET | ≥1 Phase at schema-min contradicts `00:10` (V2:95) |
| | 3 | terminology consistent | MET | | MET | |
| | 4 | no internal contradictions | MET | IC=1.0 | MET | IC=1.0 |
| | 5 | claims supported | MET | path:line throughout | MET | path:line throughout |
| Structure | 1-5 | ordering, hierarchy, separation, cross-refs, conventions | 5 MET | 8 required sections in order | 5 MET | same |
| Clarity | 1 | unambiguous | NOT MET | "that phase's task AC bullets" — which task? (V1:48) | NOT MET | "`[...]` placeholders removed" (V2:97) |
| | 2 | concrete | MET | exact before/after text | MET | exact before/after text |
| | 3 | clear section purpose | MET | | MET | |
| | 4 | terms defined (AC, QA, MDTM) | NOT MET | undefined | NOT MET | undefined |
| | 5 | actionable next steps | MET | numbered edits 1-4 | MET | per-file edits |
| Risk | 1 | ≥3 risks with probability + impact | NOT MET | no probability ratings | NOT MET | no probability ratings |
| | 2 | mitigation per risk | MET | V1:210-214 | MET | V2:199-212 |
| | 3 | failure modes / recovery | MET | E-GATE + contract `failed` (V1:196) | MET | V2:183-184 |
| | 4 | external dependencies | MET | installed-path risk (V1:211) | MET | V2:207 |
| | 5 | validation mechanism | MET | guard test (V1:150-167) | MET | test + mirror assert (V2:121-142) |
| Invariant | 1 | collection boundaries | MET | ≥1 Task; ≥1 Task per Phase (V1:113,137) | MET | ≥1 Phase, ≥1 Task (V2:95) |
| | 2 | state across boundaries | MET | cross-run `version` state analysed (V1:213) | MET | overwrite semantics (V2:16) |
| | 3 | guard gaps | MET | regexes for version/date (V1:111) | NOT MET | `version` "non-empty" only (V2:94) |
| | 4 | count divergence | MET | contiguous ids, `Depends on` lower K (V1:138) | MET | unique ids, earlier Task (V2:95,113) |
| | 5 | interaction effects | MET | Phase/Task H2 × `/sc:implement` (V1:210) | MET | numbered steps × enumeration (V2:202) |

### Qualitative Summary
| Dimension | V1 | V2 |
|-----------|----|----|
| Completeness | 5 | 5 |
| Correctness | 5 | 4 |
| Structure | 5 | 5 |
| Clarity | 3 | 3 |
| Risk Coverage | 4 | 4 |
| Invariant & Edge Case | 5 | 4 |
| **Total / 30** | **27 (0.900)** | **25 (0.833)** |

### Edge Case Floor Check
V1 5/5 eligible; V2 4/5 eligible.

## Position-Bias Mitigation
Dual independent passes were not executed: at `--depth quick` the orchestrator scored once (input order, V1 then V2). Disagreements found: n/a. Verdicts changed: 0. The base decision below does not rest on the qualitative margin alone (tiebreaker level 1 = debate points).

## Combined Scoring
| Variant | quant × 0.5 | qual × 0.5 | Score |
|---------|-------------|------------|-------|
| V1 opus:architect | 0.500 | 0.450 | **0.950** |
| V2 sonnet:refactorer | 0.500 | 0.417 | 0.917 |

Margin 0.033 < 0.05 → tiebreaker applied, level 1 (debate points won): V1 7 (S-002, C-002, C-003, C-004, C-005, C-007, C-008) vs V2 3 (C-001, C-006, X-001). V1 selected.

## Selected Base: Variant 1 (opus:architect)
- **Rationale:** wins 7 of 10 decided diff points with both advocates agreeing; stricter, template-faithful gate; only variant addressing the `SKILL.md:65` Phase/Task ambiguity.
- **Strengths to preserve:** Wave 2 text (V1:38-51) minus the counter; schema-min/full gate split (V1:109-142); quoted `created_date`; Inputs → task body; Risks 1-3,5.
- **Strengths to incorporate from V2:** constant `version: "1"` (C-001/X-001); plugin-mirror byte-equality assert (C-006); Checkpoint → the phase's last task's `Acceptance criteria:` (C-003 refinement); "never infer priority from tone" (U-004).
- **Debate resolutions to apply:** drop V1's bare "`[`-bracketed placeholder line" clause (C-004); numbered/checkbox ban explicitly applies inside fenced code too (A-001); `created_date` from session date context, STOP `E-GATE` if unavailable, Bash rule unchanged (A-002).
