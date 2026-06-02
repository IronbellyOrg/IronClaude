# Research 04: Template & Examples (Single-Track Task-Builder)

**Topic:** MDTM complex-task template structure + decision-gate / conditional-phase shape + prior example.
**Track goal:** a durable-fix task with an investigation/decision gate (intentional-vs-drift + family-SoT location) then conditional implementation.
**Status: In Progress**

Sources:

- Template: `/config/workspace/IronClaude-RoadmapRewrite/.claude/templates/workflow/02_mdtm_template_complex_task.md` (PART 1 = lines 1-888, PART 2 template = lines 890-1205)
- Prior example: `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260602-060714/TASK-RF-20260602-060714.md` (488 lines, the R1-R5 remediation task with an investigation→decision→conditional-implementation structure)

---

## 1. Frontmatter (required fields)

Copied verbatim from the template's frontmatter block (lines 1-44). For the new task, fill these and leave the rest as house-style defaults:

| Field | Notes |
|---|---|
| `id` | `TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS`. The directory already implies `TASK-RF-20260602-162259`; use that exact id. |
| `title` | Clear, action-oriented. |
| `description` | Detailed multi-sentence description (the prior example uses a long single-line string — see lines 4). |
| `status` | `"🟡 To Do"` at build time (executor flips to `🟠 Doing` / `🟢 Done`). |
| `type` | e.g. `"🔨 Refactor"` (prior example) or `"📝 Documentation"` (template default). |
| `priority` | `"🔼 High"`. |
| `created_date` / `updated_date` | `2026-06-02` (today). |
| `assigned_to` | `"rf-task-executor"` (prior example) or an agent name. |
| `coordinator` | `orchestrator`. |
| `parent_task` | empty string if standalone. |
| `depends_on` | `[]` if none. |
| `related_docs` | list of `{path, description}` — the prior example lists the design doc, the four numbered research files, and the QA-gate reports. |
| `tags` | list. |
| `template_schema_doc` | `".claude/templates/workflow/02_mdtm_template_complex_task.md"` (prior example sets this; template leaves it blank). |
| `start_date` / `completion_date` / `blocker_reason` | empty at build. |
| `task_type` | `static` (fixed content) vs `dynamic` (items discovered at runtime). Use **`static`** — all items are pre-enumerated by the builder (I6, K2). |

Other inert fields present in the schema: `autogen`, `autogen_method`, `estimation`, `sprint`, `due_date`, `ai_model`, `model_settings`, `review_info.{last_reviewed_by,last_review_date,next_review_date}`. Keep them as empty defaults.

---

## 2. Mandatory body sections & overall structure

PART 1 of the template defines the rules; PART 2 (lines 890-1205) is the literal skeleton to copy. The body order is:

1. `# [Task Title]`
2. `## Task Overview` — prose: what + why.
3. `## Key Objectives` — numbered `**[Objective]:** ...` list (informational, NO checkboxes).
4. `## Prerequisites & Dependencies`
   - `### Parent Task & Dependencies` (parent / blocking deps / what this blocks)
   - `### Previous Stage Outputs (MANDATORY INPUTS)` — **INFORMATIONAL ONLY, NO CHECKLIST ITEMS** (D2, lines 247-267; the actual reads happen in Phase 1 Step 1.4)
   - `### Handoff File Convention` — names the `phase-outputs/` dir + the 5 subdirs `discovery/ test-results/ reviews/ plans/ reports/` (Section L convention, lines 718-730; PART 2 lines 928-941)
   - `### Frontmatter Update Protocol` — the 4 checkpoints (F5)
5. `## Detailed Task Instructions` — the executable phases.
6. `## Post-Completion Actions` — final checklist items (I13/I17).
7. `## Task Log / Notes 📋` — with `### Task Summary`, `### Execution Log`, per-phase `### Phase N ... Findings`, `### Phase Gate Findings`, `### Follow-Up Items Identified`, `### Deviations from Process` (PART 2 lines 1128-1205).

**D3 CRITICAL RULE (lines 269-273):** NO checklist items may appear before Phase 1 begins. Frontmatter → informational sections → Phase 1 (first executable checkboxes). All context-reading items live *inside* Phase 1 Steps 1.2-1.4, never as standalone pre-Phase-1 reads.

