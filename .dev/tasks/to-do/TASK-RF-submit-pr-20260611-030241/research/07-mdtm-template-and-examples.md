# R7 — MDTM Template-02 Rules & Prior-Art Patterns

Status: In Progress

Scope: meta-layer only (template rules + how-to-structure the generated task file). Codebase/spec content covered by R1–R6.

All citations are to `.claude/templates/workflow/02_mdtm_template_complex_task.md` (the Template-02 source; 1515 lines) unless noted. Prior-art exemplars cited by absolute path.

---

## 1. Template-02 PART 1 Rules (builder-only; NOT emitted into output task file)

PART 1 spans lines 66–852 and is for the orchestrator/task-builder only — "NONE of this content appears in the actual output task file" (`:73-75`). The clean structure the builder emits lives in PART 2 (`:1180`+). Template-02 = Template-01 + Section L (intra-task handoff patterns) (`:78`).

### Section A — Granularity & iteration

- **A3. Complete Granular Breakdown** (`:108-112`): break EVERY phase into atomic, verifiable checklist items; one item per file/component/iteration; NO bulk/high-level operations; include exact file paths + measurable outcomes.
- **A4. Iterative Process Structure** (`:114-133`): for any multi-item process — (1) pre-enumerate ALL items in an initial discovery step, (2) one checklist item per item, (3) incremental updates after each, (4) a consolidation step ONLY after all items complete. The `Step X.1 scan/enumerate → Step X.2 per-item → Step X.3 consolidate` shape is given verbatim at `:121-133`.
- **A5. Cross-Stage Integration** (`:135-139`, workflow-dependent): every phase explicitly names inputs (file paths) from prior stages; validate against prior-stage findings before proceeding.

### Section B — Self-contained items (CRITICAL)

- **B1. Session-rollover protection** (`:151-157`): tasks execute in batches across sessions; context loaded in batch 1 is GONE by batch 3+. So standalone "read context" items are useless.
- **B2. Six mandatory elements per item** (`:159-165`): every `- [ ]` item is ONE self-contained prompt that includes:
  1. **Context Reference + WHY** — which file(s) to read and why for THIS action
  2. **Action + WHY** — what to do and why
  3. **Output Specification** — exact output file name + path + content + template to follow
  4. **Integrated Verification** — an "ensuring…" clause (no fabrication; 100% derived from cited source files; document negative evidence)
  5. **Evidence on Failure Only** — log a blocker to Task Log ONLY if blocked (the output file IS the success evidence)
  6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions are completed in their entirety… Once done, mark this item as complete."
- **B3** (`:167-170`): each item is ONE FULL verbose paragraph (not bullets), readable as a standalone executable prompt. Canonical correct example at `:174`.
- **B4 NOTE / B5 FORBIDDEN** (`:177-182`): do NOT create separate verification items (verification is the "ensuring…" clause); FORBIDDEN: standalone read-context items, separate verify/confirm items, multi-line/bulleted items, over-granular items (e.g. "create directory" alone — fold it into the file-creation that needs it).

### Section L — Intra-task handoff patterns (the Template-02 differentiator)

Each pattern has a canonical self-contained example in PART 1; the same patterns are mirrored as PART 2 fill-in stubs.

- **L1. Discovery item** (`:928-937`): Glob/enumerate → write a consolidated inventory to `phase-outputs/discovery/`. Use to scan before building.
- **L2. Build-from-Discovery** (`:940-949`): read the discovery inventory + source → create the deliverable.
- **L3. Test/Execute** (`:952-961`): Bash a test/build command → write raw output to `phase-outputs/test-results/<name>.txt` AND a structured `<name>.md` summary (PASSED/FAILED + counts + failure table). **This is the pattern Template-02 mandates for testing items** (`:695`: "For Template 02 tasks: use the L3 (Test/Execute) pattern for testing items").
- **L4. Review/QA** (`:964-973`): read output + source + inventory → write a PASS/FAIL verdict file to `phase-outputs/reviews/`.
- **L5. Conditional-Action** (`:976-987`): read a result → IF pass write a verdict; IF fail read raw output, root-cause each failure, write a `fix-plan.md`. This is how build-order gating / fix-cycle branching is encoded.
- **L6. Aggregation** (`:990-999`): Glob all per-item outputs → consolidate into a single report.
- **L7. Pattern Selection Guide + composition flows** (`:1003-1026`): maps intent→pattern. The code+test flow is given as `Phase 2: K1/K2 (build items) → L3 (run tests) → L5 (conditional: fix or proceed)` (`:1019-1020`), and the QA-gated flow as `L1 → L2 → **M3 (QA Gate)** → L3 → L5 → L4 → L6 → **M3 (QA Gate)**` (`:1026`).

