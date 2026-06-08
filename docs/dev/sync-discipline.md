# Source-of-Truth Sync Discipline

> **Status:** Phase 1 reference doc for the MultiModelSwarm release (T01.05 /
> R-005 / AC-019). Applies to every contributor touching skills, agents,
> commands, hooks, or templates — not just the swarm surface.

## The rule

**Edit `src/superclaude/`, then run `make sync-dev`. Never edit `.claude/`
directly.**

`src/superclaude/` is the canonical source of every distributable component.
The `.claude/` tree in this repo is a generated mirror that exists only so
Claude Code can load skills, agents, and commands during local development.
The upstream installer (`superclaude install`) regenerates `.claude/` from
`src/`, and the same convention is enforced inside the repo by `make
verify-sync` and a pre-commit gate.

This is the project-wide rule documented in
[`CLAUDE.md`](../../CLAUDE.md#-component-sync) (§ "Component Sync") and in
the user-global `~/.claude/CLAUDE.md`. T01.05 codifies the same rule for
the swarm contribution surface so AC-019 has a doc anchor.

## What lives where

| Path | Role |
|------|------|
| `src/superclaude/skills/<name>/` | Source — edit here. |
| `src/superclaude/agents/*.md` | Source — edit here. |
| `src/superclaude/commands/*.md` | Source — edit here. |
| `src/superclaude/hooks/scripts/*.sh` | Source — edit here. |
| `src/superclaude/templates/**` | Source — edit here. |
| `.claude/skills/<name>/` | Generated mirror — do not edit. |
| `.claude/agents/*.md` | Generated mirror — do not edit. |
| `.claude/commands/sc/*.md` | Generated mirror — do not edit. |
| `.claude/hooks/*.sh` | Generated mirror — do not edit. |
| `.claude/templates/**` | Generated mirror — do not edit. |
| `.claude/settings.json` | **Tracked** — project hook/permission registry. The only exception. |

Everything under `.claude/{skills,agents,commands,hooks,templates}/` is
gitignored output. `.claude/settings.json` is the sole tracked file under
`.claude/` and is hand-authored, not regenerated.

## The contributor workflow

1. **Edit the source.** Open the file under `src/superclaude/…` and make the
   change.
2. **Sync.** Run `make sync-dev`. This copies `src/superclaude/{skills,
   agents,commands,hooks,templates}` into `.claude/` so Claude Code picks up
   your edits in this session.
3. **Verify.** Run `make verify-sync`. It must exit 0 before you stage
   anything. Drift means you either edited a mirror directly or forgot
   step 2 — fix the source under `src/`, re-run `make sync-dev`, and
   re-verify.
4. **Stage only `src/`.** Never `git add` any path under
   `.claude/{skills,agents,commands,hooks,templates}/`. The `.gitignore` and
   the pre-commit hook below will reject those paths anyway; staging them
   is the bug, not their rejection.

## If you accidentally edited `.claude/` first

It happens — Claude Code reads from `.claude/` and the iteration loop can
land changes there. Recover with:

1. Copy the edited files from `.claude/<path>` back to the matching
   `src/superclaude/<path>`.
2. Run `make sync-dev` so the mirror is regenerated from the (now-correct)
   source.
3. Run `make verify-sync` — it should be clean.
4. Stage only the `src/` side.

Do **not** run `git add -f` on a `.claude/` path to "fix" the situation.
That `-f` is the violation siren documented in `CLAUDE.md` ("ABSOLUTE
RULE: Never Stage or Commit `.claude/` Contents"). Stop and move the
change to `src/`.

## Enforcement gates

The discipline above is backed by three mechanical gates. If any of them
trip, do exactly what they say — never strategy-pivot around them.

### 1. `make verify-sync`

Diffs every `src/superclaude/<component>/` tree against its `.claude/`
counterpart and exits 1 on drift. Used as the CI-friendly sync check and
referenced as the smoke verification for several Phase 1 tasks (T01.01,
T01.03, T01.05 itself). Always passes on the first run after a clean
`make sync-dev`.

### 2. Pre-commit hook — `block-claude-generated-mirrors`

Lives in [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) under
the `AC11 / R-017 / T01.20` section (see also
[`scripts/precommit_block_claude_mirrors.sh`](../../scripts/precommit_block_claude_mirrors.sh)).
It fails any commit that stages a path under
`.claude/{skills,agents,commands,hooks,templates}/`, prints the offending
paths, and reminds you that `.claude/settings.json` is the only allowed
exception. This is the sync-discipline pre-commit gate referenced in
AC-019.

### 3. `.gitignore`

`.claude/` is gitignored except for `.claude/settings.json`. This catches
most accidental stagings before they reach the pre-commit layer.

## Cross-references

- [`CLAUDE.md` § Component Sync](../../CLAUDE.md#-component-sync) — the
  project-wide source-of-truth rule that this doc enforces for swarm
  contributions.
- [`CLAUDE.md` § ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents](../../CLAUDE.md#absolute-rule-never-stage-or-commit-claude-contents)
  — the `-f` siren and the only exception (`.claude/settings.json`).
- [`docs/swarm/runbook.md`](../swarm/runbook.md) — the swarm operator
  runbook (AC-001 UV mandate).
- [`Makefile`](../../Makefile) — `sync-dev` and `verify-sync` targets.
