---
name: task-builder
description: "Build MDTM task files from user requests via parallel codebase research, quality gates, and automated task file creation. Use this skill when the user wants to build a task file, create a task, create an MDTM task, build a task for a specific goal, or when the user provides a BUILD_REQUEST file path. Trigger on phrases like 'build a task file for...', 'create a task for...', 'rf task builder', 'build a task for...', 'create an MDTM task for...', 'task-builder for...', or when the user references a BUILD-REQUEST*.md file."
---

# RF Task Builder

Creates MDTM task files by researching the actual codebase with parallel agents, running quality gates, and spawning the `rf-task-builder` agent to produce a validated, ready-to-execute task file. This skill uses Rigorflow's Agent tool for all subagent spawning — no agent teams, enabling concurrent task builds.

**How it works:** The skill performs scope discovery, spawns parallel researcher agents via the Agent tool, runs rf-analyst + rf-qa quality gates on the research, optionally spawns web research agents, then spawns the `rf-task-builder` agent with a structured BUILD_REQUEST to create the MDTM task file. After the builder returns, rf-qa validates the task file in task-integrity mode. The skill presents the validated task file path and execution command to the user.

This skill stops after task file creation. There is no Stage B — the user reviews the task file and executes it with `/task [path]` when ready.

## Why This Process Works

Task files go wrong when built from memory, shallow exploration, or unverified assumptions. This skill forces every task item through evidence-based codebase research — parallel agents read actual source files, trace actual dependencies, and document actual behavior with file paths and line numbers.

The multi-phase structure (scope discovery → parallel research → **analyst verification** → **QA gate** → builder → **task file validation** → **qualitative review**) prevents four common failure modes:
- **Context rot** — By isolating each research topic in its own subagent with its own output file, no single agent needs to hold the entire investigation in context. Findings are written to disk incrementally, not accumulated in memory.
- **Shallow coverage** — By spawning many parallel agents (each focused on one topic slice from the scope map), the research goes deep on every aspect simultaneously rather than skimming across everything sequentially. Minimum 3 researchers per track, scaling to 8 for complex scopes.
- **Hallucinated content** — By separating research (what exists) from task file creation (what to do about it), each phase can be verified independently. The builder only works from verified research files, not from memory or inference. Research claims are evidence-based with file paths and line numbers.
- **Uncaught quality drift** — Dedicated `rf-analyst`, `rf-qa`, and `rf-qa-qualitative` agents provide independent verification at three critical gates: after research (rf-analyst completeness check + rf-qa evidence quality), after task file creation (rf-qa task-integrity structural validation), and after structural QA passes (rf-qa-qualitative task-qualitative operational validation — verifying the plan would actually succeed if executed). The QA agents assume everything is wrong until independently verified — zero-trust verification prevents rubber-stamping.

The research artifacts persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and provide the evidence trail for all task file items.

---

## Input

The skill needs four pieces of information to produce a well-researched task file. The first is mandatory; the rest are optional but improve output quality.

1. **GOAL — what task to build** (mandatory) — What the task file should accomplish when executed. This can be a natural language description, a structured request, or a pointer to source files/directories. Examples: "Create API documentation for all handlers", "Refactor the auth middleware and add tests", "Build a new feature for project templates".

2. **WHY — context** (strongly recommended) — Why this task is needed and what constraints apply. This shapes the task file's scope and verification criteria. Examples: "we need docs for onboarding new engineers", "the current auth is non-compliant with new security requirements", "product wants this for the Q2 release".

3. **WHERE — source directories** (optional, saves significant research time) — Specific directories, files, or subsystems the task involves. Prevents researchers from spending time on irrelevant areas. Examples: `backend/app/api/v1/`, `frontend/app/wizard/`, `backend/app/services/auth_service.py`.

4. **BUILD_REQUEST file path** (optional) — A `.md` file containing a structured build request. Used for programmatic invocation by other skills or when the request is too complex for a one-line prompt. The file should contain GOAL, WHY, OUTPUTS, CONTEXT, and optionally TEMPLATE preference.

### Effective Prompt Examples

**Strong — explicit goal with scope and deliverables:**
> Build a task file to create API documentation for all 14 handlers in `backend/app/api/v1/`. Output docs to `docs/api/` as individual markdown files per handler.

**Strong — build request file:**
> Build a task from `.dev/tasks/to-do/existing-doc-template-convergence/BUILD-REQUEST-TASK-FILE-REMEDIATION.md`

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

This skill is invoked directly by users via `/task-builder [request]`. Other document-producing skills (tech-reference, prd, tdd, operational-guide, repo-cleanup, readme) spawn the `rf-task-builder` **agent** via the Agent tool during their Stage A — they use the agent definition at `.claude/agents/rf-task-builder.md`, not this skill. The agent and the skill share the same builder logic but operate in different contexts: the agent receives a BUILD_REQUEST from the orchestrating skill, while this skill IS the orchestrator.

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

All persistent artifacts go into the task folder at `.dev/tasks/to-do/TASK-RF-YYYYMMDD-HHMMSS/`.

**Variable reference block:**
```
TASK_ID:     TASK-RF-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/
QA:          ${TASK_DIR}qa/
```

Note: This skill does NOT produce synthesis files, reviews, or final documents. It produces a task file + research artifacts + QA reports. There are no `synthesis/` or `reviews/` subfolders.

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}${TASK_ID}.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Analyst reports | `${TASK_DIR}qa/analyst-completeness-report.md` |
| QA research gate reports | `${TASK_DIR}qa/qa-research-gate-report.md` |
| QA task validation report | `${TASK_DIR}qa/qa-task-validation-report.md` |
| QA qualitative review | `${TASK_DIR}qa/qa-qualitative-review.md` |

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
8. Research quality gate — rf-analyst + rf-qa in parallel via Agent tool, with gap-fill cycle if needed (A.8)
9. Optional web research — only if tier allows web agents AND quality gate identified external knowledge gaps (A.8.5)
10. Spawn the `rf-task-builder` agent via Agent tool with structured BUILD_REQUEST (A.9)
11. Task file structural validation — rf-qa in task-integrity mode via Agent tool, with fix authorization (A.10)
12. Task file qualitative validation — rf-qa-qualitative in task-qualitative mode via Agent tool, with fix authorization (A.10.5)
13. Present results — task file path, quality gate summary, recommended batch size, execution command (A.11)

If a task folder already exists for this request (from a previous session), skip to the appropriate step based on artifact state:
- Research files complete but no QA reports → skip to A.8 (quality gate)
- QA reports pass but no task file → skip to A.9 (spawn builder)
- Task file exists but no validation report → skip to A.10 (structural validation)
- Task file + structural validation report but no qualitative report → skip to A.10.5 (qualitative validation)
- Task file + both validation reports exist → skip to A.11 (present results)

---

## Stage A: Task File Creation Pipeline

### A.1: Check for Existing Task Folder

Before creating a new task folder, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `TASK-RF-*/` folder related to this request
2. If found, check the artifact state to determine the resume point:
   - If `research/` has complete research files but `qa/` has no analyst/QA reports → skip to A.8 (quality gate)
   - If `qa/` has passing analyst/QA reports but no task file in `${TASK_DIR}` → skip to A.9 (spawn builder)
   - If task file exists but no `qa-task-validation-report.md` in `qa/` → skip to A.10 (structural validation)
   - If task file + `qa-task-validation-report.md` exist but no `qa-qualitative-review.md` in `qa/` → skip to A.10.5 (qualitative validation)
   - If task file and validation report both exist → skip to A.11 (present results)
   - If `research-notes.md` exists with `Status: Complete` → skip to A.5 (review sufficiency)
   - If `research-notes.md` exists with `Status: In Progress` → resume A.3 scope discovery
