# Research: patterns, conventions, sync, reflect-flags

Status: In Progress
Date: 2026-06-04
Agent: R5 (Patterns & Conventions + reflect flag-surface confirmation)

---

## Area 1 — Reflect Flag Surface (AUTHORITATIVE CONFIRMATION)

**Highest-value deliverable.** Every flag the two proposals template was checked against the live reflect surface. Source files (all Read this session):
`src/superclaude/commands/reflect.md` (Options table L66-96, STOP conditions L30-36, Usage L39-62),
`src/superclaude/skills/sc-reflect-protocol/SKILL.md` (Inputs L64-95, mode-selection L92-103, STOP L106-111, depth/tier overrides §5.1 L356-364),
`refs/input-resolution.md`, `refs/reviewer-spec.md`, `refs/cost-profile.yaml`.

### 1.1 Definitive flag → exists? → file:line → semantics table

| Flag (as templated by proposals) | Exists? | Authoritative file:line | Confirmed semantics |
|---|---|---|---|
| `--mode pre` | ✅ YES | reflect.md:68; SKILL.md:66; SKILL.md:96 (rule 1) | UC-1 coverage/gap audit. **Requires `--spec`** (HARD STOP without it). |
| `--mode post` | ✅ YES | reflect.md:68; SKILL.md:66; SKILL.md:97 (rule 2) | UC-2 deviation audit. **Requires `--diff` OR `--task-log`** (HARD STOP without either). |
| `--spec <path>` | ✅ YES | reflect.md:72; SKILL.md:67 | Driving spec/PRD/objectives doc. Required for UC-1; recommended for UC-2. |
| `--tasklist <path>` | ✅ YES | reflect.md:73; SKILL.md:68 | Tasklist file. Required for UC-2; recommended for UC-1. |
| `--diff <range>` | ✅ YES | reflect.md:74; SKILL.md:69 | Git ref (`HEAD~1..HEAD`, branch) or diff-file path. Satisfies UC-2 input. |
| `--depth quick` | ✅ YES | reflect.md:78; SKILL.md:73; **SKILL.md:361 (§5.1 hard override: "STOP at T1")** | Tier 1 ONLY — hard override, skips Wave 3+. **CONFIRMS O4 floor rationale: `quick` disables regression-escalation (§5.3 rule 3 never fires because Wave 3 is skipped).** |
| `--depth standard` | ✅ YES | reflect.md:78; SKILL.md:73 | Tier 1, then escalate by §5.3 rubric (the rubric — incl. rule-3 regression escalation — CAN fire). Default. |
| `--depth deep` | ✅ YES | reflect.md:78; SKILL.md:73; **SKILL.md:362 (§5.1 hard override: "ALWAYS escalate to T2")** | Force Tier 2 (heterogeneous ensemble) unconditionally. |
| `--tier 1\|2\|auto` | ✅ YES | reflect.md:79; SKILL.md:74; SKILL.md:359-360 (§5.1) | Explicit tier PIN overriding rubric. `auto` default. NOTE: `--tier 2` + zero env-aliases ⇒ **STOP** (SKILL.md:221, input-resolution.md:87). |
| `--remediate` | ✅ YES | reflect.md:89; SKILL.md:78; input-resolution.md:23 | Audit-first: after report ships, OFFER Tier-3 task-builder chain; operator runs `/task` themselves. **Never auto-executes** (reflect.md:255-263). |
| `--executor-model <class>` | ✅ YES | reviewer-spec.md:74; reviewer-spec.md:92 | **EXCLUSION flag, NOT selection.** Names the executor's model class so reflect REMOVES it from the reviewer rotation (anti-self-confirmation). Resolution order: flag → `EXECUTOR_MODEL_CLASS` env → log-heuristic → unknown (fail-open, weakened guarantee logged). |
| `--budget-remaining <int>` | ✅ YES | reflect.md:90; SKILL.md:82; SKILL.md §4.0 step 0.9 (L286-296) | Caller budget hint; reflect cross-checks §15 cost profile and may auto-downgrade tier; emits `budget_forced_tier_downgrade`. |
| `--output <dir>` | ✅ YES | reflect.md:81; SKILL.md:76 | Output dir. Default `.dev/reflect/<mode>-<slug>-<ts>/`. **HARD STOP if it resolves under `.claude/skills,agents,commands/`** (reflect.md:35, SKILL.md:111). |
| `--task-log <path>` | ✅ YES | SKILL.md:72; SKILL.md:109 | UC-2 alternative input when no diff. (Templated indirectly via the UC-2 "diff OR task-log" requirement.) |
| `--coverage-floor <float>` | ✅ YES | reflect.md:82; SKILL.md:77 | UC-1 coverage stop-floor override (default 0.90). task-builder proposal §6.1 references the 0.90 floor — consistent. |
| `--tier auto` (sc:tasklist proposal §4 band `4-9`) | ✅ YES | SKILL.md:74 (`auto` is the documented value) | Defers T1/T2 to the rubric. Valid. |

