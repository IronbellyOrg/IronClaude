"""Tests for ``superclaude.cli.eval.capabilities.CapabilityReport``.

Covers cliEval Phase 1 / Task T01.10 acceptance criteria (DM-008):

* ``CapabilityReport`` exposes the 6 list fields named in DM-008 and a
  ``to_json()`` method.
* ``to_json()`` produces a JSON-serializable mapping per DM-008.
* Empty report serialises to a stable canonical form documented in
  ``spec.md``.

Cross-links: FR-CLI4 ``eval doctor`` (T01.13) consumes ``to_json()``;
COMP-009 ``CapabilityGates`` (T01.11) produces these reports.
"""

from __future__ import annotations

import dataclasses
import json

import pytest

from superclaude.cli.eval.capabilities import (
    CapabilityReport,
    CapabilityStatus,
)


def _passing_status() -> CapabilityStatus:
    return CapabilityStatus(
        name="binary.claude",
        passed=True,
        failure_mode="hard",
        description="Claude CLI on PATH",
        detail="/usr/local/bin/claude (v0.5.3)",
    )


def _failing_status() -> CapabilityStatus:
    return CapabilityStatus(
        name="mcp_server.airis-mcp-gateway",
        passed=False,
        failure_mode="skip",
        description="AIRIS MCP gateway reachable",
        detail="connection refused",
    )


def test_capability_report_has_six_list_fields() -> None:
    field_names = [f.name for f in dataclasses.fields(CapabilityReport)]
    assert field_names == [
        "report",
        "blocked_evals",
        "skip_flags",
        "hard_failures",
        "soft_skips",
        "soft_xfails",
    ]


def test_capability_report_is_frozen() -> None:
    report = CapabilityReport()
    with pytest.raises(dataclasses.FrozenInstanceError):
        report.blocked_evals = ("E1",)  # type: ignore[misc]


def test_capability_report_defaults_to_empty_tuples() -> None:
    report = CapabilityReport()
    assert report.report == ()
    assert report.blocked_evals == ()
    assert report.skip_flags == ()
    assert report.hard_failures == ()
    assert report.soft_skips == ()
    assert report.soft_xfails == ()


def test_capability_report_to_json_returns_mapping() -> None:
    report = CapabilityReport()
    payload = report.to_json()
    assert isinstance(payload, dict)
    # JSON-serializable per DM-008.
    encoded = json.dumps(payload)
    assert json.loads(encoded) == payload


def test_capability_report_empty_to_json_canonical_shape() -> None:
    """Empty report serialises to a stable canonical form (spec.md)."""
    report = CapabilityReport()
    assert report.to_json() == {
        "report": [],
        "blocked_evals": [],
        "skip_flags": [],
        "hard_failures": [],
        "soft_skips": [],
        "soft_xfails": [],
    }


def test_capability_report_populated_to_json_roundtrips() -> None:
    report = CapabilityReport(
        report=(_passing_status(), _failing_status()),
        blocked_evals=("E5",),
        skip_flags=("--no-mcp",),
        hard_failures=(),
        soft_skips=("mcp_server.airis-mcp-gateway",),
        soft_xfails=(),
    )
    payload = report.to_json()
    # Top-level keys preserve dataclass field order.
    assert list(payload.keys()) == [
        "report",
        "blocked_evals",
        "skip_flags",
        "hard_failures",
        "soft_skips",
        "soft_xfails",
    ]
    # report[] entries are dicts, not dataclass instances (JSON-safe).
    assert payload["report"][0]["name"] == "binary.claude"
    assert payload["report"][0]["passed"] is True
    assert payload["report"][0]["failure_mode"] == "hard"
    assert payload["report"][1]["passed"] is False
    assert payload["report"][1]["failure_mode"] == "skip"
    # Scalar tuple fields are emitted as JSON arrays.
    assert payload["blocked_evals"] == ["E5"]
    assert payload["skip_flags"] == ["--no-mcp"]
    assert payload["soft_skips"] == ["mcp_server.airis-mcp-gateway"]
    # Round-trips through json.dumps without loss.
    assert json.loads(json.dumps(payload)) == payload


def test_capability_report_equality_is_structural() -> None:
    a = CapabilityReport(
        report=(_passing_status(),),
        blocked_evals=("E1", "E2"),
        skip_flags=("--no-mcp",),
        hard_failures=(),
        soft_skips=("mcp_server.auggie",),
        soft_xfails=(),
    )
    b = CapabilityReport(
        report=(_passing_status(),),
        blocked_evals=("E1", "E2"),
        skip_flags=("--no-mcp",),
        hard_failures=(),
        soft_skips=("mcp_server.auggie",),
        soft_xfails=(),
    )
    assert a == b
    assert a != dataclasses.replace(a, blocked_evals=("E1",))


def test_capability_status_has_required_fields() -> None:
    field_names = {f.name for f in dataclasses.fields(CapabilityStatus)}
    assert field_names == {
        "name",
        "passed",
        "failure_mode",
        "description",
        "detail",
        "skipped_by_flag",
    }


def test_capability_status_rejects_invalid_failure_mode() -> None:
    with pytest.raises(ValueError):
        CapabilityStatus(
            name="x",
            passed=True,
            failure_mode="warn",  # type: ignore[arg-type]
        )


def test_capability_status_to_dict_is_json_safe() -> None:
    status = _passing_status()
    json.dumps(status.to_dict())  # no TypeError raised
