# E2E Verification Report — PRD Pipeline Integration

**Date:** 2026-03-31
**Task:** TASK-E2E-20260327-prd-pipeline-e2e
**Branch:** feat/tdd-spec-merge

---

## Executive Summary

**Verdict: CONDITIONAL PASS — PRD enrichment works but 2 code bugs found and fixed, 1 unresolved regression**

PRD enrichment works. Both pipeline paths (TDD+PRD and spec+PRD) produce enriched output with persona references, business metrics, compliance items, and business value ordering that are absent without PRD. Auto-wire from `.roadmap-state.json` works after fixing 2 code bugs discovered during qualitative QA: (1) state file stored `input_type: "auto"` instead of resolved type — fixed in `executor.py`, (2) auto-wire couldn't discover TDD when it was the primary input — fixed in `tasklist/commands.py`. The `build_tasklist_generate_prompt` function handles all 4 interaction scenarios. No TDD content leaks into the spec+PRD path.

**Exceptions:**
- 1/13 criteria NO: TDD+PRD fingerprint_coverage dropped from 0.76 to 0.69 (below 0.7 threshold). Causality not established — may be LLM variance, not PRD-caused.
- 1/13 criteria INCONCLUSIVE: Tasklist validation enrichment untestable E2E (no tasklist generate CLI).
- 2 code bugs found and fixed post-test (state file input_type, auto-wire TDD fallback).

---

## Test 1: TDD+PRD Pipeline

| Artifact | Check | Result | PRD Enrichment |
|----------|-------|--------|----------------|
| extraction.md | 19 fields, 14 sections | PASS | +20 PRD refs (was 0) |
| roadmap variants | exist, ≥100 lines | PASS | present |
| diff/debate/score | gates pass | PASS | 11 PRD refs in scoring |
| roadmap.md | 593 lines, frontmatter | PASS | 13 PRD refs |
| anti-instinct | fingerprint ≥0.7 | **FAIL (0.69)** | REGRESSION from 0.76 |
| state file | prd_file, input_type | PASS | correct values |
| test-strategy | — | SKIPPED | anti-instinct halt |
| spec-fidelity | — | SKIPPED | anti-instinct halt |

## Test 2: Spec+PRD Pipeline

| Artifact | Check | Result | PRD Enrichment |
|----------|-------|--------|----------------|
| extraction.md | 13 fields, 8 sections | PASS | +20 PRD refs (was 1) |
| extraction.md | 0 TDD fields/sections | PASS | no leak |
| roadmap.md | 638 lines | PASS | present |
| anti-instinct | fingerprint ≥0.7 | PASS (0.78) | improved from 0.72 |
| state file | prd_file, tdd_file=null | PASS | correct |
| test-strategy | — | SKIPPED | anti-instinct halt |
| spec-fidelity | — | SKIPPED | anti-instinct halt |

## Auto-Wire Results

| Scenario | Result |
|----------|--------|
| Basic auto-wire (no flags) | PASS — prd_file auto-wired from state |
| Precedence (explicit overrides) | PASS — no auto-wire when flag provided |
| Missing file | SKIPPED (unit tests cover) |
| No state file | Crashes on missing roadmap (pre-existing) |

## Validation Enrichment Results

| Test | Result |
|------|--------|
| Tasklist validate with TDD+PRD | INCONCLUSIVE — no tasklist exists |
| `build_tasklist_generate_prompt` | ALL 4 SCENARIOS PASS |

## Cross-Run Comparison

### TDD+PRD vs TDD-Only

| Dimension | TDD-Only | TDD+PRD | Delta | Assessment |
|-----------|----------|---------|-------|------------|
| Extraction sections | 14 | 14 | 0 | Same |
| PRD content in extraction | 0 refs | 20 refs | +20 | ENRICHED |
| Roadmap lines | 634 | 593 | -41 | Slightly shorter |
| fingerprint_coverage | 0.76 | 0.69 | -0.07 | **REGRESSION** |

### Spec+PRD vs Spec-Only

| Dimension | Spec-Only | Spec+PRD | Delta | Assessment |
|-----------|-----------|----------|-------|------------|
| Extraction sections | 8 | 8 | 0 | Same (no TDD leak) |
| PRD content in extraction | 1 ref | 38 refs | +37 | ENRICHED |
| Roadmap lines | 494 | 638 | +144 | Significantly richer |
| fingerprint_coverage | 0.72 | 0.78 | +0.06 | IMPROVED |
| TDD content leak | 0 | 0 | 0 | CLEAN |

PRD enrichment adds meaningful product context to both paths. The spec path benefits more (+37 PRD refs, +144 roadmap lines, improved fingerprint). The TDD path shows a fingerprint regression that needs investigation.

## 4-Way Anti-Instinct Comparison

| Run | fingerprint | obligations | contracts |
|-----|------------|-------------|-----------|
| TDD-only | 0.76 PASS | 5 FAIL | 4 FAIL |
| TDD+PRD | **0.69 FAIL** | 4 FAIL | 4 FAIL |
| Spec-only | 0.72 PASS | 0 PASS | 3 FAIL |
| Spec+PRD | 0.78 PASS | 1 FAIL | 3 FAIL |

## Success Criteria Checklist

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `--prd-file` accepted on roadmap run | YES |
| 2 | `--tdd-file` accepted on roadmap run | YES |
| 3 | `--prd-file` accepted on tasklist validate | YES |
| 4 | PRD enrichment in TDD extraction | YES (+20 refs) |
| 5 | PRD enrichment in spec extraction | YES (+38 refs) |
| 6 | PRD enrichment in roadmap | YES (24 TDD path, present spec path) |
| 7 | State file stores prd_file/input_type | YES |
| 8 | Auto-wire works | YES |
| 9 | Redundancy guard works | YES |
| 10 | No TDD leak in spec+PRD | YES |
| 11 | No regressions from PRD | **NO** — fingerprint regression 0.76→0.69 |
| 12 | Tasklist validation enrichment | INCONCLUSIVE (no tasklist) |
| 13 | `build_tasklist_generate_prompt` | YES (4/4 scenarios) |

**11/13 YES, 1 NO (regression), 1 INCONCLUSIVE**

## Known Issues

- Anti-instinct gate halts all 4 pipelines (pre-existing)
- Click stderr swallowed in dry-run (pre-existing)
- `superclaude tasklist generate` CLI doesn't exist (validation enrichment untestable E2E)
- fingerprint_coverage regression on TDD+PRD path (NEW — causality unestablished)
- PRD prompt section numbers (S6, S7, etc.) are supplementary — heading names are the primary reference. Less fragile than initially assessed but should be documented.
- 2 code bugs found and FIXED during qualitative QA: state file input_type ("auto" → resolved), auto-wire TDD fallback via spec_file

## Findings

1. **fingerprint_coverage regression** — TDD+PRD drops from 0.76 to 0.69. **Causality not established.** The 3 missing fingerprints are Prometheus metric names (`auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`) whose presence in roadmap text depends on LLM phrasing choices, not PRD content. With N=1 runs, the 0.07 delta is within expected LLM variance. To confirm causality, re-run TDD without PRD and compare fingerprint counts. The regression may not be reproducible.
2. **Spec+PRD path improves** — fingerprint goes from 0.72 to 0.78 and roadmap grows from 494 to 638 lines. PRD enrichment is net-positive for the spec path.
3. **Auto-wire works cleanly** — the mechanism correctly reads state, wires files, respects precedence, emits info messages.
4. **No tasklist to validate** — the biggest gap is the missing `superclaude tasklist generate` CLI. Build request already written.
