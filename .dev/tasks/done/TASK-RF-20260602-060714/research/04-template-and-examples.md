# Research: Template & Examples

**Status: In Progress**

Topic: The MDTM complex-task template + prior task-folder examples the builder will follow.
Track goal: remediate validated PR #112 + #111 review findings (investigation/decision gate + conditional implementation).

Primary sources:
- Template: `.claude/templates/workflow/02_mdtm_template_complex_task.md` (1205 lines; PART 1 = build instructions L46-870, PART 2 = task-file template L890-1205)
- Real example (in-flight): `.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` (13 phases, R0/R1 release-scoped, 12 phase gates)
- Decision-output example: `.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-3-proceed-decision.md`

---

## 1. Frontmatter — required fields

Source: template PART 2 frontmatter `02_mdtm_template_complex_task.md:1-44`; real values confirmed in `TASK-RF-20260531-042405.md:1-75`.

Required/expected fields (the builder MUST populate these):
- `id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"` — e.g. `TASK-RF-20260531-042405`. For this task the folder is already `TASK-RF-20260602-060714`, so `id: "TASK-RF-20260602-060714"`.
- `title`, `description` (the example uses a very long single-line description that doubles as a running status log — see `:4` and `last_phase_completed` at `:10`)
- `status: "🟡 To Do"` (set to `🟠 Doing` on start, `🟢 Done` on completion, `⚪ Blocked` if blocked — F5/`:947-952`)
- `type` (emoji-prefixed: `📝 Documentation`, `🔨 Refactor`, etc. — the remediation task should use `🔨 Refactor` like the example `:6`)
- `priority: "🔼 High"`
- `created_date`, `updated_date` (YYYY-MM-DD)
- `assigned_to`, `autogen: false`, `autogen_method: ""`, `coordinator: orchestrator`
- `parent_task`, `depends_on: []`
- `related_docs:` — list of `{path, description}` (the example lists the BUILD-REQUEST, master report, vector analyses, and each research file — `:17-33`). The remediation task should list the PR #112/#111 review findings + the combined `/sc:design` `.md` here.
- `tags:` — list
- `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` (example sets this at `:49`)
- `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`
- `review_info:` (`last_reviewed_by`, `last_review_date`, `next_review_date`)
- `task_type: static` (use `static` for fixed content; `dynamic` only if items are discovered during execution — I6/`:531-532`)

The example also adds optional custom keys (`category`, `phasing`, `preserves`, `inverts`) — these are non-mandatory and task-specific.

## 2. Mandatory PART-2 sections (the body skeleton the builder copies)

Source: template PART 2 `02_mdtm_template_complex_task.md:890-1205`. Section order is fixed — checklist items are FORBIDDEN before Phase 1 (rule D3/`:269-272`). The body skeleton, top to bottom:

1. `# [Task Title]`
2. `## Task Overview` (`:892`) — prose, what + why.
3. `## Key Objectives` (`:896`) — numbered `**[Objective]:** ...` bold list, no checkboxes.
4. `## Prerequisites & Dependencies` (`:904`) with sub-sections:
   - `### Parent Task & Dependencies` (Parent Task / Blocking Dependencies / This task blocks) — informational.
   - `### Previous Stage Outputs (MANDATORY INPUTS)` (`:914`) — **INFORMATIONAL ONLY - NO CHECKLIST ITEMS**; lists `[Output Type]: path - Purpose`. Actual reads happen in Phase 1 Step 1.4.
   - `### Handoff File Convention` (`:928`) — declares `.dev/tasks/TASK-NAME/phase-outputs/` with the 5 subdirs.
   - `### Frontmatter Update Protocol` (`:943`) — the 4 checkpoint rules.
5. `## Detailed Task Instructions` (`:954`) — contains the orchestrator instruction block (removed from output) then the phases.
6. `### Phase 1: Preparation and Setup` (`:1012`) — status update + create handoff dirs.
7. `### Task-Specific Context Files` (`:1052`) — informational reference list; usage is embedded in Phase 2+ items, NOT read separately (G3).
8. `### Phase 2: [Main Execution Phase Name]` (`:1063`) and further phases.
9. `### Phase Gate: Quality Verification` (`:1090`) — QA gate items (or omit if no gate needed).
10. `### Phase [N]: Testing & Verification` (`:1098`) — for code-modifying tasks (I18).
11. `### Phase 3: [Review and Quality Assessment]` (`:1106`).
12. `## Post-Completion Actions` (`:1118`) — see §8.
13. `## Task Log / Notes 📋` (`:1128`) with `### Task Summary` (stub), `### Execution Log`, per-phase `### Phase N - [Name] Findings`, `### Phase Gate Findings`, `### Follow-Up Items Identified`, `### Deviations from Process`.

