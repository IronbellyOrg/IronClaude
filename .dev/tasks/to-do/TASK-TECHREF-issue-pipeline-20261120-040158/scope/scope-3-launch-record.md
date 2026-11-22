# Scope 3: issue watcher launch and state-record layer
**Scope:** src/superclaude/cli/issue_watch/launch.py, record.py (runner.py only where they are called)
**Source root:** /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6)
**Status:** Complete
**Date:** 2026-11-20
(All paths relative to the snapshot root; line numbers read from the snapshot.)
---

## 1. File inventory

| Path | Lines | Purpose | Key symbols (line) |
|---|---|---|---|
| src/superclaude/cli/issue_watch/launch.py | 370 | Find Orca, check worktree origin, build and run ONE `orca agent launch`; maps reply to `LaunchOutcome`. Writes no state, caches nothing (docstring 1-9). | `ORCA_AGENT="claude"` 28; `PROMPT_PATTERN` 33; `OPERATION_ID_PATTERN` 36; `OPERATION_ID_PATHS` 42; `OP_UNKNOWN_TEXT` 47; `ORIGIN_REPO` 50; `LAUNCH_DETAILS` 58; `build_claim_prompt` 84; `launch_argv` 95; `retry_argv` 119; `find_orca` 163; `parse_origin` 215; `check_origin` 233; `LaunchOutcome` 255; `Launcher` Protocol 277; `outcome_of` 326; `OrcaLauncher.launch` 358 |
| src/superclaude/cli/issue_watch/record.py | 865 | Dispatch record `dispatch.json`: schema, validation, migrations, `FileStore` (atomic save, flock lock, DISABLED switch), pure transition functions T-1..T-13, day-cap, dry-run shadow file. No clock, no commands (docstring 1-8). | `SCHEMA_VERSION=1` 31; `ENTRY_STATES` 34; `Entry` 69; `StoreDoc` 92; `PendingContext` 105; `validate` 213; `migrate` 251; `STORE_FILE/LOCK_FILE/DISABLED_FILE` 281-283; `Store` Protocol 318; `FileStore` 334 (`load` 347, `save` 370, `lock` 381, `disabled` 421, `disabled_since` 425); constants 434-448; `fail` 503; `backoff_elapsed` 528; `mark_pending` 538; `mark_launched` 580; `mark_unknown` 599; `mark_spawn_error` 620; `sweep` 627; `mark_claimed` 654; `day_cap_count` 699; `reset_entry` 706; `init_state` 753; `load_dry_run` 831; `save_dry_run` 851 |
| src/superclaude/cli/issue_watch/runner.py | 130 | Only module importing `subprocess`; `Runner` Protocol 38; `SubprocessRunner.run` 70 (shell=False 93, stdin DEVNULL 99, `cwd` 100); `CommandResult` 20; stderr cap 500 B (15). | |
| src/superclaude/cli/issue_watch/cycle.py (caller, not in slice) | 1406 | Config loader (`enabled` etc.) and the one cycle that calls launch + record. `_launch` 1026-1112; `load_config` 195; `Config` 97. | |

## 2. Behaviour map

### 2.1 What launch.py launches
- Command: `orca agent launch --agent claude --worktree path:<worktree> --surface terminal --prompt "<prompt>" --json`, a fixed 12-element argv: `launch_argv` launch.py:95-116. Retry form inserts `--retry-launch <id>` before `--json`: launch.py:119-132.
- Agent: the Orca agent id `claude` (Claude CLI, `--surface terminal`), "deliberately not configurable": launch.py:26-28.
- Prompt / pipeline level: only `/sc:issue --claim <n> --pipeline none` (n int 1..999999999): launch.py:33 (regex), :84-92 (builder), :101 (guard in `launch_argv`). So pipeline level is hard-coded `none`; the launched session runs the `/sc:issue --claim` command (assign, accuracy check, summary, next-step prompt) and stops there (no worktree/agent creation by that session; level semantics live in sc-issue-protocol, OUT OF SLICE).
- Worktree: launch.py does NOT create a worktree. It launches into one pre-existing, operator-configured checkout: `cfg.worktree` passed as `path:<worktree>` and as process `cwd` (OrcaLauncher.launch launch.py:358-370; "only call in the package that passes cwd" 363). cycle.py:1099 `d.launcher.launch(orca, cfg.worktree, prompt, LAUNCH_TIMEOUT_S)` with `LAUNCH_TIMEOUT_S=120.0` cycle.py:40. `worktree` is a required absolute-path config key: cycle.py:65, :257-259, :280; validated as existing dir `validate_setup` cycle.py:372-375.
- Orca discovery: `find_orca` probes each `_ORCA_CLIS` name via `shutil.which`, requires an absolute path (launch.py:195), runs `<path> skills list --json`, accepts only when topics contain `orca-cli` (`_lists_orca_cli` 144-160). `_ORCA_CLIS` is imported from `superclaude.cli.install_user_setup` (launch.py:22). Not cached.
- Origin guard: `git -C <worktree> remote get-url origin` must parse to `ironbellyorg/ironclaude` (lower-cased) else `origin_mismatch`: launch.py:50, :233-251. Called by cycle at cycle.py:721 (start) and :1074 (just before launch).
- Reply mapping `outcome_of` launch.py:326-349: spawn_error -> `spawn_error`; timeout / `agent_session_operation_unknown` text (OP_UNKNOWN_TEXT 47) / non-zero exit / non-JSON / missing id / invalid id -> `unknown` (keeps a valid id if parsed); exit 0 + JSON + valid id at `receipt.operation_id` (then `error.operation_id`) -> `launched`. Paths flagged `[PROPOSAL, UNVERIFIED]` launch.py:39-45.

