# Research: MDTM Template 02 + Examples

Topic type: Template & Examples
Scope: src/superclaude/templates/workflow/02_mdtm_template_complex_task.md (PART 1) + prior .dev/tasks/to-do/TASK-RF-* examples
Status: Complete
Date: 2026-06-02

Template path note: canonical template lives at
`src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`
(the `.claude/templates/...` path in the brief does not exist; `.claude/` mirror
does not include `templates/`). Cite as `template:LINE` against the src path.
Template is 1204 lines: PART 1 (instructions, lines 46-888 inside an HTML comment)
+ PART 2 (the actual copy-out task template, lines 890-1204).

---

## 1. Core building rules (PART 1)

### Section A — Core Principles

- **A3 Complete Granular Breakdown** (`template:91-95`): Break EVERY phase into
  atomic, verifiable checklist items. One checklist item per file/component/iteration.
  NO high-level or bulk operations. Include exact file paths, specific requirements,
  measurable outcomes. → For our 8-FR skill task: one item per file edited, per
  eval-case scaffold, per QA gate.
- **A4 Iterative Process Structure** (`template:97-116`): For any multi-item process —
  (1) pre-enumerate ALL items in an initial step, (2) one checklist item per specific
  item, (3) incremental updates after each, (4) a consolidation step only after all
  done. Canonical shape: `Step X.1` scan/enumerate → `Step X.2` process each
  individually → `Step X.3` consolidate. The orchestrator (builder) enumerates;
  the worker NEVER dynamically adds items.
- A1/A2/A5/A6 are `[WORKFLOW-DEPENDENT]` (`template:72-83,85-89,118-128`): only apply
  when governing workflow docs exist in `.gfdoc/workflows/` etc. For a skill-protocol
  task with no formal workflow doc, A1 step 3 says **omit** workflow-specific sections
  and derive requirements from the spec/FRs directly.

### Section B — Self-Contained Checklist Items (CRITICAL)

- **B1 rationale** (`template:134-140`): Rigorflow executes in batches across sessions;
  context from batch 1 is GONE by batch 3+. Hence every item must be self-contained.
  Standalone "read context" items are USELESS (context lost before use).
- **B2 the 6 required elements** (`template:142-148`) — every item must embed:
  1. Context Reference **with WHY** — which file(s) to read and why needed for THIS action
  2. Action **with WHY** — what to do and why
  3. Output Specification — exact output file name, location, content, template to follow
  4. Integrated Verification — an `"ensuring..."` clause (no fabrication; 100% source-derived;
     document negative evidence on failure)
  5. Evidence on Failure Only — log to task notes ONLY if blocked (success = output file exists)
  6. Explicit Completion Gate — literal: *"This item cannot be marked as done until the
     actions are completed in their entirety exactly as described. Once done, mark this
     item as complete."*
- **B3 format** (`template:150-153`): each item is ONE FULL PARAGRAPH (not bullets/multi-line),
  verbose and explanatory, reads like a standalone prompt.
- **B4 canonical correct example** (`template:155-158`) — quoted verbatim in §3 below.
  NOTE (`template:160-162`): do NOT create separate verification items — verification is
  the `ensuring...` clause; QA handles inter-batch verification.
- **B5 FORBIDDEN patterns** (`template:164-183`): standalone read-context items; missing
  context reference; multi-line/bulleted items; separate verification/confirmation items;
  overly granular items (e.g. "create directory" alone); separate REMINDER blocks.
- **B7 key principles** (`template:189-196`): each item is a complete independently-runnable
  prompt; context embedded IN the action; verification embedded IN the action; output files
  are the evidence; log only on failure; one verbose paragraph; QA handles inter-batch
  verification (see I15-I16).

### Section C — Embedding (NEVER separate sections)

`template:198-230`. Outputs & Deliverables (C1), Success Criteria (C2), Verification (C3)
are EMBEDDED into the items — NEVER standalone sections. C4 (`template:225-230`): task
completion handled only by the **Post-Completion Actions** section (frontmatter update +
task summary); post-completion validation = I17.

