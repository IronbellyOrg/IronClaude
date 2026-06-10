# Phase 7 pipx install + --help (Step 7.2, NFR-5)

**Date:** 2026-06-10

## Install vector

`pipx install --force /config/workspace/IronClaude/.claude/worktrees/reflectWrapper`

**Path note:** installed from THIS worktree (which carries the reflect CLI), NOT the literal
`/config/workspace/IronClaude` master worktree — `git ls-tree origin/master -- src/superclaude/cli/reflect/`
is EMPTY, so master would not expose `reflect run` (per the canonical-base correction + worktree discipline).

Result: `installed package superclaude 4.3.5` ... `done! ✨` — globally available: `superclaude`, `SuperClaude`, `ic`.

## `superclaude reflect run --help` (resolves — NO "no such command")

New flags exposed (NFR-5 satisfied):

- `--fix / --no-fix` — "Run the bounded audit->apply->re-verify auto-fix loop (gate default --fix)."  ✅
- `--max-fix-iterations INTEGER` — "Max apply->verify cycles before terminal HALT (D3, default 2)."  ✅
- `--base TEXT` — "Explicit audit base ref (single ref vs working tree). Highest precedence over frontmatter start_commit + merge-base."  ✅
- `--promote / --no-promote` — "Allow reflect's gated Wave-7 promotion (default: --promote). O2 callers pass --no-promote."  ✅ (default flipped to --promote)

Existing flags retained: `--tmux`, `--print-command`, `--timeout`, `--depth`, `--output`,
`--allow-single-vendor`, `--dry-run`, `--resume`. No `--model`/`--max-turns` added (FR-7 honored).

**NFR-5 met:** the evolved `superclaude reflect run` is `pipx install --force`-able with the new flags
and resolves on PATH — ready BEFORE the companion generator worktree's O1/O2 gates go live.
