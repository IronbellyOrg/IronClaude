# Variant 1 (architect): Run ledger script and its setup

Verified on this host (read-only): `run-list --json` gives `result.runs[]` (`id, objective, legacy (0/1 int), created_at, updated_at`); worker rows carry `resource.worktreeId` and `projection.workspace.id`, both exactly `<repoId>::<abs path>`, the same string as `worktree list --json` `result.worktrees[].id`; `worker-list` returns `result.page{limit,total,hasMore,nextCursor}`; Task statuses seen across all Runs: `completed` 644, `failed` 60, `blocked` 18, `ready` 12. `worker-list --run <unknown>` returns `ok:true` with zero workers (no error), while `task-list --run <unknown>` returns `run_not_found`. Hence "zero workers" is never proof a Run exists.

## Decision summary
1. New command group `superclaude run-ledger` (subcommands `build`, `add`, `show`, `path`) in a new package `src/superclaude/cli/run_ledger/`, registered in `src/superclaude/cli/main.py` next to `sweep_group` (same deferred-import pattern, line ~585). Not a standalone script: a console entry is installed by `superclaude install`, is testable, and cron/hook call one stable name.
2. Sweep reads the ledger itself: `superclaude sweep run` gains `--ledger/--no-ledger` (default: use ledger when no `--run` is given). The sweep skill stays limited to `superclaude sweep run`; sweep's Orca allowlist is untouched.
3. Ledger at a fixed per-user path `~/.superclaude/run-ledger/ledger.json` (override `SUPERCLAUDE_RUN_LEDGER`), not `.dev/coordinator/`.
4. Lock plus atomic rename; hook uses `add`, build uses a merge-under-lock.
5. Schedule: system crontab line shipped as a file; nothing installed.

## Q1 Code layout (all under `src/superclaude/cli/run_ledger/`)
- `__init__.py` exports `run_ledger_group` (click group).
- `commands.py`: CLI (`build`, `add`, `show`, `path`).
- `orca.py`: the only module that shells out (`subprocess.run([...], timeout=30, shell=False)`); functions `run_list()`, `worker_pages(run_id)`, `task_list(run_id)`, `worktree_ids()`. Fixed templates only. Kept separate from `sweep/probes.py` so the sweep allowlist test (`tests/sweep/test_probes_allowlist.py`) stays valid.
- `rules.py`: pure function `decide(runs, workers_by_run, tasks_by_run, live_worktree_ids, prev_ledger, now) -> list[Entry]`. No I/O; this is the extension seam (new rule = new `reason` string plus a branch).
- `store.py`: path resolution, lock, atomic read/write, schema validation.
- Hook script source: `src/superclaude/hooks/scripts/run-ledger-record.sh`; schedule file: `src/superclaude/templates/run-ledger.cron.example`.
- Tests in `tests/run_ledger/` (see Test plan). Install: `make sync-dev` copies hooks and templates to `.claude/`; `superclaude install` copies them to `~/.claude/hooks/` and `~/.claude/templates/`. The CLI is already on PATH after `superclaude install`, so cron calls `superclaude run-ledger build`.
- Never write `src/superclaude/` inside the hook or cron file; both call `superclaude run-ledger ...` only.

## Q3/Q4 Ledger file, schema, locking
Path `~/.superclaude/run-ledger/ledger.json`; lock file `ledger.lock` beside it. One path works from any worktree, so the hook firing in a worker worktree reaches it. `.dev/coordinator/` is rejected: it exists in one worktree only and a hook in another worktree would write a different file.

Schema (version 1):
```json
{"schema":1,"built_at":"2026-11-27T10:00:00Z","build_ok":true,
 "counts":{"runs_listed":63,"included":3,"worktrees_listed":N},
 "runs":[{"id":"run_20a750dbf442","reasons":["live_worktree","unfinished_task","created_since_build","hook_added"],
          "added_at":"...","source":"build|hook","last_seen_active":"..."}]}
```
`reasons` is a non-empty subset of those four strings. `run_legacy_local` (legacy=1 or id `run_legacy_local`) is never written.

Locking: `fcntl.flock(fd, LOCK_EX)` on `ledger.lock` (Linux/macOS; Windows UNVERIFIED and out of scope). Every writer does: acquire lock (blocking, 10 s timeout, else exit 3 and leave the file untouched) -> read current ledger -> compute new content -> write `ledger.json.tmp.<pid>` in the same directory -> `fsync` -> `os.replace` -> release. The Orca reads of a build happen BEFORE taking the lock (they take ~10-50 s), and the build merges under the lock: its result is the rebuilt set union any entry with `source=="hook"` and `added_at > build_started_at`. That closes the lost-append race: a Run added by the hook while a build is running survives.

