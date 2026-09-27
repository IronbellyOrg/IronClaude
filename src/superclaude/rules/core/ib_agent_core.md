---
title: "IB Agent Task Execution: Core Plan, Principles, and Standards"
description: "Consolidated core information for task execution including AI execution guidelines, orchestrator responsibilities, agent tooling principles, core principles, AI Golden Rules, and Standard AI Directives."
id: "ib-agent-core"
sidebar_position: 1
created_date: "2025-08-05"
last_updated: "2026-07-01"
version: 1.0.0
draft: false
content_status: Published
tags:
- "core-plan"
- "task-execution"
- "ai-execution"
- orchestration
- principles
- "ai-rules"
- foundational
content_type: CoreConcept
target_audience:
- Developer
- ComponentDeveloper
- SystemDesigner
- SystemArchitect
- QAEngineer
- AI
- Machine
owner: orchestrator
autogen: false
autogen_method: ""
autogen_source: []
autogen_version: ""
ai_model: ""
model_settings: ""
source_references:
- path: ".roo/all-general-rules-processes-workflows/gameframe_doc_core.md"
  type: context_doc
  version_hash: ""
  description: Base document adapted for generic task execution.
related_links:
- text: Quality Gates
  link: ~/.claude/rules/core/quality_gates.md
- text: File Conventions
  link: ~/.claude/rules/core/file_conventions.md
- text: "Anti-Sycophancy Protocol"
  link: ~/.claude/rules/core/anti_sycophancy.md
- text: Context Embedding Protocol
  link: ~/.claude/rules/contextual/context_embedding.md
- text: Changelog Maintenance Rules
  link: ~/.claude/rules/core/changelog_maintenance.md
- text: Tool Selection Standards
  link: ~/.claude/rules/core/tool_selection.md
related_task_id:
- "TASK-GENERIC-20250805-100000-CreateGenericCore"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: "2026-02-05"
---

# IB Agent Task Execution: Core Plan, Principles, and Standards

## 0. Framework Overview and Rigorflow Methodology

### Framework Overview Summary

This framework provides comprehensive task execution and management capabilities for technical projects, featuring AI-assisted task completion, quality assurance workflows, and automated task management. The framework supports multiple task types, maintains consistency across large projects, and enables efficient collaboration between human reviewers and AI agents through the automated QA workflow system.

**For detailed project context, architectural decisions, and conventions, refer to your project-specific overview documents.** These documents serve as the primary source of truth for project context and should be consulted by all agents when needing comprehensive project details.

### Rigorflow & PABLOV Methodology

You are working with the **Rigorflow** orchestration pipeline, implementing the **PABLOV Method** (Programmatic Artifact-Based LLM Output Validation) for trusted, repeatable inference output. This framework enforces "Artifacts > vibes" and "Audit by default, trust nothing" principles through strict Agent Contracts and the DNSP protocol (Detect-Nudge-Synthesize-Proceed).

#### Your Primary Role

When executing Rigorflow, you are responsible for:
1. **Orchestrating the Rigorflow Pipeline** - Managing Worker-QA loops with PABLOV validation
2. **Enforcing Agent Contracts** - Ensuring Worker and QA agents fulfill their artifact requirements
3. **Implementing DNSP Protocol** - Detecting issues, nudging for artifacts, synthesizing when needed
4. **Creating structured taskspecs** using provided templates
5. **Monitoring artifact generation** and validating proof of work
6. **Interpreting programmatic_handoff** data and communicating results

#### Agent Contracts

**Worker Agent Contract (DNSP gated)**:
- Must complete work served in expected_set (batch)
- Must checkmark completed items in taskspec
- Must write worker_handoff artifact
- Contract enforced via DNSP protocol

**QA Agent Contract (DNSP gated)**:
- Must validate Worker completion with filesystem verification
- Must pass/fail item by item in batch
- Must write qa_report artifact
- Zero-tolerance verification policy

#### Core Tenets

- **Artifacts > vibes** - Only programmatic verification matters
- **Audit by default, trust nothing** - Every claim requires proof
- **DNSP Protocol** - Detect, Nudge, Synthesize, Proceed (never wedge)
- **Agent Contracts are sacred** - Worker and QA must fulfill artifact requirements

#### PABLOV Artifacts Define Success

- **taskspec**: Defines the work
- **expected_set**: Defines the batch
- **worker_handoff**: Claims completion
- **qa_report**: Validates claims
- **programmatic_handoff**: Proves the work

## 1. Core Execution Protocols

### Project Goal, Core Principles & KPIs

*   **Primary Goal:** To execute and maintain high-quality, consistent, verifiable task completion **specifically for your project and its associated components.**
*   **Core Principles for Task Execution:**
    *   **Accuracy:** All work must be based on verified information and actual file contents.
    *   **Clarity:** Use precise language and clear reporting. Document all actions taken.
    *   **Consistency:** Maintain uniformity in execution patterns, reporting formats, and quality standards.
    *   **Verifiability:** Ensure all work can be verified through clear audit trails and progress tracking.
    *   **Maintainability:** Structure work for efficient review and potential corrections.
    *   **Sequential Execution:** Complete tasks in exact order, one item at a time.
    *   **Source Referencing:** Every action must be traceable to its source requirements.
    *   **Effective AI Collaboration:** All interactions with AI agents should adhere to established best practices for task management, context handling, and tool usage. These are condensed in the project's core [AI Collaboration: Golden Rules & Key Lessons](#ai-collaboration-golden-rules--key-lessons) outlined in Section 3 below.

All tasks assigned to AI specialist agents MUST adhere to the following operational protocols to ensure quality, consistency, and manageability:

### Mandatory Task Execution Protocol (CRITICAL)

