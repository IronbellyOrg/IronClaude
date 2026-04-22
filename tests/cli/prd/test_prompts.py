"""Unit tests for superclaude.cli.prd.prompts.

Section 8.1 test plan: 4 tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.prd.models import PrdConfig
from superclaude.cli.prd.prompts import (
    _read_file,
    build_analyst_completeness_prompt,
    build_analyst_synthesis_prompt,
    build_assembly_prompt,
    build_completion_prompt,
    build_gap_filling_prompt,
    build_investigation_prompt,
    build_parse_request_prompt,
    build_preparation_prompt,
    build_qa_research_gate_prompt,
    build_qa_synthesis_gate_prompt,
    build_qualitative_qa_prompt,
    build_research_notes_prompt,
    build_scope_discovery_prompt,
    build_structural_qa_prompt,
    build_sufficiency_review_prompt,
    build_synthesis_prompt,
    build_task_file_prompt,
    build_verify_task_file_prompt,
    build_web_research_prompt,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def task_dir(tmp_path: Path) -> Path:
    """Create a minimal task directory with required fixtures."""
    td = tmp_path / "prd-test-product"
    td.mkdir()
    (td / "research").mkdir()
    (td / "synthesis").mkdir()
    (td / "qa").mkdir()

    # parsed-request.json
    (td / "parsed-request.json").write_text(
        '{"GOAL": "Test goal", "PRODUCT_NAME": "TestProduct", '
        '"PRODUCT_SLUG": "test-product", "PRD_SCOPE": "feature", '
        '"SCENARIO": "A", "WHERE": ["src/"], '
        '"WHY": "testing", "TIER_RECOMMENDATION": "standard"}',
        encoding="utf-8",
    )

    # scope-discovery-raw.md
    (td / "scope-discovery-raw.md").write_text(
        "# Scope Discovery\n\n## Project Overview\nTest project.\n",
        encoding="utf-8",
    )

    # TASK-PRD-test-product.md (task file)
    (td / "TASK-PRD-test-product.md").write_text(
        "---\nid: TASK-PRD-test-product\ntitle: Create PRD for TestProduct\n"
        "status: to-do\ncomplexity: L\ncreated_date: 2026-04-12\n"
        "type: prd-creation\ntier: standard\n---\n"
        "# Phase 1\n- [ ] Task item\n",
        encoding="utf-8",
    )

    # research-notes.md
    (td / "research-notes.md").write_text(
        "---\nDate: 2026-04-12\nScenario: A\nTier: standard\n---\n"
        "# Research Notes: TestProduct\n\n"
        "## EXISTING_FILES\n- src/main.py -- entry point\n\n"
        "## PATTERNS_AND_CONVENTIONS\n- snake_case\n\n"
        "## FEATURE_ANALYSIS\n- Auth feature\n\n"
        "## RECOMMENDED_OUTPUTS\n- PRD\n\n"
        "## SUGGESTED_PHASES\n"
        "- **Topic**: Auth\n  **Agent type**: Feature Analyst\n"
        "  **Files**: src/auth.py\n  **Output path**: research/01-auth.md\n\n"
        "## TEMPLATE_NOTES\n- Standard template\n\n"
        "## AMBIGUITIES_FOR_USER\n- None\n",
        encoding="utf-8",
    )

    return td


@pytest.fixture()
def config(task_dir: Path) -> PrdConfig:
    """A PrdConfig pointing at the test task directory."""
    skill_refs = task_dir / "refs"
    skill_refs.mkdir()
    for name in (
        "build-request-template.md",
        "agent-prompts.md",
        "synthesis-mapping.md",
        "validation-checklists.md",
        "operational-guidance.md",
    ):
        (skill_refs / name).write_text(f"# {name}\nContent.\n", encoding="utf-8")

    return PrdConfig(
        user_message="Create a PRD for TestProduct",
        product_name="TestProduct",
        product_slug="test-product",
        tier="standard",
        task_dir=task_dir,
        skill_refs_dir=skill_refs,
        output_path=task_dir / "output.md",
    )


# ---------------------------------------------------------------------------
# Tests (Section 8.1)
# ---------------------------------------------------------------------------


class TestInvestigationPromptStalenessProtocol:
    """[F-011] Verify Documentation Staleness Protocol markers in output."""

    def test_build_investigation_prompt_includes_staleness_protocol(self) -> None:
        prompt = build_investigation_prompt(
            topic="Auth system",
            agent_type="Feature Analyst",
            files=["src/auth.py", "src/middleware.py"],
            product_root="src/",
            output_path=Path("research/01-auth.md"),
        )

        assert "Documentation Staleness Protocol" in prompt
        assert "[CODE-VERIFIED]" in prompt
        assert "[CODE-CONTRADICTED]" in prompt
        assert "[UNVERIFIED]" in prompt
        assert "EXIT_RECOMMENDATION: CONTINUE" in prompt


class TestSynthesisPromptTemplateReference:
    """[F-011] Verify template path reference in synthesis prompt output."""

    def test_build_synthesis_prompt_includes_template_reference(self) -> None:
        template_path = Path("docs/docs-product/templates/prd_template.md")
        prompt = build_synthesis_prompt(
            research_files=[Path("research/01-auth.md"), Path("research/02-api.md")],
            template_sections=["S7 User Personas", "S21.1 User Stories"],
            output_path=Path("synthesis/synth-01.md"),
            template_path=template_path,
        )

        assert str(template_path) in prompt
        assert "Template reference" in prompt
        assert "EXIT_RECOMMENDATION: CONTINUE" in prompt


class TestPromptSizeUnder100KB:
    """[F-011] All 19 builders produce output < 100KB for synthetic worst-case inputs."""

    def test_prompt_size_under_100kb(self, config: PrdConfig) -> None:
        # Heavyweight tier with maximum research file count
        config.tier = "heavyweight"
        max_size = 100_000  # 100KB

        # -- Stage A builders (config-based) --
        stage_a_builders = [
            build_parse_request_prompt(config),
            build_scope_discovery_prompt(config),
            build_research_notes_prompt(config),
            build_sufficiency_review_prompt(config),
            build_task_file_prompt(config),
            build_verify_task_file_prompt(config),
            build_preparation_prompt(config),
        ]

        for i, prompt in enumerate(stage_a_builders):
            assert len(prompt) < max_size, (
                f"Stage A builder #{i} exceeds 100KB: {len(prompt)} bytes"
            )
            assert len(prompt) > 0, f"Stage A builder #{i} produced empty output"

        # -- Stage B builders (dynamic args) --
        investigation = build_investigation_prompt(
            topic="Comprehensive auth system analysis",
            agent_type="Feature Analyst",
            files=[f"src/module_{i}.py" for i in range(50)],  # worst-case file count
            product_root="src/",
            output_path=Path("research/01-auth.md"),
        )
        assert len(investigation) < max_size

        web_research = build_web_research_prompt(
            topic="Competitive landscape for developer tools",
            context="Extensive codebase findings " * 100,
            product="TestProduct",
            output_path=Path("research/web-01-competitive.md"),
        )
        assert len(web_research) < max_size

        analyst_completeness = build_analyst_completeness_prompt(config)
        assert len(analyst_completeness) < max_size

        qa_research_gate = build_qa_research_gate_prompt(config)
        assert len(qa_research_gate) < max_size

        synthesis = build_synthesis_prompt(
            research_files=[Path(f"research/{i:02d}-topic.md") for i in range(10)],
            template_sections=[f"S{i} Section {i}" for i in range(1, 25)],
            output_path=Path("synthesis/synth-01.md"),
            template_path=Path("docs/docs-product/templates/prd_template.md"),
        )
        assert len(synthesis) < max_size

        analyst_synthesis = build_analyst_synthesis_prompt(config)
        assert len(analyst_synthesis) < max_size

        qa_synthesis_gate = build_qa_synthesis_gate_prompt(config)
        assert len(qa_synthesis_gate) < max_size

        # -- Final stage builders --
        assembly = build_assembly_prompt(config)
        assert len(assembly) < max_size

        structural_qa = build_structural_qa_prompt(config)
        assert len(structural_qa) < max_size

        qualitative_qa = build_qualitative_qa_prompt(config)
        assert len(qualitative_qa) < max_size

        completion = build_completion_prompt(config)
        assert len(completion) < max_size

        gap_filling = build_gap_filling_prompt(
            failure={"area": "auth-coverage", "issue": "Missing OAuth flow", "severity": "critical"},
            config=config,
            cycle=1,
            phase="research",
        )
        assert len(gap_filling) < max_size


class TestReadFileTruncation:
    """[F-011] _read_file() truncates large content with marker text."""

    def test_read_file_truncation_at_50kb(self, tmp_path: Path) -> None:
        marker = "\n\n[TRUNCATED \u2014 file exceeds 50KB inline limit]"

        # -- File exactly at boundary (50_000 bytes) should NOT be truncated --
        exact_file = tmp_path / "exact.txt"
        exact_content = "A" * 50_000
        exact_file.write_text(exact_content, encoding="utf-8")
        result = _read_file(exact_file)
        assert result == exact_content
        assert marker not in result

        # -- File at boundary + 1 byte should be truncated --
        over_file = tmp_path / "over.txt"
        over_content = "B" * 50_001
        over_file.write_text(over_content, encoding="utf-8")
        result = _read_file(over_file)
        assert result.endswith(marker)
        assert len(result) == 50_000 + len(marker)
        assert result[:50_000] == "B" * 50_000

        # -- Small file should pass through unchanged --
        small_file = tmp_path / "small.txt"
        small_content = "hello world"
        small_file.write_text(small_content, encoding="utf-8")
        result = _read_file(small_file)
        assert result == small_content
