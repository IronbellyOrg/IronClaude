"""T04.11 -- §7.4 parse_error -> success salvage promotion tests.

Pins FR-028 / R-095 acceptance:

1. **Salvageable parse_error reclassified as success.** When the
   recipe sets ``NormalizedResult.salvaged=True`` with non-empty text
   AND the worker arrived ``status="parse_error"`` AND
   ``salvage_enabled=True``, ``salvage_parse_error`` flips the status
   to ``success``; the dispatcher records ``salvaged: true`` and
   ``salvage_reason: "promoted_recipe_signal"`` on the meta sidecar.

2. **Non-salvageable parse_errors retain failed status.** Each of
   the four rejection reasons exercised independently:

   - ``rejected_not_parse_error``   -- worker arrived ``success``;
     even with ``salvaged=True`` it is not "promoted" (no §7.4 fire).
   - ``rejected_salvage_disabled``  -- ``salvage_enabled=False``.
   - ``rejected_no_recipe_signal``  -- recipe returned
     ``salvaged=False``.
   - ``rejected_empty_text``        -- recipe returned empty text.

3. **Meta sidecar provenance.** Every recipe-invoking branch records
   ``salvaged`` AND ``salvage_reason``; hard-failure short-circuits
   (timeout / proxy_error) omit ``salvage_reason`` because the recipe
   never ran.

4. **Public-API surface.** :func:`salvage_decision` returns a pure
   :class:`SalvageDecision` (no mutation, no I/O);
   :func:`salvage_parse_error` returns a fresh :class:`WorkerResult`
   via ``dataclasses.replace`` so the input is never mutated.

Two-fixture validation row (phase-4-tasklist.md T04.11):
"Two fixtures: salvageable + non-salvageable both correctly
classified" -- covered by
``test_salvageable_fixture_promotes_to_success`` and
``test_non_salvageable_fixture_stays_parse_error``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.normalize import (
    SALVAGE_PROMOTED,
    SALVAGE_REJECTED_DISABLED,
    SALVAGE_REJECTED_EMPTY_TEXT,
    SALVAGE_REJECTED_NO_RECIPE_SIGNAL,
    SALVAGE_REJECTED_NOT_PARSE_ERROR,
    NormalizedResult,
    SalvageDecision,
    normalize_wave2,
    salvage_decision,
    salvage_parse_error,
)
from superclaude.cli.swarm.recipes import REGISTRY

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


class _SalvagingRecipe:
    """Recipe that always recovers structure (salvaged=True, non-empty text)."""

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        del args
        return NormalizedResult(text=f"recovered:{raw_output}", salvaged=True)


class _BestEffortRecipe:
    """Recipe that produces text but does NOT signal salvage."""

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        del args
        return NormalizedResult(text=f"best-effort:{raw_output}", salvaged=False)


class _EmptySalvagingRecipe:
    """Recipe that signals salvage but produces an empty body."""

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        del raw_output, args
        return NormalizedResult(text="", salvaged=True)


def _make_worker(
    tmp_path: Path,
    index: int,
    *,
    status: str,
    body: str = "raw body",
) -> WorkerResult:
    raw_path = tmp_path / f"worker-{index:02d}.raw.txt"
    raw_path.write_text(body, encoding="utf-8")
    return WorkerResult(
        index=index,
        path=str(tmp_path / f"worker-{index:02d}.md"),
        raw_path=str(raw_path),
        meta_path=str(tmp_path / f"worker-{index:02d}.meta.json"),
        final_path=str(tmp_path / f"worker-{index:02d}.final.md"),
        model_id=f"model-{index:02d}",
        model_label=f"model-{index:02d}",
        bytes=len(body.encode("utf-8")),
        status=status,
        http_code=None if status != "success" else 200,
        attempts=1,
        elapsed_ms=42,
    )


@pytest.fixture
def install_recipe(monkeypatch):
    def _install(name: str, recipe) -> None:
        monkeypatch.setitem(REGISTRY, name, recipe)

    return _install


# ---------------------------------------------------------------------------
# 1 -- Pure decision surface (no I/O, no mutation)
# ---------------------------------------------------------------------------


def test_salvage_decision_promotes_parse_error_with_recovery():
    worker = WorkerResult(status="parse_error", final_path="/tmp/x.md")
    normalized = NormalizedResult(text="recovered body", salvaged=True)

    decision = salvage_decision(worker, normalized=normalized)

    assert isinstance(decision, SalvageDecision)
    assert decision.promoted is True
    assert decision.reason == SALVAGE_PROMOTED
    assert decision.salvaged_text_bytes == len(b"recovered body")


@pytest.mark.parametrize(
    "non_parse_status",
    ["success", "timeout", "proxy_error"],
)
def test_salvage_decision_rejects_non_parse_error(non_parse_status):
    worker = WorkerResult(status=non_parse_status, final_path="/tmp/x.md")
    normalized = NormalizedResult(text="recovered body", salvaged=True)

    decision = salvage_decision(worker, normalized=normalized)

    assert decision.promoted is False
    assert decision.reason == SALVAGE_REJECTED_NOT_PARSE_ERROR


def test_salvage_decision_rejects_when_salvage_disabled():
    worker = WorkerResult(status="parse_error", final_path="/tmp/x.md")
    normalized = NormalizedResult(text="recovered body", salvaged=True)

    decision = salvage_decision(worker, normalized=normalized, salvage_enabled=False)

    assert decision.promoted is False
    assert decision.reason == SALVAGE_REJECTED_DISABLED


def test_salvage_decision_rejects_when_recipe_did_not_signal_salvage():
    worker = WorkerResult(status="parse_error", final_path="/tmp/x.md")
    normalized = NormalizedResult(text="best-effort body", salvaged=False)

    decision = salvage_decision(worker, normalized=normalized)

    assert decision.promoted is False
    assert decision.reason == SALVAGE_REJECTED_NO_RECIPE_SIGNAL


def test_salvage_decision_rejects_empty_text_even_when_salvaged():
    worker = WorkerResult(status="parse_error", final_path="/tmp/x.md")
    normalized = NormalizedResult(text="", salvaged=True)

    decision = salvage_decision(worker, normalized=normalized)

    assert decision.promoted is False
    assert decision.reason == SALVAGE_REJECTED_EMPTY_TEXT


# ---------------------------------------------------------------------------
# 2 -- salvage_parse_error returns promoted WorkerResult
# ---------------------------------------------------------------------------


def test_salvage_parse_error_promotes_status_to_success():
    worker = WorkerResult(status="parse_error", index=3, bytes=0)
    normalized = NormalizedResult(text="recovered", salvaged=True)

    out = salvage_parse_error(worker, normalized=normalized)

    assert out is not worker  # fresh dataclass via replace
    assert out.status == "success"
    assert out.index == 3
    assert out.bytes == len(b"recovered")


def test_salvage_parse_error_returns_unchanged_copy_on_rejection():
    worker = WorkerResult(status="parse_error", index=7, bytes=99)
    normalized = NormalizedResult(text="anything", salvaged=False)

    out = salvage_parse_error(worker, normalized=normalized)

    assert out is not worker
    assert out.status == "parse_error"
    assert out.index == 7
    assert out.bytes == 99


def test_salvage_parse_error_does_not_mutate_input():
    worker = WorkerResult(status="parse_error", bytes=0)
    normalized = NormalizedResult(text="recovered", salvaged=True)

    salvage_parse_error(worker, normalized=normalized)

    assert worker.status == "parse_error"
    assert worker.bytes == 0


def test_salvage_parse_error_does_not_promote_success_worker():
    worker = WorkerResult(status="success", bytes=10)
    normalized = NormalizedResult(text="recovered", salvaged=True)

    out = salvage_parse_error(worker, normalized=normalized)

    assert out.status == "success"
    assert out.bytes == 10


# ---------------------------------------------------------------------------
# 3 -- Dispatcher integration: meta sidecar records salvage provenance
# ---------------------------------------------------------------------------


def test_salvageable_fixture_promotes_to_success(tmp_path, install_recipe):
    """Fixture #1 (salvageable): parse_error + salvaging recipe -> success."""
    install_recipe("findings_table_v1", _SalvagingRecipe())
    worker = _make_worker(tmp_path, 0, status="parse_error", body="messy body")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == "success"
    assert Path(worker.final_path).read_text(encoding="utf-8") == "recovered:messy body"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "success"
    assert meta["salvage_reason"] == SALVAGE_PROMOTED


