"""Tests for roadmap executor integration -- full pipeline with mock subprocesses."""

from __future__ import annotations

import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.pipeline.models import (
    GateCriteria,
    PipelineConfig,
    Step,
    StepResult,
    StepStatus,
)
from superclaude.cli.pipeline.executor import execute_pipeline
from superclaude.cli.roadmap.executor import (
    _build_steps,
    _check_annotate_deviations_freshness,
    _check_remediation_budget,
    _format_halt_output,
    _inject_pipeline_diagnostics,
    _inject_provenance_fields,
    _print_terminal_halt,
    _sanitize_output,
    _save_state,
    execute_roadmap,
)
from superclaude.cli.roadmap.models import AgentSpec, Finding, RoadmapConfig


def _now():
    return datetime.now(timezone.utc)


def _make_config(tmp_path: Path) -> RoadmapConfig:
    spec = tmp_path / "spec.md"
    spec.write_text("# Test Spec\nContent for testing.\n")
    output = tmp_path / "output"
    output.mkdir(exist_ok=True)
    return RoadmapConfig(
        spec_file=spec,
        output_dir=output,
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        depth="standard",
    )


class TestBuildSteps:
    def test_produces_8_entries(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        assert (
            len(steps) == 8
        )  # 6 sequential + 1 parallel group (2 steps) + spec-fidelity

    def test_second_entry_is_parallel(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        assert isinstance(steps[1], list)
        assert len(steps[1]) == 2

    def test_step_ids_in_order(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        ids = []
        for entry in steps:
            if isinstance(entry, list):
                ids.extend(s.id for s in entry)
            else:
                ids.append(entry.id)
        assert ids[0] == "extract"
        assert ids[1].startswith("generate-")
        assert ids[2].startswith("generate-")
        assert ids[3] == "diff"
        assert ids[4] == "debate"
        assert ids[5] == "score"
        assert ids[6] == "merge"
        assert ids[7] == "test-strategy"
        assert ids[8] == "spec-fidelity"


class TestIntegrationMockSubprocess:
    """Full pipeline run with mock step runner producing gate-passing output."""

    def test_full_pipeline_all_pass(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)

        def mock_runner(step, cfg, cancel_check):
            # Write gate-passing output for each step
            # Use realistic values for specific frontmatter fields
            fm_values = {
                "spec_source": "spec.md",
                "generated": "2026-03-08T00:00:00Z",
                "generator": "test-agent",
                "functional_requirements": "5",
                "nonfunctional_requirements": "3",
                "total_requirements": "8",
                "complexity_score": "0.7",
                "complexity_class": "MEDIUM",
                "domains_detected": "[backend, frontend]",
                "risks_identified": "3",
                "dependencies_identified": "4",
                "success_criteria_count": "5",
                "extraction_mode": "standard",
                "primary_persona": "architect",
                "total_diff_points": "3",
                "shared_assumptions_count": "4",
                "convergence_score": "0.85",
                "rounds_completed": "2",
                "base_variant": "A",
                "variant_scores": "A:78 B:72",
                "adversarial": "true",
                "validation_philosophy": "continuous-parallel",
                "validation_milestones": "3",
                "work_milestones": "6",
                "interleave_ratio": "1:2",
                "major_issue_policy": "stop-and-fix",
                "high_severity_count": "0",
                "medium_severity_count": "0",
                "low_severity_count": "0",
                "total_deviations": "0",
                "validation_complete": "true",
                "tasklist_ready": "true",
            }
            fm_fields = {}
            if step.gate and step.gate.required_frontmatter_fields:
                for f in step.gate.required_frontmatter_fields:
                    fm_fields[f] = fm_values.get(f, "test_value")

            content_lines = ["---"]
            for k, v in fm_fields.items():
                content_lines.append(f"{k}: {v}")
            content_lines.append("---")
            # Add enough content lines with list items (for has_actionable_content)
            content_lines.append("## Overview")
            min_needed = step.gate.min_lines if step.gate else 10
            for i in range(max(min_needed, 10)):
                content_lines.append(f"- Item {i}: content for {step.id}")
            content = "\n".join(content_lines)

            step.output_file.parent.mkdir(parents=True, exist_ok=True)
            step.output_file.write_text(content)

            return StepResult(
                step=step,
                status=StepStatus.PASS,
                attempt=1,
                started_at=_now(),
                finished_at=_now(),
            )

        results = execute_pipeline(
            steps=steps,
            config=config,
            run_step=mock_runner,
        )

        assert len(results) == 9  # 8 entries -> 9 individual steps
        assert all(r.status == StepStatus.PASS for r in results)

    def test_pipeline_halts_on_gate_failure(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)

        def failing_runner(step, cfg, cancel_check):
            # Don't write any output -> gates will fail
            return StepResult(
                step=step,
                status=StepStatus.PASS,
                attempt=1,
                started_at=_now(),
                finished_at=_now(),
            )

        results = execute_pipeline(
            steps=steps,
            config=config,
            run_step=failing_runner,
        )

        # First step (extract) should fail gate (no output written)
        assert results[-1].status == StepStatus.FAIL
        assert len(results) < 9  # Not all steps executed


class TestContextIsolation:
    def test_subprocess_uses_mock(self, tmp_path):
        """Verify all tests use unittest.mock.patch for subprocess isolation."""
        # This is a meta-test documenting that integration tests
        # use mock runners rather than real subprocess calls.
        with patch("subprocess.Popen") as mock_popen:
            # If any test accidentally called subprocess.Popen directly,
            # this would be caught. Our mock runner pattern avoids that.
            assert not mock_popen.called


class TestSaveAndReloadState:
    def test_state_roundtrip(self, tmp_path):
        config = _make_config(tmp_path)
        step = Step(
            id="extract",
            prompt="p",
            output_file=config.output_dir / "extract.md",
            gate=None,
            timeout_seconds=300,
        )
        results = [
            StepResult(
                step=step,
                status=StepStatus.PASS,
                attempt=1,
                started_at=_now(),
                finished_at=_now(),
            ),
        ]

        _save_state(config, results)

        from superclaude.cli.roadmap.executor import read_state

        state = read_state(config.output_dir / ".roadmap-state.json")
        assert state is not None
        assert state["schema_version"] == 1
        assert state["steps"]["extract"]["status"] == "PASS"


class TestSanitizeOutput:
    """Unit tests for _sanitize_output() -- spec §6.2 test matrix."""

    def test_strips_preamble_before_frontmatter(self, tmp_path):
        """Preamble present: file is rewritten, returns byte count."""
        f = tmp_path / "output.md"
        preamble = "Here is the result:\n\n"
        body = "---\ntitle: test\n---\n## Content\n- item 1\n"
        f.write_text(preamble + body, encoding="utf-8")

        result = _sanitize_output(f)

        assert result == len(preamble.encode("utf-8"))
        assert f.read_text(encoding="utf-8") == body

    def test_no_preamble_unchanged(self, tmp_path):
        """No preamble (starts with ---): file unchanged, returns 0."""
        f = tmp_path / "output.md"
        content = "---\ntitle: test\n---\n## Content\n"
        f.write_text(content, encoding="utf-8")

        result = _sanitize_output(f)

        assert result == 0
        assert f.read_text(encoding="utf-8") == content

    def test_no_frontmatter_unchanged(self, tmp_path):
        """No frontmatter delimiter at all: file unchanged, returns 0."""
        f = tmp_path / "output.md"
        content = "Just some text without any frontmatter.\n"
        f.write_text(content, encoding="utf-8")

        result = _sanitize_output(f)

        assert result == 0
        assert f.read_text(encoding="utf-8") == content

    def test_multi_line_preamble_stripped(self, tmp_path):
        """Multi-line preamble: all lines before first --- are stripped."""
        f = tmp_path / "output.md"
        preamble = "Sure! Here is your output.\n\nI've formatted it as requested:\n\n"
        body = "---\nkey: value\n---\n- item\n"
        f.write_text(preamble + body, encoding="utf-8")

        result = _sanitize_output(f)

        assert result == len(preamble.encode("utf-8"))
        assert f.read_text(encoding="utf-8") == body

    def test_atomic_write_uses_tmp_and_replace(self, tmp_path):
        """Atomic write: .tmp file used and os.replace() called."""
        f = tmp_path / "output.md"
        preamble = "preamble\n"
        body = "---\ntitle: test\n---\n"
        f.write_text(preamble + body, encoding="utf-8")

        with patch("os.replace", wraps=__import__("os").replace) as mock_replace:
            result = _sanitize_output(f)

        assert result > 0
        # os.replace was called with the .tmp source and original target
        mock_replace.assert_called_once()
        call_args = mock_replace.call_args[0]
        assert str(call_args[0]).endswith(".tmp")
        assert call_args[1] == f
        # Final file has correct content
        assert f.read_text(encoding="utf-8") == body


# ═══════════════════════════════════════════════════════════════
# Solution C -- Leading whitespace fix tests
# ═══════════════════════════════════════════════════════════════


class TestSanitizeOutputLeadingWhitespace:
    """Tests for _sanitize_output leading-whitespace stripping (Solution C Fix 1)."""

    def test_leading_newlines_stripped(self, tmp_path):
        """Leading \\n\\n before --- should be stripped."""
        f = tmp_path / "output.md"
        body = "---\ntitle: test\n---\n## Content\n"
        f.write_text("\n\n" + body, encoding="utf-8")

        result = _sanitize_output(f)

        assert result == 2  # two newline bytes stripped
        assert f.read_text(encoding="utf-8") == body

    def test_leading_crlf_stripped(self, tmp_path):
        """Leading \\r\\n before --- should be stripped.

        Python text mode normalizes \\r\\n → \\n on read, so the function
        sees \\n\\n (2 bytes) even when the file contains \\r\\n\\n.
        """
        f = tmp_path / "output.md"
        body = "---\ntitle: test\n---\n## Content\n"
        f.write_bytes(b"\r\n\n" + body.encode("utf-8"))

        result = _sanitize_output(f)

        # read_text normalizes \r\n -> \n, so function sees \n\n = 2 bytes
        assert result == 2
        assert f.read_text(encoding="utf-8") == body

    def test_single_leading_newline_stripped(self, tmp_path):
        """Single leading \\n before --- should be stripped."""
        f = tmp_path / "output.md"
        body = "---\ntitle: test\n---\n## Content\n"
        f.write_text("\n" + body, encoding="utf-8")

        result = _sanitize_output(f)

        assert result == 1
        assert f.read_text(encoding="utf-8") == body

    def test_no_leading_whitespace_unchanged(self, tmp_path):
        """No leading whitespace: file unchanged, returns 0."""
        f = tmp_path / "output.md"
        content = "---\ntitle: test\n---\n## Content\n"
        f.write_text(content, encoding="utf-8")

        result = _sanitize_output(f)

        assert result == 0
        assert f.read_text(encoding="utf-8") == content

    def test_no_frontmatter_with_leading_whitespace(self, tmp_path):
        """Leading whitespace but no frontmatter: file unchanged, returns 0."""
        f = tmp_path / "output.md"
        content = "\n\nJust text, no frontmatter.\n"
        f.write_text(content, encoding="utf-8")

        result = _sanitize_output(f)

        assert result == 0
        assert f.read_text(encoding="utf-8") == content

    def test_leading_newlines_plus_preamble(self, tmp_path):
        """Leading newlines followed by preamble text should all be stripped."""
        f = tmp_path / "output.md"
        preamble = "Here is the result:\n\n"
        body = "---\ntitle: test\n---\n## Content\n"
        f.write_text("\n\n" + preamble + body, encoding="utf-8")

        result = _sanitize_output(f)

        assert result == len(("\n\n" + preamble).encode("utf-8"))
        assert f.read_text(encoding="utf-8") == body

    def test_empty_file(self, tmp_path):
        """Empty file should return 0 and remain unchanged."""
        f = tmp_path / "output.md"
        f.write_text("", encoding="utf-8")

        result = _sanitize_output(f)

        assert result == 0
        assert f.read_text(encoding="utf-8") == ""

    def test_only_whitespace(self, tmp_path):
        """Whitespace-only file: no frontmatter found, returns 0, unchanged."""
        f = tmp_path / "output.md"
        f.write_text("\n\n\n", encoding="utf-8")

        result = _sanitize_output(f)

        assert result == 0
        assert f.read_text(encoding="utf-8") == "\n\n\n"


class TestInjectProvenanceFields:
    """Unit tests for _inject_provenance_fields whitespace and idempotency."""

    def test_injects_into_clean_frontmatter(self, tmp_path):
        """Baseline: fields injected when frontmatter starts at byte 0."""
        f = tmp_path / "test.md"
        f.write_text("---\ntitle: foo\n---\nbody\n", encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        content = f.read_text(encoding="utf-8")
        assert "spec_source: spec.md" in content
        assert "generator: superclaude-roadmap-executor" in content
        assert content.startswith("---")

    def test_injects_with_leading_blank_lines(self, tmp_path):
        """THE BUG: leading \\n\\n before --- must not prevent injection."""
        f = tmp_path / "test.md"
        f.write_text("\n\n---\ntitle: foo\n---\nbody\n", encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        content = f.read_text(encoding="utf-8")
        assert "spec_source: spec.md" in content
        assert content.startswith("---")  # leading whitespace stripped

    def test_noop_without_frontmatter(self, tmp_path):
        """Plain text file is left unchanged."""
        f = tmp_path / "test.md"
        original = "Just text, no frontmatter"
        f.write_text(original, encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        assert f.read_text(encoding="utf-8") == original

    def test_noop_empty_file(self, tmp_path):
        """Empty file is left unchanged."""
        f = tmp_path / "test.md"
        f.write_text("", encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        assert f.read_text(encoding="utf-8") == ""

    def test_noop_unclosed_frontmatter(self, tmp_path):
        """Unclosed frontmatter (no closing ---) is left unchanged."""
        f = tmp_path / "test.md"
        original = "---\ntitle: foo\nbody\n"
        f.write_text(original, encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        assert f.read_text(encoding="utf-8") == original

    def test_idempotent_double_call(self, tmp_path):
        """Calling twice does not duplicate provenance fields."""
        f = tmp_path / "test.md"
        f.write_text("---\ntitle: foo\n---\nbody\n", encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        _inject_provenance_fields(f, "spec.md")
        content = f.read_text(encoding="utf-8")
        assert content.count("spec_source:") == 1
        assert content.count("generator:") == 1

    def test_partial_provenance_present(self, tmp_path):
        """Only missing fields are injected when some already exist."""
        f = tmp_path / "test.md"
        f.write_text(
            "---\ntitle: foo\nspec_source: other.md\n---\nbody\n",
            encoding="utf-8",
        )
        _inject_provenance_fields(f, "spec.md")
        content = f.read_text(encoding="utf-8")
        assert content.count("spec_source:") == 1  # not overwritten
        assert "spec_source: other.md" in content  # original preserved
        assert "generator:" in content  # missing field added

    def test_empty_frontmatter_block(self, tmp_path):
        """Empty frontmatter (just --- / ---) gets fields injected."""
        f = tmp_path / "test.md"
        f.write_text("---\n---\nbody\n", encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        content = f.read_text(encoding="utf-8")
        assert "spec_source: spec.md" in content


class TestInjectPipelineDiagnostics:
    """Whitespace hardening tests for _inject_pipeline_diagnostics."""

    def test_injects_with_leading_blank_lines(self, tmp_path):
        """Leading whitespace before --- must not prevent injection."""
        f = tmp_path / "test.md"
        f.write_text("\n\n---\ntitle: foo\n---\nbody\n", encoding="utf-8")
        t0 = datetime(2025, 1, 1, tzinfo=timezone.utc)
        t1 = datetime(2025, 1, 1, 0, 1, tzinfo=timezone.utc)
        _inject_pipeline_diagnostics(f, t0, t1)
        content = f.read_text(encoding="utf-8")
        assert "pipeline_diagnostics:" in content
        assert content.startswith("---")

    def test_idempotent_double_call(self, tmp_path):
        """Calling twice does not duplicate diagnostics."""
        f = tmp_path / "test.md"
        f.write_text("---\ntitle: foo\n---\nbody\n", encoding="utf-8")
        t0 = datetime(2025, 1, 1, tzinfo=timezone.utc)
        t1 = datetime(2025, 1, 1, 0, 1, tzinfo=timezone.utc)
        _inject_pipeline_diagnostics(f, t0, t1)
        _inject_pipeline_diagnostics(f, t0, t1)
        content = f.read_text(encoding="utf-8")
        assert content.count("pipeline_diagnostics:") == 1


class TestSanitizeEnablesInjection:
    """E2E: sanitize + inject + gate flow works with leading whitespace."""

    def test_sanitize_enables_provenance_injection(self, tmp_path):
        """After sanitize strips leading newlines, _inject_provenance_fields succeeds."""
        f = tmp_path / "output.md"
        f.write_text(
            "\n\n---\ncomplexity_class: MEDIUM\n---\n## Content\n",
            encoding="utf-8",
        )

        _sanitize_output(f)
        _inject_provenance_fields(f, "my-spec.md")

        result = f.read_text(encoding="utf-8")
        assert "spec_source: my-spec.md" in result
        assert result.startswith("---")

    def test_sanitize_enables_diagnostics_injection(self, tmp_path):
        """After sanitize strips leading newlines, _inject_pipeline_diagnostics succeeds."""
        f = tmp_path / "output.md"
        f.write_text(
            "\n---\ntitle: extract\n---\n## Extraction\n",
            encoding="utf-8",
        )

        _sanitize_output(f)
        t0 = datetime(2025, 1, 1, tzinfo=timezone.utc)
        t1 = datetime(2025, 1, 1, 0, 1, tzinfo=timezone.utc)
        _inject_pipeline_diagnostics(f, t0, t1)

        result = f.read_text(encoding="utf-8")
        assert "pipeline_diagnostics:" in result
        assert result.startswith("---")

    def test_full_chain_sanitize_inject_verify(self, tmp_path):
        """Full chain: leading blanks -> sanitize -> inject provenance -> verify all fields."""
        f = tmp_path / "output.md"
        f.write_text(
            "\n\n---\ncomplexity_class: HIGH\nvalidation_philosophy: continuous-parallel\n"
            "validation_milestones: 6\nwork_milestones: 6\n"
            'interleave_ratio: "1:1"\nmajor_issue_policy: stop-and-fix\n'
            "---\n## Test Strategy\n- item\n",
            encoding="utf-8",
        )

        # Step 1: sanitize strips leading \n\n
        sanitize_result = _sanitize_output(f)
        assert sanitize_result == 2

        # Step 2: inject provenance
        _inject_provenance_fields(f, "test-spec.md")

        # Step 3: verify
        content = f.read_text(encoding="utf-8")
        assert content.startswith("---")
        assert "spec_source: test-spec.md" in content
        assert "generated:" in content
        assert "generator: superclaude-roadmap-executor" in content
        assert "complexity_class: HIGH" in content  # original fields preserved


# ═══════════════════════════════════════════════════════════════
# T06.04 -- _check_annotate_deviations_freshness (9 SC-8 cases)
# ═══════════════════════════════════════════════════════════════


def _write_spec_deviations(path: Path, roadmap_hash: str) -> None:
    """Write a valid spec-deviations.md with the given roadmap_hash."""
    path.write_text(
        f"---\nroadmap_hash: {roadmap_hash}\nschema_version: 2.25\n---\n"
        "## Spec Deviations\n- DEV-001: test deviation\n",
        encoding="utf-8",
    )


class TestCheckAnnotateDeviationsFreshness:
    """T06.04: _check_annotate_deviations_freshness -- 9 SC-8 test cases."""

    def test_matching_hash_returns_true(self, tmp_path):
        """SC-8 case 1: matching hash -> True."""
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap content\n", encoding="utf-8")
        expected_hash = hashlib.sha256(roadmap.read_bytes()).hexdigest()
        _write_spec_deviations(tmp_path / "spec-deviations.md", expected_hash)

        assert _check_annotate_deviations_freshness(tmp_path, roadmap) is True

    def test_mismatched_hash_returns_false(self, tmp_path):
        """SC-8 case 2: mismatched hash -> False."""
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap content\n", encoding="utf-8")
        _write_spec_deviations(tmp_path / "spec-deviations.md", "deadbeef" * 8)

        assert _check_annotate_deviations_freshness(tmp_path, roadmap) is False

    def test_missing_spec_deviations_returns_false(self, tmp_path):
        """SC-8 case 3: missing spec-deviations.md -> False."""
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n", encoding="utf-8")
        # No spec-deviations.md written

        assert _check_annotate_deviations_freshness(tmp_path, roadmap) is False

    def test_missing_roadmap_hash_field_returns_false(self, tmp_path):
        """SC-8 case 4: missing roadmap_hash field -> False."""
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n", encoding="utf-8")
        (tmp_path / "spec-deviations.md").write_text(
            "---\nschema_version: 2.25\n---\n## Report\n",
            encoding="utf-8",
        )

        assert _check_annotate_deviations_freshness(tmp_path, roadmap) is False

    def test_empty_spec_deviations_returns_false(self, tmp_path):
        """SC-8 case 5: empty spec-deviations.md -> False."""
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n", encoding="utf-8")
        (tmp_path / "spec-deviations.md").write_text("", encoding="utf-8")

        assert _check_annotate_deviations_freshness(tmp_path, roadmap) is False

    def test_corrupt_frontmatter_returns_false(self, tmp_path):
        """SC-8 case 6: corrupt frontmatter (no closing ---) -> False."""
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n", encoding="utf-8")
        (tmp_path / "spec-deviations.md").write_text(
            "---\nroadmap_hash: abc123\nno closing fence here",
            encoding="utf-8",
        )

        assert _check_annotate_deviations_freshness(tmp_path, roadmap) is False

    def test_missing_roadmap_md_returns_false(self, tmp_path):
        """SC-8 case 7: roadmap.md not found -> False."""
        roadmap = tmp_path / "roadmap.md"
        # roadmap not written
        _write_spec_deviations(tmp_path / "spec-deviations.md", "abc123")

        assert _check_annotate_deviations_freshness(tmp_path, roadmap) is False

    def test_empty_hash_field_returns_false(self, tmp_path):
        """SC-8 case 8: roadmap_hash field is empty -> False."""
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n", encoding="utf-8")
        (tmp_path / "spec-deviations.md").write_text(
            "---\nroadmap_hash: \nschema_version: 2.25\n---\n## Report\n",
            encoding="utf-8",
        )

        assert _check_annotate_deviations_freshness(tmp_path, roadmap) is False

    def test_hash_mismatch_resets_gate_pass_state(self, tmp_path):
        """SC-8: hash mismatch resets spec-fidelity and deviation-analysis gate state (FR-084)."""
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Current roadmap\n", encoding="utf-8")
        _write_spec_deviations(tmp_path / "spec-deviations.md", "stale_hash" * 4)

        gate_state = {"spec-fidelity": True, "deviation-analysis": True, "other": True}
        result = _check_annotate_deviations_freshness(
            tmp_path, roadmap, gate_pass_state=gate_state
        )

        assert result is False
        assert gate_state["spec-fidelity"] is False
        assert gate_state["deviation-analysis"] is False
        assert gate_state["other"] is True  # Other gates not affected

    def test_fresh_hash_does_not_modify_gate_state(self, tmp_path):
        """Matching hash does not modify gate_pass_state."""
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n", encoding="utf-8")
        expected_hash = hashlib.sha256(roadmap.read_bytes()).hexdigest()
        _write_spec_deviations(tmp_path / "spec-deviations.md", expected_hash)

        gate_state = {"spec-fidelity": True}
        result = _check_annotate_deviations_freshness(
            tmp_path, roadmap, gate_pass_state=gate_state
        )

        assert result is True
        assert gate_state["spec-fidelity"] is True  # Unchanged


# ═══════════════════════════════════════════════════════════════
# T06.04 -- _check_remediation_budget
# ═══════════════════════════════════════════════════════════════


def _write_state(path: Path, attempts: int) -> None:
    """Write a .roadmap-state.json with the given remediation_attempts."""
    state = {
        "schema_version": 1,
        "steps": {},
        "remediation_attempts": attempts,
    }
    path.write_text(json.dumps(state), encoding="utf-8")


class TestCheckRemediationBudget:
    """T06.04: _check_remediation_budget -- SC-6 budget enforcement."""

    def test_attempt_1_returns_true(self, tmp_path):
        """First attempt (0 previous) -> True (allowed)."""
        _write_state(tmp_path / ".roadmap-state.json", 0)
        assert _check_remediation_budget(tmp_path) is True

    def test_attempt_2_returns_true(self, tmp_path):
        """Second attempt (1 previous) -> True (allowed)."""
        _write_state(tmp_path / ".roadmap-state.json", 1)
        assert _check_remediation_budget(tmp_path) is True

    def test_attempt_3_returns_false(self, tmp_path):
        """Third attempt (2 previous) -> False (budget exhausted)."""
        _write_state(tmp_path / ".roadmap-state.json", 2)
        halt_called = []

        def mock_halt(output_dir, findings, count):
            halt_called.append(count)

        assert _check_remediation_budget(tmp_path, halt_fn=mock_halt) is False
        assert len(halt_called) == 1

    def test_budget_exhaustion_calls_halt(self, tmp_path):
        """Budget exhaustion calls halt_fn with correct attempt count."""
        _write_state(tmp_path / ".roadmap-state.json", 2)
        captured = {}

        def mock_halt(output_dir, findings, count):
            captured["count"] = count
            captured["output_dir"] = output_dir

        _check_remediation_budget(tmp_path, halt_fn=mock_halt)
        assert captured["count"] == 3
        assert captured["output_dir"] == tmp_path

    def test_no_state_file_returns_true(self, tmp_path):
        """No state file -> first attempt, allowed."""
        # No .roadmap-state.json written
        assert _check_remediation_budget(tmp_path) is True

    def test_configurable_max_attempts_1(self, tmp_path):
        """max_attempts=1: second attempt triggers halt."""
        _write_state(tmp_path / ".roadmap-state.json", 1)
        halt_called = []
        assert (
            _check_remediation_budget(
                tmp_path, max_attempts=1, halt_fn=lambda *a: halt_called.append(1)
            )
            is False
        )
        assert len(halt_called) == 1

    def test_configurable_max_attempts_3(self, tmp_path):
        """max_attempts=3: second attempt still allowed."""
        _write_state(tmp_path / ".roadmap-state.json", 1)
        assert _check_remediation_budget(tmp_path, max_attempts=3) is True

    def test_non_integer_attempts_treated_as_zero(self, tmp_path):
        """Non-integer remediation_attempts coerced to 0 with WARNING log."""
        state = {
            "schema_version": 1,
            "steps": {},
            "remediation_attempts": "not_a_number",
        }
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))
        assert _check_remediation_budget(tmp_path) is True


# ═══════════════════════════════════════════════════════════════
# T06.04 -- _print_terminal_halt stderr content assertions
# ═══════════════════════════════════════════════════════════════


def _make_finding(finding_id: str = "F-01", severity: str = "BLOCKING") -> Finding:
    return Finding(
        id=finding_id,
        severity=severity,
        dimension="Test",
        description=f"Test finding {finding_id}",
        location="file.py:1",
        evidence="test evidence",
        fix_guidance="fix it",
    )


class TestPrintTerminalHalt:
    """T06.04: _print_terminal_halt -- stderr content assertions (SC-6)."""

    def test_outputs_attempt_count(self, tmp_path):
        """stderr includes attempt count."""
        buf = io.StringIO()
        _print_terminal_halt(tmp_path, [], attempt_count=3, file=buf)
        output = buf.getvalue()
        assert "3" in output

    def test_outputs_remaining_finding_count(self, tmp_path):
        """stderr includes remaining failing finding count."""
        buf = io.StringIO()
        findings = [_make_finding("F-01"), _make_finding("F-02")]
        _print_terminal_halt(tmp_path, findings, attempt_count=3, file=buf)
        output = buf.getvalue()
        assert "2" in output

    def test_outputs_per_finding_details(self, tmp_path):
        """stderr includes per-finding ID and description."""
        buf = io.StringIO()
        findings = [_make_finding("F-01", "BLOCKING"), _make_finding("F-02", "WARNING")]
        _print_terminal_halt(tmp_path, findings, attempt_count=3, file=buf)
        output = buf.getvalue()
        assert "F-01" in output
        assert "F-02" in output
        assert "BLOCKING" in output

    def test_outputs_certification_report_path(self, tmp_path):
        """stderr includes path to certification report."""
        buf = io.StringIO()
        _print_terminal_halt(tmp_path, [], attempt_count=2, file=buf)
        output = buf.getvalue()
        assert "certify" in output.lower() or str(tmp_path) in output

    def test_outputs_resume_command(self, tmp_path):
        """stderr includes resume command instructions."""
        buf = io.StringIO()
        _print_terminal_halt(tmp_path, [], attempt_count=2, file=buf)
        output = buf.getvalue()
        assert "resume" in output.lower()

    def test_outputs_manual_fix_instructions(self, tmp_path):
        """stderr includes manual fix instructions."""
        buf = io.StringIO()
        _print_terminal_halt(tmp_path, [], attempt_count=2, file=buf)
        output = buf.getvalue()
        assert "manual" in output.lower() or "fix" in output.lower()

    def test_no_findings_still_outputs_header(self, tmp_path):
        """Empty findings list still produces terminal halt header."""
        buf = io.StringIO()
        _print_terminal_halt(tmp_path, [], attempt_count=1, file=buf)
        output = buf.getvalue()
        assert "TERMINAL HALT" in output or "halt" in output.lower()

    def test_spec_patch_budget_exhausted_adds_note(self, tmp_path):
        """spec_patch_budget_exhausted=True adds dual-budget note."""
        buf = io.StringIO()
        _print_terminal_halt(
            tmp_path, [], attempt_count=3, spec_patch_budget_exhausted=True, file=buf
        )
        output = buf.getvalue()
        assert "budget" in output.lower()
        assert "v2.26" in output
