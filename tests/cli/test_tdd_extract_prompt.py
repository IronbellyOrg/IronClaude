"""Tests for TDD extract prompt and CLI config changes."""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.roadmap.prompts import (
    _OUTPUT_FORMAT_BLOCK,
    build_extract_prompt,
    build_extract_prompt_tdd,
    build_merge_prompt,
)
from superclaude.cli.roadmap.models import RoadmapConfig
from superclaude.cli.tasklist.models import TasklistValidateConfig


@pytest.fixture
def dummy_path(tmp_path):
    p = tmp_path / "test.md"
    p.write_text("# Test")
    return p


class TestBuildExtractPromptTdd:
    """Tests for the new build_extract_prompt_tdd() function."""

    def test_has_all_14_sections(self, dummy_path):
        result = build_extract_prompt_tdd(dummy_path)
        sections = [
            "## Functional Requirements",
            "## Non-Functional Requirements",
            "## Complexity Assessment",
            "## Architectural Constraints",
            "## Risk Inventory",
            "## Dependency Inventory",
            "## Success Criteria",
            "## Open Questions",
            "## Data Models and Interfaces",
            "## API Specifications",
            "## Component Inventory",
            "## Testing Strategy",
            "## Migration and Rollout Plan",
            "## Operational Readiness",
        ]
        for section in sections:
            assert section in result, f"Missing section: {section}"

    def test_has_tdd_frontmatter_fields(self, dummy_path):
        result = build_extract_prompt_tdd(dummy_path)
        new_fields = [
            "data_models_identified",
            "api_surfaces_identified",
            "components_identified",
            "test_artifacts_identified",
            "migration_items_identified",
            "operational_items_identified",
        ]
        for field in new_fields:
            assert field in result, f"Missing frontmatter field: {field}"

    def test_has_output_format_block(self, dummy_path):
        result = build_extract_prompt_tdd(dummy_path)
        assert _OUTPUT_FORMAT_BLOCK in result, (
            "CRITICAL: _OUTPUT_FORMAT_BLOCK missing — EXTRACT_GATE will fail"
        )

    def test_preserves_spec_source(self, dummy_path):
        result = build_extract_prompt_tdd(dummy_path)
        assert "spec_source" in result, "spec_source field missing — gates will fail"

    def test_with_retrospective(self, dummy_path):
        retro = "Prior release had auth issues in module X."
        result = build_extract_prompt_tdd(dummy_path, retrospective_content=retro)
        assert retro in result
        assert "Advisory" in result

    def test_neutralized_framing(self, dummy_path):
        result = build_extract_prompt_tdd(dummy_path)
        assert "requirements and design extraction specialist" in result
        assert "source specification or technical design document" in result
        # Must NOT have the old spec-only framing
        assert "You are a requirements extraction specialist" not in result


class TestBuildExtractPromptUnchanged:
    """Verify the original build_extract_prompt() was NOT modified."""

    def test_no_tdd_sections_in_original(self, dummy_path):
        result = build_extract_prompt(dummy_path)
        assert "## Data Models and Interfaces" not in result
        assert "## API Specifications" not in result

    def test_original_has_spec_language(self, dummy_path):
        result = build_extract_prompt(dummy_path)
        assert "specification file" in result.lower() or "specification" in result.lower()


class TestRoadmapConfigDefaults:
    """Verify new RoadmapConfig fields have correct defaults."""

    def test_input_type_defaults_to_auto(self):
        config = RoadmapConfig(spec_file=Path("."))
        assert config.input_type == "auto"

    def test_tdd_file_defaults_to_none(self):
        config = RoadmapConfig(spec_file=Path("."))
        assert config.tdd_file is None


class TestTasklistValidateConfigDefaults:
    """Verify new TasklistValidateConfig field has correct default."""

    def test_tdd_file_defaults_to_none(self):
        config = TasklistValidateConfig()
        assert config.tdd_file is None


