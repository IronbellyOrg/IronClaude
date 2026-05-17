"""Unit coverage for `_extract_component_context` in obligation_scanner.

Pins the three local-variable assignments restored in `obligation_scanner.py:445`
(merge commit `3ac7bb6` had silently dropped them, producing a `NameError` at
the P4 fallback whenever no prior priority matched). The two cases below
exercise the Priority-4 path that depends on `line` and `line_label`.

Source of truth for the restored block: the pre-merge revision at
`f336da1:src/superclaude/cli/roadmap/obligation_scanner.py` lines 358-376.
"""

from __future__ import annotations

from superclaude.cli.roadmap.obligation_scanner import (
    _TABLE_SEPARATOR_RE,
    _extract_component_context,
)


def test_p4_fallback_lowercase_shell_line_no_nameerror():
    """Case A — file 01 hypothesis A: an all-lowercase shell line with no
    backticks and no capitalized terms must traverse Priority-4 and return
    the lowercased line, not raise `NameError`.
    """
    text = "- grep -rn 'placeholder' src/superclaude/"
    pos = text.index("placeholder")
    result = _extract_component_context(text, pos)
    assert isinstance(result, str)
    # Fallback contract: P4 returns the lowercased line when no cap term wins.
    assert result == text.lower()


class TestTableSeparatorRegex:
    """Pins `_TABLE_SEPARATOR_RE` (T2.1/T2.2) — distinguishing markdown
    table separator rows (skip) from data rows (process).

    The old `stripped_context.startswith("|")` predicate was overbroad:
    it skipped every line beginning with `|`, including data rows, which
    blocked Layer 3a/3b detectors from running on table-cell fixtures.
    The new regex matches separator rows only.
    """

    def test_plain_separator_matches(self):
        assert _TABLE_SEPARATOR_RE.match("|---|---|") is not None

    def test_alignment_markers_left_and_right_match(self):
        assert _TABLE_SEPARATOR_RE.match("| :--- | ---: |") is not None

    def test_center_alignment_matches(self):
        assert _TABLE_SEPARATOR_RE.match("| :---: |") is not None

    def test_data_row_does_not_match(self):
        # The fixture that test 02 exercises — must NOT be skipped.
        assert (
            _TABLE_SEPARATOR_RE.match("| 2.2.1 | Scaffold cmd | FR-001 |")
            is None
        )


def test_extract_component_context_smoke_on_data_row():
    """T2.4 smoke assertion: `_extract_component_context` must return a
    non-empty, non-malformed string on a pipe-delimited data row.

    Sentinel guard against the predicted secondary defect surfaced in
    Stage 4 file 02's Con round: once the predicate narrows, table data
    rows reach the component-context helper for the first time; verify
    that helper handles them gracefully.
    """
    text = "| 2.2.1 | Scaffold command file | FR-001 |"
    pos = text.index("Scaffold")
    result = _extract_component_context(text, pos)
    assert isinstance(result, str)
    assert result  # non-empty


def test_p4_rejects_line_label_via_lowercase_equality():
    """Case B — `line_label` rejection logic must be reachable.

    The fixture is a field-labeled line like `Component: Placeholder Module`.
    The P4 loop sees `Placeholder Module` as a candidate cap-term; the
    `line_label` of the line resolves to `component`. Because the cap-term's
    lowercase form (`placeholder module`) does not equal the label, P4
    returns it. The point of this test is not the specific return value,
    but proof that `line_label` resolution did not crash on a NameError.
    """
    text = "Component: Placeholder Module"
    pos = text.index("Placeholder")
    result = _extract_component_context(text, pos)
    assert isinstance(result, str)
    # Either the cap-term or the lowercased line is acceptable — both prove
    # the P4 block executed without raising.
    assert result  # non-empty
