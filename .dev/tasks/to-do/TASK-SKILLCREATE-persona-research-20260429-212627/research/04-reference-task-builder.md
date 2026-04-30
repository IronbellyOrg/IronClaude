# Research: Reference Skill Analysis — task-builder
**Investigation type:** Reference Skill Analysis
**Scope:** /config/workspace/IronClaude/.claude/skills/task-builder/SKILL.md
**Status:** Complete
**Date:** 2026-04-29
---

## File Overview

- **Source file:** /config/workspace/IronClaude/.claude/skills/task-builder/SKILL.md
- **Total lines:** 1709
- **Frontmatter:** lines 1-4 (name, description only — no `version`, no `inputs`, no `outputs`)
- **Domain:** Meta-skill — produces MDTM task files via parallel research + multi-gate QA pipeline
- **Stage model:** Stage A only (no Stage B); 13 sub-steps A.1 → A.11 (with A.8.5 and A.10.5 inserted)
- **Unique character:** This is NOT a canonical document skill (it lacks Stage B/`/task` delegation). It is the orchestrator that produces task files for OTHER skills.

## Domain Variables Extracted (Verbatim from Source)

| Variable | Value | Source Line |
|----------|-------|-------------|
| TASK_ID_PREFIX | `TASK-RF` | line 111, 729 |
| TASK_DIR pattern | `.dev/tasks/to-do/${TASK_ID}/` | line 112 |
| TASK_FILE pattern | `${TASK_DIR}${TASK_ID}.md` | line 113 |
| Multi-track folder | `TASK-RF-track-T-YYYYMMDD-HHMMSS/` | line 131, 1692 |
| Slug field name | NONE — uses TASK_ID alone (no separate slug) | n/a |
| QA phase names | `research-gate`, `task-integrity`, `task-qualitative` | lines 618, 882, 935 |
| Phase count default | Not fixed — varies (Simple: 4 phases, Discovery-Heavy: 6, Refactoring: 5, Documentation: 6, Feature Build: 7) | line 1367-1373 |
| Tier counts | Quick: 3 researchers / 0 web; Standard: 4-5 / 0-1; Deep: 6-8 / 1-2 | lines 91-94 |
| Track count range | 1-5 (default 1, max 5) | lines 226, 1661 |
| Gap-fill cycle max | 3 rounds (research gate); 2 rounds (sufficiency gate); 2 rounds each (RESEARCH_NEEDED + MALFORMED) | lines 371, 651, 859, 865 |
| Line ceiling | NOT specified anywhere in this skill | n/a |
| Research file naming | `[NN]-[topic-slug].md` (zero-padded) | line 124, 133, 1197 |
| Web research naming | `web-[NN]-[topic-slug].md` | line 125, 1233 |
| Validation requirements | "Standard project validation: lint, type-check, and build must pass." (default) | line 749 |
| Testing requirements | NONE / UNIT / INTEGRATION / E2E / ALL | line 752 |
| QA gate requirements | NONE / FINAL_ONLY / PER_PHASE | line 735 |
| Templates | `01_mdtm_template_generic_task.md` (simple), `02_mdtm_template_complex_task.md` (complex) | lines 543-544 |

## Agent Type Roster

| Agent Type | Spawned Where | Purpose |
|------------|---------------|---------|
| `general-purpose` | A.7 (researchers), A.8.5 (web), A.8 gap-fill | Research / web research / gap-fill |
| `rf-analyst` | A.8 (research gate) | Completeness verification |
| `rf-qa` | A.8 (research gate), A.10 (task integrity) | Adversarial QA gate / structural validation |
| `rf-qa-qualitative` | A.10.5 (task qualitative) | Operational viability validation |
| `rf-task-builder` | A.9 | The actual task file creation agent (recursive: this skill spawns its own namesake agent) |

All spawned with `mode: "bypassPermissions"` (verified lines 398, 581, 614, 720, 876, 927, etc.).

---

## Section-by-Section Classification (Top-Level + Sub-sections)

This skill does NOT match a clean "29 canonical sections" template. The actual top-level section count is **22**, with deep nesting under "Stage A: Task File Creation Pipeline" (13 sub-steps) and "Agent Prompt Templates" (6 sub-prompts). Below is the complete enumeration.

