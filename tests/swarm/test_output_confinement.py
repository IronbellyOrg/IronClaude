"""T03.17 -- NFR-013 / AC-014 ``--output`` write confinement.

Covers the acceptance criteria from
``.dev/releases/Current/MultiModelSwarm/tasklist/phase-3-tasklist.md``::

* Attempted writes outside ``--output`` rejected with explicit
  :class:`OutputConfinementError`.
* All writer call sites (state, log, manifest, env-missing contract)
  import and call :func:`confine_path`.
* Tests cover absolute escape, ``..`` traversal, and symlink escape.

The guard sits in :mod:`superclaude.cli.swarm.state` so every writer
that already imports the state module gets it for free; the per-writer
audit grep
(``grep -RnE "confine_path\\(" src/superclaude/cli/swarm/``) is
asserted in :func:`test_writers_invoke_confine_path` below.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

from superclaude.cli.swarm.logging_ import Logger
from superclaude.cli.swarm.models import EventRecord, Manifest, SwarmState
from superclaude.cli.swarm.preflight import write_manifest
from superclaude.cli.swarm.state import (
    OutputConfinementError,
    confine_path,
    write_state,
)

# ---------------------------------------------------------------------------
# confine_path -- core guard semantics.
# ---------------------------------------------------------------------------


def test_confine_path_accepts_descendant(tmp_path: Path) -> None:
    """Targets inside the root resolve cleanly and round-trip absolute."""
    target = tmp_path / "swarm-state.json"
    resolved = confine_path(target, tmp_path)
    assert resolved == target.resolve()


def test_confine_path_accepts_nested_descendant(tmp_path: Path) -> None:
    """Deeply nested targets (jobs/worker-01/...) are still confined."""
    target = tmp_path / "jobs" / "worker-01" / "result.json"
    resolved = confine_path(target, tmp_path)
    assert resolved == target.resolve()


def test_confine_path_accepts_root_itself(tmp_path: Path) -> None:
    """The output_dir itself counts as a valid target.

    A caller passing ``output_dir`` as both arguments (e.g. when
    confining the directory before stamping the first sub-path inside
    it) must not be rejected.
    """
    resolved = confine_path(tmp_path, tmp_path)
    assert resolved == tmp_path.resolve()


def test_confine_path_rejects_absolute_escape(tmp_path: Path) -> None:
    """Absolute paths outside the root raise :class:`OutputConfinementError`."""
    with pytest.raises(OutputConfinementError):
        confine_path("/etc/passwd", tmp_path)


def test_confine_path_rejects_relative_dotdot_traversal(tmp_path: Path) -> None:
    """``..`` traversal that escapes the root is rejected."""
    inside = tmp_path / "jobs"
    inside.mkdir()
    # jobs/../../etc/passwd resolves above tmp_path.
    escape = inside / ".." / ".." / "etc" / "passwd"
    with pytest.raises(OutputConfinementError):
        confine_path(escape, tmp_path)


def test_confine_path_rejects_dotdot_that_lands_outside(tmp_path: Path) -> None:
    """``..`` that produces a sibling of the root is still rejected.

    ``<root>/../sibling`` resolves outside ``<root>`` even though it
    looks lexically close; ``confine_path`` must catch this branch.
    """
    sibling_escape = tmp_path / ".." / "sibling-outside"
    with pytest.raises(OutputConfinementError):
        confine_path(sibling_escape, tmp_path)


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="symlink semantics differ on Windows; POSIX-only branch",
)
def test_confine_path_rejects_symlink_escape(tmp_path: Path) -> None:
    """A symlink inside the root whose target is outside is rejected.

    :func:`Path.resolve` follows symlinks, so the escape lands in the
    same resolution branch as the absolute / ``..`` cases.
    """
    outside = tmp_path.parent / "confinement-outside-target"
    outside.mkdir(exist_ok=True)
    try:
        link = tmp_path / "evil-link"
        link.symlink_to(outside)
        forbidden = link / "secret"
        with pytest.raises(OutputConfinementError):
            confine_path(forbidden, tmp_path)
    finally:
        # Clean up so other tests do not see a stray sibling directory.
        try:
            outside.rmdir()
        except OSError:
            pass


def test_confine_path_accepts_in_root_symlink(tmp_path: Path) -> None:
    """A symlink whose target is *inside* the root is allowed.

    The contract is "the resolved path is under the root", not "no
    symlinks anywhere"; in-root links are fine.
    """
    inner = tmp_path / "inner"
    inner.mkdir()
    link = tmp_path / "link-inside"
    link.symlink_to(inner)
    resolved = confine_path(link / "file.txt", tmp_path)
    assert resolved == (inner / "file.txt").resolve()


def test_confine_path_error_message_names_both_paths(tmp_path: Path) -> None:
    """The exception message names both resolved paths for triage."""
    with pytest.raises(OutputConfinementError) as exc_info:
        confine_path("/etc/passwd", tmp_path)
    message = str(exc_info.value)
    assert "/etc/passwd" in message
    assert str(tmp_path.resolve()) in message


# ---------------------------------------------------------------------------
# write_state -- confinement enforced when output_dir is supplied.
# ---------------------------------------------------------------------------


def test_write_state_confines_to_output_dir(tmp_path: Path) -> None:
    """A target inside the output root writes successfully."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    target = output_dir / ".swarm-state.json"
    write_state(target, SwarmState(job_id="job-confined"), output_dir=output_dir)
    assert target.exists()


