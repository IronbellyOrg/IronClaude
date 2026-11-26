"""Extractor E5 (class C2, DESIGN 4.6): source rules whose identifiers no citing task carries.

Each extractor test has a positive case, a negative case, a near-miss or boundary case and a determinism case.
E5 reads only the candidate and the source (no repository), so no snapshot is built. The plan fixtures are
fixtures/plans/p_basic.md with fixtures/plans/source.md: Task 3 cites sections 2.3 and Q4, and the source rule of 2.3
names `deleted_count`, `RetentionError` and `age_limit_days`, none of which Task 3 carries.
"""

import json
from pathlib import Path

import pytest

from sweep import extractors, plan
from sweep.extractors import Candidate, Ctx

PLANS = Path(__file__).resolve().parents[1] / "fixtures" / "plans"
BASIC_TEXT = (PLANS / "p_basic.md").read_text(encoding="utf-8")
SOURCE_TEXT = (PLANS / "source.md").read_text(encoding="utf-8")
RULE_23 = "The job must write `deleted_count` to the run log and must halt with `RetentionError` when `age_limit_days` is unset."
FIRST_T3 = "Create `src/exporter/retention.py` and `tests/test_retention.py`."


def mkplan(
    body="Edit `src/exporter/report.py` for it.",
    cites="2.3",
    criterion="`make test` exits 0.",
):
    """A one-task plan: the body is line 3, the citation line 5, the criterion bullet line 8."""
    cite = f"Source sections: {cites}\n\n" if cites else ""
    return plan.parse(
        f"## Task 1: Change the report\n\n{body}\n\n{cite}Acceptance criteria:\n- {criterion}\n"
    )


def mksource(*sections):
    """A source with one `## <number> Title` section per (number, text) pair, in a blank-line separated layout."""
    return plan.parse(
        "# Source\n\n" + "".join(f"## {n} Title {n}\n\n{t}\n\n" for n, t in sections)
    )


def src23():
    """A source whose section 2.3 holds only the retention rule (the fixture's own 2.3 holds a second rule)."""
    return mksource(("2.3", RULE_23))


def find(doc, source, **kw):
    return extractors.find_e5(doc, Ctx(doc, source=source, **kw))


def run(doc, source, **kw):
    ctx = Ctx(doc, source=source, **kw)
    cands = extractors.find_e5(doc, ctx)
    extractors.attach_e5(cands, ctx)
    return cands


def basic(**kw):
    return run(plan.parse(BASIC_TEXT), plan.parse(SOURCE_TEXT), **kw)


def dump(cands):
    return json.dumps([c.to_dict() for c in cands], sort_keys=True)


def source_line(fragment):
    return next(i for i, t in enumerate(SOURCE_TEXT.split("\n"), 1) if fragment in t)


# ---------------------------------------------------------------- no source (REQ-01 part)


def test_no_source_returns_nothing():
    """E5 runs only when a source exists; without one it returns nothing and Ctx reports C2 as not applicable."""
    doc = plan.parse(BASIC_TEXT)
    ctx = Ctx(doc)
    assert extractors.find_e5(doc, ctx) == []
    assert ctx.no_source is True
    assert ctx.not_applicable == {"C2": "no_source"}
    assert ctx.tasks_without_citations == []  # E5 did not run, so it counted nothing
    # through the two-phase run, with the real registry entry
    assert extractors.EXTRACTORS["E5"] == (extractors.find_e5, extractors.attach_e5)
    assert extractors.run_extractors(ctx, {"E5": extractors.EXTRACTORS["E5"]}) == []


def test_with_a_source_class_c2_applies():
    doc = plan.parse(BASIC_TEXT)
    ctx = Ctx(doc, source=plan.parse(SOURCE_TEXT))
    assert ctx.no_source is False
    assert ctx.not_applicable == {}


def test_an_empty_source_gives_nothing_but_still_counts_tasks_without_citations():
    doc = plan.parse(BASIC_TEXT)
    ctx = Ctx(doc, source=plan.parse(""))
    assert extractors.find_e5(doc, ctx) == []
    assert ctx.tasks_without_citations == ["T5"]


# ---------------------------------------------------------------- positive


