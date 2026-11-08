# Reflect Reviewer — Deviation Findings

**Reviewer persona**: refactorer (structure, duplication, boundaries, security hygiene, documentation fidelity)
**Grounding root**: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher
**Diff scope**: e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b...26f551f41edece1f05c07a3c02d78325e365f6d1
**Timestamp**: 2026-11-08T04:50:00Z
**Total deviations**: 11

## Deviations

| # | Category | Location | What diverged | Evidence (file:line) | Severity |
|---|----------|----------|---------------|----------------------|----------|
| 1 | Drift | `src/superclaude/cli/issue_watch/cli.py:35`, `cli.py:123-129` | `once` can exit 1 with reason `cycle_crashed`. The design's `once` exit set is "0, 2, 3, 4, 5, 6, 7, 75" with no 1. The exit table has no 1 and no `cycle_crashed`. Design 10.1 says `audit.REASONS` "is a frozenset equal to the spec's reason table". The only authority is an executor PROPOSAL (Gate C fix C-3). The deviation register Table 2 row 1 says no R-003 row authorizes it, and no decision-register (DF) row does either. Mitigating: design 10.1 does foresee a stderr fallback "used for a crash", and the runbook documents exit 1 faithfully (`docs/designs/issue-watcher-setup.md:318`, `:331`). | `docs/designs/issue-watcher.md:114`, `issue-watcher.md:153-164`, `issue-watcher.md:718`, `issue-watcher.md:722`; `cli.py:124` comment "[PROPOSAL] (Gate C fix C-3, executor decision)" | MEDIUM |
| 2 | Drift | `src/superclaude/cli/issue_watch/record.py:23-29` | `record` imports four predicate functions (`format_utc`, `parse_utc`, `valid_issue_number`, `valid_operation_id`) plus the type `ApprovalResult`, and it uses an absolute import where every sibling uses a relative one. Design 5.3 allows `record` to import from `predicates` "types only". The boundary test rule was widened to "any name" instead of the design being amended, and its docstring miscounts the imports as "three functions and one type". The tasklist logs this as PRE-11 (minor); it is not in the 29 authorized departures. | `docs/designs/issue-watcher.md:239`; `tests/issue_watch/test_module_boundaries.py:20-21`, `:57-58` | LOW |
| 3 | Drift | `src/superclaude/cli/issue_watch/cycle.py:468`, `cycle.py:76` | Two duplicates that the design's import rules (section 5.3) do not force. `cycle._LOGIN` copies `github._LOGIN_RE` byte for byte, and `cycle._UTC_TS_FORMAT` copies `predicates._UTC_FORMAT`. `cycle` is allowed to import both `github` and `predicates`. No test pins either pair. | `cycle.py:468` vs `github.py:134`; `cycle.py:76` vs `predicates.py:23`; `docs/designs/issue-watcher.md:241` | LOW |
| 4 | Drift | `src/superclaude/cli/issue_watch/audit.py:395-397` | `stderr_fallback` reads the wall clock directly when no `ts` is given. `cli.py` calls it without a `ts` on three paths: config error, crash and reset refused. NFR-014 says every time read goes through the clock. | `audit.py:396` `datetime.datetime.now(datetime.timezone.utc)`; callers `cli.py:79`, `cli.py:127`, `cli.py:219`; `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md:231` | LOW |
| 5 | Drift | `src/superclaude/cli/issue_watch/cli.py:319` | `cli` calls `cycle.format_utc(now)`, which is the `predicates` helper reached through `cycle`'s namespace. Design 5.3 does not let `cli` use `predicates`. The boundary walker checks import statements only, so it cannot catch attribute access. The tasklist's Phase 8 log names this leak. | `cli.py:319`; `docs/designs/issue-watcher.md:242` | LOW |
| 6 | Drift | `docs/designs/issue-watcher-setup.md:53`, `:432`; `src/superclaude/cli/issue_watch/cli.py:314` | The CLI and its documented exit codes disagree in three places. (a) The runbook says only `once`, `check-config` and `init-state` exit 2 off Linux, but `reset` also runs the platform check, because `_load_config` defaults to `platform=True`. (b) The design's `reset --rate-limit` row lists exits 0, 6 and 75, but the code can exit 2 for a config or platform failure. (c) The runbook's `status` section lists exits 0, 1 and 6, omitting the exit 2 that the design lists and the code returns. | `cli.py:84-91`, `cli.py:169`, `cli.py:314`; `docs/designs/issue-watcher.md:115`, `:119`; `issue-watcher-setup.md:53`, `:432` | LOW |
| 7 | Necessary deviation | `src/superclaude/cli/issue_watch/cycle.py:1134-1137` | A new reason name, `cycle_complete`, is added to the closed reason table. Design 10.1 requires a `reason` on every cycle line, but design 4.3 names no reason for a cycle that ran to its end, so some name was needed. It still departs from "REASONS equal to the spec's reason table". The runbook flags it as a [PROPOSAL] name. | `docs/designs/issue-watcher.md:709`, `:157`, `:718`; `docs/designs/issue-watcher-setup.md:344` | LOW |
| 8 | Necessary deviation | `src/superclaude/cli/issue_watch/cycle.py:1227`, `cycle.py:1230` | `cycle` reads `launch._ORCA_CLIS`, a private name that `launch` imported from `install_user_setup`. Design 10.2 requires `status` (which lives in `cycle`) to use "the first `_ORCA_CLIS` name on PATH", and design 5.3 forbids `cycle` from importing `install_user_setup`. Going through `launch` is the only allowed route, but it couples `cycle` to a private name. | `docs/designs/issue-watcher.md:741`, `:240-241`; `launch.py:22` | LOW |
| 9 | Necessary deviation | `src/superclaude/cli/issue_watch/runner.py:89-129` | `runner` reads `time.monotonic()` to fill `duration_s`, outside the Clock interface. The field is required by design 5.4's `CommandResult`, and `runner` may import nothing from the package, so it cannot use the Clock. `duration_s` is never read in production code (Grep before compaction: only `runner.py:35`, `:110`, `:120`, `:129`). | `docs/designs/issue-watcher.md:235`, `:255-262`; `spec-final.md:231` | LOW |
| 10 | Necessary deviation | `src/superclaude/cli/issue_watch/record.py:310-315`, `audit.py:110-115`, `audit.py:200`, `audit.py:203`, `audit.py:204-206`, `launch.py:30` | Copies forced by design 5.3: `_fsync_dir` exists in both `record` and `audit`; `audit` has its own UTC format, `_MAX_ISSUE` and `_ENTRY_STATES`; `launch` has its own `MAX_ISSUE_NUMBER`. `audit` may import nothing and `launch` may import only `runner`. On the reuse question: do NOT consolidate `_fsync_dir`. Neither `record` nor `audit` may import the other, and moving operating-system I/O into the pure `predicates` module would break its "standard library only, no I/O" role. The function is 6 identical lines, and the copies cost less than a 5.3 amendment. | `docs/designs/issue-watcher.md:237`, `:239`, `:240`; `predicates.py:20`, `:23` | LOW |
| 11 | Authorized expansion | `src/superclaude/main.py:563-565` | `issue_watch_group` is registered eagerly, like `reflect`, while design 5.3 says `cli.py` "imports the package lazily from `main.py`". Authorized by DF-29 / OQ-21. `main.py` is the only existing source file the change touches. | `docs/designs/issue-watcher.md:244`; tasklist Open Questions (OQ-21) | LOW |