3. If no matching task folder exists → continue with A.2

### A.2: Parse & Triage

Break the user's request into structured components:

- **GOAL**: What the task file should accomplish when executed
- **WHY**: Why this task is needed (if stated)
- **OUTPUTS**: Specific deliverables, paths, formats (if stated)
- **CONTEXT**: Files, directories, components mentioned (if any)

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
```
Researcher 1 (File Inventory): Scan backend/app/api/v1/ — catalog all handler files, classes, methods, line counts
Researcher 2 (Patterns & Conventions): Read 3-4 handlers in detail — extract naming, error handling, response patterns
Researcher 3 (Integration Points): Trace handler dependencies — services, models, schemas they import/use
Researcher 4 (Doc Cross-Validator): Read existing docs/ for handler documentation — cross-validate against actual handler code
Researcher 5 (Template & Examples): Read MDTM templates + check .dev/tasks/to-do/ for prior task folder examples
```

**Example assignment for "Build a new feature with tests":**
```
Researcher 1 (File Inventory): Scan directories where feature will live — catalog existing files, identify insertion points
Researcher 2 (Patterns & Conventions): Study similar features already implemented — extract patterns to follow
Researcher 3 (Integration Points): Map how the new feature connects to existing services, APIs, database
Researcher 4 (Solution Research): WebSearch for best practices, library options, architecture patterns
Researcher 5 (Template & Examples): Read MDTM templates + existing task files for similar work
Researcher 6 (Test & Verification): Study existing test patterns, fixtures, mocking approaches
Researcher 7 (Data Flow Tracer): Trace how data flows through related subsystems
```

3. **Produce per-track scope map:**
```
TRACK [T] SCOPE MAP:
  Relevant directories: [list]
  Key files found: [count and top examples]
  Patterns/classes identified: [list]
  Existing docs/templates: [list]
  Estimated complexity: [low/medium/high]
```

Create the task folder: `.dev/tasks/to-do/TASK-RF-YYYYMMDD-HHMMSS/` with subfolders `research/` and `qa/`. For multi-track: `.dev/tasks/to-do/TASK-RF-track-T-YYYYMMDD-HHMMSS/` per track.

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

```
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
```
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
```
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
```
For the subsystems involved in this track's goal:
- Map all imports/dependencies between modules
- Identify API contracts (function signatures, request/response schemas)
- Document configuration surfaces (env vars, config files, feature flags)
- Note cross-service communication patterns
- Identify extension points where new functionality could hook in
```

**Doc Cross-Validator:**
```
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
```
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
```
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
```
Trace how data enters, transforms, and exits the relevant subsystem:
- Entry points (API endpoints, event handlers, scheduled tasks)
- Data transformations (what functions process the data, in what order)
- Storage/persistence (database writes, file outputs, cache updates)
- Exit points (API responses, events emitted, files written)
Document with actual function signatures and file:line references.
```

**Test & Verification:**
```
Investigate testing infrastructure for the relevant area:
- Existing test files and what they cover
- Test framework and patterns used (fixtures, mocking, factories)
- Coverage gaps — what's tested vs what isn't
- Verification approaches for the type of output this track produces
- CI/CD test integration (how tests are run in pipeline)
```

**Orchestrator collection:** After all Agent calls return, the orchestrator has all research file paths from agent outputs. List research files in `${TASK_DIR}research/` to verify completeness. No message-based coordination needed.

### A.8: Research Quality Gate

Spawn rf-analyst and rf-qa in parallel to independently verify research completeness before allowing task file creation.

**Spawn analyst + QA in parallel** — two Agent calls in one message:

```
Agent 1:
  subagent_type: "rf-analyst"
  mode: "bypassPermissions"
  description: "Research completeness verification"
  prompt: |
    ANALYSIS_TYPE: completeness-verification
    SCOPE: Research files for task-builder track [T]

    RESEARCH DIR: ${TASK_DIR}research/
    TRACK GOAL: [goal for this track]
    ASSIGNED FILES: [list all .md files in research/]

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

Agent 2:
  subagent_type: "rf-qa"
  mode: "bypassPermissions"
  description: "Research quality gate"
  prompt: |
    QA_MODE: research-gate
    fix_authorization: false

    **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

    RESEARCH DIR: ${TASK_DIR}research/
    TRACK GOAL: [goal for this track]
    ASSIGNED FILES: [list all .md files in research/]

    Zero-trust verification of research quality:
    1. Are claims evidence-based (file paths, line numbers, function names)?
    2. Any unsupported assertions or assumptions stated as facts?
    3. Are [CODE-CONTRADICTED] or [UNVERIFIED] claims properly flagged?
    4. Coverage gaps — are there obvious areas the researchers missed?
    5. Are findings actionable for a task builder (not too vague, not too abstract)?

    OUTPUT FILE: ${TASK_DIR}qa/qa-research-gate-report.md
    Write the file IMMEDIATELY with a header, then append findings incrementally.
    Conclude with: VERDICT: PASS or FAIL, and severity-rated issues if FAIL.
    Severity ratings: CRITICAL (blocks builder), IMPORTANT (reduces quality), MINOR (nice-to-fix).

    ESCALATION: You have NO team context. Do NOT use SendMessage.
    Return your verdict and report file path as your final output.
```

**Partitioning:** When >6 research files per track, spawn 2 analyst + 2 QA instances (4 agents total), each with assigned_files subsets. Merge reports after all return.

**Gate evaluation:** Read both analyst and QA reports. Gate PASSES when both verdicts are PASS with ALL findings resolved regardless of severity.

**Gap-fill cycle:** If the gate fails:
1. Compile all CRITICAL, IMPORTANT, and MINOR issues from analyst + QA reports into a structured gap list
2. Spawn targeted gap-fill researcher(s) via Agent tool (`subagent_type: "general-purpose"`) with specific gaps to fill
3. After gap-fill, re-run analyst + QA on the NEW research files only
4. **Maximum 3 gap-fill rounds** (aligned with canonical skills and rf-qa agent definition)
5. After 3 rounds, proceed with remaining gaps as Open Questions in the task file

**Cross-track validation (multi-track only):** After gate evaluation, cross-validate that no two tracks have overlapping scope that would produce conflicting task files.

**DNSP Synthetic Finding Protocol (PR-03 — paradigm-neutral, the BASE proposal of this release):**

When the orchestrator spawns rf-analyst / rf-qa / rf-qa-qualitative with partition `assigned_files` slices, a single partition agent that exhausts its escalation ladder (WebSearch → /rf:opinion → team-lead, per rf-task-researcher.md and the agent definitions) AND fails the existing single retry (Bucket A SKILL.md "retry once before reporting error" baseline) MUST NOT silently weaken the gate or abort the entire pipeline. Instead, the orchestrator synthesises a **HIGH-severity finding** with this emission contract:

- `severity: HIGH`
- `source: "synthetic-dnsp"`
- `affected_range`: the failed agent's `assigned_files` slice (verbatim)
- `evidence`: path to the failed agent's spawn log (or a `<!-- evidence-absence: spawn-log-unavailable -->` stub citing the absence)
- `recommendation`: "Manual review required — partition agent failed twice on this range"

Then the orchestrator **merges with the remaining N-1 partition agents' findings** rather than aborting. This preserves the parallel-research invariant (N-1 partitions still complete) and the zero-trust QA invariant (the gap is surfaced HIGH-severity, never silently passed).

**All-agents-fail guard.** If zero partition agents succeeded, the orchestrator escalates normally per the existing retry-then-Open-Questions flow — DNSP does NOT fire (a HIGH synthetic for every partition is informationally equivalent to escalation and adds noise).

