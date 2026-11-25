# Scope 1: issue watcher orchestration layer (cycle.py, runner.py, cli.py, __init__.py, design doc)
**Scope:** src/superclaude/cli/issue_watch/{cycle,runner,cli,__init__}.py + docs/designs/issue-watcher.md (snapshot root /home/coder/.cache/ic-snap-20261120/master, origin/master 61ac2c2e6)
**Status:** Complete
**Date:** 2026-11-20
---

All paths below are relative to the snapshot root unless absolute.

## 1. File inventory

| Path | Lines | Purpose |
|---|---|---|
| `src/superclaude/cli/issue_watch/__init__.py` | 0 (empty) | Package marker only. No exports, no side effects. |
| `src/superclaude/cli/issue_watch/runner.py` | 130 | Only module in the package that imports `subprocess`. `shell=False`, stdin `DEVNULL`, UTF-8 `errors=replace`, stderr capped. |
| `src/superclaude/cli/issue_watch/cli.py` | 348 | Click group `issue-watch` (5 verbs), `build_deps`, exit-code mapping. No business logic, no `subprocess`. |
| `src/superclaude/cli/issue_watch/cycle.py` | 1406 | Config + validators (part 1, l.34-483), one poll cycle `_Cycle` (part 2, l.485-1222), status report + SLO reducer (part 3, l.1225-1406). |
| `docs/designs/issue-watcher.md` | 942 | Design (18 sections). Status line: "Implemented and merged in PRs #447 and #448; never run live; `enabled` ships as `false`; no schedule is installed". |

Sibling modules (other slices, only referenced): `audit.py` 404, `github.py` 960, `launch.py` 370, `predicates.py` 312, `record.py` 865. Registration: `src/superclaude/cli/main.py:577-579` (`from superclaude.cli.issue_watch.cli import issue_watch_group`; `main.add_command(issue_watch_group, name="issue-watch")`).

### runner.py key symbols
- `STDERR_CAP_BYTES = 500` (l.15); `CommandResult` frozen dataclass (l.19-35: argv, returncode, stdout, stderr, timed_out, spawn_error, duration_s); `Runner` Protocol (l.38); `_as_text` (l.48); `_cap_stderr` (l.57, drops a split multibyte char); `SubprocessRunner.run(argv, timeout, *, cwd=None)` (l.67-130).
- `TypeError` for non-list / empty / non-str argv (l.82-87); `TimeoutExpired` -> `timed_out=True, returncode=None`; `OSError`/`ValueError` -> `spawn_error=<class name>`. Only stderr is capped (stdout is not).

### cli.py key symbols
- Constants l.31-38: `_DEFAULT_CONFIG="~/.config/superclaude/issue-watch.json"`, `_EXIT_UNHEALTHY=1`, `_EXIT_CRASH=1`, `_EXIT_CONFIG=2`, `_EXIT_STORE=6`, `_EXIT_LOCK_HELD=75`.
- `_expand_config` l.41, `_config_option` l.49, `build_deps(config)->Deps` l.62 (SubprocessRunner, FileStore, OrcaLauncher, SystemClock, AuditLog, `shutil.which`, `socket.gethostname()`), `_config_exit` l.77, `_load_config(config_path, *, platform=True)` l.84.
- `issue_watch_group` l.94; verbs: `once_command` l.111-137 (`--dry-run`), `status_command` l.164-182 (`--json`), `check_config_command` l.185-198, `init_state_command` l.201-214, `reset_command` l.282-348 (`ISSUE` arg `IntRange(1, MAX_ISSUE_NUMBER)`, `--forfeit-guarantee`, `--rate-limit`).
- Helpers: `_print_status` l.140, `_refuse_reset` l.217, `_save` l.224, `_reset_locked` l.232, `_write_reset` l.255.

