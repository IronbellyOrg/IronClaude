# Research: Template & Examples
**Topic type:** Template & Examples
**Scope:** MDTM template 02, existing .dev/tasks/* examples
**Status:** Complete
**Date:** 2026-05-17
---

## 1. Template 02 PART 1 — Rule Inventory

**File:** `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1197 lines; PART 1 ends at line 870, PART 2 begins at line 896).

### Section A — Core Principles

| Rule | Title |
|------|-------|
| A1 | WORKFLOW DOCUMENT AVAILABILITY CHECK |
| A2 | WORKFLOW DOCUMENT DEEP INTEGRATION [WORKFLOW-DEPENDENT] |
| A3 | COMPLETE GRANULAR BREAKDOWN |
| A4 | ITERATIVE PROCESS STRUCTURE |
| A5 | CROSS-STAGE INTEGRATION [WORKFLOW-DEPENDENT] |
| A6 | WORKFLOW COMPLIANCE ENFORCEMENT [WORKFLOW-DEPENDENT] |

**A3 — verbatim quote (lines 91-95):**
> "COMPLETE GRANULAR BREAKDOWN
> - Break down EVERY workflow phase into atomic, verifiable checklist items
> - Create individual checklist items for EVERY file, component, or iteration
> - NO high-level or bulk operations allowed - everything must be granular
> - Include exact file paths, specific requirements, and measurable outcomes"

**A4 — verbatim quote (lines 97-116):**
> "ITERATIVE PROCESS STRUCTURE
> - For ANY process involving multiple items (files, components, etc.):
>   * Pre-enumerate ALL items to be processed in initial step
>   * Create individual checklist item for each specific item
>   * Require incremental updates after each item
>   * Include consolidation step only after all items complete"
>
> Use this pattern:
> ```
> **Step X.1:** Scan and enumerate all [items] in [location]
> - [ ] Complete [item] listing generated: [count] items identified
> **Step X.2:** Process each [item] individually:
> - [ ] [Item 1]: [exact identifier] - [specific action] completed
> ...
> **Step X.3:** Consolidate all individual results
> ```

### Section B — Self-Contained Checklist Items (CRITICAL)

| Rule | Title |
|------|-------|
| B1 | WHY THIS MATTERS (SESSION ROLLOVER PROTECTION) |
| B2 | EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT (6-element pattern) |
| B3 | THE SELF-CONTAINED PATTERN (one paragraph, verbose) |
| B4 | CORRECT EXAMPLE — self-contained item with integrated verification |
| B5 | FORBIDDEN PATTERNS (standalone "read context", missing references, multi-line bullets, separate verification items) |
| B6 | PREFERENTIAL (context references / output specs when applicable) |
| B7 | KEY PRINCIPLES (complete prompt; embedded verification; output IS evidence) |

**B2 — verbatim 6-element pattern (lines 142-148):**
> "EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT THAT INCLUDES:
> 1. **Context Reference with WHY** - What file(s) to read and why that context is needed for this specific action
> 2. **Action with WHY** - What to do with that context and why it needs to be done
> 3. **Output Specification** - The exact output file name, location, what content to produce, and template to follow (if applicable)
> 4. **Integrated Verification** - An 'ensuring...' clause that specifies what must be verified (DO NOT assume, hallucinate, or make up any information - all content MUST be derived from source files referenced in the checklist item, 100% accuracy based on source materials, document negative evidence when verification fails)
> 5. **Evidence on Failure Only** - Log to task notes ONLY if unable to complete due to blockers, missing info, or errors (successful completion is evidenced by the output file itself)
> 6. **Explicit Completion Gate** - 'This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.'"

### Section C — Embedding Requirements
- C1 Outputs & Deliverables (embed in items, no separate section)
- C2 Success Criteria (embed as "ensuring..." clause)
- C3 Verification (embed in action items, NO separate verification items)
- C4 Task Completion (only Post-Completion Actions; no separate Handoff Protocol section)

### Section D — Mandatory Task Sections
- D1 Workflow Compliance Declaration [WORKFLOW-DEPENDENT]
- D2 Cross-Stage Integration Requirements [WORKFLOW-DEPENDENT]
- D3 CRITICAL RULE: NO CHECKLIST ITEMS BEFORE PHASE 1 BEGINS

### Section E — Checklist Structure Rules
- E1 Checkbox format (flat, no nesting, no parent checkboxes summarizing children)
- E2 CRITICAL: Summary/parent checkboxes MUST come AFTER component items
- E3 Sequential order (top to bottom only)
- E4 Checkbox formatting (no checkboxes on step numbers; no REMINDER blocks)

### Section F — Execution Requirements (Worker Agents)
- F1 Five-step execution pattern: READ -> IDENTIFY -> EXECUTE -> UPDATE -> REPEAT
- F2 Prohibited actions (multi-item execution, skipping QA gates, skipping post-completion validation)
- F2a Item Execution Discipline (one-item-at-a-time within session) + parallel-spawning exception
- F3 Universal requirements (every item REQUIRED, no optional)
- F4 Task file modification restrictions
- F5 Frontmatter update protocol

### Section G — Context for Headless Agents
- G1 Framework context files NOT auto-loaded for headless agents
- G2 Either reference rule file OR template that incorporates conventions
- G3 Task-specific context embedded directly in action items
- G4 Previous stage outputs format

### Section H — Tool Specification
- H1 Default: rely on model selection
- H2 ONLY specify tools when a specific tool is required
- H3 Embed tool guidance inside the checklist item
- H4 Tool selection matrix

### Section I — Additional Guidelines
- I1 Use explicit directive language ("YOU MUST", "DO NOT")
- I2 Extreme granularity required
- I3 Incremental file modification
- I4 Parent task relationships
- I5 All requirements absolute
- I6 Dynamic content handling
- I7 Explicit template usage
- I8 Mandatory template usage
- I9 Hallucination prevention system
- I10 Critical workflow compliance reinforcement
- I11 Early status update protocol (status update is FIRST action)
- I12 Verification is integrated (no separate verification items)
- I13 Post-completion actions (final items only)
- I14 Anti-hallucination controls integration
- **I15 PHASE-GATE QA ENFORCEMENT** — "Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint between the primary execution phase and any subsequent phase that depends on its outputs."
- **I16 QA GATE VERDICT AND FIX CYCLES** — Binary PASS/FAIL; any severity -> FAIL. Fix cycle table by gate type (research-gate=3, synthesis-gate=2, report-validation=3, task-integrity=2, qualitative=3).
- **I17 POST-COMPLETION VALIDATION PROTOCOL** — Before Done: (1) all items `[x]`, (2) all output files exist (Glob), (3) blockers have resolution notes, (4) tests pass if source modified.
- **I18 TESTING REQUIREMENTS FOR CODE-MODIFYING TASKS** — If source code modified: at least one testing item with test command, pass criteria, results capture path, B2 pattern. Use L3 for Template 02.

### Section J — Error Handling
- J1 Pattern: "log specific blocker using templated format in ### Phase [N] Findings, then mark item complete"
- J2 Items NEVER left unchecked; success = output file exists
- J3 Do NOT block task for individual item failures

### Section K — Example Patterns
- K1 File-by-file processing pattern
- K2 Multi-item processing pattern (orchestrator pre-enumerates ALL items)

### Section L — Intra-Task Handoff Patterns

**File convention (lines 718-727):** `.dev/tasks/TASK-NAME/phase-outputs/` with subdirs `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`.

**L1 DISCOVERY ITEM** — discovery file IS the deliverable; later items read it directly.
**L2 BUILD-FROM-DISCOVERY ITEM** — reads BOTH discovery file AND original source files.
**L3 TEST/EXECUTE ITEM** — captures BOTH raw output AND structured summary.
**L4 REVIEW/QA ITEM** — structured PASS/FAIL verdict with specific findings.
**L5 CONDITIONAL-ACTION ITEM** — handles BOTH branches; output file always created.
**L6 AGGREGATION ITEM** — Glob to discover files dynamically; consolidate.
**L7 PATTERN SELECTION GUIDE** — table maps "Task Need" -> pattern; common phase structures.

### Section M — Phase-Gate Composite Patterns
- M1 PHASE-GATE QA SEQUENCE: 2-3 items — L6 aggregate -> QA spawn (rf-qa, optionally rf-qa-qualitative sequentially) -> L5 conditional proceed
- M2 PHASE-GATE APPLICABILITY: code-modifying tasks -> "after implementation phase and before testing phase (if testing is separate), or after combined implement+test phase"

---

## 2. Template 02 PART 2 — Section Structure

PART 2 begins at line 896 with `# [Task Title]`.

### YAML Frontmatter (lines 1-44) — required fields:
- `id`, `title`, `description`, `status`, `type`, `priority`
- `created_date`, `updated_date`, `assigned_to`, `coordinator`
- `parent_task`, `depends_on[]`, `related_docs[]` (each with `path` + `description`)
- `tags[]`, `task_type` (static/dynamic)
- Lifecycle: `start_date`, `completion_date`, `blocker_reason`, `due_date`, `sprint`
- Plus auto-managed: `autogen`, `autogen_method`, `template_schema_doc`, `estimation`, `ai_model`, `model_settings`, `review_info`

### Mandatory Sections (in order):
1. `# [Task Title]`
2. `## Task Overview`
3. `## Key Objectives` — numbered, "MUST be achieved by this task"
4. `## Prerequisites & Dependencies` with subsections:
   - `### Parent Task & Dependencies` (Parent Task, Blocking Dependencies, This task blocks)
   - `### Previous Stage Outputs (MANDATORY INPUTS)` — INFORMATIONAL ONLY
   - `### Handoff File Convention` — lists `phase-outputs/` subdirs
   - `### Frontmatter Update Protocol`
5. `## Detailed Task Instructions`
   - `### Phase 1: Preparation and Setup` (status update FIRST, handoff dirs SECOND)
   - `### Phase 2: [Main Execution]` (uses L1-L6 patterns)
   - `### Phase Gate: Quality Verification` (optional — M1 sequence when needed)
   - `### Phase N: Testing & Verification` (required for code-modifying — I18)
   - `### Phase 3: [Review/Aggregate]` (optional)
6. `## Post-Completion Actions` — I17 validation items + frontmatter update
7. `## Task Log / Notes 📋` with subsections:
   - `### Task Summary` (filled in Post-Completion)
   - `### Execution Log`
   - `### Phase [N] - [Name] Findings` (one per phase)
   - `### Phase Gate Findings`
   - `### Follow-Up Items Identified`
   - `### Deviations from Process`

### Optional sections (when applicable)
- D1 Workflow Compliance Declaration (only if governing workflow exists)
- D2 Cross-Stage Integration Requirements (only if workflow-dependent)
- `### Task-Specific Context Files` (informational reference list)
- Execution Context — emit when task touches multi-component or fragile paths

---

## 3. Nearest-Match Example: TASK-RF-track-2-20260517-032112

**Path:** `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-2-20260517-032112/TASK-RF-track-2-20260517-032112.md` (239 lines).

**Why nearest match for this task:**
- Modifies many files mechanically (ruff format)
- Includes `make verify-sync` and `make sync-dev` smoke checks
- Multi-phase gated workflow (Prep -> Execute -> Verify -> Commit)
- Captures shell command output to `phase-outputs/test-results/*.txt` with `EXIT=$?` pattern
- Uses PASS/FAIL verdict files in `phase-outputs/plans/*.md`

### Phase structure (4 phases + Post-Completion):
1. **Phase 1: Preparation and Setup** — 5 steps:
   - 1.1 Status update (frontmatter + Execution Log entry)
   - 1.2 Create handoff directories via `mkdir -p`
   - 1.3 HALT GATE: verify PR dependency merged (gh CLI capture)
   - 1.4 Sync local master + cut branch
   - 1.5 Install dev deps + verify tools available
2. **Phase 2: Execute** — 1 step:
   - 2.1 Apply mechanical change + capture output
3. **Phase 3: Verify** — 4 verification steps:
   - 3.1 AC2 check (ruff format --check) -> PASS/FAIL verdict file
   - 3.2 AC1 preserved (ruff check) -> PASS/FAIL verdict file
   - 3.3 Full pytest run -> PASS/FAIL verdict
   - 3.4 `make verify-sync` clean -> PASS/FAIL verdict
4. **Phase 4: Commit and Open PR** — 2 steps (stage+commit, push+PR)
5. **Post-Completion Actions** — 4 items (output verification via ls, test re-verification reference, Task Summary, frontmatter Done update)

**Total checklist items: ~16** (excluding Post-Completion).

### Patterns relevant to this task

**Output-capture-with-exit pattern (verbatim from Step 3.1):**
> "Run the CI-equivalent format check by executing `uv run ruff format --check src/ tests/` from `/config/workspace/IronClaude` and capture both the stdout/stderr and the exit code to `[path]` (use the pattern `uv run ruff format --check src/ tests/ > path 2>&1; echo \"EXIT=$?\" >> path`). Then read the capture file and confirm the line `EXIT=0` is present. IF exit code is 0, write a PASS verdict to `[plans/...-verdict.md]`. IF non-zero, write a FAIL verdict ... STOP."

**HALT-GATE pattern (Step 1.3):** branch-and-stop logic embedded inside a single self-contained item — writes either `VERDICT: HALT` or `VERDICT: PASS`, updates frontmatter to Blocked on HALT.

**verify-sync smoke-test pattern (Step 3.4):** capture exit code; if FAIL, instructions inside the same item tell agent to `make sync-dev` then re-check (fix-cycle embedded).

---

## 4. Second Example: TASK-RF-track-3-20260517-032112 (manual file edits)

**Path:** `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-3-20260517-032112/TASK-RF-track-3-20260517-032112.md` (320 lines).

**Relevance:** Demonstrates how to structure tasks that need MANY targeted file edits (47 files, 79 renames) — uses **dynamic Phase 3 expansion** (`Step 3.TEMPLATE` per-file batch). Phase Gate PG-2 verifies the inventory before Execute begins.

### Phase structure (5 phases + Post-Completion):
1. Phase 1 Prep (status, dirs, PR2-merged check, branch, dev env)
2. Phase 2 Discovery (raw inventory + triage table with NFR4 escalation gate)
3. **Phase Gate PG-2: Inventory Quality Verification** (M1 pattern — single PASS/FAIL verdict file in `reviews/`)
4. Phase 3 Execute (dynamic per-file expansion via Step 3.TEMPLATE + Step 3.AGGREGATE)
5. Phase 4 Final Verification (4 steps: ruff scoped, full pytest, verify-sync, **PG-4 Final Verdict**)
6. Phase 5 Commit & PR (2 steps)

### Useful patterns for our task
- **PG-4 final verdict pattern (Step 4.4):** read all 3 test-result captures + reports -> write `pg4-final-verdict.md` with 4-criterion checklist; only proceed to Phase 5 if all PASS.
- **Test-result capture with PIPESTATUS:** Step 4.2 uses `make verify-sync 2>&1 | tee path; echo "EXIT=${PIPESTATUS[0]}" >> path` — preserves exit code through tee.

---

## 5. Patterns and Pitfalls Observed in Examples

### Effective patterns (REUSE)
- **Per-step verdict file** in `plans/` with `VERDICT: PASS` or `VERDICT: FAIL - [reason]` — enables downstream items to read a single line to branch.
- **`EXIT=$?` capture inside the same output file** as stdout/stderr (or `PIPESTATUS[0]` when piping through tee) — makes exit code part of the audit trail.
- **`make verify-sync` as a recurring smoke gate** after every step that touches `src/superclaude/` or `.claude/` mirrored files. When it fails, embedded fallback "run `make sync-dev` then re-check" inside the item itself.
- **Embedded HALT-GATE logic** for dependency checks (Phase 1) avoids burning batches when a prerequisite isn't met.
- **Status update is ALWAYS Step 1.1** (per I11) before anything else.
- **Handoff dir creation is ALWAYS Step 1.2** with `mkdir -p .dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}`.
- **PG (Phase Gate) numbered separately** from sequential phases (e.g., `PG-2.1`, `PG-4.1`) so the orchestrator can identify gates at a glance.
- **Post-Completion Action #1 is always Glob-verify all expected output files exist** — directly implements I17(2).

### Pitfalls / common deviations (AVOID)
- **`git add -A` over-staging:** track-2 noted deviation — staged auto-generated jsonl. Use scoped `git add 'src/**/*.py'` or `git add Makefile src/superclaude/hooks/...` patterns.
- **Strict STOP semantics:** Both track-2 and track-3 had legitimate cases where the spec said "STOP" but the agent investigated + fixed instead. Spec items SHOULD include an explicit fix-cycle clause rather than bare STOP when the failure is recoverable.
- **Per-item test invocations expensive:** track-3 skipped per-file pytest (NFR2 deviation) for cost reasons. For a small set of changes, prefer a single Phase 4 full pytest over per-step pytest unless isolation is essential.
- **Spec ambiguity around "empty working tree":** track-2 found that hooks/auto-loggers leave incidental untracked files. Items checking `git status --short` should accept incidental untracked artifacts explicitly.
- **In-line literal `<br>`-separated heredocs** (seen in track-2 Step 4.1 commit body) are a markdown-rendering artifact — when authoring new items, ensure real newlines inside heredoc blocks rather than `<br>` tokens.

