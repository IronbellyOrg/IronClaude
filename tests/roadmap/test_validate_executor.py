"""Integration tests for validate_executor -- known-good and known-bad scenarios.

Uses mock step runners (no real subprocesses) to verify:
- Single-agent: known-good input produces report with blocking_count == 0
- Single-agent: known-bad input produces report with blocking_count > 0
- Multi-agent: partial failure produces degraded report
- Missing input files raise FileNotFoundError

C06 characterization (cleanup-debt item 2.11): a two-facade helper matrix over
``_embed_inputs`` / ``_sanitize_output`` in BOTH ``superclaude.cli.tasklist.executor``
and ``superclaude.cli.roadmap.validate_executor`` (G3.1-G3.18), plus REAL
``validate_run_step`` cases with a fake caller-local ``ClaudeProcess``
(dry_run=False, isolated tmp files, no real subprocess).
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import pytest

from superclaude.cli.pipeline.models import (
    PipelineConfig,
    Step,
    StepResult,
    StepStatus,
)
from superclaude.cli.roadmap import executor as main_roadmap_executor
from superclaude.cli.roadmap import tool_writer, validate_executor
from superclaude.cli.roadmap.models import AgentSpec, ValidateConfig
from superclaude.cli.roadmap.validate_executor import (
    _parse_report_counts,
    _write_degraded_report,
    execute_validate,
)
from superclaude.cli.tasklist import executor as tasklist_executor


def _now():
    return datetime.now(timezone.utc)


def _make_pipeline_outputs(output_dir: Path) -> None:
    """Write the 3 required input files that the validator reads."""
    (output_dir / "roadmap.md").write_text(
        "---\ntitle: Test Roadmap\n---\n## M1\n- D-001: deliverable\n",
        encoding="utf-8",
    )
    (output_dir / "test-strategy.md").write_text(
        "---\ntitle: Test Strategy\n---\n## M1 Tests\n- T-001: test\n",
        encoding="utf-8",
    )
    (output_dir / "extraction.md").write_text(
        "---\ntitle: Extraction\n---\n## Requirements\n- R-001: requirement\n",
        encoding="utf-8",
    )


def _make_validate_config(
    output_dir: Path,
    agent_count: int = 1,
) -> ValidateConfig:
    """Create a ValidateConfig for testing."""
    agents = [AgentSpec("opus", "architect")]
    if agent_count > 1:
        agents.append(AgentSpec("haiku", "architect"))
    return ValidateConfig(
        output_dir=output_dir,
        agents=agents,
        dry_run=True,  # Use dry_run to avoid real subprocess calls
    )


def _known_good_report() -> str:
    """Report content with 0 blocking issues."""
    lines = [
        "---",
        "blocking_issues_count: 0",
        "warnings_count: 2",
        "tasklist_ready: true",
        "---",
        "",
        "## Findings",
        "",
        "- **[WARNING]** Interleave: ratio at lower bound",
        "  - Location: roadmap.md:section M3",
        "  - Evidence: ratio = 0.15",
        "  - Fix: distribute test activities",
        "",
        "- **[WARNING]** Decomposition: compound deliverable",
        "  - Location: roadmap.md:D-003",
        "  - Evidence: 'implement and test' joined",
        "  - Fix: split into separate deliverables",
        "",
        "- **[INFO]** Schema: all fields present",
        "  - Location: roadmap.md:frontmatter",
        "",
        "## Summary",
        "",
        "0 blocking, 2 warnings, 1 info.",
    ]
    # Pad to meet min_lines
    for i in range(10):
        lines.append(f"- Additional detail line {i}")
    return "\n".join(lines)


def _known_bad_report() -> str:
    """Report content with blocking issues."""
    lines = [
        "---",
        "blocking_issues_count: 3",
        "warnings_count: 1",
        "tasklist_ready: false",
        "---",
        "",
        "## Findings",
        "",
        "- **[BLOCKING]** Schema: missing milestone_count field",
        "  - Location: roadmap.md:frontmatter",
        "  - Evidence: field absent",
        "  - Fix: add milestone_count to frontmatter",
        "",
        "- **[BLOCKING]** Structure: DAG cycle detected",
        "  - Location: roadmap.md:M2->M1",
        "  - Evidence: M2 depends on M1, M1 depends on M2",
        "  - Fix: remove circular dependency",
        "",
        "- **[BLOCKING]** Traceability: untraced requirement R-005",
        "  - Location: extraction.md:R-005",
        "  - Evidence: no deliverable maps to R-005",
        "  - Fix: add deliverable for R-005",
        "",
        "- **[WARNING]** Decomposition: compound deliverable",
        "  - Location: roadmap.md:D-002",
        "  - Evidence: multiple outputs",
        "  - Fix: split deliverable",
        "",
        "## Summary",
        "",
        "3 blocking, 1 warning, 0 info.",
    ]
    for i in range(10):
        lines.append(f"- Additional detail line {i}")
    return "\n".join(lines)


class TestExecuteValidateKnownGood:
    """Known-good input: validation report produced, blocking_count == 0."""

    def test_known_good_single_agent(self, tmp_path, monkeypatch):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        _make_pipeline_outputs(output_dir)
        config = _make_validate_config(output_dir, agent_count=1)

        # Mock execute_pipeline to write a known-good report
        def mock_execute_pipeline(steps, config, run_step, **kwargs):
            validate_dir = output_dir / "validate"
            validate_dir.mkdir(parents=True, exist_ok=True)
            report = validate_dir / "validation-report.md"
            report.write_text(_known_good_report(), encoding="utf-8")
            return [
                StepResult(
                    step=steps[0],
                    status=StepStatus.PASS,
                    attempt=1,
                    started_at=_now(),
                    finished_at=_now(),
                )
            ]

        monkeypatch.setattr(
            "superclaude.cli.roadmap.validate_executor.execute_pipeline",
            mock_execute_pipeline,
        )

        result = execute_validate(config)

        assert result["blocking_count"] == 0
        assert result["warning_count"] == 2
        assert result["info_count"] == 1
        assert (output_dir / "validate" / "validation-report.md").exists()


class TestExecuteValidateKnownBad:
    """Known-bad input: blocking issues detected, blocking_count > 0."""

    def test_known_bad_single_agent(self, tmp_path, monkeypatch):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        _make_pipeline_outputs(output_dir)
        config = _make_validate_config(output_dir, agent_count=1)

        def mock_execute_pipeline(steps, config, run_step, **kwargs):
            validate_dir = output_dir / "validate"
            validate_dir.mkdir(parents=True, exist_ok=True)
            report = validate_dir / "validation-report.md"
            report.write_text(_known_bad_report(), encoding="utf-8")
            return [
                StepResult(
                    step=steps[0],
                    status=StepStatus.PASS,
                    attempt=1,
                    started_at=_now(),
                    finished_at=_now(),
                )
            ]

        monkeypatch.setattr(
            "superclaude.cli.roadmap.validate_executor.execute_pipeline",
            mock_execute_pipeline,
        )

        result = execute_validate(config)

        assert result["blocking_count"] == 3
        assert result["warning_count"] == 1
        assert result["blocking_count"] > 0


class TestExecuteValidateMissingInputs:
    """Missing input files raise FileNotFoundError."""

    def test_missing_roadmap(self, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        # Only write 2 of 3 required files
        (output_dir / "test-strategy.md").write_text("content")
        (output_dir / "extraction.md").write_text("content")
        config = _make_validate_config(output_dir)

        with pytest.raises(FileNotFoundError, match="roadmap.md"):
            execute_validate(config)

    def test_missing_test_strategy(self, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        (output_dir / "roadmap.md").write_text("content")
        (output_dir / "extraction.md").write_text("content")
        config = _make_validate_config(output_dir)

        with pytest.raises(FileNotFoundError, match="test-strategy.md"):
            execute_validate(config)

    def test_missing_extraction(self, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        (output_dir / "roadmap.md").write_text("content")
        (output_dir / "test-strategy.md").write_text("content")
        config = _make_validate_config(output_dir)

        with pytest.raises(FileNotFoundError, match="extraction.md"):
            execute_validate(config)


class TestPartialFailure:
    """Multi-agent partial failure produces degraded report."""

    def test_degraded_report_on_partial_failure(self, tmp_path, monkeypatch):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        _make_pipeline_outputs(output_dir)
        config = _make_validate_config(output_dir, agent_count=2)

        def mock_execute_pipeline(steps, config, run_step, **kwargs):
            validate_dir = output_dir / "validate"
            validate_dir.mkdir(parents=True, exist_ok=True)

            # Parallel group is steps[0] (list of reflect steps)
            parallel_group = steps[0]
            agent_a_step = parallel_group[0]
            agent_b_step = parallel_group[1]

            # Agent A succeeds, agent B fails
            # Write agent A's reflection file
            agent_a_step.output_file.write_text(_known_good_report(), encoding="utf-8")
            return [
                StepResult(
                    step=agent_a_step,
                    status=StepStatus.PASS,
                    attempt=1,
                    started_at=_now(),
                    finished_at=_now(),
                ),
                StepResult(
                    step=agent_b_step,
                    status=StepStatus.FAIL,
                    attempt=2,
                    gate_failure_reason="Step timed out",
                    started_at=_now(),
                    finished_at=_now(),
                ),
            ]

        monkeypatch.setattr(
            "superclaude.cli.roadmap.validate_executor.execute_pipeline",
            mock_execute_pipeline,
        )

        execute_validate(config)

        report_path = output_dir / "validate" / "validation-report.md"
        assert report_path.exists()
        content = report_path.read_text(encoding="utf-8")
        assert "validation_complete: false" in content
        assert "DEGRADED VALIDATION REPORT" in content
        assert "reflect-haiku-architect" in content

    def test_degraded_report_preserves_successful_reflection(
        self, tmp_path, monkeypatch
    ):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        _make_pipeline_outputs(output_dir)
        config = _make_validate_config(output_dir, agent_count=2)

        def mock_execute_pipeline(steps, config, run_step, **kwargs):
            validate_dir = output_dir / "validate"
            validate_dir.mkdir(parents=True, exist_ok=True)

            parallel_group = steps[0]
            agent_a_step = parallel_group[0]
            agent_b_step = parallel_group[1]

            # Agent A succeeds -- write its file
            agent_a_step.output_file.write_text(_known_good_report(), encoding="utf-8")
            return [
                StepResult(
                    step=agent_a_step,
                    status=StepStatus.PASS,
                    attempt=1,
                    started_at=_now(),
                    finished_at=_now(),
                ),
                StepResult(
                    step=agent_b_step,
                    status=StepStatus.FAIL,
                    attempt=2,
                    gate_failure_reason="Agent failed",
                    started_at=_now(),
                    finished_at=_now(),
                ),
            ]

        monkeypatch.setattr(
            "superclaude.cli.roadmap.validate_executor.execute_pipeline",
            mock_execute_pipeline,
        )

        execute_validate(config)

        # Agent A's reflection file is preserved
        reflect_a = output_dir / "validate" / "reflect-opus-architect.md"
        assert reflect_a.exists()


class TestWriteDegradedReport:
    """Unit tests for _write_degraded_report."""

    def test_frontmatter_contains_validation_complete_false(self, tmp_path):
        report = tmp_path / "report.md"
        _write_degraded_report(
            report,
            failed_ids=["reflect-haiku-architect"],
            passed_ids=["reflect-opus-architect"],
        )
        content = report.read_text(encoding="utf-8")
        assert "validation_complete: false" in content

    def test_banner_names_failed_agents(self, tmp_path):
        report = tmp_path / "report.md"
        _write_degraded_report(
            report,
            failed_ids=["reflect-haiku-architect"],
            passed_ids=["reflect-opus-architect"],
        )
        content = report.read_text(encoding="utf-8")
        assert "reflect-haiku-architect" in content
        assert "DEGRADED VALIDATION REPORT" in content

    def test_multiple_failed_agents(self, tmp_path):
        report = tmp_path / "report.md"
        _write_degraded_report(
            report,
            failed_ids=["agent-1", "agent-2"],
            passed_ids=[],
        )
        content = report.read_text(encoding="utf-8")
        assert "agent-1" in content
        assert "agent-2" in content
        assert "passed_agents: none" in content

    def test_creates_parent_directory(self, tmp_path):
        report = tmp_path / "nested" / "dir" / "report.md"
        _write_degraded_report(report, failed_ids=["a"], passed_ids=["b"])
        assert report.exists()


class TestParseReportCounts:
    """Unit tests for _parse_report_counts."""

    def test_parses_known_good(self, tmp_path):
        report = tmp_path / "report.md"
        report.write_text(_known_good_report(), encoding="utf-8")
        result = _parse_report_counts(report)
        assert result["blocking_count"] == 0
        assert result["warning_count"] == 2
        assert result["info_count"] == 1

    def test_parses_known_bad(self, tmp_path):
        report = tmp_path / "report.md"
        report.write_text(_known_bad_report(), encoding="utf-8")
        result = _parse_report_counts(report)
        assert result["blocking_count"] == 3
        assert result["warning_count"] == 1

    def test_missing_file_returns_zeros(self, tmp_path):
        report = tmp_path / "nonexistent.md"
        result = _parse_report_counts(report)
        assert result == {"blocking_count": 0, "warning_count": 0, "info_count": 0}

    def test_no_frontmatter_returns_zeros(self, tmp_path):
        report = tmp_path / "report.md"
        report.write_text("Just plain text, no frontmatter.\n")
        result = _parse_report_counts(report)
        assert result == {"blocking_count": 0, "warning_count": 0, "info_count": 0}


# ── C06 two-facade helper matrix (G3.1-G3.18) ─────────────────────────────────
#
# Helpers are always looked up on the facade module at call time, so the
# matrix keeps exercising whatever module-local names the two executors expose.

_FACADE_LOGGERS = {
    "superclaude.cli.tasklist.executor": "superclaude.tasklist.executor",
    "superclaude.cli.roadmap.validate_executor": "superclaude.roadmap.validate_executor",
}

FACADES = [
    pytest.param(tasklist_executor, id="tasklist"),
    pytest.param(validate_executor, id="validate"),
]

_PRE = "é" * 1000 + "\n"

# (case id, input bytes, expected return, expected bytes after; None = unchanged)
SANITIZE_CASES = [
    pytest.param(b"", 0, None, id="G3.2-empty"),
    pytest.param(b"a", 0, None, id="G3.3-minimal"),
    pytest.param(b"just prose\nno frontmatter\n", 0, None, id="plain-no-delimiter"),
    pytest.param(b"---\nx: 1\n---\nbody", 0, None, id="G3.4-frontmatter"),
    pytest.param(b" \n\t---\nx: 1\n---\nbody", 0, None, id="G3.4-leading-ws"),
    pytest.param(
        b"Hi\n---\nx: 1\n---\nbody", 3, b"---\nx: 1\n---\nbody", id="G3.5-prefix3"
    ),
    pytest.param(
        (_PRE + "---\nbody").encode("utf-8"), 2001, b"---\nbody", id="G3.6-prefix2001"
    ),
    pytest.param(b"  ---not-yaml", 0, None, id="G3.7-leading-malformed"),
    pytest.param(b"---\nunclosed", 0, None, id="G3.7-unclosed"),
    pytest.param(b"x---y", 0, None, id="G3.8-inline"),
    pytest.param(b"x\n ---\nbody", 0, None, id="G3.8-indented"),
    pytest.param(b"x\n--- \t", 2, b"--- \t", id="G3.9-terminal-spaced"),
    pytest.param(b"x\n---\na\n---\nb", 2, b"---\na\n---\nb", id="G3.10-first-match"),
    # G3.18: text-mode read_text/write_text semantics (universal newlines on
    # read, "\n" on write) -- not a raw-byte sanitizer.
    pytest.param(
        b"Hi\r\n---\r\nx: 1\r\n---\r\nbody\r\n",
        3,
        b"---\nx: 1\n---\nbody\n",
        id="G3.18-crlf",
    ),
    pytest.param(b"Hi\r---\rbody", 3, b"---\nbody", id="G3.18-cr"),
    pytest.param(b"---\r\nx: 1\r\n", 0, None, id="G3.18-crlf-noop-bytes-kept"),
]


def _logger_name(facade) -> str:
    return _FACADE_LOGGERS[facade.__name__]


def _records(caplog, name: str) -> list[logging.LogRecord]:
    return [r for r in caplog.records if r.name == name]


def _any_sanitize_log(caplog) -> bool:
    return any("preamble" in r.getMessage() for r in caplog.records)


class TestC06SanitizeMatrix:
    """G3.1-G3.10 and G3.18 through both facades."""

    @pytest.mark.parametrize("facade", FACADES)
    def test_g3_1_missing_output_returns_zero(self, facade, tmp_path, caplog):
        caplog.set_level(logging.DEBUG)
        out = tmp_path / "missing.md"
        assert facade._sanitize_output(out) == 0
        assert not out.exists()
        assert not (tmp_path / "missing.md.tmp").exists()
        assert not _any_sanitize_log(caplog)

    @pytest.mark.parametrize("facade", FACADES)
    @pytest.mark.parametrize("data,expected_ret,expected_after", SANITIZE_CASES)
    def test_sanitize_case(
        self, facade, data, expected_ret, expected_after, tmp_path, caplog
    ):
        caplog.set_level(logging.DEBUG)
        out = tmp_path / "out.md"
        out.write_bytes(data)

        ret = facade._sanitize_output(out)

        assert ret == expected_ret
        assert out.read_bytes() == (data if expected_after is None else expected_after)
        assert not (tmp_path / "out.md.tmp").exists()
        assert sorted(p.name for p in tmp_path.iterdir()) == ["out.md"]
        mine = _records(caplog, _logger_name(facade))
        if expected_ret == 0:
            # No-op: no write, no success log.
            assert not _any_sanitize_log(caplog)
        else:
            # Success-only log on the ORIGINAL caller logger, after replace.
            assert [(r.levelno, r.getMessage()) for r in mine] == [
                (logging.INFO, f"Stripped {expected_ret}-byte preamble from {out}")
            ]
            other = [n for n in _FACADE_LOGGERS.values() if n != _logger_name(facade)][
                0
            ]
            assert _records(caplog, other) == []


class TestC06SanitizeFailures:
    """G3.11-G3.13 plus logger failure and fixed ``<suffix>.tmp`` naming."""

    @pytest.mark.parametrize("facade", FACADES)
    def test_g3_11_permission_error_on_read_propagates(
        self, facade, tmp_path, monkeypatch, caplog
    ):
        caplog.set_level(logging.DEBUG)
        out = tmp_path / "out.md"
        out.write_bytes(b"Hi\n---\nbody")
        real_read_text = Path.read_text

        def fake_read_text(self, *args, **kwargs):
            if self == out:
                raise PermissionError("denied")
            return real_read_text(self, *args, **kwargs)

        monkeypatch.setattr(Path, "read_text", fake_read_text)
        with pytest.raises(PermissionError, match="denied"):
            facade._sanitize_output(out)
        assert out.read_bytes() == b"Hi\n---\nbody"
        assert not (tmp_path / "out.md.tmp").exists()
        assert not _any_sanitize_log(caplog)

    @pytest.mark.parametrize("facade", FACADES)
    def test_g3_11_unicode_decode_error_propagates(self, facade, tmp_path, caplog):
        caplog.set_level(logging.DEBUG)
        out = tmp_path / "out.md"
        data = b"Hi\n\xff\n---\nbody"
        out.write_bytes(data)
        with pytest.raises(UnicodeDecodeError):
            facade._sanitize_output(out)
        assert out.read_bytes() == data
        assert not (tmp_path / "out.md.tmp").exists()
        assert not _any_sanitize_log(caplog)

    @pytest.mark.parametrize("facade", FACADES)
    def test_g3_12_tmp_write_failure_propagates_before_replace(
        self, facade, tmp_path, monkeypatch, caplog
    ):
        caplog.set_level(logging.DEBUG)
        out = tmp_path / "out.md"
        out.write_bytes(b"Hi\n---\nbody")
        replaced: list = []
        real_write_text = Path.write_text

        def fake_write_text(self, *args, **kwargs):
            if self.name.endswith(".tmp"):
                raise OSError("tmp write boom")
            return real_write_text(self, *args, **kwargs)

        monkeypatch.setattr(Path, "write_text", fake_write_text)
        monkeypatch.setattr(os, "replace", lambda *a: replaced.append(a))
        with pytest.raises(OSError, match="tmp write boom"):
            facade._sanitize_output(out)
        assert replaced == []
        assert out.read_bytes() == b"Hi\n---\nbody"
        assert not (tmp_path / "out.md.tmp").exists()
        assert not _any_sanitize_log(caplog)

    @pytest.mark.parametrize("facade", FACADES)
    def test_g3_13_replace_failure_propagates_temp_remains(
        self, facade, tmp_path, monkeypatch, caplog
    ):
        caplog.set_level(logging.DEBUG)
        out = tmp_path / "out.md"
        out.write_bytes(b"Hi\n---\nbody")

        def boom(src, dst):
            raise OSError("replace boom")

        monkeypatch.setattr(os, "replace", boom)
        with pytest.raises(OSError, match="replace boom"):
            facade._sanitize_output(out)
        # Destination unchanged; temp remains (no added cleanup); no log.
        assert out.read_bytes() == b"Hi\n---\nbody"
        assert (tmp_path / "out.md.tmp").read_bytes() == b"---\nbody"
        assert not _any_sanitize_log(caplog)

    @pytest.mark.parametrize("facade", FACADES)
    def test_logger_failure_propagates_after_replace(
        self, facade, tmp_path, monkeypatch
    ):
        class _BoomLogger:
            def info(self, *args, **kwargs):
                raise RuntimeError("logger boom")

        monkeypatch.setattr(facade, "_log", _BoomLogger())
        out = tmp_path / "out.md"
        out.write_bytes(b"Hi\n---\nbody")
        with pytest.raises(RuntimeError, match="logger boom"):
            facade._sanitize_output(out)
        assert out.read_bytes() == b"---\nbody"
        assert not (tmp_path / "out.md.tmp").exists()

    @pytest.mark.parametrize("facade", FACADES)
    @pytest.mark.parametrize(
        "name,tmp_name",
        [("out.md", "out.md.tmp"), ("report", "report.tmp")],
        ids=["md-suffix", "no-suffix"],
    )
    def test_fixed_suffix_tmp_then_replace(
        self, facade, name, tmp_name, tmp_path, monkeypatch
    ):
        out = tmp_path / name
        out.write_bytes(b"Hi\n---\nbody")
        calls: list = []
        real_replace = os.replace

        def recording_replace(src, dst):
            calls.append((Path(src), Path(dst), Path(src).read_bytes()))
            return real_replace(src, dst)

        monkeypatch.setattr(os, "replace", recording_replace)
        assert facade._sanitize_output(out) == 3
        assert calls == [(tmp_path / tmp_name, out, b"---\nbody")]

    @pytest.mark.parametrize("facade", FACADES)
    def test_module_local_logger_seam(self, facade, tmp_path, monkeypatch, caplog):
        seam = logging.getLogger("tests.c06.logger_seam")
        monkeypatch.setattr(facade, "_log", seam)
        caplog.set_level(logging.DEBUG)
        out = tmp_path / "out.md"
        out.write_bytes(b"Hi\n---\nbody")
        assert facade._sanitize_output(out) == 3
        assert [r.getMessage() for r in _records(caplog, seam.name)] == [
            f"Stripped 3-byte preamble from {out}"
        ]
        assert _records(caplog, _logger_name(facade)) == []


class TestC06EmbedMatrix:
    """G3.15-G3.17 through both facades."""

    @pytest.mark.parametrize("facade", FACADES)
    def test_g3_15_empty_inputs(self, facade):
        assert facade._embed_inputs([]) == ""

    @pytest.mark.parametrize("facade", FACADES)
    def test_g3_16_three_ordered_blocks_no_dedupe(self, facade, tmp_path):
        p = tmp_path / "p.md"
        q = tmp_path / "q.md"
        p.write_text("", encoding="utf-8")
        q.write_bytes("é".encode("utf-8"))
        assert facade._embed_inputs([p, p, q]) == (
            f"# {p}\n```\n\n```\n\n# {p}\n```\n\n```\n\n# {q}\n```\né\n```"
        )

    @pytest.mark.parametrize("facade", FACADES)
    def test_g3_17_missing_input_propagates(self, facade, tmp_path):
        ok = tmp_path / "ok.md"
        ok.write_text("ok", encoding="utf-8")
        with pytest.raises(FileNotFoundError):
            facade._embed_inputs([ok, tmp_path / "absent.md"])

    @pytest.mark.parametrize("facade", FACADES)
    def test_g3_17_undecodable_input_propagates(self, facade, tmp_path):
        bad = tmp_path / "bad.md"
        bad.write_bytes(b"\xff\xfe")
        with pytest.raises(UnicodeDecodeError):
            facade._embed_inputs([bad])


class TestC06MainRoadmapHelpersSeparate:
    """Main-roadmap helpers are distinct and keep their own behavior."""

    @pytest.mark.parametrize("facade", FACADES)
    def test_distinct_objects(self, facade):
        assert facade._embed_inputs is not main_roadmap_executor._embed_inputs
        assert facade._sanitize_output is not main_roadmap_executor._sanitize_output

    @pytest.mark.parametrize("facade", FACADES)
    def test_leading_whitespace_contrast(self, facade, tmp_path):
        data = b" \n\t---\nx: 1\n---\nbody"
        a = tmp_path / "facade.md"
        b = tmp_path / "main.md"
        a.write_bytes(data)
        b.write_bytes(data)
        assert facade._sanitize_output(a) == 0
        assert a.read_bytes() == data
        assert main_roadmap_executor._sanitize_output(b) == 3
        assert b.read_bytes() == b"---\nx: 1\n---\nbody"


# ── C06 real validate_run_step (fake caller-local ClaudeProcess) ──────────────


class _FakePopen:
    def __init__(self, polls):
        self._polls = list(polls)

    def poll(self):
        return self._polls.pop(0) if self._polls else 0


def _install_fake_process(
    monkeypatch, *, output: bytes | None = None, exit_code: int = 0, polls=()
):
    """Patch the module-local ``validate_executor.ClaudeProcess`` name."""
    created: list = []

    class FakeClaudeProcess:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.started = False
            self.terminated = False
            self.wait_calls = 0
            self._process = _FakePopen(polls) if polls else None
            created.append(self)

        def start(self):
            self.started = True
            if output is not None:
                self.kwargs["output_file"].write_bytes(output)

        def wait(self):
            self.wait_calls += 1
            return exit_code

        def terminate(self):
            self.terminated = True

    monkeypatch.setattr(validate_executor, "ClaudeProcess", FakeClaudeProcess)
    return created


def _vstep(tmp_path: Path, inputs=(), step_id="c06-step", model="") -> Step:
    return Step(
        id=step_id,
        prompt="P",
        output_file=tmp_path / "out.md",
        gate=None,
        timeout_seconds=60,
        inputs=list(inputs),
        model=model,
    )


def _vconfig(**kw) -> PipelineConfig:
    base = dict(dry_run=False, max_turns=7, model="cfg-model", permission_flag="--perm")
    base.update(kw)
    return PipelineConfig(**base)


_VLOG = "superclaude.roadmap.validate_executor"
_PREAMBLE_OUT = b"Hi\n---\nx: 1\n---\nbody"


def _assert_times(result):
    assert result.started_at.tzinfo == timezone.utc
    assert result.finished_at.tzinfo == timezone.utc
    assert result.started_at <= result.finished_at


class TestC06ValidateRunStepReal:
    def test_success_prompt_options_sanitize_and_caller_logger(
        self, tmp_path, monkeypatch, caplog
    ):
        caplog.set_level(logging.DEBUG)
        a = tmp_path / "a.md"
        b = tmp_path / "b.md"
        a.write_text("A", encoding="utf-8")
        b.write_text("B", encoding="utf-8")
        created = _install_fake_process(monkeypatch, output=_PREAMBLE_OUT)
        step = _vstep(tmp_path, inputs=[a, b])

        result = validate_executor.validate_run_step(step, _vconfig(), lambda: False)

        assert result.status == StepStatus.PASS
        assert result.attempt == 1
        assert result.gate_failure_reason is None
        assert result.step is step
        _assert_times(result)
        (proc,) = created
        assert proc.kwargs == {
            "prompt": f"P\n\n# {a}\n```\nA\n```\n\n# {b}\n```\nB\n```",
            "output_file": step.output_file,
            "error_file": tmp_path / "out.err",
            "max_turns": 7,
            "model": "cfg-model",
            "permission_flag": "--perm",
            "timeout_seconds": 60,
            "output_format": "text",
            "extra_args": [],
        }
        assert proc.started and proc.wait_calls == 1 and not proc.terminated
        assert step.output_file.read_bytes() == b"---\nx: 1\n---\nbody"
        assert not (tmp_path / "out.md.tmp").exists()
        assert [(r.levelno, r.getMessage()) for r in _records(caplog, _VLOG)] == [
            (logging.INFO, f"Stripped 3-byte preamble from {step.output_file}")
        ]
        assert _records(caplog, "superclaude.tasklist.executor") == []

    def test_no_inputs_uses_bare_prompt_and_step_model(self, tmp_path, monkeypatch):
        created = _install_fake_process(monkeypatch, output=b"---\nok\n")
        step = _vstep(tmp_path, model="step-model")
        result = validate_executor.validate_run_step(step, _vconfig(), lambda: False)
        assert result.status == StepStatus.PASS
        assert created[0].kwargs["prompt"] == "P"
        assert created[0].kwargs["extra_args"] == []
        assert created[0].kwargs["model"] == "step-model"
        assert step.output_file.read_bytes() == b"---\nok\n"

    @pytest.mark.parametrize(
        "exit_code,status,reason",
        [
            (124, StepStatus.TIMEOUT, "Step 'c06-step' timed out after 60s"),
            (3, StepStatus.FAIL, "Step 'c06-step' exited with code 3"),
        ],
        ids=["timeout", "nonzero"],
    )
    def test_timeout_and_nonzero_skip_sanitize(
        self, exit_code, status, reason, tmp_path, monkeypatch, caplog
    ):
        caplog.set_level(logging.DEBUG)
        _install_fake_process(monkeypatch, output=_PREAMBLE_OUT, exit_code=exit_code)
        sanitized: list = []
        monkeypatch.setattr(validate_executor, "_sanitize_output", sanitized.append)
        step = _vstep(tmp_path)
        result = validate_executor.validate_run_step(step, _vconfig(), lambda: False)
        assert result.status == status
        assert result.gate_failure_reason == reason
        _assert_times(result)
        assert sanitized == []
        assert step.output_file.read_bytes() == _PREAMBLE_OUT

    def test_cancel_terminates_and_skips_wait_and_sanitize(self, tmp_path, monkeypatch):
        created = _install_fake_process(monkeypatch, output=_PREAMBLE_OUT, polls=[None])
        step = _vstep(tmp_path)
        result = validate_executor.validate_run_step(step, _vconfig(), lambda: True)
        assert result.status == StepStatus.CANCELLED
        assert result.gate_failure_reason == "Cancelled by external signal"
        _assert_times(result)
        assert created[0].terminated
        assert created[0].wait_calls == 0
        assert step.output_file.read_bytes() == _PREAMBLE_OUT

    def test_poll_loop_sleeps_one_second(self, tmp_path, monkeypatch):
        _install_fake_process(monkeypatch, output=_PREAMBLE_OUT, polls=[None, 0])
        sleeps: list = []
        monkeypatch.setattr(validate_executor.time, "sleep", sleeps.append)
        step = _vstep(tmp_path)
        result = validate_executor.validate_run_step(step, _vconfig(), lambda: False)
        assert result.status == StepStatus.PASS
        assert sleeps == [1]
        assert step.output_file.read_bytes() == b"---\nx: 1\n---\nbody"

    def test_dry_run_never_embeds_spawns_or_sanitizes(
        self, tmp_path, monkeypatch, caplog
    ):
        caplog.set_level(logging.DEBUG)
        created = _install_fake_process(monkeypatch, output=_PREAMBLE_OUT)
        step = _vstep(tmp_path, inputs=[tmp_path / "absent.md"])
        result = validate_executor.validate_run_step(
            step, _vconfig(dry_run=True), lambda: False
        )
        assert result.status == StepStatus.PASS
        _assert_times(result)
        assert created == []
        assert not step.output_file.exists()
        assert [r.getMessage() for r in _records(caplog, _VLOG)] == [
            "[dry-run] Would execute step 'c06-step'"
        ]

    def test_unreadable_input_propagates_before_process(self, tmp_path, monkeypatch):
        created = _install_fake_process(monkeypatch, output=_PREAMBLE_OUT)
        step = _vstep(tmp_path, inputs=[tmp_path / "absent.md"])
        with pytest.raises(FileNotFoundError):
            validate_executor.validate_run_step(step, _vconfig(), lambda: False)
        assert created == []

    def test_module_local_helper_seams(self, tmp_path, monkeypatch):
        events: list = []
        created = _install_fake_process(monkeypatch, output=_PREAMBLE_OUT)
        monkeypatch.setattr(
            validate_executor,
            "_embed_inputs",
            lambda paths: events.append(("embed", list(paths))) or "EMBED",
        )
        monkeypatch.setattr(
            validate_executor,
            "_sanitize_output",
            lambda p: events.append(("sanitize", p, created[0].wait_calls)) or 0,
        )
        x = tmp_path / "x.md"
        step = _vstep(tmp_path, inputs=[x])
        result = validate_executor.validate_run_step(step, _vconfig(), lambda: False)
        assert result.status == StepStatus.PASS
        assert created[0].kwargs["prompt"] == "P\n\nEMBED"
        assert events == [("embed", [x]), ("sanitize", step.output_file, 1)]
        # Patched sanitizer did nothing, so the preamble is still on disk.
        assert step.output_file.read_bytes() == _PREAMBLE_OUT

    def test_module_local_logger_seam_through_run_step(
        self, tmp_path, monkeypatch, caplog
    ):
        seam = logging.getLogger("tests.c06.run_step_logger_seam")
        monkeypatch.setattr(validate_executor, "_log", seam)
        caplog.set_level(logging.DEBUG)
        _install_fake_process(monkeypatch, output=_PREAMBLE_OUT)
        step = _vstep(tmp_path)
        validate_executor.validate_run_step(step, _vconfig(), lambda: False)
        assert [r.getMessage() for r in _records(caplog, seam.name)] == [
            f"Stripped 3-byte preamble from {step.output_file}"
        ]
        assert _records(caplog, _VLOG) == []


class TestC06ValidateRunStepToolWriteOrder:
    """Sanitize runs before the reflect tool-write render."""

    def _run(self, tmp_path, monkeypatch, render_result, flag=True):
        _install_fake_process(monkeypatch, output=b"Hi\n---\n{}")
        seen: list = []

        def fake_render(step_id, json_text, output_path):
            seen.append((step_id, json_text, output_path, output_path.read_bytes()))
            return render_result

        monkeypatch.setattr(tool_writer, "render_step_tool_write", fake_render)
        config = ValidateConfig(
            output_dir=tmp_path,
            dry_run=False,
            tool_write_validate_reflect=flag,
        )
        step = _vstep(tmp_path, step_id="reflect")
        result = validate_executor.validate_run_step(step, config, lambda: False)
        return step, result, seen

    def test_render_receives_sanitized_text(self, tmp_path, monkeypatch):
        step, result, seen = self._run(tmp_path, monkeypatch, [])
        assert result.status == StepStatus.PASS
        assert seen == [("reflect", "---\n{}", step.output_file, b"---\n{}")]

    def test_render_errors_fail_after_sanitize(self, tmp_path, monkeypatch):
        step, result, seen = self._run(tmp_path, monkeypatch, ["e1", "e2"])
        assert result.status == StepStatus.FAIL
        assert result.gate_failure_reason == (
            "Step 'reflect' tool-write schema/render failure: e1; e2"
        )
        _assert_times(result)
        assert seen[0][3] == b"---\n{}"

    def test_flag_off_skips_render(self, tmp_path, monkeypatch):
        step, result, seen = self._run(tmp_path, monkeypatch, [], flag=False)
        assert result.status == StepStatus.PASS
        assert seen == []
        assert step.output_file.read_bytes() == b"---\n{}"
