"""ResumePlanner — pure-read reconstruction of a sprint resume plan (FR-1).

The planner reads only: ``execution-log.jsonl`` (release root), the per-phase
``phase-N-result.json`` files (``results/``), and task transcripts. It performs
NO writes. Its output, a :class:`ResumePlan`, tells the CLI which phase was
interrupted, which tasks sit on the resume seam, and at what granularity to
dispatch (TASK → rerun engine, PHASE → executor loop).

DD-1 (truth anchor): the atomic ``phase-N-result.json`` is the AUTHORITATIVE
phase-completion signal. The JSONL ledger append is non-durable (no fsync/rename,
``logging_.py``), so a hard crash may tear or drop its last line — a missing
``phase_complete`` line must NOT demote a phase whose result.json proves it
passed. The ledger is corroboration only.
"""

from __future__ import annotations

import json
from pathlib import Path

from superclaude.cli.sprint.config import (
    _resolve_release_dir,
    discover_phases,
    parse_tasklist_file,
)
from superclaude.cli.sprint.models import PhaseStatus, TaskStatus

from .models import BoundaryTask, Granularity, ResumePlan

# Phase-classification labels (internal).
_COMPLETE = "complete"
_CRASH = "crash"
_INTERRUPT = "interrupt"
_PENDING = "pending"