### How prior tasks specified Makefile changes
- **Neither track-2 nor track-3 actually patched the Makefile** — they only EXECUTED `make` targets. For our task (which ADDS Makefile sections), there is **no direct precedent in `.dev/tasks/done/`** for Makefile patches.
- **Implication for granularity:** The closest analog is track-3's per-file Edit pattern. Each Makefile section addition should be its own item with: (a) read the spec section that defines the target, (b) read Makefile to locate insertion point, (c) Edit to add the section, (d) run `make <new-target>` to smoke-test it exists, (e) capture output to `test-results/`.

### How prior tasks specified pytest file creation
- **No prior task in `.dev/tasks/done/` creates a brand-new pytest file** (track-4 modifies an existing test fixture; others only run pytest). For our task's new `tests/hooks/test_hooks_sync.py` (or similar), the orchestrator should:
  - Either **inline the full file content** inside one large self-contained item (B2 pattern is verbose-paragraph; multi-hundred-line code blocks ARE permissible if they are the action's output)
  - Or **scaffold via discovery+build pattern** (L1 = read spec §[test-file-section] for the V1-V7 scenarios; L2 = create the file with all 7 test functions), with the spec section serving as the discovery deliverable.

---

## 6. Recommended Phase/Item Structure for THIS Task

Based on spec §10's 6-phase outline and the track-2/track-3 patterns:

### Recommended phase count: **7 phases** (Prep + 6 execution + Post-Completion)

The spec §10 6-phase outline maps to execution phases 2-7. Plus the mandatory Phase 1 Prep.

| Phase | Name | # Items | Patterns |
|-------|------|---------|----------|
| 1 | Preparation and Setup | 5 | status, dirs, branch, dev env, dependency check |
| 2 | Part 2 Patches (shell + JSON files in `src/superclaude/hooks/scripts/`) | 4-6 | one item per file patched; per-item smoke test where applicable |
| 2.5 (Gate) | Run `make sync-dev` to propagate; then `make verify-sync` | 1-2 | PASS/FAIL verdict in `plans/` |
| 3 | Part 1 — Makefile section additions | 4-7 | **one item per Makefile section** (per A3 granularity); each item embeds: read spec §, read Makefile, Edit, run `make <target>` smoke, capture output |
| 3.5 (Gate) | After all Makefile sections, run `make verify-sync` full sweep | 1 | PASS/FAIL verdict |
| 4 | Part 3 — Cross-consistency patches | 2-4 | per-file edits with smoke test |
| 5 | Create new pytest harness `tests/hooks/test_hooks_sync.py` (V1-V7) | 1-2 | one big self-contained item with V1-V7 enumerated inside the action paragraph, OR L1+L2 split if scenarios are spec-derived |
| 6 | Test execution — run new pytest + full pytest | 2 | L3 pattern: targeted run on new file, then full suite; each captures to `test-results/`; PASS/FAIL verdict file |
| 6.5 (Gate) | Orphan-decision item (per spec §10) | 1 | L5 conditional: read test verdicts, decide whether to fix vs xfail orphans |
| 7 (Final QA) | M1 sequence: aggregate -> rf-qa structural spawn -> conditional proceed | 2-3 | matches M1 pattern; gates Post-Completion |
| Post-Completion | I17 validation + Task Summary + frontmatter Done | 4 | Glob-verify outputs, test-results reference, Task Summary, status=Done |

### Total estimated item count: **27-37 checklist items**

### Granularity decisions (per A3)
- **Each Makefile section = one item.** Do NOT bundle "add all sections" into one item; the diff is too large to verify atomically and per-section smoke tests catch errors earlier.
- **Each shell-script patch = one item.** Each JSON patch = one item. Both follow track-3's per-file pattern.
- **New pytest file creation = one big item** with V1-V7 enumerated INSIDE the action paragraph as numbered scenarios. (Splitting V1-V7 into 7 items would over-fragment a single Write operation.) If the spec encodes V1-V7 with substantial detail, split into L1 (read spec, write scenario inventory to `discovery/test-scenarios.md`) + L2 (create file using inventory).
- **Per-phase smoke tests as their own items** (not appended to the edit item) — this gives Phase Gates clear PASS/FAIL artifacts and matches track-2 Phase 3 pattern.
- **`make sync-dev` after Part 2 patches** is mandatory because hooks/scripts/ is mirrored to `.claude/scripts/` (per the project's sync rule). This is its own item.
- **Final QA Gate** uses M1 sequence with rf-qa (structural). Qualitative QA likely not needed for a hook/Makefile patch (no document content to assess).

### Specific anti-patterns to AVOID for this task
- Do NOT create a "verify Makefile diff" separate item — integrate the "ensuring..." verification clause into the Edit item itself (per C3/I12).
- Do NOT skip the `make verify-sync` checkpoint after Part 2 patches — the sync gate is the SINGLE most likely thing to break for hooks/scripts edits.
- Do NOT create a single mega-item that bundles "patch all 3 parts" — violates A3 granularity, makes session-rollover recovery impossible.
- Do NOT use bare STOP on smoke-test FAIL — include fix-cycle fallback inside the item (e.g., "IF verify-sync FAIL, run `make sync-dev` and re-check; if still FAIL after one retry, log blocker and HALT").

---

## Summary

**Findings:**
- Template 02 PART 1 has 13 sections (A-M); A3 (granularity) + B2 (6-element self-contained items) + L1-L7 (handoff patterns) + I15-I18 (gates + testing) are the load-bearing rules for this task.
- PART 2 is the actual task-file scaffold beginning at line 896; YAML frontmatter + 7 mandatory sections.
- **TASK-RF-track-2-20260517-032112** is the nearest-match example — 4-phase mechanical-change task with PASS/FAIL verdict files in `plans/` and `make verify-sync` as a smoke gate.
- **TASK-RF-track-3-20260517-032112** shows the per-file Edit pattern, dynamic Phase 3 expansion, and the PG-2/PG-4 phase-gate structure.
- **No prior task patches Makefile or creates a new pytest harness from scratch** — both are novel for this repo, so granularity choices are derived from A3 + track-3's per-file pattern.

**Recommendation:** 7 phases, ~27-37 items, one-item-per-Makefile-section + one-item-per-file-patch + one big item for new test file with V1-V7 inline. Use M1 final QA gate. Use `make sync-dev`+`make verify-sync` as recurring smoke checks after each phase that touches mirrored paths.

**Output file:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260517-183817/research/04-template-examples.md`