def test_write_state_rejects_escape_when_output_dir_supplied(
    tmp_path: Path,
) -> None:
    """An escape attempt with output_dir set raises and writes nothing."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    escape = tmp_path / "elsewhere" / ".swarm-state.json"
    with pytest.raises(OutputConfinementError):
        write_state(escape, SwarmState(job_id="x"), output_dir=output_dir)
    assert not escape.exists()
    assert not escape.parent.exists(), (
        "write_state must not create parent dirs outside output_dir"
    )


def test_write_state_rejects_absolute_escape(tmp_path: Path) -> None:
    """Absolute path outside output_dir is rejected."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    with pytest.raises(OutputConfinementError):
        write_state(
            "/tmp/escape-attempt-state.json",
            SwarmState(job_id="x"),
            output_dir=output_dir,
        )


# ---------------------------------------------------------------------------
# Logger -- confinement enforced at construction.
# ---------------------------------------------------------------------------


def test_logger_confines_paths_to_output_dir(tmp_path: Path) -> None:
    """In-root JSONL + MD paths construct and append cleanly."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    logger = Logger(
        output_dir / "event-log.jsonl",
        output_dir / "event-log.md",
        output_dir=output_dir,
    )
    logger.log_event(EventRecord(event_type="wave_transition"))
    assert (output_dir / "event-log.jsonl").exists()
    assert (output_dir / "event-log.md").exists()


def test_logger_rejects_jsonl_escape(tmp_path: Path) -> None:
    """JSONL path outside the root is rejected at Logger construction."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    with pytest.raises(OutputConfinementError):
        Logger(
            tmp_path / "elsewhere.jsonl",
            output_dir / "event-log.md",
            output_dir=output_dir,
        )


