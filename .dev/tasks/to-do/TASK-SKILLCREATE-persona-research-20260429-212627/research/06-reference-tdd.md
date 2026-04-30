# Research: Reference Skill Analysis — tdd
**Investigation type:** Reference Skill Analysis
**Scope:** /config/workspace/IronClaude/.claude/skills/tdd/SKILL.md
**Status:** Complete
**Date:** 2026-04-29
---

## CRITICAL FINDING: Modularized Structure (Not 29 Sections)

The TDD SKILL.md at `/config/workspace/IronClaude/.claude/skills/tdd/SKILL.md` is **422 lines total** and follows a **modularized architecture** that does NOT match the canonical 29-section monolithic skill template structure. It uses a **Phase Loading Contract** that offloads the bulk of content to 5 refs files.

**Refs files (loaded on demand, NOT in SKILL.md):**
- `refs/build-request-template.md` (16,254 bytes) — Loaded at Stage A.7 by orchestrator
- `refs/agent-prompts.md` (23,388 bytes) — Loaded at Stage A.7 by builder only
- `refs/synthesis-mapping.md` (7,058 bytes) — Loaded at Stage A.7 by builder only
- `refs/validation-checklists.md` (10,287 bytes) — Loaded at Stage A.7 by builder only
- `refs/operational-guidance.md` (8,361 bytes) — Loaded at Stage A.7 by builder only

**SKILL.md contains only:** frontmatter, intro, Why This Process Works, Input, Tier Selection, Output Locations, Execution Overview, Stage A (A.1–A.8), Stage B delegation, Phase Loading Contract.

**SKILL.md does NOT contain (offloaded to refs):**
- Agent prompt templates (in `refs/agent-prompts.md`)
- BUILD_REQUEST template (in `refs/build-request-template.md`)
- Synthesis mapping table (in `refs/synthesis-mapping.md`)
- Validation checklists (in `refs/validation-checklists.md`)
- Operational guidance, session management, PRD pipeline, error handling (in `refs/operational-guidance.md`)

This means the "29 canonical sections" from skill-creator's standard template do not all appear directly in this SKILL.md — many are in refs files. Classification below treats both presence-in-SKILL.md and presence-in-refs.

---

## Section-by-Section Analysis (Aligned to 29 Canonical Sections)

The 29 canonical sections come from the skill-creator standard template. For each, I document: Classification (COPY = boilerplate verbatim across skills / SUBSTITUTE = template with domain variable swaps / GENERATE = entirely domain-specific content), Location, Boundaries, Domain variables.

### Section 1: YAML Frontmatter (name + description)
- **Location:** SKILL.md lines 1–4
- **Classification:** SUBSTITUTE
- **Domain variables:** `name: tdd`; description trigger phrases include "create a TDD for...", "design the architecture for...", "populate this TDD", "TDD for the agent system", "turn this PRD into a TDD"
- **Boilerplate boundary:** Frontmatter format is COPY (YAML structure); name + description content is SUBSTITUTE
- **Anomalies:** Description is single-line quoted string (~715 chars); heavily trigger-phrase-rich

### Section 2: Title (H1)
- **Location:** SKILL.md line 6
- **Classification:** SUBSTITUTE
- **Domain variables:** "TDD Creator"
- **Boilerplate boundary:** "[Domain] Creator" pattern (e.g., "PRD Creator", "TDD Creator", "Tech Reference Creator")

### Section 3: Opening Paragraph / Mission Statement
- **Location:** SKILL.md lines 8–12
- **Classification:** SUBSTITUTE
- **Domain variables:** "Technical Design Documents (TDDs)", "components, services, and systems", template path `src/superclaude/examples/tdd_template.md`, mention of PRD-to-TDD feeding
- **Boilerplate boundary:** Generic phrasing about MDTM task system, F1 execution loop, parallel agents, phase-gate QA, session management is COPY-equivalent across RF doc skills. Specific artifact name + template path is SUBSTITUTE.
- **Notes:** References `rf-task-builder` subagent, `/task` skill — these are stable across RF doc skills