Sections marked `[WORKFLOW-DEPENDENT]` (A1/`:72-83`) — `## MANDATORY WORKFLOW COMPLIANCE`, `## Cross-Stage Integration Requirements` — are OMITTED when no governing workflow doc exists (this remediation task has none; it derives from PR review findings + the design `.md`). The real example correctly omits the Workflow Compliance H2 block.

## 3. Rules A3, A4, B2 (the load-bearing item-construction rules)

### Rule A3 — Complete Granular Breakdown (`02_mdtm_template_complex_task.md:91-95`)
- Break EVERY phase into atomic, verifiable checklist items.
- One checklist item per file/component/iteration. NO bulk operations.
- Include exact file paths, specific requirements, measurable outcomes.

### Rule A4 — Iterative Process Structure (`:97-116`)
For any multi-item process: pre-enumerate ALL items in an initial step, create one checklist item per item, require incremental updates, add a consolidation step only after all items complete. Pattern:
```
**Step X.1:** Scan and enumerate all [items] in [location]
- [ ] Complete [item] listing generated: [count] items identified
**Step X.2:** Process each [item] individually:
- [ ] [Item 1]: [exact identifier] - [specific action] completed
**Step X.3:** Consolidate all individual results
- [ ] All [count] items processed and results logged
```
The orchestrator (builder) MUST enumerate all items up front; the worker NEVER dynamically adds items (K2/`:694-696`).

### Rule B2 — Self-contained item pattern (`:142-148`)
The single most important rule. Every checklist item is ONE FULL PARAGRAPH (B3/`:150-153`) that is a complete, independently-executable prompt embedding all 6 elements:
1. **Context Reference with WHY** — what file(s) to read and why.
2. **Action with WHY** — what to do and why.
3. **Output Specification** — exact output file name, location, content, template to follow.
4. **Integrated Verification** — an "ensuring..." clause (NO separate verification items; "DO NOT assume, hallucinate, or make up any information"; 100% accuracy from source).
5. **Evidence on Failure Only** — log to task notes ONLY if blocked (the output file itself is success evidence).
6. **Explicit Completion Gate** — literal closing: "If unable to complete due to [...], log the specific blocker using the templated format in the `### Phase [N] ... Findings` section [...], then mark this item complete. Once done, mark this item as complete."

Rationale (B1/`:134-140`): session rollovers between batches mean context loaded early is LOST later — so standalone "read context" items are USELESS.

FORBIDDEN patterns (B5/`:164-183`): standalone "read X and log findings" items; items missing a context reference; multi-line/bulleted items; separate verification/confirmation items; over-granular items ("create directory" alone); REMINDER blocks between items.

Real-world confirmation: every item in `TASK-RF-20260531-042405.md` (e.g. Step 2.1 at `:272`, Step 2.2 at `:276`) is a single dense paragraph that opens with "Read [file] at [path] to [why]...", embeds the action + output path, an "ensuring..." clause, and closes with the exact blocker+completion-gate sentence. Items also inline project guardrails as "REMEMBER:" (e.g. "REMEMBER: UV-only; `src/superclaude/` first" at `:276`).

## 4. Exact item format (checkbox + Step header + 5 embedded fields) and anti-orphaning rule

### Item / Step format
Source: E1/E4 (`:278-292`, `:367-389`).
- Group with bold `**Step X.Y:** [short label]` headers — these are NOT checkboxes (E4/`:368-369`: "NEVER place checkboxes next to step numbers").
- Each actionable item is a flat `- [ ] ...` checkbox. NO nested checkboxes, NO parent checkboxes summarizing children (E1/`:280-281`).
- Real example shape (`TASK-RF-20260531-042405.md:270-272`):
  ```
  **Step 2.1:** Discover all spec-ID extraction sites

  - [ ] Read the R1 file inventory at `...` to identify [...], then [...action...], then write [...output path...] [...ensuring clause...]. If unable to complete [...], log the specific blocker [...] then mark this item complete. Once done, mark this item as complete.
  ```
