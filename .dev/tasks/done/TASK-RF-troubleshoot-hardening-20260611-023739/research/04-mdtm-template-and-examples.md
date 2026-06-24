# Research: MDTM Template 02 + Examples

> ⚠️ **SUPERSEDED (design conclusions only):** This file was researched against the older DRAFT spec. Its CODEBASE anchors (SKILL.md headings/lines, refs house-style, sync model, MDTM mechanics) are VALID and re-verified. But its DESIGN CONCLUSIONS (ref count, output-contract field count, testing scope, draft §6.2/§7/§9 section numbers) are STALE — see `08-v1.1.0-deliverable-reconciliation.md` + `07-release-spec-structure.md` (AUTHORITATIVE for v1.1.0: 6 refs, 10+1 fields incl. waiver_status/contract_version/backtest_status, 17+6 tests, advisory REQUIRED).


**Topic type:** Template & Examples
**Scope:** template 02 PART 1 + TASK-RF examples
**Status:** Complete
**Date:** 2026-06-10

---

## 1. Template 02 PART 1 — Structure Rules

**Template path:** `.claude/templates/workflow/02_mdtm_template_complex_task.md` (1515 lines; PART 1 = lines 1-1127, PART 2 template = lines 1143+).

### 1a. Required frontmatter (lines 1-61)

All fields between the opening/closing `---` at lines 1/61. Builder MUST populate (not leave as `[...]` placeholders):
- `id` (line 2): `TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS` — for this track: `TASK-RF-...` form already chosen.
- `title`, `description`, `status` (default `🟡 To Do`, line 7), `type` (this is a **`📚 Documentation`** task per line 9 default), `priority`, `created_date`, `updated_date`, `assigned_to`, `coordinator: orchestrator`.
- `depends_on` (lines 20-22) — list or empty.
- `spec_path` (line 23): *"driving spec/PRD/TDD path; populated by task-builder (A.2), empty if none."* For this track the SOURCE spec is the troubleshoot hardening source material → set `spec_path` to it (drives the M4 fidelity gate and the POST-reflect `--spec`).
- `reflect_pre` block (lines 24-31): `verdict / coverage_pct / depth / tcs / run_id / report / reviewed_at` — populated by task-builder at A.10.7 (PRE reflect gate).
- `reflect_post` (line 32): `""` initially — *"POST reflect verdict; recorded by the executor after the final-phase reflect subagent runs."*
- `related_docs`, `tags`, `task_type: static` (line 60).

### 1b. Mandatory sections + ordering (Section D, lines 250-289)

Per **D3 (line 286, CRITICAL RULE):** NO checklist items before Phase 1. Document order is:
`Frontmatter → Workflow Compliance (informational, D1) → Prerequisites/Cross-Stage (informational, D2) → Phase 1 (first executable) → ... → Post-Completion Actions`.
- D1/D2 are **INFORMATIONAL ONLY — NO checklist items** (lines 262, 268). All context-review + previous-stage-input reads go INTO Phase 1, Steps 1.2-1.4 (lines 272, 289).
- Both D1 and D2 are `[WORKFLOW-DEPENDENT]`; if no `.gfdoc/.roo` workflow docs exist (A1, lines 89-100), omit workflow-specific sections and derive requirements from user input directly. **This track has no governing workflow doc → omit D1/D2 workflow framing, keep granular breakdown.**

### 1c. B2 — Self-Contained Item Pattern (5+1 components, lines 159-166)

Every `- [ ]` item is ONE complete, self-contained paragraph (B3, line 167) embedding:
1. **Context Reference with WHY** — what file(s) to read + why (line 160)
2. **Action with WHY** — what to do + why (line 161)
3. **Output Specification** — exact output file name, location, content, template to follow (line 162)
4. **Integrated Verification** — an *"ensuring..."* clause; NO fabrication, 100% source-derived, document negative evidence (line 163)
5. **Evidence on Failure Only** — log to task notes ONLY on blocker/error; success is evidenced by the output file itself (line 164)
6. **Explicit Completion Gate** — *"This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."* (line 165)

