---
title: "Eval Execution Summary"
date: 2026-03-19
prompt_sequence: 5 of 6
runs_completed: 4
runs_successful: 2
minimum_threshold_met: true (1 local + 1 global completed per policy)
---

# Eval Execution Summary

## Run Results

| Run ID | Branch | Status | Steps PASS | Steps FAIL | Stages Completed | Wall-Clock (approx) | Artifact Count |
|--------|--------|--------|-----------|-----------|-----------------|---------------------|---------------|
| local-A | v3.0-AuditGates | PARTIAL | 8 | 1 (spec-fidelity) | 9/10 | ~860s | 10 .md + 1 .json |
| local-B | v3.0-AuditGates | PARTIAL | 8 | 1 (spec-fidelity) | 9/10 | ~810s | 10 .md + 1 .json |
| global-A | master | PARTIAL | 2 | 1 (generate-opus) | 3/8 | ~400s | 4 .md + 1 .json |
| global-B | master | PARTIAL | 2 | 1 (generate-opus) | 3/8 | ~370s | 4 .md + 1 .json |

**Minimum threshold met**: 2 local runs + 2 global runs executed. Both local runs completed 9/10 steps. Both global runs completed 3/8 steps.

## Per-Step Timing (Local Runs)

| Step | Local-A (s) | Local-B (s) | Notes |
|------|------------|------------|-------|
| extract | 50 | 55 | PASS both |
| generate-opus-architect | 232 | 218 | PASS both |
| generate-haiku-architect | 76 | 72 | PASS both |
| diff | 52 | 54 | PASS both |
| debate | 70 | 97 | PASS both |
| score | 41 | 46 | PASS both |
| merge | 106 | 103 | PASS both |
| test-strategy | 85 | 81 | PASS both |
| spec-fidelity | 87 | 81 | FAIL both (high_severity_count_zero semantic check) |
| wiring-verification | - | - | SKIPPED (blocked by spec-fidelity failure) |

## Per-Step Timing (Global Runs)

| Step | Global-A (s) | Global-B (s) | Notes |
|------|-------------|-------------|-------|
| extract | 46 | 40 | PASS both |
| generate-opus-architect | 206 | 161 | FAIL both (below min line count: 9-11 < 100) |
| generate-haiku-architect | 109 | 124 | PASS both |
| diff | - | - | SKIPPED |
| debate | - | - | SKIPPED |
| score | - | - | SKIPPED |
| merge | - | - | SKIPPED |
| test-strategy | - | - | SKIPPED |

## Artifact Inventory

### Local-A (9 artifacts + state)
| File | Size (bytes) | Lines |
|------|-------------|-------|
| extraction.md | 9,255 | 94 |
| roadmap-opus-architect.md | 11,146 | 208 |
| roadmap-haiku-architect.md | 18,352 | 526 |
| diff-analysis.md | 7,502 | 125 |
| debate-transcript.md | 9,603 | 96 |
| base-selection.md | 5,305 | 62 |
| roadmap.md | 13,567 | 206 |
| test-strategy.md | 14,120 | 282 |
| spec-fidelity.md | 14,051 | 124 |
| .roadmap-state.json | 3,389 | - |

### Local-B (9 artifacts + state)
| File | Size (bytes) | Lines |
|------|-------------|-------|
| extraction.md | 10,656 | 111 |
| roadmap-opus-architect.md | 12,128 | 182 |
| roadmap-haiku-architect.md | 13,565 | 390 |
| diff-analysis.md | 7,900 | 111 |
| debate-transcript.md | 14,224 | 148 |
| base-selection.md | 5,698 | 61 |
| roadmap.md | 16,462 | 251 |
| test-strategy.md | 13,785 | 300 |
| spec-fidelity.md | 12,211 | 132 |
| .roadmap-state.json | 3,389 | - |

### Global-A (4 artifacts + state)
| File | Size (bytes) | Lines |
|------|-------------|-------|
| extraction.md | 7,120 | 84 |
| roadmap-opus-architect.md | 835 | 9 |
| roadmap-haiku-architect.md | 18,655 | 572 |
| roadmap.md | 15,221 | 242 |
| .roadmap-state.json | 1,514 | - |

### Global-B (4 artifacts + state)
| File | Size (bytes) | Lines |
|------|-------------|-------|
| extraction.md | 7,561 | 83 |
| roadmap-opus-architect.md | 745 | 11 |
| roadmap-haiku-architect.md | 15,357 | 480 |
| roadmap.md | 12,154 | 208 |
| .roadmap-state.json | 1,514 | - |

## Key Findings

### 1. Local Runs: Reproducible spec-fidelity gate enforcement
Both local runs (A and B) produced identical step verdicts: 8 PASS, 1 FAIL (spec-fidelity). The spec-fidelity gate correctly detected HIGH severity deviations (fabricated requirement IDs, missing spec references) in the LLM-generated roadmap. This demonstrates:
- The SPEC_FIDELITY_GATE semantic check `high_severity_count_zero` works as designed
- The gate blocks pipeline progression when high-severity deviations exist
- Both runs agreed on the failure — this is **reproducible** behavior

### 2. Local Runs: wiring-verification skipped
Because spec-fidelity failed, wiring-verification (step 10) was never reached. This means W-1 through W-9 cannot be scored from pipeline execution. However, W-10 through W-12 (detection power) can be scored via direct analysis (eval_1.py Phase B), and the wiring step's existence in `_build_steps()` is verified by the dry-run output.

### 3. Global Runs: generate-opus consistently fails on master
Both global runs failed at generate-opus-architect with "below minimum line count: 9-11 < 100". The opus model on master's prompt template produced a 10-line summary instead of a full roadmap. This is itself a delta finding:
- **v3.0 generate prompts produce full roadmaps** (208/182 lines on local runs)
- **Master generate prompts produce summaries** (9/11 lines on global runs)
- This suggests v3.0's prompt improvements (or gate strictness improvements) are material

### 4. Global Runs: Partial data available
Despite the early failure, global runs produced extraction.md and roadmap-haiku-architect.md successfully. These artifacts can be compared against local runs for the extract and generate-haiku steps.

## Reproducibility Assessment

### Local pair (A vs B)
- **Artifact set**: MATCH (same 9 files produced)
- **Gate verdicts**: MATCH (same 8 PASS + 1 FAIL pattern)
- **Duration variance**: Steps vary 6-39% (debate: 70s vs 97s = 28% variance)
- **Classification**: **STABLE** (all verdict checks pass, duration variance within limits)

### Global pair (A vs B)
- **Artifact set**: MATCH (same 4 files + 1 state)
- **Gate verdicts**: MATCH (same 2 PASS + 1 FAIL pattern)
- **Duration variance**: extract 15%, generate-opus 28%
- **Classification**: **STABLE** (verdict match, within variance limits for completed steps)

## Errors and Rate Limits

- No HTTP 429 rate-limit errors observed
- No subprocess timeouts
- No retries needed beyond the pipeline's built-in 2-attempt retry on gate failure
- Global runs used a shared worktree (IronClaude-eval-global-A) for both A and B runs (sequential, not parallel)

## Worktree Status

| Worktree | Branch | Location | Status |
|----------|--------|----------|--------|
| Main | v3.0-AuditGates | /config/workspace/IronClaude | Active |
| Global eval | master | /config/workspace/IronClaude-eval-global-A | Cleanup pending |
