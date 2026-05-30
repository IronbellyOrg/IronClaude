# Research 04: Template & Examples

**Researcher**: 4 of 5
**Topic**: Template & Examples
**Task**: TASK-RF-20260529-160318
**Status**: Complete

## Sources

- **Primary**: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1204 lines total; PART 1 instructions L46-887; PART 2 template L890-1204)
- **Prior task examples**:
  - `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260527-043715-sc-reflect-rebuild/TASK-RF-20260527-043715-sc-reflect-rebuild.md` (73 items, 7 phases, edits SKILL.md + refs + Makefile + commands, uses make sync-dev/verify-sync)
  - `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260520-230051/TASK-RF-20260520-230051.md` (21 items, 5 phases, edits SKILL.md + evals.json + hook script, uses make sync-dev/verify-sync as sole parity gate)

---

## 1. Frontmatter Fields (Template L1-44)

The full frontmatter shape that the generated MDTM file MUST emit. All fields appear in the template; "required" means the value MUST be populated (not left as placeholder text).

| Field | Type | Default / Placeholder | Required? |
|---|---|---|---|
| `id` | string | `"TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"` | YES — must be the actual task ID, e.g. `"TASK-RF-20260529-160318"` |
| `title` | string | `"[Clear, Action-Oriented Task Title]"` | YES |
| `description` | string | `"[Detailed description...]"` | YES |
| `status` | string | `"🟡 To Do"` (start), updated to `"🟠 Doing"` → `"🟢 Done"` per F5 / I11 | YES |
| `type` | string | `"📝 Documentation"` (template default; pick from project taxonomy) | YES |
| `priority` | string | `"🔼 High"` | YES |
| `created_date` | YYYY-MM-DD | `"YYYY-MM-DD"` | YES — must be today's date (2026-05-29) |
| `updated_date` | YYYY-MM-DD | `"YYYY-MM-DD"` | YES |
| `assigned_to` | string | `"[agent-name]"` (typically `"rf-task-executor"` based on prior examples) | YES |
| `autogen` | bool | `false` | required-default |
| `autogen_method` | string | `""` | optional |
| `coordinator` | string | `orchestrator` | required-default |
| `parent_task` | string | `"[PARENT-TASK-ID]"` | optional — empty if no parent |
| `depends_on` | list | `["[DEPENDENCY-TASK-ID-1]", ...]` | optional — empty list `[]` if none |
| `related_docs` | list of `{path, description}` | template provides 3-item placeholder | YES — must list all source/spec/research files |
| `tags` | list | `["[relevant]", "[tags]", ...]` | YES |
| `template_schema_doc` | string | `""` | YES per `/sc:task` convention — must be `".claude/templates/workflow/02_mdtm_template_complex_task.md"` (prior tasks set this; e.g. TASK-RF-20260520-050937 L38) |
| `estimation` | string | `""` | optional (`"Quick"` / `"Medium"` / `"Heavy"` in prior tasks) |
| `sprint` | string | `""` | optional |
| `due_date` | YYYY-MM-DD | `""` | optional |
| `start_date` | YYYY-MM-DD | `""` | populated when status → Doing |
| `completion_date` | YYYY-MM-DD | `""` | populated when status → Done |
| `blocker_reason` | string | `""` | populated only if Blocked |
| `ai_model` | string | `""` | optional |
| `model_settings` | string | `""` | optional |
| `review_info` | object `{last_reviewed_by, last_review_date, next_review_date}` | empty strings | optional |
| `task_type` | enum `static` \| `dynamic` | `static` | YES — `static` unless the task uses I6 dynamic content markers |

---

## 2. Section A-K Rules

### A. CORE PRINCIPLES (Template L68-128)

**A1. Workflow document availability check** (L72-83) — Orchestrator checks whether governing workflow docs exist (typically `.gfdoc/workflows/`, `.roo/workflows/`). If they DO exist, include workflow-compliance sections; if NOT, omit `[WORKFLOW-DEPENDENT]` sections and derive requirements from user input.

**A2. Workflow document deep integration** [WORKFLOW-DEPENDENT] (L85-89): "BEFORE creating task content: Thoroughly review the complete governing workflow document. Extract EVERY requirement, phase, step, and quality standard from the workflow. Map EVERY workflow element to corresponding task elements."

**A3. Complete granular breakdown** (L91-95, verbatim): "Break down EVERY workflow phase into atomic, verifiable checklist items. Create individual checklist items for EVERY file, component, or iteration. NO high-level or bulk operations allowed - everything must be granular. Include exact file paths, specific requirements, and measurable outcomes."

