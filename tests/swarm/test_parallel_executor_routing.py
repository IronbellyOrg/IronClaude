"""T03.15 -- NFR-001 / AC-004 ParallelExecutor routing CI guard.

Enforces roadmap rows R-074 (NFR-001) and R-080 (AC-004) -- the swarm
dispatch fan-out MUST route through
:class:`superclaude.execution.parallel.ParallelExecutor`. No code path
inside ``src/superclaude/cli/swarm/`` is permitted to instantiate
``concurrent.futures.ThreadPoolExecutor`` (or
``ProcessPoolExecutor``) directly: every parallel surface in the swarm
package goes through ``ParallelExecutor`` so a future cancellation /
quota / scheduling layer has a single seam to extend.

Relationship to sibling guards
------------------------------

* ``test_concurrency_python_only.py`` (T03.14, INV-002) bans the
  *shell-out* family (``subprocess``, ``os.system``, retired
  ``swarm_dispatch.sh``). That guard explicitly notes the
  ``ThreadPoolExecutor`` mandate is enforced **here**.
* ``test_imm3_parallel.py`` (T03.02 / T03.11, IMM-3) proves the
  dispatch wave actually overlaps workers in wall-clock. That guard
  asserts the *behaviour*; this guard asserts the *routing*. The two
  are complementary -- a regression that swapped ``ParallelExecutor``
  for a raw ``ThreadPoolExecutor`` might still pass IMM-3 timing-wise
  but would silently bypass the single-seam invariant NFR-001 / AC-004
  exist to preserve.

Audit shape
-----------

Three layered assertions:

1. **Routing -- functional.** ``dispatch_wave1`` invokes
   ``ParallelExecutor.plan`` and ``ParallelExecutor.execute`` against a
   transport-backed run. A recording subclass counts the calls; a
   regression that bypassed the executor (e.g. constructed a
   ``ThreadPoolExecutor`` inline) would leave the counter at zero.
2. **Routing -- static.** ``dispatch.py`` is parsed with ``ast`` and
   the module is required to import ``ParallelExecutor`` from
   ``superclaude.execution.parallel``. The import statement is the
   single seam; deleting it is the canonical way the mandate would be
   silently broken.
3. **Ban -- static.** Every ``.py`` source under
   ``src/superclaude/cli/swarm/`` is parsed with ``ast`` and any
   ``ThreadPoolExecutor(...)`` or ``ProcessPoolExecutor(...)`` call
   expression is flagged. Bare docstring/comment mentions are left
   alone (they appear legitimately in the ``dispatch.py`` module
   docstring documenting the mandate itself).

Docstring contract
------------------

The acceptance criterion mandates the AC-004 / NFR-001 contract is
documented in ``dispatch.py``'s module docstring. The fourth assertion
parses the dispatch module's docstring and requires the literal tokens
``AC-004``, ``NFR-001``, and ``ParallelExecutor`` to appear. A future
docstring rewrite that loses any of those anchors must update this
guard intentionally.

Mutation guarantee
------------------

Each detector ships with a ``test_audit_detects_*`` mutation guard that
runs the detector against a synthetic offending source. Without those
guards a regression in the AST visitor (typo'd attribute name, empty
forbidden set, broken file-discovery glob) would silently green the
whole suite.
"""

from __future__ import annotations

import ast
import threading
from pathlib import Path
from typing import Optional

import pytest

from superclaude.cli.swarm import dispatch as dispatch_module
from superclaude.cli.swarm.dispatch import dispatch_wave1
from superclaude.cli.swarm.models import (
    Manifest,
    PreflightSummary,
    SwarmState,
    WorkerResult,
)
from superclaude.cli.swarm.preflight import PreflightResult
from superclaude.execution.parallel import ExecutionPlan, ParallelExecutor


REPO_ROOT = Path(__file__).resolve().parents[2]
SWARM_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"
DISPATCH_PATH = SWARM_DIR / "dispatch.py"

# Forbidden Executor constructors. ``ParallelExecutor`` wraps a
# ``ThreadPoolExecutor`` internally; swarm code MUST go through it
# rather than instantiate either of these primitives directly.
FORBIDDEN_EXECUTOR_NAMES: frozenset[str] = frozenset(
    {
        "ThreadPoolExecutor",
        "ProcessPoolExecutor",
    }
)