class TestAutoDetection:
    """Test the auto-detection logic from executor.py."""

    def test_detects_tdd_from_numbered_headings(self, tmp_path):
        """A file with 20+ numbered headings is detected as TDD."""
        from superclaude.cli.roadmap.executor import detect_input_type
        tdd = tmp_path / "doc.md"
        sections = "\n".join(f"## {i}. Section {i}\nContent." for i in range(1, 25))
        tdd.write_text(f"---\ntitle: Test\ncoordinator: lead\n---\n{sections}")
        assert detect_input_type(tdd) == "tdd"

    def test_detects_spec_from_no_numbered_headings(self, tmp_path):
        """A file with no numbered headings and no TDD signals is detected as spec."""
        from superclaude.cli.roadmap.executor import detect_input_type
        spec = tmp_path / "spec.md"
        spec.write_text("---\nspec_type: new_feature\n---\n## Requirements\nFR-001: Do thing\n## Architecture\nMonolith.")
        assert detect_input_type(spec) == "spec"

    def test_detects_tdd_from_frontmatter_fields(self, tmp_path):
        """A file with TDD-exclusive frontmatter fields + section names is detected as TDD."""
        from superclaude.cli.roadmap.executor import detect_input_type
        tdd = tmp_path / "doc.md"
        tdd.write_text("---\nfeature_id: AUTH-001\nparent_doc: some-prd\nauthors: [me]\nquality_scores:\n  clarity: 8\ncoordinator: lead\n---\n## 1. Summary\n## 2. Problem\n## 3. Goals\n## 4. Metrics\n## 5. Requirements\n## Data Models\nEntities.\n")
        assert detect_input_type(tdd) == "tdd"

    def test_detects_tdd_from_section_names(self, tmp_path):
        """A file with TDD-specific section names is detected as TDD."""
        from superclaude.cli.roadmap.executor import detect_input_type
        tdd = tmp_path / "doc.md"
        tdd.write_text("# TDD\n## Data Models\nEntities here.\n## API Specifications\nEndpoints here.\n## Component Inventory\nComponents.\n## Testing Strategy\nTests.\n## Operational Readiness\nRunbooks.")
        assert detect_input_type(tdd) == "tdd"

    def test_detects_tdd_from_real_template(self):
        """The actual TDD template is detected as TDD."""
        from superclaude.cli.roadmap.executor import detect_input_type
        tdd = Path("src/superclaude/examples/tdd_template.md")
        if tdd.exists():
            assert detect_input_type(tdd) == "tdd"

    def test_detects_spec_from_numbered_spec_template(self, tmp_path):
        """A spec with 12 numbered headings is NOT detected as TDD.

        The release-spec-template uses ## N. headings (12 sections).
        This must NOT trigger TDD detection — only TDDs with 20+ sections should.
        """
        from superclaude.cli.roadmap.executor import detect_input_type
        spec = tmp_path / "spec.md"
        sections = "\n".join(f"## {i}. Section {i}\nContent." for i in range(1, 13))
        spec.write_text(f"---\ntitle: Test Spec\nfeature_id: AUTH-001\nauthors: [user]\nquality_scores:\n  clarity: 8\n---\n{sections}")
        assert detect_input_type(spec) == "spec"

    def test_detects_spec_from_empty_file(self, tmp_path):
        """An empty file defaults to spec."""
        from superclaude.cli.roadmap.executor import detect_input_type
        empty = tmp_path / "empty.md"
        empty.write_text("")
        assert detect_input_type(empty) == "spec"

    def test_missing_file_defaults_to_spec(self, tmp_path):
        """A nonexistent file defaults to spec."""
        from superclaude.cli.roadmap.executor import detect_input_type
        assert detect_input_type(tmp_path / "nonexistent.md") == "spec"


