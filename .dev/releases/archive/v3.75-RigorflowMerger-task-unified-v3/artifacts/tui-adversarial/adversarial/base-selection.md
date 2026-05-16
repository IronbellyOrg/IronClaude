# Base Selection: TUI Top-5 Shortlist

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A | Variant B | Variant C |
|---|---|---|---|---|
| Requirement Coverage (RC) — covers all 10 P-NN with explicit slot or held-back rationale | 0.30 | 1.00 | 1.00 | 1.00 |
| Internal Consistency (IC) — 1 − (contradictions / total claims) | 0.25 | 0.95 | 0.92 | 0.93 |
| Specificity Ratio (SR) — concrete file:line citations vs vague claims | 0.15 | 0.85 | 0.88 | 0.91 (per-day ROI numerics) |
| Dependency Completeness (DC) — internal cross-references resolved | 0.15 | 0.92 | 0.94 | 0.93 |
| Section Coverage (SC) — variant-sections / max-sections | 0.15 | 0.83 (5/6 sections) | 1.00 (6/6 sections — adds Smoke-Test) | 1.00 (6/6 sections — adds Flagged-L) |

**Computed quant scores**:
- Variant A: (1.00×0.30) + (0.95×0.25) + (0.85×0.15) + (0.92×0.15) + (0.83×0.15) = **0.927**
- Variant B: (1.00×0.30) + (0.92×0.25) + (0.88×0.15) + (0.94×0.15) + (1.00×0.15) = **0.953**
- Variant C: (1.00×0.30) + (0.93×0.25) + (0.91×0.15) + (0.93×0.15) + (1.00×0.15) = **0.952**

## Qualitative Scoring (50% weight) — 30-criterion additive binary rubric

### Completeness (5 criteria) — per variant

| Criterion | A | B | C |
|---|---|---|---|
| Covers all explicit requirements (top-5 + held-back + sequencing) | MET | MET | MET |
| Addresses edge cases (e.g. dead-on-arrival P-10 failure mode) | MET | MET | MET |
| Includes dependencies | MET | MET | MET |
| Defines success/completion criteria | NOT MET (no explicit AC) | MET (Manual Smoke-Test AC) | NOT MET (per-day ROI math is not AC) |
| Specifies out-of-scope | MET (P-04/06/08/09/10 explicitly held-back) | MET | MET (with Flagged-L section) |

### Correctness (5 criteria)

| Criterion | A | B | C |
|---|---|---|---|
| No factual errors | MET | MET | MET |
| Technical approaches feasible | MET | MET | MET |
| Terminology consistent | MET | MET | MET |
| No internal contradictions | MET | MET | MET |
| Claims supported by file:line evidence | MET | MET | MET |

### Structure (5 criteria)

| Criterion | A | B | C |
|---|---|---|---|
| Logical section ordering | MET | MET | MET |
| Consistent hierarchy depth | MET | MET | MET |
| Clear separation of concerns | MET | MET | MET |
| Navigation aids | NOT MET (no TOC) | NOT MET | NOT MET |
| Follows artifact-type conventions | MET | MET | MET |

### Clarity (5 criteria)

| Criterion | A | B | C |
|---|---|---|---|
| Unambiguous language | MET | MET | MET |
| Concrete rather than abstract | MET (cites file:line) | MET (cites screen behaviour) | MET (cites per-day numerics) |
| Each section single-sentence summarisable | MET | MET | MET |
| Acronyms defined | MET | MET | MET |
| Actionable next steps | NOT MET (no AC) | MET (Smoke-Test ACs) | MET (day-by-day sequencing) |

### Risk Coverage (5 criteria)

| Criterion | A | B | C |
|---|---|---|---|
| ≥3 risks per proposal with prob+impact | MET | MET | MET |
| Mitigation per risk | PARTIAL (some flagged not mitigated) — NOT MET | MET (Manual Smoke-Test ACs are mitigations) | PARTIAL — NOT MET |
| Failure modes addressed | MET | MET | MET |
| External dependencies considered | MET | MET | MET |
| Monitoring/validation mechanism | NOT MET | MET (Smoke-Test ACs) | NOT MET |

