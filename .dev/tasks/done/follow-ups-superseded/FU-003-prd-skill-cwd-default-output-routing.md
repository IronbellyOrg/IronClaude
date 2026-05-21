---
id: "FU-003-prd-skill-cwd-default-output-routing"
title: "PRD skill writes dry-run output to repo root instead of .dev/eval-workspaces/"
status: "🟡 To Do"
type: "🐛 Bug"
priority: "🔼 High"
created_date: "2026-05-18"
parent_task: "TASK-RF-20260518-181333"
tags:
- "follow-up"
- "root-cause-fix"
---

## Background

Phase 1 of TASK-RF-20260518-181333 surfaced stray repo-root directories `prd-test-product/` and `prd-dry-run-test/` containing `execution-log.md` files. These are output artifacts of the PRD skill's dry-run / test paths. They should NEVER land at the repo root — the expected destination is under `.dev/eval-workspaces/<skill-name>/` per the CLAUDE.md "Plugin Override — Skill-Creator Workspace Destination" convention.

## Symptom

Running PRD-skill in dry-run / test mode leaves output directories at the repo root instead of routing them to `.dev/eval-workspaces/`. CLAUDE.md addendum already documents the intended convention but the skill code doesn't honor it. The Phase 3 cleanup (commit `fe11bd8`) added `.gitignore` guards as a retroactive safety net, but the skill itself still writes to the wrong location on every run.

## Root Cause Hypothesis

The PRD skill's output-path resolution defaults to `os.getcwd()` (or equivalent) when no `--output` flag is specified, AND the skill doesn't check whether the resolved path is the repo root. The PRD skill code (likely in `src/superclaude/skills/prd/` if it exists, or as a slash-command resolver) treats CWD as the output destination unconditionally — there is no guard rerouting writes that would land at the repo root.

## Suggested Fix Direction

- Locate the PRD skill's output-path resolver (`src/superclaude/skills/prd/` and/or `.claude/skills/prd/SKILL.md`).
- Add a guard: if the resolved output path would land outside `.dev/` (especially at the repo root), redirect to `.dev/eval-workspaces/prd-<slug>/`.
- Add a PreToolUse hook (similar to existing `reject-workspace-writes.sh`) that rejects writes to `<repo-root>/prd-*-test/`, `<repo-root>/prd-*/`, etc. with a redirect message.
- Sync changes via `make sync-dev` and verify with `make verify-sync`.

## Acceptance Criteria

- PRD dry-run / test mode without explicit `--output` writes to `.dev/eval-workspaces/<slug>/` not to repo root.
- The `.gitignore` guards from commit `fe11bd8` become redundant for new runs (kept as defense-in-depth).
- An automated test or hook prevents writes to `/prd-*/` at the repo root.
- CLAUDE.md "Plugin Override" convention applies uniformly across skill-creator AND prd skills.

## References

- PRD skill source: `src/superclaude/skills/prd/` and `.claude/skills/prd/`
- Existing reject-workspace-writes.sh pattern: `.claude/hooks/reject-workspace-writes.sh`
- Phase 3 cleanup commit: `fe11bd8`
- CLAUDE.md "Plugin Override — Skill-Creator Workspace Destination" section
- Parent task: `TASK-RF-20260518-181333`
