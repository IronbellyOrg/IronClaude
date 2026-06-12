# R1: O1 Whole-Tasklist Terminal POST Gate — task-builder SKILL.md Edit Surface

Status: In Progress

Target file: `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/task-builder/SKILL.md`
Contract: `/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md`

## Contract anchors (R1-relevant)

From `reflect-wrapper-contract.md`:
- **§2 O1 invocation (FLAT, fixed deep):** `superclaude reflect run <ABS_TASKLIST_PATH> --depth deep --fix --promote`. `--base` OMITTED → wrapper resolves base from frontmatter `start_commit`. `--depth deep` is HARDCODED (O1 is fixed Tier-2 deep).
- **§3 recursion breaker:** wrap with `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard; `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "...nested gate suppressed"; exit 0; fi` then the `superclaude reflect run` line.
- **§6 frontmatter:** generators MUST persist `start_commit` (git SHA, O1 base) and `executor_model_class` (model-class alias). `reflect_post:` is written BACK by the wrapper — generators must LEAVE ROOM (do not hand-author/lock).
- **Exit codes:** only 0 completes the gate; 10/11/2 FAIL.
- **MUST NOT emit:** `--reflect` dial, `--max-turns`, `<base>..HEAD` range, `/sc:reflect --mode post` self-run subagent form.

---

## SURFACE 1 — POST reflect checklist item template `N.{X-1}` (self-run subagent)

**Current location:** lines 2193-2198 (item body) within the final-phase template block. The whole MDTM template fence runs from ~line 2136 to line 2219 (closing ```` ``` ````). The item sits between the `## Phase N: [Final Phase ...]` header (line 2191) and the `N.X — Update task status to Done` item (lines 2200-2205).

**VERBATIM current block (lines 2193-2198):**

```markdown
- [ ] **N.{X-1} -- Independent post-execution reflection gate (run via subagent)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per project memory `feedback_sc_reflect_vs_inline_rfqa`, an independent `/sc:reflect --mode post` ensemble catches spec-literal-token, invariant-arithmetic, and integration/orphan blindspots that same-frame QA misses.
  - **Action**: Spawn a subagent that runs `/sc:reflect --mode post --remediate --diff <BASE> --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}` -- where `<BASE>` is the branch's fork point from its integration branch, computed as `git merge-base HEAD <integration-branch>`, where `<integration-branch>` defaults to the repo's ACTUAL default branch -- resolve it with `git symbolic-ref --short refs/remotes/origin/HEAD` (yields e.g. `origin/main` or `origin/master`), falling back to whichever of `origin/master`/`origin/main` exists if that symbolic ref is unset. Do NOT hardcode `origin/master`: when the project integrates onto a DIFFERENTLY-named branch (e.g. `integration`), pass it explicitly rather than relying on the default. Pass `<BASE>` as a SINGLE ref (NOT `<BASE>..HEAD`) so reflect diffs it against the current **working tree** -- this captures the task's changes whether committed, staged, or left as unstaged edits to tracked files. **Caveat -- brand-new untracked files are NOT captured:** `git diff <BASE>` omits files that have never been `git add`-ed, and reflect performs no separate untracked-file enumeration, so newly-created task artifacts escape the audit. Run `git add -A` (or otherwise stage new files) BEFORE this gate so the working-tree diff includes them. **Do NOT use `start_commit..HEAD`:** `start_commit` (the HEAD captured at task start) silently becomes a WRONG base in two common cases -- (a) the work is left **uncommitted** (the usual `/task` outcome: it edits the working tree but does not commit, so a `..HEAD` range audits none of the task's changes), and (b) an **unrelated commit interleaves** on the branch after task start (so `start_commit..HEAD` spans foreign work). `start_commit` is retained in frontmatter for provenance only, never as the diff base. `{DEPTH}` is floored at `standard` per O4 (the POST gate NEVER runs `--depth quick`), and `{EXECUTOR_CLASS}` is this executor's model class so reflect excludes it from its audit panel. Running reflect inside a subagent supplies the clean, executor-disjoint context that prevents self-rubber-stamping, so NO separate human session is needed. The gate command uses `/sc:reflect` and never `/sc:task`; any re-execution uses `/task`.
  - **Output**: The reflect subagent returns; record its `{verdict, run_id, report}` to this file's frontmatter `reflect_post`. If reflect surfaces deviations, apply the remediations or append them to `### Open Questions` (never delete existing items).
  - **Verification**: `reflect_post` in frontmatter holds the subagent's `{verdict, run_id, report}` (not empty), and any flagged deviations were remediated or logged to Open Questions.
  - **Completion gate**: The reflect subagent has returned and its verdict is recorded in `reflect_post`. THEN the Update-status-to-Done item proceeds.
