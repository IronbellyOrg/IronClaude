"""Lens table and lens render (DESIGN 5, R1, DR-3, DR-4, DR-7).

config/lenses.json says which recipes each reviewer of each panel gets. It is data: a new panel, model or class
placement is an edit of that file, with no change here. `validate` returns the breaks of the six rules of 5.2 as
"rule N: ..." strings; `load` raises LensInvalid (message starts with E_LENS_INVALID) when there is any.

`render` returns {role: {...}} in table order. `recipes` is the list of recipe ids (C2 left out when there is no
source); a recipe prints as `R-C<n>. <text>` (`printed`). `assigned_ids` are the row ids the row check accepts (DR-5).
"""

from __future__ import annotations

import json
import math
import re
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from rl import recipes as recipes_mod
from scaffold import cards as cards_mod

RL = Path(__file__).resolve().parents[1]
LENSES_JSON = RL / "config" / "lenses.json"
VALUES_JSON = RL / "config" / "values.json"
COMMON_SH = RL / "bin" / "common.sh"
SCHEMA = "rl-lenses/1"
E_LENS_INVALID = "E_LENS_INVALID"
LENS_MIN, LENS_MAX = 2, 4
ROLE_KEYS = {"rid", "model", "lens", "table_cap", "search_form", "reask"}
# REQ-25: the classes that two reviewers of one panel both hold (MR 3.2(a))
REQ25_DUPLICATES = {"primary": {"C2", "C4"}, "haiku": {"C1"}, "sonnet": {"C1", "C7"}}
REASK_PANEL = "primary"
NO_SOURCE_CLASS = "C2"


class LensInvalid(ValueError):
    """The lens table breaks a rule of DESIGN 5.2 (configuration error; the launcher falls back to Z0)."""


@lru_cache(maxsize=None)
def allowed_models() -> tuple[str, ...]:
    """The reviewer allowlist K2, read from the one place that holds it: ALLOWED_MODELS in bin/common.sh."""
    m = re.search(r'^ALLOWED_MODELS="([^"]*)"', COMMON_SH.read_text(), re.M)
    return tuple(m.group(1).split()) if m else ()


