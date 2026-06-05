"""T06.07 -- FR-025 ``--force-relens`` opt-in re-resolution.

Covers roadmap row R-115 (FR-025): the resume orchestrator's default
path is manifest-driven (INV-001 / INV-016) so live LENSES edits
between the original Wave-0 emit and the resume invocation are
silently ignored. The ``--force-relens`` flag is the opt-in escape
hatch -- it re-resolves the lens against the current registry,
producing a JobSpec whose lens-derived fields (system prompt, user
template, recipe, next-command template) reflect the freshly-edited
lens body. The lens NAME, ``workers.count``, and ``transport.kind``
still come from the manifest so the slot fan-out and transport
binding stay aligned with the original job.

The acceptance contract this module pins (phase-6-tasklist.md §T06.07):

    * ``preflight.resume_mode(manifest_path, force_relens=True)``
      re-resolves the lens via :func:`resolve_lens` and returns a
      JobSpec whose ``prompt.system`` / ``prompt.user_template`` /
      ``normalization.recipe`` / ``recommended_next_command_template``
      carry the live registry values, not the manifest snapshot.
    * ``preflight.resume_mode(manifest_path)`` (default path) stays
      manifest-driven -- the live registry is not consulted (the
      INV-001 contract piggybacks here for the contrast assertion).
    * ``swarm run --resume <id> --force-relens`` wires the flag
      through to the resume orchestrator end-to-end; the synthetic
      manifest fed into ``dispatch_wave1`` carries the freshly
      re-resolved snapshot so dispatched workers see the live body.
    * ``--force-relens`` without ``--resume`` exits :data:`EXIT_USAGE`
      with an actionable diagnostic (the flag has no meaning on the
      preflight-driven input modes).
    * ``--force-relens`` with a lens that is no longer registered
      exits :data:`EXIT_USAGE` (fail-fast on the operator's explicit
      opt-in rather than silently falling through).
    * ``--help`` advertises the new flag.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import preflight
from superclaude.cli.swarm.commands import (
    EXIT_OK,
    EXIT_USAGE,
    run_cmd,
)
from superclaude.cli.swarm.models import (
    JobSpec,
    LensEntry,
    Manifest,
    PreflightSummary,
    ResolvedLensEntry,
    WorkerResult,
    to_json,
)
from superclaude.cli.swarm.preflight import (
    resume_mode,
    set_lens_resolver,
    write_manifest,
)
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE


# ---------------------------------------------------------------------------
# Fixture data -- original (manifest-frozen) vs mutated (live registry)
# ---------------------------------------------------------------------------


LENS_NAME: str = "bare-review"
JOB_ID: str = "job-resume-T06.07"


ORIGINAL_FRAGMENT: str = (
    "ORIGINAL lens prompt fragment. " + CANONICAL_INJECTION_GUARD_SENTENCE
)
ORIGINAL_USER_TEMPLATE: str = "ORIGINAL user template: {{target}}"
ORIGINAL_RECIPE: str = "bare-review-v1"
ORIGINAL_NEXT_CMD: str = "sc:reflect on {job_id}"


MUTATED_FRAGMENT: str = (
    "MUTATED lens prompt fragment. " + CANONICAL_INJECTION_GUARD_SENTENCE
)
MUTATED_USER_TEMPLATE: str = "MUTATED user template: {{target}}"
MUTATED_RECIPE: str = "verdict-only-v1"
MUTATED_NEXT_CMD: str = "sc:troubleshoot {job_id}"


def _snapshot() -> ResolvedLensEntry:
    """The manifest-frozen lens snapshot stamped at the original Wave 0."""
    return ResolvedLensEntry(
        name=LENS_NAME,
        system_prompt_fragment=ORIGINAL_FRAGMENT,
        user_template=ORIGINAL_USER_TEMPLATE,
        recipe_name=ORIGINAL_RECIPE,
        default_workers=3,
        suspect=True,
        tier="T2",
        recommended_next_command_template=ORIGINAL_NEXT_CMD,
        stability="stable",
    )


def _mutated_lens() -> LensEntry:
    """A live-registry LensEntry that overwrites every snapshot field."""
    return LensEntry(
        name=LENS_NAME,
        description="mutated lens registry entry",
        system_prompt_fragment=MUTATED_FRAGMENT,
        user_template=MUTATED_USER_TEMPLATE,
        output_template_path="/abs/path/to/mutated-template.j2",
        recipe_name=MUTATED_RECIPE,
        normalizer_strategy="passthrough",
        default_workers=5,
        default_target_line_cap=6000,
        suspect=False,
        tier="T3",
        recommended_next_command_template=MUTATED_NEXT_CMD,
        acceptance_notes="mutated",
        stability="experimental",
    )


def _manifest(snapshot: ResolvedLensEntry, *, job_id: str = JOB_ID) -> Manifest:
    return Manifest(
        contract_version="1.0",
        job_id=job_id,
        resolved_lens_entry=snapshot,
        preflight=PreflightSummary(
            target_checksum="a" * 64,
            workers_requested=3,
            transport_kind="stub",
        ),
    )


@pytest.fixture
def emitted_manifest_path(tmp_path: Path) -> Path:
    """Emit a manifest carrying the pinned ORIGINAL snapshot."""
    path = write_manifest(_manifest(_snapshot()), tmp_path)
    return Path(path)


@pytest.fixture
def mutated_registry():
    """Install the mutated lens resolver and record any consult."""
    calls: list[str] = []

    def resolver(name: str) -> LensEntry:
        calls.append(name)
        return _mutated_lens()

    previous = set_lens_resolver(resolver)
    try:
        yield calls
    finally:
        set_lens_resolver(previous)


@pytest.fixture
def empty_registry():
    """Install a resolver that rejects every lookup with KeyError."""
    calls: list[str] = []

    def resolver(name: str) -> LensEntry:
        calls.append(name)
        raise KeyError(name)

    previous = set_lens_resolver(resolver)
    try:
        yield calls
    finally:
        set_lens_resolver(previous)


def _write_manifest_on_disk(
    output_dir: Path,
    *,
    workers_requested: int = 3,
    job_id: str = JOB_ID,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = Manifest(
        contract_version="1.0",
        job_id=job_id,
        resolved_lens_entry=_snapshot(),
        preflight=PreflightSummary(
            target_checksum="a" * 64,
            workers_requested=workers_requested,
            transport_kind="stub",
        ),
    )
    path = output_dir / "manifest.json"
    path.write_text(to_json(manifest), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Unit-level: resume_mode(force_relens=...) contract on preflight
# ---------------------------------------------------------------------------


def test_resume_mode_default_keeps_manifest_lens(
    emitted_manifest_path: Path, mutated_registry: list[str]
) -> None:
    """Default ``force_relens=False`` -- snapshot wins, registry untouched."""
    spec = resume_mode(emitted_manifest_path)

    assert spec.prompt.system == ORIGINAL_FRAGMENT
    assert spec.prompt.user_template == ORIGINAL_USER_TEMPLATE
    assert spec.normalization.recipe == ORIGINAL_RECIPE
    assert spec.recommended_next_command_template == ORIGINAL_NEXT_CMD
    # The contrast assertion: registry mutation does not leak in.
    assert MUTATED_FRAGMENT not in spec.prompt.system
    # The resolver was not called -- INV-001 holds.
    assert mutated_registry == []


def test_resume_mode_force_relens_uses_live_registry(
    emitted_manifest_path: Path, mutated_registry: list[str]
) -> None:
    """``force_relens=True`` -- live registry overwrites the snapshot fields."""
    spec = resume_mode(emitted_manifest_path, force_relens=True)

    # All four lens-derived fields carry the MUTATED values.
    assert spec.prompt.system == MUTATED_FRAGMENT
    assert spec.prompt.user_template == MUTATED_USER_TEMPLATE
    assert spec.normalization.recipe == MUTATED_RECIPE
    assert spec.recommended_next_command_template == MUTATED_NEXT_CMD
    # ORIGINAL values are gone.
    assert ORIGINAL_FRAGMENT not in spec.prompt.system
    assert ORIGINAL_USER_TEMPLATE != spec.prompt.user_template
    # The resolver WAS consulted -- exactly once, for the manifest lens name.
    assert mutated_registry == [LENS_NAME]


def test_resume_mode_force_relens_preserves_manifest_job_id(
    emitted_manifest_path: Path, mutated_registry: list[str]
) -> None:
    """Non-lens manifest fields stay manifest-driven even with --force-relens.

    Re-resolving the lens body must not move job_id / workers / transport;
    the slot fan-out and dispatch binding remain aligned with the original
    job acceptance.
    """
    spec = resume_mode(emitted_manifest_path, force_relens=True)

    assert spec.job_id == JOB_ID
    assert spec.workers.count == 3
    assert spec.transport.kind == "stub"
    assert spec.lens == LENS_NAME


def test_resume_mode_force_relens_returns_jobspec(
    emitted_manifest_path: Path, mutated_registry: list[str]
) -> None:
    """Type contract: ``force_relens=True`` still returns a :class:`JobSpec`."""
    spec = resume_mode(emitted_manifest_path, force_relens=True)
    assert isinstance(spec, JobSpec)


def test_resume_mode_force_relens_raises_keyerror_when_lens_unregistered(
    emitted_manifest_path: Path, empty_registry: list[str]
) -> None:
    """A lens removed from the registry surfaces as ``KeyError``.

    Operators who explicitly opt into ``--force-relens`` get a hard
    failure rather than a silent fall-through to the manifest snapshot;
    the CLI wrapper turns this into :data:`EXIT_USAGE`.
    """
    with pytest.raises(KeyError):
        resume_mode(emitted_manifest_path, force_relens=True)
    # The resolver was consulted once with the manifest lens name.
    assert empty_registry == [LENS_NAME]


def test_resume_mode_default_does_not_raise_when_lens_unregistered(
    emitted_manifest_path: Path, empty_registry: list[str]
) -> None:
    """Default path tolerates an empty registry -- snapshot is the source."""
    # The contrast to the prior test: with force_relens=False (the default),
    # the registry is not consulted at all, so an unknown lens does not
    # break the resume call.
    spec = resume_mode(emitted_manifest_path)
    assert spec.prompt.system == ORIGINAL_FRAGMENT
    assert empty_registry == []


# ---------------------------------------------------------------------------
# CLI surface: --force-relens advertised + usage gating
# ---------------------------------------------------------------------------


def test_force_relens_advertised_in_help() -> None:
    """``--help`` lists ``--force-relens`` and links it to ``--resume``."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--help"])

    assert result.exit_code == 0
    assert "--force-relens" in result.output
    # The help text mentions the resume gating so operators understand
    # the flag is not usable outside the resume path.
    assert "--resume" in result.output


