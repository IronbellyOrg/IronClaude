"""Briefs (REQ-01, REQ-05, REQ-09, REQ-23): parts, arms, hashes. MR and RR are read as files; nothing else is."""

import hashlib
import re

import pytest
from helpers import REPO, SW
from judge_support import brief_of, jj_brief

from scaffold import briefs, cards, fnd

BRIEFS = SW / "briefs"
MR = (
    REPO
    / ".dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md"
)
RR = (
    REPO
    / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh"
)
CAND = "/tmp/evalsb-sweep/cand/p1/candidate.md"
SHA = "ab" * 32
SOURCE = "/tmp/evalsb-sweep/cand/p1/source.md"
SHEET_PATH = "/tmp/evalsb-sweep/run1/sheets/r1.md"
SHEET_TEXT = "Items assigned to you: S1, S2\n\n### S1   (class C4)\nWhere: Task 1\n"
DOC = {"cand_sb": CAND, "sha": SHA}
ITEMS = {"path": SHEET_PATH, "text": SHEET_TEXT}
FIRST_LINE = f"/sc:spec-panel @{CAND} --mode critique"
# DESIGN 8.1, written out here so the code cannot grade itself
Z0 = ["base", "cb1", "cb2", "cb3", "cb4", "cb5"]
EXPECTED = {
    "Z0-raw": ["base"],
    "Z0": Z0,
    "K": [*Z0, "k"],
    "SS": [*Z0, "ledger-rule", "sheet-block"],
}


def part(name):
    return (BRIEFS / briefs.FILES[name]).read_text(encoding="utf-8")


def render(arm, source=SOURCE, items=ITEMS, **kw):
    return briefs.render(arm, DOC, items, source, **kw)


def test_cb1_rendered_with_source():
    r = render("Z0")
    assert f"Driving document: {SOURCE}. Read it in full before you review" in r["text"]
    assert "{{SOURCE_ABS}}" not in r["text"] and r["parts"][1] == "cb1"
    assert r["no_source"] is False


@pytest.mark.parametrize("arm", ["Z0", "K", "SS"])
@pytest.mark.parametrize("source", [None, ""])
def test_cb1_absent_without_source(arm, source):
    r = render(arm, source=source)
    assert "Driving document:" not in r["text"] and "cb1" not in r["parts"]
    assert r["no_source"] is True
    for cb in ("cb2", "cb3", "cb4", "cb5"):
        assert cb in r["parts"]


def test_cb_verbatim_against_mr():
    mr = MR.read_text(encoding="utf-8")
    assert set(briefs.MR_OPENINGS) == {
        "cb1",
        "cb2",
        "cb3",
        "cb4",
        "cb5",
        "ledger-rule",
        "sheet-block",
    }
    for name, opening in briefs.MR_OPENINGS.items():
        quoted = briefs.mr_quote(mr, opening)
        assert (BRIEFS / briefs.FILES[name]).read_bytes() == quoted.encode("utf-8"), (
            name
        )
    assert "{{SOURCE_ABS}}" in part("cb1")
    assert "{{SHEET_PATH}}" in part("sheet-block")
    # the rule behind the extraction: a missing or doubled block is an error, not a guess
    with pytest.raises(ValueError):
        briefs.mr_quote(mr, "No such opening words")
    with pytest.raises(ValueError):
        briefs.mr_quote('> "One block"\n> "One block again"\n', "One block")


def test_arm_part_sets():
    for arm, names in EXPECTED.items():
        assert set(render(arm)["parts"]) == set(names), arm
        assert render(arm)["parts"] == names, arm  # and the order
    # the optional parts: CB-1 needs a source; the SS parts need a sheet
    assert set(briefs.part_names("Z0", False, False)) == set(Z0) - {"cb1"}
    assert set(briefs.part_names("SS", True, False)) == set(Z0)
    assert set(briefs.part_names("SS", True, True)) == set(EXPECTED["SS"])
    assert set(briefs.part_names("K", True, True)) == set(EXPECTED["K"])
    assert set(briefs.part_names("Z0-raw", True, True)) == {"base"}
    assert set(briefs.ARMS) == set(EXPECTED)
    with pytest.raises(ValueError):
        briefs.part_names("RL", True, True)  # reserved, not built here
    # every part of every arm exists as a file (the K paragraph's lead-in is a file too)
    assert {briefs.FILES[n] for n in briefs.FILES} == {p.name for p in BRIEFS.iterdir()}


def test_base_equals_rr_lines_13_17():
    first, last, text = briefs.rr_brief(RR.read_text(encoding="utf-8"))
    assert (first, last) == (13, 17)
    assert (BRIEFS / "base.txt").read_bytes() == text.encode("utf-8")
    base = part("base")
    assert base.startswith("/sc:spec-panel @$CAND_SB --mode critique\n")
    assert "$SHA" in base
    for arm in briefs.ARMS:
        assert render(arm)["text"].startswith(FIRST_LINE + "\n"), arm
    # what bash makes of the string: the two variables expanded, nothing else
    raw = render("Z0-raw")["text"]
    assert raw == text.replace("$CAND_SB", CAND).replace("$SHA", SHA)
    assert f"(sha256 of the file: {SHA})" in raw and "$" not in raw


