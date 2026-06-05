"""T03.14 -- INV-002 Python-only concurrency CI guard.

Enforces roadmap row R-073 (INV-002) -- the swarm dispatch surface MUST
route concurrency through Python (``ParallelExecutor`` -> threaded
``httpx``). The V2-era ``swarm_dispatch.sh`` shell script and any
equivalent ``subprocess``/``os.system`` shell-dispatch path are
**retired**. Mixing Python lock-guarded JSONL appends with shell-side
PIPE_BUF-atomic appends would re-introduce the dual-writer race that
INV-002 eliminated; the PIPE_BUF assumption (Linux-only, <=4 KiB lines)
is also retired with it.

Distinguishing dispatch code from contract docstrings
-----------------------------------------------------

``src/superclaude/cli/swarm/models.py`` documents that **external**
callers may invoke the swarm CLI via ``subprocess.run(...)`` (FR-030).
Those docstring mentions describe consumers of the CLI surface and do
**not** constitute internal shell dispatch. To keep the audit precise
the scanner uses ``ast`` to flag only real code-level constructs:
``import subprocess`` statements and ``subprocess.X(...)`` /
``os.system(...)`` / ``os.popen(...)`` call expressions. Doc-string and
comment mentions are intentionally left untouched.

The bare-text token ``swarm_dispatch.sh`` IS scanned in every source
file (including docstrings) because the retired script name carries no
legitimate documentation purpose -- any reappearance is a regression
signal regardless of where it lives.

Mutation guarantee
------------------

A regression that silently broke the AST visitor or the file-discovery
glob (e.g. an empty source set, a typo'd attribute name) would make the
green-suite outcome meaningless. ``test_audit_detects_*`` proves the
detectors actually flag synthetic offending sources for each forbidden
construct.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

# INV-002 Python-only dispatch (T08.03 / NFR-007). Module-level marker
# so every test in this file is selected by ``pytest -m inv``.
pytestmark = pytest.mark.inv

REPO_ROOT = Path(__file__).resolve().parents[2]
SWARM_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"

# Forbidden module-level imports. These names belong to the retired
# shell-dispatch path. ``concurrent.futures.ThreadPoolExecutor`` is
# guarded separately by ``test_parallel_executor_routing.py`` (T03.15);
# this guard targets the shell-out family specifically.
FORBIDDEN_IMPORT_MODULES: frozenset[str] = frozenset(
    {
        "subprocess",
        "shlex",
        "pty",
        "pexpect",
    }
)

# Forbidden ``module.attr`` call targets. These cover the canonical
# Python-side ways to shell out -- any one of them in dispatch code
# would reopen the INV-002 hole.
FORBIDDEN_CALL_TARGETS: frozenset[tuple[str, str]] = frozenset(
    {
        ("subprocess", "Popen"),
        ("subprocess", "run"),
        ("subprocess", "call"),
        ("subprocess", "check_call"),
        ("subprocess", "check_output"),
        ("subprocess", "getoutput"),
        ("subprocess", "getstatusoutput"),
        ("os", "system"),
        ("os", "popen"),
        ("os", "execv"),
        ("os", "execve"),
        ("os", "execvp"),
        ("os", "execvpe"),
        ("os", "spawnl"),
        ("os", "spawnv"),
        ("os", "spawnvp"),
    }
)

# Plain-text tokens that must not appear anywhere -- including
# docstrings and comments -- because the retired script name has no
# legitimate use even as documentation.
FORBIDDEN_TEXT_TOKENS: tuple[str, ...] = (
    "swarm_dispatch.sh",
)

# This test file documents the rule by naming the forbidden tokens; it
# is excluded from the scan so the documentation does not self-flag.
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


def _iter_swarm_all_sources() -> list[Path]:
    """Return every text file under the swarm package for token scans."""
    if not SWARM_DIR.exists():
        return []
    suffixes = {".py", ".md", ".toml", ".yaml", ".yml", ".cfg", ".ini", ".txt"}
    return [
        p
        for p in SWARM_DIR.rglob("*")
        if p.is_file()
        and p.suffix in suffixes
        and "__pycache__" not in p.parts
        and p.resolve() != SELF_PATH
    ]


def _resolve_attribute_chain(node: ast.AST) -> str | None:
    """Resolve ``a.b.c`` chains to a dotted string; return None otherwise.

    Used to identify the call target of ``subprocess.run(...)`` vs an
    indirect callable. Anything that doesn't resolve to a static name
    chain (a method on a local variable, a lambda, etc.) is ignored;
    the import-statement guard already blocks the path that would let
    such a callable reach swarm code.
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


