# Research: MDTM Template 02 & Examples

**Status:** Complete
**Date:** 2026-06-18

**Template file (single source of truth):** `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (Template 02 = complex task; extends Template 01 with **Section L: Intra-Task Handoff Patterns**). Use Template 02 for the swarm-tui wiring task because it has discovery → build → test → verify phases.

Structure: file is two parts. **PART 1 (lines 61–1127)** = task-building instructions (HTML-commented, never copied into output). **PART 2 (lines 1143+)** = the actual task-file skeleton to instantiate.

---

## SECTION A — Core Principles (PART 1, lines 85–145)

- **A3. Complete Granular Breakdown** (lines 108–112): Break EVERY phase into atomic, verifiable checklist items. One checklist item per file / component / iteration. NO bulk/high-level operations. Include exact file paths, specific requirements, measurable outcomes. → For swarm-tui: one item per edit site (commands.py flag add, helper add, each test).
- **A4. Iterative Process Structure** (lines 114–133): For ANY multi-item process: (1) pre-enumerate ALL items in an initial step, (2) one checklist item per specific item, (3) require incremental updates, (4) a consolidation step ONLY after all items complete. Canonical pattern:
  - `**Step X.1:** Scan and enumerate all [items]` → `- [ ] Complete listing generated: [count] identified`
  - `**Step X.2:** Process each individually` → one `- [ ]` per item
  - `**Step X.3:** Consolidate` → `- [ ] All [count] items processed` + `- [ ] Consolidated output created`
- A1/A2/A5/A6 are WORKFLOW-DEPENDENT — omit if no governing workflow docs (`.gfdoc/workflows/` etc.). This project has none for ad-hoc tasks, so omit workflow-compliance sections.

## SECTION B — Self-Contained Checklist Items (CRITICAL) (PART 1, lines 147–213)

- **B1** (session-rollover protection): items execute across multiple sessions/batches; context loaded in batch 1 is GONE by batch 3. So every item must be self-contained. Standalone "read context" items are USELESS.
- **B2. Every checklist item MUST be a complete self-contained prompt with these 6 elements** (lines 159–165):
  1. **Context Reference with WHY** — what file(s) to read and why needed for THIS action
  2. **Action with WHY** — what to do and why
  3. **Output Specification** — exact output file name, location, content, template (if any)
  4. **Integrated Verification** — an "ensuring..." clause; DO NOT assume/hallucinate; 100% derived from source files; document negative evidence on failure
  5. **Evidence on Failure Only** — log to task notes ONLY on blocker/error; success is evidenced by the output file itself
  6. **Explicit Completion Gate** — verbatim: "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
- **B3** Each item = ONE FULL PARAGRAPH (not bullets/multi-line), verbose, reads like a standalone prompt.
- **B4** Correct example: read spec → read pattern file → create file → "ensuring..." clause → failure-log instruction → "Once done, mark this item as complete." (no separate verification item).
- **B5 FORBIDDEN**: standalone "read context" items; missing context reference; multi-line/bulleted items; separate verification/confirmation items; overly granular items ("create directory" alone); separate REMINDER blocks.
- **B7** Verification is embedded via "ensuring..." clause; QA process handles verification between batches (see I15-I16). Do NOT create separate verification items.

## SECTION C — Embedding Requirements (PART 1, lines 215–247)

Outputs (C1), Success Criteria (C2), Verification (C3) are EMBEDDED in checklist items, NEVER separate sections. C4: Task completion is handled only by the **## Post-Completion Actions** section (frontmatter update + execution-log entry). Do NOT add "Outputs & Deliverables", "Success Criteria", "Verification Checklist", or "Task Completion and Handoff Protocol" sections.

## SECTION D — Mandatory Task Sections (PART 1, lines 249–289)

- D1/D2 are WORKFLOW-DEPENDENT (Workflow Compliance Declaration, Cross-Stage Integration) — omit when no workflow docs.
- **D3 CRITICAL RULE**: NO checklist items may appear before Phase 1 begins. Order: Frontmatter → (Workflow Compliance informational) → Prerequisites (informational) → Phase 1 (first executable `- [ ]`). All context-review / input-reading items live IN Phase 1 (Steps 1.2–1.4).

## SECTION E — Checklist Structure Rules (PART 1, lines 291–399)

- **E1**: every actionable item is `- [ ] Action text`; FLAT structure only — no nested checkboxes, no parent checkboxes summarizing children. Use `**Step X.Y:**` bold headers for grouping, not checkboxes. Items in exact completion order.
- **E2**: summary/parent checkboxes come AFTER their component items, never before. Use headers (no checkbox) to group, then individual `- [ ]` items.
- **E3 Sequential order**: flow ALWAYS top→bottom. FORBIDDEN: "mark item complete in section above", "see checklist below", "return to phase and mark complete", any backward movement.
- **E4**: never put checkboxes next to step numbers (step numbers = bold headers); no separate REMINDER blocks between items (workers see only their batch items) — fold reminders INTO the item text.

## SECTION I — Additional Guidelines (selected, PART 1, lines 510–841)

- **I1** Directive language: "YOU MUST" / "DO NOT" (no passive voice).
- **I2** Extreme granularity: exact file paths, not directories.
- **I3** Incremental modification: "DO NOT attempt to complete entire files at once".
- **I4** Parent-task relationships in frontmatter (`parent_task`, `depends_on`).
- **I6** `task_type: static` (fixed content) vs `dynamic` (runtime-discovered items use `<!-- DYNAMIC CONTENT START/END: [purpose] -->` markers between a Step header and its items). For swarm-tui the edit sites are known → `static`.
- **I11** First action of the task = status update to "🟠 Doing" (Phase 1, Step 1.1).
- **I12** Verification integrated via "ensuring..." clause — never separate verify items.
- **I13** Every task MUST have a `## Post-Completion Actions` section (frontmatter update + Execution Log entry).
- **I15 Phase-gate QA enforcement**: every task with 2+ execution phases MUST have ≥1 phase-gate QA checkpoint between the primary execution phase and any dependent later phase. Every gate step (each lens spawn, consolidation, fix agent, each verification agent) MUST be an explicit `- [ ]` item — "No QA is implicit. No QA lives only in prose."
- **I16** QA verdict: consolidated verdict is FAIL if ANY agent reports ANY issue of any severity. Fix cycles follow I20 serialized protocol; max cycles per gate-type (3 for most, 2 for synthesis/task-integrity), then HALT + escalate.
- **I17 Post-completion validation**: before status→Done, run final-state lens-based QA per M3 (item 5) — IN ADDITION to phase-gate QA. These items appear in `## Post-Completion Actions` BEFORE the frontmatter-update item.
- **I19 Lens-based QA minimum agents (FULL intensity floors)**: every gate spawns multiple agents, each one lens. Single/dual-agent QA PROHIBITED. Floors: FINAL/assembled-output gate ≥ 6 agents (3 rf-qa structural + 3 rf-qa-qualitative content); INTERMEDIATE gate (research-gate/synthesis-gate/task-integrity) ≥ 5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative). Each lens agent gets its own prompt/report/checklist + adversarial framing: **"Assume this document has at least N errors focused on [lens]. Find them."** (N: 5 for <500 lines, 10 for 500–1500, 15 for 1500–3000, 20 for >3000). **I22 scales these down**: lite = 2 agents total / standard = 3 / full = I19 floors.
- **I20 Serialized fix authorization**: any gate with 3+ agents on the same file MUST serialize fixes. (1) all lens agents report with `fix_authorization: false`; (2) consolidate to `${TASK_DIR}qa/qa-consolidated-findings.md`; (3) ONE fix agent applies ALL fixes with `fix_authorization: true`; (4) verification round (≥2 agents, `fix_authorization: false`). Parallel fix authorization is PROHIBITED ("Agent A fixes line 50 one way, Agent B another").

