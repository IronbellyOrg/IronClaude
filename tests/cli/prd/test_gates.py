"""Unit tests for superclaude.cli.prd.gates.

Section 8.1 test plan: 8 tests.
"""

from __future__ import annotations

import pytest

from superclaude.cli.prd.gates import (
    _check_b2_self_contained,
    _check_no_placeholders,
    _check_no_truncation_marker,
    _check_parallel_instructions,
    _check_parsed_request_fields,
    _check_prd_template_sections,
    _check_research_notes_sections,
    _check_verdict_field,
    _safe_check,
)


class TestCheckParsedRequestFields:
    """Validate parsed request field detection."""

    def test_check_parsed_request_fields_valid(self) -> None:
        content = """
{"GOAL": "Build a user dashboard", "PRODUCT_SLUG": "dashboard", "PRD_SCOPE": "feature", "SCENARIO": "B"}
"""
        assert _check_parsed_request_fields(content) is True

    def test_check_parsed_request_fields_valid_markdown(self) -> None:
        content = """
GOAL: Build a user dashboard
PRODUCT_SLUG: dashboard
PRD_SCOPE: feature
SCENARIO: B
"""
        assert _check_parsed_request_fields(content) is True

    def test_check_parsed_request_fields_missing(self) -> None:
        content = '{"GOAL": "Build something"}'
        result = _check_parsed_request_fields(content)
        assert isinstance(result, str)
        assert "PRODUCT_SLUG" in result
        assert "PRD_SCOPE" in result
        assert "SCENARIO" in result


class TestCheckResearchNotesSections:
    """Validate all 7 required research sections."""

    def test_check_research_notes_sections(self) -> None:
        content = """
## EXISTING_FILES
Details here.

## PATTERNS_AND_CONVENTIONS
Details here.

## FEATURE_ANALYSIS
Details here.

## RECOMMENDED_OUTPUTS
Details here.

## SUGGESTED_PHASES
1. Phase one detail

## TEMPLATE_NOTES
Details here.

## AMBIGUITIES_FOR_USER
Details here.
"""
        assert _check_research_notes_sections(content) is True

    def test_check_research_notes_sections_missing(self) -> None:
        content = """
## EXISTING_FILES
Some content.

## PATTERNS_AND_CONVENTIONS
Some content.
"""
        result = _check_research_notes_sections(content)
        assert isinstance(result, str)
        assert "FEATURE_ANALYSIS" in result


class TestCheckVerdictField:
    """Detect PASS/FAIL in both JSON and markdown format."""

    def test_check_verdict_field(self) -> None:
        # JSON format
        assert _check_verdict_field('{"verdict": "PASS"}') is True
        assert _check_verdict_field('{"verdict": "FAIL"}') is True

        # Markdown format
        assert _check_verdict_field("verdict: PASS") is True
        assert _check_verdict_field("**Verdict**: FAIL") is True

        # Missing verdict
        result = _check_verdict_field("No verdict here")
        assert isinstance(result, str)
        assert "verdict" in result.lower()

    @pytest.mark.parametrize(
        "shape",
        [
            "Verdict: PASS",
            "**Verdict**: PASS",
            "**Verdict:** PASS",
            "**Verdict:** **PASS**",
            "**VERDICT: PASS**",
            "**VERDICT:** **FAIL**",
        ],
    )
    def test_check_verdict_field_accepts_valid_markdown_shapes(
        self, shape: str
    ) -> None:
        """Legitimate markdown verdict shapes are accepted."""
        content = f"## QA Report\n\n{shape}\n\nDetails follow.\n"
        assert _check_verdict_field(content) is True

    @pytest.mark.parametrize(
        "shape",
        [
            "Verdict PASS",
            "Verdict::: PASS",
            "Verdict***PASS",
            "verdict pass",
            "Verdict: PASSING",
            "Verdict: FAILURE",
        ],
    )
    def test_check_verdict_field_rejects_invalid_shapes(self, shape: str) -> None:
        """Malformed verdict shapes (no colon, junk separators, lowercase
        value) are rejected — the tightened regex no longer false-accepts."""
        content = f"## QA Report\n\n{shape}\n\nDetails follow.\n"
        result = _check_verdict_field(content)
        assert result is not True

    @pytest.mark.parametrize(
        "shape",
        [
            "- **Verdict:** ✅ **PASS**",  # the live research-qa repro
            "## Verdict: ✅ PASS — CONTINUE",
            "### Verdict: 🟢 FAIL",
            "- Verdict: ✅ PASS",
            "**Verdict**: ❌ FAIL",
            "## VERDICT: ✅ PASS",
        ],
    )
    def test_check_verdict_field_accepts_decorated_shapes(self, shape: str) -> None:
        """Agents decorate verdicts with heading/bullet prefixes, bold wrapping,
        emoji, and bold-wrapped values; all are accepted as long as the colon +
        uppercase PASS/FAIL are present (the unified line-anchored regex)."""
        content = f"## QA Report\n\n{shape}\n\nRationale follows.\n"
        assert _check_verdict_field(content) is True

    def test_check_verdict_field_rejects_rationale_heading_without_value(self) -> None:
        """A 'Verdict rationale' heading with no PASS/FAIL value must not match."""
        content = "## Verdict rationale\n\nWe weighed the evidence.\n"
        assert _check_verdict_field(content) is not True


