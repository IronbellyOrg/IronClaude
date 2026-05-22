"""Tests for ``superclaude.cli.eval.config.EvalConfig``.

Covers cliEval Phase 1 / Task T01.01 acceptance criteria:

* Module exports a frozen ``EvalConfig`` with fields ``paths``, ``defaults``,
  ``allowed_scratch_roots``, and ``min_claude_version``.
* Mutation is rejected (frozen dataclass).
* Default ``allowed_scratch_roots`` contains ``/tmp/eval-runs`` and
  ``.dev/eval-runs``.
* Two instances built from the same inputs compare equal.

Phase 2 / Task T02.20 (R1-mit) extended the schema with
``min_claude_version`` so the ``eval doctor`` ``claude.min_version`` HARD
floor has a single configuration source.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from superclaude.cli.eval.config import EvalConfig


def test_evalconfig_has_required_fields() -> None:
    field_names = {f.name for f in dataclasses.fields(EvalConfig)}
    assert field_names == {
        "paths",
        "defaults",
        "allowed_scratch_roots",
        "min_claude_version",
    }


def test_evalconfig_is_frozen() -> None:
    cfg = EvalConfig()
    with pytest.raises(dataclasses.FrozenInstanceError):
        cfg.paths = {"x": Path("/tmp")}  # type: ignore[misc]


def test_default_allowed_scratch_roots_includes_ac12_paths() -> None:
    cfg = EvalConfig()
    assert Path("/tmp/eval-runs") in cfg.allowed_scratch_roots
    assert Path(".dev/eval-runs") in cfg.allowed_scratch_roots


def test_allowed_scratch_roots_is_immutable_tuple() -> None:
    cfg = EvalConfig()
    assert isinstance(cfg.allowed_scratch_roots, tuple)


def test_deterministic_equality() -> None:
    a = EvalConfig(
        paths={"suites_dir": Path("/x/suites")},
        defaults={"timeout_sec": 30},
        allowed_scratch_roots=(Path("/tmp/eval-runs"),),
    )
    b = EvalConfig(
        paths={"suites_dir": Path("/x/suites")},
        defaults={"timeout_sec": 30},
        allowed_scratch_roots=(Path("/tmp/eval-runs"),),
    )
    assert a == b
    assert hash(a.allowed_scratch_roots) == hash(b.allowed_scratch_roots)


def test_default_factories_yield_independent_defaults() -> None:
    a = EvalConfig()
    b = EvalConfig()
    # paths / defaults mappings should not be shared instances.
    assert a.paths is not b.paths
    assert a.defaults is not b.defaults