# Required module-level import in dispatch.py. The import is the
# single seam NFR-001 / AC-004 codify; deleting it is the canonical
# way the mandate would be silently broken.
REQUIRED_DISPATCH_IMPORT_MODULE = "superclaude.execution.parallel"
REQUIRED_DISPATCH_IMPORT_NAME = "ParallelExecutor"

# Tokens that MUST appear in the dispatch.py module docstring per the
# T03.15 acceptance criterion ("AC-004 mandate documented in
# dispatch.py docstring").
REQUIRED_DISPATCH_DOCSTRING_TOKENS: tuple[str, ...] = (
    "AC-004",
    "NFR-001",
    "ParallelExecutor",
)

# Excluded from the static ban scan: this test file references the
# forbidden constructor names by literal string (in the forbidden set
# above and in docstrings) so the audit can name what it forbids.
SELF_PATH = Path(__file__).resolve()


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


def _resolve_attribute_chain(node: ast.AST) -> Optional[str]:
    """Resolve ``a.b.c`` chains to a dotted string; return None otherwise.

    Mirrors the helper in ``test_concurrency_python_only.py`` so the
    two guards stay structurally consistent. A bare ``Name`` (e.g.
    ``ThreadPoolExecutor(...)`` called against a plain imported name)
    resolves to the unqualified identifier; an attribute chain
    (``concurrent.futures.ThreadPoolExecutor(...)``) resolves to the
    fully-dotted string.
    """
    parts: list[str] = []
    current: ast.AST = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))
    return None


