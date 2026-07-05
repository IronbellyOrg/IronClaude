"""T04.01 -- COMP-008 Wave 2 normalize dispatcher unit tests.

Pins the per-worker normalize contract:

1. ``normalize_wave2`` resolves the recipe from
   :data:`recipes.REGISTRY` and falls back to passthrough when the
   M2-era ``None`` sentinel is still in place (pre-T04.03..T04.09).
2. Unknown recipe names raise ``KeyError`` (lens validator drift --
   would have been caught at preflight per FR-LENSREG.NS / U-008).
3. Happy-path: success worker -> recipe applied -> ``final_path``
   written atomically (write-to-tmp + ``os.replace``) -> meta sidecar
   records ``recipe`` / ``schema_version`` / ``salvaged`` flag.
4. Parse-error branch: recipe raises -> dispatcher catches -> status
   downgraded to ``parse_error`` and ``error`` field appears on the
   meta sidecar.
5. Hard-failure short-circuit: ``timeout`` and ``proxy_error`` workers
   skip normalization (no ``final_path`` write) but still emit the
   meta sidecar so the per-worker surface is uniform across statuses.
6. Salvage-flag passthrough: when the recipe sets ``salvaged=True`` on
   a worker that arrived ``status='parse_error'`` with non-empty text,
   the dispatcher promotes to ``success`` and records ``salvaged:
   true`` on the sidecar. T04.11 expands the §7.4 policy.
7. Input list is not mutated -- each output is a fresh dataclass via
   ``dataclasses.replace``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm import normalize as normalize_mod
from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.normalize import (
    NormalizedResult,
    Recipe,
    normalize_wave2,
)
from superclaude.cli.swarm.recipes import REGISTRY

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


class _EchoRecipe:
    """Test recipe -- echoes raw with a ``# normalized`` header."""

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        del args
        return NormalizedResult(text=f"# normalized\n{raw_output}", salvaged=False)


class _RaisingRecipe:
    """Test recipe -- raises ValueError to exercise the parse_error branch."""

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        del raw_output, args
        raise ValueError("synthetic parse failure")


class _SalvagingRecipe:
    """Test recipe -- recovers structure and signals salvage."""

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        del args
        return NormalizedResult(text=f"recovered:{raw_output}", salvaged=True)


def _make_worker(
    tmp_path: Path,
    index: int,
    *,
    status: str = "success",
    body: str = "raw body",
) -> WorkerResult:
    """Build a WorkerResult with raw_path / meta_path / final_path resolved
    under ``tmp_path`` so each test owns its scratch directory."""
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
        http_code=200 if status == "success" else None,
        attempts=1,
        elapsed_ms=42,
    )


@pytest.fixture
def install_recipe(monkeypatch):
    """Install a recipe under a known name in REGISTRY for the test scope."""

    def _install(name: str, recipe: Recipe) -> None:
        # Use setitem semantics that monkeypatch reverses on teardown.
        monkeypatch.setitem(REGISTRY, name, recipe)

    return _install


# ---------------------------------------------------------------------------
# 1 -- Recipe resolution: passthrough fallback on None sentinel
# ---------------------------------------------------------------------------


def test_passthrough_fallback_when_registry_value_is_none(tmp_path, install_recipe):
    """REGISTRY accepts ``None`` sentinels; dispatcher must fall back
    to its internal passthrough so the M3 -> M4 handshake works for
    any recipe slot whose concrete object has not yet landed.

    T04.08 replaced ``REGISTRY["passthrough"]`` with the real
    :class:`Passthrough`, so this test reinstates the ``None``
    sentinel for the test scope via :func:`install_recipe` to keep
    coverage on the dispatcher's None-fallback branch (still relied
    on by any open-class slot whose value is left at ``None``).
    """
    assert "passthrough" in REGISTRY
    install_recipe("passthrough", None)  # type: ignore[arg-type]
    assert REGISTRY["passthrough"] is None

    worker = _make_worker(tmp_path, 0, body="hello\n")
    [out] = normalize_wave2([worker], "passthrough")

    assert out.status == "success"
    # final_path written verbatim (passthrough returns raw unchanged).
    assert Path(worker.final_path).read_text(encoding="utf-8") == "hello\n"
    # meta sidecar carries recipe + schema_version + salvage flag.
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "passthrough"
    assert meta["schema_version"] == "1.0"
    assert meta["salvaged"] is False
    assert meta["status"] == "success"
    assert meta["bytes"] == len(b"hello\n")


