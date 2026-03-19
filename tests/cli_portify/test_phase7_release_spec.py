"""Phase 7 tests — Release Spec Synthesis.

Covers:
- T07.01: load_release_spec_template(), create_working_copy() (R-048, AC-009)
- T07.02: execute_release_spec_synthesis_step() — 4-substep synthesis (R-049, FR-027)
- T07.03: scan_for_placeholders(), G-010 gate, portify-release-spec.md emission (R-050)
- T07.04: build_release_spec_prompt() inline embed guard (R-051, OQ-008),
           _EMBED_SIZE_LIMIT constant, CONTENT_TOO_LARGE in STEP_REGISTRY timeout,
           timeout_s=900 for release-spec-synthesis
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.cli_portify.executor import (
    STEP_REGISTRY,
    execute_release_spec_synthesis_step,
    scan_for_placeholders,
)
from superclaude.cli.cli_portify.models import (
    CONTENT_TOO_LARGE,
    BrainstormFinding,
    PortifyStatus,
    PortifyValidationError,
)
from superclaude.cli.cli_portify.prompts import (
    _EMBED_SIZE_LIMIT,
    build_brainstorm_prompt,
    build_release_spec_prompt,
    build_section_population_prompt,
    create_working_copy,
    incorporate_findings,
    load_release_spec_template,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent.parent


def _make_finding(
    gap_id: str = "GAP-001",
    description: str = "Test gap",
    severity: str = "MINOR",
    affected_section: str = "3",
    persona: str = "architect",
) -> BrainstormFinding:
    return BrainstormFinding(
        gap_id=gap_id,
        description=description,
        severity=severity,
        affected_section=affected_section,
        persona=persona,
    )


# ---------------------------------------------------------------------------
# T07.01: load_release_spec_template and create_working_copy
# ---------------------------------------------------------------------------


class TestLoadReleaseSpecTemplate:
    """T07.01 — Template loader (R-048, AC-009)."""

    def test_release_spec_template_loads_from_real_path(self):
        """load_release_spec_template() returns non-empty string from real template."""
        content = load_release_spec_template(REPO_ROOT)
        assert isinstance(content, str)
        assert len(content) > 0

    def test_release_spec_template_has_placeholders(self):
        """Template has ≥13 {{SC_PLACEHOLDER:*}} sentinels confirmed."""
        content = load_release_spec_template(REPO_ROOT)
        count = content.count("{{SC_PLACEHOLDER:")
        assert count >= 13, f"Expected ≥13 placeholders, found {count}"

    def test_release_spec_template_missing_raises_invalid_path(self, tmp_path):
        """load_release_spec_template() raises PortifyValidationError(INVALID_PATH) when absent."""
        fake_root = tmp_path / "fake_project"
        fake_root.mkdir()
        with pytest.raises(PortifyValidationError) as exc_info:
            load_release_spec_template(fake_root)
        assert exc_info.value.error_code == "INVALID_PATH"

    def test_release_spec_template_error_message_contains_path(self, tmp_path):
        """Error message includes the missing template path."""
        fake_root = tmp_path / "fake_project"
        fake_root.mkdir()
        with pytest.raises(PortifyValidationError, match="release-spec-template"):
            load_release_spec_template(fake_root)


class TestCreateWorkingCopy:
    """T07.01 — Working copy creation (R-048)."""

    def test_working_copy_written_to_workdir(self, tmp_path):
        """create_working_copy() writes release-spec-working.md to workdir."""
        template = "# Template\n{{SC_PLACEHOLDER:section1}}\n"
        path = create_working_copy(template, tmp_path)
        assert path.name == "release-spec-working.md"
        assert path.exists()

    def test_working_copy_byte_identical_to_template(self, tmp_path):
        """Working copy content is byte-identical to source template."""
        template = "# Template\n{{SC_PLACEHOLDER:section1}}\nMore content.\n"
        path = create_working_copy(template, tmp_path)
        assert path.read_text(encoding="utf-8") == template

    def test_working_copy_creates_workdir_if_missing(self, tmp_path):
        """create_working_copy() creates workdir if it doesn't exist."""
        nested = tmp_path / "nested" / "workdir"
        # Directory does not exist yet
        create_working_copy("content", nested)
        assert (nested / "release-spec-working.md").exists()

    def test_working_copy_path_returned(self, tmp_path):
        """Return value is the Path to the working copy."""
        result = create_working_copy("# Template", tmp_path)
        assert isinstance(result, Path)
        assert result == tmp_path / "release-spec-working.md"


