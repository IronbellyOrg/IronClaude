---
name: tdd
description: "Create or populate a Technical Design Document (TDD) for a component, service, or system. Use this skill when the user wants to create a TDD, design a technical architecture, populate an existing TDD stub, or write a comprehensive technical design document following the project template. Can be fed from a PRD to translate product requirements into engineering specifications. Trigger on phrases like 'create a TDD for...', 'design the architecture for...', 'write a technical design document', 'populate this TDD', 'TDD for the agent system', 'technical design for the wizard', or when the user references a *_TDD.md file that needs content. Also trigger when the user says 'design this system', 'architect this feature', or 'turn this PRD into a TDD'."
---

# TDD Creator

Creates comprehensive Technical Design Documents (TDDs) for components, services, and systems by researching the actual codebase, synthesizing findings into template-aligned sections, and assembling the final document. This skill uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts.

**How it works:** The skill performs initial scope discovery (Stage A), then spawns the `rf-task-builder` subagent to create an MDTM task file encoding all investigation and documentation phases. Stage B delegates execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA, and session management.

The output always follows the project template at `src/superclaude/examples/tdd_template.md`. The template is the schema — every TDD must conform to it. Can be fed from a PRD to translate product requirements into engineering specifications.

## Why This Process Works

Technical design documents go stale when written from memory or existing docs. This skill forces every claim through codebase verification — parallel agents read actual source files, trace actual architectures, and document actual implementation patterns.

The MDTM task file provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off.

The multi-phase structure (scope discovery → deep investigation → **analyst verification** → web research → synthesis → **synthesis QA** → assembly → **report validation**) prevents four common failure modes:
- **Context rot** — By isolating each investigation topic in its own subagent with its own output file, no single agent needs to hold the entire investigation in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning many parallel agents (each focused on one aspect), the investigation goes deep on every subsystem simultaneously rather than skimming across everything sequentially.
- **Hallucinated design details** — By separating research (what exists) from synthesis (what it means for the design) from assembly (the final TDD), each phase can be verified independently. Synthesis agents only work from verified research files, not from memory or inference.
- **Uncaught quality drift** — Dedicated `rf-analyst` and `rf-qa` agents provide independent verification at three critical gates: after research (rf-analyst completeness check + rf-qa evidence quality), after synthesis (rf-analyst synthesis review + rf-qa template alignment), and after assembly (rf-qa final TDD validation). The QA agent assumes everything is wrong until independently verified — zero-trust verification prevents rubber-stamping.

The research artifacts persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and feed directly into the assembled TDD.

---

## Input

The skill needs four pieces of information to produce a comprehensive TDD. The first is mandatory; the rest are optional but dramatically improve output quality.

1. **WHAT to design** (mandatory) — The component, service, or system to create a technical design for. Not just a topic name — what you want to architect and why it needs a design document.
   - A component or service description (e.g., "the agent orchestration system", "pixel streaming infrastructure", "wizard state management")
   - An existing TDD stub with a scope or dependencies section
   - A detailed feature specification describing what needs to be built

2. **PRD reference** (optional but strongly recommended) — A Product Requirements Document that this TDD implements. When provided, the TDD extracts relevant epics, user stories, acceptance criteria, technical requirements, and success metrics from the PRD as foundational context. The PRD feeds the TDD the same way tech-research feeds a tech-reference — it provides verified requirements context that the TDD translates into engineering specifications. If no PRD exists, a sufficiently detailed feature description serves the same purpose.

3. **WHERE to look** (optional, saves significant time) — Specific directories, plugins, services, or subsystems to focus on. Prevents agents from spending time on irrelevant areas.

4. **Output location** (optional, has sensible default) — Where the final TDD goes. If a stub exists, write there. If creating from scratch, follow the project convention: `docs/[domain]/TDD_[COMPONENT-NAME].md`.

### What to Do If the Prompt Is Incomplete

If the user provides only a topic name or a vague request, **do NOT proceed immediately**. Ask the user to clarify using this template:

> I can create a TDD for [topic]. To make the design thorough and the specifications actionable, can you help me with:
>
> 1. **What specifically do you want to design?** (e.g., "the agent orchestration system", "the wizard state management", "the pixel streaming infrastructure")
> 2. **Is there a PRD or feature spec to work from?** (This significantly improves requirements traceability)
> 3. **Any specific areas of the codebase I should focus on?** (directories, plugins, services)
> 4. **What tier — Lightweight, Standard, or Heavyweight?** (See Tier Selection below)

