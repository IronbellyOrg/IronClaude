"""T03.01 / FR-001 -- ``superclaude swarm run`` subcommand wiring.

Covers roadmap row R-060 (COMP-002). Pins the operator-visible
contract of ``cli/swarm/commands.py::run_cmd``:

1. Registered with ``swarm_group`` under the ``run`` name (replaces
   the T01.08 placeholder).
2. ``--help`` advertises the three input modes (spec-file argument,
   ``--stdin``, ``--lens``) plus the ``--target`` / ``--output`` /
   ``--transport`` overrides and the ``--auto-inject-guard`` flag.
3. Mutually-exclusive enforcement: more than one of (SPEC_PATH /
   ``--stdin`` / ``--lens``) -> :data:`EXIT_USAGE`.
4. Zero input modes -> :data:`EXIT_USAGE`.
5. Spec-file mode: a clean minimal JobSpec drives Wave 0 (preflight)
   succeed and Wave 1 (dispatch) is invoked end-to-end against the
   T03.01 reference dispatcher; the success line on stdout names the
   mode and worker count.
6. Preflight failure: structured rule diagnostics on stderr, exit
   :data:`EXIT_INVALID`. The INV-007 env-missing contract path is
   surfaced on stderr when written.
7. Dispatch wiring: :func:`dispatch_wave1` is invoked with the
   :class:`PreflightResult` returned from Wave 0 -- verified via a
   monkeypatched sentinel so the test does not depend on the M3
   concrete transports landing.

The fixture spec is the same minimal valid spec used by
``test_validate_cmd.py``; duplicated here so the CLI test does not
depend on schema-test internals.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import (
    EXIT_INVALID,
    EXIT_OK,
    EXIT_USAGE,
    run_cmd,
)
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _minimal_valid_spec() -> dict[str, Any]:
    """Return a freshly-allocated minimal valid JobSpec dict.

    Mirrors ``tests/swarm/test_validate_cmd.py::_minimal_valid_spec``
    so the CLI test is decoupled from the schema-test fixtures.
    """
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-run-cmd",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "run-cmd-test",
            "kind": "claude",
        },
        "lens": "bare-review",
        "custom_prompt_dir": None,
        "workers": {
            "count": 3,
            "models": ["gpt-5-codex", "claude-haiku-4.5", "gemini-1.5-pro"],
            "timeout_sec": 180,
            "temperature": 0.2,
            "retry": {
                "on_5xx": True,
                "on_5xx_backoff_sec": 2,
                "on_4xx": False,
                "on_timeout": False,
            },
        },
        "transport": {
            "kind": "openai_compat",
            "base_url_env": "T2ProxyUrl",
            "api_key_env": "T2ProxyKey",
        },
        "prompt": {
            "system": (
                "You are a code reviewer. " + CANONICAL_INJECTION_GUARD_SENTENCE
            ),
            "user_template": "Review: {{target}}",
            "variables": {},
        },
        "target": {
            "kind": "file",
            "path": "/abs/path/to/target.py",
            "truncation": {"line_cap": 4000, "byte_floor": 50},
            "delimiters": {"open": "<<<TARGET>>>", "close": "<<<END TARGET>>>"},
            "injection_guard": {
                "enabled": True,
                "required_substring": CANONICAL_INJECTION_GUARD_SENTENCE,
            },
        },
        "normalization": {
            "recipe": "bare-review-v1",
            "template_path": "/abs/path/to/template.j2",
            "schema_version": "1.0",
            "recipe_args": {},
            "on_parse_error": {"salvage": True, "retain_raw": True},
        },
        "output": {
            "dir": "/abs/path/to/output",
            "filename_template": "{lens}-{index:02d}-{model_slug}.md",
            "lens_name": "bare-review",
            "atomic_write": True,
            "emit_meta_sidecar": True,
        },
        "amalgamation_mode": "normalize+merge",
        "status_policy": {
            "floor": 2,
            "success_first": True,
            "partial_threshold": 2,
        },
        "recommended_next_command_template": "sc:reflect on {job_id}",
        "recommended_next_command_substitutions": {"job_id": "job-run-cmd"},
        "runtime": {
            "mode": "inline",
            "log_level": "info",
            "on_completion": {
                "write_done_sentinel": True,
                "print_contract_to_stdout": True,
            },
        },
    }


def _write_spec(tmp_path: Path, spec: Any, name: str = "spec.json") -> Path:
    """Serialize ``spec`` to ``tmp_path/<name>`` and return the path."""
    path = tmp_path / name
    path.write_text(json.dumps(spec), encoding="utf-8")
    return path


def _runnable_spec(tmp_path: Path) -> dict[str, Any]:
    """Minimal spec with target/output paths resolvable under ``tmp_path``.

    Preflight loads ``target.path`` via the default file reader, so the
    spec-file integration test needs a real on-disk target. The byte
    floor (default 50) requires a non-trivial payload; the body is a
    fixed string so the test is deterministic.
    """
    spec = _minimal_valid_spec()
    target = tmp_path / "target.py"
    target.write_text(
        "# T03.01 swarm-run smoke target\n"
        + "def hello() -> str:\n    return 'hello world from a target'\n"
        + "# padding to clear the IMM-4 byte-floor guard\n" * 4,
        encoding="utf-8",
    )
    spec["target"]["path"] = str(target)
    spec["output"]["dir"] = str(tmp_path / "out")
    # F-P3-1 -- the run-dispatch wiring path uses the deterministic,
    # network-free ``stub`` transport so the concrete-transport resolver
    # (which replaced the historical ``transport=None`` no-op) constructs
    # without requiring the live T2 proxy env contract. The openai_compat
    # transport surface is covered directly in ``test_openai_compat.py``.
    spec["transport"]["kind"] = "stub"
    return spec


# ---------------------------------------------------------------------------
# Registration -- run_cmd resolves on swarm_group
# ---------------------------------------------------------------------------


def test_run_cmd_registered_on_swarm_group() -> None:
    """AC: ``run_cmd`` is registered under the ``run`` name (T03.01)."""
    assert "run" in swarm_group.commands, (
        "run subcommand missing from swarm_group; "
        f"registered: {sorted(swarm_group.commands)}"
    )
    assert swarm_group.commands["run"] is run_cmd, (
        "swarm run must resolve to commands.run_cmd, not the T01.08 placeholder"
    )


def test_run_cmd_help_lists_all_input_modes() -> None:
    """AC: ``--help`` advertises every input mode + override option."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--help"])
    assert result.exit_code == 0, result.output
    for token in (
        "SPEC_PATH",
        "--stdin",
        "--lens",
        "--target",
        "--output",
        "--transport",
        "--auto-inject-guard",
    ):
        assert token in result.output, f"--help missing {token!r}:\n{result.output}"


