# Research: Reference Skill Analysis — skill-creator
**Investigation type:** Reference Skill Analysis
**Scope:** /config/workspace/IronClaude/.claude/skills/skill-creator/SKILL.md
**Status:** Complete
**Date:** 2026-04-29
**File Size:** 1522 lines, 119,462 bytes
---

## Top-Level Structure (Lines 1-700)

### Frontmatter (Lines 1-17) [CODE-VERIFIED]
- `name: skill-creator`
- `description:` mentions "29-section standard structure", "10-differentiator domain model", "agent-creator nesting"
- `trigger.phrases:` 10 phrases: "create a skill", "build a skill", "make a skill", "generate a skill", "write a skill", "design a skill", "scaffold a skill", "author a skill", "spin up a skill", "new skill"

### Domain Variables Identified (from Lines 48-58, A.3 Step 2 differentiators)

| Variable | Value | Source Line |
|----------|-------|-------------|
| TASK_ID | `TASK-SKILLCREATE-<subject>-YYYYMMDD-HHMMSS` | L49 |
| TASK_ID_PREFIX | `TASK-SKILLCREATE` | L470 |
| DOMAIN_NAME | parameterized (kebab-case skill name) | L68 |
| DOMAIN_SLUG | kebab-case version of DOMAIN_NAME | L299 |
| OUTPUT location | `.temp/skills/${DOMAIN_NAME}/SKILL.md` | L57, L161 |
| TEMPLATE_BASE | `.claude/templates/documents/` | L56 |
| Subject derivation | from DOMAIN_NAME, kebab-case, ~30 char cap, fallback "general" | L60 |
| Output type | report (default) / document / distributed | L72-77 |
| Reference skills default | report→tech-research+repo-cleanup; document→tech-reference+prd; distributed→readme | L80-82 |

### Depth Tiers (Lines 117-143) [CODE-VERIFIED]
| Tier | Codebase Agents | Reference Skills | Target Lines | qa_intensity |
|------|----------------|------------------|--------------|--------------|
| Quick | 2 | 2 | 800-1000 | lite |
| Standard | 3 | 3 | 1000-1300 | standard |
| Deep | 5 | 5+ | 1200-1500 | full |

### Phase Structure (Lines 185-194) [CODE-VERIFIED]
**7-phase structure with L-level mappings:**
- Phase 1: Preparation — L0 Setup
- Phase 2: Reference Skill Analysis — L1 Discovery (parallel agents)
- Phase 3: Completeness Verification — L4 Review/QA (6 lens agents)
- Phase 4: Skeleton Assembly + Domain Generation — L2 Build-from-Discovery
- Phase 5: Lens-Based Structural + Qualitative QA Gate — L4 Review/QA (6+ lens + 3 fidelity)
- Phase 6: Lens-Based Final QA — L6 Aggregation (6+ lens)
- Phase 7: Present to User & Complete Task — L0 Closeout

### 10-Differentiator Domain Model (Lines 285-296) [CODE-VERIFIED]
| # | Differentiator | Skill-Creator Value |
|---|---------------|---------------------|
| D1 | TASK_ID_PREFIX | TASK-SKILLCREATE |
| D2 | Slug field name | DOMAIN_SLUG |
| D3 | Agent type roster | Reference Skill Analyst, Section Classifier (+ generic 3 if Scenario B) |
| D4 | Scope classification | A/B + Quick/Standard/Deep, Standard default |
| D5 | Line ceiling | None for skill-creator (default for non-navigational) |
| D6 | Output location | .temp/skills/${DOMAIN_NAME}/SKILL.md (in-task-folder report variant) |
| D7 | QA lens phase names | `{domain-short}-{lens}` pattern; e.g., codereview-actionability |
| D8 | Validation requirements | TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + SECTION_COUNT_29 |
| D9 | Additional input fields | OUTPUT_TYPE, REFERENCE_SKILLS, AGENT_FILES |
| D10 | Phase structure | 7-phase |

### Agent Type Roster (Lines 342-348) [CODE-VERIFIED]
5 types defined in Research assignment table:
1. Code Tracer — read implementations, trace data flow
2. Doc Analyst — extract context from docs, cross-validate against code
3. Integration Mapper — map APIs, extension points
4. Reference Skill Analyst — extract structural patterns from existing skills
5. Section Classifier — classify sections for the new skill

