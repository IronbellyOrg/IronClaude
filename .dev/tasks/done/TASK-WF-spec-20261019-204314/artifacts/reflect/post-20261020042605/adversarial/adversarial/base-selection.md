# Base Selection Report

Inputs: variant-1 (R1 analyzer, input C=0.71), variant-2 (R2 QA, C=0.78), variant-3 (R3 refactorer, C=0.80). Input calibrations are reused as-is (mean 0.763, method: arithmetic mean of the three independently blind-calibrated `confidence_calibrated` values); no new calibration was fabricated here.

## Quantitative Scoring (50% weight)

Requirement universe for RC: the seven debated points D1..D7 (menu-0 whole-selection, permission predicate, HOME-ancestor, list-flag drift, Linux-only authority, doc disclosure, verification/fixture gaps). Cards are task-partitioned, so AC-level RC across the whole spec would penalize assignment rather than quality.

| Metric | Weight | V1 (R1) | V2 (R2) | V3 (R3) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.71 (D1,D2,D3,D5,D7 = 5/7) | 0.71 (D1,D2,D3,D5,D7 = 5/7) | 1.00 (D1..D7 = 7/7) |
| internal_consistency | 0.25 | 0.92 (2 tensions / ~25 claims: "new feature cannot regress" vs "regression candidate"; "receipt necessary" vs "conditional drift") | 0.95 (1 / ~22: Necessary label vs own "operator authority may affect label") | 0.96 (1 / ~24: source.md:90 cited as macOS-exclusion support while :90 lists macOS) |
| specificity_ratio | 0.15 | 0.85 (dense file:line cites; several "[brief-only]"/"not read" hedges) | 0.88 | 0.90 |
| dependency_completeness | 0.15 | 0.80 (brief-hunk refs unresolved to current lines) | 0.90 (errata resolved: 907-910 → 49-53) | 0.85 (Task4 numeric anchors imprecise; :90 misanchor) |
| section_coverage | 0.15 | 1.00 (7 H2) | 0.71 (5 H2) | 1.00 (7 H2) |
| **quant_score** | | **0.841** | **0.824** | **0.953** |

Computation: V1 = 0.213+0.230+0.128+0.120+0.150 = 0.841; V2 = 0.213+0.238+0.132+0.135+0.107 = 0.824; V3 = 0.300+0.240+0.135+0.128+0.150 = 0.953.

## Qualitative Scoring (50% weight) — Additive Binary Rubric (CEV)

### Completeness (5)
| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Covers assigned explicit requirements | MET | T2/T4/T5 per-AC anchors (card §Assigned completion) | MET | T1/T3/T6 anchored by region | MET | T7 all 7 ACs anchored (guide/reference lines) |
| Edge cases / failure scenarios | MET | 0775, HOME-symlink, restore-failure paths | MET | partial-install cleanup, ambiguous discovery | MET | retry-without-receipt, root-owned alias |
| Dependencies / prerequisites | MET | ccsession mkdir → native ordering | MET | curl/Bash acquisition-only | MET | main.py:224→255 ordering |
| Success/completion criteria defined | NOT MET | next steps directional, no pass criteria (calibrator note) | NOT MET | "recommended next cases lack precise success criteria" (calibrator) | NOT MET | recommendations name cases, not pass criteria |
| Out of scope stated | MET | "No fixes or live execution were authorized/performed" | MET | "Live … remains pending separate authorization" | MET | "No code fix, test execution or live operation occurred" |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Correctness (5)
| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| No factual errors | NOT MET | "regression candidate" withdrawn in debate; umask-002 recollection flagged unverified by the card itself | MET | source/test cites spot-checked by calibrator; label dispute is classification, not fact | NOT MET | source.md:90 misanchored (conceded R1) |
| Feasible under constraints | MET | | MET | | MET | |
| Terminology consistent | NOT MET | "candidate"/"qualified"/"conditional" blur the four classes (calibrator 0.65) | NOT MET | Necessary vs Authorized mislabel (conceded R1) | MET | four classes + separated advisories used consistently |
| No internal contradictions | NOT MET | IC tensions above | MET | | MET | |
| Claims evidence-supported | MET | | MET | | MET | |
| **Subtotal** | **2/5** | | **4/5** | | **4/5** | |

### Structure (5)
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Logical ordering | MET | MET | MET |
| Consistent hierarchy | MET | MET | MET |
| Separation of concerns | MET (D1/D2/D3 sections) | MET (dispositions vs advisory vs limits) | MET (coverage / D1-3 / new deviation / ordering) |
| Navigation aids | NOT MET | NOT MET | NOT MET |
| Artifact-type conventions | MET | MET | MET |
| **Subtotal** | **4/5** | **4/5** | **4/5** |

### Clarity (5)
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Unambiguous language | NOT MET ("candidate", "may", "debate-open") | MET | MET |
| Concrete over abstract | MET | MET | MET |
| Section purpose clear | MET | MET | MET |
| Terms defined on first use | NOT MET | NOT MET | NOT MET |
| Actionable next steps | NOT MET (calibrator 0.55) | NOT MET (calibrator 0.60) | MET (three named isolated cases + guide edits; calibrator 0.70) |
| **Subtotal** | **2/5** | **3/5** | **4/5** |