## SECTION M — Phase-Gate Composite Patterns (PART 1, lines 1029–1121)

- **M1 is DEPRECATED** (single-agent QA). New task files MUST use **M3**.
- **M3 Lens-Based QA Sequence** — the mandatory 8-step gate, EACH step an explicit `- [ ]` item (orchestrator MUST NOT collapse steps):
  1. Aggregation (L6) → summary/inventory file
  2. Structural lens agents (rf-qa, PARALLEL, `fix_authorization: false`) → `${TASK_DIR}qa/qa-structural-[lens]-report.md`
  3. Content lens agents (rf-qa-qualitative, PARALLEL, `fix_authorization: false`) → `${TASK_DIR}qa/qa-content-[lens]-report.md`
  4. Domain-specific lens agents (if any, PARALLEL)
  5. Findings consolidation → `${TASK_DIR}qa/qa-consolidated-findings.md` (deduplicated, severity CRITICAL/IMPORTANT/MINOR + originating lens)
  6. ONE fix agent (`fix_authorization: true`)
  7. Verification round (≥2 agents, PARALLEL, `fix_authorization: false`) → `qa-verification-structural-report.md` + `qa-verification-content-report.md`
  8. Conditional proceed (L5): both PASS → proceed; else repeat 5–7 (max cycles per I16, then HALT).
  - Standard structural lenses: template-conformance, internal-consistency, evidence-quality, completeness. Standard content lenses: actionability, numbers-metrics, crossref-chain, domain-accuracy.
