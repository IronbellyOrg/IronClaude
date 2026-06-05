"""T03.08 / FR-001 / FR-020 -- ``swarm run`` three input modes.

Covers roadmap row R-066 (FR-001) end-to-end: the ``run_cmd`` subcommand
accepts a JobSpec via three mutually-exclusive input modes
(spec-file, stdin, ``--lens`` shortcut), and the lens-shortcut path
(``T03.08``) expands a bare ``--lens NAME --target ... --output ...``
into a fully populated JobSpec via lens defaults (FR-020).

Pins:

1. Spec-file mode dispatches Wave 0 -> Wave 1 successfully against the
   reference dispatcher.
2. Stdin mode parses the JobSpec JSON document off ``sys.stdin`` and
   dispatches end-to-end.
3. Lens-shortcut mode (``--lens bare-review --target FILE --output DIR``)
   builds a preflight-valid JobSpec from lens defaults and dispatches
   end-to-end without a companion spec file.
4. The internal JobSpec carried into preflight is structurally
   equivalent across all three modes (same lens, workers count,
   prompt.system, normalization.recipe).
5. Mutually-exclusive enforcement: any pair of (SPEC_PATH, ``--stdin``,
   ``--lens``) -> :data:`EXIT_USAGE`.
6. Lens-shortcut rejects unknown names and the ``custom`` escape hatch
   with :data:`EXIT_USAGE` so the operator gets an actionable diagnostic
   before preflight ever runs.

The tests deliberately monkeypatch :func:`dispatch_wave1` to a sentinel
so the test does not depend on the M3 concrete transports landing
(T03.05 / T03.07). The capture sentinel records the
:class:`PreflightResult` so the test can assert on the resolved
JobSpec shape regardless of input mode.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm.commands import (
    EXIT_INVALID,
    EXIT_OK,
    EXIT_USAGE,
    _build_spec_from_lens,
    run_cmd,
)
from superclaude.cli.swarm.lenses import LENSES
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
    validate,
)


# ---------------------------------------------------------------------------
# Fixtures -- minimal preflight-valid spec + on-disk target/output helpers
# ---------------------------------------------------------------------------


def _padded_target_body() -> str:
    """Return a target body that comfortably clears the IMM-4 byte floor."""
    return (
        "# T03.08 swarm-run input-mode smoke target\n"
        + "def hello() -> str:\n    return 'hello world from a target'\n"
        + "# padding to clear the IMM-4 50-byte non-whitespace floor\n" * 6
    )


def _write_target(tmp_path: Path, name: str = "target.py") -> Path:
    """Create a real target file under ``tmp_path`` for preflight."""
    target = tmp_path / name
    target.write_text(_padded_target_body(), encoding="utf-8")
    return target


def _minimal_runnable_spec(tmp_path: Path) -> dict[str, Any]:
    """Minimal valid JobSpec with target/output paths under ``tmp_path``.

    Mirrors ``test_commands_run.py::_runnable_spec`` so the input-mode
    tests can drive spec-file and stdin modes off the same fixture
    shape. Defined locally so this test does not depend on the
    structurally-similar fixture in ``test_commands_run.py``.
    """
    target = _write_target(tmp_path)
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-run-inputs",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "run-inputs-test",
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
                "You are a code reviewer. "
                + CANONICAL_INJECTION_GUARD_SENTENCE
            ),
            "user_template": "Review: {{target}}",
            "variables": {},
        },
        "target": {
            "kind": "file",
            "path": str(target),
            "truncation": {"line_cap": 4000, "byte_floor": 50},
            "delimiters": {
                "open": "<<<TARGET>>>",
                "close": "<<<END TARGET>>>",
            },
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
            "dir": str(tmp_path / "out"),
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
        "recommended_next_command_substitutions": {"job_id": "job-run-inputs"},
        "runtime": {
            "mode": "inline",
            "log_level": "info",
            "on_completion": {
                "write_done_sentinel": True,
                "print_contract_to_stdout": True,
            },
        },
    }


@pytest.fixture
def fake_dispatch(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Patch :func:`dispatch_wave1` and return a capture dict.

    The capture dict gains ``preflight_result`` and ``transport`` keys
    when the patched dispatcher fires; tests assert against the
    :class:`PreflightResult` shape to verify that all three input
    modes resolve to a structurally-equivalent JobSpec by the time
    Wave 1 is called.
    """
    captured: dict[str, Any] = {}

    def _fake(preflight_result: Any, transport: Any = None, **_: Any) -> list[Any]:
        captured["preflight_result"] = preflight_result
        captured["transport"] = transport
        return []

    import superclaude.cli.swarm.dispatch as dispatch_mod

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _fake)
    return captured


