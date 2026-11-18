# Reviewer brief 1

## T1 card excerpt

### Summary

The plan covers the spec well: every file of source.md section 6, every test named in section 7 and every plan note of section 10 maps to a task (see coverage). The defects I found are contradictions or gaps inside acceptance criteria and signatures, not missing work. None of them makes the plan unbuildable. Three are MAJOR, four MINOR.

### Findings

F1 MAJOR, contradiction (Task 7). The acceptance criterion asks that a static scan assert "every `gh` line carries `--repo` or a `repos/` path" (plan line 113) and also that the new script join `_RESOLUTION_SCRIPTS` and pass its tests (plan line 108, 113). Those tests require a line containing `gh repo view --json nameWithOwner` (tests/pr_submit/test_static_grep.py:549, inside the tests that use `_RESOLUTION_SCRIPTS` at :481), which carries neither `--repo` nor `repos/`; the model script has exactly that line (scripts/retrigger-review.sh:50). Both cannot hold unless the new scan reuses the existing `_repo_scoped` predicate, which accepts the resolution idiom (test_static_grep.py:35, :107). The plan names the stricter wording instead.

F2 MAJOR, under-specified signature (Task 4, spec 4.1). `resume_decision` row 4 is "re-enter `release_decision` with `push_completed=True`" (source.md:166), but `resume_decision`'s documented parameters (source.md:109, plan line 70) omit `cycle_id`, `applied_edits` and `target_sha`, which `release_decision` needs (source.md:107). No `GuardAction` value stands for "re-enter" (source.md:82-85). The acceptance criterion (plan line 77) cannot be written as stated. An implementer who omits the head proof would release without confirming the head, breaking the rule that release needs a confirmed push.

F3 MAJOR, report gap (Task 3, Task 8). The spec says a halt with reason `draft_guard_unavailable` reports `unavailable` (source.md:112, :68), but `guard_status(guard, mode, ordinal)` has no halt input, and plan line 61 pins "no record at ordinal 3 gives `released`". An engage that halts because the read or the timeline failed writes no guard event, so the run reports `released` for a halt. No task (Task 8 Exit report, plan line 124; Task 11) assigns the halt-reason override or tests it.

F4 MINOR, untested fold field (Task 3). `guard_status` maps `DISABLED` + `user_override` to `user_override` (source.md:112), but the fold table row for `settled(any, skipped, user_override)` (source.md:206) does not say `disabled_cause` is set, and Task 3's fold criterion (plan line 60) tests `already_draft` only. A fold that leaves the cause empty passes Task 3 and mis-reports.

F5 MINOR, weak baseline (Task 1, Task 13). Task 1 records the base failures before any `make sync-dev` (plan line 33). The repo notes that fresh worktrees fail about 43 mirror/ruff tests until `make install` and `make sync-dev` run and to record the baseline after both (docs/memory/reflect/deviation-patterns-post-release-v5.0.0.md:7). Task 13 passes when no failing id is "absent from the base-commit record" (plan line 199), so a feature-caused mirror failure that is also in the stale baseline is hidden; only two files are re-run separately.

F6 MINOR, unowned mapping (spec 4.1/4.4). `GuardRead` fields (`is_draft`, `head_sha`, `auto_merge_armed`; source.md:88-91) differ from the script's JSON keys (`isDraft`, `headRefOid`, `autoMergeRequest`; source.md:230). No task or function does the conversion, and the SKILL has no python fence to do it.

F7 MINOR, test wording (Task 9). The Wave 0 bullet must name the `--merge-guard off` L3 case (plan line 137) yet its test must fail on "L3 or `draft` gate wording" (plan line 140); a sentence "no draft call is made" contains the word `draft`.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T04:10:31Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:73-172

````markdown
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

### tests/pr_submit/test_static_grep.py:35-36

```python
_REPO_RESOLVE = re.compile(r"\bgh\s+repo\s+view\b")
# The T-N50 core-pure file set.
```

### tests/pr_submit/test_static_grep.py:107-132

