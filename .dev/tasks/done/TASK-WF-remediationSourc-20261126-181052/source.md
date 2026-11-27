<!-- Merged spec. Base: variant-2-sonnet-refactorer.md (Variant 2). Donor: variant-1-sonnet-architect.md (Variant 1). Plan: refactor-plan.md (14 changes). Merge date: 2026-11-26. -->
# Run ledger: requirements spec (IronbellyOrg/IronClaude#895)

Goal: `superclaude sweep run` must find Orca Run ids without a person naming them. A deterministic script (no model) rebuilds a Run ledger file from scratch every 30 minutes; a hook adds a new Run at once; sweep reads the ledger. Result file for this work: `.dev/issues/895/result.md`.

## Decisions summary
<!-- Source: Base (original, modified) - table added to satisfy the required section list; rows reflect Changes #1-#14 -->
| Q | Question | Decision |
|---|---|---|
| 1 | Code location and run | One new file `src/superclaude/cli/sweep/ledger.py`, command `superclaude sweep ledger`, attached to the existing `sweep_group` (no `main.py` change); pure `decide()`; own Orca runner, not `sweep/probes.py`. |
| 2 | How sweep consumes it | `sweep run` reads the ledger (file read, no Orca call) when no `--run` and no terminal-bound Run; explicit `--run` wins; no new flag; stale header at 90 minutes. |
| 3 | Ledger location | Fixed per-user file `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json`, override `--ledger` or env `SUPERCLAUDE_RUN_LEDGER`. Never under the repo. |
| 4 | Concurrency | Two writers (rebuild, hook `--add`): `fcntl.flock` sidecar lock, 10 s timeout then exit 3; atomic temp file + `fsync` + `os.replace`; rebuild merges hook entries newer than its own start. |
| 5 | Exact definitions | Three rules (live worktree, unfinished Task, new) over `run-list` non-legacy Runs; denylist of terminal statuses; whole-string worktree id match; paged `worker-list`; four implausible-result guards. |
| 6 | Scheduling | Recommend the system crontab every 30 minutes (`17,47`), as a repo doc for Coder#545 to adopt; nothing installed. Session cron is the fallback. |
| 7 | Hook | Delivered: PostToolUse `Bash` script via `superclaude install`; kept only if one scratch `run-create` shows the Run id in its output, else dropped with that reason and the fallback documented. Registration is Coder#545's. |

## Code layout and command surface
<!-- Source: Base (original, modified) - command renamed to `sweep ledger` and --add added per Change #3; the base's `run-ledger` command name and main.py line are replaced -->
- Builder and `decide()`: `src/superclaude/cli/sweep/ledger.py`. Tests: `tests/run_ledger/`. Hook: `run-ledger-record.sh` in the same `src/superclaude/hooks/` source folder as `require-orca-worktree-agent.sh` (exact subfolder to confirm in the code).
- Commands (subcommands of the existing `sweep` group; `main.py` untouched):
  - `superclaude sweep ledger [--ledger PATH] [--dry-run] [--json] [--accept-empty]`: rebuild. `--dry-run` prints the would-be ledger and writes nothing; `--json` prints the summary as JSON.
  - `superclaude sweep ledger --add <run_id>`: append one id (idempotent; validated with the sweep id pattern `probes.RUN_ID_RE`; merges under the lock; no Orca call).
  - No `show`, `path`, `--timeout`, `--no-ledger`, or sweep `--ledger` flag.
- A standalone script would not be on PATH after `superclaude install`; a subcommand is.
- The builder calls Orca through its own small runner (`subprocess.run([...], capture_output=True, timeout=30)`, fixed argv, no shell), never through `sweep/probes.py`, so the pinned `ALLOWED_ORCA` and `tests/sweep/test_probes_allowlist.py` stay unchanged and green. Calls used: `orca orchestration run-list --json`; `orca worktree list --json`; `orca orchestration task-list --run <id> --json`; `orca orchestration worker-list --run <id> --json --limit 100 [--cursor <c>]`.
- Orca binary: use `find_orca` in `src/superclaude/cli/issue_watch/` if its signature fits, else `shutil.which("orca")`.
- Exit codes: see "Failure and implausible-result rules".