Classification key:
- **COPY** — boilerplate that would copy verbatim into a new skill of similar shape
- **SUBSTITUTE** — structural shell stays, but values/text get domain-specific replacement
- **GENERATE** — domain-unique content; would have to be authored from scratch for a new skill

### Top-Level Sections

| # | Title | Lines | Classification | Notes |
|---|-------|-------|----------------|-------|
| 1 | Frontmatter (YAML) | 1-4 | SUBSTITUTE | Only `name` + `description` fields. Description starts with capability statement then enumerates trigger phrases. |
| 2 | H1 Title (`# RF Task Builder`) + intro paragraphs | 6-12 | SUBSTITUTE | Three paragraphs: what it does, how it works, stage model statement. |
| 3 | `## Why This Process Works` | 14-25 | SUBSTITUTE | Multi-phase justification + 4 named failure modes (context rot, shallow coverage, hallucinated content, uncaught quality drift). Pattern reusable. |
| 4 | `## Input` | 28-83 | SUBSTITUTE | Has 4 numbered inputs, "Effective Prompt Examples" subsection, "What to Do If the Prompt Is Incomplete" subsection, "Request Triage" subsection (Scenario A/B), "Multi-Track Detection" subsection, "Relationship to Other Skills" subsection. Highly domain-shaped. |
| 5 | `## Tier Selection` | 86-103 | SUBSTITUTE | 3-tier table (Quick/Standard/Deep) with researcher counts + web agent counts. Tier rules block. |
| 6 | `## Output Locations` | 105-137 | SUBSTITUTE | Variable reference block, artifact table, multi-track path convention, file numbering convention. |
| 7 | `## Execution Overview` | 139-165 | SUBSTITUTE | Single-stage statement, 13-step enumeration of A.1-A.11, resume routing rules. |
| 8 | `## Stage A: Task File Creation Pipeline` | 167-1071 | SUBSTITUTE (parent) | Container for A.1-A.11 sub-steps. |
| 9 | `## Agent Prompt Templates` | 1074-1402 | SUBSTITUTE (parent) | Container for 6 agent prompt blocks. |
| 10 | `## Output Structure` | 1405-1486 | SUBSTITUTE | Shows the literal MDTM task file template the builder produces. Has nested `## Task Overview`, `## Key Objectives`, `## Prerequisites & Dependencies`, `## Phase 1`, `## Phase N`, `## Task Log / Notes`. These are NOT skill sections — they're inside a fenced markdown block showing OUTPUT format. |
| 11 | `## Task File Validation Checklist` | 1489-1507 | COPY-mostly | 15-item checklist. Items 4, 6, 7, 9, 10 are MDTM-specific; rest are generic. |
| 12 | `## Task File Content Rules` | 1511-1523 | COPY-mostly | 8-row Do/Don't table. MDTM-flavored. |
| 13 | `## Critical Rules (Non-Negotiable)` | 1526-1564 | SUBSTITUTE | 18 numbered rules. Rules 1, 2, 5, 6, 8 are universal; rest are domain-specific. Has "Precedence rule" footnote. |
| 14 | `## Research Quality Signals` | 1568-1591 | COPY | 3 sub-sections: Strong / Weak / When to Spawn Additional Agents. Generic to research-driven skills. |
| 15 | `## Artifact Locations` | 1594-1608 | SUBSTITUTE | 9-row table. Duplicates info from Output Locations (section 6). |
| 16 | `## Session Management` | 1612-1633 | SUBSTITUTE | Resume detection, state-to-resume-point table (7 rows), session-end notes. |
| 17 | `## Multi-Track Handling` | 1637-1697 | GENERATE | Explicitly stated (line 1639): "This section is unique to the task-builder skill — the canonical document skills don't support multi-track." Has 5 sub-sections: Track Determination, Per-Track State, Parallel Execution, Track Isolation, Naming Conventions. |
| 18 | `## Updating an Existing Task File` | 1700-1709 | COPY | 6-step generic update protocol. |

### Stage A Sub-Steps (under section 8)