### cycle.py key symbols
- Constants l.34-47: `MAX_CANDIDATES=10`, `MAX_LAUNCHES_PER_CYCLE=1` (l.35; grep over src/ and tests/ finds NO other use, so it is a dead constant; the one-launch limit is really enforced by `self.halt`, l.833-834), `DAY_CAP=6`, `GH_TIMEOUT_S=20.0`, `PROBE_TIMEOUT_S=10.0`, `GIT_TIMEOUT_S=10.0`, `LAUNCH_TIMEOUT_S=120.0`, `DEADLINE_TOTAL_S=240.0`, `GH_FLOOR_S=5.0`, `LAUNCH_CUTOFF_S=120.0`, `SKEW_WARN_S=60`, `HEALTH_AGE_S=900`, `STALE_AGE_S=86400`, `DISCOVERY_WARN=80`.
- Other constants: l.50 `NETWORK_FS_TYPES` (nfs, nfs4, cifs, smb3, sshfs, fuse.sshfs, 9p); l.54 `SCHEMA_VERSION=1`; l.55-56 `DEFAULT_TRIGGER_LABEL="issue-watch:trigger"`, `DEFAULT_APPROVAL_LABEL="issue-watch:approved"`; l.58 `_TOP_KEYS`; l.72 `_PROJECT_ID=PVT_[A-Za-z0-9_-]{1,64}`; l.73 `_APPROVER_LINE`; l.75 `_APPROVERS_MAX_BYTES=1 MiB`; l.462 `_PRECEDENCE=(2,6,7,5,3,4)`; l.463 `_LOCK_HELD_EXIT=75`; l.487 `_LOGIN`; l.488 `_RATE_CLAMP` (= `github.RATE_LIMIT_MAX_WAIT_S`, 3600 s per github.py:376); l.1227 `_SLO_WINDOW=7 days`; l.1228 `_SLO_EXCLUDED_REASONS={disabled, not_enabled}`.
- Public: `ConfigError` l.81; `Config` l.97; `fs_type_of` l.146; `load_config` l.195; `check_platform` l.286; `validate_approvers` l.298; `approvers_summary` l.364; `validate_setup` l.371; `Clock`/`SystemClock` l.380/392; `Deadline` l.402 (`elapsed`, `remaining`, `timeout_for`, `launch_allowed`); `Deps` l.435; `CycleResult` l.449; `resolve_exit` l.466; `exit_for` l.480; `run_cycle(deps, dry_run)` l.1214; `status_report(store, audit, now, *, which=shutil.which)` l.1270; `SloNumbers` l.1339; `slo_numbers(lines, doc, now)` l.1359.
- Internal: `_Skip` l.491, `_Transient` l.499, `_Stop` l.503, `_Cand` l.517, `_LastResult` l.527, `_Cycle` l.541; `_read_store_doc` l.1231, `_is_stale` l.1251, `_retry_orca` l.1262.
- `_Cycle` methods (cycle.py): `run` l.682, `_locked_body` l.704, `_steps` l.711, `_load` l.739, `_login_step` l.752, `_sweep` l.777, `_discover` l.794, `_candidates` l.812, `_val` l.836, `_hit` l.848, `_day_cap_reached` l.867, `_approve` l.878, `_claim` l.896, `_reclaim` l.901, `_examine` l.915, `_rv` l.965, `_revalidate` l.979, `_fail` l.1018, `_launch` l.1026, `_commit` l.1116, `_commit_store` l.1128, `_commit_shadow` l.1146, `_cycle_reason` l.1164, `_conclude` l.1176.

## 2. Behaviour map

