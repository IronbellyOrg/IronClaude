# Canonical Reference Summary — tech-research/SKILL.md
**Status:** Complete
**Date:** 2026-04-30
**Source:** /config/workspace/IronClaude/.claude/skills/tech-research/SKILL.md (1322 lines)
---

## Pass 1 — Sections discovered in lines 1-700

- **S1 Frontmatter+Title** — lines 1-6 (frontmatter: 1-4; H1 title: 6). Description text is domain-specific (technical investigation triggers).
- **S2 Overview+How-it-works** — lines 7-12. Brief overview paragraph + "How it works" + gap-filling paragraph. Domain-specific framing.
- **S3 Why This Process Works** — lines 14-29. Explains MDTM benefits + multi-phase failure-mode prevention. Largely COPY-able boilerplate; references domain-specific phase names.
- **S4 Variable Reference** — lines 31-43. TASK_ID/TASK_DIR/RESEARCH/SYNTHESIS/QA/REVIEWS paths. SUBSTITUTE (paths use TASK-RESEARCH prefix).
- **S5 Input** — lines 45-58. Four-piece input model (WHAT/WHY/WHERE/OUTPUT_TYPE).
- **S6 Effective Prompt Examples** — lines 59-75. Four examples (strong/strong/strong/weak/weak). Domain-specific.
- **S7 What to Do If Prompt Incomplete** — lines 76-87. Clarification template with 4 questions.
- **S8 Depth Tiers** — lines 89-106. Quick/Standard/Deep table + selection rules.
- **S9 Output Locations** — lines 108-132. Artifact-to-location table + numbering convention.
- **S10 Execution Overview** — lines 134-153. Stage A / Stage B summary.
- **S11 Stage A header** — line 155 (just `## Stage A: Scope Discovery & Task File Creation`).
- **S12 A.1 Check for Existing Task File** — lines 157-170.
- **S13 A.2 Parse & Triage** — lines 172-192.
- **S14 A.3 Perform Scope Discovery** — lines 194-229. Includes research assignment types table.
- **S15 A.4 Write Research Notes File** — lines 231-271. 6-category template.
- **S16 A.5 Review Research Sufficiency** — lines 273-294.
- **S17 A.6 Template Triage** — lines 296-312.
- **S18 A.7 Build the Task File** — lines 314-448. Massive BUILD_REQUEST template with embedded Phase definitions.
- **S18b A.8 Receive & Verify** — lines 450-461 (sub-step of Stage A).
- **S19 Stage B Task File Execution** — lines 463-553. Execution Loop F1, Prohibited Actions F2, Parallel Spawning, F4, F5, Error Handling, Session Resumption.
- **S20 Agent Prompt Templates** — starts line 555. Codebase Research Agent Prompt (560-649), Web Research Agent Prompt (651-688), Synthesis Agent Prompt starts at 690...

## Pass 2 — Sections discovered in lines 701-1322

- **S20 (cont.)** — Synthesis Agent Prompt continues 690-721; Research Analyst Agent Prompt (rf-analyst Completeness Verification) 723-761; Research QA Agent Prompt (rf-qa Research Gate) 763-806; Synthesis QA Agent Prompt (rf-qa Synthesis Gate) 808-850; Report Validation QA Agent Prompt (rf-qa Report Validation) 852-897; Assembly Agent Prompt (rf-assembler Report Assembly) 899-965. Full S20 span: lines 555-965.
- **S21 Output Structure / Report Structure** — lines 967-1143. The 10-section report scaffold (Problem, Current State, Target, Gap Analysis, External Findings, Options, Recommendation, Implementation Plan, Open Questions, Evidence Trail). Heavily domain-specific (research-report flavored).
- **S22 Synthesis Mapping Table** — lines 1145-1158. Standard synth-file-to-section mapping (synth-01 through synth-06).
- **S23 Synthesis Quality Review Checklist** — lines 1160-1178. The 9 analyst criteria + note about rf-qa adding 3 more.
- **S24 Assembly Process** — lines 1180-1194. The 4 assembly steps + cross-checks.
- **S25 Validation Checklist** — lines 1196-1215. 15 boxes covering report sections + content quality.
- **S26 Content Rules** — lines 1217-1241. Do/Don't table + general principles.
- **S27 Critical Rules** — lines 1243-1278. 15 numbered cross-phase rules.
- **S28 Session Management** — lines 1280-1298. Session start + session end protocols.
- **S29 Research Quality Signals** — lines 1300-1322. Strong/weak investigation signals + when to spawn additional agents.

