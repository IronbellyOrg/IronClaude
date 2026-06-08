"""T03.19 -- NFR-014 / AC-015 no-cross-invocation response caching guard.

Enforces the spec rule that every ``swarm run`` invocation MUST
re-dispatch its workers against the live transport. The dispatch
layer is forbidden from carrying a cross-invocation response cache:
two identical inputs run back-to-back must hit the transport twice,
not once, so the caller sees the actual current upstream behaviour
(timeouts, retries, 5xx flapping) instead of a stale snapshot.

Why a structural guard
======================

This is a property that disappears the instant a well-meaning
contributor wraps :func:`dispatch_wave1` or a transport ``send`` in
``functools.lru_cache`` / ``cachetools.cached`` / ``requests_cache``
to "save tokens" on a re-run. None of those decorators leave a
runtime symptom that an ad-hoc test would catch -- the second call
just silently returns the cached body and the test still passes. So
this file pairs two independent detectors:

1. **Static AST audit** -- walks every ``.py`` source under
   ``src/superclaude/cli/swarm/`` and flags any forbidden cache
   import (whole-module or symbol-level), and any attribute-chain
   reference to a forbidden cache callable. The AST visitor matches
   the same shape as ``test_concurrency_python_only.py`` so the two
   guards reinforce each other.
2. **Live integration probe** -- runs :func:`dispatch_wave1` twice
   with byte-identical inputs against a call-counting transport and
   asserts the transport was invoked the full ``2 * N`` times. A
   regression that introduced a memoizing wrapper around dispatch
   would collapse the second invocation's call count to ``N`` (or
   ``0`` for a per-prompt cache) and trip this assertion.

Forbidden-cache surface
=======================

The audit targets the ecosystem's mainstream response-cache layers:

* ``functools.lru_cache`` / ``functools.cache`` (stdlib decorators).
  ``functools`` itself is fine -- ``functools.partial`` etc are
  unrelated; only the two cache symbols are flagged.
* ``cachetools.*`` (third-party in-memory cache, including
  ``cached`` / ``cachedmethod`` / ``func.lru_cache`` / ``func.ttl_cache``).
* ``requests_cache`` (HTTP response cache layered on requests; would
  cache transport responses across invocations).
* ``aiocache.*`` / ``diskcache.*`` (async + on-disk variants -- same
  category, listed so the audit doesn't shift from "blanket ban" to
  "lru_cache-only ban" if a future contributor swaps libraries).

The deliberate exclusion is ``functools.cached_property`` -- that
caches an attribute on an instance for the instance's lifetime
(intra-invocation), which is orthogonal to the cross-invocation
response-cache rule. Including it would create false positives the
moment someone uses it for a per-job derived value.

Mutation guarantee
==================

A regression that silently broke the AST visitor or the call-count
assertion would make the green-suite outcome meaningless. The
``test_audit_detects_*`` mutation tests prove the detectors actually
flag synthetic offending sources for each forbidden construct, and
``test_call_counting_transport_increments_per_call`` proves the
integration probe's counter actually advances per ``send`` call.
"""

from __future__ import annotations

import ast
import threading
from pathlib import Path

import pytest

from superclaude.cli.swarm.dispatch import dispatch_wave1
from superclaude.cli.swarm.models import (
    Manifest,
    PreflightSummary,
    SwarmState,
    WorkerResult,
)
from superclaude.cli.swarm.preflight import PreflightResult


REPO_ROOT = Path(__file__).resolve().parents[2]
SWARM_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"

# ---------------------------------------------------------------------------
# Forbidden-symbol enumeration.
# ---------------------------------------------------------------------------

# Whole-module imports that have no purpose other than caching. Any
# ``import X`` or ``from X[.sub] import ...`` rooted at one of these
# names is a regression.
FORBIDDEN_CACHE_MODULE_ROOTS: frozenset[str] = frozenset(
    {
        "cachetools",
        "requests_cache",
        "aiocache",
        "diskcache",
    }
)

# Symbol-level imports from otherwise-legitimate stdlib modules that
# DO have non-cache uses (notably ``functools``). Listing the exact
# ``(module, attr)`` keeps unrelated functools utilities (``partial``,
# ``reduce``, ``wraps``) usable while still flagging the two cache
# decorators.
FORBIDDEN_FROM_IMPORT_PAIRS: frozenset[tuple[str, str]] = frozenset(
    {
        ("functools", "lru_cache"),
        ("functools", "cache"),
    }
)

