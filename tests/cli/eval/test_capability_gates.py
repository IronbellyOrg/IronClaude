"""Tests for ``superclaude.cli.eval.capabilities.CapabilityGates``.

Covers cliEval Phase 1 / Task T01.11 acceptance criteria (COMP-009 /
roadmap R-010):

* ``CapabilityGates`` exposes ``check_all()``, ``which_or_skip()``,
  ``mcp_server_reachable()`` and returns a populated
  :class:`CapabilityReport`.
* Missing ``claude`` on PATH classifies HARD; missing MCP server
  classifies SOFT-SKIP under ``--no-mcp``.
* ``check_all()`` is idempotent — two invocations on the same gate
  instance return equal reports.

Cross-links: FR-CLI4 ``eval doctor`` (T01.13) renders the
``CapabilityReport``; OQ-5 (M2 follow-up) refines the
``mcp_server_reachable`` semantics — the gate's ``mcp_probe`` keyword is
the override hook the M2 patch will use.
"""

from __future__ import annotations

import shutil

import pytest

from superclaude.cli.eval.capabilities import (
    _DEFAULT_CAPABILITY_SPECS,
    Capability,
    CapabilityGates,
    CapabilityReport,
    _CapabilitySpec,
)


def _binary_only_specs() -> tuple[_CapabilitySpec, ...]:
    return tuple(s for s in _DEFAULT_CAPABILITY_SPECS if s.kind == "binary")


def _mcp_only_specs() -> tuple[_CapabilitySpec, ...]:
    return tuple(s for s in _DEFAULT_CAPABILITY_SPECS if s.kind == "mcp_server")


def test_default_roster_contains_expected_binaries_and_mcp_servers() -> None:
    """T01.11 Steps[2]: roster = claude/jq/make/git HARD + 3 MCP SOFT-SKIP."""
    names = {spec.name for spec in _DEFAULT_CAPABILITY_SPECS}
    assert names == {
        "binary.claude",
        "binary.make",
        "binary.jq",
        "binary.git",
        "mcp_server.auggie",
        "mcp_server.auggie-mcp",
        "mcp_server.airis-mcp-gateway",
    }


def test_hard_binaries_are_hard_and_mcp_servers_are_skip() -> None:
    by_name = {spec.name: spec for spec in _DEFAULT_CAPABILITY_SPECS}
    for hard_name in ("binary.claude", "binary.make", "binary.jq", "binary.git"):
        assert by_name[hard_name].failure_mode == "hard"
        assert by_name[hard_name].skip_flag is None
    for soft_name in (
        "mcp_server.auggie",
        "mcp_server.auggie-mcp",
        "mcp_server.airis-mcp-gateway",
    ):
        assert by_name[soft_name].failure_mode == "skip"
        assert by_name[soft_name].skip_flag == "--no-mcp"


def test_check_all_returns_capability_report() -> None:
    report = CapabilityGates().check_all()
    assert isinstance(report, CapabilityReport)
    # One status row per spec in declaration order.
    assert len(report.report) == len(_DEFAULT_CAPABILITY_SPECS)
    assert [row.name for row in report.report] == [
        spec.name for spec in _DEFAULT_CAPABILITY_SPECS
    ]


def test_check_all_is_idempotent() -> None:
    """T01.11 AC: calling twice returns equal reports."""
    gate = CapabilityGates()
    first = gate.check_all()
    second = gate.check_all()
    assert first == second


def test_which_or_skip_resolves_existing_binary(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    passed, detail = CapabilityGates().which_or_skip("ls")
    assert passed is True
    assert detail == "/usr/bin/ls"


def test_which_or_skip_returns_false_when_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: None)
    passed, detail = CapabilityGates().which_or_skip("definitely-missing-xyz")
    assert passed is False
    assert "not found" in detail.lower()


def test_missing_claude_classifies_hard(monkeypatch: pytest.MonkeyPatch) -> None:
    """T01.11 AC: missing claude on PATH classifies HARD."""

    def fake_which(name: str) -> str | None:
        return None if name == "claude" else f"/usr/bin/{name}"

    monkeypatch.setattr(shutil, "which", fake_which)
    report = CapabilityGates().check_all()
    assert "binary.claude" in report.hard_failures
    # The other HARD binaries are still classified as passing.
    by_name = {row.name: row for row in report.report}
    assert by_name["binary.claude"].passed is False
    assert by_name["binary.claude"].failure_mode == "hard"
    assert by_name["binary.make"].passed is True
    assert by_name["binary.jq"].passed is True
    assert by_name["binary.git"].passed is True


