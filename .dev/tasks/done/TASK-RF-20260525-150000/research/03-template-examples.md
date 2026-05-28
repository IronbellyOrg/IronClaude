# Research: Template & Examples
**Topic type:** Template & Examples
**Scope:** MDTM template 02 PART 1 + prior task examples
**Status:** Complete
**Date:** 2026-05-25
---

## Source Template

**Authoritative template:**
`/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`

- Total lines: 1205
- PART 1 (instructions for orchestrator/task builder) = lines 47-870
- PART 2 (the actual task-file template content) = lines 888-1204
- Sections A-M cover all rules. Sections L (handoff patterns) + M (phase-gate composites) are 02-specific extensions of Template 01.

The merged Fix B refactor (single Python module modify + tests) MUST use Template 02 because it requires: discovery (line-number drift verification), per-file build items, a test/execute item (uv run pytest), and a QA gate before Done. Template 01 is insufficient.

---

## Frontmatter Requirements (template lines 1-44)

### Required fields the task builder MUST populate

| Field | Type | Value for this Fix B task |
|---|---|---|
| `id` | string | `"TASK-RF-20260525-150000"` (matches folder name) |
| `title` | string | Short action title — e.g. `"Refactor build-anti-instinct: extract uncovered-contracts helper + add coverage tests (Fix B)"` |
| `description` | string (1-3 sentences) | What this task accomplishes (the merged Fix B scope) |
| `status` | string with emoji | `"🟡 To Do"` initially. Lifecycle: 🟡 To Do → 🟠 Doing → 🟢 Done. (⚪ Blocked exists but is rare.) |
| `type` | string with emoji | For this refactor: `"🛠 Code Remediation"` or `"♻️ Refactor"` (matches prior 153212 task) |
| `priority` | string with emoji | `"🔼 High"` (medium also valid: `"➡️ Medium"`) |
| `created_date` | YYYY-MM-DD | `"2026-05-25"` |
| `updated_date` | YYYY-MM-DD | `"2026-05-25"` |
| `assigned_to` | string | `"rf-task-executor"` (matches prior pattern; also seen: `"orchestrator"`) |
| `autogen` | bool | `false` |
| `autogen_method` | string | `""` |
| `coordinator` | string | `orchestrator` |
| `parent_task` | string | `""` (no parent for this standalone refactor) |
| `depends_on` | list | `[]` |
| `related_docs` | list of `{path, description}` | MUST include the merged-output.md adversarial doc + research files |
| `tags` | list | e.g. `["refactor", "python", "test-first", "anti-instinct", "coverage"]` |
| `template_schema_doc` | string | `".claude/templates/workflow/02_mdtm_template_complex_task.md"` |
| `estimation` | string | optional |
| `sprint` | string | `""` |
| `due_date`, `start_date`, `completion_date`, `blocker_reason` | string | empty at creation |
| `ai_model`, `model_settings` | string | `""` |
| `review_info` | nested dict with 3 empty strings | `{last_reviewed_by: "", last_review_date: "", next_review_date: ""}` |
| `task_type` | string | `"static"` (fixed-content task; no dynamic discovery of additional items) |

### Optional but recommended for this task

- `last_session_paused_at: ""` (seen in 153212 example) — useful for multi-session refactors

---

## Phase Structure Rules

### Section D3 Critical Rule (template lines 269-272)

> NO CHECKLIST ITEMS may appear before Phase 1 begins. The template structure ensures:
> - Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable)
> - All checklist items for context review and previous stage inputs appear IN Phase 1, Steps 1.2-1.4

### Phase 1 mandatory items (template lines 1044-1050)

- **Step 1.1** Update task status to `🟠 Doing` and `start_date`; log entry in Execution Log
- **Step 1.2** Create the `phase-outputs/` directory structure with five subdirs: `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`
- **Step 1.3+** Discovery items (L1 pattern) — verify line numbers, capture baselines (pytest, ruff, verify-sync)

### Phase numbering / ordering (Section E3, template lines 350-365)

- Sequential top-to-bottom; never reference items below current position
- Each phase must complete ALL its checkboxes before next phase
- Summary checkboxes come AFTER component items (Section E2)
- FORBIDDEN: parent checkboxes with child checkboxes; summary in middle; backward movement

