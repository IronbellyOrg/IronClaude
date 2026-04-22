"""Unit tests for superclaude.cli.prd.gates.

Section 8.1 test plan: 8 tests.
"""

from __future__ import annotations

import pytest

from superclaude.cli.prd.gates import (
    GATE_CRITERIA,
    _check_b2_self_contained,
    _check_no_placeholders,
    _check_parallel_instructions,
    _check_parsed_request_fields,
    _check_prd_template_sections,
    _check_qa_verdict,
    _check_research_notes_sections,
    _check_verdict_field,
    _safe_check,
)


class TestCheckParsedRequestFields:
    """Validate parsed request field detection."""

    def test_check_parsed_request_fields_valid(self) -> None:
        content = '''
{"GOAL": "Build a user dashboard", "PRODUCT_SLUG": "dashboard", "PRD_SCOPE": "feature", "SCENARIO": "B"}
'''
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
## Product Capabilities
Details here.

## Technical Architecture
Details here.

## User Flows
Details here.

## Integration Points
Details here.

## Existing Documentation
Details here.

## Gap Analysis
Details here.

## Suggested Phases
1. Phase one detail
"""
        assert _check_research_notes_sections(content) is True

    def test_check_research_notes_sections_missing(self) -> None:
        content = """
## Product Capabilities
Some content.

## Technical Architecture
Some content.
"""
        result = _check_research_notes_sections(content)
        assert isinstance(result, str)
        assert "User Flows" in result


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
    """Validate parallel keywords in phases 2-5."""

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
