"""AST call-chain reachability analyzer for wiring manifest validation.

Implements FR-4.2: static analysis tool that determines whether target symbols
are reachable from declared entry points via static call chains.

Algorithm:
    1. ``ast.parse()`` each module encountered
    2. Build a per-module call graph (function -> set of called names)
    3. Resolve cross-module imports (``import X``, ``from X import Y``,
       relative imports) to discover additional modules
    4. BFS from the entry-point function to compute the full reachable set
    5. Report any manifest target NOT in the reachable set as a GAP

Cross-module import resolution:
    - ``from X import Y`` is resolved by converting the dotted module path
      to a filesystem path relative to ``source_root``
    - Relative imports (``from . import X``, ``from ..sub import Y``) are
      resolved against the importing module's package directory
    - Missing modules are recorded but do not crash the analyzer

Lazy import handling:
    - Imports inside ``ast.FunctionDef`` / ``ast.AsyncFunctionDef`` bodies
      ARE included in the call graph for that function, because these are
      real runtime paths (e.g. circular-dependency avoidance patterns)

Documented limitations (NFR-6):
    1. **Dynamic dispatch false negatives** — calls via ``getattr()``,
       ``**kwargs`` delegation, string-based dispatch (e.g. registry
       lookups like ``REGISTRY[key]()``) are invisible to static AST
       analysis. The analyzer will report these targets as UNREACHABLE
       even if they execute at runtime. Mitigation: use the wiring
       manifest ``required_reachable`` entries to declare expectations
       and accept known false negatives via allowlists.
    2. **TYPE_CHECKING exclusions** — imports guarded by
       ``if TYPE_CHECKING:`` blocks are excluded from the call graph
       because they never execute at runtime.
    3. **Function-scope lazy imports included** — imports nested inside
       function bodies (e.g. ``def foo(): from bar import baz``) are
       treated as reachable from that function. This is correct for
       circular-import-avoidance patterns but may over-report reachability
       for conditionally-unreachable lazy imports.
"""

from __future__ import annotations

import ast
import logging
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class EntryPoint:
    """A declared entry point from the wiring manifest."""

    module: str
    function: str


@dataclass
class ReachableTarget:
    """A symbol that must be reachable from an entry point."""

    target: str
    from_entry: str
    spec_ref: str


@dataclass
class ReachabilityResult:
    """Result for a single required_reachable entry."""

    target: str
    from_entry: str
    spec_ref: str
    reachable: bool
    chain: list[str] = field(default_factory=list)
    """Call chain from entry to target, empty if unreachable."""

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "from_entry": self.from_entry,
            "spec_ref": self.spec_ref,
            "reachable": self.reachable,
            "chain": self.chain,
        }


@dataclass
class ReachabilityReport:
    """Aggregate report for all manifest targets."""

    results: list[ReachabilityResult] = field(default_factory=list)
    gaps: list[ReachabilityResult] = field(default_factory=list)
    modules_parsed: int = 0
    modules_failed: list[str] = field(default_factory=list)
    passed: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "total_targets": len(self.results),
            "reachable_count": sum(1 for r in self.results if r.reachable),
            "gap_count": len(self.gaps),
            "gaps": [g.to_dict() for g in self.gaps],
            "results": [r.to_dict() for r in self.results],
            "modules_parsed": self.modules_parsed,
            "modules_failed": self.modules_failed,
        }


# ---------------------------------------------------------------------------
# Manifest loader
# ---------------------------------------------------------------------------


