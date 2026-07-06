# QA Report — Phase Gate B (lens: TEMPLATE-CONFORMANCE)

**Topic:** sc:pr-submit skill package + command house-style conformance
**Date:** 2026-06-11
**Phase:** report-validation (structural template-conformance lens)
**Fix authorization:** false (report only)
**Stance:** ADVERSARIAL — assumed ≥10 template-conformance errors; checked every file.

---

## Scope (files read in full)

| File | Lines | Read |
|------|------:|------|
| `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` | 133 | full |
| `src/superclaude/commands/pr-submit.md` | 81 | full |
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh` | 62 | full |
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh` | 103 | full |
| `refs/*.md` (8 files) | — | H1 + naming verified |

Convention source of truth: `research/02-skill-command-hook-conventions.md` (R2), §1.1, §1.2, §3.3, §4.1, §4.3.

---

## A. SKILL.md conformance

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| A1 | Flavor-A frontmatter (minimal real YAML + HTML-comment extended block) | PASS | `SKILL.md:1-5` real YAML = `name`/`description`/`allowed-tools` only; `:7-12` HTML-comment "(for documentation, not parsed)" block with category/complexity/mcp-servers/personas — exactly the auggie-review Flavor-A shape (R2 §1.1, `:32-37`). |
| A2 | `name: sc:pr-submit-protocol` | PASS | `SKILL.md:2` `name: sc:pr-submit-protocol` — colon form, matching the auggie-review PR-sibling convention (R2 §1.1 `:79`). |
| A3 | `allowed-tools` includes scoped `Bash(gh *)` + `Bash(git *)` | PASS | `SKILL.md:4`: `... Bash(gh *), Bash(git *), Bash(uv *), Bash(make *), Bash(jq *), Task, Skill`. Scoped Bash globs per R2 §1.1 `:39`. |
| A4 | Canonical section order: Purpose → Required Input (STOP) → Output Contract → Wave structure → Will/Will-Not → Error Handling | PASS | `## Purpose` `:16`; `## Required Input (STOP if missing)` `:41`; `## Output Contract` `:57`; `## Wave / Phase Structure` `:70`; `## Will Do` `:106` / `## Will Not Do` `:113`; `## Error Handling` `:122`. Order matches R2 §1.2 canonical sequence. |
| A5 | Wave structure with LAZY per-wave ref loading | PASS | `SKILL.md:70` header literally annotates "(refs are LAZY-loaded per wave, never pre-loaded)"; ASCII map `:72-81` tags each wave with its ref; per-wave bodies restate "load `refs/X.md`" (`:84` arm gate, `:85` severity-routing, `:86` finding-verify, `:87` troubleshoot-dispatch, `:89` thread-reply, `:90` loop-guard). Matches R2 §1.2 `:106` hard convention. |
| A6 | Output Contract is a `\| Field \| Type \| Description \|` table | PASS | `SKILL.md:59-68` table with status/pr_url/round_counter/push_count/reply_count/summary_posted/applied_edits/run_log_path. Lighter-table form per R2 §1.3. |
| A7 | Required Input has explicit STOP clause | PASS | `SKILL.md:52-55` two **STOP** clauses (monitor≥1 unconfirmed PR; locked:false contract). |

---

## B. command pr-submit.md conformance

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| B1 | Full-YAML frontmatter (no HTML comment) | PASS | `pr-submit.md:1-10` all-real YAML: name/description/category/complexity/mcp-servers/personas/argument-hint/version. No HTML-comment block — correct command flavor per R2 §4.1. |
| B2 | `name: pr-submit` BARE (not `sc:pr-submit`) | PASS | `pr-submit.md:2` `name: pr-submit`. Bare command, `/sc:` prefix implied by install location — matches `commands/auggie-review.md:2` `name: auggie-review` (R2 §4.1 `:246`). |
| B3 | `## Activation` section present | PASS | `pr-submit.md:59` `## Activation`. |
| B4 | Activation contains `> Skill sc:pr-submit-protocol` blockquote (lint-architecture Check 6) | PASS | `pr-submit.md:61-62`: `**MANDATORY**: Before executing any protocol steps, invoke:` then `> Skill sc:pr-submit-protocol`. Exact R2 §4.3 `:297-298` shape; blockquote skill-id matches SKILL.md:2 `name:`. |
| B5 | `argument-hint:` present | PASS | `pr-submit.md:8` one-line signature covering all flags. |
| B6 | Body is a thin parse/validate/handoff shim (not duplicating protocol) | PASS | `pr-submit.md:56-57` `## Behavioral Flow` states "does ONLY parse + environment-validate + handoff"; `:69` defers deterministic decisions to the core + skill. |
| B7 | `## Triggers` documents hook→command linkage | PASS | `pr-submit.md:14-20`; `:19` names `offer-pr-review.sh` hook mention (R2 §4.2 `:272`). |

---

## C. scripts/*.sh conformance (gold template: `sc-bare-review/scripts/t2_preflight.sh`, R2 §3.3)

