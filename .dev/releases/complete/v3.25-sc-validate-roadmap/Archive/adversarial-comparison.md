# Adversarial Comparison: Three Roadmap Validation Prompts

**Date**: 2026-03-21
**Sources**:
- **P1 (Brainstorm)**: `prompt-brainstorm.md` — "Universal Roadmap-vs-Spec Validation Prompt"
- **P2 (Recommend)**: `prompt-recommend.md` — "Roadmap-to-Spec Fidelity Validator"
- **P3 (Direct)**: `prompt-direct.md` — "Universal Roadmap-vs-Spec Validation Prompt v2.0"

**Goal**: Compare all three across 10 design dimensions, pick the strongest approach per dimension, and justify the merge strategy for the unified prompt.

---

## 1. Requirement Extraction Algorithm

### P1 (Brainstorm)
Defines 17 explicit extraction categories in a table (FR, NFR, AC, Architectural Decisions, Open Questions, Risks, Test Plan, Data Models, API Contracts, Integration Points, Configuration, File Changes, Quality Gates, Inter-Release Contracts, Success Criteria, Sequencing Constraints, LOC/Effort Budgets). Each category has "What to Extract" and "Example" columns. Outputs to `requirement-universe.md`.

### P2 (Recommend)
Uses a YAML schema per requirement with typed fields: `id`, `type`, `description`, `source_file`, `source_lines`, `domain`, `priority`, `dependencies`. Defines a priority heuristic based on RFC-style language ("must"=P0, "should"=P1, "nice to have"=P2, "future"=P3). Types are: FR, NFR, SYSTEM, INTEGRATION, CONSTRAINT, BEHAVIOR, CONFIG, MIGRATION, ROLLOUT. Outputs to `00-spec-inventory.md`.

### P3 (Direct)
Uses a similar YAML schema: `id`, `text`, `source`, `type`, `priority`, `domain`, `testability`, `cross_cutting`, `related_reqs`. Has 12 types (FUNCTIONAL, NON_FUNCTIONAL, CONSTRAINT, DECISION, RISK_MITIGATION, INTEGRATION, DATA_MODEL, CONFIG, TEST, ACCEPTANCE_CRITERION, DEPENDENCY, PROCESS). Defines a 7-step extraction algorithm (explicit requirements, implicit requirements, test requirements, NFRs, integration requirements, process requirements, cross-cutting). Outputs to `extraction.md`.

### Verdict: HYBRID — P1 categories + P3 algorithm + P2/P3 YAML schema

**Justification**: P1 has the most exhaustive category list (17 categories covering edge cases like LOC budgets, inter-release contracts, and file changes that the others miss entirely). P3 has the best extraction ALGORITHM (ordered steps that tell the LLM where to look). P2/P3's YAML schema is more machine-parseable than P1's prose. The merge should use P1's category breadth as the extraction checklist, P3's ordered algorithm as the procedure, and the YAML schema for structured output.

---

## 2. Domain Decomposition / Agent Splitting Strategy

### P1 (Brainstorm)
5-step algorithm: (1) cluster by domain signal (file paths, tech, req type, section headers, system boundaries), (2) merge clusters <3 reqs, (3) split clusters >25 reqs, (4) ensure non-overlapping coverage, (5) cap at 20. Pure auto-detection, no hardcoded domain names. Cross-cutting requirements assigned to primary discipline with a cross-cutting list for consolidation.

### P2 (Recommend)
Domain-based partitioning with 3 steps: (1) group by domain, merge <3, (2) split >30, (3) mandatory cross-cutting agents (Internal Consistency Roadmap, Internal Consistency Spec, Dependency & Ordering, Completeness Sweep) that do NOT count toward the domain limit. Also has agent floor of 5 and ceiling of 20.

### P3 (Direct)
Domain Detection Heuristic: (1) group by domain tag, (2) merge <3, (3) split >15, (4) assign cross-cutting to primary domain with flag, (5) max 20 min 2. Provides 20 default domain categories as starting vocabulary. Has appendix examples for different project types.

### Verdict: HYBRID — P2 mandatory cross-cutting agents + P1 signal-based clustering + P3 default vocabulary

**Justification**: P2's mandatory cross-cutting agents (Internal Consistency, Dependency & Ordering, Completeness Sweep) are the standout innovation. These are structural validators that domain agents systematically miss. P1's signal-based clustering is the most principled detection method. P3's default domain vocabulary gives the LLM a useful starting point without being prescriptive. The split threshold should be 20 (between P1's 25 and P3's 15). Merge threshold stays at 3.

---

## 3. Coverage Status Model

### P1 (Brainstorm)
5 verdicts: COVERED (PASS), PARTIAL (WARN), MISSING (FAIL), CONTRADICTED (CRIT), IMPLICIT (INFO). Weighted scoring: IMPLICIT=0.25.