### Section E — Checklist structure rules

`template:275-388`. E1: every actionable item is a flat `- [ ] ` checkbox, NO nested
checkboxes, NO parent checkboxes summarizing children; use `**Step X.Y:**` bold headers
for grouping (not checkboxes). E2/E3: **components first, summary last** — a summary/parent
checkbox MUST come AFTER its component items, never before; work flows top→bottom only;
NEVER reference checkboxes that appear later. E4 (`template:367-372`): never place a
checkbox next to a step number; NO separate REMINDER blocks between items (workers only
see batch items, not surrounding prose) — fold any reminder INTO the item text.

### Section F — Execution (worker contract; builder must respect)

`template:390-451`. F1 five-step loop READ→IDENTIFY→EXECUTE→UPDATE→REPEAT (`template:394-403`).
F2 prohibited (`template:405-412`): no working from memory; no multi-item execution; no
skipping ahead; **no delegating across phase boundaries** (a subagent gets work from a
SINGLE checklist item only — `template:410`); **no skipping phase-gate QA** (must spawn
rf-qa after Phase 2+ — `template:411`); **no skipping post-completion validation** (rf-qa
structural + rf-qa-qualitative before Done — `template:412`). F2a (`template:414-430`)
defines item-execution discipline + the **parallel spawning exception** (`template:430`):
consecutive items in the SAME phase that spawn INDEPENDENT subagents MAY be spawned in
parallel; does NOT apply to data-dependent items.

### Section I — Additional guidelines (most load-bearing for this task)

- **I15 Phase-Gate QA Enforcement** (`template:599-607`): every task with 2+ execution
  phases MUST have ≥1 phase-gate QA checkpoint between the primary execution phase and any
  dependent later phase. A checkpoint = (1) aggregation item collecting prior-phase outputs,
  (2) QA agent spawn item (rf-qa / rf-qa-qualitative), (3) conditional-action item (proceed
  on PASS / fix-cycle on FAIL). The QA spawn item MUST follow B2's 6-element pattern and
  include: agent to spawn, phase type, input files, output report path, verdict handling,
  error clause.
- **I16 QA verdict + fix cycles** (`template:609-624`): verdicts are binary PASS/FAIL; ANY
  issue (CRITICAL/IMPORTANT/MINOR) = FAIL. Fix-cycle table:
  | Gate Type | Max Fix Cycles | After Max |
  |-----------|----------------|-----------|
  | research-gate | 3 | HALT + escalate to user |
  | synthesis-gate | 2 | unresolved → Open Questions |
  | report-validation | 3 | HALT + escalate |
  | task-integrity | 2 | unresolved → Open Questions |
  | Any qualitative gate | 3 | HALT + escalate |
  Each cycle re-verifies all previously-failed items + checks for new issues. Encode fix-cycle
  logic as L5 conditional-action items or explicit IF/ELSE inside the QA gate item.
- **I17 Post-Completion Validation** (`template:626-635`): BEFORE setting status Done, include
  validation items verifying (1) all `- [ ]` marked `- [x]`, (2) all output files exist on disk
  (Glob), (3) every blocker entry has resolution notes, (4) if source code modified — all
  relevant tests pass. These live in `## Post-Completion Actions` BEFORE the frontmatter-update item.
- **I18 Testing for code-modifying tasks** (`template:637-646`): if a task creates/modifies
  SOURCE CODE (not docs, not config), MUST include ≥1 testing item that (1) specifies the test
  command, (2) defines pass criteria, (3) specifies where results are captured, (4) follows B2.
  Use the L3 pattern. **Note for this task:** the skill protocol is markdown + eval scaffolds; if
  it touches `.py` (e.g. a grader script under `scripts/`/`refs/`), I18 applies → need a
  `uv run pytest` L3 item. If purely markdown/YAML, I18's "source code" trigger does not fire,
  but `make sync-dev`/`make verify-sync` items are still required (see §6).
