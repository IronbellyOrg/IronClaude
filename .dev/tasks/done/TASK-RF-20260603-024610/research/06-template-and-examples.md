# R6 — Template & Examples (MDTM Template-02 structure for Sprint CLI wiring)

**Status: Complete**

Research agent R6 owns TEMPLATE STRUCTURE + formatting examples. R1–R5 own the codebase.

## Summary

- **Template path correction confirmed:** real template = `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (85,583 bytes); `.claude/templates/workflow/` does **not** exist in this repo (Section 0). Set `template_schema_doc` to the `src/...` path, not `.claude/...`.
- **Template-02 fully documented (Section 1):** required frontmatter (1a), PART-2 mandatory section ordering (1b), the B2 6-element self-contained item pattern (1c), rules A3/A4 (1d), L1–L6 handoff + M1 phase-gate + F2 subagent discipline (1e), and the template's own FORBIDDEN/INCORRECT pitfalls (1f) — all with line citations.
- **Concrete example (Section 2):** `TASK-RF-OVM-VERIFICATION-GAP-CLOSURE-20260531-040500` (found in `.dev/tasks/to-do/`, not `done/`) — a 5-phase, code-modifying, QA-gate-per-phase task. Shows as-shipped frontmatter, section ordering with an `## Execution Context` block, a real B2 item (Step 2.1, line 179), and the M1 QA-gate item encoding (rf-qa structural per phase + rf-qa-qualitative final; I16 fix-cycle ceilings; I17 Post-Completion PC.1–PC.4).
- **TB-Add-1..8 gates (Section 3):** authoritatively cited from `src/superclaude/skills/task-builder/SKILL.md` L1165–1173 / L1972–1979, with a per-gate table and the critical TB-Add-7/8 ↔ `## Execution Context` interaction (header = area names with NO paths per NFR-CONV.3 grep guard; items = full file:line citations). Plus a pre-write self-check mapping to template rules D3/E1–E4/I15/I17/I18.

**Output file:** `.dev/tasks/to-do/TASK-RF-20260603-024610/research/06-template-and-examples.md`

---

## 0. Path correction (IMPORTANT)

The brief warned, and this is confirmed by direct `ls`:

- **CORRECT (exists):** `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (85,583 bytes, 1199+ lines).
- **DEAD (does NOT exist):** `.claude/templates/workflow/` — `ls` returns "No such file or directory". The `.claude/` mirror in this repo does **not** include `templates/`. Any task-file reference that points a worker at `.claude/templates/workflow/02_...` will break. Use the `src/superclaude/templates/workflow/...` path.
- Note: the template's OWN internal example text (C1, line 209) references `.claude/templates/workflow/api-template.md` as an illustrative path. That is a placeholder in the template's examples — not a real file. Builders must rewrite such paths to real `src/superclaude/templates/...` locations or to actual project source.

Companion templates in the same dir: `01_mdtm_template_generic_task.md` (simple tasks, no handoff), `02_...` (complex/handoff — THIS one), `05_prd_template.md`, `99_..._old.md` (deprecated). Rule I8/B-WHEN: use 02 only when items depend on each other via handoff artifacts; otherwise 01.

---

## 1. Template-02 structure (PART 1 instructions, fully read)

The template is split by a giant comment banner into **PART 1** (lines 46–888, orchestrator-only build instructions, NOT emitted to the output file) and **PART 2** (lines 890–end, the literal task-file skeleton you copy and fill). The YAML frontmatter at the very top (lines 1–44) is ALSO part of PART 2.

### 1a. Required frontmatter fields (lines 1–44)

```yaml
id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"   # e.g. TASK-RF-SPRINTCLI-20260603-024610
title: "[Clear, Action-Oriented Task Title]"
description: "[what + purpose within larger workflow]"
status: "🟡 To Do"        # lifecycle: 🟡 To Do → 🟠 Doing → 🟢 Done (⚪ Blocked)
type: "📝 Documentation"  # adjust to task domain
priority: "🔼 High"
created_date / updated_date: "YYYY-MM-DD"
assigned_to: "[agent-name]"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: "[PARENT-TASK-ID]"
depends_on: [list]
related_docs: [ {path, description}, ... ]   # parent workflow + process + related docs
tags: [list]
template_schema_doc: ""
estimation / sprint / due_date / start_date / completion_date / blocker_reason: ""
ai_model / model_settings: ""
review_info: { last_reviewed_by, last_review_date, next_review_date }
task_type: static          # "static" for fixed content, "dynamic" if items added during run (I6)
```

Frontmatter update protocol (F5 / PART2 lines 943–952): set `status: 🟠 Doing` + `start_date` as FIRST action (I11); `status: 🟢 Done` + `completion_date` at end; `⚪ Blocked` + `blocker_reason` only if ALL remaining items blocked (J3); bump `updated_date` each session.

### 1b. Required / mandatory output sections (PART 2 ordering)

The clean task file (what the builder emits) has this exact top-to-bottom order:

1. `# [Task Title]`
2. `## Task Overview`
3. `## Key Objectives` (numbered, bold, concrete outcomes)
4. `## Prerequisites & Dependencies` → `### Parent Task & Dependencies`, `### Previous Stage Outputs (MANDATORY INPUTS)` (INFORMATIONAL ONLY — no checklist items), `### Handoff File Convention`, `### Frontmatter Update Protocol`
5. `## Detailed Task Instructions` (contains the orchestrator instruction block to DELETE from output, then the phases)
6. `### Phase 1: Preparation and Setup` — Step 1.1 status update, Step 1.2 create handoff dirs, etc.
7. `### Phase 2: [Main Execution Phase Name]` — the real work (L-patterns)
8. `### Phase Gate: Quality Verification` — QA-gate spawn item (omit if no gate needed)
9. `### Phase [N]: Testing & Verification` — only if code-modifying (I18)
10. `### Phase 3: [Review and Quality Assessment]` — L4 review + L6 aggregate
11. `## Post-Completion Actions` — 4 items: Glob-verify outputs exist, run tests if code-modified, write Task Summary, flip frontmatter to Done
12. `## Task Log / Notes 📋` — `### Task Summary`, `### Execution Log`, `### Phase N Findings` (one per phase, hold blocker entries), `### Phase Gate Findings`, `### Follow-Up Items Identified`, `### Deviations from Process`