# ---------------------------------------------------------------------------
# 2 -- Unknown recipe name -> KeyError
# ---------------------------------------------------------------------------


def test_unknown_recipe_name_raises_keyerror(tmp_path):
    worker = _make_worker(tmp_path, 0)
    with pytest.raises(KeyError) as excinfo:
        normalize_wave2([worker], "no-such-recipe")
    assert "no-such-recipe" in str(excinfo.value)


# ---------------------------------------------------------------------------
# 3 -- Happy path: recipe applied, atomic write, meta sidecar
# ---------------------------------------------------------------------------


def test_happy_path_writes_final_and_meta(tmp_path, install_recipe):
    install_recipe("findings_table_v1", _EchoRecipe())
    worker = _make_worker(tmp_path, 1, body="finding-1\n")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == "success"
    final = Path(worker.final_path).read_text(encoding="utf-8")
    assert final == "# normalized\nfinding-1\n"

    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "findings_table_v1"
    assert meta["schema_version"] == "1.0"
    assert meta["salvaged"] is False
    assert meta["status"] == "success"
    assert meta["bytes"] == len(final.encode("utf-8"))
    assert "error" not in meta


def test_schema_version_override_is_recorded(tmp_path, install_recipe):
    install_recipe("findings_table_v1", _EchoRecipe())
    worker = _make_worker(tmp_path, 0, body="x")

    normalize_wave2(
        [worker],
        "findings_table_v1",
        schema_version="2.0",
    )
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["schema_version"] == "2.0"


def test_recipe_args_forwarded(tmp_path, install_recipe):
    captured: dict[str, Any] = {}

    class _CapturingRecipe:
        def normalize(self, raw_output, args):
            captured["raw"] = raw_output
            captured["args"] = dict(args)
            return NormalizedResult(text=raw_output)

    install_recipe("findings_table_v1", _CapturingRecipe())
    worker = _make_worker(tmp_path, 0, body="hello")

    normalize_wave2(
        [worker],
        "findings_table_v1",
        recipe_args={"cap": 4000, "lens": "bare-review"},
    )
    assert captured["raw"] == "hello"
    # FR-028: the dispatcher forwards recipe_args verbatim EXCEPT it
    # injects the per-worker ``status`` (here the default "success") into
    # a per-worker copy so the recipe's §7.4 salvage gate sees the real
    # upstream status. The original recipe_args dict is not mutated.
    assert captured["args"] == {
        "cap": 4000,
        "lens": "bare-review",
        "status": "success",
    }


# ---------------------------------------------------------------------------
# 4 -- Parse error branch: recipe raises -> status downgraded + error on meta
# ---------------------------------------------------------------------------


def test_recipe_exception_downgrades_to_parse_error(tmp_path, install_recipe):
    install_recipe("findings_table_v1", _RaisingRecipe())
    worker = _make_worker(tmp_path, 2, body="anything")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == "parse_error"
    # No final file written on recipe exception.
    assert not Path(worker.final_path).exists()
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["status"] == "parse_error"
    assert meta["salvaged"] is False
    assert "error" in meta
    assert "synthetic parse failure" in meta["error"]
    assert "ValueError" in meta["error"]


# ---------------------------------------------------------------------------
# 5 -- Hard-failure short-circuit: timeout / proxy_error skip normalization
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("hard_status", ["timeout", "proxy_error"])
def test_hard_failure_skips_normalize_but_emits_meta(
    tmp_path, install_recipe, hard_status
):
    install_recipe("findings_table_v1", _EchoRecipe())
    worker = _make_worker(tmp_path, 3, status=hard_status, body="")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == hard_status
    assert not Path(worker.final_path).exists()
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["status"] == hard_status
    assert meta["salvaged"] is False
    assert meta["recipe"] == "findings_table_v1"
    assert meta["bytes"] == 0


# ---------------------------------------------------------------------------
# 6 -- Salvage flag: parse_error worker with salvageable body -> success
# ---------------------------------------------------------------------------


