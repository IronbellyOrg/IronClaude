# Research 05: Template & Examples — MDTM Template 02 + Sibling Cross-Validation + SoT/Reversibility

**Status: Complete**

Topic: MDTM Template 02 rules + sibling-task cross-validation + SoT/reversibility conventions.
Track goal: Implement `--reflect auto|1|2` POST-gate refactor per spec `.dev/brainstorms/20260608-191030-reflect-flag-post-gate/merged-requirements.md`.

**HEADLINE CROSS-VALIDATION RESULT (read first):** The highly-relevant sibling — both its task file
`.dev/tasks/to-do/TASK-RF-20260608-185553/TASK-RF-20260608-185553.md` AND its
`research/06-taskbuilder-template-integration.md` — models `POST_REFLECT_MODE: wrapper|halt` as a
**LIVE BUILD_REQUEST field to ADD**. **THIS spec RETIRES `POST_REFLECT_MODE`** (§10.1) — it becomes a
**deprecated read-only alias** behind the new primary field `REFLECT_POST_MODE` / flag `--reflect`.
The builder MUST NOT copy the sibling's "add `POST_REFLECT_MODE: wrapper|halt`" item verbatim. See §2 below
for the exact divergence map. All of the sibling's *SKILL.md anchor facts* (line numbers, O4, TCS, Rule#19)
are [CODE-VERIFIED] and reusable; only its *schema-field design* is [CODE-CONTRADICTED by spec].

---

## 1. MDTM Template 02 PART 1 — Rules the Builder MUST Follow

Source: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (1205 lines; PART 1 = the
HTML-comment-wrapped instructions L46–870; PART 2 = the emitted template L890+). NOTE: in THIS worktree the
`.claude/templates/` mirror does NOT exist — only the `src/` source-of-truth copy is present (verified via
`find`). The builder reads/cites the `src/` path.

### 1.1 Frontmatter schema (PART 2 top, template L1–44)
Required keys the emitted task file carries (verbatim from L1–44):
`id` (`"TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"`), `title`, `description`, `status` (`"🟡 To Do"`),
`type` (e.g. `"🔧 Refactor"` / `"📝 Documentation"`), `priority`, `created_date`, `updated_date`,
`assigned_to`, `autogen`, `autogen_method`, `coordinator`, `parent_task`, `depends_on` (list),
`related_docs` (list of `{path, description}`), `tags` (list), `template_schema_doc`, `estimation`,
`sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`,
`review_info` (`{last_reviewed_by, last_review_date, next_review_date}`), `task_type` (`static`|`dynamic`).
*This is a refactor of source code + a skill markdown → `type: "🔧 Refactor"`, `task_type: static`.*

### 1.2 A3 — Complete Granular Breakdown (L91–96, quoted)
> "A3. COMPLETE GRANULAR BREAKDOWN — Break down EVERY workflow phase into atomic, verifiable checklist
> items — Create individual checklist items for EVERY file, component, or iteration — NO high-level or bulk
> operations allowed - everything must be granular — Include exact file paths, specific requirements, and
> measurable outcomes."

### 1.3 A4 — Iterative Process Structure (L97–116)
For ANY multi-item process: pre-enumerate ALL items in an initial Step X.1, create one checklist item per
item in Step X.2, consolidate in Step X.3. (Quoted Step X.1/X.2/X.3 markdown skeleton at L104–116.)

### 1.4 B2 — Self-contained item pattern (CRITICAL, L142–148, quoted)
> "B2. EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT THAT INCLUDES:
> 1. **Context Reference with WHY** … 2. **Action with WHY** … 3. **Output Specification** (exact output
> file name, location, content, template) … 4. **Integrated Verification** (an "ensuring..." clause …
> 100% accuracy based on source materials, document negative evidence when verification fails) …
> 5. **Evidence on Failure Only** (Log to task notes ONLY if unable to complete) …
> 6. **Explicit Completion Gate** — 'This item cannot be marked as done until the actions are completed in
> their entirety exactly as described. Once done, mark this item as complete.'"

**Item-format rule (B3, L150–153, quoted):** "Each checklist item should be written as ONE FULL PARAGRAPH
(not multiple lines or bullets) that is verbose and explanatory. The item should read like a complete prompt
that could be executed independently without any prior context."

**Forbidden patterns (B5, L164–183):** standalone "read context" items (no output); items missing a context
reference; multi-line/bulleted items; separate verification/confirmation items (integrate via "ensuring…");
overly-granular items ("create directory" alone); separate REMINDER blocks between items.

