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
from typing import Any, Optional

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


# ===========================================================================
# Item 2.13 -- frozen characterization of the C07 atomic writers (G4) and
# the C09 recipe resolver / Wave-2 dispatcher (G2), pinned against the
# UNCHANGED production source. Every case below carries a stable case ID
# (the parametrize ``id``) and an expected-oracle literal. Failure seams
# are injected at the ``os`` / ``tempfile`` module attributes of the module
# that actually runs each facade's transaction (item 4.10: the facade
# module itself while it holds the original transaction, then
# ``superclaude.cli.swarm.atomic`` once the facade calls
# ``write_prepared_bytes``), at ``pathlib.Path.mkdir``, and through text
# that UTF-8 cannot encode (lone surrogate). Registry changes use
# ``monkeypatch.setitem`` so REGISTRY is restored on teardown.
# ===========================================================================

import dataclasses  # noqa: E402
import errno  # noqa: E402
import os  # noqa: E402
import tempfile  # noqa: E402

from superclaude.cli.swarm import atomic as atomic_mod  # noqa: E402
from superclaude.cli.swarm import preflight as preflight_mod  # noqa: E402
from superclaude.cli.swarm import reduce as reduce_mod  # noqa: E402
from superclaude.cli.swarm.models import Manifest  # noqa: E402

# ---------------------------------------------------------------------------
# G4 instrumentation -- proxies installed on the writer modules' own
# ``os`` / ``tempfile`` bindings; every real effect is delegated.
# ---------------------------------------------------------------------------


class _WriterSpy:
    """Records the writer's event sequence and raises planned failures."""

    def __init__(self, plan: dict[str, BaseException]) -> None:
        self.plan = plan
        self.events: list[tuple[Any, ...]] = []
        self.fds: list[int] = []
        self.tmp_names: list[str] = []

    def hit(self, step: str, *detail: Any) -> None:
        self.events.append((step, *detail))
        if step in self.plan:
            raise self.plan[step]

    def steps(self) -> tuple[str, ...]:
        return tuple(e[0] for e in self.events)


class _HandleProxy:
    def __init__(self, real: Any, spy: _WriterSpy) -> None:
        self._real = real
        self._spy = spy

    def __enter__(self) -> "_HandleProxy":
        return self

    def __exit__(self, *exc: Any) -> bool:
        self.close()
        return False

    def write(self, data: bytes) -> int:
        self._spy.hit("write", data if isinstance(data, str) else bytes(data))
        return self._real.write(data)

    def flush(self) -> None:
        self._spy.hit("flush")
        self._real.flush()

    def fileno(self) -> int:
        return self._real.fileno()

    def close(self) -> None:
        self._real.close()
        self._spy.hit("close")


class _OsProxy:
    def __init__(self, spy: _WriterSpy) -> None:
        self._spy = spy

    def __getattr__(self, name: str) -> Any:
        return getattr(os, name)

    def fdopen(self, fd: int, mode: str = "r", *args: Any, **kwargs: Any) -> Any:
        self._spy.hit("fdopen", mode)
        return _HandleProxy(os.fdopen(fd, mode, *args, **kwargs), self._spy)

    def fsync(self, fd: int) -> None:
        self._spy.hit("fsync")
        os.fsync(fd)

    def replace(self, src: str, dst: str) -> None:
        dst_before = Path(dst).read_bytes() if Path(dst).exists() else None
        self._spy.hit("replace", src, dst, Path(src).read_bytes(), dst_before)
        os.replace(src, dst)

    def unlink(self, path: str) -> None:
        self._spy.hit("unlink", path)
        os.unlink(path)


class _TempfileProxy:
    def __init__(self, spy: _WriterSpy) -> None:
        self._spy = spy

    def __getattr__(self, name: str) -> Any:
        return getattr(tempfile, name)

    def mkstemp(self, **kwargs: Any) -> tuple[int, str]:
        self._spy.hit(
            "mkstemp", kwargs.get("prefix"), kwargs.get("suffix"), kwargs.get("dir")
        )
        fd, name = tempfile.mkstemp(**kwargs)
        self._spy.fds.append(fd)
        self._spy.tmp_names.append(name)
        return fd, name


# Writer under test -> (facade module, facade name, payload preparation).
# The bytes writer's callers encode.
_WRITERS: dict[str, tuple[Any, str, Any]] = {
    "text": (normalize_mod, "_atomic_write_text", lambda s: s),
    "bytes": (reduce_mod, "_atomic_write_bytes", lambda s: s.encode("utf-8")),
}


