---
name: prd
description: "Create or populate a Product Requirements Document (PRD) for a product, feature, or platform. Use this skill when the user wants to create a PRD, document product requirements, populate an existing PRD stub, or write a comprehensive product requirements document following the project template. Trigger on phrases like 'create a PRD for...', 'document the product requirements', 'write a PRD', 'populate this PRD', 'product requirements for the wizard system', or when the user references a PRD file that needs content following the PRD template. Also trigger when the user says 'define the product' in the context of product planning or requirements gathering."
---

# PRD Creator

A skill for creating comprehensive Product Requirements Documents (PRDs) for products, features, and platform capabilities. This skill uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts.

**How it works:** The skill performs initial scope discovery (mapping the product area, identifying research topics, assessing complexity), then spawns the `rf-task-builder` subagent to create an MDTM task file encoding all investigation, synthesis, and assembly phases. The skill then executes from that task file, marking items complete as it progresses. If context compresses or the session restarts, the skill re-reads the task file and resumes from the first unchecked item.

The output always follows the project template at `.claude/templates/documents/prd_template.md`. The template is the schema — every PRD must conform to it.

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
| Final PRD | `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md` |
| Template schema | `.claude/templates/documents/prd_template.md` |

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

6. **Select depth tier** based on component count — Lightweight (<5 files), Standard (5-20), Heavyweight (20+). Default to Standard if unsure. Record the tier selection and rationale in the research notes.

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

The file MUST be organized into these 6 categories (include all, mark as "N/A" if empty):

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

**BUILD_REQUEST format for the subagent prompt:**

