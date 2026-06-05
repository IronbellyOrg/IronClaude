"""T06.04 -- FR-015 ``swarm run --resume <job_id>`` end-to-end.

Covers roadmap row R-113 (FR-015): the resume orchestrator in
:func:`superclaude.cli.swarm.commands.run_cmd` must locate the prior
job's ``manifest.json`` under ``--output``, rehydrate the JobSpec via
:func:`preflight.resume_mode` (INV-001 manifest source-of-truth),
classify per-worker status from ``*.meta.json`` sidecars, skip the
succeeded slots, re-dispatch the remaining slots only, re-run Wave 2
normalize on the redispatched workers, and regenerate ``merged.md``
via :func:`reduce_wave3` with ``resume=True`` (INV-010).

The acceptance contract this module pins (phase-6-tasklist.md §T06.04):

    * **Succeeded workers skipped** -- a slot whose sidecar reports
      ``status: success`` is NOT passed to ``dispatch_wave1`` again.
    * **Remaining slots re-dispatched** -- only the slots whose
      sidecars are missing or report a non-success status flow into the
      redispatch.
    * **Merge regenerated** -- ``merged.md`` produced by the prior run
      is removed and rewritten when ``amalgamation_mode==normalize+merge``.
    * **swarm run --resume exits 0 on success** -- the success line on
      stdout names the job_id, total worker count, skipped count, and
      redispatched count.
    * **No duplicate worker outputs** -- combined slot list is
      slot-aligned (each slot index appears at most once).

The test uses ``--transport stub`` for transport semantics and
monkeypatches :func:`dispatch_wave1` for slot-level visibility into
the redispatch call. Sidecars are pre-staged on disk to simulate a
crashed prior run.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm.commands import (
    EXIT_OK,
    EXIT_USAGE,
    discover_succeeded_slots,
    run_cmd,
)
from superclaude.cli.swarm.models import (
    Manifest,
    PreflightSummary,
    ResolvedLensEntry,
    WorkerResult,
    to_json,
)
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

# ---------------------------------------------------------------------------
# Fixture helpers -- mirror the on-disk shape the executor would produce.
# ---------------------------------------------------------------------------


JOB_ID: str = "job-resume-T06.04"
LENS_NAME: str = "bare-review"
RECIPE_NAME: str = "bare-review-v1"
TRANSPORT_KIND: str = "stub"
NEXT_CMD: str = "sc:reflect on {job_id}"


def _resolved_lens() -> ResolvedLensEntry:
    return ResolvedLensEntry(
        name=LENS_NAME,
        system_prompt_fragment=(
            "You are a bare reviewer. " + CANONICAL_INJECTION_GUARD_SENTENCE
        ),
        user_template="Review: {{target}}",
        recipe_name=RECIPE_NAME,
        default_workers=3,
        suspect=True,
        tier="T2",
        recommended_next_command_template=NEXT_CMD,
        stability="stable",
    )


def _write_manifest(
    output_dir: Path,
    *,
    workers_requested: int = 3,
    job_id: str = JOB_ID,
    transport_kind: str = TRANSPORT_KIND,
) -> Path:
    """Emit ``output_dir/manifest.json`` for the resume orchestrator to load."""
    manifest = Manifest(
        contract_version="1.0",
        job_id=job_id,
        resolved_lens_entry=_resolved_lens(),
        preflight=PreflightSummary(
            target_checksum="a" * 64,
            workers_requested=workers_requested,
            transport_kind=transport_kind,
        ),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "manifest.json"
    path.write_text(to_json(manifest), encoding="utf-8")
    return path


def _write_succeeded_sidecar(
    output_dir: Path,
    *,
    slot_index: int,
    model_slug: str = "stub-model",
    body: str = "succeeded body from prior run\n",
) -> tuple[Path, Path]:
    """Write a ``*.meta.json`` + ``*.final.md`` pair for a succeeded slot.

    Returns ``(meta_path, final_path)`` so the test can assert that the
    resume orchestrator preserves these artefacts verbatim (no rewrite).
    """
    stem = f"{LENS_NAME}-{slot_index:02d}-{model_slug}"
    final_path = output_dir / f"{stem}.final.md"
    final_path.write_text(body, encoding="utf-8")
    meta_path = output_dir / f"{stem}.meta.json"
    meta_payload = {
        "recipe": RECIPE_NAME,
        "schema_version": "1.0",
        "salvaged": False,
        "status": "success",
        "bytes": len(body.encode("utf-8")),
    }
    meta_path.write_text(
        json.dumps(meta_payload, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return meta_path, final_path


# ---------------------------------------------------------------------------
# discover_succeeded_slots -- standalone helper contract
# ---------------------------------------------------------------------------


def test_discover_returns_empty_when_no_sidecars(tmp_path: Path) -> None:
    """No sidecars on disk -> empty dict; resume should redispatch every slot."""
    assert discover_succeeded_slots(tmp_path, workers_requested=3) == {}


def test_discover_returns_empty_when_dir_missing(tmp_path: Path) -> None:
    """Missing output_dir is tolerated -- defensive guard."""
    missing = tmp_path / "does-not-exist"
    assert discover_succeeded_slots(missing, workers_requested=3) == {}


def test_discover_returns_succeeded_slots(tmp_path: Path) -> None:
    """Each well-formed sidecar with status=success surfaces in the map."""
    _write_succeeded_sidecar(tmp_path, slot_index=0)
    _write_succeeded_sidecar(tmp_path, slot_index=2)

    succeeded = discover_succeeded_slots(tmp_path, workers_requested=3)

    assert set(succeeded) == {0, 2}
    assert succeeded[0].status == "success"
    assert succeeded[2].status == "success"
    # final_path points at the on-disk body.
    assert Path(succeeded[0].final_path).exists()
    assert Path(succeeded[2].final_path).exists()


def test_discover_ignores_failed_sidecars(tmp_path: Path) -> None:
    """Non-success sidecars are excluded so the slot is redispatched."""
    _write_succeeded_sidecar(tmp_path, slot_index=0)
    # Slot 1 -- timeout sidecar; must NOT count as succeeded.
    failed_meta = tmp_path / f"{LENS_NAME}-01-stub-model.meta.json"
    failed_meta.write_text(
        json.dumps({"status": "timeout", "bytes": 0}),
        encoding="utf-8",
    )

    succeeded = discover_succeeded_slots(tmp_path, workers_requested=3)
    assert set(succeeded) == {0}


def test_discover_ignores_out_of_range_slots(tmp_path: Path) -> None:
    """Stale sidecars from a larger fan-out must not pollute the result."""
    _write_succeeded_sidecar(tmp_path, slot_index=0)
    _write_succeeded_sidecar(tmp_path, slot_index=5)  # outside [0, 3)

    succeeded = discover_succeeded_slots(tmp_path, workers_requested=3)
    assert set(succeeded) == {0}


def test_discover_tolerates_corrupt_sidecar(tmp_path: Path) -> None:
    """A corrupt sidecar does not abort discovery -- slot is just redispatched."""
    _write_succeeded_sidecar(tmp_path, slot_index=0)
    bad = tmp_path / f"{LENS_NAME}-01-stub-model.meta.json"
    bad.write_text("not json{{{", encoding="utf-8")

    succeeded = discover_succeeded_slots(tmp_path, workers_requested=3)
    assert set(succeeded) == {0}


# ---------------------------------------------------------------------------
# --resume CLI flag -- usage validation
# ---------------------------------------------------------------------------


def test_resume_requires_output_flag(tmp_path: Path) -> None:
    """--resume without --output exits with EXIT_USAGE."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--resume", JOB_ID])
    assert result.exit_code == EXIT_USAGE, (
        f"expected EXIT_USAGE; got {result.exit_code}\nstderr:\n{result.stderr}"
    )
    assert "--output" in result.stderr


