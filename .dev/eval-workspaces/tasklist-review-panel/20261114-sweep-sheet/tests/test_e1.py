"""Extractor E1 (classes C1 and C6, DESIGN 4.2): set words and the scope they name.

Each extractor test has a positive case, a negative case, a near-miss or boundary case and a determinism case.
`find_e1` is lexical; `attach_e1` reads the plan's own lines and, for a universal sentence, the enforcing test file of
the snapshot built by fixtures/repos/build_repo.py (git runs there only).
"""

import json
from pathlib import Path

import pytest

from fixtures.repos.build_repo import build_repo
from scaffold import cards
from sweep import extractors, plan
from sweep.extractors import Candidate, Ctx

PLANS = Path(__file__).resolve().parents[1] / "fixtures" / "plans"
BASIC_TEXT = (PLANS / "p_basic.md").read_text(encoding="utf-8")
EVERY = (
    "Every module under `src/exporter/` returns an empty result for an empty report."
)
NO_REMAINING = "No remaining `3 report formats` text exists in `docs/guide.md`."
ONLY = (
    "`tests/test_retention.py` shows that only the retention job removes a report file."
)
LIMITER_SENTENCE = "Leave `tests/test_retention.py` as it is; it skips any report whose hold flag is set."
FORBIDDEN = ("claim", "severity", "defect")


def basic_line(fragment):
    """The 1-based line of p_basic.md that holds fragment (the plan's own line numbers)."""
    return next(i for i, t in enumerate(BASIC_TEXT.split("\n"), 1) if fragment in t)


def mkplan(
    criterion="`make test` exits 0.", body="Edit `src/exporter/report.py` for it."
):
    """A one-task plan: line 3 holds the body and line 6 the criterion bullet."""
    return plan.parse(
        f"## Task 1: Change the report\n\n{body}\n\nAcceptance criteria:\n- {criterion}\n"
    )


def find(doc, snapshot=None, **kw):
    return extractors.find_e1(doc, Ctx(doc, snapshot=snapshot, **kw))


def run(doc, snapshot=None, **kw):
    ctx = Ctx(doc, snapshot=snapshot, **kw)
    cands = extractors.find_e1(doc, ctx)
    extractors.attach_e1(cands, ctx)
    return cands


def basic(snapshot=None, **kw):
    return run(plan.parse(BASIC_TEXT), snapshot, **kw)


def by_kind(cands, kind):
    return [c for c in cands if c.kind == kind]


def dump(cands):
    return json.dumps([c.to_dict() for c in cands], sort_keys=True)


def texts(c):
    return [e["text"] for e in c.evidence]


def held_repo(tmp_path, test_text):
    return build_repo(tmp_path, extra={"tests/test_retention.py": test_text}).repo


# ---------------------------------------------------------------- positive: the two case kinds on p_basic.md


def test_registered_in_the_extractor_table():
    assert extractors.EXTRACTORS["E1"] == (extractors.find_e1, extractors.attach_e1)


def test_positive_unbounded_set_word_beside_a_narrower_instruction_scope():
    (c,) = [c for c in basic() if c.anchor_text == EVERY]
    assert (c.extractor, c.cls, c.kind, c.route) == ("E1", "C1", "completeness", "read")
    line = basic_line(EVERY)
    assert c.location == {"task": "T1", "line_start": line, "line_end": line}
    f = c.features
    assert (f["bound_none"], f["scope_differs"], f["set_word_count"]) == (1, 1, 1)
    assert (f["bound"], f["instr_scope"], f["sent_scope"]) == (
        "none",
        ["src/exporter/report.py"],
        ["src/exporter/"],
    )
    assert c.pre_priority == 30 + 25 + 25 + 0 and c.priority == c.pre_priority
    # both scopes side by side, each with its plan line
    assert c.evidence == [
        {
            "path": "plan",
            "line": basic_line("Edit `src/exporter/report.py` so that"),
            "text": "instruction scope: [src/exporter/report.py]",
        },
        {
            "path": "plan",
            "line": line,
            "text": "criterion scope: [src/exporter/], bound: none",
        },
    ]


