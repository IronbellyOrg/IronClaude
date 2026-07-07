# Research 05 — Template & Examples (MDTM Template 02 + prior TASK-RF example)

**Status: Complete**

Topic: give the builder the exact MDTM Template 02 structure + a proven prior CLI-change example so the generated `TASK-RF-t2-fallback-ladder` tasklist conforms.

All paths relative to repo root `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback`.

Primary sources:
- Template: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (dev copy: `.claude/templates/workflow/02_mdtm_template_complex_task.md`). PART 1 = builder instructions (lines 63–1131), PART 2 = the actual task template (line 1139+).
- Builder skill: `src/superclaude/skills/task-builder/SKILL.md`.
- Proven example (CLI change, cli-mode POST gate): `.dev/tasks/done/TASK-RF-per-phase-turn-budget-20260618-160752/TASK-RF-per-phase-turn-budget-20260618-160752.md`.

---

## 1. Template 02 PART 1 — required structure (section anchors)

The template file is a single file with TWO parts. PART 1 (`## PART 1: TASK BUILDING INSTRUCTIONS`, line 68) is instructions ONLY — none of it appears in the output task file. PART 2 (`## PART 2: TASK FILE TEMPLATE`, line 1143) is what gets copied and placeholder-filled. Template 02 "Extends Template 01 with Section L: Intra-Task Handoff Patterns" (line 78) — use it "when tasks require discovery, testing, review, conditional logic, or aggregation between checklist items" (lines 79–81). A T2-fallback-ladder CLI change with tests + QA gate qualifies.

### Required output-file sections (from PART 2 structure + Section D)
Section D3 (lines 286–290) "CRITICAL RULE — NO CHECKLIST ITEMS may appear before Phase 1 begins":
`Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable)`. All context-review / previous-stage-input checklist items live IN Phase 1 (Steps 1.2–1.4), never before it.

Mandatory sections a generated task MUST contain:
- Frontmatter (schema in §2 below).
- `## Task Overview` / `## Key Objectives` (informational).
- `## Prerequisites & Dependencies` (informational; `### Previous Stage Outputs (MANDATORY INPUTS)`).
- `## Execution Context` (References, Source Areas, Key Constraints, `### Handoff File Convention`, `### Frontmatter Update Protocol`).
- `## Detailed Task Instructions` → `### Phase N:` executable phases with `**Step N.M:**` bold headers (NOT checkboxes) grouping `- [ ]` items.
- `## Post-Completion Actions` (I13, I17): post-completion validation items → **POST reflect gate item (penultimate)** → **Update status to Done (final)**.
- `## Task Log / Notes` with `### Phase N Findings` subsections (blocker sink) + `### Task Summary` + `### Execution Log`.

### B2 self-contained item pattern (Section B, lines 148–213) — THE core rule
Every checklist item MUST be a COMPLETE, SELF-CONTAINED prompt (one full paragraph, verbose — B3 line 167) executable with zero prior context, because Rigorflow batches across session rollovers (B1, lines 151–157). The 6 required elements (B2, lines 159–166):
1. **Context Reference with WHY** — which file(s) to read and why.
2. **Action with WHY** — what to do and why.
3. **Output Specification** — exact output file path/name + content + template to follow.
4. **Integrated Verification** — an "ensuring…" clause (DO NOT assume/hallucinate; 100% source-derived; document negative evidence). Verification is NEVER a separate item (C3 lines 236–240, I12 lines 609–614).
5. **Evidence on Failure Only** — log to `### Phase N Findings` ONLY on blocker; success is evidenced by the output file itself.
6. **Explicit Completion Gate** — literal closing: "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

Canonical correct example: B4 lines 172–175. FORBIDDEN patterns (B5, lines 181–201): standalone "read context" items with no output; missing context reference; multi-line/bulleted items; separate verification/confirmation items; over-granular ("create directory" alone); REMINDER blocks between items.

Embedded, never separate sections (Section C, lines 216–247): Outputs & Deliverables (C1), Success Criteria (C2 → "ensuring…" clause), Verification (C3), Task Completion (C4 → only frontmatter update + summary in Post-Completion).

### Rule A3 — Complete Granular Breakdown (lines 108–112)
Break EVERY phase into atomic, verifiable checklist items; individual item for EVERY file/component/iteration; NO high-level/bulk items; include exact file paths, specific requirements, measurable outcomes.

### Rule A4 — Iterative Process Structure (lines 114–133)
For any multi-item process: pre-enumerate ALL items in an initial step, one checklist item per specific item, incremental updates after each, consolidation step only after all complete. Pattern (lines 121–133): `Step X.1` scan/enumerate → `Step X.2` process each item individually → `Step X.3` consolidate.