```python
def _repo_scoped(line: str) -> bool:
    """A gh command line is repo-scoped if it pins a whole-token ``--repo``, is a
    ``gh api`` call carrying a ``repos/<owner/repo>/`` path or ``graphql``, or IS the
    ``gh repo view`` resolution idiom.

    This is the generalized safety property: the prior implementation required the
    literal fork slug, but the repo is now RESOLVED at runtime — so "scoped" means the
    call carries an explicit repo reference (computed, not bare), never a hardcoded
    owner/repo. A bare `gh pr`/`gh api` with none of these would silently default onto
    an upstream parent → the defect.

    The match is structure-anchored, NOT a loose substring (D3 hardening): a trailing
    ``#`` comment is stripped first (so ``gh pr create … # see repos/docs`` does NOT
    pass), ``--repo`` is matched as a whole token (so ``--reposcope`` does NOT pass), and
    ``repos/``/``graphql`` only count when they ride on an actual ``gh api`` command (so
    an incidental ``# graphql`` mention does NOT pass). These three holes were real
    bypasses of the prior unanchored ``in``-substring predicate.
    """
    code = re.sub(r"\s+#.*$", "", line)  # strip a trailing shell / markdown comment
    if re.search(r"--repo\b", code):  # whole-token --repo (gh pr / gh repo)
        return True
    if _REPO_RESOLVE.search(code) is not None:  # the `gh repo view` resolution idiom
        return True
    # repos/ path or graphql must be on an actual `gh api` invocation, not anywhere.
    if re.search(r"\bgh\s+api\b", code) and ("repos/" in code or "graphql" in code):
        return True
```

### tests/pr_submit/test_static_grep.py:481-487

```python
_RESOLUTION_SCRIPTS = (
    SKILL_DIR / "scripts" / "poll-augment-review.sh",
    SKILL_DIR / "scripts" / "poll-ci-checks.sh",
    SKILL_DIR / "scripts" / "retrigger-review.sh",
    SKILL_DIR / "scripts" / "reply-resolve-thread.sh",
    SKILL_DIR / "scripts" / "set-draft-state.sh",
)
```

### tests/pr_submit/test_static_grep.py:540-552

```python
            i
            for i, line in enumerate(lines)
            if line.lstrip().startswith(("REPO=", "[ -n"))
            and "git remote get-url origin" in line
        )
        gh_view_at = next(
            i
            for i, line in enumerate(lines)
            if line.lstrip().startswith(("REPO=", "[ -n"))
            and "gh repo view --json nameWithOwner" in line
        )
        assert origin_at < gh_view_at, (
            f"{script.name}: `gh repo view` is tried before the origin remote"
```

### src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh:46-51

