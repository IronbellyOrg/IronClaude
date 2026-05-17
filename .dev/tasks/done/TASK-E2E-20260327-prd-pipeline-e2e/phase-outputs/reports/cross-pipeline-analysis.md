# Phase 9: Cross-Pipeline Anti-Instinct Analysis
**Date:** 2026-03-31

## 4-Way Anti-Instinct Comparison

| Run | fingerprint | Threshold | obligations | contracts | Overall |
|-----|------------|-----------|-------------|-----------|---------|
| TDD-only (prior) | 0.76 | ≥0.7 PASS | 5 FAIL | 4 FAIL | FAIL |
| TDD+PRD (new) | **0.69** | ≥0.7 **FAIL** | 4 FAIL | 4 FAIL | FAIL |
| Spec-only (prior) | 0.72 | ≥0.7 PASS | 0 PASS | 3 FAIL | FAIL |
| Spec+PRD (new) | 0.78 | ≥0.7 PASS | 1 FAIL | 3 FAIL | FAIL |

## PRD Impact Assessment: MIXED

- **Spec path: POSITIVE** — fingerprint improved (0.72→0.78), PRD enrichment added value. One new obligation introduced (0→1) but fingerprint improved.
- **TDD path: NEGATIVE** — fingerprint REGRESSED (0.76→0.69, now below threshold). The PRD supplementary content in the TDD extraction may have caused the LLM to generate roadmap text that uses fewer backticked identifiers, diluting fingerprint density. Obligations slightly improved (5→4).

## Pipeline Step Comparison

All four runs have identical step pass/fail pattern: steps 1-7 (extract through merge) PASS, anti-instinct FAIL, wiring PASS (trailing), test-strategy and spec-fidelity SKIPPED. PRD enrichment did not change which steps pass or fail.
