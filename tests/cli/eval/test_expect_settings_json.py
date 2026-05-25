"""Per-primitive tests for ``Expect.settings_json`` (COMP-010.3 / D-0067 / T04.04).

Covers all four named arguments of
``Expect.settings_json(path, key_path, equals=None, exists=None)`` with
positive and negative cases, plus the path-resolution invariant that
``path`` resolves against :attr:`HomeIsolation.home_path` rather than the
real ``~/.claude`` on the host (DM-006 / NFR-ISO1).

T04.01's ``tests/cli/eval/test_expect_primitives.py`` covers the
declarative surface and one happy / one sad path; this module is the
COMP-010.3 acceptance harness — it touches each named argument in
isolation and in combination, plus argument edge cases (nested key_path
traversal, JSON null equality via the sentinel-aware ``equals``, missing
file path, malformed JSON, ``exists=False`` for absent key paths).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import pytest

from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.expect import Expect
from superclaude.cli.eval.isolation import HomeIsolation
from superclaude.cli.eval.models import (
    EvalContext,
    EvalSpec,
    ExpectFailure,
    ExpectResult,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    root = tmp_path / "scratch"
    root.mkdir()
    return root


@pytest.fixture
def home(scratch_root: Path) -> HomeIsolation:
    iso = HomeIsolation(
        eval_id="ExpectSettingsJsonEval1",
        home_root=scratch_root,
        session_id="sess-expect-settings-json-001",
    )
    iso.setup(config=EvalConfig(allowed_scratch_roots=(scratch_root,)))
    return iso


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="ExpectSettingsJsonEval1", title="expect.settings_json coverage")


def _make_ctx(
    *,
    eval_spec: EvalSpec,
    home: HomeIsolation,
    run_dir: Path,
) -> EvalContext:
    artifacts_dir = home.home_path / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = artifacts_dir / "stdout.log"
    stderr_path = artifacts_dir / "stderr.log"
    transcript_path = artifacts_dir / "pty.transcript"
    stdout_path.write_text("", encoding="utf-8")
    stderr_path.write_text("", encoding="utf-8")
    return EvalContext.from_runner_state(
        eval_spec=eval_spec,
        home=home,
        run_dir=run_dir,
        artifacts_dir=artifacts_dir,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        transcript_path=transcript_path,
        jsonl_paths={},
        env={"HOME": str(home.home_path)},
        exit_code=0,
        stdout="",
        stderr="",
        duration_sec=0.0,
        artifacts={},
    )


def _write_settings(home: HomeIsolation, payload: Mapping[str, Any]) -> Path:
    settings = home.home_path / "settings.json"
    settings.write_text(json.dumps(payload), encoding="utf-8")
    return settings


# ---------------------------------------------------------------------------
# Path resolution (against HomeIsolation.home_path)
# ---------------------------------------------------------------------------


def test_relative_path_resolves_against_home_path(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """A relative ``path`` resolves under ``ctx.home_path`` rather than the
    real ``~/.claude`` (DM-006 / NFR-ISO1)."""
    settings = _write_settings(home, {"key": "value"})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="key", equals="value"
    )(ctx)
    assert result.passed, result.message
    assert isinstance(result, ExpectResult)
    assert result.name == "settings_json"
    assert result.details["path"] == str(settings)


def test_absolute_path_is_used_verbatim(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Absolute ``path`` arguments bypass home_path resolution entirely."""
    settings = tmp_path / "absolute-settings.json"
    settings.write_text(json.dumps({"k": 1}), encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path=str(settings), key_path="k", equals=1
    )(ctx)
    assert result.passed
    assert result.details["path"] == str(settings)


def test_resolution_isolated_from_real_home(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Even if the real ``~/.claude/settings.json`` exists, the primitive
    must resolve against ``home.home_path`` (the scratch HOME). We verify
    this by asserting against a payload only the scratch HOME contains."""
    _write_settings(home, {"scratch_only_marker": True})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json",
        key_path="scratch_only_marker",
        equals=True,
    )(ctx)
    assert result.passed
    # And the resolved path is unambiguously under the scratch HOME.
    assert result.details["path"].startswith(str(home.home_path))


def test_missing_settings_file_fails(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Absent settings.json yields an ExpectFailure with a settings_json_present
    expected/actual payload (DM-005)."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="anything", exists=True
    )(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expect_name == "settings_json"
    assert result.failure.expected == {"settings_json_present": True}
    assert result.failure.actual == {"settings_json_present": False}


# ---------------------------------------------------------------------------
# key_path navigation
# ---------------------------------------------------------------------------


def test_key_path_navigates_nested_dicts(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Dot-separated traversal walks nested mappings."""
    _write_settings(
        home,
        {"hooks": {"PreToolUse": {"matchers": ["mcp__auggie__*"]}}},
    )
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json",
        key_path="hooks.PreToolUse.matchers",
        equals=["mcp__auggie__*"],
    )(ctx)
    assert result.passed