- **M4 Source-Document Fidelity Gate** — runs AFTER M3; only required if the output was DERIVED FROM source documents (I21). For swarm-tui (code wiring, not doc-from-spec), the fidelity gate is generally NOT applicable — note "Fidelity gate not applicable — code change, no consumed source documents" if omitted.

## SECTION L — Intra-Task Handoff Patterns (the L1–L6 item types)

These are the building blocks for the discovery/build/test/verify phases (PART 1 lines 902–1027; summarized in PART 2 lines 1263–1272):
- **L1 Discovery** — Glob/Read to explore, write findings to `phase-outputs/discovery/`.
- **L2 Build-from-discovery** — read a discovery inventory + source, create the deliverable.
- **L3 Test/execute** — run a command (Bash), capture raw output + structured summary to `phase-outputs/test-results/`.
- **L4 Review/QA** — assess one output, write a verdict file to `phase-outputs/reviews/`.
- **L5 Conditional-action** — branch on a prior result (IF PASSED … / IF FAILED …).
- **L6 Aggregation** — Glob to consolidate many outputs into a report in `phase-outputs/reports/`.
- Recommended phase recipes (lines 1017–1023): code+test phase pattern and full pattern documented at PART 1 lines 1017–1023 (`build -> run tests -> conditional fix-or-proceed`; full `discover -> build -> test -> conditional -> review -> aggregate`).

---

## PART 2 — Task-File Skeleton (the structure the generated file MUST have)

The generated task file copies PART 2 (PART 1 lines 1143+; HTML-comment orchestrator blocks are REMOVED from output). Exact top-level sections, in order:

1. **YAML frontmatter** (template lines 1–60). Notable required fields:
   - `id` (`TASK-RF-...`), `title`, `description`, `version`, `status` (start `"🟡 To Do"`), `type` (use `"🧩 Integration"` or `"✨ Feature"` for swarm-tui wiring), `priority`, `created_date`, `updated_date`, `assigned_to`, `autogen`, `autogen_method`, `coordinator: orchestrator`, `parent_doc`, `parent_task`, `depends_on:` (list).
   - `spec_path: ""` — driving spec/PRD/TDD; populated by task-builder (A.2); empty if none.
   - `reflect_pre:` block — `verdict / coverage_pct / depth / tcs / run_id / report / reviewed_at` (PRE reflect-gate sign-off; builder populates at A.10.7).
   - `reflect_post: ""` — POST reflect verdict; recorded by the executor after the final-phase reflect wrapper runs.
   - `related_docs:`, `related_prd`, `related_tdd`, `tags:`, `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info:`, `task_type: static`.
2. `# [Task Title]`
3. `## Task Overview`
4. `## Key Objectives` (numbered, concrete outcomes)
5. `## Prerequisites & Dependencies` — INFORMATIONAL ONLY, no checkboxes. Sub-sections `### Parent Task & Dependencies`, `### Previous Stage Outputs (MANDATORY INPUTS)`.
6. **`## Execution Context`** (template lines 1193–1231) — builder MUST populate. Required sub-headers (quote exactly): `### References`, `### Source Areas`, `### Key Constraints`, `### Handoff File Convention`, `### Frontmatter Update Protocol`.
7. `## Detailed Task Instructions` containing the phases:
   - **`### Phase 1: Preparation and Setup`** — Step 1.1 status update item (`- [ ] Update status to "🟠 Doing" ...` + Execution Log entry), Step 1.2 create `phase-outputs/` dirs. Per **D3** this is the FIRST place `- [ ]` items may appear.
   - **`### Phase 2: [Main Execution]`** + further phases (discovery/build/test/verify), each with `**Step X.Y:**` headers + self-contained `- [ ]` items, with an `<!-- ORCHESTRATOR: insert lens-based QA gate per M3 -->` boundary where a later phase depends on an earlier phase's output.
8. **`## Post-Completion Actions`** — output-existence verification item, test-suite regression item, (MANDATORY per I17) post-completion lens-based QA per M3, optional M4 fidelity gate, **POST reflect-gate item (penultimate)**, `### Task Summary` creation item, then final frontmatter→Done item.
9. **`## Task Log / Notes 📋`** — `### Task Summary`, `### Execution Log`, one `### Phase N - [Name] Findings` per phase (the blocker-log targets every item references), plus `### Phase Gate Findings` / `### Follow-Up Items Identified`.

