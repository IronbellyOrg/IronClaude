---
schema_version: "1.0"
topic: "improving onboarding workflow for new contributors"
domain: process
strategy: agile
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-05-27T00:00:00Z
intent_summary: "Reduce friction for new open-source contributors so they can submit their first meaningful PR quickly, while keeping maintainer review overhead manageable. Apply agile, iterative improvements rather than a top-down redesign."
context_anchors:
  - "Existing CONTRIBUTING.md and docs/ already present in repository"
  - "Project uses UV for Python operations; new contributors often hit environment setup friction"
  - "Pre-commit hooks (verify-sync, markdownlint) gate merges and can block first-time contributors"
  - "Slash command + skill architecture has steep conceptual learning curve"
  - "Target audience: open-source contributors, varying experience levels, async global timezones"
must_preserve:
  - "Existing pre-commit quality gates (verify-sync, lint, format) — non-negotiable"
  - "Branch discipline: feature/* off integration, never direct commits to master"
  - "Source-of-truth rule: edit src/superclaude/, sync via make sync-dev"
  - "Conventional commit message format"
  - "PM Agent confidence-check workflow for non-trivial contributions"
out_of_scope:
  - "Paid or enterprise-only onboarding tracks"
  - "Mandatory synchronous mentoring (project is async-first)"
  - "Rewriting CONTRIBUTING.md from scratch (iterative improvement only)"
  - "Changing core architectural decisions to ease onboarding"
  - "Implementing a new auth/identity system for contributors"
source_confidence: medium
defaults_applied:
  - "Non-interactive mode: auto-proceeded with project-context-derived defaults"
  - "Audience assumed: external OSS contributors with mixed Python/CLI experience"
  - "Success metrics assumed: time-to-first-PR, drop-off rate at setup, contributor return rate"
  - "Tooling assumed in-scope: docs, scripts, CI, issue templates, labels, mentorship pairing"
---

# Seed Brief: Improving Onboarding Workflow for New Contributors

## Intent Summary

Reduce friction for new open-source contributors so they can submit their first meaningful PR quickly, while keeping maintainer review overhead manageable. The goal is incremental, agile improvements layered onto the existing CONTRIBUTING flow — not a redesign. Target outcomes: faster time-to-first-PR, lower drop-off at environment setup, higher contributor retention (return for a second contribution).

The brainstorm should surface concrete, shippable-in-one-sprint improvements that respect the project's source-of-truth discipline, pre-commit gates, and async-first culture.

## Context Anchors

- Repository already has `CONTRIBUTING.md`, `CLAUDE.md`, `KNOWLEDGE.md`, and `docs/` covering high-level architecture and workflow rules.
- Python toolchain is UV-only — new contributors using vanilla `pip`/`python -m` hit immediate friction.
- `make sync-dev` and `make verify-sync` are mandatory before commits touching `src/superclaude/`; failure modes are non-obvious to first-timers.
- Pre-commit hooks (verify-sync, markdownlint, freshness-pre-edit) reject commits without clear remediation guidance for newcomers.
- The skill + slash-command architecture (`.claude/skills/`, `src/superclaude/skills/`) is conceptually unique and not documented from a "first 30 minutes" lens.
- Async-first global community: timezone-spanning, no synchronous standups, contributor mentorship must be self-service.
- Existing labels (`good-first-issue`, `help-wanted`) likely under-curated; issue templates may not match agile sprint cadence.

## Must Preserve

- Pre-commit quality gates: verify-sync, ruff lint/format, markdownlint, freshness checks.
- Branch discipline: feature/fix/docs branches off `integration`, never direct to `master`.
- Source-of-truth rule: all distributable content edited in `src/superclaude/`, then `make sync-dev` to `.claude/`.
- Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`).
- PM Agent confidence-check pattern for medium/complex contributions.
- UV-only Python operations; no `pip install`, no `python -m`.
- `.claude/` gitignore rule — never stage skills/commands/agents/hooks directories.

## Out of Scope

- Paid contributor tracks, sponsored onboarding, or enterprise-tier flows.
- Mandatory synchronous mentoring or scheduled office hours (async-first principle).
- Wholesale rewrite of `CONTRIBUTING.md` — only additive, iterative edits.
- Loosening any quality gate (verify-sync, lint, markdownlint) to ease onboarding.
- Introducing a new contributor identity/auth system beyond GitHub OAuth.
- Restructuring `src/superclaude/` package layout for newcomer convenience.
- Building a custom contributor portal app — out of scope for an agile sprint.
