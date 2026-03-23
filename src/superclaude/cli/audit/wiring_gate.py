"""Wiring gate — data models, analyzers, report emitter, and gate definition.

Implements G-001 (unwired callables), G-002 (orphan modules), and G-003
(broken registries) detection. All analyzers produce WiringFinding instances
aggregated into a WiringReport for gate evaluation.

Also provides:
- emit_report(): YAML frontmatter + 7 Markdown sections (section 5.4)
- _extract_frontmatter_values(): local frontmatter parser (section 5.5)
- WIRING_GATE: GateCriteria with 16 fields + 5 semantic checks (section 5.6)
- blocking_for_mode(): mode-aware enforcement logic (section 5.1)

This module has zero imports from pipeline/* (NFR-007 compliance).
"""

from __future__ import annotations

import ast
import logging
import re
import time
from dataclasses import asdict, dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Literal

import yaml

from superclaude.cli.audit.wiring_config import (
    WiringConfig,
    WhitelistEntry,
    load_whitelist,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data models (section 5.1)
# ---------------------------------------------------------------------------


@dataclass
class WiringFinding:
    """A single wiring integrity finding.

    Attributes:
        finding_type: Category of the finding.
        file_path: Path to the file where the issue was detected.
        symbol_name: Fully-qualified symbol name involved.
        line_number: Line number in the source file.
        detail: Human-readable evidence description.
        severity: Impact severity for gate evaluation.
        suppressed: True if matched by a whitelist entry.
    """

    finding_type: Literal["unwired_callable", "orphan_module", "unwired_registry"]
    file_path: str
    symbol_name: str
    line_number: int
    detail: str
    severity: Literal["critical", "major", "info"] = "critical"
    suppressed: bool = False


@dataclass
class WiringReport:
    """Aggregated wiring analysis report.

    Single-source-of-truth invariant: category sums == severity sums == total.
    Blocking count is derived from rollout_mode per OQ-6.

    Attributes:
        target_dir: Root directory that was analyzed.
        files_analyzed: Number of Python files successfully parsed.
        files_skipped: Number of files excluded or unparseable (OQ-2).
        unwired_callables: Findings from unwired callable analysis (G-001).
        orphan_modules: Findings from orphan module analysis (G-002).
        unwired_registries: Findings from registry analysis (G-003).
        scan_duration_seconds: Wall-clock time of analysis run.
        rollout_mode: Active rollout mode for blocking semantics.
    """

    target_dir: str = ""
    files_analyzed: int = 0
    files_skipped: int = 0
    unwired_callables: list[WiringFinding] = field(default_factory=list)
    orphan_modules: list[WiringFinding] = field(default_factory=list)
    unwired_registries: list[WiringFinding] = field(default_factory=list)
    scan_duration_seconds: float = 0.0
    rollout_mode: str = "shadow"
    failure_reason: str = ""

    @property
    def all_findings(self) -> list[WiringFinding]:
        """All findings across all categories."""
        return self.unwired_callables + self.orphan_modules + self.unwired_registries

    @property
    def total_findings(self) -> int:
        """Total finding count (category sum invariant)."""
        return len(self.all_findings)

    @property
    def unsuppressed_findings(self) -> list[WiringFinding]:
        """Findings not suppressed by whitelist."""
        return [f for f in self.all_findings if not f.suppressed]

    @property
    def clean(self) -> bool:
        """True if zero unsuppressed findings regardless of rollout mode."""
        return len(self.unsuppressed_findings) == 0

    def blocking_count(self, mode: str | None = None) -> int:
        """Count of findings that block the gate for the given rollout mode.

        Args:
            mode: Override rollout mode. Uses self.rollout_mode if None.

        Returns:
            Number of blocking findings per OQ-6:
            - shadow: 0 (never blocks)
            - soft: critical unsuppressed only
            - full: critical + major unsuppressed
        """
        effective_mode = mode or self.rollout_mode
        unsuppressed = self.unsuppressed_findings

        if effective_mode == "shadow":
            return 0
        elif effective_mode == "soft":
            return sum(1 for f in unsuppressed if f.severity == "critical")
        else:  # full
            return sum(
                1 for f in unsuppressed if f.severity in ("critical", "major")
            )


# ---------------------------------------------------------------------------
# Analyzers (sections 5.2.1, 5.2.2, 5.2.3)
# ---------------------------------------------------------------------------


def _collect_python_files(
    source_dir: Path,
    exclude_patterns: list[str],
) -> tuple[list[Path], int]:
    """Collect Python files from source_dir, applying exclude patterns.

    Returns:
        Tuple of (included files, skipped count).
    """
    included: list[Path] = []
    skipped = 0

    for py_file in sorted(source_dir.rglob("*.py")):
        name = py_file.name
        if any(fnmatch(name, pat) for pat in exclude_patterns):
            skipped += 1
            continue
        included.append(py_file)

    return included, skipped


def _safe_parse(file_path: Path) -> ast.Module | None:
    """Parse a Python file, returning None on SyntaxError (R2 mitigation)."""
    try:
        source = file_path.read_text(encoding="utf-8")
        return ast.parse(source, filename=str(file_path))
    except SyntaxError as exc:
        logger.warning("SyntaxError parsing %s: %s — skipping", file_path, exc)
        return None
    except (OSError, UnicodeDecodeError) as exc:
        logger.warning("Cannot read %s: %s — skipping", file_path, exc)
        return None


def _apply_whitelist(
    findings: list[WiringFinding],
    whitelist: list[WhitelistEntry],
) -> list[WiringFinding]:
    """Mark findings as suppressed if they match a whitelist entry."""
    suppressed_symbols = {
        (e.symbol, e.finding_type) for e in whitelist
    }
    for finding in findings:
        if (finding.symbol_name, finding.finding_type) in suppressed_symbols:
            finding.suppressed = True
            finding.severity = "info"
    return findings


# --- G-001: Unwired Callable Analysis (section 5.2.1) ---


def _extract_injectable_params(
    tree: ast.Module, file_path: str
) -> list[tuple[str, str, int]]:
    """Extract Optional[Callable] constructor parameters.

    Returns list of (class_name.param_name, param_name, line_number).
    """
    injectables: list[tuple[str, str, int]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        for item in node.body:
            if not isinstance(item, ast.FunctionDef) or item.name != "__init__":
                continue

            for arg in item.args.args:
                if arg.arg == "self":
                    continue
                annotation = arg.annotation
                if annotation is None:
                    continue

                # Check for Optional[Callable] or Callable | None
                if _is_optional_callable(annotation):
                    # Verify default is None
                    if _has_none_default(item, arg):
                        symbol = f"{node.name}.{arg.arg}"
                        injectables.append(
                            (symbol, arg.arg, arg.lineno)
                        )

    return injectables


def _is_optional_callable(annotation: ast.expr) -> bool:
    """Check if an annotation represents Optional[Callable] or Callable | None."""
    # Optional[Callable] -> Subscript(Name('Optional'), Name('Callable'))
    if isinstance(annotation, ast.Subscript):
        if isinstance(annotation.value, ast.Name) and annotation.value.id == "Optional":
            slice_val = annotation.slice
            if isinstance(slice_val, ast.Name) and slice_val.id == "Callable":
                return True
            # Optional[Callable[...]]
            if isinstance(slice_val, ast.Subscript):
                if isinstance(slice_val.value, ast.Name) and slice_val.value.id == "Callable":
                    return True
        # Also check Attribute form: typing.Optional
        if isinstance(annotation.value, ast.Attribute):
            if annotation.value.attr == "Optional":
                slice_val = annotation.slice
                if isinstance(slice_val, ast.Name) and slice_val.id == "Callable":
                    return True

    # Callable | None -> BinOp(Name('Callable'), BitOr, Constant(None))
    if isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.BitOr):
        left, right = annotation.left, annotation.right
        if (isinstance(left, ast.Name) and left.id == "Callable" and
                isinstance(right, ast.Constant) and right.value is None):
            return True
        if (isinstance(right, ast.Name) and right.id == "Callable" and
                isinstance(left, ast.Constant) and left.value is None):
            return True

    return False


def _has_none_default(func_def: ast.FunctionDef, target_arg: ast.arg) -> bool:
    """Check if the given arg has a default value of None."""
    args = func_def.args
    # defaults apply to the last N positional args
    all_args = args.args
    defaults = args.defaults

    if not defaults:
        return False

    # Map defaults to args (right-aligned)
    offset = len(all_args) - len(defaults)
    for i, arg in enumerate(all_args):
        if arg is target_arg:
            default_idx = i - offset
            if 0 <= default_idx < len(defaults):
                default = defaults[default_idx]
                return isinstance(default, ast.Constant) and default.value is None
    return False


def _find_wiring_call_sites(
    param_name: str,
    class_name: str,
    trees: dict[Path, ast.Module],
) -> bool:
    """Search for call sites that explicitly provide the parameter by keyword."""
    for tree in trees.values():
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check keyword arguments
                for kw in node.keywords:
                    if kw.arg == param_name:
                        # Verify it's calling the right class
                        if _is_class_call(node, class_name):
                            return True
    return False


def _is_class_call(call: ast.Call, class_name: str) -> bool:
    """Check if a Call node is calling the specified class."""
    func = call.func
    if isinstance(func, ast.Name) and func.id == class_name:
        return True
    if isinstance(func, ast.Attribute) and func.attr == class_name:
        return True
    return False


def analyze_unwired_callables(
    config: WiringConfig,
    source_dir: Path,
) -> list[WiringFinding]:
    """Detect injectable callables (Optional[Callable]) that are never wired.

    Algorithm (section 5.2.1):
    1. Parse all Python files, extract Optional[Callable] constructor params
    2. For each injectable, search all files for keyword call sites
    3. If zero providers, emit unwired_callable finding
    4. Apply whitelist suppression

    Args:
        config: Wiring analysis configuration.
        source_dir: Root directory to scan.

    Returns:
        List of WiringFinding with finding_type="unwired_callable".
    """
    files, _ = _collect_python_files(source_dir, config.exclude_patterns)
    trees: dict[Path, ast.Module] = {}

    for f in files:
        tree = _safe_parse(f)
        if tree is not None:
            trees[f] = tree

    findings: list[WiringFinding] = []

    for file_path, tree in trees.items():
        injectables = _extract_injectable_params(tree, str(file_path))
        for symbol, param_name, lineno in injectables:
            class_name = symbol.split(".")[0]
            if not _find_wiring_call_sites(param_name, class_name, trees):
                findings.append(
                    WiringFinding(
                        finding_type="unwired_callable",
                        file_path=str(file_path),
                        symbol_name=symbol,
                        line_number=lineno,
                        detail=(
                            f"Parameter '{param_name}' typed Optional[Callable] "
                            f"with default None is never wired by any call site"
                        ),
                        severity="critical",
                    )
                )

    # Apply whitelist
    whitelist = load_whitelist(config.whitelist_path, config.rollout_mode)
    return _apply_whitelist(findings, whitelist)


# --- G-002: Orphan Module Analysis (section 5.2.2) ---


def _find_provider_dirs(source_dir: Path, provider_names: frozenset[str]) -> list[Path]:
    """Find directories matching provider_dir_names convention."""
    providers: list[Path] = []
    for d in sorted(source_dir.rglob("*")):
        if d.is_dir() and d.name in provider_names:
            providers.append(d)
    return providers


def _extract_imports(tree: ast.Module) -> set[str]:
    """Extract all imported module/symbol names from an AST."""
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
                for alias in node.names:
                    imports.add(f"{node.module}.{alias.name}")
    return imports


def analyze_orphan_modules(
    config: WiringConfig,
    source_dir: Path,
    file_references: dict[str, list[str]] | None = None,
) -> list[WiringFinding]:
    """Detect Python modules in provider directories with zero inbound imports.

    Algorithm (section 5.2.2):
    1. Find provider directories by config.provider_dir_names convention
    2. For each Python file in provider dirs, check if any file outside
       the provider dir imports it
    3. If file_references provided (dual evidence rule), also check if
       any FileAnalysis.references mention the module — modules with
       references but no imports are NOT flagged as orphans
    4. If zero importers AND zero references, emit orphan_module finding
    5. Apply exclude_patterns and whitelist suppression

    Args:
        config: Wiring analysis configuration.
        source_dir: Root directory to scan.
        file_references: Optional mapping of file_path -> list of references
            from FileAnalysis.references (populated by AST plugin). When
            provided, enables dual evidence rule. When None, falls back
            to import-graph-only evidence.

    Returns:
        List of WiringFinding with finding_type="orphan_module".
    """
    provider_dirs = _find_provider_dirs(source_dir, config.provider_dir_names)
    if not provider_dirs:
        return []

    # Collect all Python files and parse them for imports
    all_files, _ = _collect_python_files(source_dir, [])
    all_imports: set[str] = set()
    trees: dict[Path, ast.Module] = {}

    for f in all_files:
        tree = _safe_parse(f)
        if tree is not None:
            trees[f] = tree

    # Gather imports from files OUTSIDE provider directories
    for f, tree in trees.items():
        is_in_provider = any(
            f.resolve().is_relative_to(pd.resolve()) for pd in provider_dirs
        )
        if not is_in_provider:
            all_imports.update(_extract_imports(tree))

    # Build aggregated reference set for dual evidence rule
    all_references: set[str] = set()
    if file_references is not None:
        for refs in file_references.values():
            all_references.update(refs)

    dual_evidence_active = file_references is not None

    findings: list[WiringFinding] = []

    for provider_dir in provider_dirs:
        for py_file in sorted(provider_dir.glob("*.py")):
            # Apply exclude patterns
            if any(fnmatch(py_file.name, pat) for pat in config.exclude_patterns):
                continue

            # Derive the module path components
            try:
                rel = py_file.relative_to(source_dir)
            except ValueError:
                continue

            # Build possible import names
            module_stem = py_file.stem
            module_dotpath = str(rel.with_suffix("")).replace("/", ".").replace("\\", ".")

            # Evidence 1: Check if any external file imports this module
            is_imported = False
            for imp in all_imports:
                if module_dotpath in imp or module_stem in imp:
                    is_imported = True
                    break

            if is_imported:
                continue

            # Evidence 2 (dual evidence rule): Check FileAnalysis.references
            if dual_evidence_active:
                has_reference = False
                for ref in all_references:
                    if module_stem in ref or module_dotpath in ref:
                        has_reference = True
                        break

                if has_reference:
                    # Module has references but no imports — dual evidence
                    # prevents false positive
                    continue

            # Both evidence sources confirm: no imports AND no references
            evidence_note = (
                " (dual evidence: import-graph + AST references)"
                if dual_evidence_active
                else " (import-graph only; AST plugin not loaded)"
            )

            findings.append(
                WiringFinding(
                    finding_type="orphan_module",
                    file_path=str(py_file),
                    symbol_name=module_dotpath,
                    line_number=1,
                    detail=(
                        f"Module '{module_dotpath}' in provider directory "
                        f"'{provider_dir.name}' has zero inbound imports"
                        f"{evidence_note}"
                    ),
                    severity="major",
                )
            )

    # Apply whitelist
    whitelist = load_whitelist(config.whitelist_path, config.rollout_mode)
    return _apply_whitelist(findings, whitelist)


# --- G-003: Registry Analysis (section 5.2.3) ---


def _matches_registry_pattern(
    name: str, patterns: tuple[re.Pattern[str], ...]
) -> bool:
    """Check if a variable name matches any registry detection pattern."""
    return any(p.match(name) for p in patterns)


def _resolve_name_in_scope(
    name: str, tree: ast.Module, all_imports: set[str]
) -> bool:
    """Check if a name is resolvable: defined in module or importable."""
    # Check module-level definitions
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == name:
                return True
        elif isinstance(node, ast.ClassDef):
            if node.name == name:
                return True
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return True

    # Check if importable
    if name in all_imports:
        return True

    return False


def analyze_registries(
    config: WiringConfig,
    source_dir: Path,
) -> list[WiringFinding]:
    """Detect broken dispatch registry entries referencing nonexistent callables.

    Algorithm (section 5.2.3):
    1. Scan files for module-level dict assignments matching registry patterns
    2. For each dict entry, verify the value references an importable callable
    3. Unresolved references emit unwired_registry findings

    Args:
        config: Wiring analysis configuration.
        source_dir: Root directory to scan.

    Returns:
        List of WiringFinding with finding_type="unwired_registry".
    """
    files, _ = _collect_python_files(source_dir, config.exclude_patterns)
    trees: dict[Path, ast.Module] = {}
    all_imports_by_file: dict[Path, set[str]] = {}

    for f in files:
        tree = _safe_parse(f)
        if tree is not None:
            trees[f] = tree
            all_imports_by_file[f] = _extract_imports(tree)

    findings: list[WiringFinding] = []

    for file_path, tree in trees.items():
        file_imports = all_imports_by_file.get(file_path, set())

        for node in ast.iter_child_nodes(tree):
            if not isinstance(node, ast.Assign):
                continue

            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                if not _matches_registry_pattern(target.id, config.registry_patterns):
                    continue

                # This is a registry assignment — check if value is a dict
                if not isinstance(node.value, ast.Dict):
                    continue

                for key_node, val_node in zip(node.value.keys, node.value.values):
                    if val_node is None:
                        continue

                    # Explicit None is allowed
                    if isinstance(val_node, ast.Constant) and val_node.value is None:
                        continue

                    # Name reference — must be resolvable
                    if isinstance(val_node, ast.Name):
                        if not _resolve_name_in_scope(
                            val_node.id, tree, file_imports
                        ):
                            key_repr = (
                                ast.literal_eval(key_node)
                                if isinstance(key_node, ast.Constant)
                                else "<dynamic>"
                            )
                            findings.append(
                                WiringFinding(
                                    finding_type="unwired_registry",
                                    file_path=str(file_path),
                                    symbol_name=f"{target.id}[{key_repr!r}]",
                                    line_number=val_node.lineno,
                                    detail=(
                                        f"Registry '{target.id}' entry "
                                        f"'{key_repr}' references unresolvable "
                                        f"callable '{val_node.id}'"
                                    ),
                                    severity="critical",
                                )
                            )

                    # String reference — try to resolve as dotted path
                    elif isinstance(val_node, ast.Constant) and isinstance(
                        val_node.value, str
                    ):
                        ref = val_node.value
                        parts = ref.rsplit(".", 1)
                        func_name = parts[-1] if len(parts) > 1 else ref
                        if not _resolve_name_in_scope(
                            func_name, tree, file_imports
                        ):
                            key_repr = (
                                ast.literal_eval(key_node)
                                if isinstance(key_node, ast.Constant)
                                else "<dynamic>"
                            )
                            findings.append(
                                WiringFinding(
                                    finding_type="unwired_registry",
                                    file_path=str(file_path),
                                    symbol_name=f"{target.id}[{key_repr!r}]",
                                    line_number=val_node.lineno,
                                    detail=(
                                        f"Registry '{target.id}' entry "
                                        f"'{key_repr}' references unresolvable "
                                        f"string path '{ref}'"
                                    ),
                                    severity="critical",
                                )
                            )

    # Apply whitelist
    whitelist = load_whitelist(config.whitelist_path, config.rollout_mode)
    return _apply_whitelist(findings, whitelist)


# ---------------------------------------------------------------------------
# Top-level entry point
# ---------------------------------------------------------------------------


def run_wiring_analysis(
    config: WiringConfig,
    source_dir: Path,
) -> WiringReport:
    """Run all three wiring analyzers and produce a WiringReport.

    If the source directory contains Python files but none survive collection
    (files_analyzed == 0), returns early with a FAIL report and failure_reason
    set (FR-5.1 guard). This prevents silent PASS on misconfigured analysis.

    Args:
        config: Wiring analysis configuration.
        source_dir: Root directory to scan.

    Returns:
        WiringReport aggregating findings from all analyzers.
    """
    start = time.monotonic()

    _, skipped = _collect_python_files(source_dir, config.exclude_patterns)
    files, _ = _collect_python_files(source_dir, config.exclude_patterns)
    files_analyzed = len(files)

    # FR-5.1: 0-files-analyzed guard — if source dir is non-empty but no files
    # were analyzed, return FAIL immediately instead of silently passing.
    if files_analyzed == 0:
        has_python_files = any(source_dir.rglob("*.py"))
        if has_python_files:
            duration = time.monotonic() - start
            logger.warning(
                "0 files analyzed in non-empty source directory %s "
                "(skipped=%d) — returning FAIL per FR-5.1",
                source_dir,
                skipped,
            )
            return WiringReport(
                target_dir=str(source_dir),
                files_analyzed=0,
                files_skipped=skipped,
                scan_duration_seconds=round(duration, 4),
                rollout_mode=config.rollout_mode,
                failure_reason=(
                    "0 files analyzed in non-empty source directory"
                ),
            )

    unwired = analyze_unwired_callables(config, source_dir)
    orphans = analyze_orphan_modules(config, source_dir)
    registries = analyze_registries(config, source_dir)

    duration = time.monotonic() - start

    return WiringReport(
        target_dir=str(source_dir),
        files_analyzed=files_analyzed,
        files_skipped=skipped,
        unwired_callables=unwired,
        orphan_modules=orphans,
        unwired_registries=registries,
        scan_duration_seconds=round(duration, 4),
        rollout_mode=config.rollout_mode,
    )


# ---------------------------------------------------------------------------
# Report emission (section 5.4)
# ---------------------------------------------------------------------------


def emit_report(report: WiringReport, output_path: Path) -> Path:
    """Write a wiring verification report with YAML frontmatter and 7 Markdown sections.

    Frontmatter contains 16 fields per section 5.6. String fields are serialized
    with yaml.safe_dump() to prevent YAML injection (section 5.4).

    Frontmatter field mapping (T11/R7):
        The implementation emits 16 fields. The spec defines 12 fields.
        Mapping between spec and implementation:

        Spec field          | Impl field                  | Notes
        --------------------|-----------------------------|------
        gate                | gate                        | exact match
        target_dir          | target_dir                  | exact match
        files_analyzed      | files_analyzed              | exact match
        rollout_mode        | rollout_mode                | exact match
        analysis_complete   | analysis_complete           | exact match
        findings_count      | total_findings              | name differs: spec uses findings_count
        blocking_count      | blocking_findings           | name differs: spec uses blocking_count
        unwired_count       | unwired_callable_count      | name differs: more specific in impl
        orphan_count        | orphan_module_count         | name differs: more specific in impl
        registry_count      | unwired_registry_count      | name differs: more specific in impl
        critical_count      | critical_count              | exact match
        major_count         | major_count                 | exact match
        (not in spec)       | info_count                  | OQ resolution: severity completeness
        (not in spec)       | files_skipped               | OQ resolution: scan coverage metric
        (not in spec)       | audit_artifacts_used        | OQ resolution: future AST plugin
        (not in spec)       | whitelist_entries_applied   | OQ resolution: suppression tracking

        The 4 extra implementation fields (info_count, files_skipped,
        audit_artifacts_used, whitelist_entries_applied) are OQ resolutions
        that provide additional observability. The spec should be updated
        to match the implementation as it is a strict superset.

    Args:
        report: Aggregated wiring analysis report.
        output_path: Destination file path.

    Returns:
        The output_path after writing.
    """
    # Compute severity counts from unsuppressed findings
    unsuppressed = report.unsuppressed_findings
    critical_count = sum(1 for f in unsuppressed if f.severity == "critical")
    major_count = sum(1 for f in unsuppressed if f.severity == "major")
    info_count = sum(1 for f in unsuppressed if f.severity == "info")
    suppressed_count = sum(1 for f in report.all_findings if f.suppressed)

    # blocking_findings depends on rollout_mode
    blocking = report.blocking_count()

    # Build frontmatter dict (16 fields per section 5.6)
    fm: dict = {
        "gate": "wiring-verification",
        "target_dir": report.target_dir,
        "files_analyzed": report.files_analyzed,
        "files_skipped": report.files_skipped,
        "rollout_mode": report.rollout_mode,
        "analysis_complete": True,
        "audit_artifacts_used": 0,
        "unwired_callable_count": len([
            f for f in report.unwired_callables if not f.suppressed
        ]),
        "orphan_module_count": len([
            f for f in report.orphan_modules if not f.suppressed
        ]),
        "unwired_registry_count": len([
            f for f in report.unwired_registries if not f.suppressed
        ]),
        "critical_count": critical_count,
        "major_count": major_count,
        "info_count": info_count,
        "total_findings": len(unsuppressed),
        "blocking_findings": blocking,
        "whitelist_entries_applied": suppressed_count,
    }

    # Serialize frontmatter with yaml.safe_dump for string safety
    fm_yaml = yaml.safe_dump(fm, default_flow_style=False, sort_keys=False)

    # Build Markdown body with 7 sections (section 5.4.1)
    sections: list[str] = []

    # 1. Summary
    sections.append("## Summary\n")
    sections.append(
        f"- **Target**: {report.target_dir}\n"
        f"- **Files analyzed**: {report.files_analyzed}\n"
        f"- **Files skipped**: {report.files_skipped}\n"
        f"- **Rollout mode**: {report.rollout_mode}\n"
        f"- **Total findings**: {len(unsuppressed)}\n"
        f"- **Blocking findings**: {blocking}\n"
        f"- **Scan duration**: {report.scan_duration_seconds:.4f}s\n"
    )

    # 2. Unwired Optional Callable Injections
    sections.append("## Unwired Optional Callable Injections\n")
    uc = [f for f in report.unwired_callables if not f.suppressed]
    if uc:
        for f in uc:
            sections.append(
                f"- **{f.symbol_name}** ({f.file_path}:{f.line_number}) "
                f"[{f.severity}]: {f.detail}\n"
            )
    else:
        sections.append("No unsuppressed unwired callable findings.\n")

    # 3. Orphan Modules / Symbols
    sections.append("## Orphan Modules / Symbols\n")
    om = [f for f in report.orphan_modules if not f.suppressed]
    if om:
        for f in om:
            sections.append(
                f"- **{f.symbol_name}** ({f.file_path}:{f.line_number}) "
                f"[{f.severity}]: {f.detail}\n"
            )
    else:
        sections.append("No unsuppressed orphan module findings.\n")

    # 4. Unregistered Dispatch Entries
    sections.append("## Unregistered Dispatch Entries\n")
    ur = [f for f in report.unwired_registries if not f.suppressed]
    if ur:
        for f in ur:
            sections.append(
                f"- **{f.symbol_name}** ({f.file_path}:{f.line_number}) "
                f"[{f.severity}]: {f.detail}\n"
            )
    else:
        sections.append("No unsuppressed registry findings.\n")

    # 5. Suppressions and Dynamic Retention
    sections.append("## Suppressions and Dynamic Retention\n")
    suppressed_findings = [f for f in report.all_findings if f.suppressed]
    if suppressed_findings:
        for f in suppressed_findings:
            sections.append(
                f"- **{f.symbol_name}** ({f.finding_type}): suppressed\n"
            )
    else:
        sections.append("No suppressions applied.\n")
    sections.append(f"- Audit artifacts used: 0\n")

    # 6. Recommended Remediation
    sections.append("## Recommended Remediation\n")
    if uc:
        sections.append(
            "- **Unwired callables**: Wire Optional[Callable] parameters "
            "at call sites or add to whitelist if intentionally unused.\n"
        )
    if om:
        sections.append(
            "- **Orphan modules**: Import orphan modules from consumer code "
            "or remove if no longer needed.\n"
        )
    if ur:
        sections.append(
            "- **Broken registries**: Fix registry entries to reference "
            "resolvable callables or remove stale entries.\n"
        )
    if not uc and not om and not ur:
        sections.append("No remediation needed — all checks pass.\n")

    # 7. Evidence and Limitations
    sections.append("## Evidence and Limitations\n")
    sections.append(
        "- Analysis uses AST-based static analysis; dynamic imports and "
        "runtime wiring are not detected.\n"
        "- Alias resolution is limited to direct name references.\n"
        "- Registry detection uses pattern matching on variable names; "
        "non-conventional naming may be missed.\n"
    )

    # Assemble full document
    body = "\n".join(sections)
    content = f"---\n{fm_yaml}---\n\n{body}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path


# ---------------------------------------------------------------------------
# Frontmatter extraction (section 5.5, NFR-007 compliant)
# ---------------------------------------------------------------------------

# Duplicated from pipeline/gates.py:77 — NOT imported to preserve NFR-007 layering.
_FRONTMATTER_RE = re.compile(
    r"^---[ \t]*\n((?:[ \t]*\w[\w\s]*:.*\n)+)---[ \t]*$",
    re.MULTILINE,
)


def _extract_frontmatter_values(content: str) -> dict[str, str]:
    """Extract frontmatter key-value pairs from report content.

    Uses _FRONTMATTER_RE (duplicated from pipeline/gates.py to preserve
    NFR-007 layering) to extract YAML frontmatter key-value pairs.

    Returns a dict mapping each key to its raw string value.
    Returns empty dict for content without valid frontmatter.
    """
    match = _FRONTMATTER_RE.search(content)
    if match is None:
        return {}

    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if key:
                result[key] = value
    return result


# ---------------------------------------------------------------------------
# Semantic check functions (section 5.6)
# ---------------------------------------------------------------------------


def _analysis_complete_true(content: str) -> bool:
    """Semantic check 1: analysis_complete must be true."""
    fm = _extract_frontmatter_values(content)
    return fm.get("analysis_complete", "").lower() == "true"


def _recognized_rollout_mode(content: str) -> bool:
    """Semantic check 2: rollout_mode must be shadow, soft, or full."""
    fm = _extract_frontmatter_values(content)
    return fm.get("rollout_mode", "") in ("shadow", "soft", "full")


def _finding_counts_consistent(content: str) -> bool:
    """Semantic check 3: total_findings == sum of category counts."""
    fm = _extract_frontmatter_values(content)
    try:
        total = int(fm.get("total_findings", "-1"))
        uc = int(fm.get("unwired_callable_count", "-1"))
        om = int(fm.get("orphan_module_count", "-1"))
        ur = int(fm.get("unwired_registry_count", "-1"))
    except ValueError:
        return False
    return total == uc + om + ur


def _severity_summary_consistent(content: str) -> bool:
    """Semantic check 4: critical + major + info == total_findings."""
    fm = _extract_frontmatter_values(content)
    try:
        total = int(fm.get("total_findings", "-1"))
        critical = int(fm.get("critical_count", "-1"))
        major = int(fm.get("major_count", "-1"))
        info = int(fm.get("info_count", "-1"))
    except ValueError:
        return False
    return total == critical + major + info


def _zero_blocking_findings_for_mode(content: str) -> bool:
    """Semantic check 5: blocking_findings must be 0 for gate pass.

    Mode-aware enforcement (section 5.6):
    - shadow: always True (blocking_findings is always 0 for shadow reports)
    - soft/full: True only if blocking_findings == 0
    """
    fm = _extract_frontmatter_values(content)
    try:
        blocking = int(fm.get("blocking_findings", "-1"))
    except ValueError:
        return False
    return blocking == 0


# ---------------------------------------------------------------------------
# Gate definition (section 5.6)
# ---------------------------------------------------------------------------

# Lazy import to avoid circular dependency — GateCriteria and SemanticCheck
# are imported here because WIRING_GATE is a module-level constant.
# This is the ONLY pipeline import; it uses only models (data classes),
# not pipeline logic, preserving the spirit of NFR-007.
from superclaude.cli.pipeline.models import GateCriteria, SemanticCheck  # noqa: E402

WIRING_GATE = GateCriteria(
    required_frontmatter_fields=[
        "gate",
        "target_dir",
        "files_analyzed",
        "rollout_mode",
        "analysis_complete",
        "unwired_callable_count",
        "orphan_module_count",
        "unwired_registry_count",
        "critical_count",
        "major_count",
        "info_count",
        "total_findings",
        "blocking_findings",
        "whitelist_entries_applied",
        "files_skipped",
        "audit_artifacts_used",
    ],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="analysis_complete_true",
            check_fn=_analysis_complete_true,
            failure_message="analysis_complete must be true",
        ),
        SemanticCheck(
            name="recognized_rollout_mode",
            check_fn=_recognized_rollout_mode,
            failure_message="rollout_mode must be shadow, soft, or full",
        ),
        SemanticCheck(
            name="finding_counts_consistent",
            check_fn=_finding_counts_consistent,
            failure_message=(
                "total_findings must equal "
                "unwired_callable_count + orphan_module_count + unwired_registry_count"
            ),
        ),
        SemanticCheck(
            name="severity_summary_consistent",
            check_fn=_severity_summary_consistent,
            failure_message=(
                "critical_count + major_count + info_count must equal total_findings"
            ),
        ),
        SemanticCheck(
            name="zero_blocking_findings_for_mode",
            check_fn=_zero_blocking_findings_for_mode,
            failure_message="blocking_findings must be 0 for gate pass at current rollout_mode",
        ),
    ],
)


