"""Tests for ``superclaude eval doctor`` (FR-CLI4 / Task T01.13 / D-0011).

Covers the four acceptance criteria from the phase tasklist:

1. ``superclaude eval doctor`` exits 0 on a clean dev machine with
   claude>=0.5.0, jq, make, git present and ``~/.claude/`` extant.
2. ``superclaude eval doctor --json`` emits a deterministic JSON payload
   matching the :class:`CapabilityReport` contract (extended with the
   three doctor-specific rows and a ``coverage_gate`` marker).
3. Doctor fails closed (exit 2) when any HARD capability is missing;
   stderr carries a HARD-failure artifact identifying every offending
   capability.
4. Module exports ``build_doctor_report`` / ``eval_group`` for downstream
   consumers (CLI wiring + integration tests).

The doctor probes (``shutil.which`` for binaries, ``claude --version``,
``~/.claude/``, vendored ptytest path) are all injectable so the tests do
not depend on the runtime host configuration.
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
)
from superclaude.cli.eval.commands import (
    HARD_FAIL_EXIT_CODE,
    NON_LINUX_REFUSAL_TEMPLATE,
    PARALLEL_RAM_GATE_THRESHOLD,
    RAM_CEILING_BYTES,
    RAM_CEILING_TEXT,
    _check_claude_home,
    _check_claude_version,
    _check_free_ram_for_parallel,
    _check_ptytest_vendored,
    _default_free_ram_probe,
    build_doctor_report,
    doctor_payload,
    eval_group,
    render_checklist,
    render_hard_failure_artifact,
)


@pytest.fixture
def clean_host(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    """Simulate a clean dev machine: every binary on PATH, ~/.claude/ extant."""

    claude_home = tmp_path / ".claude"
    claude_home.mkdir()

    def fake_which(name: str) -> str:
        return f"/usr/bin/{name}"

    monkeypatch.setattr(shutil, "which", fake_which)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: "claude 0.5.1",
    )
    return {"home": tmp_path, "claude_home": claude_home}


# ---------------------------------------------------------------------------
# Helper-level checks (unit tests for the supplementary capability probes)
# ---------------------------------------------------------------------------


def test_version_probe_passes_on_supported_release() -> None:
    status = _check_claude_version(probe=lambda: "claude 0.5.0")
    assert status.passed is True
    assert status.failure_mode == "hard"
    assert "0.5.0" in status.detail


def test_version_probe_passes_on_higher_release() -> None:
    status = _check_claude_version(probe=lambda: "claude 0.7.3 (build 12)")
    assert status.passed is True
    assert "0.7.3" in status.detail


def test_version_probe_fails_below_min() -> None:
    status = _check_claude_version(probe=lambda: "claude 0.4.9")
    assert status.passed is False
    assert "< required 0.5.0" in status.detail


def test_version_probe_fails_when_unparseable() -> None:
    status = _check_claude_version(probe=lambda: "unrecognised banner")
    assert status.passed is False
    assert "could not parse" in status.detail


def test_version_probe_fails_when_callable_returns_none() -> None:
    status = _check_claude_version(probe=lambda: None)
    assert status.passed is False
    assert "not callable" in status.detail


def test_version_probe_catches_callable_exception() -> None:
    def boom() -> str:
        raise RuntimeError("subprocess died")

    status = _check_claude_version(probe=boom)
    assert status.passed is False
    assert "RuntimeError" in status.detail


def test_claude_home_passes_when_directory_exists(tmp_path: Path) -> None:
    home = tmp_path / ".claude"
    home.mkdir()
    status = _check_claude_home(home=home)
    assert status.passed is True
    assert status.detail == str(home)


def test_claude_home_fails_when_missing(tmp_path: Path) -> None:
    missing = tmp_path / "absent"
    status = _check_claude_home(home=missing)
    assert status.passed is False
    assert "not found" in status.detail


def test_ptytest_vendored_passes_when_init_present(tmp_path: Path) -> None:
    pty = tmp_path / "pty"
    pty.mkdir()
    (pty / "__init__.py").write_text("")
    status = _check_ptytest_vendored(pty_dir=pty)
    assert status.passed is True
    assert status.failure_mode == "skip"  # SOFT-SKIP regardless


def test_ptytest_vendored_soft_skips_when_absent(tmp_path: Path) -> None:
    status = _check_ptytest_vendored(pty_dir=tmp_path / "missing-pty")
    assert status.passed is False
    assert status.failure_mode == "skip"


# ---------------------------------------------------------------------------
# build_doctor_report contract
# ---------------------------------------------------------------------------


def test_build_doctor_report_appends_three_supplementary_rows(clean_host: dict) -> None:
    report = build_doctor_report()
    names = [row.name for row in report.report]
    # Last three rows must be the doctor-specific checks in this order.
    assert names[-3:] == [
        "claude.min_version",
        "filesystem.claude_home",
        "vendored.ptytest",
    ]


def test_build_doctor_report_clean_host_has_no_hard_failures(clean_host: dict) -> None:
    report = build_doctor_report()
    assert report.hard_failures == ()
    # ptytest is not vendored at M1; it lands in soft_skips.
    assert "vendored.ptytest" in report.soft_skips


def test_build_doctor_report_missing_claude_binary_is_hard(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    claude_home = tmp_path / ".claude"
    claude_home.mkdir()

    def fake_which(name: str) -> str | None:
        return None if name == "claude" else f"/usr/bin/{name}"

    monkeypatch.setattr(shutil, "which", fake_which)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: None,
    )
    report = build_doctor_report()
    assert "binary.claude" in report.hard_failures
    assert "claude.min_version" in report.hard_failures


def test_build_doctor_report_missing_claude_home_is_hard(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: "claude 0.5.2",
    )
    report = build_doctor_report()
    assert "filesystem.claude_home" in report.hard_failures


def test_build_doctor_report_below_min_version_is_hard(clean_host: dict, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: "claude 0.4.9",
    )
    report = build_doctor_report()
    assert "claude.min_version" in report.hard_failures


def test_build_doctor_report_no_mcp_flag_forces_soft_skip(clean_host: dict) -> None:
    """--no-mcp populates skip_flags + every MCP row lands in soft_skips."""
    report = build_doctor_report(skip_flags={"--no-mcp"})
    assert "--no-mcp" in report.skip_flags
    for name in (
        "mcp_server.auggie",
        "mcp_server.auggie-mcp",
        "mcp_server.airis-mcp-gateway",
    ):
        assert name in report.soft_skips


def test_build_doctor_report_accepts_gate_override() -> None:
    """Tests can supply a preconfigured gate to control the base roster."""
    fake_status = CapabilityStatus(
        name="binary.claude",
        passed=True,
        failure_mode="hard",
        description="Claude CLI on PATH",
        detail="/opt/claude",
    )
    fake_report = CapabilityReport(report=(fake_status,))

    class _StubGate(CapabilityGates):
        def check_all(self) -> CapabilityReport:  # type: ignore[override]
            return fake_report

    report = build_doctor_report(
        gates=_StubGate(),
        claude_version_probe=lambda: "claude 0.5.0",
        claude_home=Path("/nonexistent"),  # forces HARD on claude_home
        pty_dir=Path("/nonexistent-pty"),
    )
    assert report.report[0] == fake_status
    assert "filesystem.claude_home" in report.hard_failures


# ---------------------------------------------------------------------------
# CLI integration via Click's CliRunner
# ---------------------------------------------------------------------------


def test_cli_doctor_exits_zero_on_clean_host(clean_host: dict) -> None:
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor"])
    assert result.exit_code == 0, result.output
    assert "superclaude eval doctor:" in result.output
    assert "all HARD capabilities satisfied" in result.output


def test_cli_doctor_json_payload_matches_report_contract(clean_host: dict) -> None:
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    # Base CapabilityReport keys must remain intact.
    for key in (
        "report",
        "blocked_evals",
        "skip_flags",
        "hard_failures",
        "soft_skips",
        "soft_xfails",
    ):
        assert key in payload
    # Doctor-specific extension marker (T04.14: deferred → skipped/passed/failed).
    assert payload["coverage_gate"] == {
        "requested": False,
        "status": "skipped",
    }
    # Last three rows are the doctor-specific checks.
    names = [row["name"] for row in payload["report"]]
    assert names[-3:] == [
        "claude.min_version",
        "filesystem.claude_home",
        "vendored.ptytest",
    ]


def test_cli_doctor_json_is_deterministic_across_invocations(clean_host: dict) -> None:
    runner = CliRunner()
    first = runner.invoke(eval_group, ["doctor", "--json"]).output
    second = runner.invoke(eval_group, ["doctor", "--json"]).output
    assert first == second


def test_cli_doctor_exits_two_when_hard_capability_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def fake_which(name: str) -> str | None:
        return None if name == "jq" else f"/usr/bin/{name}"

    monkeypatch.setattr(shutil, "which", fake_which)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    (tmp_path / ".claude").mkdir()
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: "claude 0.5.0",
    )
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor"])
    assert result.exit_code == HARD_FAIL_EXIT_CODE
    # HARD-failure artifact lands on stderr identifying the missing capability.
    assert "HARD failures" in result.stderr
    assert "binary.jq" in result.stderr


def test_cli_doctor_json_exit_two_includes_hard_failures_in_payload(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def fake_which(name: str) -> str | None:
        return None if name == "claude" else f"/usr/bin/{name}"

    monkeypatch.setattr(shutil, "which", fake_which)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    (tmp_path / ".claude").mkdir()
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: None,
    )
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--json"])
    assert result.exit_code == HARD_FAIL_EXIT_CODE
    payload = json.loads(result.stdout)
    assert "binary.claude" in payload["hard_failures"]
    assert "claude.min_version" in payload["hard_failures"]


def test_cli_doctor_no_mcp_flag_propagates_to_skip_flags(clean_host: dict) -> None:
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--json", "--no-mcp"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["skip_flags"] == ["--no-mcp"]
    soft_skips = set(payload["soft_skips"])
    assert {
        "mcp_server.auggie",
        "mcp_server.auggie-mcp",
        "mcp_server.airis-mcp-gateway",
    } <= soft_skips


# ---------------------------------------------------------------------------
# AC1 / R-109 / T06.07 — Linux-only platform refusal
# ---------------------------------------------------------------------------


def test_cli_doctor_refuses_non_linux_with_friendly_message(
    clean_host: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    """macOS (or any non-Linux ``platform.system()`` value) exits 2 with a
    single AC1-citing stderr line and never reaches the capability gates.
    """
    monkeypatch.setattr(doctor_module, "_default_platform_probe", lambda: "Darwin")
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor"])
    assert result.exit_code == HARD_FAIL_EXIT_CODE
    assert "unsupported platform: 'Darwin'" in result.stderr
    assert "Linux-only for v1" in result.stderr
    assert "AC1" in result.stderr
    assert "DOC-OQ9" in result.stderr
    # Capability checklist never rendered — the refusal short-circuits.
    assert "superclaude eval doctor:" not in result.stdout


def test_cli_doctor_refuses_windows_platform(
    clean_host: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Windows is rejected on the same code path as macOS."""
    monkeypatch.setattr(doctor_module, "_default_platform_probe", lambda: "Windows")
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--json"])
    assert result.exit_code == HARD_FAIL_EXIT_CODE
    assert "unsupported platform: 'Windows'" in result.stderr
    # --json must NOT emit a payload when the precheck fails — the
    # refusal lands on stderr only so a downstream pipe sees no JSON.
    assert result.stdout == ""