### 1.2 NO model-routing / model-selection flag is introduced — CONFIRMED

`grep -nE "\-\-model\b"` across `reflect.md`, `SKILL.md`, and all `refs/*.md` returns **zero matches**. The ONLY model-related flag is `--executor-model`, which is an **exclusion** flag (reviewer-spec.md:74 "The *executor* … MUST NOT appear in the reviewer pool … When the executor's class is in the candidate rotation, it is **removed**"). Both proposals correctly state they introduce no model-routing flag and that spawned reflect agents use the default subagent model (task-builder proposal §6.4 L239-241; sc:tasklist proposal §5 L274-278). Reviewer heterogeneity comes from env-alias routing (SKILL.md:216-228) + the rotation table (reviewer-spec.md:80-84: `2→sonnet,haiku`; `3→sonnet,haiku,(qwen|kimi|deepseek else opus)`). **No defect.**

### 1.3 `--depth quick` disables regression-escalation — CONFIRMED (O4 floor is sound)

SKILL.md §5.1 (L361) lists `--depth quick` as a **hard override = "STOP at T1"**, i.e. Wave 3+ is skipped. §5.3 rule 3 (L387, "regression must be debated by ≥2 reviewers") lives in the Tier-2 escalation rubric that ONLY runs when Tier 1 does NOT stop. Therefore `quick` structurally cannot reach the regression-escalation path. The task-builder proposal's **O4 POST-gate floor** (never emit `--depth quick` for the POST gate, since it audits executed code where regression matters most) is **technically correct and load-bearing** — emit `--depth standard` minimum at POST.

### 1.4 Cross-skill invocation pattern the A.10.7 PRE gate must mirror — CONFIRMED

The proposals say the PRE gate should mirror how `/sc:brainstorm` invokes the adversarial skill. The exact pattern (sc-brainstorm-protocol/SKILL.md:278):

> **Invoke**: `Skill sc-adversarial-protocol` with above arguments. **Direct skill invocation, not command — per sc:roadmap pattern.**

So the A.10.7 PRE gate must invoke reflect via **`Skill sc:reflect-protocol`** (direct skill invocation, NOT the `/sc:reflect` command), passing the flag string as arguments — mirroring reflect.md's own Activation directive (reflect.md:127-128: "invoke: `> Skill sc:reflect-protocol`"). The task-builder proposal §6.1 L171 already states this ("Direct skill invocation, mirroring how `/sc:brainstorm` Wave 3 invokes `Skill sc-adversarial-protocol`"). **Consistent — no defect.**

### 1.5 Cost bands (for the depth-determinism cost argument) — CONFIRMED

cost-profile.yaml: T1 = 3-8k Claude tokens / 60-180s (L38-40); T2 = 35-70k / 480-900s (L50-52); T3 adds 20-40k (L61-63). Both proposals cite these correctly. The ~10× quick→deep multiplier (task-builder §2.3 L50) is accurate (8k→70k upper bound ≈ 8.75×).