# Dotted-name targets that must not appear as decorators or call
# expressions anywhere in swarm code. Covers the ``import functools``
# + ``@functools.lru_cache`` form that the from-import audit cannot
# see, plus every cache-decorator surface exposed by the third-party
# libraries above.
FORBIDDEN_DOTTED_TARGETS: frozenset[str] = frozenset(
    {
        "functools.lru_cache",
        "functools.cache",
        "cachetools.cached",
        "cachetools.cachedmethod",
        "cachetools.func.lru_cache",
        "cachetools.func.ttl_cache",
        "requests_cache.install_cache",
        "requests_cache.CachedSession",
        "aiocache.cached",
        "aiocache.cached_stampede",
        "diskcache.memoize",
    }
)

# This test file enumerates the forbidden tokens to document the
# rule; exclude it from the scan so the documentation does not
# self-flag.
SELF_PATH = Path(__file__).resolve()


# ---------------------------------------------------------------------------
# Source enumeration + AST visitor.
# ---------------------------------------------------------------------------


def _iter_swarm_py_sources() -> list[Path]:
    """Return every ``.py`` source file under the swarm package."""
    if not SWARM_DIR.exists():
        return []
    return [
        p
        for p in SWARM_DIR.rglob("*.py")
        if p.is_file()
        and "__pycache__" not in p.parts
        and p.resolve() != SELF_PATH
    ]


def _resolve_attribute_chain(node: ast.AST) -> str | None:
    """Resolve ``a.b.c`` chains to a dotted string; return None otherwise.

    Mirrors the helper in ``test_concurrency_python_only.py``: anything
    that doesn't resolve to a static name chain (a method on a local
    variable, a lambda, an indirect callable) is ignored. The
    import-statement guard handles the path that would let an indirect
    callable reach swarm code.
    """
    parts: list[str] = []
    current: ast.AST = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if not isinstance(current, ast.Name):
        return None
    parts.append(current.id)
    return ".".join(reversed(parts))


class _CacheImportVisitor(ast.NodeVisitor):
    """Collect forbidden cache imports + decorator / call expressions."""

    def __init__(self) -> None:
        self.module_import_hits: list[tuple[int, str]] = []
        self.from_import_hits: list[tuple[int, str]] = []
        self.dotted_target_hits: list[tuple[int, str]] = []

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802 -- ast API
        for alias in node.names:
            root = alias.name.split(".", 1)[0]
            if root in FORBIDDEN_CACHE_MODULE_ROOTS:
                self.module_import_hits.append((node.lineno, alias.name))
        self.generic_visit(node)

    def visit_ImportFrom(  # noqa: N802 -- ast API
        self, node: ast.ImportFrom
    ) -> None:
        module = node.module or ""
        root = module.split(".", 1)[0]
        if root in FORBIDDEN_CACHE_MODULE_ROOTS:
            self.from_import_hits.append(
                (node.lineno, f"from {module} import ...")
            )
        else:
            for alias in node.names:
                if (module, alias.name) in FORBIDDEN_FROM_IMPORT_PAIRS:
                    self.from_import_hits.append(
                        (node.lineno, f"from {module} import {alias.name}")
                    )
        self.generic_visit(node)

    def _record_dotted_hit(self, node: ast.AST) -> None:
        """Flag ``node`` if it resolves to a forbidden dotted target."""
        dotted = _resolve_attribute_chain(node)
        if dotted is None:
            return
        if dotted in FORBIDDEN_DOTTED_TARGETS:
            self.dotted_target_hits.append((getattr(node, "lineno", 0), dotted))

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802 -- ast API
        # ``functools.lru_cache(...)`` shows up as Call(func=Attribute(...))
        # whether used as a bare call or a parameterised decorator.
        self._record_dotted_hit(node.func)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802 -- ast API
        # ``@functools.lru_cache`` (no parens) shows up as a bare
        # Attribute in the decorator_list; covered by the same dotted
        # chain check.
        self._record_dotted_hit(node)
        self.generic_visit(node)


