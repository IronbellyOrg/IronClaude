"""T04.05 -- ``hypothesis_table_v1`` recipe tests (R-090 / COMP-018 / D-0072).

Covers five layers:

1. **Recipe surface**: ``HypothesisTableV1.normalize`` produces a
   canonical 5-column markdown table (``ID | Cause | Evidence |
   Confidence | Next Step``) with auto-assigned ``H-NN`` IDs, across
   the 5-column (supporting + falsifying) and 4-column lens fixtures.

2. **REGISTRY**: the ``hypothesis_table_v1`` slot resolves to a
   Recipe-conforming object (no longer the M2-era ``None`` sentinel)
   and the Wave-2 dispatcher routes a worker through it end-to-end.

3. **§7.4 salvage**: a ``parse_error`` worker with a recoverable body
   is promoted via ``salvaged=True``; a ``parse_error`` worker with
   neither hypotheses nor notes stays failed.

4. **AC-011 boundary**: row order preserved, duplicates retained,
   every parsed row reaches the output (no scoring / dedup / reorder).

5. **Helper coverage**: parser internals and confidence reformatting.
"""

from __future__ import annotations

import inspect
import json
import sys
from datetime import datetime as _real_datetime
from datetime import timezone as _real_timezone
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.normalize import normalize_wave2
from superclaude.cli.swarm.recipes import REGISTRY, NormalizedResult, Recipe
from superclaude.cli.swarm.recipes import hypothesis_table_v1 as hyp_mod
from superclaude.cli.swarm.recipes.bare_review_v1 import parse_conf as bare_parse_conf
from superclaude.cli.swarm.recipes.hypothesis_table_v1 import (
    CAUSE_CAP,
    EVIDENCE_CAP,
    FALLBACK_NOTES_CAP,
    NEXT_STEP_CAP,
    HypothesisTableV1,
    extract_notes,
    parse_confidence,
    parse_hypothesis_table,
    strip_frontmatter,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "hypothesis_table_v1"

FIXED_GENERATED = "2026-06-01T11:19:39Z"
FIXED_CHECKSUM = "deadbeefcafe"
FIXED_TARGET = "/tmp/example/auth_login_500.log"


def _run(
    raw: str,
    *,
    status: str = "success",
    lens: str = "troubleshoot-hypothesis",
    tier: str = "T2-tshoot",
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
    return HypothesisTableV1().normalize(raw, args)


# ---------------------------------------------------------------------------
# 1 -- Recipe surface
# ---------------------------------------------------------------------------


def test_recipe_renders_canonical_table_with_supporting_and_falsifying():
    raw = (FIXTURES_DIR / "troubleshoot_hypothesis.raw.txt").read_text(encoding="utf-8")
    result = _run(raw)
    assert result.error is None
    assert result.salvaged is False
    text = result.text

    # Canonical header present.
    assert "| ID | Cause | Evidence | Confidence | Next Step |" in text
    assert "|----|-------|----------|------------|-----------|" in text

    # Three hypotheses with auto-assigned H-NN ids.
    for i in range(1, 4):
        assert f"| H-{i:02d} |" in text
    assert "| H-04 |" not in text

    # Frontmatter records lens + tier + hypothesis_count.
    assert 'lens: "troubleshoot-hypothesis"' in text
    assert 'tier: "T2-tshoot"' in text
    assert "hypothesis_count: 3" in text

    # 5-column input collapses supporting + falsifying into Evidence cell.
    assert "Supporting evidence" not in text  # header text not propagated
    assert "75 |" in text  # numeric confidence preserved
    assert "## Notes" in text


def test_recipe_renders_canonical_table_with_minimal_four_columns():
    raw = (FIXTURES_DIR / "minimal_four_col.raw.txt").read_text(encoding="utf-8")
    result = _run(raw, target="/tmp/example/disk_full.log")
    assert result.error is None
    assert result.salvaged is False
    text = result.text

    assert "| ID | Cause | Evidence | Confidence | Next Step |" in text
    assert "| H-01 |" in text
    assert "| H-02 |" in text
    assert "| H-03 |" not in text
    assert "hypothesis_count: 2" in text


def test_recipe_records_target_metadata_in_frontmatter():
    raw = (FIXTURES_DIR / "troubleshoot_hypothesis.raw.txt").read_text(encoding="utf-8")
    result = _run(raw)
    assert FIXED_GENERATED in result.text
    assert FIXED_CHECKSUM in result.text
    assert FIXED_TARGET in result.text
    # Slug appears in heading.
    assert (
        "T2-Hypothesis Table (troubleshoot-hypothesis) — auth_login_500" in result.text
    )


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


def test_recipe_freeform_fallback_on_success_with_no_hypotheses_or_notes():
    raw = "Some prose from the model. No table, no Notes heading.\n"
    result = _run(raw, status="success")
    assert result.error is None
    assert result.salvaged is False
    assert "Some prose from the model" in result.text
    # Placeholder row keeps the markdown table well-formed.
    assert "| H-00 |" in result.text


def test_recipe_uses_notes_only_fixture_via_fallback_path():
    raw = (FIXTURES_DIR / "notes_only.raw.txt").read_text(encoding="utf-8")
    result = _run(raw)
    assert result.error is None
    assert "No reproducible failure pattern surfaced" in result.text
    # No hypothesis rows because the body had no table.
    assert "| H-01 |" not in result.text
    assert "hypothesis_count: 0" in result.text


# ---------------------------------------------------------------------------
# 2 -- REGISTRY + dispatcher integration
# ---------------------------------------------------------------------------


def test_registry_resolves_hypothesis_table_v1_to_recipe():
    entry = REGISTRY["hypothesis_table_v1"]
    assert entry is not None
    assert isinstance(entry, Recipe)
    assert isinstance(entry, HypothesisTableV1)


def test_registry_hypothesis_table_v1_protocol_callable():
    recipe = REGISTRY["hypothesis_table_v1"]
    assert recipe is not None
    result = recipe.normalize(
        "| Cause | Evidence | Confidence | Next step |\n"
        "|-------|----------|------------|-----------|\n"
        "| stale cache | cache_age > ttl | 80 | flush and retry |\n"
        "\n## Notes\nok\n",
        {
            "target": "/x.log",
            "generated": FIXED_GENERATED,
            "status": "success",
            "lens": "troubleshoot-hypothesis",
        },
    )
    assert isinstance(result, NormalizedResult)
    assert "T2-Hypothesis Table (troubleshoot-hypothesis)" in result.text
    assert "| H-01 |" in result.text


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


def test_dispatcher_routes_success_worker_through_hypothesis_table_v1(tmp_path):
    body = (FIXTURES_DIR / "troubleshoot_hypothesis.raw.txt").read_text(
        encoding="utf-8"
    )
    worker = _make_worker(tmp_path, 0, status="success", body=body)

    [out] = normalize_wave2(
        [worker],
        "hypothesis_table_v1",
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
            "lens": "troubleshoot-hypothesis",
            "tier": "T2-tshoot",
            "suspect": False,
        },
    )

    assert out.status == "success"
    final_text = Path(worker.final_path).read_text(encoding="utf-8")
    assert "T2-Hypothesis Table (troubleshoot-hypothesis)" in final_text
    assert "| H-01 |" in final_text
    assert FIXED_CHECKSUM in final_text

    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "hypothesis_table_v1"
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
        "hypothesis_table_v1",
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
            "lens": "troubleshoot-hypothesis",
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
        "hypothesis_table_v1",
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
            "lens": "troubleshoot-hypothesis",
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
    assert "| H-01 |" in result.text


def test_salvage_flag_false_when_status_was_success():
    raw = (FIXTURES_DIR / "troubleshoot_hypothesis.raw.txt").read_text(encoding="utf-8")
    result = _run(raw, status="success")
    assert result.salvaged is False


def test_recipe_recovers_parse_error_with_notes_only():
    raw = (FIXTURES_DIR / "notes_only.raw.txt").read_text(encoding="utf-8")
    result = _run(raw, status="parse_error")
    # Notes alone is enough to salvage.
    assert result.salvaged is True
    assert "No reproducible failure pattern surfaced" in result.text


# ---------------------------------------------------------------------------
# 4 -- AC-011 boundary: order preserved, duplicates retained, no dedup
# ---------------------------------------------------------------------------


def test_ac011_preserves_all_hypotheses_including_duplicates():
    raw = (
        "| Cause | Evidence | Confidence | Next step |\n"
        "|-------|----------|------------|-----------|\n"
        "| stale cache | cache_age > ttl | 80 | flush |\n"
        "| stale cache | cache_age > ttl | 80 | flush |\n"
        "| pool exhausted | pool_full counter | 60 | bump |\n"
        "| stale cache | cache_age > ttl | 80 | flush |\n"
        "\n## Notes\nthree duplicates by design\n"
    )
    result = _run(raw)
    # 4 row IDs present, in input order.
    assert "| H-01 |" in result.text
    assert "| H-02 |" in result.text
    assert "| H-03 |" in result.text
    assert "| H-04 |" in result.text
    # The duplicate text appears 3 times in the rendered output.
    assert result.text.count("stale cache") == 3
    assert result.text.count("pool exhausted") == 1


def test_ac011_preserves_row_order_no_resort_by_confidence():
    """Likelihood ranking is the model's job; the recipe must not
    re-sort by confidence (that would cross the AC-011 boundary)."""
    raw = (
        "| Cause | Evidence | Confidence | Next |\n"
        "|-------|----------|------------|------|\n"
        "| low-conf first | e1 | 20 | n1 |\n"
        "| high-conf middle | e2 | 95 | n2 |\n"
        "| mid-conf last | e3 | 50 | n3 |\n"
        "\n## Notes\nleave order alone\n"
    )
    result = _run(raw)
    pos_low = result.text.index("low-conf first")
    pos_high = result.text.index("high-conf middle")
    pos_mid = result.text.index("mid-conf last")
    assert pos_low < pos_high < pos_mid


def test_ac011_does_not_filter_low_confidence_rows():
    raw = (
        "| Cause | Evidence | Confidence | Next |\n"
        "|-------|----------|------------|------|\n"
        "| barely plausible | thin evidence | 5 | maybe probe |\n"
        "| also weak | weak signal | 10 | maybe probe |\n"
        "\n## Notes\nkeeping every row\n"
    )
    result = _run(raw)
    assert "| H-01 |" in result.text
    assert "| H-02 |" in result.text
    assert "barely plausible" in result.text
    assert "also weak" in result.text


# ---------------------------------------------------------------------------
# 5 -- Helper-level coverage (parser + confidence internals)
# ---------------------------------------------------------------------------


def test_strip_frontmatter_drops_leading_yaml():
    text = "---\nfoo: 1\n---\n# Body\n"
    assert strip_frontmatter(text).lstrip().startswith("# Body")


def test_strip_frontmatter_passthrough_when_no_frontmatter():
    text = "# Body\nno yaml here\n"
    assert strip_frontmatter(text) == text


def test_parse_hypothesis_table_skips_header_and_divider():
    text = (
        "| Cause | Evidence | Conf | Next |\n"
        "|-------|----------|------|------|\n"
        "| c | e | 50 | n |\n"
    )
    rows = parse_hypothesis_table(text)
    assert len(rows) == 1
    assert rows[0] == {
        "cause": "c",
        "evidence": "e",
        "confidence": "50",
        "next_step": "n",
    }


def test_parse_hypothesis_table_handles_three_columns():
    """3-col input: cause | evidence | next_step (no confidence)."""
    text = "| Cause | Evidence | Next |\n|-------|----------|------|\n| c | e | n |\n"
    rows = parse_hypothesis_table(text)
    assert len(rows) == 1
    assert rows[0]["cause"] == "c"
    assert rows[0]["evidence"] == "e"
    assert rows[0]["confidence"] == ""
    assert rows[0]["next_step"] == "n"


def test_parse_hypothesis_table_joins_supporting_and_falsifying():
    """5-col input (supporting + falsifying evidence) folds into Evidence."""
    text = (
        "| Cause | Supporting | Falsifying | Conf | Next |\n"
        "|-------|------------|------------|------|------|\n"
        "| c | sup | fal | 70 | n |\n"
    )
    rows = parse_hypothesis_table(text)
    assert len(rows) == 1
    assert rows[0]["cause"] == "c"
    assert "sup" in rows[0]["evidence"]
    assert "fal" in rows[0]["evidence"]
    assert rows[0]["confidence"] == "70"
    assert rows[0]["next_step"] == "n"


def test_parse_hypothesis_table_packs_extra_cells_into_evidence():
    """6+ columns: middle cells join into evidence, tail anchors hold."""
    text = (
        "| Cause | E1 | E2 | E3 | Conf | Next |\n"
        "|-------|----|----|----|------|------|\n"
        "| c | one | two | three | 40 | n |\n"
    )
    rows = parse_hypothesis_table(text)
    assert len(rows) == 1
    assert "one" in rows[0]["evidence"]
    assert "two" in rows[0]["evidence"]
    assert "three" in rows[0]["evidence"]
    assert rows[0]["confidence"] == "40"
    assert rows[0]["next_step"] == "n"


def test_parse_hypothesis_table_multiple_blocks():
    text = (
        "| C | E | Cf | N |\n"
        "|---|---|----|---|\n"
        "| c1 | e1 | 50 | n1 |\n"
        "\n"
        "Some prose between tables.\n"
        "\n"
        "| C | E | Cf | N |\n"
        "|---|---|----|---|\n"
        "| c2 | e2 | 75 | n2 |\n"
    )
    rows = parse_hypothesis_table(text)
    assert len(rows) == 2
    assert rows[0]["cause"] == "c1"
    assert rows[1]["cause"] == "c2"


def test_parse_hypothesis_table_skips_data_with_no_divider_seen():
    text = "| not a real table |\n| just two rows |\n"
    rows = parse_hypothesis_table(text)
    assert rows == []


def test_parse_confidence_extracts_first_digit_run():
    assert parse_confidence("85%") == "85"
    assert parse_confidence("score: 73") == "73"
    assert parse_confidence("") == ""
    assert parse_confidence("   ") == ""


def test_parse_confidence_clamps_to_zero_to_hundred():
    assert parse_confidence("9000") == "100"
    assert parse_confidence("-5") == "5"  # regex extracts digits only


def test_parse_confidence_passes_qualitative_label_through():
    """No digit run -> keep the label (recipe does not classify it)."""
    assert parse_confidence("high") == "high"
    assert parse_confidence("  Medium  ") == "Medium"


def test_extract_notes_caps_at_default():
    body = "## Notes\n" + ("x " * 500)
    assert len(extract_notes(body)) <= FALLBACK_NOTES_CAP


def test_extract_notes_returns_empty_when_no_heading():
    assert extract_notes("# Heading\nbody without notes section\n") == ""


def test_truncation_caps_oversize_cell_content():
    """Cell-level truncation caps protect against runaway model output
    without dropping the hypothesis itself (AC-011 preservation)."""
    big_cause = "c" * (CAUSE_CAP * 4)
    big_evidence = "e" * (EVIDENCE_CAP * 4)
    big_next = "n" * (NEXT_STEP_CAP * 4)
    text = (
        "| Cause | Evidence | Conf | Next |\n"
        "|-------|----------|------|------|\n"
        f"| {big_cause} | {big_evidence} | 50 | {big_next} |\n"
    )
    rows = parse_hypothesis_table(text)
    assert len(rows) == 1
    assert len(rows[0]["cause"]) <= CAUSE_CAP
    assert len(rows[0]["evidence"]) <= EVIDENCE_CAP
    assert len(rows[0]["next_step"]) <= NEXT_STEP_CAP


@pytest.mark.parametrize(
    "fixture_name",
    ["troubleshoot_hypothesis.raw.txt", "minimal_four_col.raw.txt"],
)
def test_recipe_emits_well_formed_yaml_frontmatter(fixture_name):
    raw = (FIXTURES_DIR / fixture_name).read_text(encoding="utf-8")
    result = _run(raw)
    text = result.text
    # Frontmatter delimiters around the head of the document.
    assert text.startswith("---\n")
    second_delim = text.index("---\n", 4)
    assert second_delim > 0
    # Required keys present.
    head = text[:second_delim]
    for key in [
        "schema_version:",
        "tier:",
        "suspect:",
        "lens:",
        "reviewer_model_id:",
        "reviewer_model_label:",
        "target:",
        "target_checksum:",
        "target_truncated:",
        "generated:",
        "caller_label:",
        "elapsed_ms:",
        "hypothesis_count:",
    ]:
        assert key in head, f"missing frontmatter key {key!r}"


# ---------------------------------------------------------------------------
# 6 -- Phase 2 characterization (cleanup-debt item 2.9 / C03 / panel G5)
#
# Expected values below were OBSERVED from the unchanged implementation
# and pinned; they are the before-extraction oracle for C03. Module-level
# case tables are also consumed by the baseline capture script under the
# task's artifacts/baselines/recipes/hypothesis/ directory.
# ---------------------------------------------------------------------------


E = "é"  # 'é': one code point, two UTF-8 bytes

EXPECTED_ALL = [
    "HypothesisTableV1",
    "DIVIDER_CELL_RE",
    "CAUSE_CAP",
    "EVIDENCE_CAP",
    "NEXT_STEP_CAP",
    "FALLBACK_NOTES_CAP",
    "iso_now",
    "yaml_str",
    "strip_frontmatter",
    "parse_confidence",
    "parse_hypothesis_table",
    "extract_notes",
    "render_markdown",
]

# (cell, hypothesis parse_confidence, bare parse_conf)
CONFIDENCE_CASES: list[tuple[str, str, str]] = [
    ("", "", ""),  # G5.2
    ("  ", "", ""),  # G5.2
    ("\t", "", ""),
    ("0", "0", "0"),  # G5.3
    ("confidence 73%", "73", "73"),  # G5.4
    ("100", "100", "100"),  # G5.5
    ("101", "100", "100"),  # G5.6
    ("9000", "100", "100"),
    ("-1", "1", "1"),  # G5.7 signed-looking -> first digit run
    ("-5", "5", "5"),
    ("+7", "7", "7"),
    ("x-0042y", "42", "42"),
    ("007", "7", "7"),
    ("12.5 then 99", "12", "12"),  # G5.8
    (" high  confidence ", "high confidence", ""),  # G5.9 split
    ("Medium\n\tHigh", "Medium High", ""),
    ("٣", "3", "3"),  # Unicode decimal digit matches \d
]

# (data-row cells, expected parsed row) -- G5.37..G5.42 and qualitative tails
WIDTH_CASES: list[tuple[list[str], dict[str, str]]] = [
    (["a"], {"cause": "a", "evidence": "", "confidence": "", "next_step": ""}),
    (["a", "b"], {"cause": "a", "evidence": "", "confidence": "", "next_step": "b"}),
    (
        ["a", "b", "c"],
        {"cause": "a", "evidence": "b", "confidence": "", "next_step": "c"},
    ),
    (
        ["a", "b", "73", "c"],
        {"cause": "a", "evidence": "b", "confidence": "73", "next_step": "c"},
    ),
    (
        ["a", "b", "c", "73", "d"],
        {"cause": "a", "evidence": "b | c", "confidence": "73", "next_step": "d"},
    ),
    (
        ["a", "b", "c", "d", "73", "e"],
        {"cause": "a", "evidence": "b | c | d", "confidence": "73", "next_step": "e"},
    ),
    (
        ["a", "b", "c", "d", "e", "f", "g"],
        {
            "cause": "a",
            "evidence": "b | c | d | e",
            "confidence": "f",
            "next_step": "g",
        },
    ),
    (
        ["a", "b", " high  confidence ", "c"],
        {
            "cause": "a",
            "evidence": "b",
            "confidence": "high confidence",
            "next_step": "c",
        },
    ),
    (
        ["a", "b", "c", "low", "d"],
        {"cause": "a", "evidence": "b | c", "confidence": "low", "next_step": "d"},
    ),
    (
        ["a  b", "c   d", "-1", "  e  f "],
        {"cause": "a b", "evidence": "c d", "confidence": "1", "next_step": "e f"},
    ),
]

# (table text, expected cause list) -- divider / reset / trailing-cell (G5.34/35)
TABLE_BLOCK_CASES: list[tuple[str, str, list[str]]] = [
    (
        "reset_on_plain_and_blank",
        "| h |\n|---|\n| a |\nplain\n| b |\n|---|\n| c |\n\n| d |\n",
        ["a", "c"],
    ),
    ("divider_with_empty_inner_cell_is_not_divider", "|C|\n|---||---|\n| a |\n", []),
    ("alignment_divider", "|C|\n| :-: | --- |\n| a |\n", ["a"]),
    ("divider_without_header", "|---|\n| a |\n", ["a"]),
    ("header_only_no_divider", "| not a real table |\n| just two rows |\n", []),
    ("all_empty_pipe_row_skipped_no_reset", "|C|\n|---|\n| | | |\n| x |\n", ["x"]),
    ("leading_empty_cell_kept", "|C|\n|---|\n|  | a |\n", [""]),
    ("doubled_leading_pipe_collapses", "|C|\n|---|\n|| a |\n", ["a"]),
    ("indented_rows_accepted", "  | h |\n  |---|\n  | a |", ["a"]),
    (
        "mid_block_divider_rearms_not_a_row",
        "|C|\n|---|\n| a |\n| --- |\n| b |\n",
        ["a", "b"],
    ),
    ("no_pipes", "just prose\n", []),
]

# (raw, status, expected salvaged, expected error, expected Notes body or None)
NORMALIZE_CASES: list[tuple[str, str, str, bool, str | None, str | None]] = [
    ("empty_success", "", "success", False, "empty raw body", None),  # G5.1
    ("whitespace_parse_error", " \n ", "parse_error", False, "empty raw body", None),
    (
        "pe_frontmatter_only",
        "---\nx\n---\n",
        "parse_error",
        False,
        "no hypotheses or notes",
        None,
    ),  # G5.49
    (
        "pe_empty_notes_heading",
        "## Notes\n\n",
        "parse_error",
        False,
        "no hypotheses or notes",
        None,
    ),
    (
        "pe_unstructured",
        "raw stream, no pipes\n",
        "parse_error",
        False,
        "no hypotheses or notes",
        None,
    ),
    (
        "pe_rows_only",
        "|C|\n|---|\n| a |\n",
        "parse_error",
        True,
        None,
        "(no notes returned)",
    ),  # G5.50
    ("pe_notes_only", "## Notes\nn\n", "parse_error", True, None, "n"),
    (
        "ok_freeform",
        "free  form\ntext",
        "success",
        False,
        None,
        "free form text",
    ),  # G5.51
    (
        "ok_frontmatter_then_blank",
        "---\nx: 1\n---\n   \n",
        "success",
        False,
        None,
        "(no structured hypotheses returned)",
    ),
    (
        "ok_empty_notes_heading_falls_back_to_body",
        "## Notes\n\n## Other\nprose\n",
        "success",
        False,
        None,
        "## Notes ## Other prose",
    ),
    (
        "unknown_status_uses_success_branch",
        "free text",
        "timeout",
        False,
        None,
        "free text",
    ),
    (
        "ok_structured",
        "|C|\n|---|\n| a | b | 73 | c |\n## Notes\nn",
        "success",
        False,
        None,
        "n",
    ),  # G5.52
]

FROZEN_STRUCTURED_RAW = (
    "---\nfoo: 1\n---\n"
    "## Hypotheses\n"
    "| Cause | Supporting | Falsifying | Conf | Next |\n"
    "|-------|------------|------------|------|------|\n"
    "| stale cache | ttl > age | none | 80% | flush |\n"
    "| pool | full | | high | bump |\n"
    "\n## Notes\nkeep  both\n"
)

FROZEN_STRUCTURED_EXPECTED = (
    "---\n"
    'schema_version: "1.0"\n'
    'tier: "T2-tshoot"\n'
    "suspect: false\n"
    'lens: "troubleshoot-hypothesis"\n'
    'reviewer_model_id: "m"\n'
    'reviewer_model_label: "M"\n'
    'target: "/tmp/example/auth_login_500.log"\n'
    'target_checksum: "deadbeefcafe"\n'
    "target_truncated: false\n"
    'generated: "2026-06-01T11:19:39Z"\n'
    'caller_label: ""\n'
    "elapsed_ms: 12345\n"
    "hypothesis_count: 2\n"
    "---\n"
    "\n"
    "# T2-Hypothesis Table (troubleshoot-hypothesis) — auth_login_500\n"
    "\n"
    "## Hypotheses\n"
    "\n"
    "| ID | Cause | Evidence | Confidence | Next Step |\n"
    "|----|-------|----------|------------|-----------|\n"
    "| H-01 | stale cache | ttl > age | none | 80 | flush |\n"
    "| H-02 | pool | full | | high | bump |\n"
    "\n"
    "## Notes\n"
    "keep both\n"
)

FROZEN_PLACEHOLDER_EXPECTED_TAIL = (
    "| ID | Cause | Evidence | Confidence | Next Step |\n"
    "|----|-------|----------|------------|-----------|\n"
    "| H-00 | (no rows) | (no structured hypotheses returned) | — | — |\n"
    "\n"
    "## Notes\n"
    "free form text\n"
)

FM_KEY_ORDER = [
    "schema_version",
    "tier",
    "suspect",
    "lens",
    "reviewer_model_id",
    "reviewer_model_label",
    "target",
    "target_checksum",
    "target_truncated",
    "generated",
    "caller_label",
    "elapsed_ms",
    "hypothesis_count",
]


def _notes_body(text: str) -> str:
    return text.split("\n## Notes\n", 1)[1].removesuffix("\n")


def _fm_lines(text: str) -> list[str]:
    return text.split("---\n", 2)[1].splitlines()


def _row(cells: list[str]) -> str:
    return "| C |\n|---|\n| " + " | ".join(cells) + " |\n"


# -- surface / constants -----------------------------------------------------


def test_c03_hyp_all_exports_pinned():
    assert hyp_mod.__all__ == EXPECTED_ALL
    for name in EXPECTED_ALL:
        assert hasattr(hyp_mod, name), name


def test_c03_hyp_cap_constants_and_divider_regex_pinned():
    assert (CAUSE_CAP, EVIDENCE_CAP, NEXT_STEP_CAP, FALLBACK_NOTES_CAP) == (
        240,
        320,
        240,
        300,
    )
    assert hyp_mod.DIVIDER_CELL_RE.pattern == r"^[\-:\s]+$"


# -- confidence (G5.2-G5.10) -------------------------------------------------


@pytest.mark.parametrize(("cell", "expected", "_bare"), CONFIDENCE_CASES)
def test_c03_hyp_parse_confidence_cases(cell, expected, _bare):
    assert parse_confidence(cell) == expected


@pytest.mark.parametrize(("cell", "_hyp", "bare_expected"), CONFIDENCE_CASES)
def test_c03_hyp_bare_no_digit_distinction_survives(cell, _hyp, bare_expected):
    """Bare ``parse_conf`` stays distinct: no digit -> '' (G5.9)."""
    assert bare_parse_conf(cell) == bare_expected


def test_c03_hyp_parse_confidence_int_conversion_error_propagates():
    """G5.10: over-limit digit run raises the baseline ValueError, no fallback."""
    huge = "9" * (sys.get_int_max_str_digits() + 1)
    with pytest.raises(ValueError):
        parse_confidence(huge)
    with pytest.raises(ValueError):
        parse_hypothesis_table(_row(["a", "b", huge, "c"]))


# -- Notes adapter: default binding + section semantics ----------------------


def test_c03_hyp_extract_notes_default_bound_at_definition_time(monkeypatch):
    assert inspect.signature(extract_notes).parameters["cap"].default == 300
    monkeypatch.setattr(hyp_mod, "FALLBACK_NOTES_CAP", 5)
    body = "## Notes\n" + E * 400
    assert extract_notes(body) == E * 300  # omitted cap ignores the patch
    assert hyp_mod.extract_notes(body) == E * 300
    assert extract_notes(body, 5) == E * 5


def test_c03_hyp_fallback_notes_cap_is_runtime_lookup(monkeypatch):
    """The freeform fallback reads FALLBACK_NOTES_CAP at call time."""
    monkeypatch.setattr(hyp_mod, "FALLBACK_NOTES_CAP", 5)
    assert _notes_body(_run("abcdefgh").text) == "abcde"


@pytest.mark.parametrize(
    ("text", "cap", "expected"),
    [
        ("plain", None, ""),  # G5.17
        ("## Notes\n## Other\nx", None, ""),  # G5.18
        ("## nOtEs\na", None, "a"),  # G5.19
        ("## Notes\na  b\n## Other\nc", None, "a b"),  # G5.20
        ("## Notes\na  b\n", None, "a b"),  # G5.21
        ("## Notes\nfirst\n## Notes\nsecond", None, "first"),  # G5.22
        ("## Notes\na", 0, ""),  # G5.23
        ("## Notes\nabc", -1, "ab"),  # G5.24
        ("## Notes\n a   b \n", 3, "a b"),  # G5.28
        ("#Notes\nx", None, "x"),
        ("### Notes  \nx\n#tag-not-heading\ny", None, "x #tag-not-heading y"),
        ("## Notes:\nx", None, ""),
    ],
)
def test_c03_hyp_extract_notes_section_cases(text, cap, expected):
    got = extract_notes(text) if cap is None else extract_notes(text, cap)
    assert got == expected


# -- caps k-1 / k / k+1, code-point based (G5.25-G5.27) ----------------------


def _cap_field(field: str, value: str) -> str:
    if field == "cause":
        return parse_hypothesis_table(_row([value, "e", "50", "n"]))[0]["cause"]
    if field == "evidence":
        return parse_hypothesis_table(_row(["c", value, "50", "n"]))[0]["evidence"]
    if field == "next_step":
        return parse_hypothesis_table(_row(["c", "e", "50", value]))[0]["next_step"]
    if field == "next_step_width2":
        return parse_hypothesis_table(_row(["c", value]))[0]["next_step"]
    if field == "notes_default":
        return extract_notes("## Notes\n" + value)
    if field == "fallback_notes":
        return _notes_body(_run(value).text)
    raise AssertionError(field)


CAP_FIELDS = [
    ("cause", 240),
    ("evidence", 320),
    ("next_step", 240),
    ("next_step_width2", 240),
    ("notes_default", 300),
    ("fallback_notes", 300),
]


@pytest.mark.parametrize(("field", "k"), CAP_FIELDS)
@pytest.mark.parametrize("delta", [-1, 0, 1])
def test_c03_hyp_caps_code_point_boundaries(field, k, delta):
    value = E * (k + delta)
    got = _cap_field(field, value)
    assert got == E * min(k, k + delta)
    assert len(got) == min(k, k + delta)
    assert len(got.encode("utf-8")) == 2 * min(k, k + delta)


def test_c03_hyp_evidence_cap_applies_after_middle_join():
    left, right = "x" * 200, "y" * 200
    rows = parse_hypothesis_table(_row(["c", left, right, "50", "n"]))
    assert rows[0]["evidence"] == (left + " | " + right)[:320]


def test_c03_hyp_cell_caps_are_runtime_lookup_collapse_then_slice(monkeypatch):
    monkeypatch.setattr(hyp_mod, "CAUSE_CAP", 3)
    monkeypatch.setattr(hyp_mod, "EVIDENCE_CAP", 3)
    monkeypatch.setattr(hyp_mod, "NEXT_STEP_CAP", 3)
    rows = parse_hypothesis_table(_row(["a   b   c", "d   e   f", "1", "g   h   i"]))
    assert rows == [
        {"cause": "a b", "evidence": "d e", "confidence": "1", "next_step": "g h"}
    ]


# -- widths and table blocks (G5.34, G5.35, G5.37-G5.42) ---------------------


@pytest.mark.parametrize(("cells", "expected"), WIDTH_CASES)
def test_c03_hyp_row_width_mapping(cells, expected):
    assert parse_hypothesis_table(_row(cells)) == [expected]


@pytest.mark.parametrize("trailing", ["", " |", "   |  |", "   "])
def test_c03_hyp_trailing_empty_cells_dropped(trailing):
    """Trailing empty cells never widen the row (stays width 2)."""
    rows = parse_hypothesis_table("| C |\n|---|\n| a | b |" + trailing + "\n")
    assert rows == [{"cause": "a", "evidence": "", "confidence": "", "next_step": "b"}]


@pytest.mark.parametrize(
    ("text", "causes"),
    [(t, c) for (_n, t, c) in TABLE_BLOCK_CASES],
    ids=[n for (n, _t, _c) in TABLE_BLOCK_CASES],
)
def test_c03_hyp_table_block_divider_reset(text, causes):
    assert [r["cause"] for r in parse_hypothesis_table(text)] == causes


# -- normalize: empty / parse-error recovery / freeform (G5.1, G5.49-G5.52) --


@pytest.mark.parametrize(
    ("raw", "status", "salvaged", "error", "notes"),
    [c[1:] for c in NORMALIZE_CASES],
    ids=[c[0] for c in NORMALIZE_CASES],
)
def test_c03_hyp_normalize_recovery_matrix(raw, status, salvaged, error, notes):
    result = _run(raw, status=status)
    assert result.salvaged is salvaged
    assert result.error == error
    if error is not None:
        assert result.text == ""
    else:
        assert _notes_body(result.text) == notes


# -- frozen-clock serialization (G5.30, G5.31, G5.53, G5.54) -----------------


def test_c03_hyp_frozen_structured_render_bytes():
    result = _run(FROZEN_STRUCTURED_RAW)
    assert result.salvaged is False and result.error is None
    assert result.text == FROZEN_STRUCTURED_EXPECTED


def test_c03_hyp_frozen_placeholder_render():
    text = _run("free  form\ntext").text
    assert text.endswith(FROZEN_PLACEHOLDER_EXPECTED_TAIL)
    assert "hypothesis_count: 0\n" in text


def test_c03_hyp_frontmatter_key_order_and_types():
    result = HypothesisTableV1().normalize(
        "|C|\n|---|\n| a |\n",
        {
            "generated": FIXED_GENERATED,
            "suspect": True,
            "target_truncated": 1,
            "caller_label": E,
            "model_id": 'a"b\\c',
            "elapsed_ms": 0,
            "tier": "",
            "lens": "",
        },
    )
    lines = _fm_lines(result.text)
    assert [ln.split(":", 1)[0] for ln in lines] == FM_KEY_ORDER
    assert lines == [
        'schema_version: "1.0"',
        'tier: "T2-tshoot"',
        "suspect: true",
        'lens: "troubleshoot-hypothesis"',
        'reviewer_model_id: "a\\"b\\\\c"',
        'reviewer_model_label: ""',
        'target: ""',
        'target_checksum: ""',
        "target_truncated: true",
        'generated: "2026-06-01T11:19:39Z"',
        f'caller_label: "{E}"',
        "elapsed_ms: 0",
        "hypothesis_count: 1",
    ]
    # Empty target -> empty slug; heading keeps the trailing separator.
    assert "\n# T2-Hypothesis Table (troubleshoot-hypothesis) — \n" in result.text


def test_c03_hyp_custom_lens_and_tier_flow_to_render():
    text = _run("|C|\n|---|\n| a |\n", lens="custom-lens", tier="T9").text
    assert 'lens: "custom-lens"' in text
    assert 'tier: "T9"' in text
    assert "# T2-Hypothesis Table (custom-lens) — auth_login_500\n" in text


@pytest.mark.parametrize(
    ("elapsed", "expected"),
    [(0, 0), (None, 0), ("bad", 0), ("", 0), ("7", 7), (3.9, 3), ([], 0)],
)
def test_c03_hyp_elapsed_ms_conversion(elapsed, expected):
    text = (
        HypothesisTableV1()
        .normalize("x", {"generated": FIXED_GENERATED, "elapsed_ms": elapsed})
        .text
    )
    assert f"\nelapsed_ms: {expected}\n" in text


@pytest.mark.parametrize("generated", [None, "", 0])
def test_c03_hyp_generated_falsy_uses_module_iso_now(monkeypatch, generated):
    monkeypatch.setattr(hyp_mod, "iso_now", lambda: "1999-12-31T23:59:59Z")
    args: dict[str, Any] = {"target": FIXED_TARGET}
    if generated is not None:
        args["generated"] = generated
    text = HypothesisTableV1().normalize("x", args).text
    assert '\ngenerated: "1999-12-31T23:59:59Z"\n' in text


def test_c03_hyp_generated_supplied_never_reads_clock(monkeypatch):
    def _boom() -> str:
        raise AssertionError("clock read despite supplied generated")

    monkeypatch.setattr(hyp_mod, "iso_now", _boom)
    assert f'generated: "{FIXED_GENERATED}"' in _run("x").text


def test_c03_hyp_iso_now_reads_module_datetime_seam(monkeypatch):
    seen: list[Any] = []

    class _FrozenDatetime:
        @staticmethod
        def now(tz=None):
            seen.append(tz)
            return _real_datetime(2026, 1, 2, 3, 4, 5, tzinfo=_real_timezone.utc)

    monkeypatch.setattr(hyp_mod, "datetime", _FrozenDatetime)
    assert hyp_mod.iso_now() == "2026-01-02T03:04:05Z"
    assert seen == [hyp_mod.timezone.utc]
    text = HypothesisTableV1().normalize("x", {}).text
    assert '\ngenerated: "2026-01-02T03:04:05Z"\n' in text


# -- exported lookup seams stay effective (G5.55) ----------------------------


def test_c03_hyp_module_global_seams_are_effective(monkeypatch):
    monkeypatch.setattr(hyp_mod, "parse_confidence", lambda c: "PC")
    assert parse_hypothesis_table(_row(["a", "b", "73", "c"]))[0]["confidence"] == "PC"
    monkeypatch.setattr(hyp_mod, "yaml_str", lambda v: "<Y>")
    assert "\ntier: <Y>\n" in _run("x").text
    monkeypatch.setattr(hyp_mod, "extract_notes", lambda t, cap=0: "PATCHED")
    assert _notes_body(_run("|C|\n|---|\n| a |\n").text) == "PATCHED"
    monkeypatch.setattr(hyp_mod, "strip_frontmatter", lambda t: "## Notes\nSF")
    assert _notes_body(_run("anything").text) == "PATCHED"
    monkeypatch.undo()
    monkeypatch.setattr(hyp_mod, "strip_frontmatter", lambda t: "## Notes\nSF")
    assert _notes_body(_run("anything").text) == "SF"