- Also relevant: I1 (use "YOU MUST"/"DO NOT" directive language, `template:499-503`),
  I2 extreme granularity (`template:505-509`), I3 incremental file modification —
  "DO NOT attempt to complete entire files at once" (`template:511-514`), I6 static vs
  dynamic `task_type` (`template:526-536`), I7 explicit template usage (`template:538-544`),
  I9/I14 hallucination prevention (`template:557-561,587-597`), I11 status→Doing is the
  first action (`template:569-571`), I12 verification integrated (`template:573-578`),
  I13 Post-Completion Actions section required (`template:580-585`).

### Section J — Error handling (embedded per item)

`template:651-673`. J1 standard embedded clause: *"If unable to complete due to missing
information, file access issues, or unclear requirements, log the specific blocker using the
templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the
bottom of this task file, then mark this item complete."* J2: items are NEVER left unchecked;
success = output exists, failure = blocker logged. J3: only mark whole task ⚪ Blocked if ALL
remaining items blocked by the same issue.

### Section K — Example patterns (orchestrator reference, not copied verbatim)

`template:675-708`. K1 file-by-file processing (`#### File:` header + one self-contained item),
K2 multi-item processing (**orchestrator MUST enumerate all items at build time; worker NEVER
dynamically adds**, `template:694-696`).

### Section L — Intra-task handoff patterns — see §5 below.

### Section M — Phase-gate composite patterns

`template:837-860`. M1 phase-gate QA sequence = 3 items: (1) Aggregation (L6), (2) QA Agent
Spawn (rf-qa structural; if qualitative needed, spawn rf-qa-qualitative in a SEPARATE
following item — sequential, qualitative after structural passes), (3) Conditional Proceed (L5).
M2 applicability table (`template:852-860`): task-building tasks get a **research-gate** after
research and a **task-integrity** gate after task-file creation; doc-creation tasks get a
document-type gate after content creation before Post-Completion; code-modifying tasks get a
gate after implementation before/around testing. "When in doubt, include a gate."

### Handoff file convention (`template:718-730`)

Items write intermediate outputs to `.dev/tasks/TASK-NAME/phase-outputs/` with subdirs
`discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`. These persist across
batches/rollovers — the mechanism for cross-item info flow.

---

## 2. Frontmatter schema (`template:1-44`)

The frontmatter block IS part of the copy-out template (`template:883`). Verbatim example:

```yaml
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
```

Field notes for the builder:
- `id` format `TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS` — must match the task dir name.
- `status` lifecycle (F5/Frontmatter Update Protocol `template:447-451,943-952`):
  `🟡 To Do` → `🟠 Doing` (on start, also set `start_date`) → `🟢 Done` (on completion,
  set `completion_date`) → or `⚪ Blocked` (set `blocker_reason`). `updated_date` after
  each work session.
- `task_type: static` for fixed content (no dynamic item generation); `dynamic` only if
  items are discovered during execution (I6 `template:526-536`). The 8-FR skill task is
  **static** — all items are enumerable at build time.
- `related_docs` — list the FR spec / matrix / SKILL.md as governing docs.
- `template_schema_doc` — points back to the template used (kept empty in the raw template).
- `coordinator: orchestrator`, `autogen: false` are constants.

---

## 3. Self-contained item format — canonical example (`template:155-158`, B4)

The exact 5-field-in-one-paragraph shape (B2's 6 elements collapse into one paragraph;
element 5 "evidence on failure" + element 6 "completion gate" are the trailing two sentences):

