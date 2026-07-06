# Research: BoundaryIntegrityGate Signal B Opt-2a Edit
**Topic type:** File Inventory + Data Flow
**Scope:** `src/superclaude/cli/sprint/resume/integrity.py`, resume models/report surfacing, executor PASS_RECOVERED evidence, `_classify_transcript` localization check
**Status:** Complete
**Date:** 2026-06-04

---

## 1. Source tree note and full `_validate_last_completed` method

The requested path `src/superclaude/cli/sprint/resume/integrity.py` is not present in the currently checked-out branch, but it is present on `origin/master` at commit `02949fb3cee8b456df69c9b1e2eac59c3f51c6c6`. I extracted the `origin/master` file content to `/tmp/ironclaude-origin-master-sprint/resume/integrity.py`; line numbers below correspond to the `origin/master` source file `src/superclaude/cli/sprint/resume/integrity.py`.

Full `_validate_last_completed` method, `src/superclaude/cli/sprint/resume/integrity.py:92-154`:

```python
    def _validate_last_completed(
        self, plan: ResumePlan, phase_file: Path | None, results_dir: Path
    ) -> tuple[bool, list[BoundaryTask], BoundaryTask | None]:
        """Doubly-validate the last-completed task (Signal A ∧ Signal B ∧ artifacts).

        Signal A = persisted status (claim). Signal B = independent re-derivation
        from the task transcript. ``artifacts_ok`` = every declared deliverable for
        the task exists on disk. A PASS claim is RE-CHECKED, never trusted (R1).
        Vacuously True when there is no last-completed task (PHASE granularity /
        hard crash) — the deterministic checkpoint/deliverable checks carry the gate.
        """
        lc = next(
            (bt for bt in plan.boundary_tasks if bt.role == "last_completed"), None
        )
        if lc is None:
            return True, [], None

        from superclaude.cli.sprint.rerun_tasks import (
            _classify_transcript,
            _declared_deliverables,
        )

        # F-4/CG-3: a prior-phase-tail last_completed (emitted by the planner on a
        # PHASE hard crash) carries its OWNING phase in ``lc.phase``. Resolve BOTH
        # the transcript and the declared deliverables under that phase, not the
        # interrupted phase. ``lc.phase is None`` for ordinary interrupted-phase
        # boundary tasks ⇒ fall back to ``plan.interrupted_phase`` / the passed
        # ``phase_file`` (backward-compatible).
        lc_phase = lc.phase if lc.phase is not None else plan.interrupted_phase

        # Signal A — the persisted claim.
        signal_a_pass = (
            lc.persisted_status is not None and lc.persisted_status.is_success
        )

        # Signal B — independent re-derivation from the transcript (under lc_phase).
        transcript = self._read_transcript(results_dir, lc_phase, lc.task_id)
        derived = _classify_transcript(transcript)
        lc.derived_status = derived
        signal_b_pass = derived is TaskStatus.PASS

        # Artifacts — every declared deliverable must exist. Resolve the tasklist
        # for lc's OWN phase (the prior phase for a hard-crash prior-tail). If we
        # kept reading the interrupted phase's tasklist (``phase_file``), a prior
        # tail's deliverables would be read from the WRONG tasklist (the
        # interrupted phase declares none for it), ``_declared_deliverables``
        # would return [], ``all([])`` would be vacuously True, and the negative
        # case could never STOP. So resolve lc's phase file explicitly.
        if lc.phase is None or lc.phase == plan.interrupted_phase:
            lc_phase_file = phase_file
        else:
            lc_phase_file = self._phase_file(plan, lc.phase)
        artifacts_ok = True
        if lc_phase_file is not None:
            deliverables = _declared_deliverables(lc_phase_file, lc.task_id)
            artifacts_ok = all(self._exists(p) for p in deliverables)
        lc.artifacts_present = artifacts_ok

        validated = signal_a_pass and signal_b_pass and artifacts_ok
        if not validated:
            lc.suspect = True
            return False, [lc], lc
        return True, [], lc
```

Required relocated blocks:

- Signal A, `src/superclaude/cli/sprint/resume/integrity.py:122-125`:

