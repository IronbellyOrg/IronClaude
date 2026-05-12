---
name: task
description: "Execute an MDTM task file — process checklist items sequentially with the F1 execution loop, spawn subagents when items require them, use parallel spawning for independent items, and track progress via frontmatter and task log. Use this skill when the user wants to execute a task file, run a task, process a checklist, resume an in-progress task, or work through an MDTM task file. Trigger on phrases like 'execute this task file', 'run this task', 'process this task', 'resume the task', 'pick up where we left off', 'continue the task', or when the user provides a path to a .md file in .dev/tasks/ and wants it executed. Also trigger when the user says '/task' followed by a file path or task identifier."
---

# Task File Executor

A skill for executing MDTM task files with the same rigor and discipline used in all Rigorflow skills. This skill is the generic execution engine — it takes any well-formed MDTM task file and processes its checklist items using the F1 execution loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT).

**How it works:** The skill reads the task file, finds the first unchecked `- [ ]` item, executes it exactly as written, marks it `- [x]`, and repeats. If the item says to spawn a subagent, it spawns one. If it says to read files and produce output, it does that directly. If consecutive items are independent subagent spawns, it spawns them in parallel. Progress is tracked on disk — if context compresses or the session restarts, the skill re-reads the task file and resumes from the first unchecked item.