### 1.6 FLAG-SURFACE VERDICT

**Every flag templated in BOTH proposals exists with the claimed semantics. No nonexistent flag is templated. No defect found.** A builder generating these command strings will emit only real reflect flags. The one nuance to preserve in the generated MDTM/skill text: `--executor-model` must be described as an *exclusion* (not selection) flag, and `--depth quick` must never be emitted for a POST gate (O4).

---

## Area 2 — SKILL.md Structural Conventions (house style for new content)

### 2.1 task-builder/SKILL.md — Stage heading convention (A.x)

Pipeline stages use **`### A.N: Title`** (h3, colon, sequential). Sub-versions use a decimal: `### A.10.5: Task File Qualitative Validation` (SKILL.md:1194), `### A.10.6: …` (:1339). So the new PRE gate must be **`### A.10.7: <Title>`** (h3, colon-style) to match. Representative shape (A.10.5, SKILL.md:1194-1199):

```
### A.10.5: Task File Qualitative Validation

After structural QA passes, validate that the task file would actually succeed if executed. This step catches operational issues that structural QA cannot: …

**Spawn rf-qa-qualitative:** Use the Agent tool with `subagent_type: "rf-qa-qualitative"`, `mode: "bypassPermissions"`.

**ADVERSARIAL STANCE:** Assume the work contains errors. …
```

Pattern: h3 heading → 1-paragraph purpose → bolded `**Directive:**` lead-ins → fenced prompt blocks labeled ` ```text `. The pipeline-overview bullet list (SKILL.md:155-162) must also gain a step for A.10.7.

### 2.2 task-builder Critical Rules convention

Header is **`## Critical Rules (Non-Negotiable)`** (SKILL.md:1998). Rules are an **ordered (1., 2., …) list**, each `**Bold lead.** Prose.` (SKILL.md:2000-2030). The new POST_REFLECT_GATE rule appends as **#19** (current highest is #18, SKILL.md:2030; Precedence rule follows at :2032). Match the existing `**Bold lead.** …MALFORMED output.` cadence.

### 2.3 Critical Rule #16 machinery (the pattern POST_REFLECT_GATE reuses) — quoted

SKILL.md:2030 (verbatim):

> **16. QA gates in generated task files.** When the BUILD_REQUEST specifies QA_GATE_REQUIREMENTS of FINAL_ONLY or PER_PHASE, the builder MUST encode corresponding QA gate checklist items in the generated task file. These items must specify the QA agent type (rf-analyst, rf-qa, rf-qa-qualitative), the QA mode, the files to verify, and the pass/fail handling. **A generated task file that omits required QA gates is a MALFORMED output.**

The reusable machinery = **(BUILD_REQUEST field present) → (builder MUST emit a specific checklist item with specified sub-fields) → (omission = MALFORMED output)**. Rules #17 (VALIDATION_REQUIREMENTS) and #18 (TESTING_REQUIREMENTS) follow the identical template (SKILL.md "…is a MALFORMED output." closer on each). The new rule should read: *"When `POST_REFLECT_GATE: ENABLED`, the builder MUST emit … the penultimate item of the final phase … A generated task file that omits the POST reflect item when POST_REFLECT_GATE is ENABLED is a MALFORMED output."* — mirroring the closer exactly so the A.10 structural validator can enforce it (this is proposal §7 risk 5 / §6.2).

### 2.4 B2 self-contained item shape (Context/Action/Output/Verification/Completion gate) — quoted

The canonical generated-MDTM item (SKILL.md:1916-1921):

```
- [ ] **1.1 — [Step Title]**
  - **Context**: [What the executor needs to know]
  - **Action**: [Exactly what to do]
  - **Output**: [What gets created/modified]
  - **Verification**: [How to confirm it worked]
  - **Completion gate**: [When this item is done]
```