def test_cli_doctor_linux_platform_proceeds(clean_host: dict) -> None:
    """On Linux the precheck is a no-op and the existing happy path runs."""
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor"])
    assert result.exit_code == 0, result.output
    assert "superclaude eval doctor:" in result.output


def test_non_linux_refusal_template_cites_ac1_and_doc_oq9() -> None:
    """The friendly error string MUST name AC1 + DOC-OQ9 so an operator
    landing on it can trace the v1 platform commitment to the ADR log
    without a documentation hunt.
    """
    rendered = NON_LINUX_REFUSAL_TEMPLATE.format(system="Darwin")
    assert "AC1" in rendered
    assert "R-109" in rendered
    assert "DOC-OQ9" in rendered
    assert "decisions.md" in rendered


def test_cli_doctor_check_coverage_flag_is_accepted(clean_host: dict) -> None:
    """--check-coverage on a clean host (no settings.json) passes the gate."""
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--check-coverage"])
    assert result.exit_code == 0
    assert "coverage gate" in result.output


def test_cli_doctor_check_coverage_marker_emitted_in_json(clean_host: dict) -> None:
    """T04.14: marker carries the structured CoverageResult payload."""
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--json", "--check-coverage"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["coverage_gate"]["requested"] is True
    # Clean host has no settings.json under monkeypatched home, so the
    # gate reports an empty matcher set and passes.
    assert payload["coverage_gate"]["status"] == "passed"
    assert payload["coverage_gate"]["result"]["passed"] is True
    assert payload["coverage_gate"]["result"]["matchers"] == []


