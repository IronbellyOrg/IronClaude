"""``bare-review-v1`` recipe tests (R-088 / COMP-016 / D-0070).

Legacy-independent recipe coverage (post M8/M9 migration -- WS-C retires the
legacy ``t2_normalize.py``):

1. **Recipe salvage-flag semantics**: the recipe's ``salvaged`` flag is True iff
   the input status was ``parse_error`` and the recipe recovered non-empty text
   (the §7.4 promotion in semantic form).

2. **REGISTRY surface**: the ``bare-review-v1`` slot resolves to a
   Recipe-conforming object (no longer the M2-era ``None`` sentinel),
   and the Wave-2 dispatcher routes a worker through it end-to-end
   (raw read → recipe call → atomic ``final_path`` write → meta sidecar
   emission → salvage promotion on ``parse_error``).

The legacy-vs-recipe **byte-identity** A/B parity (formerly here as
``test_legacy_vs_recipe_byte_identical``, which imported the standalone legacy
``t2_normalize.py`` via importlib) is now provided by the permanent
**CLI-vs-frozen-golden** gate in ``tests/swarm/test_bare_review_parity.py``: it
drives ``superclaude swarm run --lens bare-review`` and asserts byte-equality
against a golden frozen from the real legacy output -- so the parity coverage
survives the WS-C deletion of the legacy script (this file no longer depends on
it at run time).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.normalize import normalize_wave2
from superclaude.cli.swarm.recipes import REGISTRY, NormalizedResult, Recipe
from superclaude.cli.swarm.recipes.bare_review_v1 import BareReviewV1

# ---------------------------------------------------------------------------
# Fixture corpus
# ---------------------------------------------------------------------------


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "bare_review_v1"

FIXED_GENERATED = "2026-06-01T11:19:39Z"
FIXED_CHECKSUM = "deadbeefcafe"
FIXED_TARGET = "/tmp/example/target.py"


# Each fixture: (filename, worker_status). The worker_status mirrors
# what ``t2_dispatch`` would have stamped on the meta sidecar; the
# recipe uses it to decide §7.4 salvage; the legacy script reads it
# from the meta JSON sidecar.
FIXTURES: list[tuple[str, str]] = [
    ("basic_findings.raw.txt", "success"),
    ("salvage.raw.txt", "parse_error"),
    ("verdict_only.raw.txt", "success"),
    ("freeform_fallback.raw.txt", "success"),
    ("odd_cites.raw.txt", "success"),
]


def _run_recipe(
    raw_text: str,
    status: str,
    elapsed_ms: int,
    model_id: str,
    model_label: str,
    caller_label: str,
) -> NormalizedResult:
    """Call BareReviewV1.normalize() with deterministic args."""
    recipe = BareReviewV1()
    args: dict[str, Any] = {
        "status": status,
        "target": FIXED_TARGET,
        "target_checksum": FIXED_CHECKSUM,
        "target_truncated": False,
        "model_id": model_id,
        "model_label": model_label,
        "caller_label": caller_label,
        "elapsed_ms": elapsed_ms,
        "generated": FIXED_GENERATED,
    }
    return recipe.normalize(raw_text, args)


# ---------------------------------------------------------------------------
# 1 -- Recipe salvage-flag semantics (byte-identity parity now lives in the
# CLI-vs-frozen-golden gate at tests/swarm/test_bare_review_parity.py)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("filename,status", FIXTURES)
def test_recipe_salvage_flag_matches_status_transition(filename: str, status: str):
    """Recipe's ``salvaged`` flag is True iff input status was
    ``parse_error`` and the recipe recovered non-empty text. Mirrors the
    legacy §7.4 promotion in semantic (not byte) form."""
    raw_text = (FIXTURES_DIR / filename).read_text(encoding="utf-8")
    result = _run_recipe(raw_text, status, 0, "m", "M", "")
    if status == "parse_error" and result.text:
        assert result.salvaged is True
    else:
        assert result.salvaged is False


def _make_tmp_dir(tmp_path: Path) -> Path:
    legacy_dir = tmp_path / "legacy"
    legacy_dir.mkdir(parents=True, exist_ok=True)
    return legacy_dir


# ---------------------------------------------------------------------------
# 2 -- REGISTRY surface
# ---------------------------------------------------------------------------


def test_registry_resolves_bare_review_v1_to_recipe():
    """T04.03 acceptance: the slot is no longer ``None``."""
    entry = REGISTRY["bare-review-v1"]
    assert entry is not None
    assert isinstance(entry, Recipe)
    assert isinstance(entry, BareReviewV1)


def test_registry_bare_review_v1_protocol_callable():
    """The registered recipe accepts the canonical Protocol signature."""
    recipe = REGISTRY["bare-review-v1"]
    assert recipe is not None
    result = recipe.normalize(
        "## Findings\n\n## Verdict\nok\n",
        {"target": "/x.py", "generated": FIXED_GENERATED, "status": "success"},
    )
    assert isinstance(result, NormalizedResult)
    assert "T2-Bare Review" in result.text


# ---------------------------------------------------------------------------
# 3 -- Dispatcher integration: end-to-end through normalize_wave2
# ---------------------------------------------------------------------------


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


def test_dispatcher_routes_success_worker_through_bare_review_v1(tmp_path):
    """normalize_wave2 picks the registered recipe and writes the
    rendered body to final_path; meta sidecar records the recipe."""
    body = (FIXTURES_DIR / "basic_findings.raw.txt").read_text(encoding="utf-8")
    worker = _make_worker(tmp_path, 0, status="success", body=body)

    [out] = normalize_wave2(
        [worker],
        "bare-review-v1",
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
        },
    )

    assert out.status == "success"
    final_text = Path(worker.final_path).read_text(encoding="utf-8")
    assert "T2-Bare Review" in final_text
    assert "F-01" in final_text
    assert "deadbeefcafe" in final_text

    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "bare-review-v1"
    assert meta["salvaged"] is False
    assert meta["status"] == "success"


def test_dispatcher_promotes_parse_error_via_salvage_flag(tmp_path):
    """A parse_error worker whose body is recoverable is promoted to
    success per §7.4. The recipe sets ``salvaged=True``; the dispatcher
    flips the status."""
    body = (FIXTURES_DIR / "salvage.raw.txt").read_text(encoding="utf-8")
    worker = _make_worker(tmp_path, 1, status="parse_error", body=body)

    [out] = normalize_wave2(
        [worker],
        "bare-review-v1",
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
        },
    )

    assert out.status == "success"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "success"


def test_dispatcher_keeps_parse_error_when_body_is_unrecoverable(tmp_path):
    """A parse_error worker with no findings AND no verdict stays
    parse_error; the recipe returns empty text and the dispatcher does
    not promote."""
    body = "this body has no findings table and no verdict heading\n"
    worker = _make_worker(tmp_path, 2, status="parse_error", body=body)

    [out] = normalize_wave2(
        [worker],
        "bare-review-v1",
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
        },
    )

    assert out.status == "parse_error"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is False
    assert meta["status"] == "parse_error"
    # Recipe surfaces the recovery failure via error field.
    assert meta.get("error", "")
    assert not Path(worker.final_path).exists()


# ---------------------------------------------------------------------------
# 4 -- AC-011 boundary -- findings preserved verbatim (no scoring/dedup)
# ---------------------------------------------------------------------------


def test_recipe_preserves_all_findings_including_duplicates():
    """AC-011: recipes MUST NOT dedupe or reorder findings. T04.14 lands
    the full boundary suite; this is the bare_review_v1 slice."""
    raw = (
        "## Findings\n\n"
        "| ID | Sev | Claim | Cite | SelfConf |\n"
        "|----|-----|-------|------|----------|\n"
        "| F-01 | crit | duplicate claim text | x.py:1 | 50 |\n"
        "| F-02 | crit | duplicate claim text | x.py:1 | 50 |\n"
        "| F-03 | high | second unique row | x.py:2 | 60 |\n"
        "| F-04 | crit | duplicate claim text | x.py:1 | 50 |\n"
        "\n## Verdict\nok\n"
    )
    result = _run_recipe(raw, "success", 0, "m", "M", "")
    # 4 row ids present, in input order (renumbered F-01..F-04 by the
    # renderer but preserving count + order).
    assert result.text.count("duplicate claim text") == 3
    assert result.text.count("second unique row") == 1
    # Renumbered row IDs are sequential 1..N (legacy behavior).
    assert "| F-01 |" in result.text
    assert "| F-04 |" in result.text