The final-phase Done item (SKILL.md:1928-1935) is the anchor the POST reflect item sits **immediately before** (penultimate position, anti-orphaning §2.5). The templated POST item in the task-builder proposal (§6.2 L206-227) already conforms to this exact 5-field shape — **consistent with house style**.

### 2.5 task-builder Validation Checklist convention

Header **`## Task File Validation Checklist`** (SKILL.md ~:1957), items are `- [ ]` unchecked-checkbox bullets (SKILL.md:1959-1969, e.g. `- [ ] Items follow B2 self-contained pattern (context + action + output + verification + completion gate)`, `- [ ] Anti-orphaning: completion items inside final phase`). The new "POST reflect item present + correctly positioned when POST_REFLECT_GATE ENABLED" check appends here as another `- [ ]` bullet.

### 2.6 sc-tasklist-protocol/SKILL.md — Stage + gate + Self-Check conventions

- **Stage headings:** `### Stage N: Title` (h3, colon). E.g. `### Stage 7: Roadmap Validation (2N Parallel Agents)` (SKILL.md:1174), `### Stage 10: Spot-Check Verification` (:1359). The new gate is **`### Stage 10.5: Pre-Reflect Sign-off`** — decimal sub-stage matching the A.10.5 precedent on the task-builder side.
- **Structural gates** are a **numbered table** `| # | Check | Rationale |` (SKILL.md:1108-1115). Gate #19 verbatim (SKILL.md:1114): `| 19 | End-of-phase position: the \`### T<PP>.<NN> -- Checkpoint: End of Phase <PP>\` task has the highest \`<NN>\` in its phase, with no regular task following it | Ensures the end-of-phase gate is the last instruction the agent sees |`. The closer "**If any check 1-20 fails, fix it before writing any output file.**" (SKILL.md:1117) must be updated to whatever the new highest number is if a gate row is added.
- **Self-Check** (SKILL.md:1066-1074) is a **numbered list** under `## Sprint Compatibility Self-Check (Pre-Write, Mandatory)`; check #6 verbatim: `6. Every phase file ends with an end-of-phase checkpoint task (per checks 18-20)`. The sc:tasklist proposal's Decision C1 (§proposal L117) correctly identifies that the checkpoint-is-last invariant is encoded in **four** coupled places — check #6 (:1073), structural check #18 (:1113), gate #19 (:1114), gate #20 (:1115) — and all four must be amended together. **House-style note:** edits to these are surgical row/line edits, NOT rewrites.

### 2.7 The generated POST MDTM task in sc:tasklist is a DIFFERENT shape than task-builder's

Critical for R6/the editor: sc-tasklist generated tasks use the **Sprint-CLI metadata-table format** (`### T<PP>.<TT> -- Title` + a `| Field | Value |` table with Tier/Effort/Risk/Verification Method/Sub-Agent Delegation/Deliverable IDs + `**Steps:**` + `**Acceptance Criteria:**`), NOT the B2 Context/Action/Output shape (SKILL.md:862-916). The proposal's templated POST task (§proposal L167-209) correctly uses this Sprint-CLI table shape. **Do not cross-contaminate:** task-builder POST item = B2 5-field shape; sc:tasklist POST task = Sprint-CLI metadata-table shape.

---

## Area 3 — SoT Sync + Lint Discipline

### 3.1 `make sync-dev` — what it copies (Makefile:109-165)

Copies, one-directional, **`src/superclaude/` → `.claude/`**:
- **Skills:** every `src/superclaude/skills/<name>/` (skipping `__*`) with a `SKILL.md`/`skill.md` → `.claude/skills/<name>/`, recursive `find`, excluding `__init__.py` + `__pycache__`.
- **Agents:** `src/superclaude/agents/*.md` (skip README.md) → `.claude/agents/`.
- **Commands:** `src/superclaude/commands/*.md` (skip README.md, `__init__.py`) → `.claude/commands/sc/`.
- **Hooks:** `src/superclaude/hooks/scripts/*.sh` → `.claude/hooks/` (chmod +x) + `session-init.sh`.
- **Templates:** `src/superclaude/templates/` → `.claude/templates/`.

