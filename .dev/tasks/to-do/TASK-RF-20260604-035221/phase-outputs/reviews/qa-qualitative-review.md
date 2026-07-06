# QA Report — Task Qualitative Review (Operational)

**Topic:** TASK-RF-20260604-035221 — PR #124 conflict resolution + PASS_RECOVERED resume coupling
**Date:** 2026-06-04
**Phase:** task-qualitative (rf-qa-qualitative, adversarial, fix_authorization: true)
**Agent verdict:** FAIL (1 CRITICAL, 2 IMPORTANT) — see scope adjudication below.

> The rf-qa-qualitative agent declined to write this file itself (perceived a no-write harness
> instruction) and returned findings inline; the executor persisted them here to preserve the
> evidence trail, then adjudicated scope (below).

---

## Agent findings (verbatim severity)

### Issue #1 — CRITICAL — `rerun_tasks.py:1204-1216` `_rerun_targets_passed`
`_rerun_targets_passed` gates rerun merge-back on strict string equality
`status_by_id.get(t) == "pass"`. A task-level auto-resume rerun TARGET that completes as
`TaskStatus.PASS_RECOVERED` serializes to `"pass_recovered"` (`models.py:190-207`), so
`_rerun_targets_passed` returns False → merge-back is blocked despite success-family semantics.
Consumed via `commands.py:323-325,509-529` (`_dispatch_resume_rerun` → `run_rerun_tasks(merge_back=True)`)
and evaluated at `rerun_tasks.py:1409-1413`. Same bug class as the 6 resume sites.

### Issue #2 — IMPORTANT — task-file bookkeeping
At QA time the task frontmatter still read `status: "🟠 Doing"`, `completion_date: ""`, post-completion
items unchecked, Task Summary placeholders unfilled.

### Issue #3 — IMPORTANT — research follow-up enumeration gap
research/02 §7 enumerated `handoff.py:34` and `rerun_tasks.py:1231` (`last_pass`) as out-of-scope
same-class couplings but MISSED `rerun_tasks.py:1216` (`_rerun_targets_passed`), which is
operationally more severe because it gates rerun merge-back.

### PASS items (10/15)
Command dry-run (`sprint run --help` renders all options; `pytest test_resume.py` 23 passed),
convention compliance, intra-phase simulation, function-signature verification (run() params bind +
are consumed), module context, test validity (new test exercises planner/drift/Signal-A genuinely),
None-path coverage, kwarg sequencing, existence claims, template cross-refs.

---

## Executor scope adjudication

**Issue #1 + #3 (rerun_tasks.py `_rerun_targets_passed`): REAL but OUT OF SCOPE for this task.**

Verified independently (zero-trust): the `_rerun_targets_passed` body and its
`status_by_id.get(t) == "pass"` predicate are **BYTE-IDENTICAL on `origin/master`** (master line 1177;
worktree line 1216). It is a **pre-existing master coupling, NOT introduced or modified by PR #124.**
Evidence:
```
$ diff <(git show origin/master:.../rerun_tasks.py | grep -A14 'def _rerun_targets_passed') \
       <(grep -A14 'def _rerun_targets_passed' .../rerun_tasks.py)
>>> IDENTICAL on master (PRE-EXISTING, out of scope)
```
It is NOT one of this task's deliverables:
- It is NOT a conflict hunk (Deliverable A = CHANGELOG/commands.py/executor.py only).
- It is NOT one of the 6 `resume/` sites (Deliverable B = planner ×3, drift ×1, integrity ×2 — all in
  `resume/`).
- It is in `rerun_tasks.py`, the exact module research §7 + the task's Out-of-Scope Follow-Up section
  deliberately EXCLUDE as pre-existing same-bug-class couplings ("record but DO NOT fix here").

Per CLAUDE.md scope discipline (build exactly what's asked; no speculative additions) and the task's
F-rules (execute as written; no improvisation), this is **recorded as a HIGH-priority follow-up**, not
fixed in this task. Whether to fold the fix into PR #124 before merge is a **scope decision for the
user** (analogous to the Signal-B `needs_human_decision` gate). The research follow-up enumeration is
amended to add `rerun_tasks.py:1216` (Issue #3 addressed).

**Issue #2 (bookkeeping): in-flight, not a defect.** The QA ran during post-completion validation,
BEFORE the final post-completion bookkeeping items (Task Summary + status→Done). Those items are being
completed now.

## Net effect on the task's SCOPED deliverables

The qualitative FAIL does NOT impugn Deliverable A (4 conflict hunks resolved, mergeable PR) or
Deliverable B (6 resume sites widened, Signal B correctly gated, RED→GREEN test). Those remain
verified PASS (structural rf-qa PG.1; suite 1154 green; both ruff gates clean). The CRITICAL is a
correctly-out-of-scope pre-existing coupling escalated to the user as a follow-up.
