"""Extractor E6 (class C3, experimental, DESIGN 4.7): a backticked value that is read and never written.

Each extractor test has a positive case, a negative case, a near-miss or boundary case and a determinism case.
E6 is lexical (no repository, no source). On fixtures/plans/p_basic.md Task 3 says "The purge step keys on `legal_hold`
and leaves such reports in place." and no other sentence writes `legal_hold`, so it is the one E6 item of that plan.
Every E6 item carries `experimental: true` (REQ-21).
"""

import json
from pathlib import Path

import pytest

from sweep import extractors, plan
from sweep.extractors import Candidate, Ctx

PLANS = Path(__file__).resolve().parents[1] / "fixtures" / "plans"
BASIC_TEXT = (PLANS / "p_basic.md").read_text(encoding="utf-8")
CLEAN_TEXT = (PLANS / "p_clean.md").read_text(encoding="utf-8")
T3_SENTENCE = "The purge step keys on `legal_hold` and leaves such reports in place."


def mkplan(body, criterion="`make test` exits 0.", constraint=None):
    """A one-task plan: the body is line 3, the criterion bullet line 6; a constraint is a bullet at line 3 and moves
    the task down by four lines."""
    head = f"## Constraints\n\n- {constraint}\n\n" if constraint else ""
    return plan.parse(
        f"{head}## Task 1: Change it\n\n{body}\n\nAcceptance criteria:\n- {criterion}\n"
    )


def find(doc, **kw):
    return extractors.find_e6(doc, Ctx(doc, **kw))


def run(doc, **kw):
    ctx = Ctx(doc, **kw)
    cands = extractors.find_e6(doc, ctx)
    extractors.attach_e6(cands, ctx)
    return cands


def basic(**kw):
    return run(plan.parse(BASIC_TEXT), **kw)


def dump(cands):
    return json.dumps([c.to_dict() for c in cands], sort_keys=True)


def literals(cands):
    return [c.features["literal"] for c in cands]


# ---------------------------------------------------------------- registration


def test_e6_is_registered_and_all_seven_extractors_are_in_the_table():
    assert extractors.EXTRACTORS["E6"] == (extractors.find_e6, extractors.attach_e6)
    assert set(extractors.EXTRACTORS) == set(extractors.EXTRACTOR_IDS)
    assert tuple(sorted(extractors.EXTRACTORS)) == tuple(f"E{i}" for i in range(1, 8))
    for eid, (find_fn, attach_fn) in extractors.EXTRACTORS.items():
        assert callable(find_fn) and callable(attach_fn), eid
        assert find_fn.__name__ == f"find_{eid.lower()}"
        assert attach_fn.__name__ == f"attach_{eid.lower()}"


# ---------------------------------------------------------------- positive


def test_basic_plan_gives_the_one_unwritten_literal_of_task_3():
    (c,) = basic()
    assert (c.extractor, c.cls, c.kind) == ("E6", "C3", "unwritten")
    assert c.anchor_text == T3_SENTENCE
    assert c.location["task"] == "T3"
    assert BASIC_TEXT.split("\n")[c.location["line_start"] - 1] == (
        "Create `src/exporter/retention.py` and `tests/test_retention.py`. "
        + T3_SENTENCE
    )
    f = c.features
    assert (
        f["literal"] == "legal_hold" and f["read_count"] == 1 and f["write_count"] == 0
    )
    assert c.pre_priority == 25 and c.priority == 25


def test_every_item_is_marked_experimental():
    items = basic() + run(mkplan("The job runs when `a_flag` is on."))
    assert len(items) == 2
    for c in items:
        assert c.features["experimental"] is True
        assert c.to_dict()["features"]["experimental"] is True


def test_evidence_is_the_read_quote_and_the_zero_write_count():
    (c,) = basic()
    assert c.evidence == [
        {"path": "plan", "line": c.location["line_start"], "text": T3_SENTENCE},
        {
            "path": "plan",
            "line": c.location["line_start"],
            "text": "write-position occurrences of 'legal_hold': 0",
        },
    ]
    c.validate(Ctx(plan.parse(BASIC_TEXT)))


