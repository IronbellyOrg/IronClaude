---
name: tech-reference
description: "Create or populate a Technical Reference document for a built feature. Use this skill when the user wants to create a tech reference, document a feature's architecture and implementation, populate an existing tech reference stub, or write a comprehensive technical reference following the project template. Trigger on phrases like 'create a tech reference for...', 'document this feature', 'write a technical reference', 'populate this tech reference', 'tech ref for the agent system', or when the user references a *-technical-reference.md file that needs content. Also trigger when the user says 'research this feature' in the context of documentation."
---

# Technical Reference Creator

Creates comprehensive Technical Reference documents for built features by researching the actual codebase, synthesizing findings into template-aligned sections, and assembling the final document. This skill uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts.

**How it works:** The skill performs initial scope discovery (Stage A), then invokes the `/task-builder` skill to create an MDTM task file encoding all investigation and documentation phases. Stage B then delegates execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA, and session management.

The output always follows the project template at `.claude/templates/documents/technical_reference_template.md`. The template is the schema — every tech reference must conform to it.

## Why This Process Works

Technical references go stale when written from memory or existing docs. This skill forces every claim through codebase verification — parallel agents read actual source files, trace actual imports, and document actual behavior with file paths and line numbers.

The MDTM task file provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off.

The multi-phase structure (scope discovery → deep investigation → **analyst verification** → web research → synthesis → **synthesis QA** → assembly → **report validation**) prevents four common failure modes:
- **Context rot** — By isolating each investigation topic in its own subagent with its own output file, no single agent needs to hold the entire investigation in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning many parallel agents (each focused on one slice), the investigation goes deep on every aspect simultaneously rather than skimming across everything sequentially.
- **Hallucinated content** — By separating research (what exists) from synthesis (what it means) from assembly (the final document), each phase can be verified independently. Synthesis agents only work from verified research files, not from memory or inference.
- **Uncaught quality drift** — Dedicated `rf-analyst`, `rf-qa`, and `rf-qa-qualitative` agents provide independent verification at three critical gates: after research (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative for completeness and depth verification), after synthesis (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative for synthesis review and coherence), and after assembly (lens-based multi-agent QA with 6-12+ agents each focused on a single quality dimension — template conformance, internal consistency, evidence quality, completeness, actionability, numbers/metrics, cross-reference chains, and domain accuracy, plus tech-reference domain-specific lenses for code-example accuracy, API-signature correctness, and configuration-value verification). The QA agent assumes everything is wrong until independently verified — zero-trust verification prevents rubber-stamping.
- **Source fidelity gaps** — A dedicated source-document fidelity gate after assembly verifies that the generated tech reference faithfully represents the original source code it documents. Fidelity agents read BOTH the source code files AND the assembled document, checking semantic coverage, detail preservation, and phantom coverage. Without this gate, a document can be internally consistent but semantically divorced from the code it claims to describe.

The research artifacts persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and feed directly into downstream documentation updates.

---

## Input

The skill needs four pieces of information to produce a thorough technical reference. The first is mandatory; the rest are optional but dramatically improve output quality.

1. **WHAT feature to document** (mandatory) — The feature, subsystem, or system to create a technical reference for. This can come from:
   - A directory path (e.g., `frontend/app/wizard/`, `backend/app/services/`)
   - An existing tech reference stub with a "Source Files to Consolidate" section
   - Both — the stub provides hints, the paths provide scope

2. **WHY / what's the context** (strongly recommended) — What prompted this documentation effort and what you want the reference to accomplish. This shapes whether the document emphasizes architecture understanding, onboarding guidance, consolidation of existing docs, or operational reference. Examples: "we built a new wizard system and need to document it", "consolidate these three architecture docs into one reference", "new team members need onboarding docs for the agent system".

3. **WHERE to look** (optional, saves significant time) — Specific directories, files, or subsystems to focus investigation on. Prevents research agents from spending time on irrelevant areas of the codebase.

4. **OUTPUT location** (optional but helpful) — Where the final tech reference should be written. If an existing stub exists, provide its path. If creating from scratch, follow the project convention: `docs/[domain]/FEATURE-NAME-TECHNICAL-REFERENCE.md` (ALL-CAPS-KEBAB-CASE). If not provided, the skill infers the path from the feature name and domain.

### Effective Prompt Examples

**Strong — all four pieces present:**
> Create a tech reference for the wizard system. Root: `frontend/app/wizard/`. We built a 10-stage game configuration wizard and need comprehensive documentation for onboarding and maintenance. There's an existing stub at `docs/frontend/wizard-technical-reference.md` to populate.

**Strong — clear feature + scope + output type:**
> Document the agent LLM system. Scope: `backend/app/agents/`, `backend/app/services/`. I need a Standard-tier reference covering agent orchestration, tool registration, and memory integration.

**Strong — consolidation focus:**
> Consolidate the three existing architecture docs into a single tech reference for the platform architecture. Source docs are listed in the stub at `docs/architecture/platform-architecture-technical-reference.md`.

**Weak — topic only (will work but produces broader, less focused results):**
> Document something.

**Weak — no feature specified (skill cannot proceed):**
> Tech ref.

### What to Do If the Prompt Is Incomplete

If the user provides only a topic name or a vague request, **do NOT proceed immediately**. Ask the user to clarify using this template:

> I can create a technical reference for you. To make the document focused and comprehensive, can you help me with:
>
> 1. **What feature should I document?** (e.g., "the wizard system", "the agent orchestration layer", "pixel streaming integration")
> 2. **What's the context?** (e.g., "we just built this and need docs", "consolidate existing architecture docs", "onboarding reference for new engineers")
> 3. **Any specific directories or files I should focus on?** (e.g., `frontend/app/wizard/`, `backend/app/agents/`)
> 4. **Is there an existing stub or target location?** (e.g., `docs/frontend/wizard-technical-reference.md`)

Proceed once you have at least #1 answered clearly. Items #2-4 improve quality but aren't blockers.

---

## Tier Selection

Match the tier to feature scope. **Default to Standard** unless the feature is clearly documentable with a quick scan of <5 files.

| Tier | When | Codebase Agents | Web Agents | Target Lines |
|------|------|-----------------|------------|-------------|
| **Lightweight** | Small features, single subsystem, <5 relevant files | 2–3 | 0–1 | 400–600 |
| **Standard** | Most features (5-20 files), multiple subsystems, moderate complexity | 4–6 | 1–2 | 800–1,200 |
| **Heavyweight** | Cross-cutting systems, 20+ files, multiple integration points | 6–10+ | 2–4 | 1,200–1,800 |

**Tier selection rules:**
- If in doubt, pick Standard
- If the user says "thorough", "comprehensive", or "detailed" — always Heavyweight
- Only use Lightweight for genuinely small features (<5 files, single concern)
- If the scope spans multiple subsystems, architectural layers, or integration boundaries — always Heavyweight

**QA Intensity Mapping (per Template 02 I22):**

| Tier | Default qa_intensity | Override allowed? |
|------|---------------------|-------------------|
| Lightweight | lite | Yes |
| Standard | standard | Yes |
| Heavyweight | full | Yes |

If the user says "quick", "fast", "light QA", or "basic" → lite.
If the user says "thorough QA", "full QA", "careful" → full.
Otherwise → default per tier.

---

## Output Locations

All persistent artifacts go into the task folder at `.dev/tasks/to-do/TASK-TECHREF-<subject>-YYYYMMDD-HHMMSS/`. The feature slug is derived from the feature name (e.g., `wizard`, `agent-llm-system`, `pixel-streaming`).

**Variable reference block:**
```
TASK_ID:     TASK-TECHREF-<subject>-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/
SYNTHESIS:   ${TASK_DIR}synthesis/
QA:          ${TASK_DIR}qa/
REVIEWS:     ${TASK_DIR}reviews/
```

**Subject derivation:** `<subject>` is derived at task-folder-creation time from the subject of the reference and normalized to kebab-case (lowercase, hyphen-separated, 1-3 words, ~30 char soft cap). If no clean subject can be derived, fall back to the literal word `general`. Example TASK_ID: `TASK-TECHREF-docker-compose-20260408-140000`.

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}${TASK_ID}.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Gap/question log (interim) | `${TASK_DIR}gaps-and-questions.md` |
| Analyst reports (research gate) | `${TASK_DIR}qa/analyst-completeness-report.md`, `analyst-crossval-report.md` |
| QA reports (research gate) | `${TASK_DIR}qa/qa-research-evidence-report.md`, `qa-research-gaps-report.md` |
| QA-qualitative reports (research gate) | `${TASK_DIR}qa/qa-research-depth-report.md` |
| Research gate consolidated findings | `${TASK_DIR}qa/qa-research-consolidated-findings.md` |
| Analyst reports (synthesis gate) | `${TASK_DIR}qa/analyst-synthesis-accuracy-report.md`, `analyst-synthesis-tracing-report.md` |
| QA reports (synthesis gate) | `${TASK_DIR}qa/qa-synthesis-structure-report.md`, `qa-synthesis-quality-report.md` |
| QA-qualitative reports (synthesis gate) | `${TASK_DIR}qa/qa-synthesis-coherence-report.md` |
| Synthesis gate consolidated findings | `${TASK_DIR}qa/qa-synthesis-consolidated-findings.md` |
| Lens QA reports (Phase 6, per-lens) | `${TASK_DIR}qa/qa-lens-[lens-name]-report.md` |
| Lens QA-qualitative reports (Phase 6) | `${TASK_DIR}qa/qa-qual-[lens-name]-report.md` |
| Lens QA consolidated findings | `${TASK_DIR}qa/qa-consolidated-findings.md` |
| Source fidelity reports | `${TASK_DIR}qa/qa-source-fidelity-[N]-report.md` |
| Final tech reference | `docs/[domain]/FEATURE-NAME-TECHNICAL-REFERENCE.md` |
| Template schema | `.claude/templates/documents/technical_reference_template.md` |

**File numbering convention:** All research, web, and synthesis files use zero-padded sequential numbers: `01-`, `02-`, `03-`, etc. This ensures correct ordering when listing files.

Check for existing task folders matching `TASK-TECHREF-*` in `.dev/tasks/to-do/` before creating new ones — if prior research exists on the same feature, read it first and build on it.

---

## Execution Overview

The skill operates in two stages:

**Stage A — Scope Discovery & Task File Creation (before the task file exists):**
1. Check for an existing task file or research directory (A.1)
2. Parse the user's request and triage into Scenario A vs B (A.2)
3. Perform scope discovery — map feature files, plan assignments (A.3)
4. Write scope discovery results to a structured research notes file (A.4)
5. Review research sufficiency — mandatory gate (A.5)
6. Triage template selection (A.6)
7. Write BUILD-REQUEST.md and invoke the `/task-builder` skill to create the MDTM task file (A.7) — task-builder handles structural and qualitative validation internally