### 2.1 Triggers (what starts a cycle)
- Only a person or an external scheduler running `superclaude issue-watch once [--dry-run] [--config PATH]` (`cli.py:111`). The package has NO daemon, listener, loop, sleep, systemd unit or cron file. A grep of the snapshot (outside this package, tests and `.dev/`) finds mentions only in docs, `main.py`, CHANGELOG, `docs/user-guide/cli-groups.md`, `docs/designs/{issue-watcher-setup,issue-pipeline-fu1,orchestrator,orchestrator-mode}.md`, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` and `skills/agent-work-report/*`. No scheduler artefact exists in code.
- Intended cadence: every 5 min (design l.15; setup runbook `docs/designs/issue-watcher-setup.md:288` says cron `0 */5 * * * *`, six fields, seconds first; scheduler "is your choice", Coder cron entry is follow-up FU-2). Overlap is harmless: second run exits 75 `lock_held`.
- Other verbs are operator-run only: `status`, `check-config`, `init-state`, `reset`.

### 2.2 Verb table (cli.py)
| Verb | Platform check | Reads | Writes | Exit codes (code) |
|---|---|---|---|---|
| `once` | yes (`check_platform`, Linux only) | config, approvers file, store, DISABLED, GitHub, git, Orca | `dispatch.json` (not dry-run), `audit.jsonl`, `dry-run.json` (dry-run only), one `orca agent launch` | cycle exit (0,2,3,4,5,6,7,75); 1 on any `Exception` out of `run_cycle`/`build_deps` (cli.py:123-129, reason `cycle_crashed`, prints class name only) |
| `status` | NO (`platform=False`, l.169) | `dispatch.json`, DISABLED mtime | nothing | 0 healthy, 1 unhealthy, 6 StoreError; 2 config |
| `check-config` | yes | config, worktree dir, approvers file | nothing | 0 or 2 |
| `init-state` | yes | config | `state_dir` (0700), `dispatch.json`, `lock` via `record.init_state` | 0; 6 on `StateExists` or `StoreError` |
| `reset ISSUE --forfeit-guarantee` / `reset --rate-limit` | yes (after usage checks) | store under lock | store + ONE audit line (decision line `operator_reset` for an issue, warning line for the rate limit; `reset_refused`/`lock_held` as warning) | 0; 2 usage or `reset_refused` (entry not abandoned/unknown); 6 store/lock; 75 lock held |
- `SystemExit`/`KeyboardInterrupt` are never caught around a cycle (cli.py:123 comment, `except Exception`).
- `once` prints `cycle: <reason>`, `exit: <code>`; in dry-run also `probe:` and `would_launch:`.

### 2.3 State stores and what touches them
| Store | Location | Reader | Writer |
|---|---|---|---|
| Config JSON | `--config`, default `~/.config/superclaude/issue-watch.json` | all verbs (`load_config` l.195) | nobody (operator) |
| Approvers file | `config.approvers_file` (abs path; regular, not symlink, euid-owned, not group/other-writable, <=1 MiB, one decimal id per line, `#` comments) | `validate_approvers` l.298 on `once`, `check-config` | nobody |
| Store `dispatch.json`, `lock`, `DISABLED`, `audit.jsonl` (+rotations), `dry-run.json` | `config.state_dir`, default `$XDG_STATE_HOME or ~/.local/state` + `/superclaude/issue-watch` (cycle.py:187) | `FileStore` in `record.py` (other slice) | `once`, `reset`, `init-state` |
| Dry-run shadow | `dry-run.json` (record.py:805) | `record.load_dry_run` (cycle.py:727) | `record.save_dry_run` (cycle.py:1159), only in `_commit_shadow` when something was examined/would launch/shadow reset |
- Network-FS `state_dir` is rejected (config_invalid) via `/proc/self/mountinfo` (cycle.py:270-272; unreadable mountinfo skips the check).
- Labels in play (read-only): trigger `issue-watch:trigger`, approval `issue-watch:approved` (overridable under config `labels`, must differ).