def _transaction_module(facade_module: Any) -> Any:
    """Return the module whose ``os``/``tempfile`` run the facade's transaction.

    A facade switched to the shared leaf holds the global
    ``write_prepared_bytes`` (it must be the atomic leaf's function), so the
    syscalls happen in ``superclaude.cli.swarm.atomic``. An unswitched facade
    still runs the original transaction on its own module bindings.
    """
    shared = getattr(facade_module, "write_prepared_bytes", None)
    if shared is not None:
        assert shared is atomic_mod.write_prepared_bytes
        return atomic_mod
    assert hasattr(facade_module, "os") and hasattr(facade_module, "tempfile")
    return facade_module


@pytest.fixture
def writer_spy(monkeypatch):
    """Install a spy on the seams one writer actually reaches; return
    (spy, write)."""

    def _install(kind: str, plan: Optional[dict[str, BaseException]] = None):
        spy = _WriterSpy(plan or {})
        module, facade, prepare = _WRITERS[kind]
        target = _transaction_module(module)
        monkeypatch.setattr(target, "os", _OsProxy(spy))
        monkeypatch.setattr(target, "tempfile", _TempfileProxy(spy))
        real_mkdir = Path.mkdir

        def _mkdir(self, *args: Any, **kwargs: Any) -> None:
            spy.hit("mkdir", str(self), kwargs.get("parents"), kwargs.get("exist_ok"))
            return real_mkdir(self, *args, **kwargs)

        monkeypatch.setattr(Path, "mkdir", _mkdir)
        writer = getattr(module, facade)
        return spy, (lambda path, payload: writer(path, prepare(payload)))

    return _install


def _close_leaked_fds(spy: _WriterSpy) -> list[int]:
    """Close any mkstemp fd the writer left open; return those that were."""
    leaked = []
    for fd in spy.fds:
        try:
            os.close(fd)
            leaked.append(fd)
        except OSError:
            pass
    return leaked


# Exact success event order (oracle literal), shared by both writers.
G4_SUCCESS_STEPS = (
    "mkdir",
    "mkstemp",
    "fdopen",
    "write",
    "flush",
    "fsync",
    "close",
    "replace",
)

# G4.1-G4.6 frozen success cases:
# (case_id, parent_pre_exists, initial_dest, payloads, expected_returns,
#  expected_final_bytes)
G4_SUCCESS_CASES = [
    ("G4.1-empty-payload", False, None, ("",), (0,), b""),
    ("G4.2-ascii-a", False, None, ("a",), (1,), b"a"),
    ("G4.3-unicode-e-acute", False, None, ("é",), (2,), b"\xc3\xa9"),
    ("G4.4-repeated-whole-writes", False, None, ("A", "BB"), (1, 2), b"BB"),
    ("G4.5-old-destination-replaced", True, b"prior", ("next",), (4,), b"next"),
    ("G4.6-absent-destination-valid-parent", True, None, ("new",), (3,), b"new"),
]


@pytest.mark.parametrize("kind", ["text", "bytes"])
@pytest.mark.parametrize(
    "case_id,parent_exists,initial,payloads,returns,final",
    G4_SUCCESS_CASES,
    ids=[c[0] for c in G4_SUCCESS_CASES],
)
def test_g4_writer_success_matrix(
    tmp_path,
    writer_spy,
    kind,
    case_id,
    parent_exists,
    initial,
    payloads,
    returns,
    final,
):
    parent = tmp_path / "out"
    dest = parent / "dest.md"
    if parent_exists:
        parent.mkdir()
    if initial is not None:
        dest.write_bytes(initial)
    spy, write = writer_spy(kind)

    observed_returns = []
    prior: Optional[bytes] = initial
    for payload in payloads:
        start = len(spy.events)
        observed_returns.append(write(dest, payload))
        events = spy.events[start:]
        encoded = payload.encode("utf-8")
        # Exact order: one mkdir, same-parent unique temp, binary open,
        # single whole write, flush, fsync, close, then replace.
        assert tuple(e[0] for e in events) == G4_SUCCESS_STEPS
        assert events[0][1:] == (str(parent), True, True)
        assert events[1][1:] == ("dest.md.", ".tmp", str(parent))
        assert events[2][1:] == ("wb",)
        assert events[3][1:] == (encoded,)
        tmp_src, tmp_dst, tmp_bytes_at_replace, dest_before = events[7][1:]
        assert Path(tmp_src).parent == parent
        assert Path(tmp_src).name.startswith("dest.md.")
        assert tmp_src.endswith(".tmp")
        assert tmp_dst == str(dest)
        # Temp holds the complete payload; the live file is still the
        # prior version (or absent) until the replace.
        assert tmp_bytes_at_replace == encoded
        assert dest_before == prior
        prior = encoded

    assert tuple(observed_returns) == returns
    assert dest.read_bytes() == final
    assert sorted(p.name for p in parent.iterdir()) == ["dest.md"]
    assert len(set(spy.tmp_names)) == len(payloads)  # unique temp per write
    assert "unlink" not in spy.steps()