**A4. Iterative process structure** (L97-116): "For ANY process involving multiple items (files, components, etc.): Pre-enumerate ALL items to be processed in initial step. Create individual checklist item for each specific item. Require incremental updates after each item. Include consolidation step only after all items complete." Uses the X.1 scan/enumerate → X.2 per-item → X.3 consolidate pattern.

**A5-A6** [WORKFLOW-DEPENDENT] (L118-128) — Cross-stage integration + workflow compliance enforcement: every phase specifies inputs from previous stages; copy quality standards directly from workflow docs.

### B. SELF-CONTAINED CHECKLIST ITEMS (CRITICAL) (Template L130-196)

**B1. Why it matters** (L134-140) — Session rollovers mean batch-1 context is lost by batch-3+. Standalone "read context" items are USELESS because the context evaporates.

**B2. The 6-element pattern** (L142-148, verbatim — note template lists **6** elements, not the 5 implied by some sections; the BUILD_REQUEST's "5-field" framing corresponds to the first 4 + the completion gate, with #5 "Evidence on Failure Only" being a logging convention):

> 1. **Context Reference with WHY** - What file(s) to read and why that context is needed for this specific action
> 2. **Action with WHY** - What to do with that context and why it needs to be done
> 3. **Output Specification** - The exact output file name, location, what content to produce, and template to follow (if applicable)
> 4. **Integrated Verification** - An "ensuring..." clause that specifies what must be verified (DO NOT assume, hallucinate, or make up any information - all content MUST be derived from source files referenced in the checklist item, 100% accuracy based on source materials, document negative evidence when verification fails)
> 5. **Evidence on Failure Only** - Log to task notes ONLY if unable to complete due to blockers, missing info, or errors (successful completion is evidenced by the output file itself)
> 6. **Explicit Completion Gate** - "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

**B3. Format** (L150-153) — ONE FULL PARAGRAPH per item; verbose, explanatory; reads like a complete prompt executable without prior context. NOT multi-line / bulleted.

**B4. Canonical example** (L155-158, verbatim — quoted in §5 below).

**B5. Forbidden patterns** (L164-183):
- Standalone "read context" items
- Missing context reference (no source of truth)
- Multi-line / bulleted items
- Separate verification / confirmation items
- Overly granular items ("create directory" alone)
- Separate REMINDER blocks between items

**B7. Key principles** (L189-196): each item is a COMPLETE PROMPT; context embedded in action; verification embedded via "ensuring..."; output file = evidence; only log on failure; one paragraph; QA process handles inter-batch verification.

### C. EMBEDDING REQUIREMENTS (NOT SEPARATE SECTIONS) (L198-230)

- **C1 Outputs & Deliverables**: embedded in the item that creates the output (`"...then create the file X at path Y..."`); no separate "Outputs & Deliverables" section.
- **C2 Success Criteria**: embedded as `"ensuring..."` clause; no separate Success Criteria section.
- **C3 Verification**: embedded in action items; no separate Verification Checklist section.
- **C4 Task Completion**: handled by Post-Completion Actions section only (frontmatter + Execution Log); no "Task Completion and Handoff Protocol" section.

### D. MANDATORY TASK SECTIONS (L232-272)

- **D1 Workflow Compliance Declaration** [WORKFLOW-DEPENDENT]: informational only, no checklist items.
- **D2 Cross-Stage Integration Requirements** [WORKFLOW-DEPENDENT]: informational only.
- **D3 Critical Rule** (L269-272): **NO CHECKLIST ITEMS may appear before Phase 1 begins**. Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable).

### E. CHECKLIST STRUCTURE RULES (L274-388)

- **E1 Checkbox format**: `- [ ] Action text`; flat structure only; NO nested checkboxes; NO parent checkboxes summarizing children; one atomic action per checkbox; use **Step X.Y:** headers for grouping.
- **E2 Critical structure rule (fundamental)**: summary/parent checkboxes MUST come AFTER component items, never before. Use descriptive headers (no checkbox) for grouping.
- **E3 Sequential order**: top-to-bottom only; never require marking items above current position; no "go back and update", "see below", "return to phase" patterns.
- **E4 Formatting**: NEVER place checkboxes next to step numbers; step numbers are bold headings; NO separate REMINDER blocks between items.

### F. EXECUTION REQUIREMENTS (FOR WORKER AGENTS) (L390-451)

