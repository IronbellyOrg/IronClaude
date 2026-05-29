"""Tests for ``superclaude.cli.eval.expect`` FR-EXP1 primitives.

Covers cliEval Phase 4 / Task T04.01 acceptance criteria (COMP-010 /
D-0064):

* ``Expect`` exposes 7 primitives ``file``, ``jsonl``, ``settings_json``,
  ``exit_code``, ``stderr``, ``stdout``, ``duration``.
* None of the primitives raise ``NotImplementedError``.
* Each primitive returns an ``ExpectCallable`` (callable taking an
  ``EvalContext`` and returning an ``ExpectResult``).
* Declarative invocation via :meth:`Expect.from_mapping` reaches the same
  primitive and produces an equivalent result for matching inputs.
* ``Expect.exit_code`` rejects mutually-exclusive ``equals`` + ``in_set``.

Per-primitive edge-case coverage (negative cases, regex, key-paths,
timing bounds) lands in T04.02..T04.08.
"""

from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Any, Mapping

import pytest

from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.expect import PRIMITIVE_NAMES, Expect
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
        eval_id="ExpectPrimitiveEval1",
        home_root=scratch_root,
        session_id="sess-expect-001",
    )
    iso.setup(config=EvalConfig(allowed_scratch_roots=(scratch_root,)))
    return iso


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="ExpectPrimitiveEval1", title="expect primitives")


def _make_ctx(
    *,
    eval_spec: EvalSpec,
    home: HomeIsolation,
    run_dir: Path,
    exit_code: int = 0,
    stdout: str = "",
    stderr: str = "",
    duration_sec: float = 0.5,
    jsonl_paths: Mapping[str, Path] | None = None,
) -> EvalContext:
    artifacts_dir = home.home_path / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = artifacts_dir / "stdout.log"
    stderr_path = artifacts_dir / "stderr.log"
    transcript_path = artifacts_dir / "pty.transcript"
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    return EvalContext.from_runner_state(
        eval_spec=eval_spec,
        home=home,
        run_dir=run_dir,
        artifacts_dir=artifacts_dir,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        transcript_path=transcript_path,
        jsonl_paths=jsonl_paths or {},
        env={"HOME": str(home.home_path)},
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        duration_sec=duration_sec,
        artifacts={},
    )


# ---------------------------------------------------------------------------
# Surface tests
# ---------------------------------------------------------------------------


def test_primitive_names_matches_attribute_surface() -> None:
    # Every primitive name resolves to a static method on Expect.
    assert PRIMITIVE_NAMES == (
        "file",
        "jsonl",
        "settings_json",
        "exit_code",
        "stderr",
        "stdout",
        "duration",
    )
    for name in PRIMITIVE_NAMES:
        attr = getattr(Expect, name)
        assert callable(attr), f"Expect.{name} must be callable"


@pytest.mark.parametrize("name", list(PRIMITIVE_NAMES))
def test_primitive_construction_does_not_raise_notimplemented(name: str) -> None:
    """T04.01 AC: no primitive raises NotImplementedError on construction."""

    # Build with permissive defaults (no kwargs) so any
    # NotImplementedError in the M1 stubs is caught at construction time.
    # exit_code is the only one whose default kwargs change behaviour, and
    # it must construct cleanly with `equals=0` defaults.
    primitive = getattr(Expect, name)
    sig = inspect.signature(primitive)
    # We deliberately call with no kwargs; primitives that need a path
    # (file, jsonl, settings_json) take it as a keyword-only argument and
    # we supply a placeholder for those.
    kwargs: dict[str, Any] = {}
    if "path" in sig.parameters:
        kwargs["path"] = "placeholder.txt"
    if "key_path" in sig.parameters:
        kwargs["key_path"] = "a.b"
    callable_ = primitive(**kwargs)
    assert callable(callable_), f"Expect.{name}(...) must return a callable"
    assert callable_.__name__ == name


# ---------------------------------------------------------------------------
# Programmatic invocation — each primitive runs end-to-end
# ---------------------------------------------------------------------------