def test_force_relens_without_resume_exits_usage(tmp_path: Path) -> None:
    """``--force-relens`` requires ``--resume``; otherwise EXIT_USAGE."""
    spec_path = tmp_path / "spec.json"
    spec_path.write_text("{}", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [str(spec_path), "--force-relens"],
    )

    assert result.exit_code == EXIT_USAGE, (
        f"expected EXIT_USAGE; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    # Diagnostic surface names the missing prerequisite.
    combined = (result.stderr or "") + (result.stdout or "")
    assert "--force-relens" in combined
    assert "--resume" in combined


def test_force_relens_unknown_lens_exits_usage(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    empty_registry: list[str],
) -> None:
    """Live registry rejects the manifest lens -> EXIT_USAGE on the CLI path.

    The flag is the operator's explicit opt-in. When the lens no longer
    exists in the live registry, the orchestrator surfaces this as a
    usage error rather than silently falling through to the manifest
    snapshot (which would defeat the purpose of the override).
    """
    out_dir = tmp_path / "out"
    _write_manifest_on_disk(out_dir)

    # Stub dispatch / normalize so the orchestrator can't accidentally
    # reach them on a regression path.
    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.normalize as normalize_mod

    dispatch_calls: list[Any] = []
    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        lambda *a, **k: dispatch_calls.append((a, k)) or [],
    )
    monkeypatch.setattr(
        normalize_mod,
        "normalize_wave2",
        lambda workers, recipe_name, **kw: list(workers),
    )

    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        ["--resume", JOB_ID, "--output", str(out_dir), "--force-relens"],
    )

    assert result.exit_code == EXIT_USAGE, (
        f"expected EXIT_USAGE; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    # Diagnostic names the lens that could not be resolved.
    combined = (result.stderr or "") + (result.stdout or "")
    assert LENS_NAME in combined
    # No worker fan-out happened on the failure path.
    assert dispatch_calls == []


# ---------------------------------------------------------------------------
# End-to-end: ``swarm run --resume --force-relens`` re-resolves the lens
# ---------------------------------------------------------------------------


def test_cli_resume_force_relens_uses_live_lens(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutated_registry: list[str],
) -> None:
    """``--resume ... --force-relens`` carries the live snapshot into dispatch.

    The synthetic manifest the resume orchestrator passes to
    :func:`dispatch_wave1` must carry the freshly-resolved
    :class:`ResolvedLensEntry` (MUTATED body), not the persisted
    manifest snapshot (ORIGINAL body). This is the structural anchor
    of the FR-025 contract: the redispatched workers see the live
    lens body.
    """
    out_dir = tmp_path / "out"
    _write_manifest_on_disk(out_dir, workers_requested=2)
    # No sidecars on disk -- every slot redispatches.

    captured: dict[str, Any] = {}

    def _fake_dispatch(
        preflight_result: Any, transport: Any = None, **kwargs: Any
    ) -> list[WorkerResult]:
        snap = preflight_result.manifest.resolved_lens_entry
        captured["system_prompt_fragment"] = snap.system_prompt_fragment
        captured["user_template"] = snap.user_template
        captured["recipe_name"] = snap.recipe_name
        captured["next_cmd"] = snap.recommended_next_command_template
        captured["lens_name"] = snap.name
        captured["workers_requested"] = (
            preflight_result.manifest.preflight.workers_requested
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
            "--force-relens",
        ],
    )

    assert result.exit_code == EXIT_OK, (
        f"resume --force-relens should exit 0; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    # Lens-derived fields on the dispatch snapshot reflect the LIVE entry.
    assert captured["system_prompt_fragment"] == MUTATED_FRAGMENT
    assert captured["user_template"] == MUTATED_USER_TEMPLATE
    assert captured["recipe_name"] == MUTATED_RECIPE
    assert captured["next_cmd"] == MUTATED_NEXT_CMD
    # Lens NAME and workers count still come from the manifest.
    assert captured["lens_name"] == LENS_NAME
    assert captured["workers_requested"] == 2
    # The live resolver was consulted (force-relens path).
    assert LENS_NAME in mutated_registry


def test_cli_resume_without_force_relens_keeps_manifest_lens(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutated_registry: list[str],
) -> None:
    """Contrast: same fixture without ``--force-relens`` -> snapshot wins.

    The companion to the prior test. With the same MUTATED registry in
    place but no ``--force-relens`` flag, the dispatch snapshot must
    carry the ORIGINAL manifest values. This is the INV-001 / INV-016
    default behaviour, verified again here from the CLI surface so a
    future regression that flips the default cannot pass silently.
    """
    out_dir = tmp_path / "out"
    _write_manifest_on_disk(out_dir, workers_requested=2)

    captured: dict[str, Any] = {}

    def _fake_dispatch(
        preflight_result: Any, transport: Any = None, **kwargs: Any
    ) -> list[WorkerResult]:
        snap = preflight_result.manifest.resolved_lens_entry
        captured["system_prompt_fragment"] = snap.system_prompt_fragment
        captured["user_template"] = snap.user_template
        captured["recipe_name"] = snap.recipe_name
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
        ["--resume", JOB_ID, "--output", str(out_dir)],
    )

    assert result.exit_code == EXIT_OK, result.stderr
    # Dispatch sees the ORIGINAL (manifest) snapshot, not the MUTATED entry.
    assert captured["system_prompt_fragment"] == ORIGINAL_FRAGMENT
    assert captured["user_template"] == ORIGINAL_USER_TEMPLATE
    assert captured["recipe_name"] == ORIGINAL_RECIPE
    # The live registry was NOT consulted -- INV-001 default holds.
    assert mutated_registry == []


