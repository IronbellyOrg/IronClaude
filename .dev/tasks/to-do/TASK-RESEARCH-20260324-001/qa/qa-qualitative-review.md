# QA Report — report-qualitative

**Topic:** IronClaude PRD/TDD/Spec Pipeline Architecture
**Date:** 2026-03-24
**Phase:** report-qualitative
**Fix cycle:** 1
**Document reviewed:** RESEARCH-REPORT-prd-tdd-spec-pipeline.md

---

## Overall Verdict: PASS (after in-place fixes)

All issues found were fixed in-place during this review cycle. The document is clear to proceed.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Problem statement matches findings | PASS | S1 accurately frames the verification mission, lists the 5 CODE-CONTRADICTED claims by table, and explains why each affects implementation scope. The findings in Sections 2-4 directly answer the research question. |
| 2 | Current state analysis is coherent | PASS | S2 provides a non-contradictory, component-by-component picture of the pipeline. Each subsection (2.1-2.5) is tagged CODE-VERIFIED against a named research file. The pipeline diagram in 2.6 is internally consistent with all subsections. |
| 3 | Gap analysis is honest | PASS | All gaps reference specific code evidence. Severities are proportionate: Critical gaps block Option 3 entirely (--spec flag zero implementation, sc:spec-panel cannot create specs). High gaps degrade output quality. The three Low-severity frontmatter gaps explicitly note they produce no pipeline value without simultaneous changes. No manufactured or inflated gaps found. |
| 4 | Options are genuinely distinct | PASS | The three options represent meaningfully different approaches: (1) no changes, (2) single new conversion step through sc:spec-panel only, (3) full pipeline upgrade across 4 tools. Option 2 is not just a lite version of Option 3 — it deliberately avoids touching sc:tasklist and sc:roadmap. The tradeoff table surfaces real differences in maintainability and data richness. |
| 5 | Recommendation follows from analysis | PASS | Option 3 is recommended. The 5-point rationale directly references verified findings: --spec flag as declared-but-dead extension point (File 03), spec-panel Boundaries constraint (File 01), frontmatter-is-ignored finding (File 06). Each rationale point cites the specific research file that supports it. The recommendation is consistent with the options scoring. |
| 6 | Implementation plan is actionable | FAIL | Phase 5, Addition 2 contains CRITICAL errors: the synthesis file names listed are PRD skill files (synth-03-competitive-scope.md, synth-04-stories-requirements.md, etc.), not TDD skill files (synth-03-architecture.md, synth-04-data-api.md, etc.). A developer following this plan would be editing the wrong skill's files. Additionally, the note at the end of Addition 2 states that "synth-01, synth-02, synth-08, and synth-09 do not require PRD extraction" — this is exactly backwards. These four files already read PRD extraction according to the report's own Section 2.5 and verified code. |
| 7 | Open questions are genuinely unresolved | FAIL | Four open questions are actually answerable from evidence already in the report or from direct code verification: (a) OQ-1 (spec_type as variable being read) — grep of sc-roadmap-protocol/ returns zero matches; (b) OQ-7 (domain_spread denominator) — scoring.md line 17 confirms `min(domains / 5, 1.0)`, denominator update IS required; (c) OQ-5 (rf-prd-extractor agent existence) — `.claude/agents/` listing confirms no such file exists; (d) OQ-10 (PRD_REF auto-population) — PRD SKILL.md line 491 confirms PRD_REF is not auto-populated. All four should be in Section 9.2, not Section 9.1. |
| 8 | Evidence trail is complete | PASS | Section 10 lists all 6 research files, 4 synthesis files, 5 QA reports, 1 gaps log, and 15 source files. The file inventory matches the task directory structure. Research file statuses are accurate (all Complete). QA report verdicts match what a review of the reports would find. |
| 9 | No circular reasoning | PASS | Claims trace from research files to actual code, not from the report back to itself. The five CODE-CONTRADICTED claims are each sourced to a specific research file and a specific source file. No claim uses "the report concludes X" as evidence for X. |
| 10 | Conclusion is proportionate to evidence | PASS | The recommendation carries appropriate confidence. It acknowledges Option 3's high effort and medium risk rather than underselling them. The success criteria in Section 3.3 specify measurable deltas. The "bounded scope" claim is qualified by noting the highest risk is the scoring formula rebalancing, which is accurate and substantiated by the verified 7-factor weight table. |
| 11 | CODE-CONTRADICTED claims correctly reflected | PASS | All 5 contradicted claims from the analysis document are correctly carried through the report. Each appears in S1.3 (summary table), in the relevant subsection of S2 with explicit [CODE-CONTRADICTED] tags, in S4.6 (correctness gaps table), and in S6 Options Analysis (specifically, spec-panel's Boundaries constraint is called out in Option 2's Cons and again in S7 recommendation point 3). No contradicted claim is inadvertently perpetuated as a current-state fact. |
| 12 | Implementation plan uses real file paths and field names | FAIL | Phase 5, Addition 2 uses PRD skill synthesis file names instead of TDD skill synthesis file names. The actual TDD skill synthesis files are synth-01-exec-problem-goals.md through synth-09-risks-alternatives-ops.md. The plan lists synth-03-competitive-scope.md, synth-04-stories-requirements.md, synth-05-technical-stack.md, synth-06-ux-legal-business.md, synth-07-metrics-risk-impl.md — these are PRD skill synthesis files from `.claude/skills/prd/` and do not exist in `.claude/skills/tdd/`. |

