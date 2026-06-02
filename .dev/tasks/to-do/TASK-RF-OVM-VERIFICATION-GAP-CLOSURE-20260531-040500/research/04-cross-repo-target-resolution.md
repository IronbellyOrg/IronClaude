# Research: Cross-Repo Target Resolution (BLOCKER-CLOSER)

**Topic type:** Patterns & Conventions / Cross-repo target binding
**Scope:** `/config/workspace/Coder/` vs `/config/workspace/IronClaude/`
**Status:** Complete
**Date:** 2026-05-31

---

## Background

Researchers R1, R2, R3 independently surfaced the same blocker: the SuperClaude framework files (`src/superclaude/`, `Makefile`, `.dev/eval-workspaces/sc-reflect/`) do NOT exist in `/config/workspace/Coder/`. Only the live `.claude/` mirror is present.

## Resolution (orchestrator-verified)

**`/config/workspace/IronClaude/` IS the SuperClaude framework repo.** Direct verification:

| Required artifact | IronClaude path | Verified? |
|-------------------|-----------------|-----------|
| Source-of-truth SKILL.md | `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md` (140,853 bytes, sha256 `0aaef85fc8172c36ba8a2257b607018a8ed2c48718fb50b99881d35ec4d333ea`) | ✅ |
| Mirror sha256-match | `/config/.claude/skills/sc-reflect-protocol/SKILL.md` has same sha256 `0aaef85f...` | ✅ |
| Makefile `sync-dev` | `/config/workspace/IronClaude/Makefile:109` | ✅ |
| Makefile `verify-sync` | `/config/workspace/IronClaude/Makefile:166` | ✅ |
| Makefile `lint` | `/config/workspace/IronClaude/Makefile:48` | ✅ |
| Makefile `reflect-eval` | `/config/workspace/IronClaude/Makefile:493` | ✅ |
| Makefile `reflect-eval-quick` | `/config/workspace/IronClaude/Makefile:501` | ✅ |
| Eval-workspace + grader.py | `/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/` with `cases/falsifier-suite/T2-converges-on-wrong.yaml`, `T2-judge-class-collision.yaml`, `README.md`, and `grader.py` (per R3 findings: `falsifier_skeleton_present` implemented at `grader.py:270-286`, dispatched at `:405-406`) | ✅ |
| Current branch | `feat/cleanup-audit-scope-defaults` | ✅ — note: feature branch already in progress; this task may need to merge or branch off `main` |

## Task structural decision

**Execution target = IronClaude.** All Edit operations, file creations, Makefile invocations, and CI gates in the MDTM checklist will operate against `/config/workspace/IronClaude/` paths.

**Planning home = Coder.** The MDTM task file itself stays at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-OVM-VERIFICATION-GAP-CLOSURE-20260531-040500/` (where this research and the merged proposal already live). Rationale: the task is co-located with its driving artifacts (brainstorm preamble, proposals A+B, adversarial pipeline, merged proposal) so the planning trail is auditable in one tree.

## Implications for the MDTM task file

The task file MUST:

1. Declare prominently in its frontmatter or first body section: `execution_repo: /config/workspace/IronClaude/` and `planning_repo: /config/workspace/Coder/` (or equivalent fields per template 02 frontmatter — `related_docs` with annotations is one valid encoding).
2. First checklist item: `cd /config/workspace/IronClaude && git status && git rev-parse HEAD` to verify the executor is in the right repo and capture pre-task SHA.
3. Decide branch strategy in an early checklist item: the IronClaude current branch is `feat/cleanup-audit-scope-defaults`. The executor must either (a) branch off `main` into a new `feat/ovm-verification-gap-closure-20260531` branch, or (b) confirm with user. Recommended: (a) — OVM is independent of cleanup-audit scope defaults.
4. All Edit operations target `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md` (NOT the `.claude/` mirror).
5. After Edits: `cd /config/workspace/IronClaude && make sync-dev && make verify-sync` as the project's canonical sync verification.
6. Final CI gates: `cd /config/workspace/IronClaude && make lint && make reflect-eval-quick` (per R2 findings, these are real targets).
7. Reference to merged proposal stays at `/config/workspace/IronClaude/.dev/brainstorm/reflect-verification-gap-20260531/MERGED-PROPOSAL.md`. The executor reads it from Coder but writes outputs to IronClaude.

## Falsifier eval-case decision (per R3 W-A8 / Path A vs Path B finding)

R3 flagged: merged proposal §7.1 says `status: active` for the docker-cli-miss falsifier, but the IronClaude eval-workspace's W-A8 precedent uses skeleton-pending. The merged-proposal direction (active iteration-1) is the authoritative debate outcome (debate-transcript.md C-012 winner: A's "active immediately is right because the docker miss is real, not hypothetical"). The task file MUST instruct the executor to write the docker-cli-miss case as `status: active` per merged §7.1, accepting that it diverges from the W-A8 skeleton-first pattern. The sibling `outcome-verification-deferred-runtime-config.yaml` may remain `status: skeleton-pending-iteration-3-fixture` per merged §7.2 (the deferred-runtime case is a placeholder for V-Deferred-Outcome mode coverage, which has no real-world incident driving it yet).

## STRICT-tier encoding decision (per R2 finding)

R2 confirmed: there is no frontmatter field named `compliance_tier:` / `task_tier:` / `tier:` in MDTM template 02. STRICT is a runtime annotation emitted by `/sc:task` as an HTML comment block. For this task:
- Frontmatter uses standard template 02 fields (no tier field).
- A prose marker in the Task Overview section: "**Compliance tier: STRICT** — multi-file protocol-text amendment with §9.3 consumer-field-map impact. Per the /sc:task classifier rules, this task warrants STRICT enforcement when executed."
- Execution Log section to be annotated by the executor with `<!-- SC:TASK-UNIFIED:CLASSIFICATION strict -->` if executed via `/sc:task`; if executed via plain `/task`, the prose marker stands.

## All blockers closed

- ✅ Cross-repo target identified and verified.
- ✅ Makefile target availability confirmed (lint, sync-dev, verify-sync, reflect-eval, reflect-eval-quick — all present at IronClaude Makefile).
- ✅ Eval-workspace infrastructure confirmed at IronClaude (grader.py + `falsifier_skeleton_present` assertion ready).
- ✅ STRICT-tier encoding resolved (prose marker, not frontmatter field).
- ✅ Falsifier case status decision (active for docker case per merged §7.1; skeleton for sibling per merged §7.2).
- ✅ Branch strategy decision (executor branches off IronClaude main).

The builder can now produce a fully-specified, unambiguous MDTM task file. No further user input required.

## Summary

| Aspect | Resolution |
|--------|-----------|
| Execution target | `/config/workspace/IronClaude/` (all paths, all commands) |
| Planning home | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-...` (task file lives here) |
| Edit target | `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md` (source of truth) |
| Sync | `cd /config/workspace/IronClaude && make sync-dev && make verify-sync` |
| CI gates | `make lint && make reflect-eval-quick` (also at IronClaude) |
| STRICT marker | Prose in Task Overview + optional HTML comment by executor |
| Branch | Executor branches off IronClaude `main` into a new feature branch |
| Falsifier status | docker case `active`; sibling case `skeleton-pending-iteration-3-fixture` |