def test_positive_no_remaining_with_equal_scopes_is_ranked_lower():
    (c,) = [c for c in basic() if c.anchor_text == NO_REMAINING]
    assert c.cls == "C1" and (
        c.features["bound_none"],
        c.features["scope_differs"],
    ) == (1, 0)
    assert c.pre_priority == 30 + 25
    assert texts(c) == [
        "instruction scope: [docs/guide.md]",
        "criterion scope: [docs/guide.md], bound: none",
    ]


def test_positive_universal_sentence_beside_a_skip_rule():
    (c,) = by_kind(basic(), "universal")
    assert (c.extractor, c.cls, c.anchor_text, c.route) == ("E1", "C6", ONLY, "search")
    line = basic_line(ONLY)
    assert c.location == {"task": "T3", "line_start": line, "line_end": line}
    assert (c.features["names_path"], c.features["set_word_count"]) == (1, 1)
    assert c.pre_priority == 30 + 20
    # no snapshot: the skip rule of task 4 (shown as its own sentence) and the test file the plan names
    assert c.evidence == [
        {
            "path": "plan",
            "line": basic_line("skips any report"),
            "text": LIMITER_SENTENCE,
        },
        {
            "path": "plan",
            "line": line,
            "text": "enforcing test named by the plan: tests/test_retention.py",
        },
    ]
    assert c.features["limiter_lines"] == 1 and c.features["test_defs"] is None
    assert c.priority == 50 + 20 + 20


def test_positive_the_enforcing_test_file_in_the_snapshot_adds_its_count_and_limiter_lines(
    tmp_path,
):
    src = (
        "def test_a():\n    pass\n\n# skip a report on legal hold\n"
        "def test_purge_keeps_held():\n    pass\n\n# only the job may purge\n"
    )
    (c,) = by_kind(basic(held_repo(tmp_path, src)), "universal")
    rel = "tests/test_retention.py"
    assert c.evidence == [
        {
            "path": "plan",
            "line": basic_line("skips any report"),
            "text": LIMITER_SENTENCE,
        },
        {
            "path": "plan",
            "line": basic_line(ONLY),
            "text": f"enforcing test named by the plan: {rel}",
        },
        {"path": rel, "line": 0, "text": f"2 def test_ functions in {rel}"},
        {"path": rel, "line": 4, "text": "# skip a report on legal hold"},
        {"path": rel, "line": 8, "text": "# only the job may purge"},
    ]
    assert c.features["test_defs"] == 2
    assert c.priority == 90


def test_positive_a_planned_test_file_that_is_not_in_the_snapshot_says_so(tmp_path):
    (c,) = by_kind(basic(build_repo(tmp_path).repo), "universal")
    assert (
        texts(c)[-1]
        == "enforcing test named by the plan: tests/test_retention.py (not in the snapshot)"
    )
    assert c.priority == 90 and c.features["test_defs"] is None


def test_positive_evidence_is_capped_at_five_and_a_file_with_limiter_lines_keeps_a_slot(
    tmp_path,
):
    body = "\n".join(
        f"Keep `tests/test_hold.py` out of reach; skip {n}." for n in range(3)
    )
    doc = mkplan("`tests/test_hold.py` shows that only the job runs.", body)
    src = "# skip one\n# skip two\n# skip three\n# skip four\ndef test_x():\n    pass\n"
    (c,) = run(doc, build_repo(tmp_path, extra={"tests/test_hold.py": src}).repo)
    assert len(c.evidence) == 5
    paths = [e["path"] for e in c.evidence]
    # 2 plan limiter lines, the enforcing-test line, the count, and 1 limiter line of the file
    assert paths == ["plan", "plan", "plan", "tests/test_hold.py", "tests/test_hold.py"]
    assert texts(c)[2].startswith("enforcing test named by the plan")
    assert c.evidence[4]["text"] == "# skip one"
    assert c.features["limiter_lines"] == 3
    c.validate(Ctx(doc))