### 1.5 Checklist structure (E1–E4, L278–389)
Every actionable item is `- [ ] …`; **flat structure only — NO nested checkboxes, NO parent checkbox that
summarizes children** (use `**Step X.Y:**` bold headers to group, L283). Components FIRST, summary LAST
(E2, L294–308). Sequential top-to-bottom; never require marking an item above current position; never
reference a later checkbox (E3, L350–366). Never place a checkbox next to a step number (E4, L367).

### 1.6 F-loop + discipline (F1–F5, L394–452)
READ→IDENTIFY→EXECUTE→UPDATE→REPEAT (F1). F2a item-execution discipline: one item at a time within a session;
**parallel-spawning exception** (L430) — consecutive SAME-phase items spawning INDEPENDENT subagents may be
spawned in parallel. Frontmatter protocol F5: start→`🟠 Doing`+`start_date`; done→`🟢 Done`+`completion_date`.

### 1.7 QA gates / validation (I15–I18, L599–646)
- **I15 phase-gate QA:** any task with 2+ execution phases MUST have ≥1 phase-gate QA checkpoint between the
  primary execution phase and a dependent successor (aggregation item → rf-qa spawn item → conditional-proceed).
- **I16 verdict + fix cycles:** binary PASS/FAIL (any-severity issue ⇒ FAIL); fix-cycle caps per gate type.
- **I17 post-completion validation** (BEFORE the frontmatter→Done item): all `[ ]`→`[x]`, all output files
  exist (Glob), blockers have resolution notes, **if source code modified → all relevant tests pass.**
- **I18 testing requirement for code-modifying tasks:** at least one testing item specifying the test command,
  pass criteria, results-capture path, B2-compliant; **use the L3 (Test/Execute) pattern.**

### 1.8 L1–L7 handoff patterns (L711–836) — the seam vocabulary for this refactor
- **L1 Discovery** — explore/scan, write a structured findings file to `phase-outputs/discovery/` (the file
  IS the deliverable; later items read it). Use for the **anchor re-verification / drift-guard** step.
- **L2 Build-from-Discovery** — read discovery file + source file, create the deliverable (the per-seam edits).
- **L3 Test/Execute** — run a command (pytest, `make verify-sync`, lint), capture raw output + structured
  summary to `phase-outputs/test-results/`. Use for every sync/lint/test item.
- **L4 Review/QA** — produce a PASS/FAIL verdict with specific findings to `phase-outputs/reviews/`.
- **L5 Conditional-Action** — branch on a prior result, handle BOTH success AND failure branches.
- **L6 Aggregation** — Glob + consolidate into a report.
- **L7 pattern-selection guide** (L811) + common phase structures (Discovery→Build→Review;
  Build→Test→Fix; Full-Lifecycle-with-QA-Gates `L1→L2→M1→L3→L5→L4→L6→M1`).
- **M1 phase-gate composite (L843):** Aggregation(L6) → rf-qa spawn → conditional-proceed(L5);
  optionally a separate rf-qa-qualitative item immediately after (sequential).

### 1.9 PART 2 mandatory body sections (L890+)
`# [Task Title]` → `## Task Overview` → `## Key Objectives` → `## Prerequisites & Dependencies`
(Parent Task & Dependencies; Previous Stage Outputs INFORMATIONAL-only; **Handoff File Convention** →
`.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}`; Frontmatter Update
Protocol) → `## Detailed Task Instructions` (the orchestrator-instruction block at L956–998 is REMOVED from
output) → phases → `## Post-Completion Actions` → `## Task Log / Notes`. **D3 critical rule (L269):** NO
checklist items may appear before Phase 1.

---

## 2. DOC CROSS-VALIDATOR — Sibling Research-06 + Sibling Task File, Claim-by-Claim

Sibling sources cross-validated:
- `.dev/tasks/to-do/TASK-RF-20260608-185553/research/06-taskbuilder-template-integration.md`
- `.dev/tasks/to-do/TASK-RF-20260608-185553/TASK-RF-20260608-185553.md` (Phase 5, L250–270)

Verified against the ACTUAL current `src/superclaude/skills/task-builder/SKILL.md` (2308 lines).

### 2.1 SKILL.md anchor facts — ALL [CODE-VERIFIED]