### [WORKFLOW-DEPENDENT] sections — OMIT for this task

Sections marked `[WORKFLOW-DEPENDENT]` (A2, A5, A6, D1 Workflow Compliance Declaration, D2 Cross-Stage Integration) apply only when a governing workflow doc exists in `.gfdoc/workflows/` etc. (A1, lines 72-83). This durable-fix task is **derived from research files + a design intent**, not a stage workflow — so omit the "MANDATORY WORKFLOW COMPLIANCE" declaration and replace workflow references with the research-file/design inputs directly. The prior example (TASK-RF-20260602-060714) does exactly this: it has no Workflow Compliance Declaration section and instead carries an `## Execution Context` reader-aid block (example lines 121-127) plus the research files in `related_docs`.

---

## 3. The self-contained checklist item — exact shape (B2 / B3 / B4)

**Every actionable line is `- [ ] <one full paragraph>`.** Each paragraph is a complete standalone prompt embedding all 6 elements (B2, lines 142-148; reinforced PART 2 lines 970-976):

1. **Context Reference + WHY** — which file(s) to read and why (`Read the file X at <path> to extract ...`).
2. **Action + WHY** — what to do with that context.
3. **Output Specification** — exact output file name + path + content + template (if any).
4. **Integrated Verification** — an `ensuring ...` clause (no fabrication, 100% from source, document negative evidence). **Verification is NOT a separate item** (B4 NOTE, C3, I12).
5. **Evidence on Failure Only** — `If unable to complete due to ..., log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete.` (J1, lines 659-663). Success needs no log — the output file IS the evidence.
6. **Explicit Completion Gate** — `Once done, mark this item as complete.` (or the longer "This item cannot be marked as done until ...").

**Grouping:** use `**Step X.Y:** <header text>` lines (bold, NO checkbox) to group; the checkbox(es) follow underneath (E1 line 283, E4 lines 367-381). Step numbers must NOT carry a checkbox.

### Checklist structure rules that constrain the builder (Section E)

- Flat checkboxes only — NO nested/parent checkboxes (E1).
- Components BEFORE summaries; any summary/aggregation checkbox comes LAST in its sequence (E2, lines 294-348).
- Strictly top-to-bottom; never reference a later checkbox or require marking an earlier one (E3, lines 350-366). Forbidden phrases: "mark item complete in section above", "see checklist below", "return to phase and mark complete".
- One paragraph per item — no multi-line/bulleted items, no separate REMINDER blocks (B5, E4).

### FORBIDDEN item patterns (B5, lines 164-184)

- Standalone "read context and log findings" items that produce no output (context is lost across session rollovers — B1).
- Items with no context reference / source of truth.
- Multi-line or bulleted item bodies.
- Separate verification / confirmation items.
- Overly granular items (e.g. "create directory" alone — fold it into the file-creating item; cf. PART 2 Step 1.2 which folds dir-creation into one item).

---

## 4. Decision gate / conditional phase shape (the core of this task)

The template expresses a decision gate as a sequence of intra-task handoff items (Section L, lines 710-836), and the **L5 Conditional-Action item** is the decision gate itself.

### Pattern flow for an investigation → decision → conditional-implementation task

The recommended structure (Section L7 "Build → Test → Fix" / "Full Lifecycle", lines 823-835) maps cleanly onto this track:

```
Phase: Investigation (L1 Discovery + L3 Test/Execute)
   -> writes evidence to phase-outputs/discovery/ and phase-outputs/test-results/
Phase: Decision Gate (L5 Conditional-Action)
   -> reads the investigation evidence, writes ONE decision artifact to phase-outputs/plans/
      that handles BOTH branches (intentional-vs-drift; family-SoT-location-A vs B)
Phase: Conditional Implementation (every item GATED on the decision artifact)
   -> each item begins by reading the decision artifact; IF branch-skip -> mark complete with a
      "Skipped: <reason>" note and make NO change; IF branch-proceed -> perform the edit
Phase: Final Validation Gate (L3 captures + QA gate)
```

### L1 Discovery item (investigation) — lines 737-747

Explores codebase/data and writes a **structured, machine-readable** findings file to `phase-outputs/discovery/`. The discovery file IS the deliverable; later items read it by path. Use `Glob` + `Read` and write an inventory/evidence file.

### L3 Test/Execute item (reproduction) — lines 761-771

