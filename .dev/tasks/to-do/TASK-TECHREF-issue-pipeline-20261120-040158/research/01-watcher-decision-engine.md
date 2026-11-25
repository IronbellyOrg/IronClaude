# Research: Watcher decision engine
**Investigation type:** Code Tracer
**Scope:** issue_watch/cycle.py, predicates.py, audit.py, issue-watcher.md sec 6-8, six test files
**Status:** Complete
**Date:** 2026-11-20
---

All paths are relative to the snapshot root `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6) unless absolute. `P` = `src/superclaude/cli/issue_watch/`. Every line number below was re-read from the live snapshot file in this session. The scope hint files were used only as pointers.

## 1. Cycle constants (`P/cycle.py` lines 34-47) and which are read

| Constant | Value | Line | Read at (production code) | Status |
|---|---|---|---|---|
| `MAX_CANDIDATES` | 10 | 34 | cycle.py:736 (`eligibility_order(...)[:MAX_CANDIDATES]`) | read |
| `MAX_LAUNCHES_PER_CYCLE` | 1 | 35 | NONE. `Grep MAX_LAUNCHES_PER_CYCLE|max_launches_per_cycle` over the whole snapshot excluding `.dev/` and `docs/` finds exactly one hit, the definition at cycle.py:35 (no hit in `src/`, none in `tests/`). | DEAD constant |
| `DAY_CAP` | 6 | 36 | cycle.py:876 (`return used >= DAY_CAP`) | read |
| `GH_TIMEOUT_S` | 20.0 | 37 | cycle.py:578 (`_tf`), 582 (`_tf_shared`) | read |
| `PROBE_TIMEOUT_S` | 10.0 | 38 | cycle.py:1036, 1044 | read |
| `GIT_TIMEOUT_S` | 10.0 | 39 | cycle.py:716, 1071 | read |
| `LAUNCH_TIMEOUT_S` | 120.0 | 40 | cycle.py:1099 (passed to `launcher.launch`) | read |
| `DEADLINE_TOTAL_S` | 240.0 | 41 | cycle.py:405 (`Deadline.__init__` default) | read |
| `GH_FLOOR_S` | 5.0 | 42 | cycle.py:425 (`Deadline.timeout_for`) | read |
| `LAUNCH_CUTOFF_S` | 120.0 | 43 | cycle.py:431 (`Deadline.launch_allowed`) | read |
| `SKEW_WARN_S` | 60 | 44 | cycle.py:774 (`if skew > SKEW_WARN_S`) | read |
| `HEALTH_AGE_S` | 900 | 45 | cycle.py:1327 (status report only, not the cycle) | read (status) |
| `STALE_AGE_S` | 86400 | 46 | cycle.py:1259 (status report only) | read (status) |
| `DISCOVERY_WARN` | 80 | 47 | cycle.py:806 (`if len(issues) >= DISCOVERY_WARN`) | read |

Other module constants read by the cycle: `_PRECEDENCE = (2, 6, 7, 5, 3, 4)` (462), `_LOCK_HELD_EXIT = 75` (463), `_LOGIN = [A-Za-z0-9][A-Za-z0-9-]{0,38}` (487), `_RATE_CLAMP = timedelta(seconds=github.RATE_LIMIT_MAX_WAIT_S)` (488; `RATE_LIMIT_MAX_WAIT_S` = 3600 at github.py:376, owned by agent 02). Defaults that are NOT in cycle.py but drive the cycle: `record.MAX_ATTEMPTS = 3` (record.py:434), `record.BACKOFF = 10 min` (437), `record.LEASE = 60 min` (440), `record.DAY_CAP_WINDOW = 24 h` (443), `github.CALL_CAP = 35`, `github.RESERVED_CALLS = 3`, `github.PAGE_CAP = 5`, `github.PAGE_SIZE = 100`, `github.DISCOVERY_BOUND = 100`, `predicates.SKEW_TOLERANCE_S = 300` (predicates.py:17), `audit.ROTATE_BYTES = 5 MiB` (audit.py:106), `audit._ROTATIONS = 4` (107).

**What enforces the one-launch-per-cycle limit instead.** `_Cand.launching` (cycle.py:524) is set `True` on the first line of `_launch` (cycle.py:1028). After `_examine` returns or raises `_Skip`, `_candidates` writes the decision line and then runs `if c.launching: self.halt = True` (cycle.py:833-834, comment "S1: nothing after a launch-step outcome (DF-50)"); the loop head `if self.halt: break` (cycle.py:816-817) stops the cycle. Consequence: the halt fires after ANY outcome of the launch step, not only a successful launch: `launched` (also dry-run `would_launch`), `launch_unknown`, `spawn_error`, `prompt_invalid`/`revalidation_transient` (via `_fail`), and every `_Skip` raised inside `_launch` or `_revalidate` (`revalidation_failed`, `assigned_other`/`unassigned` at re-read, `day_cap`, `budget_exhausted`). A `_Stop` raised inside the launch step (`orca_not_found`, `disabled_mid_cycle`, `origin_mismatch`, `project_read_failed`, `rate_limit_clamped`, `state_dir_unwritable`) ends the cycle directly. Later candidates then get no read, no `considered` stamp and no decision line (design 6.3 line 393 says the same).

**Key Takeaways**
- 13 constants at lines 34-47; 12 are read, `MAX_LAUNCHES_PER_CYCLE` is dead (cycle.py:35 only).
- The real cap on launches is the `launching` flag plus `halt` (cycle.py:524, 833-834, 816-817), and it also halts the cycle after a launch-step skip, not only after a launch.
- The tolerance values 60 (`SKEW_WARN_S`, cycle.py:44) and 300 (`predicates.SKEW_TOLERANCE_S`, predicates.py:17) are two different things; see section 11 for the design doc row that mixes them up.

## 2. Per-cycle flow of one `issue-watch once` poll cycle (`P/cycle.py`)

Entry point: `run_cycle(deps, dry_run)` (cycle.py:1214) builds `_Cycle(deps, dry_run)` and calls `_Cycle.run` (cycle.py:682). `_Cycle.__init__` (544-566) creates the cycle id (`uuid4().hex`), the 240 s `Deadline`, a fresh `github.CallBudget`, the empty line list, the condition list `conds: list[(reason, exit)]`, and the flags `halt`, `dirty`, `stop_reason`. `check_platform` is the caller's job (docstring 1217); `run_cycle` never imports `subprocess`. Control flow uses three private exceptions: `_Skip(reason)` (491, one issue skipped, cycle continues), `_Stop(reason, stamp)` (503, cycle ends with a cycle-level reason), `_Transient` (499, a re-read timed out or got 5xx).

| # | Step (method, lines) | What it does | External calls (GitHub budget counter) | On failure: reason, exit | Writes |
|---|---|---|---|---|---|
| 0 | `run` 685-686: `enabled` gate | `if not deps.config.enabled and not self.dry_run: raise _Stop("not_enabled")` | none | `not_enabled`, exit 0; runs `_conclude(locked=False)` (no lock, no rotation) | one cycle line `not_enabled` |
| 1 | `run` 687-693: `validate_setup(config)` (cycle.py:371-377) | worktree must be an existing directory, then the approvers file is validated (lstat, regular, euid-owned, not group/other-writable, <= 1 MiB, id lines, non-empty) | none (local fs) | `worktree_invalid` or `approvers_invalid`, exit 2; `_conclude(locked=False)` | one cycle line |
| 2 | `run` 694-702: `deps.store.lock()` | non-blocking `flock` on `state_dir/lock` (record.py:380-419) | none | `LockHeld` -> `lock_held`, exit 75; `LockError` -> `lock_missing`/`lock_invalid`, exit 6; both `_conclude(locked=False)` | one cycle line, no rotation |
| 3 | `_steps` 712-713: kill switch | `deps.store.disabled()` is `os.path.lexists(state_dir/DISABLED)` (record.py:421-423, a dangling symlink counts) | none | `_Stop("disabled")`, exit 0 | cycle line only; the health stamp is NOT written (stop_reason set) |
| 4 | `_load` 739-750 | `store.load()`; a real cycle saves a migrated store immediately (746-747, `not dry_run and store.migrated`); `now < doc.next_permitted_at` | none | `store_missing`/`store_invalid` exit 6; `rate_limited` exit 5 | migrated store save (real only) |
| 5 | `_login_step` 752-775 | G1 `github.user(capture, self._tf_shared)`; regex `_LOGIN`; `owner_account_id` pin; clock skew from the `Date` header | G1 = shared call #1 (`spend_shared`, counted only if the deadline allowed the call) | rate limited: `rate_limit_wait` -> `next_permitted_at` set in memory, `_Stop(reason)` exit 5 (`rate_limited` or `rate_limit_clamped`); other read failure -> `_Stop(read.reason)` (`gh_timeout`, `gh_non_json`, `gh_auth_failed`, `project_read_failed`, all exit 3); `login_invalid` exit 3; `account_id_mismatch` exit 2 | clock skew: `cycle_line.clock_skew_s` every cycle where the header parsed; warning line `clock_skew` only when `abs(skew) > SKEW_WARN_S` (60) |
| 6 | `_steps` 716-722 | `deadline.timeout_for(GIT_TIMEOUT_S)`; `launch.check_origin(runner, worktree, timeout) is None` | one `git` call (not GitHub; not budgeted) | no time left: `_Stop("gh_timeout")` exit 3 (comment "Gate C fix C-1"); origin wrong: `origin_mismatch` exit 2 | none |
| 7 | `_sweep` 777-792 | `record.sweep(doc, now)`: pending -> abandoned `pending_orphan`; launched with `now >= lease_expires_at` -> abandoned `claim_not_observed` (record.py:627-651) | none | none | decision line per changed entry (reason = entry `last_reason`, state `abandoned`); store change in memory, saved in the commit |
| 8 | `_discover` 794-808 | G2 `github.discover(runner, trigger, login, self._tf_shared)` | G2 = shared call #2 | `rate_limited` kind -> `_rate_stop` (always clamp 3600 s, `rate_limit_clamped` exit 5); `truncated`/`discovery_duplicate` exit 4; else exit 3 reasons | warning line `discovery_count` when `len(issues) >= 80` |
| 9 | `_steps` 725-737: ordering | dry-run: `record.load_dry_run(state_dir)` gives shadow (warning `dry_run_shadow_reset` when the file was replaced); `predicates.eligibility_order(issues, considered)[:MAX_CANDIDATES]` | none | none | none |
| 10 | `_candidates` 812-834 | for each issue number, unless `halt`: build `_Cand`, call `_examine`, then write one decision line | per-issue reads (see section 4, budget) | `_Skip` -> reason with `state=None`; `_Stop` propagates (candidate gets NO decision line; stamped only if `stop.stamp`) | one decision line per examined candidate |
| 11 | `_launch` 1026-1112 | the launch step (section 5) | probe (local), 3+ reserved GitHub reads, one `git`, one `orca agent launch` | see section 5 | `pending` save before launch; outcome entry in the commit |
| 12 | `_locked_body` -> `_commit` 709, 1116-1126 | one final write: store (real) or `dry-run.json` (dry-run) | none | `OSError` -> `_stopped("state_dir_unwritable")` exit 6 | `dispatch.json` / `dry-run.json` |
| 13 | `_conclude` 1176-1211 | decision lines first, then ONE cycle line; `rotate_if_needed()` only when `locked=True`; `OSError` -> `audit.stderr_fallback(reason, exit, ts=, host=)` | none | none | `audit.jsonl` |

Step 3 is inside the lock; step 0, 1 and the lock failures happen before any state is read. The `enabled` gate therefore runs before `validate_setup`, before the lock and before every external call (cycle.py:685 vs 688, 695, 712, 755).

### 2.1 Exit code and cycle reason

- `_cond(reason)` appends `(reason, exit_for(reason))` to `conds` (587-588); `_stopped(reason)` also sets `stop_reason` (590-592). `exit_for(reason)` is `audit.REASON_TABLE[reason][1]` (cycle.py:480-482).
- `_exit()` (594-595) is `resolve_exit(frozenset(code for _, code in conds))`.
- `resolve_exit(conditions)` (cycle.py:466-477): for `code in _PRECEDENCE = (2, 6, 7, 5, 3, 4)` return the first code present; else `75` only if `set(conditions) - {0} == {75}`; else `0`. Exit 1 is never produced by the cycle (only `once` writes `cycle_crashed`, exit 1, audit.py:57). Exit 4 is last in precedence, exit 75 only when it is the sole non-zero condition.
- `_cycle_reason(exit_code)` (1164-1174): if `exit_code != 0`, the reason of the FIRST condition in `conds` whose code equals `exit_code`; else `stop_reason` if set; else the literal `cycle_complete`. So a skip or entry reason is never a cycle-line reason; the cycle line names a stop reason, a condition reason, or `cycle_complete`.
- Conditions raised without stopping the cycle: `_fail` (1021, `prompt_invalid` / `revalidation_transient`, exit 7, also when the third failure abandons the entry), `launch_unknown` (1108, exit 7), `spawn_error` (1111, exit 7). Each of them is followed by the S1 halt, so a later rate-limit or GitHub failure cannot be added to the same cycle.
- Design 4.3 (issue-watcher.md:173) says "the combinations that can occur are 7 with 5 ... and 7 with 3". **[CODE-CONTRADICTED] as traced**: after a `_fail`/`launch_unknown`/`spawn_error` the candidate has `launching = True`, so `halt` stops the loop (cycle.py:833-834) and no further GitHub read runs; the only exit-7 combination reachable through `_Cycle` is 7 with 6 (the commit save fails, cycle.py:1125-1126; exit 6 wins). `resolve_exit` itself is pure and handles {7,5} and {7,3} (precedence 7 before 5 before 3).

### 2.2 Commit and conclude details

- `_commit_store` (1128-1144), real cycles only: if `examined` and discovery succeeded, `record.set_considered(doc, examined, discovered_numbers, now)` (stamps examined candidates, prunes to the discovery set; record.py:738-745). If `stop_reason is None and self._exit() == 0`, `record.set_last_completed` (the health stamp). If anything changed, `record.prune_consumed_log` then ONE `store.save`. `if self.stop_reason == "state_dir_unwritable": return` (1118) skips the commit.
- Health stamp rule: written only when there is no stop reason AND the exit is 0. A cycle that stopped on `disabled`, `not_enabled`, `disabled_mid_cycle`, any exit 2-6 stop, or one that hit exit 7 does not stamp. [CODE-VERIFIED] against design 6.2 step 14 (issue-watcher.md:364).
- `_commit_shadow` (1146-1162), dry-run only: returns without writing when `shadow is None`, discovery did not run, or nothing was examined / no would-launch / no shadow reset (1148-1152). Otherwise it writes `dry-run.json` with `considered` (pruned to discovery set, examined stamped `now`) and `shadow_launches` (pruned to the last 24 h).
- `_conclude` (1176-1211): builds the cycle line with `gh_calls = budget.total` and `duration_ms = int(deadline.elapsed() * 1000)`; if `stop_reason == "state_dir_unwritable"` it raises `OSError` on purpose so the only output is the stderr fallback (1195-1196, FR-020); `rotate_if_needed()` only when the lock was held (1197-1198); then appends every line.
- Return value `CycleResult(exit_code, reason, cycle_id, launched_issue, would_launch, probe, lines)` (449-458); `probe` is `"skipped"` exactly when `would_launch is not None` (1209).

**Key Takeaways**
- One cycle is: enabled gate, setup validation, lock, DISABLED, load, login (G1), origin (git), sweep, discovery (G2), order, <= 10 candidates, one commit, one audit write. All of it sits in `_Cycle.run`/`_steps`.
- The decision lines come first, then exactly one cycle line, in `_conclude` (cycle.py:1193-1200).
- The cycle line reason is a stop reason, the first condition reason matching the exit code, or `cycle_complete`; skip reasons live on decision lines only.
- The doc's claim that exit 7 can combine with 5 or 3 is not reachable through `_Cycle` because of the S1 halt.

## 3. Candidate selection and the per-candidate gate order (`_candidates` 812-834, `_examine` 915-961)

**Selection.** `predicates.eligibility_order(issues, considered)` (predicates.py:299-312) returns the never-examined issue numbers ascending, then the examined ones sorted by `(considered[n], n)`; `cycle._steps` slices `[:MAX_CANDIDATES]` (cycle.py:736, so 10). `considered` is the store's map in a real cycle (735) and the `dry-run.json` shadow map in a dry-run (732). Discovery already filtered by label and assignee (G2); the cycle re-checks the assignee set locally.

**Per-candidate loop.** For each number: `_Cand(n, issue, entry=self.doc.entries.get(n))`; `_examine(c)` returns `(reason, state)` or raises. `_Skip` gives `(skip.reason, None)`; `_Stop` propagates with no decision line (stamped as examined only when `stop.stamp`); a normal return and a `_Skip` both write one decision line via `_issue_line` (646-661) with approver/event/approved_at from the fresh approval, else from the entry, else nulls, and `note = "re-approved"` when the entry holds a different `approval_event_id` than the new approval. Then `if reason != "budget_exhausted": examined.append(n)` (831-832): everything except `budget_exhausted` is stamped in `considered`.

**Gate order inside `_examine`** (first gate that fires ends the candidate; "calls" = GitHub calls consumed, minimum one page each):

| # | Gate (cycle.py lines) | Condition | Outcome (decision-line reason, state) | Calls |
|---|---|---|---|---|
| E1 | 919-921 | entry state `claimed` or `pending` | `_Skip("already_dispatched")` | 0 |
| E2 | 922-931 | entry state `launched` or `unknown`, or `abandoned` with `pending_at` set | G4 marker read; `_hit(markers, e.pending_at, None)` true -> `_claim(c, None)` = T-10, returns `("claimed", "claimed")`; else `_Skip("already_dispatched")` | G4 |
| E3 | 932-933 | entry state `abandoned` without `pending_at` (an `attempts_exhausted` tombstone) | `_reclaim(c, "already_dispatched")` (901-913): G4 then G3; `_approve(c, events, fallback)`; `_hit(markers, None, approval.approved_at)` true -> `_claim(c, approval)`; else `_Skip("already_dispatched")` (any read or approval failure also becomes the fallback word, except a marker-read failure which keeps `marker_unreadable`) | G4, G3 |
| E4 | 934-935 | entry exists (so state `failed`) and `not record.backoff_elapsed(e, now)` (now < `updated_at + 10 min`, or attempts >= 3) | `_reclaim(c, "in_backoff")` as E3 with fallback `in_backoff` | G4, G3 |
| E5 | 936-937 | `_day_cap_reached()` (867-876): `record.day_cap_count(doc, now)` over `consumed_at` and `consumed_log` in `(now - 24 h, now]`, plus (dry-run) shadow launches in the same window, `>= DAY_CAP` (6) | `_Skip("day_cap")` | 0 |
| E6 | 938-940 | `predicates.is_intended_owner(c.issue.assignees, self.login)` false | `_Skip("unassigned")` (empty set) or `_Skip("assigned_other")` | 0 |
| E7 | 941-943 | G4 marker read via `_val` | read failure -> `_Skip("marker_unreadable")` (all G4 failures incl. incomplete map to it, github.py:880-881); rate limit -> `_Stop` clamp; missing scope -> `_Stop("project_read_failed")`; budget -> `_Skip("budget_exhausted")` | G4 |
| E8 | 944 | G3 events read via `_val` | `events_unreadable` (any failure), `events_incomplete` (page cap or repeated id), same rate/scope/budget mapping | G3 |
| E9 | 945, 878-894 | `predicates.approval_of(...)` with `labels_now=c.issue.labels` (from discovery), trigger and approval label, approvers set, `store_created_at=doc.created_at` | not approved -> `_Skip(result.reason)`: `events_incomplete`, `not_approved`, `approval_before_trigger`, `approval_before_init` (rules in section 8) | 0 |
| E10 | 946-947 | `_hit(markers, None, approval.approved_at)`: an own-login marker strictly after the current approval | `_claim(c, approval)` = T-11 (no entry) or T-12 (failed); returns `("claimed", "claimed")`; the launch never happens | 0 |
| E11 | 948 | G5 edits read | `edits_unreadable`; same rate/scope/budget mapping | G5 |
| E12 | 949-956 | `predicates.unchanged_since(approved_at, edits, events, own_login)` | `_Skip("edited_after_approval")` | 0 |
| E13 | 957 | G6 project-items read | `project_unreadable`; `scope_missing` -> `_Stop("project_read_failed")`, exit 3 | G6 |
| E14 | 958-960 | `predicates.project_check(items, cfg.project_id)` | `_Skip("project_mismatch")` | 0 |
| E15 | 961 | `self._launch(c, approval)` | section 5 | see 5 |

Notes:
- A read failure of kind `rate_limited` in any per-issue read raises `_rate_stop()` (663-668): `next_permitted_at = now + 3600 s`, `_Stop("rate_limit_clamped")` (exit 5, no stamp). Per-issue reads carry no `--include`, so no `Retry-After` exists and the clamp always applies (design 8.3, issue-watcher.md:609).
- A read failure of kind `scope_missing` (any per-issue read, not only G6) raises `_Stop("project_read_failed")`, exit 3 (cycle.py:842-843).
- A read of kind `budget_exhausted` (no call could start: budget cap or deadline floor) is `_Skip("budget_exhausted")` and is the only reason that is not stamped (831). It does not halt the loop, so each remaining candidate that reaches a GitHub read repeats the same skip; candidates ending locally (E1, E5, E6) still get their own reasons.
- The marker read (E7) runs before the events read (E8), so an unreadable marker skips the candidate before events are read. A marker hit at E10 also needs a successful events read (E8) and an approval (E9): an own marker is only honoured when the issue is still approved (T-11/T-12).

### 3.1 Entry-state transitions as driven by the cycle

(`record.*` functions are owned by agent 02; this table shows only where the cycle calls them. `Entry` states: `pending`, `launched`, `unknown`, `failed`, `abandoned`, `claimed`, record.py:34.)

| Cycle trigger (file:line) | From | To | `record` call | Decision line (reason, state) | Cycle exit condition |
|---|---|---|---|---|---|
| `_sweep` 777-792 | `pending` | `abandoned` | `record.sweep` (record.py:638-639) `pending_orphan` | (`pending_orphan`, `abandoned`) | none |
| `_sweep` | `launched`, `now >= lease_expires_at` | `abandoned` | `record.sweep` (640-643) `claim_not_observed` | (`claim_not_observed`, `abandoned`) | none |
| E2 `_claim(c, None)` 929-930 | `launched`, `unknown`, `abandoned` with `pending_at` | `claimed` | `record.mark_claimed` T-10 | (`claimed`, `claimed`) | none |
| E3/E4 `_reclaim` 911-912 | `abandoned` tombstone; `failed` in backoff | `claimed` | `record.mark_claimed` with the current approval | (`claimed`, `claimed`) | none |
| E10 946-947 | no entry; `failed` | `claimed` | `record.mark_claimed` T-11 / T-12 | (`claimed`, `claimed`) | none |
| `_fail` 1018-1024 called from 1056 / 1060 | no entry; `failed` | `failed` (attempts 1-2) or `abandoned` with `last_reason` `attempts_exhausted` (attempts 3) | `record.fail` T-1 / T-3 | (`prompt_invalid` or `revalidation_transient`, `failed`) or (`attempts_exhausted`, `abandoned`) | `_cond(reason)` exit 7 in both cases |
| `_launch` 1091-1092 | no entry; `failed` (after backoff) | `pending` | `record.mark_pending` T-4, then `_save()` (durable BEFORE launch) | none yet | none |
| `_launch` 1095-1098 | `pending` (just saved) | previous document restored whole, saved again | `self._set(before_pending)`; `_save()` | (`budget_exhausted`, no state) | none |
| `_launch` 1101-1105 | `pending` | `launched` | `record.mark_launched` T-5 | (`launched`, `launched`) | none; `launched_issue = n` |
| `_launch` 1106-1109 | `pending` | `unknown` | `record.mark_unknown` T-6 | (`launch_unknown`, `unknown`) | `_cond("launch_unknown")` exit 7 |
| `_launch` 1110-1112 | `pending` | `abandoned` | `record.mark_spawn_error` T-7 | (`spawn_error`, `abandoned`) | `_cond("spawn_error")` exit 7 |
| dry-run `_launch` 1029-1035 | any (nothing written) | none | none; `would_launch = n`, shadow launch time appended | (`launched`, no `state`) | none |

Every cycle-side change is held in `self.doc` and saved once in `_commit_store`, except the two early saves: the migrated store (747) and the `pending` write (1092, plus its undo 1097). In a dry-run every `_set` stays in memory and `_decision` forces `state=None` (cycle.py:639), so dry-run lines never name a written state.

`launch_unknown` and `claim_not_observed` leave the entry looping through E2 on every later cycle: each costs at least one G4 call per cycle while the issue stays in the discovery set, until a marker appears (`claimed`) or the operator runs `reset N --forfeit-guarantee` (CLI, agent 03). `unknown` never leaves on the lease (design 7.3, issue-watcher.md:478; sweep only touches `pending` and `launched`, record.py:638-643).

**Key Takeaways**
- 15 ordered gates; local gates (E1, E5, E6, E9, E10, E12, E14) cost no GitHub call; the reads are G4, G3, G5, G6 in that order.
- The only transitions to `pending`, `launched`, `unknown`, `abandoned (spawn_error)` and `failed` are in `_launch`/`_fail`; `claimed` is reached only through a marker read (E2, E3, E4, E10).
- Skip reasons never change the store, but they do stamp `considered` (except `budget_exhausted`), which pushes the issue behind never-examined ones in the next cycle's order.

## 4. The launch step (`_launch`, cycle.py:1026-1112) and the re-read (`_revalidate`, 979-1016)

`_launch` runs only for a candidate that passed E1-E14. Order, with the line that decides each outcome:

| # | Line | Action | Failure outcome |
|---|---|---|---|
| L0 | 1028 | `c.launching = True` (this arms the S1 halt) | n/a |
| L1 | 1029-1035 | dry-run: `would_launch = n`, shadow launch time appended, return `("launched", None)`; no probe, no re-read, no Orca, nothing written | n/a |
| L2 | 1036-1038 | `deadline.timeout_for(PROBE_TIMEOUT_S)` is None | `_Skip("budget_exhausted")` |
| L3 | 1048-1052 | `launch.find_orca(runner, which=, timeout=probe_allowance)` | None: out of time -> `_Skip("budget_exhausted")`; else `_Stop("orca_not_found", stamp=True)`, exit 2 |
| L4 | 1054-1056 | `launch.build_claim_prompt(n)` | `ValueError` -> `_fail(c, "prompt_invalid")`, exit 7. Not reachable with discovered issues (numbers are validated 1..999999999 in `github.discover`, github.py:827-828), only through a test seam: test_cycle.py:3348 |
| L5 | 1057-1060 | `_revalidate(c)` (below) | `_Skip("revalidation_failed")`, `_Skip("unassigned"/"assigned_other")`, or `_Transient` -> `_fail(c, "revalidation_transient")` exit 7 |
| L6 | 1061-1062 | day cap again | `_Skip("day_cap")` |
| L7 | 1063-1064 | `store.disabled()` again | `_Stop("disabled_mid_cycle", stamp=True)`, exit 0 |
| L8 | 1069-1070 | `not deadline.launch_allowed()` (elapsed > 120 s) | `_Skip("budget_exhausted")` |
| L9 | 1071-1073 | `timeout_for(GIT_TIMEOUT_S)` None | `_Skip("budget_exhausted")` |
| L10 | 1074-1075 | origin re-check (git, not cached) | `_Stop("origin_mismatch", stamp=True)`, exit 2 |
| L11 | 1078-1079 | `launch_allowed()` again (the git call may have crossed 120 s) | `_Skip("budget_exhausted")` |
| L12 | 1082-1092 | `record.PendingContext(approver_id, approval_event_id, approved_at, launch_cwd=str(cfg.worktree), launch_login, launch_account_id)`; `mark_pending`; `_save()` | save `OSError` -> `_Stop("state_dir_unwritable")`, exit 6 |
| L13 | 1095-1098 | `launch_allowed()` after the save; if false the previous document is restored and saved | `_Skip("budget_exhausted")` |
| L14 | 1099 | `d.launcher.launch(orca, cfg.worktree, prompt, LAUNCH_TIMEOUT_S)` (the only call that starts a process which can write outside the host: `orca agent launch`; argv at launch.py:103-116) | outcomes `launched` / `unknown` / `spawn_error` (section 3.1 table) |

`_revalidate(c)` (979-1016, FR-011) re-reads with the reserved budget:
1. G7 `github.reread(runner, budget, n, self._tf)` (always `reserved=True`, github.py:942). The snapshot must be `state.lower() == "open"` and both `cfg.trigger_label` and `cfg.approval_label` in `snap.labels`, else `_Skip("revalidation_failed")` (985-990).
2. `is_intended_owner(snap.assignees, login)` again; failure is `_Skip("unassigned")` or `_Skip("assigned_other")` (991-993; these are the one place skip words other than `revalidation_failed` come out of the re-read).
3. G3' events `reserved=True`, then `approval_of` with the fresh labels; it must be approved AND carry the same `approval_event_id` as the first approval (1007-1011); a voided or newer approval is `revalidation_failed`.
4. G6' project items `reserved=True`, then `project_check`; mismatch is `revalidation_failed` (1012-1016).
5. Edits (G5) are NOT re-read (comment at 1006).
`_rv` (965-977) maps a re-read failure: `rate_limited` -> `_rate_stop` (clamp); `scope_missing` -> `_Stop("project_read_failed")`; `budget_exhausted` -> `_Skip("budget_exhausted")`; kind `timeout` or `transient` -> `_Transient` (becomes a `failed` entry with `revalidation_transient`, exit 7); any other failure -> `_Skip("revalidation_failed")`.

**Key Takeaways**
- Between the last GitHub read and the `pending` save the cycle checks day cap, DISABLED, the 120 s launch cut-off, the origin and (three times) the cut-off again; every one of those is a guard point listed in section 10.
- `pending` is durable before `orca agent launch` starts (cycle.py:1091-1092), and the undo path restores the prior document if the save itself crossed the cut-off (1095-1098).
- `prompt_invalid` is defined and tested but unreachable for discovered issues; it only fires via a test seam.

## 5. How the cycle spends the 35-call GitHub budget

Mechanism (`github.CallBudget`, github.py:437-463, defined by agent 02; consumption traced here). Two counters per cycle: `calls` (per-issue) and `shared_calls`. `spend(reserved=False)` refuses when `calls >= CALL_CAP - RESERVED_CALLS = 32`; `spend(reserved=True)` refuses when `calls >= 35`; a refused spend counts nothing. `spend_shared()` is never refused. `total = calls + shared_calls` is written to the cycle line as `gh_calls` (cycle.py:1188). `_call` (github.py:557-577) first asks the deadline (`timeout_for()` is None when < 5 s remain, so no call starts), then spends the budget, then runs the argv; both refusals return `Read(None, "budget_exhausted", "budget_exhausted")` (github.py:588).

| Step | Call | Counter | Spent by | If refused |
|---|---|---|---|---|
| Login (cycle.py:755) | G1 `gh api user --include` | shared #1 | `_tf_shared` (cycle.py:580-585) increments only if the deadline allowed the call | no call: `gh_timeout` exit 3 |
| Discovery (cycle.py:796) | G2 `gh issue list ...` | shared #2 | `_tf_shared` | `gh_timeout` exit 3 |
| E2/E3/E4/E7 | G4 comments, one call per page (max 5 pages) | per-issue, non-reserved | `_call` -> `spend(False)` | `_Skip("budget_exhausted")`, not stamped |
| E3/E4/E8 | G3 events, one per page (max 5) | per-issue, non-reserved | same | same |
| E11 | G5 edits GraphQL, one per page (max 5) | per-issue, non-reserved | same | same |
| E13 | G6 project items GraphQL, one per page (max 5) | per-issue, non-reserved | same | same |
| L5 step 1 | G7 re-read (1 call) | per-issue, RESERVED | `spend(True)` | `_Skip("budget_exhausted")` |
| L5 step 3 | G3' events (>= 1 call) | RESERVED | `spend(True)` | same |
| L5 step 4 | G6' items (>= 1 call) | RESERVED | `spend(True)` | same |

Arithmetic:
- Idle cycle (no trigger issues): 2 calls (G1, G2). `test_cli_e2e.py` asserts exactly 2 `gh` calls for an idle cycle (scope hint; FR-001).
- Maximum: 2 shared + 35 per-issue = 37 calls (design 6.3, issue-watcher.md:388). Non-reserved reads stop at 32; the last 3 slots can be used only by G7, G3', G6'.
- "Reserved" means the last three slots of the same counter, not a separate pool: if fewer than 32 non-reserved calls were used, the re-read may spend more than 3; and if G3' or G6' needs more than one page the re-read can run out of budget (`budget_exhausted` skip, no launch).
- Minimum per-candidate reads when a candidate runs the whole chain: 4 (G4, G3, G5, G6), so with one page per read `floor(32 / 4) = 8` candidates can be examined before `budget_exhausted` (design 6.3 line 391: `k = min(10, 8)`).
- Candidates that end locally (E1 claimed/pending, E5 day cap, E6 owner) spend 0 calls; entry-state candidates E2 spend >= 1; E3/E4 spend >= 2; a candidate that claims through a marker (E10) spends 2.
- Orca probe and `git` calls are not GitHub calls and do not use the counter; the deadline bounds them (240 s total).

**Key Takeaways**
- The cap is enforced per call in `_call` (github.py:574), not per candidate; paging multiplies the cost.
- A refused call is a skip (`budget_exhausted`, not stamped, cycle continues), never an error exit; the exceptions are G1/G2, which can only fail by deadline (`gh_timeout`).
- Worst case 37 calls per cycle; 2 on an idle cycle.

## 6. The pure predicates (`P/predicates.py`, 312 lines; no I/O, no clock, imports nothing from `superclaude`)

Constants: `CLAIM_MARKER = "<!-- sc:issue:claim -->"` (14), `SKEW_TOLERANCE_S = 300` (17, the claim-marker window, not the clock-skew warning), `MAX_ISSUE_NUMBER = 999_999_999` (20), `OPERATION_ID_PATTERN = ^[A-Za-z0-9._:-]{1,128}$` (57). Helpers: `parse_utc` (27-39, strict `YYYY-MM-DDTHH:MM:SSZ`, ASCII digits and capital `Z` only, raises `ValueError`), `format_utc` (42-49, rejects naive datetimes), `valid_issue_number` (52-54, `type(value) is int`, 1..MAX), `valid_operation_id` (65-67). Frozen dataclasses: `Login` 71, `DiscoveredIssue` 80, `LabelEvent` 90, `IssueSnapshot` 103, `ProjectItem` 113, `MarkerEvidence` 122, `CommentEdit` 133, `EditEvidence` 143, `ApprovalResult` 152.

### 6.1 `is_intended_owner(assignees, own_login) -> (bool, reason|None)` (predicates.py:162-174)
Rule: `set(assignees) == {own_login}` gives `(True, None)`. Else an empty set gives `(False, "unassigned")`, anything else `(False, "assigned_other")`. The comparison is exact (no case folding): a set holding the own login plus another user is `assigned_other`. Callers: cycle.py:938 (E6) and 991 (re-read).

### 6.2 `approval_of(events, *, labels_now, trigger_label, approval_label, approvers, store_created_at) -> ApprovalResult` (predicates.py:185-234)
Sorts events by `(created_at, id)` (199). Builds `appr_on` (`labeled` with the approval label), `appr_off` (`unlabeled`, approval label), `trig_on` (`labeled`, trigger label). Rules, in this exact order; the first that fails returns `ApprovalResult(False, reason, None, None, None)`:

| # | Lines | Rule | Reason |
|---|---|---|---|
| 1 | 205-209 | the set of second-truncated times of ALL approval-on events intersects the times of approval-off events OR of trigger-on events (a same-second collision) | `events_incomplete` |
| 2 | 210-211 | `approval_label not in labels_now` or no approval-on event | `not_approved` |
| 3 | 212-215 | the last approval-on event (by sort key) has an approval-off event with a greater `(created_at, id)` | `not_approved` |
| 4 | 216-223 | the last approval-on actor must have `actor_type == "User"`, a non-null login not ending in `[bot]`, `type(actor_id) is int` (a bool fails) and `actor_id in approvers` | `not_approved` |
| 5 | 224-227 | no trigger-on event at all (OQ-38; absent evidence never counts) | `events_incomplete` |
| 6 | 228-229 | `approval.created_at <= trig_on[-1].created_at` (approval must be strictly after the last trigger event) | `approval_before_trigger` |
| 7 | 230-231 | `approval.created_at <= store_created_at` (strictly after the store was initialised) | `approval_before_init` |
| ok | 232-234 | `ApprovalResult(True, None, actor_id, event_id, created_at)` | none |

Callers: cycle.py:883 (`_approve`, with `labels_now=c.issue.labels` from discovery) and cycle.py:998 (re-read, `labels_now=snap.labels` and the same `approval_event_id` required). An unlabel BEFORE a relabel does not void the approval (rule 3 compares only later unlabels); pinned by `test_ac3_unlabeled_before_relabel_still_approves__fr006` (test_predicates.py:171).

### 6.3 `unchanged_since(approved_at, edits, events, *, own_login) -> "edited_after_approval" | None` (predicates.py:237-259)
Collects: issue `created_at` and `last_edited_at`; for each comment whose `author_login != own_login` (a null author counts as not own), its `created_at` and `last_edited_at`; the `created_at` of every `renamed` event. Returns `edited_after_approval` if any non-null time is `>= approved_at` (an equal time counts as changed, OQ-37). The watcher's own comments are ignored entirely. Caller: cycle.py:949 (E12); not repeated at re-read.

### 6.4 `project_check(items, project_id) -> "project_mismatch" | None` (predicates.py:262-271)
`matching = [i for i in items if not i.is_archived and i.project_id == project_id]`. Passes only if `len(matching) == 1` and `matching[0].status_name == "Backlog"`; anything else is `project_mismatch`. Callers: cycle.py:958 (E14), 1015 (re-read; mismatch there is `revalidation_failed`).

### 6.5 `marker_time`, `marker_in_window` (predicates.py:274-296)
`marker_time = max(created_at, updated_at)` (DF-16: an edited old comment counts). `marker_in_window(marker, *, own_login, pending_at, approved_at)`: false unless `marker.marker` and `marker.login == own_login`; with `pending_at` set the time must be `>= pending_at - 300 s`; otherwise only `approved_at is not None and when > approved_at`. The cycle's `_hit` (cycle.py:848-865) returns False when both floors are None, else `any(...)` over the markers.

### 6.6 `eligibility_order(discovered, considered) -> list[int]` (predicates.py:299-312)
Never-examined numbers ascending, then examined numbers by `(considered[n], n)`. The cap is applied by the cycle (MAX_CANDIDATES 10).

**Key Takeaways**
- Seven approval rules in a fixed order; the first failure names the reason; success needs a human `User` actor whose numeric id is in the approvers file.
- Strictness: approval must be strictly after the trigger event and the store creation; edits at or after approval void it; same-second label collisions are `events_incomplete` (fail closed).
- `SKEW_TOLERANCE_S` (300) belongs only to `marker_in_window`.

## 7. The audit log (`P/audit.py`, 404 lines)

### 7.1 Writer
- Path `state_dir/audit.jsonl` (`AuditLog.__init__`, audit.py:126-128). `append(line)` (130-139): `json.dumps(line, sort_keys=True, ensure_ascii=True)` plus `"\n"` encoded ASCII (118-120); opens `O_WRONLY | O_APPEND | O_CREAT` with mode `0o600` (the mode applies at creation only), ONE `os.write`, closes, raises `OSError` on a short write.
- `rotate_if_needed()` (141-156), documented "call only with the lock held": stat size; missing file or `size < ROTATE_BYTES` (5 MiB, line 106) returns; else for `n` in 3, 2, 1 `os.replace("audit.jsonl.n" -> ".n+1")` (a missing file is ignored), then `os.replace("audit.jsonl" -> "audit.jsonl.1")`, then `_fsync_dir(state_dir)`. At most four rotated files (`_ROTATIONS = 4`, line 107); the previous `.4` is overwritten. Production callers: cycle.py:1198 (only when `locked=True`) and cli.py:276 (reset). An exit-75 or pre-lock exit appends and never rotates (cycle.py:1197).
- `stderr_fallback(reason, exit_code, *, ts=None, host=None)` (381-404): validates the reason is in `REASONS` and the `exit`, `ts`, `host` values; writes ONE JSON line `{"kind": "cycle", "ts", "host", "exit", "reason"}` to stderr (no login, no cycle id). Call sites: cycle.py:1202 (audit write failed or `state_dir_unwritable`), cli.py:79 (config/platform failure), 127 (`cycle_crashed`), 219 (reset usage error), 266 and 279 (reset).
- Writers of real audit lines: `cycle._conclude` (cycle.py:1176-1211) and `cli._write_reset` (cli.py:255-279). No other module writes the file.

### 7.2 Line schema (`_KEYS` 162-175, `_TYPES` 178-197, `_RULES` 229-243)
Common required keys for every kind (`_COMMON`, 159): `kind`, `ts`, `host`, `login`, `cycle_id`, `dry_run`, `reason`.

| Key | Cycle line | Decision line | Warning line | Type (null?) | Closed-shape rule |
|---|---|---|---|---|---|
| `kind` | `"cycle"` | `"decision"` | `"warning"` | str | one of the three kinds |
| `ts` | required | required | required | str | `YYYY-MM-DDTHH:MM:SSZ`, parsed |
| `host` | required | required | required | str | printable token, 1-255 chars |
| `login` | required | required | required | str or null | printable, no whitespace, 1-100 chars |
| `cycle_id` | required | required | required | str | 32 lowercase hex (`uuid4().hex`) |
| `dry_run` | required | required | required | bool | n/a |
| `reason` | required | required | required | str | key of `REASON_TABLE`, and not a `note`-kind name |
| `exit` | required | no | no | int | 0..255 |
| `gh_calls` | required | no | no | int | >= 0 |
| `duration_ms` | required | no | no | int | >= 0 |
| `discovery_count` | optional | no | optional | int | >= 0 |
| `clock_skew_s` | optional | no | optional | int | no rule beyond int |
| `issue` | no | required | optional | int | 1..999,999,999 |
| `approver_id` | no | required | no | int or null | > 0 |
| `approval_event_id` | no | required | no | int or null | > 0 |
| `approved_at` | no | required | no | str or null | `YYYY-MM-DDTHH:MM:SSZ` |
| `state` | no | optional | no | str | one of `pending, launched, unknown, failed, abandoned, claimed` (`_ENTRY_STATES`, 204) |
| `note` | no | optional | no | str | must be a REASON_TABLE name of kind `note` (only `re-approved`) |

`line(kind, **fields)` (261-285) raises `ValueError` for an unknown kind, an extra key, a missing key, a wrong type (a bool is not an int), a value outside its shape, or an unknown reason. The builders `cycle_line` (292, `exit_code` is written as `exit`; optional keys only when not None), `decision_line` (322), `warning_line` (354) only add `state`, `note`, `issue`, `discovery_count` and `clock_skew_s` when they are not None. No key can hold an issue title, body, label name or stderr text, but `host` and `login` accept any printable token (module docstring, audit.py:5-8), so the setup doc sentence "No issue title, body, label name or error text is ever written to it" (docs/designs/issue-watcher-setup.md:418) is stronger than the code guarantee (see Gaps).
- `issue` on a warning line is never set by the cycle (cycle `_warn` passes only `discovery_count` / `clock_skew_s`, cycle.py:608-619); only `cli._write_reset` sets it (cli.py:272, for `reset_refused`).

### 7.3 Line content written by the cycle
- Decision line per examined candidate: `_decision` (cycle.py:621-644): `reason`, `issue`, `state` (None in a dry-run), `approver_id`, `approval_event_id`, `approved_at`, optional `note="re-approved"`; sweep decision lines use the entry's `last_reason` and state `abandoned` (784-791).
- Warning lines: `discovery_count` (807), `clock_skew` (775), `dry_run_shadow_reset` (731). A warning line never carries `issue`.
- Cycle line: exactly one per `once` exit that reaches `_conclude`, with `gh_calls`, `duration_ms`, optional `discovery_count`, `clock_skew_s` (cycle.py:1180-1192).
- `once` exits with no `audit.jsonl` line at all (stderr fallback only): a config or platform failure before `run_cycle` (cli.py:88-91, 79), an unexpected exception (cli.py:127), `state_dir_unwritable` (cycle.py:1195-1196).

### 7.4 Readers of `audit.jsonl`
`Grep slo_numbers|SloNumbers|audit.jsonl|AuditLog` over `src/**/*.py` finds: the writers above, `cli.py:173` (constructs `AuditLog` for `status`), `cycle.py:1272` (the `audit` parameter of `status_report`, documented "accepted for the fixed signature and not read", cycle.py:1280-1281) and the definition of `slo_numbers` at cycle.py:1359. No production code reads the file or calls `slo_numbers`; only `tests/issue_watch/test_slo_helper.py` does. See the Defect Candidates section.

**Key Takeaways**
- Three line kinds, 18 distinct keys, every value type- and shape-checked before it is written; only `host` and `login` are free printable tokens.
- Rotation is size-triggered (5 MiB), keeps four old files, and only runs with the lock held.
- Nothing in the snapshot reads `audit.jsonl` back, and the SLO reducer has no production caller.

## 8. `REASON_TABLE` (59 entries, audit.py:26-102) cross-referenced to where each word is raised

Count: `Grep '^    "[a-z_-]+": \("' audit.py` gives 59. `REASONS = frozenset(REASON_TABLE)` (audit.py:104). The test `test_audit.py:214` pins the names literally in order (`list(REASON_TABLE) == EXPECTED_NAMES`) and `:223` pins every `(kind, exit)` pair. The decision line or cycle line column says which audit line kind the word appears on in this snapshot.

### 8.1 Cycle-kind reasons (appear on the cycle line)

| Reason | Exit | Raised at (file:line) | Notes |
|---|---|---|---|
| `config_invalid` | 2 | cycle.py:110-111 `_invalid` (raised through `load_config`, 129-272) | surfaced by cli.py:77-81 as stderr fallback; never inside `run_cycle` |
| `approvers_invalid` | 2 | cycle.py:294-361 via `validate_setup` 377; `_Stop(exc.reason)` 689-690 | |
| `platform_unsupported` | 2 | cycle.py:286-291 (`check_platform`); caller cli.py:88 | stderr fallback only |
| `worktree_invalid` | 2 | cycle.py:373-376; `_Stop` 690 | |
| `origin_mismatch` | 2 | cycle.py:722 (start), 1075 (before launch, stamp True) | |
| `orca_not_found` | 2 | cycle.py:1052 (stamp True) | |
| `account_id_mismatch` | 2 | cycle.py:768-769 | needs `owner_account_id` in config |
| `store_invalid` | 6 | record.py:136, 358-366 (`load`); cycle.py:743-744 | |
| `store_missing` | 6 | record.py:358 | `dispatch.json` absent (run `init-state`) |
| `lock_missing` | 6 | record.py:395; cycle.py:700-701 | |
| `lock_invalid` | 6 | record.py:397, 401; cycle.py:700-701 | symlink, directory, not regular, wrong owner |
| `state_dir_unwritable` | 6 | cycle.py:605 (`_save`), 1126 (`_commit`); record.py:780-801 (`init_state`) | cycle writes stderr fallback only (cycle.py:1195-1196) |
| `login_invalid` | 3 | cycle.py:764-765 | G1 login fails `_LOGIN` regex |
| `gh_auth_failed` | 3 | github.py:585 (default of `_SHARED_REASONS.get(kind, "gh_auth_failed")`); cycle.py:762, 802 | any unclassified G1/G2 failure |
| `gh_timeout` | 3 | cycle.py:720; github.py:489-491, 589 | also deadline floor on G1/G2 |
| `gh_non_json` | 3 | github.py:492, 800, 841 | |
| `project_read_failed` | 3 | cycle.py:843, 972; github.py:494 | `scope_missing` kind on any read |
| `truncated` | 4 | github.py:823-824 (>= 100 results) | |
| `discovery_duplicate` | 4 | github.py:829-830 | |
| `rate_limited` | 5 | cycle.py:750 (`now < next_permitted_at`); github.py:427 (G1 with a usable header) | |
| `rate_limit_clamped` | 5 | cycle.py:668 (`_rate_stop`); github.py:431 | per-issue and G2 limits always clamp |
| `lock_held` | 75 | cycle.py:699 | |
| `cycle_crashed` | 1 | cli.py:127 only | stderr fallback + stderr message; never written by the cycle |
| `disabled` | 0 | cycle.py:713 | |
| `disabled_mid_cycle` | 0 | cycle.py:1064 (stamp True) | |
| `not_enabled` | 0 | cycle.py:686 | |
| `cycle_complete` | 0 | cycle.py:1174 | named by `_cycle_reason` when no stop reason |

### 8.2 Skip-kind reasons (decision lines, exit 0)

| Reason | Raised at |
|---|---|
| `not_approved` | predicates.py:211, 215, 223; fallback cycle.py:892 |
| `approval_before_trigger` | predicates.py:229 |
| `approval_before_init` | predicates.py:231 |
| `events_incomplete` | predicates.py:209, 227; github.py:861 (page cap, repeated event id) |
| `events_unreadable` | github.py:860 (any other failed events read) |
| `edited_after_approval` | predicates.py:258 via cycle.py:955-956 |
| `project_mismatch` | predicates.py:271 via cycle.py:959-960 |
| `project_unreadable` | github.py:928 via `_val` |
| `unassigned`, `assigned_other` | predicates.py:173-174 via cycle.py:938-940, 991-993 |
| `already_dispatched` | cycle.py:921, 931, and as `_reclaim` fallback 913/933 |
| `in_backoff` | cycle.py:935 as the `_reclaim` fallback (a failed entry in backoff that is not claimed) |
| `day_cap` | cycle.py:937, 1062 |
| `budget_exhausted` | github.py:588 (`_NO_CALL`); cycle.py:845, 974, 1038, 1051, 1070, 1073, 1079, 1098; NOT stamped in `considered` (831) |
| `revalidation_failed` | cycle.py:977, 990, 1011, 1016 |
| `marker_unreadable` | github.py:880-881 (all G4 failures, including incomplete) |
| `edits_unreadable` | github.py:898 |

### 8.3 Entry-kind reasons (decision lines; the entry's `last_reason`)

| Reason | Exit | Raised at |
|---|---|---|
| `prompt_invalid` | 7 | cycle.py:1056 (unreachable for discovered issues) |
| `revalidation_transient` | 7 | cycle.py:1060 (from `_Transient`, 975-976) |
| `attempts_exhausted` | 0 | record.py:523 (third `fail`); shown at cycle.py:1023-1024 with state `abandoned`; the cycle still adds condition exit 7 for the underlying fail reason (1021) |
| `spawn_error` | 7 | cycle.py:1111 |
| `launch_unknown` | 7 | cycle.py:1108 |
| `pending_orphan` | 0 | record.py:639 (sweep), emitted at cycle.py:785 |
| `claim_not_observed` | 0 | record.py:643 (sweep), emitted at cycle.py:785 |
| `launched` | 0 | cycle.py:1105 (real), 1035 (dry-run would-launch) |
| `claimed` | 0 | cycle.py:899 |

### 8.4 Note, warning and operator reasons

| Reason | Kind | Exit | Raised at |
|---|---|---|---|
| `re-approved` | note | 0 | cycle.py:660; only valid as a `note` value (audit.py:280-284 rejects it as a `reason`) |
| `discovery_count` | warning | 0 | cycle.py:807 (>= 80) |
| `clock_skew` | warning | 0 | cycle.py:775 (skew > 60 s) |
| `dry_run_shadow_reset` | warning | 0 | cycle.py:731 |
| `reset_refused` | warning | 2 | cli.py:248 (decision-state refusal), cli.py:219 (usage, stderr only) |
| `operator_reset` | skip/warning | 0 | cli.py:244, 250 |

Totals: cycle 7+5+5+2+2+1+1+4 = 27 (exit 2: 7, exit 6: 5, exit 3: 5, exit 4: 2, exit 5: 2, exit 75: 1, exit 1: 1, exit 0: 4), skip 17, entry 9, note 1, warning 4, skip/warning 1 = 59.

### 8.5 Exit-code map (from the table; precedence from `resolve_exit`)

| Exit | Reasons | Produced by |
|---|---|---|
| 0 | `cycle_complete`, `disabled`, `disabled_mid_cycle`, `not_enabled`, every skip reason, `attempts_exhausted`, `launched`, `claimed`, `pending_orphan`, `claim_not_observed` | cycle |
| 1 | `cycle_crashed` | `once` only (cli.py:123-129) |
| 2 | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch` (+ `reset_refused`) | cycle and cli |
| 3 | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` | cycle |
| 4 | `truncated`, `discovery_duplicate` | cycle |
| 5 | `rate_limited`, `rate_limit_clamped` | cycle |
| 6 | `store_invalid`, `store_missing`, `lock_missing`, `lock_invalid`, `state_dir_unwritable` | cycle |
| 7 | `prompt_invalid`, `revalidation_transient`, `launch_unknown`, `spawn_error` | cycle (launch step) |
| 75 | `lock_held` | cycle |

Precedence when several conditions are present: 2, then 6, then 7, then 5, then 3, then 4 (cycle.py:462); 75 only alone; otherwise 0. [CODE-VERIFIED] against design 4.3 (issue-watcher.md:159-173).

**Adding a skip reason (extension pattern).** (1) add the name to `REASON_TABLE` with kind `skip` and exit 0 (audit.py:26); (2) raise `_Skip("name")` from `_examine`/`_val` or return it from a predicate; (3) update the literal pin in `tests/issue_watch/test_audit.py` (`EXPECTED_NAMES`, `EXPECTED_TABLE`; the pin test fails otherwise, test_audit.py:214-227). `audit.line` raises `ValueError` for any reason not in the table (audit.py:279-281), so a typo fails at the first line built. New audit key: add it to `_KEYS`, `_TYPES`, `_RULES` (audit.py:162-243) and to the forbidden-key tests. New predicate: add a pure function to predicates.py and call it from `_examine` in the gate order of section 3; `test_predicates.py:708` checks every predicate reason exists in the table.

**Key Takeaways**
- 59 words: 27 cycle-kind, 17 skip, 9 entry, 1 note, 4 warning, 1 skip/warning; each has a raise site above.
- Five words never come out of `run_cycle`: `config_invalid` (via `load_config` before it), `platform_unsupported`, `cycle_crashed`, `reset_refused`, `operator_reset` (CLI-owned).
- Reason words are the only way a decision reaches the audit log; every state change is paired with one.

## 9. Dry-run versus real behaviour (as the cycle sees it)

`once --dry-run` runs the same `run_cycle` with `dry_run=True` (cli.py:122, 132-136 print `probe:` and `would_launch:` only in a dry-run). All differences, each with the line that makes it:

| Aspect | Real cycle | Dry-run | Lines |
|---|---|---|---|
| `enabled` gate | `enabled: false` -> exit 0 `not_enabled` | ignored | cycle.py:685 |
| Setup validation, lock, DISABLED check, store load, `next_permitted_at` check | yes | yes (a dry-run needs `dispatch.json`, takes the same lock, honours DISABLED and a persisted rate limit) | 688, 695, 712, 739-750 |
| Migrated store saved | yes, immediately | never (kept in memory) | 746-747 |
| G1, G2, origin check, all per-issue reads | yes | yes (all GitHub reads still run) | 755, 796, 721, 941-957 |
| Sweep | result kept and saved at commit | result kept in memory only; the decision lines are still written (state omitted) | 777-792 |
| Rate limit stop | `next_permitted_at` persisted | set in memory, never persisted | 760, 667; test_cycle.py:4071 |
| `considered` map | the store's `considered` | the shadow map from `dry-run.json` | 727-735 |
| Corrupt or unreadable `dry-run.json` | not opened | replaced with an empty shadow, warning `dry_run_shadow_reset` | 727-731; record.py:831-848 |
| Day cap | store entries + `consumed_log` | the same plus `shadow_launches` in the last 24 h | 867-876 |
| Claim detection (T-10/11/12) | recorded and saved | recorded in memory only; decision line `claimed` without `state` | 896-899; 639 |
| `_launch` | the 14 steps of section 4 | returns at L1: `would_launch = n`, shadow launch time appended, decision line `launched` with no `state`; no `find_orca`, no prompt, no re-read, no day-cap/DISABLED/origin recheck, no `pending` write, no Orca call | 1029-1035 |
| One-launch halt | yes | yes (`launching = True` is set before the dry-run branch) | 1028-1035, 833 |
| Final write | `dispatch.json` (one save) | `dry-run.json` only when something was examined, would launch, or the shadow was reset; never `dispatch.json`, never the health stamp | 1121-1124, 1146-1162 |
| Audit lines | `dry_run: false` | `dry_run: true`; `state` absent on decision lines | 639 |
| Cycle result | `launched_issue` | `would_launch`, `probe = "skipped"` | 1203-1210 |
| Exit code and reasons | as computed | the same computation, same table | 1178-1179 |

So a dry-run exercises discovery, the gate chain E1-E14 and the audit writer, but it does not exercise any of L2-L14 (probe, re-read, `pending` write, launch). Dry-run decisions carry the same reason words, so the owner can read the would-be outcome of the gate chain from `audit.jsonl`.

**Key Takeaways**
- Dry-run is read-only for GitHub-state purposes (all reads happen) and for `dispatch.json`; it writes `audit.jsonl` and `dry-run.json`.
- Because the launch branch returns early, a dry-run cannot reveal an Orca-probe, re-read or launch-step problem.

## 10. The `enabled` gate and the DISABLED kill switch as seen by the cycle

| Gate | Where | Condition | Reason, exit | Effect |
|---|---|---|---|---|
| `enabled` | cycle.py:685-686; `Config.enabled` parsed at 228-230 (default `False`; must be a JSON boolean) | `not config.enabled and not dry_run` | `not_enabled`, 0 | `_conclude(locked=False)`: one cycle line, no lock, no GitHub call, no store read |
| DISABLED file, start | cycle.py:712-713 via `store.disabled()` = `os.path.lexists(state_dir/"DISABLED")` (record.py:421-423; a dangling symlink counts) | file exists (any type, any content) | `disabled`, 0 | after the lock, before the store load and every GitHub call; cycle line only; no health stamp (stop reason set) |
| DISABLED file, mid-cycle | cycle.py:1063-1064 | file exists after the re-read and day-cap checks | `disabled_mid_cycle`, 0 (`stamp=True`: the candidate is stamped in `considered`) | no `pending` write, no launch |
| `next_permitted_at` | cycle.py:748-750 | `now < doc.next_permitted_at` | `rate_limited`, 5 | before any GitHub call |

Observations: dry-run honours DISABLED (the check is in `_steps`, which both modes run) but ignores `enabled`. `disabled` and `not_enabled` are exit 0, so a scheduler sees success while nothing runs; `status` reports `disabled_since` from the file's mtime (cycle.py:1292, 1329; agent 03). The only places the snapshot sets `enabled: true` are test fixtures (`conftest.make_config`) and the operator's JSON; the shipped default is `false` (cycle.py:228), and `cli.py` has no code that sets it.

**Key Takeaways**
- Two independent switches: config `enabled` (default false, ignored by dry-run) and the `DISABLED` file (honoured twice per real cycle, once by a dry-run).
- Both stop the cycle with exit 0 and no health stamp.

## 11. Deliverable (a): test-pin table

Counts: `wc -l` and `Grep '^\s*def test_'` run against `/home/coder/.cache/ic-snap-20261120/master/tests/issue_watch/` in this session (parametrised cases are not expanded). The assignment header says "six test files" but names five (test_cycle, test_predicates, test_audit, test_marker_contract, conftest); five rows follow. All of these tests are mocked: they use `FakeRunner`, `FakeLauncher`, `GhWorld`, `FakeClock`; none calls the real `gh`, `git` or Orca (`stub_path` in conftest.py:1108 provides PATH stubs only for other files' e2e tests).

| Path | Lines | Test count | What it pins | Key test names |
|---|---|---|---|---|
| `tests/issue_watch/test_cycle.py` | 4982 | 237 | Part A (l.78-1210): `load_config` rules and defaults, XDG default state dir, 50-char label and 64-char project id edges, no `~` expansion, network-FS deny set and `/proc/self/mountinfo` parsing (`fs_type_of`), `check_platform`, `validate_approvers` (symlink, mode, owner, FIFO, size 1 MiB, TOCTOU swap), `validate_setup` order (worktree first), `resolve_exit` precedence over every pair and every subset, `exit_for`, `Deadline` constants (240, 5, 120). Part B (1211-2357): idle cycle = 2 gh calls, login/account-id failures, lock held 75 with no rotation, DISABLED and `not_enabled` = 0 calls and no health stamp, dry-run ignores `enabled`, origin mismatch, store missing/invalid, shared-failure voids the cycle, discovery bounds (99 ok, >= 100 exit 4, duplicate), warning thresholds (79/80 and 60/61 s), rate-limit persistence and clamp, deadline floors and the 120 s launch cut-off, one cycle line per exit, REASON_TABLE kind/exit parity. Part C (2358-4217): every per-issue skip reason, entry-state skips, marker claims (T-10/11/12), tombstones, launch step order with durable `pending`, unknown/spawn_error/probe/prompt outcomes, S1 halt, re-read outcomes (FR-011), DISABLED/origin between discovery and the pending write, S1 cases A and B, `considered` map stamping and pruning, dry-run (writes only shadow, never persists a rate limit, honours a persisted one), failed-entry backoff and third-failure abandonment. Part D (4218-4982): 50-cycle at-most-once run, 24 h acceptance property, second `once` launches nothing, 35-call budget (32 + 3 reserved), Gate C fix tests (deadline edges, `cycle_complete`, save failures, migration, S1 after spawn error, mountinfo reader). | `test_resolve_exit_precedence_over_every_pair__fr028` (990), `test_resolve_exit_seven_with_five_is_seven__fr028` (1005), `test_idle_cycle_makes_two_gh_calls_and_writes_one_cycle_line__fr001` (1444), `test_enabled_false_is_exit_0_not_enabled_with_zero_calls__fr027` (1607), `test_dry_run_ignores_enabled_false__fr027` (1623), `test_exit_and_kind_follow_reason_table__df41` (2290), `test_the_launch_steps_run_in_the_fr014_order_and_pending_is_durable__fr010_fr014` (3151), `test_the_launch_steps_stop_at_the_first_launch_outcome__fr016_s1` (3371), `test_s1_case_a_fifteen_skipping_issues_examine_k_then_the_rest__fr016_df50` (3721), `test_s1_case_b_fifteen_eligible_issues_examine_and_launch_exactly_one__fr016_df50` (3760), `test_a_dry_run_never_persists_a_rate_limit__fr019_fr028` (4071), `test_fifty_cycles` (4302), `test_second_once_launches_nothing` (4408), `test_ten_skipping_candidates_stop_at_32_calls_and_leave_two_unread__nfr009` (4445), `test_the_three_reserved_calls_remain_for_the_re_read__nfr009` (4467), `test_no_later_candidate_is_read_or_stamped_after_a_launch_step_outcome__fr016_s1_c10` (4914). No test references `MAX_LAUNCHES_PER_CYCLE` (grep over tests/ is empty). |
| `tests/issue_watch/test_predicates.py` | 732 | 44 | `approval_of` rows (allow-listed `User` approves; bot, wrong id, missing actor fields, bool id, no approval event, unlabel after, unlabel before relabel still approves, before trigger, before init, exactly at store creation is before init, opposing same-second tie and missing trigger event are `events_incomplete`, order key `(created_at, id)`); `unchanged_since` (edit after approval, equal timestamp counts, only `renamed` events count, own-login comment ignored, strictly earlier passes); `is_intended_owner` (exactly own login); `project_check` (one live Backlog item; archived item ignored); `marker_in_window` (exactly at the skew floor counts, one second before does not, `pending_at` wins, strictly after approval otherwise, other login or no marker never, edited old comment counts, no floor never); `eligibility_order`; `parse_utc`/`format_utc`; `valid_issue_number`; `valid_operation_id`; every predicate reason is in the audit table. | `test_ac3_allow_listed_user_approves__fr005` (108), `test_ac3_unlabeled_before_relabel_still_approves__fr006` (171), `test_ac3_approval_exactly_at_store_creation_is_before_init__fr005` (241), `test_ac3_opposing_tie_is_events_incomplete__fr006` (273), `test_ac3_equal_timestamp_counts_as_changed__fr005` (385), `test_fr009_marker_exactly_at_skew_floor_counts` (521), `test_fr023_new_issue_first_then_oldest_examined` (576), `test_every_predicate_reason_is_in_the_audit_table` (708) |
| `tests/issue_watch/test_audit.py` | 849 | 46 | The 59 reason names pinned literally in order and every `(kind, exit)` pair, never imported from the module; `line()` rejections (unknown kind/reason/key, missing key, wrong type, value outside shape, `note` name as a reason); forbidden-key lists; host/login accept any printable token; state enum equals the design set; issue bound equals the predicates bound; append (sorted keys, ASCII, one line per call, mode 0600, one `os.write`); rotation (below threshold does nothing, 5 MiB shifts every file, exactly four rotated files, partial states, one directory fsync after the last replace, no fsync without rotation); exit-75 path appends without rotating; stderr fallback emits five keys; builder examples for cycle, decision (skip, entry, `re-approved`, `operator_reset`) and warning lines. | `test_reasons_pin_59_names__ac14_fr020_nfr006` (214), `test_reason_table_kind_and_exit__ac14_fr020_nfr006` (223), `test_line_note_name_is_not_a_reason__ac14_fr020_nfr006` (246), `test_host_and_login_take_any_printable_bounded_token__ac14_fr020_nfr006` (449), `test_append_makes_one_os_write__ac14_fr020_nfr006` (524), `test_rotation_shifts_every_file_at_5_mib__ac14_fr020_nfr006` (559), `test_rotation_keeps_exactly_four_rotated_files__ac14_fr020_nfr006` (580), `test_exit_75_path_appends_without_rotating__ac14_fr020_nfr006` (662), `test_stderr_fallback_emits_only_five_keys__ac14_fr020_nfr006` (674) |
| `tests/issue_watch/test_marker_contract.py` | 53 | 3 | DF-21/DF-46: `predicates.CLAIM_MARKER` literal is present in both required `src/` copies (`skills/sc-issue-protocol/refs/claim.md` and `templates/claim-comment.md`) and in the project `.claude/` and `~/.claude` copies when they exist (test_marker_contract.py:28-39); the claim-comment template's last non-blank line is the marker (42-48); `github.MARKER_JQ` embeds `CLAIM_MARKER` (51-53). | `test_marker_in_every_existing_copy__fr009` (28), `test_template_last_line_is_marker__fr009` (42), `test_marker_jq_is_built_from_claim_marker__fr009` (51) |
| `tests/issue_watch/conftest.py` | 1155 | 0 (fixtures only) | Shared fakes and fixtures, no assertions: `FakeClock` (51), `FakeRunner` (74) + `fake_runner` fixture (109), `CrashingStore` with crash points `CRASH_POINTS = (None, "C1", "C3", "C4", "C5")` (126-129), `FailingStore` (188), `tmp_state` fixture (243-244), `FakeLauncher` (251), constants `OWN_LOGIN = "owner-login"`, `OWN_ID = 1001`, `PROJECT_ID`, `ORIGIN_URL` (309-315), `make_config` (342; builds an ENABLED config), `make_deps` (393), `GhWorld` scripted GitHub replies (528) + `gh_world` fixture (922-923), `STUB_TOOLS = ("gh", "orca", "orca-ide", "git")` and `stub_path` fixture (968, 1108-1109). | n/a |

**Key Takeaways**
- The reason table, the exit precedence, the 32+3 budget split, the S1 halt, the dry-run isolation and the rotation size are all pinned by name in these files.
- No test pins `MAX_LAUNCHES_PER_CYCLE`; `test_s1_case_b` pins the behaviour it was meant to name.
- `make_config` hard-codes `enabled: True` (conftest.py:352), so every cycle test runs with the gate open; the `enabled: false` path is pinned only by `test_cycle.py:1607` and `:1623`.

## 12. Deliverable (b): live-versus-off status for every piece in this area

Status words: BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED. "Live" here means reachable code that runs when a cycle is invoked; the snapshot has no invoker (item 12 below).

| # | Piece | Status | Evidence that decides it |
|---|---|---|---|
| 1 | Real poll cycle `run_cycle(deps, dry_run=False)` end to end (`_Cycle`, cycle.py:541-1211) | BUILT-OFF (enabled:false) | `enabled = raw.get("enabled", False)` (cycle.py:228) and `if not deps.config.enabled and not self.dry_run: raise _Stop("not_enabled")` (685-686); `Glob **/issue-watch*.json` in the snapshot finds no shipped config; with no config file `load_config` raises `config_invalid` (cycle.py:206-213) |
| 2 | Dry-run cycle (`once --dry-run`) | BUILT-ON | ignores `enabled` (685); registered verb (cli.py:111-137); needs a config, an initialised store and an approvers file; writes only `audit.jsonl` and `dry-run.json` |
| 3 | Login, origin, sweep, discovery steps (cycle.py:752-808, 716-723) | BUILT-OFF (enabled:false) for a real cycle; run by a dry-run | behind the gate at 685 |
| 4 | Candidate gate chain E1-E14 and the pure predicates | BUILT-OFF (enabled:false) for a real cycle; exercised by a dry-run | wired: `approval_of` cycle.py:883, 998; `is_intended_owner` 938, 991; `unchanged_since` 949; `project_check` 958, 1015; `eligibility_order` 736; `marker_in_window` via `_hit` 858 |
| 5 | Launch step L2-L14 and re-read (cycle.py:1036-1112, 979-1016) | BUILT-OFF (enabled:false) | not reached by a dry-run (1029-1035 returns first); real cycle gated at 685 |
| 6 | One launch per cycle (`halt`) | BUILT-OFF (enabled:false) with the cycle | cycle.py:833-834, 816-817 |
| 7 | `MAX_LAUNCHES_PER_CYCLE` constant | NOT BUILT (dead) | defined at cycle.py:35, no read anywhere (Grep over snapshot excluding `.dev/` and `docs/`) |
| 8 | `enabled` config switch | BUILT-ON (the switch itself); value shipped `false` | cycle.py:228 default `False`; only read at 685 |
| 9 | `DISABLED` file kill switch | BUILT-ON | checked at cycle.py:712 and 1063; `os.path.lexists` (record.py:421-423); no `DISABLED` file ships (an operator creates it) |
| 10 | Audit writer, rotation, stderr fallback | BUILT-ON | not behind the `enabled` gate: a `not_enabled` cycle still writes a cycle line (cycle.py:691-693 -> `_conclude`) |
| 11 | Readers of `audit.jsonl` and the SLO reducer in operation | NOT BUILT | `slo_numbers` (cycle.py:1359) has no caller in `src/`; `status_report` does not read audit (cycle.py:1279-1281) |
| 12 | A trigger that runs `issue-watch once` on a schedule (cron, timer, dispatcher) | NOT BUILT | no hit for a scheduler artefact in `hooks/`, `scripts/`, `.github/`, `plugins/`, Makefile or `pyproject.toml`; the 20 files that mention `issue-watch` outside `tests/` and `.dev/` are docs, `main.py`, the package, CHANGELOG, and the agent-work-report skill (Grep, this session) |
| 13 | Live-test record `docs/designs/issue-watcher-live-test.md` (deployment gate) | NOT BUILT | `Glob docs/designs/issue-watcher*` finds only `issue-watcher.md` and `issue-watcher-setup.md`; the design says the owner writes it (issue-watcher.md:33) |
| 14 | Dispatcher, `COORD-<RepoName>` coordinator worktree, zero-setup install | not found in snapshot | `Grep 'COORD-[A-Z]|COORD-<|zero-setup|zero setup'` over `src`, `docs`, `plugins`, `scripts`, `.github` finds no such name; "grant row" occurs in `docs/designs/issue-pipeline-fu1.md:24,26`, `docs/designs/orchestrator.md:116` and `src/superclaude/core/WORKER-CONTRACT.md:57` (other agents' areas) |

## 13. Deliverable (c): writes to GitHub, and read-only `gh` calls

**No GitHub write in this area.** Evidence: (1) `Grep '"gh"'` in `P/github.py` finds exactly five literals (github.py:177, 183, 204, 231, 255), each the first element of a read argv (below); (2) `cycle.py` contains no `"gh"`, `"git"`, `"orca"` or `subprocess` literal outside comments and docstrings (Grep, this session), every command goes through `deps.runner` / `deps.launcher`; (3) `Grep 'POST|PATCH|PUT|DELETE|mutation|"edit"|"comment"|"create"|"close"'` in `github.py` finds only the comment at 107-108 and the two `--method` lines 206 and 257; (4) the REST argv carry `--method GET` (github.py:206-207, 257-258). The GraphQL calls (G5, G6) are HTTP POSTs by design but run queries only (comment github.py:107-108: "the GraphQL calls are POST and carry no --method"). The repository is the literal `IronbellyOrg/IronClaude` (github.py:37, 187, 208, 259) and the GraphQL queries hard-code `owner: "IronbellyOrg", name: "IronClaude"` (github.py:75).

Read-only `gh` calls the cycle makes (exact argv, builder line; cycle call sites):

| Id | Argv | Builder | Cycle call site |
|---|---|---|---|
| G1 | `gh api user --include` | github.py:175-177 | cycle.py:755 |
| G2 | `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --assignee <login> --json number,labels,assignees,state -L 100` | github.py:180-198 | cycle.py:796 |
| G3 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events -F per_page=100 -F page=<P> --jq <EVENTS_JQ>` | github.py:201-220 | cycle.py:907, 944, 996 (reserved) |
| G4 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/comments -F per_page=100 -F page=<P> --jq <MARKER_JQ>` | github.py:223-225 | cycle.py:905, 926, 942 |
| G5 | `gh api graphql -f query=<EDITS_QUERY> -F number=<N> [-f after=<cursor>]` | github.py:228-244 | cycle.py:948 |
| G6 | `gh api graphql -f query=<PROJECT_ITEMS_QUERY> -F number=<N> [-f after=<cursor>]` | github.py:228-249 | cycle.py:957, 1013 (reserved) |
| G7 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N> --jq <REREAD_JQ>` | github.py:252-262 | cycle.py:983 (reserved) |