def test_cli_resume_force_relens_with_all_workers_succeeded_still_resolves(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutated_registry: list[str],
) -> None:
    """Even with no redispatch, ``--force-relens`` re-resolves the lens.

    The lens snapshot governs the rehydrated :class:`JobSpec` carried
    into reduce -- specifically the ``normalization.recipe`` chosen
    for any Wave 2 work and the ``amalgamation_mode`` defaulting. We
    want the operator's explicit override to flow through even on the
    happy path where every slot already succeeded.
    """
    out_dir = tmp_path / "out"
    _write_manifest_on_disk(out_dir, workers_requested=3)

    # Stage three succeeded sidecars so the redispatch set is empty.
    for index in range(3):
        stem = f"{LENS_NAME}-{index:02d}-stub-model"
        body = f"slot-{index} body\n"
        (out_dir / f"{stem}.final.md").write_text(body, encoding="utf-8")
        (out_dir / f"{stem}.meta.json").write_text(
            json.dumps(
                {
                    "recipe": ORIGINAL_RECIPE,
                    "schema_version": "1.0",
                    "salvaged": False,
                    "status": "success",
                    "bytes": len(body.encode("utf-8")),
                }
            ),
            encoding="utf-8",
        )

    # Dispatch should not be called on this path -- track it just in case.
    dispatch_calls: list[Any] = []

    def _fake_dispatch(*args: Any, **kwargs: Any) -> list[WorkerResult]:
        dispatch_calls.append((args, kwargs))
        return []

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
            "--force-relens",
        ],
    )

    assert result.exit_code == EXIT_OK, result.stderr
    # No dispatch (nothing to redispatch) -- success line should reflect that.
    assert dispatch_calls == []
    assert "skipped=3" in result.stdout
    assert "redispatched=0" in result.stdout
    # Even with no redispatch, the resolver was consulted because the
    # operator explicitly asked for re-resolution -- fail-fast on a
    # missing lens, never silent.
    assert LENS_NAME in mutated_registry