### Section 4: Why This Process Works
- **Location:** SKILL.md lines 14–29
- **Classification:** SUBSTITUTE (mostly COPY with domain swaps)
- **Domain variables:** "Technical design documents", "design", "engineering specifications" (vs. "product requirements" in PRD skill)
- **Boilerplate boundary:** Lines 18–22 (three guarantees: progress survives compression, no steps skipped, resumability) `[UNVERIFIED — cross-skill verbatim diff not performed in this pass; classification based on stylistic similarity to other RF doc skills, requires Phase 4 cross-skill comparison vs prd lines 18-22 and tech-research equivalent for confirmation]` are classified COPY across RF skills. Lines 23–28 (multi-phase structure list + four failure modes: context rot, shallow coverage, hallucinated details, uncaught quality drift) `[UNVERIFIED — same caveat]` are classified COPY-with-substitution; the phase list itself is GENERATE.
- **Phase list anchor:** "scope discovery → deep investigation → analyst verification → web research → synthesis → synthesis QA → assembly → report validation"

### Section 5: Input
- **Location:** SKILL.md lines 33–59
- **Classification:** SUBSTITUTE
- **Structure:** 4 numbered inputs (mandatory + 3 optional), then "What to Do If the Prompt Is Incomplete" sub-block
- **Domain variables:**
  - Input 1: "WHAT to design" — components/services/systems
  - Input 2: "PRD reference" (TDD-specific — feeds upstream document)
  - Input 3: "WHERE to look"
  - Input 4: "Output location" — `docs/[domain]/TDD_[COMPONENT-NAME].md`
- **Boilerplate boundary:** Format and 4-input pattern is COPY; specific input descriptions are SUBSTITUTE
- **Anomaly:** Input 2 (upstream document reference) is conditionally present — TDD has PRD as upstream; tech-reference and PRD likely differ

### Section 6: Tier Selection
- **Location:** SKILL.md lines 63–78
- **Classification:** SUBSTITUTE
- **Domain variables:**
  - Tier table columns: Tier name, When, Codebase Agents, Web Agents, Target Lines
  - Lightweight: 2–3 codebase, 0–1 web, 300–600 lines
  - Standard: 4–6 codebase, 1–2 web, 800–1,400 lines
  - Heavyweight: 6–10+ codebase, 2–4 web, 1,400–2,200 lines
- **Boilerplate boundary:** Three-tier structure (Lightweight/Standard/Heavyweight) is COPY across RF doc skills; agent counts and line targets are SUBSTITUTE

### Section 7: Output Locations
- **Location:** SKILL.md lines 81–113
- **Classification:** SUBSTITUTE
- **Domain variables:**
  - `TASK_ID_PREFIX: TASK-TDD-`
  - `COMPONENT_SLUG` (TDD-specific slug field name; PRD likely uses `PRODUCT_SLUG` or similar)
  - Final output: `docs/[domain]/TDD_[COMPONENT-NAME].md`
  - Template schema: `src/superclaude/examples/tdd_template.md`
  - PRD extraction artifact: `${TASK_DIR}research/00-prd-extraction.md` (TDD-specific upstream-doc extraction)
- **Boilerplate boundary:** Variable definitions block (TASK_ID, TASK_DIR, RESEARCH, SYNTHESIS, QA, REVIEWS) is COPY pattern across RF skills; values within are SUBSTITUTE
- **File numbering convention:** zero-padded `01-`, `02-`, etc. — COPY

### Section 8: Execution Overview
- **Location:** SKILL.md lines 116–145
- **Classification:** SUBSTITUTE
- **Domain variables:**
  - Stage A is 8 sub-steps (A.1–A.8)
  - Phase count: 7
  - Phase names: Preparation, Deep Investigation, Completeness Verification, Web Research, Synthesis + Analyst + QA Synthesis Gate, Assembly, Present to User & Complete Task
  - QA phases referenced: rf-analyst, rf-qa, rf-qa-qualitative, rf-assembler
- **Boilerplate boundary:** Two-stage structure (A=preparation, B=execution) is COPY; specific phase content is SUBSTITUTE
- **L-level mappings:** NOT explicitly present — phases are numbered 1–7 but no L-level (L0/L1/L2) tagging visible in SKILL.md proper

### Section 9: Stage A.1 — Check for Existing Task File
- **Location:** SKILL.md lines 149–161
- **Classification:** COPY (with TASK_ID_PREFIX substitution)
- **Domain variables:** `TASK-TDD-*/` glob pattern
- **Boilerplate boundary:** Logic flow (check task file → unchecked items → resume; check research-notes.md → status branches) is COPY across RF skills

### Section 10: Stage A.2 — Parse & Triage the Design Request
- **Location:** SKILL.md lines 163–184
- **Classification:** SUBSTITUTE
- **Domain variables:**
  - GOAL/WHY/WHERE/OUTPUT_TYPE/PRD_REF/COMPONENT_SLUG fields
  - Scenario A example uses `docs/docs-product/tech/agents/PRD_AGENT_SYSTEM.md` and `backend/app/agents/`
  - Scenario B example: "Create a TDD for the wizard"
