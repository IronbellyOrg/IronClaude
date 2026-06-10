# Ad-hoc documentation tasklist — PR #159 (reflect auto-fix wrapper)

**Driving change:** PR #159 — `feat(reflect): audit-only wrapper → bounded auto-fix engine (contract 1.4.0)`.
Branch `feat/reflect-wrapper-autofix`. Evolves `superclaude reflect run` into a
validate→review→auto-fix→verify→promote engine and bumps the `sc-reflect-protocol`
skill contract `1.3.0 → 1.4.0`.

**Source-of-truth refs every doc agent should read before writing:**
- Spec: `.dev/brainstorms/20260610-053000-reflect-wrapper-autofix/merged-requirements.md` (FR-1–FR-10, §1 state machine, §3 verdict→action table, §8 ACs)
- CLI source: `src/superclaude/cli/reflect/{commands,config,runner,contract,models}.py`
- Skill contract: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §9.1 (`remediation_task_path`, `contract_version: 1.4.0`), §4.6 + `refs/remediation-handoff.md` (headless `--remediate`)
- Audit verdict: `.dev/tasks/to-do/TASK-RF-reflect-wrapper-autofix-20260610-053000/phase-outputs/reviews/deep-reflect/REPORT.md`
- Template to mirror (for the new CLI guide): `docs/guides/sprint-cli-tools-release-guide.md`

## Parallel-safety contract (READ FIRST)

- **Each task owns exactly ONE target file** — no two tasks touch the same file, so all run concurrently with zero merge risk.
- Match the **existing voice/structure** of the file (or, for the new guide, of `sprint-cli-tools-release-guide.md`).
- **SoT discipline:** never edit or stage anything under `.claude/`. Docs live in `docs/`, `README.md`, `CHANGELOG.md`.
- **No fabrication:** every flag/exit-code/behavior must trace to the source refs above. When unsure, read `commands.py`/`runner.py` rather than guess.
- Do **not** run `git add`/commit — leave staging to the operator.

---

## D1 — CREATE: `docs/guides/reflect-cli-tools-guide.md`  🔴 High (headline gap)

The `superclaude reflect run` CLI is undocumented (0 hits across 230 doc files). Create a guide mirroring `docs/guides/sprint-cli-tools-release-guide.md`'s structure (Release Summary → Command Reference: What it does / Use when / Syntax / Key options / Examples).