## Adherence summary

- Spec units audited: 18. These are NFR-001 to NFR-014, plus four architecture units: the design 5.3 import table, the design 5.4 four Protocols, the design 4.1 CLI surface and the design 4.3 exit table.
- Fully adherent: 13 (NFR-001 to NFR-013, at the level of the checks listed in Notes).
- Units with deviations: 5 (NFR-014, 5.3, 4.1, 4.3, plus design 10.1 / 10.2 through rows 1 and 7).
- Authorized expansion: 1 | Necessary deviation: 4 | Drift: 6 | Regression: 0

## Notes

- **Checked and found adherent.** Each item names the evidence behind it, so this is not a bare "no issues".
  - Python 3.10 floor: no `datetime.UTC`, `tomllib`, `StrEnum`, `except*`, `match`, `ExceptionGroup`, `Self` or `fromisoformat` anywhere in `src` or `tests`, and `from __future__ import annotations` is in all 8 modules.
  - `subprocess` appears only in `runner.py`.
  - The only third-party import is `click`, in `cli`.
  - Every `gh` command is pinned to `IronbellyOrg/IronClaude`, with no `{owner}` placeholder (`github.py:37`, `:75`, `:89`).
  - No issue title or body is fetched, and the claim marker is a jq boolean.
  - The prompt is built only from a validated `int`: `launch.py:90-92`, and `launch.py:101-102` refuses any other prompt.
  - `retry_argv` validates the operation id before `status` prints it as a shell command (`launch.py:127-130`).
  - `find_orca` skips relative `PATH` hits (`launch.py:184`).
  - The origin check uses `git -C` with no `cwd` (`launch.py:229`). The launch is the only call that passes `cwd` (`launch.py:355`).
  - File modes: the state directory is 0700, re-applied with `chmod` because `makedirs` is filtered by the umask (`record.py:777-778`). The lock file is created 0600 with `O_EXCL|O_NOFOLLOW` (`record.py:782-792`). The store and `dry-run.json` get `chmod` 0600 plus a directory fsync (`record.py:376-378`, `:863-865`). The audit log is opened 0600 with append (`audit.py:133`).
  - The lock opens with `O_NOFOLLOW`, then checks the file is regular, owned by the current user, the inode is unchanged and the link count is nonzero (`record.py:393-414`). It is released in a `finally`.
  - The exit-75 path never rotates the audit log (`cycle.py:679-683`, `cli.py:331`), matching `issue-watcher.md:720`.
  - `init-state` never overwrites (`record.py:773-775`).
