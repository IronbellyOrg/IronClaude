"""Class cards (REQ-06, REQ-10, DD-11): schema, instances, promotion category, a ninth card as data only."""

import copy
import json
import re
import shutil

import jsonschema
import pytest
from helpers import REPO, SW

from scaffold import cards, fnd

CARDS = SW / "cards"
IDS = [f"C{i}" for i in range(1, 9)]
MR = (
    REPO
    / ".dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md"
)
CITE = re.compile(r"^[\w./-]+(:\d+(-\d+)?(,\d+(-\d+)?)*)?$")
# phrases that would tell the reviewer what the answer is (AO-8)
OUTCOME = re.compile(
    r"\b(is|are|was|were) (a |an )?(defect|defective|bug|wrong|broken|stale|missing)\b"
    r"|\b(will|must|does|do) (always )?fail\b|\bnever (match|pass)|\bcannot (match|pass)\b"
    r"|\bthe (defect|problem|bug)\b",
    re.IGNORECASE,
)


def card_c9(**over):
    """An invented ninth class; no real class, package or file name."""
    c = {
        "id": "C9",
        "name": "Invented sample class",
        "version": 1,
        "definition": "A numbered step refers to a figure that no earlier step defines.",
        "question_template": "Which earlier step defines this figure? Quote it, or answer PROBLEM.",
        "extractor": None,
        "route": "search",
        "replicas": 1,
        "applies_to": ["doc"],
        "instances": [
            {"cite": "notes/alpha.md:10", "target": "doc", "kind": "P"},
            {"cite": "notes/beta.md:20-22", "target": "doc", "kind": "I"},
        ],
        "severity_guidance": "Blocking when the figure decides an outcome.",
        "known_weakness": "Figures defined by a table the reader never sees.",
        "promote_category": "other",
        "swap_test": {"reviewer": "", "date": ""},
    }
    c.update(over)
    return c


def mr_questions():
    out = {}
    for ln in MR.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split(" | ")]
        if re.match(r"^C[1-8]$", cells[0]) and len(cells) == 3 and cells[2][:1] == '"':
            out[cells[0]] = cells[2][1:-1]
    return out


def mr_definitions():
    out = {}
    for ln in MR.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split(" | ")]
        if re.match(r"^C[1-8]$", cells[0]) and len(cells) == 6:
            out[cells[0]] = cells[1]
    return out


