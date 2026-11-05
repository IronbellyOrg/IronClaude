# Worktree hit classification (Task 1)

## Summary

Historical record: POST-REFLECT-TASK.md, 79 of the Search A hits, left unchanged. The file's status is Blocked (POST-REFLECT-TASK.md:6) and its `.dev/worktrees` paths are intentionally stale; anyone resuming it must substitute an Orca-created worktree.

- Live totals on 2026-11-02 (23:08Z): Search A 108 lines in 17 files; Search B 9 lines in 7 files. Both match the baseline in the plan's Constraints, so no new hits needed classifying.
- Raw outputs: `./artifacts/t1-search-a.txt` (Search A, `-c` then `-n`), `./artifacts/t1-search-b.txt` (Search B, `-c` then `-n`), `./artifacts/t1-worktree-list.txt` (`git worktree list`).
- Search A: `git grep -n -E '\.dev/worktrees|git worktree add' -- ':!.dev'`. Search B: `git grep -n -E '"worktree",\s*"add"' -- ':!.dev'`.
- Classes: Project worktree (rewrite to Orca's default location); Internal temporary checkout (works without Orca); Historical record (unchanged).

## Search A table (108 lines, 17 files)

| File | Hits | Class | Action | Reason |
|---|---|---|---|---|
| POST-REFLECT-TASK.md | 79 | Historical record | none (byte-unchanged) | Owner decision: Blocked historical task file; its `.dev/worktrees` paths are intentionally stale. |
| CLAUDE.md | 8 | Project worktree | rewrite subsection `### Parallel Development with Git Worktrees` to the Orca rule (Task 3) | Lines 299-329 tell agents to create project worktrees with `git worktree add .dev/worktrees/...`. |
| .gitignore | 2 | Project worktree | rewrite comment only; keep the `.dev/worktrees/` entry as a retired-path guard (Task 5) | Line 240 calls `.dev/worktrees/<name>/` the canonical location; line 242 is the ignore entry. |
| src/superclaude/commands/recommend.md | 1 | Project worktree | make the path note location-neutral (Task 6) | Line 137 assumes linked worktrees live at `.dev/worktrees/<name>/`. |
| src/superclaude/skills/sc-recommend/SKILL.md | 2 | Project worktree | make the path notes location-neutral (Task 6) | Lines 128 and 198 assume `.dev/worktrees/<name>/`. |
| src/superclaude/skills/sc-recommend/refs/surface-enumeration.md | 1 | Project worktree | make the path note location-neutral (Task 6) | Line 19 assumes `.dev/worktrees/<name>/`. |
| plugins/superclaude/commands/recommend.md | 1 | Project worktree | byte copy of the src file (Task 7) | Plugin mirror of src/superclaude/commands/recommend.md:137. |
| plugins/superclaude/skills/sc-recommend/SKILL.md | 2 | Project worktree | byte copy of the src file (Task 7) | Plugin mirror of src/superclaude/skills/sc-recommend/SKILL.md:128, :198. |
| plugins/superclaude/skills/sc-recommend/refs/surface-enumeration.md | 1 | Project worktree | byte copy of the src file (Task 7) | Plugin mirror of surface-enumeration.md:19. |
| tests/docs/test_tavily_doc_alignment.py | 1 | Project worktree | comment only (Task 8) | Line 49 comment says the worktree lives under `.dev/worktrees/…`. |
| src/superclaude/cli/reflect/config.py | 1 | Internal temporary checkout | none | Line 171 docstring: reflect `--isolate-reviewers` snapshot made with `git worktree add --detach` and removed with `git worktree remove --force`. |
| src/superclaude/skills/sc-reflect-protocol/SKILL.md | 2 | Internal temporary checkout | none | Lines 250-251 describe the same reflect review snapshot. |
| src/superclaude/skills/sc-post-release-protocol/SKILL.md | 1 | Internal temporary checkout | state that the optional tag checkout is made in a temporary directory and removed after the scan (Task 6) | Line 91 offers a `git worktree add` checkout of the release tag. |
| tests/cli/reflect/test_isolate_reviewers_cli.py | 2 | Internal temporary checkout | none | Lines 9 and 124 are docstrings of the reflect snapshot test. |
| tests/skills/test_implement_retry_revert.py | 2 | Internal temporary checkout | none | Lines 613 and 1053 build a linked worktree inside a pytest `tmp_path` fixture repo. |
| tests/troubleshoot/backtest/git_replay.py | 1 | Internal temporary checkout | none | Line 9 docstring: backtest replay checkout, removed after use. |
| tests/troubleshoot/backtest/test_git_replay_integration.py | 1 | Internal temporary checkout | none | Line 100 docstring about concurrent `git worktree add` in the replay test. |
| **Total** | **108** | | | |

## Search B table (9 lines, 7 files)

| File | Hits | Class | Action | Reason |
|---|---|---|---|---|
| scripts/eval_runner.py | 1 | Internal temporary checkout | rewrite to create its master checkout in a temporary directory and remove it (Task 2) | Line 143 creates `REPO_ROOT.parent / "IronClaude-eval-master"` and never removes it (owner decision 2026-11-02). |
| src/superclaude/cli/reflect/config.py | 1 | Internal temporary checkout | none | Line 202 creates the reflect review snapshot with `--detach`. |
| tests/cli/reflect/test_isolate_reviewers_cli.py | 1 | Internal temporary checkout | none | Line 147 asserts no `("worktree", "add")` call happens on the STOP path. |
| tests/skills/test_implement_retry_revert.py | 2 | Internal temporary checkout | none | Lines 614 and 1054 add a linked worktree in a pytest `tmp_path` fixture repo. |
| tests/troubleshoot/backtest/git_replay.py | 1 | Internal temporary checkout | none | Line 191 creates the backtest replay checkout, removed after use. |
| tests/troubleshoot/backtest/test_git_replay_unit.py | 1 | Internal temporary checkout | none | Line 34 inspects mocked `git worktree add --detach` calls. |
| tests/unit/test_ccsession_tag.py | 2 | Internal temporary checkout | none | Lines 1858 and 1912 add a linked worktree in a pytest `tmp_path` fixture repo. |
| **Total** | **9** | | | |

Files found by both searches: `src/superclaude/cli/reflect/config.py`, `tests/cli/reflect/test_isolate_reviewers_cli.py`, `tests/skills/test_implement_retry_revert.py`, `tests/troubleshoot/backtest/git_replay.py`.

## Outside both searches, recorded only

- `docs/swarm/runbook.md:34` cites `/config/workspace/IronClaude/.claude/worktrees/BareReview/CLAUDE.md`, a documentation reference to another host's checkout. Out of scope and left unchanged.

## Existing checkouts at the retired location

`./artifacts/t1-worktree-list.txt` (23:08Z) contains no line with `/.dev/worktrees/`, so there is nothing to list. The two checkouts named in the plan's Constraints (`.../IronClaude/.dev/worktrees/issue-body-templates` and `.../markdownlint-issue-body-files`) were present when the plan was written but no longer exist; this plan moved or removed nothing. Any checkout that appears there later is left in place; not moved or removed by this plan.
