"""Shared loader for the golden-resolution tests.

The goldens were taken when the packaged default template had the id `default`. That template now
lives on as `@classic` and the default is chosen by `review-default.json`, so the name `default`
is served from the frozen byte copy `fixtures/review-panel.default.frozen.json` and every other
name (such as `live7`) from the packaged templates.
"""

from __future__ import annotations

import json
from pathlib import Path

from superclaude.cli.review import panel as pnl

FROZEN_DEFAULT = Path(__file__).parent / "fixtures" / "review-panel.default.frozen.json"


def golden_panel(name: str) -> dict:
    if name == "default":
        return json.loads(FROZEN_DEFAULT.read_text(encoding="utf-8"))
    return pnl.packaged_panel(name)
