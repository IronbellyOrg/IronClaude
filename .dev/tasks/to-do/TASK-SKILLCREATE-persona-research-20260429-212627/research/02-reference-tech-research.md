# Research: Reference Skill Analysis — tech-research
**Investigation type:** Reference Skill Analysis
**Scope:** /config/workspace/IronClaude/.claude/skills/tech-research/SKILL.md
**Status:** Complete
**Date:** 2026-04-29
**Source line count:** 1322
---

## Domain Variable Extraction

| Variable | Value (in tech-research) | Notes |
|----------|--------------------------|-------|
| `TASK_ID_PREFIX` | `TASK-RESEARCH` | Used in folder + file names |
| `TASK_ID` format | `TASK-RESEARCH-YYYYMMDD-HHMMSS` | timestamp-based |
| Slug field name | `TOPIC_SLUG` | kebab-case (e.g., `locomotion-params`) |
| Slug examples | `locomotion-params`, `ade-hot-reload`, `agent-memory-system` | from line 111 |
| Output location root | `.dev/tasks/to-do/${TASK_ID}/` | TASK_DIR |
| Final output filename | `RESEARCH-REPORT-[descriptor].md` | placed in TASK_DIR |
| QA phase names | `research-gate`, `synthesis-gate`, `report-validation`, `report-qualitative`, `fix-cycle` | five distinct QA phases |
| Phase count | **7 phases** (Preparation, Deep Investigation, Completeness Verification, Web Research, Synthesis+QA, Assembly+Validation, Present) | from lines 384-431 |
| Line ceiling (file) | 1322 lines | actual file length |
| Subfolders created | `research/`, `synthesis/`, `qa/`, `reviews/` | line 225 |
| Section count in final report | **10 sections** | lines 927-937 |
| Validation checklist size | **15 items + 4 content quality checks** | line 869 / lines 873-895 |
| Synthesis QA checklist size | **12 items** | line 833 |
| Synthesis Quality Review (analyst) | **9 criteria** | line 1166 |
| Research Gate checklist | **10 items** | line 788 |
| Research Completeness checklist (analyst) | **8 items** | line 745 |
| Qualitative QA checklist | **12 items** | line 423 |
| Partitioning threshold (Phase 3) | **>6 research files** | line 397 |
| Partitioning threshold (Phase 5) | **>4 synth files** | line 416 |
| Max fix cycles | **3** | lines 401, 417 |
| Max gap-fill rounds (A.5) | **2** | line 292 |

## Agent Roster

| Agent | subagent_type | Purpose | Phase |
|-------|---------------|---------|-------|
| rf-task-builder | `rf-task-builder` | Build the MDTM task file from research notes | A.7 (pre-task) |
| rf-task-researcher | `rf-task-researcher` | Optional scope discovery helper | A.3 (pre-task) |
| Codebase Research Agent | generic `Agent` | Investigate codebase aspects | Phase 2 |
| Web Research Agent | generic `Agent` | External research | Phase 4 |
| Synthesis Agent | generic `Agent` | Build report sections from research files | Phase 5 |
| rf-analyst | `rf-analyst` | Analytical quality gate (completeness-verification, synthesis-review) | Phases 3, 5 |
| rf-qa | `rf-qa` | QA quality gate (research-gate, synthesis-gate, report-validation, fix-cycle) | Phases 3, 5, 6 |
| rf-qa-qualitative | `rf-qa-qualitative` | Qualitative content review | Phase 6 |
| rf-assembler | `rf-assembler` | Single dedicated report assembler | Phase 6 |

## Phase-to-L-level Mapping (from BUILD_REQUEST lines 341-345)

| Phase | Activity | L-level |
|-------|----------|---------|
| Phase 2 | Deep Investigation | L1 Discovery |
| Phase 3 | Completeness Verification | L4 Review/QA |
| Phase 4 | Web Research | L1 Discovery |
| Phase 5 | Synthesis + QA Gate | L2 Build-from-Discovery |
| Phase 6 | Assembly + Validation | L6 Aggregation |