@lru_cache(maxsize=None)
def _values(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def values(path: Path | str | None = None) -> dict:
    """The planning values of config/values.json (b, c, row cap constants, overhead, re-ask constants)."""
    return _values(str(path or VALUES_JSON))


def lens_row_cap(
    b: float, c: float, table_cap: int, share=None, fixed=None, hard_cap=None
) -> int:
    """DR-4: min(table_cap, floor((share * b - fixed) / c)), never below 0 and never above the hard cap.

    b: smallest same-block Z0 median of the panel (s); c: seconds per ledger row of the reviewer's model. The
    division is exact (Fractions of the decimal text), so 14.0 or 12.0 at a table value never becomes 13.999.
    """
    k = values()["row_cap"]
    share = k["share"] if share is None else share
    fixed = k["fixed_s"] if fixed is None else fixed
    hard_cap = k["hard_cap"] if hard_cap is None else hard_cap
    if c <= 0:
        raise ValueError(f"cost per row must be positive, got {c}")
    exact = (Fraction(str(share)) * Fraction(str(b)) - Fraction(str(fixed))) / Fraction(
        str(c)
    )
    return max(0, min(table_cap, hard_cap, math.floor(exact)))


def assigned_ids(recipe_ids, recipes: dict | None = None) -> list[str]:
    """`C<n>.1 ... C<n>.<N>` for every recipe in order, N the recipe's row budget (DR-5)."""
    recipes = recipes or recipes_mod.load()
    return [
        f"{rid}.{k}"
        for rid in recipe_ids
        for k in range(1, recipes_mod.row_budget(rid, recipes) + 1)
    ]


def printed(recipe_id: str, recipes: dict | None = None) -> str:
    """How a recipe appears in a brief (DESIGN 4.1): `R-C<n>. <text>`."""
    return f"R-{recipe_id}. {(recipes or recipes_mod.load())[recipe_id]['text']}"


def validate(
    table: dict, card_ids=None, recipes=None, models=None, duplicates=None
) -> list[str]:
    """Every break of the six rules of DESIGN 5.2, as "rule N: ..." strings; [] means the table is sound.

    card_ids defaults to the ids in cards/, recipes to the ids in recipes.json, models to the K2 allowlist and
    duplicates to REQ25_DUPLICATES.
    """
    ids = set(cards_mod.load() if card_ids is None else card_ids)
    have = set(recipes_mod.load() if recipes is None else recipes)
    models = allowed_models() if models is None else models
    duplicates = REQ25_DUPLICATES if duplicates is None else duplicates
    cap = values()["row_cap"]["hard_cap"]
    errs: list[str] = []
    panels = table.get("panels") if isinstance(table, dict) else None
    if not isinstance(panels, dict) or not panels or table.get("schema") != SCHEMA:
        return [f"rule 0: schema is not {SCHEMA} or there are no panels"]
    for name, panel in panels.items():
        roles = panel.get("roles") if isinstance(panel, dict) else None
        if not isinstance(roles, dict) or not roles:
            errs.append(f"rule 0: panel {name} has no roles")
            continue
        bad = [
            r
            for r, v in roles.items()
            if not isinstance(v, dict) or set(v) != ROLE_KEYS
        ]
        if bad:
            errs.append(
                f"rule 0: panel {name} roles {bad} do not have exactly {sorted(ROLE_KEYS)}"
            )
            continue
        lenses = {r: v["lens"] for r, v in roles.items()}
        held = [c for lens in lenses.values() for c in lens]
        for c in sorted(ids - set(held)):
            errs.append(f"rule 1: panel {name}: class {c} is in no lens")
        for r, lens in lenses.items():
            where = f"panel {name} role {r}"
            if not LENS_MIN <= len(lens) <= LENS_MAX or len(set(lens)) != len(lens):
                errs.append(
                    f"rule 2: {where}: lens {lens} needs {LENS_MIN} to {LENS_MAX} different recipes"
                )
            errs.extend(
                f"rule 2: {where}: recipe {c} does not exist"
                for c in lens
                if c not in have
            )
            tc = roles[r]["table_cap"]
            if (
                not isinstance(tc, int)
                or isinstance(tc, bool)
                or not len(lens) <= tc <= cap
            ):
                errs.append(
                    f"rule 3: {where}: table_cap {tc!r} outside {len(lens)} to {cap}"
                )
            if roles[r]["model"] not in models:
                errs.append(
                    f"rule 4: {where}: model {roles[r]['model']!r} is not an allowed reviewer model"
                )
            kept = [c for c in lens if c != NO_SOURCE_CLASS]
            if len(kept) < LENS_MIN:
                errs.append(
                    f"rule 6: {where}: lens {lens} keeps {len(kept)} recipes without {NO_SOURCE_CLASS}"
                )
        rids = [v["rid"] for v in roles.values()]
        if len(set(rids)) != len(rids):
            errs.append(f"rule 4: panel {name}: rid repeats in {rids}")
        if sum(v["search_form"] is True for v in roles.values()) != 1:
            errs.append(
                f"rule 4: panel {name}: exactly one role needs search_form true"
            )
        asks = sum(v["reask"] is True for v in roles.values())
        if asks != (1 if name == REASK_PANEL else 0):
            errs.append(f"rule 4: panel {name}: {asks} roles have reask true")
        twice = {c for c in held if held.count(c) > 1}
        if name in duplicates and twice != set(duplicates[name]):
            errs.append(
                f"rule 5: panel {name}: duplicated classes {sorted(twice)} differ from {sorted(duplicates[name])}"
            )
    errs.extend(
        f"rule 5: panel {p} is not in the REQ-25 list"
        for p in sorted(set(duplicates) - set(panels))
    )
    return errs


def load(path: Path | str | None = None, **kw) -> dict:
    """The parsed lens table; raises LensInvalid (E_LENS_INVALID) when `validate` finds anything."""
    try:
        table = json.loads(Path(path or LENSES_JSON).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise LensInvalid(f"{E_LENS_INVALID}: cannot read the lens table: {e}") from e
    errs = validate(table, **kw)
    if errs:
        raise LensInvalid(f"{E_LENS_INVALID}: " + "; ".join(errs))
    return table


def render(
    panel: str,
    has_source: bool,
    b_min: float,
    c_by_model: dict,
    table: dict | None = None,
    recipes: dict | None = None,
) -> dict[str, dict]:
    """The lens of every role of one panel (DESIGN 5.3): {role: {rid, model, recipes, budgets, assigned_ids,
    row_cap, search_form, reask, no_budget}}.

    row_cap = min(lens_row_cap(b_min, c_model, table_cap), sum of the budgets); no_budget when it is below the
    number of recipes (one row per recipe is the least that makes a ledger mean anything).
    """
    table = load() if table is None else table
    recipes = recipes_mod.load() if recipes is None else recipes
    out = {}
    for role, spec in table["panels"][panel]["roles"].items():
        ids = [c for c in spec["lens"] if has_source or c != NO_SOURCE_CLASS]
        budgets = {c: recipes_mod.row_budget(c, recipes) for c in ids}
        cap = min(
            lens_row_cap(b_min, c_by_model[spec["model"]], spec["table_cap"]),
            sum(budgets.values()),
        )
        out[role] = {
            "rid": spec["rid"],
            "model": spec["model"],
            "recipes": ids,
            "budgets": budgets,
            "assigned_ids": assigned_ids(ids, recipes),
            "row_cap": cap,
            "search_form": spec["search_form"],
            "reask": spec["reask"],
            "no_budget": cap < len(ids),
        }
    return out
