# Source-Site Inventory — Step 2.1

**Date:** 2026-06-05
**Worktree root:** `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered`
**HEAD:** `7dd3f9bd` (== `origin/master`)
**Seed evidence:** `research/01-rerun-handoff-coupling-sites.md:14-239`

## Verified coupling sites (current worktree line numbers)

| Site ID | Severity | Worktree File | Function | Current Predicate | Current Line | Required Replacement | Data Type | Verification Notes |
|---------|----------|---------------|----------|-------------------|--------------|----------------------|-----------|--------------------|
| S1 | **CRITICAL** | `src/superclaude/cli/sprint/rerun_tasks.py` | `_rerun_targets_passed` | `all(status_by_id.get(t) == "pass" for t in targets)` | **1216** | Coerce each raw status string → `TaskStatus` via a local None/invalid-safe helper, return `status.is_success`; preserve `bool(targets)` guard | **Serialized string** (`entry.get("status")` from JSON, line 1215) | Merge-back skipped for `pass_recovered` rerun targets. Bug present and unchanged on origin/master. |
| S2 | **HIGH** | `src/superclaude/cli/sprint/handoff.py` | `is_validated_success` | `if record.status != TaskStatus.PASS.value:` → `return False` | **34** | Coerce `record.status` → `TaskStatus` in None/invalid-safe `try`, check `.is_success`; KEEP `GateOutcome(record.gate_outcome).is_success` requirement (lines 36-40) | **Serialized string** (`record.status` is the enum `.value` per docstring lines 31-32) | Validated-success resume-skip wrongly False for `pass_recovered`+good gate. Bug present and unchanged. |
| S3 | **LOW** | `src/superclaude/cli/sprint/rerun_tasks.py` | `_print_investigation_summary` | `if tr.status is TaskStatus.PASS:` | **1231** | Replace identity check with success-family predicate. **Carried correction F2 [LOW]:** prefer the None-safe local helper from S1 (`_is_success_task_status(tr.status)`) over bare `tr.status.is_success`, so a `None` status can never raise `AttributeError` | **Enum** (`tr.status` is a `TaskStatus` from `_load_phase_result_view` → `from_dict`) | Display-only `last PASS task` pointer; `pass_recovered` never updates it. Bug present and unchanged. |

## Fix idiom (gold standard)

`TaskStatus.is_success` (`src/superclaude/cli/sprint/models.py:57-58`):
```python
def is_success(self) -> bool:
    return self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)
```
This is already the module's established idiom for the main rerun path (`rerun_tasks.py:456` uses `tr.status.is_success`); S1 and S3 are the two stragglers on the JSON-string / identity-check paths. The fix aligns them to the established `is_success` semantics.

## ⚠️ INPUT-DRIFT FINDING (research premise now stale — descriptive only, fix unaffected)

The task (Step 2.1) instructs the inventory to "explicitly state that `src/superclaude/cli/sprint/resume/planner.py` and `_coerce_task_status` do not exist on origin/master and must not be imported."

**This premise is STALE on the current `origin/master` (HEAD `7dd3f9bd`):**

- `src/superclaude/cli/sprint/resume/planner.py` **EXISTS**.
- `_coerce_task_status` **EXISTS** at `resume/planner.py:339` — but as a class-private `@staticmethod` (`def _coerce_task_status(value: object) -> TaskStatus | None`), not a module-level function.

**Why the research said otherwise:** research/01 was authored against an earlier tree state (the primary checkout `feature/prd-spec-flag`, which predates the PR #124 `resume/` merge into master). `origin/master` has since advanced.

**Impact assessment: NONE on the fix.**
1. All three target bugs (S1/S2/S3) still exist byte-for-byte on current `origin/master` — the fix is still valid and needed.
2. The required **action** (add a local None/invalid-safe helper; do NOT import the resume planner helper) remains correct because `planner._coerce_task_status` is a **class-private staticmethod** — importing it would couple `rerun_tasks`/`handoff` to resume-planner class internals. A local module-level helper is the cleaner, self-contained choice and matches the task's intent.
3. The only thing that changed is this descriptive claim. The inventory records reality truthfully (per the task's own "fabricate no sites / no fabrication" guardrail) rather than asserting a falsehood.

**Decision (carried into Phase 3):** Create a local module-level helper in `rerun_tasks.py` (and reuse the same None/invalid-safe pattern in `handoff.py`). Do NOT import `resume.planner._coerce_task_status`. This is surfaced to the operator and will be independently checked by the Phase 2 discovery QA gate (Step 2.3).

## Absent-symbol guard (corrected)

- ❌ Original research claim "`resume/planner.py` does not exist" — **FALSE on current origin/master** (see drift finding above).
- ✅ A **module-level** `_coerce_task_status` in `rerun_tasks.py` / `handoff.py` does NOT exist yet — the fix creates it locally.
- ✅ No fabricated sites beyond the three verified above.
