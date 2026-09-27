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
==============================================
TASK CREATION GUIDELINES - MANDATORY FOR ORCHESTRATOR
==============================================

These guidelines are MANDATORY for the orchestrator when creating tasks. Every task MUST implement the governing workflow document requirements with complete granularity. this template is used to create detailed, unambiguous tasks for AI agents.

**IMPORTANT: WORKFLOW DOCUMENT AVAILABILITY CHECK**
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

1. **WORKFLOW DOCUMENT DEEP INTEGRATION** [WORKFLOW-DEPENDENT]
   - BEFORE creating task content: Thoroughly review the complete governing workflow document
   - Extract EVERY requirement, phase, step, and quality standard from the workflow
   - Map EVERY workflow element to corresponding task elements
   - Include ALL workflow verification criteria in task verification section

2. **COMPLETE GRANULAR BREAKDOWN**
   - Break down EVERY workflow phase into atomic, verifiable checklist items
   - Create individual checklist items for EVERY file, component, or iteration
   - NO high-level or bulk operations allowed - everything must be granular
   - Include exact file paths, specific requirements, and measurable outcomes

3. **ITERATIVE PROCESS STRUCTURE**
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

4. **CROSS-STAGE INTEGRATION** [WORKFLOW-DEPENDENT]
   - EVERY phase must explicitly specify inputs from previous stages
   - Include specific file paths to analysis reports, verified outputs, etc.
   - Require consultation of previous stage outputs before proceeding
   - Include validation steps against previous stage findings

5. **WORKFLOW COMPLIANCE ENFORCEMENT** [WORKFLOW-DEPENDENT]
   - Include explicit workflow adherence requirements in every phase
   - Reference specific workflow document sections throughout task
   - Copy quality standards directly from workflow documents
   - Include workflow verification criteria in task verification

6. **MANDATORY TASK SECTIONS**
   Every task MUST include these sections:

   **Workflow Compliance Declaration:** [WORKFLOW-DEPENDENT]
   ```markdown
   ## MANDATORY WORKFLOW COMPLIANCE

   **CRITICAL:** This task implements [Stage X] from [`stageX_workflow.md`](path).
   YOU MUST strictly follow ALL requirements from the governing workflow document.
   ```
   Note: This section is INFORMATIONAL only - no checklist items here.

   **Cross-Stage Integration Requirements:** [WORKFLOW-DEPENDENT]
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

   **CRITICAL RULE**: NO CHECKLIST ITEMS may appear before Phase 1 begins. The template structure ensures:
   - Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable)
   - All checklist items for context review and previous stage inputs appear IN Phase 1, Steps 1.2-1.4

7. **AGENT EXECUTION REQUIREMENTS**
   - Agents MUST complete items in exact sequential order
   - Agents MUST reference workflow document continuously
   - Agents MUST NOT attempt bulk or batch operations
   - Agents MUST update outputs incrementally after each item

8. **VERIFICATION INTEGRATION**
   - Include ALL quality gates from quality_gates.md applicable to the workflow
   - Copy verification criteria directly from workflow documents
   - Ensure workflow compliance verification before task completion

9. DETAILED CHECKLISTS ARE MANDATORY
   - Checkboxes MUST appear in the exact order they will be completed
   - Every task MUST have step-by-step checklists that agents complete sequentially
   - Never require marking items above the current working position
   - Never reference checkboxes that appear later in the document
   - Each checklist item must be atomic and verifiable
   - Agents MUST mark each item complete before moving to the next
   - DO NOT create high-level or vague checklist items
   - NEVER create parent checkbox items with child checkbox items - use descriptive headers instead
   - For grouped tasks, use a header without checkbox, then list individual items with checkboxes

9A. CRITICAL CHECKLIST STRUCTURE RULES
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

9B. EVIDENCE AND VERIFICATION REQUIREMENTS (CRITICAL FOR QA)
   - **EVERY checklist item MUST include verifiable evidence**
   - **EVERY checklist item MUST specify the exact file name and full path being worked on**
   - Evidence must be ONE of these types:
     1. **Task Log Entry**: "and log to task notes: [specific findings]"
     2. **File Output**: "in file [filename.ext] at path: [full/path]" or "creates file at: [full/path/filename.ext]"
     3. **Verification Record**: "Re-read file [filename.ext] at [full/path] and log to task notes: [what verified]"

   **REQUIRED CHECKLIST ITEM PATTERNS:**

   **Pattern A - File Reading with Logging:**
   ```markdown
   - [ ] Read file [filename.ext] at [full/path/to/file.ext] and log to task notes in ### [Phase Name] Findings: [specific information to extract], then mark this item complete
   ```

   **Pattern B - File Creation/Modification:**
   ```markdown
   - [ ] [Action verb] file [filename.ext] at path: [full/path] and log to task notes in ### [Phase Name] Findings: [what was done], then mark this item complete
   ```

   **Pattern C - Verification:**
   ```markdown
   - [ ] Re-read file [filename.ext] at [full/path] and log to task notes in ### [Phase Name] Findings: [what you verified], then mark this item complete
   ```

   **Pattern D - Existence Check:**
   ```markdown
   - [ ] Check if file [filename.ext] exists at path: [full/path] and log to task notes in ### [Phase Name] Findings: [status - exists/does not exist]. If [filename.ext] does not exist, [action to take], then mark this item complete
   ```

   **CORRECT - Active Voice with Evidence:**
   ```markdown
   - [ ] Read file `config.yaml` at `/full/path/config.yaml` and log to task notes in ### Phase 1 Findings: Database connection settings and retry policy values, then mark this item complete
   - [ ] Add frontmatter to file `output.md` at path: `/full/path/output.md` and log to task notes in ### Phase 2 Findings: All frontmatter fields added with values, then mark this item complete
   - [ ] Re-read file `output.md` at `/full/path/output.md` and log to task notes in ### Phase 2 Findings: Confirmed all required fields present and properly formatted, then mark this item complete
   ```

   **INCORRECT - Passive Voice / No Evidence (FORBIDDEN):**
   ```markdown
   - [ ] File read: configuration ❌ Passive voice, no path, no logging location
   - [ ] Update output ❌ Which file? Where? No logging requirement
   - [ ] Verify completeness ❌ No logging requirement, no "then mark complete"
   ```

10. USE EXPLICIT DIRECTIVE LANGUAGE
   - Always use "YOU MUST" for requirements
   - Use "DO NOT" for prohibitions  
   - Avoid passive voice or suggestions
   - Every instruction must be unambiguous