def test_file_passes_when_content_matches(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    target = home.home_path / "note.txt"
    target.write_text("hello world\n", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="note.txt", contains="hello")(ctx)
    assert isinstance(result, ExpectResult)
    assert result.passed
    assert result.name == "file"
    assert result.failure is None


def test_file_fails_when_substring_missing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    target = home.home_path / "note.txt"
    target.write_text("hello world\n", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="note.txt", contains="goodbye")(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expect_name == "file"


def test_jsonl_passes_with_line_count(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    log_path = home.home_path / "hooks.jsonl"
    log_path.write_text('{"event": "a"}\n{"event": "b"}\n', encoding="utf-8")
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        jsonl_paths={"hook_log": log_path},
    )
    result = Expect.jsonl(path="hook_log", line_count=2)(ctx)
    assert result.passed, result.message
    assert result.name == "jsonl"


def test_jsonl_assert_any_finds_matching_row(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    log_path = home.home_path / "hooks.jsonl"
    log_path.write_text('{"event": "a"}\n{"event": "b"}\n', encoding="utf-8")
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        jsonl_paths={"hook_log": log_path},
    )
    result = Expect.jsonl(
        path="hook_log",
        assert_any=lambda row: row.get("event") == "b",
    )(ctx)
    assert result.passed


def test_settings_json_passes_on_key_equals(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    settings = home.home_path / "settings.json"
    settings.write_text(
        json.dumps({"hooks": {"matchers": ["PreToolUse"]}}),
        encoding="utf-8",
    )
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(
        path="settings.json",
        key_path="hooks.matchers",
        equals=["PreToolUse"],
    )(ctx)
    assert result.passed, result.message


def test_settings_json_exists_flag(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    settings = home.home_path / "settings.json"
    settings.write_text(json.dumps({"x": 1}), encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.settings_json(path="settings.json", key_path="y", exists=False)(ctx)
    assert result.passed


def test_exit_code_default_passes_on_zero(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    result = Expect.exit_code()(ctx)
    assert result.passed


def test_exit_code_fails_on_mismatch(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=1)
    result = Expect.exit_code(equals=0)(ctx)
    assert not result.passed
    assert result.failure is not None and result.failure.actual == 1


def test_exit_code_in_set_passes(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=2)
    result = Expect.exit_code(in_set={0, 2})(ctx)
    assert result.passed


def test_exit_code_rejects_equals_and_in_set_together() -> None:
    with pytest.raises(ValueError):
        Expect.exit_code(equals=0, in_set={0, 1})


def test_stdout_predicate(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="welcome to the harness\n",
    )
    assert Expect.stdout(contains="welcome")(ctx).passed
    assert not Expect.stdout(contains="absent")(ctx).passed


def test_stderr_predicate(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stderr="Error: something failed\n",
    )
    assert Expect.stderr(regex=r"Error:\s+\w+")(ctx).passed


def test_duration_informational_passes(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=2.5)
    result = Expect.duration()(ctx)
    assert result.passed
    assert result.details["observed_sec"] == 2.5


def test_duration_max_sec_fails_over_budget(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=5.0)
    result = Expect.duration(max_sec=1.0)(ctx)
    assert not result.passed
    assert result.failure is not None


# ---------------------------------------------------------------------------
# Declarative invocation — Expect.from_mapping resolves YAML rows
# ---------------------------------------------------------------------------


def test_from_mapping_equivalent_to_programmatic_exit_code(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    decl = Expect.from_mapping({"exit_code": {"equals": 0}})(ctx)
    prog = Expect.exit_code(equals=0)(ctx)
    assert decl.passed and prog.passed
    assert decl.name == prog.name == "exit_code"


def test_from_mapping_empty_value_invokes_with_defaults(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    result = Expect.from_mapping({"exit_code": {}})(ctx)
    assert result.passed
    assert result.name == "exit_code"


def test_from_mapping_rejects_unknown_primitive() -> None:
    with pytest.raises(ValueError, match="Unknown Expect primitive"):
        Expect.from_mapping({"not_a_real_primitive": {}})


def test_from_mapping_rejects_multi_key_mapping() -> None:
    with pytest.raises(ValueError, match="exactly one primitive key"):
        Expect.from_mapping({"exit_code": {}, "stdout": {}})


def test_from_mapping_threads_kwargs_to_file_primitive(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    (home.home_path / "report.txt").write_text("PASS\n", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.from_mapping({"file": {"path": "report.txt", "contains": "PASS"}})(
        ctx
    )
    assert result.passed
