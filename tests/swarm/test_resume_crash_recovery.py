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
        captured["transport_kind"] = preflight_result.manifest.preflight.transport_kind
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
    assert (
        json.loads((out_dir / "done.json").read_text())["terminal_status"] == "success"
    )


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
    assert (
        json.loads((out_dir / "done.json").read_text())["terminal_status"] == "success"
    )


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


@pytest.mark.parametrize("hazard", ["duplicate", "parent", "symlink", "raw-symlink"])
def test_resume_discovery_rejects_unsafe_inventory(tmp_path, monkeypatch, hazard):
    output = tmp_path / "out"
    manifest_path = _write_manifest(output)
    payload = json.loads(manifest_path.read_text())
    outside = tmp_path / "outside"
    outside.mkdir()
    if hazard == "parent":
        payload["output_filename_template"] = (
            "../outside/{lens}-{index:02d}-{model_slug}.md"
        )
    elif hazard == "symlink":
        (output / "linked").symlink_to(outside, target_is_directory=True)
        payload["output_filename_template"] = (
            "linked/{lens}-{index:02d}-{model_slug}.md"
        )
    else:
        _write_succeeded_sidecar(output, slot_index=0)
        if hazard == "duplicate":
            _write_succeeded_sidecar(output, slot_index=0, model_slug="another-model")
        else:
            raw = outside / "body.md"
            raw.write_text("Outside body stays private.\n")
            (output / f"{LENS_NAME}-00-stub-model.raw.md").symlink_to(raw)
    manifest_path.write_text(json.dumps(payload))
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    calls = []

    def forbidden(*args, **kwargs):
        calls.append(True)
        pytest.fail("unsafe inventory must fail before dispatch")

    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", forbidden)
    result = CliRunner().invoke(run_cmd, ["--resume", JOB_ID, "--output", str(output)])
    assert result.exit_code != 0
    assert calls == []
    assert {p: p.read_bytes() for p in before} == before


def test_discovery_does_not_guess_unrelated_numeric_segment(tmp_path):
    _write_succeeded_sidecar(tmp_path, slot_index=0)
    unrelated = tmp_path / "unrelated-01-record.meta.json"
    unrelated.write_text(json.dumps({"status": "success"}))
    succeeded = discover_succeeded_slots(
        tmp_path,
        3,
        lens_name=LENS_NAME,
        filename_template="{model_slug}-{lens}-slot-{index:02d}.md",
    )
    assert set(succeeded) == {0}


@pytest.mark.parametrize("enabled", [False, True])
@pytest.mark.parametrize("successes", [0, 2, 3])
@pytest.mark.parametrize("skip_all", [False, True])
def test_resume_completion_policy_status_and_order(
    tmp_path, monkeypatch, enabled, successes, skip_all
):
    """A genuine old marker must be retired before every terminal result status."""
    import yaml

    import superclaude.cli.swarm.commands as commands
    import superclaude.cli.swarm.dispatch as dispatch
    import superclaude.cli.swarm.normalize as normalize
    import superclaude.cli.swarm.preflight as preflight
    import superclaude.cli.swarm.reduce as reducer

    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    saved = []
    if skip_all:
        saved = [(p, p.read_bytes()) for p in out.glob("*.meta.json")]
        saved.extend((p, p.read_bytes()) for p in out.glob("*.final.md"))
    else:
        for meta in out.glob("*.meta.json"):
            data = json.loads(meta.read_text())
            data["status"] = "timeout"
            meta.write_text(json.dumps(data))
    assert (out / "done.json").is_file()
    real_rehydrate = preflight.resume_mode

    def rehydrate(*a, **kw):
        spec = real_rehydrate(*a, **kw)
        spec.runtime.on_completion.write_done_sentinel = enabled
        return spec

    monkeypatch.setattr(preflight, "resume_mode", rehydrate)
    calls = []

    def workers(pf, **kwargs):
        calls.append(pf.manifest.preflight.workers_requested)
        return [
            WorkerResult(index=i, status="success" if i < successes else "timeout")
            for i in range(3)
        ]

    monkeypatch.setattr(dispatch, "dispatch_wave1", workers)
    monkeypatch.setattr(normalize, "normalize_wave2", lambda workers, **kwargs: workers)
    events = []
    real_state, real_marker = commands._write_swarm_state, reducer.emit_done_sentinel
    real_contract = reducer.emit_contract

    def contract(*args, **kwargs):
        result = real_contract(*args, **kwargs)
        assert events == ["accepted"]
        events.append("contract")
        return result

    def state(root, value, job_id):
        assert not (out / "done.json").exists()
        if value == "terminal":
            assert events == ["accepted", "contract"]
            assert (out / "return-contract.yaml").is_file()
            events.append("terminal")
        else:
            assert value == "dispatching"
            events.append("accepted")
        return real_state(root, value, job_id)

    def marker(status, contract_path):
        assert (
            json.loads((out / ".swarm-state.json").read_text())["state"] == "terminal"
        )
        assert yaml.safe_load(Path(contract_path).read_text())["status"] == status
        events.append("marker")
        return real_marker(status, contract_path)

    monkeypatch.setattr(commands, "_write_swarm_state", state)
    monkeypatch.setattr(reducer, "emit_contract", contract)
    monkeypatch.setattr(reducer, "emit_done_sentinel", marker)
    result = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
    assert result.exit_code == EXIT_OK, result.output
    assert calls == ([] if skip_all else [3])
    assert events == (
        ["accepted", "contract", "terminal", "marker"]
        if enabled
        else ["accepted", "contract", "terminal"]
    )
    expected = (
        "success"
        if skip_all or successes == 3
        else "partial"
        if successes == 2
        else "failed"
    )
    assert (
        yaml.safe_load((out / "return-contract.yaml").read_text())["status"] == expected
    )
    assert (out / "done.json").exists() is enabled
    if enabled:
        assert json.loads((out / "done.json").read_text()) == {
            "atomic_write": True,
            "terminal_status": expected,
            "contract_path": str((out / "return-contract.yaml").resolve()),
        }
    assert (
        len(
            {
                w["index"]
                for w in yaml.safe_load((out / "return-contract.yaml").read_text())[
                    "output_files"
                ]
            }
        )
        == 3
    )
    for path, original in saved:
        assert path.read_bytes() == original