# ---------------------------------------------------------------------------
# Render helpers
# ---------------------------------------------------------------------------


def test_render_checklist_lists_every_row(clean_host: dict) -> None:
    report = build_doctor_report()
    text = render_checklist(report)
    for row in report.report:
        assert row.description in text


def test_render_hard_failure_artifact_lists_each_failure() -> None:
    bad_row = CapabilityStatus(
        name="binary.jq",
        passed=False,
        failure_mode="hard",
        description="jq JSON processor on PATH",
        detail="not found on PATH",
    )
    report = CapabilityReport(
        report=(bad_row,),
        hard_failures=("binary.jq",),
    )
    text = render_hard_failure_artifact(report)
    assert "HARD failures" in text
    assert "binary.jq" in text
    assert "not found on PATH" in text


# ---------------------------------------------------------------------------
# NFR-PERF2 free-RAM precheck (T03.17 / D-0059)
# ---------------------------------------------------------------------------


def test_free_ram_check_returns_none_below_threshold() -> None:
    """Gate stays silent when ``--parallel`` < 15 (the documented ceiling)."""
    status = _check_free_ram_for_parallel(
        requested_parallel=8,
        probe=lambda: 0,  # would otherwise be insufficient
    )
    assert status is None


def test_free_ram_check_returns_none_when_parallel_not_supplied() -> None:
    """Operator did not declare ``--parallel`` — no precheck fires."""
    assert _check_free_ram_for_parallel(requested_parallel=None) is None