## Verbatim protocol blocks (byte-copy boilerplate inside S20)

These nested blocks appear inside agent prompts and must be byte-copied even when surrounding S20 prompt is GENERATE'd:
- **Incremental File Writing Protocol** — appears in Codebase Research Agent (lines 570-590), Web Research Agent (lines 660-664), Synthesis Agent (lines 712-718), Assembly Agent (lines 912-925).
- **Documentation Staleness Protocol** — Codebase Research Agent lines 601-628.
- **ADVERSARIAL STANCE / "be adversarial"** — Research Analyst (line 760), Research QA (line 776), Report Validation QA (line 865 "you can and should fix").
- **VERDICTS (PASS/FAIL)** — Research Analyst (lines 755-757), Research QA (lines 800-802), Synthesis QA (lines 847-849).

---

## Unified 29-Section Summary Table

| S# | Section Name | Tech-research line range | Boilerplate vs domain | Notes |
|----|--------------|--------------------------|-----------------------|-------|
| S1 | Frontmatter + Title | 1-6 | GENERATE | YAML name/description must be authored from new skill spec; H1 title is domain. |
| S2 | Overview + How-it-works | 7-12 | GENERATE | Two paragraphs of domain framing + gap-fill statement. Structure is consistent across RF skills but content is fully domain-specific. |
| S3 | Why This Process Works | 14-29 | SUBSTITUTE | MDTM 3 guarantees + multi-phase failure-mode list are largely COPY; phase-name list ("scope discovery → ... → qualitative review") needs substitution to match new skill's phases. |
| S4 | Variable Reference | 31-43 | SUBSTITUTE | Boilerplate paths block; replace TASK_ID prefix `TASK-RESEARCH-` with new skill's prefix. Subfolder set (research/synthesis/qa/reviews) may shrink for simpler skills. |
| S5 | Input | 45-58 | GENERATE | Four-piece input model is reusable shape, but the four bullets (WHAT/WHY/WHERE/OUTPUT_TYPE) are domain-specific to research. |
| S6 | Effective Prompt Examples | 59-75 | GENERATE | Strong/weak examples are inherently domain-specific; pattern (3 strong + 2 weak) is reusable shape. |
| S7 | What to Do If Prompt Incomplete | 76-87 | GENERATE | Clarification template + 4 questions are domain-specific; structure (blockquote + 4 numbered questions) is reusable. |
| S8 | Depth Tiers | 89-106 | SUBSTITUTE | Quick/Standard/Deep table is COPY-able shape with domain-specific row content (agent counts, when-to-use criteria). |
| S9 | Output Locations | 108-132 | SUBSTITUTE | Artifact-to-location table is structurally COPY; rows must enumerate the new skill's actual artifacts. |
| S10 | Execution Overview | 134-153 | COPY | Stage A / Stage B summary text is generic across RF skills (with minor adjustment to enumerated A.1-A.7 step counts). |
| S11 | Stage A header | 155 | COPY | Single line `## Stage A: Scope Discovery & Task File Creation`. Pure boilerplate. |
| S12 | A.1 Check for Existing Task File | 157-170 | COPY | Pure resumption boilerplate; only TASK prefix substitutes. |
| S13 | A.2 Parse & Triage | 172-192 | SUBSTITUTE | GOAL/WHY/WHERE/OUTPUT_TYPE/TOPIC_SLUG schema is reusable; example sentences are domain-specific. |
| S14 | A.3 Perform Scope Discovery | 194-229 | SUBSTITUTE | Scope-discovery scaffold is COPY; the **research assignment types table** (Code Tracer, Doc Analyst, etc.) is domain-specific and must be regenerated for the new skill. |
| S15 | A.4 Write Research Notes File | 231-271 | SUBSTITUTE | The 6-category template (EXISTING_FILES, PATTERNS_AND_CONVENTIONS, SOLUTION_RESEARCH, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER) is the canonical RF shape; some category labels may need light tweaking for non-research skills. |
| S16 | A.5 Review Research Sufficiency | 273-294 | COPY | 6 review questions + max-2-rounds rule are generic. Item 6 (CODE-VERIFIED tags) is research-specific and may be removed for non-research skills. |
| S17 | A.6 Template Triage | 296-312 | COPY | Template 01 vs 02 selection rules are pure boilerplate; final sentence ("for tech-research, almost always Template 02") needs name substitution. |
| S18 | A.7 Build the Task File | 314-448 | GENERATE | Largest single section. The BUILD_REQUEST scaffold is reusable shape, but Phase 1-7 definitions inside it are heavily domain-specific. Verbatim pieces (ESCALATION block lines 371-379, MDTM template paths lines 437-439, granularity requirement lines 355-362) are COPY. |
| S19 | Stage B Task File Execution | 463-553 | COPY | Execution Loop (F1), Prohibited Actions (F2), Parallel Spawning, F4/F5, Error Handling, Session Resumption — all generic RF orchestration boilerplate. Includes A.8 Verify (lines 450-461) as Stage A trailing piece — actually before this section. |
| S20 | Agent Prompt Templates | 555-965 | GENERATE | All 7 prompts are domain-specific (Codebase Research, Web Research, Synthesis, rf-analyst Completeness, rf-qa Research-Gate, rf-qa Synthesis-Gate, rf-qa Report-Validation, rf-assembler). HOWEVER nested protocol blocks are byte-copy: Incremental File Writing Protocol (570-590, 660-664, 712-718, 912-925), Documentation Staleness Protocol (601-628), ADVERSARIAL STANCE phrasing, VERDICTS PASS/FAIL blocks. |
| S21 | Output Structure (Report Structure) | 967-1143 | GENERATE | Full 10-section report markdown scaffold; entirely domain-shaped to research reports. New skill must author its own document scaffold. |
| S22 | Synthesis Mapping Table | 1145-1158 | GENERATE | synth-01..synth-06 mapping is research-specific; structure (synth-file → report-sections → source-files) is reusable shape. |
| S23 | Synthesis Quality Review Checklist | 1160-1178 | GENERATE | 9 analyst criteria are research-specific (cite "Gap/Current/Target", "doc-only claims in Sections 2 and 8"). Pattern of 9 numbered checks is reusable. |
| S24 | Assembly Process | 1180-1194 | COPY | 4 assembly steps + cross-check list are generic RF assembly boilerplate (header, sections, ToC, consistency). The 4 cross-check bullets reference domain section numbers that need substitution. |
| S25 | Validation Checklist | 1196-1215 | GENERATE | 15 checkbox items are domain-specific to research-report contents; new skill must author its own validation list. |
| S26 | Content Rules | 1217-1241 | SUBSTITUTE | Do/Don't table format is COPY; rule rows are mostly generic (tables-over-prose, no full source dumps, evidence citations) with some research-specific rows (Gap analysis, Options analysis). |
| S27 | Critical Rules | 1243-1278 | SUBSTITUTE | 15 numbered rules: rules 1-3, 7-8, 10-13 are pure COPY boilerplate; rules 4-6, 9, 14-15 contain research-specific phrasing (codebase-as-source-of-truth, gap-driven web research, doc verification). |
| S28 | Session Management | 1280-1298 | COPY | Session start + session end protocols are pure RF boilerplate; only TASK prefix path substitutes. |
| S29 | Research Quality Signals | 1300-1322 | SUBSTITUTE | Strong/weak/when-to-spawn 3-block structure is reusable shape; bullet content is domain-specific (file paths, data flow, gap specificity). |

---

**Status:** Complete