### Section M — QA gate composite patterns

- **M1** (`:1034-1045`): LEGACY single-agent QA. **DEPRECATED — new task files MUST NOT use M1; they MUST use M3.**
- **M2. Phase-gate placement** (`:1047-1057`): for **Code-modifying tasks** — gate "After implementation phase and before testing phase (if testing is separate), or after combined implement+test phase… M3 lens-based (minimum 6 agents per I19). Fidelity gate only if code was derived from spec documents" (`:1052`).
- **M3. Lens-Based QA Sequence** (`:1059-1096`) — the mandated gate composite. 8 steps: (1) L6 aggregation of phase outputs; (2) structural-lens rf-qa agents in PARALLEL, `fix_authorization: false`; (3) content-lens rf-qa-qualitative agents in PARALLEL, `fix_authorization: false`; (4) optional domain-lens agents; (5) consolidate findings → `${TASK_DIR}qa/qa-consolidated-findings.md`; (6) ONE rf-qa fix agent `fix_authorization: true`; (7) verification round (≥2 agents) `fix_authorization: false`; (8) L5 conditional proceed — IF both verify PASS proceed, ELSE repeat 5–7 up to I16 max cycles, then HALT+escalate. Every step is an explicit `- [ ]` item (`:1121`).
- **M4. Source-Document Fidelity Gate** (`:1098-1121`): runs AFTER M3 (`:1119` ordering — "document must be structurally sound before checking fidelity"). Fidelity agents read BOTH source inputs AND the generated output to verify faithful representation. Same report→consolidate→fix→verify cycle.

### Section I — counts, serialization, applicability, intensity

- **I19. Lens-based QA minimum agents** (`:699-743`): FLOORS for the final/output gate scale by size — `<500 lines`: **6** (3 rf-qa structural + 3 rf-qa-qualitative content); `500-1500`: **8** (4+4); `1500-3000`: **10**; `>3000`: **12** (`:706-711`). Standard 4 structural lenses (template-conformance, internal-consistency, evidence-quality, completeness) + 4 content lenses (actionability, numbers/metrics, crossref-chain integrity, domain-accuracy) (`:715-725`). Adversarial framing N scales: 5 / 10 / 15 / 20 (`:729`). Intermediate-gate floors = **5** agents (research-gate / synthesis-gate / task-integrity tables at `:733-737`). NOTE (`:700`): I19 tables are FULL-intensity; lite/standard use reduced counts per I22.
- **I20. Serialized fix authorization** (`:745-757`): when 3+ agents touch one file, fixes MUST be serialized — report (all, `fix_authorization: false`) → consolidate → **ONE** fixer (`fix_authorization: true`) → verify (≥2) → cycle-control (max per I16; HALT after 3). Parallel fix authorization is PROHIBITED. Every protocol step is an explicit `- [ ]` item (`:757`). Applies at ALL intensity levels (`:838`).
- **I21. Source-document fidelity applicability** (`:759-788`): MANDATORY when output is derived from source docs (PRD/TDD/roadmap/tech-ref/README/tech-research/repo-cleanup, "Any task where the orchestrator reads source documents to produce output" `:771`). NOT required for pure mechanical transforms / config-only tasks (`:773-775`). Min 2 fidelity agents (partition to 3-4 if sources >1000 lines). Runs AFTER M3 (`:788`).
- **I22. QA intensity levels** (`:793-840`): three levels with reduced counts. **Default mapping** (`:806-809`): Quick/Lightweight→**lite**, Standard→**standard**, Deep/Heavyweight→**full**.
  - **lite**: intermediate 2, final-gate **3** (1 structural + 1 content + 1 domain, combined lenses), fidelity 1 (combined), 1 fix cycle, 1 verification (`:802`, `:816-823`).
  - **standard**: intermediate 3, final-gate **7** (3 structural + 3 content + 1 domain), fidelity 2, 2 fix cycles, 2 verification (`:803`, `:825-832`).
  - **full**: per I19 tables (5+ intermediate, 6-12+ final), all domain lenses, fidelity per I21, fix cycles per I16, 2 verification (`:804`, `:834-836`).
  - **User override** allowed (e.g. "deep but lite QA") (`:811-814`).
  - Serialized fix (I20) is NEVER bypassed, even at lite (`:838-840`).