**Rationale (B1, lines 151-157):** session-rollover protection — context loaded in an early batch is gone by batch 3+, so standalone "read context" items are USELESS.

**FORBIDDEN (B5, lines 181-200):** standalone "read context" items with no output; missing context reference; multi-line/bulleted items (must be single paragraph); separate verification/confirmation items (integrate via "ensuring..."); over-granular items ("create directory" alone); separate REMINDER blocks.

> **NOTE for examples below:** Several recent TASK-RF files use a structured **multi-line bullet item form** (`- **Context** / **Action** / **Output** / **Verification** / **Completion gate**`) — see §5. This is the form the task-builder skill's own SKILL.md models (SKILL.md:2186-2198) and is the *de facto* current convention, in tension with the template's literal B3/B5 "single paragraph" rule. The builder for this track follows the skill's structured-bullet form (it is what /task executes against and what the validation checklist at SKILL.md:2239-2253 checks).

### 1d. A3/A4 — Granularity & Iterative Structure (lines 108-133)

- **A3 Complete Granular Breakdown (108-112):** break EVERY phase into atomic, verifiable items; an **individual checklist item for EVERY file, component, or iteration**; NO bulk operations; exact file paths + measurable outcomes. → For this track: **9 file operations (4 edits + 5 new ref files) = at minimum 9 distinct content items**, not one "update the docs" item.
- **A4 Iterative Process Structure (114-133):** for any multi-item process: (X.1) pre-enumerate ALL items in an initial step; (X.2) one checklist item per specific item; (X.3) consolidation step only after all items complete. Pattern quoted at lines 121-133.
- **E1/E2 (lines 295-315):** flat checkboxes only; NO nested checkboxes; NO parent checkbox summarizing children; use `**Step X.Y:**` headers for grouping; summary/parent checkboxes come AFTER their components (E2, line 312); checkboxes in completion order; never reference later checkboxes.

---

## 2. QA Gate Encoding Rules (THIS TRACK'S CORE)

**Critical for this track:** output is markdown protocol content > 500 lines AND it transforms a SOURCE spec (sc:troubleshoot-protocol source material) → protocol refs. So **BOTH** the M3 lens-based gate (size trigger) and the M4 source-fidelity gate (source-transformation trigger, I21) apply.

### 2a. M3 — Lens-Based QA Sequence (lines 1059-1096) — the MANDATORY pattern

8 steps, EACH an explicit `- [ ]` item (line 1096 — "MUST NOT collapse multiple steps into a single item"):
1. **Aggregation (L6)** — collect all preceding-phase outputs into an inventory file; use Glob for variable counts (line 1062).
2. **Structural lens agents (PARALLEL)** — `rf-qa`, one per structural lens, all `fix_authorization: false`; report path `${TASK_DIR}qa/qa-structural-[lens-name]-report.md` (lines 1064-1071).
3. **Content lens agents (PARALLEL)** — `rf-qa-qualitative`, one per content lens, all `fix_authorization: false`; report path `${TASK_DIR}qa/qa-content-[lens-name]-report.md` (lines 1072-1078). Steps 2+3 MAY share one parallel batch (line 1080).
4. **Domain-specific lens agents (PARALLEL, if any)** — same pattern (lines 1082).
5. **Findings consolidation** — read ALL reports → single `${TASK_DIR}qa/qa-consolidated-findings.md`, deduplicated, severity + originating lens (line 1084).
6. **Fix agent** — ONE `rf-qa` with `fix_authorization: true` + consolidated findings; applies ALL fixes; no other agent edits the doc (line 1086).
7. **Verification round (PARALLEL)** — min 2 agents (1 `rf-qa` + 1 `rf-qa-qualitative`), `fix_authorization: false`; outputs `qa-verification-structural-report.md` + `qa-verification-content-report.md` (line 1088).
8. **Conditional proceed (L5)** — PASS→proceed; FAIL→repeat Steps 5-7; max cycles per I16; HALT+escalate after max (line 1090).

