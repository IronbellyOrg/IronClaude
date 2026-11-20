d7ceadc3243b9259667099feb23072c80bf0a361
Task 25 review, attempt 1

Earlier blocking findings: none (first review).

AC marks
- T25.AC1 met. T25.AC1@tests/issue_watch/test_cli.py:1868 (clean sweep), :1880 (skipped repo, plus a failed child giving exit 1), :1896 (held lock, exit 75, `seen == {}` shows no sweep ran), :1908 (dry run, `sorted(tmp_path.rglob("*"))` equal before and after, and `seen["dry_run"] is True`). The dry-run snapshot would show a lock file if one were created, because the CLI skips `dispatch.loop_lock` when `--dry-run` is set (src/superclaude/cli/issue_watch/cli.py:507-510, the `if dry_run:` branch before `with dispatch.loop_lock(base)`).
- T25.AC2 met. T25.AC2@src/superclaude/cli/issue_watch/cli.py:432 registers `run-all` on `issue_watch_group`. I ran `uv run superclaude issue-watch run-all --help` and it exited 0 with the option list. `test_run_all_help_exits_0_and_is_listed` and `test_the_group_lists_exactly_the_six_commands__df06` cover the group listing.
- T25.AC3 met. T25.AC3@tests/issue_watch: `uv run pytest tests/issue_watch -q` gave 3020 passed.

Scope checks
- Exit codes use the existing set: 2 through `_config_exit` for a config problem (a bad defaults file, a relative or missing `--orca` or `--superclaude`), 75 through `_EXIT_LOCK_HELD` when `dispatch.LoopLockHeld` is raised, 1 (`_EXIT_UNHEALTHY`) for a failed child or a failed `orca repo list`, and 0 for clean, waiting and dry-run sweeps.
- Lock: `dispatch.loop_lock` takes `flock(LOCK_EX|LOCK_NB)` on `<state>/issue-watch/run-all.lock` (src/superclaude/cli/issue_watch/dispatch.py, `loop_lock`). It is released in a `finally`, uses `O_NOFOLLOW`, and never waits.
- Dry run: `run_sweep(dry_run=True)` skips `ensure_config`, `first_run`, the rotation write and the child start. It does the reads (`orca repo list`, origin check, label, field and Project reads) and reports `would_generate` and `would_run`. `load_defaults` only reads.
- The report prints one line per child, skipped repo and generated repo, then an overall line. Repo names are sanitised by `_name`.
- The module-boundary test allows the new `cli` imports (tests/issue_watch/test_module_boundaries.py).
- The diff shows `dispatch.py` and `test_dispatch.py` as delete plus add. `git status` lists both as untracked files, so this is a snapshot artefact (they were untracked at the start sha). The live files exist and pass.

Findings (none block)
F1.1 ac=T25.AC1 at=tests/issue_watch/test_dispatch.py:1 anchor="--dry-run flag that lists repos and decisions but takes no lock, writes no config, no rotation file and no label and starts no child" chk=n,n,n,n family=dry-run-coverage fix=add a test in tests/issue_watch/test_dispatch.py that calls `run_sweep(dry_run=True)` over the existing `World` and asserts no child call, no `ensure_config`, no rotation or wait file, and no `gh label create`. The CLI dry-run test fakes `run_sweep`, so the "writes nothing" property of the real dry-run branch is not exercised. Low severity, since the code reads correctly and the AC1 text is met as written.