### QA Intensity Lens Counts (Lines 499-514) [CODE-VERIFIED]
**Gate 1 (Phase 3, Research Completeness):**
- lite: 2 agents, max 1 fix cycle
- standard: 3 agents (1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative), max 2 fix cycles
- full: 6 agents (2+2+2), max 3 fix cycles

**Gate 2 (Phase 5, Structural+Qualitative):**
- lite: 3 agents, max 1 fix cycle
- standard: 6 agents (3 rf-qa + 3 rf-qa-qualitative), max 2 fix cycles
- full: 6 agents, max 2 fix cycles

**Gate 2.5 (Phase 5, Source-Document Fidelity):**
- lite: 1 agent, max 1 fix cycle
- standard: 2 agents, max 2 fix cycles
- full: 3 agents (rf-qa reference-skill + rf-qa template + rf-qa-qualitative domain-noun), max 2 fix cycles

**Gate 3 (Phase 6, Final QA):**
- lite: 3 agents, max 1 fix cycle
- standard: 5 agents, max 2 fix cycles
- full: 6 agents (2 rf-qa + 4 rf-qa-qualitative), max 2 fix cycles

### VALIDATION_REQUIREMENTS (Lines 516-520) [CODE-VERIFIED]
- TEMPLATE_COMPLIANCE: 29 sections present, correct ordering
- EVIDENCE_TRAIL: every generated section cites domain model field(s)
- CROSS_VALIDATION: COPY byte-match, SUBSTITUTE has no leftover reference nouns
- SECTION_COUNT_29: exactly 29 sections

---

## 29-Section Classification Table (Skill-Creator)

S-numbers verified against L1247 explanatory note ("S1 = Frontmatter + `#` Title heading, S2 = Overview paragraph under the title, S19 = Stage B including Delegation Protocol and What the Task File Must Contain subsections") and the section-numbered comments in the Output Structure schema (L1245-1312). [CODE-VERIFIED]

