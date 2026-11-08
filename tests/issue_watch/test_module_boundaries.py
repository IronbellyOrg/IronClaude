"""Import-graph boundaries of ``superclaude.cli.issue_watch`` (NFR-014, AC-25).

Design section 5.3 lists, per module, what it may import. This test parses every
module with ``ast`` and fails on any other import. Three details matter:

* imports come in two spellings of the same thing (``from . import cycle``,
  ``from .cycle import x`` and ``from superclaude.cli.issue_watch.cycle import x``)
  and are all resolved to one absolute dotted name before they are checked;
* the whole tree is walked, so an import inside a function or under
  ``TYPE_CHECKING`` counts (DF-29: ``record`` imports ``write_prepared_bytes``
  inside a function, ``fcntl`` is imported inside a function);
* the scan is proven to fail on a forbidden import by feeding the same walker
  synthetic sources (positive and negative), so it cannot pass vacuously.

Rule encoded where the code and the design wording differ:

* ``superclaude.cli.swarm.atomic`` may be imported by ``record`` inside any
  function (``FileStore.save`` and ``save_dry_run`` both do), never at module level.
  Design C18 says "inside ``save``".
* ``record`` may import any name from ``predicates`` (it imports three functions
  and one type); design 5.3 says "types only". The rule is checked per module.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePath

import pytest

PACKAGE = "superclaude.cli.issue_watch"
PACKAGE_DIR = Path(__file__).resolve().parents[2] / "src/superclaude/cli/issue_watch"
ATOMIC = "superclaude.cli.swarm.atomic"
INSTALL_USER_SETUP = "superclaude.cli.install_user_setup"
EXPECTED_PROTOCOLS = {"Runner", "Store", "Launcher", "Clock"}


@dataclass(frozen=True)
class Rule:
    """What one module may import besides the standard library."""

    siblings: frozenset[str] = frozenset()
    superclaude: frozenset[str] = frozenset()  # exact module targets
    third_party: frozenset[str] = frozenset()  # top-level distribution names
    function_only: frozenset[str] = frozenset()  # targets never at module level
    names_only: dict[str, frozenset[str]] = field(default_factory=dict)


RULES: dict[str, Rule] = {
    "__init__": Rule(),
    "runner": Rule(),
    "predicates": Rule(),
    "audit": Rule(),
    "github": Rule(siblings=frozenset({"runner", "predicates"})),
    "record": Rule(
        siblings=frozenset({"predicates"}),
        superclaude=frozenset({ATOMIC}),
        function_only=frozenset({ATOMIC}),
    ),
    "launch": Rule(
        siblings=frozenset({"runner"}),
        superclaude=frozenset({INSTALL_USER_SETUP}),
        names_only={INSTALL_USER_SETUP: frozenset({"_ORCA_CLIS"})},
    ),
    "cycle": Rule(
        siblings=frozenset(
            {"runner", "github", "predicates", "record", "launch", "audit"}
        )
    ),
    "cli": Rule(
        siblings=frozenset({"cycle", "record", "audit", "launch", "runner"}),
        third_party=frozenset({"click"}),
    ),
}


@dataclass(frozen=True)
class Imp:
    """One imported module, resolved to an absolute dotted name."""

    module: str
    names: tuple[str, ...] | None  # None for a plain ``import x``
    in_function: bool
    lineno: int


class _Collector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.imports: list[Imp] = []
        self.depth = 0

    def _function(self, node: ast.AST) -> None:
        self.depth += 1
        self.generic_visit(node)
        self.depth -= 1

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._function(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.append(Imp(alias.name, None, self.depth > 0, node.lineno))

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        parts = node.module.split(".") if node.module else []
        if node.level:  # level 1 is this package, level 2 its parent, and so on
            pkg = PACKAGE.split(".")
            parts = pkg[: len(pkg) - (node.level - 1)] + parts
        target = ".".join(parts)
        names = tuple(a.name for a in node.names)
        in_function = self.depth > 0
        if target == PACKAGE:
            # ``from . import cycle``: each name is a sibling module.
            for name in names:
                self.imports.append(
                    Imp(f"{PACKAGE}.{name}", (), in_function, node.lineno)
                )
        else:
            self.imports.append(Imp(target, names, in_function, node.lineno))


def collect_imports(source: str, filename: str = "<source>") -> list[Imp]:
    """Every import in ``source`` (module level, function level, any block)."""
    collector = _Collector()
    collector.visit(ast.parse(source, filename=filename))
    return collector.imports


def violations(module: str, imports: list[Imp], rule: Rule) -> list[str]:
    """Human-readable breaches of ``rule`` by ``module``'s imports."""
    out: list[str] = []
    for imp in imports:
        where = f"{module}.py:{imp.lineno}: {imp.module}"
        top = imp.module.split(".")[0]
        if imp.module == PACKAGE or imp.module.startswith(PACKAGE + "."):
            sibling = imp.module[len(PACKAGE) + 1 :].split(".")[0]
            if sibling not in rule.siblings:
                out.append(f"{where} (sibling not allowed)")
        elif top == "superclaude":
            if imp.module not in rule.superclaude:
                out.append(f"{where} (superclaude import not allowed)")
                continue
            if imp.module in rule.function_only and not imp.in_function:
                out.append(f"{where} (must be imported inside a function)")
            only = rule.names_only.get(imp.module)
            if only is not None and (imp.names is None or not set(imp.names) <= only):
                out.append(f"{where} (only {sorted(only)} may be imported)")
        elif top in sys.stdlib_module_names:
            if top == "fcntl" and not imp.in_function:
                out.append(f"{where} (fcntl must be imported inside a function)")
        elif top not in rule.third_party:
            out.append(f"{where} (third-party import not allowed)")
    return out