- The five sub-fields from B2 are NOT separate bullet labels — they are woven into the one paragraph in order (context → action → output → ensuring → blocker/completion-gate). The template's B4 "CORRECT EXAMPLE" at `:155-158` and the FORBIDDEN multi-line form at `:175-180` make this explicit: bolded `**Context:** / **Action:** / **Output:**` line breaks are WRONG.

### Checklist structure rule (components-first, summary-last)
Source: E2 (`:294-348`). Summary/parent checkboxes MUST come AFTER their component items, never before. Use descriptive headers (not parent checkboxes) for grouping. Work flows top→bottom only; never require marking an item above the current position (E3/`:350-365`).

### Anti-orphaning rule (completion items live in the final phase)
Source: C4 (`:225-230`), I13 (`:580-585`), I17 (`:626-635`), and PART 2 `## Post-Completion Actions` (`:1118-1126`).
- Task completion is handled ONLY by the `## Post-Completion Actions` section, which is the LAST section before `## Task Log / Notes`.
- Do NOT create a separate "Task Completion and Handoff Protocol" section.
- Post-completion validation items (verify all `[ ]`→`[x]`, confirm output files exist via Glob, ensure blockers have resolution notes, run tests if code changed) appear in Post-Completion Actions BEFORE the frontmatter-to-Done update item (I17/`:632-633`).
- The frontmatter status→`🟢 Done` update is the FINAL checklist item (`:753`, `:1126`).

## 5. L1–L6 handoff patterns + subagent-spawning (the substrate for intra-task information flow)

Source: Section L (`:711-836`). Handoff files persist on disk across all batches/session-rollovers under `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/` (`:718-730`). Use these patterns ONLY when later items depend on earlier items' outputs (else use template 01).

| Pattern | Purpose | Output subdir | Template ref |
|---|---|---|---|
| **L1 Discovery** | Explore codebase/data, write structured findings later items read | `discovery/` | `:737-747` |
| **L2 Build-from-Discovery** | Create deliverable from a discovery file + source files (reference BOTH paths) | (deliverable path) | `:749-759` |
| **L3 Test/Execute** | Run a command/test; capture BOTH raw output (`.txt`) AND structured summary (`.md`) | `test-results/` | `:761-771` |
| **L4 Review/QA** | Assess an output vs source; produce structured PASS/FAIL verdict + findings | `reviews/` | `:773-783` |
| **L5 Conditional-Action** | Branch on a previous result; MUST handle BOTH success AND failure; output file always created | `plans/` | `:785-797` |
| **L6 Aggregation** | Glob-discover + consolidate many outputs into one report (final item in a phase) | `reports/` | `:799-809` |

L7 Pattern Selection Guide (`:811-836`) gives canonical phase compositions:
- Discovery→Build→Review: L1 → L2(per item) → L4(per item) → L6
- Build→Test→Fix: K1/K2 → L3 → L5
- Full lifecycle with QA gates: L1 → L2 → **M1(QA gate)** → L3 → L5 → L4 → L6 → **M1(QA gate)**

### Subagent spawning (the QA-gate spawn item)
The template models subagent spawning via the **QA Agent Spawn item** inside a Phase Gate (M1/`:843-851`). The spawn item is itself a B2 self-contained item that names: the agent (`rf-qa` for structural / `rf-qa-qualitative` for operational), the phase/mode, input file paths, output report path, verdict handling (proceed on PASS / fix-cycle on FAIL), and the error clause.
- F2 (`:405-412`) constrains delegation: a subagent receives work from a SINGLE checklist item only; NEVER delegate across phase boundaries; NEVER delegate the F1 loop itself.
- F2a parallel-spawning exception (`:430`): consecutive items in the SAME phase that spawn INDEPENDENT subagents MAY be spawned in parallel; the executor still marks each item individually.
- Real example spawn item: `TASK-RF-20260531-042405.md:310` (PG2.2) — spawns rf-qa in `task-integrity` mode with an inlined "ADVERSARIAL STANCE: ... fix_authorization: true" prompt, explicit (a)–(g) verification checklist, output verdict path, and "HALT-PRECEDENCE GUARDS: regression → monotonicity → cap (max 2 cycles per I16)". This matches the user-memory `feedback_rfqa_adversarial_pattern.md` (pair adversarial framing with fix_authorization).

## 6. Modeling a DECISION GATE / conditional phase (the core need for this task)

The track goal is "investigation/decision gate + conditional implementation": investigate findings, then EITHER close (path A) OR do a remediation subtree (path B). The template expresses this with the **L5 Conditional-Action pattern** plus phase structuring. There is NO dedicated "decision gate" section type — it is built from L5 + a `plans/` decision artifact + downstream phases gated on that artifact.