## 29-Section Canonical Classification

Note: tech-research SKILL.md does not literally use 29 numbered "canonical sections" — it uses domain-organized headings. I map each tech-research section to the closest canonical-skill role and classify what's reusable across skills.

Classification key:
- **COPY** — verbatim or near-verbatim across skills (boilerplate)
- **SUBSTITUTE** — same shape, but bracketed values/names change per domain
- **GENERATE** — domain-specific content authored fresh per skill

### Section Index (file order)

| # | Section Heading | Lines | Classification | Domain Variables |
|---|----------------|-------|----------------|------------------|
| 1 | Frontmatter (`name`, `description`) | 1-4 | SUBSTITUTE | `name`, full description string with trigger phrases |
| 2 | Title (`# Technical Research & Investigation`) | 6 | SUBSTITUTE | skill display title |
| 3 | Skill preamble (description + how it works) | 8-12 | SUBSTITUTE | builder agent name (`rf-task-builder`), skill purpose, downstream skill ref (`tech-reference`) |
| 4 | `## Why This Process Works` | 14-29 | SUBSTITUTE | phase list (lines 23), QA agent names, four failure modes paragraph |
| 5 | `### Variable Reference` | 31-43 | SUBSTITUTE | TASK_ID prefix, subfolder list (research/synthesis/qa/reviews) |
| 6 | `## Input` (4 pieces of info) | 47-58 | SUBSTITUTE | domain-specific examples of WHAT/WHY/WHERE/OUTPUT_TYPE |
| 7 | `### Effective Prompt Examples` | 60-74 | GENERATE | full domain-specific prompts |
| 8 | `### What to Do If the Prompt Is Incomplete` | 76-87 | SUBSTITUTE | clarification template with domain placeholders |
| 9 | `## Depth Tiers` | 91-105 | SUBSTITUTE | tier table (Quick/Standard/Deep), agent counts, "default to Deep" rule |
| 10 | `## Output Locations` | 109-131 | SUBSTITUTE | artifact table — TASK_ID prefix, file naming patterns, subfolder layout |
| 11 | `## Execution Overview` (Stage A / Stage B) | 135-153 | COPY | nearly verbatim two-stage pattern; only step 2 ("triage Scenario A vs B") is domain-tinted |
| 12 | `## Stage A: Scope Discovery & Task File Creation` header + `### A.1` | 156-170 | SUBSTITUTE | TASK prefix in folder check |
| 13 | `### A.2: Parse & Triage the Research Question` | 172-192 | SUBSTITUTE | GOAL/WHY/WHERE/OUTPUT_TYPE/TOPIC_SLUG variable names; Scenario A/B examples |
| 14 | `### A.3: Perform Scope Discovery` | 194-229 | SUBSTITUTE | research assignment types table (Code Tracer / Doc Analyst / Integration Mapper / Pattern Investigator / Architecture Analyst); subfolder list |
| 15 | `### A.4: Write Research Notes File` | 231-271 | SUBSTITUTE | 6 mandatory categories (EXISTING_FILES, PATTERNS_AND_CONVENTIONS, SOLUTION_RESEARCH, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER) |
| 16 | `### A.5: Review Research Sufficiency` | 273-294 | COPY | gate logic with 6 review criteria; max 2 gap-fill rounds |
| 17 | `### A.6: Template Triage` | 296-312 | COPY | Template 01 vs 02 selection logic |
| 18 | `### A.7: Build the Task File` (BUILD_REQUEST) | 314-448 | SUBSTITUTE | full BUILD_REQUEST format — phase definitions, agent prompts, granularity requirement, escalation rules |
| 19 | `### A.8: Receive & Verify the Task File` | 450-461 | SUBSTITUTE | verification criteria reference Phase 6 agents (rf-assembler/rf-qa/rf-qa-qualitative) |
| 20 | `## Stage B: Task File Execution` (Execution Loop F1) | 465-483 | COPY | five-step READ→IDENTIFY→EXECUTE→UPDATE→REPEAT |
| 21 | `### Prohibited Actions (F2)` | 485-494 | COPY | universal MDTM rules |
| 22 | `### Parallel Agent Spawning` | 496-507 | SUBSTITUTE | phase numbers (2, 3, 4, 5) and which phases require parallelism |
| 23 | `### Task File Modification Restrictions (F4)` | 509-521 | COPY | universal MDTM rules |
| 24 | `### Frontmatter Update Protocol (F5)` | 523-532 | COPY | universal MDTM event table |
| 25 | `### Error Handling` | 534-540 | COPY | universal blocker handling |
| 26 | `### Session Resumption` | 542-552 | SUBSTITUTE | TASK prefix in folder pattern; subfolder list |
| 27 | `## Agent Prompt Templates` (header) | 556-558 | COPY | one-line section intro |
| 28 | `### Codebase Research Agent Prompt` | 560-649 | SUBSTITUTE | topic, file list, output path are placeholders; protocol blocks (Incremental File Writing + Documentation Staleness) are COPY-grade boilerplate |
| 29 | `### Web Research Agent Prompt` | 651-688 | SUBSTITUTE | topic, codebase context summary; protocol intro is COPY-grade |
| 30 | `### Synthesis Agent Prompt` | 690-721 | SUBSTITUTE | research files, report sections, output path; 10 rules + Incremental File Writing block are COPY |
| 31 | `### Research Analyst Agent Prompt` | 723-761 | SUBSTITUTE | task-dir-path, depth tier, output path; 8-item checklist is fixed |
| 32 | `### Research QA Agent Prompt` | 763-806 | SUBSTITUTE | task-dir-path, depth tier; 10-item checklist is fixed |
| 33 | `### Synthesis QA Agent Prompt` | 808-850 | SUBSTITUTE | task-dir-path, fix authorization; 12-item checklist is fixed |
| 34 | `### Report Validation QA Agent Prompt` | 852-897 | SUBSTITUTE | report path, task dir; 15+4 checklist is fixed |
| 35 | `### Assembly Agent Prompt (rf-assembler)` | 899-965 | SUBSTITUTE | component file list, report header values; 7 assembly rules + content rules are COPY |
| 36 | `## Report Structure` (10-section markdown template) | 969-1143 | GENERATE | entire report scaffold is fully domain-specific |
| 37 | `## Synthesis Mapping Table` | 1147-1158 | GENERATE | synth-file-to-report-section mapping is fully domain-specific |
| 38 | `## Synthesis Quality Review Checklist` (9 criteria) | 1162-1178 | SUBSTITUTE | criteria 1-7 generic with domain section refs; criteria 8-9 reference specific report sections (Sections 2/4/8/9) |
| 39 | `## Assembly Process` (4 steps) | 1182-1194 | SUBSTITUTE | step 4 cross-checks reference specific report sections (4, 6, 8, 9, 10) |
| 40 | `## Validation Checklist` (15 items) | 1198-1215 | SUBSTITUTE | each item references specific report sections of this domain |
| 41 | `## Content Rules (Non-Negotiable)` | 1219-1242 | COPY | universal writing standards table — applies across docs/research skills |
| 42 | `## Critical Rules` (15 numbered) | 1246-1277 | SUBSTITUTE | 15 rules mostly universal; specific phase numbers and partitioning thresholds are domain values |
| 43 | `## Session Management` | 1281-1297 | SUBSTITUTE | TASK prefix and subfolder list |
| 44 | `## Research Quality Signals` | 1301-1322 | GENERATE | strong/weak signals + when-to-spawn — fully domain-specific examples |