```

**What must change for O1 (PRIMARY EDIT):** Replace this entire 6-field self-run-subagent item with a FLAT Bash shell-out item. The new Action must drop the subagent spawn, the `<BASE>` `git merge-base`/`symbolic-ref` resolution, the `--diff`/`--tasklist`/`--spec`/`--depth {DEPTH}`/`--executor-model` flag string, and the `/sc:reflect --mode post` command. It becomes:
- A skip-guard prelude: `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi`
- Then: `superclaude reflect run <ABS_TASKLIST> --depth deep --fix --promote` (`<ABS_TASKLIST>` = `{TASK_FILE}` resolved to absolute; `--depth deep` HARDCODED — no `{DEPTH}` threading; no `--base` — wrapper reads frontmatter `start_commit`).
- Output/Verification/Completion-gate must shift from "record `{verdict,run_id,report}` to `reflect_post`" (the wrapper now WRITES `reflect_post` back itself, §6) to "consume the EXIT CODE: only exit 0 lets Update-status-to-Done proceed; 10/11/2 FAIL and surface" (contract §2 exit table). The `git add -A` staging note is still useful (untracked files) but the base-resolution prose is now wrapper-owned and must be removed.
- NOTE re anti-orphaning: it stays penultimate (immediately before `N.X — Update task status to Done`), unchanged.

---

## SURFACE 2 — Critical Rule 20 (POST reflect gate)

**Current location:** line 2312 (single paragraph). Header `## Critical Rules (Non-Negotiable)` is at line 2272.

**VERBATIM (line 2312):**

```text
20. **POST reflect gate in generated task files.** When the BUILD_REQUEST specifies `POST_REFLECT_GATE: ENABLED`, the builder MUST emit, as the penultimate item of the final phase (immediately before the `Update task status to Done` item, preserving anti-orphaning per the validation checklist), a SELF-RUN reflect item. The item instructs the executor to spawn a subagent that runs `/sc:reflect --mode post` with the resolved args, then record reflect's `{verdict, run_id, report}` to the `reflect_post` frontmatter and remediate or log any deviations before proceeding to Update-status-to-Done. Running reflect in a subagent supplies the executor-disjoint context, so the item MUST NOT halt for a human or defer to a separate session. The gate command uses `/sc:reflect`, and `/task` (never `/sc:task`) for any re-execution. A generated task file that omits the POST reflect item when `POST_REFLECT_GATE: ENABLED`, or that emits a human-handoff/HALT form instead of the self-run form, is a MALFORMED output.
```

**What must change for O1:** "a SELF-RUN reflect item ... spawn a subagent that runs `/sc:reflect --mode post` with the resolved args, then record reflect's `{verdict, run_id, report}` to the `reflect_post` frontmatter" → "a FLAT Bash shell-out item that runs `superclaude reflect run <ABS_TASKLIST> --depth deep --fix --promote`, wrapped in the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard, consuming the exit code (only 0 proceeds)". Drop "record `{verdict,run_id,report}` to `reflect_post`" (wrapper writes `reflect_post` back). The MALFORMED clause stays but its trigger flips: MALFORMED if the item is the OLD `/sc:reflect --mode post` subagent form, or emits `--reflect`/`<base>..HEAD`, or is missing the skip guard. Keep "MUST NOT halt for a human" (the wrapper HALTs internally via exit 10; the gate item itself is non-interactive) and keep `/task` (never `/sc:task`) for re-execution.

---

## SURFACE 3 — A.9 BUILD_REQUEST `POST_REFLECT_GATE: ENABLED` block

**Current location:** lines 1073-1076 (inside the A.9 BUILD-REQUEST template).