def test_salvage_promotion_when_recipe_signals_recovery(tmp_path, install_recipe):
    install_recipe("findings_table_v1", _SalvagingRecipe())
    worker = _make_worker(tmp_path, 4, status="parse_error", body="messy")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == "success"
    assert Path(worker.final_path).read_text(encoding="utf-8") == "recovered:messy"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "success"


def test_salvage_flag_alone_does_not_promote_success_worker(tmp_path, install_recipe):
    """When the worker already arrived as success, salvaged stays a flag
    only -- status is not rewritten (no promotion needed)."""
    install_recipe("findings_table_v1", _SalvagingRecipe())
    worker = _make_worker(tmp_path, 5, status="success", body="ok")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert out.status == "success"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "success"


# ---------------------------------------------------------------------------
# 7 -- Input list is not mutated
# ---------------------------------------------------------------------------


def test_input_list_not_mutated(tmp_path, install_recipe):
    install_recipe("findings_table_v1", _EchoRecipe())
    workers = [_make_worker(tmp_path, i, body=f"body-{i}") for i in range(3)]
    snapshot = [(w.index, w.status, w.bytes) for w in workers]

    outs = normalize_wave2(workers, "findings_table_v1")

    # New list with same length, new dataclass instances.
    assert len(outs) == 3
    for original, returned in zip(workers, outs):
        assert original is not returned
    # Original worker dataclasses unchanged.
    assert [(w.index, w.status, w.bytes) for w in workers] == snapshot


# ---------------------------------------------------------------------------
# 8 -- Reads from in-memory ``body`` attribute when present
# ---------------------------------------------------------------------------


def test_in_memory_body_preferred_over_raw_path(tmp_path, install_recipe):
    install_recipe("findings_table_v1", _EchoRecipe())
    worker = _make_worker(tmp_path, 0, body="on-disk")
    # Stash an in-memory body the way StubTransport does.
    worker.body = "in-memory"  # type: ignore[attr-defined]

    normalize_wave2([worker], "findings_table_v1")

    assert (
        Path(worker.final_path).read_text(encoding="utf-8") == "# normalized\nin-memory"
    )


# ---------------------------------------------------------------------------
# 9 -- Atomic write contract: no .tmp left behind on success
# ---------------------------------------------------------------------------


def test_atomic_write_leaves_no_tmp_artifact(tmp_path, install_recipe):
    install_recipe("findings_table_v1", _EchoRecipe())
    worker = _make_worker(tmp_path, 0, body="x")

    normalize_wave2([worker], "findings_table_v1")

    leftover = list(tmp_path.glob("*.tmp"))
    assert leftover == [], f"unexpected tmp artifacts: {leftover}"


# ---------------------------------------------------------------------------
# 10 -- Non-conforming REGISTRY entry raises TypeError
# ---------------------------------------------------------------------------


def test_non_conforming_recipe_raises_typeerror(monkeypatch, tmp_path):
    monkeypatch.setitem(REGISTRY, "findings_table_v1", object())  # bare object
    worker = _make_worker(tmp_path, 0)
    with pytest.raises(TypeError):
        normalize_wave2([worker], "findings_table_v1")


# ---------------------------------------------------------------------------
# 11 -- Multiple workers: positional correspondence + independence
# ---------------------------------------------------------------------------


def test_multiple_workers_normalized_independently(tmp_path, install_recipe):
    install_recipe("findings_table_v1", _EchoRecipe())
    workers = [_make_worker(tmp_path, i, body=f"body-{i}") for i in range(4)]

    outs = normalize_wave2(workers, "findings_table_v1")

    for i, out in enumerate(outs):
        assert out.index == i
        assert out.status == "success"
        final = Path(workers[i].final_path).read_text(encoding="utf-8")
        assert final == f"# normalized\nbody-{i}"
        meta = json.loads(Path(workers[i].meta_path).read_text(encoding="utf-8"))
        assert meta["recipe"] == "findings_table_v1"
        assert meta["status"] == "success"


# ---------------------------------------------------------------------------
# 12 -- Module surface sanity
# ---------------------------------------------------------------------------


def test_module_exports():
    assert hasattr(normalize_mod, "normalize_wave2")
    assert hasattr(normalize_mod, "NormalizedResult")
    assert hasattr(normalize_mod, "Recipe")
