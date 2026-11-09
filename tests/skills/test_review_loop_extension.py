"""Pins for the Review Loop extension of ``/sc:spec-panel`` (#346, phase P4).

Each clause answers a failure seen in the #346 experiments and is prose only: no
parser, script or state machine. The seven Review Loop bullets stay single lines
in their existing order (``test_spec_panel_review_loop.py``).

Enforcement type: STATIC - assertions over the text of both spec-panel copies.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)
spec_panel = pytest.mark.parametrize("rel", SPEC_PANELS)


def _flat(text: str) -> str:
    return " ".join(text.split())


def _bullet(rel: str, number: int) -> str:
    lines = (_REPO / rel).read_text(encoding="utf-8").splitlines()
    start = lines.index("## Review Loop") + 1
    return _flat(
        next(line for line in lines[start:] if line.startswith(f"{number}. **"))
    )


@spec_panel
def test_provenance_in_the_report_header(rel):
    mode = _bullet(rel, 1)
    assert "records the SHA-256 of the baseline and of the candidate" in mode
    assert "the reviewer model actually used" in mode
    assert "cannot be taken stops the run like an unreadable file" in mode
    assert "never fall back to a first review" in mode  # existing pin kept


@spec_panel
def test_fail_closed_on_a_missing_or_ambiguous_report(rel):
    verdict = _bullet(rel, 3)
    assert (
        "is missing, ambiguous or cites a finding id absent from the table" in verdict
    )
    assert "as `verdict: FAIL`, never as PASS and never as zero findings" in verdict


@spec_panel
def test_no_edits_between_the_second_fix_and_the_third_review(rel):
    cap = _bullet(rel, 4)
    assert "after the second fix cycle only the third review runs" in cap
    assert (
        "a severity or necessity audit before it only reports and edits nothing" in cap
    )
    assert "at most 2 fix cycles (3 reviews)" in cap  # cap unchanged


@spec_panel
def test_identity_and_open_counting_of_prior_findings(rel):
    out = _bullet(rel, 5)
    assert "each keeps its id from the prior report" in out
    assert "deferred or withdrew" in out
    assert "cannot match to a prior id with certainty, counts as open" in out
    assert "`resolved|open|regressed`" in out  # existing vocabulary kept


@spec_panel
def test_scoped_pass_names_its_coverage(rel):
    out = _bullet(rel, 5)
    assert "`scoped PASS: changed lines + prior blockers`" in out
    assert "whole-document assurance needs a separate, labelled first review" in out
    assert "never start a fourth review" in out


@spec_panel
def test_reviser_prefers_deleting_and_reports_gross_bytes(rel):
    reviser = _bullet(rel, 6)
    assert "prefers deleting or narrowing to adding" in reviser
    assert "byte size before and after" in reviser  # existing pin kept
    assert "bytes added and deleted per finding id" in reviser
    assert not re.search(r"\b\d+ ?(bytes|words)\b", reviser), "no numeric budget"


@spec_panel
def test_brief_cannot_regrade_or_authorize_minor_edits(rel):
    prec = _bullet(rel, 7)
    assert (
        "may not widen it past the changed lines and the prior blocking findings"
        in prec
    )
    assert (
        "cannot make a minor or Medium finding fail the review or authorize editing one"
        in prec
    )
    assert 'including through "apply all findings"' in prec
    assert "the report names any brief clause it overrode" in prec


@spec_panel
def test_section_adds_no_script_or_parser_requirement(rel):
    lines = (_REPO / rel).read_text(encoding="utf-8").splitlines()
    start = lines.index("## Review Loop") + 1
    end = next(i for i in range(start, len(lines)) if lines[i].startswith("## "))
    section = _flat("\n".join(lines[start:end])).lower()
    for word in ("parser", "script", "state machine", "transcript", "asynchronous"):
        assert word not in section, word