### Phase-Gate QA placement (Section I15, template lines 599-607)

> Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint between the primary execution phase and any subsequent phase that depends on its outputs.

A phase-gate consists of three checklist items:
1. **Aggregation** (L6 pattern) — collect outputs from preceding phase
2. **QA agent spawn** (rf-qa or rf-qa-qualitative) with phase-type, input paths, output report path
3. **Conditional-action** (L5 pattern) — PASS proceeds, FAIL triggers fix cycle

### Fix-cycle caps (Section I16, template lines 609-624)

| Gate Type | Max Fix Cycles | After Max Reached |
|---|---|---|
| research-gate | 3 | HALT, escalate to user |
| synthesis-gate | 2 | unresolved → Open Questions |
| report-validation | 3 | HALT, escalate |
| task-integrity | 2 | unresolved → Open Questions |
| Any qualitative gate | 3 | HALT, escalate |

For the Fix B refactor, the post-Phase-2 QA gate is `task-integrity` (max 2 fix cycles).

### Recommended phase structure for the Fix B merged refactor

Based on prior task `TASK-RF-20260522-153212.md` (a structurally similar Python-module refactor + test-add) and Template 02 §L7 patterns:

```
Phase 1: Preparation & Discovery
  1.1 Update status → 🟠 Doing
  1.2 Create phase-outputs/ subdirs
  1.3 Capture pre-state pytest baseline
  1.4 Capture pre-state ruff + verify-sync baselines
  1.5 Verify line numbers from research are still accurate (re-confirm)
  1.6 Read merged-output.md to confirm scope (defensive read)

Phase 2: Test Scaffolding (RED baseline) — test-first
  2.1 Add failing test for new helper signature
  2.2 Add failing test for coverage gap N
  2.x ... (one item per new test)
  2.last Verify Phase 2 tests are RED (uv run pytest, expect non-zero exit)

Phase Gate PG-1: Test Scaffolding QA (rf-qa, task-integrity mode)
  PG-1.1 Aggregate Phase 2 outputs
  PG-1.2 Spawn rf-qa
  PG-1.3 Conditional proceed (PASS → Phase 3; FAIL → fix cycle, max 2)

Phase 3: Source Refactor (Fix B implementation)
  3.1 Extract helper / refactor target
  3.2 Update call sites
  3.3 Run full suite — confirm Phase 2 tests now GREEN, no regressions

Phase Gate PG-FINAL: Composite task-integrity rf-qa gate

Post-Completion Actions (4 fixed items per template lines 1118-1126)
```

---

## Checklist Item Format (Section B2 — the SELF-CONTAINED PATTERN)

### The 6 mandatory elements (template lines 142-148)

Every `- [ ]` item MUST be ONE FULL PARAGRAPH (Section B3) containing:

1. **Context Reference with WHY** — what file(s) to read and why
2. **Action with WHY** — what to do and why
3. **Output Specification** — exact file name, location, content, template
4. **Integrated Verification** — `ensuring ...` clause (NO fabrication; 100% from source)
5. **Evidence on Failure Only** — log to task notes ONLY if blocked
6. **Explicit Completion Gate** — verbatim long form: `"This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."` (the 153212 example uses the shorter `"Once done, mark this item as complete."` consistently; either form is acceptable when the action paragraph already enforces completion).

### Verbatim example template (Section K1, template lines 685-689)