def test_key_path_top_level_key(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Single-segment key_path resolves a top-level field."""
    _write_settings(home, {"theme": "dark"})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="theme", equals="dark"
    )(ctx)
    assert result.passed


def test_key_path_short_circuits_on_missing_intermediate(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """When an intermediate segment is absent, traversal short-circuits
    rather than raising; ``equals`` then fails with a missing-key message."""
    _write_settings(home, {"hooks": {}})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json",
        key_path="hooks.PreToolUse.matchers",
        equals=["x"],
    )(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == ["x"]
    assert result.failure.actual is None


def test_key_path_into_non_mapping_value(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Traversing into a non-mapping (string/list) reports the key as
    absent rather than raising a TypeError."""
    _write_settings(home, {"hooks": "not-a-dict"})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json",
        key_path="hooks.PreToolUse",
        exists=False,
    )(ctx)
    assert result.passed
    assert result.details["found"] is False


# ---------------------------------------------------------------------------
# exists semantics
# ---------------------------------------------------------------------------


def test_exists_true_passes_when_key_present(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    _write_settings(home, {"hooks": {"matchers": ["PreToolUse"]}})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="hooks.matchers", exists=True
    )(ctx)
    assert result.passed
    assert result.details["found"] is True


def test_exists_true_fails_when_key_absent(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    _write_settings(home, {"hooks": {}})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="hooks.matchers", exists=True
    )(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == {
        "key_path": "hooks.matchers",
        "exists": True,
    }
    assert result.failure.actual == {
        "key_path": "hooks.matchers",
        "exists": False,
    }


def test_exists_false_passes_when_key_absent(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Asserting a key path *should not* be present."""
    _write_settings(home, {"x": 1})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="y", exists=False
    )(ctx)
    assert result.passed
    assert result.failure is None


def test_exists_false_fails_when_key_present(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    _write_settings(home, {"y": 2})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="y", exists=False
    )(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"key_path": "y", "exists": False}


# ---------------------------------------------------------------------------
# equals semantics
# ---------------------------------------------------------------------------


def test_equals_passes_on_scalar_value(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    _write_settings(home, {"timeout_sec": 30})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="timeout_sec", equals=30
    )(ctx)
    assert result.passed


def test_equals_fails_on_scalar_mismatch(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    _write_settings(home, {"timeout_sec": 30})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="timeout_sec", equals=60
    )(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == 60
    assert result.failure.actual == 30


def test_equals_supports_list_values(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``equals`` compares JSON arrays with strict order + element parity."""
    matchers = ["mcp__auggie__*", "mcp__auggie-mcp__*", "mcp__airis-mcp-gateway__*"]
    _write_settings(home, {"hooks": {"matchers": matchers}})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="hooks.matchers", equals=matchers
    )(ctx)
    assert result.passed


def test_equals_supports_dict_values(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    _write_settings(home, {"hooks": {"PreToolUse": {"limit": 10}}})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json",
        key_path="hooks.PreToolUse",
        equals={"limit": 10},
    )(ctx)
    assert result.passed


def test_equals_distinguishes_null_from_unset(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """The sentinel-aware default lets manifests assert ``equals=None``
    (JSON null) without colliding with the "no equals argument" default."""
    _write_settings(home, {"feature_flag": None})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="feature_flag", equals=None
    )(ctx)
    assert result.passed


def test_equals_fails_when_key_path_missing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``equals`` on a missing key_path yields a clear failure rather than
    a False positive (the JSON-null trap)."""
    _write_settings(home, {"other": 1})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="missing", equals=None
    )(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert "missing" in result.failure.message


# ---------------------------------------------------------------------------
# Combined exists + equals
# ---------------------------------------------------------------------------


def test_exists_true_and_equals_both_evaluated(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """When both ``exists=True`` and ``equals`` are set, both must hold."""
    _write_settings(home, {"hooks": {"matchers": ["A"]}})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    # exists passes, equals passes
    assert Expect.settings_json(
        path="settings.json",
        key_path="hooks.matchers",
        exists=True,
        equals=["A"],
    )(ctx).passed
    # exists passes, equals fails
    miss = Expect.settings_json(
        path="settings.json",
        key_path="hooks.matchers",
        exists=True,
        equals=["B"],
    )(ctx)
    assert not miss.passed
    assert miss.failure is not None and miss.failure.expected == ["B"]


# ---------------------------------------------------------------------------
# Malformed input
# ---------------------------------------------------------------------------


def test_invalid_json_payload_fails(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """A settings.json with invalid JSON returns a failure with the parse
    error captured (not an uncaught ``json.JSONDecodeError``)."""
    settings = home.home_path / "settings.json"
    settings.write_text("{ not-json", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json", key_path="x", exists=True
    )(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == "valid JSON"
    assert result.failure.traceback is not None
    assert "JSONDecodeError" in result.failure.traceback


# ---------------------------------------------------------------------------
# ExpectResult envelope
# ---------------------------------------------------------------------------


def test_result_carries_primitive_name_and_timing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    _write_settings(home, {"k": 1})
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    callable_ = Expect.settings_json(
        path="settings.json", key_path="k", equals=1
    )
    assert callable_.__name__ == "settings_json"
    result = callable_(ctx)
    assert result.name == "settings_json"
    assert result.duration_sec >= 0.0
