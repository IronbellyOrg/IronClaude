"""T04.04 -- ``findings_table_v1`` recipe tests (R-089 / COMP-017 / D-0071).

Covers four layers:

1. **Recipe surface**: ``FindingsTableV1.normalize`` produces a
   canonical 5-column markdown table (``ID | Locator | Finding |
   Detail | Action``) with auto-assigned ``F-NN`` IDs across all three
   findings-shape lens fixtures (refactor-find, edge-case-hunt,
   doc-completeness).

2. **REGISTRY**: the ``findings_table_v1`` slot resolves to a
   Recipe-conforming object (no longer the M2-era ``None`` sentinel)
   and the Wave-2 dispatcher routes a worker through it end-to-end.

3. **§7.4 salvage**: a ``parse_error`` worker with a recoverable body
   is promoted via ``salvaged=True``; a ``parse_error`` worker with
   neither findings nor notes stays failed.

4. **AC-011 boundary**: row order preserved, duplicates retained,
   every parsed row reaches the output (no scoring / dedup / reorder).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import superclaude.cli.swarm.recipes.findings_table_v1 as _ft
from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.normalize import normalize_wave2
from superclaude.cli.swarm.recipes import REGISTRY, NormalizedResult, Recipe
from superclaude.cli.swarm.recipes.findings_table_v1 import (
    CLAIM_CAP,
    DETAIL_CAP,
    FALLBACK_NOTES_CAP,
    FindingsTableV1,
    extract_notes,
    parse_findings_table,
    strip_frontmatter,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "findings_table_v1"

FIXED_GENERATED = "2026-06-01T11:19:39Z"
FIXED_CHECKSUM = "deadbeefcafe"
FIXED_TARGET = "/tmp/example/target.py"


def _run(
    raw: str,
    *,
    status: str = "success",
    lens: str = "refactor-find",
    tier: str = "T2-code",
    suspect: bool = False,
    elapsed_ms: int = 12345,
    model_id: str = "m",
    model_label: str = "M",
    caller_label: str = "",
    target: str = FIXED_TARGET,
) -> NormalizedResult:
    args: dict[str, Any] = {
        "status": status,
        "target": target,
        "target_checksum": FIXED_CHECKSUM,
        "target_truncated": False,
        "model_id": model_id,
        "model_label": model_label,
        "caller_label": caller_label,
        "elapsed_ms": elapsed_ms,
        "generated": FIXED_GENERATED,
        "lens": lens,
        "tier": tier,
        "suspect": suspect,
    }
    return FindingsTableV1().normalize(raw, args)


# ---------------------------------------------------------------------------
# 1 -- Recipe surface across the three findings-shape lens fixtures
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "filename,lens,tier,row_count",
    [
        ("refactor_find.raw.txt", "refactor-find", "T2-code", 3),
        ("edge_case_hunt.raw.txt", "edge-case-hunt", "T2-edge", 3),
        ("doc_completeness.raw.txt", "doc-completeness", "T2-doc", 4),
    ],
)
def test_recipe_renders_canonical_table_per_lens(
    filename: str, lens: str, tier: str, row_count: int
):
    raw = (FIXTURES_DIR / filename).read_text(encoding="utf-8")
    result = _run(raw, lens=lens, tier=tier)
    assert result.error is None
    assert result.salvaged is False
    text = result.text

    # Canonical header present.
    assert "| ID | Locator | Finding | Detail | Action |" in text
    assert "|----|---------|---------|--------|--------|" in text

    # Auto-assigned IDs F-01..F-NN, in order, with the right count.
    for i in range(1, row_count + 1):
        assert f"| F-{i:02d} |" in text
    assert f"| F-{row_count + 1:02d} |" not in text

    # Frontmatter records the lens + tier + finding_count.
    assert f'lens: "{lens}"' in text
    assert f'tier: "{tier}"' in text
    assert f"finding_count: {row_count}" in text

    # Notes section preserved.
    assert "## Notes" in text


def test_recipe_records_target_metadata_in_frontmatter():
    raw = (FIXTURES_DIR / "refactor_find.raw.txt").read_text(encoding="utf-8")
    result = _run(raw)
    assert FIXED_GENERATED in result.text
    assert FIXED_CHECKSUM in result.text
    assert "/tmp/example/target.py" in result.text
    # Slug appears in heading.
    assert "T2-Findings Table (refactor-find) — target" in result.text


def test_recipe_handles_empty_raw_body():
    result = _run("")
    assert result.text == ""
    assert result.salvaged is False
    assert result.error == "empty raw body"


def test_recipe_handles_whitespace_only_raw_body():
    result = _run("   \n  \n\t\n")
    assert result.text == ""
    assert result.salvaged is False
    assert result.error == "empty raw body"


def test_recipe_freeform_fallback_when_no_findings_and_no_notes_on_success():
    """Success worker with no parseable findings AND no Notes heading
    falls back to a Notes-only body (truncated body text) so the
    payload is never silently dropped."""
    raw = "Some prose from the model. No table, no Notes heading.\n"
    result = _run(raw, status="success")
    assert result.error is None
    assert result.salvaged is False
    # Falls back to body-as-notes.
    assert "Some prose from the model" in result.text
    # Table placeholder row rendered so the markdown table stays valid.
    assert "| F-00 |" in result.text


def test_recipe_uses_notes_only_fixture_via_fallback_path():
    raw = (FIXTURES_DIR / "notes_only.raw.txt").read_text(encoding="utf-8")
    result = _run(raw, lens="refactor-find")
    assert result.error is None
    assert "code is already tight" in result.text
    # No findings rows because the body had no table.
    assert "| F-01 |" not in result.text
    assert "finding_count: 0" in result.text


# ---------------------------------------------------------------------------
# 2 -- REGISTRY + dispatcher integration
# ---------------------------------------------------------------------------


def test_registry_resolves_findings_table_v1_to_recipe():
    entry = REGISTRY["findings_table_v1"]
    assert entry is not None
    assert isinstance(entry, Recipe)
    assert isinstance(entry, FindingsTableV1)


def test_registry_findings_table_v1_protocol_callable():
    recipe = REGISTRY["findings_table_v1"]
    assert recipe is not None
    result = recipe.normalize(
        "| Section | Gap | Issue | Fix |\n"
        "|---------|-----|-------|-----|\n"
        "| §1 | missing | empty | add intro |\n"
        "\n## Notes\nok\n",
        {
            "target": "/x.md",
            "generated": FIXED_GENERATED,
            "status": "success",
            "lens": "doc-completeness",
        },
    )
    assert isinstance(result, NormalizedResult)
    assert "T2-Findings Table (doc-completeness)" in result.text


def _make_worker(
    tmp_path: Path,
    index: int,
    *,
    status: str,
    body: str,
) -> WorkerResult:
    raw_path = tmp_path / f"worker-{index:02d}.raw.md"
    raw_path.write_text(body, encoding="utf-8")
    return WorkerResult(
        index=index,
        path=str(tmp_path / f"worker-{index:02d}.md"),
        raw_path=str(raw_path),
        meta_path=str(tmp_path / f"worker-{index:02d}.meta.json"),
        final_path=str(tmp_path / f"worker-{index:02d}.final.md"),
        model_id=f"model-{index}",
        model_label=f"Model {index}",
        bytes=len(body.encode("utf-8")),
        status=status,
        http_code=200 if status == "success" else None,
        attempts=1,
        elapsed_ms=42,
    )


def test_dispatcher_routes_success_worker_through_findings_table_v1(tmp_path):
    body = (FIXTURES_DIR / "refactor_find.raw.txt").read_text(encoding="utf-8")
    worker = _make_worker(tmp_path, 0, status="success", body=body)

    [out] = normalize_wave2(
        [worker],
        "findings_table_v1",
        recipe_args={
            "status": "success",
            "target": FIXED_TARGET,
            "target_checksum": FIXED_CHECKSUM,
            "target_truncated": False,
            "model_id": worker.model_id,
            "model_label": worker.model_label,
            "caller_label": "dispatcher-test",
            "elapsed_ms": worker.elapsed_ms,
            "generated": FIXED_GENERATED,
            "lens": "refactor-find",
            "tier": "T2-code",
            "suspect": False,
        },
    )

    assert out.status == "success"
    final_text = Path(worker.final_path).read_text(encoding="utf-8")
    assert "T2-Findings Table (refactor-find)" in final_text
    assert "| F-01 |" in final_text
    assert FIXED_CHECKSUM in final_text

    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "findings_table_v1"
    assert meta["salvaged"] is False
    assert meta["status"] == "success"


# ---------------------------------------------------------------------------
# 3 -- §7.4 salvage gate
# ---------------------------------------------------------------------------


def test_dispatcher_promotes_parse_error_via_salvage_flag(tmp_path):
    body = (FIXTURES_DIR / "salvage.raw.txt").read_text(encoding="utf-8")
    worker = _make_worker(tmp_path, 1, status="parse_error", body=body)

    [out] = normalize_wave2(
        [worker],
        "findings_table_v1",
        recipe_args={
            "status": "parse_error",
            "target": FIXED_TARGET,
            "target_checksum": FIXED_CHECKSUM,
            "target_truncated": False,
            "model_id": worker.model_id,
            "model_label": worker.model_label,
            "caller_label": "",
            "elapsed_ms": worker.elapsed_ms,
            "generated": FIXED_GENERATED,
            "lens": "refactor-find",
        },
    )

    assert out.status == "success"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "success"


def test_dispatcher_keeps_parse_error_when_body_is_unrecoverable(tmp_path):
    body = "raw stream with no pipe rows and no notes heading\n"
    worker = _make_worker(tmp_path, 2, status="parse_error", body=body)

    [out] = normalize_wave2(
        [worker],
        "findings_table_v1",
        recipe_args={
            "status": "parse_error",
            "target": FIXED_TARGET,
            "target_checksum": FIXED_CHECKSUM,
            "target_truncated": False,
            "model_id": worker.model_id,
            "model_label": worker.model_label,
            "caller_label": "",
            "elapsed_ms": worker.elapsed_ms,
            "generated": FIXED_GENERATED,
            "lens": "refactor-find",
        },
    )

    assert out.status == "parse_error"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is False
    assert meta["status"] == "parse_error"
    assert meta.get("error", "")
    assert not Path(worker.final_path).exists()


def test_salvage_flag_propagates_from_recipe_on_recoverable_parse_error():
    raw = (FIXTURES_DIR / "salvage.raw.txt").read_text(encoding="utf-8")
    result = _run(raw, status="parse_error")
    assert result.salvaged is True
    assert result.text  # non-empty
    assert "| F-01 |" in result.text


def test_salvage_flag_false_when_status_was_success():
    raw = (FIXTURES_DIR / "refactor_find.raw.txt").read_text(encoding="utf-8")
    result = _run(raw, status="success")
    assert result.salvaged is False


def test_recipe_recovers_parse_error_with_notes_only():
    raw = (FIXTURES_DIR / "notes_only.raw.txt").read_text(encoding="utf-8")
    result = _run(raw, status="parse_error")
    # Notes alone is enough to salvage.
    assert result.salvaged is True
    assert "code is already tight" in result.text


# ---------------------------------------------------------------------------
# 4 -- AC-011 boundary: order preserved, duplicates retained, no dedup
# ---------------------------------------------------------------------------


def test_ac011_preserves_all_findings_including_duplicates():
    raw = (
        "| File:line | Cleanup | Rationale | Patch sketch |\n"
        "|-----------|---------|-----------|---------------|\n"
        "| a.py:1 | duplicate cleanup | same reason | same patch |\n"
        "| a.py:1 | duplicate cleanup | same reason | same patch |\n"
        "| b.py:2 | unique cleanup | other reason | other patch |\n"
        "| a.py:1 | duplicate cleanup | same reason | same patch |\n"
        "\n## Notes\nthree duplicates by design\n"
    )
    result = _run(raw)
    # 4 row IDs present, in input order (renumbered F-01..F-04).
    assert "| F-01 |" in result.text
    assert "| F-02 |" in result.text
    assert "| F-03 |" in result.text
    assert "| F-04 |" in result.text
    # The duplicate text appears 3 times in the rendered output.
    assert result.text.count("duplicate cleanup") == 3
    assert result.text.count("unique cleanup") == 1


def test_ac011_preserves_row_order():
    raw = (
        "| File:line | Cleanup | Rationale | Patch |\n"
        "|-----------|---------|-----------|-------|\n"
        "| z.py:1 | last alphabetically | r1 | p1 |\n"
        "| a.py:1 | first alphabetically | r2 | p2 |\n"
        "| m.py:1 | middle alphabetically | r3 | p3 |\n"
        "\n## Notes\nleave order alone\n"
    )
    result = _run(raw)
    # Verify natural row order is preserved (no sort).
    pos_z = result.text.index("last alphabetically")
    pos_a = result.text.index("first alphabetically")
    pos_m = result.text.index("middle alphabetically")
    assert pos_z < pos_a < pos_m


def test_ac011_does_not_filter_low_signal_rows():
    raw = (
        "| File:line | Finding | Detail | Action |\n"
        "|-----------|---------|--------|--------|\n"
        "| x.py:1 | trivial nit | none really | skip |\n"
        "| x.py:2 | another low-signal | meh | maybe |\n"
        "\n## Notes\nkeeping every row\n"
    )
    result = _run(raw)
    assert "| F-01 |" in result.text
    assert "| F-02 |" in result.text
    assert "trivial nit" in result.text
    assert "another low-signal" in result.text


# ---------------------------------------------------------------------------
# 5 -- Helper-level coverage (parser internals)
# ---------------------------------------------------------------------------


def test_strip_frontmatter_drops_leading_yaml():
    text = "---\nfoo: 1\n---\n# Body\n"
    assert strip_frontmatter(text).lstrip().startswith("# Body")


def test_strip_frontmatter_passthrough_when_no_frontmatter():
    text = "# Body\nno yaml here\n"
    assert strip_frontmatter(text) == text


def test_parse_findings_table_skips_header_and_divider():
    text = (
        "| Loc | Find | Detail | Act |\n"
        "|-----|------|--------|-----|\n"
        "| a:1 | f | d | a |\n"
    )
    rows = parse_findings_table(text)
    assert len(rows) == 1
    assert rows[0] == {"locator": "a:1", "finding": "f", "detail": "d", "action": "a"}


def test_parse_findings_table_handles_missing_trailing_cells():
    text = (
        "| Loc | Find | Detail | Act |\n"
        "|-----|------|--------|-----|\n"
        "| a:1 | onlyFind |\n"
    )
    rows = parse_findings_table(text)
    assert len(rows) == 1
    assert rows[0]["finding"] == "onlyFind"
    assert rows[0]["detail"] == ""
    assert rows[0]["action"] == ""


def test_parse_findings_table_packs_extra_cells_into_action():
    text = (
        "| Loc | Find | Detail | A1 | A2 | A3 |\n"
        "|-----|------|--------|----|----|----|\n"
        "| x:1 | f | d | one | two | three |\n"
    )
    rows = parse_findings_table(text)
    assert len(rows) == 1
    # AC-011 preservation: extra cells join into action, not dropped.
    assert "one" in rows[0]["action"]
    assert "two" in rows[0]["action"]
    assert "three" in rows[0]["action"]


def test_parse_findings_table_multiple_blocks():
    text = (
        "| L | F | D | A |\n"
        "|---|---|---|---|\n"
        "| a:1 | f1 | d1 | a1 |\n"
        "\n"
        "Some prose between tables.\n"
        "\n"
        "| L | F | D | A |\n"
        "|---|---|---|---|\n"
        "| b:2 | f2 | d2 | a2 |\n"
    )
    rows = parse_findings_table(text)
    assert len(rows) == 2
    assert rows[0]["locator"] == "a:1"
    assert rows[1]["locator"] == "b:2"


def test_parse_findings_table_skips_data_with_no_divider_seen():
    text = "| not a real table |\n| just two rows |\n"
    rows = parse_findings_table(text)
    assert rows == []


def test_extract_notes_caps_at_default():
    body = "## Notes\n" + ("x " * 500)
    assert len(extract_notes(body)) <= FALLBACK_NOTES_CAP


def test_extract_notes_returns_empty_when_no_heading():
    assert extract_notes("# Heading\nbody without notes section\n") == ""


def test_truncation_caps_oversize_cell_content():
    """Cell-level truncation caps protect against runaway model output
    without dropping the finding itself (AC-011 preservation)."""
    big = "x" * (CLAIM_CAP * 4)
    bigger = "y" * (DETAIL_CAP * 4)
    text = (
        "| Loc | Find | Detail | Act |\n"
        "|-----|------|--------|-----|\n"
        f"| z:1 | {big} | {bigger} | {bigger} |\n"
    )
    rows = parse_findings_table(text)
    assert len(rows) == 1
    assert len(rows[0]["finding"]) <= CLAIM_CAP
    assert len(rows[0]["detail"]) <= DETAIL_CAP
    assert len(rows[0]["action"]) <= DETAIL_CAP


# ---------------------------------------------------------------------------
# 6 -- Item 2.8 characterization (C03 / panel G5): every expected value below
# was observed from the UNCHANGED findings_table_v1 implementation and is
# frozen here before any shared-primitive extraction. Serialized copies live
# in the task artifacts (A/baselines/recipes/findings/cases.json).
# ---------------------------------------------------------------------------

_E = "é"  # 2-byte UTF-8 code point for Unicode cap checks
_TABLE = "| L | F | D | A |\n|---|---|---|---|\n"
_FB = "Some prose from the model. No table, no Notes heading.\n"

_FM_DEFAULT = (
    "---\n"
    'schema_version: "1.0"\n'
    'tier: "T2-code"\n'
    "suspect: false\n"
    'lens: "refactor-find"\n'
    'reviewer_model_id: "m"\n'
    'reviewer_model_label: "M"\n'
    'target: "/tmp/example/target.py"\n'
    'target_checksum: "deadbeefcafe"\n'
    "target_truncated: false\n"
    'generated: "2026-06-01T11:19:39Z"\n'
    'caller_label: ""\n'
    "elapsed_ms: 12345\n"
)
_HEAD = (
    "---\n"
    "\n"
    "# T2-Findings Table (refactor-find) — target\n"
    "\n"
    "## Findings\n"
    "\n"
    "| ID | Locator | Finding | Detail | Action |\n"
    "|----|---------|---------|--------|--------|\n"
)
_PLACEHOLDER = "| F-00 | (no rows) | (no structured findings returned) | — | — |\n"


def _notes_section(text: str) -> str:
    return text.split("\n## Notes\n", 1)[1]


def _frontmatter(text: str) -> list[tuple[str, str]]:
    block = text.split("---\n", 2)[1]
    return [tuple(line.split(": ", 1)) for line in block.splitlines()]


def _row(loc="", fin="", det="", act=""):
    return {"locator": loc, "finding": fin, "detail": det, "action": act}


# --- extract_notes: omitted/explicit cap + definition-time default binding ---


@pytest.mark.parametrize("n,expected_len", [(299, 299), (300, 300), (301, 300)])
def test_c03_extract_notes_omitted_cap_is_300_unicode(n, expected_len):
    out = extract_notes("## Notes\n" + _E * n)
    assert out == _E * expected_len
    assert len(out.encode("utf-8")) == 2 * expected_len


@pytest.mark.parametrize(
    "text,cap,expected",
    [
        ("## Notes\n" + _E * 10, 5, _E * 5),
        ("## Notes\n" + _E * 400, 350, _E * 350),  # explicit cap overrides default
        ("## Notes\nabc", 0, ""),
        ("## Notes\nabc", -1, "ab"),
        ("## Notes\n a   b ", 3, "a b"),  # G5.28 collapse then slice
    ],
)
def test_c03_extract_notes_explicit_cap(text, cap, expected):
    assert extract_notes(text, cap) == expected


def test_c03_extract_notes_default_bound_at_definition_time():
    assert FALLBACK_NOTES_CAP == 300
    assert extract_notes.__defaults__ == (300,)


def test_c03_default300_survives_patching_module_constant(monkeypatch):
    monkeypatch.setattr(_ft, "FALLBACK_NOTES_CAP", 10)
    # Omitted cap still uses the value bound when extract_notes was defined.
    assert extract_notes.__defaults__ == (300,)
    assert len(_ft.extract_notes("## Notes\n" + _E * 400)) == 300
    assert len(extract_notes("## Notes\n" + _E * 400)) == 300


def test_c03_freeform_fallback_reads_module_constant_at_runtime(monkeypatch):
    """Contrast pin: the normalize freeform fallback (findings_table_v1.py
    `_truncate(body, FALLBACK_NOTES_CAP)`) looks the constant up at call
    time, so the same patch DOES change it."""
    monkeypatch.setattr(_ft, "FALLBACK_NOTES_CAP", 10)
    result = _run(_E * 400)
    assert _notes_section(result.text) == _E * 10 + "\n"


# --- extract_notes: section selection (G5.17-G5.22) ---


@pytest.mark.parametrize(
    "text,expected",
    [
        ("plain", ""),  # G5.17 absent
        ("## Notes\n## Other\nx", ""),  # G5.18 empty before next heading
        ("## Notes\n## Notes\nsecond", ""),  # G5.18 no later repeat selected
        ("## nOtEs\na", "a"),  # G5.19 case-insensitive
        ("## Notes\na  b\n## Other\nc", "a b"),  # G5.20 next heading
        ("## Notes\na  b\n", "a b"),  # G5.21 to EOF
        ("## Notes\nfirst\n## Notes\nsecond", "first"),  # G5.22 first only
        ("# Notes  \nx\n### NOTES\ny", "x"),
        ("##Notes\nx", "x"),
        ("## Notes\na\n#tag b\n## End\nc", "a #tag b"),  # '#tag' is not a heading
        ("## Notes about\nx", ""),
    ],
)
def test_c03_extract_notes_section_selection(text, expected):
    assert extract_notes(text) == expected


# --- parse_findings_table: widths, trailing cells, block reset, caps ---


@pytest.mark.parametrize(
    "line,expected",
    [
        ("| a |", _row("a")),
        ("| a | b |", _row("a", "b")),
        ("| a | b | c |", _row("a", "b", "c")),
        ("| a | b | c | d |", _row("a", "b", "c", "d")),
        ("| a | b | c | d | e | f |", _row("a", "b", "c", "d / e / f")),
        ("| a | b |  |   |", _row("a", "b")),  # trailing empty cells popped
        ("| a |  | c | d |", _row("a", "", "c", "d")),  # middle empty kept
        ("|  | x |", _row("", "x")),  # leading empty kept
        ("   | a | b", _row("a", "b")),  # indented, no closing pipe
        ("| a   b | c \t d |", _row("a b", "c d")),  # per-cell collapse
    ],
)
def test_c03_parse_widths_and_cells(line, expected):
    assert parse_findings_table(_TABLE + line + "\n") == [expected]


def test_c03_parse_all_empty_row_skipped_without_block_reset():
    rows = parse_findings_table(_TABLE + "|  |  |\n| a | b | c | d |\n")
    assert rows == [_row("a", "b", "c", "d")]


def test_c03_parse_header_divider_reset():
    """G5.34: header -> divider -> data -> plain -> pipe (no divider) ->
    header -> divider -> data."""
    text = (
        "| H1 | H2 |\n|---|---|\n| d1 | x |\nplain\n| after-plain | y |\n"
        "| H | H |\n| :--: | --- |\n| d2 | z |\n"
    )
    assert parse_findings_table(text) == [_row("d1", "x"), _row("d2", "z")]


def test_c03_parse_blank_line_resets_block():
    assert parse_findings_table(_TABLE + "| d1 | x |\n\n| d2 | y |\n") == [
        _row("d1", "x")
    ]


def test_c03_parse_second_divider_keeps_block_open():
    text = _TABLE + "| d1 | x |\n|---|---|\n| d2 | y |\n"
    assert parse_findings_table(text) == [_row("d1", "x"), _row("d2", "y")]


def test_c03_parse_preserves_order_and_duplicates():
    text = _TABLE + "| z | 1 |\n| a | 2 |\n| z | 1 |\n"
    assert parse_findings_table(text) == [
        _row("z", "1"),
        _row("a", "2"),
        _row("z", "1"),
    ]


@pytest.mark.parametrize("n,kept", [(199, 199), (200, 200), (201, 200)])
def test_c03_locator_finding_cap_200_unicode(n, kept):
    assert CLAIM_CAP == 200
    [row] = parse_findings_table(_TABLE + f"| {_E * n} | {_E * n} |\n")
    assert row == _row(_E * kept, _E * kept)


@pytest.mark.parametrize("n,kept", [(199, 199), (200, 200), (201, 200)])
def test_c03_detail_action_cap_200_unicode(n, kept):
    assert DETAIL_CAP == 200
    [row] = parse_findings_table(_TABLE + f"| a | b | {_E * n} | {_E * n} |\n")
    assert row == _row("a", "b", _E * kept, _E * kept)


def test_c03_action_tail_joined_before_cap():
    [row] = parse_findings_table(_TABLE + f"| a | b | c | {_E * 198} | xyz |\n")
    assert row == _row("a", "b", "c", _E * 198 + " /")


# --- normalize: branches with exact serialized output ---


def test_c03_normalize_structured_success_exact():
    raw = _TABLE + "| a:1 | f | d | x |\n| b:2 | g |  |  |\n\n## Notes\nok  notes\n"
    result = _run(raw)
    assert (result.salvaged, result.error) == (False, None)
    assert result.text == (
        _FM_DEFAULT
        + "finding_count: 2\n"
        + _HEAD
        + "| F-01 | a:1 | f | d | x |\n"
        + "| F-02 | b:2 | g |  |  |\n"
        + "\n## Notes\nok notes\n"
    )


def test_c03_normalize_freeform_success_exact():
    result = _run(_FB)
    assert (result.salvaged, result.error) == (False, None)
    assert result.text == (
        _FM_DEFAULT
        + "finding_count: 0\n"
        + _HEAD
        + _PLACEHOLDER
        + "\n## Notes\nSome prose from the model. No table, no Notes heading.\n"
    )


@pytest.mark.parametrize("n,kept", [(299, 299), (300, 300), (301, 300)])
def test_c03_normalize_freeform_fallback_cap_300_unicode(n, kept):
    result = _run(_E * n)
    assert result.text == (
        _FM_DEFAULT
        + "finding_count: 0\n"
        + _HEAD
        + _PLACEHOLDER
        + "\n## Notes\n"
        + _E * kept
        + "\n"
    )


@pytest.mark.parametrize(
    "raw,notes",
    [
        ("---\nx: 1\n---\n   ", "(no structured findings returned)"),
        ("## Notes\n\n", "## Notes"),  # empty Notes -> body collapsed as fallback
    ],
)
def test_c03_normalize_freeform_edge_bodies(raw, notes):
    result = _run(raw)
    assert (result.salvaged, result.error) == (False, None)
    assert "finding_count: 0\n" in result.text
    assert _PLACEHOLDER in result.text
    assert _notes_section(result.text) == notes + "\n"


def test_c03_normalize_non_parse_error_status_uses_success_path():
    assert _run(_FB, status="timeout").text == _run(_FB).text


@pytest.mark.parametrize(
    "raw,status,error",
    [
        ("", "success", "empty raw body"),
        (" \n\t", "success", "empty raw body"),
        ("", "parse_error", "empty raw body"),
        (_FB, "parse_error", "no findings or notes"),
    ],
)
def test_c03_normalize_error_branches(raw, status, error):
    result = _run(raw, status=status)
    assert (result.text, result.salvaged, result.error) == ("", False, error)


def test_c03_normalize_parse_error_salvage_rows_exact():
    result = _run(_TABLE + "| a | b |\n", status="parse_error")
    assert (result.salvaged, result.error) == (True, None)
    assert result.text == (
        _FM_DEFAULT
        + "finding_count: 1\n"
        + _HEAD
        + "| F-01 | a | b |  |  |\n"
        + "\n## Notes\n(no notes returned)\n"
    )


def test_c03_normalize_parse_error_salvage_notes_only_exact():
    result = _run("## Notes\nkept\n", status="parse_error")
    assert (result.salvaged, result.error) == (True, None)
    assert result.text == (
        _FM_DEFAULT + "finding_count: 0\n" + _HEAD + _PLACEHOLDER + "\n## Notes\nkept\n"
    )


# --- metadata field order / types under fixed generated values ---


def test_c03_metadata_field_order_and_types_exact():
    raw = _TABLE + "| a | b |\n"
    args: dict[str, Any] = {
        "status": "success",
        "target": "/a/b.tar.gz",
        "target_checksum": FIXED_CHECKSUM,
        "target_truncated": 1,
        "model_id": "m",
        "model_label": 'q"b\\' + _E,
        "caller_label": None,
        "elapsed_ms": "7",
        "generated": FIXED_GENERATED,
        "lens": "",
        "tier": "",
        "suspect": "yes",
    }
    result = FindingsTableV1().normalize(raw, args)
    assert _frontmatter(result.text) == [
        ("schema_version", '"1.0"'),
        ("tier", '"T2"'),
        ("suspect", "true"),
        ("lens", '"findings-table"'),
        ("reviewer_model_id", '"m"'),
        ("reviewer_model_label", '"q\\"b\\\\' + _E + '"'),
        ("target", '"/a/b.tar.gz"'),
        ("target_checksum", '"deadbeefcafe"'),
        ("target_truncated", "true"),
        ("generated", '"2026-06-01T11:19:39Z"'),
        ("caller_label", '""'),
        ("elapsed_ms", "7"),
        ("finding_count", "1"),
    ]
    assert "# T2-Findings Table (findings-table) — b.tar\n" in result.text


@pytest.mark.parametrize("elapsed", ["bad", None, 0, 0.9])
def test_c03_metadata_elapsed_fallback_zero(elapsed):
    result = _run(_TABLE + "| a | b |\n", elapsed_ms=elapsed)
    assert ("elapsed_ms", "0") in _frontmatter(result.text)


def test_c03_empty_target_gives_empty_slug():
    result = _run(_TABLE + "| a | b |\n", target="")
    assert ("target", '""') in _frontmatter(result.text)
    assert "# T2-Findings Table (refactor-find) — \n" in result.text


@pytest.mark.parametrize("generated", [None, ""])
def test_c03_generated_absent_uses_module_iso_now(monkeypatch, generated):
    monkeypatch.setattr(_ft, "iso_now", lambda: "2000-01-02T03:04:05Z")
    raw = _TABLE + "| a | b |\n"
    args: dict[str, Any] = {"status": "success", "target": FIXED_TARGET}
    if generated is not None:
        args["generated"] = generated
    result = FindingsTableV1().normalize(raw, args)
    assert ("generated", '"2000-01-02T03:04:05Z"') in _frontmatter(result.text)
