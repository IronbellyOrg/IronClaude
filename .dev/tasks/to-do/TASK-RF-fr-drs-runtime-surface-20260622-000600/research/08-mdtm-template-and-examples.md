# R8 Research: MDTM Template 02 + Examples (Template & Examples)

**Status: Complete**
**Date: 2026-06-22**
**Researcher: R8 of 8 (FR-DRS task-builder)**
**Focus: MDTM Template 02 rules + effective patterns from prior reflect task files**
**Scope ownership:** ONLY the template rules + task-file formatting conventions + example patterns. R1–R7 own codebase substance.

**Primary sources (all [CODE-VERIFIED] by direct Read this turn):**
- Template: `.claude/templates/workflow/02_mdtm_template_complex_task.md` (1516 lines; Part 1 = build instructions L62–1131, Part 2 = clean template L1157–1516).
- Real recent exemplar: `.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md` (141 KB; the immediate predecessor FR — same reflect-skill-edit + eval shape, same POST_REFLECT_GATE).
- Cross-check exemplar: `.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/TASK-RF-reflect-post-gate-wiring-20260611-022409.md`.
- Canonical schema doc the builder must point `template_schema_doc` at: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (the `src/` SoT copy; the `.claude/` copy is sync-dev output — see UC2 frontmatter L51 [CODE-VERIFIED]).

