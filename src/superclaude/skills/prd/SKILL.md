---
name: prd
description: "Create or populate a Product Requirements Document (PRD) for a product, feature, or platform. Use this skill when the user wants to create a PRD, document product requirements, populate an existing PRD stub, or write a comprehensive product requirements document following the project template. Trigger on phrases like 'create a PRD for...', 'document the product requirements', 'write a PRD', 'populate this PRD', 'product requirements for the wizard system', or when the user references a PRD file that needs content following the PRD template. Also trigger when the user says 'define the product' in the context of product planning or requirements gathering."
---

# PRD Creator

A skill for creating comprehensive Product Requirements Documents (PRDs) for products, features, and platform capabilities. This skill uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts.

**How it works:** The skill performs initial scope discovery (mapping the product area, identifying research topics, assessing complexity), then spawns the `rf-task-builder` subagent to create an MDTM task file encoding all investigation, synthesis, and assembly phases. The skill then executes from that task file, marking items complete as it progresses. If context compresses or the session restarts, the skill re-reads the task file and resumes from the first unchecked item.

The output always follows the project template at `docs/docs-product/templates/prd_template.md`. The template is the schema — every PRD must conform to it.

## Why This Process Works

PRDs go stale when written from memory or existing docs. This skill forces every claim through codebase verification and market research — parallel agents read actual source files, trace actual capabilities, investigate competitive landscapes, and document actual product behavior.

The MDTM task file provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off.

The multi-phase structure (scope discovery → deep investigation → **analyst verification** → web research → synthesis → **synthesis QA** → assembly → **report validation**) prevents four common failure modes:
- **Context rot** — By isolating each research topic in its own subagent with its own output file, no single agent needs to hold the entire investigation in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning many parallel agents (each focused on one product area), the investigation goes deep on every aspect simultaneously rather than skimming across everything sequentially.
- **Hallucinated requirements** — By separating research (what exists) from synthesis (what it means for the product) from assembly (the final PRD), each phase can be verified independently. Synthesis agents only work from verified research files, not from memory or inference.
- **Uncaught quality drift** — Dedicated `rf-analyst` and `rf-qa` agents provide independent verification at three critical gates: after research (rf-analyst completeness check + rf-qa evidence quality), after synthesis (rf-analyst synthesis review + rf-qa template conformance), and after assembly (rf-qa final PRD validation). The QA agent assumes everything is wrong until independently verified — zero-trust verification prevents rubber-stamping.

The research artifacts persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and feed directly into the assembled PRD.

---

## Input

The skill needs four pieces of information to produce a comprehensive PRD. The first is mandatory; the rest are optional but dramatically improve output quality.

1. **WHAT product/feature to document** (mandatory) — A clear product area, feature, or platform capability. Not just a name — what scope the PRD should cover.

2. **WHY / what decisions this PRD supports** (strongly recommended) — Whether this is for investor pitches, engineering planning, feature prioritization, or stakeholder alignment. This shapes emphasis: market analysis vs technical depth vs UX focus.

3. **WHERE to look** (optional, saves significant time) — Specific directories, services, or subsystems that implement the product. Prevents agents from spending time on irrelevant areas.

4. **OUTPUT location** (optional) — Where the final PRD goes. If a stub exists, write there. If creating from scratch, follow the project convention: `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md`.

### Effective Prompt Examples

**Strong — all four pieces present:**
> Create a PRD for the GameFrame AI multi-agent system. We need this for Series A investor materials and to align the engineering team on the next quarter's roadmap. Focus on: `backend/app/agents/`, `backend/app/services/`, `frontend/src/components/Chat/`. Output to `docs/docs-product/tech/agents/PRD_MULTI_AGENT_SYSTEM.md`.

**Strong — clear scope + purpose:**
> Create a PRD for the wizard configuration system. We want to add new stages and need to document current capabilities vs planned features for the product team. Key areas: `frontend/app/wizard/`, the stage configs, and the Zustand store slices.

**Strong — consolidation focus:**
> Create a PRD for the canvas roadmap feature by consolidating the existing docs at `docs/docs-product/tech/canvas/`. Need a single source of truth for product planning.

**Weak — topic only (will work but produces broader, less actionable results):**
> Write a PRD for the platform.