### P2 (Recommend)
5 statuses: COVERED, PARTIAL, MISSING, DISTORTED, IMPLICIT. Weighted scoring: PARTIAL=0.5, IMPLICIT not explicitly weighted. Adjudication phase adds 7 meta-verdicts: VALID-CRITICAL, VALID-HIGH, VALID-MEDIUM, VALID-LOW, REJECTED, STALE, NEEDS-SPEC-DECISION.

### P3 (Direct)
4 statuses: COVERED, PARTIAL, MISSING, CONFLICTING. Match quality sub-tier: EXACT, SEMANTIC, WEAK, NONE. No IMPLICIT status. Weighted scoring: PARTIAL=0.5. Confidence interval calculation with uncertainty margins.

### Verdict: HYBRID — P1's 5 statuses (rename CONTRADICTED to CONFLICTING) + P2's adjudication verdicts + P3's match quality sub-tier

**Justification**: P1's IMPLICIT status is important — it captures a real category (side-effect coverage) that P3 drops entirely. P2's adjudication phase (VALID-*, REJECTED, STALE, NEEDS-SPEC-DECISION) is the strongest post-processing model, especially STALE and NEEDS-SPEC-DECISION which address real failure modes. P3's match quality tier (EXACT/SEMANTIC/WEAK/NONE) adds useful granularity within COVERED/PARTIAL. Scoring: COVERED=1.0, PARTIAL=0.5, IMPLICIT=0.25, MISSING/CONFLICTING=0.

---

## 4. Evidence Standards

### P1 (Brainstorm)
5-part evidence: spec reference, roadmap reference, gap description, impact assessment, confidence (HIGH/MEDIUM/LOW). Confidence definitions: HIGH=direct textual evidence, MEDIUM=inference across sections, LOW=circumstantial.

### P2 (Recommend)
3-part evidence: spec evidence (file:line + quote), roadmap evidence (file:line + quote or ABSENT with search terms), confidence (HIGH/MEDIUM/LOW). Quote max 2 sentences. Finding must include severity, type, impact, suggested remediation, dependencies.

### P3 (Direct)
Evidence per requirement: spec source, spec text (exact quote), roadmap location, roadmap text (exact quote), match quality. Sub-requirement and acceptance criteria coverage tracked individually. Rule R7: "Quote, Don't Paraphrase."

### Verdict: HYBRID — P3's exact-quote mandate + P1's impact assessment + P2's search-terms-on-absence

**Justification**: P3's insistence on exact quotes with line numbers is the strongest evidence standard. P2's requirement to list search terms when something is ABSENT is excellent for proving the agent actually looked. P1's impact assessment ("what happens if this gap reaches implementation") is critical for prioritization and missing from the others. The merge should require: exact spec quote + line, exact roadmap quote + line (or ABSENT with search terms attempted), gap description, impact assessment, and confidence tier.

---

## 5. Cross-Cutting Concern Handling

### P1 (Brainstorm)
Dedicated Phase 4 (sequential, after all agents): integration point tracing (producer/consumer with sequencing), cross-cutting requirement verification (primary + secondary consistency), completeness boundary check (sum all requirements, compare to universe), sequencing consistency (dependency graph). Outputs to `cross-cutting-validation.md`.

### P2 (Recommend)
Mandatory cross-cutting agents spawned WITH the domain agents: Internal Consistency (Roadmap), Internal Consistency (Spec), Dependency & Ordering, Completeness Sweep. These run in parallel with domain agents. Additional Step 2.3 (consolidation) checks cross-cutting matrix from Phase 1.

### P3 (Direct)
Step 3.3 (Cross-Cutting Concern Validation) in consolidation: primary agent + secondary agent check. Step 3.4 (Integration Wiring Audit) with detailed per-integration-point assessment (system_a_side, system_b_side, wiring_task, error_handling, initialization_sequence — verdict: FULLY_WIRED, PARTIALLY_WIRED, UNWIRED).

### Verdict: HYBRID — P2's mandatory cross-cutting agents + P3's integration wiring audit model + P1's completeness boundary check

**Justification**: P2's approach of making cross-cutting validation parallel (as dedicated agents) rather than sequential (as a post-processing phase) is more efficient and catches more. P3's integration wiring audit is the most granular — it checks 5 dimensions per integration point. P1's completeness boundary check (sum all requirements across agents, verify against universe) is a critical safety net. The merge should spawn P2's cross-cutting agents in parallel, use P3's wiring audit model during consolidation, and include P1's boundary check as a mandatory consolidation step.

---

## 6. Consolidation / Merge Strategy