### F/C discipline (execution + prohibitions)

- Phase-gate QA cannot be skipped (`:428`): proceeding to the next phase without a passing QA gate is PROHIBITED.
- Min-agent prohibition (`:638`): final/assembled-output gates floor at 6 agents; intermediate gates at 5; sub-floor gates are REJECTED at task-file validation.
- Post-completion lens-QA + fidelity gate are MANDATORY in `## Post-Completion Actions` BEFORE the frontmatter Done-flip (`:681-684`).

---

## 2. PART 2 emitted-structure requirements

The builder emits (PART 2, `:1`-frontmatter through `:1498`):

### Frontmatter (`:1-55` template; richer in prior art)

YAML frontmatter with: `title`, `description`, `status` ("🟡 To Do" initial), `type` (pick from the enum at `:8` — e.g. "🐛 BugFix", "✨ Feature", "🔧 Refactor", "✅ Verification/QA"), `priority`, plus (from the troubleshoot exemplar `:14-55`): `coordinator`, `spec_path`, **`reflect_pre:` block** (`verdict`/`coverage_pct`/`depth`/`tcs`/`run_id`/`report`/`reviewed_at`), **`reflect_post: ""`**, `related_docs`, `tags`, `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"`, `start_date`/`completion_date`/`blocker_reason`, `task_type`. The prd exemplar additionally uses `start_commit` (captured in Step 1.3, consumed by the POST-reflect diff).

### Body sections (in order)

1. `## Task Overview` (`:59`) — one-paragraph what+why.
2. `## Key Objectives` (`:67`).
3. `## Prerequisites & Dependencies` (`:79`).
4. **`## Execution Context`** (`:1193-1231`) — **MANDATORY, builder MUST populate** (`:1195`). Four required sub-sections:
   - `### References` — governing docs/specs/workflow (`:1197-1199`)
   - `### Source Areas` — codebase dirs/modules read or modified (`:1201-1203`)
   - `### Key Constraints` — QA intensity, scope limits, known blockers, standing prohibitions (`:1205-1207`)
   - `### Handoff File Convention` — declares `phase-outputs/{discovery,test-results,reviews,plans,reports}/` (`:1209-1221`)
   - `### Frontmatter Update Protocol` — mandatory checkpoints: Doing on start, Done on completion, Blocked + `blocker_reason` if blocked, `updated_date` each session (`:1223-1231`)
5. `## Open Questions` (prior art) — human-decision / deferred items.
6. `## Detailed Task Instructions` (`:1233`) — the phases. Each phase header `### Phase N: …`, files grouped under `#### File: …` headers WITHOUT checkboxes (`:1242-1243` warning: never put a parent/summary checkbox before its components; summaries last), then per-item `- [ ]` paragraphs. Phase 1 always opens with the status→Doing + Execution-Log item (`:1322-1323`).
7. **`## Post-Completion Actions`** (`:1423-1441`) — order: (a) post-completion lens-QA + fidelity validation items (I17/`:681-684`), (b) `### Task Summary` item, (c) POST `/sc:reflect` gate item, (d) final status→Done flip (LAST item, `:1441`).
8. **`## Task Log / Notes 📋`** (`:1443`-end) — contains `### Task Summary` (filled post-completion), `### Execution Log` (timestamped `**[YYYY-MM-DD HH:MM]** - …` entries), and per-phase `### Phase N - <name> Findings` blocker sinks (`:1477`, `:1487`, `:1496`) + `### Phase Gate Findings` (`:1498`). EVERY item's "log the specific blocker using the templated format in the ### Phase N Findings section" clause points here.

---

## 3. Effective prior-art patterns (2 exemplars)

### Exemplar A — `TASK-RF-prd-local-file-20260609-005242/` (code+test build, FINAL_ONLY lite)