Standard 8 lenses defined at I19 lines 715-726: structural = template-conformance, internal-consistency, evidence-quality, completeness; content = actionability, numbers-metrics, crossref-chain, domain-accuracy.

### 2b. M4 — Source-Document Fidelity Gate (lines 1098-1121) — runs AFTER M3

Verifies the output FAITHFULLY represents the source (external fidelity vs M3's internal quality). Steps (each an explicit `- [ ]` item, line 1121):
1. **Source identification** — explicitly name source docs (NOT discovered dynamically) (line 1104). → For this track: the troubleshoot-protocol source spec.
2. **Fidelity agents (PARALLEL)** — min 2 `rf-qa`; each reads assigned source section range + FULL output doc; report `${TASK_DIR}qa/qa-source-fidelity-report-[N].md`; `fix_authorization: false` (lines 1106-1111).
3. **Cross-source contradiction agent** — only if multiple source docs; reads ALL sources (not output) (line 1113). *This track has a single primary source spec → likely SKIP unless multiple source files feed the 5 refs.*
4. **Fidelity findings consolidation** → `${TASK_DIR}qa/qa-fidelity-consolidated-findings.md` (line 1115).
5. **Fidelity fix agent** — ONE `rf-qa`, `fix_authorization: true` (line 1117).
6. **Fidelity verification** — min 2 agents; same cycle control as M3 Step 8 (max 3 cycles → HALT) (line 1119).

M4 fidelity checks (I21 lines 777-783): semantic coverage, detail preservation, cross-source contradiction, phantom-coverage detection, operational/compliance completeness.
**Ordering rule (I21 line 788):** fidelity gate runs AFTER M3 — "The document must be structurally sound before checking fidelity."

### 2c. I19 — Minimum Agent Floors (lines 699-743) — EXACT QUOTES

**Final Document / Assembled Output QA table (lines 706-711), verbatim floors:**
| Output Size | rf-qa (structural) | rf-qa-qualitative (content) | Total Minimum |
|---|---|---|---|
| <500 lines | 3 | 3 | **6** |
| 500-1500 lines | 4 | 4 | **8** |
| 1500-3000 lines | 5 | 5 | **10** |
| >3000 lines | 6 | 6 | **12** |

→ **This track's primary output is >500 lines** (protocol content transforming a source spec; build request states output >500). At minimum **8 agents** (4 structural + 4 content) for the final/post-completion gate IF it lands in 500-1500; scale up per actual line count. These are FLOORS not targets (line 702), BEFORE domain-specific lenses (line 713).

**Adversarial framing N (line 729):** "Assume this document has at least N errors focused on your lens. Find them." — N = 5 (<500), 10 (500-1500), 15 (1500-3000), 20 (>3000). → N=10 for this track.

**Intermediate gate floors (lines 731-737), verbatim:** each intermediate gate (research / synthesis / task-integrity) = **5 agents**:
- Research gate: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative
- Synthesis gate: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative
- task-integrity: 2 rf-qa + 2 rf-qa-qualitative + 1 rf-analyst

Partitioning (lines 739-741): floors are per-lens-per-partition; >6 (full) / >10 (standard) research files trigger partitioning, increasing agent count.

### 2d. I20 — Serialized Fix Authorization (lines 745-757)

Any gate with 3+ agents on the same file → fix authorization MUST be serialized; parallel fix authorization PROHIBITED (line 746). Protocol: (1) all lens agents report `fix_authorization: false`; (2) consolidate → `${TASK_DIR}qa/qa-consolidated-findings.md`; (3) ONE fix agent `fix_authorization: true` applies ALL fixes; (4) verification round min 2 (1 rf-qa + 1 rf-qa-qualitative); (5) on new issues, repeat from consolidation, max cycles per I16. Every protocol step MUST be an explicit `- [ ]` item (line 757). "Why serialized" (line 755): parallel fixes cause churn/contradictions.

### 2e. I21 — Source-Fidelity Applicability (lines 759-788)

MANDATORY when outputs derive from source docs (list lines 762-771 includes "Any task where the orchestrator reads source documents to produce output"). NOT required for pure mechanical transforms (rename) or config-only tasks (lines 773-775). → **This track READS a source spec to produce protocol content → fidelity gate MANDATORY.** Agent count (line 784): min 2; if sources >1000 lines total, partition across 3-4 agents.

### 2f. I22 — QA Intensity (lines 793-834)

Three levels scale agent counts. Default mapping (lines 806-809): Quick/Lightweight→lite, Standard→standard, Deep/Heavyweight→**full**. **This is a Deep-tier build → qa_intensity = full** → I19 tables apply IN FULL (the I19 floors quoted in §2c are the operative numbers; lite/standard reduce them per the I22 table lines 800-804). At full: final gate per I19 tables + all domain lenses; fidelity per I21 (2-8 agents); fix cycles per I16 (2-3/gate); 2 verification agents (line 804).

### 2g. I15/I16 — Phase-Gate Enforcement + Verdicts (lines 635-673)

- **I15 (635-651):** every task with 2+ phases MUST have ≥1 phase-gate between the primary execution phase and any dependent phase. **PROHIBITION (line 638):** gates with only 1-2 agents are PROHIBITED; final/assembled-output floor = 6 agents, intermediate floor = 5 agents. Every QA step (each lens spawn, consolidation, fix, each verification) = individual `- [ ]` item; "No QA is implicit. No QA lives only in prose." (line 651).
- **I16 (653-673):** binary PASS/FAIL — ANY issue of ANY severity (CRITICAL/IMPORTANT/MINOR) = FAIL (line 654). Fix-cycle max table (lines 660-667): source-fidelity = 3 cycles → HALT+escalate; most gates 3; synthesis-gate + task-integrity = 2.

---

## 3. Anti-Orphaning + Task-Completion Item Placement

### Template view (I13/I17, lines 616-622, 675-686)
Template's PART 2 keeps a literal `## Post-Completion Actions` section (lines 1423-1441) containing, in order:
1. Glob-verify all output files exist (line 1425)
2. Run tests IF code was modified (line 1427)
3. **POST-COMPLETION LENS-BASED QA placeholder** — orchestrator MUST expand into per-agent M3 items, min 6 agents scaled by I19 (line 1435)
4. **POST-COMPLETION SOURCE FIDELITY GATE placeholder** — MANDATORY if task consumed source docs per I21; expand into M4 items (line 1437)
5. Write `### Task Summary` (line 1439)
6. Update `completion_date`/`updated_date` + status `🟢 Done` + Execution Log entry (line 1441) — **the final item**.

### Task-builder OVERRIDE — anti-orphaning (SKILL.md, AUTHORITATIVE for this build)
The task-builder skill **overrides the template's separate Post-Completion section**:
- **SKILL.md:2302 (rule 15):** *"Task completion items (update status to Done, write task summary) MUST be inside the final phase of the generated task file, never in a separate Post-Completion section. If the final phase includes downstream skill offers..., those items MUST come AFTER all task-completion actions, MUST be marked `NON-BLOCKING`, and MUST NOT gate task completion. Only major critical issues halt task execution."*
- Validation checklist enforces it: **SKILL.md:2239** `- [ ] Task completion items inside final phase (anti-orphaning)`.
- **C4 (template line 242-247):** task-completion = update frontmatter (status, completion_date) + log to Execution Log; do NOT create a "Task Completion and Handoff Protocol" section.

**Net for this build:** put the M3 post-completion lens QA, the M4 fidelity gate, the Task Summary, and the Update-status-to-Done item all **inside the final phase** (e.g. `## Phase N: Final — Validation & Completion`), in execution order, with Update-status-to-Done LAST.

---

## 4. POST Reflect Gate Item (penultimate, SELF-RUN subagent — NOT human-handoff)

The POST-reflect item is NOT in the template; it is emitted by the task-builder skill when the BUILD_REQUEST sets `POST_REFLECT_GATE: ENABLED`.

**Placement rule (SKILL.md:2253, 2312):** the POST reflect item is the **penultimate item of the final phase — immediately before the `Update task status to Done` item** (preserving anti-orphaning). It MUST be the **SELF-RUN form** (spawns a reflect subagent + records the verdict), **NOT a human-handoff / HALT**. A task file that omits it (when ENABLED) or emits a human-handoff/HALT form is **MALFORMED** (SKILL.md:2312).

**Canonical item form — quoted verbatim from SKILL.md:2193-2198:**

```markdown
- [ ] **N.{X-1} -- Independent post-execution reflection gate (run via subagent)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per project memory `feedback_sc_reflect_vs_inline_rfqa`, an independent `/sc:reflect --mode post` ensemble catches spec-literal-token, invariant-arithmetic, and integration/orphan blindspots that same-frame QA misses.
  - **Action**: Spawn a subagent that runs `/sc:reflect --mode post --remediate --diff <BASE> --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}` -- where `<BASE>` is `git merge-base HEAD <integration-branch>` (resolve `<integration-branch>` via `git symbolic-ref --short refs/remotes/origin/HEAD`, fallback origin/master|origin/main). Pass `<BASE>` as a SINGLE ref (NOT `<BASE>..HEAD`) so reflect diffs the working tree. Run `git add -A` BEFORE this gate so new untracked files are captured. Do NOT use `start_commit..HEAD`. `{DEPTH}` floored at `standard` (NEVER `quick`); `{EXECUTOR_CLASS}` excludes this executor from reflect's panel. Subagent supplies executor-disjoint context — NO human session needed. Uses `/sc:reflect`, never `/sc:task`; re-execution uses `/task`.
  - **Output**: Record reflect's `{verdict, run_id, report}` to frontmatter `reflect_post`. If reflect surfaces deviations, apply remediations or append to `### Open Questions` (never delete existing items).
  - **Verification**: `reflect_post` holds `{verdict, run_id, report}` (not empty); flagged deviations remediated or logged.
  - **Completion gate**: The reflect subagent has returned and its verdict is recorded in `reflect_post`. THEN the Update-status-to-Done item proceeds.
