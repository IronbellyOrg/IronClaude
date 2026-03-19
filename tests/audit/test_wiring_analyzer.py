"""Tests for ast_analyze_file() utility and AST plugin in wiring_analyzer.py.

Validates AST-based file analysis for ToolOrchestrator integration,
including import extraction, export detection, reference collection,
SyntaxError handling (R2), plugin registration (T07.01), references
population (SC-013), and dual evidence rule (T07.02).
"""

from __future__ import annotations

import textwrap

from superclaude.cli.audit.tool_orchestrator import FileAnalysis, ToolOrchestrator
from superclaude.cli.audit.wiring_analyzer import ast_analyze_file, ast_references_plugin


class TestAstAnalyzeFileValid:
    def test_extracts_imports(self):
        code = textwrap.dedent("""
            import os
            from pathlib import Path
            from typing import Optional
        """)
        result = ast_analyze_file("test.py", code)
        assert "import os" in result.imports
        assert "from pathlib import Path" in result.imports
        assert "from typing import Optional" in result.imports

    def test_extracts_exports_with_all(self):
        code = textwrap.dedent("""
            __all__ = ["Foo", "bar"]

            class Foo:
                pass

            def bar():
                pass

            def _private():
                pass
        """)
        result = ast_analyze_file("test.py", code)
        assert result.exports == ["Foo", "bar"]

    def test_extracts_exports_without_all(self):
        code = textwrap.dedent("""
            class Foo:
                pass

            def bar():
                pass

            def _private():
                pass
        """)
        result = ast_analyze_file("test.py", code)
        assert "Foo" in result.exports
        assert "bar" in result.exports
        assert "_private" not in result.exports

    def test_extracts_references(self):
        code = textwrap.dedent("""
            import os

            def main():
                os.path.join("a", "b")
                print("hello")
        """)
        result = ast_analyze_file("test.py", code)
        assert "os.path.join" in result.references
        assert "print" in result.references

    def test_metadata_contains_line_count(self):
        code = "line1\nline2\nline3\n"
        result = ast_analyze_file("test.py", code)
        assert result.metadata["line_count"] == 3
        assert result.metadata["size_bytes"] == len(code)


class TestAstAnalyzeFileSyntaxError:
    def test_syntax_error_returns_empty_analysis(self):
        code = "def broken("
        result = ast_analyze_file("bad.py", code)
        assert result.imports == []
        assert result.exports == []
        assert result.references == []
        assert "parse_error" in result.metadata

    def test_syntax_error_preserves_metadata(self):
        code = "def broken(\n"
        result = ast_analyze_file("bad.py", code)
        assert result.metadata["line_count"] == 1
        assert result.file_path == "bad.py"
        assert result.content_hash != ""


class TestAstAnalyzeFileEdgeCases:
    def test_empty_file(self):
        result = ast_analyze_file("empty.py", "")
        assert result.imports == []
        assert result.exports == []
        assert result.references == []
        assert result.metadata["line_count"] == 0

    def test_content_hash_consistent(self):
        code = "x = 1\n"
        r1 = ast_analyze_file("a.py", code)
        r2 = ast_analyze_file("b.py", code)
        assert r1.content_hash == r2.content_hash


# ---------------------------------------------------------------------------
# Plugin integration tests (T07.01, T07.02, T07.03 / SC-013)
# ---------------------------------------------------------------------------


class TestPluginRegistration:
    """T07.01: Verify AST plugin registers with ToolOrchestrator."""

    def test_plugin_registers_with_orchestrator(self):
        """Plugin registers with ToolOrchestrator and appears in plugins list."""
        orchestrator = ToolOrchestrator()
        assert len(orchestrator.plugins) == 0

        orchestrator.register_plugin(ast_references_plugin)
        assert len(orchestrator.plugins) == 1
        assert orchestrator.plugins[0] is ast_references_plugin

    def test_plugin_callable_through_orchestrator(self):
        """Plugin is invoked during analyze_file and enriches references."""
        orchestrator = ToolOrchestrator()
        orchestrator.register_plugin(ast_references_plugin)

        code = textwrap.dedent("""\
            import os

            def main():
                os.path.join("a", "b")
                print("hello")
        """)
        result = orchestrator.analyze_file("test.py", code)
        assert "os.path.join" in result.references
        assert "print" in result.references

    def test_plugin_does_not_modify_orchestrator_interface(self):
        """Plugin registration does not change analyze_file or analyze_batch signatures."""
        orchestrator = ToolOrchestrator()
        orchestrator.register_plugin(ast_references_plugin)

        # analyze_file still works with (str, str) signature
        result = orchestrator.analyze_file("x.py", "x = 1\n")
        assert isinstance(result, FileAnalysis)

        # analyze_batch still works with dict[str, str] signature
        results = orchestrator.analyze_batch({"a.py": "a = 1\n", "b.py": "b = 2\n"})
        assert len(results) == 2
        assert all(isinstance(r, FileAnalysis) for r in results)


