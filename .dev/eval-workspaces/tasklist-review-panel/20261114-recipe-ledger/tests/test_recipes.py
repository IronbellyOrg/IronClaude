"""REQ-06, REQ-09, REQ-25, DR-1: the eight recipes in recipes/recipes.json (DESIGN 4.1, 4.2)."""

import json

import pytest
from helpers import SW

from rl import extract_mr, recipes
from scaffold import cards

RECIPES_DIR = SW / "recipes"
DATA = json.loads((RECIPES_DIR / "recipes.json").read_text(encoding="utf-8"))
# C2, C5, C6 and C8 carry the owner-approved rewording of 2026-11-15 (recipes.json "override"); C4 changed without a word-count change
WORDS = {"C1": 71, "C2": 90, "C3": 56, "C4": 99, "C5": 87, "C6": 95, "C7": 50, "C8": 79}
BUDGETS = {"C2": 6, "C1": 4, "C3": 4, "C4": 4, "C5": 4, "C6": 4, "C7": 4, "C8": 4}
# the design documents and the session logs of the planning and build runs quote the wording on purpose
QUOTING = {"DESIGN.md", "TESTING.md", "IMPLEMENTATION.md", "recipes/recipes.json"}
# runs/ holds the rendered briefs of generated run folders (written by bin/run-panel.sh, never committed)
QUOTING_DIRS = {"design-report", "workflow-report", "implement-report", "runs"}


def test_file_shape():
    assert DATA["schema"] == "rl-recipes/1" and DATA["version"] == 1
    assert all(set(r) == {"version", "text"} for r in DATA["recipes"].values())


def test_recipe_keys_equal_card_ids():
    assert set(DATA["recipes"]) == set(cards.load()) == set(WORDS)
    assert recipes.validate(DATA) == []
    assert set(recipes.load()) == set(WORDS)


def test_each_recipe_at_most_120_words():
    counts = {k: len(v["text"].split()) for k, v in DATA["recipes"].items()}
    assert counts == WORDS
    assert all(n <= 120 for n in counts.values())


def test_budget_sentence_once_and_parsed():
    for rid, entry in DATA["recipes"].items():
        text = entry["text"]
        assert text.count("Write at most") == 1
        assert text.endswith(f"Write at most {BUDGETS[rid]} rows.")
        n = recipes.row_budget(rid)
        assert n == BUDGETS[rid] and 1 <= n <= 14


@pytest.mark.parametrize(
    "text",
    [
        "Do it.",
        "Do it. Write at most 4 rows. Write at most 4 rows.",
        "Write at most 4 rows. Then stop.",
        "Do it. Write at most 0 rows.",
        "Do it. Write at most 15 rows.",
        "Do it. Write at most 4 rows.".replace("Do it.", " ".join(["w"] * 120)),
        "You will see it. Write at most 4 rows.",
        "It should find it. Write at most 4 rows.",
        "The expected result. Write at most 4 rows.",
        "Read src/superclaude/x. Write at most 4 rows.",
    ],
)
def test_validate_refuses_a_broken_recipe(text):
    data = {"schema": "rl-recipes/1", "recipes": {"C1": {"version": 1, "text": text}}}
    assert recipes.validate(data, ["C1"]) != []


def test_validate_refuses_key_set_mismatch():
    ok = {"version": 1, "text": "Do it. Write at most 4 rows."}
    assert (
        recipes.validate({"schema": "rl-recipes/1", "recipes": {"C1": ok}}, ["C1"])
        == []
    )
    assert recipes.validate(
        {"schema": "rl-recipes/1", "recipes": {"C1": ok}}, ["C1", "C2"]
    )
    assert recipes.validate(
        {"schema": "rl-recipes/1", "recipes": {"C1": ok, "C9": ok}}, ["C1"]
    )
    assert recipes.validate({"schema": "other", "recipes": {"C1": ok}}, ["C1"])


def test_recipes_equal_mr_quotes():
    if "override" in DATA:
        pytest.skip(
            "an override entry is recorded: a wording change after the freeze (DESIGN 4.1)"
        )
    quotes = extract_mr.quotes(extract_mr.MR.read_text(encoding="utf-8"))
    assert {k: v["text"] for k, v in DATA["recipes"].items()} == {
        k: quotes[k] for k in WORDS
    }
    block = (RECIPES_DIR / "rl-block.txt").read_text(encoding="utf-8")
    assert block.count("{{LENS_ROW_CAP}}") == 1 and block == quotes["rl_block"]
    assert block.replace("{{LENS_ROW_CAP}}", "14").count("14 rows") == 1
    assert (RECIPES_DIR / "search-form.txt").read_text(encoding="utf-8") == quotes[
        "search_form"
    ]
    assert extract_mr.diff(extract_mr.MR.read_text(encoding="utf-8")) == []


def test_no_src_path_in_recipe_files():
    files = [p for p in RECIPES_DIR.rglob("*") if p.is_file()]
    assert {p.name for p in files} >= {
        "recipes.json",
        "rl-block.txt",
        "search-form.txt",
    }
    assert not [
        p.name for p in files if "src/superclaude/" in p.read_text(encoding="utf-8")
    ]


def test_recipe_text_only_in_one_file():
    heads = {
        rid: " ".join(e["text"].split()[:10]) for rid, e in DATA["recipes"].items()
    }
    assert all(len(h.split()) == 10 for h in heads.values())
    holders = []
    for p in sorted(SW.rglob("*")):
        rel = p.relative_to(SW)
        if (
            not p.is_file()
            or "__pycache__" in p.parts
            or rel.parts[0] in QUOTING_DIRS
            or rel.as_posix() in QUOTING
        ):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        holders.extend((str(rel), rid) for rid, h in heads.items() if h in text)
    assert holders == []
