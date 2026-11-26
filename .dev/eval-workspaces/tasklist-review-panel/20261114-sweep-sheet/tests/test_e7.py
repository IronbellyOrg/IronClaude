"""Extractor E7 (class C7, DESIGN 4.8): clauses of a constraint that dictated text leaves out.

Each extractor test has a positive case, a negative case, a near-miss or boundary case and a determinism case.
E7 is lexical (no repository, no source). On fixtures/plans/p_basic.md the constraint K2 ("A deletion notice must name
the report id, state the expiry date, and give the appeal address.") has three clauses; the dictated block of Task 4
("Report id 41 has expired. The expiry date is 2027-01-01.") shares `expiry` and `date` with clause 2, `report` with
clause 1 and nothing with clause 3 (`appeal`, `address`).
"""

import json
import re
from pathlib import Path

import pytest

from sweep import extractors, plan
from sweep.extractors import Candidate, Ctx

PLANS = Path(__file__).resolve().parents[1] / "fixtures" / "plans"
BASIC_TEXT = (PLANS / "p_basic.md").read_text(encoding="utf-8")
CLEAN_TEXT = (PLANS / "p_clean.md").read_text(encoding="utf-8")
FIRST_D1 = "Report id 41 has expired."
K2 = "A deletion notice must name the report id, state the expiry date, and give the appeal address."
FORBIDDEN = re.compile(r"defect|severity|\bclaim", re.IGNORECASE)


def mkplan(
    constraint=K2, dictated="> Report id 41 has expired. The expiry date is 2027-01-01."
):
    """A one-task plan: the constraint is line 3, the dictated text line 9."""
    return plan.parse(
        f"## Constraints\n\n- {constraint}\n\n## Task 1: Write it\n\nWrite the notice as quoted.\n\n{dictated}\n\n"
        "Acceptance criteria:\n- `make test` exits 0.\n"
    )


def find(doc, **kw):
    return extractors.find_e7(doc, Ctx(doc, **kw))


def run(doc, **kw):
    ctx = Ctx(doc, **kw)
    cands = extractors.find_e7(doc, ctx)
    extractors.attach_e7(cands, ctx)
    return cands


def basic(**kw):
    return run(plan.parse(BASIC_TEXT), **kw)


def dump(cands):
    return json.dumps([c.to_dict() for c in cands], sort_keys=True)


def shares(
    constraint, dictated="> Report id 41 has expired. The expiry date is 2027-01-01."
):
    return find(mkplan(constraint, dictated))


# ---------------------------------------------------------------- positive


def test_basic_plan_gives_the_omitted_appeal_clause_for_the_task_4_text():
    (c,) = basic()
    assert (c.extractor, c.cls, c.kind) == ("E7", "C7", "clause")
    assert c.anchor_text == FIRST_D1
    assert c.location["task"] == "T4"
    assert (
        BASIC_TEXT.split("\n")[c.location["line_start"] - 1]
        == "> " + FIRST_D1 + " The expiry date is 2027-01-01."
    )
    f = c.features
    assert f["constraint"] == "K2" and BASIC_TEXT.split("\n")[
        f["constraint_line"] - 1
    ].endswith("appeal address.")
    assert [r["shared"] for r in f["clauses"]] == [["report"], ["date", "expiry"], []]
    assert f["clauses"][2]["distinct"] == ["address", "appeal"]
    assert f["best"] == 1 and f["zero"] == [2]
    assert c.pre_priority == 30 + 15 * 1 + 10 == 55 and c.priority == 55
    line = f["constraint_line"]
    assert c.evidence == [
        {"path": "plan", "line": line, "text": "clause 1: 'A deletion notice must name the report id' - tokens found in the block: report"},
        {"path": "plan", "line": line, "text": "clause 2: 'state the expiry date' - tokens found in the block: date, expiry"},
        {"path": "plan", "line": line, "text": "clause 3: 'give the appeal address.' - tokens found in the block: none"},
    ]  # fmt: skip


def test_candidates_pass_the_core_checks_and_take_the_class_route():
    doc = plan.parse(BASIC_TEXT)
    got = extractors.run_extractors(Ctx(doc), {"E7": extractors.EXTRACTORS["E7"]})
    assert [(c.cls, c.route, c.status) for c in got] == [("C7", "read", "attached")]
    assert got[0].evidence_computed and got[0].priority == 55
    assert extractors.EXTRACTORS["E7"] == (extractors.find_e7, extractors.attach_e7)


def test_a_second_dictated_block_and_a_second_constraint_each_make_a_pair():
    doc = plan.parse(
        "## Constraints\n\n- "
        + K2
        + "\n- A deletion notice must carry the policy number, show the renewal period, "
        "and list the refund channel.\n\n## Task 1: Write it\n\nWrite as quoted.\n\n> Expiry date set. The report is old.\n\n"
        "## Task 2: Write more\n\nWrite as quoted.\n\n> Renewal period shown. The policy number is 7.\n"
    )
    got = find(doc)
    assert [(c.features["constraint"], c.location["task"]) for c in got] == [
        ("K1", "T1"), ("K2", "T2"),
    ]  # fmt: skip


