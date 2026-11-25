# Codegraph grounding: TASK-WF-issueSummary-20261125-190451 (regenerate route; carries over from the archived first package)

## Run state

- index_state: stale (token `graph:stale`); the one readiness check of this run was made at 2026-11-25T17:53:41Z for the first package and is not repeated (one check per run). CLI status warned the last index run never finished, so every lookup used Glob, Grep and Read. The codegraph server later disconnected; no graph lookup was needed.
- worktree_root / projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-834

## Resolved symbols

Same files and anchors as the first package's record (archived with it under the archive folder): refs/create.md lines 57, 63-69, 82-84, 95-97; SKILL.md lines 4, 76, 102, 103; templates/draft-notes.md; the three worker files at line 24; commands/issue.md lines 19 and 85; docs/designs/sc-issue-command.md lines 223-225, 381, 460; docs/user-guide/commands.md line 357; the five test files named in Tasks 4, 7 and 8. New for this package, resolved with Read: `src/superclaude/cli/install_skills.py:62-64` (`install_all_skills(target_path, force)`), `install_agents.py:15`, `install_commands.py:16`, `main.py:211-255` (the phases `superclaude install` also runs), `src/superclaude/hooks/scripts/launch-level-guard.sh:466, :415, :510, :665, :814-819` (what the launch guard refuses).

## Dependents

- The old trigger text appears only in create.md:84, SKILL.md:102 and docs/designs/sc-issue-command.md:225 and :460 (re-checked by the first run's review: none in `tests/`). Tasks 1, 4 and 6 edit those.
- Exact-line pins: `tests/skills/test_worker_contract.py:3057-3060` pins SKILL.md line 103 (Task 4 updates the key); refs/create.md's GitHub-write paragraph, lookup paragraph and Wave 5 step 6 are pinned and stay unchanged.
- The tests of Tasks 7 and 8 must build the old trigger from fragments so Tasks 7, 8 and 10 can search `tests/` for the whole phrase.

## Pre-check

- Files named by tasks: all exist (15 from the first package, plus the three installer files, main.py and the guard script, checked by Read in the first run's review).
- Line anchors: carried over from the first package, which the review's evidence validator re-read (181 citations checked, 0 dropped).
- Dependents of touched text that no task names: none found.
