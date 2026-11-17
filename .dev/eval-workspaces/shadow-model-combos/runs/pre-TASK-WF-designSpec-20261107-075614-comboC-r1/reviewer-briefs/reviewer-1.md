# Reviewer 1 brief (persona: analyzer, model class: sonnet)

Task: Tier 2 pre-execution audit (UC-1) of a workflow plan against its driving design spec. Audit read-only: no file edits, no shell, no git.
Subject: the plan .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md (13 tasks) against the spec .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md (v3 design for the pr-submit merge guard).
Attribution: both files are an archived package. Repository HEAD has moved and already contains the shipped feature; HEAD code is not evidence about the plan. Cite ONLY the plan and the spec (role `plan` or `spec`, the repo-relative paths above). The facts you need about the repo at the spec's base commit are in the base-commit facts hunk below.
Rule: a claim you cannot tie to a plan or spec line is not a finding. Before you claim that a criterion cannot fail, quote the criterion text. Severity: CRITICAL only for a wrong outcome an implementer would ship; MAJOR for a gap a wrong implementation would pass; MINOR for wording or a nit.
Your lens: You are the analyzer reviewer. Look for logic defects in the design (decision tables, the fold, the toggle classifier, resume rules) and for plan steps that would make an implementer build the wrong behaviour. Trace a concrete input to a wrong output before you claim a defect.

## T1 card excerpt

#### Grounding performed (Read / git show at e8db2fe6)

- Import cycle risk (spec F13, plan Task 3 constraint): `conflicts.py` imports only `.fsm` and `.models`; `fsm.py` imports `.loop_guard`, `.models`, `.severity_router`; `run_log.py` imports only `.models`; only `recovery.py` imports `.run_log`. No cycle run_log -> merge_guard -> conflicts. The spec's claim holds.
- Enum-count pins (Task 2): the "43" claims sit in `models.py` (module docstring and class docstring), `run_log.py` (append docstring), `refs/loop-guard.md` (heading and "EXACTLY 43"), `test_run_log.py` (test name and two asserts) and `test_codex_reviews.py` (one assert). Task 2 names all of them.
- Allowed-tools rule (Task 8/9 worry): the SKILL front matter grants `Bash(gh *)`, `Bash(git *)`, `Bash(uv *)`, `Bash(make *)`, `Bash(jq *)`; `test_allowed_tools_cover_every_program` only checks that a `scripts/` path exists on disk. No front-matter edit is needed for the new script. Hypothesis refuted.
- Plan symbols all exist at e8db2fe6: `_NEW_KEY_DEFAULTS`, `CORE_PURE_FILES`, `_RESOLUTION_SCRIPTS`, `WRITE_VERB_CLASSIFICATION`, `test_conflict_max_tier_default_and_bounds`, `test_t105_runtime_repo_pin`, `test_tn50_core_pure_no_gh_git_tokens`, `test_allowed_tools_cover_every_program`, `test_intent_and_validator_lines_say_tier_2`, `scripts/retrigger-review.sh`, `tests/pr_submit/test_conflict_scripts.py`.

F1 (MAJOR, not blocking, missing-requirement). Task 7 never fixes the timeline count semantics with a failable check. Spec section 4.4 requires `gh api --paginate` over the timeline and a count of `convert_to_draft` plus `ready_for_review` events (source.md:230), and the toggle classifier depends on that count (source.md:114-125). Task 7's acceptance criteria (plan:111-113) check only that the JSON line carries the keys and that a failing timeline call gives `transitions: null`. No criterion feeds N timeline events and asserts `transitions == N`, nor asserts `--paginate` in the recorded call. An implementation that counts one event type, or drops `--paginate`, passes every criterion.

F5 (MINOR, missing-requirement). Spec fold row for a settled `not_applied` ready request returns to `HELD`, "or `RELEASE_PENDING` when a failed release preceded it" (source.md:201). Task 3's criterion tests only the `HELD` outcome (plan:60). The failed-release variant is untested.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Write the heading exactly `## Findings block` and open the fence with the info string exactly `findings-v2` (not json). Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote of at most 200 characters). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=stale checked_at=2026-11-13T02:59:52Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:99-171