**Section D3 CRITICAL RULE (lines 269–273):** NO checklist items may appear before Phase 1. Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (first executable checkboxes). All "read context / read previous-stage outputs" items live IN Phase 1 (Steps 1.2–1.4), never as standalone preamble items.

### 1c. The B2 self-contained item pattern (the core rule)

Section B (lines 130–197). **Every** checklist item is ONE verbose paragraph (B3) that reads as an independent prompt, because Rigorflow executes in batches across session rollovers and context from batch 1 is gone by batch 3 (B1). The 6 required elements (B2, lines 142–148):

1. **Context Reference with WHY** — which file(s) to read and why this context is needed for THIS action.
2. **Action with WHY** — what to do with that context and why.
3. **Output Specification** — exact output file name + location + content + template to follow.
4. **Integrated Verification** — an "ensuring…" clause (no assume/hallucinate; 100% source-derived; document negative evidence on failure). NOT a separate item (C3, I12).
5. **Evidence on Failure Only** — log a blocker to `### Phase [N] Findings` ONLY if blocked; the output file itself is the success evidence.
6. **Explicit Completion Gate** — literal closing sentence: *"…then mark this item complete. Once done, mark this item as complete."*

Canonical correct example: PART1 B4 (line 157) and PART2 L1/L2 examples (lines 1001, 1006).

**B5 FORBIDDEN patterns (lines 164–184):** standalone "read context and log findings" items (no actionable output → useless after rollover); items with no context reference / source of truth; multi-line or bulleted items (must be a single paragraph); separate verification/confirmation items; over-granular items ("create directory" alone — fold it into the file-creation item); separate REMINDER blocks between items (workers only see batch items, E4 line 371).

### 1d. Rules A3 (Complete Granular Breakdown) and A4 (Iterative Process Structure)

- **A3 (lines 91–95):** break EVERY phase into atomic verifiable checkbox items; one checklist item per file/component/iteration; NO bulk/high-level operations; exact paths + measurable outcomes. Reinforced by I2 (Extreme Granularity).
- **A4 (lines 97–116):** for any multi-item process — (Step X.1) pre-enumerate ALL items in an initial scan item; (Step X.2) one self-contained item per enumerated item; (Step X.3) a consolidation/aggregation item AFTER all individuals. The orchestrator (not the worker) must enumerate up front — K2 (lines 691–708) says the worker MUST NEVER dynamically add items.

### 1e. L1–L6 handoff / subagent patterns (Section L, lines 710–836)

Handoff mechanism: items write artifacts to `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`; these persist across batches so later items just read them by path (lines 718–730).

