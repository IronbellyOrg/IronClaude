---
name: task-builder
description: "Build MDTM task files from user requests via parallel codebase research, quality gates, and automated task file creation. Use this skill when the user wants to build a task file, create a task, create an MDTM task, build a task for a specific goal, or when the user provides a BUILD_REQUEST file path. Trigger on phrases like 'build a task file for...', 'create a task for...', 'rf task builder', 'build a task for...', 'create an MDTM task for...', 'task-builder for...', or when the user references a BUILD-REQUEST*.md file."
---

# RF Task Builder

Creates MDTM task files by researching the actual codebase with parallel agents, running quality gates, and spawning the `rf-task-builder` agent to produce a validated, ready-to-execute task file. This skill uses Rigorflow's Agent tool for all subagent spawning — no agent teams, enabling concurrent task builds.

**How it works:** The skill performs scope discovery, spawns parallel researcher agents via the Agent tool, runs rf-analyst + rf-qa quality gates on the research, optionally spawns web research agents, then spawns the `rf-task-builder` agent with a structured BUILD_REQUEST to create the MDTM task file. After the builder returns, rf-qa validates the task file in task-integrity mode. The skill presents the validated task file path and execution command to the user.

When invoked directly by a user (`/task-builder`), this skill stops after task file creation — the user reviews the task file and executes it with `/task [path]` when ready. When invoked by a calling skill (`Source: skill-delegated` in the BUILD_REQUEST), this skill outputs only the task file path so the calling skill can continue to its own Stage B.

## Why This Process Works

Task files go wrong when built from memory, shallow exploration, or unverified assumptions. This skill forces every task item through evidence-based codebase research — parallel agents read actual source files, trace actual dependencies, and document actual behavior with file paths and line numbers.

The multi-phase structure (scope discovery → parallel research → **analyst verification** → **QA gate** → builder → **task file validation** → **qualitative review**) prevents four common failure modes:

- **Context rot** — By isolating each research topic in its own subagent with its own output file, no single agent needs to hold the entire investigation in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning many parallel agents (each focused on one topic slice from the scope map), the research goes deep on every aspect simultaneously rather than skimming across everything sequentially. Minimum 3 researchers per track, scaling to 8 for complex scopes.
- **Hallucinated content** — By separating research (what exists) from task file creation (what to do about it), each phase can be verified independently. The builder only works from verified research files, not from memory or inference. Research claims are evidence-based with file paths and line numbers.
- **Uncaught quality drift** — Lens-based multi-agent QA provides independent verification at three critical gates: after research (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative = 5 agents minimum, each with a focused lens), after task file creation (2 rf-qa structural + 1 rf-analyst research-alignment + 2 rf-qa-qualitative content = 5 agents across A.10/A.10.25/A.10.5, meeting I19 intermediate gate floor). The QA agents assume everything is wrong until independently verified — zero-trust verification prevents rubber-stamping. Serialized fix authorization (report-only agents first, then single fix agent) prevents parallel fix churn. Generated task files are also validated for QA gate sufficiency — any gate with fewer than 6 agents is rejected.

The research artifacts persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and provide the evidence trail for all task file items.

---

## Input

The skill needs five pieces of information to produce a well-researched task file. The first is mandatory; the rest are optional but improve output quality.

1. **GOAL — what task to build** (mandatory) — What the task file should accomplish when executed. This can be a natural language description, a structured request, or a pointer to source files/directories. Examples: "Create API documentation for all handlers", "Refactor the auth middleware and add tests", "Build a new feature for project templates".

2. **WHY — context** (strongly recommended) — Why this task is needed and what constraints apply. This shapes the task file's scope and verification criteria. Examples: "we need docs for onboarding new engineers", "the current auth is non-compliant with new security requirements", "product wants this for the Q2 release".

3. **WHERE — source directories** (optional, saves significant research time) — Specific directories, files, or subsystems the task involves. Prevents researchers from spending time on irrelevant areas. Examples: `backend/app/api/v1/`, `frontend/app/wizard/`, `backend/app/services/auth_service.py`.

4. **BUILD_REQUEST file path** (optional) — A `.md` file containing a structured build request. Used for programmatic invocation by other skills or when the request is too complex for a one-line prompt. The file should contain GOAL, WHY, OUTPUTS, CONTEXT, and optionally TEMPLATE preference.

5. **`--spec <path>` -- driving spec/PRD/TDD** (optional) -- The path to the driving specification, PRD, or TDD that the task implements. When supplied it is threaded into the PRE reflect gate's coverage audit (the `--mode pre --spec <path>` call at A.10.7). The O1 POST gate is a flat `superclaude reflect run` wrapper shell-out that does NOT take `--spec` (it audits the executed diff via the wrapper's own base resolution), so `--spec` flows to the PRE gate only. Resolved in priority order: explicit `--spec <path>` -> an `@file` reference in the GOAL -> a `SPEC:`/`PRD:`/`TDD:` field in a BUILD_REQUEST file -> none. Written to the generated tasklist frontmatter as `spec_path:`. Examples: `--spec .dev/proposals/reflect-in-task-builder.md`, `--spec docs/specs/auth-system-prd.md`.

### Skill-Delegated Build Requests

When a calling skill (tech-research, tech-reference, tdd, prd, operational-guide, readme, repo-cleanup) invokes this skill via `Skill(skill: "task-builder", args: "<BUILD-REQUEST-file-path>")`, the BUILD-REQUEST file uses the `Source: skill-delegated` convention to signal that scope discovery and research notes are pre-computed.

**Skill-delegated BUILD-REQUEST metadata fields:**

| Field | Required | Default | Purpose |
|-------|----------|---------|---------|
| `Source` | Yes | `user` (when absent) | `skill-delegated` signals pre-computed scope discovery |
| `Calling Skill` | Yes (skill-delegated) | -- | Which skill invoked task-builder (logging/diagnostics) |
| `Task Directory` | Yes (skill-delegated) | -- | Pre-created task directory path (task-builder uses this, does NOT create TASK-RF-*) |
| `Research Notes` | Yes (skill-delegated) | -- | Path to research-notes.md written by calling skill |
| `Research Notes Status` | Yes (skill-delegated) | -- | `Complete` or `In Progress` |
| `SKIP_RESEARCHERS` | No | `true` (skill-delegated), `false` (user-invoked) | Whether to skip the researcher layer (A.7-A.8.5) |

**SKIP_RESEARCHERS defaults:** When `Source: skill-delegated` is present, SKIP_RESEARCHERS defaults to `true` because the calling skill already performed domain-specific scope discovery and wrote comprehensive research notes. Skills that want the additional researcher layer can explicitly set `SKIP_RESEARCHERS: false`.

**Example BUILD-REQUEST.md header for skill-delegated invocations:**

```markdown
# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-reference
Task Directory: .dev/tasks/to-do/TASK-TECHREF-docker-compose-20260401-120000/
Research Notes: .dev/tasks/to-do/TASK-TECHREF-docker-compose-20260401-120000/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

GOAL: ...
WHY: ...
[rest of BUILD_REQUEST as normally structured]
```

### Effective Prompt Examples

**Strong — explicit goal with scope and deliverables:**
> Build a task file to create API documentation for all 14 handlers in `backend/app/api/v1/`. Output docs to `docs/api/` as individual markdown files per handler.

**Strong — build request file (user-invoked):**
> Build a task from `.dev/tasks/to-do/existing-doc-template-convergence/BUILD-REQUEST-TASK-FILE-REMEDIATION.md`

**Strong — skill-delegated build request:**
> /task-builder .dev/tasks/to-do/TASK-TECHREF-docker-compose-20260310/BUILD-REQUEST.md

**Strong — clear goal with context:**
> Create a task to refactor the auth middleware. The current session token storage doesn't meet compliance requirements. Focus on `backend/app/core/security.py` and `backend/app/core/middleware.py`.

**Weak — topic only (will work but requires more researcher exploration):**
> Build a task for documenting the handlers.

**Weak — no goal specified (skill cannot proceed):**
> Build a task.

### What to Do If the Prompt Is Incomplete

If the user provides only a vague request or no clear goal, **do NOT proceed immediately**. Ask the user to clarify using this template:

> I can build a task file for you. To make it focused and comprehensive, can you help me with:
>
> 1. **What should the task accomplish?** (e.g., "create API docs for the handlers", "refactor the auth system", "add tests for the services")
> 2. **Why is this needed?** (e.g., "onboarding new engineers", "compliance requirement", "tech debt cleanup")
> 3. **Any specific directories or files involved?** (e.g., `backend/app/api/v1/`, `frontend/app/wizard/`)
> 4. **Do you have a build request file?** (e.g., a `.md` file with structured requirements)

Proceed once you have at least #1 answered clearly. Items #2-4 improve quality but aren't blockers.

### Request Triage

The skill triages requests into two scenarios that affect scope discovery depth:

- **Scenario A (Explicit)** — User provided most details: goal, output paths, source locations, format. Researchers confirm and fill minor gaps.
- **Scenario B (Vague)** — User provided a goal but few specifics. Researchers do broad exploration to figure out what exists and determine reasonable defaults.

### Multi-Track Detection

Requests with multiple independent deliverables may be split into parallel tracks (1-5). Tracks are independent when they have distinct goals, operate on different source files, produce different outputs, and have no cross-dependencies. Details in the Multi-Track Handling section below.

### Relationship to Other Skills

This skill is invoked directly by users via `/task-builder [request]`, or by other document-producing skills (tech-reference, prd, tdd, operational-guide, repo-cleanup, readme, tech-research) via `Skill(skill: "task-builder", args: "<BUILD-REQUEST-file-path>")` during their Stage A. When invoked by a calling skill, the skill detects the `Source: skill-delegated` header in the BUILD-REQUEST.md file and follows the skill-delegated flow path (see Input section and A.1). When invoked directly by a user, the skill runs the full pipeline including scope discovery and researchers.

---

## Tier Selection

Match the tier to request complexity. **Default to Standard** unless the scope is clearly small (<5 files) or clearly large (20+ files, multiple subsystems).

| Tier | When | Researchers | Web Agents | Purpose |
|------|------|-------------|------------|---------|
| **Quick** | Small scope, <5 relevant files, single concern | 3 | 0 | Fast task file for simple requests |
| **Standard** | Most requests, 5-20 files, moderate complexity | 4-5 | 0-1 | Default — balanced depth and speed |
| **Deep** | Complex scope, 20+ files, multiple subsystems, multi-track | 6-8 | 1-2 | Thorough research for ambitious tasks |

**Tier selection rules:**

- If in doubt, pick Standard
- If the user says "thorough", "comprehensive", or "deep dive" — always Deep
- Only use Quick for genuinely small tasks (<5 files, single concern, no discovery needed)
- If the scope spans multiple subsystems, involves multi-track, or requires significant discovery — always Deep
- Multi-track requests default to Deep (each track still gets its own researcher set)

---

## Output Locations

All persistent artifacts go into the task folder at `.dev/tasks/to-do/TASK-RF-<subject>-YYYYMMDD-HHMMSS/`.

**Variable reference block:**

```text
TASK_ID:     TASK-RF-<subject>-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/
QA:          ${TASK_DIR}qa/
```

**Subject derivation:** `<subject>` is derived at task-folder-creation time from the goal slug of the user's request and normalized to kebab-case (lowercase, hyphen-separated, 1-3 words, ~30 char soft cap). If no clean subject can be derived, fall back to the literal word `general`. Example TASK_ID: `TASK-RF-api-docs-20260408-140000`.

Note: This skill does NOT produce synthesis files, reviews, or final documents. It produces a task file + research artifacts + QA reports. There are no `synthesis/` or `reviews/` subfolders.

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}${TASK_ID}.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Analyst reports (research gate) | `${TASK_DIR}qa/analyst-completeness-report.md`, `analyst-cross-validation-report.md` |
| QA research gate reports | `${TASK_DIR}qa/qa-research-evidence-report.md`, `qa-research-gap-report.md` |
| QA research depth report | `${TASK_DIR}qa/qa-research-depth-report.md` |
| QA task validation reports | `${TASK_DIR}qa/qa-task-validation-b2-report.md`, `qa-task-validation-structure-report.md` |
| QA task validation consolidated | `${TASK_DIR}qa/qa-task-validation-consolidated.md` |
| QA task-research-alignment report | `${TASK_DIR}qa/qa-task-research-alignment-report.md` |
| QA qualitative reports | `${TASK_DIR}qa/qa-qualitative-operational-report.md`, `qa-qualitative-sufficiency-report.md` |
| QA qualitative consolidated | `${TASK_DIR}qa/qa-qualitative-consolidated.md` |

**Multi-track path convention:** For multi-track builds, each track gets its own folder: `TASK-RF-track-T-YYYYMMDD-HHMMSS/` (e.g., `TASK-RF-track-1-20260318-140000/`). Track ID goes BEFORE the timestamp so folders sort by track. Each track folder has its own `research/` and `qa/` subfolders.

**File numbering convention:** All research files use zero-padded sequential numbers: `01-`, `02-`, `03-`, etc. This ensures correct ordering when listing files.

Check for existing task folders matching `TASK-RF-*` in `.dev/tasks/to-do/` before creating new ones — if prior research exists for the same goal, read it first and build on it.

---

## Execution Overview

This skill operates in a single stage (Stage A only). Unlike the canonical document skills which have Stage A (create task file) + Stage B (delegate to `/task` for execution), this skill stops after task file creation. The user reviews the task file and executes it with `/task [path]` when ready.

**Stage A — Scope Discovery, Research, Quality Gate, Task File Creation:**

1. Check for an existing task folder or research directory (A.1)
2. Parse the user's request — triage into Scenario A vs B, determine track count (1-5), select MDTM template per track (A.2)
3. Perform scope discovery — map relevant files/directories, plan researcher assignments from 8 topic types (A.3)
4. Write scope discovery results to a structured research notes file with 7 categories (A.4)
5. Review research sufficiency — mandatory self-review gate (A.5)
6. Triage template selection — Template 01 (generic) vs 02 (complex) per track (A.6)
7. Spawn parallel researchers via Agent tool — 3-8 per track based on tier and scope complexity (A.7)
8. Research quality gate — 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative in parallel via Agent tool (5 agents minimum), with gap-fill cycle if needed (max 3 rounds) (A.8)
9. Optional web research — only if tier allows web agents AND quality gate identified external knowledge gaps (A.8.5)
10. Spawn the `rf-task-builder` agent via Agent tool with structured BUILD_REQUEST (A.9)
11. Task file structural validation — 2 rf-qa agents with focused lenses (B2 self-containment + phase structure/ordering) via Agent tool, serialized fix authorization (A.10)
12. Task file research-alignment validation — 1 rf-analyst agent (task-research-alignment lens) cross-validates the task file against research files (A.10.25)
13. Task file qualitative validation — 2 rf-qa-qualitative agents with focused lenses (operational correctness + QA gate sufficiency) via Agent tool, serialized fix authorization (A.10.5)
14. PRE reflect gate: spawn `/sc:reflect --mode pre` against the built tasklist (advisory-blocking sign-off; A.10.7)
15. Present results — task file path, quality gate summary, recommended batch size, execution command (A.11)

If a task folder already exists for this request (from a previous session), skip to the appropriate step based on artifact state:

- Research files complete but no QA reports → skip to A.8 (quality gate)
- QA reports pass but no task file → skip to A.9 (spawn builder)
- Task file exists but no validation report → skip to A.10 (structural validation)
- Task file + structural validation but no research-alignment report → skip to A.10.25 (research-alignment validation)
- Task file + structural + alignment reports but no qualitative report → skip to A.10.5 (qualitative validation)
- Task file + all validation/alignment/qualitative reports exist → skip to A.11 (present results)

**Skill-delegated flow (alternative path):** When invoked by a calling skill via `Skill(skill: "task-builder", args: "<BUILD-REQUEST-file-path>")` with `Source: skill-delegated` and `SKIP_RESEARCHERS: true` (default):

`A.1 (detect skill-delegated, extract metadata, check artifact state) → skip A.2-A.8.5 (scope discovery, research, quality gate — already done by caller) → A.9 (spawn builder from BUILD-REQUEST.md file) → A.10 (structural QA) → A.10.25 (research-alignment) → A.10.5 (qualitative QA) → A.11 (present results)`

When `SKIP_RESEARCHERS: false` (e.g., research-notes.md missing or caller explicitly sets false):

`A.1 (detect skill-delegated) → skip A.2-A.4 (scope discovery — already done by caller) → A.5 (review research sufficiency) → A.6-A.8.5 (researchers + quality gate) → A.9 (spawn builder) → A.10 → A.10.25 → A.10.5 → A.11`

In both cases, A.1 checks for prior artifacts first and resumes from the appropriate point if a partially-completed build exists in the Task Directory.

---

## Stage A: Task File Creation Pipeline

### A.1: Check for Existing Task Folder

Before creating a new task folder, check if one already exists.

**Branch 1 — Skill-Delegated Build Request Detection:**

When the input is a file path matching `BUILD-REQUEST*.md`:

1. Read the BUILD-REQUEST file and check for `Source: skill-delegated` in the metadata header.
2. If `Source: skill-delegated` is present, extract metadata:
   - `Calling Skill` — which skill invoked us (for logging/diagnostics)
   - `Task Directory` — the pre-created task directory (use this as TASK_DIR — do NOT create a new TASK-RF-* folder)
   - `Research Notes` — path to research-notes.md
   - `Research Notes Status` — whether scope discovery is complete
   - `SKIP_RESEARCHERS` — whether to skip the researcher layer (default: `true` for skill-delegated)
3. Verify research-notes.md exists at the specified path and has `Status: Complete`.
4. **CRITICAL PRECEDENCE — Check existing artifact state FIRST:** After extracting metadata, check the Task Directory for prior artifacts using the SAME resume logic as Branch 2 below (the state-to-resume-point checks). If prior artifacts exist (research files, QA reports, task file, validation reports), resume from the appropriate point regardless of SKIP_RESEARCHERS. This handles session resumption for partially-completed skill-delegated builds.
5. **ONLY IF no prior artifacts exist in the Task Directory:**
   - If `SKIP_RESEARCHERS` is `true` (or absent, defaulting to true for skill-delegated) → skip to A.9 (spawn builder with BUILD-REQUEST.md content)
   - If `SKIP_RESEARCHERS` is `false` → skip to A.5 (review research sufficiency), then proceed through A.6-A.8.5 (researchers + quality gate) before A.9

**Error handling for skill-delegated detection:**

- Missing `Source: skill-delegated` field → treat as user-invoked BUILD_REQUEST file, proceed to A.2 (existing behavior)
- Missing or nonexistent `Task Directory` → log blocker: "Task Directory not found at [path]. Cannot proceed with skill-delegated build." and halt
- Missing research-notes.md at the specified path → log warning: "research-notes.md not found at [path]. Setting SKIP_RESEARCHERS=false to enable full research pipeline." Set SKIP_RESEARCHERS to false and skip to A.3 (scope discovery) instead of A.5, since A.5 (review sufficiency) also requires research-notes.md. A.3 will create the research-notes.md file, then flow through A.4 → A.5 → A.6-A.8.5 → A.9 normally.

**Branch 2 — Standard Resume Detection (user-invoked builds):**

1. Look in `.dev/tasks/to-do/` for any `TASK-RF-*/` folder related to this request
2. If found, check the artifact state to determine the resume point:
   - If `research/` has complete research files but `qa/` has no analyst/QA reports → skip to A.8 (quality gate)
   - If `qa/` has all 5 A.8 report files (`analyst-completeness-report.md`, `analyst-cross-validation-report.md`, `qa-research-evidence-report.md`, `qa-research-gap-report.md`, `qa-research-depth-report.md`) but no task file in `${TASK_DIR}` → skip to A.9 (spawn builder). Resume checks verify file EXISTENCE; the orchestrator re-reads verdicts if needed.
   - If task file exists but no `qa-task-validation-b2-report.md` AND `qa-task-validation-structure-report.md` in `qa/` → skip to A.10 (structural validation)
   - If task file + structural reports exist but no `qa-task-research-alignment-report.md` in `qa/` → skip to A.10.25 (research-alignment validation)
   - If task file + structural + alignment reports exist but no `qa-qualitative-operational-report.md` AND `qa-qualitative-sufficiency-report.md` in `qa/` → skip to A.10.5 (qualitative validation)
   - If task file and all validation/qualitative/alignment reports exist → skip to A.11 (present results)
   - If `research-notes.md` exists with `Status: Complete` → skip to A.5 (review sufficiency)
   - If `research-notes.md` exists with `Status: In Progress` → resume A.3 scope discovery
3. If no matching task folder exists → continue with A.2

### A.2: Parse & Triage

Break the user's request into structured components:

- **GOAL**: What the task file should accomplish when executed
- **WHY**: Why this task is needed (if stated)
- **OUTPUTS**: Specific deliverables, paths, formats (if stated)
- **CONTEXT**: Files, directories, components mentioned (if any)
- **SPEC_PATH**: The driving spec/PRD/TDD path, resolved in priority order (explicit `--spec <path>` -> an `@file` reference in GOAL -> a `SPEC:`/`PRD:`/`TDD:` field in BUILD_REQUEST -> none); written to the generated tasklist frontmatter as `spec_path:`, threaded into the A.10.7 PRE call's `--spec` (the O1 POST wrapper shell-out does not take `--spec`; the spec is consumed by the PRE gate only)

**Triage into Scenario A or B:**

**Scenario A — Explicit request:** User provided most of: goal, output paths, source locations, format.
Example: "Build a task to create API documentation for all handlers in `backend/app/api/v1/`, output to `docs/api/` as markdown"
→ Researchers confirm details and fill minor gaps. Lighter exploration.

**Scenario B — Vague request:** User provided a goal but few specifics.
Example: "Build a task to document the handlers"
→ Researchers do broad exploration to figure out what exists and determine reasonable defaults.