- **Runbook claims checked against code (13).** Nine hold and one is wrong; three were checked as named in Deviation 6 and the Correctness gaps below.
  1. Five commands (`setup.md:59`, matching `cli.py:111`, `:164`, `:185`, `:201`, `:282`).
  2. `check-config` output (`:65`, matching `cli.py:195-198`).
  3. `init-state` modes, refusal and exit 6 (`:156`, matching `record.py:773-795` and `cli.py:208-214`).
  4. `not_enabled` before the lock (`:251`, matching `cycle.py:666-667`).
  5. `DISABLED` is checked first under the lock, also in a dry run (`:300`, matching `cycle.py:693-694`).
  6. `cycle_crashed` behaviour (`:331`, matching `cli.py:123-129`).
  7. Rotation at 5 MiB into `.1` to `.4` (`:410`, matching `audit.py:106-107`, `:150-155`).
  8. `status --json` fields and the 900-second health rule (`:432-443`, matching `cycle.py:1289-1298`).
  9. The retry command uses the bare `orca-ide` or `orca` name (`:525`, matching `cycle.py:1225-1230`).
  10. `reset` messages and exit codes (`:503-513`, matching `cli.py:309-345`).
  11. The platform list is incomplete (Deviation 6).
  12. `status` exit codes (Deviation 6).
  13. "Disabled since" for a dangling symlink is WRONG (Correctness gap 1).
- **Could not fully verify.**
  - NFR-001 to NFR-013 were checked through the specific hooks above, not clause by clause.
  - Whether `launch_cwd` can ever be None on an `unknown` entry that has an operation id (Correctness gap 4): I did not read `record.mark_pending`.
  - `github.classify` and `CallBudget` (around `github.py:345` and `:437`) were not read in this pass.
  - The `runner.py` and `main.py` citations come from Greps and Reads done earlier in this session, not re-read after the context was summarized.