### 2.4 Cycle flow (cycle.py `_Cycle.run` l.682 -> `_steps` l.711)
1. `enabled` gate: `not config.enabled and not dry_run` -> `_Stop("not_enabled")` (l.685), exit 0, before `validate_setup`, before the lock. Dry-run IGNORES `enabled`.
2. `validate_setup` (worktree dir + approvers) l.688; failure reasons `worktree_invalid`/`approvers_invalid` (exit 2), no lock taken.
3. `store.lock()` non-blocking (l.695); `LockHeld` -> `lock_held` (75); `LockError` -> its reason (6).
4. Kill switch: `store.disabled()` (DISABLED file) -> `_Stop("disabled")`, exit 0 (l.712). Re-checked right before launch -> `disabled_mid_cycle` (l.1063).
5. `_load`: `store.load()`; real cycle saves a migrated store (l.746); `now < next_permitted_at` -> `rate_limited` (exit 5).
6. `_login_step`: `gh api user` (github.user). Login regex; `owner_account_id` mismatch -> `account_id_mismatch` (2); clock skew recorded on cycle line, warning line only if `> SKEW_WARN_S` (60 s).
7. Origin check `launch.check_origin` (git `remote get-url origin` in `config.worktree`) -> `origin_mismatch` (2); no time left -> `gh_timeout` (3) (l.716-722).
8. `_sweep` (record.sweep: pending -> abandoned, launched past lease -> abandoned; decision lines).
9. `_discover` (`github.discover` with trigger label and own login); `>= DISCOVERY_WARN` (80) warning line; truncated/duplicate = exit 4.
10. Order `predicates.eligibility_order(issues, considered)[:MAX_CANDIDATES]`; dry-run uses the shadow `considered` map.
11. Per candidate `_examine` (l.915), in this order: entry state (`claimed/pending` -> `already_dispatched`; `launched/unknown/abandoned+pending_at` -> marker check, T-10 claim or `already_dispatched`; tombstone -> `_reclaim`; failed in backoff -> `_reclaim`/`in_backoff`) -> day cap (`DAY_CAP` 6 in rolling 24 h incl. dry-run shadow launches) -> `is_intended_owner` -> GitHub reads marker comments, events -> `approval_of` -> marker hit means `claimed` -> edits (`unchanged_since`) -> project items (`project_check` vs `config.project_id`) -> `_launch`.
12. `_launch` (l.1026): dry-run records `would_launch`, shadow launch, no probe/Orca. Real: probe `find_orca` -> `build_claim_prompt` -> `_revalidate` (re-read issue state open + both labels + assignee, re-read events same approval event id, re-read project items; 3 reserved calls) -> day cap again -> DISABLED again -> 120 s cutoff -> origin re-check -> `mark_pending` + `_save()` (durable BEFORE launch) -> cutoff check (undo to prior doc) -> `launcher.launch(orca, worktree, prompt, 120 s)` -> `launched` / `unknown` (exit 7) / `spawn_error` (abandoned, exit 7).
13. Halt: after any launch-step outcome (`c.launching`) the loop stops (`self.halt`, l.833); later candidates get no read/stamp/decision line.
14. `_commit`: stamps `considered` for examined (not `budget_exhausted`), prunes, sets `last_completed_cycle_at` only if no stop reason and exit 0 (l.1138), saves once. `_conclude` appends decision lines then ONE cycle line; `rotate_if_needed` only when locked; OSError -> `audit.stderr_fallback`.
- Exit precedence `resolve_exit` l.466: first present of 2,6,7,5,3,4; 75 only if sole non-zero; else 0. Cycle reason on exit 0: `cycle_complete` unless a stop reason exists.
- Deadline: total 240 s; a `gh`/git/probe call is not started with `< 5 s` left; launch not started once `elapsed > 120 s`.

### 2.5 Gates and approval points
- Config gate `enabled` (default `false`, `load_config` l.228); dry-run bypasses it.
- DISABLED file in `state_dir` (operator `touch`), checked twice per cycle.
- Approval gate: label events replayed by `predicates.approval_of` with trigger label, approval label, approver id allow-list from the approvers file, and `store_created_at` floor; re-verified in `_revalidate` (voided or newer approval event fails).
- Intended-owner gate (assignee set exactly {own login}), `owner_account_id` optional pin, Project gate (config `project_id`), `unchanged_since` (no edits after approval), day cap 6/24 h, 1 launch per cycle, max 10 candidates, call budget 35 (3 reserved, github.py:46-49).
- `reset ... --forfeit-guarantee` is the only way to let an issue launch twice.

### 2.6 What it writes to GitHub
- Nothing. Every `gh` call is a read (`gh api user`, `gh issue list`, REST GET, GraphQL query constants); design NG-2 and `test_security_invariants.py` pin no `mutation` and every REST argv carrying `--method GET`. The only outward side effect is the Orca launch.
- Outward launch argv (launch.py:95-116, 12 elements): `<orca> agent launch --agent claude --worktree path:<abs worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json`; the prompt is built only by `launch.build_claim_prompt` (int 1..999999999). All claim assignment, comments and later work are the launched session's job (not this slice).
- Repo is hard-wired: `github.REPO = "IronbellyOrg/IronClaude"` (github.py:37), `launch.ORIGIN_REPO = "ironbellyorg/ironclaude"` (launch.py:50).

## 3. Doc-vs-code checks (docs/designs/issue-watcher.md)