### How to model "if path A, close; if path B, do subtree X"

**(a) Investigation phase (L1 Discovery).** A phase whose items investigate each PR #112/#111 finding and write a structured findings/triage inventory to `phase-outputs/discovery/` — one item per finding (A3 granularity), each classifying the finding as (e.g.) `still-valid / already-fixed / wont-fix` with file:line evidence.

**(b) Decision item (L5 Conditional-Action, `02_mdtm_template_complex_task.md:785-797`).** A single self-contained item that reads the investigation inventory and writes a decision artifact to `phase-outputs/plans/<name>-decision.md`. It MUST handle BOTH branches explicitly:
```
- [ ] Read [investigation inventory at path] to determine [...], then:
   IF [no findings require code changes / all already-fixed],
     create `.../plans/<name>-decision.md` recording verdict=CLOSE with the evidence
     and a statement that Phases [X+1..] are SKIPPED;
   IF [≥1 finding requires remediation],
     create `.../plans/<name>-decision.md` recording verdict=PROCEED, an enumerated
     list of which remediation sub-items/phases apply, and the priority ordering;
   ensuring both branches are based on actual evidence with no fabrication [...].
   If unable [...], log the blocker [...], then mark this item complete. Once done, mark this item as complete.
```
The decision artifact's frontmatter mirrors the real example `r1-3-proceed-decision.md:1-9` (`artifact`, `phase`, `gate`, `verdict_source`, `decision: PROCEED to Phase N`). The body records the verdict, what was delivered/found, and a "Mandatory carry-forward" list — see `r1-3-proceed-decision.md`.

**(c) Conditional implementation phase(s) (path B subtree).** The remediation phases that follow are written normally (K1/K2/L2 build items + L3 test items), but each is governed by the decision artifact. Two encoding options, both seen in the example:
- **Gate-on-artifact:** the first item of the remediation phase opens with "Read the decision artifact at `.../plans/<name>-decision.md`; IF verdict=CLOSE, skip this phase and mark all its items complete with a note; IF verdict=PROCEED, [...]". This keeps the subtree in the file but conditionally inert.
- **Phase-gate conditional proceed (M1 Item 3 / I16 fix-cycle):** the real example uses L5 "Act on QA verdict" items at every gate — `TASK-RF-20260531-042405.md:314` (PG2.3): "IF verdict is PASS, create `.../plans/r0-1-proceed-decision.md` and proceed to Phase 3; IF FAIL, [...fix cycle, max N cycles...]". This is the exact shape for an investigation→decision→conditional-work flow.

**Key invariant (L5/`:790-792`):** the output file is ALWAYS created regardless of branch — so even a "CLOSE" decision produces a `plans/*-decision.md` proving the gate was evaluated. This is how the worker (and any resumed session) knows which branch was taken.

## 7. QA-gate / validation / testing items as checklist items

This task needs a final validation gate: `make lint-architecture`, `make verify-sync`, targeted `uv run pytest`. The template encodes these as L3 Test/Execute items (`:761-771`) and Phase-Gate sequences (M1/`:843-851`); I18 (`:637-646`) MANDATES ≥1 testing item for any code-modifying task.

### Test/lint item encoding (L3) — confirmed in the real example
- `TASK-RF-20260531-042405.md:296` (Step 2.7): `uv run pytest ... -v 2>&1`, write raw `.txt` to `test-results/`, write structured `.md` summary (overall result, counts, failed-test table). Closes with the blocker/completion gate.
- `TASK-RF-20260531-042405.md:300` (Step 2.8): `uv run ruff check ...` + `uv run ruff format --check ...`, summary to `test-results/`, with an inline fix loop ("If ruff reports issues, run `uv run ruff check --fix` ... then re-run").
- For `make lint-architecture` / `make verify-sync`: model as their own L3 items (`uv run`/`make` via Bash, capture output, write summary, inline fix loop). Example `make lint-architecture` wiring appears at `:384` (Step 4.4). `make verify-sync` is verified inside the terminal qualitative gate at `:739` (point (d): "`make verify-sync` passes (no orphan `.claude/` edits)").