````markdown
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

````markdown
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

## Task 5: Fold the guard into the run log and export the public names

Depends on: Task 3
Depends on: Task 4

Edit `src/superclaude/pr_submit/run_log.py` `rebuild_state()` so `state["draft_guard"]` is `fold_draft_guard(events)` (default `None`, documented in the method docstring beside the #305 keys), importing from `src/superclaude/pr_submit/merge_guard.py`. Add the public guard names (the enums, dataclasses, the `BRANCH_*` constants, `fix_cycle_id`, `next_cycle_number`, `fold_draft_guard`, `pending_requests`, `held_cycle_published`, `classify_toggles`, `engage_decision`, `release_decision`, `resume_decision`, `guard_status`) to the imports and `__all__` of `src/superclaude/pr_submit/__init__.py`. Update `tests/pr_submit/test_run_log.py`: add `"draft_guard": None` to `_NEW_KEY_DEFAULTS` and add a test that a legacy log rebuilds every old key unchanged with `draft_guard` `None`, and that a log with a request and a confirmed settle rebuilds `phase: held`. Add `src/superclaude/pr_submit/merge_guard.py` to `CORE_PURE_FILES` in `tests/pr_submit/test_static_grep.py`.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_idempotency.py -q` passes, including `test_tn50_core_pure_no_gh_git_tokens` over the new file and the exact key-set assertions that use `_NEW_KEY_DEFAULTS`.
- `uv run python -c "from superclaude.pr_submit import fold_draft_guard, engage_decision, release_decision, resume_decision, held_cycle_published, fix_cycle_id; import superclaude.pr_submit.run_log"` exits 0 in a fresh interpreter (no import cycle).
- Rebuilding a log that holds `requested(draft)` then `settled(draft, confirmed, changed=True)` returns `state["draft_guard"]["phase"] == "held"` with `owned_draft` true; a log that ends after only the request returns `unsettled == 1` and phase `engage_pending`.
```

### .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r1/artifacts/base-commit-facts.md:1-13

```markdown
# Base-commit facts (orchestrator-read with git show e8db2fe6, the spec's grounding commit, 2026-11-07)

Reviewers have no shell. These are the repo facts the orchestrator verified. Repository HEAD has moved (the feature has since shipped), so never use HEAD repo files as evidence about the plan. Cite only the plan and the spec.

1. Import graph (checks spec F13 and plan Task 3 constraint "must not import recovery"): conflicts.py imports `.fsm` (run_validation_gates) and `.models` (MonitorState). fsm.py imports `.loop_guard`, `.models`, `.severity_router`. run_log.py imports only `.models` (EventType). recovery.py imports `.conflicts`, `.models`, `.run_log`. Result: no cycle run_log -> merge_guard -> conflicts.
2. recovery.py constants: BRANCH_A_LANDED = "landed", BRANCH_B_NOT_LANDED = "not_landed", BRANCH_C_AMBIGUOUS = "ambiguous".
3. conflicts.py: CONFLICT_CYCLE_PREFIXES = ("sync-", "conflict-"); is_conflict_cycle(cycle_id) = isinstance str and startswith prefixes.
4. Claims of "43" members at the base commit: models.py module docstring ("exactly 43 members - the 32 from spec ..."), models.py EventType class docstring ("EXACTLY 43 members"), a models.py comment "the 42nd-43rd" on the conflict-cycle block, run_log.py append docstring ("one of the 43 closed"), refs/loop-guard.md heading "The 43 event types" and "EXACTLY 43 members", test_run_log.py test name test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events plus two asserts, test_codex_reviews.py one `len(EventType) == 43`.
5. SKILL.md front matter allowed-tools at the base commit: `Read, Grep, Glob, Write, Edit, Bash(gh *), Bash(git *), Bash(uv *), Bash(make *), Bash(jq *), Task, Skill`. test_allowed_tools_cover_every_program checks that each fenced command's first word is an allowed program that is granted, and for a `scripts/` path only that the file exists. No front-matter edit is needed for a new script.
6. fsm.py: DEFAULT_CONFLICT_MAX_TIER = 0; SkillArgs.conflict_max_tier; build_arg_parser adds `--conflict-max-tier` with dest conflict_max_tier; parse_args passes ns.conflict_max_tier.
7. Test symbols present at the base commit: _NEW_KEY_DEFAULTS and exact key-set asserts in test_run_log.py; test_conflict_max_tier_default_and_bounds in test_skill_parse.py; CORE_PURE_FILES, _RESOLUTION_SCRIPTS, test_tn50_core_pure_no_gh_git_tokens, test_t105_runtime_repo_pin in test_static_grep.py; test_intent_and_validator_lines_say_tier_2 and test_allowed_tools_cover_every_program in test_conflict_sync_protocol.py; test_idempotency.py asserts len(IDEMPOTENCY_SETS) == 7; tests/pr_submit/test_conflict_scripts.py exists; scripts/retrigger-review.sh exists with `die`, an exit 127 check for a missing gh, and a numeric --pr check.
8. tests/skills/test_worker_contract.py: WRITE_VERB_RE matches `git (add|commit|push|merge|stash|update-ref|worktree add|remove)` and `gh (pr|api)` as whole words. The table key is (repo-relative path, "+".join of the distinct verbs found on that line, exact stripped line). Categories allowed: wc9-allowed, deferred:P1-P4, never-worker, no-command, read-only. A read-only entry that is a gh api POST is rejected (test_read_only_entries_are_not_gh_api_posts). test_classification_table_has_no_stale_entries fails when a keyed line no longer exists.

```

## Coverage slice

Inferred requirement rows (parsed_count = 0, so every row is inferred; match = containment >= 0.6 against one task). Unmatched rows were read by hand by the orchestrator and look carried by a task under other wording, but you may disagree.

| Row | Spec citation | Best task | Ratio | Match | Quote |
|---|---|---|---|---|---|
| INF-015 | source.md:101 | TASK-3 | 0.7143 | containment | `ValueError` otherwise or when `n < 1`. Never collides with `CONFLICT_CYCLE_PREFIXES`. |
| INF-016 | source.md:107 | TASK-8 | 0.6 | containment | it is not the run-wide `applied_edits` output field (which counts the whole run), so a zero-edit cycle after a fixing cycle still releases with `no_edits`. |
| INF-017 | source.md:108 | TASK-1 | 0.375 | none | whether written by the push triad or synthesized by recovery (`recovered: true`) |
| INF-018 | source.md:109 | TASK-3 | 0.4 | none | a test imports both modules and asserts equality, because the core cannot import `recovery`. |
| INF-019 | source.md:112 | TASK-3 | 0.6667 | containment | phase `DISABLED` with cause `already_draft` gives `off` (the PR was a draft before the run, nothing is guarded) |
| INF-020 | source.md:127 | TASK-4 | 0.6 | containment | `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action |
| INF-021 | source.md:164 | TASK-8 | 0.6 | containment | `REPORT_HELD` (no mutation; prints the clear command) |
| INF-022 | source.md:165 | TASK-4 | 0.6667 | containment | Each reason has its own test. |
| INF-023 | source.md:143 | TASK-4 | 0.8 | containment | `ENGAGE`; `notes` carries `auto_merge_armed` when set |
| INF-024 | source.md:175 | TASK-2 | 0.7143 | containment | Add to `EventType` in `models.py` (43 to 45, update the docstring and the `models.py:3,24` count, and the 43 text at `run_log.py:117`): |
| INF-025 | source.md:184 | TASK-3 | 0.8 | containment | `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` (`k` = 1 + prior requests with the same cycle and direction) |
| INF-026 | source.md:201 | TASK-3 | 0.9231 | containment | For a draft request that was the first guard record, the whole record is erased (the fold returns `None`, including `baseline` and `original_is_draft`) |
| INF-027 | source.md:208 | TASK-3 | 0.5333 | none | `original_is_draft` is never read from GitHub after the first record, so a resumed run cannot mistake its own draft for an original one. |
