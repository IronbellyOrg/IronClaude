# QA Report: Gate B, design-correctness lens (Phases 4 and 5)

**Topic:** issue-watch store (`record.py`) and launcher (`launch.py`) against design, spec and decisions
**Date:** 2026-11-07
**Phase:** design-correctness lens, rf-qa-qualitative (code-vs-binding-source review; the Axis column is omitted because this is not the task-qualitative phase)
**Fix cycle:** N/A (first review; `fix_authorization: false`, no file other than this report was written)

---

## Overall Verdict: FAIL

One blocking finding (B-1). Nine minor notes (M-1 to M-9). I did not find 15 blocking errors and I am not padding the list to reach that number: the store and launcher match the design on every other point I checked, and 686 tests pass (see Evidence log).

## Scope and sources read

Change set: `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/gate-b-change-set.md`. Code under review: `src/superclaude/cli/issue_watch/record.py` (858 lines, read in full) and `launch.py` (348 lines, read in full). Binding sources, all read: `docs/designs/issue-watcher.md` lines 215-290, 388-537, 602-648, 672-695 (plus 741 and 843); spec lines 150-180, 255-307, 326-361 of `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md`; decision rows DF-01, 03, 04, 11, 15, 17, 21, 30, 36, 42, 43, 44, 46, 54 (and 18, 19, 22, 35, 41, 57 for context) of `research/06-gap-fill-decisions.md`. Parity sources: `install_user_setup.py:198-221`, `origin_repo.py:65-99`, `swarm/atomic.py` (whole file).