def test_free_ram_check_passes_when_budget_met() -> None:
    """Probe reporting >= 2.25 GB free yields a PASS SOFT-SKIP row."""
    status = _check_free_ram_for_parallel(
        requested_parallel=PARALLEL_RAM_GATE_THRESHOLD,
        probe=lambda: 4 * (1024**3),  # 4 GB free
    )
    assert status is not None
    assert status.passed is True
    assert status.failure_mode == "skip"
    assert RAM_CEILING_TEXT in status.detail
    assert status.name == "host.free_ram_for_max_parallel"


def test_free_ram_check_warns_when_budget_short() -> None:
    """Insufficient free RAM yields a SOFT-SKIP row whose detail names 2.25 GB."""
    status = _check_free_ram_for_parallel(
        requested_parallel=PARALLEL_RAM_GATE_THRESHOLD,
        probe=lambda: 1 * (1024**3),  # 1 GB free << 2.25 GB
    )
    assert status is not None
    assert status.passed is False
    assert status.failure_mode == "skip"
    # The AC pins the literal token; refusing to assert on it would
    # let a rewording that drops the units slip past the test.
    assert RAM_CEILING_TEXT in status.detail


def test_free_ram_check_warns_when_probe_returns_none() -> None:
    """Probe unavailability counts as 'cannot certify' — record SOFT-SKIP."""
    status = _check_free_ram_for_parallel(
        requested_parallel=PARALLEL_RAM_GATE_THRESHOLD,
        probe=lambda: None,
    )
    assert status is not None
    assert status.passed is False
    assert RAM_CEILING_TEXT in status.detail


def test_free_ram_check_handles_probe_exception() -> None:
    """A crashing probe must not crash the doctor; SOFT-SKIP with detail."""

    def boom() -> int:
        raise RuntimeError("meminfo unreadable")

    status = _check_free_ram_for_parallel(
        requested_parallel=PARALLEL_RAM_GATE_THRESHOLD,
        probe=boom,
    )
    assert status is not None
    assert status.passed is False
    assert "RuntimeError" in status.detail
    assert RAM_CEILING_TEXT in status.detail