# G4.7 / G4.9-G4.17 frozen failure cases:
# (case_id, injected step(s) -> exception factory, expected exact steps,
#  raised step, temp sibling remains)
G4_FAILURE_CASES = [
    (
        "G4.7-mkdir-PermissionError",
        {"mkdir": lambda: PermissionError(errno.EACCES, "mkdir denied")},
        ("mkdir",),
        "mkdir",
        False,
    ),
    (
        "G4.9-mkstemp-ENOSPC",
        {"mkstemp": lambda: OSError(errno.ENOSPC, "no space")},
        ("mkdir", "mkstemp"),
        "mkstemp",
        False,
    ),
    (
        "G4.10-fdopen-raises",
        {"fdopen": lambda: OSError(errno.EBADF, "fdopen failed")},
        ("mkdir", "mkstemp", "fdopen", "unlink"),
        "fdopen",
        False,
    ),
    (
        "G4.11-write-raises",
        {"write": lambda: RuntimeError("write failed")},
        ("mkdir", "mkstemp", "fdopen", "write", "close", "unlink"),
        "write",
        False,
    ),
    (
        "G4.12-flush-raises",
        {"flush": lambda: OSError(errno.EIO, "flush failed")},
        ("mkdir", "mkstemp", "fdopen", "write", "flush", "close", "unlink"),
        "flush",
        False,
    ),
    (
        "G4.13-fsync-raises",
        {"fsync": lambda: OSError(errno.EIO, "fsync failed")},
        ("mkdir", "mkstemp", "fdopen", "write", "flush", "fsync", "close", "unlink"),
        "fsync",
        False,
    ),
    (
        "G4.14-close-raises",
        {"close": lambda: OSError(errno.EIO, "close failed")},
        ("mkdir", "mkstemp", "fdopen", "write", "flush", "fsync", "close", "unlink"),
        "close",
        False,
    ),
    (
        "G4.15-replace-raises",
        {"replace": lambda: OSError(errno.EXDEV, "replace failed")},
        G4_SUCCESS_STEPS + ("unlink",),
        "replace",
        False,
    ),
    (
        "G4.16-replace-and-unlink-raise",
        {
            "replace": lambda: OSError(errno.EXDEV, "replace failed"),
            "unlink": lambda: OSError(errno.EACCES, "unlink failed"),
        },
        G4_SUCCESS_STEPS + ("unlink",),
        "replace",
        True,
    ),
    (
        "G4.17-KeyboardInterrupt-at-write",
        {"write": lambda: KeyboardInterrupt()},
        ("mkdir", "mkstemp", "fdopen", "write", "close"),
        "write",
        True,
    ),
    (
        "G4.17-SystemExit-at-replace",
        {"replace": lambda: SystemExit(3)},
        G4_SUCCESS_STEPS,
        "replace",
        True,
    ),
]


@pytest.mark.parametrize("dest_state", ["absent", "old"])
@pytest.mark.parametrize("kind", ["text", "bytes"])
@pytest.mark.parametrize(
    "case_id,plan_factories,steps,raised_step,temp_remains",
    G4_FAILURE_CASES,
    ids=[c[0] for c in G4_FAILURE_CASES],
)
def test_g4_writer_failure_matrix(
    tmp_path,
    writer_spy,
    kind,
    dest_state,
    case_id,
    plan_factories,
    steps,
    raised_step,
    temp_remains,
):
    parent = tmp_path / "out"
    dest = parent / "dest.md"
    if dest_state == "old":
        parent.mkdir()
        dest.write_bytes(b"prior")
    plan = {step: factory() for step, factory in plan_factories.items()}
    spy, write = writer_spy(kind, plan)

    with pytest.raises(BaseException) as excinfo:
        write(dest, "payload-é")
    leaked = _close_leaked_fds(spy)

    # Original exception object propagates (never a cleanup error, never a
    # byte count); the exact event sequence is pinned.
    assert excinfo.value is plan[raised_step]
    assert spy.steps() == steps
    assert spy.steps().count("mkdir") == 1
    # Old destination unchanged / absent destination still absent.
    if dest_state == "old":
        assert dest.read_bytes() == b"prior"
    else:
        assert not dest.exists()
    leftovers = sorted(p.name for p in parent.iterdir()) if parent.exists() else []
    expected_live = ["dest.md"] if dest_state == "old" else []
    temps = [n for n in leftovers if n not in expected_live]
    if temp_remains:
        # Orphan allowance: unlink suppressed (G4.16) or never attempted for
        # a non-Exception BaseException (G4.17) -- the temp sibling remains.
        assert temps == [Path(spy.tmp_names[0]).name]
    else:
        assert temps == []
    if raised_step == "mkdir":
        assert parent.exists() is (dest_state == "old")
        assert spy.tmp_names == []
    if raised_step == "mkstemp":
        assert spy.tmp_names == []
    # fdopen failure leaves the raw mkstemp fd open (known, unrepaired
    # limit); every other path closes it.
    assert leaked == (spy.fds if raised_step == "fdopen" else [])