def test_basic_plan_gives_the_retention_rule_for_task_3():
    (c,) = basic()
    assert (c.extractor, c.cls, c.kind) == ("E5", "C2", "section")
    assert c.anchor_text == FIRST_T3  # the `Depends on: Task 1` line is no sentence
    assert c.location["task"] == "T3"
    assert BASIC_TEXT.split("\n")[c.location["line_start"] - 1].startswith(FIRST_T3)
    f = c.features
    assert f["ref"] == "2.3" and f["rule"] == RULE_23
    assert f["rule_line"] == source_line("The job must write")
    assert f["ids"] == ["deleted_count", "RetentionError", "age_limit_days"]
    assert (
        f["missing"] == f["ids"]
    )  # `legal_hold` is the other rule's, and Task 3 carries it
    assert c.pre_priority == 30 + 15 * 3 == 75 and c.priority == 75
    assert c.evidence == [
        {"path": "source", "line": f["rule_line"], "text": RULE_23},
        {
            "path": "source",
            "line": f["rule_line"],
            "text": "missing identifiers: deleted_count, RetentionError, age_limit_days",
        },
        {"path": "plan", "line": c.location["line_start"], "text": FIRST_T3},
    ]


def test_candidates_pass_the_core_checks_and_take_the_class_route():
    doc = plan.parse(BASIC_TEXT)
    ctx = Ctx(doc, source=plan.parse(SOURCE_TEXT))
    got = extractors.run_extractors(ctx, {"E5": extractors.EXTRACTORS["E5"]})
    assert [(c.cls, c.route, c.status) for c in got] == [("C2", "read", "attached")]
    assert got[0].evidence_computed and got[0].priority == 75


def test_a_decision_line_is_a_cited_section():
    src = plan.parse(
        "# S\n\n## Decisions\n\nQ4: the job must write `run_total` once.\n"
        "It never reads `other_total` again.\n\nQ5: the step must write `skipped_total`.\n"
    )
    got = find(
        mkplan(cites="Q4"), src
    )  # the decision runs to the blank line, so Q5 is not part of it
    assert [(c.kind, c.features["ref"], c.features["missing"]) for c in got] == [
        ("decision", "Q4", ["run_total"]),
        ("decision", "Q4", ["other_total"]),
    ]
    assert [c.features["rule_line"] for c in got] == [5, 6]
    assert [c.features["missing"] for c in find(mkplan(cites="Q5"), src)] == [
        ["skipped_total"]
    ]


def test_a_decision_bullet_and_its_continuation_line():
    src = plan.parse(
        "# S\n\n- **Q4**: the job must write\n  `run_total` once.\n- Q5: the step must write `skipped_total`.\n"
    )
    (c,) = find(mkplan(cites="Q4"), src)
    assert c.features["missing"] == ["run_total"]
    assert c.features["rule"].endswith("the job must write `run_total` once.")


def test_sub_sections_belong_to_the_cited_section():
    src = plan.parse(
        "## 2.3 Job\n\nIntro text.\n\n### 2.3.1 Detail\n\nThe job shall report `job_total`.\n\n## 2.4 Next\n\nIt must set `next_flag`.\n"
    )
    (c,) = find(mkplan(cites="2.3"), src)
    assert c.features["missing"] == ["job_total"] and c.features["rule_line"] == 7


# ---------------------------------------------------------------- negative


def test_task_that_carries_every_identifier_gives_no_candidate():
    body = "Write `deleted_count`, raise `RetentionError` and read `age_limit_days`."
    assert find(mkplan(body=body), src23()) == []
    # the fixture's 2.3 also holds the `legal_hold` rule, which this task does not carry
    (c,) = find(mkplan(body=body), plan.parse(SOURCE_TEXT))
    assert c.features["missing"] == ["legal_hold"]


def test_an_identifier_in_the_criteria_counts_as_carried():
    ids = "`deleted_count`, `RetentionError`, `age_limit_days`"
    assert find(mkplan(criterion=f"The log holds {ids}."), src23()) == []
    (c,) = find(mkplan(criterion="The log holds `deleted_count`."), src23())
    assert c.features["missing"] == ["RetentionError", "age_limit_days"]


def test_a_rule_without_identifiers_gives_no_candidate():
    assert (
        find(mkplan(cites="2.1"), plan.parse(SOURCE_TEXT)) == []
    )  # "must support the formats csv, json, ..."