def test_resume_mutually_exclusive_with_spec_path(tmp_path: Path) -> None:
    """--resume and SPEC_PATH together exit EXIT_USAGE."""
    spec_path = tmp_path / "spec.json"
    spec_path.write_text("{}", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            str(spec_path),
            "--resume",
            JOB_ID,
            "--output",
            str(tmp_path / "out"),
        ],
    )
    assert result.exit_code == EXIT_USAGE
    assert "mutually exclusive" in result.stderr


def test_resume_mutually_exclusive_with_lens(tmp_path: Path) -> None:
    """--resume and --lens together exit EXIT_USAGE."""
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            "--resume",
            JOB_ID,
            "--lens",
            LENS_NAME,
            "--output",
            str(tmp_path / "out"),
        ],
    )
    assert result.exit_code == EXIT_USAGE
    assert "mutually exclusive" in result.stderr


def test_resume_missing_manifest_exits_usage(tmp_path: Path) -> None:
    """No manifest.json under --output -> EXIT_USAGE with actionable diagnostic."""
    runner = CliRunner()
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = runner.invoke(
        run_cmd,
        ["--resume", JOB_ID, "--output", str(out_dir)],
    )
    assert result.exit_code == EXIT_USAGE
    assert "manifest.json" in result.stderr


def test_resume_job_id_mismatch_exits_usage(tmp_path: Path) -> None:
    """Wrong --resume <job_id> for the manifest content exits EXIT_USAGE."""
    out_dir = tmp_path / "out"
    _write_manifest(out_dir, job_id="actual-job-id")
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        ["--resume", "different-job-id", "--output", str(out_dir)],
    )
    assert result.exit_code == EXIT_USAGE
    assert "job_id mismatch" in result.stderr


