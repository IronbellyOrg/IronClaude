"""E2E-4 — real-``claude``-subprocess proof for ``rerun-tasks`` recovery.

Sibling to ``test_e2e_rerun_happy_path.py`` (E2E-1). Where E2E-1 proves the
*successful* round-trip (rerun → merge-back), this module proves the two
RECOVERY surfaces of ``sprint rerun-tasks`` against the same unmocked
spawn → stdin-prompt → stdout-capture chain (real ``claude`` shim on ``$PATH``;
NO ``subprocess.Popen`` / ``shutil.which`` mock):

1. **Abort auto-restore (AC8).** When the rerun of a target task FAILS, the
   orchestrator's ``finally`` block (step 15) calls
   ``restore_checkboxes_on_abort`` to revert the step-10 provenance block it
   wrote to the source ``phase-1-tasklist.md`` *before* execution. We prove the
   source tasklist is restored **byte-for-byte** and that no
   ``SUPERCLAUDE-RERUN`` delimiter / ``rerun_in_progress:`` marker survives.

2. **``--restore`` from a bundle.** A ``--no-merge-back`` rerun runs the step-9
   ``stash_and_restore_deliverables`` pass (which always fires, before any
   mutation) and then — on success with merge-back disabled — leaves the bundle
   and its ``preserved/manifest.json`` intact (``exit_code == 0``). Note: only
   the merge-back success branch clears ``restore_info``; the ``--no-merge-back``
   path leaves it set, so the ``finally`` block still reverts the source
   tasklist's provenance — but that touches the tasklist only, NOT the bundle's
   ``preserved/`` stash, which is exactly what ``--restore`` later consumes. We
   then corrupt a canonical deliverable and prove ``rerun-tasks --restore``
   locates the most recent bundle (``most_recent_bundle``) and replays the
   stashed bytes back over the canonical file (``restore_from_bundle``).

Only environmental noise is patched: ``notify._notify`` (no desktop toast) and
``rerun_tasks.subprocess.run`` (the post-merge ``verify-checkpoints --recover``
auto-invoke, which only fires on a merge-back success path — patched defensively
so no second ``superclaude`` CLI is shelled out). ``os.setpgrp`` and
``subprocess.Popen`` are NOT patched — the shim is spawned for real.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from superclaude.cli.sprint.commands import sprint_group
from superclaude.cli.sprint.executor import execute_sprint

_RERUN_DELIM = "SUPERCLAUDE-RERUN"
_IN_PROGRESS_MARKER = "rerun_in_progress:"


def _seed_failed_phase_run(config, claude_shim) -> None:
    """Run the real sprint once so T01.02 lands FAIL_RECOVERABLE on disk.

    Mirrors the E2E-1 setup: the shim fails T01.02 transiently (is_error:true +
    output_tokens:0 → ``_is_transient_failure`` → FAIL_RECOVERABLE), so the
    phase ERRORs and the sprint exits non-zero. This leaves a real
    ``phase-1-result.json`` whose T01.02 entry is ``fail_recoverable`` and real
    per-task transcripts on disk — the precondition the rerun consumes.
    """
    claude_shim.set_failures("T01.02")
    with patch("superclaude.cli.sprint.notify._notify"):
        with pytest.raises(SystemExit) as exc_info:
            execute_sprint(config)
        assert exc_info.value.code == 1


def _invoke_rerun(runner: CliRunner, index: Path, *extra: str):
    """Invoke ``sprint rerun-tasks`` with the verify-checkpoints shell-out mocked."""
    with (
        patch("superclaude.cli.sprint.notify._notify"),
        patch("superclaude.cli.sprint.rerun_tasks.subprocess.run") as mock_verify,
    ):
        result = runner.invoke(
            sprint_group,
            ["rerun-tasks", str(index), *extra],
        )
    return result, mock_verify


@pytest.mark.integration
class TestE2EAbortRestore:
    def test_failed_rerun_restores_source_tasklist_byte_for_byte(
        self, claude_shim, real_release
    ):
        """AC8: a failed rerun reverts the step-10 provenance byte-for-byte.

        The shim fails T01.02 on the rerun too → ``rerun_succeeded`` False →
        merge skipped → the ``finally`` auto-restore (step 15) runs. The source
        ``phase-1-tasklist.md`` must be byte-identical to its pre-rerun content
        (the ``flip_target_checkboxes`` provenance block written at step 10 was
        stripped back out by ``restore_checkboxes_on_abort``).
        """
        config, index = real_release
        phase_tasklist = config.release_dir / "phase-1-tasklist.md"

        _seed_failed_phase_run(config, claude_shim)

        # Capture the EXACT pre-rerun bytes of the source tasklist. At this
        # point no rerun has touched it, so it carries no provenance block.
        pre_bytes = phase_tasklist.read_bytes()
        assert _RERUN_DELIM not in pre_bytes.decode("utf-8"), (
            "precondition: source tasklist already carries a rerun provenance block"
        )

        # Rerun T01.02, but keep it failing so the abort path is exercised.
        # set_failures persists fail_tasks across runs, so T01.02 fails again.
        claude_shim.set_failures("T01.02")
        runner = CliRunner()
        result, _mock_verify = _invoke_rerun(
            runner, index, "--phase", "1", "--tasks", "T01.02"
        )

        # The aborted rerun exits non-zero (merge skipped, source restored).
        assert result.exit_code != 0, result.output

        # --- Proof: the rerun was actually attempted (shim re-ran T01.02) ----
        # The rerun executes against an isolated sub-config, so the run-log
        # reflects only what the rerun re-executed.
        assert claude_shim.run_log() == ["T01.02"], (
            f"rerun did not re-execute exactly T01.02; run_log={claude_shim.run_log()}"
        )

        # --- Proof: byte-for-byte restore of the source tasklist ------------
        post_bytes = phase_tasklist.read_bytes()
        assert post_bytes == pre_bytes, (
            "source tasklist was not restored byte-for-byte after the aborted "
            "rerun; the step-10 provenance block leaked.\n"
            f"--- pre ---\n{pre_bytes.decode('utf-8', 'replace')!r}\n"
            f"--- post ---\n{post_bytes.decode('utf-8', 'replace')!r}"
        )

        # --- Proof: no provenance markers survive on disk -------------------
        post_text = post_bytes.decode("utf-8")
        assert _RERUN_DELIM not in post_text, (
            "SUPERCLAUDE-RERUN delimiter survived the abort restore"
        )
        assert _IN_PROGRESS_MARKER not in post_text, (
            "rerun_in_progress marker survived the abort restore"
        )

    def test_abort_clears_rerun_in_progress_marker(self, claude_shim, real_release):
        """Focused AC8 variant: provenance is written then fully reverted.

        The step-10 ``flip_target_checkboxes`` writes a ``rerun_in_progress:``
        block (proven by the audit log / the merge of E2E-1). After an aborted
        rerun, ``restore_checkboxes_on_abort`` must leave NEITHER the
        ``rerun_in_progress:`` key NOR the ``SUPERCLAUDE-RERUN`` delimiter on the
        source tasklist.
        """
        config, index = real_release
        phase_tasklist = config.release_dir / "phase-1-tasklist.md"

        _seed_failed_phase_run(config, claude_shim)

        # Independent evidence the abort actually wrote-then-reverted provenance:
        # the bundle's recovery audit log records both the flip and the restore.
        claude_shim.set_failures("T01.02")
        runner = CliRunner()
        result, _mock_verify = _invoke_rerun(
            runner, index, "--phase", "1", "--tasks", "T01.02"
        )
        assert result.exit_code != 0, result.output

        post_text = phase_tasklist.read_text(encoding="utf-8")
        assert _IN_PROGRESS_MARKER not in post_text, (
            f"rerun_in_progress survived; tasklist tail:\n{post_text[-400:]!r}"
        )
        assert _RERUN_DELIM not in post_text, (
            f"SUPERCLAUDE-RERUN delimiter survived; tasklist tail:\n{post_text[-400:]!r}"
        )

        # Audit-log corroboration: the abort wrote a flip event AND a restore
        # event into the shared recovery audit log (the provenance really was
        # written then reverted, not merely never written). The log is a JSONL
        # file at ``<results_dir>/recovery-audit.log`` (write_recovery_audit_log
        # / _audit_log_path = bundle_dir.parent / "recovery-audit.log").
        audit_log = config.results_dir / "recovery-audit.log"
        assert audit_log.exists(), "recovery audit log was not written during abort"
        events = {
            json.loads(line).get("event")
            for line in audit_log.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        assert "rerun_checkboxes_flipped" in events, (
            "expected the step-10 flip to be audit-logged"
        )
        assert "rerun_checkboxes_restored" in events, (
            "expected the abort restore to be audit-logged"
        )

    def test_restore_from_bundle_recovers_state(self, claude_shim, real_release):
        """``--restore`` replays a bundle's stashed deliverables.

        Path to a consumable bundle: a SUCCESSFUL ``--no-merge-back`` rerun.
        Step 9 (``stash_and_restore_deliverables``) ALWAYS fires before any
        mutation, copying the target's canonical ``phase-1-task-T01.02-*``
        artifacts into ``<bundle>/preserved/`` with a ``manifest.json``. With
        ``--no-merge-back`` and a passing rerun, the orchestrator exits 0 and
        leaves that bundle on disk. We then CORRUPT the canonical T01.02
        transcript and prove ``rerun-tasks --restore`` locates the bundle via
        ``most_recent_bundle`` and replays the stashed bytes via
        ``restore_from_bundle``.

        ``--restore`` still requires ``--phase`` (commands.py enforces
        ``--phase`` whenever ``--from-reflect-report`` is absent), but the
        short-circuit in ``run_rerun_tasks`` ignores ``--tasks`` once ``restore``
        is set — it operates purely on the most-recent bundle's manifest.
        """
        config, index = real_release
        canonical = config.results_dir / "phase-1-task-T01.02-output.txt"

        _seed_failed_phase_run(config, claude_shim)
        assert canonical.exists(), "precondition: T01.02 transcript was not produced"

        # --- Produce a bundle with a stash via a passing --no-merge-back rerun
        claude_shim.set_failures()  # T01.02 now PASSES on the rerun
        runner = CliRunner()
        result, _mock_verify = _invoke_rerun(
            runner, index, "--phase", "1", "--tasks", "T01.02", "--no-merge-back"
        )
        # Success + merge-back disabled → exit 0, bundle + stash preserved.
        assert result.exit_code == 0, result.output

        bundles = sorted(p for p in config.results_dir.glob("rerun-*") if p.is_dir())
        assert bundles, "no rerun bundle directory was created"
        bundle = bundles[-1]
        manifest_path = bundle / "preserved" / "manifest.json"
        assert manifest_path.exists(), (
            "step-9 stash did not write preserved/manifest.json; "
            f"bundle held: {sorted(p.name for p in bundle.rglob('*'))}"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = manifest.get("entries", [])
        # The stash captured the canonical T01.02 transcript (a real artifact
        # that existed pre-rerun) into the bundle.
        stashed_canonicals = {Path(e["canonical"]) for e in entries}
        assert canonical in stashed_canonicals, (
            "stash manifest did not capture the canonical T01.02 transcript; "
            f"entries={entries}"
        )
        # Bytes the stash preserved (what --restore must replay back).
        stash_entry = next(e for e in entries if Path(e["canonical"]) == canonical)
        preserved_bytes = Path(stash_entry["preserved"]).read_bytes()

        # --- Corrupt the canonical deliverable, then --restore --------------
        sentinel = b"CORRUPTED-BY-TEST: this should be overwritten by --restore\n"
        canonical.write_bytes(sentinel)
        assert canonical.read_bytes() == sentinel

        restore_result, _ = _invoke_rerun(runner, index, "--phase", "1", "--restore")
        assert restore_result.exit_code == 0, restore_result.output

        # --- Proof 1: --restore reports the located bundle + a restore count -
        assert "Restored" in restore_result.output, restore_result.output
        # most_recent_bundle resolves to the bundle we created; the report names
        # that path (the observable that proves discovery happened).
        assert bundle.name in restore_result.output, (
            f"--restore did not name the located bundle {bundle.name}; "
            f"output={restore_result.output!r}"
        )

        # --- Proof 2: the stashed bytes were replayed over the canonical file
        assert canonical.read_bytes() == preserved_bytes, (
            "--restore did not replay the stashed canonical T01.02 bytes; "
            "the corrupted sentinel survived"
        )
        assert canonical.read_bytes() != sentinel