def test_missing_mcp_server_classifies_soft_skip(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """T01.11 AC: missing MCP server classifies SOFT-SKIP under --no-mcp."""
    # All binaries present; no MCP server resolvable.
    def fake_which(name: str) -> str | None:
        if name in ("claude", "make", "jq", "git"):
            return f"/usr/bin/{name}"
        return None

    monkeypatch.setattr(shutil, "which", fake_which)
    report = CapabilityGates(skip_flags={"--no-mcp"}).check_all()
    # No HARD failures because the four HARD binaries resolved.
    assert report.hard_failures == ()
    # All MCP servers fall into soft_skips because (a) they aren't on
    # PATH, and (b) --no-mcp would also force them down.
    for name in (
        "mcp_server.auggie",
        "mcp_server.auggie-mcp",
        "mcp_server.airis-mcp-gateway",
    ):
        assert name in report.soft_skips
    # skip_flags propagate verbatim onto the report.
    assert report.skip_flags == ("--no-mcp",)


def test_no_mcp_flag_skips_even_when_servers_are_reachable() -> None:
    """``--no-mcp`` forces SOFT-SKIP even when probe would have passed."""
    gate = CapabilityGates(
        skip_flags={"--no-mcp"},
        capabilities=_mcp_only_specs(),
        mcp_probe=lambda name: (True, f"/opt/{name}"),
    )
    report = gate.check_all()
    # Every MCP server lands in soft_skips because the flag overrides
    # the would-be-passing probe.
    assert set(report.soft_skips) == {spec.name for spec in _mcp_only_specs()}
    # Each status row carries the override marker and the probe's detail
    # so doctor can render "would have passed at <path>, skipped by
    # --no-mcp".
    for row in report.report:
        assert row.skipped_by_flag is True
        assert row.passed is False
        assert row.detail.startswith("/opt/")


def test_mcp_server_reachable_default_uses_path_presence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OQ-5 M1 stub: PATH presence is the default reachability signal."""
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    passed, detail = CapabilityGates().mcp_server_reachable("auggie")
    assert passed is True
    assert detail == "/usr/bin/auggie"


def test_mcp_server_reachable_honours_injected_probe() -> None:
    """``mcp_probe`` keyword overrides the default PATH-presence probe."""
    calls: list[str] = []

    def custom_probe(name: str) -> tuple[bool, str]:
        calls.append(name)
        return False, "handshake timeout"

    gate = CapabilityGates(mcp_probe=custom_probe)
    passed, detail = gate.mcp_server_reachable("auggie")
    assert passed is False
    assert detail == "handshake timeout"
    assert calls == ["auggie"]


def test_capabilities_accessor_returns_capability_dataclasses() -> None:
    caps = CapabilityGates().capabilities()
    assert len(caps) == len(_DEFAULT_CAPABILITY_SPECS)
    for cap, spec in zip(caps, _DEFAULT_CAPABILITY_SPECS):
        assert isinstance(cap, Capability)
        assert cap.name == spec.name
        assert cap.failure_mode == spec.failure_mode
        assert cap.skip_flag == spec.skip_flag


def test_capability_check_closures_defer_to_gate_probes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Capability.check() reuses the gate's probe methods (no duplicate logic)."""
    monkeypatch.setattr(shutil, "which", lambda name: None)
    gate = CapabilityGates()
    by_name = {cap.name: cap for cap in gate.capabilities()}
    # Every default capability's probe should fail when PATH is empty.
    for name, cap in by_name.items():
        assert cap.check() is False, name


def test_check_all_report_status_rows_carry_descriptions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    report = CapabilityGates().check_all()
    by_name = {row.name: row for row in report.report}
    assert by_name["binary.claude"].description == "Claude CLI on PATH"
    assert by_name["mcp_server.auggie"].description == "Auggie MCP server reachable"


def test_xfail_capability_classifies_into_soft_xfails() -> None:
    """A custom spec table with an xfail capability lands in soft_xfails."""
    xfail_spec = _CapabilitySpec(
        name="binary.optional",
        target="definitely-not-on-path-xyz",
        kind="binary",
        failure_mode="xfail",
        skip_flag=None,
        description="Optional tool",
    )
    gate = CapabilityGates(capabilities=(xfail_spec,))
    report = gate.check_all()
    assert report.soft_xfails == ("binary.optional",)
    assert report.hard_failures == ()
    assert report.soft_skips == ()


def test_unknown_capability_kind_is_rejected_at_check_time() -> None:
    bad_spec = _CapabilitySpec(
        name="weird.thing",
        target="nope",
        kind="binary",  # placeholder; we'll mutate below via dataclasses.replace
        failure_mode="hard",
        skip_flag=None,
        description="",
    )
    # _CapabilitySpec is frozen, but Python doesn't enforce the Literal at
    # runtime; we construct one with an unexpected kind via object.__setattr__
    # to simulate a downstream typo.
    object.__setattr__(bad_spec, "kind", "unknown")
    gate = CapabilityGates(capabilities=(bad_spec,))
    with pytest.raises(ValueError, match="unknown capability kind"):
        gate.check_all()


def test_skip_flags_are_emitted_sorted_and_deduplicated() -> None:
    gate = CapabilityGates(skip_flags=["--no-mcp", "--no-mcp", "--zzz"])
    assert gate.skip_flags == ("--no-mcp", "--zzz")


def test_status_rows_for_passing_binaries_have_no_skipped_by_flag(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    report = CapabilityGates().check_all()
    for row in report.report:
        # No HARD binary carries a skip_flag, so skipped_by_flag stays
        # False even if --no-mcp were passed (but we didn't pass it).
        if row.failure_mode == "hard":
            assert row.skipped_by_flag is False