**Do NOT interrogate the user with a list of questions.** Proceed with what you have and let scope discovery figure out the rest from the codebase. Only ask the user if there's a genuine ambiguity about **intent** that can't be inferred.

**Determine track count:**

Analyze whether the request contains **independent work streams** that can be executed in parallel.

Independent means ALL of these are true:

- Each track has its own distinct goal (a subset of the overall request)
- Each track operates on different source files or concerns
- Each track produces different output files
- No track depends on another track's outputs

**SPLIT into multiple tracks when you see:**

- Multiple unrelated deliverables: "Create docs for handlers AND add tests for services"
- Distinct output areas: different output directories, different file types
- Explicit enumeration of independent items: "do these three things: A, B, C" (where A, B, C don't depend on each other)

**DO NOT SPLIT (keep as single track) when:**

- Work items build on each other sequentially
- All items contribute to a single cohesive output
- Items share source context that must be understood holistically
- You're unsure whether items are truly independent

**DEFAULT: Single track.** Only split when independence is clear. **MAXIMUM: 5 tracks.**

**Select MDTM template per track:**

| Signal in the Request | Template |
|-----------------------|----------|
| "Create these files" (known inputs, known outputs) | 01 |
| "Build X with tests" (need to discover, build, then test) | 02 |
| "Document all handlers" (need discovery scan first) | 02 |
| "Create a config file from this spec" (direct transformation) | 01 |
| "Refactor X and verify nothing breaks" (build + test + conditional fix) | 02 |
| When uncertain | **02 (safer)** |

### A.3: Perform Scope Discovery

Use Glob, Grep, and codebase-retrieval to map the problem space. This must happen BEFORE spawning researchers so each researcher gets a focused assignment from the scope map.

**Adjust depth by scenario:**

- **Scenario A**: Focused discovery — verify files/directories exist, scan for related code, identify gaps.
- **Scenario B**: Broad discovery — scan the full codebase for anything related, map all relevant subsystems, count files.

**Discovery steps:**

1. **Map relevant files and directories** — enumerate:
   - Primary source directories and key subdirectories
   - Number of files and approximate complexity
   - Major subsystems (group files by function)
   - External integration points
   - Existing documentation or templates

2. **Plan researcher assignments** — select 3-8 topic types per track from:

| Topic Type | What It Investigates | When to Include |
|------------|---------------------|-----------------|
| **File Inventory** | All source files, their exports, sizes, dependencies | Always (every track needs this) |
| **Patterns & Conventions** | Naming, code style, architecture patterns, templates used | Always (builder needs conventions to follow) |
| **Integration Points** | APIs, imports, cross-module dependencies, config surfaces | When the goal touches multiple subsystems |
| **Doc Cross-Validator** | Existing docs accuracy vs actual code (staleness check) | When relevant docs exist for the area |
| **Solution Research** | External best practices, libraries, architecture patterns | When building something new or choosing approaches |
| **Template & Examples** | MDTM templates, existing task examples, similar prior work | Always (builder needs template context) |
| **Data Flow Tracer** | How data moves through the relevant subsystem end-to-end | When understanding runtime behavior matters |
| **Test & Verification** | Existing tests, test patterns, verification approaches | When the task involves testing or has quality gates |

**Assignment planning rules:**

- **Minimum 3 researchers per track**: File Inventory + Patterns & Conventions + Template & Examples
- **Scale up based on scope map complexity**: high complexity = 6-8 researchers; medium = 4-5; low = 3
- **Each researcher gets specific directories/files** from the scope map — no overlapping file assignments
- **Every researcher is told what OTHER researchers cover** — prevents duplication

**Example assignment for "Document all 14 API handlers":**

```text
Researcher 1 (File Inventory): Scan backend/app/api/v1/ — catalog all handler files, classes, methods, line counts
Researcher 2 (Patterns & Conventions): Read 3-4 handlers in detail — extract naming, error handling, response patterns
Researcher 3 (Integration Points): Trace handler dependencies — services, models, schemas they import/use
Researcher 4 (Doc Cross-Validator): Read existing docs/ for handler documentation — cross-validate against actual handler code
Researcher 5 (Template & Examples): Read MDTM templates + check .dev/tasks/to-do/ for prior task folder examples
```

**Example assignment for "Build a new feature with tests":**

```text
Researcher 1 (File Inventory): Scan directories where feature will live — catalog existing files, identify insertion points
Researcher 2 (Patterns & Conventions): Study similar features already implemented — extract patterns to follow
Researcher 3 (Integration Points): Map how the new feature connects to existing services, APIs, database
Researcher 4 (Solution Research): WebSearch for best practices, library options, architecture patterns
Researcher 5 (Template & Examples): Read MDTM templates + existing task files for similar work
Researcher 6 (Test & Verification): Study existing test patterns, fixtures, mocking approaches
Researcher 7 (Data Flow Tracer): Trace how data flows through related subsystems
```

3. **Produce per-track scope map:**

```text
TRACK [T] SCOPE MAP:
  Relevant directories: [list]
  Key files found: [count and top examples]
  Patterns/classes identified: [list]
  Existing docs/templates: [list]
  Estimated complexity: [low/medium/high]
```

Compute `<subject>` from the goal slug of the user's request using the rules in the Subject Derivation section. If no clean subject is derivable, use `general`. Create the task folder: `.dev/tasks/to-do/TASK-RF-<subject>-YYYYMMDD-HHMMSS/` with subfolders `research/` and `qa/`. For multi-track: `.dev/tasks/to-do/TASK-RF-track-T-YYYYMMDD-HHMMSS/` per track.

### A.4: Write Research Notes File (MANDATORY)

Write the scope discovery results to a structured research notes file at `${TASK_DIR}research-notes.md`. This file is what the builder reads — NOT inline content in the BUILD_REQUEST.

The file MUST be organized into these 7 categories (include all, mark as "N/A" if empty):

```markdown
# Research Notes: [GOAL]

**Date:** [today]
**Scenario:** [A or B]
**Depth Tier:** [Quick / Standard / Deep]
**Track Count:** [1-5]

---

## EXISTING_FILES
[Key source files, directories, and stubs found during scope discovery. Per-file detail: path, purpose, key exports, approximate line count. Group by directory or subsystem.]

## PATTERNS_AND_CONVENTIONS
[Naming patterns, architecture patterns, design decisions observed. Cite specific files as evidence.]

## GAPS_AND_QUESTIONS
[Unknowns, ambiguities requiring investigation. Specific gaps the researchers need to fill. Areas where the codebase context is insufficient.]

## RECOMMENDED_OUTPUTS
[Research files to create, their topics and output paths. Each researcher assignment: topic type, scope, output file path.]

## SUGGESTED_PHASES
[How to structure the researchers. Per-researcher assignment detail:
- Researcher number, topic type, topic name
- Specific directories/files to investigate
- Output file path
- What other researchers cover (prevents duplication)]

## TEMPLATE_NOTES
[MDTM template selection reasoning (01 vs 02 per track), tier selection reasoning (Quick/Standard/Deep), notes on which MDTM features the generated task file should use.]

## AMBIGUITIES_FOR_USER
[Genuine ambiguities about user intent that cannot be resolved from the codebase. If none, write "None — intent is clear from the request and codebase context."]
```

For multi-track builds: write per-track research notes (one file per track in the track's `research/` folder) or clearly delineated track sections within a single file.

### A.5: Review Research Sufficiency (MANDATORY GATE)

**You MUST review the research notes before spawning researchers.** This is a quality gate — do NOT skip it.

Read `${TASK_DIR}research-notes.md` and evaluate:

1. Is the task scope clearly bounded?
2. Are all major subsystems and source areas identified?
3. Are integration points mapped (if the task touches multiple subsystems)?
4. Are researcher assignments concrete enough? (Each needs: topic type, specific scope, output path)
5. Is the template selection reasonable (01 vs 02)?
6. Are existing docs/templates inventoried?
7. Are genuine ambiguities flagged in AMBIGUITIES_FOR_USER (not silently assumed)?

**If sufficient** → proceed to A.6 (template triage).

**If insufficient** → either:

- Do additional scope discovery yourself and update the research notes file, OR
- Spawn a general-purpose research subagent with specific feedback about what's missing, then re-review

**Maximum 2 gap-fill rounds.** After 2 rounds, proceed with what's available and note remaining gaps in the AMBIGUITIES_FOR_USER section.

Do NOT proceed to the researchers with incomplete research notes. The researchers work from the scope map you provide — incomplete maps produce incomplete research.

### A.6: Template Triage

Determine which MDTM template the task builder should use for each track:

**Use Template 02 (Complex Task) when the work involves:**

- Discovery before building (investigating unknown areas)
- Parallel subagent spawning
- Multiple phases with different activities (research, build, test, review)
- Conditional flows based on findings
- Quality gates or verification steps

**Use Template 01 (Generic Task) when the work involves:**

- Simple, sequential file creation
- Straightforward execution with no discovery
- Single-pass operations with known inputs and outputs

**For most task-builder requests, the answer is Template 02** — the generated task file will typically involve discovery, building, and verification phases. Only use Template 01 for trivial tasks with known inputs and outputs.

### A.7: Spawn Researchers

Spawn parallel researcher agents via the Agent tool. Each researcher gets a focused topic from the scope map and writes findings to its own file in `${TASK_DIR}research/`.

**Spawning pattern:**

- Use Agent tool with `subagent_type: "general-purpose"`, `mode: "bypassPermissions"`
- Each researcher returns its research file path as output
- ALL researchers for a track spawned in the SAME message for parallel execution
- Multi-track: ALL researchers across ALL tracks in one message

**Researcher Prompt Template:**

Each researcher receives the following prompt adapted with track-specific and topic-specific context:

```text
Agent:
  subagent_type: "general-purpose"
  mode: "bypassPermissions"
  prompt: |
    You are a research agent for the task-builder skill.
    [If multi-track: You are researching TRACK T of [N] parallel tracks.]

    YOUR SPECIFIC RESEARCH TOPIC: [TOPIC_TYPE]
    YOUR SCOPE: [specific directories, files, or areas to investigate from scope map]
    YOUR FOCUS: [what specifically to investigate and document within your scope]

    TRACK GOAL: [goal for this track]
    USER PROVIDED: [list specifics the user gave]
    USER DID NOT SPECIFY: [list what's missing — you figure it out from the codebase]

    OTHER RESEARCHERS COVERING:
    [List what other parallel researchers are covering so this agent knows its boundaries.]
    - researcher-[other-topic]: [their scope and focus]
    Do NOT duplicate their work. Focus exclusively on YOUR topic.

    YOUR RESEARCH MUST BE THOROUGH AND GRANULAR:
    The task builder needs enough detail to create individual checklist items for EVERY file,
    component, or iteration involved. Per MDTM template rules A3 (Complete Granular Breakdown)
    and A4 (Iterative Process Structure), the builder must create individual items for each
    file/component — NOT batch items like "document all 14 handlers." Your research must
    provide the per-file detail that makes this possible.

    [TOPIC-SPECIFIC INSTRUCTIONS — include the block matching this researcher's topic type]

    INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
    1. FIRST ACTION: Create your output file at ${TASK_DIR}research/[NN]-[topic-slug].md
       with this header:
       ```markdown
       # Research: [Your Topic]
       **Topic type:** [type]
       **Scope:** [your assigned scope]
       **Status:** In Progress
       **Date:** [today]
       ---
       ```
    2. As you investigate each file/component, IMMEDIATELY append findings using Edit.
       Do NOT accumulate in context and one-shot at the end.
    3. When finished, update Status to "Complete" and append a summary section.

    EVIDENCE-BASED CLAIMS ONLY:
    Every finding must cite actual file paths, line numbers, function names, class names.
    No assumptions, no inferences, no guessing. If you can't verify it, mark "Unverified."

    ESCALATION: You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate,
    or TaskList. These tools do not exist in your context.

    STEPS:
    1. Create your output file FIRST (incremental writing protocol)
    2. Explore the codebase within your assigned scope
    3. Write findings incrementally to your output file
    4. When complete, update Status to "Complete" and append summary
    5. Verify file exists by reading it back
    6. Return your research file path and a brief findings summary as your final output

[Spawn ALL researchers in the SAME message for parallel execution]
```

**Topic-Specific Instruction Blocks:**

Include the matching block in each researcher's prompt based on their assigned topic type:

**File Inventory:**

```text
For every relevant file in your assigned directories:
- Full relative path from project root
- File purpose (1 sentence)
- Key exports: classes, functions, constants with signatures
- Line count and complexity estimate
- Dependencies (imports from other project files)
Organize as a structured inventory table or list. The builder will create one checklist
item per file from this inventory.
```

**Patterns & Conventions:**

```text
Read 3-5 representative files in the relevant area and extract:
- Naming conventions (files, classes, functions, variables)
- Code structure patterns (class hierarchy, module organization)
- Error handling approach
- Documentation/comment style
- Configuration patterns
- Testing patterns (if visible in source)
Document with specific examples from actual code (file:line references).
```

**Integration Points:**

```text
For the subsystems involved in this track's goal:
- Map all imports/dependencies between modules
- Identify API contracts (function signatures, request/response schemas)
- Document configuration surfaces (env vars, config files, feature flags)
- Note cross-service communication patterns
- Identify extension points where new functionality could hook in
```

**Doc Cross-Validator:**

```text
CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state, NOT necessarily current state.
For EVERY doc you read that makes architectural claims:
1. Services/components described: Verify the directory/entry point actually exists (use Glob)
2. Pipelines/call chains described: Trace at least first and last hop in actual source
3. File paths mentioned: Spot-check that referenced files exist
4. API endpoints described: Verify endpoint exists in actual router/app code

Mark EVERY doc-sourced claim with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** — code shows different implementation (describe what code shows)
- **[UNVERIFIED]** — could not find corresponding code; may be stale or planned

List all stale documentation found. This prevents the builder from creating task items
based on architecture that no longer exists.
```

**Solution Research:**

```text
Use WebSearch to investigate:
1. Problem domain patterns — established approaches, expert recommendations
2. Tools & libraries — what's commonly used, open-source options, feature comparison
3. Architecture patterns — how others solve this type of problem
4. Project fit — alignment with project constraints (check CLAUDE.md for tech stack)

For each finding: source URL, key information, relevance rating (HIGH/MEDIUM/LOW),
how it relates to our codebase. Codebase is source of truth — external research
supplements but never overrides verified code findings.
```

**Template & Examples:**

```text
1. Read the MDTM template specified for this track:
   - If template 02: .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If template 01: .claude/templates/workflow/01_mdtm_template_generic_task.md
2. Read PART 1 completely — note all rules, especially A3 (Complete Granular Breakdown)
   and B2 (self-contained item pattern)
3. Check .dev/tasks/to-do/ for existing task folder examples — note effective patterns
4. Document: required sections, item format, common pitfalls, template-specific features
   (e.g., L1-L6 handoff patterns for template 02)
```

**Data Flow Tracer:**

```text
Trace how data enters, transforms, and exits the relevant subsystem:
- Entry points (API endpoints, event handlers, scheduled tasks)
- Data transformations (what functions process the data, in what order)
- Storage/persistence (database writes, file outputs, cache updates)
- Exit points (API responses, events emitted, files written)
Document with actual function signatures and file:line references.
```

**Test & Verification:**

```text
Investigate testing infrastructure for the relevant area:
- Existing test files and what they cover
- Test framework and patterns used (fixtures, mocking, factories)
- Coverage gaps — what's tested vs what isn't
- Verification approaches for the type of output this track produces
- CI/CD test integration (how tests are run in pipeline)
```

**Orchestrator collection:** After all Agent calls return, the orchestrator has all research file paths from agent outputs. List research files in `${TASK_DIR}research/` to verify completeness. No message-based coordination needed.

### A.8: Research Quality Gate

Spawn rf-analyst, rf-qa, and rf-qa-qualitative in parallel to independently verify research completeness before allowing task file creation. Minimum agents per I22 qa_intensity (lite: 2, standard: 3, full: 5): 2 rf-analyst (completeness lens + cross-validation lens), 2 rf-qa (evidence-quality lens + gap-detection lens), 1 rf-qa-qualitative (research-depth lens).

**Spawn analyst + QA + qualitative in parallel** — Agent calls in one message (5 at full intensity, 3 at standard, 2 at lite per I22):

```text
Agent 1 (rf-analyst — completeness lens):
  subagent_type: "rf-analyst"
  mode: "bypassPermissions"
  description: "Research completeness verification — completeness lens"
  prompt: |
    ANALYSIS_TYPE: completeness-verification
    LENS: completeness
    SCOPE: Research files for task-builder track [T]

    RESEARCH DIR: ${TASK_DIR}research/
    TRACK GOAL: [goal for this track]
    ASSIGNED FILES: [list all .md files in research/]

    YOUR LENS FOCUS: Verify that every area from the scope map has
    corresponding research coverage. You check BREADTH, not depth.

    Read each research file and verify:
    1. Source files identified with paths and exports?
    2. Output paths and formats clear or reasonably inferred?
    3. Logical breakdown of phases/steps present?
    4. Patterns and conventions documented with examples?
    5. MDTM template notes present with rule references?
    6. Granularity sufficient for per-file/per-component checklist items?
    7. Documentation cross-validation: doc-sourced claims tagged [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]?
    8. If new implementation: solution research evaluated approaches?
    9. Unresolved ambiguities documented (not silently skipped)?

    For each criterion: PASS (with evidence) or FAIL (with specific gaps).

    OUTPUT FILE: ${TASK_DIR}qa/analyst-completeness-report.md
    Write the file IMMEDIATELY with a header, then append findings incrementally.
    Conclude with: VERDICT: PASS or FAIL, and a structured gap list if FAIL.

    ESCALATION: You have NO team context. Do NOT use SendMessage.
    Return your verdict and report file path as your final output.

Agent 2 (rf-analyst — cross-validation lens):
  subagent_type: "rf-analyst"
  mode: "bypassPermissions"
  description: "Research cross-validation — cross-validation lens"
  prompt: |
    ANALYSIS_TYPE: completeness-verification
    LENS: cross-validation
    SCOPE: Research files for task-builder track [T]

    RESEARCH DIR: ${TASK_DIR}research/
    TRACK GOAL: [goal for this track]
    ASSIGNED FILES: [list all .md files in research/]

    YOUR LENS FOCUS: Cross-validate claims BETWEEN research files.
    Where two researchers cover overlapping areas, verify their findings
    are consistent. Flag contradictions, conflicting counts, or divergent
    descriptions of the same component.

    Checklist:
    1. Cross-file consistency — do findings about the same files/APIs agree?
    2. No contradictory claims between research files?
    3. Shared dependencies documented consistently?
    4. Integration point descriptions match across researchers?

    OUTPUT FILE: ${TASK_DIR}qa/analyst-cross-validation-report.md
    Write the file IMMEDIATELY with a header, then append findings incrementally.
    Conclude with: VERDICT: PASS or FAIL, and a structured gap list if FAIL.

    ESCALATION: You have NO team context. Do NOT use SendMessage.
    Return your verdict and report file path as your final output.

Agent 3 (rf-qa — evidence-quality lens):
  subagent_type: "rf-qa"
  mode: "bypassPermissions"
  description: "Research evidence quality gate — evidence-quality lens"
  prompt: |
    QA_MODE: research-gate
    LENS: evidence-quality
    fix_authorization: false

    **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

    RESEARCH DIR: ${TASK_DIR}research/
    TRACK GOAL: [goal for this track]
    ASSIGNED FILES: [list all .md files in research/]

    YOUR LENS FOCUS: Verify EVIDENCE QUALITY in each research file.
    Every claim must cite file paths, line numbers, function names.

    Zero-trust verification:
    1. Are claims evidence-based (file paths, line numbers, function names)?
    2. Any unsupported assertions or assumptions stated as facts?
    3. Are [CODE-CONTRADICTED] or [UNVERIFIED] claims properly flagged?
    4. Spot-check 20% of cited file paths — do they actually exist?

    OUTPUT FILE: ${TASK_DIR}qa/qa-research-evidence-report.md
    Write the file IMMEDIATELY with a header, then append findings incrementally.
    Conclude with: VERDICT: PASS or FAIL, and severity-rated issues if FAIL.
    Severity ratings: CRITICAL (blocks builder), IMPORTANT (reduces quality), MINOR (nice-to-fix).

    ESCALATION: You have NO team context. Do NOT use SendMessage.
    Return your verdict and report file path as your final output.

Agent 4 (rf-qa — gap-detection lens):
  subagent_type: "rf-qa"
  mode: "bypassPermissions"
  description: "Research gap detection gate — gap-detection lens"
  prompt: |
    QA_MODE: research-gate
    LENS: gap-detection
    fix_authorization: false

    **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

    RESEARCH DIR: ${TASK_DIR}research/
    TRACK GOAL: [goal for this track]
    ASSIGNED FILES: [list all .md files in research/]

    YOUR LENS FOCUS: Find GAPS — areas the researchers missed entirely.
    Read the scope map/research notes, then check whether every area
    has corresponding research coverage.

    Gap-detection checklist:
    1. Coverage gaps — are there obvious areas the researchers missed?
    2. Are findings actionable for a task builder (not too vague, not too abstract)?
    3. Missing integration points between subsystems?
    4. Missing test/verification coverage for areas the task will modify?

    OUTPUT FILE: ${TASK_DIR}qa/qa-research-gap-report.md
    Write the file IMMEDIATELY with a header, then append findings incrementally.
    Conclude with: VERDICT: PASS or FAIL, and severity-rated issues if FAIL.
    Severity ratings: CRITICAL (blocks builder), IMPORTANT (reduces quality), MINOR (nice-to-fix).

    ESCALATION: You have NO team context. Do NOT use SendMessage.
    Return your verdict and report file path as your final output.

Agent 5 (rf-qa-qualitative — research-depth lens):
  subagent_type: "rf-qa-qualitative"
  mode: "bypassPermissions"
  description: "Research depth assessment — research-depth lens"
  prompt: |
    QA_PHASE: research-depth
    LENS: research-depth
    fix_authorization: false

    **ADVERSARIAL STANCE:** Assume the research is superficial until proven otherwise. Your job is to determine whether findings are genuinely deep or merely surface-level. Researchers that list file names without understanding behavior are shallow.

    RESEARCH DIR: ${TASK_DIR}research/
    TRACK GOAL: [goal for this track]
    ASSIGNED FILES: [list all .md files in research/]

    YOUR LENS FOCUS: Evaluate whether research is DEEP ENOUGH to produce
    a high-quality task file. Surface-level file inventories without
    behavioral understanding produce vague task items.

    Depth checklist:
    1. Do research files explain HOW components work, not just WHAT they are?
    2. Are data flows traced end-to-end (not just entry points listed)?
    3. Are edge cases, error handling, and failure modes documented?
    4. Are patterns specific enough to replicate (not just "follows MVC")?
    5. Could a task builder create per-file checklist items from this research
       without needing to re-read any source files?

    OUTPUT FILE: ${TASK_DIR}qa/qa-research-depth-report.md
    Write the file IMMEDIATELY with a header, then append findings incrementally.
    Conclude with: VERDICT: PASS or FAIL, and severity-rated issues if FAIL.

    ESCALATION: You have NO team context. Do NOT use SendMessage.
    Return your verdict and report file path as your final output.
```

**Partitioning:** When >6 research files per track, partition across agent types: spawn 4 rf-analyst instances (2 lenses x 2 partitions) + 4 rf-qa instances (2 lenses x 2 partitions) + 2 rf-qa-qualitative instances (1 lens x 2 partitions) = 10 agents total, each with assigned_files subsets. Merge reports per lens after all return.

**Gate evaluation:** Read ALL 5 agent reports (2 analyst + 2 QA + 1 qualitative). Gate PASSES when ALL verdicts are PASS with ALL findings resolved regardless of severity. A single FAIL from any agent fails the gate.

**Gap-fill cycle:** If the gate fails:

1. Compile all CRITICAL, IMPORTANT, and MINOR issues from analyst + QA reports into a structured gap list
2. Spawn targeted gap-fill researcher(s) via Agent tool (`subagent_type: "general-purpose"`) with specific gaps to fill
3. After gap-fill, re-run analyst + QA on the NEW research files only
4. **Maximum 3 gap-fill rounds** (aligned with canonical skills and rf-qa agent definition)
5. After 3 rounds, proceed with remaining gaps as Open Questions in the task file

**Cross-track validation (multi-track only):** After gate evaluation, cross-validate that no two tracks have overlapping scope that would produce conflicting task files.

**DNSP Synthetic Finding Protocol (PR-03 - paradigm-neutral, the BASE proposal of this release):**

When the orchestrator spawns rf-analyst / rf-qa / rf-qa-qualitative with partition `assigned_files` slices, a single partition agent that exhausts its escalation ladder (WebSearch -> /rf:opinion -> team-lead, per rf-task-researcher.md and the agent definitions) AND fails the existing single retry (Bucket A SKILL.md "retry once before reporting error" baseline) MUST NOT silently weaken the gate or abort the entire pipeline. Instead, the orchestrator synthesises a **HIGH-severity finding** with this emission contract:

- `severity: HIGH`
- `source: "synthetic-dnsp"`
- `affected_range`: the failed agent's `assigned_files` slice (verbatim)
- `evidence`: path to the failed agent's spawn log (or a `<!-- evidence-absence: spawn-log-unavailable -->` stub citing the absence)
- `recommendation`: "Manual review required — partition agent failed twice"
- `dedup_key`: 2-tuple `(assigned_files_range, escalation_ladder_exhaust_point)`, emitted as YAML list `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`; `escalation_ladder_exhaust_point` MUST be drawn from the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` (free-form descriptions are rejected by the emitter)
- `found_n_times`: int, default `1`; increments by `1` on each within-cycle dedup-key collapse (see the **Dedup key** paragraph below for the cross-cycle composition rule with PR-02 / INV-012)

**Fixed-field emitter rejection (R-113 + R-114).** The `severity` and `source` fields are non-overridable fixed-value invariants of DM-003. The emitter MUST reject any synthetic-dnsp emission whose `severity` field is not the literal `HIGH` (case-sensitive) OR whose `source` field is not the literal `synthetic-dnsp` (case-sensitive). Such rejections surface as `DM-003-fixed-field-invariant-violation` errors and MUST NOT be silently coerced. Rationale: the `HIGH` pin prevents merge-time severity downgrade (without it the synthetic could be quietly demoted past the gate's any-gap-regardless-of-severity = FAIL rule); the literal `synthetic-dnsp` sentinel is what allows downstream operators to filter, audit, and report on synthetic emissions distinct from real findings.

**Dynamic-field emitter rejection (R-115 + R-116).** The `affected_range` and `evidence` fields are dynamic-value invariants of DM-003 bound by content rules rather than fixed strings. The `affected_range` field MUST be the partition's spawn-prompt `assigned_files` (or `assigned_phases` for rf-qa-qualitative) slice copied verbatim: byte-for-byte, with no normalization, canonicalization, ordering changes, or whitespace edits. The `evidence` field MUST NEVER be blank: the canonical wire value is the spawn-log path `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`; when that log is unavailable the emitter MUST substitute the stub `<!-- evidence-absence: no-spawn-log: <reason> -->` explicitly citing the absence (e.g., `no-spawn-log: tmpfs-cleared`, `no-spawn-log: orchestrator-write-failed`). The emitter MUST reject any synthetic-dnsp emission whose `affected_range` does not byte-match the spawn-prompt assigned slice OR whose `evidence` field is empty / whitespace-only / missing the absence stub when the path is unresolvable. Such rejections surface as `DM-003-dynamic-field-invariant-violation` errors and MUST NOT be silently coerced.

**Fixed-value + tuple-shape + counter emitter rejection (R-117 + R-118 + R-119).** The `recommendation`, `dedup_key`, and `found_n_times` fields complete the DM-003 emitter rejection contract. The `recommendation` field is a fixed-value invariant pinned to the literal byte-exact string `Manual review required — partition agent failed twice` (case-sensitive; no leading/trailing whitespace; no suffix); the emitter MUST reject any synthetic-dnsp emission carrying any other value, including same-prefix-with-trailing-suffix variants (the wrapper's earlier `on this range` extension was a pre-T06.01 drift and is removed by T06.05). The `dedup_key` field MUST be emitted as a 2-element YAML list of the shape `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`; the emitter MUST reject any synthetic emission whose `dedup_key` is not a 2-element list OR whose second element falls outside the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`. The `found_n_times` field defaults to the integer `1` on first emission and increments by exactly `1` on each within-cycle dedup-key collapse; the emitter MUST reject any synthetic emission whose `found_n_times` is not a positive integer >=1 OR whose first emission carries a value other than `1`. Such rejections surface as `DM-003-recommendation-invariant-violation`, `DM-003-dedup-key-shape-violation`, and `DM-003-found-n-times-invariant-violation` errors respectively and MUST NOT be silently coerced.

**API-003-M6 emission wire-shape (R-120 + R-121).** The synthetic-dnsp finding MUST be emitted by the orchestrator as a structured Markdown block written into the partition agent's **normal output stream**, the same stdout/report channel that real findings use, with no separate signalling channel, sideband API, structured-result frame, or out-of-band metadata transport. The block is consumed downstream by the merge step at SKILL.md §A.8 (Research Quality Gate merge) and §A.10 (Task File Validation merge); the merge step picks up the synthetic block alongside real findings and treats it as a real finding for the existing "any gap regardless of severity = FAIL" gating rule. The `escalation_ladder_exhaust_point` value (the second element of the `dedup_key` 2-tuple at R-118) MUST be drawn from the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`; the emitter MUST reject any synthetic-dnsp emission whose `escalation_ladder_exhaust_point` falls outside this vocabulary OR whose value is a free-form description, paraphrase, or natural-language summary of the exhaust point (e.g., `"second retry"`, `"gap-fill round 2"`, `"after WebSearch exhaustion"`, `"escalation-ladder rung 3"` - all rejected). Such rejections surface as `API-003-exhaust-point-vocabulary-violation` errors and MUST NOT be silently coerced.

Then the orchestrator **merges with the remaining N-1 partition agents' findings** rather than aborting. This preserves the parallel-research invariant (N-1 partitions still complete) and the zero-trust QA invariant (the gap is surfaced HIGH-severity, never silently passed).

**All-agents-fail guard.** If zero partition agents succeeded, the orchestrator escalates normally per the existing retry-then-Open-Questions flow: DNSP does NOT fire (a HIGH synthetic for every partition is informationally equivalent to escalation and adds noise).

**All-agents-fail guard precedence (R-122).** The synthetic-dnsp emitter MUST gate on the partition-cohort success count BEFORE any per-partition emission attempt, routing the cohort outcome down exactly one of three mutually-exclusive paths. **Path A (zero-partitions-succeeded: existing `rf-team-lead's Fix Cycles rule` fix-cycle escalation; NO synthetic emits)** fires when the success count is `0`. **Path B (>=1-success AND >=1-exhaust: synthetic-dnsp emits ALONGSIDE real findings)** fires when at least one partition succeeded AND at least one partition exhausted its escalation ladder; the orchestrator MUST emit one synthetic-dnsp block per exhausted partition alongside the real findings from the successful partitions (strictly additive, never replaces real findings). **Path C (all-partitions-succeeded: no synthetic; normal merge)** fires when every partition succeeded. The three paths are mutually exclusive (a single partition-cohort outcome MUST traverse exactly one path; the guard MUST reject any cohort outcome that satisfies more than one path's precondition or none -- e.g., a cohort with zero successes AND zero exhausts is a contract violation because every partition must terminate in success-or-exhaust). Guard-precedence violations surface as `R-122-guard-precedence-violation` errors. At the A.8 / A.10 merge step, when zero partitions succeeded the merge step is skipped and `rf-team-lead's Fix Cycles rule` activates instead (Path A). The `rf-team-lead's Fix Cycles rule` line MUST be byte-stable across the M6 landing (COMP-006-M6 preservation gate; sha256 frozen at `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`); the Path A activation MUST NOT replace, short-circuit, or modify the existing fix-cycle escalation, only route control to it.

**Within-cycle + cross-cycle dedup composition (INV-012, R-123 + R-124).** The synthetic-dnsp emitter MUST apply two distinct dedup-collapse rules at orthogonal scopes. **Within-cycle collapse (R-123).** Two synthetic-dnsp findings emitted within the SAME retry cycle for the SAME `(assigned_files_range, escalation_ladder_exhaust_point)` 2-tuple MUST collapse to a single record with `found_n_times` incremented by exactly `1` from its current value; the emitter MUST NOT emit two cardinality-2 records and MUST NOT skip the increment. **Cross-cycle composition (R-124, INV-012 non-regression).** A synthetic-dnsp finding with an identical `dedup_key` re-emitted on cycle `n+1` AFTER appearing on cycle `n` is a DEDUP case, NOT a regression: it contributes `1` (not `2`) to `|F_{n+1}|`. The cross-cycle collapse runs BEFORE the PR-02 monotonicity comparison at Step 2 of the 4-step ordering rule. The cross-cycle synthetic-dnsp persistence MUST NOT trip Step 1 (regression detection) because `dedup_key ∈ FAIL_n` implies `dedup_key ∉ PASS_n`. Violations surface as `INV-012-within-cycle-collapse-violation` and `INV-012-cross-cycle-composition-violation` errors respectively. NOTE: the sha256 subsection pin from IC's version is OMITTED as a bridge-stage item; the behavioral contract is adopted.

**INV-021 N-1 cohort concurrency + R-126 HIGH severity non-overridable across merge step (R-125 + R-126).** The synthetic-dnsp emitter MUST preserve two cohort-level invariants spanning the partition-agent execution lattice and the merge-step output stream. **INV-021 N-1 cohort concurrency (R-125).** When one partition's escalation ladder exhausts, the orchestrator MUST allow the remaining N-1 sibling partitions to continue executing concurrently to their own success-or-exhaust terminal state BEFORE the exhausted partition's synthetic-dnsp emission is composed AND BEFORE the merge step at SKILL.md §A.8 / §A.10 runs (explicit pick-up wiring lands at T06.11 / R-127 + R-128). The exhausted partition's synthesis MUST NOT block, pause, serialize, or reduce the parallelism of the sibling cohort; spawn-log timestamps MUST evidence the N-1 partitions completing concurrently with (overlapping in wall-clock time with) the exhausted partition's synthesis step. This is the per-cohort instantiation of the NFR-CONV.10 parallel-research invariant (the M6-scoped governance entry recorded at MIG-006 / T06.17). **R-126 HIGH severity non-overridable across merge step + real findings preserved alongside synthetic.** The synthetic-dnsp `severity: HIGH` value MUST be non-overridable at every downstream layer: the per-emission `DM-003-fixed-field-invariant-violation` gate from T06.03 enforces non-override at the emission boundary, and T06.10 extends the invariant transitively across the cohort-level merge step at SKILL.md §A.8 / §A.10 (no merge-time normalization, severity-downgrade transform, severity-coalesce rule, or operator-overridable severity flag is permitted to lower the synthetic-dnsp severity below HIGH). The synthetic-dnsp block MUST be merged ALONGSIDE the real findings from the successful partitions (Path B from T06.08), never IN PLACE OF them: the cohort's real-finding count post-merge MUST equal the cohort's real-finding count pre-merge plus the synthetic count (strictly additive — not replacement, coalesce, or filter); any merge logic that drops real findings to make room for synthetic findings, that coalesces real findings into synthetic ones, or that filters real findings on the basis of severity-bucket collisions with synthetic findings is a contract violation. Violations of the N-1 concurrency invariant (e.g., sibling cohort paused awaiting exhausted-partition synthesis; spawn-log timestamps show serialization of the N-1 partitions behind the exhausted partition's synthesis; the parallel-research invariant NFR-CONV.10 is degraded for the exhausted-partition case) surface as `INV-021-cohort-serialization-violation` errors. Violations of the real-findings-preservation invariant (e.g., a real finding is dropped during the merge step; a real finding is coalesced into a synthetic finding; the cohort's real-finding count post-merge is strictly less than the real-finding count pre-merge; merge logic replaces a real finding with a synthetic one when both share a severity bucket) surface as `R-126-real-findings-replacement-violation` errors. Violations of the merge-step HIGH-severity non-overridable invariant (e.g., merge-time severity-downgrade transform reduces synthetic-dnsp severity below HIGH; merge-time severity-coalesce rule overrides synthetic-dnsp severity from HIGH to another bucket; an operator override flag is honored to lower synthetic-dnsp severity) surface as `R-126-severity-override-violation` errors (distinct from `DM-003-fixed-field-invariant-violation` from T06.03 — the DM-003 symbol scopes per-emission boundary failures, the R-126 symbol scopes merge-step / cohort-layer override failures across the emission lifecycle; both layers are needed because the wire format is preserved post-emission but merge logic could still apply transforms). All three new symbols are distinct from `INV-012-within-cycle-collapse-violation` + `INV-012-cross-cycle-composition-violation` (T06.09 — cross-emission compositional layer), `R-122-guard-precedence-violation` (T06.08 — cohort-level path-selection), `API-003-exhaust-point-vocabulary-violation` (T06.07 — per-emission wire-shape), `DM-003-found-n-times-invariant-violation` (T06.05 — per-emission counter-shape), and `DM-003-fixed-field-invariant-violation` (T06.03 — per-emission boundary fixed-field), because the INV-021 + R-126 gates scope the **execution-layer + merge-step layer** spanning cohort-wide parallelism and post-emission severity / count preservation across the merge boundary. All three rejections MUST NOT be silently coerced. Rationale: a per-cohort N-1 concurrency invariant pinned at the orchestrator boundary makes the parallel-research property NFR-CONV.10 auditable across the exhausted-partition case (a sibling cohort serialized behind an exhausted partition's synthesis would multiply the wall-clock cost of the partition-research pipeline by the number of exhausted partitions, breaking the constant-factor parallelism that NFR-CONV.10 ratifies, and a regression here would be invisible to per-emission gates because the synthetic block itself would still pass DM-003 / API-003 / R-122 / INV-012 checks); a real-findings-preservation invariant pinned at the merge-step boundary distinguishes the strictly-additive synthetic emission from a replacement / coalesce / filter merge (a non-additive merge could let a partition that succeeded on K real findings have those K findings absorbed into the synthetic emission for an exhausted sibling, silently reducing the merged report's information content and breaking R-126 alongside-not-replacement; the per-emission gates cannot detect this failure because each individual synthetic block is well-formed — the failure emerges only at the cohort-level count comparison); a merge-step-layer HIGH non-overridable invariant distinct from the per-emission DM-003 fixed-field invariant scopes the override failure to its actual emergence boundary (the per-emission DM-003 gate catches `severity != HIGH` at the emitter; the R-126 merge-step gate catches downstream override attempts that bypass the emitter — both layers are needed because the wire format is preserved post-emission but the merge step can still apply transforms, and a single conflated symbol would force operators to read the full execution log to triangulate which layer failed); three distinct named rejection symbols at the execution-layer + merge-step layer let operator tooling grep-distinguish cohort serialization failures (spawn-log timing pathology) from real-findings replacement failures (merge-step count pathology) from merge-step severity override failures (merge-step severity-transform pathology) without false positives across the layers.

**Dedup key (composition with PR-02 Retry Monotonicity, INV-012).** Two synthetic findings emitted across consecutive retry cycles for the SAME `(assigned_files_range, escalation_ladder_exhaust_point)` collapse into ONE finding annotated `found N times`. This prevents the dedup case from reading as a regression to the PR-02 monotonicity guard (the same partition failed the same way twice is dedup, not regression). Two synthetics with DIFFERENT escalation_ladder_exhaust_points are DISTINCT findings.

This protocol applies symmetrically to:

- A.8 research-gate partition spawns of rf-analyst + rf-qa
- A.10 task-integrity partition spawns of rf-qa (when partitioning is invoked)
- A.10.5 qualitative partition spawns of rf-qa-qualitative

**Synthetic-dnsp merge step for A.8 (R-127, COMP-001-M6 - A.8 Research Quality Gate merge).** Before the **Gate evaluation** paragraph below reads the analyst + QA reports, the orchestrator MUST scan each partition agent's normal output stream for `source: "synthetic-dnsp"` blocks emitted under the API-003-M6 wire-shape contract and merge them into the partition-cohort findings set ALONGSIDE the real analyst + QA findings. Merge semantics: (a) the merge is **strictly additive**: post-merge real-finding count MUST equal pre-merge real-finding count plus synthetic count; (b) the synthetic `severity: HIGH` value is **non-overridable across the merge**; (c) **within-cycle dedup-key collapse (R-123)** MUST run BEFORE the merged set is handed to gate evaluation; (d) **cross-cycle dedup composition (R-124, INV-012)** MUST run before the PR-02 monotonicity comparison; (e) the **all-agents-fail guard (R-122)** MUST have run BEFORE this merge step. The Gate evaluation paragraph then treats each merged synthetic-dnsp record as a real finding: a present synthetic-dnsp record causes FAIL until the operator manually reviews per its fixed `recommendation` literal `Manual review required — partition agent failed twice` (R-117); the gap-fill cycle MUST NOT attempt to auto-resolve synthetic-dnsp records.

### A.8.5: Optional Web Research

**Skip this step unless BOTH conditions are true:**

1. The tier allows web agents (Standard: 0-1, Deep: 1-2, Quick: 0)
2. The quality gate's analyst/QA reports identified **external knowledge gaps** that codebase research cannot fill (e.g., best practices for a technology, library API documentation, design pattern recommendations, MDTM template conventions from external sources)

If neither condition is met, proceed directly to A.9.

**Spawning:** Use the Agent tool with `subagent_type: "general-purpose"`, `mode: "bypassPermissions"`. Spawn 1-2 web research agents in parallel, each investigating a specific gap identified by the quality gate.

**Prompt format:**

```text
Research this topic externally and write findings to ${TASK_DIR}research/web-[NN]-[topic-slug].md

Topic: [specific external research topic from quality gate gaps]
What we already know from codebase: [brief summary of relevant codebase findings]
Task context: [the overall goal for this task file build]

ESCALATION — CRITICAL OVERRIDE:
You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, or TaskList.
You are a standalone agent invoked via the Agent tool. Return your findings by writing
them to the output file. The orchestrator reads the file after you complete.

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for official documentation, guides, and API references
2. Search for design patterns and best practices relevant to this topic
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
  [How external findings should inform the task file being built]

IMPORTANT: Our codebase is the source of truth. External research adds context but does
not override verified code behavior. If you find a discrepancy, note it explicitly.
```

**Output integration:** Web research files are placed in `${TASK_DIR}research/` alongside codebase research files, using the `web-NN-topic.md` naming convention. The builder reads ALL `.md` files in the research directory, so web research is automatically included without special handling.

### A.9: Spawn Builder

Spawn the `rf-task-builder` agent via the Agent tool. The builder reads all research files and the MDTM template, then creates the task file incrementally.

**Skill-delegated BUILD_REQUEST check:** Before constructing the BUILD_REQUEST inline, check if a `BUILD-REQUEST.md` file exists in the task directory (`${TASK_DIR}BUILD-REQUEST.md` or the file path provided at A.1). If found, read its content and use it as the BUILD_REQUEST text block in the agent prompt below — replacing ONLY the inline `BUILD_REQUEST:\n==============\n...` content. Preserve the Agent tool invocation structure (`subagent_type: "rf-task-builder"`, `mode: "bypassPermissions"` wrapper) and all orchestrator mediation logic (RESEARCH_NEEDED, MALFORMED, NEED_USER_INPUT flows). If no BUILD-REQUEST.md file exists, construct the BUILD_REQUEST inline as normal (the default for user-invoked builds).

**BUILD_REQUEST format for the subagent prompt:**

```text
Agent:
  subagent_type: "rf-task-builder"
  mode: "bypassPermissions"
  prompt: |
    BUILD_REQUEST:
    ==============
    GOAL: [GOAL — what the task file should accomplish when executed]

    WHY: [WHY — context for why this task is needed]

    TASK_ID_PREFIX: TASK-RF

    TEMPLATE: [01 or 02 — orchestrator selected:
      01 = simple task, known inputs/outputs, direct transformation
      02 = complex task requiring discovery, build, test, review phases]

    QA_INTENSITY: [lite / standard / full]  (per I22 — determined by calling skill's tier mapping or user override)
    QA_GATE_REQUIREMENTS: [Default: FINAL_ONLY for Template 01, PER_PHASE
      for Template 02. NONE = no QA gates in generated task file. FINAL_ONLY
      = include a final QA validation phase before task completion.
      PER_PHASE = include QA gates after each major phase.

      MANDATORY QA ENCODING RULES (apply to FINAL_ONLY and PER_PHASE):
      1. Agent counts per QA gate are determined by the BUILD_REQUEST's QA_INTENSITY field per I22: lite = 3 agents minimum (1 structural + 1 content + 1 domain), standard = 7 agents minimum (3 structural + 3 content + 1 domain), full = 6+ agents minimum (3 rf-qa + 3 rf-qa-qualitative per I19, plus domain lenses). Gates with fewer than the I22 minimum for the specified intensity
         are PROHIBITED and will be REJECTED during A.10.5.
      2. Each agent gets a SPECIFIC LENS FOCUS (not generic "check everything").
         Standard structural lenses: template-conformance, internal-consistency,
         evidence-quality, completeness.
         Standard content lenses: actionability, numbers-metrics,
         crossref-chain-integrity, domain-accuracy.
      3. Follow MDTM M3 (Lens-Based QA Sequence): spawn all lens agents
         in parallel with fix_authorization: false, consolidate findings,
         spawn single fix agent, then verification round.
      4. If the task produces documents >500 lines OR transforms source
         material into a different format, include a source-document fidelity
         gate per MDTM M4 and I21 (SOURCE-DOCUMENT FIDELITY GATE REQUIREMENT):
         agents read BOTH source inputs AND output to verify faithful
         representation. See I21 for full applicability criteria.
      5. QA gate items MUST be explicit checklist items (`- [ ]`) in the
         task file, not prose descriptions.
      6. All QA agent prompts include adversarial framing.
      7. Scale agents UP for larger outputs per MDTM I19:
         <500 lines: 6 agents, 500-1500: 8, 1500-3000: 10, >3000: 12.
      8. Follow MDTM I20 (Serialized Fix Authorization): NEVER give
         fix_authorization: true to multiple agents simultaneously.
         All lens agents REPORT ONLY. A single fix agent applies all
         fixes after consolidation.

      INTERMEDIATE GATE MINIMUMS (per MDTM I19 — for research-gate,
      synthesis-gate, and task-integrity gates within generated task files):
      | Gate | Min Agents | Agent Types |
      |------|-----------|-------------|
      | Research gate | 5 | 2 rf-analyst (completeness + cross-validation) + 2 rf-qa (evidence-quality + gap-detection) + 1 rf-qa-qualitative (research-depth) |
      | Synthesis gate | 5 | 2 rf-analyst (synthesis-accuracy + source-tracing) + 2 rf-qa (structure + content-quality) + 1 rf-qa-qualitative (synthesis coherence) |

      GUIDANCE: For intermediate gates (research-gate, synthesis-gate),
      use the intermediate agent mix above. For final-document gates
      (phase-gate QA, assembled output QA), use 3 rf-qa + 3 rf-qa-qualitative
      (minimum 6). The two tables serve different purposes — do not
      apply the final-document minimum (per I22) to intermediate gates,
      and do not apply the intermediate 5-agent mix to final-document gates.

      LENS-TO-AGENT MAPPING NOTE: When fewer agents than lenses are
      available (e.g., 3 agents for 4 lenses at the <500 line tier),
      combine related lenses per agent: e.g., template-conformance +
      completeness on one agent, internal-consistency + evidence-quality
      on another. Each agent's prompt must list ALL assigned lenses.
      At higher tiers (4+ agents per type), assign one lens per agent.

      The orchestrator determines the value based on GOAL complexity and
      template selection.]

    VALIDATION_REQUIREMENTS: [Specifies validation checklist items the
      generated task file must include. Examples: "Verify all modified files
      pass linting", "Verify type checking passes", "Verify build succeeds",
      "Verify existing tests still pass". Pull from CLAUDE.md project
      conventions and research findings. Default: "Standard project
      validation: lint, type-check, and build must pass."]

    TESTING_REQUIREMENTS: [Options: NONE (docs-only, config changes), UNIT,
      INTEGRATION, E2E, ALL. Default: Infer from GOAL — implementation/
      refactoring defaults to UNIT minimum; API changes default to UNIT +
      INTEGRATION. When testing is required, task file items must specify:
      test file locations, test naming conventions, coverage targets, and
      verification commands.]

    EXECUTION_CONTEXT_INSTRUCTION: The builder MUST populate the `## Execution Context` section that is present in the MDTM template (immediately after Prerequisites & Dependencies). Populate all three sub-bullets using research findings:
      - **References:** BUILD_REQUEST GOAL verbatim; WHY summary; related-doc IDs (R-001, R-002, ...)
      - **Source areas:** named modules/packages identified in research -- NEVER specific file:line paths (e.g., "rf-qa agent prompts", "task-builder skill body")
      - **Key constraints:** top 1-3 invariants from QA_GATE_REQUIREMENTS / VALIDATION_REQUIREMENTS / TESTING_REQUIREMENTS or research findings
      Omit any sub-bullet that lacks data. If GOAL is the only signal, emit References only.
      NO specific path.py:NN references in this block -- those belong in per-item Context fields.

    POST_REFLECT_GATE: ENABLED
      TASK_FILE: ${TASK_FILE}
      # O1 emits the FLAT wrapper shell-out `superclaude reflect run ${TASK_FILE} --depth deep --fix --promote`
      # behind the SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE skip guard. No SPEC_PATH/DEPTH is threaded into the POST
      # emission: --depth is fixed `deep`, and the wrapper resolves the audit base from frontmatter `start_commit`
      # and the reviewer-exclusion class from frontmatter `executor_model_class`. (PRE still consumes `--spec`.)

    DOCUMENTATION STALENESS WARNINGS:
    [If doc cross-validator researcher found issues, list the specific
    claims and contradictions here. If none found, write:
    "None found during scope discovery. Researchers performed full
    documentation cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/
    UNVERIFIED tags."]
    Do NOT create task items that reference architecture marked
    [CODE-CONTRADICTED] or [UNVERIFIED]. Only use [CODE-VERIFIED]
    findings as the basis for task items.

    RESEARCH DIR: ${TASK_DIR}research/
    Read ALL .md files in this directory for full research findings.
    The research directory contains multiple research files from parallel
    researchers covering:
    [list each researcher's topic and file name]

    QUALITY GATE RESULTS:
    The research was reviewed by analyst and QA agents. Their reports are
    in ${TASK_DIR}qa/:
    - qa/analyst-completeness-report.md — completeness verification
    - qa/qa-research-evidence-report.md — evidence quality verification
    - qa/qa-research-gap-report.md — gap detection and coverage analysis
    - qa/qa-research-depth-report.md — research depth assessment
    [If gap-fill was needed: gap-fill research is in NN-gap-fill.md]

    OPEN QUESTIONS (could not be resolved by research):
    [List any Open Questions from the quality gate — document these as
    risks/assumptions in the task file, NOT as the basis for task items]

    REMAINING GAPS (if any — after max gap-fill rounds):
    [List any gaps that persisted. Document as known limitations.]

    CRITICAL — GRANULARITY REQUIREMENT:
    Per MDTM template rules A3 (Complete Granular Breakdown) and A4
    (Iterative Process Structure), you MUST create individual checklist
    items for EVERY file, component, or iteration involved. Do NOT create
    batch items like "document all 14 handlers in a single item." Each
    handler gets its own item. The research files contain per-file detail
    specifically to enable this granularity.

    CRITICAL — QA GATE ENCODING REQUIREMENT:
    When QA_GATE_REQUIREMENTS is FINAL_ONLY or PER_PHASE, you MUST encode
    QA gates as explicit checklist items in the task file following these
    patterns from the MDTM template:

    M3 — LENS-BASED QA SEQUENCE (mandatory for every QA gate):
    1. Spawn lens-based rf-qa agents in PARALLEL (fix_authorization: false)
       — each agent has a SPECIFIC lens (template-conformance, internal-
       consistency, evidence-quality, completeness). Minimum 3 rf-qa agents.
    2. Spawn lens-based rf-qa-qualitative agents in PARALLEL
       (fix_authorization: false) — each agent has a SPECIFIC lens
       (actionability, numbers-metrics, crossref-chain, domain-accuracy).
       Minimum 3 rf-qa-qualitative agents.
    3. Consolidate all findings into a single findings file.
    4. Spawn ONE fix agent (fix_authorization: true) with consolidated
       findings to apply ALL fixes.
    5. Spawn verification agents to confirm fixes applied correctly.
    6. Max 3 fix-verify cycles.

    M4 — SOURCE FIDELITY GATE (mandatory when output >500 lines):
    After M3 completes, spawn fidelity agents that read BOTH source inputs
    AND the generated output to verify faithful representation. Minimum 2
    fidelity agents.

    I19 — MINIMUM AGENT COUNTS (FLOORS, not targets):

    Final-document / assembled output QA:
    <500 lines output: 6 agents (3 rf-qa + 3 rf-qa-qualitative)
    500-1500 lines: 8 agents (4+4)
    1500-3000 lines: 10 agents (5+5)
    >3000 lines: 12 agents (6+6)
    Domain-specific lenses are ADDITIONAL to these counts.

    Intermediate gate minimums (research-gate, synthesis-gate):
    | Gate | Min Agents | Agent Types |
    |------|-----------|-------------|
    | Research gate | 5 | 2 rf-analyst (completeness + cross-validation) + 2 rf-qa (evidence-quality + gap-detection) + 1 rf-qa-qualitative (research-depth) |
    | Synthesis gate | 5 | 2 rf-analyst (synthesis-accuracy + source-tracing) + 2 rf-qa (structure + content-quality) + 1 rf-qa-qualitative (synthesis coherence) |

    GUIDANCE: For intermediate gates, use the intermediate agent mix.
    For final-document gates, use 3 rf-qa + 3 rf-qa-qualitative (minimum 6).

    I20 — SERIALIZED FIX AUTHORIZATION:
    NEVER give fix_authorization: true to multiple agents simultaneously.
    All lens agents REPORT ONLY. A single fix agent applies all fixes.

    I21 — SOURCE-DOCUMENT FIDELITY GATE REQUIREMENT:
    A source-document fidelity gate (M4) is MANDATORY when:
    (a) the task produces documents >500 lines, OR
    (b) the task transforms source material into a different format (e.g.,
        research → report, code → documentation, spec → implementation plan).
    When I21 applies, the fidelity gate must be encoded as explicit checklist
    items AFTER the M3 lens-based QA sequence. Fidelity agents read BOTH
    source inputs AND generated output to verify faithful representation.
    The builder must evaluate I21 applicability for EVERY QA gate it encodes.

    A final-document QA gate with fewer than 6 agents, or an intermediate
    gate with fewer than 5 agents, will be REJECTED during task file
    validation (A.10.5). Encode each QA agent as its own `- [ ]` item
    with a fully embedded lens-specific prompt.

    TO BUILD A GOOD TASK FILE, YOU NEED:
    - Goal and outputs (what to create, where, what format)
    - Source files and context (what exists, what to reference)
    - Phases and steps (logical breakdown of the work)
    - Verification criteria (how to know each step is done)
    - Dependencies (what's needed before each step)
    The researchers' findings should cover most of this.

    ESCALATION — CRITICAL OVERRIDE:
    Since you are running as a subagent (not a teammate), you have NO
    team context. Do NOT broadcast TASK_READY, use TaskCreate, or use
    SendMessage — these tools will fail because there is no team. This
    overrides your agent definition's Critical Rule 6 ("ALWAYS broadcast
    TASK_READY") and Step 6 (TaskCreate + broadcast). Instead, return the
    task file path as your final output.
    - **Codebase questions** → use WebSearch or codebase-retrieval
    - **External docs/syntax** → use WebSearch
    - **If blocked** → create the best task file you can and note gaps
      in the Task Log section. The skill will review and iterate.
    - **User intent ambiguity** → document in the task file's Open
      Questions section and proceed with the most reasonable
      interpretation.

    INCREMENTAL TASK FILE WRITING (MANDATORY — NEVER ONE-SHOT):
    The task file MUST be written incrementally to disk. NEVER accumulate
    the entire task in context and write it in one shot. One-shotting
    large task files hits the max token output limit and loses all content.

    1. FIRST: Create the file IMMEDIATELY with Write tool containing ONLY:
       - YAML frontmatter (---, NOT +++)
       - # Title
       - ## Task Overview (1-2 paragraphs)
       - ## Key Objectives (bullet list)
       - ## Prerequisites & Dependencies
    2. THEN: Append each phase ONE AT A TIME using Edit tool.
       One phase per Edit call. Verify each Edit succeeded.
    3. LAST: Append the Task Log section after all phases are written.

    TASK FILE LOCATION:
    ${TASK_DIR}${TASK_ID}.md

    STEPS:
    1. Read the MDTM template specified in TEMPLATE field above (MANDATORY):
       - If TEMPLATE: 02 → .claude/templates/workflow/02_mdtm_template_complex_task.md
       - If TEMPLATE: 01 → .claude/templates/workflow/01_mdtm_template_generic_task.md
    2. Read PART 1 (Task Building Instructions) completely
    3. Read ALL research files in the research directory
    4. Follow ALL instructions in PART 1 (Sections A-K for template 01;
       A-K + L for template 02)
    5. If anything is missing, note it in the Task Log section
    5a. Populate the `## Execution Context` section from the template with References / Source areas / Key constraints drawn from research files and BUILD_REQUEST fields. This section is REQUIRED in every task file (except GOAL-only with no source areas, where it degrades to References-only). Do NOT include specific file:line paths in the block header.
    6. Encode QA gates per M3/M4/I19/I20/I21 patterns (see QA GATE ENCODING
       REQUIREMENT above). Every QA gate must have minimum 6 agents with
       lens-focused prompts. Encode each agent as a separate `- [ ]` item.
    7. Create the task file using PART 2 structure (incremental writing)
    8. Return the task file path as your final output
```

**Spawning:** Use `Agent` tool with `subagent_type: "rf-task-builder"` and `mode: "bypassPermissions"`. For multi-track, spawn one builder per track — all in a single message for parallel execution.

**Orchestrator mediation — two distinct flows with independent retry counts:**

1. **RESEARCH_NEEDED flow** (builder needs more data): Builder's return value starts with `RESEARCH_NEEDED:` followed by specific gaps. Orchestrator action:
   - Parse the return for specific research gaps
   - Spawn a new `general-purpose` researcher Agent with the specific question
   - Wait for researcher to return the new research file path
   - Re-invoke builder with original context PLUS the new research file path added to the research directory listing
   - **Maximum 2 RESEARCH_NEEDED rounds** (tracked independently from malformed rounds)
   - After max rounds, proceed with gaps as Open Questions in the task file

2. **MALFORMED flow** (builder produced bad output): Builder returns a task file path, but the file fails structural validation (frontmatter missing, no checklist items, clearly incomplete). Orchestrator action:
   - Read the task file and identify specific problems
   - Re-invoke builder with the problems listed and "fix these issues" instruction
   - **Maximum 2 MALFORMED rounds** (tracked independently from RESEARCH_NEEDED rounds)
   - After max rounds, present the task file as-is with issues documented

3. **NEED_USER_INPUT flow** (unresolvable user-intent ambiguity): Since the builder runs as a fire-and-forget Agent subagent, it cannot pause mid-execution to ask the orchestrator questions. If the builder encounters an ambiguity that cannot be inferred from research, it documents the ambiguity in the task file's **Open Questions** section and proceeds with the most reasonable interpretation. The user reviews Open Questions when the task file is presented (A.11) and can modify the task file before execution.

These are SEPARATE retry counters — a builder that returns RESEARCH_NEEDED twice and then produces a malformed file gets 2+2=4 total invocations maximum.

**Halt-precedence note (FR-CONV.5 / API-004 -- COMP-001-M5 A.9 invariant tail).** Every retry counter in this section (RESEARCH_NEEDED, MALFORMED) -- and every per-gate counter inherited from rf-task-builder/rf-qa -- is governed by the strict 4-step ordering rule `regression -> monotonicity -> hard-cap -> proceed`. On every cycle transition `n -> n+1`, the regression halt-message `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (byte-exact wire string per API-004) is evaluated BEFORE the monotonicity halt-message `[HALT-MONOTONICITY] |F|=<n>` (byte-exact wire string per API-004); when both conditions would trigger in the same cycle transition, the regression halt is emitted and the monotonicity check is NOT consulted on the regressed item. Each counter keeps its own halt-precedence state -- counters are NEVER collapsed across gates.

**Retry Monotonicity Protocol (FR-CONV.5 / PR-02 -- strengthens zero-trust QA against oscillation):**

This protocol is the FR-CONV.5 halt-guards wrapper layered ON TOP of every existing fix-cycle loop in task-builder (RESEARCH_NEEDED, MALFORMED, the A.8 research-gate gap-fill loop, the A.10 / A.10.5 fix cycles, rf-task-builder per-gate fix-cycles in rf-task-builder.md, and rf-qa's 3-fix-cycle in rf-qa.md). The wrapper introduces NO new retry loop and NO new stage -- it adds two stop conditions evaluated BEFORE the existing iteration cap fires; the existing 3-cycle hard cap at `rf-team-lead's Fix Cycles rule` is preserved as the fourth-precedence backstop:

1. **Monotonicity guard.** Record the count of remaining gate failures `F_n` at the end of each cycle `n`. If `F_{n+1} >= F_n` -- i.e., the failure count did NOT strictly shrink -- HALT and emit `[HALT-MONOTONICITY] |F|=<n>` (the byte-exact halt-message wire string per API-004). The guard fires only on strict non-shrink; legitimate slow convergence (`F_{n+1} = F_n - 1`) continues to the existing cap. The monotonicity check is only consulted when `|F_n| > 0` AND only after the regression check has passed for this cycle transition.
2. **Regression detection.** Record the set of items that PASSED at the end of each cycle. If any item that PASSed at cycle `n` is FAILing at cycle `n+1`, HALT immediately and emit `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (the byte-exact halt-message wire string per API-004). Regression detection fires only on previously-PASS items -- legitimate refinement of still-FAILing items does not trigger.

**Precedence rule (regression > monotonicity).** Regression detection ALWAYS runs BEFORE the monotonicity check on every cycle transition `n -> n+1`. When both conditions would trigger in the same cycle, the regression halt-message is emitted and the monotonicity check is NOT consulted on the regressed item.

**Independent counters.** Each retry counter keeps its own monotonicity history. RESEARCH_NEEDED, MALFORMED, research-gate gap-fill, A.10 fix cycle, A.10.5 fix cycle, and any per-gate cycles in rf-task-builder/rf-qa each track `F_n` and PASS-set state separately. Counters are NEVER collapsed.

**Composition with PR-03 DNSP synthetic findings (INV-012 acceptance criterion).** Synthetic findings emitted by the DNSP protocol (PR-03) COUNT as failures for the `|F_n|` monotonicity comparison. BUT a synthetic finding with the same `(assigned_files_range, escalation_ladder_exhaust_point)` dedup key appearing across consecutive cycles is a DEDUP case, NOT a regression. Two synthetic findings with identical dedup keys collapse into one with a "found N times" note.

**Single-cycle case.** If the first cycle PASSes, no second cycle runs; both guards are no-ops by construction.

**API-004 Fix-Loop Halt Signals -- wire ABI (M5 contract freeze):**

| Signal | Wire string (byte-exact) | Substitution |
|---|---|---|
| Monotonicity halt | `[HALT-MONOTONICITY] \|F\|=<n>` | `<n>` <- the integer cardinality `\|F_{n+1}\|` at the cycle the guard fires |
| Regression halt | `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` | `X.Y` <- the regressed item identifier; `N` <- the prior-PASS cycle number |

**F-set definition (item identity = dedup-key, cardinality post-dedup):**

`F_n` is the SET of FAIL-verdict items at the end of fix cycle `n`. Set membership is determined by the dedup-key:

- For ordinary checklist items: dedup-key = item ID (e.g., `3.2`).
- For synthetic-dnsp findings (PR-03): dedup-key = `(assigned_files_range, escalation_ladder_exhaust_point)`.

`|F_n|` is the cardinality of `F_n` AFTER dedup-key deduplication.

**4-step ordering rule (strict per cycle transition `n -> n+1`):**

On every cycle transition `n -> n+1`, run the following steps in this exact order and EXIT on the first match -- `regression -> monotonicity -> hard-cap -> proceed`:

1. **Regression check.** If any item with verdict PASS at end-of-cycle-`n` has verdict FAIL at end-of-cycle-`n+1` (by dedup-key identity), HALT and emit the byte-exact regression halt-message. Do NOT consult subsequent steps.
2. **Monotonicity check.** If `|F_n| > 0` AND `|F_{n+1}| >= |F_n|` (cardinality after dedup), HALT and emit the byte-exact monotonicity halt-message `[HALT-MONOTONICITY] |F|=<n>` (with `<n>` = `|F_{n+1}|`). Do NOT consult subsequent steps.
3. **Hard-cap check.** If the per-gate cycle counter has reached the gate-specific cap (research-gate=3, synthesis-gate=2, report-validation=3, task-integrity=2, qualitative=3 -- see the rf-task-builder.md per-gate cap table, with the global 3-cycle backstop at `rf-team-lead's Fix Cycles rule`), HALT per the gate's existing escalation path (HALT-and-escalate or Open Questions).
4. **Proceed.** Re-spawn the fix cycle for cycle `n+1`.

Strict ordering invariant: regression ALWAYS exits BEFORE monotonicity; monotonicity ALWAYS exits BEFORE hard-cap; hard-cap ALWAYS exits BEFORE proceed. Producers MUST NOT reorder or skip steps; consumers (fixture asserts) MUST verify ordering by emission ordering in the execution log.

**Regression non-emission invariant (cross-cycle synthetic-dnsp).** A regression halt MUST NOT be emitted for any item whose dedup-key was in `F_n` (i.e., FAIL_n) -- regardless of whether the item is a synthetic-dnsp finding or an ordinary checklist item. The Step 1 set predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is the only condition that fires the regression halt; cross-cycle dedup is excluded from regression by construction of the predicate. Consumers (fixture asserts) MUST verify `grep -c "Regression detected on Item" <execution-log>` returns `0` for any cross-cycle same-dedup_key transition; the cross-cycle synthetic-dnsp fixture (TEST-022 at T05.14 / D-0065) codifies this invariant.

### A.10: Task File Validation

After the builder returns a task file path, validate the task file before presenting to the user. Spawn 2 rf-qa agents in parallel, each with a focused structural lens. Use serialized fix authorization: both agents report findings only (fix_authorization: false), then a single fix agent applies all consolidated findings.

**Spawn 2 rf-qa agents in parallel** — two Agent calls in one message, both with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`.

**ADVERSARIAL STANCE for both agents:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

**QA prompt:**

```text
Agent 1 (rf-qa — B2 self-containment lens):
  QA_MODE: task-integrity
  LENS: b2-self-containment
  fix_authorization: false

  TASK FILE: [path to the task file the builder created]
  TEMPLATE USED: [01 or 02]
  TRACK GOAL: [goal for this track]
  RESEARCH DIR: ${TASK_DIR}research/

  ESCALATION — CRITICAL OVERRIDE:
  You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate,
  or TaskList. You are a standalone agent invoked via the Agent tool. Return
  your verdict and report file path as your final output.

  **ADVERSARIAL STANCE:** Assume the work contains errors. Find at least 5 issues — a verdict of 0 issues requires extraordinary evidence you thoroughly checked.

  YOUR LENS FOCUS: Verify every checklist item is SELF-CONTAINED per MDTM B2.
  An item must have context + action + output + verification + completion gate.
  An item that says "see above" or "continue from previous" FAILS.

  B2 Self-Containment Checklist:
  1. Every checklist item has all 5 B2 components?
  2. No item references context from a prior item without restating it?
  3. Agent-spawning items have fully embedded prompts (not "see SKILL.md")?
  4. File paths in items are specific (not "the relevant file")?
  5. Verification criteria are measurable (not "verify it works")?
  6. No batch items ("process all X") — each file/component has its own item?
  7. No items based on [CODE-CONTRADICTED] or [UNVERIFIED] findings?

  OUTPUT FILE: ${TASK_DIR}qa/qa-task-validation-b2-report.md
  Write the file IMMEDIATELY with a header, then append findings incrementally.
  Conclude with: VERDICT: PASS or FAIL, and severity-rated issues if FAIL.

Agent 2 (rf-qa — phase structure/ordering lens):
  QA_MODE: task-integrity
  LENS: phase-structure
  fix_authorization: false

  TASK FILE: [path to the task file the builder created]
  TEMPLATE USED: [01 or 02]
  TRACK GOAL: [goal for this track]
  RESEARCH DIR: ${TASK_DIR}research/

  ESCALATION — CRITICAL OVERRIDE:
  You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate,
  or TaskList. You are a standalone agent invoked via the Agent tool. Return
  your verdict and report file path as your final output.

  **ADVERSARIAL STANCE:** Assume the work contains errors. Find at least 5 issues — a verdict of 0 issues requires extraordinary evidence you thoroughly checked.

  YOUR LENS FOCUS: Verify task file STRUCTURE and PHASE ORDERING.

  Phase Structure Checklist:
  1. YAML frontmatter complete and well-formed?
  2. All mandatory sections present per template?
  3. Phase dependencies are logical (no circular or missing dependencies)?
  4. Phase ordering follows logical progression (research before build, build before test)?
  5. Task completion items inside final phase (anti-orphaning)?
  6. Task Log section present at bottom?
  7. Estimated item count is reasonable for the scope?
  8. Open Questions and remaining gaps documented (if any)?
  9. QA gate items in the task file follow MDTM M3 (lens-based QA sequence)
     and M4 (source fidelity gate) patterns? (If MDTM template has been
     updated with these patterns, verify compliance.)
  Structural Gate Additions (TB-Add-1, TB-Add-3 through TB-Add-8, imported from sc:tasklist 17-point pre-write gate per CB-3 per-check classification, see rf-qa agent definition for full rationale):
  10. TB-Add-1: Placeholder scan: no item contains `TBD`/`TODO`/`FIXME` and no item is title-only (5-field schema enforced).
  11. TB-Add-3: Clarification adjacency: each blocked item references its blocking Open Question by index in Context.
  12. TB-Add-4: Circular dependency detection: item-to-item dependencies form a DAG; no cycles.
  13. TB-Add-5: Granularity / XL splitting: items flagged complex/multi-file are either split into subtasks or carry a justifying comment.
  14. TB-Add-6: Confidence/Verification format consistency: uniform `Verify: ...` prefix and `- [x]` Acceptance Criteria form.
  15. TB-Add-7: Execution Context source areas reappear in items: every "Source areas:" entry in the `## Execution Context` block reappears in at least one item's Context field; the block itself contains NO specific file:line references. INACTIVE if no Execution Context block exists.
  16. TB-Add-8: Per-item Context evidence binding: every item Context field that references a code surface includes a file:line citation OR an `<!-- evidence-absence: ... -->` justified-absence comment. Structurally proves PR-01's "no specific paths" rule is confined to the header (INV-015 scope-confinement).

  OUTPUT FILE: ${TASK_DIR}qa/qa-task-validation-structure-report.md
  Write the file IMMEDIATELY with a header, then append findings incrementally.
  Conclude with: VERDICT: PASS or FAIL, and severity-rated issues if FAIL.

Consolidation + Fix Round:
  After both agents return, read both reports. Consolidate all findings
  into ${TASK_DIR}qa/qa-task-validation-consolidated.md. Then spawn a
  SINGLE rf-qa fix agent (fix_authorization: true) with the consolidated
  findings list to apply ALL fixes to the task file. After fixes, spawn
  a verification agent to confirm fixes were applied correctly.
  Max 3 fix-verify cycles.
```

**Handling the verdict:**

- **ALL PASS** → Proceed to A.10.25 (research-alignment validation)
- **ANY FAIL, all fixes applied by fix agent** → Verification confirms fixes. Proceed to A.10.25.
- **FAIL with unfixable issues after 3 fix-verify cycles** → Present the issues to the user alongside the task file. Let them decide whether to proceed, fix manually, or re-run.
- **No verdict emitted (report file absent OR present but no `VERDICT:` line OR `VERDICT:` value not `PASS`/`FAIL`)** -- treat as a failed cycle, do NOT advance to A.10.25. Re-spawn rf-qa (counts against the A.10 fix-cycle budget, max 3 cycles). At max cycle, surface the missing/malformed report to the user as an Open Question in the task file and proceed to A.10.25 with the issue documented. The orchestrator MUST: (a) check `${TASK_DIR}qa/qa-task-validation-b2-report.md` and `qa-task-validation-structure-report.md` exist on disk; (b) if absent, log `INV-002-no-producer-artifact` and surface the missing-report path to the user; (c) if present, grep for `^VERDICT: (PASS|FAIL)` (case-sensitive, line-anchored); if zero matches, log `INV-002-no-verdict-line` and surface the malformed-report path to the user. DM-005 token: `failure_mode: retry-into-max-cycle-then-Open-Questions`.

### A.10.25: Task File Research-Alignment Validation

After structural QA passes, cross-validate the task file against the research files to ensure the builder faithfully translated research findings into actionable checklist items. This is the 5th agent in the task-integrity gate (A.10 provides 2 rf-qa, A.10.5 provides 2 rf-qa-qualitative, and A.10.25 provides 1 rf-analyst), satisfying the MDTM I19 intermediate gate floor of 5 agents.

**Spawn 1 rf-analyst agent** via Agent tool with `subagent_type: "rf-analyst"`, `mode: "bypassPermissions"`.

**QA prompt:**

```text
Agent (rf-analyst — task-research-alignment lens):
  QA_MODE: task-integrity
  LENS: task-research-alignment

  TASK FILE: [path to the task file the builder created]
  RESEARCH DIR: ${TASK_DIR}research/
  TRACK GOAL: [goal for this track]

  ESCALATION — CRITICAL OVERRIDE:
  You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate,
  or TaskList. You are a standalone agent invoked via the Agent tool. Return
  your verdict and report file path as your final output.

  **ADVERSARIAL STANCE:** Assume the builder dropped or misrepresented
  research findings. Find at least 3 alignment gaps.

  YOUR LENS FOCUS: Cross-validate that every significant finding in the
  research files has a corresponding checklist item in the task file, and
  that no task file item fabricates actions not grounded in research.

  Research-Alignment Checklist:
  1. For each research file, identify its key findings (file paths, patterns,
     requirements, conventions discovered).
  2. For each key finding, verify a corresponding task file item exists that
     acts on that finding.
  3. Identify any task file items that reference files, patterns, or
     requirements NOT present in any research file (fabrication check).
  4. Verify that research-identified edge cases and caveats are reflected
     in task file verification criteria ("ensuring..." clauses).
  5. Check that research-identified dependencies between components are
     reflected in task file phase ordering.

  OUTPUT FILE: ${TASK_DIR}qa/qa-task-research-alignment-report.md
  Write the file IMMEDIATELY with a header, then append findings incrementally.
  Conclude with: VERDICT: PASS or FAIL, and severity-rated issues if FAIL.
```

**Handling the verdict:**

- **PASS** → Proceed to A.10.5 (qualitative validation)
- **FAIL** → Findings are merged into the A.10 consolidated findings file (`qa-task-validation-consolidated.md`). Spawn a NEW rf-qa fix agent (fix_authorization: true) with the alignment findings appended to the consolidated file. This fix agent applies alignment fixes to the task file. After fix, proceed to A.10.5. Maximum 1 fix-verify cycle for A.10.25 findings (independent of A.10's 3-cycle budget). If unfixable after 1 cycle, document issues in the consolidated file and proceed to A.10.5.

**Note on gate composition:** The combined task-integrity gate spans A.10 + A.10.25 + A.10.5 = 2 rf-qa + 1 rf-analyst + 2 rf-qa-qualitative = 5 agents, meeting the MDTM I19 intermediate gate floor.

### A.10.5: Task File Qualitative Validation

After structural QA passes, validate that the task file would actually succeed if executed AND that it contains sufficient QA gate coverage. Spawn 2 rf-qa-qualitative agents in parallel, each with a focused lens. Use serialized fix authorization: both agents report findings only (fix_authorization: false), then a single fix agent applies all consolidated findings.

This step catches two categories of issues:

- **Operational issues** (Agent 1): gates that will fail, function signatures that don't match the described modifications, downstream dependencies not updated, tests that exercise stubs instead of real artifacts, runtime paths that break partway through.
- **QA gate sufficiency issues** (Agent 2): generated task files with inadequate QA coverage — too few agents at gates, missing lens-based QA patterns, missing source fidelity gates. This is the enforcement mechanism that closes the QA hardening loop.

**Spawn 2 rf-qa-qualitative agents in parallel** — two Agent calls in one message, both with `subagent_type: "rf-qa-qualitative"`, `mode: "bypassPermissions"`.

**ADVERSARIAL STANCE for both agents:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

**Building the target file list:** Before spawning, read the task file and extract ALL unique source file paths referenced by checklist items (every file that an item reads, modifies, creates, or runs a command against). This is the TARGET_FILE_LIST. Do NOT allow spot-checking — both qualitative agents must verify every target file, not a sample.

**Inherited Structural Verdict (PR-04 Gate Results Passthrough -- operationalises rf-qa-qualitative rule #11):** Before spawning rf-qa-qualitative, read `${TASK_DIR}qa/qa-task-validation-consolidated.md` (rf-qa's A.10 consolidated output). Extract the "Items Reviewed" PASS/FAIL table **contiguously** -- a single span between the `## Items Reviewed` heading and the next top-level (`##`) heading -- verbatim, with no editing/summarising/renaming/re-ordering. **Splice the extracted span byte-for-byte into the rf-qa-qualitative spawn prompt as a `## Inherited Structural Verdict` section, after the TARGET FILES + PROJECT CONVENTIONS context blocks and before the ADVERSARIAL STANCE / INSTRUCTIONS directive blocks.** The orchestrator MUST also dynamically enumerate every TB-Add-* item from rf-qa.md's current checklist (do NOT hand-maintain the list -- read rf-qa.md and pull the live TB-Add catalogue) so the verdict passthrough auto-picks up future structural additions (INV-010). On EVERY fix cycle re-spawn, the orchestrator MUST re-read the freshly-written consolidated report and re-inject the new verdict -- never reuse a stale verdict from a prior cycle (INV-002). If the consolidated report is missing or its `VERDICT:` line is absent/malformed, handle per the DM-005 `failure_mode: retry-into-max-cycle-then-Open-Questions` lever (see A.10 verdict handling).

The consumer agent (rf-qa-qualitative) retains independent standalone capability, but operationally FR-CONV.3 (PR-04 passthrough) + INV-002 (freshness) + INV-010 (dynamic enumeration) require a producer verdict for every spawn: the anti-inflation rule requires an enumerated checklist that only the producer can publish, and the Self-Audit obligation (INV-019) requires the consumer to declare which producer-PASS items it relied on.

**QA prompt:**

```text
QA_PHASE: task-qualitative
fix_authorization: true

TASK FILE: [path to the task file]
RESEARCH DIR: ${TASK_DIR}research/
TRACK GOAL: [goal for this track]

TARGET FILES (verify ALL — no spot-checking):
[list every unique source file path from checklist items]

PROJECT CONVENTIONS:
[Include any project-specific patterns discovered during research that affect
whether items will succeed. Examples:
- Sync models: "src/superclaude/ is source of truth. make sync-dev copies
  src/ → .claude/. make verify-sync fails if .claude/ has dirs with no src/
  counterpart."
- Build gates: "make lint runs ESLint with --max-warnings 0"
- Test location: "Tests go in tests/ using pytest. The project does not use
  inline python -c scripts for testing."
- CI requirements: "Pre-commit hooks run ESLint + Prettier on staged files"
Pull these from CLAUDE.md and research files. If no project-specific
conventions were discovered, state "None identified."]

## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)
[Verbatim embed of rf-qa's "Items Reviewed" table from
qa/qa-task-validation-report.md. On each fix-cycle re-spawn the
orchestrator re-injects the freshly-written verdict (INV-002).]

Items marked PASS by rf-qa are machine-verified. Do NOT re-verify
section numbering, frontmatter shape, item structure, or any TB-Add-*
structural check that rf-qa already PASSED. Focus on semantic quality
(scope, audience, logical flow, contradictions, evidence sufficiency,
the 5 Adversarial Axes per your task-qualitative checklist).

Items marked FAIL by rf-qa are machine-verified defects. Flag them as
HIGH severity in your own report — they remain blockers regardless of
how qualitative review proceeds.

ANTI-INFLATION RULE: rf-qa PASS items skip structural re-checking but
each SEMANTIC check requires your own tool engagement. Reliance is not
verification. Your Self-Audit MUST list (a) which rf-qa PASS items you
relied on and (b) at least one semantic check where rf-qa PASS was
INSUFFICIENT and your own tool work was required (e.g., section content
quality vs. section numbering — rf-qa verifies the number, you verify
the prose) (INV-019).

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

INSTRUCTIONS:
Apply the 15-item Task File Qualitative Review checklist from your agent
definition. For each checklist item that requires reading source code, read
the ACTUAL target files — do not rely on research file summaries alone.

Apply the 5 Adversarial Axes (PR-07) as a sharpening overlay across all
15 checks: drift, contradictions, omissions, weakened-criteria,
invented-content. Every task-qualitative row's Axis column carries
exactly one value from the canonical vocabulary `{AX-1, AX-2, AX-3,
AX-4, AX-5, none}` — FAIL rows MUST carry the most-specific firing
axis (AX-1..AX-5); PASS rows that surfaced no axis finding carry
`none` (positive statement that all five axes were applied and none
fired, NOT an N/A escape). `N/A`/`n/a`/`—`/blank in the Axis column
is forbidden for task-qualitative phase. The drift axis (AX-1)
requires a BUILD_REQUEST.GOAL verbatim baseline; if no GOAL verbatim
is reachable, emit the literal `drift-axis-inactive` annotation in
the Summary block (not as an Axis-column cell value) and proceed with
the other four axes (AX-2..AX-5).

For every shell command or make target referenced in checklist items, verify
its preconditions are satisfied by earlier items or the current repo state.

For task files with >15 checklist items: you may receive an assigned_phases
list limiting your scope. If so, verify only items in those phases and note
cross-phase limitations in your report.

Verify that QA_GATE_REQUIREMENTS, VALIDATION_REQUIREMENTS, and
TESTING_REQUIREMENTS from the BUILD_REQUEST are reflected as corresponding
checklist items in the generated task file. If QA_GATE_REQUIREMENTS is
PER_PHASE but no QA gate items exist, FAIL. If TESTING_REQUIREMENTS is
UNIT but no test items exist, FAIL.

ESCALATION — CRITICAL OVERRIDE:
You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate,
or TaskList. You are a standalone agent invoked via the Agent tool. Return
your verdict and report file path as your final output.

OUTPUT FILE: ${TASK_DIR}qa/qa-qualitative-review.md

Write the file IMMEDIATELY with a header, then append findings incrementally.

If fix_authorization is true and you find issues: fix them IN-PLACE in the
task file using Edit, then document what you fixed in your report.

Conclude with: VERDICT: PASS or FAIL (with list of unfixable issues if FAIL).
```

**Parallel partitioning for large task files:** If the task file has >15 checklist items, spawn multiple rf-qa-qualitative instances in parallel, each assigned a subset of phases via the `assigned_phases` field in the prompt. Each instance reads its assigned phases' items + the source files those items reference. After all instances complete, read all partition reports and merge findings. For cross-phase checks (downstream consumer analysis, runtime path trace), perform a brief cross-phase validation yourself after merging — the partition instances can only trace within their assigned phases.

**Handling the verdict:**

- **PASS** → Proceed to A.11 (present results)
- **FAIL with all fixes applied** → QA fixed all issues in-place. Verify fixes by re-reading affected sections. Proceed to A.11.
- **FAIL with unfixable issues** → Present the issues to the user alongside the task file. Let them decide whether to proceed, fix manually, or re-run.

Read the qualitative QA report. If any issues found (CRITICAL, IMPORTANT, or MINOR), verify fixes were applied correctly by re-reading the affected task file sections. If issues remain unfixed, address ALL of them before proceeding to A.11. Zero leniency — no severity level is exempt.

**Fix-cycle re-entry (INV-002 freshness — stale-verdict rejection):** Any re-entry into A.10.5 — whether triggered by an A.10 producer fix-cycle (rf-qa re-ran and rewrote `${TASK_DIR}qa/qa-task-validation-report.md`), an A.10.5 consumer fix-cycle (rf-qa-qualitative re-spawn after task-file edits), or any external orchestrator-driven re-run — MUST execute the following procedure BEFORE re-issuing the Agent spawn call. Skipping the procedure and re-using a verdict block from the prior cycle is forbidden (INV-002).

1. **Discard cached state.** If the orchestrator memoised any of `(a)` the prior cycle's extracted "Items Reviewed" span, `(b)` the prior cycle's TB-Add-* enumeration snapshot, `(c)` the prior cycle's assembled `## Inherited Structural Verdict` block, or `(d)` the prior cycle's fully-rendered QA prompt string, it MUST drop them. No cached artifact from cycle N may participate in cycle N+1's spawn.
2. **Re-read the producer artifact from disk.** Re-stat `${TASK_DIR}qa/qa-task-validation-report.md` (capture `mtime` and `sha256` as the freshness witness) and re-open it. If the witness equals the prior cycle's witness, the producer did not re-run between cycles — log a `stale-producer` warning but proceed; freshness is enforced by re-extraction, not by mtime comparison alone. If the witness differs, the file is confirmed fresh.
3. **Re-extract the "Items Reviewed" span contiguously.** Apply the same single-span extraction rule from the directive above (between the `## Items Reviewed` heading and the next top-level `##` heading). Do NOT reuse the prior cycle's extraction even if the surrounding file appears unchanged — re-extract every time.
4. **Re-enumerate the TB-Add-* catalogue (INV-010).**Re-read `rf-qa.md`'s live checklist and re-pull the TB-Add-* IDs. Do NOT reuse the prior cycle's enumeration snapshot.
5. **Re-assemble and re-splice.** Build the new `## Inherited Structural Verdict` block from the freshly-extracted span + freshly-enumerated TB-Add-* IDs. Splice it into the spawn prompt at the API-002 wire-contract position (after TARGET FILES + PROJECT CONVENTIONS; before ADVERSARIAL STANCE / INSTRUCTIONS). The cycle N+1 spawn prompt MUST contain the cycle N+1 verdict; a byte-diff of cycle N vs. cycle N+1 at the verdict-table region MUST surface the cycle N+1 content (`grep -A` on `## Inherited Structural Verdict` returns the new span).
6. **Stale-verdict-rejection (defense-in-depth).** Before issuing the spawn call, compute `sha256` of the new `## Inherited Structural Verdict` block and compare it to a `last_injected_verdict_sha256` ledger entry keyed by `${TASK_DIR}`. If the prior cycle wrote a verdict with a non-zero ledger entry AND the new sha256 equals the prior entry AND the producer-artifact witness in step 2 reports a NEW mtime/sha256, that combination is impossible under a correct re-extract — REJECT the spawn, log an `INV-002-stale-verdict-rejected` error with both witnesses, and re-run steps 2–5. (Equal witnesses + equal block sha256 is the legitimate no-op case when the producer truly did not change; only the contradiction case is rejected.)
7. **Log the re-extract.** Emit a structured log line `INV-002: re-extracted verdict for ${TASK_DIR} cycle=N+1 producer_mtime=<iso> producer_sha256=<hex8> block_sha256=<hex8>` at every fix-cycle boundary. The log is the operator-visible audit-trail proving the re-extract ran.

This procedure operationalises the `freshness_rule: INV-002-reinject-NEW` field of the DM-005 Phase Contract (A.10.6). The 2-cycle byte-diff fixture (TEST-008, T03.13) consumes log lines from step 7 and the assembled blocks from step 5 as its assertion surface.

**TB-Add catalogue enumeration (INV-010 dynamic catalogue lookup):** The TB-Add-* catalogue is sourced from `rf-qa.md`'s live "Structural Gate Additions" section at runtime — never from a hand-maintained list inside this skill. Every spawn (initial entry **and** every fix-cycle re-entry per step 4 of the freshness procedure above) MUST execute the following procedure to build the enumeration handed to the consumer:

1. **Locate `rf-qa.md`.** Resolve the path via the project's agent registry (canonical surface: `src/superclaude/agents/rf-qa.md`; mirror surface: `.claude/agents/rf-qa.md`). The canonical surface is authoritative; the mirror is consulted only when the canonical surface is unreachable.
2. **Bound the catalogue region.** Identify the `#### Structural Gate Additions` heading and treat the catalogue region as the span from that heading to the next `####`, `###`, or `##` heading (whichever comes first). Enumeration MUST be confined to this span — TB-Add tokens outside the span (e.g., illustrative references in narrative prose) do NOT contribute to the catalogue.
3. **Extract IDs.** Within the bounded span, match the regex `^[0-9]+\. \*\*TB-Add-([0-9]+):` (Python `re` flavour, MULTILINE) against the span. Each match yields one TB-Add-N ID via the captured integer N.
4. **Build the live set.** Deduplicate, sort ascending by N, and form `LIVE_TB_ADD = [TB-Add-1, TB-Add-3, …, TB-Add-K]`. K is the runtime size of the catalogue; it is never asserted against a hard-coded constant in this skill.
5. **Cross-check against the producer.** Every `TB-Add-*` row present in the freshly-extracted "Items Reviewed" span (step 3 of the freshness procedure) MUST appear in `LIVE_TB_ADD`. A row whose TB-Add-N is absent from `LIVE_TB_ADD` is an orphan (producer ran on a stale catalogue) — FAIL the spawn with `INV-010-orphan-tb-add` and retry into the max cycle then Open Questions (re-uses the `failure_mode: retry-into-max-cycle-then-Open-Questions` lever). A TB-Add-N present in `LIVE_TB_ADD` but absent from the producer table is allowed only when the producer's own report explicitly annotates it as `not-yet-implemented`; otherwise FAIL with `INV-010-missing-tb-add-row`.
6. **Forbid hard-coded enumeration in the orchestrator logic.** This A.10.5 procedure block MUST NOT itself enumerate a fixed `[TB-Add-1, …, TB-Add-K]` list as the spawn target. The directive narratives in this section reference the catalogue abstractly (via the dynamic `LIVE_TB_ADD`); only `rf-qa.md` is the source of the live IDs. (Operator self-check: grep for `TB-Add-[0-9]+` inside the A.10.5 span and confirm every match is either a regex pattern, a worked example tagged `illustrative`, or an integrated-checklist reference — never an orchestrator enumeration target.)
7. **Emit a structured log line.** Write `INV-010: enumerated TB-Add-* catalogue size=K ids=[TB-Add-1,...,TB-Add-K] source=rf-qa.md source_sha256=<hex8>` at every spawn boundary (initial entry and each fix-cycle re-entry). The log is the operator-visible audit-trail and the TEST-010 fixture's (T03.15) assertion surface.
8. **Auto-richening invariant.** Appending a new `**TB-Add-N+1: <name>` line inside the bounded catalogue region of `rf-qa.md` MUST cause `LIVE_TB_ADD` to grow by exactly one entry on the next spawn — with **zero edits** to this SKILL.md, to orchestrator code, or to any consumer-side configuration. This is the K-007 sequencing-inversion mitigation cited in `roadmap.md` R-069: FR-CONV.1 catalogue additions auto-propagate to the PR-04 passthrough.

This procedure operationalises the `enumeration_rule: INV-010-auto-pick-TB-Add` field of the DM-005 Phase Contract (A.10.6). The structural-diff fixture (TEST-010, T03.15) consumes log lines from step 7 and the LIVE_TB_ADD set assembled in step 4 as its assertion surface — adding a synthetic TB-Add-N+1 stub to `rf-qa.md`'s bounded region and asserting the cycle-2 spawn prompt auto-richens by exactly one TB-Add-N+1 row.

### A.10.6: DM-005 Phase Contract -- rf-qa -> rf-qa-qualitative (published row)

Standalone publication of the 10-field producer/consumer agreement that governs the A.10 -> A.10.5 inter-agent handoff. The contract was frozen at M1 (T01.13 / D-0011 section DM-005) and is published here as the wire reference for FR-CONV.3 (PR-04), which lands the orchestrator-mediated spawn-prompt injection. `schema_version: 1.0.0` is the baseline for all future inter-agent contracts emitted by this skill.

**DM-005 Phase Contract (10 fields):**

```yaml
# DM-005 -- Phase Contract: rf-qa -> rf-qa-qualitative
producer: rf-qa
consumer: rf-qa-qualitative
artifact: Inherited Structural Verdict block
schema_version: 1.0.0
delivery_semantics: at-most-once-per-cycle
freshness_rule: INV-002-reinject-NEW
enumeration_rule: INV-010-auto-pick-TB-Add
consumer_obligation: INV-019-Self-Audit
anti_inflation: preserve-766-775-byte-stable
failure_mode: retry-into-max-cycle-then-Open-Questions
```

**Field-by-field semantics (1.0.0 wire ABI):**

| Field | Wire Value | Meaning |
|---|---|---|
| producer | `rf-qa` | The rf-qa agent invoked under `QA_MODE: task-integrity` (A.10). Writes consolidated report to `${TASK_DIR}qa/qa-task-validation-consolidated.md`. |
| consumer | `rf-qa-qualitative` | The rf-qa-qualitative agent invoked under `QA_PHASE: task-qualitative` (A.10.5). Consumes the producer artifact via spawn-prompt injection. |
| artifact | `Inherited Structural Verdict block` | Named block embedded under heading `## Inherited Structural Verdict` in the consumer's spawn prompt. Contents = the entire "Items Reviewed" PASS/FAIL table from the producer's consolidated report, byte-identical. |
| schema_version | `1.0.0` | Wire ABI version. Major-version bump REQUIRED for any field add/rename, semantic change, or value-type change. |
| delivery_semantics | `at-most-once-per-cycle` | Exactly one verdict block is injected per consumer spawn. On fix-cycle re-spawn, the prior block is REPLACED (not appended). |
| freshness_rule | `INV-002-reinject-NEW` | Orchestrator MUST re-read the freshly-written consolidated report on EVERY fix-cycle re-spawn and re-inject the NEW cycle-N verdict. |
| enumeration_rule | `INV-010-auto-pick-TB-Add` | Orchestrator MUST dynamically enumerate every TB-Add-* item from rf-qa.md's live checklist at injection time. |
| consumer_obligation | `INV-019-Self-Audit` | rf-qa-qualitative MUST emit a `## Self-Audit` section listing which rf-qa PASS items it relied on AND >=1 semantic check where rf-qa PASS was insufficient. |
| anti_inflation | `preserve-766-775-byte-stable` | The anti-inflation bullet at the canonical rf-qa-qualitative.md anchor MUST remain byte-identical across releases. |
| failure_mode | `retry-into-max-cycle-then-Open-Questions` | If the consolidated report is missing or malformed, orchestrator treats as failed cycle (per DET-015 no-halt decision). |

### A.10.7: PRE Reflect Gate

After the qualitative gate (A.10.5) passes and the DM-005 phase contract (A.10.6) is recorded, run an independent PRE reflect gate against the just-built tasklist BEFORE presenting results (A.11). This is the cheapest executor-disjoint anti-bias check: the three rf-* gates above verify the tasklist is *present and internally correct*, but they run in the same orchestrator frame and cannot confirm it is *spec-literal-correct and coverage-complete*. The gate is **advisory-blocking** in ONE narrow sense ONLY: its verdict does not auto-mutate the tasklist and does not auto-re-invoke the builder. "Advisory" NEVER means the reflect run is optional. When a `--spec` resolves, running reflect to completion is MANDATORY; deferring or skipping it for ANY reason (cost, runtime, context length, the skill-under-edit, an unratified spec, or coverage already shown by another gate) is a PROTOCOL VIOLATION, not a permitted degrade.

**Resolve depth and spec.** Compute the Tasklist Complexity Score (see `## Reflect Depth (Deterministic TCS)`) from the finished MDTM file -> `pre_depth` (`quick`/`standard`/`deep`; `quick` is permitted at PRE because no diff exists yet). Resolve `spec_path` per the A.2 priority order. `verdict: skipped` is legal in EXACTLY ONE case: `spec_path` is null (no `--spec` resolves), and the only `skip_reason` that exists is `no-spec`. In that one case the gate degrades to `verdict: skipped` (UC-1 coverage is spec-dependent) and proceeds to A.11. If a spec resolves, `skipped` is FORBIDDEN and reflect MUST run.

**Spawn reflect directly.** Invoke `Skill sc:reflect-protocol` via the Agent/Task tool using the **default subagent model** (no model-routing flag), mirroring how `/sc:brainstorm` Wave 3 invokes `Skill sc-adversarial-protocol`. Pass the flag string:

```text
--mode pre --remediate
[--spec <spec_path>]            # omitted => verdict: skipped (no-spec)
--tasklist <TASK_FILE>
--depth <pre_depth>            # raw TCS-derived depth; quick permitted at PRE
--output ${TASK_DIR}reflect/pre/
```

Do **NOT** pass `--executor-model` at PRE: no executor has run in `--mode pre`, so excluding an executor class is a category error (it is a POST-only concern, see A.9 `POST_REFLECT_GATE`).

**Route the verdict (advisory-blocking).** Consume reflect's return contract (`status`, `coverage_pct`, `unmapped_requirements`, `run_id`). Then:

- `coverage_pct >= coverage-floor` (default 0.90) AND `status` not failed -> stamp the sign-off block `verdict: pass` and proceed to A.11.
- else -> stamp `verdict: fail`, **additively** append the `unmapped_requirements` list to the tasklist's `### Open Questions` via Edit (NEVER rewrite or delete existing items), and carry the `--remediate` Tier-3 offer into A.11. The build still completes; the tasklist is flagged not-signed-off.
- no spec -> `verdict: skipped` (reason: no-spec); proceed (the rf-* gates remain the only coverage check).

**Record the sign-off.** Add to the generated tasklist frontmatter:

```yaml
reflect_pre:
  verdict: pass | fail | skipped   # skipped LEGAL ONLY when spec_path is null (reason: no-spec); a skipped verdict with a resolved spec is MALFORMED
  skip_reason: no-spec | null      # REQUIRED `no-spec` when verdict: skipped; null (or omitted) for verdict: pass | fail
  coverage_pct: <float | null>
  depth: quick | standard | deep
  tcs: <int>
  run_id: <reflect run id | n/a>   # real reflect run id when spec_path resolved (verdict: pass|fail); `n/a` ONLY when verdict: skipped (no-spec). Never deferred / pending / empty.
  report: ${TASK_DIR}reflect/pre/report.md | null   # report path when spec_path resolved; null when verdict: skipped (no-spec)
  reviewed_at: <ISO-ts>
```

**Mandatory-run check (hard STOP, the enforcement, not advisory).** This check is conditional on spec resolution. **When `spec_path` resolved (`verdict` ∈ {`pass`, `fail`}):** before proceeding to A.11, verify ON DISK that reflect actually executed — the report file at `${TASK_DIR}reflect/pre/report.md` MUST exist AND `reflect_pre.run_id` MUST be a real reflect run id. A `run_id` of `deferred` / `n/a` / `pending` / empty, OR a `verdict: skipped` while `spec_path` is non-null, OR a missing report file when a spec resolved, ALL mean the PRE gate did not run: this is a MALFORMED run. **When `spec_path` is null (`verdict: skipped`, `skip_reason: no-spec`):** reflect legitimately did not run — `run_id: n/a` and `report: null` are the CORRECT recorded values, NOT a MALFORMED run; the report-exists / real-run_id requirements do NOT apply and MUST NOT be used to fabricate a `run_id` or a report file. On a MALFORMED run, do NOT present A.11. Either invoke reflect now and complete the gate, or, ONLY if the `sc:reflect-protocol` skill probe genuinely fails, log a hard blocker per Rule 14 with the specific failure. Substituting another gate's coverage result (e.g. the A.10.25 alignment verdict) for an actual reflect run is explicitly NOT permitted.

**Loop policy: max 0 auto-loops.** The PRE gate NEVER re-invokes the builder automatically: a `fail` verdict is surfaced for operator action only (avoiding the unattended-mutation failure mode). Reflect's findings are spec-level and may require human judgment, unlike the bounded auto-fix of the rf-* gates.

### A.11: Present Results

**Check the BUILD_REQUEST for `Source: skill-delegated`:**

If `Source: skill-delegated` is present in the BUILD_REQUEST:

- Do NOT print the TASK FILE BUILD COMPLETE banner
- Do NOT print the TO EXECUTE instructions
- Output ONLY this single line: `TASK_FILE_READY: ${TASK_DIR}${TASK_ID}.md`
- Then STOP -- the calling skill will handle presentation and Stage B invocation.

If `Source: skill-delegated` is NOT present (direct user invocation):

- Present the completed task file to the user with the full banner format below.

**Single-track result format:**

```text
================================================================
              TASK FILE BUILD COMPLETE
================================================================

TASK FILE: ${TASK_DIR}${TASK_ID}.md
TEMPLATE: [01 Generic / 02 Complex]
ITEMS: [X] checklist items across [N] phases
RECOMMENDED BATCH SIZE: [N]

QUALITY GATES:
  Research gate: [PASS/FAIL] ([N] researchers, [N] gap-fill rounds)
  Task structural validation: [PASS/FAIL] ([N] issues fixed in-place)
  Task research-alignment: [PASS/FAIL] ([N] issues fixed in-place)
  Task qualitative validation: [PASS/FAIL] ([N] issues fixed in-place)

REFLECT GATES:
  PRE  (--mode pre):  [PASS coverage=0.94 depth=standard tcs=22] | [FAIL coverage=0.71 see Open Questions] | [SKIPPED no-spec]
  POST (superclaude reflect run): emitted as the penultimate final-phase item N.{X-1} — a flat wrapper shell-out (`--depth deep --fix --promote`) behind the recursion-breaker skip guard

TASK FOLDER: ${TASK_DIR}
  research/   [list each research file and its topic]
  qa/         [list analyst/QA reports]

[If Open Questions exist:]
OPEN QUESTIONS (documented in task file):
  - [question 1]
  - [question 2]

SUMMARY:
[Brief description of what the task will accomplish]

TO EXECUTE:
  /task ${TASK_DIR}${TASK_ID}.md
================================================================
```

**Multi-track result format:**

```text
================================================================
       TASK FILE BUILD COMPLETE ([N] TRACKS)
================================================================

--- Track 1: [goal] ---
TASK FILE: .dev/tasks/to-do/TASK-RF-track-1-YYYYMMDD-HHMMSS/TASK-RF-track-1-YYYYMMDD-HHMMSS.md
TEMPLATE: [01/02] | ITEMS: [X] | PHASES: [N] | BATCH: [N]
GATES: research=[PASS/FAIL] | structural=[PASS/FAIL] | alignment=[PASS/FAIL] | qualitative=[PASS/FAIL]
REFLECT: pre=[PASS coverage=0.94 depth=standard tcs=22 | FAIL | SKIPPED no-spec] | post=[final-phase item, executor-run]

--- Track 2: [goal] ---
TASK FILE: .dev/tasks/to-do/TASK-RF-track-2-YYYYMMDD-HHMMSS/TASK-RF-track-2-YYYYMMDD-HHMMSS.md
TEMPLATE: [01/02] | ITEMS: [X] | PHASES: [N] | BATCH: [N]
GATES: research=[PASS/FAIL] | structural=[PASS/FAIL] | alignment=[PASS/FAIL] | qualitative=[PASS/FAIL]
REFLECT: pre=[PASS coverage=0.94 depth=standard tcs=22 | FAIL | SKIPPED no-spec] | post=[final-phase item, executor-run]

TASK FOLDERS:
- .dev/tasks/to-do/TASK-RF-track-1-YYYYMMDD-HHMMSS/ (research/ + qa/)
- .dev/tasks/to-do/TASK-RF-track-2-YYYYMMDD-HHMMSS/ (research/ + qa/)

TO EXECUTE:
  /task .dev/tasks/to-do/TASK-RF-track-1-YYYYMMDD-HHMMSS/TASK-RF-track-1-YYYYMMDD-HHMMSS.md
  /task .dev/tasks/to-do/TASK-RF-track-2-YYYYMMDD-HHMMSS/TASK-RF-track-2-YYYYMMDD-HHMMSS.md
================================================================
```

**Overall status logic:**

- **Success**: ALL tracks produced task files
- **Partial**: Some tracks produced task files, some failed/skipped
- **Failed**: ALL tracks failed

---

## Agent Prompt Templates

This section contains prompt templates and summaries for the agents the skill spawns. For agents with inline prompts in A.8, A.10, and A.10.5, this section provides a structural summary with references to the authoritative inline prompt. The orchestrator passes track-specific context (goal, scope, file paths) via template variables.

### Researcher Agent Prompt (general-purpose)

Spawn via `Agent` tool with `subagent_type: "general-purpose"`, `mode: "bypassPermissions"`.

```text
You are a research agent for the task-builder skill.

YOUR SPECIFIC RESEARCH TOPIC: [TOPIC_TYPE — e.g., "File Inventory", "Patterns & Conventions"]
YOUR SCOPE: [specific directories, files, or areas to investigate from scope map]
YOUR FOCUS: [what specifically to investigate and document within your scope]

TRACK GOAL: [goal for this track]
USER PROVIDED: [list specifics the user gave]
USER DID NOT SPECIFY: [list what's missing — you figure it out from the codebase]

OTHER RESEARCHERS COVERING:
[List what other parallel researchers are covering so this agent knows its boundaries.]
- researcher-[other-topic]: [their scope and focus]
- researcher-[other-topic]: [their scope and focus]
Do NOT duplicate their work. Focus exclusively on YOUR topic.

ESCALATION — CRITICAL OVERRIDE:
You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, or TaskList.
You are a standalone agent invoked via the Agent tool. Return your research file path
and a brief findings summary as your final output.

YOUR RESEARCH MUST BE THOROUGH AND GRANULAR:
The task builder needs enough detail to create individual checklist items for EVERY file,
component, or iteration involved. Per MDTM template rules A3 (Complete Granular Breakdown)
and A4 (Iterative Process Structure), the builder must create individual items for each
file/component — NOT batch items like "document all 14 handlers." Your research must
provide the per-file detail that makes this possible.

[TOPIC-SPECIFIC INSTRUCTIONS — include the block matching this researcher's topic type:]

--- IF TOPIC IS "File Inventory" ---
For every relevant file in your assigned directories:
- Full relative path from project root
- File purpose (1 sentence)
- Key exports: classes, functions, constants with signatures
- Line count and complexity estimate
- Dependencies (imports from other project files)
Organize as a structured inventory table or list. The builder will create one checklist
item per file from this inventory.

--- IF TOPIC IS "Patterns & Conventions" ---
Read 3-5 representative files in the relevant area and extract:
- Naming conventions (files, classes, functions, variables)
- Code structure patterns (class hierarchy, module organization)
- Error handling approach
- Documentation/comment style
- Configuration patterns
- Testing patterns (if visible in source)
Document with specific examples from actual code (file:line references).

--- IF TOPIC IS "Integration Points" ---
For the subsystems involved in this track's goal:
- Map all imports/dependencies between modules
- Identify API contracts (function signatures, request/response schemas)
- Document configuration surfaces (env vars, config files, feature flags)
- Note cross-service communication patterns
- Identify extension points where new functionality could hook in

--- IF TOPIC IS "Doc Cross-Validator" ---
CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state, NOT necessarily current state.
For EVERY doc you read that makes architectural claims:
1. Services/components described: Verify the directory/entry point actually exists (use Glob)
2. Pipelines/call chains described: Trace at least first and last hop in actual source
3. File paths mentioned: Spot-check that referenced files exist
4. API endpoints described: Verify endpoint exists in actual router/app code

Mark EVERY doc-sourced claim with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** — code shows different implementation (describe what code shows)
- **[UNVERIFIED]** — could not find corresponding code; may be stale or planned

List all stale documentation found. This prevents the builder from creating task items
based on architecture that no longer exists.

--- IF TOPIC IS "Solution Research" ---
Use WebSearch to investigate:
1. Problem domain patterns — established approaches, expert recommendations
2. Tools & libraries — what's commonly used, open-source options, feature comparison
3. Architecture patterns — how others solve this type of problem
4. Project fit — alignment with project constraints (check CLAUDE.md for tech stack)

For each finding: source URL, key information, relevance rating (HIGH/MEDIUM/LOW),
how it relates to our codebase. Codebase is source of truth — external research
supplements but never overrides verified code findings.

--- IF TOPIC IS "Template & Examples" ---
1. Read the MDTM template specified for this track:
   - If template 02: .claude/templates/workflow/02_mdtm_template_complex_task.md
   - If template 01: .claude/templates/workflow/01_mdtm_template_generic_task.md
2. Read PART 1 completely — note all rules, especially A3 (Complete Granular Breakdown)
   and B2 (self-contained item pattern)
3. Check .dev/tasks/to-do/ for existing task folder examples — note effective patterns
4. Document: required sections, item format, common pitfalls, template-specific features
   (e.g., L1-L6 handoff patterns for template 02)

--- IF TOPIC IS "Data Flow Tracer" ---
Trace how data enters, transforms, and exits the relevant subsystem:
- Entry points (API endpoints, event handlers, scheduled tasks)
- Data transformations (what functions process the data, in what order)
- Storage/persistence (database writes, file outputs, cache updates)
- Exit points (API responses, events emitted, files written)
Document with actual function signatures and file:line references.

--- IF TOPIC IS "Test & Verification" ---
Investigate testing infrastructure for the relevant area:
- Existing test files and what they cover
- Test framework and patterns used (fixtures, mocking, factories)
- Coverage gaps — what's tested vs what isn't
- Verification approaches for the type of output this track produces
- CI/CD test integration (how tests are run in pipeline)
--- END TOPIC-SPECIFIC INSTRUCTIONS ---

INCREMENTAL FILE WRITING PROTOCOL (MANDATORY):
1. FIRST ACTION: Create your output file at ${TASK_DIR}research/[NN]-[topic-slug].md
   with this header:
   ```markdown
   # Research: [Your Topic]
   **Topic type:** [type]
   **Scope:** [your assigned scope]
   **Status:** In Progress
   **Date:** [today]
   ---
   ```

2. As you investigate each file/component, IMMEDIATELY append findings using Edit.
   Do NOT accumulate in context and one-shot at the end.
3. When finished, update Status to "Complete" and append a summary section.

EVIDENCE-BASED CLAIMS ONLY:
Every finding must cite actual file paths, line numbers, function names, class names.
No assumptions, no inferences, no guessing. If you can't verify it, mark "Unverified."

STEPS:

1. Create your output file FIRST (incremental writing protocol)
2. Explore the codebase within your assigned scope
3. Write findings incrementally to your output file
4. When complete, update Status to "Complete" and append summary
5. Verify file exists by reading it back
6. Return your research file path and a brief findings summary as your final output

```text

**Orchestrator collection:** After all researcher agents return, Glob `${TASK_DIR}research/*.md` to confirm all expected files exist. Count files vs expected researcher count. If any are missing, check agent return values for errors.

### Web Research Agent Prompt (general-purpose)

Spawn via `Agent` tool with `subagent_type: "general-purpose"`, `mode: "bypassPermissions"`. Only spawned when the tier allows web agents AND the quality gate identified external knowledge gaps.

The full prompt template is embedded in **A.8.5** above. Key elements:
- Topic, codebase context, and task context filled by orchestrator
- ESCALATION block (no team context)
- Incremental writing to `${TASK_DIR}research/web-[NN]-[topic-slug].md`
- Research protocol: official docs → design patterns → implementation patterns → source reliability ratings
- Output format: descriptive headers, source URLs, HIGH/MEDIUM/LOW relevance, Key External Findings + Recommendations sections
- Codebase is source of truth — external research supplements but never overrides

### Research Analyst Agent Prompt (rf-analyst — Completeness Verification)

Spawn via `Agent` tool with `subagent_type: "rf-analyst"`, `mode: "bypassPermissions"`.

```

Perform a completeness verification of all research files for [track goal].

Analysis type: completeness-verification
LENS: completeness
YOUR LENS FOCUS: Verify that every area from the scope map has corresponding research coverage. You check BREADTH, not depth.
Research directory: ${TASK_DIR}research/
Track goal: [goal for this track]
Depth tier: [Quick/Standard/Deep]
Output path: ${TASK_DIR}qa/analyst-completeness-report.md
Assigned files: [list all .md files, or subset if partitioned]

ESCALATION — CRITICAL OVERRIDE:
You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, or TaskList.
Return your verdict, report file path, and findings summary as your final output.

Your job is to independently verify that research agents produced thorough, evidence-based
findings before the builder creates the task file. You are the analytical quality gate.

PROCESS:

1. Use Glob to find ALL research files in the research directory (*.md)
2. Read EVERY assigned research file — do not skip any
3. Apply the completeness verification checklist
4. Write your report incrementally to the output path

CHECKLIST:

1. Source files identified with paths and exports?
2. Output paths and formats clear or reasonably inferred?
3. Logical breakdown of phases/steps present?
4. Patterns and conventions documented with examples?
5. MDTM template notes present with rule references?
6. Granularity sufficient for per-file/per-component checklist items?
7. Documentation cross-validation: doc-sourced claims tagged [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]?
8. If new implementation: solution research evaluated approaches?
9. Unresolved ambiguities documented (not silently skipped)?

For each criterion: PASS (with evidence) or FAIL (with specific gaps).

VERDICTS:

- PASS: All checks pass, no critical gaps
- FAIL: Critical gaps exist (list each with specific remediation action and severity)

Write the file IMMEDIATELY with a header, then append findings incrementally.
Be adversarial — your job is to find problems, not confirm things work.

```text

### Research Analyst Agent Prompt (rf-analyst — Cross-Validation)

A.8 Agent 2. Spawn via `Agent` tool with `subagent_type: "rf-analyst"`, `mode: "bypassPermissions"`. See **A.8** for full inline prompt.

- Lens focus: Cross-validates findings BETWEEN research files — checks for contradictions, inconsistencies, and conflicting claims across different researchers' outputs
- Output: `${TASK_DIR}qa/analyst-cross-validation-report.md`
- Adversarial stance and ESCALATION block (no team context)

### Research Depth Agent Prompt (rf-qa-qualitative — Research Depth)

A.8 Agent 5. Spawn via `Agent` tool with `subagent_type: "rf-qa-qualitative"`, `mode: "bypassPermissions"`. See **A.8** for full inline prompt.

- Lens focus: Evaluates whether research depth matches the selected tier (Quick/Standard/Deep), checks for shallow investigation signals, and verifies that research is thorough enough for per-file/per-component task items
- Output: `${TASK_DIR}qa/qa-research-depth-report.md`
- `fix_authorization: false` (report-only), adversarial stance, ESCALATION block

### Research QA Agent Prompts (rf-qa — Research Gate, 2 Agents)

A.8 spawns TWO rf-qa agents with focused lenses, both with `fix_authorization: false`. See **A.8** for full inline prompts.

**Agent 3 — Evidence-Quality Lens (rf-qa):**
- Spawn via `Agent` tool with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`
- `fix_authorization: false` (report-only)
- Lens focus: Verifies every claim in research files is evidence-based with actual file paths, line numbers, and function names. Checks that file paths exist and code references are accurate.
- Output: `${TASK_DIR}qa/qa-research-evidence-report.md`

**Agent 4 — Gap-Detection Lens (rf-qa):**
- Spawn via `Agent` tool with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`
- `fix_authorization: false` (report-only)
- Lens focus: Identifies coverage gaps, missing scope areas, unresolved contradictions, and insufficiently documented integration points. Classifies gaps by severity: CRITICAL / IMPORTANT / MINOR.
- Output: `${TASK_DIR}qa/qa-research-gap-report.md`

Both agents use adversarial stance and ESCALATION block (no team context).
Verdicts: PASS or FAIL per agent; gap-fill cycle triggered on FAIL.

### Builder Agent Prompt (rf-task-builder — Task File Creation)

Spawn via `Agent` tool with `subagent_type: "rf-task-builder"`, `mode: "bypassPermissions"`.

The complete BUILD_REQUEST template is embedded in **A.9** above. This section documents the key elements that must be present in every builder invocation:

**Required BUILD_REQUEST fields:**
- `GOAL` — What the task file should accomplish when executed
- `WHY` — Context for why this task is needed
- `TASK_ID_PREFIX` — Always `TASK-RF` for this skill
- `TEMPLATE` — `01` (simple) or `02` (complex), selected by orchestrator
- `DOCUMENTATION STALENESS WARNINGS` — From doc cross-validator findings
- `RESEARCH DIR` — `${TASK_DIR}research/` with listing of all research files
- `QUALITY GATE RESULTS` — Analyst and QA report locations
- `OPEN QUESTIONS` — Unresolvable ambiguities from research/gate
- `GRANULARITY REQUIREMENT` — Per-file/per-component items mandate
- `ESCALATION` — No team context override block
- `INCREMENTAL TASK FILE WRITING` — Mandatory incremental writing protocol
- `TASK FILE LOCATION` — `${TASK_DIR}${TASK_ID}.md`

**COMMON PHASE PATTERNS** (included in BUILD_REQUEST to guide the builder):

The builder creates task files for ARBITRARY requests. These common patterns provide a framework — the builder adapts based on research notes and request scope:

| Pattern | Phases | When to Use |
|---------|--------|-------------|
| **Simple Creation** | Preparation → Implementation → Verification → Completion | Creating files with known inputs/outputs (config, scripts, simple docs) |
| **Discovery-Heavy** | Preparation → Research → Quality Gate → Implementation → Testing → Completion | When codebase exploration is needed before implementation |
| **Refactoring** | Analysis → Refactoring → Testing → Validation → Completion | Restructuring existing code or files |
| **Documentation** | Preparation → Deep Investigation → Synthesis → Assembly → Validation → Completion | Creating comprehensive documents from multiple sources |
| **Feature Build** | Preparation → Design → Implementation → Testing → Integration → Review → Completion | Building new features with tests and integration |

**PROHIBITED_ACTIONS** (included in BUILD_REQUEST):
- Do NOT use SendMessage, TaskCreate, TaskUpdate, TaskList, TeamCreate, or TeamDelete
- Do NOT broadcast TASK_READY — return the file path as final output
- Do NOT create batch items — individual items per file/component
- Do NOT one-shot the task file — use incremental writing

### Task File Validation QA Agent Prompts (rf-qa — 2-Agent Serialized Fix)

A.10 uses TWO rf-qa agents with focused structural lenses, both with `fix_authorization: false`, followed by a serialized fix round. See **A.10** for full inline prompts.

**Agent 1 — B2 Self-Containment Lens:**
- Spawn via `Agent` tool with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`
- `fix_authorization: false` (report-only)
- Lens focus: Validates that every checklist item follows the B2 self-contained pattern (context + action + output + verification + completion gate)
- Output: `${TASK_DIR}qa/qa-task-validation-b2-report.md`

**Agent 2 — Phase Structure/Ordering Lens:**
- Spawn via `Agent` tool with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`
- `fix_authorization: false` (report-only)
- Lens focus: Validates phase structure, ordering, dependencies, and template conformance
- Output: `${TASK_DIR}qa/qa-task-validation-structure-report.md`

**Serialized Fix Protocol (after both agents report):**
1. Consolidate findings from both reports into `${TASK_DIR}qa/qa-task-validation-consolidated.md`
2. Spawn ONE fix agent (`fix_authorization: true`) with consolidated findings to apply all fixes
3. Verification round to confirm fixes applied correctly

- Both agents use adversarial stance and ESCALATION block (no team context)
- Verdict: PASS or FAIL per agent; overall PASS requires both agents PASS

### Research-Alignment Validation Agent Prompt (rf-analyst -- Task-Research-Alignment)

A.10.25 uses ONE rf-analyst agent to cross-validate the task file against the research files. See **A.10.25** for full inline prompt.

- Spawn via `Agent` tool with `subagent_type: "rf-analyst"`, `mode: "bypassPermissions"`
- Lens focus: Verifies every significant research finding has a corresponding task file item, and no task items fabricate actions not grounded in research
- Output: `${TASK_DIR}qa/qa-task-research-alignment-report.md`
- Adversarial stance and ESCALATION block (no team context)
- This is the 5th agent in the combined task-integrity gate (A.10 + A.10.25 + A.10.5 = 5 agents per I19)

### Qualitative Validation Agent Prompts (rf-qa-qualitative — 2-Agent Serialized Fix)

A.10.5 uses TWO rf-qa-qualitative agents with focused operational lenses, both with `fix_authorization: false`, followed by a serialized fix round. See **A.10.5** for full inline prompts.

**Agent 1 — Operational-Correctness Lens:**
- Spawn via `Agent` tool with `subagent_type: "rf-qa-qualitative"`, `mode: "bypassPermissions"`
- `fix_authorization: false` (report-only)
- Lens focus: Validates that task items are operationally correct — commands will work, file paths are valid, verification steps are meaningful, and the task can be executed as written
- Output: `${TASK_DIR}qa/qa-qualitative-operational-report.md`

**Agent 2 — QA-Gate-Sufficiency Lens:**
- Spawn via `Agent` tool with `subagent_type: "rf-qa-qualitative"`, `mode: "bypassPermissions"`
- `fix_authorization: false` (report-only)
- Lens focus: Validates that QA gates in the generated task file meet minimum requirements — minimum 6 agents per gate, lens-focused prompts, serialized fix authorization, MDTM M3 pattern. REJECTION RULE: If ANY QA gate has fewer than 6 agents, verdict is FAIL with severity CRITICAL.
- Output: `${TASK_DIR}qa/qa-qualitative-sufficiency-report.md`

**Serialized Fix Protocol (after both agents report):**
1. Consolidate findings into `${TASK_DIR}qa/qa-qualitative-consolidated.md`
2. Spawn ONE fix agent (`fix_authorization: true`) with consolidated findings
3. Verification round to confirm fixes applied correctly

---

## Output Structure

This is what the generated MDTM task file looks like — NOT a tech reference document, but the task file that the builder produces:

```markdown
---
id: "TASK-RF-<subject>-YYYYMMDD-HHMMSS"
title: "[Task Title]"
description: "[Brief description of what the task accomplishes]"
status: "🟡 To Do"
type: "🔧 Refactor"  # or 📝 Documentation, ✨ Feature, etc.
priority: "🔼 High"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "orchestrator"
template_schema_doc: ".claude/templates/workflow/0[1|2]_mdtm_template_[generic|complex]_task.md"
estimation: "[estimated duration]"
task_type: static
start_commit: "<git merge-base HEAD <integration-branch>, captured at build time — the O1 wrapper's audit base when --base is omitted>"
executor_model_class: "<executor model-class alias, e.g. sonnet — passed to reflect as --executor-model for anti-self-confirmation>"
# reflect_post: written back by the `superclaude reflect run` wrapper at execution time — leave room, do NOT hand-author or lock.
related_docs:
- path: "[relevant file]"
  description: "[why it's relevant]"
tags:
- "[tag1]"
- "[tag2]"
---

# [Task Title]

> **Frontmatter population (O1 wrapper gate keys, contract §6):** at build time the builder MUST capture `start_commit` as `git merge-base HEAD <integration-branch>` (resolve `<integration-branch>` from `git symbolic-ref --short refs/remotes/origin/HEAD`, falling back to whichever of `origin/master`/`origin/main` exists; pass it explicitly when the project integrates onto a differently-named branch) — this is the O1 wrapper's audit base when `--base` is omitted. It MUST also record `executor_model_class` (the executor's model-class alias, e.g. `sonnet`) so reflect can exclude the executor from its reviewer panel. `reflect_post:` is left as a room comment — the wrapper writes it back; never hand-author or lock it.

## Task Overview

[1-2 paragraphs describing what the task accomplishes and why]

## Key Objectives

- [Objective 1]
- [Objective 2]
- [Objective 3]

## Prerequisites & Dependencies

- [Prerequisite 1]
- [Prerequisite 2]

---

## Phase 1: [Phase Name]

- [ ] **1.1 — [Step Title]**
  - **Context**: [What the executor needs to know]
  - **Action**: [Exactly what to do]
  - **Output**: [What gets created/modified]
  - **Verification**: [How to confirm it worked]
  - **Completion gate**: [When this item is done]

- [ ] **1.2 — [Step Title]**
  ...

---

## Phase N: [Final Phase — includes completion items]

- [ ] **N.{X-1} -- Independent post-execution reflection gate (wrapper shell-out)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per the reflect-wrapper contract, the canonical POST gate is a flat `superclaude reflect run` Bash shell-out: the wrapper internally runs reflect's POST audit as a disjoint `claude --print` subprocess (the executor-disjoint context that prevents self-rubber-stamping per `feedback_sc_reflect_vs_inline_rfqa`) and, with `--fix`, runs a bounded audit→apply→re-verify loop before writing `reflect_post:` back to this file's frontmatter itself.
  - **Action**: Ensure new task artifacts are staged so the working-tree diff is complete (`git add -A` — the wrapper's audit omits never-`git add`-ed files). Then emit the recursion-breaker-guarded wrapper shell-out as a single Bash command: first the §3.2 skip guard `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi`, then `superclaude reflect run {TASK_FILE} --depth deep --fix --promote`. `{TASK_FILE}` is the absolute tasklist path (the wrapper absolutizes its positional). NO `--base` is passed — the wrapper resolves the audit base from frontmatter `start_commit` as a SINGLE ref diffed against the working tree (so uncommitted task edits ARE audited; this is why a single-ref base is correct where a `start_commit..HEAD` range would not be). Base precedence is `--base` > frontmatter `start_commit` > `git merge-base HEAD master` (contract §6). `--depth deep` is fixed (O1 forces Tier-2 fan-out); `--fix` runs the bounded auto-fix loop; `--promote` lets the `task` adapter move the tasklist dir to `done/` on a clean/auto-fixed PASS. Emit NO `--reflect`, NO `--max-turns`, NO `<base>..HEAD` range, and no agent-spawn directive of any kind (the gate is a flat shell-out, never a subagent — per NFR-7 it carries none of the nesting tokens). Consume the EXIT CODE: only `0` completes the gate (clean OR auto-fixed-and-verified); `10` (halted — human-required deviations / non-convergent fix loop), `11` (degraded — audit untrustworthy), and `2` (blocked — child crash / missing-or-bad contract) all FAIL → surface the wrapper report and HALT before Update-status-to-Done. The gate uses `superclaude reflect run` and never `/sc:task`; any re-execution uses `/task`.
  - **Output**: The wrapper returns and writes `reflect_post: {verdict, run_id, report}` back to this file's frontmatter itself (do NOT hand-author or lock it). If the wrapper surfaces unresolved deviations (exit 10/11/2), apply remediations or append them to `### Open Questions` (never delete existing items).
  - **Verification**: The wrapper exited `0`; frontmatter `reflect_post` holds a non-empty `{verdict, run_id, report}` written by the wrapper; any flagged deviations were remediated or logged to Open Questions.
  - **Completion gate**: The wrapper exited 0 (clean or auto-fixed-and-verified, and promoted). THEN the Update-status-to-Done item proceeds.

- [ ] **N.X — Update task status to Done**
  - **Context**: All phases complete.
  - **Action**: Update frontmatter: status to "🟢 Done", set completion_date.
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows "🟢 Done".
  - **Completion gate**: Task marked complete.

---

## Task Log / Notes

### Execution Log
[Entries added during execution]

### Phase Findings
[Notable outputs or issues per phase]

### Follow-Up Items
[Items discovered during execution that need separate tasks]
```

---

## Task File Validation Checklist

The QA agents (A.10 + A.10.25 + A.10.5) validate the generated task file against these criteria:

- [ ] Frontmatter properly populated (id, title, status, created_date, related_docs)
- [ ] All planned phases present as checklist items
- [ ] Items follow B2 self-contained pattern (context + action + output + verification + completion gate)
- [ ] No nested checkboxes or standalone context-reading items
- [ ] Granularity: individual items per file/component, no batch items
- [ ] Agent prompts fully embedded in subagent-spawning items (not "see SKILL.md")
- [ ] Parallel spawning instructions included for research/QA phases
- [ ] Partitioning guidance included when file counts may exceed thresholds
- [ ] Evidence-based file paths (not fabricated or hypothetical)
- [ ] No items based on [CODE-CONTRADICTED] or [UNVERIFIED] findings
- [ ] Open questions and remaining gaps documented
- [ ] Phase dependencies logical (no circular or missing)
- [ ] Task completion items inside final phase (anti-orphaning)
- [ ] Task Log section present at bottom
- [ ] Reasonable item count for scope
- [ ] QA gates have minimum 6 agents each (3 rf-qa + 3 rf-qa-qualitative) with lens-focused prompts
- [ ] QA gates use serialized fix authorization (report-only first, single fix agent, verification)
- [ ] QA gates follow MDTM M3 lens-based sequence pattern
- [ ] Source fidelity gate present when output exceeds 500 lines (MDTM M4 pattern)
- [ ] TB-Add-1: No `TBD`/`TODO`/`FIXME` tokens and no title-only items (5-field schema enforced)
- [ ] TB-Add-3: Each blocked item references its blocking Open Question by index in Context
- [ ] TB-Add-4: Item-to-item dependencies form a DAG (no circular item-level references)
- [ ] TB-Add-5: XL/multi-file items either split into subtasks or carry justifying comment
- [ ] TB-Add-6: Uniform `Verify: ...` prefix and consistent Acceptance Criteria form
- [ ] TB-Add-7: Every `## Execution Context` "Source areas:" entry reappears in at least one item Context; block contains no file:line citations (INACTIVE if no Execution Context block)
- [ ] TB-Add-8: Every per-item Context referencing a code surface carries a file:line citation OR an `<!-- evidence-absence: ... -->` comment (PR-01 INV-015 scope-confinement)
- [ ] POST reflect item present and positioned penultimate (immediately before Update-status-to-Done) when POST_REFLECT_GATE is ENABLED; the item must be the FLAT wrapper shell-out form (`superclaude reflect run … --depth deep --fix --promote` wrapped in the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard, consuming the exit code so only `0` proceeds), NFR-7-clean (no agent-spawn / nesting tokens), and emitting no `--reflect`/`<base>..HEAD`. MALFORMED if omitted, or if it emits the legacy self-run reflect-subagent form or a human-handoff/HALT form.

---

## Task File Content Rules

| Rule | Do | Don't |
|------|-----|-------|
| Self-contained items | Each item has context + action + output + verification | Items that say "see above" or "continue from previous" |
| Granularity | Individual item per file, component, or agent | Batch items like "process all 14 handlers" |
| Agent prompts | Fully embedded in each spawning item | References to "see SKILL.md" or "use the standard prompt" |
| File paths | Actual verified paths from research | Hypothetical or fabricated paths |
| Parallel spawning | Explicit "spawn in SAME message" instructions | Implicit assumption of parallelism |
| Incremental writing | "Create file first, then append" in every file-producing item | One-shot file creation |
| Phase dependencies | Explicit ordering: "after Phase N completes" | Implicit ordering relying on execution order |
| Verification clauses | "ensuring..." clause with measurable criteria | Vague "verify it works" |

---

## Critical Rules (Non-Negotiable)

1. **Codebase is the source of truth.** Code > docs > web. Web research and internal documentation supplement but never override verified code findings. Internal docs describe intent or historical state — NOT necessarily current state.

2. **Evidence-based claims only.** Every finding must cite actual file paths, line numbers, function names. No assumptions, no inferences, no guessing. If unverifiable, mark as "Unverified."

3. **Gap-driven web research.** Do not web search everything up front. First investigate the codebase thoroughly, identify specific gaps, then target web research at those gaps.

4. **Documentation is not verification.** Internal docs describe intent or planned state. A doc saying "Service X exists at path Y" does not prove it exists. Only reading actual source code proves it. Tag doc-sourced claims with [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED].

5. **Preserve research artifacts.** Research files, analyst reports, and QA reports persist after the task file is built. They serve as the evidence trail. Do NOT delete intermediate files.

6. **Report all uncertainty.** If something is unclear, ambiguous, or requires judgment, document it in Open Questions. Do not silently pick one interpretation and present it as fact.

7. **Quality gates are mandatory.** Minimum 5 agents at the research gate (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative), minimum 5 agents at task validation (2 rf-qa + 2 rf-qa-qualitative + 1 rf-analyst per I19 intermediate gate floor), with A.10 handling structural lenses, A.10.25 handling research-alignment, and A.10.5 handling content lenses. Do not skip verification to save time. Uncaught errors compound — bad research becomes a bad task file. Generated task files must also contain adequate QA — minimum 6 agents per gate enforced during A.10.5. Every retry loop (research gate, A.10, A.10.5, RESEARCH_NEEDED, MALFORMED, per-gate cycles inside rf-task-builder and rf-qa) is governed by the **Retry Monotonicity Protocol** (PR-02) -- monotonicity guard + regression detection halt oscillation BEFORE the existing iteration cap fires. The guards strengthen the gate, never loosen it.

8. **No one-shotting files.** Every file creation follows incremental writing: Write header first, Edit to append sections. NEVER accumulate content in context and attempt a single large Write.

9. **Partitioning thresholds.** When >6 research files exist, partition across all 3 agent types: 4 rf-analyst + 4 rf-qa + 2 rf-qa-qualitative = 10 agents (2 lenses x 2 partitions per type). When task files have >15 checklist items, partition qualitative validation across phase subsets. Prevents context overload in gate agents.

10. **Default tier is Standard.** Upgrade to Deep when scope demands it (20+ files, multiple subsystems, multi-track). Downgrade to Quick only for genuinely narrow requests (<5 files, single concern).

11. **Multi-track isolation.** Failure in one track MUST NOT prevent other tracks from completing. Each track is independent — failed tracks are reported alongside successful ones.

12. **Builder mediation has separate retry counters.** RESEARCH_NEEDED (max 2 rounds) and MALFORMED (max 2 rounds) are tracked independently. A builder that needs more research twice and then produces a bad file gets 4 total invocations, not 2.

13. **No team infrastructure.** This skill uses the Agent tool exclusively. NEVER use TeamCreate, TeamDelete, SendMessage, TaskCreate (with team_name), or TaskUpdate. All agents receive ESCALATION blocks overriding their team-based defaults.

14. **Task file actionability.** The generated task file must be specific enough that the `/task` executor can process every item without external context — each item must be self-contained with context, action, output, verification, and completion gate.

15. **Anti-orphaning.** Task completion items (update status to Done, write task summary) MUST be inside the final phase of the generated task file, never in a separate Post-Completion section. If the final phase includes downstream skill offers (e.g., "create a TDD from this PRD"), those items MUST come AFTER all task-completion actions, MUST be marked `NON-BLOCKING`, and MUST NOT gate task completion. Only major critical issues halt task execution.

16. **QA gates in generated task files.** When the BUILD_REQUEST specifies QA_GATE_REQUIREMENTS of FINAL_ONLY or PER_PHASE, the builder MUST encode corresponding QA gate checklist items in the generated task file following MDTM M3 (lens-based QA sequence), M4 (source fidelity gate), and I21 (source-document fidelity gate applicability) patterns. Each final-document QA gate must meet the I22 minimum for its qa_intensity level (lite: 3, standard: 7, full: 6+ per I19); each intermediate gate (research-gate, synthesis-gate) must have MINIMUM 5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative) with lens-focused prompts per I19 agent count floors. Agents use serialized fix authorization per I20 (report-only first, then single fix agent, then verification). The builder must evaluate I21 to determine when M4 fidelity gates are mandatory (output >500 lines or source-material transformation). QA gate items must be explicit `- [ ]` checklist items with fully embedded lens-specific prompts. A generated task file that omits required QA gates OR has any final-document gate with fewer agents than the I22 minimum OR any intermediate gate with fewer than 5 agents is a MALFORMED output rejected during A.10.5.

17. **Validation in generated task files.** When the BUILD_REQUEST specifies VALIDATION_REQUIREMENTS, the builder MUST encode corresponding validation checklist items in the generated task file. Validation items must be placed AFTER the phase they validate and BEFORE the next phase begins. A task file with implementation items but no validation items (when VALIDATION_REQUIREMENTS is non-empty) is a MALFORMED output.

18. **Testing in generated task files.** When the BUILD_REQUEST specifies TESTING_REQUIREMENTS other than NONE or N/A, the builder MUST encode testing checklist items in the generated task file. Testing items must specify: test file paths, test commands, coverage thresholds (if applicable), and verification that tests pass. Testing items are placed after implementation items and before QA gate items. A generated task file that requires testing items (TESTING_REQUIREMENTS is not NONE or N/A) but omits them is a MALFORMED output.

19. **No scope/cost-anxiety pauses during execution.** Once a task file begins executing (via /task or any execution loop), the executor MUST process every item sequentially to completion. It MUST NOT pause mid-execution to present the user with options like "stop here and review, or continue to phase N?" or to flag scope/cost/time concerns. Scope is established at task file creation time. Cost is committed when the user invokes execution. The only permitted mid-execution halts are: all items blocked by the same unrecoverable issue, phase-gate QA failing 3 fix cycles, or an item output fundamentally invalidating the rest of the task. "This will take a while" / "Phase N is expensive" / "the user might want to review" are NOT valid halt reasons. Pausing for these reasons violates the F1 loop discipline and the skill's trust model.

20. **POST reflect gate in generated task files.** When the BUILD_REQUEST specifies `POST_REFLECT_GATE: ENABLED`, the builder MUST emit, as the penultimate item of the final phase (immediately before the `Update task status to Done` item, preserving anti-orphaning per the validation checklist), a FLAT wrapper shell-out item: a single Bash command that runs `superclaude reflect run {TASK_FILE} --depth deep --fix --promote` wrapped in the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker skip guard (contract §2/§3.2). The item consumes the wrapper's EXIT CODE — only `0` lets Update-status-to-Done proceed; `10`/`11`/`2` FAIL and surface the wrapper report. The wrapper itself runs reflect's POST audit as an executor-disjoint subprocess and writes `reflect_post:` back to frontmatter, so the gate item MUST NOT halt for a human or defer to a separate session, and MUST NOT hand-author `reflect_post`. The gate command uses `superclaude reflect run`, and `/task` (never `/sc:task`) for any re-execution. A generated task file that omits the POST reflect item when `POST_REFLECT_GATE: ENABLED`, or that emits the legacy self-run reflect-subagent form or a human-handoff/HALT form instead of the wrapper shell-out, is a MALFORMED output.

**Precedence rule:** When a BUILD_REQUEST contains both SKILL PHASES TO ENCODE and QA_GATE_REQUIREMENTS, the SKILL PHASES TO ENCODE field is authoritative. QA_GATE_REQUIREMENTS serves as a structured summary and quick reference. For the standalone task-builder (which has no SKILL PHASES TO ENCODE), QA_GATE_REQUIREMENTS is the sole authority for QA gate encoding.

---

## Reflect Depth (Deterministic TCS)

The PRE reflect gate (A.10.7) derives reflect's `--depth` from a **Tasklist Complexity Score (TCS)**: a pure-arithmetic score computed from observable signals on the finished MDTM file + BUILD_REQUEST + spec. (The O1 POST gate does NOT consume the TCS-derived depth — it is a wrapper shell-out fixed at `--depth deep`; see O4.) No inference is used except a single bounded tiebreaker within +/-4 TCS of a band edge (see below). Each signal carries a **frozen extraction rule (FER)** so two implementers compute the same integer from the same inputs.

### TCS Signals

| # | Signal | Frozen extraction rule (deterministic) | Why it predicts audit complexity | Weight |
|---|--------|----------------------------------------|----------------------------------|--------|
| S1 | **Distinct files touched** | Apply regex `(?:[\w.-]+/)+[\w.-]+\.[\w]+` to the MDTM body, **excluding fenced code blocks and the `### Open Questions` section**; lowercase, strip a trailing `:\d+` line suffix, dedupe by exact string. S1 = size of the deduped set. | Breadth of the surface reflect must re-ground and re-Read | ×3 |
| S2 | **Distinct subsystems** | From the S1 deduped set, take **exactly the first 2 path segments** (or all segments if the path has <2 dir segments) as the subsystem key; dedupe. S2 = count of distinct keys. | Cross-cutting changes are where drift/regression hide | ×4 |
| S3 | **FR/NFR count in spec** | If `--spec` known: count **distinct** `FR-\d+`/`NFR-\d+` IDs in the spec file (an `FR-1` cited 5× counts once). Else 0. | Each requirement is a coverage row reflect must map | ×2 |
| S4 | **Inter-task dependencies** | Count occurrences of the fixed dependency-token set `{after Phase \d+, depends_on:}` (case-insensitive, those literal forms only — no open-ended "explicit item ref" inference) across all items. | Dependency depth → more verdict-matrix coupling | ×2 |
| S5 | **Human-decision / Open-Question-blocked items** | Count **distinct** `OQ-\d+` (or `Open Question \d+`) tokens that appear in a checklist item's Context line AND have a matching entry under the tasklist's `### Open Questions` section. If a `### Open Questions` section exists but no in-Context index references, fall back to the count of non-empty `### Open Questions` entries. | Each is a decision-point reflect must check did NOT auto-resolve | ×5 |
| S6 | **Risk/refactor class (file-level)** | Read the single frontmatter `type:` field, **first stripping any surrounding quotes and leading emoji + whitespace before matching** (so `type: "🔧 Refactor"` normalizes to `Refactor`); S6 = **1 if the normalized value matches a refactor/remediation-class token** (`Refactor`, `Remediation`, or `Code Remediation`, case-insensitive — covering the `🔧`/`♻️`/`🔨 Refactor` and `🔧 Remediation` quoted-emoji variants), **else 0**. A 0-or-1 file-level signal, not a per-item count. | Regression-class deviations force reflect Tier-2 escalation | ×4 |

**S4 token-set note (trimmed):** the dependency-token set is exactly `{after Phase \d+, depends_on:}`. The broader 4-token form is trimmed: `blockedBy:` has zero occurrences in the generated-tasklist corpus (inert) and `after N\.\d+` is dropped, leaving the two live literal forms.

### The TCS Formula

```text
TCS = 3*S1 + 4*S2 + 2*S3 + 2*S4 + 5*S5 + 4*S6
```

All S* are non-negative integers read directly from the tasklist/spec; the formula is pure arithmetic. Human-decision (S5) and risk (S6) carry the highest weights because they are exactly the classes that flip reflect to Tier 2 (make it non-vacuous).

### TCS Threshold Table (TCS -> `--depth`)

| TCS range | reflect `--depth` | reflect tier reached | Rationale |
|-----------|-------------------|----------------------|-----------|
| **TCS <= 12** | `quick` | Tier 1 only | Small, single-subsystem, no human-decision/risk items. A single grounded pass suffices. |
| **13 <= TCS <= 34** | `standard` | Tier 1, escalate-by-rubric | Moderate breadth; reflect's own rubric decides if it needs T2. |
| **TCS >= 35** | `deep` | Tier 2 (forced) | Cross-subsystem, dependency-heavy, or carries human-decision/risk items. |

### TCS Hard Overrides (deterministic, take precedence over the band)

- **O1: Any `S5 > 0` (human-decision item) => floor `--depth standard`.** A decision or open-question item must get at least the rubric-escalation path.
- **O2: `S6 = 1` (file-level refactor/remediation `type:`) => force `--depth deep`.** Matches reflect's own unconditional-T2 rule for regression-class surfaces.
- **O3: Item-count cap:** if checklist item count > 40 (single-track > 50) => floor `--depth standard` even if TCS is low (a large tasklist is never "quick" to audit).
- **O4: POST-gate depth is fixed `deep` (HARD RULE, no exceptions):** the O1 POST wrapper shell-out always emits `--depth deep` (Tier-2 heterogeneous fan-out per contract §2). This trivially satisfies the historical floor that the POST depth never be `quick` — `--depth quick` disables reflect's regression-escalation rubric, and the POST gate audits executed code, which is exactly where that escalation matters most. The TCS-derived depth is consumed by the PRE call ONLY (the PRE call may still use `quick`, since no diff exists pre-execution); it is NOT threaded into the POST item.

Within +/-4 TCS of a band edge (the span an S2 +/-1 disagreement can traverse), the orchestrator may apply one bounded inference, "are these N FER-distinct dirs truly distinct *logical* subsystems?", recorded as `tcs_boundary_inference: {applied, from, to, reason}` in the sign-off block for auditability. Outside the +/-4 windows, no inference is permitted.

---

## Research Quality Signals

### Strong Investigation Signals

- Specific file paths with line numbers and function signatures
- Data flow traced end-to-end (entry → processing → output)
- Integration points mapped with API contracts
- Gaps are specific and actionable ("missing test coverage for X in file Y")
- Doc-sourced claims tagged [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]
- Analyst + QA both return PASS on first attempt

### Weak Investigation Signals (Redo)

- Vague descriptions without file references ("the system handles authentication")
- Assumptions stated as facts ("this service probably calls...")
- Missing gap analysis — no gaps found is a red flag
- No cross-references between research files
- Doc-sourced claims without verification tags
- Repeated gate failures (2+ rounds)

### When to Spawn Additional Agents

- Critical gaps identified by analyst/QA that existing research doesn't cover
- Contradictions between research files that need resolution
- Scope larger than initially estimated — new subsystems discovered
- Web research needed for external knowledge gaps (only if tier allows)

---

## Artifact Locations

| Artifact | Location |
|----------|----------|
| MDTM task file (output) | `${TASK_DIR}${TASK_ID}.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| Research files | `${TASK_DIR}research/[NN]-[topic].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Gap-fill research | `${TASK_DIR}research/[NN]-gap-fill.md` |
| Analyst reports (research gate) | `${TASK_DIR}qa/analyst-completeness-report.md`, `analyst-cross-validation-report.md` |
| QA reports (research gate) | `${TASK_DIR}qa/qa-research-evidence-report.md`, `qa-research-gap-report.md`, `qa-research-depth-report.md` |
| QA reports (task validation) | `${TASK_DIR}qa/qa-task-validation-b2-report.md`, `qa-task-validation-structure-report.md`, `qa-task-validation-consolidated.md` |
| QA task-research-alignment report | `${TASK_DIR}qa/qa-task-research-alignment-report.md` |
| QA reports (qualitative review) | `${TASK_DIR}qa/qa-qualitative-operational-report.md`, `qa-qualitative-sufficiency-report.md`, `qa-qualitative-consolidated.md` |

Research and QA report files persist after the task file is built — they serve as the evidence trail for all claims and enable future re-investigation.

---

## Session Management

This skill may span multiple sessions. The task folder and its contents persist on disk.

**Resume detection:** At session start, check `.dev/tasks/to-do/` for `TASK-RF-*/` folders from the current request.

**State-to-resume-point table:**

| State on Disk | Resume Point |
|---------------|-------------|
| No task folder | A.2 (start fresh) |
| research-notes.md In Progress | A.3 (continue scope discovery) |
| research-notes.md Complete, no research files | A.5 (review research sufficiency) |
| research/ has complete files, qa/ empty | A.8 (quality gate) |
| qa/ has all 5 A.8 report files (`analyst-completeness-report.md` + `analyst-cross-validation-report.md` + `qa-research-evidence-report.md` + `qa-research-gap-report.md` + `qa-research-depth-report.md`), no task file | A.9 (spawn builder) |
| Task file exists, no validation reports (`qa-task-validation-b2-report.md` + `qa-task-validation-structure-report.md`) | A.10 (structural validation) |
| Task file + structural validation (`qa-task-validation-b2-report.md` + `qa-task-validation-structure-report.md`), no research-alignment report (`qa-task-research-alignment-report.md`) | A.10.25 (research-alignment validation) |
| Task file + structural + research-alignment validation, no qualitative reports (`qa-qualitative-operational-report.md` + `qa-qualitative-sufficiency-report.md`) | A.10.5 (qualitative validation) |
| Task file + all validation/qualitative/alignment reports | A.11 (present results) |

**Resume check clarification:** Resume checks verify file EXISTENCE on disk, not verdict content. If files exist, the orchestrator re-reads the verdicts inside to determine whether to proceed or re-run the gate. |

**At session end:**

- All files should be on disk in the task folder
- Note which step was reached if interrupted
- The user can resume by re-invoking the skill with the same goal

---

## Multi-Track Handling

This section is unique to the task-builder skill — the canonical document skills don't support multi-track.

### Track Determination Rules

A request contains **independent work streams** when ALL of these are true:

- Each track has its own distinct goal (a subset of the overall request)
- Each track operates on different source files or concerns
- Each track produces different output files
- No track depends on another track's outputs

**Split into multiple tracks when you see:**

- Multiple unrelated deliverables: "Create docs for handlers AND add tests for services"
- Distinct output areas: different output directories, different file types
- Explicit enumeration of independent items where A, B, C don't depend on each other
- Independent components: "update both the frontend and backend"

**Do NOT split (keep as single track) when:**

- Work items build on each other sequentially
- All items contribute to a single cohesive output
- Items share source context that must be understood holistically
- You're unsure whether items are truly independent

**Default: single track.** Only split when independence is clear. **Maximum: 5 tracks.**

### Per-Track State Tracking

The orchestrator maintains a per-track state map internally:

```text
Track 1: research=[pending|done], gate=[pending|pass|fail], build=[pending|done], validate=[pending|pass|fail]
Track 2: ...
```

No shared task list needed — the orchestrator tracks state from agent return values and output files.

### Parallel Execution

- All researchers across all tracks spawned in one message
- Per-track quality gates run as each track's research completes
- As each track's gate passes, immediately spawn its builder (don't wait for other tracks)

### Track Isolation

Failure in one track MUST NOT prevent other tracks from completing. If a track fails:

- Track quality gate fails after max gap-fill rounds → mark track as FAILED
- Track builder returns RESEARCH_NEEDED after max rounds → mark track as FAILED with "insufficient research"
- Track builder produces unfixable task file → present it with issues documented

Mixed-status results use the multi-track format from A.11 with per-track status.

### Naming Conventions

| Artifact | Single Track | Multi-Track (Track T) |
|----------|-------------|----------------------|
| Task folder | `TASK-RF-<subject>-YYYYMMDD-HHMMSS/` | `TASK-RF-track-T-YYYYMMDD-HHMMSS/` |
| Researcher agents | `researcher-[topic]` | `researcher-T-[topic]` |
| Analyst agent | `analyst-research` | `analyst-research-T` |
| QA agent | `qa-research-gate` | `qa-research-gate-T` |
| Builder agent | `builder` | `builder-T` |

---

## Updating an Existing Task File

To modify or regenerate a previously-built task file:

1. Read the existing task file to understand what's already built
2. Re-run scope discovery for changed areas only
3. Spawn targeted researchers for the changes (not full research)
4. Re-run quality gate on new research
5. Spawn builder with the updated research + existing task file as context (builder can modify or regenerate)
6. Validate the updated task file