# ---------------------------------------------------------------- negative


def test_p_clean_gives_nothing():
    doc = plan.parse(CLEAN_TEXT)
    assert find(doc) == []
    assert (
        extractors.run_extractors(Ctx(doc), {"E7": extractors.EXTRACTORS["E7"]}) == []
    )


def test_a_plan_without_dictated_text_or_without_a_constraint_gives_nothing():
    no_text = (
        "## Constraints\n\n- "
        + K2
        + "\n\n## Task 1: Do\n\nEdit `a.py` for the notice.\n"
    )
    assert find(plan.parse(no_text)) == []
    assert (
        find(
            plan.parse(
                "## Task 1: Do\n\nWrite as quoted.\n\n> Expiry date set today.\n"
            )
        )
        == []
    )


def test_a_text_that_carries_every_clause_gives_nothing():
    text = (
        "> The report names a deletion notice, the expiry date and the appeal address."
    )
    assert shares(K2, text) == []


# ---------------------------------------------------------------- near misses and boundaries


def test_one_shared_token_is_not_enough():
    assert (
        shares(K2, "> The expiry is soon.") == []
    )  # `expiry` only (and `date` is missing)
    assert len(shares(K2, "> The expiry date is soon.")) == 1


def test_no_clause_with_zero_overlap_gives_nothing():
    # `report` reaches clause 1 and `address` reaches clause 3, so no clause is left out
    assert shares(K2, "> The report shows the expiry date and the address.") == []


def test_a_token_found_in_two_clauses_is_not_distinctive():
    c = "The notice must show the expiry date, show the expiry year now, and give the appeal address."
    (cand,) = shares(
        c, "> The expiry date and the notice are shown. The expiry year is clear."
    )
    rows = cand.features["clauses"]
    assert [r["distinct"] for r in rows] == [
        ["date", "notice"],
        ["year"],
        ["address", "appeal"],
    ]  # not `expiry`, `show`
    assert [r["shared"] for r in rows] == [["date", "notice"], ["year"], []]
    # `expiry` alone is no distinctive token, so a text that holds only it matches nothing
    assert shares(c, "> The expiry is shown. The expiry is clear.") == []
    # with `expiry` the only shared word, nothing is distinctive enough
    assert shares(c, "> The expiry is shown. The expiry is clear.") == []


def test_a_clause_of_three_words_is_dropped():
    block = mkplan(
        "The notice must name the report id, state the date, and give the appeal address."
    ).of("constraint")[0]
    assert [t for _, t in extractors._e7_clauses(block)] == [
        "The notice must name the report id",
        "give the appeal address.",
    ]  # "state the date" has 3 words; the sentence's last clause keeps its full stop


def test_a_zero_overlap_clause_needs_a_distinctive_token():
    # clause 3 has words, but each is a stop word or shorter than four characters, so it proves nothing
    c = "The notice must name the report id, state the expiry date, and use it for all of them."
    assert shares(c) == []


def test_words_of_three_characters_and_stop_words_are_not_tokens():
    assert extractors._e7_tokens("the report id must have been made with them") == {
        "report"
    }


def test_splits_at_semicolon_comma_and_and_keeps_longer_clauses_whole():
    c = "The notice must state the expiry date; the notice must name the report id and give the appeal address"
    block = mkplan(c).of("constraint")[0]
    assert [t for _, t in extractors._e7_clauses(block)] == [
        "The notice must state the expiry date",
        "the notice must name the report id",
        "give the appeal address",
    ]
    block = mkplan("Keep the old format and the new format for the readers").of(
        "constraint"
    )[0]
    assert [t for _, t in extractors._e7_clauses(block)] == [
        "Keep the old format",
        "the new format for the readers",
    ]


def test_a_nested_bullet_is_its_own_clause_group_and_lines_are_numbered():
    doc = plan.parse(
        "## Constraints\n\n- The notice must name the report id.\n  - It must state the expiry date.\n"
        "- It must give the appeal address.\n\n## Task 1: W\n\nWrite as quoted.\n\n> Report id and expiry date.\n"
    )
    (block,) = [b for b in doc.of("constraint")][:1]
    got = extractors._e7_clauses(block)
    assert [(ln, t) for ln, t in got] == [
        (3, "The notice must name the report id."),
        (4, "It must state the expiry date."),
    ]