**Weak — no "why" (agents won't know what to emphasize):**
> Create a PRD for pixel streaming.

### What to Do If the Prompt Is Incomplete

If the user provides only a product name or a vague request, **do NOT proceed immediately**. Ask the user to clarify using this template:

> I can create a PRD for [product/feature]. To make the document focused and actionable, can you help me with:
>
> 1. **What's the scope?** (single feature, product area, or entire platform?)
> 2. **What's this PRD for?** (engineering planning, investor materials, stakeholder alignment, feature prioritization?)
> 3. **Any specific areas of the codebase I should focus on?** (directories, services, subsystems)
> 4. **Where should the final PRD go?** (existing stub path or new location)

Proceed once you have at least #1 answered clearly. Items #2-4 improve quality but aren't blockers.

---

## Tier Selection

Match the tier to product scope. **Default to Standard** unless the product is clearly documentable with a quick scan of <5 files.

| Tier | When | Codebase Agents | Web Agents | Target Lines |
|------|------|-----------------|------------|-------------|
| **Lightweight** | Single feature, narrow scope, <5 user stories, <5 relevant files | 2–3 | 0–1 | 400–800 |
| **Standard** | Full product area, 5-20 user stories, moderate complexity, 5-20 files | 4–6 | 1–2 | 800–1,500 |
| **Heavyweight** | Platform-level PRD, 20+ user stories, multiple product areas, 20+ files | 6–10+ | 2–4 | 1,500–2,500 |

**Tier selection rules:**
- If in doubt, pick Standard
- If the user says "detailed", "comprehensive", "thorough" — always Heavyweight
- Only use Lightweight for genuinely narrow products (<5 files, single concern)
- If the scope spans multiple product areas, architectural layers, or integration boundaries — always Heavyweight

---

## Output Locations

All persistent artifacts go into the task folder at `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/`. The product slug is derived from the product scope (e.g., `wizard-system`, `multi-agent-platform`, `pixel-streaming`).

**Variable reference block:**
```
TASK_ID:     TASK-PRD-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/
SYNTHESIS:   ${TASK_DIR}synthesis/
QA:          ${TASK_DIR}qa/
REVIEWS:     ${TASK_DIR}reviews/
```

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/TASK-PRD-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Gaps log | `${TASK_DIR}gaps-and-questions.md` |
| Analyst reports | `${TASK_DIR}qa/analyst-report-[gate].md` |
| QA reports | `${TASK_DIR}qa/qa-report-[gate].md` |
| Analyst completeness report | `${TASK_DIR}qa/analyst-completeness-report.md` |
| Analyst synthesis review | `${TASK_DIR}qa/analyst-synthesis-review.md` |
| QA report (research gate) | `${TASK_DIR}qa/qa-research-gate-report.md` |
| QA report (synthesis gate) | `${TASK_DIR}qa/qa-synthesis-gate-report.md` |
| QA report (report validation) | `${TASK_DIR}qa/qa-report-validation.md` |
| QA report (qualitative review) | `${TASK_DIR}qa/qa-qualitative-review.md` |
| Final PRD | `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md` |
| Final PRD | `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md` |
| Template schema | `docs/docs-product/templates/prd_template.md` |

**File numbering convention:** All research, web, and synthesis files use zero-padded sequential numbers: `01-`, `02-`, `03-`, etc. This ensures correct ordering when listing files.

Check for existing task folders matching `TASK-PRD-*` in `.dev/tasks/to-do/` before creating new ones — if prior research exists on the same product, read it first and build on it.

---

## Execution Overview

The skill operates in two stages:

**Stage A — Scope Discovery & Task File Creation (before the task file exists):**
1. Check for an existing task file or research directory (A.1)
2. Parse the user's PRD request and triage into Scenario A vs B (A.2)
3. Perform scope discovery — map product files, plan assignments (A.3)
4. Write scope discovery results to a structured research notes file (A.4)
5. Review research sufficiency — mandatory gate (A.5)
6. Triage template selection (A.6)
7. Spawn the task builder to create the MDTM task file (A.7)
8. Verify the task file (A.8)

**Stage B — Task File Execution (after the task file exists):**
9. Delegate execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA, and session management
10. Each checklist item is a self-contained prompt — no prior context needed

Phase names within the task file:
- **Phase 1: Preparation** — Scope confirmation, template read, tier selection
- **Phase 2: Deep Investigation** — Parallel subagent investigation of product code and capabilities
- **Phase 3: Completeness Verification** — rf-analyst completeness verification + rf-qa research gate (parallel)
- **Phase 4: Web Research** — Optional external research for market context, competitive landscape, industry standards
- **Phase 5: Synthesis + Analyst + QA Synthesis Gate** — Template-aligned synthesis, then rf-analyst synthesis review + rf-qa synthesis gate (parallel)
- **Phase 6: Assembly** — rf-assembler produces final document, then rf-qa structural validation, then rf-qa-qualitative content review
- **Phase 7: Present to User & Complete Task** — Deliver document, present artifacts, offer companion document creation

If a task file already exists for this product (from a previous session), skip Stage A and invoke `/task` directly to resume from the first unchecked item.

---

## Stage A: Scope Discovery & Task File Creation

### A.1: Check for Existing Task File

Before creating a new task file, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `TASK-PRD-*/` folder containing a task file related to this product
2. If found, read the task file and check for unchecked `- [ ]` items
3. If unchecked items exist → skip to Stage B (resume execution)
4. If all items are checked → inform user that PRD is already complete, offer to update or re-run
5. Check for existing task folder at `.dev/tasks/to-do/TASK-PRD-*/`:
   a. If `research-notes.md` exists with `Status: Complete` → skip to A.5 (review sufficiency, then build task file)
   b. If `research-notes.md` exists with `Status: In Progress` → read it, resume A.3 scope discovery from where it left off, then continue to A.4 to update the file
   c. If task folder exists but no `research-notes.md` → continue with A.3 but use the existing folder
6. If no task folder exists → continue with A.2

### A.2: Parse & Triage the PRD Request

Break the user's request into structured components:

- **GOAL**: What product, feature, or platform capability to document (the PRD scope)
- **WHY**: What this PRD is for (engineering planning, investor materials, stakeholder alignment, feature prioritization)
- **WHERE**: Specific directories, services, or subsystems to focus on
- **OUTPUT_TYPE**: Where the final PRD goes (existing stub or new file)
- **PRODUCT_SLUG**: A kebab-case identifier for the task folder (e.g., `wizard-system`, `multi-agent-platform`, `pixel-streaming`). Derivation rule: use the shortest unambiguous kebab-case description of the product scope. Prefer 2-3 word slugs. Examples: `wizard-system` not `gameframe-wizard-configuration-system`, `pixel-streaming` not `ps`.
- **PRD_SCOPE**: Classify as **Product PRD** or **Feature/Component PRD** (see below).

**Classify PRD scope:**

| Type | When | Template Section Impact |
|------|------|------------------------|
| **Product PRD** | The PRD covers an entire standalone product or platform (e.g., "GameFrame AI Platform PRD") | All 32 sections applicable. Include TAM/SAM/SOM, pricing, GTM, competitive analysis, full compliance. |
| **Feature/Component PRD** | The PRD covers a feature, subsystem, or component within the platform (e.g., "Task Management System", "Wizard System", "Pixel Streaming") | Sections S5 (Business Context), S8 (Value Proposition), S9 (Competitive Analysis), S19 (Legal/Compliance), S20 (Business Requirements) are typically N/A or abbreviated. These are platform-level concerns — the feature PRD should reference the Platform PRD for market sizing, pricing, GTM, and full compliance. Feature PRDs keep feature-specific KPIs (S5), feature-specific data handling (S19), and feature-specific cost notes (S20). |

**This classification MUST be recorded in the research notes file** and embedded in the BUILD_REQUEST for the task builder. Synthesis agents must know whether to fill platform-level sections or mark them N/A.

**Triage into Scenario A or B:**

**Scenario A — Explicit request:** User provided most of: product scope, purpose, source locations, output path.
Example: "Create a PRD for the wizard configuration system. We need this for product planning and to document current capabilities vs planned features. Focus on: `frontend/app/wizard/`, the stage configs, and the Zustand store slices. Output to `docs/docs-product/tech/frontend/PRD_WIZARD_SYSTEM.md`."
→ Scope discovery confirms details and fills minor gaps. Lighter exploration.

**Scenario B — Vague request:** User provided a product name but few specifics.
Example: "Write a PRD for pixel streaming"
→ Scope discovery does broad exploration to map what exists, identify product areas, and plan investigation assignments.

**Do NOT interrogate the user with a list of questions.** Proceed with what you have and let scope discovery figure out the rest from the codebase. Only ask the user if there's a genuine ambiguity about **intent** that can't be inferred (e.g., the product name is too vague to even begin searching). Use the "What to Do If the Prompt Is Incomplete" template from the Input section only when the request truly cannot proceed.

### A.3: Perform Scope Discovery

Use Glob, Grep, and codebase-retrieval to map the product space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.

**Adjust depth by scenario:**
- **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, scan for related code, identify gaps in what the user specified.
- **Scenario B**: Broad discovery — scan the full codebase for anything touching the product, map all relevant subsystems, identify documentation, count files.

**Discovery steps:**

1. **Check for an existing stub** — look for a `PRD_*.md` or `*-PRD.md` file at the expected output location or in `docs/`. Also scan for any existing documentation about this product (READMEs, architecture docs, design docs in `docs/`) — these become input for Doc Analyst research agents.

2. **Map the product's files and directories** — enumerate:
   - Primary source directory and key subdirectories
   - Number of files and approximate complexity
   - Major subsystems (group files by product area)
   - External integration points (third-party services, APIs, frameworks)
   - User-facing flows, interaction patterns, and feature implementations

3. **Plan research assignments** — divide the product into specific investigation topics, each becoming a subagent assignment. Common topics for PRDs:
   - Feature inventory and user-facing capabilities
   - Each major product area (1 per area)
   - User experience and interaction patterns
   - Integration points and service boundaries
   - Architecture and technology choices
   - Existing documentation review (if consolidating other docs)

4. **Plan web research topics** — from gaps identified during discovery (market context, competitive landscape, industry trends, framework references)

5. **Determine synthesis file mapping** — map planned research files to template sections using the synth mapping table

6. **Select depth tier** based on component count — Lightweight (<5 files), Standard (5-20), Heavyweight (20+). For explicit feature requests, default to Standard if unsure; for vague or open-ended requests, default to Heavyweight. Record the tier selection and rationale in the research notes.

**Research assignment types** (use as many as the topic requires):

| Type | Purpose | What the Agent Does |
|------|---------|-------------------|
| **Feature Analyst** | Inventory product capabilities | Read implementations, document user-facing features, trace user flows |
| **Doc Analyst** | Extract context from existing documentation | Read docs, **cross-validate every product claim against actual code** (see Documentation Staleness Protocol), note discrepancies and stale content |
| **Integration Mapper** | Identify connection points | Map APIs, extension points, service boundaries, config surfaces, external dependencies |
| **UX Investigator** | Understand user experience | Trace interaction patterns, document UI flows, identify accessibility and usability patterns |
| **Architecture Analyst** | Understand system design | Trace architectural decisions, dependency chains, component relationships, technology choices |

Create the task folder: `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/` with subfolders `research/`, `synthesis/`, `qa/`, `reviews/`

**Optional — spawn rf-task-researcher for complex scope discovery:**

If scope discovery needs deeper context (e.g., Scenario B with a large unknown product area, or Scenario A where the specified directories contain deep nested structures), spawn an `rf-task-researcher` subagent. Pass it a RESEARCH_REQUEST describing what to explore. It will write research notes to a file. You then use those notes as input for A.4.

### A.4: Write Research Notes File (MANDATORY)

Write the scope discovery results to a structured research notes file at `${TASK_DIR}research-notes.md`. This file is what the builder reads — NOT inline content in the BUILD_REQUEST.

The file MUST be organized into these 7 categories (include all, mark as "N/A" if empty):

```markdown
# Research Notes: [PRODUCT]

**Date:** [today]
**Scenario:** [A or B]
**Tier:** [Lightweight / Standard / Heavyweight]
**PRD Scope:** [Product PRD / Feature PRD]
<!-- If Feature PRD: Sections S5 (market sizing), S8 (value prop), S9 (competitive), S17 (full compliance), S18 (pricing/GTM) are N/A or abbreviated. Include feature-specific KPIs, data handling, and cost notes only. Reference Platform PRD for platform-level concerns. -->

---

## EXISTING_FILES
[All files, directories, and subsystems found during scope discovery. Per-file detail: path, purpose, key features, approximate line count. Group by product area or subsystem.]

## PATTERNS_AND_CONVENTIONS
[Product patterns, naming conventions, architectural patterns, design decisions observed. Cite specific files as evidence.]

## FEATURE_ANALYSIS
[If the product area involves multiple features or capabilities: inventory of features discovered, their implementation status, and user-facing behavior. Mark as "N/A — single feature scope" if not applicable.]

## RECOMMENDED_OUTPUTS
[Planned output files: research files, web research files, synthesis files, final PRD. Full paths and purposes.]

## SUGGESTED_PHASES
[Planned investigation breakdown. For each planned research agent:
- Agent number, investigation type, topic
- Files/directories to investigate
- Output file path
- Web research topics identified from gaps
- Synthesis file mapping]

## TEMPLATE_NOTES
[Notes about which MDTM template to use and why. Almost always Template 02 for PRD creation.]

## AMBIGUITIES_FOR_USER
[Genuine ambiguities about user intent that cannot be resolved from the codebase. If none, write "None — intent is clear from the request and codebase context."]
```

### A.5: Review Research Sufficiency (MANDATORY GATE)

**You MUST review the research notes before spawning the builder.** This is a quality gate — do NOT skip it.

Read `${TASK_DIR}research-notes.md` and evaluate:

1. Is the product scope clearly bounded?
2. Are all major subsystems identified?
3. Are integration points mapped?
4. Is existing documentation inventoried?
5. Are research assignments concrete enough for the task builder to create per-agent checklist items? (Each needs: topic, agent type, file list, output path)
6. Is the template section mapping reasonable?
7. Are stakeholder segments and user personas identified (at minimum from codebase evidence)?
8. If any doc-sourced claims appear in the research notes (e.g., from scanning existing documentation during scope discovery), are they tagged with `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`? Claims marked `[CODE-CONTRADICTED]` or `[UNVERIFIED]` must be flagged in AMBIGUITIES_FOR_USER.

**If sufficient** → proceed to A.6 (template triage).

**If insufficient** → either:
- Do additional scope discovery yourself and update the research notes file, OR
- Spawn an rf-task-researcher subagent with specific feedback about what's missing, then re-review

**Maximum 2 gap-fill rounds.** After 2 rounds, proceed with what's available and note remaining gaps in the research notes AMBIGUITIES_FOR_USER section.

Do NOT proceed to the builder with incomplete research notes. The builder cannot explore the codebase effectively — it relies on what you provide.

### A.6: Template Triage

Determine which MDTM template the task builder should use:

**Use Template 02 (Complex Task) when the work involves:**
- Discovery before building (investigating unknown product areas)
- Parallel subagent spawning
- Multiple phases with different activities (research, web research, synthesis, assembly)
- Review/validation steps
- Conditional flows based on findings

**Use Template 01 (Generic Task) when the work involves:**
- Simple PRD update (adding a section to an existing PRD)
- Straightforward execution with no discovery
- Single-pass operations

**For PRD creation, the answer is almost always Template 02** — the skill inherently involves scope discovery, parallel research agents, web research, synthesis, quality gates, and assembly.

### A.7: Build the Task File

Spawn the `rf-task-builder` subagent. The builder reads the research notes file and the MDTM template, then creates the task file. It also reads the SKILL.md itself for phase requirements and agent prompt templates.


**Loading declaration :** Before spawning the builder, the orchestrator MUST load `refs/build-request-template.md`:

```
Read refs/build-request-template.md
```

This provides the BUILD_REQUEST structure that the orchestrator fills in and passes to the builder. No other refs files are loaded by the orchestrator at this phase.

> **Loaded at runtime from** `refs/build-request-template.md` — Full BUILD_REQUEST template with field definitions, tier-specific parameters, and orchestrator fill-in instructions.

**Builder load dependencies :** The `rf-task-builder` subagent MUST load these 4 refs files to construct the task file:

```
Read refs/agent-prompts.md
Read refs/synthesis-mapping.md
Read refs/validation-checklists.md
Read refs/operational-guidance.md
```

These refs are loaded by the builder (not the orchestrator). The builder uses them to embed agent prompt templates, synthesis mapping rules, validation checklists, and operational guidance directly into the task file's B2 checklist items.

> **Loaded at runtime from** `refs/agent-prompts.md` — Codebase research, web research, synthesis, analyst, QA, assembly, and PRD extraction agent prompt templates with per-agent instructions.

> **Loaded at runtime from** `refs/synthesis-mapping.md` — Output structure definition and research-to-template-section synthesis mapping table.

> **Loaded at runtime from** `refs/validation-checklists.md` — Assembly process steps, structural/content validation checklists, and non-negotiable content rules.

> **Loaded at runtime from** `refs/operational-guidance.md` — Critical execution rules, research quality signals, artifact location conventions, PRD update protocol, and session management guidance.

**Spawning the builder:**

Use the Agent tool with `subagent_type: "rf-task-builder"` and `mode: "bypassPermissions"`. Pass the full BUILD_REQUEST as the prompt.

### A.8: Receive & Verify the Task File

The builder subagent returns the path to the created task file. Read the file and verify:
- Frontmatter is properly populated
- All planned phases are present as checklist items
- Checklist items follow the B2 self-contained pattern (single paragraph: context + action + output + verification)
- No nested checkboxes, no standalone context-reading items
- Agent prompts are FULLY embedded in each subagent-spawning item (not references to "see above")
- Phases 2, 3, 4, and 5 items include explicit parallel spawning instructions (including partitioning guidance for analyst/QA when file counts are high)
- Phase 6 uses `rf-assembler` (not a general-purpose Agent) and references the validation checklist from `refs/validation-checklists.md`
- Phase 7 includes task-completion items (write task summary, update frontmatter to Done) WITHIN the phase — not as a separate section

If the task file is malformed or missing critical elements, re-run the builder with specific corrections. Otherwise, proceed to Stage B.

---

## Stage B: Task File Execution

Stage B delegates execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA verification, error handling, and session management.

### Delegation Protocol

1. **Invoke /task:** Use the Skill tool with `skill: "task"` and `args` set to the task file path created in Stage A (e.g., `.dev/tasks/to-do/TASK-PRD-20260309-120000/TASK-PRD-20260309-120000.md`). This transfers execution to the `/task` skill.
2. **Execution by /task:** The `/task` skill reads the task file and processes each checklist item via the F1 loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT), spawning subagents as specified in the B2 self-contained items and running phase-gate QA after each phase (Phase 2+).
3. **No additional execution logic needed:** All execution rules — F1 loop, F2 prohibited actions, parallel agent spawning, F4 modification restrictions, F5 frontmatter protocol, error handling, and session resumption — are provided by the `/task` skill.
4. **QA coverage:** The task file already contains skill-specific QA items (rf-analyst completeness-verification, rf-qa research-gate, synthesis-gate, report-validation, rf-qa-qualitative prd-qualitative) embedded in Phases 3, 5, and 6. The `/task` skill adds phase-gate QA on top of these, resulting in intentional, acceptable double QA at gate phases.