(Note: 44 distinct headings observed — more than 29 because the source skill subdivides Stage A into A.1–A.8 and Agent Prompt Templates into 7 sub-templates. The "29 canonical sections" model in the task brief likely groups these.)

## Substitution Points (Bracketed Placeholders Inventory)

These are placeholders that appear throughout tech-research and which a new skill must populate. Each entry shows the placeholder, its meaning, and an example value from tech-research.

| Placeholder | Meaning | tech-research value |
|-------------|---------|---------------------|
| `[topic]` | The thing being investigated | "GameFrame locomotion parameters" |
| `[TOPIC]` | Capitalized topic header | "LOCOMOTION PARAMS" |
| `[descriptor]` | Final report filename suffix | e.g. `locomotion-hot-reload` |
| `[output-path]` | Per-agent output file path | `${TASK_DIR}research/[NN]-[aspect].md` |
| `[NN]` | Zero-padded sequence number | `01`, `02`, ... |
| `[aspect-name]` / `[topic]` | Slug for the assignment | `agent-routing`, `gpu-allocation` |
| `[type]` | Investigation type | Code Tracer / Doc Analyst / Integration Mapper / Pattern Investigator / Architecture Analyst |
| `[task-dir-path]` | Full TASK_DIR | `.dev/tasks/to-do/TASK-RESEARCH-YYYYMMDD-HHMMSS/` |
| `[Quick/Standard/Deep]` | Depth tier | one of three |
| `[count]` | Numeric count of files | e.g. "8 codebase + 3 web" |
| `[GOAL]`, `[WHY]` | Triage variables | substituted in BUILD_REQUEST |
| `[01 or 02]` | Template selector | almost always `02` |
| `[today]` | Current date | YYYY-MM-DD |
| `${TASK_DIR}` | Variable reference | `.dev/tasks/to-do/${TASK_ID}/` |
| `${TASK_ID}` | Task identifier | `TASK-RESEARCH-YYYYMMDD-HHMMSS` |

