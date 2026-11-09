"""Pins for the consequence-based severity mapping and Medium tier (#346, phase P2).

Findings are graded by consequence, not label. On ``/sc:spec-panel``'s scale
CRITICAL is blocking; MAJOR and FR-8/FR-9 are blocking only when they name a
concrete wrong outcome or a security, data-loss or safety-boundary risk,
otherwise they are Medium warnings listed under ``follow-up candidates``; MINOR
is a note. The boundary table asks for one row per applicable input class, not a
six-row quota. The S1-S5 bullets of ``pragmatic.md`` stay byte-identical (ten
files copy them verbatim); the Medium tier is added after S5.

Enforcement type: STATIC - assertions over tracked primitive text.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.skills.test_review_severity_rule import canonical_rule_bullets

_REPO = Path(__file__).resolve().parents[2]
STYLE = _REPO / "src/superclaude/output-styles/pragmatic.md"
SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)

spec_panel = pytest.mark.parametrize("rel", SPEC_PANELS)


def _flat(text: str) -> str:
    return " ".join(text.split())


def _text(rel: str) -> str:
    return _flat((_REPO / rel).read_text(encoding="utf-8"))


def _bullet(rel: str, number: int) -> str:
    lines = (_REPO / rel).read_text(encoding="utf-8").splitlines()
    start = lines.index("## Review Loop") + 1
    prefix = f"{number}. **"
    return next(line for line in lines[start:] if line.startswith(prefix))


# --- spec-panel Review Loop ---------------------------------------------------


@spec_panel
def test_grading_bullet_grades_by_consequence(rel):
    grading = _flat(_bullet(rel, 2))
    for literal in (
        "grade by consequence, not by label",
        "CRITICAL is blocking",
        "a MAJOR or an FR-8/FR-9 finding is blocking only if it names a concrete wrong outcome",
        "security, data-loss or safety-boundary risk",
        "otherwise it is Medium (a warning listed under `follow-up candidates`)",
        "MINOR is a note",
        "never appear in the Reviser brief",
    ):
        assert literal in grading, literal
    assert "CRITICAL and FR-8/FR-9 findings are blocking" not in grading


@spec_panel
def test_verdict_bullet_routes_follow_up_candidates(rel):
    verdict = _flat(_bullet(rel, 3))
    for literal in (
        "minor notes and Medium warnings allowed",
        "`follow-up candidates`",
        "asks the user once per loop",
        "creates none without the user's answer",
        "an `--unattended` run only records the list",
    ):
        assert literal in verdict, literal


@spec_panel
def test_reviser_brief_still_lists_only_blocking_ids(rel):
    assert "listing only blocking finding ids" in _flat(_bullet(rel, 6))


# --- boundary table -------------------------------------------------------------


@spec_panel
def test_boundary_table_is_one_row_per_applicable_class(rel):
    text = _text(rel)
    assert "one row per input class that applies to the guard" in text
    assert "the six classes below are the menu, not a quota" in text
    assert "minimum 6 input condition rows per guard" not in text


@spec_panel
def test_fr8_fr9_grade_by_outcome_not_by_status_cell(rel):
    text = _text(rel)
    assert "**MAJOR** severity minimum" not in text
    fr8 = text[text.index("**FR-8: GAP Status Rule**") :]
    fr8 = fr8[: fr8.index("**FR-10")]
    assert "It is blocking when it names a concrete wrong outcome" in fr8
    assert "otherwise it is Medium" in fr8
    assert "graded like FR-8" in fr8


@spec_panel
def test_fr10_gate_survives_with_applicable_rows(rel):
    text = _text(rel)
    assert "**FR-10: Synthesis-Blocking Gate**" in text
    assert "This is a hard gate, not advisory." in text
    assert "left out with its one-line reason" in text


# --- pragmatic.md ----------------------------------------------------------------


def test_medium_tier_follows_the_untouched_s1_s5_bullets():
    lines = STYLE.read_text(encoding="utf-8").splitlines()
    s5 = canonical_rule_bullets()[4]
    i = lines.index(s5)
    medium, scale = lines[i + 1], lines[i + 2]
    flat = _flat(medium)
    assert flat.startswith(
        "- Among minor findings, one that describes a real but non-blocking weakness"
    )
    assert "is Medium" in flat and "never fails a review" in flat
    assert "never appears in a reviser brief" in flat
    assert "asks the user once per loop whether to open an issue" in flat
    assert "no issue is created without the user's answer" in flat
    assert "only records the list" in flat
    flat = _flat(scale)
    assert flat.startswith("- On `/sc:spec-panel`'s CRITICAL / MAJOR / MINOR scale")
    assert "MAJOR is blocking only when it names a concrete wrong outcome" in flat
    assert (
        "a reviewer never suppresses such a finding because its label says Medium or minor"
        in flat
    )


def test_security_and_data_loss_risk_is_never_downgraded_by_label():
    flat = _flat(STYLE.read_text(encoding="utf-8"))
    assert (
        "a finding of any label whose consequence is a security, data-loss or safety-boundary risk is blocking"
        in flat
    )
