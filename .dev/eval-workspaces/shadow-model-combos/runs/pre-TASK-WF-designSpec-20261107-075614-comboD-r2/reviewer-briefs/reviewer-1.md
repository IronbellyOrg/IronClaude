# Reviewer brief 1 (analyzer)

You are reviewer 1, persona analyzer: hunt contradictions, wrong outcomes and missing cases between the design spec and the plan's tasks, especially in the decision tables, the fold and the resume logic.

Audit the plan (tasklist) against its driving spec before execution. The plan was already executed once; judge what the plan and spec say, not the state of HEAD, and do not report a post-implementation difference as a plan defect. Read-only: no edits, no shell, no git.
Full files, if you need more than the hunks: spec `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`, plan `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (Read, Grep and Glob are allowed).

## T1 card excerpt

# T1 reflection card (UC-1, pre-execution)

- spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines, design spec v3, issue #375)
- plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks, 5 phases)
- attribution note: the plan was already executed (PR #428, commit 0b8a5801d is the only commit that touches `merge_guard.py`). A defect is a plan or spec defect only if it existed at plan time; post-implementation HEAD state is evidence of what execution found, not a plan failure.

#### Coverage (Step 1B.0, deterministic script `artifacts/coverage-map.py`)

- Pass 1 (ID_REGEX `R-/REQ-/SPEC-/T-`): 0 parsed ids in the spec and 0 in the tasklist. The spec labels its requirements FR-n, F-n, G-n, O-n, which the regex does not match.
- Pass 2: 90 inferred rows, each quote-pinned to one spec line (0 dropped). Containment match (>= 0.6 of content words in one task item): 74 matched, 16 unmatched.
- `coverage_pct` null (parsed total 0). `coverage_pct_union` 0.8222. `coverage_degraded: parsed-sparse` (90 inferred > 0 parsed), which forbids a Tier-1 stop.
- `S_dev_density` = (16 + 0) / 90 = 0.1778 (mechanical, union denominator). Below 0.20, so rule 5 alone would not escalate.
- Manual read of the 16 unmatched rows: all 16 have a covering task. INF-004, 010, 013, 023, 034, 044, 045, 046, 052, 075, 081 map to Tasks 3, 4, 7, 11. INF-048, 049 map to Tasks 6 and 12. INF-078, 079, 080 are tasklist constraints with no task of their own. The unmatched count is a limit of word-overlap matching, not a plan gap.
- Method limit: tasks are 150 to 500 words each, so containment of a short quote is easy to satisfy. 16 matches fall between 0.60 and 0.75 and deserve a human look (listed in `artifacts/coverage-matrix.json`, key `thin_matches_lt_0.75`).

### Deviation / root-cause slice (analyzer lens)

- T1-F1 (MAJOR, not blocking): the guard record's `cycle_id` is never defined as updated. The fold field list names `cycle_id` (source.md:190) but no row of the effect table sets or changes it after the first request. `held_cycle_published` and resume row 4 key on it (source.md:108, 166). Engage row 7 returns `NOOP(already_held)` for any later cycle that finds the guard HELD (source.md:139), so a second cycle reusing a held draft leaves `guard.cycle_id` stale and the release or the resume check is judged against the earlier cycle's push. The plan has no acceptance criterion for it (plan:61 covers only `guard_status`; Tasks 3 and 4 list no cycle rebinding case). The shipped code added a `REBIND` action for exactly this (`src/superclaude/pr_submit/merge_guard.py:438-442`), so execution had to discover it.
- T1-F2 (MAJOR, not blocking): Task 8 narrows the spec's source sections. The spec says the protocol ref carries "sections 3 and 4.1 to 4.4" (source.md:240); the plan builds it "from ./source.md sections 3, 4.1, 4.5, 4.6 and 5" (plan:124). Sections 4.2 (event fields, `timeline_baseline`, `original_is_draft`, the `guard:<run_id>:<cycle_id>:<to>:a<k>` key), 4.3 (flag) and 4.4 (the `--read` JSON that feeds `GuardRead`) are left out, and no acceptance criterion asks the ref to state the event fields. The shipped ref does carry them, so the executor compensated.
- T1-F3 (MINOR): `guard_status` and the unavailable halt disagree. The spec says a halt with reason `draft_guard_unavailable` reports `unavailable` (source.md:112), but the read-failed and timeline-unreadable engage halts (source.md:135, 140) happen before any `requested` event, so the log has no guard record and the first-match mapping returns `released`. Plan:61 pins "no record at ordinal 3 (released)"; the engage-failure scenario test of plan:166 covers only the `--to draft` failure path.

#### Refuted candidates (not findings)

- No task grants `Bash(scripts/set-draft-state.sh *)` in the `SKILL.md` front matter: refuted, `test_allowed_tools_cover_every_program` adds `scripts/` words to a separate set and only checks the files exist.
- Import cycle `run_log` -> `merge_guard` -> `conflicts`: refuted, `fsm.py` and `conflicts.py` do not import `run_log`; Task 5 also runs a fresh-interpreter import check.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line. Write the literal heading `## Findings block` and open the fence with ```findings-v2 (not ```json). Keep each claim at or under 300 characters and each quote at or under 200. After the self-report line add `rows_verified:` followed by the assigned row ids you actually checked. Return the whole card as your final message; you are read-only, the orchestrator saves it.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T04:04:27Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:97-171