Other commands the cycle starts (not GitHub): `git -C <worktree> remote get-url origin` (launch.py:244; cycle.py:721, 1074); `<orca> skills list --json` (launch.py:200; cycle.py:1048); and the one outward launch, `<orca> agent launch --agent claude --worktree path:<worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json` (12 elements, launch.py:95-116; cycle.py:1099, run with `cwd=<worktree>`, launch.py:370). The launched session, not the watcher, assigns the issue and posts the claim comment carrying the marker (out of this area).

## 14. Deliverable (d): triggers

- The cycle starts only when something runs `superclaude issue-watch once [--dry-run] [--config PATH]` (cli.py:111-137, registered in `main.py:577-579`). The group's docstring says "Run `once` from a timer" (cli.py:98).
- Intended cadence: every 5 minutes from a cron entry that is follow-up FU-2 (issue-watcher.md:15, 30); the setup runbook names the schedule `0 */5 * * * *`, six fields with seconds first (issue-watcher-setup.md:288) and says "This work does not install or enable the entry".
- No trigger found in snapshot: nothing in the package loops, sleeps or schedules, and no scheduler artefact exists (item 12 of section 12). Overlap is tolerated: a second concurrent run exits 75 `lock_held` (cycle.py:698-699).
- The design header says "no schedule is installed" (issue-watcher.md:3) and that the claim session ends after its comments and "a coordinator starts the worker" (issue-watcher.md:29, 818). The snapshot code of this area has no coordinator hook; that claim is outside this area and is [UNVERIFIED] here.

