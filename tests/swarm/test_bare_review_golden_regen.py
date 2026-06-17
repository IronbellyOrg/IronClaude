"""Env-gated one-shot regeneration of the bare-review CLI-vs-golden FROZEN GOLDEN.

WS-B of the sc-bare-review M8/M9 corrective migration. This module runs the
**real** legacy ``t2_normalize.py`` aggregator against the fixed fixture corpus
with **CLI-aligned args**, normalizes the single non-portable field (the absolute
target path) to a sentinel, and writes the frozen golden tree under
``tests/swarm/fixtures/bare_review_v1/golden/<scenario>/``.

The frozen golden is the permanent parity reference that
``tests/swarm/test_bare_review_parity.py`` (rebuilt in Step 4.3) asserts the live
``superclaude swarm run --lens bare-review`` output against — so the parity gate
survives the WS-C deletion of ``t2_normalize.py`` (no legacy script needed at run
time).

Why CLI-aligned args (not the legacy parity test's fake pins)
============================================================
``BareReviewV1.normalize`` (the recipe the CLI runs) is a byte-faithful port of
legacy ``t2_normalize`` — so ``legacy(args) == CLI-recipe(args)`` for identical
(raw body, args). The live CLI inline path emits **empty** model identity +
**empty** caller_label + ``elapsed_ms=0`` and a **real** sha256 checksum, so the
golden is captured with those exact values (see
``phase-outputs/discovery/ws-b-golden-design.md``). The checksum is computed via
the SAME ``preflight._target_checksum`` / ``_truncate_target`` the CLI uses, so it
matches by construction.

Regeneration is a DELIBERATE, HUMAN-APPROVED act (never auto-blessed)
===================================================================
    SWARM_REGEN_GOLDEN=1 uv run pytest tests/swarm/test_bare_review_golden_regen.py -v

With ``SWARM_REGEN_GOLDEN`` unset (the default) this module SKIPS, so CI never
silently re-blesses the golden. Mirrors the ``SWARM_REAL_E2E`` gating pattern at
``tests/swarm/test_e2e_real_proxy.py``. See ``golden/README.md``.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import types
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm.preflight import _target_checksum, _truncate_target

# ---------------------------------------------------------------------------
# Paths + pins (Step 4.3's permanent gate mirrors these constants).
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "bare_review_v1"
GOLDEN_DIR = FIXTURES_DIR / "golden"
TARGET_FIXTURE = GOLDEN_DIR / "_review_target.py"
LEGACY_SCRIPT = (
    REPO_ROOT
    / "src"
    / "superclaude"
    / "skills"
    / "sc-bare-review"
    / "scripts"
    / "t2_normalize.py"
)

# The deterministic ``generated`` pin (the only wall-clock field). Both the
# golden capture and the permanent gate stamp this so the byte comparison is
# mechanical.
FIXED_GENERATED = "2026-06-01T17:59:55Z"

# The bare-review lens default_target_line_cap (preflight expands 4000 -> lens
# default; for the small fixture target truncation is a no-op).
DEFAULT_LINE_CAP = 4000

# CLI-aligned per-reviewer args: the inline ``run_cmd`` path does NOT thread
# model identity into recipe_args (so the rendered body carries empty model
# fields), emits an empty caller_label unless ``--label`` is passed, and stamps
# elapsed_ms=0 for the stub transport.
CLI_MODEL_ID = ""
CLI_MODEL_LABEL = ""
CLI_CALLER_LABEL = ""
CLI_ELAPSED_MS = 0

# Sentinel substituted for the absolute target path so the committed golden is
# portable across checkouts/CI. The permanent gate applies the SAME substitution
# to the live CLI body before byte comparison (symmetric -> cannot mask a real
# divergence).
TARGET_SENTINEL = "<<TARGET>>"
OUTPUT_DIR_SENTINEL = "<<OUTPUT_DIR>>"

# Scenario plans -- identical to the legacy parity gate's SCENARIOS
# (fixture filename or "" for a body-less slot, upstream worker status).
SCENARIOS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "all-success",
        [
            ("basic_findings.raw.txt", "success"),
            ("verdict_only.raw.txt", "success"),
            ("odd_cites.raw.txt", "success"),
        ],
    ),
    (
        "partial-with-timeout",
        [
            ("basic_findings.raw.txt", "success"),
            ("verdict_only.raw.txt", "success"),
            ("", "timeout"),  # body-less slot -> no final.md
        ],
    ),
    (
        "salvage-promoted",
        [
            ("basic_findings.raw.txt", "success"),
            ("verdict_only.raw.txt", "success"),
            ("salvage.raw.txt", "parse_error"),  # §7.4 promoted to success
        ],
    ),
]


pytestmark = pytest.mark.skipif(
    os.environ.get("SWARM_REGEN_GOLDEN") != "1",
    reason=(
        "Golden regeneration is a deliberate, human-approved act. "
        "Set SWARM_REGEN_GOLDEN=1 to re-bless the frozen golden tree."
    ),
)


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------


def _slug_model(model_id: str) -> str:
    """Mirror the legacy bash ``slug`` routine (== parity test's _slug_model)."""
    cleaned: list[str] = []
    prev_dash = False
    for ch in model_id.lower():
        if ch.isalnum():
            cleaned.append(ch)
            prev_dash = False
        elif not prev_dash:
            cleaned.append("-")
            prev_dash = True
    out = "".join(cleaned).strip("-")
    return out or "m"


def _load_legacy() -> types.ModuleType:
    """Import the standalone ``t2_normalize.py`` via importlib."""
    spec = importlib.util.spec_from_file_location(
        "t2_normalize_legacy_for_golden_regen", str(LEGACY_SCRIPT)
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _golden_checksum() -> str:
    """Checksum the committed target the SAME way the CLI preflight does."""
    raw = TARGET_FIXTURE.read_bytes()
    truncated_bytes, _ = _truncate_target(raw, DEFAULT_LINE_CAP)
    return _target_checksum(truncated_bytes)


def _stage_manifest(
    run_dir: Path,
    target_path: str,
    checksum: str,
    plan: list[tuple[str, str]],
) -> tuple[Path, list[dict[str, Any]]]:
    """Stage a legacy manifest + per-reviewer sidecars with CLI-aligned args."""
    run_dir.mkdir(parents=True, exist_ok=True)
    reviewers: list[dict[str, Any]] = []
    for index, (fixture_name, status) in enumerate(plan, start=1):
        slug = _slug_model(CLI_MODEL_ID)
        base = f"bare-review-{index:02d}-{slug}"
        raw_path = run_dir / f"{base}.md.raw"
        meta_path = run_dir / f"{base}.meta.json"
        final_path = run_dir / f"{base}.md"

        if fixture_name:
            raw_text = (FIXTURES_DIR / fixture_name).read_text(encoding="utf-8")
            raw_path.write_text(raw_text, encoding="utf-8")

        meta_path.write_text(
            json.dumps(
                {
                    "status": status,
                    "elapsed_ms": CLI_ELAPSED_MS,
                    "http_code": 200 if status == "success" else None,
                    "attempts": 1,
                    "model_id": CLI_MODEL_ID,
                }
            ),
            encoding="utf-8",
        )

        reviewers.append(
            {
                "index": index,
                "model_id": CLI_MODEL_ID,
                "model_label": CLI_MODEL_LABEL,
                "raw_path": str(raw_path),
                "meta_path": str(meta_path),
                "final_path": str(final_path),
                "base": base,
                "_fixture": fixture_name,
                "_status": status,
            }
        )

    manifest_path = run_dir / "manifest.json"
    contract_path = run_dir / "return-contract.yaml"
    manifest = {
        "contract_version": "1.0",
        "target": target_path,
        "target_checksum": checksum,
        "target_truncated": False,
        "caller_label": CLI_CALLER_LABEL,
        "reviewers_requested": len(plan),
        "contract_path": str(contract_path),
        "reviewers": [
            {
                "index": r["index"],
                "model_id": r["model_id"],
                "model_label": r["model_label"],
                "raw_path": r["raw_path"],
                "meta_path": r["meta_path"],
                "final_path": r["final_path"],
            }
            for r in reviewers
        ],
    }
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path, reviewers


def _normalize(text: str, target_path: str, run_dir: str) -> str:
    """Replace non-portable absolute paths with stable sentinels."""
    return text.replace(target_path, TARGET_SENTINEL).replace(
        run_dir, OUTPUT_DIR_SENTINEL
    )


# ---------------------------------------------------------------------------
# Regen entry.
# ---------------------------------------------------------------------------


def test_regenerate_frozen_golden(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Re-bless the frozen golden tree from the real legacy aggregator.

    Skipped unless SWARM_REGEN_GOLDEN=1. Requires the legacy script present
    (pre-WS-C). Writes per-reviewer normalized ``.md`` + ``return-contract.yaml``
    per scenario under ``golden/<scenario>/``.
    """
    assert LEGACY_SCRIPT.exists(), (
        f"legacy t2_normalize.py missing at {LEGACY_SCRIPT}; the golden must be "
        f"captured BEFORE WS-C deletes the script. Post-deletion, re-blessing "
        f"must drive the CLI (a separate human-approved step)."
    )
    target_path = str(TARGET_FIXTURE.resolve())
    checksum = _golden_checksum()

    for scenario_id, plan in SCENARIOS:
        run_dir = tmp_path / scenario_id
        manifest_path, reviewers = _stage_manifest(run_dir, target_path, checksum, plan)

        legacy = _load_legacy()
        monkeypatch.setattr(legacy, "iso_now", lambda: FIXED_GENERATED)
        monkeypatch.setattr(
            sys, "argv", ["t2_normalize.py", "--manifest", str(manifest_path)]
        )
        exit_code = legacy.main()
        assert exit_code == 0, (
            f"legacy main() exited {exit_code} for scenario {scenario_id}"
        )

        scenario_golden = GOLDEN_DIR / scenario_id
        scenario_golden.mkdir(parents=True, exist_ok=True)
        run_dir_abs = str(run_dir.resolve())

        # Per-reviewer normalized bodies (only slots that produced a final.md).
        for rev in reviewers:
            final_path = Path(rev["final_path"])
            if not final_path.exists():
                continue
            body = final_path.read_text(encoding="utf-8")
            body = _normalize(body, target_path, run_dir_abs)
            (scenario_golden / f"{rev['base']}.md").write_text(body, encoding="utf-8")

        # Legacy-schema contract reference (semantic fields; the permanent gate
        # extracts CLI-contract fields rather than byte-comparing this file).
        contract_path = run_dir / "return-contract.yaml"
        contract_text = contract_path.read_text(encoding="utf-8")
        contract_text = _normalize(contract_text, target_path, run_dir_abs)
        (scenario_golden / "return-contract.yaml").write_text(
            contract_text, encoding="utf-8"
        )

    # Sanity: every scenario dir now carries a contract + >=2 bodies.
    for scenario_id, plan in SCENARIOS:
        d = GOLDEN_DIR / scenario_id
        assert (d / "return-contract.yaml").exists(), f"{scenario_id}: no contract"
        bodies = sorted(d.glob("bare-review-*.md"))
        expected_bodies = sum(1 for fx, st in plan if fx and st != "timeout")
        assert len(bodies) == expected_bodies, (
            f"{scenario_id}: {len(bodies)} bodies, expected {expected_bodies}"
        )
