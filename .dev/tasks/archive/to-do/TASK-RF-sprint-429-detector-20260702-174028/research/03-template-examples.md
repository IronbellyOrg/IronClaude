# Research 03 — Template & Examples (MDTM template 02 rules + prior TASK-RF example)

**Status: Complete**

**Topic:** Exact template-02 authoring rules the builder must follow so the generated sprint-429-detector task file is well-structured, granular, and has a compliant QA gate + POST reflect wrapper item.

**Primary sources (all cited file:line below):**
- `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (template; PART 1 = builder instructions, PART 2 = clean task shell)
- `/config/workspace/IronClaude/.claude/skills/task-builder/SKILL.md` (canonical POST reflect wrapper form + TB-Add-7/8 gates)
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md` (recent shipped example, same builder, same POST-reflect + lens-QA machinery)

---

## 1. Required frontmatter + mandatory sections

### Frontmatter (template lines 1–61 + builder-added keys)
Template `---` block fields (template:1–61): `id`, `title`, `description`, `version`, `status` (default `"🟡 To Do"`; executor flips to `"🟠 Doing"`/`"🟢 Done"`), `type`, `priority`, `created_date`, `updated_date`, `assigned_to`, `autogen`/`autogen_method`, `coordinator`, `parent_doc`, `parent_task`, `depends_on`, `spec_path` (driving spec — populated by builder, template:23), `reflect_pre:` map (`verdict|coverage_pct|depth|tcs|run_id|report|reviewed_at`, template:24–31), `reflect_post: ""` (template:32 — **room comment, wrapper writes it back; never hand-author or lock**), `related_docs`, `tags`, `template_schema_doc` (template:47), `estimation`, `sprint`, `task_type: static` (template:60 — this task has fixed content, so `static`).

**Builder-added frontmatter keys** (NOT in the template `---` block; task-builder appends them per SKILL.md:2155–2168, confirmed present in the example at lines 69–70):
- `start_commit: "<sha>"` — `git merge-base HEAD <integration-branch>` captured at build time; this is the O1 wrapper's audit base when `--base` is omitted (SKILL.md:2155, 2168). Example: `start_commit: "156f28292b4ddba09cefb89e5f160cbd2475e875"` (example:69).
- `executor_model_class: "<alias>"` — e.g. `sonnet`; passed to reflect as `--executor-model` so the executor is excluded from the reviewer panel (SKILL.md:2156, 2168). Example:70.
- The example also carries `template: "02-complex-task"`, `tracks: 1`, `created`, and populated `reflect_pre` (example:12–30) — all optional/builder-populated.

### Mandatory body sections (template PART 2, lines 1157–1445)
In order: `# [Task Title]` (1157) → `## Task Overview` (1159) → `## Key Objectives` (1163) → `## Prerequisites & Dependencies` (1171, with `### Parent Task & Dependencies` 1173 and `### Previous Stage Outputs (MANDATORY INPUTS)` 1180) → **`## Execution Context`** (1193, see §5) → `## Detailed Task Instructions` (1233) → phases (`### Phase 1: Preparation and Setup` 1291, `### Phase 2: [Main]` 1339, `### Phase Gate: Quality Verification (M3 Lens-Based QA)` 1365, `### Phase [N]: Testing & Verification` 1404, `### Phase 3: [Review]` 1412) → `## Post-Completion Actions` (1423) → `## Task Log / Notes 📋` (1443, with `### Task Summary`, `### Execution Log`, per-phase `### Phase N - Findings`, `### Phase Gate Findings`, `### Follow-Up Items Identified`, `### Deviations from Process`).

---

## 2. Rule A3 (granular breakdown) + B2 (self-contained item) — one item per change

**A3. COMPLETE GRANULAR BREAKDOWN (template:108–112)** — quoted:
> - Break down EVERY workflow phase into atomic, verifiable checklist items
> - Create individual checklist items for EVERY file, component, or iteration
> - NO high-level or bulk operations allowed - everything must be granular
> - Include exact file paths, specific requirements, and measurable outcomes

Reinforced by **A4 (template:114–133)**: "Pre-enumerate ALL items to be processed in an initial step; create individual checklist item for each specific item." → **Direct application:** each of the 3 fixtures = its own `- [ ]` item; each of the 2 monitor.py hunks = its own item; the parametrized contract-table test = its own item; each of the 4 parity tests = its own item (or one enumerated Step listing all 4 as separate `- [ ]` lines). No "add all fixtures" bulk item.