### P1 (Brainstorm)
Phase 5 (Consolidation): collect reports, compute aggregate metrics (overall coverage, weighted coverage, gap count by severity, discipline health, cross-cutting health), GO/NO-GO decision matrix with 5 conditions, write consolidated report with executive summary + all findings sorted by severity + remediation roadmap.

### P2 (Recommend)
Phase 2 (Consolidation): collect reports, build unified coverage matrix (handle conflicts: most specific assessment wins; domain overrides cross-cutting), deduplicate findings (3 rules), adversarial adjudication (7 verdicts with rules), freshness verification (re-read cited lines for HIGH+ findings), consolidated findings report with YAML frontmatter.

### P3 (Direct)
Phase 3 (Consolidation): collect reports, build unified gap registry with severity-prefixed IDs, cross-cutting validation, integration wiring audit, compute coverage scores with confidence intervals, generate report. Deduplication: merge same-gap-different-angles, keep separate-but-linked for different-aspects, escalate contradictions.

### Verdict: HYBRID — P2's adjudication + freshness verification + P3's confidence intervals + P1's decision matrix

**Justification**: P2's consolidation is the most rigorous: adjudication verdicts (VALID-*, REJECTED, STALE, NEEDS-SPEC-DECISION) and freshness verification (re-reading cited lines) are innovations that directly address the fix-and-fail loop. P3's confidence interval calculation adds useful uncertainty quantification. P1's GO/NO-GO decision matrix is the clearest decision framework. The merge should use P2's adjudication pipeline, P2's freshness verification, P3's confidence intervals, and P1's decision matrix criteria.

---

## 7. Adversarial Pass Design

### P1 (Brainstorm)
No dedicated adversarial pass. The adversarial posture is baked into the operational rules (Section 6.4): "Assume the roadmap is incomplete until proven otherwise." IMPLICIT gets 0.25 weight. Mentioning a requirement by ID without specificity is PARTIAL. This is passive adversarialism.

### P2 (Recommend)
No explicit adversarial pass. The adjudication step (2.4) serves a similar role: LOW confidence findings are re-verified, contradictory findings are re-read, quote-based findings are checked for freshness. This is adjudication-as-adversarialism.

### P3 (Direct)
Full dedicated Phase 4: Adversarial Pass with 11 specific checks: challenge every COVERED assessment, search for orphan requirements (buried in prose/footnotes/appendices/examples), search for orphan roadmap tasks (scope creep detection), validate sequencing, check silent assumptions, validate test coverage mapping, produce typed adversarial findings (MISSED_GAP, FALSE_COVERAGE, SEQUENCING_ERROR, ORPHAN_REQUIREMENT, ORPHAN_TASK, SILENT_ASSUMPTION, TEST_MISMATCH). Updates the consolidated report with new findings.

### Verdict: P3 wins decisively

**Justification**: P3's adversarial pass is a full independent review phase with 11 specific attack vectors. The "challenge every COVERED assessment" step is the most valuable — it actively tries to break the parallel agents' conclusions. Orphan requirement search (in prose, footnotes, appendices, examples) catches extraction failures. Silent assumption detection catches a class of bugs that no other approach addresses. P1 and P2 have adversarial elements but no dedicated pass. The merge must include P3's full adversarial phase.

---

## 8. Remediation Output

### P1 (Brainstorm)
Section in the consolidated report: per-finding remediation with finding ID, required action, effort estimate (trivial/small/medium), and dependencies. Integrated into the main report rather than a separate file.

### P2 (Recommend)
Dedicated Phase 3: dependency-ordered remediation plan with 9 phases (spec-internal contradictions first, then roadmap-internal, then missing coverage CRIT+HIGH, then distorted, then partial MEDIUM, then ordering fixes, then implicit-to-explicit promotion, then cleanup, then re-validate). Separate file `03-remediation-plan.md`. Includes revalidation checklist.

### P3 (Direct)
Dedicated Phase 5: prioritized by severity then effort then dependency. Concrete patch checklist per gap (file, line range, action type ADD/EDIT/MOVE/SPLIT/REMOVE, exact text change, verification method). Computes projected coverage after remediation. Separate file `remediation-plan.md`.

### Verdict: HYBRID — P2's phased ordering + P3's concrete patch format + projected impact

**Justification**: P2's 9-phase dependency ordering is the most principled — fixing spec-internal contradictions before roadmap gaps prevents cascading waste. P3's patch checklist format (action type, exact text, verification) is the most actionable. P3's projected coverage computation gives a clear picture of what remediation achieves. The merge should use P2's phase ordering, P3's per-gap patch format, and P3's projected impact calculation.

---

## 9. Operational Rules / Failure Mode Handling