DEVIATION rows applied as overrides and NOT reported as errors: DF-01 (Runner `cwd`), DF-15 (lock released in `finally`), DF-17 (migrated store never saved on load; dry-run), DF-42 (`record` checks `last_reason` as str or null only), DF-43 (failed-to-failed), DF-44 (`sweep` and `day_cap_count` take a `StoreDoc`), and the task's own OQ-41a (probe cache lives in the cycle, not in `OrcaLauncher`, departing from design line 614).

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Store schema: 7 store keys, 17 entry keys | PASS | `_STORE_KEYS` (record.py:120-130) equals design 7.2 (D 406-414); `_ENTRY_KEYS = Entry.__dataclass_fields__` gives the 17 fields of D 419-437 in the same order. |
| 2 | Key sets and validation (D 439) | PASS | `validate`/`_entry` (record.py:168-242) check exact key sets at both levels, int-not-bool types, `issue == key`, `launches in {0,1}`, `launches == 1` implies `consumed_at` and `pending_at`, `failed` implies `launches == 0`, strict `YYYY-MM-DDTHH:MM:SSZ` via `predicates.parse_utc`, decimal-string keys `[1-9][0-9]*` within 1..999999999. Probe: bool, `1.0`, `"007"`-style keys and a non-Z time are all rejected (also pinned by `test_ac22_*`). |
| 3 | Migration seam (D 441, DF-17) | PASS | `MIGRATIONS = {}`; `migrate(doc, migrations=...)` rejects non-int, higher, unregistered and wrong-result versions (record.py:249-276); `FileStore.load` migrates in memory and never saves (record.py:345-366). |
| 4 | Atomic save, dir fsync, 0600/0700 (D 509, DF-30) | PASS | `save` = `json.dumps(sort_keys, indent=2, ensure_ascii)` + `b"\n"`, then `write_prepared_bytes`, `os.chmod(0o600)`, `_fsync_dir` (record.py:368-376; `_fsync_dir` at 308-313 uses `O_RDONLY|O_DIRECTORY`, close in `finally`). Probe: `init_state` gives dir 0o700, `dispatch.json` and `lock` 0o600. |
| 5 | Lock protocol, release in `finally` (D 511-521, FR-017, DF-15) | FAIL | Steps 2 to 5 and the `finally` release are correct (probe: second lock gives `LockHeld`, relock after normal exit and after `SystemExit` works, missing gives `lock_missing`, symlink gives `lock_invalid`). Step 1 leaks an untyped `PermissionError` for a lock file the process cannot open: see B-1. |
| 6 | Transitions T-1 to T-13 | PASS | One function per row: `fail` (T-1, T-3), `backoff_elapsed` (T-2), `mark_pending` (T-4), `mark_launched` (T-5), `mark_unknown` (T-6), `mark_spawn_error` (T-7), `sweep` (T-8, T-9), `mark_claimed` (T-10 to T-12), `reset_entry` (T-13); all return a new `StoreDoc`; every other (state, trigger) pair raises `TransitionError` (probe: `fail` from `abandoned`, `mark_claimed` from `pending`). |
| 7 | Failed-to-failed retry (DF-43) | PASS | Probe: attempts 1, 2 stay `failed`; the third `fail` gives `abandoned` with `last_reason` `attempts_exhausted`, attempts 3. |
| 8 | Half-open windows (D 496-505) | PASS | Lease: `now >= lease_expires_at` (record.py:634). Backoff: `now >= updated_at + BACKOFF` (537). Day cap: `now - 24h < t <= now` (683). Prune: `t > cutoff` kept (689). Probe: lease expired at exactly +60 min and not at +59:59; a `consumed_at` exactly 24 h old gives count 0, one second younger gives 1. |
| 9 | Day-cap count (D 500, FR-024) | PASS | `day_cap_count` counts every entry's `consumed_at` (any state) plus `consumed_log`. Probe: after `reset_entry` the count stays 1. |
| 10 | Sweep (T-8, T-9, DF-44) | PASS | `sweep(doc, now)` touches only `pending` (always) and `launched` (lease end or no lease); `unknown` is never swept; returns the changed entries in issue order; input document unchanged. |
| 11 | Reset functions (T-13, DF-03, DF-04) | PASS | `reset_entry` removes only `abandoned`/`unknown`, appends a non-null `consumed_at` to `consumed_log`, then prunes; a missing entry or other state raises `TransitionError` (CLI maps it later). `reset_rate_limit` clears `next_permitted_at` only. |
| 12 | `init-state` (D 396-398, D 117) | PASS | `init_state` (record.py:746-795): `makedirs(mode=0o700)` then `chmod`, lock created `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW` 0600, empty store stamped `created_at=now`; existing store or lock gives `StateExists` with nothing changed; a lock it created is removed if the store cannot be saved; OSError gives `state_dir_unwritable`. |
| 13 | 12-element launch argv (D 618-623, FR-013) | PASS | `launch_argv` returns exactly `[orca, agent, launch, --agent, ORCA_AGENT, --worktree, "path:"+worktree, --surface, terminal, --prompt, prompt, --json]` (launch.py:94-115); `ORCA_AGENT = "claude"` (DF-11); the prompt is gated by `PROMPT_PATTERN.fullmatch`. `build_claim_prompt` accepts only `type(n) is int` in 1..999999999 (bool, str, float, 0, -1, 10**9 raise). |
| 14 | Outcome mapping (D 627-634, OQ-40, OQ-47) | PASS | `outcome_of` (launch.py:304-327): runner `spawn_error` gives `spawn_error`; `timed_out` gives `unknown`/`timeout`; the text `agent_session_operation_unknown` gives `unknown`; non-zero gives `exit_nonzero`; non-JSON gives `non_json`; no id gives `no_operation_id`; an id failing `^[A-Za-z0-9._:-]{1,128}$` gives `unknown` with `operation_id` None (D 689); exit 0 plus a valid id gives `launched`. Probe confirmed each row. |
| 15 | Orca probe acceptance (D 606-616, DF-36, DF-54) | PASS | `_lists_orca_cli` requires exit 0, no timeout/spawn error, a JSON object, `topics` a list of dicts, and one dict named `orca-cli`; every other shape returns False without raising (DF-36). `find_orca(runner, *, which=shutil.which, timeout=10.0)` tries `_ORCA_CLIS` in order, imported not copied; `timeout=None` starts nothing. |
| 16 | Origin check (D 222, FR-025, DF-01) | PASS | `check_origin` runs exactly `["git","-C",worktree,"remote","get-url","origin"]` with no `cwd`; `parse_origin` is byte-for-byte the rules of `origin_repo.parse_origin_url` (compared line by line, launch.py:184-208 against origin_repo.py:65-69, 86-99); comparison lower-cased against `ironbellyorg/ironclaude`; timeout, non-zero exit and unparseable URL all fail closed. `OrcaLauncher.launch` is the only caller that passes `cwd` (DF-01). |

## Summary
- Checks passed: 15 / 16
- Checks failed: 1
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)
- Blocking findings: 1 (B-1). Minor notes: 9 (M-1 to M-9).

## Findings (blocking)

