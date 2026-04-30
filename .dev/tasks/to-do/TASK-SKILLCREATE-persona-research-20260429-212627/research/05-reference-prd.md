# Research: Reference Skill Analysis — prd
**Investigation type:** Reference Skill Analysis
**Scope:** /config/workspace/IronClaude/.claude/skills/prd/SKILL.md
**Status:** Complete
**Date:** 2026-04-29
**Source line count:** 454 lines
**Refs directory:** Present, 5 refs files (agent-prompts.md, build-request-template.md, operational-guidance.md, synthesis-mapping.md, validation-checklists.md)
---

## Source File Structure (Top-Level Headings)

The prd SKILL.md does NOT use explicit numbered "Section 1..29" headings. Instead, it uses descriptive H2/H3 headings organized into two stages (A and B). The mapping below maps each *observable* heading to the closest canonical section number from the standard 29-section template.

Top-level H2 headings observed (in order):
1. `# PRD Creator` (title, line 6)
2. `## Why This Process Works` (line 14)
3. `## Input` (line 33)
4. `## Tier Selection` (line 77)
5. `## Output Locations` (line 95)
6. `## Execution Overview` (line 135)
7. `## Stage A: Scope Discovery & Task File Creation` (line 166)
   - A.1 Check for Existing Task File (line 168)
   - A.2 Parse & Triage the PRD Request (line 182)
   - A.3 Perform Scope Discovery (line 214)
   - A.4 Write Research Notes File (line 263)
   - A.5 Review Research Sufficiency (line 307)
   - A.6 Template Triage (line 332)
   - A.7 Build the Task File (line 350)
   - A.8 Receive & Verify the Task File (line 388)
8. `## Stage B: Task File Execution` (line 404)
9. `## Phase Loading Contract (FR-PRD-R.6c)` (line 429)
10. `## Session Management` (line 451)

CRITICAL OBSERVATION: The prd SKILL.md is NOT structured as a 29-section canonical document. It is an **action-oriented procedural skill** organized as Stages → Steps → Phases. Many "canonical sections" from the assumed 29-section model do not appear as discrete sections. The mapping below classifies each canonical section as PRESENT, ABSENT, or EMBEDDED.

---

## Domain Variables Extracted