Closest structural match to "Deep single-track code+test build" at the small-change end. Phases:
- **Phase 1** Preparation, Setup, Anchor Re-Verification (status-flip item + phase-outputs dir creation `:164`).
- **Phase 2-3** surgical source edits (`process.py`, then `prompts.py`), each item an enumerated **EXPLICIT ENUMERATED COMPLETION GATE** listing every sub-behavior that must be independently verified (`:222` — a single ~2-paragraph item with in-item measurable evidence: `uv run python -c "ast.parse(...)"` + a `grep -n -e … ` token-survival check).
- **Phase 4** Tests (invert assertions + add coverage).
- **Phase 5** Verification — grep guard + pytest + sync/verify-sync drift guard, as concrete L3 Bash command items (`:274`).
- **Phase 6** Final Validation = **FINAL_ONLY lite gate** (`:282-284`): 3 lens agents (1 structural rf-qa + 1 content rf-qa-qualitative + 1 domain SOURCE-FIDELITY rf-qa) all `fix_authorization: false` → consolidate (any-fail-is-fail, I16) → ONE serialized fixer `fix_authorization: true` (1 cycle max) → ONE verification agent. Each agent item embeds the byte-exact adversarial framing string `ADVERSARIAL STANCE: Assume this work contains at least 5 errors focused on your lens. Find them…`.
- **Post-Completion**: a NON-BLOCKING manual-acceptance note item (`:324`), then the **INDEPENDENT POST-EXECUTION REFLECTION GATE (FRESH SESSION, HALT)** (`:326`), then the Done-flip (`:328`).