## Q5 Exact inclusion rules (`rules.py`)
Let `LIVE` = set of `worktrees[].id` from one `orca worktree list --json` taken at build start. A Run (non-legacy) is IN if any:
- `live_worktree`: any worker row has `resource.worktreeId` in `LIVE` (exact string equality; also check `projection.workspace.id`, either match counts). No path normalisation, no suffix matching: ids are `<repoId>::<abs path>` on both sides (verified). A row with null `worktreeId` does not match.
- `unfinished_task`: `task-list --run <id> --json` has any task whose `status` is not in the terminal set `{completed, failed, cancelled}`. Observed non-terminal: `ready`, `blocked`. Any unknown status counts as unfinished (fail toward inclusion). `cancelled` and other names (`pending`, `dispatched`, `running`) are UNVERIFIED; only 4 statuses were seen. Whether `blocked` should keep an old Run alive forever (18 exist) is an owner decision; default: yes, include, and report the number of blocked-only Runs in `build` output so the owner can see the cost.
- `created_since_build`: `created_at` > previous ledger `built_at` (if no previous ledger: > now minus 24 h). Always in, even with no workers.
- `hook_added`: preserved from the previous ledger only while `now - added_at < 24 h` (then re-evaluated by the three rules above), so hook entries cannot live forever.
A Run matching none is OUT. Workers are paged: `worker-list --run <id> --json --limit 100`, follow `page.nextCursor` while `page.hasMore` is true, cap 20 pages (more = FAIL). Cost control: skip `worker-list` once a Run already has `live_worktree`; run `worker-list` for a Run only when it has no unfinished task and was not created since build, saving most of the 63 calls' paging.

Failure and implausible-result rules (keep old ledger, print reason to stderr, exit non-zero):
- any Orca call non-zero exit, timeout, invalid JSON, or `ok != true` -> exit 1;
- `run-list` returns 0 non-legacy Runs while the old ledger had >0 -> exit 4 (implausible);
- `worktree list` returns 0 worktrees (the main checkout is always listed) -> exit 4;
- new `included` is 0 while the old ledger had >= 1 AND at least one Run was created or updated within 24 h -> exit 4;
- shrink guard: new included < 20% of old included when old >= 5 -> exit 4. `--force` bypasses guards 3 and 4 only, never an Orca failure.
Exit codes: 0 ok, 1 Orca failure, 2 usage, 3 lock timeout, 4 implausible.
`build` flags: `--dry-run` (print, do not write), `--json`, `--ledger PATH`, `--timeout SECONDS` (default 120 aggregate), `--force`.

## Q2 How sweep consumes the ledger
In `src/superclaude/cli/sweep/commands.py` add `--ledger PATH` (default: the ledger path; used only when no `--run` is given and no Run is bound to the terminal). The code loads ids with `run_ledger.store.read_ids()` (pure file read, no Orca call), validates each with `probes.RUN_ID_RE`, and sweeps them. Missing/corrupt/`build_ok:false` ledger: exit 2 with "run ledger missing or stale: run `superclaude run-ledger build`"; stale = `built_at` older than 3 h (print a warning, still sweep, add a line to the report header). An explicit `--run` always wins. No change to `ALLOWED_ORCA`. Alternative rejected: coordinator expanding ids into `--run` args needs `show` outside the sweep skill's single-command allowlist.

## Q6 Scheduling recommendation
Recommend a system crontab entry, shipped as `src/superclaude/templates/run-ledger.cron.example`:
`*/45 * * * * flock -n ~/.superclaude/run-ledger/cron.lock superclaude run-ledger build >> ~/.superclaude/run-ledger/build.log 2>&1`
Reasons: survives session restart; no model; Orca-automation behaviour (survives Orca restart, can run a shell command) is UNVERIFIED; session-only cron dies with the session. Cron needs `orca` on PATH (set `PATH=` in the file). Failure visibility: non-zero exit plus `build.log`; sweep warns when stale. Nothing is installed by this work; the owner gives a go, then runs `crontab -e` and pastes the line. Fallback if Orca needs a desktop session socket UNVERIFIED: run the same line from a session cron.