@pytest.mark.parametrize(
    "case_id,parent_exists",
    [("G4.8-surrogate-new-parent", False), ("G4.8-surrogate-existing-parent", True)],
)
def test_g4_8_text_mkdir_precedes_encode_failure(
    tmp_path, writer_spy, case_id, parent_exists
):
    parent = tmp_path / "out"
    if parent_exists:
        parent.mkdir()
    dest = parent / "dest.md"
    spy, write = writer_spy("text")

    with pytest.raises(UnicodeEncodeError):
        write(dest, "ok\ud800")

    # Exactly one mkdir ran BEFORE the encode failure; nothing after it.
    assert spy.steps() == ("mkdir",)
    assert parent.is_dir()
    assert list(parent.iterdir()) == []


def test_g4_7_text_mkdir_error_wins_over_malformed_text(tmp_path, writer_spy):
    denied = PermissionError(errno.EACCES, "mkdir denied")
    spy, write = writer_spy("text", {"mkdir": denied})
    dest = tmp_path / "out" / "dest.md"

    with pytest.raises(PermissionError) as excinfo:
        write(dest, "bad\ud800")

    assert excinfo.value is denied
    assert spy.steps() == ("mkdir",)
    assert not dest.parent.exists()


def test_g4_18_writers_apply_no_path_policy(tmp_path, writer_spy):
    """The C07 writers add no confinement: a symlinked parent is followed.
    Any rejection therefore stays at the caller level (path construction /
    state/preflight/logging confine_path), which this file does not own."""
    root = tmp_path / "root"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (root / "link").symlink_to(outside, target_is_directory=True)
    for kind, name in (("text", "t.md"), ("bytes", "b.md")):
        spy, write = writer_spy(kind)
        assert write(root / "link" / name, "x") == 1
        assert (outside / name).read_bytes() == b"x"


# ---------------------------------------------------------------------------
# G4.19 / G4.20 -- dispatcher body/meta emission gates (facade-call spy).
# ---------------------------------------------------------------------------


@pytest.fixture
def text_writer_calls(monkeypatch):
    calls: list[tuple[str, str]] = []
    real = normalize_mod._atomic_write_text

    def _spy(path: Path, content: str) -> int:
        calls.append((str(path), content))
        return real(path, content)

    monkeypatch.setattr(normalize_mod, "_atomic_write_text", _spy)
    return calls


# (case_id, recipe text, drop final_path, drop meta_path, expected writes
#  as ('final'|'meta') labels, expected out.bytes)
G4_EMISSION_GATE_CASES = [
    ("G4.19-empty-text-no-body", "", False, False, ("meta",), 0),
    ("G4.19-final-path-absent", "body", True, False, ("meta",), 0),
    ("G4.20-meta-path-none", "body", False, True, ("final",), 4),
    ("G4.20-meta-path-present", "body", False, False, ("final", "meta"), 4),
]


@pytest.mark.parametrize(
    "case_id,text,drop_final,drop_meta,writes,out_bytes",
    G4_EMISSION_GATE_CASES,
    ids=[c[0] for c in G4_EMISSION_GATE_CASES],
)
def test_g4_dispatcher_emission_gates(
    tmp_path,
    install_recipe,
    text_writer_calls,
    case_id,
    text,
    drop_final,
    drop_meta,
    writes,
    out_bytes,
):
    class _Fixed:
        def normalize(self, raw_output, args):
            return NormalizedResult(text=text, salvaged=False)

    install_recipe("g4-gate", _Fixed())
    base = _make_worker(tmp_path, 0, body="raw")
    worker = dataclasses.replace(
        base,
        final_path=None if drop_final else base.final_path,
        meta_path=None if drop_meta else base.meta_path,
    )
    [out] = normalize_wave2([worker], "g4-gate")

    labels = {base.final_path: "final", base.meta_path: "meta"}
    assert tuple(labels[p] for p, _ in text_writer_calls) == writes
    assert out.bytes == out_bytes
    assert out.status == "success"
    assert Path(base.final_path).exists() is ("final" in writes)
    assert Path(base.meta_path).exists() is ("meta" in writes)
    if "meta" in writes:
        meta = json.loads(Path(base.meta_path).read_text(encoding="utf-8"))
        assert meta == {
            "bytes": out_bytes,
            "recipe": "g4-gate",
            "salvage_reason": "rejected_not_parse_error",
            "salvaged": False,
            "schema_version": "1.0",
            "status": "success",
        }


