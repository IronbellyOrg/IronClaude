"""Pins for the review-prompt overrides removed for issue #346 (phase P1).

Evidence: the coordinator briefs of the #346 experiments ("assume defects
remain", "any finding of any severity is FAIL") overrode the #427 Review Loop,
and finding quotas ("at least N errors") plus "a zero is suspect" wording in
the output style, the rf-qa agents and the task templates pushed reviewers to
invent findings. This module pins the replacement wording and a brief lint.
The two fixtures ``review_brief_t07_original.txt`` and
``review_brief_t09_original.txt`` are byte copies of the experiment's original
review briefs (T07, T09) and must keep being flagged.

Enforcement type: STATIC - assertions over tracked primitive text.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_FIXTURES = Path(__file__).resolve().parent / "fixtures"
STYLE = _REPO / "src/superclaude/output-styles/pragmatic.md"
GUIDE = _REPO / "src/superclaude/core/HOW-WE-WORK.md"
GUIDE_TWIN = _REPO / "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md"


def _flat(text: str) -> str:
    return " ".join(text.split())


# --- brief lint ------------------------------------------------------------

BRIEF_VIOLATIONS = {
    "any-severity FAIL": re.compile(
        r"any (finding|issue)s? of any severity (is|means|results in)? ?FAIL",
        re.IGNORECASE,
    ),
    "assume defects remain": re.compile(
        r"assume (that )?(defects|errors|mistakes|issues) (remain|exist)",
        re.IGNORECASE,
    ),
    "finding quota": re.compile(
        r"(at least|a minimum of|no fewer than) (N|\d+|\[N\]) "
        r"(errors|findings|defects|issues)",
        re.IGNORECASE,
    ),
    "apply all findings": re.compile(r"apply all findings", re.IGNORECASE),
}

# Phrases that appear only inside a prohibition ("Never put ...") are allowed in
# the guide's explanation, so the lint is run on the two quoted briefs only.


def lint_brief(text: str) -> list[str]:
    flat = _flat(text)
    return [name for name, rx in BRIEF_VIOLATIONS.items() if rx.search(flat)]


def _guide_briefs() -> dict[str, str]:
    text = GUIDE.read_text(encoding="utf-8")
    found = {}
    for label in ("Review brief", "Revise brief"):
        m = re.search(rf'- {label}: "([^"]+)"', text)
        assert m, f"HOW-WE-WORK.md has no quoted {label.lower()}"
        found[label] = m.group(1)
    return found


@pytest.mark.parametrize(
    "fixture",
    ["review_brief_t07_original.txt", "review_brief_t09_original.txt"],
)
def test_lint_flags_the_original_experiment_briefs(fixture):
    hits = lint_brief((_FIXTURES / fixture).read_text(encoding="utf-8"))
    assert "any-severity FAIL" in hits, fixture
    assert "assume defects remain" in hits, fixture


@pytest.mark.parametrize(
    "scratch,expected",
    [
        ("any finding of any severity is FAIL", "any-severity FAIL"),
        ("Assume defects remain and look for them.", "assume defects remain"),
        ("Assume this document has at least N errors.", "finding quota"),
        ("Find at least 10 findings.", "finding quota"),
        ("Then apply all findings to the spec.", "apply all findings"),
    ],
)
def test_lint_matcher_fires(scratch, expected):
    assert expected in lint_brief(scratch)


def test_lint_ignores_the_new_wording():
    assert not lint_brief(
        "Minor findings are notes and never fail the review. "
        "Report concrete wrong outcomes, not a minimum number of findings."
    )


def test_guide_ships_both_briefs_and_they_pass_the_lint():
    briefs = _guide_briefs()
    for label, text in briefs.items():
        assert lint_brief(text) == [], label
    review, revise = briefs["Review brief"], briefs["Revise brief"]
    assert "resolved, open or regressed" in review
    assert "never fail the review" in review
    assert "not a minimum number of findings" in review
    assert "return incomplete" in review
    assert "do not start another review" in review
    assert "Prefer deleting or narrowing" in revise
    assert "cite the finding id" in revise
    assert "bytes added and deleted" in revise
    assert "do not award yourself a PASS" in revise


def test_guide_and_plugin_twin_are_byte_equal():
    assert GUIDE.read_bytes() == GUIDE_TWIN.read_bytes()


# --- quota and suspicion wording is gone -------------------------------------

REMOVED_PHRASES = (
    "at least N errors",
    "at least [N]",
    "{error_target}",
    "adversarial position",
    "with suspicion, not satisfaction",
    "surfaces zero issues as suspect",
    "Ship NO partial or simplified versions",
)


def _scan(trees=("src", "plugins")) -> list[str]:
    hits = []
    for tree in trees:
        for path in sorted((_REPO / tree).rglob("*")):
            if (
                not path.is_file()
                or path.suffix not in {".md", ".yaml", ".yml", ".txt", ".py"}
                or "__pycache__" in path.parts
            ):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for n, line in enumerate(text.splitlines(), 1):
                for phrase in REMOVED_PHRASES:
                    if phrase.lower() in line.lower():
                        hits.append(f"{path.relative_to(_REPO)}:{n}: {phrase!r}")
    return hits


def test_removed_quota_and_suspicion_wording_does_not_return():
    hits = _scan()
    assert not hits, "removed review wording survives:\n" + "\n".join(hits)


def test_scan_matcher_would_catch_the_old_text(tmp_path):
    # guards against a scan that silently matches nothing
    old = 'Assume this document has at least N errors. Find them.'
    assert any(p.lower() in old.lower() for p in REMOVED_PHRASES)


# --- replacement wording present ----------------------------------------------


def test_style_allows_evidence_backed_zero_findings():
    flat = _flat(STYLE.read_text(encoding="utf-8"))
    assert "A zero-finding result is valid." in flat
    assert "MUST state what it checked" in flat
    assert "Never invent a finding to avoid a zero" in flat
    assert "an unreadable or missing input is incomplete, not zero" in flat
    assert "never to meet a quota" in flat


def test_style_allows_deleting_redundant_text():
    flat = _flat(STYLE.read_text(encoding="utf-8"))
    assert "Ship NO stubs or partial versions of required behaviour" in flat
    assert (
        "Removing or narrowing redundant text, rules or mechanisms is allowed "
        "when every stated requirement is still met" in flat
    )


@pytest.mark.parametrize(
    "rel",
    [
        "src/superclaude/agents/rf-qa.md",
        "src/superclaude/agents/rf-qa-qualitative.md",
        "src/superclaude/templates/documents/agent_template_qa.md",
    ],
)
def test_qa_agents_use_the_independent_stance(rel):
    flat = _flat((_REPO / rel).read_text(encoding="utf-8"))
    assert "**Independent stance**" in flat, rel
    assert "there is no minimum count" in flat, rel
    assert "do not invent findings to avoid a zero" in flat, rel


@pytest.mark.parametrize(
    "rel",
    [
        "src/superclaude/skills/task/SKILL.md",
        "src/superclaude/skills/tech-reference/SKILL.md",
        "src/superclaude/skills/tech-research/SKILL.md",
        "src/superclaude/templates/workflow/01_mdtm_template_generic_task.md",
        "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md",
    ],
)
def test_lens_prompts_state_no_minimum_count(rel):
    flat = _flat((_REPO / rel).read_text(encoding="utf-8"))
    assert "no minimum count" in flat, rel
