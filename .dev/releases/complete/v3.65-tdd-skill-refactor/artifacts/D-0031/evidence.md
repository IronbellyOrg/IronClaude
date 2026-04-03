# D-0031: Token Count Comparison Pre vs Post Refactor

**Task:** T05.09
**SC:** SC-14 (confirmed token reduction in pre-refactor vs post-refactor SKILL.md)
**Date:** 2026-04-03
**Status:** PASS

---

## Token Estimation Method

Token counts estimated using `chars / 4` approximation (standard GPT/Claude tokenizer heuristic).
Character, word, and line counts measured via `wc` on source files.

---

## Pre-Refactor Baseline (commit a9cf7ee)

Single monolithic file: `src/superclaude/skills/tdd/SKILL.md`

| Metric | Value |
|--------|-------|
| Lines | 1,387 |
| Words | 13,108 |
| Characters | 92,209 |
| **Estimated Tokens** | **~23,052** |

---

## Post-Refactor SKILL.md (working tree)

Reduced SKILL.md after extracting content to refs/:

| Metric | Value |
|--------|-------|
| Lines | 438 |
| Words | 4,254 |
| Characters | 30,684 |
| **Estimated Tokens** | **~7,671** |

---

## Refs Files (on-demand, not loaded at invocation)

These files are loaded only when needed during Stage B execution, not at skill invocation time:

| File | Lines | Words | Characters | Est. Tokens |
|------|-------|-------|------------|-------------|
| agent-prompts.md | 418 | 3,379 | 23,259 | ~5,815 |
| build-request-template.md | 140 | 2,132 | 15,312 | ~3,828 |
| operational-guidance.md | 117 | 1,158 | 8,149 | ~2,037 |
| synthesis-mapping.md | 143 | 888 | 6,917 | ~1,729 |
| validation-checklists.md | 139 | 1,487 | 10,038 | ~2,510 |
| **Total refs/** | **957** | **9,044** | **63,675** | **~15,919** |

---

## Comparison Summary

| Metric | Pre-Refactor | Post-Refactor SKILL.md | Reduction |
|--------|-------------|----------------------|-----------|
| Lines | 1,387 | 438 | **-949 (68.4%)** |
| Words | 13,108 | 4,254 | **-8,854 (67.5%)** |
| Characters | 92,209 | 30,684 | **-61,525 (66.7%)** |
| Est. Tokens | ~23,052 | ~7,671 | **-15,381 (66.7%)** |

### Invocation Cost Analysis

- **Pre-refactor invocation cost:** ~23,052 tokens (entire monolithic SKILL.md loaded)
- **Post-refactor invocation cost:** ~7,671 tokens (only reduced SKILL.md loaded)
- **Token savings per invocation:** ~15,381 tokens (66.7% reduction)

### Content Integrity Check

- Post-refactor SKILL.md + refs/ total: 30,684 + 63,675 = **94,359 characters**
- Pre-refactor total: **92,209 characters**
- Delta: +2,150 chars (~2.3% increase) — accounts for added ref-path directives, file headers, and structural metadata in the decomposed files

---

## SC-14 Verdict

**PASS** — Post-refactor SKILL.md is **66.7% smaller** than pre-refactor, confirming meaningful token reduction per NFR-TDD-R.1 invocation efficiency improvement. Content is preserved in refs/ files loaded on-demand only when needed.