### Invariant & Edge Case Coverage (5 criteria) — **edge-case floor applies**

| Criterion | A | B | C |
|---|---|---|---|
| Boundary conditions for collections | MET (_seen_files edge case flagged) | MET (NDJSON event count edge case) | MET (per-task subprocess subprocess startup window) |
| State variable interactions | MET (phase_started_at dual writers) | MET (heartbeat 0.0s ago failure) | MET (effort-tier interactions) |
| Guard condition gaps | MET (proc._process underscore-coupling) | MET (spinner false-positive risk) | MET (P-10 effective-effort = S+M) |
| Count divergence | NOT MET | NOT MET | MET (per-day ROI tie within noise) |
| Interaction effects | MET (P-07+P-03 compositional) | MET (P-03 alone half-fix) | MET (P-01+P-05 stack vs P-01+P-04 stack) |

**Edge case floor check**: All three variants score ≥4/5 on invariant coverage (well above 1/5 floor). All eligible.

### Qualitative summary

| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | **Total /30** | qual_score |
|---|---|---|---|---|---|---|---|---|
| A | 4 | 5 | 4 | 4 | 3 | 4 | **24** | 0.800 |
| B | 5 | 5 | 4 | 5 | 5 | 4 | **28** | 0.933 |
| C | 4 | 5 | 4 | 5 | 3 | 5 | **26** | 0.867 |

## Position-Bias Mitigation

Dual-pass evaluation (Pass 1 A→B→C order; Pass 2 C→B→A order). Disagreements: 2 criteria (B's "monitoring/validation mechanism" flipped MET ↔ NOT MET; C's "count divergence" flipped). Re-evaluation kept both as MET (B's Smoke-Test AC explicitly validates, C's per-day ROI math explicitly handles tie within noise). Final verdicts above reflect re-evaluation.

## Combined Scoring

| Variant | quant (×0.50) | qual (×0.50) | **combined** |
|---|---|---|---|
| A | 0.927 × 0.50 = 0.464 | 0.800 × 0.50 = 0.400 | **0.864** |
| B | 0.953 × 0.50 = 0.477 | 0.933 × 0.50 = 0.467 | **0.944** |
| C | 0.952 × 0.50 = 0.476 | 0.867 × 0.50 = 0.434 | **0.910** |

**Margin between top two**: B (0.944) − C (0.910) = 0.034 = 3.4% — within 5% tiebreaker zone.

## Tiebreaker Protocol Applied

Top two within 5% → apply tiebreaker levels:

**Level 1 — Debate performance** (points won in scoring matrix):
- A: won S-002 (60%) — 0.6 points
- B: won S-004 (75%) — 0.75 points
- C: won S-005 (65%) — 0.65 points
- B leads by debate performance. **B selected as base.**

(Levels 2 and 3 not needed.)

## Selected Base: Variant B

### Selection rationale
- Variant B's combined score (0.944) is highest by 3.4%.
- Variant B carries the universally-incorporated U-001 (Manual Smoke-Test Acceptance Criteria).
- Variant B's Round 3 final position matches the converged outcome exactly (P-01, P-05, P-02, P-03, P-07).
- Variant B has the highest qualitative score (28/30) — strongest on Clarity, Risk, and Smoke-Test-AC contributions.

### Strengths to preserve from B
- Manual Smoke-Test Acceptance Criteria section (universally-accepted unique contribution)
- Saliency-weighted ranking rationale
- Week-numbered sequencing labels (will be substituted for C's day-numbered labels per S-005)

### Strengths to incorporate from A
- U-003: Architectural layering critique for P-07 (assistant-text trim relocation from monitor.py to render-time)
- Steelmanned defence pattern for contested calls
- Explicit "ship P-01 last for fireworks landing" sequencing rationale
- INV-001/005 mitigation contract (test-driven `OutputMonitor.reset_for_next_task()` method)

### Strengths to incorporate from C
- U-002: Per-day ROI quantification (summarised, not reproduced in full)
- Flagged-L-effort section explicitly addressing P-09
- Day-numbered sequencing labels (replaces B's week-numbered per S-005 winner)
- INV-004 mitigation (15-min grep audit for prompt_preview consumers)