**B2. EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT (template:159–166)** — the 6 mandatory elements, quoted:
> 1. **Context Reference with WHY** - What file(s) to read and why that context is needed for this specific action
> 2. **Action with WHY** - What to do with that context and why it needs to be done
> 3. **Output Specification** - The exact output file name, location, what content to produce, and template to follow (if applicable)
> 4. **Integrated Verification** - An "ensuring..." clause ... (DO NOT assume, hallucinate ... document negative evidence when verification fails)
> 5. **Evidence on Failure Only** - Log to task notes ONLY if unable to complete due to blockers ... (successful completion is evidenced by the output file itself)
> 6. **Explicit Completion Gate** - "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

**B3 (template:167–170):** each item is ONE FULL PARAGRAPH (not multiple lines/bullets), verbose, readable as a standalone prompt. **B5 forbidden patterns (template:181–200):** no standalone "read context" items with no output; no missing context reference; no multi-line/bulleted items; no separate verification/confirmation items (fold verification into the "ensuring…" clause per **I12**, template:609–614); no "create directory" alone.

**Rationale (B1, template:151–157):** session rollover — context loaded in an early batch is gone by a later batch, so every item embeds its own context. This is why each hunk/fixture/test must be self-sufficient.

> NOTE ON ITEM STYLE: The template's canonical form (B3/B4, template:172–175) and the shipped example (`TASK-RF-detection-contract`, e.g. example:340, 426, 430) both use the **single-paragraph** form ("Read X because …, then <action>, ensuring …. If unable … log the blocker … Once done, mark this item as complete."). The task-builder SKILL's tail template (SKILL.md:2196–2214) shows a **structured multi-field** form (`- **Context** / **Action** / **Output** / **Verification** / **Completion gate**`). Both encode the same 6 B2 elements. **Mirror the single-paragraph form the shipped example uses** — it is the observed on-disk convention for this builder/project and satisfies B3 directly.

---

## 3. QA gate encoding (M3, M4, I19/I22 floors) — exact item shapes

### M3 — Lens-Based QA Sequence (template:1059–1096), the MANDATORY gate pattern
M1 single-agent QA is DEPRECATED (template:1045, 1057). Every gate is M3 + serialized fix (I20). The 8 steps, each an explicit `- [ ]` item (template:1096 — "EVERY step … MUST be an explicit `- [ ]` checklist item; MUST NOT collapse multiple steps into a single item"):
1. **Aggregation** (L6) — collect preceding-phase outputs into an inventory file (Glob if variable count) (template:1062).
2. **Structural lens agents (rf-qa, PARALLEL, `fix_authorization: false`)** — one per structural lens (template:1064–1070).
3. **Content lens agents (rf-qa-qualitative, PARALLEL, `fix_authorization: false`)** — one per content lens (template:1072–1078). Steps 2+3 MAY spawn in one parallel batch (template:1080).
4. Domain-specific lens agents (if any) — same shape (template:1082).
5. **Findings consolidation** — read ALL reports → single `${TASK_DIR}qa/qa-consolidated-findings.md`, deduped, severity + originating lens (template:1084).
6. **Fix agent** — exactly ONE rf-qa with `fix_authorization: true`, applies ALL fixes (template:1086). No other agent edits the doc.
7. **Verification round (PARALLEL)** — min 2 agents (1 rf-qa + 1 rf-qa-qualitative), `fix_authorization: false`; verify findings addressed, no new issues, integrity intact (template:1088).
8. **Conditional proceed (L5)** — both PASS → proceed; either FAIL → repeat Steps 5–7; max cycles per I16; else HALT + escalate (template:1090).

### M4 — Source-Document Fidelity Gate (template:1098–1104, I21 template:759–789)
Runs AFTER M3. Reads BOTH source docs AND output; checks semantic coverage / detail preservation / phantom-coverage. **Likely N/A for the sprint-429-detector task** — this is a code+test change (monitor.py hunks + fixtures + tests), not a source-doc→doc derivation. I21's mandatory list (template:762–771) is PRD/TDD/roadmap/tech-reference/README/tech-research/cleanup; I21 explicitly excludes "Configuration-only tasks" and mechanical transforms (template:773–775). For "Code-modifying tasks" the M3 cross-walk (template:1052) says "Fidelity gate only if code was derived from spec documents." → **Include M4 only if the builder judges the code was mechanically derived from the merged-requirements spec; otherwise omit and note the omission.** (When in doubt, template:1055 leans include-a-gate — but M4 specifically keys off source-doc derivation.)

