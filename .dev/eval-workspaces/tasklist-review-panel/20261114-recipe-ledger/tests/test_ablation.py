"""REQ-35, DR-13: the brief-level leave-one-class-out ablation. With one recipe and its lens placements removed, every
other recipe paragraph, every Z0 part, the ledger rule and every other lens position of every brief is byte for byte
the same. (The row cap in the RL block follows the budgets, so the block is compared with its number masked; the
model-stage ablation needs model runs and is a manual item, DR-13.)"""

import copy

import pytest
from rl_support import B_MIN, CLASSES, DOC, PANELS, SEP, SOURCE, VALUES

from fixtures.lens.make_lens import valid_table
from rl import lens, recipes, render


def masked(text, role):
    return text.replace(render.rl_block(role["row_cap"]), "<RL-BLOCK>")


@pytest.mark.parametrize("gone", CLASSES)
def test_removing_one_recipe_leaves_every_other_part_byte_identical(gone):
    table, cut = valid_table(), valid_table()
    full = recipes.load()
    short = {c: v for c, v in full.items() if c != gone}
    for panel in cut["panels"].values():
        for role in panel["roles"].values():
            role["lens"] = [c for c in role["lens"] if c != gone]
    errs = lens.validate(cut, card_ids=set(CLASSES) - {gone}, recipes=short)
    # Still valid, or only the two rules that count classes break: rule 5 (the REQ-25 duplicate sets, which name the
    # class in their expected set) and rule 6 (a lens that keeps fewer than 2 recipes once C2 is dropped). Rules 1
    # to 4 hold: removing a class never leaves the card, recipe, cap or model checks wrong.
    assert all(e.startswith(("rule 5", "rule 6")) for e in errs), errs
    assert all(gone in e for e in errs if e.startswith("rule 5")), errs
    checked = 0
    for panel in PANELS:
        base = lens.render(panel, True, B_MIN[panel], VALUES["c"], table=table)
        abl = lens.render(
            panel, True, B_MIN[panel], VALUES["c"], table=cut, recipes=short
        )
        for role, b in base.items():
            before = render.brief(b, DOC, SOURCE, recipes=full)
            after = render.brief(abl[role], DOC, SOURCE, recipes=short)
            assert after["z0_sha256"] == before["z0_sha256"]
            want = masked(before["text"], b).replace(SEP + lens.printed(gone, full), "")
            assert masked(after["text"], abl[role]) == want, (panel, role)
            assert gone not in after["recipes"]
            assert after["recipes"] == [c for c in before["recipes"] if c != gone]
            checked += 1
    assert checked == 9


def test_the_ablated_class_changes_only_its_own_brief_parts():
    """The two renders differ for a class that a lens holds, and only there (the test above is not vacuous)."""
    full = recipes.load()
    cut = copy.deepcopy(valid_table())
    cut["panels"]["primary"]["roles"]["L1"]["lens"] = ["C1", "C3"]
    a = lens.render("primary", True, B_MIN["primary"], VALUES["c"])
    b = lens.render("primary", True, B_MIN["primary"], VALUES["c"], table=cut)
    assert (
        render.brief(a["L1"], DOC, SOURCE, recipes=full)["text"]
        != render.brief(b["L1"], DOC, SOURCE, recipes=full)["text"]
    )
    for role in ("S", "L2"):
        assert (
            render.brief(a[role], DOC, SOURCE, recipes=full)["text"]
            == render.brief(b[role], DOC, SOURCE, recipes=full)["text"]
        )
