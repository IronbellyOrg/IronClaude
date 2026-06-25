# Research Notes: Implement reflect-in-task-builder.md + reflect-in-sc-tasklist.md against src/superclaude/ (with S4 token-set trim), then make sync-dev

**Date:** 2026-06-04
**Scenario:** A (Explicit — two detailed proposals with Implementer Checklists + cited deltas)
**Depth Tier:** Deep
**Track Count:** 1 (single track — two disjoint-file proposals + one shared `make sync-dev`; user asked for "a task file" singular)

---

## EXISTING_FILES

**Proposal 1 target — `src/superclaude/skills/task-builder/SKILL.md`** (2190 lines, single-file skill, no refs/rules/templates subdirs).
Deltas required (from reflect-in-task-builder.md §8):
- Add `--spec` to Input/flags surface.
- A.2: spec_path resolution (priority: `--spec` → `@file` in GOAL → `SPEC:`/`PRD:`/`TDD:` in BUILD_REQUEST → none).
- New **A.10.7 PRE reflect gate** between A.10.5 and A.11 + pipeline-overview bullet (current steps 12/13).
- A.9 BUILD_REQUEST: add `POST_REFLECT_GATE` block (after `EXECUTION_CONTEXT_REQUIREMENTS`) + new Critical Rule (companion to #16/#17/#18).
- Output Structure: add `reflect_pre`/`reflect_post`/`spec_path` frontmatter + penultimate reflect item in the `Phase N` example.
- Task File Validation Checklist: add "POST reflect item present + positioned when enabled" (MALFORMED guard).
- A.11: `REFLECT GATES` block (+ multi-track per-track row).
- New `## Reflect Depth (Deterministic TCS)` section: TCS formula `3·S1+4·S2+2·S3+2·S4+5·S5+4·S6`, frozen extraction rules, threshold table (≤12 quick / 13-34 standard / ≥35 deep), overrides O1-O4.
- **S4 TOKEN-SET TRIM (in-scope cleanup, user-mandated):** S4 dependency-token set in the proposal is `{after Phase \d+, blockedBy:, depends on N\.\d+, after N\.\d+}`. TRIM to **drop `blockedBy:` and `after N\.\d+`, KEEP `after Phase \d+` and `depends_on:`** → final S4 set = `{after Phase \d+, depends_on:}`. (Rationale: blockedBy:/after N.N are not real emitted patterns, mirroring the proposal's own S7/multifile drops.) Note `depends_on:` (underscore) replaces the proposal's prose `depends on N.\d+`.

**Proposal 2 targets:**
- **`src/superclaude/skills/sc-tasklist-protocol/SKILL.md`** (1491 lines; has rules/ + templates/ subdirs).
  Deltas (from reflect-in-sc-tasklist.md §6): new **Stage 10.5** pre-reflect fan-out (after Stage 10); **Stage 5** templated POST task; amend **checkpoint-is-last invariant set together** (Self-Check #6, structural check #18, gate #19, gate #20); deterministic per-phase `COMPLEXITY_SCORE = 3·n_strict + 3·n_cpo + 2·n_high_risk + ceil(n_tasks/5) + ceil(n_R/5)` + threshold table (0-3 quick/T1, 4-9 standard/auto, ≥10 deep/T2) + hard overrides (n_cpo≥1 OR n_strict≥2 → deep/T2; n_tasks==0 → skip); 10-stage table → 11; new `depth-map.yaml` + `reflect-pre/`/`reflect-post/` under `TASKLIST_ROOT/validation/`.
- **`src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md`** + **`index-template.md`** — likely need the POST-task template + the Pre-Reflect Sign-off index column.
- **`src/superclaude/commands/tasklist.md`** (118 lines) — add `--no-reflect` escape hatch to Arguments table + argument-hint.

**Shared finalization:** `make sync-dev` (then `make verify-sync` per SoT discipline).

**Reflect surface (read-only reference, NO edits):** `src/superclaude/commands/reflect.md` + `src/superclaude/skills/sc-reflect-protocol/{SKILL.md,refs/*}`. Proposals use only reflect's EXISTING flags (`--mode pre/post`, `--spec`, `--tasklist`, `--depth`, `--tier`, `--diff`, `--executor-model`, `--remediate`, `--budget-remaining`, `--output`). **No reflect-side changes.**

**MDTM templates (for the BUILDER to read, not edit):** `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (+ 01). NOTE: skill text references `.claude/templates/workflow/...` (synced copy) — both paths exist post-sync.

## PATTERNS_AND_CONVENTIONS

- **SoT discipline (ABSOLUTE):** edit `src/superclaude/` ONLY → `make sync-dev` → `.claude/` is regenerated. NEVER stage/edit `.claude/{skills,commands,agents}`. `make verify-sync` must pass. (CLAUDE.md ABSOLUTE RULEs.)
- **markdownlint** (`.markdownlint.json` at repo root) applies to edited `.md` — edits must not introduce lint violations. PreToolUse/markdownlint hooks enforce; never pivot to escape (memory `feedback_no_strategy_pivot_to_avoid_hooks`).
- These are **markdown protocol files** (SKILL.md, command .md), not Python — "implementation" = precise additive markdown edits matching existing stage/rule/section structure.
- task-builder Critical Rules #16/#17/#18 establish the "BUILD_REQUEST field drives generated MDTM items; omission = MALFORMED" pattern the POST gate reuses — new rule is a companion.
- Both proposals: gates are **advisory-blocking / audit-first**, never auto-mutate (honor `feedback_human_decision_items_must_halt`); POST is a **fresh-session handoff**, never inline (honor `feedback_sc_reflect_vs_inline_rfqa`); execution uses `/task`, gate uses `/sc:reflect` — **never `/sc:task`** (honor `feedback-no-sctask-on-task-builder-tasklists`).

## GAPS_AND_QUESTIONS

1. **Line-anchor drift** — every `SKILL.md:NNNN` citation in both proposals must be re-verified against CURRENT files; line numbers WILL have drifted. (R1, R2, R3.)
2. **Test breakage risk (HIGH)** — `tests/audit/test_*` (DNSP, TB-Add-8, INV-002/010/019, monotonicity/regression halts, NFR-CONV-6..10) reference task-builder SKILL.md; `tests/sprint/test_checkpoints.py` + `tests/audit/test_checkpoint.py` reference checkpoint behavior that proposal-2's checkpoint-is-last amendment touches. MUST determine: do these tests parse/grep the SKILL.md text (break on edits) or are they pure-Python fixtures? What is the exact run command + must-pass set? (R4 — load-bearing.)
3. **S4 trim exact wording** — confirm the final S4 token set + that no existing S4 anchor needs editing (S4 is NEW content in the new TCS section). (R1.)
4. **commands/tasklist.md `--spec` already exists?** Proposal says `--spec` is already a flag; `--no-reflect` is the only new flag. Confirm. (R3.)
5. **phase-template.md / index-template.md** — exact insertion points for POST task + sign-off column. (R3.)
6. **Markdownlint config specifics** — which rules (line length? fenced-code? heading levels?) could the dense new sections trip. (R5.)

## RECOMMENDED_OUTPUTS

Research files in `research/`:
- `01-taskbuilder-skill-anchors.md` (R1)
- `02-tasklist-skill-anchors.md` (R2)
- `03-tasklist-command-and-templates.md` (R3)
- `04-test-verification-impact.md` (R4)
- `05-patterns-conventions-sync-reflect.md` (R5)
- `06-mdtm-template-and-examples.md` (R6)

## SUGGESTED_PHASES (researcher assignments)

- **R1 (Integration/Anchors):** task-builder/SKILL.md — verify ALL §8 anchors, locate current line ranges for every delta site (Input/flags, A.2, A.10.5 end, A.11, A.9 BUILD_REQUEST, Output Structure Phase-N example + frontmatter, Validation Checklist, Critical Rules #16-18, pipeline-overview steps 12/13). Confirm S4 trim is new-content-only. Output `01-...`.
- **R2 (Integration/Anchors):** sc-tasklist-protocol/SKILL.md — verify Stage 10 end, Stage 5 emission site, the 4 checkpoint invariants (Self-Check #6, structural check #18, gate #19, gate #20), 10-stage table, signal sources (tier distribution, traceability R-###, CPO, risk, n_tasks), Stage 7 fan-out primitive, `validation/` dir convention. Output `02-...`.
- **R3 (File Inventory):** commands/tasklist.md (Arguments table, `--spec` presence, argument-hint, Skill invocation, where `--no-reflect` lands) + tasklist templates/{phase-template,index-template}.md structure. Output `03-...`.
- **R4 (Test & Verification — CRITICAL):** enumerate exactly which tests load/parse task-builder vs tasklist SKILL.md text; classify break-risk; determine the must-pass verification commands (sync-dev, verify-sync, pytest subsets, markdownlint, ruff-format if any .py). Output `04-...`.
- **R5 (Patterns & Conventions):** SKILL.md stage/rule structure conventions; Rule #16 QA-gate-emission machinery; markdownlint.json rules; SoT sync workflow; reflect.md flag surface confirmation (every flag the templated commands use). Output `05-...`.
- **R6 (Template & Examples):** MDTM template 02 PART 1 (rules A3/A4/B2, L1-L6 handoff) + 2-3 real TASK-RF tasklists (incl. TASK-RF-20260602-135209) for multi-phase markdown-editing patterns. Output `06-...`.

## TEMPLATE_NOTES

- **MDTM template: 02 (Complex)** — multi-phase (discovery/verify-anchors → edit proposal-1 → edit proposal-2 → S4-trim cleanup → sync → test/verify → reflect gates), conditional flows, QA gates.
- **Tier: Deep** — 4 target files + large blast-radius test suite + two dense proposals.
- Generated MDTM should: be granular (one item per delta-site, not "implement proposal 1"); include explicit `make sync-dev` + `make verify-sync` + targeted `uv run pytest tests/audit/ tests/sprint/...` validation items AFTER each edit phase; include markdownlint validation; encode the PRE + POST reflect gates per the skill's own POST_REFLECT_GATE machinery (dogfooding — this build's own tasklist should carry the reflect POST item).
- **Self-referential note:** the task-builder proposal modifies the very skill (task-builder) that built this tasklist. Edits must be additive and not break the in-flight skill semantics; verification via the audit test suite is the guardrail.

## AMBIGUITIES_FOR_USER

- **Single vs multi-track:** chosen single-track (disjoint files but shared `make sync-dev` + singular "a task file" request). If the user prefers two independently-executable task files, that is the only reasonable alternative — but the shared sync/verify finalization argues for one cohesive file. Proceeding single-track.
- **S4 `depends_on:` token:** user wrote "keep ... `depends_on:`"; the proposal's prose token was `depends on N.\d+` (spaces). Interpreting the kept token as the literal `depends_on:` (underscore, colon) per the user's exact wording. Final S4 set = `{after Phase \d+, depends_on:}`. Flagged for builder to encode literally.
