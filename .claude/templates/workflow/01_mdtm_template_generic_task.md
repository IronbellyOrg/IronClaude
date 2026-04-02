---
id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"
title: "[Clear, Action-Oriented Task Title]"
description: "[Detailed description of what this task accomplishes and its purpose within the larger workflow]"
status: "🟡 To Do"
type: "📝 Documentation"
priority: "🔼 High"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "[agent-name]"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: "[PARENT-TASK-ID]"
depends_on:
- "[DEPENDENCY-TASK-ID-1]"
- "[DEPENDENCY-TASK-ID-2]"
related_docs:
- path: "[path/to/governing/workflow.md]"
  description: "Parent workflow this task implements"
- path: "[path/to/process.md]"
  description: "Process document governing this task"
- path: "[path/to/related/doc.md]"
  description: "Related documentation"
tags:
- "[relevant]"
- "[tags]"
- "[for]"
- "[categorization]"
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---

<!--
################################################################################
################################################################################
##                                                                            ##
##                                                                            ##
##                    PART 1: TASK BUILDING INSTRUCTIONS                      ##
##                    ===================================                      ##
##                                                                            ##
##                    FOR ORCHESTRATOR/TASK BUILDER ONLY                      ##
##                                                                            ##
##     This entire PART 1 section contains instructions for building          ##
##     the task file. NONE of this content appears in the actual output       ##
##     task file. The clean template structure is in PART 2 below.            ##
##                                                                            ##
##                                                                            ##
################################################################################
################################################################################

==============================================
SECTION A: CORE PRINCIPLES
==============================================

A1. WORKFLOW DOCUMENT AVAILABILITY CHECK
   Before using this template, the orchestrator MUST:
   1. Check if governing workflow documents exist in the project (typically in `.gfdoc/workflows/`, `.roo/workflows/`, or similar directories)
   2. If workflow documents EXIST:
      - Follow all workflow-related sections in this template
      - Reference specific workflow documents throughout the task
      - Include workflow compliance sections
   3. If workflow documents DO NOT EXIST:
      - Omit all workflow-specific sections (marked with "WORKFLOW-DEPENDENT" below)
      - Replace workflow references with direct user requirements
      - Focus on clear, granular task breakdown based on user's stated objectives
      - Still maintain the same level of detail and structure, but derive requirements from user input rather than workflow documents

A2. WORKFLOW DOCUMENT DEEP INTEGRATION [WORKFLOW-DEPENDENT]
   - BEFORE creating task content: Thoroughly review the complete governing workflow document
   - Extract EVERY requirement, phase, step, and quality standard from the workflow
   - Map EVERY workflow element to corresponding task elements
   - Include ALL workflow verification criteria in task verification section

A3. COMPLETE GRANULAR BREAKDOWN
   - Break down EVERY workflow phase into atomic, verifiable checklist items
   - Create individual checklist items for EVERY file, component, or iteration
   - NO high-level or bulk operations allowed - everything must be granular
   - Include exact file paths, specific requirements, and measurable outcomes

A4. ITERATIVE PROCESS STRUCTURE
   - For ANY process involving multiple items (files, components, etc.):
     * Pre-enumerate ALL items to be processed in initial step
     * Create individual checklist item for each specific item
     * Require incremental updates after each item
     * Include consolidation step only after all items complete
   - Use this pattern:
     ``` markdown
     **Step X.1:** Scan and enumerate all [items] in [location]
     - [ ] Complete [item] listing generated: [count] items identified

     **Step X.2:** Process each [item] individually:
     - [ ] [Item 1]: [exact identifier] - [specific action] completed
     - [ ] [Item 2]: [exact identifier] - [specific action] completed
     [Continue for each item]

     **Step X.3:** Consolidate all individual results
     - [ ] All [count] items processed and results logged
     - [ ] Consolidated output created per requirements
     ```

A5. CROSS-STAGE INTEGRATION [WORKFLOW-DEPENDENT]
   - EVERY phase must explicitly specify inputs from previous stages
   - Include specific file paths to analysis reports, verified outputs, etc.
   - Require consultation of previous stage outputs before proceeding
   - Include validation steps against previous stage findings

A6. WORKFLOW COMPLIANCE ENFORCEMENT [WORKFLOW-DEPENDENT]
   - Include explicit workflow adherence requirements in every phase
   - Reference specific workflow document sections throughout task
   - Copy quality standards directly from workflow documents
   - Include workflow verification criteria in task verification

==============================================
SECTION B: SELF-CONTAINED CHECKLIST ITEMS (CRITICAL)
==============================================

B1. WHY THIS MATTERS (SESSION ROLLOVER PROTECTION)
   Rigorflow executes tasks in batches across multiple sessions. Due to session
   rollovers (context limits), any context loaded in batch 1 will NOT be available
   in batch 3+. Therefore, EVERY checklist item MUST be self-contained - embedding
   all context references, actions, and outputs within a single item. Standalone
   "read context" items that don't produce actionable output are USELESS because
   that context will be lost before it can be used.

B2. EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT THAT INCLUDES:
   1. **Context Reference with WHY** - What file(s) to read and why that context is needed for this specific action
   2. **Action with WHY** - What to do with that context and why it needs to be done
   3. **Output Specification** - The exact output file name, location, what content to produce, and template to follow (if applicable)
   4. **Integrated Verification** - An "ensuring..." clause that specifies what must be verified (DO NOT assume, hallucinate, or make up any information - all content MUST be derived from source files referenced in the checklist item, 100% accuracy based on source materials, document negative evidence when verification fails)
   5. **Evidence on Failure Only** - Log to task notes ONLY if unable to complete due to blockers, missing info, or errors (successful completion is evidenced by the output file itself)
   6. **Explicit Completion Gate** - "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

B3. THE SELF-CONTAINED PATTERN
   Each checklist item should be written as ONE FULL PARAGRAPH (not multiple lines
   or bullets) that is verbose and explanatory. The item should read like a complete
   prompt that could be executed independently without any prior context.

