"""Contract #5 + #8 integration tests against the real `src/superclaude/` tree.

These tests are the CI gate that makes ``superclaude.contracts`` the
**source of truth** for cross-skill / cross-module constants. They are the
PR-blocking counterpart to ``make lint-architecture`` (Check 11) per the
Phase 5 Step 5.1 wiring plan.

Coverage:

* :func:`test_id_patterns_defined_once_in_src` — exactly one ``ID_PATTERNS``
  rebind in ``src/superclaude/`` (the canonical one in the contracts
  module). Identical for ``CONVERGENCE_THRESHOLDS`` and ``GATE_FIELD_NAMES``.
* :func:`test_r0_3_consumers_import_from_contracts` — the three R0.3-scope
  consumers documented in
  ``phase-outputs/discovery/contracts-consumer-sites.md`` §F all contain a
  ``from superclaude.contracts import …`` statement.
* :func:`test_arch_lint_fails_on_duplicate` — the walker returns non-zero on
  a synthetic duplicate (end-to-end CLI invocation; complements the unit
  tests in ``tests/contracts/test_arch_lint.py``).
* :func:`test_no_orphan_id_pattern_literals_in_cli` — no source file under
  ``src/superclaude/cli/`` contains an inline regex string equal to a
  canonical ``ID_PATTERNS`` body (anti-creep guard).
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

from superclaude.contracts import ID_PATTERNS

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC_ROOT = _REPO_ROOT / "src" / "superclaude"
_CONTRACTS_FILE = _SRC_ROOT / "contracts" / "__init__.py"

_CONSUMER_FILES = [
    _SRC_ROOT / "cli" / "roadmap" / "id_registry.py",
    _SRC_ROOT / "cli" / "roadmap" / "spec_parser.py",
    _SRC_ROOT / "cli" / "roadmap" / "gates.py",
]


def _count_top_level_assignments(path: Path, target_name: str) -> int:
    """Count Assign / AnnAssign nodes binding ``target_name`` in ``path``."""
    if not path.exists():
        return 0
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == target_name:
                    count += 1
        elif isinstance(node, ast.AnnAssign):
            tgt = node.target
            if isinstance(tgt, ast.Name) and tgt.id == target_name:
                count += 1
    return count


def _has_contracts_import(path: Path) -> bool:
    """Return True iff ``path`` contains ``from superclaude.contracts import …``."""
    if not path.exists():
        return False
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == "superclaude.contracts":
                return True
    return False


@pytest.mark.parametrize(
    "constant_name",
    ["ID_PATTERNS", "CONVERGENCE_THRESHOLDS", "GATE_FIELD_NAMES"],
)
def test_constant_defined_exactly_once_in_src(constant_name: str) -> None:
    """Each contract constant has exactly one canonical assignment.

    The canonical assignment lives in ``src/superclaude/contracts/__init__.py``.
    Any other assignment is a Contract #8 violation.
    """
    total = 0
    locations: list[str] = []
    for py_file in sorted(_SRC_ROOT.rglob("*.py")):
        n = _count_top_level_assignments(py_file, constant_name)
        if n:
            locations.append(f"{py_file.relative_to(_REPO_ROOT)} (count={n})")
            total += n
    assert total == 1, (
        f"{constant_name} must be defined exactly once in src/superclaude/; "
        f"found {total} occurrence(s):\n  " + "\n  ".join(locations)
    )
    # And the one location must be the canonical file.
    assert locations and str(_CONTRACTS_FILE.relative_to(_REPO_ROOT)) in locations[0]


@pytest.mark.parametrize("consumer_path", _CONSUMER_FILES)
def test_r0_3_consumers_import_from_contracts(consumer_path: Path) -> None:
    """Each R0.3-scope consumer reads from ``superclaude.contracts``."""
    assert consumer_path.exists(), (
        f"R0.3 consumer file missing: {consumer_path.relative_to(_REPO_ROOT)}"
    )
    assert _has_contracts_import(consumer_path), (
        f"{consumer_path.relative_to(_REPO_ROOT)} must contain "
        "'from superclaude.contracts import …' (R0.3 consumer-inventory §F)"
    )


def test_arch_lint_passes_on_clean_repo() -> None:
    """End-to-end: ``arch_lint`` exits 0 against the current ``src/superclaude/cli/``."""
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "superclaude.tools.arch_lint",
            "--check-contracts",
            str(_CONTRACTS_FILE),
            "--scan-paths",
            str(_SRC_ROOT / "cli"),
        ],
        cwd=_REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, (
        f"arch-lint failed on clean repo:\n{proc.stdout}\n{proc.stderr}"
    )
    assert "arch-lint: PASS" in proc.stdout


def test_arch_lint_fails_on_duplicate(tmp_path: Path) -> None:
    """End-to-end: the walker exits 1 on a synthetic duplicate."""
    bad = tmp_path / "bad.py"
    bad.write_text("ID_PATTERNS = {}\n", encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "superclaude.tools.arch_lint",
            "--check-contracts",
            str(_CONTRACTS_FILE),
            "--scan-paths",
            str(tmp_path),
        ],
        cwd=_REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert "arch-lint: FAIL" in proc.stdout
    assert "ID_PATTERNS" in proc.stdout


def test_no_orphan_id_pattern_literals_in_cli() -> None:
    """No source file under ``src/superclaude/cli/`` carries an inline regex
    string equal to a canonical ``ID_PATTERNS`` body.

    The arch-lint walker enforces the same invariant; this test surfaces
    failures as readable pytest output (the walker only emits on stdout).
    """
    bodies = set(ID_PATTERNS.values())
    offenders: list[str] = []
    for py_file in sorted((_SRC_ROOT / "cli").rglob("*.py")):
        if py_file.resolve() == _CONTRACTS_FILE.resolve():
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value in bodies:
                    offenders.append(
                        f"{py_file.relative_to(_REPO_ROOT)}:{node.lineno}: "
                        f"literal {node.value!r}"
                    )
    assert not offenders, (
        "Inline ID-pattern bodies found in src/superclaude/cli/ "
        "(Contract #8 violation):\n  " + "\n  ".join(offenders)
    )


def test_g_family_present_in_id_patterns() -> None:
    """G-family MUST be in ``ID_PATTERNS`` (Phase 2 D1 deviation).

    Required to honor Contract #8 against the pre-existing extractor at
    ``cli/roadmap/spec_parser.py:328``. Deletion of the G key here would
    silently regress G-ID extraction.
    """
    assert "G" in ID_PATTERNS, (
        "ID_PATTERNS['G'] missing — see Phase 2 D1 informational deviation "
        "+ phase-outputs/discovery/contracts-consumer-sites.md §E"
    )


def test_convergence_thresholds_shape_matches_build_request() -> None:
    """``CONVERGENCE_THRESHOLDS`` shape must match BUILD-REQUEST §MVR §5 verbatim.

    Per Phase 4 Step 4.2 "constants exactly match the BUILD-REQUEST verbatim
    (regex strings, threshold tuples, dict shapes — no paraphrasing)".
    """
    from superclaude.contracts import CONVERGENCE_THRESHOLDS

    assert CONVERGENCE_THRESHOLDS == {
        "sc:roadmap": (0.7, 0.5),
        "sc:release-split": (0.7, 0.5),
    }


def test_gate_field_names_shape_matches_build_request() -> None:
    """``GATE_FIELD_NAMES`` shape must match BUILD-REQUEST §MVR §5 verbatim."""
    from superclaude.contracts import GATE_FIELD_NAMES

    assert GATE_FIELD_NAMES == {
        "deviation_analysis": {"ambiguous": "ambiguous_deviations"},
    }