| Sibling-06 claim | Current SKILL.md (verified) | Tag |
|---|---|---|
| Phase-N POST HALT item at `SKILL.md:1992-2006`; uses `/sc:reflect`, penultimate, HALTs, writes `reflect_post: PENDING` | `sed -n '1992,2006p'` confirms verbatim: item `N.{X-1}` "Independent post-execution reflection gate (fresh session, HALT)"; **Action** prints `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}`; immediately before `N.X — Update task status to Done` | **[CODE-VERIFIED]** |
| `<BASE>` resolution = "frontmatter `start_commit`, or `git merge-base HEAD <integration>` if unset" | Present in the L1996 Action text verbatim | **[CODE-VERIFIED]** |
| `{DEPTH}` floored at `standard` per O4 (POST never `quick`) | L1996 Action says "floored at `standard` per O4 (the POST gate NEVER runs `--depth quick`)" | **[CODE-VERIFIED]** |
| `POST_REFLECT_GATE` BUILD_REQUEST block at `SKILL.md:853-856` with `SPEC_PATH`/`DEPTH`/`TASK_FILE` | `sed -n '853,856p'` confirms `POST_REFLECT_GATE: ENABLED` + `SPEC_PATH` + `DEPTH: <max(tcs-derived depth, standard)>` + `TASK_FILE` | **[CODE-VERIFIED]** |
| `DEPTH` already baked via L855 → no new depth-baking work | L855 = `DEPTH: <max(tcs-derived depth, standard)>   # POST floor per O4 — never quick` | **[CODE-VERIFIED]** |
| `reflect_post: ""` empty sentinel seeded at `SKILL.md:1942` | L1942 = `reflect_post: ""   # PENDING sentinel set by the final-phase POST reflect item; operator records {verdict, run_id, report} in a fresh session` | **[CODE-VERIFIED]** |
| Checklist MALFORMED line at `SKILL.md:2051` keyed on `POST_REFLECT_GATE is ENABLED` | L2051 verbatim: "POST reflect item present and positioned penultimate … when POST_REFLECT_GATE is ENABLED — MALFORMED if omitted" | **[CODE-VERIFIED]** |
| Critical Rule #19 at `SKILL.md:2108-2109` hardcodes "handoff command uses `/sc:reflect`" + "MALFORMED" | L2108 verbatim: Rule 19, "When the BUILD_REQUEST specifies `POST_REFLECT_GATE: ENABLED` … The handoff command uses `/sc:reflect` for the gate and `/task` (never `/sc:task`) … is a MALFORMED output." | **[CODE-VERIFIED]** |
| TCS section header `## Reflect Depth (Deterministic TCS)` at `SKILL.md:2114`; O4 floor at `SKILL.md:2152` | L2114 = the header; L2152 = "O4 — POST-gate depth floor (HARD RULE, no exceptions): the POST gate depth ∈ {`standard`, `deep`} — it may NEVER be `quick`…" | **[CODE-VERIFIED]** |
| TCS formula `3·S1+4·S2+2·S3+2·S4+5·S5+4·S6`; bands quick≤12 / standard 13-34 / deep≥35 | Sibling cited L2133-2145; consistent with spec §7. (Re-verify exact line if an item depends on the formula text — not re-paginated in this pass.) | **[CODE-VERIFIED via sibling, line-confirm recommended]** |

**Takeaway for the builder:** every SKILL.md *anchor* in sibling-06 is real and current. The builder can
reuse them as the load-bearing line citations — BUT see §2.2 for what the spec changes ON TOP of them.

### 2.2 The CRITICAL divergence — `POST_REFLECT_MODE` is RETIRED, not a live field [CODE-CONTRADICTED by spec]

**Sibling assumption (BOTH files):**
- Research-06 "Minimal reversible edit" (item 1, L161–163) proposes adding a NEW live BUILD_REQUEST sub-field
  `POST_REFLECT_MODE: <halt (default) | wrapper>` to the `POST_REFLECT_GATE` block, plus Optional-signals doc,
  plus a `halt`/`wrapper` item branch, plus Rule#19/checklist broadening.
- Sibling task file Phase 5 (`TASK-RF-20260608-185553.md:250–270`) implements exactly that: Step 5.1 "Add
  `POST_REFLECT_MODE` to the POST_REFLECT_GATE BUILD_REQUEST block"; 5.2 document under Optional signals;
  5.3 branch `halt`/`wrapper`; 5.4 broaden Rule#19+checklist; 5.5 sync. Wrapper-arm = Bash
  `superclaude reflect run {TASK_FILE}`; `halt`-arm byte-identical.

