---
topic: "the best way to re-write sc:implement according the objectives above and the findings and best practices from the references"
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-09-24T19:27:15Z
---

# Seed Brief: sc-implement-rewrite

## Problem Statement

`/sc:implement` is a persona/MCP behavioral mode that invents and writes a feature from free-form text. Completion is "compiles + basic functionality + ready for `/sc:test`". That is the wrong job.

The command must become a **middleweight executor**: given a spec, PRD, or simple tasklist (never a blank feature pitch), walk the tasks, and after each task verify **actual completion against that task's acceptance criteria, spec, and instructions**. Lint + `npm test`/typecheck are cheap extras, never the pass/fail. This is a simpler ledger than `/task` (no 6-agent phase gates, no MDTM ceremony).

After this brainstorm produces merged requirements, the user will invoke `/sc:improve` to rewrite `/sc:implement` accordingly.

## Known Context

- SoT file: `src/superclaude/commands/implement.md`. No protocol skill exists. No `## Activation`. Modern `/sc:*` commands (reflect, brainstorm, auggie-review) are thin dispatchers that MUST invoke `Skill sc:<name>-protocol`. `make lint-architecture` Check 1 requires a matching skill directory once Activation is added (`sc-implement-protocol` or `sc-implement`). Edit `src/` then `make sync-dev`.
- Current flow: Analyze → Plan → Generate → Validate → Integrate. Flags: `--type`, `--framework`, `--safe`, `--with-tests`. Personas + Context7/Magic/Sequential/Playwright. Done when code compiles and is "ready for testing".
- `/task` F1 loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT) plus 6-agent phase-gate QA is the **heavy** ledger. Out of scope to import.
- Session research (GitHub API + raw SKILL.md, 2026-09-24):
  - **mattpocock `implement`**: requires spec/tickets; TDD at seams; **full suite once + `/code-review` once**. No per-task spec QA. Wrong shape.
  - **Superpowers `executing-plans`**: plan+spec required; per-task TDD + `Expected:` vs output; one-line SDD ledger; **no reviewer per task**; one whole-branch review. Test-runner-shaped gate — user rejected as primary QA (useless for ~90% of tasks).
  - **Superpowers `subagent-driven-development`**: same ledger; fresh implementer per task; **task reviewer Part 1 = spec compliance** (Missing / Extra / Misunderstood vs the brief + global constraints); Part 2 = code quality; then whole-branch review. This is the target QA shape.
  - Cheap extras: lint + typecheck + `npm test` if present; a red suite that does not touch this task's files is not a fail.
- User constraints (this session, binding):
  1. Always require a tasklist, spec, or PRD. Never write the feature from a pitch.
  2. Primary QA = task completion vs AC + spec + instructions of **that task**.
  3. Lint + npm/typecheck are free add-ons, not the verdict.
  4. Simpler than `/task` ledger: one markdown file, one line per task.

## Constraints

- Do not import `/task` phase-gate QA (6+ agents), MDTM templates, or reflect pre/post.
- Do not use `npm test` / TDD-watched-fail as the per-task pass/fail.
- Do not keep free-form "implement this feature" as a valid invocation.
- Command stays a thin dispatcher; protocol lives in a skill (`sc-implement-protocol`).
- Source of truth is `src/superclaude/`; never commit `.claude/` skill mirrors.
- Ponytail: shortest protocol that holds. One reviewer vs the brief, not an ensemble.
- Spec is binding authority. Deviations are ledgered rulings, not silent.

## Success Criteria

- `/sc:implement` refuses to run without a path to a spec, PRD, or tasklist (STOP with usage).
- Tasks execute sequentially (or bounded-independent parallel only when the source says they are independent).
- After each task: a spec-compliance verdict (compliant | missing | extra | misunderstood | cannot-verify) against that task's AC + spec + instructions; append one ledger line; do not proceed on fail without a ledgered ruling or fix.
- Lint/typecheck/`npm test` run when available; recorded as extras; never the sole gate.
- One optional whole-list review at the end (not per-task ensemble).
- Ledger is one markdown file, resumable after compaction (first task without `complete`).
- `## Activation` + skill package + `make lint-architecture` / `make verify-sync` pass.

## Open Questions

- Tasklist format: accept a simple markdown checklist / numbered AC list, or also a SuperClaude phase-N tasklist? (Lean: any markdown with enumerable tasks + AC; do not require MDTM.)
- Reviewer: inline (same session, cheaper) vs fresh subagent (SDD-style, better isolation)? (Lean: subagent when >3 tasks or context is fat; inline otherwise.)
- Where the ledger lives: `.dev/implement/<slug>/progress.md` vs next to the spec?
- Does a 1-task spec still get the per-task reviewer, or just implement + extras + one review?
- Relationship to `/sc:task` (compliance tiers) and `/task` (MDTM): implement is the middleweight path; those remain the heavy path. No silent routing into `/task`.

## Enrichment Context

Codebase (auggie, primary): `implement.md` is a persona-mode command with no Activation/skill. Adding Activation requires `src/superclaude/skills/sc-implement-protocol/` (lint-architecture Check 1). Mirror reflect/brainstorm thin-dispatcher. Do not copy `/task` F1 or tasklist execution-log schemas.

Research (session-verified GitHub + raw SKILL.md, primary): steal Superpowers SDD Part 1 spec compliance (Missing/Extra/Misunderstood vs brief) + one-line ledger. Reject Matt end-of-batch suite+review, executing-plans TDD gate, feature-dev 7-phase, /task 6-agent QA. Lint/npm are extras.

Full artifacts: `enrichment/codebase-context.md`, `enrichment/research-light.md`.
