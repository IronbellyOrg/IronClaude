# R1 — File-Inventory / Git-Disposition Research

- **Topic:** Per-file git disposition for PR #197 "reduce-then-merge" on `feat/rf-harness-sync`
- **Scope:** Verify disposition of all 18 changed files; produce EXACT single-line git commands the tasklist embeds.
- **Status:** In Progress
- **Date:** 2026-06-28
- **CWD/worktree:** `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation`

## Baseline (verified)

```
$ git rev-list --left-right --count origin/master...HEAD
0	5            # 0 behind / 5 ahead of origin/master
$ git merge-base HEAD origin/master
cda6e2d4526c73a3d2739a3bf6efb500c4402f60
$ git rev-parse origin/master
cda6e2d4526c73a3d2739a3bf6efb500c4402f60   # == merge-base (start_commit)
$ git rev-parse HEAD
b01b33e3b2bb009e9be2da8e798e9015a5d22821
```

`start_commit` = `cda6e2d4` (origin/master tip == merge-base). origin = IronbellyOrg/IronClaude fork.

## 18-file name-status (verified)

```
$ git diff --name-status origin/master...HEAD
M	src/superclaude/agents/rf-assembler.md
M	src/superclaude/agents/rf-task-builder.md
M	src/superclaude/agents/rf-task-executor.md
M	src/superclaude/agents/rf-task-researcher.md
M	src/superclaude/agents/rf-team-lead.md
M	src/superclaude/cli/reflect/runner.py
A	src/superclaude/skills/operational-guide/SKILL.md
A	src/superclaude/skills/readme/SKILL.md
A	src/superclaude/skills/roadmap/SKILL.md
M	src/superclaude/skills/sc-reflect-protocol/SKILL.md
M	src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md
M	src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md
M	src/superclaude/skills/task-builder/SKILL.md
M	src/superclaude/skills/task/SKILL.md
M	src/superclaude/skills/tech-reference/SKILL.md
M	src/superclaude/skills/tech-research/SKILL.md
A	tests/cli/reflect/test_inline_directive.py
M	tests/cli/reflect/test_no_nesting_guard.py
```

## Per-file disposition matrix (all 18, verified)

| # | Path | Type | Disposition | Evidence |
|---|------|------|-------------|----------|
| 1 | src/superclaude/agents/rf-assembler.md | M | ACCEPT (no edit) | EXISTS on master (M) |
| 2 | src/superclaude/agents/rf-task-builder.md | M | ACCEPT (no edit) | EXISTS on master (M) |
| 3 | src/superclaude/agents/rf-task-executor.md | M | ACCEPT (no edit) | EXISTS on master (M) |
| 4 | src/superclaude/agents/rf-task-researcher.md | M | ACCEPT (no edit) | EXISTS on master (M) |
| 5 | src/superclaude/agents/rf-team-lead.md | M | ACCEPT (no edit) | EXISTS on master (M) |
| 6 | src/superclaude/cli/reflect/runner.py | M | **DROP** restore-master | EXISTS on master → `git checkout origin/master` |
| 7 | src/superclaude/skills/operational-guide/SKILL.md | A | ACCEPT (no edit) | ABSENT on master (new) |
| 8 | src/superclaude/skills/readme/SKILL.md | A | ACCEPT (no edit) | ABSENT on master (new) |
| 9 | src/superclaude/skills/roadmap/SKILL.md | A | ACCEPT (no edit) | ABSENT on master (new) |
| 10 | src/superclaude/skills/sc-reflect-protocol/SKILL.md | M | **HUNK-SURGERY** | EXISTS on master; 40-line net diff carries EV value |
| 11 | src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md | M | **REJECT** restore-master | EXISTS on master → `git checkout origin/master` |
| 12 | src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md | M | **REJECT** restore-master | EXISTS on master → `git checkout origin/master` |
| 13 | src/superclaude/skills/task-builder/SKILL.md | M | **HUNK-SURGERY** | EXISTS on master; 143-line net diff carries EV value |
| 14 | src/superclaude/skills/task/SKILL.md | M | ACCEPT (no edit) | EXISTS on master (M) |
| 15 | src/superclaude/skills/tech-reference/SKILL.md | M | ACCEPT (no edit) | EXISTS on master (M) |
| 16 | src/superclaude/skills/tech-research/SKILL.md | M | ACCEPT (no edit) | EXISTS on master (M) |
| 17 | tests/cli/reflect/test_inline_directive.py | A | **RM** (new in 197) | ABSENT on master → `git rm` |
| 18 | tests/cli/reflect/test_no_nesting_guard.py | M | **DROP** restore-master | EXISTS on master → `git checkout origin/master` |