**VERBATIM (lines 1073-1076):**

```text
    POST_REFLECT_GATE: ENABLED
      SPEC_PATH: <spec_path or NONE>
      DEPTH: <max(tcs-derived depth, standard)>   # POST floor per O4, never quick
      TASK_FILE: ${TASK_FILE}
```

**What must change for O1:** `SPEC_PATH` and `DEPTH` placeholders become POST-gate-IRRELEVANT — the wrapper does not take `--spec` or a TCS-derived `--depth` at O1 (`--depth deep` is fixed; spec comes from frontmatter/contract, not a CLI flag here). Per contract §2/§6, the POST gate needs only the ABS tasklist path + frontmatter (`start_commit`, `executor_model_class`). The block should be reduced to (at minimum) `POST_REFLECT_GATE: ENABLED` + `TASK_FILE: ${TASK_FILE}`, and surface the need for `start_commit`/`executor_model_class` frontmatter. `SPEC_PATH` is still consumed by the PRE gate (A.10.7) — but PRE reads it via A.2 `spec_path:` resolution, not via this POST block (see Surface 8 / SPEC_PATH §282). `DEPTH: <max(tcs..., standard)>` and the O4 floor comment are now dead for POST (deep is hardcoded); remove from this POST block.

---

## SURFACE 4 — Output-Structure / validation-checklist "SELF-RUN ... penultimate ... not human-handoff" line

**Current location:** line 2253 (validation checklist under "Task File Content Rules" region; the checklist starts above line 2240).

**VERBATIM (line 2253):**

```text
- [ ] POST reflect item present and positioned penultimate (immediately before Update-status-to-Done) when POST_REFLECT_GATE is ENABLED; the item must be the SELF-RUN form (spawns a reflect subagent and records the verdict), NOT a human-handoff/HALT. MALFORMED if omitted or if it halts for a human.
```

**What must change for O1:** "the item must be the SELF-RUN form (spawns a reflect subagent and records the verdict)" → "the item must be the FLAT `superclaude reflect run ... --depth deep --fix --promote` shell-out wrapped in the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard (NOT a `/sc:reflect --mode post` subagent, NOT a human-handoff/HALT)". Keep penultimate-positioning + "MALFORMED if omitted". Optionally add a check that it consumes the exit code (only 0 proceeds) and emits no `--reflect`/`<base>..HEAD`.

---

## SURFACE 5 — A.11 present-results POST gate line

**Current location:** line 2724 region — specifically the REFLECT GATES sub-block of the result banner, lines 1722-1724.

**VERBATIM (lines 1722-1724):**

```text
REFLECT GATES:
  PRE  (--mode pre):  [PASS coverage=0.94 depth=standard tcs=22] | [FAIL coverage=0.71 see Open Questions] | [SKIPPED no-spec]
  POST (--mode post): emitted as final-phase item N.{X-1} (the executor runs /sc:reflect via a subagent at the end of the run)
```

**What must change for O1:** The POST line must drop `(--mode post)` and "the executor runs /sc:reflect via a subagent". New shape e.g.: `POST (terminal gate): emitted as final-phase item N.{X-1} -- runs 'superclaude reflect run <tasklist> --depth deep --fix --promote' (recursion-guarded) at the end of the run`. The PRE line (1723) stays INTACT.

---

## SURFACE 6 — `## Reflect Depth (Deterministic TCS)` section + O4 floor (TCS plumbing: PRE vs POST)

**Section location:** lines 2318-2358. Header at 2318. Formula at 2338. Threshold table 2345-2349. Hard overrides 2353-2356.

**Where `{DEPTH}` is threaded into the POST item:** ONLY in the Surface-1 Action string (line 2195: `--depth {DEPTH}`) and described in the prose `{DEPTH}` is floored at `standard` per O4. The A.9 POST block `DEPTH: <max(tcs-derived depth, standard)>` (line 1075) computes the value that fills `{DEPTH}`.

**O4 verbatim (line 2356):**