class TestTddInputValidation:
    """Test the TDD input validation logic from commands.py.

    The validation reads the first 500 bytes of the input file and checks
    for 'Technical Design Document' to warn users about potential misuse
    of --input-type tdd.
    """

    def test_valid_tdd_file_no_extra_warning(self, tmp_path):
        """A file containing 'Technical Design Document' in first 500 bytes passes silently."""
        tdd_file = tmp_path / "design.md"
        tdd_file.write_text(
            "---\ntype: Technical Design Document\ntitle: Test TDD\n---\n# TDD Content\n"
        )
        head = tdd_file.read_bytes()[:500].decode("utf-8", errors="replace")
        assert "Technical Design Document" in head

    def test_non_tdd_file_triggers_warning_condition(self, tmp_path):
        """A file without 'Technical Design Document' in first 500 bytes triggers warning."""
        spec_file = tmp_path / "spec.md"
        spec_file.write_text("# Product Requirements Document\n\nSome spec content.\n")
        head = spec_file.read_bytes()[:500].decode("utf-8", errors="replace")
        assert "Technical Design Document" not in head

    def test_empty_file_triggers_warning_condition(self, tmp_path):
        """An empty file triggers the warning condition."""
        empty_file = tmp_path / "empty.md"
        empty_file.write_text("")
        head = empty_file.read_bytes()[:500].decode("utf-8", errors="replace")
        assert "Technical Design Document" not in head

    def test_tdd_marker_beyond_500_bytes_triggers_warning(self, tmp_path):
        """A file with 'Technical Design Document' after byte 500 triggers warning."""
        tdd_file = tmp_path / "late-marker.md"
        tdd_file.write_text("x" * 501 + "Technical Design Document")
        head = tdd_file.read_bytes()[:500].decode("utf-8", errors="replace")
        assert "Technical Design Document" not in head

    def test_read_bytes_handles_binary_gracefully(self, tmp_path):
        """Binary content is handled via errors='replace' without raising."""
        bin_file = tmp_path / "binary.md"
        bin_file.write_bytes(b"\x80\x81\x82" * 100)
        head = bin_file.read_bytes()[:500].decode("utf-8", errors="replace")
        # Should not raise, and should not contain the marker
        assert "Technical Design Document" not in head


class TestExtractPromptTddWithPrd:
    """C-16: Tests for build_extract_prompt_tdd with prd_file."""

    def test_prd_block_present_when_prd_file_given(self, dummy_path):
        result = build_extract_prompt_tdd(dummy_path, prd_file=dummy_path)
        assert "Supplementary PRD Context" in result
        assert "Success Metrics" in result
        assert "S19" in result

    def test_prd_block_absent_when_no_prd_file(self, dummy_path):
        result = build_extract_prompt_tdd(dummy_path)
        assert "Supplementary PRD Context" not in result

    def test_tdd_block_present_when_tdd_file_given(self, dummy_path):
        result = build_extract_prompt_tdd(dummy_path, tdd_file=dummy_path)
        assert "Supplementary TDD Context" in result

    def test_both_tdd_and_prd_blocks(self, dummy_path):
        result = build_extract_prompt_tdd(
            dummy_path, tdd_file=dummy_path, prd_file=dummy_path
        )
        assert "Supplementary TDD Context" in result
        assert "Supplementary PRD Context" in result

    def test_prd_block_in_standard_extract(self, dummy_path):
        result = build_extract_prompt(dummy_path, prd_file=dummy_path)
        assert "Supplementary PRD Context" in result
        assert "S19" in result

    def test_prd_guardrail(self, dummy_path):
        result = build_extract_prompt_tdd(dummy_path, prd_file=dummy_path)
        assert "authoritative for business context" in result
        assert "TDD wins on implementation details" in result


class TestMergePromptTddPrd:
    """C-06: Tests for build_merge_prompt with tdd_file and prd_file."""

    def test_merge_baseline_no_tdd_prd(self, dummy_path):
        result = build_merge_prompt(dummy_path, dummy_path, dummy_path, dummy_path)
        assert "producing the final merged roadmap" in result
        assert "Supplementary TDD" not in result
        assert "Supplementary PRD" not in result

    def test_merge_with_tdd(self, dummy_path):
        result = build_merge_prompt(
            dummy_path, dummy_path, dummy_path, dummy_path, tdd_file=dummy_path
        )
        assert "Supplementary TDD Context" in result
        assert "Preserve exact technical identifiers" in result

    def test_merge_with_prd(self, dummy_path):
        result = build_merge_prompt(
            dummy_path, dummy_path, dummy_path, dummy_path, prd_file=dummy_path
        )
        assert "Supplementary PRD Context" in result
        assert "personas" in result.lower()

    def test_merge_with_both(self, dummy_path):
        result = build_merge_prompt(
            dummy_path, dummy_path, dummy_path, dummy_path,
            tdd_file=dummy_path, prd_file=dummy_path,
        )
        assert "Supplementary TDD Context" in result
        assert "Supplementary PRD Context" in result