## Ledger file and schema
<!-- Source: Base (original, modified) - schema extended with source/added_at, counts and stale-candidate fields per Changes #4, #10 -->
Orca Runs are global to the Orca server, not to a worktree; `.dev/coordinator/` in one worktree is invisible to a schedule or sweep started elsewhere and disappears with that worktree. Nothing to stage, nothing to gitignore. Version 1:
```json
{"version":1,"generated_at":"2026-11-26T18:00:00Z","orca":{"runs_listed":63,"worktrees_listed":12},
 "counts":{"live_worktree":3,"unfinished_task":9,"new":0,"hook_added":0,"main_checkout_only":0,
           "open_task_stale_7d_only":0,"blocked_only":0},
 "runs":[{"id":"run_915328e33d9a","created_at":"...","objective":"first 120 chars",
   "reasons":["live_worktree","unfinished_task","new","hook_added"],"source":"build","added_at":"...",
   "live_worktree_ids":["<repoId>::<path>"],"unfinished_task_count":0,
   "main_checkout_only":false,"stale_open_tasks_only":false}]}
```
- `generated_at` is captured BEFORE the first Orca call, so the `new` rule cannot miss a Run created mid-build. `reasons` is a non-empty subset of the four names; `source` is `build` or `hook`.
- `--add` keeps `generated_at` unchanged (so sweep staleness is not masked) and writes `source:"hook"`, `reasons:["hook_added"]`, `added_at`.

## Inclusion rules
<!-- Source: Base (original, modified) - 24 h fallback per Change #5 (Variant 1 Q5), universe rule per Change #11 (Variant 1), stale-candidate report per Change #10, measured facts added -->
Universe: Runs from `run-list` only, with `legacy == 0` and `id != "run_legacy_local"` (the only `legacy:1` Run on this host). Never infer that a Run exists from `worker-list`: for an unknown Run it returns `ok:true` with zero workers, while `task-list` returns `run_not_found`. A non-legacy Run is IN if any one reason holds:
- `live_worktree`: any worker row has `resource.worktreeId` exactly equal (whole string) to an `id` in `worktree list --json` `result.worktrees[].id`. Both are `<repoId>::<absolute path>` (verified); never split, normalise, or compare bare paths. A row with no `resource` or null `worktreeId` does not match.
- `unfinished_task`: any Task whose `status` is NOT in the terminal set `{completed, failed, cancelled}`. Observed on this host: completed 644, failed 60, blocked 18, ready 12. Denylist, not allowlist: an unseen status (`pending`, `dispatched`, `in_progress`; names UNVERIFIED) keeps the Run in rather than dropping live work. `failed` is terminal (counting it would keep old Runs forever). The terminal set is one constant.
- `new`: `created_at >= previous_ledger.generated_at`. With no previous ledger, or an unreadable one, `new` means `created_at` within the last `NEW_FALLBACK_HOURS = 24` (named constant).
- A hook-added entry newer than the rebuild start is kept (see Concurrency); an older one is re-evaluated by the three rules like any other Run.
- Rules stay as the issue defines them: a worktree Orca still lists, including the main checkout, counts. No age cutoff and no main-checkout exclusion is built (over-inclusion is the safe direction); a cutoff is the owner's decision (see Open decisions).

Measured on 2026-11-26 on this host: 63 Runs listed, 62 non-legacy; 10 admitted (3 by live worktree, 9 by Task, 2 by both), not the 3 the issue assumed. Rebuild without the short-circuit took 26.1 s (about 0.18 s per Orca call; 62 `task-list` calls plus `worker-list` pages, about 8 at limit 100); sweeping every Run took 48.6 s and a 3,666-line report.

Pagination: loop `worker-list` while `result.page.hasMore` is true, passing `--cursor result.page.nextCursor` with `--limit 100`. A repeated cursor, or more than 50 pages for one Run, is a failure (exit 1). `task-list` returned all Tasks in one response (`result.tasks[]`, `count`); behaviour above 100 Tasks is UNVERIFIED.
Short-circuit: fetch Tasks first; fetch workers only for Runs not already IN by Task or `new`.

Report (stdout summary and the ledger `counts` and per-run fields): per-reason counts; Runs admitted only through the main checkout (`isMainWorktree`); Runs admitted only by `ready` or `blocked` Tasks whose `updated_at` is older than 7 days; the count of Runs held in only by `blocked` Tasks. These show the owner the cost; they change no rule.