**Binding for the edits:** edit `task-builder/SKILL.md`, `sc-tasklist-protocol/SKILL.md`, and `reflect.md` ONLY under `src/superclaude/`, then `make sync-dev`. The `.claude/` copies of those three files are sync output.

### 3.2 `make verify-sync` — what it checks (Makefile:166+)

For Skills/Agents/Commands/Hooks/Templates it runs **bidirectional `diff -rq`** (`--exclude __init__.py __pycache__`): every `src/` item must exist + match in `.claude/`, AND every `.claude/` item must have a `src/` counterpart (else "not distributable!"). Any drift → `drift=1` → `exit 1` with "Run 'make sync-dev' to fix". It also checks installer registration (`_FRESHNESS_SCRIPTS`) and hooks cross-consistency — **not relevant to these SKILL.md/command edits** (no hook/installer changes). **Run `make verify-sync` before committing** (per CLAUDE.md rule + the pre-commit `verify-sync` local hook).

### 3.3 `.claude/` is gitignored except settings.json — CONFIRMED

`.gitignore:117-118`: `.claude/*` then `!.claude/settings.json` (plus narrow cache allowlist :120-124). So `.claude/skills/`, `.claude/commands/sc/`, `.claude/agents/` are all gitignored. **NEVER `git add` the `.claude/` mirrors** of the edited files (CLAUDE.md ABSOLUTE RULE + memory `feedback_claude_dir_gitignored`). Stage only the `src/superclaude/` side. There is also a pre-commit SoT-discipline gate (.pre-commit-config.yaml ~:97) that rejects `.claude/` mirrors on the commit path.

### 3.4 `.markdownlint.json` active rules (root config)

```json
{ "default": true, "MD024": { "siblings_only": true }, "MD013": false, "MD029": false, "MD036": false, "MD033": false }
```

`"default": true` ⇒ **ALL** markdownlint rules are ON except the four explicitly disabled:
- **MD013 (line-length): DISABLED** — long lines OK. (The dense TCS/COMPLEXITY_SCORE tables and long templated command strings are fine.)
- **MD024 (duplicate-heading): `siblings_only`** — duplicate headings allowed only if NOT siblings under the same parent. Reusing a heading like `### Context` at the same nesting level twice in one section WILL trip it.
- **MD029 (ordered-list-prefix): DISABLED** — non-`1.`-style ordered lists OK.
- **MD036 (emphasis-as-heading): DISABLED** — `**Bold lead.**` lines (the Critical-Rules / stage-directive house style) won't trip.
- **MD033 (inline-HTML): DISABLED** — `<!-- comment -->` and inline HTML OK.

### 3.5 Which files are actually linted (pre-commit scope)