## 15. Deliverable (e): state stores

| Path pattern | Writer | Readers | Format and mode |
|---|---|---|---|
| `~/.config/superclaude/issue-watch.json` (or `--config`) | the operator; no code writes it | `cycle.load_config` (cycle.py:195-283) | JSON object; unknown top-level keys rejected (`_TOP_KEYS`, cycle.py:58-69); no shipped copy |
| approvers file (`config.approvers_file`) | the operator | `validate_approvers` every cycle (cycle.py:688, 298-361) | one decimal id per line, `#` comments; must be a regular file owned by the euid and not group/other-writable |
| `<state_dir>/dispatch.json` | `FileStore.save` (record.py:370-378) called from `_save` (cycle.py:601), the migrated-store save (747), the commit (1143) | `FileStore.load` (cycle.py:742), `status`, `reset` | JSON, sorted keys, indent 2, atomic write, mode 0600, directory fsync |
| `<state_dir>/lock` | nobody (created by `init-state`) | `FileStore.lock` (cycle.py:695) | `flock` LOCK_EX/LOCK_NB, `O_NOFOLLOW`, must be a regular file owned by the euid |
| `<state_dir>/DISABLED` | the operator | `store.disabled()` (cycle.py:712, 1063) | existence only (`os.path.lexists`) |
| `<state_dir>/audit.jsonl`, `.1`-`.4` | `AuditLog.append` from `_conclude` (cycle.py:1200) and `cli._write_reset` | none in code (section 7.4) | one sorted-key ASCII JSON object per line, mode 0600, rotated at 5 MiB |
| `<state_dir>/dry-run.json` | `record.save_dry_run` (cycle.py:1159), dry-run only | `record.load_dry_run` (cycle.py:727), dry-run only | JSON `{schema_version, considered, shadow_launches}`, mode 0600 |
| stderr | `audit.stderr_fallback` | the scheduler's log capture | one five-key JSON line |
Default `state_dir`: `$XDG_STATE_HOME` (when set and non-empty) else `~/.local/state`, plus `superclaude/issue-watch` (cycle.py:187-192); a network filesystem is refused (cycle.py:270-272); an unreadable `/proc/self/mountinfo` skips that check.