- **F1 Five-step pattern**: READ → IDENTIFY → EXECUTE → UPDATE → REPEAT (one item at a time).
- **F2 Prohibited actions**: multi-item execution; skipping ahead; delegating across phase boundaries; **skipping phase-gate QA** (must spawn rf-qa after Phase 2+); **skipping post-completion validation** (rf-qa structural + rf-qa-qualitative operational).
- **F2a Item Execution Discipline**: explicit definition of multi-item execution violations + parallel-spawning exception when consecutive items spawn INDEPENDENT subagents in the SAME phase.
- **F3 Universal requirements**: every item required; exact sequential order; every checkbox marked [x].
- **F4 Modification restrictions**: workers may only check items, update frontmatter, add notes, or add to DYNAMIC CONTENT MARKER sections.
- **F5 Frontmatter update protocol**: status `🟠 Doing` + start_date on start; `🟢 Done` + completion_date on completion; `⚪ Blocked` + blocker_reason if blocked.

### G. CONTEXT FOR HEADLESS AGENTS (L453-468)

- G1: Framework context files (ib_agent_core.md, quality_gates.md, anti_hallucination_*, anti_sycophancy.md, file_conventions.md) are NOT auto-loaded into headless workers.
- G2: Reference specific rule files in items OR reference a template that already incorporates them (preferred).
- G3: Task-specific context embedded in action items, NOT in separate "context loading" steps.

### H. TOOL SPECIFICATION (L470-490)

- H1: Rely on the model to select tools by default; do NOT include tool guidance unless a SPECIFIC tool is required.
- H2-H4: When tool specification IS needed, embed it in the item (`"...use the Bash tool to run X..."` / `"...use Glob to find Y..."`).

### I. ADDITIONAL GUIDELINES (L492-647)

Most-relevant I-rules for this build:
- **I1 Explicit directive language** — "YOU MUST", "DO NOT".
- **I2 Extreme granularity** — exact file paths, not directories.
- **I8 Mandatory template usage** — "create an MDTM task" ALWAYS means use this template.
- **I9 Hallucination prevention** — DO NOT assume / hallucinate / fabricate; 100% accuracy based on source materials.
- **I11 Early status update protocol** — status → 🟠 Doing must be the FIRST action in the task (Step 1.1).
- **I12 Verification is integrated** — NO separate verification items; embed via `"ensuring..."` clause.
- **I13 Post-completion actions** — every task includes Post-Completion Actions with frontmatter update + Execution Log entry.
- **I14 Anti-hallucination integration** — reference anti-hallucination rules; require source verification for every claim.
- **I15 Phase-gate QA enforcement** (L599-607): Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint. The gate = aggregation item + QA agent spawn (rf-qa or rf-qa-qualitative) + conditional-action item (PASS proceeds, FAIL triggers fix cycle).
- **I16 QA gate verdict and fix cycles** (L609-624): Binary PASS/FAIL. Fix-cycle table:

  | Gate Type | Max Cycles | After Max |
  |---|---|---|
  | research-gate | 3 | HALT, escalate to user |
  | synthesis-gate | 2 | Unresolved → Open Questions |
  | report-validation | 3 | HALT, escalate |
  | task-integrity | 2 | Unresolved → Open Questions |
  | Any qualitative gate | 3 | HALT, escalate |

- **I17 Post-completion validation protocol** (L626-635): Before frontmatter → Done, validate (1) all `[ ]` are `[x]`, (2) all output files exist on disk (Glob), (3) blockers have resolution notes, (4) if source code modified, tests pass. Appears in `## Post-Completion Actions` BEFORE the frontmatter update item.
- **I18 Testing requirements for code-modifying tasks** (L637-646): If the task creates or modifies source code (NOT docs, NOT config), MUST include at least one testing item with: test command, pass criteria, results capture path, B2 self-contained shape. For Template 02: use L3 (Test/Execute) pattern.

### J. ERROR HANDLING GUIDANCE (L651-673)

- **J1**: Embed the standard blocker-logging clause in every item: `"If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."`
- **J2**: Items are NEVER left unchecked. Success = output exists; Failure = blocker logged. Task continues.
- **J3**: Do NOT block entire task for individual item failures. Only mark `⚪ Blocked` if ALL remaining items blocked by same issue.

### K. EXAMPLE PATTERNS (L675-708)

- **K1 File-by-File Processing**: one self-contained item per file using `#### File: [filename]` header.
- **K2 Multi-Item Processing**: orchestrator pre-enumerates ALL items; worker NEVER dynamically adds items. One item per file, no separate verification items.

---

## 3. Section L — Intra-Task Handoff Patterns (Complex-Task Specific) (L710-836)

**Handoff convention** (L718-730): items write outputs to `.dev/tasks/TASK-NAME/phase-outputs/`. Subdirs: `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`. Files persist across all batches and session rollovers.

**When to use** (L732-735): Use handoff patterns when items depend on info produced by earlier items. If every item is independent, use template 01.

### L1. Discovery item pattern (L737-747)