- **Boilerplate boundary:** Scenario A vs B triage pattern is COPY; specific examples are SUBSTITUTE
- **Slug field name:** `COMPONENT_SLUG` (TDD-specific naming)

### Section 11: Stage A.3 — Perform Scope Discovery
- **Location:** SKILL.md lines 186–234
- **Classification:** SUBSTITUTE (heavily domain-flavored)
- **Domain variables:**
  - Stub pattern: `*_TDD.md` or `*-TDD.md`
  - 6 research assignment types: Architecture Analyst, Code Tracer, Data Model Analyst, API Surface Mapper, Integration Mapper, Doc Analyst
  - PRD extraction details: epics, user stories, acceptance criteria, technical requirements, technology stack, success metrics/KPIs, scope definition (in/out/deferred), performance/security/scalability requirements
  - Tier thresholds: Lightweight <5 files, Standard 5-20, Heavyweight 20+
- **Agent type roster (TDD-specific):** Architecture Analyst, Code Tracer, Data Model Analyst, API Surface Mapper, Integration Mapper, Doc Analyst (6 types)
- **Boilerplate boundary:** Discovery flow steps 1–6 are COPY pattern; agent type table is SUBSTITUTE

### Section 12: Stage A.4 — Write Research Notes File
- **Location:** SKILL.md lines 236–279
- **Classification:** SUBSTITUTE
- **Domain variables:** 8 mandatory categories: EXISTING_FILES, PATTERNS_AND_CONVENTIONS, PRD_CONTEXT (TDD-specific), SOLUTION_RESEARCH, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER
- **Boilerplate boundary:** 8-category structure is COPY pattern; PRD_CONTEXT is TDD-specific (replaces equivalent upstream-doc category in other skills)
- **Mandatory marker:** "(MANDATORY)" in heading