def test_run_cmd_help_via_main_swarm_group() -> None:
    """End-to-end: ``superclaude swarm run --help`` exits 0."""
    from superclaude.cli.main import main

    runner = CliRunner()
    result = runner.invoke(main, ["swarm", "run", "--help"])
    assert result.exit_code == 0, result.output
    assert "Run a swarm job" in result.output or "preflight" in result.output


# ---------------------------------------------------------------------------
# Input-mode resolution -- mutually exclusive + zero-mode rejection
# ---------------------------------------------------------------------------


def test_run_cmd_no_input_mode_exits_usage() -> None:
    """AC: zero input modes -> EXIT_USAGE with actionable diagnostic."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, [])
    assert result.exit_code == EXIT_USAGE, (
        f"expected EXIT_USAGE ({EXIT_USAGE}); got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "SPEC_PATH" in result.stderr or "--stdin" in result.stderr


def test_run_cmd_conflicting_modes_exits_usage(tmp_path: Path) -> None:
    """AC: SPEC_PATH + --lens together -> EXIT_USAGE."""
    spec_path = _write_spec(tmp_path, _minimal_valid_spec())
    runner = CliRunner()
    result = runner.invoke(run_cmd, [str(spec_path), "--lens", "bare-review"])
    assert result.exit_code == EXIT_USAGE, (
        f"expected EXIT_USAGE on conflicting modes; got {result.exit_code}\n"
        f"stderr:\n{result.stderr}"
    )
    assert "mutually exclusive" in result.stderr


def test_run_cmd_stdin_plus_lens_exits_usage() -> None:
    """AC: --stdin + --lens together -> EXIT_USAGE."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--stdin", "--lens", "bare-review"], input="{}")
    assert result.exit_code == EXIT_USAGE
    assert "mutually exclusive" in result.stderr


