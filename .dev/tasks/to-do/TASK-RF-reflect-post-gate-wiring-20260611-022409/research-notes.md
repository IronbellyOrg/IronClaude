# Research Notes: Reflect-Wrapper POST/terminal gate-wiring (O1 + O2)

**Date:** 2026-06-11
**Scenario:** A (explicit)
**Depth Tier:** Standard (focused — small edit surface, deep prior investigation)
**Track Count:** 1
**Decision of record:** Option A — conform to the authoritative contract; the abandoned-dial `Mode 2 / auto-resolved-2 / §6.3` taxonomy is NOT revived. The stale acceptance-test assertion is rewritten to the flat contract shape.

---

## DRIVING SPEC (authoritative — do NOT re-derive)

`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md` (Contract v1.0; reflect skill contract target `1.4.0`).
Design source: `.../20260610-053000-reflect-wrapper-autofix/merged-requirements.md` (§0 abandons the dial).

**SUPERSEDED — do NOT use as spec:** `.dev/proposals/reflect-in-task-builder.md`, `reflect-in-sc-tasklist.md` (#138-era in-tasklist `/sc:reflect --mode post` form).

## GOAL

Replace ONLY the terminal/per-phase POST reflect-gate **emission** in two generator skills with flat Bash shell-outs to `superclaude reflect run`, wrapped in the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker skip guard, persisting `start_commit` / per-phase start SHA / `executor_model_class` in frontmatter. Leave the PRE gate (Stage 10.5, `--mode pre`, #138) intact. Rewrite the stale acceptance test to the flat shape. `make sync-dev` after editing `src/`.

- **O1** (task-builder terminal gate — whole tasklist):
  `superclaude reflect run <ABS_TASKLIST_PATH> --depth deep --fix --promote`
  (`--base` omitted → wrapper resolves from frontmatter `start_commit`).
- **O2** (sc:tasklist end-of-phase gate — per phase):
  `superclaude reflect run <ABS_PHASE_FILE_PATH> --depth deep --fix --no-promote --base <PHASE_N_START_SHA>`.
- **Skip-guard (contract §3.2)** wraps BOTH gates:
  ```bash
  if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then
    echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0
  fi
  superclaude reflect run <FILE> --depth deep --fix [--promote | --no-promote --base <SHA>]
  ```
- **Exit codes (fail-closed):** only `0` completes the gate; `10` halted, `11` degraded, `2` blocked → gate FAILS, surface.

## EXISTING_FILES (edit surface — VERIFIED on branch reflect/wrapper-gate-wiring @ bcad8852)

1. `src/superclaude/skills/task-builder/SKILL.md` (185 KB) — **O1 owner.** Current POST emission is the **self-run subagent** form (`/sc:reflect --mode post` spawned via subagent), NOT a wrapper shell-out. Surfaces to change (line anchors approximate — researchers MUST re-verify):
   - POST item template `N.{X-1}` (~L2193–2198): self-run subagent `/sc:reflect --mode post …`.
   - Critical Rule 20 (~L2312): mandates the self-run subagent form, forbids human-handoff/HALT.
   - A.9 BUILD_REQUEST `POST_REFLECT_GATE: ENABLED` block (~L1073).
   - Validation-checklist line for the POST item (~L2253).
   - A.11 presentation line describing POST (~L1724).
   - `## Reflect Depth (Deterministic TCS)` (~L2320+) + O4 floor (~L2356): currently feeds `{DEPTH}` into the `/sc:reflect` item. Under the contract, the wrapper gate depth is **fixed `deep`** (not TCS-derived). Builder MUST reconcile: the O1 shell-out hardcodes `--depth deep`; TCS/O4 no longer parameterize the POST wrapper gate's depth. PRE gate keeps using TCS depth (PRE is unchanged).
2. `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (81 KB) — **O2 owner.** Current per-phase terminal task is `/sc:reflect --mode post …` (heading "Post-Execution Reflection: sc:reflect --mode post", ~L1041; spawn directive ~L1063). Surfaces:
   - Per-phase Post-Execution Reflection task block (~L1036–1082).
   - Mirror in `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` (~L129–174).
   - Structural checks / Self-Check governing checkpoint-is-last + post-reflection task (~L359–363, 1020–1064, 1129, 1169 incl. checks #18–20).
   - `argument-hint` `--no-reflect` toggle (~L9) — distinct from the abandoned `--reflect` dial; KEEP (it is the gate on/off toggle).
3. `tests/cli/reflect/test_no_nesting_guard.py` (6.3 KB) — **acceptance test owner.** `test_layer_a_wrapper_branch_is_bash_shellout` + helper `_extract_wrapper_branch` (marker `**Mode \`2\` / \`auto-resolved-2\` (§6.3, DEFAULT) — wrapper shell-out, remediate:**` … `**Mode \`halt\``) + `@pytest.mark.xfail(strict=False)`. MUST be rewritten to assert the FLAT contract shape (skip-guard + `superclaude reflect run` + `--depth deep` + `--fix`; NFR-7 negative: no `Task(` / `subagent_type`) against the new O1 emission, and resolve to green/XPASS. Layer B + thinness tests (same file) are UNCHANGED — do NOT touch them.

## VERIFIED CLI SURFACE (branch includes PR #159; NFR-5 satisfied here)

`superclaude reflect run <TASKLIST>` exists with: `--depth [standard|deep]`, `--fix/--no-fix` (default `--fix`), `--promote/--no-promote` (default `--promote`), `--base TEXT` (highest precedence), `--max-fix-iterations` (default 2), `--timeout` (3600), `--print-command`, `--dry-run`, `--resume`, `--tmux`, `--output`, `--allow-single-vendor`. Source: `src/superclaude/cli/reflect/commands.py`; registered `src/superclaude/cli/main.py:442`.

## FRONTMATTER the generators MUST persist (contract §6)

| Key | Site | Shape |
|-----|------|-------|
| `start_commit` | O1 | git SHA (whole-task base; `--base` omitted → wrapper resolves from here) |
| per-phase `start_commit` (or pass `--base <sha>` on the gate line) | O2 | git SHA per phase; canonical path = explicit `--base <PHASE_N_START_SHA>` on the gate line |
| `executor_model_class` | O1 + O2 | model-class alias (e.g. `sonnet`) → reflect `--executor-model` |
| `reflect_post:` | both | written BACK by the wrapper — generators leave room, never hand-author/lock |

## PATTERNS_AND_CONVENTIONS

- Source-of-truth: edit `src/superclaude/` then `make sync-dev`; never edit `.claude/` directly (memory `feedback_hooks_source_of_truth`). The acceptance test reads `src/superclaude/skills/task-builder/SKILL.md` (the SRC, per its own docstring), so sync is for parity not for the test.
- PRE gate (Stage 10.5 / A.10.7, `--mode pre`) is INTACT — do NOT modify.
- Recursion-breaker marker name is load-bearing: MUST be exactly `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`; never clear/unset/rename/second-marker it.
- No `--reflect <…>` dial flag anywhere (abandoned). No `<base>..HEAD` range for `--base`. `--depth` only `standard|deep`.

## GAPS_AND_QUESTIONS (for focused researchers to close)

1. EXACT current text of each O1 surface in task-builder/SKILL.md (verbatim block to replace, exact line numbers) — so the builder writes surgical Edits.
2. EXACT current text of each O2 surface in sc-tasklist-protocol/SKILL.md + phase-template.md + which structural checks/Self-Checks reference the post-reflection task shape (and whether any assert `/sc:reflect` literally, requiring update).
3. EXACT test rewrite target: new `_extract_wrapper_branch` anchor (what marker delimits the O1 block in the NEW SKILL) + the flat assertions + xfail decorator disposition (keep strict=False → XPASS, vs remove → PASS).
4. How O1/O2 emit an ABSOLUTE path + the per-phase start SHA at generation time (the executor resolves `<phase-N-start-sha>` at run time — placeholder vs frontmatter; confirm canonical path per contract §6 note).
5. TCS-depth reconciliation: confirm the wrapper gate depth is fixed `deep` and the TCS `{DEPTH}` plumbing is removed ONLY from the POST wrapper item (PRE keeps TCS).

## RECOMMENDED_OUTPUTS (focused researcher assignments)

- `research/01-o1-taskbuilder-edit-surface.md` — all O1 anchors, verbatim current blocks, frontmatter, TCS reconciliation.
- `research/02-o2-sctasklist-edit-surface.md` — all O2 anchors, verbatim current blocks, phase-template mirror, structural checks/Self-Checks, --no-reflect toggle.
- `research/03-acceptance-test-and-guard-shape.md` — verbatim current test, flat rewrite target, marker/anchor for new extractor, skip-guard shape, exit-code consumption, other-worktree copies (do-not-touch note).

## SUGGESTED_PHASES (for the generated task file)

P1 Preparation/branch + frontmatter-key plumbing · P2 O1 wiring (task-builder) · P3 O2 wiring (sc-tasklist + phase-template) · P4 Acceptance-test rewrite · P5 sync-dev + verification (xfail→XPASS, full reflect test suite, verify-sync) · P6 QA gate(s) + POST reflect item + Done. Template **02** (discovery + multi-file edit + conditional verification).

## TEMPLATE_NOTES

Template 02. Tier Standard. QA_GATE_REQUIREMENTS: PER_PHASE (multi-file skill-body edit with a hard acceptance gate). TESTING_REQUIREMENTS: UNIT (the reflect test suite is the acceptance surface — `tests/cli/reflect/test_no_nesting_guard.py` + full `tests/cli/reflect/`). VALIDATION: `make sync-dev`, `make verify-sync`, `uv run ruff format --check src/ tests/` (memory `reference_make_lint_vs_ci_ruff_format`), full `uv run pytest tests/cli/reflect/`.

## AMBIGUITIES_FOR_USER

RESOLVED by the user (2026-06-11): Option A — conform to contract, retire the stale Mode-2 test assertion. The `Mode 2 / auto-resolved-2 / §6.3` dial taxonomy is NOT revived. One residual sub-decision for the builder to surface as an Open Question (non-blocking): keep the `@pytest.mark.xfail(strict=False)` decorator so the rewritten test reports **XPASS** (literal "xfail flips to XPASS"), vs remove the decorator for a clean **PASS**. Default: keep strict=False → XPASS, matching the stated acceptance phrasing; note the staleness in the xfail reason.
