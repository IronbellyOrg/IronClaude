1975b2aeaac7696d1509db9f1c89771dff33d4e6
# Task 27 review 1

Earlier blocking findings: none (first review).

## AC marks

- T27.AC1 met. `docs/designs/issue-watcher-zero-setup-coder-handoff.md:43-51` has a row for each of R1, R6, R9, R10, R17, R20 and R21. Issue 515 is on R6 and R21. Issue 516 is on R9, R10 and R17. R1 and R20 say "none". R20 is recorded as open with a reproduction step (line 50). The values match `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:36,40,41,43,48,49`. Requirements R10 and R21 name no issue number themselves. The 516 on R10 and 515 on R21 are inferred from the rows' topics and from requirements.md:79. That is not a blocking issue.
- T27.AC2 met. Lines 64, 97 and 101 of the handoff file.
  - Line 64 records the `gh auth status` result under `env -i`. I re-ran it, and it came back logged in as `ironbelly`, scopes `gist`, `project`, `read:org`, `repo` and `workflow`, with exit 0. That matches the file.
  - Line 97 states the credential row.
  - Line 101 states the `superclaude install --force` step for guard version 2. `src/superclaude/hooks/scripts/launch-level-guard.sh:10` carries `launch-level-guard-version: 2`.
- T27.AC3 met. Lines 58-59 of the handoff file contain an absolute `PATH=`, `/usr/bin/flock -n`, `>> /home/coder/.aidev/logs/issue-watch.log` and `run-all`.

## Fact checks against live files

- All tool paths exist: the Orca shim, `/home/coder/.local/bin/gh`, `/usr/local/bin/superclaude` (a link into `/opt/uv/tools/superclaude/bin/superclaude`), `/usr/local/bin/uv` and `/usr/bin/flock`. `/home/coder/.aidev/logs` exists.
- The claim that the installed `/usr/local/bin/superclaude` has no `run-all` is true. `superclaude issue-watch --help` lists only `check-config`, `init-state`, `once`, `reset` and `status`.
- `run-all` and its `--orca` option exist in the source (`src/superclaude/cli/issue_watch/cli.py:432,462`). The loop-lock exit code is 75 (`cli.py:40,514`).
- `git ls-remote --heads origin Coordinator` printed nothing, so there is no remote `Coordinator` branch. That matches line 50.
- The defaults JSON at lines 71-78 equals the built-ins. See `defaults.py:28-30` for the approvers, trigger label and owners, and `predicates.py:17,20` for the field name `Approved` and the option `Yes`. The file name `issue-watch-defaults.json` matches `defaults.py:25`. The key set matches `defaults.py:34-39`.
- `approved_field_missing` is a real reason (`dispatch.py:74,293`). `approver_is_launch_account` is a real warning (`cli.py:224`, `first_run.py:190`).

## Findings

F1.1 ac=scope at=docs/designs/issue-watcher-zero-setup-coder-handoff.md:93 anchor=dispatch.py:74,293 chk=n,n,n,n family=wording fix=optional: say "the loop's per-repo check" instead of "the first-run check reports" `approved_field_missing`: the reason is raised in `dispatch.py` (the loop's repo check), and the text is close enough to be non-blocking.

No blocking findings.
