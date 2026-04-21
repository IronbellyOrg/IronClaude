# Gaps and Questions — Roadmap & Tasklist Architecture Overhaul

**Date:** 2026-04-04
**Phase 3 verdict:** PASS (after fixing 1 CRITICAL, 2 IMPORTANT issues)

---

## Critical Gaps (RESOLVED)

| # | Gap | Source | Resolution |
|---|-----|--------|------------|
| C-1 | File 03 summary incorrectly stated inputs passed via `--file` flags | QA P1 | Fixed — corrected to describe `_embed_inputs()` inline embedding |

## Important Gaps (RESOLVED or ACCEPTED)

| # | Gap | Source | Status |
|---|-----|--------|--------|
| I-1 | Missing formal `[CODE-VERIFIED]` tags in files 01-04 | Analyst P1, QA P1 | Accepted — files cross-validate in prose, tags are formatting preference |
| I-2 | Certify step ambiguity in file 01 | QA P1 | Fixed — grep confirmed `build_certify_step()` is dead code (defined but never called) |
| I-3 | File 06 missed PRD suppression language at tasklist/prompts.py:221-223 | Analyst P2 | Noted — covered by file 08 (prior research context) which cross-validates this finding |
| I-4 | File 07 line references not explicitly code-verified | Analyst P2 | Accepted — template analysis doesn't involve code behavior claims |

## Minor Gaps

| # | Gap | Source |
|---|-----|--------|
| M-1 | Step numbering inconsistency in executor.py comments (duplicate "Step 8") | File 01 |
| M-2 | `convergence_enabled` has no CLI flag (programmatic only) | File 01 |
| M-3 | `--input-type` CLI accepts `auto/tdd/spec` but not `prd` (detect returns it) | File 02 |
| M-4 | TDD/PRD section references in prompts use hardcoded section numbers | File 03 |
| M-5 | Neither `build_diff_prompt` nor `build_debate_prompt` accept tdd_file/prd_file | File 03 |
| M-6 | Latent frontmatter parser bug — two parsers with conflicting behavior | File 05 |
| M-7 | Field name mismatch: `ambiguous_count` vs `ambiguous_deviations` in DEVIATION_ANALYSIS_GATE | File 05 |

## Open Questions for Synthesis

1. What is the optimal incremental writing strategy — subprocess tool-use (Sprint pattern) vs streaming output with checkpoints?
2. Should extraction be removed entirely for TDD/PRD or retained as optional with a bypass flag?
3. How should the roadmap output template handle variable-length content (many phases vs few)?
4. Should the tasklist generation move from skill-only to CLI pipeline, or should the skill be enhanced?
5. What is the migration path — can template-driven output coexist with current output during transition?