def test_non_salvageable_fixture_stays_parse_error(tmp_path, install_recipe):
    """Fixture #2 (non-salvageable): parse_error + best-effort recipe -> stays parse_error."""
    install_recipe("findings_table_v1", _BestEffortRecipe())
    worker = _make_worker(tmp_path, 1, status="parse_error", body="messy body")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == "parse_error"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is False
    assert meta["status"] == "parse_error"
    assert meta["salvage_reason"] == SALVAGE_REJECTED_NO_RECIPE_SIGNAL


def test_salvage_disabled_blocks_promotion(tmp_path, install_recipe):
    """salvage_enabled=False forces parse_error to stay, recording reason."""
    install_recipe("findings_table_v1", _SalvagingRecipe())
    worker = _make_worker(tmp_path, 2, status="parse_error", body="messy")

    [out] = normalize_wave2([worker], "findings_table_v1", salvage_enabled=False)

    assert out.status == "parse_error"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True  # recipe still signaled salvage
    assert meta["status"] == "parse_error"  # but promotion was gated off
    assert meta["salvage_reason"] == SALVAGE_REJECTED_DISABLED


def test_empty_text_blocks_promotion(tmp_path, install_recipe):
    """Empty body with salvaged=True is NOT promoted (no body to emit)."""
    install_recipe("findings_table_v1", _EmptySalvagingRecipe())
    worker = _make_worker(tmp_path, 3, status="parse_error", body="anything")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == "parse_error"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "parse_error"
    assert meta["salvage_reason"] == SALVAGE_REJECTED_EMPTY_TEXT


