---
name: tech-research
description: "Deep technical investigation and feasibility research across the codebase. Produces structured research reports with findings, gap analysis, options, and detailed implementation recommendations. Use this skill when the user wants to research how something works, investigate a technical problem, figure out what needs to be built or changed, do a feasibility study, or deep dive into a system or integration. Trigger on phrases like 'research how X works', 'investigate this', 'figure out what we need for X', 'feasibility study', 'deep dive into X', 'how does X work and what do we need to change', 'tech research on X', 'what would it take to build X', 'analyze this system', or 'research this problem'. Also trigger when the user says 'research' in the context of understanding a technical problem or planning an implementation."
---

# Technical Research & Investigation

A skill for deep technical investigation across the codebase. This skill uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts.

**How it works:** The skill performs initial scope discovery, then invokes the `/task-builder` skill to create an MDTM task file encoding all investigation phases. The skill then delegates execution to the `/task` skill, which processes the task file — marking items complete as it progresses. If context compresses or the session restarts, the skill re-reads the task file and resumes from the first unchecked item.

This skill fills the gap between `repo-cleanup` (audits what exists) and `tech-reference` (documents what's built). `tech-research` **investigates a problem and recommends what to build or change**.

## Why This Process Works

Technical investigations fail when they rely on assumptions, memory, or surface-level reading. This skill forces every claim through codebase verification — parallel agents read actual source files, trace actual data flows, and document actual behavior with file paths and line numbers.

The MDTM task file provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off.

The multi-phase structure (scope discovery → deep investigation → **analyst + QA + qualitative verification** → web research → synthesis → **synthesis QA** → assembly → **lens-based multi-agent QA** → **source-document fidelity gate** → **anti-omission gate**) prevents six common failure modes:
- **Context rot** — By isolating each investigation topic in its own subagent with its own output file, no single agent needs to hold the entire investigation in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning many parallel agents (each focused on one slice), the investigation goes deep on every aspect simultaneously rather than skimming across everything sequentially.
- **Hallucinated recommendations** — By separating research (what exists) from synthesis (what it means) from assembly (the final report), each phase can be verified independently. Synthesis agents only work from verified research files, not from memory or inference.
- **Uncaught quality drift** — Lens-based multi-agent QA at the final gate assigns each agent a focused quality dimension ("lens") — structural lenses (template conformance, internal consistency, evidence quality, completeness) and content lenses (actionability, numbers/metrics, cross-reference chains, domain accuracy) plus tech-research domain lenses (recommendation feasibility, finding reproducibility, implementation plan concreteness). Each lens agent reads the full report but evaluates ONLY its assigned dimension. This prevents the rubber-stamping that occurs when 1-2 agents try to check everything on a large document. Minimum 11 agents at the final gate (4 structural + 4 content + 3 domain), with serialized fix authorization (all agents report findings first, then a single fix agent applies all corrections, then a verification round confirms). Intermediate gates (research, synthesis) use 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents minimum.
- **Source-document semantic drift** — A dedicated fidelity gate spawns agents that read BOTH the original codebase source files AND the assembled report, verifying that findings faithfully represent the actual code. This catches cases where research findings are structurally present but semantically distorted during synthesis and assembly.
- **Compression omission**: Synthesis and assembly compress many research findings into fewer report items; without an explicit check, distinct findings are silently dropped during that compression. A dedicated anti-omission gate enumerates EVERY distinct finding in the research and synthesis inputs and verifies each is represented in the output. This is a source→output completeness check, the exact INVERSE of the fidelity gate's output→source no-fabrication check, and the two are not interchangeable: a report can fabricate nothing yet still drop half its inputs. Every omission is recovered or explicitly justified as intentional dedup, never silently lost. Coverage is judged by meaning, never by ID/reference-citation (the synthesis absorbs findings without citing their source IDs, so an ID-membership test both over- and under-reports).

The research artifacts persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and feed directly into downstream skills like `tech-reference`.

### Variable Reference

Every invocation creates a self-contained folder. All paths below are relative to this folder:

```
TASK_ID:     TASK-RESEARCH-<subject>-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/
SYNTHESIS:   ${TASK_DIR}synthesis/
QA:          ${TASK_DIR}qa/
REVIEWS:     ${TASK_DIR}reviews/
```

**Subject derivation:** `<subject>` is derived at task-folder-creation time from the research topic (already available as `TOPIC_SLUG`) and normalized to kebab-case (lowercase, hyphen-separated, 1-3 words, ~30 char soft cap). If no clean subject can be derived, fall back to the literal word `general`. Example TASK_ID: `TASK-RESEARCH-locomotion-params-20260408-140000`.

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

**QA Intensity Mapping (per Template 02 I22):**

| Tier | Default qa_intensity | Override allowed? |
|------|---------------------|-------------------|
| Quick | lite | Yes |
| Standard | standard | Yes |
| Deep | full | Yes |

If the user says "quick", "fast", "light QA", or "basic" → lite.
If the user says "thorough QA", "full QA", "careful" → full.
Otherwise → default per tier.

---

## Output Locations

All persistent artifacts go to the task folder `${TASK_DIR}` (see Variable Reference above). The topic slug is derived from the research question (e.g., `locomotion-params`, `ade-hot-reload`, `agent-memory-system`) and used in the TASK_ID.

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}TASK-RESEARCH-<subject>-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research/research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[aspect-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[section-name].md` |
| Final research report | `${TASK_DIR}RESEARCH-REPORT-[descriptor].md` |
| Gap/question log (interim) | `${TASK_DIR}gaps-and-questions.md` |
| Analyst completeness report(s) | `${TASK_DIR}qa/analyst-completeness-report[-N].md` |
| QA research gate report(s) | `${TASK_DIR}qa/qa-research-gate-report[-N].md` |
| QA research qualitative report | `${TASK_DIR}qa/qa-research-qualitative-report.md` |
| Analyst synthesis review(s) | `${TASK_DIR}qa/analyst-synthesis-review[-N].md` |
| QA synthesis gate report(s) | `${TASK_DIR}qa/qa-synthesis-gate-report[-N].md` |
| QA synthesis qualitative report | `${TASK_DIR}qa/qa-synthesis-qualitative-report.md` |
| Lens QA reports (structural) | `${TASK_DIR}qa/qa-lens-[lens-name].md` |
| Lens QA reports (content) | `${TASK_DIR}qa/qa-lens-[lens-name].md` |
| Consolidated QA findings | `${TASK_DIR}qa/qa-consolidated-findings-phase{3,5,6}.md` |
| QA fix verification report | `${TASK_DIR}qa/qa-fix-verification.md` |
| Source fidelity report(s) | `${TASK_DIR}qa/qa-source-fidelity-report[-N].md` |

**File numbering convention:** All research, web, and synthesis files use zero-padded sequential numbers: `01-`, `02-`, `03-`, etc. This ensures correct ordering when listing files.

Check for existing task folders in `.dev/tasks/to-do/` before creating new ones — if prior research exists on the same topic (matching `TASK-RESEARCH-*/`), read it first and build on it.

---

## Execution Overview

The skill operates in two stages:

**Stage A — Scope Discovery & Task File Creation (before the task file exists):**
1. Check for existing task file (resume if found) (A.1)
2. Parse the user's research question and triage (Scenario A vs B) (A.2)
3. Perform scope discovery (depth adjusted by scenario) (A.3)
4. Write scope discovery results to a structured research notes file (A.4)
5. Review research sufficiency (mandatory gate) (A.5)
6. Triage template selection (A.6)
7. Write BUILD-REQUEST.md and invoke /task-builder skill to create the MDTM task file (A.7) -- task-builder handles structural and qualitative validation internally

**Stage B — Task File Execution (after the task file exists):**
7. Delegate to the `/task` skill, which executes from the task file using the F1 loop
8. Each checklist item is a self-contained prompt — no prior context needed

If a task file already exists for this research topic (from a previous session), skip Stage A and invoke `/task` with the existing task file path — it resumes from the first unchecked item.

---

## Stage A: Scope Discovery & Task File Creation

### A.1: Check for Existing Task File

Before creating a new task file, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `TASK-RESEARCH-*/` folder related to this topic
2. If found, read the task file inside it (`${TASK_DIR}TASK-RESEARCH-*.md`) and check for unchecked `- [ ]` items
3. If unchecked items exist → invoke the /task skill with the task file path (Stage B)
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

Compute `<subject>` from the research topic (already available as `TOPIC_SLUG`) using the rules in the Subject Derivation section. If no clean subject is derivable, use `general`. Create the task folder: `.dev/tasks/to-do/TASK-RESEARCH-<subject>-YYYYMMDD-HHMMSS/` with subfolders `research/`, `synthesis/`, `qa/`, `reviews/`

**MANDATORY — Partition large input across parallel agents.** Single-agent scope discovery is PROHIBITED for any input exceeding ~1000 lines total (this includes user-provided documents plus any referenced source files). Input size thresholds:
- **≤1000 lines total:** 1 scope-discovery agent is acceptable
- **1000-3000 lines:** 2-3 parallel agents, each assigned a slice (per-document, per-section-range, or per-aspect)
- **3000-6000 lines:** 4-5 parallel agents
- **6000+ lines:** 5-10+ parallel agents per the Deep tier requirement

**Partitioning heuristics:**
- By document — one agent per source file if multiple files
- By section range — split a large file into sequential section groups (e.g., sections 1-14 / 15-28)
- By aspect — requirements / architecture / data models / API specs / integration points as separate slices

**rf-task-researcher as agent type, not replacement:** The rf-task-researcher agent type may be used for each partitioned slice when context isolation is valuable. Spawn N rf-task-researchers in parallel (one per slice), each with its own RESEARCH_REQUEST scoping its assigned slice. A SINGLE rf-task-researcher reading the entire input is explicitly prohibited — it defeats parallelism and causes the same context pressure the partitioning is meant to prevent.

**Spawning pattern:** All scope-discovery agents MUST be spawned in parallel using multiple Agent tool calls in a single message. Sequential scope discovery is prohibited.

**Why this matters:** A single agent reading >1000 lines will skim, miss detail, and consume the parent orchestrator's context budget via its return value. Partitioning achieves depth (each agent focused on a slice) AND context protection (each slice isolated to its own agent context) simultaneously.

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
- Spawn one or more rf-task-researcher subagents in parallel with specific feedback about what's missing. For multiple gaps, spawn one agent per gap slice, not a single agent for all gaps

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

**For tech-research, the answer is almost always Template 02** — the skill inherently involves discovery (Phase 2), parallel agents (Phases 2-5), synthesis (Phase 5), and validation (Phase 6).

### A.7: Build the Task File

Write the BUILD_REQUEST to a file at `${TASK_DIR}BUILD-REQUEST.md`, then invoke the `/task-builder` skill. The task-builder reads the BUILD_REQUEST file, performs quality gates (rf-analyst + rf-qa), spawns the rf-task-builder agent to create the MDTM task file, and runs structural and qualitative validation internally. No manual verification step is needed — task-builder handles all validation and mediation.

**Step 1: Write `${TASK_DIR}BUILD-REQUEST.md`** using the Write tool with the following content:

```
# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: ${TASK_DIR}
Research Notes: ${TASK_DIR}research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Conduct a technical investigation on [GOAL] and produce a structured research report with findings, gap analysis, options, and implementation recommendations. The report will be written to `${TASK_DIR}RESEARCH-REPORT-[descriptor].md`.

WHY: [WHY — what prompted this investigation and what the findings will be used for]

TASK_ID_PREFIX: TASK-RESEARCH

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
- Phase 3 (Completeness Verification): L4 Review/QA — spawn 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (5 agents minimum, all report-only). Serialized fix: consolidate findings → single fix agent → verification round. Partitioning >6 files.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — agents read research files and produce report sections. Then spawn 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (5 agents minimum, all report-only). Serialized fix: consolidate → fix → verify. Partitioning >4 files.
- Phase 6 (Assembly & Validation): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final report. Then lens-based multi-agent QA: 3-5 rf-qa (structural lenses) + 3-5 rf-qa-qualitative (content lenses) + 3 domain-specific lenses (recommendation feasibility, finding reproducibility, implementation plan concreteness). All report-only. Serialized fix: consolidate → single fix agent → verification. Then source-document fidelity gate: 2-4 rf-qa fidelity agents reading codebase source files + full report. Then the anti-omission gate (Step 6.7b): 2-4 rf-analyst agents that exhaustively enumerate every distinct finding in the research + synthesis files and verify each is represented in the report (source→output completeness, the inverse of the fidelity gate).

QA_INTENSITY: [lite / standard / full]  (per I22 — determined by tier mapping in Depth Tiers section or user override)
QA_GATE_REQUIREMENTS: PER_PHASE
  **NOTE: Gate descriptions below specify FULL intensity agent counts. When QA_INTENSITY is lite or standard, the rf-task-builder applies I22 reductions via the QA Intensity Adaptation table in the Agent Prompt Templates section.**
  Gate 1: Research Completeness (Phase 3)
    - lite: 1 rf-qa (evidence + gaps) + 1 rf-qa-qualitative (depth + completeness) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 3 fix cycles. Partitioning >6 files.
  Gate 2: Synthesis Quality (Phase 5)
    - lite: 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 fix cycles. Partitioning >4 files.
  Gate 3: Report Validation (Phase 6)
    - lite: 1 rf-qa (combined structural) + 1 rf-qa-qualitative (combined content) + 1 domain lens (finding-reproducibility) = 3 agents. Max 1 fix cycle.
    - standard: 3 rf-qa structural (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content (actionability, domain-accuracy, crossref-chain) + 1 domain lens (finding-reproducibility) = 7 agents. Max 2 fix cycles.
    - full: 3-5 rf-qa + 3-5 rf-qa-qualitative (scaled by report size per I19) + 3 domain lenses (recommendation-feasibility, finding-reproducibility, implementation-plan-concreteness) = 9-13 agents. Max 3 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, after Gate 3)
    - lite: 1 rf-qa fidelity agent (combined semantic-coverage + phantom-detection lenses). Max 1 fix cycle.
    - standard: 2 rf-qa fidelity agents. Max 2 fix cycles.
    - full: 2 rf-qa fidelity agents (partition to 3-4 if source >1000 lines). Max 2 fix cycles. HALT after max cycles exceeded.
  Gate 5: Anti-Omission (Phase 6, after Gate 4): MANDATORY at every intensity
    - lite: 1 rf-analyst anti-omission agent (enumerate every distinct research+synthesis finding, verify each is represented in the report). Max 1 fix cycle.
    - standard: 2 rf-analyst anti-omission agents (partition the research+synthesis files). Max 2 fix cycles.
    - full: 2 rf-analyst anti-omission agents (partition to 3-4 if research+synthesis >1000 lines). Max 2 fix cycles. HALT after max cycles exceeded.
    - Method (all intensities): exhaustive enumeration (not spot-check); judge coverage by MEANING, never by ID/reference-citation; every omission is recovered or explicitly justified as dedup/out-of-scope, never silently dropped. This gate is the inverse of Gate 4 and is never skipped at any intensity.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
  TEMPLATE_COMPLIANCE: All report sections must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.

TESTING_REQUIREMENTS: N/A — documentation-only skill (research reports), no code produced, no tests applicable.

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
- Create the task folder at .dev/tasks/to-do/TASK-RESEARCH-<subject>-YYYYMMDD-HHMMSS/ with `research/`, `synthesis/`, `qa/`, `reviews/` subfolders

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research agent (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md
- Each item specifies: investigation topic, type, files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from SKILL.md) in each checklist item per B2
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. For example, with 8 research assignments: spawn all 8 agents in one message, mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.

Phase 3 — Research Completeness Verification (5-AGENT GATE + SERIALIZED FIX):

Step 3.1: Spawn lens-based research gate agents (PARALLEL, all fix_authorization: false)
  - [ ] Spawn rf-analyst (completeness lens) — reads all research files, applies coverage audit + completeness + cross-reference checks from 8-item checklist. Writes to `${TASK_DIR}qa/analyst-completeness-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-analyst (cross-validation lens) — reads all research files, applies contradiction detection + gap compilation + depth assessment checks. Writes to `${TASK_DIR}qa/analyst-cross-validation-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (evidence-quality lens) — reads all research files, applies file inventory + evidence density + scope coverage + doc cross-validation checks from 10-item checklist. Writes to `${TASK_DIR}qa/qa-research-evidence-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (gap-detection lens) — reads all research files, applies gap severity + depth appropriateness + integration points + pattern documentation + incremental writing checks. Writes to `${TASK_DIR}qa/qa-research-gaps-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa-qualitative (research-depth lens) — reads all research files, evaluates whether findings are genuinely deep or superficial. Are key findings actionable or vague? Does analysis go beyond surface-level code reading? Writes to `${TASK_DIR}qa/qa-research-qualitative-report.md`. Embed full prompt per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, EACH of the 5 agent types above gets partitioned into multiple instances with `assigned_files` subsets. For example, with 10 research files: 2 completeness-analyst (5 files each) + 2 cross-validation-analyst + 2 evidence-qa + 2 gap-qa + 2 depth-qualitative = 10 parallel agents. Each writes to numbered reports. Merge after completion.

Step 3.2: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL reports from Step 3.1, consolidate into `${TASK_DIR}qa/qa-consolidated-findings-phase3.md`
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated findings. Fix agent spawns additional targeted research agents for gaps requiring new research (one per gap). Applies all fixes.
  - [ ] Spawn rf-qa (verification, fix_authorization: false) + rf-qa-qualitative (verification, fix_authorization: false) to confirm fixes applied correctly
  - [ ] If verification finds new issues: repeat Step 3.2 (max 3 cycles total), then HALT — log issues in Task Log, present to user

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

Step 5.N+1: Spawn lens-based synthesis gate agents (PARALLEL, all fix_authorization: false)
  - [ ] Spawn rf-analyst (synthesis-accuracy lens) — reads all synth files + corresponding research files. Verifies synthesis claims trace back to research evidence. Applies items 1-5 of 10-item Synthesis Quality Review Checklist. Writes to `${TASK_DIR}qa/analyst-synthesis-accuracy.md`. Embed full prompt per B2.
  - [ ] Spawn rf-analyst (source-tracing lens) — reads all synth files + research files. Traces every synthesis claim to its research source. Verifies no fabrication, no doc-only claims in Sections 2/6/7/8, key findings reflected. Applies items 6-10 of checklist. Writes to `${TASK_DIR}qa/analyst-synthesis-tracing.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (structure lens) — reads all synth files. Applies items 1-6 of 12-item synthesis-gate checklist (section headers, table columns, fabrication, evidence citations, options analysis, implementation plan). Writes to `${TASK_DIR}qa/qa-synthesis-structure.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (content-quality lens) — reads all synth files. Applies items 7-12 of checklist (cross-section consistency, doc-only claims, stale docs, content rules, section completeness, hallucinated paths). Writes to `${TASK_DIR}qa/qa-synthesis-content.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa-qualitative (synthesis-coherence lens) — reads all synth files. Evaluates whether synthesis tells a coherent story from the research: do findings build logically? Are conclusions proportionate to evidence? Are contradictions between research files resolved? Writes to `${TASK_DIR}qa/qa-synthesis-qualitative-report.md`. Embed full prompt per B2.

- **Parallel partitioning for large workloads:** When >4 synthesis files exist, each agent type gets partitioned into multiple instances with `assigned_files` subsets. Same threshold rationale as Phase 3 but lower (>4 vs >6) because synthesis QA traces claims back to research.

Step 5.N+2: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL reports from Step 5.N+1, consolidate into `${TASK_DIR}qa/qa-consolidated-findings-phase5.md`
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated findings. Fixes issues in synth files in-place.
  - [ ] Spawn rf-qa (verification) + rf-qa-qualitative (verification) to confirm fixes
  - [ ] If issues remain: repeat Steps 5.N+2 (consolidate, fix, verify) (max 2 cycles total), then HALT

- Do NOT continue to Phase 6 without PASS verdict.

Phase 6 — Assembly & Validation (RF-ASSEMBLER + LENS-BASED QA + FIDELITY GATE):

Step 6.1: Assembly
  - [ ] Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") — NOT a general-purpose Agent — to assemble the final report. Hand it: the list of synth file paths in order (as component_files), the report output path `${TASK_DIR}RESEARCH-REPORT-[descriptor].md`, the Report Structure template from SKILL.md (as output_format), the Assembly Process steps from SKILL.md (as assembly_rules), and the Content Rules from SKILL.md (as content_rules). The assembler reads each synth file and writes the report incrementally section by section — header first, then sections in order, then Table of Contents, then cross-checks internal consistency (gaps in S4 addressed in S8, options in S6 reference S2, Open Questions in S9 not answered elsewhere, Evidence Trail in S10 lists all files). The assembler must be a single agent (NOT parallel) because cross-section consistency requires seeing the whole report. Embed the full assembler prompt (see Assembly Agent Prompt Template below and Assembly Process section in SKILL.md) in the checklist item per B2.

Step 6.2: Spawn lens-based rf-qa agents (PARALLEL, all fix_authorization: false)
  4 structural lens agents (agent count shown is for default 500-1500 line tier; task builder adjusts per BUILD_REQUEST Gate 3 scaling). Each agent reads the FULL report but evaluates ONLY its assigned lens. Prompt includes: "Assume this document has at least N errors. Find them." (N = report_lines / 100, minimum 5).
  - [ ] Spawn rf-qa (template-conformance lens) — all 10 report sections present or N/A, correct ordering, no remaining placeholders/sentinels. Output: `${TASK_DIR}qa/qa-lens-template-conformance.md`
  - [ ] Spawn rf-qa (internal-consistency lens) — IDs match across tables, counts agree, cross-references resolve, no contradictions within document. Output: `${TASK_DIR}qa/qa-lens-internal-consistency.md`
  - [ ] Spawn rf-qa (evidence-quality lens) — all claims cite file paths/line numbers, no unverified assertions, no hallucinated paths (verify parent dirs exist). Output: `${TASK_DIR}qa/qa-lens-evidence-quality.md`
  - [ ] Spawn rf-qa (completeness lens) — every topic from scope discovery appears in output, no gaps, no silently dropped items, evidence trail lists all files. Output: `${TASK_DIR}qa/qa-lens-completeness.md`

Step 6.3: Spawn lens-based rf-qa-qualitative agents (PARALLEL, all fix_authorization: false)
  4 content lens agents (agent count shown is for default 500-1500 line tier; task builder adjusts per BUILD_REQUEST Gate 3 scaling).
  - [ ] Spawn rf-qa-qualitative (actionability lens) — every recommendation is specific enough to execute without interpretation; criteria are testable pass/fail not aspirational. Output: `${TASK_DIR}qa/qa-lens-actionability.md`
  - [ ] Spawn rf-qa-qualitative (numbers-metrics lens) — all quantitative claims internally consistent, realistic, sourced; percentages add up; counts match between sections. Output: `${TASK_DIR}qa/qa-lens-numbers-metrics.md`
  - [ ] Spawn rf-qa-qualitative (crossref-chain lens) — trace end-to-end: gap → implementation step, option → evidence, finding → recommendation. Verify every link exists. Output: `${TASK_DIR}qa/qa-lens-crossref-chain.md`
  - [ ] Spawn rf-qa-qualitative (domain-accuracy lens) — claims about codebase match actual code; claims about product match capabilities; no aspirational features as current. Output: `${TASK_DIR}qa/qa-lens-domain-accuracy.md`

Step 6.4: Spawn domain-specific lens agents (PARALLEL, all fix_authorization: false)
  These 3 lenses are specific to tech-research output:
  - [ ] Spawn rf-qa-qualitative (recommendation-feasibility lens) — is the recommended option actually feasible given the codebase constraints documented in Section 2? Are effort/risk assessments realistic? Does the recommendation account for dependencies identified in gap analysis? Output: `${TASK_DIR}qa/qa-lens-recommendation-feasibility.md`
  - [ ] Spawn rf-qa-qualitative (finding-reproducibility lens) — could another investigator reproduce each finding by following the cited evidence? Are file paths and line numbers sufficient to locate each claim? Are data flow traces complete? Output: `${TASK_DIR}qa/qa-lens-finding-reproducibility.md`
  - [ ] Spawn rf-qa (implementation-plan-concreteness lens) — does the implementation plan specify actual files to create/modify, actual function signatures, actual integration points? Or is it generic ("create a service", "add configuration")? Every step must name specific files. Output: `${TASK_DIR}qa/qa-lens-implementation-concreteness.md`

Step 6.5: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL lens QA reports from Steps 6.2-6.4, consolidate into `${TASK_DIR}qa/qa-consolidated-findings-phase6.md`. Include: finding description, source lens, severity (CRITICAL/IMPORTANT/MINOR), affected section, proposed fix.
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated findings list. The fix agent reads the report, applies ALL fixes from the consolidated list, and documents each fix applied. Writes fix log to `${TASK_DIR}qa/qa-fix-log.md`.

Step 6.6: Verification round (PARALLEL)
  - [ ] Spawn rf-qa (verification, fix_authorization: false) — verify fixes applied correctly, no new issues introduced. Output: `${TASK_DIR}qa/qa-fix-verification.md`
  - [ ] Spawn rf-qa-qualitative (verification, fix_authorization: false) — verify content quality maintained after fixes. Output: `${TASK_DIR}qa/qa-fix-verification-qualitative.md`
  - [ ] If issues found: repeat Steps 6.5-6.6 (max 3 cycles), then HALT if unresolved.

Step 6.7: Source-document fidelity gate (PARALLEL)
  - [ ] Spawn rf-qa (fidelity-agent-1, fix_authorization: false) — reads the first half of codebase source files investigated during Phase 2 (from research file paths) + the FULL assembled report. Checks: semantic coverage (each major code component found in research appears in report), detail preservation (specific function names, line numbers, data types survive into report), phantom finding detection (report claims present in evidence trail but not substantiated by source code). Output: `${TASK_DIR}qa/qa-source-fidelity-report-1.md`
  - [ ] Spawn rf-qa (fidelity-agent-2, fix_authorization: false) — reads the second half of codebase source files + FULL report. Same checks. Output: `${TASK_DIR}qa/qa-source-fidelity-report-2.md`
  - [ ] If source files >1000 lines total: spawn 3-4 fidelity agents instead of 2, partitioning source files across agents.
  - [ ] Consolidate fidelity findings, apply fixes via serialized protocol (same as Step 6.5-6.6). Verification round on fidelity fixes. Max 2 fix cycles.
  - [ ] If fidelity issues persist after max 2 fix cycles: HALT, present to user.

Step 6.7b: Anti-omission gate (source→output completeness, PARALLEL): MANDATORY
  - [ ] Spawn rf-analyst (anti-omission-agent-1, fix_authorization: false): assigned the first half of the research + synthesis files. ENUMERATE every distinct finding/claim/recommendation/item in the assigned files, then verify EACH is represented (semantically) in the final report. CRITICAL METHOD: judge coverage by MEANING, never by ID/reference-citation; the report absorbs findings without citing their source IDs, so an ID-membership test is invalid and both over- and under-reports. A finding whose substance appears nowhere in the report = OMISSION. Rate each omission by importance (a dropped distinct finding/discipline = IMPORTANT or CRITICAL; a legitimately deduped restatement is NOT an omission, note it as covered-by-dedup). Output: `${TASK_DIR}qa/qa-anti-omission-report-1.md`
  - [ ] Spawn rf-analyst (anti-omission-agent-2, fix_authorization: false): assigned the second half of the research + synthesis files; same exhaustive enumerate-and-verify method, same output format. Output: `${TASK_DIR}qa/qa-anti-omission-report-2.md`
  - [ ] If the research + synthesis files exceed ~1000 lines total: spawn 3-4 anti-omission agents instead of 2, partitioning the files across agents so the enumeration is EXHAUSTIVE, never a spot-check.
  - [ ] Consolidate anti-omission findings. For EACH omission: either RECOVER it (the single fix agent adds the dropped finding to the report) or EXPLICITLY JUSTIFY it as intentional dedup / out-of-scope (recorded in the consolidated findings). NEVER silently drop an omission. Apply via the serialized fix protocol (report-only agents → consolidate → single fix agent → verification round). Max 2 fix cycles, then HALT and present to user.
  - [ ] This gate is the INVERSE of Step 6.7 (fidelity verifies output→source: no fabrication/distortion; anti-omission verifies source→output: no dropped finding). BOTH are mandatory; passing fidelity does NOT imply completeness.

- Zero leniency — no severity level is exempt. ALL findings must be resolved before Phase 7.

Phase 7 — Present to User & Complete Task:
- Present summary to user (report location, key findings, recommendation, research file count, open questions)
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date
- `NON-BLOCKING` Suggest downstream skill: "This research can feed directly into a Technical Reference document. You can create one using `/tech-reference` — the research files are already in place and will accelerate the process." Present the suggestion, mark this item complete immediately, and do NOT wait for a user response. This item does not gate task completion.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-RESEARCH-<subject>-YYYYMMDD-HHMMSS/TASK-RESEARCH-<subject>-YYYYMMDD-HHMMSS.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, report structure, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-RESEARCH-<subject>-YYYYMMDD-HHMMSS/TASK-RESEARCH-<subject>-YYYYMMDD-HHMMSS.md using PART 2 structure
7. Return the task file path
```

**Step 2: Invoke the task-builder skill:**
**CRITICAL: After task-builder completes and outputs TASK_FILE_READY, you MUST continue to Stage B below. Do NOT stop at task-builder's output.**


```
Skill(skill: "task-builder", args: "${TASK_DIR}BUILD-REQUEST.md")
```

The task-builder skill reads the BUILD_REQUEST file, detects `Source: skill-delegated` and `SKIP_RESEARCHERS: true`, skips its own research phase, spawns the rf-task-builder agent, and runs structural and qualitative validation internally. It returns the task file path.

**Note:** Task-builder handles all verification internally — structural validation checks frontmatter, phases, B2 pattern, embedded prompts, parallel spawning instructions, partitioning guidance, rf-assembler usage, and anti-orphaning. Qualitative validation checks operational correctness. No separate verification step is needed in this skill. Proceed directly to Stage B with the returned task file path.

---

## Stage B: Task File Execution

Stage B delegates execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA verification, error handling, and session management.

### Delegation Protocol

1. **Invoke /task** using the Skill tool with `skill: "task"` and `args` set to the task file path from Stage A (e.g., `.dev/tasks/to-do/TASK-RESEARCH-locomotion-params-20260309-120000/TASK-RESEARCH-locomotion-params-20260309-120000.md`).
2. **Execution transfers to /task**, which reads the task file and processes each checklist item via the F1 loop — spawning subagents as specified in B2 items and running phase-gate QA after each phase (Phase 2+).
3. **No additional execution logic is needed** in this skill since all execution rules (F1 loop, F2 prohibited actions, parallel spawning, F4 modification restrictions, F5 frontmatter protocol, error handling, session resumption) are provided by /task.
4. **QA coverage:** The task file already contains skill-specific QA items (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative at Phases 3 and 5; lens-based multi-agent rf-qa + rf-qa-qualitative + domain-specific lenses + source-document fidelity gate at Phase 6), and /task adds phase-gate QA on top. This results in intentional, acceptable double QA at gate phases — skill-specific QA uses domain-aware lens-based gates while /task's phase-gate QA verifies "ensuring..." clauses from all items in the phase.
5. **Depth tier handling:** The task file created by Stage A already encodes the correct phases and agent counts for the selected depth tier (Quick/Standard/Deep). /task does not need to know about depth tiers — all tier logic lives in Stage A's BUILD_REQUEST, which selects the appropriate number of research agents, web research scope, and partitioning thresholds and embeds them into the task file's B2 items.

### What the Task File Must Contain

Since /task does NOT read this SKILL.md during execution, all skill-specific instructions must be baked into the task file during Stage A:

- **Agent prompt templates** customized with specific investigation topics, file paths, and research assignments
- **Validation checklists and content rules** embedded in "ensuring..." clauses of each B2 item
- **Output paths and file naming conventions** specified in each item (research/, synthesis/, qa/, reviews/ subdirectories)
- **Depth-tier-specific phase items** selected by Stage A based on the detected tier
- **Partitioning guidance** for analyst/QA agents when file counts exceed thresholds (>6 research files for Phase 3, >4 synth files for Phase 5)
- **All phase-specific context** so each B2 item is fully self-contained — an executor reading only the task file has everything needed to complete each item

**CRITICAL:** `/task` does NOT read this SKILL.md during execution. ALL skill-specific instructions, agent prompts, validation criteria, and content rules must be baked into the task file items during Stage A. This includes prohibited actions: research agents READ code, they do not modify it; do not invent file paths; do not fabricate content; do not delete research artifacts after assembly.

---

## Agent Prompt Templates

These templates are provided to the task builder (in the BUILD_REQUEST) so it can embed them in the task file's self-contained checklist items. The builder should customize each instance with the specific investigation topic, files, and output path.

**QA Intensity Adaptation (per Template 02 I22):**
- lite: Gate 3 combines to 3 agents:
  (1) rf-qa combined-structural: use template-conformance + internal-consistency + evidence-quality + completeness lenses
  (2) rf-qa-qualitative combined-content: use actionability + domain-accuracy + crossref-chain + numbers-metrics lenses
  (3) highest-value domain lens: finding-reproducibility
  Intermediate gates: 2 agents (1 rf-qa combined + 1 rf-qa-qualitative combined)
  Fidelity: 1 agent (combined coverage + phantom lenses). Max 1 fix cycle. 1 verification agent.
- standard: Gate 3 uses 7 agents:
  3 rf-qa structural: template-conformance, internal-consistency, evidence-quality
  3 rf-qa-qualitative content: actionability, domain-accuracy, crossref-chain
  1 domain lens: finding-reproducibility
  Intermediate gates: 3 agents (1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative)
  Fidelity: 2 agents. Max 2 fix cycles. 2 verification agents.
- full: Use all prompts below as-is (current behavior, no changes).

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
11. **Key findings from research must be reflected in synthesis.** Before finalizing your output, read the Summary/Key Takeaway section of every research file you were assigned. Each key finding must either appear in your synthesis or be explicitly noted as excluded with rationale. Data included in tables but omitted from conclusions/recommendations is a synthesis failure.

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
Analyst reports: [task-dir-path]qa/analyst-completeness-report.md and [task-dir-path]qa/analyst-cross-validation-report.md (if they exist, verify the analysts' work; if not, perform full verification)
Research notes file: [task-dir-path]research/research-notes.md
Depth tier: [Quick/Standard/Deep]
Output path: [output-path]

You are the last line of defense before synthesis begins. Assume everything is wrong until you verify it.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

IF ANALYST REPORT EXISTS:
1. Read all analyst reports
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
Fix authorization: false (report findings only — a separate fix agent applies all fixes via serialized protocol)
Output path: [output-path]

You are verifying that synthesis files are ready for assembly into the final report.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

PROCESS:
1. Use Glob to find ALL synth files (synth-*.md) in the synthesis directory (`${TASK_DIR}synthesis/`)
2. Read EVERY synth file completely
3. Apply the 12-item Synthesis Gate checklist from your agent definition
4. For each issue found:
   a. Document the issue (what, where, severity)
   b. Document the required fix with specific location and suggested correction. Do NOT fix in-place — a separate fix agent handles all fixes.
5. Write your QA report to [output-path]

12-ITEM CHECKLIST:
1. Section headers match Report Structure template
2. Table column structures correct
3. No fabrication (Verify EVERY claim in each file, trace to research files)
4. Evidence citations use actual file paths
5. Options analysis: 2+ options with pros/cons
6. Implementation plan: specific file paths, not generic steps
7. Cross-section consistency (gaps in S4 addressed in S8, etc.)
8. No doc-only claims in Sections 2, 6, 7, or 8
9. Stale docs surfaced in Sections 4 or 9
10. Content rules compliance (tables over prose, no code reproductions)
11. All expected sections have content (no placeholders)
12. No hallucinated file paths (verify parent directories exist)

VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found (list with specific fixes and locations)
```

### Report Validation QA Agent Prompt (rf-qa — Report Validation)

> **LEGACY PROMPT** — This single-agent validation prompt is superseded by the lens-based multi-agent approach in Steps 6.2-6.4. It is retained as a reference for the combined checklist items that the lens agents collectively verify. Do NOT use this prompt for Phase 6 QA — use the Lens-Specific QA Agent Prompt Template instead.

```
Perform final QA validation of the assembled research report for [topic].

QA phase: report-validation
Report path: [report-path]
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Synthesis directory: [task-dir-path]synthesis/
Output path: [output-path]
Fix authorization: false (report findings only)

You report findings only. A serialized fix agent applies all corrections.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

PROCESS:
1. Read the ENTIRE research report
2. Apply the 15-item Validation Checklist + 4 Content Quality Checks
3. For each issue: document it with location, severity, and suggested fix (do NOT fix in-place)
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

Report every issue you find with specific location and fix recommendation. Do NOT apply fixes — the serialized fix agent handles all corrections.
```

### Qualitative QA Agent Prompt (rf-qa-qualitative — Report Qualitative Review)

> **LEGACY PROMPT** — This single-agent qualitative review prompt is superseded by the content lens agents (Step 6.3) and domain-specific lens agents (Step 6.4). Retained as reference for the combined qualitative checklist. Do NOT use for Phase 6 QA.

```
Perform qualitative review of the assembled research report for [topic].

QA phase: report-qualitative
Report path: [report-path]
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Synthesis directory: [task-dir-path]synthesis/
Output path: [output-path]
Fix authorization: false (report findings only)

You are performing a deep content-quality review — does this report make sense as a technical investigation?

**ADVERSARIAL STANCE:** Assume this document has at least 10 errors. Find them. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

PROCESS:
1. Read the ENTIRE research report
2. Apply the 12-item Research Report Qualitative Review checklist below
3. For each issue: document it with severity (CRITICAL/IMPORTANT/MINOR) and suggested fix (do NOT fix in-place)
4. Write your QA report to [output-path]

12-ITEM QUALITATIVE REVIEW CHECKLIST:
1. Problem statement matches findings — does the report actually answer the question posed?
2. Options are genuinely distinct — not variants of the same approach dressed up differently
3. Recommendation follows from analysis — the recommended option should be the logical winner of the comparison, not an arbitrary choice
4. Implementation plan is actionable — a developer could begin work from Section 8 alone without needing to re-research
5. Gaps are honestly acknowledged — no optimistic hand-waving; if something is unknown, it appears in Open Questions
6. No circular reasoning — conclusions don't depend on unverified assumptions stated earlier as facts
7. Evidence trail is complete — every research and synthesis file appears in Section 10
8. Conclusion is proportionate to evidence strength — strong claims require strong evidence; weak evidence gets hedged language
9. External research is properly contextualized — web findings supplement but never override code findings
10. Cross-section consistency — no contradictions between Problem Statement, Gap Analysis, Options, and Implementation Plan
11. Technical accuracy — code patterns, function signatures, and architecture described match what research files documented
12. Depth matches tier — a Deep-tier investigation should have comprehensive coverage; a Quick-tier can be narrower

SEVERITY DEFINITIONS:
- CRITICAL: Factual error, contradictory sections, missing major topic, recommendation unsupported by evidence
- IMPORTANT: Shallow analysis, vague implementation steps, missing cross-references, unacknowledged gaps
- MINOR: Formatting issues, minor inconsistencies, could-be-clearer language

Report every issue you find with specific location and fix recommendation. Do NOT apply fixes.
```

### Lens-Specific QA Agent Prompt Template (for Phase 6 lens agents)

```
Perform [LENS_NAME] quality review of the assembled research report for [topic].

QA phase: report-lens-[lens-slug]
Lens focus: [LENS_NAME]
Report path: [report-path]
Task directory: [task-dir-path]
Output path: [output-path]
Fix authorization: false (report findings only — do NOT modify the document)

You are evaluating ONE quality dimension of this document. Your ONLY job is [LENS_NAME].
Do NOT check other quality dimensions — other agents handle those.

**ADVERSARIAL STANCE:** Assume this document has at least [N] errors in your dimension. Find them. (N = document_lines / 100, minimum 5)

LENS-SPECIFIC CHECKLIST:
[LENS_CHECKLIST_BLOCK — use the matching checklist below based on LENS_NAME]

--- STRUCTURAL LENSES (rf-qa, Step 6.2) ---

Template-Conformance Checklist:
  a. All 10 report sections present (S1-S10) or explicitly marked N/A with rationale
  b. Section ordering matches the Report Structure template exactly (no reordering, no merged sections)
  c. No placeholder text, sentinel values, or TODO markers remaining anywhere in the document
  d. Table of Contents entries match actual section headers (names and hierarchy)

Internal-Consistency Checklist:
  a. IDs, labels, and names used in tables match their references in prose (e.g., Option A in S6 is the same Option A in S7)
  b. Counts agree across sections (number of gaps in S4 matches gap references in S8; file counts in S10 match research files)
  c. Cross-references resolve — every "see Section N" or "as described in S.N" points to content that actually exists
  d. No contradictions within the document (e.g., S2 says X exists, S4 says X is missing)

Evidence-Quality Checklist:
  a. Every factual claim cites a specific file path and line number (not just a directory or vague reference)
  b. No unverified assertions presented as fact — claims without evidence carry [UNVERIFIED] tags
  c. No hallucinated file paths — verify that parent directories of all cited paths exist in the codebase
  d. Code-sourced claims distinguish between code evidence and doc evidence ([CODE-VERIFIED] vs [UNVERIFIED])

Completeness Checklist:
  a. Every topic from scope discovery (research-notes.md) appears in the final output — no silently dropped items
  b. No gaps from gap-analysis are unaddressed — each gap either has a resolution in S8 or appears in Open Questions S9
  c. Evidence Trail (S10) lists every research file and synthesis file produced during the investigation
  d. All research Key Takeaways are reflected in synthesis conclusions or explicitly noted as excluded with rationale

--- CONTENT LENSES (rf-qa-qualitative, Step 6.3) ---

Actionability Checklist:
  a. Every recommendation in S7 is specific enough to execute without re-research (names files, functions, integration points)
  b. Implementation Plan steps (S8) each specify: action, target file(s), and expected outcome
  c. Success criteria are testable pass/fail — not aspirational ("improve performance" fails; "reduce p95 latency below 200ms" passes)
  d. A developer unfamiliar with the investigation could begin work from S8 alone

Numbers-Metrics Checklist:
  a. All quantitative claims are internally consistent (percentages add to 100%, counts match between sections)
  b. Effort/risk/complexity estimates are sourced or justified, not arbitrary
  c. Size/count metrics (file counts, line counts, component counts) match verifiable codebase data
  d. No unsourced statistics or benchmarks presented as fact

Crossref-Chain-Integrity Checklist:
  a. Every gap in S4 has a corresponding resolution step in S8 or an entry in Open Questions S9
  b. Every option in S6 references evidence from S2 (Current State) or S5 (External Research)
  c. Every recommendation in S7 traces back to the options comparison in S6
  d. Every finding in S2/S3 that warrants action appears in either S4 (as a gap) or S8 (as an implementation step)

Domain-Accuracy Checklist:
  a. Claims about codebase architecture match actual code structure (verified via file paths and function signatures)
  b. Claims about product capabilities match what the code actually implements — no aspirational features described as current
  c. Technology version claims match package.json / requirements.txt / actual dependency files
  d. Integration point descriptions (APIs, data flows, event chains) match verified code behavior

--- DOMAIN-SPECIFIC LENSES (tech-research, Step 6.4) ---

Recommendation-Feasibility Checklist (rf-qa-qualitative):
  a. Recommended option is actually feasible given codebase constraints documented in S2
  b. Effort and risk assessments are realistic — not optimistic hand-waving
  c. Recommendation accounts for dependencies identified in gap analysis (S4)
  d. No recommended changes to components that don't exist or are deprecated

Finding-Reproducibility Checklist (rf-qa-qualitative):
  a. Another investigator could reproduce each finding by following the cited evidence trail
  b. File paths and line numbers are sufficient to locate each claim without searching
  c. Data flow traces are complete — no missing intermediate steps
  d. Key code patterns are described precisely enough to identify in source (function names, class names, config keys)

Implementation-Plan-Concreteness Checklist (rf-qa):
  a. Every implementation step names specific files to create or modify (no generic "create a service" or "add configuration")
  b. Function signatures or interface contracts are specified where new code is proposed
  c. Integration points name specific existing functions/endpoints/events to connect to
  d. Migration or rollback considerations are addressed where applicable

OUTPUT FORMAT:
## [LENS_NAME] QA Report
**Report reviewed:** [report-path]
**Lens:** [LENS_NAME]
**Date:** [today]

### Findings
| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|-------------|
| 1 | CRITICAL/IMPORTANT/MINOR | Section N | [description] | [specific fix] |

### Summary
- Total findings: [count]
- Critical: [count]
- Important: [count]
- Minor: [count]
- Verdict: PASS (0 critical + 0 important + 0 minor) / FAIL
```

### Source-Document Fidelity Agent Prompt (rf-qa — Fidelity Gate)

```
Perform source-document fidelity verification for [topic].

QA phase: source-fidelity
Report path: [report-path]
Assigned source files: [list of codebase source file paths from research phase]
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Output path: [output-path]
Fix authorization: false (report findings only)

You are verifying that the assembled report faithfully represents the actual codebase.
Read your assigned source files first, then read the full report, then check fidelity.

**ADVERSARIAL STANCE:** Assume the report has distorted at least 5 findings during synthesis. Find them.

FIDELITY CHECKLIST:
1. Semantic coverage — for each major component/function/pattern in the source files, does the report contain a corresponding finding that accurately describes it?
2. Detail preservation — specific details from source code (function signatures, parameter types, error handling patterns, configuration values) survive into the report, not just high-level summaries
3. Phantom finding detection — does the report claim findings that cannot be traced back to actual source code? Verify at least 5 specific claims by reading the cited source files.
4. Accuracy of code characterization — when the report describes how code works (data flow, call chains, error handling), does the description match what the code actually does?
5. No aspirational claims — the report does not describe planned/future code as if it currently exists

OUTPUT FORMAT:
## Source-Document Fidelity Report
**Report reviewed:** [report-path]
**Source files checked:** [count] files, [total lines] lines
**Date:** [today]

### Fidelity Findings
| # | Type | Source File | Report Section | Finding | Severity |
|---|------|-------------|---------------|---------|----------|
| 1 | Missing/Distorted/Phantom/Inaccurate | [path] | Section N | [description] | CRITICAL/IMPORTANT/MINOR |

### Summary
- Files checked: [count]
- Claims verified: [count]
- Fidelity issues: [count]
- Verdict: PASS / FAIL
```

### Anti-Omission Agent Prompt (rf-analyst, Anti-Omission Gate)

```
Perform anti-omission (source→output completeness) verification for [topic].

QA phase: anti-omission
Assigned input files: [slice of research/*.md + synthesis/*.md files]
Final report: [report-path]
Output path: [output-path]
Fix authorization: false (report findings only)

You verify that NO distinct finding was silently dropped when the research + synthesis
inputs were compressed into the final report. This is the INVERSE of the fidelity gate:
fidelity checks output→source (no fabrication); you check source→output (no omission).

**ADVERSARIAL STANCE:** Assume the compression silently dropped at least 5 distinct findings. Find them.

**CRITICAL METHOD: do NOT use ID/reference-citation as your coverage test.** The report
absorbs findings without citing their source IDs, so an ID-membership test is invalid (it
both over- and under-reports). Judge coverage by MEANING.

ANTI-OMISSION CHECKLIST:
1. ENUMERATE every distinct finding / claim / rule / recommendation / item in your assigned input files. Be exhaustive: list them, do not sample.
2. For EACH enumerated finding, search the final report for a SEMANTIC representation (the substance appears, regardless of wording or whether the source ID is cited).
3. Classify each: REPRESENTED (cite where in the report) | OMITTED (substance appears nowhere) | COVERED-BY-DEDUP (legitimately merged into another item, name it; this is NOT an omission).
4. Rate each OMISSION by importance: CRITICAL (a distinct foundational discipline/finding dropped) | IMPORTANT (a distinct secondary finding dropped) | MINOR (a redundant detail).
5. Do not invent omissions for findings that are genuinely deduped or out-of-scope, but when in doubt, FLAG it (a false OMISSION is cheap to dismiss; a missed drop is the failure this gate exists to prevent).

OUTPUT FORMAT:
## Anti-Omission Report
**Report reviewed:** [report-path]
**Input files checked:** [list], [total findings enumerated]
**Date:** [today]

### Omissions Found
| # | Source finding | Source file | Status (OMITTED / COVERED-BY-DEDUP) | If deduped, by which report item | Severity |
|---|---------------|-------------|-------------------------------------|----------------------------------|----------|
| 1 | [the dropped finding] | [path] | OMITTED | n/a | CRITICAL/IMPORTANT/MINOR |

### Summary
- Findings enumerated: [count]
- Represented: [count]  Covered-by-dedup: [count]  Omitted: [count]
- Verdict: PASS (0 omitted) / FAIL ([n] omitted)
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
| [gap] | [what exists] | [what's needed] | Critical/Important/Minor | [context] |

**Docs may not close a defect (C8, behavioral-reachability control).** A gap that is an **UNWIRED IN-SCOPE capability** — one the driving spec/TDD names as shipped or enabled-by-config but that is NOT actually wired at its runtime entrypoint (no production caller, its result discarded/dead-guarded, or its callee a not-implemented sentinel such as an `ErrNoStream`-shape stub) — is a **DEFECT, not merely future-phase work**. It MUST be recorded with Severity **Critical/High**, MUST carry (or link) an MDTM remediation task under `.dev/tasks/to-do/`, and MUST NOT be silently downgraded to "future phase" / "later release" / Open Question **without an on-record, cited scope decision** (a spec/user decision, with citation, that the capability is deliberately out of scope). A research Gap Analysis may not retire an unwired in-scope capability by labeling it future work. (This mirrors the tech-reference C8 rule; both exist because the v1.4.1 WS-dial post-mortem records docs normalizing an unwired `Subscribe` as a documented gap instead of a defect.)

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

**This checklist is now enforced by 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative agents** (see Phase 5 in the task phases above). The rf-analyst agents apply these 10 criteria split across two lenses (synthesis-accuracy and source-tracing). The rf-qa agents independently verify with the 12-item Synthesis Gate checklist split across two lenses (structure and content-quality). The rf-qa-qualitative agent evaluates synthesis coherence — whether the synthesis tells a coherent story from the research. All agents report findings only (fix_authorization: false); a single fix agent then applies all collected findings via serialized fix protocol.

The 10 criteria (used by rf-analyst):

1. Report section headers match the expected format from the Report Structure template
2. Tables use the correct column structure (Gap/Current/Target/Severity, Criterion/OptionA/OptionB, Step/Action/Files/Details)
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and evidence (not vague descriptions)
5. Options analysis includes at least 2 options with pros/cons assessment tables
6. Implementation plan has specific steps with file paths (not generic actions like "create a service")
7. All cross-references between sections are consistent (e.g., gaps in Section 4 are addressed in Section 8)
8. **No doc-only claims in Current State, Options, Recommendation, or Implementation Plan.** Verify that Sections 2, 6, 7, and 8 only contain architecture descriptions backed by code-traced evidence. If a synth file describes a pipeline, service, or component and the only evidence is a documentation file (no source code path), reject that claim and either remove it or flag it as `[UNVERIFIED — doc-only]`
9. **Stale documentation discrepancies are surfaced.** Any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings from research files should appear in the Gap Analysis (Section 4) or Open Questions (Section 9), not silently omitted
10. **Key finding coverage.** Each research file's Summary/Key Takeaway section contains findings that should be reflected in the synthesis. Verify that the strongest findings from source research are represented in synthesis conclusions/recommendations. Flag any research Key Takeaway that has no corresponding synthesis content.

The rf-qa agents apply an independent 12-item Synthesis Gate checklist (see Synthesis QA Agent Prompt). Items 1-10 overlap with the analyst criteria above; the following 3 items are unique to rf-qa:

11. Content rules compliance (tables over prose, no code reproductions)
12. Section completeness (all expected sections have content, no placeholders)
13. Hallucinated file path detection (verify parent directories exist for all cited paths)

If synthesis QA fails, the serialized fix agent applies all collected fixes. Issues remaining after max fix cycles trigger re-synthesis of affected files.

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
- [ ] Every agent prompt includes its required protocol blocks (Incremental Writing for all, ADVERSARIAL STANCE for QA, Documentation Staleness for research)
- [ ] Every distinct finding/requirement/recommendation in the research and synthesis inputs is represented in the generated report, OR explicitly justified as deduped/out-of-scope (the anti-omission gate, Step 6.7b; judged by meaning, never by ID/reference-citation; exhaustive, not a spot-check). If a design spec or requirements document was an input, every feature/requirement in it is likewise covered.
- [ ] Phase 3 QA gate spawns at least 5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative) with serialized fix authorization
- [ ] Phase 5 QA gate spawns at least 5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative) with serialized fix authorization
- [ ] Phase 6 QA gate spawns at least 6 lens-based agents (3 rf-qa structural + 3 rf-qa-qualitative content), scaled up to 8 (4+4) for 500-1500 lines and 10 (5+5) for >1500 lines per Gate 3, PLUS 3 domain-specific lenses (recommendation feasibility, finding reproducibility, implementation plan concreteness)
- [ ] Phase 6 uses serialized fix protocol (all agents report-only → consolidate → single fix agent → verification round)
- [ ] Source-document fidelity gate runs after lens-based QA with at least 2 fidelity agents reading codebase source files + full report
- [ ] Anti-omission gate (Step 6.7b) runs after the fidelity gate with at least 2 rf-analyst agents that exhaustively enumerate every distinct finding in the research + synthesis files and verify each is represented in the final report (source→output completeness, judged semantically not by ID-citation); every omission is recovered or explicitly justified, never silently dropped
- [ ] All QA agents use fix_authorization: false (report-only) except the single designated fix agent per gate

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

Two execution-discipline rules (task-file-source-of-truth, maximize-execution-parallelism) are enforced by the `/task` skill during Stage B and do not appear here. The rules below govern Stage A (scope discovery, research, task file creation) and the content quality standards for all agents.

Violations compromise research quality.

1. **Incremental writing is mandatory — ZERO TOLERANCE.** Every agent's FIRST ACTION must be creating its output file on disk using Write (frontmatter/header only). All subsequent content is appended using Edit, one section at a time. NEVER accumulate content in context and attempt a single large Write — this is the #1 failure mode across all agents. It hits max token output limits and freezes the process, losing all work. The procedure is: Write (create file with header) → Edit (append section 1) → Edit (append section 2) → ... → Edit (update Status to Complete). This applies to: research agents, synthesis agents, analyst reports, QA reports, task file builder, and assembler.

2. **Codebase is source of truth.** Web research supplements but never overrides verified code findings. Internal documentation is treated with the same skepticism as external sources unless code-verified.

3. **Evidence-based claims only.** Every finding must cite actual file paths, line numbers, function names, class names. No assumptions, no inferences, no guessing. If you can't verify it, mark it as "Unverified — needs confirmation."

4. **Default to Deep.** Unless the question is clearly answerable with a quick scan of <5 files, use the Deep tier. When in doubt, go deeper.

5. **No one-shotting reports.** Agents must write incrementally as they discover information. The orchestrator must write the final report section by section. This is non-negotiable.

6. **Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, codebase-retrieval for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations.

7. **Gap-driven web research.** Do not web search everything up front. First investigate the codebase thoroughly (Phase 2), identify specific gaps, then target web research (Phase 4) at those gaps. This keeps web research focused and efficient.

8. **Preserve research artifacts.** Research and web research files persist after the report is written. They serve as the evidence trail for all claims and enable future re-investigation without starting from scratch. Do NOT delete research files, synthesis files, or the gaps log after assembly.

9. **Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. The synthesis phase relies on these connections to build a coherent picture across investigation slices.

10. **Implementation plans must be actionable.** The implementation plan section should contain enough detail that a developer (or another AI agent) could begin work from it. Include specific files to create/modify, code patterns to follow, and integration points.

11. **Report all uncertainty.** If something is unclear, ambiguous, or requires a judgment call, document it in Open Questions. Do not silently pick one interpretation and present it as fact.

12. **Documentation is not verification.** Internal documentation (design docs, architecture docs, integration guides, READMEs in `docs/`) describes intent, history, or planned state — NOT necessarily current state. A doc saying "Service X exists at path Y" does not prove Service X exists. Only reading actual source code at path Y proves it exists. Doc Analyst agents MUST cross-validate every architectural claim against actual code using the Documentation Staleness Protocol. Any doc-sourced claim without a `[CODE-VERIFIED]` tag is treated as unverified.

13. **Docs-vs-code has the same trust hierarchy as web-vs-code.** Critical Rule 2 establishes that web research never overrides code. The same applies to internal documentation: if a doc describes an architecture that contradicts what the code shows, **the code is correct and the doc is stale**. This is especially dangerous because internal docs feel authoritative — but a doc written 6 months ago about a planned architecture may describe services, pipelines, and components that were never built, were refactored, or were removed. Treat internal docs with the same skepticism as external blog posts unless code-verified.

14. **QA gates are checklist items, not prose — with minimum agent counts.** Every QA gate specified in QA_GATE_REQUIREMENTS must appear in the generated task file as individual `- [ ]` checklist items following B2 self-contained pattern — one item per agent. QA gates described only in prose or comments are invisible to the F1 executor and will be skipped. **Minimum agent counts are FLOORS:** intermediate gates (research, synthesis) require at least 5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative). Final document gates require at least 6 agents (3 rf-qa structural lenses + 3 rf-qa-qualitative content lenses), scaled by output size per the agent count table in QA_GATE_REQUIREMENTS. Domain-specific lenses are ADDED on top. Any QA gate in a generated task file with fewer than 5 total agents is REJECTED during task-builder validation. (Intermediate gates: 5 minimum. Output/final gates: 6 minimum before domain lenses are added.) **Serialized fix authorization:** all gate agents use fix_authorization: false (report-only). A single fix agent applies all collected findings. A verification round confirms fixes.

15. **Every agent prompt MUST include ALL mandatory protocol blocks:** Incremental File Writing Protocol (all agents), ADVERSARIAL STANCE (QA/analyst agents), Documentation Staleness Protocol (research agents). Missing protocol blocks are the most common generation defect — verify every prompt individually.

16. **Single-agent large-input prohibition.** No single agent may read more than ~1000 lines of input at any discovery, analysis, or extraction stage. Large inputs MUST be partitioned into slices, with one agent per slice spawned in parallel. The rf-task-researcher agent type is permitted per slice but not as a replacement for parallelism. Violations cause shallow coverage and defeat the Deep-tier depth guarantee.

17. **No scope/cost-anxiety pauses during execution.** Once a task file begins executing (via /task or any execution loop), the executor MUST process every item sequentially to completion. It MUST NOT pause mid-execution to present the user with options like "stop here and review, or continue to phase N?" or to flag scope/cost/time concerns. Scope is established at task file creation time. Cost is committed when the user invokes execution. The only permitted mid-execution halts are: all items blocked by the same unrecoverable issue, phase-gate QA failing 3 fix cycles, or an item output fundamentally invalidating the rest of the task. "This will take a while" / "Phase N is expensive" / "the user might want to review" are NOT valid halt reasons. Pausing for these reasons violates the F1 loop discipline and the skill's trust model.

18. **Anti-omission is mandatory: the inverse of fidelity, and not optional.** Compression (research → synthesis → report) silently drops distinct findings, and the fidelity gate does NOT catch this: fidelity verifies output→source (no fabrication/distortion), which a report can pass while dropping half its inputs. A source→output completeness gate is therefore mandatory (Step 6.7b): enumerate EVERY distinct finding in the research and synthesis files and verify each is represented in the final output. Judge coverage by MEANING, never by ID/reference-citation; the synthesis absorbs findings without citing their source IDs, so an ID-membership test is invalid (it both over- and under-reports). The enumeration MUST be exhaustive and partitioned across agents, never a spot-check. Every omission is recovered or explicitly justified as intentional dedup / out-of-scope; an omission is NEVER silently dropped. This rule exists because a prior large research run mined ~890 rules, compressed them to 94, and silently dropped ~50 distinct disciplines that no gate was looking for; the fidelity gate passed because nothing was fabricated, yet the output was materially incomplete.

---

## Session Management

Session management is provided by the `/task` skill. At session start, check `.dev/tasks/to-do/` for `TASK-RESEARCH-*/` folders related to the current topic.

**Resume states (from A.1):**
- **Task file exists with unchecked items** → Skip Stage A, invoke `/task` with the task file path — it resumes from the first unchecked `- [ ]` item.
- **Task file exists, all items checked** → Research is complete. Offer to re-run or build on existing research.
- **Task folder exists, `research-notes.md` has `Status: Complete`, but no task file** → Resume at A.5 (review sufficiency, then build task file).
- **Task folder exists, `research-notes.md` has `Status: In Progress`** → Resume at A.3 (continue scope discovery from where it left off).
- **Task folder exists but no `research-notes.md`** → Resume at A.3 using the existing folder.
- **No task folder exists** → Start fresh at A.2.

If a task file is found, invoke `/task` with the task file path — it reads the file, finds the first unchecked `- [ ]` item, and resumes from there.

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
