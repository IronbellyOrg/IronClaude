"""COMP-012 probe — pin the upstream IsolationLayers API surface (Task T02.05).

Read-only smoke test pinning the public shape of
``superclaude.cli.sprint.executor.IsolationLayers`` and the
``setup_isolation`` factory it pairs with. These live at
``src/superclaude/cli/sprint/executor.py`` (lines 107-182 at the time of
authoring). HomeIsolation extension (COMP-006 / T02.07 / T02.11) layers
HOME, CLAUDE_SESSION_ID, and CLAUDE_FAKE_TIME_OFFSET on top of this
record; if any upstream rename, field reorder, signature drift, or
property removal lands first, this probe must fail loud so the extension
work is fixed up rather than silently breaking the 4 existing isolation
guarantees (scoped_work_dir / git_boundary / plugin_dir / settings_dir).

Probe discipline:

* No ``IsolationLayers`` instance is constructed. All assertions go
  through ``dataclasses.fields`` and :mod:`inspect`.
* No subprocess is spawned and no env vars are written.
* If any assertion in this file fails, an upstream refactor of
  ``cli/sprint/executor.py:IsolationLayers`` / ``setup_isolation`` has
  occurred and downstream HomeIsolation extension assumptions need to be
  re-validated before re-pinning.
"""

from __future__ import annotations

import dataclasses
import inspect
from pathlib import Path
from typing import get_type_hints

import pytest

from superclaude.cli.sprint import executor as _executor_module
from superclaude.cli.sprint.executor import IsolationLayers, setup_isolation

# --- class identity --------------------------------------------------------


def test_isolation_layers_is_dataclass() -> None:
    """IsolationLayers must remain a dataclass — HomeIsolation extension relies on
    ``dataclasses.fields`` for field introspection."""

    assert dataclasses.is_dataclass(IsolationLayers)


def test_isolation_layers_lives_in_sprint_executor_module() -> None:
    """Pin the import path so HomeIsolation extension does not silently shift
    to a renamed module."""

    assert IsolationLayers.__module__ == "superclaude.cli.sprint.executor"
    assert getattr(_executor_module, "IsolationLayers") is IsolationLayers


# --- field contract --------------------------------------------------------


_EXPECTED_FIELDS: tuple[tuple[str, type], ...] = (
    ("scoped_work_dir", Path),
    ("git_boundary", Path),
    ("plugin_dir", Path),
    ("settings_dir", Path),
)


def test_isolation_layers_field_names_and_order() -> None:
    """The 4 layer fields and their order must match the upstream contract."""

    names = tuple(f.name for f in dataclasses.fields(IsolationLayers))
    assert names == tuple(name for name, _ in _EXPECTED_FIELDS)


@pytest.mark.parametrize(("field_name", "field_type"), _EXPECTED_FIELDS)
def test_isolation_layers_field_types(field_name: str, field_type: type) -> None:
    """All 4 layer fields must remain typed as ``pathlib.Path``."""

    hints = get_type_hints(IsolationLayers)
    assert hints[field_name] is field_type


# --- property surface ------------------------------------------------------


def test_isolation_layers_env_vars_is_property() -> None:
    """``env_vars`` must be exposed as a property (no-arg accessor)."""

    attr = inspect.getattr_static(IsolationLayers, "env_vars")
    assert isinstance(attr, property)


def test_isolation_layers_env_vars_return_annotation_is_str_dict() -> None:
    """``env_vars`` annotated return must remain ``dict[str, str]`` so the
    HomeIsolation extension can merge its own dict without coercion."""

    fget = inspect.getattr_static(IsolationLayers, "env_vars").fget
    assert fget is not None
    hints = get_type_hints(fget)
    assert hints["return"] == dict[str, str]


def test_isolation_layers_layers_active_is_property() -> None:
    """``layers_active`` must remain a property so verification call-sites do
    not need to know whether it is a method."""

    attr = inspect.getattr_static(IsolationLayers, "layers_active")
    assert isinstance(attr, property)


def test_isolation_layers_layers_active_return_annotation_is_list_str() -> None:
    """``layers_active`` annotated return must remain ``list[str]``."""

    fget = inspect.getattr_static(IsolationLayers, "layers_active").fget
    assert fget is not None
    hints = get_type_hints(fget)
    assert hints["return"] == list[str]


# --- setup_isolation factory ----------------------------------------------


def test_setup_isolation_signature_pin() -> None:
    """``setup_isolation`` is the construction entry point that HomeIsolation
    will sit alongside; pin its parameter set and return annotation."""

    sig = inspect.signature(setup_isolation)
    params = sig.parameters
    # H1 (TASK-RF-SPRINTCLI-WIRE-DEAD): a keyword-only ``scope`` param was added
    # so each phase/task/worker can get its own settings dir. Re-pinned to the
    # new contract — ``config`` stays positional-or-keyword, ``scope`` is
    # keyword-only with an empty-string default (scope="" == legacy behavior).
    assert tuple(params.keys()) == ("config", "scope")
    assert params["config"].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params["scope"].kind == inspect.Parameter.KEYWORD_ONLY
    assert params["scope"].default == ""

    hints = get_type_hints(setup_isolation)
    assert hints["return"] is IsolationLayers


def test_setup_isolation_module_path() -> None:
    """``setup_isolation`` must remain co-located with ``IsolationLayers``."""

    assert setup_isolation.__module__ == "superclaude.cli.sprint.executor"
