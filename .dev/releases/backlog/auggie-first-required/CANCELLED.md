# auggie-first-required — CANCELLED

**Cancellation date:** 2026-05-18
**Cancelled by:** RyanW (project maintainer)
**Original target:** PreToolUse Bash gate that would block actionable verbs when the `auggie-first` sticky is present, preventing the user from invoking shell commands before consulting auggie.

## Rationale (verbatim from maintainer 2026-05-18)

> "we went through a lot of back and forth and then I decided on a simpler solution for now where we just rely on memory before doing a bunch of work and overcomplicating things"

A behavioral / memory-based auggie-first convention (the existing `auggie_first_required=1` session-context flag + the v2.1 PostToolUse `auggie-flag-clear.sh` reactive system) was judged sufficient for the current need. The PreToolUse Bash gate was determined to be over-engineering for the present moment.

## What remained on disk at cancellation time

By the time the cancellation decision was made, this release directory had already been emptied (likely via an interactive `rm` or `git clean -fd` during heavy task-builder pipeline work on 2026-05-17). The only surviving artifacts of the original release effort were:

1. `.claude/hooks/auggie-bash-gate.sh` (62 LOC PreToolUse Bash gate, gitignored location, never committed to any branch). **Disposition:** archived to `.dev/releases/complete/auggie-first/auggie-bash-gate-archived-2026-05-18.sh` and deleted from `.claude/hooks/` per the 2026-05-18 cleanup (OQ-2 resolution in PR #49's follow-up).
2. `tests/hooks/__pycache__/test_auggie_bash_gate.cpython-312-pytest-9.0.3.pyc` (orphaned bytecode; source `.py` was deleted with the release directory). **Disposition:** deleted in the same cleanup.
3. Three dangling commits by RyanW from 2026-05-17 17:57-18:00 UTC (`9d31e4c`, `a759ce7`, `9920456`) containing the registration deltas (`install_hooks.py +1`, `hooks.json +10`). These were orphaned via branch reset during `task-merge consolidation` work and are unreachable from any branch.

## Where the design body lives now

The archived script body at `.dev/releases/complete/auggie-first/auggie-bash-gate-archived-2026-05-18.sh` preserves the verb list, the sticky-detection logic, the JSONL `gate_blocked` event schema, and the dual escape-hatch convention. If a future release decides to ship a Bash gate, the recovery path is documented in the archive file's header comment.

## Discovery context

The orphaned `.claude/hooks/auggie-bash-gate.sh` was first surfaced by the new `=== Hooks ===` reverse-check in `make verify-sync` introduced by the `hook-sync-and-matcher-fix` release (PR #49, merged 2026-05-18 11:43:55 UTC). It was tracked as Open Question OQ-2 in that release's PR description and resolved here.

## Why this entire release directory was moved to backlog/ instead of complete/

`.dev/releases/complete/` is reserved for releases that shipped to master. `.dev/releases/backlog/` is the appropriate destination for releases that were cancelled / scoped out before shipping. The release directory's contents had already been wiped before cancellation became formal, so the move preserves the directory name as a historical breadcrumb without implying the work was completed.