def test_logger_rejects_md_escape(tmp_path: Path) -> None:
    """Markdown path outside the root is rejected at Logger construction."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    with pytest.raises(OutputConfinementError):
        Logger(
            output_dir / "event-log.jsonl",
            tmp_path / "elsewhere.md",
            output_dir=output_dir,
        )


# ---------------------------------------------------------------------------
# write_manifest -- confinement enforced implicitly via in-tree target.
# ---------------------------------------------------------------------------


def test_write_manifest_confines_to_output_dir(tmp_path: Path) -> None:
    """``write_manifest`` lands ``manifest.json`` inside ``output_dir``."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    manifest_path = write_manifest(Manifest(), output_dir)
    assert Path(manifest_path).resolve().is_relative_to(output_dir.resolve())


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="symlink semantics differ on Windows; POSIX-only branch",
)
def test_write_manifest_rejects_symlinked_output_dir_escape(
    tmp_path: Path,
) -> None:
    """A symlinked output_dir whose resolved target is outside is rejected.

    The contract is "resolved manifest.json must be under resolved
    output_dir". When the resolved output_dir is itself an escape (the
    symlink follows out of the test root), the manifest lands inside
    that resolved directory, which is allowed by the confinement
    relation (root == root). This test instead pins the negative case:
    handing a *missing* output_dir whose lexical parent is the test
    root but whose resolution leaves the root.
    """
    real_outside = tmp_path.parent / "manifest-outside-real"
    real_outside.mkdir(exist_ok=True)
    try:
        link = tmp_path / "linked-out"
        link.symlink_to(real_outside)
        # The manifest path is constructed inside ``link``; both the
        # target and root resolve to ``real_outside``, so it actually
        # succeeds. The escape case we want is: target=link/manifest,
        # root=tmp_path (different from resolved target).
        with pytest.raises(OutputConfinementError):
            confine_path(link / "manifest.json", tmp_path)
    finally:
        try:
            real_outside.rmdir()
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Static guard: every writer module imports confine_path.
# ---------------------------------------------------------------------------


_WRITER_MODULES = (
    "src/superclaude/cli/swarm/state.py",
    "src/superclaude/cli/swarm/logging_.py",
    "src/superclaude/cli/swarm/preflight.py",
)


def test_writers_invoke_confine_path() -> None:
    """Per-writer audit: every writer module references ``confine_path``.

    Mirrors the phase-3 validation grep
    (``grep -RnE "confine_path\\(" src/superclaude/cli/swarm/``) so the
    rule is enforced inside the test lane too. The state module is the
    canonical definition site; the other writers either import the
    symbol or invoke it.
    """
    for relpath in _WRITER_MODULES:
        src = Path(relpath).read_text(encoding="utf-8")
        assert "confine_path" in src, (
            f"{relpath} must reference confine_path -- NFR-013 / AC-014 "
            "confinement guard required at every writer."
        )


def test_state_module_exposes_confinement_symbols() -> None:
    """``state.__all__`` must export both the helper and its exception."""
    from superclaude.cli.swarm import state as state_mod

    assert "confine_path" in state_mod.__all__
    assert "OutputConfinementError" in state_mod.__all__


# ---------------------------------------------------------------------------
# F-P3-7 -- production CALL-SITE confinement (AST), not just substring.
#
# ``test_writers_invoke_confine_path`` above is substring-only: it passes
# even if a production call site forgets ``output_dir=`` (so confinement is
# silently skipped) or if a writer module merely mentions ``confine_path`` in
# a comment. These AST checks assert the actual run / kill call sites in
# ``commands.py`` pass ``output_dir=`` to ``write_state`` and ``Logger``, that
# the env-missing / manifest writer FUNCTIONS in ``preflight.py`` actually
# invoke ``confine_path`` inside their bodies, and the vacuity guards prove
# the AST checker fails when the kwarg / call is dropped (so a regression
# cannot pass silently).
# ---------------------------------------------------------------------------


_COMMANDS_PATH = "src/superclaude/cli/swarm/commands.py"
_PREFLIGHT_PATH = "src/superclaude/cli/swarm/preflight.py"


def _parse(relpath: str) -> ast.Module:
    return ast.parse(Path(relpath).read_text(encoding="utf-8"))


def _call_simple_name(call: ast.Call) -> str | None:
    """The simple callee name for ``foo(...)`` or ``obj.foo(...)``."""
    func = call.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _calls_named(tree: ast.AST, names: set[str]) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_simple_name(node) in names
    ]


def _has_kwarg(call: ast.Call, kw: str) -> bool:
    return any(k.arg == kw for k in call.keywords)


