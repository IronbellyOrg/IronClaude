"""JSON-schema definitions for cliEval artefacts.

This package hosts the canonical machine-readable contracts emitted by
the eval pipeline. Today it carries:

* ``summary.schema.json`` (Roadmap DM-012 / Deliverable D-0053, Task
  T03.10) — the contract every ``superclaude eval run`` summary file
  must match. ``RunSummary.to_dict()`` (T03.09) is the canonical
  producer; FR-RPT1 (T03.11) is the canonical writer; TEST-007 (T04.17)
  is the canonical fidelity test.

Schemas live next to their loader / writer modules so that the source
tree mirrors the runtime contract. Files are loaded via
``importlib.resources`` to keep them importable from installed wheels
without filesystem-relative path tricks.
"""

from __future__ import annotations

import json
from importlib import resources
from typing import Any, Mapping

__all__ = ["SUMMARY_SCHEMA_FILENAME", "load_summary_schema"]


SUMMARY_SCHEMA_FILENAME = "summary.schema.json"


def load_summary_schema() -> Mapping[str, Any]:
    """Return the parsed DM-012 ``summary.schema.json`` document.

    Uses :mod:`importlib.resources` so the schema is discoverable from
    both editable installs and built wheels. Returns a freshly decoded
    mapping on every call — callers are free to mutate it without
    affecting the on-disk file.
    """

    schema_text = (
        resources.files(__name__)
        .joinpath(SUMMARY_SCHEMA_FILENAME)
        .read_text(encoding="utf-8")
    )
    return json.loads(schema_text)
