"""Recipes as data (DESIGN 4.1, REQ-25, DR-1): recipes/recipes.json is the only file that holds recipe text.

The row budget is never stored: `row_budget` reads N out of the last sentence of the text, "Write at most N rows.".
`validate` returns the list of rule breaks (empty when the file is sound); `load` raises ValueError on any.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from scaffold import cards

RECIPES_DIR = Path(__file__).resolve().parents[1] / "recipes"
RECIPES_JSON = RECIPES_DIR / "recipes.json"
SCHEMA = "rl-recipes/1"
MAX_WORDS = 120
BUDGET_MIN, BUDGET_MAX = 1, 14
_BUDGET = re.compile(r"Write at most (\d+) rows\.")
FORBIDDEN_PHRASES = ("expected", "should find", "will find", "you will see")
FORBIDDEN_PATH = "src/superclaude/"


def budget_of(text: str) -> int | None:
    """N of the single closing sentence "Write at most N rows.", or None when it is missing, repeated or not last."""
    found = _BUDGET.findall(text)
    if len(found) != 1 or not text.rstrip().endswith(f"Write at most {found[0]} rows."):
        return None
    return int(found[0])


def validate(data: dict, card_ids=None) -> list[str]:
    """Every rule of DESIGN 4.1 that `data` (a parsed recipes.json) breaks; card_ids defaults to the ids in cards/."""
    ids = set(cards.load() if card_ids is None else card_ids)
    errors: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema is not {SCHEMA}")
    recipes = data.get("recipes", {})
    if set(recipes) != ids:
        errors.append(
            f"recipe ids {sorted(recipes)} differ from card ids {sorted(ids)}"
        )
    for rid, entry in sorted(recipes.items()):
        text = entry.get("text", "") if isinstance(entry, dict) else ""
        low = text.lower()
        if not text:
            errors.append(f"{rid}: no text")
            continue
        if len(text.split()) > MAX_WORDS:
            errors.append(f"{rid}: more than {MAX_WORDS} words")
        n = budget_of(text)
        if n is None:
            errors.append(f"{rid}: no single closing sentence 'Write at most N rows.'")
        elif not BUDGET_MIN <= n <= BUDGET_MAX:
            errors.append(f"{rid}: budget {n} outside {BUDGET_MIN} to {BUDGET_MAX}")
        if FORBIDDEN_PATH in text:
            errors.append(f"{rid}: holds a {FORBIDDEN_PATH} path")
        errors.extend(
            f"{rid}: states an expected outcome ({p!r})"
            for p in FORBIDDEN_PHRASES
            if p in low
        )
    return errors


def load(path: Path | str | None = None, card_ids=None) -> dict[str, dict]:
    """{recipe id: {"version", "text"}} from recipes.json; ValueError when validate finds anything."""
    data = json.loads(Path(path or RECIPES_JSON).read_text(encoding="utf-8"))
    errors = validate(data, card_ids)
    if errors:
        raise ValueError("; ".join(errors))
    return data["recipes"]


def row_budget(recipe_id: str, recipes: dict[str, dict] | None = None) -> int:
    """The row budget N of one recipe, parsed from its text."""
    return budget_of((recipes or load())[recipe_id]["text"])