---

## Summary

- Checks passed: 9 / 12
- Checks failed: 3 (Checks 6, 7, 12)
- Critical issues: 2 (Checks 6 and 12 — same root cause: wrong synthesis file names and inverted note)
- Important issues: 4 (Check 7 — stale open questions OQ-1, OQ-5, OQ-7, OQ-10)
- Issues fixed in-place: 6 (all issues resolved; see Actions Taken)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | S8 Phase 5, Addition 2, table rows | Implementation plan lists PRD skill synthesis file names (synth-03-competitive-scope.md, synth-04-stories-requirements.md, synth-05-technical-stack.md, synth-06-ux-legal-business.md, synth-07-metrics-risk-impl.md) instead of TDD skill synthesis file names. These files exist in `.claude/skills/prd/`, not `.claude/skills/tdd/`. A developer following this plan would edit the wrong files. | Replace the 5 file names in the Addition 2 table with the correct TDD skill synthesis file names: synth-03-architecture.md, synth-04-data-api.md, synth-05-state-components.md, synth-06-error-security.md, synth-07-observability-testing.md. Map each to its appropriate PRD extraction section based on what TDD sections each file covers. |
| 2 | CRITICAL | S8 Phase 5, Addition 2, Note paragraph | The note states "synth-01, synth-02, synth-08, and synth-09 do not require PRD extraction — they cover executive summary, business context, customer journey, and maintenance sections." This is exactly backwards. synth-01, synth-02, synth-08, and synth-09 are precisely the files that ALREADY read PRD extraction, per Section 2.5 and verified code. The note's rationale is also wrong — synth-01/02 cover executive summary and technical requirements (not "business context and customer journey"), and synth-08/09 cover performance/migration and risks/ops. The "customer journey" description applies to PRD synth-08-journey-design-api.md, not TDD synth-08. | Replace the note with the factually correct statement: "Note: synth-01, synth-02, synth-08, and synth-09 already list PRD extraction as a source in the current Synthesis Mapping Table and do not require modification. Only synth-03 through synth-07 are missing PRD extraction as a source." |
| 3 | IMPORTANT | S9 Open Questions, OQ-1 | OQ-1 asks whether spec_type is read as a variable anywhere in sc:roadmap pipeline. This is answerable: Section 2.2 already tags this as [CODE-CONTRADICTED] and Section 9.2 already answers "No." Direct grep of sc-roadmap-protocol/ returns zero matches for spec_type. The question was stale — it duplicated a resolved finding. | Move OQ-1 to Section 9.2 with answer: "No — grep of entire sc-roadmap-protocol/ returns zero matches. Consistent with S2.2 [CODE-CONTRADICTED] finding and existing S9.2 entry." APPLIED. |
| 4 | IMPORTANT | S9 Open Questions, OQ-7 | OQ-7 asks whether the domain_spread normalization denominator needs updating from 5 to 7. scoring.md line 17 confirms current value is `min(domains / 5, 1.0)`. The answer is yes, it needs updating. The implementation plan Phase 2 Step 1 already includes this change. The question was resolved by the plan itself. | Move OQ-7 to Section 9.2 with answer: "Yes — denominator is 5 per scoring.md line 17; must update to 7 when two domains added; Phase 2 Step 1 already specifies this change." APPLIED. |
| 5 | IMPORTANT | S9 Open Questions, OQ-5 and OQ-10 | OQ-5 (does rf-prd-extractor exist?) and OQ-10 (is PRD_REF auto-populated?) are answerable from direct code verification. OQ-5: `.claude/agents/` listing confirms no prd-extractor file exists (35 agent files, none matching). OQ-10: PRD SKILL.md line 491 confirms invocation offers to run tdd skill "with the PRD as input" but does not auto-set PRD_REF explicitly. | Move OQ-5 and OQ-10 to Section 9.2 with verified answers. APPLIED. |
| 6 | IMPORTANT | S8 Phase 5, Addition 2, source mappings | The source section mappings in the corrected Phase 5 Addition 2 table needed re-derivation from TDD synthesis file section ownership (not PRD skill section ownership). synth-04-data-api.md covers Data Models/API Specs — not epics/user stories. All 5 PRD extraction source mappings were wrong in the original. | Re-derived and applied as part of Fix 1 above. |