B4. CORRECT EXAMPLE - Self-Contained Checklist Item (action + verification integrated):
   ```markdown
   - [ ] Read the file `component-spec.md` at `docs/specs/component-spec.md` to extract the API interface requirements including all method signatures, parameter types, and return values that must be implemented, then read the file `BaseHandler.ts` at `src/handlers/BaseHandler.ts` to understand the structural patterns and conventions used in existing handlers, then create the file `ApiHandler.ts` at `src/handlers/ApiHandler.ts` containing a TypeScript class that implements all methods defined in the component spec with proper error handling, type annotations, and JSDoc comments following the patterns from BaseHandler, ensuring the file includes the standard header comment block, exports the class as the default export, all methods from the spec are implemented with correct signatures, no content is fabricated or assumed beyond what the source explicitly states, and no placeholder or TODO comments remain. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
   ```

   **NOTE:** Do NOT create separate verification items. Verification requirements
   are integrated into the action item above (the "ensuring..." clause). The QA
   process handles verification between batches.

B5. FORBIDDEN PATTERNS:
   - Standalone "read context" items that don't produce output
     ```markdown
     - [ ] Read file `ib_agent_core.md` and log findings ❌ WRONG - reads context but produces no actionable output; context lost by next batch
     - [ ] Read file `component-spec.md` for requirements ❌ WRONG - standalone read with no action; useless after session rollover
     ```
   - Missing context reference (no source of truth)
     ```markdown
     - [ ] Create ApiHandler.ts with proper methods ❌ WRONG - what methods? from where? no context reference
     - [ ] Update the configuration file ❌ WRONG - which file? what updates? based on what source?
     ```
   - Multi-line/bulleted checklist items (must be single paragraph)
     ```markdown
     - [ ] **Context:** Read spec file  ❌ WRONG - formatted as multiple lines/bullets
           **Action:** Create handler
           **Output:** ApiHandler.ts
     ```
   - Separate verification/confirmation items (integrate via "ensuring..." clause)
   - Overly granular items (e.g., "create directory" alone)
   - Separate REMINDER blocks between checklist items

B6. PREFERENTIAL (include when applicable):
   - Context source references - when action requires reading from source files
   - Output specifications - when action produces a file

B7. KEY PRINCIPLES:
   1. Each checklist item is a COMPLETE PROMPT that could execute independently
   2. Context is embedded IN the action item, not in separate "setup" items
   3. Verification is embedded IN the action item (the "ensuring..." clause), not in separate verification items
   4. Output files serve as evidence of completion - no need to log successful work
   5. Only log to task notes when something FAILS or is BLOCKED
   6. One paragraph, verbose, explanatory - not terse or abbreviated
   7. QA process handles verification between batches (see I15-I16 for phase-gate rules) - do NOT create separate verification items

==============================================
SECTION C: EMBEDDING REQUIREMENTS (NOT SEPARATE SECTIONS)
==============================================

The following information is collected during task planning but MUST BE EMBEDDED
directly into the self-contained checklist items. These are NEVER separate sections
in the task file.

C1. OUTPUTS & DELIVERABLES (embed in checklist items)
   - Each output MUST be specified in the checklist item that creates it
   - Include: exact file path, file name, content requirements, template to follow
   - Example embedding: "...then create the file `api-docs.md` at `docs/api/api-docs.md` containing all public method signatures with parameter types and return values following the format in `.claude/templates/workflow/api-template.md`..."
   - The OUTPUT FILE ITSELF is evidence of successful completion - no separate logging needed
   - Do NOT create an "Outputs & Deliverables" section in the task file

C2. SUCCESS CRITERIA (embed as "ensuring..." clause)
   - Each success criterion MUST be embedded in the relevant checklist item as an "ensuring..." clause
   - Example embedding: "...ensuring all required sections are present, no placeholder text remains, all links are valid, and content matches the source specification..."
   - Do NOT create separate success criteria checklist items
   - Do NOT create a "Success Criteria" section in the task file

C3. VERIFICATION (embed in action items, NOT separate items)
   - Verification requirements MUST be embedded in each action item via "ensuring..." clause
   - Do NOT create separate verification checklist items
   - Do NOT create a "Verification Checklist" section in the task file
   - The intra-task QA process handles verification between batches — see I15 for phase-gate enforcement and I17 for post-completion validation

C4. TASK COMPLETION (final Post-Completion task items only)
   - Task completion is handled by the Post-Completion Actions section
   - Include items for: updating frontmatter (status, completion_date), logging completion to Execution Log
   - Post-completion validation items (I17) handle output verification; frontmatter update and task summary are the only Post-Completion Actions
   - Do NOT create a "Task Completion and Handoff Protocol" section in the task file
   - Orchestrator info about handoff lives in ib_agent_core.md, not in individual task files

==============================================
SECTION D: MANDATORY TASK SECTIONS
==============================================

Every task MUST include these sections:

D1. WORKFLOW COMPLIANCE DECLARATION [WORKFLOW-DEPENDENT]
   ```markdown
   ## MANDATORY WORKFLOW COMPLIANCE

   **CRITICAL:** This task implements [Stage X] from [`stageX_workflow.md`](path).
   YOU MUST strictly follow ALL requirements from the governing workflow document.
   ```
   Note: This section is INFORMATIONAL only - no checklist items here.

D2. CROSS-STAGE INTEGRATION REQUIREMENTS [WORKFLOW-DEPENDENT]
   ```markdown
   ## Cross-Stage Integration Requirements

   **INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

   This section describes cross-stage integration requirements for this task.
   The orchestrator must specify which previous stage outputs are required.
   The actual checklist items for reading and verifying these outputs appear in Phase 1, Step 1.4.

   **Previous Stage Inputs Required:**
   [Orchestrator must specify exact inputs from previous stages]
   - Analysis reports from Stage X: [exact paths and purpose]
   - Verified outputs from Stage Y: [exact paths and purpose]
   - Required context files: [exact paths and purpose]

   **What will be verified in Phase 1:**
   - All previous stage outputs will be read and reviewed
   - Required inputs will be validated for completeness and accuracy
   - Cross-references will be prepared for current stage execution
   ```

D3. CRITICAL RULE
   NO CHECKLIST ITEMS may appear before Phase 1 begins. The template structure ensures:
   - Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable)
   - All checklist items for context review and previous stage inputs appear IN Phase 1, Steps 1.2-1.4

