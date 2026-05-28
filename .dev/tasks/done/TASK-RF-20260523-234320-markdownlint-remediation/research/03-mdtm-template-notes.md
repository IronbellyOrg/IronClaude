# Research 03 — MDTM Template & Examples Notes

**Status**: Complete
**Scope**: Template 02 (complex task) features the task builder must invoke
**Target task**: 234 markdownlint violations across 9 RF agent files, Phase 2 parallelizable per-file
**Sources**:

- `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (PART 1, lines 1-870; PART 2, lines 894-1198)
- Recent worked example: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/TASK-RF-20260522-203947-tavily-agents-refactor.md`

---

## 1. Required Sections in the Generated Task File

Driven by Template 02 PART 2 (the actual file body, lines 894-1198). Sections are listed in the exact order they must appear in the output.

### 1.1 Frontmatter (MANDATORY — see lines 1-44 of template)

Required fields the task builder MUST populate (no placeholders left behind):

| Field | Value for this task |
|---|---|
| `id` | `TASK-RF-20260523-234320-markdownlint-remediation` |
| `title` | "Remediate 234 markdownlint violations across 9 RF agent files" (or equivalent action title) |
| `description` | Detailed multi-sentence purpose statement |
| `status` | `"🟡 To Do"` (initial — flips to 🟠 Doing in Step 1.1) |
| `type` | `"📝 Documentation"` (markdown content fixes; not code) |
| `priority` | `"🔼 High"` (blocks Tavily agents PR merge) |
| `created_date` | `"2026-05-23"` |
| `updated_date` | `"2026-05-23"` |
| `assigned_to` | agent slug or empty |
| `autogen` | `false` |
| `coordinator` | `orchestrator` |
| `parent_task` | parent task ID if any (likely the Tavily agents refactor task) |
| `depends_on` | list (likely empty for fresh remediation) |
| `related_docs` | list of {path, description} including: pre-commit config, CLAUDE.md absolute rule on `.claude/`, the 9 source agent files |
| `tags` | `["markdownlint", "remediation", "rf-agents", "pre-commit"]` |
| `task_type` | `static` (all 9 files are pre-enumerated — no dynamic discovery) |

Other fields (`template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info.*`) may be left as empty strings — they are present in frontmatter schema but populated later by the executor/QA.

### 1.2 Body sections (in order)

Per PART 2 lines 896-1124:

1. `# [Task Title]` — H1 heading
2. `## Task Overview` — comprehensive description (1-2 paragraphs explaining what + why)
3. `## Key Objectives` — numbered list of 3-6 concrete outcomes
4. `## Prerequisites & Dependencies` — contains nested:
   - `### Parent Task & Dependencies` — IDs only
   - `### Previous Stage Outputs (MANDATORY INPUTS)` — INFORMATIONAL list; no checklist items here (D2, D3)
   - `### Handoff File Convention` — points at `.dev/tasks/TASK-NAME/phase-outputs/` with the 5 subdirs (`discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`)
   - `### Frontmatter Update Protocol` — restates F5 protocol verbatim
5. `## Execution Context` (OPTIONAL — per worked example lines 137-160) — used when the executor needs a pre-baked "Source areas / WHY / Goals" block so spawned subagents see all context without being told to read it. STRONGLY RECOMMENDED for this task because Phase 2 spawns 9 parallel subagents that each need to know the project conventions (`.claude/` is gitignored, src/ is SoT, edits via Edit tool only)
6. `## Detailed Task Instructions` — wraps every Phase + Phase Gate; the only place checklist items appear (D3 critical rule: NO checkboxes before Phase 1)
   - `### Phase 1: Preparation and Setup` — Steps 1.1 (status update), 1.2 (create phase-outputs dirs), plus 1.3/1.4 if needed for freshness re-reads
   - `### Phase 2: [main execution]` — the 9 per-file items
   - `### Phase Gate: Quality Verification` — aggregation + rf-qa task-integrity spawn + conditional proceed (M1 pattern)
   - `### Phase 3: Sync & verify` — `make sync-dev` + `make verify-sync`
   - `### Phase 4: Smoke tests` — `uv run pytest` baseline match
   - `### Phase 5: Stage & commit` — `git add` (src/ only) + commit