def protocol_class_names(source: str) -> list[str]:
    """Names of classes that list ``Protocol`` (or ``typing.Protocol``) as a base."""
    names = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.ClassDef):
            continue
        for base in node.bases:
            if isinstance(base, ast.Subscript):
                base = base.value
            tail = (
                base.attr
                if isinstance(base, ast.Attribute)
                else getattr(base, "id", "")
            )
            if tail == "Protocol":
                names.append(node.name)
    return names


def select_named(rel_paths: list[PurePath]) -> list[PurePath]:
    """Paths with a component whose stem is ``select`` (it would shadow the stdlib)."""
    return [
        p for p in rel_paths if any(PurePath(part).stem == "select" for part in p.parts)
    ]


def package_sources(root: Path = PACKAGE_DIR) -> dict[str, str]:
    """Source text by module name for every ``.py`` file under ``root``.

    A top-level file gives its stem; a nested one gives a dotted name
    (``sub/x.py`` is ``sub.x``), which is in no rule table.
    """
    return {
        ".".join(p.relative_to(root).with_suffix("").parts): p.read_text(
            encoding="utf-8"
        )
        for p in sorted(root.rglob("*.py"))
    }


def stray_directories(root: Path = PACKAGE_DIR) -> list[str]:
    """Sub-directories of ``root`` other than ``__pycache__`` (the design has none)."""
    return [
        str(p.relative_to(root))
        for p in sorted(root.rglob("*"))
        if p.is_dir() and "__pycache__" not in p.relative_to(root).parts
    ]


def _sources() -> dict[str, str]:
    return package_sources()


# ---------------------------------------------------------------------------
# The real package.
# ---------------------------------------------------------------------------


def test_package_has_exactly_the_designed_modules() -> None:
    """NFR-014, AC-25: the package holds exactly the designed modules."""
    assert set(_sources()) == set(RULES), (
        "the package modules differ from design 5.3 (add a row to RULES only "
        "with a design change)"
    )
    assert stray_directories() == [], "the design has no sub-package"


