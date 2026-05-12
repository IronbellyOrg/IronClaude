# QA Report -- Research Report Qualitative Review

**Topic:** PRD as Supplementary Pipeline Input
**Date:** 2026-03-27
**Phase:** report-qualitative
**Fix cycle:** 1

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Problem statement matches findings | PASS | See 1.1 below |
| 2 | Options are genuinely distinct | PASS | See 2.1 below |
| 3 | Recommendation follows from analysis | PASS | See 3.1 below |
| 4 | Implementation plan is actionable | FAIL | See 4.1 below |
| 5 | Gaps are honestly acknowledged | PASS | See 5.1 below |
| 6 | No circular reasoning | PASS | See 6.1 below |
| 7 | Evidence trail is complete | PASS | See 7.1 below |
| 8 | Conclusion is proportionate to evidence strength | PASS | See 8.1 below |
| 9 | Cross-section coherence | FAIL | See 9.1 below |
| 10 | Technical accuracy | PASS | See 10.1 below |
| 11 | Appropriate scope | PASS | See 11.1 below |
| 12 | Clarity | PASS | See 12.1 below |

## Summary
- Checks passed: 10 / 12
- Checks failed: 2
- Critical issues: 0
- Important issues: 1
- Minor issues: 0
- Issues fixed in-place: 1

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Section 8 vs Section 7 | Implementation plan does not reflect Option C's progressive delivery model. Section 7 recommends two independently shippable phases (Phase 1 = P1 builders, Phase 2 = P2 + skill docs), but Section 8 presents 4 sequential implementation steps that include ALL prompt enrichment (P1 and P2) in a single "Phase 2" and all skill docs in a single "Phase 3". A developer following Section 8 would build Option A (full enrichment in one pass), not Option C (progressive). Specifically: Section 8 Phase 2 includes `build_extract_prompt_tdd` (step 2.1.3-2.1.4) and `build_score_prompt` (step 2.4), both of which Section 7.4 explicitly defers to the second delivery increment. | Restructure Section 8 into two top-level delivery increments matching the Option C recommendation. Delivery 1: Phases 1-2 covering only P1 prompt builders (extract, generate, spec-fidelity, test-strategy) + tasklist fidelity, with testing. Delivery 2: P2 prompt builders (extract_tdd, score) + P3 API-only stubs + skill/reference layer + comprehensive TDD+PRD interaction tests. Each delivery increment must be independently shippable and testable. |

## Detailed Evidence

### 1.1 Problem statement matches findings

The research question (Section 1.1) asks how `--prd-file` should be added as supplementary input to roadmap and tasklist pipelines. The findings directly answer this: they map every prompt builder, identify the 4-layer wiring pattern from the existing TDD integration, quantify the PRD content loss (82% of sections not reaching the pipeline), and produce a concrete implementation plan. The investigation did not drift -- every section contributes to answering the stated question.

### 2.1 Options are genuinely distinct

The three options (Full, Minimal, Progressive) vary on a meaningful dimension: implementation scope per delivery increment. Option A ships everything at once (12-14 files, 2-3 sessions). Option B ships only the highest-value touchpoints and defers the rest indefinitely (7-9 files, 1 session). Option C splits into two planned increments (7-9 then 6-8 files, 1+1 sessions). The trade-offs are real: coverage vs velocity, skill doc freshness vs delivery speed. These are not cosmetic variations.

### 3.1 Recommendation follows from analysis

Option C scores best on the value-per-effort dimension the report emphasizes. The comparison table (Section 6.4) shows Option C delivers 80% of PRD value in Phase 1 (matching Option B's coverage) while committing to eventual full coverage (matching Option A's completeness). The rationale in Section 7.1 cites five specific reasons, each traceable to analysis in Sections 4-6. The recommendation does not contradict the scoring.

### 4.1 Implementation plan is actionable (FAIL)

The implementation plan is detailed enough that a developer could start work -- step-level actions with file paths, line numbers, and specific code changes. However, the plan's phase structure contradicts the recommended option. See Issues Found #1 above. The plan is actionable for Option A but does not faithfully implement Option C.

### 5.1 Gaps are honestly acknowledged

Section 9 contains 18 open questions across three categories (gaps log, research files, unverified claims). The report does not hide uncertainty: Q7 flags unverified PRD template section numbering as IMPORTANT, Q3 explicitly states that PRD enrichment improves task quality not quantity, and Q14 acknowledges potential token budget issues. Section 4.4 documents 5 contradictions found between research files. The gaps log (`gaps-and-questions.md`) is referenced and traceable.

