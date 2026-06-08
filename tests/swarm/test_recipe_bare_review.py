"""T04.03 -- ``bare-review-v1`` recipe parity tests (R-088 / COMP-016 / D-0070).

Two-layer coverage:

1. **A/B parity gate (TEST-003)**: every raw fixture under
   ``tests/swarm/fixtures/bare_review_v1/`` is fanned through both
   paths -- the legacy
   ``src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py``
   script and the new
   :class:`superclaude.cli.swarm.recipes.bare_review_v1.BareReviewV1`
   recipe -- with a deterministic ``generated`` timestamp threaded
   through both, and the per-reviewer normalized markdown is asserted
   byte-identical. This pins the M8 bare-review parity gate.

2. **REGISTRY surface**: the ``bare-review-v1`` slot resolves to a
   Recipe-conforming object (no longer the M2-era ``None`` sentinel),
   and the Wave-2 dispatcher routes a worker through it end-to-end
   (raw read → recipe call → atomic ``final_path`` write → meta sidecar
   emission → salvage promotion on ``parse_error``).

The legacy script lives outside the Python package (``src/superclaude/
skills/sc-bare-review/scripts/`` has no ``__init__.py``), so the helper
loads it via :mod:`importlib.util` and invokes ``main()`` in-process
with a monkeypatched ``iso_now`` and a stubbed ``sys.argv``. That lets
both legacy and recipe stamp the same ``generated`` field and produce
byte-identical frontmatter without subprocess overhead.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import types
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

REPO_ROOT = Path(__file__).resolve().parents[2]
LEGACY_SCRIPT = (
    REPO_ROOT
    / "src"
    / "superclaude"
    / "skills"
    / "sc-bare-review"
    / "scripts"
    / "t2_normalize.py"
)

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


# ---------------------------------------------------------------------------
# Legacy loader
# ---------------------------------------------------------------------------


def _load_legacy() -> types.ModuleType:
    """Import the standalone ``t2_normalize.py`` script as a module."""
    assert LEGACY_SCRIPT.exists(), (
        f"legacy script missing at {LEGACY_SCRIPT} -- parity gate cannot run"
    )
    spec = importlib.util.spec_from_file_location(
        "t2_normalize_legacy_for_parity", str(LEGACY_SCRIPT)
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_legacy(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    raw_text: str,
    status: str,
    elapsed_ms: int,
    model_id: str,
    model_label: str,
    caller_label: str,
) -> str:
    """Stage a one-reviewer manifest, run legacy main(), return final md."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    raw_path = tmp_path / "reviewer.raw.md"
    meta_path = tmp_path / "reviewer.meta.json"
    final_path = tmp_path / "reviewer.final.md"
    contract_path = tmp_path / "return-contract.yaml"
    manifest_path = tmp_path / "manifest.json"

    raw_path.write_text(raw_text, encoding="utf-8")
    meta_path.write_text(
        json.dumps({"status": status, "elapsed_ms": elapsed_ms}),
        encoding="utf-8",
    )

    manifest = {
        "target": FIXED_TARGET,
        "target_checksum": FIXED_CHECKSUM,
        "target_truncated": False,
        "caller_label": caller_label,
        "reviewers_requested": 1,
        "contract_path": str(contract_path),
        "reviewers": [
            {
                "model_id": model_id,
                "model_label": model_label,
                "raw_path": str(raw_path),
                "meta_path": str(meta_path),
                "final_path": str(final_path),
            }
        ],
    }
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    legacy = _load_legacy()
    monkeypatch.setattr(legacy, "iso_now", lambda: FIXED_GENERATED)
    monkeypatch.setattr(
        sys, "argv", ["t2_normalize.py", "--manifest", str(manifest_path)]
    )
    exit_code = legacy.main()
    assert exit_code == 0

    # On §7.4-stays-failed branches the legacy script does not write a
    # final file -- mirror the recipe's empty-text return in that case.
    if not final_path.exists():
        return ""
    return final_path.read_text(encoding="utf-8")


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
# 1 -- A/B parity gate
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("filename,status", FIXTURES)
def test_legacy_vs_recipe_byte_identical(
    monkeypatch, tmp_path, filename: str, status: str
):
    """Legacy ``t2_normalize`` and ``BareReviewV1`` emit byte-identical
    markdown for every fixture in the corpus. The deterministic
    ``generated`` field neutralises the only wall-clock-dependent
    frontmatter value; everything else is mechanical."""
    raw_text = (FIXTURES_DIR / filename).read_text(encoding="utf-8")
    elapsed_ms = 12345
    model_id = "test-model-id"
    model_label = "Test Model Label"
    caller_label = "parity-gate"

    # Each call needs its own tmp subdir so legacy stages cleanly.
    legacy_md = _run_legacy(
        monkeypatch,
        tmp_path / "legacy",
        raw_text,
        status,
        elapsed_ms,
        model_id,
        model_label,
        caller_label,
    )
    (tmp_path / "legacy").mkdir(exist_ok=True)

    recipe_result = _run_recipe(
        raw_text, status, elapsed_ms, model_id, model_label, caller_label
    )

    assert recipe_result.text == legacy_md, (
        f"byte parity broke for {filename!r}: "
        f"legacy={len(legacy_md)} bytes, recipe={len(recipe_result.text)} bytes"
    )


@pytest.mark.parametrize("filename,status", FIXTURES)
def test_recipe_salvage_flag_matches_status_transition(
    filename: str, status: str
):
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
    body = (FIXTURES_DIR / "basic_findings.raw.txt").read_text(
        encoding="utf-8"
    )
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