```
BUILD_REQUEST:
==============
GOAL: Create a comprehensive Product Requirements Document (PRD) for [GOAL] following the project template at .claude/templates/documents/prd_template.md. The PRD will be written to [OUTPUT_PATH].

WHY: [WHY — what this PRD is for and how it will be used]

TASK_ID_PREFIX: TASK-PRD

TEMPLATE: [01 or 02 — skill selects:
  01 = simple PRD update, straightforward execution
  02 = needs discovery, parallel research, web research, synthesis, quality gates, assembly]

PRD_SCOPE: [Product PRD / Feature PRD]
If Feature PRD, the following sections are affected:
- S2 Problem Statement: Do NOT include a "Market Opportunity" subsection with TAM/SAM/SOM.
  Instead include "Why This Feature is Required" explaining criticality to the platform.
  Reference Platform PRD for market context.
- S3 Background & Strategic Fit: Focus on why THIS FEATURE is needed now (what enablers
  exist, what dependencies are ready, what bets it makes). Do NOT repeat platform-level
  market trends, company revenue projections, or competitive moat. Reference Platform PRD.
- S5 Business Context: Skip market sizing, revenue projections, and KPI tables. Include
  business justification (why this feature matters, cost drivers, strategic value) and a
  forward reference to S19 for all KPIs. Do NOT duplicate metrics here — S19 is the
  single source of truth for KPIs.
- S8 Value Proposition Canvas: N/A — reference Platform PRD.
- S9 Competitive Analysis: N/A unless the feature competes directly with a standalone
  product category. Reference Platform PRD.
- S16 User Experience Requirements: Include only feature-specific user flows (S16.2).
  Onboarding (S16.1), accessibility (S16.3), and localization (S16.4) are platform-level
  concerns — mark N/A and reference Platform PRD.
- S17 Legal & Compliance: Include only feature-specific data handling requirements.
  Reference Platform PRD for SOC 2, GDPR, CCPA, EU AI Act.
- S18 Business Requirements: N/A — feature has no independent pricing or GTM.
  Include brief note on feature-specific cost drivers only.
Synthesis agents MUST check this field and skip platform-level content for Feature PRDs.
Do NOT hardcode specific person names (Product Owner, Engineering Lead, etc.) — use TBD.

DOCUMENTATION STALENESS WARNINGS:
[If scope discovery found any documentation that contradicts actual code, list the
specific claims and contradictions here. If none found during scope discovery, write:
"None found during scope discovery. Phase 2 agents will perform full documentation
cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags."]
Do NOT create task items that reference product capabilities marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 1 (Preparation): Update task status, confirm scope from research notes, read the template, select depth tier, create task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase and write findings files to ${TASK_DIR}research/
- Phase 3 (Completeness Verification): L4 Review/QA — spawn rf-analyst (completeness-verification) then rf-qa (research-gate) as parallel quality gate. Both write reports. QA verdict gates progression.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources (market data, competitive landscape, industry trends) and write findings files
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — agents read research files and produce PRD template sections. Then spawn rf-analyst (synthesis-review) and rf-qa (synthesis-gate) as parallel quality gate. QA can fix issues in-place.
- Phase 6 (Assembly & Validation): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final PRD, then spawn rf-qa (report-validation) for structural quality check, then spawn rf-qa-qualitative (prd-qualitative) for content/scope/logic quality check. Both QA agents have in-place fix authorization.
- Phase 7 (Present to User & Complete Task): ANTI-ORPHANING — task-completion items are WITHIN this phase, not in a separate Post-Completion section.

QA_GATE_REQUIREMENTS: PER_PHASE
  Gate 1: Research Completeness (Phase 3) — rf-analyst (completeness-verification) + rf-qa (research-gate) in parallel, max 3 fix cycles, partitioning >6 files.
  Gate 2: Synthesis Quality (Phase 5) — rf-analyst (synthesis-review) + rf-qa (synthesis-gate, fix_authorization: true) in parallel, max 2 fix cycles, partitioning >4 files.
  Gate 3: Report Validation (Phase 6) — rf-qa (report-validation, fix_authorization: true) + rf-qa-qualitative (prd-qualitative, fix_authorization: true) sequential. HALT after max fix cycles exceeded.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + PRD_SCOPE_COMPLIANCE
  TEMPLATE_COMPLIANCE: All sections from PRD template must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.
  PRD_SCOPE_COMPLIANCE: Feature PRDs must skip platform-level sections per PRD_SCOPE field.

TESTING_REQUIREMENTS: N/A — documentation-only skill, no code produced, no tests applicable.

RESEARCH NOTES FILE:
${TASK_DIR}research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, planned investigation assignments, synthesis mapping, and output paths.

SKILL CONTEXT FILE:
.claude/skills/prd/SKILL.md
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt. Read the "Synthesis Mapping Table" section for the standard synth-file-to-PRD-section mapping. Read the "Synthesis Quality Review Checklist" section for post-synthesis verification. Read the "Assembly Process" section for PRD assembly steps. Read the "Validation Checklist" section for Phase 6 validation criteria. Read the "Content Rules" section for writing standards. Read the "Tier Selection" section for depth tier line budgets and agent counts. These must be embedded in the relevant checklist items per B2 self-contained pattern.

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
- Confirm scope from research notes (product boundaries, key directories, tier selection)
- Read the PRD template at .claude/templates/documents/prd_template.md
- Select depth tier (Lightweight / Standard / Heavyweight) based on product scope and complexity
- Create the task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders (if not already created during scope discovery)

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research agent (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md
- Each item specifies: investigation topic, type (Feature Analyst / Doc Analyst / Integration Mapper / UX Investigator / Architecture Analyst), files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from SKILL.md) in each checklist item per B2
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. For example, with 6 research assignments: spawn all 6 agents in one message, mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.
- Agent count follows tier guidance: Lightweight 2-3, Standard 4-6, Heavyweight 6-10+

Phase 3 — Research Completeness Verification (ANALYST + QA GATE, PARALLEL):
- Spawn `rf-analyst` (subagent_type: "rf-analyst", analysis_type: "completeness-verification") AND `rf-qa` (subagent_type: "rf-qa", qa_phase: "research-gate") IN PARALLEL. **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked. Both agents independently read research files and apply their own checklists. The analyst writes to `${TASK_DIR}qa/analyst-completeness-report.md`. The QA agent writes to `${TASK_DIR}qa/qa-research-gate-report.md`. Embed full prompts from respective agent definitions in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE analyst instances and MULTIPLE QA instances in parallel, each with an `assigned_files` subset. The threshold is >6 for research files because research files tend to be longer and more detailed than synthesis files. Each partition instance writes to a numbered report (e.g., `${TASK_DIR}qa/analyst-completeness-report-1.md`). After all instances complete, merge their reports.
- Read ALL reports. Determine verdict from QA report(s) (PASS / FAIL).
- If PASS → proceed to Phase 4. If FAIL → fix ALL findings regardless of severity before proceeding. Spawn additional targeted research agents (one item per gap-filling agent).
- After gap-filling, spawn `rf-qa` with qa_phase: "fix-cycle". **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked. Maximum 3 fix cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present findings to user.
- Compile final gaps into ${TASK_DIR}gaps-and-questions.md
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
- Each item specifies: topic, context from codebase findings, output file path
- Web research targets should include (as applicable): competitive landscape analysis, TAM/SAM/SOM market data, industry standards and compliance requirements, technology trend reports, user research findings, pricing model analysis
- Agent count follows tier guidance: Lightweight 0-1, Standard 1-2, Heavyweight 2-4

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One checklist item PER synthesis file (from Synthesis Mapping Table in SKILL.md)
- Each item spawns an Agent subagent with the synthesis agent prompt from SKILL.md
- Each item specifies: research files to read, template sections to produce, output path
- After ALL synthesis agents complete, spawn `rf-analyst` (analysis_type: "synthesis-review") AND `rf-qa` (qa_phase: "synthesis-gate", fix_authorization: true) IN PARALLEL. The analyst writes to `${TASK_DIR}qa/analyst-synthesis-review.md`. The QA agent writes to `${TASK_DIR}qa/qa-synthesis-gate-report.md`. Embed full prompts in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >4 synthesis files exist, spawn multiple analyst and QA instances with `assigned_files` subsets. The threshold is lower than Phase 3 (>4 vs >6) because synthesis QA requires deeper per-file analysis (tracing claims back to research files, verifying cross-section consistency). Same partitioning pattern as Phase 3. Each partition instance writes to a numbered report. Orchestrator merges all partition reports after completion.
- If FAIL → re-run affected synthesis agents, then re-spawn `rf-qa` (fix-cycle). Maximum 2 fix cycles for synthesis — after 2 failed cycles, HALT and present to user.

Phase 6 — Assembly & Validation (RF-ASSEMBLER + Structural QA + Qualitative QA):
- Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") to assemble the final PRD. Hand it: the list of synth file paths in order, the PRD output path, the PRD template structure from SKILL.md, the Assembly Process steps from SKILL.md, and the Content Rules from SKILL.md. The assembler reads each synth file and writes the PRD incrementally section by section. The assembler must be a single agent (NOT parallel) because cross-section consistency requires seeing the whole document. Embed the full assembler prompt in the checklist item per B2.
- After the assembler returns, spawn `rf-qa` (qa_phase: "report-validation", fix_authorization: true). **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked. The QA agent validates the assembled PRD against the Validation Checklist from SKILL.md (structural/semantic checks: section numbers, cross-references, evidence citations, template conformance). The QA agent writes to `${TASK_DIR}qa/qa-report-validation.md`. Embed the full QA prompt in the checklist item per B2.
- Read the structural QA report. If issues remain unfixed, address them before proceeding to qualitative QA.
- After structural QA passes, spawn `rf-qa-qualitative` (subagent_type: "rf-qa-qualitative", qa_phase: "prd-qualitative", fix_authorization: true). **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked. The qualitative QA agent reads the entire PRD and verifies it makes sense from product and engineering perspectives: correct scoping (feature vs platform content), logical flow, realistic requirements, no contradictions, no red flags, appropriate audience. It applies the 23-item PRD Qualitative Review checklist from its agent definition. The agent writes to `${TASK_DIR}qa/qa-qualitative-review.md`. Embed the full qualitative QA prompt (including document type: Product PRD or Feature PRD, template path, and output path) in the checklist item per B2.
- Read the qualitative QA report. If any issues found (CRITICAL, IMPORTANT, or MINOR), verify fixes were applied correctly by re-reading the affected sections. If issues remain unfixed, address ALL of them before proceeding to Phase 7. Zero leniency — no severity level is exempt.

Phase 7 — Present to User & Complete Task:
- Present summary to user (PRD location, line count, tier classification, sections populated vs skipped, research/synth artifact locations, gaps needing manual review)
- Ask about downstream documents: "This PRD can feed directly into a Technical Design Document. Would you like me to create a TDD using the `/tdd` skill? The research files are already in place." If yes, invoke the `tdd` skill with the PRD as input.
- If the PRD was created by consolidating existing docs, present source docs to user and ask about archiving (Step 11 from SKILL.md)
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date

TASK FILE LOCATION: .dev/tasks/to-do/TASK-PRD-[YYYYMMDD]-[HHMMSS]/TASK-PRD-[YYYYMMDD]-[HHMMSS].md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, PRD template structure, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-PRD-[YYYYMMDD-HHMMSS]/TASK-PRD-[YYYYMMDD-HHMMSS].md using PART 2 structure
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

## Agent Prompt Templates

These templates are provided to the task builder (in the BUILD_REQUEST) so it can embed them in the task file's self-contained checklist items. The builder should customize each instance with the specific product area, files, and output path.

### Codebase Research Agent Prompt

```
Research this aspect of [product name] and write findings to [output-path]:

Topic: [topic description]
Investigation type: [Feature Analyst / Doc Analyst / Integration Mapper / UX Investigator / Architecture Analyst]
Files to investigate: [list of files/directories]
Product root: [primary directory]

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
1. Read the actual source files — understand what each file does, what capabilities it provides, what user value it delivers
2. Trace user flows — how does the user interact with this part of the product? What is the experience?
3. Document the product interface — what features, settings, capabilities, and user touchpoints exist?
4. Identify patterns — what product conventions, design decisions, or UX patterns are evident?
5. Check for edge cases — error states, missing features, configuration-driven behavior, accessibility gaps
6. Note dependencies — what does this product area depend on? What depends on it?
7. Flag gaps — what is missing, broken, undocumented, or unclear? What needs further investigation?
8. Note integration opportunities — where could new features or product capabilities hook in? What extension points exist? What APIs, events, or plugin systems could be leveraged?

CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Code describes CURRENT state. These frequently diverge.
When you encounter documentation that describes a product capability, feature, service, or workflow, you MUST cross-validate structural claims against actual code before reporting them as current:

1. **Features/capabilities described in docs:** Verify the feature's implementation files actually exist in the repo. Use Glob to check. If a doc says "real-time collaboration at frontend/app/collab/", verify the path exists. If it doesn't, the doc is STALE — report as historical, not current.

2. **User flows described in docs:** Trace at least the entry and exit points in actual source code. If a doc describes a user flow but the referenced components don't exist, the flow is STALE.

3. **File paths mentioned in docs:** Spot-check that referenced files exist.

4. **API endpoints described in docs:** Verify route definitions exist in the actual codebase. If a doc describes an endpoint at `/api/v1/sessions` but the route handler doesn't exist, the endpoint is STALE.

For EVERY doc-sourced claim, mark it with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** — code shows different implementation (describe what code actually shows)
- **[UNVERIFIED]** — could not find corresponding code; may be stale, planned, or in a different repo

Claims marked [UNVERIFIED] or [CODE-CONTRADICTED] MUST appear in the Gaps and Questions section.

Output Format:
- Use descriptive headers for each file or logical group
- Include actual feature capabilities, user flows, configuration options, and technology choices (not reproduced code blocks — summaries with key capabilities)
- Note any anomalies, tech debt, or surprising behavior
- End each section with a "Key Takeaways" bullet list
- End the file with:
  ## Gaps and Questions
  - [things that need further investigation or are unclear]
  - [all UNVERIFIED and CODE-CONTRADICTED claims from docs]

  ## Stale Documentation Found
  - [list any docs that describe features/capabilities that no longer exist in code]

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
Product context: [the overall product being documented]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for market data, industry reports, and competitive landscape information
2. Search for comparable products and their feature sets
3. Search for industry best practices and standards relevant to this product area
4. Search for technology trends affecting this product category
5. For each finding, document:
   - Source URL
   - Key information extracted
   - How it relates to our product's current capabilities
   - Whether it supports, extends, or contradicts what we found in code
6. Rate source reliability (official reports > industry publications > well-maintained repos > blog posts > forum answers)

Output Format:
- Use descriptive headers for each research area
- Always include source URLs
- Mark relevance: HIGH / MEDIUM / LOW for each finding
- End with:
  ## Key External Findings
  [Bullet list of the most important discoveries]

  ## Recommendations from External Research
  [How external findings should influence the PRD — market positioning, feature gaps, competitive threats]

IMPORTANT: Our codebase is the source of truth for current capabilities. External research adds market context and competitive intelligence but does not override verified product behavior. If you find a discrepancy, note it explicitly.
```

Common web research topics for PRDs:
- Competitive landscape and feature comparison matrices
- Market sizing (TAM/SAM/SOM) data and industry reports
- Industry standards and compliance requirements
- Technology trends and emerging capabilities
- User research findings and market validation
- Pricing models and monetization patterns in the space

### Synthesis Agent Prompt

```
Read the research files listed below and synthesize them into template-aligned sections for a Product Requirements Document (PRD).

Research files to read: [list of paths]
Template sections to produce: [section numbers and names]
Output path: [synth file path]
Template reference: .claude/templates/documents/prd_template.md

Rules:
0. **Read the template first.** Before synthesizing anything, read the PRD template to understand each section's expected content, format, and depth.
1. Follow the template structure exactly — use the same headers, tables, and section format
2. Every fact must come from the research files — do not invent or assume
3. Use tables over prose for multi-item data (feature lists, competitive comparisons, KPI tables, requirements)
4. Do not reproduce full source code or configuration files — summarize with key capabilities and technology choices
5. User stories must follow the standard format: "As a [persona], I want [goal] so that [benefit]"
6. Acceptance criteria must be specific and testable
7. Reference actual file paths and feature names, not hypothetical ones
8. Use RICE scoring or MoSCoW prioritization where the template requires it
9. Include competitive analysis with feature comparison matrices where applicable
10. Documentation-sourced claims require verification status. If a research file reports a finding from documentation, check whether it carries a [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED] tag. Only [CODE-VERIFIED] claims may be presented as current product capability. [CODE-CONTRADICTED] claims must be corrected. [UNVERIFIED] claims must be flagged as uncertain.
11. Never describe product capabilities from docs alone. When writing sections about current product state, ONLY use findings that trace back to actual source code reads. If the only evidence is a documentation file, flag as [UNVERIFIED — doc-only] and exclude from feature inventories.

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
Perform a completeness verification of all research files for [product name] PRD.

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
4. Apply the 8-item Research Completeness Verification checklist from your agent definition
5. Write your report to [output-path]