Runs a command/probe and captures **BOTH** raw output (`phase-outputs/test-results/<name>.txt`, exact) **AND** a structured summary (`phase-outputs/test-results/<name>.md`). This is how the prior example reproduces a defect before deciding.

### L5 Conditional-Action item = the DECISION GATE (lines 785-797) — KEY PATTERN

> **Key rule:** The item MUST handle BOTH branches (success AND failure). Specify exactly what to do in each case. The output file is always created regardless of which branch is taken.

Shape:

> `- [ ] Read the <evidence file> at <path> to determine <the decision criterion>, then: IF <condition A> create the file <decision-artifact>.md at .dev/tasks/<TASK>/phase-outputs/plans/<name>.md containing <branch-A content + a statement that downstream phase is SKIPPED>; IF <condition B> ... create the same artifact containing <branch-B content + the enumerated carry-forward list naming which downstream items apply>, ensuring <no fabrication, evidence-based>. If unable to complete ..., log the blocker ..., then mark this item complete. Once done, mark this item as complete.`

The decision artifact is **always written** (so a resumed session knows which path was taken). It carries a `decision:` field plus the evidence. Downstream phases gate on it.

### Conditional (gated) implementation items

Each implementation item in the conditional phase is itself an L5-flavored item: it **opens by reading the decision artifact** and branches:

- IF skip-branch → "mark this item complete with a `Skipped: <decision> = <branch>` note in the `### Phase N Findings` section and make NO change".
- IF proceed-branch → read the source/research and perform the edit.

Sub-scope gating (a second axis) is layered the same way — e.g. items tagged "(scope X only)" are additionally gated on a scope field in the decision artifact, and skipped under the other scope with a distinct "Skipped: scope = ..." note.

### L6 Aggregation item — lines 799-808

Final-in-phase consolidation: `Glob` all `*-review.md` (or test-result) files, read each, write a consolidated report to `phase-outputs/reports/`. Discover files dynamically; do not hardcode lists.

---

## 5. QA-gate / validation / test item encoding

### I15-I16 Phase-gate QA (lines 599-624) + M1 composite (lines 843-851)

A phase-gate QA checkpoint is a **2-3 item sequence** between phases:

1. **Aggregation (L6):** collect preceding-phase outputs into one summary/inventory (Glob-driven).
2. **QA agent spawn:** a self-contained B2 item that spawns `rf-qa` (structural) or `rf-qa-qualitative` (operational), stating: agent name, phase type, input file paths, output report path, verdict handling (proceed on PASS / fix cycle on FAIL), error clause. If qualitative QA is also needed, it's a SEPARATE item immediately after (sequential).
3. **Conditional proceed (L5):** read the QA report; IF PASS proceed; IF FAIL run the bounded fix cycle (max cycles per the I16 table below), re-run QA, re-check.

**I16 fix-cycle caps:** research-gate 3 (HALT+escalate); synthesis-gate 2 (→Open Questions); report-validation 3 (HALT); **task-integrity 2 (→Open Questions)**; any qualitative gate 3 (HALT). Each cycle re-verifies all prior failures + checks for new issues; rising issue count = systemic problem flag.

**M2 applicability (lines 852-860):** code-modifying tasks need a gate after implementation (before/with testing). When in doubt, include a gate. For this durable-fix task the natural gate is a **FINAL task-integrity gate** after validation (matching the prior example's terminal `### Phase Gate: Task-Integrity Quality Verification`).

### I17 Post-completion validation (lines 626-635)

Before status → Done, include items that verify: (1) all `- [ ]` marked `- [x]`; (2) all specified output files exist on disk (Glob); (3) blocker entries have resolution notes; (4) if source code was modified, relevant tests pass. These live in `## Post-Completion Actions` BEFORE the frontmatter-update item.

### I18 Testing requirement for code-modifying tasks (lines 637-646)

Because this task modifies source, it MUST include ≥1 testing item using the **L3 pattern**, specifying: the exact test command, pass criteria, where results are captured, B2 shape.

### Encoding the specific final validation gate this task needs

This task's required final gate is three commands. Encode each as its own **L3 capture item with an inline fix loop** (mirrors the prior example's Phase 6, example lines 306-321):

