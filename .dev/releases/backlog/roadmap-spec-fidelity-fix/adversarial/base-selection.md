# Base Selection — Scoring Breakdown

## Quantitative Scoring (50% weight)

| Metric | Weight | S1 | S2 | S3 | S4 | S5 | S6 |
|--------|--------|----|----|----|----|----|----|
| Requirement coverage (RC) — addresses failure root causes | 0.30 | 0.40 (4/10 HIGHs) | 1.00 (gives all 10 a target) | 0.00 (wrong shape) | 0.00 (no real bug) | 0.40 (4/10 HIGHs) | 0.00 (workaround) |
| Internal consistency (IC) | 0.25 | 1.00 | 0.95 | 0.90 (some legacy override risk) | 1.00 | 0.95 | 1.00 |
| Specificity ratio (SR) — concrete vs vague | 0.15 | 1.00 (regex tokens, line refs) | 0.95 (per-mismatch tables, line refs) | 0.85 | 0.90 | 0.95 | 0.95 |
| Dependency completeness (DC) | 0.15 | 0.90 | 1.00 (cites all callers) | 0.80 | 0.85 | 0.85 | 0.95 |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.79** | **0.97** | **0.49** | **0.55** | **0.78** | **0.64** |

## Qualitative Scoring (50% weight) — 30-criterion CEV rubric (condensed)

| Dimension | S1 | S2 | S3 | S4 | S5 | S6 |
|-----------|----|----|----|----|----|----|
| Completeness (5) | 3 | 5 | 4 | 3 | 4 | 4 |
| Correctness (5) | 5 | 5 | 4 | 5 (math reconciled) | 5 | 5 |
| Structure (5) | 5 | 5 | 5 | 4 | 5 | 5 |
| Clarity (5) | 5 | 5 | 4 | 4 | 4 | 5 |
| Risk Coverage (5) | 4 | 5 | 5 | 3 | 5 | 5 |
| Invariant/Edge-Case (5) | 4 | 4 | 5 | 3 | 4 | 5 |
| **MET / 30** | 26 | 29 | 27 | 22 | 27 | 29 |
| **qual_score** | **0.87** | **0.97** | **0.90** | **0.73** | **0.90** | **0.97** |
| Edge-case floor (≥1/5) | PASS | PASS | PASS | PASS | PASS | PASS |

## Position-Bias Mitigation
Dual-pass evaluation (forward + reverse order). 4 criterion-variant pairs disagreed initially; all resolved on re-evaluation with identical verdicts. No verdicts changed.

## Combined Scoring

| Variant | quant×0.50 | qual×0.50 | **Final** | Rank |
|---------|------------|-----------|-----------|------|
| S2 | 0.485 | 0.485 | **0.970** | 1 |
| S5 | 0.390 | 0.450 | **0.840** | 3 |
| S1 | 0.395 | 0.435 | **0.830** | 2* |
| S6 | 0.320 | 0.485 | **0.805** | 4 |
| S3 | 0.245 | 0.450 | **0.695** | 5 |
| S4 | 0.275 | 0.365 | **0.640** | 6 |

\* S1 vs S5 within 5% (0.830 vs 0.840) → tiebreaker applied:
- L1 (debate performance): S1 won C-001 (unique); S5 won C-002 (unique). Tie.
- L2 (correctness count): both 5/5. Tie.
- L3 (input order): S1 precedes S5 → S1 ranked 2nd.

## Selected Base: **S2 — Route Manifest Findings to Roadmap Target + Per-Mismatch Fix Guidance**

### Selection Rationale
S2 wins on three orthogonal axes:
1. **Failure-shape match**: Directly addresses the load-bearing `files_affected=[]` gap that prevents remediation of ALL 10 HIGHs.
2. **Unique contribution (U-001)**: Per-mismatch `fix_guidance` templates — no other solution touches this and the debate established it is necessary for routing alone to be effective.
3. **Synergy**: Amplifies S1 (S1 removes noise, S2 ensures the remainder is fixable) and S5 (S5 demotes NFR softs, S2 routes anything that remains).

### Strengths to Preserve
- Per-mismatch routing table keyed on `(dimension, mismatch_type)` → roadmap or AMBIGUOUS
- Templated `fix_guidance` per mismatch_type
- `AMBIGUOUS` deviation_class for spec-defect edge cases (nfrs/security_missing)
- Prompt-template additive-edits nudge

### Strengths to Incorporate from Other Variants
- **From S1**: Regex sanitization in `extract_file_paths_from_tables` to prevent S2 from routing phantoms to the roadmap. **Critical pre-merge** — without S1, S2 will add nonsense rows.
- **From S5**: Per-section iteration in `check_nfrs` so NFR soft findings get appropriate severity. Eliminates 4 HIGHs without needing to "fix" them via remediation.

### Excluded
- **S3** (tiered diff relax) — addresses a different failure shape; defer.
- **S4** (budget overhaul) — math is fine; observability-only improvements deferred.
- **S6** (MANUAL_TRIAGE halt) — useful as safety net but unnecessary if S1+S2+S5 converge cleanly. Defer.