class TestReferencesPopulated:
    """SC-013: Verify FileAnalysis.references populated for files with imports."""

    def test_references_populated_for_file_with_imports(self):
        """FileAnalysis.references is non-empty for files with import statements."""
        code = textwrap.dedent("""\
            from pathlib import Path

            def process():
                p = Path("/tmp")
                p.exists()
        """)
        orchestrator = ToolOrchestrator()
        orchestrator.register_plugin(ast_references_plugin)
        result = orchestrator.analyze_file("processor.py", code)

        assert len(result.references) > 0
        assert "Path" in result.references

    def test_references_empty_for_file_without_calls(self):
        """FileAnalysis.references may be empty for files with no calls."""
        code = "x = 1\ny = 2\n"
        orchestrator = ToolOrchestrator()
        orchestrator.register_plugin(ast_references_plugin)
        result = orchestrator.analyze_file("constants.py", code)
        assert result.references == []

    def test_plugin_handles_syntax_error_gracefully(self):
        """Plugin returns original analysis unchanged on SyntaxError."""
        orchestrator = ToolOrchestrator()
        orchestrator.register_plugin(ast_references_plugin)

        result = orchestrator.analyze_file("bad.py", "def broken(")
        assert isinstance(result, FileAnalysis)
        # Default analyzer still produces a result; plugin just doesn't enrich
        assert result.file_path == "bad.py"


class TestDualEvidenceRule:
    """T07.02: Verify dual evidence rule reduces orphan false positives."""

    def test_dual_evidence_prevents_false_positive(self):
        """Module with references but no imports is NOT flagged as orphan."""
        from pathlib import Path
        from superclaude.cli.audit.wiring_config import WiringConfig
        from superclaude.cli.audit.wiring_gate import analyze_orphan_modules

        fixture_dir = Path(__file__).parent / "fixtures" / "project_with_providers"

        config = WiringConfig(
            provider_dir_names=frozenset({"handlers"}),
            exclude_patterns=["__init__.py"],
        )

        # Without dual evidence: orphan_handler is flagged
        findings_without = analyze_orphan_modules(config, fixture_dir)
        orphan_names_without = [f.symbol_name for f in findings_without]
        assert any("orphan_handler" in s for s in orphan_names_without)

        # With dual evidence: simulate that some file references orphan_handler
        file_references = {
            "some_file.py": ["orphan_handler.handle_orphan", "other_ref"],
        }
        findings_with = analyze_orphan_modules(
            config, fixture_dir, file_references=file_references
        )
        orphan_names_with = [f.symbol_name for f in findings_with]
        # orphan_handler should NOT be flagged because references provide evidence
        assert not any("orphan_handler" in s for s in orphan_names_with)

    def test_dual_evidence_still_flags_true_orphans(self):
        """Module with neither imports nor references IS still flagged."""
        from pathlib import Path
        from superclaude.cli.audit.wiring_config import WiringConfig
        from superclaude.cli.audit.wiring_gate import analyze_orphan_modules

        fixture_dir = Path(__file__).parent / "fixtures" / "project_with_providers"

        config = WiringConfig(
            provider_dir_names=frozenset({"handlers"}),
            exclude_patterns=["__init__.py"],
        )

        # Dual evidence with empty references — orphan_handler still flagged
        file_references = {
            "some_file.py": ["unrelated_module.something"],
        }
        findings = analyze_orphan_modules(
            config, fixture_dir, file_references=file_references
        )
        orphan_names = [f.symbol_name for f in findings]
        assert any("orphan_handler" in s for s in orphan_names)

    def test_fallback_to_import_only_without_plugin(self):
        """When file_references is None, falls back to import-graph-only."""
        from pathlib import Path
        from superclaude.cli.audit.wiring_config import WiringConfig
        from superclaude.cli.audit.wiring_gate import analyze_orphan_modules

        fixture_dir = Path(__file__).parent / "fixtures" / "project_with_providers"

        config = WiringConfig(
            provider_dir_names=frozenset({"handlers"}),
            exclude_patterns=["__init__.py"],
        )

        # No file_references (plugin not loaded) — uses import-graph only
        findings = analyze_orphan_modules(config, fixture_dir, file_references=None)
        assert any("import-graph only" in f.detail for f in findings)

    def test_dual_evidence_note_in_detail(self):
        """When dual evidence is active, finding detail includes evidence note."""
        from pathlib import Path
        from superclaude.cli.audit.wiring_config import WiringConfig
        from superclaude.cli.audit.wiring_gate import analyze_orphan_modules

        fixture_dir = Path(__file__).parent / "fixtures" / "project_with_providers"

        config = WiringConfig(
            provider_dir_names=frozenset({"handlers"}),
            exclude_patterns=["__init__.py"],
        )

        # Dual evidence active but orphan_handler has no references
        file_references = {"other.py": ["unrelated"]}
        findings = analyze_orphan_modules(
            config, fixture_dir, file_references=file_references
        )
        orphan_findings = [f for f in findings if "orphan_handler" in f.symbol_name]
        assert len(orphan_findings) >= 1
        assert "dual evidence" in orphan_findings[0].detail