**What this skill does NOT do:** It does not create task files (use `rf:task-builder` for that), does not define what work to do (the task file defines that), and does not prescribe which agents to use (the task file's B2 self-contained items embed all context, actions, and agent prompts). This skill is the disciplined loop that ensures every item gets executed completely, in order, with evidence of completion.

## Why This Process Works

Task file execution fails when it relies on memory, skips steps, or accumulates work without writing to disk. This skill forces every action through a verified loop — read the file, find the next item, do exactly what it says, write the result, mark it done, repeat.

The F1 execution loop provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off. Completed items' output files already exist on disk.

The parallel spawning rules prevent two common failure modes:
- **Unnecessary serialization** — When consecutive items are independent (e.g., multiple research agents, analyst + QA pairs), spawning them sequentially wastes time. Parallel spawning achieves depth and speed simultaneously.
- **Context rot** — By isolating each subagent in its own context with its own output file, no single agent needs to hold excessive content. Findings are written to disk incrementally, not accumulated in memory.

---

## Input

The skill needs one piece of information:

**Task file path** (mandatory): The path to an MDTM task file to execute. This is typically in `.dev/tasks/to-do/` but can be anywhere.

Under the centralized path convention, each task file lives inside its own folder: `.dev/tasks/to-do/TASK-[ID]/TASK-[ID].md`. All intermediate artifacts (research, synthesis, QA reports) go into typed subfolders within that folder. The task folder is the self-contained workspace for the entire execution.

Examples of strong input:
- `execute .dev/tasks/to-do/TASK-SKILL-TRANSFORM-20260308-tech-reference/TASK-SKILL-TRANSFORM-20260308-tech-reference.md`
- `resume the tech-reference transformation task`
- `/task .dev/tasks/to-do/TASK-SKILL-TRANSFORM-20260308-tech-reference/TASK-SKILL-TRANSFORM-20260308-tech-reference.md`

Examples of weak input (skill will search for the task file):
- `continue the task` — Skill will search `.dev/tasks/to-do/` for in-progress task folders (status: "🟠 Doing")
- `run the task` — Ambiguous if multiple task files exist; skill will list candidates and ask

**What to Do If No Path Is Provided:**
1. Search `.dev/tasks/to-do/` for `TASK-*/` folders, read the task file inside each folder to check for status "🟠 Doing"
2. If exactly one found, resume it
3. If multiple found, list them and ask the user which one to execute
4. If none found, search for status "🟡 To Do" and list candidates
5. If still none, inform the user no task files were found

---

## Task File Discovery

### Finding Task Files

On invocation, determine which task file to execute:

1. **Explicit path provided** — Use that path directly. Verify it exists.
2. **Identifier provided** (e.g., "tech-reference transformation") — Search `.dev/tasks/to-do/` for `TASK-*/` folders matching the identifier, then read the task file inside the matching folder.
3. **No path provided** — Follow the "What to Do If No Path Is Provided" protocol above.

### Validating the Task File

Before executing, verify the task file is well-formed. The task file should be located at `TASK_DIR/TASK_ID.md` inside its own folder (e.g., `.dev/tasks/to-do/TASK-FOO-20260310/TASK-FOO-20260310.md`).
- Has YAML frontmatter with at least: `id`, `title`, `status`, `created_date`
- Has checklist items (`- [ ]` or `- [x]`)
- Items appear to follow B2 self-contained pattern (single paragraphs, not terse bullets)
- Has a `## Task Log / Notes` section at the bottom

If the file is malformed, inform the user of specific issues rather than attempting to execute it.

---

## Execution

### The F1 Execution Loop

Execute the task file using the five-step execution pattern:

```
READ → IDENTIFY → EXECUTE → UPDATE → REPEAT
```

1. **READ**: Read the task file from disk. ALWAYS — never work from memory of previous state. This is the most important rule.
2. **IDENTIFY**: Find the FIRST unchecked `- [ ]` item. Scan from top to bottom. The first unchecked item is the next action.
3. **EXECUTE**: Complete ONLY that single identified item by doing exactly what it says:
   - If the item says to spawn a subagent → use the Agent tool with the prompt embedded in the item
   - If the item says to read files and produce output → do it directly
   - If the item says to edit a file → edit it
   - If the item says to run a command → run it via Bash
   - If the item says to present to the user → output the required information
   - If the item says to update frontmatter → edit the task file's frontmatter
   - If the item includes an "ensuring..." clause → verify those conditions before marking complete
4. **UPDATE**: Mark ONLY that item as `- [x]` in the task file on disk. Also log completion to the appropriate Phase Findings section if the item produced a notable output or encountered issues.
5. **REPEAT**: Return to step 1. Do NOT proceed from memory — re-read the file.

### First Item Protocol

The very first action when starting a new task (status: "🟡 To Do") should be to look for the status update item (typically Step 1.1). If the first item is a status update, execute it — this changes status to "🟠 Doing" and sets `start_date`. If the task file doesn't have a status update item, update the frontmatter yourself before proceeding to the first checklist item.

### Prohibited Actions (F2)

These actions are NEVER permitted during task file execution:

- **Working from memory** — You MUST re-read the task file before each action. Never assume you know the current state. The task file on disk is the ONLY source of truth.
- **Executing multiple items simultaneously** — One item at a time, marked complete before moving to the next. Exception: parallel agent spawning (see below).
- **Skipping items** — Items MUST be completed in exact sequential order. No reordering, no "I'll come back to this."
- **Assuming completion** — An item is only complete when you have evidence of completion (file written, output produced, command succeeded) AND have marked it `- [x]` on disk.
- **Inventing file paths** — Only reference files you have verified exist via Glob/Read. If an item references a file that doesn't exist, log the blocker rather than guessing.
- **Modifying items** — Do not rewrite, rephrase, or reinterpret checklist items. Execute them as written. If an item is ambiguous or incorrect, log the issue in Task Log / Notes and ask the user.
- **Adding items** — Do not add new checklist items unless the task file contains DYNAMIC CONTENT MARKER sections that explicitly permit it.
- **Delegating across phase boundaries** — You MUST NOT spawn a subagent and instruct it to execute items spanning multiple phases. Each phase is a separate execution unit with a mandatory QA gate between phases. A subagent may only receive work from a SINGLE checklist item (or a parallel batch of independent items within the same phase). Delegating the F1 loop itself to a subagent is prohibited — the executor must maintain the READ-IDENTIFY-EXECUTE-UPDATE-REPEAT loop and spawn subagents only for individual item execution.
- **Skipping phase-gate QA** — After completing all items in a phase (Phase 2+), you MUST spawn rf-qa before executing any item in the next phase. This is not optional. See Phase-Gate QA Verification for the full protocol. Proceeding to the next phase without a passing QA gate is a prohibited action equivalent to skipping items.
- **Skipping post-completion validation** — After the final phase's phase-gate QA passes, you MUST run both rf-qa structural validation and rf-qa-qualitative operational validation BEFORE marking the task "Done." See Post-Completion Validation for the full protocol. Marking a task done without running both validations is a prohibited action.

### Parallel Agent Spawning

When multiple consecutive items each spawn independent subagents within the same phase, you MUST spawn them in parallel using multiple Agent tool calls in a single response. This is not optional — it is how Rigorflow achieves depth and minimizes wall-clock time.

**Identifying a parallel batch:**
1. Read the task file and find the first unchecked `- [ ]` item
2. Starting from that item, read forward through all consecutive unchecked items that are independent subagent spawns within the same phase step
3. Items are "independent" if they don't depend on each other's output (they read from the same source but write to different files)
4. All of these form a single parallel batch

**Executing a parallel batch:**
1. Spawn ALL agents in the batch using parallel Agent tool calls in a single message
2. As each agent returns, mark its corresponding item `- [x]` immediately — do not wait for all to finish before checking any off. This ensures progress is captured even if the session ends mid-batch
3. After ALL agents in the batch return, re-read the task file before proceeding to the next item or phase

**Identifying non-parallel items:**
- Items that read a previous item's output are NOT parallel — they must run sequentially. Example: if item 3 reads a file created by item 2, they CANNOT be parallelized even if both spawn agents.
- Items within different phases are NOT parallel — complete one phase before starting the next
- Items that edit the same file are NOT parallel — they must run sequentially
- When in doubt, run sequentially — correctness over speed

**Partitioning for large batches:** When a parallel batch includes agents that each read from many files (e.g., an analyst reviewing 10 research files), partition the work to prevent context rot. Spawn multiple instances of the same agent type, each with an `assigned_files` subset. Partitioning thresholds: >6 files for analysis/completeness phases, >4 files for synthesis/review phases. Each partitioned instance writes to its own numbered report file; the orchestrator merges findings after all return. This follows the same partitioning pattern used by rf-analyst and rf-qa in the tech-research skill.

**On resumption after a mid-batch failure:** If some items in a batch are `- [x]` and others are `- [ ]`, spawn only the unchecked ones. The checked agents' output files already exist on disk — do not re-run them.

### Task File Modification Restrictions (F4)

During execution, you MAY ONLY modify the task file to:
- Check off completed items (`- [ ]` → `- [x]`)
- Update frontmatter fields (status, updated_date, start_date, completion_date, blocker_reason)
- Add entries to the Task Log / Notes section (Execution Log, Phase Findings, Follow-Up Items)
- Add items within DYNAMIC CONTENT MARKER sections (if the task file includes them)

You MUST NOT:
- Rewrite or rephrase existing checklist items
- Add new checklist items outside of DYNAMIC CONTENT MARKER sections
- Delete or reorder existing items
- Modify the Task Overview, Key Objectives, or Variables sections
- Change the task file's structure or headings

### Frontmatter Update Protocol (F5)

Update frontmatter at these specific points:

| Event | Fields to Update |
|-------|-----------------|
| **Task start** | `status: "🟠 Doing"`, `start_date: [today]`, `updated_date: [today]` |
| **After each work session** | `updated_date: [today]` |
| **Task blocked** | `status: "⚪ Blocked"`, `blocker_reason: [description]`, `updated_date: [today]` |
| **Task completion** | `status: "🟢 Done"`, `completion_date: [today]`, `updated_date: [today]` |

### Error Handling

If an item cannot be completed:

1. **Log the blocker** in the Task Log / Notes section with: timestamp, item reference (step number), error description, attempted resolution
2. **If recoverable** (e.g., agent returned partial results, file exists but is incomplete) — complete what you can and note the gap in Task Log
3. **If unrecoverable** (e.g., required file doesn't exist, dependency missing) — mark the item `- [x]` with a note in Task Log explaining what was blocked and why, then continue to next item. Items are NEVER left unchecked — everything gets marked complete. Success = output file exists. Failure = blocker logged to task notes.
4. **If ALL remaining items are blocked** by the same issue — update frontmatter to "⚪ Blocked" with reason, inform the user, and stop execution

Do NOT block the entire task for individual item failures. Only mark the task as "⚪ Blocked" if ALL remaining items are blocked by the same issue.

### Phase-Gate QA Verification

After completing all items in a phase (all items `- [x]`), phase-gate QA MUST be explicitly invoked by the executor. QA verification is mandatory for every phase except Phase 1 (which is setup-only — status updates, directory creation, and backups don't produce verifiable outputs).

**After every phase (Phase 2+), before proceeding to the next phase:**

1. **Collect phase outputs** — Identify all files created or modified during the phase. These are the artifacts to verify.

2. **Collect verification criteria** — Extract the "ensuring..." clauses from all checked items in the completed phase. These are the acceptance criteria the QA agent will verify against.

3. **Spawn rf-qa** — Use the Agent tool with `subagent_type: "rf-qa"` and `mode: "bypassPermissions"`. The prompt MUST include:
   - **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
   - The task file path and phase number just completed
   - The list of output files to verify (full paths)
   - The extracted "ensuring..." clauses as acceptance criteria
   - The QA report output path: `.dev/tasks/to-do/TASK-[ID]/reviews/qa-phase-[N]-report.md` (the `reviews/` subfolder inside the task's own folder)
   - Instruction to use zero-trust verification — verify claims independently by reading the actual output files, not trusting any prior statements
   - `fix_authorization: true` — the QA agent MUST fix ALL issues in-place regardless of severity (formatting, missing sections, incomplete content, and any other findings)

4. **Process the QA verdict:**
   - **PASS** — Log the pass in the Task Log Phase Findings section. Proceed to the next phase.
   - **FAIL with ALL fixes applied** — The QA agent fixed ALL issues in-place. Log ALL findings and fixes in Task Log. Verify no findings remain unresolved before proceeding.
   - **FAIL with unfixable issues** — Log the issues in Task Log. Attempt a fix cycle: re-execute the specific items whose outputs failed (re-read the task file, identify the failed items by cross-referencing the QA report, re-run them). Then re-run rf-qa. Maximum 3 fix cycles per phase gate. After 3 failed cycles, HALT execution — log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance on how to proceed. Do NOT continue to the next phase without user approval.

5. **Write QA report to disk** — The rf-qa agent writes its report to `.dev/tasks/to-do/TASK-[ID]/reviews/qa-phase-[N]-report.md`. This persists as evidence. The `reviews/` subfolder should be created during Phase 1 setup alongside `research/`, `synthesis/`, and `qa/` subfolders.

**QA gate timing:** The gate runs AFTER all items in a phase are checked off and BEFORE the first item of the next phase is executed. The progress update to the user (Critical Rule #12) happens after the QA gate passes.

**Partitioning for QA:** If a phase produced more than 6 output files, spawn multiple rf-qa instances with `assigned_files` subsets (same partitioning pattern as parallel agent spawning). Merge the QA reports before processing the verdict.

**No exceptions:** QA gates are not optional. Every task file processed by this skill gets phase-gate verification on Phase 2+. This is how Rigorflow maintains trust — every phase's outputs are independently verified before proceeding.

### Post-Completion Validation (Final Phase Only)

After the LAST phase's phase-gate QA passes and BEFORE marking the task "Done," run a final validation pass on the complete output. This catches cross-phase consistency issues and divergent execution — cases where each phase passed individually but the overall result doesn't work as a whole.

**This runs ONCE, after the final phase, not after every phase.**

**Step 1: rf-qa structural validation of complete output**

Spawn `rf-qa` (subagent_type: "rf-qa", qa_phase: "report-validation", fix_authorization: true) with:
- **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
- ALL output files produced across ALL phases (not just the final phase)
- The task file path for cross-referencing against claimed outputs
- Instruction: "Verify cross-phase consistency — outputs from earlier phases that are consumed by later phases match expectations. Verify all 'ensuring...' clauses across the ENTIRE task file are satisfied, not just the final phase. Check for orphaned outputs (files created but never consumed) and missing outputs (files referenced but never created)."
- Output path: `${TASK_DIR}reviews/qa-final-validation-report.md`

**Step 2: rf-qa-qualitative operational validation**

After structural validation passes, spawn `rf-qa-qualitative` (subagent_type: "rf-qa-qualitative", qa_phase: "task-qualitative", fix_authorization: true) with:
- **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
- The task file path
- ALL output files produced across ALL phases (the TARGET_FILE_LIST — extract every unique file path from checklist items)
- ALL source files that were modified during execution
- PROJECT CONVENTIONS from CLAUDE.md (sync models, build gates, test location, CI requirements). If none identified, state "None identified."
- The research directory path if one exists (`${TASK_DIR}research/`)
- `document_type: "Executed Task File"`
- Note in the prompt: "This task has been EXECUTED. Evaluate against ACTUAL outputs on disk, not just planned outputs in checklist items. The agent applies its full 15-item task-qualitative checklist: gate/command dry-run, project convention compliance, intra-phase execution simulation, function signature verification, module context analysis, downstream consumer analysis, test validity, test coverage, error path coverage, runtime failure path trace, completion scope honesty, ambient dependency completeness, kwarg sequencing red flags, function existence claims verification, and cross-reference accuracy for templates."
- Output path: `${TASK_DIR}reviews/qa-qualitative-review.md`

**Parallel partitioning:** If the task produced >15 output files, spawn multiple rf-qa-qualitative instances with assigned subsets of phases/files.

**Handling verdicts:**
- Both PASS → proceed to mark task "Done"
- Either FAIL with all fixes applied → verify fixes, then proceed
- Either FAIL with unfixable issues → log issues, present to user, ask for guidance before marking done

**Read both QA reports. If any issues found (CRITICAL, IMPORTANT, or MINOR), verify fixes were applied correctly. If issues remain unfixed, address ALL of them before marking the task done. Zero leniency — no severity level is exempt.**

---

## Incremental Writing Protocol

This protocol applies whenever you or a subagent creates a file during execution. It is the #1 failure mode across all agents — violating it causes data loss.

**The rule:** Every file creation MUST follow this pattern:
1. **Create the file immediately** with header/frontmatter only using Write
2. **Append content section by section** using Edit, one section at a time
3. **NEVER accumulate content in context** and attempt a single large Write

**Why:** Large single writes hit max token output limits and freeze the process, losing all accumulated work. Incremental writing ensures that even if the session ends mid-file, all previously written sections persist on disk.

**This applies to:** All output files — research files, analysis files, validation reports, documentation, any file created during task execution.

---

## Session Resumption

If the session restarts or context compresses mid-execution:

1. **Find the task file** — Check `.dev/tasks/to-do/` for `TASK-*/` folders. Look inside each for the task file. If the user provided a path, use it directly. Otherwise search for task files with status "🟠 Doing".
2. **Read the task file** — Read it end-to-end to understand the full scope and current state.
3. **Find the first unchecked item** — Scan for the first `- [ ]` item. This is where execution resumes.
4. **Read existing output files** — If the task file lives inside a task folder (e.g., `.dev/tasks/to-do/TASK-[ID]/`), read key output files from its `research/`, `synthesis/`, `qa/`, and `reviews/` subfolders to understand what has been completed. This provides context without re-executing completed items.
5. **Resume the execution loop** — Start the F1 loop from the first unchecked item. Do NOT re-execute any `- [x]` items — they are complete and their outputs exist on disk.
6. **Do not re-research completed topics** — If an item's output file exists, that work is done regardless of whether you "remember" it.

**At session end:**
- All output files should be written to disk
- The task file should reflect exactly which items are checked and unchecked
- The user should know the current state (which phase, which step, what's next)
- Update `updated_date` in frontmatter

---

## Agent Spawning Conventions

When a checklist item instructs you to spawn a subagent, follow these conventions:

### Subagent Type Selection
Use the agent type specified in the checklist item. Common types:
- `general-purpose` — Default for research, file analysis, code exploration
- `rf-analyst` — For completeness verification, cross-validation, gap analysis
- `rf-qa` — For quality gates (research-gate, synthesis-gate, report-validation) and post-completion structural validation
- `rf-qa-qualitative` — For post-completion operational validation (task-qualitative)
- `rf-assembler` — For document assembly from component files
- `rf-task-builder` — For creating MDTM task files
- `rf-task-researcher` — For codebase exploration to gather context
- `Explore` — For quick codebase exploration

### Agent Prompt Handling
The checklist item should embed the full agent prompt (per B2 self-contained pattern). Pass the entire prompt from the item to the Agent tool. Do NOT abbreviate, summarize, or modify the embedded prompt — pass it exactly as written.

### Agent Mode
Unless the checklist item specifies otherwise, use `mode: "bypassPermissions"` for subagents to prevent interactive permission prompts that would block execution.

### Background vs Foreground
- **Foreground (default):** Use when you need the agent's result before proceeding (most cases)
- **Background:** Use when the item explicitly says to run in the background, or when spawning parallel agents where you can process other items while waiting

### Output Quality for Implementation Plans
When a task item requests an implementation plan (from you or a subagent), ensure it includes: (1) specific files to create or modify with full paths, (2) code patterns or function signatures to follow from existing code, (3) integration points with existing systems. Generic steps like "create a service that handles X" are insufficient — they must be actionable enough that a developer or another AI agent could begin work directly.

### Agent Results
When an agent returns:
1. Read any output files it created to verify completion
2. If the agent produced a report with a verdict (PASS/FAIL), note the verdict in Task Log
3. Mark the corresponding checklist item `- [x]`
4. If the agent failed or returned incomplete results, follow the Error Handling protocol

---

## Critical Rules

These rules apply across ALL task file executions. Violations compromise execution quality.

1. **Task file is the source of truth.** Never work from memory of prior state. Always read the task file before acting. Progress is tracked by checked/unchecked items on disk. If your memory of the task conflicts with what the file shows, the file is correct.

2. **Incremental writing is mandatory — ZERO TOLERANCE.** Every file creation's FIRST ACTION must be creating the file on disk using Write (frontmatter/header only). All subsequent content is appended using Edit, one section at a time. NEVER accumulate content in context and attempt a single large Write — this is the #1 failure mode across all agents. It hits max token output limits and freezes the process, losing all work. The procedure is: Write (create file with header) → Edit (append section 1) → Edit (append section 2) → ... → Edit (update Status to Complete).

3. **Maximize parallelism (MANDATORY).** When consecutive checklist items spawn independent subagents within the same phase, you MUST spawn them in parallel using multiple Agent tool calls in a single message. Each agent operates in isolated context and writes to its own file. The only sequential requirement is when one item depends on another's output. This is not optional — it is how Rigorflow achieves depth, breadth, and speed simultaneously.

4. **Execute items as written.** Do not reinterpret, abbreviate, or "improve" checklist items. They were authored with specific context references, action steps, output paths, and verification criteria for a reason. If an item seems wrong, log the issue and ask the user rather than silently deviating.

5. **Evidence-based completion only.** An item is only complete when there is evidence — a file was written, a command produced output, a verification passed. Never mark an item `- [x]` based on "I think I did that" or "that should be fine."

6. **Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, codebase-retrieval for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations. Use Edit for file modifications, not `sed` or `awk`.

7. **One item at a time (with parallel exception).** The default is strictly sequential — complete one item fully before starting the next. The ONLY exception is parallel agent spawning of independent items within the same phase. Even then, each agent's completion is tracked individually.

8. **Never skip the re-read.** After completing an item and marking it `- [x]`, you MUST re-read the task file before identifying the next item. This prevents drift between your mental model and the actual file state, catches any concurrent modifications, and ensures you always work from the latest state.

9. **Log blockers, don't freeze.** If an item can't be completed, log the blocker and continue to the next item. The task should keep making progress on items that aren't blocked. Only stop execution if ALL remaining items are blocked by the same issue.

10. **Respect the task file's structure.** Phases are executed in order. Items within a phase are executed in order. The only exception is parallel batches of independent items. Never jump between phases, never go backward to re-execute items.

11. **Phase boundaries are inviolable QA gates.** A phase boundary is not just a section divider — it is a mandatory QA checkpoint. After completing a phase's last item (Phase 2+), phase-gate QA MUST run and PASS before the first item of the next phase is executed, delegated, or even identified. This applies regardless of how work is delegated — if a subagent is spawned, it receives work from ONE phase only. No item from Phase N+1 may begin until Phase N's QA gate has passed.

12. **The F1 loop is non-delegable.** The executor MUST maintain the READ-IDENTIFY-EXECUTE-UPDATE-REPEAT loop itself. It may spawn subagents to perform the EXECUTE step for individual items, but it MUST NOT delegate the loop — i.e., it must not spawn a subagent and instruct it to "process items X through Y" or "execute the remaining items." The executor is always the one reading the task file, identifying the next item, spawning the subagent (if needed), and marking items complete.

13. **Preserve output artifacts.** Files created during execution persist after the task is complete. They serve as the evidence trail for all claims and enable future re-investigation. Do NOT delete intermediate files, working files, or output files unless the task explicitly instructs you to clean up.

14. **Report progress at milestones.** At the end of each phase (when all items in that phase are `- [x]`), run the phase-gate QA check (see Phase-Gate QA Verification), then briefly inform the user: which phase completed, key outputs produced, QA verdict, which phase is next, and any issues logged. Keep these updates concise — 2-3 sentences maximum. After the FINAL phase's phase-gate QA passes, run the Post-Completion Validation (rf-qa structural + rf-qa-qualitative operational) before marking the task done.

---

## Session Management

This work may span multiple sessions. The task file and output files serve as the persistent record.

**At session start:**
1. Check for the task file (path provided by user, or search `.dev/tasks/to-do/` for `TASK-*/` folders, reading each folder's task file to find status "🟠 Doing")
2. If found, read it and resume from the first unchecked `- [ ]` item
3. Read existing output files referenced in the task file for context
4. Inform the user of current state: which phase, which step, how many items remaining
5. Do not re-execute completed items

**At session end:**
- All output files should be written to disk
- The task file should reflect exactly which items are checked and unchecked
- Update `updated_date` in frontmatter
- Inform the user of current state: which phase, which step, what's next
- If the task is incomplete, tell the user they can resume with `/task .dev/tasks/to-do/TASK-[ID]/TASK-[ID].md`

**Multi-session progress tracking:**
The task file's frontmatter and checked items are the canonical record of progress. The Execution Log in Task Log / Notes provides a human-readable timeline. Between these two, anyone (human or AI) can determine exactly where the task stands and what remains.