class TestCheckB2SelfContained:
    """Catch 'see above' violations in checklist items."""

    def test_check_b2_self_contained(self) -> None:
        # Clean checklist
        clean = """
- [ ] Implement user authentication
- [x] Create database schema
- [ ] Write unit tests
"""
        assert _check_b2_self_contained(clean) is True

        # Violation: "see above"
        violation = """
- [ ] Implement the feature (see above for details)
- [x] Create database schema
"""
        result = _check_b2_self_contained(violation)
        assert isinstance(result, str)
        assert "see above" in result.lower()


class TestCheckParallelInstructions:
    """Validate parallel keywords in work phases (>=2), with the final
    completion/presentation phase exempt."""

    def test_check_parallel_instructions(self) -> None:
        content = """
## Phase 1: Setup
Sequential setup tasks.

## Phase 2: Research
Run research agents in parallel across all areas.

## Phase 3: Synthesis
Process synthesis files concurrently.
"""
        assert _check_parallel_instructions(content) is True

    def test_check_parallel_instructions_missing(self) -> None:
        content = """
## Phase 1: Setup
Sequential setup.

## Phase 2: Research
Run each research file one by one.
"""
        result = _check_parallel_instructions(content)
        assert isinstance(result, str)
        assert "Phase 2" in result

    def test_check_parallel_final_completion_phase_exempt_live_repro(self) -> None:
        # Live repro: heavyweight task with parallel work phases 2-6 and a
        # sequential final completion phase 7. The completion phase must NOT
        # trip the gate (it previously HALTed build-task-file).
        content = """
## Phase 1: Setup
Sequential setup.

## Phase 2: Deep Investigation
Run 9 research agents in parallel.

## Phase 3: Research Gate
Run gate agents in parallel.

## Phase 4: Web Research
Run web agents in parallel.

## Phase 5: Synthesis
Run synthesis agents in parallel.

## Phase 6: Assembly & Validation
Run lens QA agents in parallel.

## Phase 7: Present to User & Complete Task
Present the summary and mark the task done. Sequential.
"""
        assert _check_parallel_instructions(content) is True

    def test_check_parallel_final_completion_phase_exempt_short(self) -> None:
        # A short task whose final phase is a completion phase: exempt it.
        content = """
## Phase 1: Setup
Sequential setup.

## Phase 2: Build
Process components in parallel.

## Phase 3: Present & Complete
Present results to the user and mark complete. Sequential.
"""
        assert _check_parallel_instructions(content) is True

    def test_check_parallel_final_work_phase_still_checked(self) -> None:
        # The final phase is exempt ONLY when its heading marks it a completion
        # phase. A final WORK phase (not completion-titled) missing parallelism
        # is still flagged -- no over-exemption.
        content = """
## Phase 1: Setup
Sequential setup.

## Phase 2: Investigation
Run agents in parallel.

## Phase 3: Synthesis
Process each synthesis file one at a time.
"""
        result = _check_parallel_instructions(content)
        assert isinstance(result, str)
        assert "Phase 3" in result

    def test_check_parallel_final_incomplete_phase_not_exempted(self) -> None:
        # Regression (PR #154 review r3383060121): the completion-signal match
        # must be word-boundary anchored. A final WORK phase whose heading
        # merely CONTAINS a signal as a substring ("Incomplete" contains
        # "complete") must NOT be exempted -- it is real work and missing
        # parallelism must still be flagged.
        content = """
## Phase 1: Setup
Sequential setup.

## Phase 2: Investigation
Run agents in parallel.

## Phase 3: Incomplete Work Reconciliation
Process each leftover item one at a time.
"""
        result = _check_parallel_instructions(content)
        assert isinstance(result, str)
        assert "Phase 3" in result