def test_free_ram_check_fires_at_threshold_minus_one_pass(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Threshold uses ``>=`` so parallel=15 fires; parallel=14 does not."""
    assert (
        _check_free_ram_for_parallel(requested_parallel=14, probe=lambda: 0)
        is None
    )
    fired = _check_free_ram_for_parallel(
        requested_parallel=15, probe=lambda: 0
    )
    assert fired is not None


def test_default_free_ram_probe_returns_positive_or_none() -> None:
    """The default Linux probe never raises; on non-Linux it returns None.

    Running the test on a dev host where ``/proc/meminfo`` exists should
    yield a positive integer; on a sandbox without procfs the probe
    returns ``None``. Either is contractually acceptable — we only assert
    it does not raise and returns the documented shapes.
    """
    value = _default_free_ram_probe()
    assert value is None or (isinstance(value, int) and value > 0)


def test_build_doctor_report_appends_ram_row_when_parallel_15(
    clean_host: dict,
) -> None:
    """At ``--parallel 15`` the NFR-PERF2 row is appended last."""
    report = build_doctor_report(
        requested_parallel=15,
        free_ram_probe=lambda: 4 * (1024**3),
    )
    names = [row.name for row in report.report]
    assert names[-1] == "host.free_ram_for_max_parallel"


def test_build_doctor_report_omits_ram_row_below_threshold(
    clean_host: dict,
) -> None:
    """At ``--parallel 8`` the NFR-PERF2 row is not appended."""
    report = build_doctor_report(
        requested_parallel=8,
        free_ram_probe=lambda: 0,
    )
    names = [row.name for row in report.report]
    assert "host.free_ram_for_max_parallel" not in names


def test_build_doctor_report_records_ram_short_as_soft_skip(
    clean_host: dict,
) -> None:
    """A short-RAM report classifies the row under ``soft_skips``."""
    report = build_doctor_report(
        requested_parallel=15,
        free_ram_probe=lambda: 1 * (1024**3),
    )
    assert "host.free_ram_for_max_parallel" in report.soft_skips
    # Doctor still exits 0 (no hard_failures from the new row).
    assert "host.free_ram_for_max_parallel" not in report.hard_failures


def test_cli_doctor_parallel_15_low_ram_emits_2_25_gb_warning(
    clean_host: dict,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The CLI surface emits the literal '2.25 GB' token on a tight host."""
    monkeypatch.setattr(
        "superclaude.cli.eval.commands._default_free_ram_probe",
        lambda: 1 * (1024**3),
    )
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--parallel", "15"])
    # SOFT-SKIP, not HARD: doctor still exits 0 so legitimate runs on
    # tight hosts are not blocked.
    assert result.exit_code == 0, result.output
    assert RAM_CEILING_TEXT in result.stderr
    assert "NFR-PERF2 warning" in result.stderr


def test_cli_doctor_parallel_15_with_ample_ram_does_not_warn(
    clean_host: dict,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ample free RAM keeps the warning silent (row present but passed)."""
    monkeypatch.setattr(
        "superclaude.cli.eval.commands._default_free_ram_probe",
        lambda: 8 * (1024**3),
    )
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--parallel", "15"])
    assert result.exit_code == 0
    assert "NFR-PERF2 warning" not in result.stderr


def test_cli_doctor_parallel_8_does_not_run_ram_check(
    clean_host: dict,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """At ``--parallel 8`` the doctor does not consult the probe at all."""
    calls: list[int] = []

    def counting_probe() -> int:
        calls.append(1)
        return 0

    monkeypatch.setattr(
        "superclaude.cli.eval.commands._default_free_ram_probe",
        counting_probe,
    )
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--parallel", "8"])
    assert result.exit_code == 0
    assert RAM_CEILING_TEXT not in result.stderr
    assert calls == []  # probe never consulted


def test_cli_doctor_json_payload_records_ram_short_row(
    clean_host: dict,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``--json --parallel 15`` keeps the SOFT-SKIP row in the payload."""
    monkeypatch.setattr(
        "superclaude.cli.eval.commands._default_free_ram_probe",
        lambda: 1 * (1024**3),
    )
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--json", "--parallel", "15"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert "host.free_ram_for_max_parallel" in payload["soft_skips"]
    # The warning still lands on stderr alongside the JSON payload.
    assert RAM_CEILING_TEXT in result.stderr


def test_ram_ceiling_bytes_matches_text() -> None:
    """The byte and text views of the ceiling cannot drift."""
    assert RAM_CEILING_BYTES == int(2.25 * (1024**3))
    assert RAM_CEILING_TEXT == "2.25 GB"


def test_doctor_payload_extends_capability_report_contract() -> None:
    base = CapabilityReport()
    payload = doctor_payload(base, check_coverage=False)
    for key in (
        "report",
        "blocked_evals",
        "skip_flags",
        "hard_failures",
        "soft_skips",
        "soft_xfails",
        "coverage_gate",
    ):
        assert key in payload
    assert payload["coverage_gate"]["requested"] is False
    # No --check-coverage → gate is "skipped" (status string fixed by
    # T04.14; the deferred marker from M2 was retired when the gate
    # landed).
    assert payload["coverage_gate"]["status"] == "skipped"