**When**: An item needs to explore the codebase/environment and produce structured findings for later items.
**Key rule**: The discovery file IS the deliverable. Must be well-structured, machine-readable. Use Glob + Read pattern → consolidated inventory in `phase-outputs/discovery/`.

### L2. Build-from-Discovery item pattern (L749-759)

**When**: An item creates output based on a previous discovery item's findings.
**Key rule**: Reference BOTH the discovery file AND the source files. Discovery tells WHAT to process; source provides CONTENT.

### L3. Test/Execute item pattern (L761-771)

**When**: Run a command/script/test suite and capture results.
**Key rule**: Capture BOTH raw output AND structured summary. Raw preserves detail; summary enables quick assessment by later items. Outputs land in `phase-outputs/test-results/`.

### L4. Review/QA item pattern (L773-783)

**When**: Assess quality of a previous item's output against source materials/specs/requirements.
**Key rule**: Must produce structured verdict (PASS/FAIL) with specific findings. Never vague "looks good".

### L5. Conditional-action item pattern (L785-797)

**When**: Item behavior depends on result of previous item (typically test or review).
**Key rule**: Item MUST handle BOTH branches (success AND failure). Specify exactly what to do in each case. Output file always created regardless of branch.

### L6. Aggregation item pattern (L799-809)

**When**: Consolidate multiple previous outputs into a single report. Typically final item in a phase.
**Key rule**: Use Glob to discover files dynamically — don't hardcode file lists.

### L7. Pattern selection guide (L811-836)

Common phase structures:
- **Discovery → Build → Review**: L1 → L2 (per item) → L4 (per item) → L6
- **Build → Test → Fix**: K1/K2 → L3 → L5
- **Full Lifecycle**: L1 → L2 → L3 → L5 → L4 → L6
- **Full Lifecycle with QA Gates**: L1 → L2 → **M1 (QA Gate)** → L3 → L5 → L4 → L6 → **M1 (QA Gate)**

### Parallel spawning (F2a L430)

> "When consecutive checklist items within the SAME phase spawn INDEPENDENT subagents (agents that do not read each other's outputs), the executor MAY spawn all such agents in parallel using multiple Agent tool calls in a single message. Each agent operates in isolated context. The executor MUST still mark each item individually as the corresponding agent completes. This exception does NOT apply to items that have data dependencies on each other."

### Section M — Phase-Gate Composite Patterns (L837-860)

**M1 Phase-gate QA sequence**: 2-3 items inserted between phases:
1. **Aggregation item (L6 pattern)** — collect all phase outputs into a summary/inventory file (Glob for dynamic counts).
2. **QA agent spawn item** — spawn rf-qa (structural) with appropriate phase type. Must include: agent name, phase type, input file paths, output report path, verdict handling, error clause. If qualitative QA also required, spawn rf-qa-qualitative in SEPARATE item immediately following (sequential).
3. **Conditional-proceed item (L5 pattern)** — read QA report. PASS → next phase. FAIL → fix cycle (per I16 max cycles).

**M2 Applicability** (L852-860): task-building tasks specifically need **research-gate** after research phase, **task-integrity** after task file creation.

---

## 4. PART 2 Heading Hierarchy (L890-1204)

Exact ordering (every generated task file must follow this):

```
[frontmatter YAML]
---

# [Task Title]

## Task Overview
[1-paragraph description]

## Key Objectives
[numbered list of 3+ concrete outcomes]

## Prerequisites & Dependencies

### Parent Task & Dependencies
[bullet list: Parent Task, Blocking Dependencies, This task blocks]

### Previous Stage Outputs (MANDATORY INPUTS)
[informational only, no checklist items]

### Handoff File Convention
[describes phase-outputs/ subdirs]

### Frontmatter Update Protocol
[Upon Start / Upon Completion / If Blocked / After Each Work Session]

## Execution Context        ← OPTIONAL block (DM-001 / R-033/R-034/R-035, see §10 below)
                              ← inserted between Prerequisites and Detailed Task Instructions

## Detailed Task Instructions

### Phase 1: Preparation and Setup
  Step 1.1: Update task status  ← I11: status → 🟠 Doing FIRST
    - [ ] (single self-contained item)
  Step 1.2: Create handoff directories
    - [ ] Create `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`
  Step 1.3+: [other prep items]

### Phase 2: [Main Execution]
  Step 2.1: Discovery (L1 pattern)
  Step 2.2: Build (L2 pattern)
  Step 2.3: Test (L3 pattern)
  Step 2.4: Assess (L5 pattern)
  ...

### Phase Gate: Quality Verification  ← M1 sequence (aggregation → rf-qa spawn → conditional-proceed)
  Step PG.1: [QA gate item]

### Phase [N]: Testing & Verification  ← REQUIRED if I18 applies (source code modified)
  Step N.1: [L3 test execution item]

### Phase 3: [Review and Quality Assessment]  ← optional, depends on task
  Step 3.1: Review per item (L4)
  Step 3.2: Aggregate reviews (L6)

## Post-Completion Actions    ← I17 validation items come FIRST, then frontmatter update LAST
- [ ] I17.1: Verify all outputs exist on disk (Glob)
- [ ] I17.2: Run relevant test suite (if I18 applies)
- [ ] I17.3: Create ### Task Summary in Task Log / Notes
- [ ] I17.4: Update completion_date, updated_date, status → 🟢 Done + Execution Log entry

## Task Log / Notes 📋

### Task Summary           ← filled in Post-Completion
### Execution Log
### Phase 1 - [Phase Name] Findings
### Phase 2 - [Phase Name] Findings
### Phase 3 - [Phase Name] Findings
### Phase Gate Findings
### Follow-Up Items Identified
### Deviations from Process
```