Counts: ACCEPT=11 (5 agents + 3 new skills + task/tech-reference/tech-research), DROP-restore=2, REJECT-restore=2, RM=1, HUNK-SURGERY=2. Total=18. ✓

## Existence verification (raw)

```
$ for p in <restore targets>; do git cat-file -e origin/master:"$p"; done
EXISTS: src/superclaude/cli/reflect/runner.py
EXISTS: tests/cli/reflect/test_no_nesting_guard.py
EXISTS: src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md
EXISTS: src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md
ABSENT (expected): tests/cli/reflect/test_inline_directive.py
EXISTS: src/superclaude/skills/sc-reflect-protocol/SKILL.md   (HUNK-SURGERY target)
EXISTS: src/superclaude/skills/task-builder/SKILL.md          (HUNK-SURGERY target)
$ git ls-files tests/cli/reflect/test_inline_directive.py
tests/cli/reflect/test_inline_directive.py    # tracked on branch → rm target valid
```

## EXACT single-line commands (verified to resolve cleanly, then reset)

> All four restore/rm one-liners were dry-run executed in the worktree and then reset with
> `git checkout HEAD -- <paths>`; final `git status --porcelain` over those paths = CLEAN.

### Step 2 — DROP (restore reflect-runner + nesting-guard test to master, rm new test)

Restore one-liner:

```
git checkout origin/master -- src/superclaude/cli/reflect/runner.py tests/cli/reflect/test_no_nesting_guard.py
```

Remove one-liner (new-in-197 test):

```
git rm tests/cli/reflect/test_inline_directive.py
```

### Step 3 — REJECT refs (restore reviewer-spec + reflection-rubric to master)

```
git checkout origin/master -- src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md
```

Both `git checkout origin/master -- …` invocations returned `RESTORE-OK` (exit 0, no error). NOTE:
the `--source=origin/master` form is INVALID git syntax (`error: unknown option`) — embed only the
canonical positional `<tree-ish> -- <paths>` form above.

## Sanity checks (Task 3)

- **ACCEPT files need NO git restore.** All 11 stay as-is on the branch. The 5 agents + task/tech-reference/tech-research are `M` (exist on master, kept as branch versions); the 3 new skills (operational-guide, readme, roadmap) are `A` (absent on master) and are kept. None are touched by any restore command.
- **HARD WARNING — HUNK-SURGERY files must NOT be full `git checkout origin/master`.** `skills/sc-reflect-protocol/SKILL.md` (40 net lines) and `skills/task-builder/SKILL.md` (143 net lines: 132 ins / 51 del) carry net-new EV value. A full `git checkout origin/master -- <those>` would DESTROY that value and collapse the entire reduce-then-merge premise. These two files are surgically edited only (R2 covers reflect SKILL.md hunks; R3 covers task-builder clause flip). The tasklist MUST NOT list either path in any `git checkout origin/master` one-liner.

## `.claude/` mirror risk (Task 4)

- All edits are in `src/superclaude/` (source of truth) only. After edits run `make sync-dev` to regenerate `.claude/`.
- `.claude/skills/sc-reflect-protocol/SKILL.md` is **gitignored** (`git check-ignore` → IGNORED). Only `.claude/settings.json` (and `.claude/cache/sc-recommend-lookup.yaml`) are tracked.
- **The tasklist MUST NEVER `git add` any `.claude/` path except `.claude/settings.json`.** If any `git add` requires `-f` on a `.claude/` path, that is the violation siren — STOP. (Per CLAUDE.md ABSOLUTE RULE + memory `feedback_claude_dir_gitignored.md`.)
- Note: `.claude/cache/sc-recommend-lookup.yaml` IS currently tracked but is unrelated to this task; do not stage it as part of remediation.

## Status: Complete