==============================================
SECTION E: CHECKLIST STRUCTURE RULES
==============================================

E1. CHECKBOX FORMAT
   - EVERY actionable item MUST be a checkbox: `- [ ] Action text`
   - NO nested checkboxes (flat structure only)
   - NO parent checkboxes that summarize children
   - Each checkbox is ONE atomic, verifiable action
   - Use **Step X.Y:** headers for grouping, NOT checkboxes
   - Checkboxes MUST appear in the exact order they will be completed
   - Every task MUST have step-by-step checklists that agents complete sequentially
   - Never require marking items above the current working position
   - Never reference checkboxes that appear later in the document
   - Each checklist item must be atomic and verifiable
   - Agents MUST mark each item complete before moving to the next
   - DO NOT create high-level or vague checklist items
   - NEVER create parent checkbox items with child checkbox items - use descriptive headers instead
   - For grouped tasks, use a header without checkbox, then list individual items with checkboxes

E2. CRITICAL CHECKLIST STRUCTURE RULES
   - **FUNDAMENTAL RULE**: Summary/parent checkboxes MUST come AFTER all their component items
   - **NEVER** put a parent checkbox before its child components
   - **ALWAYS** place summary checkboxes at the END of a sequence
   - Indented checklists are allowed, but ONLY when they don't have a parent checkbox above them

   **CORRECT PATTERN - Components First, Summary Last:**
   ```markdown
   ### Step 2.1: Create Directory Structure
   - [ ] Create `outputs/` directory
   - [ ] Create `outputs/analysis/` subdirectory
   - [ ] Create `outputs/reports/` subdirectory
   - [ ] Create `outputs/logs/` subdirectory
   - [ ] Verify all 4 directories were created successfully
   ```

   **CORRECT PATTERN - Using Headers for Grouping:**
   ```markdown
   ### Step 2.2: Validate Configuration Files

   Check git configuration:
   - [ ] Verify `~/.gitconfig` exists
   - [ ] Extract user.name from gitconfig
   - [ ] Document git version

   Check SSH configuration:
   - [ ] Verify `~/.ssh/config` exists
   - [ ] Count number of host entries
   - [ ] Document file permissions

   - [ ] All configuration validations completed
   ```

   **INCORRECT PATTERN - Parent Before Children (FORBIDDEN):**
   ```markdown
   - [ ] Create directory structure:  ❌ WRONG - parent before children
     - [ ] Create outputs/
     - [ ] Create analysis/
     - [ ] Create reports/
   ```

   **INCORRECT PATTERN - Summary in Middle (FORBIDDEN):**
   ```markdown
   - [ ] Create outputs/ directory
   - [ ] All directories created  ❌ WRONG - summary before completion
   - [ ] Create analysis/ subdirectory
   - [ ] Create reports/ subdirectory
   ```

   **KEY PRINCIPLES:**
   1. Work flows TOP to BOTTOM only
   2. Components are completed BEFORE summaries
   3. Parent items come at the END, never the beginning
   4. Use descriptive headers instead of parent checkboxes
   5. Summary checkboxes should verify/confirm completed work

E3. SEQUENTIAL ORDER
   - Checkboxes MUST appear in exact order they will be completed
   - NEVER require marking items above current position
   - Flow is ALWAYS top to bottom
   - Summary checkboxes come AFTER component items, never before
   - Each phase must complete ALL its checkboxes before moving to next phase
   - NO go back and update or see below instructions allowed
   - FORBIDDEN PATTERNS:
      - Mark item complete in section above
      - Update the section checklist
      - See checklist below
      - Return to phase and mark complete
      - Any instruction requiring movement except forward
      - Parent checkbox items that have child checkbox items beneath them
      - Summary checkboxes that appear BEFORE their component items
      - Any checklist structure requiring backward movement to complete

E4. CHECKBOX FORMATTING REQUIREMENTS
   - NEVER place checkboxes next to step numbers
   - Step numbers should be bold headings without checkboxes
   - Place checkboxes ONLY on specific actionable items
   - DO NOT include separate REMINDER blocks between checklist items (worker agents only see batch items, not surrounding text)
   - If a reminder is needed, integrate it INTO the checklist item itself as part of the self-contained prompt

   CORRECT PATTERN for grouped items:
   ```markdown
   ### Step 1.1: Create subdirectory structure
   Create the following subdirectories:
   - [ ] Create `outputs/analysis/` for raw analysis data
   - [ ] Create `outputs/reports/` for generated reports
   - [ ] Create `outputs/documentation/` for user-facing docs
   ```

   INCORRECT PATTERN (FORBIDDEN):
   ```markdown
   - [ ] Create subdirectory structure:
     - [ ] Create `outputs/analysis/` for raw analysis data
     - [ ] Create `outputs/reports/` for generated reports
   ```

==============================================
SECTION F: EXECUTION REQUIREMENTS (FOR WORKER AGENTS)
==============================================

F1. FIVE-STEP EXECUTION PATTERN
   Tasks must be executed following this pattern:
   ```
   READ → IDENTIFY → EXECUTE → UPDATE → REPEAT
   ```
   - READ: Always read the task file before ANY action
   - IDENTIFY: Find the FIRST unchecked `- [ ]` item
   - EXECUTE: Complete ONLY that single identified item
   - UPDATE: Mark ONLY that item as `- [x]`
   - REPEAT: Return to READ for the next action

F2. PROHIBITED ACTIONS
   - Working from memory of previous task state
   - Executing multiple checklist items at once
   - Skipping ahead to later phases
   - Assuming any item is complete without verification
   - Delegating across phase boundaries — must not spawn a subagent for items spanning multiple phases; must not delegate the F1 loop itself; a subagent receives work from a SINGLE checklist item only
   - Skipping phase-gate QA — must spawn rf-qa after completing all items in Phase 2+; proceeding to the next phase without a passing QA gate is prohibited (see I15-I16)
   - Skipping post-completion validation — must run both rf-qa structural and rf-qa-qualitative operational validation before marking the task Done (see I17)

#### F2a. Item Execution Discipline

**Definition:** Multi-item execution occurs when an agent identifies multiple unchecked items and executes work for more than one, or marks more than one item as `[x]`, before returning to the READ step of the F1 loop. This violates the one-item-at-a-time discipline required within each agent session.

