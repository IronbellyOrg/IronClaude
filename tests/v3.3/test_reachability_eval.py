"""Unit tests for the AST call-chain reachability analyzer (FR-4.4).

Tests cover:
- Known-good reachability (positive): directly and transitively called functions
- Known-bad unreachability (negative): dead code paths
- Cross-module import resolution: ``from X import Y`` across module boundaries
- Lazy import detection: imports inside function bodies

All tests use synthetic Python modules written to tmp directories for
deterministic AST analysis. No mocks on analyzer internals.

Task: T01.08 (R-009)
Dependencies: T01.06 (ReachabilityAnalyzer), T01.07 (wiring manifest), T01.02 (audit_trail)
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest
import yaml

from superclaude.cli.audit.reachability import ReachabilityAnalyzer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_module(source_root: Path, module_dotted: str, source: str) -> Path:
    """Write a synthetic Python module to ``source_root``.

    Handles both ``a.b.c`` -> ``a/b/c.py`` and package ``__init__.py`` files.
    Returns the written file path.
    """
    parts = module_dotted.split(".")
    file_path = source_root / Path(*parts).with_suffix(".py")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # Ensure every parent directory has an __init__.py
    for i in range(1, len(parts)):
        init = source_root / Path(*parts[:i]) / "__init__.py"
        if not init.exists():
            init.write_text("")
    file_path.write_text(textwrap.dedent(source))
    return file_path


def _write_manifest(manifest_path: Path, entry_points: list[dict], targets: list[dict]) -> None:
    """Write a minimal wiring manifest YAML."""
    data = {
        "wiring_manifest": {
            "entry_points": entry_points,
            "required_reachable": targets,
        }
    }
    manifest_path.write_text(yaml.dump(data, default_flow_style=False))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def workspace(tmp_path: Path) -> tuple[Path, Path]:
    """Provide a (source_root, manifest_path) pair backed by tmp_path."""
    source_root = tmp_path / "src"
    source_root.mkdir()
    manifest_path = tmp_path / "manifest.yaml"
    return source_root, manifest_path


# ---------------------------------------------------------------------------
# Test: known-good reachability (positive)
# ---------------------------------------------------------------------------


class TestKnownGoodReachability:
    """Analyzer returns REACHABLE for directly and transitively called functions."""

    def test_direct_call_reachable(self, workspace: tuple[Path, Path], audit_trail) -> None:
        """A function directly called from the entry point is reachable."""
        source_root, manifest_path = workspace

        _write_module(source_root, "app.main", """\
            from app.helpers import do_work

            def entry():
                do_work()
        """)
        _write_module(source_root, "app.helpers", """\
            def do_work():
                pass
        """)

        _write_manifest(manifest_path,
            entry_points=[{"module": "app.main", "function": "entry"}],
            targets=[{
                "target": "app.helpers.do_work",
                "from_entry": "entry",
                "spec_ref": "FR-TEST-1",
            }],
        )

        analyzer = ReachabilityAnalyzer(manifest_path)
        report = analyzer.analyze(source_root)

        assert report.passed is True
        assert len(report.gaps) == 0
        assert len(report.results) == 1
        assert report.results[0].reachable is True
        assert len(report.results[0].chain) > 0

        audit_trail.record(
            test_id="test_direct_call_reachable",
            spec_ref="FR-4.4",
            assertion_type="structural",
            inputs={"entry": "app.main.entry", "target": "app.helpers.do_work"},
            observed={"reachable": True, "chain": report.results[0].chain},
            expected={"reachable": True},
            verdict="PASS",
            evidence="Direct call from entry() to do_work() detected by AST analyzer",
        )

    def test_transitive_call_reachable(self, workspace: tuple[Path, Path], audit_trail) -> None:
        """A function called transitively (A -> B -> C) is reachable from A."""
        source_root, manifest_path = workspace

        _write_module(source_root, "pkg.entry", """\
            from pkg.middle import step_one

            def run():
                step_one()
        """)
        _write_module(source_root, "pkg.middle", """\
            from pkg.leaf import final_action

            def step_one():
                final_action()
        """)
        _write_module(source_root, "pkg.leaf", """\
            def final_action():
                pass
        """)

        _write_manifest(manifest_path,
            entry_points=[{"module": "pkg.entry", "function": "run"}],
            targets=[{
                "target": "pkg.leaf.final_action",
                "from_entry": "run",
                "spec_ref": "FR-TEST-2",
            }],
        )

        analyzer = ReachabilityAnalyzer(manifest_path)
        report = analyzer.analyze(source_root)

        assert report.passed is True
        assert len(report.gaps) == 0
        assert report.results[0].reachable is True
        # Chain should have at least 3 nodes: entry -> middle -> leaf
        assert len(report.results[0].chain) >= 3

        audit_trail.record(
            test_id="test_transitive_call_reachable",
            spec_ref="FR-4.4",
            assertion_type="structural",
            inputs={"entry": "pkg.entry.run", "target": "pkg.leaf.final_action"},
            observed={"reachable": True, "chain_length": len(report.results[0].chain)},
            expected={"reachable": True},
            verdict="PASS",
            evidence="Transitive call chain run()->step_one()->final_action() resolved",
        )


# ---------------------------------------------------------------------------
# Test: known-bad unreachability (negative)
# ---------------------------------------------------------------------------


class TestKnownBadUnreachability:
    """Analyzer returns UNREACHABLE for dead code paths."""

    def test_uncalled_function_unreachable(
        self, workspace: tuple[Path, Path], audit_trail
    ) -> None:
        """A function that exists but is never called from the entry point is unreachable."""
        source_root, manifest_path = workspace

        _write_module(source_root, "svc.main", """\
            from svc.used import active_path

            def start():
                active_path()
        """)
        _write_module(source_root, "svc.used", """\
            def active_path():
                pass
        """)
        _write_module(source_root, "svc.dead", """\
            def orphan_function():
                pass
        """)

        _write_manifest(manifest_path,
            entry_points=[{"module": "svc.main", "function": "start"}],
            targets=[{
                "target": "svc.dead.orphan_function",
                "from_entry": "start",
                "spec_ref": "FR-TEST-3",
            }],
        )

        analyzer = ReachabilityAnalyzer(manifest_path)
        report = analyzer.analyze(source_root)

        assert report.passed is False
        assert len(report.gaps) == 1
        assert report.gaps[0].target == "svc.dead.orphan_function"
        assert report.gaps[0].reachable is False
        assert report.gaps[0].chain == []

        audit_trail.record(
            test_id="test_uncalled_function_unreachable",
            spec_ref="FR-4.4",
            assertion_type="structural",
            inputs={"entry": "svc.main.start", "target": "svc.dead.orphan_function"},
            observed={"reachable": False, "gaps": 1},
            expected={"reachable": False},
            verdict="PASS",
            evidence="orphan_function() never imported or called from start(); correctly flagged",
        )

    def test_imported_but_uncalled_unreachable(
        self, workspace: tuple[Path, Path], audit_trail
    ) -> None:
        """A function imported at module level but never called is unreachable.

        Module-level imports are recorded in the import map but do not create
        call-graph edges. Only actual ``ast.Call`` nodes inside function bodies
        create edges.
        """
        source_root, manifest_path = workspace

        _write_module(source_root, "lib.main", """\
            from lib.utils import helper_a, helper_b

            def go():
                helper_a()
                # helper_b is imported but never called
        """)
        _write_module(source_root, "lib.utils", """\
            def helper_a():
                pass

            def helper_b():
                pass
        """)

        _write_manifest(manifest_path,
            entry_points=[{"module": "lib.main", "function": "go"}],
            targets=[{
                "target": "lib.utils.helper_b",
                "from_entry": "go",
                "spec_ref": "FR-TEST-4",
            }],
        )

        analyzer = ReachabilityAnalyzer(manifest_path)
        report = analyzer.analyze(source_root)

        assert report.passed is False
        assert len(report.gaps) == 1
        assert report.gaps[0].target == "lib.utils.helper_b"

        audit_trail.record(
            test_id="test_imported_but_uncalled_unreachable",
            spec_ref="FR-4.4",
            assertion_type="structural",
            inputs={"entry": "lib.main.go", "target": "lib.utils.helper_b"},
            observed={"reachable": False},
            expected={"reachable": False},
            verdict="PASS",
            evidence="helper_b imported but never called; correctly flagged as unreachable",
        )


# ---------------------------------------------------------------------------
# Test: cross-module import resolution
# ---------------------------------------------------------------------------


class TestCrossModuleResolution:
    """Analyzer follows ``from X import Y`` across module boundaries."""

    def test_from_import_resolved(self, workspace: tuple[Path, Path], audit_trail) -> None:
        """``from X import Y`` is resolved to the target module's function."""
        source_root, manifest_path = workspace

        _write_module(source_root, "cross.alpha", """\
            from cross.beta import transform

            def process():
                transform()
        """)
        _write_module(source_root, "cross.beta", """\
            from cross.gamma import finalize

            def transform():
                finalize()
        """)
        _write_module(source_root, "cross.gamma", """\
            def finalize():
                pass
        """)

        _write_manifest(manifest_path,
            entry_points=[{"module": "cross.alpha", "function": "process"}],
            targets=[{
                "target": "cross.gamma.finalize",
                "from_entry": "process",
                "spec_ref": "FR-TEST-5",
            }],
        )

        analyzer = ReachabilityAnalyzer(manifest_path)
        report = analyzer.analyze(source_root)

        assert report.passed is True
        assert report.results[0].reachable is True
        # Verify the analyzer parsed all three modules
        assert report.modules_parsed >= 3

        audit_trail.record(
            test_id="test_from_import_resolved",
            spec_ref="FR-4.4",
            assertion_type="structural",
            inputs={"chain": "alpha -> beta -> gamma"},
            observed={
                "reachable": True,
                "modules_parsed": report.modules_parsed,
                "chain": report.results[0].chain,
            },
            expected={"reachable": True, "modules_parsed_gte": 3},
            verdict="PASS",
            evidence="Cross-module chain alpha->beta->gamma correctly resolved via from-imports",
        )

    def test_relative_import_resolved(self, workspace: tuple[Path, Path], audit_trail) -> None:
        """Relative imports (``from . import X``) are resolved correctly."""
        source_root, manifest_path = workspace

        _write_module(source_root, "rel.sub.entry", """\
            from .worker import do_task

            def main():
                do_task()
        """)
        _write_module(source_root, "rel.sub.worker", """\
            def do_task():
                pass
        """)

        _write_manifest(manifest_path,
            entry_points=[{"module": "rel.sub.entry", "function": "main"}],
            targets=[{
                "target": "rel.sub.worker.do_task",
                "from_entry": "main",
                "spec_ref": "FR-TEST-6",
            }],
        )

        analyzer = ReachabilityAnalyzer(manifest_path)
        report = analyzer.analyze(source_root)

        assert report.passed is True
        assert report.results[0].reachable is True

        audit_trail.record(
            test_id="test_relative_import_resolved",
            spec_ref="FR-4.4",
            assertion_type="structural",
            inputs={"import_style": "relative", "pattern": "from .worker import do_task"},
            observed={"reachable": True, "chain": report.results[0].chain},
            expected={"reachable": True},
            verdict="PASS",
            evidence="Relative import `from .worker import do_task` resolved to rel.sub.worker",
        )

    def test_missing_module_does_not_crash(
        self, workspace: tuple[Path, Path], audit_trail
    ) -> None:
        """Importing a non-existent module is recorded but does not crash the analyzer."""
        source_root, manifest_path = workspace

        _write_module(source_root, "safe.entry", """\
            from safe.missing import ghost
            from safe.real import concrete

            def run():
                concrete()
        """)
        _write_module(source_root, "safe.real", """\
            def concrete():
                pass
        """)
        # Note: safe.missing is NOT created

        _write_manifest(manifest_path,
            entry_points=[{"module": "safe.entry", "function": "run"}],
            targets=[{
                "target": "safe.real.concrete",
                "from_entry": "run",
                "spec_ref": "FR-TEST-7",
            }],
        )

        analyzer = ReachabilityAnalyzer(manifest_path)
        report = analyzer.analyze(source_root)

        assert report.passed is True
        assert report.results[0].reachable is True
        # The analyzer should not have crashed, just logged a warning

        audit_trail.record(
            test_id="test_missing_module_does_not_crash",
            spec_ref="FR-4.4",
            assertion_type="structural",
            inputs={"missing_module": "safe.missing"},
            observed={"reachable": True, "modules_failed": report.modules_failed},
            expected={"no_crash": True, "reachable": True},
            verdict="PASS",
            evidence="Missing module safe.missing did not crash analyzer; real target still found",
        )


