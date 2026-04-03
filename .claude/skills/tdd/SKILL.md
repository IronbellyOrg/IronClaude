---
name: tdd
description: "Create or populate a Technical Design Document (TDD) for a component, service, or system. Use this skill when the user wants to create a TDD, design a technical architecture, populate an existing TDD stub, or write a comprehensive technical design document following the project template. Can be fed from a PRD to translate product requirements into engineering specifications. Trigger on phrases like 'create a TDD for...', 'design the architecture for...', 'write a technical design document', 'populate this TDD', 'TDD for the agent system', 'technical design for the wizard', or when the user references a *_TDD.md file that needs content. Also trigger when the user says 'design this system', 'architect this feature', or 'turn this PRD into a TDD'."
---

# TDD Creator

Creates comprehensive Technical Design Documents (TDDs) for components, services, and systems by researching the actual codebase, synthesizing findings into template-aligned sections, and assembling the final document. This skill uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts.

**How it works:** The skill performs initial scope discovery (Stage A), then spawns the `rf-task-builder` subagent to create an MDTM task file encoding all investigation and documentation phases. Stage B delegates execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA, and session management.

The output always follows the project template at `docs/docs-product/templates/tdd_template.md`. The template is the schema — every TDD must conform to it. Can be fed from a PRD to translate product requirements into engineering specifications.

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

### Effective Prompt Examples

**Strong — all four pieces present:**
> Create a TDD for the agent orchestration system. The PRD is at `docs/docs-product/tech/agents/PRD_AGENT_SYSTEM.md`. Focus on `backend/app/agents/`, `backend/app/services/agent_service.py`, and `backend/app/workers/`. Write to `docs/agents/TDD_AGENT_ORCHESTRATION.md`.

**Strong — clear scope + PRD + output type:**
> Turn the canvas roadmap PRD into a TDD. The PRD is at `docs/docs-product/tech/canvas/PRD_ROADMAP_CANVAS.md`. I need a Standard-tier design covering the React canvas system, dependency management, and node type architecture. Focus on `frontend/app/roadmap/`.

**Strong — design from scratch with clear scope:**
> Design the technical architecture for a shared GPU pool to replace per-session VMs. Scope: `ue_manager/`, `infrastructure/`, `backend/app/services/streaming_service.py`. This is a Heavyweight TDD — new system, cross-team impact.

**Weak — topic only (will work but produces broader, less focused results):**
> Create a TDD for the wizard.

