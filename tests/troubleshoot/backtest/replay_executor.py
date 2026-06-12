"""ReplayExecutor seam -- the spawn -> observe driver for the in-process differential replay.

Mirrors ``src/superclaude/cli/eval/runner.py``'s ``LifecycleExecutor`` Protocol (runner.py:136-156)
and its frozen ``ObservedRun`` result (runner.py:109-133): ``LifecycleExecutor`` is the injectable
strategy that production implements over a PTY driver and tests substitute with a recording stub.

Here the analogue is ``ReplayExecutor.replay(escape, worktree) -> ReplayResult``: a single seam that
invokes the REAL pre-fix product callable IN-PROCESS (NOT a literal Claude PTY -- per NFR-3's
single-seam bound) against a checked-out pre-fix-parent worktree, and is unit-testable by
substituting a stub ``ReplayExecutor``.

INVOCATION-CONTRACT CAVEAT (why invokers are injected, not hardcoded): the five pre-fix callables
are NOT uniform. E1 ``_build_file_args`` (class ``PrdClaudeProcess``, cli/prd/process.py) and E4
``_evaluate_gate`` (class ``PrdExecutor``, cli/prd/executor.py) are CLASS-BOUND; E2
``_check_parallel_instructions`` (cli/prd/gates.py) and E3 ``gate_passed`` (cli/pipeline/gates.py)
are MODULE-LEVEL functions; E5 lives in a markdown skill, not a Python callable. The owning-class
names are only guidance for what to instantiate -- the ACTUAL pre-fix-parent signature may differ
(e.g. a ``@staticmethod`` with a different arg shape at the parent commit). So this module does NOT
hardcode any call signature: it provides ``resolve_callable`` (which reads the real signature from
the checked-out tree via ``inspect``) and a default executor that delegates the per-escape, signature-
adaptive invocation to an injected invoker (the per-escape Phase 4 runners supply these, where the
target signature is known and can be inspected first).
"""

from __future__ import annotations

import importlib.util
import inspect
import json
import subprocess as _subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Protocol, runtime_checkable

from tests.troubleshoot.backtest.git_replay import ReplayEscape, checkout_worktree

# Verdict tokens -- kept identical to catch_rate.EscapeResult.verdict ({CATCH, MISS}); ERROR is an
# executor-internal sentinel for an invocation that raised (never a legitimate catch-rate verdict).
VERDICT_MISS = "MISS"
VERDICT_CATCH = "CATCH"
VERDICT_ERROR = "ERROR"


@dataclass(frozen=True)
class ReplayResult:
    """Outcome of one in-process replay (mirror of ``ObservedRun`` at runner.py:109-133).

    Fields:
        escape_id: Canonical escape id (E1..E5).
        verdict: ``MISS`` (old protocol let the escape through) | ``CATCH`` (new gate would catch)
            | ``ERROR`` (the invocation itself raised -- not a legitimate catch-rate verdict).
        observed: The raw thing the pre-fix callable returned/emitted (argv list, gate tuple, etc.).
        detail: Human-readable note on what was observed and why it maps to the verdict.
    """

    escape_id: str
    verdict: str
    observed: Any = None
    detail: str = ""


@dataclass(frozen=True)
class ResolvedCallable:
    """A product callable resolved from a checked-out worktree, with its REAL signature read.

    ``is_class_bound`` distinguishes the two class-bound callables (E1/E4) from the two module-level
    ones (E2/E3). ``signature`` is read from the checked-out tree so the invoker adapts to the
    actual pre-fix-parent arg shape rather than a hardcoded guess.
    """

    target: Any
    qualname: str
    is_class_bound: bool
    owning_class: type | None
    signature: inspect.Signature | None


@runtime_checkable
class ReplayExecutor(Protocol):
    """Spawn -> observe seam (mirrors ``LifecycleExecutor`` at runner.py:136-156).

    Production: the default in-process executor invokes the real pre-fix callable. Tests substitute
    a stub that records the call and returns a canned :class:`ReplayResult`. No literal PTY/pexpect.
    """

    def replay(
        self, escape: ReplayEscape, worktree: Path
    ) -> ReplayResult:  # pragma: no cover - protocol
        ...


def read_source_from_worktree(worktree: str | Path, relpath: str) -> str:
    """Return the verbatim text of ``relpath`` as it exists in the checked-out ``worktree``.

    Source-level reading is the safe option when importing a pre-fix module is unsound (absolute
    ``from superclaude...`` imports would resolve against the live tree on ``sys.path``, not the
    checked-out parent). Per-escape runners use this for assertions like "argv contains ``--file``".
    """
    return (Path(worktree) / relpath).read_text(encoding="utf-8")


