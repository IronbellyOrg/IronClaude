"""The RL brief (DESIGN 6.1 to 6.3, DR-2, DR-3, DR-7) and the run.json fields of the lens step (DESIGN 2.2).

The RL brief is the copied renderer's Z0 text (`scaffold.briefs.render("Z0", ...)`, never rebuilt here), then the
copied ledger rule, the RL block with `{{LENS_ROW_CAP}}` filled, the heading, the reviewer's recipes (one paragraph
each, `R-C<n>. <text>`, in lens order) and, for the search role only, the search-form line. Parts are joined with the
copied module's SEPARATOR. On `fallback` the brief is the Z0 text and nothing else. No clock, no randomness (2.4).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from rl import lens as lens_mod
from rl import recipes as recipes_mod
from scaffold import briefs as briefs_mod

PLACEHOLDER = "{{LENS_ROW_CAP}}"
RECIPES_HEADING = "## RECIPES ASSIGNED TO YOU"
RL_BLOCK_FILE = "rl-block.txt"
SEARCH_FORM_FILE = "search-form.txt"


def _text(directory: Path | str | None, name: str) -> str:
    return (
        (Path(directory or recipes_mod.RECIPES_DIR) / name)
        .read_text(encoding="utf-8")
        .rstrip("\n")
    )


def rl_block(row_cap: int, directory: Path | str | None = None) -> str:
    """The RL block with the row cap in place of the placeholder (at 14 it is the MR 3.2(a) quote, DR-3)."""
    return _text(directory, RL_BLOCK_FILE).replace(PLACEHOLDER, str(row_cap))


def brief(
    role: dict,
    doc: dict,
    source: str | None,
    *,
    fallback: bool = False,
    recipes: dict | None = None,
    recipes_dir: Path | str | None = None,
    briefs_dir: Path | str | None = None,
) -> dict:
    """One reviewer's RL brief. `role` is one entry of `lens.render` (`recipes`, `row_cap`, `search_form`).

    doc and source are as for `scaffold.briefs.render`. Returns {"text", "sha256", "z0_sha256", "parts", "recipes",
    "no_source", "fallback"}; `parts` names the parts in order and `recipes` the recipe ids printed.
    """
    z0 = briefs_mod.render("Z0", doc, None, source, directory=briefs_dir)
    ids: list[str] = [] if fallback else list(role["recipes"])
    if fallback:
        parts, texts = z0["parts"], [z0["text"]]
    else:
        recipes = recipes or recipes_mod.load()
        rule = (
            Path(briefs_dir or briefs_mod.BRIEFS_DIR) / briefs_mod.FILES["ledger-rule"]
        )
        parts = [
            *z0["parts"],
            "ledger-rule",
            "rl-block",
            "recipes-heading",
            *(f"R-{c}" for c in ids),
        ]
        texts = [
            z0["text"],
            rule.read_text(encoding="utf-8").rstrip("\n"),
            rl_block(role["row_cap"], recipes_dir),
            RECIPES_HEADING,
            *(lens_mod.printed(c, recipes) for c in ids),
        ]
        if role["search_form"]:
            parts.append("search-form")
            texts.append(_text(recipes_dir, SEARCH_FORM_FILE))
    text = briefs_mod.SEPARATOR.join(texts)
    return {
        "text": text,
        "sha256": briefs_mod.sha256_text(text),
        "z0_sha256": z0["sha256"],
        "parts": parts,
        "recipes": ids,
        "no_source": z0["no_source"],
        "fallback": fallback,
    }


def file_sha256(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_fields(
    roles: dict[str, dict],
    *,
    has_source: bool,
    b: float,
    c_by_model: dict,
    lenses_path: Path | str,
    recipes_path: Path | str | None = None,
    fallback: bool = False,
    fallback_reason: str | None = None,
    briefs: dict[str, dict] | None = None,
) -> dict:
    """The run.json fields the lens step owns (DESIGN 2.2): the flags, the two file hashes and, per reviewer id, the
    lens row cap with the `b` and `c` it came from. `briefs` is {rid: brief()} and adds each brief's sha256. With
    `fallback` the roles need only `rid` and `model`."""
    per = {}
    for r in roles.values():
        per[r["rid"]] = {"model": r["model"]}
        if not fallback:  # a fallback run has no lens: no recipes and no cap
            per[r["rid"]].update(
                recipes=r["recipes"],
                row_cap=r["row_cap"],
                b=b,
                c=c_by_model[r["model"]],
            )
        if briefs:
            per[r["rid"]]["brief_sha256"] = briefs[r["rid"]]["sha256"]
    out = {
        "fallback": fallback,
        "fallback_reason": fallback_reason,
        "no_source": not has_source,
        "c2_not_applicable": not has_source,
        "no_budget": any(r.get("no_budget") for r in roles.values()),
        "lenses_sha256": file_sha256(lenses_path),
        "recipes_sha256": file_sha256(recipes_path or recipes_mod.RECIPES_JSON),
        "reviewers": per,
    }
    if briefs:
        out["z0_sha256"] = next(iter(briefs.values()))["z0_sha256"]
    return out


def dumps(obj) -> str:
    """JSON as every RL file is written: sorted keys, no ASCII escapes, one trailing newline (DESIGN 2.4)."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=1) + "\n"