## Boilerplate Boundaries (where shared content ends and domain content begins)

| Section | Boilerplate (COPY-able) | Domain-specific (must regenerate) |
|---------|-------------------------|-----------------------------------|
| Variable Reference (31-43) | `TASK_DIR`/`TASK_FILE`/output subfolder pattern | `TASK_ID` prefix, subfolder names |
| Stage A overview (135-153) | Two-stage A/B model entirely | Phase enumeration in step 2 (triage labels) |
| A.5 review gate (273-294) | 6-criteria gate logic, "max 2 rounds" | Domain-specific check (e.g., line 283 mentions SOLUTION_RESEARCH for implementation work) |
| A.6 template triage (296-312) | Template 01 vs 02 logic | Closing line "for tech-research, the answer is almost always Template 02" |
| Stage B Execution Loop (467-483) | Entirely COPY (F1 pattern) | None |
| Prohibited Actions F2 (485-494) | Entirely COPY | "Modifying source code" rule (line 493) is research-domain; documentation skills may differ |
| F4 modification restrictions (509-521) | Entirely COPY | None |
| F5 frontmatter protocol (523-532) | Entirely COPY | None |
| Error Handling (534-540) | Entirely COPY | None |
| Critical Rules 1-3, 7-8, 10-11, 13 (1249-1273) | COPY (universal MDTM rules) | Rules 4, 6, 9, 14, 15 are research-specific (codebase as source of truth, default to Deep, gap-driven web research, doc skepticism) |
| Codebase Research Agent prompt (560-649) | Incremental File Writing block (570-589); Documentation Staleness Protocol (601-627) | Topic, files, output path; "Investigation type" enum |
| Synthesis Agent prompt (690-721) | 10 numbered rules; Incremental File Writing block | research files list, sections to produce, output path |
| Content Rules table (1219-1242) | Entirely COPY (universal writing standards) | None |

## Phase Structure (Detailed)

