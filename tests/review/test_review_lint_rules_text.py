"""Rules-file pins for the PN2 lint insertions (#346). Static text assertions only."""

from __future__ import annotations

import ast
import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
RULES_FILE = _REPO / "src/superclaude/rules/prompts/document_review_loop_prompts.md"
PLACEMENT_TEST = _REPO / "tests/skills/test_review_brief_placement.py"

INSERTION_P = (
    "- **Lint evidence**: before each review the coordinator runs `superclaude review lint <candidate> "
    "--format md --out <review dir>/lint-<N>.md` and passes the file as the value lint. When the brief gives lint, "
    "read that file first and address each lint id in the report: confirm it as a finding graded with the grading "
    "check, or dismiss it with the quote that shows it is not a defect. A lint id never fails the review by itself."
)
INSERTION_Q = (
    "- **Lint evidence**: when the brief gives lint, the file was produced on the revised candidate; address each "
    "lint id whose lines the diff touches and each lint id that is new since the prior review, as in the first review."
)
FIRST_ANCHOR = "Write `review: 1 of 3` once"
RE_ANCHOR = "Follow the re-review core below in order"

# The finding-quota scan of tests/skills/test_review_prompt_overrides.py.
QUOTA_PATTERN = re.compile(
    r"\b(?:assume|find)\b[^.\n\"]{0,120}?\bat least (?:N|\[N\]|\d+|one)\b"
    r"|\bAdversarial target:\*\* at least"
    r"|\bat least \d+ [a-z-]+ (?:are|were|is) (?:expected|assumed)\b",
    re.IGNORECASE,
)


def _lines() -> list[str]:
    return RULES_FILE.read_text(encoding="utf-8").split("\n")


def test_insertion_p_present_once_right_after_the_first_review_anchor():
    lines = _lines()
    assert lines.count(INSERTION_P) == 1
    anchors = [i for i, ln in enumerate(lines) if ln.startswith(FIRST_ANCHOR)]
    assert len(anchors) == 1
    assert lines[anchors[0] + 1] == INSERTION_P


def test_insertion_q_present_once_right_after_the_re_review_anchor():
    lines = _lines()
    assert lines.count(INSERTION_Q) == 1
    anchors = [i for i, ln in enumerate(lines) if ln.startswith(RE_ANCHOR)]
    assert len(anchors) == 1
    assert lines[anchors[0] + 1] == INSERTION_Q


def test_exactly_two_lint_lines():
    assert sum(1 for ln in _lines() if "Lint evidence" in ln) == 2


def test_rules_file_names_no_src_path_and_trips_no_quota_scan():
    text = RULES_FILE.read_text(encoding="utf-8")
    assert "src/superclaude" not in text
    assert not QUOTA_PATTERN.search(" ".join(text.split()))
    assert "superclaude review lint" in text


def test_every_placement_token_is_still_present():
    """Parse the placement test and require each token of its rules-file tuple."""
    tree = ast.parse(PLACEMENT_TEST.read_text(encoding="utf-8"))
    func = next(
        n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "test_rules_file_holds_all_prompt_text"
    )
    tokens: list[str] = []
    for node in ast.walk(func):
        if isinstance(node, ast.For) and isinstance(node.iter, ast.Tuple):
            tokens.extend(
                e.value for e in node.iter.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)
            )
    assert len(tokens) >= 25, tokens
    text = RULES_FILE.read_text(encoding="utf-8")
    missing = [t for t in tokens if t not in text]
    assert not missing, missing