### 2.2 Order of steps in cycle._launch (cycle.py:1026-1112)
1. dry-run: no probe, no Orca call, appends shadow launch only (1029-1035).
2. `find_orca` (1048) -> `orca_not_found` stop (1052). 3. `build_claim_prompt` (1054) -> `fail(prompt_invalid)`. 4. `_revalidate` (979-1016; re-read issue, labels, owner, approval event, project item) -> `fail(revalidation_transient)`. 5. day-cap recheck (1061), DISABLED recheck -> `disabled_mid_cycle` (1063). 6. launch deadline guards (1069-1079) + origin recheck (1074). 7. `mark_pending` then `_save()` BEFORE the launch call (1091-1092, FR-010). 8. Deadline recheck after save; if crossed, restore previous doc and save (1095-1098). 9. `launcher.launch` (1099). 10. `mark_launched` / `mark_unknown` / `mark_spawn_error` (1101-1112). Final write `_commit_store` 1128-1144 (`set_considered`, `set_last_completed`, `prune_consumed_log`, `store.save`).

### 2.3 Enabled-style switches
- `enabled` config key, default False, must be JSON bool: cycle.py:61, :228-230, `Config.enabled` 100. In `run`: `if not deps.config.enabled and not self.dry_run: raise _Stop("not_enabled")` cycle.py:685-686 (dry-run bypasses it).
- `DISABLED` file (kill switch): `state_dir/DISABLED`; `FileStore.disabled()` record.py:421-423 (`os.path.lexists`, a dangling symlink counts); `disabled_since` record.py:425-431 (mtime); module-level `disabled_present` record.py:748-750. Checked at cycle start (cycle.py:712) and again mid-launch (1063).
- Also: `owner_account_id` account pin (cycle.py:768), `state_dir` network-FS refusal (cycle.py:50, 271).
- Default state_dir: `${XDG_STATE_HOME:-~/.local/state}/superclaude/issue-watch` cycle.py:187-192; config key `state_dir` overrides 261-264. Default labels `issue-watch:trigger` / `issue-watch:approved` cycle.py:55-56.

