# Consolidated Fidelity Findings — Phase 5.5 Gate 2.5 (Cycle 1 of max 2)

**Date:** 2026-04-30
**Cycle:** 1 of 2
**Source reports:** qa-fidelity-{1,2,3}-*.md

## Overall Verdict: FAIL

| Lens | Verdict | Critical | Important | Minor |
|---|---|---|---|---|
| F1 Reference-Skill Coverage | FAIL | 2 | 3 | 1 |
| F2 Spec FR Coverage | PASS | 0 | 0 | 0 |
| F3 Domain-Noun Leakage | FAIL | 1 | 3 | 2 |
| **Total** | — | **3** | **6** | **3** |

## Deduplicated Unique Findings (priority-ordered)

### CRITICAL

| ID | Issue | Affected Section | Source Lens | Suggested Fix |
|---|---|---|---|---|
| FC1 | **§21.1 fabricated 29-section schema** — fenced "logical 29-section" schema lists section names ("When to Use This Skill", "Stage A Output", "Delegate to /sc:task-unified") that don't match actual `## ` headers, canonical tech-research spine, or 12-section-classification.md. | Lines 1449-1483 | F1 | Replace fenced schema with the actual canonical 29-section list (S1-S29) matching tech-research convention; cross-reference `12-section-classification.md`. |
| FC2 | **`/sc:task-unified` leak** — "Stage B — Delegate to /sc:task-unified" is hallucinated; actual Stage B is the inline F1 execution loop. | Line 1472 | F1 | Remove the `/sc:task-unified` delegation reference; restore inline F1 execution loop description. |
| FC3 | **`Investigation type:` field name leak from tech-research** — present in S20 worker-prompt headers at lines 664, 780, 907. Workers will write this label into runtime output files, propagating tech-research vocabulary into runtime artifacts. | Lines 664, 780, 907 | F3 | Replace `Investigation type:` with persona-research-appropriate label `Subject research type:` or `Persona research type:` in all three worker-prompt headers. |

### IMPORTANT

| ID | Issue | Affected Section | Source Lens | Suggested Fix |
|---|---|---|---|---|
| FI1 | Inconsistent provenance tagging across S20 — three schemes ([SOURCE-VERIFIED], [MULTI-SOURCE-VERIFIED], [CODE-VERIFIED]) used for similar claims. | S20 throughout | F1 | Normalize to single tagging scheme: use [SPEC-VERIFIED] for spec-sourced claims, [CODE-VERIFIED] for code-sourced. |
| FI2 | Generation-time rules embedded as runtime Critical Rules — Rules 11, 12, 13, 16, 18 describe COPY/SUBSTITUTE/GENERATE classification, 29-section invariants, "Phase 2b spawned 3 spec analyst agents" — none apply to runtime persona-research execution. | Lines 1782-1796 (Critical Rules 11-18) | F1 | Remove or relocate generation-time-only rules from S27 Critical Rules. Persona-research runtime should have rules about identity verification, ethics floor, generic-purity — not about how this skill was built. |
| FI3 | Lens-QA prompt context conflation — S20 prompts mix "produced SKILL.md" vs runtime persona-research artifacts as inspection targets. | Lines 1117-1152 | F1 | Clearly separate skill-creator's build-time QA prompts from persona-research's runtime QA prompts. Generation-time lens prompts should be removed or relocated. |
| FI4 | "section classification" used as active domain noun in S20 QA prompts and S25 validation checklist (5 occurrences) — leaking skill-creator's vocabulary into the persona-research runtime skill. | S20, S25 | F3 | Replace with persona-research-appropriate terms (e.g., "dossier section taxonomy" or simply remove if generation-time only). |
| FI5 | "BUILD_REQUEST" surfaces as primary vocabulary in lens-QA prompts where it should be reframed for persona-research runtime. | Lens-QA prompts in S20 | F3 | Reframe "BUILD_REQUEST" references in runtime contexts. Acceptable in S18 A.7 BUILD_REQUEST template; not in runtime QA prompts. |
| FI6 | task-builder noun leakage — overlap with FI4/FI5. | S20 | F3 | Resolved by FI4/FI5. |

### MINOR

| ID | Issue | Suggested Fix |
|---|---|---|
| FM1 | Variable Reference rendered as `### Variable Reference` sub-section but listed as top-level S8 in §21.1. | Reconcile §21.1 schema with actual structure (resolved by FC1 fix). |
| FM2 | Three informational FR-23 mapping observations from F2 (loose mapping to three-questions test). | No fix required — non-blocking. |
| FM3 | "[SOURCE-VERIFIED]" tag inconsistency — partial duplicate of FI1. | Resolved by FI1. |

## Fix-Priority List

1. **FC1** Replace §21.1 fabricated schema with canonical 29-section list
2. **FC2** Remove `/sc:task-unified` hallucination
3. **FC3** Replace `Investigation type:` with persona-research label in S20 worker prompts
4. **FI1** Normalize provenance tagging scheme
5. **FI2** Remove generation-time rules from S27 Critical Rules
6. **FI3-FI5** Address skill-creator/task-builder noun leakage in S20

## Cycle Counter

**Cycle 1 of max 2** (Gate 2.5 — Source-Fidelity).

## Verdict

**FAIL — proceed to Step 5.7a (fix agent) — Cycle 1.**