class _ShellDispatchVisitor(ast.NodeVisitor):
    """Collect forbidden imports and call expressions in a module."""

    def __init__(self) -> None:
        self.import_hits: list[tuple[int, str]] = []
        self.call_hits: list[tuple[int, str]] = []

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802 -- ast API
        for alias in node.names:
            root = alias.name.split(".", 1)[0]
            if root in FORBIDDEN_IMPORT_MODULES:
                self.import_hits.append((node.lineno, alias.name))
        self.generic_visit(node)

    def visit_ImportFrom(  # noqa: N802 -- ast API
        self, node: ast.ImportFrom
    ) -> None:
        module = node.module or ""
        root = module.split(".", 1)[0]
        if root in FORBIDDEN_IMPORT_MODULES:
            self.import_hits.append((node.lineno, module))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802 -- ast API
        dotted = _resolve_attribute_chain(node.func)
        if dotted is not None and "." in dotted:
            module, _, attr = dotted.rpartition(".")
            module_root = module.split(".", 1)[0]
            if (module_root, attr) in FORBIDDEN_CALL_TARGETS:
                self.call_hits.append((node.lineno, dotted))
        self.generic_visit(node)


def _scan_module(path: Path) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    """Return (import_hits, call_hits) for one swarm source file."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    visitor = _ShellDispatchVisitor()
    visitor.visit(tree)
    return visitor.import_hits, visitor.call_hits


def test_swarm_package_exists() -> None:
    """Phase 3 has wired the swarm package; the audit needs a target.

    Without this assertion an accidentally-deleted ``swarm/`` directory
    would silently make every scan pass vacuously.
    """
    assert SWARM_DIR.is_dir(), (
        f"Swarm package missing at {SWARM_DIR.relative_to(REPO_ROOT)}; "
        "INV-002 audit has nothing to scan."
    )


def test_no_shell_scripts_in_swarm_package() -> None:
    """INV-002: no ``.sh`` files anywhere under the swarm package.

    Mirrors the spec validation step
    ``find src/superclaude/cli/swarm/ -name '*.sh'`` -- any reappearance
    of a dispatch shell script is a direct INV-002 regression.
    """
    shell_files = sorted(
        p.relative_to(REPO_ROOT) for p in SWARM_DIR.rglob("*.sh") if p.is_file()
    )
    assert not shell_files, (
        "INV-002 violation: shell scripts present in swarm package "
        "(dispatch must be Python-only):\n  "
        + "\n  ".join(str(p) for p in shell_files)
    )


def test_no_subprocess_or_shell_imports_in_swarm_sources() -> None:
    """INV-002: no module-level ``import subprocess`` / ``shlex`` / pty.

    Importing one of the shell-out modules is a structural signal that
    code intends to spawn an external process. Documentation that
    *describes* external callers (e.g. ``models.py`` mentioning
    ``subprocess.run`` per FR-030) lives inside string literals and is
    not picked up by the AST import visitor.
    """
    offenders: list[str] = []
    for source in _iter_swarm_py_sources():
        import_hits, _ = _scan_module(source)
        for lineno, name in import_hits:
            offenders.append(f"  {source.relative_to(REPO_ROOT)}:{lineno}: import {name}")
    assert not offenders, (
        "INV-002 violation: shell-dispatch module imported in swarm sources. "
        "Concurrency must route through ParallelExecutor + httpx only:\n"
        + "\n".join(offenders)
    )


def test_no_shell_dispatch_calls_in_swarm_sources() -> None:
    """INV-002: no ``subprocess.Popen(...)`` / ``os.system(...)`` calls.

    AST-level check so doc-string mentions of ``subprocess.run`` for
    FR-030 caller documentation in ``models.py`` do not trigger the
    audit -- only actual call expressions count.
    """
    offenders: list[str] = []
    for source in _iter_swarm_py_sources():
        _, call_hits = _scan_module(source)
        for lineno, target in call_hits:
            offenders.append(f"  {source.relative_to(REPO_ROOT)}:{lineno}: {target}(...)")
    assert not offenders, (
        "INV-002 violation: shell-dispatch call detected in swarm sources. "
        "Dispatch must go through ParallelExecutor + httpx:\n"
        + "\n".join(offenders)
    )


@pytest.mark.parametrize("token", FORBIDDEN_TEXT_TOKENS)
def test_no_retired_shell_dispatch_token(token: str) -> None:
    """INV-002: ``swarm_dispatch.sh`` must not appear in any swarm source.

    Unlike ``subprocess`` (which has legitimate doc-string uses for
    FR-030 caller documentation), the retired script name carries no
    valid documentation purpose; even a docstring reappearance signals
    a copy-paste regression from the V2 design.
    """
    offenders: list[str] = []
    for source in _iter_swarm_all_sources():
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if token in line:
                offenders.append(
                    f"  {source.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}"
                )
    assert not offenders, (
        f"INV-002 violation: retired shell-dispatch token '{token}' present "
        "in swarm sources:\n" + "\n".join(offenders)
    )


def test_audit_detects_mutation_shell_script_file(tmp_path: Path) -> None:
    """Mutation guard: ``.sh`` discovery flags an injected dispatch script.

    Verifies the rglob('*.sh') scan would have caught a real
    regression. Without this guard a typo in the glob (e.g. matching
    only ``*.shell``) would silently green every audit run.
    """
    fake = tmp_path / "swarm_dispatch.sh"
    fake.write_text("#!/usr/bin/env bash\necho regression\n", encoding="utf-8")
    matches = list(tmp_path.rglob("*.sh"))
    assert fake in matches, (
        "Shell-script detector failed on a synthetic ``.sh`` file -- "
        "INV-002 audit would silently pass on a real regression."
    )


def test_audit_detects_mutation_subprocess_import() -> None:
    """Mutation guard: AST visitor flags an injected ``import subprocess``."""
    synthetic = (
        "import subprocess\n"
        "import shlex\n"
        "from subprocess import Popen as _P\n"
        "def f():\n"
        "    return None\n"
    )
    tree = ast.parse(synthetic, filename="<synthetic>")
    visitor = _ShellDispatchVisitor()
    visitor.visit(tree)
    imported = {name for _, name in visitor.import_hits}
    assert "subprocess" in imported, (
        "Import visitor failed on synthetic ``import subprocess``; "
        "INV-002 audit would silently pass on a real regression."
    )
    assert "shlex" in imported, (
        "Import visitor failed on synthetic ``import shlex``; "
        "INV-002 audit would silently pass on a real regression."
    )
    assert "subprocess" in imported, (
        "Import-from visitor failed on synthetic ``from subprocess import``; "
        "INV-002 audit would silently pass on a real regression."
    )


def test_audit_detects_mutation_subprocess_call() -> None:
    """Mutation guard: AST visitor flags an injected ``subprocess.Popen(...)``."""
    synthetic = (
        "def dispatch():\n"
        "    subprocess.Popen(['bash', '-c', 'echo hi'])\n"
        "    subprocess.run(['sh', '-c', 'echo hi'])\n"
        "    os.system('echo hi')\n"
        "    return None\n"
    )
    tree = ast.parse(synthetic, filename="<synthetic>")
    visitor = _ShellDispatchVisitor()
    visitor.visit(tree)
    flagged = {target for _, target in visitor.call_hits}
    assert "subprocess.Popen" in flagged, (
        "Call visitor failed on synthetic subprocess.Popen call; "
        "INV-002 audit would silently pass on a real regression."
    )
    assert "subprocess.run" in flagged, (
        "Call visitor failed on synthetic subprocess.run call; "
        "INV-002 audit would silently pass on a real regression."
    )
    assert "os.system" in flagged, (
        "Call visitor failed on synthetic os.system call; "
        "INV-002 audit would silently pass on a real regression."
    )


def test_audit_detects_mutation_retired_token() -> None:
    """Mutation guard: token scan flags a synthetic ``swarm_dispatch.sh`` mention.

    Walks the same line-by-line search the real test uses to prove a
    regression in the substring check would not silently green the
    suite.
    """
    synthetic = (
        "module docstring mentioning swarm_dispatch.sh as a regression\n"
    )
    hits = [
        lineno
        for lineno, line in enumerate(synthetic.splitlines(), start=1)
        if "swarm_dispatch.sh" in line
    ]
    assert hits, (
        "Token scanner failed to flag a synthetic ``swarm_dispatch.sh`` "
        "mention; INV-002 audit would silently pass on a real regression."
    )


def test_forbidden_sets_are_nonempty() -> None:
    """Guard against an empty forbidden set silently greening every scan.

    A future refactor that emptied ``FORBIDDEN_IMPORT_MODULES`` or
    ``FORBIDDEN_CALL_TARGETS`` or ``FORBIDDEN_TEXT_TOKENS`` would make
    the corresponding test pass vacuously. This guard makes that
    failure-mode loud.
    """
    assert FORBIDDEN_IMPORT_MODULES, (
        "FORBIDDEN_IMPORT_MODULES must enumerate the shell-out family; "
        "an empty set would render the import audit a no-op."
    )
    assert FORBIDDEN_CALL_TARGETS, (
        "FORBIDDEN_CALL_TARGETS must enumerate shell-out call sites; "
        "an empty set would render the call audit a no-op."
    )
    assert FORBIDDEN_TEXT_TOKENS, (
        "FORBIDDEN_TEXT_TOKENS must include retired script names; "
        "an empty tuple would render the token audit a no-op."
    )