````text
Functions (all total, no I/O):

| Function | Contract |
|---|---|
| `fix_cycle_id(kind, n)` | `"fix-<n>"` for kind `fix`, `"ci-<n>"` for kind `ci`; `ValueError` otherwise or when `n < 1`. Never collides with `CONFLICT_CYCLE_PREFIXES`. |
| `next_cycle_number(events, kind)` | 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. |
| `fold_draft_guard(events)` | Section 4.2. Returns `None` when the log holds no guard record. |
| `pending_requests(events)` | Guard requests with no matching settle, matched by `idempotency_key` (the guard's own crash window; `recovery.py` stays push-only). |
| `classify_toggles(guard, read)` | `"ok"`, `"foreign"` or `"unreadable"`; rule below. |
| `engage_decision(*, mode, ordinal, cycle_id, guard, read)` | Table below. |
| `release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)` | Table below. `applied_edits` is THIS cycle's count of applied edits; it is not the run-wide `applied_edits` output field (which counts the whole run), so a zero-edit cycle after a fixing cycle still releases with `no_edits`. |
| `held_cycle_published(events, guard)` | `True` when `guard` is not `None` and the log holds a `push_completed` event whose `cycle_id` equals `guard.cycle_id`, whether written by the push triad or synthesized by recovery (`recovered: true`); `False` otherwise. The SKILL passes the result as `published`. It is the only way resume learns that a held cycle's push completed normally (F13). |
| `resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)` | Table below. `dangling_branch` is `None` or one of the module constants `BRANCH_LANDED = "landed"`, `BRANCH_NOT_LANDED = "not_landed"`, `BRANCH_AMBIGUOUS = "ambiguous"`, which equal the `recovery.py` strings (F13); a test imports both modules and asserts equality, because the core cannot import `recovery`. `published` is the output of `held_cycle_published`. |
| `guard_status(guard, mode, ordinal)` | `"off"`, `"released"`, `"held"`, `"user_override"`, `"unavailable"` for the output field `merge_guard`. |

`guard_status(guard, mode, ordinal)` maps, first match wins: `mode == OFF` or `ordinal < 3` with no guard record gives `off`; no guard record gives `released`; phase `HELD` gives `held`; phase `ENGAGE_PENDING` or `RELEASE_PENDING` gives `held` when `owned_draft` is true, else `unavailable`; phase `DISABLED` with cause `user_override` gives `user_override`; phase `DISABLED` with cause `already_draft` gives `off` (the PR was a draft before the run, nothing is guarded); phase `RELEASED` gives `released`. A halt with reason `draft_guard_unavailable` reports `unavailable`.

`classify_toggles(guard, read)` (the only foreign-toggle test; no actor identity, F11):

```text
if not read.ok or not read.complete or read.transitions is None:        -> "unreadable"
observed = read.transitions - guard.baseline
slack    = guard.unsettled + guard.failed_mutations
if observed < guard.run_toggles:                                        -> "unreadable"   # events missing
if observed > guard.run_toggles + slack:                                -> "foreign"
expected = {HELD: True, RELEASED: False}.get(guard.phase)               # pending phases accept either
if expected is not None and read.is_draft != expected:                  -> "foreign"
else                                                                    -> "ok"
```

`failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action (a retry then finds the PR already in the target state and settles `confirmed, changed: false`).

`engage_decision`, first matching row wins:

| # | Condition | Decision |
|---|---|---|
| 1 | `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | `NOOP` (reason `mode_off`, `ordinal`, `conflict_cycle`) |
| 2 | `guard.phase == DISABLED` | `NOOP(disabled)` |
| 3 | `not read.ok` | `HALT_UNAVAILABLE(read_failed)` |
| 4 | `read.state != "OPEN"` | `HALT_PR_NOT_OPEN` |
| 5 | `guard.phase == RELEASE_PENDING` and `guard.owned_draft` | `RETRY_RELEASE` (release first, then re-decide) |
| 6 | `guard.phase == RELEASE_PENDING` and not `owned_draft` | `HOLD(ownership_unproven)` |
| 7 | `guard.phase == HELD` | `NOOP(already_held)` |
| 8 | `not read.complete` or `read.transitions is None` | `HALT_UNAVAILABLE(timeline_unreadable)` |
| 9 | `guard` exists and `classify_toggles == "foreign"` | `SKIP_USER_OVERRIDE` |
| 10 | `guard is None` and `read.is_draft` | `SKIP_ALREADY_DRAFT` |
| 11 | otherwise | `ENGAGE`; `notes` carries `auto_merge_armed` when set |

`release_decision`, first matching row wins:

| # | Condition | Decision |
|---|---|---|
| 1 | `mode == OFF`, `ordinal < 3`, or conflict cycle | `NOOP` |
| 2 | `guard is None` or `guard.phase not in (HELD, RELEASE_PENDING)` | `NOOP(not_held)` |
| 3 | `not read.ok` | `HOLD(read_failed)` |
| 4 | `read.state != "OPEN"` | `HALT_PR_NOT_OPEN` |
| 5 | `classify_toggles == "unreadable"` | `HOLD(timeline_unreadable)` |
| 6 | `classify_toggles == "foreign"` | `SKIP_USER_OVERRIDE` |
| 7 | `applied_edits == 0` | `RELEASE(cause=no_edits)` |
| 8 | `push_completed` and `read.head_sha == target_sha` | `RELEASE(cause=pushed)` |
| 9 | otherwise | `HOLD(head_mismatch or push_not_completed)` |

`resume_decision`, first matching row wins:

| # | Condition | Decision |
|---|---|---|
| 1 | `guard is None` | `NOOP` |
| 2 | `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED`) | `REPORT_HELD` (no mutation; prints the clear command) |
| 3 | `pending` non-empty | `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous`: live draft state and `classify_toggles` decide; live state matching the request's direction and `observed == run_toggles + 1` settles `confirmed, changed: true, cause: resume_reconciled`; live state not matching settles `skipped, cause: not_applied`; anything else is `ambiguous` and holds. Each reason has its own test. |
| 4 | phase `HELD` and (`dangling_branch == "landed"` or `published`) | re-enter `release_decision` with `push_completed=True` (`landed` is a push recovery just completed; `published` is a push that completed normally before the crash) |
| 5 | `dangling_branch == "not_landed"` and phase `HELD` | `NOOP(held_through_redrive)` |
| 6 | `dangling_branch == "ambiguous"` | `HOLD(ambiguous_remote_tip)` |
| 7 | phase `RELEASE_PENDING` and `owned_draft` | `RETRY_RELEASE` |
| 8 | phase `RELEASE_PENDING` and not `owned_draft`, live draft | `HOLD(ownership_unproven)` |
| 9 | otherwise | `NOOP` |
````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:173-210