| # | Doc claim (section/line) | Tag | Evidence |
|---|---|---|---|
| 1 | Defaults table sec.14 (l.816-834): max candidates 10, day cap 6, timeouts gh 20/probe 10/git 10/Orca 120/deadline 240, health 900 s, stale 24 h, stderr cap 500, clamp 3600, discovery warn 80 | [CODE-VERIFIED] | cycle.py:34-47; runner.py:15; github.py:376 |
| 2 | Same table: call cap 35 with 3 reserved; lease 60 min; backoff 10 min; max_attempts 3; audit rotation 5 MiB, 4 files | [CODE-VERIFIED] | github.py:46-49; record.py:434-440; audit.py:106-107 |
| 3 | Same table: "skew tolerance 300 s" | [CODE-CONTRADICTED] | cycle.py:44 `SKEW_WARN_S = 60`; the doc's own sec.7.5 (l.510) and audit table (l.722) say 60 s, so the doc contradicts itself |
| 4 | Same table: `max_launches_per_cycle` 1 as a value | [CODE-VERIFIED] behaviour, dead constant | cycle.py:35 defined, never read; enforced by `self.halt` (l.833) |
| 5 | Exit codes sec.4.3 (0,1,2,3,4,5,6,7,75) and reason-to-exit mapping | [CODE-VERIFIED] | audit.py:24-96 `REASON_TABLE`; cli.py:31-38, 123-129; cycle.py:462-477 |
| 6 | Precedence 2, 6, 7, 5, 3, 4; 75 only when sole condition | [CODE-VERIFIED] | cycle.py:462-477 |
| 7 | Config fields, unknown-key rejection, label rules, `PVT_` project id, owner id range, abs paths, network-FS deny-list (sec.4.2) | [CODE-VERIFIED] | cycle.py:58-75, 195-283 |
| 8 | Approvers file rules (lstat, regular, euid owner, not group/other-writable, id regex, non-empty) | [CODE-VERIFIED] | cycle.py:298-361 (also O_NOFOLLOW, same-inode recheck, 1 MiB cap, not in doc table) |
| 9 | `enabled: false` -> exit 0 `not_enabled` before any external call; dry-run ignores it | [CODE-VERIFIED] | cycle.py:685-686, 228 |
| 10 | Step order 6.2 (platform/config, lock, DISABLED, load, user, origin, sweep, discover, order, per-candidate, launch steps, commit) | [CODE-VERIFIED] | cycle.py:682-737, 915-1112, 1116-1211 |
| 11 | Launch step order: probe, prompt, re-read (3 reserved), day cap, DISABLED, origin re-check, pending save, launch | [CODE-VERIFIED] | cycle.py:1026-1112 |
| 12 | Health stamp only on exit-0, non-dry-run, no stop reason | [CODE-VERIFIED] | cycle.py:1138-1140; dry-run writes shadow only (l.1146) |
| 13 | `status` takes no lock, writes nothing, exit 0/1/2/6, unhealthy when age > 900 s or no cycle | [CODE-VERIFIED] | cli.py:164-182; cycle.py:1231-1335 (plain `open`, `healthy = age <= 900`) |
| 14 | Import rules sec.5.3 for `runner`, `cycle`, `cli`; `cycle` never imports subprocess | [CODE-VERIFIED] | runner.py (no package imports); cycle.py:27-31; cli.py:26-29 |
| 15 | Prompt is `/sc:issue --claim <N> --pipeline none`, 12-element launch argv | [CODE-VERIFIED] | launch.py:84-116 |
| 16 | Group registered in `main.py` "after `reflect`, line 561" (sec.5.1 diagram) | [CODE-CONTRADICTED] on line number only | main.py:577-579 (registration is still directly after `reflect`, l.575) |
| 17 | `SubprocessRunner.run(argv, timeout)` (sec.5.2) | [CODE-CONTRADICTED] minor | runner.py:70-72 has an extra `cwd` keyword (who passes it was not traced) |
| 18 | `audit.stderr_fallback(line)` (sec.5.2) | [CODE-CONTRADICTED] minor (call sites only) | cli.py:79,127 and cycle.py:1202 call `stderr_fallback(reason, code, ts=, host=)`; def in audit.py not read |
| 19 | `find_orca (cached)` once per cycle (sec.6.1) | [UNVERIFIED] | cycle.py calls `launch.find_orca` once per launch attempt (l.1048) and halts after; caching is in launch.py (other slice) |
| 20 | Header: "Implemented and merged in PRs #447 and #448; never run live; no schedule installed" | [UNVERIFIED] for PRs and live state | Snapshot has no git history or runtime state. `enabled` default false [CODE-VERIFIED]; no scheduler artefact in the snapshot [CODE-VERIFIED by grep] |
| 21 | Sec.2.1 D2 superseded 2026-11-17: coordinator starts the worker | [UNVERIFIED] here | The poller side (`--pipeline none`, no worktree/assign/comment) is CODE-VERIFIED; coordinator behaviour is outside this slice |

