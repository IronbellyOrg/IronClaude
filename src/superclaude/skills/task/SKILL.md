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
   - If the item says to offer or suggest a downstream skill/action (marked `NON-BLOCKING`) → present the offer to the user, mark the item complete immediately, and continue. Do NOT wait for a user response. The user can act on the offer after the task is done.
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
- **Skipping phase-gate QA** — After completing all items in a phase (Phase 2+), you MUST run the full lens-based QA gate (minimum 6 agents: 3+ rf-qa structural lenses + 3+ rf-qa-qualitative content lenses, followed by the Serialized Fix Protocol) before executing any item in the next phase. This is not optional. See Phase-Gate QA Verification for the full protocol. Proceeding to the next phase without a passing QA gate is a prohibited action equivalent to skipping items.
- **Spawning fewer than 6 agents at any QA gate** — Every QA gate (phase-gate and post-completion) requires a minimum of 6 agents (3 rf-qa structural + 3 rf-qa-qualitative content). For intermediate gates (research-gate, synthesis-gate), the minimum is 5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative) per I19 (MDTM template rule defining discrete error-target tiers and minimum agent count floors)9. For task-integrity gates, the minimum is 5 agents (2 rf-qa + 2 rf-qa-qualitative + 1 rf-analyst) per I19. Gates with fewer agents than these floors are a protocol violation equivalent to skipping QA entirely. See Phase-Gate QA Verification for size-based scaling.
- **Skipping post-completion validation** — After the final phase's phase-gate QA passes, you MUST run the full Post-Completion Validation: lens-based structural validation (Step 1), lens-based content validation (Step 2), serialized fix protocol (Step 3), and source-document fidelity gate (Step 4) BEFORE marking the task "Done." See Post-Completion Validation for the full protocol. Marking a task done without running all four steps is a prohibited action.
- **Pausing execution mid-flow to present scope, cost, or time-estimate concerns to the user** — The F1 loop executes every item sequentially per the task file. Cost, scope, and time estimates are established at task file creation time (Stage A of the calling skill). Once execution begins, the executor MUST proceed through every item without pausing to ask the user "are you sure you want to continue given the scope?" or presenting options like "stop here and review, or continue to phase N?". The ONLY halts permitted mid-execution are: (1) all remaining items are blocked by the same unrecoverable issue, (2) a phase-gate QA has failed 3 fix cycles, (3) an item's output fundamentally invalidates the rest of the task file. "This is going to take a while" is not a valid halt reason. "Phase N will spawn many subagents" is not a valid halt reason. "The user might want to review before the next phase" is not a valid halt reason. Scope-awareness pauses violate the F1 loop discipline and the skill's trust model — the user already committed to the full task file when they invoked /task.

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

<!-- Step mapping: SKILL Step 1 = M3 Step 1, SKILL Step 2 = additional (not in M3), SKILL Step 3 = M3 Step 2, SKILL Step 4 = M3 Step 3, SKILL Step 5 = M3 Step 4 (domain-specific lenses), SKILL Step 6 = M3 Step 5 (consolidation), SKILL Step 7 = M3 Step 6 (fix), SKILL Step 8 = M3 Step 7 (verification), SKILL Step 9 = M3 Step 8 (conditional proceed), SKILL Step 10 = additional (write reports) -->