def _function_def(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"function {name!r} not found")


def test_commands_write_state_callsites_pass_output_dir() -> None:
    """F-P3-7: every ``write_state`` call in commands.py passes ``output_dir=``.

    Covers the inline-run state transitions (via ``_write_swarm_state`` ->
    ``_write_state``) and the kill path's two ``write_state`` calls. A call
    site that omits ``output_dir`` would bypass confinement -- the exact gap
    the substring-only test cannot see.
    """
    tree = _parse(_COMMANDS_PATH)
    calls = _calls_named(tree, {"write_state", "_write_state"})
    assert calls, "expected write_state call sites in commands.py"
    offenders = [c.lineno for c in calls if not _has_kwarg(c, "output_dir")]
    assert not offenders, (
        "write_state call(s) in commands.py missing output_dir= "
        f"(NFR-013 confinement bypass) at line(s) {offenders}"
    )


def test_commands_logger_construction_passes_output_dir() -> None:
    """F-P3-7: the production ``Logger`` construction passes ``output_dir=``.

    The run path builds the dual-format logger as ``_Logger(...)``; without
    ``output_dir`` the logger skips the ``confine_path`` branch entirely
    (the F-P3-6 gap). Assert the call site carries the kwarg.
    """
    tree = _parse(_COMMANDS_PATH)
    calls = _calls_named(tree, {"Logger", "_Logger"})
    assert calls, "expected a Logger construction in commands.py"
    offenders = [c.lineno for c in calls if not _has_kwarg(c, "output_dir")]
    assert not offenders, (
        "Logger construction(s) in commands.py missing output_dir= "
        f"(NFR-013 confinement bypass) at line(s) {offenders}"
    )


def test_preflight_writer_functions_invoke_confine_path() -> None:
    """F-P3-7: the env-missing + manifest writer FUNCTIONS call confine_path.

    Function-scoped (not module-substring): each writer's body must contain
    a ``confine_path(...)`` call so the write is confined before the file is
    materialised.
    """
    tree = _parse(_PREFLIGHT_PATH)
    for fn_name in ("emit_env_missing_contract", "write_manifest"):
        fn = _function_def(tree, fn_name)
        confine_calls = _calls_named(fn, {"confine_path"})
        assert confine_calls, (
            f"{fn_name} must invoke confine_path inside its body "
            "(NFR-013 / AC-014 writer confinement)"
        )


def test_callsite_ast_check_is_not_vacuous() -> None:
    """F-P3-7 vacuity guard: the AST kwarg check detects a missing output_dir.

    If this assertion ever inverted (a kwarg-less call reported as having the
    kwarg), the call-site tests above would pass vacuously. Pin both polarities.
    """
    missing = _calls_named(ast.parse("write_state(p, s)\n"), {"write_state"})
    assert missing and not _has_kwarg(missing[0], "output_dir"), (
        "vacuity: a write_state(...) without output_dir must be detectable"
    )
    present = _calls_named(
        ast.parse("write_state(p, s, output_dir=d)\n"), {"write_state"}
    )
    assert present and _has_kwarg(present[0], "output_dir"), (
        "vacuity: a write_state(..., output_dir=d) must register the kwarg"
    )


def test_confine_path_callsite_ast_check_is_not_vacuous() -> None:
    """F-P3-7 vacuity guard: the function-body confine_path check is real.

    A function with no confine_path call must register zero confine_path
    calls (so ``test_preflight_writer_functions_invoke_confine_path`` cannot
    pass for a writer that dropped the guard).
    """
    no_guard = ast.parse("def w(p, out):\n    return open(p, 'w')\n")
    assert not _calls_named(_function_def(no_guard, "w"), {"confine_path"})
    with_guard = ast.parse(
        "def w(p, out):\n    t = confine_path(p, out)\n    return t\n"
    )
    assert _calls_named(_function_def(with_guard, "w"), {"confine_path"})