### Phase-gate QA sequence (M1, the 2–3 item gate between phases)
Source M1 (`:843-851`), I15 (`:599-607`), I16 verdict/fix-cycle table (`:609-624`). A gate = 3 items:
1. **Aggregation (L6):** Glob-collect the phase's outputs into a `reports/*-aggregation.md`. Real: `:306` (PG2.1).
2. **QA Agent Spawn:** spawn `rf-qa` (structural) and/or `rf-qa-qualitative` (operational) — sequential, qualitative after structural. Real: `:310` (PG2.2), and terminal qualitative gate `:739` (PG13.1).
3. **Conditional Proceed (L5):** read verdict; PASS→proceed + write `plans/*-proceed-decision.md`; FAIL→fix cycle (max cycles per I16: task-integrity=2, qualitative=3), then proceed or HALT/escalate. Real: `:314` (PG2.3), `:743` (PG13.2).

I16 fix-cycle caps (`:614-620`): research-gate 3 / synthesis-gate 2 / report-validation 3 / task-integrity 2 / any qualitative gate 3. After max: HALT+escalate (research/report/qualitative) or unresolved→Open Questions (synthesis/task-integrity). The real example encodes "HALT-PRECEDENCE: regression → monotonicity → cap" in every conditional-proceed item.

For THIS task, a sensible final gate (per M2/`:852-860` "Code-modifying tasks: gate after implementation"): a Testing & Verification phase running targeted `uv run pytest` + `make lint-architecture` + `make verify-sync` (L3 items), then a Phase Gate spawning rf-qa task-integrity (adversarial + fix_authorization), then a conditional-proceed item. Validation that has nothing to fix simply records PASS and proceeds — cheap, per M2 "when in doubt, include a gate".

## 8. Post-Completion Actions + Task Log structure (verbatim shape to reuse)

Source PART 2 `:1118-1205`; real `:745-797`. The `## Post-Completion Actions` section has exactly these items in order (each a B2 self-contained item):
1. Verify all outputs exist via Glob (list expected output files + source/test files); log gaps to `### Follow-Up Items Identified` (`:747`, `:1120`).
2. If source code modified, run the relevant test suite one final time for regression confirmation; may note "Tests verified in Phase [N]" if recent + unchanged (`:749`, `:1122`).
3. Create the `### Task Summary` (work completed / challenges / deviations / blockers with status) (`:751`, `:1124`).
4. Update `completion_date` + `updated_date` + `status: "🟢 Done"` in frontmatter and append the Execution Log completion entry — FINAL item (`:753`, `:1126`).

`## Task Log / Notes 📋` skeleton (`:755-797`, `:1128-1205`): `### Task Summary` (stub with templated fields), `### Execution Log` (timestamped `**[YYYY-MM-DD HH:MM]** - ...` entries), one `### Phase N - [Name] Findings` per phase (each carries the templated blocker-entry HTML comment), `### Phase Gate Findings` ("QA gate verdicts, fix cycle counts, and unresolved issues recorded here"), `### Follow-Up Items Identified`, `### Deviations from Process`. The blocker-log target referenced by every item's completion gate is the matching `### Phase N ... Findings` heading — so the builder MUST create one Findings heading per phase, named to match what the items cite.

## 9. Prior-example shapes (effective patterns to mirror)

### `TASK-RF-20260531-042405/` (in-flight, the strongest precedent)
- Folder layout: the task `.md` + `research/` (numbered research files 01–03) + `phase-outputs/{discovery,test-results,reviews,plans,reports}/` + `qa/` + `NEXT-SESSION-*-PROMPT.md` resume notes.
- 13 phases, each release-scoped (R0.1, R0.2, ...), EACH followed by a `### Phase Gate: <name> Quality Verification` with the 3-item M1 sequence (aggregate → rf-qa spawn → act-on-verdict). This is the dominant repeating unit.
- Phase 1 = Preparation: Step 1.1 status→Doing + Execution Log entry (`:239`); Step 1.2 verify/create handoff dirs (`:243`); Step 1.3 git-remote+branch hygiene check writing to `discovery/git-remote-confirmation.md` (`:247` — enforces the fork-PR ABSOLUTE RULE); Step 1.4 read spec authority in full + write a structural index (`:251`).
- Every code phase ends with a pytest L3 item + a ruff lint/format L3 item before its gate.
- Decision artifacts under `plans/` (`r0-1-proceed-decision.md`, `r1-3-proceed-decision.md`) record the PROCEED/CLOSE verdict + carry-forward list.

### Other TASK-RF-* folders (older, simpler shape)
- `TASK-RF-20260529-171029/`, `TASK-RF-20260526-183300/`, `TASK-RF-20260525-194356/` each hold a single task `.md` + `research/` + `phase-outputs/` (+ some a `qa/`). Same skeleton, fewer phases — confirms the template scales down: a remediation task does not need 13 phases.

