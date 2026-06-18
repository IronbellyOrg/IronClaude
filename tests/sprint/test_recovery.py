"""Tests for sprint recovery bundle, audit log, and merge orchestration."""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import click
import pytest

from superclaude.cli.sprint.recovery import (
    ManualNominator,
    RecoveryBundle,
    RecoveryBundleRef,
    RecoveryStatus,
    ReflectReportNominator,
    acquire_recovery_lock,
    acquire_run_lock,
    compute_tasklist_sha256,
    merge_recovery_bundle,
    release_recovery_lock,
    release_run_lock,
    retry_count_for_task,
    write_recovery_audit_log,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _seed_release(tmp_path: Path, phase: int = 7) -> tuple[Path, Path, Path]:
    """Create a minimal canonical release layout for merge tests.

    Returns ``(source_index, release_dir, results_dir)``. ``release_dir`` is
    ``tmp_path`` itself so ``_resolve_release_dir(source_index)`` resolves to
    it (index lives directly in the release dir, not under a ``tasklist/``
    subdir). Seeds a canonical ``phase-N-result.json`` so merge step 7 has a
    file to rewrite.
    """
    source_index = tmp_path / "tasklist-index.md"
    source_index.write_text(
        "# Sprint\n\n| # | File |\n|---|------|\n", encoding="utf-8"
    )
    results_dir = tmp_path / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    result_json = results_dir / f"phase-{phase}-result.json"
    result_json.write_text(
        json.dumps({"phase": phase, "task_results": [], "recovery_history": []}),
        encoding="utf-8",
    )
    return source_index, tmp_path, results_dir


def _bundle_with_sidecar(
    tmp_path: Path, *, bundle_id: str, phase: int, task_ids: list[str]
) -> RecoveryBundle:
    """Build a RecoveryBundle whose bundle dir holds a ``task-results.json``
    sidecar, so merge step 7 can refresh the affected tasks and settle SUCCESS.

    Without the sidecar the engine intentionally records a
    ``result-json-not-refreshed`` failure (no silent data loss), which
    downgrades the bundle to PARTIAL. The sidecar mirrors the serialized
    rerun ``PhaseResult.task_results`` that Phase 3's ``run_rerun_tasks``
    writes alongside the rerun transcripts.
    """
    bundle_dir = tmp_path / "bundles" / bundle_id
    bundle_dir.mkdir(parents=True, exist_ok=True)
    sidecar = bundle_dir / "task-results.json"
    sidecar.write_text(
        json.dumps([{"task": {"task_id": tid}, "status": "pass"} for tid in task_ids]),
        encoding="utf-8",
    )
    # artifacts_produced[0].parent resolves to bundle_dir (where the sidecar
    # lives); a placeholder transcript file anchors that parent.
    placeholder = bundle_dir / f"phase-{phase}-task-{task_ids[0]}-output.txt"
    placeholder.write_text("rerun output", encoding="utf-8")
    return RecoveryBundle(
        bundle_id=bundle_id,
        affected_phase=phase,
        affected_tasks=list(task_ids),
        artifacts_produced=[placeholder],
    )


# ---------------------------------------------------------------------------
# RecoveryBundle construction + state transitions
# ---------------------------------------------------------------------------


class TestRecoveryBundle:
    def test_construct_empty_bundle(self):
        """All-default constructor: empty task/artifact collections, status
        defaults to DRYRUN until the merge engine commits."""
        bundle = RecoveryBundle(bundle_id="rerun-001", affected_phase=7)
        assert bundle.bundle_id == "rerun-001"
        assert bundle.affected_phase == 7
        assert bundle.verb == "rerun-tasks"
        assert bundle.affected_tasks == []
        assert bundle.artifacts_produced == []
        assert bundle.artifacts_replaced == {}
        assert bundle.source_tasklist_sha256 == ""
        assert bundle.end_tasklist_sha256 is None
        assert bundle.status is RecoveryStatus.DRYRUN
        assert bundle.rerun_attempt == 1

    def test_add_entry_transitions_to_in_progress(self):
        """Populating ``affected_tasks`` / ``artifacts_produced`` is the actual
        state-accrual mechanism (no add_entry() method on the dataclass). The
        bundle accumulates work while remaining in the pre-merge DRYRUN state."""
        bundle = RecoveryBundle(bundle_id="rerun-002", affected_phase=3)
        bundle.affected_tasks.append("T03.01")
        bundle.artifacts_produced.append(Path("phase-3-task-T03.01-output.txt"))
        assert bundle.affected_tasks == ["T03.01"]
        assert bundle.artifacts_produced == [Path("phase-3-task-T03.01-output.txt")]
        # Status has NOT yet advanced — merge_recovery_bundle owns that flip.
        assert bundle.status is RecoveryStatus.DRYRUN
        assert bundle.end_tasklist_sha256 is None

    def test_finalize_transitions_to_complete(self, tmp_path: Path):
        """``merge_recovery_bundle`` is the finalize mechanism: on a clean merge
        it sets ``status`` to SUCCESS and populates ``end_tasklist_sha256``."""
        source_index, _release_dir, _results_dir = _seed_release(tmp_path, phase=7)
        bundle = _bundle_with_sidecar(
            tmp_path, bundle_id="rerun-003", phase=7, task_ids=["T07.11"]
        )
        bundle.source_tasklist_sha256 = "seed"
        merge_recovery_bundle(bundle, source_index)
        assert bundle.status is RecoveryStatus.SUCCESS
        assert bundle.end_tasklist_sha256 == compute_tasklist_sha256(source_index)
        assert bundle.status.is_terminal is True


# ---------------------------------------------------------------------------
# RecoveryStatus enum contract
# ---------------------------------------------------------------------------


class TestRecoveryStatus:
    def test_status_values_and_properties(self):
        assert RecoveryStatus.SUCCESS.value == "success"
        assert RecoveryStatus.PARTIAL.value == "partial"
        assert RecoveryStatus.FAILED.value == "failed"
        assert RecoveryStatus.DRYRUN.value == "dryrun"
        # is_terminal is True only for the two settled outcomes.
        assert RecoveryStatus.SUCCESS.is_terminal is True
        assert RecoveryStatus.FAILED.is_terminal is True
        assert RecoveryStatus.PARTIAL.is_terminal is False
        assert RecoveryStatus.DRYRUN.is_terminal is False


# ---------------------------------------------------------------------------
# merge_recovery_bundle — audit, idempotency, atomic rollback
# ---------------------------------------------------------------------------


class TestMergeRecoveryBundle:
    def test_merge_writes_audit_log_entry(self, tmp_path: Path):
        """A successful merge appends a ``merge_recovery_bundle`` JSONL event to
        ``<results_dir>/recovery-audit.log``."""
        source_index, _release_dir, results_dir = _seed_release(tmp_path, phase=7)
        bundle = _bundle_with_sidecar(
            tmp_path, bundle_id="rerun-audit", phase=7, task_ids=["T07.11"]
        )
        merge_recovery_bundle(bundle, source_index)

        audit_log = results_dir / "recovery-audit.log"
        assert audit_log.exists()
        lines = [
            json.loads(line)
            for line in audit_log.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        merge_events = [e for e in lines if e.get("event") == "merge_recovery_bundle"]
        assert len(merge_events) == 1
        evt = merge_events[0]
        assert evt["bundle_id"] == "rerun-audit"
        assert evt["affected_phase"] == 7
        assert evt["affected_tasks"] == ["T07.11"]
        assert evt["status"] == "success"
        assert "timestamp" in evt

    def test_merge_is_idempotent(self, tmp_path: Path):
        """Merging the same bundle twice does not corrupt state: each call adds
        exactly one audit entry and one recovery_history ref, and the bundle
        settles to a terminal-or-partial status both times (no exception)."""
        source_index, _release_dir, results_dir = _seed_release(tmp_path, phase=7)
        bundle = RecoveryBundle(
            bundle_id="rerun-idem",
            affected_phase=7,
            affected_tasks=["T07.11"],
        )
        merge_recovery_bundle(bundle, source_index)
        first_status = bundle.status
        merge_recovery_bundle(bundle, source_index)

        # Audit log accumulates one entry per merge call.
        audit_log = results_dir / "recovery-audit.log"
        merge_events = [
            json.loads(line)
            for line in audit_log.read_text(encoding="utf-8").splitlines()
            if line.strip() and json.loads(line).get("event") == "merge_recovery_bundle"
        ]
        assert len(merge_events) == 2

        # phase-N-result.json remains valid JSON and accumulates one ref per merge.
        result_json = results_dir / "phase-7-result.json"
        data = json.loads(result_json.read_text(encoding="utf-8"))
        refs = [
            r
            for r in data.get("recovery_history", [])
            if r.get("bundle_id") == "rerun-idem"
        ]
        assert len(refs) == 2
        # Second merge did not regress the status to a failure.
        assert bundle.status in (RecoveryStatus.SUCCESS, RecoveryStatus.PARTIAL)
        assert first_status in (RecoveryStatus.SUCCESS, RecoveryStatus.PARTIAL)

    def test_merge_failure_rolls_back_atomically(self, tmp_path: Path):
        """If the atomic result-json write fails (simulated OSError on the temp
        file write), the canonical ``phase-N-result.json`` is left untouched and
        the bundle downgrades to PARTIAL (failure recorded, no data loss)."""
        source_index, _release_dir, results_dir = _seed_release(tmp_path, phase=7)
        result_json = results_dir / "phase-7-result.json"
        original = result_json.read_text(encoding="utf-8")

        bundle = RecoveryBundle(
            bundle_id="rerun-rollback",
            affected_phase=7,
            affected_tasks=["T07.11"],
        )

        real_write_text = Path.write_text

        def _selective_write(self, data, *args, **kwargs):
            # Fail only the result-json temp write; allow all other writes
            # (manifest, audit log, lock files) to proceed normally.
            if self.name == "phase-7-result.json.tmp":
                raise OSError("simulated disk-full on result-json temp write")
            return real_write_text(self, data, *args, **kwargs)

        with patch.object(Path, "write_text", _selective_write):
            merge_recovery_bundle(bundle, source_index)

        # Canonical result-json is byte-identical to the pre-merge content.
        assert result_json.read_text(encoding="utf-8") == original
        # Failure was recorded → bundle downgraded to PARTIAL, never SUCCESS.
        assert bundle.status is RecoveryStatus.PARTIAL

    def test_merge_refreshes_canonical_status_from_sidecar(self, tmp_path: Path):
        """AC-2/AC-3 (TASK-SIDECAR-GAP): with a ``task-results.json`` sidecar
        present, merge step 7 REPLACES the affected task's prior entry with the
        refreshed rerun result — the canonical ``phase-N-result.json`` flips
        ``fail_recoverable`` → ``pass`` with no duplicate entry, and the bundle
        settles SUCCESS (no ``result-json-not-refreshed`` failure)."""
        source_index, _release_dir, results_dir = _seed_release(tmp_path, phase=7)
        result_json = results_dir / "phase-7-result.json"
        # Seed a prior fail_recoverable entry for the task about to be reran.
        result_json.write_text(
            json.dumps(
                {
                    "phase": 7,
                    "task_results": [
                        {"task": {"task_id": "T07.11"}, "status": "fail_recoverable"}
                    ],
                    "recovery_history": [],
                }
            ),
            encoding="utf-8",
        )
        # _bundle_with_sidecar writes a sidecar holding the refreshed PASS result.
        bundle = _bundle_with_sidecar(
            tmp_path, bundle_id="rerun-refresh", phase=7, task_ids=["T07.11"]
        )

        merge_recovery_bundle(bundle, source_index)

        data = json.loads(result_json.read_text(encoding="utf-8"))
        entries = [
            tr
            for tr in data["task_results"]
            if tr.get("task", {}).get("task_id") == "T07.11"
        ]
        assert len(entries) == 1, "affected task must be replaced, not duplicated"
        assert entries[0]["status"] == "pass"
        assert len(data["recovery_history"]) == 1
        assert bundle.status is RecoveryStatus.SUCCESS

    def test_merge_without_sidecar_preserves_prior_and_partials(self, tmp_path: Path):
        """AC-4 (R-F3 no-data-loss): with NO ``task-results.json`` sidecar, merge
        step 7 must PRESERVE the affected task's prior entry (never silently drop
        it) and downgrade the bundle to PARTIAL."""
        source_index, _release_dir, results_dir = _seed_release(tmp_path, phase=7)
        result_json = results_dir / "phase-7-result.json"
        result_json.write_text(
            json.dumps(
                {
                    "phase": 7,
                    "task_results": [
                        {"task": {"task_id": "T07.11"}, "status": "fail_recoverable"}
                    ],
                    "recovery_history": [],
                }
            ),
            encoding="utf-8",
        )
        # Bundle whose artifacts_produced parent holds NO task-results.json sidecar.
        bundle_dir = tmp_path / "bundles" / "rerun-nosidecar"
        bundle_dir.mkdir(parents=True, exist_ok=True)
        placeholder = bundle_dir / "phase-7-task-T07.11-output.txt"
        placeholder.write_text("rerun output", encoding="utf-8")
        bundle = RecoveryBundle(
            bundle_id="rerun-nosidecar",
            affected_phase=7,
            affected_tasks=["T07.11"],
            artifacts_produced=[placeholder],
        )

        merge_recovery_bundle(bundle, source_index)

        data = json.loads(result_json.read_text(encoding="utf-8"))
        entries = [
            tr
            for tr in data["task_results"]
            if tr.get("task", {}).get("task_id") == "T07.11"
        ]
        assert len(entries) == 1, "prior entry must be preserved, never dropped"
        assert entries[0]["status"] == "fail_recoverable"
        assert bundle.status is RecoveryStatus.PARTIAL

    def test_merge_relocates_deliverable_trees_or_partials(self, tmp_path: Path):
        """Defect-1 regression: a rerun's TASKLIST_ROOT deliverable trees written
        into the bundle root must be relocated to the canonical TASKLIST_ROOT — or
        the merge must fail loudly (PARTIAL with a ``deliverable-not-landed:`` audit
        entry). It must NEVER report SUCCESS while deliverables stay stranded inside
        the bundle (the pre-Fix-1 silent-data-loss behavior)."""
        source_index, _release_dir, results_dir = _seed_release(tmp_path, phase=7)
        bundle = _bundle_with_sidecar(
            tmp_path, bundle_id="rerun-strand", phase=7, task_ids=["T07.11"]
        )
        # Fixture geometry: _bundle_with_sidecar anchors the placeholder DIRECTLY
        # in bundle_dir, so bundle.artifacts_produced[0].parent.parent (the same
        # formula Step 3.5 uses to derive bundle_root) resolves to tmp_path/"bundles"
        # here — NOT the production <bundle>/results/ nesting. Seed the deliverable
        # trees under that derived bundle_root so test-seed and relocation-read agree.
        bundle_root = bundle.artifacts_produced[0].parent.parent
        module_src = bundle_root / "artifacts" / "D-0711" / "module.py"
        module_src.parent.mkdir(parents=True, exist_ok=True)
        module_src.write_text("print('rerun deliverable')", encoding="utf-8")
        proof_src = bundle_root / "evidence" / "T07.11" / "proof.md"
        proof_src.parent.mkdir(parents=True, exist_ok=True)
        proof_src.write_text("evidence body", encoding="utf-8")

        # Canonical destinations are mirrored under the canonical TASKLIST_ROOT
        # (= source_index.parent, which is tmp_path in this fixture).
        canonical_root = source_index.parent
        module_dest = canonical_root / "artifacts" / "D-0711" / "module.py"
        proof_dest = canonical_root / "evidence" / "T07.11" / "proof.md"

        merge_recovery_bundle(
            bundle,
            source_index,
            release_dir=tmp_path,
            expected_deliverables={"T07.11": [module_dest, proof_dest]},
        )

        # Load-bearing coupling (REPORT Test-A spec): EITHER the trees landed in
        # canonical with content preserved AND status SUCCESS, OR status PARTIAL
        # with a non-empty failures list carrying a deliverable-not-landed entry.
        audit_log = results_dir / "recovery-audit.log"
        merge_events = [
            json.loads(line)
            for line in audit_log.read_text(encoding="utf-8").splitlines()
            if line.strip() and json.loads(line).get("event") == "merge_recovery_bundle"
        ]
        assert merge_events, "merge must write a merge_recovery_bundle audit event"
        failures = merge_events[-1].get("failures", [])

        landed = (
            module_dest.is_file()
            and module_dest.read_text(encoding="utf-8") == "print('rerun deliverable')"
            and proof_dest.is_file()
            and proof_dest.read_text(encoding="utf-8") == "evidence body"
        )
        if bundle.status is RecoveryStatus.SUCCESS:
            assert landed, (
                "SUCCESS requires the deliverable trees to have landed in "
                "canonical with content preserved (never stranded-but-SUCCESS)"
            )
        else:
            assert bundle.status is RecoveryStatus.PARTIAL
            assert any(f.startswith("deliverable-not-landed:") for f in failures), (
                "a stranded deliverable must produce a deliverable-not-landed failure"
            )

    def test_merge_partial_when_declared_not_landed_in_canonical(self, tmp_path: Path):
        """DEV-3 (Drift, MED): the landing-verify must check the CANONICAL mirror
        only. A declared deliverable resolves against cwd, which need not equal
        the canonical root; if relocation never lands the tree in canonical but a
        stale/pre-existing file exists at the non-canonical declared path, the
        pre-fix OR-clause (``... or declared.is_file()``) reports it as landed and
        the merge silently reports SUCCESS. Here the bundle has a sidecar (SUCCESS
        reachable) and NO deliverable tree under the bundle root (so relocation
        copies nothing), yet a stale declared file exists at a NON-canonical path.
        Pre-fix: SUCCESS (the masking bug). Post-fix: PARTIAL with a
        ``deliverable-not-landed:`` failure."""
        source_index, _release_dir, results_dir = _seed_release(tmp_path, phase=7)
        bundle = _bundle_with_sidecar(
            tmp_path, bundle_id="rerun-notland", phase=7, task_ids=["T07.11"]
        )
        # Deliberately seed NO artifacts/ tree under the bundle root → relocation
        # copies nothing, so the canonical destination is never created.
        canonical_root = source_index.parent
        canonical_dest = canonical_root / "artifacts" / "D-0711" / "module.py"
        assert not canonical_dest.exists()
        # Stale, pre-existing file at a NON-canonical declared path (resolves
        # against a cwd-like location, NOT under canonical_root).
        stale_declared = tmp_path / "stale_cwd" / "artifacts" / "D-0711" / "module.py"
        stale_declared.parent.mkdir(parents=True, exist_ok=True)
        stale_declared.write_text("stale pre-existing content", encoding="utf-8")
        assert stale_declared.resolve() != canonical_dest.resolve()

        merge_recovery_bundle(
            bundle,
            source_index,
            release_dir=tmp_path,
            expected_deliverables={"T07.11": [stale_declared]},
        )

        audit_log = results_dir / "recovery-audit.log"
        merge_events = [
            json.loads(line)
            for line in audit_log.read_text(encoding="utf-8").splitlines()
            if line.strip() and json.loads(line).get("event") == "merge_recovery_bundle"
        ]
        assert merge_events, "merge must write a merge_recovery_bundle audit event"
        failures = merge_events[-1].get("failures", [])

        # The deliverable never reached canonical, so the merge MUST NOT report
        # SUCCESS via the stale non-canonical declared file.
        assert bundle.status is RecoveryStatus.PARTIAL, (
            "a declared deliverable absent from canonical must downgrade to "
            "PARTIAL even when a stale non-canonical declared file exists"
        )
        assert any(f.startswith("deliverable-not-landed:") for f in failures), (
            "the canonical mirror is missing — a deliverable-not-landed failure "
            "must be recorded (the OR-clause must not mask it)"
        )
        # And the canonical destination genuinely never materialized.
        assert not canonical_dest.exists()


# ---------------------------------------------------------------------------
# write_recovery_audit_log — shared JSONL audit writer
# ---------------------------------------------------------------------------


class TestSharedAuditLogWriter:
    def test_writer_appends_jsonl_line_with_timestamp(self, tmp_path: Path):
        """``write_recovery_audit_log`` creates the parent dir, appends one JSONL
        line per call, and injects an ISO-8601 ``timestamp`` into the payload."""
        audit_log = tmp_path / "results" / "recovery-audit.log"
        write_recovery_audit_log(audit_log, {"event": "alpha", "bundle_id": "b1"})
        write_recovery_audit_log(audit_log, {"event": "beta", "bundle_id": "b2"})

        assert audit_log.exists()
        lines = [
            json.loads(line)
            for line in audit_log.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        assert len(lines) == 2
        assert [e["event"] for e in lines] == ["alpha", "beta"]
        assert lines[0]["bundle_id"] == "b1"
        # Timestamp injected by the writer and parseable as ISO-8601.
        from datetime import datetime

        assert "timestamp" in lines[0]
        datetime.fromisoformat(lines[0]["timestamp"])


# ---------------------------------------------------------------------------
# Recovery surface smoke checks (nominators, lock helpers, retry counter)
# ---------------------------------------------------------------------------


class TestRecoverySurfaceSmoke:
    def test_manual_nominator_returns_explicit_task_ids(self):
        nominator = ManualNominator(phase=7, tasks=["T07.11", "T07.12"])
        assert nominator.nominate({}) == ["T07.11", "T07.12"]

    def test_reflect_report_nominator_missing_file_returns_empty(self, tmp_path: Path):
        nominator = ReflectReportNominator(tmp_path / "no-such-report.json")
        assert nominator.nominate({}) == []

    def test_lock_acquire_then_release_round_trip(self, tmp_path: Path):
        lock_path = acquire_recovery_lock(tmp_path, phase=7)
        assert lock_path.exists()
        release_recovery_lock(lock_path)
        assert not lock_path.exists()
        # Idempotent: releasing an already-removed lock is a no-op.
        release_recovery_lock(lock_path)

    def test_retry_count_for_task_counts_matching_bundles(self):
        from superclaude.cli.sprint.models import Phase, PhaseResult

        phase_result = PhaseResult(phase=Phase(number=7, file=Path(".")))
        phase_result.recovery_history = [
            RecoveryBundle(bundle_id="b1", affected_phase=7, affected_tasks=["T07.11"]),
            RecoveryBundle(bundle_id="b2", affected_phase=7, affected_tasks=["T07.12"]),
            # A compact ref carries no affected_tasks → not counted.
            RecoveryBundleRef(
                bundle_id="b3",
                path=Path("recovery-bundle-b3.json"),
                status=RecoveryStatus.SUCCESS,
            ),
        ]
        assert retry_count_for_task(phase_result, "T07.11") == 1
        assert retry_count_for_task(phase_result, "T99.99") == 0


# ---------------------------------------------------------------------------
# R7 — Release-scoped run lock (13-case matrix)
# ---------------------------------------------------------------------------


def _write_run_lock(tmp_path: Path, payload: dict) -> Path:
    """Pre-write a run.lock under tmp_path/.recovery-locks with ``payload``."""
    locks_dir = tmp_path / ".recovery-locks"
    locks_dir.mkdir(parents=True, exist_ok=True)
    lock_path = locks_dir / "run.lock"
    lock_path.write_text(json.dumps(payload), encoding="utf-8")
    return lock_path


class TestRunLock:
    def test_run_lock_acquire_creates_file_with_payload(self, tmp_path: Path):
        # Case 1: acquire creates the lockfile with a pid+payload.
        path = acquire_run_lock(tmp_path)
        try:
            assert path == tmp_path / ".recovery-locks" / "run.lock"
            assert path.exists()
            payload = json.loads(path.read_text(encoding="utf-8"))
            assert payload["pid"] == os.getpid()
            assert "starttime" in payload
            assert "timestamp" in payload
            assert "hostname" in payload
        finally:
            release_run_lock(path)

    def test_run_lock_live_holder_refused_naming_pid(self, tmp_path: Path):
        # Case 2: a live holder raises ClickException naming PID + timestamp.
        holder_pid = os.getpid()  # self is guaranteed alive
        ts = "2026-06-17T00:00:00+00:00"
        _write_run_lock(
            tmp_path,
            {"pid": holder_pid, "starttime": None, "timestamp": ts},
        )
        with pytest.raises(click.ClickException) as excinfo:
            acquire_run_lock(tmp_path)
        msg = excinfo.value.format_message()
        assert str(holder_pid) in msg
        assert ts in msg
        assert "--ignore-run-lock" in msg

    def test_run_lock_reclaims_stale_dead_pid(self, tmp_path: Path, monkeypatch):
        # Case 3: stale dead-PID lock is reclaimed (os.kill -> ProcessLookupError).
        _write_run_lock(
            tmp_path,
            {"pid": 424242, "starttime": None, "timestamp": "t"},
        )

        def _dead(pid, sig):
            raise ProcessLookupError

        monkeypatch.setattr(os, "kill", _dead)
        path = acquire_run_lock(tmp_path)
        try:
            assert path.exists()
            payload = json.loads(path.read_text(encoding="utf-8"))
            assert payload["pid"] == os.getpid()
        finally:
            release_run_lock(path)

    def test_run_lock_permission_error_treated_alive(self, tmp_path: Path, monkeypatch):
        # Case 4: PermissionError from os.kill -> treated alive -> refuse.
        _write_run_lock(
            tmp_path,
            {"pid": 424242, "starttime": None, "timestamp": "t"},
        )

        def _perm(pid, sig):
            raise PermissionError

        monkeypatch.setattr(os, "kill", _perm)
        with pytest.raises(click.ClickException):
            acquire_run_lock(tmp_path)

    def test_run_lock_atomic_link_loser_refused(self, tmp_path: Path, monkeypatch):
        # Case 5: the atomic-create loser is refused and never overwrites the winner.
        # Acquisition is now temp-file + os.link (PR #184 review: link-after-write
        # eliminates the empty-file window), so the loser is the one whose os.link
        # raises FileExistsError. (os.open is NOT patched — mkstemp uses it.)
        winner_payload = {"pid": os.getpid(), "starttime": None, "timestamp": "winner"}
        lock_path = _write_run_lock(tmp_path, winner_payload)
        original = lock_path.read_text(encoding="utf-8")

        def _always_exists(*args, **kwargs):
            raise FileExistsError

        # Concurrent winner already holds the lock and is alive; the bounded
        # retry exhausts and the acquirer refuses, never clobbering the payload.
        monkeypatch.setattr(os, "link", _always_exists)
        monkeypatch.setattr(os, "kill", lambda pid, sig: None)  # alive
        with pytest.raises(click.ClickException):
            acquire_run_lock(tmp_path)
        assert lock_path.read_text(encoding="utf-8") == original

    def test_run_lock_released_on_atexit(self, tmp_path: Path, monkeypatch):
        # Case 6: lock released via the atexit-registered callback.
        import atexit

        captured = []
        monkeypatch.setattr(atexit, "register", lambda fn, *a, **k: captured.append(fn))
        path = acquire_run_lock(tmp_path)
        assert path.exists()
        assert captured, "no atexit callback was registered"
        for fn in captured:
            fn()
        assert not path.exists()

    def test_run_lock_released_on_sigterm(self, tmp_path: Path, monkeypatch):
        # Case 7: lock released by the SIGTERM handler.
        import signal as _signal

        handlers = {}

        def _capture(sig, handler):
            handlers[sig] = handler
            return None

        monkeypatch.setattr(_signal, "signal", _capture)
        # Previous handler is SIG_DFL: the handler restores SIG_DFL and re-raises via
        # os.kill so SIGTERM is NOT swallowed (PR #184 review). Capture os.kill so the
        # re-raise is recorded rather than actually terminating the test process.
        monkeypatch.setattr(_signal, "getsignal", lambda sig: _signal.SIG_DFL)
        killed: list = []
        monkeypatch.setattr(os, "kill", lambda pid, sig: killed.append((pid, sig)))
        path = acquire_run_lock(tmp_path)
        assert path.exists()
        assert _signal.SIGTERM in handlers
        handlers[_signal.SIGTERM](_signal.SIGTERM, None)
        assert not path.exists()
        assert killed == [(os.getpid(), _signal.SIGTERM)]  # re-raised, not swallowed

    def test_run_lock_released_on_sigint(self, tmp_path: Path, monkeypatch):
        # Case 8: lock released by the SIGINT handler (closes R1.2 weakness).
        import signal as _signal

        handlers = {}

        def _capture(sig, handler):
            handlers[sig] = handler
            return None

        monkeypatch.setattr(_signal, "signal", _capture)
        # Previous handler is SIG_DFL: handler restores SIG_DFL and re-raises via
        # os.kill so SIGINT is NOT swallowed (PR #184 review). Capture os.kill so the
        # re-raise is recorded rather than terminating the test process.
        monkeypatch.setattr(_signal, "getsignal", lambda sig: _signal.SIG_DFL)
        killed: list = []
        monkeypatch.setattr(os, "kill", lambda pid, sig: killed.append((pid, sig)))
        path = acquire_run_lock(tmp_path)
        assert path.exists()
        assert _signal.SIGINT in handlers
        handlers[_signal.SIGINT](_signal.SIGINT, None)
        assert not path.exists()
        assert killed == [(os.getpid(), _signal.SIGINT)]  # re-raised, not swallowed

    def test_run_lock_force_bypasses_live_holder(self, tmp_path: Path, monkeypatch):
        # Case 9: force=True reclaims even a live holder.
        ts = "2026-06-17T00:00:00+00:00"
        _write_run_lock(
            tmp_path,
            {"pid": os.getpid(), "starttime": None, "timestamp": ts},
        )
        monkeypatch.setattr(os, "kill", lambda pid, sig: None)  # alive
        # Confirm force=False would refuse.
        with pytest.raises(click.ClickException):
            acquire_run_lock(tmp_path)
        path = acquire_run_lock(tmp_path, force=True)
        try:
            assert path.exists()
            payload = json.loads(path.read_text(encoding="utf-8"))
            assert payload["pid"] == os.getpid()
        finally:
            release_run_lock(path)

    def test_run_lock_corrupt_json_reclaimed(self, tmp_path: Path):
        # Case 10: corrupt/torn JSON is tolerated -> treated dead -> reclaimed.
        locks_dir = tmp_path / ".recovery-locks"
        locks_dir.mkdir(parents=True, exist_ok=True)
        (locks_dir / "run.lock").write_text("{not valid json", encoding="utf-8")
        path = acquire_run_lock(tmp_path)
        try:
            assert path.exists()
            payload = json.loads(path.read_text(encoding="utf-8"))
            assert payload["pid"] == os.getpid()
        finally:
            release_run_lock(path)

    def test_run_lock_double_release_idempotent(self, tmp_path: Path):
        # Case 11: double release_run_lock is a no-op.
        path = acquire_run_lock(tmp_path)
        release_run_lock(path)
        assert not path.exists()
        # Second release must not raise and must not change state.
        release_run_lock(path)
        assert not path.exists()

    def test_run_and_recovery_locks_coexist_distinct_paths(self, tmp_path: Path):
        # Case 12: run lock + recovery lock coexist (distinct paths, no error).
        phase_lock = acquire_recovery_lock(tmp_path, phase=7)
        run_lock = acquire_run_lock(tmp_path)
        try:
            assert phase_lock == tmp_path / ".recovery-locks" / "phase-7.lock"
            assert run_lock == tmp_path / ".recovery-locks" / "run.lock"
            assert phase_lock.exists()
            assert run_lock.exists()
            assert phase_lock != run_lock
        finally:
            release_recovery_lock(phase_lock)
            release_run_lock(run_lock)

    def test_run_lock_pid_reuse_starttime_mismatch_reclaimed(
        self, tmp_path: Path, monkeypatch
    ):
        # Case 13: live PID but starttime mismatch -> treated dead -> reclaimed.
        from superclaude.cli.sprint import recovery as _recovery

        _write_run_lock(
            tmp_path,
            {"pid": 424242, "starttime": "1000", "timestamp": "t"},
        )
        # os.kill succeeds (PID appears alive) ...
        monkeypatch.setattr(os, "kill", lambda pid, sig: None)
        # ... but the current starttime differs from the recorded "1000".
        monkeypatch.setattr(_recovery, "_read_proc_starttime", lambda pid: "9999")
        path = acquire_run_lock(tmp_path)
        try:
            assert path.exists()
            payload = json.loads(path.read_text(encoding="utf-8"))
            assert payload["pid"] == os.getpid()
        finally:
            release_run_lock(path)
