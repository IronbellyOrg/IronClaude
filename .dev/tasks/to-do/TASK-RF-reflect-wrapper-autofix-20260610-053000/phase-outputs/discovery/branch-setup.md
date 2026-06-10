# Branch Setup — Canonical Audit-Only Base Acquisition (Step 1.3)

**Date:** 2026-06-10
**Executor:** rf-executor (F1 loop)

## Resolved BASE_SHA

```
BASE_SHA = a5343f570e3d7cfca99ba22e42f04ab0e02d6825
```

## Source of BASE_SHA

The committed audit-only base was established by **freezing the `wrapper-onto-master`
worktree's staged-but-uncommitted audit-only CLI tree** into a new commit, per the
Step 1.3 CRITICAL BASE-ACQUISITION CORRECTION.

- **Worktree:** `/config/workspace/IronClaude/.claude/worktrees/wrapper-onto-master`
- **Branch there:** `feat/reflect-wrapper-onto-master`
- **Prior HEAD (parent of freeze commit):** `e97aa4fd2a9d317abdc19f6ce2b5ccd35497df0e`
- **Freeze commit message:** `chore(reflect): freeze audit-only base for wrapper-autofix`
- **Freeze action:** `git add -A src/superclaude/cli/reflect tests/cli/reflect src/superclaude/cli/main.py` → `git commit`
- **Staged tree captured:** 21 reflect/test files (6 `cli/reflect/*` incl. `__init__.py`, 15 `tests/cli/reflect/*`) + `cli/main.py` reflect registration.
- Note: the freeze captured the LATEST working-tree `runner.py` (blob `8736ad89`), one revision **ahead** of `reflectWrapper@ab2dae1a` (`1dcf7797`).

### Why NOT branched off `origin/master`

`git ls-tree origin/master -- src/superclaude/cli/reflect/` is **EMPTY** — `origin/master`
(`1b0264f1`) does not contain the reflect CLI at all. Branching off it would reproduce a
base with no `cli/reflect/`, making Phases 2–7 unexecutable. The corrected acquisition
roots the branch at the committed audit-only base instead.

### Ancestry note

- `git merge-base --is-ancestor 1b0264f1 a5343f57` → **NO**. origin/master is NOT a direct ancestor of BASE_SHA.
- BASE_SHA parent = `e97aa4fd` (wrapper-onto-master HEAD), which is itself an ancestor of `origin/master`.
- Therefore BASE_SHA and origin/master are **sibling lines diverging at `e97aa4fd`**: origin/master = `e97aa4fd` + later commits; BASE_SHA = `e97aa4fd` + audit-only freeze. The audit-only CLI tree on BASE_SHA mirrors the `wrapper-onto-master` staged tree exactly (the canonical base the task mandates).

## New Feature Branch

```
$ git branch --show-current
feat/reflect-wrapper-autofix

$ git rev-parse HEAD
a5343f570e3d7cfca99ba22e42f04ab0e02d6825
```

## Confirmation — rooted at the committed audit-only base

The new branch `feat/reflect-wrapper-autofix` is rooted at the committed audit-only base
(`BASE_SHA = a5343f57`, the `wrapper-onto-master` staged-tree freeze), and is **NOT** rooted at:

- ❌ `origin/master` (`1b0264f1`) — has no `cli/reflect/`
- ❌ the `reflectWrapper` dial branch (`879bb64f`, abandoned `--reflect <none|0|1|2|auto>` dial, PR #157)
- ❌ the `ReflectInTaskLists` generator branch (`9e521e2d`, `reflect/f3-hygiene-stage105-e2e`, the consumer)

## `git ls-tree HEAD -- src/superclaude/cli/reflect/` (all five `*.py` present)

```
73b5d7ce  src/superclaude/cli/reflect/__init__.py
99be3b72  src/superclaude/cli/reflect/commands.py
ad0484f4  src/superclaude/cli/reflect/config.py
dce2e01d  src/superclaude/cli/reflect/contract.py
9c6e6a4a  src/superclaude/cli/reflect/models.py
8736ad89  src/superclaude/cli/reflect/runner.py
```

All five reflect source `*.py` files (plus `__init__.py`) are present on the new base. ✅