**Stage B — Task File Execution (after the task file exists):**
8. Delegate execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA, and session management
9. Each checklist item is a self-contained prompt — no prior context needed

Phase names within the task file:
- **Phase 1: Preparation** — Scope confirmation, template read, tier selection
- **Phase 2: Deep Investigation** — Parallel subagent investigation of feature code
- **Phase 3: Completeness Verification** — rf-analyst completeness verification + rf-qa research gate + rf-qa-qualitative research-depth (parallel), consolidated verdict gates progression, gap-fill cycles if needed (max 3)
- **Phase 4: Web Research** — Optional external research for framework/API gaps
- **Phase 5: Synthesis + Analyst + QA Synthesis Gate** — Template-aligned synthesis, then rf-analyst synthesis review + rf-qa synthesis gate + rf-qa-qualitative synthesis-coherence (parallel), then serialized fix (consolidate findings, single fix agent, 2-agent verification round)
- **Phase 6: Assembly + Lens-Based QA + Source Fidelity Gate** — rf-assembler produces final document, then parallel lens-based QA (4-6 rf-qa structural lenses + 4-6 rf-qa-qualitative content lenses + 3 tech-reference domain-specific lenses, all fix_authorization: false), then consolidated findings, then a single serialized fix agent, then verification round, then a source-document fidelity gate (minimum 5 rf-qa fidelity agents, scale to 6-8, reading the source code files AND the assembled document)
- **Phase 7: Present to User & Complete Task** — Deliver document, present artifacts, handle consolidation sources

If a task file already exists for this feature (from a previous session), skip Stage A and invoke `/task` with the existing task file path to resume from the first unchecked item.

---

## Stage A: Scope Discovery & Task File Creation

### A.1: Check for Existing Task File

Before creating a new task file, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `TASK-TECHREF-*/` folder containing a task file related to this feature
2. If found, read the task file inside the folder and check for unchecked `- [ ]` items
3. If unchecked items exist → skip to Stage B (resume execution)
4. If all items are checked → inform user that the tech reference is already complete, offer to re-run or update the existing document
5. Check for existing task folder at `.dev/tasks/to-do/TASK-TECHREF-*/`:
   a. If `research-notes.md` exists inside the task folder with `Status: Complete` → skip to A.5 (review sufficiency, then build task file)
   b. If `research-notes.md` exists inside the task folder with `Status: In Progress` → read it, resume A.3 scope discovery from where it left off, then continue to A.4 to update the file
   c. If task folder exists but no `research-notes.md` → continue with A.3 but use the existing folder
6. If no task folder exists → continue with A.2

### A.2: Parse & Triage

Break the user's request into structured components:

- **GOAL**: What feature or subsystem to document (the technical reference subject)
- **WHY**: What prompted the documentation effort (new feature, consolidation, onboarding, update)
- **WHERE**: Specific directories, files, or subsystems to focus on
- **OUTPUT_TYPE**: The kind of tech reference needed (new creation, stub population, consolidation, update)
- **FEATURE_SLUG**: A kebab-case identifier for the research directory (e.g., `wizard`, `agent-llm-system`, `pixel-streaming`)

**Triage into Scenario A or B:**

**Scenario A — Explicit request:** User provided most of: feature name, source directories, output location, context for documentation.
Example: "Create a tech reference for the wizard system. Root: `frontend/app/wizard/`. There's an existing stub at `docs/frontend/wizard-technical-reference.md` to populate."
→ Scope discovery confirms details and fills minor gaps. Lighter exploration.

**Scenario B — Vague request:** User provided a feature name but few specifics.
Example: "Document the agent system"
→ Scope discovery does broad exploration to map what exists, identify subsystems, and plan investigation assignments.

**Do NOT interrogate the user with a list of questions.** Proceed with what you have and let scope discovery figure out the rest from the codebase. Only ask the user if there's a genuine ambiguity about **intent** that can't be inferred (e.g., the feature name is too vague to even begin searching). Use the "What to Do If the Prompt Is Incomplete" template from the Input section only when the request truly cannot proceed.

### A.3: Perform Scope Discovery

Use Glob, Grep, and codebase-retrieval to map the feature's shape. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.

**Adjust depth by scenario:**
- **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, scan for related code, identify gaps in what the user specified.
- **Scenario B**: Broad discovery — scan the full codebase for anything touching the feature, map all relevant subsystems, identify documentation, count files.

**Discovery steps:**

1. **Check for an existing stub** — look for a `*-technical-reference.md` file at the expected output location or in `docs/`. If it has a "Source Files to Consolidate" section, read those source docs for context — but treat them as hints, not truth. Also scan for any existing documentation about this feature (READMEs, architecture docs, design docs in `docs/`) — these become input for Doc Analyst research agents.

2. **Map the feature's files and directories** — enumerate:
   - Primary source directory and key subdirectories
   - Number of files and approximate complexity
   - Major subsystems (group files by function)
   - External integration points (imports from outside the feature)

3. **Plan research assignments** — divide the feature into specific investigation topics, each becoming a subagent assignment. Common topics for tech references:
   - Directory structure and file organization
   - Each major subsystem (1 per subsystem)
   - State management / data model
   - Integration points and API surface
   - Hooks, utilities, and shared code
   - Existing documentation review (if consolidating other docs)

**Research assignment types** (use as many as the feature requires):

| Type | Purpose | What the Agent Does |
|------|---------|-------------------|
| **Code Tracer** | Understand how code actually works | Read implementations, trace data flow, follow imports, document behavior |
| **Doc Analyst** | Extract context from existing documentation | Read docs, **cross-validate every architectural claim against actual code** (see Documentation Staleness Protocol), note discrepancies and stale content, extract relevant context |
| **Integration Mapper** | Identify connection points | Map APIs, extension points, plugin interfaces, service boundaries, config surfaces |
| **Pattern Investigator** | Find reusable patterns | Search for similar implementations that solve analogous problems |
| **Architecture Analyst** | Understand system design | Trace architectural decisions, dependency chains, component relationships |

4. **Plan web research topics** — from gaps identified during discovery (framework docs, third-party API references, pattern documentation)

5. **Determine synthesis file mapping** — map planned research files to template sections using the synth mapping table

6. **Select depth tier** based on component count — Lightweight (<5 files), Standard (5-20), Heavyweight (20+). Default to Standard if unsure. Record the tier selection and rationale in the research notes.

Compute `<subject>` from the subject of the reference using the rules in the Subject Derivation section. If no clean subject is derivable, use `general`. Create the task folder: `.dev/tasks/to-do/TASK-TECHREF-<subject>-YYYYMMDD-HHMMSS/` with subfolders `research/`, `synthesis/`, `qa/`, `reviews/`

**MANDATORY — Partition large input across parallel agents.** Single-agent scope discovery is PROHIBITED for any input exceeding ~1000 lines total (this includes user-provided documents plus any referenced source files). Input size thresholds:
- **≤1000 lines total:** 1 scope-discovery agent is acceptable
- **1000-3000 lines:** 2-3 parallel agents, each assigned a slice (per-document, per-section-range, or per-aspect)
- **3000-6000 lines:** 4-5 parallel agents
- **6000+ lines:** 5-10+ parallel agents per the Heavyweight tier requirement

**Partitioning heuristics:**
- By document — one agent per source file if multiple files
- By section range — split a large file into sequential section groups (e.g., sections 1-14 / 15-28)
- By aspect — requirements / architecture / data models / API specs / integration points as separate slices

**rf-task-researcher as agent type, not replacement:** The rf-task-researcher agent type may be used for each partitioned slice when context isolation is valuable. Spawn N rf-task-researchers in parallel (one per slice), each with its own RESEARCH_REQUEST scoping its assigned slice. A SINGLE rf-task-researcher reading the entire input is explicitly prohibited — it defeats parallelism and causes the same context pressure the partitioning is meant to prevent.

**Spawning pattern:** All scope-discovery agents MUST be spawned in parallel using multiple Agent tool calls in a single message. Sequential scope discovery is prohibited.

**Why this matters:** A single agent reading >1000 lines will skim, miss detail, and consume the parent orchestrator's context budget via its return value. Partitioning achieves depth (each agent focused on a slice) AND context protection (each slice isolated to its own agent context) simultaneously.

### A.4: Write Research Notes File (MANDATORY)

Write the scope discovery results to a structured research notes file at `${TASK_DIR}research-notes.md`. This file is what the builder reads — NOT inline content in the BUILD_REQUEST.

The file MUST be organized into these 7 categories (include all, mark as "N/A" if empty):

```markdown
# Research Notes: [FEATURE]

**Date:** [today]
**Scenario:** [A or B]
**Depth Tier:** [Lightweight / Standard / Heavyweight]

---

## EXISTING_FILES
[Key source files, directories, and stubs found during scope discovery. Per-file detail: path, purpose, key exports, approximate line count. Group by directory or subsystem.]

## PATTERNS_AND_CONVENTIONS
[Naming patterns, architecture patterns, design decisions observed. Cite specific files as evidence.]

## FEATURE_ANALYSIS
[Subsystems identified, complexity assessment, major components and their responsibilities, integration boundaries. This replaces SOLUTION_RESEARCH from tech-research — tech-reference is always documenting what exists, not evaluating new approaches.]

## RECOMMENDED_OUTPUTS
[Research files to create, synthesis files to produce, and the mapping from research files to template sections. Full paths and purposes for each.]

## SUGGESTED_PHASES
[How to structure the task file phases. For each planned research agent:
- Agent number, investigation type, topic
- Files/directories to investigate
- Output file path
- Web research topics identified from gaps
- Synthesis file mapping]

## TEMPLATE_NOTES
[Tech reference template observations, tier selection reasoning (Lightweight/Standard/Heavyweight), notes on which template sections apply vs N/A for this feature.]

## AMBIGUITIES_FOR_USER
[Genuine ambiguities about user intent that cannot be resolved from the codebase. If none, write "None — intent is clear from the request and codebase context."]
```

### A.5: Review Research Sufficiency (MANDATORY GATE)

**You MUST review the research notes before spawning the builder.** This is a quality gate — do NOT skip it.

Read `${TASK_DIR}research-notes.md` and evaluate:

1. Is the feature scope clearly bounded?
2. Are all major subsystems identified?
3. Are integration points mapped?
4. Is existing documentation inventoried?
5. Are research assignments concrete enough for the task builder to create per-agent checklist items? (Each needs: topic, agent type, file list, output path)
6. Is the template section mapping reasonable?
7. If any doc-sourced claims appear in the research notes (e.g., from scanning existing documentation during scope discovery), are they tagged with `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`? Claims marked `[CODE-CONTRADICTED]` or `[UNVERIFIED]` must be flagged in AMBIGUITIES_FOR_USER.

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

