"""Contract #6 — exactly ONE canonical frontmatter parser in the gate layer.

Before R1.6 the pipeline carried two divergent frontmatter parsers
(``roadmap/gates.py:_parse_frontmatter`` and ``pipeline/gates.py:_check_frontmatter``)
that could return different parses — and therefore different gate verdicts —
for the same artifact. Step 11.2 collapsed both into the single canonical
:func:`superclaude.cli.pipeline.frontmatter.extract_frontmatter`.

Because there is now only ONE gate parser, "consistency across parsers"
degenerates to "determinism of the one parser": the same input must always
produce the same output. This module enforces that, plus the structural
invariants that keep the gate layer single-parser:

1. The canonical parser is deterministic across a corpus of 50+ blobs.
2. Both legacy gate parsers are gone from the source.
3. Both gate-layer modules route through the one canonical parser.
4. The retained cross-cutting parsers are DISTINCT-PURPOSE (different return
   contracts), explicitly enumerated so a future regression that re-adds a
   duplicate *gate* parser is catchable.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.pipeline.frontmatter import extract_frontmatter

_SRC_ROOT = (
    Path(__file__).resolve().parent.parent.parent / "src" / "superclaude" / "cli"
)
_FIXTURE_DIR = (
    Path(__file__).resolve().parent / "fixtures" / "recurrence" / "frontmatter_parser"
)


def _build_corpus() -> list[str]:
    """Generate 50+ frontmatter blobs spanning the parser's input space."""
    blobs: list[str] = []

    # 1. Plain top-level scalar frontmatter, varying field counts.
    for n in range(1, 31):
        lines = "\n".join(f"key{i}: value{i}" for i in range(n))
        blobs.append(f"---\n{lines}\n---\nbody text\n")

    # 1b. Quoted-value variants across field counts (quote stripping path).
    for n in range(1, 16):
        lines = "\n".join(f'key{i}: "value {i}"' for i in range(n))
        blobs.append(f"---\n{lines}\n---\nbody text\n")

    # 2. Quoted values (single + double), which the parser must strip.
    blobs.append('---\ntitle: "Quoted Title"\nratio: "1:1"\n---\nbody\n')
    blobs.append("---\ntitle: 'Single Quoted'\nratio: '2:1'\n---\nbody\n")
    blobs.append('---\nmixed: "value"\nbare: value\n---\nbody\n')

    # 3. Preamble before frontmatter (CONV comments / chat preamble) — tolerated.
    blobs.append(
        "Some preamble line.\n\n---\ntitle: After Preamble\ncount: 3\n---\nbody\n"
    )
    blobs.append("<!-- CONV: generated -->\n---\nid: M1\nstatus: done\n---\nbody\n")

    # 4. Nested list items — only top-level keys are captured.
    blobs.append("---\ntitle: With List\nitems:\n  - id: A\n  - id: B\n---\nbody\n")
    blobs.append("---\ntotal_analyzed: 5\nrouting_fix_roadmap: FR-1, FR-2\n---\nbody\n")

    # 5. No frontmatter / malformed — parser returns None deterministically.
    blobs.append("# Just a heading\n\nSome text, no frontmatter.\n")
    blobs.append("---\nno closing delimiter\nkey: value\n")
    blobs.append("")
    blobs.append("---\n---\n")  # empty / horizontal-rule-only block

    # 6. Values containing colons (partition on first colon only).
    blobs.append("---\nurl: https://example.com/path\ntime: 12:30:00\n---\nbody\n")

    # 7. Whitespace around delimiters and values.
    blobs.append("---  \n  key:   spaced value   \n---  \nbody\n")

    return blobs


_CORPUS = _build_corpus()


# Golden (input, expected-output) pairs — hand-verified. Unlike the
# determinism loop (which a broken parser returning ``{}`` would still pass),
# these pin the ACTUAL parse, so a behavioral regression is caught. Includes
# CRLF / CR cases that guard the line-ending-normalization fix.
_GOLDEN: list[tuple[str, dict[str, str] | None]] = [
    ("---\ntitle: Hi\ncount: 5\n---\nbody\n", {"title": "Hi", "count": "5"}),
    ('---\nratio: "1:1"\n---\n', {"ratio": "1:1"}),
    ("---\nratio: '2:1'\n---\n", {"ratio": "2:1"}),
    ("---\ntitle:\n---\n", {"title": ""}),
    ("---\nurl: https://x.com/p\n---\n", {"url": "https://x.com/p"}),
    ("preamble\n\n---\nid: M1\n---\nbody\n", {"id": "M1"}),
    (
        "<!-- CONV: gen -->\n---\nid: M1\nstatus: done\n---\n",
        {"id": "M1", "status": "done"},
    ),
    ("---\ntitle: T\nitems:\n  - id: A\n  - id: B\n---\n", {"title": "T", "items": ""}),
    ("---  \nkey:   spaced value   \n---  \nbody\n", {"key": "spaced value"}),
    # CRLF: must parse identically to the LF form (line-ending normalization).
    ("---\r\ntitle: Hi\r\ncount: 5\r\n---\r\nbody\r\n", {"title": "Hi", "count": "5"}),
    # Bare-CR line endings (old splitlines() handled these too).
    ("---\rtitle: Hi\r---\r", {"title": "Hi"}),
    # Absent / unterminated / empty → None (deterministic).
    ("# heading only\n", None),
    ("---\nkey: value with no closing delimiter\n", None),
    ("", None),
    ("---\n---\n", None),  # horizontal-rule-only block (no top-level key)
]


