---
name: operational-guide
description: "Create or populate an Operational Guide document for a deployment, setup, or operations procedure. Use this skill when the user wants to create an operational guide, document an installation or setup process, populate an existing operational guide stub, or write a comprehensive operational guide following the project template. Trigger on phrases like 'create an operational guide for...', 'document this setup process', 'write an operational guide', 'populate this operational guide', 'ops guide for the deployment process', or when the user references a guide file that needs content following the operational guide template. Also trigger when the user says 'document this procedure' in the context of devops or operations."
---

# Operational Guide Creator

A skill for creating comprehensive Operational Guide documents for deployment, setup, and operations procedures. This skill uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts.

**How it works:** The skill performs initial scope discovery, then invokes the `/task-builder` skill to create an MDTM task file encoding all investigation and assembly phases. The skill then delegates execution to the `/task` skill, which processes the task file by marking items complete as it progresses. If context compresses or the session restarts, the skill re-reads the task file and resumes from the first unchecked item.

The skill follows a three-phase pipeline — Research → Synthesis → Assembly — to produce the final document. The output always follows the project template at `.claude/templates/documents/operational_guide_template.md`. The template is the schema — every operational guide must conform to it.

## Why This Process Works

Operational guides go stale when written from memory or existing docs. This skill forces every claim through codebase verification — parallel agents read actual source files, trace actual configurations, and document actual behavior with file paths and line numbers.

The MDTM task file provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off.

The multi-phase structure (scope discovery → deep investigation → **analyst + QA + qualitative verification** → web research → synthesis → **synthesis QA (analyst + QA + qualitative)** → assembly → **lens-based multi-agent QA** → **source-document fidelity gate**) prevents five common failure modes:
- **Context rot** — By isolating each investigation topic in its own subagent with its own output file, no single agent needs to hold the entire investigation in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning many parallel agents (each focused on one slice), the investigation goes deep on every aspect simultaneously rather than skimming across everything sequentially.
- **Hallucinated procedures** — By separating research (what exists) from synthesis (what it means) from assembly (the final guide), each phase can be verified independently. Synthesis agents only work from verified research files, not from memory or inference.
- **Uncaught quality drift** — Lens-based multi-agent QA replaces single-agent verification. At intermediate gates (research, synthesis), `rf-analyst` + `rf-qa` + `rf-qa-qualitative` agents verify completeness, evidence quality, and content depth independently. At the final gate, **9–11 lens-focused agents** (3–4 structural lenses via rf-qa + 3–4 content lenses via rf-qa-qualitative + 3 ops-guide domain-specific lenses) each evaluate one quality dimension, preventing rubber-stamping by any single agent. All QA agents report findings without fix authorization; a single fix agent then applies ALL collected fixes, followed by a verification round. This serialized fix protocol eliminates the churn caused by parallel fix authorization.
- **Source-document infidelity** — A dedicated source-document fidelity gate (minimum 2 agents) reads BOTH the original config/infrastructure source files AND the assembled operational guide, verifying that the guide faithfully represents actual system configuration. This catches semantic drift where the guide describes procedures differently from (or not matching) the actual config files and scripts.

The research artifacts persist in the task folder so findings survive context compression, can be re-verified later, and feed directly into the assembled operational guide.

### Variable Reference Block

Every skill invocation creates a self-contained task folder. Define these variables early and reference them throughout:

```
TASK_ID:     TASK-OPSGUIDE-<subject>-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/
SYNTHESIS:   ${TASK_DIR}synthesis/
QA:          ${TASK_DIR}qa/
REVIEWS:     ${TASK_DIR}reviews/
```

**Subject derivation:** `<subject>` is derived at task-folder-creation time from the procedure name and normalized to kebab-case (lowercase, hyphen-separated, 1-3 words, ~30 char soft cap). If no clean subject can be derived, fall back to the literal word `general`. Example TASK_ID: `TASK-OPSGUIDE-deploy-staging-20260408-140000`.

All intermediate artifacts (research files, synthesis files, analyst/QA reports) go into typed subfolders within `TASK_DIR`. The task file lives inside the task folder. When the task reaches "🟢 Done", the entire folder moves from `.dev/tasks/to-do/` to `.dev/tasks/completed/`.

---

## Input

The skill needs four pieces of information to produce an actionable operational guide. The first two are mandatory; the rest are optional but improve output quality.

1. **WHAT to document** (mandatory) — The procedure scope. Not just a system name — what operational procedure you want documented. This can come from:
   - A directory path (e.g., `infrastructure/docker/`, `ue_manager/`, `k8s/`)
   - An existing operational guide stub with a "Source Files" section
   - Both — the stub provides hints, the paths provide scope

2. **WHERE to write it** (mandatory) — The output location. If a stub exists, write there. If creating from scratch, follow the project convention: `docs/docs-product/ops/[name]-operational-guide.md`.

3. **WHY / what operational need** (strongly recommended) — What prompted this guide and who will use it. This shapes whether the guide emphasizes initial setup, day-to-day operations, disaster recovery, or migration procedures.

4. **WHAT kind of procedure** (optional, shapes depth) — Whether the guide covers a one-time setup, a repeatable deployment, an upgrade/migration path, or ongoing maintenance. This determines phase structure and verification depth.

### Effective Prompt Examples

**Strong — scope + output + operational context:**
> Create an operational guide for the Docker deployment at `infrastructure/docker/`. We need a repeatable setup procedure for new team members joining the project. Output to `docs/docs-product/ops/docker-deployment-operational-guide.md`.

**Strong — consolidation with clear scope:**
> Document the pixel streaming setup process covering `ue_manager/` and `infrastructure/`. There are existing partial docs scattered across `docs/pixel-streaming/` that should be consolidated. The guide should cover both the Docker host and UE host setup. Output to `docs/docs-product/ops/pixel-streaming-unified-setup-operational-guide.md`.

**Strong — update with specific focus:**
> Update the Kubernetes deployment guide at `docs/docs-product/ops/k8s-deployment-operational-guide.md`. We switched from raw manifests to Kustomize overlays in `k8s/` and the current guide is outdated. Focus on the overlay structure and ArgoCD integration.

**Weak — topic only (will work but produces broader, less focused results):**
> Write a guide.

