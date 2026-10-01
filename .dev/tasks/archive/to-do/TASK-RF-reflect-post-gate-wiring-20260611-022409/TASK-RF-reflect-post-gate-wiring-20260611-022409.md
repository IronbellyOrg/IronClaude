---
id: "TASK-RF-reflect-post-gate-wiring-20260611-022409"
title: "Wire reflect-wrapper POST/terminal gates (O1 + O2) as flat superclaude reflect run shell-outs"
description: "Replace the terminal (O1) and per-phase (O2) POST reflect-gate emission in task-builder and sc-tasklist-protocol with flat `superclaude reflect run` Bash shell-outs per the authoritative contract; persist start_commit / per-phase start-SHA / executor_model_class; rewrite the stale Layer-A acceptance test to the flat shape; make sync-dev."
status: "🟠 Doing"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-06-11"
updated_date: "2026-06-11"
start_date: "2026-06-11"
assigned_to: "orchestrator"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: "1 focused session (surgical multi-file edits + test rewrite + validation)"
task_type: static
spec_path: "/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md"
start_commit: "8cefefdee026346b4d6dd804d142513096b05b5e"
executor_model_class: "opus"
# reflect_post: the wrapper did NOT write this back (degraded path / exit 11). The executor records the
# actual run outcome below per item 6.3 Output; it is the real degraded result, not a hand-authored pass.
reflect_post:
  wrapper_exit: 11            # degraded (null-convergence) -> gate FAILS per contract §2; item 6.3 HALTs
  substantive_verdict: pass   # REPORT.md recommendation: status=success, Tier 2, calibrated 0.92
  deviations: "0 drift / 0 regression / 2 authorized / 2 necessary"
  reviewer_findings: "3 raised -> 3 dropped (all refuted vs contract by evidence-validator)"
  degraded_cause: "SELF-INFLICTED dogfood artifact — SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1 leaked into the audit's own test-verify env -> 6 cli-smoke/promote tests hit the recursion breaker (env -u -> all 10 pass); +2 pre-existing e2e fileno sandbox failures. verification_regressions_detected: 0. NOT a deliverable problem."
  report: ".dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/reflect/post/8cefefdee026/REPORT.md"
  return_contract: ".dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/reflect/post/8cefefdee026/return-contract.yaml"
  reviewed_at: "2026-06-11"
  decision_pending: "OQ-3 — exit 11 HALTs the gate; operator decision required before status->Done (item 6.4)."
reflect_pre:
  verdict: pass
  coverage_pct: 1.00
  depth: deep
  tcs: "S6=1 (Refactor) -> O2 override forces deep"
  unmapped_requirements: none
  report: ".dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/reflect/pre/report.md"
  reviewed_at: "2026-06-11"
related_docs:
- path: "/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md"
  description: "Authoritative interface contract (O1/O2 shapes, skip-guard §3.2, exit codes §2, frontmatter §6, promotion §5). Single source — do NOT re-derive."
- path: ".dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/research/01-o1-taskbuilder-edit-surface.md"
  description: "Verbatim O1 edit sites in task-builder/SKILL.md with line anchors."
- path: ".dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/research/02-o2-sctasklist-edit-surface.md"
  description: "Verbatim O2 edit sites in sc-tasklist-protocol/SKILL.md + phase-template.md."
- path: ".dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/research/03-acceptance-test-and-guard-shape.md"
  description: "Layer-A test rewrite target (lines 49-84) + DO-NOT-MODIFY map + contract guard/exit verbatim."
- path: ".dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/research/04-gap-fill-o2-viability.md"
  description: "Resolutions for the 6 research-gate gaps (O2 --base placeholder, reflect_post writeback Option 2A, --output, abspath, sibling tests, corrected test anchor)."
- path: ".dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/qa/qa-research-gap-report-round2.md"
  description: "Final research-gate report — adds the four-assertion amendment, O1 frontmatter gap, and O1 diff-base reversal."
tags:
- "reflect-wrapper"
- "task-builder"
- "sc-tasklist"
- "gate-wiring"
- "contract-conformance"
reflect_post:
  verdict: degraded
  status: success
  run_id: 8cefefdee026
  tier_reached: 2
  report: /config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/reflect/post/8cefefdee026/REPORT.md
  contract: /config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/reflect/post/8cefefdee026/return-contract.yaml
  reason: null-convergence
  deviations:
    authorized: 2
    necessary: 2
    drift: 0
    regression: 0
  head: 8cefefdee026346b4d6dd804d142513096b05b5e
  reviewed_at: '2026-06-11T12:32:03.420190+00:00'
---

# Wire reflect-wrapper POST/terminal gates (O1 + O2) as flat `superclaude reflect run` shell-outs

## Task Overview

PR #159 landed the `superclaude reflect run` auto-fix wrapper engine on this branch (`reflect/wrapper-gate-wiring`, HEAD `bcad8852`). The two generator skills still emit the OLD POST reflect form (`/sc:reflect --mode post` self-run subagent in task-builder; `/sc:reflect --mode post` spawn directive per phase in sc-tasklist). The authoritative interface contract (`reflect-wrapper-contract.md`) requires the generators to emit **flat Bash shell-outs** to `superclaude reflect run`, wrapped in the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker skip guard, with `start_commit` / per-phase start-SHA / `executor_model_class` persisted in frontmatter.

This task replaces ONLY the terminal/per-phase POST gate **emission** at two sites — **O1** (task-builder terminal gate, whole tasklist) and **O2** (sc-tasklist end-of-phase gate, per phase) — leaves the PRE gate (Stage 10.5 / A.10.7 `--mode pre`) fully intact, rewrites the stale Layer-A acceptance test (`test_layer_a_wrapper_branch_is_bash_shellout`) to assert the flat shape, and runs `make sync-dev`.

**Decision of record (user-confirmed 2026-06-11):** conform to the contract (Option A). The abandoned `--reflect` dial `Mode 2 / auto-resolved-2 / §6.3` taxonomy is **NOT** revived — the stale test assertion that waits on it is retired in favor of the flat contract shape.

## Key Objectives

- O1: task-builder/SKILL.md terminal POST item emits `superclaude reflect run <ABS_TASKLIST> --depth deep --fix --promote` behind the §3.2 skip guard; the generated-tasklist frontmatter template gains `start_commit` + `executor_model_class` + room for `reflect_post`.
- O2: sc-tasklist-protocol/SKILL.md + phase-template.md per-phase task emits `superclaude reflect run <ABS_PHASE_FILE> --depth deep --fix --no-promote --base <PHASE_N_START_SHA> --output …` behind the §3.2 skip guard; emitted phase files are pre-seeded with minimal frontmatter; all four `# Phase N` line-1 assertions are amended to permit it.
- Critical Rule 20 + the L2195 diff-base prose are rewritten so the wrapper shell-out form is CANONICAL (was MALFORMED) and `start_commit` is the O1 base (reversing the old prohibition, per the contract).
- The Layer-A acceptance test asserts the flat shape and resolves green; Layer B + the thinness guards + `test_promote_plumbing.py` + `test_cli_smoke.py` are untouched.
- `make sync-dev` + `make verify-sync` + `ruff format --check` + full `tests/cli/reflect/` + sc-tasklist structural tests all green.

## Prerequisites & Dependencies

- The wrapper engine (`src/superclaude/cli/reflect/`) is present on this branch via PR #159 (`superclaude reflect run --help` confirms `--depth/--fix/--promote/--no-promote/--base`). NFR-5 (land-before-generators) is satisfied here.
- Work on a fresh branch off updated `origin/master`, mirroring the worktree's base, per the build request. Capture the branch's `start_commit` for provenance.
- Edit `src/superclaude/` ONLY; run `make sync-dev` to mirror into `.claude/`. NEVER edit `.claude/` directly and NEVER stage `.claude/` (gitignored except settings.json).
- Read the contract (`reflect-wrapper-contract.md`) §2/§3/§5/§6 and the five research files before editing. Do NOT re-derive the contract.

## Execution Context