```text
- **O4: POST-gate depth floor (HARD RULE, no exceptions):** the POST gate depth is one of {`standard`, `deep`}: it may **NEVER** be `quick`. `--depth quick` disables reflect's regression-escalation rubric, and the POST gate audits executed code, which is exactly where that escalation matters most. When the band yields `quick`, the POST command is emitted with `--depth standard` (the PRE call may still use `quick`, since no diff exists pre-execution).
```

**Section intro verbatim (line 2320, first sentence):**

```text
The PRE reflect gate (A.10.7) and the templated POST item both derive reflect's `--depth` from a **Tasklist Complexity Score (TCS)**: ...
```

**Contract confirmation + what changes:** Contract §2 states O1 is FIXED `--depth deep` (forces Tier-2 fan-out). Therefore the POST gate is NO LONGER TCS-derived for depth — the entire TCS→`--depth` plumbing becomes **POST-gate-IRRELEVANT** for O1. Specifically now POST-irrelevant:
- O4 (line 2356) — the standard-floor-for-POST rule is moot once POST is hardcoded deep; either delete O4 or restrict it to "PRE only" (PRE still allows quick).
- The line-2320 intro must stop claiming "the templated POST item ... derive[s] reflect's `--depth` from TCS"; it should say only the PRE gate (A.10.7) derives `--depth` from TCS.
- A.9 POST block `DEPTH:` (line 1075) and `{DEPTH}` in the POST Action (Surface 1) — removed.

**What STAYS for PRE (do NOT touch):** The whole TCS apparatus (S1-S6 signals 2324-2331, formula 2338, threshold table 2345-2349, overrides O1/O2/O3 lines 2353-2355, boundary inference 2358) remains live for the PRE gate, which still emits `--depth <pre_depth>` (line 1662, `quick` permitted at PRE). The contract only fixes O1 depth; the A.10.7 PRE gate (Surface 8 / lines 1654, 1662) is explicitly OUT OF SCOPE per the task framing ("PRE gate stays INTACT").

---

## SURFACE 7 — Frontmatter the builder writes for generated tasklists