```markdown
- [ ] Read the file `component-spec.md` at `docs/specs/component-spec.md` to extract the API interface requirements including all method signatures, parameter types, and return values that must be implemented, then read the file `BaseHandler.ts` at `src/handlers/BaseHandler.ts` to understand the structural patterns and conventions used in existing handlers, then create the file `ApiHandler.ts` at `src/handlers/ApiHandler.ts` containing a TypeScript class that implements all methods defined in the component spec with proper error handling, type annotations, and JSDoc comments following the patterns from BaseHandler, ensuring the file includes the standard header comment block, exports the class as the default export, all methods from the spec are implemented with correct signatures, no content is fabricated or assumed beyond what the source explicitly states, and no placeholder or TODO comments remain. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

Anatomy mapped to B2:
- **(1) Context + WHY** — "Read `component-spec.md` … to extract the API interface requirements…"
- **(2) Action + WHY** — "then create the file `ApiHandler.ts` … containing a TypeScript class that implements…"
- **(3) Output spec** — exact name `ApiHandler.ts` + exact path `src/handlers/ApiHandler.ts` + content reqs.
- **(4) Integrated verification** — "ensuring … no content is fabricated … no placeholder or TODO comments remain."
- **(5) Evidence on failure only** — "If unable to complete … log the specific blocker … in the ### Phase 2 Findings section …"
- **(6) Completion gate** — "Once done, mark this item as complete." (B2 wording variant; full literal at `template:148`).

---

## 4. Phase structure & anti-orphaning

PART 2's skeleton (`template:1012-1126`) delimits phases with `###` headers and steps with
`**Step X.Y:**` bold (non-checkbox) headers:

- `### Phase 1: Preparation and Setup` (`template:1012`) — Step 1.1 status→Doing
  (`template:1044-1046`), Step 1.2 create `phase-outputs/` handoff dirs (`template:1048-1050`).
  D3 CRITICAL RULE (`template:269-272`): **NO checklist items may appear before Phase 1.**
  Frontmatter → (informational) Workflow Compliance/Prerequisites → Phase 1 (first executable).
- `### Phase 2: [Main Execution Phase Name]` (`template:1063`) — L1→L2→L3→L5 step examples.
- `### Phase Gate: Quality Verification` (`template:1090-1096`) — Step PG.1 QA gate
  (remove section entirely if no gate needed).
- `### Phase [N]: Testing & Verification` (`template:1098-1104`) — only for code-modifying
  tasks (I18); remove if doc/config-only.
- `### Phase 3: [Review and Quality Assessment]` (`template:1106-1116`) — L4 review + L6 aggregate.
- **`## Post-Completion Actions`** (`template:1118-1126`) — the **final-phase completion items**
  (anti-orphaning). Exactly 4 items in the raw template:
  1. Glob-verify all output files exist (I17.2) — `template:1120`
  2. If source modified, run test suite / confirm tests passed (I17.4) — `template:1122`
  3. Create `### Task Summary` at top of Task Log (work done, challenges, deviations, blockers) — `template:1124`
  4. Update `completion_date`/`updated_date`, set status `🟢 Done`, append Execution Log entry — `template:1126`
  The frontmatter-Done item is **last** so validation precedes the Done flip (I17).
- **`## Task Log / Notes 📋`** (`template:1128-1204`) goes at the very bottom and contains:
  `### Task Summary` (filled in post-completion), `### Execution Log`, and one
  `### Phase N - [Name] Findings` block per phase, `### Phase Gate Findings`,
  `### Follow-Up Items Identified`, `### Deviations from Process`. All blocker logging
  (J1) routes into the matching `### Phase N Findings` block.

Anti-orphaning principle: every completion/validation action lives in `## Post-Completion
Actions` as the terminal phase; no later phase can depend on an output that isn't QA-gated
first (I15). Summary checkboxes always come AFTER their components (E2/E3).

---

## 5. Subagent-spawning item pattern (L1-L6) (`template:710-835`)

L-patterns are the handoff vocabulary. Each is a single self-contained B2 item that
writes/reads a handoff file under `phase-outputs/`:

- **L1 Discovery** (`template:737-747`): explore codebase → write structured machine-readable
  inventory to `phase-outputs/discovery/`. "The discovery file IS the deliverable."
- **L2 Build-from-Discovery** (`template:749-759`): read discovery file AND source file →
  create deliverable. Always reference BOTH the discovery path and the source path.
- **L3 Test/Execute** (`template:761-771`): run a command via Bash → capture BOTH raw output
  (`phase-outputs/test-results/*.txt`) AND a structured summary (`*.md`). This is the pattern
  I18 mandates for code-modifying tasks and the pattern for `make verify-sync`/`pytest` items.
