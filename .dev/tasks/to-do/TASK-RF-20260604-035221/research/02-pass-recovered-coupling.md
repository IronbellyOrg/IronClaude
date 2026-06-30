# Research: PASS_RECOVERED coupling

Status: Complete
Date: 2026-06-04

Refs: PR branch = `origin/feat/sprint-auto-resume-v435` (aedd0104); master = `origin/master` (643e6e7f). All line numbers below are from `git show <ref>:<path>` of the named branch.

---

## The latent regression (one paragraph)

Master (#121/#126) added `TaskStatus.PASS_RECOVERED = "pass_recovered"` — a per-task success outcome assigned when a task exits non-zero but emitted completion evidence before a budget/turn overrun. Master's `TaskStatus.is_success` is PASS-family: `self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)`. The PR branch's `TaskStatus` predates this: it has **no** `PASS_RECOVERED` member, and `is_success == (self == TaskStatus.PASS)`. The PR's new `resume/` package never uses `is_success` for task-level decisions — it compares the persisted task status by **identity** to `TaskStatus.PASS` (`is`/`is not`). A plain `git merge` of the two branches **auto-merges `models.py` with NO conflict** and keeps master's `PASS_RECOVERED` enum + PASS-family `is_success` (verified below). The PR's identity checks survive the merge unchanged. Result: a task that master persisted as `"pass_recovered"` deserializes to `TaskStatus.PASS_RECOVERED`, which `is not TaskStatus.PASS` → the resume planner treats a genuinely-completed task as **unfinished** and re-runs it (and the integrity/drift signals mis-classify it). This is silent: no merge conflict, no test failure on the PR branch (whose own `TaskStatus` can never produce `PASS_RECOVERED`).

---

## 1. master vs PR `TaskStatus` + merge-tree (CONFIRMED)

Command: `git show origin/master:src/superclaude/cli/sprint/models.py`

master `models.py:46-58`:
```python
class TaskStatus(Enum):
    PASS = "pass"
    PASS_RECOVERED = "pass_recovered"  # non-zero exit but evidence of success
    FAIL_TERMINAL = "fail"
    FAIL_RECOVERABLE = "fail_recoverable"
    INCOMPLETE = "incomplete"
    SKIPPED = "skipped"

    @property
    def is_success(self) -> bool:
        return self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)
```

Command: `git show origin/feat/sprint-auto-resume-v435:src/superclaude/cli/sprint/models.py`

PR branch `models.py:45-56`:
```python
class TaskStatus(Enum):
    PASS = "pass"
    FAIL_TERMINAL = "fail"
    FAIL_RECOVERABLE = "fail_recoverable"
    INCOMPLETE = "incomplete"
    SKIPPED = "skipped"

    @property
    def is_success(self) -> bool:
        return self == TaskStatus.PASS
```

PR branch `TaskStatus` has **no `PASS_RECOVERED`** and `is_success` is identity-to-PASS. (Both branches' `PhaseStatus.is_success` IS PASS-family-safe — master `models.py:426-432`, PR `models.py:315-322`.)

**Merge-tree (CONFIRMED no conflict in models.py):**
Command: `git merge-tree --write-tree --name-only origin/master origin/feat/sprint-auto-resume-v435`
- Reports `Auto-merging src/superclaude/cli/sprint/models.py` with **NO** `CONFLICT` line for it.
- Conflicts reported only for: `CHANGELOG.md`, `cli/sprint/commands.py`, `cli/sprint/executor.py` (unrelated to this enum).
- The auto-merged `models.py` keeps master's version: verified by reading the merged tree's blob — `TaskStatus` has `PASS_RECOVERED = "pass_recovered"` and `is_success` returns `self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)`.

**This is the regression surface: the merge silently widens the enum/`is_success` while leaving every PR-branch identity-against-PASS check intact.**

---

## 2. master executor.py persists `"pass_recovered"` into phase-N-result.json (CONFIRMED)

Command: `git show origin/master:src/superclaude/cli/sprint/executor.py`

**Assignment** — shared per-task status determination, `executor.py:1004-1015`:
```python
if exit_code == 0:
    status = TaskStatus.PASS
elif exit_code == 124:
    status = TaskStatus.INCOMPLETE
elif detect_error_max_turns(task_output_path) and _task_completed_before_overrun(task_output_path):
    status = TaskStatus.PASS_RECOVERED      # executor.py:1011
elif _is_transient_failure(task_output_path):
    status = TaskStatus.FAIL_RECOVERABLE
else:
    status = TaskStatus.FAIL_TERMINAL
```

**Serialization** — `TaskResult.to_dict` in master `models.py:190-207`:
```python
"status": self.status.value,    # models.py:207  → "pass_recovered"
```
Round-trip: `from_dict` at master `models.py:231` → `status=TaskStatus(data["status"])`.

**Persistence to disk** — master `executor.py:2638-2658` `_write_phase_result_json`:
```python
payload = { ..., "task_results": [tr.to_dict() for tr in result.task_results], ... }  # :2652
out = config.phase_result_json(phase)                                                # :2655
tmp.write_text(json.dumps(payload, indent=2) + "\n")                                  # :2658
```

So a recovered task is persisted as `phase-N-result.json → task_results[].status == "pass_recovered"`, and when the resume code reloads that file it reconstructs `TaskStatus.PASS_RECOVERED`. (Aggregation already handles this correctly: master `executor.py:354` uses `r.status.is_success`. The resume code does NOT.)

---

## 3. PR resume/planner.py — 3 coupled sites (CONFIRMED)

Command: `git show origin/feat/sprint-auto-resume-v435:src/superclaude/cli/sprint/resume/planner.py`
`BoundaryTask.persisted_status` is populated via `_coerce_task_status(...)` which returns `TaskStatus | None` (`planner.py:330-336`) — so EVERY widened predicate must be None-safe.

**Site 3a — `rerun_task_ids` comprehension, `planner.py:160-163`:**
```python
plan.rerun_task_ids = [
    bt.task_id
    for bt in boundary
    if bt.persisted_status is not TaskStatus.PASS      # :163  ← a pass_recovered task lands here → re-run
]
```
A `PASS_RECOVERED` task `is not TaskStatus.PASS` → wrongly added to `rerun_task_ids` (completed work re-executed).

**Site 3b — `last_completed` selection, `planner.py:316-322` (in `_assign_roles`):**
```python
passed = sorted(
    (bt for bt in boundary if bt.persisted_status is TaskStatus.PASS),   # :318  ← excludes pass_recovered
    key=lambda bt: bt.task_id,
)
if passed:
    passed[-1].role = "last_completed"
```
A `PASS_RECOVERED` boundary task is excluded from `passed` → never eligible to be `last_completed` (the resume boundary anchor is mis-placed / dropped).

**Site 3c — `next_unfinished` selection, `planner.py:324-328` (in `_assign_roles`):**
```python
non_pass = sorted(
    (bt for bt in boundary if bt.persisted_status is not TaskStatus.PASS),  # :324  ← includes pass_recovered
    key=lambda bt: bt.task_id,
)
if non_pass:
    non_pass[0].role = "next_unfinished"
```
A `PASS_RECOVERED` task is wrongly counted as "not finished" → can become `next_unfinished`, mis-anchoring the resume point earlier than reality.

**PHASE-level check — DO NOT CHANGE.** `planner.py:380-385` `_is_pass_family` already uses `PhaseStatus(status_str).is_success`, and `PhaseStatus.is_success` is PASS-family-safe on both branches (master `models.py:426-432`; PR `models.py:315-322`). `_classify_phase` (`planner.py:338-371`) routes its result.json status through `_is_pass_family`, so the phase-level path is correct as-is. The bug is purely the TASK-level `TaskStatus.PASS` identity checks above.

**Synthetic boundary task — `planner.py:215-220` is fine as-is.** It constructs `BoundaryTask(persisted_status=TaskStatus.PASS, role="last_completed")` by hand (a literal PASS for a prior-tail). That literal is unaffected — it is an assignment, not a comparison.

### Proposed edits (planner.py)

| Line | Current | Proposed (None-safe PASS-family) |
|---|---|---|
| 163 | `if bt.persisted_status is not TaskStatus.PASS` | `if bt.persisted_status is None or not bt.persisted_status.is_success` |
| 318 | `(bt for bt in boundary if bt.persisted_status is TaskStatus.PASS)` | `(bt for bt in boundary if bt.persisted_status is not None and bt.persisted_status.is_success)` |
| 324 | `(bt for bt in boundary if bt.persisted_status is not TaskStatus.PASS)` | `(bt for bt in boundary if bt.persisted_status is None or not bt.persisted_status.is_success)` |

`is_success` is the post-merge PASS-family predicate (`PASS` or `PASS_RECOVERED`); the `is None` guard preserves the original behavior for junk/unparseable statuses (which `_coerce_task_status` maps to `None` → treated as "not done", same as today).

---

## 4. PR resume/integrity.py — 2 coupled sites (CONFIRMED, with one important nuance)

Command: `git show origin/feat/sprint-auto-resume-v435:src/superclaude/cli/sprint/resume/integrity.py`

**Site 4a — `signal_a_pass` (the persisted claim), `integrity.py:123`:**
```python
signal_a_pass = lc.persisted_status is TaskStatus.PASS     # :123  ← pass_recovered last_completed → signal_a False
```
`lc.persisted_status` is `TaskStatus | None` (a `BoundaryTask` field). A `PASS_RECOVERED` `last_completed` makes `signal_a_pass=False` → `validated = signal_a_pass and ... = False` → `lc.suspect = True` (`integrity.py:148-150`). A legitimately-recovered prior task gets flagged suspect, blocking/STOPping resume.

**Site 4b — `signal_b_pass` (re-derived from transcript), `integrity.py:127-129`:**
```python
derived = _classify_transcript(transcript)   # :127  → TaskStatus (non-Optional)
lc.derived_status = derived
signal_b_pass = derived is TaskStatus.PASS    # :129
```
**NUANCE — Signal B will not, by itself, regress from PASS_RECOVERED.** `_classify_transcript` (imported from `rerun_tasks`, master `rerun_tasks.py:547-593`) is typed `-> TaskStatus` (non-Optional) and **never returns `PASS_RECOVERED`** — it only emits `PASS / INCOMPLETE / FAIL_RECOVERABLE / FAIL_TERMINAL`. So widening `signal_b_pass` to `derived.is_success` is **behavior-neutral for `PASS_RECOVERED`** (the value can't appear). HOWEVER: a recovered task by definition exited non-zero with an error result-event, so `_classify_transcript` will classify its transcript as `FAIL_TERMINAL` (or `FAIL_RECOVERABLE` if transient signals present) — meaning **Signal B independently returns False for a genuinely-recovered task even after Signal A is fixed.** This is a DEEPER coupling than the 6 identity sites: the integrity double-check's Signal B cannot recognize a recovered task at all. The minimal merge-safety fix is the `is_success` widening on both signals (keeps them consistent and future-proof if `_classify_transcript` ever gains PASS_RECOVERED); but the task file should flag that integrity validation of a `PASS_RECOVERED` `last_completed` may still STOP via Signal B unless the integrity logic is taught that `PASS_RECOVERED` last_completed tasks are exempt from the transcript re-derivation (or Signal B is made PASS-family by treating a recovered persisted status as authoritative). **Mark: Signal-B-vs-recovered = needs design decision, not a one-line swap.**

### Proposed edits (integrity.py) — minimal None-safe widening

| Line | Current | Proposed |
|---|---|---|
| 123 | `signal_a_pass = lc.persisted_status is TaskStatus.PASS` | `signal_a_pass = lc.persisted_status is not None and lc.persisted_status.is_success` |
| 129 | `signal_b_pass = derived is TaskStatus.PASS` | `signal_b_pass = derived is not None and derived.is_success` |

(For 129, `derived` is currently non-Optional `TaskStatus`, so `derived is not None` is always True; including it costs nothing and is robust if the signature later widens. Behavior for `PASS_RECOVERED` is unchanged because `_classify_transcript` never yields it — see the nuance above.)

---

## 5. PR resume/drift.py — 1 coupled site (CONFIRMED)

Command: `git show origin/feat/sprint-auto-resume-v435:src/superclaude/cli/sprint/resume/drift.py`

**Site 5 — the COMPLETED-task-ID set, `drift.py:90-94`:**
```python
recorded_completed = {
    bt.task_id
    for bt in plan.boundary_tasks
    if bt.persisted_status is TaskStatus.PASS          # :93  ← excludes pass_recovered
}
```
`bt.persisted_status` is `TaskStatus | None`. A `PASS_RECOVERED` task is excluded from `recorded_completed`. Effect: drift's "a completed task ID was removed/renamed ⇒ material edit ⇒ low confidence/STOP" check (`drift.py:136-150`) no longer treats the recovered task as completed work that must survive — a tasklist edit that drops/renames that task would NOT be flagged material, weakening the drift safety guarantee for recovered tasks. (The `recorded_all` set at `drift.py:95-96` uses `is not None`, so it already includes `PASS_RECOVERED`; only the `recorded_completed` partition is wrong.)

### Proposed edit (drift.py)

| Line | Current | Proposed |
|---|---|---|
| 93 | `if bt.persisted_status is TaskStatus.PASS` | `if bt.persisted_status is not None and bt.persisted_status.is_success` |

---

## 6. Per-site predicate summary (the 6 resume sites)

"done" predicate (keep / completed): `bt.persisted_status is not None and bt.persisted_status.is_success`
"not done" predicate (rerun / next_unfinished): `bt.persisted_status is None or not bt.persisted_status.is_success`

| # | File:line | Role | Current | Proposed |
|---|---|---|---|---|
| 1 | planner.py:163 | rerun_task_ids ("not done") | `bt.persisted_status is not TaskStatus.PASS` | `bt.persisted_status is None or not bt.persisted_status.is_success` |
| 2 | planner.py:318 | last_completed ("done") | `bt.persisted_status is TaskStatus.PASS` | `bt.persisted_status is not None and bt.persisted_status.is_success` |
| 3 | planner.py:324 | next_unfinished ("not done") | `bt.persisted_status is not TaskStatus.PASS` | `bt.persisted_status is None or not bt.persisted_status.is_success` |
| 4 | integrity.py:123 | signal_a_pass ("done") | `lc.persisted_status is TaskStatus.PASS` | `lc.persisted_status is not None and lc.persisted_status.is_success` |
| 5 | integrity.py:129 | signal_b_pass ("done", `derived`) | `derived is TaskStatus.PASS` | `derived is not None and derived.is_success` (see §4 nuance) |
| 6 | drift.py:93 | recorded_completed ("done") | `bt.persisted_status is TaskStatus.PASS` | `bt.persisted_status is not None and bt.persisted_status.is_success` |

---

## 7. Codebase-wide sweep (other `TaskStatus.PASS` identity/eq checks)

Commands: per-file `git show <ref>:<path> | grep -nE "(is|is not|==|!=)\s+TaskStatus\.PASS\b ..."` across `cli/sprint/*.py` on BOTH branches.

**Inside the 6 resume sites (the regression — IN SCOPE):** planner.py:163,318,324; integrity.py:123,129; drift.py:93. (All resume/ files exist ONLY on the PR branch and are silently auto-merged — no conflict surfaces them.)

**OUTSIDE the 6 resume sites:**

| File:line | Branch(es) | Check | Verdict |
|---|---|---|---|
| `executor.py:324` (PR) / merged-conflict | PR has `r.status == TaskStatus.PASS`; **master already uses `r.status.is_success` (master `:354`)** | tasks_passed sum | **NOT silent — merge CONFLICTS here** (`git merge-tree` emits `<<<<<<<` markers at this line). Resolver MUST keep master's `is_success`. Out of scope for resume edits, but flag in the merge-resolution step. |
| `executor.py:1286` (PR) `all(r.status == TaskStatus.PASS ...)` | PR only; master replaced this region with `phase_report.status == "PASS"` (master `:1736`) | all_passed | Auto-resolves to master's form in the merged tree (merged line ~1740, no marker). Out of scope. |
| `handoff.py:34` `record.status != TaskStatus.PASS.value` | **master only** (handoff.py does NOT exist on PR branch) | resume-skip predicate `is_validated_success` | **Pre-existing master coupling, NOT introduced by this merge.** A `HandoffRecord` whose status is `"pass_recovered"` would be treated as "not a validated success" → not skipped on resume (re-run). Compares the `.value` string, not the enum. OUT OF SCOPE for this PR (master-side, independent of resume/), but worth a follow-up note: it has the same bug class. |
| `preflight.py:189` `task_status != TaskStatus.PASS`; `:206` `tr.status == TaskStatus.PASS` | **identical on both branches** | preflight all_passed / tasks_passed | OUT OF SCOPE. Preflight constructs its own `task_status` from a local classifier and NEVER assigns `PASS_RECOVERED`, so these can't misfire. Pre-existing, unchanged by merge. |
| `rerun_tasks.py:624` `status is not TaskStatus.PASS` | **identical on both branches** | failed-task discovery from transcripts | OUT OF SCOPE. Operates on `_classify_transcript` output, which never yields `PASS_RECOVERED`. Pre-existing. |
| `rerun_tasks.py:1231` (PR) / `:1192` (master) `tr.status is TaskStatus.PASS` | **identical on both branches** | last_pass tracking in a recovery view | Borderline. Operates on `view.task_results`; if those are ever loaded from persisted phase-N-result.json (which CAN carry `pass_recovered`), a recovered task would not set `last_pass`. **Pre-existing on master — NOT introduced by this PR**, so out of scope for the resume regression, but the same bug class. Flag as follow-up. |

**Conclusion:** Only the **6 resume/ sites** are *silently* introduced by this clean merge (no conflict, no failing PR-branch test). The executor.py `==PASS` lines are caught by a merge conflict / auto-resolve to master's safe form. handoff.py:34 and rerun_tasks.py:1231 are pre-existing master couplings of the same class (recommend follow-up, but not part of THIS PR's regression).

---

## 8. Test coverage gap (PR branch tests/sprint/test_resume.py)

Command: `git show origin/feat/sprint-auto-resume-v435:tests/sprint/test_resume.py`

- **No fixture anywhere in the PR sprint test suite uses `"pass_recovered"`.** Grep for `pass_recovered|PASS_RECOVERED` in `tests/sprint/test_resume.py` and `tests/sprint/test_resume_semantics.py` → **zero hits**. Every `task_results[].status` fixture uses only `"pass"`, `"incomplete"`, `"fail_recoverable"`.
- Therefore **no existing assertion encodes a `== PASS` expectation that the fix would break** — the proposed `is_success` widening keeps all current tests green. But there is also **zero regression coverage**: the bug is invisible to the current suite.
- **Recommended new test** (mirror `test_resume_task_level_recoverable`, `test_resume.py:108-140`): same fixture, but make `T03.01` status `"pass_recovered"` instead of `"pass"`, and assert `T03.01 NOT in plan.rerun_task_ids`, `roles["T03.01"] == "last_completed"`. Against the unfixed code this test FAILS (T03.01 wrongly enters `rerun_task_ids` and is denied `last_completed`); against the fixed code it passes — making it a true regression guard. A parallel integrity/drift fixture with a `pass_recovered` `last_completed` should assert `lc.suspect is False` (note the §4 Signal-B caveat may require additional integrity work for that assertion to hold).

---

## Summary

| File | Line | Current | Proposed | Effect if unfixed |
|---|---|---|---|---|
| resume/planner.py | 163 | `bt.persisted_status is not TaskStatus.PASS` | `bt.persisted_status is None or not bt.persisted_status.is_success` | A `pass_recovered` task is added to `rerun_task_ids` → completed work re-executed on resume. |
| resume/planner.py | 318 | `bt.persisted_status is TaskStatus.PASS` | `bt.persisted_status is not None and bt.persisted_status.is_success` | `pass_recovered` task excluded from `passed` → never chosen as `last_completed`; resume boundary mis-anchored. |
| resume/planner.py | 324 | `bt.persisted_status is not TaskStatus.PASS` | `bt.persisted_status is None or not bt.persisted_status.is_success` | `pass_recovered` task counted as unfinished → can become `next_unfinished`, anchoring resume too early. |
| resume/integrity.py | 123 | `lc.persisted_status is TaskStatus.PASS` | `lc.persisted_status is not None and lc.persisted_status.is_success` | `signal_a_pass=False` for a recovered `last_completed` → `lc.suspect=True` → integrity STOP on legitimate work. |
| resume/integrity.py | 129 | `derived is TaskStatus.PASS` | `derived is not None and derived.is_success` | Behavior-neutral for `pass_recovered` (`_classify_transcript` never yields it); see §4 — Signal B still fails a recovered task via FAIL_* classification (deeper, needs design). |
| resume/drift.py | 93 | `bt.persisted_status is TaskStatus.PASS` | `bt.persisted_status is not None and bt.persisted_status.is_success` | `pass_recovered` task omitted from `recorded_completed` → drift fails to flag removal/rename of completed recovered work as material. |

**Merge mechanics:** `git merge-tree --write-tree --name-only origin/master origin/feat/sprint-auto-resume-v435` → `models.py` AUTO-MERGES with NO conflict, keeping master's `PASS_RECOVERED` enum + PASS-family `is_success`. The 6 resume/ sites carry the PR branch's identity-against-PASS checks into the merged tree unchanged and uncontested. No PR-branch test produces `pass_recovered`, so the regression is fully silent until a real recovered task is persisted and a resume is attempted.

**Out-of-scope same-class couplings (follow-up, NOT this PR):** master `handoff.py:34` (`is_validated_success`) and master `rerun_tasks.py:1192` both compare task status to PASS by `==`/`is` and would also mishandle `pass_recovered`; they pre-date this PR and are independent of the resume regression.