```markdown
- [ ] Read the file `[template.md]` at `[path/to/template.md]` to understand the required format and structure for [what you're creating/modifying], then read the file `[source-data.md]` at `[path/to/source-data.md]` to extract the specific content needed for this file including [specific data points], then create or update the file `[filename1.ext]` at `[full/path/to/filename1.ext]` with the content derived from the source data following the template format, ensuring all required sections are included and properly formatted, all content matches the source data accurately with no fabrication, formatting is correct, and no placeholder text remains. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

### Forbidden patterns (Section B5)

- Standalone "read context" items that produce no output (context lost on session rollover)
- Missing context reference (no source of truth)
- Multi-line/bulleted items (must be a single paragraph)
- Separate verification items (integrate via `ensuring ...` clause)
- Overly granular items (e.g. `create directory` alone)
- Separate REMINDER blocks between items

---

## Section L: Intra-Task Handoff Patterns (specific to Template 02)

These patterns enable cross-item information flow via files written to `phase-outputs/`.

| Pattern | When to use | Output directory |
|---|---|---|
| **L1 Discovery** | Explore codebase/data and produce structured findings later items will read | `phase-outputs/discovery/` |
| **L2 Build-from-Discovery** | Create output using discovery results + source files | wherever the deliverable belongs |
| **L3 Test/Execute** | Run command/test suite, capture raw output + structured summary | `phase-outputs/test-results/` |
| **L4 Review/QA** | Assess quality with PASS/FAIL verdict + specific findings | `phase-outputs/reviews/` |
| **L5 Conditional-Action** | Branch on previous-item result; MUST handle both PASS and FAIL | `phase-outputs/plans/` |
| **L6 Aggregation** | Consolidate multiple outputs via Glob; usually final item in phase | `phase-outputs/reports/` |

### Pattern selection for Fix B merged refactor

- Phase 1 Steps 1.3/1.4 → **L1 Discovery** (pytest/ruff baseline capture, line-number reconfirm)
- Phase 2 Steps adding RED tests → standard B2 paragraph items (no L-pattern needed — test files ARE the output)
- Phase 2 final step (`uv run pytest`) → **L3 Test/Execute** capturing pytest output + EXIT_CODE
- Phase 3 source-fix items → standard B2 (the source edit + the immediate pytest re-run for fast feedback)
- PG-1.1 → **L6 Aggregation** (consolidate Phase 2 outputs for the QA gate input)
- PG-1.2 → standard B2 (rf-qa Agent spawn) — see Section M1 below
- PG-1.3 → **L5 Conditional-Action** (PASS proceeds, FAIL fix cycle with retry monotonicity)

### EXIT_CODE capture pitfall (from prior task 153212 Phase 2 Findings)

The idiom `cmd 2>&1 | tee file; echo "EXIT_CODE=$?" >> file` captures `tee`'s exit (always 0), NOT the upstream command's exit. To get the upstream command's exit:

- **Recommended:** prefix with `set -o pipefail`, OR
- Use `${PIPESTATUS[0]}` instead of `$?` after the pipeline

The prior task documented this false-clean issue; the new Fix B task should use one of these forms when capturing pytest exit codes to L3 test-results files.

---

## Section M: Phase-Gate Composite Patterns

### M1 Phase-Gate QA Sequence (template lines 843-851)

2-3 items inserted between phases:

- **Item 1 (Aggregation, L6):** Collect outputs from preceding phase
- **Item 2 (QA Agent Spawn):** rf-qa (structural) or rf-qa-qualitative (operational). If both apply, spawn rf-qa first, then rf-qa-qualitative in a separate sequential item
- **Item 3 (Conditional Proceed, L5):** Read verdict → PASS proceeds; FAIL triggers fix cycle up to I16 cap

### Retry Monotonicity Protocol (from prior task 153212 Step PG-1.3)

When a fix cycle re-spawns the QA agent for cycle N+1:

1. **Regression check FIRST.** Compare cycle N+1's would-be PASS set against cycle N's PASS set. If any item previously PASS is now FAIL → HALT with byte-exact message: `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`
2. **THEN monotonicity check.** Compare `|F_{n+1}|` to `|F_n|`. If `|F_{n+1}| >= |F_n|` → HALT with byte-exact message: `[HALT-MONOTONICITY] |F|=<n>` (the count of failing findings).
3. ONLY if both checks pass, proceed with cycle N+1.

This protocol is encoded as the conditional logic inside the PG-1.3 (L5) item itself.

### M2 Phase-Gate applicability for the Fix B refactor

Per template lines 852-860:
> Code-modifying tasks: After implementation phase and before testing phase (if testing is separate), or after combined implement+test phase.

The Fix B refactor lands tests first (Phase 2) and source fixes second (Phase 3). The natural gate is **between Phase 2 (test scaffolding) and Phase 3 (source refactor)** — exactly as the prior 153212 task did. A second gate after Phase 3 is the `PG-FINAL` composite task-integrity gate.

---

## Granularity Rules (Section A3 + A4)

### A3 Complete Granular Breakdown (template lines 91-95)

- Break every phase into atomic, verifiable checklist items
- Individual checklist item for EVERY file, component, or iteration
- NO high-level or bulk operations
- Exact file paths, specific requirements, measurable outcomes

### A4 Iterative Process Structure (template lines 97-117)

For any process with multiple items:
- Pre-enumerate ALL items in initial step (Discovery / L1)
- Create one checklist item per specific item
- Require incremental updates after each item
- Consolidation step ONLY after all items complete

For the Fix B refactor: each new test = its own Phase 2 item; each source fix = its own Phase 3 item; the final pytest run is one item per phase.

### A5 Cross-Stage Integration (workflow-dependent, mostly N/A here)

For workflow-driven tasks, every phase must explicitly specify inputs from previous stages. For this standalone refactor, prior-stage inputs are the research files under `research/` (this task's file inventory, patterns, this template-examples research) and the merged-output.md adversarial doc — these are listed in `related_docs:` frontmatter and embedded in Phase 1 read items.

---

## Section I18: Testing Requirements for Code-Modifying Tasks (template lines 637-646)

Because this Fix B task modifies source code, it MUST include at least one testing checklist item that:

1. Specifies the test command — e.g. `uv run pytest tests/path/test_build_anti_instinct.py -v` (or broader as required)
2. Defines pass criteria — e.g. `all new tests pass, no regressions in full suite`
3. Specifies where test results are captured — `phase-outputs/test-results/<name>.txt`
4. Follows the B2 self-contained pattern
5. Uses the L3 (Test/Execute) pattern

The prior 153212 task captures pytest output to `phase-outputs/test-results/0X-NN-pytest.txt` after every source-fix step (per-step micro-validation) AND at phase boundaries (Step X.last verification). For the Fix B refactor, this dual-capture pattern is recommended.

---

## Post-Completion Actions Structure (template lines 1118-1126)

EXACTLY 4 items, in this order (anti-orphaning rule: these MUST appear under `## Post-Completion Actions`, NOT inside any phase):