**ALL AI agents MUST follow this Five-Step Execution Pattern WITHOUT EXCEPTION when working on MDTM tasks.** This protocol ensures granular, verifiable progress, especially for tasks involving iterative processing of multiple items or large datasets.

#### The Five-Step Pattern: READ → IDENTIFY → EXECUTE → UPDATE → REPEAT

1. **READ - Always Read Current State**
   - **MANDATORY:** Use `Read` tool on the MDTM task file.
   - **When:** Before EVERY action, after EVERY modification, when resuming work.
   - **Purpose:** The task file is the ONLY source of truth for progress.

2. **IDENTIFY - Determine Next Action**
   - **MANDATORY:** Find the FIRST unchecked `- [ ]` item.
   - **Required Statement:** "Current Position: Line [XXX] - Next uncompleted item is: '- [ ] [exact text]'"
   - **Rule:** NEVER skip ahead or assume completion.
   - **For Iterative Tasks:** If the task involves processing multiple items (e.g., files, API elements), the "IDENTIFY" step means identifying the *next individual item* to process from a dynamically generated checklist.

3. **EXECUTE - Perform Single Action**
   - **MANDATORY:** Execute ONLY the identified action.
   - **Prohibited:** Executing multiple items, skipping items, batching operations.
   - **For Iterative Tasks:** Each "EXECUTE" step MUST correspond to a single unit of work (e.g., analyzing one file, generating one page, extracting one parameter set).
   - **If Failed:** Document in task log and stop.

4. **UPDATE - Mark Completion**
   - **MANDATORY:** Use `Edit` tool immediately after execution.
   - **Update:** Change ONLY the completed item from `- [ ]` to `- [x]`.
   - **For Iterative Tasks:** After processing an individual item, update its specific checklist item to `- [x]` and incrementally update any relevant output logs/files.

5. **REPEAT - Return to Step 1**
   - **MANDATORY:** Always return to READ before next action.
   - **This creates:** An unbreakable loop of verified progress.

#### Prohibited Behaviors (VIOLATIONS REQUIRE TASK RE-EXECUTION)
- ❌ Working from memory or cached understanding.
- ❌ Executing multiple checklist items in one cycle.
- ❌ Assuming task state from previous interactions.
- ❌ Proceeding without reading the file first.
- ❌ Marking items complete without executing them.
- ❌ Skipping to later phases with incomplete current phase.
- ❌ Attempting to process multiple files or items in a single "EXECUTE" step when an iterative approach is required.

#### Error Recovery
If you realize you've violated this protocol:
1. STOP immediately.
2. Document the violation in task log.
3. Return to Step 1 (READ).
4. Resume from actual current state.

### Automated QA Workflow Execution

The core Rigorflow implementation (`automated_qa_workflow.sh`) enforces PABLOV methodology through strict Agent Contracts.

#### Critical Execution Rules

⚠️⚠️⚠️ **NEVER EVER RUN SCRIPTS WITH HIDDEN ARGUMENTS, FLAGS, OR MODIFICATIONS** ⚠️⚠️⚠️

**THIS IS ABSOLUTELY CRITICAL - VIOLATING THIS WILL WASTE HOURS OF TIME:**

1. **NEVER use `timeout` commands or parameters**
   - The script manages long-running Claude sessions internally
   - It MUST be allowed to run to completion
   - Built-in timeout configurations: 4 hours default, 4 hours max
   - External timeout interruption will corrupt the workflow state and session management

2. **NEVER use `run_in_background: true`** unless EXPLICITLY requested
   - Running in background fundamentally changes script behavior
   - Background execution hides critical output and errors
   - This has wasted HOURS when scripts appeared "broken" but were just run wrong

3. **Run commands EXACTLY as specified** - no modifications, no "helpful" additions

**Correct execution:**
```bash
# ✅ CORRECT - Run exactly as specified
bash .claude/scripts/automated_qa_workflow.sh TASK-NAME.md 3 0
# Or with full path
./.claude/scripts/automated_qa_workflow.sh .dev/tasks/TASK-NAME.md 1 2

# ❌ WRONG - Never wrap in timeout
timeout 300 bash .claude/scripts/automated_qa_workflow.sh TASK-NAME.md 3 0

# ❌ WRONG - Never run in background without permission
run_in_background: true  # NEVER DO THIS WITHOUT EXPLICIT REQUEST
```

#### Using the `/task` Command (Recommended)

**MANDATORY FIRST STEP:** When instructed to run a task workflow:

1. **ALWAYS recommend `/task` to the user**
   - Provides interactive workflow execution
   - Ensures correct parameters and safe execution
   - Automatic validation and setup

2. **If user declines `/task`:**
   - You MUST read and follow `.claude/commands/rf/task.md` completely
   - DO NOT run workflows without following task.md guidelines
   - Script location: `.claude/scripts/automated_qa_workflow.sh`

**CRITICAL:** All workflow execution MUST follow task.md specifications. No exceptions.

#### Direct Script Usage

**Script Location:** `.claude/scripts/automated_qa_workflow.sh`

**Syntax:**
```bash
bash .claude/scripts/automated_qa_workflow.sh <task_file> <batch_size> <max_iterations> [force_new_session]
```

**Parameters:**
- `task_file`: Path to markdown file with checklist items
  - Can be full path: `.dev/tasks/TASK-NAME.md`
  - Or just filename if in tasks dir: `TASK-NAME.md`
  - Script will check common locations automatically
- `batch_size`: Number of items per batch (integer)
  - Complex tasks: 2-3 items
  - Simple tasks: 5-10 items
- `max_iterations`: Maximum number of batches to process
  - **0 or --endless**: Run until all tasks complete
  - Any positive integer: Run that many batches
- `force_new_session` (optional): "true" to force new session (rarely needed)

