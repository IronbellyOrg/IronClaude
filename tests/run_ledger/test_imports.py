"""ledger.py may import only ``RUN_ID_RE`` and ``parse_time`` from probes (AST check).

The sweep package uses relative imports, so the check handles ``from .probes import X``,
``from . import probes`` (then ``probes.X``), the absolute forms and ``import ... as``.
"""

from __future__ import annotations

import ast
from pathlib import Path

import superclaude.cli.sweep.ledger as ledger_module

ALLOWED = {"RUN_ID_RE", "parse_time"}
PROBES_ABSOLUTE = "superclaude.cli.sweep.probes"


def probes_names(source: str) -> set[str]:
    """Every name a module takes from ``superclaude.cli.sweep.probes`` (``*`` and a bare module use included)."""
    tree = ast.parse(source)
    names: set[str] = set()
    module_aliases: set[str] = set()  # local names that stand for the probes module
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            from_probes = (node.level == 1 and node.module == "probes") or (
                node.level == 0 and node.module == PROBES_ABSOLUTE
            )
            package_import = (node.level == 1 and node.module is None) or (
                node.level == 0 and node.module == "superclaude.cli.sweep"
            )
            for alias in node.names:
                if from_probes:
                    names.add(alias.name)
                elif package_import and alias.name == "probes":
                    module_aliases.add(alias.asname or "probes")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == PROBES_ABSOLUTE:
                    module_aliases.add(alias.asname or PROBES_ABSOLUTE)
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id in module_aliases:
                names.add(node.attr)
        if (
            isinstance(node, ast.Attribute)
            and ast.unparse(node.value) in module_aliases
        ):
            names.add(node.attr)
    if module_aliases and not names:
        names.add(
            "<module>"
        )  # a bare module import with no attribute use is still a use
    return names


def test_checker_sees_every_import_form():
    assert probes_names("from .probes import parse_time, ALLOWED_ORCA") == {
        "parse_time",
        "ALLOWED_ORCA",
    }
    assert probes_names("from superclaude.cli.sweep.probes import _call") == {"_call"}
    assert probes_names("from . import probes\nprobes.bind_run(1)") == {"bind_run"}
    assert probes_names("from . import probes as p\np.run_orca()") == {"run_orca"}
    assert probes_names("import superclaude.cli.sweep.probes as p\np.x") == {"x"}
    assert probes_names(
        "import superclaude.cli.sweep.probes\nsuperclaude.cli.sweep.probes.y"
    ) == {"y"}
    assert probes_names("from .probes import *") == {"*"}
    assert probes_names("import json\nfrom .models import SweepContext") == set()


def test_ledger_imports_only_allowed_probes_names():
    source = Path(ledger_module.__file__).read_text(encoding="utf-8")
    used = probes_names(source)
    assert used, "ledger.py no longer imports parse_time from probes"
    assert used <= ALLOWED, (
        f"ledger.py takes more than {sorted(ALLOWED)} from probes: {sorted(used - ALLOWED)}"
    )


def test_fcntl_is_not_imported_at_module_level():
    # main.py imports this module for every command, so a platform without fcntl must import it.
    tree = ast.parse(Path(ledger_module.__file__).read_text(encoding="utf-8"))
    top_level = {
        alias.name.split(".")[0]
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        node.module.split(".")[0]
        for node in tree.body
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert "fcntl" not in top_level