def test_resume_advertised_in_help() -> None:
    """``--help`` lists the new --resume flag."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--help"])
    assert result.exit_code == 0
    assert "--resume" in result.output


# ---------------------------------------------------------------------------
# Kill-then-resume end-to-end -- the canonical T06.04 §3 verification.
# ---------------------------------------------------------------------------


def test_resume_skips_succeeded_workers_and_redispatches_remaining(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: skip succeeded workers; only redispatch the remaining slots.

    Compose the §T06.04 kill-then-resume scenario:

        1. Prior run dispatched 3 workers; slot 0 succeeded (sidecar +
           final body on disk), slots 1 and 2 crashed before reporting.
        2. Resume locates the manifest, classifies slot 0 as succeeded,
           and re-dispatches slots 1 and 2.
        3. The fake dispatch records how many workers it was asked to
           run; the assertion proves the redispatch is sized to the
           remaining set, not the original N.
    """
    out_dir = tmp_path / "out"
    _write_manifest(out_dir, workers_requested=3)
    _write_succeeded_sidecar(out_dir, slot_index=0, body="slot-0 prior body\n")

    captured: dict[str, Any] = {}

    def _fake_dispatch(
        preflight_result: Any, transport: Any = None, **kwargs: Any
    ) -> list[WorkerResult]:
        captured["workers_requested"] = (
            preflight_result.manifest.preflight.workers_requested
        )
        captured["job_id"] = preflight_result.manifest.job_id
        captured["transport_kind"] = (
            preflight_result.manifest.preflight.transport_kind
        )
        captured["resolved_lens_name"] = (
            preflight_result.manifest.resolved_lens_entry.name
        )
        # Return one success per slot requested -- the redispatch
        # succeeds for both remaining workers.
        return [
            WorkerResult(
                index=i,
                status="success",
                model_id=f"fresh-model-{i}",
                model_label=f"fresh-model-{i}",
            )
            for i in range(preflight_result.manifest.preflight.workers_requested)
        ]

    import superclaude.cli.swarm.commands as commands_mod
    import superclaude.cli.swarm.dispatch as dispatch_mod

    # The resume branch imports dispatch_wave1 lazily; patch on the source
    # module so the lazy import inside the function picks up the fake.
    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _fake_dispatch)
    monkeypatch.setattr(commands_mod, "dispatch_wave1", _fake_dispatch, raising=False)

    # Wave 2 normalize: stub out so the test doesn't depend on the recipe
    # registry. The orchestrator must call this for the redispatched
    # workers only (not the succeeded slot 0).
    normalize_calls: list[list[WorkerResult]] = []

    def _fake_normalize(
        worker_results: list[WorkerResult], recipe_name: str, **kwargs: Any
    ) -> list[WorkerResult]:
        normalize_calls.append(list(worker_results))
        return list(worker_results)

    import superclaude.cli.swarm.normalize as normalize_mod
    monkeypatch.setattr(normalize_mod, "normalize_wave2", _fake_normalize)

    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        ["--resume", JOB_ID, "--output", str(out_dir)],
    )

    assert result.exit_code == EXIT_OK, (
        f"resume should exit 0; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    # The redispatch saw only the remaining 2 slots, not all 3.
    assert captured["workers_requested"] == 2
    # The synthetic preflight carried the manifest job_id verbatim.
    assert captured["job_id"] == JOB_ID
    # Transport kind comes from the manifest (no --transport override).
    assert captured["transport_kind"] == TRANSPORT_KIND
    # Lens name comes from the manifest snapshot (INV-001).
    assert captured["resolved_lens_name"] == LENS_NAME

    # Normalize was called once, with the 2 redispatched workers only.
    assert len(normalize_calls) == 1
    assert len(normalize_calls[0]) == 2

    # Stdout success line names the job_id and the slot counts.
    assert "skipped=1" in result.stdout
    assert "redispatched=2" in result.stdout
    assert JOB_ID in result.stdout


def test_resume_all_workers_succeeded_skips_redispatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When every slot succeeded, dispatch must not be called at all."""
    out_dir = tmp_path / "out"
    _write_manifest(out_dir, workers_requested=3)
    for index in range(3):
        _write_succeeded_sidecar(out_dir, slot_index=index)

    dispatch_calls: list[Any] = []

    def _fake_dispatch(
        preflight_result: Any, transport: Any = None, **kwargs: Any
    ) -> list[WorkerResult]:
        dispatch_calls.append(preflight_result)
        return []

    import superclaude.cli.swarm.dispatch as dispatch_mod
    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _fake_dispatch)

    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        ["--resume", JOB_ID, "--output", str(out_dir)],
    )

    assert result.exit_code == EXIT_OK
    # No redispatch happened.
    assert dispatch_calls == []
    assert "skipped=3" in result.stdout
    assert "redispatched=0" in result.stdout


def test_resume_regenerates_merged_md(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: merge regenerated when amalgamation_mode == normalize+merge.

    Pre-stage a stale ``merged.md`` from the notional prior run. After
    resume completes, the file body must reflect the re-dispatched
    workers (or be absent when M < floor); the stale bytes must not
    survive.
    """
    out_dir = tmp_path / "out"
    _write_manifest(out_dir, workers_requested=3)
    for index in range(3):
        _write_succeeded_sidecar(out_dir, slot_index=index)

    stale_merged = out_dir / "merged.md"
    stale_bytes = b"STALE-MERGED-BODY-MUST-NOT-SURVIVE\n"
    stale_merged.write_bytes(stale_bytes)

    # No redispatch is needed (everything succeeded). reduce_wave3 with
    # resume=True must regenerate merged.md from the current worker set
    # via the mechanical_merge module; monkeypatch the merge module to
    # return a deterministic body so the assertion is byte-stable.
    import superclaude.cli.swarm.merge as merge_mod
    monkeypatch.setattr(
        merge_mod,
        "mechanical_merge",
        lambda workers: f"FRESH-MERGE\nN={len(workers)}\n",
    )

    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        ["--resume", JOB_ID, "--output", str(out_dir)],
    )

    assert result.exit_code == EXIT_OK, (
        f"resume should exit 0; stderr:\n{result.stderr}"
    )
    # Stale bytes are gone; fresh body landed.
    assert stale_merged.exists()
    fresh_body = stale_merged.read_text(encoding="utf-8")
    assert "STALE-MERGED-BODY-MUST-NOT-SURVIVE" not in fresh_body
    assert "FRESH-MERGE" in fresh_body