def test_run_cmd_invalid_json_exits_usage(tmp_path: Path) -> None:
    """AC: a non-JSON spec file -> EXIT_USAGE with json error diagnostic."""
    bad = tmp_path / "bad.json"
    bad.write_text("not-json{", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(run_cmd, [str(bad)])
    assert result.exit_code == EXIT_USAGE
    assert "not valid JSON" in result.stderr


def test_run_cmd_stdin_mode_parses_json() -> None:
    """AC: ``--stdin`` reads the JobSpec dict from stdin.

    Even though preflight will reject this fixture (the default
    target.path does not exist), the test only asserts that the
    stdin reader resolved the input mode -- preflight diagnostics
    on stderr prove the dict was parsed.
    """
    runner = CliRunner()
    spec_json = json.dumps(_minimal_valid_spec())
    result = runner.invoke(run_cmd, ["--stdin"], input=spec_json)
    # The fixture target path does not exist on disk, so preflight
    # surfaces RULE_TARGET_UNREADABLE rather than a usage error.
    # Either EXIT_INVALID or EXIT_OK is acceptable depending on the
    # target reader; the assertion below is that stdin was consumed.
    assert result.exit_code in (EXIT_INVALID, EXIT_OK), (
        f"stdin parse failure surfaced before preflight; "
        f"exit_code={result.exit_code}\nstderr:\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# Preflight -> Dispatch end-to-end wiring (T03.01 smoke path)
# ---------------------------------------------------------------------------


def test_run_cmd_spec_file_mode_invokes_preflight_and_dispatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: spec-file mode runs Wave 0 then Wave 1 end-to-end.

    Patches ``dispatch_wave1`` to a sentinel so the test asserts on
    the handshake (the preflight result is forwarded into dispatch)
    without depending on the M3 concrete transports landing
    (T03.05 / T03.07). The success line on stdout names the input
    mode and the worker count.
    """
    spec = _runnable_spec(tmp_path)
    spec_path = _write_spec(tmp_path, spec)

    captured: dict[str, Any] = {}

    def _fake_dispatch(
        preflight_result: Any, transport: Any = None, **kwargs: Any
    ) -> list[Any]:
        captured["preflight_result"] = preflight_result
        captured["transport"] = transport
        return []

    # The run_cmd body does a lazy import; patch the source module so
    # the lazy import inside the function picks up the fake.
    import superclaude.cli.swarm.dispatch as dispatch_mod

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _fake_dispatch)

    runner = CliRunner()
    result = runner.invoke(run_cmd, [str(spec_path)])

    assert result.exit_code == EXIT_OK, (
        f"clean spec should exit {EXIT_OK}; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "preflight_result" in captured, (
        "dispatch_wave1 was not invoked; preflight->dispatch handshake broken"
    )
    # Manifest is the INV-001 source-of-truth and must reach dispatch.
    preflight_result = captured["preflight_result"]
    assert preflight_result.manifest.job_id == "job-run-cmd"
    assert preflight_result.manifest.preflight.workers_requested == 3
    # F-P3-1 -- run_cmd now resolves a CONCRETE transport before dispatch
    # (the historical ``transport=None`` made dispatch a no-op). The
    # fixture uses ``stub`` so the resolved transport is a StubTransport.
    from superclaude.cli.swarm.transports.stub import StubTransport

    assert captured["transport"] is not None, (
        "run_cmd must pass a concrete transport to dispatch_wave1 (F-P3-1); "
        "transport=None is the no-op that dispatched zero workers"
    )
    assert isinstance(captured["transport"], StubTransport)

    # Stdout success line names the input mode and worker count.
    assert "mode=spec-file" in result.stdout
    assert "workers=3" in result.stdout


def test_run_cmd_emits_failed_diagnostics_on_preflight_error(
    tmp_path: Path,
) -> None:
    """AC: preflight failure surfaces structured rule block on stderr."""
    spec = _runnable_spec(tmp_path)
    # Corrupt the spec so preflight rejects it. Drop the §11.5
    # required substring -- a deterministic cross-field rule that
    # fires under :data:`RULE_INJECTION_SUBSTRING`.
    spec["prompt"]["system"] = "You are a reviewer with no guard sentence."
    spec_path = _write_spec(tmp_path, spec)

    runner = CliRunner()
    result = runner.invoke(run_cmd, [str(spec_path)])

    assert result.exit_code == EXIT_INVALID, (
        f"preflight failure should exit {EXIT_INVALID}; "
        f"got {result.exit_code}\nstdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert "preflight FAILED" in result.stderr, (
        f"missing structured failure header; got stderr:\n{result.stderr}"
    )


def test_run_cmd_target_override_propagates_to_preflight(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: ``--target`` override flows into the resolved JobSpec dict."""
    spec = _runnable_spec(tmp_path)
    # Wipe target.path so the override is the only source.
    override_target = tmp_path / "override-target.py"
    override_target.write_text(
        "# T03.01 override target -- padded to clear the byte floor\n"
        + "value = 42\n" * 20,
        encoding="utf-8",
    )
    # Original spec target points elsewhere; override should win.
    spec["target"]["path"] = "/nonexistent/original.py"
    spec_path = _write_spec(tmp_path, spec)

    captured: dict[str, Any] = {}

    def _fake_dispatch(
        preflight_result: Any, transport: Any = None, **kwargs: Any
    ) -> list[Any]:
        captured["ok"] = True
        return []

    import superclaude.cli.swarm.dispatch as dispatch_mod

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _fake_dispatch)

    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [str(spec_path), "--target", str(override_target)],
    )
    assert result.exit_code == EXIT_OK, (
        f"--target override should yield clean preflight; "
        f"got exit_code={result.exit_code}\nstderr:\n{result.stderr}"
    )
    assert captured.get("ok") is True