def load_module_from_worktree(worktree: str | Path, relpath: str, *, module_name: str):
    """Import the module at ``worktree/relpath`` under a synthetic ``module_name``.

    CAVEAT: a module that performs absolute ``from superclaude...`` imports will resolve those
    against whatever ``superclaude`` is on ``sys.path`` (typically the live tree), NOT the checked-out
    parent. Use this only for modules whose pre-fix target is import-safe in isolation; otherwise use
    :func:`read_source_from_worktree`. The per-escape runner owns this decision.
    """
    path = Path(worktree) / relpath
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot build import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def resolve_callable(module: Any, qualname: str) -> ResolvedCallable:
    """Resolve ``qualname`` on ``module`` and read its REAL signature (do not assume a shape).

    ``qualname`` may be a bare function name (``gate_passed``) or ``Class.method``
    (``PrdClaudeProcess._build_file_args``). For the latter the returned ``target`` is the function
    object found on the class (an unbound function the invoker can call with a constructed or
    ``SimpleNamespace`` ``self``, or via an instance). ``signature`` is read from the actual object
    so the invoker adapts to the pre-fix-parent arg shape rather than a hardcoded guess.
    """
    if "." in qualname:
        class_name, attr = qualname.split(".", 1)
        owning_class = getattr(module, class_name)
        target = inspect.getattr_static(owning_class, attr)
        # Unwrap staticmethod/classmethod descriptors to the underlying function for signature read.
        underlying = getattr(target, "__func__", target)
        try:
            signature = inspect.signature(underlying)
        except (TypeError, ValueError):
            signature = None
        return ResolvedCallable(
            target=target,
            qualname=qualname,
            is_class_bound=True,
            owning_class=owning_class,
            signature=signature,
        )
    target = getattr(module, qualname)
    try:
        signature = inspect.signature(target)
    except (TypeError, ValueError):
        signature = None
    return ResolvedCallable(
        target=target,
        qualname=qualname,
        is_class_bound=False,
        owning_class=None,
        signature=signature,
    )


# A per-escape invoker performs the signature-adaptive in-process call and returns a ReplayResult.
ReplayInvoker = Callable[[ReplayEscape, Path], ReplayResult]


@dataclass(frozen=True)
class InProcessReplayExecutor:
    """Default ``ReplayExecutor`` that delegates per-escape, signature-adaptive invocation.

    ``invokers`` maps ``escape_id`` -> an invoker (supplied by the per-escape Phase 4 runners, which
    know each target's pre-fix signature and resolve it via :func:`resolve_callable` FIRST). The
    executor is the thin spawn -> observe wrapper: it dispatches to the invoker and folds any raised
    exception into a ``VERDICT_ERROR`` :class:`ReplayResult` (mirroring ``run_eval`` classifying a
    raised executor as ``ERRORED``), so a single broken replay never aborts the aggregation.
    """

    invokers: Mapping[str, ReplayInvoker] = field(default_factory=dict)

    def replay(self, escape: ReplayEscape, worktree: Path) -> ReplayResult:
        invoker = self.invokers.get(escape.escape_id)
        if invoker is None:
            return ReplayResult(
                escape_id=escape.escape_id,
                verdict=VERDICT_ERROR,
                detail=f"no invoker registered for {escape.escape_id}",
            )
        try:
            return invoker(escape, Path(worktree))
        except Exception as exc:  # noqa: BLE001 - executor folds any failure into ERROR
            return ReplayResult(
                escape_id=escape.escape_id,
                verdict=VERDICT_ERROR,
                detail=f"replay invoker raised {type(exc).__name__}: {exc}",
            )


class PrefixReplayError(RuntimeError):
    """Raised when a pre-fix-parent subprocess replay exits non-zero or emits no JSON observable."""


def run_prefix_replay_snippet(
    parent_sha: str,
    snippet: str,
    *,
    scratch_root: str | Path | None = None,
    timeout: int = 120,
) -> dict[str, Any]:
    """Replay ``snippet`` against the PRE-FIX-PARENT tree and return its JSON observable.

    Checks out ``parent_sha`` into a throwaway detached worktree (via ``checkout_worktree`` -- bare
    sha, NO caret per G1), then runs ``snippet`` in a FRESH subprocess whose ``sys.path[0]`` is the
    worktree's ``src/`` so ``import superclaude...`` loads the PRE-FIX code from the parent tree, NOT
    the live editable install. A prelude purges any inherited ``superclaude`` modules first. This is
    the real, isolated in-process invocation of the pre-fix callable (no Claude PTY -- per NFR-3).

    The ``snippet`` MUST print exactly one JSON object as its LAST stdout line (the observed result);
    this returns the parsed dict. Raises :class:`PrefixReplayError` on non-zero exit or no JSON.
    """
    with checkout_worktree(parent_sha, scratch_root=scratch_root) as wt:
        src = str(Path(wt) / "src")
        prelude = (
            "import sys, json\n"
            f"sys.path.insert(0, {src!r})\n"
            "for _m in list(sys.modules):\n"
            "    if _m == 'superclaude' or _m.startswith('superclaude.'):\n"
            "        del sys.modules[_m]\n"
        )
        proc = _subprocess.run(
            [sys.executable, "-c", prelude + snippet],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(wt),
        )
    if proc.returncode != 0:
        raise PrefixReplayError(
            f"prefix replay against {parent_sha} exited {proc.returncode}: {proc.stderr.strip()}"
        )
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    if not lines:
        raise PrefixReplayError(
            f"prefix replay against {parent_sha} produced no stdout; stderr={proc.stderr.strip()}"
        )
    try:
        return json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        raise PrefixReplayError(
            f"prefix replay against {parent_sha} last stdout line is not JSON: {lines[-1]!r}"
        ) from exc