@pytest.mark.parametrize(
    "failure", ["reduce", "contract", "terminal", "missing", "malformed", "mismatch"]
)
def test_resume_no_marker_on_error(tmp_path, monkeypatch, failure):
    import superclaude.cli.swarm.commands as commands
    import superclaude.cli.swarm.reduce as reducer

    out = tmp_path / "out"
    manifest = _write_manifest(out, workers_requested=3)
    for i in range(3):
        _write_succeeded_sidecar(out, slot_index=i)

    def fail(*a, **kw):
        raise OSError("injected resume persistence failure")

    if failure == "reduce":
        monkeypatch.setattr(reducer, "reduce_wave3", fail)
    elif failure == "contract":
        monkeypatch.setattr(reducer, "emit_contract", fail)
    elif failure == "terminal":
        monkeypatch.setattr(commands, "_write_swarm_state", fail)
    elif failure == "missing":
        manifest.unlink()
    elif failure == "malformed":
        manifest.write_text("not JSON")
    else:
        data = json.loads(manifest.read_text())
        data["job_id"] = "different-job"
        manifest.write_text(json.dumps(data))
    result = CliRunner().invoke(run_cmd, ["--resume", JOB_ID, "--output", str(out)])
    assert result.exit_code != EXIT_OK
    assert not (out / "done.json").exists()


def _artifact_bytes(out):
    return {
        str(p.relative_to(out)): p.read_bytes() for p in out.rglob("*") if p.is_file()
    }


def _completed_stub_run(tmp_path, monkeypatch):
    """Seed a genuine terminal marker through the public CLI, never a fixture marker."""
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    monkeypatch.setenv("HOME", str(home))
    target = tmp_path / "target.md"
    target.write_text("A local simulated review target. " * 12)
    out = tmp_path / "out"
    fresh = CliRunner().invoke(
        run_cmd,
        [
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(target),
            "--output",
            str(out),
        ],
    )
    assert fresh.exit_code == EXIT_OK, fresh.output
    assert (out / "done.json").is_file()
    job_id = json.loads((out / "manifest.json").read_text())["job_id"]
    return out, job_id


def _retry_one(out):
    meta = sorted(out.glob("*.meta.json"))[0]
    data = json.loads(meta.read_text())
    data["status"] = "timeout"
    meta.write_text(json.dumps(data))


def _completion_policy(monkeypatch, enabled):
    import superclaude.cli.swarm.preflight as preflight

    real = preflight.resume_mode

    def rehydrate(*args, **kwargs):
        spec = real(*args, **kwargs)
        spec.runtime.on_completion.write_done_sentinel = enabled
        return spec

    monkeypatch.setattr(preflight, "resume_mode", rehydrate)


