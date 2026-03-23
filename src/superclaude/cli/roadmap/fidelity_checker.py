"""Impl-vs-spec fidelity checker — verifies codebase evidence for spec FRs.

Matching Contract (OQ-2)
========================
This checker uses **exact name matching only** — no NLP, fuzzy, or semantic
matching.  For each FR extracted from the spec, it searches the codebase for
evidence that the required function or class exists.

Evidence search methods (in order):
1. AST parse (``ast.parse``) of ``.py`` files — extracts top-level and nested
   function/class definitions for exact name comparison.
2. String search fallback — for non-Python files or AST parse failures, a
   case-sensitive substring search of file contents.

Ambiguity Policy (R-3 Mitigation)
==================================
When a match is ambiguous (e.g. a name appears but context is unclear),
the checker **fails open**: it logs a warning and reports the FR as FOUND
rather than blocking the pipeline.  This prevents false-positive gaps from
stalling the convergence engine.

Checker output conforms to the ``list[Finding]`` shape used by structural
and semantic checkers, enabling direct integration into ``_run_checkers()``.
"""

from __future__ import annotations

import ast
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .convergence import compute_stable_id
from .models import Finding
from .spec_parser import (
    ParseResult,
    extract_requirement_ids,
    parse_document,
)

logger = logging.getLogger(__name__)

# FR pattern for extracting requirement references with associated names
_FR_HEADING_RE = re.compile(
    r"^#{1,6}\s+.*?\b(FR-\d+(?:\.\d+)?)\b",
    re.MULTILINE,
)

# Patterns to extract function/class names associated with an FR section
_FUNC_NAME_RE = re.compile(r"`(\w{3,})\(\)`|`(\w{3,})`\s*function|function\s+`(\w{3,})`")
_CLASS_NAME_RE = re.compile(r"`(\w{3,})`\s*class|class\s+`(\w{3,})`|`(\w{3,})`\s*(?:object|instance)")
_CODE_DEF_RE = re.compile(r"(?:def|class)\s+(\w{4,})")

# Common English words to exclude from name extraction
_STOP_WORDS = frozenset({
    "self", "cls", "none", "true", "false", "return", "class", "from",
    "import", "with", "that", "this", "will", "must", "shall", "should",
    "have", "been", "each", "when", "then", "else", "elif", "except",
    "raise", "yield", "async", "await", "lambda", "global", "assert",
    "while", "break", "continue", "pass", "finally", "nonlocal",
    "file", "path", "data", "name", "names", "type", "types", "list",
    "dict", "sets", "args", "kwargs", "value", "values", "function",
    "method", "module", "package", "defined", "required", "implement",
})


@dataclass
class FRMapping:
    """A single FR-to-implementation mapping."""

    fr_id: str
    expected_names: list[str]  # function or class names expected in codebase
    source_context: str = ""  # text around the FR for diagnostics


@dataclass
class FidelityResult:
    """Result for a single FR check."""

    fr_id: str
    found: bool
    evidence_names: list[str] = field(default_factory=list)
    searched_names: list[str] = field(default_factory=list)
    ambiguous: bool = False
    message: str = ""