| # | Section Name | Classification | Lines | Domain Variables | Notes |
|---|--------------|---------------|-------|------------------|-------|
| S1 | Frontmatter + `#` Title | SUBSTITUTE | 1-19 | name, description, trigger.phrases | YAML frontmatter + H1 title; all 5 trigger phrase signals + 5 verb synonyms |
| S2 | Overview (intro paragraph + "How it works") | GENERATE | 19-25 | DOMAIN_NAME, workflow description | Domain-specific narrative |
| S3 | Why This Process Works | GENERATE (mostly) | 27-43 | failure modes, phase list, guarantees | Skill-specific failure modes; references "29-section structure", "10-differentiator domain model", "33+ total agent spawns" |
| S4 | Variable Reference | SUBSTITUTE | 44-62 | TASK_ID_PREFIX (D1), OUTPUT path (D6), TEMPLATE_BASE | Boilerplate scaffolding with substituted paths; contains TASK-SKILLCREATE prefix and `.temp/skills/${DOMAIN_NAME}/SKILL.md` output |
| S5 | Input | GENERATE | 64-115 | 5 input fields (DOMAIN_NAME, DOMAIN_DESCRIPTION, OUTPUT_TYPE, REFERENCE_SKILLS, AGENT_FILES) | Domain-specific 5-field model; 1 mandatory, 4 optional |
| S6 | Effective Prompt Examples | GENERATE | 86-102 | Strong/Weak examples | Domain-specific prompt examples |
| S7 | What to Do If the Prompt Is Incomplete | GENERATE | 103-115 | Clarification template | 5-question elicitation template |
| S8 | Depth Tiers | SUBSTITUTE | 117-143 | Quick/Standard/Deep table with metrics | Standard 3-tier table with skill-creator-specific metrics (codebase agents, ref skills, target lines) + qa_intensity mapping table |
| S9 | Output Locations | SUBSTITUTE | 145-166 | Artifact table with skill-creator paths | Standard 12-row artifact table with skill-creator-specific outputs (.temp/skills/, agent files) |
| S10 | Execution Overview | GENERATE | 168-196 | Stage A 7-step list + Stage B + 7 phase names | Domain-specific phase list with L-level mappings |
| S11 | Stage A header | COPY | 198 | none | Pure header line |
| S12 | A.1: Check for Existing Task File | SUBSTITUTE | 200-213 | TASK_ID glob pattern, paths | Standard pattern with TASK-SKILLCREATE-* glob |
| S13 | A.2: Parse & Triage | GENERATE | 214-247 | 5-field extraction table, scenario A/B examples | Domain-specific 5-field signal table; collision check via Glob |
| S14 | A.3: Perform Scope Discovery | GENERATE | 248-366 | 3-step pipeline with 10-differentiator table | Largest section; contains canonical 10-differentiator definition (D1-D10), partitioning rules, agent type roster table |
| S15 | A.4: Write Research Notes File | SUBSTITUTE | 367-400 | Research notes template | Standard structure with skill-creator section labels (EXISTING_FILES, REFERENCE_SKILL_ANALYSIS, etc.) |
| S16 | A.5: Review Research Sufficiency | SUBSTITUTE | 402-424 | 7-item gate checklist | Standard gate pattern with skill-creator-specific items (3 reference skills minimum, 10 differentiators populated) |
| S17 | A.6: Template Triage | SUBSTITUTE | 426-442 | Template 01 vs 02 decision | Standard triage with skill-creator override "almost always Template 02" |
| S18 | A.7: Build the Task File | GENERATE | 444-670 | BUILD_REQUEST template with all phases | Largest sub-section; contains complete BUILD_REQUEST embedded as a code block with TASK_ID_PREFIX, 7-phase encoding, QA Intensity gate definitions, agent-creator nesting protocol |
| S19 | Stage B: Task File Execution | COPY | 672-694 | Delegation protocol | Standard /task delegation; minor skill-creator phase descriptor in QA coverage paragraph |
| S20 | Agent Prompt Templates | GENERATE | 696-1241 | 13 agent prompts | Domain-specific 13 prompt templates: Reference Skill Analyst, Section Classifier, rf-analyst Completeness, rf-qa Research Gate, 6 lens prompts (Template-Conformance, Internal-Consistency, Evidence-Quality, Actionability, Domain-Accuracy, Section-Classification-Accuracy), Research Depth, Research Breadth, Source-Fidelity. Each prompt embeds VERBATIM protocol blocks (Incremental Writing, Documentation Staleness, Adversarial Stance) |
| S21 | Output Structure | SUBSTITUTE | 1245-1313 | Section schema with S-numbers | Schema diagram with skill-creator's 29 sections labeled with S-numbers in HTML comments |
| S22 | Synthesis Mapping Table | GENERATE | 1315-1333 | 5-row synth file mapping | Domain-specific reference table; explicitly notes synth files NOT produced (Phase 4 writes directly to output) |
| S23 | Synthesis Quality Review Checklist | SUBSTITUTE | 1335-1354 | 10-criteria checklist | Standard 10-item checklist with skill-creator-specific criteria (29-section structure, COPY byte-identical, etc.) |
| S24 | Assembly Process | GENERATE | 1356-1370 | 4-step incremental Edit pattern | Domain-specific assembly with section group ordering S1-S4, S5-S18, S19-S20, S21-S29 |
| S25 | Validation Checklist | GENERATE | 1372-1399 | 23-item checklist | Domain-specific items: 29 sections, COPY byte-match, SUBSTITUTE no leftover nouns, GENERATE no TODOs, line count ranges per tier, lens-based QA gates, source-fidelity gate, etc. |
| S26 | Content Rules (Non-Negotiable) | SUBSTITUTE | 1401-1424 | 11-row Do/Don't table | Standard 6 boilerplate rows + 5 domain-specific rows (Boilerplate sections, Section classifications, Template GUIDANCE comments, Domain nouns, QA architecture in generated skills) |
| S27 | Critical Rules (Non-Negotiable) | GENERATE | 1426-1477 | 22 numbered rules | 9 generic rules + 13 skill-creator-specific rules (default tier Standard, .temp/ output only, section classifications from comparison, boilerplate verbatim, AGENT_FILES default false, all protocol blocks mandatory, single-agent prohibition, no cost-anxiety pauses, min QA floor, serialized fix mandatory, source-fidelity mandatory) |
| S28 | Session Management | SUBSTITUTE | 1479-1493 | Session resumption pattern | Standard /task delegation with skill-creator TASK-SKILLCREATE-* glob |
| S29 | Research Quality Signals | SUBSTITUTE | 1495-1522 | Strong/Weak signals + spawn triggers | Standard 3-section pattern (Strong/Weak/When to Spawn) with skill-creator-specific signals (10 differentiators, section classifications, boilerplate boundaries) |

