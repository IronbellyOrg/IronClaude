"""Pinned behavior of ``superclaude review lint`` on the p5 documents (#346, PN2 Phase O).

These pin what the offline measurement found, including what the lint does NOT catch:
S2 (log deletion against retention), S3 (secret logged) and the FR-5 deletion are semantic
defects and produce no finding. A change that starts catching them must update these tests.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.review.lint import run_lint

FIX = Path(__file__).parent / "fixtures"


def _lint(name: str) -> dict:
    return run_lint((FIX / f"{name}.md").read_bytes())


def test_clean_and_minor_documents_have_no_findings():
    for name in ("clean", "minor"):
        assert _lint(name)["findings"] == [], name


def test_seeded_retry_conflict_is_the_only_finding():
    """S1 (retry 8 vs FR-3 5) is caught by KV; S2 and S3 are not reachable mechanically."""
    found = _lint("seeded")["findings"]
    assert [(f["check"], f["class"], f["lines"], f["other_lines"]) for f in found] == [
        ("KV", "possible", [39, 39], [13, 13])
    ]
    assert "8 times" in found[0]["message"] and "5 times" in found[0]["message"]


def test_removed_requirement_still_used_is_not_caught_known_miss():
    """FR-5 is deleted but only its payload (delivery_id) is still used; no id is referenced, so nothing dangles."""
    assert _lint("cand_deletion")["findings"] == []


def test_known_false_positive_inline_definition_is_flagged():
    """Known false positive (REF): an id defined inline in a table cell list is reported as undefined."""
    text = "## 1. Scope\n\n| Non-goals | NG-1 no daemon; NG-2 no writes |\n|---|---|\n\nSee NG-2.\n"
    flags = [f for f in run_lint(text.encode())["findings"] if f["check"] == "REF"]
    assert [f["message"] for f in flags] == [
        "NG-1 is referenced but never defined.",
        "NG-2 is referenced but never defined (2 references).",
    ]


def test_output_is_stable_for_the_fixtures():
    for name in ("clean", "seeded"):
        assert run_lint((FIX / f"{name}.md").read_bytes()) == run_lint((FIX / f"{name}.md").read_bytes())