def test_success_worker_records_not_parse_error_reason(tmp_path, install_recipe):
    """A success worker exercising a salvaging recipe records the
    "rejected_not_parse_error" reason -- promotion never fires because
    success was never parse_error to begin with."""
    install_recipe("findings_table_v1", _SalvagingRecipe())
    worker = _make_worker(tmp_path, 4, status="success", body="ok")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == "success"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "success"
    assert meta["salvage_reason"] == SALVAGE_REJECTED_NOT_PARSE_ERROR


# ---------------------------------------------------------------------------
# 4 -- Hard-failure short-circuit omits salvage_reason
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("hard_status", ["timeout", "proxy_error"])
def test_hard_failure_meta_omits_salvage_reason(tmp_path, install_recipe, hard_status):
    install_recipe("findings_table_v1", _SalvagingRecipe())
    worker = _make_worker(tmp_path, 5, status=hard_status, body="")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == hard_status
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    # Recipe was never invoked -> no §7.4 branch to classify.
    assert "salvage_reason" not in meta
    assert meta["salvaged"] is False
    assert meta["status"] == hard_status


# ---------------------------------------------------------------------------
# 5 -- Recipe exception: parse_error downgrade records salvage_reason
# ---------------------------------------------------------------------------


def test_recipe_exception_records_no_recipe_signal_reason(tmp_path, install_recipe):
    """When a recipe raises, the synthesized NormalizedResult has
    salvaged=False so the salvage decision rejects with
    "rejected_no_recipe_signal" -- recorded on the sidecar so callers
    can distinguish "recipe failed cleanly" from the other rejection
    branches."""

    class _RaisingRecipe:
        def normalize(self, raw_output, args):
            del raw_output, args
            raise ValueError("synthetic parse failure")

    install_recipe("findings_table_v1", _RaisingRecipe())
    worker = _make_worker(tmp_path, 6, status="success", body="anything")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == "parse_error"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["status"] == "parse_error"
    assert meta["salvaged"] is False
    assert meta["salvage_reason"] == SALVAGE_REJECTED_NO_RECIPE_SIGNAL
    assert "synthetic parse failure" in meta["error"]