| id | severity | file | evidence | expected versus actual |
|----|----------|------|----------|------------------------|
| B-1 | blocking (wrong behaviour against FR-017 and the `Store` contract) | `src/superclaude/cli/issue_watch/record.py:389-399` (`FileStore.lock`, step 1) | The `os.open(path, O_RDWR\|O_NOFOLLOW\|O_CLOEXEC)` handler maps only `FileNotFoundError` (to `lock_missing`), `IsADirectoryError` and `ELOOP` (to `lock_invalid`); every other `OSError` is re-raised untyped (line 399). Probe (uid 1000, scratch dir, removed afterwards): `chmod 0` on the lock file, then `with store.lock()` gave `PermissionError`, not `LockError`. The only foreign-owner test, `tests/issue_watch/test_record.py:681-688`, monkeypatches `os.geteuid`, so it passes only because the open succeeds; the real case (a lock file owned by another user with mode 0600, which cannot be opened) is untested. | Expected: spec FR-017 (S 172-173, panel PF-045) "a lock path that is not a regular file owned by the effective UID exits 6", design 5.4 (D 272) `lock()` "raises LockHeld / LockError(reason)", and design 7.6 step 2 (`st_uid == geteuid()` else 6 `lock_invalid`). Actual: a lock the process cannot open (foreign owner at 0600, mode 000, `ENOTDIR`, `ENAMETOOLONG`) escapes as a raw `OSError` subclass. A cycle that catches only `LockError`/`LockHeld`/`StoreError` would die with a traceback (exit 1) and write no audit line. Fix: map `PermissionError` and every other `OSError` raised by that `os.open` to `LockError("lock_invalid")` (keep `lock_missing` for `FileNotFoundError`), and add a test that uses `os.chmod(lock, 0)` instead of faking `geteuid`. Caveat: `cycle.py` does not exist yet, so the crash is not reachable end to end today; the defect is in the store's contract, which Phase 6 will build on. |

## Minor notes (never fail the review; not rechecked later)

| id | file | note |
|----|------|------|
| M-1 | `record.py:582-610`, `:180-181` | `mark_launched`, `mark_unknown` and `validate` accept any `str` as `operation_id` (probe stored and reloaded `"x y;z"` and `"bad id; rm -rf"`). D 687-689 says the id reaches the store only after `^[A-Za-z0-9._:-]{1,128}$` because `status` prints it in a shell command. Today `LaunchOutcome.__post_init__` enforces it upstream and `launch.retry_argv` re-checks it, so no injection path exists; a 3-line regex in `record` would make the store defend itself too. |
| M-2 | `launch.py:211-229`, task item 5.1 | `check_origin(timeout=None)` and a git timeout or spawn failure all return `origin_mismatch` (exit 2 at cycle start). D 646 says the git origin call is "as gh": not started when `remaining() < 5`, giving `budget_exhausted` per issue. The task item chose this reading and it is not in the Open Questions list. It fails closed; the cycle must test `deadline.timeout_for(10)` for `None` before calling, as OQ-39 text already does for the probe. |
| M-3 | `launch.py:41-44`, `:270-281` | `_first_hit` accepts the error-path id (`error.operation_id`) on an exit-0 reply, so `{"error": {"operation_id": ...}}` with exit 0 maps to `launched`; `outcome.kind` is never consulted. The reply shape is UNVERIFIED (D 636) and pinned only by assumed fixtures; recheck when FU-1 records a real reply. |
| M-4 | `record.py:423-433`, `:741-743` | A dangling `DISABLED` symlink makes `disabled()` and `disabled_present()` True while `disabled_since()` returns None (probe). `status` must print "disabled" without a time in that case. A `PermissionError` from the `stat` is also untyped. |
| M-5 | `record.py:368-376`, `:844-858` | `save` and `save_dry_run` raise raw `OSError` (probe: `FileNotFoundError` for a missing `state_dir`). The cycle must map these to `state_dir_unwritable` (S 336); no store-level typed error exists for a failed save. |
| M-6 | `record.py:316-329`, `tests/issue_watch/conftest.py:148-151` | `FileStore.migrated` (an OQ-41 name) is not part of the `Store` Protocol (D 268-274). `CrashingStore` proxies it, but a cycle typed on `Store` cannot read it without widening the Protocol. Unreachable in v1 because `MIGRATIONS` ships empty. |
| M-7 | `record.py:372`, `predicates.format_utc` | A `now` with sub-second precision is truncated on save (probe: `12:00:00.7` reloads as `12:00:00`), while in-cycle comparisons use the unrounded value; a lease or backoff can end up to 1 s early after a reload. Have `SystemClock.now()` return whole seconds in Phase 6. |
| M-8 | `record.py:566-567` | `mark_pending` writes `last_reason=None` (clearing a previous `failed` reason), while D 437 lists `last_reason` as set on every write. The closed table (S 330-358) has no reason that names a pending write, so None is the only value available; the code comment says so. |
| M-9 | `launch.py:143-157` | D 612 "Accept" (some element is a dict named `orca-cli`) and D 613 "Reject ... a non-dict element" disagree for a mixed list; `find_orca` follows DF-36 and rejects the whole reply. The original `_find_orca` would return the path when the `orca-cli` dict precedes the non-dict element (its `any` short-circuits), so DF-36's "the original raises" holds only when no match comes first. The parity test excludes mixed lists, so nothing is affected. |

