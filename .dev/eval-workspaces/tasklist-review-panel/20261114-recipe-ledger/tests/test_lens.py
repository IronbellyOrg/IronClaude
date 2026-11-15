"""REQ-10, REQ-25 (lens part), REQ-26 (cap part), DR-4, DR-7: config/lenses.json, config/values.json and rl/lens.py."""

import json
import time

import pytest
from helpers import SW

from fixtures.lens.make_lens import build_c9, invalid_tables, valid_table, write_table
from rl import lens, recipes
from scaffold import cards

TABLE = json.loads((SW / "config" / "lenses.json").read_text(encoding="utf-8"))
VALUES = json.loads((SW / "config" / "values.json").read_text(encoding="utf-8"))
PANELS = ("primary", "haiku", "sonnet")
B_MIN = {p: min(v.values()) for p, v in VALUES["b"].items()}
# REQ-25, from MR 3.2(a); written out here on purpose so a change of the table or of lens.py cannot move it
REQ25 = {"primary": {"C2", "C4"}, "haiku": {"C1"}, "sonnet": {"C1", "C7"}}
ROLE_KEYS = {"rid", "model", "lens", "table_cap", "search_form", "reask"}
FIELDS = {
    "rid",
    "model",
    "recipes",
    "budgets",
    "assigned_ids",
    "row_cap",
    "search_form",
    "reask",
    "no_budget",
}


def render(panel, has_source=True, **kw):
    return lens.render(panel, has_source, B_MIN[panel], VALUES["c"], **kw)


def test_table_shape_and_rules():
    assert TABLE["schema"] == "rl-lenses/1" and set(TABLE["panels"]) == set(PANELS)
    assert lens.validate(TABLE) == [] and lens.load() == TABLE
    for panel in TABLE["panels"].values():
        assert set(panel["roles"]) == {"S", "L1", "L2"}
        for role in panel["roles"].values():
            assert set(role) == ROLE_KEYS and 2 <= len(role["lens"]) <= 4


def test_every_class_in_every_panel():
    ids = set(cards.load())
    for panel in TABLE["panels"].values():
        assert {c for r in panel["roles"].values() for c in r["lens"]} == ids


def test_values_file_is_all_planning():
    assert VALUES["status"] == "planning" and "planning" in VALUES["note"]
    assert VALUES["c"] == {
        "muse-ember-1.0": 0.4,
        "gpt-6-luna": 2,
        "claude-haiku-5-5": 4,
        "claude-sonnet-5-5": 3,
    }
    assert [sorted(v.values()) for v in VALUES["b"].values()] == [
        [100, 120, 122],
        [220, 226, 238],
        [259, 269, 302],
    ]
    assert VALUES["row_cap"] == {"fixed_s": 6, "share": 0.35, "hard_cap": 14}
    assert VALUES["overhead_s"] == {"primary": 28, "haiku": 30, "sonnet": 30}
    assert VALUES["reask"] == {"fixed_s": 30, "factor": 1.35}


def test_duplicated_classes_equal_req25():
    for panel, want in REQ25.items():
        held = [c for r in render(panel).values() for c in r["recipes"]]
        assert {c for c in held if held.count(c) > 1} == want, panel


def test_search_form_only_in_search_role():
    for panel in PANELS:
        flags = {role: r["search_form"] for role, r in render(panel).items()}
        assert flags == {"S": True, "L1": False, "L2": False}, panel
    asks = {p: [r for r, v in render(p).items() if v["reask"]] for p in PANELS}
    assert asks == {"primary": ["S"], "haiku": [], "sonnet": []}


def test_row_cap_per_panel():
    caps = {p: [r["row_cap"] for r in render(p).values()] for p in PANELS}
    assert caps == {
        "primary": [14, 14, 14],
        "haiku": [6, 14, 12],
        "sonnet": [8, 12, 12],
    }
    assert not any(r["no_budget"] for p in PANELS for r in render(p).values())


@pytest.mark.parametrize(
    ("b", "c", "want"),
    [
        (100, 2.00, 14),
        (100, 2.07, 14),
        (100, 2.41, 12),
        (100, 2.50, 11),
        (100, 3.00, 9),
        (122, 2.00, 14),
        (122, 3.00, 12),
        (60, 2.00, 7),
    ],
)
def test_row_cap_formula_table(b, c, want):
    assert lens.lens_row_cap(b, c, 14) == want


def test_row_cap_formula_edges():
    # the break-even at b = 100 is 29 / 14 = 2.0714...: just below it 14 rows fit, just above only 13
    assert lens.lens_row_cap(100, 2.0714, 14) == 14
    assert lens.lens_row_cap(100, 2.0715, 14) == 13
    assert (
        lens.lens_row_cap(122, 2.0, 99) == 14
    )  # the hard cap holds even for a large table_cap
    assert lens.lens_row_cap(10, 2.0, 14) == 0  # 3.5 - 6 is negative: never below 0
    with pytest.raises(ValueError):
        lens.lens_row_cap(100, 0, 14)