def test_package_listing_reaches_a_sub_package(tmp_path: Path) -> None:
    """A nested module is listed under a dotted name and its directory is stray."""
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "sub" / "x.py").write_text("import subprocess\n", encoding="utf-8")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "cycle.py").write_text("", encoding="utf-8")
    assert set(package_sources(tmp_path)) == {"cycle", "sub.__init__", "sub.x"}
    assert not set(package_sources(tmp_path)) <= set(RULES)
    assert stray_directories(tmp_path) == ["sub"]


@pytest.mark.parametrize("module", sorted(RULES))
def test_module_imports_obey_the_design_table(module: str) -> None:
    """NFR-014, AC-25: each module imports only what the design table allows."""
    source = _sources()[module]
    imports = collect_imports(source, f"{module}.py")
    if module != "__init__":
        assert imports, f"{module}.py: the scan found no import (walker is blind)"
    found = violations(module, imports, RULES[module])
    assert not found, "forbidden imports:\n" + "\n".join(found)


def test_real_relative_imports_resolve_to_the_package() -> None:
    """The walker sees sibling imports written in relative form (research F6)."""
    cli = {i.module for i in collect_imports(_sources()["cli"])}
    assert f"{PACKAGE}.cycle" in cli  # ``from . import audit, cycle, record``
    assert f"{PACKAGE}.launch" in cli  # ``from .launch import ...``
    assert "click" in cli


def test_record_defers_atomic_and_fcntl_to_function_level() -> None:
    """NFR-014, DF-29: swarm.atomic and fcntl are imported inside functions only."""
    imports = collect_imports(_sources()["record"])
    atomic = [i for i in imports if i.module == ATOMIC]
    fcntl = [i for i in imports if i.module == "fcntl"]
    assert atomic and fcntl, "record no longer defers swarm.atomic or fcntl"
    assert all(i.in_function for i in atomic + fcntl)
    assert any(i.module == f"{PACKAGE}.predicates" for i in imports)


def test_no_module_is_named_select() -> None:
    """NFR-014, AC-25: no module or directory of the package is named select."""
    rel = [p.relative_to(PACKAGE_DIR) for p in PACKAGE_DIR.rglob("*")]
    assert rel, "package directory is empty"
    assert select_named(rel) == []


def test_exactly_four_protocol_classes() -> None:
    """NFR-014, AC-25: exactly four Protocols exist (runner, store, launcher, clock)."""
    found: list[str] = []
    for path in PACKAGE_DIR.rglob("*.py"):
        found += protocol_class_names(path.read_text(encoding="utf-8"))
    assert sorted(found) == sorted(EXPECTED_PROTOCOLS), found


# ---------------------------------------------------------------------------
# Mutation guards: the walker must flag synthetic bad sources and pass good ones.
# ---------------------------------------------------------------------------

_CYCLE = "from superclaude.cli.issue_watch.cycle import x"

FLAGGED = [
    ("runner", _CYCLE),
    ("runner", "from .cycle import x"),
    ("runner", "from . import cycle"),
    ("runner", "import superclaude.cli.issue_watch.cycle"),
    ("runner", "from superclaude.cli.issue_watch import cycle"),
    ("runner", "def f():\n    from .cycle import x\n"),
    ("runner", "import click"),
    ("predicates", "from .runner import Runner"),
    ("audit", "from .record import Entry"),
    ("audit", f"from {ATOMIC} import write_prepared_bytes"),
    ("github", "from .launch import Launcher"),
    ("github", "from . import record"),
    ("record", "from .runner import Runner"),
    ("record", f"from {ATOMIC} import write_prepared_bytes"),
    ("record", f"if True:\n    from {ATOMIC} import write_prepared_bytes"),
    (
        "record",
        f"from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    import {ATOMIC}",
    ),
    ("record", "from superclaude.cli.swarm import atomic"),
    ("record", "import fcntl"),
    ("record", "if True:\n    from .cycle import Entry"),
    ("launch", "from .github import x"),
    ("launch", f"from {INSTALL_USER_SETUP} import main"),
    ("launch", f"import {INSTALL_USER_SETUP}"),
    ("cycle", "from .cli import x"),
    ("cycle", "import requests"),
    ("cycle", "import click"),
    ("cycle", "from click import group"),
    ("cycle", "from superclaude.cli.main import main"),
    ("cycle", f"from {ATOMIC} import write_prepared_bytes"),
    ("cycle", "import superclaude"),
    ("cycle", "from .. import cli"),
    ("cli", "from .github import x"),
    ("cli", "from . import predicates"),
    ("cli", "from superclaude.cli.issue_watch.predicates import x"),
    ("cli", "import yaml"),
    ("__init__", "from . import runner"),
]

