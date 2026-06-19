# Research: Template and Examples

**Status:** Complete
**Date:** 2026-06-19

**Scope:** MDTM Template 02 (complex-task) rules a builder/generator must satisfy so the
implementation tasklist it emits is well-formed, plus a worked example (the doc-refresh
sibling task) and two further QA-gate-encoding examples.

**Template file:** `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`
(1516 lines; PART 1 = build instructions lines 63–1131, PART 2 = actual task template
lines 1157–1515).

---

## 1. YAML Frontmatter Schema (template lines 1–61)

The frontmatter the builder must populate (template `02_mdtm_template_complex_task.md:1-61`).
Field → meaning (verbatim defaults / option enums from the template):

| Field | Line | Notes |
|---|---|---|
| `id` | :2 | `TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS` |
| `title` | :3 | Clear, action-oriented |
| `description` | :4 | What the task accomplishes + purpose in larger workflow |
| `status` | :7 | enum `🔵 Backlog \| 🟡 To Do \| 🟠 Doing \| 🔴 Blocked \| 🟢 Done \| ⚪ Cancelled`; default `🟡 To Do` |
| `type` | :9 | enum incl. `✨ Feature \| 🐛 BugFix \| 📚 Documentation \| ⚙️ Maintenance \| 🔬 Research/Spike \| ✅ Verification/QA \| 🧩 Integration \| 🛠️ Tooling/Automation` (full list :8) |
| `priority` | :11 | enum `🔥 Highest \| 🔼 High \| ▶️ Medium \| 🔽 Low \| 🧊 Lowest` |
| `created_date` / `updated_date` | :12-13 | `YYYY-MM-DD` |
| `assigned_to` | :14 | agent name |
| `coordinator` | :17 | `orchestrator` |
| `parent_task` / `depends_on` | :19-22 | parent + blocking dep IDs |
| `spec_path` | :23 | "driving spec/PRD/TDD path; populated by task-builder (A.2), empty if none" |
| `reflect_pre` | :24-31 | PRE reflect-gate sign-off block: `verdict` (pass\|fail\|skipped), `coverage_pct`, `depth` (quick\|standard\|deep), `tcs`, `run_id`, `report`, `reviewed_at` — populated by task-builder at A.10.7 |
| `reflect_post` | :32 | "POST reflect verdict; recorded by the executor after the final-phase reflect subagent runs" (string, set during execution) |
| `related_docs` | :33-39 | list of `{path, description}` |
| `related_prd` / `related_tdd` | :40-41 | |
| `tags` | :42-46 | categorization list |
| `template_schema_doc` | :47 | path to the schema doc this task conforms to |
| `task_type` | :60 | `static` (fixed content) or `dynamic` (runtime-added items inside DYNAMIC markers; see I6) |

NOTE: the prompt's expected field name `executor_model_class` is **NOT present** in this
template's frontmatter (Unverified — closest fields are `assigned_to`, `ai_model`,
`model_settings`). `start_commit` is also **NOT** a template frontmatter field (Unverified).
A generator wanting those must add them — they are not template-mandated.

## 2. Section A — Core Principles (the granularity contract)

- **A3 Complete Granular Breakdown** (`:108-112`): break EVERY workflow phase into atomic,
  verifiable checklist items; an individual item for EVERY file/component/iteration; **NO
  high-level or bulk operations**; include exact file paths, specific requirements,
  measurable outcomes.
- **A4 Iterative Process Structure** (`:114-133`): for any multi-item process — (1)
  pre-enumerate ALL items in an initial step, (2) one checklist item per specific item,
  (3) incremental update after each item, (4) a consolidation step only after all items
  complete. The template gives the exact `Step X.1 scan/enumerate → Step X.2 process each
  → Step X.3 consolidate` skeleton.

## 3. Section B — Self-Contained Items (B2, the core item shape)

**B2** (`:159-166`) — EVERY checklist item is a complete, self-contained prompt with **6
mandatory elements**:
1. **Context Reference with WHY** — what file(s) to read and why needed for *this* action.
2. **Action with WHY** — what to do with that context and why.
3. **Output Specification** — exact output file name, location, content, template to follow.
4. **Integrated Verification** — an "ensuring…" clause (no assume/hallucinate; 100% derived
   from referenced source files; document negative evidence on failure).