---

## Actions Taken

All fixes applied in-place with Edit tool. Verification performed by reading back affected sections.

### Fix 1: Phase 5, Addition 2 — Synthesis file names and source mappings corrected

Replaced 5 incorrect PRD skill synthesis file names (synth-03-competitive-scope.md, synth-04-stories-requirements.md, synth-05-technical-stack.md, synth-06-ux-legal-business.md, synth-07-metrics-risk-impl.md) with the correct TDD skill synthesis file names (synth-03-architecture.md, synth-04-data-api.md, synth-05-state-components.md, synth-06-error-security.md, synth-07-observability-testing.md). Re-derived all 5 PRD extraction source section mappings from the TDD synthesis file section ownership table in TDD SKILL.md lines 1074-1082. Added correction notice to the document.

- Verified: Addition 2 table now references files that exist in `.claude/skills/tdd/` context.

### Fix 2: Phase 5, Addition 2 — Inverted note corrected

Replaced the note claiming "synth-01, synth-02, synth-08, and synth-09 do not require PRD extraction" with the accurate statement that these four files already have PRD extraction as a source (confirmed per TDD SKILL.md lines 1074-1082) and only synth-03 through synth-07 need it added.

- Verified: Note now correctly identifies the 5 files requiring change and the 4 files that already have PRD extraction.

### Fix 3: Open Questions OQ-1, OQ-5, OQ-7, OQ-10 moved to Section 9.2

Removed OQ-1 (spec_type), OQ-5 (rf-prd-extractor existence), OQ-7 (domain_spread denominator), and OQ-10 (PRD_REF auto-population) from Section 9.1 Open Questions table. Added all four to Section 9.2 with verified answers based on direct code verification performed during this review.

- OQ-1: grep of sc-roadmap-protocol/ confirms zero matches for spec_type as variable.
- OQ-5: ls of .claude/agents/ confirms no rf-prd-extractor file exists.
- OQ-7: scoring.md line 17 confirms `min(domains / 5, 1.0)`; denominator update to 7 required; already in Phase 2 Step 1.
- OQ-10: PRD SKILL.md line 491 confirms PRD_REF is not auto-populated in Phase 7 invocation.
- Verified: Section 9.2 table now contains 10 definitively-answered questions (was 7).

---

## Recommendations

- Before any developer begins Phase 5 implementation, re-read the corrected Addition 2 table and verify the synthesis file names match the actual files in `.claude/skills/tdd/` by running: `ls .claude/skills/tdd/` and confirming synth-03-architecture.md through synth-07-observability-testing.md exist at the expected paths.
- OQ-2, OQ-3, OQ-4, OQ-6, OQ-8, OQ-9, OQ-11, OQ-12, OQ-13, OQ-14, OQ-15 remain genuinely unresolved and require decision before implementation of their respective phases. (OQ-1, OQ-5, OQ-7, OQ-10 resolved by this review and moved to Section 9.2.)
- The scoring formula weights in the 7-factor TDD formula (Phase 2 Step 2) have been verified to sum to 1.00 and are correct. No action needed.

---

## QA Complete
