---
name: roadmap
description: "Create a phased implementation roadmap from any user input (PRD, TDD, free-form prompt, any document). Produces a roadmap document, BUILD_REQUEST files, and execution-ready MDTM task files by composing /task-builder and /task. Use this skill when the user wants to create a roadmap, generate a roadmap, build a roadmap, plan the implementation, create an execution plan, break something into phases, create a phased plan, produce a roadmap, or plan how to build something. Trigger on phrases like 'roadmap', 'create a roadmap', 'generate roadmap', 'build a roadmap', 'plan the implementation', 'create an execution plan', 'break this into phases', 'create a phased plan', 'produce a roadmap', 'plan how to build this', 'decompose this into phases', or 'what are the steps to build X'."
---

# Roadmap Generator

A skill for creating phased implementation roadmaps from any user input. This skill is a pure orchestrator — it composes `/task-builder` and `/task` to produce three deliverables: a structured roadmap document, a set of BUILD_REQUEST files (one per phase), and execution-ready MDTM task files for every phase. The user's only remaining action after the skill completes is to execute each phase in order using `/task`.

**How it works:** The skill accepts any input describing something to build (PRD, TDD, free-form prompt, any document), performs scope discovery, then invokes `/task-builder` to create a task file for roadmap generation. It delegates to `/task` to execute that task file — producing the roadmap document from a template. After post-completion validation, the skill generates BUILD_REQUEST files for each roadmap phase and invokes `/task-builder` on each one, producing execution-ready MDTM task files. Every step uses the same two skills: `/task-builder` creates work plans, `/task` executes them.

This skill fills the gap between upstream document skills (`/prd`, `/tdd`) and downstream execution (`/task`). Where `/prd` defines what to build and `/tdd` defines how to build it, `/roadmap` decomposes the work into ordered phases with dependencies, coverage traceability, and ready-to-execute task files.

## Why This Process Works

Roadmaps fail when they rely on shallow phase decomposition, incomplete requirement coverage, or unvalidated dependency chains. This skill forces every requirement through coverage traceability — parallel agents analyze the input, trace requirement coverage across phases, and validate integration contracts with file paths and specific deliverables.

The MDTM task file provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off.

The multi-phase structure (scope discovery -> roadmap generation -> **4-stage QA** -> BUILD_REQUEST generation -> **task file creation** -> presentation) prevents five common failure modes:
- **Context rot** — By isolating each investigation topic in its own subagent with its own output file, no single agent needs to hold the entire roadmap in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning parallel agents (each focused on one aspect of the input), the analysis goes deep on every requirement simultaneously rather than skimming across everything sequentially.
- **Hallucinated phase dependencies** — By separating input analysis (what requirements exist) from phase design (how to sequence work) from validation (does coverage hold), each phase can be verified independently. Phase designers only work from verified requirement lists, not from memory or inference.
- **Uncaught quality drift** — **Lens-based multi-agent QA** with 44-48 evaluating agents minimum across 4 stages (assumes 6 phases; formula: 15 lens + 2-4 fidelity (2 for single-source, 4 for prd+tdd) + 2 source-verification + 3 coverage + 3×N BUILD_REQUEST + 4 post-task-file-validation where N = phase count) (plus fix/verification agents as needed) ensures no single agent rubber-stamps a large output. Each agent evaluates ONE quality dimension (lens) — structural lenses (template conformance, internal consistency, evidence quality, completeness) and content lenses (actionability, numbers/metrics, cross-reference chains, domain accuracy) plus 7 roadmap-specific domain lenses (dependency acyclicity, phase boundary correctness, obligation discharge, task-to-requirement semantic match, task granularity, resource/effort realism, integration contract completeness). Serialized fix authorization prevents conflicting parallel edits — all agents report findings first, then a single fix agent applies all corrections, then verification agents confirm.
- **Phantom coverage** — **Source-document fidelity gates** with 2-4 dedicated agents (4 for prd+tdd: 2 on PRD sections + 2 on TDD sections; 2 for single-source or free-form inputs) read the original inputs alongside the roadmap output and verify semantic fidelity — not just ID presence, but that each task ACTUALLY implements its mapped requirement with source-specific details preserved (error code counts, field types, state pairs, thresholds). This catches the phantom coverage problem where a REQ ID appears in the coverage matrix but the task description doesn't actually address the requirement.

The 4-stage QA architecture ensures errors don't cascade:
- **Stage 1 (Document QA, 15 lens + 2-4 fidelity = 17-19 evaluating agents):** Lens-based verification of the roadmap document itself — 8 standard lens agents (4 structural + 4 content) + 7 domain-specific lens agents + 2-4 source-fidelity agents (4 for prd+tdd, 2 for single-source or free-form inputs).
- **Stage 2 (Coverage Validation, 3 agents):** Forward coverage (semantic match, not just ID), backward orphan detection, and detail preservation sampling.
- **Stage 3 (BUILD_REQUEST Validation, ~18-24 agents):** 3 agents per BUILD_REQUEST verifying structural completeness, content sufficiency, and source-fidelity (Rule 28) before /task-builder invocation.
- **Stage 4 (Post-Task-File Validation, 2 agents):** Cross-task-file consistency and task-file-to-roadmap alignment after all task files are created.

The roadmap artifacts persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and feed directly into downstream execution via `/task`.

### Variable Reference

Every invocation creates a self-contained folder. All paths below are relative to this folder:

```
TASK_ID:        TASK-ROADMAP-<subject>-YYYYMMDD-HHMMSS
TASK_DIR:       .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:      ${TASK_DIR}${TASK_ID}.md
RESEARCH:       ${TASK_DIR}research/
QA:             ${TASK_DIR}qa/
ROADMAP_DIR:    ${TASK_DIR}
BUILD_REQUESTS: ${TASK_DIR}build-requests/
```

**Subject derivation:** `<subject>` is derived at task-folder-creation time from the `PROJECT_NAME` and normalized to kebab-case (lowercase, hyphen-separated, 1-3 words, ~30 char soft cap). If no clean subject can be derived, fall back to the literal word `general`. Example TASK_ID: `TASK-ROADMAP-task-management-system-20260408-140000`.

---

## Input

The skill needs four pieces of information to produce a phased roadmap. The first is mandatory; the rest are optional but dramatically improve output quality.

1. **WHAT to build** (mandatory) — A description of what needs to be built. Accepts any input type: a standard RF PRD (28 sections from `/prd`), a standard RF TDD (28 sections from `/tdd`), a PRD + TDD together, a partial PRD/TDD, a free-form prompt, any other document (product vision, spec, design doc, RFC), or a combination of the above. The skill does NOT parse these inputs with a deterministic section parser — the LLM reads the full input directly. The input type affects the richness of the roadmap, not the process.

2. **WHY / what context** (strongly recommended) — What prompted this work and what constraints apply. This shapes whether the roadmap emphasizes speed, quality, incremental delivery, or risk mitigation.

3. **SOURCE_PATHS** (optional, saves significant time) — Specific file paths to input documents (PRD, TDD, design docs). When provided, the skill reads these files directly instead of relying on inline content. Multiple paths supported.

4. **PROJECT_NAME** (optional, improves artifact naming) — A short name or slug for the roadmap project. Used in the roadmap title and artifact naming. If not provided, the skill infers one from the input content.

### Effective Prompt Examples

**Strong — document paths + context:**
> Create a roadmap from this PRD and TDD: `.dev/docs/TASK_MANAGEMENT_PRD.md` and `.dev/docs/TASK_MANAGEMENT_TDD.md`. The project needs to be built incrementally — each phase should be independently deployable. Project name: task-management-system.

**Strong — free-form with clear scope:**
> Build a roadmap for implementing a real-time collaboration system. We need WebSocket infrastructure, presence indicators, cursor sharing, and conflict resolution. Start with the transport layer, then build features on top. The backend is FastAPI + Redis, frontend is Next.js + Zustand.

**Strong — combined input:**
> Generate a phased execution plan from this design doc: `.dev/plans/pixel-streaming-redesign.md`. We want to migrate from VM-per-session to a shared GPU pool. Priority is zero downtime — each phase must maintain backward compatibility. Dry run first so I can review the phase plan before committing.

**Weak — no subject (will be asked to clarify):**
> Create a roadmap.

**Weak — too vague (will produce a broad, less actionable roadmap):**
> Plan how to build the platform.

### What to Do If the Prompt Is Incomplete

If the user provides only a topic name or a vague request, **do NOT proceed immediately**. Ask the user to clarify using this template:

> I can create a roadmap for [topic] for you. To make the phases focused and the task files actionable, can you help me with:
>
> 1. **What specifically do you want to build?** (e.g., "a real-time collaboration system", "the task management feature from the PRD")
> 2. **What are you trying to achieve?** (e.g., "incremental delivery with each phase deployable", "migrate without downtime")
> 3. **Any specific documents I should read?** (PRD, TDD, design docs, specs — file paths)
> 4. **What should I call this project?** (a short name for the roadmap title and artifact naming)

Proceed once you have at least #1 answered clearly. Items #2-4 improve quality but aren't blockers.

---

## Depth Tiers

Select a tier based on input complexity. **Default to Deep** unless the request is clearly narrow and simple.

| Tier | When to Use | Codebase Agents | Web Agents | Roadmap Depth |
|------|------------|-----------------|------------|---------------|
| **Quick** | Simple feature, single subsystem, <5 requirements | 1-2 | 0-1 | 1-3 phases, roadmap document only (no BUILD_REQUESTs or task files) |
| **Standard** | Multi-subsystem, 5-20 requirements, moderate complexity | 3-5 | 1-2 | 3-6 phases, roadmap + BUILD_REQUESTs (no automatic task file creation) |
| **Deep** | Cross-cutting, 20+ requirements, architectural decisions, integration work | 5-10+ | 2-4 | Full pipeline: roadmap + BUILD_REQUESTs + task files via /task-builder |

**Tier selection rules:**
- If in doubt, pick Deep
- If the user says "full roadmap", "comprehensive", "end-to-end plan" — always Deep
- Only use Quick for genuinely simple requests ("plan how to add a single endpoint")
- If the input spans multiple services, layers, or architectural boundaries — always Deep

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