- **L4 Review/QA** (`template:773-783`): assess a prior output vs source → write a structured
  PASS/FAIL verdict to `phase-outputs/reviews/`. Never a vague "looks good."
- **L5 Conditional-Action** (`template:785-797`): read a result/status file → branch. MUST
  handle BOTH branches (PASS → verdict file; FAIL → fix-plan file). Output always created.
- **L6 Aggregation** (`template:799-809`): Glob to discover all relevant files → consolidate
  into a report in `phase-outputs/reports/`. Discover dynamically, don't hardcode the list.

**The QA-gate spawn item (the per-phase QA gate spawning rf-qa) — quoted verbatim**
from the PART 2 skeleton (`template:1096`), the literal pattern the builder fills in:

```markdown
- [ ] [QA GATE ITEM — Replace with actual QA agent spawn item following B2 pattern. Example: "Spawn rf-qa in [phase-type] mode to verify all Phase 2 outputs at [paths], ensuring the agent writes its report to [output-path] and returns a PASS/FAIL verdict. If FAIL, read the report, address all findings in the relevant Phase 2 output files, then re-spawn rf-qa in fix-cycle mode (max [N] cycles per I16). If unable to complete due to agent spawn failure, log the blocker in ### Phase Gate Findings below, then mark this item complete."]
```

And the L3 testing-item skeleton (`template:1104`) — the shape for a `make verify-sync` /
`pytest` gate:

```markdown
- [ ] [TESTING ITEM -- Replace with actual test execution item following B2 pattern. Example: "Run the test suite covering the modified code by executing `[test command]` to verify all tests pass with no regressions, ensuring the test output shows 0 failures and no errors in the modified modules, then capture the results to `[output-path]`. If tests fail, read the failure output to identify the root cause, attempt to fix the failing tests or the source code causing failures, then re-run. If unable to resolve test failures, log the specific failures using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."]
```

Key spawn rules (from M1 `template:843-851` + F2 `template:410-412`):
- The QA spawn item embeds the **agent name** (rf-qa structural; rf-qa-qualitative in a
  SEPARATE following item if qualitative QA needed — sequential, qualitative after structural),
  **phase type**, **input file paths**, **output report path**, **verdict handling**
  (PASS→proceed, FAIL→fix cycle up to I16 max), and the **error clause**.
- A subagent receives work from a SINGLE checklist item only; never delegate across phase
  boundaries; never delegate the F1 loop itself (`template:410`).
- Independent same-phase spawns may run in parallel (F2a exception `template:430`);
  data-dependent spawns must be sequential.

---

## 6. Prior-example patterns (what works)

