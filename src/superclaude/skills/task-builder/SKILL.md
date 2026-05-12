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

### A.10.5: Task File Qualitative Validation

After structural QA passes, validate that the task file would actually succeed if executed. This step catches operational issues that structural QA cannot: gates that will fail, function signatures that don't match the described modifications, downstream dependencies not updated, tests that exercise stubs instead of real artifacts, and runtime paths that break partway through.

**Spawn rf-qa-qualitative:** Use the Agent tool with `subagent_type: "rf-qa-qualitative"`, `mode: "bypassPermissions"`.

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

**Building the target file list:** Before spawning, read the task file and extract ALL unique source file paths referenced by checklist items (every file that an item reads, modifies, creates, or runs a command against). This is the TARGET_FILE_LIST. Do NOT allow spot-checking — the qualitative agent must verify every target file, not a sample.

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

**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

INSTRUCTIONS:
Apply the 15-item Task File Qualitative Review checklist from your agent
definition. For each checklist item that requires reading source code, read
the ACTUAL target files — do not rely on research file summaries alone.

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

7. **Quality gates are mandatory.** rf-analyst + rf-qa MUST be spawned at the research gate. Do not skip verification to save time. Uncaught errors compound — bad research becomes a bad task file.

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
