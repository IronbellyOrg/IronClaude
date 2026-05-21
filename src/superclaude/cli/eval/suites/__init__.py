"""cliEval suite manifest package.

Houses ``suite.schema.json`` (DM-011) and built-in suite manifests. The
schema is the canonical contract for ``suites/*.yaml`` files validated by
:func:`superclaude.cli.eval.loader.validate_manifest` (T01.04).
"""

from __future__ import annotations

from pathlib import Path

SCHEMA_PATH: Path = Path(__file__).resolve().parent / "suite.schema.json"
"""Absolute path to the JSON Schema describing the v1 suite manifest."""

__all__ = ["SCHEMA_PATH"]
