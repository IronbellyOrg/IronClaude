# Base Selection Report

## Quantitative Scoring (50% weight)
RC uses section-topic matching (the seed brief has no requirement IDs): 15 topics from its Constraints and Success Criteria. SR counts concrete tokens in prose outside mockups (numbers, named frameworks and widgets, NO_COLOR, ASCII/ANSI, Orca) against the vague-word list from scoring-protocol.md.

| Metric | Weight | V1 (opus:frontend) | V2 (sonnet:architect) |
|--------|--------|-------------------|-------------------|
| requirement_coverage | 0.30 | 1.000 (15/15 topics) | 1.000 (15/15 topics) |
| internal_consistency | 0.25 | 0.975 (1 contradiction / ~40 claims: A "2 workers waiting" on schema choice vs E, where only billing-migration waits on it) | 1.000 (0 found) |
| specificity_ratio | 0.15 | 0.969 (31 concrete / 1 vague "may") | 0.951 (39 concrete / 2 vague "may") |
| dependency_completeness | 0.15 | 1.000 (screen A-E refs all defined; REPORT ref external, excluded) | 1.000 (A-E and AskRail/FleetTable/DetailPane defined) |
| section_coverage | 0.15 | 1.000 (6/6 H2) | 1.000 (6/6 H2) |
| **quant_score** | | **0.989** | **0.993** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric
CEV shorthand: each cell is VERDICT: evidence. "Searched 1-6" means all six sections were searched with no evidence found.

### Completeness (5 criteria)
| Criterion | V1 | V2 |
|-----------|----|----|
| Covers all explicit requirements | NOT MET: Screen D gives only "Wide" and "Narrow", no default mode; brief asks for wide/default/narrow | MET: every screen has "Wide / Default / Narrow", focus, filter, updates lines |
| Edge cases/failures | MET: "`?` unknown (never shown as 0), `~` stale, `capped`" | MET: "impact unknown ?", "no sig?", ghost marker |
| Dependencies/prerequisites | MET: Risks: live API, durable store, enumeration unverified | MET: Risks: same three plus ask-to-worker mapping |
| Success/completion criteria | NOT MET: searched 1-6, no acceptance conditions | NOT MET: searched 1-6, no acceptance conditions |
| Out-of-scope stated | MET: "the dashboard only observes", "nothing was benchmarked" | MET: "none of their domain logic", "imply no working integration" |
| **Subtotal** | **3/5** | **4/5** |

### Correctness (5 criteria)
| Criterion | V1 | V2 |
|-----------|----|----|
| No factual errors/hallucinated claims | NOT MET: "step 4 of ?" step progress is not among the Orca observations named in the brief (attention, liveness, scope, paging) | MET: synthetic impact caveated in Risks ("may not be derivable") |
| Feasible approaches | MET: documented widgets only, "nothing was benchmarked" | MET: DataTable, Sparkline, Table/Chart/Gauge, join; "not any performance comparison" |
| Consistent terminology | MET: "requests", "reported complete" used throughout | MET: "asks", "reported done/self-reported" used throughout |
| No internal contradictions | NOT MET: A "2 workers waiting" vs E one waiter on schema choice | MET: blocker counts match across B, D, E (DB lock 2, CI 1) |
| Claims supported by rationale | MET: Sec 4 default rationale and per-screen suitability | MET: Sec 4 rationale; Sec 5 widget mapping |
| **Subtotal** | **3/5** | **5/5** |

### Structure (5 criteria)
| Criterion | V1 | V2 |
|-----------|----|----|
| Logical ordering | MET: thesis, conventions, screens, default, framework, risks | MET: same order |
| Consistent hierarchy | MET: H2 sections, H3 per screen | MET: same |
| Separation of concerns | MET: conventions separate from screens | MET: same |
| Navigation aids | MET: Sec 4-5 cross-reference screens A-E by letter | MET: Sec 4-5 cross-reference A-E |
| Artifact conventions | MET: mockup plus color/width/focus/update notes per screen | MET: same |
| **Subtotal** | **5/5** | **5/5** |

### Clarity (5 criteria)
| Criterion | V1 | V2 |
|-----------|----|----|
| Unambiguous language | MET: only hedge is the risk line "may be incomplete" | MET: hedges only in Risks |
| Concrete | MET: thresholds "over 30m", "under 80", "about 60 columns" | MET: "rail 34 cols", "<80", "up to 4" |
| Section purpose clear | MET: each section summarizable in one line | MET: same |
| Terms defined on first use | NOT MET: gh-dash, btop, otel-tui, NO_COLOR undefined | NOT MET: gh-dash, otel-tui, btop undefined |
| Decision points identified | MET: "Revisit if C or D wins the visual vote"; thresholds await calibration | MET: "Provisional, not user approval"; ASCII mode must be tested |
| **Subtotal** | **4/5** | **4/5** |