## Failure and implausible-result rules
<!-- Source: Base (original, modified) - guard 4 clause per Change #6, exit codes per Change #7, orca-not-found text per Change #9 -->
On any of these the old ledger is left untouched, one reason goes to stderr (first word `orca-failure:` or `implausible:`), and the exit is non-zero. The whole new ledger is built in memory first; an exception before the write leaves the disk untouched.
1. Any Orca call exits non-zero, times out (30 s each), or returns JSON without `"ok": true` (`orca-failure:`). If the binary is missing or Orca is not running the text names "orca not found or Orca app not running".
2. `worktree list` returns 0 worktrees (the main checkout always exists, so 0 is a broken read) (`implausible:`).
3. `run-list` returns 0 Runs while a previous ledger exists (`implausible:`).
4. The new ledger has 0 Runs, the previous ledger had at least 1, at least 1 non-legacy Run exists, AND at least 1 non-legacy Run was created or updated within 24 h (`implausible:`). `--accept-empty` overrides this guard only, never an Orca failure.

Exit codes: 0 written; 1 Orca failure or implausible result; 2 usage (including `--add` with a malformed id); 3 lock timeout. No 20% shrink guard. Ceiling: a partial read that returns a plausible non-empty list is not caught; add a shrink guard if one is ever seen.

