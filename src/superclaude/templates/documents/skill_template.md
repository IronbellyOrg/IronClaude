<!-- CLASSIFICATION: SUBSTITUTE -->
---
name: [skill-name]
description: "[One sentence: what it does. When to use it. Trigger phrases.]"
---

<!-- CLASSIFICATION: GENERATE -->
# [Skill Display Name]

[One paragraph describing what this skill does and its role in the RF ecosystem]

<!-- CLASSIFICATION: SUBSTITUTE -->
**How it works:** The skill performs initial scope discovery, then invokes the `/task-builder` skill to create an MDTM task file encoding all [domain activity — e.g., investigation, documentation, audit] phases. The skill then delegates execution to the `/task` skill, which processes each checklist item via the F1 loop. If context compresses or the session restarts, the skill re-reads the task file and resumes from the first unchecked item.

<!-- TEMPLATE GUIDANCE: Include ONE of the following patterns depending on whether the skill produces a document from a project template or generates a standalone output. -->
[If document-based: "The output always follows the project template at [template path]. The template is the schema — every [doc type] must conform to it."]
[If standalone: "This skill fills the gap between [Skill A] ([verb A]) and [Skill B] ([verb B]). [This Skill] **[verb this]**."]

<!-- CLASSIFICATION: SUBSTITUTE -->
## Why This Process Works

[Doc type plural — e.g., "Technical investigations", "Product requirements", "Technical references"] fail when they rely on assumptions, memory, or [failure mode — e.g., "surface-level reading", "outdated documentation"]. This skill forces every claim through codebase verification — parallel agents read actual source files, trace actual [trace target — e.g., "data flows", "imports", "capabilities"], and document actual behavior with file paths and line numbers.

The MDTM task file provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off.

The multi-phase structure ([phase list — e.g., "scope discovery → deep investigation → **analyst verification** → ..."]) prevents four common failure modes:
- **Context rot** — By isolating each investigation topic in its own subagent with its own output file, no single agent needs to hold the entire investigation in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning many parallel agents (each focused on one slice), the investigation goes deep on every aspect simultaneously rather than skimming across everything sequentially.
- **Hallucinated [domain noun — e.g., "recommendations", "content", "requirements", "design details", "procedures"]** — By separating research (what exists) from synthesis (what it means) from assembly (the final report), each phase can be verified independently. Synthesis agents only work from verified research files, not from memory or inference.
- **Uncaught quality drift** — Dedicated [agent names — e.g., "`rf-analyst`, `rf-qa`, and `rf-qa-qualitative`"] agents provide independent verification at [number] critical gates: [gate descriptions — e.g., "after research (completeness + evidence quality), after synthesis (accuracy + structure), and after assembly (structural report validation + qualitative content review)"]. This follows the same analyst→QA pattern used in the recipe pipeline, adapted for [domain] outputs. The QA agents assume everything is wrong until independently verified — zero-trust verification prevents rubber-stamping.

The [artifact type — e.g., "research artifacts"] persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and feed directly into [downstream target — e.g., "downstream skills like `tech-reference`" or "the assembled [doc type]"].

<!-- CLASSIFICATION: SUBSTITUTE -->
### Variable Reference

Every invocation creates a self-contained folder. All paths below are relative to this folder:

```
TASK_ID:     [TASK-PREFIX]-<subject>-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/
SYNTHESIS:   ${TASK_DIR}synthesis/
QA:          ${TASK_DIR}qa/
REVIEWS:     ${TASK_DIR}reviews/
```

<!-- TEMPLATE GUIDANCE — Placeholder conventions used in this template:
  - [BRACKETED WORDS] = substitute a domain-specific noun or phrase (e.g., [domain noun], [TASK-PREFIX])
  - <angle brackets> = slot in a computed or derived value (e.g., <subject>, <timestamp>)
  - ${VAR_NAME} = variable reference from the Variable Reference table above
  - [GENERATE ...] = fully custom content the skill author writes from scratch
  - [SUBSTITUTE ...] = replace with skill-specific equivalent of the example shown
  - [COPY ...] = copy verbatim from the referenced source
-->
<!-- TEMPLATE GUIDANCE: TASK_PREFIX values follow the pattern TASK-KEYWORD (e.g., TASK-RESEARCH, TASK-TECHREF, TASK-PRD, TASK-TDD, TASK-CLEANUP, TASK-OPSGUIDE, TASK-README). Choose a short, unique prefix for the skill. -->
<!-- TEMPLATE GUIDANCE: <subject> is a kebab-case slug (1-3 words, ~30 char soft cap) derived from the user's GOAL field describing the task topic (e.g., "locomotion-params", "wizard-state", "auth-middleware"). If the goal is too broad to summarize, use "general". This matches the convention in all existing skills (e.g., TASK-RESEARCH-locomotion-params-20260408-140000). -->

---

<!-- CLASSIFICATION: SUBSTITUTE structure + GENERATE items -->
## Input

The skill needs [count — e.g., four] pieces of information to produce [output description — e.g., an actionable report, a thorough technical reference]. The first is mandatory; the rest are optional but dramatically improve output quality.

1. **[Input 1 name — MANDATORY]:** [What the user must provide. E.g., WHAT to investigate, WHAT feature to document]

2. **[Input 2 name — optional]:** [Second piece of context. E.g., WHY/problem statement, related PRD]

3. **[Input 3 name — optional]:** [Third piece. E.g., WHERE to focus, directory scope]

4. **[Input 4 name — optional]:** [Fourth piece. E.g., output type preference, tier selection]

<!-- TEMPLATE GUIDANCE: Item 1 is always mandatory. Items 2-4 improve quality but aren't blockers. The first item typically answers WHAT, item 2 answers WHY, item 3 answers WHERE, item 4 answers HOW/FORMAT. -->

<!-- CLASSIFICATION: GENERATE -->
### Effective Prompt Examples

**Strong — [description, e.g., all four pieces present]:**
> [Example prompt showing strong usage with all input fields provided]

**Strong — [description, e.g., clear question + scope + output type]:**
> [Example showing clear goal with some optional fields]

**Weak — [weakness, e.g., topic only]:**
> [Example showing minimal input that will work but produce broader results]

**Weak — [weakness, e.g., no "why"]:**
> [Example showing missing context]

<!-- TEMPLATE GUIDANCE: Provide 2-3 strong examples and 1-2 weak examples. Strong examples demonstrate all input pieces. Weak examples show what happens with minimal input. -->

<!-- CLASSIFICATION: SUBSTITUTE -->
### What to Do If the Prompt Is Incomplete

If the user provides only a [vague input type — e.g., topic name, feature name] or a vague request, **do NOT proceed immediately**. Ask the user to clarify using this template:

> I can [skill action — e.g., investigate, document, audit] [topic] for you. To make the [output type — e.g., report, reference, PRD] focused and [quality adjective — e.g., actionable, comprehensive], can you help me with:
>
> 1. **[Question 1 — maps to mandatory Input item #1]**
> 2. **[Question 2 — maps to optional Input item #2]**
> 3. **[Question 3 — maps to optional Input item #3]**
> 4. **[Question 4 — maps to optional Input item #4]**

Proceed once you have at least #1 answered clearly. Items #2-[N] improve quality but aren't blockers.

<!-- TEMPLATE GUIDANCE: Questions should map 1:1 to the Input items above. Question 1 maps to the mandatory input. The clarification template format (blockquote with numbered items) is BOILERPLATE — only the question text is domain-specific. -->

<!-- CLASSIFICATION: SUBSTITUTE -->
## Depth Tiers

[Match instruction — e.g., "Match depth tier to the scope of the request"]. **Default to [default tier — e.g., Standard]** unless [simple case].

| Tier | When | Codebase Agents | Web Agents | [Metric — e.g., Report Depth] |
|------|------|-----------------|------------|------|
| **Quick** | [Quick criteria] | [count] | [count] | [metric value] |
| **Standard** | [Standard criteria — this is the default] | [count] | [count] | [metric value] |
| **Deep** | [Deep criteria] | [count] | [count] | [metric value] |

**Tier selection rules:**
- If in doubt, pick [default tier]
- If the user says "thorough", "comprehensive", or "deep dive" — always [top tier]
- Only use [bottom tier] for [simple case]
- If the scope spans [complexity indicator] — always [top tier]

<!-- TEMPLATE GUIDANCE: Standardize on Quick/Standard/Deep tier names. Default tier is Standard for most doc skills, Deep for tech-research. Last column metric varies: "Report Depth" (tech-research, repo-cleanup), "Target Lines" (tech-reference, prd, tdd), "Sections Required" (readme). -->

<!-- CLASSIFICATION: SUBSTITUTE structure + GENERATE artifact rows -->
## Output Locations

All persistent artifacts go [location description — e.g., "into the task folder created at invocation time"].

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}${TASK_ID}.md` |
| Research notes | `${TASK_DIR}research/research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| [Domain-specific artifact 1 — e.g., Gap log] | `[path]` |
| [Domain-specific artifact 2 — e.g., Analyst reports] | `[path]` |
| [Domain-specific artifact 3 — e.g., QA reports] | `[path]` |
| [Final output — e.g., Research report, Technical reference] | `[final output path]` |

<!-- TEMPLATE GUIDANCE: The first 5 rows (MDTM Task File through Synthesis files) are BOILERPLATE — identical across all skills. Remaining rows are domain-specific: gap logs, analyst/QA reports, final output documents. Add or remove domain rows as needed. -->

**File numbering convention:** All research, web, and synthesis files use zero-padded sequential numbers: `01-`, `02-`, `03-`, etc. This ensures correct ordering when listing files.

Check for existing task folders [match pattern — e.g., `TASK-RESEARCH-*`] in `.dev/tasks/to-do/` before creating new ones — if prior research exists on the same [subject — e.g., topic, feature, system], read it first and build on it.

<!-- CLASSIFICATION: SUBSTITUTE -->
## Execution Overview

The skill operates in two stages:

**Stage A — Scope Discovery & Task File Creation (before the task file exists):**
1. [Step 1 — e.g., Check for an existing task file or research directory]
2. [Step 2 — e.g., Parse the user's request — triage into Scenario A vs B]
3. [Step 3 — e.g., Perform scope discovery — map relevant files/directories]
4. [Step 4 — e.g., Write scope discovery results to research notes file]
5. [Step 5 — e.g., Review research sufficiency — mandatory self-review gate]
6. [Step 6 — e.g., Triage template selection — Template 01 vs 02]
7. [Step 7 — e.g., Write BUILD-REQUEST.md and invoke /task-builder skill]

**Stage B — Task File Execution (after the task file exists):**
8. Delegate to the `/task` skill, which processes each checklist item via the F1 loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT)
9. Each checklist item is a self-contained prompt — no prior context needed

<!-- TEMPLATE GUIDANCE: Include a "Phase names within the task file:" list mapping task file phases to skill workflow steps. This is GENERATE content — each skill defines its own phase names. Example:
Phase 1: Preparation
Phase 2: Deep Investigation
Phase 3: Quality Gate (rf-analyst + rf-qa)
Phase 4: [Web Research — if applicable]
Phase 5: Synthesis
Phase 6: Synthesis Quality Gate
Phase 7: Assembly + Final Validation + Present Results
-->

**Phase names within the task file:**
- Phase 1: [Phase 1 name and purpose]
- Phase 2: [Phase 2 name and purpose]
- Phase 3: [Phase 3 name and purpose]
- [Additional phases as needed — most skills use 6-7 phases]

If a task file already exists for this [subject — e.g., topic, feature, component] (from a previous session), skip Stage A and invoke `/task` with the existing task file path — it resumes from the first unchecked item.

---

<!-- CLASSIFICATION: BOILERPLATE -->
## Stage A: Scope Discovery & Task File Creation

<!-- CLASSIFICATION: SUBSTITUTE -->
### A.1: Check for Existing Task File

Before creating a new task folder, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `[TASK-PREFIX]-*/` folder [relation clause — e.g., related to this topic, matching this feature].
2. **If folder found AND task file exists inside it** (`${TASK_DIR}[TASK-PREFIX]-*.md`):
   a. If unchecked `- [ ]` items exist → invoke the `/task` skill with the task file path (Stage B).
   b. If all items are checked → inform user that [work type — e.g., research, documentation, the tech reference] is already complete, offer to [alternative — e.g., re-run or build on existing research].
3. **If folder found but NO task file inside:**
   a. If `${TASK_DIR}research/research-notes.md` exists with `Status: Complete` → skip to A.5 (review sufficiency).
   b. If `${TASK_DIR}research/research-notes.md` exists with `Status: In Progress` → read it, resume A.3 scope discovery from where it left off.
   c. If no `research-notes.md` → continue with A.3 but use the existing folder.
4. **If no folder found** → continue with A.2.

<!-- TEMPLATE GUIDANCE: This 4-item branching tree is IDENTICAL across all existing skills. Only the nouns in square brackets and the relation clause change per skill. The branching logic and all 6 logical paths MUST be preserved exactly. -->

<!-- CLASSIFICATION: SUBSTITUTE structure + GENERATE parsed fields -->
### A.2: Parse & Triage [section suffix — e.g., "the Research Question", "the PRD Request", or empty]

Break the [request type — e.g., research question, documentation request, PRD request] into structured components:

- **GOAL**: What specifically needs to be [verb — e.g., investigated, documented, specified] ([context — e.g., the research question, the feature to document])
- **WHY**: What the user wants to do with the findings ([examples — e.g., decision, implementation plan, understanding, feasibility])
- **WHERE**: Specific directories, files, or subsystems to focus on
- [Additional domain-specific field — e.g., **OUTPUT_TYPE**, **FEATURE_SLUG**, **PRODUCT_SLUG**]: [Description]
- [Additional domain-specific field — e.g., **TOPIC_SLUG**]: [Description — e.g., A kebab-case identifier for the task directory]

<!-- TEMPLATE GUIDANCE: The first 3 fields (GOAL, WHY, WHERE) are BOILERPLATE across all skills — only the parenthetical context changes. Fields 4+ are domain-specific GENERATE content. Most skills have 4-5 fields total. -->

<!-- TEMPLATE GUIDANCE: The Effective Prompt Examples subsection (under Input) and A.2 (Parse & Triage) serve DIFFERENT purposes and must use DIFFERENT examples to avoid redundancy.
  - The Effective Prompt Examples subsection shows what users might say — these are TRIGGER/RECOGNITION examples that help users craft good prompts and help the skill identify when it should activate. The Effective Prompt Examples subsection answers: "What does a good invocation look like?"
  - A.2 shows how the skill breaks those inputs into structured fields (GOAL, WHY, WHERE, etc.) — these are PARSING examples that demonstrate the triage decision. A.2 answers: "Once triggered, how does the skill interpret and classify the input?"
  - The Scenario A example here MUST use a DIFFERENT prompt than the Effective Prompt Examples subsection's strong examples. If the Effective Prompt Examples subsection shows "Research how the wizard state management works across all 14 Zustand slices," A.2's Scenario A should use a distinct explicit prompt to demonstrate parsing without repeating it.
  - The Scenario B example should show a genuinely vague input that requires broad scope discovery — this naturally differs from the Effective Prompt Examples subsection's weak examples because the focus is on how the skill handles ambiguity in its triage logic, not on teaching the user to write better prompts. -->

**Triage into Scenario A or B:**

**Scenario A — Explicit request:** User provided most of: [explicit list — e.g., goal, source locations, output expectations, specific technical question].
Example: "[Scenario A example prompt showing explicit, detailed request with file paths and specific goals — MUST differ from the Effective Prompt Examples subsection's strong examples to avoid redundancy]"
→ Scope discovery confirms details and fills minor gaps. Lighter exploration.

**Scenario B — Vague request:** User provided a [minimal input — e.g., goal, topic name, feature name] but few specifics.
Example: "[Scenario B example prompt showing minimal/vague request]"
→ Scope discovery does broad exploration to map what exists, identify subsystems, and plan [domain activity — e.g., investigation assignments, documentation sections].

**Do NOT interrogate the user with a list of questions.** Proceed with what you have and let scope discovery figure out the rest from the codebase. Only ask the user [ask condition — e.g., "(via `AskUserQuestion`) if there's a genuine ambiguity about **intent** that can't be inferred from the codebase", "if the request is so ambiguous that two valid interpretations would produce completely different documents"].

<!-- TEMPLATE GUIDANCE: The Scenario A/B triage structure and the "Do NOT interrogate" closing are BOILERPLATE — identical pattern across all existing skills. Only the bracketed nouns, example prompts, and ask condition vary per skill. -->

<!-- CLASSIFICATION: SUBSTITUTE structure + GENERATE discovery targets -->
### A.3: Perform Scope Discovery

Use Glob, Grep, and codebase-retrieval to map the [domain — e.g., problem, feature, product, system] space. This must happen BEFORE building the task file so the builder can enumerate specific [assignment type — e.g., investigation assignments, documentation sections, requirement areas].

**Adjust depth by scenario:**
- **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, scan for related code, identify gaps in what the user specified.
- **Scenario B**: Broad discovery — scan the full codebase for anything touching the [subject — e.g., topic, feature, component], map all relevant subsystems, identify documentation, count files.

<!-- TEMPLATE GUIDANCE: The "Adjust depth by scenario" block above (both bullets) is VERBATIM across all existing skills. Do not modify the bullet text. -->

Discover:
- [Discovery target 1 — e.g., All files, directories, and plugins that touch the topic]
- [Discovery target 2 — e.g., Existing documentation covering related areas]
- [Discovery target 3 — e.g., Code patterns, classes, functions, and APIs involved]
- [Discovery target 4 — e.g., External integration points (frameworks, engines, third-party systems)]
- [Discovery target 5 — e.g., Count of relevant files and subsystems]

<!-- TEMPLATE GUIDANCE: Discovery targets are GENERATE content — each skill defines domain-specific steps. tech-research has 5 generic "Discover:" bullets. tech-reference has 6 numbered steps including "Check for existing stub." prd adds "User-facing flows, interaction patterns." -->

Based on the discovery:
- Select depth tier (default: [default tier — e.g., Deep, Standard])
- Plan [assignment type — e.g., research assignments, documentation sections] — divide the [work — e.g., investigation, documentation] into specific topics, each becoming a subagent assignment
- Plan web research topics (from identified gaps)
- Determine the synthesis file mapping

**Research assignment types** (use as many as the [subject] requires):

| Type | Purpose | What the Agent Does |
|------|---------|-------------------|
| **Code Tracer** | Understand how code actually works | Read implementations, trace data flow, follow imports, document behavior |
| **Doc Analyst** | Extract context from existing documentation | Read docs, **cross-validate every architectural claim against actual code** (see Documentation Staleness Protocol below), note discrepancies and stale content, extract relevant context |
| **Integration Mapper** | Identify connection points | Map APIs, extension points, plugin interfaces, service boundaries, config surfaces |
| **[Domain-specific type 1 — e.g., Pattern Investigator, Feature Analyst, Design Pattern Analyst]** | [Purpose] | [What the agent does] |
| **[Domain-specific type 2 — e.g., Architecture Analyst, UX Investigator]** | [Purpose] | [What the agent does] |

<!-- TEMPLATE GUIDANCE: The first 3 rows (Code Tracer, Doc Analyst, Integration Mapper) are BOILERPLATE — identical across all existing skills. Rows 4+ are domain-specific GENERATE content. Most skills have 4-5 types total. -->

Create the task folder: `.dev/tasks/to-do/[TASK-PREFIX]-<subject>-YYYYMMDD-HHMMSS/` with subfolders `research/`, `synthesis/`, `qa/`, `reviews/`

**Optional — spawn rf-task-researcher for complex scope discovery:**

If scope discovery needs deeper context (e.g., Scenario B with a large unknown codebase area, or Scenario A where the specified directories contain deep nested structures), spawn an `rf-task-researcher` subagent. Pass it a RESEARCH_REQUEST describing what to explore. It will write research notes to a file. You then use those notes as input for A.4.

<!-- CLASSIFICATION: SUBSTITUTE structure + GENERATE category names -->
### A.4: Write Research Notes File (MANDATORY)

Write the scope discovery results to a structured research notes file at `${TASK_DIR}research/research-notes.md`. This file is what the builder reads — NOT inline content in the BUILD_REQUEST.

**Format:**

```markdown
# Research Notes: [SUBJECT]

**Date:** [today]
**Scenario:** [A or B]
**Depth Tier:** [TIER_NAMES]

## EXISTING_FILES
[List all files, directories, and subsystems discovered during scope discovery. Include file paths, line counts, and brief descriptions.]

## PATTERNS_AND_CONVENTIONS
[Document coding patterns, naming conventions, architectural patterns, and style conventions observed in the relevant codebase areas.]

## [DOMAIN_CATEGORY]
[Domain-specific analysis category. Examples: SOLUTION_RESEARCH (tech-research), FEATURE_ANALYSIS (tech-reference, prd), DESIGN_CONTEXT (tdd). Content describes domain-relevant findings from scope discovery.]

## RECOMMENDED_OUTPUTS
[List the specific output files the task should produce, with paths and descriptions.]

## SUGGESTED_PHASES
[Propose the phase structure for the MDTM task file based on what scope discovery revealed about complexity and dependencies.]

## TEMPLATE_NOTES
[Notes about which MDTM template to use, any template customizations needed, and references to relevant project templates.]

## AMBIGUITIES_FOR_USER
[Document any ambiguities, unclear requirements, or decisions that need user input. These become Open Questions in the task file if unresolved.]
```

<!-- TEMPLATE GUIDANCE: The 3rd category (marked [DOMAIN_CATEGORY]) varies per skill: SOLUTION_RESEARCH (tech-research), FEATURE_ANALYSIS (tech-reference, prd), DESIGN_CONTEXT (tdd), or a batch-focused category (repo-cleanup). The 6 shared categories (EXISTING_FILES, PATTERNS_AND_CONVENTIONS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER) are BOILERPLATE across all skills. Only the domain category name and its content description are GENERATE content. -->

<!-- CLASSIFICATION: SUBSTITUTE -->
### A.5: Review Research Sufficiency (MANDATORY GATE)

**You MUST review the research notes before spawning the builder.** This is a quality gate — do NOT skip it.

Read `${TASK_DIR}research/research-notes.md` and evaluate:

1. [Evaluation criterion 1 — e.g., Are the EXISTING_FILES comprehensive enough to assign investigation topics?]
2. [Evaluation criterion 2 — e.g., Are the PATTERNS_AND_CONVENTIONS specific enough to guide agents?]
3. [Evaluation criterion 3 — domain-specific, e.g., Are investigation assignments concrete enough?]
4. [Evaluation criterion 4 — domain-specific, e.g., Is the synthesis mapping clear?]
5. [Evaluation criterion 5 — e.g., Are there any documentation-staleness risks flagged?]

<!-- TEMPLATE GUIDANCE: Criteria 1, 2, 5 and the doc-staleness criterion are shared across all skills. Criteria 3-4 are domain-specific GENERATE content. tech-research uses "Are investigation assignments concrete enough?" / "Is the synthesis mapping clear?". tech-reference uses "Are all major subsystems identified?" / "Are integration points mapped?". prd adds "Are stakeholder segments and user personas identified?". -->

**If sufficient** -> proceed to A.6 (template triage).

**If insufficient** -> either:
- Do additional scope discovery yourself and update the research notes file, OR
- Spawn an rf-task-researcher subagent with specific feedback about what's missing, then re-review

**Maximum 2 gap-fill rounds.** After 2 rounds, proceed with what's available and note remaining gaps in the research notes AMBIGUITIES_FOR_USER section.

Do NOT proceed to the builder with incomplete research notes. The builder cannot explore the codebase effectively — it relies on what you provide.

<!-- CLASSIFICATION: COPY + SUBSTITUTE -->
### A.6: Template Triage

Determine which MDTM template the task builder should use:

**Use Template 02 (Complex Task) when the work involves:**
- Discovery before building (investigating unknown areas)
- Parallel subagent spawning
- Multiple phases with different activities (research, synthesis, assembly)
- Review/validation steps
- Conditional flows based on findings

**Use Template 01 (Generic Task) when the work involves:**
- Simple, sequential file creation
- Straightforward execution with no discovery
- Single-pass operations

**For [skill-name], the answer is almost always Template 02** — [rationale — e.g., the skill requires discovery, multi-phase synthesis, and quality gates before producing output].

<!-- TEMPLATE GUIDANCE: The Template 02 and Template 01 criteria bullets above are VERBATIM COPY from the reference skill — do not modify them. Only the final recommendation sentence (with the [skill-name] and [rationale] placeholders) is SUBSTITUTE content. -->

<!-- CLASSIFICATION: SUBSTITUTE wrapper + GENERATE content -->
### A.7: Build the Task File

Write the BUILD_REQUEST to a file at `${TASK_DIR}BUILD-REQUEST.md`, then invoke the `/task-builder` skill. The task-builder reads the BUILD_REQUEST file, performs quality gates (rf-analyst + rf-qa), spawns the rf-task-builder agent to create the MDTM task file, and runs structural validation and qualitative validation internally. No manual verification step is needed — task-builder handles all validation and mediation.

**Step 1: Write `${TASK_DIR}BUILD-REQUEST.md`** using the Write tool with the following content:

```
# BUILD REQUEST

Source: skill-delegated
Calling Skill: [skill-name]
Task Directory: ${TASK_DIR}
Research Notes: [${TASK_DIR}research/research-notes.md OR ${TASK_DIR}research-notes.md — pick per skill convention]
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: [Goal text — GENERATE per skill. Pattern: "Create/Conduct a [doc_type_description] for [PLACEHOLDER] ... The [doc_type] will be written to [OUTPUT_PATH]." See reference skills for examples.]

WHY: [WHY — what prompted this work and what the output will be used for]

TASK_ID_PREFIX: [TASK-PREFIX — e.g., TASK-RESEARCH, TASK-PRD, TASK-TDD, TASK-TECHREF, TASK-OPSGUIDE, TASK-README, TASK-CLEANUP]

TEMPLATE: [01 or 02 — skill selects:
  01 = simple file creation, straightforward execution
  02 = needs discovery, testing, review, conditional flows, or aggregation]

[Domain-specific slug fields — GENERATE per skill. Examples:
  PRODUCT_SLUG (prd), COMPONENT_SLUG (tdd), FEATURE_SLUG (tech-reference),
  PRD_REF (tdd), PRD_SCOPE (prd), MODE (repo-cleanup),
  TECH_REF (readme), TEMPLATE_PATH, OUTPUT_PATH, PROHIBITED_ACTIONS]

DOCUMENTATION STALENESS WARNINGS:
[If scope discovery found any documentation that contradicts actual code, list the
specific claims and contradictions here. If none found during scope discovery, write:
"None found during scope discovery. Phase 2 agents will perform full documentation
cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags."]
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
[GENERATE per skill — each phase maps to a section of the skill's workflow. Example from tech-research:
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase and write findings files to ${TASK_DIR}research/
- Phase 3 (Completeness Verification): L4 Review/QA — spawn rf-analyst + rf-qa as sequential quality gate
- Phase 4 (Web Research): L1 Discovery — agents explore external sources and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — agents read research files and produce report sections, then QA gate
- Phase 6 (Assembly & Validation): L6 Aggregation — rf-assembler consolidates, then structural + qualitative QA
Customize phase names, L-level mappings, and descriptions for the skill's specific workflow.]

QA_GATE_REQUIREMENTS: PER_PHASE
  Gate 1: Research Completeness (Phase 3) — rf-analyst (completeness-verification) + rf-qa (research-gate) in parallel, max 3 fix cycles, partitioning >6 files.
  Gate 2: Synthesis Quality (Phase 5) — rf-analyst (synthesis-review) + rf-qa (synthesis-gate, fix_authorization: true) in parallel, max 2 fix cycles, partitioning >4 files.
  Gate 3: Report Validation (Phase 6) — rf-qa (report-validation, fix_authorization: true) + rf-qa-qualitative ([skill-qualitative-phase — e.g., report-qualitative, prd-qualitative, tdd-qualitative], fix_authorization: true) sequential. HALT after max fix cycles exceeded.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
  TEMPLATE_COMPLIANCE: All [report sections / template sections] must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.
  [Additional domain validation items if needed — e.g., PRD_SCOPE_COMPLIANCE (prd), LINE_CEILING (operational-guide, readme)]

TESTING_REQUIREMENTS: N/A — documentation-only skill, no code produced, no tests applicable.

<!-- TEMPLATE GUIDANCE: If the skill produces code rather than documentation, replace the TESTING_REQUIREMENTS line with appropriate test requirements. For documentation-only skills, some add a parenthetical clarification — e.g., "N/A — documentation-only skill (research reports), no code produced, no tests applicable." -->

RESEARCH NOTES FILE:
[research-notes-path — e.g., ${TASK_DIR}research/research-notes.md]
Read this file FIRST for full detailed findings including: [domain-specific list — e.g., "existing files, patterns, planned investigation assignments, synthesis mapping, and output paths"].

SKILL CONTEXT FILE:
.claude/skills/[skill-name]/SKILL.md
Read the "[section1]" section for: [description]. Read the "[section2]" section for: [description]. [Continue for all sections the builder needs.] These must be embedded in the relevant checklist items per B2 self-contained pattern.

<!-- TEMPLATE GUIDANCE: The SKILL CONTEXT FILE section is fully DOMAIN-specific. List every section of SKILL.md that the task builder needs to read, and explain what each section provides. The builder uses this to embed the right prompts and rules in checklist items. -->

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process
Structure), you MUST create individual checklist items for EVERY research agent,
web research topic, synthesis file, and validation step. Do NOT create batch items
like "spawn all 5 research agents" or "run all web research" — each agent gets
its own checklist item. The research notes SUGGESTED_PHASES section contains
per-agent detail specifically to enable this granularity.

TO BUILD A GOOD TASK FILE, YOU NEED:
- Goal and outputs (what to create, where, what format)
- Source files and context (what exists, what to reference) — from the research notes
- Phases and steps (logical breakdown of the work) — from the research notes SUGGESTED_PHASES + SKILL.md phase definitions
- Verification criteria (how to know each step is done)
- Dependencies (what's needed before each step)
The research notes file should cover most of this.

ESCALATION:
Since you are running as a subagent (not a teammate), you have NO team context.
Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage — these tools
will fail because there is no team. This overrides your agent definition's
Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
Instead, return the task file path as your final output.
- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
- **External docs/syntax** → use WebSearch
- **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.

SKILL PHASES TO ENCODE IN TASK FILE:
The task file MUST encode these phases as sequential checklist items. Each phase maps to a section of the skill's workflow. All items MUST follow the B2 self-contained pattern from the MDTM template.

[GENERATE per skill — define each phase with its checklist item requirements.
Use the tech-research phases as a structural reference (Phase 1: Preparation,
Phase 2: Deep Investigation with PARALLEL SPAWNING MANDATORY,
Phase 3: Research Completeness Verification with ANALYST + QA GATE,
Phase 4: Web Research with PARALLEL SPAWNING MANDATORY,
Phase 5: Synthesis + QA Gate,
Phase 6: Assembly & Validation with RF-ASSEMBLER + Structural QA + Qualitative QA,
Phase 7: Present to User & Complete Task).
Customize phase names, agent prompts, partitioning thresholds, fix cycle limits,
and downstream suggestions for the skill's specific workflow.
Each phase description must specify:
- What checklist items to create
- What agents to spawn (with full prompt embedding per B2)
- Parallel vs sequential spawning rules
- QA gate behavior (verdict handling, fix cycles, HALT conditions)
- Output file paths]

TASK FILE LOCATION: .dev/tasks/to-do/[TASK-PREFIX]-<subject>-YYYYMMDD-HHMMSS/[TASK-PREFIX]-<subject>-YYYYMMDD-HHMMSS.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, [domain-specific list — e.g., "report structure, validation checklist, and content rules"] (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at [TASK FILE LOCATION path from above] using PART 2 structure
7. Return the task file path
```

**Step 2: Invoke the task-builder skill:**

```
Skill(skill: "task-builder", args: "${TASK_DIR}BUILD-REQUEST.md")
```

The task-builder skill reads the BUILD_REQUEST file, detects `Source: skill-delegated` and `SKIP_RESEARCHERS: true`, skips its own research phase, spawns the rf-task-builder agent, and runs structural and qualitative validation. It returns the task file path.

**Note:** Task-builder handles all verification internally — structural validation checks frontmatter, phases, B2 pattern, embedded prompts, parallel spawning instructions, partitioning guidance, rf-assembler usage, and anti-orphaning. Qualitative validation checks operational correctness. No separate verification step is needed in this skill. Proceed directly to Stage B with the returned task file path.

<!-- TEMPLATE GUIDANCE for A.7:
This is the LARGEST section in the template. Key classification summary:
- SHARED HEADER BLOCK: Source/Calling Skill/Task Directory/Research Notes/SKIP_RESEARCHERS structure is identical across all skills. Only values change.
- DOCUMENTATION STALENESS WARNINGS: VERBATIM COPY from reference (most skills identical; repo-cleanup uses shorter variant).
- TEMPLATE 02 PATTERN MAPPING: Fully GENERATE per skill — phase names, L-level mappings, and descriptions differ.
- QA_GATE_REQUIREMENTS: SHARED structure (3 gates). Only Gate 3 qualitative phase name varies per skill.
- VALIDATION_REQUIREMENTS: SHARED core (3 items). Some skills add domain-specific items (PRD_SCOPE_COMPLIANCE, LINE_CEILING).
- TESTING_REQUIREMENTS: VERBATIM COPY (minor parenthetical clarification varies in 2 skills).
- RESEARCH NOTES FILE: SHARED pattern, DOMAIN path and content list.
- SKILL CONTEXT FILE: Fully GENERATE per skill — lists sections the builder needs to read.
- GRANULARITY REQUIREMENT: VERBATIM COPY from reference (6/7 identical; repo-cleanup uses different nouns).
- TO BUILD A GOOD TASK FILE: VERBATIM COPY from reference (6/7 identical; readme has customized parentheticals).
- ESCALATION: VERBATIM COPY from reference (all 7 identical).
- SKILL PHASES TO ENCODE: Fully GENERATE per skill — phase structure, agents, prompts, thresholds differ.
- TASK FILE LOCATION: SUBSTITUTE — only TASK-PREFIX changes.
- STEPS: VERBATIM COPY structure (steps 1, 3-7 identical). Step 2 has DOMAIN list variation. Step 6 has DOMAIN path.
- Step 2 invocation + closing note: VERBATIM COPY from reference (all 7 identical).
-->

<!-- CLASSIFICATION: SUBSTITUTE -->
## Stage B: Task File Execution

Stage B delegates execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA verification, error handling, and session management.

### Delegation Protocol

1. **Invoke /task** using the Skill tool with `skill: "task"` and `args` set to the task file path from Stage A (e.g., `.dev/tasks/to-do/[TASK-PREFIX]-<subject>-YYYYMMDD-HHMMSS/[TASK-PREFIX]-<subject>-YYYYMMDD-HHMMSS.md`).
2. **Execution transfers to /task**, which reads the task file and processes each checklist item via the F1 loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT).
3. **No additional execution logic is needed** in this skill since all execution rules — sequential item processing, parallel subagent spawning for independent items, session resumption, and progress tracking — are provided by /task.
4. **QA coverage:** The task file already contains skill-specific QA items (rf-analyst completeness verification, rf-qa research gate, rf-qa synthesis gate, rf-assembler assembly, rf-qa report validation, rf-qa qualitative review) as checklist items. The /task skill processes them the same as any other item.

<!-- TEMPLATE GUIDANCE: Points 1-4 are BOILERPLATE with only the example path in point 1 and QA item names in point 4 varying per skill. The example path uses the skill's TASK-PREFIX. -->

### What the Task File Must Contain

Since /task does NOT read this SKILL.md during execution, all skill-specific instructions must be baked into the task file during Stage A:

- **Agent prompt templates** customized with specific [domain — e.g., investigation, documentation, design] topics, file paths, and [domain — e.g., research, documentation, audit] assignments
- **Validation checklists and content rules** embedded in "ensuring..." clauses of each B2 item
- **Output paths and file naming conventions** specified in each item
- **All phase-specific context** so each B2 item is fully self-contained

**CRITICAL:** `/task` does NOT read this SKILL.md during execution. ALL skill-specific instructions, agent prompts, validation criteria, and content rules must be baked into the task file items during Stage A. This includes prohibited actions: research agents READ code, they do not modify it — if the task file doesn't say this, agents won't know.

<!-- TEMPLATE GUIDANCE: The "What the Task File Must Contain" subsection is near-VERBATIM across all existing skills. Only the domain nouns in the bullet list's bracketed placeholders change per skill. The CRITICAL note is VERBATIM — do not modify it. -->

---

<!-- CLASSIFICATION: GENERATE (structure) + COPY (protocol blocks) -->
## Agent Prompt Templates

These prompt templates are embedded verbatim into task file checklist items during Stage A (A.7). Each agent type receives a specialized prompt that includes domain-specific investigation instructions plus mandatory protocol blocks. The protocol blocks (marked VERBATIM below) are identical across all skills and MUST NOT be modified. Domain-specific sections (marked GENERATE) are customized per skill.

<!-- TEMPLATE GUIDANCE: This is the LARGEST section in the template. It contains 9 agent prompt sub-sections. Each prompt is wrapped in a fenced code block (``` ... ```) in the actual SKILL.md files. The VERBATIM protocol blocks within prompts are shared across all existing skills — copy them character-for-character. The GENERATE portions (investigation steps, domain checklists, synthesis rules) are fully customized per skill. -->

### Codebase Research Agent Prompt

```
You are a codebase research agent investigating [assigned topic] for [overall research goal].

Investigation scope: [specific files/directories assigned to this agent]
Task directory: [task-dir-path]
Output path: [task-dir-path]research/[NN]-[topic-slug].md

<!-- VERBATIM — Incremental File Writing Protocol (Codebase Research variant) -->
CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create your output file immediately with this header:
   ```markdown
   # Research: [Your Topic]

   **Investigation type:** [type]
   **Scope:** [files/directories assigned]
   **Status:** In Progress
   **Date:** [today]

   ---
   ```

2. As you investigate each file, component, or logical unit, IMMEDIATELY append your findings to the output file using Edit. Do NOT accumulate findings in your context window.

3. After each append, your output file grows. This is correct behavior. Never rewrite the file from scratch.

4. When finished, update the Status line from "In Progress" to "Complete" and append a summary section.
<!-- END VERBATIM -->

[GENERATE — Research Protocol steps. These are domain-specific investigation instructions. Example from tech-research:
1. Read actual source files — understand what each file does, what it exports, what it imports
2. Trace data flow — how does data enter, transform, and exit this part of the system?
3. Document the implementation — key classes, functions, methods with file paths and line numbers
4. Identify patterns — what conventions, architectural decisions, or design patterns are used?
5. Check for edge cases — error handling, fallbacks, configuration-driven behavior
6. Note dependencies — what does this subsystem depend on? What depends on it?
7. Flag gaps — what is missing, broken, undocumented, or unclear? What needs further investigation?
8. Note integration opportunities — where could new functionality hook in?
Customize these steps for the skill's domain (e.g., prd uses product-capability-focused steps, repo-cleanup uses audit-focused steps).]

<!-- VERBATIM — Documentation Staleness Protocol -->
CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Code describes CURRENT state. These frequently diverge.
When you encounter documentation that describes [DOMAIN — e.g., an architecture, pipeline, service, component, endpoint, or workflow / a product capability, feature, service, or workflow], you MUST cross-validate EVERY structural claim against actual code before reporting it as current:

1. [DOMAIN_ENTITY — e.g., Services/components] described in docs: Verify [DOMAIN_CHECK — e.g., the service directory, entry point file, and key classes actually exist in the repo]. Use Glob to check. [DOMAIN_EXAMPLE — e.g., If a doc says "Go Worker Service at apps/workerv2/", verify `apps/workerv2/` exists. If it doesn't, the doc is STALE — report it as historical, not current.]

2. [DOMAIN_FLOWS — e.g., Pipelines/call chains] described in docs: Trace at least the [first and last hop / entry and exit points] in actual source code. [DOMAIN_EXAMPLE — e.g., If a doc says "Agent → WorkerClient → Go Worker → RCAPI", verify WorkerClient exists as an import/class in the agent code, AND verify the Go Worker service exists. If any hop is missing, the pipeline is STALE.]

3. File paths mentioned in docs: Spot-check that referenced files exist. If a doc references `[example_file.py]` but the actual file is `[example_file_enhanced.py]`, note the discrepancy.

4. API endpoints described in docs: Verify the endpoint exists in the actual router/app code. If a doc describes [DOMAIN_EXAMPLE — e.g., `PUT /api/datatable` proxied through a Go worker], check whether [DOMAIN_CHECK — e.g., the Go worker exists and whether the endpoint is actually served by a different service].

For EVERY doc-sourced [architectural / product capability] claim, mark it with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** — code shows different implementation (describe what code actually shows)
- **[UNVERIFIED]** — could not find corresponding code; may be stale, planned, or in a different repo

Claims marked [UNVERIFIED] or [CODE-CONTRADICTED] MUST appear in the Gaps and Questions section.
Do NOT present doc-sourced claims as verified facts without the code verification tag.
<!-- END VERBATIM — Only the bracketed DOMAIN placeholders change per skill. The 3 tag definitions and closing sentences are character-for-character identical across all skills. -->

[GENERATE — Output Format instructions. Define the expected structure of findings (headers, file paths, anomalies, stale doc markers, Gaps and Questions section, Stale Documentation Found section, Summary). Customize for the skill's domain.]

<!-- VERBATIM — Closing Discipline Statement -->
Be thorough. Be specific. Only document what you verified in the source. Do not guess or infer.
Documentation is NOT verification — reading a doc that says "X exists" does not verify X exists.
Only reading the actual source code of X verifies X exists.
<!-- END VERBATIM — "Do not guess or infer." sentence is present in tech-research and prd; repo-cleanup omits it. Include it by default. -->
```

<!-- TEMPLATE GUIDANCE for Codebase Research Agent Prompt:
- The Incremental File Writing Protocol (steps 1-4) is VERBATIM across all existing skills. Only the header template inside step 1 varies: tech-research/prd use "# Research: [Your Topic]" with Investigation type/Scope/Status/Date; repo-cleanup uses "# Audit Research Batch [N]" with Scope/Status/Date (no Investigation type).
- The Documentation Staleness Protocol skeleton is VERBATIM. Items 3-4 and the 3 tag definitions are identical. Items 1-2 need domain entity names and examples.
- The Closing Discipline Statement is VERBATIM across all skills.
- Research Protocol steps are fully GENERATE — customize for the skill's investigation domain. -->

### Web Research Agent Prompt

```
Research [specific web research topic] for [overall research goal].

Topic: [topic]
Task directory: [task-dir-path]
Output path: [task-dir-path]research/web-[NN]-[topic-slug].md

What we already know from codebase: [brief summary of relevant codebase findings]
Research question context: [the overall research question]

<!-- VERBATIM — Incremental File Writing Protocol (Web Research variant) -->
CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot
<!-- END VERBATIM -->

[GENERATE — Research Protocol steps. These are domain-specific web research instructions. Example from tech-research:
1. Search for official documentation, guides, and API references
2. Look for community best practices, blog posts, and case studies
3. Find comparison analyses and benchmarks
4. Check for known issues, limitations, and workarounds
5. Document findings with source URLs and relevance ratings
Customize these steps for the skill's domain.]

[GENERATE — Output Format instructions. Define the expected structure of web research findings (e.g., Findings section with source URLs, Recommendations from External Research section).]

<!-- SUBSTITUTE — Source-of-Truth Statement -->
IMPORTANT: Our [codebase / codebase audit findings] [is/are] the source of truth [for current capabilities]. External research adds [context and options / market context and competitive intelligence / context] but does not override verified [code behavior / product behavior / repo state]. If you find a discrepancy, note it explicitly.
<!-- END SUBSTITUTE — The skeleton is shared; fill in domain-appropriate nouns. tech-research uses "codebase is the source of truth. External research adds context and options but does not override verified code behavior." prd uses "codebase is the source of truth for current capabilities. External research adds market context and competitive intelligence but does not override verified product behavior." -->
```

<!-- TEMPLATE GUIDANCE for Web Research Agent Prompt:
- The Incremental File Writing Protocol (3 lines) is VERBATIM across all skills.
- Research Protocol steps and Output Format are fully GENERATE per skill.
- The Source-of-Truth Statement follows a shared skeleton with DOMAIN noun substitution. -->

### Synthesis Agent Prompt

```
Synthesize research findings into [section name / report section] for [topic].

Synthesis assignment: [section(s) to synthesize — e.g., "Section 2: Current State Analysis" or "Sections 4-5: Gap Analysis + External Research"]
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Output path: [task-dir-path]synthesis/synth-[NN]-[section-slug].md
Assigned research files: [list of specific research file paths to read]

[GENERATE — Synthesis Rules. These are domain-specific instructions for how to synthesize research into report sections. Example synthesis rules from tech-research:
1. Read EVERY assigned research file completely before synthesizing
2. Write in the exact format that sections should appear in the final report
3. Use the section structure and table formats from the Output Structure section
4. Evidence cited inline: file.cpp:123, ClassName::method()
5. Tables over prose for multi-item data
6. No full source code reproductions — summarize with key signatures and file paths
7. Use ASCII diagrams for architecture, not prose descriptions
8. Every claim needs evidence — no file path = belongs in Open Questions
9. Documentation-sourced claims require verification status ([CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED]). Only [CODE-VERIFIED] claims may be presented as current architecture.
10. Never describe architecture from docs alone — ONLY use findings that trace back to actual source code reads
11. Key findings from research must be reflected in synthesis — read Summary/Key Takeaway sections and ensure each key finding appears or is explicitly excluded with rationale
Customize these rules for the skill's domain and output format.]

<!-- VERBATIM — Synthesis Incremental File Writing Protocol -->
CRITICAL — Incremental File Writing:
You MUST write to your output file incrementally as you synthesize each section. Do NOT read all research files into context and attempt a single large write. The process is:
1. Create the output file with a header and your first synthesized section
2. After completing each subsequent section, append it to the output file immediately using Edit
3. Never rewrite the entire file from memory — always append or do targeted edits
<!-- END VERBATIM -->

[GENERATE — Additional synthesis guidance. E.g., "Write the sections in the exact format they should appear in the final report, using the section structure and table formats from the report template."]
```

<!-- TEMPLATE GUIDANCE for Synthesis Agent Prompt:
- The Incremental File Writing Protocol (3 steps) is VERBATIM across all skills. prd adds an extra sentence after step 3: "This prevents data loss from context limits and ensures partial results survive if the agent is interrupted." — optional.
- Synthesis rules 9-11 (documentation staleness via synthesis) encode the staleness protocol at the synthesis layer. These are SHARED in structure but domain nouns vary.
- The rest of the synthesis rules are fully GENERATE per skill. -->

### Research Analyst Agent Prompt (rf-analyst — Completeness Verification)

```
Perform a completeness verification of all research files for [topic].

Analysis type: completeness-verification
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Research notes file: [task-dir-path]research/research-notes.md
Depth tier: [Quick/Standard/Deep]
Output path: [output-path]

Your job is to independently verify that research agents produced thorough, evidence-based findings
before downstream synthesis begins. You are the analytical quality gate — be rigorous.

PROCESS:
1. Read the research-notes.md file to understand the planned scope (EXISTING_FILES, SUGGESTED_PHASES)
2. Use Glob to find ALL research files in the research directory (files matching [NN]-*.md)
3. Read EVERY research file — do not skip any
4. Apply the 8-item Research Completeness Verification checklist from your agent definition
5. Write your report to [output-path]

CHECKLIST:
1. Coverage audit — every key file from scope covered by at least one research file
2. Evidence quality — claims cite specific file paths, line numbers, function names
3. Documentation staleness — all doc-sourced claims tagged [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED]
4. Completeness — every file has Status: Complete, Summary section, Gaps section, Key Takeaways
5. Cross-reference check — cross-cutting concerns covered by multiple agents are cross-referenced
6. Contradiction detection — conflicting findings about the same component surfaced
7. Gap compilation — all gaps unified, deduplicated, and severity-rated (Critical/Important/Minor)
8. Depth assessment — investigation depth matches the stated tier

VERDICTS:
- PASS: All checks pass, no critical gaps
- FAIL: Critical gaps exist (list each with specific remediation action)

Use the full output format from your agent definition (tables for coverage, evidence quality, staleness, completeness).
Be adversarial — your job is to find problems, not confirm things work.
```

<!-- TEMPLATE GUIDANCE for Research Analyst Agent Prompt:
- This prompt is near-VERBATIM across all skills. The 8-item checklist is identical. Only [topic], directory paths, and depth tier are substituted.
- The VERDICTS block is VERBATIM across all skills. -->

### Research QA Agent Prompt (rf-qa — Research Gate)

```
Perform QA verification of research completeness for [topic].

QA phase: research-gate
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Analyst report: [task-dir-path]qa/analyst-completeness-report.md (if exists, verify the analyst's work; if not, perform full verification)
Research notes file: [task-dir-path]research/research-notes.md
Depth tier: [Quick/Standard/Deep]
Output path: [output-path]

You are the last line of defense before synthesis begins. Assume everything is wrong until you verify it.

<!-- VERBATIM — ADVERSARIAL STANCE block -->
**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
<!-- END VERBATIM -->

IF ANALYST REPORT EXISTS:
1. Read the analyst's completeness report
2. Verify ALL of their coverage audit claims (verify the scope items are actually covered)
3. Validate gap severity classifications (are "Critical" really critical? Are "Minor" really minor?)
4. Check their verdict against your own independent assessment
5. Apply the 10-item Research Gate checklist from your agent definition

IF NO ANALYST REPORT:
Apply the full 10-item Research Gate checklist from your agent definition independently.

10-ITEM CHECKLIST:
1. File inventory — all research files exist with Status: Complete and Summary
2. Evidence density — Verify EVERY claim in each file — verify file paths exist
3. Scope coverage — every key file from research-notes EXISTING_FILES examined
4. Documentation cross-validation — all doc-sourced claims tagged, Verify EVERY CODE-VERIFIED claim
5. Contradiction resolution — no unresolved conflicting findings
6. Gap severity — Critical gaps block synthesis, Important reduce quality, Minor are lower priority but must still be fixed
7. Depth appropriateness — matches the tier expectation
8. Integration point coverage — connection points documented
9. Pattern documentation — code patterns and conventions captured
10. Incremental writing compliance — files show iterative structure, not one-shot

<!-- VERBATIM — Research QA Verdict pattern -->
VERDICTS:
- PASS: Green light for synthesis
- FAIL: ALL findings must be resolved. Only PASS or FAIL — no conditional pass.
<!-- END VERBATIM — repo-cleanup uses "assembly" instead of "synthesis" in the PASS line -->

Use the full QA report output format from your agent definition.
Zero tolerance — if you can't verify it, it fails.
```

<!-- TEMPLATE GUIDANCE for Research QA Agent Prompt:
- The ADVERSARIAL STANCE block is VERBATIM — identical across all skills and all QA phases. Copied from rf-qa.md and tech-research SKILL.md L730.
- The 10-item checklist is VERBATIM across all skills.
- The VERDICTS block is VERBATIM (repo-cleanup substitutes "assembly" for "synthesis").
- The "Zero tolerance" closing line is VERBATIM across all skills. -->

### Synthesis QA Agent Prompt (rf-qa — Synthesis Gate)

```
Perform QA verification of synthesis files for [topic].

QA phase: synthesis-gate
Task directory: [task-dir-path]
Synthesis directory: [task-dir-path]synthesis/
Research directory: [task-dir-path]research/
Fix authorization: [true/false]
Output path: [output-path]

You are verifying that synthesis files are ready for assembly into the final report.
If fix_authorization is true, you can fix issues in-place using Edit.

<!-- VERBATIM — ADVERSARIAL STANCE block -->
**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
<!-- END VERBATIM -->

PROCESS:
1. Use Glob to find ALL synth files (synth-*.md) in the synthesis directory (`${TASK_DIR}synthesis/`)
2. Read EVERY synth file completely
3. Apply the 12-item Synthesis Gate checklist from your agent definition
4. For each issue found:
   a. Document the issue (what, where, severity)
   b. If fix_authorization is true: fix in-place with Edit, verify the fix
   c. If fix_authorization is false: document the required fix
5. Write your QA report to [output-path]

[GENERATE — 12-ITEM CHECKLIST. Customize for the skill's output format. Example from tech-research:
1. Section headers match Output Structure section
2. Table column structures correct
3. No fabrication (Verify EVERY claim in each file, trace to research files)
4. Evidence citations use actual file paths
5. Options analysis: 2+ options with pros/cons
6. Implementation plan: specific file paths, not generic steps
7. Cross-section consistency (gaps in S4 addressed in S8, etc.)
8. No doc-only claims in Sections 2 or 8
9. Stale docs surfaced in Sections 4 or 9
10. Content rules compliance (tables over prose, no code reproductions)
11. All expected sections have content (no placeholders)
12. No hallucinated file paths (verify parent directories exist)
Items 3, 4, 10, 11, 12 are near-identical across all skills. Items 1, 2, 5-9 vary by output format.]

<!-- VERBATIM — Synthesis QA Verdict pattern -->
VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found (list with specific fixes, note which were fixed in-place)
<!-- END VERBATIM -->
```

<!-- TEMPLATE GUIDANCE for Synthesis QA Agent Prompt:
- The ADVERSARIAL STANCE block is VERBATIM — identical to the Research QA version.
- The 12-item checklist is partially SHARED (items 3, 4, 10-12 are near-identical) and partially GENERATE (items matching the skill's output structure).
- The VERDICTS block is VERBATIM across all skills. -->

### Report Validation QA Agent Prompt (rf-qa — Report Validation)

```
Perform final quality validation of the assembled [document type — e.g., research report, PRD, TDD] for [topic].

QA phase: report-validation
Report path: [task-dir-path][REPORT-FILENAME].md
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Synthesis directory: [task-dir-path]synthesis/
Output path: [output-path]
Fix authorization: true (always authorized for report validation)

This is the final quality check before presenting to the user. You can and should fix issues in-place.

<!-- VERBATIM — ADVERSARIAL STANCE block -->
**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
<!-- END VERBATIM -->

PROCESS:
1. Read the ENTIRE [document type]
2. Apply the [N]-item Validation Checklist + [N] Content Quality Checks
3. For each issue: document it, fix it in-place with Edit, verify the fix
4. Write your QA report to [output-path]

[GENERATE — VALIDATION CHECKLIST. Customize for the skill's output structure. Example from tech-research (15 + 4 = 19 items):
1. All 10 report sections present (or N/A for Quick tier)
2. Problem Statement references original research question
3. Current State Analysis cites actual file paths and line numbers
4. Gap Analysis table has severity ratings
5. External Research Findings include source URLs
6. Options Analysis: 2+ options with comparison table
7. Recommendation references comparison analysis
8. Implementation Plan: specific file paths and actions
9. Open Questions: impact and suggested resolution
10. Evidence Trail lists every research and synthesis file
11. No full source code reproductions
12. Tables over prose for multi-item data
13. No assumptions as verified facts
14. No doc-only claims in Sections 2, 6, 7, 8
15. All CODE-CONTRADICTED/STALE DOC findings in Sections 4 or 9

CONTENT QUALITY CHECKS:
16. Table of Contents accuracy
17. Internal consistency (no contradictions between sections)
18. Readability (scannable — tables, headers, bullets)
19. Actionability (developer could begin work from Implementation Plan alone)
Customize validation items and counts for the skill's specific output format and template.]

<!-- VERBATIM — Report Validation closing -->
Fix every issue you find. Report honestly.
<!-- END VERBATIM -->
```

<!-- TEMPLATE GUIDANCE for Report Validation QA Agent Prompt:
- The ADVERSARIAL STANCE block is VERBATIM — identical to all other QA phases.
- The validation checklist is GENERATE per skill — items match the skill's output template structure. Items 11-13 and 16-19 are near-identical across skills.
- The "Fix every issue you find. Report honestly." closing is VERBATIM across all skills.
- Report Validation has NO explicit VERDICTS section — it uses the closing line instead. -->


### Qualitative QA Agent Prompt (rf-qa-qualitative — Intermediate Gates)

<!-- CLASSIFICATION: SUBSTITUTE structure + GENERATE checklists -->

```
QA_PHASE: [gate name — e.g., research-depth, synthesis-coherence]
LENS: [specific lens for this gate]
fix_authorization: false

**ADVERSARIAL STANCE:** Assume the work is superficial until proven otherwise.
Your job is to determine whether findings are genuinely deep or merely
surface-level. A verdict of 0 issues requires evidence you thoroughly checked.

[GENERATE — Gate-specific context block. Include:
- Research/synthesis directory path
- Track goal
- Assigned files list
- Lens-specific focus description]

[GENERATE — Depth/coherence checklist. Examples from existing skills:
- Research-depth lens: Do files explain HOW components work, not just WHAT?
  Are data flows traced end-to-end? Are edge cases documented? Could a builder
  create per-file items without re-reading source?
- Synthesis-coherence lens: Do findings build logically? Are conclusions
  proportionate to evidence? Are contradictions between research files resolved?]

OUTPUT FILE: [qa-report-path]
Write the file IMMEDIATELY with a header, then append findings incrementally.
Conclude with: VERDICT: PASS or FAIL, and severity-rated issues if FAIL.

ESCALATION — CRITICAL OVERRIDE:
You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate,
or TaskList. Return your verdict and report file path as your final output.
```

<!-- TEMPLATE GUIDANCE for Qualitative QA Agent Prompt:
- This agent is spawned at intermediate gates (research-gate, synthesis-gate) alongside rf-analyst and rf-qa agents. It is the 5th agent meeting the I19 intermediate gate floor of 5.
- The ADVERSARIAL STANCE block is VERBATIM across all skills.
- The depth/coherence checklist is GENERATE per skill — each skill defines what "deep enough" means for its domain.
- Research-depth lens: used at research gates (Phase 3 in most skills).
- Synthesis-coherence lens: used at synthesis gates (Phase 5 in most skills).
- The ESCALATION block is VERBATIM across all skills. -->
### Assembly Agent Prompt (rf-assembler — Report Assembly)

```
Assemble the final [document type — e.g., research report, PRD, TDD, technical reference] for [topic] from synthesis files.

Component files (in order):
[ordered list of synth file paths]

Output path: [report-output-path]
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Synthesis directory: [task-dir-path]synthesis/

<!-- VERBATIM — Assembler Incremental File Writing Protocol -->
CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create the output file immediately with the [document type] header:
<!-- END VERBATIM (opening) — The header content below is DOMAIN-specific -->
   [GENERATE — Document header. Example from tech-research:
   # Technical Research Report: [Topic]
   **Date:** [today]
   **Depth:** [Quick / Standard / Deep]
   **Research files:** [count] codebase + [count] web research
   **Scope:** [directories/subsystems investigated]
   Customize the header fields for the skill's output document type.]

<!-- VERBATIM — Assembler steps 2-3 -->
2. As you assemble each section, IMMEDIATELY write it to the output file using Edit.
   Do NOT accumulate the entire report in context and attempt a single write.

3. After each Edit, the file grows. This is correct behavior. Never rewrite from scratch.
<!-- END VERBATIM -->

[GENERATE — Output format specification. Define the required sections of the final document in order. Example from tech-research:
Output format — the final report MUST contain these 10 sections in this order:
1. Problem Statement
2. Current State Analysis
3. Target State
4. Gap Analysis
5. External Research Findings
6. Options Analysis
7. Recommendation
8. Implementation Plan
9. Open Questions
10. Evidence Trail
Customize section list for the skill's output template.]

[GENERATE — Assembly rules. Define how sections are assembled, cross-checked, and validated. Example from tech-research:
Assembly rules:
1. Write the report header first
2. Assemble sections in order — read each synth file and write its content into the correct position
3. Write each section to disk immediately after composing it — do NOT one-shot
4. Generate the Table of Contents from actual section headers after all sections are placed
5. Cross-check internal consistency ([GENERATE: cross-reference checks for YOUR skill's output sections -- e.g., gaps in gap-analysis have steps in recommendations, options reference scope])
6. Flag contradictions between sections
7. Ensure no placeholder text remains
Customize for the skill's specific cross-check requirements.]

[GENERATE — Content rules. Define non-negotiable formatting and quality standards. Example from tech-research:
Content rules (non-negotiable):
- Tables over prose whenever presenting multi-item data
- No full source code reproductions — summarize with key signatures and file paths
- Use ASCII diagrams for architecture and data flow
- Evidence cited inline: file.cpp:123, ClassName::method()
- Conciseness over comprehensiveness
- Every claim needs evidence — no file path or URL = belongs in Open Questions
- Uncertainty marked explicitly
Customize for the skill's output standards.]
```

<!-- TEMPLATE GUIDANCE for Assembly Agent Prompt:
- The Incremental File Writing Protocol opening (2 lines: "CRITICAL..." and "1. FIRST ACTION...") is VERBATIM across all skills. The header content inside step 1 is DOMAIN-specific.
- Steps 2-3 are VERBATIM across all skills.
- Output format, assembly rules, and content rules are fully GENERATE per skill — they must match the skill's output template structure.
- The assembly rules item about writing to disk immediately (rule 3) and cross-checking consistency (rule 5) are near-identical patterns across all skills. -->

---

## Output Structure

[GENERATE — This entire section is domain-specific. Define the complete output document structure that synthesis agents produce sections for and the assembler assembles into. The structure must match the skill's document template (e.g., `.claude/templates/documents/[template_name].md`).

Optional BOILERPLATE intro note (include for skills that use BUILD_REQUEST task file construction):
> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

Followed by an introductory sentence:
"The final [document_type] follows the template at `[template_path]`. The synthesis agents produce sections that are assembled into this format."

Then provide the full output document skeleton inside a markdown code block. Example pattern:

```markdown
---
[frontmatter from template]
---

# [Document Title]: [Topic]

**Purpose:** [one-sentence purpose]
**Date:** [today]
**Tier:** [tier names from the Depth Tiers section]
**Scope:** [directories/subsystems covered]

---

## Table of Contents
[Generated from section headers]

---

## 1. [First Section Name]
[Section description and expected content pattern]

## 2. [Second Section Name]
[Section description and expected content pattern]

## N. [Last Section Name]
[Section description and expected content pattern]

## Document History
[Initial entry and subsequent updates]
```

Replace all section names, numbers, and descriptions with the skill's actual output template structure. Every section that appears in the document template must appear here.]

<!-- TEMPLATE GUIDANCE for Output Structure:
- This section is fully GENERATE — no extraction possible across skills since each skill's output format is entirely defined by its document template.
- The optional intro note ("This section is reference documentation...") is present in most existing skills (tech-reference, prd, tdd, readme, operational-guide) and absent from tech-research and repo-cleanup.
- The document skeleton inside the code block must exactly match the skill's template sections.
- Include subsection patterns (e.g., "5.1 [Subsystem A]") where the template uses repeating subsections. -->

---

<!-- CLASSIFICATION: GENERATE structure + BOILERPLATE table format -->
## Synthesis Mapping Table (Reference)

[GENERATE with BOILERPLATE table structure — Map synthesis files to output document sections. The table structure is BOILERPLATE; the mapping rows are fully domain-specific.

Optional BOILERPLATE intro note (include for skills that use BUILD_REQUEST task file construction):
> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

BOILERPLATE adjustment note (substitute the placeholders):
"This is the standard mapping of synthesis files to [SECTIONS_HEADER] sections. Adjust based on [COMPLEXITY_DIMENSION] — for [BOTTOM_TIER] tier, combine more sections per synth file. For [TOP_TIER] tier, split further if needed (e.g., [SPLIT_EXAMPLE])."

Where:
- [SECTIONS_HEADER] = "Report Sections" (for research skills) or "Template Sections" (for document skills)
- [COMPLEXITY_DIMENSION] = "investigation complexity" / "feature complexity" / "document complexity" etc.
- [BOTTOM_TIER] / [TOP_TIER] = tier names from the Depth Tiers section (e.g., Quick/Deep, Lightweight/Heavyweight)
- [SPLIT_EXAMPLE] = domain-specific example of when to split (e.g., "separate synth files per option in Section 6")

BOILERPLATE table structure:]

| Synth File | [SECTIONS_HEADER] | Source Research Files |
|------------|---------------------|----------------------|
| `synth-01-[name].md` | [Section N, Section M] | [which research files feed this synthesis] |
| `synth-02-[name].md` | [Section N, Section M] | [which research files feed this synthesis] |
| `synth-NN-[name].md` | [Section N, Section M] | [which research files feed this synthesis] |

[GENERATE — Replace the placeholder rows above with the skill's actual synthesis-to-section mapping. Each row maps one synthesis file to the output sections it produces and the research files it draws from. The number of rows depends on the output structure complexity and tier defaults.

Optional BOILERPLATE closing note (include when the mapping varies by feature type):
"Adjust the mapping based on [COMPLEXITY_DIMENSION]. [SKIP_GUIDANCE]. [COMBINE_GUIDANCE]."]

<!-- TEMPLATE GUIDANCE for Synthesis Mapping Table:
- The 3-column table structure (Synth File | Sections Header | Source Research Files) is BOILERPLATE across all skills.
- Column 2 header varies: "Report Sections" for research-oriented skills, "Template Sections" for document-oriented skills.
- The adjustment note about tier-based sizing is BOILERPLATE with domain-specific placeholders.
- The mapping rows themselves are fully GENERATE — each skill defines its own synth-to-section mapping based on its output structure (the Output Structure section).
- Typical skills have 5-7 synthesis files for Standard tier; Quick/Lightweight may combine to 3-4, Deep/Heavyweight may expand to 8-10. -->

---

<!-- CLASSIFICATION: SUBSTITUTE -->
## Synthesis Quality Review Checklist

**This checklist is enforced by the rf-analyst and rf-qa agents** (see Phase 5 in the task phases). The rf-analyst applies these [COUNT] criteria as its Synthesis Quality Review analysis type, and the rf-qa agent independently verifies the analyst's findings with its expanded 12-item Synthesis Gate checklist. The QA agent can fix issues in-place when authorized.

The [COUNT] criteria (used by rf-analyst):

1. Section headers match the expected Output Structure section layout exactly
2. Tables use the correct column structure [SUBSTITUTE: describe expected column formats for this skill's tables]
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and evidence (not vague descriptions)
5. [SUBSTITUTE: domain-specific depth or quality check — e.g., "Options analysis includes at least 2 options" or "Subsystem sections stay within depth budget"]
6. Architecture descriptions backed by code-traced evidence (not doc-only)
7. All cross-references between sections are consistent (e.g., [SUBSTITUTE: example cross-reference pairs from this skill's output structure])
8. **No doc-only claims in [CRITICAL_SECTIONS].** Verify that [SUBSTITUTE: section numbers/names] only contain descriptions backed by code-traced evidence. If a synth file describes a component and the only evidence is a documentation file (no source code path), reject that claim and flag it as `[UNVERIFIED — doc-only]`
9. **Stale documentation discrepancies are surfaced.** Any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings from research files should appear in [SUBSTITUTE: target section for discrepancies — e.g., "Gap Analysis (Section 4)" or "Tech Debt (Section 14)"], not silently omitted
10. [GENERATE: additional domain-specific criterion — e.g., "Key finding coverage" for research skills, line count budgets for reference skills. Add more items as needed.]

The rf-qa agent's Synthesis Gate adds 3 additional checks ([N]-[M]): content rules compliance, section completeness, and hallucinated file path detection. If synthesis QA fails, the QA agent fixes issues in-place (when authorized) and issues remaining unfixed trigger re-synthesis of the affected files.

<!-- TEMPLATE GUIDANCE for Synthesis Quality Review Checklist:
- The opening paragraph about rf-analyst/rf-qa enforcement is BOILERPLATE — keep verbatim, only fill in [count — total criteria].
- Items 3, 4, 6, and 9 are BOILERPLATE across all skills — keep verbatim.
- Items 1, 2, 5, 7, 8 are SUBSTITUTE — same structure but domain nouns/section references change per skill.
- Items 10+ are GENERATE — fully domain-specific, count varies (tech-research has 10 total, tech-reference has 9).
- The closing paragraph about rf-qa Synthesis Gate is BOILERPLATE — keep verbatim, only fill in check number range [N]-[M].
- [count] = total criteria count (typically 8-12 depending on domain complexity). -->

---

<!-- CLASSIFICATION: SUBSTITUTE -->
## Assembly Process

The assembly step reads all synth files in order and produces the final [DOC_TYPE]. Follow these steps:

1. **Write the [HEADER_TYPE]** — [SUBSTITUTE: describe what the header contains — e.g., "title, date, depth tier, research file count, scope summary" for reports or "frontmatter fields, purpose block, document information table" for reference docs]
2. **Assemble sections in order** — paste each synth file's content into the correct position, writing incrementally section by section (do NOT one-shot the entire [DOC_TYPE])
3. **Write the Table of Contents** — generate from actual section headers after all sections are placed
4. **Cross-check internal consistency** — verify that:
   - [GENERATE: cross-reference check 1 — e.g., "Gaps in Section 4 have corresponding implementation steps in Section 8"]
   - [GENERATE: cross-reference check 2 — e.g., "Options in Section 6 reference evidence from Section 2"]
   - [GENERATE: cross-reference check 3 — e.g., "Open Questions in Section 9 aren't answered elsewhere"]
   - [GENERATE: cross-reference check 4 — e.g., "Evidence Trail lists every research file produced"]
5. [OPTIONAL GENERATE: additional assembly step — e.g., "Add Document Provenance appendix documenting source materials" for consolidation-oriented skills. Omit if not needed.]
6. [OPTIONAL GENERATE: additional assembly step — e.g., "Consolidation Protocol for zero content loss" for reference skills. Omit if not needed.]

<!-- TEMPLATE GUIDANCE for Assembly Process:
- Steps 1-3 are BOILERPLATE structure across all skills — only the [header-type]/[header-desc] placeholders change.
- Step 2 is VERBATIM across all skills (the incremental writing rule is universal).
- Step 3 is VERBATIM across all skills.
- Step 4's cross-check bullets are fully GENERATE — each skill defines domain-specific cross-reference pairs based on its output structure (the Output Structure section).
- Steps 5-6 are OPTIONAL GENERATE — tech-reference and operational-guide add Document Provenance and Consolidation Protocol; other skills may omit these.
- Typical step count: 4 for research-oriented skills, 5-6 for document-oriented skills. -->

<!-- CLASSIFICATION: GENERATE -->
## Validation Checklist

Before presenting the [DOC_TYPE] to the user, validate against this checklist (this is encoded in the task file's Assembly phase):

- [ ] All [DOC_TYPE] sections present (or marked N/A with justification)
- [ ] No full source code reproductions — summaries and citations only
- [ ] Tables used over prose for multi-item data
- [ ] No assumptions presented as verified facts
- [ ] No doc-only claims in critical sections — every claim backed by code evidence
- [ ] All CODE-CONTRADICTED/STALE DOC findings surfaced explicitly
- [GENERATE: domain-specific validation item 1 — e.g., "Options Analysis has at least 2 options" for research, "Total line count within tier budget" for reference, "Summary table row count matches total files audited" for cleanup]
- [GENERATE: domain-specific validation item 2 — e.g., "Implementation Plan has specific file paths" for research, "No subsystem section exceeds 200 lines" for reference, "Decision column shows *pending* for unreviewed items" for cleanup]
- [GENERATE: domain-specific validation item 3]
- [GENERATE: domain-specific validation item 4]

<!-- TEMPLATE GUIDANCE for Validation Checklist:
- The first 6 items are BOILERPLATE — include them verbatim in every skill (only [doc-type] changes).
- Domain-specific items are fully GENERATE — each skill defines 4-11 additional items based on its output format and quality requirements.
- Typical total: 10-17 items. Research-oriented skills lean toward 13-17; document-oriented skills lean toward 10-14.
- These items encode the acceptance criteria that rf-qa checks during the final gate. -->

<!-- CLASSIFICATION: SUBSTITUTE -->
## Content Rules (Non-Negotiable)

These rules govern how content is written within research files, synthesis files, and the final [DOC_TYPE]. They prevent bloat, ensure consistency, and keep the output actionable.

| Rule | Do | Don't |
|------|-----|-------|
| **Source code** | Summarize behavior, cite file path + line numbers | Reproduce full function bodies or large code blocks |
| **Architecture** | Use tables and ASCII diagrams | Use multi-paragraph prose to describe structure |
| **File inventories** | Table format (path, purpose, status columns) | List files in paragraph or bullet form |
| **Data flow** | ASCII diagram or numbered step list | Use narrative prose for sequential processes |
| **Evidence** | Inline citations with file paths (`path/to/file.ts:42`) | Cite findings without file paths or line numbers |
| **Uncertainty** | Explicit markers: "Unverified", "Needs confirmation" | Present uncertain findings as verified facts |
| [GENERATE: domain-specific rule category] | [GENERATE: do guidance] | [GENERATE: don't guidance] |
| [GENERATE: domain-specific rule category] | [GENERATE: do guidance] | [GENERATE: don't guidance] |

<!-- TEMPLATE GUIDANCE for Content Rules table:
- The first 6 rows are BOILERPLATE — include them verbatim in every skill.
- Domain-specific rows are fully GENERATE — each skill defines 2-4 additional rows based on its output concerns.
- Examples: tech-research adds "Comparisons" (table format), "Implementation steps" (numbered with file paths), "Gap analysis" (severity-rated table), "Options analysis" (pros/cons table), "Statistics" (table with source citations).
- tech-reference adds "Configuration" (table format), "State shape" (TypeScript interface or table), "Conventions" (table with rationale column).
- repo-cleanup adds "File findings" (table with evidence), "Recommendations" (action + rationale table), "Overlap" (side-by-side table). -->

**General content principles:**
- Tables over prose whenever presenting multi-item data
- Conciseness over comprehensiveness — the [OUTPUT] should be scannable, not exhaustive prose
- Every claim needs evidence — if you can't cite a file path or URL, it belongs in [FALLBACK_SECTION]
- Prefer ASCII diagrams for visual relationships over paragraph descriptions

<!-- TEMPLATE GUIDANCE for General content principles:
- These 4 bullets are BOILERPLATE across all skills.
- [output] substitutes to the skill's primary output noun (e.g., "report", "reference document", "README", "operational guide", "audit report").
- [fallback-section] substitutes to the section where unverified claims belong (e.g., "Open Questions", "Known Gaps", "Tech Debt / Unresolved"). -->

---

<!-- CLASSIFICATION: SUBSTITUTE (rules 1-9) + GENERATE (rules 10+) -->
## Critical Rules (Non-Negotiable)

These are SKILL-SPECIFIC content rules that apply across ALL phases. Violations compromise document quality.

Three execution-discipline rules (task-file-source-of-truth, maximize-parallelism, use-dedicated-tools) are enforced by the `/task` skill and do not appear here. The incremental-writing mandate is retained as Rule 9 below because it is a content-quality requirement specific to this skill's multi-agent research pipeline, not just an execution mechanism.

1. **Codebase is source of truth** — Code > docs > web. Internal documentation describes intent or historical state, not necessarily current state. Only reading actual source code proves a claim. Web research supplements but never overrides verified code findings.

2. **Evidence-based claims only** — Every finding must cite actual file paths, line numbers, and function names. No assumptions, no inferences, no guessing. If you cannot verify it, mark it as "Unverified — needs confirmation."

3. **Gap-driven web research** — Do not web-search everything up front. First investigate the codebase thoroughly, identify specific gaps, then target web research at those gaps. This keeps external research focused and efficient.

4. **Documentation is not verification** — Internal documentation (design docs, architecture docs, READMEs) describes intent, history, or planned state. A doc written 6 months ago about a planned architecture may describe services that were never built, were refactored, or were removed. Treat internal docs with the same skepticism as external blog posts unless code-verified with `[CODE-VERIFIED]` tags.

5. **Preserve research artifacts** — Research files, synthesis files, gaps logs, analyst reports, and QA reports persist after the final document is written. They serve as the evidence trail for all claims and enable future re-investigation. Do NOT delete intermediate files after assembly.

6. **Cross-reference findings** — When multiple research agents investigate related areas, cross-reference their findings. Contradictions between agents must be surfaced, not silently resolved. If Agent A says "service X uses pattern Y" and Agent B says "service X uses pattern Z," both claims must appear with evidence so synthesis can reconcile.

7. **Report all uncertainty** — If something is unclear, ambiguous, or requires a judgment call, document it explicitly in [TARGET_SECTION — e.g., "Open Questions", "Tech Debt / Unresolved", "Known Gaps"]. Do not silently pick one interpretation and present it as fact.

8. **Quality gates mandatory** — [GATE_DETAILS — e.g., "rf-analyst + rf-qa MUST be spawned at gate points: after research (completeness + evidence quality), after synthesis (accuracy + structure), and after assembly (structural validation + qualitative review). Do not skip quality verification to save time. Uncaught errors compound through phases — a bad research file becomes a bad synthesis becomes a bad document."]

9. **No one-shotting documents** — NEVER accumulate content in context and attempt a single large Write. This hits max token output limits and freezes the process, losing all work. Mandatory procedure for ANY file >50 lines: (1) Create the file on disk with header/frontmatter only, (2) Append sections one at a time using Edit, (3) Never rewrite the entire file from memory. This applies to research files, synthesis files, task files, reports, documents — everything. No exceptions.

[GENERATE — Domain-specific rules 10+. Add rules that are specific to this skill's workflow, output format, and quality requirements. Common rules that appear in 5+ existing skills and should be considered for inclusion:
- **Anti-orphaning rule** — Task completion items (frontmatter update, task log entry, user presentation) MUST be inside the final phase, never in a separate Post-Completion section. Orphaned completion items get skipped when the /task skill finishes the last phase.
- **Partitioning thresholds** — When >N research files exist (typically 6), spawn multiple rf-analyst/rf-qa instances with assigned_files subsets to prevent context rot. Each instance reviews a partition independently.
- **Default tier is [TIER_NAME]** — If the user does not specify a depth tier, default to [TIER_NAME] (typically "Standard" for document skills, "Deep" for research skills).
- **Docs-vs-code trust hierarchy** — Code-verified claims > doc-sourced claims with [CODE-VERIFIED] tags > doc-only claims tagged [UNVERIFIED]. Never promote doc-only claims to verified status without code evidence.
- **QA gates are checklist items, not prose** — Every QA gate (research gate, synthesis gate, report validation, qualitative review) must be encoded as a checklist item in the task file with full agent prompts embedded. QA gates described only in prose (in this SKILL.md) are not executed by /task.
Add additional domain-specific rules as needed. Typical total: 10-17 rules for document skills, 12-25 for audit/cleanup skills.]

<!-- TEMPLATE GUIDANCE for Critical Rules:
- Rules 1-9 are SHARED across all skills — keep them verbatim. Only the [target-section] in rule 7 and [gate-details] in rule 8 are substituted per skill.
- Rules 10+ are fully GENERATE — each skill defines its own domain-specific rules based on workflow, output format, and lessons learned.
- The 5 common late-added rules listed in the GENERATE block above (anti-orphaning, partitioning thresholds, default tier, docs-vs-code trust, QA gates as checklist items) appear in most existing skills. Consider including all 5 unless the skill has a specific reason to omit one.
- repo-cleanup has the most domain-specific rules due to its unique audit/delete workflow. Most skills have 12-20+ total depending on domain complexity. -->

---

<!-- CLASSIFICATION: SUBSTITUTE -->
## Session Management

Session management is provided by the `/task` skill. At session start, check `.dev/tasks/to-do/` for `[TASK-PREFIX]-*/` folders related to the current [SUBJECT]. If found, invoke `/task` with the task file path — it resumes from the first unchecked item.

<!-- TEMPLATE GUIDANCE for Session Management:
When resuming a session:

1. Check for an existing task folder matching `[task-prefix]-*/` in `.dev/tasks/to-do/`
2. If found, invoke `/task` with the task file path inside the folder — it will resume from the first unchecked item
3. Check for existing research files in `${TASK_DIR}research/` for context
4. Read any analyst/QA gate reports to understand which gates have already passed

If no task file exists but research files are present, the user likely needs to restart from the first stage (e.g., scope discovery).

- The core statement (single sentence + folder check + invoke /task) is BOILERPLATE across all skills — only [task-prefix] and [subject] change.
- The expanded version (4 steps) varies in detail: tech-research uses the minimal 3-line version; document skills (tech-reference, prd, tdd, readme, operational-guide) add steps for checking research files and analyst/QA gate reports.
- [task-prefix] examples: TASK-RESEARCH, TASK-TECHREF, TASK-PRD, TASK-TDD, TASK-README, TASK-OPSGUIDE, TASK-CLEANUP
- [subject] examples: "research topic", "feature under documentation", "project/module being documented", "directories under audit" -->

---

<!-- CLASSIFICATION: SUBSTITUTE -->
## Research Quality Signals

### Strong [INVESTIGATION_TYPE] Signals

- Findings cite specific file paths and line numbers
- Data flow traced end-to-end
- Integration points mapped with actual function signatures
- Gaps are specific and actionable
- Doc-sourced claims carry verification tags (`[CODE-VERIFIED]`, `[UNVERIFIED]`, `[CODE-CONTRADICTED]`)
- [GENERATE: domain-specific strong signal — e.g., "Implementation plan uses specific file paths and concrete steps" for research, "Subsystem sections stay within depth budget" for reference, "Delete/archive recommendations cite evidence" for cleanup]

### Weak [INVESTIGATION_TYPE] Signals (Redo)

- Vague descriptions without file paths
- Assumptions stated as facts
- Missing gap analysis
- No cross-references between research files
- Doc-sourced claims without verification tags
- [GENERATE: domain-specific weak signal — e.g., "Implementation plan uses generic steps" for research, "Features described from documentation alone" for readme, "Recommendations lack evidence trail" for cleanup]

### When to Spawn Additional Agents

- Research agent flags a critical gap it cannot resolve with available tools
- Two agents' findings contradict each other on a material point
- Scope turns out larger than estimated (e.g., additional subsystems discovered)
- New subsystem discovered during investigation that was not in the original research plan
- [GENERATE: domain-specific spawn trigger — e.g., "Options analysis needs external research for a technology not in the codebase" for research, "Audit surface area exceeds single-agent capacity" for cleanup]

<!-- TEMPLATE GUIDANCE for Research Quality Signals:
- The 3-subsection structure (Strong / Weak (Redo) / When to Spawn) is BOILERPLATE across all skills.
- [investigation-type] substitutes to the skill's investigation noun — e.g., "Research" for tech-research, "Investigation" for tech-reference/prd/tdd, "Audit" for repo-cleanup.
- The 5 BOILERPLATE bullets in each subsection are shared across all existing skills (with minor domain noun swaps).
- Each subsection has 1+ GENERATE bullets for domain-specific signals. Add as many domain-specific bullets as needed.
- repo-cleanup has a significantly different structure: "Strong Delete/Archive Signals" / "Strong Keep Signals" / "Flag When Uncertain" — the 3-subsection pattern holds but subsection names and bullet content are fully domain-specific. -->