All persistent artifacts go to the task folder `${TASK_DIR}` (see Variable Reference above). The TASK_ID uses the format `TASK-ROADMAP-<subject>-YYYYMMDD-HHMMSS` (timestamp-based). The roadmap document filename uses `${PROJECT_NAME}` in SCREAMING_SNAKE_CASE (see A.2 for the derivation rule).

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}TASK-ROADMAP-<subject>-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research/research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[aspect-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Roadmap document | `${TASK_DIR}ROADMAP-[PROJECT_NAME].md` (SCREAMING_SNAKE_CASE, e.g., `ROADMAP-TASK_MANAGEMENT_SYSTEM.md`) |
| BUILD_REQUEST files | `${TASK_DIR}build-requests/BUILD_REQUEST-phase-NN-[name].md` |
| Phased MDTM task files | `.dev/tasks/to-do/TASK-*/` (one per phase, created by /task-builder) |
| State file | `${TASK_DIR}.roadmap-state.json` |
| Deviation report (re-runs) | `${TASK_DIR}deviation-report.md` |
| QA reports | `${TASK_DIR}qa/` |
| Analyst completeness report | `${TASK_DIR}qa/analyst-completeness-report.md` |
| QA research gate report | `${TASK_DIR}qa/qa-research-gate-report.md` |
| Stage 1 lens reports (structural) | `${TASK_DIR}qa/qa-lens-template-conformance.md`, `qa-lens-internal-consistency.md`, `qa-lens-evidence-quality.md`, `qa-lens-completeness.md` |
| Stage 1 lens reports (content) | `${TASK_DIR}qa/qa-lens-actionability.md`, `qa-lens-numbers-metrics.md`, `qa-lens-crossref-chain.md`, `qa-lens-domain-accuracy.md` |
| Stage 1 domain lens reports | `${TASK_DIR}qa/qa-lens-dependency-acyclicity.md`, `qa-lens-phase-boundary.md`, `qa-lens-obligation-discharge.md`, `qa-lens-task-req-semantic-match.md`, `qa-lens-task-granularity.md`, `qa-lens-resource-realism.md`, `qa-lens-integration-contract.md` |
| Stage 1 consolidated findings | `${TASK_DIR}qa/qa-stage1-consolidated-findings.md` |
| Stage 1 fidelity reports | `${TASK_DIR}qa/qa-fidelity-prd-1.md`, `qa-fidelity-prd-2.md`, `qa-fidelity-tdd-1.md`, `qa-fidelity-tdd-2.md` |
| Stage 1 fidelity consolidated | `${TASK_DIR}qa/qa-fidelity-consolidated-findings.md` |
| Stage 2 coverage reports | `${TASK_DIR}qa/qa-coverage-forward.md`, `qa-coverage-backward-orphan.md`, `qa-coverage-detail-preservation.md` |
| Stage 3 BUILD_REQUEST reports | `${TASK_DIR}qa/qa-build-request-phase-NN-structural.md`, `qa-build-request-phase-NN-sufficiency.md` |
| Stage 4 cross-task reports | `${TASK_DIR}qa/qa-cross-task-consistency.md`, `qa-task-roadmap-alignment.md` |

**File numbering convention:** All research and web research files use zero-padded sequential numbers: `01-`, `02-`, `03-`, etc. This ensures correct ordering when listing files.

Check for existing task folders in `.dev/tasks/to-do/` before creating new ones — if prior roadmap work exists on the same topic (matching `TASK-ROADMAP-*/`), read it first and build on it.

---

## Execution Overview

The skill operates in two stages:

**Stage A — Scope Discovery & Task File Creation (before the task file exists):**
1. Check for existing task file (resume if found) (A.1)
2. Parse the user's input and triage (Scenario A vs B) (A.2)
3. Perform scope discovery (depth adjusted by scenario) (A.3)
4. Write scope discovery results to a structured research notes file (A.4)
5. Review research sufficiency (mandatory gate) (A.5)
6. Triage template selection (A.6)
7. Write BUILD-REQUEST.md and invoke /task-builder skill to create the MDTM task file (A.7) — task-builder handles structural and qualitative validation internally

**Stage B — Task File Execution (after the task file exists):**
8. Delegate to the `/task` skill, which executes from the task file using the F1 loop
9. Each checklist item is a self-contained prompt — no prior context needed

If a task file already exists for this roadmap topic (from a previous session), skip Stage A and invoke `/task` with the existing task file path — it resumes from the first unchecked item.

**The task file encodes these phases:**
- **Phase 1** — Preparation (create folders, read template)
- **Phase 2** — Roadmap Generation (create stub from template, populate 11 sections incrementally, sentinel gate, obligation scan, integration contract validation, Stage 1 lens-based QA with 15 lens + 2-4 fidelity = 17-19 evaluating agents (fidelity agents: 4 for prd+tdd, 2 for single-source or free-form inputs), plus fix/verification as needed, serialized fix protocol). After Stage 1 QA passes, run Source Document Fidelity Verification (Step 2.VERIFY): verification agents read original PRD/TDD + populated roadmap, verify each REQ/SPEC has a faithful task mapping in S4 with matching detail. Remediation loop (Step 2.VERIFY.FIX) addresses gaps before proceeding to Phase 3 Coverage Validation.
- **Phase 3** — Post-Completion Validation (Stage 2: 3 Coverage Validator agents — forward semantic coverage + backward orphan + detail preservation, input hash, state file)
- **Phase 4** — BUILD_REQUEST Generation (one BUILD_REQUEST per roadmap phase, Stage 3: 3 QA agents per BUILD_REQUEST (structural + sufficiency + source-fidelity))
- **Phase 5** — Task File Creation (invoke `/task-builder` per BUILD_REQUEST, Stage 4: 2 post-creation validation agents)
- **Phase 6** — Presentation (summary, task file tracker update, downstream skill offers)

---

## Stage A: Scope Discovery & Task File Creation

### A.1: Check for Existing Task File

Before creating a new task file, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `TASK-ROADMAP-*/` folder related to this topic
2. If found, read the task file inside it (`${TASK_DIR}TASK-ROADMAP-*.md`) and check for unchecked `- [ ]` items
3. If unchecked items exist → invoke the /task skill with the task file path (Stage B)
4. If all items are checked → roadmap is already complete. Check for re-run with changed input:
   a. Read `${TASK_DIR}.roadmap-state.json` (if it exists) and extract the stored `input_hash`
   b. Compute SHA-256 hash of the current user input
   c. If hashes match → inform user roadmap is already complete and up-to-date. Offer to re-generate or execute existing phase task files.
   d. If hashes differ → **deviation tracking workflow:**
      1. Diff the requirement and specification lists: compare the old roadmap's Section 2 (Input Analysis) requirement and specification IDs with the new input.s requirements and specifications
      2. Categorize changes: **NEW** requirements (need new roadmap tasks/phases), **REMOVED** requirements (roadmap tasks/phases may be orphaned), **MODIFIED** requirements (affected roadmap tasks may need updates)
      3. Generate a deviation report at `${TASK_DIR}deviation-report.md` documenting: new requirements/specifications and their suggested phase placement, orphaned tasks covering removed requirements/specifications, modified requirements/specifications and which tasks they affect
      4. Incremental update: re-populate only affected sections (S2 Input Analysis, S4 affected phase details, S7 Coverage Traceability Matrix) rather than full regeneration
      5. Re-validate: run all gates (sentinel, obligation scan, integration contracts, coverage) on the updated roadmap
      6. Update `.roadmap-state.json` with the new input_hash and last_run timestamp
   e. If no `.roadmap-state.json` exists → treat as a fresh re-run (inform user, offer to re-generate from scratch or build on existing roadmap)
5. Check for existing task folder matching `TASK-ROADMAP-*/` in `.dev/tasks/to-do/`:
   a. If `${TASK_DIR}research/research-notes.md` exists with `Status: Complete` → skip to A.5 (review sufficiency, then build task file)
   b. If `${TASK_DIR}research/research-notes.md` exists with `Status: In Progress` → read it, resume A.3 scope discovery from where it left off, then continue to A.4 to update the file
   c. If task folder exists but no `research-notes.md` → continue with A.3 but use the existing folder
6. If no task folder exists → continue with A.2

### A.2: Parse & Triage the Input

Break the user's input into structured components:

- **GOAL**: What the roadmap should accomplish (the thing to be built)
- **WHY**: What the user wants to achieve and what constraints apply (incremental delivery, zero downtime, etc.)
- **WHERE**: Specific file paths to input documents (PRD, TDD, design docs)
- **PROJECT_NAME**: The project name in SCREAMING_SNAKE_CASE, used in the roadmap document filename (e.g., `TASK_MANAGEMENT_SYSTEM`, `PIXEL_STREAMING_REDESIGN`). Derive from the user-provided project name by: (1) trimming whitespace, (2) uppercasing, (3) replacing spaces and hyphens with underscores. Examples: "task management system" → `TASK_MANAGEMENT_SYSTEM`; "pixel-streaming-redesign" → `PIXEL_STREAMING_REDESIGN`; "Task Management System" → `TASK_MANAGEMENT_SYSTEM`. Used to produce the roadmap filename `ROADMAP-${PROJECT_NAME}.md` per the template's file naming convention.
- **INPUT_TYPE**: Classification of the input — one of:
  - `prd` — Standard RF PRD (28 sections)
  - `tdd` — Standard RF TDD (28 sections)
  - `prd+tdd` — Both PRD and TDD provided
  - `partial-doc` — PRD/TDD missing template-standard fields
  - `free-form` — Free-form prompt describing what to build
  - `other-doc` — Product vision, spec, design doc, RFC, or other document
  - `combined` — Multiple input types (e.g., prompt + document paths)

**Triage into Scenario A or B:**

**Scenario A — Explicit request:** User provided most of: input documents, project scope, constraints, specific features/requirements.
Example: "Create a roadmap from this PRD and TDD: `.dev/docs/TASK_MANAGEMENT_PRD.md` and `.dev/docs/TASK_MANAGEMENT_TDD.md`. Each phase should be independently deployable."
→ Scope discovery confirms details and fills minor gaps. Lighter exploration.

**Scenario B — Vague request:** User provided a goal but few specifics.
Example: "Build a roadmap for the collaboration feature"
→ Scope discovery does broad exploration to understand what exists, identify requirements, and plan phase decomposition.

**Dry-run detection:** If the user's input contains `--dry-run`, "dry run", or "plan only", set DRY_RUN=true. The skill will produce a phase plan summary without generating the full roadmap, BUILD_REQUESTs, or task files.

**Do NOT interrogate the user with a list of questions.** Proceed with what you have and let scope discovery figure out the rest from the input and codebase. Only ask the user (via `AskUserQuestion`) if there's a genuine ambiguity about **intent** that can't be inferred.

### A.3: Perform Scope Discovery

Use Glob, Grep, Read, and codebase-retrieval to map the problem space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.

**Adjust depth by scenario:**
- **Scenario A**: Focused discovery — read the provided documents, verify referenced files/directories exist, scan for related code, identify gaps in what the user specified.
- **Scenario B**: Broad discovery — scan the codebase for anything touching the topic, read existing documentation, map all relevant subsystems, identify requirements from the input.

Discover:
- All requirements, features, and components described in the input
- Existing code, documentation, and infrastructure related to the topic
- External dependencies, integration points, and constraints
- Complexity indicators (number of subsystems, cross-cutting concerns, existing tech debt)
- Potential phase boundaries (natural groupings of work)

Based on the discovery:
- Select depth tier (default: Deep)
- Plan research assignments — divide the input analysis into specific topics, each becoming a subagent assignment
- Determine the phase decomposition strategy
- Identify validation requirements

**Research assignment types** (use as many as the topic requires):

| Type | Purpose | What the Agent Does |
|------|---------|-------------------|
| **Code Tracer** | Understand existing implementations | Read implementations, trace data flow, follow imports, document what exists |
| **Doc Analyst** | Extract context from existing documentation | Read docs, **cross-validate every architectural claim against actual code**, note discrepancies and stale content |
| **Integration Mapper** | Identify connection points | Map APIs, extension points, plugin interfaces, service boundaries, config surfaces |
| **Input Analyst** | Extract requirements from user input | Read the full user input, enumerate requirements with REQ-NNN IDs and specifications with SPEC-NNN IDs, classify priority, identify ambiguities |
| **Phase Designer** | Propose phase structure from requirements and specifications | Group requirements and specifications into phases, define dependencies, estimate complexity, annotate parallelism |

**Note:** These are the scope-discovery agent types used during A.3. Additional agent types used during roadmap generation and validation (Coverage Validator, Web Research, rf-analyst, rf-qa, rf-qa-qualitative, rf-qa structural) are defined in the Agent Prompt Templates section below.

Compute `<subject>` from the `PROJECT_NAME` normalized to kebab-case using the rules in the Subject Derivation section. If no clean subject is derivable, use `general`. Create the task folder: `.dev/tasks/to-do/TASK-ROADMAP-<subject>-YYYYMMDD-HHMMSS/` with subfolders `research/`, `qa/`, `build-requests/`

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
# Research Notes: [PROJECT_NAME]

**Date:** [today]
**Scenario:** [A or B]
**Depth Tier:** [Quick / Standard / Deep]

---

## EXISTING_FILES
[All files, directories, and subsystems found during scope discovery. Per-file detail: path, purpose, key exports, approximate line count. Group by directory or subsystem.]

## PATTERNS_AND_CONVENTIONS
[Code patterns, naming conventions, architectural patterns, design decisions observed. Cite specific files as evidence.]

## INPUT_ANALYSIS
[Summary of the user's input: document type, key requirements/features identified with REQ-NNN IDs and key specifications identified with SPEC-NNN IDs, scope boundaries, ambiguities, constraints. This is the foundation for the roadmap's Input Analysis section (S2).]

## RECOMMENDED_OUTPUTS
[Planned output files: roadmap document path, BUILD_REQUEST paths, task file expectations. Full paths and purposes.]

## SUGGESTED_PHASES
[Planned phase breakdown. For each phase:
- Phase number, name, goal
- Requirements and specifications covered (REQ-NNN / SPEC-NNN IDs)
- Dependencies on prior phases
- Estimated complexity (S/M/L)
- Key deliverables]

## TEMPLATE_NOTES
[Notes about which MDTM template to use and why. Almost always Template 02 for roadmap.]

## AMBIGUITIES_FOR_USER
[Genuine ambiguities about user intent that cannot be resolved from the input or codebase. If none, write "None — intent is clear from the request and codebase context."]
```

### A.5: Review Research Sufficiency (MANDATORY GATE)

**You MUST review the research notes before spawning the builder.** This is a quality gate — do NOT skip it.

Read `${TASK_DIR}research/research-notes.md` and evaluate:

1. Are relevant source files and input documents identified with specific paths?
2. Are requirements enumerated with REQ-NNN IDs and priorities? Are specifications enumerated with SPEC-NNN IDs and types (when TDD input is present)?
3. Is the phase structure justified with clear dependency rationale?
4. Are there unresolved ambiguities that would block the builder?
5. If the input includes references to existing code: are those code paths verified against the actual codebase?
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
- Multiple phases with different activities (research, generation, validation)
- Review/validation steps
- Conditional flows based on findings

**Use Template 01 (Generic Task) when the work involves:**
- Simple, sequential file creation
- Straightforward execution with no discovery
- Single-pass operations

**For roadmap, the answer is almost always Template 02** — the skill inherently involves input analysis, template-driven document generation, multi-section population, obligation scanning, integration contract validation, coverage verification, BUILD_REQUEST generation, and nested `/task-builder` invocations.

### A.7: Build the Task File

Write the BUILD_REQUEST to a file at `${TASK_DIR}BUILD-REQUEST.md`, then invoke the `/task-builder` skill. The task-builder reads the BUILD_REQUEST file, performs quality gates (rf-analyst + rf-qa), spawns the rf-task-builder agent to create the MDTM task file, and runs structural and qualitative validation internally. No manual verification step is needed — task-builder handles all validation and mediation.

**Step 1: Write `${TASK_DIR}BUILD-REQUEST.md`** using the Write tool with the following content:

````
# BUILD REQUEST

Source: skill-delegated
Calling Skill: roadmap
Task Directory: ${TASK_DIR}
Research Notes: ${TASK_DIR}research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Create a phased implementation roadmap from user input and produce BUILD_REQUEST files for each phase. The roadmap will be written to `${TASK_DIR}ROADMAP-[PROJECT_NAME].md` (SCREAMING_SNAKE_CASE per the template's file naming convention, e.g., `ROADMAP-TASK_MANAGEMENT_SYSTEM.md`) using the roadmap template at `.claude/templates/documents/roadmap_template.md`. After roadmap completion, generate BUILD_REQUEST files at `${TASK_DIR}build-requests/BUILD_REQUEST-phase-NN-[name].md` and invoke `/task-builder` on each to produce execution-ready MDTM task files.

WHY: [WHY — what the user wants to build and why a phased roadmap is needed]

TASK_ID_PREFIX: TASK-ROADMAP

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
[If scope discovery found any documentation that contradicts actual code, list the
specific claims and contradictions here. If none found during scope discovery, write:
"None found during scope discovery. Phase 2 agents will perform full documentation
cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags."]
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:
- Phase 1 (Preparation): L0 Setup — create folders, read template, validate inputs
- Phase 2 (Roadmap Generation): L2 Build-from-Discovery — create stub from template, populate 11 sections incrementally, run sentinel gate, obligation scan, integration contract validation, QA structural, QA qualitative
- Phase 3 (Post-Completion Validation): L4 Review/QA — Coverage Validator agent verifies 100% forward coverage, backward orphan check, input hash computation, state file creation
- Phase 4 (BUILD_REQUEST Generation): L2 Build-from-Discovery — generate one BUILD_REQUEST per roadmap phase
- Phase 5 (Task File Creation): L6 Aggregation — invoke Skill(skill: "task-builder", args: "<BUILD_REQUEST-path>") per BUILD_REQUEST, update Task File Tracker
- Phase 6 (Presentation): L0 Closeout — present results, update task frontmatter

QA_INTENSITY: [lite / standard / full]  (per I22 — determined by tier mapping in Depth Tiers section or user override)
QA_GATE_REQUIREMENTS: PER_PHASE (4-STAGE QA ARCHITECTURE — 44-48 EVALUATING AGENTS MINIMUM (assumes 6 phases; formula: 15 lens + 2-4 fidelity (2 for single-source, 4 for prd+tdd) + 2 source-verification + 3 coverage + 3×N BUILD_REQUEST + 4 post-task-file-validation where N = phase count) + FIX/VERIFICATION AS NEEDED (formula: per fix cycle = 1 fix agent + 2 verification agents; max additional across all stages: Stage 1 lens 3x3=9, Stage 1 fidelity 2x3=6, Stage 2 4x3=12, Stage 3 per-BR 2x3=6, Stage 4 2x3=6))
  **NOTE: Stage descriptions below specify FULL intensity agent counts. When QA_INTENSITY is lite or standard, the rf-task-builder applies I22 reductions via the QA Intensity Adaptation table in the Agent Prompt Templates section. The 4-stage architecture is roadmap-specific — see intensity adaptation table for per-stage reductions.**
  Stage 1 — Roadmap Document QA (Phase 2)
    - lite: 2 rf-qa (combined structural) + 1 rf-qa-qualitative (combined content) + 1 domain lens (dependency-acyclicity) + 1 fidelity agent = 5 agents. Max 1 fix cycle. Inline gates (sentinel + obligation) still run.
    - standard: 3 rf-qa structural + 3 rf-qa-qualitative content + 2 domain (dependency-acyclicity + obligation-discharge) + 2 fidelity agents = 10 agents. Max 2 fix cycles.
    - full: 4 rf-qa structural + 4 rf-qa-qualitative content + 7 domain lenses + 2-4 fidelity (4 for prd+tdd, 2 for single-source) = 17-19 agents. Max 3 fix cycles. Serialized fix protocol (Steps 2.QA.1-2.QA.9). PLUS Step 2.VERIFY: 2-4 additional source document verification agents scaled by source doc size (21-23 total for Stage 1 + Step 2.VERIFY). Step 2.VERIFY intensity: lite = 1 agent, standard = 2 agents, full = 2-4 agents (partitioned if source >1000 lines).
    NOTE: Stage 1 includes TWO fidelity verification layers: (1) the existing source-document fidelity gate (Steps 2.QA.8-2.QA.9) performs a SWEEP check: does the roadmap mention each source section's topics (coverage) and preserve notable details (error counts, field counts)?, and (2) the new Source Document Fidelity Verification (Step 2.VERIFY) performs a LINE-ITEM AUDIT: for each individual REQ/SPEC ID, read the source detail, read the S4 task, and rate whether the specific implementation details survived — whether each REQ/SPEC's specific details are faithfully reflected in the corresponding task descriptions in S4. The existing fidelity gate runs BEFORE Step 2.VERIFY; Step 2.VERIFY runs AFTER the existing fidelity gate passes.
  Stage 2 — Coverage Validation (Phase 3)
    - lite: SKIP — coverage validation deferred to task-builder's own QA.
    - standard: 3 agents (forward-coverage + backward-orphan + detail-preservation). Max 2 fix cycles.
    - full: 3 agents (forward-coverage rf-qa, backward-orphan rf-qa, detail-preservation rf-qa-qualitative). Max 3 fix cycles.
  Stage 3 — BUILD_REQUEST Validation (Phase 4)
    - lite: 1 agent per BUILD_REQUEST (combined structural + sufficiency + source-fidelity in one pass via a merged lens).
    - standard: 2 agents per BUILD_REQUEST (1 rf-qa structural+sufficiency + 1 rf-qa source-fidelity). All validated in parallel across BRs.
    - full: 3 agents per BUILD_REQUEST (rf-qa structural + rf-qa-qualitative sufficiency + rf-qa source-fidelity). All validated in parallel across BRs.
  Stage 4 — Post-Task-File End-to-End Validation (Phase 5)
    - lite: 2 agents (1 rf-qa cross-task-consistency + 1 rf-qa-qualitative end-to-end fidelity). Max 1 fix cycle.
    - standard: 3 agents (1 rf-qa cross-task-consistency + 1 rf-qa-qualitative roadmap-to-task-fidelity + 1 rf-qa input-to-task-fidelity). Max 2 fix cycles. For >4 phases: add 1 agent per 2 additional phases.
    - full: 4+ agents (1 rf-qa cross-task-consistency + 1 rf-qa-qualitative roadmap-to-task-fidelity + 1 rf-qa input-to-task-fidelity + 1 rf-qa-qualitative SPEC-detail-survival). For >4 phases: partition task files across additional agents (1 agent per 2 task files). Max 2 fix cycles.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + OBLIGATION_SCAN + INTEGRATION_CONTRACTS + COVERAGE_TRACEABILITY
  TEMPLATE_COMPLIANCE: All roadmap sections must be populated (zero remaining {{RF_PLACEHOLDER:*}} sentinels).
  EVIDENCE_TRAIL: Every requirement and specification traces to specific input content.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.
  OBLIGATION_SCAN: Zero undischarged scaffold obligations across phases.
  INTEGRATION_CONTRACTS: Zero orphan artifacts, zero missing creators in cross-phase Integration Points tables.
  COVERAGE_TRACEABILITY: 100% forward coverage (every REQ and every SPEC from S2 has >= 1 task in S7). Backward check (every task traces to >= 1 REQ or SPEC).

TESTING_REQUIREMENTS: N/A — documentation-only skill (roadmap documents + BUILD_REQUESTs), no code produced, no tests applicable.

RESEARCH NOTES FILE:
${TASK_DIR}research/research-notes.md
Read this file FIRST for full detailed findings including: input analysis, existing files, patterns, planned phase breakdown, and output paths.

SKILL CONTEXT FILE:
.claude/skills/roadmap/SKILL.md
Read the "Agent Prompt Templates" section for: Input Analyst Prompt, Phase Designer Prompt, Coverage Validator Prompt, Web Research Agent Prompt. Read the "Roadmap Document Structure" section for roadmap document format. Read the "Section-to-Agent Mapping Table" section for which agent populates which roadmap section. Read the "Roadmap Quality Review Checklist" section for post-population verification. Read the "Roadmap Population Process" section for the stub-populate-validate flow. Read the "Validation Checklist" section for validation criteria. Read the "Content Rules" section for writing standards. These must be embedded in the relevant checklist items per B2 self-contained pattern.

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process
Structure), you MUST create individual checklist items for EVERY roadmap section
population, validation gate, BUILD_REQUEST generation, and /task-builder invocation.
Do NOT create batch items like "populate all 11 sections" or "generate all BUILD_REQUESTs"
— each section gets its own item, each BUILD_REQUEST gets its own item. The research
notes SUGGESTED_PHASES section contains per-phase detail specifically to enable this
granularity.

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

PRE-ENCODING LINT — SINGLE-AGENT-AT-SCALE ENFORCEMENT (MANDATORY):
Before encoding any agent-spawning checklist items, the task-builder MUST perform this audit on the SKILL.md content it is about to encode. The audit covers four dimensions:

**Dimension 1 — READ-side (Rule 21):**
1. Grep for "Read the ENTIRE" in agent prompt code blocks.
2. For every match, verify the prompt contains an `Assigned slice:` parameter. If not → Rule 21 violation. HALT, log, refuse to encode.
3. For every SKILL PHASES agent-spawn bullet, verify bullets reading source documents state "PARTITIONED PER §A.3 THRESHOLDS" or have a thresholds-formula K.
4. For every partitioned read step, verify a "Merge sub-step" exists immediately after.

**Dimension 2 — WRITE/FIX-side (Rule 24):**
5. Grep for "Spawn 1 rf-qa fix agent" / "Spawn 1 fix agent" / "ONE fix agent applies all" in SKILL PHASES bullets.
6. For every match, verify the bullet contains a Rule 24 scope threshold ("K per Rule 24 thresholds", "≤15 findings", "SEQUENTIAL fix agents"). Unconditional "Spawn 1 fix agent" without threshold → Rule 24 violation.
7. Verify every fix-cycle bullet names the consolidated-findings file AND references K-per-Rule-24-thresholds.

**Dimension 3 — ANALYSIS-side (EDIT 10):**
8. Grep for "15 lens agents" / "Spawn N lens agents" in SKILL PHASES bullets.
9. For every match, verify K-per-lens partitioning based on roadmap size. Unconditional 15 agents without roadmap-size branching → violation.
10. Grep for "Spawn 2 verification agents" / "2 verifiers".
11. For every match, verify V determined by document-size thresholds (V=2/4/6). Unconditional V=2 → violation.

**Dimension 4 — GENERATION-side (EDIT 12):**
12. In the Section-to-Agent Mapping Table, for rows S7/S8/S10/S11 that say "Orchestrator (inline)", verify each row includes "OR N Populator agents when [threshold]". Unconditional inline → violation.
13. In SKILL PHASES population bullets for S7/S8/S10/S11, verify each contains "PARTITIONED BY [count]". Bullets without scale branch → violation.

**Dimension 5 — FIDELITY-side (Rule 28):**
14. For every agent prompt in Agent Prompt Templates classified as a GENERATOR (Per-Phase Designer, Populator agents for S7/S8/S10/S11, BUILD_REQUEST Source-Extractor, BUILD_REQUEST Generator), verify the Design Protocol / Protocol block contains an Extract-Before-Compose step (typically labeled "0. SOURCE EXTRACTION" or "STEP 0").
15. For every generator agent prompt, verify the prompt requires every concrete claim in output to be marked `[verbatim: CITATION]` or `[derived from: CITATION]`. Unmarked concrete claims are a Rule 28 violation.
16. For every generator agent prompt, verify the prompt includes a self-audit step before emitting output (grep own output, cross-check against source-extract, remove fabrications; adversarial assumption of ≥N fabrications).
17. In the Phase 4 SKILL PHASES bullets, verify the BUILD_REQUEST generation pipeline spawns a Source-Extractor BEFORE the Generator (Step 1 → Step 2 ordering), and the Generator's Step 2 gates on ALL Step 1 extracts existing on disk.
18. In the Phase 4 SKILL PHASES bullets, verify Stage 3 QA spawns 3 agents per BUILD_REQUEST (structural + sufficiency + source-fidelity), not 2.
19. In the Per-phase BUILD_REQUEST format, verify CONTEXT FILES requires explicit line ranges per cited section (not just file paths), and a SOURCE CITATIONS section is present at the end of the format.

**Enforcement:**
Any violation HALTS encoding with a structured error report. The lint is intentionally strict — a skill that cannot pass this lint is a skill that will fail at scale.

Phase 1 — Preparation:
- Update task status to "🟠 Doing"
- Create the task folder at .dev/tasks/to-do/TASK-ROADMAP-<subject>-YYYYMMDD-HHMMSS/ with `research/`, `qa/`, `build-requests/` subfolders
- Read the roadmap template at `.claude/templates/documents/roadmap_template.md` — this defines all 11 sections and their 19 placeholder sentinels (8 metadata/title + 11 section content). The template contains `<!-- GUIDANCE: ... -->` comments for each section that define expected content format, table structure, column specifications, and content rules. Section-population agents MUST read and follow these GUIDANCE comments when generating content for each section.

Phase 2 — Roadmap Generation (TEMPLATE-DRIVEN, INCREMENTAL):
- Read the full user input (entire document content, never a compressed summary). If SOURCE_PATHS were provided, read those files.
- Create roadmap stub — Write the roadmap template to `${TASK_DIR}ROADMAP-[PROJECT_NAME].md` (SCREAMING_SNAKE_CASE per the template's file naming convention at lines 308-309, e.g., `ROADMAP-TASK_MANAGEMENT_SYSTEM.md`) with ALL `{{RF_PLACEHOLDER:*}}` sentinels intact. This is the roadmap document's initial state.
- Populate Metadata — Replace metadata placeholders (project name, source input description, date, total phases, total tasks, estimated scope, estimated duration)
- Populate Section 1 (Executive Summary) — Read user input, generate 1-2 paragraph summary covering what's being built, why, phased approach, expected outcome, key architectural decisions, critical path, and business impact (per template S1 GUIDANCE). Replace `{{RF_PLACEHOLDER:executive_summary}}`
- Populate Section 2 (Input Analysis) — Read user input, enumerate ALL requirements/features/components with IDs (REQ-001, REQ-002...) and all specifications with IDs (SPEC-001, SPEC-002...) when TDD input is present, classify priority (Must/Should/Could), note source references. Replace `{{RF_PLACEHOLDER:input_analysis}}`. This section establishes the coverage contract. (PARTITIONED PER §A.3 THRESHOLDS: ≤1000 lines→K=1, 1000-3000→K=2-3, 3000-6000→K=4-5, 6000+→K=5-10+; partition by source document, then section range within each.)
- Merge Input Analyst outputs — consolidate all K agent outputs into `${TASK_DIR}qa/s2-input-analysis-merged.md`; deduplicate REQ/SPEC IDs; renumber if needed.
- Populate Section 3 (Phase Overview) — Spawn 1 Phase Designer Lead agent (reads merged input analysis only, bounded ≤2000 lines by design). Output is `${TASK_DIR}qa/s3-phase-overview.md` plus a Per-Phase Slice Plan that partitions build-content across phases for the next stage. Replace `{{RF_PLACEHOLDER:phase_overview_table}}` from the Lead's S3 Phase Overview Table.
- Populate Section 4 (Phase Details) — Spawn N Per-Phase Designer agents IN PARALLEL (one per phase from S3's Per-Phase Slice Plan). Each agent reads only its assigned slice of the merged input analysis + relevant codebase research and produces `${TASK_DIR}qa/s4-phase-detail-NN.md` with the full 8-col Task Table, Integration Points, and Coverage Gaps. MERGE SUB-STEP: orchestrator concatenates all s4-phase-detail-NN.md files into the S4 section of the roadmap, preserving per-phase order. Replace `{{RF_PLACEHOLDER:phase_details}}`.
- Populate Section 5 (Dependency Graph) — Orchestrator synthesizes S5 Dependency Graph by cross-referencing all per-phase dependency blocks from the merged s4-phase-detail-NN files (no separate agent spawn). Include cross-phase task-level dependencies. Must be acyclic. Replace `{{RF_PLACEHOLDER:dependency_graph}}`.
- Populate Section 6 (Task File Tracker) — Create tracking table with one row per phase, all statuses "pending", BUILD_REQUEST paths TBD. Replace `{{RF_PLACEHOLDER:task_file_tracker}}`
- Populate Section 7 (Coverage Traceability Matrix) — Cross-reference Section 2 requirement IDs and specification IDs against Section 4 task IDs. Verify 100% forward coverage for both REQ and SPEC. Flag orphan tasks (backward check). Replace `{{RF_PLACEHOLDER:coverage_traceability_matrix}}`. IF REQ+SPEC ≤50: orchestrator inline. IF REQ+SPEC >50: PARTITIONED BY (REQ pool / SPEC pool); spawn N Coverage Matrix Populator agents (rf-analyst) IN PARALLEL using Coverage Matrix Populator Agent Prompt; further partition SPEC pool by TDD section range when SPEC >200. Merge sub-step: concatenate all s7-matrix-[pool]-[N].md files into the S7 section; aggregate orphan lists.
- Populate Section 8 (Risk Register) — Identify risks with severity, probability, mitigation, contingency. Replace `{{RF_PLACEHOLDER:risk_register}}`. IF risks ≤20: inline. IF risks >20: PARTITIONED BY phase; spawn N Risk Register Populator agents (rf-analyst) IN PARALLEL using Risk Register Populator Agent Prompt. Merge sub-step: concatenate s8-risks-[N].md files.
- Populate Section 9 (Resource Requirements) — Identify external dependencies and resources per phase. Replace `{{RF_PLACEHOLDER:resource_requirements}}`
- Populate Section 10 (Open Questions) — Compile unresolved questions with blocking phase annotations. Replace `{{RF_PLACEHOLDER:open_questions}}`. IF questions ≤20: inline. IF questions >20: PARTITIONED BY blocking phase; spawn N Open Questions Populator agents (rf-analyst) IN PARALLEL using Open Questions Populator Agent Prompt. Merge sub-step: concatenate s10-questions-[N].md files.
- Populate Section 11 (Architectural Debt) — Document intentional shortcuts and deferred decisions. Replace `{{RF_PLACEHOLDER:architectural_debt}}`. IF debt items ≤15: inline. IF debt items >15: PARTITIONED BY phase or category; spawn N Architectural Debt Populator agents (rf-analyst) IN PARALLEL using Architectural Debt Populator Agent Prompt. Merge sub-step: concatenate s11-debt-[N].md files.
- Sentinel gate — Scan for remaining `{{RF_PLACEHOLDER:*}}` sentinels. Any found = FAIL. Fix cycle (max 3): identify unpopulated sections, re-populate, re-scan.
- Obligation scan — Scan all phase details for scaffold terms (mock, stub, skeleton, placeholder, scaffold, temporary, hardcoded, hardwired, no-op, dummy, fake). For each found, verify a discharge term exists in a later phase referencing the same component (replace, wire up, integrate, connect, swap out, remove mock/stub, implement real, fill in, complete). Zero undischarged obligations required. Violations → add to Open Questions (Section 10) with blocking annotation.
- Integration contract validation — For every Integration Points table entry: verify "Created By" has a matching "Consumed By" in a later phase, and vice versa. Zero orphan artifacts, zero missing creators. Violations → add to Risk Register (Section 8) as Critical.
- Stage 1 — Lens-based QA (15 lens agents, ALL with fix_authorization: false):
  - (PARTITIONED PER §A.3 + roadmap-size thresholds: K per-lens branching based on roadmap size — ≤2000 lines→K=1, 2000-5000→K=2, 5000-8000→K=3, 8000+→K=4+. Each lens spawns K agents, each on its assigned section slice.) Spawn (4 × K) rf-qa structural lens agents IN PARALLEL using the "Structural Lens Agent Prompts" from the Agent Prompt Templates section. Each lens evaluates ONE dimension: (1) template-conformance, (2) internal-consistency, (3) evidence-quality, (4) completeness. Each agent writes to `${TASK_DIR}qa/qa-lens-[lens-name]-[N].md`.
  - (PARTITIONED PER §A.3 + roadmap-size thresholds: K per-lens branching based on roadmap size — ≤2000 lines→K=1, 2000-5000→K=2, 5000-8000→K=3, 8000+→K=4+.) Spawn (4 × K) rf-qa-qualitative content lens agents IN PARALLEL using the "Content Lens Agent Prompts" from the Agent Prompt Templates section. Each lens evaluates ONE dimension: (1) actionability, (2) numbers-metrics, (3) crossref-chain, (4) domain-accuracy. Each agent writes to `${TASK_DIR}qa/qa-lens-[lens-name]-[N].md`.
  - (PARTITIONED PER §A.3 + roadmap-size thresholds: K per-lens branching based on roadmap size — ≤2000 lines→K=1, 2000-5000→K=2, 5000-8000→K=3, 8000+→K=4+.) Spawn (7 × K) roadmap domain-specific lens agents IN PARALLEL using the "Domain Lens Agent Prompts" from the Agent Prompt Templates section. Each lens evaluates ONE dimension: (1) dependency-acyclicity [rf-qa], (2) phase-boundary-correctness [rf-qa-qualitative], (3) obligation-discharge [rf-qa], (4) task-req-semantic-match [rf-qa-qualitative], (5) task-granularity [rf-qa-qualitative], (6) resource-realism [rf-qa], (7) integration-contract-completeness [rf-qa]. Each agent writes to `${TASK_DIR}qa/qa-lens-[lens-name]-[N].md`.
  - Consolidate findings — Read all 15×K lens agent reports (merge per-slice reports for each lens first, then combine across lenses), merge into `${TASK_DIR}qa/qa-stage1-consolidated-findings.md`. Deduplicate overlapping findings. Severity-rate each: CRITICAL / IMPORTANT / MINOR.
  - Fix round — Count consolidated lens findings. Determine K per Rule 24 thresholds (≤15→K=1, 16-40→K=2-3, 41-100→K=4-6, 100+→HALT). Partition by finding category (structural / content / domain) or section range. Spawn K SEQUENTIAL fix agents (rf-qa, fix_authorization: true) using the Partitioned Fix Agent Prompt — fix agent N+1 does NOT start until fix agent N has returned. Each receives its partition of findings (finding IDs + allowed file regions) and applies only those fixes. Consolidated findings file: `${TASK_DIR}qa/qa-stage1-consolidated-findings.md`.
  - Verification round — Determine V per document-size thresholds (≤2000 lines→V=2, 2000-5000→V=4, 5000+→V=6). Spawn V verification agents IN PARALLEL (split ~50/50 between rf-qa structural and rf-qa-qualitative content; fix_authorization: false) to confirm fixes applied correctly and no new issues introduced across the full roadmap. Each agent covers a section slice (partitioned identically to the Stage 1 lens agents). (Verification confirms fix application, not original detection — scope narrower than initial evaluation but must scale with document size to maintain coverage.) If issues remain, repeat fix-verify cycle (max 3 total cycles). HALT if unresolved after 3 cycles.
- Stage 1 — Source-document fidelity gate (2-4 agents depending on input type, ALL with fix_authorization: false):
  - Spawn fidelity agents IN PARALLEL using the "Source Fidelity Agent Prompt" from the Agent Prompt Templates section. Agent count depends on input type: If `prd+tdd`: spawn 4 agents — (1) PRD first half + full roadmap, (2) PRD second half + full roadmap, (3) TDD first half + full roadmap, (4) TDD second half + full roadmap. If `combined`: decompose to component types and apply the most expansive matching branch (e.g., if combined includes prd+tdd, use the prd+tdd branch with 4 agents; otherwise use the single-source branch with 2 agents). If `prd` or `tdd` only: spawn 2 agents — (1) source first half + full roadmap, (2) source second half + full roadmap. If `free-form`, `other-doc`, or `partial-doc`: spawn 2 agents — (1) original input first half + full roadmap, (2) original input second half + full roadmap. Minimum 2 fidelity agents always. Each checks: semantic coverage (does the roadmap task ACTUALLY implement the source requirement?), detail preservation (error code counts, field types, state pairs, thresholds survive), phantom coverage detection (REQ ID present but task doesn't address it), cross-source contradiction flagging (if multiple sources exist). Each writes to `${TASK_DIR}qa/qa-fidelity-[source]-[N].md`.
  - Consolidate fidelity findings into `${TASK_DIR}qa/qa-fidelity-consolidated-findings.md`. Determine K per Rule 24 thresholds based on consolidated fidelity findings count. Spawn K SEQUENTIAL fix agents (rf-qa, fix_authorization: true) using the Partitioned Fix Agent Prompt — partitioned by source-document type (PRD findings / TDD findings) and finding category. Verification round — Determine V per document-size thresholds (≤2000→V=2, 2000-5000→V=4, 5000+→V=6), split ~50/50 rf-qa and rf-qa-qualitative. Each agent covers a fidelity slice (partitioned by source-doc type × section range identically to Stage 1 fidelity agents). Max 2 fidelity fix cycles.

- Step 2.VERIFY: Source Document Fidelity Verification — After Stage 1 QA passes, spawn source document fidelity verification agents to read the ORIGINAL PRD/TDD alongside the populated roadmap. This is an outward-facing check: does the roadmap faithfully capture what the source documents say? Unlike Stage 1 QA (which checks internal roadmap quality), this step checks source-to-roadmap fidelity for implementation detail — does each REQ-NNN's acceptance criteria and each SPEC-NNN's specific details (field types, index definitions, error codes, state transitions) appear in the corresponding S4 task descriptions? Agent count scales by qa_intensity: lite = 1 agent (combined sources), standard = 2 agents (1 per source document type present), full = 2-4 agents (partition source docs by section range if >1000 lines, same scaling as Stage 1 fidelity gate). Each agent reads its assigned source document section range (or full doc if not partitioned) + the full populated roadmap (S2 + S4 + S7). Output: ${TASK_DIR}qa/qa-source-verification-[source-type].md. If FAIL: run remediation loop (Step 2.VERIFY.FIX).
- Step 2.VERIFY.FIX: Source Fidelity Remediation Loop — (1) Consolidate all verification agent gap reports into ${TASK_DIR}qa/qa-source-verification-consolidated.md. (2) For each gap rated MISSING or PARTIAL: either (a) update the corresponding task in S4 to add the missing details from the source document (preferred — adds field names, index specs, error codes, transition counts, etc. to the task description and acceptance criteria), or (b) if the gap cannot be addressed by a task update (i.e., it represents a deliberate scope exclusion where the source document specifies something the roadmap intentionally does not cover, OR a design trade-off where the implementation approach differs from the TDD spec for documented reasons. Example task-update: SPEC says 8 compound indexes but task only lists 5 = add the 3 missing indexes to the task acceptance criteria. Example Open Questions: TDD specifies Redis caching but roadmap uses PostgreSQL instead = document the architectural decision), document it in S10 Open Questions with the source reference and justification for deferral. (3) After all gaps are addressed, re-run the source document verification agents (Step 2.VERIFY) to confirm the remediation resolved the gaps. Max 2 remediation cycles. If gaps remain after 2 cycles, document remaining gaps in S10 Open Questions and proceed to Phase 3 Coverage Validation. (4) Determine K per Rule 24 thresholds based on consolidated gap count. Spawn K SEQUENTIAL fix agents (rf-qa, fix_authorization: true) using the Partitioned Fix Agent Prompt. Each agent receives a partition of gaps (e.g., by source-doc type or by S4 section range) + allowed file regions. Sequential execution preserves anti-churn.

Phase 3 — Post-Completion Validation:
- Spawn 3 Coverage Validation agents IN PARALLEL using the upgraded "Coverage Validator Agent Prompts" from the Agent Prompt Templates section:
  - (1) Forward coverage agents (rf-qa) — Spawn Forward Coverage agents IN PARALLEL (PARTITIONED PER §A.3 THRESHOLDS: by coverage pool first — always split REQ pool vs SPEC pool; then by source section range when a pool covers >1000 source lines; K=1 if both pools ≤1000 combined, K=2 if split by pool, K=3-6 if additionally split by section range). Each agent reads roadmap S2 + S7 + its assigned source slice. For EACH REQ and EACH SPEC in its assigned pool+slice, reads the actual task description in S4 and verifies SEMANTIC match (not just ID presence in S7). Every requirement and specification must have at least one task that genuinely implements it. Each writes to `${TASK_DIR}qa/qa-coverage-forward-[pool]-[N].md`. Merge sub-step: orchestrator concatenates all forward coverage reports into `${TASK_DIR}qa/qa-coverage-forward-consolidated.md` before proceeding to Backward Orphan and Detail Preservation gates.
  - (2) Backward orphan agent (rf-qa) — reads roadmap S4 + S7. Every task in S4 must trace to at least one REQ or SPEC in S7. Tasks with no backing requirement or specification are flagged as scope creep. Write to `${TASK_DIR}qa/qa-coverage-backward-orphan.md`.
  - (3a) REQ Detail Preservation agent (rf-qa-qualitative) — reads PRD only; samples 20% of REQs (min 10); outputs `${TASK_DIR}qa/qa-coverage-detail-preservation-req.md`. Spawn once regardless of PRD size (PRD sampling is bounded at 20%).
  - (3b) SPEC Detail Preservation agent (rf-qa-qualitative) — TDD inputs only; reads TDD only; samples 20% of SPECs (min 10). PARTITIONED: K=1 when TDD ≤3000 lines; K=2-3 when TDD >3000 lines (partition by TDD section range). Each agent writes to `${TASK_DIR}qa/qa-coverage-detail-preservation-spec-[N].md`. Merge sub-step: concatenate SPEC-DP reports into `${TASK_DIR}qa/qa-coverage-detail-preservation-spec-consolidated.md`. Skip entirely if input does not include TDD.
- If coverage gaps found: consolidate findings from all 3 coverage agents into a single findings file, determine K per Rule 24 thresholds based on consolidated coverage finding count. Spawn K SEQUENTIAL fix agents (rf-qa, fix_authorization: true) using the Partitioned Fix Agent Prompt — partitioned by coverage pool (REQ pool / SPEC pool) and section (add-missing-tasks / update-S7 / remove-orphans). Then re-spawn V verification agents per document-size thresholds (≤2000→V=2, 2000-5000→V=4, 5000+→V=6) drawn from the same coverage agent roster (Forward Coverage / Backward Orphan / Detail Preservation). Each verification agent covers a coverage slice (partitioned identically to its originating coverage agent). Max 3 fix cycles.
- Compute SHA-256 hash of user input. Store in roadmap metadata and in `${TASK_DIR}.roadmap-state.json`.
- Create/update `.roadmap-state.json` with: schema_version, input_hash, input_paths, created, last_run, roadmap_status, sections_populated, validation_status (obligation_scan, integration_contracts, coverage, sentinel_check), build_requests_generated, task_files_created, fix_cycles.

Phase 4 — BUILD_REQUEST Generation (3-step per-phase pipeline, Rule 28 Extract-Before-Compose):
- Step 1 — Source extraction (PARALLEL across phases). Spawn N BUILD_REQUEST Source-Extractor agents IN PARALLEL (one per phase) using the "BUILD_REQUEST Source-Extractor Agent Prompt" from the Agent Prompt Templates section. Each agent reads roadmap Phase NN's S4/S5/S7/S8/S10/S11 rows + cited PRD/TDD sections and writes a citation manifest to `${TASK_DIR}qa/build-request-phase-NN-source-extract.md`. Merge sub-step: none — each extract is independent.
- Step 2 — BUILD_REQUEST composition (PARALLEL across phases, gated on Step 1). After ALL source-extract files exist, spawn N BUILD_REQUEST Generator agents IN PARALLEL (one per phase) using the "BUILD_REQUEST Generator Agent Prompt" from the Agent Prompt Templates section. Each generator reads ONLY its phase's source-extract file and composes the BUILD_REQUEST at `${TASK_DIR}build-requests/BUILD_REQUEST-phase-NN-[name].md` using the per-phase BUILD_REQUEST format. Every concrete claim marked `[verbatim: CITATION]` or `[derived from: CITATION]`. Generator self-audits before emitting.
- Step 3 — Stage 3 QA (PARALLEL across phases). For EACH BUILD_REQUEST generated, spawn 3 QA agents IN PARALLEL using the Stage 3 agent prompts from the Agent Prompt Templates section:
  - (1) rf-qa (BUILD_REQUEST structural) — verifies all required sections present: GOAL, WHY, DEPTH_TIER, TEMPLATE, CONTEXT FILES (with line ranges), DELIVERABLES, DEPENDENCIES, ACCEPTANCE CRITERIA, PHASE-SPECIFIC GUIDANCE, QA REQUIREMENTS, SOURCE CITATIONS. No missing sections, no empty fields. Write to `${TASK_DIR}qa/qa-build-request-phase-NN-structural.md`.
  - (2) rf-qa-qualitative (BUILD_REQUEST sufficiency) — verifies GOAL is specific enough for task-builder to produce a useful task file, CONTEXT FILES reference the correct source files with valid line ranges, QA REQUIREMENTS specify adequate agent counts (minimum 6 per gate). Write to `${TASK_DIR}qa/qa-build-request-phase-NN-sufficiency.md`.
  - (3) rf-qa (BUILD_REQUEST source-fidelity, Rule 28 enforcement) — NEW. Reads source-extract + BUILD_REQUEST + roadmap/PRD/TDD. Grep-verifies every concrete claim against sources. Flags fabrications (unverifiable claims), miscitations (wrong line ranges), marker-missing lint (unmarked concrete claims), contradictions, duplications. Write to `${TASK_DIR}qa/qa-build-request-phase-NN-source-fidelity.md`.
  - All Stage 3 validations run in parallel across BUILD_REQUESTs × 3 agents each (with 6-8 phases, Stage 3 is 18-24 agents total, was 12-16 before the fidelity refactor).
  - If any BUILD_REQUEST fails validation: for each failing BUILD_REQUEST independently, determine K per Rule 24 thresholds based on that BUILD_REQUEST's consolidated finding count (source-fidelity findings typically dominate; K=1 for ≤15 findings, K=2-3 for 16-40). Spawn K SEQUENTIAL fix agents (rf-qa, fix_authorization: true) using the Partitioned Fix Agent Prompt — each receives a partition of findings (by category: structural / sufficiency / fabrication / miscitation / marker-missing). Then re-spawn the 3 evaluating agents for that BUILD_REQUEST (fix_authorization: false) to verify. Each BUILD_REQUEST has its own independent fix cycle. Max 2 fix cycles per BUILD_REQUEST.
- After all BUILD_REQUESTs pass Stage 3, update `.roadmap-state.json` with `build_requests_generated: true`.

````
Per-phase BUILD_REQUEST format:
```markdown
# BUILD_REQUEST: Phase NN — [Phase Name]

## GOAL
[1-2 sentences. Every concrete noun marked `[verbatim: CITATION]` or `[derived from: CITATION]`.]

## WHY
[Context from roadmap + original input. Quoted motivation marked `[verbatim: CITATION]`.]

## DEPTH_TIER
[Quick / Standard / Deep — from input analysis]

## TEMPLATE
02 (complex task — this phase depends on prior phase outputs)

## CONTEXT FILES (task-builder researcher MUST read these; line ranges required)
- Roadmap: [path] §<section numbers> L<start>-<end>
- Original user input: [path or inline] §<section numbers> L<start>-<end> for each cited section
- PRD (if present): [path] §<section numbers> L<start>-<end> per cited section
- TDD (if present): [path] §<section numbers> L<start>-<end> per cited section (example: `TDD: docs/TDD_RIGORFLOW_PLATFORM.md §8 L1447-1808 (API Specs), §14 L2649-2871 (Observability)`)
- Prior phase outputs (if phase > 1):
  - Phase N-1 task file: [DEFERRED — created in Phase 5; task-builder should reference roadmap Phase N-1 details instead]
  - Phase N-1 expected outputs: [list from roadmap] [verbatim: ROADMAP Lx-y]

## DELIVERABLES
[One bullet per concrete deliverable from roadmap. Each concrete noun / count / name marked `[verbatim: CITATION]` or `[derived from: CITATION]`.]

## DEPENDENCIES
- Depends on: [Phase N-1 completion, specific outputs — each item marked]
- Blocks: [Phase N+1, if applicable]

## ACCEPTANCE CRITERIA
[Verbatim from roadmap Exit Criteria. Each criterion cited `[verbatim: ROADMAP Lx-y]`.]

## PHASE-SPECIFIC GUIDANCE
[Implementation hints. Each concrete claim marked `[verbatim: CITATION]` or `[derived from: CITATION]`. No bare concrete claims permitted.]

## QA REQUIREMENTS
The task file created from this BUILD_REQUEST MUST include:
- Lens-based QA gate items after each major deliverable: minimum 6 agents per gate (3 rf-qa structural lenses + 3 rf-qa-qualitative content lenses). Single-agent or 2-agent QA gates are PROHIBITED.
- Source-document fidelity gate items reading the roadmap + original source docs to verify semantic fidelity (minimum 2 fidelity agents)
- Serialized fix authorization for all multi-agent gates (report-only → consolidate → K-per-Rule-24 sequential fix → verify)
- Post-completion validation item checking outputs against roadmap requirements
- All QA gates encoded as explicit `- [ ]` checklist items in the task file, not prose descriptions

## SOURCE CITATIONS
[Unique list of every citation referenced in the body above. Format one per line:
- [ROADMAP Lx-y] — brief description
- [PRD §x Ly-z] — brief description
- [TDD §x Ly-z] — brief description
This block is the validator's quick-reference and MUST match exactly the citations used inline.]

## TIER-CONDITIONAL PHASE ENCODING
When generating BUILD_REQUESTs, respect the DEPTH_TIER to determine which phases to encode:
- If DEPTH_TIER is Quick: encode Phases 1-3 and Phase 6 only (omit Phase 4 BUILD_REQUEST Generation and Phase 5 Task File Creation).
- If DEPTH_TIER is Standard: encode Phases 1-4 and Phase 6 only (omit Phase 5 Task File Creation).
- If DEPTH_TIER is Deep: encode all Phases 1-6.
```
````

Phase 5 — Task File Creation (NESTED /task-builder INVOCATIONS):

**CRITICAL: After each task-builder invocation completes and outputs TASK_FILE_READY, continue to the next BUILD_REQUEST or Phase 6. Do NOT stop at task-builder's output.**

- For each BUILD_REQUEST file (in phase order), invoke `/task-builder` via: Skill(skill: "task-builder", args: "${TASK_DIR}build-requests/BUILD_REQUEST-phase-NN-[name].md")
- One checklist item PER /task-builder invocation — do NOT batch.
- Each item: (1) invoke /task-builder with BUILD_REQUEST path, (2) receive created task file path, (3) update the roadmap's Task File Tracker (Section 6) with the task file path and status "created", (4) update `.roadmap-state.json` task_files_created entry, (5) mark checklist item complete.
- Phase ordering matters: Phase N's BUILD_REQUEST references Phase N-1's expected outputs. Task-builder's researcher reads those references. Actual outputs don't exist yet, but the task file is structured to expect them as inputs when executed.
- Post-Task-File End-to-End Validation (Stage 4 QA) — After ALL task files are created from all BUILD_REQUESTs, spawn agents IN PARALLEL (agent count per qa_intensity: lite=2, standard=3+, full=4+) using the 'Post-Task-File Validation Agent Prompts' from the Agent Prompt Templates section. This is the FINAL end-to-end fidelity check: Input → Roadmap → BUILD_REQUEST → Task File.
  - (1) rf-qa (cross-task-file consistency) — reads ALL created task files + the roadmap's dependency graph (S5). Verifies: dependencies between task files match the roadmap's dependency graph; Phase N's task file doesn't reference outputs from Phase N+1's task file; entry criteria of each task file are satisfiable given prior task file's exit deliverables. Write to ${TASK_DIR}qa/qa-cross-task-consistency.md.
  - (2) rf-qa-qualitative (roadmap-to-task-fidelity) — reads ALL created task files + roadmap Phase Details (S4) + S7 Coverage Traceability Matrix. Verifies: each task file's scope matches its roadmap phase, task item counts match roadmap task counts, acceptance criteria match roadmap exit criteria, AND every REQ/SPEC from S7 has a corresponding checklist item in a task file that implements it. Write to ${TASK_DIR}qa/qa-roadmap-to-task-fidelity.md.
  - (3) rf-qa (input-to-task-fidelity) — Spawn Input-to-Task Fidelity agents IN PARALLEL (PARTITIONED PER §A.3 THRESHOLDS: by source-doc type × task-file slice; K=1 for single-source + ≤3 task files; K=2-3 for single-source + 4-10 task files; K=4+ for multi-source or 10+ task files). Each agent reads its assigned source slice + its assigned task-file slice. Verifies end-to-end: every requirement from the original input has a task file checklist item that addresses it; every TDD specification (when TDD present) has a task file item whose acceptance criteria preserve the specific detail (field types, index names, error codes, state transitions, API signatures). This catches content lost in the Input → Roadmap → BUILD_REQUEST → Task File pipeline. Each writes to `${TASK_DIR}qa/qa-input-to-task-fidelity-[source]-[task-slice]-[N].md`. Merge sub-step: consolidate all reports into `${TASK_DIR}qa/qa-input-to-task-fidelity-consolidated.md`.
  - (4) rf-qa-qualitative (SPEC-detail-survival, full intensity only) — Spawn SPEC-Detail-Survival agents IN PARALLEL (PARTITIONED PER §A.3 THRESHOLDS: by TDD section range; K=1 when TDD ≤2000 lines; K=2-3 when TDD >2000 lines). Each agent reads its assigned TDD slice + ALL task files. For its assigned SPEC-NNN subset, reads the original TDD specification, traces through S2 → S4 → BUILD_REQUEST → task file checklist item, and rates detail survival: PRESERVED (exact details in task item), DEGRADED (high-level intent only), LOST (not in any task file). Each writes to `${TASK_DIR}qa/qa-spec-detail-survival-[N].md`. Merge sub-step: consolidate into `${TASK_DIR}qa/qa-spec-detail-survival-consolidated.md`. Runs at full intensity only; skipped at lite/standard.
  - For >4 phases at standard/full intensity: partition task files across additional agents (1 agent per 2 task files) for agents (2) and (3) to prevent context overflow.
  - If issues found: for each failing task file independently, determine K per Rule 24 thresholds based on consolidated post-task-file finding count. Spawn K SEQUENTIAL fix agents (rf-qa, fix_authorization: true) using the Partitioned Fix Agent Prompt — partitioned by task-file (each fix agent gets one or more task-file slices) since each task file is an independent edit target. Then re-spawn the evaluating agents for that task file (fix_authorization: false) to verify. Each task file has its own independent fix cycle. Max 2 fix cycles per task file.

Phase 6 — Presentation:
- Present summary to user: roadmap document path, list of phased task files with phase names and execution order, dependency chain, command to start: `/task [phase-1-task-file-path]`, note that phases should be executed in order.
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date
- `NON-BLOCKING` Suggest downstream execution: "You can now execute the roadmap phases in order using `/task [phase-1-task-file-path]`. Each subsequent phase may depend on prior phase outputs." Present the suggestion, mark this item complete immediately, and do NOT wait for a user response. This item does not gate task completion.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-ROADMAP-<subject>-YYYYMMDD-HHMMSS/TASK-ROADMAP-<subject>-YYYYMMDD-HHMMSS.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, roadmap structure, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review and iterate
6. Create the task file at .dev/tasks/to-do/TASK-ROADMAP-<subject>-YYYYMMDD-HHMMSS/TASK-ROADMAP-<subject>-YYYYMMDD-HHMMSS.md using PART 2 structure
7. Return the task file path
````

**Step 2: Invoke the task-builder skill:**
**CRITICAL: After task-builder completes and outputs TASK_FILE_READY, you MUST continue to Stage B below. Do NOT stop at task-builder's output.**


```
Skill(skill: "task-builder", args: "${TASK_DIR}BUILD-REQUEST.md")
```

The task-builder skill reads the BUILD_REQUEST file, detects `Source: skill-delegated` and `SKIP_RESEARCHERS: true`, skips its own research phase, spawns the rf-task-builder agent, and runs structural and qualitative validation internally. It returns the task file path.

**Note:** Task-builder handles all verification internally — structural validation checks frontmatter, phases, B2 pattern, embedded prompts, parallel spawning instructions, partitioning guidance, and anti-orphaning. Qualitative validation checks operational correctness. No separate verification step is needed in this skill. Proceed directly to Stage B with the returned task file path.

---

## Stage B: Task File Execution

Stage B delegates execution to the `/task` skill, which provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA verification, error handling, and session management.

### Delegation Protocol

1. **Invoke /task** using the Skill tool with `skill: "task"` and `args` set to the task file path from Stage A (e.g., `.dev/tasks/to-do/TASK-ROADMAP-task-management-system-20260407-120000/TASK-ROADMAP-task-management-system-20260407-120000.md`).
2. **Execution transfers to /task**, which reads the task file and processes each checklist item via the F1 loop — spawning subagents as specified in B2 items and running phase-gate QA after each phase (Phase 2+).
3. **No additional execution logic is needed** in this skill since all execution rules (F1 loop, F2 prohibited actions, parallel spawning, F4 modification restrictions, F5 frontmatter protocol, error handling, session resumption) are provided by /task.
4. **QA coverage:** The task file already contains skill-specific QA items (sentinel gate, obligation scan, integration contracts, rf-qa-qualitative at Phase 2, Coverage Validator at Phase 3), and /task adds phase-gate QA on top. This results in intentional, acceptable double QA at gate phases — skill-specific QA uses domain-aware roadmap gates while /task's phase-gate QA verifies "ensuring..." clauses from all items in the phase. Both the skill-embedded QA items and /task's phase-gate QA use lens-based multi-agent evaluation per the QA hardening changes. They evaluate different things: skill items run domain-specific roadmap lenses; /task's phase-gate verifies generic "ensuring..." clause satisfaction.

### What the Task File Must Contain

Since /task does NOT read this SKILL.md during execution, all skill-specific instructions must be baked into the task file during Stage A:

- **Agent prompt templates** customized with specific input analysis topics, section population instructions, and validation criteria
- **Validation checklists and content rules** embedded in "ensuring..." clauses of each B2 item
- **Output paths and file naming conventions** specified in each item (research/, qa/, build-requests/ subdirectories)
- **Depth-tier-specific phase items** selected by Stage A based on the detected tier
- **Roadmap template path** and instructions for template-driven generation (read template → create stub → populate sections → validate sentinels)
- **Nested Skill() invocation syntax** for /task-builder calls in Phase 5
- **All phase-specific context** so each B2 item is fully self-contained — an executor reading only the task file has everything needed to complete each item

**CRITICAL:** `/task` does NOT read this SKILL.md during execution. ALL skill-specific instructions, agent prompts, validation criteria, and content rules must be baked into the task file items during Stage A. This includes prohibited actions: section population agents populate content based on the user's input, they do not modify the template; do not invent requirements not in the input; do not fabricate file paths; do not delete research artifacts after completion.

---

## Agent Prompt Templates

These templates are provided to the task builder (in the BUILD_REQUEST) so it can embed them in the task file's self-contained checklist items. The builder should customize each instance with the specific input content, section assignment, and output path.

**QA Intensity Adaptation (per Template 02 I22) — Roadmap 4-Stage Architecture:**
- lite: Stage 1 reduces to 5 agents:
  (1) rf-qa combined-structural: template-conformance + internal-consistency lenses
  (2) rf-qa combined-structural: evidence-quality + completeness lenses
  (3) rf-qa-qualitative combined-content: actionability + domain-accuracy + crossref-chain + numbers-metrics lenses
  (4) highest-value domain lens: dependency-acyclicity
  (5) 1 fidelity agent (combined coverage + detail-preservation)
  Stage 2: SKIP. Stage 3: SKIP. Stage 4: 1 agent combined.
- standard: Stage 1 uses 10 agents:
  3 rf-qa structural: template-conformance, internal-consistency, evidence-quality
  3 rf-qa-qualitative content: actionability, domain-accuracy, crossref-chain
  2 domain: dependency-acyclicity, obligation-discharge
  2 fidelity agents
  Stage 2: 3 agents (same as full). Stage 3: 2 per BUILD_REQUEST (combined structural+sufficiency + source-fidelity as separate agent). Stage 4: 2 agents.
- full: Use all prompts below as-is (current 4-stage architecture, no changes).

### Input Analyst Agent Prompt

```
You are a technical requirements analyst extracting structured requirements from user input to produce a phased roadmap.

Analyze the user's input and extract all requirements and specifications with unique IDs. Write your findings to [output-path].

Input to analyze: [full user input content or file paths to read]
Input type: [prd / tdd / prd+tdd / partial-doc / free-form / other-doc / combined]
  NOTE: When input_type is tdd or prd+tdd (or combined with TDD component), TDD content yields SPEC-NNN IDs in addition to REQ-NNN IDs from PRD content. See SPEC extraction rules below.
Project name: [project name]
Assigned slice: [source document name + section range, e.g., "PRD sections 1-5, lines 1-800" or "full input if ≤1000 lines"]
Partition context: [K of N total Input Analyst agents, merge target path]

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create your output file immediately with this header:
   ```markdown
   # Input Analysis: [Project Name]

   **Input type:** [type]
   **Source:** [file paths or "inline prompt"]
   **Status:** In Progress
   **Date:** [today]

   ---
   ```

2. As you analyze each section or logical unit of the input, IMMEDIATELY append your findings to the output file using Edit. Do NOT accumulate findings in your context window.

3. After each append, your output file grows. This is correct behavior. Never rewrite the file from scratch.

4. When finished, update the Status line from "In Progress" to "Complete" and append a summary section.

Analysis Protocol:
0. **FIRST: Read the roadmap template as your extraction contract.** Read `.claude/templates/documents/roadmap_template.md`. For each section (S1-S11), read its `<!-- GUIDANCE: ... -->` comment to understand what content kind that section accepts. Note explicitly:
   - S2 Input Analysis accepts requirements/features/components with priorities (Must/Should/Could)
   - S8 Risk Register accepts risks with severity/probability/mitigation/contingency
   - S10 Open Questions accepts unresolved questions with blocking phase annotations
   - S11 Architectural Debt accepts intentional shortcuts and deferred decisions
   - There is NO section for: personas, jobs-to-be-done, business context, competitive analysis, value propositions, vision/strategy, market analysis. These are context that informs HOW you describe requirements but are NOT themselves requirements to be extracted.
   - Architecture, data models, API specs, component inventories, migration plans, phase plans, integration points → these are BUILD-CONTENT for Sections 3-5 (Phase Overview, Phase Details, Dependency Graph). The Phase Designer will use them. Mark them in your output as "build-content" so the Phase Designer knows to consume them.
   - **TDD specifications (SPEC-NNN extraction):** When input_type includes tdd, the following TDD content gets DUAL classification: it is BOTH build-content (flows to Phase Designer for S4 task descriptions) AND coverage-content (gets SPEC-NNN IDs tracked in S2 and S7). TDD specification types: entity field definitions (column names, types, constraints), index specifications (columns, fillfactors), API endpoint signatures (request/response schemas), state machine transition rules (guards, side-effects), error code enumerations (codes, HTTP statuses), performance thresholds (SLOs, benchmarks), test specifications (coverage targets, fixtures), deployment procedures (rollout stages, rollback plans), security specifications (threat mitigations, CSRF requirements, encryption parameters, compliance controls), observability specifications (structured logging formats, monitoring instrumentation, metric definitions, alerting rules). Mark these in your output as "build-content WITH SPEC-NNN" so the Phase Designer consumes them AND they appear in S2/S7 coverage tracking.
   - Only extract content that has a destination in the roadmap template. If content from the user input doesn't fit any section's GUIDANCE, it does not belong in the roadmap (even if it's interesting or important).
1. Read the ENTIRE assigned slice — do not skim, skip sections, or compress within your slice. Every detail matters for coverage. Other slices are handled by peer agents; do NOT read outside your assigned slice.
2. Enumerate every requirement, feature, component, and deliverable with a unique ID: REQ-001, REQ-002, etc. When input includes a TDD, additionally enumerate every specification with SPEC-001, SPEC-002, etc. (see SPEC types in the build-content classification above).
3. For each requirement, record: ID, description, source reference (section/line in input), priority (Must/Should/Could — infer from language if not explicit), complexity estimate (S/M/L)
3b. For each specification (SPEC-NNN, when TDD input is present), record: ID, specification description, source reference (TDD section), type (entity/index/api/state/error/perf/test/deploy/security/observability)
4. Identify scope boundaries — what is explicitly IN scope, what is explicitly OUT of scope, what is ambiguous
5. Note constraints mentioned in the input (performance targets, compatibility requirements, tech stack mandates)
6. Identify dependencies between requirements and specifications (REQ-003 depends on REQ-001, SPEC-005 depends on SPEC-002)
7. Flag ambiguities — requirements that are unclear, contradictory, or underspecified
8. Identify natural phase boundaries — groups of requirements and specifications that belong together

TDD WEIGHTING — IMPLEMENTATION CONTRACT:
When input_type includes tdd (i.e., tdd, prd+tdd, or combined with TDD component), the TDD is the PRIMARY source for task-level implementation detail. The PRD defines WHAT must be true (requirements, acceptance criteria, success metrics) and is the coverage contract. The TDD defines HOW to build it (entities, fields, types, indexes, APIs, state transitions, error codes, algorithms) and is the implementation contract. A roadmap is a build plan — its value is in the Phase Details (S4) task tables that /task-builder consumes to create execution-ready task files. Those task tables MUST contain TDD-level specificity: exact field names and types, exact index definitions with columns, exact state transition counts with guards, exact API signatures with request/response schemas, exact error code enumerations, observability instrumentation specs. When both PRD and TDD are present: use PRD for coverage scope (what to build, S2 REQ-NNN IDs, S7 coverage), use TDD for implementation detail (how to build it, S2 SPEC-NNN IDs, S4 task acceptance criteria). TDD-specific details that are lost or summarized in task descriptions are the #1 cause of incorrect code generation downstream.

PRD-TDD CONFLICT RESOLUTION:
When PRD and TDD contradict on a specific detail (e.g., PRD says 8 error codes, TDD says 12), use the TDD value for SPEC-NNN extraction and flag the contradiction in the Ambiguities section with both source references. The TDD is assumed to be the more recent and more detailed specification. If the PRD explicitly overrides a TDD detail (e.g., PRD says "reduce to 8 error codes from the 12 in the TDD"), use the PRD value and note the override. The Coverage Validators and Source Fidelity agents will verify against whichever value was chosen.

Output Format:
- Requirements table: | ID | Requirement | Source | Priority | Complexity | Dependencies | Notes |
- Specifications table (when TDD input is present): | ID | Specification | Source (TDD section) | Type (entity/index/api/state/error/perf/test/deploy/security/observability) |
  Example row: SPEC-001 | task_templates.slug column VARCHAR(255) UNIQUE | TDD S6.2 | entity
- Scope boundaries section
- Constraints section
- Ambiguities section (with suggested resolutions)
- Phase boundary suggestions

Be thorough. Be specific. Extract EVERY requirement AND every specification — missing a requirement or specification means missing coverage in the roadmap.

Template alignment: The orchestrator will distill your output into roadmap Section 2 (Input Analysis) per the template's `<!-- GUIDANCE: ... -->` comment at `.claude/templates/documents/roadmap_template.md`. Template S2 uses a 4-column REQ table: `ID | Requirement/Feature | Source | Priority` and, when TDD input is present, a separate 4-column SPEC table: `ID | Specification | Source (TDD section) | Type`. Your output may include richer columns (Complexity, Dependencies, Notes) for internal use, but ensure the core columns for both tables are cleanly extractable.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

### Phase Designer Lead Agent Prompt

Spawned via `subagent_type: "rf-analyst"`. The Lead always runs as K=1 — it reads only the merged input analysis file (bounded ≤2000 lines by design) and produces the S3 Phase Overview plus a Per-Phase Slice Plan that drives the N parallel Per-Phase Designer agents in the next stage.

```
You are a technical project planner producing the Phase Overview (S3) for a phased implementation roadmap. Your output is the high-level phase decomposition that downstream Per-Phase Designer agents will expand into S4 detail blocks.

Read the merged input analysis file ONLY (this is bounded ≤2000 lines by design — it is the consolidated output of the Input Analyst partition). Do NOT read the original user input — that has already been processed into the input analysis file. Do NOT read individual research files unless the input analysis file references them as essential.

Inputs:
- Input analysis file: [path to ${TASK_DIR}qa/s2-input-analysis-merged.md]
- Project name: [project name]
- Constraints: [user-specified constraints]
- Output path: [path to ${TASK_DIR}qa/s3-phase-overview.md]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with header.
2. As you design each phase, IMMEDIATELY append to the output file using Edit.
3. Never accumulate the entire phase plan in context.
4. When finished, update Status to Complete and append a summary.

Design Protocol:
0. Read the roadmap template at .claude/templates/documents/roadmap_template.md — focus on S3 GUIDANCE comment (8-column Phase Overview table).
0.1. Honor existing phase structure in the input analysis if present (look for "Phase Boundary Suggestions" section).
1. Read the input analysis file in full — understand requirements, specifications, priorities, dependencies, complexity.
2. Group REQs and SPECs into phases based on dependency order, logical cohesion, risk mitigation, user constraints.
3. For each phase, define ONLY:
   - Phase number and name
   - Goal (1-2 sentences)
   - REQ-NNN / SPEC-NNN IDs covered (list, not detail)
   - Dependencies on prior phases
   - Estimated duration (lightweight)
   - Complexity (S/M/L)
   - Parallelizable (yes/no)
4. Do NOT design task tables (T<phase>.<seq>) — that is Per-Phase Designer's job.
5. Do NOT design Integration Points — that is Per-Phase Designer's job.
6. Do NOT design Dependency Graph (S5) — the orchestrator synthesizes that from per-phase outputs.
7. Output the S3 Phase Overview Table per template column structure: Phase | Name | Goal | Duration | Dependencies | Key Deliverables | Complexity | Parallelizable.
8. Append a "Per-Phase Slice Plan" section listing, for each phase, what build-content slice from the input analysis the Per-Phase Designer for that phase should consume (this is the partitioning key for the next stage).

Output Format:
- S3 Phase Overview Table (8 columns)
- Per-Phase Slice Plan: | Phase | Input Analysis Sections | Build-Content Slice | REQ/SPEC IDs |

Begin your response with the file creation action directly. Do not include conversational preamble.
```

### Per-Phase Designer Agent Prompt

Spawned via `subagent_type: "rf-analyst"`, one instance per phase identified by the Lead (N PARALLEL agents). Each Per-Phase Designer reads only its assigned slice of the merged input analysis plus the relevant codebase research — never the full input — and produces a single S4 Phase Detail block.

```
You are a technical project planner producing the S4 Phase Details block for ONE specific phase of a roadmap. You operate as one of N Per-Phase Designer agents spawned in parallel, each responsible for ONE phase.

Your assigned phase: [Phase number and name from Lead's S3]
Your assigned input analysis slice: [REQ/SPEC IDs and build-content sections this phase covers, per Lead's Per-Phase Slice Plan]

Inputs:
- Phase Overview file (S3): [path to ${TASK_DIR}qa/s3-phase-overview.md]
- Input analysis file (read ONLY the slice for your phase per the Per-Phase Slice Plan): [path to ${TASK_DIR}qa/s2-input-analysis-merged.md]
- Codebase research files relevant to your phase: [paths]
- Output path: [path to ${TASK_DIR}qa/s4-phase-detail-NN.md where NN is your phase number]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with header.
2. As you design each task in your phase, IMMEDIATELY append using Edit.
3. Never accumulate.

Design Protocol (Rule 28 Extract-Before-Compose):
0. Read the roadmap template — focus on S4 GUIDANCE comment (per-phase subsection structure: Objective, Duration, Entry/Exit Criteria, 8-col Task Table, Integration Points 4-col table, Key Deliverables).
0.1. Read your assigned slice of the input analysis ONLY. Do NOT read other phases' slices — those are other agents' responsibility.
0.2. Read the S3 Phase Overview to understand your phase's context (what comes before, what comes after, dependencies).
0.3. SOURCE EXTRACTION (mandatory, before composition). Write `${TASK_DIR}qa/phase-NN-source-extract.md` enumerating every concrete claim your assigned slice contains (field names, types, index specs, state counts, error codes, API signatures, perf thresholds, observability specifics, integration-point artifacts). Use the same table format as BUILD_REQUEST Source-Extractor: `| Kind | Claim | Source Citation | Original Text |`. This is your authoritative universe of claims.
1. For your assigned phase, produce:
   - Objective (1-2 sentences expanding the S3 Goal; concrete nouns `[verbatim: CITATION]` or `[derived from: CITATION]`)
   - Duration estimate
   - Entry criteria (what must be true to start; each criterion marked)
   - Exit criteria (what must be true to complete; each criterion marked)
   - Dependencies on prior phases (specific outputs needed from each, each `[verbatim: CITATION]`)
   - Task table (8 cols: # | ID | Task | Description | Depends On | Acceptance Criteria | Effort | Parallel) — Description and Acceptance Criteria cells MUST have `[verbatim: CITATION]` or `[derived from: CITATION]` markers on every concrete claim
   - Integration Points table (4 cols: Artifact | Type | Created By | Consumed By) — Artifact and Type marked
   - Key Deliverables list — each deliverable marked
2. Use T<phase>.<seq> task IDs where <phase> is YOUR phase number.
3. Anti-consolidation: NEVER merge multiple REQs into a single task. One task per discrete work unit.
4. SPEC handling: SPECs typically become acceptance criteria on the parent REQ task that implements them, NOT standalone tasks. Standalone SPEC tasks only for orphan SPECs with no parent REQ.
5. TDD detail preservation: When input includes TDD, preserve TDD-level specificity in acceptance criteria — exact field names/types, index definitions with columns, state transition counts with guards, error code enumerations, API signatures with schemas, performance thresholds, observability instrumentation. Every TDD-derived detail MUST be `[verbatim: TDD §x Ly-z]` or `[derived from: TDD §x Ly-z]`.
6. Verify that EVERY REQ-NNN and SPEC-NNN in your assigned slice is covered by at least one task in your phase. If you find a REQ/SPEC that doesn't fit your phase, flag it in a "Coverage Gaps" section at the end of your output — do NOT silently drop it.
7. Self-audit before emitting: grep your phase detail output for every number, ID, field name, endpoint, file path, error code. Each match MUST appear in your source-extract OR be marked `[derived from: CITATION]`. ADVERSARIAL STANCE: Assume at least 3 fabrications in your output. Find and correct them. Emit only after audit passes.

Output Format:
- Phase Detail block per template structure
- Coverage Gaps section (REQ/SPECs that should belong to a different phase, or to no phase)

Begin your response with the file creation action directly. Do not include conversational preamble.
```

### Forward Coverage Agent Prompt (rf-qa — Coverage Stage 2.1)

```
You are a coverage validation specialist verifying forward coverage of a phased roadmap.

Perform forward coverage validation: every requirement AND specification from the original input must have at least one task that SEMANTICALLY implements it (not just ID presence in the Coverage Traceability Matrix).

Roadmap path: [path to completed roadmap document]
Original user input: [full user input or file paths]
Assigned slice: [coverage pool (REQ | SPEC) + source section range for large pools]
Partition context: [K of N total Forward Coverage agents, output path suffix -N]
Output path: [output-path]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you validate each REQ/SPEC, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Protocol:
1. Read the ENTIRE assigned slice of the original source document (per the Assigned slice parameter). Do NOT read outside your assigned slice — peer agents cover other slices.
2. Read the roadmap's Section 2 (Input Analysis) and Section 7 (Coverage Traceability Matrix)
3. For EACH REQ and EACH SPEC in S2:
   a. Find the task ID(s) mapped to it in S7
   b. Read the ACTUAL task description in Section 4 (Phase Details)
   c. Verify the task description SEMANTICALLY matches the requirement — not just that the REQ ID appears
   d. Rate match quality: FULL (task clearly implements the req), PARTIAL (task addresses some aspects), PHANTOM (ID present but task doesn't actually implement req), MISSING (no mapping exists)
4. Also extract requirements AND specifications DIRECTLY from the original user input (independently of S2) and verify they appear

Output: | REQ/SPEC ID | Requirement/Specification | S7 Task ID(s) | Match Quality | Evidence |
Verdict: PASS (all FULL or PARTIAL) / FAIL (any PHANTOM or MISSING)

**ADVERSARIAL STANCE:** Assume phantom coverage exists. Your job is to find REQ-to-task and SPEC-to-task mappings where the task doesn't actually implement the requirement or specification.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

### Backward Orphan Agent Prompt (rf-qa — Coverage Stage 2.2)

```
You are a coverage validation specialist detecting orphan tasks (scope creep) in a phased roadmap.

Perform backward coverage validation: every task in the roadmap must trace to at least one requirement or specification.

Roadmap path: [path to completed roadmap document]
Output path: [output-path]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create output file with header
2. Append findings incrementally
3. Never accumulate and one-shot

Protocol:
1. Read roadmap Section 4 (Phase Details) — enumerate ALL task IDs (T<phase>.<seq>)
2. Read roadmap Section 7 (Coverage Traceability Matrix)
3. For EACH task ID in S4: verify it appears in S7 mapped to at least one REQ or SPEC
4. Tasks with no backing requirement or specification = orphan = scope creep flag

Output: | Task ID | Task Description | Mapped REQ/SPEC(s) | Status (Covered/Orphan) |
Verdict: PASS (zero orphans) / FAIL (orphans found)

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

### REQ Detail Preservation Agent Prompt (rf-qa-qualitative)

Spawned via `subagent_type: "rf-qa-qualitative"`. Reads the PRD only (never the TDD). PRD sampling is bounded at 20% so this always runs as K=1.

```
You are a detail preservation specialist verifying that PRD requirement specifics survive into roadmap task descriptions.

Perform detail preservation validation on a random 20% sample of REQs (minimum: all REQs if total < 10, otherwise minimum 10).

Roadmap path: [roadmap-document-path]
Source document (PRD only): [PRD path]
Output path: ${TASK_DIR}qa/qa-coverage-detail-preservation-req.md

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create output file with header.
2. Append findings per sampled REQ.
3. Never accumulate.

Protocol:
1. Read roadmap S2 to get the full REQ-NNN list.
2. Randomly sample 20% of REQs (minimum 10).
3. For EACH sampled REQ:
   a. Find original PRD text describing this requirement.
   b. Find roadmap task description in S4 (via S7 mapping).
   c. Compare: do source-specific details survive? Check for numeric specifics (counts, thresholds), type specifics (enum values), naming specifics (endpoint paths, config keys), compliance/operational specifics (GDPR, SLA, retention).
   d. Rate: PRESERVED / DEGRADED / MISSING.
4. Summary with REQ preservation rate.

Output: | REQ ID | PRD Detail | Task ID | Task Detail | Rating | Missing Detail |
Verdict: PASS (≥80% PRESERVED) / FAIL.

**ADVERSARIAL STANCE:** Assume at least 5 REQ-level details were lost. Find them.

Begin your response with the file creation action directly.
```

### SPEC Detail Preservation Agent Prompt (rf-qa-qualitative, TDD inputs only)

Spawned via `subagent_type: "rf-qa-qualitative"`. Reads the TDD only. Skipped entirely if the input has no TDD component. Partitioned by TDD section range when TDD >3000 lines (K=2-3 in that case); otherwise K=1.

```
You are a detail preservation specialist verifying that TDD specification specifics survive into roadmap task descriptions.

Perform detail preservation validation on a random 20% sample of SPECs (minimum 10 if available; skip this agent entirely if input does not include TDD).

Roadmap path: [roadmap-document-path]
Source document (TDD only): [TDD path]
Assigned TDD slice: [TDD section range, e.g., "TDD sections 1-5" or "full TDD if ≤3000 lines"]
Partition context: [K of N total SPEC-DP agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-coverage-detail-preservation-spec-[N].md

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create output file with header.
2. Append findings per sampled SPEC.
3. Never accumulate.

Protocol:
1. Read roadmap S2 to get the full SPEC-NNN list.
2. Randomly sample 20% of SPECs (minimum 10).
3. For EACH sampled SPEC:
   a. Find original TDD text describing this specification.
   b. Find roadmap task description in S4 (via S7 SPEC-to-Task mapping).
   c. Compare: do TDD-specific details survive? Check for field names and types (VARCHAR(255), UNIQUE, NOT NULL), index definitions (columns, fillfactors, compound keys), API signatures (request/response schemas, HTTP methods), state transition counts and guards, error code enumerations with HTTP status codes, performance thresholds with specific numbers.
   d. Rate: PRESERVED / DEGRADED / MISSING.
4. Summary with SPEC preservation rate.

Output: | SPEC ID | TDD Detail | Task ID | Task Detail | Rating | Missing Detail |
Verdict: PASS (≥80% PRESERVED) / FAIL.

**ADVERSARIAL STANCE:** Assume at least 5 SPEC-level details were lost. Find them.

Begin your response with the file creation action directly.
```

### Web Research Agent Prompt

```
You are a technical researcher gathering external best practices and documentation to inform a phased implementation roadmap.

Research this topic externally and write findings to [output-path].

Topic: [specific external research topic — e.g., phase decomposition best practices, dependency management patterns]
What we already know from input analysis: [brief summary of relevant findings]
Research question context: [the overall roadmap creation context]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for official documentation, guides, and API references relevant to the roadmap topic
2. Search for community patterns, solutions, and best practices for phased implementation
3. Search for tutorials and implementation examples
4. For each finding, document:
   - Source URL
   - Key information extracted
   - How it relates to our roadmap requirements
   - Whether it supports, extends, or contradicts what we found in the input
5. Rate source reliability (official docs > well-maintained repos > blog posts > forum answers)

Output Format:
- Use descriptive headers for each research area
- Always include source URLs
- Mark relevance: HIGH / MEDIUM / LOW for each finding
- End with:
  ## Key External Findings
  [Bullet list of the most important discoveries]

  ## Recommendations from External Research
  [How external findings should influence our roadmap approach]

IMPORTANT: Our codebase and user input are the source of truth. External research adds context and options but does not override verified requirements or code behavior. If you find a discrepancy, note it explicitly.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

### Research Analyst Agent Prompt (rf-analyst — Completeness Verification)

```
You are a research quality analyst verifying the completeness and evidence quality of codebase research before roadmap generation.

Perform a completeness verification of all research files for [topic].

Analysis type: completeness-verification
Task directory: [task-dir-path]
Research directory: [task-dir-path]research/
Research notes file: [task-dir-path]research/research-notes.md
Depth tier: [Quick/Standard/Deep]
Output path: [output-path]

Your job is to independently verify that research agents produced thorough, evidence-based findings
before downstream roadmap population begins. You are the analytical quality gate — be rigorous.

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.
1. FIRST ACTION: Create your output file immediately with a header including topic, date, and status
2. As you complete each checklist item, IMMEDIATELY append findings to the output file using Edit
3. Never accumulate and one-shot

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

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

### Content Lens Agent Prompts (rf-qa-qualitative — 4 Parallel Content Lenses)

#### Lens 1: Actionability (rf-qa-qualitative)

```
Lens: actionability
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total content lens-actionability agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-actionability-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 5 items are too vague to execute. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-actionability agents cover other slices. Report issues only within your slice.

Checklist:
1. Each phase's deliverables are concrete enough for /task-builder to create task files (file paths, component names, not vague categories)
2. Task-level acceptance criteria are testable with pass/fail, not aspirational ("system is stable" = bad, "all unit tests pass with >90% coverage" = good)
3. Entry/exit criteria are pass/fail verifiable, not aspirational
4. Each task in the Task Table is specific enough to be a single checklist item in a task file

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Lens 2: Numbers and Metrics (rf-qa-qualitative)

```
Lens: numbers-metrics
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total content lens-numbers-metrics agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-numbers-metrics-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 3 numeric claims are inconsistent. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-numbers-metrics agents cover other slices. Report issues only within your slice.

Checklist:
1. Total phases count matches actual phase detail blocks
2. Total tasks count matches actual task rows across all phases
3. Effort estimates per task are internally consistent (S/M/L scale used consistently)
4. Duration estimates per phase are realistic given task count and effort
5. Coverage percentage in S7 is arithmetically correct

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Lens 3: Cross-Reference Chain Integrity (rf-qa-qualitative)

```
Lens: crossref-chain
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total content lens-crossref-chain agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-crossref-chain-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 3 cross-reference chains are broken. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-crossref-chain agents cover other slices. Report issues only within your slice.

Checklist:
1. Trace end-to-end: REQ/SPEC (S2) → Phase (S3) → Task (S4) → Coverage (S7) — every link exists
2. Task IDs in Dependency Graph (S5) all exist in Phase Details (S4)
3. Task File Tracker (S6) references all phases from S3
4. Parallelism annotations in S3 don't conflict with dependency annotations in S4 or S5

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Lens 4: Domain Accuracy (rf-qa-qualitative)

```
Lens: domain-accuracy
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total content lens-domain-accuracy agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-domain-accuracy-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 3 domain claims are inaccurate. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-domain-accuracy agents cover other slices. Report issues only within your slice.

Checklist:
1. Claims about codebase match actual code (if verifiable from context)
2. Claims about product match actual capabilities
3. No aspirational features described as current
4. Technology choices in task descriptions match the project's actual tech stack

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

### Structural Lens Agent Prompts (rf-qa — 4 Parallel Structural Lenses)

#### Lens 1: Template Conformance (rf-qa)

```
You are a structural QA specialist focused EXCLUSIVELY on template conformance.

Lens: template-conformance
Report path: [roadmap-document-path]
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total structural lens-template-conformance agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-template-conformance-[N].md
Fix authorization: false (report only)

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you complete each checklist item, IMMEDIATELY append findings to the output file using Edit
3. Never accumulate and one-shot

**ADVERSARIAL STANCE:** Assume this document has at least 5 template conformance errors. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-template-conformance agents cover other slices. Report issues only within your slice.

Your ONLY job is template conformance. Ignore content quality, dependency logic, and coverage — other lens agents handle those.

Checklist:
1. Metadata block plus all 11 content sections (S1-S11) present with content (12 total document blocks) — no remaining {{RF_PLACEHOLDER:*}} sentinels
2. Metadata completeness — all 7 metadata fields populated, dates valid, counts > 0
3. Table structure — Phase Overview (8 cols), Task Table (8 cols), Coverage Matrix (5 cols), Risk Register (6 cols), Integration Points (4 cols), all correctly formatted
4. No placeholder or template artifacts — no {{, }}, TODO, TBD, PLACEHOLDER, [fill in], or template comments remaining
5. Section ordering matches template (Metadata, S1-S11 in order)

Output: | Check | Status | Evidence | for each item. Verdict: PASS/FAIL.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Lens 2: Internal Consistency (rf-qa)

```
You are a structural QA specialist focused EXCLUSIVELY on internal consistency.

Lens: internal-consistency
Report path: [roadmap-document-path]
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total structural lens-internal-consistency agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-internal-consistency-[N].md
Fix authorization: false (report only)

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you complete each checklist item, IMMEDIATELY append findings to the output file using Edit
3. Never accumulate and one-shot

**ADVERSARIAL STANCE:** Assume this document has at least 5 internal contradictions. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-internal-consistency agents cover other slices. Report issues only within your slice.

Checklist:
1. Phase count in S3 overview table matches number of detail blocks in S4 AND matches Metadata `total_phases` field
2. Requirement ID format — all requirement IDs follow REQ-NNN pattern and all specification IDs follow SPEC-NNN pattern consistently in S2 and S7
3. Task ID format — all IDs follow T<phase>.<seq> pattern consistently in S4, S5, S7
4. All "Depends On" references in task tables resolve to existing task IDs or "--"
5. Total task count in Metadata matches actual task count across all S4 phase detail blocks
6. Phase names in S3 match phase names in S4 section headers
7. No contradictions between sections — phase count in S3 matches S4 detail count, REQ and SPEC counts in S2 match S7 row count

Output: | Check | Status | Evidence | for each item. Verdict: PASS/FAIL.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Lens 3: Evidence Quality (rf-qa)

```
You are a structural QA specialist focused EXCLUSIVELY on evidence quality.

Lens: evidence-quality
Report path: [roadmap-document-path]
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total structural lens-evidence-quality agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-evidence-quality-[N].md
Fix authorization: false (report only)

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you complete each checklist item, IMMEDIATELY append findings to the output file using Edit
3. Never accumulate and one-shot

**ADVERSARIAL STANCE:** Assume this document has at least 5 unsubstantiated claims. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-evidence-quality agents cover other slices. Report issues only within your slice.

Checklist:
1. Every requirement and specification in S2 cites a source reference (section/line in original input)
2. Phase Details task descriptions reference specific deliverables, file paths, or component names — not vague categories
3. No assumptions presented as verified facts anywhere in the document
4. No doc-only architectural claims in Phase Details without [UNVERIFIED] tags
5. Risk Register risks are specific and evidence-based, not generic ("things might break")

Output: | Check | Status | Evidence | for each item. Verdict: PASS/FAIL.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Lens 4: Completeness (rf-qa)

```
You are a structural QA specialist focused EXCLUSIVELY on completeness.

Lens: completeness
Report path: [roadmap-document-path]
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total structural lens-completeness agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-completeness-[N].md
Fix authorization: false (report only)

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you complete each checklist item, IMMEDIATELY append findings to the output file using Edit
3. Never accumulate and one-shot

**ADVERSARIAL STANCE:** Assume this document is missing at least 3 required elements. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-completeness agents cover other slices. Report issues only within your slice.

Checklist:
1. Coverage matrix completeness — every REQ and every SPEC from S2 appears in S7, every task in S4 appears in S7. Verify EACH pool independently: count REQs in S2 vs REQs in S7 (must match), count SPECs in S2 vs SPECs in S7 (must match when TDD input present). Zero-SPEC is valid for PRD-only inputs.
2. Integration Points bidirectionality — every "Created By" has a "Consumed By" and vice versa
3. Risk Register has at least 1 risk with severity/probability populated per phase
4. Open Questions have blocking phase annotations where applicable
5. Every phase in S4 has all required subsections: Objective, Duration, Entry Criteria, Exit Criteria, Dependencies, Task Table, Integration Points, Key Deliverables

Output: | Check | Status | Evidence | for each item. Verdict: PASS/FAIL.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```


### Domain Lens Agent Prompts (7 Roadmap-Specific Lenses)

These 7 domain-specific lenses are unique to the roadmap skill and run IN ADDITION to the 8 standard lenses. They target the roadmap's unique quality dimensions that standard lenses don't cover.

#### Domain Lens 1: Dependency Acyclicity (rf-qa)

```
Lens: dependency-acyclicity
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total domain lens-dependency-acyclicity agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-dependency-acyclicity-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 2 circular dependencies exist. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-dependency-acyclicity agents cover other slices. Report issues only within your slice.

Trace ALL dependency chains end-to-end at both phase level (S3, S5) and task level (S4 "Depends On" column). Verify:
1. No circular dependencies at phase level (Phase A depends on Phase B which depends on Phase A)
2. No circular dependencies at task level (T1.3 depends on T2.1 which depends on T1.3)
3. Entry criteria for each phase are satisfiable given the stated dependency order
4. Exit deliverables of Phase N are actually produced before Phase N+1's entry criteria reference them
5. Cross-phase task dependencies in S5 don't create implicit phase-level cycles

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Domain Lens 2: Phase Boundary Correctness (rf-qa-qualitative)

```
Lens: phase-boundary-correctness
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total domain lens-phase-boundary-correctness agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-phase-boundary-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 2 phase boundaries are wrong. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-phase-boundary-correctness agents cover other slices. Report issues only within your slice.

1. Each phase's exit deliverables match the next phase's entry prerequisites
2. No phase assumes outputs from a skipped phase
3. No phase has entry criteria that can never be met given the dependency chain
4. Phase boundaries align with logical groupings (foundations before features, data models before APIs)
5. No single phase is overloaded (contains work that should be split across phases)

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Domain Lens 3: Obligation Discharge (rf-qa)

```
Lens: obligation-discharge
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total domain lens-obligation-discharge agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-obligation-discharge-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 3 obligations are undischarged. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-obligation-discharge agents cover other slices. Report issues only within your slice.

Scan ALL phase details for scaffold terms: mock, stub, skeleton, placeholder, scaffold, temporary, hardcoded, hardwired, no-op, dummy, fake. For EACH found:
1. Identify the component being scaffolded
2. Search ALL later phases for a discharge term referencing the SAME component: replace, wire up, integrate, connect, swap out, remove mock/stub, implement real, fill in, complete
3. Verify the discharge is in a LATER phase (not the same phase, not an earlier phase)
4. Zero undischarged obligations required

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Domain Lens 4: Task-to-Requirement Semantic Match (rf-qa-qualitative)

```
Lens: task-req-semantic-match
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total domain lens-task-req-semantic-match agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-task-req-semantic-match-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 5 task-requirement mappings are phantom. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-task-req-semantic-match agents cover other slices. Report issues only within your slice.

This is the PHANTOM COVERAGE DETECTOR. For EACH REQ-to-Task and SPEC-to-Task mapping in the Coverage Traceability Matrix (S7):
1. Read the requirement or specification description in S2
2. Read the actual task description in S4
3. Verify the task IMPLEMENTS the requirement or specification — not just that the REQ ID appears in S7
4. Rate: GENUINE (task clearly implements req), WEAK (task partially addresses req), PHANTOM (ID present in S7 but task doesn't actually address req)
5. Flag all PHANTOM and WEAK mappings

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Domain Lens 5: Task Granularity (rf-qa-qualitative)

```
Lens: task-granularity
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total domain lens-task-granularity agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-task-granularity-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 3 tasks are too coarse-grained. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-task-granularity agents cover other slices. Report issues only within your slice.

1. Each task in the Task Tables should be specific enough to be a single checklist item in a task file
2. Tasks like "implement the system", "set up infrastructure", "configure the environment" are too vague and must be decomposed
3. Task descriptions should include specific deliverables, not vague categories
4. Each task should have a clear, testable acceptance criterion — not "working correctly" but specific measurable outcomes
5. Anti-consolidation check: no task covers multiple unrelated requirements

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Domain Lens 6: Resource and Effort Realism (rf-qa)

```
Lens: resource-realism
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total domain lens-resource-realism agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-resource-realism-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 2 effort estimates are unrealistic. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-resource-realism agents cover other slices. Report issues only within your slice.

1. Effort estimates per task are internally consistent (S/M/L used consistently)
2. Total phase effort doesn't exceed stated phase duration (a phase with 20 L-effort tasks can't be "1 week")
3. Resource requirements in S9 are specified, not assumed
4. Parallelism claims are realistic (tasks marked "parallel" don't have undeclared dependencies)
5. No phase has zero-effort tasks (every task requires SOME effort)

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Domain Lens 7: Integration Contract Completeness (rf-qa)

```
Lens: integration-contract-completeness
Assigned section slice: [S1-S3 | S4 | S5-S7 | S8-S11 | full roadmap if ≤2000 lines]
Partition context: [K of N total domain lens-integration-contract-completeness agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-lens-integration-contract-completeness-[N].md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least 2 integration contracts are incomplete. Find them.

SCOPE DISCIPLINE: Process ONLY your assigned section slice. Do NOT evaluate content outside your slice — peer lens-integration-contract-completeness agents cover other slices. Report issues only within your slice.

1. Every Integration Points table entry has BOTH "Created By" and "Consumed By" filled
2. Every artifact created in one phase is consumed in another — zero orphans in either direction
3. Cross-phase artifacts referenced in task descriptions match Integration Points table entries
4. The "Consumed By" phase is LATER than the "Created By" phase
5. Every phase transition that produces outputs consumed by later phases has an Integration Points table

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file with Write tool containing ONLY the header (report title, date, lens, verdict placeholder).
2. As you evaluate each section/item, IMMEDIATELY append findings using Edit tool. Do NOT accumulate findings in context.
3. When finished, update the verdict and append the summary section.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```


### Source Fidelity Agent Prompt (rf-qa — 4 Parallel Fidelity Agents)

```
You are a source-document fidelity specialist verifying that the roadmap faithfully represents its source inputs.

Lens: source-fidelity
Roadmap path: [roadmap-document-path]
Assigned source document: [PRD path, TDD path, or original input document path for free-form/other-doc inputs]
Assigned section range: [first half / second half of the assigned source doc]
Task directory: [task-dir-path]
Output path: [output-path]
Fix authorization: false (report only)

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you validate each source section, IMMEDIATELY append findings to the file
3. Never accumulate and one-shot

**ADVERSARIAL STANCE:** Assume the roadmap has lost at least 5 specific details from the source document. Find them.

You read your assigned source document section range AND the FULL roadmap. You check:

1. **Semantic coverage** — for each requirement/spec/feature in your assigned source sections (when assigned TDD sections, explicitly verify SPEC-NNN ID extraction completeness and detail preservation for entity fields, index specs, API signatures, state transitions, error codes, performance thresholds, test specifications, deployment procedures, observability instrumentation), does the roadmap contain a corresponding task that ACTUALLY addresses it (not just mentions the ID)?
2. **Detail preservation** — source-specific details survive into the roadmap:
   - Error code counts (source says 12 error codes → roadmap task mentions 12 error codes, not just "error handling")
   - Field types and names (source says `created_at: timestamp` → roadmap task preserves this)
   - State pairs and transitions (source says 25 state transitions → roadmap preserves count)
   - Threshold values (source says "99.9% uptime" → roadmap task includes this target)
   - Index/key names (source says "idx_project_user" → roadmap task references specific index)
3. **Phantom coverage detection** — Both REQ-NNN and SPEC-NNN IDs present in Coverage Traceability Matrix (S7) must be verified by reading the actual task description to confirm semantic match
4. **Cross-source contradiction flagging** — if multiple source documents exist (e.g., PRD + TDD), flag contradictions between them (e.g., PRD says 8 error codes, TDD says 12; PRD REQ-NNN requirement scope vs TDD SPEC-NNN implementation scope). If only one source document or a free-form input was provided, skip this check
5. **Operational/compliance completeness** — source sections mentioning compliance, security, operational, or regulatory requirements must each have a corresponding roadmap task

Output: | Source Section | Source Detail | Roadmap Location | Match Quality | Notes |
Verdict: PASS / FAIL with specific gaps listed.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```


### BUILD_REQUEST Validation Agent Prompts (2 Per BUILD_REQUEST)

#### BUILD_REQUEST Structural Validation (rf-qa)

```
You are a structural QA specialist validating a BUILD_REQUEST file before /task-builder invocation.

BUILD_REQUEST path: [path]
Roadmap path: [roadmap-document-path]
Output path: ${TASK_DIR}qa/qa-build-request-phase-NN-structural.md
Fix authorization: false

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you validate each section, IMMEDIATELY append findings
3. Never accumulate and one-shot

Checklist:
1. GOAL section present and non-empty
2. WHY section present and non-empty
3. TEMPLATE section specifies 01 or 02
4. CONTEXT FILES section present with at least: roadmap path, original user input path
5. DELIVERABLES section lists specific outputs expected from this phase
6. DEPENDENCIES section specifies prior phase dependencies
7. ACCEPTANCE CRITERIA section has testable pass/fail criteria
8. PHASE-SPECIFIC GUIDANCE section has implementation guidance
9. QA REQUIREMENTS section specifies minimum agent counts (must be >= 6 per gate)
10. No empty sections, no placeholder text

Verdict: PASS / FAIL.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### BUILD_REQUEST Sufficiency Validation (rf-qa-qualitative)

```
You are a content QA specialist validating that a BUILD_REQUEST provides enough context for /task-builder.

BUILD_REQUEST path: [path]
Roadmap path: [roadmap-document-path]
Output path: ${TASK_DIR}qa/qa-build-request-phase-NN-sufficiency.md
Fix authorization: false

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you validate each aspect, IMMEDIATELY append findings
3. Never accumulate and one-shot

Checklist:
1. GOAL is specific enough that task-builder can produce a useful task file WITHOUT reading the entire roadmap (the BUILD_REQUEST must be self-contained)
2. CONTEXT FILES reference the correct source files for this phase. Exception: CONTEXT FILES may contain DEFERRED references for prior-phase task files (not yet created). These are acceptable — task-builder will use roadmap Phase Details as the authoritative source for prior-phase context
3. QA REQUIREMENTS specify adequate agent counts (not 1-2 agents per gate)
4. DELIVERABLES match the roadmap phase's Key Deliverables section
5. ACCEPTANCE CRITERIA match the roadmap phase's Exit Criteria
6. DEPENDENCIES accurately reflect the roadmap's dependency graph

Verdict: PASS / FAIL.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```


### BUILD_REQUEST Source-Extractor Agent Prompt

Insert into Agent Prompt Templates section, immediately after the existing `BUILD_REQUEST Validation Agent Prompts` block. Spawned via `subagent_type: "rf-task-researcher"`. One per phase, PARALLEL across phases. Reads roadmap Phase N's S4/S5/S7/S8/S10/S11 rows + PRD/TDD sections cited in those rows, writes every concrete claim (task IDs, field names, endpoint paths, counts, thresholds, error codes, file paths, metric names, alert names, SPEC-IDs, section citations with line numbers) to `${TASK_DIR}qa/build-request-phase-NN-source-extract.md` with `[ROADMAP Lx-y]` / `[PRD §x Ly-z]` / `[TDD §x Ly-z]` citations.

````
You are a source-extraction specialist producing a per-phase citation manifest that the BUILD_REQUEST Generator consumes. You do NOT compose the BUILD_REQUEST. You ONLY enumerate every concrete claim a downstream generator could reference, with precise citations.

Your phase: [Phase NN — Phase Name from roadmap S3]
Inputs:
- Roadmap path: [path to completed roadmap]
- PRD path (if present): [path]
- TDD path (if present): [path]
- Other source docs: [paths or "none"]
- Output path: ${TASK_DIR}qa/build-request-phase-NN-source-extract.md

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with header (phase number/name, source paths, date, status: In Progress).
2. As you extract each claim, IMMEDIATELY append to the file using Edit.
3. Never accumulate.

Extraction Protocol:
1. Read roadmap Phase NN's S4 detail block, and the S5 dependency graph rows mentioning Phase NN, and the S7 rows covering Phase NN, and S8 risks for Phase NN, and S10 open questions for Phase NN, and S11 debt for Phase NN. Record the line ranges you read as `[ROADMAP Lx-y]`.
2. For every PRD/TDD/source-doc section referenced in those roadmap rows (or implied by the task descriptions), read that section in full. Record `[PRD §x Ly-z]` or `[TDD §x Ly-z]` citations.
3. Enumerate EVERY concrete claim a generator could need:
   - Task IDs (T<phase>.<seq>) and their descriptions, effort, parallel annotation
   - Field names, types, constraints (e.g., `organizations.slug VARCHAR(255) UNIQUE NOT NULL`)
   - Index names and column lists
   - API endpoint paths, HTTP methods, request/response schema field names
   - Error code names and HTTP status codes (exact enum values)
   - State machine states and transition counts/guards
   - Performance thresholds (specific numbers)
   - Observability: metric names, alert names, log format field names
   - File paths the phase touches
   - Runbook names and P0/P1/P2 classifications
   - Compliance/regulatory requirements (GDPR, SOC2, SLA targets)
   - Acceptance criteria (verbatim from roadmap)
   - Integration Points: artifact names, Created By / Consumed By phases
   - Dependencies: prior-phase task IDs or outputs
4. For EACH extracted claim, emit exactly one row in a single table:
   `| Kind | Claim | Source Citation | Original Text |`
   Where:
   - Kind = one of `task-id`, `field`, `index`, `endpoint`, `error-code`, `state`, `threshold`, `metric`, `alert`, `file-path`, `runbook`, `compliance`, `acceptance-criteria`, `integration-point`, `dependency`, `other`.
   - Claim = the concrete value exactly as stated in source (e.g., `organizations.slug VARCHAR(255) UNIQUE NOT NULL`).
   - Source Citation = `[ROADMAP L<start>-<end>]` or `[PRD §<n> L<start>-<end>]` or `[TDD §<n> L<start>-<end>]`.
   - Original Text = the verbatim text snippet from the source (short, ≤200 chars; longer snippets abbreviated with `...`).
5. Also emit a "Section Map" block listing which roadmap/PRD/TDD sections were read and their line ranges, so the generator knows the bounded extraction universe.
6. Do NOT infer, paraphrase, or invent. If a claim is not grep-findable in source, do not include it. If a roadmap task description says "implement rate limiting" but no concrete tier/threshold appears in PRD or TDD, record the task reference only — not a fabricated tier.

Anti-fabrication discipline:
- Every row MUST cite a grep-verifiable source location. If you cannot produce one, drop the row.
- Prefer verbatim quotes over paraphrase. The Original Text column is the ground truth the generator and validator will grep.
- When source documents contradict each other (PRD vs TDD), emit BOTH rows with source-citations and a Notes column explaining the contradiction.

Output Format:
```
# Source Extract — BUILD_REQUEST Phase NN

## Section Map
| Source | Sections Read | Line Ranges |

## Claims
| Kind | Claim | Source Citation | Original Text |

## Contradictions (if any)
| Claim A | Source A | Claim B | Source B | Notes |
```

ESCALATION — No team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, TaskList. Return the output file path as your final output.

Begin with the file creation action directly. No conversational preamble.
````


### BUILD_REQUEST Generator Agent Prompt

Insert immediately after the Source-Extractor Agent Prompt. Spawned via `subagent_type: "rf-analyst"`, one per phase, parallel with other phases' generators.

```
You are the BUILD_REQUEST Generator for ONE specific roadmap phase. You compose the BUILD_REQUEST file for Phase NN using EXCLUSIVELY the claims in the source-extract file. You are forbidden from composing from memory, context, or inference.

Your phase: [Phase NN — Phase Name]
Inputs:
- Source-extract file (AUTHORITATIVE): ${TASK_DIR}qa/build-request-phase-NN-source-extract.md
- BUILD_REQUEST format template: (see SKILL.md Per-phase BUILD_REQUEST format)
- Roadmap path: [path] (for reading only, NOT for extracting new claims — the extract file already contains every claim you may reference)
- Output path: ${TASK_DIR}build-requests/BUILD_REQUEST-phase-NN-[name].md

fix_authorization: false (you WRITE the BUILD_REQUEST; you do NOT edit roadmap or source docs)

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create the BUILD_REQUEST file with the required section headers and empty bodies.
2. Populate each section incrementally using Edit.
3. Never accumulate.

Composition Protocol:

STEP 0 — Read the source-extract file FIRST. It is the complete universe of claims you may reference. If a claim you think belongs in the BUILD_REQUEST is NOT in the extract, you MUST NOT include it. Instead, log a "Missing Extract" note in the Task Log of the task directory and proceed without that claim.

STEP 1 — Populate sections using ONLY extract claims:
- GOAL: 1-2 sentences derived from roadmap Phase Goal (cite `[ROADMAP Lx-y]`). Concrete nouns must be from extract.
- WHY: cite `[ROADMAP Lx-y]` for context; if you quote PRD/TDD motivation, cite `[PRD §x Ly-z]` / `[TDD §x Ly-z]`.
- DEPTH_TIER: copy from input-analysis scope discovery.
- TEMPLATE: copy exactly `02 (complex task — this phase depends on prior phase outputs)`.
- CONTEXT FILES: list each source file with explicit LINE RANGES (not just paths). Example: `TDD: docs/TDD_RIGORFLOW_PLATFORM.md §8 L1447-1808 (API Specs), §14 L2649-2871 (Observability)`. Line ranges MUST come from extract's Section Map.
- DELIVERABLES: one bullet per concrete deliverable from extract (task IDs, artifact names, file paths). Mark each `[verbatim: CITATION]` or `[derived from: CITATION]`.
- DEPENDENCIES: prior-phase task IDs + specific outputs. Each item `[verbatim: CITATION]`.
- ACCEPTANCE CRITERIA: copy verbatim from roadmap phase Exit Criteria. Each criterion `[verbatim: ROADMAP Lx-y]`.
- PHASE-SPECIFIC GUIDANCE: concrete implementation hints drawn from extract's TDD rows. Each hint `[verbatim: TDD §x Ly-z]` or `[derived from: TDD §x Ly-z]`.
- QA REQUIREMENTS: standard template text + any phase-specific QA requirements from extract.
- SOURCE CITATIONS: at the end, list every citation you used (unique set), with file + line range. This is the quick-reference for the validator.

STEP 2 — Verbatim vs Derived markers:
- For EVERY concrete claim (numbers, IDs, field names, paths, endpoint specs, error codes, thresholds, counts, names):
  - If the claim appears WORD-FOR-WORD in the extract's Original Text column → append `[verbatim: CITATION]` after the claim.
  - If the claim is paraphrased, summarized, combined from multiple rows, or inferred → append `[derived from: CITATION]`.
- If a sentence contains multiple concrete claims, mark each claim individually or the sentence collectively if all cite the same source.
- Bare concrete claims without markers are a fabrication signal and will be flagged by the validator.

STEP 3 — Self-Audit Before Emitting:
Before declaring done, perform this self-audit:
1. Grep your BUILD_REQUEST for every number, ID pattern (`T<n>.<n>`, `REQ-<n>`, `SPEC-<n>`), endpoint path (`/` followed by alphanumeric), error code (UPPER_SNAKE_CASE tokens), field name (lowercase or snake_case tokens near types), file path (containing `/`), quoted names.
2. For EACH match, verify: (a) the claim appears in the extract's Claims table OR (b) the claim is marked `[derived from: CITATION]`.
3. If any match fails both criteria, that claim is a FABRICATION — remove it or replace it with an extract-backed value or `[derived from: CITATION]` marker.
4. ADVERSARIAL STANCE: Assume you have fabricated AT LEAST 3 claims. Find and correct them before emitting.
5. Emit only after audit passes.

Anti-fabrication discipline:
- You may NOT invent task IDs. Use only task IDs present in the extract.
- You may NOT invent endpoint names, error codes, field names, or table names. All such tokens must come from extract.
- You may NOT cite PRD/TDD sections not in the extract's Section Map.
- If the phase's roadmap content legitimately requires a synthesis of multiple extract rows (e.g., "implement all 3 rate-limit tiers"), mark it `[derived from: EXTRACT-ROW-IDs]` with the row references.
- When in doubt, prefer being incomplete (drop the claim, log in Missing Extract) over fabricating.

Output Format: the BUILD_REQUEST follows the per-phase format template in SKILL.md, extended with verbatim/derived markers and a SOURCE CITATIONS section at the end.

ESCALATION — No team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, TaskList. Return the output file path as your final output.

Begin with the file creation action directly. No conversational preamble.
```


### BUILD_REQUEST Source-Fidelity Validator Agent Prompt

Insert immediately after the Generator prompt. Spawned via `subagent_type: "rf-qa"`, `fix_authorization: false`. Runs as the 3rd Stage 3 agent per BR, parallel with structural + sufficiency validators.

````
You are the source-fidelity validator for ONE specific BUILD_REQUEST. Your job is to detect fabrications — concrete claims that are not grep-verifiable in the source-extract file or source documents.

BUILD_REQUEST path: [${TASK_DIR}build-requests/BUILD_REQUEST-phase-NN-[name].md]
Source-extract file: [${TASK_DIR}qa/build-request-phase-NN-source-extract.md]
Roadmap path: [roadmap-document-path]
PRD path (if present): [path or "none"]
TDD path (if present): [path or "none"]
Output path: ${TASK_DIR}qa/qa-build-request-phase-NN-source-fidelity.md

fix_authorization: false (report only)

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with `# QA Report — BUILD_REQUEST Phase NN Source-Fidelity` header + phase number + verdict placeholder.
2. Append findings per claim incrementally.
3. Never accumulate.

ADVERSARIAL STANCE: Assume this BUILD_REQUEST contains AT LEAST 5 fabrications. Find them.

Validation Protocol:

STEP 1 — Read the source-extract file. Build a set of grep-findable tokens from its Claims table's Original Text column. This is your "verified token set."

STEP 2 — Read the BUILD_REQUEST. For every concrete claim:
1. Extract the token (task ID, field name, endpoint path, error code, threshold number, table name, metric/alert name, section citation, file path, runbook name, state name, counts).
2. Check if the claim is marked `[verbatim: CITATION]` or `[derived from: CITATION]`.
3. For `[verbatim: ...]` claims: grep the cited source location (the extract file row OR directly the roadmap/PRD/TDD at the cited line range) to confirm the token appears word-for-word. If mismatch → FABRICATION or MISCITATION.
4. For `[derived from: ...]` claims: open the cited extract row(s) or source location; verify the derivation is reasonable (the derived claim is a fair summary/combination of the cited source text). Subjective fabrications (claims that go beyond what the cited source says) → FABRICATION.
5. For UNMARKED concrete claims: every unmarked concrete claim is a lint violation — the BUILD_REQUEST format requires markers. Report it. Additionally grep-check the token against the extract set; if missing → FABRICATION. If present but unmarked → MARKER-MISSING (lint, not fabrication).

STEP 3 — Verify CONTEXT FILES line ranges. For every CONTEXT FILE entry with a line range, open the source file at that line range and confirm the cited content actually exists there (e.g., if CONTEXT FILES says `TDD §8 L1447-1808 (API Specs)`, open TDD §8 L1447-1808 and confirm it's the API Specs section). Mismatches → WRONG-CITATION.

STEP 4 — Cross-check internal contradictions:
- Count task IDs listed in GOAL/DELIVERABLES vs count implied by roadmap Phase NN. If they differ without explanation → CONTRADICTION.
- Scan for contradictory numeric claims (e.g., "8 error codes" in one section, "12 error codes" in another) → CONTRADICTION.
- Scan for duplicate task IDs, duplicate SPEC IDs → DUPLICATION.

STEP 5 — Verify SOURCE CITATIONS block at end of BUILD_REQUEST:
- Every citation used in the body appears in this block.
- Every citation in this block was actually referenced in the body.
- No citations to files/sections not in the extract's Section Map.

Output Format:
```
# QA Report — BUILD_REQUEST Phase NN Source-Fidelity

**Phase:** NN
**BUILD_REQUEST:** [path]
**Source-extract:** [path]
**Date:** [today]
**Adversarial target:** at least 5 fabrications expected

## Overall Verdict: PASS | FAIL

## Summary
- Concrete claims checked: X
- Verbatim markers verified: X
- Derived markers verified: X
- Unmarked concrete claims: X
- Fabrications detected: X (CRITICAL)
- Mis-citations detected: X (IMPORTANT)
- Marker-missing lint violations: X (MINOR)
- Contradictions / duplications: X

## Issues Found
| # | Severity | Location | Token | Claim in BUILD_REQUEST | Expected Source | Why it failed |

## Recommendations
[What the generator must fix before this BR can proceed to Phase 5]

## QA Complete
```

Severity: CRITICAL (fabrication), IMPORTANT (miscitation / wrong-citation / contradiction), MINOR (marker-missing / cosmetic).

ESCALATION — No team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, TaskList. Edit tool is for appending to your OWN output file only. Do NOT modify the BUILD_REQUEST.

Begin with file creation. No conversational preamble.
````


### Post-Task-File End-to-End Validation Agent Prompts (4 Agents at Full Intensity)

#### Cross-Task-File Consistency (rf-qa)

```
You are a consistency specialist verifying that task files created from BUILD_REQUESTs are internally consistent.

Task file paths: [list of all created task file paths]
Roadmap path: [roadmap-document-path]
Roadmap Dependency Graph: Section 5
Output path: ${TASK_DIR}qa/qa-cross-task-consistency.md
Fix authorization: false

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you validate each task file pair, IMMEDIATELY append findings
3. Never accumulate and one-shot

Checklist:
1. Dependencies between task files match the roadmap's dependency graph (S5)
2. Phase N's task file doesn't reference outputs from Phase N+1's task file
3. Entry criteria of each task file are satisfiable given prior task file's exit deliverables
4. No task file references a deliverable that no other task file produces
5. Phase ordering in task files matches roadmap phase ordering

Verdict: PASS / FAIL.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Roadmap-to-Task Fidelity (rf-qa-qualitative)

```
You are a fidelity specialist verifying task files faithfully implement the roadmap's requirements and specifications.

Task file paths: [list of all created task file paths]
Roadmap path: [roadmap-document-path]
Roadmap Phase Details: Section 4
Roadmap Coverage Matrix: Section 7
Output path: ${TASK_DIR}qa/qa-roadmap-to-task-fidelity.md
Fix authorization: false

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you validate each task file, IMMEDIATELY append findings
3. Never accumulate and one-shot

Checklist:
1. Each task file's scope matches its roadmap phase (no work from a different phase)
2. Task item counts roughly match roadmap task counts per phase
3. Acceptance criteria in task files match roadmap exit criteria
4. No task file includes work that the roadmap assigned to a different phase
5. Task file QA gates specify adequate agent counts (per I22 qa_intensity)
6. Every REQ-NNN from S7 Coverage Matrix has a corresponding checklist item in a task file that implements it
7. Every SPEC-NNN from S7 Coverage Matrix (when TDD present) has a corresponding checklist item whose acceptance criteria reference the specification's details
8. No roadmap S4 task was dropped during BUILD_REQUEST generation (compare S4 task count per phase vs task file item count)

Verdict: PASS / FAIL.

Begin your response with the file creation action directly. Do not include conversational preamble, summaries of what you plan to do, or meta-commentary.
```

#### Input-to-Task Fidelity (rf-qa)

```
You are an end-to-end fidelity specialist. You verify that the ORIGINAL user input content survived through the entire pipeline into the final task files.

Original user input: [full user input or file paths to PRD/TDD/prompt]
Task file paths: [list of all created task file paths]
Assigned slice: [source-doc type (PRD|TDD|free-form) + task-file slice (e.g., "task files for Phases 1-3" or "task files for Phases 4-6")]
Partition context: [K of N total Input-to-Task Fidelity agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-input-to-task-fidelity.md
Fix authorization: false

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you validate each requirement/specification, IMMEDIATELY append findings
3. Never accumulate and one-shot

Protocol:
1. Read the ENTIRE assigned slice of the original source document independently (do not rely on S2 extraction). Your slice is defined by the Assigned slice parameter — typically (source-doc type × task-file slice). Do NOT read outside your assigned slice; peer agents cover other slices.
2. Extract requirements and specifications directly from the source
3. For EACH requirement/specification you identify:
   a. Search ALL task files for a checklist item that addresses it
   b. If found: verify the task item's acceptance criteria preserve the source detail
   c. Rate: PRESERVED (detail in task item), DEGRADED (high-level only), LOST (not in any task file)
4. Produce gap report

Output: | Source Ref | Requirement/Spec | Task File | Task Item | Rating | Missing Detail |
Verdict: PASS (all PRESERVED or DEGRADED-minor) / FAIL (any LOST or DEGRADED-critical)

**ADVERSARIAL STANCE:** Assume at least 5 requirements or specifications were lost in the Input -> Roadmap -> BUILD_REQUEST -> Task File pipeline. Find them.

Begin your response with the file creation action directly. Do not include conversational preamble.
```

#### SPEC-Detail-Survival (rf-qa-qualitative, full intensity only)

```
You are a TDD detail preservation specialist. You trace TDD specifications through the full pipeline to verify implementation-level detail survived into task files.

Original TDD: [TDD file path]
Roadmap path: [roadmap-document-path]
BUILD_REQUEST paths: [list of BUILD_REQUEST file paths]
Task file paths: [list of all created task file paths]
Assigned slice: [TDD section range, e.g., "TDD sections 1-5" or "full TDD if ≤2000 lines"]
Partition context: [K of N total SPEC-Detail-Survival agents, output path suffix -N]
Output path: ${TASK_DIR}qa/qa-spec-detail-survival.md
Fix authorization: false

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you trace each SPEC, IMMEDIATELY append findings
3. Never accumulate and one-shot

Protocol:
1. Read roadmap Section 2 to get the SPEC-NNN subset matching your assigned TDD slice (per the Assigned slice parameter). Do NOT process SPECs outside your assigned slice; peer agents cover them.
2. Randomly sample 20% of SPECs (minimum 10 if available)
3. For EACH sampled SPEC-NNN:
   a. Read the ORIGINAL TDD text for this specification
   b. Find the SPEC in roadmap S2 — verify detail level
   c. Find the corresponding S4 task description — verify detail level
   d. Find the BUILD_REQUEST that covers this phase — verify SPEC referenced
   e. Find the task file checklist item — verify acceptance criteria preserve exact detail
   f. Rate the full chain: PRESERVED (exact detail at every step), DEGRADED (detail lost at step [N]), LOST (SPEC absent from task file)
4. Produce trace report

Output: | SPEC ID | TDD Detail | S2 | S4 | BUILD_REQUEST | Task File Item | Chain Rating | Where Lost |
Verdict: PASS (>80% PRESERVED) / FAIL (<80% or any critical SPEC LOST)

**ADVERSARIAL STANCE:** Assume at least 5 TDD specifications lost implementation detail during the pipeline. Trace them.

Begin your response with the file creation action directly. Do not include conversational preamble.
```


### Serialized Fix Authorization Protocol

When multiple QA agents evaluate the same document (Stage 1 lens-based QA), fixes are SERIALIZED to prevent conflicting parallel edits:

1. **Report phase** — All lens agents spawn in parallel with `fix_authorization: false`. They REPORT findings only (no edits to the document).
2. **Consolidation** — Read all lens agent reports, merge findings into a single consolidated findings file. Deduplicate overlapping findings. Severity-rate: CRITICAL / IMPORTANT / MINOR.
3. **Fix phase** — Count fixable findings in the consolidated file. Determine fix-agent count K per Rule 24 thresholds (≤15→K=1, 16-40→K=2-3, 41-100→K=4-6, 100+→HALT). Partition findings by category or section range. Spawn K SEQUENTIAL fix agents with `fix_authorization: true` — fix agent N+1 does NOT start until fix agent N has returned. Each agent receives its partition of findings (finding IDs + allowed file regions) and applies only those fixes. Sequential execution satisfies I20's anti-churn requirement without capping total fix volume.
4. **Verification phase** — Determine V per document-size thresholds (≤2000→V=2, 2000-5000→V=4, 5000+→V=6). Spawn V verification agents in parallel (`fix_authorization: false`), split appropriately between rf-qa and rf-qa-qualitative, to confirm fixes were applied correctly and no new issues were introduced. (Verification confirms fix application, not original detection — the scope is narrower than the initial evaluation. Verification agents scale with document size to maintain coverage after fixes land.)
5. **Iteration** — If verification finds new issues, repeat steps 3-4. Maximum cycles vary by sub-stage (this section documents the per-stage budgets defined in SKILL PHASES TO ENCODE — it does not override them): Stage 1 lens QA: max 3 fix cycles. Stage 1 fidelity: max 2 fix cycles (lower because fidelity issues tend to require source-document re-reading, not iterative editing). Stage 2 coverage: max 3 fix cycles. Stage 3 per-BUILD_REQUEST: max 2 fix cycles. Stage 4 post-task-file: max 2 fix cycles. If issues remain after the maximum cycles, HALT and report unresolved issues.

**Why serialized (not parallel):** Parallel fix authorization causes churn. Agent A fixes line 50 one way, Agent B fixes line 50 a different way. The next round has to fix contradictions. SEQUENTIAL partitioned fix authorization (one fix agent running at a time, each on a non-overlapping partition) preserves this anti-churn property while lifting the total-fix-count ceiling. One-agent-per-all-fixes is the degenerate case (K=1) for small finding counts; at scale, K>1 sequential agents are required.

**Where this applies:** Every QA gate in the roadmap skill that spawns 3+ agents on the same file: Stage 1 lens-based QA (15 agents), Stage 1 fidelity gate (4 agents). Stages 2-4 validate different files so parallel is acceptable.

**Note on domain lenses:** The design spec listed 5 domain lenses; this skill implements 7 (adding task-granularity and resource-realism) and renames "BUILD_REQUEST completeness" to "integration-contract-completeness" for clarity. The additional lenses are improvements over the spec (more lenses = more issues caught).

### Partitioned Fix Agent Prompt

Spawned via `subagent_type: "rf-qa"` with `fix_authorization: true`. Used at every fix-cycle gate that runs K SEQUENTIAL fix agents per Rule 24 thresholds. Agent N+1 does NOT start until agent N has returned.

```
You are a fix agent applying corrections to a document. You are one of K SEQUENTIAL fix agents; agent N-1 has already completed, and you MUST finish before agent N+1 starts.

Your partition:
- Assigned findings: [list of finding IDs from the consolidated findings file — e.g., "F1, F3, F7, F12-F18"]
- Assigned file region: [line range or section labels where your fixes land — e.g., "Section 4 (Phase Details), lines 800-1400" or "S7 coverage matrix rows only"]
- Consolidated findings file: [path]
- Target document: [path — e.g., the roadmap document or task file]

fix_authorization: true

CRITICAL — Scope discipline:
1. Apply ONLY the findings in your assigned partition. Do NOT apply findings outside your partition — another fix agent is handling those.
2. Stay within your assigned file region. Do NOT modify content outside that region — another fix agent may be handling those edits in a subsequent sequential step.
3. Do NOT re-interpret findings. Apply them exactly as specified in the consolidated findings file.

Protocol:
1. Read the consolidated findings file. Filter to your assigned finding IDs.
2. For each assigned finding:
   a. Locate the target content in the document (within your assigned file region).
   b. Apply the Edit tool with the fix specified in the finding.
   c. Verify the edit landed (read the modified section or grep for a post-edit anchor).
3. Log fix outcomes (succeeded / failed / skipped with reason) in a summary block appended to the consolidated findings file under a "## Fix Agent [N of K] — Applied" section.
4. Return a completion summary: fixes applied, fixes skipped (with reason), and the next fix agent's partition boundary if applicable.

ESCALATION — No team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, TaskList. Return your completion summary as your final output.

Begin with Read of the consolidated findings file. No conversational preamble.
```

### Coverage Matrix Populator Agent Prompt

Spawned via `subagent_type: "rf-analyst"`. Used by EDIT 12 S7 scale branch when REQ+SPEC >50 to populate the Coverage Traceability Matrix rows in parallel. Partitioned by coverage pool (REQ / SPEC), further by TDD section range when SPEC >200.

```
You are a coverage matrix populator generating the S7 Coverage Traceability Matrix rows for an assigned coverage pool.

Your partition:
- Coverage pool: [REQ | SPEC]
- Assigned ID range: [e.g., "REQ-001 to REQ-200" or "SPEC-001 to SPEC-200" or "SPEC-201 to SPEC-420"]
- Output path: ${TASK_DIR}qa/s7-matrix-[pool]-[N].md

Inputs:
- Merged input analysis (for your pool's full ID list): ${TASK_DIR}qa/s2-input-analysis-merged.md
- Merged phase details (for task IDs and their REQ/SPEC coverage annotations): ${TASK_DIR}qa/s4-phase-detail-NN.md (all files)

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create output file with header (pool name, assigned ID range, status: In Progress).
2. As you build each row, IMMEDIATELY append to the output file using Edit.
3. Never accumulate all rows in context.

Protocol (Rule 28 Extract-Before-Compose):
0. SOURCE EXTRACTION. Write `${TASK_DIR}qa/s7-matrix-[pool]-[N]-source-extract.md` enumerating, for every ID in your assigned range: ID, description (verbatim from merged input analysis), TDD SPEC-kind (for SPEC pool), and which phase detail file(s) contain covering tasks. Format: `| ID | Description | Source Citation | Covering Task IDs (from phase detail files) |`. This is your authoritative row list.
1. Read merged input analysis; filter to your Coverage pool + Assigned ID range.
2. Read all merged phase detail files; build a reverse index of Task ID → REQ/SPEC IDs covered.
3. For EACH ID in your assigned range (drawn from the source-extract file):
   a. Lookup the Task IDs that cover it (from the reverse index).
   b. If zero task coverage: mark orphan, add to a "Orphans" section at the end of your output.
   c. Write row: | [Pool]-NNN | Description [verbatim: CITATION] | Covering Task IDs [verbatim: PHASE-DETAIL-FILE Lx-y] | Phase(s) |
4. Self-audit before emitting: grep your output for every Pool-NNN ID and every T<n>.<n> task ID. Each must appear in your source-extract. ADVERSARIAL: Assume ≥3 fabrications. Find them.
5. Append a summary at the end: total rows, orphan count.

Output format (per row):
| ID | Description | Covering Task IDs | Phase(s) |

ESCALATION — No team context. Return your output path as final output.

Begin with the file creation action directly.
```

### Risk Register Populator Agent Prompt

Spawned via `subagent_type: "rf-analyst"`. Used by EDIT 12 S8 scale branch when risks >20, partitioned by phase.

```
You are a risk register populator generating S8 Risk Register rows for an assigned phase range.

Your partition:
- Assigned phases: [e.g., "Phases 1-3" or "Phases 4-5"]
- Output path: ${TASK_DIR}qa/s8-risks-[N].md

Inputs:
- Merged phase details (for your assigned phases): ${TASK_DIR}qa/s4-phase-detail-NN.md (your phases only)
- Scope discovery output: ${TASK_DIR}research-notes.md
- Any scope-discovery risks file if present

Protocol (Rule 28 Extract-Before-Compose):
0. SOURCE EXTRACTION. Write `${TASK_DIR}qa/s8-risks-[N]-source-extract.md` enumerating every risk indicator in your assigned phases: external dependencies, untested integrations, deferred decisions, vendor lock-ins, performance assumptions, security gaps, data-migration hazards. Cite each with `[PHASE-DETAIL-FILE-NN Lx-y]` or `[RESEARCH-NOTES Lx-y]`. Format: `| Indicator | Phase | Source Citation | Original Text |`.
1. Create output file with header.
2. For each assigned phase, consume your source-extract rows (do NOT scan phase details a second time for new indicators).
3. Write each risk as a row: | Risk ID | Phase | Description [verbatim: CITATION] or [derived from: CITATION] | Severity | Probability | Mitigation [derived from: CITATION] | Contingency [derived from: CITATION] |. Severity and Probability are assessments; they should be justified by the source citation.
4. Self-audit before emitting: grep output for every phase number, component name, and quantitative claim. Each must appear in source-extract. ADVERSARIAL: Assume ≥2 fabrications.
5. Append a summary count at the end.

ESCALATION — No team context. Return output path as final output.

Begin with the file creation action directly.
```

### Open Questions Populator Agent Prompt

Spawned via `subagent_type: "rf-analyst"`. Used by EDIT 12 S10 scale branch when questions >20, partitioned by blocking phase.

```
You are an open questions populator generating S10 Open Questions rows for an assigned blocking phase.

Your partition:
- Assigned blocking phase: [Phase N, OR "cross-phase" for questions that block multiple phases]
- Output path: ${TASK_DIR}qa/s10-questions-[N].md

Inputs:
- Aggregated open questions file (orchestrator-prepared): lists ambiguities from Input Analyst merged output + Per-Phase Designer Coverage Gaps + Stage 1 QA unresolved issues, each tagged with blocking phase.

Protocol (Rule 28 Extract-Before-Compose):
0. SOURCE EXTRACTION. Write `${TASK_DIR}qa/s10-questions-[N]-source-extract.md` enumerating every question/ambiguity sourced from: Input Analyst merged Ambiguities section, Per-Phase Designer Coverage Gaps, Stage 1 QA unresolved issues. Cite each with source + line range. Format: `| Question | Source Citation | Original Text | Suggested Blocking Phase |`.
1. Create output file with header.
2. Filter your source-extract to your assigned blocking phase.
3. For each question, write: | Question ID | Question [verbatim: CITATION] | Blocking Phase(s) | Proposed Resolution [derived from: CITATION] | Severity (blocking / advisory) |.
4. Self-audit before emitting: every Question ID must resolve to a source-extract row. ADVERSARIAL: Assume ≥2 fabrications.
5. Append a summary count at the end.

ESCALATION — No team context. Return output path as final output.

Begin with the file creation action directly.
```

### Architectural Debt Populator Agent Prompt

Spawned via `subagent_type: "rf-analyst"`. Used by EDIT 12 S11 scale branch when debt items >15, partitioned by phase or category.

```
You are an architectural debt populator generating S11 Architectural Debt rows for an assigned phase or debt category.

Your partition:
- Assigned scope: [e.g., "Phases 1-3" OR "stub-term category" OR "migration-pending category"]
- Output path: ${TASK_DIR}qa/s11-debt-[N].md

Inputs:
- Obligation scan findings from Phase 2: ${TASK_DIR}qa/obligation-scan.md (if present)
- Merged phase detail files (for deferred decisions): ${TASK_DIR}qa/s4-phase-detail-NN.md
- Stub/mock/placeholder references catalog from scope discovery (if present)

Protocol (Rule 28 Extract-Before-Compose):
0. SOURCE EXTRACTION. Write `${TASK_DIR}qa/s11-debt-[N]-source-extract.md` enumerating every debt item in your assigned scope: obligation scan findings, phase detail deferred decisions, stub/mock/placeholder catalog. Cite each with source + line range. Format: `| Debt Indicator | Category | Source Citation | Original Text | Discharge Phase (if any) |`.
1. Create output file with header.
2. Filter your source-extract rows to your assigned scope.
3. For each debt item, write: | Debt ID | Description [verbatim: CITATION] | Originating Phase | Category | Discharge Phase | Blocking Risk [derived from: CITATION] |.
4. Self-audit before emitting: every Debt ID resolves to an extract row; every Phase number verified against roadmap S3. ADVERSARIAL: Assume ≥2 fabrications.
5. Append a summary count at the end.

ESCALATION — No team context. Return output path as final output.

Begin with the file creation action directly.
```

### Source Document Verification Agent Prompt (rf-qa — Step 2.VERIFY)

```
You are a source document fidelity verification specialist. You read ONE source document (PRD or TDD) alongside the full populated roadmap and verify implementation-level fidelity.

Assigned source document: [PRD path or TDD path]
Roadmap path: [roadmap-document-path]
Output path: ${TASK_DIR}qa/qa-source-verification-[source-type].md
Fix authorization: false (report only)

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file immediately with header
2. As you validate each REQ/SPEC, IMMEDIATELY append findings to the file
3. Never accumulate and one-shot

Protocol:
1. Read the ENTIRE assigned source document
2. Read roadmap Section 2 (Input Analysis) to get the full REQ and SPEC list
3. Read roadmap Section 7 (Coverage Traceability Matrix) for REQ/SPEC-to-Task mappings
4. For EACH REQ-NNN (if assigned PRD) or EACH SPEC-NNN (if assigned TDD) in S2:
   a. Find the task ID(s) mapped to it in S7
   b. Read the ACTUAL task description and acceptance criteria in Section 4
   c. Compare the source document detail against the task detail:
      - For PRD requirements: do the acceptance criteria in S4 match the PRD's acceptance criteria?
      - For TDD specifications: do the task descriptions preserve specific details?
        * Entity field definitions (column names, types like VARCHAR(255), constraints like UNIQUE/NOT NULL)
        * Index specifications (columns, fillfactors, compound keys)
        * API endpoint signatures (request/response schemas, HTTP methods)
        * State machine transitions (guard conditions, side-effects, exact transition count)
        * Error code enumerations (specific codes with HTTP status mappings)
        * Performance thresholds (exact SLO numbers, benchmark targets)
        * Test specifications (coverage targets, fixture requirements)
        * Deployment procedures (rollout stages, rollback steps)
        * Observability specifications (structured logging formats, metric definitions, alerting rules)
   d. Rate: FAITHFUL (task captures source detail), PARTIAL (task mentions topic but loses specifics like field types, index names, threshold values), MISSING (task does not address the requirement/specification)
5. Produce gap report

Output: | REQ/SPEC ID | Source Detail | Task ID | Task Detail | Verdict | Missing Details |
Verdict: PASS (all FAITHFUL or PARTIAL with minor losses) / FAIL (any MISSING or PARTIAL with critical detail loss)

**ADVERSARIAL STANCE:** Assume the roadmap has lost at least 5 source-specific details. Find them. A verdict of 0 gaps requires evidence of exhaustive verification.

Begin your response with the file creation action directly. Do not include conversational preamble.
```

---

## Roadmap Document Structure

The final roadmap document follows this structure, defined by the roadmap template at `.claude/templates/documents/roadmap_template.md`. The section-population agents and orchestrator produce content that replaces template sentinels to populate this format.

```markdown
# Roadmap: [Project Name]

## Metadata
- **Source input:** [description of input type and content]
- **Source path(s):** [file paths to input documents]
- **Created:** [date]
- **Total phases:** [count]
- **Total tasks:** [count across all phases]
- **Estimated scope:** [S/M/L]
- **Estimated duration:** [estimate]

---

## 1. Executive Summary
[1-2 paragraph summary: what's being built, why, phased approach, expected outcome, critical path]

---

## 2. Input Analysis
[Requirements and specifications enumerated with IDs for traceability]
| ID | Requirement/Feature | Source | Priority |
|-----|---------------------|--------|----------|
| REQ-001 | [requirement] | [source ref] | [Must/Should/Could] |

[When TDD input is present, specifications enumerated with SPEC-NNN IDs:]
| ID | Specification | Source (TDD section) | Type |
|-----|---------------|---------------------|------|
| SPEC-001 | task_templates.slug column VARCHAR(255) UNIQUE | TDD S6.2 | entity |

---

## 3. Phase Overview
| Phase | Name | Goal | Duration | Dependencies | Key Deliverables | Complexity | Parallelizable |
|-------|------|------|----------|-------------|------------------|------------|----------------|

---

## 4. Phase Details
### Phase 1: [Name]
**Objective:** [goal]
**Duration:** [estimate]
**Entry Criteria:** [what must be true to start]
**Exit Criteria:** [what must be true to complete]
**Dependencies:** [prior phases]

#### Task Table
| # | ID | Task | Description | Depends On | Acceptance Criteria | Effort | Parallel |
|---|-----|------|-------------|-----------|---------------------|--------|----------|

#### Integration Points
| Artifact | Type | Created By | Consumed By |
|----------|------|-----------|-------------|

#### Key Deliverables
- [deliverable 1]
- [deliverable 2]

[Repeat for each phase]

---

## 5. Dependency Graph
[ASCII diagram + structured table showing phase and cross-phase task dependencies]

---

## 6. Task File Tracker
| Phase | Task File | BUILD_REQUEST | Status | Depends On | Blocks | Created |
|-------|-----------|---------------|--------|-----------|--------|---------|

---

## 7. Coverage Traceability Matrix
| Req/Spec ID | Requirement/Specification | Phase | Task ID(s) | Status |
|--------|---------------------|-------|-----------|--------|

Coverage: [X/Y] requirements covered ([percentage]%). When TDD input present: [A/B] specifications covered ([percentage]%). Omit specification count for PRD-only inputs.

---

## 8. Risk Register
| Risk | Severity | Probability | Phase(s) Affected | Mitigation | Contingency |
|------|----------|------------|-------------------|------------|-------------|

---

## 9. Resource Requirements
| Resource | Phase(s) | Notes |
|----------|---------|-------|

---

## 10. Open Questions
| # | Question | Impact | Blocking Phase(s) | Suggested Resolution |
|---|----------|--------|-------------------|---------------------|

---

## 11. Architectural Debt & Post-Completion Items
| Item | Reason Deferred | Impact if Not Addressed | Suggested Timeline |
|------|----------------|------------------------|-------------------|
```

---

## Section-to-Agent Mapping Table (Reference)

This table maps each roadmap section to the agent type responsible for populating it during Phase 2 of the task file. The roadmap uses direct template population (stub -> populate -> validate), not a separate synthesis/assembly pipeline.

| Roadmap Section | Populating Agent Type | Source Data |
|----------------|----------------------|-------------|
| Metadata | Orchestrator (inline) | User input, scope discovery |
| 1. Executive Summary | Orchestrator (inline) | User input, Input Analyst output |
| 2. Input Analysis | Input Analyst agent (1-N agents per §A.3 thresholds) | Full user input (documents, prompts); extracts REQ-NNN + SPEC-NNN IDs |
| 3. Phase Overview | Phase Designer Lead (always 1 agent) | Merged Input Analyst output only |
| 4. Phase Details | Per-Phase Designer (N agents, one per phase from S3) | S3 Per-Phase Slice Plan, assigned slice of merged input analysis, codebase research |
| 5. Dependency Graph | Orchestrator synthesis from per-phase outputs (no dedicated agent) | Merged s4-phase-detail-NN files |
| 6. Task File Tracker | Orchestrator (inline) | Phase Overview (one row per phase, all "pending") |
| 7. Coverage Traceability Matrix | Orchestrator (inline) when REQ+SPEC ≤50; OR N Coverage Matrix Populator agents (rf-analyst) when >50, partitioned by REQ pool / SPEC pool, further by TDD section range when SPEC >200. Coverage Validator verifies in Phase 3. | Section 2 requirement IDs and specification IDs, Section 4 task IDs |
| 8. Risk Register | Orchestrator (inline) when risks ≤20; OR N Risk Register Populator agents (rf-analyst) when >20, partitioned by phase | Phase Details, scope discovery |
| 9. Resource Requirements | Orchestrator (inline) | Phase Details, codebase research |
| 10. Open Questions | Orchestrator (inline) when questions ≤20; OR N Open Questions Populator agents (rf-analyst) when >20, partitioned by blocking phase | Ambiguities from Input Analyst, unresolved from scope discovery |
| 11. Architectural Debt | Orchestrator (inline) when debt items ≤15; OR N Architectural Debt Populator agents (rf-analyst) when >15, partitioned by phase or category | Obligation scan findings, Phase Details |

**Depth tier adjustment:** For Quick tier, the orchestrator populates all sections inline. For Standard/Deep tier, Input Analyst and Phase Designer agents handle their respective sections. For Deep tier with many phases (6+), consider spawning per-phase subagents for Section 4 to avoid context limits.

**Phase Designer split — depth-tier note:** The Phase Designer Lead always runs as K=1 regardless of depth tier (it reads the bounded merged input analysis only). Per-Phase Designers always parallelize across N phases (one agent per phase from S3's Per-Phase Slice Plan). What varies by depth tier is the richness of output per agent (Quick = lightweight per-phase blocks; full = full 8-column task tables + Integration Points + TDD detail preservation), not the agent-count shape — the Lead stays at K=1 and the Per-Phase Designers stay at N (one per phase) in every depth tier.

---

## Roadmap Quality Review Checklist

**This checklist is enforced by the 4-stage QA architecture** (see Phase 2-5 validation gates in the task phases above). Stage 1 distributes these criteria across 15 lens agents (4 structural + 4 content + 7 domain-specific), each evaluating ONE quality dimension. The Stage 1 fidelity gate (2-4 agents depending on input type; 4 for prd+tdd, 2 for single-source or free-form inputs) verifies source-document fidelity. Stage 2 (3 agents) validates coverage. Stage 3 (~18-24 agents) validates BUILD_REQUESTs. Stage 4 (2 agents) validates cross-task-file consistency. Total: 44-48 evaluating agents minimum (assumes 6 phases; formula: 15 lens + 2-4 fidelity (2 for single-source, 4 for prd+tdd) + 2 source-verification + 3 coverage + 3×N BUILD_REQUEST + 4 post-task-file-validation where N = phase count), plus fix/verification agents as needed. All use serialized fix authorization.

The 10 criteria (used by rf-analyst):

1. Roadmap section headers match the expected format from the Roadmap Document Structure template (11 sections + Metadata)
2. Tables use the correct column structure (Phase Overview 8-col, Task Table 8-col, Coverage Matrix 5-col, Risk Register 6-col, Integration Points 4-col)
3. No content was fabricated beyond what the user input and research files contain
4. Findings cite actual file paths and evidence (not vague descriptions)
5. Phase details include specific deliverables, testable acceptance criteria, and T<phase>.<seq> task IDs
6. Dependency graph is acyclic with all phases represented
7. All cross-references between sections are consistent: every REQ and every SPEC in S2 is covered in S7, every phase in S3 has a detail subsection in S4, every task ID in S7 exists in S4
8. **No doc-only claims in Phase Details or Task Tables.** Verify that Sections 4 and 7 only contain requirements backed by the user's input or code-traced evidence.
9. **Integration contracts validated.** Every Integration Points table entry has both a "Created By" and "Consumed By" — no orphan artifacts, no missing creators.
10. **Key finding coverage.** Each research file's Summary/Key Takeaway section contains findings that should be reflected in the populated sections. Verify that the strongest findings are represented.

The rf-qa agent adds 2 additional checks (11-12): content rules compliance and hallucinated file path detection. If QA fails, the QA agent fixes issues in-place (when authorized) and remaining unfixed issues trigger re-population of affected sections.

---

## Roadmap Population Process

**The template IS the contract.** Every section in the template has a `<!-- GUIDANCE: ... -->` comment defining what content kind that section accepts. Section-population agents MUST read the GUIDANCE comment for their assigned section BEFORE generating content. Content that has no matching template section does not belong in the roadmap (even if it's interesting or important in the source document). Business context, personas, competitive analysis, vision statements, and similar "framing" content INFORM how sections are written (e.g., the Executive Summary may reference the business problem) but are NOT themselves copied into any section. The roadmap is a build plan, not a copy of the input.

The population step reads the roadmap template and populates it section by section using agent outputs and user input. Follow these steps:

1. **Copy the roadmap template** to the output path — all `{{RF_PLACEHOLDER:*}}` sentinels intact. This is the document stub.
2. **Replace sentinels in order** — for each section, read the template's `<!-- GUIDANCE: ... -->` comment for that section to understand the expected content format, table structure, and rules, then generate content (using agent output or inline analysis) and replace the sentinel using Edit. One section at a time. Never one-shot the entire roadmap.
3. **Verify no remaining sentinels** — scan for `{{RF_PLACEHOLDER:*}}` after all sections are populated. Any remaining = FAIL.
4. **Cross-check internal consistency** — verify that:
   - Requirements and specifications in S2 all appear in S7 Coverage Traceability Matrix
   - Phase count in S3 overview matches S4 detail blocks
   - Dependency Graph in S5 represents all dependencies from S3 and S4
   - Task IDs are consistent across S4, S5, and S7 (T<phase>.<seq> format)
   - Integration Points tables in S4 have no orphan artifacts
   - Open Questions in S10 aren't answered elsewhere in the roadmap

---

## Validation Checklist

Before presenting the roadmap to the user, validate against this checklist (this is encoded in the task file's 4-stage QA architecture: Stage 1 lens-based + fidelity in Phase 2, Stage 2 coverage in Phase 3, Stage 3 BUILD_REQUEST validation in Phase 4, Stage 4 cross-task validation in Phase 5):

- [ ] All 11 roadmap sections present and populated (no remaining `{{RF_PLACEHOLDER:*}}` sentinels)
- [ ] Metadata fields all populated with valid values (dates, counts > 0)
- [ ] Executive Summary references the project name and phased approach
- [ ] Input Analysis has REQ-NNN IDs with priorities for every identified requirement and SPEC-NNN IDs with types for every identified specification
- [ ] Phase Overview table has all 8 columns populated, dependencies are acyclic
- [ ] Phase Details: every phase has objective, duration, entry/exit criteria, 8-column task table, Integration Points, key deliverables
- [ ] Task IDs follow T<phase>.<seq> format consistently across S4, S5, and S7
- [ ] Dependency Graph is acyclic, connected (no orphan phases), and represents all declared dependencies
- [ ] 100% forward coverage — every REQ and every SPEC from S2 has >= 1 task in S7
- [ ] Backward coverage — every task in S4 traces to >= 1 REQ or SPEC in S7 (no orphan tasks / scope creep)
- [ ] Zero undischarged scaffold obligations (obligation scan passes)
- [ ] Zero orphan artifacts and zero missing creators in Integration Points tables
- [ ] All "Depends On" references in task tables resolve to existing task IDs or "--"
- [ ] Risk Register has at least 1 risk with severity/probability populated
- [ ] Open Questions have blocking phase annotations where applicable
- [ ] Tables used over prose for multi-item data throughout
- [ ] No assumptions presented as verified facts
- [ ] No doc-only architectural claims without [UNVERIFIED] tags
- [ ] Input hash computed and stored in metadata and `.roadmap-state.json`
- [ ] Stage 1 lens-based QA completed with 15+ lens agents (4 structural + 4 content + 7 domain-specific)
- [ ] Stage 1 source-document fidelity gate completed with 2-4 fidelity agents (4 for prd+tdd: 2 PRD + 2 TDD; 2 for single-source or free-form inputs). When TDD is present, the 2 TDD-assigned fidelity agents MUST explicitly verify SPEC-NNN extraction completeness (every TDD specification matching the 10-type taxonomy — entity, index, api, state, error, perf, test, deploy — has a SPEC-NNN ID in S2; fidelity agents use this taxonomy to independently identify what SHOULD have been extracted) and detail preservation (field types, index names, error codes, state transitions survive into S4 task descriptions)
- [ ] Source Document Fidelity Verification (Step 2.VERIFY) ran after Stage 1 QA, with verification agents reading original PRD/TDD + populated roadmap. Gap report produced. All MISSING/PARTIAL gaps either remediated in S4 tasks or documented in S10 Open Questions with justification.
- [ ] All Stage 1 fixes applied via serialized fix protocol (report-only → consolidate → single fix agent → verify)
- [ ] Stage 2 coverage validation completed with 3 agents (forward semantic + backward orphan + detail preservation)
- [ ] Stage 3 BUILD_REQUEST validation completed with 3 agents per BUILD_REQUEST
- [ ] Stage 4 post-task-file-creation validation completed with 2 agents (cross-consistency + alignment)
- [ ] Total evaluating agents across all 4 stages: 44-48 minimum (assumes 6 phases; formula: 15 lens + 2-4 fidelity (2 for single-source, 4 for prd+tdd) + 2 source-verification + 3 coverage + 3×N BUILD_REQUEST + 4 post-task-file-validation where N = phase count), plus fix/verification agents as needed

---

## Content Rules (Non-Negotiable)

These rules govern how content is written within research files, agent outputs, and the final roadmap. They prevent bloat, ensure consistency, and keep the output actionable.

| Rule | Do | Don't |
|------|-----|-------|
| **Source code** | Summarize behavior in tables and prose with key signatures | Reproduce full function bodies, interfaces, config files |
| **Architecture** | Use tables and ASCII diagrams | Multi-paragraph prose for what could be a table row |
| **Comparisons** | Use comparison tables with clear criteria | Prose-based side-by-side descriptions |
| **File inventories** | Table: Path / Purpose / Key Exports | List files in paragraph form |
| **Data flow** | ASCII diagram or numbered step list | Multi-paragraph narrative |
| **Phase decomposition** | Structured per-phase blocks with task tables, entry/exit criteria, Integration Points | Running prose describing what each phase does |
| **Coverage matrices** | Table: Req/Spec ID / Requirement/Specification / Phase / Task ID(s) / Status | Narrative description of what covers what |
| **BUILD_REQUESTs** | Structured fields: GOAL, WHY, TEMPLATE, CONTEXT FILES, DELIVERABLES, DEPENDENCIES, ACCEPTANCE CRITERIA | Free-form prose describing what task-builder should do |
| **Validation gates** | Checklist items with pass/fail criteria | Prose description of what to check |
| **Evidence** | Inline citations: requirement IDs (`REQ-001`) and specification IDs (`SPEC-001`), task IDs (`T01.03`), file paths | "The roadmap covers X" without referencing specific IDs |

**General content principles:**
- Tables over prose whenever presenting multi-item data
- Conciseness over comprehensiveness — the roadmap should be scannable, not exhaustive prose
- Every requirement and specification needs coverage — if you can't trace it to a task, it belongs in Open Questions
- Prefer ASCII diagrams for dependency relationships over paragraph descriptions

---

## Critical Rules

Two execution-discipline rules (task-file-source-of-truth, maximize-execution-parallelism) are enforced by the `/task` skill during Stage B and do not appear here. The rules below govern Stage A (scope discovery, roadmap creation, task file creation) and the content quality standards for all agents.

Violations compromise roadmap quality.

1. **Incremental writing is mandatory — ZERO TOLERANCE.** Every agent's FIRST ACTION must be creating its output file on disk using Write (frontmatter/header only). All subsequent content is appended using Edit, one section at a time. NEVER accumulate content in context and attempt a single large Write — this is the #1 failure mode across all agents. It hits max token output limits and freezes the process, losing all work. The procedure is: Write (create file with header) → Edit (append section 1) → Edit (append section 2) → ... → Edit (update Status to Complete). This applies to: input analysts, phase designers, coverage validators, section-population agents, QA reports, and the task file builder.

2. **Codebase is source of truth.** Web research supplements but never overrides verified code findings. Internal documentation is treated with the same skepticism as external sources unless code-verified.

3. **Evidence-based claims only.** Every finding must cite actual file paths, requirement IDs, task IDs, or function names. No assumptions, no inferences, no guessing. If you can't verify it, mark it as "Unverified — needs confirmation."

4. **Default to Deep.** Unless the request is clearly simple with <5 requirements, use the Deep tier. When in doubt, go deeper.

5. **No one-shotting roadmaps.** Agents must write incrementally as they analyze and design. The orchestrator must populate the roadmap section by section. This is non-negotiable.

6. **Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, codebase-retrieval for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations.

7. **Gap-driven web research.** Do not web search everything up front. First analyze the input and codebase thoroughly, identify specific gaps, then target web research at those gaps. This keeps web research focused and efficient.

8. **Preserve research artifacts.** Research files, agent outputs, and QA reports persist after the roadmap is written. They serve as the evidence trail for all claims and enable future re-investigation. Do NOT delete research files, agent outputs, or QA reports after roadmap completion.

9. **Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. The section-population phase relies on these connections to build a coherent picture across requirement groups.

10. **No lossy extraction.** Pass the FULL user input to every agent that needs it. Do not compress, summarize, or extract key points. The LLM reads the full input directly — lossy extraction causes missed requirements and incomplete coverage.

11. **Template-driven output.** The roadmap MUST follow the template structure at `.claude/templates/documents/roadmap_template.md`. Do not invent a different format or skip sections. Every section in the template must appear in the output.

12. **Validate against original input, not intermediary.** Coverage checks compare the roadmap against the ORIGINAL user input, not against the Input Analysis section. The Input Analysis may have missed requirements — the Coverage Validator independently extracts requirements from the original input. When TDD is present, coverage checks MUST include SPEC extraction from TDD content — both REQ and SPEC must be independently verified against the original input.

13. **Preserve structure.** If the user's input contains tables, code blocks, specs, or structured data, preserve that structure in the roadmap's Phase Details and Task Tables. Do not convert structured input to prose.

14. **100% coverage is non-negotiable.** Every requirement AND every specification from the user's input must appear in the Coverage Traceability Matrix with at least one task covering it. If a requirement or specification cannot be covered, it goes in Open Questions with a blocking annotation — it does NOT get silently dropped.

15. **Zero undischarged obligations.** If any phase uses scaffold terms (mock, stub, placeholder, temporary, etc.), a later phase MUST discharge them. The obligation scan is a hard gate — undischarged obligations block completion.

16. **Nested Skill() syntax for /task-builder invocations.** Phase 5 items must use `Skill(skill: "task-builder", args: "<BUILD_REQUEST-path>")` to invoke /task-builder. Do not attempt to create task files directly — /task-builder handles research, quality gates, and validation.

17. **BUILD_REQUESTs persist as artifacts.** BUILD_REQUEST files are NOT temporary — they persist in `${TASK_DIR}build-requests/` and are re-runnable. If /task-builder fails on one phase, the user can re-invoke it on that specific BUILD_REQUEST without regenerating the roadmap.

18. **QA gates are checklist items, not prose.** Every QA gate specified in QA_GATE_REQUIREMENTS must appear in the generated task file as a `- [ ]` checklist item following B2 self-contained pattern. QA gates described only in prose or comments are invisible to the F1 executor and will be skipped.

19. **Granularity floor.** Richer input must produce more phases, tasks, and deliverables — not fewer. A PRD+TDD with 50 requirements must produce a more detailed roadmap than a free-form prompt with 5. The number of phases, tasks, and the specificity of deliverables should scale with input complexity. If a complex input produces fewer phases or less detail than a simple input, the phase decomposition has failed. This prevents the LLM from collapsing rich structured input into a handful of vague phases.

20. **Template-as-contract discipline.** Every extraction agent (Input Analyst, Phase Designer, section-population agents) MUST read the roadmap template FIRST and use its sections and GUIDANCE comments as the extraction contract. Content from the user's input only enters the roadmap if it has a matching template section. Personas, JTBD, competitive analysis, business context, and vision content inform HOW requirements are written but are NOT themselves extracted as requirements. This prevents the analyst from treating every paragraph in the input as something that must be preserved in the output. Build-content (architecture, data models, APIs, existing phase plans) is the primary source for Sections 3-5 (Phase Overview, Phase Details, Dependency Graph); coverage-content (requirements with REQ-NNN IDs and specifications with SPEC-NNN IDs) is the source for Section 2 (Input Analysis) and Section 7 (Coverage Traceability Matrix). When input_type includes tdd, TDD specifications get DUAL classification: they are both build-content (flow to Phase Designer for S4 task descriptions) and coverage-content (tracked in S2/S7 with SPEC-NNN IDs).

21. **Single-agent large-input prohibition.** No single agent may read more than ~1000 lines of input at any discovery, analysis, extraction, or verification stage. Large inputs MUST be partitioned into slices, with one agent per slice spawned in parallel. The rf-task-researcher agent type is permitted per slice but not as a replacement for parallelism. Violations cause shallow coverage and defeat the Deep-tier depth guarantee.

    **Stages this rule applies to** (non-exhaustive — apply universally):
    - A.3 scope discovery (partitioning thresholds defined inline at §A.3)
    - Phase 2 Section Population: Input Analyst (S2), Phase Designer Lead (S3), Per-Phase Designers (S4)
    - Phase 2 Stage 1 Source-Document Fidelity Gate (already partitioned)
    - Step 2.VERIFY Source Document Verification (already partitioned)
    - Phase 3 Coverage Validation: Forward Coverage, Detail Preservation
    - Phase 5 Stage 4 Post-Task-File Validation: Input-to-Task Fidelity, SPEC-Detail-Survival

    **Partitioning-key heuristic per stage:**
    - Input Analyst — by source document, then by section range within each
    - Phase Designer — Lead reads merged input analysis only (always 1 agent); Per-Phase Designers always partition by phase (one agent per phase from S3)
    - Forward Coverage — by coverage pool (REQ vs SPEC), then by source section range for large pools
    - Detail Preservation — always split by coverage pool (REQ-DP reads PRD only, SPEC-DP reads TDD only); SPEC-DP further partitioned by TDD section range when TDD >3000 lines
    - Input-to-Task Fidelity — by source-doc type × task file slice
    - SPEC-Detail-Survival — by TDD section range / by sample subset

    **Lint check:** Any agent prompt in this skill that contains the phrase "Read the ENTIRE [user input | source document | original input | original user input | full TDD | full PRD]" without a corresponding `Assigned slice` parameter is a Rule 21 violation. The phrase "Read the ENTIRE assigned slice" is the compliant form.

22. **No scope/cost-anxiety pauses during execution.** Once a task file begins executing (via /task or any execution loop), the executor MUST process every item sequentially to completion. It MUST NOT pause mid-execution to present the user with options like "stop here and review, or continue to phase N?" or to flag scope/cost/time concerns. Scope is established at task file creation time. Cost is committed when the user invokes execution. The only permitted mid-execution halts are: all items blocked by the same unrecoverable issue, phase-gate QA failing 3 fix cycles, or an item output fundamentally invalidating the rest of the task. "This will take a while" / "Phase N is expensive" / "the user might want to review" are NOT valid halt reasons. Pausing for these reasons violates the F1 loop discipline and the skill's trust model.

23. **Lens-based QA minimums are non-negotiable.** No DOCUMENT QA gate (Stage 1 lens-based review) in the roadmap skill may use fewer than 6 agents total. Cross-artifact validation stages (Stage 2 coverage, Stage 3 per-BUILD_REQUEST, Stage 4 post-task-file) are exempt from this minimum because they validate specific cross-references rather than full document quality — their agent counts are defined per-stage in the SKILL PHASES TO ENCODE section. The Stage 1 fidelity gate (2-4 agents) is also exempt as it validates source-document fidelity, not document quality. The Stage 1 document QA gate uses 15 lens agents minimum (4 structural + 4 content + 7 domain-specific). The Stage 1 fidelity gate uses 2-4 agents (4 for prd+tdd, 2 for single-source or free-form inputs). Stage 2 uses 3 agents. Stage 3 uses 3 per BUILD_REQUEST. Stage 4 uses 2. Single-agent DOCUMENT QA gates are PROHIBITED — they rubber-stamp. The total evaluating-agent count across all 4 stages is 44-48 minimum (assumes 6 phases; formula: 15 lens + 2-4 fidelity (2 for single-source, 4 for prd+tdd) + 2 source-verification + 3 coverage + 3×N BUILD_REQUEST + 4 post-task-file-validation where N = phase count). Task files generated by /task-builder that specify fewer than 6 agents at any document QA gate will be REJECTED during task-builder's qualitative validation.

24. **Serialized fix authorization with scope partitioning.** When 3+ QA agents evaluate the same document, ALL agents report findings first (fix_authorization: false), findings are consolidated, then fix agents apply corrections SERIALLY (one at a time, never concurrently). The number of fix agents is determined by consolidated-findings count:

    **Fix-agent scope thresholds:**
    - ≤15 findings: K=1 fix agent applies all corrections
    - 16-40 findings: K=2-3 SEQUENTIAL fix agents, partitioned by finding category or section range
    - 41-100 findings: K=4-6 SEQUENTIAL fix agents, partitioned by category + section range
    - 100+ findings: HALT — finding volume suggests structural problem requiring orchestrator review before continuing

    **What "sequential" means:** Fix agent 1 completes all its assigned fixes (returns successfully), THEN fix agent 2 spawns with a non-overlapping partition, and so on. No two fix agents with `fix_authorization: true` run at the same time. This preserves the anti-churn intent of the original rule (concurrent writes on the same file cause conflicts) while lifting the arbitrary "one agent regardless of scope" cap that breaks at scale.

    **Partitioning keys for fix work** (pick one per stage, not all):
    - By finding category: structural / content / coverage / cross-reference / integration-contract
    - By section range: S1-S4 / S5-S7 / S8-S11 / Task File Tracker / external refs
    - By finding severity: CRITICAL batch, IMPORTANT batch, MINOR batch — each its own fix agent if each batch warrants it

    Parallel fix authorization on the same file is PROHIBITED. Sequential partitioned fix authorization is MANDATORY at scale.
25. **TDD specifications get tracked IDs.** TDD specifications get SPEC-NNN IDs tracked in S2 and S7 alongside PRD REQ-NNN IDs. SPEC-NNN extraction is mandatory when input_type includes tdd. Coverage is 100% for both REQ and SPEC. A roadmap that extracts REQ-NNN but not SPEC-NNN from a prd+tdd input is incomplete.
26. **Source Document Fidelity Verification is mandatory.** For all input types that include source documents (prd, tdd, prd+tdd), Step 2.VERIFY runs AFTER Stage 1 QA passes and BEFORE Phase 3 Coverage Validation. Skipping source verification is prohibited. If verification agents find PARTIAL or MISSING fidelity for any REQ/SPEC, the remediation loop (Step 2.VERIFY.FIX) MUST run before proceeding. Unresolvable gaps MUST be documented in S10 Open Questions — they cannot be silently dropped.
27. **TDD is the implementation contract.** When input_type includes tdd, the TDD is the PRIMARY source for task-level implementation detail. Task descriptions in S4 MUST preserve TDD-specific details (field names/types, index definitions, state transition counts, error code enumerations, API signatures, performance thresholds, observability instrumentation). A task description that summarizes TDD content as high-level intent (e.g., 'implement state machine' instead of 'implement 5-state state machine with 25 transitions: draft->submitted, submitted->in_review...') is a PARTIAL fidelity finding in Step 2.VERIFY.
28. **Source-fidelity across all translation steps.** Every generator agent in the pipeline (Per-Phase Designer, Populator agents for S7/S8/S10/S11, BUILD_REQUEST Source-Extractor, BUILD_REQUEST Generator) MUST perform Extract-Before-Compose: produce a per-agent source-extract file enumerating every concrete claim with `[ROADMAP Lx-y]` / `[PRD §x Ly-z]` / `[TDD §x Ly-z]` citations BEFORE writing its primary output. Every concrete claim in the primary output (task IDs, field names, endpoint paths, error codes, table names, index names, state counts, thresholds, metric names, alert names, file paths, runbook names, compliance items) MUST be marked `[verbatim: CITATION]` (word-for-word match to source) or `[derived from: CITATION]` (paraphrase/summary/combination, with the source row(s) cited). Every generator MUST self-audit its output (grep own output for concrete tokens, cross-check against source-extract, remove fabrications) BEFORE emitting. Every generator MUST have a downstream source-fidelity validator (Stage 3 source-fidelity agent for BUILD_REQUESTs; Stage 1 Source Document Fidelity Gate + Coverage Detail Preservation for roadmap generators) that grep-verifies claims against source files with an adversarial stance (assume ≥3 fabrications exist, find them). Violations cause cascading fabrication downstream: roadmap → BUILD_REQUEST → task file → implementation code that does not match the spec. A skill that cannot enforce this rule is a skill that will ship wrong specifications to downstream executors.

---

## Dry-Run Mode

The skill supports a `--dry-run` flag (or user says "dry run" / "plan only"), detected at A.2.

**What dry-run does:**
1. Reads and analyzes the user's input (scope discovery still runs)
2. Produces a **phase plan summary** — estimated number of phases, phase names, approximate task counts, dependency chain, estimated complexity
3. Does NOT generate the roadmap document, BUILD_REQUESTs, or task files
4. Does NOT invoke `/task-builder` or `/task`
5. Presents the plan to the user for review before committing

**Output format:**
```
ROADMAP DRY RUN
================
Input: [type and summary]
Estimated phases: N
Estimated tasks: ~M

Phase Plan:
| Phase | Name | Est. Tasks | Dependencies | Complexity |
|-------|------|-----------|-------------|------------|
| 1 | [name] | ~N | None | S |
| 2 | [name] | ~N | Phase 1 | M |
| ... | | | | |

Estimated generation time: [rough estimate]
Proceed with full generation? (y/n)
```

**Branching behavior:** When DRY_RUN=true, the skill completes A.1 through A.4 (scope discovery and research notes), then presents the phase plan summary above instead of proceeding to A.5-A.7. If the user confirms ("y", "yes", "proceed"), the skill continues with A.5 (research sufficiency review) and the full pipeline. If the user declines, the skill ends — the research notes persist in the task folder for future use.

---

## Session Management

Session management is provided by the `/task` skill. At session start, check `.dev/tasks/to-do/` for `TASK-ROADMAP-*/` folders related to the current topic. If found, skip Stage A and invoke `/task` with the task file path — it reads the file, finds the first unchecked `- [ ]` item, and resumes from there.

---

## Research Quality Signals

### Strong Roadmap Signals
- Requirements enumerated with specific IDs, priorities, and source references
- Phase boundaries justified by dependency analysis, not arbitrary groupings
- Task tables contain specific file paths, component names, and testable acceptance criteria
- Integration Points tables show cross-phase artifact flow with specific creator/consumer task IDs
- Coverage matrix shows 100% forward and backward coverage
- Dependency graph is acyclic with parallelism annotations

### Weak Roadmap Signals (Redo)
- Vague phase descriptions without specific deliverables ("implement the backend")
- Requirements listed without IDs or traceability
- Missing coverage analysis (no Coverage Traceability Matrix or incomplete mapping)
- No dependency analysis (phases listed sequentially without justification)
- Task descriptions without acceptance criteria ("set up the database")
- No Integration Points tables (cross-phase dependencies not tracked)
- Doc-sourced architecture reported without code verification tags

### When to Spawn Additional Agents
- Input analysis identifies more requirements than initially estimated — need additional Phase Designers
- A phase's scope turns out larger than initially estimated — need to split into sub-phases
- Two agents' phase designs contradict each other — need a tie-breaker investigation
- Coverage validation reveals gaps — need additional phases or tasks to cover missed requirements
- Integration contract validation reveals orphan artifacts — need to trace missing creators/consumers