**For tech-reference, the answer is almost always Template 02** — the pipeline inherently involves discovery (scope mapping), parallel agents (codebase research), analyst/QA gates (research gate, synthesis gate, report validation), synthesis, and assembly. Only use Template 01 for trivial updates to an existing tech reference (e.g., updating a single section with known content).

### A.7: Build the Task File

Write the BUILD_REQUEST to a file at `${TASK_DIR}BUILD-REQUEST.md`, then invoke the `/task-builder` skill. The task-builder reads the BUILD_REQUEST file, performs quality gates (rf-analyst + rf-qa), spawns the rf-task-builder agent to create the MDTM task file, and runs structural and qualitative validation internally. No manual verification step is needed — task-builder handles all validation and mediation.

**Step 1: Write `${TASK_DIR}BUILD-REQUEST.md`** using the Write tool with the following content:

```
# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-reference
Task Directory: ${TASK_DIR}
Research Notes: ${TASK_DIR}research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Create a comprehensive Technical Reference document for [FEATURE] following the project template. The document will be written to docs/[domain]/FEATURE-NAME-TECHNICAL-REFERENCE.md.

WHY: [WHY — what prompted this documentation effort and what the reference will be used for]

TASK_ID_PREFIX: TASK-TECHREF

FEATURE_SLUG: [FEATURE_SLUG — derived from feature name, e.g., wizard-system, agent-orchestration]

TEMPLATE: [01 or 02 — skill selects:
  01 = simple update to existing tech reference, single-section change
  02 = full tech reference creation with discovery, research, synthesis, assembly]

DOCUMENTATION STALENESS WARNINGS:
[If scope discovery found any documentation that contradicts actual code, list the
specific claims and contradictions here. If none found during scope discovery, write:
"None found during scope discovery. Phase 2 agents will perform full documentation
cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags."]
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 1 (Preparation): Update task status, confirm scope from research notes, read the template, select depth tier, create task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders
- Phase 2 (Deep Investigation): L1 Discovery — agents investigate feature code and write findings files to ${TASK_DIR}research/
- Phase 3 (Completeness Verification): L4 Review/QA — spawn 2 rf-analyst (lenses: completeness-verification + cross-validation), 2 rf-qa (lenses: evidence-quality + gap-detection), and 1 rf-qa-qualitative (lens: research-depth — are findings genuinely deep or surface-level?) IN PARALLEL as a multi-lens quality gate. All 5 agents write lens-specific reports, all fix_authorization: false. Serialized fix protocol: consolidate findings into qa-research-consolidated-findings.md, spawn targeted gap-filling research agents (one per gap), then 2-agent verification round (1 rf-qa + 1 rf-qa-qualitative). Max 3 cycles. Partitioning >6 research files: spawn each lens type across partitions (e.g., 10 files = 2 analyst × 2 + 2 qa × 2 + 1 qualitative × 2 = 10 agents).
- Phase 4 (Web Research): L1 Discovery — agents explore external sources and write findings files
- Phase 5 (Synthesis + Multi-Agent Synthesis Gate): L2 Build-from-Discovery — agents read research files and produce template-aligned synth sections. Then spawn 2 rf-analyst (lenses: synthesis-accuracy + source-tracing), 2 rf-qa (lenses: structure + content-quality), and 1 rf-qa-qualitative (lens: synthesis-coherence — does the synthesis tell a coherent story from the research?) IN PARALLEL as a multi-lens quality gate, all fix_authorization: false. Consolidate findings, then spawn ONE rf-qa fix agent (fix_authorization: true) applying all consolidated findings, then 2-agent verification round. Partitioning >4 synthesis files.
- Phase 6 (Assembly + Lens-Based QA + Source Fidelity Gate): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final tech reference document, then spawn lens-based QA agents in parallel (4-6 rf-qa on structural lenses: template-conformance, internal-consistency, evidence-quality, completeness; 4-6 rf-qa-qualitative on content lenses: actionability, numbers-metrics, crossref-chain, domain-accuracy; 3 tech-reference domain-specific lens agents: code-example-accuracy, api-signature-correctness, configuration-value-verification — all fix_authorization: false, report only). Consolidate findings, then spawn ONE rf-qa fix agent (fix_authorization: true), then 2-agent verification round (max 3 cycles). After lens-based QA passes, spawn source-fidelity gate (minimum 5 rf-qa fidelity agents, scale to 6-8, each reading assigned source code range + FULL tech reference), serialized fix protocol, verification round. Both gates use serialized (not parallel) fix authorization to prevent churn.
- Phase 7 (Present to User & Complete Task): ANTI-ORPHANING — task-completion items are WITHIN this phase, not in a separate Post-Completion section.

QA_INTENSITY: [lite / standard / full]  (per I22 — determined by tier mapping in Tier Selection section or user override)
QA_GATE_REQUIREMENTS: PER_PHASE
  **NOTE: Gate descriptions below specify FULL intensity agent counts. When QA_INTENSITY is lite or standard, the rf-task-builder applies I22 reductions via the QA Intensity Adaptation table in the Agent Prompt Templates section.**
  Gate 1: Research Completeness (Phase 3)
    - lite: 1 rf-qa (evidence + gaps) + 1 rf-qa-qualitative (depth + completeness) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 3 gap-fill cycles. Partitioning >6 files (each lens type partitioned independently).
  Gate 2: Synthesis Quality (Phase 5)
    - lite: 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 3 fix cycles. Partitioning >4 files.
  Gate 3: Final Document Lens-Based QA (Phase 6, step 6a)
    - lite: 1 rf-qa (combined structural) + 1 rf-qa-qualitative (combined content) + 1 domain lens (code-example-accuracy) = 3 agents. Max 1 fix cycle.
    - standard: 3 rf-qa structural (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content (actionability, domain-accuracy, crossref-chain) + 1 domain lens (code-example-accuracy) = 7 agents. Max 2 fix cycles.
    - full: 4-6 rf-qa + 4-6 rf-qa-qualitative (scaled by output size, partitioning at 1500+ lines) + 3 domain lenses (code-example-accuracy, api-signature-correctness, configuration-value-verification) = 11-15 agents. Max 3 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, step 6c)
    - lite: 1 rf-qa fidelity agent (combined semantic-coverage + phantom-detection lenses). Max 1 fix cycle.
    - standard: 2 rf-qa fidelity agents (semantic-coverage + detail-preservation). Max 2 fix cycles.
    - full: 5 rf-qa fidelity agents (semantic-coverage, detail-preservation, phantom-coverage, aspirational-content-detection, cross-reference-verification). Scale to 6 at 1000-2000 source lines, 8 at >2000. Max 3 fix cycles.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + SOURCE_FIDELITY
  TEMPLATE_COMPLIANCE: All sections from technical_reference_template.md must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.
  SOURCE_FIDELITY: Phase 6 Gate 4 fidelity agents read the actual source code files AND the assembled tech reference; semantic coverage of every documented subsystem, API signature, and configuration value must be verified against source code (not just the synthesis files). Detail preservation is mandatory: function signatures, config defaults, and type shapes in the tech reference must match the code verbatim.

TESTING_REQUIREMENTS: N/A — documentation-only skill, no code produced, no tests applicable.

RESEARCH NOTES FILE:
${TASK_DIR}research-notes.md
Read this file FIRST for full detailed findings including: existing files, patterns, planned investigation assignments, synthesis mapping, and output paths.

TEMPLATE_PATH: .claude/templates/documents/technical_reference_template.md
OUTPUT_PATH: docs/[domain]/FEATURE-NAME-TECHNICAL-REFERENCE.md

SKILL CONTEXT FILE:
.claude/skills/tech-reference/SKILL.md
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt. Read the "Synthesis Mapping Table" section for the standard synth-file-to-template-section mapping. Read the "Synthesis Quality Review Checklist" section for post-synthesis verification. Read the "Assembly Process" section for tech reference assembly steps. Read the "Validation Checklist" section for Phase 6 validation criteria. Read the "Content Rules" section for writing standards. Read the "Tier Selection" section for depth tier line budgets and agent counts. Read the "Output Structure" section for the final document format. These must be embedded in the relevant checklist items per B2 self-contained pattern.

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
- Confirm scope from research notes (feature boundaries, key directories, tier selection)
- Read the technical reference template at .claude/templates/documents/technical_reference_template.md
- Select depth tier (Lightweight / Standard / Heavyweight) based on component count and complexity
- Create the task folder at ${TASK_DIR} with research/, synthesis/, qa/, reviews/ subfolders (if not already created during scope discovery)

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research agent (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md
- Each item specifies: investigation topic, type (Code Tracer / Doc Analyst / Integration Mapper / Pattern Investigator / Architecture Analyst), files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from SKILL.md) in each checklist item per B2
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. For example, with 6 research assignments: spawn all 6 agents in one message, mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.
- Agent count follows tier guidance: Lightweight 2-3, Standard 4-6, Heavyweight 6-10+

**Authoritative specification for gate parameters (agent counts, fix cycle budgets, scaling tiers) is in the BUILD_REQUEST template above (QA_GATE_REQUIREMENTS). This section provides expanded operational guidance for each phase. In case of conflict between this section and the BUILD_REQUEST specification, the BUILD_REQUEST values take precedence.**

Phase 3 — Research Completeness Verification (MULTI-AGENT LENS GATE, PARALLEL):
- Spawn 5 agents IN PARALLEL, all fix_authorization: false (report only): (1) rf-analyst (completeness-verification lens) — writes to `${TASK_DIR}qa/analyst-completeness-report.md`; (2) rf-analyst (cross-validation lens — do findings from different research agents agree? do cross-references between research files resolve?) — writes to `${TASK_DIR}qa/analyst-crossval-report.md`; (3) rf-qa (evidence-quality lens) — writes to `${TASK_DIR}qa/qa-research-evidence-report.md`; (4) rf-qa (gap-detection lens — are there subsystems, files, or integration points mentioned in scope discovery but absent from research?) — writes to `${TASK_DIR}qa/qa-research-gaps-report.md`; (5) rf-qa-qualitative (research-depth lens — are findings genuinely deep with traced data flows and function signatures, or surface-level file listings?) — writes to `${TASK_DIR}qa/qa-research-depth-report.md`. Each agent gets a lens-specific prompt with adversarial framing: "Assume these research files missed at least 5 critical issues in your lens area. Find them." Embed full prompts in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE analyst instances and MULTIPLE QA instances in parallel, each with an `assigned_files` subset. The threshold is >6 for research files because research files tend to be longer and more detailed than synthesis files. For example, with 10 research files: spawn 2 analyst instances (5 files each) + 2 QA instances (5 files each) + 2 qualitative instances (5 files each) = 6 parallel agents. Each partition instance writes to a numbered report (e.g., `analyst-completeness-report-1.md`, `analyst-completeness-report-2.md`). After all instances complete, merge their reports: union of all findings, take the more severe rating for any item flagged by multiple partitions, deduplicate gaps.
- Read ALL reports (or the merged report). Determine verdict from the QA report(s) (PASS / FAIL), cross-referenced with analyst findings. If PASS, proceed to Phase 4. If FAIL, follow the serialized fix protocol below.
- **Serialized fix protocol for Phase 3 (follows the same consolidate-fix-verify pattern as Phases 5 and 6):**
  1. **Consolidate findings:** Merge all 5 agent reports into a single findings list at `${TASK_DIR}qa/qa-research-consolidated-findings.md`. Deduplicate overlapping findings. Preserve the highest severity rating when duplicates disagree.
  2. **Gap-filling as fix step:** A "gap" is any FAIL-rated finding from the consolidated findings list. Spawn additional targeted research agents (one per gap from the consolidated findings). Each gap-filling agent follows the same incremental writing protocol. This is the "fix" step, analogous to the single fix agent in Phases 5 and 6, but using research agents since the remediation is additional investigation, not file editing.
  3. **Verification round:** After gap-filling agents complete, spawn a verification round: rf-qa (fix-cycle, fix_authorization: false) re-verifies the previously-failed items against the new research, plus rf-qa-qualitative (re-check, fix_authorization: false) confirms the gaps are genuinely filled. **ADVERSARIAL STANCE:** Assume the work contains errors. Verify every claim exhaustively.
  4. **Cycle:** If verification finds remaining gaps, repeat from step 1 (re-consolidate remaining + new findings, spawn gap-fillers, verify). Maximum 3 cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance on how to proceed. Do NOT continue to Phase 4 without user approval. Note: This budget is independent of the A.5 gap-fill rounds. A.5 verifies research notes sufficiency for the builder (a lightweight pre-builder check). Phase 3 verifies research agent output quality (a formal multi-lens gate). Different scope, separate counters.
- Compile final gaps into ${TASK_DIR}gaps-and-questions.md (merged from all reports)
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (from research notes SUGGESTED_PHASES and Phase 3 gaps)
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
- Each item specifies: topic, context from codebase findings, output file path
- Web research targets should include (as applicable): official framework/engine documentation, design patterns and best practices, third-party tools/libraries/APIs, community solutions to similar problems, GitHub issues and discussions, conference talks and technical blog posts from recognized experts
- Web research is optional — only spawn when codebase research reveals gaps requiring external documentation

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One checklist item PER synthesis file (from research notes RECOMMENDED_OUTPUTS, mapped via the Synthesis Mapping Table in SKILL.md)
- Each item spawns an Agent subagent with the synthesis agent prompt from SKILL.md
- Each item specifies: research files to read, template sections to produce, output path (${TASK_DIR}synthesis/synth-[NN]-[topic].md)
- After ALL synthesis agents complete, spawn 5 agents IN PARALLEL, all fix_authorization: false (report only): (1) rf-analyst (synthesis-accuracy lens — do synth claims match research file evidence?) — writes to `${TASK_DIR}qa/analyst-synthesis-accuracy-report.md`; (2) rf-analyst (source-tracing lens — can every synth claim be traced to a specific research file finding?) — writes to `${TASK_DIR}qa/analyst-synthesis-tracing-report.md`; (3) rf-qa (structure lens — synth files follow template section mapping, correct headers, no missing sections) — writes to `${TASK_DIR}qa/qa-synthesis-structure-report.md`; (4) rf-qa (content-quality lens — content rules compliance, no code reproductions, appropriate detail level) — writes to `${TASK_DIR}qa/qa-synthesis-quality-report.md`; (5) rf-qa-qualitative (synthesis-coherence lens — does the synthesis tell a coherent, connected story from the research, or is it fragmented?) — writes to `${TASK_DIR}qa/qa-synthesis-coherence-report.md`. Each agent gets a lens-specific prompt with adversarial framing. Embed full prompts per B2. After all 5 reports are received: consolidate findings at `${TASK_DIR}qa/qa-synthesis-consolidated-findings.md`, spawn ONE rf-qa fix agent (fix_authorization: true) to apply all fixes, then 2-agent verification round. Partitioning threshold >4 synthesis files still applies — each lens type is partitioned independently.
- **Parallel partitioning for large workloads:** When >4 synthesis files exist, spawn multiple analyst instances and multiple QA instances in parallel, each with an `assigned_files` subset. The threshold is lower than Phase 3 (>4 vs >6) because synthesis QA requires deeper per-file analysis (tracing claims back to research files, verifying cross-section consistency). Same partitioning pattern as Phase 3. Each partition instance writes to a numbered report. Orchestrator merges all partition reports after completion.
- Read ALL reports. Determine verdict from QA report(s), cross-referenced with analyst findings. If PASS → proceed to Phase 6. If FAIL → if fix agent could not resolve all findings, re-run affected synthesis agents whose output files were flagged in the consolidated findings (identify them by matching finding locations to synthesis file paths), then re-spawn `rf-qa` (fix-cycle). Maximum 3 fix cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present findings to user, ask for guidance. Do NOT continue to Phase 6 without user approval.

Phase 6 — Assembly & Validation (RF-ASSEMBLER + Structural QA + Qualitative QA):
- Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") — NOT a general-purpose Agent — to assemble the final technical reference. Hand it: the list of synth file paths in order (as component_files), the output path docs/[domain]/FEATURE-NAME-TECHNICAL-REFERENCE.md, the template at .claude/templates/documents/technical_reference_template.md (as output_format), the Assembly Process steps from SKILL.md (as assembly_rules), and the Content Rules from SKILL.md (as content_rules). The assembler reads each synth file and writes the document incrementally — frontmatter first, then sections in template order, then Table of Contents, then cross-checks internal consistency. The assembler must be a single agent (NOT parallel) because cross-section consistency requires seeing the whole document. Embed the full assembler prompt in the checklist item per B2.
- **Step 6a: Lens-Based QA (PARALLEL, all fix_authorization: false).** After the assembler returns the document path, determine the document's line count and select the lens agent count from this table: <500 lines = 4+4; 500-1500 = 4+4; 1500-3000 = 5+5; >3000 = 6+6 (rf-qa structural + rf-qa-qualitative content). At higher tiers, the additional agents are partitioned instances of existing lenses with assigned section ranges (e.g., at 5+5: split the completeness lens across 2 agents, each covering half the document; at 6+6: also split evidence-quality). PLUS 3 tech-reference domain-specific lens agents (see below). Spawn ALL lens agents IN PARALLEL. Each agent gets a lens-specific prompt, its own report file, and fix_authorization: false (report only). **Standard structural lenses (rf-qa):** (1) template-conformance — all required sections present, correct ordering, no remaining placeholders; (2) internal-consistency — IDs match across tables, counts agree, cross-references resolve; (3) evidence-quality — all claims cite file paths/line numbers, no unverified assertions, no hallucinated paths; (4) completeness — every topic from scope discovery appears in the output. **Standard content lenses (rf-qa-qualitative):** (1) actionability — every Extension Guide entry is specific enough to execute; (2) numbers-metrics — quantitative claims are consistent and sourced; (3) crossref-chain-integrity — subsystem→API→config→example chains all resolve; (4) domain-accuracy — claims about codebase match actual code, no aspirational features described as current. **Tech-reference domain-specific lenses:** (1) code-example-accuracy (rf-qa) — code snippets match actual source files; (2) api-signature-correctness (rf-qa) — documented API signatures match actual code; (3) configuration-value-verification (rf-qa-qualitative) — config values and defaults match actual files. Each lens agent writes to `${TASK_DIR}qa/qa-lens-[lens-name]-report.md`. Embed lens-specific prompt with adversarial framing in each checklist item per B2: "Assume this document has at least N errors in your lens area. Find them." (N = document_lines / 100, minimum 5).
- **Step 6b: Consolidate Findings + Serialized Fix.** Read ALL lens reports. Consolidate into a single findings list at `${TASK_DIR}qa/qa-consolidated-findings.md`. Spawn ONE rf-qa fix agent (fix_authorization: true) with the consolidated findings list — it applies ALL fixes to the document. Then spawn a 2-agent verification round: 1 rf-qa (structural verification, fix_authorization: false) + 1 rf-qa-qualitative (content verification, fix_authorization: false). If verification finds new issues, repeat from fix agent (max 3 total cycles). After 3 cycles, HALT: log remaining issues, present to user, ask for guidance.
- **Step 6c: Source-Document Fidelity Gate (PARALLEL, fix_authorization: false).** After lens-based QA passes, spawn minimum 5 rf-qa fidelity agents (scale to 6 if the research files reference 1000-2000 lines of source code total, 8 if >2000 lines). Each fidelity agent reads BOTH its assigned source-code-file range (from Phase 2 research file paths) AND the FULL assembled tech reference. Each fidelity agent is assigned ONE focused lens from the list below. Fidelity lenses: (a) semantic-coverage — every subsystem, API endpoint, and configuration item documented in the tech reference can be traced to actual source code; (b) detail-preservation — function signatures, config defaults, error codes, and type shapes match the code exactly; (c) phantom-coverage-detection — file paths referenced in the tech reference must exist and contain what the doc says they contain; (d) aspirational-content-detection — no planned/aspirational features described as current; (e) cross-reference-verification — all cross-references between sections resolve correctly and reference the right content. Each fidelity agent writes to `${TASK_DIR}qa/qa-source-fidelity-[N]-report.md`. If fidelity agents find issues: consolidate findings, spawn ONE fix agent (fix_authorization: true), then 2-agent verification round (1 rf-qa + 1 rf-qa-qualitative, fix_authorization: false) (max 3 fix cycles). HALT after max cycles exceeded.
- **Step 6d: Verify all QA complete.** Read all lens reports, consolidated findings, verification reports, and fidelity reports. If any unresolved issues remain at any severity (CRITICAL, IMPORTANT, MINOR), address ALL of them before proceeding to Phase 7. Zero leniency — no severity level is exempt.

Phase 7 — Present to User & Complete Task:
- Present summary to user: document location, line count and tier classification, sections populated vs skipped, research/synth artifact locations, gaps needing manual review
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date
- If the tech reference was created by consolidating existing docs: present the source doc list to the user and note they can be archived to docs/archive/[appropriate-subdir]/ when ready
- CRITICAL ANTI-ORPHANING RULE: Task-completion items (write task summary, update frontmatter to "🟢 Done") MUST be inside this phase, NEVER a separate Post-Completion section. Downstream offers and archival suggestions are `NON-BLOCKING` — present them, mark complete, do not wait for user response.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-TECHREF-<subject>-[YYYYMMDD]-[HHMMSS]/TASK-TECHREF-<subject>-[YYYYMMDD]-[HHMMSS].md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, synthesis mapping, content rules, validation checklist, tier selection, and assembly procedure (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-TECHREF-<subject>-[YYYYMMDD-HHMMSS]/TASK-TECHREF-<subject>-[YYYYMMDD-HHMMSS].md using PART 2 structure
7. Return the task file path
```