### Checklist structure rules (Section E, lines 292–405)
Flat checkboxes only — NO nested/parent checkboxes (E1 lines 295–309). Summary/parent checkboxes come AFTER their components, never before (E2 lines 311–366). Sequential top-to-bottom, never require marking items above current position, never reference later checkboxes (E3 lines 367–383). Use `**Step X.Y:**` bold headers (not checkboxes) for grouping; checkboxes only on actionable items; no REMINDER blocks between items (E4 lines 384–405).

### Execution discipline (Section F, lines 408–468)
F1 five-step loop `READ → IDENTIFY → EXECUTE → UPDATE → REPEAT` (lines 411–420). F2 prohibits multi-item execution, phase-boundary delegation, skipping phase-gate QA, skipping post-completion validation (lines 422–429). F2a defines the one-item-at-a-time discipline + the **parallel spawning exception** (lines 431–447): consecutive same-phase items that spawn INDEPENDENT subagents MAY be spawned in one message via multiple Agent calls; still mark each individually.

### L1–L6 intra-task handoff patterns (Section L, lines 902–1026)
Handoff files persist on disk at `.dev/tasks/TASK-NAME/phase-outputs/` across all batches (convention lines 909–921): `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`. The patterns:
- **L1 Discovery** (928–938) — explore + write structured findings file; the discovery file IS the deliverable, later items read it.
- **L2 Build-from-Discovery** (940–950) — read discovery file AND source; discovery says WHAT, source provides CONTENT.
- **L3 Test/Execute** (952–962) — run a command; capture BOTH raw output AND a structured summary. **This is the required pattern for testing items (I18 line 695).**
- **L4 Review/QA** (964–974) — assess an output vs source; produce a structured PASS/FAIL verdict, never "looks good".
- **L5 Conditional-Action** (976–988) — branch on a prior result file; MUST handle BOTH success and failure branches; output file always created.
- **L6 Aggregation** (990–1000) — Glob-discover + consolidate multiple outputs (used as QA-gate step 1 and phase aggregation).
- **L7 Pattern Selection Guide** (1002–1026) — common structures: `Build → Test → Fix` = K1/K2 build → L3 test → L5 conditional; `Full Lifecycle with QA Gates` = L1→L2→**M3(QA)**→L3→L5→L4→L6→**M3(QA)**.

For a T2-fallback CLI change the natural shape is: Phase 2 source edits (K1/K2 per-file items) → Phase (tests, L3) → Phase (validation, L3+L5) → Phase (M3 lens QA gate) → Post-Completion (validation + POST reflect + Done).

---

## 2. Frontmatter schema for the generated task file

Base frontmatter block: template PART 1 lines 1–61 (the frontmatter is also part of the template, note line 1150). Builder-emitted schema: `task-builder/SKILL.md` lines 2165–2170. Key fields the builder writes:

```yaml
id: "TASK-RF-t2-fallback-ladder-YYYYMMDD-HHMMSS"     # matches dir name
title: "[Action-oriented title]"
status: "🟡 To Do"      # → "🟠 Doing" on start, "🟢 Done" on completion (F5, lines 464-468)
type: "🐛 BugFix" | "🔧 Refactor" | "✨ Feature" | ...   # line 8 enum
priority: "🔼 High" | "🔥 Highest" | ...                  # line 10 enum
created_date / updated_date: "YYYY-MM-DD"
spec_path: "<driving spec/PRD/TDD>"                       # A.2 priority order
reflect_pre:                                             # PRE gate sign-off, populated at A.10.7
  verdict: ""      # pass | fail | skipped
  coverage_pct: null
  depth: ""        # MUST equal TCS-derived depth
  tcs: 0           # real integer, never placeholder
  run_id: ""
  report: ""
  reviewed_at: ""
reflect_post: ""    # ROOM COMMENT ONLY — wrapper writes it back; NEVER hand-author or lock
related_docs:
- path: "..."
  description: "..."
tags: [ ... ]
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"   # line 2165
estimation: ""
task_type: static     # line 2167 (static unless dynamic-content markers needed, I6)
reflect_post_mode: cli | skill    # line 2168 — ALWAYS emitted every build
start_commit: "<sha>"             # line 2169 — CLI MODE ONLY (omitted in skill mode)
executor_model_class: "sonnet"    # line 2170 — CLI MODE ONLY (omitted in skill mode)
```

