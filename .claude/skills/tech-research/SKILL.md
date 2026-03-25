---
name: tech-research
description: "Deep technical investigation and feasibility research across the codebase. Produces structured research reports with findings, gap analysis, options, and detailed implementation recommendations. Use this skill when the user wants to research how something works, investigate a technical problem, figure out what needs to be built or changed, do a feasibility study, or deep dive into a system or integration. Trigger on phrases like 'research how X works', 'investigate this', 'figure out what we need for X', 'feasibility study', 'deep dive into X', 'how does X work and what do we need to change', 'tech research on X', 'what would it take to build X', 'analyze this system', or 'research this problem'. Also trigger when the user says 'research' in the context of understanding a technical problem or planning an implementation."
---

# Technical Research & Investigation

A skill for deep technical investigation across the codebase. This skill uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts.

**How it works:** The skill performs initial scope discovery, then spawns the `rf-task-builder` subagent to create an MDTM task file encoding all investigation phases. The skill then executes from that task file, marking items complete as it progresses. If context compresses or the session restarts, the skill re-reads the task file and resumes from the first unchecked item.

This skill fills the gap between `repo-cleanup` (audits what exists) and `tech-reference` (documents what's built). `tech-research` **investigates a problem and recommends what to build or change**.

## Why This Process Works

Technical investigations fail when they rely on assumptions, memory, or surface-level reading. This skill forces every claim through codebase verification — parallel agents read actual source files, trace actual data flows, and document actual behavior with file paths and line numbers.

The MDTM task file provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off.

The multi-phase structure (scope discovery → deep investigation → **analyst verification** → web research → synthesis → **synthesis QA** → assembly → **report validation** → **qualitative review**) prevents four common failure modes:
- **Context rot** — By isolating each investigation topic in its own subagent with its own output file, no single agent needs to hold the entire investigation in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning many parallel agents (each focused on one slice), the investigation goes deep on every aspect simultaneously rather than skimming across everything sequentially.
- **Hallucinated recommendations** — By separating research (what exists) from synthesis (what it means) from assembly (the final report), each phase can be verified independently. Synthesis agents only work from verified research files, not from memory or inference.
- **Uncaught quality drift** — Dedicated `rf-analyst`, `rf-qa`, and `rf-qa-qualitative` agents provide independent verification at three critical gates: after research (completeness + evidence quality), after synthesis (accuracy + structure), and after assembly (structural report validation + qualitative content review). This follows the same analyst→QA pattern used in the recipe pipeline, adapted for technical research outputs. The QA agents assume everything is wrong until independently verified — zero-trust verification prevents rubber-stamping.

The research artifacts persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and feed directly into downstream skills like `tech-reference`.

### Variable Reference

Every invocation creates a self-contained folder. All paths below are relative to this folder:

```
TASK_ID:     TASK-RESEARCH-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/
SYNTHESIS:   ${TASK_DIR}synthesis/
QA:          ${TASK_DIR}qa/
REVIEWS:     ${TASK_DIR}reviews/
```

---

## Input

The skill needs four pieces of information to produce an actionable report. The first is mandatory; the rest are optional but dramatically improve output quality.

1. **WHAT to investigate** (mandatory) — A clear problem, question, or system to research. Not just a topic name — what you actually want to understand or solve.

2. **WHY / what problem to solve** (strongly recommended) — What prompted this investigation and what you want to do with the findings. This shapes whether the report emphasizes understanding, feasibility, options, or implementation planning.

3. **WHERE to look** (optional, saves significant time) — Specific directories, plugins, docs, or subsystems to focus on. Prevents agents from spending time on irrelevant areas.

4. **WHAT kind of output you need** (optional, shapes the report) — Whether you need a decision ("should we do X or Y?"), an implementation plan ("what do we need to build?"), understanding ("how does this work end-to-end?"), or feasibility ("can we do X given our architecture?").

### Effective Prompt Examples

**Strong — all four pieces present:**
> How do GameFrame locomotion parameters get modified at runtime? Data table modifications don't work for locomotion because the GE uses OVERRIDE operations. The Advanced Data Editor (GameTune) plugin handles this via `ApplyCSVDataToSelf()` with hot reload. Research how ADE does this, what GFxAI's agents or UE manager would need to replicate this capability, and recommend an implementation approach. Key areas: `docs/plugin-integration/v0.1/`, the IBSFLocomotion and IBSFAdvancedDataEditor plugins, `ue_manager/`, and `backend/app/agents/`.

**Strong — clear question + scope + output type:**
> What would it take to add a new specialist agent (e.g., UI Designer) to the multi-agent system? Research the current agent registration, routing, tool assignment, and memory isolation patterns. I need an implementation plan with specific files to create/modify. Scope: `backend/app/agents/`, `backend/app/services/`.

**Strong — feasibility focus:**
> Can we replace our current VM-per-session pixel streaming approach with a shared GPU pool? Research the current session lifecycle, GPU resource allocation, and streaming architecture. I need options with effort/risk tradeoffs. Scope: `ue_manager/`, `infrastructure/`, `docs/pixel-streaming/`.

**Weak — topic only (will work but produces broader, less actionable results):**
> Research the agent system.

**Weak — no "why" (agents won't know what to recommend):**
> Research locomotion.

### What to Do If the Prompt Is Incomplete

If the user provides only a topic name or a vague request, **do NOT proceed immediately**. Ask the user to clarify using this template:

> I can research [topic] for you. To make the investigation focused and the recommendations actionable, can you help me with:
>
> 1. **What specifically do you want to understand?** (e.g., "how does X work", "why does Y fail", "what would it take to build Z")
> 2. **What are you trying to achieve?** (e.g., "we need to modify locomotion params at runtime", "we want to add a new agent type")
> 3. **Any specific areas of the codebase I should focus on?** (directories, plugins, services)
> 4. **What kind of output do you need?** (understanding, implementation plan, options comparison, feasibility assessment)

Proceed once you have at least #1 answered clearly. Items #2-4 improve quality but aren't blockers.

---

## Depth Tiers

Select a tier based on scope complexity. **Default to Deep** unless the question is clearly narrow and answerable with a quick scan.

| Tier | When to Use | Codebase Agents | Web Agents | Report Depth |
|------|------------|-----------------|------------|-------------|
| **Quick** | Narrow question, single subsystem, <5 relevant files | 1–2 | 0–1 | Problem + findings + recommendation |
| **Standard** | Multi-subsystem, 5–20 files, moderate complexity | 3–5 | 1–2 | Full report, moderate implementation detail |
| **Deep** | Cross-cutting, 20+ files, architectural decisions, integration work | 5–10+ | 2–4 | Full report, detailed implementation plan |

**Tier selection rules:**
- If in doubt, pick Deep
- If the user says "deep dive", "thorough", "comprehensive" — always Deep
- Only use Quick for genuinely narrow questions ("what function handles X?")
- If the scope spans multiple plugins, services, or architectural layers — always Deep

---

## Output Locations

All persistent artifacts go to the task folder `${TASK_DIR}` (see Variable Reference above). The topic slug is derived from the research question (e.g., `locomotion-params`, `ade-hot-reload`, `agent-memory-system`) and used in the TASK_ID.

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}TASK-RESEARCH-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research/research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[aspect-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[section-name].md` |
| Final research report | `${TASK_DIR}RESEARCH-REPORT-[descriptor].md` |
| Gap/question log (interim) | `${TASK_DIR}gaps-and-questions.md` |
| Analyst completeness report | `${TASK_DIR}qa/analyst-completeness-report.md` |
| QA research gate report | `${TASK_DIR}qa/qa-research-gate-report.md` |
| Analyst synthesis review | `${TASK_DIR}qa/analyst-synthesis-review.md` |
| QA synthesis gate report | `${TASK_DIR}qa/qa-synthesis-gate-report.md` |
| QA report validation | `${TASK_DIR}qa/qa-report-validation.md` |
| QA qualitative review | `${TASK_DIR}qa/qa-qualitative-review.md` |

**File numbering convention:** All research, web, and synthesis files use zero-padded sequential numbers: `01-`, `02-`, `03-`, etc. This ensures correct ordering when listing files.

Check for existing task folders in `.dev/tasks/to-do/` before creating new ones — if prior research exists on the same topic (matching `TASK-RESEARCH-*/`), read it first and build on it.

---

## Execution Overview

The skill operates in two stages:

**Stage A — Scope Discovery & Task File Creation (before the task file exists):**
1. Parse the user's research question and triage (Scenario A vs B)
2. Perform scope discovery (depth adjusted by scenario)
3. Write scope discovery results to a structured research notes file
4. Review research sufficiency (mandatory gate)
5. Triage template selection
6. Spawn the task builder to create the MDTM task file
7. Verify the task file

**Stage B — Task File Execution (after the task file exists):**
8. Execute from the task file using the READ → IDENTIFY → EXECUTE → UPDATE → REPEAT loop
9. Each checklist item is a self-contained prompt — no prior context needed

If a task file already exists for this research topic (from a previous session), skip Stage A and resume Stage B from the first unchecked item.

---

## Stage A: Scope Discovery & Task File Creation

### A.1: Check for Existing Task File

Before creating a new task file, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `TASK-RESEARCH-*/` folder related to this topic
2. If found, read the task file inside it (`${TASK_DIR}TASK-RESEARCH-*.md`) and check for unchecked `- [ ]` items
3. If unchecked items exist → skip to Stage B (resume execution)
4. If all items are checked → inform user that research is already complete, offer to re-run or build on existing research
5. Check for existing task folder matching `TASK-RESEARCH-*/` in `.dev/tasks/to-do/`:
   a. If `${TASK_DIR}research/research-notes.md` exists with `Status: Complete` → skip to A.5 (review sufficiency, then build task file)
   b. If `${TASK_DIR}research/research-notes.md` exists with `Status: In Progress` → read it, resume A.3 scope discovery from where it left off, then continue to A.4 to update the file
   c. If task folder exists but no `research-notes.md` → continue with A.3 but use the existing folder
6. If no task folder exists → continue with A.2

### A.2: Parse & Triage the Research Question

Break the research question into structured components:

- **GOAL**: What specifically needs to be investigated (the research question)
- **WHY**: What the user wants to do with the findings (decision, implementation plan, understanding, feasibility)
- **WHERE**: Specific directories, files, or subsystems to focus on
- **OUTPUT_TYPE**: The kind of report needed (options analysis, implementation plan, system understanding, feasibility assessment)
- **TOPIC_SLUG**: A kebab-case identifier for the research directory (e.g., `locomotion-params`, `agent-memory`)

**Triage into Scenario A or B:**

**Scenario A — Explicit request:** User provided most of: goal, source locations, output expectations, specific technical question.
Example: "Research how ADE's ApplyCSVDataToSelf() works for locomotion hot reload. Key areas: docs/plugin-integration/, IBSFLocomotion, IBSFAdvancedDataEditor plugins, ue_manager/, backend/app/agents/"
→ Scope discovery confirms details and fills minor gaps. Lighter exploration.

**Scenario B — Vague request:** User provided a goal but few specifics.
Example: "Research the agent system"
→ Scope discovery does broad exploration to map what exists, identify subsystems, and plan investigation assignments.

**Do NOT interrogate the user with a list of questions.** Proceed with what you have and let scope discovery figure out the rest from the codebase. Only ask the user (via `AskUserQuestion`) if there's a genuine ambiguity about **intent** that can't be inferred from the codebase.

### A.3: Perform Scope Discovery

Use Glob, Grep, and codebase-retrieval to map the problem space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.

**Adjust depth by scenario:**
- **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, scan for related code, identify gaps in what the user specified.
- **Scenario B**: Broad discovery — scan the full codebase for anything touching the topic, map all relevant subsystems, identify documentation, count files.

Discover:
- All files, directories, and plugins that touch the topic
- Existing documentation covering related areas
- Code patterns, classes, functions, and APIs involved
- External integration points (frameworks, engines, third-party systems)
- Count of relevant files and subsystems

Based on the discovery:
- Select depth tier (default: Deep)
- Plan research assignments — divide the investigation into specific topics, each becoming a subagent assignment
- Plan web research topics (from identified gaps)
- Determine the synthesis file mapping

**Research assignment types** (use as many as the topic requires):

| Type | Purpose | What the Agent Does |
|------|---------|-------------------|
| **Code Tracer** | Understand how code actually works | Read implementations, trace data flow, follow imports, document behavior |
| **Doc Analyst** | Extract context from existing documentation | Read docs, **cross-validate every architectural claim against actual code** (see Documentation Staleness Protocol below), note discrepancies and stale content, extract relevant context |
| **Integration Mapper** | Identify connection points | Map APIs, extension points, plugin interfaces, service boundaries, config surfaces |
| **Pattern Investigator** | Find reusable patterns | Search for similar implementations that solve analogous problems |
| **Architecture Analyst** | Understand system design | Trace architectural decisions, dependency chains, component relationships |

Create the task folder: `.dev/tasks/to-do/TASK-RESEARCH-YYYYMMDD-HHMMSS/` with subfolders `research/`, `synthesis/`, `qa/`, `reviews/`

**Optional — spawn rf-task-researcher for complex scope discovery:**

If scope discovery needs deeper context (e.g., Scenario B with a large unknown codebase area, or Scenario A where the specified directories contain deep nested structures), spawn an `rf-task-researcher` subagent. Pass it a RESEARCH_REQUEST describing what to explore. It will write research notes to a file. You then use those notes as input for A.4.

### A.4: Write Research Notes File (MANDATORY)

Write the scope discovery results to a structured research notes file at `${TASK_DIR}research/research-notes.md`. This file is what the builder reads — NOT inline content in the BUILD_REQUEST.

The file MUST be organized into these 6 categories (include all, mark as "N/A" if empty):

```markdown
# Research Notes: [TOPIC]

**Date:** [today]
**Scenario:** [A or B]
**Depth Tier:** [Quick / Standard / Deep]

---

## EXISTING_FILES
[All files, directories, and subsystems found during scope discovery. Per-file detail: path, purpose, key exports, approximate line count. Group by directory or subsystem.]

## PATTERNS_AND_CONVENTIONS
[Code patterns, naming conventions, architectural patterns, design decisions observed. Cite specific files as evidence.]

## SOLUTION_RESEARCH
[If the goal involves building something new: approaches evaluated, tools/libraries considered, external research findings. Mark as "N/A — pure investigation, not implementation" if not applicable.]

## RECOMMENDED_OUTPUTS
[Planned output files: research files, synthesis files, final report. Full paths and purposes.]

## SUGGESTED_PHASES
[Planned investigation breakdown. For each planned research agent:
- Agent number, investigation type, topic
- Files/directories to investigate
- Output file path
- Web research topics identified from gaps
- Synthesis file mapping]

## TEMPLATE_NOTES
[Notes about which MDTM template to use and why. Almost always Template 02 for tech-research.]

## AMBIGUITIES_FOR_USER
[Genuine ambiguities about user intent that cannot be resolved from the codebase. If none, write "None — intent is clear from the request and codebase context."]
```

### A.5: Review Research Sufficiency (MANDATORY GATE)

**You MUST review the research notes before spawning the builder.** This is a quality gate — do NOT skip it.

Read `${TASK_DIR}research/research-notes.md` and evaluate:

1. Are relevant source files identified with specific paths?
2. Are investigation assignments concrete enough for the builder to create per-agent checklist items?
3. Is the synthesis mapping clear (which research files feed which report sections)?
4. Are there unresolved ambiguities that would block the builder?
5. If the goal involves new implementation: are approaches evaluated in SOLUTION_RESEARCH?
6. If any doc-sourced claims appear in the research notes (e.g., from scanning existing documentation during scope discovery), are they tagged with `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`? Claims marked `[CODE-CONTRADICTED]` or `[UNVERIFIED]` must be flagged in AMBIGUITIES_FOR_USER.

**If sufficient** → proceed to A.6 (template triage).

**If insufficient** → either:
- Do additional scope discovery yourself and update the research notes file, OR
- Spawn an rf-task-researcher subagent with specific feedback about what's missing, then re-review

**Maximum 2 gap-fill rounds.** After 2 rounds, proceed with what's available and note remaining gaps in the research notes AMBIGUITIES_FOR_USER section.

Do NOT proceed to the builder with incomplete research notes. The builder cannot explore the codebase effectively — it relies on what you provide.

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

**For tech-research, the answer is almost always Template 02** — the skill inherently involves discovery (Phase 2), parallel agents (Phases 2-4), synthesis (Phase 4), and validation (Phase 5).

### A.7: Build the Task File

Spawn the `rf-task-builder` subagent. The builder reads the research notes file and the MDTM template, then creates the task file. It also reads the SKILL.md itself for phase requirements and agent prompt templates.

**BUILD_REQUEST format for the subagent prompt:**

```
BUILD_REQUEST:
==============
GOAL: Conduct a technical investigation on [GOAL] and produce a structured research report with findings, gap analysis, options, and implementation recommendations. The report will be written to `${TASK_DIR}RESEARCH-REPORT-[descriptor].md`.

WHY: [WHY — what prompted this investigation and what the findings will be used for]

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
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase and write findings files to ${TASK_DIR}research/
- Phase 3 (Completeness Verification): L4 Review/QA — spawn rf-analyst (completeness-verification) then rf-qa (research-gate) as sequential quality gate. Both write reports. QA verdict gates progression.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — agents read research files and produce report sections. Then spawn rf-analyst (synthesis-review) and rf-qa (synthesis-gate) as sequential quality gate. QA can fix issues in-place.
- Phase 6 (Assembly & Validation): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final report, then spawn rf-qa (report-validation) for structural quality check, then spawn rf-qa-qualitative (report-qualitative) for content/logic quality check. Both QA agents have in-place fix authorization.

RESEARCH NOTES FILE:
${TASK_DIR}research/research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, planned investigation assignments, synthesis mapping, and output paths.

SKILL CONTEXT FILE:
.claude/skills/tech-research/SKILL.md
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt. Read the "Report Structure" section for final report format (includes full sub-section scaffolding). Read the "Synthesis Mapping Table" section for the standard synth-file-to-report-section mapping. Read the "Synthesis Quality Review Checklist" section for post-synthesis verification. Read the "Assembly Process" section for report assembly steps. Read the "Validation Checklist" section for Phase 6 validation criteria. Read the "Content Rules" section for writing standards. These must be embedded in the relevant checklist items per B2 self-contained pattern.

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
- Create the task folder at .dev/tasks/to-do/TASK-RESEARCH-YYYYMMDD-HHMMSS/ with `research/`, `synthesis/`, `qa/`, `reviews/` subfolders

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research agent (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md
- Each item specifies: investigation topic, type, files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from SKILL.md) in each checklist item per B2
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. For example, with 8 research assignments: spawn all 8 agents in one message, mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.

Phase 3 — Research Completeness Verification (ANALYST + QA GATE, PARALLEL):
- Spawn `rf-analyst` (subagent_type: "rf-analyst", analysis_type: "completeness-verification") AND `rf-qa` (subagent_type: "rf-qa", qa_phase: "research-gate") IN PARALLEL. Both agents independently read research files and apply their own checklists. The analyst applies its 8-item completeness checklist (coverage audit, evidence quality, doc staleness, completeness, cross-references, contradictions, gap compilation, depth assessment). The QA agent applies its 10-item research-gate checklist (file inventory, evidence density, scope coverage, doc cross-validation, contradiction resolution, gap severity, depth appropriateness, integration points, pattern documentation, incremental writing compliance). The analyst writes to `${TASK_DIR}qa/analyst-completeness-report.md`. The QA agent writes to `${TASK_DIR}qa/qa-research-gate-report.md`. Embed full prompts from respective agent definitions in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE analyst instances and MULTIPLE QA instances in parallel, each with an `assigned_files` subset. The threshold is >6 for research files because research files tend to be longer and more detailed than synthesis files. For example, with 10 research files: spawn 2 analyst instances (5 files each) + 2 QA instances (5 files each) = 4 parallel agents. Each partition instance writes to a numbered report (e.g., `${TASK_DIR}qa/analyst-completeness-report-1.md`, `${TASK_DIR}qa/analyst-completeness-report-2.md`). After all instances complete, merge their reports: union of all findings, take the more severe rating for any item flagged by multiple partitions, deduplicate gaps.
- Read ALL reports (or the merged report). Determine verdict from the QA report(s) (PASS / FAIL), cross-referenced with analyst findings.
- If PASS → proceed to Phase 4. If FAIL → fix ALL findings regardless of severity before proceeding. Reports list gaps with specific remediation actions.
- If verdict is FAIL: spawn additional targeted research agents (one item per gap-filling agent, from merged gap list). Each gap-filling agent follows the same incremental writing protocol. Wait for gap-filling agents to complete before proceeding.
- After gap-filling, spawn `rf-qa` with qa_phase: "fix-cycle" and the previous QA report path. The QA agent re-verifies only the previously-failed items. Maximum 3 fix cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance on how to proceed. Do NOT continue to Phase 4 without user approval.
- Compile final gaps into ${TASK_DIR}gaps-and-questions.md (merged from all reports)
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
- Each item specifies: topic, context from codebase findings, output file path
- Web research targets should include (as applicable): official framework/engine documentation, design patterns and best practices, third-party tools/libraries/APIs, community solutions to similar problems, GitHub issues and discussions, conference talks and technical blog posts from recognized experts

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One checklist item PER synthesis file (from research notes RECOMMENDED_OUTPUTS)
- Each item spawns an Agent subagent with the synthesis agent prompt from SKILL.md
- Each item specifies: research files to read, report sections to produce, output path
- After ALL synthesis agents complete, spawn `rf-analyst` (subagent_type: "rf-analyst", analysis_type: "synthesis-review") AND `rf-qa` (subagent_type: "rf-qa", qa_phase: "synthesis-gate", fix_authorization: true) IN PARALLEL. The analyst applies the 9-item Synthesis Quality Review Checklist. The QA agent applies its 12-item synthesis-gate checklist and can fix issues in-place. The analyst writes to `${TASK_DIR}qa/analyst-synthesis-review.md`. The QA agent writes to `${TASK_DIR}qa/qa-synthesis-gate-report.md`. Embed full prompts from respective agent definitions in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >4 synthesis files exist, spawn multiple analyst instances and multiple QA instances in parallel, each with an `assigned_files` subset of synthesis files. The threshold is lower than Phase 3 (>4 vs >6) because synthesis QA requires deeper per-file analysis (tracing claims back to research files, verifying cross-section consistency). Same partitioning pattern as Phase 3. Each partition instance writes to a numbered report. Orchestrator merges all partition reports after completion.
- Read ALL reports (or the merged report). The QA agent may have already fixed issues in-place on the synth files. Merge findings from all reports. Determine verdict from QA report(s), cross-referenced with analyst findings. If PASS → proceed to Phase 6. If FAIL → check which issues QA already fixed vs which remain. For remaining issues, re-run affected synthesis agents, then re-spawn `rf-qa` (fix-cycle). Maximum 3 fix cycles for synthesis — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance on how to proceed. Do NOT continue to Phase 6 without user approval.

Phase 6 — Assembly & Validation (RF-ASSEMBLER + Structural QA + Qualitative QA):
- Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") — NOT a general-purpose Agent — to assemble the final report. Hand it: the list of synth file paths in order (as component_files), the report output path `${TASK_DIR}RESEARCH-REPORT-[descriptor].md`, the Report Structure template from SKILL.md (as output_format), the Assembly Process steps from SKILL.md (as assembly_rules), and the Content Rules from SKILL.md (as content_rules). The assembler reads each synth file and writes the report incrementally section by section — header first, then sections in order, then Table of Contents, then cross-checks internal consistency (gaps in S4 addressed in S8, options in S6 reference S2, Open Questions in S9 not answered elsewhere, Evidence Trail in S10 lists all files). The assembler must be a single agent (NOT parallel) because cross-section consistency requires seeing the whole report. Embed the full assembler prompt (see Assembly Agent Prompt Template below and Assembly Process section in SKILL.md) in the checklist item per B2.
- After the assembler returns the report path, spawn `rf-qa` (subagent_type: "rf-qa", qa_phase: "report-validation", fix_authorization: true). The QA agent validates the assembled report against the 15-item Validation Checklist + 4 Content Quality Checks from SKILL.md. The QA agent is authorized to fix issues in-place and writes its report to `${TASK_DIR}qa/qa-report-validation.md`. Embed the full QA prompt from the rf-qa agent definition (QA Phase: Report Validation) in the checklist item per B2.
- Read the structural QA report. If issues remain unfixed, address them before proceeding to qualitative QA.
- After structural QA passes, spawn `rf-qa-qualitative` (subagent_type: "rf-qa-qualitative", qa_phase: "report-qualitative", fix_authorization: true). The qualitative QA agent reads the entire research report and verifies it makes sense as a technical investigation: problem statement matches findings, options are genuinely distinct, recommendation follows from analysis, implementation plan is actionable, gaps are honestly acknowledged, no circular reasoning, evidence trail is complete, conclusion is proportionate to evidence strength. The agent applies the 12-item Research Report Qualitative Review checklist from its agent definition. The agent writes to `${TASK_DIR}qa/qa-qualitative-review.md`. Embed the full qualitative QA prompt (including document_type: "Research Report", template path, and output path) in the checklist item per B2.
- Read the qualitative QA report. If any issues found (CRITICAL, IMPORTANT, or MINOR), verify fixes were applied correctly by re-reading the affected sections. If issues remain unfixed, address ALL of them before proceeding to Phase 7. Zero leniency — no severity level is exempt.

Phase 7 — Present to User & Complete Task:
- Present summary to user (report location, key findings, recommendation, research file count, open questions)
- Ask about tech reference skill: "This research can feed directly into a Technical Reference document. Would you like me to create a tech reference for the recommended solution using the `/tech-reference` skill? The research files are already in place and will accelerate the process." If yes, invoke the `tech-reference` skill with the research directory as input scope and the research report as context. The research files from `${TASK_DIR}research/` feed directly into tech-reference Phase 1 as pre-existing research.
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date

TASK FILE LOCATION: .dev/tasks/to-do/TASK-RESEARCH-YYYYMMDD-HHMMSS/TASK-RESEARCH-YYYYMMDD-HHMMSS.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, report structure, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .gfdoc/templates/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .gfdoc/templates/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-RESEARCH-YYYYMMDD-HHMMSS/TASK-RESEARCH-YYYYMMDD-HHMMSS.md using PART 2 structure
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
- Phase 6 uses `rf-assembler` (not a general-purpose Agent), `rf-qa` (report-validation), and `rf-qa-qualitative` (report-qualitative), and references the validation checklist from SKILL.md

If the task file is malformed or missing critical elements, re-run the builder with specific corrections. Otherwise, proceed to Stage B.

---

## Stage B: Task File Execution

### Execution Loop (F1)

Execute the task file using the five-step execution pattern from the MDTM template (Section F1):

```
READ → IDENTIFY → EXECUTE → UPDATE → REPEAT
```

1. **READ**: Read the task file from disk (always — never work from memory of previous state)
2. **IDENTIFY**: Find the FIRST unchecked `- [ ]` item
3. **EXECUTE**: Complete ONLY that single identified item:
   - If the item says to spawn a subagent → use the Agent tool with the prompt embedded in the item
   - If the item says to read files and produce output → do it directly
   - If the item says to present to the user → output the required information
   - If the item says to update frontmatter → edit the task file's frontmatter
4. **UPDATE**: Mark ONLY that item as `- [x]` in the task file on disk
5. **REPEAT**: Return to step 1

### Prohibited Actions (F2)

These actions are NEVER permitted during task file execution:

- **Working from memory** — You MUST re-read the task file before each action. Never assume you know the current state.
- **Executing multiple items simultaneously** — One item at a time, marked complete before moving to the next. Exception: parallel agent spawning (see below).
- **Skipping items** — Items MUST be completed in exact sequential order. No reordering, no "I'll come back to this."
- **Assuming completion** — An item is only complete when you have evidence of completion (file written, output produced, command succeeded) AND have marked it `- [x]` on disk.
- **Modifying source code** — Research agents READ code, they do not modify it. The skill produces reports, not code changes.
- **Inventing file paths** — Only reference files you have verified exist via Glob/Read.

### Parallel Agent Spawning (MANDATORY for Phases 2, 3, 4, 5)

When multiple consecutive items each spawn independent subagents, you MUST spawn them in parallel using multiple Agent tool calls in a single response. This applies to: Phase 2 investigation agents, Phase 3 analyst + QA agents, Phase 4 web research agents, Phase 5 synthesis agents AND the subsequent analyst + QA agents. This is not optional — it is how the skill achieves depth and minimizes wall-clock time.

Rules for parallel spawning:
1. Read the task file and find the first unchecked `- [ ]` item
2. Identify the **batch**: starting from that item, read forward through all consecutive unchecked items that are independent subagent spawns within the same phase. All of these form a single parallel batch.
3. Spawn ALL agents in the batch using parallel Agent tool calls in a single message
4. As each agent returns, mark its corresponding item `- [x]` immediately — do not wait for all to finish before checking any off. This ensures progress is captured even if the session ends mid-batch.
5. After ALL agents in the batch return, read the task file again before proceeding to the next phase

**On resumption after a mid-batch failure:** If some items in a batch are `- [x]` and others are `- [ ]`, spawn only the unchecked ones. The checked agents' output files already exist on disk — do not re-run them.

### Task File Modification Restrictions (F4)

During execution, you MAY ONLY modify the task file to:
- Check off completed items (`- [ ]` → `- [x]`)
- Update frontmatter fields (status, updated_date, start_date, completion_date)
- Add entries to the Task Log / Notes section
- Add items within DYNAMIC CONTENT MARKER sections (if the template includes them)

You MUST NOT:
- Rewrite or rephrase existing checklist items
- Add new checklist items outside of DYNAMIC CONTENT MARKER sections
- Delete or reorder existing items
- Modify the Task Overview or Key Objectives sections

### Frontmatter Update Protocol (F5)

Update frontmatter at these specific points:

| Event | Fields to Update |
|-------|-----------------|
| **Task start** | `status: "🟠 Doing"`, `start_date: [today]`, `updated_date: [today]` |
| **After each work session** | `updated_date: [today]` |
| **Task blocked** | `status: "⚪ Blocked"`, `blocker_reason: [description]`, `updated_date: [today]` |
| **Task completion** | `status: "🟢 Done"`, `completion_date: [today]`, `updated_date: [today]` |

### Error Handling

If an item cannot be completed:
1. Log the blocker in the Task Log / Notes section with: timestamp, item reference, error description, attempted resolution
2. If the error is recoverable (e.g., agent returned partial results), complete what you can and note the gap
3. If the error is unrecoverable, mark the item `- [x]` with a note in Task Log, continue to next item
4. If ALL remaining items are blocked by the same issue, update frontmatter to "⚪ Blocked" with reason

### Session Resumption

If the session restarts or context compresses mid-execution:

1. Check `.dev/tasks/to-do/` for `TASK-RESEARCH-*/` folders related to the current topic
2. Read the task file inside the folder (`${TASK_DIR}TASK-RESEARCH-*.md`)
3. Find the first unchecked `- [ ]` item
4. Resume the execution loop from that item
5. Do NOT re-execute any `- [x]` items — they are complete

The task folder `${TASK_DIR}` contains all intermediate artifacts in typed subfolders (`research/`, `synthesis/`, `qa/`, `reviews/`). Read existing research files to understand what has been completed before resuming.

---

## Agent Prompt Templates

These templates are provided to the task builder (in the BUILD_REQUEST) so it can embed them in the task file's self-contained checklist items. The builder should customize each instance with the specific investigation topic, files, and output path.

### Codebase Research Agent Prompt

```
Investigate this aspect of [topic] and write your findings to [output-path].

Topic: [specific investigation topic]
Investigation type: [Code Tracer / Doc Analyst / Integration Mapper / Pattern Investigator / Architecture Analyst]
Files to investigate: [list of files/directories]
Research question context: [the overall research question for context]

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
1. Read actual source files — understand what each file does, what it exports, what it imports
2. Trace data flow — how does data enter, transform, and exit this part of the system?
3. Document the implementation — key classes, functions, methods with file paths and line numbers
4. Identify patterns — what conventions, architectural decisions, or design patterns are used?
5. Check for edge cases — error handling, fallbacks, configuration-driven behavior
6. Note dependencies — what does this subsystem depend on? What depends on it?
7. Flag gaps — what is missing, broken, undocumented, or unclear? What needs further investigation?
8. Note integration opportunities — where could new functionality hook in?

CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Code describes CURRENT state. These frequently diverge.
When you encounter documentation that describes an architecture, pipeline, service, component, endpoint,
or workflow, you MUST cross-validate EVERY structural claim against actual code before reporting it as current:

1. Services/components described in docs: Verify the service directory, entry point file, and key classes
   actually exist in the repo. Use Glob to check. If a doc says "Go Worker Service at apps/workerv2/",
   verify `apps/workerv2/` exists. If it doesn't, the doc is STALE — report it as historical, not current.

2. Pipelines/call chains described in docs: Trace at least the first and last hop in actual source code.
   If a doc says "Agent → WorkerClient → Go Worker → RCAPI", verify WorkerClient exists as an import/class
   in the agent code, AND verify the Go Worker service exists. If any hop is missing, the pipeline is STALE.

3. File paths mentioned in docs: Spot-check that referenced files exist. If a doc references
   `adjust_data_table.py` but the actual file is `adjust_data_table_enhanced.py`, note the discrepancy.

4. API endpoints described in docs: Verify the endpoint exists in the actual router/app code.
   If a doc describes `PUT /api/datatable` proxied through a Go worker, check whether the Go worker exists
   and whether the endpoint is actually served by a different service.

For EVERY doc-sourced architectural claim, mark it with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** — code shows different implementation (describe what code actually shows)
- **[UNVERIFIED]** — could not find corresponding code; may be stale, planned, or in a different repo

Claims marked [UNVERIFIED] or [CODE-CONTRADICTED] MUST appear in the Gaps and Questions section.
Do NOT present doc-sourced claims as verified facts without the code verification tag.

Output Format:
- Use descriptive headers for each file or logical group investigated
- Include actual file paths, class names, function names, line numbers
- Note anomalies, tech debt, or surprising behavior
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
Research question context: [the overall research question]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for official documentation, guides, and API references
2. Search for community patterns, solutions, and best practices
3. Search for tutorials and implementation examples
4. For each finding, document:
   - Source URL
   - Key information extracted
   - How it relates to our codebase findings
   - Whether it supports, extends, or contradicts what we found in code
5. Rate source reliability (official docs > well-maintained repos > blog posts > forum answers)

Output Format:
- Use descriptive headers for each research area
- Always include source URLs
- Mark relevance: HIGH / MEDIUM / LOW for each finding
- End with:
  ## Key External Findings
  [Bullet list of the most important discoveries]

  ## Recommendations from External Research
  [How external findings should influence our approach]

IMPORTANT: Our codebase is the source of truth. External research adds context and options but does not override verified code behavior. If you find a discrepancy, note it explicitly.
```

### Synthesis Agent Prompt

```
Read the research files listed below and synthesize them into report sections for a Technical Research Report.

Research files to read: [list of specific file paths]
Report sections to produce: [section numbers and names]
Output path: [synth file path]
Research question context: [the overall research question]

Rules:
1. Every fact must come from the research files — do not invent, assume, or infer
2. Use tables over prose for multi-item data (file lists, comparisons, gap inventories, step lists)
3. Do not reproduce full source code — summarize with key class names, function signatures, and file paths
4. Use ASCII diagrams for architecture and data flow where the research supports them
5. Reference actual file paths from the research — not hypothetical ones
6. When research files contradict each other, note the contradiction and which finding has stronger evidence
7. Web research findings must be explicitly marked as external context, with source URLs
8. Implementation plan steps must be specific and actionable — include file paths, function names, integration points
9. **Documentation-sourced claims require verification status.** If a research file reports a finding from documentation, check whether it carries a [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED] tag. Only [CODE-VERIFIED] claims may be presented as current architecture. [CODE-CONTRADICTED] claims must be corrected to match what the code actually shows. [UNVERIFIED] claims must be flagged as uncertain and placed in Open Questions — never in Current State Analysis or Implementation Plan as if they are fact.
10. **Never describe architecture from docs alone.** When writing Current State Analysis (Section 2) or Implementation Plan (Section 8), ONLY use findings that trace back to actual source code reads. If the only evidence for a pipeline, service, or component is a documentation file, it MUST be flagged as [UNVERIFIED — doc-only, no code confirmation] and excluded from architecture diagrams and implementation steps.

CRITICAL — Incremental File Writing:
You MUST write to your output file incrementally as you synthesize each section. Do NOT read all research files into context and attempt a single large write. The process is:
1. Create the output file with a header and your first synthesized section
2. After completing each subsequent section, append it to the output file immediately using Edit
3. Never rewrite the entire file from memory — always append or do targeted edits

This prevents data loss from context limits and ensures partial results survive if the agent is interrupted.

Write the sections in the exact format they should appear in the final report, using the section structure and table formats from the report template.
```

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

IF ANALYST REPORT EXISTS:
1. Read the analyst's completeness report
2. Spot-check 3-5 of their coverage audit claims (verify the scope items are actually covered)
3. Validate gap severity classifications (are "Critical" really critical? Are "Minor" really minor?)
4. Check their verdict against your own independent assessment
5. Apply the 10-item Research Gate checklist from your agent definition

IF NO ANALYST REPORT:
Apply the full 10-item Research Gate checklist from your agent definition independently.

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
Perform QA verification of synthesis files for [topic].

QA phase: synthesis-gate
Task directory: [task-dir-path]
Synthesis directory: [task-dir-path]synthesis/
Research directory: [task-dir-path]research/
Fix authorization: [true/false]
Output path: [output-path]

You are verifying that synthesis files are ready for assembly into the final report.
If fix_authorization is true, you can fix issues in-place using Edit.

PROCESS:
1. Use Glob to find ALL synth files (synth-*.md) in the synthesis directory (`${TASK_DIR}synthesis/`)
2. Read EVERY synth file completely
3. Apply the 12-item Synthesis Gate checklist from your agent definition
4. For each issue found:
   a. Document the issue (what, where, severity)
   b. If fix_authorization is true: fix in-place with Edit, verify the fix
   c. If fix_authorization is false: document the required fix
5. Write your QA report to [output-path]

12-ITEM CHECKLIST:
1. Section headers match Report Structure template
2. Table column structures correct
3. No fabrication (sample 5 claims per file, trace to research files)
4. Evidence citations use actual file paths
5. Options analysis: 2+ options with pros/cons
6. Implementation plan: specific file paths, not generic steps
7. Cross-section consistency (gaps in S4 addressed in S8, etc.)
8. No doc-only claims in Sections 2 or 8
9. Stale docs surfaced in Sections 4 or 9
10. Content rules compliance (tables over prose, no code reproductions)
11. All expected sections have content (no placeholders)
12. No hallucinated file paths (verify parent directories exist)

VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found (list with specific fixes, note which were fixed in-place)
```

### Report Validation QA Agent Prompt (rf-qa — Report Validation)

```
Perform final QA validation of the assembled research report for [topic].

QA phase: report-validation
Report path: [report-path]
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Synthesis directory: [task-dir-path]synthesis/
Output path: [output-path]
Fix authorization: true (always authorized for report validation)

This is the final quality check before presenting to the user. You can and should fix issues in-place.

PROCESS:
1. Read the ENTIRE research report
2. Apply the 15-item Validation Checklist + 4 Content Quality Checks
3. For each issue: document it, fix it in-place with Edit, verify the fix
4. Write your QA report to [output-path]

15-ITEM VALIDATION CHECKLIST:
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

Fix every issue you find. Report honestly.
```

### Assembly Agent Prompt (rf-assembler — Report Assembly)

```
Assemble the final research report for [topic] from synthesis files.

Component files (in order):
[ordered list of synth file paths]

Output path: [report-output-path]
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Synthesis directory: [task-dir-path]synthesis/

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create the output file immediately with the report header:
   # Technical Research Report: [Topic]
   **Date:** [today]
   **Depth:** [Quick / Standard / Deep]
   **Research files:** [count] codebase + [count] web research
   **Scope:** [directories/subsystems investigated]

2. As you assemble each section, IMMEDIATELY write it to the output file using Edit.
   Do NOT accumulate the entire report in context and attempt a single write.

3. After each Edit, the file grows. This is correct behavior. Never rewrite from scratch.

Output format — the final report MUST contain these 10 sections in this order:
1. Problem Statement (what we are solving, why, what prompted this)
2. Current State Analysis (how things work now — every claim cites file paths and line numbers)
3. Target State (what we want to achieve, success criteria, constraints)
4. Gap Analysis (table: Gap / Current State / Target State / Severity / Notes)
5. External Research Findings (findings with source URLs, relevance ratings)
6. Options Analysis (2+ options, each with assessment table: Effort/Risk/Reuse/Files/Pros/Cons, plus comparison table)
7. Recommendation (recommended option with rationale referencing comparison)
8. Implementation Plan (specific steps with file paths, function names, integration points — table: Step / Action / Files / Details)
9. Open Questions (table: # / Question / Impact / Suggested Resolution)
10. Evidence Trail (tables listing all research, web research, and synthesis files)

Assembly rules:
1. Write the report header first (title, date, depth tier, research file count, scope summary)
2. Assemble sections in order — read each synth file and write its content into the correct position
3. Write each section to disk immediately after composing it — do NOT one-shot
4. Generate the Table of Contents from actual section headers after all sections are placed
5. Cross-check internal consistency:
   - Gaps in Section 4 have corresponding implementation steps in Section 8
   - Options in Section 6 reference evidence from Section 2
   - Open Questions in Section 9 aren't answered elsewhere in the report
   - Evidence Trail in Section 10 lists every research and synthesis file produced
6. Flag any contradictions between sections using: [CONTRADICTION: Component A claims X, Component B claims Y]
7. Ensure no placeholder text remains (search for [, TODO, TBD, PLACEHOLDER)

Content rules (non-negotiable):
- Tables over prose whenever presenting multi-item data
- No full source code reproductions — summarize with key signatures and file paths
- Use ASCII diagrams for architecture and data flow, not prose descriptions
- Evidence cited inline: file.cpp:123, ClassName::method()
- Conciseness over comprehensiveness — scannable, not exhaustive prose
- Every claim needs evidence — no file path or URL = belongs in Open Questions
- Uncertainty marked explicitly with "Unverified" or "Open Question" markers

CRITICAL: You are assembling existing content, not creating new findings. Preserve fidelity
to the synthesis files. Add only minimal transitional text where needed for coherence.
Do NOT attempt full content validation — that is the QA agent's job. Focus on assembly
integrity: correct ordering, internal consistency, no placeholders, all components included.
```

---

## Report Structure

The final research report follows this structure. The synthesis agents produce sections that are assembled into this format.

```markdown
# Technical Research Report: [Topic]

**Date:** [today]
**Depth:** [Quick / Standard / Deep]
**Research files:** [count] codebase + [count] web research
**Scope:** [directories/subsystems investigated]

---

## Table of Contents
[Generated from section headers]

---

## 1. Problem Statement

What we are solving, why it matters, and what prompted this investigation.

- **The question:** [original research question]
- **Why it matters:** [business/technical impact]
- **Trigger:** [what prompted this research]

---

## 2. Current State Analysis

How things work right now — every claim verified against actual code.

### 2.1 [Subsystem/Component A]
[How it works, key files, key functions, data flow]
**Evidence:** [file paths, line numbers]

### 2.2 [Subsystem/Component B]
[...]

### 2.N Current State Summary
[Concise summary table or diagram of the current state]

---

## 3. Target State

What we want to achieve — the goal described concretely.

- **Desired behavior:** [what should happen]
- **Success criteria:** [how we know it works]
- **Constraints:** [what we cannot change, must preserve, or must comply with]

---

## 4. Gap Analysis

What is missing between current state and target state.

| Gap | Current State | Target State | Severity | Notes |
|-----|--------------|-------------|----------|-------|
| [gap] | [what exists] | [what's needed] | Critical/High/Medium/Low | [context] |

---

## 5. External Research Findings

Supplementary context from web research. Codebase findings take precedence.

### 5.1 [Topic Area]
- **Finding:** [what was found]
- **Source:** [URL]
- **Relevance:** HIGH / MEDIUM / LOW
- **Relationship to codebase:** [supports / extends / contradicts]

### 5.N External Research Summary
[Key takeaways from external research]

---

## 6. Options Analysis

### Option A: [Name]
**Description:** [what this approach entails]
**How it works:** [technical description]

| Aspect | Assessment |
|--------|-----------|
| Effort | [XS / S / M / L / XL] |
| Risk | [Low / Medium / High] |
| Reuse of existing code | [what can be reused] |
| Files/systems affected | [list] |
| Pros | [bullet list] |
| Cons | [bullet list] |

### Option B: [Name]
[same structure]

### Option C: [Name] (if applicable)
[same structure]

### Options Comparison

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Effort | | | |
| Risk | | | |
| Maintainability | | | |
| Integration complexity | | | |
| Reuse potential | | | |

---

## 7. Recommendation

**Recommended approach:** [Option X]

**Rationale:**
[Why this option is recommended, referencing the comparison analysis. Address the key trade-offs and why they are acceptable.]

---

## 8. Implementation Plan

Detailed steps to implement the recommended approach. As specific as possible — file paths, function signatures, integration points, code patterns to follow.

### Phase 1: [Name]
**Goal:** [what this phase achieves]
**Dependencies:** [what must exist first]

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 1.1 | [action] | [file paths] | [specifics] |
| 1.2 | [action] | [file paths] | [specifics] |

### Phase 2: [Name]
[same structure]

### Phase N: [Name]
[same structure]

### Integration Checklist
- [ ] [integration step]
- [ ] [integration step]
- [ ] [verification step]

---

## 9. Open Questions

Issues that need resolving before or during implementation.

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|---------------------|
| 1 | [question] | [what it blocks] | [how to resolve] |

---

## 10. Evidence Trail

All research files produced during this investigation.

### Codebase Research
| File | Topic | Agent Type |
|------|-------|-----------|
| `[path]` | [topic] | [type] |

### Web Research
| File | Topic |
|------|-------|
| `[path]` | [topic] |

### Gaps Log
- `[path to gaps file]`
```

---

## Synthesis Mapping Table (Reference)

This is the standard mapping of synthesis files to report sections. Adjust based on investigation complexity — for Quick tier, combine more sections per synth file. For Deep tier, split further if needed (e.g., separate synth files per option in Section 6).

| Synth File | Report Sections | Source Research Files |
|------------|----------------|----------------------|
| `synth-01-problem-current-state.md` | 1. Problem Statement, 2. Current State Analysis | All codebase research files, gaps log |
| `synth-02-target-gaps.md` | 3. Target State, 4. Gap Analysis | Codebase research files, gaps log, web research files |
| `synth-03-external-findings.md` | 5. External Research Findings | All web research files |
| `synth-04-options-recommendation.md` | 6. Options Analysis, 7. Recommendation | All codebase + web research files, gaps log |
| `synth-05-implementation-plan.md` | 8. Implementation Plan | All codebase research files (for integration points), web research files (for patterns) |
| `synth-06-questions-evidence.md` | 9. Open Questions, 10. Evidence Trail | All gaps, all research file paths |

---

## Synthesis Quality Review Checklist

**This checklist is now enforced by the rf-analyst and rf-qa agents** (see Phase 5 in the task phases above). The rf-analyst applies these 9 criteria as its Synthesis Quality Review analysis type, and the rf-qa agent independently verifies the analyst's findings with its expanded 12-item Synthesis Gate checklist. The QA agent can fix issues in-place when authorized.

The 9 criteria (used by rf-analyst):

1. Report section headers match the expected format from the Report Structure template
2. Tables use the correct column structure (Gap/Current/Target/Severity, Criterion/OptionA/OptionB, Step/Action/Files/Details)
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and evidence (not vague descriptions)
5. Options analysis includes at least 2 options with pros/cons assessment tables
6. Implementation plan has specific steps with file paths (not generic actions like "create a service")
7. All cross-references between sections are consistent (e.g., gaps in Section 4 are addressed in Section 8)
8. **No doc-only claims in Current State or Implementation Plan.** Verify that Sections 2 and 8 only contain architecture descriptions backed by code-traced evidence. If a synth file describes a pipeline, service, or component and the only evidence is a documentation file (no source code path), reject that claim and either remove it or flag it as `[UNVERIFIED — doc-only]`
9. **Stale documentation discrepancies are surfaced.** Any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings from research files should appear in the Gap Analysis (Section 4) or Open Questions (Section 9), not silently omitted

The rf-qa agent's Synthesis Gate adds 3 additional checks (10-12): content rules compliance, section completeness, and hallucinated file path detection. If synthesis QA fails, the QA agent fixes issues in-place (when authorized) and issues remaining unfixed trigger re-synthesis of the affected files.

---

## Assembly Process

The assembly step reads all synth files in order and produces the final report. Follow these 4 steps:

1. **Write the report header** — title, date, depth tier, research file count, scope summary
2. **Assemble sections in order** — paste each synth file's content into the correct position, writing incrementally section by section (do NOT one-shot the entire report)
3. **Write the Table of Contents** — generate from actual section headers after all sections are placed
4. **Cross-check internal consistency** — verify that:
   - Gaps in Section 4 have corresponding implementation steps in Section 8
   - Options in Section 6 reference evidence from Section 2
   - Open Questions in Section 9 aren't answered elsewhere in the report
   - Evidence Trail in Section 10 lists every research file produced

---

## Validation Checklist

Before presenting the report to the user, validate against this checklist (this is encoded in the task file's Assembly phase):

- [ ] All 10 report sections present (or explicitly marked as N/A for Quick tier)
- [ ] Problem Statement references the original research question
- [ ] Current State Analysis cites actual file paths and line numbers for every claim
- [ ] Gap Analysis table has severity ratings for every gap
- [ ] External Research Findings include source URLs for every finding
- [ ] Options Analysis has at least 2 options with comparison table
- [ ] Recommendation explicitly references the comparison analysis
- [ ] Implementation Plan has specific file paths and actions (not generic steps)
- [ ] Open Questions table includes impact and suggested resolution for each
- [ ] Evidence Trail lists every research and synthesis file produced
- [ ] No full source code reproductions
- [ ] Tables used over prose for multi-item data throughout
- [ ] No assumptions presented as verified facts
- [ ] No doc-only architectural claims in Sections 2, 6, 7, or 8
- [ ] All [CODE-CONTRADICTED] and [STALE DOC] findings surfaced in Sections 4 or 9

---

## Content Rules (Non-Negotiable)

These rules govern how content is written within research files, synthesis files, and the final report. They prevent bloat, ensure consistency, and keep the output actionable.

| Rule | Do | Don't |
|------|-----|-------|
| **Source code** | Summarize behavior in tables and prose with key signatures | Reproduce full function bodies, interfaces, config files, or CSS values |
| **Architecture** | Use tables and ASCII diagrams | Multi-paragraph prose for what could be a table row |
| **Comparisons** | Use comparison tables with clear criteria | Prose-based side-by-side descriptions |
| **File inventories** | Table: Path / Purpose / Key Exports | List files in paragraph form |
| **Data flow** | ASCII diagram or numbered step list | Multi-paragraph narrative |
| **Implementation steps** | Table: Step / Action / Files / Details | Prose paragraphs describing what to do |
| **Gap analysis** | Table: Gap / Current / Target / Severity | Narrative description of each gap |
| **Options analysis** | Structured per-option blocks with assessment table | Running prose comparing options |
| **Evidence** | Inline citations: `file.cpp:123`, `ClassName::method()` | "The code does X" without pointing to where |
| **Statistics** | State key numbers once in the relevant section | Scatter file counts, line counts throughout |
| **Uncertainty** | Explicit "Unverified" or "Open Question" markers | Present uncertain findings as verified facts |

**General content principles:**
- Tables over prose whenever presenting multi-item data
- Conciseness over comprehensiveness — the report should be scannable, not exhaustive prose
- Every claim needs evidence — if you can't cite a file path or URL, it belongs in Open Questions
- Prefer ASCII diagrams for visual relationships over paragraph descriptions

---

## Critical Rules

These rules apply across ALL phases. Violations compromise research quality.

1. **Task file is the source of truth.** Never work from memory of prior state. Always read the task file before acting. Progress is tracked by checked/unchecked items on disk.

2. **Incremental writing is mandatory — ZERO TOLERANCE.** Every agent's FIRST ACTION must be creating its output file on disk using Write (frontmatter/header only). All subsequent content is appended using Edit, one section at a time. NEVER accumulate content in context and attempt a single large Write — this is the #1 failure mode across all agents. It hits max token output limits and freezes the process, losing all work. The procedure is: Write (create file with header) → Edit (append section 1) → Edit (append section 2) → ... → Edit (update Status to Complete). This applies to: research agents, synthesis agents, analyst reports, QA reports, task file builder, and assembler.

3. **Maximize parallelism (MANDATORY).** For Phases 2, 3, 4, and 5, you MUST spawn all independent agents in each batch in parallel using multiple Agent tool calls in a single message. This includes: Phase 2 investigation agents, Phase 3 analyst + QA (both read research files independently), Phase 4 web research agents, Phase 5 synthesis agents AND the subsequent analyst + QA pair. Each agent operates in isolated context and writes to its own file. The only sequential requirement is: the QA fix-cycle must wait for its predecessor's report. **Additionally, for Phases 3 and 5, when file counts exceed the partitioning threshold (>6 research files for Phase 3, >4 synth files for Phase 5), you MUST spawn multiple analyst instances AND multiple QA instances in parallel, each with an `assigned_files` subset.** This prevents context rot when any single agent would need to hold too many files in context. This is not optional — it is how the skill achieves depth, breadth, and speed simultaneously.

4. **Codebase is source of truth.** Web research supplements but never overrides verified code findings. Internal documentation is treated with the same skepticism as external sources unless code-verified.

5. **Evidence-based claims only.** Every finding must cite actual file paths, line numbers, function names, class names. No assumptions, no inferences, no guessing. If you can't verify it, mark it as "Unverified — needs confirmation."

6. **Default to Deep.** Unless the question is clearly answerable with a quick scan of <5 files, use the Deep tier. When in doubt, go deeper.

7. **No one-shotting reports.** Agents must write incrementally as they discover information. The orchestrator must write the final report section by section. This is non-negotiable.

8. **Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, codebase-retrieval for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations.

9. **Gap-driven web research.** Do not web search everything up front. First investigate the codebase thoroughly (Phase 2), identify specific gaps, then target web research (Phase 3) at those gaps. This keeps web research focused and efficient.

10. **Preserve research artifacts.** Research and web research files persist after the report is written. They serve as the evidence trail for all claims and enable future re-investigation without starting from scratch. Do NOT delete research files, synthesis files, or the gaps log after assembly.

11. **Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. The synthesis phase relies on these connections to build a coherent picture across investigation slices.

12. **Implementation plans must be actionable.** The implementation plan section should contain enough detail that a developer (or another AI agent) could begin work from it. Include specific files to create/modify, code patterns to follow, and integration points.

13. **Report all uncertainty.** If something is unclear, ambiguous, or requires a judgment call, document it in Open Questions. Do not silently pick one interpretation and present it as fact.

14. **Documentation is not verification.** Internal documentation (design docs, architecture docs, integration guides, READMEs in `docs/`) describes intent, history, or planned state — NOT necessarily current state. A doc saying "Service X exists at path Y" does not prove Service X exists. Only reading actual source code at path Y proves it exists. Doc Analyst agents MUST cross-validate every architectural claim against actual code using the Documentation Staleness Protocol. Any doc-sourced claim without a `[CODE-VERIFIED]` tag is treated as unverified.

15. **Docs-vs-code has the same trust hierarchy as web-vs-code.** Critical Rule 4 establishes that web research never overrides code. The same applies to internal documentation: if a doc describes an architecture that contradicts what the code shows, **the code is correct and the doc is stale**. This is especially dangerous because internal docs feel authoritative — but a doc written 6 months ago about a planned architecture may describe services, pipelines, and components that were never built, were refactored, or were removed. Treat internal docs with the same skepticism as external blog posts unless code-verified.

---

## Session Management

This work may span multiple sessions. The task file and research directory serve as the persistent record.

**At session start:**
1. Check for existing task folder in `.dev/tasks/to-do/TASK-RESEARCH-*/`
2. If found, read the task file inside it and resume from the first unchecked `- [ ]` item
3. Read existing research files in `${TASK_DIR}research/` for context
4. Read the gaps-and-questions file if it exists
5. Read any partial research report
6. Do not re-research completed topics

**At session end:**
- All research files should have Status: Complete
- The task file should reflect exactly which items are checked and unchecked
- If synthesis is in progress, note which synth files are complete and which report sections are assembled
- The user should know the current state (which phase, which step)

---

## Research Quality Signals

### Strong Investigation Signals
- Findings cite specific file paths and line numbers
- Data flow is traced end-to-end, not just entry points
- Integration points are mapped with actual function signatures
- Existing patterns identified that can be reused
- Gaps are specific and actionable ("function X doesn't handle case Y")

### Weak Investigation Signals (Redo)
- Vague descriptions without file paths ("the system uses a plugin architecture")
- Assumptions stated as facts ("this probably works by...")
- Missing gap analysis (everything seems fine — unlikely for non-trivial systems)
- No cross-references between research files
- Implementation plan uses generic steps ("create a service that handles X")
- Doc-sourced architecture reported without code verification tags — if a research file describes pipelines, services, or components and the evidence trail only points to documentation files (no source code paths), the investigation is incomplete and must be redone with code cross-validation

### When to Spawn Additional Agents
- A research agent flags a gap that's critical to the analysis
- Two agents' findings contradict each other — need a tie-breaker investigation
- The scope turns out larger than initially estimated
- A new subsystem is discovered during investigation that wasn't in the original plan