**Step 2: Invoke the task-builder skill:**
**CRITICAL: After task-builder completes and outputs TASK_FILE_READY, you MUST continue to Stage B below. Do NOT stop at task-builder's output.**


```
Skill(skill: "task-builder", args: "${TASK_DIR}BUILD-REQUEST.md")
```

The task-builder skill reads the BUILD_REQUEST file, detects `Source: skill-delegated` and `SKIP_RESEARCHERS: true`, skips its own research phase, spawns the rf-task-builder agent, and runs structural and qualitative validation. It returns the task file path.

**Note:** Task-builder handles all verification internally — structural validation checks frontmatter, phases, B2 pattern, embedded prompts, parallel spawning instructions, partitioning guidance, rf-assembler usage, and anti-orphaning. Qualitative validation checks operational correctness. No separate verification step is needed in this skill. Proceed directly to Stage B with the returned task file path.

---

## Stage B: Task File Execution

Stage B delegates execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA verification, error handling, and session management.

### Delegation Protocol

1. **Invoke /task** using the Skill tool with `skill: "task"` and `args` set to the task file path from Stage A (e.g., `.dev/tasks/to-do/TASK-TECHREF-docker-compose-20260309-120000/TASK-TECHREF-docker-compose-20260309-120000.md`).
2. **Execution transfers to /task**, which reads the task file and processes each checklist item via the F1 loop — spawning subagents as specified in B2 items and running phase-gate QA after each phase (Phase 2+).
3. **No additional execution logic is needed** in this skill since all execution rules (F1 loop, F2 prohibited actions, parallel spawning, F4 modification restrictions, F5 frontmatter protocol, error handling, session resumption) are provided by /task.
4. **QA coverage:** The task file already contains skill-specific QA items (rf-analyst + rf-qa + rf-qa-qualitative at Phases 3, 5, and 6), and /task adds phase-gate QA on top. This results in intentional, acceptable double QA at gate phases — skill-specific QA uses domain-aware research/synthesis gates while /task's phase-gate QA verifies "ensuring..." clauses from all items in the phase.

