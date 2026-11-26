# Result: Run ledger for /sc:sweep (IronbellyOrg/IronClaude#895)

outcome: succeeded. The `superclaude sweep ledger` command, the sweep fallback to the ledger, the hook file and the install notes are built and tested; 893 tests pass with none failing, and the real runs below worked. Nothing is installed, scheduled, registered, committed or pushed.

pull_request: https://github.com/IronbellyOrg/IronClaude/pull/907

PR 907 (base `integration`, head `ironbelly/run-ledger`, opened 2026-11-26 after the owner's "Go 895 pr"): CI all green on `e8a10c264`, mergeable and clean, not merged. Review rounds: round 1 fixed the Orca executable name and the module-level `fcntl` import; round 2 fixed the hook's command-name matching; round 3 hit the 2-round cap, so three findings were left open: the hook fixture shape was not live-captured (Augment, medium; cannot be fixed before the hook is registered, stays disclosed), `--add` of an already-present Run recorded no fresh hook time (Codex P2) and the hook did not match a quoted absolute Orca path with spaces (Augment, medium). One extra commit (`e8a10c264`) repaired my own CI break (a test fixture imported twice). After the owner answered "No, fix first", a further round fixed the last two: `--add` now refreshes the hook metadata of a Run already in the ledger, and the hook matches a quoted path with spaces and a quoted bare name. The statements above that nothing is committed or pushed describe the state when the real runs were made.

artifacts:
- src/superclaude/cli/sweep/ledger.py (new: inclusion rules, Orca reader and guards, file store, the `ledger` command)
- src/superclaude/cli/sweep/commands.py (registers `ledger`; `run` falls back to the ledger)
- src/superclaude/cli/sweep/models.py (`SweepContext.run_source`)
- src/superclaude/cli/sweep/report.py (header line for the Run source)
- src/superclaude/commands/sweep.md and src/superclaude/skills/sc-sweep-protocol/SKILL.md (text; synced to `.claude/` by `make sync-dev`, which is gitignored and never staged)
- src/superclaude/hooks/scripts/run-ledger-record.sh and its byte-equal mirror plugins/superclaude/hooks/scripts/run-ledger-record.sh (the hook file; not registered)
- src/superclaude/cli/install_hooks.py (one entry in `_FRESHNESS_SCRIPTS`)
- docs/user-guide/run-ledger.md (install notes for Coder#545)
- tests/run_ledger/ (conftest.py, test_rules.py, test_build.py, test_imports.py, test_store.py, test_cli.py, test_hook.py, fixtures/run_create_stdout.json, fixtures/posttooluse_run_create.json)
- tests/sweep/test_ledger_input.py (new), tests/sweep/conftest.py, tests/sweep/test_cli_contract.py, tests/sweep/test_report.py, tests/cli/test_install_hooks.py (edited)
- .dev/tasks/done/TASK-WF-remediationSourc-20261126-181052/ (the plan package; its progress.md ledger, artifacts/pytest.log, artifacts/ledger.json, artifacts/hook-decision.md and per-task logs and review files)
- .dev/sweeps/20261126-184526-sweep.md (the report the acceptance sweep wrote; gitignored)
- .dev/brainstorms/20261126-run-ledger-script/ and .dev/reflect/pre-TASK-WF-*/ (brainstorm and plan-review records)

## Real runs on this host (2026-11-26)

Ledger written to a temporary path, `/tmp/runledger-acceptance/run-ledger.json` (copy: `.dev/tasks/done/TASK-WF-remediationSourc-20261126-181052/artifacts/ledger.json`), generated 2026-11-26T18:44:50Z.

| Measure | This run | Baseline in the brief |
|---|---|---|
| Rebuild wall time (`superclaude sweep ledger`, 65 Runs listed, 24 worktrees) | 24.4 s (a dry run 24.7 s, the stripped-environment check 24.3 s) | 26.1 s with no short-circuit |
| Sweep over the ledger (`superclaude sweep run`, 12 Runs) | 24.4 s, 2,367 lines of report | 48.6 s and 3,666 lines for all Runs |

- Runs kept: 12 of 65 listed. By reason (a Run can have several): live worktree 1, unfinished Task 9, created since the last build 2 (the first build took the 24-hour fallback; one of the 2 is the scratch Run), hook-added 0. The live-worktree count is lower than the 3 measured earlier because workers are no longer fetched for a Run that a Task or its age already admits (the short-circuit in the plan).
- Cost figures the owner asked to see: admitted only through the main checkout: 0. Admitted only by `ready` or `blocked` Tasks older than 7 days: 7 of the 12. Held in only by `blocked` Tasks: 1.
- The sweep ran with exit 0, `orca_available: true`, and the header says "Run ids from the Run ledger built 2026-11-26T18:44:50Z" (that proves the ledger path was taken); neither stderr nor the report holds "no Run bound".
- How the binding was made to fail: `run-create` had bound this terminal to the scratch Run, so I ran the sweep with `ORCA_TERMINAL_HANDLE` unset. In that case `run-current` answers "Could not determine the sender terminal", which the sweep treats as "Orca unavailable"; it took the ledger path and every other read still worked. The plain "No Run is bound" answer is covered by the tests (`tests/sweep/test_ledger_input.py`), not by this real run.
- Hook end to end: the real hook script, with this worktree's `superclaude` and a copy of the ledger, turned a payload (the captured `run-create` output with the id replaced) into a `source: "hook"` entry; `generated_at` stayed unchanged.

## Hook decision

Decision: deliver. Authority: the owner's brief to this agent orders the test in these words: "first test what such a hook actually receives from run-create". One scratch Run was created, `run_e97be8837462` (objective "scratch Run for the run-ledger hook payload test, safe to ignore", 2026-11-26T18:38:33Z). Orca cannot delete it, so it stays; `run-list` went from 64 to 65 Runs. No Run was deleted, `orca orchestration reset` was not run. The real `run-create` output carries the new Run's id (`result.run.id`). Also seen: `run-create` binds the calling terminal to the new Run. The shape of a live Bash `tool_response` was not captured (the hooks reference gives the keys `stdout`, `stderr`, `interrupted`, `isImage` but no full Bash example), so `tests/run_ledger/fixtures/posttooluse_run_create.json` is built from those documented keys around the real captured output, and the script accepts a string or an object. Details: `.dev/tasks/done/TASK-WF-remediationSourc-20261126-181052/artifacts/hook-decision.md`.

## Tests

`uv run pytest tests/run_ledger tests/sweep tests/commands/test_sweep_command.py tests/cli/test_install_hooks.py -v`: 893 passed, 0 failed, 0 errors (log: `.dev/tasks/done/TASK-WF-remediationSourc-20261126-181052/artifacts/pytest.log`). `uv run ruff check` and `make verify-sync` are clean. `src/superclaude/cli/main.py`, `src/superclaude/cli/sweep/probes.py` and `src/superclaude/hooks/hooks.json` have no diff. Each of the 11 tasks was reviewed by a fresh reviewer agent against its acceptance criteria: all compliant, none blocking (the non-blocking notes are in each task's `artifacts/retries/T<n>/notes.md`).

## Pre-install check

`env -i HOME=$HOME PATH=<orca shim>:/usr/local/bin:/usr/bin:/bin <this worktree>/.venv/bin/superclaude sweep ledger --dry-run`: exit 0 in 24.3 s, found Orca without the session environment. Caveat: `command -v superclaude` prints `/usr/local/bin/superclaude` (version 6.1.0), but that installed copy does not have `sweep ledger` yet (`superclaude sweep ledger --help` there answers with the `sweep` help), so the check on the target host only passes after the installed copy is updated. That belongs to Coder#545.

## Decisions for the owner

1. Age cutoff for stale Runs: none is built. 7 of the 12 kept Runs are held only by `ready` or `blocked` Tasks older than 7 days. Keep (default, over-inclusion is safe) or give a cutoff (for example Task age over N days). Decided in chat on 2026-11-26: "Yes" to keeping the default, so no cutoff is built.
2. The 30-minute schedule and the hook registration are left to Coder#545, as ordered. Two things for that issue: the cron line needs the `superclaude` state folder to exist before its first run (`flock` and the redirect do not create it), and the installed `superclaude` must be updated first. `docs/user-guide/run-ledger.md` has the text to adopt; one sentence there still says the 24-hour rule catches a missed Run when it only applies without a previous ledger (the Run is caught either way); recorded as a note, not edited.

## Deviations and limits

- The plan reviews used Sonnet and Haiku, two reviewers, not three, and a reduced second pipeline, because Opus is not selected automatically (owner rule). The per-task reviews used one Sonnet reviewer each.
- In `commands.py` the `ledger` module is imported at the top and the command registered right after the group definition, instead of a mid-file import, so no lint exception is needed.
- Two plan review findings were left to implementation and are handled: every time comparison goes through `parse_time` (mixed SQLite and ISO forms are tested), and the import-allowlist test handles `from .probes import X`, `from . import probes` and attribute access.
- Not done: nothing was committed, pushed or opened as a pull request; no crontab, no `settings.json` edit, no GitHub write. `.dev/tasks` is staged.