### What the Task File Must Contain

The task file created in Stage A must be fully self-contained because `/task` does NOT read this SKILL.md during execution. All skill-specific instructions must be baked into the task file during Stage A:

- **Agent prompt templates** customized with specific product areas, investigation topics, and file paths
- **Validation checklists and content rules** embedded in "ensuring..." clauses of relevant items
- **Output paths and file naming conventions** for all research, synthesis, and assembly artifacts
- **All phase-specific context** so each B2 item is a complete, single-paragraph prompt that can be executed without external references

**CRITICAL:** `/task` does NOT read this SKILL.md during execution. ALL skill-specific instructions, agent prompts, validation criteria, and content rules must be baked into the task file items during Stage A. This includes prohibited actions: research agents READ code, they do not modify it; do not fabricate product capabilities; do not invent file paths; do not delete research artifacts after assembly.


---

## Phase Loading Contract (FR-PRD-R.6c)

This table declares which refs files are loaded at each phase and by which actor. No phase may load a refs file listed in its Forbidden Loads column. This contract enforces phase isolation — refs content is only loaded when needed, by the actor that needs it.

| Phase | Actor | Declared Loads | Forbidden Loads |
|---|---|---|---|
| Invocation (SKILL.md load) | Claude Code | `SKILL.md` | `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
| Stage A.1–A.6 | Orchestrator | `SKILL.md` | `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
| Stage A.7 (orchestrator) | Orchestrator | `refs/build-request-template.md` | _(none)_ |
| Stage A.7 (builder) | `rf-task-builder` | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` | _(none)_ |
| Stage A.8 | Orchestrator | `SKILL.md` | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
| Stage B | `/task` execution | Generated task file + task skill | `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |

**Contract validation rules (FR-PRD-R.6d):**

1. **Set intersection:** `declared_loads ∩ forbidden_loads = ∅` for every phase
2. **Runtime containment:** `runtime_loaded_refs ⊆ declared_loads` for every phase

If a refs file is loaded outside its declared phase, the phase contract is violated and execution must halt.

---

## Session Management

Session management is provided by the `/task` skill. See `refs/operational-guidance.md` for detailed session resumption, PRD update protocol, and artifact location conventions.

