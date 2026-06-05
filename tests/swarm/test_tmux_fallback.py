"""T07.17 -- tmux-optional fallback contract.

Covers the acceptance criteria from
``.dev/releases/Current/MultiModelSwarm/tasklist/phase-7-tasklist.md``:

* Detached mode (``swarm run --detached``) requires tmux on PATH.
  When ``shutil.which('tmux')`` returns None (or the operator is
  nested inside an outer tmux session), the detached branch surfaces
  a structured ``EXIT_USAGE`` diagnostic instead of silently falling
  back to inline -- the operator explicitly opted in by passing
  ``--detached`` and the contradiction must be visible.
* Inline mode (the default ``swarm run`` invocation) needs no tmux.
  The inline branch never imports :mod:`superclaude.cli.swarm.tmux`
  and runs to ``EXIT_OK`` even when tmux is genuinely absent from
  the host. This is the AC-008 fallback semantic documented in
  ``docs/swarm/runbook.md`` (T07.17 section).

The tests force the no-tmux branch via ``monkeypatch`` on
``shutil.which`` rather than gating on the host's actual tmux
presence so the suite is deterministic on CI runners that ship tmux
and on minimal containers that don't.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm.commands import EXIT_OK, EXIT_USAGE, run_cmd
from superclaude.cli.swarm import tmux as swarm_tmux


# ---------------------------------------------------------------------------
# Shared minimal spec -- mirrors test_commands_run._minimal_valid_spec but
# kept local so the fallback contract test is self-contained.
# ---------------------------------------------------------------------------


def _runnable_spec(tmp_path: Path) -> dict[str, Any]:
    """Return a JobSpec dict with on-disk target/output paths under ``tmp_path``."""
    from superclaude.cli.swarm.schema import CURRENT_SPEC_VERSION
    from superclaude.cli.swarm.preflight import CANONICAL_INJECTION_GUARD_SENTENCE

    target = tmp_path / "target.py"
    target.write_text(
        "# T07.17 fallback smoke target\n"
        + "def hello() -> str:\n    return 'tmux-optional fallback'\n"
        + "# padding to clear the IMM-4 byte-floor guard\n" * 4,
        encoding="utf-8",
    )
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-tmux-fallback",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "tmux-fallback-test",
            "kind": "claude",
        },
        "lens": "bare-review",
        "custom_prompt_dir": None,
        "workers": {
            "count": 2,
            "models": ["gpt-5-codex", "claude-haiku-4.5"],
            "timeout_sec": 60,
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
        "recommended_next_command_substitutions": {"job_id": "job-tmux-fallback"},
        "runtime": {
            "mode": "inline",
            "log_level": "info",
            "on_completion": {
                "write_done_sentinel": True,
                "print_contract_to_stdout": True,
            },
        },
    }


def _write_spec(tmp_path: Path, spec: dict[str, Any]) -> Path:
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Detection contract -- is_tmux_available is the single gate
# ---------------------------------------------------------------------------


def test_is_tmux_available_false_when_path_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: missing tmux on PATH -> ``is_tmux_available`` returns False.

    This is the detection primitive the detached branch (T07.11) and
    the runbook fallback note both consult. The negative branch must
    be deterministic regardless of host tmux state.
    """
    monkeypatch.setattr(swarm_tmux.shutil, "which", lambda _: None)
    assert swarm_tmux.is_tmux_available() is False


# ---------------------------------------------------------------------------
# Detached path -- explicit opt-in surfaces a structured error
# ---------------------------------------------------------------------------


def test_run_cmd_detached_exits_usage_when_tmux_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: ``swarm run --detached`` without tmux -> EXIT_USAGE + diagnostic.

    The detached branch refuses to fall back to inline because the
    operator passed ``--detached`` explicitly. The diagnostic on
    stderr names tmux so the operator can install it or drop the
    flag.
    """
    spec_path = _write_spec(tmp_path, _runnable_spec(tmp_path))
    monkeypatch.setattr(swarm_tmux.shutil, "which", lambda _: None)

    runner = CliRunner()
    result = runner.invoke(run_cmd, [str(spec_path), "--detached"])

    assert result.exit_code == EXIT_USAGE, (
        f"--detached without tmux should exit {EXIT_USAGE}; "
        f"got {result.exit_code}\nstderr:\n{result.stderr}"
    )
    assert "tmux" in result.stderr.lower(), (
        f"missing tmux diagnostic on stderr:\n{result.stderr}"
    )
    assert "--detached" in result.stderr or "detached" in result.stderr.lower(), (
        f"diagnostic should name the offending flag:\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# Inline fallback -- the default path runs to EXIT_OK without tmux
# ---------------------------------------------------------------------------


def test_run_cmd_inline_default_succeeds_without_tmux(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC-008: the default (inline) ``swarm run`` needs no tmux.

    Forces the no-tmux branch by stubbing ``shutil.which`` on both
    the swarm tmux module and globally, then runs the inline
    pipeline against a stubbed ``dispatch_wave1``. EXIT_OK confirms
    that the inline path never consults tmux. ``test_no_tmux_paths_*``
    in ``test_tmux_detached.py`` already proves the helper layer is
    safe; this test proves the CLI command surface is safe too.
    """
    spec_path = _write_spec(tmp_path, _runnable_spec(tmp_path))

    # Force tmux-absent on the swarm tmux module. The inline branch
    # never imports the tmux module at all, but stubbing here is the
    # belt-and-braces guarantee: if someone later threads an
    # unconditional tmux probe through the swarm tmux module, this
    # test will fail loudly.
    monkeypatch.setattr(swarm_tmux.shutil, "which", lambda _: None)

    captured: dict[str, Any] = {}

    def _fake_dispatch(preflight_result: Any, transport: Any = None, **kwargs: Any) -> list[Any]:
        captured["preflight_result"] = preflight_result
        return []

    import superclaude.cli.swarm.dispatch as dispatch_mod

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _fake_dispatch)

    runner = CliRunner()
    result = runner.invoke(run_cmd, [str(spec_path)])

    assert result.exit_code == EXIT_OK, (
        f"inline swarm run must succeed without tmux; got "
        f"exit_code={result.exit_code}\nstdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert "preflight_result" in captured, (
        "inline path did not reach dispatch -- the run aborted before "
        "the fallback semantic could be exercised"
    )
    assert "tmux" not in result.stderr.lower(), (
        f"inline run mentioned tmux on stderr (it should never reference "
        f"the detached layer):\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# Documentation anchor -- runbook contains the tmux-optional paragraph
# ---------------------------------------------------------------------------


def test_runbook_documents_tmux_optional_fallback() -> None:
    """AC: ``docs/swarm/runbook.md`` carries the tmux-optional note.

    Validation clause from T07.17 explicitly requires the runbook
    to contain the tmux-optional paragraph so operators reading the
    doc can confirm the fallback semantic before invoking the CLI.
    """
    repo_root = Path(__file__).resolve().parents[2]
    runbook = repo_root / "docs" / "swarm" / "runbook.md"
    assert runbook.exists(), f"missing runbook: {runbook}"
    text = runbook.read_text(encoding="utf-8")

    # Section anchor + the two halves of the contract.
    assert "AC-008" in text, "runbook must cite AC-008 for the fallback semantic"
    assert "tmux-optional" in text.lower() or "tmux optional" in text.lower(), (
        "runbook must include the tmux-optional anchor phrase"
    )
    assert "inline" in text.lower(), "runbook must name the inline default mode"
    assert "--detached" in text, "runbook must name the --detached flag"
