---
name: readme
description: "Create or populate a README.md document for a project, module, or package. Use this skill when the user wants to create a README, document a project overview, populate an existing README stub, or write a comprehensive README following the project template. Trigger on phrases like 'create a README for...', 'write a README', 'populate this README', 'README for the wizard system', 'document this module', or when the user references a README.md file that needs content following the project template. Also trigger when the user says 'write a README' in the context of documenting a module, package, or project."
---

# README Creator

A skill for creating README.md documents distributed throughout the codebase at module roots (e.g., `frontend/README.md`, `frontend/app/wizard/README.md`, `backend/README.md`). READMEs are **navigational entry points** — NOT technical documentation. They orient the reader and link to deeper docs; technical references, operational guides, PRDs, and TDDs live in `/docs/`. This skill relies primarily on existing technical reference files plus codebase exploration as input sources, distilling verified content into concise, newcomer-friendly READMEs.

**How it works:** The skill performs initial scope discovery (identifying the module, its tech references, and its audience), then invokes the `/task-builder` skill to create an MDTM task file encoding all investigation and assembly phases. The skill then delegates execution to the `/task` skill, which processes the task file by marking items complete as it progresses. If context compresses or the session restarts, the skill re-reads the task file and resumes from the first unchecked item.

The skill follows a three-phase pipeline — Research → Synthesis → Assembly — to produce the final document. The output always follows the project template at `.claude/templates/documents/readme_template.md`. The template is the schema — every README must conform to it.

## Why This Process Works

READMEs go stale when written from memory or existing docs. This skill forces every claim through codebase verification — parallel agents read actual source files, trace actual entry points, and document actual behavior with file paths and line numbers.

The MDTM task file provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off.

The multi-phase structure (scope discovery → deep investigation → **analyst verification** → web research → synthesis → **synthesis QA** → assembly → **lens-based README validation** → **source-document fidelity gate**) prevents six common failure modes:
- **Context rot** — By isolating each investigation topic in its own subagent with its own output file, no single agent needs to hold the entire investigation in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning many parallel agents (each focused on one slice), the investigation goes deep on every aspect simultaneously rather than skimming across everything sequentially.
- **Hallucinated content** — By separating research (what exists) from synthesis (what it means) from assembly (the final README), each phase can be verified independently. This prevents hallucinated features, fabricated setup steps, or aspirational content presented as current. Synthesis agents only work from verified research files, not from memory or inference.
- **Uncaught quality drift** — Lens-based multi-agent QA replaces single-agent rubber-stamping. At the final document gate, minimum 11 agents (4 structural lenses + 4 content lenses + 3 readme-specific lenses) each focus on ONE quality dimension. Intermediate gates (research, synthesis) use 5+ agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative). A single agent reading 500 lines rubber-stamps; 11 focused agents find issues a generalist misses.
- **Source-document infidelity** — A dedicated source-document fidelity gate spawns minimum 2 agents that read BOTH the module's original source code AND the assembled README, verifying every feature claim, setup step, and dependency against actual code. This catches phantom features, fabricated setup procedures, and missing dependencies that internal-only QA misses.
- **Fix churn from parallel edits** — Serialized fix authorization ensures only ONE agent applies fixes per round. All lens agents report findings with `fix_authorization: false`, a single fix agent applies consolidated fixes, then a verification round confirms correctness. This eliminates contradictory edits from parallel fix agents.

### Variable Reference Block

Every skill invocation creates a self-contained folder. Define these variables early and reference them throughout:

```
TASK_ID:     TASK-README-<subject>-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/
SYNTHESIS:   ${TASK_DIR}synthesis/
QA:          ${TASK_DIR}qa/
REVIEWS:     ${TASK_DIR}reviews/
```

**Subject derivation:** `<subject>` is derived at task-folder-creation time from the module name and normalized to kebab-case (lowercase, hyphen-separated, 1-3 words, ~30 char soft cap). If no clean subject can be derived, fall back to the literal word `general`. Example TASK_ID: `TASK-README-wizard-20260408-140000`.

The research artifacts persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and feed directly into the assembled README.

---

## Input

The skill needs four pieces of information to produce a useful README. The first two are mandatory; the rest are optional but improve output quality.

1. **WHAT to document** (mandatory) — The project or module scope. Not just a name — what area of the codebase you want a README for. This can come from:
   - A directory path (e.g., `frontend/app/wizard/`, `backend/`, `ue_manager/`)
   - An existing README.md stub that needs populating
   - Both — the stub provides hints, the paths provide scope
   - Any existing technical reference files that should serve as primary input (e.g., `docs/frontend/WIZARD_TECHNICAL_REFERENCE.md`)

2. **WHERE to write it** (mandatory) — The README.md output location. READMEs live at module roots, not in `/docs/`. Examples: `frontend/app/wizard/README.md`, `backend/README.md`, `ue_manager/README.md`.

3. **WHY / what audience** (strongly recommended) — Who will read this README and what they need. This shapes tone, depth, and emphasis:
   - New users evaluating whether this module solves their problem
   - New contributors setting up and making their first change
   - Returning contributors navigating the codebase after time away