def test_positive_both_kinds_from_one_sentence():
    cs = find(mkplan("Only the job removes every report."))
    assert [(c.kind, c.cls) for c in cs] == [
        ("completeness", "C1"),
        ("universal", "C6"),
    ]
    assert cs[0].anchor_text == cs[1].anchor_text


def test_positive_a_set_word_in_dictated_text_is_read():
    doc = plan.parse(
        "## Task 1: Notice\n\nWrite the notice as the quote below.\n\n> All notices end with the appeal address.\n"
        "\nAcceptance criteria:\n- `make test` exits 0.\n"
    )
    (c,) = find(doc)
    assert c.anchor_text == "All notices end with the appeal address."
    assert c.location["line_start"] == 5


def test_positive_a_goal_sentence_has_no_instruction_scope():
    doc = plan.parse(
        "Goal: Every report in `src/exporter/` is written.\n\n## Task 1: A task\n\nEdit `a/b.py`.\n"
    )
    (c,) = run(doc)
    assert c.features["instr_scope"] == [] and c.features["scope_differs"] == 0
    assert texts(c)[0] == "instruction scope: [NONE]"
    assert texts(c)[1] == "criterion scope: [src/exporter/], bound: none"


# ---------------------------------------------------------------- negative


def test_negative_nothing_on_the_clean_plan():
    doc = plan.parse((PLANS / "p_clean.md").read_text(encoding="utf-8"))
    assert find(doc) == [] and run(doc) == []


def test_negative_a_task_body_is_not_an_input_block():
    assert find(mkplan(body="Every module under `src/` needs the change.")) == []


def test_negative_a_set_word_inside_a_longer_word_is_not_one():
    for text in (
        "The overall result is shown here.",
        "Allowed values are listed in it.",
        "It is an all-in-one report.",
    ):
        assert find(mkplan(text)) == [], text


# ---------------------------------------------------------------- the 12-character floor and bullets


def test_boundary_a_sentence_of_11_characters_is_ignored_and_one_of_12_is_read():
    assert len("All rows ok.") == 12 and len("All rows o.") == 11
    assert [c.anchor_text for c in find(mkplan("All rows ok."))] == ["All rows ok."]
    assert find(mkplan("All rows o.")) == []
    assert find(mkplan("Every row.")) == []


def test_boundary_a_long_sentence_gives_its_first_200_characters():
    sent = "Every row " + "x" * 300 + "."
    (c,) = find(mkplan(sent))
    assert c.anchor_text == sent[:200] and len(c.anchor_text) == 200


def test_boundary_a_block_is_split_at_bullets_and_sentence_ends():
    cs = find(
        mkplan(
            "Every row is written. The rest is plain\n  - All cells are written too\n  - Nothing else here."
        )
    )
    assert [c.anchor_text for c in cs] == [
        "Every row is written.",
        "All cells are written too",
    ]
    assert [c.location["line_start"] for c in cs] == [6, 7]


# ---------------------------------------------------------------- bound types, scope sets and the formulas


@pytest.mark.parametrize(
    "sentence, bound, bound_none",
    [
        ("Every file in `a/x.py` and `b/y.py` is listed.", "closed_list", 0),
        ("Every file matching `src/*.py` is checked.", "glob", 1),
        ("Every file matching `*.py` is checked.", "glob", 1),
        ("Every file matching `a/x.py` and `*.py` is checked.", "glob", 1),
        ("All 3 reports are written.", "count", 0),
        ("Every file in `a/x.py` is checked.", "none", 1),
        ("Every file on the list is checked.", "none", 1),
        ("All `2 reports` are written.", "none", 1),
    ],
)
def test_bound_types(sentence, bound, bound_none):
    (c,) = find(mkplan(sentence))
    assert (c.features["bound"], c.features["bound_none"]) == (bound, bound_none)


