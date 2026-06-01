"""Arch-lint walker — Contract #5 + #8 anti-duplication enforcement.

Per BUILD-REQUEST §R0 item 3 + §Contract items #5 and #8, no module
outside :mod:`superclaude.contracts` may redefine a constant whose name or
literal value is owned by the contracts registry.

This walker:

1. Imports :mod:`superclaude.contracts` to learn the canonical constant
   names (``__all__`` membership: ``ID_PATTERNS``, ``CONVERGENCE_THRESHOLDS``,
   ``GATE_FIELD_NAMES``, ``THRESHOLDS``, ``RETURN_CONTRACTS``,
   ``AdversarialReturn``, ``UnaddressedInvariant``) and the verbatim
   regex/string values they own.
2. Walks the AST of every ``.py`` file under one or more scan paths.
3. Flags every ``ast.Assign`` / ``ast.AnnAssign`` whose LHS targets a name
   in the contract constant set, when the file is NOT the contracts module.
4. Flags every ``ast.Constant`` (string literal) whose value matches an
   ID-pattern body string from :data:`ID_PATTERNS`, when the surrounding
   line does not carry the opt-out marker
   ``# arch-lint: allow-duplicate <reason>``.
5. Flags every ``ast.ClassDef`` whose ``name`` matches a canonical
   class name (e.g. ``AdversarialReturn``, ``UnaddressedInvariant``),
   when the file is NOT the contracts module. Added in R1.1 Step 6.3 to
   prevent dataclass shadowing of the SoT return-contract types.

Usage::

    uv run python -m superclaude.tools.arch_lint \\
        --check-contracts src/superclaude/contracts/__init__.py \\
        --scan-paths src/superclaude/cli/

Exit codes:
* ``0`` — clean.
* ``1`` — at least one violation.
* ``2`` — invocation error (missing path, etc).

The walker emits single-line errors of the form::

    <file>:<line>: arch-lint: duplicate constant '<name>' redefined here \\
      (canonical in src/superclaude/contracts/__init__.py)

so editors and CI surfaces (GitHub Actions annotations) can render them
inline.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

_CANONICAL_MODULE = "superclaude.contracts"
_CANONICAL_RELPATH = Path("src/superclaude/contracts/__init__.py")
_ALLOW_MARKER = "arch-lint: allow-duplicate"


@dataclass(frozen=True)
class Violation:
    """A single arch-lint violation site."""

    path: Path
    lineno: int
    kind: str  # "name-rebind" | "literal-duplicate" | "class-redef"
    name: str
    detail: str

    def format(self) -> str:
        """Render a single-line message for CI / editor annotation."""
        return (
            f"{self.path}:{self.lineno}: arch-lint: "
            f"{self.kind} '{self.name}' redefined here "
            f"(canonical in {_CANONICAL_RELPATH}) — {self.detail}"
        )


def _load_canonical_constants() -> tuple[set[str], set[str]]:
    """Return ``(canonical_names, canonical_pattern_bodies)``.

    Imports :mod:`superclaude.contracts`. If the import fails the lint
    cannot meaningfully run — surface the failure as a violation-class
    error in the caller.
    """
    module = importlib.import_module(_CANONICAL_MODULE)
    canonical_names: set[str] = set(getattr(module, "__all__", []))
    id_patterns: dict[str, str] = getattr(module, "ID_PATTERNS", {})
    canonical_pattern_bodies: set[str] = set(id_patterns.values())
    return canonical_names, canonical_pattern_bodies


def _iter_python_files(scan_paths: Iterable[Path]) -> Iterable[Path]:
    """Yield every ``.py`` file under each scan path (recursive)."""
    for root in scan_paths:
        if root.is_file() and root.suffix == ".py":
            yield root
        elif root.is_dir():
            yield from sorted(root.rglob("*.py"))


def _line_has_allow_marker(source_lines: list[str], lineno: int) -> bool:
    """Check whether the line at ``lineno`` (1-based) carries the opt-out."""
    if not 1 <= lineno <= len(source_lines):
        return False
    return _ALLOW_MARKER in source_lines[lineno - 1]


def _is_canonical_file(path: Path) -> bool:
    """Return True iff ``path`` is the canonical contracts module."""
    # Resolve to handle absolute / relative invocations uniformly.
    return path.resolve().match(str(_CANONICAL_RELPATH))


def scan_file(
    path: Path,
    canonical_names: set[str],
    canonical_pattern_bodies: set[str],
) -> list[Violation]:
    """Scan a single Python file for contract-constant violations.

    Returns a list of :class:`Violation` instances; empty if the file is
    clean. The canonical contracts file is skipped (it owns the constants).
    """
    if _is_canonical_file(path):
        return []

    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    source_lines = source.splitlines()

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return []

    violations: list[Violation] = []

    for node in ast.walk(tree):
        # Rule 1: name rebinding via Assign / AnnAssign on a contract constant.
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets: list[ast.expr]
            if isinstance(node, ast.Assign):
                targets = list(node.targets)
            else:
                targets = [node.target]
            for tgt in targets:
                if isinstance(tgt, ast.Name) and tgt.id in canonical_names:
                    if _line_has_allow_marker(source_lines, node.lineno):
                        continue
                    violations.append(
                        Violation(
                            path=path,
                            lineno=node.lineno,
                            kind="name-rebind",
                            name=tgt.id,
                            detail=(
                                "constant owned by superclaude.contracts; "
                                "import instead of redefine"
                            ),
                        )
                    )

        # Rule 2: string literal that exactly matches a canonical ID pattern body.
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value in canonical_pattern_bodies:
                if _line_has_allow_marker(source_lines, node.lineno):
                    continue
                violations.append(
                    Violation(
                        path=path,
                        lineno=node.lineno,
                        kind="literal-duplicate",
                        name=node.value,
                        detail=(
                            "ID-pattern body owned by "
                            "superclaude.contracts.ID_PATTERNS; "
                            "import the body instead of inlining the literal"
                        ),
                    )
                )

        # Rule 3 (R1.1 Step 6.3): class definition shadowing a canonical name.
        # Prevents `class AdversarialReturn: ...` outside the contracts module
        # from evading the name-rebind rule (ClassDef is not Assign/AnnAssign).
        if isinstance(node, ast.ClassDef) and node.name in canonical_names:
            if _line_has_allow_marker(source_lines, node.lineno):
                continue
            violations.append(
                Violation(
                    path=path,
                    lineno=node.lineno,
                    kind="class-redef",
                    name=node.name,
                    detail=(
                        "dataclass owned by superclaude.contracts; "
                        "import instead of redefine"
                    ),
                )
            )

    return violations


def check_paths(
    canonical_file: Path,
    scan_paths: list[Path],
) -> list[Violation]:
    """Run the walker across ``scan_paths`` and return all violations.

    ``canonical_file`` is currently informational (the canonical names are
    loaded via import) but is accepted so future versions can read the AST
    of the contracts module directly without importing (relevant if the
    module gains import-time side effects).
    """
    _ = canonical_file  # reserved for future AST-based loader
    canonical_names, canonical_pattern_bodies = _load_canonical_constants()
    violations: list[Violation] = []
    for py_file in _iter_python_files(scan_paths):
        violations.extend(scan_file(py_file, canonical_names, canonical_pattern_bodies))
    return violations


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint. See module docstring for usage / exit codes."""
    parser = argparse.ArgumentParser(
        prog="superclaude.tools.arch_lint",
        description=(
            "Contract #5 + #8 anti-duplication walker. "
            "Fails CI if any module redefines a constant the "
            "superclaude.contracts registry owns."
        ),
    )
    parser.add_argument(
        "--check-contracts",
        type=Path,
        default=_CANONICAL_RELPATH,
        help=(
            "Path to the canonical contracts file (informational; "
            "constants are loaded via import)."
        ),
    )
    parser.add_argument(
        "--scan-paths",
        nargs="+",
        type=Path,
        required=True,
        help="One or more directories or files to scan recursively.",
    )
    args = parser.parse_args(argv)

    for scan_path in args.scan_paths:
        if not scan_path.exists():
            print(
                f"arch-lint: scan path does not exist: {scan_path}",
                file=sys.stderr,
            )
            return 2

    violations = check_paths(args.check_contracts, args.scan_paths)

    if not violations:
        print("arch-lint: PASS — no contract-constant duplications detected.")
        return 0

    for v in violations:
        print(v.format())
    print(
        f"arch-lint: FAIL — {len(violations)} violation(s). "
        f"Canonical constants live in {_CANONICAL_RELPATH}."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