| # | Title | Lines | Classification | Notes |
|---|-------|-------|----------------|-------|
| 8.1 | `### A.1: Check for Existing Task Folder` | 169-182 | SUBSTITUTE | Resume routing logic. Conditions reference domain-specific files (research-notes.md, qa-task-validation-report.md, etc). |
| 8.2 | `### A.2: Parse & Triage` | 184-237 | GENERATE | Domain-specific: GOAL/WHY/OUTPUTS/CONTEXT decomposition, Scenario A vs B, track determination, MDTM template selection table. |
| 8.3 | `### A.3: Perform Scope Discovery` | 239-305 | GENERATE | 8-topic researcher type table is the domain core. Two example assignments (handlers, feature build). Per-track scope map structure. |
| 8.4 | `### A.4: Write Research Notes File (MANDATORY)` | 307-349 | GENERATE | 7-category template (EXISTING_FILES, PATTERNS_AND_CONVENTIONS, GAPS_AND_QUESTIONS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER). Note: these 7 H2-rendered headings inside a fenced code block at lines 323/326/329/332/335/342/345 are part of the embedded template, NOT real skill sections — but `grep "^##"` picks them up. |
| 8.5 | `### A.5: Review Research Sufficiency (MANDATORY GATE)` | 351-373 | COPY-mostly | 7-item review checklist. Max-2-rounds rule. Generic gate logic. |
| 8.6 | `### A.6: Template Triage` | 375-391 | SUBSTITUTE | Template 01 vs 02 decision criteria. Domain-specific to MDTM templates. |
| 8.7 | `### A.7: Spawn Researchers` | 393-572 | GENERATE | Massive section (180 lines). Researcher prompt template with 8 topic-specific instruction blocks. This is the heart of the skill. |
| 8.8 | `### A.8: Research Quality Gate` | 574-654 | SUBSTITUTE | Parallel rf-analyst + rf-qa spawning. Two embedded prompts. Gap-fill cycle (max 3 rounds). Cross-track validation. |
| 8.9 | `### A.8.5: Optional Web Research` | 656-710 | SUBSTITUTE | Conditional spawning. Embedded web research prompt. |
| 8.10 | `### A.9: Spawn Builder` | 712-870 | GENERATE | BUILD_REQUEST template (130+ lines). Mediation flows: RESEARCH_NEEDED, MALFORMED, NEED_USER_INPUT. Independent retry counters. |
| 8.11 | `### A.10: Task File Validation` | 872-921 | SUBSTITUTE | rf-qa task-integrity prompt. 9-item validation checklist. Verdict handling. |
| 8.12 | `### A.10.5: Task File Qualitative Validation` | 923-1000 | SUBSTITUTE | rf-qa-qualitative task-qualitative prompt. Target file list extraction. Parallel partitioning for >15 items. |
| 8.13 | `### A.11: Present Results` | 1002-1071 | SUBSTITUTE | Single-track + multi-track result format templates. Overall status logic. |

### Agent Prompt Template Sub-sections (under section 9)

| # | Title | Lines | Classification | Notes |
|---|-------|-------|----------------|-------|
| 9.1 | `### Researcher Agent Prompt (general-purpose)` | 1078-1224 | GENERATE | Full self-contained prompt with all 8 topic blocks. Largely DUPLICATES content embedded in A.7. |
| 9.2 | `### Web Research Agent Prompt (general-purpose)` | 1226-1236 | COPY | Pointer back to A.8.5 with key elements summary. |
| 9.3 | `### Research Analyst Agent Prompt (rf-analyst)` | 1238-1284 | SUBSTITUTE | Full prompt. 9-item completeness checklist. |
| 9.4 | `### Research QA Agent Prompt (rf-qa — Research Gate)` | 1286-1341 | SUBSTITUTE | Adversarial stance block (repeated twice in same prompt — lines 1291, 1308). 10-item Research Gate checklist. |
| 9.5 | `### Builder Agent Prompt (rf-task-builder)` | 1343-1380 | SUBSTITUTE | Pointer to A.9 + required field list, common phase patterns table, prohibited actions. |
| 9.6 | `### Task File Validation QA Agent Prompt (rf-qa — Task Integrity)` | 1381-1402 | SUBSTITUTE | Pointer to A.10 + 9-item validation summary. |