## 4. Tests that pin this slice (tests/issue_watch/, all mocked; none calls real gh, git or Orca except test_cli_e2e which uses PATH stubs)

Counts are `def test_` counts (parametrisation not expanded). Only docstrings and test names were read.

| File | Lines | Tests | What it covers |
|---|---|---|---|
| `conftest.py` | 1155 | 0 | Shared fakes: `FakeClock` l.51, `FakeRunner` l.74, `CrashingStore` l.129, `FailingStore` l.188, `FakeLauncher` l.251, `tmp_state` fixture l.244, `make_deps` l.393, `GhWorld` l.528 (scripted GitHub replies), `gh_world` fixture l.923, `stub_path` fixture l.1109 (PATH stubs for gh/orca/orca-ide/git). |
| `test_cycle.py` | 4982 | 237 | Everything in `cycle.py`. Part A: `load_config`, `fs_type_of`/network FS, `check_platform`, `validate_approvers`, `validate_setup`, `resolve_exit`/`exit_for`, `Deadline`. Part B (l.1212): idle cycle, own login, voided shared inputs, discovery warnings, rate limits (FR-028), deadline in process (AC-19), one cycle line per exit, REASON_TABLE exit parity. Part C (l.2359): per-issue skip reasons, entry-state skips, claimed paths, tombstones, launch step order, re-read (FR-011), DISABLED/origin between discovery and pending write, S1 halt, `considered` map, dry-run, backoff/attempts_exhausted. Part D (l.4219): 50-cycle at-most-once, 24 h property, second-`once` no-op, 35-call budget; then "Gate C fix tests" l.4493. Status report / `status_report` is NOT referenced here (0 hits). |
| `test_runner.py` | 226 | 16 | `SubprocessRunner`: str/empty/non-str argv raise TypeError, no shell, cwd passthrough, 500-byte stderr cap incl. multibyte, timeout, spawn-error class name, NUL bytes, non-UTF-8 output, real timeout speed (NFR-004, NFR-008). |
| `test_cli.py` | 1672 | 60 | The Click group (exactly five commands), `--config` and `~` rules (DF-13), `check-config`, `once` (exit mapping, dry-run output, crash -> exit 1, SystemExit/KeyboardInterrupt pass through, build_deps failure), `build_deps`, `status` (JSON fields, text, retry argv by Orca name, exit 0/1/6/2, no mtime change), `init-state` (DF-53), `reset` (usage errors, forfeit, rate limit, lock held 75, fallback-only cases). In-process via `CliRunner`; `SubprocessRunner.run` is made to raise. |
| `test_cli_e2e.py` | 443 | 4 | Real `python -m superclaude.cli.main issue-watch` processes with PATH stubs: stub guard, idle cycle = exactly 2 gh calls (FR-001), eligible issue launches once through `orca-ide` (FR-010/013), second `once` launches nothing (NFR-010). |
| `test_concurrency.py` | 275 | 6 | Two real spawned processes on one store -> one launch and exit 75 for the other (FR-017, AC-11); lock as symlink / directory / missing -> exit 6 with no call; lock replaced after flock -> 75. |
| `test_crash_injection.py` | 373 | 6 | Crash (`SystemExit`) at the five write/spawn points C1-C5 of design 7.6, then five more cycles: launcher called at most once, `launches` stays 1 (NFR-005, AC-17). |
| `test_module_boundaries.py` | 413 | 13 | AST import-graph walker enforcing design 5.3 per module; exactly the designed modules; record defers `atomic`/`fcntl` imports; no module named `select`; exactly four Protocol classes; walker self-tests. |
| `test_no_shell.py` | 266 | 9 | AST scan: no `shell=` other than False, no `os.system`/`os.popen`, `subprocess` imported only by `runner.py`; scanner self-tests. |
| `test_no_text.py` | 971 | 22 | Canary `PWNED-TITLE` in labels, logins, non-JSON stdout, long stderr, extra title/body: must never reach state files, argv, prompt, launch args or command output; audit key set closed; no argv asks for title/body/comment text. |
| `test_security_invariants.py` | 1013 | 16 | Prompt regex property (NFR-001, AC-7), hostile labels/logins/assignees/config, allowed-argv forms for every cycle call, `--method GET` on REST, no GraphQL mutation, literal repo in GraphQL, 12-element launch argv, `dispatch.json` entry keys with the `--pipeline none` prompt. |