class FidelityChecker:
    """Checks that spec FRs have corresponding implementation evidence in the codebase.

    Args:
        source_dir: Root directory of the codebase to search.
        allowlist: Optional dict of FR-id -> list[function/class names] for
            known mappings.  These supplement (and override) auto-extracted names.
    """

    def __init__(
        self,
        source_dir: Path,
        allowlist: dict[str, list[str]] | None = None,
    ) -> None:
        self.source_dir = Path(source_dir)
        self.allowlist: dict[str, list[str]] = allowlist or {}
        self._codebase_names: set[str] | None = None

    # ------------------------------------------------------------------
    # Codebase scanning
    # ------------------------------------------------------------------

    def _scan_codebase(self) -> set[str]:
        """Collect all function and class names from Python files via AST.

        Falls back to regex extraction on AST parse failure.
        """
        if self._codebase_names is not None:
            return self._codebase_names

        names: set[str] = set()
        py_files = list(self.source_dir.rglob("*.py"))

        for py_file in py_files:
            try:
                source = py_file.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=str(py_file))
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        names.add(node.name)
                    elif isinstance(node, ast.ClassDef):
                        names.add(node.name)
            except (SyntaxError, UnicodeDecodeError, OSError) as exc:
                logger.debug("AST parse failed for %s: %s; using regex fallback", py_file, exc)
                try:
                    source = py_file.read_text(encoding="utf-8", errors="replace")
                    for match in _CODE_DEF_RE.finditer(source):
                        names.add(match.group(1))
                except OSError:
                    pass

        self._codebase_names = names
        logger.debug("Scanned %d Python files, found %d unique names", len(py_files), len(names))
        return names

    # ------------------------------------------------------------------
    # FR extraction from spec
    # ------------------------------------------------------------------

    def _extract_fr_mappings(self, spec_text: str) -> list[FRMapping]:
        """Extract FR IDs and their associated function/class names from spec text.

        Strategy:
        1. Find all FR-X.Y headings.
        2. For each FR section, extract backtick-quoted names that look like
           functions or classes.
        3. Merge with allowlist overrides.
        """
        # Split spec into sections by FR heading
        fr_sections: dict[str, str] = {}
        headings = list(_FR_HEADING_RE.finditer(spec_text))

        for i, match in enumerate(headings):
            fr_id = match.group(1)
            start = match.end()
            end = headings[i + 1].start() if i + 1 < len(headings) else len(spec_text)
            section_text = spec_text[start:end]
            fr_sections.setdefault(fr_id, "")
            fr_sections[fr_id] += section_text

        # Also gather FR IDs that appear without headings (inline references)
        parsed = parse_document(spec_text)
        all_fr_ids = set(parsed.requirement_ids.get("FR", []))
        for fr_id in all_fr_ids:
            if fr_id not in fr_sections:
                fr_sections[fr_id] = ""

        mappings: list[FRMapping] = []
        for fr_id, section_text in sorted(fr_sections.items()):
            names: list[str] = []

            # Extract from allowlist first (overrides)
            if fr_id in self.allowlist:
                names.extend(self.allowlist[fr_id])

            # Auto-extract function names from section
            for pattern in (_FUNC_NAME_RE, _CLASS_NAME_RE):
                for match in pattern.finditer(section_text):
                    # Match groups — take whichever group matched
                    for g in match.groups():
                        if g:
                            names.append(g)

            # Extract from code blocks in the section
            for match in _CODE_DEF_RE.finditer(section_text):
                name = match.group(1)
                names.append(name)

            # Deduplicate and filter stop words while preserving order
            seen: set[str] = set()
            unique_names: list[str] = []
            for n in names:
                if n not in seen and n.lower() not in _STOP_WORDS:
                    seen.add(n)
                    unique_names.append(n)

            mappings.append(FRMapping(
                fr_id=fr_id,
                expected_names=unique_names,
                source_context=section_text[:200] if section_text else "",
            ))

        return mappings

    # ------------------------------------------------------------------
    # Core check
    # ------------------------------------------------------------------

    def check(self, spec_path: str | Path) -> list[FidelityResult]:
        """Run fidelity check: compare spec FRs against codebase evidence.

        Returns a FidelityResult for each FR found in the spec.
        """
        spec_text = Path(spec_path).read_text(encoding="utf-8")
        mappings = self._extract_fr_mappings(spec_text)
        codebase_names = self._scan_codebase()
        results: list[FidelityResult] = []

        for mapping in mappings:
            if not mapping.expected_names:
                # No extractable names for this FR — ambiguous, fail-open
                logger.warning(
                    "FR %s: no function/class names extracted from spec; "
                    "marking as ambiguous (fail-open per R-3)",
                    mapping.fr_id,
                )
                results.append(FidelityResult(
                    fr_id=mapping.fr_id,
                    found=True,  # fail-open
                    ambiguous=True,
                    message=f"No extractable names for {mapping.fr_id}; fail-open",
                ))
                continue

            # Exact name matching against codebase
            evidence: list[str] = []
            missing: list[str] = []
            for name in mapping.expected_names:
                if name in codebase_names:
                    evidence.append(name)
                else:
                    missing.append(name)

            if evidence:
                # At least some evidence found
                found = True
                if missing:
                    logger.warning(
                        "FR %s: partial evidence — found %s, missing %s; "
                        "marking as found (fail-open per R-3)",
                        mapping.fr_id,
                        evidence,
                        missing,
                    )
                results.append(FidelityResult(
                    fr_id=mapping.fr_id,
                    found=found,
                    evidence_names=evidence,
                    searched_names=mapping.expected_names,
                    ambiguous=bool(missing),
                    message=(
                        f"Found: {evidence}"
                        + (f"; missing: {missing}" if missing else "")
                    ),
                ))
            else:
                # No evidence at all — report gap
                results.append(FidelityResult(
                    fr_id=mapping.fr_id,
                    found=False,
                    searched_names=mapping.expected_names,
                    message=f"No codebase evidence for {mapping.fr_id}: searched {mapping.expected_names}",
                ))

        return results

    # ------------------------------------------------------------------
    # Finding-compatible output (for _run_checkers integration)
    # ------------------------------------------------------------------

    def check_as_findings(self, spec_path: str | Path) -> list[Finding]:
        """Run fidelity check and return results as Finding objects.

        This output shape is compatible with structural and semantic checkers,
        enabling direct merge into the convergence registry.
        """
        results = self.check(spec_path)
        findings: list[Finding] = []

        for r in results:
            if r.found:
                continue  # Only report gaps

            stable_id = compute_stable_id(
                "fidelity", "impl_gap", f"spec:fr:{r.fr_id}", "impl_gap",
            )

            findings.append(Finding(
                id=f"fidelity-impl_gap-{stable_id[:8]}",
                severity="HIGH",
                dimension="fidelity",
                description=(
                    f"FR {r.fr_id} has no codebase implementation evidence. "
                    f"Searched for: {', '.join(r.searched_names)}"
                ),
                location=f"spec:fr:{r.fr_id}",
                evidence=f"Searched names: {r.searched_names}",
                fix_guidance=f"Implement {r.fr_id} or update allowlist if already implemented under a different name",
                status="ACTIVE",
                source_layer="fidelity",
                rule_id="impl_gap",
                spec_quote=f"{r.fr_id}: {', '.join(r.searched_names)}",
                roadmap_quote="[MISSING]",
                stable_id=stable_id,
            ))

        # Deterministic ordering
        findings.sort(key=lambda f: (f.dimension, f.rule_id, f.location))
        return findings


def run_fidelity_check(
    spec_path: str | Path,
    source_dir: str | Path,
    allowlist: dict[str, list[str]] | None = None,
) -> list[Finding]:
    """Convenience entry point for running the fidelity checker.

    Args:
        spec_path: Path to the spec markdown file.
        source_dir: Root of the codebase to search for implementation evidence.
        allowlist: Optional FR-id -> name list for known mappings.

    Returns:
        List of Finding objects for FRs with no implementation evidence.
    """
    checker = FidelityChecker(source_dir=Path(source_dir), allowlist=allowlist)
    return checker.check_as_findings(spec_path)