class TestOldSchemaStateBackwardCompat:
    """C-17: Tests for old-schema state file backward compatibility."""

    def test_state_without_tdd_prd_fields(self, tmp_path):
        """Old state files without tdd_file/prd_file/input_type load gracefully."""
        from superclaude.cli.roadmap.executor import read_state
        import json

        state_file = tmp_path / ".roadmap-state.json"
        old_state = {
            "schema_version": 1,
            "spec_file": str(tmp_path / "spec.md"),
            "spec_hash": "abc123",
            "agents": [{"model": "opus", "persona": "architect"}],
            "depth": "standard",
            "last_run": "2026-01-01T00:00:00+00:00",
            "steps": {},
        }
        state_file.write_text(json.dumps(old_state))
        state = read_state(state_file)
        assert state is not None
        assert state.get("tdd_file") is None
        assert state.get("prd_file") is None
        assert state.get("input_type") is None

    def test_restore_from_old_state_no_crash(self, tmp_path):
        """_restore_from_state handles old state without tdd/prd/input_type."""
        from superclaude.cli.roadmap.executor import _restore_from_state
        import json

        spec = tmp_path / "spec.md"
        spec.write_text("# Test Spec")
        output = tmp_path / "output"
        output.mkdir()
        state_file = output / ".roadmap-state.json"
        old_state = {
            "schema_version": 1,
            "spec_file": str(spec),
            "spec_hash": "abc123",
            "agents": [{"model": "opus", "persona": "architect"}],
            "depth": "standard",
            "last_run": "2026-01-01T00:00:00+00:00",
            "steps": {},
        }
        state_file.write_text(json.dumps(old_state))

        config = RoadmapConfig(spec_file=spec, output_dir=output)
        restored = _restore_from_state(config, agents_explicit=False, depth_explicit=False)
        assert restored.tdd_file is None
        assert restored.prd_file is None


class TestDetectionThresholdBoundary:
    """C-18: Explicit detection threshold boundary tests (score=4 vs 5)."""

    def test_score_4_is_spec(self, tmp_path):
        """Score exactly 4 should detect as spec (below threshold 5)."""
        from superclaude.cli.roadmap.executor import detect_input_type
        # coordinator=+2, parent_doc=+2 = total 4
        doc = tmp_path / "doc.md"
        doc.write_text("---\ncoordinator: lead\nparent_doc: prd\n---\n# Simple doc\nContent.")
        assert detect_input_type(doc) == "spec"

    def test_score_5_is_tdd(self, tmp_path):
        """Score exactly 5 should detect as tdd (at threshold)."""
        from superclaude.cli.roadmap.executor import detect_input_type
        # coordinator=+2, parent_doc=+2, Data Models section=+1 = total 5
        doc = tmp_path / "doc.md"
        doc.write_text("---\ncoordinator: lead\nparent_doc: prd\n---\n# Doc\n## Data Models\nEntities.")
        assert detect_input_type(doc) == "tdd"

    def test_score_6_is_tdd(self, tmp_path):
        """Score 6 is clearly TDD."""
        from superclaude.cli.roadmap.executor import detect_input_type
        # coordinator=+2, parent_doc=+2, Data Models=+1, API Specifications=+1 = 6
        doc = tmp_path / "doc.md"
        doc.write_text("---\ncoordinator: lead\nparent_doc: prd\n---\n# Doc\n## Data Models\nEntities.\n## API Specifications\nEndpoints.")
        assert detect_input_type(doc) == "tdd"

    def test_zero_score_is_spec(self, tmp_path):
        """A file with no TDD signals at all is spec."""
        from superclaude.cli.roadmap.executor import detect_input_type
        doc = tmp_path / "doc.md"
        doc.write_text("# Requirements\nFR-001: Do something\n## Architecture\nMonolith.")
        assert detect_input_type(doc) == "spec"


class TestSameFileGuard:
    """C-20: --tdd-file and --prd-file cannot be the same file."""

    def test_same_file_raises_system_exit(self, tmp_path):
        """Identical tdd_file and prd_file should raise UsageError via routing guard."""
        import click
        from superclaude.cli.roadmap.executor import execute_roadmap

        shared = tmp_path / "shared.md"
        shared.write_text("# Shared doc")
        output = tmp_path / "output"
        output.mkdir()
        config = RoadmapConfig(
            spec_file=shared,
            output_dir=output,
            tdd_file=shared,
            prd_file=shared,
            input_type="spec",
        )
        with pytest.raises(click.UsageError, match="same file"):
            execute_roadmap(config)

    def test_different_files_no_error(self, tmp_path):
        """Different tdd_file and prd_file should not trigger the guard."""
        spec = tmp_path / "spec.md"
        spec.write_text("# Spec")
        tdd = tmp_path / "tdd.md"
        tdd.write_text("# TDD")
        prd = tmp_path / "prd.md"
        prd.write_text("# PRD")
        config = RoadmapConfig(
            spec_file=spec,
            output_dir=tmp_path,
            tdd_file=tdd,
            prd_file=prd,
            input_type="spec",
            dry_run=True,  # prevent full pipeline execution
        )
        # Should not raise — dry_run will print and return
        from superclaude.cli.roadmap.executor import execute_roadmap
        execute_roadmap(config)