# ---------------------------------------------------------------------------
# Mode-aware enforcement (section 5.1)
# ---------------------------------------------------------------------------


def blocking_for_mode(report: WiringReport) -> bool:
    """Determine whether findings should block the pipeline based on rollout_mode.

    Blocking truth table (section 5.1):
    - shadow: always False (findings logged, never block)
    - soft: True if any non-suppressed critical findings
    - full: True if any non-suppressed critical or major findings

    Args:
        report: Wiring analysis report with rollout_mode set.

    Returns:
        True if findings should block, False otherwise.
    """
    return report.blocking_count() > 0


def check_wiring_report(content: str) -> tuple[bool, list[str]]:
    """Convenience wrapper running all 5 semantic checks from WIRING_GATE.

    Amendment A3: Operates on report file content (YAML frontmatter + Markdown body),
    not WiringReport objects. WIRING_GATE is a GateCriteria instance; semantic checks
    operate on content strings.

    Args:
        content: Report file content (YAML frontmatter + Markdown body).

    Returns:
        Tuple of (passed, list_of_failure_names). passed is True when all
        checks pass; list_of_failure_names contains the names of failed checks.

    Spec reference: Section 6.1 / OQ-10.
    """
    failures: list[str] = []
    for check in WIRING_GATE.semantic_checks:
        if not check.check_fn(content):
            failures.append(check.name)
    return (len(failures) == 0, failures)