### I19 / I22 — minimum agent floors for a FINAL_ONLY final-document gate
**I19 Final Document floor (template:704–711):** `<500 lines` → **3 rf-qa (structural) + 3 rf-qa-qualitative (content) = 6 total**. This is the FINAL_ONLY floor cited in the topic. Standard structural lenses (template:715–719): template-conformance, internal-consistency, evidence-quality, completeness. Standard content lenses (template:721–725): actionability, numbers-and-metrics, crossref-chain-integrity, domain-accuracy.
**I15 PROHIBITION (template:638):** "QA gates using only 1-2 agents are PROHIBITED. For FINAL DOCUMENT / ASSEMBLED OUTPUT ... absolute minimum is 6 agents (3 rf-qa + 3 rf-qa-qualitative). For INTERMEDIATE gates ... minimum is 5 (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative)." Below-floor gates are REJECTED at validation.
**I22 intensity scaling (template:793–838):** `full` = per-I19 tables (Deep/Heavyweight, >1500 lines, or user "thorough"); `standard` = 7 final agents (3+3+1 domain); `lite` = 3 final agents. The example ran `qa-full` (example tag line 54). **For this hardening task pick `full`/`standard`** per the BUILD_REQUEST's qa_intensity; the FINAL gate floor is 6 at full for a <500-line output surface, scaling up by output size.

### Exact `- [ ]` item shape for a single embedded QA agent (I15 template:649–651; live example:340 region)
Each lens agent spawn is ONE self-contained `- [ ]` item that embeds the agent's entire standalone prompt. Observed pattern (example lens-QA item, `.../TASK-RF-detection-contract...md`):
> `- [ ] Read <input files> because <why coverage matters>, then spawn <N>` rf-qa `agents in parallel, each with` fix_authorization: false `and a fully embedded standalone prompt — agent A:` QA_MODE: task-integrity`,` QA_PHASE: <gate>`,` lens: <lens-name>`, assigned files = <paths>, adversarial framing "Assume at least <N> defects exist in <lens area>; find them", checklist = <lens-specific checks>, output report` <${TASK_DIR}/phase-outputs/reviews/phase-N-qa-<lens>.md>`, PASS/FAIL rule = FAIL on any finding of any severity; agent B:` lens: <...>` …; agent C:` lens: <...>` …. If unable to spawn agents or collect reports, log the blocker … in the` ### Phase Gate Findings `section …, then stop … Once done, mark this item as complete.`

Each agent MUST carry (template:649): agent type (rf-qa | rf-qa-qualitative), assigned lens, input files, output report path, `fix_authorization: false`, and adversarial framing ("Assume this document has at least N errors focused on your lens. Find them." — N scales 5/10/15/20 by size, template:729). **No QA is implicit or prose-only** (template:651). Consolidation, fix agent, and each verification agent are ALSO separate `- [ ]` items (I20 template:757; example shows consolidate → fix-decision → single fix agent → structural-verify → content-verify → PASS-gate as six sequential items).

---

## 4. POST reflect gate item — the FLAT wrapper shell-out (canonical form)

The builder MUST emit this as the **penultimate final-phase item**, immediately before `Update task status to Done` (SKILL.md:1729, 2263, 2322). The canonical, must-reproduce-exactly form (SKILL.md:2205, matched by the shipped example at example:426):

**Skip guard (recursion breaker, contract §3.2) then the wrapper command:**
```bash
if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi
superclaude reflect run {TASK_FILE} --depth deep --fix --promote
```
where `{TASK_FILE}` is the **absolute** task file path (wrapper absolutizes its positional).