````text
### 4.2 Events and the folded key

Add to `EventType` in `models.py` (43 to 45, update the docstring and the `models.py:3,24` count, and the 43 text at `run_log.py:117`):

```text
DRAFT_GUARD_REQUESTED = "draft_guard_requested"   # appended and fsynced BEFORE the draft/ready call
DRAFT_GUARD_SETTLED   = "draft_guard_settled"     # appended AFTER the call, or alone for a skip
```

| Event | Fields |
|---|---|
| `draft_guard_requested` | `run_id`, `cycle_id`, `to` (`draft` or `ready`), `timeline_baseline` (int, set on the first request only), `original_is_draft` (bool, first request only), `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` (`k` = 1 + prior requests with the same cycle and direction), `timestamp` |
| `draft_guard_settled` | `run_id`, `cycle_id`, `to`, `idempotency_key`, `outcome` (`confirmed`, `failed`, `skipped`), `changed` (bool), `cause`, `original_is_draft` (carried by a skip that has no request) |

`fold_draft_guard(events)` returns `None` or this dict, and `run_log.rebuild_state()` stores it as `state["draft_guard"]` (default `None`, added to `_NEW_KEY_DEFAULTS`):

```text
phase, phase_before_request, cycle_id, original_is_draft, baseline, run_toggles,
unsettled, failed_mutations, owned_draft, disabled_cause
```