5. **Evidence on Failure Only** — log to task notes ONLY if blocked (success is evidenced by
   the output file itself).
6. **Explicit Completion Gate** — verbatim: "This item cannot be marked as done until the
   actions are completed in their entirety exactly as described. Once done, mark this item
   as complete."

Supporting rules: **B3** one full paragraph (not bullets), verbose/explanatory, reads like a
standalone prompt (`:167-170`); **B4** correct example with action+verification integrated
(`:172-179` — note "Do NOT create separate verification items"); **B5** forbidden patterns
(`:181-200`): standalone "read context" items, missing context reference, multi-line/bulleted
items, separate verification items, over-granular items, separate REMINDER blocks. **C1-C3**
(`:223-240`): outputs / success criteria / verification are EMBEDDED in items, never separate
sections.

## 4. Section M — Lens-Based QA + Source Fidelity (M3, M4)

- **M3 Lens-Based QA Sequence** (`:1059-1096`) — MANDATORY replacement for the deprecated
  single-agent M1 (`:1034-1045`). 8 steps, each an explicit `- [ ]` item:
  1. Aggregation (L6) — collect preceding-phase outputs.
  2. Structural lens agents (rf-qa) — PARALLEL, one per lens, `fix_authorization: false`,
     report path `${TASK_DIR}qa/qa-structural-[lens]-report.md`, adversarial framing
     "Assume this document has at least N errors focused on [lens]. Find them."
  3. Content lens agents (rf-qa-qualitative) — PARALLEL, same shape, `qa-content-[lens]`.
  4. Domain-specific lens agents (if skill defines extras) — PARALLEL.
  5. Findings consolidation → `${TASK_DIR}qa/qa-consolidated-findings.md` (dedup, severity,
     originating lens).
  6. Fix agent — ONE rf-qa with `fix_authorization: true`, applies ALL fixes.
  7. Verification round — ≥2 agents (1 rf-qa + 1 rf-qa-qualitative), `fix_authorization:
     false`.
  8. Conditional proceed (L5) — PASS→proceed; FAIL→repeat 5-7 up to I16 max, then HALT.
  Every step MUST be its own `- [ ]` item; the orchestrator must NOT collapse steps (`:1096`).
- **M4 Source-Document Fidelity Gate** (`:1098-1121`) — runs AFTER M3. Validates *external*
  fidelity (output faithfully represents source docs) vs M3's internal quality. Steps:
  source-doc identification → fidelity agents (≥2, partition to 3-4 if sources >1000 lines;
  each reads its source section range + FULL output) → cross-source contradiction agent (if
  multiple sources; reads sources only) → consolidation → fix agent → verification (≥2). Same
  cycle control as M3 (max 3, then HALT).

## 5. Section I — QA enforcement floors (I19–I22)

- **I19 Lens-Based QA Minimum Agents** (`:699-743`). FULL-intensity floors:
  - **Final / assembled-output QA** by size: `<500`→3 structural + 3 content = **6**;
    `500-1500`→4+4=**8**; `1500-3000`→5+5=**10**; `>3000`→6+6=**12**. These are floors,
    BEFORE domain-specific lenses.
  - **Intermediate-gate 5-agent floor** (`:731-737`): research-gate = 2 rf-analyst +
    2 rf-qa + 1 rf-qa-qualitative; synthesis-gate = 2 rf-analyst + 2 rf-qa +
    1 rf-qa-qualitative; task-integrity = 2 rf-qa + 2 rf-qa-qualitative + 1 rf-analyst.
  - Standard structural lenses (`:715-720`): template-conformance, internal-consistency,
    evidence-quality, completeness. Standard content lenses (`:721-726`): actionability,
    numbers-and-metrics, crossref-chain-integrity, domain-accuracy.
  - Adversarial-framing N scales with size: 5 (<500), 10 (500-1500), 15 (1500-3000),
    20 (>3000) (`:729`). Partitioning is per-lens-per-partition and INCREASES agent count
    (`:739-741`, `:1094`).
- **I20 Serialized Fix Authorization** (`:745-757`). Any gate with 3+ agents on the same
  file MUST serialize fixes: report (all `fix_authorization:false`) → consolidate →
  ONE fix agent (`fix_authorization:true`) → verify (≥2). Parallel fix authorization is
  PROHIBITED ("Agent A fixes line 50 one way, Agent B another"). Applies at ALL intensities
  (`:838-840`).