# ---------------------------------------------------------------------------
# T07.03: scan_for_placeholders
# ---------------------------------------------------------------------------


class TestScanForPlaceholders:
    """T07.03 — Placeholder scanner (FR-028)."""

    def test_no_placeholders_returns_empty_list(self):
        """Clean content returns empty list."""
        result = scan_for_placeholders("No placeholders here.\nAll good.")
        assert result == []

    def test_detects_single_placeholder(self):
        """Single placeholder returns its name."""
        result = scan_for_placeholders("Content with {{SC_PLACEHOLDER:INTRO}} here.")
        assert result == ["INTRO"]

    def test_detects_multiple_placeholders(self):
        """Multiple distinct placeholders are all detected."""
        content = "{{SC_PLACEHOLDER:TITLE}}\n{{SC_PLACEHOLDER:VERSION}}\n{{SC_PLACEHOLDER:AUTHOR}}"
        result = scan_for_placeholders(content)
        assert "TITLE" in result
        assert "VERSION" in result
        assert "AUTHOR" in result
        assert len(result) == 3

    def test_placeholder_names_extracted_correctly(self):
        """Names after SC_PLACEHOLDER: are extracted verbatim."""
        result = scan_for_placeholders("{{SC_PLACEHOLDER:spec_title}}")
        assert result == ["spec_title"]

    def test_content_with_placeholder_raises_on_spec_emit(self, tmp_path):
        """A content containing placeholders should not pass G-010 in synthesis step."""

        # Simulate a process_runner that writes content with a placeholder
        def process_runner(prompt: str, output_path: Path):
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text("{{SC_PLACEHOLDER:INTRO}}", encoding="utf-8")
            return 0, "EXIT_RECOMMENDATION: CONTINUE", False

        # Create fake portify-spec.md to satisfy the executor
        (tmp_path / "portify-spec.md").write_text(
            "## Step Mapping\n- step1\n", encoding="utf-8"
        )

        result = execute_release_spec_synthesis_step(
            "test-cli",
            tmp_path,
            project_root=REPO_ROOT,
            process_runner=process_runner,
        )
        # Should fail because the draft still has placeholders
        assert result.portify_status == PortifyStatus.ERROR
        assert (
            "Placeholder" in result.error_message
            or "placeholder" in result.error_message.lower()
        )


# ---------------------------------------------------------------------------
# T07.02: BrainstormFinding dataclass
# ---------------------------------------------------------------------------


class TestBrainstormFinding:
    """T07.02 — BrainstormFinding importable from models (FR-027)."""

    def test_brainstorm_finding_importable(self):
        """BrainstormFinding is importable from superclaude.cli.cli_portify.models."""
        assert BrainstormFinding is not None

    def test_brainstorm_finding_has_required_fields(self):
        """BrainstormFinding has all required fields: gap_id, description, severity,
        affected_section, persona."""
        f = BrainstormFinding(
            gap_id="GAP-001",
            description="Missing timeout handling",
            severity="CRITICAL",
            affected_section="4",
            persona="architect",
        )
        assert f.gap_id == "GAP-001"
        assert f.description == "Missing timeout handling"
        assert f.severity == "CRITICAL"
        assert f.affected_section == "4"
        assert f.persona == "architect"

    def test_brainstorm_finding_default_severity_is_minor(self):
        """Default severity is MINOR."""
        f = BrainstormFinding()
        assert f.severity == "MINOR"


# ---------------------------------------------------------------------------
# T07.02: build_section_population_prompt and build_brainstorm_prompt
# ---------------------------------------------------------------------------