def test_no_budget_refuses():
    slow = dict(
        VALUES["c"], **{"gpt-6-luna": 12.0}
    )  # 29 / 12 = 2 rows for a lens of 3 recipes
    out = lens.render("primary", True, 100, slow)
    assert out["L1"]["row_cap"] == 2 and out["L1"]["no_budget"] is True
    assert out["L2"]["no_budget"] is True and out["S"]["no_budget"] is False
    exactly = dict(
        VALUES["c"], **{"gpt-6-luna": 9.6}
    )  # 29 / 9.6 = 3.02: one row per recipe is enough
    out = lens.render("primary", True, 100, exactly)
    assert out["L1"]["row_cap"] == 3 and out["L1"]["no_budget"] is False


def test_assigned_ids():
    out = render("primary")
    assert out["L1"]["assigned_ids"] == [
        f"{c}.{k}"
        for c, n in (("C1", 4), ("C2", 6), ("C3", 4))
        for k in range(1, n + 1)
    ]
    assert out["L1"]["budgets"] == {"C1": 4, "C2": 6, "C3": 4}
    assert lens.assigned_ids(["C7"]) == ["C7.1", "C7.2", "C7.3", "C7.4"]
    r = recipes.load()
    assert lens.printed("C7", r) == f"R-C7. {r['C7']['text']}"


def test_render_fields_and_models():
    for panel in PANELS:
        out = render(panel)
        for role, r in out.items():
            spec = TABLE["panels"][panel]["roles"][role]
            assert set(r) == FIELDS
            assert (r["rid"], r["model"], r["recipes"]) == (
                spec["rid"],
                spec["model"],
                spec["lens"],
            )
            assert r["row_cap"] <= sum(r["budgets"].values())


def test_every_lens_keeps_two_recipes_without_c2():
    for panel in PANELS:
        for role, r in render(panel, has_source=False).items():
            assert "C2" not in r["recipes"] and len(r["recipes"]) >= 2, (panel, role)
            assert not any(i.startswith("C2.") for i in r["assigned_ids"])
            assert "C2" not in r["budgets"]
    assert render("primary")["L1"]["recipes"] == ["C1", "C2", "C3"]
    assert render("primary", False)["L1"]["recipes"] == ["C1", "C3"]
    assert render("sonnet", False)["S"]["recipes"] == ["C5", "C6", "C8"]


def test_fixture_class_c9_needs_no_code_change(tmp_path):
    f = build_c9(tmp_path)
    ids = cards.load(f.cards_dir)
    assert "C9" in ids
    data = json.loads(f.recipes_path.read_text(encoding="utf-8"))["recipes"]
    assert lens.validate(f.table, card_ids=ids, recipes=data) == []
    out = lens.render("primary", True, 100, VALUES["c"], table=f.table, recipes=data)
    assert out["L1"]["recipes"] == ["C1", "C2", "C3", "C9"]
    assert "C9.1" in out["L1"]["assigned_ids"] and "C9.4" in out["L1"]["assigned_ids"]
    assert lens.printed("C9", data).startswith("R-C9. Compare the two named lists")
    assert out["L1"]["row_cap"] == 14
    # the recipe entry removed: the table is invalid, and so is the recipes file (card without recipe)
    gone = json.loads(f.recipes_missing_path.read_text(encoding="utf-8"))["recipes"]
    assert any(
        "rule 2" in e and "C9" in e
        for e in lens.validate(f.table, card_ids=ids, recipes=gone)
    )
    assert recipes.validate({"schema": "rl-recipes/1", "recipes": gone}, ids)
    # and the placement removed: the card exists but no lens holds it
    plain = valid_table()
    assert any(
        "rule 1" in e and "C9" in e
        for e in lens.validate(plain, card_ids=ids, recipes=data)
    )


def test_load_reads_a_table_file(tmp_path):
    assert lens.load(write_table(tmp_path / "ok.json", valid_table())) == valid_table()
    with pytest.raises(lens.LensInvalid, match="E_LENS_INVALID"):
        lens.load(tmp_path / "missing.json")


@pytest.mark.parametrize("name", sorted(invalid_tables()))
def test_invalid_table_is_refused(name, tmp_path):
    rule, table = invalid_tables()[name]
    errs = lens.validate(table)
    assert any(e.startswith(f"rule {rule}:") for e in errs), (name, errs)
    with pytest.raises(lens.LensInvalid, match="E_LENS_INVALID"):
        lens.load(write_table(tmp_path / f"{name}.json", table))


def test_every_rule_has_a_variant():
    assert {rule for rule, _ in invalid_tables().values()} == {1, 2, 3, 4, 5, 6}
    assert lens.validate(valid_table()) == []


def test_missing_schema_is_refused():
    assert lens.validate({"panels": TABLE["panels"]}) and lens.validate({})


def test_render_under_one_second():
    t0 = time.perf_counter()
    for panel in PANELS:
        render(panel)
        render(panel, has_source=False)
    assert time.perf_counter() - t0 < 1.0
