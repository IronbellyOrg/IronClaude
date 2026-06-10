# Research Notes: task-builder `--reflect auto|1|2` — 3-mode POST reflect gate dial

**Date:** 2026-06-08
**Scenario:** A (Explicit — fully merged requirements spec with 13 FRs, 8 NFRs, §4 auto-FER, §5 knob map, §6 per-mode templates, §7 depth reconciliation, §8 fallback ladder, §9 V1–V16 validation matrix, §10 plumbing, §13 acceptance-test matrix)
**Depth Tier:** Deep
**Track Count:** 1 (single cohesive refactor — the dial, per-mode templates, auto predicate, knob reconciliation, depth/TCS reconciliation, and validation rewrites are tightly interdependent; not independent work streams)
**Source spec:** `.dev/brainstorms/20260608-191030-reflect-flag-post-gate/merged-requirements.md`

---

## EXISTING_FILES

**Primary edit target — `src/superclaude/skills/task-builder/SKILL.md` (2308 lines; spec cited ≤2155, file drifted +153 but every cited anchor is present and verified):**

- `:41` — `--spec <path>` input doc (threading source). Resolves explicit `--spec` → `@file` in GOAL → `SPEC:`/`PRD:`/`TDD:` in BUILD_REQUEST → none; written to frontmatter `spec_path:`. (FR-12 anchor)
- `:201` — `SPEC_PATH` BUILD_REQUEST-component doc (parallels :41).
- `:853-856` — **BUILD_REQUEST POST gate block**: `POST_REFLECT_GATE: ENABLED` + `SPEC_PATH:` + `DEPTH: <max(tcs-derived depth, standard)>` + `TASK_FILE:`. This is the §10.2 schema-change site (retire `POST_REFLECT_GATE`, introduce `REFLECT_POST_MODE`). A.9 mediation MALFORMED flow referenced at `:848-851`.
- `:1423` — A.10.7 PRE-gate cross-ref to A.9 `POST_REFLECT_GATE` (rename ripple — OUT OF SCOPE to change PRE behavior, but the reference text may need a touch).
- `:1933` — frontmatter `spec_path:` field.
- `:1942` — **frontmatter `reflect_post: ""` PENDING sentinel** (§10.3 / FR-2 / §9.5 — sentinel retained ONLY for halt/2-degraded-halt; absent for none; written by inline run/wrapper for modes 1/2). Add `reflect_post_mode:` here.
- `:1994-1999` — **CURRENT POST item, verbatim** ("Independent post-execution reflection gate (fresh session, HALT)"). This is the §6.4 byte-for-byte back-compat anchor (NFR-2 / V15). The §6.3.1 unified diff is computed against exactly these 6 lines.
- `:2051` — validation-checklist item: "POST reflect item present and positioned penultimate … when POST_REFLECT_GATE is ENABLED — MALFORMED if omitted". Replaced by §9 V1–V16 / per-mode map.
- `~:2094` — per-gate `task-integrity` counter (§9.3 MODE-MATCH insertion site — verify exact line).
- `:2108` — **Critical Rule 19** "POST reflect gate in generated task files." Rewritten for the dial (§9.1 fail=MALFORMED).
- `:2114-2154` — **`## Reflect Depth (Deterministic TCS)`**: S1–S6 FERs (`:2122-2127`), formula `TCS = 3·S1+4·S2+2·S3+2·S4+5·S5+4·S6` (`:2134`), threshold table (`:2141-2145`), overrides **O1** (S5>0⇒floor standard `:2149`), **O2** (S6=1⇒force deep `:2150`), **O3** (item-cap `:2151`), **O4** (POST never quick `:2152`), ±4 tiebreaker (`:2154`). §4 auto predicate + §7 depth reconciliation reuse this verbatim — single producer.

**Second edit target — `src/superclaude/agents/rf-qa.md` (552 lines):**

- `:330-369` — **`#### Structural Gate Additions (TB-Add-1 through TB-Add-8)`** section. This is where the §9 V1–V16 assertion matrix + per-mode active-assertion map + MODE-MATCH integrate (likely a new TB-Add-9 or a parameterized task-integrity sub-block). Mirror the existing TB-Add citation/format style.
- `:45`, `:429` — task-integrity phase listing (phase enumeration).

**Out-of-scope boundary (do NOT modify behavior):**

