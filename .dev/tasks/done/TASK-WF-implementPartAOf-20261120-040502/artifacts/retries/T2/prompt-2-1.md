4703d676e266123a563c95f335e39211c80e0c75
Review one task for spec compliance.

Task brief: Task 2: Test the result file and update the no-new-file test

Depends on: Task 1

In `tests/skills/test_issue_orca_worktree.py`, next to the `ir6` tests, add four tests that use `launch_scene` and `run_launch`, and a fifth next to `test_fo16_worktree_json_is_never_copied_and_keeps_its_launch_entry` (line 799), named `test_fo16_launch_result_file_is_never_copied_into_the_worktree`, that puts a `launch-result.json` in the issue folder, runs the `worktree` step as `test_fo16` does, and asserts the file is not in `<wt>/.dev/issues/302/` and no `launch-result.json.prev` exists. The four launch tests are: a launched result is written and equals the printed JSON (compare `json.loads` of the file with the returned dict); a refused launch (`launch_scene(..., hook=None)`) writes a `failed` file with `enforcement_hook` `missing`; a second `run_launch` after a launched one returns `already_launched` and leaves the file's bytes identical; a write failure (create a directory named `launch-result.json` in the issue folder before the launch, so the rename in `atomic_write_text` raises `OSError`; do not monkeypatch `atomic_write_text` itself, because `record_launch` also uses it) still prints the launched JSON and exits 0, and the printed dict is unchanged: assert `status` `launched`, `warning` `W-L2-ABSENT` (the scene has no pre-push hook, as `test_la6` shows), `enforcement_hook` `installed`, `terminal` `term_abc` (the handle `LAUNCH_OK` returns), `layers[0]` starting with `L1 guard: effective`, `release` starting with `to release this session` (as the `ir6` test's text shows), and that `detail` does not contain `launch-result`. Name the five tests so each contains `launch_result_file`. Then change `test_launch_creates_no_file_in_the_worktree_or_the_source_directory` (line 2136) so the worktree listing and `git status --porcelain` stay unchanged but the source directory listing gains exactly `launch-result.json`, and rename it `test_launch_adds_only_the_launch_result_file_to_the_source_directory`.

Acceptance criteria:
- T2.AC1: `uv run pytest tests/skills/test_issue_orca_worktree.py -k launch_result_file` passes with the five new tests and the renamed one, removing the `write_launch_result` call from the `launched` path makes the first new test fail, and removing `LAUNCH_RESULT_NAME` from the skip in `copy_issue_dir` makes the copy test fail.
- T2.AC2: The rest of `tests/skills/test_issue_orca_worktree.py` and `tests/skills/test_issue_l2_install.py` pass unchanged.
Global constraints: Edit distributable files only under `src/superclaude/` and tests under `tests/`; then run `make sync-dev` and `make verify-sync`. The `.claude/` copies are never staged, and no installed primitive may name a `src/superclaude/` path. The file is best-effort: a failed write never changes the JSON the `launch` subcommand prints, and the existing launch JSON keys keep their names and values. Part B (session-gov.sh, observation runbook, superclaude install, live OB-H2 rerun) and a verbatim-print rule for the claiming agent are out of scope.
Start sha: 4703d676e266123a563c95f335e39211c80e0c75
Diff against the start snapshot: The change is in the worktree at /home/coder/workspaces/worktrees/IronClaude/issue-691-launch-result. Produce it with `git diff 4703d676e266123a563c95f335e39211c80e0c75 -- src tests` (changed files: tests/skills/test_issue_orca_worktree.py; no untracked product files). Codegraph context: index_state: fresh, checked_at: 2026-11-20T04:06:49Z, worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-launch-result. Call codegraph only when index_state: fresh, never to widen scope.
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