@pytest.mark.parametrize(
    "phrase",
    ["keys on", "when", "is read", "returns for", "depends on", "KEYS ON"],
)
def test_each_read_phrase_makes_a_candidate(phrase):
    got = find(mkplan(f"The purge step {phrase} `legal_hold` here."))
    assert literals(got) == ["legal_hold"]


def test_the_double_equals_sign_is_a_read_position():
    got = find(mkplan("The purge step skips a row where `legal_hold` == true here."))
    assert literals(got) == ["legal_hold"]


def test_read_in_a_criterion_and_in_a_constraint_is_found():
    d = mkplan(
        "Edit the retention job as the plan says.",
        criterion="The job keys on `held_flag` for each report.",
        constraint="The notice is built when `locale_code` is known.",
    )
    got = find(d)
    assert sorted(literals(got)) == ["held_flag", "locale_code"]
    by = {c.features["literal"]: c for c in got}
    assert by["held_flag"].location["task"] == "T1"
    assert by["locale_code"].location["task"] is None


@pytest.mark.parametrize(
    "reads, want",
    [(1, 25), (2, 30), (3, 35), (4, 35), (6, 35)],
)
def test_pre_priority_is_20_plus_5_per_read_capped_at_3(reads, want):
    body = "\n\n".join(
        f"The step reads when `legal_hold` is {i}." for i in range(reads)
    )
    (c,) = find(mkplan(body))
    assert c.pre_priority == want
    assert c.features["read_count"] == reads
    assert c.location["line_start"] == 3
    assert len(run(mkplan(body))[0].evidence) == min(reads, 3) + 1


def test_two_literals_in_one_read_sentence_make_two_candidates():
    got = find(mkplan("The job keys on `alpha_one` and `beta_two` together."))
    assert literals(got) == ["alpha_one", "beta_two"]
    assert got[0].anchor_text == got[1].anchor_text


# ---------------------------------------------------------------- negative


def test_clean_plan_gives_nothing():
    assert run(plan.parse(CLEAN_TEXT)) == []


@pytest.mark.parametrize(
    "write",
    [
        "The setup sets `legal_hold` to false.",
        "The setup gives `legal_hold` a default.",
        "The setup writes `legal_hold` to the log.",
        "The setup assigns `legal_hold` a value.",
        "The setup produces `legal_hold` per report.",
        "The setup returns `legal_hold` to the caller.",
        "Set `legal_hold = false` at load.",
        "The load step does legal_hold = 1 once.",
    ],
)
def test_a_write_position_occurrence_anywhere_clears_the_literal(write):
    body = f"The purge step keys on `legal_hold` here.\n\n{write}"
    assert find(mkplan(body)) == []
    # the same write in a criterion or in a constraint clears it as well
    assert (
        find(mkplan("The purge step keys on `legal_hold` here.", criterion=write)) == []
    )
    assert (
        find(
            mkplan(
                "The purge step keys on `legal_hold` here.", constraint=write.strip()
            )
        )
        == []
    )


def test_a_sentence_that_reads_and_writes_the_literal_clears_it():
    assert (
        find(mkplan("The step keys on `legal_hold` and sets `legal_hold` back.")) == []
    )


def test_no_read_position_makes_no_candidate():
    assert find(mkplan("The purge step uses `legal_hold` for each report.")) == []


def test_a_literal_without_backticks_is_not_a_candidate():
    assert find(mkplan("The purge step keys on legal_hold here.")) == []


def test_a_depends_on_line_is_not_a_read():
    d = plan.parse(
        "## Task 1: A\n\nWrite it.\n\n## Task 2: B\n\nDepends on: `Task_1`\n\nWrite it too.\n"
    )
    assert find(d) == []


# ---------------------------------------------------------------- near-miss and boundary