CLEAN = [
    ("runner", "from __future__ import annotations\nimport subprocess, os.path"),
    ("runner", "from dataclasses import dataclass\nfrom typing import Protocol"),
    ("cycle", "from . import runner"),
    ("cycle", "from .runner import Runner"),
    ("cycle", "from superclaude.cli.issue_watch.runner import Runner"),
    ("cycle", "import superclaude.cli.issue_watch.runner"),
    ("cycle", "from superclaude.cli.issue_watch import runner"),
    ("github", "from .predicates import x\nfrom .runner import y"),
    ("record", "from .predicates import x"),
    ("record", "from superclaude.cli.issue_watch.predicates import x"),
    ("record", f"def save():\n    from {ATOMIC} import write_prepared_bytes"),
    ("record", f"async def save():\n    from {ATOMIC} import write_prepared_bytes"),
    (
        "record",
        f"class S:\n    def save(self):\n        from {ATOMIC} import write_prepared_bytes",
    ),
    ("record", "def lock():\n    import fcntl"),
    (
        "launch",
        f"from {INSTALL_USER_SETUP} import _ORCA_CLIS\nfrom .runner import Runner",
    ),
    ("cli", "import click\nfrom click.testing import CliRunner"),
    (
        "cli",
        "from . import audit, cycle, record\nfrom .launch import X\nfrom .runner import Y",
    ),
    ("__init__", ""),
]


def _verdict(module: str, source: str) -> list[str]:
    return violations(module, collect_imports(source), RULES[module])


@pytest.mark.parametrize(("module", "source"), FLAGGED)
def test_walker_flags_forbidden_import(module: str, source: str) -> None:
    assert _verdict(module, source), f"{module!r} was not flagged for: {source!r}"


@pytest.mark.parametrize(("module", "source"), CLEAN)
def test_walker_accepts_allowed_import(module: str, source: str) -> None:
    assert _verdict(module, source) == []


def test_walker_resolves_relative_and_absolute_to_the_same_name() -> None:
    forms = [
        "from .launch import X",
        "from superclaude.cli.issue_watch.launch import X",
    ]
    assert {i.module for f in forms for i in collect_imports(f)} == {
        f"{PACKAGE}.launch"
    }
    assert [i.module for i in collect_imports("from . import audit, cycle")] == [
        f"{PACKAGE}.audit",
        f"{PACKAGE}.cycle",
    ]


def test_walker_marks_function_level_and_nested_imports() -> None:
    source = "import os\ndef f():\n    def g():\n        import fcntl\n    return g\n"
    assert {i.module: i.in_function for i in collect_imports(source)} == {
        "os": False,
        "fcntl": True,
    }


def test_protocol_detector_flags_synthetic_protocols_only() -> None:
    source = (
        "import typing\n"
        "class A(Protocol): ...\n"
        "class B(typing.Protocol): ...\n"
        "class C(Protocol[T]): ...\n"
        "class D: ...\n"
        "class E(Base): ...\n"
    )
    assert protocol_class_names(source) == ["A", "B", "C"]


def test_select_detector_flags_synthetic_paths() -> None:
    bad = [PurePath("select.py"), PurePath("select/__init__.py")]
    good = [PurePath("cycle.py"), PurePath("selection.py")]
    assert select_named(bad + good) == bad
