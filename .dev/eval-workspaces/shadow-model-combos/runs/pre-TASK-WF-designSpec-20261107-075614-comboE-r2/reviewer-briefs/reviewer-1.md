## T1 card excerpt

Persona: analyzer. You audit logic and root causes: do the plan tasks, as written, produce the behavior the spec tables define? Look for contradictions between spec and plan, acceptance criteria that cannot detect a wrong implementation of a table row, and glue nobody owns.

Attribution note: this package already executed (landed in commit 0b8a5801d, parent 0e486ab8d). The spec facts F1-F13 were re-read at the parent commit and hold there (EventType has 43 members at the parent, `conflicts.py` imports only `.fsm` and `.models`, `fsm.py` does not import `run_log`, `recovery.py` defines `BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED`, `BRANCH_C_AMBIGUOUS`, the enum already has `FIX_APPLIED`, `PUSH_COMPLETED`, `REREVIEW_REQUESTED`, `TERMINAL_HALTED`). HEAD now carries the implementation, so a citation of HEAD text as a plan defect or as a gap must be checked against 0e486ab8d (`git show 0e486ab8d:<path>` is not available to you; if you cannot check, say so and mark the claim as inferred). You audit the PLAN and SPEC text, not the shipped code. Rules for claims: before you say an acceptance criterion "cannot fail" or "is missing", quote the criterion text first; a constraint stated in task prose without an acceptance criterion is a MINOR gap unless a wrong outcome follows.

Coverage (Step 1B.0): 0 parsed requirement IDs (the spec uses FR/F/G/O labels), 48 inferred rows INF-001..INF-048 with verbatim quotes (artifacts/coverage-matrix.json); containment matching covered 42 of 48 (`coverage_pct_union` 0.875). `coverage_degraded: parsed-sparse`, so no Tier-1 stop. Unmatched rows are partly matcher noise: INF-007, INF-012, INF-015, INF-026, INF-029, INF-046.

Candidate gaps from Tier 1 for your lens (hypotheses; verify or refute each, then add what is missing):
- H2. Cycle-id continuity is asserted by wording only: spec section 4.6 (source.md:249-251) says the SKILL mints one id at the end of Wave 3 and the push triad and `rereview_requested` reuse it; `held_cycle_published` (source.md:108) depends on the id matching the `push_completed` event. Task 8 AC (plan:127) only requires the ref to state the single place; Task 10 (plan:150) checks the Wave 3 bullet.
- H3. Two pieces of glue have no owner: (a) `GuardRead` is "the parsed output of --read" (source.md:88-90) but no function maps the script JSON keys `isDraft`, `headRefOid`, `autoMergeRequest` to `is_draft`, `head_sha`, `auto_merge_armed`; (b) the request key `guard:<run_id>:<cycle_id>:<to>:a<k>` (source.md:184) has no builder and no AC checks the ref states the format.
- H4. Task 7 AC (plan:111) lists the `autoMergeRequest` key but not its type; the spec example prints a boolean (source.md:230) while `gh pr view --json autoMergeRequest` returns an object or null.