@pytest.mark.parametrize(
    "extra,zero,expected",
    [
        ("", 1, 55),
        (", and offer the refund channel", 2, 70),
        (
            ", and offer the refund channel, and show the policy number",
            3,
            70,
        ),  # the zero-overlap term stops at 2
    ],
)
def test_pre_priority_is_30_plus_15_per_zero_overlap_clause_plus_10(
    extra, zero, expected
):
    c = K2.rstrip(".") + extra + "."
    (cand,) = shares(c)
    assert len(cand.features["zero"]) == zero and cand.pre_priority == expected
    assert 55 <= cand.pre_priority <= 70


def test_every_emitted_candidate_is_ranked_55_to_70():
    seen = []
    for text in (BASIC_TEXT, CLEAN_TEXT):
        seen += basic() if text is BASIC_TEXT else run(plan.parse(text))
    for n in range(1, 6):
        c = (
            K2.rstrip(".")
            + "".join(
                f", and offer the extra feature number {k} here" for k in range(n)
            )
            + "."
        )
        seen += run(mkplan(c))
    assert seen and all(
        55 <= c.pre_priority <= 70 and c.priority == c.pre_priority for c in seen
    )


def test_with_more_than_five_clauses_the_evidence_keeps_the_sharing_and_the_zero_overlap_clauses():
    parts = [
        f"offer the extra feature number {w} here"
        for w in ("alpha", "bravo", "charlie", "delta", "echo")
    ]
    c = (
        "A deletion notice must name the report id, state the expiry date, "
        + ", ".join(parts)
        + "."
    )
    (cand,) = run(mkplan(c))
    assert len(cand.features["clauses"]) == 7
    assert len(cand.evidence) == extractors.EVIDENCE_MAX
    texts = [e["text"] for e in cand.evidence]
    assert texts[0].startswith("clause 1:") and texts[1].startswith(
        "clause 2:"
    )  # the sharing clauses, in order
    assert sum("tokens found in the block: none" in t for t in texts) >= 2
    assert [int(re.match(r"clause (\d+):", t)[1]) for t in texts] == sorted(
        int(re.match(r"clause (\d+):", t)[1]) for t in texts
    )


def test_the_anchor_is_the_first_sentence_of_twelve_characters_cut_to_200_and_an_exact_quote():
    (c,) = shares(K2, "> Ok. Report id 41 has expired. The expiry date is 2027-01-01.")
    assert c.anchor_text == FIRST_D1
    long = (
        "Report id 41 has expired "
        + "and the notice goes out " * 12
        + "today. The expiry date is soon."
    )
    (c,) = shares(K2, "> " + long)
    assert len(c.anchor_text) <= 200 and c.anchor_text in " ".join(long.split())
    c.validate(Ctx(mkplan(K2, "> " + long)))


def test_a_fenced_dictated_block_is_read_too():
    (c,) = shares(
        K2, "```text\nReport id 41 has expired.\nThe expiry date is 2027-01-01.\n```"
    )
    assert c.anchor_text.startswith("Report id 41 has expired.")


def test_evidence_texts_are_cut_to_160_characters_and_hold_no_claim_severity_or_defect():
    long = (
        "A deletion notice must name the report id, state the expiry date "
        + "with a very long explanation " * 8
        + ", and give the appeal address."
    )
    (c,) = run(mkplan(long))
    assert len(c.evidence) <= extractors.EVIDENCE_MAX
    assert all(len(e["text"]) <= 160 for e in c.evidence)
    assert all(
        len(re.match(r"clause \d+: '([^']*)'", e["text"])[1]) <= 100 for e in c.evidence
    )
    for cand in [c, *basic()]:
        assert not any(FORBIDDEN.search(e["text"]) for e in cand.evidence)


def test_attach_needs_no_snapshot_and_sets_priority_to_pre_priority():
    (c,) = basic()
    c.priority = None
    extractors.attach_e7([c], Ctx(plan.parse(BASIC_TEXT)))
    assert c.priority == c.pre_priority == 55


def test_a_candidate_with_only_its_features_can_be_attached_again():
    doc = plan.parse(BASIC_TEXT)
    (c,) = find(doc)
    twin = Candidate(
        c.extractor, c.cls, c.kind, c.anchor_text, dict(c.location),
        features=json.loads(json.dumps(c.features)), pre_priority=c.pre_priority,
    )  # fmt: skip
    extractors.attach_e7([c, twin], Ctx(doc))
    assert twin.evidence == c.evidence and twin.priority == c.priority


# ---------------------------------------------------------------- determinism


def test_the_output_is_the_same_on_every_run():
    assert dump(basic()) == dump(basic()) == dump(basic(seed=5))
    doc = plan.parse(BASIC_TEXT)
    a = extractors.run_extractors(Ctx(doc), {"E7": extractors.EXTRACTORS["E7"]})
    b = extractors.run_extractors(Ctx(doc), {"E7": extractors.EXTRACTORS["E7"]})
    assert dump(a) == dump(b)