Not in this slice but in the same folder (pins sibling modules or cross-checks): `test_audit.py`, `test_github.py`, `test_launch.py`, `test_predicates.py`, `test_record.py`, `test_find_orca_parity.py`, `test_origin_parity.py`, `test_marker_contract.py`, and `test_slo_helper.py` (421 lines; its docstring says it tests `cycle.slo_numbers`, the only test file that references `slo_numbers`, so it also pins part 3 of `cycle.py`).

## 5. Proposed deep-research assignments for this slice (2 topics)

1. **Per-cycle decision engine and exit/reason model** (output `research/r1-cycle-decision-engine.md`).
   Files: `src/superclaude/cli/issue_watch/cycle.py` l.485-1222 (`_Cycle`), `audit.py:24-104` (`REASON_TABLE`), `predicates.py` (`approval_of`, `eligibility_order`, `is_intended_owner`, `unchanged_since`, `project_check`), `github.py` (`CallBudget` l.437, `Read.kind` classification), design sec.6-8, tests `test_cycle.py` Parts B-C.
   Deliver: a step-by-step state/decision table (every skip and stop reason, which gate raises it, entry-state transitions, exit code, decision vs cycle line), dry-run vs real differences, and the 35-call budget arithmetic.
2. **Operator surface: config, verbs, state directory, kill switch, status and SLO** (output `research/r2-operator-surface-cli-config-status.md`).
   Files: `cli.py`, `cycle.py` l.34-483 (config/approvers/Deadline) and l.1225-1406 (`status_report`, `slo_numbers`), `runner.py`, `record.py` (`FileStore`, `init_state`, `reset_entry`, `DISABLED`, lock), `docs/designs/issue-watcher.md` sec.4, 7, 10, `docs/designs/issue-watcher-setup.md` (runbook, section 8 "Before cron", 8.7 cron line), tests `test_cli.py`, `test_cli_e2e.py`, `test_slo_helper.py`.
   Deliver: verb-by-verb reference with exit codes, config schema with validation rules, on-disk layout and modes, the retry-argv output of `status`, runbook-vs-code reconciliation, and what a real deployment must provide (scheduler, persisted `state_dir`, approvers file).

## 6. Gaps and open questions
- No runtime evidence: the snapshot has no live state; "never run live" and the PR numbers (#447, #448) are [UNVERIFIED] (item 20 in sec.3). Whether anything now schedules `once` (Coder cron FU-2, any dispatcher) cannot be seen in this snapshot; the only scheduling text is the setup runbook (`issue-watcher-setup.md:198-204, 286-290`). Later owner decisions about a cron plus dispatcher live outside this snapshot and were not checked.
- Doc sec.14 skew value (300 s) disagrees with code and with the doc's own sec.7.5 (60 s). `MAX_LAUNCHES_PER_CYCLE` is dead.
- `Deps.audit` and `status_report`'s `audit` parameter shadow the `audit` module name inside `cycle.py` (cycle.py:442, 1272); `status_report` accepts `audit` but never reads it (docstring l.1280-1281). Harmless; note for the reference text.
- `status` skips the platform check while `once`/`check-config`/`init-state`/`reset` run it (cli.py:169 vs 84); the doc says `status` can return 2 for config, not for platform.
- `reset` usage errors (`_refuse_reset`, cli.py:217) write only a stderr fallback line, never an `audit.jsonl` line; other `reset` exits write one audit line (design sec.7.1 says "every exit of once and reset" appends to the audit log, so this is a small doc imprecision, not traced further).
- `launch.find_orca` caching, `record` lock/atomic-write protocol, `github.py` reply classification, `predicates` approval replay, and `audit` line schema were deliberately not read; they belong to the sibling slices.
- test bodies were not read (names and docstrings only); test counts do not expand parametrisation. `tests/issue_watch/test_cli.py` status tests exercise `status_report` only through the CLI.
- Design sec.15 lists many reply shapes as UNVERIFIED (`_assumed_shape` fixtures); resolution depends on the owner live test, which is not in the snapshot (`docs/designs/issue-watcher-live-test.md` does NOT exist in the snapshot's `docs/designs/`; the nearest files are `issue-pipeline-fu1.md`, `issue-pipeline-guard-g2.md`, `issue-pipeline-guard-g2-no-to.md`, `issue-watcher-setup.md`).