markdownlint-cli runs with `--fix` and **excludes `\.dev/.*`** (.pre-commit-config.yaml:80). So:
- **The SKILL.md / reflect.md edits under `src/superclaude/` ARE linted** (with autofix on commit).
- **This research file and any generated task file under `.dev/tasks/` are NOT linted** — markdownlint never sees them. (So the dense tables in the *generated MDTM output* don't risk a markdownlint failure; only the *skill-source* edits do.)

### 3.6 Active rules the dense new sections COULD trip — concrete avoid-list

Because `MD013` is OFF, long lines are NOT a risk. The live risks for the **`src/superclaude/` SKILL/command edits** (which ARE linted, default=true):

| Rule | Status | Risk in the new content | Avoid-guidance for the editor |
|---|---|---|---|
| **MD040** (fenced-code-language) | **ACTIVE** (default true) | Every ``` ``` ``` fence MUST declare a language. The TCS formula block, the templated `/sc:reflect …` command blocks, the `POST_REFLECT_GATE` BUILD_REQUEST block, and the frontmatter YAML block are all fenced. A bare ``` ``` ``` fence FAILS. | Tag EVERY fence: ` ```text ` for command/formula/BUILD_REQUEST blocks (matches existing A.10.5 ` ```text ` convention), ` ```yaml ` for the `reflect_pre:` frontmatter block, ` ```markdown ` for the templated MDTM item. NOTE: `sc-reflect-protocol/SKILL.md:8` opts out via `<!-- markdownlint-disable MD013 MD040 -->`, but **task-builder/SKILL.md and sc-tasklist-protocol/SKILL.md do NOT have that disable** — so MD040 is enforced there. Do NOT add a disable comment to escape it (see §4.4); just label the fences. |
| **MD001** (heading-increment) | **ACTIVE** | New `### A.10.7` / `### Stage 10.5` headings must not skip a level (no `###` → `#####`). Sub-bullets use `-` lists, not deeper headings. | Keep new stage headings at h3 (`###`) matching siblings; use bold-lead paragraphs + `-` lists underneath, never `#####`. |
| **MD024** (duplicate-heading, siblings_only) | **ACTIVE (siblings_only)** | If the new section introduces two same-text headings at the same nesting (e.g. two `#### Behavior`), it trips. | Give each new heading a distinct title; the proposal's `## Reflect Depth (Deterministic TCS)` etc. are already unique. |
| **MD012** (multiple-blank-lines) / **MD009** (trailing-spaces) / **MD047** (single-trailing-newline) | **ACTIVE** | Hand-authored dense tables often leave double blank lines or trailing whitespace. | One blank line between blocks; no trailing spaces; file ends with exactly one newline. (`--fix` autofixes most, but author clean to avoid surprise diffs.) |
| **MD031** (blanks-around-fences) / **MD032** (blanks-around-lists) | **ACTIVE** | Fenced code blocks and lists need a surrounding blank line. | Put a blank line before/after every fence and every list block in the new sections. |
| **MD041** (first-line-h1) | **ACTIVE** but not at risk | Only the file's first line matters; edits are mid-file. | No action — not inserting at line 1. |