**Weak — no context (agents won't know what to focus on):**
> Write a technical design document.

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

Match the tier to component scope. **Default to Standard** unless the component is clearly documentable with a quick scan of <5 files.

| Tier | When | Codebase Agents | Web Agents | Target Lines |
|------|------|-----------------|------------|-------------|
| **Lightweight** | Bug fixes, config changes, small features (<1 sprint), <5 relevant files | 2–3 | 0–1 | 300–600 |
| **Standard** | Most features and services (1-3 sprints), 5-20 files, moderate complexity | 4–6 | 1–2 | 800–1,400 |
| **Heavyweight** | New systems, platform changes, cross-team projects, 20+ files | 6–10+ | 2–4 | 1,400–2,200 |

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
| Template schema | `docs/docs-product/templates/tdd_template.md` |

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

**BUILD_REQUEST format for the subagent prompt:**

```
BUILD_REQUEST:
==============
GOAL: Create a comprehensive Technical Design Document (TDD) for [COMPONENT] by researching the actual codebase, synthesizing findings into template-aligned sections, and assembling the final document. The TDD will be written to [OUTPUT_PATH].

WHY: [WHY — what prompted this TDD and what the design document will be used for]

PRD_REF: [path to PRD, or "None"]

TASK_ID_PREFIX: TASK-TDD

TEMPLATE: [01 or 02 — skill selects:
  01 = simple file creation, straightforward execution
  02 = needs discovery, testing, review, conditional flows, or aggregation]

DOCUMENTATION STALENESS WARNINGS:
[If scope discovery found any documentation that contradicts actual code, list the
specific claims and contradictions here. If none found during scope discovery, write:
"None found during scope discovery. Phase 2 agents will perform full documentation
cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags."]
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 1 (Preparation): Update task status, confirm scope from research notes, read the TDD template, select depth tier, create task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase and write findings files to ${TASK_DIR}research/. If PRD provided, first item extracts PRD context to ${TASK_DIR}research/00-prd-extraction.md.
- Phase 3 (Completeness Verification): L4 Review/QA — spawn rf-analyst (completeness-verification) AND rf-qa (research-gate) IN PARALLEL. Both write reports. QA verdict gates progression.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — agents read research files and produce template-aligned sections. Then spawn rf-analyst (synthesis-review) AND rf-qa (synthesis-gate, fix_authorization: true) IN PARALLEL. QA can fix issues in-place.
- Phase 6 (Assembly & Validation): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final TDD, then spawn rf-qa (report-validation) for structural quality check, then spawn rf-qa-qualitative (tdd-qualitative) for content/logic quality check. Both QA agents have in-place fix authorization.
- Phase 7 (Present to User & Complete Task): ANTI-ORPHANING — task-completion items are WITHIN this phase, not in a separate Post-Completion section.

RESEARCH NOTES FILE:
${TASK_DIR}research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, PRD context, planned investigation assignments, synthesis mapping, and output paths.

SKILL CONTEXT FILE:
.claude/skills/tdd/SKILL.md
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt. Read the "Synthesis Mapping Table" section for the standard synth-file-to-TDD-section mapping. Read the "Synthesis Quality Review Checklist" section for post-synthesis verification. Read the "Assembly Process" section for TDD assembly steps. Read the "Validation Checklist" section for Phase 6 validation criteria. Read the "Content Rules" section for writing standards. Read the "Tier Selection" section for depth tier line budgets and agent counts. These must be embedded in the relevant checklist items per B2 self-contained pattern.

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

Phase 1 — Preparation:
- Update task status to "🟠 Doing"
- Confirm scope from research notes (component boundaries, key directories, tier selection)
- Read the TDD template at docs/docs-product/templates/tdd_template.md
- Select depth tier (Lightweight / Standard / Heavyweight) based on component count and complexity
- Create the task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders (if not already created during scope discovery)

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- If PRD provided: first item extracts PRD context to ${TASK_DIR}research/00-prd-extraction.md
- One checklist item PER research agent (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md
- Each item specifies: investigation topic, type (Architecture Analyst / Code Tracer / Data Model Analyst / API Surface Mapper / Integration Mapper / Doc Analyst), files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from SKILL.md) in each checklist item per B2
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. For example, with 6 research assignments: spawn all 6 agents in one message, mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.
- Agent count follows tier guidance: Lightweight 2-3, Standard 4-6, Heavyweight 6-10+

Phase 3 — Research Completeness Verification (ANALYST + QA GATE, PARALLEL):
- Spawn `rf-analyst` (subagent_type: "rf-analyst", analysis_type: "completeness-verification") AND `rf-qa` (subagent_type: "rf-qa", qa_phase: "research-gate") IN PARALLEL. Both agents independently read research files and apply their own checklists. The analyst applies its 8-item completeness checklist (coverage audit, evidence quality, doc staleness, completeness, cross-references, contradictions, gap compilation, depth assessment). The QA agent applies its 10-item research-gate checklist (file inventory, evidence density, scope coverage, doc cross-validation, contradiction resolution, gap severity, depth appropriateness, integration points, pattern documentation, incremental writing compliance). The analyst writes to `${TASK_DIR}qa/analyst-completeness-report.md`. The QA agent writes to `${TASK_DIR}qa/qa-research-gate-report.md`. Embed full prompts from respective agent definitions in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE analyst + QA instances with assigned_files subsets. The threshold is >6 for research files because research files tend to be longer and more detailed than synthesis files. Each partition instance writes to a numbered report (e.g., `${TASK_DIR}qa/analyst-completeness-report-1.md`). After all instances complete, merge reports: union of findings, take the more severe rating for any item flagged by multiple partitions, deduplicate gaps.
- Read ALL reports (or merged report). Determine verdict from QA report(s) (PASS / FAIL), cross-referenced with analyst findings.
- If PASS → proceed to Phase 4. If FAIL → fix ALL findings regardless of severity before proceeding. Spawn targeted gap-filling agents, then rf-qa fix-cycle.
- Maximum 3 fix cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance on how to proceed. Do NOT continue to Phase 4 without user approval.
- Compile final gaps into ${TASK_DIR}gaps-and-questions.md
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
- Web research is optional — only spawn when codebase research reveals gaps requiring external documentation

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One checklist item PER synthesis file (from Synthesis Mapping Table)
- After ALL synthesis agents complete, spawn rf-analyst (synthesis-review) AND rf-qa (synthesis-gate, fix_authorization: true) IN PARALLEL
- **Parallel partitioning for large workloads:** When >4 synthesis files exist, spawn multiple analyst + QA instances with assigned_files subsets. The threshold is lower than Phase 3 (>4 vs >6) because synthesis QA requires deeper per-file analysis (tracing claims back to research files, verifying cross-section consistency). Same partitioning pattern as Phase 3. Each partition instance writes to a numbered report. Orchestrator merges all partition reports after completion.
- Max 2 fix cycles for synthesis gate. After 2 failed cycles, HALT execution: log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance. Do NOT continue to Phase 6 without user approval.

Phase 6 — Assembly & Validation (RF-ASSEMBLER + Structural QA + Qualitative QA):
- Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") — NOT a general-purpose Agent — to assemble the final TDD. Hand it: the list of synth file paths in order (as component_files), the TDD output path `docs/[domain]/TDD_[COMPONENT-NAME].md`, the TDD template reference `docs/docs-product/templates/tdd_template.md` (as output_format), the Assembly Process steps from SKILL.md (as assembly_rules), and the Content Rules from SKILL.md (as content_rules). The assembler reads each synth file and writes the TDD incrementally section by section — frontmatter first, then sections in template order, then Table of Contents, then cross-checks internal consistency (requirements in Section 5 trace to architecture in Section 6, risks in Section 20 have mitigations, Open Questions in Section 22 not answered elsewhere, Dependencies in Section 18 complete). The assembler must be a single agent (NOT parallel) because cross-section consistency requires seeing the whole document. Embed the full assembler prompt (see Assembly Agent Prompt Template below and Assembly Process section in SKILL.md) in the checklist item per B2.
- After the assembler returns the TDD path, spawn `rf-qa` (subagent_type: "rf-qa", qa_phase: "report-validation", fix_authorization: true). The QA agent validates the assembled TDD against the 15-item Validation Checklist + 4 Content Quality Checks from SKILL.md (structural/semantic checks: section numbers, cross-references, evidence citations, template conformance). The QA agent is authorized to fix issues in-place and writes its report to `${TASK_DIR}qa/qa-report-validation.md`. Embed the full QA prompt in the checklist item per B2.
- Read the structural QA report. If issues remain unfixed, address them before proceeding to qualitative QA.
- After structural QA passes, spawn `rf-qa-qualitative` (subagent_type: "rf-qa-qualitative", qa_phase: "tdd-qualitative", fix_authorization: true). The qualitative QA agent reads the entire TDD and verifies it makes sense from product and engineering perspectives: architecture decisions match PRD requirements, API contracts are internally consistent, implementation details are specific enough to code from, no PRD content repeated verbatim, data models match across diagrams/contracts/migrations, no requirements invented that aren't in the PRD. The agent writes to `${TASK_DIR}qa/qa-qualitative-review.md`. Embed the full qualitative QA prompt (including document_type: "Technical Design Document", template path, and output path) in the checklist item per B2.
- Read the qualitative QA report. If any issues found (CRITICAL, IMPORTANT, or MINOR), verify fixes were applied correctly by re-reading the affected sections. If issues remain unfixed, address ALL of them before proceeding to Phase 7. Zero leniency — no severity level is exempt.

Phase 7 — Present to User & Complete Task (ANTI-ORPHANING):
- Present summary to user (TDD location, line count, tier, sections populated vs skipped, research artifacts location, gaps)
- Ask about cleanup of consolidation sources (if applicable)
- Suggest downstream workflow: "This TDD can feed directly into implementation task files. Would you like me to create implementation tasks using the `/task` skill? The research files and design specifications are already in place." If yes, invoke the task skill with the TDD as context.
- Write task summary to Task Log
- Update task file frontmatter: status to "🟢 Done", set completion_date

TASK FILE LOCATION: .dev/tasks/to-do/TASK-TDD-[YYYYMMDD]-[HHMMSS]/TASK-TDD-[YYYYMMDD]-[HHMMSS].md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, synthesis mapping, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .gfdoc/templates/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .gfdoc/templates/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-TDD-[YYYYMMDD-HHMMSS]/TASK-TDD-[YYYYMMDD-HHMMSS].md using PART 2 structure
7. Return the task file path
```

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

## Agent Prompt Templates

These templates are provided to the task builder (in the BUILD_REQUEST) so it can embed them in the task file's self-contained checklist items. The builder should customize each instance with the specific investigation topic, files, and output path.

### Codebase Research Agent Prompt

```
Research this aspect of [component name] and write findings to [output-path]:

Topic: [topic description]
Investigation type: [Architecture Analyst / Code Tracer / Data Model Analyst / API Surface Mapper / Integration Mapper / Doc Analyst]
Files to investigate: [list of files/directories]
Component root: [primary directory]
PRD context: [path to PRD extraction file, if applicable — cross-reference requirements as you research]

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

Research Protocol:
1. Read the actual source files — understand what each file does, what it exports, what it imports
2. Trace data flow — how does data enter, transform, and exit this part of the system?
3. Document the implementation — key classes, functions, methods with file paths and line numbers
4. Identify architecture patterns suitable for the design — what patterns can inform the TDD?
5. Document data model shapes and relationships — entity types, field definitions, constraints
6. Map API surface and integration contracts — endpoints, request/response schemas, service boundaries
7. Check for edge cases — error handling, fallbacks, configuration-driven behavior
8. Note dependencies — what does this subsystem depend on? What depends on it?
9. Flag gaps — what is missing, broken, undocumented, or unclear? What needs further investigation?
10. Note integration opportunities — where could new functionality hook in? Where are the natural extension points?

CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Code describes CURRENT state. These frequently diverge.
When you encounter documentation that describes an architecture, pipeline, service, component, endpoint,
or workflow, you MUST cross-validate EVERY structural claim against actual code before reporting it as current:

1. **Services/components described in docs:** Verify the service directory, entry point file, and key classes actually exist in the repo. Use Glob to check. If a doc says "Service X at path/Y/", verify the path exists. If it doesn't, the doc is STALE — report as historical, not current.

2. **Pipelines/call chains described in docs:** Trace at least the first and last hop in actual source code. If any hop is missing, the pipeline is STALE.

3. **File paths mentioned in docs:** Spot-check that referenced files exist.

4. **API endpoints described in docs:** Verify the endpoint exists in the actual router/app code.

For EVERY doc-sourced architectural claim, mark it with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** — code shows different implementation (describe what code actually shows)
- **[UNVERIFIED]** — could not find corresponding code; may be stale, planned, or in a different repo

Claims marked [UNVERIFIED] or [CODE-CONTRADICTED] MUST appear in the Gaps and Questions section.
Do NOT present doc-sourced claims as verified facts without the code verification tag.

Output Format:
- Use descriptive headers for each file or logical group investigated
- Include actual class names, function signatures, data model shapes, and API endpoints (not reproduced code blocks — summaries with key signatures)
- Note any anomalies, tech debt, or surprising behavior
- Flag stale documentation explicitly with **[STALE DOC]** markers
- End each section with a "Key Takeaways" bullet list
- End the file with:
  ## Gaps and Questions
  - [things that need further investigation or are unclear]
  - [all UNVERIFIED and CODE-CONTRADICTED claims from docs]

  ## Stale Documentation Found
  - [list any docs that describe architecture/components that no longer exist in code]

  ## Summary
  [3-5 sentence summary of what you found]

Be thorough. Be specific. Only document what you verified in the source. Do not guess or infer.
Documentation is NOT verification — reading a doc that says "X exists" does not verify X exists.
Only reading the actual source code of X verifies X exists.
```

### Web Research Agent Prompt

```
Research this topic externally and write findings to [output-path].

Topic: [specific external research topic]
What we already know from codebase: [brief summary of relevant codebase findings]
Component context: [the overall component being designed]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for official documentation, guides, and API references for relevant technologies
2. Search for architectural patterns and design best practices
3. Search for performance benchmarks and optimization strategies
4. Search for security patterns and threat models for this type of system
5. Search for API design standards and industry conventions
6. Search for SLO/SLI industry benchmarks for similar systems
7. Search for implementation examples and reference architectures
8. For each finding, document:
   - Source URL
   - Key information extracted
   - How it relates to our codebase findings
   - Whether it supports, extends, or contradicts what we found in code
9. Rate source reliability (official docs > well-maintained repos > blog posts > forum answers)

Output Format:
- Use descriptive headers for each research area
- Always include source URLs
- Mark relevance: HIGH / MEDIUM / LOW for each finding
- End with:
  ## Key External Findings
  [Bullet list of the most important discoveries]

  ## Recommendations from External Research
  [How external findings should influence the technical design]

IMPORTANT: Our codebase is the source of truth. External research adds technology context and best practices but does not override verified code behavior. If you find a discrepancy, note it explicitly.
```

**Common web research topics for TDDs:**
- Design pattern references relevant to the component architecture (e.g., repository pattern, saga pattern, circuit breaker)
- Scalability benchmarks for the technology stack and expected load profile
- Security best practices for the component type (e.g., auth patterns, input validation, encryption standards)
- API design standards and industry conventions (e.g., REST best practices, GraphQL schema design, gRPC patterns)
- Infrastructure patterns for the component type (e.g., caching strategies, message queue patterns, database scaling)

### Synthesis Agent Prompt

```
Read the research files listed below and synthesize them into template-aligned sections for a Technical Design Document (TDD).

Research files to read: [list of paths]
Template sections to produce: [section numbers and names]
Output path: [synth file path]
Template reference: docs/docs-product/templates/tdd_template.md

Rules:
0. **Read the template first.** Before synthesizing anything, read the TDD template to understand each section's expected content, format, and depth.
1. Follow the template structure exactly — use the same headers, tables, and section format
2. Every fact must come from the research files — do not invent or assume
3. Use tables over prose for multi-item data (requirements, dependencies, metrics, risks)
4. Do not reproduce full interfaces, function bodies, or configuration files — summarize with key signatures and data shapes
5. Architecture sections must include ASCII or Mermaid diagrams where the research supports them
6. Requirements must use ID numbering (FR-001, NFR-001) with priority and acceptance criteria
7. Reference actual file paths, not hypothetical ones
8. Alternatives Considered must include Alternative 0: Do Nothing (mandatory per template)
9. SLOs must include SLI measurements and error budget policies where applicable
10. Documentation-sourced claims require verification status. If a research file reports a finding from documentation, check whether it carries a [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED] tag. Only [CODE-VERIFIED] claims may be presented as current architecture. [CODE-CONTRADICTED] claims must be corrected. [UNVERIFIED] claims must be flagged as uncertain and placed in Open Questions (Section 22) — never in Architecture, Data Models, or API Specifications sections as if they are fact.
11. Never describe architecture from docs alone. When writing Architecture (Section 6), Data Models (Section 7), or API Specifications (Section 8), ONLY use findings that trace back to actual source code reads. If the only evidence is a documentation file, flag as [UNVERIFIED — doc-only] and exclude from architecture diagrams.
12. Every FR in TDD Section 5.1 must trace back to a PRD epic or user story. Cite the epic ID in the FR row's "Source" column. If no PRD epic can be identified for an FR, mark it "[NO PRD TRACE]" and flag it as a gap.
13. TDD Section 4.2 (Business Metrics, if included) must include at least one engineering proxy metric for each business KPI listed in the PRD's Section 4 and Section 19. Format as: Business KPI: [PRD KPI name] — Engineering Proxy: [measurable technical metric].

CRITICAL — Incremental File Writing:
You MUST write to your output file incrementally as you synthesize each section. Do NOT read all research files into context and attempt a single large write at the end. The process is:
1. Create the output file with a header and your first synthesized section
2. After completing each subsequent section, append it to the output file immediately using Edit
3. Never rewrite the entire file from memory — always append or do targeted edits

This prevents data loss from context limits and ensures partial results survive if the agent is interrupted.

Write the sections in the exact format they should appear in the final document, including all table structures and headers from the template.
```

### Research Analyst Agent Prompt (rf-analyst — Completeness Verification)

```
Perform a completeness verification of all research files for [component].

Analysis type: completeness-verification
Research directory: [research-dir-path]
Research notes file: [research-notes-path]
Tier: [Lightweight/Standard/Heavyweight]
Output path: [output-path]

Your job is to independently verify that research agents produced thorough, evidence-based findings
before downstream synthesis begins. You are the analytical quality gate — be rigorous.

PROCESS:
1. Read the research-notes.md file to understand the planned scope (EXISTING_FILES, SUGGESTED_PHASES)
2. Use Glob to find ALL research files in the research directory (files matching [NN]-*.md)
3. Read EVERY research file — do not skip any
4. Apply the 8-item Research Completeness Verification checklist
5. Write your report to [output-path]

CHECKLIST:
1. Coverage audit — every key file/subsystem from scope covered by at least one research file
2. Evidence quality — claims cite specific file paths, line numbers, function names
3. Documentation staleness — all doc-sourced claims tagged [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED]
4. Completeness — every file has Status: Complete, Summary section, Gaps section, Key Takeaways
5. Cross-reference check — cross-cutting concerns covered by multiple agents are cross-referenced
6. Contradiction detection — conflicting findings about the same component surfaced
7. Gap compilation — all gaps unified, deduplicated, and severity-rated (Critical/Important/Minor)
8. Depth assessment — investigation depth matches the stated tier (data models documented, API surfaces mapped, architecture patterns identified)

VERDICTS:
- PASS: All checks pass, no critical gaps
- FAIL: Critical gaps exist (list each with specific remediation action)

Use the full output format from your agent definition (tables for coverage, evidence quality, staleness, completeness).
Be adversarial — your job is to find problems, not confirm things work.
```

### Research QA Agent Prompt (rf-qa — Research Gate)

```
Perform QA verification of research completeness for [component].

QA phase: research-gate
Research directory: [research-dir-path]
Analyst report: [analyst-report-path] (if exists, verify the analyst's work; if not, perform full verification)
Research notes file: [research-notes-path]
Tier: [Lightweight/Standard/Heavyweight]
Output path: [output-path]

You are the last line of defense before synthesis begins. Assume everything is wrong until you verify it.

IF ANALYST REPORT EXISTS:
1. Read the analyst's completeness report
2. Spot-check 3-5 of their coverage audit claims (verify the scope items are actually covered)
3. Validate gap severity classifications (are "Critical" really critical? Are "Minor" really minor?)
4. Check their verdict against your own independent assessment
5. Apply the 10-item Research Gate checklist

IF NO ANALYST REPORT:
Apply the full 10-item Research Gate checklist independently.

10-ITEM CHECKLIST:
1. File inventory — all research files exist with Status: Complete and Summary
2. Evidence density — sample 3-5 claims per file, verify file paths exist
3. Scope coverage — every key file from research-notes EXISTING_FILES examined
4. Documentation cross-validation — all doc-sourced claims tagged, spot-check 2-3 CODE-VERIFIED
5. Contradiction resolution — no unresolved conflicting findings
6. Gap severity — Critical gaps block synthesis, Important reduce quality, Minor are lower priority but must still be fixed
7. Depth appropriateness — matches the tier expectation
8. Integration point coverage — connection points documented
9. Pattern documentation — code patterns and conventions captured
10. Incremental writing compliance — files show iterative structure, not one-shot

VERDICTS:
- PASS: Green light for synthesis
- FAIL: ALL findings must be resolved. Only PASS or FAIL — no conditional pass.

Use the full QA report output format from your agent definition.
Zero tolerance — if you can't verify it, it fails.
```

### Synthesis QA Agent Prompt (rf-qa — Synthesis Gate)

```
Perform QA verification of synthesis files for [component].

QA phase: synthesis-gate
Research directory: [research-dir-path]
Fix authorization: [true/false]
Output path: [output-path]

You are verifying that synthesis files are ready for assembly into the final TDD.
If fix_authorization is true, you can fix issues in-place using Edit.

PROCESS:
1. Use Glob to find ALL synth files (synth-*.md) in the synthesis directory
2. Read EVERY synth file completely
3. Apply the 12-item Synthesis Gate checklist
4. For each issue found:
   a. Document the issue (what, where, severity)
   b. If fix_authorization is true: fix in-place with Edit, verify the fix
   c. If fix_authorization is false: document the required fix
5. Write your QA report to [output-path]

12-ITEM CHECKLIST:
1. Section headers match TDD template (docs/docs-product/templates/tdd_template.md)
2. Table column structures correct (FR/NFR numbering, assessment tables, SLO/SLI tables)
3. No fabrication (sample 5 claims per file, trace to research files)
4. Evidence citations use actual file paths
5. Architecture sections include diagrams (ASCII or Mermaid)
6. Requirements use FR-001/NFR-001 ID numbering with priority and acceptance criteria
7. Cross-section consistency (requirements trace to architecture, risks to mitigations)
8. No doc-only claims in Architecture (Section 6), Data Models (Section 7), or API Specs (Section 8)
9. Stale docs surfaced in Open Questions (Section 22)
10. Content rules compliance (tables over prose, no code reproductions)
11. All expected sections have content (no placeholders)
12. No hallucinated file paths (verify parent directories exist)

VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found (list with specific fixes, note which were fixed in-place)
```

### Report Validation QA Agent Prompt (rf-qa — Report Validation)

```
Perform final QA validation of the assembled TDD for [component].

QA phase: report-validation
Report path: [report-path]
Research directory: [research-dir-path]
Template path: docs/docs-product/templates/tdd_template.md
Output path: [output-path]
Fix authorization: true (always authorized for report validation)

This is the final quality check before presenting to the user. You can and should fix issues in-place.

PROCESS:
1. Read the ENTIRE TDD document
2. Apply the 15-item Validation Checklist + 4 Content Quality Checks
3. For each issue: document it, fix it in-place with Edit, verify the fix
4. Write your QA report to [output-path]

15-ITEM VALIDATION CHECKLIST:
1. All template sections present (or explicitly marked as N/A with rationale per tier)
2. Frontmatter has all required fields from the template
3. Total line count within tier budget (Lightweight: 300-600, Standard: 800-1400, Heavyweight: 1400-2200)
4. Document purpose block with tiered usage table present
5. Document Information table has all 7 rows plus Approvers table
6. Numbered Table of Contents present
7. Requirements use FR/NFR ID numbering with priority
8. Architecture section includes at least one diagram (ASCII or Mermaid)
9. Alternative 0: Do Nothing is present in Alternatives Considered
10. SLO/SLI tables present for Standard and Heavyweight tiers
11. No full source code reproductions (interfaces, function bodies, config files)
12. All file paths reference actual files that exist
13. Document History table present
14. Tables use correct column structure from template
15. No doc-sourced architectural claims presented as verified without code cross-validation tags

CONTENT QUALITY CHECKS:
16. Table of Contents accuracy (matches actual section headers)
17. Internal consistency (no contradictions between sections)
18. Readability (scannable — tables, headers, bullets)
19. Web research findings include source URLs for every external claim
20. Actionability (engineer could begin implementation from the Architecture, Data Models, and API Specifications alone)

Fix every issue you find. Report honestly.
```

### Assembly Agent Prompt (rf-assembler — TDD Assembly)

```
Assemble the final Technical Design Document for [component] from synthesis files.

Component files (in order):
[ordered list of synth file paths]

Output path: [tdd-output-path]
Research directory: [research-dir-path]
Template reference: docs/docs-product/templates/tdd_template.md

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create the output file immediately with the TDD frontmatter and header:
   - Fill in all template frontmatter fields. Set status: "🟡 Draft", populate created_date, parent_doc (link to PRD if applicable), depends_on, tags
   - Write the document purpose block with tiered usage table
   - Write the Document Information table

2. As you assemble each section, IMMEDIATELY write it to the output file using Edit.
   Do NOT accumulate the entire TDD in context and attempt a single write.

3. After each Edit, the file grows. This is correct behavior. Never rewrite from scratch.

Assembly rules:
1. Start with template frontmatter, then document header, then Document Information table
2. Assemble sections in template order — read each synth file and write its content into the correct position
3. Write each section to disk immediately after composing it — do NOT one-shot
4. Sections not assigned a synth file (27. References, 28. Glossary) get written directly during assembly
5. Generate the Table of Contents from actual section headers after all sections are placed
6. Add Appendices — Detailed API Specifications, Database Schema, Wireframes, Performance Test Results as applicable
7. Add Document History — initial entry
8. Add Document Provenance — if created from PRD or by consolidating existing docs, document source materials and creation method
9. Cross-check internal consistency:
   - Requirements in Section 5 trace to architecture in Section 6
   - Risks in Section 20 have mitigations
   - Open Questions in Section 22 aren't answered elsewhere
   - Dependencies in Section 18 are complete
10. Flag any contradictions between sections
11. Ensure no placeholder text remains (search for [, TODO, TBD, PLACEHOLDER)

Content rules (non-negotiable):
- Architecture: ASCII or Mermaid diagrams with component tables, not multi-paragraph prose
- Data models: Entity tables with Field / Type / Required / Description / Constraints
- API specs: Endpoint overview tables plus key endpoint details with request/response examples
- Requirements: FR/NFR split with ID numbering (FR-001, NFR-001)
- Testing: Test pyramid tables by level with coverage targets and tools
- Performance: Budget tables with specific metrics and measurement methods
- Security: Threat model tables plus security controls with verification methods
- Alternatives: Structured Pros/Cons with mandatory "Why Not Chosen" and Do Nothing option
- Dependencies: Tables with Version / Purpose / Risk Level / Fallback
- SLOs: SLO / SLI / Error Budget tables with burn-rate alerts
- Evidence cited inline: file.cpp:123, ClassName::method()

CRITICAL: You are assembling existing content from synthesis files, not creating new findings.
Preserve fidelity to the synthesis files. Add only minimal transitional text for coherence.
Do NOT attempt full content validation — that is the QA agent's job. Focus on assembly
integrity: correct ordering, internal consistency, no placeholders, all components included.

Consolidation protocol (when consolidating existing docs into this TDD):
1. Read each source document listed in the task's "Source Files to Consolidate" section
2. Map each source document's content to the corresponding template section(s)
3. Where source docs overlap, merge by keeping the most specific/recent information and noting conflicts
4. Add an Appendix: Document Provenance subsection listing each source doc with its path, original purpose, and which sections it contributed to
5. Zero content loss — every metadata piece and unique finding from source docs must appear in the final output or be explicitly noted as superseded
6. After assembly, the source docs should be candidates for archival (the TDD replaces them)
```

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

## Output Structure

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

The final TDD follows the template at `docs/docs-product/templates/tdd_template.md`. The synthesis agents produce sections that are assembled into this format.

```markdown
---
[frontmatter from template]
---

# [Component Name] - Technical Design Document (TDD)

**Document Type:** Technical Design Document (Engineering Specification)
**Purpose:** [one-sentence purpose]
**Date:** [today]
**Tier:** [Lightweight / Standard / Heavyweight]
**Parent PRD:** [link to Product PRD, if applicable]

---

## Document Information
Component metadata table and Approvers table.

## Table of Contents
[Generated from section headers]

---

## 1. Executive Summary
Key deliverables, high-level scope, 2-3 paragraph overview.

## 2. Problem Statement & Context
Background, problem statement, business context, PRD reference.

## 3. Goals & Non-Goals
Goals with success criteria, explicit non-goals with rationale, future considerations.

## 4. Success Metrics
Technical metrics and business KPIs with baselines, targets, and measurement methods.

## 5. Technical Requirements
Functional requirements (FR-001 numbering), non-functional requirements (performance, scalability, reliability, SLOs, security).

## 6. Architecture
High-level architecture, component diagram, system boundaries, key design decisions, multi-tenancy (if applicable).

## 7. Data Models
Data entities with field tables, data flow diagrams, storage strategy.

## 8. API Specifications
Endpoint overview, detailed endpoint specs, error response format, API governance & versioning.

## 9. State Management (if applicable — frontend)
State architecture, state shape, state transitions.

## 10. Component Inventory (if applicable — frontend)
Page/route structure, shared components, component hierarchy.

## 11. User Flows & Interactions
Sequence diagrams, step-by-step flows, success criteria, error scenarios.

## 12. Error Handling & Edge Cases
Error categories, edge cases, graceful degradation, retry strategies.

## 13. Security Considerations
Threat model, security controls, sensitive data handling, data governance & compliance.

## 14. Observability & Monitoring
Logging, metrics, tracing, alerts, dashboards, business metric instrumentation.

## 15. Testing Strategy
Test pyramid, test cases (unit/integration/E2E), test environments.

## 16. Accessibility Requirements
WCAG 2.1 AA requirements and testing tools.

## 17. Performance Budgets
Frontend performance, backend performance, performance testing.

## 18. Dependencies
External, internal, and infrastructure dependencies.

## 19. Migration & Rollout Plan
Migration strategy, feature flags & progressive delivery, rollout stages, rollback procedure.

## 20. Risks & Mitigations
Risk table with probability, impact, mitigation, and contingency.

## 21. Alternatives Considered
Alternative 0: Do Nothing (mandatory), plus additional alternatives with pros/cons.

## 22. Open Questions
Question tracking table with owner, target date, status, resolution.

## 23. Timeline & Milestones
High-level timeline and implementation phases with exit criteria.

## 24. Release Criteria
Definition of Done checklist, release checklist.

## 25. Operational Readiness
Runbook, on-call expectations, capacity planning.

## 26. Cost & Resource Estimation (if applicable)
Infrastructure costs, cost scaling model, optimization opportunities.

## 27. References & Resources
Related documents and external references.

## 28. Glossary
Term definitions.

## Document History
Version table.

## Appendices
A: Detailed API Specifications, B: Database Schema, C: Wireframes, D: Performance Test Results.
```

---

## Synthesis Mapping Table

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

Maps synth files to TDD template sections and their source research files. Synthesis agents use this mapping to know which template sections they are responsible for and which research files to draw from.

| Synth File | Template Sections | Source Research Files |
|------------|-------------------|----------------------|
| `synth-01-exec-problem-goals.md` | 1. Executive Summary, 2. Problem Statement & Context, 3. Goals & Non-Goals, 4. Success Metrics | PRD extraction, architecture overview, existing docs |
| `synth-02-requirements.md` | 5. Technical Requirements | PRD extraction, architecture overview, all subsystem research |
| `synth-03-architecture.md` | 6. Architecture | architecture overview, integration points, subsystem research, 00-prd-extraction.md (Section 4: Technical Requirements — architectural constraints) |
| `synth-04-data-api.md` | 7. Data Models, 8. API Specifications | data models research, API surface research, web research (API standards, schema patterns), 00-prd-extraction.md (Section 2: User Stories and ACs — data model traceability) |
| `synth-05-state-components.md` | 9. State Management, 10. Component Inventory, 11. User Flows | state management research, subsystem research, 00-prd-extraction.md (Section 2: User Stories and ACs — interaction flows; Section 5: Scope Boundaries) |
| `synth-06-error-security.md` | 12. Error Handling & Edge Cases, 13. Security Considerations | security research, all subsystem research, web research (security patterns, threat models), 00-prd-extraction.md (Section 4: Technical Requirements — security and error-handling constraints) |
| `synth-07-observability-testing.md` | 14. Observability & Monitoring, 15. Testing Strategy | architecture overview, integration points, web research (SLO benchmarks, testing patterns), 00-prd-extraction.md (Section 3: Success Metrics — KPIs to translate into observability targets; Section 2: ACs — acceptance criteria driving test coverage) |
| `synth-08-perf-deps-migration.md` | 16. Accessibility, 17. Performance Budgets, 18. Dependencies, 19. Migration & Rollout | PRD extraction, architecture overview, all subsystem research, web research (performance benchmarks) |
| `synth-09-risks-alternatives-ops.md` | 20. Risks, 21. Alternatives Considered, 22. Open Questions, 23. Timeline, 24. Release Criteria, 25. Operational Readiness, 26. Cost | PRD extraction, all research files, web research (industry practices), gaps log |

**PRD extraction fallback:** When `00-prd-extraction.md` is absent (no PRD provided), synthesis agents skip PRD-sourced content for that mapping row and note "PRD source unavailable -- requirements derived from feature description and codebase research" in the synthesis file. Do not fail or block on the missing file.

Adjust the mapping based on component complexity. Backend components skip Section 9 (State Management) and Section 10 (Component Inventory). Small components can combine more sections per synth file.

---

## Synthesis Quality Review Checklist

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

**This checklist is enforced by the rf-analyst and rf-qa agents** (see Phase 5 in the task phases). The rf-analyst applies these 9 criteria as its Synthesis Quality Review analysis type, and the rf-qa agent independently verifies the analyst's findings with its expanded 12-item Synthesis Gate checklist. The QA agent can fix issues in-place when authorized.

The 9 criteria (used by rf-analyst):

1. Template section headers match the TDD template exactly (`docs/docs-product/templates/tdd_template.md`)
2. Tables use the correct column structure (FR/NFR ID numbering, entity tables with Field/Type/Required/Description/Constraints, SLO/SLI/Error Budget tables)
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and evidence (not vague descriptions)
5. Architecture sections include at least one diagram (ASCII or Mermaid) with component relationships
6. Requirements use FR-001/NFR-001 ID numbering with priority and acceptance criteria
7. All cross-references between sections are consistent (requirements trace to architecture decisions, risks trace to mitigations, dependencies trace to integration points)
8. **No doc-only claims in Architecture (Section 6), Data Models (Section 7), or API Specs (Section 8).** Only `[CODE-VERIFIED]` findings may appear as current architecture. If the only evidence is a documentation file, reject and flag as `[UNVERIFIED — doc-only]`
9. **Stale documentation discrepancies are surfaced.** Any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings from research files should appear in Open Questions (Section 22), not silently omitted

The rf-qa agent's Synthesis Gate adds 4 additional checks (10-13): content rules compliance, section completeness, hallucinated file path detection, and PRD traceability. If synthesis QA fails, the QA agent fixes issues in-place (when authorized) and issues remaining unfixed trigger re-synthesis of the affected files.

13. **FR traceability** — spot-check 3 FRs in the synth-04 output: each must cite a PRD epic ID in its Source column. If any FR lacks a PRD epic citation and is not marked "[NO PRD TRACE]", flag as FAIL.

---

## Assembly Process

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction. This section provides supplementary context for understanding the workflow.

### Step 8: Assemble the TDD

Read all synth files in order and assemble the final document:

1. **Start with the template frontmatter** — fill in all fields from the template. Set `status: "🟡 Draft"`, populate `created_date`, `parent_doc` (link to PRD if applicable), `depends_on`, `tags`, etc.

2. **Write the document header** — the purpose block with document type, relationship to PRD, and tiered usage table.

3. **Write the Document Information table** — Component Name, Component Type, Tech Lead, Engineering Team, Target Release, Last Updated, Status. Include the Approvers table.

4. **Assemble sections in template order** — paste each synth file's content into the correct position. Sections that weren't assigned a synth file (27. References, 28. Glossary) get written directly during assembly from patterns observed in the synth files.

5. **Write the Table of Contents** — generate from actual section headers.

6. **Add Appendices** — Detailed API Specifications, Database Schema, Wireframes, Performance Test Results as applicable.

7. **Add Document History** — initial entry.

8. **Add Document Provenance** — if the TDD was created by consolidating existing docs or from a PRD, add an `Appendix: Document Provenance` subsection documenting the source materials and creation method. Zero content loss: every piece of metadata from source documents must appear somewhere in the TDD.

See the standalone `## Validation Checklist` section below for the full pre-presentation validation checklist.

### Step 10: Present to User

Notify the user:
- Where the final document was written
- Line count and tier classification
- Number of sections populated vs skipped
- Where the research/synth artifacts live (for future reference)
- Any gaps or areas that need manual review

### Step 11: Clean Up Consolidation Sources

If the TDD was created by consolidating existing docs:
- Do NOT delete the source docs automatically
- Present the source docs to the user and confirm they can be archived
- Archive approved sources to `docs/archive/[appropriate-subdir]/`
- Update any references to the archived files in other documents
- Check off items in the stub's consolidation checklist if one exists

---

## Validation Checklist

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

Before presenting the TDD to the user, validate against this checklist (this is encoded in the task file's Assembly phase):

**Structural Completeness:**
- [ ] Frontmatter has all required fields from the template (id, title, status, created_date, parent_doc, depends_on, tags)
- [ ] Document purpose block with tiered usage table present
- [ ] Document Information table has all 7 rows (Component Name, Component Type, Tech Lead, Engineering Team, Target Release, Last Updated, Status) plus Approvers table
- [ ] Table of Contents present and matches actual section headers exactly — no orphaned or missing entries
- [ ] All 28 template sections present (or explicitly marked as N/A with rationale per tier)
- [ ] Total line count within tier budget (Lightweight: 300-600, Standard: 800-1400, Heavyweight: 1400-2200)

**Architecture & Design Quality:**
- [ ] Architecture section (Section 6) includes at least one diagram (ASCII or Mermaid) showing component relationships
- [ ] Data model definitions complete with entity tables (Field / Type / Required / Description / Constraints columns)
- [ ] API contracts specified with endpoint overview tables, request/response examples, and error response format
- [ ] Integration points mapped — system boundaries table populated with upstream, downstream, and external boundaries
- [ ] Key Design Decisions table populated with rationale and alternatives considered
- [ ] Alternative 0: Do Nothing is present in Alternatives Considered (Section 21)

**Requirements & Specifications:**
- [ ] Requirements use FR-001/NFR-001 ID numbering with priority (Must Have / Should Have / Could Have) and acceptance criteria
- [ ] SLO/SLI/Error Budget tables present for Standard and Heavyweight tiers
- [ ] Performance budgets specified with concrete metrics and measurement methods
- [ ] Security considerations documented — threat model, security controls, sensitive data handling

**Evidence & Integrity:**
- [ ] No fabricated claims — all architecture and implementation descriptions backed by `[CODE-VERIFIED]` tags
- [ ] No doc-sourced architectural claims presented as verified without cross-validation tags
- [ ] All `[CODE-CONTRADICTED]` or `[STALE DOC]` findings surfaced in Open Questions (Section 22)
- [ ] All file paths reference actual files that exist (spot-check 5+ paths)
- [ ] No full source code reproductions (interfaces, function bodies, config files)
- [ ] Web research findings include source URLs for every external claim

**Document Quality:**
- [ ] Document History table present with initial entry
- [ ] Tables use correct column structure from template
- [ ] Internal consistency — no contradictions between sections (requirements trace to architecture, risks to mitigations, dependencies to integration points)
- [ ] Readability — scannable structure with tables, headers, bullets; no walls of prose

---

## Content Rules (From Template — Non-Negotiable)

These rules come from the template's structure and conventions. Every TDD must follow them.

| Rule | Do | Don't |
|------|-----|-------|
| **Architecture** | ASCII or Mermaid diagrams with component tables | Multi-paragraph prose for what could be a diagram |
| **Data models** | Entity tables with Field / Type / Required / Description / Constraints | Full TypeScript interface reproductions |
| **API specs** | Endpoint overview tables plus key endpoint details with request/response examples | Reproducing entire OpenAPI specs inline |
| **Requirements** | Functional/Non-functional split with ID numbering (FR-001, NFR-001) | Prose paragraphs mixing requirement types |
| **Testing** | Test pyramid tables by level with coverage targets and tools | Generic "write tests" instructions |
| **Performance** | Budget tables with specific metrics and measurement methods | Vague "should be fast" requirements |
| **Security** | Threat model tables plus security controls with verification methods | General security platitudes without specifics |
| **Alternatives** | Structured Pros/Cons with mandatory "Why Not Chosen" and Do Nothing option | Surface-level dismissal of alternatives |
| **Dependencies** | Tables with Version / Purpose / Risk Level / Fallback | Inline dependency mentions scattered through prose |
| **SLOs** | SLO / SLI / Error Budget tables with burn-rate alerts | Undefined or aspirational reliability targets |
| **Source code** | Summarize behavior with key signatures | Reproduce full function bodies or config files |
| **Evidence** | Inline citations: `file.cpp:123`, `ClassName::method()` | Say "the code does X" without citing where |
| **Uncertainty** | Explicit "Unverified" or "Open Question" markers | Present uncertain findings as verified facts |

**General content principles:**
- Tables over prose whenever presenting multi-item data
- Conciseness over comprehensiveness — the TDD should be scannable, not exhaustive prose
- Every claim needs evidence — if you can't cite a file path or URL, it belongs in Open Questions
- Prefer ASCII/Mermaid diagrams for visual relationships over paragraph descriptions

---

## Critical Rules (Non-Negotiable)

These are SKILL-SPECIFIC content rules that apply across ALL phases. Violations compromise document quality.

Three execution-discipline rules (task-file-source-of-truth, maximize-parallelism, use-dedicated-tools) are enforced by the `/task` skill and do not appear here. The incremental-writing mandate is retained as Rule 9 below because it is a content-quality requirement specific to this skill's multi-agent research pipeline, not just an execution mechanism.

1. **Codebase is source of truth.** For claims about current architecture, code overrides documentation. Web research supplements with technology context but never overrides verified code findings.

2. **Evidence-based claims only.** Every finding must cite actual file paths, class names, function signatures. No assumptions, no inferences, no guessing. If you can't verify it, mark as "Unverified — needs confirmation."

3. **Gap-driven web research.** Do not web search everything up front. First investigate the codebase thoroughly (Phase 2), identify specific gaps, then target web research (Phase 4) at those gaps.

4. **Documentation is not verification.** Internal documentation describes intent or historical state — NOT necessarily current state. A doc saying "Service X exists at path Y" does not prove Service X exists. Only reading actual source code proves it.

5. **Preserve research artifacts.** Research, web research, and synthesis files persist after the document is written. They serve as the evidence trail for all claims.

6. **Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. The synthesis phase relies on these connections.

7. **Report all uncertainty.** If something is unclear, ambiguous, or requires a judgment call, flag it explicitly. Do not silently pick one interpretation and present it as fact.

8. **Quality gate mandate.** Quality gates are enforced at three points: after research (Phase 3 — rf-analyst completeness verification + rf-qa research gate, spawned IN PARALLEL), after synthesis (Phase 5 — rf-analyst synthesis review + rf-qa synthesis gate, spawned IN PARALLEL), and after assembly (Phase 6 — rf-qa report validation only, since the assembler already consolidated and the QA agent validates the final document with fix authorization). Skipping any gate compromises TDD quality.

9. **No one-shotting documents.** Agents must write incrementally as they discover information. The assembler must write the final TDD section by section. This is non-negotiable — one-shotting hits token limits and loses all accumulated work.

10. **Default to Standard.** Unless the component is clearly documentable with a quick scan of <5 files, use the Standard tier. When in doubt, go Standard.

11. **Docs-vs-code has the same trust hierarchy as web-vs-code.** Rule 1 establishes that web research never overrides code. The same applies to internal documentation: if a doc describes an architecture that contradicts what the code shows, **the code is correct and the doc is stale**. Treat internal docs with the same skepticism as external blog posts unless code-verified.

12. **Design specifications must be actionable.** Architecture, data models, and API specifications should contain enough detail that an engineer could begin implementation from the TDD alone. Include specific file paths, code patterns to follow, and integration points.

13. **Anti-orphaning rule.** Task-completion items (status update, Task Log entry, frontmatter update) MUST be checklist items within the final phase of the task file, not in a separate Post-Completion section. This ensures they are executed by the F1 loop and not orphaned.

14. **Partitioning thresholds.** When >6 research files exist (Phase 3) or >4 synthesis files exist (Phase 5), spawn MULTIPLE analyst and QA instances in parallel, each with an `assigned_files` subset. This prevents context rot when any single agent would need to hold too many files in context.

---

## Research Quality Signals

### Strong Investigation Signals
- Findings cite specific file paths and line numbers
- Data flow is traced end-to-end, not just entry points
- Integration points are mapped with actual function signatures
- Existing patterns identified that can inform the design
- Gaps are specific and actionable ("function X doesn't handle case Y")
- Doc-sourced claims carry verification tags
- rf-analyst completeness report shows PASS verdict
- rf-qa research gate shows PASS

### Weak Investigation Signals (Redo)
- Vague descriptions without file paths ("the system uses a plugin architecture")
- Assumptions stated as facts ("this probably works by...")
- Missing gap analysis (everything seems fine — unlikely for non-trivial systems)
- No cross-references between research files
- Doc-sourced architectural claims reported without code verification tags
- rf-analyst or rf-qa reports show FAIL with critical gaps
- Data model shapes undocumented despite being in scope

### When to Spawn Additional Agents
- A research agent flags a gap that's critical to the design
- Two agents' findings contradict each other — need a tie-breaker investigation
- The scope turns out larger than initially estimated
- A new subsystem is discovered during investigation that wasn't in the original plan
- Web research reveals patterns that need codebase verification

---

## Artifact Locations

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}${TASK_ID}.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| PRD extraction file | `${TASK_DIR}research/00-prd-extraction.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Gaps log | `${TASK_DIR}gaps-and-questions.md` |
| Analyst reports | `${TASK_DIR}qa/analyst-[gate]-report.md` |
| QA reports | `${TASK_DIR}qa/qa-[gate]-report.md` |
| QA report (qualitative review) | `${TASK_DIR}qa/qa-qualitative-review.md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Final TDD | `docs/[domain]/TDD_[COMPONENT-NAME].md` |
| Template schema | `docs/docs-product/templates/tdd_template.md` |

Research and synthesis files persist in the task folder — they serve as the evidence trail for claims in the TDD and can be re-used when the document needs updating.

---

## PRD-to-TDD Pipeline

When a PRD is provided as input, the TDD creation follows an enhanced flow:

1. **PRD Extraction** (Step 1.2) — read the PRD and extract requirements, constraints, success metrics, and scope boundaries into `${TASK_DIR}research/00-prd-extraction.md`
2. **Requirements Traceability** — every requirement in the TDD's Section 5 should trace back to a PRD epic or user story where applicable
3. **Success Metrics Alignment** — TDD Section 4 (Success Metrics) should include engineering proxy metrics for business KPIs defined in the PRD
4. **Scope Inheritance** — TDD Section 3 (Goals & Non-Goals) inherits scope boundaries from PRD Section 12 (Scope Definition)
5. **Cross-referencing** — the TDD frontmatter's `parent_doc` field links back to the PRD

This pipeline ensures that product requirements are faithfully translated into engineering specifications without information loss or scope drift.

---

## Updating an Existing TDD

When the user wants to update (not create) an existing TDD:

1. Read the current document to understand what's already covered
2. Research only the changed/new areas (don't re-research everything)
3. Write new research files for the changes: `${TASK_DIR}research/update-[date]-[topic].md`
4. Edit the relevant sections of the TDD in place
5. Update the Document Information table with the new Last Updated date
6. Update Document History with what changed

---

## Session Management

Session management is provided by the `/task` skill. Task files are located at `.dev/tasks/to-do/TASK-TDD-*/TASK-TDD-*.md` and research artifacts at `${TASK_DIR}research/`. On session restart, `/task` finds the task file, reads it, and resumes from the first unchecked item.