---

## Mapping to "29 Canonical Sections" Hypothesis

The research request assumes a 29-section canonical structure. **task-builder.md does NOT exhibit a clean 29-section structure.** It has:
- 18 top-level (`##`) sections (excluding embedded-template H2s in the A.4 code block)
- 22 if you include the 4 misleading H2 captures inside fenced code blocks (lines 1433, 1437, 1443, 1450, 1464, 1475 from `## Task Overview` etc., which are output template content, not skill sections)
- 13 Stage A sub-sections (`### A.1` through `### A.11`, with A.8.5 and A.10.5)
- 6 Agent Prompt sub-sections

**Best-guess mapping to a "canonical 29" if such a list exists** — under the assumption the canonical structure is:
1. Frontmatter, 2. Title/intro, 3. Why This Process Works, 4. Input, 5. Tier Selection, 6. Output Locations, 7. Execution Overview, 8-20. Stage A.1-A.11 sub-steps (13 items), 21-26. Agent Prompt Templates (6 items), 27. Output Structure, 28. Critical Rules, 29. Artifact Locations.

That gives 29. Remaining sections in task-builder.md NOT in such a list:
- Task File Validation Checklist (line 1489)
- Task File Content Rules (line 1511)
- Research Quality Signals (line 1568)
- Session Management (line 1612)
- Multi-Track Handling (line 1637) — **explicitly unique** per line 1639
- Updating an Existing Task File (line 1700)

These 6 are LIKELY GENERATE-class, since the comment at line 1639 says "this section is unique to the task-builder skill". The other 5 may or may not be canonical depending on what "canonical" means.

[UNVERIFIED] — The "29 canonical sections" list referenced in the prompt is not enumerated anywhere in this source file. I cannot map deterministically without that reference list. See Gaps and Questions.

---

## Substitution Points & Bracketed Placeholders

Major placeholders that recur:
- `[GOAL]` / `[goal for this track]` — passed from user request
- `[YYYYMMDD-HHMMSS]` — timestamp at task folder creation
- `[T]` / `[N]` — track number / count
- `[NN]` — zero-padded sequential research file number
- `[TOPIC_TYPE]` / `[topic-slug]` — researcher topic identifier from 8-topic table
- `${TASK_ID}` / `${TASK_DIR}` / `${TASK_FILE}` — variable references (shell-style)
- `[01 or 02]` — MDTM template selection
- `[Quick / Standard / Deep]` — tier selection
- `[PASS/FAIL]` — verdict outputs
- `[CRITICAL/IMPORTANT/MINOR]` — severity ratings

Frontmatter values to substitute when porting:
- `name:` → new skill name
- `description:` → trigger phrase enumeration

## Boilerplate Boundaries

Sections that are LARGELY universal across rf skills (high COPY likelihood):
- Why This Process Works (lines 14-25) — failure-mode framing is reusable
- Critical Rules 1, 2, 5, 6, 8 (lines 1528, 1530, 1536, 1538, 1542) — universal
- Research Quality Signals (lines 1568-1591) — generic to research skills
- Updating an Existing Task File (lines 1700-1709) — generic
- ESCALATION blocks (lines 456-457, 610, 639, 674-677, 804-810, 890-893, 978-981, 1099-1102, 1252-1254, 1304-1306) — verbatim across all spawned agents
- Incremental Writing Protocol (lines 437-450, 679-682, 819-832, 1196-1209) — verbatim
- Adversarial Stance block (lines 621, 878, 895, 929, 958, 1291, 1308, 1386) — verbatim, repeated 8 times in source

Sections that are DOMAIN-CORE (high GENERATE likelihood):
- 8-topic researcher type table (A.3, lines 258-267)
- Topic-specific instruction blocks (A.7 + 9.1, 8 blocks each)
- BUILD_REQUEST template (A.9, lines 718-848)
- 7-category research notes template (A.4, lines 313-347)
- 9-item Task Validation checklist (A.10, lines 898-906)
- 10-item Research Gate checklist (9.4, lines 1323-1333)
- Multi-Track Handling section entirely (1637-1697)

## Verbatim Repeated Content (DRY violations in source)