| Phase | Name | Activity | Parallel? | QA Gate? | Output |
|-------|------|----------|-----------|----------|--------|
| 1 | Preparation | Set status, create folder | N | N | `${TASK_DIR}` + 4 subfolders |
| 2 | Deep Investigation | Codebase research agents | YES (mandatory) | N | `research/[NN]-*.md` files |
| 3 | Completeness Verification | rf-analyst + rf-qa | YES (parallel pair) | YES (research-gate) | `qa/analyst-completeness-report.md`, `qa/qa-research-gate-report.md` |
| 4 | Web Research | External research agents | YES (mandatory) | N | `research/web-[NN]-*.md` files |
| 5 | Synthesis + QA Gate | Synthesis agents → analyst+qa | YES (mandatory) | YES (synthesis-gate) | `synthesis/synth-[NN]-*.md` + 2 QA reports |
| 6 | Assembly + Validation | rf-assembler → rf-qa → rf-qa-qualitative | NO (sequential) | YES (report-validation + report-qualitative) | `RESEARCH-REPORT-[descriptor].md` + 2 QA reports |
| 7 | Present to User & Complete | Summary + downstream skill prompt | NO | N | Updated frontmatter, optional handoff to `tech-reference` |

## Anomalies & Deviations

1. **Stage A is unusually elaborated** — 8 sub-steps (A.1–A.8) where most skills could use 3–4. This reflects the discovery-heavy nature of research vs. structured-output skills like prd/tdd.
2. **Two QA agents at Phase 6 (rf-qa structural + rf-qa-qualitative)** — most skills surveyed use only one QA pass. Tech-research adopts the recipe pipeline pattern of dual structural+qualitative review.
3. **Partitioning thresholds are explicit** (>6 research files for Phase 3, >4 synth files for Phase 5). Other skills typically don't pre-partition QA workloads.
4. **Critical Rules 14 & 15 are specific to research** — codify "documentation is not verification" as first-class concerns. PRD/TDD skills don't have this requirement.
5. **Research Quality Signals (lines 1301-1322)** — appended after Critical Rules. This trailing section is research-specific; not a canonical-29 slot.
6. **Variable Reference appears very early** (lines 31-43) — placed inside `## Why This Process Works`, not under a dedicated heading. Slight structural quirk vs. having a top-level Variables section.

## Stale Documentation Found

None. All claims in this analysis are sourced directly from `/config/workspace/IronClaude/.claude/skills/tech-research/SKILL.md` lines 1-1322 [CODE-VERIFIED]. No external documentation was consulted.

## Gaps and Questions

1. **[UNVERIFIED]** The task brief references "29 canonical sections" but the source SKILL.md does not enumerate 29 numbered sections. The actual file uses 44 distinct markdown headings. The mapping above shows 44 sections; the canonical-29 model used by skill-creator is presumably defined elsewhere (likely in `.claude/skills/skill-creator/`). Builders consuming this research should reconcile the 44→29 grouping by referring to the skill-creator's canonical section roster.
2. **[UNVERIFIED]** "L-level" mapping (L1/L2/L4/L6) is referenced in BUILD_REQUEST (lines 341-345) but the L-level definitions are not in this file — they live in MDTM template documentation. A consumer building a new skill needs the template doc to interpret these.
3. **[UNVERIFIED]** The phrase "29 canonical sections" classification (COPY/SUBSTITUTE/GENERATE) is used in the research brief but no key/legend was provided in the source skill. I have used my own definitions in the classification key above.

## Summary

`tech-research` is a discovery-heavy skill with 7 execution phases, 5 QA phases (research-gate, synthesis-gate, report-validation, report-qualitative, fix-cycle), and 9 distinct agent roles. The `TASK_ID_PREFIX` is `TASK-RESEARCH`, slug field is `TOPIC_SLUG`, and the final output is `RESEARCH-REPORT-[descriptor].md` placed inside `${TASK_DIR}`. The skill produces a 10-section research report assembled by a dedicated `rf-assembler` agent.

For skill-creator template generation: roughly **40% COPY** (Stage B execution loop, F1-F5 protocols, content rules, incremental writing protocols, documentation staleness protocol, critical rules 1-3/7-8/10-11/13), **45% SUBSTITUTE** (variable references, agent prompts with placeholder topic/path/type, validation checklists referencing domain section numbers, BUILD_REQUEST shape), and **15% GENERATE** (effective prompt examples, report structure scaffolding, synthesis mapping table, research quality signals).

**Status:** Complete
