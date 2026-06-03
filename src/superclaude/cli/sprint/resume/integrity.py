"""BoundaryIntegrityGate — the resume seam safety gate (FR-2).

Sprint phases are NOT idempotent, so the resume seam (last-completed task + the
next-unfinished task) is treated as *suspect* and must pass a deterministic
integrity gate before new work is layered on top.

Determinism contract (NFR-3): ``BoundaryReport.passed`` is a PURE function of
deterministic signals — last-completed double-validation, unresolved suspects,
and whether partial work was quarantined-or-accepted. The advisory Sonnet/Haiku
coherence read (DD-2) can only append to ``coherence_warnings``; it NEVER flips
``validated_last`` or ``passed``.

Non-destructive contract (NFR-1, DD-3): by default the gate detects, reports, and
STOPs — it performs NO ``results/`` mutation. Cleanup is opt-in and reversible: a
``shutil.copy2`` into ``<results>/.resume-quarantine-<ts>/`` (canonical original
untouched) whose ``preserved/manifest.json`` shape is reversed by the EXISTING
``restore_from_bundle`` — no new restore verb.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.sprint.config import discover_phases
from superclaude.cli.sprint.models import TaskStatus

from .models import BoundaryReport, BoundaryTask, Granularity, ResumePlan


class BoundaryIntegrityGate:
    """Validates the resume seam; deterministic verdict, advisory LLM annotation."""

    def run(
        self,
        plan: ResumePlan,
        *,
        accept_suspect: bool = False,
        cleanup_opted_in: bool = False,
    ) -> BoundaryReport:
        """Validate the resume seam for ``plan`` and return a :class:`BoundaryReport`.

        ``accept_suspect`` is the explicit operator-accepted path (proceed despite
        unresolved suspects). ``cleanup_opted_in`` enables the reversible
        copy-to-quarantine of detected partial work (default: report-only).
        """
        report = BoundaryReport()
        phase_file = self._boundary_phase_file(plan)
        results_dir = plan.release_dir / "results"

        # (a) Deterministic double-validation of the last-completed task (DD-2).
        validated_last, last_suspects, lc = self._validate_last_completed(
            plan, phase_file, results_dir
        )
        report.validated_last = validated_last
        report.suspects.extend(last_suspects)

        # (b) Detect + surface next-unfinished partial work (FR-2.2 / FR-2.3).
        # Default = report-only (NO results/ mutation, NFR-1). The boundary
        # partial work belongs to the task the resume plan RE-RUNS, so it is
        # "assessed-and-accepted" by the plan itself (design §7 keeps passed=True);
        # it is SURFACED for the operator (the CLI prompt is the assent point),
        # NOT a hard gate fail. The opt-in reversible quarantine adds extra safety.
        partial_paths = self._detect_partial(plan, phase_file, results_dir)
        if partial_paths:
            self._surface_partial(plan, report)
            # design §4(b) "report suspect paths in BoundaryReport (always)": carry
            # the concrete half-written paths on the report ALWAYS, independent of
            # cleanup opt-in, so the operator sees them on the default report-only
            # path (F-2/CG-1). This is a report surface only — NEVER a term in
            # ``passed`` (NFR-3); the opt-in quarantine copy is the extra step.
            report.partial_paths = partial_paths
            if cleanup_opted_in:
                self._quarantine(plan, partial_paths, results_dir, report)

        # (c) Deterministic verdict (FR-2.4(b)). The HARD gate is the
        # last-completed integrity check (validated_last): an over-claim there
        # means we would skip work that is not actually done — that STOPs and
        # requires --start/--fresh. accept_suspect is the explicit override.
        # Boundary partial work does NOT flip the verdict (§7).
        report.passed = self._verdict(report, accept_suspect=accept_suspect)
        if not report.passed:
            report.blocking_reasons = self._blocking_reasons(report)

        # (a') ADVISORY coherence read (DD-2) — TASK-granularity only, computed
        # AFTER the verdict so it provably cannot influence it (NFR-3). Empty
        # verdict (claude absent / timed out) ⇒ no-op, CI-safe.
        self._advisory_coherence(plan, report, lc, phase_file, results_dir)
        return report

    # ---- (a) last-completed double-validation (FR-2.1, DD-2) ---------------

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
        signal_a_pass = lc.persisted_status is TaskStatus.PASS

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

    # ---- (b) next-unfinished partial-work detection (FR-2.2 / FR-2.3) ------

    def _detect_partial(
        self, plan: ResumePlan, phase_file: Path | None, results_dir: Path
    ) -> list[Path]:
        """Detect half-written work on the resume boundary across BOTH file classes.

        A never-started task has no transcript, so transcript-only detection
        misses half-written deliverables; we therefore union three sources:
        (1) a task transcript that classifies as INCOMPLETE/FAIL_*, (2) any
        declared deliverable that already exists on disk, and (3) stray
        ``phase-N-task-<id>-*`` files. For PHASE granularity (FR-2.3) the whole
        boundary phase is scanned. Pure read — returns paths, mutates nothing.
        """
        from superclaude.cli.sprint.rerun_tasks import (
            _classify_transcript,
            _declared_deliverables,
        )

        phase = plan.interrupted_phase
        found: set[Path] = set()
        for task_id in self._partial_targets(plan, results_dir):
            tpath = results_dir / f"phase-{phase}-task-{task_id}-output.txt"
            if self._exists(tpath):
                status = _classify_transcript(self._read(tpath))
                if status in (
                    TaskStatus.INCOMPLETE,
                    TaskStatus.FAIL_TERMINAL,
                    TaskStatus.FAIL_RECOVERABLE,
                ):
                    found.add(tpath)
            if phase_file is not None:
                for d in _declared_deliverables(phase_file, task_id):
                    if self._exists(d):
                        found.add(d)
            try:
                for stray in results_dir.glob(f"phase-{phase}-task-{task_id}-*"):
                    if stray.is_file():
                        found.add(stray)
            except OSError:
                pass
        return sorted(found)

    @staticmethod
    def _partial_targets(plan: ResumePlan, results_dir: Path) -> list[str]:
        """Task IDs to scan for partial work: next-unfinished (TASK) or whole
        phase (PHASE)."""
        if plan.granularity is Granularity.TASK:
            nu = [bt.task_id for bt in plan.boundary_tasks if bt.role == "next_unfinished"]
            return nu or list(plan.rerun_task_ids)
        import re

        ids: set[str] = set()
        try:
            transcripts = results_dir.glob(
                f"phase-{plan.interrupted_phase}-task-T*-*"
            )
        except OSError:
            return []
        for p in transcripts:
            m = re.search(r"task-(T\d{2}\.\d{2})-", p.name)
            if m:
                ids.add(m.group(1))
        return sorted(ids)

    @staticmethod
    def _surface_partial(plan: ResumePlan, report: BoundaryReport) -> BoundaryTask:
        """Surface the next-unfinished task as a suspect in the report (FR-2.2)."""
        nu = next(
            (bt for bt in plan.boundary_tasks if bt.role == "next_unfinished"), None
        )
        if nu is None:
            nu = BoundaryTask(task_id="(phase)", role="next_unfinished")
        nu.suspect = True
        if nu not in report.suspects:
            report.suspects.append(nu)
        return nu

    # ---- (b') opt-in reversible quarantine (FR-2.5, DD-3, NFR-1) -----------

    def _quarantine(
        self,
        plan: ResumePlan,
        partial_paths: list[Path],
        results_dir: Path,
        report: BoundaryReport,
    ) -> None:
        """COPY suspect artifacts into ``.resume-quarantine-<ts>/`` (reversible).

        Non-destructive (NFR-1): a ``shutil.copy2`` of each canonical artifact —
        originals are left untouched. The ``preserved/manifest.json`` shape is
        IDENTICAL to ``stash_and_restore_deliverables`` so the EXISTING
        ``restore_from_bundle`` reverses it (no new restore verb, DD-3). Guarded
        by ``.recovery-locks/phase-{phase}.lock`` and recorded in
        ``recovery-audit.log`` via ``write_recovery_audit_log``. Never renames in
        place, never deletes, never reuses the ``.failed-<ts>`` rename (DD-3).
        """
        import json
        import shutil
        from datetime import datetime, timezone

        from superclaude.cli.sprint.recovery import (
            acquire_recovery_lock,
            release_recovery_lock,
            write_recovery_audit_log,
        )
        from superclaude.cli.sprint.rerun_tasks import _preserved_dest

        phase = plan.interrupted_phase
        try:
            lock_path = acquire_recovery_lock(results_dir, phase)
        except Exception:
            # Lock held by a live process — do NOT mutate; stay report-only.
            return

        try:
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            qdir = results_dir / f".resume-quarantine-{ts}"
            preserved_root = qdir / "preserved"
            entries: list[dict] = []
            for canonical in partial_paths:
                try:
                    if not canonical.is_file():
                        continue
                except OSError:
                    continue
                dest = _preserved_dest(preserved_root, canonical, results_dir)
                try:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(canonical, dest)  # COPY — original untouched
                except OSError:
                    continue
                entries.append(
                    {
                        "task_id": self._task_id_for(canonical),
                        "canonical": str(canonical),
                        "preserved": str(dest),
                    }
                )
                report.quarantined[canonical] = dest

            try:
                preserved_root.mkdir(parents=True, exist_ok=True)
                (preserved_root / "manifest.json").write_text(
                    json.dumps({"entries": entries}, indent=2) + "\n",
                    encoding="utf-8",
                )
            except OSError:
                pass

            write_recovery_audit_log(
                results_dir / "recovery-audit.log",
                {
                    "event": "resume_quarantine",
                    "phase": phase,
                    "tasks": sorted({e["task_id"] for e in entries}),
                    "quarantine": str(qdir),
                    "manifest": str(preserved_root / "manifest.json"),
                    "count": len(entries),
                },
            )
        finally:
            release_recovery_lock(lock_path)

    @staticmethod
    def _task_id_for(path: Path) -> str:
        """Best-effort task id from a results filename; 'unknown' otherwise."""
        import re

        m = re.search(r"task-(T\d{2}\.\d{2})-", path.name)
        return m.group(1) if m else "unknown"

    # ---- (c) gate verdict (FR-2.4, NFR-3) ----------------------------------

    @staticmethod
    def _verdict(report: BoundaryReport, *, accept_suspect: bool) -> bool:
        """Pure-deterministic gate verdict (NFR-3).

        The hard gate is last-completed integrity. Boundary partial work is
        surfaced (FR-2.2) but does NOT flip the verdict — the resume plan re-runs
        that task (§7). ``coherence_warnings`` are NEVER a term in ``passed``.
        """
        return accept_suspect or report.validated_last

    # ---- (a') advisory coherence read (DD-2, NFR-3) ------------------------

    def _advisory_coherence(
        self,
        plan: ResumePlan,
        report: BoundaryReport,
        lc: BoundaryTask | None,
        phase_file: Path | None,
        results_dir: Path,
    ) -> None:
        """Append an ADVISORY coherence warning for the last-completed task.

        Scoped strictly to ``granularity==TASK`` with a non-empty transcript AND
        declared deliverables (a per-task last-completed object only exists on the
        TASK path; PHASE single-process runs have none). It NEVER modifies
        ``validated_last`` or ``passed`` (NFR-3) — it only appends to
        ``coherence_warnings``. Any failure (claude absent, timeout, exception)
        yields a BoundaryReport identical to the no-LLM path.
        """
        if not report.validated_last or plan.granularity is not Granularity.TASK:
            return
        if lc is None or phase_file is None:
            return
        transcript = self._read_transcript(
            results_dir, plan.interrupted_phase, lc.task_id
        )
        if not transcript.strip():
            return

        from superclaude.cli.sprint.rerun_tasks import _declared_deliverables

        deliverables = _declared_deliverables(phase_file, lc.task_id)
        if not deliverables:
            return

        try:
            suspect, reason = self._coherence_read(lc, transcript, deliverables)
        except Exception:
            return  # advisory only — never fatal
        if suspect:
            report.coherence_warnings.append((lc, reason))

    @staticmethod
    def _coherence_read(
        lc: BoundaryTask, transcript: str, deliverables: list[Path]
    ) -> tuple[bool, str]:
        """Bounded (~1 call) advisory LLM coherence read. ('' verdict ⇒ not suspect)."""
        from superclaude.cli.sprint.summarizer import invoke_sonnet

        declared = "\n".join(f"- {p}" for p in deliverables)
        prompt = (
            "You are auditing whether a sprint task's transcript is COHERENT with "
            "its declared deliverables. Reply with EXACTLY 'COHERENT' if the work "
            "appears complete and consistent, or 'SUSPECT: <one-line reason>' if "
            "the transcript contradicts the declared deliverables or shows the task "
            "did not actually finish.\n\n"
            f"Task: {lc.task_id}\n"
            f"Declared deliverables:\n{declared}\n\n"
            f"Transcript (truncated):\n{transcript[:4000]}\n"
        )
        out = invoke_sonnet(prompt).strip()
        if not out:
            return False, ""  # claude absent / timed out — CI-safe no-op
        if out.upper().startswith("SUSPECT"):
            reason = out.split(":", 1)[1].strip() if ":" in out else out
            return True, reason
        return False, ""

    # ---- helpers -----------------------------------------------------------

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

    @staticmethod
    def _phase_file(plan: ResumePlan, phase_number: int | None) -> Path | None:
        """Resolve the tasklist file for an ARBITRARY phase number (F-4/CG-3).

        Used to read a prior phase's tasklist when validating a hard-crash
        prior-tail ``last_completed`` task. Pure read; None when unresolvable.
        """
        if phase_number is None:
            return None
        try:
            for phase in discover_phases(Path(plan.index_path)):
                if phase.number == phase_number:
                    return phase.file
        except OSError:
            return None
        return None

    @classmethod
    def _boundary_phase_file(cls, plan: ResumePlan) -> Path | None:
        return cls._phase_file(plan, plan.interrupted_phase)

    @staticmethod
    def _read_transcript(results_dir: Path, phase: int | None, task_id: str) -> str:
        """Read a task transcript (``phase-N-task-<id>-output.txt``); '' if absent."""
        path = results_dir / f"phase-{phase}-task-{task_id}-output.txt"
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return ""

    @staticmethod
    def _read(path: Path) -> str:
        """Read a file's text tolerantly; '' on any error."""
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return ""

    @staticmethod
    def _exists(path: Path) -> bool:
        try:
            return path.exists()
        except OSError:
            return False