> NOTE on `${TASK_DIR}`: the template uses `${TASK_DIR}` and `.dev/tasks/TASK-NAME/` as placeholders. The builder MUST substitute the literal absolute task dir: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-fr-drs-runtime-surface-20260622-000600/`. UC2's reflect-gate item uses the full absolute path (see §5 below) — match that. [CODE-VERIFIED: UC2 L363]

---

## 1. Template 02 — Required Sections (the conformant skeleton)

### 1a. Frontmatter keys (Part 2 frontmatter, template L1–61; live shape from UC2 L1–68)

The clean template frontmatter (`02_mdtm_template_complex_task.md` L1–61) defines the base keys. Recent reflect tasks **extend** it with reflect-specific keys. The builder MUST produce this superset (verified against UC2 L1–68 [CODE-VERIFIED]):

| Key | Source | FR-DRS value guidance |
|---|---|---|
| `id` | template L2 | `"TASK-RF-fr-drs-runtime-surface-20260622-000600"` (match the task dir name) |
| `title` | L3 | action-oriented one-liner naming FR-DRS + the 4-phase rollout |
| `description` | L4 | dense paragraph: greenfield module + 4 wire-ups + sync; name every edit site |
| `version` | L5 | `"1.0"` |
| `status` | L7 | `"🟡 To Do"` (start state; template options L6) |
| `type` | L9 | `"✨ Feature"` (greenfield module = feature; template options L8) |
| `priority` | L11 | `"🔥 Highest"` or `"🔼 High"` (template options L10) |
| `created_date` / `updated_date` | L12–13 | `"2026-06-22"` |
| `assigned_to` | L14 | `"rf-task-executor"` (UC2 L11) |
| `coordinator` | L17 | `orchestrator` |
| `parent_doc` / `parent_task` | L18–19 | point at FR-DRS spec/tdd (issue-3 dir) |
| `depends_on` | L20 | `[]` if standalone (UC2 L17 used `[]`) |
| `spec_path` | L23 | `".dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/spec.md"` — the driving spec; **populated by task-builder** (template comment L23 "populated by task-builder (A.2), empty if none") |
| **`start_commit`** | NOT in base template — reflect-extension key (UC2 L19) | `"<git merge-base HEAD origin/master at build time>"` with comment `# wrapper audit base = git merge-base HEAD origin/master at build time`. The POST reflect wrapper resolves the audit base from this. [CODE-VERIFIED UC2 L19] |
| **`executor_model_class`** | reflect-extension (UC2 L20) | `"opus"` with comment `# anti-self-confirmation: executor model class captured at build time` |
| `reflect_pre` | template L24–31 (block) | PRE reflect-gate sign-off block; task-builder writes it at A.10.7. UC2 L21–29 shows live shape: `verdict / skip_reason / coverage_pct / depth / tcs / run_id / report / reviewed_at`. |
| **`reflect_post`** | template L32 | `reflect_post: ""` — **preceded by the room comment** (UC2 L30): `# reflect_post is written by the POST reflect wrapper after the final-phase gate runs — do NOT hand-author or lock this block.` Leave the value empty string; the wrapper writes it. [CODE-VERIFIED UC2 L30–31] |
| `related_docs` | L33–39 | list of `{path, description}`: spec, tdd, the NEW module path, the SKILL.md demotion target, the eval registry |
| `related_prd` / `related_tdd` | L40–41 | tdd path if one exists |
| `tags` | L42–46 | e.g. `reflect, runtime-surface, deterministic-sweep, FR-DRS, eval-driven` |
| **`template_schema_doc`** | template L47 | `"src/superclaude/templates/workflow/02_mdtm_template_complex_task.md"` (UC2 L51 — points at the **src/** SoT copy, NOT `.claude/`) [CODE-VERIFIED] |
| `start_date` / `completion_date` / `blocker_reason` | L51–53 | empty at build (executor fills) |
| `task_type` | L60 | `static` (all FR-DRS items pre-enumerable; template L548 — dynamic only if items discovered at runtime) |

**Builder rule:** do NOT hand-author or lock `reflect_post` (template L161/UC2 reinforces in Execution Context). The room comment above the empty string is mandatory.

### 1b. Body sections (Part 2, template L1157–1516) — required, in this order

1. `# [Task Title]` (L1157)
2. `## Task Overview` (L1159) — what + why, one comprehensive paragraph.
3. `## Key Objectives` (L1163) — **numbered, bolded** list, one per FR/phase outcome. UC2 L78–90 tags each objective with its phase id, e.g. `1. **Source-of-truth ref (P1):** ...` — DO THIS: each objective maps to a phase and names the concrete deliverable + acceptance hook.
4. `## Prerequisites & Dependencies` (L1171) — sub-blocks: `### Parent Task & Dependencies` (L1173), `### Previous Stage Outputs (MANDATORY INPUTS)` (L1180, **INFORMATIONAL ONLY — NO CHECKLIST ITEMS**, L1182).
5. `## Execution Context` (L1193) — **builder MUST populate** (template L1195 "Every generated task file MUST have this section populated before the task file is marked ready"). Sub-sections:
   - `### References` (L1197) — governing docs/specs/workflow, format `- [Name](path): purpose`.
   - `### Source Areas` (L1201) — codebase dirs/modules read or modified, format `` - `path/`: what/why``.
   - `### Key Constraints` (L1205) — QA intensity, scope limits, known blockers, standing prohibitions.
   - `### Handoff File Convention` (L1209) — phase-outputs/ subdirs (discovery/, test-results/, reviews/, plans/, reports/).
   - `### Frontmatter Update Protocol` (L1223) — the 4 mandatory checkpoints.
6. `## Detailed Task Instructions` (L1233) — contains the orchestrator instruction block (L1235–1289, **REMOVE FROM OUTPUT**) then the phases.
7. Phases (`### Phase 1` … `### Phase N`, with `**Step X.Y:**` headers — see §3).
8. `## Post-Completion Actions` (L1423) — see §5.
9. `## Task Log / Notes 📋` (L1443) — with sub-sections: `### Task Summary` (L1445), `### Execution Log` (L1467), `### Phase N - [Name] Findings` (one per phase, L1477+), `### Phase Gate Findings` (L1498), `### Follow-Up Items Identified` (L1502), `### Deviations from Process` (L1508).

**D3 CRITICAL RULE (template L286–290):** NO checklist items may appear before Phase 1. Frontmatter → Execution Context (informational) → Phase 1 (first executable items). All context-review items live IN Phase 1, Steps 1.2–1.4.

---

## 2. The B2 Self-Contained Item Format (the 6-field paragraph)

**Template B2, L159–166.** EVERY checklist item is ONE FULL PARAGRAPH (B3, L167–170 — not bullets, not multi-line) that embeds all six elements:

1. **Context Reference + WHY** — what file(s) to read and why this context is needed for *this* action.
2. **Action + WHY** — what to do with that context and why.
3. **Output Specification** — exact output file name, absolute path, content to produce, template to follow.
4. **Integrated Verification** — an "ensuring..." clause (DO NOT assume/hallucinate; 100% derived from referenced source files; document negative evidence on failure).
5. **Evidence on Failure Only** — log to the `### Phase N Findings` section ONLY if blocked (success = the output file itself exists).
6. **Explicit Completion Gate** — verbatim: *"This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."*

**FORBIDDEN (B5, L181–201):** standalone "read context and log findings" items (no actionable output — lost on session rollover); items with no context reference; multi-line/bulleted items; separate verification/confirmation items (integrate via "ensuring…"); over-granular items ("create directory" alone); REMINDER blocks between items (E4, L387 — workers only see batch items, not surrounding prose).

**Why (B1, L151–157):** Rigorflow executes in batches across session rollovers; context loaded in batch 1 is gone by batch 3. Each item must be a complete prompt executable with zero prior context.

### Concrete example (the canonical B4 example, template L172–175)
```markdown
- [ ] Read the file `component-spec.md` at `docs/specs/component-spec.md` to extract the API interface requirements including all method signatures, parameter types, and return values that must be implemented, then read the file `BaseHandler.ts` at `src/handlers/BaseHandler.ts` to understand the structural patterns used in existing handlers, then create the file `ApiHandler.ts` at `src/handlers/ApiHandler.ts` containing a TypeScript class that implements all methods defined in the component spec with proper error handling, type annotations, and JSDoc comments following the patterns from BaseHandler, ensuring the file includes the standard header comment block, exports the class as the default export, all methods from the spec are implemented with correct signatures, no content is fabricated or assumed beyond what the source explicitly states, and no placeholder or TODO comments remain. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

**FR-DRS adaptation (real shape — modeled on UC2 L185/L197 build items):** for the greenfield-module phase, write one item that (1) reads the FR-DRS spec section + the existing reflect runtime-surface ref + a sibling module for conventions, (2) creates the new `.py` module at its exact `src/superclaude/...` path, (3) "ensuring" the public functions match the spec contract, no TODO stubs remain (RULES #7), all behavior derived from spec. Then a **separate L3 test item** runs `uv run pytest <module tests>` (I18, see §4).

---

## 3. A3 Granularity — break the 4 phases into per-UNIT items (not batch items)

**A3 (template L108–112):** "Create individual checklist items for EVERY file, component, or iteration. NO high-level or bulk operations allowed." **A4 (L114–133):** the iterative pattern — *pre-enumerate ALL items in an initial step → one checklist item per item → consolidate only after all complete*. **I2 (L522):** extreme granularity, exact file paths not directories.

**How this maps onto the FR-DRS 4-phase rollout** (module → product wire → eval wire → SKILL prose demotion). The builder MUST decompose, NOT batch. Pattern proven by UC2, which split a single FR into 8 phases with per-edit-site steps (UC2 L181–349):

| FR-DRS phase | WRONG (batch) | RIGHT (A3/A4 per-unit) |
|---|---|---|
| **P1 Module (greenfield)** | "Implement the FR-DRS module" | one build item per module file (`<module>.py`), one item per distinct public function/data-table if large, then one L3 test item (`uv run pytest …`) + one L5 assess item. UC2 split its `refs/runtime-surface.md` into author (Step 2.1) + verify (Step 2.2). |
| **P2 Product wire** | "Wire the module into the product" | one item per call-site / integration seam. Name each file:symbol. UC2 split contract wiring into per-gate-site edits (Step 3.3 lists "3 gate sites :663/:804/:1772 + 1 cosmetic :1641; :1558 auto-derives — do not edit"). Mirror that precision. |
| **P3 Eval wire** | "Add eval coverage" | one item PER eval case (UC2 Steps 7.2–7.6 = one item per case dir), one item for registry registration (Step 7.7), one L3 run item (Step 7.8), one L5 assess item (Step 7.9). |
| **P4 SKILL prose demotion** | "Update the SKILL" | one item per SKILL.md section being demoted/edited; one verify+sync item. UC2 used per-section edits (§5.3, §10.9, §9.1 each their own step). |

**Per-phase verify+sync item (UC2 idiom, e.g. L189/L209/L221):** after each phase's edits, UC2 adds a `**Step X.last:** Verify Phase X against [acceptance criteria] + DoD; then sync` item that runs `make sync-dev && make verify-sync`. For a component-edit task editing `src/superclaude/skills/...`, EVERY phase touching skill/agent/command source needs this (Core Rule #6: src/ → sync-dev → .claude/). The module phase (pure `src/superclaude/<pkg>/`) still tests via pytest; the SKILL-demotion phase needs the sync.

**Enumeration discipline (K2, L882–899):** the orchestrator/builder MUST identify and list ALL items at build time. The worker NEVER adds items dynamically (unless `task_type: dynamic` with DYNAMIC CONTENT markers — not needed for FR-DRS; use `static`).

---

## 4. QA-Gate Encoding (M3 / M4 / I19 / I20 / I21 / I22) — PER_PHASE gates

### 4a. This build = full intensity (I22, template L793–840)
FR-DRS is a Deep/Heavyweight reflect build → **`qa_intensity = full`** (I22 default mapping L806–809: Deep/Heavyweight → full). At full intensity, I19/I20/I21 apply unmodified (L834–836).

### 4b. Per-phase gate type & minimum agent floors
This is a **code-modifying task** (greenfield module + wiring). M2 applicability (L1052): code-modifying tasks get an **M3 lens-based gate (minimum 6 agents)** after the implementation phase. Because the build is PER_PHASE QA, each substantive phase boundary (where Phase N+1 depends on Phase N output) gets a gate.

**I19 / I15 floors [CODE-VERIFIED template L638, L702–711]:**
- **Final / assembled-output gate:** absolute minimum **6 agents** = 3 rf-qa (structural lenses) + 3 rf-qa-qualitative (content lenses), scaling by output size (L706–711: <500 lines→6, 500–1500→8, 1500–3000→10, >3000→12).
- **Intermediate gate** (research-gate / synthesis-gate / task-integrity): minimum **5 agents** = 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (L638, L731–737).
- Gates with fewer than these floors are **REJECTED** at task-file validation (L638). 1–2 agent QA is PROHIBITED.

**Standard 4 structural lenses (rf-qa, L715–720):** template-conformance, internal-consistency, evidence-quality, completeness.
**Standard 4 content lenses (rf-qa-qualitative, L721–726):** actionability, numbers-metrics, crossref-chain, domain-accuracy.
For a code build, swap in domain lenses (UC2 did: PG.2 "SKILL.md-edit-conformance + contract-additivity", PG.3 "blocker-ordering + counter-hygiene", PG.5 "fail-loud-doctrine-correctness", PG.6 "eval-falsifiability", PG.7 "no-scope-expansion-past-TDD" — UC2 L305–329). For FR-DRS pick code-appropriate domain lenses (e.g. "determinism/no-LLM-in-sweep", "no-TODO-stub", "contract-additivity", "eval-falsifiability").

### 4c. M3 lens-based sequence (template L1059–1096) — each step is its own `- [ ]`
The gate is a multi-item sequence (NEVER collapse; L1096). The clean-template Phase-Gate block (L1365–1402) gives the exact item skeleton. Order:
1. **PG.1 Aggregation (L6):** Glob all phase outputs → summary file at `${TASK_DIR}phase-outputs/reports/phase-N-output-summary.md`.
2. **PG.2…(structural lens agents, PARALLEL):** one `- [ ]` per rf-qa lens, `fix_authorization: false`, adversarial framing `"Assume this document has at least N errors in [lens]. Find them."` (N scales: 5/<500, 10/500–1500, 15/1500–3000, 20/>3000 — L729), report → `${TASK_DIR}qa/qa-structural-[lens]-report.md`.
3. **PG.3…(content lens agents, PARALLEL):** one `- [ ]` per rf-qa-qualitative lens, same shape, report → `${TASK_DIR}qa/qa-content-[lens]-report.md`. (PG.2+PG.3 MAY spawn in one parallel batch — L1080/L1378.)
4. **PG.4 Consolidation (I20 step 2):** read all lens reports → `${TASK_DIR}qa/qa-consolidated-findings.md`, deduplicated, originating lens noted.
5. **PG.4b Fix agent:** spawn **ONE** rf-qa with `fix_authorization: true` + consolidated findings — applies ALL fixes (I20 serialized; parallel fix authorization PROHIBITED — L745/L1086).
6. **PG.5 Verification round (PARALLEL):** minimum **2 agents** (1 rf-qa + 1 rf-qa-qualitative), `fix_authorization: false` → verify all findings addressed + no new issues.
7. **PG.5c Conditional proceed (L5):** IF both PASS proceed; IF either FAIL repeat PG.4–PG.5. Max cycles per I16 gate-type table (L660–667: research-gate 3, synthesis-gate 2, report-validation 3, task-integrity 2, qualitative 3, source-fidelity 3); on exhaustion HALT + escalate.

### 4d. I20 Serialized Fix Authorization (template L745–757)
Report → consolidate → ONE fix agent (`fix_authorization: true`) → verify (≥2). Rationale (L755): parallel fixers churn the same lines and contradict. Applies at ALL intensity levels (L838). Every step is an explicit `- [ ]`.

### 4e. M4 / I21 Source-Fidelity gate — applicability check for FR-DRS
**I21 (L759–788) + M4 (L1098–1121).** Fidelity gate is MANDATORY when output is *derived from source documents* (PRD/TDD/tech-ref/etc.). FR-DRS is a **code-modifying task implementing a spec**, NOT a doc-derivation task. M2 (L1052) says for code-modifying tasks the "Fidelity gate only if code was derived from spec documents." **Builder decision point:** FR-DRS code IS derived from the FR-DRS spec/TDD — a light fidelity gate (does the module/contract faithfully implement the spec's stated fields/behaviors?) is defensible and UC2-aligned. If included, it runs AFTER the M3 gate (L788 ordering), minimum 2 fidelity agents (L784), reports → `${TASK_DIR}qa/qa-source-fidelity-report-N.md`. If the builder judges the spec→code mapping mechanical, it may note "Fidelity gate not applicable — [reason]" (template L1437 allows this). **Recommendation:** include it (the spec has concrete contract scalars the module must emit — exactly the detail-preservation M4 checks).

### 4f. F2 prohibitions the gate enforces (template L422–429)
- No delegating across phase boundaries (a subagent gets a SINGLE checklist item).
- No skipping phase-gate QA (must spawn lens-based M3 after Phase 2+).
- No skipping post-completion validation (rf-qa structural + rf-qa-qualitative operational before Done — I17).

---

## 5. POST Reflect Gate item — EXACT shape (penultimate final-phase item) + Update-to-Done

This is the highest-fidelity deliverable. The exact, working, flat-wrapper item is **UC2 L363** [CODE-VERIFIED]. The FR-DRS builder MUST reproduce this shape, substituting the FR-DRS absolute task-file path.

### 5a. The POST reflect wrapper item (penultimate item in the FINAL phase / Post-Completion)
Key invariants of the canonical item (all present in UC2 L363):
- It is the **PENULTIMATE** item (immediately before the Update-status-to-Done terminal item).
- **Single Bash command:** recursion-breaker skip guard FIRST, THEN the wrapper, joined with `;`.
- **Skip guard (verbatim):** `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi;`
- **Flat wrapper invocation:** `superclaude reflect run <ABSOLUTE-TASK-FILE-PATH> --depth deep --fix --promote`
- **Explicitly NO:** broad staging, NO `git add -A`, NO `--base`, NO `--reflect`, NO `<base>..HEAD` range, NO agent-spawn. The wrapper internally launches `/sc:reflect --mode post` as an **executor-disjoint** `claude --print` subprocess and writes `reflect_post` back to frontmatter; the audit base resolves from the frontmatter `start_commit`.
- **Consume the exit code:** ONLY exit 0 completes the gate. **exit 10 / 11 / 2 = FAIL** → surface the wrapper's report path and **HALT** (do NOT mark this item or the task complete; record the halt + report path in the Task Log). On a non-halting completion, route reported deviations to remediation or append to an `### Open Questions` block (**never delete a deviation**).
- **Blocker clause:** if the wrapper can't run (binary missing) or exits non-zero, log to `### Phase N - Release Findings`, then HALT — do NOT mark the subsequent Update-to-Done item.
- Completion gate: mark complete only once the wrapper exited 0 AND `reflect_post` was recorded.

**Verbatim FR-DRS item (substitute the absolute path):**
```markdown
- [ ] Run the independent post-execution reflection gate (the canonical FLAT POST reflect wrapper shell-out) as the PENULTIMATE item: use the Bash tool to run, as a single command, FIRST the recursion-breaker skip guard and THEN the wrapper, with NO broad staging and specifically NO `git add -A` (the wrapper resolves the audit base from `start_commit`) — `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi; superclaude reflect run /config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-fr-drs-runtime-surface-20260622-000600/TASK-RF-fr-drs-runtime-surface-20260622-000600.md --depth deep --fix --promote` — with NO `--base`, NO `--reflect`, NO `<base>..HEAD` range, and NO agent-spawn (the wrapper internally launches `/sc:reflect --mode post` as an executor-disjoint `claude --print` subprocess and writes `reflect_post` back to this file's frontmatter; the audit base resolves from the frontmatter `start_commit`), then consume the exit code: ONLY exit 0 completes this gate; exit 10 / 11 / 2 means FAIL — surface the wrapper's report path and HALT (do NOT mark this item or the task complete; record the halt and the report path in the Task Log), and on a non-halting completion route any reported deviations to remediation or append them to a `### Open Questions` block (never delete a deviation), ensuring the wrapper exited 0 and `reflect_post` was recorded before proceeding. If the wrapper cannot run (binary missing) or exits non-zero, log the specific blocker and the report path using the templated format in the `### Phase 8 - Release Findings` section of the `## Task Log / Notes` at the bottom of this task file, then HALT — do NOT mark the subsequent Update-status-to-Done item complete. Once the wrapper has exited 0 and `reflect_post` is recorded, mark this item as complete.
```
> Adjust the `### Phase N - Release Findings` name to the FR-DRS final phase number, and the absolute task-file path. The `start_commit` frontmatter key MUST be populated for the audit base to resolve (§1a).

### 5b. The Update-status-to-Done TERMINAL item (UC2 L365 [CODE-VERIFIED])
Immediately follows the wrapper item. It is the TERMINAL item and may only proceed after the wrapper exited 0 and `reflect_post` was recorded:
```markdown
- [ ] Update `completion_date` and `updated_date` to today's date and update task `status` to "🟢 Done" in the frontmatter (this is the TERMINAL item — it may only proceed after the POST reflect wrapper above exited 0 and `reflect_post` was recorded), then add an entry to the `### Execution Log` in the `## Task Log / Notes` section using the format: `**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.` Once done, mark this item as complete.
```

### 5c. Placement & ordering (anti-orphaning)
The wrapper + Done items live at the END of `## Post-Completion Actions` (template L1423–1441), AFTER: (1) the Glob output-existence check (L1425), (2) the test-suite re-run check (L1427), (3) the **POST-COMPLETION lens-based M3 QA** placeholder (L1435 — builder MUST expand into per-agent items per Steps PG.2–PG.5; I17 item 5), (4) the **POST-COMPLETION source-fidelity** placeholder (L1437; I17 item 6, if applicable), (5) the Task Summary item (L1439). The wrapper is penultimate, Done is terminal. There is exactly ONE reflect wrapper item per task (UC2 L363 is the only occurrence).

---

## 6. Effective patterns from the real UC2 exemplar (cite: `TASK-RF-uc2-reachability-20260620-025931.md`)

The UC2 task is the closest structural model for FR-DRS (same reflect-skill family, same eval pipeline, same POST_REFLECT_GATE, same start_commit/executor_model_class extensions). Mined patterns [all CODE-VERIFIED by line]:

1. **Phase-id-tagged objectives** (L78–90): each `## Key Objectives` entry names its phase id + concrete deliverable + which FR/acceptance it satisfies + a dependency note (e.g. "This file BLOCKS every subsequent edit"). Carry FR-DRS's per-phase blocking order into the objectives.
2. **BLOCKS ordering encoded in phase headers** (L181: "Phase 2: … (P1; BLOCKS all subsequent phases)"). Make the greenfield module phase explicitly block the wire-up phases.
3. **Per-edit-site precision with "do not edit" carve-outs** (L205/Step 3.3: names :663/:804/:1772 as edit sites, :1641 cosmetic, ":1558 auto-derives — do not edit"). FR-DRS wiring items should name exact symbols/sites and call out anything that must NOT be touched.
4. **Per-phase Verify+Sync step** (Steps 2.2, 3.4, 4.2, 5.3, 6.3 — L189/L209/L221/L237/L253): each phase ends with a verify-against-acceptance-criteria + `make sync-dev && verify-sync` item. Mandatory for any phase editing `src/superclaude/skills/`.
5. **Eval phase = one item per case + register + run(L3) + assess(L5)** (Steps 7.2–7.9, L269–296): exactly the A4 iterative pattern. FR-DRS P3 (eval wire) mirrors this.
6. **Full M3 gate with domain lenses** (Phase Gate, L297–340): 6 lens agents (3 structural + 3 content) named by domain, then consolidate (PG.8/L329), ONE serialized fix agent (PG.9/L333), verification round max-3-cycles (PG.10/L337). This is the canonical full-intensity gate to copy.
7. **POST reflect wrapper as penultimate item + Done as terminal** (L363–365) — see §5.
8. **Working-tree / SoT-discipline baseline check in Phase 1** (Step 1.3, L177: "Verify the working tree and source-of-truth discipline baseline"). Good practice for src/-editing tasks: a Phase-1 item asserting clean tree + correct branch before edits.
9. **Frontmatter Execution-Context reinforcement** (L161): repeats "The `reflect_post` block is written by the POST reflect wrapper — do NOT hand-author or lock it." in the Execution Context's Frontmatter Update Protocol.
10. **`blocker_reason` as a real audit trail** (L62–63): when a phase is deferred, UC2 records a dense, evidence-bearing blocker_reason. FR-DRS itself EXISTS because UC2 deferred its structured-output guarantee to FR-DRS (UC2 L62 names `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/spec.md`) — confirming the spec_path the builder should target.

---

## Summary for the builder

- **Template:** `02_mdtm_template_complex_task.md` Part 2 (L1157–1516) is the skeleton; copy section order exactly. Point `template_schema_doc` at the **`src/`** copy.
- **Frontmatter:** base keys + reflect extensions `start_commit` (audit base) + `executor_model_class: "opus"` + `reflect_pre` block + `reflect_post: ""` preceded by the do-not-author room comment. `spec_path` = the FR-DRS spec. `task_type: static`.
- **Items:** every item is a single B2 6-field paragraph; no standalone reads, no separate verification items, no multi-line items.
- **Granularity (A3/A4):** decompose each of the 4 phases into per-file / per-call-site / per-eval-case items + a per-phase verify+sync item; pre-enumerate all items at build time.
- **PER_PHASE QA (full intensity, I22):** M3 lens-based gate at each dependent phase boundary, ≥6 agents (3 rf-qa + 3 rf-qa-qualitative, domain lenses for a code build), `fix_authorization: false` on lens agents, ONE serialized fix agent (I20), ≥2 verification agents, conditional-proceed with max-cycle HALT. Every step is its own `- [ ]`. Optional M4 fidelity gate (spec→code) after the M3 gate.
- **Code-task obligations:** I18 testing item (`uv run pytest …`) in each implementation phase; I17 post-completion lens QA + output-existence Glob + test re-run before Done.
- **POST reflect gate:** the verbatim UC2 L363 flat-wrapper item (skip guard `;` wrapper, `--depth deep --fix --promote`, NO base/range/staging, consume exit code, exit 0 only, HALT on 10/11/2) as the **penultimate** item; the UC2 L365 Update-to-Done item as **terminal**.
- **Anti-orphaning:** completion items (Glob check, test re-run, lens QA, fidelity, Task Summary, wrapper, Done) all in `## Post-Completion Actions` in that order.

**Deliverable file:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-fr-drs-runtime-surface-20260622-000600/research/08-mdtm-template-and-examples.md`