@pytest.mark.parametrize("enabled", [True, False])
def test_stale_marker_absent_at_accepted_dispatch(tmp_path, monkeypatch, enabled):
    import superclaude.cli.swarm.dispatch as dispatch

    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    marker = out / "done.json"
    old = marker.read_bytes()
    _retry_one(out)
    _completion_policy(monkeypatch, enabled)
    real_dispatch = dispatch.dispatch_wave1
    seen = []

    def observe(*args, **kwargs):
        seen.append(marker.exists())
        return real_dispatch(*args, **kwargs)

    monkeypatch.setattr(dispatch, "dispatch_wave1", observe)
    result = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
    print(
        f"dispatch-entry enabled={enabled} marker_exists={seen}; "
        f"exit={result.exit_code}; final_marker={marker.exists()}; "
        f"old_bytes_equal={marker.read_bytes() == old if marker.exists() else False}"
    )
    assert result.exit_code == EXIT_OK, result.output
    assert seen == [False], "previous completion marker visible at accepted dispatch"
    assert marker.exists() is enabled


def test_overlapping_resume_preserves_active_fresh_artifacts(tmp_path, monkeypatch):
    import superclaude.cli.swarm.dispatch as dispatch

    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    target = tmp_path / "target.md"
    target.write_text("Local overlap witness. " * 12)
    out = tmp_path / "out"
    real_dispatch = dispatch.dispatch_wave1
    nested = []
    entered = False

    def observe(*args, **kwargs):
        nonlocal entered
        if not entered:
            entered = True
            job_id = json.loads((out / "manifest.json").read_text())["job_id"]
            before = _artifact_bytes(out)
            inner = CliRunner().invoke(
                run_cmd, ["--resume", job_id, "--output", str(out)]
            )
            nested.append((inner.exit_code, before == _artifact_bytes(out)))
        return real_dispatch(*args, **kwargs)

    monkeypatch.setattr(dispatch, "dispatch_wave1", observe)
    result = CliRunner().invoke(
        run_cmd,
        [
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(target),
            "--output",
            str(out),
        ],
    )
    print(f"overlapping_resume result={nested}; fresh_exit={result.exit_code}")
    assert result.exit_code == EXIT_OK, result.output
    assert len(nested) == 1
    assert nested[0][0] != EXIT_OK, "overlapping resume was accepted"
    assert nested[0][1], "rejected overlap changed active invocation artifacts"


@pytest.mark.parametrize("enabled", [True, False])
def test_resume_reduction_retires_old_marker_and_recovers_crash(
    tmp_path, monkeypatch, enabled
):
    import superclaude.cli.swarm.commands as commands
    import superclaude.cli.swarm.reduce as reducer

    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    _completion_policy(monkeypatch, enabled)
    commands._write_swarm_state(out, "dispatching", job_id)
    saved = {p: p.read_bytes() for p in out.glob("*.meta.json")}
    saved.update({p: p.read_bytes() for p in out.glob("*.final.md")})
    real_reduce = reducer.reduce_wave3
    entries = []

    def observe(*args, **kwargs):
        entries.append((out / "done.json").exists())
        return real_reduce(*args, **kwargs)

    monkeypatch.setattr(reducer, "reduce_wave3", observe)
    result = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
    assert result.exit_code == EXIT_OK, result.output
    assert entries == [False]
    assert (out / "done.json").exists() is enabled
    assert all(p.read_bytes() == data for p, data in saved.items())
    assert not commands._ACTIVE_OUTPUTS


@pytest.mark.parametrize("failure", ["validation", "unlink", "dispatch", "interrupt"])
def test_resume_claim_released_after_failure(tmp_path, monkeypatch, failure):
    import superclaude.cli.swarm.commands as commands
    import superclaude.cli.swarm.dispatch as dispatch

    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    _retry_one(out)
    before = _artifact_bytes(out)
    with monkeypatch.context() as patch:
        if failure == "validation":
            invoke_id = "wrong-job"
        else:
            invoke_id = job_id
        if failure == "unlink":
            real_unlink = Path.unlink

            def fail_unlink(path, *args, **kwargs):
                if path == out / "done.json":
                    raise PermissionError("injected old marker unlink failure")
                return real_unlink(path, *args, **kwargs)

            patch.setattr(Path, "unlink", fail_unlink)
        elif failure in ("dispatch", "interrupt"):

            def fail_dispatch(*args, **kwargs):
                raise (
                    KeyboardInterrupt()
                    if failure == "interrupt"
                    else RuntimeError("injected worker failure")
                )

            patch.setattr(dispatch, "dispatch_wave1", fail_dispatch)
        result = CliRunner().invoke(
            run_cmd, ["--resume", invoke_id, "--output", str(out)]
        )
        assert result.exit_code != EXIT_OK
        assert not commands._ACTIVE_OUTPUTS
        if failure in ("validation", "unlink"):
            assert before == _artifact_bytes(out)
        else:
            assert not (out / "done.json").exists()
    retry = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
    assert retry.exit_code == EXIT_OK, retry.output
    assert not commands._ACTIVE_OUTPUTS