11. EXTREME GRANULARITY REQUIRED
   - Break down every action into specific, concrete steps
   - Include exact file paths, not general directories
   - Specify exact content requirements, not general descriptions
   - If a step could be interpreted multiple ways, it needs more detail

12. INCREMENTAL FILE MODIFICATION
   - Require agents to add content incrementally as they progress
   - Explicitly state "DO NOT attempt to complete entire files at once"
   - Include save points after major sections

13. PARENT TASK RELATIONSHIPS
   - Always specify the parent task in frontmatter
   - List tasks this depends on
   - Note which tasks are blocked by this one

14. ALL REQUIREMENTS ARE ABSOLUTE
   - Everything in the task is required
   - There are no "nice-to-haves" or optional items
   - If something might be optional, it doesn't belong in the task

15. STRICT SEQUENTIAL FLOW REQUIREMENTS
   - Checkboxes MUST appear in the EXACT order they will be completed
   - NEVER require marking items above the current working position
   - NEVER reference checkboxes that appear later in the document
   - Flow is ALWAYS top to bottom, no exceptions
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

16. DYNAMIC CONTENT HANDLING
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

17. CHECKBOX FORMATTING REQUIREMENTS
   - NEVER place checkboxes next to step numbers
   - Step numbers should be bold headings without checkboxes
   - Place checkboxes ONLY on specific actionable items
   - Include explicit reminder after EVERY checklist section
   - Each reminder MUST state: "**REMINDER:** YOU MUST mark each checkbox above with [x] as you complete it before proceeding to the next item."
   
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

18. EXPLICIT TEMPLATE USAGE
- When instructing to use a template, provide explicit steps:
   - Specify exact template path
   - Require reading template with specific tool
   - List all placeholders to replace
   - Specify output location
   - Never assume implicit template usage

19. MANDATORY TEMPLATE USAGE
   - This template MUST be used for ALL general MDTM task creation
   - ANY instruction to "create a task" implicitly means "use the appropriate template"
   - Agents MUST NEVER create tasks without using templates
   - Even if not explicitly stated, template usage is ALWAYS required
   - The phrase "create an MDTM task" ALWAYS means:
      - Read the appropriate template file
      - Replace placeholders
      - Write to specified location

20. MANDATORY REPEATED REMINDERS
    - Include repeated reminders about actually completing the work associated with each checkbox before marking the checkbox complete
    - Include sequential completion reminders after every 3-5 checklist items
    - Include workflow adherence reminders after every major phase
    - Use exact formatting and directive language specified
    - Place reminders at all transition points and before major actions
    - NEVER assume agents will remember - they need constant reinforcement

21. HALLUCINATION PREVENTION SYSTEM**
   - Add explicit warning against fabricating information at all content creation points
   - Require 100% accuracy based on source materials
   - Include incremental save requirements to prevent memory overflow
   - Specify DO NOT assume, hallucinate, or make up any information repeatedly

22. CRITICAL WORKFLOW COMPLIANCE REINFORCEMENT
   - Add compliance verification at multiple levels throughout the task
   - Include HIGHEST CRITICAL and CRITICAL warning at content creation points
   - Require re-reading of governing workflow documents after each major deliverable
   - Include multi-process compliance verification for complex deliverables

23. EARLY STATUS UPDATE PROTOCOL
   - Stats update to "🟠 Doing" must be the first action in the task
   - Context review comes after status update to prevent workflow violations

24. Content Verification Integration
   - Content verification MUST be integrated into each phase where content iscreated
   - Include the following erification steps at the completion of EACH content creation step:
   - [ ] Content is accurate to source materials
   - [ ] All required sections are present and complete
   - [ ] Cross-references and links are functional
   - [ ] No "TODO" or "FIXME" makers or template placeholders remain

25. TASK COMPLETION HANDOFF PROTOCOL
   - Every task MUST include a final phase for task completion handoff
   - The final phase MUST include explicit instructions to notify the assigning agent
   - Reference `ib_agent_core.md` and other system rules for handoff requirements
   - Inclue all necessary completion verification before handoff

26. ANTI-HALLUCINATION CONTROLS INTEGRATION
   - Every task MUST reference the anti-hallucination requirements from `anti-hallucination_task_completion_rules.md`
   - Include evidence table requirements for any task involving technical claims
   - Add explicit warnings against fabricating information at all content creation points
   - Require agents to document negative evidence when verification fails
   - Include the strict definition of "COMPLETE" in task verifcation sections within each subtask checklist
   - For tasks requiring technical documentation or claims:
      - Include vidence table template in task structure
      - Require source verification for every claim
      - Add checkpoints for evidence verification
      - Mandate negative evidence documentation

Remember: The goal is to create tasks that implement workflow requirements with complete granularity, preventing any interpretation or deviation from the governing workflow.

==============================================
END OF ENHANCED GUIDELINES - TEMPLATE BEGINS BELOW
==============================================
-->

## MANDATORY WORKFLOW COMPLIANCE

**CRITICAL:** This task implements [Stage Name] from [`[workflow_document].md`](path/to/workflow).
YOU MUST strictly follow ALL requirements from the governing workflow document.

## Universal Task Requirements

The following requirements are **MANDATORY** and apply to **ALL** aspects of this task:

1. **EVERY** checklist item is **REQUIRED** - there are NO optional items
2. **ALL** steps MUST be completed in EXACT sequential order
3. **ALL** workflow document sections MUST be consulted before proceeding with each phase
4. **ALL** previous stage outputs MUST be reviewed and validated before use
5. **ALL** iterative processes MUST be completed item-by-item with incremental updates
6. **NO** bulk or batch operations are permitted
7. **ALL** generated content MUST reference specific workflow requirements
8. **ALL** quality standards from the workflow MUST be met

## Cross-Stage Integration Requirements

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

This section describes cross-stage integration requirements for this task. The orchestrator must specify which previous stage outputs are required. The actual checklist items for reading and verifying these outputs appear in Phase 1, Step 1.4.

**Previous Stage Inputs Required:**
[Orchestrator must specify exact inputs from previous stages]
- Analysis reports from Stage X: [exact paths and purpose]
- Verified outputs from Stage Y: [exact paths and purpose]
- Required context files: [exact paths and purpose]

**What will be verified in Phase 1:**
- All previous stage outputs will be read and reviewed
- Required inputs will be validated for completeness and accuracy
- Cross-references will be prepared for current stage execution

# [Task Title]

## Task Overview