**Dedup key (composition with PR-02 Retry Monotonicity, INV-012).** Two synthetic findings emitted across consecutive retry cycles for the SAME `(assigned_files_range, escalation_ladder_exhaust_point)` collapse into ONE finding annotated `found N times`. This prevents the dedup case from reading as a regression to the PR-02 monotonicity guard (the same partition failed the same way twice is dedup, not regression). Two synthetics with DIFFERENT escalation_ladder_exhaust_points (e.g., partition A failed via WebSearch exhaustion at cycle N, then via /rf:opinion timeout at cycle N+1) are DISTINCT findings.

This protocol applies symmetrically to:
- A.8 research-gate partition spawns of rf-analyst + rf-qa
- A.10 task-integrity partition spawns of rf-qa (when partitioning is invoked)
- A.10.5 qualitative partition spawns of rf-qa-qualitative

### A.8.5: Optional Web Research

**Skip this step unless BOTH conditions are true:**
1. The tier allows web agents (Standard: 0-1, Deep: 1-2, Quick: 0)
2. The quality gate's analyst/QA reports identified **external knowledge gaps** that codebase research cannot fill (e.g., best practices for a technology, library API documentation, design pattern recommendations, MDTM template conventions from external sources)

If neither condition is met, proceed directly to A.9.

**Spawning:** Use the Agent tool with `subagent_type: "general-purpose"`, `mode: "bypassPermissions"`. Spawn 1-2 web research agents in parallel, each investigating a specific gap identified by the quality gate.