## 16. Deliverable (f): gates (every approval, refusal, kill switch, cap, budget and guard point)

| # | Gate | Exact condition | Word | Exit | Where |
|---|---|---|---|---|---|
| 1 | `enabled` switch | `not config.enabled and not dry_run` | `not_enabled` | 0 | cycle.py:685-686 |
| 2 | Platform | `sys.platform != "linux"` | `platform_unsupported` | 2 | cycle.py:286-291 (cli.py:88) |
| 3 | Config valid | file missing/non-JSON/unknown key/bad value/relative path/network FS | `config_invalid` | 2 | cycle.py:195-283 (cli.py:77-81) |
| 4 | Worktree | `not os.path.isdir(config.worktree)` | `worktree_invalid` | 2 | cycle.py:373-376 |
| 5 | Approvers file | not regular, symlink, wrong owner, group/other-writable, > 1 MiB, bad line, no ids | `approvers_invalid` | 2 | cycle.py:298-361 |
| 6 | Single instance | `flock` busy, or lock inode replaced | `lock_held` | 75 | record.py:403-414; cycle.py:698-699 |
| 7 | Lock file sanity | missing / symlink / directory / not regular / not euid-owned | `lock_missing`, `lock_invalid` | 6 | record.py:393-401 |
| 8 | Kill switch (start) | `DISABLED` exists | `disabled` | 0 | cycle.py:712-713 |
| 9 | Store | missing, unparseable, invalid | `store_missing`, `store_invalid` | 6 | record.py:347-368; cycle.py:743-744 |
| 10 | Rate-limit backoff | `now < next_permitted_at` | `rate_limited` | 5 | cycle.py:748-750 |
| 11 | Own login | G1 regex `[A-Za-z0-9][A-Za-z0-9-]{0,38}` fails | `login_invalid` | 3 | cycle.py:487, 764-765 |
| 12 | Account pin | `owner_account_id` set and not equal to the G1 id | `account_id_mismatch` | 2 | cycle.py:768-769 |
| 13 | Deadline floor | fewer than 5 s left before a call (240 s total) | `gh_timeout` (shared calls and the start-of-cycle origin check), `budget_exhausted` (per-issue reads and launch-step calls) | 3 / 0 | cycle.py:418-427, 716-720, 1036-1073 |
| 14 | Origin | `git -C <worktree> remote get-url origin` not `ironbellyorg/ironclaude` (lower-cased) or git failed | `origin_mismatch` | 2 | cycle.py:721-722 (start), 1074-1075 (before launch) |
| 15 | Discovery bound | `>= 100` results; repeated number | `truncated`, `discovery_duplicate` | 4 | github.py:823-830 |
| 16 | Candidate cap | `[:MAX_CANDIDATES]` (10) | (none; remaining issues wait) | 0 | cycle.py:736 |
| 17 | Entry-state guard (at-most-once) | state `claimed`, `pending`, or (`launched`, `unknown`, `abandoned`) without a fresh own marker | `already_dispatched` | 0 | cycle.py:919-933 |
| 18 | Backoff | `failed` entry before `updated_at + 10 min` | `in_backoff` | 0 | cycle.py:934-935 |
| 19 | Day cap | `>= 6` launches in `(now - 24 h, now]` (entries + `consumed_log`, + shadow in dry-run); tested twice | `day_cap` | 0 | cycle.py:867-876, 936-937, 1061-1062 |
| 20 | Intended owner | assignee set != {own login} | `unassigned`, `assigned_other` | 0 | predicates.py:162-174; cycle.py:938-940, 991-993 |
| 21 | Per-issue read budget | non-reserved calls reach 32, or the deadline floor | `budget_exhausted` (not stamped) | 0 | github.py:448-454, 574 |
| 22 | Approval | 7 rules of section 6.2 | `not_approved`, `approval_before_trigger`, `approval_before_init`, `events_incomplete` | 0 | predicates.py:185-234 |
| 23 | Unchanged since approval | any edit/comment/rename time `>= approved_at` | `edited_after_approval` | 0 | predicates.py:237-259 |
| 24 | Project | exactly one live item in `project_id` with Status `Backlog` | `project_mismatch` | 0 | predicates.py:262-271 |
| 25 | Unreadable evidence | G3/G4/G5/G6 failure | `events_unreadable`, `events_incomplete`, `marker_unreadable`, `edits_unreadable`, `project_unreadable` | 0 | github.py:860-861, 880-881, 898, 928 |
| 26 | Missing token scope | `scope_missing` on any per-issue read | `project_read_failed` | 3 | cycle.py:842-843, 971-972 |
| 27 | GitHub rate limit | `rate_limited` on a per-issue read or G2 (no header) | `rate_limit_clamped` (+3600 s in `next_permitted_at`) | 5 | cycle.py:663-668 |
| 28 | Orca present | no `orca-ide`/`orca` whose `skills list --json` lists `orca-cli` | `orca_not_found` | 2 | cycle.py:1048-1052 |
| 29 | Re-read (FR-011) | not open, a label gone, assignee changed, approval voided or replaced, project moved, or a re-read refused/failed | `revalidation_failed`, `unassigned`, `assigned_other`, `budget_exhausted`; timeout/5xx -> `revalidation_transient` | 0 / 7 | cycle.py:979-1016, 1057-1060 |
| 30 | Kill switch (before launch) | `DISABLED` exists after the re-read | `disabled_mid_cycle` | 0 | cycle.py:1063-1064 |
| 31 | Launch cut-off | `elapsed > 120 s` (checked before the git call, after it and after the pending save) | `budget_exhausted` | 0 | cycle.py:429-431, 1069-1079, 1095-1098 |
| 32 | Write-ahead | `pending` with `launches = 1` saved and fsynced BEFORE `orca agent launch` | (state `pending`) | 6 if the save fails (`state_dir_unwritable`) | cycle.py:1082-1092 |
| 33 | One launch per cycle | `c.launching` then `halt` | (no word; later candidates silent) | 0 | cycle.py:833-834 |
| 34 | Launch outcome | `unknown` / `spawn_error` | `launch_unknown`, `spawn_error` | 7 | cycle.py:1106-1112 |
| 35 | Fail attempts | third `prompt_invalid`/`revalidation_transient` | `attempts_exhausted` (entry), condition exit 7 | 7 | record.py:503-525; cycle.py:1018-1024 |
| 36 | Commit write | store or `dry-run.json` save fails | `state_dir_unwritable` | 6 | cycle.py:1125-1126 |
| 37 | Operator forfeit (CLI) | `reset N --forfeit-guarantee` on `abandoned`/`unknown` only; else `reset_refused` | `operator_reset`, `reset_refused` | 0 / 2 | cli.py:232-252 (agent 03) |

