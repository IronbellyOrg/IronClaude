## T1 card excerpt

Persona: analyzer. You audit the spec-to-plan deviation and contradiction surface: do the plan's tasks and ACs implement every clause of the decision tables and fold rules, and do any two plan clauses contradict each other or the spec?

Attribution note: this package already executed (landed in commit 0b8a5801d, parent 0e486ab8d). The spec's facts F1-F13 were
re-read at the parent commit 0e486ab8d and hold there (EventType 43 members, `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`,
`CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`, `BRANCH_*` constants, fsm.py has 1246 lines so the 900-943 cite is valid). HEAD
now carries the implementation, so a citation of HEAD text as a plan defect or as a gap must be checked against 0e486ab8d.


## Candidate gaps (hypotheses for the reviewers; none is final)

1. Task 11 acceptance criteria assert that twelve test NAMES exist, a trace order, and forbidden calls, but not the behaviour
   of most listed scenarios (foreign toggle continues the run, engage failure halts before any edit; the merged-PR case does carry a behaviour AC about push events). A test
   with the right name and an empty body would satisfy the name AC.
2. Spec 4.6 says the guard, the push triad and `rereview_requested` of one cycle share one `cycle_id`. No AC asserts the
   shared id; Task 8 AC says only that the ref names the minting place.
3. Task 8 text says "no `file:NNN` pointer" and spec section 10 requires it; no AC checks it (constraint without AC).
4. Task 2 AC3 says `grep 43 ...` "shows no remaining claim that the enum has 43 members"; models.py keeps the comment "the
   42nd-43rd", so the grep output is never empty and the AC is a judgment call.
5. Task 7 prose requires `gh api --paginate`; no AC feeds a multi-page timeline to the fake `gh` (spec F9, gate G2).


Treat the T1 candidate gaps as hypotheses to test against the files, not as conclusions.

Before you file an "un-AC-d", "no gate" or "cannot fail" claim, quote the acceptance-criteria or constraint text you judged against; a claim whose quoted AC does cover the point is dropped. The package already executed (see the attribution note): judge the PLAN against the spec; never cite post-execution files (merge_guard.py, refs/merge-guard.md, set-draft-state.sh, tests/pr_submit/test_merge_guard*.py) as plan defects.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

Write the heading exactly "## Findings block" (two hash signs, then the words) and open the fence with exactly three backticks followed by findings-v2 (not json). Cite repo-relative paths only (the plan is .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md, the spec is .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md); a bare "source.md" path does not resolve.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T03:04:39Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:97-172
```markdown
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

```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:173-210
```markdown
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
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:52-78
```markdown
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
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:94-102
```markdown
## Task 6: Add the `--merge-guard` flag

Depends on: Task 1

Edit `src/superclaude/pr_submit/fsm.py` following ./source.md section 4.3: `DEFAULT_MERGE_GUARD = "draft"`, a `--merge-guard` argument with `dest="merge_guard"` and `choices=["draft", "off"]` placed beside `--conflict-max-tier` in `build_arg_parser`, `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD`, and `parse_args` passing `ns.merge_guard`. Leave `RunConfig` and `run_skill` unchanged. Add a test beside `test_conflict_max_tier_default_and_bounds` in `tests/pr_submit/test_skill_parse.py`.

Acceptance criteria:
- `parse_args([]).merge_guard == "draft"`, `parse_args(["--merge-guard", "off"]).merge_guard == "off"`, `SkillArgs().merge_guard == "draft"`, and `--merge-guard label` exits with an argparse error (`SystemExit`).
- `fsm.py` still contains no whole word `gh` or `git` (the static purity test passes) and every existing test in `tests/pr_submit/test_skill_parse.py` and `tests/pr_submit/test_autonomy_gates.py` passes unchanged.
```

## Coverage slice

After the Findings block also add one line "coverage_rows_checked: INF-001, INF-002, ..." listing the Coverage slice rows you actually verified. An empty Findings block is allowed only if you checked every assigned row and found no defect.

| Requirement (inferred row) | Spec citation | Match | Matched task |
|---|---|---|---|
| INF-001: engage at the first verified Medium-or-higher finding routed to a fix | source.md:6 | containment | Task 8 |
| INF-002: release when the fix push is confirmed on the PR head, before replies and the re-trigger | source.md:6 | containment | Task 8 |
| INF-003: an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | source.md:6 | containment | Task 8 |
| INF-004: No `gh` or `git` word on any line, comments included (F6). | source.md:75 | none | - |
| INF-005: Never collides with `CONFLICT_CYCLE_PREFIXES`. | source.md:101 | containment | Task 3 |
| INF-006: It is the only way resume learns that a held cycle's push completed normally (F13). | source.md:108 | containment | Task 8 |
| INF-007: A halt with reason `draft_guard_unavailable` reports `unavailable`. | source.md:112 | containment | Task 8 |
| INF-008: `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action | source.md:127 | containment | Task 4 |
| INF-009: `NOOP` (reason `mode_off`, `ordinal`, `conflict_cycle`) | source.md:133 | containment | Task 4 |
| INF-010: 43 to 45, update the docstring | source.md:175 | containment | Task 2 |
| INF-011: It is NOT `DISABLED`, so a crash before the call does not leave later cycles unguarded. | source.md:201 | none | - |
| INF-029: Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | source.md:64 | containment | Task 8 |
| INF-030: Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | source.md:65 | containment | Task 8 |
| INF-031: Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | source.md:68 | containment | Task 8 |
| INF-032: Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | source.md:66 | none | - |