| Event | Effect |
|---|---|
| `requested(to=draft)` | `phase = ENGAGE_PENDING`; remember the key as pending; first request sets `baseline` and `original_is_draft` |
| `requested(to=ready)` | `phase = RELEASE_PENDING`; remember the key |
| `settled(draft, confirmed, changed)` | `phase = HELD`, `owned_draft = True`, `run_toggles += 1` |
| `settled(draft, failed)` | `phase = RELEASE_PENDING`, `failed_mutations += 1`, `owned_draft` unchanged |
| `settled(draft, skipped, already_draft)` | `phase = DISABLED`, `disabled_cause = already_draft`; a first skip also sets `original_is_draft` |
| `settled(any direction, skipped, not_applied)` | the pending key is cleared and the phase returns to `phase_before_request`; `owned_draft` and the toggle counters are unchanged. For a draft request that was the first guard record, the whole record is erased (the fold returns `None`, including `baseline` and `original_is_draft`), so the next request is a first request again and takes a fresh baseline and a fresh `original_is_draft`; this is safe because `not_applied` means no toggle landed. For a ready request the phase returns to `HELD` (or `RELEASE_PENDING` when a failed release preceded it), and the next `release_decision` re-checks publication before a new request is made. It is NOT `DISABLED`, so a crash before the call does not leave later cycles unguarded. |
| `settled(draft, confirmed, not changed)` | `phase = HELD`, `owned_draft = True`, no toggle (a retry that finds the PR already draft after a call that failed on the client but landed) |
| `settled(ready, confirmed, changed)` | `phase = RELEASED`, `owned_draft = False`, `run_toggles += 1` |
| `settled(ready, confirmed, not changed)` | `phase = RELEASED`, `owned_draft = False`, no toggle |
| `settled(ready, failed)` | `phase = RELEASE_PENDING`, `failed_mutations += 1` |
| `settled(any, skipped, user_override)` | `phase = DISABLED`, `owned_draft = False` |

`unsettled` is the count of remembered keys with no settle. A corrupt line still raises, as it does today. `original_is_draft` is never read from GitHub after the first record, so a resumed run cannot mistake its own draft for an original one.

The matcher `pending_requests` uses the same key pairing as `detect_crash_window`, but over the two guard event types, so push recovery and guard recovery stay independent.
````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:52-90

````text
## Task 3: Create `merge_guard.py` types, cycle ids, fold, pending matcher, published check and status mapping

