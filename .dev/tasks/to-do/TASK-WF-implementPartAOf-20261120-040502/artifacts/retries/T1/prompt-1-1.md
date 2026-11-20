9d3b1ed3e5e4a8870fc36fc9fb93080ff6fcc026
Review one task for spec compliance.

Task brief: Task 1: Add write_launch_result and call it from cmd_launch.
In `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` add a module constant `LAUNCH_RESULT_NAME = "launch-result.json"` next to `RECORD_NAME`, and a function `write_launch_result(source: Path, result: dict) -> None` that writes `json.dumps(result, indent=2) + "\n"` to `source / LAUNCH_RESULT_NAME` through `atomic_write_text` and swallows `OSError` (best-effort, no new warning code, no change to the printed result). In `cmd_launch` route the result of every path that ends `launched` or `failed` through one local helper that calls `write_launch_result(source, result)` and then `emit(result)`: the no-usable-record failure, the stale-prompt failure, the `W-ENFORCEMENT-ABSENT` refusal, the `W-L2-ABSENT` refusal under `IR7_REFUSE`, the launch-record write failure, the failed `orca agent launch`, and the final `launched` result (write it after the `unrecorded` detail text is added, so the file equals what is printed). The `already_launched` path keeps calling `emit` alone, so an earlier result file is never overwritten by a repeat claim. Make the helper a function nested inside `cmd_launch`, so `cmd_launch` is the only caller of `write_launch_result`. A `failed` result of the no-usable-record path (line 1702) also replaces an earlier file: that is intended, because it is the newest result of a launch attempt that ran, and Task 3 says so in the docs.

In `copy_issue_dir` (orca_worktree.py:466-467) change the skip from `rel.as_posix() == RECORD_NAME` to `rel.as_posix() in (RECORD_NAME, LAUNCH_RESULT_NAME)`, so a re-claim of the same issue never copies an earlier `launch-result.json` into a worktree (the copy would otherwise leave a stale machine record there and could create a `.prev` file next to it).

Acceptance criteria:
- T1.AC1: After a `launched` call, `<source>/launch-result.json` parses to the same object the `launch` subcommand printed; after a refused or failed call it holds that failed object; after an `already_launched` call the file from the earlier launch is unchanged.
- T1.AC2: A `worktree` step run after a launch does not copy `launch-result.json` into `<wt>/.dev/issues/<N>/` and creates no `launch-result.json.prev`, and `worktree.json` is still not copied.
- T1.AC3: `launch_result`, `session_report`, `record_launch` and `build_parser` are unchanged, and `cmd_launch` is the only caller of `write_launch_result`.
- T1.AC4: `tests/skills/test_issue_orca_worktree.py::test_ir6_launched_result_states_the_release_and_both_layers` and `tests/skills/test_issue_l2_install.py` (which calls `cmd_launch` directly, around line 620) still pass.
(Note for the reviewer: the existing test `test_launch_creates_no_file_in_the_worktree_or_the_source_directory` is owned by Task 2 and is expected to change there; it is not part of T1's AC.)
Global constraints: Edit distributable files only under `src/superclaude/` and tests under `tests/`; then run `make sync-dev` and `make verify-sync`. The `.claude/` copies are never staged, and no installed primitive may name a `src/superclaude/` path. The file is best-effort: a failed write never changes the JSON the `launch` subcommand prints, and the existing launch JSON keys keep their names and values. Part B (session-gov.sh, observation runbook, superclaude install, live OB-H2 rerun) and a verbatim-print rule for the claiming agent are out of scope.
Start sha: 9d3b1ed3e5e4a8870fc36fc9fb93080ff6fcc026
Diff against the start snapshot: The change is in the worktree at /home/coder/workspaces/worktrees/IronClaude/issue-691-launch-result. Produce it with `git diff 9d3b1ed3e5e4a8870fc36fc9fb93080ff6fcc026 -- src tests` (only src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py changed; no untracked product files). Codegraph context: index_state: fresh, checked_at: 2026-11-20T04:06:49Z, worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-launch-result. Call codegraph only when index_state: fresh, never to widen scope. Dependents not in the diff: write_launch_result has one caller (the nested `finish` in cmd_launch, same file), confirmed by Grep; cmd_launch is called by tests/skills/test_issue_l2_install.py and tests/skills/test_issue_orca_worktree.py.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