def test_a_task_that_cites_nothing_is_counted_and_gives_no_candidate():
    doc = mkplan(cites=None)
    ctx = Ctx(doc, source=plan.parse(SOURCE_TEXT))
    assert extractors.find_e5(doc, ctx) == []
    assert ctx.tasks_without_citations == ["T1"]


def test_tasks_without_citations_are_listed_for_the_basic_plan_and_reset_on_each_call():
    doc = plan.parse(BASIC_TEXT)
    ctx = Ctx(doc, source=plan.parse(SOURCE_TEXT))
    extractors.find_e5(doc, ctx)
    extractors.find_e5(doc, ctx)
    assert ctx.tasks_without_citations == ["T5"]
    clean = plan.parse((PLANS / "p_clean.md").read_text(encoding="utf-8"))
    ctx = Ctx(clean, source=plan.parse(SOURCE_TEXT))
    assert extractors.find_e5(clean, ctx) == []
    assert ctx.tasks_without_citations == ["T1", "T2", "T3"]


def test_a_citation_that_matches_no_source_section_gives_nothing_and_is_not_counted():
    doc = mkplan(cites="9.9, Q77")
    ctx = Ctx(doc, source=plan.parse(SOURCE_TEXT))
    assert extractors.find_e5(doc, ctx) == []
    assert ctx.tasks_without_citations == []


# ---------------------------------------------------------------- near misses and boundaries


@pytest.mark.parametrize(
    "sentence,is_rule",
    [
        ("The job must write `deleted_count`.", True),
        (
            "The job returns `result_code` at the end.",
            True,
        ),  # a backticked identifier and a return verb
        ("The job halts on `RetentionError`.", True),
        (
            "The job likes `deleted_count` very much.",
            False,
        ),  # a backticked identifier, no rule verb
        (
            "The job writes results to the log.",
            False,
        ),  # a verb, no backticked identifier
        (
            "Mustard is a plant and `deleted_count` is a name.",
            False,
        ),  # "must" is not a word here
        ("Each run of `job_total` counts.", True),
    ],
)
def test_rule_sentence_selection(sentence, is_rule):
    src = mksource(("2.3", sentence))
    got = find(mkplan(), src)
    assert bool(got) is is_rule


def test_section_numbers_match_whole_numbers_only():
    src = plan.parse(
        "## 2.30 Other\n\nIt must set `other_flag`.\n\n## 2.3 Job\n\nIt must set `job_flag`.\n"
    )
    (c,) = find(mkplan(cites="2.3"), src)
    assert c.features["missing"] == ["job_flag"]
    (c,) = find(mkplan(cites="2.30"), src)
    assert c.features["missing"] == ["other_flag"]


def test_fenced_lines_and_headings_are_no_rule_sentences():
    src = plan.parse(
        "## 2.3 Job\n\n```text\nIt must set `fenced_flag`.\n```\n\n### It must set `heading_flag`\n\nPlain words only.\n"
    )
    assert find(mkplan(cites="2.3"), src) == []


def test_a_numbered_heading_inside_a_fence_does_not_end_or_start_a_section():
    src = plan.parse("## 2.3 Job\n\n```\n## 2.4 Fake\n```\n\nIt must set `job_flag`.\n")
    (c,) = find(mkplan(cites="2.3"), src)
    assert c.features["missing"] == ["job_flag"]
    assert find(mkplan(cites="2.4"), src) == []


def test_identifiers_are_case_sensitive():
    body = "Write `deleted_count` and `retentionerror` and `AGE_LIMIT_DAYS`."
    (c,) = find(mkplan(body=body), src23())
    assert c.features["missing"] == ["RetentionError", "age_limit_days"]


@pytest.mark.parametrize(
    "sentence,ids",
    [
        ("It must set `a_b` and `Name`.", ["a_b", "Name"]),
        ("It must set door_open_ms and DoorTimeout.", ["door_open_ms", "DoorTimeout"]),
        ("It must set doorTimeout.", ["doorTimeout"]),
        (
            "It must set JSON and Door and door.",
            [],
        ),  # an all-capital word and a plain word are no identifier
        (
            "It must set `src/a_b/c.py`.",
            ["src/a_b/c.py"],
        ),  # a backticked path is one id; its snake_case is no second
        ("It must run `make test`.", []),  # a backticked span with a space is a command
        ("It must set `a_b` and a_b.", ["a_b"]),  # each once
        ("It must set `" + "x" * 81 + "`.", []),
    ],
)
def test_identifier_extraction(sentence, ids):
    assert extractors._e5_ids(sentence) == ids