class TestCanonicalParserDeterminism:
    """Contract #6 invariant 1: the one parser is deterministic."""

    def test_corpus_size(self):
        assert len(_CORPUS) >= 50, (
            f"Corpus must have >= 50 blobs (consistency-of-one); got {len(_CORPUS)}"
        )

    @pytest.mark.parametrize("blob", _CORPUS, ids=range(len(_CORPUS)))
    def test_parse_is_deterministic(self, blob: str):
        """Parsing the same blob twice yields identical results."""
        first = extract_frontmatter(blob)
        second = extract_frontmatter(blob)
        assert first == second

    def test_known_fields_extracted(self):
        fm = extract_frontmatter('---\ntotal_analyzed: 5\nratio: "1:1"\n---\nbody\n')
        assert fm == {"total_analyzed": "5", "ratio": "1:1"}

    def test_preamble_tolerated(self):
        fm = extract_frontmatter("preamble\n\n---\nid: M1\n---\nbody\n")
        assert fm == {"id": "M1"}

    def test_no_frontmatter_returns_none(self):
        assert extract_frontmatter("# heading only\n") is None

    def test_nested_lines_ignored(self):
        fm = extract_frontmatter("---\ntitle: T\nitems:\n  - id: A\n---\nbody\n")
        # Only top-level keys; the nested ``- id: A`` is not a top-level key.
        assert fm == {"title": "T", "items": ""}


class TestCanonicalParserGoldenOutputs:
    """Contract #6 invariant 1 (strengthened): the one parser produces the
    correct parse, not merely a *stable* one.

    The determinism loop above cannot fail for any pure function (``f(x) ==
    f(x)``), so it would pass even for a parser that always returned ``{}``.
    These golden ``(input, expected)`` pairs assert the actual output and so
    catch behavioral regressions (e.g. the CRLF line-ending case).
    """

    @pytest.mark.parametrize("blob, expected", _GOLDEN, ids=range(len(_GOLDEN)))
    def test_parse_matches_golden(self, blob: str, expected: dict[str, str] | None):
        assert extract_frontmatter(blob) == expected

    def test_crlf_parses_identically_to_lf(self):
        lf = "---\na: 1\nb: 2\n---\nbody\n"
        crlf = lf.replace("\n", "\r\n")
        assert extract_frontmatter(crlf) == extract_frontmatter(lf)
        assert extract_frontmatter(crlf) == {"a": "1", "b": "2"}


class TestSingleGateParserInvariant:
    """Contract #6 invariants 2 + 3: one parser, both gate layers share it."""

    def test_legacy_roadmap_parser_removed(self):
        src = (_SRC_ROOT / "roadmap" / "gates.py").read_text(encoding="utf-8")
        assert "def _parse_frontmatter" not in src, (
            "roadmap/gates.py must no longer define its own frontmatter parser"
        )
        assert "def _strip_yaml_quotes" not in src

    def test_legacy_pipeline_parser_removed(self):
        src = (_SRC_ROOT / "pipeline" / "gates.py").read_text(encoding="utf-8")
        # The standalone regex parser body moved to frontmatter.py.
        assert "_FRONTMATTER_RE" not in src
        assert "_TOPLEVEL_KEY_RE" not in src

    def test_both_gate_layers_route_through_canonical_parser(self):
        roadmap_src = (_SRC_ROOT / "roadmap" / "gates.py").read_text(encoding="utf-8")
        pipeline_src = (_SRC_ROOT / "pipeline" / "gates.py").read_text(encoding="utf-8")
        assert (
            "from superclaude.cli.pipeline.frontmatter import extract_frontmatter"
            in roadmap_src
        )
        assert "from .frontmatter import extract_frontmatter" in pipeline_src
        assert "extract_frontmatter(content)" in pipeline_src


class TestDistinctPurposeParsersEnumerated:
    """Contract #6 invariant 4: retained parsers are distinct-purpose.

    These are NOT gate-frontmatter parsers — they have different return
    contracts and serve different layers. Enumerating them documents the
    intentional exceptions and catches a future regression that re-adds a
    duplicate *gate* parser under one of these names.
    """

    def test_spec_parser_is_structured_yaml(self):
        src = (_SRC_ROOT / "roadmap" / "spec_parser.py").read_text(encoding="utf-8")
        # Distinct purpose: full yaml.safe_load spec ingestion with warnings.
        assert "def parse_frontmatter" in src
        assert "yaml.safe_load" in src
        assert "DISTINCT-PURPOSE parser" in src

    def test_spec_patch_returns_raw_block(self):
        src = (_SRC_ROOT / "roadmap" / "spec_patch.py").read_text(encoding="utf-8")
        assert "def _extract_frontmatter" in src
        assert "DISTINCT-PURPOSE parser" in src

    def test_crosscutting_parsers_are_outside_gate_layer(self):
        # cli_portify + audit parsers exist but are not the gate parser; they
        # are flagged for the parser-consistency lint enumeration (Phase 13).
        assert (_SRC_ROOT / "cli_portify" / "utils.py").exists()
        assert (_SRC_ROOT / "audit" / "wiring_gate.py").exists()


class TestDisagreeingParsersFixture:
    """Seed hook for the historical disagreeing-parsers fixture (Phase 13).

    Phase 13 creates ``fixtures/recurrence/frontmatter_parser/`` with a case
    demonstrating the deleted variants disagreed. Until then this is a
    documented, skipped placeholder so the seed contract is explicit.
    """

    def test_canonical_parser_handles_historical_fixture_if_present(self):
        case = _FIXTURE_DIR / "disagreeing_parsers_case.md"
        if not case.exists():
            pytest.skip(
                "disagreeing-parsers fixture not yet created (Phase 13 seeds it)"
            )
        content = case.read_text(encoding="utf-8")
        # The one canonical parser is deterministic on the historical case.
        assert extract_frontmatter(content) == extract_frontmatter(content)
