# Research: File Inventory

**Topic type:** File Inventory
**Scope:** Files touched or referenced by the schema-divergence fix
**Status:** Complete
**Date:** 2026-05-20

---

## Files to be modified

### `src/superclaude/cli/prd/gates.py` (506 lines, 16384 bytes)

**Purpose**: Defines PRD pipeline gate criteria. Maps each pipeline step to a `GateCriteria` instance (semantic checks + min_lines + enforcement tier). This file holds the BUG (per the prior adversarial-debate turn).

**Edit Region 1 — `_RESEARCH_REQUIRED_SECTIONS` (lines 102-110)**:

Current text (verbatim, re-confirmed via `cat -n` in the immediately preceding turn):

```python
_RESEARCH_REQUIRED_SECTIONS = [
    "Product Capabilities",
    "Technical Architecture",
    "User Flows",
    "Integration Points",
    "Existing Documentation",
    "Gap Analysis",
    "Suggested Phases",
]
```

Target text (after Edit A — aligns gate to upstream `SKILL.md:267-305` and the in-tree prompt at `prompts.py:226-254`):

```python
_RESEARCH_REQUIRED_SECTIONS = [
    "EXISTING_FILES",
    "PATTERNS_AND_CONVENTIONS",
    "FEATURE_ANALYSIS",
    "RECOMMENDED_OUTPUTS",
    "SUGGESTED_PHASES",
    "TEMPLATE_NOTES",
    "AMBIGUITIES_FOR_USER",
]
```

The consuming function `_check_research_notes_sections` at `gates.py:113-126` is correct as-is (it already uses `re.escape(section)` + `re.IGNORECASE`, and `re.escape("EXISTING_FILES")` produces a literal `EXISTING_FILES` pattern that matches `## EXISTING_FILES` and `**EXISTING_FILES**` cleanly).

**Edit Region 2 — `_check_suggested_phases_detail` (lines 129-146)**:

Current text (verbatim) — function body shown; only lines 134-138 (the `phases_match = re.search(...)` block) need to change:

```python
def _check_suggested_phases_detail(content: str) -> bool | str:
    """Check that the Suggested Phases section contains per-agent detail.

    Expects at least one numbered or bulleted list item under a Phases heading.
    """
    phases_match = re.search(
        r"(?:^|\n)\s*#{1,4}\s+.*(?:Suggested\s+)?Phases",
        content,
        re.IGNORECASE,
    )
    if not phases_match:
        return "No 'Suggested Phases' section found"
    # Check for list items after the heading
    after_heading = content[phases_match.end() :]
    list_pat = re.search(r"(?:^|\n)\s*(?:\d+\.|[-*])\s+\S", after_heading)
    if not list_pat:
        return "Suggested Phases section has no detail items"
    return True
```

Target text after Edit B — change the regex on lines 134-138 to accept both space-separated and underscore-separated heading forms. The minimal change is to widen `\s+` to `[\s_]+`:

```python
    phases_match = re.search(
        r"(?:^|\n)\s*#{1,4}\s+.*(?:Suggested[\s_]+)?Phases",
        content,
        re.IGNORECASE,
    )
```

After this change, `## SUGGESTED_PHASES` matches via `IGNORECASE` (turns `Suggested` → `SUGGESTED`) + the `[\s_]+` class (matches the underscore).

### `tests/cli/prd/test_gates.py` (219 lines)

**Purpose**: Unit tests for `gates.py`. Specifically `class TestCheckResearchNotesSections` at lines 47-86 hand-writes a `## Product Capabilities` / `## Technical Architecture` / ... fixture that exercises the OLD constant. Must be rewritten in lockstep with Edit A.

**Edit Region 3 — Lines 47-86 (`class TestCheckResearchNotesSections`)**:

Current text (verbatim — re-confirmed via `cat -n` in the immediately preceding turn):

```python
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
```

Target text after Edit C:

```python
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
```

Note: the `test_check_research_notes_sections` happy-path test now also covers `_check_suggested_phases_detail` indirectly because `## SUGGESTED_PHASES` followed by a `1. Phase one detail` list item satisfies both the section-presence check AND the detail-items check. After Edit B's regex widening, this combination passes.

## File to be created

### `tests/cli/prd/test_research_notes_roundtrip.py` (NEW)

**Purpose**: The round-trip integration test from finding #8 of the validator brief. Wires `build_research_notes_prompt` output through `_check_research_notes_sections`. Closes the structural blind spot where `test_gates.py` and `test_prompts.py` test each side in isolation.