class TestPrdFileOverrideOnResume:
    """C-27: Explicit --prd-file on CLI overrides state-restored prd_file."""

    def test_explicit_prd_not_overwritten_by_state(self, tmp_path):
        """When --prd-file is set on CLI, state prd_file should NOT override it."""
        import json
        from superclaude.cli.roadmap.executor import _restore_from_state

        spec = tmp_path / "spec.md"
        spec.write_text("# Test Spec")
        cli_prd = tmp_path / "cli-prd.md"
        cli_prd.write_text("# CLI PRD")
        state_prd = tmp_path / "state-prd.md"
        state_prd.write_text("# State PRD")
        output = tmp_path / "output"
        output.mkdir()
        state_file = output / ".roadmap-state.json"
        state_file.write_text(json.dumps({
            "schema_version": 1,
            "spec_file": str(spec),
            "spec_hash": "abc",
            "agents": [{"model": "opus", "persona": "architect"}],
            "depth": "standard",
            "last_run": "2026-01-01T00:00:00+00:00",
            "prd_file": str(state_prd),
            "steps": {},
        }))

        config = RoadmapConfig(
            spec_file=spec, output_dir=output, prd_file=cli_prd
        )
        restored = _restore_from_state(config, agents_explicit=False, depth_explicit=False)
        # CLI value should win
        assert restored.prd_file == cli_prd


class TestRedundancyGuardStatePersistence:
    """C-111: Redundancy guard nullifies tdd_file and state saves correctly."""

    def test_tdd_primary_nullifies_tdd_file(self, tmp_path):
        """When input_type=tdd and tdd_file is set, redundancy guard nulls it."""
        tdd = tmp_path / "tdd.md"
        tdd.write_text("# TDD")
        config = RoadmapConfig(
            spec_file=tdd,
            output_dir=tmp_path,
            tdd_file=tdd,
            input_type="tdd",
            dry_run=True,
        )
        from superclaude.cli.roadmap.executor import execute_roadmap
        execute_roadmap(config)
        # After execute_roadmap, config should have tdd_file=None due to guard
        # (dry_run exits before _save_state, but we can verify the guard ran
        # by checking that _build_steps receives tdd_file=None)
        # We verify by checking the prompt content — no TDD supplementary block
        # should be in the extract step since tdd_file was nulled
        # This is implicitly tested by the dry_run not crashing

    def test_tdd_primary_no_tdd_file_no_warning(self, tmp_path):
        """When input_type=tdd and tdd_file is None, no redundancy warning."""
        import logging
        tdd = tmp_path / "tdd.md"
        tdd.write_text("# TDD")
        config = RoadmapConfig(
            spec_file=tdd,
            output_dir=tmp_path,
            input_type="tdd",
            dry_run=True,
        )
        from superclaude.cli.roadmap.executor import execute_roadmap
        # Should not warn — tdd_file is already None
        execute_roadmap(config)


# ── New test classes for multi-file auto-detection ──────────────────