The skill repeats large blocks verbatim:
1. **Researcher prompt** appears in A.7 (lines 405-468) AND in 9.1 (lines 1082-1222) — full topic-specific blocks duplicated
2. **Adversarial Stance** boilerplate appears 8+ times (see line list above)
3. **ESCALATION** boilerplate appears 10+ times
4. **Incremental Writing Protocol** appears 4 times
5. **8-topic instruction blocks** appear in both A.7 and 9.1

Implication for skill-creator: when generating a skill, this pattern is the established convention — duplication for self-contained agent prompts is acceptable.

## Phase Structure / L-Level Mapping

The task-builder skill itself does NOT use L1-L6 phase labeling. It uses:
- **Stage A** with sub-steps A.1 through A.11 (13 sub-steps including A.8.5 and A.10.5)
- The OUTPUT it produces (the MDTM task file) uses Phase 1 ... Phase N labeling per the template at lines 1450, 1464

L-level handoffs are referenced ONLY in the Template & Examples instruction block (line 549: "L1-L6 handoff patterns for template 02") — meaning L-levels apply to MDTM template 02, not to this skill's own structure.

QA gate placement in the skill's own pipeline:
- **Gate 1 (research-gate):** A.8 — after researchers, before builder
- **Gate 2 (sufficiency review):** A.5 — between A.4 (research notes) and A.7 (spawn) — orchestrator self-review, no spawned agent
- **Gate 3 (task-integrity):** A.10 — after builder, structural validation
- **Gate 4 (task-qualitative):** A.10.5 — after structural validation, operational viability

## Deviations from Skill Template

Items that may deviate from a hypothetical canonical skill template:
1. **No `## Outputs` section** as a top-level header — outputs are documented inside `## Output Locations` (artifact table) and `## Output Structure` (rendered MDTM task file template).
2. **No `## Critical Rules` for the skill itself separated from the agent rules** — section 13 conflates skill-level rules and rules-the-task-file-must-encode (rules 16, 17, 18 specifically).
3. **`## Multi-Track Handling`** is explicitly flagged as unique to this skill (line 1639).
4. **Stage A only** — no Stage B (line 12, 141): "There is no Stage B".
5. **Sub-step numbering uses decimals (A.8.5, A.10.5)** — suggesting these were inserted after the original numbering. This implies the canonical structure may have used 11 steps and these are extensions.
6. **Two top-level sections that overlap with Stage A content:** Output Locations (sect 6) and Artifact Locations (sect 15) duplicate the same artifact table.
7. **No top-level `## Examples` section** in the conventional sense — examples are embedded inside Input subsections.

## Output Location for Generated Artifacts

- Output base: `.dev/tasks/to-do/`
- Task folder: `${TASK_DIR}` = `.dev/tasks/to-do/TASK-RF-YYYYMMDD-HHMMSS/`
- Task file: `${TASK_DIR}${TASK_ID}.md`
- Research artifacts: `${TASK_DIR}research/[NN]-[topic].md`
- QA artifacts: `${TASK_DIR}qa/[report-name].md`
- Multi-track: `${TASK_DIR}` = `.dev/tasks/to-do/TASK-RF-track-T-YYYYMMDD-HHMMSS/`

---

## Validation Requirements (Skill-Level vs Output-Level)

### Validation that THIS SKILL performs (on its own output):
1. **A.5 sufficiency gate** — orchestrator self-review of research-notes.md (7 items)
2. **A.8 research gate** — rf-analyst (9-item checklist) + rf-qa (10-item checklist) in parallel
3. **A.10 task integrity gate** — rf-qa (9-item checklist), `fix_authorization: true`
4. **A.10.5 task qualitative gate** — rf-qa-qualitative, `fix_authorization: true`, target file list verified ALL (no spot-checking, line 931, 942)

### Validation requirements ENCODED in the generated task file (skill outputs):
- `QA_GATE_REQUIREMENTS`: NONE / FINAL_ONLY / PER_PHASE (line 735-742)
- `VALIDATION_REQUIREMENTS`: lint, type-check, build (default, line 749)
- `TESTING_REQUIREMENTS`: NONE / UNIT / INTEGRATION / E2E / ALL (line 752)

