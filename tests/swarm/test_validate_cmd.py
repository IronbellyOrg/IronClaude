"""T02.19 / FR-007 -- ``superclaude swarm validate`` subcommand.

Covers roadmap row R-045 (FR-007). Pins the operator-visible contract
of ``cli/swarm/commands.py::validate_cmd``:

1. Registered with ``swarm_group`` under the ``validate`` name.
2. Exits 0 on a clean DM-001 JobSpec and emits a single "OK" line on
   stdout.
3. Exits 1 on a spec that fails one or more schema / cross-field rules,
   and prints a structured per-rule diagnostic block on stderr that
   names the failing rule identifier (the stable ``schema.RULE_*``
   constants, not the human-facing prose).
4. Exits 2 when the spec file is missing or not valid JSON (operator
   usage error, distinguishable from a wrong-spec error by exit code).
5. Accepts the ``--strict`` flag (future-proofing for FR-007).

The fixture spec is the same minimal valid spec used by
``test_schema.py``; keeping it duplicated here (rather than importing)
isolates the CLI surface from any future refactor of the schema test's
helpers.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import (
    EXIT_INVALID,
    EXIT_OK,
    EXIT_USAGE,
    validate_cmd,
)
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
    RULE_CUSTOM_PROMPT_DIR_REQUIRES_CUSTOM_LENS,
    RULE_INJECTION_SUBSTRING,
    RULE_SCHEMA,
    RULE_SPEC_VERSION,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _minimal_valid_spec() -> dict[str, Any]:
    """Return a freshly-allocated minimal valid JobSpec dict.

    Mirrors ``tests/swarm/test_schema.py::_minimal_valid_spec`` so the
    CLI test does not depend on schema-test internals.
    """
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-validate-cmd",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "validate-cmd-test",
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
        "recommended_next_command_substitutions": {"job_id": "job-validate-cmd"},
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


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def test_validate_cmd_registered_on_swarm_group() -> None:
    """AC: ``validate_cmd`` is registered under the ``validate`` name."""
    assert "validate" in swarm_group.commands, (
        "validate subcommand missing from swarm_group; "
        f"registered: {sorted(swarm_group.commands)}"
    )
    assert swarm_group.commands["validate"] is validate_cmd, (
        "swarm validate must resolve to commands.validate_cmd, not a placeholder"
    )


def test_validate_cmd_advertises_strict_flag() -> None:
    """AC: ``--strict`` flag is accepted (FR-007 future-proofing)."""
    runner = CliRunner()
    result = runner.invoke(validate_cmd, ["--help"])
    assert result.exit_code == 0, result.output
    assert "--strict" in result.output, (
        f"--strict flag missing from help output:\n{result.output}"
    )


# ---------------------------------------------------------------------------
# Valid-spec path
# ---------------------------------------------------------------------------


def test_valid_spec_exits_zero(tmp_path: Path) -> None:
    """AC: clean spec -> exit 0 with OK summary on stdout."""
    path = _write_spec(tmp_path, _minimal_valid_spec())
    runner = CliRunner()
    result = runner.invoke(validate_cmd, [str(path)])
    assert result.exit_code == EXIT_OK, (
        f"valid spec should exit {EXIT_OK}; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr (exception): {result.exception!r}"
    )
    assert "OK" in result.stdout, f"OK summary missing from stdout:\n{result.stdout}"


def test_valid_spec_with_strict_flag_exits_zero(tmp_path: Path) -> None:
    """``--strict`` accepted on a valid spec without changing the verdict."""
    path = _write_spec(tmp_path, _minimal_valid_spec())
    runner = CliRunner()
    result = runner.invoke(validate_cmd, ["--strict", str(path)])
    assert result.exit_code == EXIT_OK, (
        f"valid spec with --strict should exit {EXIT_OK}; "
        f"got {result.exit_code}\nstdout:\n{result.stdout}"
    )


def test_validate_via_main_swarm_group_exits_zero(tmp_path: Path) -> None:
    """End-to-end: ``superclaude swarm validate <good.json>`` exits 0."""
    from superclaude.cli.main import main

    path = _write_spec(tmp_path, _minimal_valid_spec())
    runner = CliRunner()
    result = runner.invoke(main, ["swarm", "validate", str(path)])
    assert result.exit_code == EXIT_OK, (
        f"superclaude swarm validate <good.json> should exit {EXIT_OK}; "
        f"got {result.exit_code}\noutput:\n{result.output}"
    )


# ---------------------------------------------------------------------------
# Invalid-spec path -- structured diagnostics on stderr
# ---------------------------------------------------------------------------


def test_invalid_spec_missing_required_field_exits_nonzero(
    tmp_path: Path,
) -> None:
    """AC: schema-level failure -> exit 1 with RULE_SCHEMA diagnostic."""
    spec = _minimal_valid_spec()
    del spec["job_id"]
    path = _write_spec(tmp_path, spec)
    runner = CliRunner()
    result = runner.invoke(validate_cmd, [str(path)])
    assert result.exit_code == EXIT_INVALID, (
        f"invalid spec should exit {EXIT_INVALID}; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "FAILED" in result.stderr
    assert RULE_SCHEMA in result.stderr, (
        f"diagnostics must name the failing rule ({RULE_SCHEMA}); "
        f"got stderr:\n{result.stderr}"
    )


def test_invalid_spec_missing_injection_substring_exits_nonzero(
    tmp_path: Path,
) -> None:
    """AC: §11.5 cross-field failure -> exit 1 with RULE_INJECTION_SUBSTRING."""
    spec = _minimal_valid_spec()
    # Replace the prompt.system with one that lacks the canonical substring
    # but otherwise satisfies the JSON Schema. The injection_guard is still
    # enabled with the canonical required_substring, so the cross-field
    # rule fires.
    spec["prompt"]["system"] = "You are a reviewer. No guard sentence here."
    path = _write_spec(tmp_path, spec)
    runner = CliRunner()
    result = runner.invoke(validate_cmd, [str(path)])
    assert result.exit_code == EXIT_INVALID, (
        f"missing §11.5 substring should exit {EXIT_INVALID}; "
        f"got {result.exit_code}\nstdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert RULE_INJECTION_SUBSTRING in result.stderr, (
        f"diagnostics must name {RULE_INJECTION_SUBSTRING}; "
        f"got stderr:\n{result.stderr}"
    )


def test_invalid_spec_wrong_spec_version_exits_nonzero(
    tmp_path: Path,
) -> None:
    """AC: ``spec_version`` drift -> exit 1 with RULE_SPEC_VERSION."""
    spec = _minimal_valid_spec()
    spec["spec_version"] = "999.0"
    path = _write_spec(tmp_path, spec)
    runner = CliRunner()
    result = runner.invoke(validate_cmd, [str(path)])
    assert result.exit_code == EXIT_INVALID
    assert RULE_SPEC_VERSION in result.stderr, (
        f"diagnostics must name {RULE_SPEC_VERSION}; got stderr:\n{result.stderr}"
    )


def test_invalid_spec_custom_prompt_dir_without_custom_lens(
    tmp_path: Path,
) -> None:
    """AC: FR-021 binding violation -> exit 1 with custom-lens rule."""
    spec = _minimal_valid_spec()
    spec["custom_prompt_dir"] = "/abs/path/to/custom/prompts"
    # spec["lens"] is still "bare-review", not "custom" -- triggers the rule.
    path = _write_spec(tmp_path, spec)
    runner = CliRunner()
    result = runner.invoke(validate_cmd, [str(path)])
    assert result.exit_code == EXIT_INVALID
    assert RULE_CUSTOM_PROMPT_DIR_REQUIRES_CUSTOM_LENS in result.stderr, (
        f"diagnostics must name custom_prompt_dir rule; got stderr:\n{result.stderr}"
    )


def test_failure_diagnostics_include_path_and_message(
    tmp_path: Path,
) -> None:
    """Each diagnostic line includes the dotted path and human message."""
    spec = _minimal_valid_spec()
    del spec["lens"]
    path = _write_spec(tmp_path, spec)
    runner = CliRunner()
    result = runner.invoke(validate_cmd, [str(path)])
    assert result.exit_code == EXIT_INVALID
    # The structured render: ``- <rule> @ <path>: <msg>``. ``<root>`` is
    # the placeholder used when JSON-Schema reports a top-level failure
    # with an empty path (e.g., missing required key on the JobSpec
    # dict itself), which is exactly the shape produced by removing
    # the ``lens`` required field.
    assert "@" in result.stderr, (
        "diagnostic format must include ' @ ' between rule and path"
    )


# ---------------------------------------------------------------------------
# Usage-error path (operator typo vs spec error)
# ---------------------------------------------------------------------------


def test_missing_file_exits_with_usage_error(tmp_path: Path) -> None:
    """AC: missing file -> Click's usage error (exit 2)."""
    runner = CliRunner()
    missing = tmp_path / "does-not-exist.json"
    result = runner.invoke(validate_cmd, [str(missing)])
    # Click reports a usage error with exit code 2 when an ``exists=True``
    # path argument is missing. Asserting on the code (not the prose)
    # keeps the test robust against Click version drift.
    assert result.exit_code == EXIT_USAGE, (
        f"missing file should produce a usage error (exit {EXIT_USAGE}); "
        f"got {result.exit_code}\noutput:\n{result.output}"
    )


def test_malformed_json_exits_with_usage_error(tmp_path: Path) -> None:
    """AC: malformed JSON -> exit 2 with a parse-error diagnostic."""
    path = tmp_path / "broken.json"
    path.write_text("{not valid json", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(validate_cmd, [str(path)])
    assert result.exit_code == EXIT_USAGE, (
        f"malformed JSON should exit {EXIT_USAGE}; got {result.exit_code}\n"
        f"output:\n{result.output}"
    )
    assert "not valid JSON" in result.stderr, (
        f"parse error must surface 'not valid JSON'; got stderr:\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# Independence: original fixture is not mutated by edits in tests above.
# ---------------------------------------------------------------------------


def test_fixture_helper_returns_fresh_dict() -> None:
    """Smoke test: each call returns an independent dict (no shared state)."""
    a = _minimal_valid_spec()
    b = _minimal_valid_spec()
    a["job_id"] = "mutated"
    assert b["job_id"] != "mutated", (
        "_minimal_valid_spec must return a fresh dict each call"
    )
    assert a == copy.deepcopy(a)