### Section 13: Stage A.5 — Review Research Sufficiency (MANDATORY GATE)
- **Location:** SKILL.md lines 281–304
- **Classification:** SUBSTITUTE
- **Domain variables:** 8 review questions; question 7 is PRD-specific
- **Boilerplate boundary:** Gate structure (review → sufficient/insufficient → 2-round max → don't proceed without notes) is COPY; review questions are SUBSTITUTE
- **Validation requirements:** Doc-sourced claims must be tagged `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]`

### Section 14: Stage A.6 — Template Triage
- **Location:** SKILL.md lines 306–322
- **Classification:** COPY
- **Domain variables:** "For TDD creation, the answer is almost always Template 02"
- **Boilerplate boundary:** Template 01 vs 02 selection criteria is COPY; final-line "for [domain] creation" is SUBSTITUTE

### Section 15: Stage A.7 — Build the Task File
- **Location:** SKILL.md lines 324–359
- **Classification:** SUBSTITUTE (heavy refs declarations)
- **Domain variables:** FR-TDD-R.6a/R.6b loading declarations; 4 builder load dependencies (agent-prompts, synthesis-mapping, validation-checklists, operational-guidance); 1 orchestrator load (build-request-template)
- **Anomaly:** Heavy reference to refs/ files with `> Loaded at runtime from` blockquote markers — this is the modularization mechanism specific to TDD skill (likely shared with PRD/tech-reference)
- **Boilerplate boundary:** Pattern of orchestrator-vs-builder loading declarations is COPY-pattern; specific refs file names are SUBSTITUTE

### Section 16: Stage A.8 — Receive & Verify Task File
- **Location:** SKILL.md lines 361–373
- **Classification:** COPY (with phase-number substitution)
- **Domain variables:** "Phases 2, 3, 4, and 5", references `rf-assembler`, `rf-task-builder`
- **Boilerplate boundary:** Verification checklist structure is COPY; phase numbers are SUBSTITUTE

### Section 17: Stage B — Task File Execution / Delegation Protocol
- **Location:** SKILL.md lines 377–397
- **Classification:** COPY
- **Domain variables:** Task path example uses `TASK-TDD-20260309-120000`
- **Boilerplate boundary:** `/task` delegation flow is COPY; only path example uses domain prefix
- **CRITICAL note:** "task does NOT read this SKILL.md during execution" — COPY across RF skills

### Section 18: Phase Loading Contract (FR-TDD-R.6c/R.6d)
- **Location:** SKILL.md lines 401–419
- **Classification:** SUBSTITUTE
- **Domain variables:** All FR-TDD-R.6* tags use TDD-specific FR prefix; refs file names are TDD-specific
- **Boilerplate boundary:** Contract table structure (Phase | Actor | Declared Loads | Forbidden Loads) is COPY-pattern; row content is SUBSTITUTE
- **Anomaly:** This section appears to be unique to modularized RF skills (TDD/PRD/tech-reference); not present in canonical 29-section monolithic skills

---

## Sections 19–29: NOT PRESENT in SKILL.md (Offloaded to refs/)

The following canonical sections are NOT in SKILL.md and live in refs files:

### Section 19: Agent Prompt Templates
- **Location:** `refs/agent-prompts.md` (23,388 bytes — largest refs file)
- **Classification:** SUBSTITUTE
- **Loaded by:** `rf-task-builder` only at Stage A.7
- **Per SKILL.md line 349:** Contains "Codebase research, web research, synthesis, analyst, QA, assembly, and PRD extraction agent prompt templates"

### Section 20: BUILD_REQUEST Template
- **Location:** `refs/build-request-template.md` (16,254 bytes)
- **Classification:** SUBSTITUTE
- **Loaded by:** Orchestrator at Stage A.7
- **Per SKILL.md line 336:** "Full BUILD_REQUEST template with field definitions, tier-specific parameters, and orchestrator fill-in instructions"

### Section 21: Synthesis Mapping Table
- **Location:** `refs/synthesis-mapping.md` (7,058 bytes)
- **Classification:** SUBSTITUTE
- **Loaded by:** Builder only
- **Per SKILL.md line 351:** "Output structure definition and research-to-template-section synthesis mapping table"

### Section 22: Validation Checklists
- **Location:** `refs/validation-checklists.md` (10,287 bytes)
- **Classification:** SUBSTITUTE
- **Loaded by:** Builder only
- **Per SKILL.md line 353:** "Assembly process steps, structural/content validation checklists, and non-negotiable content rules"

### Section 23: Operational Guidance
- **Location:** `refs/operational-guidance.md` (8,361 bytes)
- **Classification:** SUBSTITUTE
- **Loaded by:** Builder only
- **Per SKILL.md line 355:** "Critical execution rules, research quality signals, artifact location conventions, PRD-to-TDD pipeline, TDD update protocol, and session management guidance"

### Sections 24–29: Cannot Map Without refs/ Inspection
The remaining canonical sections (e.g., examples, error handling, anti-patterns, completion criteria, quality gates, etc., as defined by skill-creator) cannot be mapped to specific SKILL.md content because the skill is structurally compressed into Stage A workflow + Phase Loading Contract. Many canonical-section content domains live inside refs files. A literal 1-to-1 mapping of 29 canonical sections to the TDD SKILL.md is not possible — this is a deliberate architectural decision documented in the Phase Loading Contract.

---

## Domain Variable Extraction Summary

| Variable | Value |
|---|---|
| `TASK_ID_PREFIX` | `TASK-TDD-` |
| Slug field name | `COMPONENT_SLUG` (kebab-case) |
| Slug derivation source | Design scope (e.g., `agent-orchestration`, `wizard-state`, `pixel-streaming-infra`) |
| Output location pattern | `docs/[domain]/TDD_[COMPONENT-NAME].md` |
| Template schema path | `src/superclaude/examples/tdd_template.md` |
| Upstream doc reference | PRD (Product Requirements Document) — optional but strongly recommended |
| Upstream extraction artifact | `${TASK_DIR}research/00-prd-extraction.md` |
| Phase count | 7 |
| Phase names | Preparation; Deep Investigation; Completeness Verification; Web Research; Synthesis + Analyst + QA Synthesis Gate; Assembly; Present to User & Complete Task |
| QA phase name(s) | "Completeness Verification" (Phase 3); "Synthesis + Analyst + QA Synthesis Gate" (Phase 5); rf-qa structural + rf-qa-qualitative content review (Phase 6) |
| QA agent roster | `rf-analyst`, `rf-qa`, `rf-qa-qualitative` |
| Assembly agent | `rf-assembler` (NOT general-purpose Agent) |
| Builder agent | `rf-task-builder` |
| Researcher agent | `rf-task-researcher` (optional spawn at A.3) |
| Line ceiling (Lightweight) | 300–600 |
| Line ceiling (Standard) | 800–1,400 |
| Line ceiling (Heavyweight) | 1,400–2,200 |
| Codebase agent count (Light/Std/Heavy) | 2–3 / 4–6 / 6–10+ |
| Web agent count (Light/Std/Heavy) | 0–1 / 1–2 / 2–4 |
| Tier file thresholds | <5 files = Light; 5–20 = Standard; 20+ = Heavyweight |
| Validation tag system | `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, `[UNVERIFIED]` |
| Agent type roster (research) | Architecture Analyst, Code Tracer, Data Model Analyst, API Surface Mapper, Integration Mapper, Doc Analyst (6 types) |
| Stage A sub-step count | 8 (A.1–A.8) |
| Research-notes.md categories | 8 mandatory: EXISTING_FILES, PATTERNS_AND_CONVENTIONS, PRD_CONTEXT, SOLUTION_RESEARCH, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER |
| Refs file count | 5 |
| FR tag prefix | `FR-TDD-R.6` (Functional Requirement TDD Reference 6) |
| Default tier | Standard |
| MDTM template default | Template 02 (Complex Task) |

---

## Substitution Points (Bracketed Placeholders)

The SKILL.md uses the following placeholder/substitution conventions:

- `[domain]` — appears in `docs/[domain]/TDD_[COMPONENT-NAME].md` (line 46, 107)
- `[COMPONENT-NAME]` — appears in output path (line 46, 107)
- `[NN]` — zero-padded research file numbering (line 102–103)
- `[topic-name]` / `[topic]` — research file topic slug (lines 101, 102, 103)
- `[gate]` — analyst/QA report gate identifier (lines 105–106)
- `[today]` — date placeholder in research notes (line 246)
- `[A or B]` — scenario placeholder (line 247)
- `[Lightweight / Standard / Heavyweight]` — tier (line 248)
- `[COMPONENT]` — research notes title (line 244)
- `${TASK_ID}`, `${TASK_DIR}`, `${RESEARCH}`, `${SYNTHESIS}`, `${QA}`, `${REVIEWS}` — bash-style env var interpolation (lines 87–93, used throughout)

---

## Phase Structure Detail

| Phase # | Name | Activity | QA Gate? | Agents Involved |
|---|---|---|---|---|
| 1 | Preparation | Scope confirmation, template read, tier selection | No | (orchestrator) |
| 2 | Deep Investigation | Parallel subagent investigation of component code/architecture | No | Architecture Analyst, Code Tracer, Data Model Analyst, API Surface Mapper, Integration Mapper, Doc Analyst (subset by tier) |
| 3 | Completeness Verification | rf-analyst completeness verification + rf-qa research gate (parallel) | YES (research gate) | rf-analyst + rf-qa |
| 4 | Web Research | Optional external research for design patterns, framework docs, API references | No | Web research agents |
| 5 | Synthesis + Analyst + QA Synthesis Gate | Template-aligned synthesis, then rf-analyst synthesis review + rf-qa synthesis gate (parallel) | YES (synthesis gate) | Synthesis agents + rf-analyst + rf-qa |
| 6 | Assembly | rf-assembler produces final document, then rf-qa structural validation, then rf-qa-qualitative content review | YES (final gate) | rf-assembler + rf-qa + rf-qa-qualitative |
| 7 | Present to User & Complete Task | Deliver document, present artifacts, offer PRD-to-TDD traceability | No | (orchestrator) |

**No L-level (L0/L1/L2) tagging is visible** in SKILL.md — phases use plain numeric labels.

---

## Boilerplate Boundary Map (Where Shared Content Ends)

| Line range | Content type | Classification |
|---|---|---|
| 1–4 | YAML frontmatter | SUBSTITUTE (name + description domain-specific) |
| 6–12 | Title + opening | SUBSTITUTE |
| 14–29 | Why This Process Works | SUBSTITUTE (mostly COPY framing, domain swaps) |
| 33–59 | Input | SUBSTITUTE (4-input pattern is COPY) |
| 63–78 | Tier Selection | SUBSTITUTE (3-tier framework is COPY, numbers SUBSTITUTE) |
| 81–113 | Output Locations | SUBSTITUTE (variable defs pattern is COPY) |
| 116–145 | Execution Overview | SUBSTITUTE (Stage A/B framework is COPY) |
| 149–161 | A.1 Existing Task Check | COPY (mostly) |
| 163–184 | A.2 Parse & Triage | SUBSTITUTE (Scenario A/B pattern is COPY) |
| 186–234 | A.3 Scope Discovery | SUBSTITUTE (6-step flow is COPY-pattern, agent roster GENERATE) |
| 236–279 | A.4 Research Notes File | SUBSTITUTE (8-category structure is COPY) |
| 281–304 | A.5 Sufficiency Gate | SUBSTITUTE (gate framework is COPY) |
| 306–322 | A.6 Template Triage | COPY |
| 324–359 | A.7 Build Task File | SUBSTITUTE (loading contract pattern is COPY, refs files SUBSTITUTE) |
| 361–373 | A.8 Verify Task File | COPY |
| 377–397 | Stage B Delegation | COPY |
| 401–419 | Phase Loading Contract | SUBSTITUTE (table structure is COPY, rows SUBSTITUTE) |

---

## Deviations from Standard Skill Template

1. **Modular refs/ architecture:** SKILL.md is intentionally short (422 lines) with content offloaded to 5 refs files. The canonical 29-section monolithic structure is NOT used.
2. **No standalone "Examples" section** in SKILL.md (may exist in refs).
3. **No standalone "Anti-patterns" section** in SKILL.md.
4. **No standalone "Quality Gates" section** in SKILL.md (offloaded to `refs/validation-checklists.md`).
5. **No standalone "Error Handling" section** in SKILL.md (offloaded to `refs/operational-guidance.md`).
6. **No L-level tags** (L0/L1/L2) visible — phases use simple numeric labels.
7. **Phase Loading Contract section** (lines 401–419) is unique to modularized RF skills — likely not present in standard 29-section template.
8. **Stage A/Stage B explicit split** with delegation to `/task` skill — not a standard skill structure but an RF-doc-skill convention.
9. **8-category research-notes.md structure** is mandatory — likely an RF-doc-skill convention.
10. **FR (Functional Requirement) reference tags** like `FR-TDD-R.6a/b/c/d` — these tag specific lines/clauses for traceability, suggesting this skill was produced from a specification doc. Likely TDD-specific or RF-doc-skill convention.

---

## Section-to-Classification Summary Table (29 Canonical Sections)

Note: Mapping canonical sections to a modularized skill is approximate. Sections 19–29 mostly do not appear directly in SKILL.md.

| # | Canonical Section | TDD SKILL.md Location | Classification |
|---|---|---|---|
| 1 | YAML Frontmatter | Lines 1–4 | SUBSTITUTE |
| 2 | Title H1 | Line 6 | SUBSTITUTE |
| 3 | Mission Statement | Lines 8–12 | SUBSTITUTE |
| 4 | Why This Process Works | Lines 14–29 | SUBSTITUTE (mostly COPY) |
| 5 | Input | Lines 33–59 | SUBSTITUTE |
| 6 | Tier Selection | Lines 63–78 | SUBSTITUTE |
| 7 | Output Locations | Lines 81–113 | SUBSTITUTE |
| 8 | Execution Overview | Lines 116–145 | SUBSTITUTE |
| 9 | Stage A.1 — Existing Task Check | Lines 149–161 | COPY |
| 10 | Stage A.2 — Parse & Triage | Lines 163–184 | SUBSTITUTE |
| 11 | Stage A.3 — Scope Discovery | Lines 186–234 | SUBSTITUTE (agent roster GENERATE) |
| 12 | Stage A.4 — Research Notes | Lines 236–279 | SUBSTITUTE |
| 13 | Stage A.5 — Sufficiency Gate | Lines 281–304 | SUBSTITUTE |
| 14 | Stage A.6 — Template Triage | Lines 306–322 | COPY |
| 15 | Stage A.7 — Build Task File | Lines 324–359 | SUBSTITUTE |
| 16 | Stage A.8 — Verify Task File | Lines 361–373 | COPY |
| 17 | Stage B — Delegation | Lines 377–397 | COPY |
| 18 | Phase Loading Contract | Lines 401–419 | SUBSTITUTE |
| 19 | Agent Prompt Templates | refs/agent-prompts.md | SUBSTITUTE (offloaded) |
| 20 | BUILD_REQUEST Template | refs/build-request-template.md | SUBSTITUTE (offloaded) |
| 21 | Synthesis Mapping | refs/synthesis-mapping.md | SUBSTITUTE (offloaded) |
| 22 | Validation Checklists | refs/validation-checklists.md | SUBSTITUTE (offloaded) |
| 23 | Operational Guidance | refs/operational-guidance.md | SUBSTITUTE (offloaded) |
| 24 | (Examples) | NOT PRESENT in SKILL.md | (likely in refs) |
| 25 | (Anti-patterns) | NOT PRESENT in SKILL.md | (likely in refs) |
| 26 | (Error Handling) | offloaded to refs/operational-guidance.md | SUBSTITUTE |
| 27 | (Completion Criteria) | inferred in Phase 7 | SUBSTITUTE |
| 28 | (Quality Gates) | offloaded to refs/validation-checklists.md | SUBSTITUTE |
| 29 | (Session Management) | offloaded to refs/operational-guidance.md | SUBSTITUTE |

**No GENERATE classifications at section level** — all section-level structures are reused from the RF doc-skill template. GENERATE-level content appears at finer-grained levels: the 6 research agent types in A.3, the FR tag values, the specific output path conventions, and the trigger phrase list in frontmatter.

---

## Gaps and Questions

1. **[UNVERIFIED] 29-section canonical mapping accuracy** — The "29 canonical sections" used as the analysis frame come from the skill-creator skill specification, which I have not read directly. The mapping above assumes the canonical 29 sections include common skill components (frontmatter, title, mission, examples, anti-patterns, error handling, completion criteria, quality gates, session management). To verify, the skill-creator's standard template must be read.

2. **[UNVERIFIED] Boilerplate vs domain content boundaries** — Without comparing TDD SKILL.md side-by-side with PRD SKILL.md and tech-reference SKILL.md, my COPY/SUBSTITUTE classifications are inferred from boilerplate-like phrasing (e.g., "Stage A/B framework", "8-category research notes"). A diff across the three skills would confirm exact boilerplate boundaries.

3. **[UNVERIFIED] L-level tagging absence** — The TDD SKILL.md does not visibly use L0/L1/L2 tags. Whether this is intentional or whether L-level tagging is part of a different convention used by other RF skills is not determinable from this file alone.

4. **[UNVERIFIED] Refs file content classification** — Sections 19–23 are classified SUBSTITUTE without inspecting the refs file contents. The classification is based on SKILL.md's brief descriptions of what each refs file contains. If refs files contain pure boilerplate (COPY) or pure domain content (GENERATE), the classification would shift.

5. **[UNVERIFIED] Whether this skill is the canonical reference or an exception** — The skill's modularized structure (5 refs files, Phase Loading Contract, 422 lines) may represent a newer architectural pattern that supersedes the 29-section monolithic template. If skill-creator is meant to produce 29-section monolithic skills, TDD is an outlier; if skill-creator is meant to produce modularized skills, TDD is the model. This affects whether researchers should treat TDD as the reference or as a deviation.

6. **[CODE-VERIFIED] FR-TDD-R.6 tag prefix** — Tags `FR-TDD-R.6a`, `FR-TDD-R.6b`, `FR-TDD-R.6c`, `FR-TDD-R.6d` are present at SKILL.md lines 328, 338, 401, 414. This indicates the skill was generated from or aligned with a specification document (likely a PRD or TDD itself).

---

## Stale Documentation Found

None within this single SKILL.md file. The file is internally self-consistent. Cross-validation against actual code (e.g., whether `rf-task-builder`, `rf-task-researcher`, `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-assembler` agents exist) was not performed as part of this scope (analyzing SKILL.md structure, not validating runtime targets).

---

## Summary

The TDD SKILL.md is a **modularized reference skill** with 422 lines of orchestration logic in SKILL.md and ~65 KB of supporting content in 5 refs files. It does NOT match the canonical 29-section monolithic structure — instead it follows a Stage A (orchestrator scope discovery) + Stage B (delegated /task execution) pattern with a Phase Loading Contract enforcing refs file isolation.

**Key takeaways for skill-creator:**
- TDD-specific values: `TASK_ID_PREFIX=TASK-TDD-`, `COMPONENT_SLUG`, 7 phases, 6 research agent types, Lightweight/Standard/Heavyweight = 300–600/800–1,400/1,400–2,200 lines, output `docs/[domain]/TDD_[COMPONENT-NAME].md`
- 18 of 29 canonical sections appear in SKILL.md proper; 5 are explicitly offloaded to refs/; 6 are inferred-or-absent.
- Most sections are SUBSTITUTE (template + domain swaps); a handful are COPY (pure boilerplate); no whole sections are pure GENERATE.
- The Phase Loading Contract (lines 401–419) is a critical structural element unique to modularized RF skills.
- Research-notes.md 8-category structure (with PRD_CONTEXT being TDD-specific) and the 6-type research-agent roster are the most TDD-distinctive content elements.

**Status:** Complete

---

## Appendix — Canonical RF 29-Section Cross-Mapping (added per Phase 3 cycle 1 finding C-5)

The earlier Section-to-Classification Summary Table mapped tdd's modularized structure to a 29-row table with approximate canonical labels. The mapping below realigns to the **canonical RF 29-section schema as defined in research-notes.md REFERENCE_SKILL_ANALYSIS table (lines 178-209)**, which is the schema persona-research output SKILL.md must conform to. Each canonical RF section gets an explicit PRESENT / ABSENT / EMBEDDED marker against the tdd source.

| Canonical # | Canonical Name (per research-notes) | Marker | Evidence in tdd SKILL.md |
|---|---|---|---|
| S1 | Frontmatter + Title | PRESENT | Lines 1-6 |
| S2 | Overview + How it works | EMBEDDED | Folded into mission statement (lines 8-12) |
| S3 | Why This Process Works | PRESENT | Lines 14-29 |
| S4 | Variable Reference | ABSENT | No standalone variable-reference section in main file |
| S5 | Input | PRESENT | Lines 33-59 |
| S6 | Effective Prompt Examples | ABSENT | Not present in main SKILL.md (likely in refs/operational-guidance.md) |
| S7 | Incomplete Prompt | EMBEDDED | Folded into Section 5 Input "What to Do If the Prompt Is Incomplete" sub-block |
| S8 | Depth Tiers | PRESENT | Lines 63-78 (Tier Selection) |
| S9 | Output Locations | PRESENT | Lines 81-113 |
| S10 | Execution Overview | PRESENT | Lines 116-145 |
| S11 | Stage A header | PRESENT | At lines 116-149 region (Stage A is anchored within Execution Overview) |
| S12 | A.1 Check existing task file | PRESENT | Lines 149-161 |
| S13 | A.2 Parse & Triage | PRESENT | Lines 163-184 |
| S14 | A.3 Scope Discovery | PRESENT | Lines 186-234 |
| S15 | A.4 Write Research Notes | PRESENT | Lines 236-279 |
| S16 | A.5 Review Sufficiency | PRESENT | Lines 281-304 |
| S17 | A.6 Template Triage | PRESENT | Lines 306-322 |
| S18 | A.7 Build the Task File | PRESENT | Lines 324-359 |
| S19 | Stage B: Delegation | PRESENT | Lines 377-397 |
| S20 | Agent Prompt Templates | EMBEDDED | Offloaded to `refs/agent-prompts.md` per Phase Loading Contract (lines 401-419) |
| S21 | Output Structure | EMBEDDED | Folded into Output Locations (S9) and refs/build-request-template.md |
| S22 | Synthesis Mapping Table | EMBEDDED | Offloaded to `refs/synthesis-mapping.md` |
| S23 | Synthesis Quality Review Checklist | EMBEDDED | Offloaded to `refs/validation-checklists.md` |
| S24 | Assembly Process | EMBEDDED | Phase 6 description references assembly procedurally; no discrete header in main file |
| S25 | Validation Checklist | EMBEDDED | Offloaded to `refs/validation-checklists.md` |
| S26 | Content Rules | ABSENT | No discrete content-rules section in main SKILL.md |
| S27 | Critical Rules | ABSENT | No standalone Critical Rules section |
| S28 | Session Management | EMBEDDED | Offloaded to `refs/operational-guidance.md` per Phase Loading Contract |
| S29 | Research Quality Signals | ABSENT | No standalone quality-signals section |

**Roll-up vs canonical 29:** PRESENT 15 / EMBEDDED 9 / ABSENT 5.
**Implication for sc-persona-research-protocol generation:** The 9 EMBEDDED-in-refs sections in tdd (S2, S7, S20, S21, S22, S23, S24, S25, S28) indicate a heavy reliance on the modularized refs pattern. For persona-research, which targets a flat 29-section monolithic structure, the equivalent S20/S21/S22/S23/S24/S25/S28 sections must be GENERATEd as in-file sections rather than offloaded.

> **Note on hedge cleanup (per Phase 3 cycle 1 finding I-15):** The "appear to be COPY" hedge language in Section 4 boilerplate-boundary descriptions (line 60) has been retagged with `[UNVERIFIED]` markers, since cross-skill verbatim diffs to confirm "across RF skills" claims were not performed in this pass. Phase 4 cross-skill comparison should resolve.