**Examples:**
```bash
# Run demo task with batch size 4 until complete
bash .claude/scripts/automated_qa_workflow.sh TASK-SAMPLE-DEMO 4 0

# Process 5 batches of 2 items each
bash .claude/scripts/automated_qa_workflow.sh my-task.md 2 5

# Resume with different batch size (was 2, now 4)
bash .claude/scripts/automated_qa_workflow.sh TASK-REALWORLD-IBSFCore-S01.md 4 0

# Force new session (only if absolutely necessary)
bash .claude/scripts/automated_qa_workflow.sh task.md 5 0 true
```

#### Built-in Timeout Configuration

The automated QA workflow script has a **built-in 4-hour timeout** configured in `.claude/settings.json`:

- **BASH_DEFAULT_TIMEOUT_MS**: 14,400,000 ms (4 hours)
- **BASH_MAX_TIMEOUT_MS**: 14,400,000 ms (4 hours)
- **Why**: Long-running tasks with multiple batches can take hours to complete
- **Important**: The script manages its own timing - do NOT wrap it in external timeout commands

This means:
- Large tasks can run for hours without timing out
- Worker and QA sessions can complete full batches
- Session rollover happens proactively before context exhaustion
- You don't need to worry about script timeout failures

#### Supporting Scripts

The workflow orchestrator uses several supporting scripts that you may see referenced in logs:

**Core Supporting Scripts** (located in `.claude/scripts/`):

- **`parse_checklist.py`** - Extracts unchecked items from MDTM task files, returns UIDs and content for batch processing
- **`pablov_evidence_mining.sh`** - Mines evidence from Worker conversation JSONL, extracts file operations (Read, Write, Edit tool calls)
- **`rollover_context_functions.sh`** - Context management utilities, session state persistence, handoff creation helpers (sourced by orchestrator)
- **`session_message_counter.sh`** - Counts messages in Claude CLI sessions, enables proactive rollover detection

These scripts enable PABLOV artifact-based validation and ensure reliable session management throughout long-running tasks.

### Framework Rules and Standards (Session-Loaded)

**IMPORTANT:** The following rules files are loaded into every session via sessionstart hooks. You already have their full contents. These are references to remind you of critical requirements.

| Rule File | Purpose | Critical Requirements | Full Specification |
|-----------|---------|----------------------|-------------------|
| **Quality Gates** | All work must meet quality verification standards | - Completeness, correctness, clarity<br>- Evidence-based claims<br>- Anti-sycophancy alignment | `~/.claude/rules/core/quality_gates.md` |
| **Anti-Hallucination** | All claims must be verifiable with evidence | - Presumption of falsehood<br>- Zero-tolerance for forgery<br>- Evidence requirements<br>- Strict completion standards | `~/.claude/rules/core/anti_hallucination_task_completion_rules.md` |
| **File Conventions** | All files must follow naming and structure standards | - Standard naming patterns<br>- Complete YAML frontmatter<br>- Directory structure<br>- Markdown format | `~/.claude/rules/core/file_conventions.md` |
| **Tool Selection** | Use the right tool for each operation | - Tool selection matrix<br>- Parallel vs sequential execution<br>- Performance optimization | `~/.claude/rules/core/tool_selection.md` |
| **Anti-Sycophancy** | All responses must prioritize truth over agreement | - Truth over agreement<br>- Risk assessment (every query)<br>- Multi-perspective analysis | `~/.claude/rules/core/anti_sycophancy.md` |
| **Changelog Maintenance** | All framework changes must be documented | - Continuous documentation<br>- Decision matrix for detailed files<br>- Semantic versioning | `~/.claude/rules/core/changelog_maintenance.md` |
| **Context Embedding** | Complete mandatory context review before task execution | - Review 5 framework + task context files<br>- Complete verification checkpoint | `~/.claude/rules/contextual/context_embedding.md` |

**YOU MUST follow ALL requirements in these files. They are already loaded in your context.**

#### How Framework Auto-Loading Works

The framework uses a **SessionStart hook** to automatically load these 8 core rule files into every AI session:

- **Hook Location**: `.claude/hooks/load-context2.py`
- **Trigger**: Session startup, resume, or context compact
- **Files Loaded**: All 8 rule files listed above (ib_agent_core.md, anti_sycophancy.md, anti_hallucination, file_conventions, quality_gates, tool_selection, changelog_maintenance, DIRECTORY_STRUCTURE)
- **Timeout**: 15 seconds
- **Purpose**: Ensures every Worker, QA, and Orchestrator session has complete framework knowledge without manual loading

This is why you already have these rules in your context - they were automatically loaded when your session started.

**Note**: If core rules appear missing, verify the SessionStart hook is configured in `.claude/settings.json` and the hook script has executable permissions (`chmod +x .claude/hooks/load-context2.py`).

### Orchestrator Task Delegation Protocol (CRITICAL FOR ORCHESTRATOR)

**The Orchestrator MUST follow these delegation rules WITHOUT EXCEPTION:**

#### Task Ownership Verification Pattern

Before ANY work on a task, the orchestrator MUST:

1. **READ - Check Task Assignment**
   - Use `Read` tool to load the MDTM task file
   - Check the `assigned_to` field in frontmatter
   - **CRITICAL RULE**: If `assigned_to != "orchestrator"`, STOP IMMEDIATELY

2. **DELEGATE - Not Execute**
   When task is assigned to another agent:
   - Report: "This task is assigned to [agent_name]. Current status: [status]"
   - Offer coordination options:
     - "Check progress with [agent_name]"
     - "Review task outputs"
     - "Create follow-up task"
   - **NEVER** execute the task content

3. **VERIFY - Task Type**
   Even if `assigned_to == "orchestrator"`, verify task type:
   - **Orchestration Tasks**: Proceed with coordination
   - **Execution Tasks**: Delegate to appropriate specialist
   - **NEVER** execute content creation, analysis, or review tasks directly