- **Evidence pathologies.**
  - The 57-reason count in the spec and tasklist is stale; the code has 59, as the runbook states (`setup.md:344`).
  - The boundary test's docstring miscounts `record`'s imports (Deviation 2).

## Correctness gaps (advisory — non-gating)

| # | Correctness gap | Location | Sibling disagreement | Evidence (file:line) |
|---|-----------------|----------|----------------------|----------------------|
| 1 | Kill-switch state is reported inconsistently, and one error is uncaught | `src/superclaude/cli/issue_watch/record.py:421-431` | `disabled()` uses `lexists`, so a dangling `DISABLED` symlink stops cycles. `disabled_since()` uses `os.stat`, which follows the link, so `status` prints "disabled since: no" for that same file. This contradicts the runbook (`setup.md:298`, `:302`). A `DISABLED` symlink loop raises an OSError (ELOOP) that `status` does not catch, because it catches only `StoreError`. That gives a traceback and exit 1 (read as "unhealthy") instead of exit 6. | `record.py:423`, `record.py:428-430`; `cli.py:171-177` |
| 2 | Missing parity tests on copied bounds | `src/superclaude/cli/issue_watch/launch.py:30`, `cycle.py:468`, `audit.py:204-206` | `launch.MAX_ISSUE_NUMBER` decides what reaches the prompt (`launch.py:90`) and the `reset` argument (`cli.py:283`), but unlike `audit._MAX_ISSUE` it is not pinned to `predicates.MAX_ISSUE_NUMBER`. `cycle._LOGIN` is not pinned to `github._LOGIN_RE`. `audit._ENTRY_STATES` is pinned to a literal, not to `record.ENTRY_STATES`. | `predicates.py:20`; `github.py:134`; `tests/issue_watch/test_audit.py:473-484` |
| 3 | `reset` accepts a meaningless flag silently and prints a misleading message | `src/superclaude/cli/issue_watch/cli.py:309-313` | `reset --rate-limit --forfeit-guarantee` is accepted, and the `--forfeit-guarantee` flag is ignored. When neither ISSUE nor `--rate-limit` is given, the message says "not both". | `cli.py:311`; `docs/designs/issue-watcher.md:121` |
| 4 | Unknown entries can be silently missing from the retry list | `src/superclaude/cli/issue_watch/cycle.py:1271`, `cycle.py:1279-1280` | Design 10.2 lists every `unknown` entry that has an `operation_id`. The code also requires `launch_cwd`, and silently drops an id that `retry_argv` refuses, with no stale or warning signal. | `docs/designs/issue-watcher.md:739` |
| 5 | Stderr fallback does not check exit codes and mislabels reset lines | `src/superclaude/cli/issue_watch/audit.py:393-402` | It checks that the reason is in the table but not that the exit matches the table's exit for that reason. It always writes `"kind": "cycle"`, including for `reset_refused` and reset write failures, while `_write_reset` says reset never writes a cycle line. | `audit.py:402`; `cli.py:219`, `cli.py:264-266`, `cli.py:279` |

## Blind calibration (attached by the orchestrator; full report: reviewer-3-calibration.md)

- Reviewer model class: opus (persona refactorer). Calibrator class: opus (calibrator_diversity degraded; same class as the reviewer, independent instance without formation context).
- Calibrated confidence C = 0.76 (citation grounding 0.88, coverage completeness 0.70, deviation-classification clarity 0.78, risk surface 0.85, recommendation actionability 0.60). C < 0.85.
- Citation spot-check: 34 of 35 match; one wrong path: row 11 cites src/superclaude/main.py:563-565, the file is src/superclaude/cli/main.py:563-565.
- Weak spots: rows 1 (cycle_crashed, Drift) and 7 (cycle_complete, Necessary) classify the same kind of executor proposal differently on thin reasoning; rows 8 and 10 describe structure the design allows (closer to aligned); row 6 part (c) overlooks that design 10.2 (issue-watcher.md:726) itself lists status exits 0/1/6.