# ---------------------------------------------------------------------------
# Test: lazy import detection
# ---------------------------------------------------------------------------


class TestLazyImportDetection:
    """Analyzer detects imports inside function bodies (lazy imports)."""

    def test_function_scope_import_detected(
        self, workspace: tuple[Path, Path], audit_trail
    ) -> None:
        """An import inside a function body creates a reachability edge."""
        source_root, manifest_path = workspace

        _write_module(source_root, "lazy.entry", """\
            def invoke():
                from lazy.deferred import heavy_work
                heavy_work()
        """)
        _write_module(source_root, "lazy.deferred", """\
            def heavy_work():
                pass
        """)

        _write_manifest(manifest_path,
            entry_points=[{"module": "lazy.entry", "function": "invoke"}],
            targets=[{
                "target": "lazy.deferred.heavy_work",
                "from_entry": "invoke",
                "spec_ref": "FR-TEST-8",
            }],
        )

        analyzer = ReachabilityAnalyzer(manifest_path)
        report = analyzer.analyze(source_root)

        assert report.passed is True
        assert report.results[0].reachable is True

        audit_trail.record(
            test_id="test_function_scope_import_detected",
            spec_ref="FR-4.4",
            assertion_type="structural",
            inputs={"pattern": "from lazy.deferred import heavy_work inside invoke()"},
            observed={"reachable": True, "chain": report.results[0].chain},
            expected={"reachable": True},
            verdict="PASS",
            evidence="Lazy import inside invoke() body detected; heavy_work() reachable",
        )

    def test_lazy_import_transitive_chain(
        self, workspace: tuple[Path, Path], audit_trail
    ) -> None:
        """Lazy imports participate in transitive reachability chains."""
        source_root, manifest_path = workspace

        _write_module(source_root, "chain.start", """\
            def begin():
                from chain.mid import bridge
                bridge()
        """)
        _write_module(source_root, "chain.mid", """\
            def bridge():
                from chain.end import finish
                finish()
        """)
        _write_module(source_root, "chain.end", """\
            def finish():
                pass
        """)

        _write_manifest(manifest_path,
            entry_points=[{"module": "chain.start", "function": "begin"}],
            targets=[{
                "target": "chain.end.finish",
                "from_entry": "begin",
                "spec_ref": "FR-TEST-9",
            }],
        )

        analyzer = ReachabilityAnalyzer(manifest_path)
        report = analyzer.analyze(source_root)

        assert report.passed is True
        assert report.results[0].reachable is True
        assert len(report.results[0].chain) >= 3

        audit_trail.record(
            test_id="test_lazy_import_transitive_chain",
            spec_ref="FR-4.4",
            assertion_type="structural",
            inputs={"pattern": "begin -> lazy(bridge) -> lazy(finish)"},
            observed={
                "reachable": True,
                "chain": report.results[0].chain,
                "chain_length": len(report.results[0].chain),
            },
            expected={"reachable": True, "chain_length_gte": 3},
            verdict="PASS",
            evidence="Two-hop lazy import chain begin()->bridge()->finish() fully resolved",
        )

    def test_type_checking_import_excluded(
        self, workspace: tuple[Path, Path], audit_trail
    ) -> None:
        """Imports guarded by ``if TYPE_CHECKING:`` are excluded from the call graph."""
        source_root, manifest_path = workspace

        _write_module(source_root, "tc.main", """\
            from __future__ import annotations
            from typing import TYPE_CHECKING

            if TYPE_CHECKING:
                from tc.types_only import TypeOnlyClass

            def run():
                pass
        """)
        _write_module(source_root, "tc.types_only", """\
            class TypeOnlyClass:
                pass
        """)

        _write_manifest(manifest_path,
            entry_points=[{"module": "tc.main", "function": "run"}],
            targets=[{
                "target": "tc.types_only.TypeOnlyClass",
                "from_entry": "run",
                "spec_ref": "FR-TEST-10",
            }],
        )

        analyzer = ReachabilityAnalyzer(manifest_path)
        report = analyzer.analyze(source_root)

        assert report.passed is False
        assert len(report.gaps) == 1
        assert report.gaps[0].target == "tc.types_only.TypeOnlyClass"

        audit_trail.record(
            test_id="test_type_checking_import_excluded",
            spec_ref="FR-4.4",
            assertion_type="structural",
            inputs={"guard": "if TYPE_CHECKING:", "target": "tc.types_only.TypeOnlyClass"},
            observed={"reachable": False, "gaps": 1},
            expected={"reachable": False},
            verdict="PASS",
            evidence="TYPE_CHECKING-guarded import correctly excluded from call graph",
        )
