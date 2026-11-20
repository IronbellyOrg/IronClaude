045b0a1d8cc199ad2e4bdc3ff50fa0d74643b5a4
# T23 review 1

Ran `uv run pytest tests/issue_watch -q`: 2996 passed. Files read on disk: `src/superclaude/cli/issue_watch/dispatch.py`, `tests/issue_watch/test_dispatch.py` (untracked), `repos.py`, `runner.py`, `generate.py`, `first_run.py`, `record.py`, and the output lines in `cli.py:130-136`.

## Earlier blocking findings
None (first review).

## ACs

T23.AC1 met. Citations, one per required case in `tests/issue_watch/test_dispatch.py`:
- Rotation across three sweeps: `test_dispatch.py:131` (`test_the_order_rotates_across_three_sweeps`), backed by `dispatch.py:220-221, 260-263`.
- Stop after the first `launched:` line: `test_dispatch.py:146`, backed by `dispatch.py:256-257`.
- Stop after an `attempted:` line: `test_dispatch.py:161`, backed by `dispatch.py:256-257`. The regexes match the real child output at `cli.py:130-136`.
- Child killed at 255 s with a pending entry stops the loop: `test_dispatch.py:199`, backed by `dispatch.py:258-259, 142-155`. It also asserts `CHILD_TIMEOUT_S == 255.0 > cycle.DEADLINE_TOTAL_S`, and `cycle.py:41` is 240.
- Same kill with no pending entry lets later repos run: `test_dispatch.py:223`.
- 270 s cap with unreached repos reported: `test_dispatch.py:253`, backed by `dispatch.py:230-235`.
- Repo with no config generated first: `test_dispatch.py:272`, backed by `dispatch.py:236-244`.
- Failed `orca repo list` gives an error result: `test_dispatch.py:334`, backed by `dispatch.py:206-209` and `repos.py:121-124`. All four reply shapes are covered.

T23.AC2 met. A timeout returns a `ChildResult` and never raises or breaks the loop (`dispatch.py:169-172, 254-259`). Each child's `exit_code` and `reason` are kept in `ChildResult` (`dispatch.py:60-71, 178-186`), and `test_dispatch.py:352` (`test_each_childs_exit_code_and_reason_are_kept`) pins this. A spawn error is also kept without stopping the loop (`dispatch.py:173-174`; `test_dispatch.py:367`).

## Constraint checks
- `dispatch.py` runs commands only through `runner.run` (`dispatch.py:167`). It imports no `subprocess`, and the `dispatch` row was added to the boundaries table.
- The store read goes through `record.FileStore.load`, which never writes (`record.py:347-368`). The only write is `rotation.json`, under `base.state_dir`, mode 0600 (`dispatch.py:114-124`).
- Absolute `orca` and `superclaude` paths are enforced (`dispatch.py:201-203`).
- `DAY_CAP` is untouched.
- Nothing enables a real watcher. The generated config starts disabled and only `first_run` enables it (`dispatch.py:242-244`).

## Findings (none blocking)
F1.1 ac=scope at=src/superclaude/cli/issue_watch/dispatch.py:230 anchor="total loop cap 270 seconds" chk=n,n,n,n family=loop-cap fix=optional: clamp the child timeout to the remaining loop time when that still exceeds `DEADLINE_TOTAL_S`, or leave as is: the cap is checked only before a child starts, so a child begun at 269 s can run to 524 s. The test pins this at `test_dispatch.py:260`. It matches the design wording "about 270 s" and "unfinished repos are skipped", so this is advisory.
F1.2 ac=T23.AC1 at=src/superclaude/cli/issue_watch/dispatch.py:150 anchor="unless the repo's `dispatch.json` store ... shows no pending or launched entry" chk=n,n,n,n family=killed-store fix=optional: a killed child whose store file is missing (`store_missing`) is treated as open and stops the loop; the conservative reading is defensible. No test covers it. Advisory.
F1.3 ac=scope at=src/superclaude/cli/issue_watch/dispatch.py:242 anchor="first_run(config_path" chk=n,n,n,n family=first-run-reason fix=optional: a failed first run is reported only as `not_enabled` (`dispatch.py:246-253`), and the first-run reason is lost in the sweep result. Task 25 may want it. Advisory.