### Anti-orphaning rule (CRITICAL for builder)

Per **D3 / E1-E3 / C4**: task-completion items (frontmatter status→Done, completion_date, Execution Log entry, Task Summary) live ONLY inside the final `## Post-Completion Actions` section, as the LAST items, AFTER all QA/validation/reflect items. NEVER place a "mark done" or summary checkbox before its component work — summaries always come last (E2). Every `- [ ]` blocker-log reference must point to a `### Phase N Findings` heading that actually EXISTS in `## Task Log / Notes`. No checklist item before Phase 1 (D3).

---

## Prior Complex-Task Examples (effective patterns observed)

Browsed `/config/workspace/IronClaude/.dev/tasks/done/` (75 task folders). Two are directly relevant to a CLI-flag-wiring + helper + tests task:

### Example A — `TASK-RF-pr167-verdict-regex-20260613-000000` (BEST MATCH: code+test+UV-validate+reflect, no QA fan-out)

Path: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-pr167-verdict-regex-20260613-000000/TASK-RF-pr167-verdict-regex-20260613-000000.md`. Phase layout that maps onto swarm-tui Approach A:
- **Phase 1: Preparation and Status Update** — single status-update item.
- **Phase 2: Implement Source and Test Changes** — item 1 edits the source file (`gates.py`, with a precise "change X while keeping Y intact, ensuring `accepts A,B,C` and `rejects D,E,F`" scope clause); item 2 adds narrowly-scoped regression tests to the test file. Each item embeds absolute paths + cites the research artifacts.
- **Phase 3: UV Validation and Git Scope Check** — separate L3 items: targeted pytest (`uv run pytest <path>::<Class> -q`), broader pytest, `uv run ruff check <files>`, `uv run ruff format --check <files>`, then a `git status --short` + `git diff -- <files>` scope-check item that does NOT stage/commit/push. Each validation item has a "if it fails, fix only <these files>, rerun the same command" loop folded in.
- **Post-Completion Actions** — (1) Task Summary item; (2) **POST reflect-gate item (penultimate)**; (3) final status→Done item.
- Every item ends with the verbatim completion gate and carries an inline `<!-- evidence-absence: ... -->` comment.
- This task explicitly **waived M3 phase-gate QA fan-out** via `QA_GATE_REQUIREMENTS: NONE` (line 135) because validation is carried by targeted pytest + ruff + git-scope + POST reflect. Useful precedent: a tightly-scoped code change MAY rely on UV validation + reflect instead of a 6-agent lens gate, IF the builder records that decision.

### Example B — `TASK-RF-20260604-102137` (code-modifying with adversarial rf-qa gates)

Path: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md`. Uses L1 discovery → L2 build → L3 validate → L4/L6 QA. Its QA gates are **single rf-qa items with ADVERSARIAL STANCE framing** (not full 6-agent M3): e.g. a discovery-gate item "spawn `rf-qa` with `QA_MODE: research-gate`, `fix_authorization: false`, ADVERSARIAL STANCE prompt, write verdict file with `VERDICT: PASS|FAIL`, on FAIL fix + re-run up to 3 cycles following **regression → monotonicity → hard-cap → proceed** ordering"; and a final task-integrity gate with `QA_MODE: task-integrity`, `fix_authorization: true`, prompt prefix "`ADVERSARIAL STANCE: Assume the work contains errors...`", up to 2 cycles. This is the leaner real-world QA shape for code tasks; the I19 6-agent floor is the FULL-intensity ceiling, scaled down by I22.

---

## POST Reflect-Gate Item — exact shape (the penultimate Post-Completion item)

NOTE: this item is NOT in the template's PART 2 Post-Completion skeleton — the template only carries `reflect_post`/`reflect_pre` frontmatter. The reflect-gate ITEM shape comes from task-builder convention (verified live in Example A, line 205). Reproduce this shape for swarm-tui (it has NO `spec_path`, so PRE reflect is skipped and POST reflect is required). The flat wrapper shell-out, behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard:

```
if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect wrapper already active; skipping nested reflect"; exit 0; else superclaude reflect run <ABSOLUTE_TASK_FILE_PATH> --depth deep --fix --promote; fi
```

