"""One-time helper: cut the quoted recipe wording out of MR 3.2(a) and diff it against recipes/.

`quotes(mr_text)` returns {"C1".."C8": text, "rl_block": text with {{LENS_ROW_CAP}}, "search_form": text}.
Run it as `uv run --frozen --project REPO python RL/rl/extract_mr.py [MR]`: it prints a unified diff of
recipes/recipes.json, rl-block.txt and search-form.txt against the quotes and exits 1 when any differs.
It reads MR only, never a ground-truth file.
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

RL = Path(__file__).resolve().parents[1]
REPO = RL.parents[3]
MR = (
    REPO
    / ".dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md"
)
CAP_PLACEHOLDER = "{{LENS_ROW_CAP}}"
_RECIPE = re.compile(r'^> \*\*R-(C[1-8])\.\*\* "(.*)"$')
_BLOCK = re.compile(r'^> "((?:RECIPES AND LEDGER\.|Search forms you may adapt:).*)"$')


def quotes(mr_text: str) -> dict[str, str]:
    """The ten quoted blocks of 3.2(a): eight recipes, the RL block (cap placeholder) and the search-form line."""
    out: dict[str, str] = {}
    for line in mr_text.splitlines():
        m = _RECIPE.match(line)
        if m:
            out[m.group(1)] = m.group(2)
            continue
        m = _BLOCK.match(line)
        if m:
            key = "rl_block" if m.group(1).startswith("RECIPES") else "search_form"
            out[key] = m.group(1)
    block = out["rl_block"]
    assert block.count("more than 14 rows") == 1
    out["rl_block"] = block.replace(
        "more than 14 rows", f"more than {CAP_PLACEHOLDER} rows"
    )
    return out


def stored(rl: Path = RL) -> dict[str, str]:
    """The same ten texts as they are stored under rl/recipes/."""
    data = json.loads((rl / "recipes" / "recipes.json").read_text(encoding="utf-8"))
    out = {k: v["text"] for k, v in data["recipes"].items()}
    out["rl_block"] = (rl / "recipes" / "rl-block.txt").read_text(encoding="utf-8")
    out["search_form"] = (rl / "recipes" / "search-form.txt").read_text(
        encoding="utf-8"
    )
    return out


def diff(mr_text: str, rl: Path = RL) -> list[str]:
    """Unified diff lines of the stored texts against the quotes (empty when they are byte for byte equal)."""
    want, have = quotes(mr_text), stored(rl)
    lines: list[str] = []
    for key in sorted(set(want) | set(have)):
        a, b = want.get(key, ""), have.get(key, "")
        if a != b:
            lines.extend(
                difflib.unified_diff(
                    [a], [b], f"MR {key}", f"recipes {key}", lineterm=""
                )
            )
    return lines


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    mr = Path(args[0]) if args else MR
    lines = diff(mr.read_text(encoding="utf-8"))
    print("\n".join(lines) if lines else "recipes equal the MR 3.2(a) quotes")
    return 1 if lines else 0


if __name__ == "__main__":
    sys.exit(main())