def test_returns_for_is_a_read_not_a_write():
    d = mkplan("The cache returns for `legal_hold` the stored row.")
    assert literals(find(d)) == ["legal_hold"]


@pytest.mark.parametrize("op", ["!=", "<=", ">=", "=>"])
def test_a_comparison_sign_is_not_a_write(op):
    got = find(mkplan(f"The purge step keys on `legal_hold` here, and x {op} y."))
    assert literals(got) == ["legal_hold"]


def test_a_sign_or_word_inside_backticks_is_not_a_position():
    # the sign "=" is read inside a span (a sentence with an assignment writes what it names), a word is not
    assert find(mkplan("The step keys on `legal_hold` with `mode = x` here.")) == []
    got = find(mkplan("The step keys on `legal_hold` and `sets` here."))
    assert "legal_hold" in literals(got)
    # a read word inside backticks is not a read position
    assert find(mkplan("The step uses `legal_hold` and `when` here.")) == []


def test_a_bare_write_of_the_literal_clears_it_but_a_longer_word_does_not():
    base = "The purge step keys on `legal_hold` here.\n\n"
    assert find(mkplan(base + "The loader sets legal_hold on load.")) == []
    got = find(mkplan(base + "The loader sets legal_hold_flag on load."))
    assert literals(got) == ["legal_hold"]


def test_a_command_a_path_and_a_long_span_are_not_literals():
    for span in (
        "grep -c 'x' docs/guide.md",
        "pytest tests/test_x.py -q",
        "src/exporter/retention.py",
        "tests/*.py",
        "x" * 81,
    ):
        assert find(mkplan(f"The purge step keys on `{span}` here.")) == [], span


def test_literals_are_compared_exactly():
    body = (
        "The step keys on `Legal_Hold` here.\n\nThe loader sets `legal_hold` on load."
    )
    assert literals(find(mkplan(body))) == ["Legal_Hold"]


def test_a_wrapped_read_sentence_keeps_a_quote_of_the_plan_as_its_anchor():
    body = "The purge step keys on `legal_hold`\nand leaves such reports\nin place."
    (c,) = find(mkplan(body))
    assert (
        c.anchor_text
        == "The purge step keys on `legal_hold` and leaves such reports in place."
    )
    assert (c.location["line_start"], c.location["line_end"]) == (3, 5)


def test_a_long_sentence_is_cut_to_200_characters():
    body = "The purge step keys on `legal_hold` " + "and more words " * 20 + "here."
    (c,) = find(mkplan(body))
    assert len(c.anchor_text) <= 200 and c.anchor_text.startswith(
        "The purge step keys on `legal_hold` and more"
    )
    c.validate(Ctx(mkplan(body)))


# ---------------------------------------------------------------- determinism and the core run


def test_same_input_same_output():
    doc = plan.parse(BASIC_TEXT)
    assert dump(run(doc)) == dump(run(doc)) == dump(run(plan.parse(BASIC_TEXT)))


def test_attach_works_on_a_candidate_read_back_from_json():
    doc = plan.parse(BASIC_TEXT)
    ctx = Ctx(doc)
    (c,) = extractors.find_e6(doc, ctx)
    d = c.to_dict()
    back = Candidate(
        d["extractor"], d["class"], d["kind"], d["anchor_text"], d["location"],
        features=d["features"], pre_priority=d["pre_priority"],
    )  # fmt: skip
    extractors.attach_e6([back], ctx)
    assert back.evidence[1]["text"] == "write-position occurrences of 'legal_hold': 0"
    assert back.priority == back.pre_priority


def test_core_run_keeps_the_experimental_label_and_the_class_route():
    doc = plan.parse(BASIC_TEXT)
    out = extractors.run_extractors(Ctx(doc), {"E6": extractors.EXTRACTORS["E6"]})
    (c,) = out
    assert c.status == "attached" and c.evidence_computed and c.priority == 25
    assert c.route == "read"  # card C3
    assert c.to_dict()["features"]["experimental"] is True