# ---------------------------------------------------------------------------
# Dispatch stub contract -- T03.01 reference body
# ---------------------------------------------------------------------------


def test_dispatch_wave1_transport_none_returns_empty() -> None:
    """T03.01 contract: ``transport=None`` -> empty result list."""
    from superclaude.cli.swarm.dispatch import dispatch_wave1
    from superclaude.cli.swarm.models import Manifest, PreflightSummary, SwarmState
    from superclaude.cli.swarm.preflight import PreflightResult

    manifest = Manifest(
        contract_version="1.0",
        job_id="job-dispatch-stub",
        preflight=PreflightSummary(
            target_checksum="deadbeef",
            workers_requested=2,
            transport_kind="stub",
        ),
    )
    state = SwarmState(state="preflight_ok", job_id="job-dispatch-stub")
    result = dispatch_wave1(PreflightResult(manifest=manifest, state=state))
    assert result == []


def test_dispatch_wave1_with_transport_calls_send_per_worker() -> None:
    """T03.01 contract: N workers -> N transport.send calls.

    Sequential reference body; T03.02 replaces with ParallelExecutor
    fan-out but keeps the contract: one ``WorkerResult`` per worker,
    in slot-index order.
    """
    from superclaude.cli.swarm.dispatch import dispatch_wave1
    from superclaude.cli.swarm.models import (
        Manifest,
        PreflightSummary,
        SwarmState,
        WorkerResult,
    )
    from superclaude.cli.swarm.preflight import PreflightResult

    manifest = Manifest(
        contract_version="1.0",
        job_id="job-dispatch-stub",
        preflight=PreflightSummary(
            target_checksum="deadbeef",
            workers_requested=3,
            transport_kind="stub",
        ),
    )
    state = SwarmState(state="preflight_ok", job_id="job-dispatch-stub")

    call_count = {"n": 0}

    class _RecordingTransport:
        def send(self, prompt: str, timeout: int) -> WorkerResult:
            call_count["n"] += 1
            return WorkerResult(status="success")

    results = dispatch_wave1(
        PreflightResult(manifest=manifest, state=state),
        transport=_RecordingTransport(),
    )
    assert call_count["n"] == 3
    assert len(results) == 3
    # Worker indices are stamped in slot order.
    assert [r.index for r in results] == [0, 1, 2]


# ---------------------------------------------------------------------------
# F-P3-1 regression -- real stub dispatch is NOT a no-op
# ---------------------------------------------------------------------------


def test_run_cmd_stub_transport_dispatches_workers_not_noop(
    tmp_path: Path,
) -> None:
    """F-P3-1: ``swarm run --transport stub`` dispatches N workers, not zero.

    This is the critical regression: before the fix, ``run_cmd`` recorded
    ``transport.kind`` on the manifest but passed ``transport=None`` to
    :func:`dispatch_wave1`, which short-circuits to an empty list -- so a
    real ``swarm run`` produced ``results=0`` with no worker artifacts or
    dispatch log events. This test runs the REAL dispatch (no monkeypatch)
    against the deterministic stub transport and asserts results == workers
    and that dispatch log events were emitted.
    """
    target = tmp_path / "target.py"
    target.write_text(
        "# F-P3-1 stub-dispatch regression target\n"
        + "def hello() -> str:\n    return 'real stub dispatch, not a no-op'\n"
        + "# padding to clear the IMM-4 non-whitespace byte floor\n" * 6,
        encoding="utf-8",
    )
    output_dir = tmp_path / "out"

    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(target),
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == EXIT_OK, (
        f"stub-transport run must succeed; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    # bare-review default_workers=3 -> results must equal worker count,
    # NOT zero (the F-P3-1 no-op signature was ``results=0``).
    assert "workers=3" in result.stdout, result.stdout
    assert "results=3" in result.stdout, (
        "F-P3-1 regression: stub dispatch produced a non-3 result count; "
        f"the transport may still be a no-op:\n{result.stdout}"
    )

    # Dispatch log events must be present (the logger is wired when an
    # output dir is supplied; dispatch emits wave_transition +
    # worker_start / worker_done events).
    jsonl = output_dir / "execution-log.jsonl"
    assert jsonl.is_file(), f"execution-log.jsonl missing under {output_dir}"
    log_body = jsonl.read_text(encoding="utf-8")
    assert "worker_done" in log_body, (
        "no worker_done events in the execution log -- dispatch did not "
        f"fan out workers:\n{log_body}"
    )
    assert log_body.count("worker_done") == 3, (
        f"expected exactly 3 worker_done events (one per worker slot); log:\n{log_body}"
    )
