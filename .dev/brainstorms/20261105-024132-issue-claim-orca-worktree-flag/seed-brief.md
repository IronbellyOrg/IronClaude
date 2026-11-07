---
topic: "a new version with a flag that would enable that behavor"
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-05T02:42:00+00:00
---

# Seed Brief: issue-claim-orca-worktree-flag

## Problem Statement

The topic refers to the previous finding: `/sc:issue --claim` does not use the Orca CLI and never creates a worktree. A claim assigns the issue, checks accuracy, writes `.dev/issues/<N>/next-steps.md` and stops. The user then has to open a new worktree by hand before starting the work. The goal is a new version of `/sc:issue` with an opt-in flag that makes a claim also create a new Orca-managed worktree for the issue automatically. Without the flag, behavior stays exactly as today.

"New version" is read as: the same `/sc:issue` command and `sc-issue-protocol` skill, extended additively with a flag (not a second command). Whether to also stamp an explicit version number is an open question.

## Known Context

(Dialogue answered from the command files and the earlier analysis; no `--interactive`.)

- Claim flow today: Waves 0-6 in `src/superclaude/skills/sc-issue-protocol/refs/claim.md`; it ends with "Print the `next-steps.md` path and STOP" (Wave 6 step 4).
- Hard boundary today: `commands/issue.md` "Will Not: Run any next-step command"; protocol rule B2.
- Existing flag-scope pattern: `--depth/--mode/--type` with `--claim` is STOP `E-CREATE-ONLY-FLAG`. A claim-only flag would mirror that for `--create`.
- `orca worktree create` already supports: `--name`, `--repo`, `--base-branch`, `--branch`, `--parent-worktree` / `--no-parent`, `--setup run|skip|inherit`, `--agent`, `--prompt`, `--model`, `--effort`, `--surface`, `--activate`, `--comment`, `--json`, `--retry-launch`. It repeats a numeric suffix when a name is taken.
- Project rules: worktrees only through Orca at its default location (never raw `git worktree add`, never `EnterWorktree`); never pass Orca link flags (`--issue`, `--pr`, and in practice `--reference` with a GitHub URL) for this repo, because Orca resolves this project to the upstream `SuperClaude-Org` id.
- `.dev/issues/<N>/` is never staged or committed (default D24), so a fresh worktree will not contain `next-steps.md` or `issue-summary.md` unless they are copied or referenced by absolute path; the next-step commands use repo-relative `@.dev/issues/<N>/issue-summary.md`.

## Constraints

- Default behavior (no flag) must be byte-for-byte unchanged; the flag is claim-only and opt-in.
- Worktree creation goes through `orca worktree create` only, with no Orca link flags and no upstream interaction.
- A claim must never fail or roll back because worktree creation failed; assignment and comments are already done by then (fail open with a clear message).
- Re-claiming the same issue must not create a duplicate worktree.
- Primitives are edited under `src/superclaude/` then `make sync-dev`; no `src/superclaude/` paths inside installed primitives; the plugin mirror and tests that pin the command/skill must stay in sync.
- More than 5 edits across files: implementation must go through a written plan (`/sc:workflow`), not direct edits.

## Success Criteria

- `/sc:issue --claim <N> <new flag>` ends with an Orca worktree for the issue that exists on disk at Orca's default location, on a new branch based on the default branch, and the final output prints its path.
- The new worktree can open and read the issue summary and next steps (files copied or path given), verified by an observed run.
- `/sc:issue --claim <N>` without the flag produces the same outputs as before.
- `--create` with the new flag STOPs with a clear error; Orca missing or failing yields a warning, not a failed claim.
- Tests pin the flag parsing, the exact `orca worktree create` argument list (no link flags) and the idempotent re-claim path.

## Open Questions

- Worktree only, or also launch an agent in it (`--agent --prompt`)? Launching an agent that runs the chain collides with B2 ("never run a next-step command").
- Flag name and shape: `--worktree`, `--orca`, `--launch`, or one flag with a value (`--worktree [name]`)?
- Branch and worktree naming (`issue-<N>-<slug>`), base ref (default branch `<B>`), and parent lineage (`--no-parent` vs inferred).
- How the new worktree gets `.dev/issues/<N>/` (copy, symlink, or absolute path in the prompt).
- Duplicate detection on re-claim (`orca worktree list` lookup by branch or name) and what to do if it exists.
- Which model/effort and tier line the launched agent gets, if any.
- Whether to add an explicit version marker to the command and skill.

## Enrichment Context

Full artifact: `enrichment/codebase-context.md` (codebase: primary; research: skipped, Orca is already in the project and its `--help` was read live).

- B2 ("claim stops after writing next-steps.md") is a ruled design decision (`docs/designs/sc-issue-command.md:27`), not just a code habit. No existing test mentions Orca or worktrees for `/sc:issue`.
- `orca worktree create` by default makes the worktree plus a terminal and starts no agent; `--agent`/`--prompt` start one. The repo's own precedent (refactor decision D3) creates worktrees **without** `--agent`.
- `.dev/issues/<N>/` is untracked, so a worktree built from the default branch will not contain the claim output; it must be copied or referenced by absolute path.
- Unverified: whether `--setup run` runs `make sync-dev` (the new worktree's `.claude/` copy may be missing), and whether `/sc:issue` may run inside an Orca-launched tab (worker contract).
