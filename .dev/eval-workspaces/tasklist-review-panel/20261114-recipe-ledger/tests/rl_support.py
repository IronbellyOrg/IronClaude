"""Shared by the render tests: the sandbox paths, the planning values, and small helpers that parse a rendered brief."""

import json
import re

from helpers import SW

from rl import lens, render
from scaffold import briefs

CAND = "/tmp/evalsb-recipe/cand/p1/candidate.md"
SHA = "ab" * 32
SOURCE = "/tmp/evalsb-recipe/cand/p1/source.md"
DOC = {"cand_sb": CAND, "sha": SHA}
SEP = briefs.SEPARATOR
LENSES = SW / "config" / "lenses.json"
TABLE = json.loads(LENSES.read_text(encoding="utf-8"))
VALUES = json.loads((SW / "config" / "values.json").read_text(encoding="utf-8"))
RECIPES_JSON = json.loads(
    (SW / "recipes" / "recipes.json").read_text(encoding="utf-8")
)["recipes"]
PANELS = ("primary", "haiku", "sonnet")
CLASSES = tuple(f"C{n}" for n in range(1, 9))
B_MIN = {p: min(v.values()) for p, v in VALUES["b"].items()}
# REQ-25, from MR 3.2(a); written out here on purpose so a change of the table or of the code cannot move it
REQ25 = {"primary": {"C2", "C4"}, "haiku": {"C1"}, "sonnet": {"C1", "C7"}}
RECIPE_PARAGRAPH = re.compile(r"R-(C\d+)\. ")


def roles(panel, has_source=True):
    return lens.render(panel, has_source, B_MIN[panel], VALUES["c"])


def rl_briefs(panel, source=SOURCE):
    """{role: render.brief(...)} of one panel."""
    return {
        role: render.brief(r, DOC, source)
        for role, r in roles(panel, bool(source)).items()
    }


def z0(source=SOURCE):
    return briefs.render("Z0", DOC, None, source)


def after_heading(text):
    """The paragraphs that follow the recipes heading of an RL brief."""
    _, found, tail = text.partition(SEP + render.RECIPES_HEADING + SEP)
    assert found, "no recipes heading"
    return tail.split(SEP)


def recipe_paragraphs(text):
    """[(class id, paragraph)] of the paragraphs that start with `R-C<n>. `, in brief order."""
    return [
        (m.group(1), p) for p in after_heading(text) if (m := RECIPE_PARAGRAPH.match(p))
    ]