class ResumePlanner:
    """Reconstructs a :class:`ResumePlan` from on-disk sprint state (read-only)."""

    def plan(self, index_path: Path, *, end_override: int | None = None) -> ResumePlan:
        """Reconstruct the resume plan for ``index_path``. Pure read; no writes."""
        index_path = Path(index_path)
        release_dir = _resolve_release_dir(index_path)
        phases = discover_phases(index_path)
        results_dir = release_dir / "results"
        jsonl = release_dir / "execution-log.jsonl"
        events = self._read_jsonl(jsonl)

        plan = ResumePlan(index_path=index_path, release_dir=release_dir)

        # FR-5 ambiguity (independent of phase classification): flag, never
        # auto-pick, when on-disk state is contradictory on an expensive run.
        self._detect_ambiguity(plan, index_path, release_dir, events, results_dir)

        if not phases:
            # No phases discovered — nothing to plan. Treat as nothing-to-resume.
            plan.granularity = Granularity.NONE
            plan.interrupt_kind = "none"
            return plan

        max_phase = max(p.number for p in phases)
        plan.end_phase = end_override if end_override is not None else max_phase

        # 1. Classify every phase from result.json (authoritative) + ledger (DD-1).
        classes: dict[int, str] = {
            p.number: self._classify_phase(p.number, events, results_dir)
            for p in phases
        }
        plan.completed_phases = sorted(n for n, c in classes.items() if c == _COMPLETE)

        # 2. Locate the resume seam.
        interrupted_phase, interrupt_kind = self._find_interrupted(phases, classes)
        any_started = any(
            c in (_COMPLETE, _CRASH, _INTERRUPT) for c in classes.values()
        )
        all_complete = len(plan.completed_phases) == len(phases)

        if all_complete:
            # AC-6: nothing to resume.
            plan.interrupted_phase = None
            plan.interrupt_kind = "complete"
            plan.start_phase = max_phase
            plan.granularity = Granularity.NONE
            return plan

        if interrupted_phase is not None:
            # A phase started but did not complete: the true interruption seam.
            plan.interrupted_phase = interrupted_phase
            plan.interrupt_kind = interrupt_kind
            plan.start_phase = interrupted_phase
            # Safe default until boundary disposition (FR-1.4) refines to TASK.
            plan.granularity = Granularity.PHASE
        elif not any_started:
            # Fresh: no phase ever started. Run normally from phase 1 (NOT NONE —
            # NONE is reserved for all-complete so bare `sprint run` on a fresh
            # index runs rather than printing "nothing to resume").
            plan.interrupted_phase = None
            plan.interrupt_kind = "none"
            plan.start_phase = 1
            plan.granularity = Granularity.PHASE
        else:
            # Clean boundary: some phases complete, the rest pending (never
            # started). Resume at the first pending phase, re-run it from scratch.
            first_pending = min(
                p.number for p in phases if classes[p.number] != _COMPLETE
            )
            plan.interrupted_phase = first_pending
            plan.interrupt_kind = "pending"
            plan.start_phase = first_pending
            plan.granularity = Granularity.PHASE

        # Boundary disposition (FR-1.4/1.5): refine granularity + build the
        # per-task seam for the interrupted phase. No-op for the fresh case
        # (interrupted_phase is None).
        if plan.interrupted_phase is not None:
            self._build_boundary(plan, results_dir)
            # F-4/CG-3: on a PHASE hard crash the interrupted phase yields an
            # empty boundary, so the integrity gate would vacuously pass without
            # double-validating the PRIOR completed phase's tail (AC-3 :141-143).
            # Emit exactly one prior-tail last_completed boundary task so the gate
            # actually re-derives it. `phases` is in scope here (NOT inside
            # _build_boundary, which only receives plan+results_dir).
            self._emit_prior_tail_boundary(plan, phases)

        return plan

    # ---- helpers -----------------------------------------------------------

    def _build_boundary(self, plan: ResumePlan, results_dir: Path) -> None:
        """Populate granularity, boundary_tasks, and rerun_task_ids (FR-1.4/1.5).

        Per-task data in ``phase-N-result.json`` ⇒ TASK granularity with a full
        per-task seam. Absent task_results ⇒ derive non-PASS tasks from
        transcripts (legacy/hard-crash); TASK if any derived, else PHASE.
        Roles: ``last_completed`` = highest-index PASS, ``next_unfinished`` =
        first (lowest-index) non-PASS.
        """
        from superclaude.cli.sprint.rerun_tasks import (
            discover_failed_tasks_from_transcripts,
        )

        interrupted = plan.interrupted_phase
        rj = self._load_result_json(results_dir / f"phase-{interrupted}-result.json")
        task_results = (rj or {}).get("task_results") or []

        boundary: list[BoundaryTask] = []
        if task_results:
            # Per-task data present (v4.3.0+): authoritative seam.
            plan.granularity = Granularity.TASK
            for tr in task_results:
                task_id = (tr.get("task") or {}).get("task_id")
                if not task_id:
                    continue
                boundary.append(
                    BoundaryTask(
                        task_id=task_id,
                        persisted_status=self._coerce_task_status(tr.get("status")),
                    )
                )
            plan.rerun_task_ids = [
                bt.task_id
                for bt in boundary
                if bt.persisted_status is None or not bt.persisted_status.is_success
            ]
        else:
            # Hard crash / pre-v4.3.0: derive the failed set from transcripts.
            derived = discover_failed_tasks_from_transcripts(results_dir, interrupted)
            plan.granularity = Granularity.TASK if derived else Granularity.PHASE
            for task_id, status in derived:
                boundary.append(BoundaryTask(task_id=task_id, derived_status=status))
            plan.rerun_task_ids = [task_id for task_id, _ in derived]

        self._assign_roles(boundary)
        plan.boundary_tasks = boundary

    def _emit_prior_tail_boundary(self, plan: ResumePlan, phases: list) -> None:
        """Emit a prior-phase-tail ``last_completed`` on a PHASE hard crash (F-4/CG-3).

        When the interrupted phase produced no per-task boundary (granularity
        PHASE, empty ``boundary_tasks`` — a true hard crash with no result.json
        task_results and no transcripts), the integrity gate's last-completed
        validation is vacuously True and the PRIOR completed phase's tail is never
        double-validated (AC-3 :141-143). This appends exactly ONE
        ``BoundaryTask`` for that prior tail so the gate re-derives it.

        Pure read: derives the prior phase from ``plan.completed_phases`` and the
        tail task id from ``parse_tasklist_file`` (read_text only) — no writes, so
        the planner's pure-read invariant is preserved.
        """
        if plan.granularity is not Granularity.PHASE or plan.boundary_tasks:
            return
        interrupted = plan.interrupted_phase
        if interrupted is None:
            return
        # Highest completed phase strictly below the interrupted one.
        prior = max((n for n in plan.completed_phases if n < interrupted), default=None)
        if prior is None:
            return  # no completed phase below the interrupted one — nothing to validate
        prior_phase = next((p for p in phases if p.number == prior), None)
        if prior_phase is None:
            return
        try:
            entries = parse_tasklist_file(prior_phase.file)
        except OSError:
            return
        if not entries:
            return
        tail_id = getattr(entries[-1], "task_id", None)
        if not tail_id:
            return
        # Signal A (PASS) is claimed because the prior phase is classed COMPLETE;
        # the gate's value-add is the independent Signal B + artifact re-check
        # under `phase=prior` (so the transcript/deliverables resolve correctly).
        plan.boundary_tasks.append(
            BoundaryTask(
                task_id=tail_id,
                persisted_status=TaskStatus.PASS,
                role="last_completed",
                phase=prior,
            )
        )

    def _detect_ambiguity(
        self,
        plan: ResumePlan,
        index_path: Path,
        release_dir: Path,
        events: list[dict],
        results_dir: Path,
    ) -> None:
        """Flag ambiguous resume state (FR-5). Never auto-picks on an expensive run.

        Triggers: (1) more than one plausible release directory carrying sprint
        state; (2) a conflicting/interleaved ledger that cannot be paired
        (concurrent ``sprint run <same index>`` share one deterministic
        release_dir with no lock — §12); (3) a present-but-unreadable core file.
        """
        reasons: list[str] = []

        candidates = self._release_dir_candidates(index_path, release_dir)
        if len(candidates) > 1:
            reasons.append(
                "Multiple plausible release directories with sprint state: "
                + ", ".join(str(c) for c in candidates)
            )

        conflict = self._ledger_conflict(events)
        if conflict:
            reasons.append(conflict)

        # (3) Core file present but unreadable: a non-empty ledger that parsed to
        # zero events while results exist means a corrupt/locked ledger we cannot
        # trust to pair — surface rather than silently resume.
        jsonl = release_dir / "execution-log.jsonl"
        try:
            ledger_nonempty = jsonl.exists() and jsonl.stat().st_size > 0
        except OSError:
            ledger_nonempty = False
        results_present = False
        try:
            results_present = any(results_dir.glob("phase-*-result.json"))
        except OSError:
            results_present = False
        if ledger_nonempty and not events and results_present:
            reasons.append(f"Execution ledger present but unparseable: {jsonl}")

        if reasons:
            plan.ambiguous = True
            plan.ambiguity_reasons = reasons

    @staticmethod
    def _release_dir_candidates(index_path: Path, release_dir: Path) -> list[Path]:
        """Plausible release dirs (resolved + backward-compatible default) that
        actually carry sprint state. >1 ⇒ we cannot disambiguate deterministically."""

        def has_state(d: Path) -> bool:
            try:
                if (d / "execution-log.jsonl").exists():
                    return True
                return any((d / "results").glob("phase-*-result.json"))
            except OSError:
                return False

        candidates: list[Path] = []
        for cand in dict.fromkeys([release_dir, index_path.parent]):
            if has_state(cand):
                candidates.append(cand)
        return candidates

    @staticmethod
    def _ledger_conflict(events: list[dict]) -> str | None:
        """Detect concurrent unpaired phase_start events (interleaved runs)."""
        from collections import Counter

        starts = Counter(
            e["phase"]
            for e in events
            if e.get("event") == "phase_start" and "phase" in e
        )
        closes = Counter(
            e["phase"]
            for e in events
            if e.get("event") in ("phase_complete", "phase_interrupt") and "phase" in e
        )
        for phase, start_count in starts.items():
            if start_count - closes.get(phase, 0) >= 2:
                return (
                    f"Conflicting ledger: phase {phase} has {start_count} "
                    f"phase_start events with only {closes.get(phase, 0)} closes "
                    "(concurrent runs?)"
                )
        return None

    @staticmethod
    def _assign_roles(boundary: list[BoundaryTask]) -> None:
        """Mark last_completed (highest-index PASS) and next_unfinished roles."""
        passed = sorted(
            (
                bt
                for bt in boundary
                if bt.persisted_status is not None and bt.persisted_status.is_success
            ),
            key=lambda bt: bt.task_id,
        )
        if passed:
            passed[-1].role = "last_completed"
        non_pass = sorted(
            (
                bt
                for bt in boundary
                if bt.persisted_status is None or not bt.persisted_status.is_success
            ),
            key=lambda bt: bt.task_id,
        )
        if non_pass:
            non_pass[0].role = "next_unfinished"

    @staticmethod
    def _coerce_task_status(value: object) -> TaskStatus | None:
        """Map a persisted status string to TaskStatus, tolerant of junk."""
        try:
            return TaskStatus(value)  # type: ignore[arg-type]
        except (ValueError, TypeError):
            return None

    def _classify_phase(
        self, phase_num: int, events: list[dict], results_dir: Path
    ) -> str:
        """Classify one phase per DD-1 ordering (result.json authoritative)."""
        rj = self._load_result_json(results_dir / f"phase-{phase_num}-result.json")
        starts = [
            e
            for e in events
            if e.get("event") == "phase_start" and e.get("phase") == phase_num
        ]
        closes = [
            e
            for e in events
            if e.get("event") in ("phase_complete", "phase_interrupt")
            and e.get("phase") == phase_num
        ]

        if rj is not None and self._is_pass_family(rj.get("status")):
            # result.json with PASS-family status is authoritative — a torn or
            # dropped phase_complete ledger line must not demote it.
            return _COMPLETE
        if starts and not closes:
            return _CRASH
        if any(e.get("event") == "phase_interrupt" for e in closes):
            return _INTERRUPT
        if rj is not None:
            # result.json present but non-passing ⇒ recoverable interrupt.
            return _INTERRUPT
        return _PENDING

    @staticmethod
    def _find_interrupted(
        phases: list, classes: dict[int, str]
    ) -> tuple[int | None, str]:
        """Lowest non-completed phase that has a start/result (crash/interrupt)."""
        for p in sorted(phases, key=lambda x: x.number):
            c = classes[p.number]
            if c in (_CRASH, _INTERRUPT):
                return p.number, c
        return None, "none"

    @staticmethod
    def _is_pass_family(status_str: object) -> bool:
        """True iff ``status_str`` maps to a PASS-family PhaseStatus."""
        try:
            return PhaseStatus(status_str).is_success  # type: ignore[arg-type]
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _load_result_json(path: Path) -> dict | None:
        """Load a phase-N-result.json, tolerant of absence/corruption (→ None)."""
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None

    @staticmethod
    def _read_jsonl(path: Path) -> list[dict]:
        """Read a JSONL ledger, skipping malformed lines (DD-1 tolerance)."""
        events: list[dict] = []
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return events
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                continue  # torn/dropped line — skip, do not abort
            if isinstance(obj, dict):
                events.append(obj)
        return events
