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
    assert f"lens: \"{lens}\"" in text
    assert f"tier: \"{tier}\"" in text
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