### 2.4 Who reads the record afterwards (readers of `dispatch.json`)
Searched the whole snapshot (src, docs, hooks, scripts); `dispatch.json` appears as a code path only in record.py and cycle.py.
- `once` cycle: `FileStore.load` under lock, record.py:347-368 (cycle.py:742); `FileStore(config.state_dir)` built in cli.py:67 (`build_deps` 62).
- `status` / `status --json`: `cycle._read_store_doc` plain `open(..., "rb")`, no lock, no write (cycle.py:1231-1248); `status_report` cycle.py:1270-1335 builds counts, `stale` (unknown, or abandoned+pending_orphan, older than 24 h: `_is_stale` 1251-1259, `STALE_AGE_S=86400` cycle.py:46), `retry` list with a printable `retry_argv` for `unknown` entries that hold `operation_id` and `launch_cwd` (1308-1325), `healthy` = last_completed_cycle age <= 900 s (`HEALTH_AGE_S` cycle.py:45, 1327). CLI wiring cli.py:164-182.
- `reset N --forfeit-guarantee` / `reset --rate-limit`: cli.py:282-345 (`_reset_locked` 232-252 calls `record.reset_entry` / `reset_rate_limit`).
- `slo_numbers(lines, doc, now)` cycle.py:1359-1405 reads the store (`stale_count`) plus audit lines.
- NO hook reads `dispatch.json`. `src/superclaude/hooks/scripts/launch-level-guard.sh` (L1 guard) and `launch-job-identity.sh` read a DIFFERENT store, `~/.claude/state/launch-level/{sessions,jobs,pending}` (guard.sh:20-23; identity.sh:45,111,226,451), written by the claim script `skills/sc-issue-protocol/scripts/orca_worktree.py` (PENDING_PARTS 791, GUARD_COMMAND 837). Per claim.md:100,142-148 a `--pipeline none` claim creates no worktree and launches no agent, so (inference, not traced) the watcher's session is not a governed launch-level session. `skills/agent-work-report/scripts/common.py:22-25` reads a third file, `~/.config/superclaude/issue-watch.json` (key `orchestrator_repo`), not the store.
- The launched session's own "claim" is observed indirectly: the claim session posts a GitHub comment marked `<!-- sc:issue:claim -->` (claim.md:30); the watcher later reads it via `github.marker_comments` (cycle.py:905, 926) and moves the entry to `claimed` (T-10). The marker, not any file, closes the loop.

## 3. Record schema and state transitions

### 3.1 Files in state_dir (record.py:281-283, 805; modes per record.py:372-378, 777-801)
| File | Mode | Created by | Written by | Notes |
|---|---|---|---|---|
| `state_dir/` | 0700 | `init_state` makedirs + chmod (record.py:777-778) | - | default `~/.local/state/superclaude/issue-watch` (cycle.py:187-192) |
| `dispatch.json` | 0600 | `init_state` -> `FileStore.save` (795) | `once` (not dry-run), `reset` | `STORE_FILE` 281; JSON `sort_keys`, indent 2, ASCII, trailing newline (374-376) |
| `lock` | 0600 | `init_state` `O_CREAT\|O_EXCL\|O_NOFOLLOW` (782-784) | nobody (flock only) | `LOCK_FILE` 282 |
| `DISABLED` | operator | operator `touch` | - | `DISABLED_FILE` 283 |
| `dry-run.json` | 0600 | first dry-run | `save_dry_run` 851-865 | keys `schema_version, considered, shadow_launches` (806); invalid file is replaced by empty shadow + `dry_run_shadow_reset` warning (831-848) |
| `audit.jsonl`, `.1`-`.4` | 0600 | first append | `audit.AuditLog` (audit.py:124-128) | other slice |

### 3.2 `dispatch.json` document (record.py:92-101, 120-129, 297-307)
Top-level keys (exact set, `_STORE_KEYS` 120): `schema_version` (=1, 31), `created_at` (approval floor, set by `init_state`), `next_permitted_at`, `last_completed_cycle_at`, `considered` {issue-> UTC}, `consumed_log` [UTC], `entries` {issue-> Entry}. Times `YYYY-MM-DDTHH:MM:SSZ`; keys decimal strings `[1-9][0-9]{0,8}` (132).
Entry fields (all 17 always present, `Entry` 69-88; `_ENTRY_KEYS` 131): `issue, state, attempts, launches, operation_id, approver_id, approval_event_id, approved_at, launch_cwd, launch_login, launch_account_id, consumed_at, pending_at, created_at, updated_at, lease_expires_at, last_reason`.
Validation rules (`_entry` 168-210, `validate` 213-244): `issue` == key; `state` in `ENTRY_STATES` (34); `attempts` int >= 0; `launches` in {0,1}; `operation_id` matches pattern (183); `launch_cwd` absolute (184); `launches==1` needs `consumed_at` and `pending_at` (206); `failed` needs `launches==0` (208). `last_reason` only checked as str|null here; membership in the reason table is pinned by tests (docstring 221-224, DF-42; this module may not import audit).
Migrations: `MIGRATIONS` ships empty (247); `migrate` chains v->v+1 in memory (251-278); `load` never saves (DF-17, 345-368); cycle saves a migrated store only in a real cycle (cycle.py:746-747).