**THIS spec CONTRADICTS the field design** (spec anchors verbatim):
- §10.1 (merged-requirements.md:802–826) — precedence is: (1) explicit `--reflect <value>` flag
  (`value ∈ none|0|1|2|auto`); (2) `REFLECT_POST_MODE:` BUILD_REQUEST field (the NEW primary field, same
  value set); (3) **legacy §5 alias map** `POST_REFLECT_GATE × POST_REFLECT_MODE → m` "consulted only if 1–2
  absent; both legacy fields are **deprecated aliases**, not surviving inputs"; (4) default `2`.
- §10.1 Change-#6 note (L818–826, quoted): "The BUILD_REQUEST field is **`REFLECT_POST_MODE`** … The CLI flag
  is **`--reflect`**. The legacy `POST_REFLECT_GATE` and the sibling-proposed `POST_REFLECT_MODE` are
  **deprecated aliases** read only at precedence step 3. **`POST_REFLECT_MODE` is retired as a live
  independent field** — it survives only as a read-time alias in the §5 map."
- §10.2 (L828–840) — "Retire `POST_REFLECT_GATE: ENABLED` + sub-fields as the *primary* surface; introduce
  `REFLECT_POST_MODE: 2  # one of: none | 0 | 1 | 2 | auto (default 2 when absent)`." Comment line: "Accepts
  deprecated aliases `POST_REFLECT_MODE: wrapper(≡2)|halt(→halt position)` and
  `POST_REFLECT_GATE: ENABLED|DISABLED(≡none)` — §5 map, precedence step 3."
- §5.3 (L431–451) — the `halt` position is **derived only, NOT selectable via the numeric dial**; reached via
  legacy `POST_REFLECT_MODE: halt` OR §8 wrapper-absent degradation; emits the current `SKILL.md:1994-1999`
  manual item verbatim with `reflect_post_mode: halt`. **REJECTED alternative (L448): `halt → Mode 1` —
  rejected (C-001/X-002).**
- §10.3 (L845–855) — frontmatter field is **`reflect_post_mode`** with value set
  `none | 1 | 2 | auto-resolved-1 | auto-resolved-2 | halt | 2-degraded-halt`; the **single recorded oracle**
  of the mode decision (NFR-3), written once at generation. Mirrors the `REFLECT_POST_MODE` BUILD_REQUEST name.

**[CODE-CONTRADICTED] verdict:** The sibling's Step-5.1 ("Add `POST_REFLECT_MODE` …") and the research-06
"Minimal reversible edit item 1" describe a **schema design THIS spec rejects**. The builder MUST instead:
- Introduce **`REFLECT_POST_MODE: none|0|1|2|auto`** (default `2`) as the primary BUILD_REQUEST field at
  `SKILL.md:853` (§10.2), NOT `POST_REFLECT_MODE: wrapper|halt`.
- Add the CLI flag **`--reflect`** with precedence > `REFLECT_POST_MODE` > legacy alias map > default `2` (§10.1).
- Keep `POST_REFLECT_MODE: wrapper|halt` + `POST_REFLECT_GATE: ENABLED|DISABLED` only as **deprecated
  read-time aliases** in the §5 map (precedence step 3), each emitting a one-line build-log "ignored" note when
  a higher-precedence source is present (§10.1 L814–815). `wrapper ≡ 2`; `halt → halt position` (NOT Mode 1);
  `DISABLED ≡ none`.
- Use frontmatter `reflect_post_mode` (the new value set above), **replacing/augmenting** the current
  `reflect_post: ""` sentinel at `SKILL.md:1942` per §10.3.