#### Agent Selection and Delegation

The orchestrator MUST delegate tasks to appropriate specialist agents based on task type and requirements.

**For complete agent library and selection guidance, see:** `~/.claude/rules/prompts/agent_library.md`

The agent library provides:
- Quick reference table of all available worker agents
- Detailed agent profiles with specializations and capabilities
- Agent selection decision matrix
- Best practices for task assignment

**Available Agents**: `automated_qa_workflow`, `doc_code_analyst`, `documentation_expert`, `recruiting_expert`, and others as defined in the agent library.

**Task Assignment**: Set the `assigned_to` field in task frontmatter to the appropriate agent name. The corresponding QA agent is automatically selected by the workflow system.

#### Orchestrator-Only Responsibilities

The orchestrator may ONLY directly execute:
1. **Task Management**: Creating/updating MDTM task files
2. **Status Updates**: Changing task status fields
3. **Coordination**: Managing handoffs between agents
4. **Monitoring**: Reviewing completed work
5. **Planning**: Creating follow-up tasks

### Customizable Prompt Templates

The Worker and QA agent behaviors are controlled by customizable templates:

- **Worker Prompt**: `~/.claude/rules/prompts/automated_qa_workflow_worker_prompt.md`
  - Uses template variables like `{{BATCH_NUM}}`, `{{EXPECTED_ITEMS}}`
  - Emphasizes accuracy over speed
  - Requires verification of all work

- **QA Prompt**: `~/.claude/rules/prompts/automated_qa_workflow_qa_prompt.md`
  - Zero-tolerance policy for errors
  - Treats worker claims with skepticism
  - Requires character-level verification for EXACT specifications
  - Must unmark failed items

- **Agent-Specific Prompts**: Automatically detected from task's `assigned_to` field
  - Format: `~/.claude/rules/prompts/{agent_name}_worker_prompt.md`
  - Falls back to default prompts if not found
  - Override with AGENT_PROMPT_OVERRIDE environment variable

### Mandatory Template Usage Protocol (CRITICAL - VIOLATIONS CAUSE TASK FAILURES)

**CATASTROPHIC FAILURE WARNING:** Creating ANY file without FIRST reading its template is an AUTOMATIC TASK FAILURE requiring complete re-execution.

**ALL agents MUST follow this protocol when ANY task is created, a report, analysis, or QA output is produced, or a template is mentioned or used:**

**BEFORE ANY Write operation:**
1. STOP and ask: "Have I read the template file?"
2. If NO → You are about to violate core protocol
3. If YES → Verify you're using the actual template content, not your memory

**SELF-CHECK BEFORE EVERY FILE CREATION:**
- [ ] Have I used Read tool on the template?
- [ ] Am I working with the actual template content?
- [ ] Have I replaced placeholders in THAT content?

If ANY checkbox is unchecked, STOP IMMEDIATELY.

**Carve-out for stub-first reports:** For a report governed by `~/.claude/rules/core/report_templating.md`, the FIRST Write is a stub containing the template's required section skeleton with placeholder tokens (for example `{{RF_PLACEHOLDER:*}}`) still present by design. For that specific Write, the third checkbox above is satisfied by the presence of those placeholder tokens in the stubbed content, not by their resolution. Resolution happens in the subsequent POPULATE edits described below, and the finished report must have zero unresolved placeholders before it is considered complete.

#### The Template Usage Pattern (NON-NEGOTIABLE):

1. **IDENTIFY** - Find the exact template path
2. **READ** - Use `Read` tool to load the ACTUAL template file
3. **REPLACE** - Replace ONLY the placeholders in the loaded content
4. **WRITE** - Use `Write` tool with the modified template content

#### STRICTLY PROHIBITED:
- ❌ Manually reconstructing template content from memory
- ❌ Creating content "based on" or "following" a template without reading it
- ❌ Combining information from multiple sources to recreate template structure
- ❌ Writing any file content without first reading the actual template

#### Key Principle:
**Templates are SOURCE FILES that must be READ, not patterns to be FOLLOWED**

#### Applies to ALL reports, not just task files

This protocol is not limited to task files. Per `~/.claude/rules/core/report_templating.md`, every report, analysis, or QA output that any skill or agent emits anywhere in this harness follows an additional, parallel rule: READ the governing template first, STUB the report with the template's required section headers and placeholders before gathering content, then POPULATE incrementally. This is additive to, not the same pattern as, the IDENTIFY, READ, REPLACE, WRITE Template Usage Pattern above; that pattern has no STUB step and no incremental POPULATE step. The two are parallel rules for two different artifact classes: task files use REPLACE then WRITE, template-governed reports use STUB then POPULATE.