Two examples inspected. **TASK-RF-20260526-183300** ("Targeted sc-brainstorm Remediation
Tasklist") is the closest analog to this task: a skill-protocol remediation editing
`src/superclaude/skills/.../SKILL.md` + `refs/`, hardening eval scripts, with a per-phase
QA gate after EVERY phase. **TASK-RF-20260529-171029** (Layer 5 detector) is a
code-modifying example with FINAL_ONLY QA + version-conditional baseline.

### 6a. Per-file edit items (markdown protocol edits)

`183300:142` (Step 2.1) is the canonical per-file SKILL.md edit. Effective pattern:
- Opens with reading the **research file at specific line ranges** ("Read `research/01...md`
  lines 16-47, 78-119, …") to extract the change spec — research is the source of truth.
- Then a **mandatory fresh pre-edit Read** of the target: "then perform a fresh pre-edit
  Read of `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` to locate the current
  Wave 1, Wave 3, … sections" — this defeats stale research line numbers (the freshness
  discipline baked into the item). The phase intro at `183300:138` states it as a rule:
  *"Each source edit item MUST perform a fresh Read of its target file before line-specific
  edits; do not rely on research line numbers alone."*
- "**edit only** `src/.../SKILL.md`" — scopes the edit to one source-of-truth file, never
  the `.claude/` mirror.
- The `ensuring…` clause encodes the success criteria ("requires a dedicated `## Provenance`
  section rather than inline comments", "no placeholder text").
- Ends with the full B2 completion gate sentence verbatim. → For the 8-FR task: one Step
  2.X item per file touched (SKILL.md, each ref, inline §9 contract), each reading the FR
  spec + matrix at cited lines, fresh-reading the target, editing only the `src/` copy.

The code analog `171029:150` (T02.07) shows the same shape for a `.py` cascade-branch insert:
read the source region, give the **exact insertion anchor** ("IMMEDIATELY AFTER the closing
line of the Layer 2 elif … and BEFORE the FR-MOD1.3 …"), specify the **exact body to insert**,
and an `ensuring (a)…(e)` multi-clause verification.

### 6b. make sync-dev / make verify-sync items

`183300` Phase 5 ("Sync and Validation Commands", `183300:208-238`) is the model for our
sync items. Effective sequence:
1. **Step 5.1 mirror-discipline audit** (`183300:214`): a read-only `git status` that
   classifies changed files into source-of-truth / eval-workspace / generated-mirror / other,
   and **treats any `.claude/skills,commands,agents,hooks,templates` change as a blocker to
   revert/regenerate, never stage**. Output → `phase-outputs/reports/source-of-truth-change-audit.md`.
2. **Step 5.2 conditional sync-dev** (`183300:218`): "if and only if mirrors are needed run
   `make sync-dev` … capture to `…/make-sync-dev-output.txt`; if not needed, create
   `…/make-sync-dev-skipped.md` explaining why." (L5-style branch — always produces an artifact.)
3. **Step 5.3 verify-sync** (`183300:222`): run `make verify-sync`, capture raw output + a
   structured summary file with PASS/FAIL, exit code, and drift paths (L3 pattern).

`171029` does it unconditionally and earlier: **T04.01 runs `make sync-dev` as the FIRST
Phase 4 item** (`171029:206`), capturing output and explicitly noting "`.claude/...*` is NOT
staged later — it is gitignored — but the mirror MUST exist." Both examples cite the global
CLAUDE.md ABSOLUTE RULE inside the item text. → For the 8-FR task (which edits
`src/superclaude/skills/sc-reflect-protocol/`), include a sync-dev item after all source
edits + a verify-sync item, each capturing output to `phase-outputs/test-results/`, with the
mirror-discipline guard embedded.

### 6c. QA-gate items (per-phase, inline rf-qa spawn)

`183300` uses **a phase gate after every phase** (PG-1…PG-6) — one `**Phase Gate PG-N:**`
header + one rf-qa spawn item — plus a final task-integrity gate in Phase 7. The canonical
gate item `183300:134` (PG-1) embeds, effectively:
- Read the phase's aggregated summary report (the L6 aggregation feeds the gate).
- `spawn rf-qa` with **`QA_MODE: task-integrity`, `fix_authorization: true`**, and the
  **exact byte-for-byte adversarial-stance string**: `ADVERSARIAL STANCE: Assume the work
  contains errors. Your job is to find what was missed, not confirm everything is fine.
  Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly
  checked.` (matches project memory `feedback_rfqa_adversarial_pattern.md`).
- QA agent writes verdict to `phase-outputs/reviews/pg-N-<name>-qa.md` with an enumerated
  PASS/FAIL coverage checklist.
- Fix-cycle: "if FAIL, fix … re-spawn rf-qa for up to **two task-integrity fix cycles** while
  applying the retry ordering regression, monotonicity, hard-cap, proceed."
- "no later phase begins unless the report verdict is PASS; unresolved issues must be logged
  as blockers and must halt the task."

`171029` runs **two final gates back-to-back**: T04.07 rf-qa task-integrity (`171029:230`)
then T04.08 rf-qa-qualitative (`171029:234`) — structural before qualitative, sequential,
each with its own fix-cycle cap (2 for task-integrity, 3 for qualitative) and a **Retry
Monotonicity Protocol** with byte-exact HALT messages (`[HALT-MONOTONICITY] |F|=<n>` and the
regression-detected string). The phase intro `171029:202` states the cycle caps explicitly.
→ For the 8-FR task: the brief asks for **per-phase QA gates** — follow the 183300 PG-N
model (a gate after each implementation/eval phase) plus a final task-integrity + qualitative
pair before Done.

### 6d. Version-conditional / baseline-gate items

`171029` T01.03 (`171029:110`) is the version-conditional pattern: a **baseline-state gate**
run BEFORE any implementation. It runs two probe commands (`wc -l …` must report ≥710 lines
AND `grep -c _is_descriptive_context …` must return ≥1), writes a PASS/FAIL verdict to
`phase-outputs/baseline-gate/gate-output.txt`, and **blocks Phase 2 if EITHER probe fails**,
pointing at remediation options in Prerequisites §1. The `### Phase 1 Exit Gate` prose
(`171029:112-114`) restates: "Phase 2 MAY begin only after T01.03 logs a PASS verdict."
The Prerequisites section (`171029:46-50`) documents that line numbers are anchored against
a specific (POST-Fix-1+Fix-3) source version living in a sibling worktree. → If sc-reflect
V3 work depends on a specific SKILL.md version/state (e.g. prior V2 edits landed), add an
analogous Phase-1 baseline probe (`grep -c` for an expected anchor + a line-count floor) that
blocks implementation until the expected baseline is confirmed.

### 6e. Other effective patterns observed

- **Phase Exit Gate prose** (non-checkbox `### Phase N Exit Gate` headers, `171029:112,152,190`)
  restate the gating rule between phases without adding a checkbox — keeps the flow legible.
- **Conditional "skip artifact" items**: when a step may not apply (Step 5.2 sync, 5.6 pytest),
  the item still produces a `*-skipped.md` artifact explaining why — never silently no-ops,
  satisfying I17.2 (every expected output exists or has a documented reason).
- **UV-only enforcement in-item** (`183300:210,226`): "All Python commands MUST use `uv run
  python` or `uv run pytest`; do not use bare Python commands" — echoed inside each command item.
- **Frontmatter**: both examples use a slightly leaner frontmatter than the raw template
  (`171029:1-21` uses `template: 02-complex`, `qa_gate: FINAL_ONLY`, `testing: UNIT`;
  `183300:1-40` uses `template: "02_mdtm_template_complex_task"`, `autogen_method: "task-builder"`).
  Both keep `id`, `title`, `status`, `priority`, `created`/`created_date`, `type`,
  `related_docs`, `tags`. The status vocabulary in practice is `To Do`/`In Progress`/`Done`
  /`Blocked` (plain words, `171029:4`) OR the emoji set (`🟡/🟠/🟢/⚪`, template default) —
  pick one and be consistent within the file.

---

## 7. Common pitfalls the template warns against (builder checklist)

1. **Standalone "read context" items** (B5 `template:166-169`, Context Loading Note
   `template:1035-1039`): never an item that only reads + logs; context is lost by the next
   batch. Always pair read with a producing action.
2. **Parent-before-children / summary-in-middle checkboxes** (E2 `template:327-341`): summary
   checkboxes only AFTER their components; no nested checkboxes; group with bold headers.
3. **Separate verification items** (B5/C3/I12 `template:181,219-222,573-578`): verification is
   the `ensuring…` clause, never its own checkbox.
4. **Multi-line / bulleted items** (B5 `template:175-180`): each item is ONE paragraph.
5. **Checklist items before Phase 1** (D3 `template:269-272`): nothing executable above Phase 1;
   Workflow-Compliance/Prerequisites blocks are INFORMATIONAL ONLY.
6. **REMINDER blocks between items** (E4 `template:371-372`): workers only see their batch items,
   not surrounding prose — fold reminders INTO the item.
7. **Backward references** ("see below", "return to phase", "mark item above") — all FORBIDDEN
   (E3 `template:357-366`).
8. **Worker dynamically adding items** (K2 `template:694-696`): the builder MUST enumerate ALL
   items at build time (A4); `task_type: static`.
9. **Missing phase-gate QA on 2+ phase tasks** (I15/F2 `template:411,599-607`) and **skipping
   post-completion validation** (I17 `template:412,626-635`).
10. **Editing / staging `.claude/` mirrors** — both examples embed this guard in-item
    (`183300:110,214`; `171029:206`); source-of-truth is `src/superclaude/`, mirror via
    `make sync-dev` only, never `git add .claude/...`.
11. **Trusting research line numbers without a fresh pre-edit Read** (`183300:138`): always
    re-Read the target file in the edit item before line-specific edits.
12. **Fabrication** (I9/I14 `template:557-561,587-597`): every item's `ensuring…` clause must say
    content is 100% source-derived, no placeholders/TODOs, document negative evidence on failure.

---

## Status: Complete

### Summary of must-follow rules for the builder

1. **Frontmatter** (`template:1-44`): `id` matches dir name, `status: 🟡 To Do` (or `To Do`),
   `task_type: static`, `coordinator: orchestrator`, `autogen: false`, `related_docs` →
   FR spec + matrix + SKILL.md. Status lifecycle To Do→Doing→Done(/Blocked).
2. **Every checklist item = one self-contained paragraph** with B2's 6 elements
   (`template:142-158`): Context+WHY, Action+WHY, exact Output spec, integrated `ensuring…`
   verification, failure-only blocker-log clause, literal completion-gate sentence.
3. **Granularity** (A3/A4): one item per file edited / eval-case / QA gate; builder
   enumerates all items up front; no worker-added items.
4. **Phase layout**: Phase 1 (status→Doing + create `phase-outputs/` dirs) → implementation
   phases (per-file edit items, L1-L6 handoff patterns) → **per-phase QA gates** (I15/M1:
   aggregate L6 → rf-qa spawn → L5 conditional) → testing items if code modified (I18/L3:
   sync-dev/verify-sync/pytest, capturing to `phase-outputs/test-results/`) → **Post-Completion
   Actions** (I17: Glob existence check, tests-pass, Task Summary, frontmatter→Done LAST) →
   `## Task Log / Notes` with per-phase Findings blocks. No items before Phase 1 (D3).
5. **QA-gate items** spawn rf-qa with `QA_MODE: task-integrity`, `fix_authorization: true`,
   the byte-exact ADVERSARIAL STANCE string, write verdict to `phase-outputs/reviews/`,
   enforce I16 fix-cycle caps, and block the next phase until PASS. Pair structural rf-qa
   with rf-qa-qualitative (sequential) at the final gate.
6. **Source-of-truth discipline embedded in-item**: edit only `src/superclaude/...`, run
   `make sync-dev` then `make verify-sync` (capture both), NEVER stage `.claude/` mirrors,
   UV-only Python commands.
7. **Mandatory fresh pre-edit Read** of every target file inside its edit item; do not trust
   research/spec line numbers alone.
8. **If a specific SKILL.md baseline is required**, add a Phase-1 baseline probe
   (grep-anchor + line-count floor) that blocks implementation on FAIL (171029 T01.03 model).

### Citations index
- Template: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`
  (A3 `:91`, A4 `:97`, B2 `:142`, B4 example `:155`, E2 `:294`, F2 `:405`, I15 `:599`,
  I16 `:609`, I17 `:626`, I18 `:637`, L1-L6 `:737-809`, M1 `:843`, PART2 skeleton `:1012-1126`).
- Example A (skill-protocol analog): `…/TASK-RF-20260526-183300/TASK-RF-20260526-183300.md`
  (frontmatter `:1`, per-file edit `:142`, PG gate `:134`, sync phase `:208-238`, Phase 7 `:264-282`).
- Example B (code-mod + version-conditional): `…/TASK-RF-20260529-171029/TASK-RF-20260529-171029.md`
  (frontmatter `:1`, baseline gate `:110`, code edit `:150`, sync-dev `:206`, final QA `:230,234`).