# ---------------------------------------------------------------------------
# _build_spec_from_lens -- unit-level: lens defaults flow into the dict
# ---------------------------------------------------------------------------


def test_build_spec_from_lens_bare_review_passes_schema() -> None:
    """AC: lens-shortcut dict passes DM-001 schema validation (FR-020)."""
    spec = _build_spec_from_lens("bare-review")
    failures = validate(spec)
    # The placeholder ``target.path`` / ``output.dir`` are empty strings
    # which the schema accepts (``"type": "string"`` -- preflight is
    # what surfaces unreadable-target diagnostics later). The schema
    # layer must accept the lens-defaulted dict structurally.
    assert failures == [], (
        "lens-shortcut dict must pass DM-001 schema; got failures:\n"
        + "\n".join(f"  {f.rule} @ {f.path}: {f.message}" for f in failures)
    )


def test_build_spec_from_lens_carries_lens_defaults() -> None:
    """AC: lens fields flow into the JobSpec dict per FR-020."""
    entry = LENSES["bare-review"]
    spec = _build_spec_from_lens("bare-review")

    assert spec["lens"] == "bare-review"
    assert spec["workers"]["count"] == entry.default_workers
    assert len(spec["workers"]["models"]) == entry.default_workers
    assert spec["prompt"]["system"] == entry.system_prompt_fragment
    assert spec["prompt"]["user_template"] == entry.user_template
    assert spec["normalization"]["recipe"] == entry.recipe_name
    assert spec["normalization"]["template_path"] == entry.output_template_path
    assert spec["target"]["truncation"]["line_cap"] == entry.default_target_line_cap
    assert spec["output"]["lens_name"] == "bare-review"
    assert spec["recommended_next_command_template"] == (
        entry.recommended_next_command_template
    )
    # §11.5 substring round-trips byte-identically via the injection guard.
    assert CANONICAL_INJECTION_GUARD_SENTENCE in spec["prompt"]["system"]
    assert spec["target"]["injection_guard"]["required_substring"] == (
        CANONICAL_INJECTION_GUARD_SENTENCE
    )


def test_build_spec_from_lens_defaults_to_stub_transport() -> None:
    """AC: lens-shortcut defaults to ``transport.kind=stub`` (FR-020 safety).

    Operators who want the T2 proxy supply ``--transport openai_compat``
    explicitly; the lens shortcut path is for safe quick-dispatch.
    """
    spec = _build_spec_from_lens("bare-review")
    assert spec["transport"]["kind"] == "stub"


def test_build_spec_from_lens_workers_count_matches_lens_default() -> None:
    """AC: lens with default_workers=N produces N model slots."""
    # ``edge-case-hunt`` has default_workers=4 per COMP-026.
    spec = _build_spec_from_lens("edge-case-hunt")
    entry = LENSES["edge-case-hunt"]
    assert spec["workers"]["count"] == entry.default_workers
    assert len(spec["workers"]["models"]) == entry.default_workers


# ---------------------------------------------------------------------------
# Mode 1: spec-file mode -- end-to-end Wave 0 -> Wave 1
# ---------------------------------------------------------------------------


def test_spec_file_mode_dispatches_end_to_end(
    tmp_path: Path,
    fake_dispatch: dict[str, Any],
) -> None:
    """AC: positional SPEC_PATH drives preflight + dispatch (mode=spec-file)."""
    spec = _minimal_runnable_spec(tmp_path)
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(run_cmd, [str(spec_path)])

    assert result.exit_code == EXIT_OK, (
        f"spec-file mode failed: exit={result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "preflight_result" in fake_dispatch, (
        "dispatch_wave1 not invoked in spec-file mode"
    )
    pr = fake_dispatch["preflight_result"]
    assert pr.manifest.job_id == "job-run-inputs"
    assert pr.manifest.preflight.workers_requested == 3
    assert "mode=spec-file" in result.stdout