def _scan_module(path: Path) -> _CacheImportVisitor:
    """Return a populated visitor for one swarm source file."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    visitor = _CacheImportVisitor()
    visitor.visit(tree)
    return visitor


# ---------------------------------------------------------------------------
# Static audit -- the production swarm tree must stay cache-free.
# ---------------------------------------------------------------------------


def test_swarm_package_exists() -> None:
    """Audit needs a target; an accidentally-deleted package must be loud."""
    assert SWARM_DIR.is_dir(), (
        f"Swarm package missing at {SWARM_DIR.relative_to(REPO_ROOT)}; "
        "NFR-014 cache audit has nothing to scan."
    )


def test_no_forbidden_cache_module_imports() -> None:
    """NFR-014: no ``import cachetools`` / ``requests_cache`` / etc.

    The whole-module roots in :data:`FORBIDDEN_CACHE_MODULE_ROOTS`
    exist for one purpose: caching. Any of them appearing as a
    module-level import inside the swarm package is a regression
    regardless of how it's eventually used.
    """
    offenders: list[str] = []
    for source in _iter_swarm_py_sources():
        visitor = _scan_module(source)
        for lineno, name in visitor.module_import_hits:
            offenders.append(
                f"  {source.relative_to(REPO_ROOT)}:{lineno}: import {name}"
            )
    assert not offenders, (
        "NFR-014 violation: response-cache module imported in swarm sources. "
        "Each invocation must re-dispatch -- no cross-run cache layer:\n"
        + "\n".join(offenders)
    )


def test_no_forbidden_symbol_imports() -> None:
    """NFR-014: no ``from functools import lru_cache`` / ``cache``.

    ``functools`` itself stays usable (``partial``, ``wraps``,
    ``reduce`` are unrelated to response caching); only the two
    cache decorators are forbidden at the symbol level.
    """
    offenders: list[str] = []
    for source in _iter_swarm_py_sources():
        visitor = _scan_module(source)
        for lineno, statement in visitor.from_import_hits:
            offenders.append(
                f"  {source.relative_to(REPO_ROOT)}:{lineno}: {statement}"
            )
    assert not offenders, (
        "NFR-014 violation: response-cache symbol imported in swarm sources. "
        "Two identical runs must both hit the transport:\n"
        + "\n".join(offenders)
    )


def test_no_forbidden_dotted_cache_targets() -> None:
    """NFR-014: no ``functools.lru_cache`` / ``cachetools.cached`` references.

    Covers the ``import functools`` + ``@functools.lru_cache`` form
    that the from-import audit cannot see, plus every third-party
    cache-decorator surface enumerated in
    :data:`FORBIDDEN_DOTTED_TARGETS`. Detects both decorator-without-
    parens (``@functools.cache``) and parameterised-call forms
    (``@functools.lru_cache(maxsize=None)``).
    """
    offenders: list[str] = []
    for source in _iter_swarm_py_sources():
        visitor = _scan_module(source)
        for lineno, dotted in visitor.dotted_target_hits:
            offenders.append(
                f"  {source.relative_to(REPO_ROOT)}:{lineno}: {dotted}"
            )
    assert not offenders, (
        "NFR-014 violation: cache-decorator reference detected in swarm "
        "sources. Dispatch / transport surfaces must re-execute on every "
        "invocation:\n" + "\n".join(offenders)
    )


def test_forbidden_sets_are_nonempty() -> None:
    """A future refactor must not silently empty the forbidden sets.

    Without this guard a typo that cleared
    :data:`FORBIDDEN_CACHE_MODULE_ROOTS` or
    :data:`FORBIDDEN_DOTTED_TARGETS` would render the corresponding
    static audit a no-op.
    """
    assert FORBIDDEN_CACHE_MODULE_ROOTS, (
        "FORBIDDEN_CACHE_MODULE_ROOTS must enumerate cache libraries; "
        "an empty set would render the module-import audit a no-op."
    )
    assert FORBIDDEN_FROM_IMPORT_PAIRS, (
        "FORBIDDEN_FROM_IMPORT_PAIRS must enumerate functools cache "
        "symbols; an empty set would render the symbol-import audit "
        "a no-op."
    )
    assert FORBIDDEN_DOTTED_TARGETS, (
        "FORBIDDEN_DOTTED_TARGETS must enumerate dotted cache targets; "
        "an empty set would render the attribute audit a no-op."
    )


# ---------------------------------------------------------------------------
# Integration probe -- two identical runs hit the transport twice.
# ---------------------------------------------------------------------------


def _make_preflight(workers_requested: int) -> PreflightResult:
    """Minimal :class:`PreflightResult` for the integration probe."""
    manifest = Manifest(
        contract_version="1.0",
        job_id="job-nfr014",
        preflight=PreflightSummary(
            target_checksum="deadbeef",
            workers_requested=workers_requested,
            transport_kind="stub",
        ),
    )
    state = SwarmState(state="preflight_ok", job_id="job-nfr014")
    return PreflightResult(manifest=manifest, state=state)


class _CountingTransport:
    """Lock-coordinated counter that records every ``send`` call.

    The lock is necessary because :func:`dispatch_wave1` fans the
    calls out through :class:`ParallelExecutor`; without a lock the
    counter increment would race and the test could falsely accept a
    cache regression that collapsed a few of the calls. The lock is
    also why the test can rely on ``len(calls) == 2 * N`` rather than
    a more permissive ``>= N`` assertion -- the counter is the
    ground-truth invocation count.
    """

    def __init__(self) -> None:
        self.calls: list[tuple[str, int]] = []
        self._lock = threading.Lock()

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        with self._lock:
            self.calls.append((prompt, timeout))
        return WorkerResult(status="success", http_code=200, attempts=1)


def test_two_identical_runs_both_hit_transport() -> None:
    """NFR-014: identical inputs re-dispatch -- transport called 2*N times.

    The acceptance criterion (phase-3-tasklist.md T03.19) reads "two
    identical runs both hit transport (call count 2, not 1)". The
    test generalises to ``2 * N`` so it scales with the fan-out
    count: a regression that wrapped dispatch in ``lru_cache`` would
    collapse the second run's calls to zero (whole-job cache) or one
    (per-prompt cache); either form trips the assertion.
    """
    workers_requested = 3
    preflight = _make_preflight(workers_requested)
    transport = _CountingTransport()

    first = dispatch_wave1(preflight, transport=transport, prompt="identical")
    second = dispatch_wave1(preflight, transport=transport, prompt="identical")

    assert len(first) == workers_requested
    assert len(second) == workers_requested
    expected_calls = 2 * workers_requested
    assert len(transport.calls) == expected_calls, (
        "NFR-014 violation: two identical dispatch_wave1 runs hit the "
        f"transport {len(transport.calls)} times; expected "
        f"{expected_calls} (one ``send`` per worker per run). A cache "
        "layer somewhere between dispatch and transport collapsed the "
        "second run's calls -- inspect dispatch_wave1, retry_policy, "
        "and the transport for an lru_cache / cachetools / "
        "requests_cache decorator."
    )
    # Belt-and-braces: every recorded call carries the same prompt.
    assert all(prompt == "identical" for prompt, _ in transport.calls)


def test_two_identical_runs_use_fresh_transport_instance() -> None:
    """A fresh transport per run still gets ``N`` calls.

    Complements the shared-transport probe by closing the
    "we cache against the transport instance" loophole. Two
    distinct ``_CountingTransport`` objects can't share a cache; if
    they did somehow share state, this test would notice because the
    second instance's call count would shift away from N.
    """
    workers_requested = 2
    preflight = _make_preflight(workers_requested)
    transport_a = _CountingTransport()
    transport_b = _CountingTransport()

    dispatch_wave1(preflight, transport=transport_a, prompt="same")
    dispatch_wave1(preflight, transport=transport_b, prompt="same")

    assert len(transport_a.calls) == workers_requested
    assert len(transport_b.calls) == workers_requested


# ---------------------------------------------------------------------------
# Mutation guards -- prove the detectors actually catch regressions.
# ---------------------------------------------------------------------------


def test_audit_detects_mutation_cache_module_import() -> None:
    """Mutation guard: AST visitor flags synthetic cache-module imports."""
    synthetic = (
        "import cachetools\n"
        "import requests_cache as _rc\n"
        "from aiocache.serializers import PickleSerializer\n"
        "from diskcache import Cache\n"
        "def f():\n"
        "    return None\n"
    )
    tree = ast.parse(synthetic, filename="<synthetic>")
    visitor = _CacheImportVisitor()
    visitor.visit(tree)
    imported = {name for _, name in visitor.module_import_hits}
    from_imports = {stmt for _, stmt in visitor.from_import_hits}
    assert "cachetools" in imported, (
        "Import visitor failed on synthetic ``import cachetools``; "
        "NFR-014 audit would silently pass on a real regression."
    )
    assert "requests_cache" in imported, (
        "Import visitor failed on synthetic ``import requests_cache``; "
        "NFR-014 audit would silently pass on a real regression."
    )
    assert any("aiocache" in stmt for stmt in from_imports), (
        "ImportFrom visitor failed on synthetic ``from aiocache...``; "
        "NFR-014 audit would silently pass on a real regression."
    )
    assert any("diskcache" in stmt for stmt in from_imports), (
        "ImportFrom visitor failed on synthetic ``from diskcache...``; "
        "NFR-014 audit would silently pass on a real regression."
    )


def test_audit_detects_mutation_functools_symbol_import() -> None:
    """Mutation guard: AST visitor flags ``from functools import lru_cache``.

    Both stdlib cache decorators must be caught, and unrelated
    functools utilities (``partial``, ``wraps``) MUST NOT be caught
    -- otherwise the audit would fire on every benign functools use
    in swarm.
    """
    synthetic = (
        "from functools import lru_cache, cache, partial, wraps\n"
        "def f():\n"
        "    return None\n"
    )
    tree = ast.parse(synthetic, filename="<synthetic>")
    visitor = _CacheImportVisitor()
    visitor.visit(tree)
    statements = {stmt for _, stmt in visitor.from_import_hits}
    assert "from functools import lru_cache" in statements, (
        "ImportFrom visitor missed ``from functools import lru_cache``; "
        "NFR-014 audit would silently pass on a real regression."
    )
    assert "from functools import cache" in statements, (
        "ImportFrom visitor missed ``from functools import cache``; "
        "NFR-014 audit would silently pass on a real regression."
    )
    # Negative: partial / wraps must NOT trip the audit.
    for benign in ("partial", "wraps"):
        assert f"from functools import {benign}" not in statements, (
            f"Audit falsely flagged the benign ``functools.{benign}`` "
            "symbol; this would break unrelated swarm code."
        )


def test_audit_detects_mutation_dotted_cache_decorator() -> None:
    """Mutation guard: visitor flags ``@functools.lru_cache`` decorator forms."""
    synthetic = (
        "import functools\n"
        "import cachetools\n"
        "@functools.lru_cache(maxsize=None)\n"
        "def cached_with_parens(x):\n"
        "    return x\n"
        "@functools.cache\n"
        "def cached_bare(x):\n"
        "    return x\n"
        "@cachetools.cached(cache={})\n"
        "def via_cachetools(x):\n"
        "    return x\n"
    )
    tree = ast.parse(synthetic, filename="<synthetic>")
    visitor = _CacheImportVisitor()
    visitor.visit(tree)
    flagged = {dotted for _, dotted in visitor.dotted_target_hits}
    assert "functools.lru_cache" in flagged, (
        "Dotted-target visitor missed ``@functools.lru_cache(...)``; "
        "NFR-014 audit would silently pass on a real regression."
    )
    assert "functools.cache" in flagged, (
        "Dotted-target visitor missed bare ``@functools.cache``; "
        "NFR-014 audit would silently pass on a real regression."
    )
    assert "cachetools.cached" in flagged, (
        "Dotted-target visitor missed ``@cachetools.cached(...)``; "
        "NFR-014 audit would silently pass on a real regression."
    )


def test_call_counting_transport_increments_per_call() -> None:
    """Mutation guard: the integration probe's counter actually advances.

    A regression that broke :class:`_CountingTransport.send` (e.g.
    dropped the ``append``) would silently zero out
    :func:`test_two_identical_runs_both_hit_transport`. Pin the
    behaviour explicitly here so the integration probe stays
    falsifiable.
    """
    transport = _CountingTransport()
    transport.send("a", 1)
    transport.send("b", 2)
    transport.send("a", 1)
    assert transport.calls == [("a", 1), ("b", 2), ("a", 1)], (
        "_CountingTransport must record every ``send`` invocation "
        "verbatim; NFR-014 integration probe relies on this counter."
    )