class TestCheckPrdTemplateSections:
    """Detect missing critical PRD sections."""

    def test_check_prd_template_sections(self) -> None:
        content = """
## Executive Summary
Summary here.

## Problem Statement
Problem here.

## Technical Requirements
Requirements here.

## Implementation Plan
Plan here.

## Success Metrics
Metrics here.
"""
        assert _check_prd_template_sections(content) is True

    def test_check_prd_template_sections_missing(self) -> None:
        content = """
## Executive Summary
Summary here.
"""
        result = _check_prd_template_sections(content)
        assert isinstance(result, str)
        assert "Problem Statement" in result


class TestCheckNoPlaceholders:
    """Catch TODO, TBD, PLACEHOLDER text."""

    def test_check_no_placeholders(self) -> None:
        clean = "This is a clean document with proper content throughout."
        assert _check_no_placeholders(clean) is True

        with_todo = "This needs TODO: complete later."
        result = _check_no_placeholders(with_todo)
        assert isinstance(result, str)
        assert "TODO" in result

        with_tbd = "Timeline is TBD."
        result = _check_no_placeholders(with_tbd)
        assert isinstance(result, str)
        assert "TBD" in result


class TestGateExceptionWrapping:
    """Verify that crashed checks return error strings, not exceptions."""

    def test_safe_check_wraps_exceptions(self) -> None:
        def crasher(content: str) -> bool | str:
            raise ValueError("intentional crash")

        wrapped = _safe_check("crasher", crasher)
        result = wrapped("any content")
        assert isinstance(result, str)
        assert "crasher" in result
        assert "crashed" in result
        assert "intentional crash" in result


class TestCheckNoTruncationMarker:
    """[AC9] _check_no_truncation_marker flags silently-truncated content.

    Detects the inline truncation marker emitted by _read_file
    ("\\n\\n[TRUNCATED — file exceeds 50KB inline limit]", em-dash) via the
    "[TRUNCATED" substring, plus content whose rstrip() ends with "...".
    """

    def test_clean_content_passes(self) -> None:
        assert (
            _check_no_truncation_marker(
                "clean full content with no truncation markers at all"
            )
            is True
        )

    def test_truncated_marker_fails(self) -> None:
        content = "body of the document\n\n[TRUNCATED — file exceeds 50KB inline limit]"
        result = _check_no_truncation_marker(content)
        assert isinstance(result, str)
        assert "truncat" in result.lower()


class TestBuildTaskFileGateAdvisoryWiring:
    """Lock the intent: on the build-task-file gate, parallel_instructions is
    ADVISORY (non-fatal) while task_phases_present and b2_self_contained stay
    STRICT/halting."""

    def test_parallel_instructions_is_advisory_others_strict(self) -> None:
        from superclaude.cli.prd.gates import GATE_CRITERIA

        checks = {
            c.name: c for c in (GATE_CRITERIA["build-task-file"].semantic_checks or [])
        }
        assert checks["parallel_instructions"].advisory is True
        assert checks["task_phases_present"].advisory is False
        assert checks["b2_self_contained"].advisory is False

    def test_trailing_ellipsis_fails(self) -> None:
        result = _check_no_truncation_marker("the document ends abruptly here ...")
        assert isinstance(result, str)
        assert "truncat" in result.lower()