[Comprehensive description of what this task accomplishes, why it's necessary, and how it fits into the larger workflow. Reference the parent workflow stage or process that requires this task.]

**Parent Workflow/Process:** [Link to parent workflow document and specific stage/section]

## MANDATORY EXECUTION REQUIREMENTS

**CRITICAL:** YOU MUST complete EVERY item in EVERY checklist and phase in EXACT sequential order. NO checklist item, step, or sub-item may be skipped or completed out of order. Work MUST NOT proceed to any subsequent item until ALL preceding items are fully completed and marked with checkmarks. This requirement is ABSOLUTE and applies to ALL sections of this task.

**CRITICAL:** This task MUST be executed following the Five-Step Execution Pattern defined in `ib_agent_core.md` under "Standard Directives for AI-Executed Tasks". 

### The Five-Step Pattern (NON-NEGOTIABLE):
```
READ → IDENTIFY → EXECUTE → UPDATE → REPEAT
```

1. **READ** - Always use `read_file` on this task file before ANY action
2. **IDENTIFY** - Find the FIRST unchecked `- [ ]` item and state: "Current Position: Line [XXX]"
3. **EXECUTE** - Complete ONLY that single identified item
4. **UPDATE** - Mark ONLY that item as `- [x]` using `apply_diff`
5. **REPEAT** - Return to step 1 for the next action

**VIOLATIONS OF THIS PATTERN WILL REQUIRE TASK RE-EXECUTION**

### Prohibited Actions:
- ❌ Working from memory of previous task state
- ❌ Executing multiple checklist items at once
- ❌ Skipping ahead to later phases
- ❌ Assuming any item is complete without verification
- ❌ Proceeding without reading the file first

## Universal Task Requirements

The following requirements are **MANDATORY** and apply to **ALL** aspects of this task:

1. **EVERY** checklist item is **REQUIRED** - there are NO optional items
2. **ALL** steps MUST be completed in EXACT sequential order per the Five-Step Pattern
3. **ALL** referenced files MUST be reviewed before use
4. **NO** batching of operations - one action per execution cycle
5. **The task file is the ONLY source of truth** - do not trust memory or assumptions

#### MANDATORY REPEATED REMINDER REQUIREMENTS

When creating ANY task, the `orchestrator` MUST include the following repeated reminders throughout the task document:

### 1. **Sequential Completion Reminders**
After EVERY checklist section (every 3-5 checklist items), include this EXACT reminder:

```markdown
**REMINDER:** YOU MUST actually complete the work associated with each checkbox and then mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.
```

### 2. **Workflow Adherence Reminders**
After EVERY major phase section, include this EXACT reminder:

```markdown
**WORKFLOW ADHERENCE REMINDER:** Before proceeding to the next phase, YOU MUST review the corresponding section of [`[workflow_document].md`](path) to ensure you are following ALL requirements exactly as specified in the governing workflow.
```

### 3. **Mandatory Reminder Placement**
The `orchestrator` MUST place these reminders:
- After the completion of each phase
- After every 3-5 checklist items within a phase
- Before any major transition or file creation step
- At the end of any iterative process (like file-by-file analysis)
- Before the final verification section

**CRITICAL:** These reminders are NOT optional - they MUST be included in every task to ensure proper agent execution.

### 4. **Reminder Formatting Requirements**
- All reminders MUST be in bold formatting: `**REMINDER:**`
- All reminders MUST be prominent and easily visible
- All reminders MUST use directive language: "YOU MUST"
- Workflow reminders MUST include the specific workflow document path

### 5. **Example Reminder Pattern for Tasks**
```markdown
**Step 2.1:** Complete first action
- [ ] First checklist item completed
- [ ] Second checklist item completed
- [ ] Third checklist item completed

**REMINDER:** YOU MUST actually complete the work associated with each checkbox and then mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

**Step 2.2:** Complete second action
- [ ] Fourth checklist item completed
- [ ] Fifth checklist item completed

**WORKFLOW ADHERENCE REMINDER:** Before proceeding to the next phase, YOU MUST review the corresponding section of [`[workflow_document].md`](path) to ensure you are following ALL requirements exactly as specified in the governing workflow.

**Phase 3: Next Phase**
[Continue pattern...]
```

### 6. **Failure to Include Reminders**
Tasks created without these repeated reminders will result in:
- Agents forgetting to mark items complete
- Agents skipping ahead or working out of order
- Agents deviating from workflow requirements
- Poor task execution and incomplete deliverables

**CRITICAL:** These reminders are NOT optional - they MUST be included in every task to ensure proper agent execution.

## Universal Task Requirements

The following requirements are **MANDATORY** and apply to **ALL** aspects of this task:

1. **EVERY** checklist item is **REQUIRED** - there are NO optional items. The checklist item must be actually completed.
2. **ALL** steps MUST be completed in EXACT sequential order
3. **ALL** referenced files MUST be reviewed before use
4. **ALL** created files MUST include ALL mandatory elements
5. **NO** assumptions or interpretations are permitted - follow instructions EXACTLY
6. **NO** skipping ahead is permitted - complete each item before moving to the next
7. If ANY uncertainty exists, STOP and request clarification - DO NOT proceed with assumptions
8. **EVERY** checkbox MUST be marked with [x] as you complete it - no exceptions

## TASK FILE MODIFICATION RESTRICTIONS

**MANDATORY:** You MAY NOT modify this task file except to:
1. Check off completed checklist items by changing [ ] to [x]
2. Update frontmatter fields as specified in the Frontmatter Update Protocol
3. Add entries to the Task Log / Notes section
4. **FOR DYNAMIC TASKS ONLY:** Add checklist items within sections marked with "DYNAMIC CONTENT MARKER" comments
   - You MAY add items following the format specified in the marker comment
   - You MUST NOT modify the section structure itself

Any other modifications REQUIRE explicit user permission. If modifications seem necessary, YOU MUST ask the user for approval before making changes.

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

**CRITICAL:** YOU MUST strictly follow ALL requirements and guidelines outlined in the governing workflow document for this task (e.g., the specific stage workflow document like `stage1_api_generation.md`). This includes all phases, steps, quality criteria, and logging requirements.

**⚠️ CHECKLIST STRUCTURE WARNING:**
When creating checklists, NEVER put parent/summary checkboxes before their component items. Components must be completed FIRST, summaries LAST. Use descriptive headers without checkboxes to group related items. Any summary checkbox must appear at the END of its component sequence.

**CRITICAL REQUIREMENTS FOR ALL CHECKLIST ITEMS:**
1. **File Specificity**: Every checklist item MUST include the specific filename and full file path being worked on
2. **Evidence Requirement**: Every checklist item MUST specify evidence via one of:
   - "and log to task notes: [what to log]"
   - "creates file at: [full/path/filename.ext]"
   - "in file [filename.ext] at path: [full/path]"
3. **Verification Steps**: After any file modification, include re-read verification step
4. **Output Locations**: Specify exact paths for all created/modified files

**CHECKLIST ITEM FORMAT PATTERNS (from Section 9B):**

**Pattern A - File Reading:**
```markdown
- [ ] Read file [filename.ext] at [full/path/to/file.ext] and log to task notes in ### [Phase Name] Findings: [specific information to extract], then mark this item complete
```

**Pattern B - File Creation/Modification:**
```markdown
- [ ] [Action verb] file [filename.ext] at path: [full/path] and log to task notes in ### [Phase Name] Findings: [what was done], then mark this item complete
```

**Pattern C - Verification:**
```markdown
- [ ] Re-read file [filename.ext] at [full/path] and log to task notes in ### [Phase Name] Findings: [what you verified], then mark this item complete
```

**Pattern D - Existence Check:**
```markdown
- [ ] Check if file [filename.ext] exists at path: [full/path] and log to task notes in ### [Phase Name] Findings: [status]. If [filename.ext] does not exist, [action to take], then mark this item complete
```

**Pattern E - Content Creation with Source Reference:**
```markdown
- [ ] Read file [source-document.ext] at [path/to/source-document.ext] to extract [specific information needed], then Read file [template.ext] at [path/to/template.ext] section "[Section Name]" to see the exact format, then [Action verb] in file [output-file.ext] at [path/to/output-file.ext] using the format from [template.ext] and content from [source-document.ext], and log to task notes in ### [Phase Name] Findings: [what was created/added], then mark this item complete
```

**CRITICAL:** When creating content for a document, EVERY checklist item must reference:
1. The SOURCE document (where to get the content/information)
2. The TEMPLATE document (where to see the format)
3. The OUTPUT document (where to create/add the content)

**Example - Creating documentation from research:**
```markdown
- [ ] Read file `research-findings.md` at `path/to/research-findings.md` to understand user activation strategies, then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section "## Section 1: [Section Title]" to see the exact format, then Create "## Activation Framework" section in file `user-activation.md` at `Docs_product/product/user-activation.md` using the format from the template and information from `research-findings.md`, and log to task notes in ### Phase 2 Findings: Activation Framework section created with [key points added], then mark this item complete
```
 
### Phase 1: Preparation and Setup
(Refer to [`[workflow_document].md#phase-1-preparation-and-setup`](path/to/workflow#phase-1-preparation-and-setup) for detailed requirements)

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 1.1:** Update task status to "🟠 Doing" in the frontmatter of this file
- [ ] Update status to "🟠 Doing" in frontmatter of this file, then mark this item complete
- [ ] Update start_date to current date in frontmatter of this file, then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

### Required Context Review

**MANDATORY:** YOU MUST thoroughly review **ALL** of the following context files BEFORE beginning any work. These files are REQUIRED for every task to ensure proper execution according to framework standards.

<!-- IMPORTANT: Do NOT include files from .roo/all-general-rules-processes-workflows/ as they are already in agent system prompts and should never be required to be reviewed as context -->

**CRITICAL:** Failure to read ALL context files will result in incomplete or incorrect task execution and task failure during QA validation.

**Step 1.2:** Read Framework Context Files (ALWAYS REQUIRED)

**Core Execution Rules:** `.gfdoc/rules/core/ib_agent_core.md`
- [ ] Read file `ib_agent_core.md` at `.gfdoc/rules/core/ib_agent_core.md` and log to task notes in ### Phase 1 Findings: Five-step execution pattern (READ→IDENTIFY→EXECUTE→UPDATE→REPEAT), prohibited behaviors, mandatory protocols, and task completion rules, then mark this item complete

**Quality Standards:** `.gfdoc/rules/core/quality_gates.md`
- [ ] Read file `quality_gates.md` at `.gfdoc/rules/core/quality_gates.md` and log to task notes in ### Phase 1 Findings: Task completion criteria, quality requirements, evidence requirements, validation standards, and error severity levels, then mark this item complete

**Anti-Hallucination Protocol:** `.gfdoc/rules/core/anti_hallucination_task_completion_rules.md`
- [ ] Read file `anti_hallucination_task_completion_rules.md` at `.gfdoc/rules/core/anti_hallucination_task_completion_rules.md` and log to task notes in ### Phase 1 Findings: Zero-tolerance accuracy policy, evidence format requirements, verification workflow, and penalties for forgery, then mark this item complete

**Anti-Sycophancy Protocol:** `.gfdoc/rules/core/anti_sycophancy.md`
- [ ] Read file `anti_sycophancy.md` at `.gfdoc/rules/core/anti_sycophancy.md` and log to task notes in ### Phase 1 Findings: Professional objectivity requirements, opinion validation standards, and disagreement protocols, then mark this item complete

**File Conventions:** `.gfdoc/rules/core/file_conventions.md`
- [ ] Read file `file_conventions.md` at `.gfdoc/rules/core/file_conventions.md` and log to task notes in ### Phase 1 Findings: Naming conventions, YAML frontmatter requirements, directory structures, and file organization standards, then mark this item complete

**REMINDER:** YOU MUST actually complete the work associated with each checkbox and then mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

**Step 1.3:** Read Task-Specific Context Files

**MANDATORY:** The orchestrator creating this task MUST specify at least ONE task-specific context file below. These provide domain knowledge, technical specifications, or workflow requirements specific to this task.

**[PLACEHOLDER: Workflow/Process Document]:** `[path/to/workflow_document.md]`
- [ ] Read file `[workflow_document.md]` at `[path/to/workflow_document.md]` and log to task notes in ### Phase 1 Findings: [Specific phases, steps, and requirements from workflow], [Critical quality criteria], and [Any mandatory deliverables specified], then mark this item complete

**[PLACEHOLDER: Domain/Technical Documentation]:** `[path/to/technical_doc.md]`
- [ ] Read file `[technical_doc.md]` at `[path/to/technical_doc.md]` and log to task notes in ### Phase 1 Findings: [Key technical concepts needed], [Domain-specific requirements], and [Integration requirements or constraints], then mark this item complete

**[PLACEHOLDER: Template/Example]:** `[path/to/template.md]`
- [ ] Read file `[template.md]` at `[path/to/template.md]` and log to task notes in ### Phase 1 Findings: [Template structure and required sections], [Frontmatter requirements], and [Content formatting requirements], then mark this item complete

<!-- ORCHESTRATOR: Add additional task-specific context files as needed following the same pattern -->

**REMINDER:** YOU MUST actually complete the work associated with each checkbox and then mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

**Step 1.4:** Read Previous Stage Outputs (IF APPLICABLE)

**MANDATORY:** If this task depends on outputs from previous stages (as specified in "Prerequisites & Dependencies" > "Previous Stage Outputs" section above), YOU MUST read all required previous stage outputs BEFORE proceeding with Phase 2 execution.

**ORCHESTRATOR:** If this task has NO previous stage dependencies, DELETE this entire Step 1.4 section. If this task DOES have previous stage dependencies, ADD a checklist item for EACH output file listed in the "Previous Stage Outputs" section, following the pattern below:

**[Output Type 1]:** `[path/to/output1.md]`
- [ ] Read file `[output1.md]` at `[path/to/output1.md]` and log to task notes in ### Phase 1 Findings: [Specific content or data to utilize from this file - e.g., key findings, requirements extracted, data points needed], then mark this item complete

**[Output Type 2]:** `[path/to/output2.md]`
- [ ] Read file `[output2.md]` at `[path/to/output2.md]` and log to task notes in ### Phase 1 Findings: [Specific content or data to utilize from this file - e.g., verified outputs, analysis results, configuration values], then mark this item complete

**[Output Type 3]:** `[path/to/output3.md]`
- [ ] Read file `[output3.md]` at `[path/to/output3.md]` and log to task notes in ### Phase 1 Findings: [Specific content or data to utilize from this file - e.g., integration requirements, technical specifications], then mark this item complete

<!-- ORCHESTRATOR: Add checklist item for EACH previous stage output listed in Prerequisites section -->

**REMINDER:** YOU MUST actually complete the work associated with each checkbox and then mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

**Step 1.5:** Review Tool Orchestration Strategy for This Task

**MANDATORY:** YOU MUST review and understand the tool selection and execution strategy for this task BEFORE beginning Phase 2 work.

## 🛠️ Tool Orchestration Guidance for This Task

### Tool Selection Matrix:
| Operation Type | Primary Tool | Alternative | Execution Mode |
|----------------|--------------|-------------|----------------|
| File Discovery | Glob | Bash (ls/find) | Parallel OK |
| Content Search | Grep | Read + manual | Parallel OK |
| File Reading | Read | Bash (cat) | Parallel OK |
| File Creation | Write | Bash (echo >) | Sequential |
| File Modification | Edit | Write (replace) | Sequential |
| Command Execution | Bash | - | Parallel if independent |
| Verification | Read | Bash (cat/ls) | Parallel OK |

### Execution Strategy for This Task:
**Phase 2 - Discovery (if applicable):**
- Use Glob to find files matching patterns
- Use Grep to search specific content
- Batch Read operations for efficiency

**Phase 2+ - Implementation:**
- Execute changes in dependency order (sequential where needed)
- Use Write for new files, Edit for modifications
- Validate after each major change

**Final Phases - Validation:**
- Batch Read operations to verify changes
- Run independent tests in parallel where possible
- Collect and analyze results

### Performance Optimization Hints:
- **Batch Operations:** Group similar tool calls (e.g., Read 5 files in one message)
- **Parallel Execution:** Run independent operations simultaneously
- **Sequential Where Required:** File Write → Read same file must be sequential
- **Fail Fast:** Stop immediately on critical errors

**For detailed tool selection guidance, see:** `.gfdoc/rules/core/tool_selection.md` (read as part of Step 1.2 above)

**Confirm Understanding:**
- [ ] Review tool orchestration guidance above and log to task notes in ### Phase 1 Findings: Tool selection strategy understood - [briefly note key tools you'll use: e.g., "Will use Glob for file discovery, Read in parallel for context files, Write/Edit sequentially for modifications, Bash for verification"], then mark this item complete

**REMINDER:** YOU MUST actually complete the work associated with each checkbox and then mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

**ALL** context files, previous stage outputs, and execution strategies are **MANDATORY**. Every file listed above MUST be read and understood, and the tool orchestration strategy MUST be reviewed before proceeding with task execution.

### Phase 2: [Main Execution Phase Name]
(Refer to [`[workflow_document].md#phase-2-main-execution-phase-name`](path/to/workflow#phase-2-main-execution-phase-name) for detailed requirements)

**CRITICAL:** DO NOT assume, hallucinate, or make up any information. These [items] are of the highest importance and MUST be 100% TRUE based on the [source] information.
**HIGHEST CRITICAL:** ALL output created below align with, conform to, and fulfill the requires in `[governing_workflow].md`

**MANDATORY INPUTS from Previous Phase:**
[Doc-commander must specify exact inputs from previous phases, e.g., analysis reports, verified outputs, etc.]
- **[Input Type 1]:** `[path/to/output1.md]`
- [ ] Read file `[output1.md]` at `[path/to/output1.md]` and log to task notes in ### Phase 2 Findings: [Specific content or data to utilize from this file], then mark this item complete
- **[Input Type 2]:** `[path/to/output2.md]`
- [ ] Read file `[output2.md]` at `[path/to/output2.md]` and log to task notes in ### Phase 2 Findings: [Specific content or data to utilize from this file], then mark this item complete

Continue working through this checklist systematically. As you create or modify files, YOU MUST add content incrementally - DO NOT attempt to complete entire files at once. YOU MUST perform [describe the main work]. ALL [items] in the [location] [criteria]. NO [item] IN THE [location] MAY BE IGNORED.

**Step 2.1:** [Specific action - e.g., "Create initial file structure"]. **HIGHEST CRITICAL:** ALL output created below align with, conform to, and fulfill the requires in `[governing_workflow].md`

Create file at: `[exact/path/to/file.md]`
- [ ] Create directory `[directory/path]` if it doesn't exist and log to task notes in ### Phase 2 Findings: Directory creation status, then mark this item complete
- [ ] Create file `[file.md]` at `[exact/path/to/file.md]` with proper extension and log to task notes in ### Phase 2 Findings: File created, then mark this item complete
- [ ] Read file `[template.md]` at `[path/to/template.md]` section "Frontmatter" (approximately lines X-Y) to see required frontmatter format, then Read file `[source-content.md]` at `[path/to/source-content.md]` to extract metadata (title, description, tags, etc.), then Add ALL mandatory frontmatter fields to file `[file.md]` at `[exact/path/to/file.md]` using the format from `[template.md]` and metadata from `[source-content.md]` per `file_conventions.md` and log to task notes in ### Phase 2 Findings: Frontmatter fields added [list them], then mark this item complete
- [ ] Read file `[template.md]` at `[path/to/template.md]` section "Content Structure" to see required sections, then Read file `[source-content.md]` at `[path/to/source-content.md]` to understand content organization needs, then Add initial content structure with required sections to file `[file.md]` at `[exact/path/to/file.md]` using structure from `[template.md]`, and log to task notes in ### Phase 2 Findings: Sections added [list them], then mark this item complete
- [ ] Re-read file `[file.md]` at `[exact/path/to/file.md]` and log to task notes in ### Phase 2 Findings: Verified all requirements from `[governing_workflow].md` are met, NO hallucinated information added, then mark this item complete
- [ ] Re-read file `[file.md]` at `[exact/path/to/file.md]` and log to task notes in ### Phase 2 Findings: Content is accurate to source materials, all required sections present and complete, cross-references functional, no TODO/FIXME markers, then mark this item complete

**REMINDER:** YOU MUST mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

**Step 2.2:** [Next specific action]. **HIGHEST CRITICAL:** ALL output created below align with, conform to, and fulfill the requires in `[governing_workflow].md`

- [ ] Confirm that YOU MUST [exact requirement], reference: [source material] for [what to extract/implement], add content section by section, saving after each major addition. DO NOT assume, hallucinate, or make up any information. These files are of the highest importance and MUST be true based on the [source] information.
- [ ] Read file `[source.md]` at `[path/to/source.md]` and log to task notes in ### Phase 2 Findings: [What to extract/implement from source material], then mark this item complete
- [ ] If [condition], then [required action per workflow]
- [ ] Read file `[template.md]` at `[path/to/template.md]` section "[Section Name]" to see exact format for [specific content section], then Read file `[source.md]` at `[path/to/source.md]` to extract [specific information needed for this section], then Add [specific content section] to file `[file.md]` at `[exact/path/to/file.md]` using format from `[template.md]` and content from `[source.md]`, section by section, and log to task notes in ### Phase 2 Findings: [Section name] added with [key content points], then mark this item complete
- [ ] Read file `[source.md]` at `[path/to/source.md]` to extract [specific data or information], then Do [specific action] with/in `[file.md]` at `[exact/path/to/file.md]` using information from `[source.md]`, and log to task notes in ### Phase 2 Findings: [What action was completed], then mark this item complete
- [ ] Re-read file `[file.md]` at `[exact/path/to/file.md]` and log to task notes in ### Phase 2 Findings: Verified all requirements from `[governing_workflow].md` fulfilled for [specific output], NO hallucinated information, then mark this item complete

**REMINDER:** YOU MUST mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

**Step 2.3:** [Continue with detailed steps]. **HIGHEST CRITICAL:** ALL output created below align with, conform to, and fulfill the requires in `[governing_workflow].md`

- [ ] Confirm that you DO NOT [common mistake to avoid], and that YOU MUST ensure [critical requirement]. DO NOT assume, hallucinate, or make up any information. These files are of the highest importance and MUST be true based on the [source] information.
- [ ] If [condition], then [required action per workflow]
- [ ] Read file `[source.md]` at `[path/to/source.md]` to verify [specific information to check], then [Perform specific verification action] on file `[file.md]` at `[exact/path/to/file.md]` comparing against `[source.md]` and log to task notes in ### Phase 2 Findings: [Specific verification completed and what was verified], then mark this item complete
- [ ] Read file `[reference.md]` at `[path/to/reference.md]` to check [requirements or standards], then [Perform another verification action] on file `[file.md]` at `[exact/path/to/file.md]` ensuring compliance with `[reference.md]` and log to task notes in ### Phase 2 Findings: [Another verification completed and compliance status], then mark this item complete
- [ ] Re-read file `[file.md]` at `[exact/path/to/file.md]` and log to task notes in ### Phase 2 Findings: Content accurate to source materials, all sections complete, cross-references functional, no TODO/FIXME markers, then mark this item complete

**REMINDER:** YOU MUST mark each checkbox  with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

<!-- EXAMPLE: File-Specific Processing Pattern (use for tasks that process multiple specific files) -->
### Example: File-by-File Processing Pattern

**Use this pattern when processing multiple known files (not for dynamic discovery):**

#### File: [filename1.ext] at [full/path/to/filename1.ext]
- [ ] Check if file [filename1.ext] exists at path: [full/path]. If file exists log to task notes in ### Phase [N] Findings: File existence status (exists/needs creation), [other status checks], [Specific information to extract from this file]. If [filename1.ext] does not exist, create it, then mark this item complete
- [ ] Read file `[template.md]` at `[path/to/template.md]` section "[Section Name]" to see format for [what you're adding], then Read file `[source-data.md]` at `[path/to/source-data.md]` to extract [specific content for filename1], then [Action verb] file [filename1.ext] at path: [full/path] using format from `[template.md]` and content from `[source-data.md]` and log to task notes in ### Phase [N] Findings: [What was done - be specific with content added], then mark this item complete
- [ ] Re-read file [filename1.ext] at [full/path] and log to task notes in ### Phase [N] Findings: [Verification checklist - confirm specific changes made match template format and source content], then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

#### File: [filename2.ext] at [full/path/to/filename2.ext]
- [ ] Check if file [filename2.ext] exists at path: [full/path]. If file exists log to task notes in ### Phase [N] Findings: File existence status (exists/needs creation), [other status checks], [Specific information to extract from this file]. If [filename2.ext] does not exist, create it, then mark this item complete
- [ ] Read file `[template.md]` at `[path/to/template.md]` section "[Section Name]" to see format for [what you're adding], then Read file `[source-data.md]` at `[path/to/source-data.md]` to extract [specific content for filename2], then [Action verb] file [filename2.ext] at path: [full/path] using format from `[template.md]` and content from `[source-data.md]` and log to task notes in ### Phase [N] Findings: [What was done - be specific with content added], then mark this item complete
- [ ] Re-read file [filename2.ext] at [full/path] and log to task notes in ### Phase [N] Findings: [Verification checklist - confirm specific changes made match template format and source content], then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

[Repeat for each file to process]

**Benefits of this pattern:**
- Clear file-by-file organization with headers showing exactly which file is being worked on
- Each file gets complete processing (check → read → modify → verify) before moving to next
- File name and full path repeated in every checklist item for absolute clarity
- QA can verify each file was processed by checking task log entries against actual file contents

<!-- FOR TASKS WITH MULTIPLE SIMILAR ITEMS: The orchestrator agent creating this task MUST enumerate all items -->
### Multi-Item Processing Pattern (For tasks with multiple similar items)

**CRITICAL:** The orchestrator agent creating this task file MUST identify and enumerate ALL items that need processing during task setup. The worker agent MUST NEVER dynamically add checklist items - all items must be listed by the orchestrator before the worker begins.

**Instructions for Orchestrator (creating task):**
1.  **Identify Items:** Use appropriate tools (e.g., `list_files`, `search_files`) to identify all individual items that need processing in this phase.
2.  **Add Checklist Items:** For EACH identified item, YOU MUST add a new checklist item below, following the specified format.
3.  **Process Iteratively:** YOU MUST process each item one by one, marking its checkbox with [x] ONLY after its processing is fully complete and its output (e.g., update to a log file) is verified.
4.  **Incremental Updates:** As you process each item, YOU MUST update the relevant output file (e.g., raw analysis log) incrementally. DO NOT wait until all items are processed to update the output file.

**Pattern for each item (orchestrator creates these):**

#### File: [filename1.ext] at [full/path/to/filename1.ext]
- [ ] Check if file [filename1.ext] exists at path: [full/path]. If file exists log to task notes in ### Phase [N] Findings: File existence status (exists/needs creation), [other status checks], [Specific information to extract from this file]. If [filename1.ext] does not exist, create it, then mark this item complete
- [ ] Read file `[template.md]` at `[path/to/template.md]` section "[Section Name]" to see format, then Read file `[source-data.md]` at `[path/to/source-data.md]` to extract [specific content for filename1], then [Action verb] file [filename1.ext] at path: [full/path] using format from `[template.md]` and content from `[source-data.md]` and log to task notes in ### Phase [N] Findings: [What was done - be specific with content added], then mark this item complete
- [ ] Re-read file [filename1.ext] at [full/path] and log to task notes in ### Phase [N] Findings: [Verification checklist - confirm specific changes made match template and source], then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

#### File: [filename2.ext] at [full/path/to/filename2.ext]
- [ ] Check if file [filename2.ext] exists at path: [full/path]. If file exists log to task notes in ### Phase [N] Findings: File existence status, [other checks], [info to extract]. If [filename2.ext] does not exist, create it, then mark this item complete
- [ ] Read file `[template.md]` at `[path/to/template.md]` section "[Section Name]" to see format, then Read file `[source-data.md]` at `[path/to/source-data.md]` to extract [specific content for filename2], then [Action verb] file [filename2.ext] at path: [full/path] using format from `[template.md]` and content from `[source-data.md]` and log to task notes in ### Phase [N] Findings: [What was done with content added], then mark this item complete
- [ ] Re-read file [filename2.ext] at [full/path] and log to task notes in ### Phase [N] Findings: [Verification checklist - confirm changes match template and source], then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item.

<!-- Orchestrator continues this pattern for ALL items identified -->

**Final Phase Verification:** For EVERY file created or modified in this phase:
- [ ] Re-read file [filename.ext] at [full/path] and log to task notes in ### Phase [N] Findings: Confirmed ALL mandatory frontmatter fields included, ALL required content sections present, content accurate to source materials, cross-references and links functional, NO "TODO" or "FIXME" markers remain, then mark this item complete

**WORKFLOW ADHERENCE REMINDER:** Before proceeding to the next phase, YOU MUST review the corresponding section of [`[workflow_document].md`](path/to/workflow) to ensure you are following ALL requirements exactly as specified in the governing workflow.

### Phase 3: [Additional Phase if Needed]
(Refer to [`[workflow_document].md#phase-3-additional-phase-if-needed`](path/to/workflow#phase-3-additional-phase-if-needed) for detailed requirements)

**HIGHEST CRITICAL:** ALL output created below align with, conform to, and fulfill the requires in `[governing_workflow].md`

**MANDATORY INPUTS from Previous Phase:**
[Doc-commander must specify exact inputs from previous phases, e.g., analysis reports, verified outputs, etc.]
- **[Input Type 1]:** `[path/to/output1.md]`
- [ ] Read file `[output1.md]` at `[path/to/output1.md]` and log to task notes in ### Phase 2 Findings: [Specific content or data to utilize from this file], then mark this item complete
- **[Input Type 2]:** `[path/to/output2.md]`
- [ ] Read file `[output2.md]` at `[path/to/output2.md]` and log to task notes in ### Phase 2 Findings: [Specific content or data to utilize from this file], then mark this item complete

Continue working through this checklist systematically. As you create or modify files, YOU MUST add content incrementally - DO NOT attempt to complete entire files at once. YOU MUST perform [describe the main work]. ALL [items] in the [location] [criteria]. NO [item] IN THE [location] MAY BE IGNORED.

[Continue with the same level of detail and explicit requirements]

**Step 3.1:** [Specific action]

[Detailed instructions]

- [ ] [Action verb] file [filename.ext] at [full/path] and log to task notes in ### Phase 3 Findings: [What was done], then mark this item complete
- [ ] Re-read file [filename.ext] at [full/path] and log to task notes in ### Phase 3 Findings: Confirmed content is accurate to source materials, all required sections present and complete, cross-references and links functional, NO "TODO" or "FIXME" markers remain, then mark this item complete

**REMINDER:** YOU MUST mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

**WORKFLOW ADHERENCE REMINDER:** Before proceeding to the next phase, YOU MUST review the corresponding section of [`[workflow_document].md`](path/to/workflow) to ensure you are following ALL requirements exactly as specified in the governing workflow.

### Phase 4: Logging and Reporting
(Refer to [`[workflow_document].md#phase-4-logging-and-reporting`](path/to/workflow#phase-4-logging-and-reporting) for detailed requirements)

**MANDATORY INPUTS from Previous Phase:**
[Doc-commander must specify exact inputs from previous phases, e.g., analysis reports, verified outputs, etc.]
- **[Input Type 1]:** `[path/to/output1.md]`
- [ ] Read file `[output1.md]` at `[path/to/output1.md]` and log to task notes in ### Phase 2 Findings: [Specific content or data to utilize from this file], then mark this item complete
- **[Input Type 2]:** `[path/to/output2.md]`
- [ ] Read file `[output2.md]` at `[path/to/output2.md]` and log to task notes in ### Phase 2 Findings: [Specific content or data to utilize from this file], then mark this item complete

Per [governing workflow document], YOU MUST log the following:

**Step 4.1:** In this task's "Task Log / Notes" section below, add entry with:
- [ ] Add entry to task notes in ### Phase 4 Findings with: Timestamp of completion, summary of all files created/modified with paths, any deviations from expected process, and required logging per [workflow section X.X], then mark this item complete

**Step 4.2:** If follow-up actions identified, log using required prefix:
- [ ] If follow-up actions identified, log to task notes in ### Follow-Up Items Identified using required prefix from [workflow document] for [type of follow-up] and include all context needed for follow-up task creation, then mark this item complete

**REMINDER:** YOU MUST mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

**WORKFLOW ADHERENCE REMINDER:** Before proceeding to the next phase, YOU MUST review the corresponding section of [`[workflow_document].md`](path/to/workflow) to ensure you are following ALL requirements exactly as specified in the governing workflow.

### Phase 5: [Insights and Gap Identification Phase Name]

Capture broader insights and identify gaps.

**Step 5.1:** Log all discovered [insight type] to `[insights_file]` in accordance with `[insights_process].md`
- [ ] Confirm that YOU MUST use the standardized four-field format: `Insight`, `Source/Context`, `Implication/Suggestion`, `Logged by`, and YOU MUST categorize insights appropriately [category examples], then Log all [Insight type] in the ### Phase 5 - [Phase Name] Findings log, and then mark this item complete.
- [ ] Re-read and ensure that all requirements in `[governing_workflow].md` and `[insights_process].md` have been completely fulfilled for the [insight type]. If they have, note such in the ### Phase 5 - [Phase Name] Findings log. If they have not, make the appropriate changes and then note such in the ### Phase 5 - [Phase Name] Findings log, and then mark this item complete.

**Step 5.2:** Propose new [terminology] in `[insights_file]` in accordance with `[terminology_process].md`
- [ ] Confirm that YOU MUST use the standardized format: `Proposed Term`, `Proposed Definition`, `Context/Source File(s)`, `Proposed by`, `Rationale`, then Log all [Terminology] proposed in the ### Phase 5 - [Phase Name] Findings log, and then mark this item complete.
- [ ] Re-read and ensure that all requirements in `[governing_workflow].md` and `[terminology_process].md` have been completely fulfilled for the [terminology]. If they have, note such in the ### Phase 5 - [Phase Name] Findings log. If they have not, make the appropriate changes and then note such in the ### Phase 5 - [Phase Name] Findings log, and then mark this item complete.

**Step 5.3:** Document any critical asset blockers.
- [ ] Confirm that YOU MUST include: Type, Asset/File, Required Information, Impact, Workaround, Priority, and then list any Critical asset blockers documented (if any) in the ### Phase 5 - [Phase Name] Findings log, and then mark this item complete.

**REMINDER:** YOU MUST mark each checkbox with [x] as you complete it before proceeding to the next item.

## Outputs & Deliverables

### Required Outputs

The following outputs MUST be produced by this task:

1. **[Output Type 1 - e.g., "Analysis Output Files"]**
   - Location: `[exact/path/to/outputs/]`
   - File naming: Must follow pattern `[naming-convention]`
   - Required format: [Markdown with full frontmatter per template X]
   - Must include: [specific content requirements]

2. **[Output Type 2 - e.g., "Analysis Report"]**
   - Location: `[exact/path/to/report.md]`
   - Must use template: `[template-name.md]`
   - Required sections: [list all mandatory sections]

3. **[Output Type 3 - e.g., "Updated System Files"]**
   - Files to update: [list specific files]
   - Update requirements: [what must be added/modified]
   - Must maintain: [what cannot be changed]

4. **Task Log with [Specific Type] Records**
   - Location: This task file's "Task Log / Notes" section
   - Must include: [list what must be logged in task notes]

**CRITICAL:** Every output must be verifiable by QA through:
- File existence at specified exact path
- File contents matching required format and elements
- Task log entries providing evidence of completion

### Success Criteria

This task is considered complete when:
- ALL checklist items are marked complete
- ALL required outputs exist at specified locations
- ALL files contain required content and structure
- Task log includes all required information
- Verification steps below have been completed

**REMINDER:** YOU MUST mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Verification Checklist

**MANDATORY:** Before marking this task as "🟢 Done", YOU MUST verify **ALL** of the following:

**Output Verification:**
- [ ] Verify that all files have been created at exact paths specified, All files contain ALL mandatory frontmatter fields, All files follow required templates, and No placeholder content remains (unless explicitly allowed or as instructed). Log your findings in the ### Execution Log, and then mark this as done.

**Process Compliance:**
- [ ] Verify that All workflow requirements from [parent workflow] have been satisfied, All logging completed per requirements, and Any identified follow-ups properly logged with correct prefixes. Log your findings in the ### Execution Log, and then mark this as done.

**REMINDER:** YOU MUST mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Error Handling

If errors occur during task execution:

### File Access Issues
- If unable to access required files: Mark task as "⚪ Blocked" and set `blocker_reason` in frontmatter
- Log specific files that cannot be accessed in Task Log

### Process Uncertainties
- If workflow requirements are unclear: Add note in Task Log with prefix per [workflow document]
- DO NOT make assumptions - escalation required per [process document section X]

### Quality Gate Failures
- If outputs fail quality gates: DO NOT mark task complete
- Document specific failures in Task Log
- Follow correction procedure from [workflow document]

## Post-Completion Actions

After all verification complete:

- [ ] Ensure that the ## Task Log / Notes 📋 contains complete execution summary. If it does not, create it, and then mark this as done.
- [ ] Update `completion_date`, and `updated_date` to today's date, and update task status to "🟢 Done" in frontmatter, and then mark this as done.

**REMINDER:** YOU MUST mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Task Completion and Handoff Protocol

**CRITICAL:** Task completion follows the automated QA workflow process described in `ib_agent_core.md`.

**For QA Workflow Integration:**
- When using the automated QA workflow script (`/rf:task`), the Worker-QA cycle handles task completion automatically
- The Worker completes checklist items sequentially, marking each as done
- When all items in the current batch are complete, QA review is automatically triggered
- The QA agent verifies completion against actual outputs and quality standards
- If QA passes, the task moves to the next batch or completes
- If QA fails, specific items are unmarked for Worker correction

**CRITICAL COMPLETION REQUIREMENTS:**
- All checklist items MUST be actually completed, not just marked
- All outputs MUST pass quality gates defined in `quality_gates.md`
- Task Log MUST contain complete execution summary
- Follow-up items MUST be logged with appropriate prefixes

**REMINDER:** YOU MUST mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Task Log / Notes 📋

### Execution Log
<!-- Agent adds timestamped entries here during task execution -->

### Phase 1 - [Phase Name] Findings
<!-- Agent logs findings here as required by "log to task notes" checklist items -->

### Phase 2 - [Phase Name] Findings
<!-- Agent logs findings here as required by "log to task notes" checklist items -->

### Phase 3 - [Phase Name] Findings
<!-- Agent logs findings here as required by "log to task notes" checklist items -->

### Follow-Up Items Identified
<!-- List any items flagged for follow-up with required prefixes -->

### Deviations from Process
<!-- Document any necessary deviations and rationale -->