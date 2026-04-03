# Consolidated Gaps and Questions

**Date:** 2026-04-03
**Source:** Analyst completeness report + QA research gate report (round 1, fixed)

## Gaps (resolved)
- IMPORTANT: 44/52 task count discrepancy in file 04 — FIXED (corrected to 44)
- IMPORTANT: Missing Status: Complete headers — FIXED (all 6 files now consistent)
- MINOR: Missing CODE-VERIFIED tags — acknowledged, procedural only

## Open Questions for Synthesis
1. What is the correct target task count for TDD+PRD? File 04 estimates ~73 if decomposed to baseline granularity. Is that the right floor?
2. Should the fix prioritize roadmap phasing (H1) or tasklist prompt instructions (H2)? Evidence supports both as contributing factors.
3. The output token ceiling finding (file 06) — is the consistent ~27-29K output token budget a hard model constraint or a soft behavior? Needs testing.
4. How should testing tasks be handled? The 5.6:1 testing consolidation (28→5) is the single biggest driver of task count reduction. Should tests always be standalone tasks?
