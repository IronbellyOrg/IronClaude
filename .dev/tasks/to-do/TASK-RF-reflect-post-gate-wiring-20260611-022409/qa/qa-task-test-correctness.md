# QA Report — Agent F test-correctness lens

**Topic:** Phase 4 Layer-A acceptance test flat `superclaude reflect run` contract
**Date:** 2026-06-11
**Fix authorization:** false — report only

---

## Candidate Issue Sweep

I investigated these candidate failure modes before assigning the verdict:
1. Anchor drift between the helper literal and the O1 SKILL heading.
2. Stale Mode/auto-resolved/§6.3 markers remaining in the helper slice logic.
3. Assertions naming flags not implemented by the CLI.
4. `xfail` accidentally removed or made strict, causing a red XPASS.
5. Scope creep into sibling tests or Layer-B/thinness guards.
6. Helper extracting an empty or wrong block.
7. Full reflect CLI suite regressions outside the focused test.

## Checks

### 1. Anchor = single source of truth — PASS

- Helper anchor at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:61` is exactly: `anchor = "Independent post-execution reflection gate (wrapper shell-out)"`.
- O1 SKILL heading at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/task-builder/SKILL.md:2200` contains the same byte string: `- [ ] **N.{X-1} -- Independent post-execution reflection gate (wrapper shell-out)**`.
- Slice bound is the next checklist item: helper uses `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:64` `end = text.index("- [ ] **N.X", start)`, matching SKILL next bullet at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/task-builder/SKILL.md:2207` `- [ ] **N.X — Update task status to Done**`.
- The helper body at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:49-65` no longer uses the stale `Mode 2`, `auto-resolved-2`, `§6.3`, or `**Mode `halt`` slice markers; it indexes the flat O1 anchor and next `N.X` bullet.

### 2. Asserted tokens real + correct — FAIL

- Positive asserted tokens are present in the test body at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:85-89`: `superclaude reflect run`, `--depth deep`, `--fix`, and `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`.
- The negative loop over `_NESTING_TOKENS` is present at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:91-92`, and `_NESTING_TOKENS = ("Task(", "subagent_type")` is defined at line 46.
- CLI flag cross-check passed: `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/commands.py:102-105` defines `--depth` as a Click choice, and `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/commands.py:128-131` defines `--fix/--no-fix`.
- Failure: the prompt required `No Mode/§6.3 markers referenced anywhere in the test`, but grep found stale-marker literals in the xfail reason at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:70-71`: `Mode 2`, `auto-resolved-2`, and `§6.3`.

### 3. xfail disposition matches OQ-1 — PASS

- The decorator is kept at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:68-79` and explicitly sets `strict=False` at line 78.
- The reason records the stale-marker-to-flat-contract migration at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:70-76`; this satisfies the migration-history requirement, while still causing Check 2's stricter no-stale-literals-anywhere requirement to fail.
- Focused test command run from repo root with UV: `uv run pytest "tests/cli/reflect/test_no_nesting_guard.py::test_layer_a_wrapper_branch_is_bash_shellout" -q`.
- Result line quoted: `============================== 1 xpassed in 0.02s ==============================`. It reported XPASS, not XFAIL and not failure.

### 4. Scope confinement — PASS

- `git diff origin/master --name-only -- tests/cli/reflect/test_no_nesting_guard.py tests/cli/reflect/test_promote_plumbing.py tests/cli/reflect/test_cli_smoke.py` returned only `tests/cli/reflect/test_no_nesting_guard.py`; the sibling tests were not in the diff.
- Zero-context diff shows changes only in the Layer-A helper/decorator/test-body region: helper docstring/body at old/new around line 50-64, xfail reason around line 65-78, test docstring/assertions around line 76-89.
- Module constants remain outside the changed diff and are present at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:19-46`: `_REPO_ROOT`, `_SKILL_SRC`, `_REFLECT_PKG`, `_RUNNER_SRC`, `_REFLECT_PY`, regex constants, and `_NESTING_TOKENS`.
- Layer B and thinness guards remain outside the changed diff and are still present at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:95`, `:105`, `:116`, and `:128`.

### 5. Full suite green — PASS

- Full suite command run from repo root with UV: `uv run pytest tests/cli/reflect/ -q`.
- Result line quoted: `======================== 77 passed, 1 xpassed in 0.27s =========================`.
- There were zero failures across 78 collected tests.

### 6. Helper extracts non-empty shell-out block — PASS

- Command run: `uv run python -c "import tests.cli.reflect.test_no_nesting_guard as t, pathlib; b=t._extract_wrapper_branch(pathlib.Path('src/superclaude/skills/task-builder/SKILL.md').read_text()); print(len(b), 'superclaude reflect run' in b, 'Task(' not in b, 'subagent_type' not in b)"`.
- Output quoted: `3102 True True True`.
- This proves the extracted block is non-empty, includes `superclaude reflect run`, and excludes both nesting tokens checked by the test.

## Summary

- Checks passed: 5 / 6
- Checks failed: 1 / 6
- Test commands run: 2 pytest commands + 1 helper extraction command
- Files read directly: `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/task-builder/SKILL.md`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/commands.py`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_promote_plumbing.py`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_cli_smoke.py`.

VERDICT: FAIL

## Numbered Findings

1. IMPORTANT — Stale Mode taxonomy literals remain referenced in the Layer-A test despite the required flat-contract-only marker surface.
   - Location: `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py:70-71`.
   - Evidence: grep found the xfail reason still quotes `Mode 2`, `auto-resolved-2`, and `§6.3`.
   - Why it matters: the requested Check 2 explicitly says `No Mode/§6.3 markers referenced anywhere in the test`. Even though Check 3 asks the reason to record the migration and the focused test XPASSes, the current wording records it by reintroducing the exact stale tokens the flat-contract test was supposed to stop referencing.
   - Required fix: rewrite the xfail reason to describe the migration without the banned literal markers, e.g. refer generically to `the abandoned dial-taxonomy markers` or `legacy mode taxonomy`, while keeping `strict=False` and preserving the XPASS behavior.

## QA Complete