---

## 5. Canonical 5-Field Self-Contained Example (B4 L155-158, verbatim)

The 5 fields are: (1) Context Reference, (2) Action, (3) Output Specification, (4) Integrated Verification ("ensuring..."), (5) Completion gate (with the blocker-logging fallback). Quoted verbatim:

```markdown
- [ ] Read the file `component-spec.md` at `docs/specs/component-spec.md` to extract the API interface requirements including all method signatures, parameter types, and return values that must be implemented, then read the file `BaseHandler.ts` at `src/handlers/BaseHandler.ts` to understand the structural patterns and conventions used in existing handlers, then create the file `ApiHandler.ts` at `src/handlers/ApiHandler.ts` containing a TypeScript class that implements all methods defined in the component spec with proper error handling, type annotations, and JSDoc comments following the patterns from BaseHandler, ensuring the file includes the standard header comment block, exports the class as the default export, all methods from the spec are implemented with correct signatures, no content is fabricated or assumed beyond what the source explicitly states, and no placeholder or TODO comments remain. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

**Field decomposition for the rf-task-builder**:

| Field | Substring within the example |
|---|---|
| (1) Context | `Read the file [name] at [path] to extract [what]... then read [next file] at [path] to understand [what]...` |
| (2) Action | `then create the file [name] at [path] containing [description] following [patterns]` |
| (3) Output | `the file [exact name] at [exact path]` (embedded inside action) |
| (4) Verification | `ensuring [criterion 1], [criterion 2], no content is fabricated or assumed beyond what the source explicitly states, and no placeholder or TODO comments remain` |
| (5) Completion gate | `If unable to complete due to ..., log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.` |

---

## 6. Granularity Rule (per-file, per-component, NOT batch)

**A3 (L91-95, verbatim)**: "Break down EVERY workflow phase into atomic, verifiable checklist items. Create individual checklist items for EVERY file, component, or iteration. NO high-level or bulk operations allowed - everything must be granular. Include exact file paths, specific requirements, and measurable outcomes."

**K2 reinforcement (L693-697)**: "The orchestrator agent creating this task file MUST identify and enumerate ALL items that need processing during task setup. The worker agent MUST NEVER dynamically add checklist items - all items must be listed by the orchestrator before the worker begins."

**Application for this build**: If the task edits multiple SKILL.md files or multiple refs/ files, each file gets ONE dedicated self-contained item (using K1 `#### File: [filename]` header). Batch items like "edit all SKILL.md files for sub-skills" are FORBIDDEN.

---

## 7. Anti-Orphaning Rule

**C4 (L225-230)** + **I13 (L580-585)**: Task completion items live in the `## Post-Completion Actions` section. Crucially per **I17 (L626-635)**:

> "These items appear in the ## Post-Completion Actions section of PART 2, BEFORE the frontmatter update item."

And **I13** explicitly forbids: "Do NOT create a separate 'Task Completion and Handoff Protocol' section in the task body."

**Implication for this build**: The post-completion validation items (Glob output-existence check, test re-run, Task Summary creation) MUST be inside `## Post-Completion Actions`, NOT inside a separate trailing phase like `### Phase N+1: Cleanup`. The frontmatter-update item (status → 🟢 Done, completion_date) is the LAST item, after the validation items.

**Note on terminology**: Post-Completion Actions sits below the last phase and IS executed last; this is the canonical placement per template L1118-1126 — not a violation of E3's "no backward movement" rule (the agent moves forward into Post-Completion after the last phase).

---

## 8. QA Gate Item Shape

Per **I15 (L600-607)** + **M1 (L843-850)**, a QA gate consists of **2-3 items**:

### Item 1 — Aggregation (L6 pattern, optional if phase has 1-2 fixed outputs)