def test_c07_normalize_body_and_meta_use_retained_text_facade(
    tmp_path, install_recipe, text_writer_calls, writer_spy
):
    """Real ``normalize_wave2`` writes body then meta through the retained
    ``normalize._atomic_write_text`` facade, and each facade call reaches the
    real transaction (one full syscall sequence per call, same bytes)."""
    install_recipe("findings_table_v1", _EchoRecipe())
    worker = _make_worker(tmp_path, 1, body="finding-é\n")
    spy, _ = writer_spy("text")

    [out] = normalize_wave2([worker], "findings_table_v1")

    assert [p for p, _ in text_writer_calls] == [worker.final_path, worker.meta_path]
    body_text, meta_text = (c for _, c in text_writer_calls)
    assert body_text == "# normalized\nfinding-é\n"
    assert out.bytes == len(body_text.encode("utf-8"))
    assert spy.steps() == G4_SUCCESS_STEPS * 2
    writes = [e[1] for e in spy.events if e[0] == "write"]
    assert writes == [body_text.encode("utf-8"), meta_text.encode("utf-8")]
    assert Path(worker.final_path).read_bytes() == writes[0]
    assert Path(worker.meta_path).read_bytes() == writes[1]


# ---------------------------------------------------------------------------
# G4.21 -- reduce merged / contract / done-sentinel gates (bytes-facade spy).
# ---------------------------------------------------------------------------


@pytest.fixture
def bytes_writer_calls(monkeypatch):
    calls: list[tuple[str, bytes]] = []
    real = reduce_mod._atomic_write_bytes

    def _spy(path: Path, data: bytes) -> int:
        calls.append((Path(path).name, data))
        return real(path, data)

    monkeypatch.setattr(reduce_mod, "_atomic_write_bytes", _spy)
    return calls


def _reduce_worker(index: int, status: str = "success") -> WorkerResult:
    return WorkerResult(
        index=index,
        path=f"w-{index}.md",
        raw_path=f"w-{index}.raw.md",
        meta_path=f"w-{index}.meta.json",
        final_path=f"w-{index}.final.md",
        model_id=f"m-{index}",
        model_label="stub",
        bytes=0,
        status=status,  # type: ignore[arg-type]
        attempts=1,
        elapsed_ms=1,
    )


# (case_id, mode, successes, emit_to_disk, expected written file names)
G4_REDUCE_GATE_CASES = [
    (
        "G4.21-merge-at-floor",
        "normalize+merge",
        2,
        None,
        ("merged.md", "return-contract.yaml"),
    ),
    ("G4.21-merge-below-floor", "normalize+merge", 1, None, ("return-contract.yaml",)),
    ("G4.21-raw-contract-only", "raw", 2, None, ("return-contract.yaml",)),
    ("G4.21-normalize-contract-only", "normalize", 2, None, ("return-contract.yaml",)),
    ("G4.21-emit-suppressed", "normalize+merge", 2, False, ()),
]


@pytest.mark.parametrize(
    "case_id,mode,successes,emit,written",
    G4_REDUCE_GATE_CASES,
    ids=[c[0] for c in G4_REDUCE_GATE_CASES],
)
def test_g4_21_reduce_emission_gates(
    tmp_path, bytes_writer_calls, case_id, mode, successes, emit, written
):
    workers = [
        _reduce_worker(i, "success" if i < successes else "timeout") for i in range(3)
    ]
    contract = reduce_mod.reduce_wave3(
        workers,
        mode=mode,
        output_dir=tmp_path,
        merge_callable=lambda ws: "MERGED-é",
        emit_to_disk=emit,
    )
    assert tuple(name for name, _ in bytes_writer_calls) == written
    assert sorted(p.name for p in tmp_path.iterdir()) == sorted(written)
    if "merged.md" in written:
        assert (tmp_path / "merged.md").read_bytes() == "MERGED-é".encode("utf-8")
        assert contract.merged_path == str(tmp_path / "merged.md")
    else:
        assert contract.merged_path is None