- **I21 Source-Document Fidelity Applicability** (`:759-789`). MANDATORY for: PRD, TDD,
  roadmap, tech-reference, operational-guide, README, tech-research, repo-cleanup, and any
  task that reads source docs to produce output. NOT required for pure mechanical
  transforms / config-only tasks. ≥2 fidelity agents (3-4 if sources >1000 lines). Runs
  AFTER lens-based QA (`:788`).
- **I22 qa_intensity → agent counts** (`:793-840`). Three levels:
  | Level | Intermediate | Final (M3) | Fidelity (M4) | Fix cycles | Verify |
  |---|---|---|---|---|---|
  | **lite** | 2 (1 rf-qa + 1 rf-qa-qualitative) | 3 (1 struct + 1 content + 1 domain) | 1 (combined) | 1 max | 1 |
  | **standard** | 3 (1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative) | 7 (3 struct + 3 content + 1 domain) | 2 | 2 max | 2 |
  | **full** | per I19 (5+) | per I19 (6-12+ + all domain lenses) | per I21 (2-8) | per I16 (2-3) | 2 |
  Default mapping: Quick/Lightweight→lite, Standard→standard, Deep/Heavyweight→full
  (`:806-809`). Serialized fix (I20) applies at ALL levels (`:838`).

Also load-bearing for the generator: **I15 Phase-Gate QA Enforcement** (`:635-651`) — any
task with 2+ phases MUST have a phase-gate QA checkpoint; gates <6 (final) / <5
(intermediate) agents are REJECTED at validation; the checkpoint MUST follow M3 (+ M4 if
source docs). **I16 QA Gate Verdict & Fix Cycles** (`:653-673`) — binary PASS/FAIL (ANY
issue of ANY severity = FAIL); per-gate max-cycle table (research/report/qualitative/
source-fidelity = 3 then HALT-escalate; synthesis/task-integrity = 2 then Open Questions).
**I17 Post-Completion Validation** (`:675-686`) — before Done: all items `[x]`, all output
files exist (Glob), blockers resolved, tests pass, **mandatory final lens-based QA (item 5)**
and **source-fidelity gate when applicable (item 6)**. **I18** (`:688-697`) — code-modifying
tasks MUST include ≥1 testing item (L3 pattern).

## 6. `## Execution Context` section (template-mandated; the P1-reused shape)

Template PART 2 (`:1193-1221`). The template MANDATES this section and marks it a required
build step: `<!-- BUILDER: Populate this section as a required build step. Every generated
task file MUST have this section populated before the task file is marked ready. -->`
(`:1195`). Exact sub-shape:

- **`### References`** (`:1197-1199`) — "all governing documents, specs, and workflow files
  this task operates under. Format: `- [Document Name](path/to/doc.md): [one-line purpose]`".
- **`### Source Areas`** (`:1201-1203`) — "all codebase directories, modules, or file sets
  this task reads from or modifies. Format: `- \`path/to/area/\`: [what it contains / why
  relevant]`".
- **`### Key Constraints`** (`:1205-1207`) — "top constraints that govern execution: QA
  intensity, scope limits, known blockers, standing prohibitions."
- Plus `### Handoff File Convention` (`:1209-1221`) and `### Frontmatter Update Protocol`
  (`:1223-1231`).

This is the same Execution Context concept P1 reuses in sc:tasklist. The defining property:
it is a **header/orientation block with NO file:line citations** — References uses
`path/to/doc.md` (doc-level), Source Areas uses `path/to/area/` (directory-level). No "at
line N" in the header; precise file:line citations belong inside individual B2 items, not in
this orientation section.

## 7. PR-02 / FR-CONV.5 Retry Monotonicity — NOT in the template (Unverified-in-template)

`grep -ni "PR-02|FR-CONV|monotonic|Retry Monotonicity"` over the template returns **zero
matches**. The template does not carry PR-02 / FR-CONV.5 Retry-Monotonicity wording. That
contract is owned by the sc:tasklist generator / its conventions doc (R01-R05 territory),
NOT by Template 02. A generator must inject it; the template will not supply it.

## 8. POST reflect gate item — NOT hardcoded in the template; generator-injected

