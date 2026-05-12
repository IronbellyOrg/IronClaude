"""TUI v2 Wave 3 (v3.7) — retrospective tests.

Covers:
- Aggregation of per-phase summaries (phase_outcomes, all_files,
  validation_matrix, all_errors, validation_coverage).
- Multi-phase file flagging.
- Narrative prompt construction includes aggregate stats.
- generate() writes results/release-retrospective.md with sections.
- Haiku failure path writes retrospective without narrative.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from superclaude.cli.sprint.models import (
    Phase,
    PhaseResult,
    PhaseStatus,
    SprintConfig,
    SprintOutcome,
    SprintResult,
)
from superclaude.cli.sprint.retrospective import (
    RetrospectiveGenerator,
    _aggregate_files,
    _aggregate_phase_outcomes,
    _aggregate_validation_matrix,
    _assess_validation_coverage,
    _build_retrospective_narrative_prompt,
    _render_retrospective_markdown,
)
from superclaude.cli.sprint.summarizer import PhaseSummary

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_config(tmp_path: Path) -> SprintConfig:
    index = tmp_path / "tasklist-index.md"
    index.write_text("")
    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[],
    )


def _make_phase_result(
    *, phase: Phase, status: PhaseStatus = PhaseStatus.PASS, **kwargs
) -> PhaseResult:
    now = datetime.now(timezone.utc)
    defaults = dict(
        phase=phase,
        status=status,
        started_at=now - timedelta(seconds=30),
        finished_at=now,
    )
    defaults.update(kwargs)
    return PhaseResult(**defaults)


def _make_sprint_result(config: SprintConfig, phase_results: list[PhaseResult]) -> SprintResult:
    sr = SprintResult(config=config, phase_results=phase_results)
    sr.finished_at = datetime.now(timezone.utc)
    return sr


def _make_summaries() -> dict[int, PhaseSummary]:
    phase1 = Phase(number=1, file=Path("/tmp/p1.md"), name="Foundation")
    phase2 = Phase(number=2, file=Path("/tmp/p2.md"), name="Backend")
    phase3 = Phase(number=3, file=Path("/tmp/p3.md"), name="Polish")
    return {
        1: PhaseSummary(
            phase=phase1,
            phase_result=_make_phase_result(
                phase=phase1, turns=3, tokens_in=100, tokens_out=50
            ),
            tasks=[{"task_id": "T01.01", "status": "PASS"}],
            files_changed=[
                {"path": "src/shared.py", "tool": "Edit"},
                {"path": "src/foo.py", "tool": "Write"},
            ],
            validations=[{"check": "pytest", "verdict": "passed", "snippet": "..."}],
            reasoning_excerpts=["Implemented foundation"],
            errors=[],
            narrative="Foundation ready.",
        ),
        2: PhaseSummary(
            phase=phase2,
            phase_result=_make_phase_result(
                phase=phase2, turns=4, tokens_in=200, tokens_out=100, files_changed=1
            ),
            tasks=[{"task_id": "T02.01", "status": "FAIL"}],
            files_changed=[
                {"path": "src/shared.py", "tool": "MultiEdit"},
                {"path": "src/bar.py", "tool": "Edit"},
            ],
            validations=[{"check": "ruff", "verdict": "passed", "snippet": "..."}],
            reasoning_excerpts=[],
            errors=[
                {"task_id": "T02.01", "tool": "Bash", "message": "exit_code: 2"},
            ],
            narrative="",
        ),
        3: PhaseSummary(
            phase=phase3,
            phase_result=_make_phase_result(
                phase=phase3, turns=2, tokens_in=50, tokens_out=25
            ),
            tasks=[],
            files_changed=[{"path": "README.md", "tool": "Write"}],
            validations=[],
            reasoning_excerpts=[],
            errors=[],
            narrative="",
        ),
    }


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


class TestAggregatePhaseOutcomes:
    def test_preserves_order_by_phase_number(self):
        summaries = _make_summaries()
        rows = _aggregate_phase_outcomes(summaries)
        assert [r["phase"] for r in rows] == [1, 2, 3]

    def test_rows_carry_expected_keys(self):
        summaries = _make_summaries()
        rows = _aggregate_phase_outcomes(summaries)
        for r in rows:
            assert set(r.keys()) >= {
                "phase",
                "name",
                "status",
                "duration",
                "turns",
                "tokens_in",
                "tokens_out",
                "files_changed",
                "errors",
            }

    def test_phase_two_counts_errors(self):
        rows = _aggregate_phase_outcomes(_make_summaries())
        by_phase = {r["phase"]: r for r in rows}
        assert by_phase[2]["errors"] == 1
        assert by_phase[1]["errors"] == 0


class TestAggregateFiles:
    def test_multi_phase_file_flagged(self):
        files = _aggregate_files(_make_summaries())
        by_path = {f["path"]: f for f in files}
        assert by_path["src/shared.py"]["multi_phase"] is True
        assert by_path["src/shared.py"]["phases"] == [1, 2]
        assert by_path["src/foo.py"]["multi_phase"] is False

    def test_tools_are_sorted_unique(self):
        files = _aggregate_files(_make_summaries())
        by_path = {f["path"]: f for f in files}
        # shared.py was touched with Edit in phase 1 and MultiEdit in phase 2.
        assert by_path["src/shared.py"]["tools"] == ["Edit", "MultiEdit"]


class TestAggregateValidationMatrix:
    def test_groups_checks_with_verdicts(self):
        rows = _aggregate_validation_matrix(_make_summaries())
        by_check = {r["check"]: r for r in rows}
        assert "pytest" in by_check and "ruff" in by_check
        assert by_check["pytest"]["verdicts"] == ["passed"]
        assert by_check["pytest"]["phases"] == [1]


class TestValidationCoverage:
    def test_empty_summaries(self):
        assert _assess_validation_coverage({}, []) == "no phases summarised"

    def test_full_coverage(self):
        summaries = _make_summaries()
        # Remove phase 3 (which has no validations) to make it "all covered".
        del summaries[3]
        matrix = _aggregate_validation_matrix(summaries)
        assert "all" in _assess_validation_coverage(summaries, matrix)

    def test_partial_coverage(self):
        summaries = _make_summaries()
        matrix = _aggregate_validation_matrix(summaries)
        msg = _assess_validation_coverage(summaries, matrix)
        assert "2/3" in msg


# ---------------------------------------------------------------------------
# Narrative prompt + markdown
# ---------------------------------------------------------------------------


class TestNarrativePrompt:
    def test_prompt_mentions_totals_and_phases(self, tmp_path):
        config = _make_config(tmp_path)
        summaries = _make_summaries()
        sr = _make_sprint_result(
            config,
            [s.phase_result for s in summaries.values()],
        )
        retro = RetrospectiveGenerator(config).aggregate(sr, summaries)
        prompt = _build_retrospective_narrative_prompt(retro)
        assert "retrospective" in prompt.lower()
        assert "3 phases" in prompt
        assert "Phase 1 (Foundation)" in prompt
        assert "multiple phases" in prompt  # multi-phase file note

    def test_prompt_includes_error_tool_histogram(self, tmp_path):
        config = _make_config(tmp_path)
        summaries = _make_summaries()
        sr = _make_sprint_result(config, [s.phase_result for s in summaries.values()])
        retro = RetrospectiveGenerator(config).aggregate(sr, summaries)
        prompt = _build_retrospective_narrative_prompt(retro)
        assert "Errors:" in prompt and "Bash" in prompt


class TestRetrospectiveMarkdown:
    def test_contains_all_sections(self, tmp_path):
        config = _make_config(tmp_path)
        summaries = _make_summaries()
        sr = _make_sprint_result(config, [s.phase_result for s in summaries.values()])
        retro = RetrospectiveGenerator(config).aggregate(sr, summaries)
        retro.narrative = "All good."
        text = _render_retrospective_markdown(retro)
        assert "# Release Retrospective" in text
        assert "## Narrative" in text and "All good." in text
        assert "## Phase Outcomes" in text
        assert "## Files Changed" in text
        assert "## Validation Matrix" in text
        assert "## Errors" in text
        # Multi-phase file flag rendered.
        assert "src/shared.py" in text and "yes" in text

    def test_empty_summaries_still_renders(self, tmp_path):
        config = _make_config(tmp_path)
        sr = _make_sprint_result(config, [])
        retro = RetrospectiveGenerator(config).aggregate(sr, {})
        text = _render_retrospective_markdown(retro)
        assert "_No per-phase summaries available._" in text


# ---------------------------------------------------------------------------
# Generator end-to-end
# ---------------------------------------------------------------------------


class TestRetrospectiveGenerator:
    def test_generate_writes_markdown_file(self, tmp_path):
        config = _make_config(tmp_path)
        summaries = _make_summaries()
        sr = _make_sprint_result(config, [s.phase_result for s in summaries.values()])
        sr.outcome = SprintOutcome.SUCCESS

        with patch(
            "superclaude.cli.sprint.retrospective.invoke_haiku",
            return_value="Release narrative",
        ):
            retro = RetrospectiveGenerator(config).generate(sr, summaries)

        assert retro.narrative == "Release narrative"
        target = config.results_dir / "release-retrospective.md"
        assert target.exists()
        text = target.read_text()
        assert "Release narrative" in text
        assert "Foundation" in text

    def test_generate_tolerates_narrative_failure(self, tmp_path):
        config = _make_config(tmp_path)
        summaries = _make_summaries()
        sr = _make_sprint_result(config, [s.phase_result for s in summaries.values()])

        with patch(
            "superclaude.cli.sprint.retrospective.invoke_haiku",
            side_effect=RuntimeError("boom"),
        ):
            retro = RetrospectiveGenerator(config).generate(sr, summaries)

        assert retro.narrative == ""
        target = config.results_dir / "release-retrospective.md"
        assert target.exists()
        assert "Narrative unavailable" in target.read_text()

    def test_generate_with_no_summaries(self, tmp_path):
        config = _make_config(tmp_path)
        sr = _make_sprint_result(config, [])

        with patch(
            "superclaude.cli.sprint.retrospective.invoke_haiku", return_value=""
        ):
            retro = RetrospectiveGenerator(config).generate(sr, {})

        assert retro.phase_outcomes == []
        assert retro.all_files == []
        target = config.results_dir / "release-retrospective.md"
        assert target.exists()