def test_resume_nested_alias_rejected_and_distinct_output_works(tmp_path, monkeypatch):
    import superclaude.cli.swarm.dispatch as dispatch

    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    other = tmp_path / "other"
    other.mkdir()
    other_out, other_id = _completed_stub_run(other, monkeypatch)
    _retry_one(out)
    real_dispatch = dispatch.dispatch_wave1
    seen = []

    def observe(*args, **kwargs):
        before = _artifact_bytes(out)
        alias = str(out / ".." / out.name)
        inner = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", alias])
        assert inner.exit_code != EXIT_OK
        assert before == _artifact_bytes(out)
        distinct = CliRunner().invoke(
            run_cmd, ["--resume", other_id, "--output", str(other_out)]
        )
        assert distinct.exit_code == EXIT_OK, distinct.output
        seen.append(True)
        return real_dispatch(*args, **kwargs)

    monkeypatch.setattr(dispatch, "dispatch_wave1", observe)
    result = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
    assert result.exit_code == EXIT_OK, result.output
    assert seen == [True]


@pytest.mark.parametrize("enabled", [True, False])
def test_resume_constructor_failure_preserves_prior_attempt(
    tmp_path, monkeypatch, enabled
):
    import superclaude.cli.swarm.commands as commands
    from superclaude.cli.swarm.transports.stub import StubTransport

    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    for meta in sorted(out.glob("*.meta.json"))[:2]:
        data = json.loads(meta.read_text())
        data["status"] = "timeout"
        meta.write_text(json.dumps(data))
    _completion_policy(monkeypatch, enabled)
    before = _artifact_bytes(out)
    constructed = []

    def factory(*args, **kwargs):
        def constructor(index):
            constructed.append(index)
            if index == 1:
                raise RuntimeError("injected delayed transport constructor failure")
            return StubTransport()

        return constructor

    with monkeypatch.context() as patch:
        patch.setattr(commands, "_resolve_run_transport_factory", factory)
        result = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
        assert result.exit_code != EXIT_OK
        assert constructed == [0, 1]
        assert _artifact_bytes(out) == before
        assert not commands._ACTIVE_OUTPUTS
    retry = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
    assert retry.exit_code == EXIT_OK, retry.output


@pytest.mark.parametrize("enabled", [True, False])
@pytest.mark.parametrize("remaining", [True, False])
@pytest.mark.parametrize(
    "damage", ["missing", "malformed", "job", "inventory", "unsafe", "relens", "cli"]
)
def test_resume_rejection_preserves_completed_artifacts(
    tmp_path, monkeypatch, enabled, remaining, damage
):
    import superclaude.cli.swarm.commands as commands
    import superclaude.cli.swarm.dispatch as dispatch
    import superclaude.cli.swarm.reduce as reducer

    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    if remaining:
        _retry_one(out)
    _completion_policy(monkeypatch, enabled)
    manifest = out / "manifest.json"
    args = ["--resume", job_id, "--output", str(out)]
    if damage == "missing":
        manifest.unlink()
    elif damage == "malformed":
        manifest.write_text("not JSON")
    elif damage == "job":
        args[1] = "wrong-job"
    elif damage == "inventory":
        # Slot zero may be retryable; duplicate an actually succeeded slot.
        _write_succeeded_sidecar(out, slot_index=1, model_slug="duplicate-slot")
    elif damage == "unsafe":
        data = json.loads(manifest.read_text())
        data["output_filename_template"] = (
            "../outside/{lens}-{index:02d}-{model_slug}.md"
        )
        manifest.write_text(json.dumps(data))
    elif damage == "relens":
        data = json.loads(manifest.read_text())
        data["resolved_lens_entry"]["name"] = "not-a-registered-lens"
        manifest.write_text(json.dumps(data))
        args.append("--force-relens")
    else:
        args.append("--tui")
    before = _artifact_bytes(out)
    entered = []

    def forbidden(*args, **kwargs):
        entered.append(True)
        pytest.fail("rejected invocation entered work")

    monkeypatch.setattr(dispatch, "dispatch_wave1", forbidden)
    monkeypatch.setattr(reducer, "reduce_wave3", forbidden)
    result = CliRunner().invoke(run_cmd, args)
    assert result.exit_code != EXIT_OK
    assert entered == []
    assert _artifact_bytes(out) == before
    assert not commands._ACTIVE_OUTPUTS