1. Verify all task outputs via Glob — confirm every output file specified in checklist items exists
2. If task modified source code, re-run relevant test suite — confirm no regressions
3. Create a `### Task Summary` section at the top of `## Task Log / Notes`
4. Update `completion_date` + `updated_date` to today's date; set `status` to `🟢 Done`; add Execution Log entry

These items satisfy I17 (Post-Completion Validation Protocol) — verifying all checkboxes marked, all output files exist on disk, blockers have resolution notes, tests pass.

---

## Anti-Orphaning Rule (Section C4 + I13)

> Task completion is handled by the **Post-Completion Actions section**. ... Do NOT create a "Task Completion and Handoff Protocol" section in the task file.

The four post-completion items MUST be under the `## Post-Completion Actions` heading at the end of the executable content, BEFORE `## Task Log / Notes 📋`. They are NOT inside any phase. Orchestrator-level handoff info (e.g. what to do after this task completes) lives in `ib_agent_core.md`, not in this task file.

**Practical check for the Fix B task:** the file structure MUST be exactly:

```
[frontmatter]
# Title
## Task Overview
## Key Objectives
## Prerequisites & Dependencies (informational)
## Detailed Task Instructions
### Phase 1: ...
### Phase 2: ...
### Phase Gate PG-1: ...
### Phase 3: ...
### Phase Gate PG-FINAL: ...
## Post-Completion Actions    <-- 4 items here, NOT inside Phase 3 or PG-FINAL
## Task Log / Notes 📋
```

---

## Task Log / Notes Section Structure (template lines 1128-1204)

Required subsections, in this order:

1. **`### Task Summary`** — filled in during Post-Completion Action item 3. Template fields:
   - `**Completion Date:** [YYYY-MM-DD]`
   - `**Work Completed:**` (bulleted list of outputs, files created/modified, handoff files)
   - `**Challenges Encountered:**` (bullet list or `None`)
   - `**Deviations from Process:**` (bullet list or `None`)
   - `**Blockers Logged:**` (with `Status: Resolved/Unresolved`)
   - `**Follow-Up Required:** [Yes/No]`

2. **`### Execution Log`** — timestamped entries per task-start, phase-completion, task-completion. Format:
   `**[YYYY-MM-DD HH:MM]** - [Action]: [Brief description]`

3. **`### Phase 1 — [Phase Name] Findings`** (with HTML-comment template inside for blocker entries)
4. **`### Phase 2 — [Phase Name] Findings`**
5. **`### Phase 3 — [Phase Name] Findings`** (one section per phase)
6. **`### Phase Gate Findings`** — QA gate verdicts, fix cycle counts, unresolved issues
7. **`### Follow-Up Items Identified`** — deferred / out-of-scope items with priority tags
8. **`### Deviations from Process`** — expected-vs-actual record with rationale

Blocker entry format (template lines 1178-1183):

```markdown
**[YYYY-MM-DD HH:MM]** - Step X.Y BLOCKED:
- **Blocker Reason:** [Specific reason]
- **Attempted:** [What was tried]
- **Required to Unblock:** [What's needed]
```

---

## Prior Task Examples (effective patterns)

### Strong reference: `TASK-RF-20260522-153212` (Python-module refactor + tests)

Path: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260522-153212/TASK-RF-20260522-153212.md`

Why it's a strong reference: same shape as the Fix B merged refactor — a single Python module modify (`src/superclaude/cli/eval/`) plus new pytest tests, plus phase-gate QA. 660 lines, completed in one task across multiple sessions.

**Effective patterns to copy:**

1. **`## Resolved Questions` section** at the top of the task body — when adversarial-debate inputs (like merged-output.md) include resolved Open Questions or DECIDED branches, lift them verbatim into a `## Resolved Questions` section above `## Key Objectives`. Each entry includes the DECIDED path, the alternative not taken, and the affected later steps. Prevents the executor from re-deliberating mid-execution.

2. **`## Key Objectives` numbered list** — 5-8 numbered bullets, each with a bolded title + concrete outcome. Maps 1:1 to acceptance criteria of the merged-output spec.

3. **Phase headers with explanatory paragraph above the steps** — each `### Phase N: Title` is followed by 1-2 sentences explaining what the phase does and its place in the overall test-first flow. Improves readability without inflating the checklist.

4. **Per-source-fix immediate pytest capture** — every Phase 3 source-fix step ends with `Run cd /config/workspace/IronClaude && uv run pytest <narrow target> -v ... ensure EXIT_CODE=0`. Fast feedback per step + full-suite verification at phase end.

5. **`## Resolved Questions` rolls into Phase 1 Step 1.5** — even though decisions are pre-recorded, a Phase 1 item explicitly writes them to `phase-outputs/plans/01-oq-decisions.md` for audit-trail completeness.

6. **`### Shell Environment Hygiene`-style sticky notes** — Phase 1's `unset VIRTUAL_ENV;` propagation note in the executor's persistent shell is the kind of one-time-setup note that lives in a short paragraph before Phase 1, NOT inside a checklist item.

7. **AC Matrix as final aggregation item** — Step 6.4 builds a matrix mapping every spec finding to remediation evidence (`phase-outputs/reports/06-ac-matrix.md`). This is the deliverable that proves Fix B was implemented faithfully and is the input to PG-FINAL.

8. **Static grep gates** — Step 6.1 runs `grep -rn <pattern> src/...` for each invariant the refactor must establish (e.g. `grep -rn "run_dir=resolved_output" src/...` MUST return 0 hits). Encodes "the bad pattern is gone" as a mechanical check. For Fix B, identify analogous grep gates from merged-output.md (e.g. "the old inlined logic no longer appears in build-anti-instinct.py").

9. **Adversarial-stance + escalation-override prompt blocks for rf-qa spawns** — every rf-qa Agent spawn passes:

   ```
   **ADVERSARIAL STANCE:** Assume the work contains errors. ...
   **ESCALATION — CRITICAL OVERRIDE:** You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, or TaskList. Return your verdict and report file path as your final output.
   ```

   This is mandatory for any rf-qa spawn — the bare subagent_type doesn't know it's a standalone invocation.