**Exact rules the item must encode (SKILL.md:2203–2208, 2322):**
- Before the shell-out: stage new task artifacts (`git add -A` — the wrapper audit omits never-`git add`-ed files; SKILL.md:2205). The example scopes staging to explicit task paths and **verifies no `.claude/` path was staged** (`git diff --cached --name-only | grep -E '(^|/)\.claude/'` → unstage hits) (example:426) — mirror this given the project's `.claude/`-never-staged rule.
- **NO `--base`** (wrapper resolves audit base from frontmatter `start_commit` as a SINGLE ref diffed vs the working tree, so uncommitted task edits ARE audited; base precedence `--base` > frontmatter `start_commit` > `git merge-base HEAD master`) (SKILL.md:2205).
- `--depth deep` is **fixed** (O1 forces Tier-2 fan-out); `--fix` runs the bounded audit→apply→re-verify loop; `--promote` lets the `task` adapter move the tasklist dir to `done/` on a clean/auto-fixed PASS (SKILL.md:2205).
- Emit **NO** `--reflect`, **NO** `--max-turns`, **NO** `<base>..HEAD` range, and **no agent-spawn / subagent directive** of any kind — the gate is a flat Bash shell-out, never a subagent (NFR-7 clean; SKILL.md:2205, 2263).
- **Consume the EXIT CODE** (SKILL.md:2205, 2322): only `0` completes the gate (clean OR auto-fixed-and-verified) and lets Update-status-to-Done proceed; `10` (halted — human-required deviations / non-convergent fix loop), `11` (degraded — audit untrustworthy), and `2` (blocked — child crash / missing-or-bad contract) all **FAIL** → surface the wrapper report and HALT before Done.
- The wrapper writes `reflect_post: {verdict, run_id, report}` back to frontmatter itself — the item **MUST NOT** hand-author or lock `reflect_post` (SKILL.md:2206, 2157).
- Gate command uses `superclaude reflect run`; any **re-execution uses `/task`** (never `/sc:task`) (SKILL.md:2205).

**MALFORMED if (SKILL.md:2263, 2322):** the item is omitted when POST_REFLECT_GATE is ENABLED, OR it emits the **legacy self-run reflect-subagent** form, OR a **human-handoff / HALT** form instead of the flat wrapper shell-out. → Do NOT emit a "spawn a reflect subagent" item and do NOT emit a "pause for human review" item.

**Then, AFTER it, the `Update task status to Done` item (anti-orphaning, SKILL.md:2210–2214; example Step 5.7, example:430):** reads the task file, confirms every prior item is `- [x]`, confirms `reflect_post` holds a non-empty wrapper-written verdict, confirms the wrapper exited 0 and no unresolved blocker remains, THEN sets `status: 🟢 Done` + `completion_date` + `updated_date` and appends an Execution Log entry. It must be the ONLY item after the wrapper. The example wraps this as its own single-paragraph self-contained item with a Blocked fallback.

---

## 5. `## Execution Context` block rules + TB-Add-7 / TB-Add-8

**Template rules (template:1193–1207):** the block has three builder-populated subsections:
- **`### References`** (template:1197–1199) — governing docs/specs/workflow files, format `- [Document Name](path): [one-line purpose]`.
- **`### Source Areas`** (template:1201–1203) — codebase dirs/modules/file-sets read or modified, format `- path/to/area/: [what it contains / why relevant]`. **Module names / directories, NO file:line.**
- **`### Key Constraints`** (template:1205–1207) — top governing constraints: QA intensity, scope limits, known blockers, standing prohibitions.
Also present: `### Handoff File Convention` (template:1209–1221 — `phase-outputs/{discovery,test-results,reviews,plans,reports}/`) and `### Frontmatter Update Protocol` (template:1223–1231). The example adds `### Open Questions` and `### Execution Command` (example:129–144) — include an `### Execution Command` line stating `/task <abs-path>` and "Do not use `/sc:task`".

**TB-Add-7 (SKILL.md:1389, gate at 2261):** every `Source Areas` entry in `## Execution Context` MUST reappear in at least one item's Context field; **the block itself contains NO specific file:line references** (INACTIVE if no Execution Context block). → Header carries module/dir names only; the file:line detail lives in items.

