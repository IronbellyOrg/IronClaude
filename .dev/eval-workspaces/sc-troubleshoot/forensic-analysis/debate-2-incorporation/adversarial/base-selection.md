# Base Selection — Adversarial Run 2

**Purpose**: Select the base variant whose framing becomes the spine of the merged incorporation report.

## Quantitative Scoring (50% weight)

| Metric | Weight | Architect | QE | Analyzer |
|---|---|---|---|---|
| Requirement coverage | 0.30 | 0.85 (covers all 31 diffs in catalogue) | 0.92 (covers diffs + 3 net-new defense-in-depth items) | 0.85 (covers diffs + concrete failure-mode mapping) |
| Internal consistency | 0.25 | 0.95 | 0.90 (3 ADAPTs deferred under Round 2 pressure) | 0.95 |
| Specificity ratio | 0.15 | 0.85 (concrete `which file changes`, `which wave`) | 0.90 (most file/wave-specific of the three) | 0.85 |
| Dependency completeness | 0.15 | 0.80 (refers to eval-1 evidence loosely) | 0.85 | 0.95 (frequency-weights against the 8 eval logs explicitly) |
| Section coverage | 0.15 | 0.90 | 0.95 | 0.90 |
| **Weighted quant** | — | **0.870** | **0.905** | **0.886** |

## Qualitative Scoring (50% weight, 30 criteria additive binary)

| Dimension | Architect | QE | Analyzer |
|---|---|---|---|
| Completeness (5) | 4/5 (could expand DEFER rationale) | 5/5 | 4/5 (REJECT list dominates; less depth on the 4 INCORPORATEs) |
| Correctness (5) | 5/5 | 4/5 (`refs/output-contract-schema.json` mentions JSON Schema validation step but doesn't spec the validation library) | 5/5 |
| Structure (5) | 5/5 | 5/5 | 5/5 |
| Clarity (5) | 4/5 (some recommendations cite forensic IDs without restating the change in plain prose) | 5/5 | 5/5 |
| Risk coverage (5) | 4/5 | 5/5 (covers 3 ADAPT risk-low explicitly) | 4/5 (assumes "wait for failure modes to fire" — risks under-mitigating asymmetrically-costly modes) |
| Invariant & Edge case coverage (5) | 3/5 | 4/5 | 3/5 |
| **Qual subtotal** | **25/30** | **28/30** | **26/30** |
| **Qual normalised** | **0.833** | **0.933** | **0.867** |

## Edge Case Floor Check

Floor threshold: 1/5 on Invariant & Edge Case Coverage. All three variants score 3/5 or 4/5 — all above the floor. None disqualified.

## Combined Scoring

| Variant | Quant (50%) | Qual (50%) | Combined | Rank |
|---|---|---|---|---|
| Architect | 0.870 | 0.833 | **0.852** | 3 |
| QE | 0.905 | 0.933 | **0.919** | 1 |
| Analyzer | 0.886 | 0.867 | **0.877** | 2 |

## Tiebreaker Protocol

Margin between top two (QE = 0.919 vs Analyzer = 0.877) = 4.2%. Within the 5% tiebreaker range.

- Tiebreaker Level 1 (debate performance): QE's Round 2 concessions (dropping 3 items to DEFER) moved the convergence to 100% unanimous. Analyzer's positions were unchanged but their REJECT list anchored the final shape. QE's *net* contribution to convergence is higher. QE wins level 1.

## Selected Base: Variant 2 (Quality Engineer)

**Rationale**: QE's framing has the broadest INCORPORATE list (5 items, including the audit-log schema and repeat-failure detection that the analyzer also advocates), the strongest enforceability discipline, and the most concrete file:wave:cost mapping. The architect provides the workload-mismatch framing and the REJECT-rationale anchor; the analyzer provides the eval-evidence-driven prioritisation. QE absorbs both strengths and adds defense-in-depth.

## Strengths to preserve (from QE base)

- 5-item INCORPORATE list with file/wave/cost per item
- The schema-rigor framing (audit-log, hypothesis-card, REPORT.md)
- Explicit MEDIUM-vs-HIGH severity tagging on ADAPTs
- The repeat-failure detection + stale-codebase pairing (even though stale-codebase deferred)

## Strengths to incorporate from non-base variants

**From Architect**:
- The workload-mismatch framing in the executive summary (forensic and v2 solve different problems)
- The REJECT-rationale anchored to "no audience" / "no driver" / "no observed failure mode" — clearer than QE's defensive framing
- The 3 INCORPORATE → 5 INCORPORATE expansion path (architect was too conservative on hypothesis-card schema; we expand to audit-log + REPORT.md schemas)

**From Analyzer**:
- The frequency-weighted prioritisation (4 INCORPORATE driven by observed eval failure modes)
- The explicit list of failure modes observed in the 8 eval logs (4/8 audit-log format variation, 4/8 inline-validator fallback)
- The "wait for failure modes to fire" principle as the ordering rule for DEFERs

**From Invariant Probe**:
- 5 MEDIUM-severity UNADDRESSED items as "implementation gotchas" in the incorporation report
- Sufficiency-challenge framing: incorporation roadmap is *necessary* but not provably *sufficient* without post-incorporation eval evidence

## Selected base proceeds to refactoring plan with these strengths layered.