- **`make lint-architecture`** → run, capture to `phase-outputs/test-results/final-lint-architecture.txt`, ensure exit 0; IF non-zero read violation, fix (import+wrap from contracts, never inline), re-run until 0.
- **`make verify-sync`** → run, capture to `final-verify-sync.txt`, ensure no drift / exit 0. Embed the ABSOLUTE RULE reminder: never `git add` any `.claude/{skills,commands,agents,hooks,templates}` path; only the `src/` side is staged; an `-f` on a `.claude/` path is the violation siren.
- **`uv run pytest -k tool_write`** (the targeted suite for this task) → run, capture raw to `.txt` + structured summary to `.md`, ensure 0 failures; IF a previously-passing test flips to fail, treat as a regression, fix and re-run. Optionally add a parent-baseline delta item (capture baseline in Phase 1 Step 1.4, compare in the final phase) as the prior example does (example lines 149-151 capture baseline; lines 318-320 compute delta).

All commands run UV-only (`uv run ...`; `python -m ...` only when wrapped in `uv run`, the sanctioned exception — example lines 250-252).

---

## 6. Prior example shape reference (TASK-RF-20260602-060714)

This is the closest precedent: investigation → decision → conditional implementation → final validation → terminal QA gate. Phase map:

- **Phase 1 — Preparation & Setup** (example lines 133-151): Step 1.1 status→Doing + Execution Log entry; Step 1.2 verify/create `phase-outputs/` subdirs (folds dir-creation into one item); Step 1.3 git remote/branch hygiene (fork discipline embedded); Step 1.4 read design doc + **capture parent test baseline** into `remediation-index.md` for the later delta.
- **Phase 2 — Investigation/Reproduction (Investigation Gate)** (lines 162-180): L1 current-state confirmation (`grep` probes → `r5-current-state.md`), L3 runtime probe + a built reproduction fixture + `check_signatures` run captured to `test-results/r5-repro-output.txt` and summarized in `r5-reproduction.md`, plus a scoping-determination item that decides the **sub-scope** (`MD-FAMILY-ONLY` vs `MD-FAMILY-PLUS-ALLOWLIST`) → `r5-scope-determination.md`.
- **Phase 3 — Decision Gate** (lines 182-188): a single L5 item that writes `r5-remediation-decision.md` to `phase-outputs/plans/` with frontmatter (`artifact:`, `phase:`, `gate:`, `verdict_source:`, `decision:`) and handles BOTH branches: `decision: CLOSE` (FP absent → document evidence, recommend closing the superseding PR, Phase 4 SKIPPED) vs `decision: PROCEED` (FP reproduced → carry the scope selection + an enumerated carry-forward list of which Phase 4 sub-items apply). **This is the canonical `<topic>-decision.md` pattern for the new task's intentional-vs-drift + family-SoT-location decision.**
- **Phase 4 — Conditional Implementation (Path B)** (lines 190-252): EVERY item opens "Read the R5 decision artifact ...; IF `decision: CLOSE`, mark complete with a `Skipped: R5 decision = CLOSE` note and make NO change; IF `decision: PROCEED`, <edit>". Allowlist-only items add a second gate: "IF scope is `MD-FAMILY-ONLY`, mark complete with a `Skipped: scope = MD-FAMILY-ONLY` note". Ends with L3 test-surface runs (`Step 4.14`) + an arch_lint-stays-green check (`Step 4.15`).
- **Phase 5 — Independent fixes** (lines 254-304): granular self-contained items, each fix paired with its own test item; optional/droppable items explicitly tagged "(OPTIONAL — DROPPABLE)" with skip-note instructions.
- **Phase 6 — Final Validation** (lines 306-321): the three L3 capture-with-fix-loop items — `make lint-architecture` (exit 0), `make verify-sync` (no drift), full targeted `uv run pytest` + parent-baseline delta. **Directly reusable as the new task's `make lint-architecture` / `make verify-sync` / `uv run pytest -k tool_write` gate.**
- **Phase Gate — Task-Integrity QA** (lines 322-336): L6 aggregation (`final-aggregation.md`) → spawn `rf-qa` in `task-integrity` mode with **explicit ADVERSARIAL STANCE + `fix_authorization: true`** → L5 act-on-verdict with the bounded 2-cycle fix loop and HALT-precedence guards (regression check → monotonicity check → hard cap → Open Questions). Matches the memory-noted rf-qa adversarial pattern.
- **Post-Completion Actions** (lines 338-346): (1) Glob-verify outputs exist + git status confirms edits under `src/`/`tests/` with NO `.claude/` staged; (2) final regression run (or "verified in Phase 6"); (3) write `### Task Summary`; (4) flip frontmatter to `🟢 Done` + final Execution Log entry — explicitly the LAST item.
- **Task Log / Notes** (lines 348+): `### Task Summary` filled at completion, then per-phase Findings sections.