**TB-Add-8 (SKILL.md:1390, gate at 2262):** every per-item Context field that references a code surface MUST include a **file:line citation OR an `<!-- evidence-absence: ... -->` justified-absence comment** (proves PR-01's "no specific paths in header" is confined to the header — INV-015 scope-confinement). → In each monitor.py-hunk item and each test item, cite the exact `monitor.py:LINE` / fixture / test path; where a surface does not yet exist (new fixture/test file), add an `<!-- evidence-absence: new file, no prior line -->`-style comment.

The example demonstrates both: `Source Areas` (example:116–122) lists only directories (`src/superclaude/pr_submit/`, `tests/pr_submit/`, …) with no line numbers, and item Context fields carry the concrete paths.

---

## 6. Concrete structural patterns to mirror (from `TASK-RF-detection-contract-20260701-164700.md`)

1. **Phase naming = descriptive + role-labeled**, not bare numbers: `### Phase 1: Setup, Handoff Workspace, and Human Decision Gates`, `### Phase 5: Final QA, Reflection, and Completion` (example:148, 5.x region). Each phase opens with a `**Step N.M: <title>**` bolded sub-header, then its `- [ ]` item(s).
2. **Item numbering via Step sub-headers** — items are grouped under `**Step 5.1: Aggregate final implementation outputs**`, `**Step 5.2: Run final scoped pytest with UV**`, `**Step 5.7: Update task status to Done**` (example:428). The POST-reflect item sits as the penultimate step; Done is the final step (example:426 then 428/430). This satisfies anti-orphaning ordering (template:1242–1243 warns: components first, summary/Done LAST).
3. **QA gate laid out as a contiguous run of sibling `- [ ]` items under one `**Phase N QA Gate: …**` header** (example:~344+): (a) 3 rf-qa structural-lens spawns in one item, (b) 3 rf-qa-qualitative content-lens spawns in one item [each item embeds 3 agents A/B/C with distinct lenses], (c) consolidate-findings item, (d) fix/no-fix decision item, (e) single fix-agent item, (f) structural-verification item, (g) content-verification item, (h) PASS-gate/proceed item. Every agent prompt is fully embedded with `QA_MODE`/`QA_PHASE`/`lens`/`fix_authorization`/adversarial-framing/output-report/PASS-FAIL-rule.
4. **UV-only + lint-scoped discipline baked into items** (example:340): "`uv run ruff check <changed trees>` … scoped to only the changed source/test trees so no unrelated file is reformatted"; "`uv run pytest <paths> -v` … no bare pytest". Every code/test item captures raw output to `phase-outputs/test-results/*.txt` and appends a PASS/FAIL line to a shared `*-validation-verdict.md`. **Mirror this for the sprint-429 regression/lint/verify items** (`make lint` is `ruff check` only — CI also runs `ruff format --check`; scope ruff to changed files per project memory).
5. **Every item ends with the exact Blocked-fallback + completion-gate sentence** (example, all items): "If unable to complete due to <specific blockers>, log the specific blocker using the templated format in the `### Phase N - … Findings` section of the `## Task Log / Notes` …, then stop before marking this item complete until the blocker is resolved. Once the action and verification pass, mark this item as complete." — this is B2 elements 5+6 rendered literally.

---

## Summary (for the builder)

- **Frontmatter:** copy template:1–61 fields, set `task_type: static`, populate `spec_path` to the merged-requirements path, leave `reflect_post: ""` untouched, and ADD builder keys `start_commit` (= `git merge-base HEAD <integration-branch>`) and `executor_model_class` (e.g. `sonnet`) per SKILL.md:2155–2168. Populate `reflect_pre` after the PRE gate.
- **Granularity (A3/A4/B2/B3):** one self-contained single-paragraph `- [ ]` item per change — each of the 3 fixtures, each of the 2 monitor.py hunks, the parametrized contract-table test, and each of the 4 parity tests is its own item, each embedding Context+WHY / Action+WHY / Output / "ensuring…" verification / blocker-log-on-failure / completion-gate. Mirror the shipped example's paragraph form (not the SKILL tail's field form).
- **QA gate:** M3 lens-based, FINAL_ONLY floor = 6 agents (3 rf-qa structural + 3 rf-qa-qualitative content, I19 <500-line row) with serialized fix (consolidate → 1 fix agent → 2-agent verify → PASS gate), every step its own `- [ ]` item, each agent prompt fully embedded with lens + `fix_authorization: false` + adversarial framing. M4 fidelity gate only if the code is judged spec-derived (likely omit; note the omission).
- **POST reflect:** penultimate final-phase item = FLAT wrapper shell-out `superclaude reflect run {abs TASK_FILE} --depth deep --fix --promote` behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard, `git add -A` (with a `.claude/`-not-staged verify) first, NO `--base`/`--reflect`/`--max-turns`/range/subagent, consume exit code (only 0 proceeds; 10/11/2 FAIL+HALT), wrapper writes `reflect_post` back (never hand-author). Then the `Update task status to Done` item AFTER it (anti-orphaning).
- **Execution Context:** References / Source Areas (module/dir names, NO file:line — TB-Add-7) / Key Constraints; per-item Context code refs carry file:line or `<!-- evidence-absence: … -->` (TB-Add-8). Add an `### Execution Command` line pointing at `/task <abs-path>` (never `/sc:task`).
