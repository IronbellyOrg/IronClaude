"""TEST-004 capability classification matrix (cliEval / Task T02.23 / D-0042).

This module is the **contract-layer readout** for the three-tier capability
gate matrix promised by design-spec §11 "Three tiers of gates":

* ``hard``   — host precondition; missing capability aborts the run via
  ``sys.exit(HARD_FAIL_EXIT_CODE)`` (= 2). Doctor checklist marker is
  ``[XX]`` with the trailing tag ``" (HARD)"``.
* ``skip``   — host nicety; missing capability marks gated evals as
  ``SKIPPED`` but does not abort. Doctor marker is ``[--]`` with tag
  ``" (SOFT-SKIP)"`` — or ``" (skipped by flag)"`` when the descriptor's
  ``skip_flag`` (e.g. ``--no-mcp``) is active.
* ``xfail``  — gated evals run as **expected-fail**; missing capability
  classifies into ``CapabilityReport.soft_xfails`` and the doctor marker
  is ``[??]`` with tag ``" (xfail)"``.

Coverage map (one slice per TEST-004 AC bullet):

* ``TestMissingClaudeHard``       — TEST-004 AC1: missing ``claude`` on
  PATH classifies HARD; ``CapabilityGates`` populates
  ``hard_failures``; doctor exits 2.
* ``TestNoMcpSoftSkip``           — TEST-004 AC2: ``--no-mcp`` flag
  soft-skips every MCP capability regardless of whether the probe
  would have passed (override semantics).
* ``TestXfailClassification``     — TEST-004 AC3: a custom ``xfail``
  spec materialises into ``soft_xfails`` and renders with the
  ``[??] ... (xfail)`` marker. The default roster has no ``xfail``
  rows today; the test injects one via the ``capabilities=`` hook so
  the classification surface stays exercised even without a
  production xfail entry.
* ``TestDoctorClassificationRendering`` — TEST-004 AC4: doctor stdout
  renders each classification's distinct status string so operators
  can visually distinguish the three tiers.
* ``test_test_004_slice_coverage_is_complete`` — meta-test that pins
  the four classification slices to the AC list so future drift in
  the matrix breaks the test first.

Companion modules (``test_capability_gates.py``,
``test_capability_dataclass.py``, ``test_capability_report.py``,
``test_doctor.py``) exercise the *components* the matrix is built from.
This module exists because the TEST-004 deliverable promises one
audit-friendly readout whose every test maps directly to a TEST-004
AC bullet — exactly the same shape as TEST-002 (D-0040) and TEST-003
(D-0041) use for the containment + symlink contracts.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.eval import commands as doctor_module
from superclaude.cli.eval.capabilities import (
    CapabilityGates,
    CapabilityReport,
    CapabilityStatus,
    _CapabilitySpec,
    _DEFAULT_CAPABILITY_SPECS,
)
from superclaude.cli.eval.commands import (
    HARD_FAIL_EXIT_CODE,
    build_doctor_report,
    eval_group,
    render_checklist,
    render_hard_failure_artifact,
)


# ---------------------------------------------------------------------------
# Shared fixtures: simulate hosts that exercise each classification cleanly.
# ---------------------------------------------------------------------------


@pytest.fixture
def clean_host(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    """Every HARD binary on PATH, ~/.claude/ extant, claude>=0.5.0."""

    claude_home = tmp_path / ".claude"
    claude_home.mkdir()
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: "claude 0.5.1",
    )
    return {"home": tmp_path, "claude_home": claude_home}


@pytest.fixture
def host_missing_claude(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    """Every HARD binary on PATH except ``claude``; ~/.claude/ extant."""

    claude_home = tmp_path / ".claude"
    claude_home.mkdir()

    def fake_which(name: str) -> str | None:
        return None if name == "claude" else f"/usr/bin/{name}"

    monkeypatch.setattr(shutil, "which", fake_which)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    # When the binary is absent the version probe cannot run either; mirror
    # that in the doctor probe so the two HARD rows agree on the failure.
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: None,
    )
    return {"home": tmp_path, "claude_home": claude_home}


def _mcp_only_specs() -> tuple[_CapabilitySpec, ...]:
    return tuple(spec for spec in _DEFAULT_CAPABILITY_SPECS if spec.kind == "mcp_server")


_DEFAULT_MCP_NAMES: frozenset[str] = frozenset(
    spec.name for spec in _DEFAULT_CAPABILITY_SPECS if spec.kind == "mcp_server"
)


# ---------------------------------------------------------------------------
# Slice 1 — TEST-004 AC1: missing claude → HARD
# ---------------------------------------------------------------------------


class TestMissingClaudeHard:
    """TEST-004 AC1: missing ``claude`` on PATH classifies HARD.

    Two layers verified together:

    * ``CapabilityGates.check_all()`` lands ``binary.claude`` in
      ``hard_failures`` (the raw classification).
    * ``superclaude eval doctor`` exits ``HARD_FAIL_EXIT_CODE`` and
      writes a HARD-failure artifact to ``stderr`` (the operator-facing
      contract).
    """

    def test_missing_claude_lands_in_hard_failures(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def fake_which(name: str) -> str | None:
            return None if name == "claude" else f"/usr/bin/{name}"

        monkeypatch.setattr(shutil, "which", fake_which)
        report = CapabilityGates().check_all()
        assert "binary.claude" in report.hard_failures
        assert report.soft_skips == ()
        assert report.soft_xfails == ()

    def test_missing_claude_row_carries_hard_failure_mode(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def fake_which(name: str) -> str | None:
            return None if name == "claude" else f"/usr/bin/{name}"

        monkeypatch.setattr(shutil, "which", fake_which)
        report = CapabilityGates().check_all()
        by_name = {row.name: row for row in report.report}
        row = by_name["binary.claude"]
        assert row.passed is False
        assert row.failure_mode == "hard"
        assert row.skipped_by_flag is False
        assert "not found" in row.detail.lower()

    def test_doctor_exits_two_when_claude_missing(
        self, host_missing_claude: dict
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(eval_group, ["doctor"])
        assert result.exit_code == HARD_FAIL_EXIT_CODE, result.output
        # HARD-failure artifact is on stderr per FR-CLI4 AC.
        assert "HARD failures" in result.stderr
        assert "binary.claude" in result.stderr

    def test_doctor_json_reports_hard_failure_on_missing_claude(
        self, host_missing_claude: dict
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(eval_group, ["doctor", "--json"])
        assert result.exit_code == HARD_FAIL_EXIT_CODE
        payload = json.loads(result.stdout)
        assert "binary.claude" in payload["hard_failures"]
        # Soft-skips remain unaffected by the HARD failure.
        assert "binary.claude" not in payload["soft_skips"]


# ---------------------------------------------------------------------------
# Slice 2 — TEST-004 AC2: --no-mcp soft-skips MCP evals
# ---------------------------------------------------------------------------


class TestNoMcpSoftSkip:
    """TEST-004 AC2: ``--no-mcp`` soft-skips MCP evals.

    The flag's contract is *override*, not *probe* — every MCP row lands
    in ``soft_skips`` whether the underlying probe would have passed or
    failed. The corresponding ``CapabilityStatus.skipped_by_flag`` bit is
    ``True`` so doctor can render the row distinctly from a probe-failure
    soft-skip.
    """

    def test_no_mcp_flag_skips_mcp_servers_even_when_probe_passes(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
        gate = CapabilityGates(
            skip_flags={"--no-mcp"},
            capabilities=_mcp_only_specs(),
            mcp_probe=lambda name: (True, f"/opt/{name}"),
        )
        report = gate.check_all()
        assert set(report.soft_skips) == {spec.name for spec in _mcp_only_specs()}
        assert report.hard_failures == ()
        for row in report.report:
            assert row.skipped_by_flag is True
            assert row.passed is False

    def test_no_mcp_flag_skips_mcp_servers_when_probe_fails(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # All HARD binaries resolve; no MCP server resolves either way.
        def fake_which(name: str) -> str | None:
            if name in ("claude", "make", "jq", "git"):
                return f"/usr/bin/{name}"
            return None

        monkeypatch.setattr(shutil, "which", fake_which)
        report = CapabilityGates(skip_flags={"--no-mcp"}).check_all()
        # HARD floor stays green.
        assert report.hard_failures == ()
        # Every MCP row routes through soft_skips (failed probe + flag both
        # contribute, but the bucket is the same).
        assert _DEFAULT_MCP_NAMES <= set(report.soft_skips)
        assert report.skip_flags == ("--no-mcp",)

    def test_no_mcp_flag_does_not_affect_hard_rows(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
        report = CapabilityGates(skip_flags={"--no-mcp"}).check_all()
        by_name = {row.name: row for row in report.report}
        # No HARD binary should be flagged as skipped_by_flag because the
        # descriptors don't declare a skip_flag for HARD rows.
        for hard_name in ("binary.claude", "binary.make", "binary.jq", "binary.git"):
            row = by_name[hard_name]
            assert row.failure_mode == "hard"
            assert row.skipped_by_flag is False

    def test_doctor_no_mcp_flag_lands_mcp_rows_in_soft_skips(
        self, clean_host: dict
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(eval_group, ["doctor", "--json", "--no-mcp"])
        assert result.exit_code == 0, result.output
        payload = json.loads(result.output)
        assert payload["skip_flags"] == ["--no-mcp"]
        soft_skips = set(payload["soft_skips"])
        assert _DEFAULT_MCP_NAMES <= soft_skips


# ---------------------------------------------------------------------------
# Slice 3 — TEST-004 AC3: XFAIL classification supported
# ---------------------------------------------------------------------------


class TestXfailClassification:
    """TEST-004 AC3: XFAIL classification supported.

    The default roster has no ``xfail`` rows today (every default spec is
    either ``hard`` or ``skip``), so this slice injects a custom
    ``_CapabilitySpec`` with ``failure_mode="xfail"`` via the
    ``capabilities=`` constructor hook. The matrix surface is the same one
    a future production ``xfail`` entry would land on, so wiring drift
    surfaces here first.
    """

    @staticmethod
    def _xfail_spec(*, missing: bool) -> _CapabilitySpec:
        return _CapabilitySpec(
            name="binary.optional-xfail",
            target=(
                "definitely-not-on-path-xfail"
                if missing
                else "ls"  # any binary that will be on PATH in CI
            ),
            kind="binary",
            failure_mode="xfail",
            skip_flag=None,
            description="Optional xfail probe",
        )

    def test_failing_xfail_capability_lands_in_soft_xfails(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # No binaries on PATH so the xfail target also fails.
        monkeypatch.setattr(shutil, "which", lambda name: None)
        gate = CapabilityGates(capabilities=(self._xfail_spec(missing=True),))
        report = gate.check_all()
        assert report.soft_xfails == ("binary.optional-xfail",)
        assert report.hard_failures == ()
        assert report.soft_skips == ()

    def test_xfail_row_carries_xfail_failure_mode_when_failing(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(shutil, "which", lambda name: None)
        gate = CapabilityGates(capabilities=(self._xfail_spec(missing=True),))
        report = gate.check_all()
        row = report.report[0]
        assert row.name == "binary.optional-xfail"
        assert row.failure_mode == "xfail"
        assert row.passed is False
        assert row.skipped_by_flag is False

    def test_passing_xfail_capability_does_not_land_in_failure_buckets(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
        gate = CapabilityGates(capabilities=(self._xfail_spec(missing=False),))
        report = gate.check_all()
        # Passing xfail rows do not contribute to any failure bucket.
        assert report.soft_xfails == ()
        assert report.hard_failures == ()
        assert report.soft_skips == ()
        assert report.report[0].passed is True
        assert report.report[0].failure_mode == "xfail"

    def test_xfail_status_serialises_through_capability_report(self) -> None:
        """``CapabilityReport.to_json`` round-trips an xfail row."""
        row = CapabilityStatus(
            name="binary.optional-xfail",
            passed=False,
            failure_mode="xfail",
            description="Optional xfail probe",
            detail="not found on PATH",
        )
        report = CapabilityReport(
            report=(row,),
            soft_xfails=("binary.optional-xfail",),
        )
        payload = report.to_json()
        assert payload["soft_xfails"] == ["binary.optional-xfail"]
        assert payload["report"][0]["failure_mode"] == "xfail"
        # The mapping is JSON-serialisable end-to-end.
        json.dumps(payload)


# ---------------------------------------------------------------------------
# Slice 4 — TEST-004 AC4: doctor renders the correct status string
# ---------------------------------------------------------------------------


def _make_report(rows: tuple[CapabilityStatus, ...]) -> CapabilityReport:
    """Build a CapabilityReport whose failure buckets agree with ``rows``."""
    hard: list[str] = []
    skip: list[str] = []
    xfail: list[str] = []
    for row in rows:
        if row.passed:
            continue
        if row.failure_mode == "hard":
            hard.append(row.name)
        elif row.failure_mode == "skip":
            skip.append(row.name)
        else:
            xfail.append(row.name)
    return CapabilityReport(
        report=rows,
        hard_failures=tuple(hard),
        soft_skips=tuple(skip),
        soft_xfails=tuple(xfail),
    )


class TestDoctorClassificationRendering:
    """TEST-004 AC4: doctor output renders distinct strings per class.

    Each classification has a unique marker glyph + trailing tag so
    operators reading the checklist can identify the tier without parsing
    JSON. The four-way matrix is:

    | classification              | marker | trailing tag             |
    |-----------------------------|--------|--------------------------|
    | passed                      | [ok]   | (none)                   |
    | failing HARD                | [XX]   | (HARD)                   |
    | failing SOFT-SKIP (probe)   | [--]   | (SOFT-SKIP)              |
    | failing SOFT-SKIP (--no-mcp)| [--]   | (skipped by flag)        |
    | failing XFAIL               | [??]   | (xfail)                  |
    """

    def test_renders_hard_failure_marker(self) -> None:
        row = CapabilityStatus(
            name="binary.claude",
            passed=False,
            failure_mode="hard",
            description="Claude CLI on PATH",
            detail="not found on PATH",
        )
        text = render_checklist(_make_report((row,)))
        assert "[XX] Claude CLI on PATH (HARD)" in text
        assert "not found on PATH" in text
        assert "HARD failures: binary.claude" in text

    def test_renders_soft_skip_probe_failure_marker(self) -> None:
        row = CapabilityStatus(
            name="mcp_server.auggie",
            passed=False,
            failure_mode="skip",
            description="Auggie MCP server reachable",
            detail="MCP server binary not on PATH",
        )
        text = render_checklist(_make_report((row,)))
        assert "[--] Auggie MCP server reachable (SOFT-SKIP)" in text
        # Soft-skip-only failures do not contribute to HARD failure tally.
        assert "HARD failures" not in text
        assert "all HARD capabilities satisfied" in text
        assert "soft skips: mcp_server.auggie" in text

    def test_renders_skipped_by_flag_marker_when_no_mcp_active(self) -> None:
        row = CapabilityStatus(
            name="mcp_server.auggie",
            passed=False,
            failure_mode="skip",
            description="Auggie MCP server reachable",
            detail="/opt/auggie",  # would have passed; flag forced down
            skipped_by_flag=True,
        )
        report = CapabilityReport(
            report=(row,),
            skip_flags=("--no-mcp",),
            soft_skips=("mcp_server.auggie",),
        )
        text = render_checklist(report)
        assert "[--] Auggie MCP server reachable (skipped by flag)" in text
        assert "skip flags: --no-mcp" in text
        # SOFT-SKIP tag must NOT appear when the override marker is present.
        assert "(SOFT-SKIP)" not in text

    def test_renders_xfail_marker(self) -> None:
        row = CapabilityStatus(
            name="binary.optional-xfail",
            passed=False,
            failure_mode="xfail",
            description="Optional xfail probe",
            detail="not found on PATH",
        )
        text = render_checklist(_make_report((row,)))
        assert "[??] Optional xfail probe (xfail)" in text
        # xfail is not HARD; the green-checklist line stays positive.
        assert "all HARD capabilities satisfied" in text

    def test_renders_passing_row_with_ok_marker(self) -> None:
        row = CapabilityStatus(
            name="binary.claude",
            passed=True,
            failure_mode="hard",
            description="Claude CLI on PATH",
            detail="/usr/bin/claude",
        )
        text = render_checklist(_make_report((row,)))
        assert "[ok] Claude CLI on PATH" in text
        # No trailing tag for passing rows.
        assert "[ok] Claude CLI on PATH (HARD)" not in text
        assert "[ok] Claude CLI on PATH (SOFT-SKIP)" not in text

    def test_hard_failure_artifact_names_offending_capability(self) -> None:
        row = CapabilityStatus(
            name="binary.claude",
            passed=False,
            failure_mode="hard",
            description="Claude CLI on PATH",
            detail="not found on PATH",
        )
        text = render_hard_failure_artifact(_make_report((row,)))
        assert "HARD failures" in text
        assert "binary.claude" in text
        assert "Claude CLI on PATH" in text
        assert "not found on PATH" in text

    def test_doctor_cli_emits_distinct_strings_for_each_classification(
        self, clean_host: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """End-to-end: doctor stdout contains the three SOFT-tier markers.

        Forces every MCP probe to fail (so SOFT-SKIP markers fire) and
        also activates ``--no-mcp`` so the override-marker variant
        renders alongside. ``vendored.ptytest`` is a SOFT-SKIP doctor row
        until M2 vendoring lands (T02.01); we pin both variants here so
        the matrix surface stays visible regardless of which MCP probe
        the run picked.
        """

        # Keep HARD binaries on PATH, but strip MCP binaries so the probe
        # falls into the failed-probe branch.
        def fake_which(name: str) -> str | None:
            if name in ("claude", "make", "jq", "git"):
                return f"/usr/bin/{name}"
            return None

        monkeypatch.setattr(shutil, "which", fake_which)
        runner = CliRunner()
        result = runner.invoke(eval_group, ["doctor"])
        assert result.exit_code == 0, result.output
        # Probe-failure SOFT-SKIP rendering visible somewhere in the output.
        assert "(SOFT-SKIP)" in result.output
        assert "all HARD capabilities satisfied" in result.output

        # Re-run with --no-mcp so the same MCP rows render with the
        # override marker instead.
        result_flag = runner.invoke(eval_group, ["doctor", "--no-mcp"])
        assert result_flag.exit_code == 0, result_flag.output
        assert "(skipped by flag)" in result_flag.output
        assert "skip flags: --no-mcp" in result_flag.output


# ---------------------------------------------------------------------------
# Coverage pin — every TEST-004 AC bullet maps to a test class above.
# ---------------------------------------------------------------------------


def test_test_004_slice_coverage_is_complete() -> None:
    """Meta-test: every TEST-004 AC bullet has at least one test class.

    Mirrors the coverage-pin pattern from D-0040 (TEST-002) and D-0041
    (TEST-003) so a future AC addition either lands with a test class or
    breaks this assertion before merge.
    """
    expected_slices = {
        "AC1 missing claude HARD": "TestMissingClaudeHard",
        "AC2 --no-mcp soft-skip": "TestNoMcpSoftSkip",
        "AC3 xfail supported": "TestXfailClassification",
        "AC4 doctor renders status string": "TestDoctorClassificationRendering",
    }
    module = globals()
    for ac, cls_name in expected_slices.items():
        assert cls_name in module, f"missing slice for {ac}: {cls_name}"
        cls = module[cls_name]
        assert isinstance(cls, type), f"{cls_name} is not a class"
        # Each slice has at least one test_ method.
        test_methods = [
            name for name in dir(cls) if name.startswith("test_")
        ]
        assert test_methods, f"{cls_name} has no test methods"