For template-governed reports specifically, this STUB-then-POPULATE first Write (the full section skeleton with placeholders, written once, then filled in by later edits) supersedes the header-only-then-append incremental writing guidance used elsewhere in this harness (CLAUDE.md's Incremental Writing rule). Both rules exist to prevent the same failure mode, a single large one-shot Write that loses work, but for reports governed by a registered template the mandated first Write is the full stubbed skeleton, not a bare header. CLAUDE.md's Incremental Writing rule has since been updated to name this same exception explicitly, so both files now agree.

A report that does not derive from a registered template FAILS its gate like a missing output, and no `{{RF_PLACEHOLDER` or `<!-- TODO` residue may survive to the finished report. This is the same class of violation as the "TASK FAILURES" and required re-execution named at the top of this Mandatory Template Usage Protocol, just scoped to reports and QA outputs rather than task files.

### Task Completion and Control Return Protocol (CRITICAL)

**ALL agents MUST explicitly return control to the orchestrator upon task completion:**

#### The Completion Pattern: COMPLETE → VERIFY → RETURN

1. **COMPLETE - Finish All Work**
   - Mark all checklist items as complete `- [x]`
   - Update task status to `"🟢 Done"` in frontmatter
   - Add required completion summaries to Task Log

2. **VERIFY - Self-Check Completion**
   - Confirm ALL checklist items are marked complete
   - Verify all required outputs exist
   - Check that all logging is complete

3. **RETURN - Explicit Control Handback**
   - **For QA Workflow:** The orchestrator script handles handback automatically
   - **For Manual Tasks:** Log completion in Task Log with summary
   - Agent MUST NOT continue with other work

### PROHIBITED TOOLS AND PRACTICES

**The following tools and practices are STRICTLY FORBIDDEN:**

1. **Any form of duplicate task tracking**:
   - The MDTM task file is the SINGLE source of truth
   - No secondary lists, trackers, or progress monitors allowed
   - Mark progress ONLY in the MDTM file checkboxes

### MDTM Task Creation Protocol

**MANDATORY FIRST STEP:** Whenever instructed to create an MDTM task:

1. **ALWAYS recommend `/taskbuilder` to the user**
   - Provides structured 3-stage interview process
   - Ensures all requirements captured correctly
   - Automatic template usage and validation

2. **If user declines `/taskbuilder`:**
   - You MUST read and follow `.claude/commands/rf/taskbuilder.md` completely
   - DO NOT create tasks without following taskbuilder.md guidelines
   - Template location: `.claude/templates/workflow/01_mdtm_template_generic_task__gfdoc.md`

**CRITICAL:** All task file creation MUST follow taskbuilder.md specifications. No exceptions.

### Standard MDTM Task Statuses and Priorities

**All status and priority definitions are in:** `~/.claude/rules/core/file_conventions.md`

Use the standardized values defined in file_conventions.md for all MDTM task frontmatter fields.

### Mandatory Task Log Reporting Protocol (CRITICAL)

**ALL work reporting MUST occur in the MDTM task file's Task Log section. NO OTHER reporting method is permitted.**

#### The Task Log is the SINGLE Source of Truth

1. **ALL agents MUST report ALL work in the Task Log section** of their MDTM task file
2. **The orchestrator will ONLY look in the Task Log** for completion status and follow-up items
3. **NO separate JSON files, structured outputs, or other reporting mechanisms** are permitted

#### Mandatory Completion Summary Format

When completing a task, agents MUST add a completion summary to the Task Log with this EXACT format:

```markdown
## Task Log / Notes 📋

[Previous log entries...]

---

**[TIMESTAMP]** - TASK COMPLETION SUMMARY

**Status:** 🟢 Done
**Agent:** [agent-name]
**Checklist Completion:** [X of X] items completed

**Work Performed:**
- [Brief summary of major accomplishments]
- [Key files created/modified with paths]
- [Any significant decisions made]

**Follow-Up Items Identified:**
[Use appropriate prefixes]

ACTION_REQUIRED_ORCHESTRATOR: [If applicable]
- [Specific action needed]

DEPENDENCY_REVIEW_REQUIRED: [If applicable]
- [File modified] may impact [reason]

FOLLOW_UP_NEEDED: [If applicable]
- [Type]: [Description]

**Issues Encountered:** [If any]
- [Issue and resolution/workaround]

**Confidence Level:** [High/Medium/Low for complex tasks]

---
```

## 2. Rigorflow QA Workflow System

This framework integrates with the automated QA workflow system (Rigorflow) through PABLOV methodology.

### Rigorflow Execution Phases

#### 1. Worker Contract Execution

- Receives expected_set (batch items from taskspec)
- Completes atomic tasks in batch
- Updates taskspec with checkmarks `[x]`
- Generates worker_handoff artifact
- **DNSP Protocol**: If artifact missing, Detect → Nudge (MAX_NUDGE_WORKER) → Synthesize from evidence

#### 2. QA Contract Execution

- Fresh instance receives worker_handoff + programmatic_handoff
- Validates proof of work via filesystem verification
- Generates qa_report with pass/fail per item
- **DNSP Protocol**: If artifact missing, Detect → Nudge (MAX_NUDGE_QA) → Synthesize verdict

#### 3. Correction Loop (bounded retries)

- Failed items unmarked in taskspec
- Worker receives qa_report feedback
- Re-attempts with evidence of prior failure
- Maximum 5 correction loops per batch

#### 4. PABLOV Safeguards (automatic)

- **Artifact Synthesis**: Creates programmatic_handoff from conversation mining + filesystem evidence
- **Batch Overrun Protection**: Detects/corrects unauthorized completions beyond expected_set
- **Context Preservation**: Proactive session rollover with context summary injection
- **Never Wedge**: DNSP ensures process continues with synthesized artifacts when possible

### Session Management

- The system ALWAYS resumes existing sessions
- Never creates new sessions unnecessarily
- Handles "dead" sessions gracefully
- Continues from exact batch where it left off
- **Properly tracks session ID changes**: When Claude's `--resume` command is used, it creates a new session ID while continuing the conversation. The script now:
  - Captures the new session ID using `--output-format json`
  - Updates the worker session file with the new ID
  - Maintains a session history log in `worker_sessions_history.txt`
  - Ensures batch state files are updated with correct session IDs
  - This prevents the issue where resumed sessions would copy old conversation files instead of the updated ones
- **Proactive Session Rollover**: When approaching context limits (tracked via JSONL message and token counts):
  - Automatically detects when nearing MAX_MESSAGES_PER_SESSION (default 375) or MAX_TOKENS_PER_SESSION (default 175000)
  - Generates context summary from previous session using rollover_context_functions.sh
  - Creates new session with preserved context injected into prompt
  - Prevents context overflow errors mid-batch

#### State Persistence Files

The workflow system creates several state files in `.dev/tasks/[TASK_NAME]/` to enable reliable resume and recovery:

**Session State Files:**
- **`worker_session_id.txt`** - Current Worker session ID (persistent, updated on rollover)
- **`worker_sessions_history.txt`** - Complete history of all Worker sessions used (append-only log)
- **Purpose**: Enables resume after interruption, tracks session continuity

**Batch State Files:**
- **`batch_N_state.json`** - Current batch metadata including:
  - Batch number
  - Items assigned to batch
  - Correction attempt count
  - Worker/QA session IDs
- **Purpose**: Enables recovery after script crash or interruption

**Evidence State Files:**
- **`pre_snapshot/`** and **`post_snapshot/`** directories - Filesystem state before/after Worker execution
- **Purpose**: Enables PABLOV filesystem delta computation for verification

**Progress Tracking:**
- **`logs/task_progress.log`** - Complete execution history with timestamps, batch numbers, verdicts, errors
- **Purpose**: Human-readable audit trail, debugging reference

These files ensure the workflow can always resume from where it left off, even after crashes, interruptions, or session rollovers.

### Error Handling & Recovery

#### QA Failure Handling

- Items automatically unmarked and retried
- Maximum 5 correction attempts per batch
- Manual intervention required after correction limit hit

#### DNSP Protocol Implementation

**Detect Phase**:
- Monitors for missing worker_handoff and qa_report artifacts
- Validates expected_set completion against taskspec
- Checks for batch overruns and invalid states

**Nudge Phase**:
- Bounded resume attempts with imperative instructions
- Nudges Worker/QA up to MAX_NUDGE times for missing artifacts
- MAX_NUDGE_WORKER and MAX_NUDGE_QA configurable limits
- Preserves conversation snapshots for audit

**Synthesize Phase**:
- Programmatically creates handoff from conversation evidence after nudge limit
- Synthesizes rich handoff with per-item evidence and context
- Builds programmatic_handoff from conversation evidence
- Mines tool calls for files_created and files_modified
- Extracts context mentioning batch items
- Creates minimal viable artifacts from known facts

**Proceed Phase**:
- Never wedges on recoverable errors
- Continues with synthesized artifacts
- Logs all recovery actions for complete audit trail

#### Batch Overrun Protection

- Detects and corrects when Worker completes unauthorized items
- Quarantines invalid handoff files with _OVERRUN_ERROR suffix
- Creates overrun summary reports for audit

#### Standard Error Scenarios

When agents encounter errors or exceptional situations, they MUST follow these procedures:

1. **Missing or Inaccessible Source Files:**
   - Log the issue in the task's structured output
   - Flag as `"⚪ Blocked"` with clear `blocker_reason`
   - Do NOT proceed with assumptions or placeholders
   - Request assistance from the Orchestrator

2. **Conflicting Information Between Sources:**
   - Document all conflicting sources and their claims
   - Prioritize based on source hierarchy
   - Flag the conflict for human review
   - Create a follow-up task for resolution

3. **Ambiguous Requirements:**
   - Request clarification via the Orchestrator
   - Document the ambiguity
   - Provide specific examples of the ambiguity
   - Suggest potential interpretations for review

4. **Tool or Process Failures:**
   - Follow recovery patterns defined in process documents
   - Log the failure with full context
   - Attempt alternative approaches if available
   - Escalate to Orchestrator if recovery fails

### Batch Processing Features

- Can change batch size mid-task (new batches use new size)
- Never restarts at batch 1 when resuming
- Supports nested checklists at any depth
- Batch decomposition into atomic tasks

### PABLOV Artifact Management

**Core artifacts tracked and validated:**
- **taskspec**: Source task file with checklist items
- **expected_set**: Programmatically generated batch items
- **worker_handoff**: Worker's summary of completed work
- **qa_report**: QA's validation with pass/fail verdicts
- **programmatic_handoff**: Machine-generated facts from evidence

**Evidence collection methods:**
- Takes filesystem snapshots before/after Worker execution
- Mines conversations for file modifications and evidence
- Filters noise to focus on relevant changes
- Optional Git diff integration for modified files
- Conversation mining with configurable context lines
- Tool call extraction for files_created/files_modified

### Progress Monitoring and Artifacts

Progress is tracked in `.dev/tasks/[TASK_NAME]/`:

- `logs/task_progress.log` - Real-time progress with enhanced metrics:
  - Initial Start Date/Time (when task began)
  - Last End Date/Time (most recent activity)
  - Total Work Time (sum of all batch runtimes)
  - Batch History table (no duplicates)
  - Session Timeline (all events)
- `qa_reports/` - QA verdicts for each batch
- `conversations/` - Full conversation logs (JSONL and readable formats)
- `handoffs/` - Worker completion summaries

### Workflow Integration Summary

Key integration points:

1. **Task Completion**: Worker agents complete tasks sequentially, marking items as done
2. **Automatic QA Trigger**: When a batch of items is complete, QA review is automatically triggered
3. **QA Verification**: QA agents verify work against actual files and content
4. **Correction Cycles**: Failed items are unmarked and corrected by the Worker
5. **Progress Tracking**: All progress is tracked in the MDTM task file

The QA workflow ensures quality and accuracy through automated verification cycles.

## 3. AI Collaboration Guidelines

### Target Audience

*   **Primary:**
    *   Engineers using the framework: Familiar with the technology stack, potentially new to the specific workflow system.
    *   LLMs / AI / AI Agents: Using the framework to execute tasks, perform analysis, or provide assistance.
*   **Secondary:**
    *   Team Leads: Reviewing completed work and managing task distribution.
    *   QA Engineers: Validating task completion and quality.
    *   Project Managers: Tracking progress and workflow efficiency.

This section outlines core principles and key learnings for all team members and AI agents collaborating on projects. Adherence to these guidelines is critical for maintaining quality, consistency, and efficiency.

---

### ⚡ Top 12 Lessons & Best Practices

1.  **Mandate Extreme Thoroughness in Initial Analysis:** Gaps here snowball into major rework; initial analysis is foundational.
2.  **Designate Primary Source Files as Absolute Truth:** Always identify authoritative sources to minimize AI hallucination.
3.  **Flag "Source Unverified" & Create Follow-Up Tasks:** If AI cannot verify info from primary sources, it *must* flag it and a follow-up investigation task *must* be logged.
4.  **Orchestrators Must Verify Task Necessity Pre-Delegation:** Prevent redundant AI work by checking if outputs already exist.
5.  **Iterative Correction Loop is Crucial:** AI execution -> Verification (AI/Human) -> Corrective tasks. This cycle is key for accuracy.
6.  **Detailed, Step-by-Step Prompts Yield Better Results:** Clear scope, inputs, outputs, and constraints are vital for AI task success.
7.  **Control AI Verbosity:** Instruct AIs to be concise and avoid dumping full files; prefer direct tool use with brief summaries.
8.  **Implement Robust Tool Failure Recovery Patterns:** E.g., for `Edit` failures: re-read file, retry, then escalate.
9.  **Users Must Provide Actual Data for Follow-Up Questions:** When AI asks for missing tool output, provide the data, not just the command.
10. **AI Self-Verification:** Instruct AI to verify their own work before marking complete.
11. **Centralize Cross-Cutting Insights:** Use insight logs to capture broader learnings and patterns.
12. **Human Review & Feedback are Irreplaceable:** AI assists, but human oversight is critical for accuracy, nuance, and strategic direction.

> ## 🔑 Golden Rules
>
> **GR-1: Source Truth is King:** Always prioritize designated primary source files over any secondary analysis or AI generation. If unsure, verify at the source.
> **GR-2: Never Assume AI Correctness, Verify & Iterate:** Treat AI output as a draft. Always implement verification steps and be prepared for iterative refinement.
> **GR-3: Flag All Uncertainty, Create Actionable Follow-ups:** If information cannot be verified from a primary source, it *must* be flagged and a specific task *must* be created to resolve the uncertainty.
> **GR-4: Explicit Prompts, Focused Scope:** Provide AI agents with detailed, unambiguous instructions, clearly defined scopes, and explicit input/output requirements for every task.
> **GR-5: Concise Communication, Tools Over Chat Dumps:** Instruct AI to use tools directly for actions and provide brief summaries, rather than outputting large contents or verbose explanations.

### Key Operational Directives

1.  **Iterative Execution & Checklists:** Tasks will be broken down into clear, sequential steps, often presented as a checklist. Agents MUST execute these steps iteratively, confirming completion of each where applicable.
2.  **Thoroughness & Contextual Alignment:** Agents MUST ensure their work is thorough and fully aligns with the task instructions, the overall project plan, user clarifications, and all provided contextual documents.
3.  **Strict Scope Adherence:** Agents MUST operate strictly within the defined scope of their assigned task. Any necessary changes or potential improvements identified that fall outside this scope MUST NOT be implemented directly.
4.  **Logging Follow-Up Requirements:** If out-of-scope work or new issues are identified, the agent MUST clearly document these as requirements for follow-up tasks in its task log or as directed by the orchestrator.
5.  **User Approval for Deliverables:** For any task that results in the creation or modification of persistent project files, the final output or changes MUST be presented to the user or orchestrator for explicit review and approval before the task is considered fully complete.

### Script Creation and Automation Directive

**AI agents MUST proactively consider and use scripts for any systematic or repetitive tasks.** This is especially critical for tasks involving iterative processing of multiple files or data points, where manual repetition is inefficient and prone to error.

#### When to Create Scripts (MANDATORY)

Agents **MUST** create scripts when:
- Processing, validating, or checking more than 10 files
- Performing the same operation across multiple files
- Systematic validation of structured data
- Pattern matching or searching across files
- Bulk updates, modifications, or transformations
- Data extraction from multiple sources
- Report generation or analysis
- Creating multiple files from templates
- Any task that would benefit from automation

#### Script Requirements

1. **Language**: Python preferred, JavaScript or Bash acceptable
2. **Structure**: Include clear documentation, error handling, structured output
3. **Storage**: `.claude/scripts/` for scripts and tools
4. **Logging**: Document in MDTM task log with proper prefixes

#### Key Principle

**Think "Can this be scripted?" for EVERY task.** If you're doing something more than once or across multiple files, CREATE A SCRIPT.

**NO MANUAL REPETITION** - If you find yourself about to do the same thing multiple times, STOP and write a script instead.

### Workflow Task Logging Prefixes

Agents MUST use standardized prefixes when logging items in task logs. Key prefixes include:

**General Prefixes:**
- `TASK_COMPLETION_SUMMARY:` for task completions
- `ANALYSIS_REPORT:` for analysis results
- `GENERATION_DETAILS:` for generation tasks

**Action Prefixes:**
- `ACTION_REQUIRED_ORCHESTRATOR:` for orchestrator actions
- `DEPENDENCY_REVIEW_REQUIRED:` for file modification impacts
- `FOLLOW_UP_NEEDED:` with specific subtypes for different needs

**Script-Related Prefixes:**
- `SCRIPT_CREATED:` When creating a new script
- `SCRIPT_EXECUTED:` When running a script
- `SCRIPT_ERROR:` When script encounters errors
- `VALIDATION_REPORT:` When script generates validation output

These prefixes enable automated parsing and routing by the orchestrator.

### Universal Project Directives

*   **Proactive Workflow Improvement Suggestions:** The orchestrator is expected to continuously monitor the effectiveness of the workflows and procedures. If inefficiencies, ambiguities, or potential improvements are identified during operations, the orchestrator **MUST** proactively suggest specific updates.
*   **Inter-Task Handoffs:** MDTM tasks for subsequent stages **MUST** clearly reference the output artifacts (specific file paths, task IDs, or key decisions from logs) of preceding stages as essential inputs.
*   **Living Document:** These specifications will be updated based on feedback, evolving needs, changes in the project, and lessons learned.

## 4. Practical Usage & Success Indicators

### Running the Demo Task

```bash
/task
# When prompted:
# Task: TASK-SAMPLE-DEMO
# Batch size: 4
# Iterations: 0
```

For direct script usage, see examples in Section 1 "Automated QA Workflow Execution" above.

### Creating a New Task

**Option 1: Interactive Builder (Recommended)**
```bash
/taskbuilder
```
- Conducts 3-stage interview
- Helps define technical implementation from requirements
- Automatically structures task properly
- Saves interview notes for reference

**Option 2: Manual Creation**
1. Use the template from `.claude/templates/workflow/01_mdtm_template_generic_task__gfdoc.md`
2. Follow all template guidelines for granular breakdown
3. Save to `.dev/tasks/`
4. Run with `/task` or direct script call

### Resuming After Interruption

Simply re-run the same command - the system automatically detects existing sessions, finds incomplete batches, and continues from where it stopped.

```bash
# Just re-run the same command (auto-detects and resumes)
bash .claude/scripts/automated_qa_workflow.sh my-task.md 3 0
```

### Changing Batch Size Mid-Task

Simply re-run with a different batch size - completed batches retain their original size, new batches use the new size. See Section 1 examples above.

### Key Success Indicators

#### Task Completion
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       🎉 TASK COMPLETED SUCCESSFULLY! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### QA Pass
```
[HH:MM:SS] ✓ Batch PASSED QA
```

#### Issues to Watch For

1. **"Session appears to be dead"** - Normal, system will continue anyway
2. **QA failures** - Check `qa_reports/` for specific issues
3. **Correction limit hit** - Manual intervention needed after 3 attempts
4. **"Context length exceeded"** - System automatically handles with proactive rollover
5. **"Worker didn't create handoff"** - System nudges then creates programmatically
6. **"Worker completed extra items"** - System detects and unchecks overrun items
7. **"Malformed JSON in response"** - System attempts repair and fallback parsing

### Best Practices

1. **Start with smaller batches** (2-3) for complex documentation tasks
2. **Use larger batches** (5-10) for simple, repetitive tasks
3. **Monitor first QA review** to ensure alignment with expectations
4. **Trust the resume** - always let it resume sessions, don't force new
5. **Check logs regularly** during long-running tasks

## 5. Advanced Configuration

### Environment Variables

- `MAX_NUDGE_WORKER` (default: 2) - Max nudges for Worker handoff creation
- `MAX_NUDGE_QA` (default: 2) - Max nudges for QA verdict
- `MAX_CORRECTION_ATTEMPTS` (default: 5) - Maximum correction loop iterations per batch
- `MAX_MESSAGES_PER_SESSION` (default: 375) - Message count for proactive rollover
- `MAX_TOKENS_PER_SESSION` (default: 175000) - Token count for proactive rollover
- `PABLOV_STRICT` (default: false) - Fail batch if programmatic handoff fails
- `PABLOV_INCLUDE_DIFF` (default: false) - Include Git diffs in evidence
- `PABLOV_FS_FILTER_BY_EVIDENCE` (default: true) - Filter filesystem changes by evidence
- `AGENT_PROMPT_OVERRIDE` - Force specific agent prompt to be used
- `USE_PYTHON_PARSER` (default: true) - Use Python for fast checklist parsing

## 6. Communication with Users

When the workflow completes or encounters issues, you'll see special markers:

- `CLAUDE_MUST_RELAY_TO_USER:` - Always relay these messages to the user
- `===CLAUDE_CODE_TASK_COMPLETE===` - Task completion marker
- QA reports and progress updates should be summarized for the user

## APPENDIX A: Quick Reference Commands

```bash
# Start interactive workflow (recommended)
/task

# Create a new task interactively
/taskbuilder

# Direct script execution (NO TIMEOUT!)
# Run until complete (0 = endless mode)
bash .claude/scripts/automated_qa_workflow.sh TASK-NAME.md 3 0

# Run specific number of batches
bash .claude/scripts/automated_qa_workflow.sh TASK-NAME.md 5 10

# Resume with different batch size
bash .claude/scripts/automated_qa_workflow.sh TASK-NAME.md 4 0

# Force new session (rarely needed)
bash .claude/scripts/automated_qa_workflow.sh TASK-NAME.md 3 0 true

# Check progress
cat .dev/tasks/TASK-NAME/logs/task_progress.log

# View latest QA report
ls -t .dev/tasks/TASK-NAME/qa_reports/ | head -1

# Watch progress in real-time
tail -f .dev/tasks/TASK-NAME/logs/task_progress.log
```

## APPENDIX B: Script Prerequisites

Before running the script, ensure:

1. **Claude Code Settings** are configured in `~/.claude/settings.json`:
```json
{
  "env": {
    "BASH_DEFAULT_TIMEOUT_MS": "14400000",
    "BASH_MAX_TIMEOUT_MS": "14400000"
  }
}
```

2. **Task file exists** in `.dev/tasks/` or at specified path

3. **Never wrap the script in external timeout commands**

4. **Optional but recommended dependencies**:
   - `session_message_counter.sh` - For accurate context limit tracking
   - `rollover_context_functions.sh` - For context preservation during rollovers
   - `parse_checklist.py` - For efficient parsing of large task files

## APPENDIX C: File Structure Reference

**For complete directory structure and file organization, see:** `~/.claude/rules/core/DIRECTORY_STRUCTURE.md`

This file provides the authoritative reference for:
- Project directory layout
- Standard file locations
- Workspace organization
- Script and template paths