- `:1407-1429` — A.10.7 PRE reflect gate (internal Agent/Task spawn). `--reflect` governs the POST template ONLY. Spec §11 hard non-goal.
- The `superclaude reflect run` wrapper (sibling spec `20260608-182553-reflect-cli-wrapper`, task `TASK-RF-20260608-185553`) — Mode 2 shells out to it but this spec does NOT build/modify it.
- `sc-reflect-protocol` skill itself.

**Reusable prior research (sibling task, directly relevant):**

- `.dev/tasks/to-do/TASK-RF-20260608-185553/research/06-taskbuilder-template-integration.md` (18KB) — already studied the Phase-N POST HALT item verbatim, TCS section, O4 floor, DEPTH baked, a 4-edit reversible plan, and Rule#19/checklist amendments. CROSS-VALIDATE, do not blindly trust (sibling scoped the wrapper's `POST_REFLECT_MODE: wrapper|halt` branch, which this spec RETIRES as a live field).

**Test surface (sparse — markdown/skill refactor, not Python):**

- `tests/skills/test_task_builder_merge.py` — only existing task-builder test.
- `tests/audit/` — fixture-based markdown assertion tests (DNSP/monotonicity/execution-context) — possible model for fixture-based V1–V16 acceptance tests IF a Python surface is warranted.
- No existing test references `reflect_post` / `POST_REFLECT` / `--reflect`. The §13 AT matrix is largely conceptual (assertions on generated-tasklist bytes).

## PATTERNS_AND_CONVENTIONS

- **SoT discipline (NFR-6, CLAUDE.md ABSOLUTE RULE):** edit `src/superclaude/skills/...` + `src/superclaude/agents/...` → `make sync-dev` → `.claude/`. NEVER stage `.claude/` mirrors. `make verify-sync` before commit. (memory `feedback_claude_dir_gitignored`)
- **UV-only** for any Python ops; `make lint` = ruff check only, CI separately runs `ruff format --check` (memory `reference_make_lint_vs_ci_ruff_format`). markdownlint applies to `.md` edits (memory `feedback_no_strategy_pivot_to_avoid_hooks` — obey hook output exactly).
- **Single-producer / single-oracle design (FR-9, NFR-3):** `reflect_post_mode` frontmatter is the lone authority; computed once at A.9; rf-qa reads it, never re-derives.
- **Byte-for-byte reversibility (NFR-2, V15):** the `halt`/`2-degraded-halt` item must reproduce `:1994-1999` exactly after placeholder substitution — a diff of "old behavior" must be empty.
- **HALT discipline (FR-7, FR-8):** every non-`none` item HALTs on non-pass, routes report+reason → `### Open Questions`, never auto-proceeds/auto-executes Tier-3 (memory `feedback_human_decision_items_must_halt`).
- **No nesting (FR-4, FR-11, NFR-7):** Mode 2 = Bash shell-out only (never Agent/Task); Mode 1 = inline by a top-level executor only, with runtime nested-executor HALT (memory `reference_subagent_cannot_nest_skill_fanout`).
- **Worktree path discipline:** cwd is `<repo>/.claude/worktrees/reflectWrapper/`; all artifact paths resolve to the worktree (memory `feedback_worktree_discipline`).

## GAPS_AND_QUESTIONS

Researchers must resolve with evidence (file:line):

1. **Exact A.9 producer site** — where in the skill body the BUILD_REQUEST POST gate field is consumed and the emitted item assembled (spec calls it "A.9"; the `:853` block is the BUILD_REQUEST schema, the `:1994-1999` block is the emitted template — pin the precise resolution/emission seam and where `reflect_post_mode` + the advisory WARNING get written).
2. **Exact `task-integrity` counter line** (spec §9.3 says `:2094`) — verify and capture surrounding text for the MODE-MATCH insertion.
3. **rf-qa integration shape** — does the V1–V16 matrix become a new `TB-Add-9`, a parameterized block under task-integrity, or a standalone `### Reflect Mode-Match` subsection? Determine the lowest-friction integration that mirrors existing TB-Add style and the per-mode active-assertion map (§9.2).
4. **`REFLECT_POST_MODE` vs sibling `POST_REFLECT_MODE` collision** — confirm the sibling task's `POST_REFLECT_MODE` field (if it landed in SKILL.md) is reconciled as a deprecated read-time alias (§10.1 step 3, INV-005), with NO live field collision.
5. **Verification approach for a markdown refactor** — is there a realistic automated test surface (fixture-based V1–V16 assertions à la tests/audit/), or is verification = self-consistency review + make verify-sync + markdownlint + manual AT walkthrough? This drives the BUILD_REQUEST TESTING_REQUIREMENTS value.
6. **`{BASE}`/`{EXECUTOR_CLASS}`/`{DEPTH}` placeholder resolution** — confirm how these are currently resolved (`start_commit`, `git merge-base`, O4 floor) so Mode 1/2 templates thread them identically (FR-12, V14).
7. **`auto` `W` wrapper-availability probe** — the §8.1 frozen probe (`superclaude reflect --help` exits 0 / `reflect` subcommand registered). Confirm the probe shape is buildable at A.9 build time and what the builder writes for `*-degraded-halt`.