def test_six_categories_unchanged():
    base = part("base")
    m = re.search(r"category ((?:[a-z-]+\|)+[a-z-]+),", base)
    assert m
    assert m.group(1).split("|") == list(fnd.CATEGORIES) and len(fnd.CATEGORIES) == 6
    assert "Grade it Medium when the sentence needs a guess" in base
    assert "'An implementer who follows the stated text as written builds X" in base
    for arm in briefs.ARMS:
        assert render(arm)["text"].startswith(
            part("base").replace("$CAND_SB", CAND).replace("$SHA", SHA)
        )


def test_empty_sheet_brief_equals_z0_by_hash():
    for source in (SOURCE, None):
        z0 = render("Z0", source=source)
        for empty in (
            None,
            {},
            {"path": SHEET_PATH, "text": ""},
            {"path": "", "text": " \n"},
        ):
            ss = render("SS", source=source, items=empty)
            assert ss["sha256"] == z0["sha256"]
            assert hashlib.sha256(ss["text"].encode()).hexdigest() == z0["sha256"]
            assert ss["no_trigger"] is True and ss["fallback"] is False
    assert render("SS")["sha256"] != render("Z0")["sha256"]
    assert render("SS")["no_trigger"] is False


def test_fallback_brief_equals_z0_by_hash():
    z0 = render("Z0")
    ss = render(
        "SS", fallback=True
    )  # a sheet exists, but the pre-pass or the render failed
    assert ss["sha256"] == z0["sha256"] and ss["parts"] == z0["parts"]
    assert ss["fallback"] is True and ss["no_trigger"] is False
    # fallback is a fact about arm SS only
    assert render("Z0", fallback=True)["fallback"] is False
    assert render("Z0", fallback=True)["sha256"] == z0["sha256"]


def test_no_src_path_in_any_brief():
    for f in BRIEFS.iterdir():
        assert "src/superclaude/" not in f.read_text(encoding="utf-8"), f.name
    for arm in briefs.ARMS:
        for source in (SOURCE, None):
            r = render(arm, source=source)
            assert "src/superclaude/" not in r["text"], arm
    assert "src/superclaude/" not in briefs.k_paragraph()


def test_sheet_block_filled_and_followed_by_items():
    r = render("SS")
    t = r["text"]
    assert f"built {SHEET_PATH} from the candidate" in t and "{{SHEET_PATH}}" not in t
    block = part("sheet-block").replace("{{SHEET_PATH}}", SHEET_PATH)
    assert t.endswith(f"{block}\n\n## SWEEP SHEET ITEMS\n\n{SHEET_TEXT.rstrip()}")
    assert (
        t.index(part("ledger-rule")) < t.index(block) < t.index("## SWEEP SHEET ITEMS")
    )
    assert t.index(part("cb5")) < t.index(part("ledger-rule"))
    with pytest.raises(ValueError):
        render("SS", items={"text": "x"})  # a sheet without its file path


def test_k_paragraph_from_the_eight_cards():
    cs = cards.load()
    p = briefs.k_paragraph(cs)
    assert "\n" not in p and len(cs) == 8
    for n, cid in enumerate(cs, 1):
        assert f"({n}) {cards.definition(cid, cs)}" in p
    positions = [p.index(cards.definition(c, cs)) for c in cs]
    assert positions == sorted(positions)
    assert render("K")["text"].endswith("\n\n" + p)
    # the draft marker is a comment: first line of k-lead.txt, never sent
    lead = part("k").splitlines()
    assert lead[0].startswith("# DRAFT") and "owner approval (DD-14)" in lead[0]
    assert "DRAFT" not in p and "owner approval" not in p
    # one governing source: changing a card changes the paragraph (REQ-10)
    changed = {k: dict(v) for k, v in cs.items()}
    changed["C3"]["definition"] = "An invented replacement definition."
    assert "An invented replacement definition." in briefs.k_paragraph(changed)
    assert render("K", cards=changed)["sha256"] != render("K")["sha256"]


def test_sha256_of_every_part_and_brief():
    ph = briefs.part_hashes()
    assert set(ph) == set(briefs.FILES)
    for name, f in briefs.FILES.items():
        assert ph[name] == hashlib.sha256((BRIEFS / f).read_bytes()).hexdigest()
    for arm in briefs.ARMS:
        r = render(arm)
        assert r["sha256"] == hashlib.sha256(r["text"].encode("utf-8")).hexdigest()
        assert set(r["part_sha256"]) == set(r["parts"])
    # a brief is stable: the same inputs give the same hash
    assert render("SS")["sha256"] == render("SS")["sha256"]
    assert render("SS")["sha256"] != render("K")["sha256"]


def test_judge_brief_sha_equals_jj():
    """REQ-43: the BRIEF of bin/judge-one.sh is byte-identical to lines 12 to 23 of the earlier study's judge worker."""
    mine = brief_of(SW / "bin" / "judge-one.sh")
    assert (
        hashlib.sha256(mine.encode()).hexdigest()
        == hashlib.sha256(jj_brief().encode()).hexdigest()
    )
    assert len(jj_brief().splitlines()) == 12