def load_manifest(manifest_path: Path) -> tuple[list[EntryPoint], list[ReachableTarget]]:
    """Load and validate a wiring manifest YAML file.

    Args:
        manifest_path: Path to the YAML manifest file.

    Returns:
        Tuple of (entry_points, required_reachable).

    Raises:
        ValueError: If the manifest is malformed or fails validation rules.
    """
    with open(manifest_path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "wiring_manifest" not in data:
        raise ValueError("Manifest must contain a top-level 'wiring_manifest' key")

    manifest = data["wiring_manifest"]

    # --- entry_points ---
    raw_eps = manifest.get("entry_points")
    if not raw_eps or not isinstance(raw_eps, list):
        raise ValueError("wiring_manifest.entry_points must be a non-empty list")

    entry_points: list[EntryPoint] = []
    ep_functions: set[str] = set()
    for ep in raw_eps:
        if not isinstance(ep, dict) or "module" not in ep or "function" not in ep:
            raise ValueError(f"Each entry_point must have 'module' and 'function': {ep}")
        entry_points.append(EntryPoint(module=ep["module"], function=ep["function"]))
        ep_functions.add(ep["function"])

    # --- required_reachable ---
    raw_targets = manifest.get("required_reachable")
    if not raw_targets or not isinstance(raw_targets, list):
        raise ValueError("wiring_manifest.required_reachable must be a non-empty list")

    targets: list[ReachableTarget] = []
    seen_pairs: set[tuple[str, str]] = set()
    for t in raw_targets:
        if not isinstance(t, dict):
            raise ValueError(f"Each required_reachable entry must be a dict: {t}")
        for key in ("target", "from_entry", "spec_ref"):
            if key not in t or not t[key]:
                raise ValueError(f"required_reachable entry missing '{key}': {t}")
        if "." not in t["target"]:
            raise ValueError(
                f"target must be fully-qualified (contain at least one dot): {t['target']}"
            )
        if t["from_entry"] not in ep_functions:
            raise ValueError(
                f"from_entry '{t['from_entry']}' not found in entry_points: "
                f"{sorted(ep_functions)}"
            )
        pair = (t["target"], t["from_entry"])
        if pair in seen_pairs:
            raise ValueError(f"Duplicate (target, from_entry) pair: {pair}")
        seen_pairs.add(pair)
        targets.append(
            ReachableTarget(
                target=t["target"],
                from_entry=t["from_entry"],
                spec_ref=t["spec_ref"],
            )
        )

    return entry_points, targets


# ---------------------------------------------------------------------------
# AST call-graph builder
# ---------------------------------------------------------------------------


class _CallGraphVisitor(ast.NodeVisitor):
    """Build a per-module call graph from AST.

    For each function/method definition, collects:
    - Names called via ``ast.Call`` nodes
    - Names imported at function scope (lazy imports)
    - Cross-module import mappings at module level and function level
    """

    def __init__(self, module_name: str) -> None:
        self.module_name = module_name
        # function_name -> set of called/imported names (local scope)
        self.call_graph: dict[str, set[str]] = {}
        # local_name -> fully-qualified imported name
        self.import_map: dict[str, str] = {}
        # Track current function context for lazy imports
        self._current_function: str | None = None
        # Track TYPE_CHECKING blocks to exclude
        self._in_type_checking = False

    def visit_If(self, node: ast.If) -> None:
        """Detect ``if TYPE_CHECKING:`` blocks and skip their body."""
        if self._is_type_checking_guard(node.test):
            # Skip the body — these imports don't run at runtime
            # But still visit orelse (the else branch runs at runtime)
            for child in node.orelse:
                self.visit(child)
            return
        self.generic_visit(node)

    def _is_type_checking_guard(self, test: ast.expr) -> bool:
        """Check if an if-test is ``TYPE_CHECKING`` or ``typing.TYPE_CHECKING``."""
        if isinstance(test, ast.Name) and test.id == "TYPE_CHECKING":
            return True
        if (
            isinstance(test, ast.Attribute)
            and isinstance(test.value, ast.Name)
            and test.value.id == "typing"
            and test.attr == "TYPE_CHECKING"
        ):
            return True
        return False

    def visit_Import(self, node: ast.Import) -> None:
        """Handle ``import X`` and ``import X as Y``."""
        for alias in node.names:
            local_name = alias.asname or alias.name
            self.import_map[local_name] = alias.name
            # If inside a function, record as a callable edge
            if self._current_function is not None:
                self.call_graph.setdefault(self._current_function, set()).add(local_name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Handle ``from X import Y`` and relative imports."""
        if self._in_type_checking:
            return
        base_module = node.module or ""
        if node.level > 0:
            # Relative import — resolve against current module's package
            base_module = self._resolve_relative(node.level, base_module)
        if node.names:
            for alias in node.names:
                local_name = alias.asname or alias.name
                fqn = f"{base_module}.{alias.name}" if base_module else alias.name
                self.import_map[local_name] = fqn
                if self._current_function is not None:
                    self.call_graph.setdefault(self._current_function, set()).add(
                        local_name
                    )

    def _resolve_relative(self, level: int, module: str) -> str:
        """Resolve a relative import to an absolute module path."""
        parts = self.module_name.split(".")
        # Go up `level` packages (each level = one parent)
        if level <= len(parts):
            base = ".".join(parts[:-level]) if level > 0 else self.module_name
        else:
            base = ""
        if module:
            return f"{base}.{module}" if base else module
        return base

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Process a function definition: build call edges from its body."""
        fqn = f"{self.module_name}.{node.name}"
        if self._current_function is not None:
            # Nested function — treat as callable from parent
            parent = self._current_function
            self.call_graph.setdefault(parent, set()).add(fqn)

        prev_function = self._current_function
        self._current_function = fqn
        self.call_graph.setdefault(fqn, set())
        self.generic_visit(node)
        self._current_function = prev_function

    def visit_Call(self, node: ast.Call) -> None:
        """Record function calls."""
        if self._current_function is None:
            self.generic_visit(node)
            return
        name = self._resolve_call_name(node.func)
        if name:
            self.call_graph.setdefault(self._current_function, set()).add(name)
        self.generic_visit(node)

    def _resolve_call_name(self, node: ast.expr) -> str | None:
        """Extract the callable name from a Call node's func attribute."""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            # e.g. self.method() or module.function()
            value_name = self._resolve_call_name(node.value)
            if value_name:
                return f"{value_name}.{node.attr}"
            return node.attr
        return None


# ---------------------------------------------------------------------------
# Module resolution
# ---------------------------------------------------------------------------


def _module_to_path(module: str, source_root: Path) -> Path | None:
    """Convert a dotted module path to a filesystem path.

    Tries both ``module/path.py`` and ``module/path/__init__.py``.
    Returns None if neither exists.
    """
    parts = module.split(".")
    # Try as a .py file
    candidate = source_root / Path(*parts).with_suffix(".py")
    if candidate.is_file():
        return candidate
    # Try as a package __init__.py
    candidate = source_root / Path(*parts) / "__init__.py"
    if candidate.is_file():
        return candidate
    return None


def _path_to_module(file_path: Path, source_root: Path) -> str:
    """Convert a filesystem path back to a dotted module name."""
    rel = file_path.relative_to(source_root)
    if rel.name == "__init__.py":
        parts = rel.parent.parts
    else:
        parts = (*rel.parent.parts, rel.stem)
    return ".".join(parts)


# ---------------------------------------------------------------------------
# ReachabilityAnalyzer
# ---------------------------------------------------------------------------


class ReachabilityAnalyzer:
    """AST-based call-chain reachability analyzer.

    Given a wiring manifest declaring entry points and required targets,
    parses Python source files, builds a cross-module call graph, and
    uses BFS to determine which targets are statically reachable.

    Args:
        manifest_path: Path to the wiring manifest YAML file.
    """

    def __init__(self, manifest_path: Path) -> None:
        self.manifest_path = manifest_path
        self.entry_points, self.targets = load_manifest(manifest_path)
        # Accumulated cross-module call graph: fqn -> set of called fqns
        self._global_graph: dict[str, set[str]] = {}
        # Accumulated import maps: module_name -> {local_name: fqn}
        self._import_maps: dict[str, dict[str, str]] = {}
        # Modules already parsed (avoid re-parsing)
        self._parsed_modules: set[str] = set()
        self._modules_failed: list[str] = []

    def analyze(self, source_root: Path) -> ReachabilityReport:
        """Run reachability analysis from source_root.

        Args:
            source_root: Root directory containing Python source packages.
                Module paths from the manifest are resolved relative to this.

        Returns:
            ReachabilityReport with per-target results and gap list.
        """
        # Phase 1: Parse entry point modules and follow imports
        for ep in self.entry_points:
            self._parse_module_recursive(ep.module, source_root)

        # Phase 2: Resolve local names in call graph to FQNs
        resolved_graph = self._resolve_graph()

        # Phase 3: BFS for each target
        report = ReachabilityReport(
            modules_parsed=len(self._parsed_modules),
            modules_failed=list(self._modules_failed),
        )

        for target in self.targets:
            # Find the entry point's FQN
            ep_fqn = self._find_entry_fqn(target.from_entry)
            if ep_fqn is None:
                result = ReachabilityResult(
                    target=target.target,
                    from_entry=target.from_entry,
                    spec_ref=target.spec_ref,
                    reachable=False,
                )
                report.results.append(result)
                report.gaps.append(result)
                continue

            reachable, chain = self._bfs_reachable(
                resolved_graph, ep_fqn, target.target
            )
            result = ReachabilityResult(
                target=target.target,
                from_entry=target.from_entry,
                spec_ref=target.spec_ref,
                reachable=reachable,
                chain=chain,
            )
            report.results.append(result)
            if not reachable:
                report.gaps.append(result)

        report.passed = len(report.gaps) == 0
        return report

    # ------------------------------------------------------------------
    # Internal: recursive module parsing
    # ------------------------------------------------------------------

    def _parse_module_recursive(
        self, module_name: str, source_root: Path, depth: int = 0
    ) -> None:
        """Parse a module and recursively follow its imports."""
        if module_name in self._parsed_modules:
            return
        if depth > 50:
            logger.warning("Import depth limit reached for %s", module_name)
            return

        self._parsed_modules.add(module_name)
        file_path = _module_to_path(module_name, source_root)
        if file_path is None:
            logger.debug("Module not found on disk: %s", module_name)
            return

        try:
            source = file_path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError) as exc:
            logger.warning("Failed to parse %s: %s", file_path, exc)
            self._modules_failed.append(module_name)
            return

        visitor = _CallGraphVisitor(module_name)
        visitor.visit(tree)

        # Merge into global graph
        for func, callees in visitor.call_graph.items():
            self._global_graph.setdefault(func, set()).update(callees)

        # Store import map for later resolution
        self._import_maps[module_name] = visitor.import_map

        # Recurse into imported modules (both module-level and function-scope)
        for fqn in visitor.import_map.values():
            # Extract the top-level module from FQN
            imported_module = self._extract_module(fqn, source_root)
            if imported_module and imported_module not in self._parsed_modules:
                self._parse_module_recursive(imported_module, source_root, depth + 1)

    def _extract_module(self, fqn: str, source_root: Path) -> str | None:
        """Try progressively shorter prefixes of a FQN to find a module on disk."""
        parts = fqn.split(".")
        # Try longest prefix first (e.g. a.b.c -> a.b.c, a.b, a)
        for i in range(len(parts), 0, -1):
            candidate = ".".join(parts[:i])
            if _module_to_path(candidate, source_root) is not None:
                return candidate
        return None

    # ------------------------------------------------------------------
    # Internal: resolve local names to FQNs
    # ------------------------------------------------------------------

    def _resolve_graph(self) -> dict[str, set[str]]:
        """Resolve local call names to fully-qualified names using import maps.

        For each function in the global graph, resolves its callees:
        - If a callee is already an FQN in the graph, keep it
        - If a callee matches an import map entry, resolve to FQN
        - If a callee contains a dot (e.g. ``self.method``), attempt
          attribute-based resolution
        """
        resolved: dict[str, set[str]] = {}

        for func, callees in self._global_graph.items():
            # Determine which module this function belongs to
            func_module = self._func_to_module(func)
            import_map = self._import_maps.get(func_module, {})

            resolved_callees: set[str] = set()
            for callee in callees:
                resolved_name = self._resolve_name(callee, func_module, import_map)
                resolved_callees.add(resolved_name)

            resolved[func] = resolved_callees

        return resolved

    def _func_to_module(self, fqn: str) -> str:
        """Extract module name from a function FQN.

        E.g. ``a.b.c.func`` -> tries ``a.b.c``, ``a.b``, ``a`` against
        parsed modules.
        """
        parts = fqn.split(".")
        for i in range(len(parts) - 1, 0, -1):
            candidate = ".".join(parts[:i])
            if candidate in self._parsed_modules:
                return candidate
        return parts[0] if parts else ""

    def _resolve_name(
        self, name: str, func_module: str, import_map: dict[str, str]
    ) -> str:
        """Resolve a local name to its best FQN guess."""
        # Direct match in import map
        if name in import_map:
            return import_map[name]

        # Dotted name — try resolving the prefix
        if "." in name:
            prefix, _, rest = name.partition(".")
            if prefix in import_map:
                return f"{import_map[prefix]}.{rest}"
            # Could be module.func — check if prefix is a known module
            if prefix in self._parsed_modules:
                return f"{prefix}.{rest}"
            # self.X or cls.X — resolve as method within same module
            if prefix in ("self", "cls"):
                return f"{func_module}.{rest}"

        # Check if it's a function defined in the same module
        candidate = f"{func_module}.{name}"
        if candidate in self._global_graph:
            return candidate

        # Return as-is (unresolved)
        return name

    def _find_entry_fqn(self, function_name: str) -> str | None:
        """Find the FQN for an entry point function name."""
        for ep in self.entry_points:
            if ep.function == function_name:
                fqn = f"{ep.module}.{ep.function}"
                if fqn in self._global_graph:
                    return fqn
                # Try without the function being directly in graph
                # (might be defined but we missed it)
                return fqn
        return None

    # ------------------------------------------------------------------
    # Internal: BFS reachability
    # ------------------------------------------------------------------

    def _bfs_reachable(
        self,
        graph: dict[str, set[str]],
        start: str,
        target: str,
    ) -> tuple[bool, list[str]]:
        """BFS from ``start`` to ``target`` in the resolved call graph.

        Returns:
            Tuple of (is_reachable, call_chain).
            call_chain is the path from start to target (inclusive), or
            empty if unreachable.
        """
        if start == target:
            return True, [start]

        visited: set[str] = set()
        # Queue entries: (current_node, path_so_far)
        queue: deque[tuple[str, list[str]]] = deque()
        queue.append((start, [start]))
        visited.add(start)

        while queue:
            current, path = queue.popleft()

            for neighbor in graph.get(current, set()):
                if neighbor in visited:
                    continue

                new_path = [*path, neighbor]

                # Exact match
                if neighbor == target:
                    return True, new_path

                # Suffix match: target "a.b.c.func" matches neighbor
                # "a.b.c.func" or neighbor ends with the target's
                # function portion
                if self._is_target_match(neighbor, target):
                    return True, new_path

                visited.add(neighbor)
                queue.append((neighbor, new_path))

        return False, []

    @staticmethod
    def _is_target_match(candidate: str, target: str) -> bool:
        """Check if candidate matches the target, allowing suffix matching.

        Handles cases where the resolved name might differ slightly
        from the manifest target (e.g. different import resolution paths).
        """
        if candidate == target:
            return True
        # Extract function name from target (last component)
        target_func = target.rsplit(".", 1)[-1]
        candidate_func = candidate.rsplit(".", 1)[-1]
        if target_func != candidate_func:
            return False
        # Same function name — check if the module paths overlap
        # (handles aliased module paths)
        return candidate.endswith(target) or target.endswith(candidate)