**Weak — no procedure context (agents won't know what phases to document):**
> Document the setup.

**Weak — ambiguous scope (could be 3 different guides):**
> Create an operational guide for infrastructure.

### What to Do If the Prompt Is Incomplete

If the user provides only a vague request, **do NOT proceed immediately**. Ask the user to clarify using this template:

> I can create an operational guide for you. To make it focused and procedurally accurate, can you help me with:
>
> 1. **What procedure should this guide cover?** (e.g., "Docker deployment setup", "Kubernetes upgrade process", "pixel streaming configuration")
> 2. **Which directories/files are the primary scope?** (e.g., `infrastructure/docker/`, `k8s/`, `ue_manager/`)
> 3. **Who is the audience?** (e.g., "new team members setting up for the first time", "ops engineers doing routine deployments")
> 4. **Where should the guide be written?** (e.g., `docs/devops/01-docker-deployment-guide.md`)

Proceed once you have at least #1 and #2 answered clearly. Items #3-4 improve quality but aren't blockers — use project conventions for output location if not specified.

---

## Tier Selection

Match the tier to procedure scope. **Operational guides should almost always be 1,000 lines or under.** Guides are procedural — they tell you how to do something. Exhaustive reference material (architecture diagrams, fixture inventories, config deep-dives) belongs in a companion Technical Reference, not in the guide.

| Tier | When | Codebase Agents | Web Agents | Target Lines |
|------|------|-----------------|------------|--------------|
| **Lightweight** | Single-service setup, <5 config files, simple linear procedure | 1–2 | 0 | 200–400 |
| **Standard** | Multi-service setup, 5-15 config files, multiple phases | 3–5 | 0–1 | 400–700 |
| **Heavyweight** | Multi-machine setup, 15+ config files, complex integration, multiple environments | 5–10+ | 1–2 | 700–1,000 |

**Hard ceiling: 1,000 lines.** If the assembled guide exceeds 1,000 lines, that is a signal of content duplication or misplaced reference material — trim before presenting. Guides should NEVER reach 2,000 lines under any circumstances.

**Tier selection rules:**
- If unsure, start with Standard
- If the user says "thorough", "comprehensive", or "detailed" — always Heavyweight
- Only use Lightweight for single-service, linear procedures with minimal configuration
- If the procedure spans multiple machines, environments, or integration boundaries — always Heavyweight

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

All persistent artifacts go into the task folder at `${TASK_DIR}` (see Variable Reference Block above). Each invocation creates a self-contained folder under `.dev/tasks/to-do/`.

| Artifact | Location |
|----------|----------|
| **Task folder** | `${TASK_DIR}` (`.dev/tasks/to-do/TASK-OPSGUIDE-<subject>-YYYYMMDD-HHMMSS/`) |
| **MDTM Task File** | `${TASK_DIR}TASK-OPSGUIDE-<subject>-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research/research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Gap/question log (interim) | `${TASK_DIR}gaps-and-questions.md` |
| Analyst reports (research/synthesis gates) | `${TASK_DIR}qa/analyst-[lens]-report[-N].md` |
| QA reports (research/synthesis gates) | `${TASK_DIR}qa/qa-[gate]-[lens]-report[-N].md` |
| Qualitative reports (all gates) | `${TASK_DIR}qa/qa-qual-[gate]-[lens]-report[-N].md` |
| Consolidated findings | `${TASK_DIR}qa/qa-[gate]-consolidated-findings.md` |
| Lens QA reports (final document) | `${TASK_DIR}qa/qa-lens-[lens-name].md` |
| Source fidelity reports | `${TASK_DIR}qa/qa-source-fidelity-report[-N].md` |
| Final operational guide | `docs/docs-product/ops/[name]-operational-guide.md` |
| Template schema | `.claude/templates/documents/operational_guide_template.md` |

**File numbering convention:** All research, web, and synthesis files use zero-padded sequential numbers: `01-`, `02-`, `03-`, etc. This ensures correct ordering when listing files.

Check for existing task folders in `.dev/tasks/to-do/` before creating new ones — if prior research exists on the same procedure, read it first and build on it.

---

## Execution Overview

The skill operates in two stages:

**Stage A — Scope Discovery & Task File Creation (before the task file exists):**
1. Check for an existing task folder or research files (A.1)
2. Parse the user's request and triage into Scenario A vs B (A.2)
3. Perform scope discovery — map procedure files, plan assignments (A.3)
4. Write scope discovery results to a structured research notes file (A.4)
5. Review research sufficiency — mandatory gate (A.5)
6. Triage template selection (A.6)
7. Write BUILD-REQUEST.md and invoke `/task-builder` skill to create the MDTM task file (A.7)

**Stage B — Task File Execution (after the task file exists):**
8. Invoke `/task` with the task file path — it provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA, and session management
9. Resume: if returning to a session, invoke `/task` — it finds the `🟠 Doing` task file and resumes from the first unchecked item

Phase names within the task file:
- **Phase 1: Preparation** — Scope confirmation, template read, tier selection
- **Phase 2: Deep Investigation** — Parallel subagent investigation of procedure configs and scripts
- **Phase 3: Completeness Verification** — rf-analyst completeness verification + rf-qa research gate + rf-qa-qualitative research-depth verification (parallel)
- **Phase 4: Web Research** — Optional external research for tool documentation and best practices
- **Phase 5: Synthesis + Analyst + QA Synthesis Gate** — Template-aligned synthesis, then rf-analyst synthesis review + rf-qa synthesis gate + rf-qa-qualitative synthesis-coherence verification (parallel)
- **Phase 6: Assembly & Lens-Based QA & Source Fidelity** — rf-assembler produces final document, then lens-based multi-agent QA (9–11 agents across structural + content + domain lenses, serialized fix protocol), then source-document fidelity gate (minimum 2 agents reading original config/infra files + assembled guide)
- **Phase 7: Present to User & Complete Task** — Deliver document, present artifacts, offer companion document creation

If a task file already exists for this procedure (from a previous session), skip Stage A and invoke `/task` with the existing task file path to resume from the first unchecked item.

---

## Stage A: Scope Discovery & Task File Creation

### A.1: Check for Existing Task File

Before creating a new task file, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `TASK-OPSGUIDE-*/` folder related to this procedure
2. If found, read the task file inside (`${TASK_DIR}TASK-OPSGUIDE-*.md`) and check for unchecked `- [ ]` items
3. If unchecked items exist → skip to Stage B (resume execution)
4. If all items are checked → inform user that the operational guide is already complete, offer to re-run or update the existing guide
5. Check for existing research files in `${TASK_DIR}research/`:
   a. If `research-notes.md` exists with `Status: Complete` → skip to A.5 (review sufficiency, then build task file)
   b. If `research-notes.md` exists with `Status: In Progress` → read it, resume A.3 scope discovery from where it left off, then continue to A.4 to update the file
   c. If task folder exists but no `research-notes.md` → continue with A.3 but use the existing folder
6. If no task folder AND no research files exist → continue with A.2

### A.2: Parse & Triage the Operational Guide Request

Break the user's request into structured components:

- **GOAL**: What procedure needs to be documented (e.g., "Document Docker deployment", "Write Kubernetes setup guide", "Consolidate pixel streaming docs")
- **WHY**: What operational need prompted this — who will use it and for what (e.g., "New team members need repeatable setup steps", "Ops team needs disaster recovery runbook")
- **WHERE**: Specific directories, files, or infrastructure to focus on (e.g., `infrastructure/docker/`, `k8s/`, `ue_manager/`)
- **OUTPUT_TYPE**: The kind of operational guide needed (options: setup guide, deployment procedure, upgrade/migration guide, maintenance runbook, consolidation of existing docs)
- **PROCEDURE_SLUG**: A kebab-case identifier for the task folder (e.g., `docker-deployment`, `pixel-streaming-setup`, `k8s-deployment`)

**Triage into Scenario A or B:**

**Scenario A — Explicit request:** User provided most of: procedure scope, source directories, output location, operational context.
Example: "Create an operational guide for the Docker deployment at `infrastructure/docker/`. We need a repeatable setup procedure for new team members. Output to `docs/docs-product/ops/docker-deployment-operational-guide.md`."
→ Scope discovery confirms details and fills minor gaps. Lighter exploration.

**Scenario B — Vague request:** User provided a goal but few specifics.
Example: "Write a guide for the deployment process"
→ Scope discovery does broad exploration to map what exists, identify all infrastructure components, and plan investigation assignments.

**Do NOT interrogate the user with a list of questions.** Proceed with what you have and let scope discovery figure out the rest from the codebase. Only ask the user (via the clarification template in the Input section) if there's a genuine ambiguity about **intent** that can't be inferred from the codebase.

### A.3: Perform Scope Discovery

Use Glob, Grep, and codebase-retrieval to map the procedure's problem space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.

**Adjust depth by scenario:**
- **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, scan for related configs and scripts, identify gaps in what the user specified.
- **Scenario B**: Broad discovery — scan the full codebase for anything touching the procedure, map all relevant infrastructure, identify documentation, count files.

**Discovery steps (all 6 are mandatory):**

1. **Check for an existing operational guide stub** at the output location. If it has a "Source Files" or prerequisites section, read those source docs for context — but treat them as hints, not truth.

2. **Map the procedure's files and directories** — enumerate the relevant configs, scripts, and infrastructure files. Identify:
   - Primary source directories and key configuration files
   - Number of files and approximate complexity
   - Major phases or stages of the procedure (group files by function)
   - External integration points (services, tools, infrastructure outside the scope)

3. **Scan for existing documentation** about the procedure. Search for:
   - READMEs in the relevant directories
   - Existing guides or partial docs in `docs/devops/`, `docs/`, and related subdirectories
   - Architecture docs that describe the system being documented
   - Companion Technical References for the same feature/system (e.g., `TESTING_TECHNICAL_REFERENCE.md` for a testing guide) — note paths for deduplication during synthesis
   - Other operational guides in the same domain — identify related docs to avoid overlap

4. **Plan research assignments** — divide the procedure into research topics, one per major aspect. Each topic becomes a subagent assignment. Common assignment types for operational guides:
   - Infrastructure and configuration file inventory
   - Each major phase or stage of the procedure (1 assignment per phase)
   - Environment configuration / environment variables
   - Service dependencies and integration points
   - Scripts, automation, and tooling
   - Existing documentation review (if consolidating other docs)

   **Research assignment types** (use as many as the topic requires):

   | Type | Purpose | What the Agent Does |
   |------|---------|-------------------|
   | **Config Tracer** | Understand how configuration actually works | Read config files, trace variable propagation, follow references, document actual values |
   | **Doc Analyst** | Extract context from existing documentation | Read docs, **cross-validate every procedural claim against actual configs/scripts** (Documentation Staleness Protocol), note discrepancies and stale content |
   | **Integration Mapper** | Identify connection points | Map service ports, network topology, dependency chains, external service boundaries |
   | **Script Analyst** | Understand automation and tooling | Read scripts, trace execution flow, document arguments and expected behavior |
   | **Architecture Analyst** | Understand infrastructure design | Trace architectural decisions, component relationships, environment topology |

5. **Plan web research topics** — based on gaps identified in steps 1-4, identify specific external research needs: official tool documentation (Docker, Kubernetes, Terraform, etc.), best practices for the tools used in the procedure, known issues and version-specific gotchas.

6. **Determine synthesis file mapping** — decide which research files will feed which template sections. Use the mapping table from Step 5 as a starting point, adjusted based on actual research assignments planned.

**Select depth tier** based on config file count and procedure complexity:
- <5 config files, single-service, linear procedure → Lightweight
- 5–15 config files, multi-service, multiple phases → Standard
- 15+ config files, multi-machine, complex integration → Heavyweight

Compute `<subject>` from the procedure name using the rules in the Subject Derivation section. If no clean subject is derivable, use `general`. Create the task folder: `.dev/tasks/to-do/TASK-OPSGUIDE-<subject>-YYYYMMDD-HHMMSS/` with subfolders `research/`, `synthesis/`, `qa/`, `reviews/`

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

The file MUST be organized into these 7 categories (include all, mark as "N/A" if empty):

```markdown
# Research Notes: [PROCEDURE]

**Date:** [today]
**Scenario:** [A or B]
**Depth Tier:** [Lightweight / Standard / Heavyweight]

---

## EXISTING_FILES
[All files found during scope discovery: config files, scripts, infrastructure definitions, Docker/Compose/Helm/Terraform files, environment files, and related documentation. Per-file detail: path, purpose, key contents, approximate line count. Group by directory or subsystem.]

## PATTERNS_AND_CONVENTIONS
[Deployment patterns, naming conventions, environment management strategies, configuration propagation patterns, variable naming schemes, directory organization conventions observed. Cite specific files as evidence.]

## PROCEDURE_ANALYSIS
[Phases identified in the procedure, dependencies between phases, prerequisites that must be satisfied before each phase, ordering constraints, conditional branches (e.g., "if deploying to staging vs production"), rollback considerations. This is the procedural skeleton the guide will flesh out.]

## RECOMMENDED_OUTPUTS
[Planned output files: research files, synthesis files, final guide. Full paths and purposes. Include the expected sections of the final document and which research files feed each.]

## SUGGESTED_PHASES
[Planned investigation breakdown. For each planned research agent:
- Agent number, investigation type (Infrastructure/Config Investigator / Script/Automation Analyst / Environment/Variables Mapper / Service Dependencies Investigator / Procedure Phase Investigator / Existing Documentation Reviewer), topic
- Files/directories to investigate
- Output file path
- Web research topics identified from gaps
- Synthesis file mapping]

## TEMPLATE_NOTES
[Notes about which MDTM template to use and why. Which template sections apply to this procedure, which are N/A. Notes on how the operational guide template maps to the discovered procedure phases.]

## AMBIGUITIES_FOR_USER
[Genuine ambiguities about user intent that cannot be resolved from the codebase — e.g., unclear procedure scope, missing context about target environments, ambiguous boundaries between this guide and companion documents. If none, write "None — intent is clear from the request and codebase context."]
```

### A.5: Review Research Sufficiency (MANDATORY GATE)

**You MUST review the research notes before spawning the builder.** This is a quality gate — do NOT skip it.

Read `${TASK_DIR}research/research-notes.md` and evaluate:

1. Is the scope clearly bounded — are procedure boundaries defined (what this guide covers vs. what it does not)?
2. Are major procedure phases identified — are all stages of the process mapped with their ordering and dependencies?
3. Are integration points mapped — are external services, tools, and dependencies documented?
4. Is existing documentation inventoried — have related guides, READMEs, and architecture docs been found?
5. Are research assignments concrete enough for the task builder — does each have a topic, agent type, file list, and output path?
6. Is the template section mapping reasonable — do all template sections have a research source?
7. Is the tier selection appropriate for the config file count and procedure complexity?
8. Are companion documents identified — have tech references or other guides in the same domain been found to avoid content duplication?
9. If any doc-sourced claims appear in the research notes (e.g., from scanning existing documentation during scope discovery), are they tagged with `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`? Claims marked `[CODE-CONTRADICTED]` or `[UNVERIFIED]` must be flagged in AMBIGUITIES_FOR_USER.

**If sufficient** → proceed to A.6 (template triage).

**If insufficient** → either:
- Do additional scope discovery yourself and update the research notes file, OR
- Spawn one or more rf-task-researcher subagents in parallel with specific feedback about what's missing. For multiple gaps, spawn one agent per gap slice, not a single agent for all gaps

**Maximum 2 gap-fill rounds.** After 2 rounds, proceed with what's available and note remaining gaps in the research notes AMBIGUITIES_FOR_USER section.

Do NOT proceed to the builder with incomplete research notes. The builder cannot explore the codebase effectively — it relies on what you provide.

### A.6: Template Triage

Determine which MDTM template the task builder should use:

**Use Template 02 (Complex Task) when the work involves:**
- Discovery before building (investigating unknown infrastructure or procedures)
- Parallel subagent spawning
- Multiple phases with different activities (research, synthesis, assembly)
- Review/validation steps
- Conditional flows based on findings

**Use Template 01 (Generic Task) when the work involves:**
- Simple, sequential file creation
- Straightforward execution with no discovery
- Single-pass operations

**For operational guides, the answer is almost always Template 02** — the skill inherently involves discovery (Phase 1 research), parallel agents (Phases 1-3), synthesis (Phase 3), and validation (Phase 4). Even lightweight-tier guides benefit from the structured phase progression.

### A.7: Build the Task File

Write the BUILD_REQUEST to a file at `${TASK_DIR}BUILD-REQUEST.md`, then invoke the `/task-builder` skill. The task-builder reads the BUILD_REQUEST file, performs quality gates (rf-analyst + rf-qa), spawns the rf-task-builder agent to create the MDTM task file, and runs structural and qualitative validation internally. No manual verification step is needed — task-builder handles all validation and mediation.

**Step 1: Write `${TASK_DIR}BUILD-REQUEST.md`** using the Write tool with the following content:

```
# BUILD REQUEST

Source: skill-delegated
Calling Skill: operational-guide
Task Directory: ${TASK_DIR}
Research Notes: ${TASK_DIR}research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Create a comprehensive Operational Guide document for [GOAL] covering setup, configuration, and operational procedures. The guide will be written to [OUTPUT_PATH] following the operational guide template at `.claude/templates/documents/operational_guide_template.md`.

WHY: [WHY — what prompted this guide and what operational needs it serves]

TASK_ID_PREFIX: TASK-OPSGUIDE

DOCUMENTATION STALENESS WARNINGS:
[If scope discovery found any documentation that contradicts actual code/config, list the
specific claims and contradictions here. If none found during scope discovery, write:
"None found during scope discovery. Phase 2 agents will perform full documentation
cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags."]
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE: [01 or 02 — skill selects:
  01 = simple file creation, straightforward execution
  02 = needs discovery, testing, review, conditional flows, or aggregation]

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 1 (Preparation): L0 Setup — update task status, confirm scope, read template, select tier, create task folder with research/, synthesis/, qa/, reviews/ subfolders
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase configs, scripts, infrastructure and write findings files to ${TASK_DIR}research/
- Phase 3 (Completeness Verification): L4 Review/QA — spawn 2 rf-analyst (completeness + cross-validation lenses) + 2 rf-qa (evidence-quality + gap-detection lenses) + 1 rf-qa-qualitative (research-depth lens), all in parallel, all fix_authorization: false. Consolidate findings, then 1 rf-qa fix agent applies all fixes. Verification round (2 agents). Max 3 fix cycles. Partitioning >6 files doubles agent counts.
- Phase 4 (Web Research): L1 Discovery — agents explore external sources for best practices, tooling docs, and operational patterns (optional for operational guides — skip when the procedure is entirely internal with no external dependencies)
- Phase 5 (Synthesis + Multi-Agent QA Gate): L2 Build-from-Discovery — agents read research files and produce guide sections. Then spawn 2 rf-analyst (synthesis-accuracy + source-tracing lenses) + 2 rf-qa (structure + content-quality lenses) + 1 rf-qa-qualitative (synthesis-coherence lens), all fix_authorization: false. Consolidate findings, 1 fix agent, verification round. Max 2 fix cycles. Partitioning >4 files doubles counts.
- Phase 6 (Assembly & Lens-Based QA & Source Fidelity): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final operational guide. Then spawn lens-based QA: 3–4 rf-qa agents (one per structural lens: template-conformance, internal-consistency, evidence-quality, completeness) + 3–4 rf-qa-qualitative agents (one per content lens: actionability, numbers-metrics, crossref-chain-integrity, domain-accuracy) + 3 ops-guide domain lens agents (procedural-step-executability, command-accuracy, environment-variable-verification). ALL agents report-only (fix_authorization: false). Consolidate findings, then 1 rf-qa fix agent applies ALL fixes. Verification round (2 agents). After lens-based QA passes, spawn source-document fidelity gate: minimum 2 rf-qa fidelity agents reading config/infra source files + full guide to verify semantic coverage and detail preservation. Serialized fix protocol on fidelity findings.
- Phase 7 (Present & Complete): L0 Closeout — present guide to user, offer companion document creation, update task file status to Done. **CRITICAL: Phase 7 task-completion items (update status, set completion_date) MUST be inside Phase 7, NOT in a separate Post-Completion section. The anti-orphaning rule requires all items be within numbered phases.**

QA_INTENSITY: [lite / standard / full]  (per I22 — determined by tier mapping in Tier Selection section or user override)
QA_GATE_REQUIREMENTS: PER_PHASE
  **NOTE: Gate descriptions below specify FULL intensity agent counts. When QA_INTENSITY is lite or standard, the rf-task-builder applies I22 reductions via the QA Intensity Adaptation table in the Agent Prompt Templates section.**
  Gate 1: Research Completeness (Phase 3)
    - lite: 1 rf-qa (evidence + gaps) + 1 rf-qa-qualitative (depth + completeness) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 3 fix cycles. Partitioning >6 files doubles all counts.
  Gate 2: Synthesis Quality (Phase 5)
    - lite: 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 fix cycles. Partitioning >4 files doubles all counts.
  Gate 3: Lens-Based Document QA (Phase 6)
    - lite: 1 rf-qa (combined structural) + 1 rf-qa-qualitative (combined content) + 1 domain lens (procedural-step-executability) = 3 agents. Max 1 fix cycle.
    - standard: 3 rf-qa structural (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content (actionability, domain-accuracy, crossref-chain) + 1 domain lens (procedural-step-executability) = 7 agents. Max 2 fix cycles.
    - full: 6 rf-qa (4 structural + 2 domain) + 5 rf-qa-qualitative (4 content + 1 domain) = 11 agents. Max 3 fix cycles. Domain lenses: procedural-step-executability, command-accuracy, environment-variable-verification.
  Gate 4: Source-Document Fidelity (Phase 6, AFTER Gate 3)
    - lite: 1 rf-qa fidelity agent (combined semantic-coverage + phantom-detection lenses). Max 1 fix cycle.
    - standard: 2 rf-qa fidelity agents. Max 2 fix cycles.
    - full: 2 rf-qa fidelity agents (partition to 3-4 if source >1000 lines). Max 2 fix cycles.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + LINE_CEILING + SOURCE_FIDELITY
  SOURCE_FIDELITY: After lens-based QA passes, fidelity agents read original config/infrastructure source files alongside the assembled guide. They verify: semantic coverage (each config file and script investigated in research appears as a documented procedure step), detail preservation (specific ports, env vars, paths, and commands survive into the guide), and phantom coverage detection (guide claims about system behavior are verified against actual configs/scripts, not just research summaries).
  TEMPLATE_COMPLIANCE: All sections from operational guide template must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.
  LINE_CEILING: Guide must stay under 1,000 lines.

TESTING_REQUIREMENTS: N/A — documentation-only skill, no code produced, no tests applicable.

RESEARCH NOTES FILE:
${TASK_DIR}research/research-notes.md
Read this file FIRST for full detailed findings including: existing files, config inventories, procedure mappings, planned investigation assignments, synthesis mapping, and output paths.

SKILL CONTEXT FILE:
.claude/skills/operational-guide/SKILL.md
Read the "Step 2: Spawn Research Agents" section for the codebase research agent prompt. Read the "Step 4: Web Research" section for the web research agent prompt. Read the "Step 6: Spawn Synthesis Agents" section for the synthesis agent prompt. Read the "Research Analyst Agent Prompt" section for the rf-analyst completeness verification prompt. Read the "Research QA Agent Prompt" section for the rf-qa research gate prompt. Read the "Synthesis QA Agent Prompt" section for the rf-qa synthesis gate prompt. Read the "Report Validation QA Agent Prompt" section for the rf-qa report validation prompt. Read the "Assembly Agent Prompt" section for the rf-assembler prompt. Read the "Synthesis Mapping Table" section for the standard synth-file-to-guide-section mapping. Read the "Synthesis Quality Review Checklist" section for post-synthesis verification. Read the "Assembly Process" section for guide assembly steps. Read the "Validation Checklist" section for Phase 3 validation criteria. Read the "Content Rules" section for writing standards. Read the "Tier Selection" section for agent count and depth guidance. These must be embedded in the relevant checklist items per B2 self-contained pattern.

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process
Structure), you MUST create individual checklist items for EVERY research agent,
web research topic, synthesis file, and validation step. Do NOT create batch items
like "spawn all 5 research agents" or "run all web research" — each agent gets
its own checklist item. The research notes SUGGESTED_PHASES section contains
per-agent detail specifically to enable this granularity.

PROHIBITED_ACTIONS:
- Modifying source code
- Deleting or moving existing files without user confirmation
- Generating code snippets unless the guide explicitly documents code/config examples

SKILL PHASES TO ENCODE IN TASK FILE:
The task file MUST encode these phases as sequential checklist items. Each phase maps to a section of the skill's workflow. All items MUST follow the B2 self-contained pattern from the MDTM template.

Phase 1 — Preparation:
- Update task status to "🟠 Doing"
- Confirm scope with user (procedure name, output path, tier)
- Read the operational guide template at `.claude/templates/documents/operational_guide_template.md`
- Select tier (Lightweight / Standard / Heavyweight) based on procedure complexity
- Create the task folder at .dev/tasks/to-do/TASK-OPSGUIDE-<subject>-YYYYMMDD-HHMMSS/ with research/, synthesis/, qa/, reviews/ subfolders

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research agent (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md
- Each item specifies: investigation topic, type, files to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from SKILL.md) in each checklist item per B2
- Agent count follows tier guidance: Lightweight 1-2, Standard 3-5, Heavyweight 5-10+
- Agent types for operational guides include: Infrastructure/Config Investigator, Script/Automation Analyst, Environment/Variables Mapper, Service Dependencies Investigator, Procedure Phase Investigator (one per major phase), Existing Documentation Reviewer
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. For example, with 6 research assignments: spawn all 6 agents in one message, mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.

Phase 3 — Research Completeness Verification (MULTI-AGENT LENS GATE, PARALLEL):
- Spawn 5 agents IN PARALLEL, all with fix_authorization: false:
  1. `rf-analyst` (analysis_type: "completeness", lens: "completeness") — writes to `${TASK_DIR}qa/analyst-completeness-report.md`
  2. `rf-analyst` (analysis_type: "cross-validation", lens: "cross-validation") — writes to `${TASK_DIR}qa/analyst-cross-validation-report.md`
  3. `rf-qa` (qa_phase: "research-gate", lens: "evidence-quality") — writes to `${TASK_DIR}qa/qa-research-evidence-quality-report.md`
  4. `rf-qa` (qa_phase: "research-gate", lens: "gap-detection") — writes to `${TASK_DIR}qa/qa-research-gap-detection-report.md`
  5. `rf-qa-qualitative` (qa_phase: "research-depth", lens: "research-depth") — writes to `${TASK_DIR}qa/qa-research-depth-report.md`
  **ADVERSARIAL STANCE (all agents):** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
  Each agent independently reads research files and applies its lens-specific checklist. Embed full lens-specific prompts in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, DOUBLE agent counts: spawn 4 rf-analyst + 4 rf-qa + 2 rf-qa-qualitative = 10 agents. Each partition instance gets an assigned_files subset and writes to a numbered report. After all complete, merge reports: union of all findings, take more severe rating for items flagged by multiple partitions, deduplicate gaps.
- **Serialized fix protocol:** Read ALL reports. Consolidate all findings into `${TASK_DIR}qa/qa-research-consolidated-findings.md`. Spawn 1 rf-qa fix agent (fix_authorization: true) with the consolidated findings to apply ALL fixes. Then spawn a verification round (2 agents: 1 rf-qa + 1 rf-qa-qualitative, fix_authorization: false) to confirm fixes.
- Determine verdict from consolidated reports (PASS / FAIL).
- If PASS → proceed to Phase 4. If FAIL → fix ALL findings regardless of severity. (a) For findings fixable in existing research files, run serialized fix cycle (max 3 cycles). (b) For findings requiring new investigation, spawn targeted research agents (max 2 gap-fill rounds). These are independent budgets. After max cycles/rounds, HALT: log remaining issues in Task Log, present findings to user.
- Compile final gaps into ${TASK_DIR}gaps-and-questions.md
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY, optional for operational guides):
- One checklist item PER web research topic (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
- Each item specifies: topic, context from codebase findings, output file path
- **Optional for operational guides** — skip when the procedure is entirely internal with no external dependencies. Include when the guide covers: external tool integrations (Docker, Kubernetes, Terraform, etc.), third-party service configurations, industry-standard operational practices, or tooling that benefits from official documentation cross-referencing
- Web research targets should include (as applicable): official tool/service documentation, operational best practices and runbooks, infrastructure-as-code patterns, monitoring and alerting standards, security hardening guides from recognized sources

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Multi-Agent Synthesis QA Gate:
- One checklist item PER synthesis file (from research notes RECOMMENDED_OUTPUTS)
- Each item spawns an Agent subagent with the synthesis agent prompt from SKILL.md
- Each item specifies: research files to read, guide sections to produce, output path
- **CONDITIONAL SYNTHESIS THRESHOLD:** When >20 config files or scripts are inventoried in the research, synthesis agents MUST use a tabular summary format for inventories rather than listing each file individually. This prevents synthesis files from becoming unwieldy.
- After ALL synthesis agents complete, spawn 5 agents IN PARALLEL, all fix_authorization: false:
  1. `rf-analyst` (analysis_type: "synthesis-accuracy", lens: "synthesis-accuracy") — writes to `${TASK_DIR}qa/analyst-synthesis-accuracy-report.md`
  2. `rf-analyst` (analysis_type: "source-tracing", lens: "source-tracing") — writes to `${TASK_DIR}qa/analyst-synthesis-source-tracing-report.md`
  3. `rf-qa` (qa_phase: "synthesis-gate", lens: "structure") — writes to `${TASK_DIR}qa/qa-synthesis-structure-report.md`
  4. `rf-qa` (qa_phase: "synthesis-gate", lens: "content-quality") — writes to `${TASK_DIR}qa/qa-synthesis-content-quality-report.md`
  5. `rf-qa-qualitative` (qa_phase: "synthesis-coherence", lens: "synthesis-coherence") — writes to `${TASK_DIR}qa/qa-synthesis-coherence-report.md`
  **ADVERSARIAL STANCE (all agents):** Assume the work contains errors. Find what was missed.
  Embed full lens-specific prompts in each checklist item per B2.
- **Serialized fix protocol:** Consolidate findings into `${TASK_DIR}qa/qa-synthesis-consolidated-findings.md`. Spawn 1 rf-qa fix agent (fix_authorization: true). Verification round (2 agents). Max 2 fix cycles.
- **Parallel partitioning for large workloads:** When >4 synthesis files exist, DOUBLE counts: 4 rf-analyst + 4 rf-qa + 2 rf-qa-qualitative = 10 agents. Same partitioning pattern as Phase 3.
- If FAIL after max fix cycles → HALT: log all remaining issues in Task Log, present to user. Do NOT continue to Phase 6 without user approval.

Phase 6 — Assembly & Lens-Based QA & Source Fidelity (RF-ASSEMBLER + MULTI-AGENT LENS QA + FIDELITY GATE):

Step 6.1 — Assembly:
- Spawn a single DEDICATED `rf-assembler` agent (subagent_type: "rf-assembler") — NOT a general-purpose Agent — to assemble the final operational guide. Hand it: the list of synth file paths in order (as component_files), the guide output path [OUTPUT_PATH], the operational guide template from `.claude/templates/documents/operational_guide_template.md` (as output_format), the Assembly Process steps from SKILL.md (as assembly_rules), and the Content Rules from SKILL.md (as content_rules). The assembler reads each synth file and writes the guide incrementally section by section — header first, then sections in order, then Table of Contents, then cross-checks internal consistency. The assembler must be a single agent (NOT parallel) because cross-section consistency requires seeing the whole guide. Embed the full assembler prompt in the checklist item per B2.

Step 6.2 — Lens-Based Structural + Domain QA (PARALLEL, all fix_authorization: false):
- Always spawn 6 rf-qa agents (4 structural + 2 domain lenses) in parallel, one per lens:
  1. `rf-qa` (lens: "template-conformance") — all required sections present (Overview, Prerequisites, Phase 1-N, Verification, Troubleshooting, Maintenance & Operations, Quick Reference, Next Steps), correct ordering, no remaining placeholders/sentinels, Symptom/Cause/Solution table structure, Step X.Y numbering, inline verification checkpoints. Writes to `${TASK_DIR}qa/qa-lens-template-conformance.md`
  2. `rf-qa` (lens: "internal-consistency") — ports in Prerequisites match Phase steps and Quick Reference, env vars consistent across sections, commands match config examples, troubleshooting covers failure modes from procedures. Writes to `${TASK_DIR}qa/qa-lens-internal-consistency.md`
  3. `rf-qa` (lens: "evidence-quality") — all claims cite file paths/line numbers, no unverified assertions, no hallucinated paths, every command traces to actual script/config. Writes to `${TASK_DIR}qa/qa-lens-evidence-quality.md`
  4. `rf-qa` (lens: "completeness") — every config file and procedure phase from scope discovery appears in output, no gaps, no silently dropped items. Writes to `${TASK_DIR}qa/qa-lens-completeness.md`
  5. `rf-qa` (lens: "command-accuracy") — OPS-GUIDE DOMAIN LENS: commands, flags, and expected outputs match actual system behavior; verify against actual scripts/configs. Writes to `${TASK_DIR}qa/qa-lens-command-accuracy.md`
  6. `rf-qa` (lens: "environment-variable-verification") — OPS-GUIDE DOMAIN LENS: every env var referenced in the guide exists in actual config files (.env, docker-compose, k8s manifests); verify values match. Writes to `${TASK_DIR}qa/qa-lens-env-var-verification.md`
  **ADVERSARIAL STANCE (all agents):** Assume this document has at least 10 errors. Find them. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
  Embed full lens-specific prompts in each checklist item per B2. Each agent gets its own focused checklist — agents do NOT share a generic "check everything" prompt.

Step 6.3 — Lens-Based Content + Domain QA (PARALLEL, all fix_authorization: false):
- Always spawn 5 rf-qa-qualitative agents (4 content + 1 domain lens) in parallel, one per lens:
  1. `rf-qa-qualitative` (lens: "actionability") — every step specific enough to execute without interpretation; verification checkpoints testable with pass/fail. Writes to `${TASK_DIR}qa/qa-lens-actionability.md`
  2. `rf-qa-qualitative` (lens: "numbers-metrics") — all port numbers, timeout values, version numbers internally consistent and match configs; counts match between sections. Writes to `${TASK_DIR}qa/qa-lens-numbers-metrics.md`
  3. `rf-qa-qualitative` (lens: "crossref-chain-integrity") — trace end-to-end chains (prerequisite → phase step → verification checkpoint → troubleshooting entry) and verify every link exists. Writes to `${TASK_DIR}qa/qa-lens-crossref-chain.md`
  4. `rf-qa-qualitative` (lens: "domain-accuracy") — claims about system configuration match actual configs; claims about infrastructure match actual manifests; no aspirational features described as current. Writes to `${TASK_DIR}qa/qa-lens-domain-accuracy.md`
  5. `rf-qa-qualitative` (lens: "procedural-step-executability") — OPS-GUIDE DOMAIN LENS: every step can be executed as written; no missing prerequisites, no assumed tribal knowledge, rollback procedures exist for destructive operations, environment-specific values are parameterized. Writes to `${TASK_DIR}qa/qa-lens-procedural-executability.md`
  **ADVERSARIAL STANCE (all agents):** Assume this document has at least 10 errors. Find them.

Step 6.4 — Consolidated Fix Round (SERIALIZED):
- Read ALL lens reports from Steps 6.2 and 6.3. Consolidate into `${TASK_DIR}qa/qa-lens-consolidated-findings.md`.
- Spawn ONE rf-qa fix agent (fix_authorization: true) with the consolidated findings list. It applies ALL fixes to the guide. No other agent edits the file concurrently.
- After fix agent completes, spawn a verification round: minimum 2 agents (1 rf-qa + 1 rf-qa-qualitative, fix_authorization: false) to confirm fixes were applied correctly and no new issues introduced.
- If verification finds new issues, repeat Step 6.4 (max 3 cycles total). After 3 cycles, HALT: log remaining issues in Task Log, present to user.

Step 6.5 — Source-Document Fidelity Gate (PARALLEL, runs AFTER lens-based QA passes):
- Spawn minimum 2 rf-qa fidelity agents in parallel, each reading config/infrastructure source files + the FULL assembled guide:
  1. `rf-qa` (qa_phase: "source-fidelity", assigned_sources: "[first half of key config/script files]") — Writes to `${TASK_DIR}qa/qa-source-fidelity-report-1.md`
  2. `rf-qa` (qa_phase: "source-fidelity", assigned_sources: "[second half of key config/script files]") — Writes to `${TASK_DIR}qa/qa-source-fidelity-report-2.md`
  If total source file lines >1000, partition across 3–4 agents instead.
  Each fidelity agent checks:
  - **Semantic coverage** — for each config file and script investigated in research, does the guide contain corresponding procedure steps?
  - **Detail preservation** — source-specific details (port numbers, environment variable names, command flags, file paths) survive into the guide, not just high-level summaries
  - **Phantom coverage detection** — guide claims about system configuration are verified by reading actual config files, not just trusting research file summaries
  **ADVERSARIAL STANCE:** Assume this document misrepresents or omits at least 5 config details. Find them.
- **Serialized fix protocol on fidelity findings:** Consolidate fidelity reports, spawn 1 fix agent, verification round (2 agents). Max 2 cycles.
- After fidelity gate passes → proceed to Phase 7.

Phase 7 — Present to User & Complete Task:
- Present summary to user (guide location, key sections, procedure coverage, research file count, open questions)
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date
- `NON-BLOCKING` Suggest downstream skill: "This operational guide can be complemented by a Technical Reference document for deeper architecture details. You can create one using `/tech-reference` — the research files are already in place." Present the suggestion, mark this item complete immediately, and do NOT wait for a user response. This item does not gate task completion.

CRITICAL ANTI-ORPHANING RULE: Phase 7 task-completion items (update status, set completion_date) MUST be inside Phase 7, NOT in a separate Post-Completion section. Downstream offers are `NON-BLOCKING` — present them, mark complete, do not wait for user response.

TO BUILD A GOOD TASK FILE, YOU NEED:
- Goal and outputs (what to create, where, what format)
- Source files and context (what exists, what to reference) — from the research notes
- Phases and steps (logical breakdown of the work) — from the research notes SUGGESTED_PHASES + SKILL.md phase definitions
- Verification criteria (how to know each step is done)
- Dependencies (what's needed before each step)
The research notes file should cover most of this.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-OPSGUIDE-<subject>-[YYYYMMDD]-[HHMMSS]/TASK-OPSGUIDE-<subject>-[YYYYMMDD]-[HHMMSS].md

ESCALATION:
Since you are running as a subagent (not a teammate), you have NO team context.
Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage — these tools
will fail because there is no team. This overrides your agent definition's
Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
Instead, return the task file path as your final output.
- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
- **External docs/syntax** → use WebSearch
- **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, guide template, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-OPSGUIDE-<subject>-[YYYYMMDD-HHMMSS]/TASK-OPSGUIDE-<subject>-[YYYYMMDD-HHMMSS].md using PART 2 structure
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

1. **Invoke /task:** Use the Skill tool with `skill: "task"` and `args` set to the task file path produced by Stage A (e.g., `.dev/tasks/to-do/TASK-OPSGUIDE-deploy-staging-20260309-120000/TASK-OPSGUIDE-deploy-staging-20260309-120000.md`).
2. **Execution transfers to /task:** The /task skill reads the task file and processes each checklist item via the F1 loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT), spawning subagents as specified in B2 items and running phase-gate QA after each Phase 2+ completion.
3. **No additional execution logic needed:** All execution rules — F1 sequential processing, F2 prohibited actions, F4 modification restrictions, F5 frontmatter protocol, error handling, session resumption — are provided by /task. This skill does not redefine them.
4. **Double QA is intentional:** The task file already contains skill-specific QA items (rf-analyst + rf-qa + rf-qa-qualitative at gates) and /task adds phase-gate QA on top. This results in intentional, acceptable double QA coverage at gate phases — skill-specific QA validates domain content while phase-gate QA validates structural completeness.

### What the Task File Must Contain

The task file from Stage A must embed all skill-specific context so that /task can execute it without reading this SKILL.md. Specifically:

- **Agent prompt templates** customized with the specific operational guide topics, source file paths, and output paths
- **Validation checklists and content rules** in ensuring clauses (e.g., "ensuring all CLI commands are verified against actual scripts")
- **Output paths and file naming conventions** for research files, synthesis files, and the final assembled document
- **Prohibited actions for this skill:** research agents READ code, configs, and scripts — they do not modify them; do not invent file paths; do not fabricate content; do not delete research artifacts after assembly
- **All phase-specific context** so each B2 item is self-contained and independently executable

**CRITICAL:** /task does NOT read this SKILL.md during execution. ALL skill-specific instructions, domain rules, quality criteria, and prohibited actions must be baked into the task file during Stage A.

---

## Agent Prompt Templates

These templates are provided to the task builder (in the BUILD_REQUEST) so it can embed them in the task file's self-contained checklist items. The builder should customize each instance with the specific procedure, files, and output path.

**QA Intensity Adaptation (per Template 02 I22):**
- lite: Gate 3 combines to 3 agents:
  (1) rf-qa combined-structural: use template-conformance + internal-consistency + evidence-quality + completeness lenses
  (2) rf-qa-qualitative combined-content: use actionability + domain-accuracy + crossref-chain + numbers-metrics lenses
  (3) highest-value domain lens: procedural-step-executability
  Intermediate gates: 2 agents (1 rf-qa combined + 1 rf-qa-qualitative combined)
  Fidelity: 1 agent (combined coverage + phantom lenses). Max 1 fix cycle. 1 verification agent.
- standard: Gate 3 uses 7 agents:
  3 rf-qa structural: template-conformance, internal-consistency, evidence-quality
  3 rf-qa-qualitative content: actionability, domain-accuracy, crossref-chain
  1 domain lens: procedural-step-executability
  Intermediate gates: 3 agents (1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative)
  Fidelity: 2 agents. Max 2 fix cycles. 2 verification agents.
- full: Use all prompts below as-is (current behavior, no changes).

### Codebase Research Agent Prompt

```
Research this aspect of [procedure name] and write findings to [output-path]:

Topic: [topic description]
Investigation type: [Procedure Tracer / Config Analyst / Dependency Mapper / Doc Analyst / Architecture Analyst]
Files to investigate: [list of files/directories]
Procedure root: [primary directory]
Research question context: [the overall procedure being documented, for context]

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
1. Read the actual source files — understand what each file does, what it configures, what it depends on
2. Trace data flow — how does configuration enter, propagate, and affect the running system?
3. Document the public interface — what commands, endpoints, ports, and configuration surfaces exist?
4. Identify patterns — what conventions, patterns, or architectural decisions are evident?
5. Check for edge cases — error handling, fallbacks, environment-specific behavior
6. Note dependencies — what does this procedure depend on? What depends on it?
7. Flag gaps — what is missing, broken, undocumented, or unclear? What needs further investigation?
8. Note integration opportunities — where could automation, monitoring hooks, or operational tooling be added to improve this procedure?

CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Code describes CURRENT state. These frequently diverge.
When you encounter documentation that describes a deployment procedure, service configuration, infrastructure setup, or operational workflow, you MUST cross-validate structural claims against actual code before reporting them as current:

1. **Services/infrastructure described in docs:** Verify the configuration files, scripts, and service definitions actually exist in the repo. Use Glob to check. If a doc says "Docker config at infrastructure/docker/X/", verify the path exists. If it doesn't, the doc is STALE.

2. **Commands/scripts described in docs:** Verify the referenced scripts exist and check their actual arguments/behavior match the documentation.

3. **File paths mentioned in docs:** Spot-check that referenced files exist.

4. **Port mappings/endpoints described in docs:** Cross-check against actual configuration files (docker-compose, .env, k8s manifests).

For EVERY doc-sourced operational claim, mark it with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source/config at [file:line]
- **[CODE-CONTRADICTED]** — actual config/script shows different behavior (describe what it actually shows)
- **[UNVERIFIED]** — could not find corresponding file; may be stale, planned, or in a different repo

Claims marked [UNVERIFIED] or [CODE-CONTRADICTED] MUST appear in the Gaps and Questions section.

Output Format:
- Use descriptive headers for each file or logical group
- Include actual configuration values, port numbers, command syntax, and file paths (not reproduced code blocks — summaries with key settings)
- Note any anomalies, tech debt, or surprising behavior
- End each section with a "Key Takeaways" bullet list
- End the file with:
  ## Gaps and Questions
  - [things that need further investigation or are unclear]
  - [all UNVERIFIED and CODE-CONTRADICTED claims from docs]

  ## Stale Documentation Found
  - [list any docs that describe procedures/configs that no longer exist]

  ## Summary
  [3-5 sentence summary of what you found]

Be thorough. Be specific. Only document what you verified in the source. Do not guess or infer.
Documentation is NOT verification — reading a doc that says "run X" does not verify X works.
Only reading the actual script/config verifies current behavior.
```

### Web Research Agent Prompt

```
Research this topic externally and write findings to [output-path].

Topic: [specific external research topic]
What we already know from codebase: [brief summary of relevant codebase/config findings]
Procedure context: [the overall procedure being documented]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for official documentation for tools, platforms, and services used in the procedure
2. Search for best practices, configuration guides, and troubleshooting references
3. Search for known issues, version-specific gotchas, and upgrade paths
4. For each finding, document:
   - Source URL
   - Key information extracted
   - How it relates to our configuration findings
   - Whether it supports, extends, or contradicts what we found in configs
5. Rate source reliability (official docs > well-maintained repos > blog posts > forum answers)

Output Format:
- Use descriptive headers for each research area
- Always include source URLs
- Mark relevance: HIGH / MEDIUM / LOW for each finding
- End with:
  ## Key External Findings
  [Bullet list of the most important discoveries]

  ## Recommendations from External Research
  [How external findings relate to the procedure's implementation]

IMPORTANT: Our configuration files are the source of truth. External research adds official documentation context but does not override verified configuration behavior.
```

**Common web research topics for operational guides:**
- Official documentation for tools/platforms (Docker, Kubernetes, Terraform, Helm, ArgoCD, cloud providers)
- Best practices for deployment/infrastructure patterns (production checklists, blue-green/canary, IaC conventions)
- Known issues and version-specific gotchas (breaking changes, compatibility matrices, migration guides)
- Security hardening guides (CIS benchmarks, secrets management, TLS/mTLS, RBAC patterns)
- Troubleshooting references (official troubleshooting guides, error databases, diagnostic commands)

### Doc Consolidation Agent Prompt

```
Consolidate existing documentation about [procedure name] and write findings to [output-path].

Source documents to consolidate: [list of document paths]
Procedure context: [the overall procedure being documented]
Output path: [output-path]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you read and consolidate each source document, IMMEDIATELY append findings to the file
3. Never accumulate and one-shot

Consolidation Protocol:
1. Read ALL source documents listed above
2. For each source document, extract:
   - Unique operational information (procedures, commands, configurations)
   - Overlap with other source documents (note which docs cover the same ground)
   - Stale or contradictory information (cross-validate against actual configs/scripts)
3. Map each piece of content to the operational guide template section where it belongs
4. For overlapping content, identify the most current and code-verified version
5. Tag every doc-sourced claim with [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED]

Output Format:
- Use descriptive headers for each source document reviewed
- Include a mapping table: Source Doc Section → Target Guide Section
- Note all contradictions between source documents
- Note all stale content found
- End with:
  ## Consolidation Summary
  - Documents reviewed: [count]
  - Unique content items extracted: [count]
  - Overlapping content merged: [count]
  - Stale/contradicted items found: [count]

  ## Content Mapping
  | Source Document | Source Section | Target Guide Section | Status |
  |----------------|---------------|---------------------|--------|

  ## Gaps and Questions
  - [things that need further investigation or are unclear]
```

### Synthesis Agent Prompt

```
Read the research files listed below and synthesize them into template-aligned sections for an Operational Guide document.

Research files to read: [list of paths]
Template sections to produce: [section numbers and names]
Output path: [synth file path]
Companion documents: [list companion doc paths identified in Step 1.4]
Procedure context: [brief description of the procedure being documented]

RULE 0 — READ THE TEMPLATE FIRST:
Before synthesizing anything, read `.claude/templates/documents/operational_guide_template.md` in full. The template is the schema — every header, table structure, callout convention, and section ordering in the template is mandatory. Do not deviate from it.

Rules:
1. Follow the template structure exactly — use the same headers, tables, and section format
2. Every fact must come from the research files — do not invent, assume, or infer
3. Use tables over prose for multi-item data (port lists, environment variables, service endpoints, troubleshooting Symptom/Cause/Solution)
4. Do not reproduce full configuration files or script bodies — summarize with key settings and commands
5. Include "Expected Output" blocks after commands where the output matters for verification
6. Use callout conventions: > **Note:**, > **Important:**, > **CRITICAL:**, > **Tip:**
7. Reference actual file paths from the research — not hypothetical ones
8. Use Step X.Y numbering within phases (e.g., Step 1.1, Step 1.2)
9. Include inline verification checkpoints at the end of each phase — a numbered checklist of observable conditions that confirm the phase succeeded
10. **Documentation-sourced claims require verification status.** If a research file reports a finding from documentation, check whether it carries a [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED] tag. Per-tag handling:
    - **[CODE-VERIFIED]** claims may be presented as current procedure — these are confirmed by actual config/script reads
    - **[CODE-CONTRADICTED]** claims must be corrected to match what the actual config/script behavior shows. Present the code-verified truth, not the stale documentation claim. Note the discrepancy in the Troubleshooting section as a "Documentation Staleness" entry
    - **[UNVERIFIED]** claims must be flagged as uncertain and EXCLUDED from procedure steps, commands, and expected outputs. Place them in a "Requires Verification" callout or in the Open Questions appendix — never in the step-by-step procedure as if they are fact
11. **Never describe procedures from docs alone.** When writing phase steps, commands, and expected outputs, ONLY use findings that trace back to actual config/script reads. If the only evidence for a command, port, path, or config value is a documentation file, it MUST be flagged as [UNVERIFIED — doc-only, no code confirmation] and excluded from the step-by-step procedure.
12. **When research files contradict each other**, note the contradiction explicitly and present the finding with stronger evidence (code reads > config reads > documentation reads > web research). Flag the weaker claim with its source so the reader can investigate.
13. **Web research findings must be explicitly marked as external context**, with source URLs. Never present web-sourced information as if it came from the codebase. Use a > **External Reference:** callout.
14. **CONTENT DEDUPLICATION** — Do NOT reproduce content that already exists in companion documents. Instead, write a brief summary (1-3 sentences) of the topic and link to the companion document for details. Specifically:
    - Architecture diagrams, fixture inventories, and exhaustive component analysis → link to the Technical Reference
    - Detailed config deep-dives and env var explanations → link to the Technical Reference
    - The guide is PROCEDURAL (how to do X). The tech reference is EXHAUSTIVE (what X is and how it works). Keep them separate.

SELF-CONTAINED DEPTH BUDGETS — Target line ranges per section type to keep the guide concise and procedural:
- Overview + Prerequisites: 30-50 lines (brief context, then a Pre-Flight Checklist table)
- Each Phase section: 80-150 lines (steps with commands, expected outputs, verification checkpoint)
- Verification section: 40-80 lines (end-to-end verification steps with pass/fail criteria)
- Troubleshooting section: 50-100 lines (Symptom/Cause/Solution table, doc staleness entries)
- Quick Reference: 30-50 lines (service URLs, key paths, common commands — self-contained)
- Maintenance & Operations: 30-60 lines (routine tasks, backup procedures, log locations)
- Next Steps + Appendix: 20-40 lines (links to related guides, open questions)
If a section is growing beyond its budget with reference material, that material belongs in the companion Technical Reference — summarize and link instead. Target total assembled guide length under 1,000 lines.

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
Perform a completeness verification of all research files for [procedure].

Analysis type: completeness-verification
Research directory: [research-dir-path]
Research notes file: [research-notes-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: [output-path]

Your job is to independently verify that research agents produced thorough, evidence-based findings
before downstream synthesis begins. You are the analytical quality gate — be rigorous.

PROCESS:
1. Read the research-notes.md file to understand the planned scope (EXISTING_FILES, SUGGESTED_PHASES, PROCEDURE_ANALYSIS)
2. Use Glob to find ALL research files in the research subfolder (files matching [NN]-*.md)
3. Read EVERY research file — do not skip any
4. Apply the 8-item Research Completeness Verification checklist below
5. Write your report to [output-path]

CHECKLIST:
1. Config inventory audit — every config file, docker-compose, Dockerfile, Makefile, Helm chart, Terraform file, and script from scope is covered by at least one research file
2. Procedure phase tracing — every phase of the operational procedure (setup, deploy, verify, maintain) has been investigated with actual commands and expected outputs traced
3. Integration point coverage — all service-to-service connections, network boundaries, port mappings, and dependency relationships are documented with evidence
4. Environment variable catalogue — all environment variables, secrets references, and configuration parameters are inventoried with their sources (env files, docker-compose, k8s manifests, terraform vars)
5. Research assignment completion — every research assignment from SUGGESTED_PHASES produced an output file with Status: Complete
6. File integrity — no empty or truncated research files; each file has Summary, Key Takeaways, and Gaps and Questions sections
7. Depth-tier alignment — investigation depth matches the stated tier (Lightweight = key configs and happy path; Standard = full procedure with edge cases; Heavyweight = exhaustive with alternatives and failure modes)
8. Gap identification — all gaps unified, deduplicated, and severity-rated (Critical/Important/Minor)

VERDICTS:
- PASS: All checks pass, no critical gaps
- FAIL: Critical gaps exist (list each with specific remediation action)

Use the full output format from your agent definition (tables for coverage, evidence quality, staleness, completeness).
Be adversarial — your job is to find problems, not confirm things work.
```

### Research QA Agent Prompt (rf-qa — Research Gate)

```
Perform QA verification of research completeness for [procedure].

QA phase: research-gate
Research directory: [research-dir-path]
Analyst report: [analyst-report-path] (if exists, verify the analyst's work; if not, perform full verification)
Research notes file: [research-notes-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: [output-path]

You are the last line of defense before synthesis begins. Assume everything is wrong until you verify it.

IF ANALYST REPORT EXISTS:
1. Read the analyst's completeness report
2. Verify ALL of their coverage audit claims (verify the config files and procedure phases are actually covered)
3. Validate gap severity classifications (are "Critical" really critical? Are "Minor" really minor?)
4. Check their verdict against your own independent assessment
5. Apply the 10-item Research Gate checklist below

IF NO ANALYST REPORT:
Apply the full 10-item Research Gate checklist independently.

10-ITEM CHECKLIST:
1. File inventory — all research files exist with Status: Complete and Summary
2. Evidence density — Verify EVERY claim in each file — verify file paths and config values exist
3. Scope coverage — every key file from research-notes EXISTING_FILES examined
4. Documentation cross-validation — all doc-sourced claims tagged [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED], Verify EVERY CODE-VERIFIED claim
5. Contradiction resolution — no unresolved conflicting findings about the same config, port, or procedure step
6. Gap severity — Critical gaps block synthesis, Important reduce quality, Minor are lower priority but must still be fixed
7. Depth appropriateness — matches the tier expectation (Lightweight/Standard/Heavyweight)
8. Integration point coverage — service boundaries, network topology, port mappings, and dependency chains documented
9. Procedure completeness — every operational phase (prerequisites, setup steps, verification, troubleshooting, maintenance) has research backing
10. Incremental writing compliance — files show iterative structure, not one-shot

VERDICTS:
- PASS: Green light for synthesis
- FAIL: ALL findings must be resolved. Only PASS or FAIL — no conditional pass. List each finding with specific remediation.

Use the full QA report output format from your agent definition.
Zero tolerance — if you can't verify it, it fails.
```

### rf-analyst Synthesis Review Prompt

```
Perform a synthesis review of all synthesis files for [procedure].

Analysis type: synthesis-review
Research directory: [research-dir-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: [output-path]

Your job is to independently verify that synthesis agents produced accurate, template-aligned,
evidence-backed sections before assembly begins. You are the analytical quality gate — be rigorous.

PROCESS:
1. Use Glob to find ALL synthesis files in `${TASK_DIR}synthesis/` (files matching synth-*.md)
2. Read EVERY synthesis file — do not skip any
3. For each synthesis file, also read the source research files it references in `${TASK_DIR}research/`
4. Apply the 9-item Synthesis Quality Review checklist below
5. Write your report to [output-path]

9-ITEM CHECKLIST:
1. Template section headers match the expected format from the operational guide template — Overview, Prerequisites, Phase sections with descriptive names, Verification, Troubleshooting, Maintenance & Operations, Quick Reference, Next Steps
2. Tables use the correct column structure — Pre-Flight Checklist uses `# | Check | How to Verify`; Troubleshooting uses `Symptom | Cause | Solution`; Document Information uses `Field | Value`; config tables use `Setting | Value | File | Notes`
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and evidence (not vague descriptions) — every command, port, path, and config value traces to an actual config/script read
5. Phase steps use Step X.Y numbering (Step 1.1, Step 1.2) with commands and Expected Output blocks
6. Each phase ends with an inline verification checkpoint — a numbered checklist of observable conditions confirming the phase succeeded
7. All cross-references between sections are consistent (e.g., ports in Prerequisites match ports in Phase steps and Quick Reference; environment variables in Phase steps are documented in Prerequisites)
8. No doc-only claims in procedure steps or commands — verify that Phase sections only contain operational procedures backed by code-traced evidence. If a synth file describes a command, port, path, or config value and the only evidence is a documentation file (no source code/config path), reject that claim and flag it as [UNVERIFIED — doc-only]
9. Stale documentation discrepancies are surfaced — any [CODE-CONTRADICTED] or [STALE DOC] findings from research files should appear in the Troubleshooting section as "Documentation Staleness" entries or in Next Steps as open questions, not silently omitted

VERDICTS:
- PASS: All synthesis files meet quality standards, no critical issues
- FAIL: Issues found (list each with specific location, severity, and remediation action)

Use the full output format from your agent definition (tables for per-file analysis, evidence tracing, cross-section consistency).
Be adversarial — your job is to find problems, not confirm things work.
```

### Synthesis QA Agent Prompt (rf-qa — Synthesis Gate)

```
Perform QA verification of synthesis files for [procedure].

QA phase: synthesis-gate
Research directory: [research-dir-path]
Fix authorization: false (report findings only -- a separate fix agent applies all fixes via serialized protocol)
Output path: [output-path]

You are verifying that synthesis files are ready for assembly into the final operational guide.
You report findings only. Do NOT fix issues in-place.

PROCESS:
1. Use Glob to find ALL synth files (synth-*.md) in `${TASK_DIR}synthesis/`
2. Read EVERY synth file completely
3. Apply the 12-item Synthesis Gate checklist below
4. For each issue found:
   a. Document the issue (what, where, severity)
   b. Document the required fix
   c. Do NOT modify the synthesis files -- a dedicated fix agent will apply all consolidated findings
5. Write your QA report to [output-path]

12-ITEM CHECKLIST:
1. Section headers match the operational guide template (Overview, Prerequisites, Phase sections, Verification, Troubleshooting, Maintenance & Operations, Quick Reference, Next Steps, Appendix)
2. Troubleshooting entries use Symptom/Cause/Solution table structure — not prose descriptions
3. No fabrication (Verify EVERY claim in each file, trace each to a research file with actual config/script evidence)
4. Evidence citations use actual file paths from the codebase — no hypothetical or placeholder paths
5. Phase steps use Step X.Y numbering within phases (e.g., Step 1.1, Step 1.2) — not flat numbering across phases
6. Commands include Expected Output blocks where the output matters for verification
7. Doc-staleness handling correct — [CODE-CONTRADICTED] claims corrected to match actual config, discrepancies surfaced in Troubleshooting as "Documentation Staleness" entries; [UNVERIFIED] claims excluded from procedure steps and placed in "Requires Verification" callouts or Open Questions
8. Depth budgets respected — Overview+Prerequisites: 30-50 lines; each Phase: 80-150 lines; Verification: 40-80 lines; Troubleshooting: 50-100 lines; Quick Reference: 30-50 lines; Maintenance: 30-60 lines; Next Steps+Appendix: 20-40 lines
9. No doc-only claims in procedure steps or commands — every command, port, path, and config value must trace to actual file reads, not documentation alone
10. Each phase ends with an inline verification checkpoint — a numbered checklist of observable conditions confirming the phase succeeded
11. Content deduplication — no reproduction of content that belongs in a companion Technical Reference; architecture, fixture inventories, and config deep-dives are summarized and linked, not reproduced
12. No hallucinated file paths (verify parent directories exist via Glob or Read)

VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found (list with specific fixes and suggested remediation)
```

### Assembly Agent Prompt (rf-assembler)

```
Assemble the final operational guide for [procedure] from synthesis files.

Component files (in order):
[ordered list of synth file paths]

Output path: [guide-output-path]
Research directory: [research-dir-path]
Template path: .claude/templates/documents/operational_guide_template.md

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create the output file immediately with the frontmatter and header:
   ---
   status: "🟡 Draft"
   created_date: [today]
   depends_on: []
   tags: []
   ---
   # [Guide Title]

2. As you assemble each section, IMMEDIATELY write it to the output file using Edit.
   Do NOT accumulate the entire guide in context and attempt a single write.

3. After each Edit, the file grows. This is correct behavior. Never rewrite from scratch.

Output format — the final guide MUST contain these sections in this order:
1. Frontmatter (status, created_date, depends_on, tags)
2. Preamble blockquote (WHAT this guide covers, WHY it exists, HOW TO USE it, Target Host)
3. Document Information table (Guide Name, Guide Type, Target Environment, Maintained By, Last Verified Against System, Prerequisites Guide, Next Guide)
4. Numbered Table of Contents (generated from actual section headers after all sections placed)
5. Overview (purpose, scope, what this guide achieves)
6. Prerequisites (required access, tools, prior guides completed, Pre-Flight Checklist)
7. Phase sections (Phase 1 through Phase N — each with numbered steps, commands with Expected Output blocks, inline verification checkpoint at end)
8. Verification (Health Checks, End-to-End Validation, All-Green Checklist)
9. Troubleshooting (Symptom/Cause/Solution tables — no prose-based problem descriptions)
10. Maintenance & Operations (scheduled tasks, log rotation, backup procedures, update process)
11. Quick Reference (service URLs, key file paths, common commands, config files — must be self-contained)
12. Next Steps (what to do after this guide, links to follow-on guides)
13. Document History (table with Date, Version, Author, Changes columns)
14. Appendix: Document Provenance (only if consolidating existing docs — see Consolidation Protocol below)

Assembly rules:
1. Write the frontmatter and header first, then the preamble blockquote and Document Information table
2. Assemble sections in order — read each synth file and write its content into the correct section position
3. Write each section to disk immediately after composing it — do NOT one-shot
4. Generate the Table of Contents from actual section headers after all sections are placed
5. Cross-check internal consistency:
   - Prerequisites mentioned in Phase 1 steps are listed in the Prerequisites section
   - Ports, paths, and service URLs in Prerequisites match those used in Phase steps and Quick Reference
   - Environment variables referenced in Phase steps are documented in Prerequisites or Overview
   - Verification checks at end of each Phase align with items in the Verification section
   - Troubleshooting entries cover failure modes mentioned in Phase steps
   - Quick Reference section contains every service URL, key path, and common command from the Phases
6. Flag any contradictions between sections using: [CONTRADICTION: Section A claims X, Section B claims Y]
7. Ensure no placeholder text remains (search for [, TODO, TBD, PLACEHOLDER)

Content rules (non-negotiable):
- Summarize configurations in tables (Setting | Value | File | Notes) — no full config file reproductions
- Show commands with Expected Output blocks immediately following each command
- Use Symptom/Cause/Solution tables for all troubleshooting entries — no prose-based problem descriptions
- Inline verification checkpoints at the end of every Phase — numbered checklist of observable conditions
- Tables over prose whenever presenting multi-item data (ports, paths, env vars, services)
- Evidence cited inline: file paths, config keys, actual values from codebase research
- Conciseness over comprehensiveness — scannable, not exhaustive prose
- Every operational claim needs evidence — no file path or verification = belongs in Open Questions
- Uncertainty marked explicitly with "Unverified" or "Requires Verification" callouts
- No full source code or script reproductions — summarize with key settings and file paths
- If a companion Technical Reference exists, link to it for architecture and config deep-dives instead of reproducing

Consolidation Protocol (when assembling from existing docs):
When the guide consolidates existing documentation, follow this protocol:
1. Read ALL source documents listed in the research notes before beginning assembly
2. Map every piece of content from source docs to the template section where it belongs
3. Merge overlapping content — when multiple sources describe the same procedure, use the most current and codebase-verified version
4. Create an "Appendix: Document Provenance" section at the end documenting:
   - Source document paths and their original titles
   - Which sections of the new guide each source contributed to
   - Any content from sources that was intentionally excluded (with rationale)
   - Date of consolidation
5. Ensure ZERO content loss — every piece of operational information from source documents must appear somewhere in the normalized guide (in the appropriate template section, in the appendix, or explicitly noted as excluded with rationale)
6. Flag any contradictions between source documents using [CONTRADICTION] markers

Hard ceiling: 1,000 lines. If the assembled guide exceeds 1,000 lines, that signals content
duplication or misplaced reference material — trim before presenting. Move exhaustive material
to a companion Technical Reference or link to existing docs.

CRITICAL: You are assembling existing content, not creating new findings. Preserve fidelity
to the synthesis files. Add only minimal transitional text where needed for coherence.
Do NOT attempt full content validation — that is the QA agent's job. Focus on assembly
integrity: correct ordering, internal consistency, no placeholders, all components included.
```

### Report Validation QA Agent Prompt (rf-qa — Template-Conformance Lens)

> **Note:** Under the lens-based QA architecture, this prompt is used as the **template-conformance structural lens** within Step 6.2. It runs with `fix_authorization: false` (report-only). Fixes are applied by a separate fix agent in Step 6.4 via the serialized fix protocol. Remaining lens agents use standard prompts from their agent definitions, customized with the lens-specific checklists from Steps 6.2 and 6.3. The builder embeds these checklists directly into each agent's B2 prompt.

```
Perform template-conformance lens QA on the assembled operational guide for [procedure].

QA phase: report-validation
Lens: template-conformance
Report path: [report-path]
Research directory: [research-dir-path]
Output path: [output-path]
Fix authorization: false (report findings only — fixes applied by dedicated fix agent)

Your ONLY job is the template-conformance lens. Do not attempt to check other quality dimensions.

PROCESS:
1. Read the ENTIRE assembled operational guide
2. Apply the 15-item Validation Checklist + 4 Content Quality Checks
3. For each issue: document it with location, severity, and suggested fix (do NOT fix in-place -- the serialized fix agent handles all fixes)
4. Write your QA report to [output-path]

15-ITEM VALIDATION CHECKLIST:
1. All 10 numbered template sections present (Overview, Prerequisites, Phase 1-N, Verification, Troubleshooting, Maintenance & Operations, Quick Reference, Next Steps) — or explicitly marked N/A with rationale
2. Frontmatter has all required fields from the template (status, created_date, depends_on, tags)
3. Preamble blockquote has WHAT, WHY, HOW TO USE, and Target Host
4. Document Information table has all 7 rows (Guide Name, Guide Type, Target Environment, Maintained By, Last Verified Against System, Prerequisites Guide, Next Guide)
5. Numbered Table of Contents present and matches actual section headers
6. Pre-Flight Checklist in Prerequisites section with specific, verifiable items
7. Each phase has inline verification checkpoint at end — numbered checklist of observable conditions
8. Verification section has Health Checks, End-to-End Validation, and All-Green Checklist subsections
9. Troubleshooting section uses Symptom/Cause/Solution tables — no prose-based problem descriptions
10. Quick Reference section is self-contained (usable without reading full guide) — includes service URLs, key paths, common commands
11. No full configuration file or script reproductions — key settings summarized in tables
12. All file paths reference actual files that exist (spot-check 5+ paths via Glob or Read)
13. Total line count within tier budget (Lightweight: 200-400, Standard: 400-700, Heavyweight: 700-1000) — hard ceiling 1,000 lines
14. No doc-sourced operational claims presented as verified without [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED] cross-validation tags
15. Web research findings include source URLs and are marked with > **External Reference:** callouts — never presented as codebase findings

CONTENT QUALITY CHECKS:
16. Table of Contents accuracy — every entry links to an actual section header, no orphaned or missing entries
17. Internal consistency — no contradictions between sections (e.g., port in Prerequisites matches port in Phase steps and Quick Reference)
18. Readability — scannable structure with tables, headers, bullets, callouts; no walls of prose
19. Actionability — a developer could execute the entire procedure from the guide alone, with commands, expected outputs, and verification steps at each phase

Report every issue you find with specific location and severity. Do NOT fix issues — report only.
```

### Ops-Guide Qualitative QA Agent Prompt (rf-qa-qualitative — Procedural-Step-Executability Lens)

> **Note:** This is the primary rf-qa-qualitative prompt template for operational guides. It serves as the procedural-step-executability domain lens in Step 6.3. Additional standard content lenses (actionability, numbers-metrics, crossref-chain-integrity, domain-accuracy) use the standard rf-qa-qualitative prompts from the agent definition, customized with the ops-guide document type and template path.

```
Perform procedural-step-executability lens QA on the assembled operational guide for [procedure].

QA phase: ops-guide-qualitative
Lens: procedural-step-executability
Document type: Operational Guide
Document path: [report-path]
Template path: .claude/templates/documents/operational_guide_template.md
Research directory: [research-dir-path]
Output path: [output-path]
Fix authorization: false (report findings only — fixes applied by dedicated fix agent)

Your ONLY job is the procedural-step-executability lens. Read the entire guide and verify it makes sense from an operations perspective.

LENS-SPECIFIC CHECKLIST:
1. Every step can be executed as written — no missing prerequisites, no assumed tribal knowledge
2. Steps are in correct operational order — no step references an output from a later step
3. Rollback procedures exist for every destructive operation (deleting data, stopping services, changing configs)
4. Environment-specific values are parameterized (not hardcoded IPs, not literal secrets)
5. Monitoring covers failure modes — every procedure that can fail has a corresponding troubleshooting entry
6. Prerequisites include ALL required access/permissions (SSH keys, cloud IAM roles, Docker group membership)
7. Expected Output blocks after commands show realistic output — not generic placeholders
8. Verification checkpoints at end of each phase test observable conditions — not "verify it works"
9. Quick Reference section is genuinely self-contained — usable without reading the full guide
10. No steps assume tools or services are running unless a prior step explicitly starts them
11. Content deduplication — no reproduction of material that belongs in a companion Technical Reference
12. Line count within tier budget (Lightweight: 200–400, Standard: 400–700, Heavyweight: 700–1000) — hard ceiling 1,000 lines

**ADVERSARIAL STANCE:** Assume this guide has at least 10 procedural errors. Find them. A real operator following these steps should not hit any undocumented failure. A verdict of 0 issues requires evidence you checked every step.

Report every issue with: section, step number, severity (CRITICAL/IMPORTANT/MINOR), description, recommended fix.
Do NOT fix issues — report only. Fixes are applied by the dedicated fix agent.
```

---

## Validation Checklist

> **Note:** Under the lens-based QA architecture, this validation is performed by multiple lens agents in Phase 6 Steps 6.2-6.5. This checklist is retained as a reference for what the lens agents collectively verify. It is NOT a separate manual validation pass.

Before presenting the operational guide to the user, validate against this checklist (this is encoded in the task file's guide-validation phase):

- [ ] All 10 numbered template sections present (Overview, Prerequisites, Phase 1-N, Verification, Troubleshooting, Maintenance & Operations, Quick Reference, Next Steps) — or explicitly marked N/A with rationale
- [ ] Frontmatter has all required fields from the template (status, created_date, depends_on, tags)
- [ ] Preamble blockquote has WHAT, WHY, HOW TO USE, and Target Host
- [ ] Document Information table has all 7 rows (Guide Name, Guide Type, Target Environment, Maintained By, Last Verified Against System, Prerequisites Guide, Next Guide)
- [ ] Numbered Table of Contents present and matches actual section headers
- [ ] Pre-Flight Checklist in Prerequisites section with specific, verifiable items
- [ ] Each phase has inline verification checkpoint at end — numbered checklist of observable conditions
- [ ] Verification section has Health Checks, End-to-End Validation, and All-Green Checklist subsections
- [ ] Troubleshooting section uses Symptom/Cause/Solution tables — no prose-based problem descriptions
- [ ] Quick Reference section is self-contained (usable without reading full guide) — includes service URLs, key paths, common commands
- [ ] No full configuration file or script reproductions — key settings summarized in tables
- [ ] All file paths reference actual files that exist (spot-check 5+ paths via Glob or Read)
- [ ] Total line count within tier budget (Lightweight: 200-400, Standard: 400-700, Heavyweight: 700-1000) — hard ceiling 1,000 lines
- [ ] No doc-only claims without [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED] tags
- [ ] All [CODE-CONTRADICTED] findings surface as adjusted procedures (not presented as current)
- [ ] Web research findings include source URLs and are marked with > **External Reference:** callouts — never presented as codebase findings

**Content quality checks (applied after structural validation):**

- [ ] Table of Contents accuracy — every entry links to an actual section header, no orphaned or missing entries
- [ ] Internal consistency — no contradictions between sections (e.g., port in Prerequisites matches port in Phase steps and Quick Reference)
- [ ] Readability — scannable structure with tables, headers, bullets, callouts; no walls of prose
- [ ] Actionability — a developer could execute the entire procedure from the guide alone, with commands, expected outputs, and verification steps at each phase
- [ ] Every agent prompt includes its required protocol blocks (Incremental Writing for all, ADVERSARIAL STANCE for QA, Documentation Staleness for research)
- [ ] If a design spec, detailed requirements document, or comprehensive user description was provided as input, every feature/requirement described in the source is represented in the generated output (run section-by-section coverage check against the source)
- [ ] Source-document fidelity gate passed — fidelity agents verified guide procedures match actual config/infra files
- [ ] Lens-based QA gate passed — minimum 9 lens agents (3 structural + 3 content + 3 ops-guide domain for <500 lines; 4+4+3 = 11 for 500–1000 lines) evaluated the guide
- [ ] All QA used serialized fix protocol — no parallel fix authorization on the same file
- [ ] All QA gates encoded as explicit `- [ ]` checklist items in the task file — no QA lives only in prose

---

## Content Rules (From Template — Non-Negotiable)

These rules come from the template's structure and conventions. Every operational guide must follow them.

| Rule | Do | Don't |
|------|-----|-------|
| **Configuration** | Summarize key settings in tables with purpose and default values | Reproduce entire config files, docker-compose.yml, or .env files |
| **Commands** | Show actual commands with Expected Output blocks | List commands without context or expected results |
| **Architecture** | Use tables and ASCII diagrams | Multi-paragraph prose for what could be a table row |
| **Troubleshooting** | Use Symptom/Cause/Solution tables | Prose-based descriptions of problems |
| **Port mappings** | Table: Port / Protocol / Direction / Purpose | Scatter port numbers throughout prose |
| **Environment variables** | Table: Variable / Purpose / Default / Required | Inline mention without context |
| **Verification** | Specific commands with expected status codes/output | Vague "check that it works" instructions |
| **Phase naming** | Descriptive: "Phase 1: Repository Setup" | Generic: "Phase 1: Step 1" |
| **Step numbering** | Step X.Y within phases (Step 1.1, Step 1.2) | Flat numbering across phases |
| **Callouts** | Use > **Note:**, > **Important:**, > **CRITICAL:**, > **Tip:** | Inline emphasis without callout structure |
| **Deduplication** | Link to companion Technical Reference or other existing docs for architecture, inventories, and exhaustive details | Reproduce content that already exists in another document in the same domain |
| **Tech Reference** | If a companion tech reference exists (e.g., `TESTING_TECHNICAL_REFERENCE.md` for a testing guide), reference it for architecture diagrams, fixture inventories, config deep-dives, and detailed component analysis | Include exhaustive reference material that belongs in the tech reference — the guide is procedural, the tech reference is exhaustive |
| **Doc staleness** | Tag doc-sourced claims with [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED]; surface contradictions as adjusted procedures | Present doc-only claims as verified without cross-validation tags |
| **Evidence** | Inline citations: `docker-compose.yml:42`, `scripts/deploy.sh`, `config/nginx.conf` | "The system uses X" without pointing to where |
| **Uncertainty** | Explicit "Unverified" or "Open Question" markers | Present uncertain findings as verified procedures |

**General content principles:**
- Tables over prose whenever presenting multi-item data
- Conciseness over comprehensiveness — the guide should be scannable, not exhaustive prose
- Every procedural claim needs evidence — if you can't cite a file path or config value, it belongs in Open Questions
- Prefer ASCII diagrams for visual relationships over paragraph descriptions

---

## Critical Rules (Non-Negotiable)

These are SKILL-SPECIFIC content rules that apply across ALL phases. Violations compromise document quality.

Three execution-discipline rules (task-file-source-of-truth, maximize-parallelism, use-dedicated-tools) are enforced by the `/task` skill and do not appear here. The incremental-writing mandate is retained as Rule 9 below because it is a content-quality requirement specific to this skill's multi-agent research pipeline, not just an execution mechanism. When other skills complete their /task integration, they will also use this reduced set.

1. **Codebase/config is source of truth.** For claims about current procedures, actual config files override documentation. Web research supplements but never overrides verified config findings.

2. **Evidence-based claims only.** Every finding must cite actual file paths, config values, command syntax. No assumptions as facts. If unverifiable, mark as "Unverified."

3. **Gap-driven web research.** Investigate configs first, identify specific gaps, then target web research at those gaps. This keeps web research focused and efficient.

4. **Documentation is not verification.** Internal docs describe intent or historical state — NOT necessarily current state. A doc saying "Service X runs on port Y" does not prove it. Only reading actual configs/scripts at that path proves it. Research agents MUST cross-validate every operational claim against actual code using verification tags. Any doc-sourced claim without a `[CODE-VERIFIED]` tag is treated as unverified.

5. **Preserve research artifacts.** Research and synthesis files persist after the guide is written. They serve as the evidence trail for all claims and enable future re-investigation without starting from scratch. Do NOT delete research files, synthesis files, or the gaps log after assembly.

6. **Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. The synthesis phase relies on these connections to build a coherent picture across investigation slices.

7. **Report all uncertainty.** If something is unclear, ambiguous, or requires a judgment call, document it in Open Questions. Do not silently pick one interpretation and present it as fact.

8. **Quality gates mandatory with minimum agent counts.** Post-research gate: minimum 5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative). Post-synthesis gate: minimum 5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative). Post-assembly gate: minimum 9–11 lens-focused agents (3–4 rf-qa structural + 3–4 rf-qa-qualitative content + 3 ops-guide domain lenses) plus source-document fidelity gate (minimum 2 agents). All gates use serialized fix protocol (report-only agents first, then single fix agent, then verification round). Max fix cycles: 3 for research, 2 for synthesis, 3 for final document, 2 for source-document fidelity. After max fix cycles, HALT and ask user for guidance. ALL findings must be resolved. NO gate uses fewer than 5 agents combined — this is the absolute floor. (Intermediate gates: 5 minimum. Output/final gates: 6 minimum before domain lenses are added.)

9. **No one-shotting documents.** Agents must write incrementally as they discover information. The assembler must write the final guide section by section. This is non-negotiable.

10. **Partitioning thresholds.** When >6 research files exist (Phase 3) or >4 synthesis files exist (Phase 5), spawn MULTIPLE analyst and QA instances in parallel, each with an `assigned_files` subset. This prevents context rot when any single agent would need to hold too many files in context.

11. **Default tier is Standard.** Unless the procedure is clearly a single-service linear setup (<5 config files) or a multi-machine complex integration (15+ config files), use the Standard tier.

12. **Docs-vs-code trust hierarchy.** Critical Rule 1 establishes that web research never overrides code. The same applies to internal documentation: if a doc describes a procedure that contradicts what the config files show, **the config is correct and the doc is stale**. This is especially dangerous because internal docs feel authoritative — but a doc written months ago about a deployment procedure may describe steps, services, and configurations that were changed, removed, or never implemented. Treat internal docs with the same skepticism as external blog posts unless code-verified.

13. **No content duplication.** Before synthesis, identify all existing documents in the same domain (companion tech references, other guides, architecture docs). During synthesis and assembly, never reproduce content that already exists in those documents — link to it instead. If a companion Technical Reference exists for the same feature/system, the guide defers to it for architecture details, fixture/component inventories, config deep-dives, and exhaustive analysis. The guide is procedural (how to do X); the tech reference is exhaustive (what X is and how it works internally).

14. **Guides must stay under 1,000 lines.** If the assembled guide exceeds 1,000 lines, that signals misplaced reference material or content duplication. Trim before presenting. Move exhaustive material to a companion tech reference or link to existing docs.

15. **Anti-orphaning — task-completion items inside final phase.** Task completion actions (update frontmatter, notify user, write completion log) are checklist items within the final phase of the task file, never in a separate Post-Completion section. This prevents them from being orphaned if context compresses after the last substantive phase.

16. **QA gates are checklist items, not prose.** Every QA gate specified in QA_GATE_REQUIREMENTS must appear in the generated task file as a `- [ ]` checklist item following B2 self-contained pattern. QA gates described only in prose or comments are invisible to the F1 executor and will be skipped.

17. **Every agent prompt MUST include ALL mandatory protocol blocks:** Incremental File Writing Protocol (all agents), ADVERSARIAL STANCE (QA/analyst agents), Documentation Staleness Protocol (research agents). Missing protocol blocks are the most common generation defect — verify every prompt individually.

18. **Single-agent large-input prohibition.** No single agent may read more than ~1000 lines of input at any discovery, analysis, or extraction stage. Large inputs MUST be partitioned into slices, with one agent per slice spawned in parallel. The rf-task-researcher agent type is permitted per slice but not as a replacement for parallelism. Violations cause shallow coverage and defeat the Deep-tier depth guarantee.

19. **No scope/cost-anxiety pauses during execution.** Once a task file begins executing (via /task or any execution loop), the executor MUST process every item sequentially to completion. It MUST NOT pause mid-execution to present the user with options like "stop here and review, or continue to phase N?" or to flag scope/cost/time concerns. Scope is established at task file creation time. Cost is committed when the user invokes execution. The only permitted mid-execution halts are: all items blocked by the same unrecoverable issue, phase-gate QA failing 3 fix cycles, or an item output fundamentally invalidating the rest of the task. "This will take a while" / "Phase N is expensive" / "the user might want to review" are NOT valid halt reasons. Pausing for these reasons violates the F1 loop discipline and the skill's trust model.

---

## Research Quality Signals

### Strong Investigation Signals
- Findings cite specific file paths and configuration values
- Data flow traced through config propagation (env vars, Docker compose, k8s manifests)
- Integration points mapped with actual ports, endpoints, and service names
- Existing scripts and automation identified with actual invocation examples
- Gaps are specific and actionable ("Dockerfile missing health check on line 42")
- Doc-sourced operational claims carry verification tags (cross-validated against actual configs/scripts)
- Quality gate reports show PASS with evidence trails linking claims to source files
- Analyst and QA reports agree on coverage completeness

### Weak Investigation Signals (Redo)
- Vague descriptions without file paths ("the system uses Docker")
- Assumptions stated as facts ("this probably restarts automatically")
- Missing gap analysis (everything works perfectly — unlikely for infrastructure)
- No cross-references between research files
- Doc-sourced operational claims without verification tags — if a research file describes deployment steps, service configs, or infrastructure and the evidence trail only points to documentation files (no actual config/script paths), the investigation is incomplete and must be redone with config/script cross-validation
- Quality gate reports show issues but no fix cycles were attempted
- Implementation steps use generic descriptions ("configure the service") instead of concrete commands

### When to Spawn Additional Agents
- A research agent flags a gap that is critical to operational correctness
- Two agents' findings contradict each other — need a tie-breaker investigation
- The scope turns out larger than initially estimated (e.g., multi-environment deployment)
- New infrastructure component discovered not in original plan
- Web research reveals tooling or procedures that need codebase verification
- Quality gate analyst identifies coverage gaps that require additional research tracks

---

## Output Structure

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

The final operational guide follows this structure. The synthesis agents produce sections that are assembled into this format by the rf-assembler agent, conforming to the template at `.claude/templates/documents/operational_guide_template.md`.

```markdown
---
status: "🟡 Draft"
created_date: [today]
depends_on: []
tags: []
---

# [Guide Title]

> **WHAT:** [What this guide covers — the procedure scope]
> **WHY:** [Why this guide exists — operational need]
> **HOW TO USE:** [How to use this guide — sequential phases, skip-ahead guidance]
> **Target Host:** [Which machine(s) this procedure targets]

## Document Information

| Field | Value |
|-------|-------|
| Guide Name | [name] |
| Guide Type | [Setup Guide / Deployment Procedure / Upgrade/Migration Guide / Maintenance Runbook] |
| Target Environment | [dev / staging / production / all] |
| Maintained By | [team or role] |
| Last Verified Against System | [date] |
| Prerequisites Guide | [link to prerequisite guide, if any] |
| Next Guide | [link to follow-on guide, if any] |

---

## Table of Contents
[Generated from actual section headers after all sections placed]

---

## 1. Overview
Purpose, scope, what this guide achieves, system context.

---

## 2. Prerequisites
Required access, tools, prior guides completed, environment setup.

### Pre-Flight Checklist
| # | Check | How to Verify |
|---|-------|---------------|
| 1 | [specific, verifiable prerequisite] | [command or action to verify] |

---

## 3. Phase 1: [Name]

### Step 1.1: [Action]
[Command with Expected Output block]

### Step 1.2: [Action]
[...]

### Phase 1 Verification Checkpoint
- [ ] [Observable condition confirming phase success]

---

## 4. Phase 2: [Name]
[Same structure as Phase 1 — Step X.Y numbering, commands with Expected Output, verification checkpoint]

---

## N. Phase N: [Name]
[Same structure — add as many phases as the procedure requires]

---

## N+1. Verification
### Health Checks
[Specific commands with expected status codes/output]

### End-to-End Validation
[Full procedure validation steps]

### All-Green Checklist
- [ ] [Each critical verification condition]

---

## N+2. Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| [observable problem] | [root cause] | [fix with specific commands] |

### Documentation Staleness
[CODE-CONTRADICTED findings surfaced here]

---

## N+3. Maintenance & Operations
Scheduled tasks, log rotation, backup procedures, update process.

---

## N+4. Quick Reference
Service URLs, key file paths, common commands, configuration files.
Must be self-contained — usable without reading the full guide.

---

## N+5. Next Steps
Links to follow-on guides, related docs, open questions.

---

## Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| [date] | 1.0 | [author] | Initial creation |

---

## Appendix: Document Provenance
[Only if consolidating existing docs — source materials and creation method]
```

---

## Synthesis Mapping Table (Reference)

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

This is the standard mapping of synthesis files to operational guide template sections. Adjust based on procedure complexity — simple procedures can combine more sections per synth file. Complex multi-phase procedures may need additional synth files for additional phases.

| Synth File | Template Sections | Source Research Files |
|------------|-------------------|----------------------|
| `synth-01-overview-prerequisites.md` | 1. Overview, 2. Prerequisites (incl. Pre-Flight Checklist) | Infrastructure inventory, environment config, existing docs, integration points |
| `synth-02-phase-[name].md` | 3. Phase 1: [Name] (steps, commands, Expected Output, verification checkpoint) | Per-phase research files, config tracers for the phase's configs |
| `synth-03-phase-[name].md` | 4. Phase 2: [Name] | Per-phase research files |
| `synth-04-phase-[name].md` | 5. Phase 3: [Name] | Per-phase research files |
| `synth-05-verification-troubleshooting.md` | N+1. Verification (Health Checks, E2E Validation, All-Green Checklist), N+2. Troubleshooting (Symptom/Cause/Solution tables, Documentation Staleness entries) | All phase research, integration points, web research (tooling docs, verification patterns) |
| `synth-06-maintenance-quickref.md` | N+3. Maintenance & Operations, N+4. Quick Reference | Environment config, scripts, automation, web research (ops best practices) |
| `synth-07-nextsteps-appendix.md` | N+5. Next Steps, Document History, Appendix: Document Provenance | Integration points, related docs, gaps log, consolidation source list |

**Phase synth file count:** The number of `synth-0N-phase-[name].md` files scales with the procedure's phase count. A 2-phase procedure needs 2 phase synth files; a 6-phase procedure needs 6. Adjust numbering accordingly.

---

## Synthesis Quality Review Checklist

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

**This checklist is enforced by the rf-analyst and rf-qa agents** (see Phase 5 in the BUILD_REQUEST phase definitions above). The rf-analyst applies these 9 criteria as its Synthesis Quality Review analysis type, and the rf-qa agent independently verifies the analyst's findings with its expanded 12-item Synthesis Gate checklist. The QA agents report findings only (fix_authorization: false). A serialized fix agent applies all collected findings.

The 9 criteria (used by rf-analyst):

1. Template section headers match the expected format from the Output Structure template — Overview, Prerequisites, Phase sections with descriptive names, Verification, Troubleshooting, Maintenance & Operations, Quick Reference, Next Steps
2. Tables use the correct column structure — Pre-Flight Checklist uses `# | Check | How to Verify`; Troubleshooting uses `Symptom | Cause | Solution`; Document Information uses `Field | Value`; config tables use `Setting | Value | File | Notes`
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and evidence (not vague descriptions) — every command, port, path, and config value traces to an actual config/script read
5. Phase steps use Step X.Y numbering (Step 1.1, Step 1.2) with commands and Expected Output blocks
6. Each phase ends with an inline verification checkpoint — a numbered checklist of observable conditions confirming the phase succeeded
7. All cross-references between sections are consistent (e.g., ports in Prerequisites match ports in Phase steps and Quick Reference; environment variables in Phase steps are documented in Prerequisites)
8. **No doc-only claims in procedure steps or commands.** Verify that Phase sections only contain operational procedures backed by code-traced evidence. If a synth file describes a command, port, path, or config value and the only evidence is a documentation file (no source code/config path), reject that claim and either remove it or flag it as `[UNVERIFIED — doc-only]`
9. **Stale documentation discrepancies are surfaced.** Any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings from research files should appear in the Troubleshooting section as "Documentation Staleness" entries or in Next Steps as open questions, not silently omitted

The rf-qa agent's Synthesis Gate adds 3 additional checks (10-12): depth budget compliance (Overview+Prerequisites: 30-50 lines; each Phase: 80-150 lines; Verification: 40-80 lines; Troubleshooting: 50-100 lines; Quick Reference: 30-50 lines; Maintenance: 30-60 lines; Next Steps+Appendix: 20-40 lines), content deduplication with companion Technical References, and hallucinated file path detection. If synthesis QA fails, the serialized fix agent applies all collected fixes from all QA reports. Issues remaining after max fix cycles trigger re-synthesis of the affected files.

---

## Assembly Process

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

The assembly step reads all synth files in order and produces the final operational guide. Follow these 4 steps:

1. **Write the guide header** — frontmatter (status, created_date, depends_on, tags), preamble blockquote (WHAT, WHY, HOW TO USE, Target Host), and Document Information table (all 7 rows)
2. **Assemble sections in template order** — read each synth file and write its content into the correct section position, writing incrementally section by section (do NOT one-shot the entire guide). Phase sections are placed in procedure order. Sections not covered by a synth file are written directly during assembly from patterns observed in the synth files.
3. **Write the Table of Contents** — generate from actual section headers after all sections are placed
4. **Cross-check internal consistency** — verify that:
   - Prerequisites mentioned in Phase 1 steps are listed in the Prerequisites section
   - Ports, paths, and service URLs in Prerequisites match those used in Phase steps and Quick Reference
   - Environment variables referenced in Phase steps are documented in Prerequisites or Overview
   - Verification checks at end of each Phase align with items in the Verification section
   - Troubleshooting entries cover failure modes mentioned in Phase steps
   - Quick Reference section contains every service URL, key path, and common command from the Phases
   - No placeholder text remains (search for `[`, `TODO`, `TBD`, `PLACEHOLDER`)
   - Total line count is within tier budget (Lightweight: 200-400, Standard: 400-700, Heavyweight: 700-1000) — hard ceiling 1,000 lines

---

## Artifact Locations

> All QA report paths in this table are relative to `${TASK_DIR}qa/` when only the filename is shown (i.e., no directory prefix). Full paths are shown for non-QA artifacts.

| Artifact | Location |
|----------|----------|
| Task folder | `${TASK_DIR}` (`.dev/tasks/to-do/TASK-OPSGUIDE-<subject>-[YYYYMMDD-HHMMSS]/`) |
| MDTM task file | `${TASK_DIR}TASK-OPSGUIDE-<subject>-[YYYYMMDD-HHMMSS].md` |
| Research notes | `${TASK_DIR}research/research-notes.md` |
| Research files | `${TASK_DIR}research/[NN]-[topic].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Gaps log | `${TASK_DIR}gaps-and-questions.md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Analyst reports (research gate) | `${TASK_DIR}qa/analyst-completeness-report[-N].md`, `analyst-cross-validation-report[-N].md` |
| QA reports (research gate) | `${TASK_DIR}qa/qa-research-evidence-quality-report[-N].md`, `qa-research-gap-detection-report[-N].md` |
| Qualitative report (research gate) | `${TASK_DIR}qa/qa-research-depth-report[-N].md` |
| Consolidated findings (research) | `${TASK_DIR}qa/qa-research-consolidated-findings.md` |
| Analyst reports (synthesis gate) | `${TASK_DIR}qa/analyst-synthesis-accuracy-report[-N].md`, `analyst-synthesis-source-tracing-report[-N].md` |
| QA reports (synthesis gate) | `${TASK_DIR}qa/qa-synthesis-structure-report[-N].md`, `qa-synthesis-content-quality-report[-N].md` |
| Qualitative report (synthesis gate) | `${TASK_DIR}qa/qa-synthesis-coherence-report[-N].md` |
| Consolidated findings (synthesis) | `${TASK_DIR}qa/qa-synthesis-consolidated-findings.md` |
| Lens QA reports (structural) | `${TASK_DIR}qa/qa-lens-template-conformance.md`, `qa-lens-internal-consistency.md`, `qa-lens-evidence-quality.md`, `qa-lens-completeness.md` |
| Lens QA reports (content) | `${TASK_DIR}qa/qa-lens-actionability.md`, `qa-lens-numbers-metrics.md`, `qa-lens-crossref-chain.md`, `qa-lens-domain-accuracy.md` |
| Lens QA reports (ops-guide domain) | `${TASK_DIR}qa/qa-lens-command-accuracy.md`, `qa-lens-env-var-verification.md`, `qa-lens-procedural-executability.md` |
| Consolidated findings (lens QA) | `${TASK_DIR}qa/qa-lens-consolidated-findings.md` |
| Source fidelity reports | `${TASK_DIR}qa/qa-source-fidelity-report-1.md`, `qa-source-fidelity-report-2.md` (more if partitioned) |
| Final operational guide | `docs/docs-product/ops/[name]-operational-guide.md` |
| Template schema | `.claude/templates/documents/operational_guide_template.md` |

Research, synthesis, and QA report files persist in the task folder — they serve as the evidence trail for claims in the operational guide and can be re-used when the document needs updating.

---

## Updating an Existing Operational Guide

When the user wants to update (not create) an existing operational guide:

1. Read the current document to understand what's already covered
2. Research only the changed/new areas (don't re-research everything)
3. Write new research files for the changes: `${TASK_DIR}research/update-[date]-[topic].md`
4. Edit the relevant sections of the operational guide in place
5. Run at minimum 2 QA lens agents (internal-consistency + procedural-step-executability) on the updated guide. For substantial updates (>3 sections changed), run the full lens-based QA gate from Phase 6.
6. Update the Document Information table with the new verification date
7. Update Document History with what changed

---

## Session Management

Session management is provided by the `/task` skill. When resuming a session:

1. Check for an existing task folder matching `TASK-OPSGUIDE-*/` in `.dev/tasks/to-do/`
2. If found, invoke `/task` with the task file path inside the folder — it will resume from the first unchecked item
3. Check for existing research files in `${TASK_DIR}research/` for context
4. Read any analyst/QA gate reports in `${TASK_DIR}qa/` to understand which gates have already passed

If no task folder exists but the user references a previous procedure, they likely need to restart from Stage A (scope discovery).