### Recommended shape for THIS remediation task (synthesis)
1. **Phase 1 Preparation:** status→Doing; create/verify `phase-outputs/` subdirs; git-remote+branch hygiene (fork rule); read the combined `/sc:design` `.md` + PR #112/#111 validated findings and write a structural index to `discovery/`.
2. **Phase 2 Investigation (L1):** one item per finding, each triaging it (still-valid / already-fixed / superseded) with file:line evidence into a `discovery/findings-triage.md`.
3. **Decision Gate (L5):** one conditional-action item → `plans/remediation-decision.md` (verdict CLOSE → skip Phase 3; PROCEED → enumerate which fixes apply). Always create the artifact.
4. **Phase 3 Conditional Remediation (path B):** gated on PROCEED; K1/K2/L2 build items (edits in `src/superclaude/` only) + L3 pytest/ruff items. Each remediation item self-contained, one fix per item.
5. **Phase Gate: Validation (M1):** L6 aggregate → rf-qa task-integrity spawn (adversarial + fix_authorization, HALT-PRECEDENCE) → L5 conditional-proceed.
6. **Phase: Final Validation (L3):** targeted `uv run pytest <paths>`, `make lint-architecture`, `make verify-sync` — each its own item with raw+summary capture and inline fix loop.
7. **Post-Completion Actions:** Glob output verification → final regression run → Task Summary → frontmatter→Done.
8. **Task Log / Notes:** Task Summary stub, Execution Log, one `### Phase N - [Name] Findings` per phase, Phase Gate Findings, Follow-Up Items, Deviations.

## 10. Builder gotchas (project-specific, load-bearing)

- **`make sync-dev` / source-of-truth:** any item editing skills/commands/agents must edit `src/superclaude/` then `make sync-dev` — NEVER `.claude/`. Items in the example inline "REMEMBER: `src/superclaude/` first; NEVER `.claude/`" (e.g. `:330`). `make verify-sync` belongs in the final gate.
- **UV-only:** every command item must use `uv run ...` / `make ...`, NEVER bare `pytest`/`ruff`/`python`/`pip` (project + user CLAUDE.md). The example repeats "REMEMBER: UV-only" in every command item.
- **Single-line commands:** per user memory `feedback_no_multiline_paste.md`, any command an item asks the worker to surface to the user must be single-line (no heredocs/`\` continuations). The example's Make-target item enforces "single-line invokable" (`:384`).
- **Fork PR rule:** if any item creates a PR, it MUST use `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> ...` — never bare `gh pr create` (ABSOLUTE RULE). The Phase 1 git-remote-confirmation item guards this.
- **No checklist items before Phase 1** (D3). Key Objectives / Prerequisites are informational only.
- **Findings-heading naming:** each item's blocker clause cites a specific `### Phase N - [exact name] Findings` heading — those headings must exist verbatim in Task Log / Notes.

---

**Status: Complete**

### Summary
The builder MUST use `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 2 as the body skeleton and PART 1 as the rulebook. Frontmatter (§1) and the fixed section order (§2) are mandatory; checklist items are forbidden before Phase 1. Every item is a single self-contained paragraph carrying B2's 6 elements (§3), grouped under non-checkbox `**Step X.Y:**` headers (§4), with completion/summary items living only in `## Post-Completion Actions` (anti-orphaning, §4/§8). The investigation→decision→conditional-work flow this task needs is built from an L1 investigation phase → an L5 conditional-action **decision item** that ALWAYS writes a `plans/*-decision.md` artifact handling BOTH the CLOSE and PROCEED branches → conditionally-gated remediation phases → an M1 phase-gate (aggregate → rf-qa spawn → conditional-proceed) (§5/§6/§7). The final `make lint-architecture` / `make verify-sync` / targeted `uv run pytest` validation is encoded as L3 test items inside a Testing & Verification phase plus a closing phase gate (§7). The in-flight `TASK-RF-20260531-042405` is the strongest precedent — its repeating "phase → L3 test+lint → Phase Gate (M1)" unit and its `plans/*-proceed-decision.md` artifacts are exactly the shapes to mirror, scaled down to ~3–4 phases (§9). Project guardrails (UV-only, `src/superclaude/` SoT, single-line commands, fork-only PRs) must be inlined into command items as "REMEMBER:" clauses (§10).