**Current location:** lines 2136-2156 (the generated-MDTM frontmatter template, inside the ```` ```markdown ```` fence opened at 2136).

**VERBATIM (lines 2137-2156):**

```markdown
---
id: "TASK-RF-<subject>-YYYYMMDD-HHMMSS"
title: "[Task Title]"
description: "[Brief description of what the task accomplishes]"
status: "🟡 To Do"
type: "🔧 Refactor"  # or 📝 Documentation, ✨ Feature, etc.
priority: "🔼 High"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "orchestrator"
template_schema_doc: ".claude/templates/workflow/0[1|2]_mdtm_template_[generic|complex]_task.md"
estimation: "[estimated duration]"
task_type: static
related_docs:
- path: "[relevant file]"
  description: "[why it's relevant]"
tags:
- "[tag1]"
- "[tag2]"
---
```

**What must change / ADD for O1 (per contract §6):** This frontmatter currently declares NONE of the three O1 keys. The builder must ADD:
- `start_commit: "<git SHA captured at task-build/emit time>"` — the whole-task `--diff` base the wrapper reads when `--base` is omitted (§6 row 1). (Captured via `git rev-parse HEAD` at build time.)
- `executor_model_class: "<model-class alias, e.g. sonnet>"` — reflect `--executor-model` for anti-self-confirmation (§6 row 3).
- `reflect_post:` — leave UNPOPULATED/room (the WRAPPER writes it back; §6 note: "do not hand-author or lock it"). Currently the PRE gate writes `reflect_pre:` to frontmatter (lines 1674-1685) but there is NO `reflect_post:` declared anywhere in the template — it is only referenced in the (to-be-replaced) Surface-1 item Output. After the rewrite, `reflect_post` should NOT be hand-authored by the gate item; the wrapper owns it.
- Also relevant: `spec_path:` is documented (A.2 §41, §282) as written to generated frontmatter but is also ABSENT from this visible template block — it feeds the PRE gate, not O1.

---

## SURFACE 8 — All other occurrences (grep sweep, line + 1-line context)

`/sc:reflect --mode post`:
- L2194 — POST item Context (memory rationale). REWRITE/REMOVE (replaced by Surface 1).
- L2195 — POST item Action command string. REWRITE (Surface 1, primary).
- L2312 — Critical Rule 20. REWRITE (Surface 2).
- L41 — A.2 `--spec` flag doc: "baked into the templated POST reflect item's command". Update prose (POST no longer takes `--spec`/`--mode post`; spec is PRE-only now).
- L282 — SPEC_PATH glossary: "threaded into ... the POST item's `{SPEC_PATH}` placeholder". Update (POST drops SPEC_PATH/{SPEC_PATH}).

`reflect_post`:
- L2196 — POST item Output (record verdict). REMOVE (wrapper writes back).
- L2197 — POST item Verification. REMOVE/REWRITE (now: exit code consumed, not frontmatter check).
- L2198 — POST item Completion gate. REWRITE (exit 0 → proceed).
- L2312 — Rule 20 (same as Surface 2).
- (Must ADD `reflect_post:` ROOM to frontmatter template — Surface 7.)

`POST_REFLECT_GATE`:
- L1073 — A.9 BUILD_REQUEST block header. REWRITE (Surface 3).
- L1666 — A.10.7 PRE-gate note: "it is a POST-only concern, see A.9 `POST_REFLECT_GATE`". Cross-ref stays valid (still POST-only) but check wording after Surface-3 edit.
- L2253 — validation checklist (Surface 4).
- L2312 — Rule 20 (Surface 2).

`superclaude reflect run`: **ZERO occurrences** — confirmed not yet present anywhere in the file. Must be INTRODUCED at Surface 1 (and referenced in Surfaces 2, 4, 5).

`start_commit`:
- L2195 only — inside POST Action prose ("`start_commit` is retained in frontmatter for provenance only, never as the diff base"). Currently NOT in the frontmatter template (Surface 7 must add it). Under O1 the wrapper USES `start_commit` as the base (§6 row 1) — so the "never as the diff base" prose is REVERSED for the wrapper path and must be removed/rewritten.

`executor_model_class`: **ZERO occurrences.** The CONCEPT exists only as `{EXECUTOR_CLASS}`/`--executor-model` (L2195) and `EXECUTOR_CLASS` is NOT even in the A.9 block (the grep for `EXECUTOR_CLASS` hit only L2195's `{EXECUTOR_CLASS}`). Must ADD `executor_model_class:` to frontmatter (Surface 7).

`SUPERCLAUDE_REFLECT_WRAPPER` / skip guard: **ZERO occurrences.** Must be INTRODUCED at Surface 1 (and asserted in Surfaces 2, 4).

`--mode pre` (PRE gate — DO NOT TOUCH, scope-fenced as INTACT):
- L41, L1654, L1659/1662 (A.10.7 spawn), L1666, L1723 (banner PRE line), L1677-1685 (`reflect_pre:` frontmatter). All PRE — leave intact except where Surface-6 prose wrongly couples POST to TCS.

---

## Summary of edit sites (line refs as of this read)

| # | Surface | Lines | Action |
|---|---------|-------|--------|
| 1 | POST item template N.{X-1} | 2193-2198 | REPLACE with flat `superclaude reflect run ... --depth deep --fix --promote` + skip guard; exit-code completion gate |
| 2 | Critical Rule 20 | 2312 | REWRITE: flat shell-out + skip guard; flip MALFORMED triggers |
| 3 | A.9 POST_REFLECT_GATE block | 1073-1076 | REDUCE to ENABLED + TASK_FILE; drop SPEC_PATH/DEPTH (POST-irrelevant) |
| 4 | Validation checklist line | 2253 | REWRITE "SELF-RUN form" → flat shell-out + skip-guard form |
| 5 | A.11 banner POST line | 1724 | REWRITE: drop `--mode post`/subagent; describe shell-out |
| 6 | Reflect Depth / O4 | 2320, 2356 | Decouple POST from TCS depth (deep hardcoded); O4 → PRE-only or delete; PRE TCS stays |
| 7 | Generated frontmatter template | 2137-2156 | ADD `start_commit`, `executor_model_class`; leave room for wrapper-written `reflect_post` |
| 8 | Cross-refs (prose) | 41, 282, 1666, 2194-2198 | Update prose; remove `start_commit` "never as diff base" reversal |

Status: Complete