### Second reference: `TASK-RF-20260518-cliEval-P1-pty-isolation-gates` (P1 sprint phase task)

Path: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/TASK-RF-20260518-cliEval-P1-pty-isolation-gates.md`

- 669 lines, 8 phases including 4 Phase-Gate QAs (PG-1 through PG-4).
- Stronger example of `## Acceptance Criteria Mapping` table mapping each spec AC-ID to checklist-item indices. For Fix B with 1-5 acceptance criteria from merged-output.md, this table is helpful but optional.
- Demonstrates the L1 Discovery + L3 Test/Execute + L4 Review/QA composition for a single phase.
- Shows the `## Open Questions` section pattern with Q1/Q2/Q3 inline resolution items in Phase 1.

---

## Common Pitfalls (from prior task post-mortems)

1. **EXIT_CODE false-clean via tee** — see 153212 Phase 2 Findings. Always use `set -o pipefail` or `${PIPESTATUS[0]}`.
2. **Line-number drift between research and execution** — Phase 1 MUST include a `Reconfirm line numbers` item (153212 Step 1.6) that re-greps the load-bearing lines from the research file. If drift detected, the discovery file becomes the new source of truth.
3. **Architectural collateral discovered mid-Phase-3** — 153212 H4 fix broke 169 other tests via a layered re-check the spec didn't contemplate. Mitigation: Phase 3's verification step (X.last) MUST run the FULL suite, not just the narrow new tests. Document collateral discoveries in Phase Findings and resolve in-cycle.
4. **`make verify-sync` drift from session hooks** — `sc-troubleshoot-protocol` drift re-appeared in 153212 Phase 2. Periodically re-run `make sync-dev` between phases if verify-sync starts failing.
5. **rf-qa subagent disk-write expectation** — per MEMORY.md note `rf-qa-subagent-disk-write.md`, rf-qa with an Output path returns text not file. Mitigation: the conditional-action item AFTER the rf-qa spawn should both read the returned text AND check the expected output path on disk.

---

## Frontmatter shape (final checklist for the Fix B task file)

Required fields (must be populated):

- `id`, `title`, `description`, `status: "🟡 To Do"`, `type`, `priority`, `created_date`, `updated_date`
- `assigned_to: "rf-task-executor"`, `coordinator: orchestrator`
- `parent_task: ""`, `depends_on: []`
- `related_docs:` MUST list:
  - `.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/adversarial/merged-output.md` (the merged Fix B spec)
  - `.dev/tasks/to-do/TASK-RF-20260525-150000/research/01-file-inventory.md`
  - `.dev/tasks/to-do/TASK-RF-20260525-150000/research/02-patterns-conventions.md`
  - `.dev/tasks/to-do/TASK-RF-20260525-150000/research/03-template-examples.md` (this file)
- `tags`, `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"`
- `autogen: false`, `autogen_method: ""`, `task_type: static`
- Empty strings for: `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`
- `review_info:` nested with three empty strings

---

## Summary

The Fix B task file MUST use Template 02 because it requires discovery, test-first phasing, source-modify with per-step micro-validation, and a phase-gate QA between test scaffolding (Phase 2) and source refactor (Phase 3). Every checklist item is a single-paragraph self-contained prompt with the 6 B2 elements (context+why, action+why, output spec, ensuring-clause, blocker-on-failure, completion gate). Phase structure: Prep+Discovery → Test Scaffolding (RED) → PG-1 task-integrity gate → Source Refactor (turn GREEN) → optional PG-FINAL → Post-Completion (4 fixed items under `## Post-Completion Actions`, NOT inside any phase). Strongest reference is `TASK-RF-20260522-153212` — same shape (single Python module + new pytest tests + phase-gate QA), 660 lines, completed cleanly. Copy its Resolved Questions / Key Objectives / Phase 3 per-step pytest capture / static-grep-gate / AC-matrix / adversarial-stance-prompt patterns directly.