7. `## Post-Completion Actions` — 4 final items (verify outputs exist via Glob, re-confirm tests, write Task Summary, flip frontmatter to Done) — see I17 + I13
8. `## Task Log / Notes 📋` — contains nested:
   - `### Task Summary` (filled in Post-Completion)
   - `### Execution Log`
   - `### Phase 1 - Findings` (one per phase)
   - `### Phase 2 - Findings`
   - `### Phase Gate Findings`
   - `### Phase 3 - Findings`, `### Phase 4 - Findings`, `### Phase 5 - Findings`
   - `### Follow-Up Items Identified`
   - `### Deviations from Process`

Mandatory: every section above MUST be present. The optional one is `## Execution Context` (recommended here). The `## MANDATORY WORKFLOW COMPLIANCE` and `## Cross-Stage Integration Requirements` sections (D1, D2) are WORKFLOW-DEPENDENT — this task has no governing `.gfdoc/` workflow, so OMIT them per A1.

---

## 2. B2 Self-Contained Item Pattern

Every `- [ ]` checklist item is a single paragraph that includes ALL six elements (Section B, lines 142-149; reinforced in PART 2 lines 968-979).

### 2.1 The 6 Mandatory Elements

1. **Context Reference + WHY** — exact file path(s) to read and why
2. **Action + WHY** — what to do
3. **Output Specification** — exact output file path + content requirements + template (if any)
4. **Integrated Verification** — "ensuring..." clause (NEVER a separate verification item per C3 / I12)
5. **Evidence on Failure Only** — log blocker to `### Phase [N] Findings` section ONLY if blocked
6. **Explicit Completion Gate** — literal text: "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

Format: ONE FULL PARAGRAPH, verbose, no bullets/sub-bullets inside the item (B3, B5).

### 2.2 Per-Item-Type Skeletons for This Task