### P1 (Brainstorm)
Section 6 (9 rules): artifact-based workflow, incremental writing, evidence-based, adversarial posture, no false positives, no false negatives, parallelism, spec hierarchy (release spec > tech spec > PRD), domain agnosticism. Section 9 (8 failure modes): vague spec, no requirement IDs, terminology mismatch, >20 disciplines, zero-gap suspicion, spec contradictions, oversized roadmap, missing referenced files.

### P2 (Recommend)
Section "Orchestrator Rules" (10 rules): write to disk, incremental construction, evidence or nothing, text on disk is authoritative, no hallucinated coverage, freshness verification mandatory, agents read-only, full coverage or explicit gap, no domain-proximity-conflation, cross-cutting agents mandatory. Also: "Design Rationale" section explaining WHY each design choice was made.

### P3 (Direct)
Section "Execution Rules" (15 rules): R1-R15 covering artifact workflow, incremental writing, evidence-based, spec is source of truth, no false positives, no false negatives, quote don't paraphrase, parallel independence, phase ordering, uncertainty reporting, cross-cutting double coverage, integration both sides, test fidelity exact, sequencing matters, preserve artifacts. Appendix B (10 edge cases): no requirement IDs, terminology mismatch, overlapping specs, orphan roadmap tasks, external references, very large specs (>500 reqs), very small specs (<10 reqs), tasklist-as-roadmap, nice-to-have/future items, agent failure/timeout.

### Verdict: HYBRID — P3's rules (most comprehensive) + P1's failure modes + P2's freshness verification rule + P1's spec hierarchy

**Justification**: P3 has the most rules (15) and the most edge cases (10). P1 adds the spec hierarchy rule (release spec > tech spec > PRD) which neither other prompt addresses. P2 adds the freshness verification rule and the no-domain-proximity-conflation rule. P1's failure mode table is the most structured (detection + recovery columns). The merge should include P3's full rule set, add P1's spec hierarchy and failure mode table, add P2's freshness verification and domain-proximity rules.

---

## 10. Overall Structure and Usability

### P1 (Brainstorm)
Linear flow: 10 sections. Clean execution flow diagram (Section 7). Three example invocations showing domain flexibility. Output file manifest. No YAML frontmatter. 582 lines.

### P2 (Recommend)
YAML frontmatter metadata. 4 phases (0-3) plus final summary. Numbered file prefixes (00-, 01-, 02-, 03-, 04-). Design rationale section explaining WHY. Usage examples. 645 lines.

### P3 (Direct)
6 phases (0-5). Appendices for domain examples and edge cases. Quick start section. Exclusions input parameter. 687 lines.

### Verdict: HYBRID — P3's phase structure + P2's numbered file naming + P1's execution flow diagram + P2's YAML frontmatter

**Justification**: P3's 6-phase structure (Ingestion, Decomposition, Parallel Execution, Consolidation, Adversarial, Remediation) is the most logical breakdown. P2's numbered file naming (00-, 01-, 02-) makes artifact ordering obvious. P1's execution flow diagram is the clearest quick-reference. P2's YAML frontmatter enables programmatic parsing. The merge should cut all three down to reduce redundancy — target ~500 lines.

---

## Summary: Merge Strategy by Dimension

| Dimension | Winner | Key Contribution |
|-----------|--------|-----------------|
| Requirement Extraction | HYBRID | P1 categories + P3 algorithm + YAML schema |
| Domain Decomposition | HYBRID | P2 mandatory cross-cutting agents + P1 signal clustering + P3 vocabulary |
| Coverage Status Model | HYBRID | P1's 5 statuses + P2's adjudication + P3's match quality |
| Evidence Standards | HYBRID | P3 exact quotes + P1 impact assessment + P2 search-terms-on-absence |
| Cross-Cutting Handling | HYBRID | P2 parallel agents + P3 wiring audit + P1 boundary check |
| Consolidation | HYBRID | P2 adjudication/freshness + P3 confidence + P1 decision matrix |
| Adversarial Pass | P3 | Full dedicated phase with 11 attack vectors |
| Remediation Output | HYBRID | P2 phased ordering + P3 patch format + projected impact |
| Operational Rules | HYBRID | P3 rules + P1 failure modes + P2 freshness + P1 spec hierarchy |
| Structure/Usability | HYBRID | P3 phases + P2 naming + P1 flow diagram + P2 frontmatter |

**Key themes**:
- P1 (Brainstorm) excels at: exhaustive category enumeration, spec hierarchy, failure mode handling, clear visual flow
- P2 (Recommend) excels at: adjudication/freshness verification, mandatory cross-cutting agents, dependency-ordered remediation, design rationale
- P3 (Direct) excels at: adversarial pass, edge case handling, integration wiring audit, evidence strictness, overall structure