### 6.1 No circular reasoning

Every claim traces to either (a) code-verified research files with specific line numbers, (b) the web research file with external source URLs, or (c) synthesis files that reference the underlying research. The report does not cite its own conclusions as evidence. The external research (Section 5) cites 27 unique sources with specific URLs and is clearly labeled as external context requiring internal validation.

### 7.1 Evidence trail is complete

Section 10 inventories 6 codebase research files, 1 web research file, 6 synthesis files, and 1 gaps log. Every major claim in the report includes a source citation with file name, section number, and line range. Spot-checked 5 code claims against actual source:
- `tdd_file` at `models.py` line 115: CONFIRMED (actual line 115)
- `build_extract_prompt` at `prompts.py` line 82: CONFIRMED (actual line 82)
- `--tdd-file` at `tasklist/commands.py` lines 61-66: CONFIRMED (actual lines 61-66)
- `tdd_file` at `tasklist/models.py` line 25: CONFIRMED (actual line 25)
- `tdd_file` dead code in roadmap executor: CONFIRMED (grep returns no matches)

### 8.1 Conclusion is proportionate to evidence strength

The recommendation is "Option C with high confidence" backed by: complete code audit of both pipelines, a working reference implementation (TDD integration in tasklist), 6 detailed research files covering every code layer, and external research validating the architectural approach. The confidence level matches the evidence depth. The report does not overclaim -- it explicitly acknowledges Phase 1 limitations (TDD+PRD gap, scoring without PRD signals, inference workflow gap) in Section 7.2.

### 9.1 Cross-section coherence (FAIL)

Most sections tell a consistent story. However, Sections 7 and 8 diverge on phase structure. Section 7 describes Option C as two independently shippable delivery phases. Section 8 describes four sequential implementation phases that encompass all work (matching Option A). See Issues Found #1. All other cross-section references are coherent: numbers match (20 gaps, 10 prompt builders, 28 PRD sections), terminology is consistent, and forward/backward references resolve correctly.

### 10.1 Technical accuracy

Code-verified claims checked against actual source files (see 7.1 above). File paths are correct. Function signatures match. Line numbers are accurate. The data flow diagram (Section 2.1) correctly represents the pipeline architecture. The TDD integration pattern trace (Section 2.2) matches the actual code. The claim about 7-of-10 builders using single-return pattern was verified by reading `prompts.py`.

### 11.1 Appropriate scope

The report covers exactly what was asked: how to add `--prd-file` to both pipelines. It does not scope-creep into redesigning the pipeline architecture, changing the extraction agent, or modifying `detect_input_type()`. The TDD+PRD interaction model is explicitly addressed in Section 3.2 (SC-4), Section 7.2 (trade-off acknowledgment), Section 8 Phase 4 (test matrix scenarios A-D including "Both"), and Section 9.2 Q13 (triple input handling). The report also properly scopes the skill/reference layer updates as secondary to CLI code changes.

### 12.1 Clarity

The report is well-structured and navigable. A reader unfamiliar with the codebase can follow the argument because: (a) Section 2 builds up the architecture layer by layer before introducing gaps, (b) tables are used consistently for structured data, (c) the data flow diagram provides visual orientation, (d) every code reference includes file path and line number, (e) the options analysis uses a consistent comparison framework. The writing is precise and technical without being obscure.

## Actions Taken

**Issue #1 (IMPORTANT): Implementation plan phase structure mismatch.**

Fixed in-place by restructuring Section 8 of the research report. The four sequential implementation phases were reorganized into two delivery increments matching Option C:
- **Delivery 1** (independently shippable): Model/CLI plumbing (both pipelines) + P1 prompt enrichment (extract, generate, spec-fidelity, test-strategy) + tasklist fidelity prompt + testing for Delivery 1 scope.
- **Delivery 2** (independently shippable): P2 prompt enrichment (extract_tdd, score) + P3 API-only stubs (diff, debate, merge) + skill/reference layer updates + TDD+PRD interaction tests.

Moved `build_extract_prompt_tdd` (steps 2.1.3-2.1.4) and `build_score_prompt` (step 2.4) from the main prompt enrichment phase into Delivery 2. Added delivery increment headers and clarified that each increment is independently testable and shippable.

Verified fix by re-reading Section 8 and confirming alignment with Section 7's Phase 1/Phase 2 scope descriptions.

## Recommendations
- No further action required. The single issue was fixed in-place.

## QA Complete
