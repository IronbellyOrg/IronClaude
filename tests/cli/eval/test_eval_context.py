"""Tests for ``superclaude.cli.eval.models.EvalContext``.

Covers cliEval Phase 3 / Task T03.03 acceptance criteria (DM-010):

* Module exports a frozen ``EvalContext`` dataclass with the 15 fields
  ``eval_spec, home, home_path, artifacts_dir, run_dir, env, stdout_path,
  stderr_path, transcript_path, jsonl_paths, exit_code, stdout, stderr,
  duration_sec, artifacts``.
* Mutation is rejected (``dataclasses.FrozenInstanceError``) for all
  attribute assignments; mapping fields are wrapped in
  :class:`types.MappingProxyType` so the more subtle attack of mutating
  ``ctx.env["HOME"]`` also fails.
* ``from_runner_state(...)`` is a keyword-only factory that builds an
  ``EvalContext`` from runner internals deterministically.
* The ``home.home_path == home_path`` invariant holds after factory
  construction.

Cross-link: ``EvalSpec`` (DM-002 / T01.03) and ``HomeIsolation`` (DM-006 /
T02.04 / T02.11) supply the runtime state the factory wraps. ``EvalContext``
is consumed by every ``ExpectCallable`` (FR-EXP1 / T04.01).
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from types import MappingProxyType

import pytest

from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.isolation import HomeIsolation
from superclaude.cli.eval.models import (
    EvalContext,
    EvalSpec,
    _EVAL_CONTEXT_FIELDS,
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
        eval_id="ExampleEval1",
        home_root=scratch_root,
        session_id="sess-001",
    )
    iso.setup(config=EvalConfig(allowed_scratch_roots=(scratch_root,)))
    return iso


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="ExampleEval1", title="example")


def _build_paths(home_path: Path, run_dir: Path) -> dict[str, Path]:
    artifacts_dir = home_path / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    return {
        "artifacts_dir": artifacts_dir,
        "run_dir": run_dir,
        "stdout_path": artifacts_dir / "stdout.log",
        "stderr_path": artifacts_dir / "stderr.log",
        "transcript_path": artifacts_dir / "pty.transcript",
    }


def _ctx_kwargs(
    *,
    eval_spec: EvalSpec,
    home: HomeIsolation,
    run_dir: Path,
) -> dict[str, object]:
    paths = _build_paths(home.home_path, run_dir)
    return {
        "eval_spec": eval_spec,
        "home": home,
        "run_dir": paths["run_dir"],
        "artifacts_dir": paths["artifacts_dir"],
        "stdout_path": paths["stdout_path"],
        "stderr_path": paths["stderr_path"],
        "transcript_path": paths["transcript_path"],
        "jsonl_paths": {"hook_log": paths["artifacts_dir"] / "hooks.jsonl"},
        "env": {"HOME": str(home.home_path), "CLAUDE_SESSION_ID": home.session_id},
        "exit_code": 0,
        "stdout": "hello\n",
        "stderr": "",
        "duration_sec": 1.25,
        "artifacts": {"stdout": str(paths["stdout_path"])},
    }


# ---------------------------------------------------------------------------
# Field schema and frozen contract
# ---------------------------------------------------------------------------


def test_eval_context_has_required_fields() -> None:
    field_names = [f.name for f in dataclasses.fields(EvalContext)]
    # Field order matches DM-010 verbatim so attribute traversal stays
    # deterministic across review diffs and downstream consumers.
    assert field_names == [
        "eval_spec",
        "home",
        "home_path",
        "artifacts_dir",
        "run_dir",
        "env",
        "stdout_path",
        "stderr_path",
        "transcript_path",
        "jsonl_paths",
        "exit_code",
        "stdout",
        "stderr",
        "duration_sec",
        "artifacts",
    ]
    assert len(field_names) == 15


def test_eval_context_field_order_constant_matches_dataclass() -> None:
    # ``_EVAL_CONTEXT_FIELDS`` is the canonical declaration order; if a
    # future change reorders the dataclass without updating the constant
    # the helper would silently desync.
    field_names = tuple(f.name for f in dataclasses.fields(EvalContext))
    assert _EVAL_CONTEXT_FIELDS == field_names


def test_eval_context_is_frozen(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = EvalContext.from_runner_state(
        **_ctx_kwargs(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        ctx.exit_code = 1  # type: ignore[misc]


@pytest.mark.parametrize(
    "field_name",
    [
        "eval_spec",
        "home",
        "home_path",
        "artifacts_dir",
        "run_dir",
        "env",
        "stdout_path",
        "stderr_path",
        "transcript_path",
        "jsonl_paths",
        "exit_code",
        "stdout",
        "stderr",
        "duration_sec",
        "artifacts",
    ],
)
def test_eval_context_every_field_is_frozen(
    eval_spec: EvalSpec,
    home: HomeIsolation,
    tmp_path: Path,
    field_name: str,
) -> None:
    # Acceptance: "EvalContext instances reject mutation
    # (FrozenInstanceError on attempted set)". Cover every field
    # individually so a future caller-introduced ``object.__setattr__``
    # bypass cannot quietly land.
    ctx = EvalContext.from_runner_state(
        **_ctx_kwargs(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(ctx, field_name, "tampered")


# ---------------------------------------------------------------------------
# Mapping proxy immutability (the more subtle attack surface)
# ---------------------------------------------------------------------------


def test_eval_context_env_is_mapping_proxy(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = EvalContext.from_runner_state(
        **_ctx_kwargs(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    )
    assert isinstance(ctx.env, MappingProxyType)
    with pytest.raises(TypeError):
        ctx.env["HOME"] = "/tmp/elsewhere"  # type: ignore[index]


def test_eval_context_jsonl_paths_is_mapping_proxy(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = EvalContext.from_runner_state(
        **_ctx_kwargs(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    )
    assert isinstance(ctx.jsonl_paths, MappingProxyType)
    with pytest.raises(TypeError):
        ctx.jsonl_paths["telemetry"] = tmp_path / "x"  # type: ignore[index]


def test_eval_context_artifacts_is_mapping_proxy(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = EvalContext.from_runner_state(
        **_ctx_kwargs(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    )
    assert isinstance(ctx.artifacts, MappingProxyType)
    with pytest.raises(TypeError):
        ctx.artifacts["new"] = "/tmp/x"  # type: ignore[index]


def test_eval_context_direct_construction_also_wraps_mappings(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    # Direct ``EvalContext(...)`` is permitted (test ergonomics), but the
    # ``__post_init__`` hook must still wrap mapping fields so the
    # frozen-dataclass invariant covers their interior state.
    paths = _build_paths(home.home_path, tmp_path)
    ctx = EvalContext(
        eval_spec=eval_spec,
        home=home,
        home_path=home.home_path,
        artifacts_dir=paths["artifacts_dir"],
        run_dir=paths["run_dir"],
        env={"HOME": str(home.home_path)},  # plain dict — must be proxied
        stdout_path=paths["stdout_path"],
        stderr_path=paths["stderr_path"],
        transcript_path=paths["transcript_path"],
        jsonl_paths={"hook_log": paths["artifacts_dir"] / "hooks.jsonl"},
        exit_code=0,
        stdout="",
        stderr="",
        duration_sec=0.0,
        artifacts={},
    )
    assert isinstance(ctx.env, MappingProxyType)
    assert isinstance(ctx.jsonl_paths, MappingProxyType)
    assert isinstance(ctx.artifacts, MappingProxyType)


def test_eval_context_factory_isolates_env_from_caller_mutation(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    # The factory wraps mappings in ``MappingProxyType(dict(env))`` — that
    # ``dict(env)`` shallow copy means a caller that mutates the source
    # mapping after construction does not bleed into the context.
    source_env: dict[str, str] = {"HOME": str(home.home_path)}
    kwargs = _ctx_kwargs(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    kwargs["env"] = source_env
    ctx = EvalContext.from_runner_state(**kwargs)  # type: ignore[arg-type]
    source_env["HOME"] = "/tmp/elsewhere"
    assert ctx.env["HOME"] == str(home.home_path)


# ---------------------------------------------------------------------------
# Factory contract
# ---------------------------------------------------------------------------


def test_from_runner_state_resolves_home_path_from_home(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    # The factory must pull ``home_path`` off the ``HomeIsolation`` so the
    # invariant ``ctx.home.home_path == ctx.home_path`` holds and runner
    # code does not duplicate the lookup at the call site.
    kwargs = _ctx_kwargs(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    ctx = EvalContext.from_runner_state(**kwargs)  # type: ignore[arg-type]
    assert ctx.home_path == home.home_path
    assert ctx.home is home


def test_from_runner_state_raises_when_home_not_setup(
    eval_spec: EvalSpec, scratch_root: Path, tmp_path: Path
) -> None:
    # ``HomeIsolation.home_path`` raises ``RuntimeError`` when setup has
    # not run; the factory propagates that error so the failure surfaces
    # at context construction rather than later when an ExpectCallable
    # reads ``ctx.home_path``.
    unsetup = HomeIsolation(
        eval_id="ExampleEval1",
        home_root=scratch_root,
        session_id="sess-001",
    )
    paths = _build_paths(scratch_root, tmp_path)
    with pytest.raises(RuntimeError, match="setup"):
        EvalContext.from_runner_state(
            eval_spec=eval_spec,
            home=unsetup,
            run_dir=paths["run_dir"],
            artifacts_dir=paths["artifacts_dir"],
            stdout_path=paths["stdout_path"],
            stderr_path=paths["stderr_path"],
            transcript_path=paths["transcript_path"],
            jsonl_paths={},
            env={},
            exit_code=0,
            stdout="",
            stderr="",
            duration_sec=0.0,
            artifacts={},
        )


def test_from_runner_state_keyword_only_arguments(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    # Keyword-only enforcement guards future field additions: a positional
    # call must raise ``TypeError`` rather than silently re-bind a value.
    with pytest.raises(TypeError):
        EvalContext.from_runner_state(  # type: ignore[misc]
            eval_spec,
            home,
            tmp_path,
        )


def test_from_runner_state_is_deterministic(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    # AC: "from_runner_state() constructs an EvalContext from EvalSpec +
    # HomeIsolation + run outputs deterministically." — two calls with
    # identical arguments compare equal.
    kwargs = _ctx_kwargs(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    a = EvalContext.from_runner_state(**kwargs)  # type: ignore[arg-type]
    b = EvalContext.from_runner_state(**kwargs)  # type: ignore[arg-type]
    assert a == b


def test_from_runner_state_field_values_round_trip(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    # Each kwarg lands on the corresponding attribute verbatim (modulo
    # the mapping-proxy wrapping that ``__post_init__`` performs).
    kwargs = _ctx_kwargs(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    ctx = EvalContext.from_runner_state(**kwargs)  # type: ignore[arg-type]
    assert ctx.eval_spec is eval_spec
    assert ctx.home is home
    assert ctx.home_path == home.home_path
    assert ctx.artifacts_dir == kwargs["artifacts_dir"]
    assert ctx.run_dir == kwargs["run_dir"]
    assert ctx.stdout_path == kwargs["stdout_path"]
    assert ctx.stderr_path == kwargs["stderr_path"]
    assert ctx.transcript_path == kwargs["transcript_path"]
    assert dict(ctx.jsonl_paths) == dict(kwargs["jsonl_paths"])  # type: ignore[arg-type]
    assert dict(ctx.env) == dict(kwargs["env"])  # type: ignore[arg-type]
    assert ctx.exit_code == kwargs["exit_code"]
    assert ctx.stdout == kwargs["stdout"]
    assert ctx.stderr == kwargs["stderr"]
    assert ctx.duration_sec == kwargs["duration_sec"]
    assert dict(ctx.artifacts) == dict(kwargs["artifacts"])  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Package re-export
# ---------------------------------------------------------------------------


def test_eval_context_reexported_from_package() -> None:
    # Consumers (ExpectCallables, EvalRunner, RunOrchestrator) import the
    # symbol from the package root, not the private models module.
    from superclaude.cli.eval import EvalContext as PkgEvalContext

    assert PkgEvalContext is EvalContext
