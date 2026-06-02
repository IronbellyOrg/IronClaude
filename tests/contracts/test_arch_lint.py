"""Unit tests for the arch-lint walker (Contract #5 + #8).

These tests cover :mod:`superclaude.tools.arch_lint` in isolation: synthetic
violations + the opt-out marker + the canonical-file skip.

Repo-wide arch-lint invariants (no real source file under
``src/superclaude/cli/`` redefines a contract constant) are exercised by
``tests/roadmap/test_threshold_registry.py``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.contracts import ID_PATTERNS
from superclaude.tools.arch_lint import (
    _CANONICAL_RELPATH,
    Violation,
    check_paths,
    main,
    scan_file,
)

_CANONICAL_NAMES = {
    "ID_PATTERNS",
    "CONVERGENCE_THRESHOLDS",
    "GATE_FIELD_NAMES",
    # R1.1 extensions (Step 6.2).
    "THRESHOLDS",
    "RETURN_CONTRACTS",
    "AdversarialReturn",
    "UnaddressedInvariant",
}
_CANONICAL_PATTERN_BODIES = set(ID_PATTERNS.values())


def test_clean_file_yields_no_violations(tmp_path: Path) -> None:
    clean = tmp_path / "clean.py"
    clean.write_text(
        '"""Clean file — imports from contracts, no redefinitions."""\n'
        "from superclaude.contracts import ID_PATTERNS\n"
        "FAMILIES = tuple(ID_PATTERNS.keys())\n",
        encoding="utf-8",
    )
    violations = scan_file(clean, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    assert violations == []


def test_name_rebind_violation_detected(tmp_path: Path) -> None:
    bad = tmp_path / "bad.py"
    bad.write_text(
        "ID_PATTERNS = {'FR': r'FR-X'}\n",
        encoding="utf-8",
    )
    violations = scan_file(bad, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    assert len(violations) >= 1
    name_rebinds = [v for v in violations if v.kind == "name-rebind"]
    assert len(name_rebinds) == 1
    assert name_rebinds[0].name == "ID_PATTERNS"
    assert name_rebinds[0].lineno == 1


def test_literal_duplicate_violation_detected(tmp_path: Path) -> None:
    # Use a verbatim ID_PATTERNS body so the literal-duplicate rule fires.
    fr_body = ID_PATTERNS["FR"]
    bad = tmp_path / "bad_literal.py"
    bad.write_text(
        f"PATTERN = {fr_body!r}\n",
        encoding="utf-8",
    )
    violations = scan_file(bad, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    literal_dupes = [v for v in violations if v.kind == "literal-duplicate"]
    assert len(literal_dupes) == 1
    assert literal_dupes[0].name == fr_body


@pytest.mark.parametrize(
    "position,source_template",
    [
        ("module", 'r"""{body}"""\nX = 1\n'),
        (
            "class",
            'r"""module docstring"""\n\n\nclass C:\n    r"""{body}"""\n    x = 1\n',
        ),
        (
            "function",
            'r"""module docstring"""\n\n\ndef f():\n    r"""{body}"""\n    return 1\n',
        ),
    ],
)
def test_docstring_with_verbatim_pattern_body_not_flagged(
    tmp_path: Path, position: str, source_template: str
) -> None:
    """R3: a docstring whose entire value equals an ``ID_PATTERNS`` body must NOT
    be flagged as a literal-duplicate — it is documentation, not a re-inlined
    constant. Covers module / class / function docstring positions. Fail-before
    (pre-R3 the docstring Constant matched the body and flagged) / pass-after."""
    fr_body = ID_PATTERNS["FR"]
    f = tmp_path / f"doc_{position}.py"
    f.write_text(source_template.format(body=fr_body), encoding="utf-8")
    violations = scan_file(f, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    literal_dupes = [v for v in violations if v.kind == "literal-duplicate"]
    assert literal_dupes == [], (
        f"R3: a {position} docstring equal to a pattern body must not flag; "
        f"got {literal_dupes}"
    )


def test_docstring_skip_does_not_mask_real_literal(tmp_path: Path) -> None:
    """R3 contrast (self-documenting in one place): a module docstring equal to a
    body is skipped, but a REAL top-level assignment of the SAME body in the same
    file STILL flags exactly once — proving the skip is scoped to docstrings only."""
    fr_body = ID_PATTERNS["FR"]
    f = tmp_path / "doc_and_literal.py"
    f.write_text(
        'r"""' + fr_body + '"""\n\nPATTERN = ' + repr(fr_body) + "\n",
        encoding="utf-8",
    )
    violations = scan_file(f, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    literal_dupes = [v for v in violations if v.kind == "literal-duplicate"]
    assert len(literal_dupes) == 1, (
        "R3: docstring skipped but the real assignment literal must still flag "
        f"exactly once; got {literal_dupes}"
    )
    assert literal_dupes[0].name == fr_body


def test_allow_marker_suppresses_violation(tmp_path: Path) -> None:
    fr_body = ID_PATTERNS["FR"]
    bad = tmp_path / "with_marker.py"
    bad.write_text(
        f"PATTERN = {fr_body!r}  # arch-lint: allow-duplicate test-fixture\n",
        encoding="utf-8",
    )
    violations = scan_file(bad, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    literal_dupes = [v for v in violations if v.kind == "literal-duplicate"]
    assert literal_dupes == []


def test_canonical_file_is_skipped() -> None:
    canonical = Path(_CANONICAL_RELPATH)
    if not canonical.exists():
        # In some run contexts the cwd may not be the repo root; resolve from
        # the installed module path instead.
        from superclaude import contracts as _contracts_pkg

        canonical = Path(_contracts_pkg.__file__)
    violations = scan_file(canonical, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    assert violations == []


def test_violation_format_includes_canonical_pointer(tmp_path: Path) -> None:
    bad = tmp_path / "bad.py"
    bad.write_text("ID_PATTERNS = {}\n", encoding="utf-8")
    violations = scan_file(bad, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    assert violations
    msg = violations[0].format()
    assert str(bad) in msg
    assert "arch-lint:" in msg
    assert "superclaude.contracts" in msg
    assert "ID_PATTERNS" in msg


def test_check_paths_aggregates_across_files(tmp_path: Path) -> None:
    (tmp_path / "ok.py").write_text(
        "from superclaude.contracts import ID_PATTERNS\n", encoding="utf-8"
    )
    (tmp_path / "bad1.py").write_text("ID_PATTERNS = {}\n", encoding="utf-8")
    (tmp_path / "bad2.py").write_text("CONVERGENCE_THRESHOLDS = {}\n", encoding="utf-8")
    violations = check_paths(
        canonical_file=Path("src/superclaude/contracts/__init__.py"),
        scan_paths=[tmp_path],
    )
    names = {v.name for v in violations}
    assert {"ID_PATTERNS", "CONVERGENCE_THRESHOLDS"}.issubset(names)


def test_main_returns_nonzero_on_violations(tmp_path: Path, capsys) -> None:
    bad = tmp_path / "bad.py"
    bad.write_text("ID_PATTERNS = {}\n", encoding="utf-8")
    rc = main(["--scan-paths", str(tmp_path)])
    assert rc == 1
    captured = capsys.readouterr()
    assert "arch-lint: FAIL" in captured.out
    assert "ID_PATTERNS" in captured.out


def test_main_returns_zero_on_clean_scan(tmp_path: Path, capsys) -> None:
    (tmp_path / "ok.py").write_text(
        "from superclaude.contracts import ID_PATTERNS\n", encoding="utf-8"
    )
    rc = main(["--scan-paths", str(tmp_path)])
    assert rc == 0
    captured = capsys.readouterr()
    assert "arch-lint: PASS" in captured.out


def test_main_returns_two_on_missing_path(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "does-not-exist"
    rc = main(["--scan-paths", str(missing)])
    assert rc == 2


def test_class_redef_violation_detected(tmp_path: Path) -> None:
    """R1.1 Rule 3: ``class AdversarialReturn`` outside contracts is a violation."""
    bad = tmp_path / "bad_class.py"
    bad.write_text(
        "from dataclasses import dataclass\n"
        "\n"
        "@dataclass(frozen=True)\n"
        "class AdversarialReturn:\n"
        "    x: str\n",
        encoding="utf-8",
    )
    violations = scan_file(bad, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    class_redefs = [v for v in violations if v.kind == "class-redef"]
    assert len(class_redefs) == 1
    assert class_redefs[0].name == "AdversarialReturn"


def test_class_redef_unaddressed_invariant_detected(tmp_path: Path) -> None:
    """R1.1 Rule 3 also catches the nested ``UnaddressedInvariant`` dataclass."""
    bad = tmp_path / "bad_nested.py"
    bad.write_text(
        "class UnaddressedInvariant:\n    pass\n",
        encoding="utf-8",
    )
    violations = scan_file(bad, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    class_redefs = [v for v in violations if v.kind == "class-redef"]
    assert len(class_redefs) == 1
    assert class_redefs[0].name == "UnaddressedInvariant"


def test_class_redef_allow_marker_suppresses(tmp_path: Path) -> None:
    """R1.1 Rule 3 respects the ``arch-lint: allow-duplicate`` opt-out."""
    bad = tmp_path / "with_marker.py"
    bad.write_text(
        "class AdversarialReturn:  # arch-lint: allow-duplicate test-fixture\n"
        "    pass\n",
        encoding="utf-8",
    )
    violations = scan_file(bad, _CANONICAL_NAMES, _CANONICAL_PATTERN_BODIES)
    class_redefs = [v for v in violations if v.kind == "class-redef"]
    assert class_redefs == []


def test_canonical_names_includes_r1_1_extensions() -> None:
    """Step 6.2: ``superclaude.contracts.__all__`` exposes the R1.1 names.

    The arch-lint walker auto-discovers canonical names via the contracts
    module's ``__all__``. This test asserts the runtime set matches the
    R1.1 surface so the walker covers the new constants without further code.
    """
    import importlib

    contracts = importlib.import_module("superclaude.contracts")
    all_set = set(getattr(contracts, "__all__", []))
    r1_1_extensions = {
        "THRESHOLDS",
        "RETURN_CONTRACTS",
        "AdversarialReturn",
        "UnaddressedInvariant",
    }
    assert r1_1_extensions.issubset(all_set), (
        f"R1.1 extensions missing from contracts.__all__: {r1_1_extensions - all_set}"
    )


def test_violation_dataclass_is_hashable() -> None:
    # Frozen dataclass invariant — needed for set / dedupe semantics in
    # downstream callers.
    v1 = Violation(
        path=Path("/tmp/x.py"),
        lineno=1,
        kind="name-rebind",
        name="ID_PATTERNS",
        detail="x",
    )
    v2 = Violation(
        path=Path("/tmp/x.py"),
        lineno=1,
        kind="name-rebind",
        name="ID_PATTERNS",
        detail="x",
    )
    assert hash(v1) == hash(v2)
    assert {v1, v2} == {v1}