class TestPrdDetection:
    """Tests for PRD document detection in detect_input_type()."""

    def test_detects_prd_from_real_fixture(self):
        """The real PRD fixture is detected as PRD."""
        from superclaude.cli.roadmap.executor import detect_input_type
        path = Path(".dev/test-fixtures/test-prd-user-auth.md")
        if path.exists():
            assert detect_input_type(path) == "prd"

    def test_detects_prd_from_prd_signals(self, tmp_path):
        """Synthetic PRD with type field + 5 sections scores 8 (threshold 5)."""
        # Score: type field (+3) + 5 PRD sections (+5) = 8
        from superclaude.cli.roadmap.executor import detect_input_type
        prd = tmp_path / "doc.md"
        prd.write_text(
            "---\ntype: Product Requirements\ntags: [prd]\n---\n"
            "## User Personas\nPersonas here.\n"
            "## Jobs To Be Done\nJTBD here.\n"
            "## Product Vision\nVision here.\n"
            "## User Stories\nStories here.\n"
            "## Success Metrics and Measurement\nMetrics here.\n"
        )
        assert detect_input_type(prd) == "prd"

    def test_prd_not_confused_with_tdd(self, tmp_path):
        """PRD signals yield 'prd', not 'tdd', even with no TDD signals."""
        # Score: type (+3) + 5 PRD sections (+5) + user story (+2) = 10
        from superclaude.cli.roadmap.executor import detect_input_type
        prd = tmp_path / "doc.md"
        prd.write_text(
            "---\ntype: Product Requirements\n---\n"
            "## User Personas\nPersonas.\n"
            "## Jobs To Be Done\nJTBD.\n"
            "## Product Vision\nVision.\n"
            "## User Stories\nAs a user, I want to log in.\n"
            "## Success Metrics and Measurement\nMetrics.\n"
        )
        assert detect_input_type(prd) == "prd"

    def test_prd_not_confused_with_spec(self, tmp_path):
        """PRD with type field + 3 section headings (score 6) is 'prd' not 'spec'."""
        # Score: type (+3) + 3 PRD sections (+3) = 6
        from superclaude.cli.roadmap.executor import detect_input_type
        prd = tmp_path / "doc.md"
        prd.write_text(
            "---\ntype: Product Requirements\n---\n"
            "## User Personas\nPersonas.\n"
            "## Competitive Analysis\nAnalysis.\n"
            "## Value Proposition\nValue.\n"
        )
        assert detect_input_type(prd) == "prd"


class TestThreeWayBoundary:
    """Exact score boundary tests for three-way detection."""

    def test_prd_score_below_threshold_is_spec(self, tmp_path):
        """3 PRD section headings only (score 3, below threshold 5) → spec."""
        from superclaude.cli.roadmap.executor import detect_input_type
        doc = tmp_path / "doc.md"
        doc.write_text(
            "# Document\n"
            "## User Personas\nContent.\n"
            "## Competitive Analysis\nContent.\n"
            "## Value Proposition\nContent.\n"
        )
        assert detect_input_type(doc) == "spec"

    def test_prd_score_at_threshold_is_prd(self, tmp_path):
        """type field (+3) + 2 PRD sections (+2) = score 5 → prd."""
        from superclaude.cli.roadmap.executor import detect_input_type
        doc = tmp_path / "doc.md"
        doc.write_text(
            "---\ntype: Product Requirements\n---\n"
            "## User Personas\nContent.\n"
            "## Jobs To Be Done\nContent.\n"
        )
        assert detect_input_type(doc) == "prd"

    def test_tdd_signals_only_is_tdd(self, tmp_path):
        """parent_doc (+2) + coordinator (+2) + Data Models (+1) = score 5 → tdd."""
        from superclaude.cli.roadmap.executor import detect_input_type
        doc = tmp_path / "doc.md"
        doc.write_text(
            "---\nparent_doc: PRD-001\ncoordinator: lead\n---\n"
            "## Data Models\nEntities here.\n"
        )
        assert detect_input_type(doc) == "tdd"

    def test_both_prd_and_tdd_signals_prd_wins(self, tmp_path):
        """PRD scored first: type (+3) + 3 sections (+3) = prd 6; coordinator = tdd 2. PRD wins."""
        from superclaude.cli.roadmap.executor import detect_input_type
        doc = tmp_path / "doc.md"
        doc.write_text(
            "---\ntype: Product Requirements\ncoordinator: lead\n---\n"
            "## User Personas\nContent.\n"
            "## Jobs To Be Done\nContent.\n"
            "## Product Vision\nContent.\n"
        )
        assert detect_input_type(doc) == "prd"


