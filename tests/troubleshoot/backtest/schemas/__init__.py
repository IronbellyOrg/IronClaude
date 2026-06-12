"""JSON-schema definitions for the sc:troubleshoot differential backtest harness.

Hosts ``catch_rate.schema.json`` -- the draft-2020-12 contract every ``catch-rate.json`` artifact
must match. ``CatchRateReport.to_dict()`` is the canonical producer; ``write_catch_rate_report`` is
the writer; ``test_catch_rate_schema.py`` is the fidelity test. The schema is loaded via
``importlib.resources`` so it is discoverable from both editable installs and built wheels without
filesystem-relative path tricks (mirrors ``src/superclaude/cli/eval/schemas/__init__.py``).
"""

from __future__ import annotations

import json
from importlib import resources
from typing import Any, Mapping

__all__ = ["CATCH_RATE_SCHEMA_FILENAME", "load_catch_rate_schema"]


CATCH_RATE_SCHEMA_FILENAME = "catch_rate.schema.json"


def load_catch_rate_schema() -> Mapping[str, Any]:
    """Return the parsed ``catch_rate.schema.json`` document.

    Uses :mod:`importlib.resources` so the schema is discoverable from both editable installs and
    built wheels. Returns a freshly decoded mapping on every call -- callers may mutate it freely.
    """
    schema_text = (
        resources.files(__name__)
        .joinpath(CATCH_RATE_SCHEMA_FILENAME)
        .read_text(encoding="utf-8")
    )
    return json.loads(schema_text)