### What the Task File Must Contain

Since /task does NOT read this SKILL.md during execution, all skill-specific instructions must be baked into the task file during Stage A:

- **Agent prompt templates** customized with specific topics, file paths, and investigation assignments
- **Validation checklists and content rules** embedded in "ensuring..." clauses of each B2 item
- **Output paths and file naming conventions** specified in each item
- **All phase-specific context** so each B2 item is fully self-contained — an executor reading only the task file has everything needed to complete each item

**CRITICAL:** `/task` does NOT read this SKILL.md during execution. ALL skill-specific instructions, agent prompts, validation criteria, and content rules must be baked into the task file items during Stage A. This includes prohibited actions: research agents READ code, they do not modify it; do not invent file paths; do not fabricate content; do not delete research artifacts after assembly.

---

## Agent Prompt Templates

These templates are provided to the task builder (in the BUILD_REQUEST) so it can embed them in the task file's self-contained checklist items. The builder should customize each instance with the specific feature, files, and output path.

**QA Intensity Adaptation (per Template 02 I22):**
- lite: Gate 3 combines to 3 agents:
  (1) rf-qa combined-structural: use template-conformance + internal-consistency + evidence-quality + completeness lenses
  (2) rf-qa-qualitative combined-content: use actionability + domain-accuracy + crossref-chain + numbers-metrics lenses
  (3) highest-value domain lens: code-example-accuracy
  Intermediate gates: 2 agents (1 rf-qa combined + 1 rf-qa-qualitative combined)
  Fidelity: 1 agent (combined coverage + phantom lenses). Max 1 fix cycle. 1 verification agent.
- standard: Gate 3 uses 7 agents:
  3 rf-qa structural: template-conformance, internal-consistency, evidence-quality
  3 rf-qa-qualitative content: actionability, domain-accuracy, crossref-chain
  1 domain lens: code-example-accuracy
  Intermediate gates: 3 agents (1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative)
  Fidelity: 2 agents. Max 2 fix cycles. 2 verification agents.
- full: Use all prompts below as-is (current behavior, no changes).

### Codebase Research Agent Prompt

```
Research this aspect of [feature name] and write findings to [output-path]:

Topic: [topic description]
Investigation type: [Code Tracer / Doc Analyst / Integration Mapper / Pattern Investigator / Architecture Analyst]
Files to investigate: [list of files/directories]
Feature root: [primary directory]
Feature context: [the overall feature being documented]

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
3. Document the public interface — what do other parts of the codebase actually use from here? Cite file paths, function signatures, and line numbers for every export.
4. Identify patterns — what conventions, architectural decisions, or design patterns are evident?
5. Check for edge cases — error handling, fallbacks, configuration-driven behavior
6. Note dependencies — what does this subsystem depend on? What depends on it?
7. Flag gaps — what is missing, broken, undocumented, or unclear? What needs further investigation?
8. Note integration points and extension patterns — where does this subsystem connect with others? What are the boundaries? How would a developer add new functionality here (new handler, new plugin, new stage)?

CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Code describes CURRENT state. These frequently diverge.
When you encounter documentation that describes an architecture, pipeline, service, component, endpoint,
or workflow, you MUST cross-validate EVERY structural claim against actual code before reporting it as current:

1. **Services/components described in docs:** Verify the service directory, entry point file, and key classes
   actually exist in the repo. Use Glob to check. If it doesn't exist, the doc is STALE — report as historical, not current.
   Example: Doc says "The AuthService in `backend/app/services/auth_service.py` handles JWT validation" → Glob for `backend/app/services/auth_service.py`. If missing, mark [CODE-CONTRADICTED].

2. **Pipelines/call chains described in docs:** Trace at least the first and last hop in actual source code.
   If any hop is missing, the pipeline is STALE.
   Example: Doc says "Request → AuthMiddleware → AgentRouter → SwarmOrchestrator → ToolExecutor" → Read the router to verify it calls SwarmOrchestrator, read SwarmOrchestrator to verify it calls ToolExecutor.

3. **File paths mentioned in docs:** Spot-check that referenced files exist.
   Example: Doc references `frontend/src/components/StreamViewer.tsx` → Glob for that exact path. If the component was renamed or moved, mark [CODE-CONTRADICTED] with the actual current path.

4. **API endpoints described in docs:** Verify the endpoint exists in the actual router/app code.
   Example: Doc says "POST /api/v1/sessions/start" → Grep for that route in the router files. If it's now "/api/v1/sessions/create", mark [CODE-CONTRADICTED].

For EVERY doc-sourced architectural claim, mark it with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** — code shows different implementation (describe what code actually shows)
- **[UNVERIFIED]** — could not find corresponding code; may be stale, planned, or in a different repo

Claims marked [UNVERIFIED] or [CODE-CONTRADICTED] MUST appear in the Gaps and Questions section.
Do NOT present doc-sourced claims as verified facts without the code verification tag.

Output Format:
- Use descriptive headers for each file or logical group investigated
- Include actual file paths, class names, function names, line numbers
- Include actual type signatures and export lists (not reproduced code blocks — summaries with key signatures)
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
Feature context: [the overall feature being documented]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for official documentation, guides, and API references
2. Search for design patterns and best practices relevant to this feature type
3. Search for implementation patterns, known issues, gotchas, and optimization strategies
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
  [How external findings relate to the feature's implementation]

IMPORTANT: Our codebase is the source of truth. External research adds context but does not override verified code behavior. If you find a discrepancy, note it explicitly.
```

**Common web research topics for tech references:**
- Framework best practices and recommended patterns for the technology stack in use
- Component API documentation for third-party libraries the feature depends on
- Architectural pattern references (e.g., event-driven, CQRS, hexagonal) relevant to the feature design
- Performance optimization guides for the feature's technology domain
- Established design patterns for the feature type (e.g., state management patterns, streaming protocols)

### Synthesis Agent Prompt

```
Read the research files listed below and synthesize them into template-aligned sections for a Technical Reference document.

Research files to read: [list of specific file paths]
Template sections to produce: [section numbers and names]
Output path: [synth file path]
Template reference: .claude/templates/documents/technical_reference_template.md

Rules:
0. **Read the template first.** Before synthesizing anything, read `.claude/templates/documents/technical_reference_template.md` to understand each section's expected content, format, and depth. Use the template as your structural guide throughout synthesis.
1. Follow the template structure exactly — use the same headers, tables, and section format
2. Every fact must come from the research files — do not invent, assume, or infer
3. Use tables over prose for multi-item data (file lists, dependencies, config values)
4. Do not reproduce full TypeScript interfaces or function bodies — summarize with key signatures
5. Keep subsystem sections to 40-200 lines depending on complexity. Budget: simple subsystems (utils, config, types) get 40-80 lines; standard subsystems (APIs, external services, integration layers) get 80-120 lines; complex subsystems (state management, routing, data layer) get 120-200 lines.
6. Include ASCII diagrams for architecture and component hierarchies where the research supports them
7. Reference actual file paths from the research — not hypothetical ones
8. When research files contradict each other, note the contradiction and which finding has stronger evidence
9. Web research findings must be explicitly marked as external context, with source URLs
10. **Documentation-sourced claims require verification status.** If a research file reports a finding from documentation, check whether it carries a [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED] tag. Only [CODE-VERIFIED] claims may be presented as current architecture. [CODE-CONTRADICTED] claims must be corrected to match what the code actually shows. [UNVERIFIED] claims must be flagged as uncertain and placed in Open Questions — never in Architecture or API sections as if they are fact.
11. **Never describe architecture from docs alone.** When writing Architecture (Section 2) or API & Integration (Section 8), ONLY use findings that trace back to actual source code reads. Doc-only evidence must be flagged as [UNVERIFIED — doc-only, no code confirmation] and excluded from architecture diagrams.
12. **Extension Guide must be actionable.** Section 13 (Extension Guide) must include specific file paths, function signatures, and step-by-step instructions for common extension scenarios. "Add a new X by creating a file in Y directory" is insufficient — specify the exact file to create, the interface to implement, the registration point to update, and include a minimal code skeleton.

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
Perform a completeness verification of all research files for [feature name].

Analysis type: completeness-verification
Research directory: [research-dir-path]
Research notes file: [research-notes-path]
Depth tier: [Lightweight/Standard/Heavyweight]
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
1. Coverage audit — every key file from scope covered by at least one research file
2. Evidence quality — claims cite specific file paths, line numbers, function names
3. Documentation staleness — all doc-sourced claims tagged [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED]
4. Completeness — every file has Status: Complete, Summary section, Gaps section, Key Takeaways
5. Cross-reference check — cross-cutting concerns covered by multiple agents are cross-referenced
6. Contradiction detection — conflicting findings about the same component surfaced
7. Gap compilation — all gaps unified, deduplicated, and severity-rated (Critical/Important/Minor)
8. Depth assessment — investigation depth matches the stated tier (all public APIs documented, integration points mapped, subsystems traced)

VERDICTS:
- PASS: All checks pass, no critical gaps
- FAIL: Critical gaps exist (list each with specific remediation action)

Use the full output format from your agent definition (tables for coverage, evidence quality, staleness, completeness).
Be adversarial — your job is to find problems, not confirm things work.
```