### start_commit & executor_model_class are the O1/CLI-mode wrapper gate keys
These two keys are REQUIRED **when `reflect_post_mode: cli`** and MUST BE ABSENT when `reflect_post_mode: skill` (SKILL.md line 2312 Mode key-presence check; POST-Gate Mode Bifurcation Table lines 2377–2397). A hybrid (one present, one absent, or present in skill mode) is MALFORMED.

- **`start_commit`** (SKILL.md lines 2169, 2242, 2276) — capture at build time as `git merge-base HEAD <integration-branch>` (resolve `<integration-branch>` from `git symbolic-ref --short refs/remotes/origin/HEAD`, falling back to `origin/master`/`origin/main`). It is the wrapper's audit base when `--base` is omitted, diffed as a SINGLE ref against the working tree (so uncommitted task edits ARE audited). Base precedence: `--base` > frontmatter `start_commit` > `git merge-base HEAD master` (contract §6). Example comment (from per-phase-turn-budget task): `# git merge-base HEAD origin/master captured at build time — the O1 wrapper's audit base when --base is omitted`.
- **`executor_model_class`** (SKILL.md lines 2170, 2246–2247, 2276) — the model-class alias the build expects to execute under (e.g. `sonnet`), captured at build time as PROVENANCE (from the building session's model, NOT a runtime probe). Forwarded to reflect as `--executor-model`; OUR sc-reflect EXCLUDES that class from the reviewer pool (executor-class exclusion — NOT accepted-and-ignored, NOT kept in pool). Comment MUST use class-exclusion / forwarded-to-`--executor-model` language, never "kept in pool" compat wording (line 2247).

### reflect_post is a ROOM COMMENT (never hand-authored)
`reflect_post:` is left blank/as a comment; the wrapper writes it back at execution time (SKILL.md line 2276; template line 32). Example comment (per-phase-turn-budget line 30): `# reflect_post: written back by the superclaude reflect run wrapper at execution time — leave room, do NOT hand-author or lock.`

Since this project's task-builder default is CLI mode for mission-critical builds (only the `--cli` wrapper POST path is session-validated end-to-end; SKILL.md line 43 disclosure, memory `reference_subagent_cannot_nest_skill_fanout`), the generated tasklist should be `reflect_post_mode: cli` and carry BOTH `start_commit` AND `executor_model_class`.

---

## 3. The POST reflect gate item shape (CLI / wrapper mode)