@pytest.mark.parametrize("enabled", [True, False])
@pytest.mark.parametrize(
    "damage", ["accepted-input", "missing-target", "checksum", "transport"]
)
def test_resume_provider_rejection_preserves_completed_artifacts(
    tmp_path, monkeypatch, enabled, damage
):
    import superclaude.cli.swarm.commands as commands
    import superclaude.cli.swarm.dispatch as dispatch
    import superclaude.cli.swarm.reduce as reducer

    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    _retry_one(out)
    _completion_policy(monkeypatch, enabled)
    manifest = out / "manifest.json"
    data = json.loads(manifest.read_text())
    if damage == "accepted-input":
        data.pop("accepted_workers", None)
        data.pop("accepted_prompt", None)
        manifest.write_text(json.dumps(data))
    elif damage == "missing-target":
        Path(data["target"]["path"]).unlink()
    elif damage == "checksum":
        Path(data["target"]["path"]).write_text("Changed accepted target. " * 12)
    before = _artifact_bytes(out)
    entered = []
    constructed = []

    def factory(*args, **kwargs):
        constructed.append(True)
        raise RuntimeError("injected transport construction failure")

    def forbidden(*args, **kwargs):
        entered.append(True)
        pytest.fail("provider rejection entered work")

    monkeypatch.setattr(commands, "_resolve_run_transport_factory", factory)
    monkeypatch.setattr(dispatch, "dispatch_wave1", forbidden)
    monkeypatch.setattr(reducer, "reduce_wave3", forbidden)
    result = CliRunner().invoke(
        run_cmd,
        ["--resume", job_id, "--output", str(out), "--transport", "openai_compat"],
    )
    assert result.exit_code != EXIT_OK
    assert constructed == ([True] if damage == "transport" else [])
    assert entered == []
    assert _artifact_bytes(out) == before
    assert not commands._ACTIVE_OUTPUTS


@pytest.mark.parametrize("enabled", [True, False])
def test_resume_completed_legacy_provider_needs_no_worker_inputs(
    tmp_path, monkeypatch, enabled
):
    """Provider-only checks do not apply when no provider will execute."""
    import superclaude.cli.swarm.commands as commands
    import superclaude.cli.swarm.dispatch as dispatch

    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    _completion_policy(monkeypatch, enabled)
    manifest = out / "manifest.json"
    data = json.loads(manifest.read_text())
    data.pop("accepted_workers", None)
    data.pop("accepted_prompt", None)
    data["preflight"]["transport_kind"] = "openai_compat"
    manifest.write_text(json.dumps(data))
    Path(data["target"]["path"]).unlink()

    def forbidden(*args, **kwargs):
        pytest.fail("reduction-only resume must not construct or run provider workers")

    monkeypatch.setattr(commands, "_resolve_run_transport_factory", forbidden)
    monkeypatch.setattr(dispatch, "dispatch_wave1", forbidden)
    result = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
    assert result.exit_code == EXIT_OK, result.output
    assert (out / "done.json").exists() is enabled