### 3.3 Atomic write, lock, crash recovery
- Save: `swarm/atomic.write_prepared_bytes` = `mkstemp` in same dir + fsync + `os.replace`, tmp unlinked on exception (src/superclaude/cli/swarm/atomic.py:14-39), then `chmod 0600` and dir fsync (record.py:370-378, `_fsync_dir` 310-315). Orphan `dispatch.json.*.tmp` after a crash is ignored (design issue-watcher.md C2 row, ~535).
- Lock: exclusive non-blocking `flock` on `state_dir/lock`; opens with `O_NOFOLLOW|O_CLOEXEC`; checks regular file + owner uid, then re-stats path vs fd (dev, ino, nlink) to detect replacement; errors `lock_missing`, `lock_invalid`, `LockHeld` (exit 75) (record.py:381-419). The lock is created only by `init_state`, never by `lock()`.
- Write order (cycle.py:1091-1099): `pending` saved durable BEFORE `launcher.launch`, so a crash after it yields `pending, launches=1` which `sweep` turns into `abandoned/pending_orphan` (record.py:627-651); no relaunch. At-most-once launch per approval.
- `init_state` refuses to overwrite (`StateExists` 64, 773-775) and removes a lock it created if the first save fails (796-801).

### 3.4 States and transitions (functions pure: take doc + now, return new doc; record.py)
States (34): `pending, launched, unknown, failed, abandoned, claimed`. Constants: `MAX_ATTEMPTS=3`, `BACKOFF=10 min`, `LEASE=60 min`, `DAY_CAP_WINDOW=24 h` (434-443); `_FAIL_REASONS` (446); `_CLAIMABLE={launched,unknown,abandoned}` (447); `_RESETTABLE={abandoned,unknown}` (448).
| # | From | Trigger | To | Function (line) |
|---|---|---|---|---|
| T-1/T-3 | none or failed | `prompt_invalid` / `revalidation_transient`; at attempts 3 -> abandoned `attempts_exhausted` | failed / abandoned | `fail` 503 |
| T-2 | failed | `now >= updated_at+10m` and attempts<3 | eligible again | `backoff_elapsed` 528 |
| T-4 | none or failed | all checks passed | pending (`launches`=1, `consumed_at`, `pending_at`, 6 ctx fields) | `mark_pending` 538 (ctx type `PendingContext` 105) |
| T-5 | pending | outcome launched | launched (+`operation_id`, `lease_expires_at`=now+60m) | `mark_launched` 580 |
| T-6 | pending | outcome unknown | unknown (keeps id if any) | `mark_unknown` 599 |
| T-7 | pending | spawn_error | abandoned `spawn_error` | `mark_spawn_error` 620 |
| T-8 | pending | found at cycle start (sweep) | abandoned `pending_orphan` | `sweep` 627 |
| T-9 | launched | lease expired, no marker | abandoned `claim_not_observed` | `sweep` 627 |
| T-10/11/12 | launched/unknown/abandoned; none; failed | own claim marker seen | claimed (terminal) | `mark_claimed` 654 |
| T-13 | abandoned, unknown | `reset N --forfeit-guarantee` | entry removed; `consumed_at` -> `consumed_log` | `reset_entry` 706 |
Any other pair raises `TransitionError` (`_refuse` 451). Day cap: `day_cap_count` 699 counts `consumed_at` + `consumed_log` in (now-24h, now]; `DAY_CAP=6` is cycle.py:36 (also `MAX_CANDIDATES=10` 34, `PROBE_TIMEOUT_S=10.0` 38, `GIT_TIMEOUT_S=10.0` 39; `Deadline` class 402; `_hit` marker check 848). `prune_consumed_log` 693. Setters: `set_next_permitted` 728, `set_last_completed` 733, `set_considered` 738.
Doc-vs-code: design `docs/designs/issue-watcher.md` section 7 tables (7.1-7.6) match code: [CODE-VERIFIED] for fields, T-1..T-13, constants, lock and save steps. The C1-C5 crash table is design text; code evidence is the write order above plus the tests in section 4.