```python
        # Signal A — the persisted claim.
        signal_a_pass = (
            lc.persisted_status is not None and lc.persisted_status.is_success
        )
```

- Signal B, `src/superclaude/cli/sprint/resume/integrity.py:127-131`:

```python
        # Signal B — independent re-derivation from the transcript (under lc_phase).
        transcript = self._read_transcript(results_dir, lc_phase, lc.task_id)
        derived = _classify_transcript(transcript)
        lc.derived_status = derived
        signal_b_pass = derived is TaskStatus.PASS
```

- Verdict, `src/superclaude/cli/sprint/resume/integrity.py:150-154`:

```python
        validated = signal_a_pass and signal_b_pass and artifacts_ok
        if not validated:
            lc.suspect = True
            return False, [lc], lc
        return True, [], lc
```

## 2. Exact Opt-2a edit from design spec

Design source read: `.dev/tasks/to-do/TASK-RF-20260604-035221/phase-outputs/oq1-adversarial/adversarial/base-selection.md`.

Load-bearing recommendation, `.dev/tasks/to-do/TASK-RF-20260604-035221/phase-outputs/oq1-adversarial/adversarial/base-selection.md:24-27`:

```markdown
Opt-2a fixes this with the SAME safety posture and a contained blast radius:
- Trusts the executor's `PASS_RECOVERED` determination for Signal B **only** — and that determination is itself transcript-evidence-based (`detect_error_max_turns` + `_task_completed_before_overrun` require completion evidence before the overrun, executor.py:997-1011 / 2321-2330). So this is NOT "blind trust in persisted status"; it substitutes the only transcript-based check that *can* validate a recovered tail for the one that structurally cannot.
- Preserves a genuine **2-signal double-check** for recovered tasks: persisted-status (Signal A) ∧ artifact-existence (`artifacts_ok`). The persisted claim alone is still insufficient.
- Does **NOT** touch the shared `_classify_transcript` (Opt-2b is rejected — it would spill into `discover_failed_tasks_from_transcripts`, rerun_tasks.py:596-625). Blast radius stays in `integrity.py`.
```

Implementation guardrails, `.dev/tasks/to-do/TASK-RF-20260604-035221/phase-outputs/oq1-adversarial/adversarial/base-selection.md:29-33`:

```markdown
**Implementation guardrails (both advocates surfaced these — bake into the fix):**
1. Guard the exemption narrowly: `if lc.persisted_status is TaskStatus.PASS_RECOVERED: signal_b_pass = True` — ordinary `PASS` MUST still be transcript-rechecked.
2. Keep Opt-1's `derived is not None and derived.is_success` widening as future-proofing for the non-recovered path.
3. Transparency: set `lc.derived_status = TaskStatus.PASS_RECOVERED` (or annotate) so the report shows Signal B was satisfied by executor-recovery evidence, not a clean PASS transcript.
4. Tests (mandatory): (a) recovered `last_completed` + present artifacts → `validated_last is True`; (b) negative — an over-claimed/missing-artifact recovered seam still STOPs; (c) ordinary false PASS claim still fails Signal B (no over-broad trust).
```

Proposed final localized code block for `src/superclaude/cli/sprint/resume/integrity.py:_validate_last_completed`:

```python
        # Signal B — independent re-derivation from the transcript (under lc_phase).
        transcript = self._read_transcript(results_dir, lc_phase, lc.task_id)
        if lc.persisted_status is TaskStatus.PASS_RECOVERED:
            # PASS_RECOVERED is already transcript-evidence-based in the executor
            # (error_max_turns after completion evidence). Preserve that recovery
            # basis for report transparency instead of forcing the clean-PASS
            # classifier path, which structurally cannot emit PASS_RECOVERED.
            derived = TaskStatus.PASS_RECOVERED
            lc.derived_status = derived
            signal_b_pass = True
        else:
            derived = _classify_transcript(transcript)
            lc.derived_status = derived
            signal_b_pass = derived is not None and derived.is_success

        # Artifacts — every declared deliverable must exist. Resolve the tasklist
        # for lc's OWN phase (the prior phase for a hard-crash prior-tail). If we
        # kept reading the interrupted phase's tasklist (``phase_file``), a prior
        # tail's deliverables would be read from the WRONG tasklist (the
        # interrupted phase declares none for it), ``_declared_deliverables``
        # would return [], ``all([])`` would be vacuously True, and the negative
        # case could never STOP. So resolve lc's phase file explicitly.
        if lc.phase is None or lc.phase == plan.interrupted_phase:
            lc_phase_file = phase_file
        else:
            lc_phase_file = self._phase_file(plan, lc.phase)
        artifacts_ok = True
        if lc_phase_file is not None:
            deliverables = _declared_deliverables(lc_phase_file, lc.task_id)
            artifacts_ok = all(self._exists(p) for p in deliverables)
        lc.artifacts_present = artifacts_ok

        validated = signal_a_pass and signal_b_pass and artifacts_ok
        if not validated:
            lc.suspect = True
            return False, [lc], lc
        return True, [], lc
```