Proceed once you have at least #1 answered clearly. Items #2-4 improve quality but aren't blockers.

---

## Tier Selection

**Tier selection rules:**
- If in doubt, pick Standard
- If the user says "detailed", "comprehensive", "thorough" — always Heavyweight
- Only use Lightweight for genuinely narrow designs (single service, <5 relevant files)
- If the scope spans multiple services, architectural layers, or integration boundaries — always Heavyweight

---

## Output Locations

All persistent artifacts go into the task folder at `.dev/tasks/to-do/TASK-TDD-YYYYMMDD-HHMMSS/`. The component slug is derived from the design scope (e.g., `agent-orchestration`, `wizard-state`, `pixel-streaming-infra`).

**Variable definitions:**
```
TASK_ID:     TASK-TDD-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/
SYNTHESIS:   ${TASK_DIR}synthesis/
QA:          ${TASK_DIR}qa/
REVIEWS:     ${TASK_DIR}reviews/
```

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}${TASK_ID}.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| PRD extraction file | `${TASK_DIR}research/00-prd-extraction.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Gap/question log (interim) | `${TASK_DIR}gaps-and-questions.md` |
| Analyst reports | `${TASK_DIR}qa/analyst-report-[gate].md` |
| QA reports | `${TASK_DIR}qa/qa-report-[gate].md` |
| Final TDD | `docs/[domain]/TDD_[COMPONENT-NAME].md` |
| Template schema | `src/superclaude/examples/tdd_template.md` |

**File numbering convention:** All research, web, and synthesis files use zero-padded sequential numbers: `01-`, `02-`, `03-`, etc. This ensures correct ordering when listing files.

Check for existing task folders matching `TASK-TDD-*` in `.dev/tasks/to-do/` before creating new ones — if prior research exists on the same component, read it first and build on it.

---

## Execution Overview

The skill operates in two stages:

**Stage A — Scope Discovery & Task File Creation (before the task file exists):**
1. Check for an existing task file or research directory (A.1)
2. Parse the user's design request and triage into Scenario A vs B (A.2)
3. Perform scope discovery — map component files, plan assignments (A.3)
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
- **Phase 2: Deep Investigation** — Parallel subagent investigation of component code and architecture
- **Phase 3: Completeness Verification** — rf-analyst completeness verification + rf-qa research gate (parallel)
- **Phase 4: Web Research** — Optional external research for design patterns, framework docs, API references
- **Phase 5: Synthesis + Analyst + QA Synthesis Gate** — Template-aligned synthesis, then rf-analyst synthesis review + rf-qa synthesis gate (parallel)
- **Phase 6: Assembly** — rf-assembler produces final document, then rf-qa structural validation, then rf-qa-qualitative content review
- **Phase 7: Present to User & Complete Task** — Deliver document, present artifacts, offer PRD-to-TDD traceability

If a task file already exists for this design topic (from a previous session), skip Stage A and invoke `/task` to resume from the first unchecked item.

---

## Stage A: Scope Discovery & Task File Creation

### A.1: Check for Existing Task File

Before creating a new task file, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `TASK-TDD-*/` folder containing a task file related to this component
2. If found, read the task file and check for unchecked `- [ ]` items
3. If unchecked items exist → skip to Stage B (resume execution)
4. If all items are checked → inform user that TDD is already complete, offer to update or re-run
5. Check for existing task folder at `.dev/tasks/to-do/TASK-TDD-*/`:
   a. If `research-notes.md` exists inside the task folder with `Status: Complete` → skip to A.5 (review sufficiency, then build task file)
   b. If `research-notes.md` exists inside the task folder with `Status: In Progress` → read it, resume A.3 scope discovery from where it left off, then continue to A.4 to update the file
   c. If task folder exists but no `research-notes.md` → continue with A.3 but use the existing folder
6. If no task folder exists → continue with A.2

### A.2: Parse & Triage the Design Request

Break the design request into structured components:

- **GOAL**: What specifically needs a technical design (the component, service, or system)
- **WHY**: What the user wants to achieve (new system design, architecture documentation, PRD translation)
- **WHERE**: Specific directories, files, or subsystems to focus on
- **OUTPUT_TYPE**: The kind of TDD needed (Lightweight / Standard / Heavyweight)
- **PRD_REF**: Path to a PRD that this TDD implements (optional but strongly recommended)
- **COMPONENT_SLUG**: A kebab-case identifier for the task folder (e.g., `agent-orchestration`, `wizard-state`)

**Triage into Scenario A or B:**

**Scenario A — Explicit request:** User provided most of: component name, source locations, PRD reference, tier selection.
Example: "Create a TDD for the agent orchestration system. The PRD is at `docs/docs-product/tech/agents/PRD_AGENT_SYSTEM.md`. Focus on `backend/app/agents/`. Standard tier."
→ Scope discovery confirms details and fills minor gaps. Lighter exploration.

**Scenario B — Vague request:** User provided a component name but few specifics.
Example: "Create a TDD for the wizard"
→ Scope discovery does broad exploration to map what exists, identify subsystems, and plan investigation assignments.

**Do NOT interrogate the user with a list of questions.** Proceed with what you have and let scope discovery figure out the rest from the codebase. Only ask the user if there's a genuine ambiguity about **intent** that can't be inferred (e.g., the component name is too vague to even begin searching). Use the "What to Do If the Prompt Is Incomplete" template from the Input section only when the request truly cannot proceed.

### A.3: Perform Scope Discovery

Use Glob, Grep, and codebase-retrieval to map the component's architecture. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.

**Adjust depth by scenario:**
- **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, scan for related code, identify gaps in what the user specified.
- **Scenario B**: Broad discovery — scan the full codebase for anything touching the component, map all relevant subsystems, identify documentation, count files.

**Discovery steps:**

1. **Check for an existing stub** — look for a `*_TDD.md` or `*-TDD.md` file at the expected output location or in `docs/`. Also scan for any existing documentation about this component (READMEs, architecture docs, PRDs in `docs/`) — these become input for Doc Analyst research agents.

2. **Map the component's files and directories** — enumerate:
   - Primary source directory and key subdirectories
   - Number of files and approximate complexity
   - Major subsystems (group files by function)
   - External integration points (imports from outside the component)
   - **If PRD_REF is provided**, read the PRD and extract: relevant epics, user stories, acceptance criteria, technical requirements, technology stack, success metrics/KPIs, scope definition (in/out/deferred), performance/security/scalability requirements.

3. **Plan research assignments** — divide the component into specific investigation topics, each becoming a subagent assignment. Common topics for TDDs:
   - Architecture and system design patterns
   - Each major subsystem (1 per subsystem)
   - Data model and entity relationships
   - API surface and service boundaries
   - Integration points and cross-service communication
   - Existing documentation review (if consolidating other docs)

4. **Plan web research topics** — from gaps identified during discovery (framework docs, third-party API references, pattern documentation)

5. **Determine synthesis file mapping** — map planned research files to template sections using the synth mapping table

6. **Select depth tier** based on component count — Lightweight (<5 files), Standard (5-20), Heavyweight (20+). Default to Standard if unsure. Record the tier selection and rationale in the research notes.

**Research assignment types** (use as many as the component requires):

| Type | Purpose | What the Agent Does |
|------|---------|-------------------|
| **Architecture Analyst** | Understand system design | Trace architectural decisions, dependency chains, component relationships, design patterns |
| **Code Tracer** | Understand how code actually works | Read implementations, trace data flow, follow imports, document behavior |
| **Data Model Analyst** | Map data shapes and storage | Document entity relationships, schemas, type definitions, data flow |
| **API Surface Mapper** | Document integration contracts | Map API endpoints, request/response schemas, service boundaries |
| **Integration Mapper** | Identify connection points | Map extension points, plugin interfaces, config surfaces, cross-service communication |
| **Doc Analyst** | Extract context from existing documentation | Read docs, **cross-validate every architectural claim against actual code**, note discrepancies and stale content |

Create the task folder: `.dev/tasks/to-do/TASK-TDD-YYYYMMDD-HHMMSS/` with subfolders `research/`, `synthesis/`, `qa/`, `reviews/`

**Optional — spawn rf-task-researcher for complex scope discovery:**

If scope discovery needs deeper context (e.g., Scenario B with a large unknown codebase area, or Scenario A where the specified directories contain deep nested structures), spawn an `rf-task-researcher` subagent. Pass it a RESEARCH_REQUEST describing what to explore. It will write research notes to a file. You then use those notes as input for A.4.

### A.4: Write Research Notes File (MANDATORY)

Write the scope discovery results to a structured research notes file at `${TASK_DIR}research-notes.md`. This file is what the builder reads — NOT inline content in the BUILD_REQUEST.

The file MUST be organized into these 8 categories (include all, mark as "N/A" if empty):

```markdown
# Research Notes: [COMPONENT]