**Bottom line for the editor:** the single highest-probability failure is **MD040 (unlabeled fences)** in task-builder/SKILL.md and sc-tasklist-protocol/SKILL.md, since the new content is fence-heavy and those two files have NO inline disable. Label every fence (` ```text ` / ` ```yaml ` / ` ```markdown `). MD013 being off means the wide tables and long command strings are safe.

---

## Area 4 — Constraining Memories (binding constraints on the EDITS)

Read directly from `/config/.claude/projects/-config-workspace-IronClaude/memory/`.

### 4.1 `feedback_sc_reflect_vs_inline_rfqa.md` — POST must be independent / executor-disjoint, never inline

Key quotes:
- (:10) "When `/task` execution spawns inline rf-qa … the same-agent self-review bias is structurally unmitigated."
- (:12) "**Mitigation:** Run `/sc:reflect --mode post --diff <commit-range>` as a separate step after each phase commit."
- (:26) "this catch held even though the executor (Opus) ran the reflect — because **the load-bearing independence was the executor-disjoint reviewer classes (sonnet/haiku), not the orchestrator.**"

**Binding constraint on the edits:** the POST reflect gate's value comes from **executor-disjoint reviewers**, so the generated POST item MUST be a **fresh-session, NOT-inline** handoff, and MUST pass `--executor-model <class>` so reflect excludes the executor's class from the reviewer pool. This is exactly the task-builder proposal's Decision B3 (templated fresh-session handoff) and the sc:tasklist proposal's Decision C1 (fresh-session spawn directive). Do NOT template a POST item that runs reflect inline in the executor's session — that reproduces the very bias the memory documents (confirmed 3×).

### 4.2 `feedback_human_decision_items_must_halt.md` — PRE remediation must HALT, never auto-mutate

Key quotes:
- (:10) "needs_human_decision items MUST write a `PENDING` sentinel and HALT the dependent mutation … It must NOT 'apply the recommended default under unattended execution'."
- (:14) "Always run `/sc:reflect --mode pre` on a freshly-built corrective tasklist before executing — the independent reviewer is non-vacuous specifically against `needs_human_decision`/spec-contradiction items."

**Binding constraint on the edits:** (1) The PRE gate (A.10.7 / Stage 10.5) is **advisory-blocking**: on FAIL it annotates frontmatter + appends to `### Open Questions` **additively (never rewrites existing items)**, and SURFACES the `--remediate` offer — it must NOT auto-loop the builder or auto-mutate the tasklist (task-builder proposal Decision A3 §4; sc:tasklist proposal Q4 §resolved). (2) The POST item must **HALT (PENDING)** until the operator records the verdict, never auto-promote to Done. (3) This memory itself *validates* placing a PRE reflect gate immediately post-generation — it is the cited justification for the whole PRE-gate design.

### 4.3 `feedback-no-sctask-on-task-builder-tasklists.md` — never `/sc:task`, always `/task`

Key quotes:
- (:10) "Never suggest `/sc:task` or invoke `/sc:task` on tasklists built with `/task-builder` … Use `/task` directly with the tasklist path."
- (:16) "In paste-ready resume commands surfaced to the user, use `/task` not `/sc:task`."

**Binding constraint on the edits:** Every paste-ready command the new sections emit — the POST item's surfaced operator command, the A.11 `REFLECT GATES` block, the PRE re-run command — MUST use **`/task`** for execution and **`/sc:reflect`** for the gate. **NEVER `/sc:task`.** Note the POST gate uses `/sc:reflect --mode post` (the reflect gate, not task execution) — that is correct and distinct from `/sc:task`. The task-builder proposal §2.4 / §6.2 L233 already encodes this. (Tangential but relevant: per memory `feedback_no_multiline_paste`, any surfaced paste-ready command should be single-line — the long `/sc:reflect --mode post …` string is already single-line in both proposals.)

### 4.4 `feedback_no_strategy_pivot_to_avoid_hooks.md` — do exactly what the hook says; never pivot tools

Key quotes:
- (:13) "When a hook blocks an action with a clear instruction, **do exactly what the hook says** and retry."
- (:24-31) "NEVER do any of the following to 'work around' a hook: Pivot to `mdformat`/`prettier`/`markdownlint --fix` … Switch to `sed -i`/`awk`/a Python helper … `--no-verify` … `git add -f`."
- (:56) "any time you see `freshness`/`verify-sync`/`markdownlint`/`pre-commit`/hook error message, the next thing you write … MUST be the action the hook requests."

**Binding constraint on the EDITING WORKFLOW (not the generated content):** when editing the three `src/superclaude/` files, if a hook fires:
- **freshness-pre-edit** ("Re-Read before editing") → Re-Read the file at the offset, then retry the Edit. (Note: this very research file already triggered a re-read reminder once — that is the expected discipline.)
- **markdownlint** (e.g. MD040 unlabeled fence) → **fix the actual fence label**; do NOT add a `<!-- markdownlint-disable -->` comment or run `markdownlint --fix`/`mdformat`/`sed` to escape it. (The MD040 risk in §3.6 must be resolved by labeling fences, NOT by copying reflect SKILL.md's disable comment into task-builder/sc-tasklist SKILL.md.)
- **verify-sync** drift → `make sync-dev` (src is canonical), never `--no-verify`.
- **SoT / `.claude/` staging** → move the change to `src/`, never `git add -f`.

---

## FLAG-SURFACE SUMMARY TABLE (definitive)

Every flag templated by `reflect-in-task-builder.md` + `reflect-in-sc-tasklist.md`, confirmed against the live reflect surface:

| Flag | Exists | file:line (authoritative) | Note for the builder/editor |
|---|---|---|---|
| `--mode pre` | ✅ | reflect.md:68, SKILL.md:96 | UC-1; requires `--spec` |
| `--mode post` | ✅ | reflect.md:68, SKILL.md:97 | UC-2; requires `--diff` OR `--task-log` |
| `--spec <path>` | ✅ | reflect.md:72, SKILL.md:67 | — |
| `--tasklist <path>` | ✅ | reflect.md:73, SKILL.md:68 | — |
| `--diff <range>` | ✅ | reflect.md:74, SKILL.md:69 | — |
| `--depth quick` | ✅ | reflect.md:78, SKILL.md:361 | = STOP-at-T1; disables regression-escalation → NEVER use at POST (O4) |
| `--depth standard` | ✅ | reflect.md:78, SKILL.md:73 | default; rubric may escalate |
| `--depth deep` | ✅ | reflect.md:78, SKILL.md:362 | forces T2 |
| `--tier 1\|2\|auto` | ✅ | reflect.md:79, SKILL.md:74 | `--tier 2` + 0 aliases = STOP |
| `--remediate` | ✅ | reflect.md:89, SKILL.md:78 | audit-first; offer only, never auto-run |
| `--executor-model <class>` | ✅ | reviewer-spec.md:74,92 | EXCLUSION flag (not selection); POST-only |
| `--budget-remaining <int>` | ✅ | reflect.md:90, SKILL.md:82 | may auto-downgrade tier |
| `--output <dir>` | ✅ | reflect.md:81, SKILL.md:76 | NEVER under `.claude/skills,agents,commands/` |
| `--coverage-floor <float>` | ✅ | reflect.md:82, SKILL.md:77 | default 0.90 |
| model-routing / `--model` selection flag | ❌ DOES NOT EXIST | (grep: 0 matches) | Proposals correctly introduce none; reflect uses default subagent model + env-alias reviewer rotation |

**VERDICT: No proposal-templated flag is nonexistent or has different semantics. Zero flag defects. Invocation pattern = `Skill sc:reflect-protocol` (direct skill, mirroring brainstorm→`Skill sc-adversarial-protocol`, SKILL.md:278).**

---

## MARKDOWNLINT AVOID-LIST (for the editor of the `src/superclaude/` files)

Linted files: `task-builder/SKILL.md`, `sc-tasklist-protocol/SKILL.md`, `reflect.md` (under `src/superclaude/`, default=true, autofix on commit). NOT linted: this research file + generated task files (`.dev/.*` excluded, .pre-commit-config.yaml:80).

1. **MD040 (TOP RISK — label every fence).** task-builder/SKILL.md and sc-tasklist-protocol/SKILL.md have NO inline disable, so every ``` fence in the new TCS table / templated command / BUILD_REQUEST / frontmatter sections MUST declare a language: ` ```text ` (commands/formulas/BUILD_REQUEST, matches A.10.5), ` ```yaml ` (frontmatter `reflect_pre:`), ` ```markdown ` (templated MDTM item). A bare fence FAILS.
2. **Do NOT escape MD040 by copying reflect SKILL.md's `<!-- markdownlint-disable MD013 MD040 -->`** into the other two files (per `feedback_no_strategy_pivot_to_avoid_hooks`). Label the fences instead.
3. **MD001 (heading-increment):** keep new headings at h3 (`### A.10.7`, `### Stage 10.5`); use bold-lead paragraphs + `-` lists below; never jump to `#####`.
4. **MD024 (siblings_only):** give every new heading a unique title (no two sibling `#### Behavior`s).
5. **MD031 / MD032:** blank line before & after every fence and every list block.
6. **MD009 / MD012 / MD047:** no trailing spaces, no double blank lines, single trailing newline (autofix covers these, but author clean to avoid surprise diffs).
7. **MD013 (line-length) is OFF** — the wide TCS / COMPLEXITY_SCORE tables and long `/sc:reflect …` command strings are SAFE; do not artificially wrap them.

---

Status: Complete