Write the literal heading `## Findings block` and under it ONE fence opened with exactly ```findings-v2 (never ```json, never a table), JSON lines, one object per line. Fields: id (F1, F2, ...), severity (only CRITICAL, MAJOR or MINOR; a MINOR finding is never blocking), blocking (true or false), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids such as INF-012 or spec labels, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote of at most 200 characters; use the exact repo-relative paths printed in the H3 headings of your grounding hunks, and take line numbers from those headings). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["INF-012"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a line `coverage_rows_checked:` listing the INF row ids of your coverage slice you verified (comma separated), then a line `reviewer_model_self_report:` stating the model you are running as in one line. Return the whole card as your reply text; do not write or edit any file.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T04:08:07Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:71-211

`````markdown
## 4. Component specifications

### 4.1 `src/superclaude/pr_submit/merge_guard.py` (new, pure)

No `gh` or `git` word on any line, comments included (F6). Imports only `enum`, `dataclasses`, `re`, `.conflicts.is_conflict_cycle`.

```python
class GuardMode(str, Enum):   DRAFT = "draft"; OFF = "off"      # extension point for later modes
class Direction(str, Enum):   DRAFT = "draft"; READY = "ready"
class Phase(str, Enum):       ENGAGE_PENDING; HELD; RELEASE_PENDING; RELEASED; DISABLED

class GuardAction(str, Enum):
    NOOP; ENGAGE; RELEASE; RETRY_RELEASE; HOLD; REPORT_HELD
    SKIP_ALREADY_DRAFT; SKIP_USER_OVERRIDE; RECONCILE
    HALT_PR_NOT_OPEN; HALT_UNAVAILABLE

@dataclass(frozen=True)
class GuardRead:              # parsed output of `--read`
    ok: bool; state: str | None; is_draft: bool | None; head_sha: str | None
    auto_merge_armed: bool; transitions: int | None; complete: bool

@dataclass(frozen=True)
class GuardDecision:
    action: GuardAction; reason: str; cause: str | None = None; notes: tuple[str, ...] = ()
```

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

`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:249-251

`````markdown
### 4.6 Cycle identity

`fix_cycle_id` gives guard-enabled cycles an explicit id: `fix-<n>` for review-fix cycles and `ci-<n>` for CI-fix cycles, `n` from `next_cycle_number`. The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push triad (`push_idempotency_key`) and of `rereview_requested`, so the guard, the push and the re-trigger of one cycle share a key. With `--merge-guard off` nothing changes. The build must first confirm where the SKILL assigns a fix cycle's id today and keep exactly one source for it (open item O1).
`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:52-90

`````markdown
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
`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:157-173

`````markdown
## Phase 4: Scenario tests

## Task 11: Write the scenario tests over the run log

Depends on: Task 3
Depends on: Task 4
Depends on: Task 5
Depends on: Task 7

Create `tests/pr_submit/test_merge_guard_scenarios.py` with a small test driver that applies the pure decisions of `merge_guard.py`, appends events to a real `RunLog` in a temporary directory and runs `scripts/set-draft-state.sh` against a fake `gh`; it imports only the fake-`gh` helper or fixture from `tests/pr_submit/test_set_draft_state.py`, never a `test_*` function (pytest would collect it twice). Implement the twelve test names of ./source.md section 7 and the acceptance trace of section 5. Cover the cases of the section 5 table: engage failure halts before any edit, validation failure leaves phase `held`, zero-edit cycle releases with `no_edits` (including a zero-edit cycle after a fixing cycle), foreign toggle disables the guard and the run continues, crash between request and settle reconciles on resume (including `not_applied` followed by a normal re-engage, and a ready request settled `not_applied` that stays `HELD` and is released after the publication check), crash after a dangling `push_initiated` with branch strings produced by the real `detect_crash_window` and `resolve_crash_window` (`landed` releases, `not_landed` holds, `ambiguous` holds), crash after a normal `push_completed` (no dangling window, `published` true) releases before the re-trigger, merged PR halts `pr_not_open`, ordinals 0 to 2 and `off` make no call, an originally draft PR is never made ready, an engage, crash, resume with live draft true stays `held` and is released after the push, and a conflict-cycle id never engages.

Acceptance criteria:
- The test file defines `test_guard_modes_ordinals_and_resume_authority`, `test_attach_and_create_preserve_preexisting_draft`, `test_guard_engages_at_routed_finding_once_per_cycle`, `test_guard_releases_only_after_publication_or_zero_edit_proof`, `test_guard_holds_on_unpublished_or_uncertain_exits`, `test_guard_engage_failure_blocks_edits`, `test_guard_release_failure_retries_once_and_reports`, `test_guard_external_toggle_and_roundtrip_disable`, `test_guard_missing_timeline_or_ambiguous_intent_never_readies`, `test_guard_crash_boundaries_and_push_recovery_abc`, `test_guard_closed_merged_or_moved_head_forbids_mutation` and `test_guard_script_contract_scoping_and_legacy_fold` (the last asserts the legacy-log fold and the script scoping through shared helpers, with no imported `test_*` function).
- The acceptance-trace test asserts the exact event order `draft_guard_requested(draft)`, `draft_guard_settled(confirmed)`, `fix_applied`, `push_completed`, `draft_guard_requested(ready)`, `draft_guard_settled(confirmed)`, `rereview_requested` from `RunLog.read_events()` and asserts no `rereview_requested` appears before the release settle.
- The crash tests build the dangling window by appending a real `push_initiated` event and calling `detect_crash_window` and `resolve_crash_window`; none of them passes a hand-written branch string to `resume_decision`, and the normal-`push_completed` test asserts `detect_crash_window` returns `None` and `published` is true.
- Forbidden-call assertions: the fake `gh` log never contains `pr ready` without `--undo` for an originally draft PR and never contains any `pr ready` call at ordinal 2 or with `off`; after a `pr_not_open` halt the test asserts on `RunLog.read_events()` that no `push_initiated` or `push_completed` event follows the halt (the fake `gh` log cannot see a `git push` and is not used for this check).
- `uv run pytest tests/pr_submit -q` passes in full.
`````

## Coverage slice

You are responsible for the rows INF-001 to INF-024 (the decision tables, fold, events and flag).

| Requirement | Matched task | Status | Grounding |
|---|---|---|---|
| INF-001: engage at the first verified Medium-or-higher finding routed to a fix; default on at `--mo | Task 8 | covered (containment 0.7333) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:6 |
| INF-002: Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made | Task 9 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:59 |
| INF-003: PR #N is still mergeable; this run's fixes are local only. | Task 9 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:60 |
| INF-004: Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | Task 8 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:64 |
| INF-005: Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, repor | Task 3 | covered (containment 0.6) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:66 |
| INF-006: Do not release; report `held (timeline unreadable)`; keep pushing. | Task 8 | covered (containment 0.7143) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:67 |
| INF-007: No `gh` or `git` word on any line, comments included (F6). | none | unmatched (best ratio 0.5714) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:75 |
| INF-008: `"fix-<n>"` for kind `fix`, `"ci-<n>"` for kind `ci`; `ValueError` otherwise or when `n <  | Task 3 | covered (containment 0.875) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:101 |
| INF-009: 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. | Task 3 | covered (containment 0.6667) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:102 |
| INF-010: `applied_edits` is THIS cycle's count of applied edits; it is not the run-wide `applied_ed | Task 4 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:107 |
| INF-011: `True` when `guard` is not `None` and the log holds a `push_completed` event whose `cycle_ | Task 3 | covered (containment 0.8182) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:108 |
| INF-012: a test imports both modules and asserts equality, because the core cannot import `recovery | none | unmatched (best ratio 0.4) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:109 |
| INF-013: `failed_mutations` keeps a call that failed on the client but landed on the server from be | Task 4 | covered (containment 0.6) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:127 |
| INF-014: `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | Task 3 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:133 |
| INF-015: `HALT_UNAVAILABLE(read_failed)` | none | unmatched (best ratio 0.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:135 |
| INF-016: `guard is None` and `read.is_draft` | Task 3 | covered (containment 0.75) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:142 |
| INF-017: `push_completed` and `read.head_sha == target_sha` | Task 4 | covered (containment 0.75) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:156 |
| INF-018: `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED`) | Task 3 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:164 |
| INF-019: `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous` | Task 4 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:165 |
| INF-020: re-enter `release_decision` with `push_completed=True` | Task 4 | covered (containment 1.0) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:166 |
| INF-021: Add to `EventType` in `models.py` (43 to 45, update the docstring and the `models.py:3,24` | Task 2 | covered (containment 0.8235) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:175 |
| INF-022: appended and fsynced BEFORE the draft/ready call | Task 7 | covered (containment 0.6) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:178 |
| INF-023: stores it as `state["draft_guard"]` (default `None`, added to `_NEW_KEY_DEFAULTS`) | Task 5 | covered (containment 0.7143) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:187 |
| INF-024: the pending key is cleared and the phase returns to `phase_before_request`; `owned_draft`  | Task 3 | covered (containment 0.9) | .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:201 |
