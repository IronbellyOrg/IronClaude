"""F-LENS (TESTING section 2): lens tables built in a temporary folder, by code.

`valid_table()` is a copy of config/lenses.json. `invalid_tables()` gives one table per way to break a rule of
DESIGN 5.2, with the rule number it must trip. `build_c9(root)` writes a copy of the cards and of the recipes with a
ninth class (card, recipe, lens placement) and a lens table that places it; nothing in the code changes for it.
"""

import copy
import json
import shutil
from pathlib import Path
from types import SimpleNamespace

RL = Path(__file__).resolve().parents[2]


def valid_table() -> dict:
    return json.loads((RL / "config" / "lenses.json").read_text(encoding="utf-8"))


def _roles(table, panel="primary"):
    return table["panels"][panel]["roles"]


def invalid_tables() -> dict[str, tuple[int, dict]]:
    """{variant name: (rule of DESIGN 5.2 that it breaks, table)}; each differs from the valid table by one edit."""
    v: dict[str, tuple[int, dict]] = {}

    def make(name, rule, edit):
        t = copy.deepcopy(valid_table())
        edit(t)
        v[name] = (rule, t)

    make(
        "class_in_no_lens", 1, lambda t: _roles(t)["S"].update(lens=["C4", "C5", "C6"])
    )
    make(
        "five_recipes",
        2,
        lambda t: _roles(t)["S"].update(lens=["C4", "C5", "C6", "C8", "C1"]),
    )
    make("one_recipe", 2, lambda t: _roles(t)["L1"].update(lens=["C1"]))
    make(
        "repeated_recipe", 2, lambda t: _roles(t)["L1"].update(lens=["C1", "C1", "C3"])
    )
    make(
        "recipe_without_text",
        2,
        lambda t: _roles(t)["L1"].update(lens=["C1", "C3", "C9"]),
    )
    make("table_cap_15", 3, lambda t: _roles(t)["L1"].update(table_cap=15))
    make("table_cap_below_count", 3, lambda t: _roles(t)["S"].update(table_cap=3))
    make("unknown_model", 4, lambda t: _roles(t)["L1"].update(model="claude-opus-5-5"))
    make("two_search_roles", 4, lambda t: _roles(t)["L1"].update(search_form=True))
    make("no_search_role", 4, lambda t: _roles(t)["S"].update(search_form=False))
    make("reask_on_haiku", 4, lambda t: _roles(t, "haiku")["S"].update(reask=True))
    make("no_reask_on_primary", 4, lambda t: _roles(t)["S"].update(reask=False))
    make("repeated_rid", 4, lambda t: _roles(t)["L2"].update(rid="t4-1"))
    make(
        "duplicated_set_differs",
        5,
        lambda t: _roles(t, "haiku")["L2"].update(lens=["C4", "C7", "C3"]),
    )
    make(
        "lens_empties_without_c2",
        6,
        lambda t: _roles(t, "sonnet")["L1"].update(lens=["C2", "C3"]),
    )
    return v


def write_table(path: Path, table: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(table, indent=1, sort_keys=True) + "\n", encoding="utf-8"
    )
    return path


def build_c9(root: Path) -> SimpleNamespace:
    """Cards, recipes and a lens table that hold a class C9, under root. C9 is appended to the L1 lens of every panel."""
    cards = root / "cards"
    shutil.copytree(RL / "cards", cards)
    card = json.loads((cards / "C8.json").read_text(encoding="utf-8"))
    card.update(id="C9", name="Invented ninth class")
    (cards / "C9.json").write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")
    data = json.loads((RL / "recipes" / "recipes.json").read_text(encoding="utf-8"))
    data["recipes"]["C9"] = {
        "version": 1,
        "text": "Compare the two named lists item by item and name the first item that differs. Write at most 4 rows.",
    }
    without = copy.deepcopy(data)
    del without["recipes"]["C9"]
    table = valid_table()
    for panel in table["panels"]:
        _roles(table, panel)["L1"]["lens"].append("C9")
    return SimpleNamespace(
        cards_dir=cards,
        recipes_path=write_table(root / "recipes.json", data),
        recipes_missing_path=write_table(root / "recipes-no-c9.json", without),
        lenses_path=write_table(root / "lenses.json", table),
        table=table,
    )