Required semantics encoded in the item (per Example A): run from the worktree/repo root; the wrapper consumes its own exit code and writes `reflect_post` back to this task file's frontmatter; ONLY exit code `0` permits the final status→Done item to proceed; exit `10/11/2`/any non-zero → read the wrapper report, summarize the blocker in `### Phase Gate Findings` / `### Follow-Up Items Identified`, set status `🔴 Blocked`, do NOT proceed to Done. Explicit prohibitions in the item: must NOT run `/sc:reflect`, must NOT use a `<base>..HEAD` range, must NOT spawn a reflect subagent, must NOT stage/commit/push, must NOT edit `.claude/` mirrors, must NOT do PR/GitHub actions.

(Cross-ref memory: `reference_reflect_exit11_degraded_benign.md` — exit 11 "degraded" can be benign; judge by `return-contract.yaml` status, not exit code. But the task-file item, per Example A, gates strictly on exit 0; the builder should mirror Example A's strict gate unless told otherwise.)

---

- Original recipe note: code+test phase = `K1/K2 (build) -> L3 (run tests) -> L5 (conditional fix-or-proceed)`; full = `L1 -> L2 -> L3 -> L5 -> L4 -> L6`.

---

## REQUIRED-SECTIONS CHECKLIST (the builder must satisfy all of these)

The generated swarm-tui task file MUST contain, in this order:

- [ ] **YAML frontmatter** with all template fields; `task_type: static`; `spec_path: ""` (no spec → PRE reflect skipped); `reflect_post: ""`; `type` = Integration/Feature; `status: "🟡 To Do"`.
- [ ] `# <Task Title>`
- [ ] `## Task Overview`
- [ ] `## Key Objectives` (numbered, concrete — each coupled FR is an objective)
- [ ] `## Prerequisites & Dependencies` (informational; `### Parent Task & Dependencies`, `### Previous Stage Outputs (MANDATORY INPUTS)`) — NO checkboxes
- [ ] `## Execution Context` with all five sub-headers: `### References`, `### Source Areas`, `### Key Constraints`, `### Handoff File Convention`, `### Frontmatter Update Protocol` — all populated, no `[placeholder]` left
- [ ] `## Detailed Task Instructions`
  - [ ] `### Phase 1: Preparation and Setup` (Step 1.1 status→Doing item; Step 1.2 create `phase-outputs/{discovery,test-results,reviews,plans,reports}/`) — FIRST `- [ ]` items (D3)
  - [ ] `### Phase 2: Discovery` (L1 — enumerate `--tui` wiring sites in `commands.py`, the swarm reader/TUI launcher seam; write inventory to `phase-outputs/discovery/`)
  - [ ] `### Phase 3: Build` (L2 — add the `--tui` flag to `swarm run` in commands.py; add/wire the TUI-launch helper; each coupled FR a separate self-contained item with a non-negotiable "ensuring ... accepts/rejects ... while X intact" gate)
  - [ ] `### Phase 4: Test` (L3 — add tests for the flag + helper; `uv run pytest <path> -q`; then broader pytest; `uv run ruff check`; `uv run ruff format --check`; git-scope check; conditional L5 fix-or-proceed)
  - [ ] phase-gate QA boundary between build and any dependent later phase (M3/I15) — OR an explicit `QA_GATE_REQUIREMENTS: NONE` waiver note in Execution Context (Example A precedent) if validation rests on UV + reflect
- [ ] `## Post-Completion Actions` (in order): output-existence verification item; test-regression item; post-completion lens-based QA per M3/I17 (or documented waiver); M4 fidelity gate item (or "not applicable — code change" note); **POST reflect-gate item (penultimate)** with the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` guard + `superclaude reflect run <task-file> --depth deep --fix --promote`, exit-0-only gate; `### Task Summary` creation item; final frontmatter→`🟢 Done` item
- [ ] `## Task Log / Notes 📋` with `### Task Summary`, `### Execution Log`, one `### Phase N - <Name> Findings` per phase (every blocker-log reference must resolve to a real heading), `### Phase Gate Findings`, `### Follow-Up Items Identified`

Per-item invariants (apply to EVERY `- [ ]`):
- [ ] Single paragraph (B3), self-contained (B2 six elements), flat — no nested/parent checkboxes (E1)
- [ ] Context reference + WHY, Action + WHY, exact output path, integrated "ensuring..." verification clause (no separate verify items — I12/C3), failure-log-only instruction pointing at the matching `### Phase N Findings`, and the verbatim completion gate: "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
- [ ] Exact absolute file paths; UV-only commands (`uv run ...`, never `python -m`/`pip`); no `.claude/` staging; no commit/push/PR unless explicitly authorized
- [ ] Top→bottom only; summaries/completion items last (E2/E3); no checklist item before Phase 1 (D3)