Notes on the proposed code:

- The PASS_RECOVERED exemption is guarded to `lc.persisted_status is TaskStatus.PASS_RECOVERED` only. Ordinary `PASS` remains in the transcript-rechecked `else` branch.
- The non-recovered branch uses Opt-1 widening: `derived is not None and derived.is_success`.
- For transparency, the recovered branch assigns `lc.derived_status = TaskStatus.PASS_RECOVERED` via `derived = TaskStatus.PASS_RECOVERED`; reports therefore show the recovered basis rather than falsely showing a clean `TaskStatus.PASS` transcript derivation.
- `artifacts_ok` and `validated = signal_a_pass and signal_b_pass and artifacts_ok` remain unchanged, so recovered persisted status alone cannot pass the gate when declared artifacts are missing.

## 3. `BoundaryTask.derived_status` exists and is surfaced

`BoundaryTask.derived_status` exists in the resume dataclass, `src/superclaude/cli/sprint/resume/models.py:37-58`:

```python
@dataclass
class BoundaryTask:
    """A single task on the resume seam of the interrupted phase.

    ``persisted_status`` is Signal A (from ``phase-N-result.json``);
    ``derived_status`` is Signal B (independent re-derivation via
    ``_classify_transcript``). ``suspect`` is set when A/B disagree OR declared
    artifacts are missing.
    """

    task_id: str
    persisted_status: TaskStatus | None = None  # Signal A
    derived_status: TaskStatus | None = None  # Signal B
    artifacts_present: bool = False  # declared deliverables/checkpoints exist
    role: str = "pending"  # "last_completed" | "next_unfinished" | "pending"
    suspect: bool = False  # A/B disagree OR artifacts missing
    # The phase this boundary task belongs to. None ⇒ the interrupted phase
    # (default, backward-compatible). Set to a PRIOR phase number when the planner
    # emits a prior-phase-tail `last_completed` on a PHASE hard crash, so the
    # integrity gate resolves the transcript/deliverables under `phase-{phase}-...`
    # rather than the interrupted phase (F-4/CG-3).
    phase: int | None = None
```

`BoundaryReport.blocking_reasons` carries the text report surface, `src/superclaude/cli/sprint/resume/models.py:92-115`:

```python
@dataclass
class BoundaryReport:
    """Integrity-gate verdict for the resume seam.

    ``passed`` is a pure function of deterministic signals (validated_last, no
    unresolved suspects, partial work quarantined-or-accepted). ``coherence_warnings``
    are advisory Haiku flags surfaced for the operator and are NOT part of ``passed``
    (NFR-3).
    """

    validated_last: bool = False
    suspects: list[BoundaryTask] = field(default_factory=list)
    quarantined: dict[Path, Path] = field(
        default_factory=dict
    )  # canonical → quarantine copy
    passed: bool = False  # gate verdict (FR-2.4) — deterministic only
    blocking_reasons: list[str] = field(default_factory=list)
    coherence_warnings: list[tuple[BoundaryTask, str]] = field(
        default_factory=list
    )  # advisory; NOT part of `passed` (NFR-3)
    # report-only suspect paths (FR-2.2 / §4(b) "always"); populated regardless of
```

`BoundaryIntegrityGate.run` writes the blocking reasons when the gate stops, `src/superclaude/cli/sprint/resume/integrity.py:80-83`:

```python
        report.passed = self._verdict(report, accept_suspect=accept_suspect)
        if not report.passed:
            report.blocking_reasons = self._blocking_reasons(report)
```

`_blocking_reasons` includes `derived_status` in suspect details, `src/superclaude/cli/sprint/resume/integrity.py:411-428`:

```python
    @staticmethod
    def _blocking_reasons(report: BoundaryReport) -> list[str]:
        """Explain the hard integrity failure (last-completed over-claim)."""
        reasons: list[str] = []
        if not report.validated_last:
            reasons.append(
                "Last-completed task failed double-validation (persisted status, "
                "transcript re-derivation, or declared artifacts disagree) — its "
                "claimed completion is not trustworthy. Re-run with --start to "
                "re-execute the phase, or --fresh to discard prior state."
            )
            for s in report.suspects:
                if s.role == "last_completed":
                    reasons.append(
                        f"Suspect task {s.task_id}: persisted={s.persisted_status}, "
                        f"derived={s.derived_status}, "
                        f"artifacts_present={s.artifacts_present}."
                    )
        return reasons
```

CLI surfacing confirms both suspect rows and blocking reasons print `derived_status`, `src/superclaude/cli/sprint/commands.py:554-577`:

```python
    if decision.report is not None:
        r = decision.report
        click.echo(
            f"  integrity gate:   {'PASS' if r.passed else 'STOP'} "
            f"(last-completed validated: {r.validated_last})"
        )
        for s in r.suspects:
            click.echo(
                f"    suspect: {s.task_id} [{s.role}] "
                f"persisted={s.persisted_status} derived={s.derived_status}"
            )
        for task, reason in r.coherence_warnings:
            click.echo(f"    coherence (advisory): {task.task_id}: {reason}")
        # F-2/CG-1: surface the half-written partial-work paths on the report-only
        # path (design §4(b) "report suspect paths in BoundaryReport (always)").
        # ``partial_paths`` is populated regardless of quarantine opt-in, so these
        # print on the dry-run and interactive-confirm paths where ``quarantined``
        # is empty.
        for p in r.partial_paths:
            click.echo(f"    partial work (uncommitted): {p}")
        for canonical, copy in r.quarantined.items():
            click.echo(f"    quarantined: {canonical} -> {copy}")
        for reason in r.blocking_reasons:
            click.echo(f"    blocking: {reason}")
```

Conclusion: assigning `lc.derived_status = TaskStatus.PASS_RECOVERED` for the exempted recovered path is meaningful because both suspect display and blocking reason strings expose `derived_status` directly.

## 4. Executor PASS_RECOVERED determination is transcript-based

The executor imports `detect_error_max_turns` from the output monitor, `src/superclaude/cli/sprint/executor.py:44`:

```python
from .monitor import OutputMonitor, detect_error_max_turns, detect_prompt_too_long
```

`detect_error_max_turns` itself reads the output transcript and checks the last non-empty NDJSON line for the `error_max_turns` result subtype, `src/superclaude/cli/sprint/monitor.py:37-61`:

```python
def detect_error_max_turns(output_path: Path) -> bool:
    """Check if the last NDJSON line indicates budget exhaustion.

    Scans the last non-empty line of the output file for the
    ``"subtype":"error_max_turns"`` pattern, which signals that a
    subprocess exhausted its turn budget.

    Returns True if error_max_turns is detected, False otherwise.
    """
    try:
        content = output_path.read_text(errors="replace")
    except (FileNotFoundError, OSError):
        return False

    if not content.strip():
        return False

    # Get last non-empty line
    lines = content.strip().splitlines()
    for line in reversed(lines):
        line = line.strip()
        if line:
            return bool(ERROR_MAX_TURNS_PATTERN.search(line))

    return False
```

The task status recovery condition is in the executor, `src/superclaude/cli/sprint/executor.py:997-1011`:

```python
    # Determine task status from exit code.
    task_output_path = config.task_output_file(phase, task)
    if exit_code == 0:
        status = TaskStatus.PASS
    elif exit_code == 124:
        status = TaskStatus.INCOMPLETE
    elif detect_error_max_turns(task_output_path) and _task_completed_before_overrun(
        task_output_path
    ):
        # Budget overrun (error_max_turns) AFTER completing substantive work:
        # the task emitted a successful result before the terminal overrun
        # envelope, so recover instead of failing the phase. Completion
        # evidence outranks the transient-failure classification below.
        # (#121, ported into the shared helper so BOTH K=1 and K>1 recover.)
        status = TaskStatus.PASS_RECOVERED
```

The helper docstring defines the transcript basis and the pre-terminal completion evidence requirement, `src/superclaude/cli/sprint/executor.py:2321-2330`:

```python
def _task_completed_before_overrun(output_path: Path) -> bool:
    """Return True iff the per-task NDJSON stream shows completion evidence
    BEFORE its terminal ``error_max_turns`` envelope.

    This is the completion-evidence gate for per-task recovery. A task that
    overran *after* finishing its substantive work shows completion evidence in
    the lines preceding the terminal ``{"type":"result","subtype":"error_max_turns"}``
    envelope; a task that overran *without* finishing does not. Recovery is
    GATED on this — ``error_max_turns`` alone is NOT sufficient (that would mask
    a task that overran without finishing).
```

The helper explicitly scans transcript lines before the terminal overrun line for completion evidence, `src/superclaude/cli/sprint/executor.py:2349-2387`:

```python
    This helper is only meaningful when called for a stream whose terminal line
    is the ``error_max_turns`` envelope (i.e. ``detect_error_max_turns`` is
    already True); it scans the lines strictly BEFORE that terminal line so the
    error line itself can never be mistaken for completion evidence.

    Returns False when the file is missing/unreadable/empty, or when neither
    class of completion evidence appears before the terminal
    ``error_max_turns`` line. Reads the file defensively (mirroring
    ``detect_error_max_turns``); performs no network or subprocess calls.
    """
    try:
        content = output_path.read_text(errors="replace")
    except (FileNotFoundError, OSError):
        return False

    if not content.strip():
        return False

    lines = [ln.strip() for ln in content.strip().splitlines() if ln.strip()]
    if not lines:
        return False

    # Class 1: a structured success/task_complete envelope anywhere in the
    # lines strictly before the terminal (last non-empty) line, which is the
    # error_max_turns envelope on the gated-recovery path.
    for line in lines[:-1]:
        if _TASK_SUCCESS_ENVELOPE_PATTERN.search(line):
            return True

    # Class 2: a strong completion verdict in the TAIL (last
    # ``_TASK_TAIL_COMPLETION_WINDOW`` pre-terminal lines). Tail-scoped on
    # purpose — a task that overran mid-work does not end on a completion
    # verdict, while one that overran after completing does. This recovers the
    # artifact-only overrun (no success envelope) that Class 1 misses.
    for line in lines[:-1][-_TASK_TAIL_COMPLETION_WINDOW:]:
        if _TASK_TAIL_COMPLETION_PATTERN.search(line):
            return True

    return False
```

Data-flow conclusion: executor `PASS_RECOVERED` is not a blind persisted status. It is written only when both transcript checks pass: the terminal NDJSON line is `error_max_turns`, and pre-terminal transcript content contains completion evidence.

## 5. `_classify_transcript` remains untouched; Opt-2a is localized to `integrity.py`

Current `_classify_transcript`, `src/superclaude/cli/sprint/rerun_tasks.py:547-593`:

```python
def _classify_transcript(text: str) -> TaskStatus:
    """Apply the TDD §T6 (lines 122-126) classification to one transcript body.

    PASS = clean result with output; FAIL_RECOVERABLE = errored with a transient
    signal (``api_retry`` / ``ConnectionRefused`` / zero output tokens);
    FAIL_TERMINAL = errored with none of those (a genuine failure); INCOMPLETE =
    no terminal result event (killed / truncated mid-task).
    """
    result_event: Optional[dict] = None
    total_output_tokens = 0
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        if not isinstance(event, dict):
            continue
        message = event.get("message")
        usage = message.get("usage") if isinstance(message, dict) else None
        if usage is None:
            usage = event.get("usage")
        if isinstance(usage, dict) and isinstance(usage.get("output_tokens"), int):
            total_output_tokens += usage["output_tokens"]
        if event.get("type") == "result":
            result_event = event

    if result_event is None:
        return TaskStatus.INCOMPLETE  # killed / truncated — no terminal result

    subtype = str(result_event.get("subtype", ""))
    is_error = bool(result_event.get("is_error")) or subtype.startswith("error")

    if not is_error and total_output_tokens > 0:
        return TaskStatus.PASS

    transient = (
        "api_retry" in text or "ConnectionRefused" in text or total_output_tokens == 0
    )
    if is_error and transient:
        return TaskStatus.FAIL_RECOVERABLE
    if is_error:
        return TaskStatus.FAIL_TERMINAL
    # Not errored but produced no output — treat as incomplete (empty run).
    return TaskStatus.INCOMPLETE
```

`discover_failed_tasks_from_transcripts` consumes `_classify_transcript`, `src/superclaude/cli/sprint/rerun_tasks.py:596-625`:

```python
def discover_failed_tasks_from_transcripts(
    results_dir: Path, phase: int
) -> list[tuple[str, TaskStatus]]:
    """Legacy fallback: classify a phase's tasks from on-disk transcripts.

    Used by ``run_rerun_tasks`` when ``phase-N-result.json`` is missing OR has an
    empty ``task_results`` (pre-v4.3.0 sprints; TDD §T6 line 130). Enumerates the
    ``phase-N-task-T<PP>.<TT>-output.txt`` transcripts (only ``-output.txt`` — the
    ``-errors.txt`` sibling carries no terminal result line and would duplicate
    the task ID), parses each terminal result event, and returns the non-PASS
    tasks as ``(task_id, TaskStatus)`` — the rerun candidates. Unreadable
    transcripts are skipped (researcher 2 §1.5), never fatal.
    """
    failed: list[tuple[str, TaskStatus]] = []
    try:
        transcripts = sorted(results_dir.glob(f"phase-{phase}-task-T*-output.txt"))
    except OSError:
        return failed

    for path in transcripts:
        id_match = _TASK_ID_FROM_TRANSCRIPT.search(str(path))
        if id_match is None:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        status = _classify_transcript(text)
        if status is not TaskStatus.PASS:
            failed.append((id_match.group(1), status))
```

Conclusion: the Opt-2a fix does not require touching `_classify_transcript`. It should be left untouched. The change is fully localized to `src/superclaude/cli/sprint/resume/integrity.py`, where only `PASS_RECOVERED` last-completed tasks are exempted from the clean-PASS transcript re-derivation check; all ordinary `PASS` paths still use `_classify_transcript`.

## Summary

- `origin/master` commit `02949fb3cee8b456df69c9b1e2eac59c3f51c6c6` contains `src/superclaude/cli/sprint/resume/integrity.py`; the current checked-out branch does not contain the `resume/` package, so source lines were read from extracted `origin/master` objects.
- Current Signal B is `derived = _classify_transcript(transcript)`, `lc.derived_status = derived`, `signal_b_pass = derived is TaskStatus.PASS` at `src/superclaude/cli/sprint/resume/integrity.py:127-131`; verdict is `signal_a_pass and signal_b_pass and artifacts_ok` at lines 150-154.
- Exact Opt-2a edit: in `integrity.py` only, branch on `lc.persisted_status is TaskStatus.PASS_RECOVERED`, set `derived = TaskStatus.PASS_RECOVERED`, `lc.derived_status = derived`, and `signal_b_pass = True`; otherwise run `_classify_transcript` and use `derived is not None and derived.is_success`.
- `BoundaryTask.derived_status` exists and is printed through suspect/blocking report paths, so assigning `PASS_RECOVERED` is visible to the operator.
- Executor `PASS_RECOVERED` is transcript-based: it requires `detect_error_max_turns(task_output_path)` and `_task_completed_before_overrun(task_output_path)` before setting `TaskStatus.PASS_RECOVERED`.
- `_classify_transcript` should be left untouched; widening it would affect `discover_failed_tasks_from_transcripts`, while Opt-2a stays localized to the integrity gate.