```markdown
- [ ] Use Glob to find all output files matching `.dev/tasks/TASK-NAME/phase-outputs/<phase-subdir>/*.{md,txt}` to discover all files produced by Phase [N], then read each file to extract [key fields], then create a consolidated inventory file `phase[N]-inventory.md` at `.dev/tasks/TASK-NAME/phase-outputs/reports/phase[N]-inventory.md` listing each output file with its path, line count, and a 1-line summary of its content, ensuring all files matching the pattern are included with accurate metadata extracted from actual file contents. If no files match the pattern (Phase [N] produced no outputs), log this as a blocker in ### Phase Gate Findings, then mark this item complete. Once done, mark this item as complete.
```

### Item 2 — rf-qa spawn (the QA agent invocation)

The TASK-RF-20260527-043715 prior example uses this exact shape (see canonical example in §9 below). Required elements per I15:
1. Agent to spawn (`rf-qa` for structural, `rf-qa-qualitative` for operational/behavioral content).
2. Phase type (`research-gate` | `synthesis-gate` | `report-validation` | `task-integrity` | etc).
3. Input file paths (exact, absolute or repo-relative).
4. Output report path under `.dev/tasks/TASK-NAME/phase-outputs/reviews/<phase>-<gate>.md`.
5. Verdict handling (PASS → proceed; FAIL → fix cycle with max cycles per I16).
6. Error / blocker clause.

Per user memory `feedback_rfqa_adversarial_pattern.md`: pair explicit `"ADVERSARIAL STANCE."` framing with `fix_authorization: true` whenever spawning rf-qa / rf-qa-qualitative for MDTM gates.

### Item 3 — Conditional proceed (L5 pattern)

```markdown
- [ ] Read the QA report at `.dev/tasks/TASK-NAME/phase-outputs/reviews/phase[N]-rf-qa-<gate>.md` to determine the verdict, then: IF verdict is PASS, create a verdict file `phase[N]-gate-verdict.md` at `.dev/tasks/TASK-NAME/phase-outputs/plans/phase[N]-gate-verdict.md` containing a single-line confirmation "Phase [N] QA gate PASS — proceeding to Phase [N+1]"; IF verdict is FAIL, read the report findings, address each finding by re-editing the relevant Phase [N] output files in place, then re-spawn rf-qa in fix-cycle mode (max 2 cycles per I16; on cycle-3 failure remaining issues become Open Questions). Ensure the verdict file accurately reflects the report. If unable to complete due to missing report, log the blocker in ### Phase Gate Findings, then mark this item complete. Once done, mark this item as complete.
```

---

## 9. Prior Task Examples (sync-dev + SKILL.md edits)

Both prior examples below are strong matches for this build (edits to `src/superclaude/skills/*/SKILL.md` + `make sync-dev` + `make verify-sync` gating).

### Example A: TASK-RF-20260527-043715-sc-reflect-rebuild

**Path**: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260527-043715-sc-reflect-rebuild/TASK-RF-20260527-043715-sc-reflect-rebuild.md`

**What it did**: Built the entire sc-reflect-protocol skill from scratch — 13-file skill package at `src/superclaude/skills/sc-reflect-protocol/` (SKILL.md ~800-1500L + 11 refs) + 10-file eval workspace + 2 runtime files + command rewrite at `src/superclaude/commands/reflect.md` + 3 new Makefile targets. 25 CREATE + 2 MODIFY.

**Phase structure (7 phases)**:
1. **Phase 1**: Preparation, Frozen Baseline, and Skill Package Scaffolding
2. **Phase 2**: SKILL.md Body Authoring (Incremental — 4 Edit Passes)
3. **Phase 3**: Refs Authoring (11 Refs — One Item per Ref) ← perfect K1/K2 application
4. **Phase 4**: Command Rewrite + Bidirectional Skill Link (ends with rf-qa task-integrity gate)
5. **Phase 5**: Eval Workspace Setup
6. **Phase 6**: Sync & Makefile Targets ← **the sync-dev phase**
7. **Phase 7**: Final QA, Eval-Quick Smoke, and Task Completion

**How it handled sync-dev** (Phase 6 Steps 6.4-6.6, lines 424-434):
- **Step 6.4**: `make sync-dev 2>&1 | tee phase-outputs/test-results/phase6-sync-dev.txt` — CRITICAL warning embedded: "DO NOT manually edit any `.claude/{skills,commands,agents,hooks,templates}/` paths. The `make sync-dev` target IS the only authorized way to populate `.claude/`."
- **Step 6.5**: `make verify-sync` — "MUST exit EXACTLY 0; this is non-negotiable; a non-zero exit indicates the sync is broken and downstream lint-architecture will also fail." Max 2 re-run cycles before HALT.
- **Step 6.6**: `make lint` (ruff over `src/superclaude/`) — max 3 re-runs.
- **Step 7.1**: `make lint-architecture` **again** post-sync to confirm bidirectional link still works after `.claude/` was repopulated.
- **Step 7.late**: `git status --short` + Grep check that NO line matches `^[AM]  \.claude/(skills|commands|agents|hooks|templates)/` (the CLAUDE.md ABSOLUTE rule guard).