**(a) Per-file remediation item (Phase 2 — 9 instances)** — use L1 hybrid (discovery + edit in one item, since the violations are already pre-enumerated in researcher-1's per-file extracts):

```markdown
- [ ] **parallelizable: yes.** Read the per-file violation extract `<file-slug>-violations.md` at `.dev/tasks/to-do/TASK-RF-20260523-234320-markdownlint-remediation/research/per-file-violations/<file-slug>-violations.md` to extract the verbatim violation list (rule ID, line number, column, message) for `src/superclaude/agents/<file-slug>.md`, then read the remediation pattern reference at `.dev/tasks/to-do/TASK-RF-20260523-234320-markdownlint-remediation/research/02-remediation-patterns.md` to confirm the canonical fix for each rule ID in the extract, then Read the target file `src/superclaude/agents/<file-slug>.md` to anchor the edits, then use the Edit tool to apply ONE Edit per discrete violation cluster (group violations on the same line/section into a single Edit; keep one Edit per anchor — never sed/awk/Python helper, never `.claude/agents/`), then run `cd /config/workspace/IronClaude && uv run pre-commit run markdownlint --files src/superclaude/agents/<file-slug>.md 2>&1` and capture the output to a per-file verification file `<file-slug>-postfix-lint.txt` at `.dev/tasks/to-do/TASK-RF-20260523-234320-markdownlint-remediation/phase-outputs/test-results/<file-slug>-postfix-lint.txt`, then write a per-file review file `<file-slug>-review.md` at `.dev/tasks/to-do/TASK-RF-20260523-234320-markdownlint-remediation/phase-outputs/reviews/<file-slug>-review.md` containing the pre-fix violation count, the post-fix violation count (from the lint output), a PASS verdict iff post-fix count is 0 (FAIL otherwise) with any residual violations listed, ensuring every violation in the extract is addressed using the canonical pattern from the reference, no `.claude/agents/` file is edited, Edit tool only (no sed/awk/Python helpers — per CLAUDE.md "Never strategy-pivot to avoid hooks"), and the post-fix lint output is the binding evidence (zero violations = PASS). If the file has anchor drift (the violation line numbers in the extract no longer match the current file content), log the specific drift using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.
```

Notes on this skeleton:

- "**parallelizable: yes.**" prefix marks the item for F2a parallel spawning by the executor.
- The per-file `uv run pre-commit run markdownlint --files <file>` IS the in-item verification — no separate verification item (C3, I12).
- The review file is the input to the Phase Gate aggregation item.

**(b) Aggregation item (Phase Gate Step PG.1 — L6 pattern):**

```markdown
- [ ] Use Glob to find all review files matching `.dev/tasks/to-do/TASK-RF-20260523-234320-markdownlint-remediation/phase-outputs/reviews/*-review.md` to discover all 9 per-file reviews produced by Phase 2, then read each review file to extract: file name, pre-fix violation count, post-fix violation count, PASS/FAIL verdict, residual violations list, then create a consolidated phase-2 review report at `.dev/tasks/to-do/TASK-RF-20260523-234320-markdownlint-remediation/phase-outputs/reports/phase-2-review-report.md` containing: an executive summary line (X/9 PASS, Y/9 FAIL, total pre-fix N → total post-fix M), a table with columns File / Pre-Fix / Post-Fix / Verdict / Residual Violations, and a final overall verdict (PASS iff all 9 are PASS with 0 post-fix violations), ensuring all 9 expected review files are present (missing files trigger a MISSING REVIEWS section + overall FAIL), no fabricated counts, and counts match individual reviews. If fewer than 9 review files are found, log the specific blocker (which files are missing) using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.
```

**(c) Adversarial QA spawn item (Phase Gate Step PG.2 — see Section 7 below for the full spawn pattern).**

**(d) Bash command item (Phase 3, 4 — L3 pattern):** worked example lines 263-267, 275-279 are direct precedents. Capture raw output verbatim + structured summary; the verdict is determined by BOTH exit code AND output content (verify-sync's 0-drift rule).

**(e) Conditional staging item (Phase 5 — L5 pattern):** read the verify-sync summary, branch on CLEAN vs DIRTY. Worked example lines 295-297 are precedent.

**(f) Frontmatter status flip (Step 1.1 / Post-Completion final item — F5):** see Section 8.

---

## 3. A3 Granularity Rule — One Phase 2 Item Per File (NOT a Batch)

Section A3 (lines 91-95): "Break down EVERY workflow phase into atomic, verifiable checklist items. Create individual checklist items for EVERY file, component, or iteration. NO high-level or bulk operations allowed."

Section K2 reinforces (lines 691-708): "The orchestrator agent creating this task file MUST identify and enumerate ALL items that need processing during task setup. The worker agent MUST NEVER dynamically add checklist items."

**For this task:** the 9 RF agent files MUST be enumerated as 9 separate `- [ ]` items under Step 2.1 through Step 2.9 (or Step 2.X with explicit `#### File:` subheaders, per K1 pattern, lines 685-689). NEVER one item like "fix all 9 files" — that is FORBIDDEN per B5 ("Overly granular" inverted: bulk operations are equally forbidden).

The 9 files (per researcher-1's per-file extracts — task builder MUST cross-check this list against researcher-1's actual output):

1. `src/superclaude/agents/deep-research.md`
2. `src/superclaude/agents/deep-research-agent.md`
3. `src/superclaude/agents/rf-analyst.md`
4. `src/superclaude/agents/rf-assembler.md`
5. `src/superclaude/agents/rf-qa.md`
6. `src/superclaude/agents/rf-qa-qualitative.md`
7. `src/superclaude/agents/rf-task-builder.md`
8. `src/superclaude/agents/rf-task-executor.md`
9. `src/superclaude/agents/rf-task-researcher.md`

(Note: `rf-team-lead.md` was 10th in the Tavily refactor scope but may not have markdownlint violations — confirm against researcher-1's enumeration. The build is "9 files" per the original requirement.)

---

## 4. A4 Iterative Process Structure + Parallelization Marking

A4 (lines 97-116) defines the iterative pattern: pre-enumerate → per-item checklist → consolidation step. For this task:

- **Pre-enumeration:** done by researcher-1 (per-file violation extracts). The task builder reads those and emits 9 self-contained items.
- **Per-item:** each `- [ ]` follows the skeleton in 2.2(a).
- **Consolidation:** Phase Gate Step PG.1 aggregation item.

**Marking items parallelizable:** Template 02 itself does not prescribe a literal keyword, but the worked example (`TASK-RF-20260522-203947-tavily-agents-refactor`, lines 195-247) uses the explicit prefix **`**parallelizable: yes.**`** at the start of each per-file item paragraph. The task builder MUST use this exact marker on every Phase 2 item — it is what the executor pattern-matches on when invoking F2a (Section 5 below).

---

## 5. F2a Parallel Spawning Exception (CRITICAL for this task)

Section F2a (lines 414-430), under "Item Execution Discipline", contains the parallel-spawning exception. **Exact wording from line 430:**

> **Parallel spawning exception:** When consecutive checklist items within the SAME phase spawn INDEPENDENT subagents (agents that do not read each other's outputs), the executor MAY spawn all such agents in parallel using multiple Agent tool calls in a single message. Each agent operates in isolated context. The executor MUST still mark each item individually as the corresponding agent completes. This exception does NOT apply to items that have data dependencies on each other.

**Applicability to this task:** the 9 Phase 2 items operate on 9 DIFFERENT source files (`deep-research.md`, `rf-qa.md`, …). No item reads another item's output (every item reads only its own pre-file violation extract + the canonical patterns reference + its own target file + writes its own review file). They are therefore INDEPENDENT subagents per F2a → the executor MAY (and per the user's explicit "as much in parallel as possible" requirement, MUST) spawn all 9 in one Agent batch.

**What the task builder must do to enable this:**

1. Place all 9 items in the SAME phase (Phase 2).
2. Prefix each item with `**parallelizable: yes.**` (matches worked-example convention).
3. Ensure no item references any other Phase 2 item's output file in its own context-reference clause.
4. The Phase Gate (Phase 2 → Phase 3) is the synchronization point — PG.1 aggregation reads ALL 9 review files (so it MUST run AFTER all 9 complete).

The executor's F1 loop still applies WITHIN each spawned agent's session — each agent does one item, marks it complete, exits. The parent executor marks each item as its agent reports back. No agent marks multiple items.

---

## 6. L1-L6 Handoff Patterns Used in This Task

| Pattern | Section | Used Where |
|---|---|---|
| **L1 Discovery** | lines 737-747 | Implicit — researcher-1's per-file violation extracts ARE the discovery output (already done as task-builder research, so no Phase 2 L1 item needed) |
| **L2 Build-from-Discovery** | lines 749-759 | Each Phase 2 per-file item is hybrid L1+L2: reads the violation extract (discovery file) + applies edits + writes review file |
| **L3 Test/Execute** | lines 761-771 | Phase 3 (`make sync-dev`, `make verify-sync`), Phase 4 (`uv run pytest`), Phase 5 (`git status --porcelain` check) |
| **L4 Review/QA** | lines 773-783 | Each Phase 2 item embeds its own L4 sub-step (per-file lint re-run is the verdict-producing review) |
| **L5 Conditional-Action** | lines 785-797 | Step 3.2 (skip verify-sync if sync-dev failed), Step 5.1 (skip staging if verify-sync DIRTY), Phase Gate PG.2 (PASS proceed / FAIL fix cycle) |
| **L6 Aggregation** | lines 799-809 | Phase Gate Step PG.1 (consolidate 9 review files → phase-2-review-report.md) |
| **M1 Phase-Gate QA Sequence** | lines 843-851 | Phase Gate (2-3 items: L6 aggregation → rf-qa spawn → L5 conditional) |

**Handoff file convention** (lines 718-731): all intermediate outputs go under `.dev/tasks/TASK-RF-20260523-234320-markdownlint-remediation/phase-outputs/{discovery,test-results,reviews,plans,reports}/`. The task builder MUST declare this in the `### Handoff File Convention` subsection of `## Prerequisites & Dependencies`.

---

## 7. Phase Gate Convention — rf-qa task-integrity Spawn

Per Section M (lines 838-860) + I15 (lines 599-607) + I16 (lines 609-624). For this task, Phase Gate sits between Phase 2 (per-file edits) and Phase 3 (sync/verify).

### 7.1 Structure (M1 pattern, 2-3 items)

1. **PG.1 Aggregation (L6):** glob the 9 `*-review.md` files, build `phase-2-review-report.md`. (Skeleton in 2.2(b) above.)
2. **PG.2 rf-qa spawn (task-integrity mode):** the critical adversarial gate. See 7.2 below.
3. **PG.3 Conditional proceed (L5):** read the verdict file, IF PASS proceed to Phase 3, IF FAIL launch fix cycle (max 2 per I16 row "task-integrity"). For 2-item phase gates this can be inlined into PG.2's "IF FAIL" branch (worked example line 259 does this — fix-cycle logic is embedded in the PG.2 item itself, eliminating a separate PG.3 item).

### 7.2 PG.2 rf-qa Spawn Item — Required Elements

Per memory `feedback_rfqa_adversarial_pattern.md` ("Pair explicit ADVERSARIAL STANCE framing with `fix_authorization: true` whenever spawning rf-qa / rf-qa-qualitative for MDTM gates") + worked-example line 259 as direct precedent.

The spawn item MUST include:

| Element | Value for this task |
|---|---|
| Agent | `rf-qa` |
| Mode | `task-integrity` |
| Stance | **ADVERSARIAL STANCE** (explicit phrase in the prompt) |
| Authorization | `fix_authorization: true` (rf-qa may directly edit findings, not just report) |
| Inputs | `phase-2-review-report.md` + the 9 post-edit agent files (rf-qa MUST re-Read each, not trust the executor's self-report) + `.dev/tasks/.../research/per-file-violations/<each>.md` (the original violation extracts, to verify completeness) |
| Verification steps rf-qa MUST perform | (a) re-run `uv run pre-commit run markdownlint --files <each-file>` independently and assert 0 violations; (b) grep `git status --porcelain` for any `.claude/agents/` modifications (CRITICAL violation per CLAUDE.md absolute rule); (c) verify no sed/awk/Python helper was used (Edit tool only — visible in task log per memory `feedback_no_strategy_pivot_to_avoid_hooks.md`) |
| Output path | `.dev/tasks/to-do/TASK-RF-20260523-234320-markdownlint-remediation/phase-outputs/reviews/rf-qa-task-integrity-verdict.md` |
| Verdict format | Binary PASS/FAIL (per I16) with per-criterion details |
| Fix-cycle rules | Max 2 cycles (I16 row "task-integrity"); if both fail → "Unresolved issues become Open Questions" in `### Open Questions` section, proceed to Phase 3 with documentation |
| Error clause | Standard "If unable to spawn rf-qa due to agent unavailability, log blocker in ### Phase Gate Findings" |

Format: SINGLE PARAGRAPH following B2 (worked example PG.2 line 259 is the canonical model — replicate its structure, swapping out the 10 Tavily files for the 9 markdownlint files and swapping the acceptance criteria from "Tavily-first refactor applied" to "0 markdownlint violations remain").

---

## 8. Frontmatter Update Protocol (F5)

Lines 447-451 (PART 1) + 947-954 (PART 2). The task builder MUST emit a `### Frontmatter Update Protocol` subsection that says verbatim:

> YOU MUST update the frontmatter at these MANDATORY checkpoints:
>
> - **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
> - **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
> - **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
> - **After Each Work Session:** Update `updated_date` to current date

And the actual update items MUST appear:

- **Start:** Phase 1 Step 1.1 (worked example line 1046 / template lines 1045-1046)
- **Done:** Post-Completion Actions final item (template line 1123)
- **Each session:** the executor handles via F1 loop; not a separate task item

---

## 9. Common Pitfalls the Template Warns Against (CHECKLIST FOR TASK BUILDER)

The task builder MUST audit the emitted task file against each of these before declaring done:

| # | Pitfall | Section | Self-Check |
|---|---|---|---|
| P1 | Batch items ("fix all 9 files in one item") | A3, K2 | Count `- [ ]` in Phase 2 = 9 |
| P2 | Standalone "read context" items with no output | B5 line 168 | Every item produces an output file or a frontmatter change |
| P3 | Multi-line / bulleted item bodies | B3, B5 line 175 | Every item is ONE paragraph (no nested bullets) |
| P4 | Separate verification items | C3, I12 | No item title contains "Verify" or "Confirm" as the only action — verification is "ensuring..." clause |
| P5 | Missing 6-element completion gate | B2, PART 2 lines 972-979 | Every item ends with the literal "Once done, mark this item as complete." |
| P6 | Parent checkbox before child checkboxes | E2 lines 327-333 | No `- [ ]` is followed by indented `- [ ]` children |
| P7 | Summary checkbox in middle of sequence | E2 lines 335-341 | Summaries (if any) are LAST in their step |
| P8 | Checklist items before Phase 1 | D3 lines 270-273 | First `- [ ]` is in Step 1.1 |
| P9 | Workflow compliance / cross-stage sections kept when no workflow exists | A1 lines 72-83 | OMIT `## MANDATORY WORKFLOW COMPLIANCE` and `## Cross-Stage Integration Requirements` for this task |
| P10 | Missing phase-gate QA after Phase 2 | I15 lines 599-607, F2 line 411 | Phase Gate section exists with rf-qa spawn |
| P11 | Missing Post-Completion validation (I17) | I17 lines 626-635 | Final 4 Post-Completion items: verify outputs exist, re-run tests, write Task Summary, flip status to Done |
| P12 | Testing item missing for code-modifying tasks (I18) | I18 lines 637-646 | This task is documentation-only (markdown content), so I18 strictly does not apply — BUT the task DOES modify files that pre-commit checks, so Phase 3 (`make verify-sync`) + Phase 4 (`uv run pytest` baseline) + per-file `uv run pre-commit run markdownlint` IS the equivalent test gate and MUST be present |
| P13 | `.claude/agents/` edits or stages (CLAUDE.md absolute rule) | Project CLAUDE.md + memory `feedback_claude_dir_gitignored.md` | Every Phase 2 item explicitly says "Edit tool only, no `.claude/agents/`"; Phase 5 stages ONLY `src/superclaude/agents/...`, never `.claude/...`; rf-qa PG.2 explicitly greps for `.claude/agents/` mods |
| P14 | sed/awk/Python helper used to escape hooks | Memory `feedback_no_strategy_pivot_to_avoid_hooks.md` | Every Phase 2 item explicitly says "Edit tool only — no sed/awk/Python helper" |
| P15 | Multi-line paste-ready commands in task body | Memory `feedback_no_multiline_paste.md` | All Bash commands in items are single-line |
| P16 | Missing `**parallelizable: yes.**` prefix on Phase 2 items | F2a + worked example convention | Every Phase 2 item starts with this prefix |
| P17 | Tool guidance over-specified | H1, H2 | Only specify Bash / Edit / Glob when REQUIRED (this task: Edit tool for per-file edits IS required to avoid sed pivot — H3 example. Bash IS required for pre-commit runs.) |

---

## 10. Task-builder BUILD_REQUEST notes

The BUILD_REQUEST.md that the task builder skill receives MUST contain these fields populated as follows:

| BUILD_REQUEST Field | Value for this task |
|---|---|
| **GOAL** | "Remediate all 234 markdownlint violations across 9 RF agent files in `src/superclaude/agents/` (deep-research, deep-research-agent, rf-analyst, rf-assembler, rf-qa, rf-qa-qualitative, rf-task-builder, rf-task-executor, rf-task-researcher) so that `uv run pre-commit run markdownlint --files <file>` reports 0 violations per file. Sync to `.claude/agents/` via `make sync-dev`, verify byte-identical via `make verify-sync`, confirm `uv run pytest` baseline holds, then stage ONLY the `src/` side and commit." |
| **WHY** | "Pre-commit blocks any further work on the Tavily agents refactor branch (`feat/agents-tavily`) until markdownlint passes. The 234 violations are all in agent definition files (markdown), pre-existing or introduced by recent edits; fixing them unblocks PR merge and restores green pre-commit." |
| **TEMPLATE** | `02_mdtm_template_complex_task.md` (complex — 5 phases, intra-task handoff, rf-qa phase gate) |
| **QA_GATE_REQUIREMENTS** | `PER_PHASE` — specifically: **rf-qa in task-integrity mode with ADVERSARIAL STANCE + `fix_authorization: true`** after Phase 2 (per memory `feedback_rfqa_adversarial_pattern.md`). No rf-qa-qualitative gate needed (markdownlint is mechanical, not qualitative). PG.1 aggregation + PG.2 rf-qa spawn = the 2-item Phase Gate; PG.3 conditional inlined into PG.2 per worked-example pattern. Max 2 fix cycles (I16 task-integrity row); unresolved → Open Questions. |
| **VALIDATION_REQUIREMENTS** | Per-file gate (Phase 2, EACH of 9 items): `cd /config/workspace/IronClaude && uv run pre-commit run markdownlint --files src/superclaude/agents/<file-slug>.md 2>&1` — output captured to `phase-outputs/test-results/<file-slug>-postfix-lint.txt`; verdict = 0 violations. Phase 3.1: `cd /config/workspace/IronClaude && make sync-dev 2>&1`. Phase 3.2: `cd /config/workspace/IronClaude && make verify-sync 2>&1` (0-drift gate, both exit code AND output). Phase 4.1: `cd /config/workspace/IronClaude && uv run pytest 2>&1` — baseline-match gate ("no NEW failures introduced", agent definitions are documentation-style so no direct test coverage — use the same justification pattern as worked example lines 271-273). Phase 5.1: `git status --porcelain` post-stage verification — exactly 9 `src/superclaude/agents/*.md` staged, NO `.claude/agents/` lines. Phase 5.2: `git commit` (pre-commit hook re-runs markdownlint — final pass gate). |
| **TESTING_REQUIREMENTS** | `NONE` — no new tests to author. This is markdown content remediation; the validation pipeline above IS the testing. I18 (lines 637-646) "code-modifying tasks" does not strictly apply because the modified files are markdown documentation, but the per-file pre-commit re-run, `make verify-sync`, and `uv run pytest` baseline-match collectively satisfy the spirit of I18. |
| **EXECUTION_CONTEXT_REQUIREMENTS** | `AUTO` — populate `## Execution Context` (per worked example lines 137-160) with 3 source areas: (1) **the 9 agent files** at `src/superclaude/agents/{deep-research,deep-research-agent,rf-analyst,rf-assembler,rf-qa,rf-qa-qualitative,rf-task-builder,rf-task-executor,rf-task-researcher}.md`; (2) **makefile gates** at `Makefile` (`sync-dev`, `verify-sync`, `test`, `lint` targets) — read these so spawned subagents know the exact commands without inferring; (3) **pre-commit config** at `.pre-commit-config.yaml` (markdownlint hook configuration — rule set, exclusion patterns). Also embed the CLAUDE.md absolute rules: (a) `.claude/agents/` is gitignored sync-dev output (never edit, never stage); (b) Edit tool only — no sed/awk/Python helper pivot. |
| **PARALLELIZATION** | Phase 2 = 9 independent per-file items, all marked `**parallelizable: yes.**` per F2a. Executor MAY spawn all 9 in one Agent batch. Phase Gate is sync point. Phases 1, 3, 4, 5 are sequential. |
| **STATIC vs DYNAMIC** | `static` — all 9 files are pre-enumerated by researcher-1; no Phase 2 discovery item needed; `task_type: static` in frontmatter. |

---

## 11. Quick Reference for Task Builder

When generating the file, walk these template citations in order:

1. Frontmatter → template lines 1-44 + Section 1.1 above
2. Section assembly → template lines 894-1124 (PART 2 body) + Section 1.2 above
3. Phase 1 Step 1.1 (status flip) → template line 1046 verbatim
4. Phase 1 Step 1.2 (phase-outputs dirs) → template line 1049 verbatim
5. Phase 2 per-file items (×9) → skeleton 2.2(a) above; cite K1 (file-by-file) + L2 (build-from-discovery) hybrid; prefix `**parallelizable: yes.**`
6. Phase Gate PG.1 (aggregation) → skeleton 2.2(b) above; L6 pattern, lines 799-809
7. Phase Gate PG.2 (rf-qa spawn) → Section 7.2 above; worked-example line 259 as direct precedent; memory `feedback_rfqa_adversarial_pattern.md`
8. Phase 3.1 (`make sync-dev`) → worked example line 263 verbatim with task-name swap
9. Phase 3.2 (`make verify-sync`) → worked example line 267 verbatim with task-name swap (L5 conditional embedded — skip if 3.1 failed)
10. Phase 4.1 (`uv run pytest`) → worked example line 275 verbatim with task-name swap
11. Phase 5.1 (`git add src/superclaude/agents/...`) → worked example line 295 verbatim with file list swap (9 not 10) and task-name swap
12. Phase 5.2 (`git commit`) → worked example structure, single-line commit message per memory `feedback_no_multiline_paste.md`
13. Post-Completion (4 items) → template lines 1117-1123 verbatim
14. Task Log scaffold → template lines 1125-1198 verbatim

---

**End of research notes.** Researcher-1 produces the per-file violation extracts (input to Phase 2 items); researcher-2 produces the remediation pattern reference (input to Phase 2 items); this document tells the task builder which template features to invoke and how. All three together feed the BUILD_REQUEST.md.