## Concurrency and write method
<!-- Source: Variant 1 (sonnet:architect), Section Q3/Q4 - merged per Change #4 (simplified: no separate hook-entry expiry) -->
Two writers exist (the schedule's rebuild and the hook's `--add`), so a lock is required (the base's no-lock design is replaced).
- Sidecar lock file `run-ledger.lock` beside the ledger, `fcntl.flock(LOCK_EX)`, blocking up to 10 s, then exit 3 with the ledger untouched (Linux/macOS; Windows UNVERIFIED and out of scope).
- A rebuild does all Orca reads first (about 26 s) without the lock, then takes the lock, re-reads the ledger, and writes the rebuilt set plus every entry with `source == "hook"` and `added_at >= generated_at`. A hook entry older than that is re-evaluated by the three rules. This closes the lost-append race.
- Every write: temp file `run-ledger.json.tmp.<pid>` in the same directory, `fsync`, `os.replace`; readers see the old or the new file, never half. No `.tmp` residue after a failure.
- `--add` on a missing or unreadable ledger writes nothing and exits 1 with `implausible:` (the first build picks the Run up through the 24 h `new` fallback).

## Sweep consumption
<!-- Source: Base (original, modified) - stale threshold 90 minutes, `sweep ledger` hint, docs and skill text per Changes #13, #14 (#895) -->
- `src/superclaude/cli/sweep/commands.py`: when no `--run` is given and no Run is bound to the terminal, read the ledger (`json.load`, zero Orca calls), validate each id with `probes.RUN_ID_RE`, and sweep them. Explicit `--run` always wins and the ledger is then not read (the existing flag; a person naming a Run is not the guessing problem; #895 says "from the ledger only" for the coordinator's case). No new flag; env var `SUPERCLAUDE_RUN_LEDGER` serves tests.
- Report header: "Run ids from the Run ledger built <time>". When `generated_at` is older than 90 minutes (the #895 threshold, three missed 30-minute builds) the header adds "ledger is N min old"; sweep still runs (a stale list beats none).
- Missing or corrupt ledger: exit 2 with the old "no Run bound" message plus `run "superclaude sweep ledger" first`. A malformed id in the ledger is rejected by `RUN_ID_RE`.
- Sweep's `ALLOWED_ORCA` is unchanged. The sweep skill still runs only `superclaude sweep run`, so its `Bash(superclaude sweep run:*)` permission is unchanged.
- Docs and skill text: edit `src/superclaude/commands/sc/sweep.md` (the `--run` row and the "no Run is bound" sentence) and `src/superclaude/skills/sc-sweep-protocol/SKILL.md` to say ids come from the ledger when none is given; use installed paths only inside those texts (never `src/superclaude/`); then `make sync-dev`.

## Hook
<!-- Source: Variant 1 (sonnet:architect), Section Q7 - merged per Change #1 (replaces base "drop it") and Change #2 (test and drop rule) -->
### Design
- PostToolUse, matcher `Bash`; script `run-ledger-record.sh`, delivered to `~/.claude/hooks/` by `superclaude install` (as `require-orca-worktree-agent.sh` is).
- Reads stdin JSON with `jq`; acts only when `tool_input.command` runs `orca orchestration run-create` or `worker-start`. Takes the first `run_[0-9a-f]{12}` found in the Bash result text (for `worker-start`, also in the command's `--run` value) and calls `superclaude sweep ledger --add <id>`.
- Always exits 0 (fail open, never blocks). If no id is found it appends one line to `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger-hook.log`; the next rebuild catches the Run through `new`.
- Registration is not ours: Coder#545 registers it (see next section for the entry). We never edit `~/.claude/settings.json`.

### Payload test and drop rule
- Before building the hook: run exactly one `orca orchestration run-create --objective "scratch Run for the run-ledger hook payload test, safe to ignore" --json`, keep its stdout as a test fixture, and check the Claude Code PostToolUse Bash payload shape (`tool_response`) in the official docs.
- Decision, written in the result: Run id present in the output means the hook is delivered; absent means the hook is dropped with that reason and the fallback is documented (the coordinator runs `superclaude sweep ledger` right after `run-create`, about 26 s, no hook). This creates exactly one Run that Orca cannot delete; flag it in the result. The run needs the owner's go (see Open decisions).
- Fixture: a recorded payload under `tests/run_ledger/fixtures/`; the hook tests below feed it. What `run-create` prints is UNVERIFIED until this run.

## Schedule and install notes doc
<!-- Source: Variant 1 (sonnet:architect), Sections Q6/Q7 - merged per Change #8 (base Q6 modified: doc for Coder#545, flock -n, PATH) -->
Ship `docs/user-guide/run-ledger.md` for Coder#545 to adopt. Nothing is installed or registered by this work. It holds:
- Schedule recommendation: system crontab, every 30 minutes at offset minutes (`17,47`), wrapped in `flock -n` on a lock file, command `superclaude sweep ledger`, with an explicit `PATH` including the directory of the Orca CLI shim; output appended to a log under `${XDG_STATE_HOME:-~/.local/state}/superclaude/`. Why: survives session and Orca restarts, needs no model, exits non-zero with a logged reason. A session-only cron dies with the session (the problem); an Orca automation adds a dependency (whether it runs non-model commands is UNVERIFIED).
- Hook registration entry for Coder: `{"matcher":"Bash","hooks":[{"type":"command","command":"~/.claude/hooks/run-ledger-record.sh"}]}` under `hooks.PostToolUse`.
- Install notes, stated plainly: in Coder the crontab is rewritten on every boot, so a hand-edited crontab is lost; the schedule and the hook registration are registered by Coder#545, not by us.
- The pre-install check (next section) and the session-cron fallback (the same line from a session cron if Orca needs a desktop session socket, UNVERIFIED).

## Pre-install check
<!-- Source: Variant 1 (sonnet:architect), Section Q6 - merged per Change #9 (A-001 QUALIFY) -->
Before the cron line is registered, `env -i HOME=$HOME PATH=<the cron PATH> superclaude sweep ledger --dry-run` must exit 0. It proves the stripped cron environment finds `superclaude` and reaches Orca (the stripped-environment call worked in the debate evidence). If it fails, the message names "orca not found or Orca app not running" (exit 1, old ledger kept). Also check `command -v superclaude` on the target host (the pipx path is UNVERIFIED there). Include this check in the doc and in the result.

## Tests
<!-- Source: Base (original, modified) - ten base tests kept, 12 added from Variant 1 per Change #12; test_new_run_in adjusted for Change #5 -->
Fake `orca` via a `monkeypatch` of the runner; no real Orca. Files under `tests/run_ledger/`. `tests/sweep/test_probes_allowlist.py` must stay unchanged and passing.
- `test_live_worktree_run_in`: worker `worktreeId` equal to a listed id gives `live_worktree`.
- `test_deleted_worktrees_only_run_out`: all worker ids absent from the list, all Tasks completed, old `created_at` gives OUT.
- `test_unfinished_task_run_in`: `ready`, `blocked`, `in_progress`, `some_unknown_status` give IN; `completed`, `failed`, `cancelled` give OUT.
- `test_new_run_in`: `created_at` after previous `generated_at`, no workers or Tasks, gives IN with `new`.
- `test_new_fallback_24h_when_no_previous_ledger`: with no or unreadable previous ledger, a Run under 24 h old is IN and an older one is OUT.
- `test_legacy_run_out`: `run_legacy_local` and any `legacy:1` Run are OUT even with a live worktree.
- `test_worktree_id_exact_match_only`: same path, different repoId, no match. `test_null_worktree_id_no_match`.
- `test_orca_failure_keeps_old_ledger`: non-zero exit, timeout, `ok:false` leave the file bytes unchanged, exit 1.
- `test_implausibly_empty_keeps_old_ledger`: guards 2 to 4; `--accept-empty` overrides guard 4 only; guard 4 needs a Run created or updated within 24 h.
- `test_worker_list_pagination`: three pages via `hasMore` and `nextCursor`; a repeated cursor fails.
- `test_atomic_write`: a failure inside `os.replace` leaves the old file and no `.tmp` residue.
- `test_add_idempotent_and_rejects_bad_id`; `test_lock_timeout_exit3`; `test_concurrent_add_and_build_no_lost_append` (multiprocessing, 20 adds during a slow build).
- `test_sweep_reads_ledger_when_no_run`: ledger ids used; explicit `--run` ignores the ledger; missing ledger gives exit 2 and the hint; malformed id rejected by `RUN_ID_RE`.
- `test_corrupt_ledger_on_sweep_gives_exit2_hint`; `test_stale_ledger_header_in_sweep` (over 90 minutes adds "ledger is N min old").
- Hook: `test_hook_extracts_run_id_from_fixture`; `test_hook_ignores_other_commands`; `test_hook_no_id_logs_and_exits_0`; `test_hook_fails_open_when_superclaude_missing` (bash with a stubbed PATH).

## Real-run acceptance and what to report
<!-- Source: Base (original, modified) - delivery steps and timings updated with measured facts and hook step per Changes #2, #10 -->
Steps: (1) edit under `src/superclaude/` only, then `make sync-dev`; never stage `.claude/`; stage `.dev/tasks` if a task package is created. (2) `uv run pytest tests/run_ledger tests/sweep -v`. (3) `uv run superclaude sweep ledger --dry-run`, then a real write to a temp `--ledger`, then `SUPERCLAUDE_RUN_LEDGER=<temp> uv run superclaude sweep run`. (4) The hook payload capture (after the owner's go). (5) Nothing installed; no commit until the owner says so.
Report in `.dev/issues/895/result.md`: ledger written (path, counts); rebuild wall time against the 26.1 s baseline; sweep time over the ledger against 48.6 s and 3,666 lines for all Runs, and that it ran without "no Run bound"; per-reason counts and the stale-candidate figures; the hook decision with the fixture evidence; that exactly one scratch Run was created (if it was); test results; the pre-install check result.

## Risks and ceilings
<!-- Source: Base (original, modified) - hook risks and lock added per Changes #1, #4, #6, #10 -->
- Hook plus lock add a second writer (highest risk). Rollback: delete the hook script and the `--add` branch; the rebuild alone still meets every other criterion.
- Unknown Task status names: the denylist keeps the Run in; a wrongly open Run only costs sweep time.
- Stale leftovers: a Run whose only open Task is a stale `blocked` or `ready` one stays in until that Task is settled (the cost is reported, no cutoff built).
- A Run with live work but a worktree Orca no longer lists, and no open Task, drops out: accepted by the issue's rule.
- A Run created and finished between two builds never enters: harmless.
- Partial read with a plausible non-empty list is not caught (no shrink guard).
- Clock: single host; an NTP step back could re-admit a few Runs as `new` (harmless).
- Cron environment lacking `orca`: caught by the pre-install check; a dead schedule shows as the 90-minute stale header.
- Helper fit of `find_orca` is UNVERIFIED until implementation. The Orca JSON shape (`legacy` int, `page` keys) is verified only on this host.

## Open decisions for the owner
<!-- Source: Base (original, modified) - section added for required list; items from Changes #2, #10 -->
1. Age cutoff for stale Runs: none is built. Of the 10 admitted, some are held only by old `ready` or `blocked` Tasks or only by the main checkout. Choose to keep (default), or give a cutoff (for example Task `updated_at` older than N days).
2. Creating the one scratch Run for the hook payload test: it cannot be deleted. Answer yes (hook decided by the fixture) or no (the hook is built from the documented payload shape with the id-absent fallback, UNVERIFIED).

## Out of scope
<!-- Source: Base (original, modified) - constraints from the seed brief restated; non-changes from the plan -->
- Constraints kept: UV only (`uv run ...`, never `python -m` or bare `pip`); edit under `src/superclaude/`, then `make sync-dev`; never stage `.claude/`; no hardcoded `src/superclaude/` paths in installed primitives (installed paths only: `~/.claude/hooks/...`, `~/.claude/skills/...`, `~/.claude/commands/sc/...`); no `orca orchestration reset`, no Run delete; no Orca link flags (`--issue`, `--pr`); no `~/.claude/settings.json` edit; no crontab edit; nothing scheduled; no commit.
- Not built: a package of modules, `show`, `path`, `--timeout`, `--no-ledger`, a sweep `--ledger` flag, a `~/.superclaude/` ledger path, a 20% shrink guard, more exit codes, excluding the main checkout, any age cutoff.
- Not touched: `sweep/probes.py` and `ALLOWED_ORCA`; Windows locking.

## Reflect Verdict State (regeneration input; appended after the first review of the plan built from the text above)
The first plan built from this spec was reviewed and failed with 6 blocking findings. The new plan must contain none of the defects below. Where this section and an earlier section disagree, this section wins.

### Blocking findings to fix
- B-1: A task check may not forbid importing `probes` while another task imports from it. The ledger module makes no Orca call through `probes` and imports only the names `RUN_ID_RE` and `parse_time` from it; a named test (an AST check of the import names) enforces this.
- B-2: A documentation check may not demand that every command and flag the doc names exists in `superclaude sweep ledger --help`, because the doc must also name `flock -n`, `env -i`, `command -v` and a crontab. The check covers `superclaude` commands and flags only.
- B-3: A step must stage the task package: after the last artifact is written, run `git add .dev/tasks` (staging is not committing). The package `./artifacts/` folder is the package's own, never the project-root `artifacts/`.
- B-4: The sweep change appends a hint to the "no Run bound" and "Orca unavailable" messages, and existing tests assert those messages exactly (tests/sweep/test_cli_contract.py, the cases that check the exact stderr text). The plan must name those test cases and update their expected text to include the hint; the spec, not the tests, decides the wording.
- B-5: Adding `run-ledger-record.sh` to `_FRESHNESS_SCRIPTS` in src/superclaude/cli/install_hooks.py breaks the existing install tests unless the hard-coded seed list of script names in tests/cli/test_install_hooks.py also names it. The hook task updates that seed list.
- B-6: Orca timestamps come in two forms, SQLite `YYYY-MM-DD HH:MM:SS` and ISO with `Z` or an offset (`probes.parse_time` reads both). Every rule that compares times (`new`, the 24 h fallback, `added_at >= generated_at`, Task age) compares parsed UTC datetimes through `probes.parse_time`, and a test feeds both forms.

### Findings that counted toward the route (the new plan must not repeat them)
- Labelled HIGH: B-4, B-5 and B-6 above.
- M-1: Where a task creates the scratch Run on the authority of the owner's brief, it quotes the brief's sentence verbatim ("first test what such a hook actually receives from run-create"), and the final report names that authority.
- M-2: `decide` takes no hook entries (none newer than `generated_at` can exist in the previous ledger). The locked merge replaces an existing row with the same Run id, names the winning row, unions the reasons and recomputes `counts` after the merge.
- M-3: When the scratch `run-create` cannot be made, the decision file ends `Decision: deliver`, marked UNVERIFIED, and records zero scratch Runs created, where the fixture came from, and an UNVERIFIED marker separate from the `Decision:` line.
- M-4: Task age comes from the Task's own timestamp. When the field is absent the stale flag is null (unavailable); it never falls back to the Run's `updated_at`.
- M-5: `main_checkout_only` means the Run is admitted only through a main-checkout worktree: its only reason is `live_worktree`, at least one worktree matched and every matched worktree is the main checkout.
- M-6: A valid ledger with an empty `runs` list is sweepable: sweep proceeds with an empty Scope and the header line, exit 0, with a named test.
- M-7: The real-run sweep runs from a terminal where the Run binding lookup fails, or the report header shows that the ledger path was taken, because the scratch Run binds the terminal that created it.
- M-8: Ledger ids are validated with `re.fullmatch` and deduplicated by reusing `_check_run_ids` or an equivalent in the ledger reader.
- M-9: The import rule of B-1 is an exact allowlist of names.

### Corrections to earlier sections
- The command file to edit is `src/superclaude/commands/sweep.md` (there is no `commands/sc/` folder in the source tree); the skill is `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, whose pinned sentence "adds no flag, reads no environment variable and has no worker mode" must stay.
- Do not reuse `find_orca` from `src/superclaude/cli/issue_watch/launch.py`: it needs that package's runner and an extra `orca skills list --json` probe. Use `shutil.which("orca")`.
- The sweep-reading tests live in `tests/sweep/` because `tests/sweep/conftest.py` already fakes the Orca seams there and blocks process starts; the other new tests live in `tests/run_ledger/`.
- Source issue: IronbellyOrg/IronClaude#895; the schedule and the hook registration are Coder#545's. The result file is `.dev/issues/895/result.md`.