- **References:** GOAL (wire O1+O2 flat wrapper shell-outs + retire the stale Layer-A test); the authoritative contract `reflect-wrapper-contract.md`; research files 01–04 and `qa/qa-research-gap-report-round2.md`; the prior investigation establishing that the `Mode 2/§6.3` dial was abandoned (PR #157 closed).
- **Source areas:** task-builder skill body (O1 POST emission, generated-tasklist frontmatter template, Critical Rule 20, the TCS depth section, A.9 BUILD_REQUEST block, A.11 banner); sc-tasklist-protocol skill body + its phase-template (O2 per-phase reflection task, the four `# Phase N` line-1 structural assertions, the `--no-reflect` toggle); reflect CLI wrapper (`commands.py`/`runner.py`/`config.py` — READ-ONLY, the consumed engine); `tests/cli/reflect/test_no_nesting_guard.py` Layer A only.
- **Key constraints:** conform to the contract (no Mode/§6.3 revival); the skip-guard marker name is EXACTLY `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` (never clear/unset/rename/second-marker it); the PRE gate (Stage 10.5 / A.10.7 `--mode pre`) stays INTACT; edit `src/superclaude/` then `make sync-dev`; do NOT touch sibling worktrees' copies of the test, nor `test_promote_plumbing.py` / `test_cli_smoke.py`.

---

## Phase 1: Preparation — branch, baseline, frontmatter-key plan

- [x] **1.1 — Create a fresh feature branch off updated `origin/master`**
  - **Context**: Per the build request, the implementation starts on a fresh branch off updated `origin/master`. This worktree's branch `reflect/wrapper-gate-wiring` @ `bcad8852` already carries the #159 wrapper engine (`src/superclaude/cli/reflect/`) and is a valid base. Project rule: feature branches only; never commit to master.
  - **Action**: `git fetch origin`; create `git checkout -b reflect/post-gate-wiring-o1o2 bcad8852cbfd681181bf2019229e0b60ae5dc0c4` (or rebase the current branch onto `origin/master` if master has advanced AND already contains the #159 wrapper). Record the resulting HEAD SHA as the working baseline.
  - **Output**: A fresh branch whose base contains `src/superclaude/cli/reflect/`.
  - **Verification**: `git rev-parse --abbrev-ref HEAD` shows the new branch; `uv run superclaude reflect run --help` exits 0 and lists `--fix`/`--promote`/`--base`/`--depth`.
  - **Completion gate**: On a fresh branch with the wrapper engine present.

- [x] **1.2 — Baseline the acceptance test and full reflect suite**
  - **Context**: The named acceptance test `tests/cli/reflect/test_no_nesting_guard.py::test_layer_a_wrapper_branch_is_bash_shellout` is currently `xfailed`. The flip must be provable against a recorded baseline.
  - **Action**: Run `uv run pytest tests/cli/reflect/test_no_nesting_guard.py -q` and `uv run pytest tests/cli/reflect/ -q`; record both results.
  - **Output**: Recorded baseline — Layer A `xfailed`; the rest of `tests/cli/reflect/` green.
  - **Verification**: Output shows `xfailed` for the named test and zero failures elsewhere.
  - **Completion gate**: Baseline recorded in the Task Log.

- [x] **1.3 — Transcribe the contract emission shapes + skip guard verbatim**
  - **Context**: The exact strings come from the contract, not memory. Source: `/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md` §2 (`:35-72` O1/O2 + exit codes), §3.2 (`:94-108` skip guard), §5 (`:142-153` O2 `--no-promote`), §6 (`:157-177` frontmatter).
  - **Action**: Read those ranges. Confirm verbatim: O1 = `superclaude reflect run <ABS_TASKLIST_PATH> --depth deep --fix --promote`; O2 = `superclaude reflect run <ABS_PHASE_FILE_PATH> --depth deep --fix --no-promote --base <PHASE_N_START_SHA>`; the §3.2 guard block; exit codes 0/10/11/2 (only 0 completes the gate). Verify no `--reflect`, no `--max-turns`, no `<base>..HEAD` range, `--depth` ∈ {standard, deep}.
  - **Output**: Verbatim strings transcribed into the Task Log for reuse in P2–P4.
  - **Verification**: Strings match the contract byte-for-byte. <!-- evidence-absence: contract lives in sibling worktree reflectWrapper; cited by absolute path, byte-identical to the ReflectGateWiring copy per cross-validation -->
  - **Completion gate**: Contract shapes confirmed and transcribed.

---

## Phase 2: O1 wiring — task-builder/SKILL.md (whole-tasklist terminal gate)

> All edits in this phase target `src/superclaude/skills/task-builder/SKILL.md`. Verbatim current blocks + line anchors are in `research/01-o1-taskbuilder-edit-surface.md` (line numbers may have shifted slightly — the executor re-greps each anchor before editing). The O1 emission is `superclaude reflect run {TASK_FILE} --depth deep --fix --promote` behind the §3.2 skip guard. `{TASK_FILE}` is already an absolute path token (the wrapper absolutizes its positional via `commands.py` `resolve_path=True` + `config.py` `.resolve()` — research 04 GAP-4).

- [x] **2.1 — Replace the terminal POST item template `N.{X-1}` with the wrapper shell-out form**
  - **Context**: The current POST item (research 01 SURFACE 1, `src/superclaude/skills/task-builder/SKILL.md` ~L2193-2200) is a self-run `/sc:reflect --mode post` SUBAGENT item. It must become a Bash shell-out. This item is also the **SINGLE SOURCE OF TRUTH for the test anchor heading** consumed by item 4.1.
  - **Action**: Re-grep the current item heading (`Independent post-execution reflection gate`). Replace the item's Action/Output/Verification/Completion-gate body with: (a) the §3.2 skip guard verbatim; (b) `superclaude reflect run {TASK_FILE} --depth deep --fix --promote`; (c) exit-code consumption (only `0` completes; `10` halted / `11` degraded / `2` blocked → surface and HALT). The item heading MUST be the EXACT literal `**N.{X-1} -- Independent post-execution reflection gate (wrapper shell-out)**` — this is MANDATORY, not an example: item 4.1's `_extract_wrapper_branch` does a byte-exact `text.index()` on the substring `Independent post-execution reflection gate (wrapper shell-out)`, so any deviation silently breaks the acceptance test (wrong slice or `ValueError`). End the block before the next `- [ ] **N.X` bullet. The block MUST contain NO `Task(` and NO `subagent_type` tokens (NFR-7).
  - **Output**: The O1 terminal item emits the flat wrapper shell-out behind the skip guard; the anchor heading is the fixed literal above.
  - **Verification**: `grep -n "Independent post-execution reflection gate (wrapper shell-out)" src/superclaude/skills/task-builder/SKILL.md` returns exactly the O1 item heading; `grep -n "superclaude reflect run" src/superclaude/skills/task-builder/SKILL.md` shows the O1 line with `--depth deep --fix --promote`; `grep -c "subagent_type\|Task(" ` within the item block = 0; the §3.2 guard string is present.
  - **Completion gate**: O1 item is the wrapper shell-out form with the EXACT mandated anchor literal and zero nesting tokens.

- [x] **2.2 — Reverse the L2195 diff-base prose (`start_commit` is now the O1 base)**
  - **Context**: The current item prose (research 01 SURFACE 1, ~L2195) says `start_commit` is "retained in frontmatter for provenance only, never as the diff base" and prefers `git merge-base`. The contract (§6) makes the wrapper resolve the O1 base from frontmatter `start_commit` (single ref vs working tree). The old prohibition conflated the `..HEAD` RANGE form with the single-ref form; the single-ref form IS valid for uncommitted work (round2 HIGH, resolved by Option A).
  - **Action**: FIRST resolve OQ-2 (see `### Open Questions`) — this item REVERSES a documented Critical-Rule rationale, so it is a `needs_human_decision` point and MUST NOT proceed on a silent default. Once OQ-2 is acknowledged, rewrite the prose to: O1 omits `--base` → the wrapper resolves the base from frontmatter `start_commit` (single ref vs working tree, capturing uncommitted work; precedence `--base > start_commit > merge-base`). Document one sentence of rationale for the reversal and cross-reference OQ-2.
  - **Output**: Prose matches the contract base-resolution; OQ-2 acknowledged.
  - **Verification**: `grep -n "never as the diff base" src/superclaude/skills/task-builder/SKILL.md` returns nothing; the new prose names `start_commit` as the O1 base; OQ-2 is marked acknowledged in the Task Log.
  - **Completion gate**: OQ-2 acknowledged by the operator AND diff-base prose reversed with rationale documented. (HALT here if OQ-2 is unresolved — do not auto-default to the reversal.)

- [x] **2.3 — Rewrite Critical Rule 20 to make the wrapper shell-out form CANONICAL**
  - **Context**: Critical Rule 20 (research 01 SURFACE 2, ~L2312) currently mandates the SELF-RUN subagent form and declares the wrapper shell-out form MALFORMED. Under the contract the shell-out IS canonical.
  - **Action**: Rewrite Rule 20: when `POST_REFLECT_GATE: ENABLED`, the builder MUST emit the penultimate terminal item as the `superclaude reflect run … --depth deep --fix --promote` wrapper shell-out behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard; the self-run-subagent and human-handoff/HALT forms are now MALFORMED. Preserve anti-orphaning (penultimate, before Update-status-to-Done).
  - **Output**: Rule 20 describes the wrapper shell-out as canonical.
  - **Verification**: `grep -n "superclaude reflect run" src/superclaude/skills/task-builder/SKILL.md` includes the Rule 20 region; Rule 20 no longer calls the shell-out MALFORMED.
  - **Completion gate**: Rule 20 reflects the contract.

- [x] **2.4 — Update the validation-checklist line for the POST item**
  - **Context**: The Task File Validation Checklist line (research 01 SURFACE 4, ~L2253) asserts the POST item is the SELF-RUN form, penultimate, not human-handoff.
  - **Action**: Rewrite it to assert the POST item is the WRAPPER SHELL-OUT form (`superclaude reflect run … --depth deep --fix --promote` + skip guard), penultimate, NFR-7-clean (no `Task(`/`subagent_type`). MALFORMED if omitted or if it emits the self-run-subagent/human-handoff form.
  - **Output**: Checklist line matches the new canonical form.
  - **Verification**: `grep -n "POST reflect item" src/superclaude/skills/task-builder/SKILL.md` shows the wrapper-shell-out wording.
  - **Completion gate**: Validation checklist updated.

- [x] **2.5 — Update the A.9 BUILD_REQUEST `POST_REFLECT_GATE` block + the SURFACE-8 `--spec`→POST prose**
  - **Context**: The A.9 BUILD_REQUEST POST block (research 01 SURFACE 3, ~L1073-1076) currently threads `SPEC_PATH`/`DEPTH`/`EXECUTOR_CLASS` into the self-run `/sc:reflect` item. Under O1 the wrapper hardcodes `--depth deep` and resolves base/spec/executor from frontmatter + contract precedence. Research 01 SURFACE 8 ALSO names two prose cross-refs that describe `--spec`/`SPEC_PATH` flowing into the POST item — ~L41 (the `--spec` input description "baked into the templated POST reflect item's command") and ~L282 (`SPEC_PATH` glossary → POST item). The O1 wrapper shell-out does NOT take `--spec`, so these must be corrected too.
  - **Action**: Update the A.9 block to instruct the builder to emit the wrapper shell-out O1 item; drop the now-irrelevant `{DEPTH}`/`{SPEC_PATH}` placeholders from the POST emission (the wrapper reads `executor_model_class` from frontmatter). Keep `POST_REFLECT_GATE: ENABLED` semantics. Then re-grep and correct the SURFACE-8 prose at ~L41 and ~L282 so they no longer claim `--spec`/`SPEC_PATH` is threaded into the POST item's command (PRE still consumes `--spec`; only the POST emission changes).
  - **Output**: A.9 block describes O1 wrapper emission; SURFACE-8 prose no longer ties `--spec` to the POST item.
  - **Verification**: `grep -n "POST_REFLECT_GATE" src/superclaude/skills/task-builder/SKILL.md` region references `superclaude reflect run`; `grep -nE "templated POST reflect item.*command|SPEC_PATH.*POST" src/superclaude/skills/task-builder/SKILL.md` shows the corrected prose (no `--spec`→POST claim).
  - **Completion gate**: A.9 block + the two SURFACE-8 prose sites updated.

- [x] **2.6 — Update the A.11 present-results POST line + the Reflect-Gates banner**
  - **Context**: The A.11 banner (research 01 SURFACE 5, ~L1722-1724) describes POST as "emitted as final-phase item N.{X-1} (the executor runs /sc:reflect via a subagent)".
  - **Action**: Rewrite to "POST (`superclaude reflect run`): emitted as the penultimate final-phase item — a flat wrapper shell-out (`--depth deep --fix --promote`) behind the recursion-breaker skip guard."
  - **Output**: Banner text matches the wrapper form.
  - **Verification**: `grep -n "superclaude reflect run" src/superclaude/skills/task-builder/SKILL.md` includes the A.11 banner region.
  - **Completion gate**: Banner updated.

- [x] **2.7 — Decouple the TCS `{DEPTH}` plumbing from the POST item (PRE keeps TCS)**
  - **Context**: O1 hardcodes `--depth deep` (contract §2). The `## Reflect Depth (Deterministic TCS)` section + O4 floor (research 01 SURFACE 6, ~L2320, ~L2356) currently feed `{DEPTH}` into the POST `/sc:reflect` item. The PRE gate (A.10.7) keeps the FULL TCS apparatus.
  - **Action**: In the TCS section, narrow the POST-gate references so the wrapper O1 item is documented as fixed `--depth deep` (not TCS-derived); explicitly retain TCS depth derivation for the PRE gate. Do NOT delete the TCS section or O4 — only stop threading `{DEPTH}` into the POST wrapper item.
  - **Output**: TCS section: PRE uses TCS depth; O1 POST is fixed deep.
  - **Verification**: The POST item carries literal `--depth deep` (not `{DEPTH}`); the PRE A.10.7 spawn still uses the TCS-derived depth.
  - **Completion gate**: TCS depth scoped to PRE; O1 fixed deep.

- [x] **2.8 — Add `start_commit` + `executor_model_class` (+ `reflect_post` room) to the generated-tasklist frontmatter template**
  - **Context**: The generated-tasklist frontmatter template (research 01 SURFACE 7, ~L2137-2156) declares none of `start_commit`/`executor_model_class`/`reflect_post`. The wrapper reads `start_commit` as the O1 base and `executor_model_class` for `--executor-model`; absence of the latter silently drops the anti-self-confirmation exclusion (round2 HIGH). The wrapper writes `reflect_post:` back and does NOT create frontmatter, so the slot must exist.
  - **Action**: Add to the frontmatter template: `start_commit: "<sha captured at task start>"`, `executor_model_class: "<executor-class>"`, and a commented `# reflect_post: written back by the wrapper — leave room, do not hand-author/lock`. Update the builder's frontmatter-population instructions to capture `start_commit` at build time and record the executor class.
  - **Output**: Generated tasklists carry the three keys; O1 writeback has a target.
  - **Verification**: `grep -nE "start_commit:|executor_model_class:|reflect_post" src/superclaude/skills/task-builder/SKILL.md` shows all three in the frontmatter template region.
  - **Completion gate**: O1 frontmatter keys present.

---

## Phase 3: O2 wiring — sc-tasklist-protocol/SKILL.md + phase-template.md (per-phase gate)

> Edits target `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` and `.../sc-tasklist-protocol/templates/phase-template.md`. Verbatim blocks + anchors in `research/02-o2-sctasklist-edit-surface.md`; viability findings in `research/04-gap-fill-o2-viability.md` + `qa/qa-research-gap-report-round2.md`. O2 emission = `superclaude reflect run <ABS_PHASE_FILE> --depth deep --fix --no-promote --base <PHASE_N_START_SHA> --output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/` behind the §3.2 skip guard. `--no-promote` is REQUIRED (contract §5, no per-phase adapter).

- [x] **3.1 — Replace the SKILL.md per-phase reflection spawn directive with the wrapper shell-out**
  - **Context**: The per-phase Post-Execution Reflection task's spawn directive (research 02, `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` ~L1062-1064) is `/sc:reflect --mode post --remediate --tasklist … --diff <phase-commit-range> --depth <DET> --tier <DET> --executor-model <CLASS> --output …`. Replace it with the flat shell-out + skip guard.
  - **Action**: Re-grep the spawn directive. Replace with: §3.2 skip guard, then `superclaude reflect run TASKLIST_ROOT/phase-<PP>-tasklist.md --depth deep --fix --no-promote --base <PHASE_N_START_SHA> --output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/`. KEEP the `### T<PP>.<NN> -- Post-Execution Reflection:` heading PREFIX (struct check #18 asserts it); change only the suffix (drop `: sc:reflect --mode post`). Drop `--tier`/`<DET DEPTH>` (wrapper is fixed `--depth deep`, no `--tier`). Update the Acceptance-Criteria line: `--remediate`→`--fix`; `--executor-model` flag → sourced from phase frontmatter.
  - **Output**: SKILL.md per-phase task emits the O2 wrapper shell-out.
  - **Verification**: `grep -n "superclaude reflect run" src/superclaude/skills/sc-tasklist-protocol/SKILL.md` shows the O2 line with `--no-promote --base`; the `### T<PP>.<NN> -- Post-Execution Reflection:` prefix is intact; no `Task(`/`subagent_type` in the block.
  - **Completion gate**: O2 SKILL emission is the wrapper shell-out, heading prefix preserved.

- [x] **3.2 — Mirror the O2 emission in phase-template.md**
  - **Context**: The mirror spawn directive lives at `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` ~L153-155 (research 02). It must match item 3.1 byte-for-byte in shape.
  - **Action**: Apply the identical replacement (skip guard + O2 shell-out + `--output`), preserving the heading prefix.
  - **Output**: phase-template.md matches SKILL.md O2 emission.
  - **Verification**: `grep -n "superclaude reflect run" src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` shows the O2 line; `diff` of the two emission blocks shows only the file-path token differing.
  - **Completion gate**: Mirror updated and consistent.

- [x] **3.3 — Specify `--base <PHASE_N_START_SHA>` runtime resolution (in-task [VERIFICATION] step)**
  - **Context**: sc:tasklist generates phase files BEFORE any phase executes, so the phase-start SHA is unknowable at generation time. There is NO programmatic Sprint-CLI placeholder substitution (research 04 GAP-1 — grep of `cli/sprint/` is clean); the existing `<phase-commit-range>` is resolved by an in-task `[VERIFICATION]` agent step (SKILL.md:1067). `--base <PHASE_N_START_SHA>` must be resolved the same way — NEVER a fabricated generation-time SHA.
  - **Action**: In the per-phase task body (and the template), add/keep a `[VERIFICATION]`-class STEP instructing the executing agent to resolve `<PHASE_N_START_SHA>` at execution time (the phase's start commit) and substitute it into the gate line before invoking it. Document that `<PHASE_N_START_SHA>` is a placeholder, never pre-filled.
  - **Output**: The O2 gate line's `--base` is a runtime-resolved placeholder with an explicit resolution step.
  - **Verification**: `grep -n "PHASE_N_START_SHA\|phase.*start.*sha" src/superclaude/skills/sc-tasklist-protocol/SKILL.md` shows the placeholder + the resolution step; no fabricated SHA appears.
  - **Completion gate**: Runtime SHA-resolution mechanism specified.

- [x] **3.4 — Pre-seed minimal frontmatter into emitted phase files (reflect_post writeback target)**
  - **Context**: The wrapper does NOT create frontmatter — `runner.py:146-148` returns `frontmatter-missing` and `runner.py:586-590` flips a clean PASS to BLOCKED (`models.py:48` → exit 2). Phase files have NO frontmatter today. So EVERY O2 gate on a frontmatter-less phase file would false-FAIL (research 04 GAP-2 / round2 — Option 2A is mechanically forced).
  - **Action**: Update the phase-file emission (SKILL.md phase-file spec + phase-template.md) so each emitted phase file begins with a minimal YAML frontmatter block: `---` / `executor_model_class: "<EXECUTOR_CLASS>"` / optional `start_commit:` / a `# reflect_post:` room comment / `---`, THEN the existing `# Phase N --` heading.
  - **Output**: Emitted phase files carry frontmatter the wrapper can write `reflect_post:` back into.
  - **Verification**: The phase-file template shows leading frontmatter then `# Phase N --`; `executor_model_class` is present.
  - **Completion gate**: Phase-file frontmatter seeded.

- [x] **3.5 — Amend ALL FOUR `# Phase N` line-1 structural assertions to allow leading frontmatter**
  - **Context**: Four assertions mandate the phase file's first line is `# Phase N`: struct check #5 (`SKILL.md:1128`), `SKILL.md:100`, `SKILL.md` ~L860-863 (re-grep — anchors may drift a few lines), and `phase-template.md:12` (round2 IMPORTANT — amending only #5 leaves the SKILL self-contradictory). The Sprint CLI parsers (`_extract_phase_name`, `count_tasks_in_file`, `parse_tasklist`) are already frontmatter-tolerant, so this is safe (the `~L860` "required for TUI display name" rationale is stale).
  - **Action**: Re-grep each of the four anchors. Amend each to permit optional leading YAML frontmatter before `# Phase N --` (e.g. "starts with an optional `---` frontmatter block followed by `# Phase N --`"). Update the stale `:863` rationale note.
  - **Output**: All four assertions permit leading frontmatter; no self-contradiction remains.
  - **Verification**: `grep -nE "starts with .*# Phase N|first line.*# Phase" src/superclaude/skills/sc-tasklist-protocol/SKILL.md src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` shows all four updated; a search for any remaining "first line must be `# Phase`" with no frontmatter allowance returns nothing.
  - **Completion gate**: Four assertions amended consistently.

- [x] **3.6 — Confirm the `--no-reflect` toggle + PRE gate (Stage 10.5) are untouched**
  - **Context**: `--no-reflect` (argument-hint L9 + sites) is the gate ON/OFF toggle, NOT the abandoned `--reflect` value-dial — it must be KEPT. The per-phase PRE gate (Stage 10.5, `/sc:reflect --mode pre`) and its COMPLEXITY_SCORE→depth/tier machinery are out of scope.
  - **Action**: Verify (do not edit) that `--no-reflect` still gates O2 emission and that Stage 10.5 PRE is unchanged. If any P3 edit incidentally touched them, revert that incidental change.
  - **Output**: `--no-reflect` and PRE gate intact.
  - **Verification**: `grep -n "no-reflect" src/superclaude/skills/sc-tasklist-protocol/SKILL.md` unchanged in count vs baseline; the Stage 10.5 `/sc:reflect --mode pre` block is byte-identical to baseline.
  - **Completion gate**: Toggle + PRE gate confirmed intact.

---

## Phase 4: Acceptance-test Layer-A rewrite (flat shape)

> Edits target ONLY lines 49-84 of `tests/cli/reflect/test_no_nesting_guard.py` (the `_extract_wrapper_branch` helper, the `@pytest.mark.xfail` decorator, and `test_layer_a_wrapper_branch_is_bash_shellout`). Verbatim current text + DO-NOT-MODIFY map in `research/03-acceptance-test-and-guard-shape.md`; corrected anchor guidance in `research/04-gap-fill-o2-viability.md` GAP-6.

- [x] **4.1 — Rewrite `_extract_wrapper_branch` to slice the O1 wrapper block by the new anchor**
  - **Context**: The current helper (`tests/cli/reflect/test_no_nesting_guard.py:49-60`) slices between the stale markers `**Mode \`2\` / \`auto-resolved-2\` (§6.3, DEFAULT) — wrapper shell-out, remediate:**` and `**Mode \`halt\``, which exist nowhere in any SKILL. The corrected anchor is the O1 item heading fixed in item 2.1 (e.g. `Independent post-execution reflection gate (wrapper shell-out)`); the slice ends at the next `- [ ] **N.X` bullet (research 04 GAP-6 — do NOT use the nonexistent `#### POST reflect gate (O1`).
  - **Action**: Rewrite `_extract_wrapper_branch` to `text.index(<the exact O1 item heading from 2.1>)` → end at the next checklist bullet after it. Keep the `text.index()` idiom (fence-agnostic). The anchor string MUST equal the heading written in item 2.1 (single source of truth).
  - **Output**: Helper extracts the live O1 wrapper-shell-out block.
  - **Verification**: `uv run python -c "import tests.cli.reflect.test_no_nesting_guard as t, pathlib; print('superclaude reflect run' in t._extract_wrapper_branch(pathlib.Path('src/superclaude/skills/task-builder/SKILL.md').read_text()))"` prints `True` (the helper returns a non-empty block containing the shell-out). The anchor substring `Independent post-execution reflection gate (wrapper shell-out)` is identical to the literal mandated in item 2.1.
  - **Completion gate**: Helper anchors on the live O1 block (substring matches 2.1 byte-for-byte).

- [x] **4.2 — Rewrite `test_layer_a_wrapper_branch_is_bash_shellout` to assert the flat shape**
  - **Context**: Positive asserts must match the contract emission + skip guard; negative asserts reuse `_NESTING_TOKENS` (`Task(`, `subagent_type`).
  - **Action**: Replace the body asserts with: `assert "superclaude reflect run" in branch`; `assert "--depth deep" in branch`; `assert "--fix" in branch`; `assert "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" in branch`; and the existing negative loop over `_NESTING_TOKENS`. Use only real CLI flags (`--depth`/`--fix`/`--promote` confirmed in `commands.py`).
  - **Output**: The test asserts the flat wrapper shell-out shape.
  - **Verification**: The asserted tokens all appear in the live O1 block; the test references no Mode/§6.3 markers.
  - **Completion gate**: Test body asserts the flat shape.

- [x] **4.3 — Resolve the `@pytest.mark.xfail` decorator (OQ-1)**
  - **Context**: OQ-1: keep `@pytest.mark.xfail(strict=False)` so the now-passing test reports XPASS (matches the user's literal acceptance "xfail flips to XPASS"), vs remove it → clean PASS. RECOMMENDED: keep `strict=False` and update the xfail `reason` to record the stale-marker history.
  - **Action**: Apply the user's choice from OQ-1 (default: keep `strict=False`, rewrite the `reason` to: the Layer-A marker was migrated from the abandoned `Mode 2/§6.3` dial taxonomy to the flat `superclaude reflect run` contract shape; the test now passes against the live O1 emission). If OQ-1 says remove, delete the decorator.
  - **Output**: Decorator disposition applied per OQ-1.
  - **Verification**: `uv run pytest tests/cli/reflect/test_no_nesting_guard.py::test_layer_a_wrapper_branch_is_bash_shellout -q` reports `xpassed` (keep) or `passed` (remove) — NOT `xfailed`, NOT `failed`.
  - **Completion gate**: The named test resolves green (xpassed/passed).

- [x] **4.4 — Confirm Layer B, the thinness guards, and sibling tests are untouched**
  - **Context**: DO-NOT-MODIFY: `test_layer_b_wrapper_module_has_no_agent_imports` (87-94), the three thinness guards (97-134), all module constants; and `test_promote_plumbing.py` / `test_cli_smoke.py` (they assert the wrapper's INTERNAL prompt — research 04 GAP-5, safe).
  - **Action**: Verify (no edit) that only lines ~49-84 changed in `test_no_nesting_guard.py` and that the two sibling test files are unmodified.
  - **Output**: Edit scope confined to Layer A.
  - **Verification**: `git diff --stat` shows only `test_no_nesting_guard.py` among test files; `git diff tests/cli/reflect/test_no_nesting_guard.py` touches only the Layer-A region.
  - **Completion gate**: Scope confined; siblings untouched.

---

## Phase 5: Sync + full validation

- [x] **5.1 — Run `make sync-dev` to mirror `src/superclaude/` into `.claude/`**
  - **Context**: Source of truth is `src/superclaude/`; `.claude/` is generated. The acceptance test reads the SRC file, but sync keeps the dev mirror consistent and is required before `verify-sync`.
  - **Action**: `make sync-dev`.
  - **Output**: `.claude/skills/{task-builder,sc-tasklist-protocol}/` mirror the edited sources.
  - **Verification**: `make sync-dev` exits 0.
  - **Completion gate**: Sync complete.

- [x] **5.2 — `make verify-sync`**
  - **Context**: CI fails if `src/` and `.claude/` diverge.
  - **Action**: `make verify-sync`.
  - **Output**: Sync parity confirmed.
  - **Verification**: `make verify-sync` exits 0.
  - **Completion gate**: verify-sync green.

- [x] **5.3 — `uv run ruff format --check src/ tests/`**
  - **Context**: `make lint` only runs `ruff check`; CI separately runs `ruff format --check src/ tests/` (project memory `reference_make_lint_vs_ci_ruff_format`). The only Python edited is the test file.
  - **Action**: `uv run ruff format --check src/ tests/` (and `uv run ruff check src/ tests/`). If the test file needs formatting, `uv run ruff format tests/cli/reflect/test_no_nesting_guard.py` and re-check.
  - **Output**: Format + lint clean.
  - **Verification**: Both commands exit 0.
  - **Completion gate**: ruff format + check green.

- [ ] **5.4 — Acceptance gate: the named test flips + full reflect suite green**
  - **Context**: The hard acceptance criterion.
  - **Action**: `uv run pytest tests/cli/reflect/test_no_nesting_guard.py::test_layer_a_wrapper_branch_is_bash_shellout -q` then `uv run pytest tests/cli/reflect/ -q`.
  - **Output**: Named test resolves green; no regressions in the reflect suite.
  - **Verification**: The named test reports `xpassed`/`passed`; `tests/cli/reflect/` shows zero failures (Layer B, thinness, promote-plumbing, cli-smoke all still green).
  - **Completion gate**: Acceptance test flipped AND full reflect suite green.

- [x] **5.5 — sc-tasklist structural-check regression**
  - **Context**: P3 amended four `# Phase N` line-1 assertions + seeded phase frontmatter. Confirm no structural-check or sprint-parser regression.
  - **Action**: Locate and run any tests covering sc-tasklist phase-file structure / checkpoint-is-last / `# Phase N` parsing (e.g. `grep -rl "Phase N\|phase-template\|checkpoint" tests/`; run the matching test files). Run the broader suite touching sc-tasklist/sprint if present.
  - **Output**: No structural/parser regressions from the frontmatter seeding.
  - **Verification**: The relevant test files pass; the Sprint task scanner still finds `### T<PP>.<NN>` headings with leading frontmatter present.
  - **Completion gate**: sc-tasklist structural tests green (or N/A documented with evidence if none exist).

---

## Phase 6: QA gate, independent reflection, completion

> Final-document QA gate per MDTM M3 (lens-based, parallel report-only) + I20 (serialized fix authorization) + I19 (≥6 agents: 3 rf-qa structural + 3 rf-qa-qualitative content). The skill bodies edited are >500 lines and this is a source-material transformation (old emission → contract emission), so the gate also verifies fidelity to the contract.

- [x] **6.1 — Spawn 3 rf-qa structural lens agents in PARALLEL (report-only)**
  - **Context**: Independent adversarial verification of the edits before completion. All three `fix_authorization: false`, spawned in ONE message via the Agent tool (`subagent_type: "rf-qa"`, `mode: "bypassPermissions"`). ADVERSARIAL STANCE: assume errors; find ≥5 issues each; a 0-issue verdict needs proof of exhaustive checking.
  - **Action**: Spawn:
    - **Agent A — contract-conformance lens:** Read the contract `reflect-wrapper-contract.md` §2/§3/§5 and the edited `src/superclaude/skills/task-builder/SKILL.md` + `sc-tasklist-protocol/SKILL.md` + `templates/phase-template.md`. Verify O1 = `superclaude reflect run … --depth deep --fix --promote` and O2 = `… --depth deep --fix --no-promote --base <PHASE_N_START_SHA> --output …` BYTE-FOR-BYTE vs the contract; the §3.2 skip guard is present and verbatim at BOTH sites; no `--reflect`/`--max-turns`/`<base>..HEAD`; `--depth` ∈ {standard,deep}. Output `qa/qa-task-contract-conformance.md`, VERDICT PASS/FAIL.
    - **Agent B — NFR-7 + skip-guard lens:** Verify NEITHER O1 nor O2 emission block contains `Task(` or `subagent_type`; the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` marker is present, correctly spelled, never cleared/renamed; exit-code consumption (0/10/11/2) is documented. Output `qa/qa-task-nfr7-guard.md`, VERDICT PASS/FAIL.
    - **Agent C — structural-integrity lens:** Verify all FOUR `# Phase N` line-1 assertions (SKILL.md:100/863/1128 + phase-template.md:12) were amended consistently; the `### T<PP>.<NN> -- Post-Execution Reflection:` heading PREFIX is preserved (struct check #18); phase-file frontmatter seeding is present; the PRE gate (Stage 10.5) + `--no-reflect` toggle are untouched. Output `qa/qa-task-structural-integrity.md`, VERDICT PASS/FAIL.
  - **Output**: 3 structural lens reports.
  - **Verification**: All three report files exist with a `VERDICT:` line.
  - **Completion gate**: 3 rf-qa reports returned.

- [x] **6.2 — Spawn 3 rf-qa-qualitative content lens agents in PARALLEL (report-only)**
  - **Context**: All three `fix_authorization: false`, ONE message (`subagent_type: "rf-qa-qualitative"`, `mode: "bypassPermissions"`). ADVERSARIAL STANCE as above.
  - **Action**: Spawn:
    - **Agent D — operational-correctness lens:** Verify the edits actually work end-to-end: the grep/test verification commands in each item are valid; `--output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/` preserves the declared Reflect Report Path + its Acceptance Criterion; `{TASK_FILE}`/phase-path tokens absolutize correctly; the `--base` runtime-resolution step is present for O2. Output `qa/qa-task-operational.md`, VERDICT PASS/FAIL.
    - **Agent E — completeness / orphan-reference lens:** Grep both edited SKILLs for ANY surviving self-run `/sc:reflect --mode post` POST-emission reference, MALFORMED-shell-out wording, `{DEPTH}` threaded into the POST item, or stale `start_commit … never as the diff base` prose. Confirm all 8 O1 sites + all O2 sites + the A.11 banner + validation checklist are mutually consistent. Output `qa/qa-task-completeness.md`, VERDICT PASS/FAIL.
    - **Agent F — test-correctness lens:** Verify the rewritten `_extract_wrapper_branch` anchor EQUALS the O1 item heading from 2.1 (single source of truth); the asserted tokens are real CLI flags; Layer B + thinness guards + sibling tests are untouched; the xfail disposition matches OQ-1. Output `qa/qa-task-test-correctness.md`, VERDICT PASS/FAIL.
  - **Output**: 3 qualitative lens reports.
  - **Verification**: All three report files exist with a `VERDICT:` line.
  - **Completion gate**: 3 rf-qa-qualitative reports returned.

- [x] **6.2.1 — Consolidate findings + serialized fix round (I20)**
  - **Context**: Serialized fix authorization — NEVER multiple fix agents at once.
  - **Action**: Consolidate all 6 reports into `qa/qa-task-consolidated.md`. If any FAIL or any CRITICAL/IMPORTANT/MINOR finding exists, spawn ONE rf-qa fix agent (`fix_authorization: true`) with the consolidated list to apply all fixes to the SKILLs/test, then re-run the relevant verification (grep + the named test). Max 3 fix-verify cycles (governed by the Retry Monotonicity Protocol: regression → monotonicity → hard-cap → proceed).
  - **Output**: All gate findings resolved; SKILLs/test corrected.
  - **Verification**: Re-run shows all 6 lenses PASS (or remaining items documented in Open Questions after 3 cycles); the named acceptance test still resolves green.
  - **Completion gate**: QA gate PASS (all findings resolved) and `make verify-sync` + the named test still green.

- [ ] **6.3 — Independent post-execution reflection gate (wrapper shell-out)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per the contract, the canonical POST gate is a flat `superclaude reflect run` shell-out (the wrapper internally launches `/sc:reflect --mode post` as a disjoint `claude --print` subprocess — supplying the executor-disjoint context that prevents self-rubber-stamping). This dogfoods the very O1 emission this task wires.
  - **Action**: Ensure new files are staged so the working-tree diff is complete (`git add -A`). Then run the recursion-breaker-guarded wrapper shell-out:
    `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi; superclaude reflect run /config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/TASK-RF-reflect-post-gate-wiring-20260611-022409.md --depth deep --fix --no-promote`
    (`--no-promote` here because this task file is being audited in place, not promoted by this gate; the base resolves from frontmatter `start_commit`). The command uses `superclaude reflect run` and never `/sc:task`; any re-execution uses `/task`. Consume the exit code: only `0` completes the gate; `10`/`11`/`2` → surface the report and HALT.
  - **Output**: The wrapper returns; record its `{verdict, run_id, report}` into this file's frontmatter `reflect_post`. If it surfaces deviations, apply remediations or append them to `### Open Questions` (never delete existing items).
  - **Verification**: `reflect_post` in frontmatter holds a non-empty `{verdict, run_id, report}`; exit code consumed (only 0 proceeds); flagged deviations remediated or logged.
  - **Completion gate**: The wrapper exited 0 (clean or auto-fixed-and-verified) and `reflect_post` is recorded. THEN the Update-status item proceeds.

- [ ] **6.4 — Update task status to Done**
  - **Context**: All phases complete; acceptance test flipped; QA + reflect gates green.
  - **Action**: Update frontmatter: `status: "🟢 Done"`; set `updated_date` / a completion date.
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows `🟢 Done`.
  - **Completion gate**: Task marked complete.

---

## Task Log / Notes

### Execution Log
- 2026-06-11 (exec P1.1): Created feature branch `reflect/post-gate-wiring-o1o2` off `origin/master` @ `8cefefde` (#161). `origin/master..HEAD` was empty → origin/master already contains #159 (bcad8852) AND advanced (#160, #161), satisfying item 1.1's "rebase-onto-origin/master if master advanced AND contains #159" path. Working baseline = `8cefefdee026346b4d6dd804d142513096b05b5e`. `superclaude reflect run --help` exits 0 with `--fix`/`--promote`/`--no-promote`/`--base`/`--depth [standard|deep]`/`--output`. **Frontmatter `start_commit` updated bcad8852→8cefefde** so item 6.3's wrapper gate audits only THIS task's delta (base bcad8852 would have polluted the audit with #160/#161). Branch authorized by the task; the baseline shift is the mechanical consequence.
- 2026-06-11 (exec OQ-3 DECISION): **Operator chose (B) HOLD — honor the fail-closed gate.** Task NOT marked Done; stays `🟠 Doing` with 6.3/6.4 OPEN. The exit-11 degraded gate is treated as a legitimate fail-closed HALT. Root blocker = reflect-wrapper marker-leakage into its verification-subprocess env (logged as a COMPLETION-BLOCKER Follow-Up). Deliverable wiring + all unit/QA validation are complete & independently verified, but the dogfood POST gate must reach a clean exit 0 (after the engine fix) before completion. `reflect_post` records the real degraded outcome.
- 2026-06-11 (exec P6.3 — HALT): **Dogfood reflect gate ran; wrapper exit 11 (degraded / null-convergence) → gate FAILS per contract §2, item 6.3 HALTs.** Ran `superclaude reflect run <task> --depth deep --fix --no-promote` detached (background, operator-chosen); base resolved from frontmatter `start_commit=8cefefde`; `executor_model_class` set to `opus` (anti-self-confirmation worked, `executor_exclusion_degraded: false`). **Substantive audit = clean PASS** (REPORT.md: status=success, Tier 2, calibrated 0.92; 0 drift / 0 regression; 2 authorized + 2 necessary deviations; contract-conformant byte-exact at all gate sites; 24 citations / 0 fabricated; 3 reviewer findings raised→all dropped vs contract; recommendation PASS, nothing to remediate). **Degraded cause = self-inflicted dogfood artifact:** the audit's own test-verify ran with `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` exported by the wrapper → 6 cli-smoke/promote tests hit the recursion breaker (`env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` → all 10 pass) + 2 pre-existing e2e fileno sandbox failures; `verification_regressions_detected: 0`. The wrapper did NOT write `reflect_post` (degraded path); executor recorded the real degraded outcome to frontmatter `reflect_post`. **6.3 left UNCHECKED (completion gate = exit 0, not met); 6.4 NOT started.** Operator decision required — see OQ-3. Report: `reflect/post/8cefefdee026/REPORT.md`.
- 2026-06-11 (exec P6 GATE): **Phase 6 QA gate (6 lenses) complete — PASS after 1 serialized fix round.** Spawned 3 rf-qa structural (A contract / B NFR-7 / C structural) + 3 rf-qa-qualitative (D operational / E completeness / F test) in parallel, report-only. Raw: B PASS; A/C/D/E/F FAIL. Executor adversarial triage (`qa/qa-task-consolidated.md`): **2 real findings fixed** — D1 (frontmatter made REQUIRED-when-reflect-gating-enabled at SKILL:100 + struct #5, since the O2 writeback needs the block or the wrapper BLOCKS) + E1 (stale `Sub-Agent Delegation | Required` metadata → `No (flat shell-out; wrapper spawns internally)` in both O2 files). **6 false positives REJECTED with rationale:** A.F1 `--output` (required by item 3.1+GAP-3, allowed flag), A.F2/F3 (negative prohibition prose, not emitted flags), A.F4/F5 (PRE `quick` is out-of-scope `/sc:reflect`, not the wrapper), C1 (pre-existing sibling `### Checkpoint:` in human-review template, untouched by this task), D2 (remove-xfail contradicts OQ-1), F.F1 (xfail reason records the Mode-marker migration per OQ-1). Re-verified post-fix: sync+verify-sync OK, named test xpassed, parser smoke transparent. All 6 lens reports + consolidated persisted to `qa/`.
- 2026-06-11 (exec P5): **Phase 5 (sync + validation) complete.** `make sync-dev` + `make verify-sync` exit 0. `ruff format --check` + `ruff check` GREEN on the only edited Python file (`test_no_nesting_guard.py`); repo-wide ruff debt (101 files / 127 errors) is PRE-EXISTING and out of scope (see P5.3). Acceptance gate (5.4): named test **xpassed**, full `tests/cli/reflect/` = 77 passed + 1 xpassed. Structural regression (5.5): sprint suite 1155 passed (2 pre-existing `test_rerun_tasks_e2e` failures, proven baseline via stash); **a load-bearing frontmatter bug was caught and fixed** — the `# reflect_post` comment broke `_extract_phase_name` (see P5.5). Re-synced after the fix.
- 2026-06-11 (exec P4 GATE): **Phase 4 (Layer-A test rewrite) complete + phase-gate QA PASS.** `tests/cli/reflect/test_no_nesting_guard.py` lines 49-84 rewritten: `_extract_wrapper_branch` now anchors on the byte-exact O1 item heading `Independent post-execution reflection gate (wrapper shell-out)` (from item 2.1), bounded at the next `- [ ] **N.X` bullet; stale `Mode 2`/`§6.3`/`auto-resolved-2`/`Mode halt` markers gone. Test asserts `superclaude reflect run` + `--depth deep` + `--fix` + `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` + negative `_NESTING_TOKENS`. OQ-1 applied: `@pytest.mark.xfail(strict=False)` KEPT, reason migrated → test reports **xpassed**. Layer B/thinness/`_NESTING_TOKENS`/siblings byte-untouched. Adversarial rf-qa (sonnet) gate: `reviews/qa-phase-4-report.md` → VERDICT PASS; full `tests/cli/reflect/` = 77 passed, 1 xpassed.
- 2026-06-11 (exec P3 GATE): **Phase 3 (O2 wiring) complete + phase-gate QA PASS.** Both `sc-tasklist-protocol/SKILL.md` and `templates/phase-template.md` rewired: per-phase gate → flat `superclaude reflect run TASKLIST_ROOT/phase-<PP>-tasklist.md --depth deep --fix --no-promote --base <PHASE_N_START_SHA> --output …/validation/reflect-post/phase-<PP>/` behind the §3.2 skip guard (byte-identical between the two files); heading prefix `-- Post-Execution Reflection:` preserved (struct #18); Step-1 `[VERIFICATION]` resolves single-ref `<PHASE_N_START_SHA>` (no fabricated SHA, no surviving `<phase-commit-range>`); phase files pre-seeded with minimal frontmatter (`executor_model_class` + `start_commit` + `# reflect_post` room); ALL FOUR `# Phase N` assertions amended for leading frontmatter; `--no-reflect` (4=4) + Stage 10.5 PRE gate confirmed untouched. Adversarial rf-qa (sonnet) gate: `reviews/qa-phase-3-report.md` → VERDICT PASS (7/7, 0 issues).
- 2026-06-11 (exec P2 GATE): **Phase 2 (O1 wiring) complete + phase-gate QA PASS.** All 8 O1 items done in `src/superclaude/skills/task-builder/SKILL.md`: POST item → flat `superclaude reflect run {TASK_FILE} --depth deep --fix --promote` behind the §3.2 skip guard (anchor heading = exact mandated literal, zero NFR-7 nesting tokens); diff-base reversed (start_commit IS the O1 base); Rule 20 + validation checklist canonicalized; A.9 block + SURFACE-8 prose (L41/L282) decoupled from `--spec`; A.11 banner rewritten; TCS/O4 decoupled from POST (fixed deep); frontmatter gained `start_commit`/`executor_model_class`/`# reflect_post` room + population note. Adversarial rf-qa (sonnet) gate: `reviews/qa-phase-2-report.md` → VERDICT PASS (10/10, 0 issues).
- 2026-06-11 (exec P1.2): Baseline recorded. `test_layer_a_wrapper_branch_is_bash_shellout` = **1 xfailed**. Full `tests/cli/reflect/` = **77 passed, 1 xfailed** (the named test), zero failures. Flip target: xfailed → xpassed/passed.
- 2026-06-11: Task file authored by the task-builder orchestrator (the `rf-task-builder` subagent timed out during the read phase; orchestrator authored directly from gate-validated research per the A.9 builder-failure path). Research gate: 4 PASS + 1 FAIL→gap-filled (6 gaps closed) + round-2 re-gate surfaced 3 additional load-bearing items, all folded in. Awaiting structural/research-alignment/qualitative validation (A.10/A.10.25/A.10.5) + PRE reflect (A.10.7).

### Phase Findings

**P1.3 — Contract verbatim transcription (from `reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md` §2/§3.2/§5/§6, byte-confirmed 2026-06-11):**

- **O1** (`:38`): `superclaude reflect run <ABS_TASKLIST_PATH> --depth deep --fix --promote` — `--base` OMITTED → wrapper resolves base from frontmatter `start_commit`.
- **O2** (`:50`): `superclaude reflect run <ABS_PHASE_FILE_PATH> --depth deep --fix --no-promote --base <PHASE_N_START_SHA>` — single ref vs working tree, NOT `<base>..HEAD`. `--no-promote` REQUIRED (§5: no per-phase adapter).
- **§3.2 skip guard** (`:100-104`):
  ```bash
  if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then
    echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0
  fi
  superclaude reflect run <FILE> --depth deep --fix [--promote|--no-promote --base <SHA>]
  ```
  Truthy = exactly `"1"`. MUST NOT clear/unset/overwrite/rename/second-marker.
- **Exit codes** (`:65-72`): 0=pass (ONLY one that completes the gate), 10=halted, 11=degraded, 2=blocked.
- **Forbidden** (`:58-61`): `--reflect`, `--max-turns`, any `<base>..HEAD` range. `--depth` ∈ {standard, deep} only.
- **Frontmatter §6** (`:162-175`): `start_commit` (O1 whole-task base when --base omitted); per-phase `start_commit` (O2, surfaced as `--base <SHA>`); `executor_model_class` (O1+O2 → `--executor-model`, anti-self-confirm). Precedence: `--base` > frontmatter `start_commit` > `git merge-base HEAD master`. `reflect_post:` written BACK by wrapper — leave room, do not lock.

- O2 is NOT a simple emission swap: the wrapper refuses frontmatter-less files (`runner.py:146-148` → BLOCKED/exit-2), forcing phase-file frontmatter seeding + amendment of FOUR `# Phase N` line-1 assertions.
- O1 frontmatter (`executor_model_class`) was also missing — its absence silently defeats anti-self-confirmation.

**P5.5 — LOAD-BEARING CORRECTION caught by validation (frontmatter `# reflect_post` comment broke `_extract_phase_name`):** The GAP-2 research claim "the Sprint parsers are frontmatter-tolerant" was TRUE for `count_tasks_in_file` (regex `^###\s+T\d{2}\.\d{2}`, re.MULTILINE — unaffected by frontmatter) and `parse_tasklist`, but FALSE for `_extract_phase_name` (`config.py:149-160`): it returns the FIRST line that `.strip().startswith("# ")`. The item-3.4 seeded frontmatter included a `# reflect_post: …` YAML comment — a `# `-prefixed line — so `_extract_phase_name` returned `'reflect_post: written back by the wrapper'` as the phase name instead of the real `# Phase N` heading. **Fix:** removed the `# reflect_post` comment line from the O2 phase-file frontmatter in BOTH `sc-tasklist-protocol/SKILL.md` and `templates/phase-template.md`; the "leave room / wrapper writes it back / do-not-pre-seed-key-or-#-comment" guidance moved to prose. The frontmatter block still exists (`executor_model_class` + `start_commit`) so the wrapper's append-path (`runner.py:168-170`) works. **Verified:** with the fix, all three parsers pass — `count_tasks_in_file`=2, `parse_tasklist`=[T02.01,T02.02], and `_extract_phase_name` now reads the real `# Phase N` line and returns BYTE-IDENTICAL output with vs without frontmatter (`'- Wiring O2'` both — the leading `- ` is a pre-existing `--`-separator quirk in `_extract_phase_name`'s regex, NOT introduced here). **O1 NOT changed:** O1 generates MDTM task files (not sprint phase files), `_extract_phase_name` never runs on them, and the wrapper writeback regex `^reflect_post` does not match the `#`-comment — so O1 keeps its documented `# reflect_post:` room comment (matches the contract example + this task file's own frontmatter). Sprint suite: 1155 passed; the only 2 failures (`test_rerun_tasks_e2e.py`) are PRE-EXISTING (proven via `git stash` → identical failures on clean origin/master baseline), unrelated to this task.

**P5.3 — ruff scope finding (pre-existing repo debt, OUT OF SCOPE):** Repo-wide `uv run ruff format --check src/ tests/` reports 101 files would-reformat and `ruff check` reports 127 errors — ALL in files NOT touched by this task (e.g. `tests/swarm/*`; empty `git diff origin/master` for sampled failing files = pre-existing baseline debt). The ONLY Python file edited by this task — `tests/cli/reflect/test_no_nesting_guard.py` — passes BOTH `ruff format --check` (1 file already formatted, exit 0) AND `ruff check` (All checks passed!, exit 0). Fixing the 101 unrelated files would violate scope discipline and create a massive off-task diff; the pre-existing repo-wide ruff debt is left untouched. Item 5.3's gate ("ruff format + check green") is satisfied for this task's change.
- The O1 diff-base reversal (Critical Rule 20 + L2195 prose) is load-bearing and intended (Option A / contract conformance), not incidental.

**P2.2 — Diff-base reversal rationale (OQ-2 ACKNOWLEDGED + AUTHORIZED by operator 2026-06-11):** The old POST item Action declared `start_commit` "retained for provenance only, never as the diff base" and preferred a `git merge-base` `<BASE>` for a `..HEAD`-style range. The reversal is contract-mandated (§6): the wrapper diffs `start_commit` as a SINGLE ref against the WORKING TREE, which audits uncommitted work — neutralizing the old objection that only applied to the `start_commit..HEAD` RANGE form. New template prose: base precedence `--base` > frontmatter `start_commit` > `git merge-base HEAD master`. Per GAP-3, the BUILDER seeds the generated tasklist's `start_commit` from `git merge-base HEAD <integration-branch>` (item 2.8). `grep "never as the diff base"` now returns nothing.

### Follow-Up Items
- **[COMPLETION BLOCKER for THIS task — per OQ-3 HOLD] Wrapper marker-leakage bug.** `superclaude reflect run` exports `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` into the environment of its internal **verification** subprocess (the `--fix` re-verify test run), so when the verification step runs reflect-CLI tests (`tests/cli/reflect/test_cli_smoke.py`, `test_promote_plumbing.py`) those tests see the marker and self-trip the recursion breaker → 6 false failures → null-convergence → false `degraded`/exit-11. Evidence: `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` → all 10 pass; `verification_regressions_detected: 0`. Fix candidate: the wrapper should UNSET/strip the marker (and/or pass `env -u`) for the verification subprocess specifically (the marker is only meant to suppress *nested reflect gate emission*, not to leak into ordinary test runs the verify step executes). Engine files: `src/superclaude/cli/reflect/runner.py` (verification-triangle invocation) + `commands.py` (`_WRAPPER_MARKER_ENV` export). **Until fixed, item 6.3 cannot reach a clean exit 0, so this task stays `🟠 Doing` (6.3/6.4 open).** Build a separate corrective task for the engine fix, then re-run 6.3 here.
- After this lands, the companion generator worktree `ReflectInTaskLists` (`reflect/f3-hygiene-stage105-e2e`) still emits the legacy `/sc:reflect --mode post` form and will need the same O1/O2 conformance (separate task).

### Open Questions

> **OQ-3 (BLOCKING — referenced by items 6.3/6.4; raised at P6.3 dogfood gate, 2026-06-11):** The dogfood `superclaude reflect run --depth deep --fix --no-promote` exited **11 (degraded / null-convergence)**, which per contract §2 FAILS the gate; item 6.3 HALTs on 10/11/2. **However the substantive audit is a clean PASS** (REPORT.md `reflect/post/8cefefdee026/REPORT.md`: status=success, 0 drift / 0 regression, 2 authorized + 2 necessary, byte-exact contract conformance, 3 reviewer findings all dropped, recommendation PASS). The degradation is a **self-inflicted dogfood artifact**: the wrapper exports `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` into the audit's own test-verification env → 6 `test_cli_smoke`/`test_promote_plumbing` tests hit the recursion breaker (`env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` → all 10 pass) + 2 pre-existing e2e fileno failures; `verification_regressions_detected: 0`. **Decision needed before 6.4 (status→Done):** (A) accept the degradation as environment-only and mark Done (substantive audit passed); (B) re-run the gate with `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` unset in the verification env to seek a clean exit 0; (C) treat exit 11 as a hard fail-closed HALT and investigate the wrapper's null-convergence handling further. **Recommendation: (A)** — the deliverable is contract-clean; the exit 11 is a known dogfooding env artifact, not a deliverable regression. Awaiting operator.
>
> **RESOLVED 2026-06-11 → (B) HOLD — honor the fail-closed gate (operator decision via AskUserQuestion).** Exit 11 is treated as a legitimate fail-closed HALT. The task is NOT marked Done; status stays `🟠 Doing` with items 6.3 and 6.4 OPEN. The deliverable wiring + all unit/QA validation are complete and independently verified, but the dogfood POST gate did not reach a clean exit 0. **Blocker for completion:** the reflect wrapper leaks `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` into its own verification-subprocess env, causing reflect-CLI tests to self-trip the recursion breaker → false `degraded`/exit-11. This is a real wrapper-engine bug (out of THIS task's scope — engine is read-only here) and must be fixed in a separate follow-up; only then can 6.3 be re-run to a clean exit 0 and 6.4 (status→Done) proceed. See Follow-Up Items.

> **RESOLVED 2026-06-11 (operator decisions via AskUserQuestion, before P2):**
> - **OQ-2 → AUTHORIZED.** The Critical-Rule-20 diff-base reversal is operator-authorized. Items 2.2/2.3 proceed: `start_commit` becomes the O1 diff base and the wrapper shell-out form is CANONICAL.
> - **OQ-2 sub-point (GAP-3) → `git merge-base HEAD <integration>`.** The generated-tasklist `start_commit` is seeded from `git merge-base HEAD <integration-branch>` (operator chose the robust-against-interleaving option over task-start HEAD). The builder's frontmatter-population instructions (item 2.8) must document this seed semantics.
> - **OQ-1 → KEEP `strict=False` (XPASS).** Item 4.3 retains `@pytest.mark.xfail(strict=False)` and rewrites the `reason` to record the stale-marker→flat-contract migration; the test resolves `xpassed`.

- **OQ-1 (non-blocking; referenced by items 4.3):** xfail decorator on the rewritten Layer-A test — keep `@pytest.mark.xfail(strict=False)` → reports XPASS (matches the literal acceptance phrasing "xfail flips to XPASS"), vs remove → clean PASS. **Recommendation: keep `strict=False` (XPASS)** with an updated `reason` recording the stale-marker migration. Decide before/at item 4.3.
- **OQ-2 (`needs_human_decision`; referenced by item 2.2 — acknowledge before executing P2):** the O1 diff-base reversal adopts `start_commit` as the base, REVERSING the documented Critical-Rule-20 rationale (the current SKILL explicitly forbids `start_commit` as the diff base and declares the shell-out form MALFORMED). **Provenance note:** the user's "Option A" confirmation (2026-06-11) was scoped to the *Mode-dial-revival vs contract-conformance* question; it did not separately ratify this Rule-20 reversal. The contract DOES entail it (§6 base-resolution `--base > start_commit > merge-base`, single ref vs working tree — which neutralizes the old "audits nothing when uncommitted" objection that applied to the `..HEAD` RANGE form, not the single-ref form). **Decision needed:** confirm the Rule-20 reversal is authorized (recommended — it is contract-mandated). Sub-point (GAP-3): which value seeds `start_commit` — task-start HEAD (research 01 SURFACE 7 default) vs `git merge-base HEAD <integration-branch>` (more robust when commits interleave post-start). Recommendation: task-start HEAD per the contract's `start_commit` semantics; offer merge-base as an operator override. Record the chosen semantics in the Task Log at item 2.2/2.8.
