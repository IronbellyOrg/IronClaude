# Base Selection Report (Q31)

Scoring was done by the orchestrating session (this group worker acting as the skill's debate orchestrator), not by a separate agent. Source "requirements" for coverage are the eight points `Q31/question.md` asks an answer to handle: (R1) say whether the check applies; (R2) set the cadence-record row status; (R3) keep the line 579 limits (no `/sc:sweep` above the WC-16 cap, no write); (R4) record the answer in the ledger; (R5) deal with the order living in the lowest source tier; (R6) deal with the cron's session-only, 7-day life (fact 6); (R7) deal with `/sc:sweep` being not runnable yet (fact 7); (R8) deal with the 2026-11-09 reporting order (fact 5).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (proposal-A) | Variant 2 (proposal-B) | Variant 3 (proposal-C) |
|--------|--------|-------------------|-------------------|-----|
| requirement_coverage | 0.30 | 0.63 (R1, R2, R4, R5, R6 by avoidance; misses R3 statement, R7, R8) | 0.88 (all but R7) | 0.88 (all but R7) |
| internal_consistency | 0.25 | 1.00 (no internal contradiction found) | 1.00 | 0.95 ("only a timer-driven check sees them go idle" is overstated against WC-16's later `/sc:sweep` coverage; conceded by its advocate) |
| specificity_ratio | 0.15 | 0.85 | 0.80 ("for example", "or the orchestration guide", "if the contract has one") | 0.90 |
| dependency_completeness | 0.15 | 1.00 (no unresolved internal references; spec references are external) | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 (5 of 5) | 1.00 | 1.00 |
| **quant_score** | | **0.87** | **0.93** | **0.94** |

## Qualitative Scoring (50% weight): Additive Binary Rubric

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Covers explicit requirements | MET | "The ledger records Q31 = no ... row ... marked" | MET | "The ledger records Q31 = yes, read-only" | MET | "the last row of the cadence record ... becomes 'in force'" |
| Edge cases and failures | MET | "If one goes quiet or finishes, nothing in WC-16 notices it" | MET | "what happens on expiry and on resume" | MET | "can silently stop if the re-creation step is missed" |
| Dependencies and prerequisites | MET | relies on WC-16 and the 6.6 GitHub row | MET | "normal PR route (`/sc:pr-submit --monitor 3` on the fork)" | MET | CronCreate, ledger, `gh pr list --repo ...` |
| Success criteria | MET | ledger row and status | MET | ledger row; contract PR merges | MET | ledger row, job id and expiry recorded |
| Out of scope stated | MET | "This answer covers this program only" | NOT MET | no explicit out-of-scope line | MET | "Limits kept ... no grant implied" |
| **Subtotal** | **5/5** | | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| No factual errors | NOT MET | "nothing in WC-16 notices it" ignores WC-16's later `/sc:sweep` coverage of person-started sessions | MET | probe quote checked against `invariant-probe.md:18` | NOT MET | "only a timer-driven check sees them go idle" overstated (advocate concession) |
| Feasible | MET | no new mechanism | MET | PR route exists | MET | CronCreate exists in session |
| Terminology consistent | MET | | MET | | MET | |
| No internal contradictions | MET | | MET | | MET | ledger record is the coordinator's own note, not a write by the check |
| Claims supported | MET | cites memory, WC-16 | MET | cites INV-010, WC-16 | MET | cites line 579, both memories |
| **Subtotal** | **4/5** | | **5/5** | | **4/5** | |

### Structure (5 criteria)

All three use the same five headings in the order the brief prescribes, consistent depth, separate concerns, cross-references to spec lines, and the brief's convention. 5/5 each.

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Unambiguous language | MET | NOT MET (contract location and wording left open: "WC-16 or the orchestration guide") | MET |
| Concrete | MET | MET | MET |
| Each section has a clear purpose | MET | MET | MET |
| Terms defined | MET (WC-16 glossed) | MET | MET (ListAgents glossed as session list) |
| Actionable next steps | MET | MET | MET |
| **Subtotal** | **5/5** | **4/5** | **5/5** |

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| At least 3 risks with probability and impact | NOT MET (risks listed, no probability) | NOT MET | NOT MET |
| Mitigation for each risk | NOT MET (unwatched peers unmitigated) | NOT MET | NOT MET (read load unmitigated) |
| Failure modes and recovery | NOT MET | NOT MET (expiry named, no recovery) | MET (re-create on expiry or resume) |
| External dependency failures | MET (cron expiry avoided) | MET (CronCreate 7-day limit) | MET |
| Monitoring or detection | NOT MET | NOT MET | MET (job id and expiry in ledger) |
| **Subtotal** | **1/5** | **1/5** | **3/5** |

### Invariant and Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Collection boundaries (no peers, many peers) | NOT MET | NOT MET | NOT MET |
| State interactions across components | MET (cron fire as WC-16 wake) | MET | MET |
| Guard condition gaps | NOT MET | MET (rule must cover expiry and resume) | MET (no sweep above cap, no write) |
| Count divergence | MET (5-minute cap versus 10-minute check) | NOT MET | MET (about 144 cycles a day; within 5-minute cap) |
| Interaction effects | MET | MET | MET |
| **Subtotal** | **3/5** | **3/5** | **4/5** |

Edge-case floor (at least 1/5): all three eligible.

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 4/5 | 5/5 |
| Correctness | 4/5 | 5/5 | 4/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 4/5 | 5/5 |
| Risk Coverage | 1/5 | 1/5 | 3/5 |
| Invariant and Edge Case | 3/5 | 3/5 | 4/5 |
| **qual_score** | **23/30 = 0.77** | **22/30 = 0.73** | **26/30 = 0.87** |

## Position-Bias Mitigation

Pass 1 in input order (1, 2, 3) and pass 2 in reverse order (3, 2, 1) were both run by the same orchestrating context, so they are not independent evaluations; this is a known limit of this run.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Correctness: no factual errors | 1 | MET | NOT MET | DISAGREE | NOT MET (same overstatement pattern as Variant 3's, judged consistently) |

Disagreements re-evaluated: 1. Final verdicts changed: 1.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate points won |
|---|---|---|---|---|
| 1 (proposal-A) | 0.435 | 0.383 | **0.82** | 0 |
| 2 (proposal-B) | 0.465 | 0.367 | **0.83** | 0 sole (5 shared with 3) |
| 3 (proposal-C) | 0.470 | 0.433 | **0.90** | 12 (5 shared with 2), 2 ties |

**Margin**: 7 percentage points over Variant 2 (above the 5 percent tiebreak threshold)
**Tiebreaker applied**: No

## Selected Base: Variant 3 (proposal-C)

### Selection Rationale
Highest combined score and won or shared 12 of 14 debate points; all three advocates, including the advocates for Variants 1 and 2, named it the best answer for the owner (75, 65, 70 percent).

### Strengths to Preserve from Base
1. Scope matches the question ("this program's coordinator").
2. Concrete cron lifecycle handling (job id and expiry in the ledger, re-create on expiry or resume).
3. Applies the 2026-11-09 reporting order and keeps every line 579 limit.

### Strengths to Incorporate from Non-Base Variants
1. From Variant 2: name the contract promotion as a separate, later owner decision (U-001), without bundling it.
2. From Variant 1 and the shared-assumption responses: say that the owner's "yes" is the fresh confirmation of a 9-day-old memory order (A-001), and that the cron fires only while the coordinator is idle (A-002).
3. From the Variant 3 advocate's own concessions: correct the "only a timer-driven check" overstatement, state that subscriptions carry no message (WC-16 "never messaged"), and state the ledger entry is the coordinator's own record, not a write by the check.
