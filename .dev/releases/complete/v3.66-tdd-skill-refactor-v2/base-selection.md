---
base_variant: "Opus (roadmap-opus-architect.md)"
variant_scores: "A:82 B:68"
---

## 1. Scoring Criteria (Derived from Debate)

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Timeline calibration — accuracy to 0.25 complexity | 10 | D-2 |
| C2 | Sync discipline — correct dev-copy workflow | 15 | D-3 (full agreement) |
| C3 | Phase structure — appropriate granularity | 10 | D-1 |
| C4 | Commit strategy — explicit atomic guidance | 10 | D-8 (full agreement) |
| C5 | Verification completeness — all 26 checks enumerable | 15 | D-5, SC-1–SC-12 |
| C6 | Parallelization guidance | 5 | D-10 |
| C7 | Architect recommendations — cross-cutting guidance | 10 | D-11 |
| C8 | Traceability — FR/NFR/SC mapping | 10 | D-5 |
| C9 | Evidence persistence — reusable artifact | 5 | D-6 |
| C10 | Actionability — can an implementer execute without ambiguity | 10 | Overall quality |

## 2. Per-Criterion Scores

| Criterion | Opus (A) | Haiku (B) | Rationale |
|-----------|----------|-----------|-----------|
| **C1: Timeline** | 9/10 | 4/10 | Opus's 85-min estimate matches 0.25 complexity. Haiku's 2 days is 10x inflated — debate Round 2 saw Haiku partially concede ("half a working day" would be better). |
| **C2: Sync discipline** | 10/10 | 5/10 | Opus correctly states dev copy comes from `make sync-dev` only. Haiku Phase 1 Task 1 says "Create... and sync copy" — both sides agreed this is a bug in Haiku's wording (D-3 full agreement). |
| **C3: Phase structure** | 7/10 | 7/10 | Debate concluded this is "cosmetic" (D-1). Opus folds baseline into Phase 1 (leaner). Haiku's Phase 0 is defensible but adds a gate for 15 min of work. Wash. |
| **C4: Commit strategy** | 10/10 | 2/10 | Opus has explicit single-commit recommendation with rationale (bisect safety, revert atomicity). Haiku omits entirely — conceded in debate as an omission (D-8 full agreement). |
| **C5: Verification** | 9/10 | 7/10 | Opus enumerates all 26 checks with specific grep/diff/wc commands per SC. Haiku lists SC-1–SC-12 but with less operational detail (no specific command invocations in Phase 3). |
| **C6: Parallelization** | 8/10 | 5/10 | Opus explicitly notes Phase 4 checks can be batched. Haiku is silent. Debate agreed inclusion is helpful though low-stakes. |
| **C7: Recommendations** | 9/10 | 5/10 | Opus has a consolidated Section 8 with 5 specific cross-cutting recommendations. Haiku distributes guidance but lacks a pre-flight checklist. Debate noted cross-cutting concerns (single commit, Phase 4 hard gate) have no natural phase home — favors Opus's approach. |
| **C8: Traceability** | 7/10 | 9/10 | Haiku's explicit "every phase closes with FR/NFR/SC mapping" rule and per-phase requirement coverage lists are stronger. Opus embeds traceability in task descriptions but lacks formal gate language. |
| **C9: Evidence report** | 5/10 | 8/10 | Opus produces no persistent artifact (YAGNI argument). Haiku's Phase 4 Task 3 produces a short evidence report. Debate was genuinely split, but for a pattern that repeats across 10+ skills, Haiku's 15-minute investment is sound. |
| **C10: Actionability** | 9/10 | 6/10 | Opus provides specific line numbers (48-63, 82-88), exact file paths, grep patterns, expected line counts at each phase. Haiku references the same data but with less operational precision and the sync-copy bug. |

## 3. Overall Scores

**Opus (A): 82/100**
- Strengths: Precise, operationally executable, correct sync discipline, explicit commit strategy, consolidated recommendations, calibrated timeline.
- Weaknesses: No evidence report artifact, traceability is implicit rather than gated.

**Haiku (B): 68/100**
- Strengths: Formal traceability gates, evidence report, open-questions escalation process.
- Weaknesses: Sync-copy wording bug (acknowledged), missing commit strategy (acknowledged), inflated timeline, less operational detail in verification phase.

## 4. Base Variant Selection Rationale

**Opus is the base** because:

1. **Correctness**: Opus has zero known bugs; Haiku has the sync-copy wording issue (D-3, acknowledged by both sides).
2. **Completeness on agreed points**: Opus already includes the two items both sides agreed were necessary — single atomic commit (D-8) and sync-derived dev copies (D-3). Haiku is missing both.
3. **Operational precision**: Opus's Phase 4 is immediately executable — specific grep patterns, expected line ranges, diff targets. Haiku's Phase 3 verification is structurally correct but less actionable.
4. **Timeline accuracy**: 85 minutes for a 0.25-complexity Markdown refactor executed by a Claude session is well-calibrated. Haiku's 2-day estimate was partially walked back in debate.

Starting from Opus requires adding 2-3 elements. Starting from Haiku requires fixing a bug, adding commit strategy, tightening verification detail, and recalibrating timeline — more editorial work for a weaker foundation.

## 5. Specific Improvements to Incorporate from Haiku

| # | Element from Haiku | Where to Merge in Opus | Priority |
|---|-------------------|----------------------|----------|
| 1 | **Formal traceability rule**: "Every phase closes with explicit FR/NFR/SC mapping before progressing" | Add as Recommendation #6 in Section 8, and add a `Requirement coverage` line at the end of each phase (lightweight — just the IDs, as Haiku does) | High |
| 2 | **Conditional evidence report**: Phase 4 Task 3 — "Produce short evidence report mapping SC and FR/NFR to checks" | Add to Opus Phase 4 as optional task: "If this refactor pattern will repeat for other skills, produce a short evidence report for template reuse" | Medium |
| 3 | **Open questions escalation**: "Any newly discovered ambiguity should be logged as a change request, not solved by in-scope expansion" | Add as a note in Section 3 (Risk Assessment) under RISK-03 mitigation, or as Recommendation #7 | Medium |
| 4 | **Reviewer role mention**: Haiku's Section 5 notes an architect + reviewer separation | Not needed for a 0.25-complexity task executed in a single session. Omit. | Low — skip |
| 5 | **Phase 0 as named phase**: Baseline capture as a distinct phase | Retain Opus's folded approach (Phase 1 Task 4) but strengthen the task language: "MANDATORY: Snapshot pre-migration state before any edits" | Low |