4. **WHAT tier** (optional, shapes depth) — Whether the README should be Lightweight (single-purpose utility), Standard (most applications), or Heavyweight (platforms/monorepos). Defaults to Standard if not specified. See [Tier Selection](#tier-selection) below.

### Effective Prompt Examples

**Strong — scope + output + tech reference:**
> Create a README for the wizard system at `frontend/app/wizard/`. It's a 10-stage game configuration interface used by game developers. There's a technical reference at `docs/frontend/WIZARD_TECHNICAL_REFERENCE.md` that should be the primary source. Output to `frontend/app/wizard/README.md`.

**Strong — consolidation with audience:**
> Write a README for the UE Manager service at `ue_manager/`. The audience is new backend developers who need to understand the service and get it running locally. There's an existing stub at `ue_manager/README.md` that needs populating. Use the tech reference at `docs/technical-reference/ue-manager-technical-reference.md` as input.

**Strong — update with specific scope:**
> Update the backend README at `backend/README.md`. We've added new agent services in `backend/app/agents/` and the current README doesn't cover them. Target audience is new contributors.

**Weak — topic only (will work but produces broader, less focused results):**
> Write a README.

**Weak — no scope (agents won't know what to investigate):**
> Document the project.

**Weak — ambiguous target (could be 5 different READMEs):**
> Create a README for the frontend.

### What to Do If the Prompt Is Incomplete

If the user provides only a vague request, **do NOT proceed immediately**. Ask the user to clarify using this template:

> I can create a README for you. To make it focused and accurate, can you help me with:
>
> 1. **What project or module should this README cover?** (e.g., "the wizard system", "the UE Manager service", "the backend API")
> 2. **Which directory is the primary scope?** (e.g., `frontend/app/wizard/`, `backend/`, `ue_manager/`)
> 3. **Who is the primary audience?** (e.g., "new contributors setting up locally", "developers evaluating the module", "returning team members")
> 4. **Where should the README.md be written?** (e.g., `frontend/app/wizard/README.md`)
> 5. **Are there existing technical references to use as input?** (e.g., `docs/frontend/WIZARD_TECHNICAL_REFERENCE.md`)

Proceed once you have at least #1 and #2 answered clearly. Items #3-5 improve quality but aren't blockers — use project conventions for output location if not specified.

---

## Tier Selection

Match the tier to module scope. **READMEs should almost always be 500 lines or under.** READMEs are navigational — they orient the reader and link to deeper docs. Exhaustive reference material (architecture diagrams, API inventories, config deep-dives) belongs in a companion Technical Reference or Operational Guide in `/docs/`, not in the README.

| Tier | When | Codebase Agents | Web Agents | Target Lines | Sections Required |
|------|------|-----------------|------------|--------------|-------------------|
| **Lightweight** | Small library or single-purpose utility, <5 source files, no complex setup | 1–2 | 0 | 50–150 | 1-6/13/16 |
| **Standard** | Most applications — multi-file modules with setup steps and configuration | 3–5 | 0–1 | 150–400 | All sections (skip N/A) |
| **Heavyweight** | Platform or monorepo — 3+ subsystems, complex setup, multiple audiences | 5–10+ | 1–2 | 200–500 | All sections fully completed |

**Hard ceiling: 500 lines.** READMEs that exceed 500 lines contain misplaced content. If the assembled README exceeds 500 lines, move content to a companion Technical Reference or Operational Guide in `/docs/` and link from the README instead. As a project grows, the README becomes more *navigational* and less *instructional* — orient the reader and link to deeper docs.

**Tier selection rules:**
- If unsure, default to Standard
- Heavyweight for monorepos with 3+ subsystems, complex integration boundaries, or multiple deployment targets
- Lightweight only for single-purpose libraries with <5 source files and no complex setup
- If the user says "thorough", "comprehensive", or "detailed" — always Heavyweight

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

All persistent artifacts go to the task folder at `${TASK_DIR}` (`.dev/tasks/to-do/TASK-README-<subject>-YYYYMMDD-HHMMSS/`).

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}TASK-README-<subject>-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research/research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Gap/question log | `${TASK_DIR}gaps-and-questions.md` |
| Analyst reports | `${TASK_DIR}qa/analyst-completeness-report-[N].md`, `${TASK_DIR}qa/analyst-synthesis-review-[N].md` |
| QA reports (intermediate gates) | `${TASK_DIR}qa/qa-research-gate-report-[N].md`, `${TASK_DIR}qa/qa-research-depth-report.md`, `${TASK_DIR}qa/qa-synthesis-gate-report-[N].md`, `${TASK_DIR}qa/qa-synthesis-coherence-report.md` |
| QA consolidated findings | `${TASK_DIR}qa/qa-consolidated-research-findings.md`, `${TASK_DIR}qa/qa-consolidated-synthesis-findings.md`, `${TASK_DIR}qa/qa-consolidated-final-findings.md` |
| QA lens reports (final gate) | `${TASK_DIR}qa/qa-lens-[lens-name].md` (11 reports: template-conformance, internal-consistency, evidence-quality, completeness, actionability, numbers-metrics, crossref-chain, domain-accuracy, feature-list-accuracy, usage-example-correctness, dependency-list-completeness) |
| QA fidelity reports | `${TASK_DIR}qa/qa-source-fidelity-coverage.md`, `${TASK_DIR}qa/qa-source-fidelity-phantom.md` |
| **Final README** | **`[module-dir]/README.md`** (e.g., `frontend/README.md`, `frontend/app/wizard/README.md`) |
| Template schema | `.claude/templates/documents/readme_template.md` |

> **Note:** See the [Artifact Locations](#artifact-locations) section at the end of this document for the complete artifact listing with instance counts.

**CRITICAL distinction:** The final README output is **distributed in the codebase** at each module's root directory, NOT centralized in `/docs/`. Research artifacts live in the task folder, but the assembled README is written directly to the module directory where developers will find it.

**File numbering convention:** All research, web, and synthesis files use zero-padded sequential numbers: `01-`, `02-`, `03-`, etc. This ensures correct ordering when listing files.

Check for existing task folders in `.dev/tasks/to-do/` before creating new ones — if prior research exists on the same module, read it first and build on it.

---

## Execution Overview

The skill operates in two stages:

**Stage A — Scope Discovery & Task File Creation (before the task file exists):**
1. Check for an existing task file or research directory (A.1)
2. Parse the user's request — identify module path, output location, audience, tier, tech references (A.2)
3. Perform scope discovery — map module structure, identify tech references, plan investigation assignments (A.3)
4. Write scope discovery results to a structured research notes file (A.4)
5. Review research sufficiency — mandatory gate (A.5)
6. Triage tier selection (A.6)
7. Write BUILD-REQUEST.md and invoke /task-builder skill to create the MDTM task file (A.7)

**Stage B — Task File Execution (after the task file exists):**
8. Invoke `/task` with the task file path — it provides the canonical F1 execution loop, parallel agent spawning, phase-gate QA, and session management
9. Resume: if returning to a session, invoke `/task` — it finds the `🟠 Doing` task file and resumes from the first unchecked item

Phase names within the task file:
- **Phase 1: Preparation** — Scope confirmation, template read, tier selection, tech reference identification
- **Phase 2: Deep Investigation** — Parallel subagent investigation (tech reference reading, project structure mapping, features inventory, setup/config tracing, existing doc review)
- **Phase 3: Completeness Verification** — rf-analyst completeness verification + rf-qa research gate + rf-qa-qualitative research depth (5 agents, parallel), then consolidate findings, apply fixes via serialized protocol (max 3 cycles), fill coverage gaps if needed (max 2 gap-fill rounds)
- **Phase 4: Web Research** — Optional external research (similar READMEs, framework docs, badge services)
- **Phase 5: Synthesis + QA Gate** — Template-aligned synthesis, then rf-analyst synthesis review + rf-qa synthesis gate + rf-qa-qualitative synthesis coherence (5 agents, parallel), then consolidate findings, apply fixes via serialized protocol (max 2 cycles)
- **Phase 6: Assembly & Lens-Based Validation** — rf-assembler produces final README, then 11 lens-based QA agents (4 structural + 4 content + 3 readme domain-specific, serialized fix protocol), then 2 source-document fidelity agents verify README against actual module source code; each gate uses consolidate-fix-verify serialized protocol (max 3 fix cycles per gate)
- **Phase 7: Present to User & Complete Task** — Deliver README, present artifacts, offer companion document creation

If a task file already exists for this module (from a previous session), skip Stage A and invoke `/task` with the existing task file path to resume from the first unchecked item.

---

## Stage A: Scope Discovery & Task File Creation

### A.1: Check for Existing Task File

Before creating a new task file, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `TASK-README-*/` folder related to this module
2. If found, read the task file inside it and check for unchecked `- [ ]` items
3. If unchecked items exist → skip to Stage B (resume execution via `/task`)
4. If all items are checked → inform user that the README is already complete, offer to create a new one or update the existing README
5. Check for existing task folder matching `TASK-README-*/` in `.dev/tasks/to-do/`:
   a. If `${TASK_DIR}research/research-notes.md` exists with `Status: Complete` → skip to A.5 (review sufficiency, then build task file)
   b. If `${TASK_DIR}research/research-notes.md` exists with `Status: In Progress` → read it, resume A.3 scope discovery from where it left off, then continue to A.4 to update the file
   c. If task folder exists but no `research-notes.md` → continue with A.3 but use the existing folder
6. If no task folder AND no research files exist → continue with A.2

### A.2: Parse & Triage the README Request

Break the user's request into structured components:

- **GOAL**: What project or module needs a README (e.g., "the wizard system", "the UE Manager service", "the backend API")
- **WHY**: Who the audience is and what they need (e.g., "new contributors setting up locally", "developers evaluating the module")
- **WHERE**: Module directory and key source files (e.g., `frontend/app/wizard/`, `backend/`)
- **OUTPUT_TYPE**: Classify as one of: Root README (top-level project overview), Subsystem README (module within a larger project), or Standalone Library README (independent utility/package)
- **MODULE_SLUG**: A kebab-case identifier for the task folder (e.g., `frontend-wizard` for `frontend/app/wizard/`, `ue-manager` for `ue_manager/`)
- **TECH_REF**: Path(s) to existing technical reference files covering this module (optional but strongly recommended — tech references are the PRIMARY research source when available, providing verified architecture, API surface, and implementation details that the README should distill and link to)

**Triage into Scenario A or B:**

**Scenario A — Explicit request:** User provided most of: module scope, source directories, output location, audience, tech reference path.
Example: "Create a README for the wizard system at `frontend/app/wizard/`. The tech reference is at `docs/frontend/WIZARD_TECHNICAL_REFERENCE.md`. Target audience is new contributors. Output to `frontend/app/wizard/README.md`."
→ Scope discovery confirms details and fills minor gaps. Lighter exploration.

**Scenario B — Vague request:** User provided a goal but few specifics.
Example: "Write a README for the backend"
→ Scope discovery does broad exploration to map what exists, identify features, locate tech references, and plan investigation assignments.

**Do NOT interrogate the user with a list of questions.** Proceed with what you have and let scope discovery figure out the rest from the codebase. Only ask the user if there's genuine ambiguity about intent that can't be inferred (e.g., "frontend" could mean the wizard, the roadmap canvas, or the entire frontend). Use the "What to Do If the Prompt Is Incomplete" template from the Input section only when the request truly cannot proceed.

### A.3: Perform Scope Discovery

Use Glob, Grep, and codebase-retrieval to map the module's structure and documentation landscape. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.

**Adjust depth by scenario:**
- **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, locate tech references, identify gaps in what the user specified.
- **Scenario B**: Broad discovery — scan the full codebase for anything touching the module, map all relevant subsystems, locate all documentation, count files.

**Discovery steps (all 6 are mandatory):**

1. **Check for an existing README stub** at the output location. If one exists, read it for context — note what sections are present, what's placeholder vs. real content, and what's missing. Treat it as a starting point, not as verified truth. An existing stub shapes the update scope but every claim still needs codebase verification.

2. **Locate existing technical reference files** — search `docs/` for technical references, architecture docs, TDDs, and operational guides covering this module. These are the PRIMARY research source — tech references contain verified architecture, API surface, implementation patterns, and configuration details that the README should distill into concise overviews and link to for depth. List all found with full paths. If a companion technical reference exists (e.g., `docs/frontend/WIZARD_TECHNICAL_REFERENCE.md` for `frontend/app/wizard/`), the README should reference it prominently rather than reproducing its content.

3. **Map the module's files and directories** — enumerate source files, config files, entry points, test directories, CI configs, and build system files. Identify:
   - Total file count and approximate complexity
   - Major features or subsystems (group files by function)
   - Build system and package manager (package.json, requirements.txt, Makefile, etc.)
   - Key dependencies (from lock files or import statements)
   - Architecture pattern (monolith, microservice, plugin-based, etc.)
   - Entry points (main files, CLI commands, API routers)

4. **Scan for existing documentation** — search for documentation that already covers aspects of this module:
   - READMEs in subdirectories (these may cover subsystems the parent README should link to)
   - Content in `docs/` referencing this module
   - CLAUDE.md sections describing this module
   - CONTRIBUTING.md, CHANGELOG.md, LICENSE files
   - Inline documentation patterns (JSDoc, docstrings, README sections in source)
   - Note what should be linked vs. what should be summarized in the README

5. **Plan research assignments** — divide the module into investigation topics, one per subagent. Each topic becomes a research file. Common assignment types for READMEs:

   **Research assignment types** (use as many as the topic requires):

   | Type | Purpose | What the Agent Does |
   |------|---------|-------------------|
   | **Tech Reference Reader** | Extract README-relevant content from existing tech references | Read tech ref files, extract overview, features list, architecture summary, key patterns, API surface — distill for README-level depth |
   | **Project Structure Analyst** | Map directory layout and build system | Enumerate directories, identify entry points, key files, build/package system, dependency tree |
   | **Feature Inventorist** | Identify user-facing features and capabilities | Read source code, configs, route definitions, UI components — build feature list with brief descriptions |
   | **Setup/Config Tracer** | Trace installation and configuration steps | Identify prerequisites, env variables, setup commands, config files, development server startup |
   | **Existing Doc Reviewer** | Read all existing documentation for this module | Extract README-relevant content from docs, READMEs, guides — identify what to link vs. reproduce |
   | **Testing/CI Analyst** | Identify test infrastructure and quality process | Find test commands, coverage targets, CI pipeline configs, testing frameworks, linting setup |

6. **Plan web research topics** and **determine synthesis file mapping** — based on gaps identified in steps 1-5, identify specific external research needs (framework documentation, badge services, similar project READMEs for structural inspiration). Decide which research files will feed which README template sections using the template as a mapping guide.

**Select depth tier** based on module scope:
- <5 source files, single-purpose utility, no complex setup → Lightweight
- Multi-file module with setup steps and configuration → Standard
- Platform or monorepo with 3+ subsystems, complex setup, multiple audiences → Heavyweight

Compute `<subject>` from the module name using the rules in the Subject Derivation section. If no clean subject is derivable, use `general`. Create the task folder: `.dev/tasks/to-do/TASK-README-<subject>-YYYYMMDD-HHMMSS/` with subfolders `research/`, `synthesis/`, `qa/`, `reviews/`

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

The file MUST be organized into these 8 categories (include all, mark as "N/A" if empty):

```markdown
# Research Notes: [MODULE] README

**Date:** [today]
**Scenario:** [A or B]
**Depth Tier:** [Lightweight / Standard / Heavyweight]

---

## EXISTING_FILES
[All files found during scope discovery: source directories, config files, entry points, test directories, CI configs, existing documentation. Per-file detail: path, purpose, key contents, approximate line count. Group by directory or subsystem.]

## PATTERNS_AND_CONVENTIONS
[Code organization patterns, naming conventions, testing patterns, build system details, framework patterns observed. Cite specific files as evidence.]

## TECH_REFERENCE_CONTEXT
[List all existing technical reference files found during A.3 step 2, their paths, what they cover, and which sections are README-relevant. Include coverage scope (e.g., "covers API endpoints and data models but not setup instructions"), last-updated indicators if available, and any sections that overlap with planned README content (for deduplication). If no tech reference exists, note: "No companion tech reference found — README research will rely entirely on codebase exploration."]

## PROJECT_ANALYSIS
[Key features of the module, architecture overview, dependencies (internal and external), setup requirements, target audience assessment. This is the content skeleton the README will flesh out.]

## RECOMMENDED_OUTPUTS
[Planned output files: research files, synthesis files, final README. Full paths and purposes. Include the expected sections of the final document and which research files feed each.]

## SUGGESTED_PHASES
[Planned investigation breakdown. For each planned research agent:
- Agent number, investigation type (Project Structure Analyst / Feature Inventorist / Setup/Config Tracer / Existing Doc Reviewer / Testing/CI Analyst), topic
- Files/directories to investigate
- Output file path
- Web research topics identified from gaps
- Synthesis file mapping]

## TEMPLATE_NOTES
[Notes about which README template sections apply for the selected tier, which are N/A. Notes on tier-specific section requirements from the template — e.g., Lightweight skips Architecture and Testing sections, Heavyweight requires subsystem breakdown. Include any section ordering adjustments needed for this module.]

## AMBIGUITIES_FOR_USER
[Genuine ambiguities about user intent that cannot be resolved from the codebase — e.g., unclear module scope, missing context about target audience, ambiguous boundaries between this README and companion documents. If none, write "None — intent is clear from the request and codebase context."]
```

This file is **MANDATORY** and must be written before any research agents are spawned. The builder and all downstream phases depend on it.

### A.5: Review Research Sufficiency (MANDATORY GATE)

**You MUST review the research notes before spawning the builder.** This is a quality gate — do NOT skip it.

Read `${TASK_DIR}research/research-notes.md` and evaluate:

1. Is the scope clearly bounded — is the module directory identified and a file inventory present?
2. Are tech reference files identified — or explicitly noted as absent? (README-specific: tech references are the primary source for deduplication decisions)
3. Is the project structure mapped — are directories, entry points, and key files counted?
4. Are key features identified — are at least the top 5 user-facing features noted?
5. Is existing documentation inventoried — is it clear what exists and what to link vs. reproduce?
6. Are research assignments concrete enough for the task builder — does each have an investigation type, target files, and output path?
7. Is the template section mapping reasonable — are the correct sections identified for the selected tier?
8. Is the tier selection appropriate — does it match the module's complexity (file count, subsystem count, setup complexity)?
9. Are companion documents identified — have tech references, ops guides, TDDs, and other docs in the same domain been found for content deduplication?

**If sufficient** → proceed to A.6 (template triage).

**If insufficient** → either:
- Do additional scope discovery yourself and update the research notes file, OR
- Spawn one or more rf-task-researcher subagents in parallel with specific feedback about what's missing. For multiple gaps, spawn one agent per gap slice, not a single agent for all gaps

**Maximum 2 gap-fill rounds.** After 2 rounds, proceed with what's available and note remaining gaps in the research notes AMBIGUITIES_FOR_USER section. If the user is available, ask them to clarify before continuing.

Do NOT proceed to the builder with incomplete research notes. The builder cannot explore the codebase effectively — it relies on what you provide.

### A.6: Template Triage

Determine which MDTM template the task builder should use:

**Use Template 02 (Complex Task) when the work involves:**
- Discovery before building (investigating module structure, features, setup procedures)
- Parallel subagent spawning
- Multiple phases with different activities (research, synthesis, assembly)
- Review/validation steps
- Conditional flows based on findings

**Use Template 01 (Generic Task) when the work involves:**
- Simple, sequential file creation
- Straightforward execution with no discovery
- Single-pass operations

**For READMEs, the answer is almost always Template 02** — the skill inherently involves discovery (Phase 2 deep investigation), parallel agents (Phases 2, 4, 5), synthesis (Phase 5), and validation (Phases 3, 5, 6). Even lightweight-tier READMEs benefit from the structured phase progression because codebase verification requires parallel exploration.

### A.7: Build the Task File

Write the BUILD_REQUEST to a file at `${TASK_DIR}BUILD-REQUEST.md`, then invoke the `/task-builder` skill. The task-builder reads the BUILD_REQUEST file, performs quality gates (rf-analyst + rf-qa), spawns the rf-task-builder agent to create the MDTM task file, and runs structural and qualitative validation internally. No manual verification step is needed — task-builder handles all validation and mediation.

**Step 1: Write `${TASK_DIR}BUILD-REQUEST.md`** using the Write tool with the following content:

```
# BUILD REQUEST

Source: skill-delegated
Calling Skill: readme
Task Directory: ${TASK_DIR}
Research Notes: ${TASK_DIR}research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Create a README at [MODULE_DIR]/README.md following the README template at `.claude/templates/documents/readme_template.md`. The README will serve as the navigational entry point for the [MODULE_NAME] module — orienting readers and linking to deeper documentation.

WHY: [WHY — from A.2: who the audience is, what they need, why this README is being created or updated]

TASK_ID_PREFIX: TASK-README

TECH_REF: [TECH_REF — from A.2: paths to existing technical reference files for this module, used as primary research source and deduplication target]

TEMPLATE: [01 or 02 — skill selects:
  01 = simple file creation, straightforward execution
  02 = needs discovery, testing, review, conditional flows, or aggregation]

DOCUMENTATION STALENESS WARNINGS:
[If scope discovery found any documentation that contradicts actual code/config, list the
specific claims and contradictions here. If none found during scope discovery, write:
"None found during scope discovery. Phase 2 agents will perform full documentation
cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags."]
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED]
or [UNVERIFIED]. Phase 2 agents will do full cross-validation, but avoid
building on obviously stale foundations.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL (if Template 02):
- Phase 1 (Preparation): L0 Setup — update task status to "🟠 Doing", confirm scope with user (module path, output path, tier, audience), read README template at `.claude/templates/documents/readme_template.md`, select tier (Lightweight/Standard/Heavyweight), identify companion tech reference files for deduplication, create the task folder at `.dev/tasks/to-do/TASK-README-<subject>-YYYYMMDD-HHMMSS/` with `research/`, `synthesis/`, `qa/`, `reviews/` subfolders
- Phase 2 (Deep Investigation): L1 Discovery — agents explore codebase + tech references and write findings files to `${TASK_DIR}research/`. Agent types: Tech Reference Reader (reads companion tech refs, extracts README-relevant content), Project Structure Analyst (maps directories, entry points, build system), Feature Inventorist (identifies user-facing capabilities from source), Setup/Config Tracer (traces installation, env vars, config files, dev server startup), Existing Doc Reviewer (scans all existing docs for link-vs-reproduce decisions), Testing/CI Analyst (checks test infrastructure, commands, coverage targets, CI pipeline)
- Phase 3 (Completeness Verification): L4 Review/QA — spawn rf-analyst (completeness-verification) AND rf-qa (research-gate) IN PARALLEL as quality gate. Both agents independently read research files and apply their checklists. Partitioning for >6 research files. QA verdict gates Phase 4.
- Phase 4 (Web Research): L1 Discovery — optional external research: similar README examples for structural inspiration, framework/tool documentation for accuracy, badge services (shields.io) for status badges. Skip when the module has no external dependencies or framework context.
- Phase 5 (Synthesis + QA Gate): L2 Build-from-Discovery — synthesis agents read research files and produce README sections aligned to the template. Then 5 synthesis gate agents ALL parallel with fix_authorization: false (SERIALIZED FIX PROTOCOL): 2 rf-analyst (synthesis-accuracy + source-tracing) + 2 rf-qa (structure + content-quality) + 1 rf-qa-qualitative (synthesis-coherence). Consolidate findings, 1 fix agent, 2 verification agents. Partitioning >4 synthesis files.
- Phase 6 (Assembly & Validation): L6 Aggregation — spawn rf-assembler to consolidate synthesis files into final README at [MODULE_DIR]/README.md following the template schema. Then lens-based QA: 11 agents (4 structural rf-qa + 4 content rf-qa-qualitative + 3 readme domain-specific), ALL fix_authorization: false (serialized fix protocol), consolidated findings, 1 fix agent, 2 verification agents. Then source-document fidelity gate: 2 rf-qa fidelity agents read module source code + assembled README, serialized fix protocol.
- Phase 7 (Present & Complete): L0 Closeout — present README to user (location, key sections, research file count, open questions), offer companion document creation ("Would you like a Technical Reference or Operational Guide for deeper coverage?"), update task file status to Done. **CRITICAL: Phase 7 task-completion items (update status, set completion_date) MUST be inside Phase 7, NOT in a separate Post-Completion section. The anti-orphaning rule requires all items be within numbered phases.**

QA_INTENSITY: [lite / standard / full]  (per I22 — determined by tier mapping in Tier Selection section or user override)
QA_GATE_REQUIREMENTS: PER_PHASE
  **NOTE: Gate descriptions below specify FULL intensity agent counts. When QA_INTENSITY is lite or standard, the rf-task-builder applies I22 reductions via the QA Intensity Adaptation table in the Agent Prompt Templates section.**
  Gate 1: Research Completeness (Phase 3)
    - lite: 1 rf-qa (evidence + gaps) + 1 rf-qa-qualitative (depth + completeness) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 3 fix cycles. Partitioning >6 files.
  **Note: All fix agents across all gates (research, synthesis, final, fidelity) use the Consolidated Fix Agent Prompt defined in the Agent Prompt Templates section unless a gate-specific override is defined.**
  Gate 2: Synthesis Quality (Phase 5)
    - lite: 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 2 agents. Max 1 fix cycle.
    - standard: 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
    - full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents. Max 2 fix cycles. Partitioning >4 files.
  Gate 3: Lens-Based Final Document QA (Phase 6)
    - lite: 1 rf-qa (combined structural) + 1 rf-qa-qualitative (combined content) + 1 domain lens (feature-list-accuracy) = 3 agents. Max 1 fix cycle.
    - standard: 3 rf-qa structural (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content (actionability, domain-accuracy, crossref-chain) + 1 domain lens (feature-list-accuracy) = 7 agents. Max 2 fix cycles.
    - full: 4 rf-qa + 4 rf-qa-qualitative + 3 domain (feature-list-accuracy, usage-example-correctness, dependency-list-completeness) = 11 agents. Max 3 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, after Gate 3)
    - lite: 1 rf-qa fidelity agent (combined semantic-coverage + phantom-detection lenses). Max 1 fix cycle.
    - standard: 2 rf-qa fidelity agents. Max 2 fix cycles.
    - full: 2 rf-qa fidelity agents. HALT if unresolved after 3 cycles.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + LINE_CEILING
  TEMPLATE_COMPLIANCE: All sections from README template must be present or marked N/A with rationale.
  EVIDENCE_TRAIL: Every claim must cite file paths, line numbers, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.
  LINE_CEILING: README must stay under 500 lines.

TESTING_REQUIREMENTS: N/A — documentation-only skill, no code produced, no tests applicable.

RESEARCH NOTES FILE:
${TASK_DIR}research/research-notes.md
Read this file FIRST for full detailed findings including: existing files, tech reference context, project structure mapping, feature inventory, planned investigation assignments, synthesis mapping, and output paths.

TEMPLATE_PATH: .claude/templates/documents/readme_template.md
OUTPUT_PATH: [MODULE_DIR]/README.md

SKILL CONTEXT FILE:
.claude/skills/readme/SKILL.md
  - Read "Agent Prompt Templates" for: all agent prompts (codebase research, web research, synthesis, analyst, QA, assembler)
  - Read "Content Rules" for: synthesis and assembly writing standards
  - Read "Critical Rules" for: non-negotiable constraints (500-line ceiling, no tech ref reproduction, navigational focus)
  - Read "Validation Checklist" for: final README validation criteria
  - Read "Output Structure" for: README section ordering per template
  - Read "Synthesis Mapping Table" for: synth file → README section mapping
  - Read "Tier Selection" for: agent count and depth guidance per tier

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process
Structure), you MUST create individual checklist items for EVERY research agent,
web research topic, synthesis file, and validation step. Do NOT create batch items
like "spawn all 5 research agents" or "run all web research" — each agent gets
its own checklist item. The research notes SUGGESTED_PHASES section contains
per-agent detail specifically to enable this granularity.

PROHIBITED_ACTIONS:
- Modifying source code (README creation is documentation-only)
- Deleting or moving existing files without user confirmation
- Creating files outside the task folder (`${TASK_DIR}`) and the final README at [MODULE_DIR]/README.md
- Reproducing tech reference content verbatim — the README distills and links, it does not duplicate

TO BUILD A GOOD TASK FILE, YOU NEED:
- Goal and outputs (what README to create, where, what tier, what audience)
- Source files and context (tech references, existing docs, module structure) — from the research notes
- Phases and steps (logical breakdown of the work) — from the research notes SUGGESTED_PHASES + SKILL.md phase definitions
- Verification criteria (how to know each step is done) — template compliance, 500-line ceiling, link validity
- Dependencies (what's needed before each step) — tech references before synthesis, research before QA gates
The research notes file should cover most of this.

SKILL PHASES TO ENCODE IN TASK FILE:
The task file MUST encode these phases as sequential checklist items. Each phase maps to a section of the skill's workflow. All items MUST follow the B2 self-contained pattern from the MDTM template.

Phase 1 — Preparation:
- Update task status to "🟠 Doing"
- Confirm scope with user (module path, output path, tier, audience, tech references)
- Read the README template at `.claude/templates/documents/readme_template.md`
- Select tier (Lightweight / Standard / Heavyweight) based on module complexity
- Identify companion tech reference files for content deduplication (list paths, note which sections overlap)
- Create the task folder at `.dev/tasks/to-do/TASK-README-<subject>-YYYYMMDD-HHMMSS/` with `research/`, `synthesis/`, `qa/`, `reviews/` subfolders

Phase 2 — Deep Investigation (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research agent (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the full codebase research agent prompt from SKILL.md
- Each item specifies: investigation topic, agent type, files/directories to investigate, output file path
- Builder MUST embed the complete agent prompt (including Incremental File Writing Protocol and Documentation Staleness Protocol from SKILL.md) in each checklist item per B2
- Agent count follows tier guidance: Lightweight 1-2, Standard 3-5, Heavyweight 5-10+
- Agent types for READMEs include: Tech Reference Reader (reads companion tech refs, extracts overview/features/architecture for README-level depth), Project Structure Analyst (enumerates directories, entry points, build system, dependency tree), Feature Inventorist (reads source code, configs, route definitions — builds feature list with brief descriptions), Setup/Config Tracer (traces prerequisites, env vars, setup commands, config files, dev server startup), Existing Doc Reviewer (reads all existing docs, identifies what to link vs. reproduce in README), Testing/CI Analyst (finds test commands, coverage targets, CI pipeline configs, linting setup)
- All research agents in the phase are spawned in parallel using multiple Agent tool calls in a single message. For example, with 5 research assignments: spawn all 5 agents in one message, mark each item complete as it returns. If context limits are reached before all return, remaining agents' output files persist on disk and the unchecked items are resumed on next session.

Phase 3 — Research Completeness Verification (LENS-BASED GATE, 5 AGENTS MINIMUM):
- Step 3.1: Spawn ALL 5 research gate agents IN PARALLEL, each with fix_authorization: false:
  - rf-analyst-1 (completeness lens): reads all research files, verifies every research assignment from SUGGESTED_PHASES produced a Complete output, checks project structure/features/setup/tech-ref coverage
  - rf-analyst-2 (cross-validation lens): cross-validates claims between research files, checks for contradictions, verifies [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags are applied consistently
  - rf-qa-1 (evidence-quality lens): verifies EVERY claim cites actual file paths/line numbers, spot-checks 5+ paths via Glob, flags any unverified assertions
  - rf-qa-2 (gap-detection lens): identifies coverage gaps against research-notes.md scope, severity-rates gaps (Critical/Important/Minor), verifies no silently dropped topics
  - rf-qa-qualitative-1 (research-depth lens): evaluates whether research findings are genuinely deep or surface-level; a research file that lists files without analyzing them is shallow and FAILS
  **ADVERSARIAL STANCE for ALL 5 agents:** "Assume the research contains at least 5 errors. Find them. A verdict of 0 issues requires evidence you thoroughly checked every file."
  Each agent writes to a separate report: `${TASK_DIR}qa/analyst-completeness-report-[N].md`, `${TASK_DIR}qa/qa-research-gate-report-[N].md`, `${TASK_DIR}qa/qa-research-depth-report.md`
- Step 3.2: Consolidate all 5 reports into `${TASK_DIR}qa/qa-consolidated-research-findings.md`. Union all findings, take more severe rating for duplicates.
- **Sub-flow A: Fix existing research content (Steps 3.3-3.4, serialized fix protocol):**
  - Step 3.3: If any findings exist in the consolidated report, spawn 1 rf-qa fix agent (fix_authorization: true, per the universal Consolidated Fix Agent Prompt) with consolidated findings to apply all fixes to existing research files.
  - Step 3.4: Spawn 2 verification agents (1 rf-qa + 1 rf-qa-qualitative, fix_authorization: false) to confirm fixes applied correctly.
  - If verification finds new issues, repeat Steps 3.3-3.4. Maximum 3 fix cycles for Sub-flow A.
- **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE instances of each of the 5 agent roles in parallel, each with an `assigned_files` subset. The threshold is >6 for research files because research files tend to be longer and more detailed than synthesis files. For example, with 10 research files: spawn 2 instances of each role (5 files each). Each partition instance writes to a numbered report (e.g., `${TASK_DIR}qa/analyst-completeness-report-1.md`, `${TASK_DIR}qa/analyst-completeness-report-2.md`). After all instances complete, merge their reports: union of all findings, take the more severe rating for any item flagged by multiple partitions, deduplicate gaps.
- Read ALL reports (or the merged report). Determine verdict from the QA report(s) (PASS / FAIL), cross-referenced with analyst findings.
- If PASS → proceed to Phase 4. If FAIL → fix ALL findings regardless of severity before proceeding. Reports list gaps with specific remediation actions.
- **Sub-flow B: Fill coverage gaps (runs only when gap-detection lens identifies missing topics):**
  - Spawn additional targeted research agents (one item per gap-filling agent, from merged gap list). Each gap-filling agent follows the same incremental writing protocol. Wait for gap-filling agents to complete before proceeding.
  - After gap-filling agents add NEW research files, spawn `rf-qa` with qa_phase: "fix-cycle" and the previous QA report path to re-verify only the previously-failed items against the new research files. **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked. Maximum 2 gap-fill rounds for Sub-flow B.
- **Total cycle budget:** Sub-flow A (max 3 fix cycles) and Sub-flow B (max 2 gap-fill rounds) are counted independently. After either sub-flow exhausts its budget, HALT execution: log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance on how to proceed. Do NOT continue to Phase 4 without user approval.
- Compile final gaps into `${TASK_DIR}gaps-and-questions.md` (merged from all reports)
- Do NOT proceed to Phase 4 until verdict is PASS

Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY, optional):
- One checklist item PER web research topic (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
- Each item specifies: topic, context from codebase findings, output file path
- **Optional for READMEs** — skip when the module is entirely internal with no external dependencies or framework context. Include when the README covers: external framework integrations (Next.js, FastAPI, Unreal Engine), third-party service configurations, badge/shield services, or when similar project READMEs would provide structural inspiration
- Web research targets should include (as applicable): similar project READMEs for structural best practices, official framework/tool documentation for accuracy, badge services (shields.io patterns), community conventions for the module's technology stack

Phase 5 — Synthesis (PARALLEL SPAWNING MANDATORY) + Synthesis QA Gate:
- One checklist item PER synthesis file (from research notes RECOMMENDED_OUTPUTS)
- Each item spawns an Agent subagent with the synthesis agent prompt from SKILL.md
- Each item specifies: research files to read, README template sections to produce, output path
- Synthesis agents map research findings to README template sections using the Synthesis Mapping Table from SKILL.md. Each synthesis file covers a cluster of related template sections (e.g., overview + features, setup + configuration, architecture + structure, testing + contributing).
- **CONDITIONAL SYNTHESIS THRESHOLD:** When >15 source files are inventoried in the research, synthesis agents MUST use concise summary format for file listings rather than enumerating each file individually. READMEs are navigational — link to deeper docs for exhaustive inventories.
- After ALL synthesis agents complete, spawn ALL 5 synthesis gate agents IN PARALLEL, each with fix_authorization: false (SERIALIZED FIX PROTOCOL):
  - rf-analyst-1 (synthesis-accuracy lens): verifies every synthesized claim traces to a specific research file finding with file path evidence
  - rf-analyst-2 (source-tracing lens): for each synthesis file, reads the source research files it references and confirms content was faithfully distilled, not fabricated or over-summarized
  - rf-qa-1 (structure lens): verifies section headers match README template, tables use correct columns, depth budgets respected, no placeholder text
  - rf-qa-2 (content-quality lens): verifies no fabrication, runnable examples reference real commands/packages, no aspirational features as current, audience-appropriate language
  - rf-qa-qualitative-1 (synthesis-coherence lens): evaluates whether synthesis files tell a coherent story from the research -- does the README flow logically? Are cross-section references consistent? Would a newcomer understand the module from these sections?
  **ADVERSARIAL STANCE for ALL 5 agents:** "Assume the synthesis contains at least 5 errors. Find them."
  Each agent writes to a separate report. After all complete, consolidate findings into `${TASK_DIR}qa/qa-consolidated-synthesis-findings.md`, then 1 rf-qa fix agent applies all fixes, then 2 verification agents confirm. **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked. The analyst applies the Synthesis Quality Review Checklist. The QA agent applies its synthesis-gate checklist. The analyst writes to `${TASK_DIR}qa/analyst-synthesis-review-[N].md`. The QA agent writes to `${TASK_DIR}qa/qa-synthesis-gate-report-[N].md`. Embed full prompts from respective agent definitions in each checklist item per B2.
- **Parallel partitioning for large workloads:** When >4 synthesis files exist, spawn multiple analyst instances and multiple QA instances in parallel, each with an `assigned_files` subset of synthesis files. The threshold is lower than Phase 3 (>4 vs >6) because synthesis QA requires deeper per-file analysis (tracing claims back to research files, verifying template alignment, checking cross-section consistency). Same partitioning pattern as Phase 3. Each partition instance writes to a numbered report. Orchestrator merges all partition reports after completion.
- Read ALL reports (or the merged report). Merge findings from all reports. The fix agent applies all consolidated fixes. Determine verdict from QA report(s), cross-referenced with analyst findings. If PASS → proceed to Phase 6. If FAIL → check which issues QA already fixed vs which remain. For remaining issues, re-run affected synthesis agents, then re-spawn `rf-qa` (fix-cycle). Maximum 2 fix cycles for synthesis — after 2 failed cycles, HALT execution: log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance on how to proceed. Do NOT continue to Phase 6 without user approval.

Phase 6 — Assembly & Lens-Based Validation (RF-ASSEMBLER + 11 LENS AGENTS + SOURCE FIDELITY):
- Step 6.1: Spawn rf-assembler (same as current — single agent, assembles README from synth files, enforces 500-line ceiling). Writes to [MODULE_DIR]/README.md.
- Step 6.2: LENS-BASED FINAL DOCUMENT QA (11 agents, SERIALIZED FIX PROTOCOL).
  Step 6.2a: Spawn ALL 11 lens agents IN PARALLEL, each with fix_authorization: false:
    Structural lenses (rf-qa):
    - rf-qa (template-conformance lens): all sections present per tier, correct ordering, no remaining placeholders/sentinels. Report: `${TASK_DIR}qa/qa-lens-template-conformance.md`
    - rf-qa (internal-consistency lens): cross-section consistency (deps in Quick Start match Config, paths in Structure match Usage), TOC accuracy, no contradictions. Report: `${TASK_DIR}qa/qa-lens-internal-consistency.md`
    - rf-qa (evidence-quality lens): every claim cites file paths/line numbers, spot-check 5+ paths via Glob, no unverified assertions presented as fact. Report: `${TASK_DIR}qa/qa-lens-evidence-quality.md`
    - rf-qa (completeness lens): every topic from scope discovery appears in output, no gaps, no silently dropped items from research. Report: `${TASK_DIR}qa/qa-lens-completeness.md`
    Content lenses (rf-qa-qualitative):
    - rf-qa-qualitative (actionability lens): Quick Start steps are copy-pasteable, config instructions are specific, no "configure as needed" hand-waving. Report: `${TASK_DIR}qa/qa-lens-actionability.md`
    - rf-qa-qualitative (numbers-metrics lens): version numbers match package.json, line counts within tier budget, prerequisite versions are current, badge URLs are valid. Report: `${TASK_DIR}qa/qa-lens-numbers-metrics.md`
    - rf-qa-qualitative (crossref-chain lens): trace prerequisite -> install -> config -> usage chains end-to-end, verify every link in the chain exists. Report: `${TASK_DIR}qa/qa-lens-crossref-chain.md`
    - rf-qa-qualitative (domain-accuracy lens): claims about the codebase match actual code, features listed are actually implemented, architecture description matches actual structure. Report: `${TASK_DIR}qa/qa-lens-domain-accuracy.md`
    README domain-specific lenses:
    - rf-qa-qualitative (feature-list-accuracy lens): every feature in Section 2 is verified to exist in actual source code, no aspirational features, features described from user perspective. Report: `${TASK_DIR}qa/qa-lens-feature-accuracy.md`
    - rf-qa (usage-example-correctness lens): every install command, config snippet, CLI example actually runs against current codebase (commands exist, flags exist, file paths exist, env vars are real). Report: `${TASK_DIR}qa/qa-lens-usage-correctness.md`
    - rf-qa (dependency-list-completeness lens): prerequisites/dependencies match package.json/requirements.txt/pyproject.toml/Dockerfile, no missing deps, no fabricated deps, versions match lock files. Report: `${TASK_DIR}qa/qa-lens-dependency-completeness.md`
  Step 6.2b: Read all 11 QA reports, consolidate into `${TASK_DIR}qa/qa-consolidated-final-findings.md`.
  Step 6.2c: Spawn 1 rf-qa fix agent (fix_authorization: true, per the universal Consolidated Fix Agent Prompt) with consolidated findings — apply ALL fixes to the README.
  Step 6.2d: Spawn 2 verification agents (1 rf-qa + 1 rf-qa-qualitative, fix_authorization: false) to confirm fixes applied correctly and no new issues introduced.
  If verification finds issues, repeat Steps 6.2c-6.2d (max 3 cycles). If unresolved after 3 cycles, HALT and present findings to user.
- Step 6.3: SOURCE-DOCUMENT FIDELITY GATE (2 agents minimum, SERIALIZED FIX PROTOCOL).
  Step 6.3a: Spawn 2 rf-qa fidelity agents IN PARALLEL, fix_authorization: false:
    - rf-qa (fidelity-coverage agent): reads module source code (entry points, package manifests, key source files) + full assembled README. Checks: every feature in source code has a corresponding README entry, every dependency in package manifest appears in Prerequisites, every setup step traces to an actual config/script file. Report: `${TASK_DIR}qa/qa-source-fidelity-coverage.md`
    - rf-qa (fidelity-phantom agent): reads module source code + full assembled README. Checks: every README claim traces to real code (no phantom features, no fabricated commands, no invented file paths), detail preservation (specific names, counts, config keys survive from code into README). Report: `${TASK_DIR}qa/qa-source-fidelity-phantom.md`
  Step 6.3b: Consolidate fidelity findings, apply fixes (same serialized protocol: 1 fix agent, 2 verification agents, max 3 cycles).
  If unresolved after 3 cycles, HALT and present findings to user.
- Step 6.4: Read all QA reports (lens + fidelity). If any issues remain unresolved, address ALL before proceeding to Phase 7. Zero leniency.

Phase 7 — Present to User & Complete Task:
- Present summary to user (README location, key sections, tier used, research file count, open questions from gaps-and-questions.md)
- Write task summary to Task Log / Notes section of the task file (completion date, total phases, key outputs, duration)
- Update task file frontmatter: status to "🟢 Done", set completion_date to today's date
- `NON-BLOCKING` Suggest downstream skills: "This README can be complemented by a Technical Reference (`/tech-reference`) for deeper architecture and API details, or an Operational Guide (`/operational-guide`) for setup and operational procedures. The research files are already in place." Present the suggestion, mark this item complete immediately, and do NOT wait for a user response. This item does not gate task completion.
- CRITICAL ANTI-ORPHANING RULE: Task-completion items (write task summary, update frontmatter to "🟢 Done") MUST be inside this phase, NEVER a separate Post-Completion section. Downstream offers are `NON-BLOCKING` — present them, mark complete, do not wait for user response.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-README-<subject>-[YYYYMMDD]-[HHMMSS]/TASK-README-<subject>-[YYYYMMDD]-[HHMMSS].md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, README template, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
   - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. If anything is missing, note it in the Task Log section — the skill will review
6. Create the task file at .dev/tasks/to-do/TASK-README-<subject>-YYYYMMDD-HHMMSS/TASK-README-<subject>-YYYYMMDD-HHMMSS.md using PART 2 structure
7. Return the task file path

ESCALATION:
Since you are running as a subagent (not a teammate), you have NO team context.
Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage — these tools
will fail because there is no team. This overrides your agent definition's
Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
Instead, return the task file path as your final output.
- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
- **External docs/syntax** → use WebSearch
- **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.
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

1. **Invoke /task:** Use the Skill tool with `skill: "task"` and `args` set to the task file path produced by Stage A (e.g., `.dev/tasks/to-do/TASK-README-wizard-20260310-120000/TASK-README-wizard-20260310-120000.md`).
2. **Execution transfers to /task:** The /task skill reads the task file and processes each checklist item via the F1 loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT), spawning subagents as specified in B2 items and running phase-gate QA after each Phase 2+ completion.
3. **No additional execution logic needed:** All execution rules — F1 sequential processing, F2 prohibited actions, F4 modification restrictions, F5 frontmatter protocol, error handling, session resumption — are provided by /task. This skill does not redefine them.
4. **Double QA is intentional:** The task file already contains skill-specific QA items (rf-analyst + rf-qa + rf-qa-qualitative at gates) and /task adds phase-gate QA on top. This results in intentional, acceptable double QA coverage at gate phases — skill-specific QA validates domain content while phase-gate QA validates structural completeness.

### What the Task File Must Contain

The task file from Stage A must embed all skill-specific context so that /task can execute it without reading this SKILL.md. Specifically:

- **Agent prompt templates** customized with the specific README module topics, source file paths (tech references, existing docs, module structure), and output paths
- **Validation checklists and content rules** in ensuring clauses (e.g., "ensuring the README stays under 500 lines", "ensuring all links resolve to real paths", "ensuring no technical deep-dives that belong in tech-ref docs")
- **Output paths and file naming conventions** for research files, synthesis files, and the final assembled README document
- **Prohibited actions for this skill:** research agents READ code, configs, docs, and directory structure — they do not modify source code; do not invent file paths; do not fabricate content; do not delete research artifacts after assembly
- **All phase-specific context** so each B2 item is self-contained and independently executable

**CRITICAL:** /task does NOT read this SKILL.md during execution. ALL skill-specific instructions, domain rules, quality criteria, and prohibited actions must be baked into the task file during Stage A.

---

## Agent Prompt Templates

These prompt templates are embedded into the MDTM task file during Stage A (scope discovery + task building). The task builder customizes each template with specific module paths, tech reference files, output paths, and topic assignments. During execution, /task spawns subagents using these prompts verbatim (with placeholders filled).

**QA Intensity Adaptation (per Template 02 I22):**
- lite: Gate 3 combines to 3 agents:
  (1) rf-qa combined-structural: use template-conformance + internal-consistency + evidence-quality + completeness lenses
  (2) rf-qa-qualitative combined-content: use actionability + domain-accuracy + crossref-chain + numbers-metrics lenses
  (3) highest-value domain lens: feature-list-accuracy
  Intermediate gates: 2 agents (1 rf-qa combined + 1 rf-qa-qualitative combined)
  Fidelity: 1 agent (combined coverage + phantom lenses). Max 1 fix cycle. 1 verification agent.
- standard: Gate 3 uses 7 agents:
  3 rf-qa structural: template-conformance, internal-consistency, evidence-quality
  3 rf-qa-qualitative content: actionability, domain-accuracy, crossref-chain
  1 domain lens: feature-list-accuracy
  Intermediate gates: 3 agents (1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative)
  Fidelity: 2 agents. Max 2 fix cycles. 2 verification agents.
- full: Use all prompts below as-is (current behavior, no changes).

### Codebase Research Agent Prompt

```
Research this aspect of [module/project name] and write findings to [output-path]:

Topic: [topic description]
Investigation type: [Tech Reference Reader / Project Structure Analyst / Feature Inventorist / Setup/Config Tracer / Existing Doc Reviewer / Architecture Analyst / Testing/CI Analyst]
Files to investigate: [list of files/directories]
Module root: [primary directory]
Tech reference files: [list of companion tech reference files, if any]
Research question context: [the overall module being documented for README, for context]

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
1. If Tech Reference Reader — read tech reference files FIRST. Extract overview/purpose, key features, architecture summary, setup requirements, dependencies, and configuration options. These are the PRIMARY input for the README and should be distilled, not duplicated.
2. Read actual source files — understand what each directory/module does, what it exports, what it depends on. Verify tech reference claims against actual code.
3. Trace dependencies — package.json, requirements.txt, pyproject.toml, import statements. Document what must be installed and in what order.
4. Document public interfaces — APIs, CLI commands, configuration options, exported functions/classes. Focus on what users and contributors INTERACT with.
5. Identify user-facing features — what can someone DO with this module? Write from the user's perspective, not the implementer's. Think "what problem does this solve?" not "what classes exist?"
6. Check setup requirements — prerequisites, install steps, environment variables, build commands, required services. Trace the actual setup flow a newcomer would follow.
7. Note integration points — external services, databases, other modules, shared state. Document boundaries.
8. Flag README-specific opportunities — features worth highlighting for newcomers, examples that would help onboarding, common gotchas, FAQ-worthy topics, badges that could be added.

CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Code describes CURRENT state. These frequently diverge.
When you encounter documentation that describes architecture, components, endpoints, or workflows,
you MUST cross-validate structural claims against actual code before reporting them as current:

1. **Services/components described in docs:** Verify the directory, entry point, and key files actually exist. Use Glob to check. If missing, the doc is STALE.

2. **File paths mentioned in docs:** Spot-check that referenced files exist.

3. **Commands/scripts described in docs:** Verify the referenced scripts exist and their actual behavior matches the documentation.

4. **Dependencies described in docs:** Cross-check against actual package.json/requirements.txt.

For EVERY doc-sourced claim, mark it with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** — code shows different implementation (describe what code actually shows)
- **[UNVERIFIED]** — could not find corresponding code; may be stale, planned, or in a different repo

Claims marked [UNVERIFIED] or [CODE-CONTRADICTED] MUST appear in the Gaps and Questions section.

Output Format:
- Use descriptive headers for each file or logical group investigated
- Include actual file paths, function names, export lists
- Focus on what matters for README: features, setup, usage, structure
- Note any anomalies, tech debt, or surprising behavior
- End each section with a "Key Takeaways" bullet list
- End the file with:
  ## Gaps and Questions
  - [things that need further investigation or are unclear]
  - [all UNVERIFIED and CODE-CONTRADICTED claims from docs]

  ## Stale Documentation Found
  - [list any docs that describe architecture/components that no longer exist]

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
Module context: [the overall module being documented for README]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for similar project READMEs in the same framework/ecosystem — identify structural patterns that work well
2. Search for official framework documentation on prerequisites, setup, and configuration (e.g., Next.js, FastAPI, Unreal Engine)
3. Search for badge services (shields.io) — identify dynamic badges relevant to the module (build status, coverage, version, license)
4. Search for README quality tools and community standards (e.g., standard-readme, readme-md-generator)
5. Search for best practices on README structure, length, and newcomer-friendliness
6. For each finding, document:
   - Source URL
   - Key information extracted
   - How it relates to our module's README needs
   - Whether it supports, extends, or contradicts what we found in the codebase
7. Rate source reliability (official docs > well-maintained repos > blog posts > forum answers)

Output Format:
- Use descriptive headers for each research area
- Always include source URLs
- Mark relevance: HIGH / MEDIUM / LOW for each finding
- End with:
  ## Key External Findings
  [Bullet list of the most important discoveries]

  ## Recommendations from External Research
  [How external findings relate to the README being created]

IMPORTANT: Our codebase is the source of truth. External research adds context and best practices but does not override verified codebase findings.
```

**Common web research topics for READMEs:**
- Similar project READMEs in the same framework/ecosystem (structural patterns, tone, depth)
- Official framework documentation for prerequisites and setup (Node.js, Python, Docker, UE5)
- Badge services (shields.io dynamic badges for build, coverage, version, license, dependencies)
- README quality tools and linters (standard-readme spec, readme-md-generator)
- Community standards for open-source READMEs (contributing guidelines, code of conduct, issue templates)

### Synthesis Agent Prompt

```
Read the research files listed below and synthesize them into template-aligned sections for a README document.

Research files to read: [list of paths]
Template sections to produce: [section numbers and names]
Output path: [synth file path]
Companion documents: [list of companion doc paths — tech references, operational guides, etc.]
Module context: [brief description of the module being documented]
Audience: [newcomer evaluator / new contributor / returning contributor]

RULE 0 — READ THE TEMPLATE FIRST:
Before synthesizing anything, read `.claude/templates/documents/readme_template.md` in full. The template is the schema — every header, section ordering, and guideline is mandatory. Do not deviate from it.

Rules:
1. Follow the template structure exactly — use the same headers, tables, and section format
2. Every fact must come from the research files — do not invent, assume, or infer
3. **Front-load value** — the first ~30 lines must answer: what is this? how do I run it? where is everything? A reader who stops at line 30 should have enough to get started.
4. **Write for the newcomer** — assume the reader has never seen this codebase. Avoid jargon without explanation. Link to deeper docs instead of explaining inline.
5. **Show, don't tell** — prefer runnable examples (install commands, usage snippets, curl examples) over descriptions of what things do. Every Quick Start step must be copy-pasteable.
6. **No aspirational content as current** — do not describe planned, future, or partially implemented features as if they exist today. If a feature is in progress, say so explicitly or omit it.
7. **Tables over prose** — use tables for multi-item data (dependencies, environment variables, directory structure, available scripts, API endpoints). Tables are scannable; paragraphs are not.
8. **No architecture deep dives** — the README is a navigational entry point, not a technical reference. For architecture, internals, and exhaustive API docs, write a 1-2 sentence summary and link to the companion Technical Reference.
9. **Content deduplication with companion docs** — do NOT reproduce content that exists in companion Technical References, Operational Guides, PRDs, or TDDs. Summarize in 1-3 sentences and link. The README is the signpost; companion docs are the destination.
10. **README vs Other Documents boundary** (per template Guideline C): READMEs cover WHAT, WHY, and HOW TO GET STARTED. Technical References cover HOW IT WORKS IN DETAIL. Operational Guides cover HOW TO DEPLOY AND OPERATE. PRDs cover WHAT TO BUILD AND WHY (product perspective). TDDs cover HOW TO BUILD IT (engineering perspective). Never cross these boundaries.
11. **Documentation-sourced claims require verification status.** If a research file reports a finding from documentation, check for [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED] tags. Only [CODE-VERIFIED] claims may be presented as current. [CODE-CONTRADICTED] must be corrected. [UNVERIFIED] must be excluded or flagged.
12. **When research files contradict each other**, note the contradiction and present the finding with stronger evidence (code reads > config reads > documentation > web research).
13. **Web research findings must be explicitly marked as external context** with source URLs. Never present web-sourced information as if it came from the codebase.
14. Use callout conventions where appropriate: > **Note:**, > **Important:**, > **Tip:**

SELF-CONTAINED DEPTH BUDGETS — Target sizes per section to keep the README concise and navigational:
- About: ≤4 sentences (what it is, what problem it solves, who it's for)
- Features: 5-10 bullet items (user-facing capabilities, not implementation details)
- Quick Start: ≤5 steps (from zero to running — prerequisites, install, configure, run, verify)
- Project Structure: Top 2-3 directory levels in a tree or table (not exhaustive file listing)
- Architecture Overview: ≤1 diagram + 2 short paragraphs (then link to tech ref)
- Configuration: Table of key environment variables and config files (not full reproduction)
- Usage/Examples: 2-4 runnable examples covering the most common use cases
- Testing: How to run tests (1-3 commands), link to test docs for details
- Contributing: ≤5 bullet steps or link to CONTRIBUTING.md
- Related Documentation: Link table to companion docs
If a section is growing beyond its budget, that material belongs in a companion doc — summarize and link.

CRITICAL — Incremental File Writing:
You MUST write to your output file incrementally as you synthesize each section. Do NOT read all research files into context and attempt a single large write at the end. The process is:
1. Create the output file with a header and your first synthesized section
2. After completing each subsequent section, append it to the output file immediately using Edit
3. Never rewrite the entire file from memory — always append or do targeted edits

This prevents data loss from context limits and ensures partial results survive if the agent is interrupted.

Write the sections in the exact format they should appear in the final README, including all table structures and headers from the template.

CRITICAL — TASK FILE EMBEDDING REQUIREMENT:
The task builder MUST embed the Content Rules (Rules 1-14 above) and the Self-Contained Depth Budgets directly into each synthesis checklist item in the generated task file. Synthesis agents spawned by /task do not have access to SKILL.md — all skill-specific instructions must be baked into the task file items. Embed the rules from the "Content Rules (From Template — Non-Negotiable)" section of this skill file into each synthesis item.
```

### Research Analyst Agent Prompts (rf-analyst — 2 Lens Instances)

At the research completeness gate (Phase 3), spawn 2 rf-analyst instances in parallel, each with a different lens focus. Together they cover the original 8-item checklist plus new cross-validation checks.

#### Analyst-1: Completeness Lens

```
Perform completeness verification of all research files for [module/project name] README.

Analysis type: completeness-verification
Lens: completeness
Research directory: [research-dir-path]
Research notes file: [research-notes-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: ${TASK_DIR}qa/analyst-completeness-report-1.md
Fix authorization: false

Your job is to verify research coverage and completeness. You focus on WHETHER everything was investigated.

PROCESS:
1. Read the research-notes.md file to understand the planned scope (EXISTING_FILES, SUGGESTED_PHASES, module structure)
2. Use Glob to find ALL research files in the research directory (files matching [NN]-*.md)
3. Read EVERY research file — do not skip any
4. Apply the checklist below
5. Write your report to the output path

CHECKLIST:
1. Project structure coverage — directory structure, key files, module boundaries, and entry points are documented with actual paths verified via Glob/Read
2. Tech reference integration — if companion tech reference files exist, research agents read them FIRST and extracted overview, features, architecture, setup, and dependencies (not duplicated, but distilled)
3. Feature inventory — user-facing features are identified from actual code, not docs alone. Each feature is described from the user perspective ("what can someone DO?") not the implementer perspective
4. Research assignment completion — every research assignment from SUGGESTED_PHASES produced an output file with Status: Complete
5. Depth-tier alignment — investigation depth matches the stated tier (Lightweight = key features and quick start; Standard = full coverage with examples; Heavyweight = exhaustive with architecture and advanced usage)
6. Gap identification — all gaps unified, deduplicated, and severity-rated (Critical/Important/Minor)

Adversarial framing: "Assume the research contains at least 3 coverage gaps. Find them."

VERDICTS:
- PASS: All checks pass, no critical gaps
- FAIL: Critical gaps exist (list each with specific remediation action)

Use the full output format from your agent definition (tables for coverage, evidence quality, completeness).
```

#### Analyst-2: Cross-Validation Lens

```
Perform cross-validation of all research files for [module/project name] README.

Analysis type: completeness-verification
Lens: cross-validation
Research directory: [research-dir-path]
Research notes file: [research-notes-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: ${TASK_DIR}qa/analyst-completeness-report-2.md
Fix authorization: false

Your job is to cross-validate findings BETWEEN research files. You focus on whether findings are CONSISTENT and VERIFIED.

PROCESS:
1. Read ALL research files in the research directory
2. For each file, note its claims about features, dependencies, setup steps, and configuration
3. Cross-validate claims between files — do different agents agree?
4. Apply the checklist below
5. Write your report to the output path

CHECKLIST:
1. Setup/config tracing — prerequisites, install steps, environment variables, build commands, and required services are traced from actual package.json, requirements.txt, Dockerfiles, and config files — not from documentation alone
2. File integrity — no empty or truncated research files; each file has Summary, Key Takeaways, and Gaps and Questions sections
3. Cross-file contradiction detection — do research files agree on features, dependencies, and setup steps? Flag any contradictions between files with specific references.
4. [CODE-VERIFIED] tag consistency — are verification tags ([CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED]) applied uniformly across all research files? Flag files missing tags.

Adversarial framing: "Assume the research files contain at least 3 contradictions or inconsistencies. Find them."

VERDICTS:
- PASS: No cross-validation issues found
- FAIL: Contradictions or inconsistencies found (list each with specific file references)

Use the full output format from your agent definition.
```

### Research QA Agent Prompts (rf-qa — 2 Lens Instances)

At the research completeness gate (Phase 3), spawn 2 rf-qa instances in parallel, each with a different lens focus. Together they cover the original 10-item checklist.

#### QA-1: Evidence-Quality Lens

```
Perform evidence-quality QA verification of research files for [module/project name] README.

QA phase: research-gate
Lens: evidence-quality
Research directory: [research-dir-path]
Analyst reports: [analyst-report-paths] (if exist, verify their claims)
Research notes file: [research-notes-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: ${TASK_DIR}qa/qa-research-gate-report-1.md
Fix authorization: false

You focus on EVIDENCE QUALITY — whether claims are backed by verifiable references.

IF ANALYST REPORTS EXIST:
1. Read the analyst reports
2. Verify their coverage audit claims independently
3. Apply your checklist below

CHECKLIST:
1. File inventory — all research files exist with Status: Complete and Summary
2. Evidence density — Verify EVERY claim in each file — verify file paths and code references exist
3. Documentation cross-validation — all doc-sourced claims tagged [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED], Verify EVERY CODE-VERIFIED claim
4. Contradiction resolution — no unresolved conflicting findings about the same feature, dependency, or setup step
5. Incremental writing compliance — files show iterative structure, not one-shot

Adversarial framing: "Assume at least 3 claims in the research files are unverified or fabricated. Find them."

VERDICTS:
- PASS: Evidence quality meets standards
- FAIL: ALL findings must be resolved. List each with specific remediation.

Zero tolerance — if you can’t verify it, it fails.
```

#### QA-2: Gap-Detection Lens

```
Perform gap-detection QA verification of research files for [module/project name] README.

QA phase: research-gate
Lens: gap-detection
Research directory: [research-dir-path]
Research notes file: [research-notes-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: ${TASK_DIR}qa/qa-research-gate-report-2.md
Fix authorization: false

You focus on COVERAGE GAPS — whether all required topics were investigated thoroughly.

CHECKLIST:
1. Scope coverage — every key file/directory from research-notes EXISTING_FILES examined
2. Gap severity — Critical gaps block synthesis, Important reduce quality, Minor are lower priority but must still be fixed
3. Depth appropriateness — matches the tier expectation (Lightweight/Standard/Heavyweight)
4. Tech reference utilization (README-specific) — if companion tech reference files exist, verify research agents actually read them and extracted relevant content rather than re-investigating from scratch
5. Feature completeness — user-facing features identified from code, not just from documentation. Features described from user perspective, not implementer perspective

Adversarial framing: "Assume the research has at least 3 coverage gaps that will cause problems during synthesis. Find them."

VERDICTS:
- PASS: No significant gaps found
- FAIL: ALL findings must be resolved. List each with specific remediation.

Zero tolerance — if you can’t verify it, it fails.
```

### Research Depth QA Agent Prompt (rf-qa-qualitative — Research Gate)

```
Perform qualitative depth assessment of research files for [module/project name] README.

QA phase: research-depth
Research directory: [research-dir-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: ${TASK_DIR}qa/qa-research-depth-report.md
Fix authorization: false

You are evaluating whether the research is genuinely deep or merely surface-level. A research file can be structurally complete (has all sections, cites file paths, marks status as Complete) but qualitatively shallow (lists files without analyzing them, names features without explaining them, copies doc content without verifying it).

CHECKLIST:
1. Analysis depth — for each research file, does it analyze what it found (WHY does this architecture exist, WHAT problems does this feature solve, HOW does this setup work) or merely inventory it (this directory has these files, this module exports these functions)?
2. User perspective — are features described from the user’s perspective (what can someone DO with this?) or from the implementer’s perspective (what classes exist)? README-bound research must be user-oriented.
3. Setup verification — are setup steps traced through actual execution flow (read the script, trace the commands, verify the dependencies) or just copied from existing docs without verification?
4. Gap quality — are identified gaps specific and actionable ("No usage examples found for the CLI interface in test files or docs") or vague ("some areas need more research")?
5. Evidence trail quality — do citations point to specific lines/functions/exports, or just to files? "See backend/app/main.py" is weak; "See backend/app/main.py:45, create_app() function initializes FastAPI with these routers" is strong.

Adversarial framing: "Assume at least 2 research files are qualitatively shallow despite being structurally complete. Find them and explain what depth is missing."

VERDICTS:
- PASS: All research files demonstrate genuine analytical depth appropriate for the tier
- FAIL: Specific files identified as shallow with concrete examples of what depth is missing
```

### Synthesis Review Analyst Prompts (rf-analyst — 2 Lens Instances)

At the synthesis QA gate (Phase 5), spawn 2 rf-analyst instances in parallel, each with a different lens focus. Together they cover the original 9-item Synthesis Quality Review Checklist.

#### Analyst-1: Synthesis-Accuracy Lens

```
Perform synthesis accuracy verification of all synthesis files for [module/project name] README.

Analysis type: synthesis-review
Lens: synthesis-accuracy
Research directory: [research-dir-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: ${TASK_DIR}qa/analyst-synthesis-review-1.md
Fix authorization: false

You focus on whether synthesis content is ACCURATE and TRACEABLE to research files.

PROCESS:
1. Use Glob to find ALL synthesis files in `${TASK_DIR}synthesis/` (files matching synth-*.md)
2. Read EVERY synthesis file
3. For each synthesis file, also read the source research files it references
4. Apply the checklist below
5. Write your report to the output path

CHECKLIST:
1. Section headers match the expected format from the README template — correct section names and ordering per tier
2. Tables use the correct column structure — Prerequisites uses `Tool | Version | Purpose | Install`; Configuration uses `Setting | Default | Description | Required`; FAQ uses `Problem | Solution`
3. No content was fabricated beyond what research files contain — every feature, setup step, and usage example traces to a research file finding
4. Findings cite actual file paths and evidence — every command, dependency, config value traces to an actual source file read
5. No aspirational features presented as current — every feature listed is verified to exist in actual code

Adversarial framing: "Assume the synthesis contains at least 3 accuracy errors or fabricated claims. Find them."

VERDICTS:
- PASS: All synthesis files are accurate and traceable
- FAIL: Issues found (list each with specific location, severity, and remediation action)
```

#### Analyst-2: Source-Tracing Lens

```
Perform source-tracing verification of all synthesis files for [module/project name] README.

Analysis type: synthesis-review
Lens: source-tracing
Research directory: [research-dir-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: ${TASK_DIR}qa/analyst-synthesis-review-2.md
Fix authorization: false

You focus on whether synthesis FAITHFULLY DISTILLS research findings — not fabricated, not over-summarized.

PROCESS:
1. Read ALL synthesis files and their referenced research files
2. For each synthesis claim, trace it back to the source research file
3. Apply the checklist below
4. Write your report to the output path

CHECKLIST:
1. Runnable code examples are actually runnable — install commands reference real packages, scripts reference real npm/make/python commands
2. Front-loaded value — the first ~30 lines answer what/how/where; a reader who stops at line 30 has enough to get started
3. Cross-section consistency — dependencies in Quick Start match those in Configuration; paths in Project Structure match Architecture and Usage
4. Stale documentation discrepancies surfaced — any [CODE-CONTRADICTED] or [STALE DOC] findings from research files appear as notes or are corrected, not silently omitted

Adversarial framing: "Assume at least 3 synthesis claims are over-summarized, distorted, or missing context from the research. Find them."

VERDICTS:
- PASS: Synthesis faithfully represents research findings
- FAIL: Issues found (list each with specific location and remediation)
```

### Synthesis QA Agent Prompts (rf-qa — 2 Lens Instances)

At the synthesis QA gate (Phase 5), spawn 2 rf-qa instances in parallel, each with a different lens focus. Together they cover the original 12-item Synthesis Gate checklist. Both spawn with `fix_authorization: false` (serialized fix protocol).

#### QA-1: Structure Lens

```
Perform structural QA verification of synthesis files for [module/project name] README.

QA phase: synthesis-gate
Lens: structure
Research directory: [research-dir-path]
Fix authorization: false
Output path: ${TASK_DIR}qa/qa-synthesis-gate-report-1.md

You focus ONLY on structural correctness of synthesis files.

NOTE: If >4 synthesis files exist, the orchestrator may partition them across multiple instances.

CHECKLIST:
1. Section headers match the README template — correct section names, ordering, and tier-appropriate inclusion
2. Depth budgets respected — About ≤4 sentences; Features 5-10 items; Quick Start ≤5 steps; Project Structure top 2-3 levels; Architecture ≤1 diagram + 2 paragraphs; Configuration table format; Usage 2-4 examples
3. Content deduplication — no reproduction of content that belongs in companion docs; architecture deep-dives summarized and linked
4. TOC accuracy — if a Table of Contents exists, every entry corresponds to an actual section header
5. README vs Other Documents boundary respected — README covers WHAT/WHY/HOW TO GET STARTED; depth links to companion docs

Adversarial framing: "Assume at least 3 structural issues exist in the synthesis files. Find them."

VERDICTS:
- PASS: All synth files meet structural standards
- FAIL: Issues found (list with specific fixes)
```

#### QA-2: Content-Quality Lens

```
Perform content-quality QA verification of synthesis files for [module/project name] README.

QA phase: synthesis-gate
Lens: content-quality
Research directory: [research-dir-path]
Fix authorization: false
Output path: ${TASK_DIR}qa/qa-synthesis-gate-report-2.md

You focus ONLY on content quality and accuracy of synthesis files.

CHECKLIST:
1. Runnable examples are actually runnable — install commands, scripts, and env vars reference real names from the codebase
2. No fabrication — Verify EVERY claim, trace each to a research file with actual source evidence
3. Evidence citations use actual file paths — no hypothetical or placeholder paths
4. No aspirational features presented as current — every listed feature verified to exist in actual code
5. Audience-appropriate — language and depth match the stated audience
6. Badge validity — if badges are included, they reference real endpoints, not placeholder URLs
7. No hallucinated file paths — verify parent directories exist via Glob or Read

Adversarial framing: "Assume at least 3 content quality issues exist. Find them."

VERDICTS:
- PASS: All synth files meet content quality standards
- FAIL: Issues found (list with specific fixes)
```

### Synthesis Coherence QA Agent Prompt (rf-qa-qualitative — Synthesis Gate)

```
Perform qualitative coherence assessment of synthesis files for [module/project name] README.

QA phase: synthesis-coherence
Synthesis directory: ${TASK_DIR}synthesis/
Research directory: [research-dir-path]
Output path: ${TASK_DIR}qa/qa-synthesis-coherence-report.md
Fix authorization: false

You are evaluating whether the synthesis files tell a coherent story that will produce a useful README. Synthesis can be structurally correct (right headers, right tables, right citations) but incoherent (sections contradict each other, the README won’t flow logically, a newcomer would be confused).

CHECKLIST:
1. Narrative flow — do the synthesis files, read in order, tell a logical story? Does About lead naturally to Features, Features to Prerequisites, Prerequisites to Quick Start? Or are there jarring topic jumps?
2. Cross-section consistency — dependencies mentioned in Quick Start synth match those in Configuration synth; paths in Project Structure synth match those in Architecture synth; features in About synth match those in Features synth
3. Audience alignment — is the language and depth consistent with the stated audience across ALL synth files? One file written for experts while another is written for newcomers creates a disorienting README.
4. Completeness of the README story — would a newcomer who reads these synth files in order understand: what this module is, how to set it up, how to use it, and where to find more? Any missing narrative beats?
5. Deduplication discipline — is content that belongs in companion docs properly summarized-and-linked rather than reproduced? Are synth files respecting the README vs Other Documents boundary?

Adversarial framing: "Assume the synthesis files contain at least 2 coherence issues that would confuse a newcomer. Find them."

VERDICTS:
- PASS: Synthesis files tell a coherent, audience-appropriate story
- FAIL: Specific coherence issues identified with remediation suggestions
```

### Assembly Agent Prompt (rf-assembler)

```
Assemble the final README for [module/project name] from synthesis files.

Component files (in order):
[ordered list of synth file paths]

Output path: [readme-output-path]
Research directory: [research-dir-path]
Template path: .claude/templates/documents/readme_template.md
Depth tier: [Lightweight/Standard/Heavyweight]

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create the output file immediately with the frontmatter and header:
   ---
   status: "Draft"
   created_date: [today]
   last_updated: [today]
   ---
   # [Module/Project Name]

2. As you assemble each section, IMMEDIATELY write it to the output file using Edit.
   Do NOT accumulate the entire README in context and attempt a single write.

3. After each Edit, the file grows. This is correct behavior. Never rewrite from scratch.

Output format — the final README MUST contain these sections in order (per tier).
Sections follow the template at `.claude/templates/documents/readme_template.md`.
Badge order: Build Status → Version → License → Coverage → Downloads. Link each badge to its source dashboard. Use shields.io for consistent styling. Maximum 4-6 badges for most projects (8-10 for major platforms). Dynamic only — no static or decorative badges.

Pre-section elements:
- Frontmatter (status, created_date, last_updated)
- Optional badges (per badge rules above)
- Tagline (1 sentence: what this is and what problem it solves)
- Table of Contents (if README >100 lines; generated from actual section headers after all sections placed)

Numbered sections (per template):
1. About (≤4 sentences — what, why, who)
2. Features (5-10 bullet items — user-facing capabilities, not implementation details)
3. Prerequisites (table: Tool | Version | Purpose | Install link — exact version requirements)
4. Quick Start (≤5 steps from zero to running — copy-pasteable, show expected output for final step)
5. Usage (2-4 runnable examples showing input → output for top use cases)
6. Configuration (summary table: Setting | Default | Description | Required — link to full config docs)
7. Project Structure (top 2-3 directory levels — tree or table format) — Standard/Heavyweight only
8. Architecture (≤1 ASCII/Mermaid diagram + ≤2 paragraphs, then link to tech ref) — Standard/Heavyweight only
9. Development Setup (full contributor setup beyond Quick Start: dev dependencies, IDE config, local services) — Standard/Heavyweight only
10. Testing (how to run tests: 1-3 commands, coverage target, link to test docs) — Standard/Heavyweight only
11. Deployment (brief summary of deployment approach, link to deployment docs) — Heavyweight only
12. Documentation (links organized by audience: For Users / For Contributors / For Operators; link to companion docs) — Heavyweight only
13. Contributing (≤5 bullet steps or link to CONTRIBUTING.md)
14. Roadmap (3-5 items with checkboxes — clearly separate completed from planned; link to project board) — Heavyweight only
15. FAQ / Troubleshooting (collapsible Q&A sections or Problem | Solution table — top 3-5 issues) — Standard/Heavyweight only
16. License (one line: license type + link to LICENSE file)
17. Acknowledgments (brief credits for key dependencies, inspirations, contributors) — Heavyweight only

Post-section element:
- Document History (table: Date | Version | Author | Changes)

Assembly rules:
1. Write the frontmatter, badges, and tagline first
2. Assemble sections in order — read each synth file and write its content into the correct section position
3. Write each section to disk immediately after composing it — do NOT one-shot
4. Generate the Table of Contents from actual section headers after all sections are placed
5. Cross-check internal consistency:
   - Dependencies in Quick Start match those in Configuration
   - Paths in Project Structure match those referenced in Architecture and Usage
   - Commands in Quick Start actually work (reference real scripts/packages)
   - Links in Related Documentation point to real files
6. Flag any contradictions between sections using: [CONTRADICTION: Section A claims X, Section B claims Y]
7. Ensure no placeholder text remains (search for [, TODO, TBD, PLACEHOLDER)

Content rules (non-negotiable):
- Tables over prose whenever presenting multi-item data (dependencies, env vars, directory structure, scripts)
- Runnable examples — every install command, usage snippet, and test command must be copy-pasteable
- Front-load value — first ~30 lines answer what/how/where
- Write for the newcomer — no unexplained jargon, no assumed context
- Evidence cited inline where it adds value: actual file paths, real config keys
- Link to companion docs for depth — do NOT reproduce architecture, exhaustive API docs, deployment procedures, or config deep-dives
- No aspirational content — only describe what exists today in code
- Conciseness over comprehensiveness — scannable, not exhaustive prose
- Uncertainty marked explicitly with "Unverified" callouts

Hard ceiling: 500 lines. If the assembled README exceeds 500 lines, that signals content
duplication or misplaced reference material — move content to companion docs and link.
Tier-specific targets: Lightweight 50-150 lines, Standard 150-400 lines, Heavyweight 200-500 lines.

CRITICAL: You are assembling existing content, not creating new findings. Preserve fidelity
to the synthesis files. Add only minimal transitional text where needed for coherence.
Do NOT attempt full content validation — that is the QA agent's job. Focus on assembly
integrity: correct ordering, internal consistency, no placeholders, all components included.
```

### Lens-Based Final Document QA Agent Prompts

These are 11 separate prompt templates, one per lens agent. At the final document gate (Phase 6, Step 6.2), ALL 11 agents spawn in parallel with `fix_authorization: false`. Each agent focuses on ONE quality dimension and writes to its own report file. After all 11 complete, findings are consolidated and a single fix agent applies all fixes.

**Lens-to-Checklist Mapping (from the original 15+4 validation items):**

| Lens | Agent Type | Original Checklist Items |
|------|-----------|-------------------------|
| template-conformance | rf-qa | Items 1 (sections per tier), 2 (frontmatter), 4 (TOC), 15 (line count) |
| internal-consistency | rf-qa | Items 19 (internal consistency), 18 (TOC accuracy), 7 (prerequisites cross-check via Glob) |
| evidence-quality | rf-qa | Items 14 (file paths exist), 16 (no doc-only claims), 17 (web research marked) |
| completeness | rf-qa | Items 5 (About scope), 6 (Features 5-10 items), 8 (Quick Start steps), 11 (Project Structure depth) |
| actionability | rf-qa-qualitative | Items 8 (Quick Start copy-pasteable), 12 (Architecture diagram + link), 21 (newcomer-friendliness) |
| numbers-metrics | rf-qa-qualitative | Items 10 (no config file reproduction), 15 (line count budget), 3 (badge validity) |
| crossref-chain | rf-qa-qualitative | Items 9 (runnable examples), 14 (file paths exist), 19 (internal consistency) |
| domain-accuracy | rf-qa-qualitative | Items 13 (no aspirational content), 16 (no doc-only claims), 20 (readability) |
| feature-list-accuracy | rf-qa-qualitative | Item 6 (Features user-focused), Item 13 (no aspirational features), trace each feature to source code |
| usage-example-correctness | rf-qa | Item 7 (prerequisites table), Item 9 (usage examples copy-pasteable), spot-check 3+ commands |
| dependency-list-completeness | rf-qa | Item 10 (config), Item 7 (Prerequisites table completeness), match against actual package manifests |

Note: Some original items appear in multiple lenses. This is intentional — overlapping coverage catches issues that single-lens analysis might miss from a different angle.

#### Structural Lens Prompts (rf-qa)

##### Template-Conformance Lens

```
Perform template-conformance validation of the assembled README for [module/project name].

QA phase: lens-template-conformance
Report path: [readme-path]
Depth tier: [Lightweight/Standard/Heavyweight]
Output path: ${TASK_DIR}qa/qa-lens-template-conformance.md
Fix authorization: false

You focus ONLY on template conformance. Do not evaluate content quality, accuracy, or readability.

CHECKLIST:
1. All sections present per tier — Lightweight requires: 1 (About), 2 (Features), 3 (Prerequisites), 4 (Quick Start), 5 (Usage), 6 (Configuration), 13 (Contributing), 16 (License). Standard adds: 7 (Project Structure), 8 (Architecture), 9 (Development Setup), 10 (Testing), 15 (FAQ/Troubleshooting). Heavyweight adds: 11 (Deployment), 12 (Documentation), 14 (Roadmap), 17 (Acknowledgments). Missing sections must be present or explicitly marked N/A with rationale.
2. Frontmatter has all required fields (status, created_date, last_updated)
3. Table of Contents present if README >100 lines, and matches actual section headers
4. Total line count within tier budget — Lightweight: 50-150, Standard: 150-400, Heavyweight: 200-500. Hard ceiling: 500 lines.

Adversarial framing: "Assume this README has at least 3 template conformance errors. Find them."
```

##### Internal-Consistency Lens

```
Perform internal-consistency validation of the assembled README for [module/project name].

QA phase: lens-internal-consistency
Report path: [readme-path]
Output path: ${TASK_DIR}qa/qa-lens-internal-consistency.md
Fix authorization: false

You focus ONLY on internal consistency between sections. Do not evaluate template conformance or content quality.

CHECKLIST:
1. Internal consistency — no contradictions between sections (dependency in Quick Start matches Configuration; paths in Project Structure match Usage examples)
2. TOC accuracy — every entry links to an actual section header, no orphaned or missing entries
3. Runnable examples actually reference real packages, scripts, and commands — spot-check 3+ commands via Glob/Read

Adversarial framing: "Assume this README has at least 3 internal consistency errors. Find them."
```

##### Evidence-Quality Lens

```
Perform evidence-quality validation of the assembled README for [module/project name].

QA phase: lens-evidence-quality
Report path: [readme-path]
Output path: ${TASK_DIR}qa/qa-lens-evidence-quality.md
Fix authorization: false

You focus ONLY on evidence quality — whether claims are backed by verifiable references.

CHECKLIST:
1. File paths referenced in the README actually exist — spot-check 5+ paths via Glob or Read
2. No doc-only claims presented as verified — if a claim comes from documentation alone, it must carry [UNVERIFIED] or be excluded
3. Web research findings include source URLs and are marked as external — never presented as codebase findings

Adversarial framing: "Assume this README has at least 3 unverified or fabricated claims. Find them."
```

##### Completeness Lens

```
Perform completeness validation of the assembled README for [module/project name].

QA phase: lens-completeness
Report path: [readme-path]
Research directory: [research-dir-path]
Output path: ${TASK_DIR}qa/qa-lens-completeness.md
Fix authorization: false

You focus ONLY on completeness — whether all required content from scope discovery made it into the README.

CHECKLIST:
1. About section is ≤4 sentences — what it is, what problem it solves, who it’s for. No implementation details.
2. Features section lists user-facing capabilities (5-10 items) — not implementation details, not architecture components
3. Quick Start is ≤5 steps and every step is copy-pasteable — no "configure as needed" hand-waving
4. Project Structure shows top 2-3 directory levels only — no exhaustive file listings

Adversarial framing: "Assume this README is missing at least 3 required content areas. Find them."
```

#### Content Lens Prompts (rf-qa-qualitative)

##### Actionability Lens

```
Perform actionability assessment of the assembled README for [module/project name].

QA phase: lens-actionability
Report path: [readme-path]
Output path: ${TASK_DIR}qa/qa-lens-actionability.md
Fix authorization: false

You focus ONLY on whether a newcomer can actually USE this README to get started.

CHECKLIST:
1. Quick Start steps are copy-pasteable — no "configure as needed" hand-waving, no missing prerequisites
2. Architecture Overview is ≤1 diagram + 2 short paragraphs, then links to companion Technical Reference
3. Newcomer-friendliness — a developer who has never seen this codebase could understand and set up the module within 15 minutes

Adversarial framing: "Assume a newcomer would get stuck at least 3 times following this README. Find those sticking points."
```

##### Numbers-Metrics Lens

```
Perform numbers and metrics validation of the assembled README for [module/project name].

QA phase: lens-numbers-metrics
Report path: [readme-path]
Output path: ${TASK_DIR}qa/qa-lens-numbers-metrics.md
Fix authorization: false

You focus ONLY on numerical accuracy and metrics.

CHECKLIST:
1. No configuration file reproduction — env vars and config options summarized in tables, not full file dumps
2. Total line count within tier budget — verify against actual count
3. Badge URLs are valid — if badges are included, they reference real endpoints (shields.io with real repo paths)

Adversarial framing: "Assume this README has at least 3 numerical inaccuracies or invalid metrics. Find them."
```

##### Cross-Reference Chain Lens

```
Perform cross-reference chain validation of the assembled README for [module/project name].

QA phase: lens-crossref-chain
Report path: [readme-path]
Output path: ${TASK_DIR}qa/qa-lens-crossref-chain.md
Fix authorization: false

You focus ONLY on tracing chains end-to-end: prerequisite -> install -> config -> usage.

CHECKLIST:
1. Runnable examples reference real packages, scripts, and commands — spot-check 3+ via Glob/Read
2. File paths referenced actually exist — trace the full chain from Prerequisites through Usage
3. Internal consistency of chains — what Prerequisites lists matches what Quick Start installs matches what Configuration configures matches what Usage demonstrates

Adversarial framing: "Assume at least 3 chains are broken (a prerequisite is missing, a command references a nonexistent script, a config key doesn’t exist). Find them."
```

##### Domain-Accuracy Lens

```
Perform domain accuracy assessment of the assembled README for [module/project name].

QA phase: lens-domain-accuracy
Report path: [readme-path]
Output path: ${TASK_DIR}qa/qa-lens-domain-accuracy.md
Fix authorization: false

You focus ONLY on whether claims about the codebase are accurate.

CHECKLIST:
1. No aspirational content presented as current — every feature and capability is verified in actual code
2. No doc-only claims presented as verified — documentation-sourced claims carry appropriate tags
3. Readability — scannable structure with tables, headers, bullets; no walls of prose; newcomer-friendly language

Adversarial framing: "Assume at least 3 claims about the codebase are inaccurate or aspirational. Find them."
```

#### README Domain-Specific Lens Prompts

##### Feature-List-Accuracy Lens (rf-qa-qualitative)

```
Perform feature list accuracy verification of the assembled README for [module/project name].

QA phase: lens-feature-list-accuracy
Report path: [readme-path]
Module source directories: [list of source dirs]
Output path: ${TASK_DIR}qa/qa-lens-feature-accuracy.md
Fix authorization: false

You focus ONLY on whether the Features section (Section 2) accurately reflects what the module actually does.

CHECKLIST:
1. Features are user-focused — described from the user’s perspective ("what can I do?"), not the implementer’s
2. No aspirational features — every feature listed traces to actual implemented code, not docs or plans
3. Source code tracing — for each feature in Section 2, verify it exists in actual source code by reading relevant files

Adversarial framing: "Assume at least 3 features listed are either aspirational, inaccurate, or missing from the source code. Find them."
```

##### Usage-Example-Correctness Lens (rf-qa)

```
Perform usage example correctness verification of the assembled README for [module/project name].

QA phase: lens-usage-example-correctness
Report path: [readme-path]
Output path: ${TASK_DIR}qa/qa-lens-usage-correctness.md
Fix authorization: false

You focus ONLY on whether usage examples, install commands, and CLI snippets actually work.

CHECKLIST:
1. Every install command references real packages that exist in package manifests
2. Every CLI example uses real commands, real flags, and real file paths
3. Spot-check 3+ commands by verifying scripts exist (via Glob), flags are valid, and file paths resolve

Adversarial framing: "Assume at least 3 commands or examples in this README would fail if copy-pasted. Find them."
```

##### Dependency-List-Completeness Lens (rf-qa)

```
Perform dependency list completeness verification of the assembled README for [module/project name].

QA phase: lens-dependency-list-completeness
Report path: [readme-path]
Package manifests: [package.json / requirements.txt / pyproject.toml paths]
Output path: ${TASK_DIR}qa/qa-lens-dependency-completeness.md
Fix authorization: false

You focus ONLY on whether the README’s prerequisites and dependencies match actual package manifests.

CHECKLIST:
1. Prerequisites table completeness — every runtime dependency in manifests appears in README Prerequisites (Section 3)
2. No fabricated dependencies — every dependency listed in the README exists in actual manifests
3. Version accuracy — versions in README match lock files or manifest constraints

Adversarial framing: "Assume at least 3 dependencies are missing, fabricated, or version-mismatched. Find them."
```

#### Consolidated Fix Agent Prompt (rf-qa)

```
Apply consolidated fixes to the README for [module/project name].

QA phase: consolidated-fix
Report path: [readme-path]
Consolidated findings: ${TASK_DIR}qa/qa-consolidated-final-findings.md
Fix authorization: true

You are the ONLY agent authorized to modify the README during this fix cycle. Read the consolidated findings list and apply ALL fixes using Edit. For each fix:
1. Read the finding (what, where, severity)
2. Locate the issue in the README
3. Apply the fix with Edit
4. Verify the fix by re-reading the affected section
5. Log the fix in your report

Do NOT skip any finding. Do NOT introduce new content beyond what is needed to fix the issue.
Write your fix report to ${TASK_DIR}qa/qa-fix-report.md.
```

#### Verification Agent Prompts (1 rf-qa + 1 rf-qa-qualitative)

##### rf-qa Structural Verification Prompt

```
Verify STRUCTURAL fixes applied to the README for [module/project name].

QA phase: fix-verification
Lens: structural-fix-verification
Report path: [readme-path]
Fix report: ${TASK_DIR}qa/qa-fix-report.md
Previous findings: ${TASK_DIR}qa/qa-consolidated-final-findings.md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least one fix was applied incorrectly or incompletely.

YOUR FOCUS: Verify STRUCTURAL correctness of applied fixes only. Content quality is handled by the rf-qa-qualitative verification agent.

For each structural fix claimed in the fix report:
1. Verify the fix was actually applied by reading the relevant section
2. Verify sections are still present and in correct order after fixes
3. Verify formatting is correct (markdown syntax, table structure, code blocks)
4. Verify all file paths referenced remain valid after fixes
5. Verify required elements (frontmatter fields, section headers, tables) still exist
6. Check that no structural elements were accidentally removed or corrupted by fixes

VERDICTS:
- PASS: All structural fixes verified correct, no structural regressions
- FAIL: Specific structural issues found (list each with location)
```

##### rf-qa-qualitative Content Verification Prompt

```
Verify CONTENT quality of fixes applied to the README for [module/project name].

QA phase: fix-verification
Lens: content-fix-verification
Report path: [readme-path]
Fix report: ${TASK_DIR}qa/qa-fix-report.md
Previous findings: ${TASK_DIR}qa/qa-consolidated-final-findings.md
Fix authorization: false

**ADVERSARIAL STANCE:** Assume at least one fix introduced a new content issue.

YOUR FOCUS: Verify CONTENT quality after fixes. Structural correctness is handled by the rf-qa verification agent.

For each content-related fix claimed in the fix report:
1. Verify claims remain accurate after fixes (no introduced inaccuracies)
2. Verify coherence is maintained across the document (fixes didn't create contradictions between sections)
3. Verify content depth is preserved (fixes didn't strip important detail)
4. Verify no new contradictions were introduced by the fixes
5. Verify qualitative issues from the consolidated findings were actually addressed
6. Check that the document still reads naturally and maintains newcomer-friendliness

VERDICTS:
- PASS: All content fixes verified correct, no content quality regressions
- FAIL: Specific content issues found (list each with location and impact)
```

---

### Source-Document Fidelity Gate Agent Prompts

These 2 agents run AFTER the lens-based QA gate passes. They read BOTH the original module source code AND the assembled README, verifying the README faithfully represents what the source code contains. This is fundamentally different from the lens-based gate which reads only the README.

#### Fidelity Coverage Agent (rf-qa)

```
Perform source-document fidelity verification for [module/project name] README.

QA phase: source-fidelity-coverage
README path: [readme-path]
Module source directories: [list of source dirs]
Package manifests: [package.json / requirements.txt / pyproject.toml paths]
Output path: ${TASK_DIR}qa/qa-source-fidelity-coverage.md
Fix authorization: false

You read the module’s actual source code AND the assembled README. Your job is to verify that everything important in the source code is represented in the README.

CHECKLIST:
1. Feature coverage — read source code entry points, exported functions/classes, and route definitions. For each user-facing capability found in code, verify the README’s Features section (Section 2) mentions it. Flag features present in code but absent from README.
2. Dependency coverage — read package.json / requirements.txt / pyproject.toml. Verify every runtime dependency appears in the README’s Prerequisites (Section 3) or is mentioned in Quick Start (Section 4). Flag dependencies present in manifest but absent from README.
3. Setup step coverage — trace the actual setup flow (install commands, env vars, config files, required services). Verify the README’s Quick Start accurately represents this flow. Flag setup requirements present in code but absent from README.
4. Configuration coverage — read actual config files, .env examples, environment variable references. Verify the README’s Configuration section (Section 6) covers the key settings. Flag important config options present in code but absent from README.
5. Entry point accuracy — verify the README correctly identifies the module’s entry points (main files, CLI commands, API routers) by reading actual source.

Adversarial framing: "Assume the README is missing at least 3 features or dependencies that exist in the source code. Find them."

Fix cycle budget: Maximum 3 fix cycles for the fidelity gate. After 3 cycles, HALT and escalate to user.
```

#### Fidelity Phantom Agent (rf-qa)

```
Perform phantom coverage detection for [module/project name] README.

QA phase: source-fidelity-phantom
README path: [readme-path]
Module source directories: [list of source dirs]
Output path: ${TASK_DIR}qa/qa-source-fidelity-phantom.md
Fix authorization: false

You read the module’s actual source code AND the assembled README. Your job is to verify that everything in the README actually exists in the source code — catching phantom features, fabricated commands, and invented paths.

CHECKLIST:
1. Phantom feature detection — for each feature listed in README Section 2, verify it exists in actual source code. Flag features described in README that do not exist in code.
2. Command verification — for each command in Quick Start and Usage, verify the command actually works (script exists, package has the command, flags are valid). Flag fabricated commands.
3. File path verification — for each file path referenced in the README, verify it exists via Glob. Flag invented paths.
4. Environment variable verification — for each env var mentioned in Configuration, verify it is actually read by the code. Flag phantom env vars.
5. Detail preservation — for specific names (function names, class names, config keys) mentioned in the README, verify they match actual source code (correct spelling, correct casing, correct location). Flag mismatches.

Adversarial framing: "Assume at least 3 claims in this README are fabricated or outdated. Find them by reading actual source code."

Fix cycle budget: Maximum 3 fix cycles for the fidelity gate. After 3 cycles, HALT and escalate to user.
```

---
## Output Structure

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

The final README follows this structure. The synthesis agents produce sections that are assembled into this format by the rf-assembler agent, conforming to the template guidelines. Section inclusion scales by tier — Lightweight READMEs omit sections marked (Standard+) or (Heavyweight).

```markdown
---
status: "🟡 Draft"
created_date: [today]
parent_doc: "[path to companion tech reference, if any]"
tier: "[Lightweight | Standard | Heavyweight]"
tags: []
---

<!-- Badges: build status, coverage, license, version — only if CI/CD exists -->
![Build Status](...)  ![Coverage](...)  ![License](...)

# [Module/Service Name]

> **Tagline:** One-sentence description of what this module does and why it matters.

## Table of Contents
<!-- Generated from actual section headers after all sections placed. Include only if README >100 lines. -->

---

## 1. About
<!-- ≤4 sentences. What it is, what problem it solves, who it's for. No implementation details. -->

---

## 2. Features
<!-- 5-10 bullet points. User-focused benefits, not internal implementation. Each feature should answer "what can I do with this?" -->

---

## 3. Prerequisites
<!-- Table format: Tool | Version | Why Needed | Install Link. Only items the user must have BEFORE starting. -->

| Tool | Version | Purpose | Install |
|------|---------|---------|---------|

---

## 4. Quick Start
<!-- ≤5 numbered steps from clone to running. Must be copy-pasteable. Include expected output for final step. -->

---

## 5. Usage
<!-- Runnable code examples for top 2-3 use cases. Show input → output. -->

---

## 6. Configuration
<!-- Summary table: Setting | Default | Description | Required. Link to full config docs if they exist. -->

| Setting | Default | Description | Required |
|---------|---------|-------------|----------|

---

## 7. Project Structure (Standard+)
<!-- Top 2-3 directory levels only. Use tree format. Annotate key directories. -->

---

## 8. Architecture (Standard+)
<!-- ≤1 ASCII/Mermaid diagram + ≤2 paragraphs. Link to tech reference for depth. -->

---

## 9. Development Setup (Standard+)
<!-- Steps beyond Quick Start for contributors: dev dependencies, IDE config, local services. -->

---

## 10. Testing (Standard+)
<!-- How to run tests. Table: Test Type | Command | What It Covers. Link to testing guide if exists. -->

---

## 11. Deployment (Heavyweight)
<!-- Brief deployment overview. Link to deployment guide/operational guide for full procedures. -->

---

## 12. Documentation (Heavyweight)
<!-- Links to companion docs: tech reference, operational guide, API docs, architecture docs. -->

---

## 13. Contributing
<!-- Branch naming, commit format, PR process. ≤5 bullet steps or link to CONTRIBUTING.md. -->

---

## 14. Roadmap (Heavyweight)
<!-- 3-5 upcoming items max. No aspirational features — only planned/in-progress work. -->

---

## 15. FAQ / Troubleshooting (Standard+)
<!-- Table: Problem | Solution. Top 3-5 issues newcomers encounter. -->

| Problem | Solution |
|---------|----------|

---

## 16. License
<!-- One line: license type + link to LICENSE file. -->

---

## 17. Acknowledgments (Heavyweight)
<!-- Credits, third-party libraries, inspiration. -->

---

## Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| [date] | 1.0 | [author] | Initial creation |
```

**Tier-based section inclusion:**
- **Lightweight** (50-150 lines): Sections 1-6, 13, 16 (About, Features, Prerequisites, Quick Start, Usage, Configuration, Contributing, License)
- **Standard** (150-400 lines): All Lightweight + Sections 7-10, 15 (Project Structure, Architecture, Dev Setup, Testing, FAQ)
- **Heavyweight** (200-500 lines): All Standard + Sections 11-12, 14, 17 (Deployment, Documentation, Roadmap, Acknowledgments)

**Hard ceiling: 500 lines.** If the assembled README exceeds 500 lines, that signals misplaced reference material or content duplication. Trim before presenting.

---

## Synthesis Mapping Table (Reference)

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

This is the standard mapping of synthesis files to README template sections. Adjust based on module complexity — simple modules can combine more sections per synth file. Complex multi-system modules may need additional synth files.

| Synth File | Template Sections | Source Research Files |
|------------|-------------------|----------------------|
| `synth-01-about-features.md` | 1. About, 2. Features | Codebase structure, existing docs, package.json/pyproject.toml, main entry points |
| `synth-02-prerequisites-quickstart.md` | 3. Prerequisites, 4. Quick Start | Dependency files, setup scripts, Docker configs, install docs |
| `synth-03-usage-config.md` | 5. Usage, 6. Configuration | API endpoints, CLI commands, config files, .env examples, existing usage docs |
| `synth-04-structure-architecture.md` | 7. Project Structure, 8. Architecture | Directory layout, import graphs, service boundaries, companion tech reference |
| `synth-05-devsetup-testing.md` | 9. Development Setup, 10. Testing | Dev scripts, test configs, CI workflows, CONTRIBUTING.md, test documentation |
| `synth-06-deployment-docs-contributing.md` | 11. Deployment, 12. Documentation, 13. Contributing | Deployment configs, existing docs inventory, git hooks, PR templates |
| `synth-07-roadmap-faq-license.md` | 14. Roadmap, 15. FAQ/Troubleshooting, 16. License, 17. Acknowledgments | Issue trackers, known issues, LICENSE file, package dependencies, README history |

**Tier scaling:** For Lightweight READMEs, synth files 04-07 are either omitted or heavily condensed. For Standard, synth files 06-07 are condensed. Only Heavyweight uses all 7 synth files at full depth.

---

## Synthesis Quality Review Checklist

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

**This checklist is enforced by 5 lens-based agents** (see Phase 5 in the BUILD_REQUEST phase definitions above). The 9 criteria below are distributed across 2 rf-analyst instances (synthesis-accuracy lens + source-tracing lens) and 2 rf-qa instances (structure lens + content-quality lens), with 1 rf-qa-qualitative (synthesis-coherence lens) providing narrative quality assessment. All 5 agents spawn with fix_authorization: false; a single fix agent applies consolidated findings using the serialized fix protocol.

The 9 criteria (used by rf-analyst):

1. Section headers match the expected format from the Output Structure template — About, Features, Prerequisites, Quick Start, Usage, Configuration, Project Structure, Architecture, etc.
2. Tables use the correct column structure — Prerequisites uses `Tool | Version | Purpose | Install`; Configuration uses `Setting | Default | Description | Required`; FAQ uses `Problem | Solution`
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and evidence (not vague descriptions) — every setup step, config value, and usage example traces to an actual codebase file
5. Code examples are runnable — commands and code snippets should be copy-pasteable and produce the described output
6. Front-loaded value — About section ≤4 sentences, Features section answers "what can I do?", Quick Start ≤5 steps
7. All cross-references between sections are consistent (e.g., dependency in Prerequisites matches what Quick Start installs; config settings in Configuration match what Usage examples reference)
8. **No aspirational features.** Every feature listed in Section 2 must be traceable to actual implemented code. Planned/future features belong only in Section 14 (Roadmap) and must be explicitly marked as not-yet-implemented
9. **Stale documentation discrepancies are surfaced.** Any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings from research files should appear in the FAQ/Troubleshooting section or as inline warnings, not silently omitted

The rf-qa agent's Synthesis Gate adds 3 additional checks (10-12): depth budget compliance (About: 3-8 lines; Features: 10-20 lines; Prerequisites: 5-15 lines; Quick Start: 10-25 lines; Usage: 15-40 lines; Configuration: 10-30 lines; per-section budgets scale by tier), content deduplication with companion Technical References (README should distill and link, not reproduce), and hallucinated file path detection. If synthesis QA fails, the QA agent fixes issues in-place (when authorized) and issues remaining unfixed trigger re-synthesis of the affected files.

---

## Assembly Process

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

The assembly step reads all synth files in order and produces the final README. Follow these 4 steps:

1. **Write the README header** — frontmatter (status, created_date, parent_doc, tier, tags), badges (only if CI/CD exists), module title as H1, and tagline blockquote
2. **Assemble sections in template order** — read each synth file and write its content into the correct section position, writing incrementally section by section (do NOT one-shot the entire README). Only include sections appropriate for the tier. Sections not covered by a synth file are written directly during assembly from patterns observed in the synth files.
3. **Write the Table of Contents** — generate from actual section headers after all sections are placed. Only include if README exceeds 100 lines.
4. **Cross-check internal consistency** — verify that:
   - Prerequisites listed in Section 3 match what Quick Start (Section 4) installs/requires
   - Configuration settings in Section 6 match what Usage examples (Section 5) reference
   - Project Structure paths (Section 7) match actual directories (spot-check via Glob)
   - Architecture description (Section 8) is consistent with Project Structure
   - All internal links resolve to actual section headers
   - No placeholder text remains (search for `[`, `TODO`, `TBD`, `PLACEHOLDER`)
   - Total line count is within tier budget (Lightweight: 50-150, Standard: 150-400, Heavyweight: 200-500) — hard ceiling 500 lines
   - No content duplicated from companion tech reference — README links to it instead

---

## Validation Checklist

Before presenting the README to the user, validate against this checklist. In the lens-based QA architecture, these items are distributed across 11 lens agents (see Lens-Based Final Document QA Agent Prompts section for the mapping). Each lens agent receives only its assigned subset of items, enabling focused evaluation. The full checklist is preserved here as the canonical reference:

- [ ] **(1)** All sections appropriate for the tier are present — or explicitly marked N/A with rationale
- [ ] **(2)** Frontmatter has all required fields (status, created_date, parent_doc, tier, tags)
- [ ] **(3)** Badges only present if CI/CD pipeline actually exists (no aspirational badges)
- [ ] **(4)** Table of Contents present if README exceeds 100 lines, and matches actual section headers
- [ ] **(5)** About section is ≤4 sentences — what it is, what problem it solves, who it's for
- [ ] **(6)** Features section lists 5-10 user-focused items answering "what can I do with this?" — no internal implementation details
- [ ] **(7)** Prerequisites table has Tool/Version/Purpose/Install columns with actual values
- [ ] **(8)** Quick Start is ≤5 numbered steps from clone to running, with expected output for final step
- [ ] **(9)** Usage examples are runnable — commands and code snippets are copy-pasteable
- [ ] **(10)** Configuration summary table has Setting/Default/Description/Required columns
- [ ] **(11)** Project Structure shows top 2-3 directory levels only (not exhaustive file listings)
- [ ] **(12)** Architecture section uses ≤1 diagram + ≤2 paragraphs — links to tech reference for depth
- [ ] **(13)** No aspirational features — every feature listed traces to actual implemented code
- [ ] **(14)** All file paths reference actual files that exist (spot-check 5+ paths via Glob or Read)
- [ ] **(15)** Total line count within tier budget (Lightweight: 50-150, Standard: 150-400, Heavyweight: 200-500) — hard ceiling 500 lines
- [ ] **(16)** No doc-only claims presented as verified — if a claim comes from documentation alone (no code verification), it must carry an [UNVERIFIED] tag or be excluded
- [ ] **(17)** Web research findings include source URLs and are marked as external — never presented as codebase findings

**Content quality checks (applied after structural validation):**

- [ ] **(18)** TOC accuracy — every entry links to an actual section header in the README, no orphaned or missing entries
- [ ] **(19)** Internal consistency — no contradictions between sections (e.g., dependency in Prerequisites matches Quick Start; paths in Project Structure match those in Usage examples)
- [ ] **(20)** Readability — scannable structure with tables, headers, bullets; no walls of prose; newcomer-friendly language throughout
- [ ] **(21)** Newcomer-friendliness — a developer who has never seen this codebase could use the README to understand what the module does, set it up, and start using it within 15 minutes
- [ ] **(22)** Every agent prompt includes its required protocol blocks (Incremental Writing for all, ADVERSARIAL STANCE for QA, Documentation Staleness for research)
- [ ] **(23)** If a design spec, detailed requirements document, or comprehensive user description was provided as input, every feature/requirement described in the source is represented in the generated output (run section-by-section coverage check against the source)

**Lens-based QA distribution (for task file encoding):**

- [ ] All 11 lens agents spawned with focused prompts (not generic "check everything")
- [ ] All lens agents spawned with fix_authorization: false (serialized fix protocol)
- [ ] Consolidated findings list created from all 11 reports before any fixes applied
- [ ] Single fix agent applied ALL consolidated fixes
- [ ] Verification round (2 agents) confirmed fixes after each fix cycle
- [ ] Source-document fidelity gate ran AFTER lens-based gate passed (2 fidelity agents minimum)
- [ ] Fidelity agents read actual module source code, not just the README
- [ ] No intermediate QA gate (research-gate, synthesis-gate) in the task file uses fewer than 5 total agents, and no final QA gate (report-validation, source-fidelity) uses fewer than 6 total agents

---

## Content Rules (From Template — Non-Negotiable)

These rules come from the README template's guidelines. Every README must follow them.

| Rule | Do | Don't |
|------|-----|-------|
| **About** | ≤4 sentences: what it is, what problem it solves, who it's for | Multi-paragraph history, implementation details, or marketing copy |
| **Features** | 5-10 user-focused bullets answering "what can I do?" | Internal implementation details, architecture descriptions, or aspirational features |
| **Quick Start** | ≤5 numbered copy-pasteable steps with expected output | Lengthy setup narratives, optional steps mixed with required ones |
| **Usage** | Runnable code examples showing input → output for top use cases | Exhaustive API reference (that belongs in API docs or tech reference) |
| **Configuration** | Summary table: Setting / Default / Description / Required | Full .env file reproductions or exhaustive config dumps |
| **Project Structure** | Top 2-3 directory levels with annotations | Complete file tree or listing every file |
| **Architecture** | ≤1 diagram + ≤2 paragraphs; link to tech reference for depth | Multi-page architecture deep-dives (those belong in tech reference) |
| **Contributing** | ≤5 bullet steps or link to CONTRIBUTING.md | Full contributor guide (link to CONTRIBUTING.md instead) |
| **Documentation** | Organize links by audience (For Users / For Contributors / For Operators); include subsystem doc table for monorepos | Flat link dump without audience segmentation |
| **Roadmap** | 3-5 items using checkboxes; clearly separate completed milestones from planned work; link to project board | Aspirational wish lists, features without implementation plans, or planned features listed as current |
| **Badges** | Only badges backed by actual CI/CD pipelines or real metrics | Aspirational badges for pipelines that don't exist yet |
| **Deduplication** | Link to companion docs (tech reference, operational guide, API docs) for depth | Reproduce content that already exists in another document |
| **Evidence** | Inline citations: `package.json`, `src/config/`, `docker-compose.yml:12` | "The system uses X" without pointing to where |
| **Uncertainty** | Explicit [UNVERIFIED] markers or exclude uncertain claims | Present uncertain findings as verified facts |

**README content boundaries — what belongs where:**

| Content Type | Belongs In | NOT in README |
|-------------|-----------|---------------|
| What it does + quick setup | README | |
| Exhaustive component analysis | Tech Reference | README |
| Setup/deployment procedures | Operational Guide | README |
| API endpoint details | API Documentation | README |
| Product requirements | PRD | README |
| Engineering specifications | TDD | README |
| Full configuration reference | Config docs or .env.example | README |
| Test fixture inventories | Testing tech reference | README |
| Architecture deep-dives | Tech Reference or Architecture docs | README |
| Code conventions and standards | CONTRIBUTING.md or CLAUDE.md | README |
| AI agent instructions | CLAUDE.md / AGENTS.md | README |
| Changelog | CHANGELOG.md | README |
| Troubleshooting procedures | Operational Guide (for ops) or FAQ section (for dev) | README (beyond top 5 issues) |

**General principle:** The README is a navigational entry point and quick-start guide. It should never duplicate content that has a canonical home elsewhere. When in doubt, write a one-line summary and link to the canonical source.

**Template guideline enforcement mapping:** These rules enforce the 6 guidelines from `.claude/templates/documents/readme_template.md`:
- **Guideline A** (Length Targets) — Tier Selection section and line budget rules
- **Guideline B** (Content Rules) — Do/Don't table above
- **Guideline C** (README vs Other Documents) — Boundary table above and Synthesis prompt Rule 10
- **Guideline D** (Monorepo Rules) — Heavyweight tier definition, Project Structure depth limits, and monorepo-specific rules: root README as navigation hub, subsystem READMEs follow Lightweight/Standard tier, include "Where Do I Go For...?" table mapping tasks to directories/docs, do NOT document all subsystems in root README, Quick Start shows simplest unified start command
- **Guideline E** (Badge Guidelines) — Badges row above and Assembly prompt badge rules (4-6 max for most projects, 8-10 for major platforms; dynamic only; order: Build Status, Version, License, Coverage, Downloads; link each to source dashboard; use shields.io for consistent styling; remove broken/unconfigured badges)
- **Guideline F** (Anti-Patterns) — Don't column above and Validation Checklist checks

---

## Critical Rules (Non-Negotiable)

These are SKILL-SPECIFIC content rules that apply across ALL phases. Violations compromise document quality.

Three execution-discipline rules (task-file-source-of-truth, maximize-parallelism, use-dedicated-tools) are enforced by the `/task` skill and do not appear here. The incremental-writing mandate is retained as Rule 9 below because it is a content-quality requirement specific to this skill's multi-agent research pipeline, not just an execution mechanism. When other skills complete their /task integration, they will also use this reduced set.

1. **Codebase is source of truth.** For claims about features, setup steps, and configuration, actual source code overrides documentation. Web research supplements but never overrides verified code findings.

2. **Evidence-based claims only.** Every finding must cite actual file paths, function names, config values. No assumptions as facts. If unverifiable, mark as "Unverified."

3. **Gap-driven web research.** Investigate the codebase first, identify specific gaps, then target web research at those gaps. This keeps web research focused and efficient.

4. **Documentation is not verification.** Internal docs describe intent or historical state — NOT necessarily current state. A doc saying "Module X supports feature Y" does not prove it. Only reading actual source code proves it. Research agents MUST cross-validate every feature claim against actual code using verification tags.

5. **Preserve research artifacts.** Research and synthesis files persist after the README is written. They serve as the evidence trail for all claims and enable future re-investigation without starting from scratch. Do NOT delete research files, synthesis files, or the gaps log after assembly.

6. **Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. The synthesis phase relies on these connections to build a coherent picture across investigation slices.

7. **Report all uncertainty.** If something is unclear, ambiguous, or requires a judgment call, document it in Open Questions. Do not silently pick one interpretation and present it as fact.

8. **Quality gates mandatory with lens-based minimums.** Intermediate gates (research, synthesis): minimum 5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative) with lens-based focus and serialized fix authorization. Final document gate: minimum 11 lens agents (4 structural rf-qa + 4 content rf-qa-qualitative + 3 readme domain-specific) with serialized fix protocol (report-only -> consolidate -> single fix agent -> verification). Source-document fidelity gate: minimum 2 rf-qa fidelity agents reading module source code + assembled README. Max fix cycles: 3 for research gate, 2 for synthesis gate, 3 for final document gate, 3 for fidelity gate. After max fix cycles, HALT and ask user for guidance. ALL findings must be resolved. An intermediate QA gate (research-gate, synthesis-gate) with fewer than 5 total agents is PROHIBITED. A final QA gate (report-validation, source-fidelity) with fewer than 6 total agents is PROHIBITED.

9. **No one-shotting documents.** Agents must write incrementally as they discover information. The assembler must write the final README section by section. This is non-negotiable.

10. **Partitioning thresholds.** When >6 research files exist (Phase 3) or >4 synthesis files exist (Phase 5), spawn MULTIPLE instances of each agent role in parallel, each with an `assigned_files` subset. At the final document gate, all 11 lens agents read the full README (no section partitioning needed for <500 line READMEs due to the 500-line hard ceiling). Source fidelity agents each read full README + their assigned source file subset.

11. **Default tier is Standard.** Unless the module is clearly a single-file utility (<3 source files) or a complex multi-system platform (15+ packages/services), use the Standard tier.

12. **Docs-vs-code trust hierarchy.** Critical Rule 1 establishes that web research never overrides code. The same applies to internal documentation: if a doc describes features that the code doesn't implement, **the code is correct and the doc is aspirational**. This is especially dangerous because internal docs feel authoritative — but a doc written months ago about planned features may describe capabilities that were never built. Treat internal docs with the same skepticism as external blog posts unless code-verified.

13. **No content duplication.** Before synthesis, identify all existing documents in the same domain (companion tech references, operational guides, API docs). During synthesis and assembly, never reproduce content that already exists in those documents — link to it instead. If a companion Technical Reference exists, the README defers to it for architecture details, component inventories, config deep-dives, and exhaustive analysis. The README is a navigational entry point; the tech reference is exhaustive.

14. **READMEs must stay under 500 lines.** If the assembled README exceeds 500 lines, that signals misplaced reference material or content duplication. Trim before presenting. Move exhaustive material to a companion tech reference or link to existing docs.

15. **Anti-orphaning — task-completion items inside final phase.** Task completion actions (update frontmatter, notify user, write completion log) are checklist items within the final phase of the task file, never in a separate Post-Completion section. This prevents them from being orphaned if context compresses after the last substantive phase.

16. **README is a navigational entry point, NOT documentation.** The README answers: What is this? How do I set it up? How do I use it? Where do I find more? It does NOT answer: How does it work internally? What are all the configuration options? How do I deploy it to production? Those answers belong in companion documents that the README links to.

17. **QA gates are checklist items, not prose.** Every QA gate specified in QA_GATE_REQUIREMENTS must appear in the generated task file as a `- [ ]` checklist item following B2 self-contained pattern. QA gates described only in prose or comments are invisible to the F1 executor and will be skipped.

18. **Every agent prompt MUST include ALL mandatory protocol blocks:** Incremental File Writing Protocol (all agents), ADVERSARIAL STANCE (QA/analyst agents), Documentation Staleness Protocol (research agents). Missing protocol blocks are the most common generation defect — verify every prompt individually.

19. **Single-agent large-input prohibition.** No single agent may read more than ~1000 lines of input at any discovery, analysis, or extraction stage. Large inputs MUST be partitioned into slices, with one agent per slice spawned in parallel. The rf-task-researcher agent type is permitted per slice but not as a replacement for parallelism. Violations cause shallow coverage and defeat the Deep-tier depth guarantee.

20. **No scope/cost-anxiety pauses during execution.** Once a task file begins executing (via /task or any execution loop), the executor MUST process every item sequentially to completion. It MUST NOT pause mid-execution to present the user with options like "stop here and review, or continue to phase N?" or to flag scope/cost/time concerns. Scope is established at task file creation time. Cost is committed when the user invokes execution. The only permitted mid-execution halts are: all items blocked by the same unrecoverable issue, phase-gate QA failing 3 fix cycles, or an item output fundamentally invalidating the rest of the task. "This will take a while" / "Phase N is expensive" / "the user might want to review" are NOT valid halt reasons. Pausing for these reasons violates the F1 loop discipline and the skill's trust model.

21. **Serialized fix authorization at all multi-agent gates.** When 3+ QA agents evaluate the same document, ALL agents spawn with `fix_authorization: false` (report-only). After all reports are collected, findings are consolidated into a single list. ONE fix agent (rf-qa, fix_authorization: true) applies ALL fixes. Then 2 verification agents confirm fixes. This prevents contradictory parallel edits. The only exception: when a gate has exactly 2 agents evaluating different files (not the same file), parallel fix authorization is acceptable.

22. **Source-document fidelity is mandatory for all READMEs.** Every assembled README must pass a source-document fidelity gate where agents read the module's actual source code alongside the README. This gate runs AFTER the lens-based structural/content QA gate. Internal-only QA (reading only the README) catches formatting and consistency issues but misses semantic fidelity: phantom features, fabricated commands, missing dependencies. The fidelity gate catches these.

---

## Research Quality Signals

### Strong Investigation Signals
- Findings cite specific file paths and actual code constructs (function names, class names, exports)
- Features listed are linked to actual implemented code, not just documentation claims
- Setup steps verified by reading actual dependency files (package.json, requirements.txt, Dockerfile)
- Companion tech reference properly distilled — README summarizes and links rather than reproducing
- Gaps are specific and actionable ("No usage examples found in existing docs or test files")
- Doc-sourced feature claims carry verification tags (cross-validated against actual source code)
- Quality gate reports show PASS with evidence trails linking claims to source files
- Analyst and QA reports agree on coverage completeness

### Weak Investigation Signals (Redo)
- Vague descriptions without file paths ("the module provides various utilities")
- Assumptions stated as facts ("this probably supports configuration via environment variables")
- Features described from documentation alone without code verification
- Full configuration file reproductions instead of summary tables
- No cross-references between research files
- Doc-sourced feature claims without verification tags — if a research file describes features and the evidence trail only points to documentation files (no actual source code paths), the investigation is incomplete
- Quality gate reports show issues but no fix cycles were attempted
- Aspirational features mixed with implemented features without distinction

### When to Spawn Additional Agents
- A research agent flags a gap that is critical to README accuracy (e.g., can't determine prerequisites)
- Two agents' findings contradict each other — need a tie-breaker investigation
- The scope turns out larger than initially estimated (e.g., module has sub-packages not in original plan)
- New companion documents discovered that need deduplication analysis
- Web research reveals setup patterns that need codebase verification
- Quality gate analyst identifies coverage gaps that require additional research tracks

---

## Artifact Locations

| Artifact | Location |
|----------|----------|
| MDTM task file | `${TASK_DIR}TASK-README-<subject>-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research/research-notes.md` |
| Research files | `${TASK_DIR}research/[NN]-[topic].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Gaps log | `${TASK_DIR}gaps-and-questions.md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Analyst reports (research) | `${TASK_DIR}qa/analyst-completeness-report-[N].md` (2 instances) |
| QA reports (research gate) | `${TASK_DIR}qa/qa-research-gate-report-[N].md` (2 instances), `${TASK_DIR}qa/qa-research-depth-report.md` |
| Consolidated findings (research) | `${TASK_DIR}qa/qa-consolidated-research-findings.md` |
| Analyst reports (synthesis) | `${TASK_DIR}qa/analyst-synthesis-review-[N].md` (2 instances) |
| QA reports (synthesis gate) | `${TASK_DIR}qa/qa-synthesis-gate-report-[N].md` (2 instances), `${TASK_DIR}qa/qa-synthesis-coherence-report.md` |
| Consolidated findings (synthesis) | `${TASK_DIR}qa/qa-consolidated-synthesis-findings.md` |
| QA lens reports (final gate) | `${TASK_DIR}qa/qa-lens-[lens-name].md` (11 reports) |
| Consolidated findings (final) | `${TASK_DIR}qa/qa-consolidated-final-findings.md` |
| QA fidelity reports | `${TASK_DIR}qa/qa-source-fidelity-coverage.md`, `${TASK_DIR}qa/qa-source-fidelity-phantom.md` |
| Final README | `[target-path]/README.md` (user-specified or module root) |

Research, synthesis, and QA report files persist — they serve as the evidence trail for claims in the README and can be re-used when the document needs updating.

---

## Tech-Reference-to-README Pipeline

When a companion Technical Reference exists for the module, the README creation follows an enhanced flow:

1. **Tech Reference Extraction** (Step 1.2) — read the companion tech reference and extract README-relevant content (overview, key features, prerequisites, configuration summary, architecture overview) into a dedicated research file (`${TASK_DIR}research/00-tech-ref-extraction.md`)
2. **Content Distillation** — the README distills tech reference content rather than re-investigating. Features, architecture, and configuration are summarized from the tech reference rather than independently researched from scratch
3. **Direct Synthesis Feed** — extracted tech reference content feeds synthesis directly, reducing the number of codebase research agents needed. Research agents focus on gaps the tech reference doesn't cover (Quick Start verification, usage examples, FAQ items)
4. **Fallback to Full Research** — if no companion tech reference exists, the full codebase research path is the primary investigation method. All sections are researched from source code and configuration files
5. **Cross-linking** — the README's frontmatter `parent_doc` field links to the tech reference, and Section 12 (Documentation) links to it as the primary depth resource

This pipeline ensures that READMEs built from tech references are consistent with the authoritative technical documentation without information loss or contradictory claims.

---

## Updating an Existing README

When the user wants to update (not create) an existing README:

1. Read the current README to understand what's already covered and its current tier/line count
2. Research only the changed/new areas (don't re-research everything)
3. Write new research files for the changes: `${TASK_DIR}research/update-[date]-[topic].md`
4. Edit the relevant sections of the README in place — do not rewrite the entire file
5. Update the frontmatter with the new date and any changed fields
6. Update Document History with what changed

After updates, verify the README still falls within its tier line budget. If updates push it over the ceiling (500 lines), trim by moving detailed content to companion documents and linking.

---

## Session Management

Session management is provided by the `/task` skill. When resuming a session:

1. Check for an existing task folder matching `TASK-README-*/` in `.dev/tasks/to-do/`
2. If found, invoke `/task` with the task file path inside the folder — it will resume from the first unchecked item
3. Check for existing research files in `${TASK_DIR}research/` for context
4. Read any analyst/QA gate reports to understand which gates have already passed

If no task file exists but research files are present, the user likely needs to restart from Stage A (scope discovery).
