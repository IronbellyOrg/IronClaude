"""T04.07 -- ``verdict_only_v1`` recipe tests (R-091 / COMP-019 / D-0073).

Covers five layers:

1. **Recipe surface**: ``VerdictOnlyV1.normalize`` produces a canonical
   three-section markdown body (``## Verdict`` / ``## Rationale`` /
   ``## Notes``) with the verdict label alias-mapped to one of
   ``yes`` / ``no`` / ``uncertain`` (or passed through verbatim for
   unknown labels) and confidence reformatted to a 0-100 integer.

2. **REGISTRY**: the ``verdict_only_v1`` slot resolves to a Recipe-
   conforming object (no longer the M2-era ``None`` sentinel) and the
   Wave-2 dispatcher routes a worker through it end-to-end.

3. **§7.4 salvage**: a ``parse_error`` worker with a recoverable body
   is promoted via ``salvaged=True``; a ``parse_error`` worker with
   neither verdict nor rationale nor notes stays failed.

4. **AC-011 boundary**: unknown labels are NOT silently coerced; the
   rationale and supporting body content reach the output verbatim
   (no scoring / dedup / reorder).

5. **Helper coverage**: ``parse_verdict`` / ``parse_confidence`` /
   ``extract_section`` internals.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.normalize import normalize_wave2
from superclaude.cli.swarm.recipes import REGISTRY, NormalizedResult, Recipe
from superclaude.cli.swarm.recipes.verdict_only_v1 import (
    CANONICAL_VERDICTS,
    NOTES_CAP,
    RATIONALE_CAP,
    VERDICT_ALIASES,
    VERDICT_LABEL_CAP,
    VerdictOnlyV1,
    extract_section,
    parse_confidence,
    parse_verdict,
    strip_frontmatter,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "verdict_only_v1"

FIXED_GENERATED = "2026-06-01T11:43:39Z"
FIXED_CHECKSUM = "deadbeefcafe"
FIXED_TARGET = "/tmp/example/auth_login_spec.md"


def _run(
    raw: str,
    *,
    status: str = "success",
    lens: str = "spec-completeness",
    tier: str = "T2-spec",
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
    return VerdictOnlyV1().normalize(raw, args)


# ---------------------------------------------------------------------------
# 1 -- Recipe surface
# ---------------------------------------------------------------------------


def test_recipe_renders_canonical_three_section_body_for_spec_completeness():
    raw = (FIXTURES_DIR / "spec_completeness.raw.txt").read_text(encoding="utf-8")
    result = _run(raw)
    assert result.error is None
    assert result.salvaged is False
    text = result.text

    # Canonical sections present.
    assert "## Verdict" in text
    assert "## Rationale" in text
    assert "## Notes" in text

    # Label alias-mapped from "incomplete" -> "no"; confidence preserved.
    assert "no (40)" in text
    assert "verdict: \"no\"" in text
    assert "verdict_confidence: \"40\"" in text

    # Frontmatter records lens + tier.
    assert 'lens: "spec-completeness"' in text
    assert 'tier: "T2-spec"' in text


def test_recipe_renders_feasibility_probe_fixture():
    raw = (FIXTURES_DIR / "feasibility_probe.raw.txt").read_text(encoding="utf-8")
    result = _run(
        raw,
        lens="feasibility-probe",
        tier="T2-feas",
        target="/tmp/example/wasm-edge-runtime.md",
    )
    assert result.error is None
    assert result.salvaged is False
    text = result.text

    # "risky" aliases to "uncertain".
    assert "uncertain (60)" in text
    assert 'verdict: "uncertain"' in text
    assert 'lens: "feasibility-probe"' in text
    # Slug appears in heading.
    assert (
        "T2-Verdict (feasibility-probe) — wasm-edge-runtime" in text
    )


def test_recipe_renders_canonical_yes_label_with_no_confidence():
    raw = (FIXTURES_DIR / "canonical_yes.raw.txt").read_text(encoding="utf-8")
    result = _run(raw, target="/tmp/example/quick.md")
    assert result.error is None
    assert result.salvaged is False
    text = result.text

    # "yes" with no confidence renders as "yes" alone (no parenthetical).
    assert "## Verdict\nyes\n" in text
    assert "yes ()" not in text
    assert 'verdict_confidence: ""' in text


def test_recipe_records_target_metadata_in_frontmatter():
    raw = (FIXTURES_DIR / "spec_completeness.raw.txt").read_text(encoding="utf-8")
    result = _run(raw)
    assert FIXED_GENERATED in result.text
    assert FIXED_CHECKSUM in result.text
    assert FIXED_TARGET in result.text
    # Slug appears in heading.
    assert "T2-Verdict (spec-completeness) — auth_login_spec" in result.text


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


def test_recipe_freeform_fallback_on_success_with_no_verdict_or_notes():
    raw = "Some prose from the model. No Verdict heading, no Notes heading.\n"
    result = _run(raw, status="success")
    assert result.error is None
    assert result.salvaged is False
    # Freeform fallback: prose collapsed into Rationale; verdict
    # degrades to canonical uncertain so the body stays well-formed.
    assert "Some prose from the model" in result.text
    assert "## Verdict\nuncertain\n" in result.text


def test_recipe_uses_notes_only_fixture_with_uncertain_fallback():
    raw = (FIXTURES_DIR / "notes_only.raw.txt").read_text(encoding="utf-8")
    result = _run(raw)
    assert result.error is None
    # No Verdict heading present, but Notes is non-empty -- recipe
    # records empty verdict label (not coerced) and preserves notes.
    assert "## Notes" in result.text
    assert "token rotation and audit retention" in result.text
    # Verdict label empty -> placeholder line.
    assert "(no verdict returned)" in result.text


def test_recipe_folds_gaps_and_concerns_headings_into_notes():
    raw = (
        "## Verdict\nyes\n"
        "\n## Gaps\nGap A; Gap B\n"
        "\n## Concerns\nConcern X\n"
        "\n## Notes\nNote alpha\n"
    )
    result = _run(raw)
    notes_block = result.text.split("## Notes", 1)[1]
    # All three headings folded; order: Notes, Gaps, Concerns (per
    # recipe's heading iteration order).
    assert "Note alpha" in notes_block
    assert "Gap A; Gap B" in notes_block
    assert "Concern X" in notes_block


# ---------------------------------------------------------------------------
# 2 -- REGISTRY + dispatcher integration
# ---------------------------------------------------------------------------


def test_registry_resolves_verdict_only_v1_to_recipe():
    entry = REGISTRY["verdict_only_v1"]
    assert entry is not None
    assert isinstance(entry, Recipe)
    assert isinstance(entry, VerdictOnlyV1)


def test_registry_verdict_only_v1_protocol_callable():
    recipe = REGISTRY["verdict_only_v1"]
    assert recipe is not None
    result = recipe.normalize(
        "## Verdict\nyes (85) — all requirements covered.\n",
        {
            "target": "/x.md",
            "generated": FIXED_GENERATED,
            "status": "success",
            "lens": "spec-completeness",
        },
    )
    assert isinstance(result, NormalizedResult)
    assert "T2-Verdict (spec-completeness)" in result.text
    assert "yes (85)" in result.text


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


def test_dispatcher_routes_success_worker_through_verdict_only_v1(tmp_path):
    body = (FIXTURES_DIR / "feasibility_probe.raw.txt").read_text(encoding="utf-8")
    worker = _make_worker(tmp_path, 0, status="success", body=body)

    [out] = normalize_wave2(
        [worker],
        "verdict_only_v1",
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
            "lens": "feasibility-probe",
            "tier": "T2-feas",
            "suspect": False,
        },
    )

    assert out.status == "success"
    final_text = Path(worker.final_path).read_text(encoding="utf-8")
    assert "T2-Verdict (feasibility-probe)" in final_text
    assert "uncertain (60)" in final_text
    assert FIXED_CHECKSUM in final_text

    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "verdict_only_v1"
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
        "verdict_only_v1",
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
            "lens": "spec-completeness",
        },
    )

    assert out.status == "success"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "success"


def test_dispatcher_keeps_parse_error_when_body_is_unrecoverable(tmp_path):
    body = "raw stream with no verdict, no notes, no rationale\n"
    worker = _make_worker(tmp_path, 2, status="parse_error", body=body)

    [out] = normalize_wave2(
        [worker],
        "verdict_only_v1",
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
            "lens": "spec-completeness",
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
    assert "uncertain" in result.text


def test_salvage_flag_false_when_status_was_success():
    raw = (FIXTURES_DIR / "spec_completeness.raw.txt").read_text(encoding="utf-8")
    result = _run(raw, status="success")
    assert result.salvaged is False


def test_recipe_recovers_parse_error_with_notes_only():
    raw = (FIXTURES_DIR / "notes_only.raw.txt").read_text(encoding="utf-8")
    result = _run(raw, status="parse_error")
    # Notes alone is enough to salvage.
    assert result.salvaged is True
    assert "token rotation and audit retention" in result.text


# ---------------------------------------------------------------------------
# 4 -- AC-011 boundary: unknown labels pass through, content preserved
# ---------------------------------------------------------------------------


def test_ac011_unknown_label_passes_through_verbatim():
    raw = "## Verdict\nbespoke-label — keep this verbatim\n"
    result = _run(raw)
    text = result.text
    # Unknown label NOT silently coerced to a canonical triple member.
    assert "bespoke-label" in text
    assert 'verdict: "bespoke-label"' in text
    # And it does NOT show up as "yes", "no", or "uncertain".
    assert "## Verdict\nbespoke-label\n" in text


def test_ac011_supporting_body_content_preserved_in_notes():
    raw = (FIXTURES_DIR / "spec_completeness.raw.txt").read_text(encoding="utf-8")
    result = _run(raw)
    # The three Gap rows from the body must reach the Notes section.
    assert "§3.5 Refresh token grant" in result.text
    assert "§5.2 Error code matrix" in result.text
    assert "§7.1 Retention SLA" in result.text


def test_ac011_long_rationale_capped_but_not_dropped():
    long_tail = "x" * (RATIONALE_CAP * 3)
    raw = f"## Verdict\nyes — {long_tail}\n"
    result = _run(raw)
    # Rationale capped at RATIONALE_CAP; not dropped to empty.
    rationale_block = result.text.split("## Rationale\n", 1)[1].split(
        "\n\n##", 1
    )[0]
    assert 0 < len(rationale_block) <= RATIONALE_CAP


def test_ac011_long_notes_capped_but_not_dropped():
    long_notes = "y " * (NOTES_CAP * 2)
    raw = f"## Verdict\nyes\n\n## Notes\n{long_notes}\n"
    result = _run(raw)
    notes_block = result.text.split("## Notes\n", 1)[1]
    # Notes cap is per-section after whitespace collapse. The render
    # adds a trailing newline; account for that.
    assert "y" in notes_block
    assert len(notes_block.strip()) <= NOTES_CAP


# ---------------------------------------------------------------------------
# 5 -- Helper-level coverage
# ---------------------------------------------------------------------------


def test_strip_frontmatter_drops_leading_yaml():
    text = "---\nfoo: 1\n---\n# Body\n"
    assert strip_frontmatter(text).lstrip().startswith("# Body")


def test_strip_frontmatter_passthrough_when_no_frontmatter():
    text = "# Body\nno yaml here\n"
    assert strip_frontmatter(text) == text


def test_canonical_verdicts_triple():
    assert set(CANONICAL_VERDICTS) == {"yes", "no", "uncertain"}


@pytest.mark.parametrize(
    "alias,canonical",
    [
        ("yes", "yes"),
        ("y", "yes"),
        ("complete", "yes"),
        ("feasible", "yes"),
        ("approved", "yes"),
        ("no", "no"),
        ("incomplete", "no"),
        ("infeasible", "no"),
        ("blocker", "no"),
        ("rejected", "no"),
        ("uncertain", "uncertain"),
        ("unclear", "uncertain"),
        ("risky", "uncertain"),
        ("partial", "uncertain"),
        ("maybe", "uncertain"),
    ],
)
def test_verdict_aliases_map_to_canonical_triple(alias, canonical):
    assert VERDICT_ALIASES[alias] == canonical
    assert canonical in CANONICAL_VERDICTS


def test_parse_verdict_handles_em_dash_separator():
    label, conf, rationale = parse_verdict(
        "incomplete (40) — three substantive gaps."
    )
    assert label == "no"
    assert conf == "40"
    assert rationale == "three substantive gaps."


def test_parse_verdict_handles_double_dash_separator():
    label, conf, rationale = parse_verdict("yes -- looks good")
    assert label == "yes"
    assert conf == ""
    assert rationale == "looks good"


def test_parse_verdict_handles_single_hyphen_with_spaces():
    label, conf, rationale = parse_verdict(
        "uncertain (50) - depends on infra availability"
    )
    assert label == "uncertain"
    assert conf == "50"
    assert rationale == "depends on infra availability"


def test_parse_verdict_handles_colon_separator():
    label, conf, rationale = parse_verdict(
        "not-feasible: blocked on missing WASI host bindings"
    )
    assert label == "no"
    assert conf == ""
    assert rationale == "blocked on missing WASI host bindings"


def test_parse_verdict_no_separator_means_no_rationale():
    label, conf, rationale = parse_verdict("uncertain")
    assert label == "uncertain"
    assert conf == ""
    assert rationale == ""


def test_parse_verdict_preserves_unknown_label_verbatim():
    label, conf, rationale = parse_verdict("custom-label — keep me verbatim")
    assert label == "custom-label"
    assert rationale == "keep me verbatim"


def test_parse_verdict_confidence_in_head_only_not_rationale_digits():
    """Digits inside the rationale must not be classified as confidence."""
    label, conf, rationale = parse_verdict("yes — needs 100 tests added")
    assert label == "yes"
    assert conf == ""  # digits in rationale, not head, so no confidence
    assert "100 tests" in rationale


def test_parse_verdict_empty_returns_empty_triple():
    assert parse_verdict("") == ("", "", "")
    assert parse_verdict("   \n  ") == ("", "", "")


def test_parse_confidence_extracts_first_digit_run():
    assert parse_confidence("85%") == "85"
    assert parse_confidence("score: 73") == "73"
    assert parse_confidence("") == ""
    assert parse_confidence("   ") == ""


def test_parse_confidence_clamps_to_zero_to_hundred():
    assert parse_confidence("9000") == "100"


def test_parse_confidence_passes_qualitative_label_through():
    assert parse_confidence("high") == "high"
    assert parse_confidence("  Medium  ") == "Medium"


def test_extract_section_pulls_named_heading():
    body = "## Verdict\nyes — go\n\n## Notes\nlooks fine\n"
    assert extract_section(body, "Verdict", 100).startswith("yes")
    assert extract_section(body, "Notes", 100) == "looks fine"


def test_extract_section_caps_at_provided_cap():
    body = "## Notes\n" + ("x " * 500)
    out = extract_section(body, "Notes", 50)
    assert len(out) <= 50


def test_extract_section_returns_empty_when_no_heading():
    assert extract_section("# Heading\nno notes here", "Notes", 100) == ""


def test_verdict_label_cap_constants_are_positive():
    assert VERDICT_LABEL_CAP > 0
    assert RATIONALE_CAP > 0
    assert NOTES_CAP > 0


# ---------------------------------------------------------------------------
# Frontmatter shape sanity (mirrors sibling recipe tests)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fixture_name",
    ["spec_completeness.raw.txt", "feasibility_probe.raw.txt"],
)
def test_recipe_emits_well_formed_yaml_frontmatter(fixture_name):
    raw = (FIXTURES_DIR / fixture_name).read_text(encoding="utf-8")
    result = _run(raw)
    text = result.text
    # Frontmatter delimiters around the head of the document.
    assert text.startswith("---\n")
    second_delim = text.index("---\n", 4)
    assert second_delim > 0
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
        "verdict:",
        "verdict_confidence:",
    ]:
        assert key in head, f"missing frontmatter key {key!r}"