## Q7 Hook design and install
PostToolUse, matcher `Bash`; script `run-ledger-record.sh`: read stdin JSON with `jq`; proceed only if `.tool_input.command` matches `orca orchestration (run-create|worker-start)`; fail open (always exit 0, never block); extract the Run id from `.tool_response` text using the regex `run_[0-9a-f]{12}` (first match); if found run `superclaude run-ledger add <id> --source hook` (flock'd, idempotent, validates the id shape, silent). If no id is found, log one line to `~/.superclaude/run-ledger/hook.log` and exit 0 (the next build catches it via `created_since_build`). What `run-create --json` and `worker-start` actually return to the hook is UNVERIFIED: the Claude Code PostToolUse payload shape for Bash (`tool_response`) and whether `run-create` prints the id need a test. Plan: a unit test feeding a recorded fixture payload; a real check needs a throwaway Run, which this task must not create, so ask the owner for permission to run one `run-create` or capture the shape from an existing Run-create transcript. If the id is not in the output, drop the hook and rely on the 45-minute build (decision recorded; cost: at most 45 min of a missing Run).
Install (after owner go): `superclaude install` copies the script to `~/.claude/hooks/run-ledger-record.sh`; the owner then adds to `~/.claude/settings.json` `hooks.PostToolUse` an entry `{"matcher":"Bash","hooks":[{"type":"command","command":"~/.claude/hooks/run-ledger-record.sh"}]}`. We do not edit settings.json. `src/superclaude/cli/install_hooks.py` registration is only added if the owner wants it automated.

## Test plan (`tests/run_ledger/`, fake `orca` via an injected runner returning fixtures; no real Orca)
`test_rules.py`: `test_live_worktree_run_in`; `test_deleted_worktrees_only_run_out`; `test_unfinished_task_run_in` (parametrised over `ready`, `blocked`, unknown status `weird`); `test_completed_failed_only_run_out`; `test_new_run_since_build_in`; `test_new_run_without_previous_ledger_uses_24h`; `test_run_legacy_local_out` (id and `legacy=1`); `test_worktree_id_exact_match_only` (same path, different repoId, no match); `test_null_worktree_id_no_match`; `test_hook_entry_expires_after_24h`.
`test_build.py`: `test_orca_failure_keeps_old_ledger_exit1` (byte-identical file, mtime unchanged); `test_invalid_json_keeps_old_ledger`; `test_empty_run_list_implausible_exit4`; `test_empty_worktree_list_implausible_exit4`; `test_shrink_guard_exit4_and_force_bypass`; `test_force_does_not_bypass_orca_failure`; `test_worker_list_pagination_follows_cursor` (3 pages); `test_pagination_cap_fails`; `test_dry_run_writes_nothing`; `test_first_build_no_old_ledger`.
`test_store.py`: `test_atomic_write_no_partial_file_on_crash` (monkeypatch `os.replace` to raise); `test_concurrent_add_and_build_no_lost_append` (multiprocessing, 20 adds during a slow build); `test_lock_timeout_exit3`; `test_corrupt_ledger_treated_as_missing_on_build_error_on_sweep`; `test_add_rejects_bad_id`; `test_add_idempotent`.
`test_sweep_ledger.py`: `test_sweep_uses_ledger_when_no_run`; `test_explicit_run_wins`; `test_missing_ledger_exit2_message`; `test_stale_ledger_warns`; and `tests/sweep/test_probes_allowlist.py` must still pass unchanged (guards that `run-list` never enters sweep).
`test_hook.py`: `test_hook_extracts_run_id_from_fixture`; `test_hook_ignores_other_commands`; `test_hook_no_id_logs_and_exits_0`; `test_hook_fails_open_when_superclaude_missing` (run via bash with a stubbed PATH).
Real-run acceptance (manual, read-only): `superclaude run-ledger build --dry-run --json` then `build`; report wall time (expect ~10-25 s: 63 `task-list` + about 25 `worker-list` calls at ~0.18 s) and then `time superclaude sweep run` (expected: 3 Runs, a few seconds). Both numbers UNVERIFIED until run.

## Risks and mitigations
- Orca JSON shape drifts (`legacy` int vs bool, `page` keys): `orca.py` validates required keys and raises `OrcaShapeError` -> exit 1, old ledger kept; fixtures recorded from real output.
- Blocked/failed leftovers keep dead Runs forever: counted in build output; owner decides; terminal set is one constant in `rules.py`.
- Unknown worker-list on bad id returns empty OK: never infer Run existence from it; use `run-list` as the universe.
- Cron environment lacks `orca` or its socket: `PATH` line in the cron file; `build.log`; sweep stale warning.
- Hook payload lacks the id: `build` already includes new Runs; hook dropped with reason.
- Two builds overlapping: `flock -n` in cron line plus ledger lock.
- Scope creep: no Run deletion, no `reset`, no Orca link flags, no settings edit, no commit.