### Risk Coverage (5)
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| ≥3 risks with probability+impact | NOT MET (no probabilities) | NOT MET | NOT MET |
| Mitigation per risk | MET (isolated cases named) | MET | MET |
| Failure modes / recovery | MET (restore-failure, retry) | MET (partial removal) | MET (first attempt/retry/removal) |
| External dependency failures | MET (upstream modes unknown) | MET | MET |
| Monitoring / validation mechanism | NOT MET | NOT MET | MET (live smoke gate procedure + block, guide:309-321) |
| **Subtotal** | **3/5** | **3/5** | **4/5** |

### Invariant & Edge Case Coverage (5)
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Collection boundaries | NOT MET | NOT MET | NOT MET |
| State interactions across components | MET (retry w/o receipt; ccsession→native) | MET (reuse vs proof predicates) | MET (mkdir precedes native, inherits umask) |
| Guard-condition gaps | MET (predicate mismatch) | MET | MET |
| Count divergence | NOT MET | NOT MET | NOT MET |
| Interaction effects | MET | MET | MET |
| **Subtotal** | **3/5** | **3/5** | **3/5** |

### Qualitative Summary
| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4/5 | 4/5 | 4/5 |
| Correctness | 2/5 | 4/5 | 4/5 |
| Structure | 4/5 | 4/5 | 4/5 |
| Clarity | 2/5 | 3/5 | 4/5 |
| Risk Coverage | 3/5 | 3/5 | 4/5 |
| Invariant & Edge Case | 3/5 | 3/5 | 3/5 |
| **qual_score** | **18/30 = 0.600** | **21/30 = 0.700** | **23/30 = 0.767** |

### Edge Case Floor Check
All three score 3/5 ≥ 1/5 → all eligible. Floor not suspended.

## Position-Bias Mitigation
Pass 1 (V1→V2→V3) and Pass 2 (V3→V2→V1) were evaluated by the coordinator against the same CEV table.
| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Correctness-1 (no factual errors) | V2 | MET | NOT MET | DISAGREE | MET — re-eval: Necessary/Authorized is a classification call the card itself flags as open, not a factual error |
| Clarity-5 (actionable next steps) | V3 | MET | MET | agree | MET |
| Risk-5 (monitoring) | V3 | MET | NOT MET | DISAGREE | MET — re-eval: card cites a concrete gate procedure + block condition (guide:309-321, t7-live-smoke-gate.md) |
Disagreements re-evaluated: 2. Final verdicts changed from Pass 1: 0.

## Combined Scoring
| Variant | Quant (×0.50) | Qual (×0.50) | **Final** | Debate points won (R2) |
|---|---|---|---|---|
| V1 (R1 analyzer) | 0.421 | 0.300 | **0.720** | 3 (C-003, C-004, X-003) |
| V2 (R2 QA) | 0.412 | 0.350 | **0.762** | 4 (S-002 structure, C-002, C-005, X-002) |
| V3 (R3 refactorer) | 0.477 | 0.383 | **0.860** | 3 (C-001, X-001, A-002) |

**Margin** (V3 − V2): 0.098 = 9.8% (above 5% threshold). **Tiebreaker applied**: No.

## Selected Base: Variant 3 (R3 refactorer / opus)

### Selection Rationale
V3 is the only card covering all seven debated points (RC = 1.0), including the only newly surfaced canonical-deviation candidate (D4) and the documentation-disclosure audit (D6). It uses the four-class taxonomy consistently and gives the most actionable verifier list. Its one factual error (source.md:90 misanchor) was conceded in Round 1 and is corrected by the plan. Note: debate point S-002 resolved that V2's *structural discipline* (strict four classes, advisories separated, errata section) is the better frame; this is applied to the V3 base as Change #1 rather than overriding the score.

### Strengths to Preserve from Base
1. D1 as Necessary deviation with the :78/:80/:144 chain and the "skip is not reject" argument.
2. D4 finding with `main.py:326-330` vs source.md:76/:117 and guide:50 disclosure-is-not-authorization.
3. D6 disclosure audit (guide:46/73/25/223).
4. Ordering section (`install_mcp.py:1299-1334`; `main.py:254-275`; `main.py:94-187,326-332`) and the live-smoke limits list.

### Strengths to Incorporate from Non-Base Variants
1. From V2: four-class structure with a separate "Advisory / no-spec" section and an explicit "Errata and evidence limits" section; the canned-`mcp_cli`-fixture caveat (`test_install_codebase_memory.py:821-835`); T1/T3/T6 AC anchors; historical-vs-fresh separation (`t6-cli-regressions.txt:49-53`).
2. From V1: the split-slice framing of D1 (explicit-mixed refuted by `:964-988`; menu-0 slice untested beyond `:944-952`); D2 chain with the caller return (`install_mcp.py:846-848`) and retry (`:597-605`); the missing-offending-path note (`install_mcp.py:577-579`); the add-json argv secret-exposure advisory; T2/T4/T5 anchors and the explicitly-unread-region discipline.
3. From the debate: Authorized (not Necessary) label for Linux-only anchored on operator-direction.md:5-7 (V1's label, conceded by V2 and V3).
