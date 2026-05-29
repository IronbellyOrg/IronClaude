"""COMP-015 probe — pin the upstream AggregatedPhaseReport shape (Task T03.14).

Read-only smoke test pinning the public surface of
``superclaude.cli.sprint.executor.AggregatedPhaseReport`` and the
``aggregate_task_results`` factory it pairs with. These live at
``src/superclaude/cli/sprint/executor.py`` (lines 190-335 at the time of
authoring). COMP-008 Reporter / AggregatedRunReport (T03.13) reuses this
shape as its pattern reference; if any upstream rename, field reorder,
signature drift, or property removal lands first, this probe must fail
loud so the eval reporter is fixed up rather than silently drifting from
the runner-constructed phase report contract.

Probe discipline:

* No ``AggregatedPhaseReport`` instance is constructed. All assertions go
  through ``dataclasses.fields`` and :mod:`inspect`.
* No subprocess is spawned and no files are written.
* If any assertion in this file fails, an upstream refactor of
  ``cli/sprint/executor.py:AggregatedPhaseReport`` /
  ``aggregate_task_results`` has occurred and the AggregatedRunReport
  downstream assumptions need to be re-validated before re-pinning.
"""

from __future__ import annotations

import dataclasses
import inspect
from typing import get_type_hints

import pytest

from superclaude.cli.sprint import executor as _executor_module
from superclaude.cli.sprint.executor import (
    AggregatedPhaseReport,
    TaskResult,
    aggregate_task_results,
)

# --- class identity --------------------------------------------------------


def test_aggregated_phase_report_is_dataclass() -> None:
    """AggregatedPhaseReport must remain a dataclass — AggregatedRunReport
    introspects its fields when mirroring the runner-constructed shape."""

    assert dataclasses.is_dataclass(AggregatedPhaseReport)


def test_aggregated_phase_report_lives_in_sprint_executor_module() -> None:
    """Pin the import path so the eval Reporter pattern reference does not
    silently shift to a renamed module."""

    assert AggregatedPhaseReport.__module__ == "superclaude.cli.sprint.executor"
    assert getattr(_executor_module, "AggregatedPhaseReport") is AggregatedPhaseReport


# --- field contract --------------------------------------------------------


_EXPECTED_FIELDS: tuple[tuple[str, type], ...] = (
    ("phase_number", int),
    ("tasks_total", int),
    ("tasks_passed", int),
    ("tasks_failed", int),
    ("tasks_incomplete", int),
    ("tasks_skipped", int),
    ("tasks_not_attempted", int),
    ("budget_remaining", int),
    ("total_turns_consumed", int),
    ("total_duration_seconds", float),
    ("task_results", list[TaskResult]),
    ("remaining_task_ids", list[str]),
)


def test_aggregated_phase_report_field_names_and_order() -> None:
    """The 12 fields and their order must match the upstream contract."""

    names = tuple(f.name for f in dataclasses.fields(AggregatedPhaseReport))
    assert names == tuple(name for name, _ in _EXPECTED_FIELDS)


@pytest.mark.parametrize(("field_name", "field_type"), _EXPECTED_FIELDS)
def test_aggregated_phase_report_field_types(field_name: str, field_type: type) -> None:
    """Each pinned field must keep its typed annotation."""

    hints = get_type_hints(AggregatedPhaseReport)
    assert hints[field_name] == field_type


# --- method / property surface --------------------------------------------


_EXPECTED_METHODS: tuple[str, ...] = ("to_yaml", "to_markdown")


@pytest.mark.parametrize("method_name", _EXPECTED_METHODS)
def test_aggregated_phase_report_emitter_methods_present(method_name: str) -> None:
    """The two emitter methods used as the AggregatedRunReport pattern
    reference must remain on the class."""

    attr = inspect.getattr_static(AggregatedPhaseReport, method_name)
    assert inspect.isfunction(attr)


@pytest.mark.parametrize("method_name", _EXPECTED_METHODS)
def test_aggregated_phase_report_emitter_returns_str(method_name: str) -> None:
    """Both emitters must keep their ``-> str`` return annotation so the
    eval Reporter can mirror the signature without coercion."""

    method = inspect.getattr_static(AggregatedPhaseReport, method_name)
    hints = get_type_hints(method)
    assert hints["return"] is str


@pytest.mark.parametrize("method_name", _EXPECTED_METHODS)
def test_aggregated_phase_report_emitter_takes_only_self(method_name: str) -> None:
    """Emitters must remain no-arg (besides ``self``) so the Reporter can
    drive them positionally."""

    method = inspect.getattr_static(AggregatedPhaseReport, method_name)
    sig = inspect.signature(method)
    assert tuple(sig.parameters.keys()) == ("self",)


def test_aggregated_phase_report_status_is_property() -> None:
    """``status`` must remain a computed property so the eval Reporter can
    treat the aggregate's overall outcome as derived state."""

    attr = inspect.getattr_static(AggregatedPhaseReport, "status")
    assert isinstance(attr, property)


def test_aggregated_phase_report_status_returns_str() -> None:
    """``status`` property must keep its ``-> str`` annotation."""

    fget = inspect.getattr_static(AggregatedPhaseReport, "status").fget
    assert fget is not None
    hints = get_type_hints(fget)
    assert hints["return"] is str


# --- aggregate_task_results factory ---------------------------------------


def test_aggregate_task_results_signature_pin() -> None:
    """``aggregate_task_results`` is the canonical construction entry point
    that AggregatedRunReport mirrors. Pin its parameter set and return
    annotation so a downstream rename or arg reshuffle does not silently
    invalidate the pattern reference."""

    sig = inspect.signature(aggregate_task_results)
    params = sig.parameters
    assert tuple(params.keys()) == (
        "phase_number",
        "task_results",
        "remaining_task_ids",
        "budget_remaining",
    )
    for param in params.values():
        assert param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD

    hints = get_type_hints(aggregate_task_results)
    assert hints["return"] is AggregatedPhaseReport


def test_aggregate_task_results_module_path() -> None:
    """``aggregate_task_results`` must remain co-located with
    ``AggregatedPhaseReport``."""

    assert aggregate_task_results.__module__ == "superclaude.cli.sprint.executor"