### Risk Coverage (5 criteria)
| Criterion | V1 | V2 |
|-----------|----|----|
| 3+ risks with probability and impact | NOT MET: 5 risks, no probability | NOT MET: 5 risks, no probability |
| Mitigation per risk | NOT MET: refresh-rate risk has none | NOT MET: ask-to-worker mapping risk has none |
| Failure modes/recovery | MET: unknown/stale/capped display fallbacks | MET: "impact unknown ?", "PARTIAL ?" fallbacks |
| External dependency failure | MET: live observation API unvalidated | MET: live observation interface untested |
| Monitoring/validation mechanism | MET: "updated Ns ago" and stale markers | MET: COVERAGE tile, "live 4s" |
| **Subtotal** | **3/5** | **3/5** |

### Invariant & Edge Case Coverage (5 criteria)
| Criterion | V1 | V2 |
|-----------|----|----|
| Collection boundaries (empty, single, max) | NOT MET: worker lists use "... 13 more", but no empty state and no request overflow (A-002 REJECTED by both) | NOT MET: "...14 more active", same gaps |
| State interactions across components | MET: E "cursor follows identity" across columns | MET: D ghost marker; C "re-sorts only on Esc" |
| Guard condition gaps identified | MET: "`?` unknown (never shown as 0)" | MET: impact derivability gap and "impact unknown ?" |
| Count divergence | MET: "overlap and are never summed" | MET: "overlap, not a sum"; "States are exclusive" |
| Feature interaction effects | MET: pause plus updates, "resume applies them in one redraw" | MET: pause plus queue, "resume applies the queue" |
| **Subtotal** | **4/5** | **4/5** |

Edge-case floor (<1/5 ineligible): V1 4/5, V2 4/5. Both eligible.

### Qualitative Summary
| Dimension | V1 | V2 |
|-----------|----|----|
| Completeness | 3/5 | 4/5 |
| Correctness | 3/5 | 5/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 3/5 |
| Invariant & Edge Case | 4/5 | 4/5 |
| **qual_score** | **22/30 = 0.733** | **25/30 = 0.833** |

## Position-Bias Mitigation
Pass 1 evaluated V1 then V2; pass 2 evaluated V2 then V1. Rows below are the disagreements only; all other 58 verdicts matched.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Covers all explicit requirements | V1 | NOT MET | MET (D "Wide: the column stays about 60 columns" read as the default) | DISAGREE | NOT MET: the brief asks for each mode and V1's other screens label Default |
| Collection boundaries | V1 | NOT MET | MET ("... 13 more") | DISAGREE | NOT MET: no empty state, no request overflow |
| Collection boundaries | V2 | NOT MET | MET ("...14 more active") | DISAGREE | NOT MET: same gaps; applied symmetrically |

Disagreements re-evaluated: 3
Final verdicts changed: 0

## Combined Scoring
| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (opus:frontend) | 0.495 | 0.367 | **0.861** | not needed |
| V2 (sonnet:architect) | 0.496 | 0.417 | **0.913** | not needed |

**Margin**: 5.2 points (above the 5% threshold)
**Tiebreaker applied**: No

## Selected Base: Variant 2 (sonnet:architect)

### Selection Rationale
V2 wins on correctness (5/5 vs 3/5) and completeness (4/5 vs 3/5): it states no unobserved data as fact (V1's step progress and unguarded impact), has no internal count contradiction, and specifies wide/default/narrow for every screen. The debate agrees with this on C-002 (V1 conceded). Debate non-convergence (62.5%) is handled by this score-based selection, per the no-convergence rule.

### Strengths to Preserve from Base
1. Missing-data guard: "impact unknown ?", "self-reported, not verified", "PARTIAL ?" (C-002, agreed).
2. Selection mechanics under transitions: Esc-only re-sort, ghost marker, unread rule (C-003, leaning V2).
3. Request Inspector (C) and Board by State (D) as distinct compositions (S-001, agreed).
4. Default A component split over one read model, fleet as named rows (S-002, unresolved; base kept).

### Strengths to Incorporate from Non-Base Variants
1. V1 Sec 2: glyph-plus-color urgency (`!!` over 30m, `!` over 15m), thresholds flagged as placeholders (C-001, agreed, 95%).
2. V1 Screen C Wait Timeline (U-001) and Screen D Focus Column (U-002) to replace V2 E and V2 B (S-001, agreed merge).
3. V1 Screen A inline thread lines in the selected-request preview (conceded by V2 advocate).
4. V1 `capped` marker for the 100-message limit (V1 Sec 2).
5. Debate outcomes for both shared assumptions: identity fallback (A-001 QUALIFY) and "+N more" request overflow (A-002 REJECT).
