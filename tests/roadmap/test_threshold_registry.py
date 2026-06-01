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

# R1.1 Step 6.3 consumer migrations — must import from superclaude.contracts.
# Per phase-outputs/discovery/return-contracts-scope.md §I.
_R1_1_CONSUMER_FILES = [
    _SRC_ROOT / "cli" / "roadmap" / "fingerprint.py",
    _SRC_ROOT / "cli" / "roadmap" / "spec_structural_audit.py",
    _SRC_ROOT / "cli" / "roadmap" / "gates.py",
    _SRC_ROOT / "cli" / "roadmap" / "fidelity_checker.py",
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
    [
        "ID_PATTERNS",
        "CONVERGENCE_THRESHOLDS",
        "GATE_FIELD_NAMES",
        # R1.1 Step 6.2 extensions — same single-definition invariant.
        "THRESHOLDS",
        "RETURN_CONTRACTS",
    ],
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


# ---------------------------------------------------------------------------
# R1.1 Step 6.4 tests — RETURN_CONTRACTS + extended threshold registry.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("consumer_path", _R1_1_CONSUMER_FILES)
def test_r1_1_consumers_import_from_contracts(consumer_path: Path) -> None:
    """Each R1.1-scope consumer reads from ``superclaude.contracts``.

    Per phase-outputs/discovery/return-contracts-scope.md §I migration plan.
    """
    assert consumer_path.exists(), (
        f"R1.1 consumer file missing: {consumer_path.relative_to(_REPO_ROOT)}"
    )
    assert _has_contracts_import(consumer_path), (
        f"{consumer_path.relative_to(_REPO_ROOT)} must contain "
        "'from superclaude.contracts import …' (R1.1 consumer migration §I)"
    )


def test_thresholds_shape_matches_consumer_inventory() -> None:
    """``THRESHOLDS`` carries the exact float values previously inlined.

    Per phase-outputs/discovery/return-contracts-scope.md §E. If a consumer
    site needs a different value, the change goes through the SoT — this test
    is the sentinel against silent drift.
    """
    from superclaude.contracts import THRESHOLDS

    assert THRESHOLDS == {
        "fingerprint.coverage_min": 0.7,
        "structural_audit.adequacy_min": 0.5,
    }


def test_return_contracts_shape_canonical() -> None:
    """``RETURN_CONTRACTS`` registers exactly the skills with programmatic
    return contracts (per return-contracts-scope.md §B — only sc:adversarial)."""
    from superclaude.contracts import RETURN_CONTRACTS, AdversarialReturn

    assert RETURN_CONTRACTS == {"sc:adversarial": AdversarialReturn}


def test_adversarial_return_fields_match_skill_prose() -> None:
    """``AdversarialReturn`` field names match the canonical skill prose.

    Source: ``src/superclaude/skills/sc-adversarial-protocol/SKILL.md:432-443``.
    Sentinel against drift between the SoT dataclass and the skill spec.
    """
    from dataclasses import fields

    from superclaude.contracts import AdversarialReturn

    field_names = {f.name for f in fields(AdversarialReturn)}
    expected = {
        "merged_output_path",
        "convergence_score",
        "artifacts_dir",
        "status",
        "base_variant",
        "unresolved_conflicts",
        "fallback_mode",
        "failure_stage",
        "invocation_method",
        "unaddressed_invariants",
    }
    assert field_names == expected, (
        "AdversarialReturn fields diverge from sc-adversarial-protocol/"
        "SKILL.md:432-443 return_contract YAML. "
        f"Missing: {expected - field_names}; extra: {field_names - expected}"
    )


def test_adversarial_return_is_frozen_hashable() -> None:
    """``AdversarialReturn`` instances are hashable per Step 6.2 invariant.

    Required so consumer code can use returns as dict keys / set members
    without TypeErrors on the ``unaddressed_invariants`` nested field.
    """
    from superclaude.contracts import AdversarialReturn, UnaddressedInvariant

    invariant = UnaddressedInvariant(
        id="INV-1", category="auth", assumption="x", severity="HIGH"
    )
    ret = AdversarialReturn(
        merged_output_path="/tmp/x.md",
        convergence_score=0.75,
        artifacts_dir="/tmp/adv",
        status="success",
        base_variant="opus:architect",
        unresolved_conflicts=0,
        fallback_mode=False,
        failure_stage=None,
        invocation_method="skill-direct",
        unaddressed_invariants=(invariant,),
    )
    # Must be hashable — would TypeError if any field were unhashable.
    assert isinstance(hash(ret), int)
    # And usable as a dict key.
    bucket: dict = {ret: "ok"}
    assert bucket[ret] == "ok"


def test_no_orphan_threshold_literals_in_migrated_files() -> None:
    """The R1.1-migrated default args resolve via ``THRESHOLDS``, not literals.

    Targeted anti-creep guard. If a future change re-inlines the literal
    (e.g. by reverting ``THRESHOLDS["..."]`` to a raw ``0.7``), this test fires.
    Generic ``0.7``/``0.5`` floats elsewhere in the files are not flagged —
    only the migrated default-arg sites.
    """
    import ast

    from superclaude.contracts import THRESHOLDS

    sentinel_value = THRESHOLDS["fingerprint.coverage_min"]
    # Functions whose default args MUST resolve via THRESHOLDS, not a literal.
    targets = {
        _SRC_ROOT / "cli" / "roadmap" / "fingerprint.py": (
            "check_fingerprint_coverage",
            "fingerprint_gate_passed",
        ),
        _SRC_ROOT / "cli" / "roadmap" / "spec_structural_audit.py": (
            "check_extraction_adequacy",
        ),
    }
    for path, fn_names in targets.items():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name in fn_names:
                for default in node.args.defaults:
                    # Default must be a Subscript (THRESHOLDS["..."]),
                    # never a Constant (literal float).
                    assert not isinstance(default, ast.Constant), (
                        f"{path.relative_to(_REPO_ROOT)}:{node.lineno}: "
                        f"{node.name} default arg is a raw literal "
                        f"({default.value!r}) — must resolve via "
                        "superclaude.contracts.THRESHOLDS"
                    )
    # Independent verification: sentinel value still 0.7 (defends against
    # accidental rewrite of THRESHOLDS itself).
    assert sentinel_value == 0.7