**Prompt format:**
```
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

**BUILD_REQUEST format for the subagent prompt:**

```
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

    QA_GATE_REQUIREMENTS: [Default: FINAL_ONLY for Template 01, PER_PHASE
      for Template 02. NONE = no QA gates in generated task file. FINAL_ONLY
      = include a final QA validation phase before task completion.
      PER_PHASE = include QA gates after each major phase. When QA gates are
      required, the task file must include checklist items that spawn
      rf-analyst and/or rf-qa to verify phase outputs before proceeding.
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

    EXECUTION_CONTEXT_REQUIREMENTS: [OPTIONAL signal (API-001-M2) controlling
      the `## Execution Context` block emission in the generated MDTM. Governs
      DM-001-frozen (T01.13 / D-0011 § 1) emitters defined in the EXECUTION
      CONTEXT BLOCK section below. Values:
      - AUTO (default) — builder emits the block when BUILD_REQUEST exposes
        rollup signal (≥3 distinct named source areas inferable from research
        findings). Fully-populated form renders all 3 labeled bullets
        (References, Source areas, Key constraints). Minimal form (GOAL-only
        BUILD_REQUEST) degenerates to References-only with Source areas and
        Key constraints bullets ABSENT (not blank-but-present).
      - REQUIRED — builder MUST emit the block. The degraded References-only
        form is permitted when only GOAL is populated; suppressing the block
        entirely is a MALFORMED output.
      - SUPPRESS — builder MUST NOT emit the block. Per-item Context fields
        remain unchanged regardless. Used for thin / throwaway task files.
      Omission of this field implies AUTO. Strictly additive — when absent
      or AUTO, the M1-frozen 15-field BUILD_REQUEST behavior is preserved
      byte-identical. Failure mode: MALFORMED retry max-2 (Critical Rule #12
      and the MALFORMED flow at SKILL.md A.9 mediation) applies when the
      builder violates this signal — e.g., emitting the block under SUPPRESS,
      or omitting the block under REQUIRED.]

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
    - qa/qa-research-gate-report.md — zero-trust quality assessment
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
       - ## Execution Context (OPTIONAL — see EXECUTION CONTEXT BLOCK below)
    2. THEN: Append each phase ONE AT A TIME using Edit tool.
       One phase per Edit call. Verify each Edit succeeded.
    3. LAST: Append the Task Log section after all phases are written.

    EXECUTION CONTEXT BLOCK (OPTIONAL, TASK-LEVEL ROLL-UP):
    Emit an `## Execution Context` section immediately after frontmatter
    (before # Title body content) when BUILD_REQUEST exposes enough rollup
    signal — typically when ≥3 distinct source areas can be inferred from
    research files. This is a READING aid for the executor, NOT a substitute
    for per-item Context fields.

    Signal control (API-001-M2): the `EXECUTION_CONTEXT_REQUIREMENTS`
    BUILD_REQUEST field overrides the AUTO heuristic when set. REQUIRED
    forces emission (degraded References-only form permitted on GOAL-only
    input); SUPPRESS forbids emission (per-item Context fields untouched);
    AUTO / omission applies the rollup-signal heuristic below. Violation of
    the signal (emit-under-SUPPRESS or omit-under-REQUIRED) is MALFORMED
    output and triggers the max-2 retry flow at SKILL.md A.9.

    The block has exactly three sub-bullets, in this order. Each is
    produced by a distinct emitter governed by the DM-001 contract-freeze
    (T01.13 / D-0011 § 1). Apply the rules below verbatim — they ARE the
    implementation (R-033 / R-034 / R-035).

    - **References emitter (DM-001.References — R-033):** A single
      labeled bullet `**References:**` followed by `R-###: <ref-line>`
      entries separated by `; `. `###` is a zero-padded ordinal starting
      at `001`, assigned in stable input order: BUILD_REQUEST GOAL
      first, then WHY, then each related-doc ID in BUILD_REQUEST source
      order. `<ref-line>` is the verbatim text of the source field — do
      not rewrite or summarize; strip only trailing whitespace. ALWAYS
      present whenever the block is emitted; never blank, never omitted
      (under minimal-BUILD_REQUEST degradation, GOAL alone produces at
      least `R-001`).
    - **Source areas emitter (DM-001.SourceAreas — R-034):** A single
      labeled bullet `**Source areas:**` followed by named modules or
      packages, comma-separated (e.g., "rf-qa agent prompts",
      "task-builder skill body"). Emit only when ≥3 distinct named areas
      can be inferred from the research files; otherwise OMIT the bullet
      entirely (do not emit a blank-but-present line). **No-file-paths
      guard (NFR-CONV.3 hidden-input determinism — MANDATORY
      pre-emission scan):** the rendered bullet MUST satisfy
      `grep -cE "src/|/.*:[0-9]+"` returning 0. If any hit is found,
      reject the candidate, rewrite area names to remove paths and `:NN`
      line numbers (rename a candidate like `src/superclaude/agents/rf-qa.md`
      to `rf-qa agent prompt`), and re-scan. Specific `path.py:NN`
      references belong in per-item Context fields and `research/*.md`,
      never here.
    - **Key constraints emitter (DM-001.KeyConstraints — R-035):** A
      single labeled bullet `**Key constraints:**` followed by 1–3
      entries separated by `; `. Entries are pulled **verbatim** from
      BUILD_REQUEST `QA_GATE_REQUIREMENTS` /
      `VALIDATION_REQUIREMENTS` / `TESTING_REQUIREMENTS` (priority
      order) or from the highest-severity invariants in research
      findings — do NOT paraphrase. Bounded strictly to 1–3 entries:
      when >3 candidates exist, keep the top 3 by priority order and
      drop the rest (do not concatenate beyond 3). OMIT the bullet
      entirely when BUILD_REQUEST and research findings produce no
      clear constraint shortlist.

    Scope-confinement rule (PROTECTS evidence-bound-item invariant): the
    "no specific file paths" rule applies ONLY to this header. Per-item
    Context fields and `research/*.md` files MUST retain file:line
    citations — they are the evidence venue. rf-qa enforces this via
    TB-Add-7 (header source areas reappear in items) and TB-Add-8
    (per-item Context fields cite file:line or carry a justified absence
    comment).

    Degradation rule (R-038 — minimal BUILD_REQUEST → References-only):
    When BUILD_REQUEST is "minimal" — defined as GOAL is the only populated
    rollup-signal field (WHY may be empty or duplicate GOAL; no
    related_docs; no QA_GATE_REQUIREMENTS / VALIDATION_REQUIREMENTS /
    TESTING_REQUIREMENTS entries; <3 inferable source areas across all
    research files) — the block degenerates to a single `**References:**`
    bullet. The Source areas and Key constraints bullets are **absent**
    from the rendered block (not present-and-blank, not stub-bulleted).
    The block heading `## Execution Context` remains; the
    `<!-- OPTIONAL header ... -->` reader-aid comment remains; only the
    two omitted bullets are physically gone from the output. If even
    GOAL-derived References cannot be produced (truly empty BUILD_REQUEST),
    OMIT the entire block — heading included.

    Header-wide hidden-input guard (R-039 — NFR-CONV.3 enforcement at the
    block boundary, MANDATORY post-assembly scan): after the three
    emitters have run and the bullets have been concatenated into the
    candidate block, run `grep -cE "src/|/.*:[0-9]+"` against the byte
    range from the `## Execution Context` heading line through the
    closing `---` separator. The count MUST be 0. The per-emitter
    Source-areas guard at the rule above is a first line of defense; this
    header-wide guard is the final boundary check, catching any
    BUILD_REQUEST-derived path leak in References (verbatim GOAL/WHY text)
    or Key constraints (verbatim invariant text) that the per-emitter
    rules cannot reach. On any hit (count ≥ 1), DO NOT emit the block —
    rewrite the offending bullet to remove the path / `:NN` reference
    (e.g., a GOAL line mentioning `src/foo/bar.py:42` becomes "the foo
    module" or "the bar handler"), re-run the assembly, and re-scan.
    Allow at most one rewrite cycle; if the scan still hits, OMIT the
    entire block and surface a `header-leak-suppressed` annotation in
    the builder's return value. The check applies uniformly to the
    fully-populated 3-bullet form and to the degraded References-only
    form.

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
    6. Create the task file using PART 2 structure (incremental writing)
    7. Return the task file path as your final output
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

**Retry Monotonicity Protocol (PR-02 — strengthens zero-trust QA against oscillation):**

Every retry loop in task-builder (RESEARCH_NEEDED, MALFORMED, the A.8 research-gate gap-fill loop, the A.10 / A.10.5 fix cycles, rf-task-builder per-gate fix-cycles in rf-task-builder.md, and rf-qa's 3-fix-cycle in rf-qa.md) MUST apply two stop conditions BEFORE the existing iteration cap fires:

1. **Monotonicity guard.** Record the count of remaining gate failures `F_n` at the end of each cycle `n`. If `F_{n+1} >= F_n` — i.e., the failure count did NOT strictly shrink — HALT and escalate with `non-convergent: |F_n| -> |F_{n+1}|` in the gate report. The guard fires only on strict non-shrink; legitimate slow convergence (`F_{n+1} = F_n - 1`) continues to the existing cap.
2. **Regression detection.** Record the set of items that PASSED at the end of each cycle. If any item that PASSed at cycle `n` is FAILing at cycle `n+1`, HALT immediately with `regression detected: Item X.Y passed at cycle N, failed at cycle N+1`. Regression detection fires only on previously-PASS items — legitimate refinement of still-FAILing items does not trigger.

**Precedence rule.** When both conditions trigger in the same cycle, regression takes precedence — the escalation message names the regressing item; the monotonicity halt is implicit.

**Independent counters.** Each retry counter keeps its own monotonicity history. RESEARCH_NEEDED, MALFORMED, research-gate gap-fill, A.10 fix cycle, A.10.5 fix cycle, and any per-gate cycles in rf-task-builder/rf-qa each track `F_n` and PASS-set state separately. Counters are NEVER collapsed (preserves the "tracked independently" property documented in Critical Rule #12).

**Composition with PR-03 DNSP synthetic findings (INV-012 acceptance criterion).** Synthetic findings emitted by the DNSP protocol (PR-03) COUNT as failures for the `|F_n|` monotonicity comparison — they are real, citable evidence items. BUT a synthetic finding with the same `(assigned_files_range, escalation_ladder_exhaust_point)` dedup key appearing across consecutive cycles is a DEDUP case, NOT a regression — the same partition failed the same way twice; the regression-detection logic must compare by dedup key, not by raw finding count, when synthetic-dnsp items are involved. Two synthetic findings with identical dedup keys collapse into one with a "found N times" note (cf. PR-03 dedup behavior).

**Single-cycle case.** If the first cycle PASSes, no second cycle runs; both guards are no-ops by construction.

### A.10: Task File Validation

After the builder returns a task file path, validate the task file before presenting to the user.

**Spawn rf-qa:** Use the Agent tool with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

**QA prompt:**
```
QA_MODE: task-integrity
fix_authorization: true

TASK FILE: [path to the task file the builder created]
TEMPLATE USED: [01 or 02]
TRACK GOAL: [goal for this track]
RESEARCH DIR: ${TASK_DIR}research/

ESCALATION — CRITICAL OVERRIDE:
You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate,
or TaskList. You are a standalone agent invoked via the Agent tool. Return
your verdict and report file path as your final output.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

Validate the task file against template requirements:
1. YAML frontmatter complete and well-formed?
2. All mandatory sections present per template?
3. Checklist items are self-contained (context + action + output + verification + completion gate)?
4. Granularity check: no batch items like "do all X" — each file/component has its own item?
5. Evidence-based: items reference specific file paths, not vague descriptions?
6. No items based on [CODE-CONTRADICTED] or [UNVERIFIED] findings?
7. Open Questions and remaining gaps documented (if any were passed from quality gate)?
8. Phase dependencies are logical (no circular or missing dependencies)?
9. Estimated item count is reasonable for the scope?

Structural Gate Additions (TB-Add-1 through TB-Add-7, imported from sc:tasklist 17-point pre-write gate per CB-3 per-check classification — see rf-qa agent definition for full rationale):
10. TB-Add-1: Placeholder scan — no item contains `TBD`/`TODO`/`FIXME` and no item is title-only (5-field schema enforced).
11. TB-Add-2: Item count bounds — track ≥3 and ≤40 items; single-track ≥3 and ≤50. ADVISORY-fail until empirical calibration completes (≥10 completed tasks in `.dev/tasks/done/` across ≥3 task_types).
12. TB-Add-3: Clarification adjacency — each blocked item references its blocking Open Question by index in Context.
13. TB-Add-4: Circular dependency detection — item-to-item dependencies form a DAG; no cycles.
14. TB-Add-5: Granularity / XL splitting — items flagged complex/multi-file are either split into subtasks or carry a justifying comment.
15. TB-Add-6: Confidence/Verification format consistency — uniform `Verify: ...` prefix and `- ✅`/`- [x]` Acceptance Criteria form.
16. TB-Add-7: Execution Context source areas reappear in items — every "Source areas:" entry in the `## Execution Context` block reappears in at least one item's Context field; the block itself contains NO specific file:line references. INACTIVE if no Execution Context block exists.
17. TB-Add-8: Per-item Context evidence binding — every item Context field that references a code surface includes a file:line citation OR an `<!-- evidence-absence: ... -->` justified-absence comment. Structurally proves PR-01's "no specific paths" rule is confined to the header (INV-015 scope-confinement).

OUTPUT FILE: ${TASK_DIR}qa/qa-task-validation-report.md

Write the file IMMEDIATELY with a header, then append findings incrementally.

If fix_authorization is true and you find issues: fix them IN-PLACE in the
task file using Edit, then document what you fixed in your report.

Conclude with: VERDICT: PASS or FAIL (with list of unfixable issues if FAIL).
```

**Handling the verdict:**
- **PASS** → Proceed to A.10.5 (qualitative validation)
- **FAIL with all fixes applied** → QA fixed all issues in-place. Proceed to A.10.5.
- **FAIL with unfixable issues** → Present the issues to the user alongside the task file. Let them decide whether to proceed, fix manually, or re-run.
- **No verdict emitted (report file absent OR present but no `VERDICT:` line OR `VERDICT:` value not `PASS`/`FAIL`)** → **HALT. Do NOT spawn rf-qa-qualitative.** This operationalises the DM-005 `failure_mode: halt-A.10-before-A.10.5` lever (A.10.6, row 7). The PR-04 passthrough cannot inject a verdict that does not exist; the consumer's anti-inflation enforcement at `rf-qa-qualitative.md:766-775` requires an enumerated PASS/FAIL checklist that only the producer can publish, so proceeding without a verdict would force the consumer to fabricate verification state (an INV-019 / Self-Audit violation by construction). The orchestrator MUST: (a) check `${TASK_DIR}qa/qa-task-validation-report.md` exists on disk; (b) if absent, log `INV-002-no-producer-artifact halt-A.10-before-A.10.5 task=${TASK_DIR}` and surface the missing-report path to the user; (c) if present, grep for `^VERDICT: (PASS|FAIL)` (case-sensitive, line-anchored); if zero matches, log `INV-002-no-verdict-line halt-A.10-before-A.10.5 task=${TASK_DIR} report=${REPORT_PATH}` and surface the malformed-report path to the user with instruction to re-run rf-qa. In both cases, the pipeline stops at end-of-A.10; control does NOT pass to A.10.5; rf-qa-qualitative is NEVER invoked for that task on that cycle. The user resumes the pipeline only after rf-qa is re-run and emits a well-formed `VERDICT:` line (at which point the orchestrator restarts from "Handling the verdict" above and routes via the PASS / FAIL-with-fixes / FAIL-unfixable branch).

### A.10.5: Task File Qualitative Validation

After structural QA passes, validate that the task file would actually succeed if executed. This step catches operational issues that structural QA cannot: gates that will fail, function signatures that don't match the described modifications, downstream dependencies not updated, tests that exercise stubs instead of real artifacts, and runtime paths that break partway through.

**Spawn rf-qa-qualitative:** Use the Agent tool with `subagent_type: "rf-qa-qualitative"`, `mode: "bypassPermissions"`.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

**Building the target file list:** Before spawning, read the task file and extract ALL unique source file paths referenced by checklist items (every file that an item reads, modifies, creates, or runs a command against). This is the TARGET_FILE_LIST. Do NOT allow spot-checking — the qualitative agent must verify every target file, not a sample.

**Inherited Structural Verdict (PR-04 Gate Results Passthrough — operationalises rf-qa-qualitative rule #11):** Before spawning rf-qa-qualitative, read `${TASK_DIR}qa/qa-task-validation-report.md` (rf-qa's A.10 output). Extract the "Items Reviewed" PASS/FAIL table **contiguously** — a single span between the `## Items Reviewed` heading and the next top-level (`## `) heading — verbatim, with no editing/summarising/renaming/re-ordering. **Splice the extracted span byte-for-byte into the rf-qa-qualitative spawn prompt as a `## Inherited Structural Verdict` section, at the API-002 wire-contract position: after the TARGET FILES + PROJECT CONVENTIONS context blocks and before the ADVERSARIAL STANCE / INSTRUCTIONS directive blocks.** The orchestrator MUST also dynamically enumerate every TB-Add-* item from rf-qa.md's current checklist (do NOT hand-maintain the list — read rf-qa.md and pull the live TB-Add catalogue) so the verdict passthrough auto-picks up future structural additions (INV-010). On EVERY fix cycle re-spawn, the orchestrator MUST re-read the freshly-written `qa-task-validation-report.md` and re-inject the new verdict — never reuse a stale verdict from a prior cycle (INV-002). If `qa-task-validation-report.md` is missing or its `VERDICT:` line is absent/malformed, the upstream A.10 verdict gate has already HALTed per DM-005 `failure_mode: halt-A.10-before-A.10.5` (see "Handling the verdict" branch 4 above) — control never reaches this A.10.5 spawn step on that cycle, so there is no orchestrator-visible "omit the section and fall back" code path. The consumer agent (rf-qa-qualitative) retains independent standalone capability, but operationally FR-CONV.3 (PR-04 passthrough) + INV-002 (freshness) + INV-010 (dynamic enumeration) require a producer verdict for every spawn: the anti-inflation rule at `rf-qa-qualitative.md:766-775` depends on an enumerated checklist that only the producer can publish, and the Self-Audit obligation (INV-019) requires the consumer to declare which producer-PASS items it relied on (an impossible declaration when no producer verdict exists).

**QA prompt:**
```
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
3. **Re-extract the "Items Reviewed" span contiguously.** Apply the same single-span extraction rule from the directive above (between the `## Items Reviewed` heading and the next top-level `## ` heading). Do NOT reuse the prior cycle's extraction even if the surrounding file appears unchanged — re-extract every time.
4. **Re-enumerate the TB-Add-* catalogue (INV-010).** Re-read `rf-qa.md`'s live checklist and re-pull the TB-Add-* IDs. Do NOT reuse the prior cycle's enumeration snapshot.
5. **Re-assemble and re-splice.** Build the new `## Inherited Structural Verdict` block from the freshly-extracted span + freshly-enumerated TB-Add-* IDs. Splice it into the spawn prompt at the API-002 wire-contract position (after TARGET FILES + PROJECT CONVENTIONS; before ADVERSARIAL STANCE / INSTRUCTIONS). The cycle N+1 spawn prompt MUST contain the cycle N+1 verdict; a byte-diff of cycle N vs. cycle N+1 at the verdict-table region MUST surface the cycle N+1 content (`grep -A` on `## Inherited Structural Verdict` returns the new span).
6. **Stale-verdict-rejection (defense-in-depth).** Before issuing the spawn call, compute `sha256` of the new `## Inherited Structural Verdict` block and compare it to a `last_injected_verdict_sha256` ledger entry keyed by `${TASK_DIR}`. If the prior cycle wrote a verdict with a non-zero ledger entry AND the new sha256 equals the prior entry AND the producer-artifact witness in step 2 reports a NEW mtime/sha256, that combination is impossible under a correct re-extract — REJECT the spawn, log an `INV-002-stale-verdict-rejected` error with both witnesses, and re-run steps 2–5. (Equal witnesses + equal block sha256 is the legitimate no-op case when the producer truly did not change; only the contradiction case is rejected.)
7. **Log the re-extract.** Emit a structured log line `INV-002: re-extracted verdict for ${TASK_DIR} cycle=N+1 producer_mtime=<iso> producer_sha256=<hex8> block_sha256=<hex8>` at every fix-cycle boundary. The log is the operator-visible audit-trail proving the re-extract ran.

This procedure operationalises the `freshness_rule: INV-002-reinject-NEW` field of the DM-005 Phase Contract (A.10.6). The 2-cycle byte-diff fixture (TEST-008, T03.13) consumes log lines from step 7 and the assembled blocks from step 5 as its assertion surface.

**TB-Add catalogue enumeration (INV-010 dynamic catalogue lookup):** The TB-Add-* catalogue is sourced from `rf-qa.md`'s live "Structural Gate Additions" section at runtime — never from a hand-maintained list inside this skill. Every spawn (initial entry **and** every fix-cycle re-entry per step 4 of the freshness procedure above) MUST execute the following procedure to build the enumeration handed to the consumer:

1. **Locate `rf-qa.md`.** Resolve the path via the project's agent registry (canonical surface: `src/superclaude/agents/rf-qa.md`; mirror surface: `.claude/agents/rf-qa.md`). The canonical surface is authoritative; the mirror is consulted only when the canonical surface is unreachable.
2. **Bound the catalogue region.** Identify the `#### Structural Gate Additions` heading and treat the catalogue region as the span from that heading to the next `####`, `###`, or `##` heading (whichever comes first). Enumeration MUST be confined to this span — TB-Add tokens outside the span (e.g., illustrative references in narrative prose) do NOT contribute to the catalogue.
3. **Extract IDs.** Within the bounded span, match the regex `^[0-9]+\. \*\*TB-Add-([0-9]+):` (Python `re` flavour, MULTILINE) against the span. Each match yields one TB-Add-N ID via the captured integer N.
4. **Build the live set.** Deduplicate, sort ascending by N, and form `LIVE_TB_ADD = [TB-Add-1, TB-Add-2, …, TB-Add-K]`. K is the runtime size of the catalogue; it is never asserted against a hard-coded constant in this skill.
5. **Cross-check against the producer.** Every `TB-Add-*` row present in the freshly-extracted "Items Reviewed" span (step 3 of the freshness procedure) MUST appear in `LIVE_TB_ADD`. A row whose TB-Add-N is absent from `LIVE_TB_ADD` is an orphan (producer ran on a stale catalogue) — FAIL the spawn with `INV-010-orphan-tb-add` and halt at end-of-A.10 (re-uses the `failure_mode: halt-A.10-before-A.10.5` lever). A TB-Add-N present in `LIVE_TB_ADD` but absent from the producer table is allowed only when the producer's own report explicitly annotates it as `not-yet-implemented`; otherwise FAIL with `INV-010-missing-tb-add-row`.
6. **Forbid hard-coded enumeration in the orchestrator logic.** This A.10.5 procedure block MUST NOT itself enumerate a fixed `[TB-Add-1, …, TB-Add-K]` list as the spawn target. The directive narratives in this section reference the catalogue abstractly (via the dynamic `LIVE_TB_ADD`); only `rf-qa.md` is the source of the live IDs. (Operator self-check: grep for `TB-Add-[0-9]+` inside the A.10.5 span and confirm every match is either a regex pattern, a worked example tagged `illustrative`, or an integrated-checklist reference — never an orchestrator enumeration target.)
7. **Emit a structured log line.** Write `INV-010: enumerated TB-Add-* catalogue size=K ids=[TB-Add-1,...,TB-Add-K] source=rf-qa.md source_sha256=<hex8>` at every spawn boundary (initial entry and each fix-cycle re-entry). The log is the operator-visible audit-trail and the TEST-010 fixture's (T03.15) assertion surface.
8. **Auto-richening invariant.** Appending a new `**TB-Add-N+1: <name>` line inside the bounded catalogue region of `rf-qa.md` MUST cause `LIVE_TB_ADD` to grow by exactly one entry on the next spawn — with **zero edits** to this SKILL.md, to orchestrator code, or to any consumer-side configuration. This is the K-007 sequencing-inversion mitigation cited in `roadmap.md` R-069: FR-CONV.1 catalogue additions auto-propagate to the PR-04 passthrough.

This procedure operationalises the `enumeration_rule: INV-010-auto-pick-TB-Add` field of the DM-005 Phase Contract (A.10.6). The structural-diff fixture (TEST-010, T03.15) consumes log lines from step 7 and the LIVE_TB_ADD set assembled in step 4 as its assertion surface — adding a synthetic TB-Add-N+1 stub to `rf-qa.md`'s bounded region and asserting the cycle-2 spawn prompt auto-richens by exactly one TB-Add-N+1 row.

### A.10.6: DM-005 Phase Contract — rf-qa → rf-qa-qualitative (published row)

Standalone publication of the 10-field producer/consumer agreement that
governs the A.10 → A.10.5 inter-agent handoff. The contract was frozen
at M1 (T01.13 / D-0011 § DM-005) and is published here at M2 (T02.04 /
D-0019) as the wire reference for M3 (FR-CONV.3 / PR-04), which lands
the orchestrator-mediated spawn-prompt injection. `schema_version: 1.0.0`
is the baseline for all future inter-agent contracts emitted by this
skill — any field add, rename, semantic change, or value-type change
requires a major version bump.

This is the source-of-truth contract documentation. A.10.5 above is the
runtime implementation (verbatim Items Reviewed table embed, INV-002
freshness reinjection, INV-010 dynamic TB-Add enumeration, anti-inflation
bullet preservation, halt-on-missing-producer-artifact failure mode).

**DM-005 Phase Contract (10 fields, frozen at M1, published at M2):**

```yaml
# DM-005 — Phase Contract: rf-qa → rf-qa-qualitative
# Frozen: M1 (T01.13 / D-0011 § DM-005)
# Published: M2 (T02.04 / D-0019)
# Consumed: M3 (FR-CONV.3 / PR-04, A.10.5 spawn-prompt injection)
producer: rf-qa
consumer: rf-qa-qualitative
artifact: Inherited Structural Verdict block
schema_version: 1.0.0
delivery_semantics: at-most-once-per-cycle
freshness_rule: INV-002-reinject-NEW
enumeration_rule: INV-010-auto-pick-TB-Add
consumer_obligation: INV-019-Self-Audit
anti_inflation: preserve-766-775-byte-stable
failure_mode: halt-A.10-before-A.10.5
```

**Field-by-field semantics (1.0.0 wire ABI):**

| Field                | Wire Value                          | Meaning |
|----------------------|-------------------------------------|---------|
| producer             | `rf-qa`                             | The rf-qa agent invoked under `QA_MODE: task-integrity` (see A.10). Writes the producer artifact to `${TASK_DIR}qa/qa-task-validation-report.md`. |
| consumer             | `rf-qa-qualitative`                 | The rf-qa-qualitative agent invoked under `QA_PHASE: task-qualitative` (see A.10.5). Consumes the producer artifact via spawn-prompt injection. |
| artifact             | `Inherited Structural Verdict block`| Named block embedded under heading `## Inherited Structural Verdict` in the consumer's spawn prompt. Contents = the entire "Items Reviewed" PASS/FAIL table from the producer's report, byte-identical (verbatim copy, no editing/summarising/renaming). |
| schema_version       | `1.0.0`                             | Wire ABI version. Major-version bump REQUIRED for any field add/rename, semantic change, or value-type change. M3 implementers MUST refuse to consume artifacts with a different schema_version until a migration is recorded. |
| delivery_semantics   | `at-most-once-per-cycle`            | Exactly one verdict block is injected per consumer spawn. On fix-cycle re-spawn, the prior block is REPLACED (not appended) — see freshness_rule. |
| freshness_rule       | `INV-002-reinject-NEW`              | Orchestrator MUST re-read the freshly-written `qa-task-validation-report.md` on EVERY fix-cycle re-spawn and re-inject the NEW cycle-N verdict. Stale verdicts from prior cycles are forbidden. |
| enumeration_rule     | `INV-010-auto-pick-TB-Add`          | Orchestrator MUST dynamically enumerate every TB-Add-* item from rf-qa.md's live checklist at injection time (do NOT hand-maintain the list). Future structural additions to rf-qa.md auto-extend the verdict passthrough. |
| consumer_obligation  | `INV-019-Self-Audit`                | rf-qa-qualitative MUST emit a `## Self-Audit` section listing (a) which rf-qa PASS items it relied on AND (b) ≥1 semantic check where rf-qa PASS was insufficient and the consumer's own tool engagement was required. Reliance is not verification. |
| anti_inflation       | `preserve-766-775-byte-stable`      | The anti-inflation bullet at the canonical `rf-qa-qualitative.md:766-775` anchor MUST remain byte-identical across releases. No downstream consumer is permitted to edit, paraphrase, or wrap this bullet. |
| failure_mode         | `halt-A.10-before-A.10.5`           | If `${TASK_DIR}qa/qa-task-validation-report.md` is missing or malformed, orchestrator HALTs the pipeline at end-of-A.10 before invoking A.10.5. Passthrough is an optimisation; the consumer cannot proceed without a valid producer artifact. (When the producer artifact is present but unparseable, A.10.5 falls back to standalone rf-qa-qualitative behavior — see A.10.5 narrative.) |

**Versioning and migration:** `schema_version: 1.0.0` is frozen for the entire M2-through-M6 release window. Any change to the 10 fields above — including renaming, splitting, merging, or altering the wire value format — requires a major version bump to `2.0.0`, a corresponding entry in the release roadmap, and a migration note documenting the cycle in which old (`1.0.0`) producer artifacts stop being accepted by the consumer.

**Cross-references:**
- Runtime implementation: A.10.5 (this skill).
- Producer prompt: A.10 (this skill) + `rf-qa.md` (task-integrity mode).
- Consumer prompt: A.10.5 (this skill) + `rf-qa-qualitative.md`.
- Future consumers of `schema_version: 1.0.0` versioning baseline: every inter-agent contract emitted by this skill after M3.

### A.11: Present Results

Present the completed task file to the user with quality gate summary and execution instructions.

**Single-track result format:**

```
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
  Task qualitative validation: [PASS/FAIL] ([N] issues fixed in-place)

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

```
================================================================
       TASK FILE BUILD COMPLETE ([N] TRACKS)
================================================================

--- Track 1: [goal] ---
TASK FILE: .dev/tasks/to-do/TASK-RF-track-1-YYYYMMDD-HHMMSS/TASK-RF-track-1-YYYYMMDD-HHMMSS.md
TEMPLATE: [01/02] | ITEMS: [X] | PHASES: [N] | BATCH: [N]
GATES: research=[PASS/FAIL] | validation=[PASS/FAIL]

--- Track 2: [goal] ---
TASK FILE: .dev/tasks/to-do/TASK-RF-track-2-YYYYMMDD-HHMMSS/TASK-RF-track-2-YYYYMMDD-HHMMSS.md
TEMPLATE: [01/02] | ITEMS: [X] | PHASES: [N] | BATCH: [N]
GATES: research=[PASS/FAIL] | validation=[PASS/FAIL]

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

This section contains the complete prompt templates for every agent the skill spawns. Each prompt is self-contained — it includes all instructions the agent needs. The orchestrator passes track-specific context (goal, scope, file paths) via template variables.

### Researcher Agent Prompt (general-purpose)

Spawn via `Agent` tool with `subagent_type: "general-purpose"`, `mode: "bypassPermissions"`.

```
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
```

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
```

### Research QA Agent Prompt (rf-qa — Research Gate)

Spawn via `Agent` tool with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`.

```
**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

Perform QA verification of research completeness for [track goal].

QA phase: research-gate
fix_authorization: false
Research directory: ${TASK_DIR}research/
Analyst report: ${TASK_DIR}qa/analyst-completeness-report.md (if exists)
Track goal: [goal for this track]
Depth tier: [Quick/Standard/Deep]
Output path: ${TASK_DIR}qa/qa-research-gate-report.md
Assigned files: [list all .md files, or subset if partitioned]

ESCALATION — CRITICAL OVERRIDE:
You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, or TaskList.
Return your verdict, report file path, and findings summary as your final output.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

You are the last line of defense before the builder creates the task file. Assume
everything is wrong until you verify it.

IF ANALYST REPORT EXISTS:
1. Read the analyst's completeness report
2. Verify ALL of their coverage audit claims
3. Validate gap severity classifications
4. Check their verdict against your own independent assessment
5. Apply the 10-item Research Gate checklist

IF NO ANALYST REPORT:
Apply the full 10-item checklist independently.

10-ITEM CHECKLIST:
1. File inventory — all research files exist with Status: Complete and Summary
2. Evidence density — Verify EVERY claim in each file — verify file paths exist
3. Scope coverage — every key area from scope map examined
4. Documentation cross-validation — doc-sourced claims tagged, Verify EVERY CODE-VERIFIED claim
5. Contradiction resolution — no unresolved conflicting findings
6. Gap severity — CRITICAL (blocks builder), IMPORTANT (reduces quality), MINOR (must still be fixed)
7. Depth appropriateness — matches tier expectation
8. Integration point coverage — connection points documented
9. Pattern documentation — code patterns and conventions captured
10. Incremental writing compliance — files show iterative structure, not one-shot

VERDICTS:
- PASS: Green light for builder
- FAIL: ALL findings must be resolved. Only PASS or FAIL — no conditional pass.

Write the file IMMEDIATELY with a header, then append findings incrementally.
Zero tolerance — if you can't verify it, it fails.
```

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

**Optional BUILD_REQUEST signals (strictly-additive, M1-frozen schema preserved):**
- `EXECUTION_CONTEXT_REQUIREMENTS` (API-001-M2) — Controls the `## Execution
  Context` block emission in the generated MDTM. Values: `AUTO` (default,
  applies rollup-signal heuristic), `REQUIRED` (force emission; degraded
  References-only form permitted), `SUPPRESS` (forbid emission). Omission
  implies `AUTO`. Violation triggers MALFORMED retry max-2.

  **Rendered forms (DM-001 contract — T01.13 / D-0011 § 1):** the block has
  exactly two valid shapes; no third intermediate form exists.

  1. **Fully-populated 3-labeled-line form** (rollup signal present —
     `AUTO` with ≥3 inferable source areas, OR `REQUIRED` with sufficient
     signal). The block emits all three labeled bullets verbatim, in this
     order:
     - `**References:**` — `R-###: <ref-line>` entries separated by `; `,
       sourced from BUILD_REQUEST GOAL / WHY / related_docs in stable
       input order (R-033).
     - `**Source areas:**` — named modules or packages, comma-separated;
       NEVER specific file paths or `file:line` citations (R-034).
     - `**Key constraints:**` — 1–3 entries pulled verbatim from
       BUILD_REQUEST `QA_GATE_REQUIREMENTS` / `VALIDATION_REQUIREMENTS` /
       `TESTING_REQUIREMENTS` (priority order) or highest-severity
       research invariants (R-035).
  2. **Degraded References-only form** (R-038 — minimal BUILD_REQUEST,
     defined as GOAL is the only populated rollup-signal field with <3
     inferable source areas). The `**References:**` bullet emits;
     `**Source areas:**` and `**Key constraints:**` bullets are
     **absent from the rendered block** (not present-and-blank, not
     stub-bulleted). The `## Execution Context` heading and the
     reader-aid HTML comment remain. If even GOAL-derived References
     cannot be produced (truly empty BUILD_REQUEST), the entire block
     including heading is omitted.

  **NFR-CONV.3 hidden-input determinism (R-039 — MANDATORY for both
  rendered forms):** the rendered block, byte range from the
  `## Execution Context` heading through the closing `---` separator,
  MUST satisfy `grep -cE "src/|/.*:[0-9]+"` returning 0. The rule
  applies uniformly to the fully-populated and the degraded form; it
  is a hard precondition for emission, not a stylistic preference. On
  any hit (count ≥ 1), the builder rewrites the offending bullet to
  remove the path / `:NN` reference, re-runs assembly, and re-scans;
  at most one rewrite cycle is permitted before the block is
  suppressed with a `header-leak-suppressed` annotation. Specific
  `path.py:NN` references belong in per-item Context fields and
  `research/*.md` (the evidence venue), never in this header.

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

### Task File Validation QA Agent Prompt (rf-qa — Task Integrity)

Spawn via `Agent` tool with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`.

The complete prompt template is embedded in **A.10** above. Key elements:
- **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
- `QA_MODE: task-integrity`, `fix_authorization: true`
- ESCALATION block (no team context)
- 9-item validation checklist:
  1. YAML frontmatter complete and well-formed
  2. All mandatory sections present per template
  3. Checklist items self-contained (context + action + output + verification + completion gate)
  4. Granularity: no batch items — each file/component has its own item
  5. Evidence-based: items reference specific file paths, not vague descriptions
  6. No items based on [CODE-CONTRADICTED] or [UNVERIFIED] findings
  7. Open Questions and remaining gaps documented
  8. Phase dependencies logical (no circular or missing)
  9. Reasonable item count for the scope
- QA fixes issues in-place when authorized
- Output: `${TASK_DIR}qa/qa-task-validation-report.md`
- Verdict: PASS or FAIL (with list of unfixable issues if FAIL)

---

## Output Structure

This is what the generated MDTM task file looks like — NOT a tech reference document, but the task file that the builder produces:

```markdown
---
id: "TASK-RF-YYYYMMDD-HHMMSS"
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
related_docs:
- path: "[relevant file]"
  description: "[why it's relevant]"
tags:
- "[tag1]"
- "[tag2]"
---

# [Task Title]

## Task Overview

[1-2 paragraphs describing what the task accomplishes and why]

## Key Objectives

- [Objective 1]
- [Objective 2]
- [Objective 3]

## Prerequisites & Dependencies

- [Prerequisite 1]
- [Prerequisite 2]

## Execution Context

<!-- OPTIONAL: emit when BUILD_REQUEST yields enough rollup signal (typically ≥3 inferable source areas). This block is a task-level READING aid; per-item Context fields and research/*.md remain the evidence venue with file:line citations. The block contains NO specific path.py:NN references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** [BUILD_REQUEST GOAL verbatim; WHY summary; related-doc IDs]
- **Source areas:** [named modules/packages — e.g., "rf-qa agent prompts", "task-builder skill body" — NEVER specific file:line paths]
- **Key constraints:** [top 1-3 invariants from QA_GATE_REQUIREMENTS / VALIDATION_REQUIREMENTS / TESTING_REQUIREMENTS or research findings]

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

The QA agent (A.10) validates the generated task file against these criteria:

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
- [ ] TB-Add-1: No `TBD`/`TODO`/`FIXME` tokens and no title-only items (5-field schema enforced)
- [ ] TB-Add-2: Item count within bounds (track ≥3/≤40; single-track ≥3/≤50) — ADVISORY-fail until calibrated
- [ ] TB-Add-3: Each blocked item references its blocking Open Question by index in Context
- [ ] TB-Add-4: Item-to-item dependencies form a DAG (no circular item-level references)
- [ ] TB-Add-5: XL/multi-file items either split into subtasks or carry justifying comment
- [ ] TB-Add-6: Uniform `Verify: ...` prefix and consistent Acceptance Criteria form
- [ ] TB-Add-7: Every `## Execution Context` "Source areas:" entry reappears in at least one item Context; block contains no file:line citations (INACTIVE if no Execution Context block)
- [ ] TB-Add-8: Every per-item Context referencing a code surface carries a file:line citation OR an `<!-- evidence-absence: ... -->` comment (PR-01 INV-015 scope-confinement)

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

7. **Quality gates are mandatory.** rf-analyst + rf-qa MUST be spawned at the research gate. Do not skip verification to save time. Uncaught errors compound — bad research becomes a bad task file. Every retry loop (research gate, A.10, A.10.5, RESEARCH_NEEDED, MALFORMED, per-gate cycles inside rf-task-builder and rf-qa) is governed by the **Retry Monotonicity Protocol** (PR-02) — monotonicity guard + regression detection halt oscillation BEFORE the existing iteration cap fires. The protocol is part of zero-trust QA; the guards strengthen the gate, never loosen it.

8. **No one-shotting files.** Every file creation follows incremental writing: Write header first, Edit to append sections. NEVER accumulate content in context and attempt a single large Write.

9. **Partitioning thresholds.** When >6 research files exist, spawn multiple analyst and QA instances with assigned file subsets. Prevents context overload in gate agents.

10. **Default tier is Standard.** Upgrade to Deep when scope demands it (20+ files, multiple subsystems, multi-track). Downgrade to Quick only for genuinely narrow requests (<5 files, single concern).

11. **Multi-track isolation.** Failure in one track MUST NOT prevent other tracks from completing. Each track is independent — failed tracks are reported alongside successful ones.

12. **Builder mediation has separate retry counters.** RESEARCH_NEEDED (max 2 rounds) and MALFORMED (max 2 rounds) are tracked independently. A builder that needs more research twice and then produces a bad file gets 4 total invocations, not 2.

13. **No team infrastructure.** This skill uses the Agent tool exclusively. NEVER use TeamCreate, TeamDelete, SendMessage, TaskCreate (with team_name), or TaskUpdate. All agents receive ESCALATION blocks overriding their team-based defaults.

14. **Task file actionability.** The generated task file must be specific enough that the `/task` executor can process every item without external context — each item must be self-contained with context, action, output, verification, and completion gate.

15. **Anti-orphaning.** Task completion items (update status to Done, write task summary) MUST be inside the final phase of the generated task file, never in a separate Post-Completion section.

16. **QA gates in generated task files.** When the BUILD_REQUEST specifies QA_GATE_REQUIREMENTS of FINAL_ONLY or PER_PHASE, the builder MUST encode corresponding QA gate checklist items in the generated task file. These items must specify the QA agent type (rf-analyst, rf-qa, rf-qa-qualitative), the QA mode, the files to verify, and the pass/fail handling. A generated task file that omits required QA gates is a MALFORMED output.

17. **Validation in generated task files.** When the BUILD_REQUEST specifies VALIDATION_REQUIREMENTS, the builder MUST encode corresponding validation checklist items in the generated task file. Validation items must be placed AFTER the phase they validate and BEFORE the next phase begins. A task file with implementation items but no validation items (when VALIDATION_REQUIREMENTS is non-empty) is a MALFORMED output.

18. **Testing in generated task files.** When the BUILD_REQUEST specifies TESTING_REQUIREMENTS other than NONE or N/A, the builder MUST encode testing checklist items in the generated task file. Testing items must specify: test file paths, test commands, coverage thresholds (if applicable), and verification that tests pass. Testing items are placed after implementation items and before QA gate items. A generated task file that requires testing items (TESTING_REQUIREMENTS is not NONE or N/A) but omits them is a MALFORMED output.

**Precedence rule:** When a BUILD_REQUEST contains both SKILL PHASES TO ENCODE and QA_GATE_REQUIREMENTS, the SKILL PHASES TO ENCODE field is authoritative. QA_GATE_REQUIREMENTS serves as a structured summary and quick reference. For the standalone task-builder (which has no SKILL PHASES TO ENCODE), QA_GATE_REQUIREMENTS is the sole authority for QA gate encoding.

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
| Analyst report (research gate) | `${TASK_DIR}qa/analyst-completeness-report.md` |
| QA report (research gate) | `${TASK_DIR}qa/qa-research-gate-report.md` |
| QA report (task validation) | `${TASK_DIR}qa/qa-task-validation-report.md` |
| QA report (qualitative review) | `${TASK_DIR}qa/qa-qualitative-review.md` |

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
| research-notes.md Complete, no research files | A.7 (spawn researchers) |
| research/ has complete files, qa/ empty | A.8 (quality gate) |
| qa/ has passing reports, no task file | A.9 (spawn builder) |
| Task file exists, no validation report | A.10 (validation) |
| Task file + validation report | A.11 (present results) |

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
```
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
| Task folder | `TASK-RF-YYYYMMDD-HHMMSS/` | `TASK-RF-track-T-YYYYMMDD-HHMMSS/` |
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