def test_resume_transport_override_wins_over_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``--transport openai_compat`` override flows into the synthetic preflight."""
    out_dir = tmp_path / "out"
    _write_manifest(out_dir, workers_requested=3, transport_kind="stub")
    # Two slots remaining so dispatch is actually invoked.
    _write_succeeded_sidecar(out_dir, slot_index=0)

    captured: dict[str, Any] = {}

    def _fake_dispatch(
        preflight_result: Any, transport: Any = None, **kwargs: Any
    ) -> list[WorkerResult]:
        captured["transport_kind"] = (
            preflight_result.manifest.preflight.transport_kind
        )
        return [
            WorkerResult(index=i, status="success")
            for i in range(preflight_result.manifest.preflight.workers_requested)
        ]

    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.normalize as normalize_mod

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _fake_dispatch)
    monkeypatch.setattr(
        normalize_mod,
        "normalize_wave2",
        lambda workers, recipe_name, **kw: list(workers),
    )

    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            "--resume",
            JOB_ID,
            "--output",
            str(out_dir),
            "--transport",
            "openai_compat",
        ],
    )

    assert result.exit_code == EXIT_OK, result.stderr
    assert captured["transport_kind"] == "openai_compat"


def test_resume_does_not_call_live_lenses_for_lens_rehydration(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """INV-001 -- live LENSES registry not consulted on resume.

    Mutating the registry between runs MUST NOT influence the rehydrated
    JobSpec. The orchestrator pulls every lens-derived field from the
    manifest's ``resolved_lens_entry`` snapshot.
    """
    out_dir = tmp_path / "out"
    _write_manifest(out_dir, workers_requested=2)
    _write_succeeded_sidecar(out_dir, slot_index=0)

    from superclaude.cli.swarm import preflight as preflight_mod

    invocations: list[str] = []

    def _boom(name: str) -> Any:
        invocations.append(name)
        raise AssertionError(
            "resume must not consult resolve_lens -- INV-001 violation"
        )

    monkeypatch.setattr(preflight_mod, "resolve_lens", _boom)

    # Stub dispatch + normalize so the orchestrator can reach reduce.
    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.normalize as normalize_mod

    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        lambda pf, transport=None, **kw: [
            WorkerResult(index=i, status="success")
            for i in range(pf.manifest.preflight.workers_requested)
        ],
    )
    monkeypatch.setattr(
        normalize_mod,
        "normalize_wave2",
        lambda workers, recipe_name, **kw: list(workers),
    )

    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        ["--resume", JOB_ID, "--output", str(out_dir)],
    )

    assert result.exit_code == EXIT_OK, (
        f"resume should not consult resolve_lens; stderr:\n{result.stderr}"
    )
    assert invocations == []


# ---------------------------------------------------------------------------
# Public surface -- discover_succeeded_slots is exported.
# ---------------------------------------------------------------------------


def test_discover_succeeded_slots_exported() -> None:
    from superclaude.cli.swarm import commands as commands_mod

    assert "discover_succeeded_slots" in commands_mod.__all__
    assert callable(commands_mod.discover_succeeded_slots)