### Research QA Agent Prompt (rf-qa — Research Gate)

```
Perform QA verification of research completeness for [feature name].

QA phase: research-gate
Research directory: [research-dir-path]
Analyst report: [analyst-report-path] (if exists, verify the analyst's work; if not, perform full verification)
Research notes file: [research-notes-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: [output-path]

You are the last line of defense before synthesis begins. Assume everything is wrong until you verify it.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

IF ANALYST REPORT EXISTS:
1. Read the analyst's completeness report
2. Verify ALL of their coverage audit claims (verify the scope items are actually covered)
3. Validate gap severity classifications (are "Critical" really critical? Are "Minor" really minor?)
4. Check their verdict against your own independent assessment
5. Apply the 10-item Research Gate checklist

IF NO ANALYST REPORT:
Apply the full 10-item Research Gate checklist independently.

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
Perform QA verification of synthesis files for [feature name].

QA phase: synthesis-gate
Synthesis directory: [synthesis-dir-path]
Fix authorization: false (report findings only -- a separate fix agent applies all fixes via serialized protocol)
Output path: [output-path]

You are verifying that synthesis files are ready for assembly into the final technical reference.
You report findings only. Do NOT fix issues in-place.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

PROCESS:
1. Use Glob to find ALL synth files (synth-*.md) in the synthesis directory
2. Read EVERY synth file completely
3. Apply the 12-item Synthesis Gate checklist
4. For each issue found:
   a. Document the issue (what, where, severity)
   b. Document the required fix
   c. Do NOT modify the synthesis files -- a dedicated fix agent will apply all consolidated findings
5. Write your QA report to [output-path]

12-ITEM CHECKLIST:
1. Section headers match technical reference template (.claude/templates/documents/technical_reference_template.md)
2. Table column structures correct per template
3. No fabrication (Verify EVERY claim in each file, trace to research files)
4. Evidence citations use actual file paths
5. Subsystem depth within budget (40-80 simple, 80-120 standard, 120-200 complex)
6. Extension Guide actionability — Section 13 includes specific file paths, interfaces, and registration points (not generic "add a file to directory X")
7. Cross-section consistency (integration points in Section 8 match subsystem references in Section 5)
8. No doc-only claims in Architecture (Section 2) or API & Integration (Section 8)
9. Stale documentation discrepancies surfaced in Tech Debt (Section 14)
10. Content rules compliance (tables over prose, no code reproductions, key signatures only)
11. All expected sections have content (no placeholders or empty sections)
12. No hallucinated file paths (verify parent directories exist)

VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found (list with specific fixes and suggested remediation)
```

### Lens-Based QA Agent Prompt Templates (Phase 6 — Final Document QA)

These templates replace the single Report Validation QA Agent Prompt. Each lens agent receives ONE of these prompts. The task-builder embeds the appropriate lens prompt in each checklist item per B2.

#### Standard Structural Lens Prompts (rf-qa)

```
Perform [LENS-NAME] validation of the assembled technical reference for [feature name].

QA phase: lens-[lens-name]
Report path: [report-path]
Template path: .claude/templates/documents/technical_reference_template.md
Output path: [output-path]
Fix authorization: false (report only — do NOT modify the document)

**ADVERSARIAL STANCE:** Assume this document has at least [N] errors in your lens area. Find them. (N = document_lines / 100, minimum 5)
```

**Note:** The full prompt body for each of the following lenses should replicate the structural format of the original Report Validation prompt (ADVERSARIAL STANCE, PROCESS, checklist, report format) but with the checklist focused ONLY on the lens:

1. **Template-Conformance Lens:** All 16 template sections present or N/A, frontmatter complete, section ordering matches template, no remaining placeholders or sentinel values.
2. **Internal-Consistency Lens:** IDs match across tables, counts agree between sections, cross-references resolve, no contradictions within the document, Table of Contents matches actual headers.
3. **Evidence-Quality Lens:** All claims cite file paths/line numbers, no unverified assertions, no hallucinated paths, every cited file actually exists, evidence is specific (not "the code does X").
4. **Completeness Lens:** Every topic from scope discovery appears in the output, no silently dropped items, every subsystem from research notes has a corresponding section.

#### Standard Content Lens Prompts (rf-qa-qualitative)

1. **Actionability Lens:** Extension Guide entries are specific enough to execute (file paths to create, interfaces to implement, registration points). Configuration instructions have exact parameter names. Every "how to" section is followable without reading other docs.
2. **Numbers-Metrics Lens:** Quantitative claims (file counts, line counts, component counts) are internally consistent and match between sections. Percentages add up. Tier budget adherence.
3. **Cross-Reference-Chain Lens:** Trace subsystem-to-API-to-config-to-example chains end-to-end. Every integration point in Section 8 maps to a subsystem in Section 5. Components in Section 7 reference actual stores/state defined in Section 6.
4. **Domain-Accuracy Lens:** Claims about the codebase match actual code. No aspirational features described as current. No planned architecture described as implemented. Configuration values match actual defaults.

#### Tech-Reference Domain-Specific Lens Prompts

1. **Code-Example-Accuracy Lens (rf-qa):** Every code snippet, inline code reference, and usage example in the tech reference must be verified against the actual source file at the cited path and line number. Flag any example that differs from actual code.
2. **API-Signature-Correctness Lens (rf-qa):** Every documented function signature, method signature, class constructor, and API endpoint must match the actual code. Parameter names, types, return types, and default values must be exact. Flag any mismatch.
3. **Configuration-Value-Verification Lens (rf-qa-qualitative):** Every configuration option documented (env vars, config file keys, default values, valid ranges) must be verified against actual configuration files and environment variable usage in the codebase. Flag any missing, extra, or incorrect config documentation.

#### Source-Document Fidelity Agent Prompt Template (Phase 6 Gate 4)

```
Perform source-document fidelity verification of the assembled technical reference for [feature name].

QA phase: source-fidelity
Tech reference path: [doc-path]
Assigned source code files: [list of source files/directories for this agent's partition]
Assigned fidelity lens: [one of: semantic-coverage | detail-preservation | phantom-coverage-detection | aspirational-content-detection | cross-reference-verification]
Output path: [output-path]
Fix authorization: false (report only)

**ADVERSARIAL STANCE:** Assume the tech reference contains at least 5 fidelity errors in your assigned lens area where the documentation diverges from the actual code. Find them.

**FOCUS:** You are assigned ONE fidelity lens. Apply ONLY your assigned lens checks below. Do not duplicate work from other fidelity agents' lenses.

PROCESS:
1. Read EACH assigned source code file carefully
2. Read the ENTIRE assembled tech reference
3. Apply your assigned lens checks (see below) to every relevant documented item
4. Write your fidelity report to [output-path]

FIDELITY LENS CHECKS (apply ONLY your assigned lens):
- **semantic-coverage:** Every subsystem, API endpoint, and configuration item documented in the tech reference can be traced to actual source code. Flag undocumented significant code features.
- **detail-preservation:** Function signatures, config defaults, error codes, and type shapes match the code exactly. Every documented behavior description matches actual code behavior.
- **phantom-coverage-detection:** File paths referenced in the tech reference must exist and contain what the doc claims. No fabricated or stale paths.
- **aspirational-content-detection:** No planned/aspirational features described as current functionality. No architecture described as implemented that is not yet built.
- **cross-reference-verification:** All cross-references between sections resolve correctly. Section references, table IDs, and internal links point to the right content.

Report format:
- PASS: No fidelity issues found (with evidence of thorough checking)
- FAIL: Issues found (list each with: documented claim, actual code, file path, line number, severity)
```

### Assembly Agent Prompt (rf-assembler — Document Assembly)

```
Assemble the final technical reference for [feature name] from synthesis files.

Component files (in order):
[ordered list of synth file paths]

Output path: [report-output-path]
Research directory: [research-dir-path]
Template path: .claude/templates/documents/technical_reference_template.md

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create the output file immediately with the document header:
   ---
   [frontmatter from template — fill in all fields, set status: "🟡 Draft"]
   ---
   # [Feature Name] Technical Reference
   **Purpose:** [one-sentence purpose]
   **Date:** [today]
   **Tier:** [Lightweight / Standard / Heavyweight]
   **Research files:** [count] codebase + [count] web research
   **Scope:** [directories/subsystems covered]

2. As you assemble each section, IMMEDIATELY write it to the output file using Edit.
   Do NOT accumulate the entire document in context and attempt a single write.

3. After each Edit, the file grows. This is correct behavior. Never rewrite from scratch.

Output format — follow the template section ordering exactly:
1. Overview (purpose, scope, key stats)
2. Architecture (diagrams, component relationships)
3. Directory Structure (file tree, organization)
4. Data Flow (data paths, transformations)
5. Subsystem Reference (one subsection per major subsystem)
6. State Management (if applicable — slices, stores, key fields)
7. Component Inventory (if applicable — component table)
8. API & Integration (endpoints, external connections)
9. Configuration (settings, environment variables)
10. Error Handling (error patterns, fallbacks)
11. Performance (metrics, optimization, caching)
12. Conventions (coding patterns, naming, style)
13. Extension Guide (how to add new functionality)
14. Tech Debt & Known Issues (documented issues, stale docs)
15. Verification (verification date, spot-check protocol)
16. Glossary (domain-specific terms)

Assembly rules:
1. Write the document header and frontmatter first
2. Assemble sections in template order — read each synth file and write its content into the correct position
3. Write each section to disk immediately after composing it — do NOT one-shot
4. Generate the Table of Contents from actual section headers after all sections are placed
5. Cross-check internal consistency:
   - Integration points in Section 8 match subsystem descriptions in Section 5
   - State slices in Section 6 match component usage in Section 5
   - Conventions in Section 12 match observed patterns in Section 5
   - Tech debt in Section 14 includes all CODE-CONTRADICTED and STALE DOC findings
   - Evidence Trail lists every research and synthesis file produced
6. Flag any contradictions between sections using: [CONTRADICTION: Section N claims X, Section M claims Y]
7. Ensure no placeholder text remains (search for [, TODO, TBD, PLACEHOLDER)

Content rules (non-negotiable):
- Tables over prose whenever presenting multi-item data
- No full source code reproductions — summarize with key signatures and file paths
- Use ASCII diagrams for architecture and component hierarchies, not prose descriptions
- Evidence cited inline: file.ts:123, ClassName.method()
- Conciseness over comprehensiveness — scannable, not exhaustive prose
- Every claim needs evidence — no file path or URL = belongs in Tech Debt or Open Questions
- Uncertainty marked explicitly with "Unverified" or "Open Question" markers

CRITICAL: You are assembling existing content, not creating new findings. Preserve fidelity
to the synthesis files. Add only minimal transitional text where needed for coherence.
Do NOT attempt full content validation — that is the QA agent's job. Focus on assembly
integrity: correct ordering, internal consistency, no placeholders, all components included.

Consolidation protocol (when consolidating existing docs into this tech reference):
1. Read each source document listed in the task's "Source Files to Consolidate" section
2. Map each source document's content to the corresponding template section(s)
3. Where source docs overlap, merge by keeping the most specific/recent information and noting conflicts
4. Add an Appendix: Document Provenance subsection listing each source doc with its path, original purpose, and which sections it contributed to
5. Zero content loss — every metadata piece and unique finding from source docs must appear in the final output or be explicitly noted as superseded
6. After assembly, the source docs should be candidates for archival (the tech reference replaces them)
```

