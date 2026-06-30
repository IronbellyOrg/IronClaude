# No-Edit Boundaries (Step 2.3)

**Date:** 2026-06-04
**Research basis:** `research/01-integrity-signalb-edit.md` (§3 derived_status, §4 executor recovery evidence, §5 `_classify_transcript` localization)
**Worktree files verified:** parent `src/superclaude/cli/sprint/models.py`, resume `src/superclaude/cli/sprint/resume/models.py`, `src/superclaude/cli/sprint/rerun_tasks.py`

## Reference-only surfaces (MUST NOT be edited)

### 1. Parent sprint `models.py` — `TaskStatus` (reference only)

Verified at `src/superclaude/cli/sprint/models.py:46–66`:

```python
class TaskStatus(Enum):
    PASS = "pass"                                     # :49
    PASS_RECOVERED = "pass_recovered"                 # :50  non-zero exit but evidence of success
    FAIL_TERMINAL = "fail"                            # :51
    FAIL_RECOVERABLE = "fail_recoverable"             # :52
    INCOMPLETE = "incomplete"                         # :53
    SKIPPED = "skipped"                               # :54

    @property
    def is_success(self) -> bool:                     # :56–58
        return self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)
```

**Why `derived is not None and derived.is_success` is SAFE for the non-recovered path:** `is_success` is True only for `PASS` and `PASS_RECOVERED`. On the `else` (non-recovered) branch the persisted status is, by construction, NOT `PASS_RECOVERED` (that case is caught by the `if`), and `_classify_transcript` can only ever return `PASS / FAIL_RECOVERABLE / FAIL_TERMINAL / INCOMPLETE` (never `PASS_RECOVERED` — see §3 below). Therefore on the non-recovered path `derived.is_success` is True **iff** `derived is TaskStatus.PASS` — behaviorally identical to the current `signal_b_pass = derived is TaskStatus.PASS`, with the `is not None` guard added for safety. The widening (Opt-1 future-proofing, guardrail #2) introduces no behavior change today. **No edit to `models.py` is required.**

### 2. Resume `models.py` — `BoundaryTask.derived_status` (reference only)

Verified at `src/superclaude/cli/sprint/resume/models.py:37–58`:

```python
    persisted_status: TaskStatus | None = None  # Signal A   (:48)
    derived_status: TaskStatus | None = None    # Signal B   (:49)
```

**Why `lc.derived_status = TaskStatus.PASS_RECOVERED` is report-visible:** the `derived_status` field is rendered through the operator-facing report paths — `_blocking_reasons` interpolates `derived={s.derived_status}` (integrity.py:421–428) and the CLI suspect/blocking surfaces print it (commands.py:554–577, per research/01 §3). Assigning `PASS_RECOVERED` (rather than a fabricated `PASS`) makes the report honestly show that Signal B was satisfied by executor-recovery evidence, not a clean-PASS transcript. **No edit to resume `models.py` is required** — the field already exists.

### 3. `rerun_tasks.py` — `_classify_transcript` (reference only)

Verified at `src/superclaude/cli/sprint/rerun_tasks.py:547–593`. It returns only `PASS` (clean result + output tokens), `FAIL_RECOVERABLE` (errored + transient signal such as `api_retry` / `ConnectionRefused` / zero output tokens), `FAIL_TERMINAL` (errored, non-transient), or `INCOMPLETE` (no terminal result event). It **never** returns `PASS_RECOVERED`.

**Why `_classify_transcript` must not be edited (Opt-2b rejected):** it is shared. Besides the integrity gate, it is consumed by `discover_failed_tasks_from_transcripts` (rerun_tasks.py:596–625), which drives rerun-task discovery. Widening the classifier to emit/accept `PASS_RECOVERED` (Opt-2b) would spill into rerun discovery and change which tasks are re-run — an out-of-scope blast radius. Opt-2a keeps the entire change inside `integrity.py` by branching on `lc.persisted_status` BEFORE calling the classifier. **No edit to `rerun_tasks.py` is required.**

## Executor recovery evidence (context for why the exemption is sound)

`PASS_RECOVERED` is not blind trust in persisted status: the executor writes it only when BOTH `detect_error_max_turns(task_output_path)` (terminal NDJSON line is `error_max_turns`) AND `_task_completed_before_overrun(task_output_path)` (completion evidence appears before that terminal line) are true (executor.py:997–1011 / 2321–2387, per research/01 §4). So substituting the recovery determination for the clean-PASS classifier on the recovered seam swaps in the only transcript-based check that *can* validate a recovered tail — not a weakening of the gate.

## Why Opt-2b is rejected (summary)

Opt-2b would modify the shared `_classify_transcript`, spilling into `discover_failed_tasks_from_transcripts` (rerun_tasks.py:596–625). Opt-2a confines the change to `integrity.py`'s Signal B branch, preserves `_classify_transcript` for every other caller, and keeps `artifacts_ok` gating recovered seams. Opt-2a is selected (adversarial base-selection, research/01 §2).

## Net no-edit rule

Modify **only** `src/superclaude/cli/sprint/resume/integrity.py` (Signal B block) and `tests/sprint/test_resume.py`. Leave **unmodified**: parent `models.py`, resume `models.py`, `rerun_tasks.py` (including `_classify_transcript`), and the executor.