| # | Check | poll-augment-review.sh | reply-resolve-thread.sh | Evidence |
|---|-------|------------------------|-------------------------|----------|
| C1 | `#!/usr/bin/env bash` shebang | PASS | PASS | both `:1`. |
| C2 | SoT-reminder comment ("Source of truth lives in src/superclaude/; do not edit the .claude/ mirror") | PASS | PASS | poll `:16`, reply `:16` — verbatim string. |
| C3 | `set -euo pipefail` | PASS | PASS | poll `:18`, reply `:18`. Stricter than hooks per R2 §3.3 `:211`. |
| C4 | `die()` helper | PASS | PASS | poll `:20`, reply `:20` — both `die() { printf '<name>: %s\n' ... >&2; exit "${2:-1}"; }`. |
| C5 | `command -v` toolchain guards | PASS (2: gh, jq) | PASS (2: gh, jq) | poll `:33-34`, reply `:44-45`. |
| C6 | Header comment block (purpose/usage/output/exit/spec) | PASS | PASS | poll `:2-14`, reply `:2-14`. |

All scripts also pin `--repo IronbellyOrg/IronClaude` / `repos/IronbellyOrg/IronClaude/...` on every `gh` call (poll `:37,:47`; reply `:49,:68`), consistent with the fork-only PR rule — no upstream leakage in shell I/O.

---

## D. refs/ naming conformance (function-named kebab-case, R2 §2.1 `:139`)

| Ref file | Kebab-case | Function-named | H1 title |
|----------|-----------|----------------|----------|
| `augment-poll.md` | yes | yes (poller contract) | `# Augment Poll (C2) — the poller contract` |
| `detection-contract.md` | yes | yes (DET constant) | `# Detection Contract (DET) — the build-gated locked constant` |
| `finding-verify.md` | yes | yes (verify-before-remediate) | `# Finding Verify (C3a) — verify-before-remediate, by reference` |
| `loop-guard.md` | yes | yes (LG counter) | `# Loop Guard (LG) — INV-001 round-counter + the §11 run-log schema` |
| `severity-routing.md` | yes | yes (C3 routing) | `# Severity Routing (C3) — re-grade by reference, then route to troubleshoot` |
| `state-machine.md` | yes | yes (FSM) | `# State Machine (FSM) — the single source for all --monitor ordinals` |
| `thread-reply.md` | yes | yes (C4 reply/resolve) | `# Thread Reply + Resolve (C4) — the reply/resolve contract` |
| `troubleshoot-dispatch.md` | yes | yes (C3b dispatch) | `# Troubleshoot Dispatch (C3b) — seed verified findings to /sc:troubleshoot` |

D-result: all 8 refs PASS — kebab-case, function-named, each carries a focused `# H1` title (R2 §2.3). All 8 are lazy-loaded by SKILL.md waves (see A5), none pre-loaded.

---

## Adversarial sweep (the ≥10-error hypothesis)

Specifically hunted for each failure mode named in the spawn prompt; none found:

| Suspected error | Verdict | Why not present |
|-----------------|---------|-----------------|
| Missing Activation in command | NOT FOUND | `pr-submit.md:59` + `:62` blockquote present (B3/B4). |
| Wrong frontmatter flavor (SKILL full-YAML / command HTML-comment) | NOT FOUND | SKILL = Flavor-A (A1); command = full-YAML (B1) — correctly opposite. |
| Eager (pre-loaded) ref loading | NOT FOUND | `:70` "LAZY-loaded per wave, never pre-loaded"; per-wave Load verbs (A5). |
| Missing SoT comment in a script | NOT FOUND | both scripts `:16` (C2). |
| Wrong `name:` (command `sc:pr-submit` / SKILL bare) | NOT FOUND | SKILL `sc:pr-submit-protocol` (A2); command bare `pr-submit` (B2). |
| Missing `Bash(gh *)`/`Bash(git *)` scope | NOT FOUND | `SKILL.md:4` (A3). |
| Missing shebang / set -euo / die / command -v | NOT FOUND | C1–C5 all PASS both scripts. |
| Non-kebab / non-function ref name | NOT FOUND | D — all 8 conform. |
| Blockquote skill-id ≠ SKILL name | NOT FOUND | `> Skill sc:pr-submit-protocol` (B4) == `name: sc:pr-submit-protocol` (A2). |
| Missing argument-hint / Triggers | NOT FOUND | B5 (`:8`), B7 (`:14-20`). |

Adversarial result: 0 confirmed template-conformance defects across 22 checks (A1–A7, B1–B7, C1–C6, D). Tool-call count (Read 6 incl. self-readback, Bash 3, Grep via Bash) >= checklist items — not padded.

---

## Items Reviewed Summary

- Checks passed: 22 / 22 (A:7, B:7, C:6, D:1 aggregate over 8 refs)
- Checks failed: 0
- Critical: 0 | Important: 0 | Minor: 0

## Issues Found

None. All template-conformance checks PASS.

## Notes (non-blocking, NOT findings)

- The R2 research recommended directory `sc-submit-pr-protocol` / command `submit-pr`; the build standardized on `sc-pr-submit-protocol` / `pr-submit` (matching the qa-input-manifest-gateB.md inventory, lines 21/41). This is an internal naming decision, consistently applied across the dir name, `name:` fields, command file, and the `> Skill` blockquote — NOT a conformance defect. Flagged only so a downstream lens reconciling against R2 prose does not mistake it for drift.

---

## VERDICT: PASS