@pytest.mark.parametrize(
    "n,expected", [(1, 45), (2, 60), (3, 75), (4, 90), (5, 90), (6, 90)]
)
def test_pre_priority_is_30_plus_15_per_missing_identifier_up_to_four(n, expected):
    ids = [f"id_{i}" for i in range(n)]
    src = mksource(("2.3", "It must set " + ", ".join(f"`{i}`" for i in ids) + "."))
    (c,) = find(mkplan(), src)
    assert len(c.features["missing"]) == n and c.pre_priority == expected


def test_two_rule_sentences_are_two_candidates_with_one_anchor_in_source_order():
    src = mksource(("2.3", "It must set `a_one`. It shall report `b_two`."))
    got = find(mkplan(), src)
    assert [c.features["missing"] for c in got] == [["a_one"], ["b_two"]]
    assert len({c.anchor_text for c in got}) == 1
    assert [c.features["rule_line"] for c in got] == [5, 5]  # both on one source line


def test_a_section_cited_twice_through_two_citations_makes_one_candidate():
    (c,) = find(mkplan(cites="2.3, 2.3"), src23())
    assert c.features["ref"] == "2.3"
    src = plan.parse("## 2.3 Job\n\n### 2.3.1 Part\n\nIt must set `job_flag`.\n")
    assert len(find(mkplan(cites="2.3, 2.3.1"), src)) == 1


def test_a_task_without_a_sentence_of_twelve_characters_gives_no_candidate():
    assert find(mkplan(body="Do it."), plan.parse(SOURCE_TEXT)) == []


def test_a_long_first_sentence_is_cut_to_200_characters_and_stays_an_exact_quote():
    body = "Edit the report writer " + "and keep going " * 20 + "now."
    (c,) = find(mkplan(body=body), src23())
    assert len(c.anchor_text) <= 200 and c.anchor_text in " ".join(body.split())
    ctx = Ctx(mkplan(body=body), source=src23())
    c.validate(ctx)  # an exact quote of the candidate, 12 to 200 characters


def test_evidence_texts_are_cut_to_160_characters_and_there_are_three_entries():
    long_rule = (
        "It must set `long_id` " + "with a very long explanation " * 12 + "today."
    )
    (c,) = run(mkplan(), mksource(("2.3", long_rule)))
    assert len(c.evidence) == 3 <= extractors.EVIDENCE_MAX
    assert all(len(e["text"]) <= 160 for e in c.evidence)
    assert c.features["rule"].endswith("today.")  # the whole rule stays in features


def test_attach_needs_no_snapshot_and_sets_priority_to_pre_priority():
    (c,) = run(mkplan(), src23())
    assert c.priority == c.pre_priority == 75
    c.priority = None
    extractors.attach_e5([c], Ctx(mkplan(), source=src23()))
    assert c.priority == 75


def test_a_candidate_with_only_its_features_can_be_attached_again():
    (c,) = find(mkplan(), src23())
    twin = Candidate(
        c.extractor, c.cls, c.kind, c.anchor_text, dict(c.location),
        features=dict(c.features), pre_priority=c.pre_priority,
    )  # fmt: skip
    extractors.attach_e5([c, twin], Ctx(mkplan(), source=src23()))
    assert twin.evidence == c.evidence and twin.priority == c.priority


# ---------------------------------------------------------------- determinism


def test_the_output_is_the_same_on_every_run():
    assert dump(basic()) == dump(basic()) == dump(basic(seed=5))
    doc = plan.parse(BASIC_TEXT)
    src = plan.parse(SOURCE_TEXT)
    a = extractors.run_extractors(
        Ctx(doc, source=src), {"E5": extractors.EXTRACTORS["E5"]}
    )
    b = extractors.run_extractors(
        Ctx(doc, source=src), {"E5": extractors.EXTRACTORS["E5"]}
    )
    assert dump(a) == dump(b)