```bash
# Resolve the target repo (owner/repo). The SKILL normally passes --repo; absent it,
# resolve from the current checkout (the origin remote, then gh repo view). The
# issue-comment POST target is COMPUTED — never a literal owner/repo (de-hardcoded).
REPO="${REPO:-$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##' || true)}"
[ -n "$REPO" ] || REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
[ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001: engage at the first verified Medium-or-higher finding routed to a fix | Goal+Constraints | covered (containment 0.875) | source.md:6 |
| INF-002: default on at `--monitor 3` via `--merge-guard {draft,off}` | Task 12 | covered (containment 1.0) | source.md:6 |
| INF-003: release when the fix push is confirmed on the PR head, before replies and the re-trigger | Goal+Constraints | covered (containment 1.0) | source.md:6 |
| INF-004: an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | Goal+Constraints | covered (containment 0.778) | source.md:6 |
| INF-005: No new `MonitorState`. | Task 10 | covered (containment 1.0) | source.md:51 |
| INF-006: Nothing mutates. A held guard found in the log is reported with the clear command. | none | UNMAPPED by rule (none 0.556) | source.md:57 |
| INF-007: unsettled requests are reconciled before any edit, release or re-trigger | Goal+Constraints | covered (containment 0.625) | source.md:58 |
| INF-008: Wave 0 prints once: "Remediation is unprotected: --merge-guard off." | Task 9 | covered (containment 1.0) | source.md:59 |
| INF-009: PR #N is still mergeable; this run's fixes are local only. | Task 9 | covered (containment 1.0) | source.md:60 |
| INF-010: Print the clear command once. | Task 9 | covered (containment 1.0) | source.md:61 |
| INF-011: Settle `skipped/already_draft`, phase `disabled`, never mutate. | Task 3 | covered (containment 0.857) | source.md:62 |
| INF-012: Release, cause `no_edits`. | Task 4 | covered (containment 1.0) | source.md:63 |
| INF-013: Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | Task 8 | covered (containment 1.0) | source.md:64 |
| INF-014: Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | Task 8 | covered (containment 0.778) | source.md:65 |
| INF-015: Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, re... | Task 3 | covered (containment 0.6) | source.md:66 |
| INF-016: Do not release; report `held (timeline unreadable)`; keep pushing. | Goal+Constraints | covered (containment 0.857) | source.md:67 |
| INF-017: Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | Task 8 | covered (containment 1.0) | source.md:68 |
| INF-018: PR stays draft; report `held` with the clear command. | Task 8 | covered (containment 0.857) | source.md:69 |
| INF-019: No `gh` or `git` word on any line, comments included (F6). | Goal+Constraints | covered (containment 0.857) | source.md:75 |
| INF-020: Never collides with `CONFLICT_CYCLE_PREFIXES`. | Task 3 | covered (containment 0.667) | source.md:101 |
| INF-021: Guard requests with no matching settle, matched by `idempotency_key` | Task 3 | covered (containment 0.833) | source.md:104 |
| INF-022: THIS cycle's count of applied edits | Task 4 | covered (containment 1.0) | source.md:107 |
| INF-023: a test imports both modules and asserts equality, because the core cannot import `recov... | none | UNMAPPED by rule (none 0.455) | source.md:109 |
| INF-024: A halt with reason `draft_guard_unavailable` reports `unavailable`. | Task 8 | covered (containment 0.8) | source.md:112 |
| INF-025: the only foreign-toggle test; no actor identity, F11 | none | UNMAPPED by rule (none 0.5) | source.md:114 |
| INF-026: `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | Task 3 | covered (containment 1.0) | source.md:133 |
| INF-027: `read.state != "OPEN"` \| `HALT_PR_NOT_OPEN` | Task 1 | covered (containment 0.75) | source.md:136 |
| INF-028: `push_completed` and `read.head_sha == target_sha` \| `RELEASE(cause=pushed)` | Task 4 | covered (containment 0.714) | source.md:156 |
| INF-029: `REPORT_HELD` (no mutation; prints the clear command) | Task 8 | covered (containment 0.6) | source.md:164 |
| INF-030: Each reason has its own test. | Goal+Constraints | covered (containment 0.667) | source.md:165 |
| INF-031: `landed` is a push recovery just completed; `published` is a push that completed normal... | Task 8 | covered (containment 0.889) | source.md:166 |
| INF-032: 43 to 45, update the docstring | Task 2 | covered (containment 1.0) | source.md:175 |
| INF-033: appended and fsynced BEFORE the draft/ready call | Goal+Constraints | covered (containment 0.667) | source.md:178 |
| INF-034: `run_log.rebuild_state()` stores it as `state["draft_guard"]` (default `None`, added to... | Task 5 | covered (containment 0.778) | source.md:187 |
| INF-035: For a draft request that was the first guard record, the whole record is erased | Task 3 | covered (containment 0.857) | source.md:201 |
| INF-036: `original_is_draft` is never read from GitHub after the first record | Task 3 | covered (containment 0.857) | source.md:208 |
| INF-037: `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD` | Task 6 | covered (containment 1.0) | source.md:215 |
| INF-065: whether written by the push triad or synthesized by recovery (`recovered: true`) | none | UNMAPPED by rule (none 0.375) | source.md:108 |
| INF-066: phase `DISABLED` with cause `already_draft` gives `off` | Task 3 | covered (containment 1.0) | source.md:112 |
