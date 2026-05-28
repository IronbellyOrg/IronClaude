"""TEST-003 — TB-Add-8 per-item Context evidence binding (NFR-CONV.7 preservation).

Re-runs the M1 three-fixture triple (bare-path FAIL / file:line PASS /
justified-absence PASS) against M2-generated MDTM that now carries the
FR-CONV.2 ``## Execution Context`` header. Backs T02.10 / D-0024: the
M2 header introduction must NOT relax per-item evidence binding, and
TB-Add-8 error citations must continue to refer to per-item Context
fields (not the header byte range).

TB-Add-8 rule source-of-truth:
- ``src/superclaude/agents/rf-qa.md:310``
- ``src/superclaude/skills/task-builder/SKILL.md:1073`` (A.10 prompt)
- ``src/superclaude/skills/task-builder/SKILL.md:1826`` (validation checklist)

Run: ``uv run pytest tests/audit/test_evidence_bound_tb_add_8.py -v``
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "execution_context"

BARE_PATH_FIXTURE = FIXTURE_DIR / "evidence_bound_bare_path.md"
FILE_LINE_FIXTURE = FIXTURE_DIR / "evidence_bound_file_line.md"
JUSTIFIED_ABSENCE_FIXTURE = FIXTURE_DIR / "evidence_bound_justified_absence.md"

HEADING = "## Execution Context"

FILE_LINE_RE = re.compile(r"[\w./-]+\.\w+:\d+")
EVIDENCE_ABSENCE_RE = re.compile(r"<!--\s*evidence-absence:")
CODE_SURFACE_RE = re.compile(r"`[^`]*\b(?:src/|\.py|\.md|\.\w+:\d+)[^`]*`|src/[\w./-]+|`\w+\.\w+`")


@dataclass
class ContextItem:
    item_id: str
    line_number: int
    paragraph: str


@dataclass
class TBAdd8Result:
    item_id: str
    line_number: int
    verdict: str
    reason: str
    cited_location: str


def _header_range(text: str) -> tuple[int, int]:
    """Return the (start_line, end_line) of the ``## Execution Context`` block.

    end_line is the line index of the first ``---`` separator after the
    heading (inclusive). Both indices are 1-based to align with grep
    output. Returns (-1, -1) when no header is present.
    """
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == HEADING)
    except StopIteration:
        return (-1, -1)
    end = start + 1
    while end < len(lines) and lines[end].strip() != "---":
        end += 1
    return (start + 1, end + 1)


def _iter_per_item_context(text: str) -> List[ContextItem]:
    """Yield per-item Context paragraphs, skipping the ``## Execution Context`` header range.

    A per-item Context paragraph is a line matching ``- **Context**:`` (or
    ``  - **Context**:``) under a checklist item like ``- [ ] **N.M —
    ...**``. Per the MDTM template at SKILL.md:1764, the Context field is
    the first sub-bullet of each checklist item.
    """
    lines = text.splitlines()
    header_start, header_end = _header_range(text)
    in_header = False
    current_item_id: Optional[str] = None
    _current_item_line: int = -1  # noqa: F841  # intentional initialization for clarity
    item_re = re.compile(r"^\s*-\s*\[[ x]\]\s*\*\*([\d.]+)\s+—")
    context_re = re.compile(r"^\s*-\s*\*\*Context\*\*\s*:\s*(.*)$")
    out: List[ContextItem] = []
    for idx, raw in enumerate(lines, start=1):
        if header_start != -1 and header_start <= idx <= header_end:
            in_header = True
            continue
        if in_header and idx > header_end:
            in_header = False
        m_item = item_re.match(raw)
        if m_item:
            current_item_id = m_item.group(1)
            _current_item_line = idx  # noqa: F841  # intentional capture for debugging/clarity
            continue
        m_ctx = context_re.match(raw)
        if m_ctx and current_item_id is not None:
            paragraph = m_ctx.group(1)
            # Gather continuation lines that belong to this Context bullet
            j = idx
            while j < len(lines):
                nxt = lines[j]
                if not nxt.strip():
                    break
                if re.match(r"^\s*-\s+\*\*", nxt):
                    break
                if re.match(r"^\s*-\s*\[[ x]\]", nxt):
                    break
                paragraph += "\n" + nxt
                j += 1
            out.append(ContextItem(current_item_id, idx, paragraph))
            current_item_id = None
    return out


def tb_add_8(text: str) -> List[TBAdd8Result]:
    """Apply TB-Add-8 (rf-qa.md:310) to every per-item Context paragraph.

    Per the rule: every per-item Context field that references a code
    surface (function, class, module, config field, or specific file)
    MUST include at least one ``file:line`` citation OR a
    ``<!-- evidence-absence: ... -->`` justified-absence comment.

    The header range (``## Execution Context`` … ``---``) is exempt — the
    header carries no file:line by design (NFR-CONV.3); per-item Context
    fields remain the evidence venue (NFR-CONV.7).
    """
    results: List[TBAdd8Result] = []
    for item in _iter_per_item_context(text):
        paragraph = item.paragraph
        references_code = bool(CODE_SURFACE_RE.search(paragraph))
        has_file_line = bool(FILE_LINE_RE.search(paragraph))
        has_absence = bool(EVIDENCE_ABSENCE_RE.search(paragraph))
        if not references_code:
            results.append(
                TBAdd8Result(
                    item.item_id,
                    item.line_number,
                    "PASS",
                    "no code surface referenced",
                    f"Item {item.item_id} Context (line {item.line_number})",
                )
            )
            continue
        if has_file_line or has_absence:
            why = "file:line citation present" if has_file_line else "justified-absence comment present"
            results.append(
                TBAdd8Result(
                    item.item_id,
                    item.line_number,
                    "PASS",
                    why,
                    f"Item {item.item_id} Context (line {item.line_number})",
                )
            )
        else:
            results.append(
                TBAdd8Result(
                    item.item_id,
                    item.line_number,
                    "FAIL",
                    "no file:line citation and no evidence-absence justification",
                    f"Item {item.item_id} Context (line {item.line_number})",
                )
            )
    return results


class TestTBAdd8ThreeFixtureTriple:
    """The M1 TEST-003 triple re-run against M2-generated MDTM (NFR-CONV.7)."""

    def test_bare_path_fixture_exists(self):
        assert BARE_PATH_FIXTURE.is_file()

    def test_file_line_fixture_exists(self):
        assert FILE_LINE_FIXTURE.is_file()

    def test_justified_absence_fixture_exists(self):
        assert JUSTIFIED_ABSENCE_FIXTURE.is_file()

    def test_all_fixtures_carry_m2_execution_context_header(self):
        """Pre-condition: each fixture must include the FR-CONV.2 header so
        the test exercises TB-Add-8 in the M2-generated environment."""
        for fixture in (BARE_PATH_FIXTURE, FILE_LINE_FIXTURE, JUSTIFIED_ABSENCE_FIXTURE):
            text = fixture.read_text(encoding="utf-8")
            assert HEADING in text, (
                f"{fixture.name} must include the M2 `## Execution Context` header"
            )
            start, end = _header_range(text)
            assert start != -1 and end > start, (
                f"{fixture.name} header range must be locatable"
            )

    def test_bare_path_fails_tb_add_8(self):
        results = tb_add_8(BARE_PATH_FIXTURE.read_text(encoding="utf-8"))
        assert any(r.verdict == "FAIL" for r in results), (
            "bare-path fixture must produce at least one TB-Add-8 FAIL "
            f"(got {[(r.item_id, r.verdict, r.reason) for r in results]})"
        )

    def test_file_line_passes_tb_add_8(self):
        results = tb_add_8(FILE_LINE_FIXTURE.read_text(encoding="utf-8"))
        assert results, "file:line fixture must contain at least one Context item"
        assert all(r.verdict == "PASS" for r in results), (
            "file:line fixture must produce only TB-Add-8 PASS verdicts "
            f"(got {[(r.item_id, r.verdict, r.reason) for r in results]})"
        )

    def test_justified_absence_passes_tb_add_8(self):
        results = tb_add_8(JUSTIFIED_ABSENCE_FIXTURE.read_text(encoding="utf-8"))
        assert results, "justified-absence fixture must contain at least one Context item"
        assert all(r.verdict == "PASS" for r in results), (
            "justified-absence fixture must produce only TB-Add-8 PASS verdicts "
            f"(got {[(r.item_id, r.verdict, r.reason) for r in results]})"
        )


class TestTBAdd8CitesPerItemContextNotHeader:
    """TB-Add-8 error citations must continue to refer to per-item Context
    fields, NEVER to the M2 header byte range (NFR-CONV.7)."""

    def test_bare_path_error_cites_per_item_context_line(self):
        text = BARE_PATH_FIXTURE.read_text(encoding="utf-8")
        header_start, header_end = _header_range(text)
        fails = [r for r in tb_add_8(text) if r.verdict == "FAIL"]
        assert fails, "expected at least one FAIL for bare-path fixture"
        for r in fails:
            assert "Item" in r.cited_location and "Context" in r.cited_location, (
                f"TB-Add-8 error must cite per-item Context (got {r.cited_location!r})"
            )
            assert not (header_start <= r.line_number <= header_end), (
                f"TB-Add-8 error line {r.line_number} must NOT fall inside the header "
                f"range [{header_start}, {header_end}]"
            )

    def test_header_range_never_yields_tb_add_8_verdict(self):
        """The ## Execution Context block carries no file:line by design
        (NFR-CONV.3). TB-Add-8 must never enumerate any Context item whose
        line index sits inside the header range, regardless of fixture
        verdict."""
        for fixture in (BARE_PATH_FIXTURE, FILE_LINE_FIXTURE, JUSTIFIED_ABSENCE_FIXTURE):
            text = fixture.read_text(encoding="utf-8")
            start, end = _header_range(text)
            for r in tb_add_8(text):
                assert not (start <= r.line_number <= end), (
                    f"{fixture.name}: TB-Add-8 enumerated a Context inside the "
                    f"header range (line {r.line_number} ∈ [{start}, {end}])"
                )


class TestTBAdd8VerdictMatrixMatchesM1Baseline:
    """The M1 baseline matrix (bare=FAIL, file:line=PASS, absence=PASS) must
    hold byte-identically against the M2 fixtures."""

    def test_verdict_matrix(self):
        matrix = {
            "bare_path": (BARE_PATH_FIXTURE, "FAIL"),
            "file_line": (FILE_LINE_FIXTURE, "PASS"),
            "justified_absence": (JUSTIFIED_ABSENCE_FIXTURE, "PASS"),
        }
        observed = {}
        for label, (fixture, _expected) in matrix.items():
            results = tb_add_8(fixture.read_text(encoding="utf-8"))
            # Per-fixture aggregate verdict: FAIL if any FAIL, else PASS.
            aggregate = "FAIL" if any(r.verdict == "FAIL" for r in results) else "PASS"
            observed[label] = aggregate
        expected = {label: verdict for label, (_f, verdict) in matrix.items()}
        assert observed == expected, (
            f"M2 verdict matrix drifted from M1 baseline: expected {expected}, got {observed}"
        )