class _ForbiddenExecutorVisitor(ast.NodeVisitor):
    """Collect call expressions instantiating banned Executor classes."""

    def __init__(self) -> None:
        self.hits: list[tuple[int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802 -- ast API
        dotted = _resolve_attribute_chain(node.func)
        if dotted is not None:
            tail = dotted.rsplit(".", 1)[-1]
            if tail in FORBIDDEN_EXECUTOR_NAMES:
                self.hits.append((node.lineno, dotted))
        self.generic_visit(node)


def _scan_for_forbidden_executors(path: Path) -> list[tuple[int, str]]:
    """Return banned-Executor call-site hits for one swarm source file."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    visitor = _ForbiddenExecutorVisitor()
    visitor.visit(tree)
    return visitor.hits


def _dispatch_import_names() -> set[str]:
    """Return the names imported into dispatch.py from the parallel module.

    Parses ``dispatch.py`` and collects every name pulled in by
    ``from superclaude.execution.parallel import X[, Y, ...]``. The
    guard then asserts ``ParallelExecutor`` is among them.
    """
    tree = ast.parse(DISPATCH_PATH.read_text(encoding="utf-8"), filename=str(DISPATCH_PATH))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == REQUIRED_DISPATCH_IMPORT_MODULE:
            for alias in node.names:
                names.add(alias.name)
    return names


# ---------------------------------------------------------------------------
# Functional routing assertion -- dispatch invokes ParallelExecutor.
# ---------------------------------------------------------------------------


class _RecordingExecutor(ParallelExecutor):
    """ParallelExecutor that records every plan + execute invocation.

    Differs from ``test_imm3_parallel._GroupCountingExecutor`` only in
    intent: this guard does not care about group cardinality, only that
    ``dispatch_wave1`` actually drives the executor at all. A regression
    that bypassed ``ParallelExecutor`` (e.g. inlined a raw
    ``ThreadPoolExecutor``) would leave both counters at zero.
    """

    def __init__(self, max_workers: int) -> None:
        super().__init__(max_workers=max_workers)
        self.plan_calls = 0
        self.execute_calls = 0

    def plan(self, tasks):  # type: ignore[override]
        self.plan_calls += 1
        return super().plan(tasks)

    def execute(self, plan: ExecutionPlan):  # type: ignore[override]
        self.execute_calls += 1
        return super().execute(plan)


class _NoOpTransport:
    """Returns a trivial success result; no sleep, no network."""

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        return WorkerResult(status="success", http_code=200, attempts=1)


def _make_preflight(workers_requested: int) -> PreflightResult:
    manifest = Manifest(
        contract_version="1.0",
        job_id="job-routing",
        preflight=PreflightSummary(
            target_checksum="cafebabe",
            workers_requested=workers_requested,
            transport_kind="stub",
        ),
    )
    return PreflightResult(
        manifest=manifest,
        state=SwarmState(state="preflight_ok", job_id="job-routing"),
    )


def test_swarm_package_exists() -> None:
    """Phase 3 has wired the swarm package; the audit needs a target.

    Mirrors the guard in ``test_concurrency_python_only.py`` -- without
    this assertion an accidentally-deleted ``swarm/`` directory would
    silently make every static scan pass vacuously.
    """
    assert SWARM_DIR.is_dir(), (
        f"Swarm package missing at {SWARM_DIR.relative_to(REPO_ROOT)}; "
        "NFR-001 / AC-004 audit has nothing to scan."
    )
    assert DISPATCH_PATH.is_file(), (
        f"Dispatch module missing at {DISPATCH_PATH.relative_to(REPO_ROOT)}; "
        "NFR-001 / AC-004 audit cannot verify the import seam."
    )


def test_dispatch_wave1_invokes_parallel_executor() -> None:
    """Functional NFR-001: dispatch routes through ParallelExecutor.

    Hands ``dispatch_wave1`` a ``_RecordingExecutor`` and asserts both
    ``plan`` and ``execute`` were driven. A regression that bypassed
    the executor (e.g. constructed a raw ``ThreadPoolExecutor``) would
    leave the counters at zero even though the workers still ran.
    """
    preflight = _make_preflight(workers_requested=3)
    executor = _RecordingExecutor(max_workers=3)

    results = dispatch_wave1(
        preflight,
        transport=_NoOpTransport(),
        parallel_executor=executor,
    )

    assert len(results) == 3
    assert all(r.status == "success" for r in results)
    assert executor.plan_calls == 1, (
        "dispatch_wave1 did not invoke ParallelExecutor.plan; "
        "NFR-001 / AC-004 regression: dispatch must route through the "
        "ParallelExecutor seam."
    )
    assert executor.execute_calls == 1, (
        "dispatch_wave1 did not invoke ParallelExecutor.execute; "
        "NFR-001 / AC-004 regression: dispatch must route through the "
        "ParallelExecutor seam."
    )


def test_dispatch_imports_parallel_executor_from_canonical_module() -> None:
    """Static NFR-001: dispatch.py imports the canonical ParallelExecutor.

    The mandate is that dispatch route through
    ``superclaude.execution.parallel.ParallelExecutor`` specifically --
    not a shim, not a re-export under a different module path. A
    regression that swapped the import target would silently break the
    "single seam" invariant the AC-004 docstring promises.
    """
    imported = _dispatch_import_names()
    assert REQUIRED_DISPATCH_IMPORT_NAME in imported, (
        f"dispatch.py is missing `from {REQUIRED_DISPATCH_IMPORT_MODULE} "
        f"import {REQUIRED_DISPATCH_IMPORT_NAME}` -- the NFR-001 / AC-004 "
        "single-seam import is the structural anchor of the mandate; "
        "every regression that drops it must do so intentionally and "
        f"update this guard. Actually imported names: {sorted(imported)}"
    )


def test_dispatch_module_docstring_documents_mandate() -> None:
    """Static AC-004: dispatch.py module docstring spells the mandate.

    T03.15 acceptance criterion: "AC-004 mandate documented in
    dispatch.py docstring." The tokens enumerated here are the minimum
    set of anchors a future reader needs to trace the contract back to
    the spec rows.
    """
    docstring = ast.get_docstring(
        ast.parse(DISPATCH_PATH.read_text(encoding="utf-8"), filename=str(DISPATCH_PATH))
    )
    assert docstring is not None, (
        "dispatch.py has no module docstring; AC-004 mandate cannot be "
        "documented where T03.15 acceptance criterion requires."
    )
    missing = [token for token in REQUIRED_DISPATCH_DOCSTRING_TOKENS if token not in docstring]
    assert not missing, (
        "dispatch.py module docstring is missing required anchors for "
        f"the AC-004 / NFR-001 mandate: {missing}. Re-add the contract "
        "summary tying dispatch to ParallelExecutor + AC-004 + NFR-001."
    )


def test_no_threadpool_or_processpool_instantiation_in_swarm() -> None:
    """Static AC-004: no raw Executor constructor calls anywhere in swarm.

    Mirrors the spec validation step
    ``grep -RnE "ThreadPoolExecutor\\(" src/superclaude/cli/swarm/`` --
    any call expression whose target's tail name is one of
    ``ThreadPoolExecutor`` / ``ProcessPoolExecutor`` is a direct
    AC-004 regression. The AST scan tolerates docstring/comment
    mentions (the dispatch module legitimately names the constructor
    in prose) while still flagging real call sites.
    """
    offenders: list[str] = []
    for source in _iter_swarm_py_sources():
        for lineno, target in _scan_for_forbidden_executors(source):
            offenders.append(
                f"  {source.relative_to(REPO_ROOT)}:{lineno}: {target}(...)"
            )
    assert not offenders, (
        "AC-004 violation: raw Executor constructor detected in swarm "
        "sources. Dispatch must route through "
        "superclaude.execution.parallel.ParallelExecutor:\n"
        + "\n".join(offenders)
    )


# ---------------------------------------------------------------------------
# Mutation guards -- prove the detectors flag real regressions.
# ---------------------------------------------------------------------------


def test_audit_detects_mutation_threadpool_call() -> None:
    """Mutation guard: AST visitor flags a synthetic ThreadPoolExecutor call."""
    synthetic = (
        "from concurrent.futures import ThreadPoolExecutor\n"
        "def fan_out():\n"
        "    with ThreadPoolExecutor(max_workers=4) as pool:\n"
        "        return pool\n"
    )
    tree = ast.parse(synthetic, filename="<synthetic>")
    visitor = _ForbiddenExecutorVisitor()
    visitor.visit(tree)
    flagged = {target for _, target in visitor.hits}
    assert "ThreadPoolExecutor" in flagged, (
        "ForbiddenExecutorVisitor failed on synthetic "
        "ThreadPoolExecutor(...) call; AC-004 audit would silently "
        "pass on a real regression."
    )


def test_audit_detects_mutation_processpool_call() -> None:
    """Mutation guard: AST visitor flags a synthetic ProcessPoolExecutor call."""
    synthetic = (
        "import concurrent.futures\n"
        "def fan_out():\n"
        "    return concurrent.futures.ProcessPoolExecutor(max_workers=2)\n"
    )
    tree = ast.parse(synthetic, filename="<synthetic>")
    visitor = _ForbiddenExecutorVisitor()
    visitor.visit(tree)
    flagged_tails = {target.rsplit(".", 1)[-1] for _, target in visitor.hits}
    assert "ProcessPoolExecutor" in flagged_tails, (
        "ForbiddenExecutorVisitor failed on synthetic "
        "concurrent.futures.ProcessPoolExecutor(...) call; AC-004 "
        "audit would silently pass on a real regression."
    )


def test_audit_detects_mutation_import_visitor() -> None:
    """Mutation guard: import-name visitor flags a missing ParallelExecutor.

    Exercises ``_dispatch_import_names`` against a synthetic module
    that imports something else from ``superclaude.execution.parallel``
    but *not* ``ParallelExecutor``. The static guard's whole purpose is
    to fail when this happens.
    """
    synthetic = (
        "from superclaude.execution.parallel import Task\n"
        "x = Task\n"
    )
    tree = ast.parse(synthetic, filename="<synthetic>")
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == REQUIRED_DISPATCH_IMPORT_MODULE:
            for alias in node.names:
                imported.add(alias.name)
    assert "Task" in imported, (
        "ImportFrom visitor failed on synthetic import; mutation guard "
        "for `_dispatch_import_names` is broken."
    )
    assert REQUIRED_DISPATCH_IMPORT_NAME not in imported, (
        "Synthetic module unexpectedly contained ParallelExecutor; "
        "mutation guard cannot prove the detector flags absence."
    )


def test_forbidden_executor_set_is_nonempty() -> None:
    """Guard against an empty forbidden set silently greening every scan.

    Mirrors the equivalent guard in ``test_concurrency_python_only.py``
    -- a future refactor that emptied ``FORBIDDEN_EXECUTOR_NAMES``
    would make the AC-004 ban audit a no-op without anyone noticing.
    """
    assert FORBIDDEN_EXECUTOR_NAMES, (
        "FORBIDDEN_EXECUTOR_NAMES must enumerate the banned Executor "
        "constructors; an empty set would render the AC-004 ban audit "
        "a no-op."
    )
    assert REQUIRED_DISPATCH_DOCSTRING_TOKENS, (
        "REQUIRED_DISPATCH_DOCSTRING_TOKENS must enumerate the docstring "
        "anchors; an empty tuple would render the docstring audit a no-op."
    )