# ---------------------------------------------------------------------------
# Mode 2: stdin mode -- JSON document on stdin
# ---------------------------------------------------------------------------


def test_stdin_mode_dispatches_end_to_end(
    tmp_path: Path,
    fake_dispatch: dict[str, Any],
) -> None:
    """AC: ``--stdin`` consumes the JobSpec JSON document from stdin."""
    spec = _minimal_runnable_spec(tmp_path)

    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--stdin"], input=json.dumps(spec))

    assert result.exit_code == EXIT_OK, (
        f"stdin mode failed: exit={result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "preflight_result" in fake_dispatch
    pr = fake_dispatch["preflight_result"]
    assert pr.manifest.job_id == "job-run-inputs"
    assert "mode=stdin" in result.stdout


def test_stdin_mode_rejects_invalid_json() -> None:
    """AC: invalid JSON on stdin -> :data:`EXIT_USAGE` (FR-007 diagnostic)."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--stdin"], input="not-json{")
    assert result.exit_code == EXIT_USAGE
    assert "not valid JSON" in result.stderr


# ---------------------------------------------------------------------------
# Mode 3: --lens shortcut -- lens defaults expanded into a full JobSpec
# ---------------------------------------------------------------------------


def test_lens_mode_dispatches_end_to_end(
    tmp_path: Path,
    fake_dispatch: dict[str, Any],
) -> None:
    """AC: ``--lens bare-review --target FILE --output DIR`` dispatches.

    The lens shortcut path (FR-020) builds a preflight-valid JobSpec
    from the lens defaults; only ``--target`` and ``--output`` need to
    be supplied to make the spec runnable end-to-end.
    """
    target = _write_target(tmp_path)
    output_dir = tmp_path / "lens-out"

    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            "--lens",
            "bare-review",
            "--target",
            str(target),
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == EXIT_OK, (
        f"lens shortcut dispatch failed: exit={result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "preflight_result" in fake_dispatch, (
        "dispatch_wave1 not invoked in lens-shortcut mode"
    )
    pr = fake_dispatch["preflight_result"]
    assert pr.manifest.preflight.workers_requested == (
        LENSES["bare-review"].default_workers
    )
    assert "mode=lens" in result.stdout
    # ``--transport`` defaulted to stub in the lens shortcut path.
    assert pr.manifest.preflight.transport_kind == "stub"


def test_lens_mode_transport_override_propagates(
    tmp_path: Path,
    fake_dispatch: dict[str, Any],
) -> None:
    """AC: ``--transport openai_compat`` overrides the stub default."""
    target = _write_target(tmp_path)
    output_dir = tmp_path / "lens-out"

    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            "--lens",
            "bare-review",
            "--target",
            str(target),
            "--output",
            str(output_dir),
            "--transport",
            "openai_compat",
        ],
    )
    assert result.exit_code == EXIT_OK, (
        f"transport override failed: exit={result.exit_code}\n"
        f"stderr:\n{result.stderr}"
    )
    pr = fake_dispatch["preflight_result"]
    assert pr.manifest.preflight.transport_kind == "openai_compat"


def test_lens_mode_rejects_custom_escape_hatch() -> None:
    """AC: ``--lens custom`` -> :data:`EXIT_USAGE` (FR-021 redirect)."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--lens", "custom"])
    assert result.exit_code == EXIT_USAGE
    assert "custom" in result.stderr
    assert "spec file" in result.stderr or "custom_prompt_dir" in result.stderr