CHECKLIST:
1. Coverage audit — every key product area from scope covered by at least one research file
2. Evidence quality — claims cite specific file paths, feature names, capability descriptions
3. Documentation staleness — all doc-sourced claims tagged [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED]
4. Completeness — every file has Status: Complete, Summary section, Gaps section, Key Takeaways
5. Cross-reference check — cross-cutting concerns covered by multiple agents are cross-referenced
6. Contradiction detection — conflicting findings about the same feature surfaced
7. Gap compilation — all gaps unified, deduplicated, and severity-rated (Critical/Important/Minor)
8. Depth assessment — investigation depth matches the stated tier (stakeholder segments identified, user journeys documented, feature scope mapped, competitive landscape analyzed)

VERDICTS:
- PASS: All checks pass, no critical gaps
- FAIL: Critical gaps exist (list each with specific remediation action)

Use the full output format from your agent definition (tables for coverage, evidence quality, staleness, completeness).
Be adversarial — your job is to find problems, not confirm things work.
```

### Research QA Agent Prompt (rf-qa — Research Gate)

```
Perform QA verification of research completeness for [product name] PRD.

QA phase: research-gate
Research directory: [research-dir-path]
Analyst report: [analyst-report-path] (if exists, verify the analyst's work; if not, perform full verification)
Research notes file: [research-notes-path]
Tier: [Lightweight/Standard/Heavyweight]
Output path: [output-path]

You are the last line of defense before synthesis begins. Assume everything is wrong until you verify it.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

IF ANALYST REPORT EXISTS:
1. Read the analyst's completeness report
2. Verify ALL of their coverage audit claims (verify the scope items are actually covered)
3. Validate gap severity classifications (are "Critical" really critical? Are "Minor" really minor?)
4. Check their verdict against your own independent assessment
5. Apply the 10-item Research Gate checklist from your agent definition

IF NO ANALYST REPORT:
Apply the full 10-item Research Gate checklist from your agent definition independently.

11-ITEM CHECKLIST:
1. File inventory — all research files exist with Status: Complete and Summary
2. Evidence density — Verify EVERY claim in each file — verify file paths exist
3. Scope coverage — every key product area from research-notes EXISTING_FILES examined
4. Documentation cross-validation — all doc-sourced claims tagged, Verify EVERY CODE-VERIFIED claim
5. Contradiction resolution — no unresolved conflicting findings
6. Gap severity — Critical gaps block synthesis, Important reduce quality, Minor are lower priority but must still be fixed
7. Depth appropriateness — matches the tier expectation
8. User flow coverage — key user interactions documented with entry and exit points
9. Integration point coverage — external dependencies and connection points documented
10. Pattern documentation — code patterns and conventions captured that inform product design
11. Incremental writing compliance — files show iterative structure, not one-shot

VERDICTS:
- PASS: Green light for synthesis
- FAIL: ALL findings must be resolved. Only PASS or FAIL — no conditional pass.

Use the full QA report output format from your agent definition.
Zero tolerance — if you can't verify it, it fails.
```

### Synthesis QA Agent Prompt (rf-qa — Synthesis Gate)

```
Perform QA verification of synthesis files for [product name] PRD.

QA phase: synthesis-gate
Research directory: [research-dir-path]
Fix authorization: [true/false]
Output path: [output-path]

You are verifying that synthesis files are ready for assembly into the final PRD.
If fix_authorization is true, you can fix issues in-place using Edit.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

PROCESS:
1. Use Glob to find ALL synth files (synth-*.md) in the synthesis directory
2. Read EVERY synth file completely
3. Apply the 12-item Synthesis Gate checklist from your agent definition
4. For each issue found:
   a. Document the issue (what, where, severity)
   b. If fix_authorization is true: fix in-place with Edit, verify the fix
   c. If fix_authorization is false: document the required fix
5. Write your QA report to [output-path]

12-ITEM CHECKLIST:
1. Section headers match PRD template structure (.claude/templates/documents/prd_template.md)
2. Table column structures correct (competitive matrix, requirements table, KPI table, etc.)
3. No fabrication (Verify EVERY claim in each file, trace to research files)
4. Evidence citations use actual file paths and feature names
5. User stories follow As a / I want / So that format with acceptance criteria
6. Requirements use RICE or MoSCoW prioritization framework
7. Cross-section consistency (personas in S7 referenced in user stories S21.1, etc.)
8. No doc-only claims in product capability or feature inventory sections
9. Stale docs surfaced in Open Questions (S13) or Assumptions & Constraints (S10)
10. Content rules compliance (tables over prose, no code reproductions)
11. All expected sections have content (no placeholders)
12. No hallucinated file paths (verify parent directories exist)

VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found (list with specific fixes, note which were fixed in-place)
```

### Report Validation QA Agent Prompt (rf-qa — Report Validation)

```
Perform final QA validation of the assembled PRD for [product name].

QA phase: report-validation
Report path: [report-path]
Research directory: [research-dir-path]
Template path: .claude/templates/documents/prd_template.md
Output path: [output-path]
Fix authorization: true (always authorized for report validation)

This is the final quality check before presenting to the user. You can and should fix issues in-place.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

PROCESS:
1. Read the ENTIRE PRD
2. Apply the 18-item Validation Checklist + 4 Content Quality Checks
3. For each issue: document it, fix it in-place with Edit, verify the fix
4. Write your QA report to [output-path]

18-ITEM VALIDATION CHECKLIST:
1. All template sections present (or explicitly marked as N/A with rationale)
2. Frontmatter has all required fields from the template
3. Total line count within tier budget (Lightweight: 400-800, Standard: 800-1500, Heavyweight: 1500-2500)
4. HOW TO USE blockquote present
5. Document Information table has all 9 rows
6. Numbered Table of Contents present
7. User stories follow As a / I want / So that format
8. Acceptance criteria are specific and testable for each story
9. Feature prioritization uses RICE or MoSCoW framework
10. Competitive analysis includes feature comparison matrix
11. KPI tables have measurement methods defined
12. No full source code reproductions
13. All file paths reference actual files that exist
14. Document History table present
15. Tables use correct column structure from template
16. No doc-sourced claims presented as verified without code cross-validation tags
17. Product capability and feature claims cite actual file paths (not just prose assertions)
18. Web research findings include source URLs for every external claim

CONTENT QUALITY CHECKS:
19. Table of Contents accuracy
20. Internal consistency (no contradictions between sections)
21. Readability (scannable — tables, headers, bullets)
22. Actionability (product team could begin planning from this PRD alone)

Fix every issue you find. Report honestly.
```

### Assembly Agent Prompt (rf-assembler — PRD Assembly)

```
Assemble the final Product Requirements Document (PRD) for [product name] from synthesis files.

Component files (in order):
[ordered list of synth file paths]

Output path: [PRD-output-path]
Research directory: [research-dir-path]
Template reference: .claude/templates/documents/prd_template.md

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create the output file immediately with the PRD frontmatter:
   Fill in all frontmatter fields from the template. Set status: "🟡 Draft",
   populate created_date, depends_on, tags, etc.

2. As you assemble each section, IMMEDIATELY write it to the output file using Edit.
   Do NOT accumulate the entire PRD in context and attempt a single write.

3. After each Edit, the file grows. This is correct behavior. Never rewrite from scratch.

Assembly procedure:
1. Write the frontmatter and HOW TO USE blockquote
2. Write the Document Information table (Product Name, Product Owner, Engineering Lead, Design Lead, Stakeholders, Status, Target Release, Last Updated, Review Cadence)
3. Assemble sections in template order — read each synth file and write its content into the correct position. Sections not covered by synth files get written directly during assembly from patterns observed in the synth files.
4. Write the Table of Contents — generate from actual section headers after all sections are placed
5. Add Appendices — Glossary, Acronyms, Technical Architecture Diagrams, User Research Data, Financial Projections as applicable
6. Add Document History — initial entry
7. Add Document Provenance — if the PRD was created by consolidating existing docs, document the source materials and creation method. Zero content loss: every piece of metadata from source documents must appear somewhere in the normalized PRD.

Assembly rules:
1. Write the header first, then sections in template order, then ToC
2. Write each section to disk immediately after composing it — do NOT one-shot
3. Cross-check internal consistency:
   - Personas in Section 7 appear in user stories in Section 21.1
   - Requirements in Section 21.2 have acceptance criteria
   - Competitive features in Section 9 map to product requirements in Section 21.2
   - Open Questions in Section 13 aren't answered elsewhere in the document
   - Success Metrics in Section 19 have measurement methods
   - Risk mitigations in Section 20 address identified risks
4. Flag any contradictions between sections using: [CONTRADICTION: Section X claims A, Section Y claims B]
5. Ensure no placeholder text remains (search for [, TODO, TBD, PLACEHOLDER)
6. Tables over prose whenever presenting multi-item data
7. No full source code reproductions — summarize with key capabilities and technology choices

Content rules (non-negotiable):
- Tables over prose whenever presenting multi-item data
- Product vision: concise statement with 1-2 paragraph expansion
- User personas: structured attribute tables with representative quotes
- User stories: As a / I want / So that format with acceptance criteria
- Competitive analysis: feature comparison matrices with status icons
- Requirements: prioritized tables with RICE/MoSCoW
- KPIs: table with Category / KPI / Target / Measurement Method
- Risk analysis: probability/impact matrices with mitigations

CRITICAL: You are assembling existing content, not creating new findings. Preserve fidelity
to the synthesis files. Add only minimal transitional text where needed for coherence.
Do NOT attempt full content validation — that is the QA agent's job. Focus on assembly
integrity: correct ordering, internal consistency, no placeholders, all components included.

Consolidation protocol (when consolidating existing docs into this PRD):
1. Read each source document listed in the task's "Source Files to Consolidate" section
2. Map each source document's content to the corresponding template section(s)
3. Where source docs overlap, merge by keeping the most specific/recent information and noting conflicts
4. Add an Appendix: Document Provenance subsection listing each source doc with its path, original purpose, and which sections it contributed to
5. Zero content loss — every metadata piece and unique finding from source docs must appear in the final output or be explicitly noted as superseded
6. After assembly, the source docs should be candidates for archival (the PRD replaces them)
```

---

## Output Structure

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

The final PRD follows the template at `.claude/templates/documents/prd_template.md`. The synthesis agents produce sections that are assembled into this format.

```markdown
---
[frontmatter from template]
---

# [Product Name] - Product Requirements Document (PRD)

> HOW TO USE THIS DOCUMENT: [preamble blockquote]

---

## Document Information
Project specifics table: Product Name, Product Owner, Engineering Lead, Design Lead, Stakeholders, Status, Target Release, Last Updated, Review Cadence.

## Table of Contents
[Generated from section headers]

---

## 1. Executive Summary
2-3 paragraph summary with Key Success Metrics.

## 2. Problem Statement
Core problem, why existing solutions fall short, market opportunity.

## 3. Background & Strategic Fit
Why now, company objective alignment, strategic bets.

## 4. Product Vision
One-sentence vision statement with expansion.

## 5. Business Context
Market opportunity (TAM/SAM/SOM), business objectives, KPIs.

## 6. Jobs To Be Done (JTBD)
Primary jobs in When/I want/So that format, related jobs table.

## 7. User Personas
Primary, secondary, tertiary personas with attribute tables; anti-personas.

## 8. Value Proposition Canvas
Customer profile, value map (pain relievers + gain creators), fit assessment.

## 9. Competitive Analysis
Competitive landscape table, feature comparison matrix, positioning statement, response plan.

## 10. Assumptions & Constraints
Technical, business, and user assumptions with risk-if-wrong; constraints table.

## 11. Dependencies
External, internal, and cross-team dependency tables.

## 12. Scope Definition
In scope, out of scope, permanently out of scope.

## 13. Open Questions
Question tracking table with owner, status, resolution.

## 14. Technical Requirements
Architecture, performance, security, scalability, data & analytics requirements.

## 15. Technology Stack
Backend, frontend, infrastructure technology tables.

## 16. User Experience Requirements
Onboarding metrics, core user flows, accessibility, localization.

## 17. Legal & Compliance Requirements
Regulatory compliance, data privacy, terms & policies.

## 18. Business Requirements
Monetization strategy, pricing tiers, go-to-market, support requirements.

## 19. Success Metrics & Measurement
Product, business, and technical metrics with targets and measurement frequency.

## 20. Risk Analysis
Technical, business, and operational risk matrices with mitigations.

## 21. Implementation Plan
Consolidated delivery plan: 21.1 Epics, Features & Stories (epic summary, user stories with acceptance criteria), 21.2 Product Requirements (core features, RICE matrix), 21.3 Implementation Phasing, 21.4 Release Criteria & DoD, 21.5 Timeline & Milestones.

## 22. Customer Journey Map
Journey stages table, moments of truth.

## 23. Error Handling & Edge Cases
Error categories, edge case scenarios, graceful degradation plan.

## 24. User Interaction & Design
Wireframes/mockups table, design system checklist, prototype links.

## 25. API Contract Examples
Key endpoint request/response examples.

## 26. Contributors & Collaboration
Contributor table, how to contribute guidelines.

## 27. Related Resources
Customer research, technical docs, design assets, business documents.

## 28. Maintenance & Ownership
Document ownership, review cadence, update process.

## Appendices
Glossary, Acronyms, Technical Architecture Diagrams, User Research Data, Financial Projections.

## Document Approval
Approval signature table.
```

---

## Synthesis Mapping Table (Reference)

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

This is the standard mapping of synthesis files to PRD template sections. Adjust based on product complexity — small features can combine more sections per synth file, large platform PRDs may need additional synth files for additional product areas.

| Synth File | Template Sections | Source Research Files |
|------------|-------------------|----------------------|
| `synth-01-exec-problem-vision.md` | 1. Executive Summary, 2. Problem Statement, 3. Background & Strategic Fit, 4. Product Vision | product capabilities, web research (market context), existing docs |
| `synth-02-business-market.md` | 5. Business Context, 6. JTBD, 7. User Personas, 8. Value Proposition Canvas | user flows, web research (market context), product capabilities |
| `synth-03-competitive-scope.md` | 9. Competitive Analysis, 10. Assumptions & Constraints, 11. Dependencies, 12. Scope Definition | web research (competitive landscape), technical stack, integration points |
| `synth-04-stories-requirements.md` | 13. Open Questions, 21.1 Epics Features & Stories, 21.2 Product Requirements | per-area research files, user flows, gaps log |
| `synth-05-technical-stack.md` | 14. Technical Requirements, 15. Technology Stack | technical stack, architecture research, web research (technology trends) |
| `synth-06-ux-legal-business.md` | 16. UX Requirements, 17. Legal & Compliance, 18. Business Requirements | user flows, product capabilities, web research (compliance, market) |
| `synth-07-metrics-risk-impl.md` | 19. Success Metrics, 20. Risk Analysis, 21.3 Implementation Phasing, 21.4 Release Criteria & DoD, 21.5 Timeline & Milestones | all research files, web research, technical stack |
| `synth-08-journey-design-api.md` | 22. Customer Journey, 23. Error Handling, 24. User Interaction, 25. API Contracts | user flows, per-area research, technical stack |
| `synth-09-resources-maintenance.md` | 26. Contributors, 27. Related Resources, 28. Maintenance & Ownership | existing docs, all research files, gaps log |

---

## Synthesis Quality Review Checklist

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

**This checklist is enforced by the rf-analyst and rf-qa agents** (see Phase 5 in the task phases). The rf-analyst applies these 9 criteria as its Synthesis Quality Review analysis type, and the rf-qa agent independently verifies the analyst's findings with its expanded 12-item Synthesis Gate checklist. The QA agent can fix issues in-place when authorized.

The 9 criteria (used by rf-analyst):

1. Template section headers match exactly (per `.claude/templates/documents/prd_template.md`)
2. Tables use the correct column structure from the template (competitive matrix, requirements table, KPI table, scope table, risk matrix, etc.)
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and feature names (not vague descriptions)
5. User stories follow the As a / I want / So that format with testable acceptance criteria
6. Requirements use RICE or MoSCoW prioritization framework
7. Cross-section consistency (personas referenced in user stories, requirements have acceptance criteria, risks have mitigations)
8. **No doc-only claims in product capability or feature sections** — every feature described must be backed by code evidence. If a synth file describes a capability and the only evidence is a documentation file (no source code path), reject that claim and flag it as `[UNVERIFIED — doc-only]`
9. **Stale documentation discrepancies are surfaced** — any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings should appear in Open Questions (Section 13) or Assumptions & Constraints (Section 10), not silently omitted

The rf-qa agent's Synthesis Gate adds 3 additional checks (10-12): content rules compliance, section completeness (no placeholders), and hallucinated file path detection. If synthesis QA fails, the QA agent fixes issues in-place (when authorized) and issues remaining unfixed trigger re-synthesis of the affected files.

---

## Assembly Process

### Step 8: Assemble the PRD

Read all synth files in order and assemble the final document:

1. **Start with the template frontmatter** — fill in all fields from the template. Set `status: "🟡 Draft"`, populate `created_date`, `depends_on`, `tags`, etc.

2. **Write the HOW TO USE blockquote** — follow the template's preamble format.

3. **Write the Document Information table** — Product Name, Product Owner, Engineering Lead, Design Lead, Stakeholders, Status, Target Release, Last Updated, Review Cadence.

4. **Assemble sections in template order** — paste each synth file's content into the correct position. Sections that weren't assigned a synth file get written directly during assembly from patterns observed in the synth files.

5. **Write the Table of Contents** — generate from actual section headers.

6. **Add Appendices** — Glossary, Acronyms, Technical Architecture Diagrams, User Research Data, Financial Projections as applicable.

7. **Add Document History** — initial entry.

8. **Add Document Provenance** — if the PRD was created by consolidating existing docs, add an `Appendix: Document Provenance` subsection documenting the source materials and creation method. Zero content loss: every piece of metadata from source documents must appear somewhere in the normalized PRD.

### Step 9: Validate the Output

Before presenting to the user, validate:

- [ ] All template sections present (or explicitly marked as N/A with rationale)
- [ ] Frontmatter has all required fields from the template
- [ ] Total line count within tier budget (Lightweight: 400-800, Standard: 800-1500, Heavyweight: 1500-2500)
- [ ] HOW TO USE blockquote present
- [ ] Document Information table has all 9 rows
- [ ] Numbered Table of Contents present
- [ ] User stories follow As a / I want / So that format
- [ ] Acceptance criteria are specific and testable for each story
- [ ] Feature prioritization uses RICE or MoSCoW framework
- [ ] Competitive analysis includes feature comparison matrix
- [ ] KPI tables have measurement methods defined
- [ ] No full source code reproductions
- [ ] All file paths reference actual files that exist
- [ ] Document History table present
- [ ] Tables use correct column structure from template
- [ ] No doc-sourced claims presented as verified without code cross-validation tags
- [ ] Web research findings include source URLs for every external claim
- [ ] Gaps and questions file exists at `${TASK_DIR}gaps-and-questions.md`

### Step 10: Present to User

Notify the user:
- Where the final document was written
- Line count and tier classification
- Number of sections populated vs skipped
- Where the research/synth artifacts live (for future reference)
- Any gaps or areas that need manual review

### Step 11: Clean Up Consolidation Sources

If the PRD was created by consolidating existing docs:
- Do NOT delete the source docs automatically
- Present the source docs to the user and confirm they can be archived
- Archive approved sources to `docs/archive/[appropriate-subdir]/`
- Update any references to the archived files in other documents
- Check off items in the stub's consolidation checklist if one exists

---

## Validation Checklist

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

Before presenting the PRD to the user, validate against this checklist (this is encoded in the task file's Assembly phase):

**Structural completeness:**

- [ ] All 32 numbered template sections present (or explicitly marked as N/A with rationale)
- [ ] Frontmatter has all required fields from the template (id, title, status, created_date, tags, depends_on)
- [ ] HOW TO USE blockquote present with document purpose and usage guidance
- [ ] Document Information table has all 9 rows (Product Name, Product Owner, Engineering Lead, Design Lead, Stakeholders, Status, Target Release, Last Updated, Review Cadence)
- [ ] Numbered Table of Contents present and matches actual section headers — no orphaned or missing entries

**Content quality:**

- [ ] Stakeholder segments clearly defined with structured persona attribute tables (Section 7)
- [ ] User journeys documented with As a / I want / So that format and testable acceptance criteria (Section 21.1)
- [ ] Feature scope bounded — In Scope, Out of Scope, and Permanently Out of Scope all populated with rationale (Section 12)
- [ ] Acceptance criteria are measurable and testable — no vague criteria like "works well" or "is fast"
- [ ] Competitive landscape analyzed with feature comparison matrix using status icons (Section 9)
- [ ] Success metrics quantified with specific targets and measurement methods (Section 19)
- [ ] Requirements use RICE or MoSCoW prioritization framework with scores/categories (Section 21.2)

**Evidence integrity:**

- [ ] No fabricated market claims — all TAM/SAM/SOM figures, market data, and competitive claims cite sources
- [ ] All feature descriptions verified against codebase — no doc-only claims without `[UNVERIFIED]` tags
- [ ] Web research findings include source URLs for every external claim
- [ ] All `[CODE-CONTRADICTED]` and `[STALE DOC]` findings surfaced in Open Questions (Section 13) or Assumptions & Constraints (Section 10)
- [ ] Gaps and questions file exists at `${TASK_DIR}gaps-and-questions.md`

**Format compliance:**

- [ ] Total line count within tier budget (Lightweight: 400-800, Standard: 800-1500, Heavyweight: 1500-2500)
- [ ] Tables use correct column structure from the template (KPI table, scope table, risk matrix, competitive matrix)
- [ ] No full source code reproductions in any section
- [ ] Document History table present with initial entry
- [ ] Document Provenance appendix present if consolidating existing docs

---

## Content Rules (From Template — Non-Negotiable)

These rules come from the template's structure and conventions. Every PRD must follow them.

| Rule | Do | Don't |
|------|-----|-------|
| **Product vision** | Concise vision statement with 1-2 paragraph expansion | Multi-page vision essays or vague aspirations |
| **User personas** | Structured attribute tables with representative quotes | Lengthy narrative character descriptions |
| **User stories** | Standard format: As a / I want / So that with acceptance criteria | Vague feature descriptions without user context |
| **Competitive analysis** | Feature comparison matrices with status icons (✅/⚠️/❌) | Prose-based competitor descriptions |
| **Requirements** | Prioritized tables with RICE scores or MoSCoW categories | Unprioritized feature lists or wish lists |
| **Market data** | TAM/SAM/SOM tables with sources and evidence | Unsourced market claims or guesses |
| **KPIs** | Table: Category / KPI / Target / Measurement Method | Vague success metrics without measurement methods |
| **Scope** | In/Out/Deferred tables with rationale for each decision | Unbounded scope descriptions or missing exclusions |
| **Risk analysis** | Probability/Impact matrices with mitigations and contingencies | Lists of concerns without assessment or mitigation |
| **Timeline** | ASCII timeline diagrams with milestones and phase breakdowns | Vague "Q3" or "soon" dates without structure |

---

## Critical Rules (Non-Negotiable)

These are SKILL-SPECIFIC content rules that apply across ALL phases. Violations compromise document quality.

Three execution-discipline rules (task-file-source-of-truth, maximize-parallelism, use-dedicated-tools) are enforced by the `/task` skill and do not appear here. The incremental-writing mandate is retained as Rule 9 below because it is a content-quality requirement specific to this skill's multi-agent research pipeline, not just an execution mechanism.

1. **Codebase is source of truth.** For claims about what the product currently does, code overrides documentation. Web research supplements with market context but never overrides verified code findings. Internal documentation is treated with the same skepticism as external sources unless code-verified.

2. **Evidence-based claims only.** Every finding must cite actual file paths, feature names, capability descriptions. No assumptions, no inferences, no guessing. If you can't verify it, mark it as "Unverified — needs confirmation."

3. **Gap-driven web research.** Do not web search everything up front. First investigate the codebase thoroughly (Phase 2), identify specific gaps, then target web research (Phase 4) at those gaps. This keeps web research focused and efficient.

4. **Documentation is not verification.** Internal documentation (design docs, architecture docs, READMEs in `docs/`) describes intent, history, or planned state — NOT necessarily current state. A doc saying "Feature X exists" does not prove Feature X exists. Only reading actual source code proves it. Doc Analyst agents MUST cross-validate every product claim against actual code using the Documentation Staleness Protocol.

5. **Preserve research artifacts.** Research, web research, and synthesis files persist after the document is written. They serve as the evidence trail for all claims and enable future re-investigation without starting from scratch. Do NOT delete research files, synthesis files, or the gaps log after assembly.

6. **Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. The synthesis phase relies on these connections to build a coherent picture across product areas.

7. **Report all uncertainty.** If something is unclear, ambiguous, or requires a judgment call, flag it explicitly in Open Questions. Do not silently pick one interpretation and present it as fact.

8. **Quality gates are mandatory.** The `rf-analyst` and `rf-qa` agents MUST be spawned at all 3 gate points: after research (completeness verification + research gate), after synthesis (synthesis review + synthesis gate), and after assembly (report validation). Skipping quality gates is never permitted.

9. **No one-shotting documents.** Agents must write incrementally as they discover information. The assembler must write the final PRD section by section. This is non-negotiable — one-shotting hits token limits and loses all accumulated work.

10. **Partitioning thresholds.** When >6 research files exist (Phase 3) or >4 synthesis files exist (Phase 5), spawn MULTIPLE analyst and QA instances in parallel, each with an `assigned_files` subset. This prevents context rot when any single agent would need to hold too many files in context.

11. **Default to Heavyweight.** Unless the product scope is clearly answerable with a single feature and <5 user stories, use the Heavyweight tier. When in doubt, go deeper. PRDs that are too thorough are easy to trim; PRDs that are too shallow require full re-investigation.

12. **Docs-vs-code has the same trust hierarchy as web-vs-code.** Critical Rule 1 establishes that web research never overrides code. The same applies to internal documentation: if a doc describes a product capability that contradicts what the code shows, **the code is correct and the doc is stale**. Treat internal docs with the same skepticism as external blog posts unless code-verified.

13. **PRD must be actionable.** The final PRD should contain enough detail that a product team could begin planning from it. User stories must be specific with testable acceptance criteria. Technical requirements (Section 14) must cite actual file paths and architectural patterns — not vague statements like "the system should be scalable." Requirements must be prioritized. This is not a placeholder document.

14. **Anti-orphaning rule.** Task-completion items (status update, Task Log entry, frontmatter update) MUST be checklist items within the final phase of the task file, not in a separate Post-Completion section. This ensures they are executed by the F1 loop and not orphaned.

15. **No fabricating product capabilities.** Research agents document what EXISTS. Never invent features, user flows, or capabilities that aren't verified in code. Every product claim must be traceable to actual source code or verified documentation.

16. **No modifying source code.** Research agents READ code, they do not modify it. This skill produces documents, not code changes. Any code changes needed should be logged as follow-up items, not executed during PRD creation.

17. **QA gates are checklist items, not prose.** Every QA gate specified in QA_GATE_REQUIREMENTS must appear in the generated task file as a `- [ ]` checklist item following B2 self-contained pattern. QA gates described only in prose or comments are invisible to the F1 executor and will be skipped.

---

## Research Quality Signals

### Strong Investigation Signals
- Findings cite specific file paths and capability descriptions
- User flows are traced end-to-end, not just entry points
- Integration points are mapped with actual technology names and versions
- Existing patterns identified that inform product design decisions
- Gaps are specific and actionable ("feature X doesn't handle case Y")
- Doc-sourced claims carry verification tags
- rf-analyst reports PASS with no critical gaps
- rf-qa research gate verdict is PASS

### Weak Investigation Signals (Redo)
- Vague descriptions without file paths ("the system has a plugin architecture")
- Assumptions stated as facts ("this probably works by...")
- Missing gap analysis (everything seems fine — unlikely for non-trivial products)
- No cross-references between research files
- Doc-sourced claims reported without code verification tags — if a research file describes capabilities and the evidence trail only points to documentation files (no source code paths), the investigation is incomplete and must be redone with code cross-validation
- rf-analyst or rf-qa reports show FAIL with critical gaps
- User stories missing acceptance criteria or feature capabilities undocumented despite being in scope

### When to Spawn Additional Agents
- A research agent flags a gap that's critical to the product analysis
- Two agents' findings contradict each other — need a tie-breaker investigation
- The scope turns out larger than initially estimated
- A new product area is discovered during investigation that wasn't in the original plan
- Web research reveals competitive features that need codebase verification
- rf-analyst or rf-qa identify coverage gaps requiring targeted investigation

---

## Artifact Locations

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/TASK-PRD-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Gaps log | `${TASK_DIR}gaps-and-questions.md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Analyst reports | `${TASK_DIR}qa/analyst-completeness-report.md`, `${TASK_DIR}qa/analyst-synthesis-review.md` |
| QA reports (research gate) | `${TASK_DIR}qa/qa-research-gate-report.md` |
| QA reports (synthesis gate) | `${TASK_DIR}qa/qa-synthesis-gate-report.md` |
| QA reports (report validation) | `${TASK_DIR}qa/qa-report-validation.md` |
| QA reports (qualitative review) | `${TASK_DIR}qa/qa-qualitative-review.md` |
| Final PRD | `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md` |
| Template schema | `.claude/templates/documents/prd_template.md` |

Research and synthesis files persist in the task folder — they serve as the evidence trail for claims in the PRD and can be re-used when the document needs updating.

---

## Session Management

Session management is provided by the `/task` skill. When resuming a session:

1. Check for an existing task folder matching `TASK-PRD-*/` in `.dev/tasks/to-do/`
2. If found, invoke `/task` with the task file path — it will resume from the first unchecked item
3. Check for existing research files in `${TASK_DIR}research/` for context
4. Read any analyst/QA gate reports to understand which gates have already passed

If no task file exists but research files are present, the user likely needs to restart from Stage A (scope discovery).

---

## Updating an Existing PRD

When the user wants to update (not create) an existing PRD:

1. Read the current document to understand what's already covered
2. Research only the changed/new areas (don't re-research everything)
3. Write new research files for the changes: `${TASK_DIR}research/update-[date]-[topic].md`
4. Edit the relevant sections of the PRD in place
5. Update the Document Information table with the new Last Updated date
6. Update Document History with what changed