**Full file contents (verbatim — to be written by Edit D)**:

```python
"""Round-trip integration test: research notes prompt → gate.

Closes the structural blind spot identified in the schema-divergence audit:
test_gates.py only feeds the gate hand-written input in the gate's schema,
and test_prompts.py only asserts the prompt emits its own schema. Neither
verifies that the schema instructed by the prompt is the schema accepted
by the gate. This test wires the two together.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from superclaude.cli.prd.gates import (
    _RESEARCH_REQUIRED_SECTIONS,
    _check_research_notes_sections,
    _check_suggested_phases_detail,
)
from superclaude.cli.prd.models import PrdConfig
from superclaude.cli.prd.prompts import build_research_notes_prompt


@pytest.fixture()
def minimal_config(tmp_path: Path) -> PrdConfig:
    task_dir = tmp_path / "task"
    task_dir.mkdir()
    (task_dir / "scope-discovery-raw.md").write_text("# scope\nstub\n")
    (task_dir / "parsed-request.json").write_text(
        '{"GOAL": "x", "PRODUCT_NAME": "X", "PRODUCT_SLUG": "x", '
        '"PRD_SCOPE": "feature", "SCENARIO": "B"}'
    )
    skill_refs = tmp_path / "refs"
    skill_refs.mkdir()
    return PrdConfig(
        user_message="x",
        product_name="X",
        product_slug="x",
        tier="standard",
        task_dir=task_dir,
        skill_refs_dir=skill_refs,
        output_path=tmp_path / "out.md",
    )


def _extract_h2_sections_from_prompt(prompt: str) -> list[str]:
    """Pull the '## SECTION_NAME' headings the prompt instructs the agent to emit."""
    return re.findall(r"^##\s+([A-Z_][A-Z0-9_]+)\s*$", prompt, re.MULTILINE)


def test_prompt_schema_matches_gate_schema(minimal_config: PrdConfig) -> None:
    """The 7 sections the prompt instructs MUST equal the 7 sections the gate requires."""
    prompt = build_research_notes_prompt(minimal_config)
    instructed = _extract_h2_sections_from_prompt(prompt)
    assert sorted(instructed) == sorted(_RESEARCH_REQUIRED_SECTIONS), (
        f"prompt instructs {instructed!r} but gate requires "
        f"{_RESEARCH_REQUIRED_SECTIONS!r}"
    )


def test_prompt_conforming_output_passes_gate(minimal_config: PrdConfig) -> None:
    """A research-notes.md that follows the prompt's instructions MUST pass the gate."""
    prompt = build_research_notes_prompt(minimal_config)
    instructed = _extract_h2_sections_from_prompt(prompt)
    fake_research_notes = "---\nDate: 2026-05-20\nScenario: B\nTier: standard\n---\n\n"
    for section in instructed:
        fake_research_notes += f"## {section}\n- detail\n\n"
    # Ensure SUGGESTED_PHASES has a numbered list item so _check_suggested_phases_detail
    # finds detail under the heading (the loop appends a "- detail" bullet which already
    # satisfies the list-pattern regex, but be explicit for clarity).
    fake_research_notes += "1. Phase one detail\n"

    assert _check_research_notes_sections(fake_research_notes) is True
    assert _check_suggested_phases_detail(fake_research_notes) is True
```

## Files referenced but NOT modified

- `src/superclaude/cli/prd/prompts.py` — debate verdict A explicitly rejects rewriting the prompt; it's already aligned with upstream.
- `src/superclaude/skills/prd/SKILL.md` — upstream source of truth; the gate was wrong, not upstream.
- `src/superclaude/cli/prd/models.py` — imported by the new test for `PrdConfig`. No edit; reference only.
- `tests/cli/prd/__init__.py` — exists; no edit.

## Summary

4 atomic changes, all under `src/superclaude/cli/prd/` and `tests/cli/prd/`:

- Edit A: rewrite `_RESEARCH_REQUIRED_SECTIONS` list literal at gates.py:102-110
- Edit B: widen regex `\s+` → `[\s_]+` at gates.py:134-138 (inside `_check_suggested_phases_detail`)
- Edit C: rewrite test_gates.py:50-86 fixture text to the new schema
- Edit D: create new file tests/cli/prd/test_research_notes_roundtrip.py (~70 lines)

All verbatim text confirmed in the immediately preceding adversarial-debate turn. No further file reads required to begin editing.