### Anti-orphaning (completion items in the final phase)

The four Post-Completion items are the anti-orphaning mechanism: output-existence verification, final test pass, Task Summary, and the terminal frontmatter flip. No completion logic is stranded mid-task; the `🟢 Done` flip is the final checkbox (C4/I13/I17). The decision artifact + per-item skip-notes guarantee that even fully-skipped conditional items are explicitly marked complete (never left orphaned/unchecked) — J2: items are NEVER left unchecked.

---

## 7. Concrete recommendations for the new task (TASK-RF-20260602-162259)

1. **Frontmatter:** id `TASK-RF-20260602-162259`, `task_type: static`, `template_schema_doc` → the 02 template, list the four research files + design doc in `related_docs`.
2. **Omit** WORKFLOW-DEPENDENT sections (no governing stage workflow); add an `## Execution Context` reader-aid block instead, as the prior example does.
3. **Handoff dir:** `.dev/tasks/to-do/TASK-RF-20260602-162259/phase-outputs/` with the 5 subdirs.
4. **Phase 1:** status flip + dir create + (git hygiene if it touches src) + read research/design + capture test baseline for the final delta.
5. **Investigation phase (L1+L3):** probe the live tree for the intentional-vs-drift signal and the family-SoT location; write evidence to `discovery/` and `test-results/`.
6. **Decision gate (L5, single item):** write `<topic>-decision.md` to `plans/` with a `decision:` field handling BOTH branches (intentional → document/close path; drift → remediate path) AND the family-SoT-location resolution; enumerate the carry-forward implementation items for the proceed branch.
7. **Conditional implementation phase:** every item gated on the decision artifact (skip-note vs edit), edits to `src/superclaude/` only, each code item paired with an L3 test item.
8. **Final validation phase (L3 ×3 with fix loops):** `make lint-architecture` (exit 0), `make verify-sync` (no drift, never stage `.claude/`), `uv run pytest -k tool_write` (0 failures + baseline delta).
9. **Terminal task-integrity QA gate:** L6 aggregation → adversarial `rf-qa` spawn (`fix_authorization: true`) → L5 bounded 2-cycle fix loop with HALT guards.
10. **Post-Completion:** Glob output-existence + git no-`.claude`-staged check; final regression; Task Summary; frontmatter→Done as the last checkbox.

---

**Status: Complete**

**Summary:** The 02 complex-task template (PART 1 rules lines 1-888, PART 2 skeleton lines 890-1205) requires the frontmatter schema in §1, the body section order in §2, and self-contained single-paragraph `- [ ]` items carrying all 6 B2 elements (§3) with verification embedded via `ensuring ...` (never a separate item). The decision gate is the **L5 Conditional-Action pattern** (template lines 785-797): one always-written decision artifact in `phase-outputs/plans/` that handles BOTH branches and gates every downstream item, which open by reading the artifact and either skip-with-note or edit (§4). QA/validation/test items are encoded as the I15-I16/M1 phase-gate sequence (aggregate → rf-qa spawn → L5 conditional proceed with bounded fix cycles, task-integrity cap = 2) plus I17 post-completion validation and I18 L3 testing items; the three required gates (`make lint-architecture`, `make verify-sync`, `uv run pytest -k tool_write`) each become an L3 capture-with-fix-loop item (§5). The prior example TASK-RF-20260602-060714 (`/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260602-060714/TASK-RF-20260602-060714.md`) is a direct precedent: Phase 2 investigation/reproduction → Phase 3 `r5-remediation-decision.md` decision gate (CLOSE vs PROCEED + sub-scope) → Phase 4 fully-gated conditional implementation → Phase 6 three-command final validation → terminal adversarial task-integrity QA gate → anti-orphaning Post-Completion items ending in the `🟢 Done` flip (§6). Concrete build recommendations in §7.