**Total items**: 73 across 7 phases.

**What worked**:
- Phase 1 Step 1.3 captured a **baseline `make verify-sync` exit-0 check** BEFORE any edits — caught pre-existing drift that would have polluted later parity checks. Worth borrowing.
- Refs authoring as one item per ref (Phase 3) is textbook K2 application.
- Phase 6 separates `sync-dev` → `verify-sync` → `lint` into 3 distinct items, each with its own max-retry policy.
- Post-sync `git status` grep is a defense-in-depth guard against the `.claude/` staging rule.

**What was awkward**:
- 73 items is heavy; required multiple session rollovers. The "rf-qa task-integrity gate" after Phase 4 caught 3 pre-existing `make lint-architecture` failures unrelated to the task, requiring operator authorization for scope expansion (logged as deviation).
- Step 4.3 had to re-run `lint-architecture` 4 times before the operator-authorized in-scope fixes resolved it.

### Example B: TASK-RF-20260520-230051 (PR #64 auggie-review fix)

**Path**: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260520-230051/TASK-RF-20260520-230051.md`

**What it did**: 3 surgical edits across `src/superclaude/hooks/scripts/offer-pr-review.sh`, `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` (L163-170 pipeline consolidation), `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` (populate 3 empty `assertions: []` arrays). All verbatim before/after text supplied by research.

**Phase structure (5 phases)**:
1. **Phase 1**: Preparation and Setup
2. **Phase 2**: Fix 1 (M2) — offer-pr-review.sh prefilter
3. **Phase 3**: Fix 2 (M1) — SKILL.md pipeline consolidation
4. **Phase 4**: Fix 3 (M4) — evals.json assertions populated
5. **Phase 5**: Sync, Validate, and Final QA Gate ← consolidates all sync-dev work
   - Step 5.1: `make sync-dev` capturing output
   - Step 5.2: `make verify-sync` as **sole src/↔.claude/ parity gate** (with conditional verdict file at `phase-outputs/plans/verify-sync-verdict.md` — L5 pattern!)
   - Step 5.3-5.4: `make lint` + `make lint-architecture`
   - Phase Gate: FINAL_ONLY rf-qa gate after all 4 fix phases

**Total items**: 21 across 5 phases.

**How it handled sync-dev**: One consolidated Phase 5 instead of inline sync-dev per phase. The verify-sync item uses an L5 conditional pattern to emit either a `VERIFY-SYNC: PASS` or `VERIFY-SYNC: FAIL` verdict file — clean and auditable.

**What worked**:
- L5 conditional verdict file for verify-sync is a clever way to capture state for downstream items.
- Per-file integrity gates BEFORE sync-dev (`bash -n` for shell scripts, `markdownlint` for SKILL.md, `jq .` for JSON) caught syntax errors before they propagated to `.claude/`.
- Explicit Risks section called out the `--no-verify` prohibition.
- Commit/push explicitly OUT OF SCOPE — task hands off to operator.

**What was awkward**:
- Only 1 phase-gate QA at the very end (FINAL_ONLY) — for small surgical edits like this it worked, but for larger builds the I15 rule favors per-phase gates.

### Examples summary

| Aspect | Example A (sc-reflect-rebuild) | Example B (PR #64 fix) |
|---|---|---|
| Items | 73 | 21 |
| Phases | 7 | 5 |
| SKILL.md edits | NEW skill (~800-1500L body + 11 refs) | Surgical L163-170 rewrite |
| `make sync-dev` placement | Phase 6 dedicated, post-content | Phase 5 dedicated, post-all-fixes |
| `make verify-sync` retries | Max 2, then HALT | Logged-only on fail (verdict file) |
| QA gates | Per-phase rf-qa (Phases 2-7) | Single FINAL_ONLY gate |
| Post-completion validation | Yes (I17 compliance) | Yes (I17 compliance) |
| Anti-`.claude/`-staging guard | Yes (Phase 7 git status grep) | Yes (Risks section + Phase 5 verify-sync) |

**Recommendation for this build**: Hybrid — borrow Example A's baseline `verify-sync` exit-0 check (Phase 1 prep) and its dedicated Phase-6-style sync block; borrow Example B's consolidated single Phase-5 sync (if total edits are small) and its L5 conditional verdict file pattern; emit per-phase rf-qa gates if the task crosses 25+ items.

---

## 10. Execution Context Block (DM-001 / R-033/R-034/R-035)

### Confirmation: BUILD_REQUEST exposes ≥3 source areas

This build's BUILD_REQUEST exposes (at minimum):
1. **SKILL.md(s)** — `src/superclaude/skills/task-builder/SKILL.md` (and possibly sub-skills depending on scope)
2. **refs/** directory(ies) — `src/superclaude/skills/task-builder/refs/*.md`
3. **Makefile** — `Makefile` (sync-dev / verify-sync / lint targets)
4. **Brainstorm spec** — likely at `.dev/brainstorms/<topic>/merged-output.md` or `merged-requirements.md`

→ **YES, ≥3 source areas**, so an `## Execution Context` block SHOULD be emitted between `## Prerequisites & Dependencies` and `## Detailed Task Instructions`.

### R-033 / R-034 / R-035 emitter rules

Confirmed by reading prior example TASK-RF-20260527-043715 which contains an `## Execution Context` block (line 105) and TASK-RF-20260520-230051 (line 118):

- **R-033 — References labels**: Use `**References:**` as the label heading.
- **R-034 — Source areas labels**: Use `**Source areas:**` as the label heading, listing high-level directories/groupings (e.g., `src/superclaude/skills/task-builder/`, `Makefile`, `.dev/brainstorms/<topic>/`).
- **R-035 — Key constraints labels**: Use `**Key constraints:**` for the bullet list of project rules in play (sync-dev parity, no-`.claude/`-staging rule, UV-only Python, etc).

### Critical emitter discipline

**The Source areas bullet MUST NOT contain `file:line` paths.** Per the BUILD_REQUEST guidance: per-item `file:line` citations belong in each checklist item's Context field (e.g., `"Read Makefile at /path/Makefile lines 109-163..."`), NOT in the Execution Context block's Source areas summary.

**Source areas** should list **directory/area-level** entries:
```
- `src/superclaude/skills/task-builder/` — task-builder skill package (SKILL.md + refs/)
- `src/superclaude/skills/task-builder/refs/` — supporting reference docs
- `Makefile` — sync-dev / verify-sync targets used by validation gates
- `.dev/brainstorms/<topic>/merged-output.md` — the spec driving this build
```

NOT:
```
- `Makefile:109-163` — the sync-dev target  ❌ WRONG (file:line in Source areas)
```

The `Makefile:109-163` citation belongs in the specific Phase 6 sync-dev item's Context field.

---

## 11. Cross-cutting recommendations for the task-builder

1. **Frontmatter `template_schema_doc`**: must be `".claude/templates/workflow/02_mdtm_template_complex_task.md"` — confirmed across all prior examples.
2. **Phase 1 Step 1.1**: I11 mandates status → 🟠 Doing as the FIRST checklist item.
3. **Phase 1 Step 1.2**: Create `.dev/tasks/TASK-RF-20260529-160318/phase-outputs/{discovery,test-results,reviews,plans,reports}/` (template L1050, lifted directly).
4. **Phase 1 prep — baseline verify-sync** (borrowed from Example A): one item that runs `make verify-sync` BEFORE any edits to capture pre-existing drift baseline. If exit non-zero, log blocker AND prompt for operator decision.
5. **Per-phase rf-qa gates** (if >20 items): insert M1 sequence at every phase boundary that produces inputs for the next phase.
6. **Final phase = Sync & Validate** (borrowed from both examples):
   - `make sync-dev` (captures output to test-results/)
   - `make verify-sync` (MUST exit 0; max 2 retries; with L5 conditional verdict file)
   - `make lint` (if any `.py` modified)
   - `make lint-architecture` (if any SKILL.md modified)
   - `git status --short` + Grep guard that no `^[AM]  \.claude/(skills|commands|agents|hooks|templates)/` line matches (the CLAUDE.md ABSOLUTE rule)
7. **Post-Completion Actions** (I17): output existence check (Glob), test re-run (if I18 applies), Task Summary creation, frontmatter update → 🟢 Done.
8. **Standard blocker-logging clause** appended to every item per J1.
9. **Tags**: include at minimum `["task-builder", "skill-edit", "sync-dev", "mdtm"]` plus topic-specific tags.
10. **assigned_to**: `"rf-task-executor"` per prior convention.

---

## Status

**Status: Complete**

All sections (1-11) populated. Template lines cited for every rule. Prior examples sourced and characterized. Execution Context guidance derived from R-033/R-034/R-035 emitter discipline and confirmed against the live example in TASK-RF-20260527-043715.