| Variable | Value | Evidence (line) |
|---|---|---|
| **Skill name** | `prd` (frontmatter line 2) | line 2 |
| **Skill title** | "PRD Creator" | line 6 |
| **TASK_ID_PREFIX** | `TASK-PRD-` | lines 97, 101, 112, 131, 173 |
| **Task ID format** | `TASK-PRD-YYYYMMDD-HHMMSS` | lines 97, 101, 112 |
| **Slug field name** | `PRODUCT_SLUG` | line 190 |
| **Slug examples** | `wizard-system`, `multi-agent-platform`, `pixel-streaming` | lines 97, 190 |
| **Output document type** | PRD (Product Requirements Document) | line 6, 8 |
| **Final output convention** | `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md` | lines 43, 126 |
| **Template schema location** | `src/superclaude/examples/prd_template.md` | lines 12, 127 |
| **Phase count** | 7 phases | lines 153–160 |
| **Phase names** | Preparation, Deep Investigation, Completeness Verification, Web Research, Synthesis + Analyst + QA Synthesis Gate, Assembly, Present to User & Complete Task | lines 154–160 |
| **QA gate phases** | Phase 3 (research gate), Phase 5 (synthesis gate), Phase 6 (assembly validation) | lines 156, 158, 159 |
| **QA agent roster** | `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-assembler`, `rf-task-builder`, `rf-task-researcher` | lines 27, 156, 158, 159, 261, 352 |
| **Research agent type roster** | Feature Analyst, Doc Analyst, Integration Mapper, UX Investigator, Architecture Analyst | lines 251–256 |
| **Tier names** | Lightweight, Standard, Heavyweight | line 83 |
| **Line ceiling (Heavyweight)** | 1,500–2,500 lines | line 85 |
| **Line ceiling (Standard)** | 800–1,500 lines | line 84 |
| **Line ceiling (Lightweight)** | 400–800 lines | line 83 |
| **Codebase agent count (LW/STD/HW)** | 2–3 / 4–6 / 6–10+ | lines 83–85 |
| **Web agent count (LW/STD/HW)** | 0–1 / 1–2 / 2–4 | lines 83–85 |
| **PRD scope classifier** | Product PRD vs Feature/Component PRD | line 191, 197–198 |
| **Document section count (template)** | 32 sections (referenced for Product PRD) | line 197 |
| **N/A sections for Feature PRD** | S5 (Business Context), S8 (Value Proposition), S9 (Competitive Analysis), S19 (Legal/Compliance), S20 (Business Requirements) | line 198 |
| **Refs files loaded by orchestrator** | `refs/build-request-template.md` | line 359 |
| **Refs files loaded by builder** | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` | lines 367–372 |
| **Subagent type for builder** | `rf-task-builder` (mode: bypassPermissions) | line 386 |
| **MDTM template number** | Template 02 (Complex Task) for PRD creation | line 348 |
| **File numbering convention** | Zero-padded sequential: `01-`, `02-`, `03-` | line 129 |
| **Validation contract identifier** | FR-PRD-R.6c, FR-PRD-R.6d | lines 429, 442 |
| **Failure modes addressed** | Context rot, Shallow coverage, Hallucinated requirements, Uncaught quality drift | lines 24–27 |

---

## 29-Section Canonical Mapping

NOTE: The 29-section canonical structure is INFERRED from the skill-creator skill's intent (the task description says "29 canonical sections"). The prd SKILL.md does not label its sections by canonical numbers. Below I map the most likely canonical section names to what is OBSERVED in the prd SKILL.md. Sections marked ABSENT do not appear as named sections in this file.

Classifications used:
- **COPY**: Section content is generic/boilerplate — copy verbatim or near-verbatim across skills
- **SUBSTITUTE**: Section content has a fixed shape but contains domain placeholders that must be substituted
- **GENERATE**: Section content is fully domain-specific — must be generated fresh per skill
- **ABSENT**: Section is not present in this skill file
- **EMBEDDED**: Section content is present but folded into another section, not standalone

### Section 1: Frontmatter (name + description)
- **Lines:** 1–4
- **Classification:** SUBSTITUTE
- **Domain variables:** `name: prd`, description string with trigger phrases ("create a PRD for...", "document the product requirements", etc.)
- **Boilerplate boundary:** Field structure is fixed (name + description); description content is fully domain-specific
- **Anomalies:** None

### Section 2: Title + One-Paragraph Description
- **Lines:** 6–10
- **Classification:** SUBSTITUTE
- **Domain variables:** "PRD Creator", "Product Requirements Documents (PRDs)", "products, features, and platform capabilities"
- **Boilerplate boundary:** The MDTM/persistence/spawning explanation (lines 8–10) is structurally identical across skills (tdd, prd, tech-research, tech-reference) — only the document-type noun changes
- **Anomalies:** None

### Section 3: Output Schema Reference
- **Lines:** 12
- **Classification:** SUBSTITUTE
- **Domain variables:** Template path `src/superclaude/examples/prd_template.md`
- **Boilerplate boundary:** "The output always follows the project template at [PATH]. The template is the schema — every [DOCTYPE] must conform to it." — boilerplate sentence with two substitutions
- **Anomalies:** None

### Section 4: Why This Process Works
- **Lines:** 14–29
- **Classification:** SUBSTITUTE
- **Domain variables:** Domain noun ("PRDs"), failure modes wording mostly stable, gate names ("rf-analyst completeness check", "rf-qa research gate", "rf-qa synthesis gate", "rf-qa final PRD validation")
- **Boilerplate boundary:** Three guarantees (lines 19–22) are pure boilerplate. Four failure modes (lines 24–27) are mostly boilerplate with domain-specific phrasing ("hallucinated requirements" is PRD-specific; would be "hallucinated designs" for TDD)
- **Anomalies:** None — this is a heavy boilerplate section

### Section 5: Input Section Header & Intro
- **Lines:** 33–35
- **Classification:** SUBSTITUTE
- **Domain variables:** Document type ("PRD")
- **Boilerplate boundary:** "The skill needs four pieces of information to produce a comprehensive [DOCTYPE]" — formula sentence
- **Anomalies:** None

### Section 6: Input Items (4 pieces)
- **Lines:** 37–43
- **Classification:** SUBSTITUTE
- **Domain variables:** WHAT/WHY/WHERE/OUTPUT items are domain-specific phrasing of generic concepts; PRD-specific WHY examples ("investor pitches, engineering planning, feature prioritization, stakeholder alignment")
- **Boilerplate boundary:** Four-item structure (WHAT, WHY, WHERE, OUTPUT) is stable across skills. Output path convention is domain-specific.
- **Anomalies:** None

### Section 7: Effective Prompt Examples
- **Lines:** 45–60
- **Classification:** GENERATE
- **Domain variables:** All examples are PRD-specific (GameFrame AI, wizard, canvas roadmap, pixel streaming)
- **Boilerplate boundary:** Strong/Weak categorization framework is boilerplate; examples are fully domain-specific
- **Anomalies:** None

### Section 8: What to Do If Prompt Is Incomplete
- **Lines:** 62–73
- **Classification:** SUBSTITUTE
- **Domain variables:** PRD-specific clarifying questions (scope/purpose/areas/output)
- **Boilerplate boundary:** Structure (4 numbered clarifying questions) is stable; specific questions are domain-specific
- **Anomalies:** None

### Section 9: Tier Selection
- **Lines:** 77–91
- **Classification:** SUBSTITUTE
- **Domain variables:** Tier naming (Lightweight/Standard/Heavyweight is stable across skills); thresholds ("<5 user stories", "5-20 user stories", "20+ user stories") are PRD-specific; line ceilings (400–800/800–1,500/1,500–2,500) likely domain-specific
- **Boilerplate boundary:** Tier table structure is boilerplate; row content is domain-specific
- **Anomalies:** None

### Section 10: Output Locations
- **Lines:** 95–131
- **Classification:** SUBSTITUTE
- **Domain variables:** TASK_ID_PREFIX (`TASK-PRD-`), final output path (`docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md`), template path, QA report names (research-gate, synthesis-gate, report-validation, qualitative-review)
- **Boilerplate boundary:** Variable reference block structure (TASK_ID/TASK_DIR/TASK_FILE/RESEARCH/SYNTHESIS/QA/REVIEWS) is boilerplate. Artifact location table is mostly boilerplate with domain-specific QA report naming
- **Anomalies:** None — this is highly structured and substitutable

### Section 11: Execution Overview
- **Lines:** 135–162
- **Classification:** SUBSTITUTE
- **Domain variables:** Phase names (7 phases for prd: Preparation, Deep Investigation, Completeness Verification, Web Research, Synthesis + Analyst + QA Synthesis Gate, Assembly, Present to User & Complete Task)
- **Boilerplate boundary:** Two-stage A/B structure is boilerplate (matches skill-creator ports). Stage A 8-step structure is boilerplate. Phase enumeration is domain-specific (phase count and names vary by skill)
- **Anomalies:** None

### Section 12: Stage A Header
- **Lines:** 166
- **Classification:** COPY
- **Anomalies:** None

### Section 13: A.1 Check for Existing Task File
- **Lines:** 168–180
- **Classification:** SUBSTITUTE
- **Domain variables:** TASK_ID_PREFIX (`TASK-PRD-*`), document type ("PRD")
- **Boilerplate boundary:** 6-step procedure is boilerplate; only the prefix glob differs
- **Anomalies:** None

### Section 14: A.2 Parse & Triage Request
- **Lines:** 182–212
- **Classification:** SUBSTITUTE
- **Domain variables:** Field names (GOAL, WHY, WHERE, OUTPUT_TYPE, PRODUCT_SLUG, PRD_SCOPE), PRD-specific scope classification (Product PRD vs Feature/Component PRD), template section impact table
- **Boilerplate boundary:** Triage A/B scenario distinction is boilerplate; PRD_SCOPE classification table is domain-specific (this is a PRD-only concept that does not appear in other skills)
- **Anomalies:** PRD_SCOPE table (lines 196–198) introduces the concept of marking sections N/A based on scope — this is unique to PRD because of the platform-vs-feature distinction. TDD/tech-reference do not have this binary

### Section 15: A.3 Perform Scope Discovery
- **Lines:** 214–261
- **Classification:** SUBSTITUTE
- **Domain variables:** Discovery topics (feature inventory, product areas, UX patterns, integration points, architecture), agent types (Feature Analyst, Doc Analyst, Integration Mapper, UX Investigator, Architecture Analyst)
- **Boilerplate boundary:** Discovery steps 1–6 structure is boilerplate. Research assignment type table is domain-specific (agent roster differs per skill)
- **Anomalies:** None

### Section 16: A.4 Write Research Notes File
- **Lines:** 263–305
- **Classification:** SUBSTITUTE
- **Domain variables:** Research notes template fields, "PRD Scope" frontmatter field, Feature PRD section list (S5, S8, S9, S17, S18 are referenced for N/A — note line 276 says "S5, S8, S9, S17, S18" but line 198 says "S5, S8, S9, S19, S20")
- **Boilerplate boundary:** 7-category structure (EXISTING_FILES, PATTERNS_AND_CONVENTIONS, FEATURE_ANALYSIS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER) is mostly boilerplate; FEATURE_ANALYSIS is domain-specific (would be different name in TDD)
- **Anomalies:** **INCONSISTENCY DETECTED** — line 276 references "S5 (market sizing), S8 (value prop), S9 (competitive), S17 (full compliance), S18 (pricing/GTM)" while line 198 says "S5 (Business Context), S8 (Value Proposition), S9 (Competitive Analysis), S19 (Legal/Compliance), S20 (Business Requirements)". The section numbers differ (S17/S18 vs S19/S20) — this is an internal contradiction in the file [CODE-VERIFIED]

### Section 17: A.5 Review Research Sufficiency
- **Lines:** 307–330
- **Classification:** SUBSTITUTE
- **Domain variables:** Sufficiency criteria (8 questions), one PRD-specific question about "stakeholder segments and user personas"
- **Boilerplate boundary:** 8-question gate structure is boilerplate; question #7 (stakeholder/persona) is PRD-specific
- **Anomalies:** None

### Section 18: A.6 Template Triage
- **Lines:** 332–348
- **Classification:** COPY
- **Domain variables:** Document type name in concluding sentence ("For PRD creation, the answer is almost always Template 02")
- **Boilerplate boundary:** Template 01 vs 02 decision criteria is fully boilerplate; only the closing sentence references domain
- **Anomalies:** None

### Section 19: A.7 Build the Task File
- **Lines:** 350–386
- **Classification:** SUBSTITUTE
- **Domain variables:** Refs file names (build-request-template.md, agent-prompts.md, synthesis-mapping.md, validation-checklists.md, operational-guidance.md). Refs file count = 5
- **Boilerplate boundary:** Loading declaration structure is boilerplate; refs file enumeration is domain-specific (different skills may load different refs)
- **Anomalies:** None

### Section 20: A.8 Verify Task File
- **Lines:** 388–400
- **Classification:** SUBSTITUTE
- **Domain variables:** Phase numbers (2, 3, 4, 5, 6, 7), `rf-assembler` agent name, validation checklist refs path
- **Boilerplate boundary:** 7-bullet verification list is mostly boilerplate; phase numbers and agent names are domain-specific
- **Anomalies:** None

### Section 21: Stage B Header
- **Lines:** 404
- **Classification:** COPY
- **Anomalies:** None

### Section 22: Stage B Delegation Protocol
- **Lines:** 406–413
- **Classification:** SUBSTITUTE
- **Domain variables:** Example task file path (`TASK-PRD-20260309-120000`), QA item names (rf-analyst completeness-verification, rf-qa research-gate, synthesis-gate, report-validation, rf-qa-qualitative prd-qualitative)
- **Boilerplate boundary:** 4-step delegation structure is fully boilerplate; QA item names domain-specific
- **Anomalies:** None

### Section 23: What the Task File Must Contain
- **Lines:** 416–424
- **Classification:** COPY
- **Domain variables:** Document type ("product capabilities", "research agents READ code") references
- **Boilerplate boundary:** This section is nearly verbatim across PRD/TDD/tech-research; only domain noun substitutions
- **Anomalies:** None

### Section 24: Phase Loading Contract
- **Lines:** 429–447
- **Classification:** SUBSTITUTE
- **Domain variables:** Contract identifiers `FR-PRD-R.6c`, `FR-PRD-R.6d` (would change to FR-TDD-R.6c, etc.), refs file list
- **Boilerplate boundary:** Table structure and validation rules are boilerplate; identifiers and refs file enumeration are domain-specific
- **Anomalies:** None

### Section 25: Session Management
- **Lines:** 451–453
- **Classification:** COPY
- **Domain variables:** "PRD update protocol" → "[DOCTYPE] update protocol"
- **Boilerplate boundary:** Three-sentence boilerplate referring users to `refs/operational-guidance.md`
- **Anomalies:** None — extremely short section

### Sections 26–29: Sections Not Present in prd SKILL.md
- **Classification:** ABSENT
- **Notes:** The task prompt references "29 canonical sections" — but the prd SKILL.md observably contains approximately 25 distinct sections (counted above: frontmatter, title/intro, output schema ref, why-this-works, input header, input items, examples, prompt-incomplete, tier, output-locations, exec-overview, stage-A header, A.1–A.8 (8 subsections), stage-B header, delegation, task-file-must-contain, phase-loading-contract, session-management). Canonical sections that may be expected but ABSENT:
  - **Persona/Agent Profile section** — ABSENT (no top-level persona definition; agent identities are defined inside refs/agent-prompts.md)
  - **Skill Activation Triggers** — EMBEDDED in frontmatter description (line 3), not a standalone section
  - **Examples Gallery / Use Cases** — EMBEDDED in Section 7 (Effective Prompt Examples)
  - **Anti-Patterns / What NOT to Do** — EMBEDDED in Section 23 (line 424 lists prohibited actions inline)
  - **Validation Rules / Quality Bar** — partially in A.5 and A.8, partially deferred to refs/validation-checklists.md
  - **Companion Documents / Related Skills** — ABSENT in main file (referenced via /task delegation)
  - **Versioning / Change Log** — ABSENT
  - **Glossary** — ABSENT

## Summary Table — 29-Section Mapping

| # | Canonical Section | Lines | Classification |
|---|---|---|---|
| 1 | Frontmatter (name + description) | 1–4 | SUBSTITUTE |
| 2 | Title + Description | 6–10 | SUBSTITUTE |
| 3 | Output Schema Reference | 12 | SUBSTITUTE |
| 4 | Why This Process Works | 14–29 | SUBSTITUTE |
| 5 | Input Header | 33–35 | SUBSTITUTE |
| 6 | Input Items (4 pieces) | 37–43 | SUBSTITUTE |
| 7 | Effective Prompt Examples | 45–60 | GENERATE |
| 8 | What to Do If Prompt Incomplete | 62–73 | SUBSTITUTE |
| 9 | Tier Selection | 77–91 | SUBSTITUTE |
| 10 | Output Locations | 95–131 | SUBSTITUTE |
| 11 | Execution Overview | 135–162 | SUBSTITUTE |
| 12 | Stage A Header | 166 | COPY |
| 13 | A.1 Check Existing Task File | 168–180 | SUBSTITUTE |
| 14 | A.2 Parse & Triage | 182–212 | SUBSTITUTE |
| 15 | A.3 Scope Discovery | 214–261 | SUBSTITUTE |
| 16 | A.4 Write Research Notes | 263–305 | SUBSTITUTE |
| 17 | A.5 Review Sufficiency | 307–330 | SUBSTITUTE |
| 18 | A.6 Template Triage | 332–348 | COPY |
| 19 | A.7 Build Task File | 350–386 | SUBSTITUTE |
| 20 | A.8 Verify Task File | 388–400 | SUBSTITUTE |
| 21 | Stage B Header | 404 | COPY |
| 22 | Stage B Delegation Protocol | 406–413 | SUBSTITUTE |
| 23 | What Task File Must Contain | 416–424 | COPY |
| 24 | Phase Loading Contract | 429–447 | SUBSTITUTE |
| 25 | Session Management | 451–453 | COPY |
| 26 | Persona/Agent Profile | — | ABSENT |
| 27 | Anti-Patterns Section | — | EMBEDDED in §23 |
| 28 | Companion Documents/Related | — | ABSENT |
| 29 | Versioning/Changelog | — | ABSENT |

Total observable distinct sections: **25** (including subsections of Stage A as discrete sections). Of these, **3 are COPY**, **18 are SUBSTITUTE**, **1 is GENERATE**, **3 are EMBEDDED elsewhere**, **3 are ABSENT** vs. an assumed 29.

---

## Substitution Points (Bracketed Placeholders Found)

Bracketed placeholders found in the source (these are values that would change per skill):
- `[PRODUCT]` (research notes template, line 270)
- `[today]` (research notes template, line 272)
- `[A or B]` (line 273)
- `[Lightweight / Standard / Heavyweight]` (line 274)
- `[Product PRD / Feature PRD]` (line 275)
- `[feature-name]` (output path placeholder, line 43, 126)
- `[FEATURE-NAME]` (output path placeholder, line 43, 126)
- `[NN]` (file numbering placeholder, lines 114–116)
- `[topic-name]`, `[topic]`, `[gate]` (file naming placeholders, lines 114–119)
- `[Planned output files...]`, `[Planned investigation breakdown...]`, etc. (research notes block content placeholders, lines 281–304)

For skill-creator ports, these become substitution targets:
- DOCTYPE: PRD → TDD / TechRef / Research / etc.
- TASK_ID_PREFIX: `TASK-PRD-` → `TASK-TDD-` / `TASK-TECHREF-` / etc.
- SLUG_FIELD: `PRODUCT_SLUG` → `COMPONENT_SLUG` / `FEATURE_SLUG` / etc.
- OUTPUT_PATH_TEMPLATE: `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md` → varies per doctype
- TEMPLATE_PATH: `src/superclaude/examples/prd_template.md` → varies per doctype
- CONTRACT_PREFIX: `FR-PRD-R.6c/d` → `FR-TDD-R.6c/d` / etc.
- AGENT_ROSTER: Feature Analyst, Doc Analyst, Integration Mapper, UX Investigator, Architecture Analyst → varies per doctype
- PHASE_NAMES (7 phases) → may differ per doctype
- LINE_CEILINGS per tier → likely doctype-specific

---

## Phase Structure Detail

| Phase # | Name | Activities | QA Gate Placement |
|---|---|---|---|
| 1 | Preparation | Scope confirmation, template read, tier selection | None |
| 2 | Deep Investigation | Parallel subagent investigation of code/capabilities | None |
| 3 | Completeness Verification | rf-analyst completeness check + rf-qa research gate (parallel) | **GATE 1** (research gate) |
| 4 | Web Research | Optional external research | None |
| 5 | Synthesis + Analyst + QA Synthesis Gate | Template-aligned synthesis, rf-analyst review, rf-qa synthesis gate (parallel) | **GATE 2** (synthesis gate) |
| 6 | Assembly | rf-assembler produces final doc, rf-qa structural validation, rf-qa-qualitative review | **GATE 3** (assembly + qualitative validation) |
| 7 | Present to User & Complete Task | Deliver, present artifacts, offer companion creation | None |

L-level mappings: NOT EXPLICITLY PRESENT in the SKILL.md. The phase structure does not use L1/L2/L3 etc. tiering language — only Lightweight/Standard/Heavyweight tier selection at the skill level (Section 9), which scales agent counts (lines 83–85) but does not relabel phase numbers.

---

## Boilerplate Boundaries Summary

**Pure boilerplate sections (would copy verbatim with minimal substitution):**
- Section 12 (Stage A header), Section 18 (A.6 Template Triage), Section 21 (Stage B header), Section 23 (What Task File Must Contain), Section 25 (Session Management)
- Three-guarantees block in Section 4 (lines 19–22)
- Variable reference block in Section 10 (lines 100–108)

**High-substitution sections (structure stable, content domain-specific):**
- Sections 5, 6, 8, 9, 14, 15, 16, 17, 19, 20, 22, 24

**Pure-domain sections (must regenerate per skill):**
- Section 7 (Effective Prompt Examples)

---

## Agent Prompt Templates

**Observation:** Agent prompt templates are NOT embedded in SKILL.md — they live in `refs/agent-prompts.md` and are loaded by the rf-task-builder at Stage A.7 (lines 365–376). The SKILL.md only references them by file path.

This means the skill-creator porting tool, when generating new skills, must:
1. Generate the SKILL.md skeleton
2. Generate the corresponding `refs/agent-prompts.md` (or equivalent) with domain-specific agent prompts

The skill agent roster declared in SKILL.md Section 15 (Feature Analyst, Doc Analyst, Integration Mapper, UX Investigator, Architecture Analyst — lines 251–256) acts as a contract that refs/agent-prompts.md must fulfill.

---

## Deviations from Skill Template (Anomalies)

1. **Internal contradiction in N/A section list:** Line 198 vs line 276 disagree on which template sections become N/A for Feature PRDs:
   - Line 198: "Sections S5 (Business Context), S8 (Value Proposition), S9 (Competitive Analysis), S19 (Legal/Compliance), S20 (Business Requirements) are typically N/A or abbreviated"
   - Line 276 (research notes template comment): "Sections S5 (market sizing), S8 (value prop), S9 (competitive), S17 (full compliance), S18 (pricing/GTM) are N/A or abbreviated"
   - **S17/S18 vs S19/S20** — likely a documentation error introduced when the prd_template.md was renumbered; one of the two references is stale [CODE-CONTRADICTED — internally]

2. **Section count claim:** Line 197 states "All 32 sections applicable" for Product PRD — implying the prd_template.md has 32 sections. This contradicts the skill-creator's "29 canonical sections" framing referenced in this task. Note: SKILL.md and prd_template.md may have different section counts — SKILL.md describes the skill's sections (~25), while prd_template.md describes the document output's sections (32). [UNVERIFIED — prd_template.md not read]

3. **No L-level mapping:** The skill does not use L1/L2/L3 phase labels. Phases are flat-numbered 1–7. Tier selection (LW/Std/HW) operates orthogonally on agent counts, not phase numbers.

4. **Two QA agent variants:** The skill uses both `rf-qa` (structural/template conformance) and `rf-qa-qualitative` (content quality) — at Phase 6 specifically, both fire. This is a deviation from skills that use a single rf-qa.

5. **PRD_SCOPE binary classifier:** The Product-PRD-vs-Feature-PRD scope classifier (lines 191–200) is unique to PRD. TDD does not have this binary; tech-reference likely does not either. This is a domain-specific extension that complicates direct porting.

6. **Section ordering note:** The Phase Loading Contract (lines 429–447) sits AFTER Stage B but BEFORE Session Management. This is acceptable but worth noting — it's a "validation contract" appended near end-of-file rather than embedded inline with Stage A.7 where loading happens.

7. **Build/Loading declarations use "block" markers:** Lines 357–361, 367–372, and 376–382 use a distinctive `> **Loaded at runtime from**` blockquote marker for runtime-load declarations. This is a structural convention worth preserving in ported skills.

---

## Stale Documentation Found

**Internal contradiction (must be flagged):**
- Lines 198 and 276 disagree on which template sections become N/A for Feature PRDs (S19/S20 vs S17/S18). This is an inconsistency within the SKILL.md itself. [CODE-CONTRADICTED — verified by reading both lines in source]

**No external stale doc claims:** The SKILL.md primarily refers to its own refs/ directory and to `src/superclaude/examples/prd_template.md`. The 5 refs files in `/config/workspace/IronClaude/.claude/skills/prd/refs/` were verified to exist (ls output shows agent-prompts.md, build-request-template.md, operational-guidance.md, synthesis-mapping.md, validation-checklists.md). [CODE-VERIFIED via ls]

**Unverified claims:**
- `src/superclaude/examples/prd_template.md` existence — not verified (out of scope of this research). [UNVERIFIED]
- `prd_template.md` having 32 sections — not verified. [UNVERIFIED]
- The "29 canonical sections" framing in the task prompt — the skill itself does not reference 29 sections. [UNVERIFIED — task-prompt assumption]

---

## Gaps and Questions

1. **Canonical section count inconsistency:** The task prompt assumes 29 canonical sections, but the prd SKILL.md does not enumerate by canonical numbers. The actual file contains ~25 observable distinct sections (with 3 absent and 3 embedded relative to the assumed 29). The skill-creator skill's notion of "29 canonical sections" must be defined elsewhere — likely in skill-creator's own template or refs. [UNVERIFIED]

2. **Internal S17/S18 vs S19/S20 contradiction (lines 198 vs 276):** Which is correct? Likely the prd_template.md should be read to determine the authoritative section numbering for "Legal/Compliance" and "Business Requirements". [CODE-CONTRADICTED — needs reconciliation]

3. **Template reference unread:** `src/superclaude/examples/prd_template.md` was not opened during this research. The "32 sections" claim and the section-name-to-number mapping cannot be verified without reading it. [UNVERIFIED]

4. **Refs file content unread:** The 5 refs files (agent-prompts.md, build-request-template.md, operational-guidance.md, synthesis-mapping.md, validation-checklists.md) were confirmed to exist via `ls` but their content was not read during this research. Agent prompt templates, full BUILD_REQUEST structure, and validation checklists therefore could not be cross-validated. [UNVERIFIED]

5. **L-level mappings:** The task prompt asks about "L-level mappings" — these are not present in this SKILL.md. The skill uses 7 flat-numbered phases plus a Lightweight/Standard/Heavyweight tier selector. No L1/L2/L3 nomenclature is used. [CODE-VERIFIED ABSENT]

6. **Document section count for Feature PRD:** Line 198 says S5/S8/S9/S19/S20 become N/A. If the template has 32 sections, that leaves 27 active sections for a Feature PRD — but this is not stated explicitly. [UNVERIFIED inference]

7. **Phase 7 scope ambiguity:** Phase 7 ("Present to User & Complete Task") is described as "Deliver document, present artifacts, offer companion document creation" (line 160). What "companion document creation" means is not defined in SKILL.md — possibly references TDD generation from PRD or similar. [UNVERIFIED]

---

## Final Summary

**Source file analyzed:** `/config/workspace/IronClaude/.claude/skills/prd/SKILL.md` (454 lines)

**Key findings:**
- prd is an **action-oriented procedural skill** organized into 2 stages, 8 sub-steps in Stage A, 4 sub-steps in Stage B, and 7 execution phases — NOT a flat 29-section document
- **TASK_ID_PREFIX:** `TASK-PRD-`
- **Slug field:** `PRODUCT_SLUG` (kebab-case, 2-3 words preferred)
- **Final output convention:** `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md`
- **Template path:** `src/superclaude/examples/prd_template.md`
- **Phase count:** 7 phases with QA gates at Phases 3, 5, and 6
- **QA agent roster:** rf-analyst, rf-qa, rf-qa-qualitative, rf-assembler, rf-task-builder, rf-task-researcher
- **Research agent roster (5 types):** Feature Analyst, Doc Analyst, Integration Mapper, UX Investigator, Architecture Analyst
- **Tier line ceilings:** LW 400–800 / Std 800–1,500 / HW 1,500–2,500
- **Refs files:** 5 (build-request-template, agent-prompts, synthesis-mapping, validation-checklists, operational-guidance)
- **Domain-unique feature:** PRD_SCOPE binary classifier (Product PRD vs Feature/Component PRD) with section-N/A logic — not present in TDD/tech-ref
- **Phase Loading Contract:** Strict declared/forbidden refs loading per phase, identifiers FR-PRD-R.6c and FR-PRD-R.6d

**Classification rollup (25 observable sections):**
- COPY: 5 sections (~20%)
- SUBSTITUTE: 18 sections (~72%)
- GENERATE: 1 section (~4%)
- EMBEDDED: 3 (anti-patterns, triggers, examples folded into other sections)
- ABSENT (vs assumed 29): persona, companion docs, versioning, etc.

---

## Appendix — Canonical RF 29-Section Cross-Mapping (added per Phase 3 cycle 1 finding C-5)

The earlier 29-Section Canonical Mapping above was structured around prd's *observable* section flow. The mapping below realigns to the **canonical RF 29-section schema as defined in research-notes.md REFERENCE_SKILL_ANALYSIS table (lines 178-209)**, which is what skill-creator and the persona-research output SKILL.md must conform to. Each canonical RF section gets an explicit PRESENT / ABSENT / EMBEDDED marker against the prd source.

| Canonical # | Canonical Name (per research-notes) | Marker | Evidence in prd SKILL.md |
|---|---|---|---|
| S1 | Frontmatter + Title | PRESENT | Lines 1-6 (frontmatter 1-4 + H1 title line 6) |
| S2 | Overview + How it works | EMBEDDED | Folded into "Why This Process Works" header (lines 14-29). No standalone "How it works" subsection. |
| S3 | Why This Process Works | PRESENT | Lines 14-29 — explicit H2 |
| S4 | Variable Reference | ABSENT | No standalone variable-reference table; placeholders documented inline in A.3 / A.4 templates |
| S5 | Input | PRESENT | Lines 33-43 — H2 "Input" |
| S6 | Effective Prompt Examples | PRESENT | Lines 45-60 |
| S7 | Incomplete Prompt | PRESENT | Lines 62-73 — "What to Do If Prompt Is Incomplete" |
| S8 | Depth Tiers | PRESENT | Lines 77-91 — "Tier Selection" |
| S9 | Output Locations | PRESENT | Lines 95-131 |
| S10 | Execution Overview | PRESENT | Lines 135-162 |
| S11 | Stage A header | PRESENT | Line 166 |
| S12 | A.1 Check existing task file | PRESENT | Lines 168-180 |
| S13 | A.2 Parse & Triage | PRESENT | Lines 182-212 |
| S14 | A.3 Scope Discovery | PRESENT | Lines 214-261 |
| S15 | A.4 Write Research Notes | PRESENT | Lines 263-305 |
| S16 | A.5 Review Sufficiency | PRESENT | Lines 307-330 |
| S17 | A.6 Template Triage | PRESENT | Lines 332-348 |
| S18 | A.7 Build the Task File | PRESENT | Lines 350-386 |
| S19 | Stage B: Delegation | PRESENT | Lines 404-413 (header line 404 + delegation block) |
| S20 | Agent Prompt Templates | EMBEDDED | NOT in main SKILL.md as a standalone section. Agent prompts live in `refs/agent-prompts.md` (referenced via Phase Loading Contract line 437). |
| S21 | Output Structure | EMBEDDED | Folded into Output Locations (S9). No separate per-doctype output schema in main file. |
| S22 | Synthesis Mapping Table | EMBEDDED | Reference to `refs/synthesis-mapping.md` per Phase Loading Contract; not in main SKILL.md as a section. |
| S23 | Synthesis Quality Review Checklist | EMBEDDED | Reference to `refs/validation-checklists.md` per Phase Loading Contract; not as standalone main-file section. |
| S24 | Assembly Process | EMBEDDED | A.7 / Phase 6 description (lines 350-386, 156) describes assembly procedurally; no discrete "Assembly Process" header. |
| S25 | Validation Checklist | EMBEDDED | Reference to `refs/validation-checklists.md`; A.5 / A.8 describe the verification gates inline. |
| S26 | Content Rules | ABSENT | No discrete content-rules section. Only inline anti-patterns embedded in §S18 (line 424). |
| S27 | Critical Rules | ABSENT | No standalone Critical Rules section. The skill relies on inline rule statements throughout. |
| S28 | Session Management | PRESENT | Lines 451-453 — H2 "Session Management" |
| S29 | Research Quality Signals | ABSENT | No standalone quality-signals section. |

**Roll-up vs canonical 29:** PRESENT 18 / EMBEDDED 7 / ABSENT 4.
**Implication for sc-persona-research-protocol generation:** The 7 EMBEDDED-in-refs sections (S2, S20, S21, S22, S23, S24, S25 in prd) and the 4 ABSENT canonical sections (S4, S26, S27, S29) require GENERATE classification rather than borrowed structure when the persona-research SKILL.md is assembled in Phase 4.

**Critical anomalies for skill-creator porting:**
1. Internal contradiction lines 198 vs 276 on Feature PRD N/A section numbers (S19/S20 vs S17/S18)
2. Two-variant QA agents (rf-qa + rf-qa-qualitative) at Phase 6
3. PRD-unique scope classifier requires per-doctype customization
4. Loading-declaration blockquotes (`> **Loaded at runtime from** ...`) are a structural convention to preserve

**Files referenced but not opened during this research:**
- `src/superclaude/examples/prd_template.md`
- `refs/agent-prompts.md`, `refs/build-request-template.md`, `refs/operational-guidance.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md` (existence verified, content not read)