Depends on: Task 2

Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6: `GuardMode`, `Direction`, `Phase`, `GuardAction`, `GuardRead`, `GuardDecision`; the string constants `BRANCH_LANDED = "landed"`, `BRANCH_NOT_LANDED = "not_landed"`, `BRANCH_AMBIGUOUS = "ambiguous"`; `fix_cycle_id(kind, n)` and `next_cycle_number(events, kind)` (never colliding with `CONFLICT_CYCLE_PREFIXES` from `src/superclaude/pr_submit/conflicts.py`); `fold_draft_guard(events)` implementing every row of the section 4.2 effect table (fields `phase, phase_before_request, cycle_id, original_is_draft, baseline, run_toggles, unsettled, failed_mutations, owned_draft, disabled_cause`; `None` when no guard record exists; `original_is_draft` taken only from the first guard record or a first skip, never from a later read); `pending_requests(events)` matching requests to settles by `idempotency_key`; `held_cycle_published(events, guard)` (true when a `push_completed` event, normal or recovered, carries the guard's `cycle_id`); `guard_status(guard, mode, ordinal)` implementing the first-match mapping of section 4.1 (`off`, `released`, `held`, `user_override`, `unavailable`). The module imports only `enum`, `dataclasses`, `re` and `is_conflict_cycle` from `.conflicts`, and contains no `gh` or `git` word on any line. Create `tests/pr_submit/test_merge_guard.py` with table tests for these functions.

Acceptance criteria:
- `fix_cycle_id("fix", 2) == "fix-2"`, `fix_cycle_id("ci", 1) == "ci-1"`, `ValueError` for kind `sync` and for `n == 0`, `is_conflict_cycle(...)` is false for both kinds; `next_cycle_number` returns 1 on an empty log and 3 after `fix-1` and `fix-2` appear in event `cycle_id` fields.
- A parametrized fold test covers every row of the section 4.2 effect table, and each of these cases fails if the row is implemented wrongly: `settled(any direction, skipped, not_applied)` clears the pending key and restores `phase_before_request` without touching `owned_draft` or the toggle counters; a draft request that was the first record followed by `not_applied` makes the fold return `None`, and a second request then sets a fresh `baseline` and `original_is_draft` (test: request, `not_applied`, request); a ready request followed by `not_applied` gives phase `HELD` with `unsettled == 0`; `settled(draft, confirmed, not changed)` gives `HELD` with `owned_draft` true and no toggle; `settled(ready, confirmed, not changed)` adds no toggle; `settled(draft, failed)` gives `RELEASE_PENDING`, increments `failed_mutations` and leaves `owned_draft` unchanged; `settled(draft, skipped, already_draft)` gives `DISABLED` with `disabled_cause == "already_draft"`; a log with no guard events returns `None`.
- A `guard_status` test covers every phase and cause of the first-match mapping, including `ENGAGE_PENDING` and `RELEASE_PENDING` with `owned_draft` true (`held`) and false (`unavailable`), `DISABLED` with `user_override` (`user_override`) and with `already_draft` (`off`), mode `OFF` and ordinal below 3 with no record (`off`), and no record at ordinal 3 (`released`).
- `pending_requests` returns exactly the requests whose key has no settle, with retries distinguished by the `:a<k>` suffix; `held_cycle_published` is true for a normal and for a recovered (`recovered: true`) `push_completed` of the guard's `cycle_id`, false for another cycle's `push_completed` and for `guard is None`; a static test asserts `merge_guard.py` has no whole word `gh` or `git`.
- A test imports `superclaude.pr_submit.recovery` and asserts `BRANCH_LANDED`, `BRANCH_NOT_LANDED` and `BRANCH_AMBIGUOUS` equal `BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED` and `BRANCH_C_AMBIGUOUS` of that module.
- `uv run pytest tests/pr_submit/test_merge_guard.py -q` passes and `uv run ruff check` and `uv run ruff format --check` are clean for both new files.

## Task 4: Add the toggle classifier and the three decision functions

Depends on: Task 3

In `src/superclaude/pr_submit/merge_guard.py` add `classify_toggles(guard, read)` (the exact rule of ./source.md section 4.1: `unreadable` for a failed, incomplete or short timeline, `foreign` when observed transitions exceed `run_toggles + unsettled + failed_mutations` or the live draft flag contradicts a `HELD` or `RELEASED` phase, `ok` otherwise), `engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows, first match wins, `notes` carries `auto_merge_armed`), `release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)` (all 9 rows; `applied_edits` is the count of edits applied in THIS cycle, not the run-wide output field) and `resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)` (all 9 rows, with the row 2 precedence, the three `RECONCILE` reasons `resume_reconciled`, `not_applied`, `ambiguous` of section 4.1, and `dangling_branch` limited to `None` or the `BRANCH_*` constants of Task 3). Extend `tests/pr_submit/test_merge_guard.py` with one parametrized case per table row, the ready-then-draft round trip, and a failed-on-client-but-landed mutation that must not classify as foreign.

Acceptance criteria:
- Each row of the three decision tables has a test that names the row number and asserts the returned `action`, `reason` and `cause`; the engage test at ordinal 2, with `mode=OFF`, and with cycle id `sync-1` and `conflict-1` all return `NOOP`.
- `classify_toggles` returns `unreadable` for `complete=False`, `transitions=None` and for observed below `run_toggles`, `foreign` for one extra transition and for a `HELD` phase with a ready PR, and `ok` when observed equals `run_toggles + failed_mutations`.
- `release_decision` called with `applied_edits=0` for a new cycle while the guard record already holds an earlier fixing cycle returns `RELEASE` with cause `no_edits`; it returns `HOLD` for a head different from `target_sha`, and `HALT_PR_NOT_OPEN` for a merged state; a guard in phase `DISABLED` (originally draft) never yields `RELEASE` or `ENGAGE`.
- `resume_decision` tests prove the precedence: ordinal 2 with phase `ENGAGE_PENDING` and a non-empty `pending` returns `REPORT_HELD` (row 2 wins over row 3); mode `OFF` at ordinal 3 with phase `HELD` returns `REPORT_HELD`; phases `RELEASED` and `DISABLED` skip row 2; ordinal 3 with `pending` non-empty returns `RECONCILE` with a distinct test for each of `resume_reconciled` (live state matches the request and observed equals `run_toggles + 1`), `not_applied` (live state does not match) and `ambiguous` (anything else, which holds).
- `resume_decision` row 4 is tested for both entries: phase `HELD` with `dangling_branch == "landed"` and phase `HELD` with `dangling_branch is None` and `published=True` each re-enter `release_decision` with `push_completed=True`; phase `HELD` with `dangling_branch is None` and `published=False` returns `NOOP` (row 9); `"not_landed"` returns `NOOP(held_through_redrive)`; `"ambiguous"` returns `HOLD(ambiguous_remote_tip)`; a test passes the real `BRANCH_A_LANDED` string of `recovery.py` and gets the row 4 result.
- `uv run pytest tests/pr_submit/test_merge_guard.py -q` passes with ruff clean.

## Task 5: Fold the guard into the run log and export the public names

Depends on: Task 3
Depends on: Task 4

Edit `src/superclaude/pr_submit/run_log.py` `rebuild_state()` so `state["draft_guard"]` is `fold_draft_guard(events)` (default `None`, documented in the method docstring beside the #305 keys), importing from `src/superclaude/pr_submit/merge_guard.py`. Add the public guard names (the enums, dataclasses, the `BRANCH_*` constants, `fix_cycle_id`, `next_cycle_number`, `fold_draft_guard`, `pending_requests`, `held_cycle_published`, `classify_toggles`, `engage_decision`, `release_decision`, `resume_decision`, `guard_status`) to the imports and `__all__` of `src/superclaude/pr_submit/__init__.py`. Update `tests/pr_submit/test_run_log.py`: add `"draft_guard": None` to `_NEW_KEY_DEFAULTS` and add a test that a legacy log rebuilds every old key unchanged with `draft_guard` `None`, and that a log with a request and a confirmed settle rebuilds `phase: held`. Add `src/superclaude/pr_submit/merge_guard.py` to `CORE_PURE_FILES` in `tests/pr_submit/test_static_grep.py`.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_idempotency.py -q` passes, including `test_tn50_core_pure_no_gh_git_tokens` over the new file and the exact key-set assertions that use `_NEW_KEY_DEFAULTS`.
- `uv run python -c "from superclaude.pr_submit import fold_draft_guard, engage_decision, release_decision, resume_decision, held_cycle_published, fix_cycle_id; import superclaude.pr_submit.run_log"` exits 0 in a fresh interpreter (no import cycle).
- Rebuilding a log that holds `requested(draft)` then `settled(draft, confirmed, changed=True)` returns `state["draft_guard"]["phase"] == "held"` with `owned_draft` true; a log that ends after only the request returns `unsettled == 1` and phase `engage_pending`.
````

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-017: No `gh` or `git` word on any line, comments included (F6). Imports only ... | - | matched Task 3 (0.769) | source.md:75 |
| INF-018: Never collides with `CONFLICT_CYCLE_PREFIXES`. | - | matched Task 3 (0.667) | source.md:101 |
| INF-019: 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. | - | matched Task 3 (0.667) | source.md:102 |
| INF-020: Guard requests with no matching settle, matched by `idempotency_key` | - | matched Task 3 (0.833) | source.md:104 |
| INF-021: `applied_edits` is THIS cycle's count of applied edits; it is not the ru... | - | matched Task 4 (1.0) | source.md:107 |
| INF-022: `True` when `guard` is not `None` and the log holds a `push_completed` e... | - | matched Task 3 (0.778) | source.md:108 |
| INF-023: a test imports both modules and asserts equality, because the core canno... | - | unmatched by containment (0.455) | source.md:109 |
| INF-024: phase `DISABLED` with cause `already_draft` gives `off` (the PR was a dr... | - | matched Task 3 (0.727) | source.md:112 |
| INF-025: A halt with reason `draft_guard_unavailable` reports `unavailable`. | - | matched Task 8 (0.8) | source.md:112 |
| INF-026: `classify_toggles(guard, read)` (the only foreign-toggle test; no actor ... | - | matched Task 4 (0.667) | source.md:114 |
| INF-027: `failed_mutations` keeps a call that failed on the client but landed on ... | - | matched Task 4 (0.6) | source.md:127 |
| INF-028: `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | - | matched Task 3 (1.0) | source.md:133 |
| INF-029: `RETRY_RELEASE` (release first, then re-decide) | - | matched Task 1 (0.6) | source.md:137 |
| INF-030: `guard` exists and `classify_toggles == "foreign"` | - | matched Task 4 (0.75) | source.md:141 |
| INF-031: `guard is None` and `read.is_draft` | - | matched Task 3 (0.75) | source.md:142 |
| INF-032: `ENGAGE`; `notes` carries `auto_merge_armed` when set | - | matched Task 4 (0.8) | source.md:143 |
| INF-033: `push_completed` and `read.head_sha == target_sha` | - | matched Task 4 (0.75) | source.md:156 |
| INF-034: `HOLD(head_mismatch or push_not_completed)` | - | unmatched by containment (0.333) | source.md:157 |
| INF-035: `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED`) | - | matched Task 3 (1.0) | source.md:164 |
| INF-036: `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `a... | - | matched Task 4 (1.0) | source.md:165 |
| INF-037: re-enter `release_decision` with `push_completed=True` | - | matched Task 4 (1.0) | source.md:166 |
| INF-038: `dangling_branch == "not_landed"` and phase `HELD` | - | matched Task 4 (1.0) | source.md:167 |
| INF-039: `HOLD(ambiguous_remote_tip)` | - | matched Task 4 (1.0) | source.md:168 |
| INF-040: Add to `EventType` in `models.py` (43 to 45, update the docstring and th... | - | matched Task 2 (0.769) | source.md:175 |
| INF-041: appended and fsynced BEFORE the draft/ready call | - | matched Task 7 (0.6) | source.md:178 |
| INF-042: `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` (`k` = 1 + pri... | - | matched Task 3 (0.667) | source.md:184 |
| INF-043: default `None`, added to `_NEW_KEY_DEFAULTS` | - | matched Task 5 (0.75) | source.md:187 |
| INF-044: It is NOT `DISABLED`, so a crash before the call does not leave later cy... | - | unmatched by containment (0.429) | source.md:201 |
| INF-045: `original_is_draft` is never read from GitHub after the first record, so... | - | unmatched by containment (0.5) | source.md:208 |
| INF-046: The matcher `pending_requests` uses the same key pairing as `detect_cras... | - | unmatched by containment (0.467) | source.md:210 |
| INF-047: `choices=["draft", "off"]` (same shape as `--conflict-max-tier`, F5) | - | matched Task 6 (0.667) | source.md:214 |

Assigned rows: INF-017, INF-018, INF-019, INF-020, INF-021, INF-022, INF-023, INF-024, INF-025, INF-026, INF-027, INF-028, INF-029, INF-030, INF-031, INF-032, INF-033, INF-034, INF-035, INF-036, INF-037, INF-038, INF-039, INF-040, INF-041, INF-042, INF-043, INF-044, INF-045, INF-046, INF-047.