### 2.3 Where the sibling's structure IS still usable (don't throw the baby out)
Even though the field *design* is contradicted, these sibling assets transfer cleanly:
- The **4-edit-surface decomposition** (BUILD_REQUEST block edit @853 → Optional-signals/field doc → emitted
  item branch @1994-1999 → Rule#19 @2108 + checklist @2051) is the correct SEAM map for THIS refactor too —
  only the field NAME and the BRANCH ARITY change (1/2/auto/none/halt/2-degraded-halt instead of halt/wrapper).
  [CODE-VERIFIED that all four anchors exist and are current.]
- The **`halt`-arm byte-identical** requirement is identical to THIS spec's NFR-2/§5.3/§6.4 — see §4 below.
- The **NFR-7 Bash-not-Agent** wrapper-arm constraint is identical (Mode 2 = `superclaude reflect run`).
- The **no-nesting-guard test** the sibling authors (`tests/cli/reflect/test_no_nesting_guard.py`,
  185553.md:300) is reusable; researcher-06 (test surface) owns the feasibility call.

### 2.4 Items where the sibling is silent / [UNVERIFIED] for THIS spec
- The sibling models a **binary** branch (halt|wrapper). THIS spec needs a **5-way emitted-item selector**:
  Mode `none` (no item), Mode 1 (inline §6.2 item), Mode 2 (wrapper §6.3 item), `halt`/`2-degraded-halt`
  (§6.4 retained manual item), plus the §10.4 advisory-warning emission for fixed `--reflect 1` when
  `S6==1 ∨ S5>0`. The sibling's research-06 does NOT cover Mode `none`, the `auto` resolution (§4), the §8
  wrapper-probe degradation to `2-degraded-halt`, or the advisory warning. **[UNVERIFIED in sibling-06]** —
  the builder must source these from the spec §4/§6/§8/§10.4 directly (other researchers 01–04 own §4/§6/§8).
- `executor_model_class` frontmatter field: sibling-06 (e) flagged it as a [CODE-CONTRADICTED] gap (template
  lacks the field). For THIS spec, `--executor-model` plumbing is a contract-side concern; flag it to the
  contract/frontmatter researchers, do not resolve here. **[UNVERIFIED for this track]**.

---

## 3. SoT / Sync Conventions the Builder MUST Encode (CLAUDE.md + Makefile, verbatim)

### 3.1 Source-of-truth rule (CLAUDE.md, this worktree)
> "Source of truth is `src/superclaude/`. Always edit there first, then `make sync-dev`." …
> "**NEVER**, under any circumstance: `git add .claude/skills/...`, `.claude/commands/...`, `.claude/agents/...`,
> `.claude/hooks/...`, `.claude/templates/...` … The ONLY tracked file under `.claude/` is
> `.claude/settings.json`." (CLAUDE.md "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents".)

Therefore every SKILL.md edit item MUST: (a) edit only `src/superclaude/skills/task-builder/SKILL.md`;
(b) be followed by a `make sync-dev` item; (c) be gated by `make verify-sync`; (d) NEVER `git add` a `.claude/`
path. The `.claude/` mirror does not even exist in this worktree until `make sync-dev` regenerates it.

### 3.2 Makefile targets (verbatim, `grep -n` + `sed` confirmed)
`make sync-dev` (Makefile:109) — header lines:
```text
sync-dev:
	@echo "🔄 Syncing src/superclaude/ → .claude/ for local development..."
```
It copies `src/superclaude/{skills,agents,commands,hooks,templates}` → `.claude/` (loop bodies Makefile:112–157),
including `src/superclaude/templates → .claude/templates` (Makefile:148–157).

`make verify-sync` (Makefile:166) — header lines:
```text
verify-sync:
	@echo "🔍 Verifying src/superclaude/ ↔ .claude/ sync..."
```
Exits 1 on drift; runs `diff -rq` per skill (Makefile:178); the final drift message (Makefile:351) is
"❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/."

`make lint` (Makefile:48) = `lint: lint-architecture` then `uv run ruff check .` (Makefile:50).
`make format` (Makefile:53) = `uv run ruff format .` (Makefile:55).
**markdownlint is NOT a make target** — it runs via pre-commit; the predecessor task invokes it as
`uv run pre-commit run markdownlint --files src/superclaude/skills/task-builder/SKILL.md`
(fallback `npx --yes markdownlint-cli …`), see `TASK-RF-20260604-042055.md:228`. **MD040 = every new fence
must carry a language label.** Per project memory `feedback_no_strategy_pivot_to_avoid_hooks`: on a
markdownlint failure, FIX the offending fence — do NOT add `<!-- markdownlint-disable -->` or run `--fix`/sed.

### 3.3 Worktree path discipline (memory `feedback_worktree_discipline`)
cwd is `/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/`. All artifact paths and the
"repository root" resolve to the WORKTREE, not `/config/workspace/IronClaude/`. The predecessor + sibling
tasks both hardcode the absolute worktree path in their sync/verify Bash items
(e.g. `cd /config/workspace/IronClaude/.claude/worktrees/reflectWrapper && make verify-sync`,
185553.md:316) — the builder should follow that convention or use relative paths from the worktree root.

### 3.4 Python-side code is normal tracked source (NOT synced)
Per sibling 185553.md:142: the Python package under `src/superclaude/cli/reflect/` and `tests/cli/reflect/` is
normal tracked source — edited directly, no sync needed. ONLY the skill/agent/command/template markdown is
sync-governed. (If THIS track touches only the SKILL.md template, the sync discipline of §3.1–3.2 is the
governing constraint; if it also touches `cli/reflect/` plumbing, that is direct-edit.)

---

## 4. Reversibility / Byte-for-byte Convention (NFR-2 / §5.3 / §6.4 / V15)

Spec anchors (merged-requirements.md, verbatim):
- **NFR-2 (L213–217):** "Default `2`. The §5 map is total and lossless for the two behaviors that exist
  today (ENABLED-wrapper, ENABLED-halt, DISABLED). The … `SKILL.md:1994-1999`'s text **byte-for-byte** so a
  downstream diff of 'old behavior' is [empty]."
- **§5.2 back-compat anchor (L427):** "(absent / `ENABLED`) | `halt` (or absent) | `halt` | §6.4 manual-HALT |
  **Back-compat anchor**: maps to the **retained manual-HALT position** (`reflect_post_mode: halt`), NOT to
  wrapper Mode 2, preserving `SKILL.md:1994-1999` byte-for-byte."
- **§5.3 (L431–446):** the derived `halt` position "emits the **current** `SKILL.md:1994-1999` manual
  fresh-session item verbatim (`reflect_post_mode: halt`)."
- **§6.4 (L580–589):** "This is the **current** `SKILL.md:1994-1999` item, emitted **verbatim**
  (byte-for-byte), with the sole addition of `reflect_post_mode: halt` (or `2-degraded-halt`) in frontmatter.
  … for `2-degraded-halt`, a single `<!-- wrapper-absent: degraded from Mode 2 -->` comment is appended to the
  item Context; the gate text itself is untouched (byte-identical)."
- **§7 depth row (L615):** "`halt` / `2-degraded-halt` | `max(TCS-band, standard)` | the retained manual item
  keeps the **existing** TCS-derived depth (`SKILL.md:1996,2152`)." — i.e. O4 still applies to the manual arm.

**Reversibility proof structure (reusable from sibling-06 L167):** because the dial defaults to `2` AND the
`halt`/`2-degraded-halt` arm reproduces `SKILL.md:1994-1999` verbatim, the *byte-for-byte test* the builder
should encode is: a build resolving to the `halt` position emits a tasklist whose POST item is
character-identical to the current `SKILL.md:1994-1999` text.
**CAUTION (divergence from sibling):** the sibling's reversibility anchor was "default `halt`"; THIS spec's
default is **`2` (wrapper)**, and `halt` is reached only via legacy alias / degradation. So the
byte-for-byte regression test must drive the `halt` position via a *legacy alias input* (or §8 wrapper-absent
degradation), NOT via "field absent" — under THIS spec "field absent" → Mode 2 (wrapper / `2-degraded-halt`),
not the verbatim `/sc:reflect` manual item. This is the single most important reversibility nuance the builder
must get right.

**Suggested "reversible N-edit plan" framing (borrowed from sibling-06's structure, re-scoped to THIS spec):**
the spec describes this as a **Change-#N** set (the spec's own §-by-§ "Change #N" labels). The builder's
template-side edits cluster as:
1. BUILD_REQUEST schema at `SKILL.md:853` — `POST_REFLECT_GATE` block → `REFLECT_POST_MODE: none|0|1|2|auto`
   (§10.2), keeping legacy as alias comments.
2. `--reflect` flag surface + §10.1 precedence + §5 alias map + default `2` (parse-site/plumbing — likely the
   plumbing researcher's seam; template side just consumes the resolved `m`).
3. Frontmatter `reflect_post_mode` field at `SKILL.md:1942` (§10.3), replacing the bare `reflect_post: ""`.
4. Emitted-item SELECTOR at `SKILL.md:1994-1999` — 5-way (none / Mode1 §6.2 / Mode2 §6.3 /
   halt|2-degraded-halt §6.4 verbatim). The §6.4 arm is the byte-for-byte anchor.
5. Enforcement: Rule#19 `SKILL.md:2108` + checklist `SKILL.md:2051` — rephrase the MALFORMED predicate from
   "`POST_REFLECT_GATE is ENABLED`" to the resolved-mode language (item present for `m ∈ {1,2,halt,
   2-degraded-halt}`, ABSENT for `m == none`); accept Bash `superclaude reflect run` (Mode 2) AND inline
   (Mode 1) AND `/sc:reflect` (halt) as valid handoff forms; preserve the `/sc:task` prohibition.
6. (§10.4) advisory-warning emission for fixed `--reflect 1` when `S6==1 ∨ S5>0`.

---

## 5. Survey of Recent SKILL.md-Refactor Task Folders (effective patterns)

### 5.1 `TASK-RF-20260604-042055` — the PREDECESSOR that wired reflect INTO the task-builder skill
Title: "Wire /sc:reflect into the task-builder and sc:tasklist tasklist-generation pipelines". This is the task
that CREATED the current `POST_REFLECT_GATE`/Rule#19/TCS section THIS refactor now mutates. Effective patterns
(structure verified via `grep '^### Phase|^\*\*Step '`):
- **Phase 1 "Preparation, Setup, and Anchor Re-Verification"** with **Step 1.3 "Capture the task-start commit
  + baseline regression-test state"** and **Step 1.4 "Re-verify the load-bearing current anchors still hold
  (drift guard)"** — an L1-discovery drift-guard FIRST, because "the proposals' own cited line numbers are
  stale". **STRONGLY recommended for THIS task** since it edits the exact same anchors (853/1942/1994-1999/
  2051/2108/2114-2152) — capture `start_commit` early (also needed as the reversibility-diff base).
- **One Step per SEAM** (Steps 2.1–2.14): `--spec` surface, A.2 parse, PRE-gate section, BUILD_REQUEST
  `POST_REFLECT_GATE` field, Rule#19, frontmatter keys, the penultimate POST item, validation checklist,
  the TCS section, an **S4-trim verification item that asserts the literal final token set** (2.13). This
  granular per-seam decomposition is exactly Template-02 A3/A4.
- **Per-phase SoT sync pair**: every source-edit phase ends with a `make sync-dev` item (Step 2.14) + a
  `make verify-sync` **AND markdownlint** item (Step 2.15). The markdownlint item embeds the no-pivot rule
  ("do NOT add `<!-- markdownlint-disable -->` or run `--fix`/sed").
- **QA gating FINAL_ONLY** (042055.md:138): "one final validation phase, no per-phase rf-qa spawns;
  REGRESSION-ONLY testing (no new tests authored)". A valid lighter-weight gate posture when edits are purely
  additive markdown — contrast with the sibling (185553) which uses per-phase rf-qa gates because it ships new
  Python. THIS task's posture depends on whether it ships Python plumbing (per-phase gates) or is template-only
  (FINAL_ONLY may suffice) — the builder decides from scope.
- **"strictly additive, preserve byte-exact wire-strings"** discipline (042055.md:75) is the same byte-for-byte
  posture §4 demands here.

### 5.2 `TASK-RF-20260608-185553` — the SIBLING (the wrapper CLI task)
Structure (verified): Phase 1 prep (1.3 build a consolidated implementation-reference discovery handoff) →
Phases 2–4 build the `cli/reflect/` package → **Phase-Gate PG-2 / PG-4 rf-qa task-integrity gates** →
**Phase 5 "Task-Builder Skill Template Branch (POST_REFLECT_MODE) + Sync"** (Steps 5.1–5.5, the template seam)
→ Phase 6 tests → Phase 7 validation gates → **PG-7 final rf-qa + rf-qa-qualitative**. Reusable patterns:
- The **Phase-5 5-step decomposition** (schema-field edit → optional-signals doc → item branch → Rule#19+
  checklist broaden → sync+verify) is the right shape for THIS track's template phase — **but rename/rescope
  per §2.2** (`REFLECT_POST_MODE` 5-way, not `POST_REFLECT_MODE` binary).
- **PG-2/PG-4/PG-7 rf-qa gate placement** (after each build phase + a final structural + qualitative pair) is
  the Template-02 I15/M1 pattern done well.
- Its **Step 5.5 sync item** (185553.md:272) is a model SoT item: runs `make sync-dev` + `make verify-sync`,
  captures to `phase-outputs/test-results/phase5-sync.txt`, embeds "Do NOT `git add` any `.claude/` path",
  embeds the no-pivot recovery ("do NOT pivot to a manual copy").
- Its **no-nesting-guard test** (185553.md:300) reads the `src/` SOURCE copy (not `.claude/`), asserts the
  Mode-2 branch contains `superclaude reflect run` and contains NONE of `Task(`/`subagent_type`/`Agent tool`
  (NFR-7). Directly reusable; coordinate with researcher-06 (test surface).

**Net recommendation to the builder:** model the template phase on the sibling's Phase-5 *shape* + the
predecessor's *per-seam granularity + drift-guard + per-phase sync/lint discipline*, but implement the spec's
`REFLECT_POST_MODE`/`--reflect` 5-way dial — explicitly NOT the sibling's `POST_REFLECT_MODE: wrapper|halt`
binary field (which THIS spec retires).

---

## Summary

**Template 02 rules (the builder must obey):** B2 six-element self-contained items written as ONE paragraph
(B3); A3/A4 granular per-file/per-seam breakdown; flat checkboxes, components-first-summary-last (E1–E3);
F1 loop + F2a one-item discipline (+ parallel-spawn exception L430); I15/M1 phase-gate QA; I17 post-completion
validation (all `[x]`, output files exist, tests pass) BEFORE frontmatter→Done; I18 + L3 testing item for
code-modifying tasks; L1–L6 handoff seam vocabulary; PART-2 body section order with NO items before Phase 1
(D3). Frontmatter schema per template L1–44 (`type: 🔧 Refactor`, `task_type: static`).

**Cross-validation verdict (the headline):** the sibling's SKILL.md ANCHOR FACTS are all **[CODE-VERIFIED]**
against the current 2308-line `SKILL.md` (1992-2006 HALT item, 853-856 BUILD_REQUEST block, 1942 sentinel,
2051 checklist, 2108 Rule#19, 2114/2152 TCS+O4, DEPTH baked). But the sibling's SCHEMA DESIGN —
`POST_REFLECT_MODE: wrapper|halt` as a LIVE BUILD_REQUEST field (sibling-06 "Minimal reversible edit" item 1
+ sibling task Phase-5 Steps 5.1–5.4) — is **[CODE-CONTRADICTED by spec §10.1/§10.2/§5.3]**: THIS spec
**retires `POST_REFLECT_MODE`** to a deprecated read-only alias and replaces it with the new primary field
**`REFLECT_POST_MODE: none|0|1|2|auto`** (default `2`) + CLI flag **`--reflect`** + frontmatter
**`reflect_post_mode`**. The builder MUST NOT base items on the sibling's binary `wrapper|halt` field; it must
build the 5-way dial (none/1/2/halt/2-degraded-halt + auto-resolution + §10.4 advisory). Items for Mode `none`,
`auto` resolution, §8 degradation, and the advisory warning are **[UNVERIFIED in sibling-06]** → source from
spec §4/§6/§8/§10.4 (owned by researchers 01–04).

**SoT/reversibility (verbatim-quoted):** edit `src/superclaude/skills/task-builder/SKILL.md` only →
`make sync-dev` (Makefile:109) → `make verify-sync` (Makefile:166, exits 1 on drift) → NEVER `git add`
`.claude/*` (except `settings.json`); markdownlint via `uv run pre-commit run markdownlint --files <file>`
(MD040, no `--fix`/disable-comment pivot). Reversibility (NFR-2/§5.3/§6.4): the `halt`/`2-degraded-halt` arm
emits `SKILL.md:1994-1999` **byte-for-byte** — BUT (key nuance) under THIS spec the byte-identical manual item
is reached via a **legacy alias / §8 degradation**, NOT via "field absent" (absent → Mode 2). Capture
`start_commit` in Phase 1 (drift-guard + diff base), borrow the predecessor's per-seam granularity + per-phase
sync/lint pair + anchor-re-verification step, and the sibling's Phase-5 shape + PG rf-qa gates + no-nesting
guard test.

**Staleness tag tally:** [CODE-VERIFIED] = 10 SKILL.md anchors (all sibling anchor facts confirmed current) +
Makefile targets + CLAUDE.md SoT rule. [CODE-CONTRADICTED by spec] = 1 major (the sibling's
`POST_REFLECT_MODE`-as-live-field schema design, contradicted by §10.1/§10.2/§5.3). [UNVERIFIED in sibling] = 4
(Mode `none`, `auto` resolution §4, §8 wrapper-probe degradation, §10.4 advisory — none covered by sibling-06,
must source from spec).

**Status: Complete**