---

## Output Structure

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

The final technical reference follows the template at `.claude/templates/documents/technical_reference_template.md`. The synthesis agents produce sections that are assembled into this format.

```markdown
---
[frontmatter from template]
---

# [Feature Name] Technical Reference

**Purpose:** [one-sentence purpose]
**Date:** [today]
**Tier:** [Lightweight / Standard / Heavyweight]
**Scope:** [directories/subsystems covered]

---

## Table of Contents
[Generated from section headers]

---

## 1. Overview
Purpose, scope, key statistics (file count, component count, dependency count).

## 2. Architecture
Component relationships, ASCII diagrams, integration map.

## 3. Directory Structure
File tree, organization rationale.

## 4. Data Flow
Data paths, transformations, state transitions.

## 5. Subsystem Reference
### 5.1 [Subsystem A]
[How it works, key files, key functions, data flow]
**Evidence:** [file paths, line numbers]

### 5.N [Subsystem N]
[...]

## 6. State Management (if applicable)
Slices, stores, key fields, subscription patterns.

## 7. Component Inventory (if applicable)
Component table: Name / Path / Purpose / Props / Dependencies.

## 8. API & Integration
Endpoints, external connections, inter-service communication.

## 9. Configuration
Settings, environment variables, feature flags.

## 10. Error Handling
Error patterns, fallbacks, recovery strategies.

## 11. Performance
Metrics, optimization strategies, caching patterns.

## 12. Conventions
Coding patterns, naming conventions, style rules.

## 13. Extension Guide
How to add new functionality following existing patterns.

## 14. Tech Debt & Known Issues
Documented issues, stale documentation findings, architectural risks.

## 15. Verification
Verification date, commit SHA, spot-check protocol.

## 16. Glossary
Domain-specific terms and definitions.

## Document History
[Initial entry and subsequent updates]

## Appendix: Document Provenance (if consolidating)
[Source materials, creation method, content mapping]
```

---

## Synthesis Mapping Table (Reference)

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

This is the standard mapping of synthesis files to template sections. Adjust based on feature complexity — for Lightweight tier, combine more sections per synth file. For Heavyweight tier, split further if needed (e.g., separate synth files per subsystem in Section 5).

| Synth File | Template Sections | Source Research Files |
|------------|-------------------|----------------------|
| `synth-01-overview-architecture.md` | 1. Overview, 2. Architecture | directory structure, integration summary, existing docs |
| `synth-02-directory-dataflow.md` | 3. Directory Structure, 4. Data Flow | directory structure, data/config research |
| `synth-03-subsystem-[name].md` | 5.N Subsystem Reference | per-subsystem research files |
| `synth-04-state-management.md` | 6. State Management | state management research |
| `synth-05-component-inventory.md` | 7. Component Inventory | directory structure, subsystem research |
| `synth-06-integration-config-perf.md` | 8. API & Integration, 9. Configuration, 10. Error Handling, 11. Performance | integration, config research, web research, error handling from subsystem research |
| `synth-07-conventions-extension-debt.md` | 12. Conventions, 13. Extension Guide, 14. Tech Debt | patterns observed across all research, web research, gaps log |

Adjust the mapping based on feature complexity. Backend features skip Section 6 (State Management) and Section 7 (Component Inventory). Small features can combine more sections per synth file.

---

## Synthesis Quality Review Checklist

**This checklist is enforced by both the rf-analyst and rf-qa agents** (see Phase 5 in the task phases). Items 1-5 and 7-9 overlap between both agents as intentional redundancy — independent agents checking the same criteria catch different failure modes. Item 6 differs: the rf-analyst checks architecture descriptions are backed by code-traced evidence, while the rf-qa checklist checks Extension Guide actionability (Section 13). Items 10-12 are rf-qa additions: content rules compliance, section completeness, and hallucinated file path detection.

The 9 criteria (used by rf-analyst):

1. Section headers match the technical reference template structure exactly
2. Tables use the correct column structure from the template
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and evidence (not vague descriptions)
5. Subsystem sections stay within depth budget (40-80 simple, 80-120 standard, 120-200 complex)
6. Architecture descriptions backed by code-traced evidence (not doc-only)
7. All cross-references between sections are consistent (e.g., integration points in Section 8 match subsystem descriptions in Section 5)
8. **No doc-only claims in Architecture or API sections.** Verify that Sections 2 and 8 only contain descriptions backed by code-traced evidence. If a synth file describes a component and the only evidence is a documentation file (no source code path), reject that claim and flag it as `[UNVERIFIED — doc-only]`
9. **Stale documentation discrepancies are surfaced.** Any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings from research files should appear in Tech Debt (Section 14), not silently omitted

The rf-qa agent's Synthesis Gate adds 3 additional checks (10-12): content rules compliance, section completeness, and hallucinated file path detection. If synthesis QA fails, findings are consolidated and a dedicated fix agent applies all fixes per the serialized fix protocol. Remaining unfixed issues trigger re-synthesis of the affected files.

---

## Assembly Process

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

The assembly step reads all synth files in order and produces the final technical reference. Follow these steps:

1. **Start with the template frontmatter** — fill in all fields from `.claude/templates/documents/technical_reference_template.md`. Set `status: "🟡 Draft"`, populate `created_date`, `source_references`, `tags`, etc.
2. **Write the document header** — the purpose block and document information table.
3. **Assemble sections in template order** — paste each synth file's content into the correct position, writing incrementally section by section (do NOT one-shot the entire document). Sections not assigned a synth file (15. Verification, 16. Glossary) get written directly during assembly from patterns observed in the synth files.
4. **Write the Table of Contents** — generate from actual section headers after all sections are placed.
5. **Cross-check internal consistency** — verify that:
   - Integration points in Section 8 match subsystem descriptions in Section 5
   - Components in Section 7 reference actual stores/hooks defined in Section 6
   - Conventions in Section 12 align with patterns observed in Section 5 subsystems
   - Tech Debt in Section 14 includes all `[CODE-CONTRADICTED]` and `[STALE DOC]` findings
   - Verification section (Section 15) has verification date and spot-check protocol
6. **Add Document Provenance** — if consolidating existing docs, add an `Appendix: Document Provenance` subsection documenting source materials. Zero content loss: every metadata piece from source documents must appear somewhere in the tech reference.

---

## Validation Checklist