---

## Classification Summary

| Classification | Count | Section Numbers |
|---------------|-------|-----------------|
| COPY | 2 | S11, S19 |
| SUBSTITUTE | 12 | S1, S4, S8, S9, S12, S15, S16, S17, S21, S23, S26, S28, S29 (13 actually) |
| GENERATE | 14 | S2, S3, S5, S6, S7, S10, S13, S14, S18, S20, S22, S24, S25, S27 |

**Recount verification:** S1, S4, S8, S9, S12, S15, S16, S17, S21, S23, S26, S28, S29 = 13 SUBSTITUTE.
2 COPY + 13 SUBSTITUTE + 14 GENERATE = 29 ✓

---

## Substitution Points (Bracketed Placeholders)

The following placeholder variables appear repeatedly in skill-creator and would need substitution per skill-domain:

| Placeholder | Skill-Creator Value | Sections Used |
|-------------|--------------------|--------------------|
| `${DOMAIN_NAME}` | parameterized (e.g., code-review) | Throughout (S4, S5, S9, S14, S18, S20, S25) |
| `${DOMAIN_SLUG}` | usually identical to DOMAIN_NAME | S5, S14, S20 |
| `${TASK_DIR}` | `.dev/tasks/to-do/TASK-SKILLCREATE-<subject>-YYYYMMDD-HHMMSS/` | S4, S9, S14, S15, S20, S28 |
| `${TASK_ID}` | `TASK-SKILLCREATE-<subject>-YYYYMMDD-HHMMSS` | S4, S9 |
| `${TEMPLATE_BASE}` | `.claude/templates/documents/` | S4, S18, S20 |
| `${TASK_ID_PREFIX}` | `TASK-SKILLCREATE` | S4, S18 |
| `[task-dir-path]` | runtime path | S20 prompts |
| `[output-path]` | runtime path | S20 prompts |
| `[Quick/Standard/Deep]` | tier selection | S20 prompts |

---

## Verbatim Protocol Blocks (must be copied byte-for-byte)

Identified in Agent Prompt Templates section (S20) (per L700-707 Mandatory Prompt Architecture):
1. **Incremental File Writing Protocol** — appears in all 13 agent prompts (e.g., L733-752 Reference Skill Analyst, L814-817 Section Classifier)
2. **Documentation Staleness Protocol** — appears in research agents (e.g., L767-785 Reference Skill Analyst)
3. **ADVERSARIAL STANCE** — appears in all QA agents (e.g., L896, L943, L975, L1006, L1038, L1073, L1110, L1146, L1186, L1222)
4. **VERDICTS (PASS/FAIL)** — appears in all QA agent prompts as final decision section

Additional verbatim protocol blocks identified (L700-707):
- **Role assignment** ("You are a [role] agent for the skill-creator skill.")
- **Task instruction** ("Read [specific files] and [specific action].")
- **Required output structure** (exact section format)
- **Anti-consolidation guard** ("Generate one [item] per discrete unit of work. NEVER merge...")
- **Specificity instruction** ("Include file paths, function names, and testable acceptance criteria")
- **Anti-preamble** ("Begin your response with the output content directly.")

---

## Phase Names → L-Level Mapping (D7/D10) [CODE-VERIFIED]

From Lines 185-194 and L488-494 of A.7 BUILD_REQUEST:

| Phase | Name | L-Level | Agent Count (full) |
|-------|------|---------|-----|
| Phase 1 | Preparation | L0 Setup | 0 (orchestrator only) |
| Phase 2 | Reference Skill Analysis | L1 Discovery | 2-5 (per tier) |
| Phase 3 | Completeness Verification | L4 Review/QA | 6 lens + 1 fix + 2 verify = 9 |
| Phase 4 | Skeleton Assembly + Domain Generation | L2 Build-from-Discovery | 0 (orchestrator) |
| Phase 5 | Lens-Based Structural + Qualitative QA Gate | L4 Review/QA | 6 lens + 1 fix + 2 verify + 3 fidelity = 12 |
| Phase 6 | Lens-Based Final QA | L6 Aggregation | 6 lens + 1 fix + 2 verify = 9 |
| Phase 7 | Present to User & Complete Task | L0 Closeout | 0 (orchestrator) |

QA phase naming pattern (D7): `skillcreate-{lens-name}` (e.g., skillcreate-template-conformance, skillcreate-internal-consistency, skillcreate-evidence-quality, skillcreate-actionability, skillcreate-domain-accuracy, skillcreate-section-classification-accuracy, skillcreate-research-depth, skillcreate-research-breadth, skillcreate-source-fidelity).

---

## Boilerplate Boundaries (Per-Section Line Ranges)

| Section | Boilerplate Range | Domain-Specific Range |
|---------|-------------------|----------------------|
| S1 (Frontmatter) | YAML structure (lines 1, 4-16, 17) | name/description/triggers values (L2, 3, 7-16) |
| S4 (Variable Reference) | Path scaffolding L46-58 | TASK_ID_PREFIX value, OUTPUT path with .temp/skills (L49, 57) |
| S8 (Depth Tiers) | Table structure | Tier metrics row values (L123-125) |
| S11 (Stage A header) | Pure header `## Stage A:...` (L198) | None |
| S14 (A.3) | Step 1/2/3 structure | 10-differentiator definitions L285-296 (CANONICAL) |
| S19 (Stage B) | Delegation protocol L676-694 | Phase mention in QA coverage paragraph (L681) |
| S20 (Agent Prompts) | 6 mandatory protocol blocks per prompt | Domain investigation steps + lens checklists |
| S26 (Content Rules) | First 6 rows of Do/Don't table | Last 5 rows (Boilerplate, Section classifications, etc.) |
| S27 (Critical Rules) | Rules 1-9 (generic) | Rules 10-22 (skill-creator-specific) |
| S28 (Session Mgmt) | /task delegation pattern | TASK-SKILLCREATE-* glob (L1481, 1485) |

---

## Anomalies / Deviations from Standard Skill Template

1. **S20 has 13 agent prompts (vs typical 4-5 in other skills)** — Domain-specific because skill-creator has lens-based QA architecture with 6 lens prompts + 3 specialized lenses (depth, breadth, fidelity) + 4 base prompts.
2. **S22 explicitly disclaims its own outputs** — L1318: "These files are NOT produced during execution. Phase 4 writes directly to the output SKILL.md via incremental Edit." This is a documented deviation from the standard synthesis pattern.
3. **S25 Validation Checklist has 23 items** (vs typical ~10) — Reflects the meta-nature: skill-creator must validate that generated skills also follow the QA standard.
4. **S27 Critical Rules has 22 rules** (vs typical ~12) — The extra rules enforce the meta-recursion (skill-creator standards must propagate to generated skills): Rule 16 (AGENT_FILES default false), Rule 17 (protocol block enforcement), Rule 19 (no cost-anxiety pauses), Rule 20 (minimum QA floor with two-tier system), Rule 21 (serialized fix mandatory), Rule 22 (source-fidelity gate mandatory).
5. **A.7 BUILD_REQUEST is exceptionally large (~225 lines, L444-670)** — Encodes complete 7-phase task structure with QA intensity tables for all 4 gates (Gate 1, 2, 2.5, 3) and 3 intensity levels (lite/standard/full).
6. **Note at L1247 explicitly clarifies S1/S2/S19 ambiguity** — explains S1 = Frontmatter + Title, S2 = Overview, S19 = Stage B including subsections. This indicates the canonical numbering had ambiguity that needed disambiguation.

---

## Key Domain Variable Values for Persona-Research Skill Inference

If using skill-creator as a reference for a persona-research skill:

