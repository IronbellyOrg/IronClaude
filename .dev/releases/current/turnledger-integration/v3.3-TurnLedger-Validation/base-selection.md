---
base_variant: "Opus"
variant_scores: "A:81 B:72"
---

# Evaluation: v3.3 TurnLedger Validation Roadmaps

## 1. Scoring Criteria (Derived from Debate)

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Implementation readiness — can an implementer start coding immediately? | 20% | D-2, D-3: actionability debate |
| C2 | Requirement traceability — are all 13 FRs and 12 SCs explicitly mapped? | 15% | D-3, Round 2 rebuttals |
| C3 | Risk management — are mitigations actionable, not just identified? | 15% | D-6, R-1 through R-5 |
| C4 | Phasing correctness — do dependencies flow forward without cycles? | 15% | D-6, Phase 0 debate |
| C5 | Timeline honesty — do estimates reflect 0.82 complexity reality? | 10% | Round 2: Haiku's range argument |
| C6 | Integration point completeness — are all wiring mechanisms documented? | 10% | D-2: 6 vs 8 mechanisms |
| C7 | Scope discipline — no unnecessary ceremony for single-agent sprint CLI | 10% | D-1: Phase 0 debate, Round 3 concessions |
| C8 | Durability — will the roadmap survive rebases and code changes? | 5% | Round 2: line number fragility |

## 2. Per-Criterion Scores

| Criterion | Opus (A) | Haiku (B) | Justification |
|-----------|----------|-----------|---------------|
| **C1: Implementation readiness** | 92 | 65 | Opus provides exact task tables with test counts, file paths, and requirement mappings per task. Haiku lists requirement IDs but defers test count and granularity decisions to the implementer. An implementer can start Phase 1A from Opus immediately; Haiku requires Phase 0 first. |
| **C2: Requirement traceability** | 85 | 80 | Both map all 13 FRs and 12 SCs. Opus embeds mapping inline per task (e.g., "2A.1: FR-1.1–FR-1.4"). Haiku provides Section 6 validation strategy but lacks per-task granularity — FR-1.1 through FR-1.18 are listed as a block, not individually assigned. |
| **C3: Risk management** | 80 | 75 | Identical risk identification (R-1 through R-5, same severities). Opus adds concrete mitigation actions (e.g., "start with allowlist of known FR→function mappings"). Haiku adds exit criteria per risk, which is useful but less actionable during implementation. |
| **C4: Phasing correctness** | 85 | 70 | Both use the same 4-phase structure. Opus correctly places AST analyzer in Phase 1B parallel with 1A (Haiku conceded this in Round 3). Haiku defers full AST implementation to Phase 3, concentrating risk. Haiku's Phase 0 was conceded as unnecessary. |
| **C5: Timeline honesty** | 65 | 85 | Opus gives fixed "~11 days" — Haiku correctly argued this is false precision at 0.82 complexity (Round 2). Haiku's 7.5–14 day range better reflects uncertainty. Opus conceded ranges are more honest in Round 3. |
| **C6: Integration points** | 72 | 88 | Haiku identifies 8 mechanisms with standalone Section 3, each with named artifact, wired components, owning phase, cross-references, and architect notes. Opus covers 6 inline. Opus conceded `merge_findings()` deserves explicit tracking (Round 3). |
| **C7: Scope discipline** | 88 | 60 | Haiku's Phase 0, team roles (4 roles for single-agent execution), and validation checkpoints A–D add ceremony. Haiku conceded Phase 0 is overkill for single-agent execution. Opus is leaner and correctly sized for the sprint CLI context. |
| **C8: Durability** | 60 | 80 | Opus references specific line numbers (executor.py:735, wiring_gate.py:673) that are already stale per git status showing uncommitted modifications. Haiku uses architectural descriptions that survive rebases. Opus conceded this point. |

## 3. Overall Scores

| Variant | Weighted Score | Strengths | Weaknesses |
|---------|---------------|-----------|------------|
| **A (Opus)** | **81** | Immediately actionable task tables; pre-resolved open questions; explicit test counts enabling SC-1 tracking; correct AST phasing; lean scope | Fragile line references; false-precision timeline; 6/8 integration points documented |
| **B (Haiku)** | **72** | Honest timeline ranges; complete integration point documentation; durable architectural references; validation checkpoints; exit criteria on risks | Phase 0 overhead (self-conceded); deferred test counts; AST in wrong phase (self-conceded); team roles unnecessary for context |

## 4. Base Variant Selection Rationale

**Opus is the correct base** for three reasons:

1. **Implementation readiness dominates.** This roadmap feeds a sprint CLI runner — the consumer needs task-level specificity, not architectural elegance. Opus's per-task tables with requirement mappings and test counts are directly executable.

2. **Debate concessions favor Opus's structure.** Haiku conceded on Phase 0 (unnecessary), AST phasing (Opus's 1B is better), and test count specificity (needed for SC-1). These are structural concessions that would require restructuring Haiku to incorporate.

3. **Opus's weaknesses are additive fixes.** Adding range estimates, two more integration points, and removing line numbers are patch operations. Haiku's weaknesses (adding test counts, removing Phase 0, moving AST to Phase 1B) require restructuring.

## 5. Specific Improvements to Incorporate from Haiku

| # | Haiku Element | Where to Merge | Rationale |
|---|--------------|----------------|-----------|
| 1 | **Range-based timeline** | Timeline Summary table: add range column (e.g., "~5 days (3–7)") | Opus conceded; false precision undermines planning credibility |
| 2 | **Integration points 7 & 8** (`merge_findings()`, registry constructor) | Add to Opus's dispatch mechanisms enumeration as named artifacts with cross-references | Opus conceded `merge_findings()` is load-bearing for Phase 3; registry constructor is an integration boundary |
| 3 | **Validation checkpoints A–D** | Add as sub-milestones within Opus's existing milestone structure | Finer-grained progress tracking without adding ceremony; checkpoints map cleanly to Opus's phases |
| 4 | **Architectural descriptions replacing line numbers** | Replace "executor.py:735" with "executor phase delegation branch" + approximate location | Opus conceded line numbers are fragile given uncommitted modifications on branch |
| 5 | **Risk exit criteria** | Append one-line exit criterion to each risk in Opus's risk table | Haiku's exit criteria make risk mitigation verifiable without adding bulk |
| 6 | **Section 3 standalone integration appendix** | Add as appendix after Opus's main content, preserving Opus's inline cross-references | Both acknowledged standalone + inline is optimal; appendix doesn't disrupt Opus's task flow |