**Date:** [today]
**Scenario:** [A or B]
**Tier:** [Lightweight / Standard / Heavyweight]

---

## EXISTING_FILES
[All files, directories, and subsystems found during scope discovery. Per-file detail: path, purpose, key exports, approximate line count. Group by directory or subsystem.]

## PATTERNS_AND_CONVENTIONS
[Code patterns, naming conventions, architectural patterns, design decisions observed. Cite specific files as evidence.]

## PRD_CONTEXT
[If PRD provided: extracted epics, user stories, acceptance criteria, technical requirements, success metrics, scope boundaries. If no PRD: "N/A — no PRD provided, using feature description as requirements source."]

## SOLUTION_RESEARCH
[If the design involves evaluating multiple approaches: architectural alternatives considered, technology options, trade-offs analyzed. If pure documentation of existing design: "N/A — documenting existing architecture, not evaluating alternatives."]

## RECOMMENDED_OUTPUTS
[Planned output files: research files, synthesis files, final TDD. Full paths and purposes.]

## SUGGESTED_PHASES
[Planned investigation breakdown. For each planned research agent:
- Agent number, investigation type, topic
- Files/directories to investigate
- Output file path
- Web research topics identified from gaps
- Synthesis file mapping]

## TEMPLATE_NOTES
[Notes about which MDTM template to use and why. Almost always Template 02 for TDD.]