| Differentiator | skill-creator value | Likely persona-research value |
|----------------|---------------------|-------------------------------|
| D1 TASK_ID_PREFIX | TASK-SKILLCREATE | TASK-PERSONA or TASK-PERSONARES |
| D2 Slug field | DOMAIN_SLUG | PERSONA_SLUG |
| D3 Agent type roster | Reference Skill Analyst, Section Classifier (+ generic 3) | Persona Researcher, Demographic Analyst, Behavior Mapper, etc. |
| D5 Line ceiling | None | None (research-type) |
| D6 Output location | .temp/skills/${DOMAIN_NAME}/SKILL.md | likely .dev/tasks/.../research/persona-*.md or similar |
| D7 QA phase names | skillcreate-{lens} | personares-{lens} or persona-{lens} |
| D10 Phase structure | 7-phase | 7-phase (default) |

---

## Gaps and Questions

1. **[UNVERIFIED]** Whether skill-creator's documented 7-phase structure is universally followed by other skills in `.claude/skills/` — would need to read tech-research, prd, etc. to confirm. Skill-creator's own sec L36 mentions a structure that includes "lens-based completeness verification (6 agents)" which is unique to skill-creator's QA-heavy nature.

2. **[UNVERIFIED]** Whether the explicit "29 sections" count is part of every skill or specific to the canonical template. The output structure schema (L1245-1312) shows 29 S-labels in this skill, but other reference skills may have variations.

3. **[CODE-VERIFIED]** The skill template at `${TEMPLATE_BASE}skill_template.md` (i.e., `.claude/templates/documents/skill_template.md`) is referenced as the schema authority but NOT read in this analysis. To fully verify COPY/SUBSTITUTE classifications, that template file would need to be read directly.

4. **[CODE-VERIFIED]** Section S29 ends at line 1522 (file end). No deviations from standard final section pattern.

5. **[UNVERIFIED]** The exact ordering of S22-S29 vs the canonical template — skill-creator places S22 (Synthesis Mapping) before S25 (Validation Checklist), but other skills may differ. The L1247 note states the template has "S29 = Research Quality Signals" confirming the final section identity, which matches skill-creator.

---

## Stale Documentation Found

None within this single-file analysis. The L1247 explanatory note ("This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.") and the similar note at L1320 explicitly flag that the schema/synthesis sections are reference-only — they are NOT stale, they are documented as informational.

The `Synthesis Mapping Table` (S22) at L1318 explicitly states: "These files are NOT produced during execution. Phase 4 writes directly to the output SKILL.md via incremental Edit. This table documents the logical section groupings for reference only -- it is NOT a list of files to create." This is a self-aware staleness disclaimer (the table represents an older synthesis-file pattern that has since been replaced by direct incremental Edit assembly).

---

## Summary

**Skill-creator** is a meta-skill that generates other skills following the 29-section RF standard. It uses:
- **TASK_ID_PREFIX:** TASK-SKILLCREATE
- **Output:** `.temp/skills/${DOMAIN_NAME}/SKILL.md`
- **Phase count:** 7-phase
- **QA architecture:** Lens-based with 3 gates (Gate 1: 6 agents Phase 3, Gate 2+2.5: 6+3=9 agents Phase 5, Gate 3: 6 agents Phase 6); all use serialized fix authorization with verification rounds
- **Line ceiling:** None
- **Agent type roster (D3):** Reference Skill Analyst, Section Classifier + 3 generic types (Code Tracer, Doc Analyst, Integration Mapper) for Scenario B deep exploration
- **Validation:** TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + SECTION_COUNT_29
- **Special characteristics:** Self-recursive (skill-creator's QA standards must propagate to generated skills via Critical Rules 16-22); explicit meta-enforcement loop

**Section classification distribution:** 2 COPY + 13 SUBSTITUTE + 14 GENERATE = 29 sections.

**For persona-research skill inference:** skill-creator demonstrates the canonical 7-phase pattern with 13 agent prompt templates and lens-based QA. The persona-research skill should likely follow the same structure but substitute domain-specific agent types (e.g., Persona Researcher, Demographic Analyst), differentiator values, and replace the "skill creation" workflow with a "persona research" workflow.

**Status:** Complete


