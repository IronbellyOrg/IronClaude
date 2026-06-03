"""DriftAssessor — tiered safety-of-resume scoring for the boundary tasklist (FR-3).

Deterministic tiers; the optional git tier and any LLM explanation are advisory.
Only the 0.8 confidence boundary gates resume (AC-4/AC-5); every other score is
informational.

  Tier 0 (hash)       exact normalized-content match → 1.0. INV-001: the recorded
                      hash in phase-N-result.json and the current hash MUST come
                      from the SAME `_content_sha256_excluding_rerun_block` over
                      the SAME per-phase `phase.file`, else Tier 0 can never match.
  Tier 1 (structural) whitespace-insensitive cosmetic check (AC-4) + structural
                      diff of task IDs / checkpoints / deliverables (AC-5).
  Tier 2 (git)        additive `git diff` annotation when tracked+online.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.sprint.config import discover_phases, parse_tasklist_file

from .models import DriftAssessment, Granularity, ResumePlan


class DriftAssessor:
    """Scores how safe it is to resume given edits to the boundary tasklist."""

    def assess(self, index_path: Path, plan: ResumePlan) -> DriftAssessment:
        """Assess drift for the interrupted phase's tasklist file. Pure read."""
        phase_file = self._boundary_phase_file(index_path, plan)
        if phase_file is None:
            # No boundary phase file to compare (e.g. nothing-to-resume / fresh).
            return DriftAssessment(
                confidence=1.0,
                tier="hash",
                explanation="No interrupted phase tasklist to compare; no drift possible.",
                cosmetic_only=True,
            )

        current_sha = self._current_sha(phase_file)
        recorded_sha = self._recorded_sha(plan)

        # Tier 0 — exact normalized-hash match (block stripped; NOT whitespace
        # tolerant). AC-4 (trailing whitespace) is handled in Tier 1, not here.
        if recorded_sha and current_sha and current_sha == recorded_sha:
            return DriftAssessment(
                confidence=1.0,
                tier="hash",
                explanation=(
                    "Tasklist unchanged since the phase completed "
                    "(normalized-content hash identical)."
                ),
                cosmetic_only=True,
            )

        # Tier 0 miss (or no recorded hash — pre-v4.3.5 phase): fall through to
        # Tier 1 structural analysis, then Tier 2 git annotation (additive).
        assessment = self._tier1(phase_file, recorded_sha, current_sha, plan)
        return self._annotate_git(assessment, phase_file)

    # ---- tiers -------------------------------------------------------------

    def _tier1(
        self,
        phase_file: Path,
        recorded_sha: str | None,
        current_sha: str,
        plan: ResumePlan,
    ) -> DriftAssessment:
        """Tier 1 — structural diff of the boundary tasklist (AC-4 / AC-5).

        Deterministic, no git required. Compares the CURRENT task-ID set
        (``parse_tasklist_file``) against the RECORDED set captured in
        ``plan.boundary_tasks`` (from ``phase-N-result.json``). Only the 0.8
        boundary gates; other scores are advisory.

          * a COMPLETED (PASS) task ID removed/renamed ⇒ material ⇒ ~0.3 (AC-5):
            we would skip work whose definition changed under us.
          * task IDs identical to the recorded set ⇒ cosmetic (whitespace /
            formatting / prose-within-unchanged-structure) ⇒ ~0.9 (AC-4).
          * IDs added/removed only in the not-yet-run (non-completed) region ⇒
            ~0.85 (advisory; we re-run those anyway).

        For PHASE granularity (hard crash, no per-task completed baseline) the
        whole boundary phase is re-run, so edits to it are tolerated ⇒ ~0.9.
        """
        current_ids = self._current_task_ids(phase_file)

        recorded_completed = {
            bt.task_id
            for bt in plan.boundary_tasks
            if bt.persisted_status is not None and bt.persisted_status.is_success
        }
        recorded_all = {
            bt.task_id for bt in plan.boundary_tasks if bt.persisted_status is not None
        }

        # Parse-failure guard: the phase file was readable (else _boundary_phase_file
        # would not exist) yet yielded ZERO task IDs while a non-empty recorded
        # baseline exists. This is a corrupt/gutted/unparseable phase file — NOT a
        # deliberate task removal. Verdict stays conservative (<0.8 STOP, FR-3.4) but
        # the explanation must accurately attribute the cause (FR-3.5) rather than
        # claim specific completed tasks were "removed".
        if plan.granularity is Granularity.TASK and recorded_all and not current_ids:
            return DriftAssessment(
                confidence=0.3,
                tier="structural",
                changed_paths=[str(phase_file)],
                explanation=(
                    "Boundary tasklist parsed to zero task IDs but the recorded "
                    "baseline lists "
                    f"{len(recorded_all)} task(s) — the phase file is empty, "
                    "corrupt, or no longer in the expected '### T<PP>.<TT>' "
                    "format. Cannot verify completed work survived; resuming is "
                    "unsafe. Re-run with --start to re-execute the phase, or "
                    "--fresh to discard prior state."
                ),
                cosmetic_only=False,
            )

        # PHASE granularity (or no recorded per-task baseline): re-running the
        # entire boundary phase makes drift non-fatal — nothing is skipped.
        if plan.granularity is not Granularity.TASK or not recorded_all:
            return DriftAssessment(
                confidence=0.9,
                tier="structural",
                changed_paths=[],
                explanation=(
                    "Boundary phase re-runs in full (phase-level resume); tasklist "
                    "edits are tolerated because no completed work is skipped."
                ),
                cosmetic_only=True,
            )

        removed_completed = sorted(recorded_completed - current_ids)
        if removed_completed:
            return DriftAssessment(
                confidence=0.3,
                tier="structural",
                changed_paths=[str(phase_file)],
                explanation=(
                    "Material edit: completed task(s) "
                    f"{', '.join(removed_completed)} no longer present in the "
                    "tasklist — resuming would skip work whose definition changed. "
                    "Re-run with --start to re-execute, or --fresh to discard state."
                ),
                cosmetic_only=False,
            )

        added = sorted(current_ids - recorded_all)
        removed_pending = sorted((recorded_all - recorded_completed) - current_ids)
        if added or removed_pending:
            changes = []
            if added:
                changes.append(f"added {', '.join(added)}")
            if removed_pending:
                changes.append(f"removed pending {', '.join(removed_pending)}")
            return DriftAssessment(
                confidence=0.85,
                tier="structural",
                changed_paths=[str(phase_file)],
                explanation=(
                    "Changes confined to the not-yet-run region ("
                    + "; ".join(changes)
                    + "); completed tasks intact."
                ),
                cosmetic_only=False,
            )

        # Task-ID set identical to the recorded set. ``assess`` only reaches Tier 1
        # AFTER a Tier-0 hash MISS (current_sha != recorded_sha), so the file
        # content provably changed. Keep 0.9/cosmetic ONLY when the whitespace-
        # normalized hashes prove the change is whitespace-only (AC-4); otherwise
        # the change is material with IDs unchanged (AC-5/F-3) — a same-ID body /
        # checkpoint / deliverable edit to a completed task — and resume must STOP
        # at <0.8. This is fully deterministic (Tier-0/1 only, never git — NFR-3).
        # Backward-compatible: a recorded baseline lacking ``tasklist_sha256_ws``
        # (pre-F-3 result.json) cannot prove cosmetic ⇒ conservative <0.8 fallback.
        recorded_ws = self._recorded_sha_ws(plan)
        current_ws = self._current_sha_ws(phase_file)
        if recorded_ws and current_ws and recorded_ws == current_ws:
            return DriftAssessment(
                confidence=0.9,
                tier="structural",
                changed_paths=[],
                explanation=(
                    "Tasklist task-ID structure identical to the recorded baseline "
                    "and the whitespace-normalized content matches; the remaining "
                    "differences are whitespace/formatting only (cosmetic)."
                ),
                cosmetic_only=True,
            )
        return DriftAssessment(
            confidence=0.5,
            tier="structural",
            changed_paths=[str(phase_file)],
            explanation=(
                "Boundary tasklist content changed (content hash differs from the "
                "recorded baseline) but no task IDs were added or removed"
                + (
                    ", and no whitespace-normalized baseline was recorded for this "
                    "phase, so the change could not be proven whitespace-only"
                    if not recorded_ws
                    else ", and the change is NOT whitespace-only"
                )
                + ". A same-ID body/checkpoint/deliverable edit to a completed task "
                "may silently skip work whose definition changed under us — resuming "
                "is unsafe (AC-5). Re-run with --start to re-execute the phase, or "
                "--fresh to discard prior state."
            ),
            cosmetic_only=False,
        )

    # ---- helpers -----------------------------------------------------------

    @staticmethod
    def _boundary_phase_file(index_path: Path, plan: ResumePlan) -> Path | None:
        """Resolve the interrupted phase's tasklist file (per-phase, NOT index)."""
        if plan.interrupted_phase is None:
            return None
        for phase in discover_phases(Path(index_path)):
            if phase.number == plan.interrupted_phase:
                return phase.file
        return None

    @staticmethod
    def _current_sha(phase_file: Path) -> str:
        from superclaude.cli.sprint.rerun_tasks import (
            _content_sha256_excluding_rerun_block,
        )

        return _content_sha256_excluding_rerun_block(phase_file)

    @staticmethod
    def _current_sha_ws(phase_file: Path) -> str:
        """Whitespace-normalized current hash (F-3/CG-2). Same fn the writer uses."""
        from superclaude.cli.sprint.rerun_tasks import (
            _content_sha256_ws_excluding_rerun_block,
        )

        return _content_sha256_ws_excluding_rerun_block(phase_file)

    @staticmethod
    def _current_task_ids(phase_file: Path) -> set[str]:
        """Parse the current task-ID set from the phase tasklist (tolerant)."""
        try:
            entries = parse_tasklist_file(phase_file)
        except OSError:
            return set()
        return {e.task_id for e in entries if getattr(e, "task_id", None)}

    @staticmethod
    def _annotate_git(assessment: DriftAssessment, phase_file: Path) -> DriftAssessment:
        """Tier 2 — additive git characterization. NEVER changes ``confidence``.

        Annotates ``changed_paths`` with a ``git diff @{upstream}`` --stat summary
        and marks ``tier='git'`` when the phase file is tracked AND an upstream
        exists. Skips gracefully (returns the Tier-1 result untouched) on
        detached-HEAD, no upstream, untracked file, or git unavailable — any such
        condition raises and is caught; the deterministic gate value is preserved.
        """
        import subprocess

        cwd = str(phase_file.parent)

        def _git(*args: str) -> subprocess.CompletedProcess:
            return subprocess.run(
                ["git", "-C", cwd, *args],
                capture_output=True,
                check=True,
                text=True,
            )

        try:
            # Require an upstream (skips detached-HEAD / no-upstream) and a
            # tracked file. Either failing raises CalledProcessError → caught.
            _git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
            _git("ls-files", "--error-unmatch", str(phase_file))
            diff = _git(
                "diff",
                "--ignore-all-space",
                "--stat",
                "@{upstream}",
                "--",
                str(phase_file),
            )
        except (OSError, subprocess.SubprocessError):
            return assessment  # git unavailable / detached / no upstream / untracked

        summary = diff.stdout.strip()
        if summary:
            annotations = [f"git: {line.strip()}" for line in summary.splitlines()]
            assessment.changed_paths = list(
                dict.fromkeys(list(assessment.changed_paths) + annotations)
            )
            assessment.tier = "git"
        return assessment

    def _recorded_sha(self, plan: ResumePlan) -> str | None:
        """Read tasklist_sha256 from the interrupted phase's result.json (or None)."""
        import json

        path = (
            plan.release_dir / "results" / f"phase-{plan.interrupted_phase}-result.json"
        )
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        sha = payload.get("tasklist_sha256")
        return sha if isinstance(sha, str) and sha else None

    def _recorded_sha_ws(self, plan: ResumePlan) -> str | None:
        """Read tasklist_sha256_ws from the interrupted phase's result.json (F-3/CG-2).

        Analogous to ``_recorded_sha`` for the whitespace-normalized field. Returns
        None when the field is absent (pre-F-3 result.json) — drift then treats the
        change as non-provably-cosmetic and scores <0.8 (conservative fallback).
        """
        import json

        path = (
            plan.release_dir / "results" / f"phase-{plan.interrupted_phase}-result.json"
        )
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        sha = payload.get("tasklist_sha256_ws")
        return sha if isinstance(sha, str) and sha else None