| Pattern | Purpose | Output dir | Key rule |
|---|---|---|---|
| **L1 Discovery** (737) | explore codebase/env, write structured findings | `discovery/` | the discovery file IS the deliverable; machine-readable table + summary count |
| **L2 Build-from-Discovery** (749) | build output from a prior discovery file | (real dest) | reference BOTH discovery file path AND source file path |
| **L3 Test/Execute** (761) | run cmd/test, capture results | `test-results/` | capture BOTH raw output (`.txt`) AND a structured `.md` summary |
| **L4 Review/QA** (773) | assess a prior output vs source | `reviews/` | produce structured PASS/FAIL verdict + per-criterion checklist; never "looks good" |
| **L5 Conditional-Action** (785) | branch on a prior result file | `plans/` | MUST handle BOTH PASS and FAIL branches; output file created either way |
| **L6 Aggregation** (799) | consolidate many outputs into one report | `reports/` | use Glob to discover files dynamically (don't hardcode lists) |

L7 (811) pattern-selection guide + common phase structures (Discovery→Build→Review; Build→Test→Fix; Full Lifecycle; Full Lifecycle **with M1 QA gates**).

**Subagent / handoff discipline (F2, lines 405–430):** a subagent receives work from a SINGLE checklist item only; never delegate the F1 READ→IDENTIFY→EXECUTE→UPDATE→REPEAT loop itself; never delegate across phase boundaries. **Parallel-spawn exception (line 430):** consecutive items in the SAME phase that spawn INDEPENDENT subagents (no shared reads) MAY be spawned in parallel; each item still marked individually; does NOT apply to data-dependent items.

**M1/M2 phase-gate composite (lines 837–860):** a gate = (Item1 L6 aggregate prior phase outputs) → (Item2 spawn rf-qa structural, optionally then rf-qa-qualitative in a separate sequential item) → (Item3 L5 conditional: PASS→proceed, FAIL→fix-cycle up to I16 max). I15 requires ≥1 gate between the primary execution phase and any dependent later phase. I16 verdict table: research-gate 3 cycles→HALT, synthesis-gate 2→Open Questions, report-validation 3→HALT, **task-integrity 2→Open Questions**, any qualitative 3→HALT. ANY severity (Critical/Important/Minor) = FAIL.

**I17 Post-Completion validation (lines 626–635):** before flipping to Done — all `[ ]` marked `[x]`; all output files exist (Glob); blocker entries have resolution notes; if code modified, tests pass. **I18 (637–646):** code-modifying tasks MUST include ≥1 L3 testing item with explicit command + pass criteria + results-capture path.

### 1f. Common pitfalls (from the template's own FORBIDDEN/INCORRECT blocks)

- Parent checkbox before its children, or a summary checkbox in the middle of a sequence (E2 lines 327–341). Components first, summary LAST; use **headers** (not checkboxes) to group.
- Checkboxes next to step numbers — step numbers are bold headers WITHOUT checkboxes (E4 line 368).
- Backward-movement instructions ("mark item above complete", "see checklist below", "return to phase") — all FORBIDDEN (E3 lines 357–365). Flow is strictly top-to-bottom.
- Nested checkboxes (E1 line 280) — flat structure only.
- Pointing a worker at framework context files (ib_agent_core.md etc.) expecting them to be auto-loaded — they are NOT (G1, line 457); reference the rule file inside the item or use a template that bakes the convention in.
- Referencing the dead `.claude/templates/workflow/` path (Section 0 above).

---

## 2. Concrete real-world example (how real items are formatted)

**Reference example chosen:** `TASK-RF-OVM-VERIFICATION-GAP-CLOSURE-20260531-040500` (the brief named this; it lives in `.dev/tasks/to-do/` not `.dev/tasks/done/` — corrected). Full path: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-OVM-VERIFICATION-GAP-CLOSURE-20260531-040500/TASK-RF-OVM-VERIFICATION-GAP-CLOSURE-20260531-040500.md` (101,943 bytes). It is a STRICT-tier, code-modifying, 5-phase task with a QA gate at every phase boundary — an ideal model for the Sprint CLI wiring task, which is also code-modifying with sync-dev/lint/test gates.

### 2a. Frontmatter as-shipped (lines 1–54)

Matches the template schema exactly. Notables for the builder to copy:
- `id` form: `TASK-RF-OVM-VERIFICATION-GAP-CLOSURE-20260531-040500` (TASK-RF-<slug>-<date>-<time>).
- `type: "🛠️ CI / Test"` (not Documentation) — pick the emoji-type matching the task domain; for Sprint CLI wiring this is code-modifying so `🛠️ CI / Test` or a feature type fits.
- `related_docs` lists the merged proposal/spec AND every `research/NN-*.md` file (lines 16–30) — the builder should list all R1–R6 research files here.
- `estimation: "L"`, `task_type: static`.
- **Drift caveat:** this file's `template_schema_doc` (line 40) points at the dead `.claude/templates/workflow/02_...` path — exactly the bug Section 0 warns about. The Sprint CLI task should set `template_schema_doc: "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md"` instead.

### 2b. Section ordering as-shipped

`# Title` → `## Task Overview` (with a bold "Compliance tier: STRICT" line, lines 60–64) → `## Key Objectives` (8 numbered concrete outcomes, lines 66–75) → `## Prerequisites & Dependencies` (Parent/Depends/Blocks; Previous Stage Outputs INFORMATIONAL; Handoff File Convention; Frontmatter Update Protocol) → **`## Execution Context`** (lines 112–139: "Source areas:" list + "Key constraints:" + "Coupling notes") → `## Detailed Task Instructions` → Phase 1..5 each ending in a Phase Gate → `## Post-Completion Actions` (PC.1–PC.4) → `## Task Log / Notes 📋`.

### 2c. How a real self-contained item is formatted (B2 in practice)

Step 2.1 (line 179) is the model. As one paragraph it chains: **(1) Context+WHY** "Read the R1 inventory file ... Amendment 1 block (lines 56-72) to extract the verbatim current text and replacement text"; **(2) Action+WHY** "then use the Edit tool against `<src path>/SKILL.md` to replace the current `allowed-tools:` line ... because OVM Wave 5.x external-spec verification requires WebFetch and WebSearch"; **(3) Output** the exact edited file; **(4) "ensuring…" verification** "ensuring the resulting line matches the verbatim R1 replacement exactly with no other frontmatter fields modified and the YAML remaining valid"; **(5) failure-only evidence** "If the Edit fails due to multiple matches or the current text not being found verbatim, log the specific blocker ... in the ### Phase 2 - SKILL.md Amendments Findings section"; **(6) completion gate** "then mark this item complete. Once done, mark this item as complete." Every item ends with that exact closing sentence.

### 2d. How phases are ordered + QA-gate items encoded (the model to copy)

Phase structure: **Phase 1** Preparation/Discovery/Branch-setup (Step 1.0 EnterWorktree, 1.1 status flip, 1.2 mkdir handoff dirs, 1.3 L1 discovery, 1.4 branch, 1.5 read sources) → **Phase 1 Gate** → **Phase 2** edits (one item per amendment) + sync → **Phase 2 Gate** → **Phase 3** new files → **Phase 3 Gate** → **Phase 4** CI gates (`make lint`, `make reflect-eval-quick`) → **Phase 4 Gate** → **Phase 5** self-validation + commit → **Phase 5 Gate** → **Post-Completion**.

**QA-gate item encoding (the M1 composite, as-shipped at lines 171, 247, 269, 287, 305):** each gate is a single self-contained item that: names the agent (`rf-qa` for structural / `rf-qa-qualitative` for the final operational review), states the mode (`task-integrity`, `report-validation`, or `qualitative`), lists the exact input files to read, enumerates numbered verification criteria, writes a `phase-N-gate-verdict.md` with binary PASS/FAIL + per-criterion checklist to `phase-outputs/reviews/`, then the L5 conditional: "IF PASS, proceed to Phase N+1. IF FAIL, address findings, re-spawn `rf-qa` in `fix-cycle` mode (max N cycles per I16 <gate-type> ceiling). If N cycles complete without PASS, [Open Questions | HALT and escalate]." and closes with the spawn-failure blocker clause + completion gate. The fix-cycle ceilings match I16 exactly (task-integrity=2→Open Questions, report-validation=3→HALT, qualitative=3→HALT — see lines 131, 171, 287, 305).

**Post-Completion (lines 307–323)** implements I17 literally: PC.1 grep-count unchecked vs checked items; PC.2 Glob-verify every output file exists; PC.3 verify blocker entries have resolution notes; PC.4 flip frontmatter to Done + final Execution Log entry. For a code-modifying task the testing happens in a dedicated phase (here Phase 4 CI gates), satisfying I18.

**Task Log skeleton (lines 325+)**: `### Task Summary`, `### Execution Log`, `### Phase 1..5 Findings` (one per phase), `### Phase Gate Findings`, `### Follow-Up Items Identified`.

---

## 3. TB-Add-1..TB-Add-8 structural-gate checks the generated file must satisfy

These are the rf-qa **task-integrity** gate's structural checks. They are authoritatively defined in the task-builder skill at `src/superclaude/skills/task-builder/SKILL.md` lines 1165–1173 (catalogue) and re-stated as the integrated post-write checklist at lines 1972–1979. The builder must write a task file that passes ALL of them so the rf-qa task-integrity gate returns PASS. (The live ID set is enumerated dynamically from `rf-qa.md` per A.10.5 / INV-010, so K may grow — but TB-Add-1..8 are the current floor.)

| ID | Check (verbatim intent) | What the Sprint CLI task file must do |
|---|---|---|
| **TB-Add-1** | Placeholder scan (SKILL.md L1166) | No `TBD`/`TODO`/`FIXME` token in any item; no title-only items — every item carries the full 5-field self-contained schema. Strip ALL template placeholders like `[path/to/...]`, `TASK-NAME`, `[component]`. |
| **TB-Add-2** | Item-count bounds (L1167) | track ≥3 and ≤40 items; single-track ≥3 and ≤50. Currently **ADVISORY-fail** (won't hard-fail) until ≥10 done-tasks across ≥3 task_types calibrate it — but stay within bounds anyway. |
| **TB-Add-3** | Clarification adjacency (L1168) | Each item blocked on an Open Question references that Open Question **by index** inside its Context field. |
| **TB-Add-4** | Circular-dependency / DAG (L1169) | Item-to-item dependencies must form a DAG — no cycles. Phases flow strictly forward (aligns with template E3). |
| **TB-Add-5** | Granularity / XL splitting (L1170) | Any item flagged complex/multi-file is either split into subtasks OR carries a justifying comment. (E.g., don't bundle 5 CLI-wiring edits into one item; one edit = one item, per A3.) |
| **TB-Add-6** | Verify-prefix / AC-format consistency (L1171) | Uniform `Verify: ...` prefix and consistent `- ✅` / `- [x]` Acceptance-Criteria form across items. |
| **TB-Add-7** | Execution Context source-area reappearance (L1172) | EVERY "Source areas:" entry in the `## Execution Context` block reappears in at least one item's Context field; AND the block itself contains **NO** file:line references. **INACTIVE if no Execution Context block exists.** |
| **TB-Add-8** | Per-item Context evidence binding (L1173) | EVERY item Context field that references a code surface includes a `file:line` citation OR an `<!-- evidence-absence: ... -->` justified-absence comment. (Proves INV-015 scope-confinement: the "no paths in header" rule is confined to the header only.) |

### 3a. How TB-Add-7 and TB-Add-8 interact with the `## Execution Context` block

The block emission rules are at `src/superclaude/skills/task-builder/SKILL.md` lines 926–1009. Key points the builder must honor so TB-Add-7/8 pass:

- The block is emitted **immediately after frontmatter**, before/at the top of the body, when ≥3 distinct source areas are inferable (or when `EXECUTION_CONTEXT_REQUIREMENTS: REQUIRED`). It has exactly three sub-bullets in order: `**References:**` (always present, `R-001:` … verbatim source lines), `**Source areas:**` (named modules, comma-separated; OMIT if <3), `**Key constraints:**` (1–3 verbatim entries; OMIT if none).
- **No-file-paths guard (NFR-CONV.3, L961–969):** the rendered `**Source areas:**` bullet MUST satisfy `grep -cE "src/|/.*:[0-9]+"` == 0. Rewrite `src/superclaude/cli/sprint.py` → "sprint CLI module"; line numbers like `:NN` are forbidden in the header. This is the scope-confinement rule (L982–988) — file:line evidence belongs in **per-item Context fields** and `research/*.md`, never in the header.
- **The trap for the Sprint CLI task:** if you emit a `## Execution Context` block (likely, since R1–R6 give ≥3 source areas: sprint CLI module, pipeline/executor, tasklist loader, etc.), then TB-Add-7 forces every named source area to reappear in ≥1 item Context, and TB-Add-8 forces every code-referencing item Context to carry a real `file:line`. So: **header = area names only (no paths); items = full file:line citations.** Getting this backwards (paths in header, or vague items) fails both gates.
- Degradation (R-038, L990–997): minimal BUILD_REQUEST (GOAL-only) → block degenerates to a single `**References:**` bullet; Source areas + Key constraints absent.

### 3b. Pre-write checklist mapping (builder self-verification before rf-qa)

Beyond TB-Add-1..8, the same gate inherits the template's structural rules; the builder should self-confirm before spawning rf-qa: no checklist items before Phase 1 (D3); flat checkboxes, no parent-before-child / mid-sequence summary (E1/E2); strictly forward flow, no backward-reference language (E3); step numbers are headers without checkboxes (E4); every item ends with the literal "Once done, mark this item as complete." gate (B2.6); a phase-gate exists between the primary execution phase and any dependent later phase (I15); a testing item exists because the task modifies code (I18); Post-Completion items implement I17. Failing any of these surfaces as a task-integrity FAIL (any severity = FAIL, I16).

---