Must cover, grounded in `commands.py` + `runner.py` + merged-requirements §1/§3:
- The validate→review→auto-fix→verify→promote engine (the §1 state machine) and how it differs from the audit-only v1.
- **Full flag surface**: `--fix/--no-fix`, `--max-fix-iterations` (default 2), `--base`, `--promote/--no-promote` (default **--promote**), `--depth standard|deep`, `--tmux`, `--resume`, `--dry-run`, `--print-command`, `--output`, `--executor-model`, `--allow-single-vendor`, `--timeout`.
- **AUTO-FIXABLE vs HUMAN-REQUIRED carve-out** (`classify_fix`): drift/necessary → auto-fix; regression / needs_human_decision / user_decision_required / unauthorized / grounding-gaps → terminal HALT.
- **Exit codes**: 0 pass / 10 halted / 11 degraded / 2 blocked.
- **`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion breaker** + `--max-fix-iterations` bound (dual termination).
- **O1 (whole-tasklist) vs O2 (per-phase)** invocation shapes; promote-by-default; O2 `--no-promote` is generator-passed (per the reconciled FR-5).
- Fail-closed semantics (DEGRADED/BLOCKED never auto-fixed; failed apply → HALT never PASS).

**Paste-ready:**
```
/sc:document docs/guides/reflect-cli-tools-guide.md --focus feature --type guide
```
Prompt to the agent: "CREATE `docs/guides/reflect-cli-tools-guide.md` documenting the `superclaude reflect run` CLI auto-fix engine from PR #159. Mirror the section structure of `docs/guides/sprint-cli-tools-release-guide.md`. Ground every flag/exit-code/behavior in `src/superclaude/cli/reflect/commands.py`, `runner.py`, and `.dev/brainstorms/20260610-053000-reflect-wrapper-autofix/merged-requirements.md` (§1 state machine, §3 verdict table, §8 ACs). Cover the full flag surface, the AUTO-FIXABLE/HUMAN-REQUIRED carve-out, exit codes 0/10/11/2, the recursion breaker + max-fix-iterations bound, O1/O2 invocation, and fail-closed semantics. Touch ONLY this one new file. Do not stage `.claude/`."

---

## D2 — UPDATE: `CHANGELOG.md`  🟠 Medium

Add a `## [Unreleased]` reflect entry (match the existing sprint-CLI entry style: `#### Added` / `#### Changed` sub-blocks).
- **Added**: `--fix/--no-fix`, `--max-fix-iterations`, `--base` precedence, `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion breaker, pure `classify_fix` carve-out, `remediation_task_path` contract field (skill `1.3.0 → 1.4.0`), headless `--remediate` auto-authoring.
- **Changed**: `--promote` default `False → True`; the wrapper never force-sets `--no-promote`.
- Note the fail-closed guarantees + thinness (no `cli.sprint`/`cli.roadmap` import, no `async`, `ClaudeProcess`-only).

**Paste-ready:**
```
/sc:document CHANGELOG.md --focus changelog
```
Prompt: "UPDATE `CHANGELOG.md` `[Unreleased]` with a reflect wrapper auto-fix entry (Added/Changed sub-blocks matching the existing sprint-CLI entry style). Source: PR #159, `merged-requirements.md`, `src/superclaude/cli/reflect/`. Touch ONLY `CHANGELOG.md`."

---

## D3 — UPDATE: `README.md`  🔴 High

The CLI command list (`README.md:91-93`) shows `superclaude sprint run` / `superclaude roadmap run|validate` but omits reflect. Add `superclaude reflect run <tasklist> --fix --promote` (and a one-line description) alongside the peers, with a link to the new D1 guide.

**Paste-ready:**
```
/sc:document README.md --focus feature
```
Prompt: "UPDATE `README.md` — add `superclaude reflect run` to the CLI command listing near lines 91-93 (alongside sprint/roadmap), one-line description + link to `docs/guides/reflect-cli-tools-guide.md`. Match the existing terse README style. Touch ONLY `README.md`."

---

## D4 — UPDATE: `docs/user-guide/commands.md`  🟠 Medium

The `/sc:reflect` *skill* is documented at `:1002-1024`, but the `superclaude reflect run` **CLI wrapper** (the auto-fix engine) is not. Add a CLI-wrapper subsection under the reflect section that: (a) distinguishes the CLI auto-fix engine from the `/sc:reflect` skill it orchestrates, (b) lists the wrapper flags (`--fix`, `--max-fix-iterations`, `--base`, promote-default), (c) notes headless `--remediate` auto-authoring + contract `1.4.0` (`remediation_task_path`), and links to the D1 guide.

**Paste-ready:**
```
/sc:document docs/user-guide/commands.md --focus feature
```
Prompt: "UPDATE `docs/user-guide/commands.md` — extend the `/sc:reflect` section (~:1002) with a `superclaude reflect run` CLI-wrapper subsection (auto-fix engine vs. the skill; wrapper flags `--fix`/`--max-fix-iterations`/`--base`/promote-default; headless `--remediate`; contract 1.4.0 `remediation_task_path`; link to `docs/guides/reflect-cli-tools-guide.md`). Source: `src/superclaude/cli/reflect/commands.py`, `SKILL.md §9.1`. Touch ONLY this file."

---

## D5 — UPDATE: `docs/reference/commands-list.md`  🟡 Low

Add `superclaude reflect run` to the catalog (Testing & Quality category, near the existing `/reflect` entry at `:27`), as the CLI auto-fix gate, with a link to the D1 guide.

**Paste-ready:**
```
/sc:document docs/reference/commands-list.md --focus reference
```
Prompt: "UPDATE `docs/reference/commands-list.md` — add a `superclaude reflect run` entry under Testing & Quality (near `:27`) as the CLI validate→auto-fix→promote gate, link to `docs/guides/reflect-cli-tools-guide.md`. Touch ONLY this file."

---

## D6 — UPDATE (OPTIONAL): `docs/user-guide/flags.md`  🟡 Low

`:138` has a `Reflect Command Flags (/sc:reflect)` table for the skill. Optionally add a short note / cross-reference that the `superclaude reflect run` CLI wrapper adds `--fix`/`--max-fix-iterations`/`--base` and flips `--promote` on by default — pointing to the D1 guide. Skip if it would duplicate D1/D4.

**Paste-ready:**
```
/sc:document docs/user-guide/flags.md --focus reference
```

---

## How to run in parallel

Spawn one agent per task (D1–D5 core; D6 optional), each running its paste-ready `/sc:document` prompt. They touch disjoint files, so order is irrelevant and all run concurrently. After they finish: `uv run` any doc-lint, then the operator stages + commits (never `.claude/`).