These are passed via BUILD_REQUEST to the rf-task-builder agent and become checklist items in the OUTPUT task file. They are not validation the skill itself runs.

---

## Stale Documentation Found

No internal contradictions or stale doc references identified within the SKILL.md itself. The file is internally consistent. All rules in section 13 (Critical Rules) align with the procedure described in Stage A. The Artifact Locations table at line 1594-1608 matches the Output Locations table at line 120-129.

[CODE-VERIFIED] All cross-references within the file (e.g., "see A.8.5 above", "embedded in A.9 above", "from your agent definition") are internally coherent — they point to sections that actually exist.

[UNVERIFIED] References to external files I did not open:
- `.claude/templates/workflow/01_mdtm_template_generic_task.md` (line 543, 1172) — referenced as the simple-task MDTM template
- `.claude/templates/workflow/02_mdtm_template_complex_task.md` (line 544, 1171) — referenced as the complex-task MDTM template
- `.claude/agents/rf-task-builder.md` (line 82) — referenced as the standalone agent file the skill spawns
- `rf-analyst`, `rf-qa`, `rf-qa-qualitative` agent definitions — referenced as `subagent_type` values; agent files not opened during this research

These are out-of-scope for this reference-skill investigation but listed here for completeness.

---

## Gaps and Questions

1. **The "29 canonical sections" structure is not defined within this source file.** The investigation prompt assumes a 29-section canonical template exists. Without that reference list, my classification is based on the actual section headings present (18 top-level + 13 Stage A subs + 6 agent-prompt subs). Recommend the team-lead provide the canonical section list, OR confirm that "29 sections" should be inferred from one of the other reference skills (likely tech-reference or prd, which the prompt suggests are the canonical models).

2. **Frontmatter has no `version`, `inputs`, or `outputs` keys.** Only `name` and `description`. If skill-creator's 29-section template requires those, this skill DEVIATES from the template. [CODE-VERIFIED via lines 1-4 of source]

3. **Two H2-level sections inside fenced code blocks** (lines 323-345 = the 7-category research notes template; lines 1433-1485 = the rendered MDTM task file template) get picked up by `grep "^##"` but are NOT skill sections — they're embedded output schemas. Any tool that classifies sections must handle this.

4. **Stage A.8.5 and A.10.5 use decimal sub-step numbering**, suggesting they were inserted retroactively. If the canonical template uses integer-only numbering, these are extensions. Worth confirming whether canonical structure permits decimal sub-steps.

5. **No explicit line-ceiling guidance in this skill.** If the 29-section template specifies a line ceiling (e.g., "skill files should stay under 1500 lines"), this skill VIOLATES it at 1709 lines. The duplicated researcher prompt (A.7 + 9.1) accounts for ~150 lines that could be DRY'd.

6. **Multi-Track Handling explicitly self-flags as unique** (line 1639) — confirming this skill is NOT a fully canonical reference for the 29-section structure. Researchers using task-builder.md as a "reference skill" should understand it has at least one section that other skills will not have.

---

## Summary

The task-builder skill is a meta-orchestrator that produces MDTM task files via parallel research → multi-gate QA → builder spawn. It is NOT a clean canonical skill — it has Stage A only (no /task delegation), uses decimal sub-step numbering, and contains an explicitly-unique Multi-Track Handling section. Its 18 top-level sections + 13 Stage A subs + 6 agent-prompt subs do not map cleanly onto a 29-section canonical structure without additional reference material.

**Most COPY-able boilerplate:** ESCALATION blocks, Adversarial Stance blocks, Incremental Writing Protocol, Research Quality Signals, Critical Rules 1/2/5/6/8.

**Most GENERATE-required content:** A.7 researcher topic taxonomy and topic-specific blocks, A.9 BUILD_REQUEST template, Multi-Track Handling section, A.4 7-category research notes template.

**Domain variables a skill-creator template would need to substitute:** TASK_ID_PREFIX (`TASK-RF`), output base (`.dev/tasks/to-do/`), agent type roster (5 types), tier counts (3-8 researchers, 0-2 web), template references (01/02), gate names (research-gate / task-integrity / task-qualitative), gap-fill cycle limits (3 / 2 / 2+2).

**Status:** Complete




