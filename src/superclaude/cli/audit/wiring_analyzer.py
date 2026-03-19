"""AST-based file analyzer for ToolOrchestrator integration.

Provides ast_analyze_file() as a drop-in replacement for the default
line-based analyzer in ToolOrchestrator. Populates the `references`
field that the default analyzer leaves empty, enabling improved
dependency graph, dead code, and profile analysis.

Also provides ast_references_plugin(), a ToolOrchestrator plugin that
enriches FileAnalysis.references with import-derived cross-file
references using AST parsing. Register with:

    orchestrator.register_plugin(ast_references_plugin)

Plugin lifecycle:
1. Registered via ToolOrchestrator.register_plugin()
2. Called after primary analysis for each file
3. Parses file content with ast.parse()
4. Merges AST-derived references into FileAnalysis.references
5. Handles circular imports and missing modules gracefully

This module has zero imports from pipeline/* (NFR-007 compliance).
"""

from __future__ import annotations

import ast
import logging
from pathlib import Path

from superclaude.cli.audit.tool_orchestrator import (
    FileAnalysis,
    compute_content_hash,
)

logger = logging.getLogger(__name__)


def ast_analyze_file(file_path: str, content: str) -> FileAnalysis:
    """Parse a Python file using AST and return structured analysis.

    Drop-in replacement for ToolOrchestrator's default analyzer. Extracts:
    - imports: All import statements (import X, from X import Y)
    - exports: Symbols listed in __all__, or top-level public definitions
    - references: Cross-file name references (function calls, attribute access)

    Handles SyntaxError gracefully per R2: returns empty FileAnalysis with
    error metadata instead of raising.

    Args:
        file_path: Path to the file being analyzed.
        content: Source code content of the file.

    Returns:
        FileAnalysis with populated imports, exports, and references.
    """
    content_hash = compute_content_hash(content)
    lines = content.splitlines()

    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError as exc:
        logger.warning("SyntaxError in %s: %s — returning empty analysis", file_path, exc)
        return FileAnalysis(
            file_path=file_path,
            content_hash=content_hash,
            imports=[],
            exports=[],
            references=[],
            metadata={
                "line_count": len(lines),
                "size_bytes": len(content),
                "parse_error": str(exc),
            },
        )

    imports = _extract_imports(tree)
    exports = _extract_exports(tree)
    references = _extract_references(tree)

    return FileAnalysis(
        file_path=file_path,
        content_hash=content_hash,
        imports=imports,
        exports=exports,
        references=references,
        metadata={
            "line_count": len(lines),
            "size_bytes": len(content),
        },
    )


def _extract_imports(tree: ast.Module) -> list[str]:
    """Extract import statements from AST."""
    imports: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"from {module} import {alias.name}")

    return imports


def _extract_exports(tree: ast.Module) -> list[str]:
    """Extract exported symbols from AST.

    Looks for __all__ assignment first. If absent, collects top-level
    public function and class definitions.
    """
    # Check for __all__
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    if isinstance(node.value, (ast.List, ast.Tuple)):
                        return [
                            elt.value
                            for elt in node.value.elts
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                        ]

    # Fallback: top-level public definitions
    exports: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                exports.append(node.name)
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith("_"):
                exports.append(node.name)

    return exports


def _extract_references(tree: ast.Module) -> list[str]:
    """Extract cross-file name references from AST.

    Collects:
    - Function/method call targets
    - Attribute access chains (module.function patterns)
    - Name references in assignments and expressions
    """
    references: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            ref = _call_target_name(node)
            if ref:
                references.add(ref)
        elif isinstance(node, ast.Attribute):
            ref = _attribute_chain(node)
            if ref:
                references.add(ref)

    return sorted(references)


def _call_target_name(call: ast.Call) -> str | None:
    """Extract the target name from a Call node."""
    func = call.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return _attribute_chain(func)
    return None


def _attribute_chain(node: ast.Attribute) -> str | None:
    """Build a dotted name from an Attribute chain (e.g., foo.bar.baz)."""
    parts: list[str] = [node.attr]
    current = node.value

    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value

    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))

    return None


def ast_references_plugin(
    file_path: str,
    content: str,
    analysis: FileAnalysis,
) -> FileAnalysis:
    """ToolOrchestrator plugin that enriches FileAnalysis.references via AST.

    Parses the file content with ast.parse() and extracts cross-file
    references (function calls, attribute access chains). Merges these
    into the existing FileAnalysis.references, deduplicating.

    Handles SyntaxError and circular imports gracefully — returns the
    original analysis unchanged on parse failure.

    Args:
        file_path: Path to the file being analyzed.
        content: Source code content.
        analysis: Existing FileAnalysis from primary analyzer.

    Returns:
        FileAnalysis with enriched references field.
    """
    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError as exc:
        logger.warning(
            "ast_references_plugin: SyntaxError in %s: %s — skipping enrichment",
            file_path,
            exc,
        )
        return analysis

    ast_refs = _extract_references(tree)

    # Merge: deduplicate with existing references
    existing = set(analysis.references)
    merged = sorted(existing | set(ast_refs))

    return FileAnalysis(
        file_path=analysis.file_path,
        content_hash=analysis.content_hash,
        imports=analysis.imports,
        exports=analysis.exports,
        references=merged,
        metadata=analysis.metadata,
    )