def test_g4_21_done_sentinel_rejects_before_write(tmp_path, writer_spy):
    spy, _ = writer_spy("bytes")
    contract_path = tmp_path / "return-contract.yaml"
    with pytest.raises(ValueError):
        reduce_mod.emit_done_sentinel("killed", contract_path)  # type: ignore[arg-type]
    assert spy.events == []
    assert list(tmp_path.iterdir()) == []

    target = reduce_mod.emit_done_sentinel("success", contract_path)
    assert target == tmp_path / "done.json"
    assert target.read_bytes() == (
        json.dumps(
            {
                "atomic_write": True,
                "contract_path": str(contract_path),
                "terminal_status": "success",
            },
            sort_keys=True,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")
    assert spy.steps() == G4_SUCCESS_STEPS


# ---------------------------------------------------------------------------
# G4.22 -- preflight's similar writer is independent and keeps its own policy.
# ---------------------------------------------------------------------------


def test_g4_22_preflight_writer_independent_of_c07_seams(tmp_path, monkeypatch):

    class _Failing:
        def __getattr__(self, name):
            raise AssertionError(f"C07 seam used by preflight: {name}")

    for facade_module in (normalize_mod, reduce_mod):
        target = _transaction_module(facade_module)
        monkeypatch.setattr(target, "os", _Failing())
        monkeypatch.setattr(target, "tempfile", _Failing())
    written = preflight_mod.write_manifest(Manifest(), tmp_path)
    assert Path(written) == (tmp_path / "manifest.json").resolve()


def test_g4_22_preflight_cleanup_policy_differs(tmp_path, monkeypatch):
    """preflight suppresses only FileNotFoundError on unlink, so a
    PermissionError from cleanup escapes (unlike C07, G4.16)."""
    primary = OSError(errno.EXDEV, "replace failed")
    cleanup = PermissionError(errno.EACCES, "unlink failed")
    spy = _WriterSpy({"replace": primary, "unlink": cleanup})
    monkeypatch.setattr(preflight_mod, "os", _OsProxy(spy))

    with pytest.raises(PermissionError) as excinfo:
        preflight_mod.write_manifest(Manifest(), tmp_path)
    assert excinfo.value is cleanup
    assert excinfo.value.__context__ is primary
    leftovers = [p.name for p in tmp_path.iterdir()]
    assert len(leftovers) == 1 and leftovers[0].startswith(".manifest-")


# ---------------------------------------------------------------------------
# G2 -- recipe resolution and dispatcher gates through existing interfaces.
# ---------------------------------------------------------------------------

_G2_SLOT = "g2-slot"
_ABSENT = object()
_KNOWN = (
    "['bare-review-v1', 'custom', 'findings_table_v1', "
    "'hypothesis_table_v1', 'passthrough', 'verdict_only_v1']"
)
_TYPE_MSG = (
    "recipe 'g2-slot' (type {t}) does not implement Recipe Protocol "
    "(normalize(raw_output, args) -> NormalizedResult)"
)


def _registry_identity() -> dict[str, int]:
    return {k: id(v) for k, v in REGISTRY.items()}


# (case_id, slot value or _ABSENT, looked-up name, exception, exact message)
G2_RESOLUTION_ERROR_CASES = [
    (
        "G2.1-empty-name-absent",
        _ABSENT,
        "",
        KeyError,
        f"recipe '' not registered in recipes.REGISTRY; known: {_KNOWN}",
    ),
    ("G2.4-int-10e100", 10**100, _G2_SLOT, TypeError, _TYPE_MSG.format(t="int")),
    (
        "G2.7-absent-name",
        _ABSENT,
        _G2_SLOT,
        KeyError,
        f"recipe 'g2-slot' not registered in recipes.REGISTRY; known: {_KNOWN}",
    ),
    ("G2.7-falsey-zero", 0, _G2_SLOT, TypeError, _TYPE_MSG.format(t="int")),
    ("G2.7-falsey-False", False, _G2_SLOT, TypeError, _TYPE_MSG.format(t="bool")),
    ("G2.7-falsey-empty-str", "", _G2_SLOT, TypeError, _TYPE_MSG.format(t="str")),
    ("G2.7-falsey-empty-list", [], _G2_SLOT, TypeError, _TYPE_MSG.format(t="list")),
]


@pytest.mark.parametrize("n_workers", [0, 1], ids=["G2.10-empty-list", "one-worker"])
@pytest.mark.parametrize(
    "case_id,slot_value,name,exc_type,message",
    G2_RESOLUTION_ERROR_CASES,
    ids=[c[0] for c in G2_RESOLUTION_ERROR_CASES],
)
def test_g2_resolution_errors(
    tmp_path, monkeypatch, n_workers, case_id, slot_value, name, exc_type, message
):
    if slot_value is not _ABSENT:
        monkeypatch.setitem(REGISTRY, _G2_SLOT, slot_value)
    before = _registry_identity()
    workers = [_make_worker(tmp_path, 0)] if n_workers else []

    with pytest.raises(exc_type) as excinfo:
        normalize_wave2(workers, name)

    # Resolution precedes the per-worker map: errors fire even for [].
    assert type(excinfo.value) is exc_type
    assert excinfo.value.args == (message,)
    assert _registry_identity() == before
    assert sorted(p.name for p in tmp_path.iterdir()) == (
        ["worker-00.raw.txt"] if n_workers else []
    )


def test_g2_3_valid_recipe_identity_is_returned_and_invoked(tmp_path, install_recipe):
    calls: list[str] = []

    class _Spy:
        def normalize(self, raw_output, args):
            calls.append(raw_output)
            return NormalizedResult(text=f"spy:{raw_output}", salvaged=False)

    recipe = _Spy()
    install_recipe(_G2_SLOT, recipe)
    before = _registry_identity()

    assert normalize_mod._resolve_recipe(_G2_SLOT) is recipe
    [out] = normalize_wave2([_make_worker(tmp_path, 0, body="r")], _G2_SLOT)

    assert calls == ["r"]
    assert out.status == "success"
    assert Path(out.final_path).read_text(encoding="utf-8") == "spy:r"
    assert REGISTRY[_G2_SLOT] is recipe
    assert _registry_identity() == before


def test_g2_none_slot_resolves_fresh_passthrough_without_registry_change(
    install_recipe,
):
    install_recipe(_G2_SLOT, None)  # type: ignore[arg-type]
    before = _registry_identity()
    first = normalize_mod._resolve_recipe(_G2_SLOT)
    second = normalize_mod._resolve_recipe(_G2_SLOT)
    assert first is not second
    assert isinstance(first, Recipe)
    assert first is not REGISTRY["passthrough"]
    result = first.normalize(" é\n  ", {"status": "success"})
    assert (result.text, result.salvaged, result.error) == (" é\n  ", False, None)
    assert REGISTRY[_G2_SLOT] is None
    assert _registry_identity() == before


def test_g2_8_none_slot_independent_of_named_passthrough(tmp_path, monkeypatch):
    invalid = object()
    monkeypatch.setitem(REGISTRY, "passthrough", invalid)
    monkeypatch.setitem(REGISTRY, _G2_SLOT, None)
    before = _registry_identity()

    [out] = normalize_wave2([_make_worker(tmp_path, 0, body="raw\n")], _G2_SLOT)
    assert out.status == "success"
    assert Path(out.final_path).read_text(encoding="utf-8") == "raw\n"
    assert REGISTRY["passthrough"] is invalid
    assert REGISTRY[_G2_SLOT] is None
    assert _registry_identity() == before

    with pytest.raises(TypeError) as excinfo:
        normalize_wave2([_make_worker(tmp_path, 1)], "passthrough")
    assert excinfo.value.args == (
        "recipe 'passthrough' (type object) does not implement Recipe Protocol "
        "(normalize(raw_output, args) -> NormalizedResult)",
    )


def test_g2_10_empty_worker_list_valid_recipe(tmp_path, install_recipe):
    install_recipe(_G2_SLOT, None)  # type: ignore[arg-type]
    assert normalize_wave2([], _G2_SLOT) == []
    assert normalize_wave2([], "passthrough") == []
    assert list(tmp_path.iterdir()) == []


class _CountingRecipe:
    def __init__(self, fn) -> None:
        self.fn = fn
        self.calls: list[str] = []

    def normalize(self, raw_output, args):
        self.calls.append(raw_output)
        return self.fn(raw_output)


def _raise_parse(raw: str) -> NormalizedResult:
    raise ValueError("synthetic parse failure")


_G2_RECIPES = {
    "none": None,
    "echo": lambda raw: NormalizedResult(text=raw, salvaged=False),
    "salvage": lambda raw: NormalizedResult(text=f"recovered:{raw}", salvaged=True),
    "salvage-empty": lambda raw: NormalizedResult(text="", salvaged=True),
    "raise": _raise_parse,
}


def _meta(status, bytes_, salvaged=False, reason=None, error=None):
    out = {
        "bytes": bytes_,
        "recipe": _G2_SLOT,
        "salvaged": salvaged,
        "schema_version": "1.0",
        "status": status,
    }
    if reason is not None:
        out["salvage_reason"] = reason
    if error is not None:
        out["error"] = error
    return out


# (case_id, recipe key, worker status, raw body, salvage_enabled,
#  expected out.status, expected out.bytes, expected final text or None,
#  expected exact meta, expected recipe call count (None = None slot))
G2_DISPATCH_CASES = [
    (
        "G2.2-none-slot-a",
        "none",
        "success",
        "a",
        True,
        "success",
        1,
        "a",
        _meta("success", 1, reason="rejected_not_parse_error"),
        None,
    ),
    (
        "G2.5-none-slot-empty",
        "none",
        "success",
        "",
        True,
        "success",
        0,
        None,
        _meta("success", 0, reason="rejected_not_parse_error"),
        None,
    ),
    (
        "G2.6-none-slot-unicode-whitespace",
        "none",
        "success",
        " é\n  ",
        True,
        "success",
        6,
        " é\n  ",
        _meta("success", 6, reason="rejected_not_parse_error"),
        None,
    ),
    (
        "G2.9-none-slot-parse-error",
        "none",
        "parse_error",
        "garbage\n",
        True,
        "parse_error",
        8,
        "garbage\n",
        _meta("parse_error", 8, reason="rejected_no_recipe_signal"),
        None,
    ),
    (
        "G2.11-hard-timeout",
        "echo",
        "timeout",
        "partial",
        True,
        "timeout",
        7,
        None,
        _meta("timeout", 0),
        0,
    ),
    (
        "G2.11-hard-proxy-error",
        "echo",
        "proxy_error",
        "partial",
        True,
        "proxy_error",
        7,
        None,
        _meta("proxy_error", 0),
        0,
    ),
    (
        "G2.12-recipe-raises-salvage-on",
        "raise",
        "success",
        "anything",
        True,
        "parse_error",
        0,
        None,
        _meta(
            "parse_error",
            0,
            reason="rejected_no_recipe_signal",
            error="ValueError: synthetic parse failure",
        ),
        1,
    ),
    (
        "G2.12-recipe-raises-salvage-off",
        "raise",
        "success",
        "anything",
        False,
        "parse_error",
        0,
        None,
        _meta(
            "parse_error",
            0,
            reason="rejected_salvage_disabled",
            error="ValueError: synthetic parse failure",
        ),
        1,
    ),
    (
        "G2.13-salvage-disabled",
        "salvage",
        "parse_error",
        "messy",
        False,
        "parse_error",
        15,
        "recovered:messy",
        _meta("parse_error", 15, salvaged=True, reason="rejected_salvage_disabled"),
        1,
    ),
    (
        "G2.14a-no-recipe-signal",
        "echo",
        "parse_error",
        "messy",
        True,
        "parse_error",
        5,
        "messy",
        _meta("parse_error", 5, reason="rejected_no_recipe_signal"),
        1,
    ),
    (
        "G2.14b-salvaged-empty-text",
        "salvage-empty",
        "parse_error",
        "messy",
        True,
        "parse_error",
        0,
        None,
        _meta("parse_error", 0, salvaged=True, reason="rejected_empty_text"),
        1,
    ),
    (
        "G2.15-promoted",
        "salvage",
        "parse_error",
        "messy",
        True,
        "success",
        15,
        "recovered:messy",
        _meta("success", 15, salvaged=True, reason="promoted_recipe_signal"),
        1,
    ),
    (
        "G2.16-success-worker-salvaging-recipe",
        "salvage",
        "success",
        "ok",
        True,
        "success",
        12,
        "recovered:ok",
        _meta("success", 12, salvaged=True, reason="rejected_not_parse_error"),
        1,
    ),
]


@pytest.mark.parametrize(
    "case_id,recipe_key,status,body,salvage_enabled,exp_status,exp_bytes,"
    "exp_final,exp_meta,exp_calls",
    G2_DISPATCH_CASES,
    ids=[c[0] for c in G2_DISPATCH_CASES],
)
def test_g2_dispatch_matrix(
    tmp_path,
    monkeypatch,
    case_id,
    recipe_key,
    status,
    body,
    salvage_enabled,
    exp_status,
    exp_bytes,
    exp_final,
    exp_meta,
    exp_calls,
):
    fn = _G2_RECIPES[recipe_key]
    recipe = None if fn is None else _CountingRecipe(fn)
    monkeypatch.setitem(REGISTRY, _G2_SLOT, recipe)
    before = _registry_identity()
    worker = _make_worker(tmp_path, 0, status=status, body=body)
    snapshot = dataclasses.asdict(worker)

    [out] = normalize_wave2([worker], _G2_SLOT, salvage_enabled=salvage_enabled)

    assert out is not worker
    assert dataclasses.asdict(worker) == snapshot
    assert (out.status, out.bytes) == (exp_status, exp_bytes)
    final = Path(worker.final_path)
    if exp_final is None:
        assert not final.exists()
    else:
        assert final.read_bytes() == exp_final.encode("utf-8")
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta == exp_meta
    if exp_calls is not None:
        assert len(recipe.calls) == exp_calls
    assert REGISTRY[_G2_SLOT] is recipe
    assert _registry_identity() == before


def test_g2_none_slot_cardinality_order_and_immutability(tmp_path, install_recipe):
    install_recipe(_G2_SLOT, None)  # type: ignore[arg-type]
    statuses = ["success", "timeout", "parse_error"]
    workers = [
        _make_worker(tmp_path, i, status=s, body=f"b{i}")
        for i, s in enumerate(statuses)
    ]
    snapshot = [dataclasses.asdict(w) for w in workers]
    recipe_args = {"k": 1}

    outs = normalize_wave2(list(workers), _G2_SLOT, recipe_args=recipe_args)

    assert [o.index for o in outs] == [0, 1, 2]
    assert [o.status for o in outs] == statuses
    assert [o.bytes for o in outs] == [2, 2, 2]
    assert all(o is not w for o, w in zip(outs, workers))
    assert [dataclasses.asdict(w) for w in workers] == snapshot
    assert recipe_args == {"k": 1}
    assert not Path(workers[1].final_path).exists()