def test_scope_sets_are_sorted_and_compared_as_sets():
    body = "Edit `b/two.py`, `a/one.py` and `src/*.py`."
    (c,) = find(
        mkplan("Every file in `a/one.py`, `src/*.py` and `b/two.py` is checked.", body)
    )
    assert (
        c.features["instr_scope"]
        == c.features["sent_scope"]
        == ["a/one.py", "b/two.py", "src/*.py"]
    )
    assert c.features["scope_differs"] == 0
    (d,) = find(mkplan("Every file in `a/one.py` is checked.", body))
    assert d.features["scope_differs"] == 1
    (e,) = find(
        mkplan("Every file is checked.", body)
    )  # an empty sentence scope never differs
    assert (e.features["sent_scope"], e.features["scope_differs"]) == ([], 0)


def test_the_instruction_scope_is_the_task_body_before_the_label_only():
    doc = plan.parse(
        "## Task 1: A\n\nEdit `a/one.py`.\n\nAcceptance criteria:\n- Every file in `b/two.py` is checked.\n"
        "- It reads `c/three.py`.\n\n## Task 2: B\n\nEdit `d/four.py`.\n\nAcceptance criteria:\n- Each file is read.\n"
    )
    c1, c2 = find(doc)
    assert c1.features["instr_scope"] == ["a/one.py"]
    assert c2.features["instr_scope"] == ["d/four.py"]


@pytest.mark.parametrize(
    "sentence, extra",
    [
        ("Every row is written.", 0),
        ("Every row and each column is written.", 5),
        ("Every row, each column and all cells are written.", 10),
        ("Every row, each column, all cells and every cover are written.", 10),
    ],
)
def test_pre_priority_completeness_formula(sentence, extra):
    (c,) = find(mkplan(sentence))
    assert c.pre_priority == 30 + 25 + extra  # bound none, no scope on the sentence


@pytest.mark.parametrize(
    "sentence, names, count, pre",
    [
        ("Only the job removes a report.", 0, 1, 30),
        ("Only the job in `src/job.py` removes a report.", 1, 1, 50),
        ("Only `test_job.py` removes a report, never another.", 1, 2, 55),
        ("Only the job removes a report, never a copy, and no other file.", 0, 3, 40),
        ("Only the job, never a copy, no other file and never twice.", 0, 4, 40),
        ("Files outside `src/` hold nothing of ours.", 1, 1, 50),
    ],
)
def test_pre_priority_universal_formula(sentence, names, count, pre):
    (c,) = by_kind(find(mkplan(sentence)), "universal")
    assert (c.features["names_path"], c.features["set_word_count"], c.pre_priority) == (
        names,
        count,
        pre,
    )


def test_the_pair_outside_nothing_needs_that_order():
    assert find(mkplan("Nothing is written outside the folder.")) == []
    assert len(find(mkplan("Files outside the folder hold nothing."))) == 1


def test_a_universal_priority_adds_the_limiter_and_the_test_terms(tmp_path):
    # no limiter line, no test file named
    (c,) = run(mkplan("Only the job in `src/job.py` removes a report."))
    assert (c.pre_priority, c.priority, c.evidence) == (50, 50, [])
    # a limiter line only
    doc = mkplan(
        "Only the job in `src/job.py` removes a report.",
        "Edit `src/job.py`; it ignores held reports.",
    )
    (c,) = run(doc)
    assert c.priority == 70 and len(c.evidence) == 1 and c.evidence[0]["line"] == 3
    # the test file only
    (c,) = run(mkplan("Only the job removes a report; `tests/test_job.py` passes."))
    assert (c.pre_priority, c.priority) == (50, 70)
    assert texts(c) == ["enforcing test named by the plan: tests/test_job.py"]


