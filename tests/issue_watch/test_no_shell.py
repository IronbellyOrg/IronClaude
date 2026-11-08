"""No-shell static guard for the issue watcher (NFR-004, design T6).

An AST scan of every module in ``src/superclaude/cli/issue_watch/`` that fails on:

* a ``shell=`` keyword argument whose value is not the constant ``False``;
* any call to ``os.system`` or ``os.popen`` (through ``import os``, an alias, or
  ``from os import system``);
* ``import subprocess`` or ``from subprocess import ...`` in any module other
  than ``runner.py``.

The scan reads syntax trees, so docstring and comment mentions of ``shell=False``
or ``subprocess`` do not trip it. The self-tests below feed the same scanner
small synthetic sources, one positive and one negative per forbidden form, so the
real scan cannot pass vacuously.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "issue_watch"

# The only module allowed to import ``subprocess``.
RUNNER_MODULE = "runner"
_OS_SHELL_FUNCS = frozenset({"system", "popen"})


def _dotted(node: ast.expr) -> str | None:
    """Return ``a.b.c`` for a Name/Attribute chain, else None."""
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if not isinstance(node, ast.Name):
        return None
    parts.append(node.id)
    return ".".join(reversed(parts))


def scan_source(source: str, module: str) -> list[str]:
    """Return one finding string per forbidden construct in ``source``.

    ``module`` is the module's file stem; only ``runner`` may import subprocess.
    """
    tree = ast.parse(source, filename=f"<{module}>")
    findings: list[str] = []
    os_names: set[str] = set()  # local names bound to the ``os`` module
    os_shell_names: set[str] = set()  # local names bound to os.system / os.popen

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root == "os":
                    # ``import os`` and ``import os.path`` both bind the name
                    # ``os``; ``import os.path as p`` binds ``p`` to os.path (not
                    # the os module), so only ``import os as o`` adds an alias.
                    if alias.asname is None:
                        os_names.add("os")
                    elif alias.name == "os":
                        os_names.add(alias.asname)
                if root == "subprocess" and module != RUNNER_MODULE:
                    findings.append(f"{node.lineno}: import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if node.level == 0 and root == "subprocess" and module != RUNNER_MODULE:
                findings.append(f"{node.lineno}: from {node.module} import ...")
            if node.level == 0 and node.module == "os":
                for alias in node.names:
                    if alias.name in _OS_SHELL_FUNCS:
                        os_shell_names.add(alias.asname or alias.name)
                        findings.append(f"{node.lineno}: from os import {alias.name}")

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for kw in node.keywords:
            if kw.arg == "shell" and not (
                isinstance(kw.value, ast.Constant) and kw.value.value is False
            ):
                findings.append(f"{node.lineno}: shell={ast.unparse(kw.value)}")
        target = _dotted(node.func)
        if target is None:
            continue
        head, _, tail = target.rpartition(".")
        if (head in os_names and tail in _OS_SHELL_FUNCS) or target in os_shell_names:
            findings.append(f"{node.lineno}: call to {target}")
    return findings


def _package_files(root: Path = PACKAGE_DIR) -> list[Path]:
    """Every ``.py`` file under ``root``, sub-packages included."""
    return sorted(root.rglob("*.py"))


def _module_name(path: Path, root: Path = PACKAGE_DIR) -> str:
    """``runner`` for ``root/runner.py``; ``sub.runner`` for ``root/sub/runner.py``.

    A nested file never equals ``runner``, so it gets no subprocess exemption.
    """
    return ".".join(path.relative_to(root).with_suffix("").parts)


def scan_tree(root: Path = PACKAGE_DIR) -> list[str]:
    """Findings of ``scan_source`` over every module under ``root``."""
    offenders: list[str] = []
    for path in _package_files(root):
        source = path.read_text(encoding="utf-8")
        for finding in scan_source(source, _module_name(path, root)):
            offenders.append(f"  {path.relative_to(root)}:{finding}")
    return offenders


def subprocess_importers(root: Path = PACKAGE_DIR) -> set[str]:
    """Module names under ``root`` that import ``subprocess`` in any spelling."""
    importers: set[str] = set()
    for path in _package_files(root):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) and any(
                a.name.split(".")[0] == "subprocess" for a in node.names
            ):
                importers.add(_module_name(path, root))
            if (
                isinstance(node, ast.ImportFrom)
                and (node.module or "").split(".")[0] == "subprocess"
            ):
                importers.add(_module_name(path, root))
    return importers


# ---------------------------------------------------------------------------
# The real scan
# ---------------------------------------------------------------------------


def test_scan_covers_the_package_and_only_the_package() -> None:
    files = _package_files()
    names = {p.name for p in files}
    assert PACKAGE_DIR.is_dir()
    assert {"runner.py", "cycle.py", "cli.py", "github.py", "launch.py"} <= names
    # Every file the scan reads lies inside the package directory.
    assert all(PACKAGE_DIR in p.parents for p in files)


def test_no_shell_forms_in_issue_watch_package() -> None:
    """AC-21, NFR-004: no shell=True or other shell form appears in the package."""
    offenders = scan_tree()
    assert not offenders, "NFR-004 violation (no shell):\n" + "\n".join(offenders)


def test_runner_is_the_only_subprocess_importer() -> None:
    """AC-21, NFR-004: only runner.py imports subprocess."""
    assert subprocess_importers() == {RUNNER_MODULE}


def _write_tree(root: Path, files: dict[str, str]) -> None:
    for rel, source in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source, encoding="utf-8")


def test_tree_scan_reaches_a_sub_package_module(tmp_path: Path) -> None:
    """A shell form or a subprocess import in a nested module is reported."""
    _write_tree(
        tmp_path,
        {
            "runner.py": "import subprocess\n",
            "sub/__init__.py": "",
            "sub/x.py": 'import subprocess\nsubprocess.run(["x"], shell=True)\n',
            "sub/y.py": 'import os\nos.system("x")\n',
            "sub/runner.py": "import subprocess\n",
        },
    )
    offenders = "\n".join(scan_tree(tmp_path))
    assert "sub/x.py:1: import subprocess" in offenders
    assert "sub/x.py:2: shell=True" in offenders
    assert "sub/y.py:2: call to os.system" in offenders
    assert "sub/runner.py:1: import subprocess" in offenders  # not the runner module
    assert subprocess_importers(tmp_path) == {"runner", "sub.x", "sub.runner"}


def test_tree_scan_is_clean_for_a_clean_tree(tmp_path: Path) -> None:
    _write_tree(
        tmp_path,
        {"runner.py": "import subprocess\n", "sub/ok.py": "import os\nos.getpid()\n"},
    )
    assert scan_tree(tmp_path) == []
    assert subprocess_importers(tmp_path) == {"runner"}


# ---------------------------------------------------------------------------
# Mutation guards: the scanner flags each forbidden form (positive) and leaves
# the look-alike alone (negative).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("source", "module"),
    [
        ('import subprocess\nsubprocess.run(["x"], shell=True)\n', "runner"),
        ('def f(flag):\n    run(["x"], shell=flag)\n', "cycle"),
        ('run(["x"], shell=1)\n', "cycle"),
        ('run(["x"], shell="false")\n', "cycle"),
        ('os_like(["x"], shell=True)\n', "runner"),
        ('import os\nos.system("x")\n', "cycle"),
        ('import os\nos.popen("x")\n', "cycle"),
        ('import os as o\no.system("x")\n', "cycle"),
        ('from os import system\nsystem("x")\n', "cycle"),
        ('from os import popen as p\np("x")\n', "cycle"),
        ('import os.path\nos.system("x")\n', "cycle"),
        ('import os.path\nos.popen("x")\n', "cycle"),
        ('import sys, os.path\nos.system("x")\n', "cycle"),
        ('import os.path as p\nimport os\nos.system("x")\n', "cycle"),
        ('from os import path\nimport os.path\nos.system("x")\n', "cycle"),
        ('import os.path\nimport os as o\no.system("x")\n', "cycle"),
        ("import subprocess\n", "cycle"),
        ("import subprocess as sp\n", "github"),
        ("import subprocess.something\n", "cli"),
        ("from subprocess import run\n", "launch"),
        ("from subprocess import run as r, PIPE\n", "record"),
    ],
)
def test_scanner_flags_forbidden_form(source: str, module: str) -> None:
    assert scan_source(source, module), source


@pytest.mark.parametrize(
    ("source", "module"),
    [
        ('"""Never uses shell=True, os.system or subprocess."""\n', "cycle"),
        ('# import subprocess; os.system("x"); shell=True\nx = 1\n', "cycle"),
        ("x = \"os.system('rm') shell=True import subprocess\"\n", "cycle"),
        ('import subprocess\nsubprocess.run(["x"], shell=False)\n', "runner"),
        ("from subprocess import run\n", "runner"),
        ('run(["x"], shell=False)\n', "cycle"),
        ('import os\nos.path.join("a", "b")\nos.getpid()\n', "cycle"),
        ("import os\nos.environ.get('A')\n", "cycle"),
        ("from os import path\n", "cycle"),
        ('import os.path\nos.path.join("a", "b")\nos.getpid()\n', "cycle"),
        ('import os.path as p\np.join("a", "b")\n', "cycle"),
        ('from os import path\npath.join("a", "b")\n', "cycle"),
        ("from . import subprocess_helper\n", "cycle"),
        ("subprocess = None\nsystem = 1\nsystem\n", "cycle"),
        ('def system(x):\n    return x\nsystem("x")\n', "cycle"),
    ],
)
def test_scanner_leaves_lookalike_alone(source: str, module: str) -> None:
    assert scan_source(source, module) == [], source


def test_scanner_flags_shell_true_even_in_runner() -> None:
    """The runner may import subprocess but still may not use shell=True."""
    source = 'import subprocess\nsubprocess.run(["x"], shell=True)\n'
    assert any("shell=True" in f for f in scan_source(source, RUNNER_MODULE))
    assert not any("import" in f for f in scan_source(source, RUNNER_MODULE))


def test_scanner_names_the_import_in_a_non_runner_module() -> None:
    findings = scan_source("import subprocess\n", "not_runner")
    assert findings == ["1: import subprocess"]