After completing all items in a phase (all items `- [x]`), phase-gate QA MUST be explicitly invoked by the executor. QA verification is mandatory for every phase except Phase 1 (which is setup-only — status updates, directory creation, and backups don't produce verifiable outputs).

**Minimum Agent Counts — these are FLOORS, not targets:**

| Phase Output Size | rf-qa Agents (structural lenses) | rf-qa-qualitative Agents (content lenses) | Total Minimum |
|-------------------|----------------------------------|------------------------------------------|---------------|
| <500 lines | 3 | 3 | 6 |
| 500-1500 lines | 4 | 4 | 8 |
| 1500-3000 lines | 5 | 5 | 10 |
| >3000 lines | 6 | 6 | 12 |

**1-2 agent QA gates are PROHIBITED.** Any QA gate that spawns fewer than 6 agents total (3 rf-qa + 3 rf-qa-qualitative) is a violation of this protocol.

**Intermediate Gate Minimums (Research, Synthesis, and Task-Integrity):**

Intermediate gates use a DIFFERENT agent type mix than final-document gates. These are gates that run mid-pipeline (e.g., after research, after synthesis) rather than on the final assembled output.

| Gate | Minimum Agents | Agent Types |
|------|---------------|-------------|
| Research gate (Phase 3) | 5 | 2 rf-analyst (completeness + cross-validation) + 2 rf-qa (evidence-quality + gap-detection) + 1 rf-qa-qualitative (research-depth) |
| Synthesis gate (Phase 5) | 5 | 2 rf-analyst (synthesis-accuracy + source-tracing) + 2 rf-qa (structure + content-quality) + 1 rf-qa-qualitative (synthesis coherence) |
| Task-integrity gate | 5 | 2 rf-qa (B2-self-containment + phase-structure) + 2 rf-qa-qualitative (operational-correctness + qa-gate-sufficiency) + 1 rf-analyst (task-research-alignment) |

Partitioning applies on top: if research files >6, each agent type gets partitioned (e.g., 10 research files → 4 rf-analyst + 4 rf-qa + 2 rf-qa-qualitative = 10 agents at research gate). If synthesis files >4, partition similarly.

rf-qa-qualitative at intermediate gates is mandatory. It catches the gap where research/synthesis is structurally complete but qualitatively shallow.

**After every phase (Phase 2+), before proceeding to the next phase:**

1. **Collect phase outputs** — Identify all files created or modified during the phase. Measure total output size in lines to determine the agent count tier from the table above.

2. **Collect verification criteria** — Extract the "ensuring..." clauses from all checked items in the completed phase. These are the acceptance criteria the QA agents will verify against.

3. **Spawn lens-based rf-qa agents (PARALLEL)** — Spawn the required number of rf-qa agents in parallel, each with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`, and `fix_authorization: false` (report-only). Each agent gets ONE structural lens from the standard set:
   - **Template conformance lens** — All required sections present, correct ordering, no remaining placeholders/sentinels
   - **Internal consistency lens** — IDs match across tables, counts agree, cross-references resolve, no contradictions within the document
   - **Evidence quality lens** — All claims cite file paths/line numbers, no unverified assertions, no hallucinated paths
   - **Completeness lens** — Every topic from scope discovery appears in the output, no gaps, no silently dropped items
   - (Additional structural lenses as needed for the tier — e.g., split completeness into coverage + depth for higher tiers)

   Every rf-qa agent prompt MUST include:
   - **ADVERSARIAL STANCE:** "Assume this document has at least N errors. Find them." Error targets by output size: 5 for <500 lines, 10 for 500-1500 lines, 15 for 1500-3000 lines, 20 for >3000 lines (per I19 discrete tiers). A verdict of 0 issues requires evidence you thoroughly checked every item in your lens.
   - The task file path and phase number just completed
   - The list of output files to verify (full paths)
   - The extracted "ensuring..." clauses as acceptance criteria
   - The agent's specific lens focus and lens-specific checklist (NOT a generic "check everything" prompt)
   - QA report output path: `${TASK_DIR}qa/qa-structural-[lens-name]-report.md` (for rf-qa) or `${TASK_DIR}qa/qa-content-[lens-name]-report.md` (for rf-qa-qualitative)
   - Instruction to use zero-trust verification

4. **Spawn lens-based rf-qa-qualitative agents (PARALLEL)** — Spawn the required number of rf-qa-qualitative agents in parallel, each with `subagent_type: "rf-qa-qualitative"`, `mode: "bypassPermissions"`, and `fix_authorization: false` (report-only). Each agent gets ONE content lens from the standard set:
   - **Actionability lens** — Every recommendation, task, or requirement is specific enough to execute without interpretation; criteria are testable with pass/fail not aspirational
   - **Numbers and metrics lens** — All quantitative claims are internally consistent, realistic, and sourced; percentages add up; counts match between sections
   - **Cross-reference chain integrity lens** — Trace end-to-end chains (e.g., requirement → task → deliverable → test) and verify every link exists
   - **Domain accuracy lens** — Claims about the codebase match actual code; claims about the product match actual capabilities; no aspirational features described as current
   - (Additional content lenses as needed for the tier)

   Every rf-qa-qualitative agent prompt MUST include the same adversarial stance, lens-specific focus, and report output path pattern as the rf-qa agents.

5. **Spawn domain-specific lens agents (PARALLEL, if applicable, M3 (Lens-Based QA Sequence pattern from the MDTM template) Step 4)** — If the task file includes domain-specific lens agents beyond the standard 8 (defined by the skill that produced the task file), spawn them in parallel alongside Steps 3-4. Each domain-specific lens agent follows the same pattern: one focused lens, one report file, `fix_authorization: false`. Domain-specific lens prompts are embedded in the task file's QA gate items by the skill that created the task file. The executor spawns them exactly as written.

6. **Findings Consolidation (M3 Step 5)** — After ALL lens agents (Steps 3-5) return, read all QA reports and consolidate into a single findings list at `${TASK_DIR}qa/qa-phase-[N]-consolidated-findings.md` (where [N] is the phase number, e.g., `qa-phase-2-consolidated-findings.md`; for post-completion use `${TASK_DIR}qa/qa-final-consolidated-findings.md`). Deduplicate overlapping findings (same issue found by multiple lenses listed once with all originating lenses noted). Preserve the highest severity rating when duplicates disagree. If zero findings across all agents: verdict is PASS, log and proceed to the next phase. Each step below becomes its own `- [ ]` checklist item when encoded in a task file.

7. **Fix Agent (M3 Step 6)** — If findings exist, spawn ONE `rf-qa` agent with `fix_authorization: true` and the consolidated findings file as input. This single agent applies ALL fixes to the output files. No other agent modifies files during this step.

8. **Verification Round (M3 Step 7, PARALLEL)** — After the fix agent returns, spawn a verification round: minimum 2 agents (1 rf-qa + 1 rf-qa-qualitative, both `fix_authorization: false`). Verification rounds are exempt from the 6-agent minimum — they use a reduced 2-agent minimum because they verify a targeted set of fixes against the consolidated findings list, not the full document. They verify: (a) all findings from the consolidated list were addressed, (b) fixes were applied correctly (no garbled text, no lost content), (c) no new issues were introduced by the fixes. Output: `${TASK_DIR}qa/qa-verification-structural-report.md` and `${TASK_DIR}qa/qa-verification-content-report.md`.

9. **Conditional Proceed (M3 Step 8)** — IF both verification agents report PASS, proceed to the next phase. IF either reports FAIL, repeat Steps 6-8 (consolidate new + remaining findings, fix, verify). Maximum 3 fix cycles total (per I16 (MDTM template rule: maximum 3 fix-verify cycles per gate)6). After 3 failed cycles: HALT execution — log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance. Do NOT continue to the next phase without user approval.

10. **Verify all QA reports exist on disk** — Check that each lens agent wrote its report to the expected path. If any reports are missing, the agent may have failed silently — log missing reports as blockers in Task Log. The expected paths are `${TASK_DIR}qa/qa-structural-[lens-name]-report.md` (rf-qa) or `${TASK_DIR}qa/qa-content-[lens-name]-report.md` (rf-qa-qualitative). The consolidated findings file, verification reports, and fix reports also persist. The `qa/` subfolder should be created during Phase 1 setup alongside `research/` and `synthesis/` subfolders.

**QA gate timing:** The gate runs AFTER all items in a phase are checked off and BEFORE the first item of the next phase is executed. The progress update to the user (Critical Rule #15) happens after the QA gate passes.

**Partitioning for QA (multi-file outputs):** If a phase produced more than 6 output files, spawn multiple instances of each lens agent type with `assigned_files` subsets (same partitioning pattern as parallel agent spawning). Merge each lens's partitioned reports before consolidation.

**Partitioning for QA (single large documents):**

| Document Size | Partitioning | Section Assignment |
|---------------|-------------|--------|
| <500 lines | No partitioning (each lens agent reads full doc) | Full document per lens |
| 500-1500 lines | Optional — lens-based is sufficient | Full document per lens |
| 1500-3000 lines | Mandatory section partitioning for fidelity gate | Split source docs across 3-4 fidelity agents |
| >3000 lines | Mandatory partitioning for ALL gates | Section ranges assigned to lens agents too |

For documents >3000 lines, each lens agent gets a section range (e.g., Sections 1-7 / 8-14 / 15-21 / 22-28) IN ADDITION to its lens focus. The agent checks its lens quality dimension only within its assigned sections.

**No exceptions:** QA gates are not optional. Every task file processed by this skill gets phase-gate verification on Phase 2+. This is how Rigorflow maintains trust — every phase's outputs are independently verified before proceeding. Gates that spawn fewer than 6 agents are a protocol violation.

### Post-Completion Validation (Final Phase Only)

After the LAST phase's phase-gate QA passes and BEFORE marking the task "Done," run a final validation pass on the complete output. This catches cross-phase consistency issues and divergent execution — cases where each phase passed individually but the overall result doesn't work as a whole.

**This runs ONCE, after the final phase, not after every phase.**

**Step 0: Pre-QA Verification (I17 checks 1-4)**

Before running any lens-based QA, complete these prerequisite checks:

1. **All items marked complete** — Scan the entire task file and verify every `- [ ]` item has been marked `- [x]`. If any unchecked items remain, they are either skipped (prohibited) or the task is not actually complete. HALT and resolve before proceeding.
2. **All output files exist on disk** — Extract every file path referenced in checklist items (output paths, report paths, artifact paths). Verify each exists via Glob. Log any missing files as CRITICAL issues in Task Log.
3. **Blocker entries have resolution notes** — Read the Task Log / Notes section. For every blocker entry logged during execution, verify it has a resolution note explaining how it was resolved or why it was deferred. Unresolved blockers without notes are a FAIL.
4. **Tests pass for code-modifying tasks** — If the task modified source code files (not documentation, not configuration), run the relevant test suite and verify all tests pass. Log test results in Task Log. If tests fail, HALT and fix before proceeding to lens-based QA.

All four checks must pass before proceeding to Step 1. These are non-negotiable prerequisites — lens-based QA assumes the task is mechanically complete.

**Step 1: Lens-based structural validation of complete output (PARALLEL)**

Determine the total output size across ALL phases and select the agent count tier from the Minimum Agent Counts table in Phase-Gate QA Verification. Spawn the required number of rf-qa agents in parallel, each with `subagent_type: "rf-qa"`, `qa_phase: "report-validation"`, `mode: "bypassPermissions"`, and `fix_authorization: false` (report-only). Each agent gets ONE structural lens:

- **Template conformance lens** — All required sections present, correct ordering, no remaining placeholders/sentinels across ALL output files
- **Internal consistency lens** — Cross-phase consistency: outputs from earlier phases consumed by later phases match expectations. IDs, counts, and references agree across the entire task output.
- **Evidence quality lens** — All claims cite file paths/line numbers. Verify all 'ensuring...' clauses across the ENTIRE task file are satisfied, not just the final phase.
- **Completeness lens** — Check for orphaned outputs (files created but never consumed) and missing outputs (files referenced but never created). Every planned output exists on disk.
- (Additional structural lenses as needed for the tier)

Every agent receives: ALL output files produced across ALL phases, the task file path for cross-referencing, adversarial stance with error count target.
Output paths: `${TASK_DIR}qa/qa-final-[lens-name]-report.md`

**Step 2: Lens-based content validation of complete output (PARALLEL)**

Spawn the required number of rf-qa-qualitative agents in parallel, each with `subagent_type: "rf-qa-qualitative"`, `qa_phase: "task-qualitative"`, `mode: "bypassPermissions"`, and `fix_authorization: false` (report-only). Each agent gets ONE content lens:

- **Actionability lens** — Every output is actionable and specific enough to use without interpretation
- **Numbers and metrics lens** — All quantitative claims across all outputs are internally consistent
- **Cross-reference chain integrity lens** — Trace end-to-end chains across phases and verify every link exists
- **Domain accuracy lens** — Claims about the codebase match actual code; no aspirational features described as current
- (Additional content lenses as needed for the tier)

Every agent receives:
- The task file path
- ALL output files produced across ALL phases (the TARGET_FILE_LIST — extract every unique file path from checklist items)
- ALL source files that were modified during execution
- PROJECT CONVENTIONS from CLAUDE.md (sync models, build gates, test location, CI requirements). If none identified, state "None identified."
- The research directory path if one exists (`${TASK_DIR}research/`)
- `document_type: "Executed Task File"`
- Note in the prompt: "This task has been EXECUTED. Evaluate against ACTUAL outputs on disk, not just planned outputs in checklist items. The agent applies its full 15-item task-qualitative checklist: gate/command dry-run, project convention compliance, intra-phase execution simulation, function signature verification, module context analysis, downstream consumer analysis, test validity, test coverage, error path coverage, runtime failure path trace, completion scope honesty, ambient dependency completeness, kwarg sequencing red flags, function existence claims verification, and cross-reference accuracy for templates."
- Output paths: `${TASK_DIR}qa/qa-final-content-[lens-name]-report.md`

**Step 3: Consolidate findings and apply fixes (Serialized Fix Protocol)**

After ALL Step 1 + Step 2 lens agents return, follow the Serialized Fix Protocol (see dedicated section below). Consolidate all findings, spawn a single fix agent, then a verification round. Maximum 3 fix cycles.

**Step 4: Source-Document Fidelity Gate (M4: Source-Document Fidelity Gate pattern from the MDTM template)** — Follow the Source-Document Fidelity Gate protocol defined in the dedicated section below. If the task did not consume source documents to produce its outputs, skip this step.

**Parallel partitioning:** If the task produced >15 output files, spawn multiple instances of each lens agent type with assigned subsets of phases/files.

**Handling verdicts:**
- All steps PASS → proceed to mark task "Done"
- Any step FAIL with all fixes applied → verify fixes, then proceed
- Any step FAIL with unfixable issues → log issues, present to user, ask for guidance before marking done

**Read ALL QA reports (lens reports + fidelity reports). If any issues found (CRITICAL, IMPORTANT, or MINOR), verify fixes were applied correctly. If issues remain unfixed, address ALL of them before marking the task done. Zero leniency — no severity level is exempt.**

### Serialized Fix Protocol

When multiple QA agents evaluate the same document or set of output files, fixes MUST be applied serially, not in parallel. Parallel fix authorization causes churn — Agent A fixes line 50 one way, Agent B fixes line 50 a different way, and the next round has to resolve contradictions.

**The protocol:**

1. **Report-only round (PARALLEL):** Spawn all lens-based QA agents with `fix_authorization: false`. They evaluate and report findings only. They do NOT modify any files.

2. **Consolidate findings:** Read all QA reports. Merge findings into a single consolidated findings list at the designated path (e.g., `${TASK_DIR}qa/qa-consolidated-findings.md` or `${TASK_DIR}qa/qa-final-consolidated-findings.md`). Deduplicate findings that multiple agents flagged independently. Preserve the highest severity rating when duplicates disagree. **Scope filtering:** After merging, read the task file's checklist items to identify which files and components the task touches. Separate findings into in-scope (affected file/component appears in a checklist item) and out-of-scope (it does not). Write ONLY in-scope findings to the consolidated findings file. Log out-of-scope findings as **Follow-Up Items** in the task file's Task Log / Notes section — these are valuable findings but outside this task's scope and must not be fixed here.

3. **Single fix agent (SEQUENTIAL):** If findings exist, spawn ONE `rf-qa` agent with `fix_authorization: true` and the consolidated findings list. This agent applies ALL fixes. No other agent modifies files during this step.

4. **Verification round (PARALLEL):** After the fix agent returns, spawn a verification round: minimum 2 agents (1 rf-qa + 1 rf-qa-qualitative, both `fix_authorization: false`) to confirm:
   - All findings from the consolidated list were addressed
   - Fixes were applied correctly (no garbled text, no lost content)
   - No new issues were introduced by the fixes

5. **Iteration:** If verification finds new issues, repeat from step 2 with updated findings (re-consolidate so the fix agent gets both remaining unfixed issues and newly introduced issues). Maximum 3 fix cycles total per gate.

6. **Escalation:** After 3 failed cycles, HALT — log all remaining issues in the Task Log, present findings to the user, and ask for guidance.

**Where this applies:** Every QA gate that spawns 3+ agents evaluating the same file(s). This includes phase-gate QA, post-completion validation, and source-document fidelity gates.

---

### Source-Document Fidelity Gate

A fidelity gate verifies that generated output faithfully represents its source inputs. This is fundamentally different from lens-based QA, which evaluates the output on its own terms. Fidelity agents read BOTH the original source documents AND the generated output, then verify the output says what the sources say.

**When it applies:** Every task that consumes source documents to produce output. Examples:
- PRD skill: reads codebase → produces PRD (verify PRD claims match code)
- TDD skill: reads PRD + codebase → produces TDD (verify TDD covers all PRD requirements AND matches code)
- Roadmap skill: reads PRD + TDD → produces roadmap (verify every requirement has a real implementing task)
- Tech-reference: reads source code → produces reference doc (verify doc matches code)
- Task executor: any task whose items reference source files and produce derivative output

**When it does NOT apply:** Tasks that produce original content not derived from source documents (e.g., creating a new skill from scratch, brainstorming). If no source documents exist, skip the fidelity gate.

**The fidelity gate follows M4's 6-step sequence:**

**Step 1 (Source Document Identification):** Identify all source documents consumed to produce the output. The skill or task file MUST specify these explicitly.

**Step 2 (Fidelity Agents — PARALLEL):** Spawn fidelity agents (minimum 2, partitioned to 3-4 if source docs exceed 1000 lines total). Each agent is an rf-qa instance with `fix_authorization: false`. Each agent gets its assigned section range of the source documents + the FULL output document. Each fidelity agent checks:
1. **Semantic coverage** — For each requirement/spec/feature in the source docs, does the output contain a corresponding item that actually addresses it (not just mentions the ID)?
2. **Detail preservation** — Source-specific details (error code counts, field types, index names, state pairs, thresholds) survive into the output, not just high-level summaries
3. **Phantom coverage detection** — IDs present in coverage/traceability matrices must be verified by reading the actual task/section description to confirm semantic match, not just ID presence
4. **Operational/compliance completeness** — Source docs mentioning compliance, security, operational, or regulatory requirements must each have a corresponding output item

Report output: `${TASK_DIR}qa/qa-source-fidelity-[N]-report.md` (numbered if partitioned)

**Step 3 (Cross-Source Contradiction Agent):** If multiple source documents exist, spawn ONE additional rf-qa agent that reads ALL source documents and checks for contradictions between them (e.g., PRD says 8 error codes, TDD says 12). This agent does NOT read the output — it only checks source-to-source consistency. Output: `${TASK_DIR}qa/qa-cross-source-contradictions-report.md`.

**Step 4 (Fidelity Findings Consolidation):** Read all fidelity reports (from Step 2) and the contradiction report (from Step 3, if applicable). Produce a consolidated fidelity findings file at `${TASK_DIR}qa/qa-fidelity-consolidated-findings.md`.

**Step 5 (Fidelity Fix Agent):** If findings exist, spawn ONE rf-qa agent with `fix_authorization: true` and the fidelity findings file as input. Apply all fixes.

**Step 6 (Fidelity Verification):** Spawn minimum 2 verification agents to confirm fidelity fixes were applied correctly. Maximum 3 fix cycles (per I16), then HALT and escalate to user.

**Agent count (Step 2):**
- Minimum 2 fidelity agents
- If source docs exceed 1000 lines total, partition across 3-4 agents (each assigned a section range of the source docs + the FULL output document)
- Each fidelity agent reads its assigned source section range + the FULL output

**Report output:** `${TASK_DIR}qa/qa-source-fidelity-[N]-report.md` (numbered if partitioned)

**Sequencing:** The fidelity gate runs AFTER the lens-based QA gate passes, not before. The document must be structurally sound before checking fidelity.

**Fidelity gate at Post-Completion:** The Post-Completion Validation includes a fidelity gate as Step 4. This checks that the task's complete output set faithfully represents all source documents referenced across all phases.

---

### Lens-Based QA Agent Prompts

This section provides template prompts for the 8 standard lenses. Skills and task files reference these templates when constructing lens agent prompts. Each prompt includes the lens focus, the adversarial stance, and the checklist. Output format is inherited from the rf-qa/rf-qa-qualitative agent definitions.

**All lens agents share this preamble (insert at the top of every lens prompt):**

> You are a QA agent performing a FOCUSED evaluation. You have ONE lens — ONE quality dimension to evaluate. Ignore everything outside your lens. Your job is to FIND problems, not confirm correctness. Assume this document has at least {error_target} errors within your lens. Find them.
>
> **Your lens:** {lens_name}
> **Files to evaluate:** {file_list}
> **Acceptance criteria:** {ensuring_clauses}
> **Report output path:** {report_path}
> **fix_authorization:** false (report findings only — do NOT modify any files)

#### Structural Lenses (rf-qa)

**1. Template Conformance Lens**
> Checklist: (1) All required sections from the template/spec are present. (2) Sections are in the correct order. (3) No remaining placeholder text, sentinel values, or TODO markers. (4) All required frontmatter fields are populated. (5) Section heading hierarchy is correct (no skipped levels). (6) Required tables have all columns and rows populated.

**2. Internal Consistency Lens**
> Checklist: (1) IDs referenced in one section exist in the section they point to. (2) Counts stated in summaries match actual counts in detail sections. (3) Cross-references between sections resolve correctly. (4) No contradictions between sections (e.g., Section A says X, Section B says not-X). (5) Terminology is used consistently (same concept = same term throughout). (6) Version numbers, dates, and identifiers are consistent.

**3. Evidence Quality Lens**
> Checklist: (1) Every factual claim cites a file path and line number. (2) Cited file paths actually exist (verify via Glob). (3) Claims about code behavior match what the code actually does (verify via Read). (4) No unverified assertions presented as fact. (5) No hallucinated paths or function names. (6) Statistical claims have sources or derivation shown.

**4. Completeness Lens**
> Checklist: (1) Every topic from scope discovery / input analysis appears in the output. (2) No items silently dropped between phases. (3) Every "ensuring..." clause from checklist items is satisfied. (4) No sections are stubs or suspiciously thin relative to their scope. (5) Edge cases, error paths, and negative scenarios are covered, not just happy paths. (6) All phases contributed their expected outputs.

#### Content Lenses (rf-qa-qualitative)

**5. Actionability Lens**
> Checklist: (1) Every recommendation is specific enough to execute without interpretation. (2) Acceptance criteria are testable with pass/fail, not aspirational ("should be fast" = FAIL, "p95 < 200ms" = PASS). (3) Task descriptions include what to do, which files to modify, and how to verify. (4) No vague directives ("improve", "enhance", "optimize" without specific targets). (5) Dependencies are explicit ("requires X from Phase N"), not implied. (6) Effort/complexity estimates are present where applicable.

**6. Numbers and Metrics Lens**
> Checklist: (1) All percentages in a group add to 100% (or are explicitly noted as non-exclusive). (2) Counts in summary match counts in detail. (3) Numeric ranges are realistic and internally consistent. (4) Growth rates, market sizes, and projections have sources. (5) Performance targets are specific and measurable. (6) Effort estimates are internally consistent (task estimates sum to phase estimates).

**7. Cross-Reference Chain Integrity Lens**
> Checklist: (1) Every requirement traces to at least one implementation item. (2) Every implementation item traces back to a requirement. (3) Traceability chains are complete end-to-end (requirement → design → task → test). (4) No orphaned items (implementation without requirement = scope creep). (5) No phantom coverage (ID present but implementation doesn't actually address the requirement). (6) Dependency chains are acyclic.

**8. Domain Accuracy Lens**
> Checklist: (1) Claims about the codebase match actual code (verify by reading files). (2) Claims about the product match actual capabilities (no aspirational features described as current). (3) Architecture descriptions match the actual architecture. (4) API descriptions match actual endpoints/schemas. (5) Configuration values match actual defaults. (6) Technology versions match actual package.json / requirements.txt.

**Skills MAY define additional domain-specific lenses beyond these 8.** Domain-specific lens prompts follow the same template structure but with domain-relevant checklists.

**Domain-specific lenses at phase gates:** If the task file includes additional domain-specific lens agents beyond the standard 8 (e.g., PRD-specific lenses like competitive-honesty, market-claim-verifiability, persona-to-story-consistency), spawn them in parallel with the structural and content lens agents per M3 Step 4. Domain-specific lenses follow the same pattern: one lens, one report, `fix_authorization: false`.

#### Standard QA Report Output Format

All lens agents MUST use this report format (matching the rf-qa agent definition):

```markdown
# QA Report — [Lens Name]

**Topic:** [topic under review]
**Date:** [today]
**Phase:** [phase-gate / post-completion / fidelity]
**Lens:** [lens name]
**Fix cycle:** [1 / 2 / 3 / N/A]

---

## Overall Verdict: [PASS / FAIL]

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | [check name] | PASS / FAIL | [what you verified and how] |

## Summary
- Checks passed: [count] / [total]
- Checks failed: [count]
- Critical issues: [count]
- Issues fixed in-place: [count] (if fix-authorized)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL / IMPORTANT / MINOR | [file:section] | [what's wrong] | [specific fix] |

## Actions Taken
[If fix-authorized, list every fix applied]

## Recommendations
- [Actions needed before proceeding]

## QA Complete
```

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

13. **Downstream offers are non-blocking.** Items that offer or suggest invoking another skill (e.g., "Would you like to create a TDD?") MUST be the last items in the final phase, MUST come after all task-completion actions (status update, completion date, task summary), and MUST be marked `NON-BLOCKING`. Present the offer, mark the item complete, done. The ONLY thing that halts task execution mid-flow is a major critical issue (e.g., a finding that fundamentally invalidates the task). Conditional user questions about optional next steps are never gates.

14. **Preserve output artifacts.** Files created during execution persist after the task is complete. They serve as the evidence trail for all claims and enable future re-investigation. Do NOT delete intermediate files, working files, or output files unless the task explicitly instructs you to clean up.

15. **Report progress at milestones.** At the end of each phase (when all items in that phase are `- [x]`), run the phase-gate QA check (see Phase-Gate QA Verification), then briefly inform the user: which phase completed, key outputs produced, QA verdict, which phase is next, and any issues logged. Keep these updates concise — 2-3 sentences maximum. After the FINAL phase's phase-gate QA passes, run the Post-Completion Validation (pre-QA verification + lens-based structural + lens-based content + serialized fix + source-document fidelity gate) before marking the task done.

16. **No scope/cost-anxiety pauses during execution.** Once a task file begins executing (via /task or any execution loop), the executor MUST process every item sequentially to completion. It MUST NOT pause mid-execution to present the user with options like "stop here and review, or continue to phase N?" or to flag scope/cost/time concerns. Scope is established at task file creation time. Cost is committed when the user invokes execution. The only permitted mid-execution halts are: all items blocked by the same unrecoverable issue, phase-gate QA failing 3 fix cycles, or an item output fundamentally invalidating the rest of the task. "This will take a while" / "Phase N is expensive" / "the user might want to review" are NOT valid halt reasons. Pausing for these reasons violates the F1 loop discipline and the skill's trust model.

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