**POST `/sc:reflect` encoding (the load-bearing pattern, `:326`):** the item writes `reflect_post: PENDING` to frontmatter and **STOPS** (does NOT run reflect inline — executor's frame is biased), surfacing a single-line paste-ready command:
`/sc:reflect --mode post --remediate --diff <START_COMMIT>..HEAD --tasklist <task.md> --spec <driving-spec> --depth standard --executor-model <EXECUTOR_CLASS>`. Invariants the item asserts: depth is `standard` (NEVER `quick`) — the POST floor; the command names `/sc:reflect` and NEVER `/sc:task`; `--spec` points at the driving spec; the item does NOT self-resolve — it HALTs the Done-flip until the operator records `reflect_post: {verdict, run_id, report}`.

### Exemplar B — `TASK-RF-troubleshoot-hardening-20260610-144537/` (full-intensity M3+M4)

Docs/refs build at full intensity — shows the heavier gate. Phase 1 includes a G-gate acknowledgement step (`:13` "Record the G1 approval acknowledgement (NOT a blocking HALT)"). Phase 4 is the full M3 gate (`:286`): **8 lens agents (4 rf-qa structural + 4 rf-qa-qualitative content)** for the 500-1500 changed-line tier, N=10 adversarial framing, opening with an L6 `qa-input-manifest.md` aggregation (`:292`), then serialized fix, then verification, max 3 cycles. Post-Completion POST-reflect item (`:388`) is the **PENULTIMATE** item, computes `<BASE>` as `git merge-base HEAD <integration-branch>` (resolved via `git symbolic-ref`), runs `git add -A` first so untracked new files enter the diff surface, passes the base as a SINGLE ref (working-tree diff, not `start..HEAD`), depth `deep` (justified by cross-subsystem + 10-acceptance + protocol-class scope), records `{verdict, run_id, report}` into `reflect_post`, appends (never deletes) deviations to `### Open Questions`.

---

## 4. Recommendation: phase structure + QA-gate encoding for a Deep, single-track, code+test build with a hard build-order DAG (detection-contract gate first)

For a Deep-tier code+test feature with a hard build-order DAG where a **detection-contract gate must be built and proven first** before downstream consumers, the generated Template-02 file should use:

**Intensity:** Deep tier → default `qa_intensity = full` (I22 `:806-809`). For a single-track code change of moderate size (<1500 changed lines) the Exemplar-A FINAL_ONLY pattern is acceptable IF the build-request scopes it as such; otherwise use a real M3 phase-gate (I19 floor: 6 agents <500 lines, 8 at 500-1500). State the chosen intensity + agent count explicitly in `### Key Constraints` (as both exemplars do).

**Encode the build-order DAG with L5 gating, not prose.** The detection-contract-first ordering is a hard dependency, so:

1. **Phase 1 — Preparation + Contract Anchor Verification:** status→Doing item; create `phase-outputs/{discovery,test-results,reviews,plans,reports}/` + `qa/`; an L1 discovery item that enumerates the exact contract surface (the detection function/schema and every downstream call site) to `phase-outputs/discovery/contract-inventory.md` so later items read it by path (A4 pre-enumeration; survives rollover).
2. **Phase 2 — Build the detection-contract gate FIRST (the DAG root):** one self-contained B2 item per contract file/symbol, each with an **EXPLICIT ENUMERATED COMPLETION GATE** (Exemplar-A `:222` style) listing every sub-behavior + an in-item measurable check (`uv run python -c "ast.parse(...)"` + token-survival grep). End the phase with an **L3 contract-proof test item** (`uv run pytest <contract tests> -q`) writing raw + summary to `phase-outputs/test-results/`, then an **L5 conditional gate item**: IF the contract tests PASS write a `contract-verdict.md` and authorize Phase 3; IF FAIL write a `fix-plan.md` and HALT — downstream phases MUST NOT start until this verdict is PASS. This L5 item is the DAG edge: it makes "detection-contract gate first" a mechanical gate, not a comment.
3. **Phase 3+ — Build downstream consumers** (one B2 item per file), each item's Context Reference explicitly reading `contract-inventory.md` + the now-proven contract (A5 cross-stage integration), so they bind to the verified contract.
4. **Phase N (testing) — L3 Test/Execute** (Template-02 mandates L3 for testing, `:695`): run the full suite + `make verify-sync` / lint as concrete Bash items; capture raw + summary; an L5 conditional fix-or-proceed item.
5. **Phase N+1 — Final QA Gate (M3, full intensity):** L6 aggregation manifest → parallel structural rf-qa + content rf-qa-qualitative lens agents (`fix_authorization: false`, per-lens prompt, byte-exact adversarial framing with N by size) → consolidate to `qa/qa-consolidated-findings.md` → ONE serialized fixer (`fix_authorization: true`, I20) → ≥2-agent verification → L5 conditional (max 3 cycles then HALT). Because this is **code derived from a spec/detection-contract**, append an **M4 source-fidelity gate** AFTER M3 (I21 applies — orchestrator read source docs to produce output): ≥2 fidelity agents reading BOTH the spec/contract AND the edited files.
6. **Post-Completion:** post-completion lens-QA verification of final state (I17) → `### Task Summary` item → **POST `/sc:reflect` HALT gate** (Exemplar-A `:326` shape — write `reflect_post: PENDING`, STOP, surface the single-line `/sc:reflect --mode post --remediate --diff <BASE> --tasklist … --spec … --depth deep --executor-model …`; depth `deep` for a Deep-tier multi-file build per Exemplar-B; named `/sc:reflect` never `/sc:task`; computes `<BASE>` as `git merge-base HEAD origin/master` and `git add -A` first so new files enter the diff) as the PENULTIMATE item → status→Done flip as the LAST item.

**Every QA agent spawn, the consolidation, the single fixer, and each verification agent are individual `- [ ]` items** (I20 `:757`, I15) — never a single "run QA" bullet. The build-order DAG is enforced by the Phase-2 L5 contract-verdict gate that withholds authorization for Phase 3+ until the contract tests pass.

---

Status: Complete

### Summary

Documented all Template-02 PART 1 rules with IDs (A3/A4/A5, B1-B5, L1-L6/L7, M1-M4, I19/I20/I21/I22, F/C prohibitions) and the PART 2 emitted structure (frontmatter incl. `reflect_pre`/`reflect_post`, mandatory `## Execution Context` with its 5 sub-sections, phase body conventions, `## Post-Completion Actions` ordering, `## Task Log / Notes` with per-phase Findings sinks). Cross-checked against 2 prior-art exemplars: the prd-local-file code+test build (FINAL_ONLY lite gate + the load-bearing POST `/sc:reflect` HALT-gate paragraph) and the troubleshoot-hardening docs build (full M3 8-agent gate + M4 + penultimate working-tree-diff reflect gate). Section 4 gives the concrete recommendation for the Deep single-track code+test build with a detection-contract-first DAG: encode the build-order dependency as a **Phase-2 L5 contract-verdict gate** that withholds authorization for downstream phases until contract tests pass (mechanical, not prose), full-intensity M3 (6-8 agents by size) + M4 fidelity gate (code-from-spec → I21 applies), and a penultimate POST `/sc:reflect --mode post --depth deep` HALT gate computing `<BASE>` via `git merge-base HEAD origin/master`.