```

**For this DOCUMENTATION-TRANSFORMATION track:** `[--spec {SPEC_PATH}]` becomes ACTIVE (the source spec is the driving spec); `{DEPTH}` floored at `standard`; the spec arg lets reflect's POST deviation audit check executed protocol content vs the original source spec — complementary to the M4 fidelity gate. PRE counterpart: task-builder spawns `/sc:reflect --mode pre --spec <path>` at A.10.7 (SKILL.md:1724 — "POST emitted as final-phase item N.{X-1}").

---

## 5. Effective Patterns from Recent TASK-RF Examples

### Example A — `TASK-RF-prd-local-file-20260609-005242` (398 lines; rf-qa + fidelity + post-reflect)
A code-from-spec build that DOES include a source-fidelity domain lens — the closest structural analog to this track's source→protocol transformation.

- **Item form (de-facto current convention):** structured multi-line bullets, NOT the template's literal single-paragraph form. Each item = `- [x] <action sentence with embedded Verification (UV ONLY): ... clause and an "If unable to complete ... log ... then mark this item complete. Once done, mark this item as complete." tail>`. (e.g. Step 4.1a `:236`). The B2 6-element content is all present, embedded inline.
- **FINAL_ONLY lite QA gate as one phase (`### Phase 6`, `:282`):** header comment states the intensity + agent math explicitly: *"QA_INTENSITY = lite, FINAL_ONLY. Per template I22 lite-intensity final-gate floor: 1 structural rf-qa + 1 content rf-qa-qualitative + 1 domain lens agent (3 agents)... then ONE consolidation, then ONE serialized fix agent with `fix_authorization: true`, then ONE verification agent — per I20... (1 fix cycle max at lite)."* (`:284`).
- **Per-step M3/M4 encoding — each step its own `- [ ]` item:**
  - 6.1 Aggregate phase outputs → `final-consolidation.md` (`:288`)
  - 6.2 structural rf-qa lens, `fix_authorization: false`, byte-exact adversarial framing string (`:292`)
  - 6.3 content rf-qa-qualitative lens, report-only (`:296`)
  - 6.4 **domain SOURCE-FIDELITY lens** (`rf-qa`, combined semantic-coverage + phantom-detection), reads BOTH spec sections AND edited files (`:300`) — this is the M4 fidelity lens folded into the gate at lite intensity
  - 6.5 consolidate 3 lens reports → `qa-consolidated-findings.md`, any-fail=FAIL (I16) (`:304`)
  - 6.6 serialized fix agent (ONE `rf-qa` `fix_authorization: true`), conditional, 1 cycle max (`:308`)
  - 6.7 verification round, single agent at lite, distinct adversarial framing (`:312`)