def test_schema_valid():
    schema = json.loads((CARDS / "schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    loaded = cards.load()
    assert list(loaded) == IDS
    for cid, card in loaded.items():
        assert json.loads((CARDS / f"{cid}.json").read_text(encoding="utf-8")) == card
        assert list(jsonschema.Draft202012Validator(schema).iter_errors(card)) == []
        assert cards.validate(card) == []
    assert cards.validate(card_c9()) == []


def test_schema_checker_agrees_with_jsonschema_on_broken_cards():
    """cards.validate is a stdlib reading of the schema; it must reject what the jsonschema package rejects."""
    schema = json.loads((CARDS / "schema.json").read_text(encoding="utf-8"))
    ref = jsonschema.Draft202012Validator(schema)
    good = cards.load()["C4"]
    mutations = {
        "missing field": lambda c: c.pop("route"),
        "unknown field": lambda c: c.update(extra=1),
        "bad route": lambda c: c.update(route="skim"),
        "bad id": lambda c: c.update(id="X4"),
        "version string": lambda c: c.update(version="1"),
        "version bool": lambda c: c.update(version=True),
        "replicas 3": lambda c: c.update(replicas=3),
        "extractor name": lambda c: c.update(extractor="Z9"),
        "empty applies_to": lambda c: c.update(applies_to=[]),
        "repeated applies_to": lambda c: c.update(applies_to=["plan", "plan"]),
        "bad target": lambda c: c.update(applies_to=["slide"]),
        "one instance": lambda c: c.update(instances=c["instances"][:1]),
        "instance without kind": lambda c: c["instances"][0].pop("kind"),
        "short question": lambda c: c.update(question_template="Why?"),
        "swap_test without date": lambda c: c["swap_test"].pop("date"),
    }
    for name, mutate in mutations.items():
        bad = copy.deepcopy(good)
        mutate(bad)
        assert list(ref.iter_errors(bad)), name
        assert cards.validate(bad), name
    ok = copy.deepcopy(good)
    ok["extractor"] = None
    assert not list(ref.iter_errors(ok)) and cards.validate(ok) == []


def test_each_card_has_two_instances():
    for cid, card in cards.load().items():
        inst = card["instances"]
        assert len(inst) >= 2, cid
        cites = [i["cite"] for i in inst]
        assert len(set(cites)) == len(cites), cid
        for c in cites:
            assert CITE.match(c), (cid, c)


def test_promote_category_valid():
    assert set(fnd.CATEGORIES) >= {"contradiction", "unpassable-check"}
    for cid, card in cards.load().items():
        assert card["promote_category"] in fnd.CATEGORIES, cid
        assert cards.promote_category(cid) == card["promote_category"]
    bad = copy.deepcopy(cards.load()["C1"])
    bad["promote_category"] = "typo"
    assert any("FND.CATEGORIES" in e for e in cards.validate(bad))


def test_fixture_card_c9_needs_no_dispatcher_change(tmp_path):
    """REQ-10: a ninth class is one data file. cards.py holds no class id and still serves the new card."""
    src = (SW / "scaffold" / "cards.py").read_text(encoding="utf-8")
    assert not re.search(r"\bC[0-9]\b", src)
    work = tmp_path / "cards"
    shutil.copytree(CARDS, work, ignore=shutil.ignore_patterns("README.md"))
    c9 = card_c9()
    (work / "C9.json").write_text(json.dumps(c9), encoding="utf-8")
    loaded = cards.load(work)
    assert list(loaded) == [*IDS, "C9"]
    assert cards.questions(loaded)["C9"] == c9["question_template"]
    assert cards.routes(loaded)["C9"] == "search"
    assert cards.promote_category("C9", loaded) == "other"
    assert cards.definition("C9", loaded) == c9["definition"]
    assert len(cards.questions(loaded)) == 9
    (work / "C10.json").write_text(
        json.dumps(card_c9(id="C10", route="skim")), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="C10.json"):
        cards.load(work)
    (work / "C10.json").write_text(json.dumps(card_c9(id="C11")), encoding="utf-8")
    with pytest.raises(ValueError, match="differs from the file name"):
        cards.load(work)


def test_routes_extractors_and_replicas():
    loaded = cards.load()
    assert cards.routes(loaded) == {
        "C1": "read",
        "C2": "read",
        "C3": "read",
        "C4": "search",
        "C5": "search",
        "C6": "search",
        "C7": "read",
        "C8": "search",
    }
    assert {i: c["extractor"] for i, c in loaded.items()} == {
        "C1": "E1",
        "C2": "E5",
        "C3": "E6",
        "C4": "E2",
        "C5": "E4",
        "C6": "E1",
        "C7": "E7",
        "C8": "E3",
    }
    assert {c["replicas"] for c in loaded.values()} == {2}
    # swap test (AO-2) signed for C1 to C8 on 2026-11-15 by a second-author session
    assert all(
        c["swap_test"]
        == {"reviewer": "second-author-session claude-sonnet-5-5", "date": "2026-11-15"}
        for c in loaded.values()
    )


def test_questions_are_neutral_and_only_c3_has_a_placeholder():
    qs = cards.questions()
    assert len(qs) == 8
    for cid, q in qs.items():
        assert "?" in q or q.startswith("Name "), cid  # a question or an instruction
        assert not OUTCOME.search(q), (cid, "states an expected outcome")
        assert ("«value»" in q) == (cid == "C3"), cid
        assert not re.search(r"[«»{}<>]", q.replace("«value»", "")), cid


def test_outcome_pattern_is_not_vacuous():
    assert OUTCOME.search("This criterion is wrong because it cannot match.")
    assert OUTCOME.search("The test will fail here.")
    assert not OUTCOME.search(cards.questions()["C4"])


@pytest.mark.skipif(not MR.exists(), reason="the requirements file is not present")
def test_questions_and_definitions_are_verbatim_from_mr():
    assert cards.questions() == mr_questions()
    loaded = cards.load()
    assert {i: cards.definition(i, loaded) for i in loaded} == mr_definitions()