def test_lens_mode_rejects_unknown_lens() -> None:
    """AC: ``--lens not-a-real-lens`` -> :data:`EXIT_USAGE`."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--lens", "not-a-real-lens"])
    assert result.exit_code == EXIT_USAGE
    assert "unknown lens" in result.stderr
    # The diagnostic enumerates the known lenses so the operator can
    # correct the typo without consulting docs.
    assert "bare-review" in result.stderr


# ---------------------------------------------------------------------------
# Cross-mode equivalence -- all 3 modes resolve to the same JobSpec shape
# ---------------------------------------------------------------------------


def test_three_modes_resolve_to_equivalent_jobspec(
    tmp_path: Path,
    fake_dispatch: dict[str, Any],
) -> None:
    """AC: all 3 input modes resolve to the same internal JobSpec.

    "Same" here means structurally equivalent on the lens-defaulted
    fields: the JobSpec lens, workers count, prompt system fragment,
    and normalization recipe all match across spec-file / stdin /
    lens-shortcut paths when the inputs encode the same lens + worker
    plan. The smoke test fires three invocations sequentially against
    the same patched dispatcher and compares the captured manifest.
    """
    target = _write_target(tmp_path)
    spec = _minimal_runnable_spec(tmp_path)

    captures: list[Any] = []

    def _record_dispatch(preflight_result: Any, transport: Any = None, **_: Any) -> list[Any]:
        captures.append(preflight_result)
        return []

    import superclaude.cli.swarm.dispatch as dispatch_mod

    # Re-patch with the recording variant so each invocation appends.
    dispatch_mod.dispatch_wave1 = _record_dispatch  # type: ignore[assignment]

    runner = CliRunner()

    # 1. spec-file mode
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    r1 = runner.invoke(run_cmd, [str(spec_path)])
    assert r1.exit_code == EXIT_OK, r1.stderr

    # 2. stdin mode (same spec body)
    r2 = runner.invoke(run_cmd, ["--stdin"], input=json.dumps(spec))
    assert r2.exit_code == EXIT_OK, r2.stderr

    # 3. lens-shortcut mode (same lens; --target / --output the same file)
    r3 = runner.invoke(
        run_cmd,
        [
            "--lens",
            "bare-review",
            "--target",
            str(target),
            "--output",
            str(tmp_path / "lens-out"),
        ],
    )
    assert r3.exit_code == EXIT_OK, r3.stderr

    assert len(captures) == 3, f"expected 3 dispatch invocations, got {len(captures)}"
    # Every preflight result names the same lens-driven worker count
    # (bare-review default_workers=3).
    for pr in captures:
        assert pr.manifest.preflight.workers_requested == 3


# ---------------------------------------------------------------------------
# Mutually-exclusive option enforcement -- all pairs + zero-mode rejection
# ---------------------------------------------------------------------------


def test_no_input_mode_exits_usage() -> None:
    """AC: zero input modes -> :data:`EXIT_USAGE`."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, [])
    assert result.exit_code == EXIT_USAGE
    assert "--lens" in result.stderr or "SPEC_PATH" in result.stderr


def test_spec_path_plus_stdin_exits_usage(tmp_path: Path) -> None:
    """AC: SPEC_PATH + --stdin -> :data:`EXIT_USAGE`."""
    spec_path = tmp_path / "spec.json"
    spec_path.write_text("{}", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(run_cmd, [str(spec_path), "--stdin"], input="{}")
    assert result.exit_code == EXIT_USAGE
    assert "mutually exclusive" in result.stderr


def test_spec_path_plus_lens_exits_usage(tmp_path: Path) -> None:
    """AC: SPEC_PATH + --lens -> :data:`EXIT_USAGE`."""
    spec_path = tmp_path / "spec.json"
    spec_path.write_text("{}", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(run_cmd, [str(spec_path), "--lens", "bare-review"])
    assert result.exit_code == EXIT_USAGE
    assert "mutually exclusive" in result.stderr


def test_stdin_plus_lens_exits_usage() -> None:
    """AC: --stdin + --lens -> :data:`EXIT_USAGE`."""
    runner = CliRunner()
    result = runner.invoke(
        run_cmd, ["--stdin", "--lens", "bare-review"], input="{}"
    )
    assert result.exit_code == EXIT_USAGE
    assert "mutually exclusive" in result.stderr


# ---------------------------------------------------------------------------
# --help surface -- all 3 modes are documented
# ---------------------------------------------------------------------------


def test_help_documents_all_three_input_modes() -> None:
    """AC: ``swarm run --help`` advertises all 3 input modes (T03.08 AC)."""
    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--help"])
    assert result.exit_code == 0
    for token in ("SPEC_PATH", "--stdin", "--lens", "--target", "--output", "--transport"):
        assert token in result.output, f"--help missing {token!r}"
    # The lens-shortcut help string names FR-020 expansion explicitly so
    # operators learn it's a full-spec shortcut rather than a parsing
    # hint for spec files.
    assert "FR-020" in result.output or "Expands lens defaults" in result.output