## 4. Tests that pin this slice (tests/issue_watch/, snapshot)
- test_launch.py (952 lines, 66 tests): "Tests for the Orca launcher: prompt, argv, Orca probe and origin check (part A)"; all commands via `FakeRunner`. Groups: prompt 38; launch argv 72 (FR-013, threat T10); retry argv 157; Orca probe 217 (T17, DF-36, DF-54); origin parse 441 and check 500; Part B outcome table 677, unknown fixture/OQ-47 776, cwd 810, operation-id paths 865, agent pin 918, "claim prompt carries --pipeline none (Plan B Task 11)" 929. Fixtures `tests/issue_watch/fixtures/_assumed_shape` (test_launch.py:617-626).
- test_record.py (2377 lines, 147 tests): "dispatch record, part A: validation, migration, save, lock, kill switch". Groups: load 171, migrate 430, save 574, lock 700, kill switch 855; Part B T-1..T-13 plus every other pair raises, half-open windows, purity 895-1538; Part C day cap 1578, resets 1655, sweep 1686, init-state 1777, dry-run shadow 1929; Part D input guards, `set_considered` 2143-2377. Literal key lists are not read from the module, so adding a field fails the pin test (docstring 4-5).
- test_concurrency.py (275 lines, 6 tests): "Two processes on one store, and the lock-file failure modes (FR-017, AC-11)"; real `spawn` processes (146), symlinked/dir/missing/replaced lock (215-255).
- test_crash_injection.py (373 lines, 6 tests): "Crash injection at every write and spawn boundary of a launch (NFR-005, AC-17)"; C1 217, C2 238, C3 287, C4 310, launcher exception 327, C5 347; asserts launcher called at most once over 6 cycles.
- conftest.py (1155 lines, 0 tests): `FakeClock` 51, `FakeRunner` 74, `fake_runner` fixture 109, `FIXED_NOW`/`CRASH_POINTS` 124-126, `tmp_state` fixture 244 (real `init_state` under tmp_path, HOME/XDG moved inside), `CrashingStore` 129, `FailingStore` 188, `FakeLauncher` 251, `GhWorld` 528.
- Related, not read: test_cycle.py (4982), test_no_shell.py, test_module_boundaries.py (import-only rule of launch.py), test_security_invariants.py, test_origin_parity.py, test_find_orca_parity.py (parity with `install_user_setup._find_orca`), test_runner.py, test_cli.py.

## 5. Proposed deep-research assignments (2)

1. **Launch path and Orca contract** -> output `research/launch-path-and-orca-contract.md`. Files: issue_watch/launch.py, runner.py, cycle.py `_launch` 1026-1112 + `Deadline`/`validate_setup`, `install_user_setup._ORCA_CLIS`, `src/superclaude/skills/sc-issue-protocol/refs/claim.md` + `commands/issue.md` (what `--claim ... --pipeline none` does inside the session), docs/designs/issue-watcher.md section 8.4, tests test_launch.py, test_find_orca_parity.py, test_origin_parity.py, test_no_shell.py. Questions: exact launched session behaviour at level `none`; operation-id reply shape (marked UNVERIFIED in launch.py:39-45); deadline/timeout budget (LAUNCH_TIMEOUT_S 120, LAUNCH_CUTOFF_S 120); where the worktree is chosen (config only).
2. **Dispatch record, state machine and crash safety** -> output `research/dispatch-record-state-machine.md`. Files: issue_watch/record.py, cycle.py (`_examine` 915-961, `_sweep` 777+, `_commit_store` 1128, `status_report` 1270, config 195-283), cli.py (init-state, status, reset), swarm/atomic.py, docs/designs/issue-watcher.md section 7 and issue-watcher-setup.md sections on recovery, tests test_record.py, test_crash_injection.py, test_concurrency.py. Questions: full transition diagram with callers, marker-window rule (300 s), recovery runbook (`reset`, `DISABLED`), day cap value and reason table (audit.py).

## 6. Gaps
- [UNVERIFIED] Orca's real launch reply: `OPERATION_ID_PATHS` (launch.py:39-45) and `OP_UNKNOWN_TEXT` (47, "C16, UNVERIFIED") are assumptions pinned by `_assumed_shape` fixtures.
- Not traced: how the `/sc:issue --claim N --pipeline none` session behaves end to end (sc-issue-protocol, other slice); the claim marker rule `marker_time >= pending_at - 300s` lives in cycle.py `_hit` (~845-865) and predicates.py, not read here.
- Not read in depth: `Deadline` class body (cycle.py:402); `audit.REASON_TABLE`. `_ORCA_CLIS = ("orca-ide", "orca")` at install_user_setup.py:36 [CODE-VERIFIED]. Marker window (300 s) is in `_hit` cycle.py:848 and predicates.py, not read.
- "Pipeline level" is not configurable in this layer: no switch changes `none`; `--pipeline worktree|full` exist only in the manual `/sc:issue` path (hook guard messages cite them).
- Inference only: no hook governs the watcher-launched session (see 2.4); verify against launch-level-guard.sh binding logic and orca_worktree.py.
- Design doc `issue-watcher.md` cites C1-C5 crash rows; code comment `# C18` in record.py:372,853 refers to design decision C18 (import of `swarm.atomic` is lazy).