**Note:** Rigorflow legitimately groups checklist items into batches for processing across sessions — that is how the script manages context efficiently. The rules below govern agent behavior *within* a session, not how items are grouped *across* sessions.

**Violation examples:**
- Reading the task file, identifying items 2.3 and 2.4, and executing both before marking either complete
- Marking item 2.3 as `[x]` and item 2.4 as `[x]` in a single Edit operation on the task file
- Completing item 2.3's work, then immediately starting 2.4's work without re-reading the task file

**Why multi-item execution fails:**
- Context overflow: executing multiple items accumulates context that exceeds working limits, causing partial completion or hallucination
- Lost progress: if execution crashes or times out mid-execution, none of the in-flight items are marked complete — all progress is lost
- State drift: the task file on disk may have been modified by another process between items; skipping re-read causes the executor to work from stale state

**Parallel spawning exception:** When consecutive checklist items within the SAME phase spawn INDEPENDENT subagents (agents that do not read each other's outputs), the executor MAY spawn all such agents in parallel using multiple Agent tool calls in a single message. Each agent operates in isolated context. The executor MUST still mark each item individually as the corresponding agent completes. This exception does NOT apply to items that have data dependencies on each other.

F3. UNIVERSAL REQUIREMENTS
   - EVERY checklist item is REQUIRED - no optional items
   - ALL steps MUST be completed in EXACT sequential order
   - ALL referenced files MUST be reviewed before use
   - ALL created files MUST include ALL mandatory elements
   - NO assumptions or interpretations - follow instructions EXACTLY
   - EVERY checkbox MUST be marked with [x] as completed

F4. TASK FILE MODIFICATION RESTRICTIONS
   Worker agents MAY ONLY modify the task file to:
   1. Check off completed items ([ ] to [x])
   2. Update frontmatter fields per protocol
   3. Add entries to Task Log / Notes section
   4. FOR DYNAMIC TASKS: Add items within DYNAMIC CONTENT MARKER sections

F5. FRONTMATTER UPDATE PROTOCOL
   - Upon Task Start: Update status to "🟠 Doing" and start_date
   - Upon Completion: Update status to "🟢 Done" and completion_date
   - If Blocked: Update status to "⚪ Blocked" and blocker_reason
   - After Each Work Session: Update updated_date

==============================================
SECTION G: CONTEXT FOR HEADLESS AGENTS
==============================================

G1. Framework context files (ib_agent_core.md, quality_gates.md, anti_hallucination_task_completion_rules.md, anti_sycophancy.md, file_conventions.md) are NOT automatically loaded into headless worker agents.

G2. If an action requires following conventions from these files, either:
   - Reference the specific rule file in that checklist item, OR
   - Reference a template that already incorporates those conventions (preferred)

G3. Task-specific context should be embedded directly in action items, NOT read in separate "context loading" steps.

G4. PREVIOUS STAGE OUTPUTS (for dependent tasks)
   - The orchestrator MUST list all outputs from previous stages needed as inputs
   - Format: `[Output Type]: [path/to/output.md] - [Purpose]`
   - These should be EMBEDDED in the action items that need them

==============================================
SECTION H: TOOL SPECIFICATION
==============================================

H1. By default, rely on the model to select appropriate tools - do NOT include tool guidance unless a SPECIFIC tool is required for a particular reason.

H2. ONLY specify tools in a checklist item when a SPECIFIC tool is required for a particular reason.

H3. When tool specification IS needed, embed it in the checklist item itself:
   - Example: "...use the Bash tool to run `npm test` (not Read/Write) because we need to execute the test runner..."
   - Example: "...use Glob to find all *.ts files in src/ (not Bash find) for efficient pattern matching..."

H4. Tool selection matrix for reference when building tasks:
   | Operation | Primary Tool | When to Specify |
   |-----------|--------------|-----------------|
   | File Discovery | Glob | Only if Bash find would be incorrect |
   | Content Search | Grep | Only if specific search behavior needed |
   | File Reading | Read | Rarely - model handles this |
   | File Creation | Write | Rarely - model handles this |
   | File Modification | Edit | Rarely - model handles this |
   | Command Execution | Bash | Specify when specific command required |

==============================================
SECTION I: ADDITIONAL GUIDELINES
==============================================

NOTE: Section J (Error Handling) and Section K (Example Patterns) follow below.

I1. USE EXPLICIT DIRECTIVE LANGUAGE
   - Always use "YOU MUST" for requirements
   - Use "DO NOT" for prohibitions
   - Avoid passive voice or suggestions
   - Every instruction must be unambiguous

I2. EXTREME GRANULARITY REQUIRED
   - Break down every action into specific, concrete steps
   - Include exact file paths, not general directories
   - Specify exact content requirements, not general descriptions
   - If a step could be interpreted multiple ways, it needs more detail

I3. INCREMENTAL FILE MODIFICATION
   - Require agents to add content incrementally as they progress
   - Explicitly state "DO NOT attempt to complete entire files at once"
   - Include save points after major sections

I4. PARENT TASK RELATIONSHIPS
   - Always specify the parent task in frontmatter
   - List tasks this depends on
   - Note which tasks are blocked by this one

I5. ALL REQUIREMENTS ARE ABSOLUTE
   - Everything in the task is required
   - There are no "nice-to-haves" or optional items
   - If something might be optional, it doesn't belong in the task

I6. DYNAMIC CONTENT HANDLING
   - If a task needs to build lists or track items discovered during execution:
      - Use inline tracking within the current phase
      - Place dynamic content markers where content will be added
      - Never create separate "tracking" sections that require jumping around
   - For tasks with fixed content: mark task_type: "static" in frontmatter
   - For tasks needing dynamic content: mark task_type: "dynamic" in frontmatter
   - CRITICAL: Even dynamic content must maintain sequential flow:
      - Discovery happens BEFORE use
      - Creation happens BEFORE verification
      - Each item is marked complete WHERE IT IS DONE, not elsewhere

I7. EXPLICIT TEMPLATE USAGE
   When instructing to use a template, provide explicit steps:
   - Specify exact template path
   - Require reading template with specific tool
   - List all placeholders to replace
   - Specify output location
   - Never assume implicit template usage

I8. MANDATORY TEMPLATE USAGE
   - This template MUST be used for ALL general MDTM task creation
   - ANY instruction to "create a task" implicitly means "use the appropriate template"
   - Agents MUST NEVER create tasks without using templates
   - Even if not explicitly stated, template usage is ALWAYS required
   - The phrase "create an MDTM task" ALWAYS means:
      - Read the appropriate template file
      - Replace placeholders
      - Write to specified location

I9. HALLUCINATION PREVENTION SYSTEM
   - Add explicit warning against fabricating information at all content creation points
   - Require 100% accuracy based on source materials
   - Include incremental save requirements to prevent memory overflow
   - Specify DO NOT assume, hallucinate, or make up any information repeatedly

I10. CRITICAL WORKFLOW COMPLIANCE REINFORCEMENT
   - Add compliance verification at multiple levels throughout the task
   - Include HIGHEST CRITICAL and CRITICAL warning at content creation points
   - Require re-reading of governing workflow documents after each major deliverable
   - Include multi-process compliance verification for complex deliverables

I11. EARLY STATUS UPDATE PROTOCOL
   - Status update to "🟠 Doing" must be the first action in the task
   - Context review comes after status update to prevent workflow violations

I12. VERIFICATION IS INTEGRATED (NO SEPARATE VERIFICATION ITEMS)
   - Content verification MUST be integrated INTO the action item itself, not as separate checklist items
   - Each action item should include an "ensuring..." clause that specifies what must be verified
   - The QA process handles inter-batch verification — phase-gate rules defined in I15-I16
   - Do NOT create separate "verify the file" or "confirm completion" checklist items
   - Example: "...create the file X at path Y containing Z, ensuring all content is accurate, all sections are complete, and no placeholders remain..."

I13. POST-COMPLETION ACTIONS (final task items only)
   - Every task MUST include a Post-Completion Actions section
   - Include items for: updating frontmatter (status, completion_date, updated_date), logging completion to Execution Log
   - Post-completion validation items (I17) handle output verification before the frontmatter update
   - Do NOT create a separate "Task Completion and Handoff Protocol" section in the task body
   - Orchestrator info about handoff lives in ib_agent_core.md, not in individual task files

I14. ANTI-HALLUCINATION CONTROLS INTEGRATION
   - Every task MUST reference the anti-hallucination requirements from `anti-hallucination_task_completion_rules.md`
   - Include evidence table requirements for any task involving technical claims
   - Add explicit warnings against fabricating information at all content creation points
   - Require agents to document negative evidence when verification fails
   - Include the strict definition of "COMPLETE" in task verification sections within each subtask checklist
   - For tasks requiring technical documentation or claims:
      - Include evidence table template in task structure
      - Require source verification for every claim
      - Add checkpoints for evidence verification
      - Mandate negative evidence documentation

I15. PHASE-GATE QA ENFORCEMENT
   Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint between the primary execution phase and any subsequent phase that depends on its outputs. The orchestrator MUST insert QA gate checklist items at these boundaries.

   A phase-gate QA checkpoint consists of:
   1. An aggregation item that collects all outputs from the preceding phase
   2. A QA agent spawn item that verifies those outputs against defined criteria
   3. A conditional-action item that proceeds to the next phase on PASS or triggers a fix cycle on FAIL

   The QA agent spawn item MUST be a self-contained checklist item following B2's 6-element pattern. It MUST include: the agent to spawn (rf-qa or rf-qa-qualitative), the phase type, the input files, the output report path, the verdict handling (proceed on PASS, fix cycle on FAIL), and the error handling clause.

I16. QA GATE VERDICT AND FIX CYCLES
   QA agents produce binary verdicts: PASS or FAIL. Any issue of any severity (CRITICAL, IMPORTANT, or MINOR) results in FAIL.

   Fix cycle rules per gate type:

   | Gate Type | Max Fix Cycles | After Max Reached |
   |-----------|---------------|-------------------|
   | research-gate | 3 | HALT and escalate to user |
   | synthesis-gate | 2 | Unresolved issues become Open Questions |
   | report-validation | 3 | HALT and escalate to user |
   | task-integrity | 2 | Unresolved issues become Open Questions |
   | Any qualitative gate | 3 | HALT and escalate to user |

   Each fix cycle MUST re-verify ALL previously failed items plus check for new issues introduced by fixes. If the number of issues increases across cycles, flag this as a systemic problem.

   The orchestrator MUST encode fix cycle logic as conditional-action items or as explicit IF/ELSE instructions within the QA gate checklist item.

I17. POST-COMPLETION VALIDATION PROTOCOL
   Before the frontmatter status is set to Done, the task MUST include validation items that verify:
   1. All `- [ ]` items have been marked `- [x]` (no items skipped)
   2. All output files specified in checklist items exist on disk (verified via Glob)
   3. Any blocker entries in the Task Log have resolution notes
   4. If the task modified source code: all relevant tests pass

   These items appear in the ## Post-Completion Actions section of PART 2, BEFORE the frontmatter update item.

   The automated QA workflow references in C4 and I13 are satisfied by these validation items — no external workflow is required when the task file includes them.

I18. TESTING REQUIREMENTS FOR CODE-MODIFYING TASKS
   If a task creates or modifies source code files (not documentation, not configuration), the orchestrator MUST include at least one testing checklist item. This item MUST:
   1. Specify the test command to run (e.g., "Run `uv run pytest tests/path/ -v`")
   2. Define pass criteria (e.g., "all tests pass with no regressions")
   3. Specify where test results are captured (e.g., a test-results file in phase-outputs/)
   4. Follow the self-contained item pattern from B2

   The orchestrator determines appropriate test scope based on the changes being made. At minimum, unit tests covering modified code are required.

Remember: The goal is to create tasks that implement workflow requirements with
complete granularity, preventing any interpretation or deviation from the governing workflow.

==============================================
SECTION J: ERROR HANDLING GUIDANCE
==============================================

Error handling is embedded directly in each checklist item. When an item cannot be
completed, the agent logs the blocker to task notes then marks the item complete.
The blocker entry serves as the record for follow-ups.

J1. ERROR HANDLING PATTERN (embedded in every checklist item):
   "If unable to complete due to missing information, file access issues, or unclear
   requirements, log the specific blocker using the templated format in the ### Phase [N]
   Findings section of the ## Task Log / Notes at the bottom of this task file, then
   mark this item complete."

J2. KEY PRINCIPLES:
   - Items are NEVER left unchecked - everything gets marked complete
   - Success = output file exists
   - Failure = blocker logged to task notes
   - The task continues - other items may still be completable
   - Blockers are reviewed in follow-up tasks

J3. DO NOT block the entire task for individual item failures. Only mark the task
   as "⚪ Blocked" if ALL remaining items are blocked by the same issue.

==============================================
SECTION K: EXAMPLE PATTERNS (FOR ORCHESTRATOR REFERENCE)
==============================================

These patterns are for the orchestrator's reference when building tasks.
They should NOT appear in the output task file - replace them with actual content.

K1. FILE-BY-FILE PROCESSING PATTERN
   Use this pattern when processing multiple known files:

   ```markdown
   #### File: [filename1.ext] at [full/path/to/filename1.ext]

   - [ ] Read the file `[template.md]` at `[path/to/template.md]` to understand the required format and structure for [what you're creating/modifying], then read the file `[source-data.md]` at `[path/to/source-data.md]` to extract the specific content needed for this file including [specific data points], then create or update the file `[filename1.ext]` at `[full/path/to/filename1.ext]` with the content derived from the source data following the template format, ensuring all required sections are included and properly formatted, all content matches the source data accurately with no fabrication, formatting is correct, and no placeholder text remains. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
   ```

K2. MULTI-ITEM PROCESSING PATTERN
   For tasks with multiple similar items:

   **CRITICAL:** The orchestrator agent creating this task file MUST identify and enumerate
   ALL items that need processing during task setup. The worker agent MUST NEVER dynamically
   add checklist items - all items must be listed by the orchestrator before the worker begins.

   **Instructions for Orchestrator (creating task):**
   1. **Identify Items:** Use appropriate tools to identify all individual items that need processing in this phase.
   2. **Add Checklist Items:** For EACH identified item, add a self-contained checklist item.
   3. **Process Iteratively:** Each item is processed one by one, marked complete after its output is created.

   Pattern for each item (one self-contained item per file - NO separate verification items):
   ```markdown
   #### File: [filename1.ext] at [full/path/to/filename1.ext]

   - [ ] Read the file `[template.md]` at `[path/to/template.md]` to understand the required format including [specific format requirements], then read the file `[source-data.md]` at `[path/to/source-data.md]` to extract the content needed for this specific file including [data points to extract], then create or update the file `[filename1.ext]` at `[full/path/to/filename1.ext]` with content derived from the source following the template format, ensuring [specific requirements for this file], all content is accurate with no fabrication, and all required sections are present. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
   ```

################################################################################
################################################################################
##                                                                            ##
##                                                                            ##
##                    END OF PART 1: INSTRUCTIONS                             ##
##                                                                            ##
##                                                                            ##
################################################################################
################################################################################








################################################################################
################################################################################
##                                                                            ##
##                                                                            ##
##                    PART 2: TASK FILE TEMPLATE                              ##
##                    ==========================                              ##
##                                                                            ##
##     This PART 2 section IS the actual task file template.                  ##
##     When creating a task, copy everything from "# [Task Title]"            ##
##     to the end of the file, replacing all placeholders.                    ##
##                                                                            ##
##     The frontmatter at the top of this file is also part of the template.  ##
##                                                                            ##
##                                                                            ##
################################################################################
################################################################################
-->

# [Task Title]

## Task Overview

[Comprehensive description of what this task accomplishes and why it's necessary]

## Key Objectives

The following objectives MUST be achieved by this task:

1. **[Objective 1]:** [Specific, concrete outcome that must be produced]
2. **[Objective 2]:** [Specific, concrete outcome that must be produced]
3. **[Objective 3]:** [Specific, concrete outcome that must be produced]

## Prerequisites & Dependencies

### Parent Task & Dependencies
- **Parent Task:** [PARENT-TASK-ID] - [Brief description of parent task]
- **Blocking Dependencies:**
  - [DEPENDENCY-ID-1]: [What output from this task is needed]
  - [DEPENDENCY-ID-2]: [What output from this task is needed]
- **This task blocks:** [List any tasks waiting for this task's outputs]

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

**MANDATORY:** The orchestrator creating this task MUST explicitly list all relevant outputs from previous stages that serve as inputs for this task. The actual checklist items for reading these outputs appear in Phase 1, Step 1.4.

**Required Previous Stage Outputs:**
- **[Output Type 1]:** `[path/to/output1.md]` - [Purpose: what will be extracted/used from this file]
- **[Output Type 2]:** `[path/to/output2.md]` - [Purpose: what will be extracted/used from this file]
- **[Output Type 3]:** `[path/to/output3.md]` - [Purpose: what will be extracted/used from this file]

<!-- ORCHESTRATOR: Add all previous stage outputs that this task depends on. These will be read in Phase 1, Step 1.4. -->

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:
- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

## Detailed Task Instructions

<!-- ╔═══════════════════════════════════════════════════════════════════════════╗
     ║  ORCHESTRATOR INSTRUCTION BLOCK - REMOVE THIS ENTIRE BLOCK FROM OUTPUT   ║
     ║  This block is guidance for building the task, NOT part of the task.     ║
     ╚═══════════════════════════════════════════════════════════════════════════╝

**CRITICAL:** YOU MUST strictly follow ALL requirements and guidelines outlined in the governing workflow document for this task (e.g., the specific stage workflow document like `stage1_api_generation.md`). This includes all phases, steps, quality criteria, and logging requirements.

**⚠️ CHECKLIST STRUCTURE WARNING:**
When creating checklists, NEVER put parent/summary checkboxes before their component items. Components must be completed FIRST, summaries LAST. Use descriptive headers without checkboxes to group related items. Any summary checkbox must appear at the END of its component sequence.

**CRITICAL: SELF-CONTAINED CHECKLIST ITEMS (see Section B in Part 1 instructions)**

Due to session rollovers between batches, context loaded in early batches is NOT available in later batches. Therefore, EVERY checklist item MUST be self-contained - a complete prompt that embeds all context references, actions, and outputs in ONE PARAGRAPH.

**REQUIRED ELEMENTS IN EVERY CHECKLIST ITEM:**
1. **Context Reference + WHY** - What file(s) to read and why that context is needed
2. **Action + WHY** - What to do with that context and why
3. **Output Specification** - Exact file name, location, content requirements, template to follow
4. **Integrated Verification** - "ensuring..." clause (DO NOT assume, hallucinate, or make up any information - all content MUST be derived from source files, 100% accuracy required)
5. **Evidence on Failure Only** - Log to task notes ONLY if blocked or unable to complete (output file IS the evidence for success)
6. **Completion Gate** - "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

**FORBIDDEN:**
- Standalone "read context" items that don't produce output
- Separate verification/confirmation items (integrate verification into the action item itself)
- Multi-line/bulleted checklist items (must be single paragraph)
- Overly granular items (e.g., "create directory" alone - combine with the file creation that needs it)

**PREFERENTIAL (not mandatory):**
- Context source references - include when the action requires reading from a source file
- Output specifications - include when the action produces a file (not all actions create files)

**SELF-CONTAINED CHECKLIST ITEM EXAMPLE:**
```markdown
- [ ] Read the file `component-spec.md` at `docs/specs/component-spec.md` to extract the API interface requirements including method signatures and parameter types that must be implemented, then read the file `BaseHandler.ts` at `src/handlers/BaseHandler.ts` to understand the structural patterns and conventions used in existing handlers, then create the file `ApiHandler.ts` at `src/handlers/ApiHandler.ts` containing a TypeScript class that implements all methods from the spec with proper error handling and type annotations following the patterns from BaseHandler, ensuring the file includes the standard header comment block, exports the class as the default export, all methods from the spec are implemented with correct signatures, no content is fabricated beyond what sources explicitly state, and no placeholder or TODO comments remain. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

     END ORCHESTRATOR INSTRUCTION BLOCK
     ═══════════════════════════════════════════════════════════════════════════ -->

### Phase 1: Preparation and Setup
(Refer to [`[workflow_document].md#phase-1-preparation-and-setup`](path/to/workflow#phase-1-preparation-and-setup) for detailed requirements)

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

<!-- ╔═══════════════════════════════════════════════════════════════════════════╗
     ║  ORCHESTRATOR INSTRUCTION BLOCK - REMOVE THIS ENTIRE BLOCK FROM OUTPUT   ║
     ╚═══════════════════════════════════════════════════════════════════════════╝

### Context Loading Note (IMPORTANT)

**Framework context files** (ib_agent_core.md, quality_gates.md, anti_hallucination_task_completion_rules.md, anti_sycophancy.md, file_conventions.md) are NOT automatically loaded into headless worker agents. If an action requires following conventions from these files (e.g., file naming from file_conventions.md), either:
1. Reference the specific rule file in that checklist item, OR
2. Reference a template that already incorporates those conventions (preferred)

**Task-specific context** should be embedded directly in the action items that need it, NOT read in separate "context loading" steps. This is because session rollovers between batches mean any context read in batch 1 will be LOST by batch 3+.

**CORRECT APPROACH:** Each action item embeds its own context references:
```
- [ ] Read the spec file at [path] to understand [what], then create [output] at [path]...
```

**INCORRECT APPROACH (FORBIDDEN):** Separate context-reading items:
```
- [ ] Read spec file and log findings...  ❌ Context lost after session rollover
- [ ] Create output based on spec...       ❌ Spec context no longer available
```

     END ORCHESTRATOR INSTRUCTION BLOCK
     ═══════════════════════════════════════════════════════════════════════════ -->

**Step 1.1:** Update task status
- [ ] Update status to "🟠 Doing" and start_date to current date in frontmatter of this file, then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.` Once done, mark this item as complete.

### Task-Specific Context Files

<!-- ORCHESTRATOR: Replace these placeholders with actual context files for this task.
     These are listed here for human/orchestrator reference.
     The actual usage is EMBEDDED in Phase 2+ checklist items, NOT read separately. -->

- **Workflow/Process:** `[path/to/workflow_document.md]` - [Purpose]
- **Technical Spec:** `[path/to/technical_doc.md]` - [Purpose]
- **Template:** `[path/to/template.md]` - [Purpose]
- **Previous Stage Output:** `[path/to/output.md]` - [Purpose]

### Phase 2: [Main Execution Phase Name]
(Refer to workflow document for detailed requirements)

**Step 2.1:** [Specific action - e.g., "Create [component name]"]

- [ ] Read the file `[template.md]` at `[path/to/template.md]` to understand the required file structure including frontmatter format, mandatory sections, and content organization, then read the file `[source-content.md]` at `[path/to/source-content.md]` to extract the specific content that needs to be included (title, description, key information, etc.), then create the file `[output-file.md]` at `[exact/path/to/output-file.md]` containing all mandatory frontmatter fields populated with values from the source content, all required sections from the template with content derived from the source, and proper formatting per file conventions, ensuring no placeholder text or TODO comments remain, no content is fabricated or assumed beyond what sources explicitly state, and the content accurately reflects the source material. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.2:** [Next specific action]

- [ ] Read the file `[workflow-or-spec.md]` at `[path/to/workflow-or-spec.md]` to understand the specific requirements for [what this step accomplishes] including [key requirements to extract], then read the file `[existing-file.md]` at `[path/to/existing-file.md]` to understand the current state and what needs to be added or modified, then update the file `[existing-file.md]` at `[path/to/existing-file.md]` by adding [specific content] in the [specific section] following the format and conventions established in the workflow document, ensuring the added content is accurate, properly formatted, integrates correctly with existing content, and no information is fabricated beyond what sources state. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.3:** [Continue with detailed steps]

- [ ] Read the file `[source.md]` at `[path/to/source.md]` to extract the [specific requirements or data] needed, then create or update the file `[output-file.md]` at `[exact/path/to/output-file.md]` implementing all requirements from the source including [specific aspects], ensuring no content is fabricated or assumed beyond what the source explicitly states, all required sections are present and complete, all cross-references and links are functional, and no TODO/FIXME markers or placeholder text remains. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

<!-- ORCHESTRATOR: For file-by-file or multi-item processing patterns, see Section K in PART 1 instructions.
     Replace this comment with actual checklist items for your specific files. -->

### Phase Gate: Quality Verification

<!-- ORCHESTRATOR: Insert QA gate items here when Phase 2 produces outputs that Phase 3 depends on. Use the QA agent appropriate for the output type. See I15-I16 for rules. Remove this comment block and replace with actual QA gate items, or remove this entire section if no QA gate is needed for this task. -->

**Step PG.1**

- [ ] [QA GATE ITEM — Replace with actual QA agent spawn item following B2 pattern. Example: "Spawn rf-qa in [phase-type] mode to verify all Phase 2 outputs at [paths], ensuring the agent writes its report to [output-path] and returns a PASS/FAIL verdict. If FAIL, read the report, address all findings in the relevant Phase 2 output files, then re-spawn rf-qa in fix-cycle mode (max [N] cycles per I16). If unable to complete due to agent spawn failure, log the blocker in ### Phase Gate Findings below, then mark this item complete."]

### Phase [N]: Testing & Verification

<!-- ORCHESTRATOR: Insert testing items here when the task creates or modifies source code files. See I18 for when this phase is required. Remove this comment block and replace with actual testing items, or remove this entire section if the task is documentation-only or configuration-only. -->

**Step [N].1**

- [ ] [TESTING ITEM -- Replace with actual test execution item following B2 pattern. Example: "Run the test suite covering the modified code by executing `[test command]` to verify all tests pass with no regressions, ensuring the test output shows 0 failures and no errors in the modified modules, then capture the results to `[output-path]`. If tests fail, read the failure output to identify the root cause, attempt to fix the failing tests or the source code causing failures, then re-run. If unable to resolve test failures, log the specific failures using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."]

### Phase 3: [Additional Phase if Needed]
(Refer to workflow document for detailed requirements)

**Step 3.1:** [Specific action]

- [ ] Read the file `[previous-output.md]` at `[path/to/previous-output.md]` from Phase 2 to understand [what was created and what data to use], then read the file `[workflow-or-spec.md]` at `[path/to/workflow-or-spec.md]` to understand the requirements for this phase including [specific requirements], then create or update the file `[output-file.md]` at `[exact/path/to/output-file.md]` by [specific action] using the data from the previous output and following the requirements in the workflow document, ensuring all requirements are met, content is accurate to source materials with no fabrication, all sections are complete, and no placeholder text remains. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

## Post-Completion Actions

- [ ] Verify all task outputs by using Glob to confirm every output file specified in checklist items exists on disk, ensuring no expected deliverables are missing. If any files are missing, check the Task Log for blockers explaining the absence. If files are missing without documented reason, log the gap in ### Follow-Up Items below, then mark this item complete.

- [ ] If this task modified source code files, run the relevant test suite (per the testing items in the execution phases) to confirm all tests still pass with no regressions, ensuring the final state of the codebase is clean. If tests were already run and passed in an earlier phase and no subsequent changes were made, note "Tests verified in Phase [N]" in the Task Log and mark this item complete.

- [ ] Create a ### Task Summary section at the top of the ## Task Log / Notes section at the bottom of this task file, using the templated format provided there. The summary should document: work completed (referencing key outputs and files created/modified), challenges encountered during execution, any deviations from the planned process and their rationale, and blockers logged during execution with their resolution status. Once the summary is complete, mark this item as complete.

- [ ] Update `completion_date` and `updated_date` to today's date and update task status to "🟢 Done" in frontmatter, then add an entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.` Once done, mark this item as complete.

## Task Log / Notes 📋

### Task Summary
<!-- Fill this section in Post-Completion Actions -->

**Completion Date:** [YYYY-MM-DD]

**Work Completed:**
- [Key output 1]: [Brief description]
- [Files created]: [List with paths]
- [Files modified]: [List with paths]

**Challenges Encountered:**
- [Challenge]: [How addressed] OR None

**Deviations from Process:**
- [Deviation]: [Rationale] OR None

**Blockers Logged:**
- [Step X.Y]: [Description] - **Status:** [Resolved/Unresolved] OR None

**Follow-Up Required:** [Yes/No] - [Description if yes]

### Execution Log

<!-- TEMPLATE FOR EXECUTION LOG ENTRIES:
**[YYYY-MM-DD HH:MM]** - [Action taken]: [Brief description of what was done and outcome]
-->

**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.

**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.

### Phase 1 - [Phase Name] Findings

<!-- TEMPLATE FOR PHASE FINDINGS:
**[YYYY-MM-DD HH:MM]** - [Step X.Y]: [Finding or blocker description]
- **Status:** [Completed | Blocked]
- **Details:** [Specific information about what was found, created, or what blocked completion]
- **Blocker Reason (if blocked):** [Specific reason why this could not be completed]
- **Files Affected:** [List of files read, created, or modified]
-->

### Phase 2 - [Phase Name] Findings

<!-- TEMPLATE FOR BLOCKER ENTRIES:
**[YYYY-MM-DD HH:MM]** - Step 2.1 BLOCKED:
- **Blocker Reason:** [Specific reason - e.g., "Source file `component-spec.md` not found at expected path `docs/specs/component-spec.md`"]
- **Attempted:** [What was tried before determining blocker]
- **Required to Unblock:** [What information or action is needed to proceed]
-->

### Phase 3 - [Phase Name] Findings

### Phase Gate Findings

_QA gate verdicts, fix cycle counts, and unresolved issues are recorded here._

### Follow-Up Items Identified

<!-- TEMPLATE FOR FOLLOW-UP ITEMS:
- **[Priority: High/Medium/Low]** [Description of follow-up needed] - Identified in Step [X.Y]
-->

### Deviations from Process

<!-- TEMPLATE FOR DEVIATIONS:
**[YYYY-MM-DD HH:MM]** - Deviation from [Step X.Y]:
- **Expected:** [What the process specified]
- **Actual:** [What was done instead]
- **Rationale:** [Why this deviation was necessary]
-->