## RECOMMENDED_OUTPUTS

6 codebase research files (Deep tier, single track), no web research (NFR-1 forbids new external logic — purely internal refactor):

- `research/01-post-gate-anatomy.md` — File Inventory: verbatim current state of every SKILL.md target surface.
- `research/02-tcs-auto-fer-machinery.md` — Data Flow Tracer: TCS/S1-S6/O1-O4 + §4 auto predicate + §7 depth reconciliation wiring.
- `research/03-rfqa-validation-integration.md` — Integration Points: rf-qa.md task-integrity + V1–V16 + MODE-MATCH + SKILL.md :2051/:2094/:2108 sites.
- `research/04-flag-plumbing-precedence.md` — Integration Points: §10 precedence, §5 old→new map, frontmatter/BUILD_REQUEST fields, advisory WARNING, sibling-field collision check.
- `research/05-template-patterns-examples.md` — Template & Examples: MDTM 02 rules + sibling task/research-06 cross-validation + SoT/reversibility patterns.
- `research/06-test-verification-surface.md` — Test & Verification: realistic verification approach for a SKILL.md/rf-qa.md refactor; feasibility of fixture-based AT tests.

## SUGGESTED_PHASES

(Builder will structure; indicative — the refactor is naturally ordered by dependency so the generated tasklist likely follows the spec's edit seams.)

- Preparation: record `start_commit`/BASE; confirm SoT + sync workflow; snapshot `:1994-1999` for the V15 byte-anchor.
- Core SKILL.md edits (one item per seam): §10 flag parse + precedence + §5 map; BUILD_REQUEST schema `:853` (`REFLECT_POST_MODE`); §7 depth reconciliation + O4 fate `:2114-2154`; §4 auto FER + §8 probe/ladder at A.9; per-mode templates §6.1-6.5 replacing `:1994-1999`; frontmatter `:1942` `reflect_post_mode`; §10.4 advisory WARNING.
- rf-qa.md edits: V1–V16 matrix + per-mode active-assertion map + MODE-MATCH; SKILL.md `:2051`/`:2108` rewrites.
- Validation/verification: `make sync-dev` + `make verify-sync` + markdownlint; self-consistency walkthrough of §9.1 against §13 AT matrix; spot-check V15 byte-identity.
- POST reflect gate (this skill's own A.9-generated item) + Update-status-to-Done.

## TEMPLATE_NOTES

- **MDTM Template: 02 (Complex Task).** Rationale: multi-phase (prep → interdependent edits → validation), conditional flows (wrapper-probe degradation, mode-dependent assertions), quality gates. Not a simple known-input/known-output transform.
- **Tier: Deep, 6 researchers.** Conceptually dense (13 FR / 8 NFR / 16 validation assertions / precedence lattice / byte-for-byte back-compat) across 2 files with a non-obvious test surface, despite low file count.
- **Granularity (A3):** one checklist item per edit seam (each spec § maps to ≥1 item), NOT a batch "implement the spec" item. The spec's `target_surfaces` list + §6/§9 sub-templates give per-item detail.
- **QA gates:** PER_PHASE not required, but a FINAL self-consistency + verify-sync gate is. The builder will append the skill's own POST reflect dial item per Critical Rule 19 (recursion is fine — this task edits the very machinery that emits it; the generated item uses the CURRENT machinery at build time).

## AMBIGUITIES_FOR_USER

None blocking — the spec is exhaustively specified (resolved open questions §, total old→new map, worked examples A/B/C, V1–V16 matrix, §13 AT matrix). Two items the builder will surface as task-file Open Questions rather than guess:

- Whether the rf-qa V1–V16 integration is a new `TB-Add-9` vs a parameterized task-integrity sub-block (research will recommend; final shape is a low-risk implementer choice the executor confirms).
- Whether any automated (fixture-based) acceptance tests are in-scope for this refactor or verification is self-consistency + verify-sync only (research §06 determines feasibility; default to the lighter approach unless a clean fixture surface exists).
