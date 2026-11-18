# Reviewer 1 brief (analyzer), UC-1 pre-execution reflection, Tier 2

You are reviewer 1 of 3. You are read-only: you may Read, Grep and Glob; you must not edit, write, move or delete anything, and you run no shell commands. Return one reviewer card as your reply (the orchestrator saves it). Audit the plan against its spec using only the evidence below and what you can Read.

Persona: analyzer. Look for root causes of defects in the plan: contradictions between the plan and the spec or inside either one, acceptance criteria a wrong implementation would still pass, inputs a function needs but is never given, steps that cannot be carried out as written.

Rules for evidence:
- Plan under review: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`. Spec it implements: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`. Cite plan and spec lines with role plan or spec and that repo-relative path.
- The spec says it read the repository at master `e8db2fe66`. The plan was executed afterwards, so the live checkout (HEAD) now holds the finished implementation and is NOT the code the plan was written against. Read repository facts from the base-commit copy under `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/` (same layout as the repository). Do not cite HEAD code as a defect of the plan; a claim that is true only at HEAD is later change, not a plan defect. Put code evidence in the claim text as `path:line` of the base copy; citations objects point only at the plan or spec.
- The code graph index describes HEAD, not the base commit: do not use it for base-commit facts.
- Do not read anything under `.dev/tasks/` and do not read other reflect or eval run directories; they hold the execution history, not the evidence.
- Report a defect only when you can show it from a cited line. If a plan line is wrong, say what it should say. A zero-finding card is valid when you state which rows you verified.
- Mark severity MAJOR or CRITICAL only when an implementer following the plan would produce a wrong outcome or the plan cannot be carried out; otherwise MINOR.

## T1 card excerpt

Temporal anchor: the spec says it read the repository at master `e8db2fe66` (spec line 13). The plan was executed later; HEAD now contains the implementation (commit `0b8a5801d`). Every repository fact below was read from a `git archive` of `e8db2fe66` extracted to `artifacts/base-e8db2fe6/` in this run's output directory, never from HEAD. A claim that holds only at HEAD is post-execution evolution, not a plan defect.

H1 (analyzer, MAJOR, non-blocking): `resume_decision` row 4 cannot be implemented from its own signature. Spec line 166 says row 4 "re-enter[s] `release_decision` with `push_completed=True`", but `release_decision` (spec line 107) needs `cycle_id`, `applied_edits` and `target_sha`, and `resume_decision` (spec line 109) receives none of them. Task 4 (plan lines 70 and 77) repeats the row and its acceptance only asserts the returned action, so an implementation that passes `target_sha=read.head_sha` (making the head check vacuous) would pass every listed test.

H2 (analyzer, MAJOR, non-blocking): the Wave 0 bullet is specified two incompatible ways. Spec line 241 says it applies at every ordinal and "contains no L3 or `draft` condition", and in the same cell says "at L3 with `--merge-guard off` it prints the unprotected line once". Task 9 (plan lines 137 and 140) copies both, and its acceptance test must fail when the bullet "names an L3 or `draft` condition". A bullet that satisfies the print rule names L3; the test as worded cannot be both written and passed.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T05:18:25Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:99-112

(function contracts incl. release_decision and resume_decision signatures)

`````markdown
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
`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:129-171

(engage, release and resume decision tables)

`````markdown
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
`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:241-241

(the Wave 0 bullet requirement)

`````markdown
| `SKILL.md` | One short bullet under each of Wave 0, Wave 3, Wave 6 and Wave 8, written as new sentences after, never inside, the pinned sentences. The Wave 0 bullet applies at every ordinal and in both modes: on `--resume`, or when the run log holds guard events, it loads the ref (Resume and Exit report) before Wave 1 and before any edit, release or re-trigger; at L3 with `--merge-guard off` it prints the unprotected line once. The Wave 3, Wave 6 and Wave 8 bullets load the ref only at L3 with `draft`: the Wave 3 bullet states that engage happens at the end of Wave 3 only when at least one verified finding of Medium severity or higher is routed to a fix, and once per cycle id (it must not contain the words `evidence-validator` or `conflict-intent.md`, which a line-content test allows only on lines that also say "Tier 2"); the Wave 6 bullet states that Pre-push runs at the pre-push head guard step before `push_decision` and Release runs after `push_completed` before reply, resolve and the re-trigger; the Wave 8 bullet states that a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll. Also one `--merge-guard {draft,off}` row in the Required Input flag table beside `--conflict-max-tier`; one row `merge_guard` in the output table, which also carries the literal L2 line "PR #N is still mergeable; this run's fixes are local only." so that a fresh L2 run prints it without loading the ref; one line in the wave structure list. The Wave 0 bullet is a flat line placed before the Wave 1 bullet and contains no L3 or `draft` condition (the Wave bullets are flat lines, not headings, so the test checks position and wording). No new python fence (the one-fence tests, `test_cosmos_protocol.py:34-44`, `test_codex_reviews.py:685-697`). |
`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:66-78

(Task 4)

`````markdown
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
`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:132-144

(Task 9)