The template Part 2 Post-Completion section (`:1423-1441`) contains, in order: (a) Glob
output-existence check (`:1425`), (b) test-regression check (`:1427`), (c) **placeholder**
post-completion lens-based QA (`:1435`, I17 item 5), (d) **placeholder** post-completion
source-fidelity gate (`:1437`, I17 item 6), (e) Task Summary (`:1439`), (f) Update-status-to-
Done (`:1441`).

There is **NO** flat `superclaude reflect run … --depth deep --fix --promote` item and **NO**
`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` guard text anywhere in the template
(`grep` → only `reflect_post` frontmatter at `:32` and the `🟢 Done` items at `:466/:1227/
:1441/:1475`). The penultimate-before-Done reflect gate is therefore **injected by the
sc:tasklist generator**, not by the template. The worked example below shows its concrete
shape (Section 9). A generator must add it; the template only reserves the `reflect_post`
frontmatter slot.

---

## 9. WORKED EXAMPLE — `TASK-RF-rfmerger-refresh-20260618-172224`

File: `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/TASK-RF-rfmerger-refresh-20260618-172224.md`
(580 lines, status `🟢 Done`). This is the doc-refresh **sibling** of the current work
(it refreshed RFMerger spec/PRD/TDD; the current task generates the *implementation*
tasklist from those refreshed docs). It is the single best template-conformant model.

### 9.1 Frontmatter — generator-added fields beyond the template
- `reflect_pre` populated as a block with `verdict: "skipped"`, `skip_reason: "no-spec"`,
  `depth: "deep"` (`:20-28`).
