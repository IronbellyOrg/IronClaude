---
topic: "improve onboarding workflow for new contributors"
domain: process
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
created: 2026-05-25T19:30:57Z
---

# Seed Brief: improve-onboarding-workflow-for-new-contributors

## Problem Statement

New contributors to the SuperClaude / IronClaude framework face a steep, undocumented ramp: environment setup (UV + pipx + Make), the src/.claude sync model, multi-surface mental model (skills, commands, agents, hooks), and project-specific workflows (worktrees, MDTM tasks, pipelines). The implicit knowledge required to make a non-trivial first contribution is not captured in a single canonical onboarding path, producing friction, abandoned PRs, and repeat clarifying questions to maintainers.

## Known Context

- Project uses **UV** exclusively for Python — `python -m`/`pip install` are forbidden (CLAUDE.md rule 1).
- **Source-of-truth discipline**: `src/superclaude/` is canonical; `.claude/` is gitignored sync-dev output (only `.claude/settings.json` is tracked).
- New contributors typically encounter: skills loading model, agent definitions, slash-command files, pytest plugin auto-loading, hook system, MCP servers (auggie/serena/sequential/context7/tavily), Make targets (`make dev`/`sync-dev`/`verify-sync`).
- Worktree-based parallel development is the recommended pattern.
- CLAUDE.md (both global + project) is dense and assumes prior context.
- KNOWLEDGE.md exists for accumulated insights but isn't a guided onboarding path.
- Current "onboarding" surface = README + CLAUDE.md + scattered docs — no end-to-end first-contribution walkthrough.

## Constraints

- Cannot change the underlying SoT model (src → sync-dev → .claude is non-negotiable).
- Must respect "UV-only" Python rule.
- Cannot commit `.claude/skills,commands,agents,hooks` artifacts — onboarding docs must explain this rule, not violate it.
- Solo-maintainer reality: onboarding improvements must be self-maintaining (low-overhead, ideally auto-checked).
- New-contributor audience varies wildly in seniority (senior engineers vs students); the path must avoid being either condescending or impenetrable.
- No external onboarding platform — must live in-repo (markdown, scripts, Make targets) for discoverability + version control.

## Success Criteria

- A first-time contributor can land a small, meaningful PR (e.g., a doc fix, a skill tweak, a test) within their first session without a maintainer DM.
- The first 30 minutes of contributor experience produces a working dev environment + a verified `make test` green run + understanding of where to edit (src/, not .claude/).
- Common confusion points (SoT discipline, UV vs pip, worktree pattern, sync-dev rule) each have a single canonical answer that's discoverable in ≤2 clicks from README.
- Friction signals (repeated maintainer questions, abandoned setup attempts, `git add -f .claude/...` violations) trend down over the next 90 days.
- Onboarding artifacts are testable / verifiable in CI (e.g., a `make onboard-check` that exercises the documented happy path).

## Open Questions

- Should onboarding be linear (one canonical CONTRIBUTING.md path) or contextual (multiple entry points by contribution type — docs vs skill vs agent vs CLI feature)?
- Is the priority preventing setup failure (env, sync, UV), or accelerating conceptual understanding (skill model, agent model, MCP wiring)?
- Where should the onboarding workflow live — CONTRIBUTING.md, a `docs/contributing/` folder, a `superclaude onboard` CLI command, or an interactive bootstrap script?
- Is there appetite for an automated "first-PR sandbox" (a curated `good-first-issue` template + scaffolded task file) vs. trusting docs alone?
- Should the workflow integrate with the existing skills system (i.e., a `skill: contributor-onboarding`) so it's discoverable from the same surface contributors will eventually maintain?
- What's the maintainer's tolerance for ceremony — a single CONTRIBUTING.md update, or a multi-artifact onboarding system (docs + scripts + Make targets + hook)?

## Enrichment Context

Skipped per `--no-codebase` and `--no-research` flags. Brainstorm relies on dialogue synthesis + general framework knowledge only.