Authoritative encoding: task-builder/SKILL.md line 2237 (the item's Action), Critical Rule 20 CLI arm (line 2371), validation-checklist line 2311, Bifurcation Table lines 2385–2397. O4 (CLI mode) fixes POST depth at `deep`.

**Placement:** the PENULTIMATE item of the final phase — immediately before the `Update task status to Done` item (preserves anti-orphaning).

**Form:** a FLAT wrapper shell-out (never a subagent, no nesting/agent-spawn tokens — NFR-7-clean). First `git add -A` so new task artifacts are in the working-tree diff (the wrapper's audit omits never-`git add`-ed files). Then a single Bash command: the skip guard, then the reflect run.

**Exact recursion-breaker skip guard (quote, SKILL.md line 2237):**
```bash
if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi
```

**Exact command (quote, SKILL.md line 2237):**
```bash
superclaude reflect run {TASK_FILE} --depth deep --fix --promote
```
`{TASK_FILE}` = the absolute tasklist path (the wrapper absolutizes its positional). Emit NO `--base`, NO `--reflect`, NO `--max-turns`, NO `<base>..HEAD` range, NO agent-spawn directive. `--depth deep` fixed (forces Tier-2 fan-out); `--fix` runs the bounded audit→apply→re-verify loop; `--promote` lets the `task` adapter move the tasklist dir to `done/` on a clean/auto-fixed PASS.

**Exit-code consumption (only 0 proceeds):** exit `0` (clean OR auto-fixed-and-verified) → gate PASSED, proceed to Update-status-to-Done. Exit `10` (halted: human-required deviations / non-convergent fix loop), `11` (degraded: audit untrustworthy), `2` (blocked: child crash / missing-or-bad contract) ALL FAIL → surface the wrapper report and HALT before Done. The gate MUST NOT hand-author `reflect_post` (the wrapper writes it) and MUST NOT halt-for-human / defer to a separate session. Re-execution uses `/task`, never `/sc:task`.

Note (project convention, memory `reference_reflect_exit11_degraded_benign`): a documented benign exit-11 "degraded (single-reviewer-fallback / single-vendor)" may be judged by the `return-contract.yaml` `status`/`regression`, not the exit code — relevant here because a T2-fallback-ladder change is likely a single-model-vendor harness where ensemble/calibrator-diversity degrade is environmental, not a content failure.

---

## 4. Proven prior completed example (CLI change, cli-mode)

### Primary: `.dev/tasks/done/TASK-RF-per-phase-turn-budget-20260618-160752/TASK-RF-per-phase-turn-budget-20260618-160752.md`
A `🐛 BugFix` (`🔥 Highest`) touching `src/superclaude/cli/sprint/executor.py` + `models.py` with a test matrix — the closest analog to a T2-fallback CLI change. `reflect_post_mode: cli`, `start_commit` + `executor_model_class: "sonnet"` present with the O1 comment strings quoted in §2. `template_schema_doc: ""` (they left it blank; the builder default per SKILL.md line 2165 fills it — prefer filling it).

Phase structure (headers grep):
- **Phase 1: Preparation, Grounding, and Live-Anchor Re-Verification** — Step 1.1 status→Doing (I11 early-status), 1.2 create handoff dirs, 1.3 confirm branch, 1.4 re-verify every live anchor vs current worktree (anti-drift gate). Discovery/L1 shape.
- **Phase 2: Source Edits** — one `**Step 2.N:**` per atomic edit (R-1…R-10), each a B2 self-contained item citing exact file:line anchors. A3 granular breakdown in action.
- **Phase 3: Model docstring + pre-merge consumer grep** (K-3).
- **Phase 4: Tests (TM-0…TM-14)** — one `**Step 4.N:**` per test-matrix item (A4 iterative structure), each item = one test function.
- **Phase 5: Validation** — 5.1 full UV-only test run (L3 Test/Execute), 5.2 conditional gate on full pass incl. regression test (L5 Conditional-Action), 5.3 lint touched files.
- **Phase 6: Final QA Gate** — see §5 (M3 lens-based, standard intensity, 7 report-only agents).
- **`## Post-Completion Actions`** — post-completion validation → **POST reflect gate (penultimate, cli wrapper form, line 320)** → Update status→Done (final).

Per-item granularity: every source edit and every test is its own `**Step**`/`- [ ]` pair with embedded file:line anchors and an "ensuring…" clause. Findings/blockers routed to `### Phase N Findings`. Each phase also has an inline per-phase QA note in the Execution Log (`Phase 2 PHASE-GATE QA (rf-qa, adversarial…): PASS`).

Final-phase reflect item ran real: exit 11 DEGRADED (single-model-vendor environmental) → per the item's fail-closed contract, execution HALTED, status set `⚪ Blocked`, options in `### Open Questions` (Execution Log lines 418, 441 confirm the exact command `superclaude reflect run <taskfile> --depth deep --fix --promote`, recursion-breaker-guarded, after `git add -A`).

### Secondary: `.dev/tasks/done/TASK-RF-ensemble-adversarial-seam-20260621-135420/TASK-RF-ensemble-adversarial-seam-20260621-135420.md`
Also `reflect_post_mode: cli`, `start_commit` + `executor_model_class: sonnet`, `## Post-Completion Actions` with the penultimate POST reflect gate (line 326) in the same flat-wrapper form. Confirms the pattern across a second reflect-domain task. Execution Log line 423 documents the wrapper ran (env var UNSET → wrapper ran), artifacts at `<task-dir>/reflect/post/<run_id>/`.

---

## 5. QA gate encoding requirements (I15–I22, M3)

**PER_PHASE gates required** (I15 lines 635–652, F2 line 428): every task with 2+ phases MUST have ≥1 phase-gate QA checkpoint between the primary execution phase and any dependent later phase, following the **M3 Lens-Based QA Sequence** (lines 1059–1096). Every QA step is an explicit `- [ ]` item — "No QA is implicit. No QA lives only in prose" (line 651).

**Minimum agent counts** (I19 lines 699–743, scaled by I22 qa_intensity lines 793–840). For a CODE+TESTS change (not a >500-line document), the example ran **standard intensity** (I22 line 803): FINAL gate = **7 agents** = 3 rf-qa structural (template-conformance/spec-coverage, internal-consistency/anchor-fidelity, evidence-quality/no-overreach) + 3 rf-qa-qualitative content (test-actionability, numbers/KPI, crossref-chain) + 1 domain lens. Intermediate gates at standard = 3 agents (1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative). Lite = 3 final / 2 intermediate; full = per I19 tables (6–12+ final). Gates below the floor are REJECTED at validation (line 638).

**Serialized fix authorization** (I20 lines 745–757, M3 Steps 5–8): the fix protocol MUST be report-only-lens-agents-then-single-fix-agent:
1. Report phase — ALL lens agents spawned in PARALLEL with `fix_authorization: false` (report only).
2. Consolidation — read all reports → one `${TASK_DIR}qa/qa-consolidated-findings.md`, deduplicated, originating lens noted, verdict FAIL if ANY issue of ANY severity.
3. Fix phase — spawn EXACTLY ONE rf-qa agent with `fix_authorization: true` + the consolidated file; only it edits the document.
4. Verification round — ≥2 agents (1 rf-qa + 1 rf-qa-qualitative), `fix_authorization: false`.
5. Conditional proceed (L5) — both PASS → proceed; else repeat from consolidation. Max cycles per I16 (task-integrity gate = 2, most = 3, then HALT/escalate).

Parallel fix authorization (multiple agents editing the same file) is PROHIBITED (line 746).

**Adversarial framing** (I15 line 649, M3 lines 1068/1076, I19 line 729): every lens agent prompt MUST include "Assume this document has at least N errors focused on [lens]. Find them." (N scales: 5 for <500 lines, 10 for 500–1500, 15 for 1500–3000, 20 for >3000). Each lens agent gets ONE lens, its own report path `${TASK_DIR}qa/qa-structural-[lens]-report.md` / `qa-content-[lens]-report.md`, its own focused checklist — NOT a generic "check everything" prompt.

The example's Phase 6 (lines 280–309) is a copy-ready encoding of all of the above: Step 6.1 aggregate (L6), 6.2 three structural rf-qa (PARALLEL, `fix_authorization: false`, adversarial), 6.3 three content rf-qa-qualitative (PARALLEL, adversarial), 6.4 one domain rf-qa, 6.5 consolidate (I20 step 2), 6.6 ONE fix agent `fix_authorization: true` (I20 step 3), 6.7 2-agent verification round (I20 step 4), 6.8 conditional/cycle control (L5, max 2 cycles). Reuse this Phase-6 shape verbatim, swapping the lens prompts to the T2-fallback-ladder surface.

**M4 source-fidelity gate** (I21 lines 759–789, M4 lines 1098–1121) is NOT required for a pure code+tests change (only when output is DERIVED from source documents — PRD/TDD/docs). The example explicitly states "NO M4/I21 source-document fidelity gate applies" (line 282). A T2-fallback-ladder CLI change likely also skips M4 unless it also produces derived docs.

**I18 testing requirement** (lines 688–697): a code-modifying task MUST include ≥1 testing item using the L3 pattern (specify test command, pass criteria, results-capture path). At minimum unit tests covering modified code. UV-only per project rules (`uv run pytest …`).

---

## Builder handoff summary

- Use Template 02 PART 2; obey Section D3 (no checklist items before Phase 1), Section B2 (6-element self-contained paragraphs ending with the literal completion gate), A3 granular + A4 iterative structure, Section E flat-checkbox rules, Section L handoff patterns (`phase-outputs/` subdirs).
- Frontmatter: emit `reflect_post_mode: cli` + REQUIRED `start_commit` (git merge-base HEAD <integration-branch>) + `executor_model_class` (build-session model alias, class-exclusion comment); `reflect_post` left as a room comment; `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"`; `reflect_pre` sign-off block with real `tcs`; `spec_path` per A.2; `task_type: static`.
- POST reflect gate = penultimate final-phase item, FLAT wrapper: guard `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi` then `superclaude reflect run {ABS_TASK_FILE} --depth deep --fix --promote` after `git add -A`; consume exit (only 0 proceeds; 10/11/2 HALT); no `--base`/`--reflect`/range/agent tokens; never hand-author `reflect_post`.
- QA: PER_PHASE M3 lens gate(s), standard intensity for a code+tests change (7 final-gate agents: 3 rf-qa + 3 rf-qa-qualitative + 1 domain), report-only lens agents → single fix agent (I20 serialized) → 2-agent verification, adversarial "Assume ≥N errors" framing per lens, each lens its own report file. Include an L3 UV-only test item (I18). No M4 fidelity gate for pure code+tests.
- Copy the Phase 6 encoding of `TASK-RF-per-phase-turn-budget-20260618-160752` verbatim as the skeleton; copy its cli-mode POST reflect item (line 320) and frontmatter (lines 1–60) as the reference; secondary reference `TASK-RF-ensemble-adversarial-seam-20260621-135420`.

**Status: Complete**