## Actions Taken

None. `fix_authorization: false`. Only this report file was written. Scratch probes ran in `/tmp/rfqa-g5-probe` (removed) and in `tempfile.mkdtemp()`; pytest ran with `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`; `git status --short` before and after showed the same entries.

## Evidence log (commands that back the table)

- `uv run --offline --no-sync pytest -p no:cacheprovider -q tests/issue_watch/test_record.py test_launch.py test_find_orca_parity.py test_origin_parity.py test_marker_contract.py` gave `686 passed in 1.17s`, exit 0.
- Probe 1 (temp dir): modes `0o700/0o600/0o600`; second lock `LockHeld`; relock after `SystemExit` works; `lock_missing`; symlink `lock_invalid`; `fail` x3 gives `failed`, `failed`, `abandoned/attempts_exhausted`; `fail` from `abandoned` raises; `mark_claimed` from `pending` raises; day cap at exactly 24 h is 0 and at 24 h minus 1 s is 1; lease expires at +60:00, not +59:59; `reset_entry` keeps the day-cap count at 1; `init_state` twice gives `StateExists`; 7 `outcome_of` cases map as listed in item 14.
- Probe 2 (scratch dir, removed): `chmod 0` lock gives `PermissionError` (B-1); `save` to a missing dir gives `FileNotFoundError` (M-5); dangling `DISABLED` gives `disabled() True`, `disabled_since() None` (M-4); sub-second truncation (M-7).

## Self-Audit

No `## Inherited Structural Verdict` section was in the spawn prompt, so this ran in standalone mode (structural checks done independently; nothing skipped on rf-qa's word).

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. The change-set file's gate table (G-1 1094 and 1372 passed, ruff, `make lint`) was not relied on for any verdict; I re-ran the five relevant test files myself (686 passed) and read every cited line range directly.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Lock behaviour under an unopenable lock file: verified by a scratch probe (`chmod 0` gives untyped `PermissionError`) and by reading `test_record.py:681-688` (the existing test fakes `geteuid`); this produced B-1, which the passing suite does not catch.
- Half-open boundaries: verified by running exact-boundary cases (24 h, 60 min) against `day_cap_count` and `sweep`, not only reading the comparison operators.
- Outcome mapping: ran 7 `CommandResult` shapes through `outcome_of` and compared each row with D 629-634 and OQ-40/OQ-47.
- Origin parser parity: compared `launch.parse_origin` with `origin_repo.parse_origin_url` line by line (identical patterns, `.git` strip, dot-name rejection).
- Operation-id boundary (D 687-689): probed the store with hostile ids (M-1).

Factual claims independently verified: about 70 (17 entry keys, 7 store keys, 13 transitions, 4 windows, 12 argv elements, 5 outcome rows, probe acceptance branches, DF-01, 03, 04, 11, 15, 17, 30, 36, 42, 43, 44, 54 applications, and file modes). Web research: none performed, so no Tavily or fallback use to record.

If I had reported 0 issues the user should not have believed it: the existing 686 tests pass and still miss B-1, which only a real unopenable lock file exposes.

## Confidence Gate

- **Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (item 5 is verified and FAILS)
- **Tool engagement:** Read: 27 | Grep: 13 | Glob: 0 | Bash: 5 (one blocked by the bare-python hook and rerun with `uv run`). Read + Grep + Glob = 40, above the 16 checklist items.
- Unchecked items: none. Unverifiable items: none. Out of scope here (other lenses or later phases): `cycle.py`, `cli.py`, `github.py`, `predicates.py`, test adequacy, gate-command reproduction, security-invariant tests.

## Recommendations

1. Fix B-1 in `FileStore.lock` (map every non-`FileNotFoundError` `OSError` from the open to `LockError("lock_invalid")`) and add a `chmod 0` test; then one re-review of that item only.
2. Optional, no re-review needed: M-1 (regex in `record`), M-2 (record the origin-deadline reading as an Open Question, or return a distinct value), M-7 (whole-second clock) before Phase 6 builds on these modules.

## QA Complete