- `reflect_post` populated as a **full block** (not the template's empty string `""`):
  `verdict: pass`, `status: success`, `run_id`, `tier_reached: 2`, `report`/`contract`
  absolute paths, a `deviations:{authorized/necessary/drift/regression}` count block,
  `head` SHA, `reviewed_at` ISO timestamp, plus task-specific gating fields
  `downstream_blocked_pending_human_decision: true`, `p2_decision: PENDING`,
  `p5_decision: PENDING`, `done_flip_permitted: true`, and a verbose
  `done_flip_justification` (`:29-50`). **Effective pattern:** the executor writes a rich
  `reflect_post` block; the generator only has to reserve the slot + emit the POST item.
- Extra generator fields not in the bare template: `template: "02"` (`:68`), `tracks:`
  (`:69-71`), `estimation: "complex"` (`:72`), `created` (`:10`), `autogen_method:
  "task-builder"` (`:14`). `executor_model_class` and `start_commit` are **absent** here
  too — confirming they are not a template/worked-example convention.

### 9.2 Phase structure (4 phases + Post-Completion)
- **Phase 1** Preparation, Source Inventory, Evidence Map (`:174`) — discovery (L1) items
  → aggregation (`:190` Step 1.4) → **Phase 1 Gate: Research Completeness** (`:194`).
- **Phase 2** Refresh the 5 documents + record P2/P5 human decisions (`:218`).
- **Phase 3** Full Document Structural+Fidelity+Qualitative QA Gate (M3 then M4) (`:250`).
- **Phase 4** Runtime, Sync, Human Review Checkpoint, Non-Blocking Downstream Handoff (`:314`).
- **Post-Completion Actions** (`:350`) — existence check → final-validation evidence →
  6-agent post-completion final QA → consolidate/fix/verify → Task Summary → **POST reflect**
  → Done flip.

### 9.3 Per-phase QA gates — exact encoding (the model to copy)
**Phase 1 research-gate** (`:194-216`), the 5-agent intermediate floor (I19): each agent is
its OWN `- [ ]` item — 2 rf-analyst (research-completeness `:198`, cross-validation `:200`),
2 rf-qa (evidence-quality `:202`, gap-detection `:204`), 1 rf-qa-qualitative
(research-depth `:206`) — then consolidation (`:208`), conditional fix agent
(`:210`, "if PASS write NO-FIX-NEEDED and skip; if FAIL spawn exactly one rf-qa
`fix_authorization: true`"), structural verification (`:212`), qualitative verification
(`:214`), gate verdict (`:216`). A prose lead-in line above the items (`:196`) explicitly
authorizes spawning the 5 report-only agents as one parallel batch.

Every QA-agent item carries (verbatim from the example): the agent type in backticks; a
**fully embedded prompt** delimited in backticks; an **`ADVERSARIAL STANCE`** preamble with
named axes (AX-1 drift, AX-2 contradictions, AX-3 omissions, AX-4 weakened criteria, AX-5
invented content); the adversarial-N framing ("Assume … at least 5 important items"
missing); an explicit `fix_authorization: false`; "Do not modify files."; an absolute QA
report output path under `…/qa/`; binary PASS/FAIL verdict requirement; and the standard
B2 blocker clause + completion gate.

**Phase 3 final/document gate** (`:250-313`): aggregation (`:256`) → 6 M3 lens agents
(3 structural rf-qa + 3 content rf-qa-qualitative) → consolidate + serialized fix (`:274`)
→ M4 source-fidelity (partitioned, `:286`) → fidelity consolidate/fix (`:302`). Matches
I19 `<500/500-1500` final floor (6+) + I21 fidelity (M4 after M3).

**Post-completion final QA** (`:358-380`): 6 report-only lens agents (`:360-370`,
"lens 1 of 6 … lens 6 of 6"), consolidation (`:372`, "PASS only if all six reports are
PASS"), serialized conditional fix (`:374`, "spawn exactly one … fix agent"), structural
verification (`:376`), qualitative verification (`:378`), consolidated verdict (`:380`).
This is the **I17 item-5 mandatory post-completion lens QA** fully expanded from the
template's placeholder.

### 9.4 B2 self-contained items
Every item is ONE long paragraph (e.g. `:224` ledger creation): reads gate-verdict + inputs
→ creates an absolute-path output with an enumerated column/section spec → "ensuring …"
clause with concrete invariants (P2 PENDING until human choice, no stale `/rf:*`/`.gfdoc`
tokens) → blocker clause → "Once done, mark this item as complete." No standalone
read-context items; no separate verification items; verification is embedded.

### 9.5 `## Execution Context` population (`:120-161`)
- **References** (`:122-130`): 8 entries `- [R-00N Name](abs-path): one-line purpose` —
  doc-level links, NO file:line.
- **Source Areas** (`:132-140`): directory/file-set entries `- \`abs/path/\`: purpose`.
- **Key Constraints** (`:142-147`): names `QA intensity is **full**` + `PER_PHASE`,
  documents-only scope limit, P2/P5 must-be-human-decision, stale-token prohibition,
  `src/superclaude` source-of-truth + `make sync-dev`/`verify-sync`.
- Plus Handoff File Convention (`:149-160`) and Frontmatter Update Protocol (`:162-168`).
Confirms the no-file:line orientation-block property from Section 6.

### 9.6 Human-decision items (the must-HALT pattern)
P2 (`:244`) and P5 (`:248`) are encoded so the item writes `decision: defer` /
`retain-…` / **`decision: PENDING`** and, critically: "ensuring **no default is chosen
without explicit human input**" and "`PENDING` clearly blocks downstream
implementation-tasklist generation while allowing document QA to continue." The blocker
branch: "If unable to complete due to missing human input, record `decision: PENDING`, log
that downstream … is blocked, then mark this item complete." This matches the memory rule
`feedback_human_decision_items_must_halt` (write PENDING + halt the dependent mutation;
never auto-default). The Done-flip item (`:386`) re-enforces it: must NOT flip Done if
"POST reflect is FAIL/PENDING" — but here P2/P5 PENDING blocks only *downstream
implementation generation*, not this docs-only task's Done (see `done_flip_justification`
`:50`).

### 9.7 POST reflect item (the exact penultimate shape — `:384`)
Single flat `- [ ]` item, penultimate immediately before the Done-flip item (`:386`).
Executable command is the **guarded wrapper**, verbatim:
```
if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi; superclaude reflect run <ABS_TASK_FILE> --depth deep --fix --promote
```
Run from repo root; capture outputs under `…/reflect/post/`; then "update this task file's
`reflect_post` frontmatter field with the substantive verdict, report path, reviewed_at
timestamp, and decision_pending status if degraded or blocked." Embedded invariants
(verbatim themes): reflect gate is **penultimate** immediately before final Done/Blocked;
runs after document creation, Task Summary, and final QA verification; **does NOT use a
slash-command POST reflect invocation** as the executable instruction; **does NOT nest
inside `/sc:tasklist`**; does NOT generate implementation tasklists; **halts the Done flip
if verdict is FAIL or a degraded verdict requires human decision**. Blocker branch: "set
`reflect_post: PENDING`, log the blocker …, do not mark the task Done." This is the literal
shape the generator must emit (it is generator-injected, not template-supplied — Section 8).

### 9.8 Anti-patterns to AVOID (lessons the example encodes)
- Do NOT collapse a QA gate into one "run QA" item — each lens/consolidate/fix/verify step
  is its own `- [ ]` (I15/M3 `:1096`). The example expands all of them.
- Do NOT spawn parallel fix authorization — exactly ONE fix agent with
  `fix_authorization: true` per cycle (I20); all lens agents are `false`. The example says
  "spawn exactly one … fix agent" (`:210`, `:374`).
- Do NOT auto-default human decisions — write PENDING + block downstream (`:244/:248`).
- Do NOT use a `/sc:*` slash invocation for the POST reflect executable (`:384`); use the
  flat guarded `superclaude reflect run` wrapper.
- Do NOT put file:line citations in `## Execution Context` headers (Section 6); keep them in
  the B2 items.
- Do NOT flip Done with unchecked items / FAIL-or-PENDING reflect / missing outputs (`:386`).
- The example's own logged deviation (`:408`): an M3 internal-consistency lens favored a
  majority "3 total passes" wording but the M4 source-fidelity lens caught the correct
  "2 total passes" from `adversarial-validation.md:141` — evidence that the layered M3→M4
  gate (Section 4) actually catches fidelity drift a single gate would miss.

---

## 10. Other recent TASK-RF examples that encode QA gates well

1. **`.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/TASK-RF-tfep-troubleshoot-migration-20260616-174519.md`**
   — Best code-modifying-task model. One **`### Phase Gate N`** M3 lens-based gate after
   EACH implementation phase, each labeled "(M3, standard intensity — 7 report-only agents,
   max 2 fix cycles)" (`:233`, `:323`, `:409`) — a clean worked instance of I22 `standard`
   intensity (7 = 3 structural + 3 content + 1 domain) with per-phase gating (I15).

2. **`.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/TASK-RF-sprint-runlock-20260617-020000.md`**
   — Multi-phase (Phase 1-7) code+test task; carries a logged POST reflect-gate result with
   the `superclaude reflect run --depth deep` wrapper and an explicit degraded-verdict
   human-decision rationale (`:166`) — a good model for recording a *degraded* reflect
   outcome without auto-flipping Done.

---

## 11. Summary for the sc:tasklist generator (what to emit so the tasklist is well-formed)

1. **Frontmatter:** populate the template schema (`:1-61`); reserve `reflect_post: ""` and
   `reflect_pre:` block; add `template: "02"`, `tracks`, `estimation` if following the
   worked-example convention. `executor_model_class`/`start_commit` are NOT template fields
   — add only if the generator's own contract requires them.
2. **`## Execution Context`** is MANDATORY and must be populated (References / Source Areas /
   Key Constraints, NO file:line) — template `:1193-1207` / example `:120-147`.
3. **Every item is B2** (6 elements, one paragraph, embedded verification, completion gate).
4. **Every phase boundary (2+ phases) gets a phase-gate QA checkpoint** following M3 (+ M4 if
   source docs), every step an explicit `- [ ]` item, agent counts per I19/I22 intensity,
   serialized fix per I20, verdict/cycles per I16.
5. **Human-decision items write PENDING + HALT the dependent mutation** — never auto-default.
6. **POST reflect item is the penultimate Post-Completion item** (before Done flip): the
   flat guarded `superclaude reflect run … --depth deep --fix --promote` wrapper with the
   `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion breaker; NOT a slash command; NOT nested in
   `/sc:tasklist`; updates `reflect_post`; halts Done on FAIL/PENDING. (Generator-injected —
   not in the template.)
7. **PR-02 / FR-CONV.5 Retry Monotonicity** is owned by the generator/its conventions, NOT
   the template — must be injected (the worked example bakes the exact halt strings
   `Regression detected on Item X.Y, previously PASS at cycle N, now FAIL. Halt overrides
   monotonicity check.` and `[HALT-MONOTONICITY] |F|=<n>` into its gate-verdict items —
   example `:216`, `:380`).