Before presenting the technical reference to the user, validate against this checklist (this is encoded in the task file's Assembly phase):

- [ ] All template sections present (or explicitly marked as N/A with rationale)
- [ ] Frontmatter has all required fields from the template
- [ ] Total line count within tier budget (Lightweight: 400-600, Standard: 800-1200, Heavyweight: 1200-1800)
- [ ] No subsystem section exceeds 200 lines
- [ ] No full source code reproductions (interfaces, function bodies, CSS values)
- [ ] All file paths reference actual files that exist
- [ ] Section 6 (State Management) under 150 lines if included
- [ ] Tables use correct column structure from template
- [ ] No doc-sourced architectural claims presented as verified without code cross-validation tags
- [ ] Web research findings include source URLs for every external claim
- [ ] Gaps and questions file exists at `${TASK_DIR}gaps-and-questions.md`
- [ ] Document Provenance appendix present if consolidating existing docs
- [ ] Architecture diagrams use ASCII format, not prose descriptions
- [ ] All CODE-CONTRADICTED/STALE DOC findings surfaced in Tech Debt (Section 14)
- [ ] Verification section (Section 15) has verification date and spot-check protocol
- [ ] Every agent prompt includes its required protocol blocks (Incremental Writing for all, ADVERSARIAL STANCE for QA, Documentation Staleness for research)
- [ ] If a design spec, detailed requirements document, or comprehensive user description was provided as input, every feature/requirement described in the source is represented in the generated output (run section-by-section coverage check against the source)

---

## Content Rules (From Template — Non-Negotiable)

These rules come from the template's Content Size & Quality Guidelines. Every tech reference must follow them.

| Rule | Do | Don't |
|------|-----|-------|
| **Source code** | Summarize behavior in tables and prose | Reproduce TypeScript interfaces, function bodies, or CSS values |
| **Statistics** | State key numbers once in Section 1 Overview | Embed file counts, line counts throughout |
| **Architecture** | Use tables and ASCII diagrams | Multi-paragraph prose for what could be a table row |
| **Configuration** | List key settings with purpose and default | Reproduce entire config files |
| **State shape** | Table: Slice / Key Fields / Notable Behavior | Full TypeScript interface definitions |
| **Conventions** | List rules with brief rationale | Lengthy explanations of why each convention exists |
| **Subsystem depth** | 40-80 lines (simple), 80-120 (standard), 120-200 (complex) | >200 lines per subsystem (split into its own tech reference) |
| **File inventories** | Table: Path / Purpose / Key Exports | List files in paragraph form |
| **Data flow** | ASCII diagram or numbered step list | Multi-paragraph narrative |
| **Evidence** | Inline citations: `file.ts:123`, `ClassName.method()` | "The code does X" without pointing to where |
| **Uncertainty** | Explicit "Unverified" or "Open Question" markers | Present uncertain findings as verified facts |

---

## Critical Rules (Non-Negotiable)

These are SKILL-SPECIFIC content rules that apply across ALL phases. Violations compromise document quality.

Three execution-discipline rules (task-file-source-of-truth, maximize-parallelism, use-dedicated-tools) are enforced by the `/task` skill and do not appear here. The incremental-writing mandate is retained as Rule 9 below because it is a content-quality requirement specific to this skill's multi-agent research pipeline, not just an execution mechanism.

1. **Codebase is source of truth.** Web research supplements but never overrides verified code findings. Internal documentation is treated with the same skepticism as external sources unless code-verified.

2. **Evidence-based claims only.** Every finding must cite actual file paths, line numbers, function names, class names. No assumptions, no inferences, no guessing. If you can't verify it, mark it as "Unverified — needs confirmation."

3. **Gap-driven web research.** Do not web search everything up front. First investigate the codebase thoroughly (Phase 2), identify specific gaps, then target web research (Phase 4) at those gaps. This keeps web research focused and efficient.

4. **Documentation is not verification.** Internal documentation describes intent or historical state — NOT necessarily current state. A doc saying "X exists" does not prove X exists. Only reading actual source code proves it exists. Doc Analyst agents MUST cross-validate every architectural claim against actual code using the Documentation Staleness Protocol. Internal docs deserve the same skepticism as blog posts — they feel authoritative because they live in the repo, but they rot just as fast as external sources when the code changes around them.

5. **Preserve research artifacts.** Research and synthesis files persist after the technical reference is written. They serve as the evidence trail for all claims and enable future updates without starting from scratch. Do NOT delete research files, synthesis files, or the gaps log after assembly.

6. **Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. The synthesis phase relies on these connections.

7. **Report all uncertainty.** If something is unclear, ambiguous, or requires a judgment call, document it in Tech Debt (Section 14) with an `[UNVERIFIED]` tag and include it in the gaps-and-questions.md file. Do not silently pick one interpretation and present it as fact.

8. **Quality gates are mandatory and lens-based.** Quality agents MUST be spawned at all 4 gate points: after research (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative for multi-lens research verification), after synthesis (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative for multi-lens synthesis review), after assembly (lens-based QA with 6-12+ agents scaled by output size, each focused on a single quality dimension), and after lens-based QA (source-document fidelity gate with minimum 5 fidelity agents, scale to 6-8, reading source code + output). NO gate at any point may use fewer than 5 agents total. A gate with only 1-2 agents is PROHIBITED — single agents rubber-stamp large outputs. All gates use serialized fix authorization: all QA agents report only (fix_authorization: false), then a single fix agent applies consolidated findings, then a verification round confirms. These gates are not optional and cannot be skipped. Maximum 3 fix cycles per gate — after 3 failed cycles, HALT execution and ask the user for guidance. Do NOT convert unresolved findings into Open Questions.

9. **No one-shotting documents.** Agents must write incrementally as they discover information. The assembler must write the final document section by section. This is non-negotiable — one-shotting hits token limits and loses all accumulated work.

10. **Partitioning thresholds.** When >6 research files exist (Phase 3) or >4 synthesis files exist (Phase 5), spawn MULTIPLE analyst and QA instances in parallel, each with an `assigned_files` subset. This prevents context rot when any single agent would need to hold too many files in context.

11. **Default tier is Standard; upgrade when scope demands it.** If no tier is specified, default to Standard. If investigation reveals more complexity than expected (>8 major components, multiple subsystems with deep interconnections, extensive state management), upgrade to Heavyweight and note the upgrade reason in research notes. Never downgrade from a user-specified tier without explicit approval.

12. **Docs-vs-code has the same trust hierarchy as web-vs-code.** Rule 1 establishes that web research never overrides code. The same applies to internal documentation: if a doc describes an architecture that contradicts what the code shows, **the code is correct and the doc is stale**. Treat internal docs with the same skepticism as external blog posts unless code-verified.

13. **Extension Guide must be actionable.** Section 13 (Extension Guide) must include specific file paths to create, interfaces to implement, registration points to update, and minimal code skeletons. Generic instructions like "add a new file to the directory" are insufficient — the Extension Guide must be detailed enough that a developer can follow it without reading other documentation.

14. **Anti-orphaning rule.** Task-completion items (status update, Task Log entry, frontmatter update) MUST be checklist items within the final phase of the task file, not in a separate Post-Completion section. This ensures they are executed by the F1 loop and not orphaned.

15. **QA gates are checklist items, not prose.** Every QA gate specified in QA_GATE_REQUIREMENTS must appear in the generated task file as individual `- [ ]` checklist items following B2 self-contained pattern. Each lens agent gets its OWN checklist item (not a batch item like "spawn all lens agents"). The consolidation step, fix agent, and verification round each get their own items. A single Phase 6 QA gate will have 12-20+ checklist items (one per lens agent, one for consolidation, one for fix agent, one per verification agent, one for fidelity gate). QA gates described only in prose or comments are invisible to the F1 executor and will be skipped.

16. **Every agent prompt MUST include ALL mandatory protocol blocks:** Incremental File Writing Protocol (all agents), ADVERSARIAL STANCE (QA/analyst agents), Documentation Staleness Protocol (research agents). Missing protocol blocks are the most common generation defect — verify every prompt individually.

17. **Single-agent large-input prohibition.** No single agent may read more than ~1000 lines of input at any discovery, analysis, or extraction stage. Large inputs MUST be partitioned into slices, with one agent per slice spawned in parallel. The rf-task-researcher agent type is permitted per slice but not as a replacement for parallelism. Violations cause shallow coverage and defeat the Deep-tier depth guarantee. Exception: the rf-assembler agent is exempt from this threshold because assembly requires cross-section consistency that cannot be partitioned. The assembler reads synthesis files (not raw source), which are already distilled to manageable size by the synthesis phase. This exemption is intentional — partitioning the assembler would break cross-section coherence.

18. **No scope/cost-anxiety pauses during execution.** Once a task file begins executing (via /task or any execution loop), the executor MUST process every item sequentially to completion. It MUST NOT pause mid-execution to present the user with options like "stop here and review, or continue to phase N?" or to flag scope/cost/time concerns. Scope is established at task file creation time. Cost is committed when the user invokes execution. The only permitted mid-execution halts are: all items blocked by the same unrecoverable issue, phase-gate QA failing 3 fix cycles, or an item output fundamentally invalidating the rest of the task. "This will take a while" / "Phase N is expensive" / "the user might want to review" are NOT valid halt reasons. Pausing for these reasons violates the F1 loop discipline and the skill's trust model.

19. **Minimum agent count floors are non-negotiable.** No QA gate may spawn fewer agents than the minimums prescribed in QA_GATE_REQUIREMENTS. The absolute floor for ANY gate is 5 agents (across all agent types combined). Exception: Verification rounds (the post-fix confirmation step within a gate's serialized fix protocol) are sub-steps of a gate, not independent gates. They are exempt from the 5-agent floor. Verification rounds use a minimum of 2 agents (1 rf-qa + 1 rf-qa-qualitative) to confirm fixes were applied correctly. For the final assembled document QA gate (Phase 6), the floor is determined by output line count per the table in QA_GATE_REQUIREMENTS: <500 lines = 8 standard + 3 domain-specific = 11 agents minimum; 500-1500 lines = 8 standard + 3 domain = 11 agents minimum; 1500-3000 lines = 10 standard + 3 domain = 13 agents minimum (partition completeness lens across 2 agents with section ranges); >3000 lines = 12 standard + 3 domain = 15 agents minimum (partition completeness and evidence-quality lenses across 2 agents each). Task files with QA gates specifying fewer agents than these floors MUST be rejected during task-builder validation. This rule applies retroactively to all generated task files.

20. **rf-qa-qualitative is mandatory at ALL gates, not just the final gate.** The research gate (Phase 3) and synthesis gate (Phase 5) each MUST include at least 1 rf-qa-qualitative agent focused on depth/coherence quality. Structural checks (rf-analyst + rf-qa) alone miss qualitatively shallow research and incoherent synthesis. This agent catches the gap where work is structurally complete but content is surface-level.

---

## Research Quality Signals

### Strong Investigation Signals
- Findings cite specific file paths and line numbers
- Data flow traced end-to-end, not just entry points
- Integration points mapped with actual function signatures
- Existing patterns identified that can be reused
- Gaps are specific and actionable ("function X doesn't handle case Y")
- Doc-sourced claims carry verification tags ([CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED])
- rf-analyst completeness report shows PASS verdict
- rf-qa research gate shows PASS

### Weak Investigation Signals (Redo)
- Vague descriptions without file paths ("the system uses a plugin architecture")
- Assumptions stated as facts ("this probably works by...")
- Missing gap analysis (everything seems fine — unlikely for non-trivial systems)
- No cross-references between research files
- Doc-sourced claims without verification tags
- Doc-sourced architecture reported without code verification — if a research file describes pipelines, services, or components and the evidence trail only points to documentation files (no source code paths), the investigation is incomplete
- Quality gates fail repeatedly (>2 fix cycles indicates systematic research problems)

### When to Spawn Additional Agents
- A research agent flags a gap that's critical to the document
- Two agents' findings contradict each other — need a tie-breaker investigation
- The scope turns out larger than initially estimated
- A new subsystem is discovered during investigation that wasn't in the original plan
- Web research reveals patterns or APIs that need codebase verification

---

<!-- Artifact Locations section removed — Output Locations table (above) is the single source of truth for artifact paths. -->

## Session Management

Session management is provided by the `/task` skill. When resuming a session:

1. Check for an existing task folder matching `TASK-TECHREF-*/` in `.dev/tasks/to-do/`
2. If found, invoke `/task` with the task file path inside the folder — it will resume from the first unchecked item
3. Check for existing research files in `${TASK_DIR}research/` for context
4. Read any analyst/QA gate reports to understand which gates have already passed

If no task file exists but research files are present, the user likely needs to restart from Stage A (scope discovery).

---

## Updating an Existing Tech Reference

When the user wants to update (not create) an existing tech reference:

1. Read the current document to understand what's already covered
2. Research only the changed/new areas (don't re-research everything)
3. Write new research files for the changes: `${TASK_DIR}research/update-[date]-[topic].md`
4. Edit the relevant sections of the tech reference in place
4.5. Spawn scoped QA on modified sections: 2 rf-qa fidelity agents (each reads the changed sections against actual source code to verify accuracy) + 2 rf-qa-qualitative (cross-section consistency of modified content + stale-claim detection in adjacent sections) + 1 rf-analyst (change-impact assessment: do the edits introduce contradictions with unchanged sections?), all with fix_authorization: true. Max 2 fix cycles. After 2 failed fix cycles, HALT: log remaining issues, present findings to user, ask for guidance before proceeding to steps 5-6. This is a lighter gate than the full Phase 6 QA but ensures no stale claims, broken cross-references, or fidelity gaps are introduced by the update.
5. Update the Verification section (Section 15) with the new verification date
6. Update Document History with what changed