`````markdown
## Task 9: Wire the Wave 0 resume and `off` hook, the flag row, the output row and the wave line into `SKILL.md`

Depends on: Task 6
Depends on: Task 8

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` additively, using the pins and line-content rules recorded in `./artifacts/pre-build-gate.md`: one new bullet under Wave 0, written as a flat line before the Wave 1 bullet, that applies at every ordinal and in both modes and carries no L3 or `draft` condition; it states that on `--resume`, or when the run log already holds guard events, the ref `refs/merge-guard.md` (Resume and Exit report) is loaded before Wave 1 and before any edit, release or re-trigger, and that at L3 with `--merge-guard off` the line "Remediation is unprotected: --merge-guard off." is printed once and no draft call is made. Add one `--merge-guard {draft,off}` row to the Required Input flag table beside `--conflict-max-tier`; one row `merge_guard` to the output table (values `off`, `released`, `held`, `user_override`, `unavailable`) that also carries the literal L2 line "PR #N is still mergeable; this run's fixes are local only." so a fresh L2 run prints it without loading the ref; and one line in the wave-structure list. No new python fence. Where a new line would contain `gh pr` or `gh api`, rephrase it (for example "print the clear command from the ref") so that no classification entry is needed; if one is unavoidable, add its `WRITE_VERB_CLASSIFICATION` entry as the last step. Extend `tests/pr_submit/test_merge_guard_protocol.py` with a test for the Wave 0 bullet (it names `--resume`, sits before the Wave 1 bullet, contains no `L3 only` or `draft` gate wording and contains the literal `off` line), one for the flag row, one for the output row including the literal L2 line, and one for the wave-structure line. Run `make sync-dev`.

Acceptance criteria:
- The Wave 0 test fails when the bullet is placed after the Wave 1 bullet, when it names an L3 or `draft` condition, or when the literal `off` line is missing, and passes on the real file.
- A test asserts the literal text "PR #N is still mergeable; this run's fixes are local only." is present in `SKILL.md` itself (not only in the ref), so a fresh L2 run needs no ref load.
- `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_cosmos_protocol.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_merge_guard_protocol.py tests/skills/test_worker_contract.py -q` passes with no edit to any existing test expectation other than those listed in Tasks 2, 5, 7 and 8.
- `SKILL.md` still has exactly one python code fence and no `src/superclaude` string, and the new lines contain neither `evidence-validator` nor `conflict-intent.md`.
- `make verify-sync` exits 0.
`````

### .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/src/superclaude/pr_submit/recovery.py:33-42

(base commit e8db2fe66)

```python
from __future__ import annotations

from .conflicts import ResumePlan, crash_resume_plan, is_conflict_cycle
from .models import EventType, MonitorState
from .run_log import RunLog

# Branch outcomes.
BRANCH_A_LANDED = "landed"
BRANCH_B_NOT_LANDED = "not_landed"
BRANCH_C_AMBIGUOUS = "ambiguous"
```

### .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/src/superclaude/pr_submit/recovery.py:69-95

(base commit e8db2fe66)

```python
def detect_crash_window(run_log: RunLog) -> dict | None:
    """Return the dangling ``push_initiated`` event (no matching ``push_completed``), or None.

    Matches on ``idempotency_key``: a ``push_initiated`` whose key has no later
    ``push_completed`` (or ``push_aborted_or_not_landed``) is the crash window.
    """
    initiated: dict[str, dict] = {}
    finalized: set[str] = set()
    for ev in run_log.read_events():
        key = ev.get("idempotency_key")
        if not key:
            continue
        et = ev.get("event_type")
        if et == EventType.PUSH_INITIATED.value:
            initiated[key] = ev
        elif et in (
            EventType.PUSH_COMPLETED.value,
            EventType.PUSH_ABORTED_OR_NOT_LANDED.value,
        ):
            finalized.add(key)
    for key, ev in initiated.items():
        if key not in finalized:
            return ev
    return None


def resolve_crash_window(
```

### .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/src/superclaude/pr_submit/models.py:20-30

(base commit e8db2fe66)

```python
from enum import Enum


class EventType(str, Enum):
    """Closed enum of run-log event types — EXACTLY 43 members.

    The 32 event types listed in spec §11.3 (merged-spec.md:724-731) PLUS
    ``push_aborted_or_not_landed`` (spec §12.1 line 771 — the crash-window
    not-landed branch) — the 33 prior members — PLUS the 4 V1.1
    re-review/fallback events (``rereview_requested``, ``decline_detected``,
    ``auggie_fallback_invoked``, ``max_rounds_clamped``; addendum §6.1) PLUS
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-003: an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | Constraints | covered | source.md:6 |
| INF-006: maps, first match wins | Task 4 | covered | source.md:112 |
| INF-007: observed = read.transitions - guard.baseline | Task 4 | covered | source.md:118 |
| INF-008: `HALT_UNAVAILABLE(timeline_unreadable)` | none | unmapped (containment 0.00) | source.md:140 |
| INF-009: `push_completed` and `read.head_sha == target_sha` | Task 4 | covered | source.md:156 |
| INF-010: re-enter `release_decision` with `push_completed=True` | Task 4 | covered | source.md:166 |
| INF-012: `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` | Task 3 | covered | source.md:184 |
| INF-013: the whole record is erased (the fold returns `None` | Task 3 | covered | source.md:201 |
| INF-014: `original_is_draft` is never read from GitHub after the first record | Task 3 | covered | source.md:208 |
| INF-024: `fix_cycle_id` gives guard-enabled cycles an explicit id | Task 8 | covered | source.md:251 |
| INF-029: protocol assertions that the Wave 0 bullet names `--resume`, is not gated on L3 or `draft` | Task 9 | covered | source.md:322 |
