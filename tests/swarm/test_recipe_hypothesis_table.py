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

import json
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.normalize import normalize_wave2
from superclaude.cli.swarm.recipes import REGISTRY, NormalizedResult, Recipe
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