def test_the_enforcing_test_comes_from_the_same_task_or_the_gate():
    doc = plan.parse(
        "## Task 1: A\n\nEdit `a/b.py`.\n\nAcceptance criteria:\n- `tests/test_one.py` is run.\n\n"
        "## Task 2: B\n\nEdit `c/d.py`.\n\nAcceptance criteria:\n- Only the job changes `c/d.py`.\n"
        "- `tests/test_two.py` is run.\n"
    )
    (c,) = find(doc)
    assert c.features["enforcing_test"] == "tests/test_two.py"
    solo = plan.parse(
        "## Task 1: A\n\nEdit `a/b.py`.\n\nAcceptance criteria:\n- Only the job changes `a/b.py`.\n"
    )
    assert find(solo)[0].features["enforcing_test"] is None
    for tok, ok in (
        ("`test_x.py`", True),
        ("`pkg/tests/x.py`", True),
        ("`tests/`", False),
        ("`src/x.py`", False),
    ):
        (d,) = find(mkplan(f"Only the job changes it; {tok} is run."))
        assert (d.features["enforcing_test"] is not None) == ok, tok


def test_the_sentence_itself_is_not_its_own_limiter_line():
    (c,) = run(mkplan("Only the job in `src/job.py` removes a report."))
    assert c.features["limiter_lines"] == 0


# ---------------------------------------------------------------- evidence text limits and wording


def test_a_long_scope_is_cut_at_whole_tokens_and_the_bound_stays():
    toks = [f"src/pkg{n:02d}/module_{n:02d}.py" for n in range(12)]
    (c,) = run(
        mkplan(
            "Every file in `src/x/` is read.",
            "Edit " + ", ".join(f"`{t}`" for t in toks) + ".",
        )
    )
    first = c.evidence[0]["text"]
    assert (
        len(first) <= 160
        and first.startswith("instruction scope: [src/pkg00/")
        and "more]" in first
    )
    assert first.endswith("more]")
    assert c.evidence[1]["text"].endswith(", bound: none")


def test_a_long_plan_line_is_shown_as_the_sentence_with_the_limiter_word():
    body = (
        "Edit `src/job.py`. "
        + "Filler words. " * 20
        + "It skips held reports in `src/job.py`."
    )
    (c,) = run(mkplan("Only the job removes a report in `src/job.py`.", body))
    assert c.evidence[0]["text"] == "It skips held reports in `src/job.py`."


def test_no_evidence_entry_holds_a_claim_a_severity_or_the_word_defect(tmp_path):
    for repo in (None, held_repo(tmp_path, "# skip held\ndef test_a():\n    pass\n")):
        for c in basic(repo):
            for e in c.evidence:
                assert not any(w in e["text"].lower() for w in FORBIDDEN), e


def test_the_candidates_survive_the_core_checks_and_the_core_flow():
    doc = plan.parse(BASIC_TEXT)
    ctx = Ctx(doc)
    out = extractors.run_extractors(ctx, {"E1": extractors.EXTRACTORS["E1"]})
    assert len(out) == 3 and all(
        c.status == "attached" and c.evidence_computed for c in out
    )
    routes = cards.routes()
    assert {(c.cls, c.route) for c in out} == {
        ("C1", routes["C1"]),
        ("C6", routes["C6"]),
    }
    assert all(isinstance(c, Candidate) and 0 <= c.priority <= 100 for c in out)


# ---------------------------------------------------------------- determinism


def test_determinism_two_runs_give_the_same_candidates(tmp_path):
    repo = held_repo(tmp_path, "# skip held\ndef test_a():\n    pass\n")
    assert dump(basic()) == dump(basic())
    assert dump(basic(repo)) == dump(basic(repo))
    doc = plan.parse(BASIC_TEXT)
    a = extractors.run_extractors(Ctx(doc, seed=7), {"E1": extractors.EXTRACTORS["E1"]})
    b = extractors.run_extractors(Ctx(doc, seed=7), {"E1": extractors.EXTRACTORS["E1"]})
    assert dump(a) == dump(b)
