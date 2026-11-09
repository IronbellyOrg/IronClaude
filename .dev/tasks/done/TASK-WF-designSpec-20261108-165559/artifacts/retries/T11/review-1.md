# Review 1: T11 (start 0d30cd35b5a9b2e4d6d5bee2eab457d3a3794225, commit D = 719e1587a)

## Earlier blocking findings

None (first review).

## AC marks

- T11.AC1 met: T11.AC1@.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/final-check-retest.md:11 (LIM-1) through `:30` (LIM-20). There is one row for each of the 20 IDs in spec §6 (`.dev/brainstorms/20261108-094705-l2-pre-push-guard/merged-requirements.md:267-286`), which match source §9.1 (`source.md:614-633`). OB-H3 is marked PENDING at `final-check-retest.md:34`, as AC-11 requires (`source.md:735`). U-10 is pending at `:35`. U-5 and U-9 are OPEN at `:39` and `:40`, and are not claimed fixed.
- T11.AC2 met: T11.AC2@.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:155. `git show --stat --format= HEAD` (719e1587a) lists 19 paths. Fourteen are under `.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/`. Three are under `docs/` (`docs/designs/sc-issue-claim-pipeline-flag.md`, `docs/designs/sc-issue-launch-level-hook.md`, `docs/user-guide/commands.md`). The last two are `src/superclaude/commands/issue.md` and `src/superclaude/skills/sc-issue-protocol/SKILL.md`. No path is under `.claude/` (grep count 0). The subject starts with `docs:` and the body ends with `Co-Authored-By: Claude Code <noreply@anthropic.com>`. `make verify-sync` reports "All components in sync."

## Findings

None.

## Self-Audit

- I checked every `path:line` cited in `final-check-retest.md` against the live files. All of them hold the claimed content:
  - `tests/hooks/test_launch_job_identity.py`: 318, 480, 707, 1151 and 1437.
  - `tests/hooks/test_launch_level_pre_push.py`: 507, 621, 630, 661, 672-675, 707, 768, 769, 896, 911, 985 and 1062-1070.
  - `tests/hooks/test_launch_level_guard_l2_tokens.py`: 60-61, 65, 107, 111, 116, 121 and 126. LIM-4 rows 107-121 assert TAMPER, and the `send-pack` row 126 asserts UNKNOWN.
  - `tests/skills/test_issue_l2_install.py`: 200-211, 219-221, 235, 289 and 312.
  - `tests/hooks/test_launch_level_guard.py`: 61, 783, 786 and 814.
  - Design doc: `docs/designs/sc-issue-launch-level-hook.md:536-557`, `:547`, `:550` and `:557`.
  - `source.md`: 600, 735, 748, 752 and 753.
- The worktree diff against the start tree makes one change to the design doc. It adds a pointer sentence to the re-test file after the limits table, and that sentence is accurate.
- Minor points that do not block:
  - The LIM-9 row says "missing or non-executable" is tested, but it cites only the not-executable case. The missing-hook case is tested at `tests/skills/test_issue_l2_install.py:553` and `:567`, and the row does not cite those lines.
  - The LIM-8 evidence points at the class tables of the #440 suite, not at specific `gh api` or `orca` test cases.
  - Neither point makes a statement false or leaves out output an AC requires.
- I did not check:
  - whether `make sync-dev` was run before the commit (the tree is in sync now);
  - whether the Task 10 doc edits themselves are correct (that is T10's scope).