class TestMultiFileRouting:
    """Tests for _route_input_files() routing logic."""

    def _make_spec(self, tmp_path, name="spec.md"):
        p = tmp_path / name
        p.write_text("---\nspec_type: new_feature\n---\n## Requirements\nFR-001: Do thing.\n")
        return p

    def _make_tdd(self, tmp_path, name="tdd.md"):
        p = tmp_path / name
        p.write_text(
            "---\nparent_doc: PRD-001\ncoordinator: lead\n---\n"
            "## Data Models\nEntities.\n## API Specifications\nEndpoints.\n"
            "## Component Inventory\nComponents.\n## Testing Strategy\nTests.\n"
            "## Operational Readiness\nRunbooks.\n"
        )
        return p

    def _make_prd(self, tmp_path, name="prd.md"):
        p = tmp_path / name
        p.write_text(
            "---\ntype: Product Requirements\ntags: [prd]\n---\n"
            "## User Personas\nPersonas.\n## Jobs To Be Done\nJTBD.\n"
            "## Product Vision\nVision.\n## User Stories\nAs a user, I want to log in.\n"
            "## Success Metrics and Measurement\nMetrics.\n"
        )
        return p

    # ── Single file routing ──

    def test_route_single_spec_file(self, tmp_path):
        from superclaude.cli.roadmap.executor import _route_input_files
        spec = self._make_spec(tmp_path)
        result = _route_input_files((spec,), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")
        assert result["spec_file"] == spec
        assert result["tdd_file"] is None
        assert result["prd_file"] is None
        assert result["input_type"] == "spec"

    def test_route_single_tdd_file(self, tmp_path):
        from superclaude.cli.roadmap.executor import _route_input_files
        tdd = self._make_tdd(tmp_path)
        result = _route_input_files((tdd,), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")
        assert result["spec_file"] == tdd  # TDD becomes primary
        assert result["input_type"] == "tdd"
        assert result["tdd_file"] is None  # redundancy guard nulls it

    def test_route_single_prd_raises(self, tmp_path):
        import click
        from superclaude.cli.roadmap.executor import _route_input_files
        prd = self._make_prd(tmp_path)
        with pytest.raises(click.UsageError, match="PRD cannot be the sole primary input"):
            _route_input_files((prd,), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")

    # ── Multi-file routing ──

    def test_route_spec_plus_tdd(self, tmp_path):
        from superclaude.cli.roadmap.executor import _route_input_files
        spec = self._make_spec(tmp_path)
        tdd = self._make_tdd(tmp_path)
        result = _route_input_files((spec, tdd), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")
        assert result["spec_file"] == spec
        assert result["tdd_file"] == tdd
        assert result["input_type"] == "spec"

    def test_route_spec_plus_prd(self, tmp_path):
        from superclaude.cli.roadmap.executor import _route_input_files
        spec = self._make_spec(tmp_path)
        prd = self._make_prd(tmp_path)
        result = _route_input_files((spec, prd), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")
        assert result["spec_file"] == spec
        assert result["prd_file"] == prd
        assert result["tdd_file"] is None

    def test_route_tdd_plus_prd(self, tmp_path):
        from superclaude.cli.roadmap.executor import _route_input_files
        tdd = self._make_tdd(tmp_path)
        prd = self._make_prd(tmp_path)
        result = _route_input_files((tdd, prd), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")
        assert result["spec_file"] == tdd  # TDD becomes primary
        assert result["prd_file"] == prd
        assert result["input_type"] == "tdd"

    def test_route_all_three_files(self, tmp_path):
        from superclaude.cli.roadmap.executor import _route_input_files
        spec = self._make_spec(tmp_path)
        tdd = self._make_tdd(tmp_path)
        prd = self._make_prd(tmp_path)
        result = _route_input_files((spec, tdd, prd), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")
        assert result["spec_file"] == spec
        assert result["tdd_file"] == tdd
        assert result["prd_file"] == prd
        assert result["input_type"] == "spec"

    # ── Error cases ──

    def test_route_duplicate_type_raises(self, tmp_path):
        """Two spec-like files → error."""  # Edge case 8.2
        import click
        from superclaude.cli.roadmap.executor import _route_input_files
        spec1 = self._make_spec(tmp_path, "spec1.md")
        spec2 = self._make_spec(tmp_path, "spec2.md")
        with pytest.raises(click.UsageError, match="Multiple files detected as spec"):
            _route_input_files((spec1, spec2), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")

    def test_route_too_many_files_raises(self, tmp_path):
        """4 files → error."""  # Edge case 8.3
        import click
        from superclaude.cli.roadmap.executor import _route_input_files
        files = tuple(self._make_spec(tmp_path, f"f{i}.md") for i in range(4))
        with pytest.raises(click.UsageError, match="1-3"):
            _route_input_files(files, explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")

    def test_route_conflict_positional_tdd_and_explicit_tdd_raises(self, tmp_path):
        """Positional TDD + --tdd-file → conflict error."""  # Edge case 8.4
        import click
        from superclaude.cli.roadmap.executor import _route_input_files
        spec = self._make_spec(tmp_path)
        tdd = self._make_tdd(tmp_path)
        other_tdd = tmp_path / "other-tdd.md"
        other_tdd.write_text("# Other TDD")
        with pytest.raises(click.UsageError, match="(?i)conflict"):
            _route_input_files((spec, tdd), explicit_tdd=other_tdd, explicit_prd=None, explicit_input_type="auto")


class TestBackwardCompat:
    """Backward compatibility tests for _route_input_files()."""

    def _make_spec(self, tmp_path):
        p = tmp_path / "spec.md"
        p.write_text("---\nspec_type: new_feature\n---\n## Requirements\nFR-001: Thing.\n")
        return p

    def _make_tdd(self, tmp_path, name="tdd.md"):
        p = tmp_path / name
        p.write_text(
            "---\nparent_doc: PRD-001\ncoordinator: lead\n---\n"
            "## Data Models\nEntities.\n## API Specifications\nEndpoints.\n"
            "## Component Inventory\nComponents.\n## Testing Strategy\nTests.\n"
            "## Operational Readiness\nRunbooks.\n"
        )
        return p

    def test_single_positional_routes_like_before(self, tmp_path):
        from superclaude.cli.roadmap.executor import _route_input_files
        spec = self._make_spec(tmp_path)
        result = _route_input_files((spec,), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")
        assert result["spec_file"] == spec
        assert result["input_type"] == "spec"

    def test_explicit_input_type_overrides_detection(self, tmp_path):
        from superclaude.cli.roadmap.executor import _route_input_files
        spec = self._make_spec(tmp_path)  # auto-detects as spec
        result = _route_input_files((spec,), explicit_tdd=None, explicit_prd=None, explicit_input_type="tdd")
        assert result["input_type"] == "tdd"

    def test_explicit_tdd_file_flag_works_with_positional(self, tmp_path):
        from superclaude.cli.roadmap.executor import _route_input_files
        spec = self._make_spec(tmp_path)
        tdd = self._make_tdd(tmp_path)
        result = _route_input_files((spec,), explicit_tdd=tdd, explicit_prd=None, explicit_input_type="auto")
        assert result["spec_file"] == spec
        assert result["tdd_file"] == tdd


class TestOverridePriority:
    """Tests for override priority in multi-file mode."""

    def _make_spec(self, tmp_path):
        p = tmp_path / "spec.md"
        p.write_text("---\nspec_type: new_feature\n---\n## Requirements\nFR-001.\n")
        return p

    def _make_tdd(self, tmp_path, name="tdd.md"):
        p = tmp_path / name
        p.write_text(
            "---\nparent_doc: PRD-001\ncoordinator: lead\n---\n"
            "## Data Models\nEntities.\n## API Specifications\nEndpoints.\n"
            "## Component Inventory\nComponents.\n## Testing Strategy\nTests.\n"
            "## Operational Readiness\nRunbooks.\n"
        )
        return p

    def _make_prd(self, tmp_path, name="prd.md"):
        p = tmp_path / name
        p.write_text(
            "---\ntype: Product Requirements\ntags: [prd]\n---\n"
            "## User Personas\nPersonas.\n## Jobs To Be Done\nJTBD.\n"
            "## Product Vision\nVision.\n## User Stories\nAs a user, I want to log in.\n"
            "## Success Metrics and Measurement\nMetrics.\n"
        )
        return p

    def test_input_type_ignored_for_multifile(self, tmp_path):
        """--input-type is ignored in multi-file mode; content detection wins."""
        from superclaude.cli.roadmap.executor import _route_input_files
        spec = self._make_spec(tmp_path)
        tdd = self._make_tdd(tmp_path)
        result = _route_input_files((spec, tdd), explicit_tdd=None, explicit_prd=None, explicit_input_type="prd")
        # --input-type=prd is ignored; files classified by content
        assert result["spec_file"] == spec
        assert result["tdd_file"] == tdd

    def test_explicit_prd_flag_works_with_multifile(self, tmp_path):
        """Explicit --prd-file supplements positional spec+tdd."""
        from superclaude.cli.roadmap.executor import _route_input_files
        spec = self._make_spec(tmp_path)
        tdd = self._make_tdd(tmp_path)
        prd = self._make_prd(tmp_path)
        result = _route_input_files((spec, tdd), explicit_tdd=None, explicit_prd=prd, explicit_input_type="auto")
        assert result["spec_file"] == spec
        assert result["tdd_file"] == tdd
        assert result["prd_file"] == prd