## AMBIGUITIES_FOR_USER
[Genuine ambiguities about user intent that cannot be resolved from the codebase. If none, write "None — intent is clear from the request and codebase context."]
```

### A.5: Review Research Sufficiency (MANDATORY GATE)

**You MUST review the research notes before spawning the builder.** This is a quality gate — do NOT skip it.

Read `${TASK_DIR}research-notes.md` and evaluate:

1. Is the component scope clearly bounded?
2. Are all major subsystems identified?
3. Are integration points mapped?
4. Is existing documentation inventoried?
5. Are research assignments concrete enough for the task builder to create per-agent checklist items? (Each needs: topic, agent type, file list, output path)
6. Is the template section mapping reasonable?
7. If a PRD was provided: is PRD_CONTEXT populated with extracted requirements (epics, acceptance criteria, technical requirements, scope boundaries)?
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
- Discovery before building (investigating unknown architectures)
- Parallel subagent spawning
- Multiple phases with different activities (research, synthesis, assembly)
- Review/validation steps
- Conditional flows based on findings

**Use Template 01 (Generic Task) when the work involves:**
- Simple, sequential file creation
- Straightforward execution with no discovery
- Single-pass operations

**For TDD creation, the answer is almost always Template 02** — the skill inherently involves scope discovery, parallel investigation (Phase 2), completeness verification (Phase 3), web research (Phase 4), synthesis (Phase 5), and assembly with validation (Phase 6).

### A.7: Build the Task File

Spawn the `rf-task-builder` subagent. The builder reads the research notes file and the MDTM template, then creates the task file. It also reads the SKILL.md itself for phase requirements and agent prompt templates.

**Loading declaration (FR-TDD-R.6a):** Before spawning the builder, the orchestrator MUST load `refs/build-request-template.md`:

```
Read refs/build-request-template.md
```

This provides the BUILD_REQUEST structure that the orchestrator fills in and passes to the builder. No other refs files are loaded by the orchestrator at this phase.

> **Loaded at runtime from** `refs/build-request-template.md` — Full BUILD_REQUEST template with field definitions, tier-specific parameters, and orchestrator fill-in instructions.

**Builder load dependencies (FR-TDD-R.6b):** The `rf-task-builder` subagent MUST load these 4 refs files to construct the task file:

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

> **Loaded at runtime from** `refs/operational-guidance.md` — Critical execution rules, research quality signals, artifact location conventions, PRD-to-TDD pipeline, TDD update protocol, and session management guidance.

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
- Phase 6 uses `rf-assembler` (not a general-purpose Agent) and references the validation checklist from SKILL.md
- Phase 7 includes task-completion items (anti-orphaning)

If the task file is malformed or missing critical elements, re-run the builder with specific corrections. Otherwise, proceed to Stage B.

---

## Stage B: Task File Execution

Stage B delegates execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA verification, error handling, and session management.

### Delegation Protocol

1. **Invoke /task** using the Skill tool with `skill: "task"` and `args` set to the task file path from Stage A (e.g., `.dev/tasks/to-do/TASK-TDD-20260309-120000/TASK-TDD-20260309-120000.md`).
2. **Execution transfers to /task**, which reads the task file and processes each checklist item via the F1 loop — spawning subagents as specified in B2 items and running phase-gate QA after each phase
3. No additional execution logic is needed in this skill — all execution rules (F1 loop, F2 prohibited actions, parallel spawning, F4 modification restrictions, F5 frontmatter protocol, error handling, session resumption) are provided by `/task`
4. **QA coverage:** The task file already contains skill-specific QA items (rf-analyst + rf-qa at gates, rf-qa-qualitative for content review). `/task` adds its own phase-gate QA on top, resulting in intentional, acceptable double QA at gate phases

### What the Task File Must Contain

The task file created in Stage A must embed all skill-specific context because `/task` does NOT read this SKILL.md during execution:

- **Agent prompt templates** customized with specific topics, file paths, and investigation assignments
- **Validation checklists and content rules** embedded in "ensuring..." clauses of each B2 item
- **Output paths and file naming conventions** specified in each item
- **All phase-specific context** so each B2 item is fully self-contained — an executor reading only the task file has everything needed to complete each item

**CRITICAL:** `/task` does NOT read this SKILL.md during execution. ALL skill-specific instructions, agent prompts, validation criteria, and content rules must be baked into the task file items during Stage A. This includes prohibited actions: research agents READ code, they do not modify it; do not fabricate design specifications without codebase evidence; do not generate code snippets unless the TDD documents existing implementation patterns.

---

## Phase Loading Contract (FR-TDD-R.6c)

This table declares which refs files are loaded at each phase and by which actor. No phase may load a refs file listed in its Forbidden Loads column. This contract enforces phase isolation — refs content is only loaded when needed, by the actor that needs it.

| Phase | Actor | Declared Loads | Forbidden Loads |
|---|---|---|---|
| Invocation (SKILL.md load) | Claude Code | `SKILL.md` | `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
| Stage A.1–A.6 | Orchestrator | `SKILL.md` | `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
| Stage A.7 (orchestrator) | Orchestrator | `refs/build-request-template.md` | _(none)_ |
| Stage A.7 (builder) | `rf-task-builder` | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` | _(none)_ |
| Stage A.8 | Orchestrator | `SKILL.md` | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
| Stage B | `/task` execution | Generated task file + task skill | `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |

**Contract validation rules (FR-TDD-R.6d):**

1. **Set intersection:** `declared_loads ∩ forbidden_loads = ∅` for every phase
2. **Runtime containment:** `runtime_loaded_refs ⊆ declared_loads` for every phase

If a refs file is loaded outside its declared phase, the phase contract is violated and execution must halt.

### PRD Extraction Agent Prompt

```
Extract structured content from the PRD at {{PRD_REF}} and write to ${TASK_DIR}research/00-prd-extraction.md.

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create the output file immediately with a header.
2. Append each section using Edit as you complete it.
3. Never accumulate and one-shot.

Extract the following 5 sections:

## Section 1: Epics
| Epic ID | Title | Description |
|---------|-------|-------------|
(One row per epic. Use the PRD's own epic identifiers.)

## Section 2: User Stories and Acceptance Criteria
For each epic, list user stories with bulleted acceptance criteria grouped by parent epic ID.

## Section 3: Success Metrics
| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|--------------------|
(One row per KPI. Preserve the PRD's metric names exactly.)

## Section 4: Technical Requirements
Flat list with requirement type labels (functional, non-functional, constraint).

## Section 5: Scope Boundaries
- **In scope:** (bulleted list)
- **Out of scope:** (bulleted list)

Tag each extracted item as [PRD-VERIFIED] (directly stated in PRD text with section reference) or [PRD-INFERRED] (derived from PRD context but not explicitly stated). Do NOT use [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags here -- those are for codebase research agents that compare documentation against source code. This agent extracts from a PRD (product requirements), not from code.

This agent is read-only — it produces the extraction file only. No code changes.
```

---