- **Adversarial framing string (verbatim, reused per lens):** `ADVERSARIAL STANCE: Assume this work contains at least 5 errors focused on your lens. Find them, do not confirm everything is fine. A verdict of 0 issues requires evidence you thoroughly checked.`
- **Report paths pattern:** `phase-outputs/reviews/{final-qa-structural, final-qa-qualitative, final-qa-fidelity, qa-consolidated-findings, qa-fix-applied, qa-verification}.md`.
- **Anti-orphaning:** completion items live in `## Post-Completion Actions` with Done-flip LAST and the POST-reflect item penultimate (`:328` Done-flip notes "this is the LAST item completed... preserving anti-orphaning").
- **⚠️ STALE POST-REFLECT FORM:** this example uses the OLD `INDEPENDENT POST-EXECUTION REFLECTION GATE (FRESH SESSION, HALT)` human-handoff form (`:326`) that writes `reflect_post: PENDING` and STOPS for the operator. **This is now MALFORMED** per the current skill (SKILL.md:2253, 2312), which requires the SELF-RUN subagent form (§4 above). Also uses `<START_COMMIT>..HEAD` as the diff base — explicitly DEPRECATED by SKILL.md:2195 (use single `<BASE>` = `git merge-base`, working-tree diff).

### Example B — `TASK-RF-20260608-150011` (475 lines; code-modifying, FINAL_ONLY structural gate)
- **Per-phase structure:** one fix or test per phase (Phase 2 Fix1, Phase 3 Test A, Phase 4 Fix2, Phase 5 Test B), `### Phase 6: Validation — Lint, Format, Full Sprint Test Suite`, `### Phase 7: Final QA Gate`, `### Phase 8: Post-Completion Actions`.
- **Item form:** named bullet headers `- [x] **7.1 — Final structural QA gate (rf-qa, task-integrity)**` with explicit sub-bullets `**Context** / **Action** / **Output** / **Verification** / **Completion gate**` (`:297-302`). This is the exact form the task-builder SKILL.md models at 2186-2198 — **the recommended item form for this track.**
- **Phase 8 header states the rule (`:308`):** *"Completion items live INSIDE this final phase (anti-orphaning). Order: output/test verification → task summary → POST reflect gate (penultimate, HALT) → Update status to Done (last)."* — confirms penultimate POST-reflect, last Done-flip.
- **⚠️ Same STALE form:** Step 8.3 (`:330`) is `(fresh session, HALT)` human-handoff with `reflect_post: PENDING` + STOP. Header even cites `POST_REFLECT_GATE is ENABLED... DEPTH: standard; SPEC_PATH: NONE`. Again, the CURRENT skill requires SELF-RUN. **Builder MUST use §4's self-run form, NOT copy these examples' HALT form.**
- **Validation items (good model for this track's make-based validation):** Phase 6 encodes lint/format/test as discrete items — `uv run pytest tests/sprint/ -v` captured to a results file (`:269`), a verdict-comparison item (`:277`), and `make lint`/`make format` as a separate item (`:287`), each with its own completion gate.

### Cross-example takeaways for the builder
1. Use the **`**Context**/**Action**/**Output**/**Verification**/**Completion gate**` structured-bullet item form** (Example B / SKILL.md:2186-2198).
2. Encode the QA gate as **one phase** with **one `- [ ]` per M3/M4 step** (aggregate → each lens → consolidate → fix → verify → conditional-proceed); state intensity + agent math in the phase header comment.
3. Embed the **byte-exact adversarial framing string** in each lens item, with N scaled to size (N=10 for 500-1500 lines here).
4. Put a **dedicated source-fidelity lens** in the gate (this is a source→protocol transformation → M4/I21 mandatory).
5. **POST-reflect = SELF-RUN subagent form (§4), penultimate; Done-flip last.** Do NOT replicate the examples' deprecated `(FRESH SESSION, HALT)` / `reflect_post: PENDING`+STOP form, and do NOT use `start_commit..HEAD` as the diff base.

---

## 6. Validation Item Encoding (markdown task, not code)

This track edits 4 `.md` files + creates 5 `.md` ref files — it modifies **documentation under `src/superclaude/` synced surfaces (skills/refs/templates)**, not Python source.

- **TESTING_REQUIREMENTS (I18, lines 688-697):** I18 applies only to tasks that "create or modify SOURCE CODE files (not documentation, not configuration)" (line 689). → **No `uv run pytest` code-test item is required by I18** for this markdown-only build. (The Post-Completion template item at line 1427 is conditional: *"If this task modified source code files, run the relevant test suite..."* — N/A here, note "no source code modified".)
- **VALIDATION = sync + drift + lint, encoded as discrete `- [ ]` items** (each B2 self-contained, per Example B's Phase 6 model):
  1. `make sync-dev` — REQUIRED here because the edits touch `src/superclaude/skills/**` and `refs/` (the SoT), which MUST be propagated to `.claude/`. Item: run `make sync-dev 2>&1`, capture to a results file. (Contrast Example A `:274` where it was a no-op drift guard because cli/ is never synced — here it is a real propagation step.)
  2. `make verify-sync` — confirm `src/` and `.claude/` match (PASS iff clean exit), capture verdict.
  3. **markdownlint** — run the repo's markdown lint over the 9 changed/created `.md` files (matches memory `reference_markdownlint_md025_frontmatter_title` + the pre-commit markdownlint hook); capture PASS/FAIL. NB: project memory flags MD025 (frontmatter `title:` + body `# H1`) and the no-multiline-paste constraint — encode lint as a single-line command the executor runs.
  4. Git-scope confirmation item (Example A `:278` model): confirm changes confined to `src/superclaude/{skills,...}/**` + `.claude/` mirror is NOT staged (0 tracked `.claude/` non-settings changes per project CLAUDE.md ABSOLUTE RULE), + `.dev/`.
- **Encoding rule:** each validation step is its own `- [ ]` item with an "ensuring..." / Verification clause + a captured artifact path, never a bulk "validate everything" item (A3/E1). Validation items live in a Validation phase BEFORE the Final QA gate phase; the make/lint/git items feed the gate's aggregation step (M3 Step 1).

---

## Status: Complete

**Summary:** Documented Template-02 PART 1 rules (frontmatter, D3 section ordering, B2 5+1 self-contained pattern, A3/A4 granularity, E1/E2 flat-checkbox) and the full QA-gate encoding stack with exact citations: M3 8-step lens sequence, M4 6-step source-fidelity gate (runs AFTER M3 per I21:788), I19 agent-count FLOORS quoted verbatim (final: <500=6, 500-1500=8, 1500-3000=10, >3000=12; intermediate=5), I20 serialized fix, I21 fidelity applicability (MANDATORY for this source→protocol transform), I22 intensity (Deep→full). For this track: output >500 lines → ≥8 final-gate agents; BOTH M3 and M4 apply. Anti-orphaning (SKILL.md:2302) puts completion items inside the final phase, Done-flip last. The canonical POST-reflect item is the **SELF-RUN subagent form** (SKILL.md:2193-2198), penultimate — NOT the human-handoff/HALT form the two examined examples still use (those are now MALFORMED per SKILL.md:2253/2312). I18 testing is N/A (markdown, not code); VALIDATION = discrete `make sync-dev` + `make verify-sync` + markdownlint + git-scope items.

**Deliverable file:** `.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260610-144537/research/04-mdtm-template-and-examples.md`