Approvals: the only approval in this area is the human approval label event (gate 22), judged against the approvers file. There is no second approval step in the cycle.

## 17. Documentation checks for `docs/designs/issue-watcher.md` sections 6, 7, 8 (with 4.3, 10.1 and 14 where they state this area's numbers)

| # | Doc claim (line) | Tag | Evidence |
|---|---|---|---|
| 1 | 6.2 step order 1-15 (issue-watcher.md:349-365) | [CODE-VERIFIED] | cycle.py:682-737, 1116-1211; section 2 above |
| 2 | 6.1 diagram and 6.2 step 12 / 8.4: `find_orca() (cached)` "Cache: per cycle, in the OrcaLauncher instance" (issue-watcher.md:331, 362, 621) | [CODE-CONTRADICTED] | launch.py:6 "caches nothing", 177 "The result is not cached here"; `OrcaLauncher` holds only `_runner` (launch.py:352-356). In practice `find_orca` runs once per cycle because the launch step halts the cycle |
| 3 | 6.2 step 10 "Per candidate, local checks ... Calls 0" (issue-watcher.md:360) | [CODE-CONTRADICTED] in part | `launched`/`unknown`/`abandoned` entries read G4, and tombstones and `failed`-in-backoff entries read G4 and G3, before they skip as `already_dispatched`/`in_backoff` (cycle.py:922-935). Only `claimed`/`pending` and `day_cap` are zero-call |
| 4 | 6.2 step 11 order marker, events, edits, items; `budget_exhausted` at 32 (issue-watcher.md:361) | [CODE-VERIFIED] | cycle.py:941-957; github.py:450-451 |
| 5 | 6.2 step 13/14 `considered` stamps except `budget_exhausted`; health stamp only for exit 0 with no stop (issue-watcher.md:363-364) | [CODE-VERIFIED] | cycle.py:831-832, 1134-1140; record.py:738-745 |
| 6 | 6.2 dry-run differences (issue-watcher.md:369) | [CODE-VERIFIED] | section 9 |
| 7 | 6.3 limits: `max_launches_per_cycle` 1; day cap 6/24 h; 32 + 3 reserved; 37 worst case; k = 8 (issue-watcher.md:380-391) | [CODE-VERIFIED] as behaviour | halt at cycle.py:833; test_cycle.py:3729, 4445-4489. The named constant is dead |
| 8 | 6.3 "after any launch-step outcome, later candidates are neither read nor stamped; a candidate skipped locally is stamped" (issue-watcher.md:393) | [CODE-VERIFIED] | cycle.py:816-834 |
| 9 | 4.3 "combinations that can occur are 7 with 5 ... and 7 with 3" (issue-watcher.md:173) | [CODE-CONTRADICTED] as traced | S1 halt stops reads after a `failed`/`unknown`/`spawn_error` outcome (cycle.py:833-834); only 7 with 6 can occur. `resolve_exit` itself handles them: test_cycle.py:1005, 1009 |
| 10 | 4.3 table: every reason-to-exit mapping (issue-watcher.md:161-171) | [CODE-VERIFIED] | audit.py:26-102 |
| 11 | 7.1 `audit.jsonl` "Written by every exit of `once` and `reset`" (issue-watcher.md:406) | [CODE-CONTRADICTED] in part | no audit line for config/platform failure (cli.py:79-81), unexpected exception (127), `state_dir_unwritable` (cycle.py:1195-1196), reset usage errors (cli.py:219) |
| 12 | 7.1 `audit.jsonl` "Read by `status`, the SLO reducer" (issue-watcher.md:406) | [CODE-CONTRADICTED] | cycle.py:1279-1281 (`audit` not read); `slo_numbers` has no caller in `src/` |
| 13 | 7.2-7.4 states and transitions T-1..T-13 as driven by the cycle | [CODE-VERIFIED] (cycle side) | section 3.1; record functions record.py:503-745 |
| 14 | 7.3 "unknown leaves only via claimed or reset (never on the lease)" (issue-watcher.md:478) | [CODE-VERIFIED] | record.py:638-643 (sweep only touches `pending` and `launched`) |
| 15 | 7.5 lease 60 min, backoff 10 min, day cap 6/24 h half-open, marker window 300 s, skew warning > 60 s (issue-watcher.md:503-510) | [CODE-VERIFIED] | record.py:437-443, 699-703; predicates.py:17, 295; cycle.py:44, 774 |
| 16 | 7.6 write order C1-C5 (issue-watcher.md:530-540) | [CODE-VERIFIED] for the cycle side | `_save()` (cycle.py:1092) before `launcher.launch` (1099); outcome saved by `_commit_store` (1143) after the loop; tests `test_a_failed_outcome_save_after_the_launch_never_relaunches__fr010_nfr005_c6` (4737) |
| 17 | 8.1 argv table G1-G7 and "every REST path call carries --method GET" (issue-watcher.md:548-561) | [CODE-VERIFIED] | github.py:175-262 |
| 18 | 8.2 paging and classification (issue-watcher.md:571-597) | [CODE-VERIFIED] for paging and reason mapping; stderr signs [UNVERIFIED] | github.py:592-702; `GH_ERROR_SIGNS` assumed (github.py:267-277 per the source marker `[UNVERIFIED]`) |
| 19 | 8.3 rate-limit time (issue-watcher.md:603-609) | [CODE-VERIFIED] | github.py:425-431; cycle.py:663-668; test_cycle.py:1996 |
| 20 | 8.4 launch argv 12 elements (issue-watcher.md:625-630) | [CODE-VERIFIED] | launch.py:95-116 |
| 21 | 8.5 timeouts and cut-off (issue-watcher.md:649-654) | [CODE-VERIFIED] | cycle.py:34-47, 418-431, 1036-1079 |
| 22 | 14 "skew tolerance 300 s, equals the cadence" (issue-watcher.md:827) | [CODE-VERIFIED] against `predicates.SKEW_TOLERANCE_S = 300` (predicates.py:17), the claim-marker window; ambiguous label, because the clock-skew WARNING threshold is `SKEW_WARN_S = 60` (cycle.py:44; the doc's own 7.5, issue-watcher.md:510, says 60). The scope hint that this row is wrong is only half right: the number 300 is real, but it is not the warning threshold |
| 23 | 14 `max_launches_per_cycle` 1 (issue-watcher.md:819) | [CODE-VERIFIED] behaviour; dead constant | cycle.py:35 only |
| 24 | 10.1 `clock_skew_s` "yes" on the cycle line (issue-watcher.md:722) | [CODE-CONTRADICTED] minor | optional key (audit.py:165); omitted when the `Date` header is absent or unparseable (cycle.py:770-773) |
| 25 | 10.1 59 reason names, REASON_TABLE, rotation 5 MiB/.1-.4, exit-75 path never rotates (issue-watcher.md:716, 725-727) | [CODE-VERIFIED] | audit.py:26-104, 106-107, 141-156; cycle.py:1197 |
| 26 | 1: "starts one ordinary top-level agent session ... with the prompt `/sc:issue --claim <N>`" (issue-watcher.md:15) | [CODE-CONTRADICTED] | launch.py:33, 92: the prompt is `/sc:issue --claim <N> --pipeline none` |
| 27 | Status line: "Implemented and merged in PRs #447 and #448; never run live" (issue-watcher.md:3) | [UNVERIFIED] | the snapshot has no history or runtime state; "no schedule is installed" is [CODE-VERIFIED] by absence |

## Gaps and Questions

CODE-CONTRADICTED (the doc says X, the code says Y; details in section 17):
1. [CODE-CONTRADICTED] `find_orca` is "cached per cycle in the OrcaLauncher instance" (issue-watcher.md:331, 362, 621); code: `find_orca` "caches nothing" (launch.py:6, 177), `OrcaLauncher` holds only the runner (launch.py:352-356). One call per cycle in practice only because the launch step halts the cycle.
2. [CODE-CONTRADICTED] Step 10 "local checks ... Calls 0" (issue-watcher.md:360): entries in `launched`/`unknown`/`abandoned` read G4, tombstones and `failed`-in-backoff entries read G4 and G3 first (cycle.py:922-935).
3. [CODE-CONTRADICTED] Exit 7 can combine with 5 or with 3 (issue-watcher.md:173): not reachable through `_Cycle` because of the S1 halt (cycle.py:833-834); only 7 with 6 is reachable. `resolve_exit` itself accepts any set (cycle.py:466-477).
4. [CODE-CONTRADICTED] `audit.jsonl` "Written by every exit of `once` and `reset`" and "Read by `status`, the SLO reducer" (issue-watcher.md:406): several exits write only a stderr line (cli.py:79-81, 127, 219; cycle.py:1195-1196) and nothing in `src/` reads the file (cycle.py:1279-1281; `slo_numbers` has no caller).
5. [CODE-CONTRADICTED] `clock_skew_s` "yes" on the cycle line (issue-watcher.md:722): it is optional (audit.py:165) and absent when the `Date` header is missing or unparseable (cycle.py:770-773).
6. [CODE-CONTRADICTED] Launch prompt `/sc:issue --claim <N>` (issue-watcher.md:15): code builds `/sc:issue --claim <N> --pipeline none` (launch.py:33, 92).
7. [CODE-CONTRADICTED, refined from the scope hint] The scope hint said issue-watcher.md:827 "skew tolerance 300 s" contradicts `SKEW_WARN_S = 60`. Read in code: 300 is `predicates.SKEW_TOLERANCE_S` (predicates.py:17, the marker window), a real value; the clock-skew warning is 60 s (cycle.py:44, 774) and the doc's own 7.5 says 60 (issue-watcher.md:510). The doc row's label is ambiguous, not wrong in number.
8. [CODE-CONTRADICTED] cross-consumer: `agent-work-report` reads the key `orchestrator_repo` from `~/.config/superclaude/issue-watch.json` (src/superclaude/skills/agent-work-report/scripts/common.py:22-40), but `load_config` rejects any key outside `_TOP_KEYS` (cycle.py:58-69, 216-220), and `orchestrator_repo` is not in that set; a config holding that key makes `issue-watch once` exit 2 `config_invalid`.

UNVERIFIED:
9. [UNVERIFIED] "Implemented and merged in PRs #447 and #448; never run live" (issue-watcher.md:3): the snapshot has no git history and no runtime state. That `enabled` ships false and that no schedule is installed ARE [CODE-VERIFIED] (cycle.py:228; no scheduler artefact).
10. [UNVERIFIED] gh stderr phrases and GraphQL error type names (`GH_ERROR_SIGNS`, github.py:267-278, marked `[UNVERIFIED]` in source) and the reply shapes behind them. They decide whether a failure becomes `gh_auth_failed`, `rate_limited`, `project_read_failed` or `gh_non_json`, so the reason a live failure produces is unverified. No live-test record exists in the snapshot (section 12 item 13).
11. [UNVERIFIED] The Orca launch reply path for the operation id (`OPERATION_ID_PATHS`, launch.py:39-45, marked `[PROPOSAL, UNVERIFIED]`); it decides `launched` versus `unknown` (agent 02's area).
12. [UNVERIFIED] Whether anything outside the snapshot (a Coder cron, a dispatcher, a coordinator) runs `issue-watch once`. The snapshot has no such artefact; "dispatcher", `COORD-<RepoName>` and "zero-setup" are not found in snapshot (section 12 item 14).
13. [UNVERIFIED] "a coordinator starts the worker" after the claim (issue-watcher.md:29, 818): outside this area; the cycle's only outward effect is the Orca launch.

Open questions and observations (not doc claims):
14. Entry states `unknown` and `claim_not_observed`/`spawn_error` (`abandoned` with `pending_at`) never leave by themselves: each costs at least one G4 call on every cycle in which the issue is still discovered (cycle.py:922-931) until a marker appears or the operator resets. Whether such issues leave the discovery set (trigger label removed) is not decided by any code in this area; the watcher never edits labels. Question for the owner: is the per-cycle G4 cost for stuck entries acceptable, given examined stamps push them behind new issues (predicates.py:299-312)?
15. `claimed` is terminal and `reset` refuses it (`_RESETTABLE = {"abandoned","unknown"}`, record.py:448), so a claimed issue can never be dispatched again by the watcher. Documented (issue-watcher.md:478), noted here for the reference.
16. The edit check (E12) runs once, before the re-read; the re-read re-verifies state, labels, assignees, approval event id and project, not edits (cycle.py:1006; design FR-011 set at issue-watcher.md:333, 556-557). A body edit made between the G5 read and the launch is not seen. This follows the design's re-read set; no design sentence discusses the window.
17. Test depth: the test files were read selectively (full read of test_marker_contract.py, test_cycle.py 3715-3792 and 4435-4490, conftest 340-370; names and module docstrings for the rest). Counts do not expand parametrisation.

## Stale Documentation Found

- **[STALE DOC]** docs/designs/issue-watcher.md:331, 362, 621: `find_orca` "cached" (code: not cached).
- **[STALE DOC]** docs/designs/issue-watcher.md:360: step 10 "Calls 0" (code: entry-state candidates read G4/G3).
- **[STALE DOC]** docs/designs/issue-watcher.md:173: exit 7 combinations with 5 and 3 (unreachable through the cycle).
- **[STALE DOC]** docs/designs/issue-watcher.md:406: audit.jsonl "Written by every exit" and "Read by status, the SLO reducer".
- **[STALE DOC]** docs/designs/issue-watcher.md:722: `clock_skew_s` "yes" (optional in code).
- **[STALE DOC]** docs/designs/issue-watcher.md:15: prompt without `--pipeline none`.
- **[STALE DOC]** docs/designs/issue-watcher.md:827: "skew tolerance 300 s" is the claim-marker window (predicates.py:17); the label reads like the 60 s warning threshold of 7.5 (line 510). Ambiguous.
- **[STALE DOC]** docs/designs/issue-watcher.md:819 and 380: `max_launches_per_cycle` as a default value; behaviour exists (halt), the named constant is dead (cycle.py:35).
- **[STALE DOC]** docs/designs/issue-watcher.md:3: PR numbers and "never run live" cannot be checked from the snapshot.
- Not stale (checked): sections 6.2 steps 1-9 and 11-15, 7.2-7.5, 8.1, 8.3, 8.4 argv, 8.5, 4.3 mapping, 10.1 reason count and rotation, 14 defaults other than the rows above.

## Defect Candidates and Not-Built Capabilities

No remediation tasks were created and nothing was written outside the task folder; the owner decides. Each row gives the capability, the declaring doc line, and the code evidence.

| # | Class | Capability | Declaring doc | Code evidence | Recorded decision that it is out of scope (path:line), if any |
|---|---|---|---|---|---|
| DC-1 | DEFECT CANDIDATE (dead constant) | `max_launches_per_cycle` = 1 as a named default | docs/designs/issue-watcher.md:380, 819 | `MAX_LAUNCHES_PER_CYCLE = 1` at `src/superclaude/cli/issue_watch/cycle.py:35`; Grep over the snapshot excluding `.dev/` and `docs/` finds no other occurrence, none in `tests/`. The one-launch limit works through `_Cand.launching` + `self.halt` (cycle.py:1028, 833-834) | none found |
| DC-2 | DEFECT CANDIDATE (declared reader missing) | `status` reads `audit.jsonl` | docs/designs/issue-watcher.md:406 | `status_report` takes `audit` but "is accepted for the fixed signature and not read" (cycle.py:1279-1281); Grep `audit.jsonl|AuditLog` over `src/**/*.py` finds only writers, the `status` constructor call (cli.py:173) and the unread parameter | none found |
| DC-3 | NOT BUILT (as an operator-visible report) | The SLO reducer that yields the four NFR-013 numbers (p95 approval-to-launch, exit-0 share over 7 days, claimed share, stale count) | docs/designs/issue-watcher.md:750-752 | `slo_numbers` (cycle.py:1359) and `SloNumbers` (1339) have no caller in `src/` (Grep, zero hits outside the definition); only `tests/issue_watch/test_slo_helper.py` calls it | issue-watcher.md:752: "It is a library function with a fixture test, not a verb (no verb was specified)": that records "no verb", not "no caller"; no other consumer is named |
| DC-4 | NOT BUILT | A scheduled trigger for `issue-watch once` (cron every 5 min) | docs/designs/issue-watcher.md:15, 30; docs/designs/issue-watcher-setup.md:286-290 | no scheduler artefact in the snapshot (section 12 item 12) | issue-watcher.md:30 lists "The Coder template and its `coder_script` cron (FU-2)" in the out-of-scope column; issue-watcher-setup.md:288 "This work does not install or enable the entry" |
| DC-5 | NOT BUILT | The owner-run live-test record that gates enabling the watcher | docs/designs/issue-watcher.md:33 | `Glob docs/designs/issue-watcher*` finds only `issue-watcher.md` and `issue-watcher-setup.md` | issue-watcher.md:33 ("neither this design nor its implementation writes it") |
| DC-6 | BUILT-OFF by design | The whole real cycle (`enabled: false`) | docs/designs/issue-watcher.md:3, 33 | cycle.py:228, 685-686; no shipped config file | issue-watcher.md:33 deployment gate ("`enabled` stays `false` until an owner-run live test (FU-1) ...") |
| DC-7 | DEFECT CANDIDATE (practically unreachable path) | `prompt_invalid` entry for a bad issue number | docs/designs/issue-watcher.md:362, 170 | `launch.build_claim_prompt` raises only for a non-int or out-of-range number (launch.py:90-91) while `github.discover` already rejects those (github.py:827-828); only test_cycle.py:3348 reaches the branch (cycle.py:1054-1056) | none found (defensive code; low severity) |
| DC-8 | DEFECT CANDIDATE (cross-consumer contradiction) | The poll config file carries `orchestrator_repo` for the agent-work-report skill | src/superclaude/skills/agent-work-report/scripts/common.py:22-25 | `_TOP_KEYS` (cycle.py:58-69) lacks `orchestrator_repo`; unknown keys raise `config_invalid` (cycle.py:216-220) | none found |

## Summary

One `issue-watch once` cycle is a strict pipeline in `cycle.py`: enabled gate, setup validation, lock, DISABLED switch, store load, login (G1), origin check, sweep, discovery (G2), up to 10 ordered candidates, a single commit and one audit write; every decision is a closed-vocabulary word from the 59-entry `REASON_TABLE`, and exit codes resolve by the fixed precedence 2, 6, 7, 5, 3, 4 (75 only alone). Eligibility is decided by pure predicates (approval replay, ownership, edits, project Backlog) after at most 32 per-issue GitHub reads, with 3 more reserved for the pre-launch re-read (37 calls worst case, 2 idle); the watcher itself writes nothing to GitHub, and its only outward effect is one `orca agent launch` after a durable `pending` record. The real cycle ships switched off (`enabled` defaults to false, no config or scheduler exists in the snapshot), the dry-run path is the only live-capable mode and stops before the launch step, the `DISABLED` file is a second kill switch, and `MAX_LAUNCHES_PER_CYCLE` is a dead constant whose job is done by the S1 halt. Eight defect or not-built candidates and several stale design-doc statements (find_orca cache, exit-7 combinations, audit readers, the launch prompt, the 300 s versus 60 s skew wording) are listed for the owner to decide.

## Gap-fill c1 B-1 (ERRATUM, supersedes the earlier wording)

Supersedes the first bullet of the section 1 "Key Takeaways" (line 34: "13 constants at lines 34-47; 12 are read ..."). That bullet miscounted. The section 1 table (lines 12-27) already had the right rows. Every line number below was re-read from the live snapshot file `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/issue_watch/cycle.py` in this session (`P` = `src/superclaude/cli/issue_watch/`).

**Corrected statement.** `P/cycle.py` lines 34-47 hold **14** constant assignments (34 `MAX_CANDIDATES` through 47 `DISCOVERY_WARN`; the comment on line 33 is "Design section 14 defaults. They are module constants, not operator knobs."). **13** of the 14 are read by production code. Two of those 13 are read only by the status report, not by the poll cycle: `HEALTH_AGE_S` (read at cycle.py:1327, `"healthy": age is not None and age <= HEALTH_AGE_S`, inside `status_report`, def at 1270) and `STALE_AGE_S` (read at cycle.py:1259 inside `_is_stale`, def at 1251; `_is_stale` is called from `status_report` at 1299 and 1405). **One** is dead: `MAX_LAUNCHES_PER_CYCLE` (defined at cycle.py:35, read nowhere). [CODE-VERIFIED]

**Evidence per constant** (Grep `-w <NAME>` over `src/` and `tests/` `*.py`, excluding the definition lines 34-47):

| # | Constant | Line | Production read (besides definition) | Tests |
|---|---|---|---|---|
| 1 | `MAX_CANDIDATES` | 34 | cycle.py:736 | test_cycle.py:1794 (comment only) |
| 2 | `MAX_LAUNCHES_PER_CYCLE` | 35 | NONE | NONE |
| 3 | `DAY_CAP` | 36 | cycle.py:876 | none |
| 4 | `GH_TIMEOUT_S` | 37 | cycle.py:578, 582 | none |
| 5 | `PROBE_TIMEOUT_S` | 38 | cycle.py:1036, 1044 | none |
| 6 | `GIT_TIMEOUT_S` | 39 | cycle.py:716, 1071 | none |
| 7 | `LAUNCH_TIMEOUT_S` | 40 | cycle.py:1099 | none |
| 8 | `DEADLINE_TOTAL_S` | 41 | cycle.py:405 | test_cycle.py:1093 pins 240.0 |
| 9 | `GH_FLOOR_S` | 42 | cycle.py:425 (docstring 421) | test_cycle.py:1094 pins 5.0 |
| 10 | `LAUNCH_CUTOFF_S` | 43 | cycle.py:431 (docstring 430) | test_cycle.py:1095 pins 120.0; 4555 monkeypatches |
| 11 | `SKEW_WARN_S` | 44 | cycle.py:774 | none |
| 12 | `HEALTH_AGE_S` | 45 | cycle.py:1327 (status report only) | none |
| 13 | `STALE_AGE_S` | 46 | cycle.py:1259 (status report only) | none |
| 14 | `DISCOVERY_WARN` | 47 | cycle.py:806 | none |

Count check: 14 rows; 13 with a production read (11 read by the cycle itself plus the two status-report-only reads); 1 with none. [CODE-VERIFIED]

**Dead-constant evidence.** A case-insensitive search for `max_launches_per_cycle` over the whole snapshot excluding `.git`, `.dev` and `docs` finds exactly one hit, the definition at cycle.py:35. No hit in `src/` other than the definition, none in `tests/`. [CODE-VERIFIED]

**Declaring doc (staleness check).** `docs/designs/issue-watcher.md:380` ("`max_launches_per_cycle` 1; day cap 6 per rolling 24 h") and `docs/designs/issue-watcher.md:819` ("`max_launches_per_cycle` | 1 | caps blast radius of a bad cycle") name it as a default that caps launches. The code does not read it. The one-launch limit is in fact enforced by `_Cand.launching` and `self.halt` (see section 1, "What enforces the one-launch-per-cycle limit instead"). Classification: **DEFECT CANDIDATE (dead constant)**, already recorded as DC-1 in the declared-but-unbuilt table of this file; no cited decision file records it as out of scope. No remediation task created. [CODE-VERIFIED]

Gap-fill c1 B-1 complete