@pytest.mark.parametrize("enabled", [True, False])
@pytest.mark.parametrize("remaining", [True, False])
@pytest.mark.parametrize(
    "failure", ["unlink", "dispatch", "normalize", "reduce", "contract", "terminal"]
)
def test_resume_old_marker_failure_matrix(
    tmp_path, monkeypatch, enabled, remaining, failure
):
    import superclaude.cli.swarm.commands as commands
    import superclaude.cli.swarm.dispatch as dispatch
    import superclaude.cli.swarm.normalize as normalize
    import superclaude.cli.swarm.reduce as reducer

    if not remaining and failure in ("dispatch", "normalize"):
        pytest.skip("reduction-only resume has no dispatch or normalize stage")
    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    if remaining:
        _retry_one(out)
    _completion_policy(monkeypatch, enabled)
    before = _artifact_bytes(out)
    real_unlink = Path.unlink
    real_state = commands._write_swarm_state
    entries = []
    real_dispatch, real_reduce = dispatch.dispatch_wave1, reducer.reduce_wave3

    def observe_dispatch(*args, **kwargs):
        entries.append("dispatch")
        return real_dispatch(*args, **kwargs)

    def observe_reduce(*args, **kwargs):
        entries.append("reduce")
        return real_reduce(*args, **kwargs)

    def fail(*args, **kwargs):
        assert not (out / "done.json").exists()
        raise OSError("injected accepted-stage failure")

    def unlink(path, *args, **kwargs):
        if path == out / "done.json":
            raise PermissionError("injected retirement failure")
        return real_unlink(path, *args, **kwargs)

    def terminal(root, state, identity):
        if state == "terminal":
            return fail()
        return real_state(root, state, identity)

    with monkeypatch.context() as patch:
        patch.setattr(dispatch, "dispatch_wave1", observe_dispatch)
        patch.setattr(reducer, "reduce_wave3", observe_reduce)
        if failure == "unlink":
            patch.setattr(Path, "unlink", unlink)
        elif failure == "dispatch":
            patch.setattr(dispatch, "dispatch_wave1", fail)
        elif failure == "normalize":
            patch.setattr(normalize, "normalize_wave2", fail)
        elif failure == "reduce":
            patch.setattr(reducer, "reduce_wave3", fail)
        elif failure == "contract":
            patch.setattr(reducer, "emit_contract", fail)
        else:
            patch.setattr(commands, "_write_swarm_state", terminal)
        result = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
        assert result.exit_code != EXIT_OK
        assert not commands._ACTIVE_OUTPUTS
        if failure == "unlink":
            assert entries == []
            assert _artifact_bytes(out) == before
        else:
            assert not (out / "done.json").exists()
    retry = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
    assert retry.exit_code == EXIT_OK, retry.output
    assert (out / "done.json").exists() is enabled


def test_resume_output_claim_is_thread_safe(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    import click

    import superclaude.cli.swarm.commands as commands

    out, _ = _completed_stub_run(tmp_path, monkeypatch)
    before = _artifact_bytes(out)
    owned, release = Event(), Event()

    def owner():
        with commands._claim_active_output(out):
            owned.set()
            assert release.wait(5)

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(owner)
        try:
            assert owned.wait(5)
            with pytest.raises(click.exceptions.Exit):
                with commands._claim_active_output(out / ".." / out.name):
                    pytest.fail("concurrent canonical alias acquired owned root")
            with commands._claim_active_output(tmp_path / "independent"):
                assert _artifact_bytes(out) == before
        finally:
            release.set()
        future.result(timeout=5)
    assert not commands._ACTIVE_OUTPUTS


@pytest.mark.parametrize("enabled", [True, False])
@pytest.mark.parametrize("mode", ["fresh", "redispatch", "reduction"])
def test_resume_overlap_preservation_at_each_boundary(
    tmp_path, monkeypatch, enabled, mode
):
    import superclaude.cli.swarm.commands as commands
    import superclaude.cli.swarm.dispatch as dispatch
    import superclaude.cli.swarm.reduce as reducer

    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
    if mode == "redispatch":
        _retry_one(out)
    _completion_policy(monkeypatch, enabled)
    real = reducer.reduce_wave3 if mode == "reduction" else dispatch.dispatch_wave1
    observed = []

    def observe(*args, **kwargs):
        active_id = json.loads((out / "manifest.json").read_text())["job_id"]
        before = _artifact_bytes(out)
        inner = CliRunner().invoke(
            run_cmd, ["--resume", active_id, "--output", str(out / ".." / out.name)]
        )
        assert inner.exit_code != EXIT_OK
        assert _artifact_bytes(out) == before
        observed.append((out / "done.json").exists())
        return real(*args, **kwargs)

    if mode == "reduction":
        monkeypatch.setattr(reducer, "reduce_wave3", observe)
    else:
        monkeypatch.setattr(dispatch, "dispatch_wave1", observe)
    args = ["--resume", job_id, "--output", str(out)]
    if mode == "fresh":
        args = [
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(tmp_path / "target.md"),
            "--output",
            str(out),
        ]
    result = CliRunner().invoke(run_cmd, args)
    assert result.exit_code == EXIT_OK, result.output
    assert observed == [mode == "fresh"]
    assert not commands._ACTIVE_OUTPUTS