class TestSectionPopulationPrompt:
    """T07.02 — Section population prompt builder."""

    def test_build_section_population_prompt_returns_string(self):
        result = build_section_population_prompt(
            working_copy="# Working Copy\n{{SC_PLACEHOLDER:INTRO}}",
            portify_spec="# Portify Spec\nstep-1: do stuff",
            analysis_report="# Analysis\nComponent: foo",
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_build_section_population_prompt_contains_exit_recommendation(self):
        result = build_section_population_prompt("template", "spec", "report")
        assert "EXIT_RECOMMENDATION" in result

    def test_build_section_population_prompt_includes_working_copy(self):
        result = build_section_population_prompt(
            working_copy="MY_WORKING_COPY_MARKER", portify_spec="", analysis_report=""
        )
        assert "MY_WORKING_COPY_MARKER" in result


class TestBrainstormPrompt:
    """T07.02 — Per-persona brainstorm prompt builder."""

    @pytest.mark.parametrize("persona", ["architect", "analyzer", "backend"])
    def test_build_brainstorm_prompt_for_each_persona(self, persona):
        """Prompts are distinct for each of the 3 personas."""
        result = build_brainstorm_prompt("# Draft", persona)
        assert isinstance(result, str)
        assert persona in result

    def test_brainstorm_prompt_contains_json_schema_hint(self):
        """Prompt includes gap_id, description, severity, affected_section, persona fields."""
        result = build_brainstorm_prompt("# Draft", "architect")
        assert "gap_id" in result
        assert "severity" in result
        assert "affected_section" in result

    def test_brainstorm_prompt_contains_exit_recommendation(self):
        result = build_brainstorm_prompt("# Draft", "architect")
        assert "EXIT_RECOMMENDATION" in result


# ---------------------------------------------------------------------------
# T07.02: incorporate_findings
# ---------------------------------------------------------------------------


class TestIncorporateFindings:
    """T07.02 — Finding incorporation (FR-027, substep 3d)."""

    def test_critical_finding_goes_to_body(self):
        """CRITICAL findings with affected_section are inserted into body."""
        draft = "# Section 1\nSome content.\n"
        findings = [_make_finding(severity="CRITICAL", affected_section="1")]
        result = incorporate_findings(draft, findings)
        assert "GAP-001" in result
        assert "CRITICAL" in result

    def test_major_finding_goes_to_body(self):
        """MAJOR findings with affected_section are inserted into body."""
        draft = "# Section 2\nContent.\n"
        findings = [_make_finding(severity="MAJOR", affected_section="2")]
        result = incorporate_findings(draft, findings)
        assert "MAJOR" in result

    def test_minor_finding_goes_to_section12(self):
        """MINOR findings without affected resolution go to Section 12 table."""
        draft = "# Section 1\nContent.\n"
        findings = [_make_finding(severity="MINOR", affected_section="")]
        result = incorporate_findings(draft, findings)
        assert "GAP-001" in result

    def test_unresolvable_finding_routes_to_section12(self):
        """Findings without affected_section always route to Section 12."""
        draft = "# Section 1\nContent.\n"
        findings = [_make_finding(severity="CRITICAL", affected_section="")]
        result = incorporate_findings(draft, findings)
        assert "GAP-001" in result

    def test_empty_findings_returns_draft_unchanged(self):
        """No findings → draft returned unchanged."""
        draft = "# Spec\nContent without gaps.\n"
        result = incorporate_findings(draft, [])
        assert result == draft

    def test_multiple_findings_from_multiple_personas(self):
        """Multiple findings from all 3 personas are all incorporated."""
        draft = "# Section 1\nContent.\n"
        findings = [
            _make_finding("GAP-001", "Arch gap", "CRITICAL", "1", "architect"),
            _make_finding("GAP-002", "Analyzer gap", "MAJOR", "1", "analyzer"),
            _make_finding("GAP-003", "Backend gap", "MINOR", "", "backend"),
        ]
        result = incorporate_findings(draft, findings)
        assert "GAP-001" in result
        assert "GAP-002" in result
        assert "GAP-003" in result


# ---------------------------------------------------------------------------
# T07.04: build_release_spec_prompt — inline embed guard
# ---------------------------------------------------------------------------


class TestBuildReleaseSpecPrompt:
    """T07.04 — Inline embed guard (R-051, OQ-008)."""

    def test_embed_size_limit_constant_is_120kb(self):
        """_EMBED_SIZE_LIMIT is exactly 120 * 1024 bytes."""
        assert _EMBED_SIZE_LIMIT == 120 * 1024

    def test_content_under_limit_returns_prompt(self):
        """Content of 100 KiB passes and returns a prompt string."""
        content = "A" * (100 * 1024)
        result = build_release_spec_prompt(content)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_content_over_limit_raises_content_too_large(self):
        """Content of 121 KiB raises PortifyValidationError(CONTENT_TOO_LARGE)."""
        content = "A" * (121 * 1024)
        with pytest.raises(PortifyValidationError) as exc_info:
            build_release_spec_prompt(content)
        assert exc_info.value.error_code == CONTENT_TOO_LARGE

    def test_content_exactly_at_limit_passes(self):
        """Content of exactly _EMBED_SIZE_LIMIT bytes passes."""
        content = "A" * _EMBED_SIZE_LIMIT
        result = build_release_spec_prompt(content)
        assert isinstance(result, str)

    def test_content_one_over_limit_raises(self):
        """Content of _EMBED_SIZE_LIMIT + 1 raises."""
        content = "A" * (_EMBED_SIZE_LIMIT + 1)
        with pytest.raises(PortifyValidationError) as exc_info:
            build_release_spec_prompt(content)
        assert exc_info.value.error_code == CONTENT_TOO_LARGE

    def test_error_message_contains_size(self):
        """Error message includes the content size."""
        content = "A" * (121 * 1024)
        with pytest.raises(PortifyValidationError) as exc_info:
            build_release_spec_prompt(content)
        assert str(len(content)) in str(exc_info.value)

    def test_prompt_does_not_contain_file_flag(self):
        """--file flag MUST NOT appear in prompt output (OQ-008 amendment)."""
        content = "Small content for testing"
        result = build_release_spec_prompt(content)
        assert "--file" not in result

    def test_prompt_contains_inline_template_content(self):
        """Prompt contains the template content inline (not by reference)."""
        content = "MY_INLINE_MARKER_CONTENT"
        result = build_release_spec_prompt(content)
        assert "MY_INLINE_MARKER_CONTENT" in result


# ---------------------------------------------------------------------------
# T07.04: STEP_REGISTRY — 900s timeout
# ---------------------------------------------------------------------------


class TestStepRegistryTimeout:
    """T07.04 — release-spec-synthesis has 900s timeout (R-051, NFR-001)."""

    def test_release_spec_synthesis_in_step_registry(self):
        """release-spec-synthesis step is registered."""
        assert "release-spec-synthesis" in STEP_REGISTRY

    def test_release_spec_synthesis_timeout_is_900s(self):
        """timeout_s = 900 for release-spec-synthesis."""
        assert STEP_REGISTRY["release-spec-synthesis"]["timeout_s"] == 900

    def test_release_spec_synthesis_phase_type_is_synthesis(self):
        """Phase type is SYNTHESIS."""
        from superclaude.cli.cli_portify.models import PortifyPhaseType

        assert (
            STEP_REGISTRY["release-spec-synthesis"]["phase_type"]
            == PortifyPhaseType.SYNTHESIS
        )


# ---------------------------------------------------------------------------
# T07.02 + T07.03: execute_release_spec_synthesis_step integration
# ---------------------------------------------------------------------------


class TestExecuteReleaseSpecSynthesisStep:
    """T07.02/T07.03 — Full synthesis step execution."""

    def _make_runner_with_section12(self, draft_content: str):
        """Make a process_runner that writes a section-12-containing draft."""

        def runner(prompt: str, output_path: Path) -> tuple[int, str, bool]:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(draft_content, encoding="utf-8")
            return 0, "EXIT_RECOMMENDATION: CONTINUE", False

        return runner

    def _setup_workdir(self, tmp_path: Path) -> None:
        """Write minimal required artifacts to workdir."""
        (tmp_path / "portify-spec.md").write_text(
            "## Step Mapping\n- step1\n- step2\n", encoding="utf-8"
        )
        (tmp_path / "portify-analysis-report.md").write_text(
            "## Source Components\nComponent: test\n", encoding="utf-8"
        )

    def test_synthesis_step_returns_pass_with_section12(self, tmp_path):
        """Step returns PASS when draft has no placeholders and Section 12."""
        self._setup_workdir(tmp_path)
        draft_content = "# Spec\nNo placeholders here.\n\n## 12. Brainstorm Gap Analysis\n\nSome content.\n"
        runner = self._make_runner_with_section12(draft_content)
        result = execute_release_spec_synthesis_step(
            "test-cli", tmp_path, project_root=REPO_ROOT, process_runner=runner
        )
        assert result.portify_status == PortifyStatus.PASS

    def test_synthesis_step_emits_portify_release_spec(self, tmp_path):
        """portify-release-spec.md is written to workdir on success."""
        self._setup_workdir(tmp_path)
        draft_content = (
            "# Spec\nNo placeholders.\n\n## 12. Brainstorm Gap Analysis\n\nGood.\n"
        )
        runner = self._make_runner_with_section12(draft_content)
        execute_release_spec_synthesis_step(
            "test-cli", tmp_path, project_root=REPO_ROOT, process_runner=runner
        )
        assert (tmp_path / "portify-release-spec.md").exists()

    def test_synthesis_step_emitted_spec_has_frontmatter(self, tmp_path):
        """portify-release-spec.md contains YAML frontmatter with title, status, quality_scores."""
        self._setup_workdir(tmp_path)
        draft_content = (
            "# Spec\nNo placeholders.\n\n## 12. Brainstorm Gap Analysis\n\nContent.\n"
        )
        runner = self._make_runner_with_section12(draft_content)
        execute_release_spec_synthesis_step(
            "test-cli", tmp_path, project_root=REPO_ROOT, process_runner=runner
        )
        content = (tmp_path / "portify-release-spec.md").read_text(encoding="utf-8")
        assert "title:" in content
        assert "status:" in content
        assert "quality_scores:" in content

    def test_synthesis_step_fails_without_section12(self, tmp_path):
        """Step returns ERROR if Section 12 is absent (G-010 gate)."""
        self._setup_workdir(tmp_path)
        draft_content = "# Spec\nNo placeholders. But missing Section 12.\n"
        runner = self._make_runner_with_section12(draft_content)
        result = execute_release_spec_synthesis_step(
            "test-cli", tmp_path, project_root=REPO_ROOT, process_runner=runner
        )
        assert result.portify_status == PortifyStatus.ERROR

    def test_synthesis_step_fails_on_timeout(self, tmp_path):
        """Step returns TIMEOUT when process_runner signals timeout."""
        self._setup_workdir(tmp_path)

        def timeout_runner(prompt: str, output_path: Path):
            return 124, "", True

        result = execute_release_spec_synthesis_step(
            "test-cli", tmp_path, project_root=REPO_ROOT, process_runner=timeout_runner
        )
        assert result.portify_status == PortifyStatus.TIMEOUT

    def test_synthesis_step_fails_on_nonzero_exit(self, tmp_path):
        """Step returns ERROR when process_runner returns non-zero exit."""
        self._setup_workdir(tmp_path)

        def error_runner(prompt: str, output_path: Path):
            return 1, "", False

        result = execute_release_spec_synthesis_step(
            "test-cli", tmp_path, project_root=REPO_ROOT, process_runner=error_runner
        )
        assert result.portify_status == PortifyStatus.ERROR

    def test_synthesis_step_creates_working_copy(self, tmp_path):
        """release-spec-working.md is created as substep 3a."""
        self._setup_workdir(tmp_path)
        draft_content = "# Spec\nContent.\n\n## 12. Brainstorm Gap Analysis\n\nGood.\n"
        runner = self._make_runner_with_section12(draft_content)
        execute_release_spec_synthesis_step(
            "test-cli", tmp_path, project_root=REPO_ROOT, process_runner=runner
        )
        assert (tmp_path / "release-spec-working.md").exists()

    def test_synthesis_step_step_name_is_correct(self, tmp_path):
        """Result step_name == 'release-spec-synthesis'."""
        self._setup_workdir(tmp_path)
        draft_content = "# Spec\nContent.\n\n## 12. Brainstorm Gap Analysis\n\nGood.\n"
        runner = self._make_runner_with_section12(draft_content)
        result = execute_release_spec_synthesis_step(
            "test-cli", tmp_path, project_root=REPO_ROOT, process_runner=runner
        )
        assert result.step_name == "release-spec-synthesis"

    def test_synthesis_step_gate_tier_is_strict(self, tmp_path):
        """Gate tier is STRICT for the release-spec-synthesis step."""
        self._setup_workdir(tmp_path)
        draft_content = "# Spec\nContent.\n\n## 12. Brainstorm Gap Analysis\n\nGood.\n"
        runner = self._make_runner_with_section12(draft_content)
        result = execute_release_spec_synthesis_step(
            "test-cli", tmp_path, project_root=REPO_ROOT, process_runner=runner
        )
        assert result.gate_tier == "STRICT"

    def test_synthesis_step_iteration_timeout_is_900(self, tmp_path):
        """iteration_timeout reflects 900s from STEP_REGISTRY."""
        self._setup_workdir(tmp_path)
        draft_content = "# Spec\nContent.\n\n## 12. Brainstorm Gap Analysis\n\nGood.\n"
        runner = self._make_runner_with_section12(draft_content)
        result = execute_release_spec_synthesis_step(
            "test-cli", tmp_path, project_root=REPO_ROOT, process_runner=runner
        )
        assert result.iteration_timeout == 900
