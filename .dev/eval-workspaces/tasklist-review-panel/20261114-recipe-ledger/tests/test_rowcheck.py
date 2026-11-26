"""REQ-13 to REQ-16 (the reader, the quote checks, linking, demotion and promotion of scaffold/ledgerv1.py, a Tier B
file built locally) and REQ-26, DR-5, DR-6 (the row check of rl/rowcheck.py: id grammar, recipe coverage, budgets).

This file is the acceptance test of the local ledgerv1.py (TESTING 1.3).
"""

import json
import re
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from helpers import SW

from fixtures.reports import make_rl_reports as rep
from fixtures.transcripts import make_transcripts as tr
from rl import cli, ledger_api, rowcheck
from rl import lens as lens_mod
from scaffold import fnd, ledgerv1

# the F-REPORT-RL list of TESTING section 2, spelled out here so a change of the generator cannot shrink it
F_REPORT_RL = (
    "good_ember good_luna1 none_found none_found_with_rows ledger_missing ledger_after_findings ledger_twice "
    "ledger_unclosed findings_unclosed findings_twice heading_between bad_json_line verdict_lowercase unknown_class "
    "over_budget_recipe over_budget_lens recipe_missing dup_row quote_plan_not_in_candidate quote_wraps_line "
    "quote_other_in_source quote_other_in_candidate quote_other_in_transcript quote_other_only_in_assistant_text "
    "problem_no_finding finding_linked_by_probe finding_linked_by_quote ok_but_finding unsure_with_blocking "
    "blocking_no_cb3 blocking_with_cb3 anchor_250 claim_301 promote_long_id promote_short_anchor promote_dup_id via_reask"
).split()


def case(name):
    return rep.build(name)


def read(name):
    c = case(name)
    return ledgerv1.read(c.report, c.assigned)


def corpora(c):
    return {
        "candidate": rep.plan_text(),
        "source": rep.source_text(),
        "transcript": ledgerv1.transcript_text(c.transcript) if c.transcript else None,
    }


def checked(name):
    c = case(name)
    return ledgerv1.check(ledgerv1.read(c.report, c.assigned)["rows"], corpora(c))


def test_every_report_case_builds():
    assert set(rep.CASES) == set(F_REPORT_RL) and len(rep.CASES) == len(F_REPORT_RL)
    for name in F_REPORT_RL:
        c = case(name)
        assert c.report.strip() and c.assigned
    for q in (
        rep.Q.values()
    ):  # a quote is always exact: it is a substring of its text as written
        assert q in rep.plan_text() or q in rep.source_text()
    with pytest.raises(ValueError):
        rep.cut(r"not in the plan at all", rep.plan_text())


# ---------------------------------------------------------------- REQ-13


@pytest.mark.parametrize(
    "name, reason",
    [
        ("ledger_missing", "no_block"),
        ("ledger_after_findings", "ledger_after_findings"),
        ("ledger_twice", "block_twice"),
        ("ledger_unclosed", "unclosed"),
        ("anchor_250", "no_ledger_heading"),
        ("claim_301", "no_ledger_heading"),
    ],
)
def test_misplaced_duplicated_truncated_blocks(name, reason):
    r = read(name)
    assert r["ledger_missing"] is True and r["reason"] == reason
    assert r["rows"] == [] and r["format_errors"] == 0


def test_findings_block_faults_are_not_ledger_missing():
    for name, state in (
        ("findings_unclosed", "unclosed"),
        ("findings_twice", "block_twice"),
    ):
        r = read(name)
        assert r["ledger_missing"] is False and r["block_unusable"] == state
        assert [x["item"] for x in r["rows"]] == [
            "C4.1",
            "C4.2",
            "C5.1",
            "C6.1",
            "C8.1",
        ]
    r = read("ledger_missing")  # no findings fault, only a missing ledger
    assert r["block_unusable"] is None


def test_good_reports_parse():
    for name, items in (
        ("good_ember", ["C4.1", "C4.2", "C5.1", "C6.1", "C8.1"]),
        ("good_luna1", ["C1.1", "C2.1", "C3.1"]),
        ("none_found", ["C4.1", "C5.1", "C6.1", "C8.1"]),
    ):
        r = read(name)
        assert (
            not r["ledger_missing"]
            and r["reason"] is None
            and r["block_unusable"] is None
        )
        assert [x["item"] for x in r["rows"]] == items
        assert (
            r["format_errors"] == 0 and r["dup_line"] == [] and r["unknown_item"] == []
        )
        assert r["normalised_verdict"] == 0


def test_fence_opener_grep_is_not_used():
    c = case("ledger_missing")
    # the launcher's check is a grep for the opener; it finds it in this report, the reader does not
    assert "```ledger-v1" in c.report
    assert ledgerv1.read(c.report, c.assigned)["ledger_missing"] is True
    # an example in a four-backtick fence holds a line that starts with the opener, and there is no ledger heading
    example = (
        "review: 1 of 3\n\n````text\n```ledger-v1\n"
        + rep.row("C4.1")
        + "\n```\n````\n\n"
    )
    report = example + rep.findings_part([rep.finding()]) + "\n"
    assert re.search(r"^```ledger-v1", report, re.M)
    r = ledgerv1.read(report)
    assert r["ledger_missing"] and r["reason"] == "no_ledger_heading"
    # a closed block that the parser can read is found whatever the prose around it says
    ok = rep.message(
        rep.ledger_part([rep.row("C4.1")]),
        rep.findings_part([]),
        prose="no opener here",
    )
    assert ledgerv1.read(ok)["rows"][0]["item"] == "C4.1"


def test_heading_between_ledger_and_findings_is_allowed_but_counted():
    # owner order 2026-11-15 (compliance spike): a heading between the block and the findings no longer makes the ledger missing
    r = read("heading_between")
    assert not r["ledger_missing"] and r["loose_layout"] is True and r["rows"]
    # a heading between the ledger heading and the block: same
    report = rep.message(
        "## Ledger\n\n## Notes\n\n" + rep.fence("ledger-v1", [rep.row("C4.1")]),
        rep.findings_part([]),
    )
    r = ledgerv1.read(report)
    assert not r["ledger_missing"] and r["loose_layout"] is True
    # prose without a heading stays strict-layout
    report = rep.message(
        rep.ledger_part([rep.row("C4.1")]) + "\n\nOne remark.", rep.findings_part([])
    )
    r = ledgerv1.read(report)
    assert not r["ledger_missing"] and r["loose_layout"] is False


@pytest.mark.parametrize(
    "raw, want",
    [
        ("C4.1", "C4.1"),
        ("R-C4.1", "C4.1"),
        ("C4.1:", "C4.1"),
        ("C4.1a", "C4.1"),
        ("row C4.12", "C4.12"),
        ("C4.1\n", "C4.1"),
        ("C4.1.1", "C4.1.1"),
        ("C04.1", "C04.1"),
        ("C4.", "C4."),
        ("an entirely different long label C4.1", "an entirely different long label C4.1"),
        ("X4.1", "X4.1"),
        ("", ""),
    ],
)
def test_canon_item_forgives_a_small_prefix_or_suffix(raw, want):
    assert ledgerv1.canon_item(raw) == want


def test_row_with_a_prefixed_id_is_read_as_the_canonical_id():
    report = rep.message(
        rep.ledger_part([rep.row("R-C4.1")]), rep.findings_part([])
    )
    r = ledgerv1.read(report)
    assert r["rows"][0]["item"] == "C4.1" and r["rows"][0]["item_raw"] == "R-C4.1"


def test_format_errors_are_counted_with_their_line():
    r = read("bad_json_line")
    assert r["format_errors"] == 1 and not r["ledger_missing"]
    err = r["errors"][0]
    assert "not valid JSON" in err["msg"] and err["item"] is None and err["line"] > 0
    assert [x["item"] for x in r["rows"]] == ["C4.1", "C5.1"]
    lines = [
        '["C4.1"]',
        json.dumps({"item": "C4.1"}),
        json.dumps({"item": "C4.2", "verdict": "MAYBE"}),
        json.dumps({"item": "C4.3", "verdict": "OK", "quote_plan": 7}),
        json.dumps({"item": "C4.4", "verdict": "OK", "quote_plan": None}),
    ]
    r = ledgerv1.read(rep.standard(lines))
    assert r["format_errors"] == 4
    assert [e["item"] for e in r["errors"]] == [None, "C4.1", "C4.2", "C4.3"]
    assert [x["item"] for x in r["rows"]] == ["C4.4"] and r["rows"][0][
        "quote_plan"
    ] == ""


def test_verdict_is_read_case_insensitively_and_counted():
    r = read("verdict_lowercase")
    assert [x["verdict"] for x in r["rows"]] == ["PROBLEM", "OK"]
    assert r["normalised_verdict"] == 2 and r["format_errors"] == 0


def test_dup_line_first_wins_and_unknown_item_is_kept():
    r = read("dup_row")
    assert (
        r["dup_line"] == ["C4.1"]
        and len(r["rows"]) == 1
        and r["rows"][0]["verdict"] == "PROBLEM"
    )
    r = read("unknown_class")
    assert r["unknown_item"] == ["C1.1"]
    assert [(x["item"], x["unknown_item"]) for x in r["rows"]] == [
        ("C4.1", False),
        ("C1.1", True),
    ]
    c = case("unknown_class")
    assert (
        ledgerv1.read(c.report)["unknown_item"] == []
    )  # no `assigned` means no membership check


def test_limits_are_flagged_and_the_row_is_kept():
    long_problem = "word " * 61
    ran16 = " ".join(["step"] * 16)
    rows = [
        rep.row("C4.1", "PROBLEM", rep.Q["short"], rep.Q["heading"], "ok"),
        rep.row("C4.2", "PROBLEM", "x" * 201, "", long_problem),
        rep.row("C4.3", "OK", ran=ran16),
        rep.row("C4.4", "OK", ran=" ".join(["step"] * 15)),
    ]
    got = {
        x["item"]: x["limits_violated"]
        for x in ledgerv1.read(rep.standard(rows))["rows"]
    }
    assert got == {
        "C4.1": ["quote_plan"],
        "C4.2": ["quote_plan", "problem"],
        "C4.3": ["ran"],
        "C4.4": [],
    }


# ---------------------------------------------------------------- REQ-14


def test_quote_wrapping_a_plan_line_matches():
    q = rep.Q["wrap"]
    assert "\n" in q  # the quote runs over two lines of the candidate
    (row,) = checked("quote_wraps_line")
    assert row["quote_plan"] == q and row["quote_plan_ok"] is True
    assert fnd.locate(rep.plan_text(), q)  # the same answer as the findings code
    assert row["quote_other_ok"] and row["corpus"] == "candidate" and row["supported"]
    flattened = fnd.flat(q)  # a model that copies it onto one line passes as well
    assert ledgerv1.check(
        [dict(row, quote_plan=flattened)], corpora(case("quote_wraps_line"))
    )[0]["quote_plan_ok"]


def test_quote_plan_not_in_candidate_fails():
    (row,) = checked("quote_plan_not_in_candidate")
    assert row["quote_plan_ok"] is False
    assert row["quote_other_ok"] is True and row["supported"] is False
    assert not fnd.locate(rep.plan_text(), row["quote_plan"])


def test_contains_gives_the_answer_of_locate():
    plan = rep.plan_text()
    flat_plan = fnd.flat(plan)
    quotes = (
        list(rep.Q.values())
        + [
            "  Create   `src/exporter/notice.py`.  ",
            "notice.py`. Write the\nnotice body",
            "Task 2: Update",  # the heading line "## Task 2: Update ..." has a different prefix, still a substring
            "no such text in the plan",
            "",
            "   ",
        ]
    )
    for q in quotes:
        assert ledgerv1.contains(flat_plan, q) == bool(fnd.locate(plan, q)), q


# ---------------------------------------------------------------- corpora (DR-9)


def test_transcript_text_reads_tool_results_only():
    text = ledgerv1.transcript_text(tr.build("search_done"))
    assert (
        tr.SEARCH_HIT in text
        and "I will search" not in text
        and "The search found" not in text
    )
    luna = ledgerv1.transcript_text(
        json.dumps(tr.build("luna_array_results"))
    )  # JSON text, array content
    assert tr.SEARCH_HIT in luna and "test_retention.py" in luna
    assert tr.ASSISTANT_ONLY not in ledgerv1.transcript_text(
        tr.build("assistant_text_only")
    )
    assert ledgerv1.transcript_text(tr.build("no_tool_call")) == ""
    final = tr.build(
        "no_tool_call", final=tr.SEARCH_HIT
    )  # the `result` event is assistant text too
    assert ledgerv1.transcript_text(final) == ""


def test_check_records_the_corpus_per_row():
    (src,) = checked("quote_other_in_source")
    assert (src["corpus"], src["quotes_supported"], src["search_supported"]) == (
        "source",
        True,
        False,
    )
    (cand,) = checked("quote_other_in_candidate")
    assert (cand["corpus"], cand["supported"]) == ("candidate", True)
    (found,) = checked("quote_other_in_transcript")
    assert (found["corpus"], found["quotes_supported"], found["search_supported"]) == (
        "transcript",
        True,
        True,
    )
    (said,) = checked("quote_other_only_in_assistant_text")
    assert (
        said["quote_other_ok"] is False
        and said["corpus"] is None
        and said["supported"] is False
    )
    # the same row without a transcript has nothing to match against
    c = case("quote_other_in_transcript")
    no_run = ledgerv1.check(
        ledgerv1.read(c.report)["rows"], {"candidate": rep.plan_text()}
    )[0]
    assert no_run["quote_other_ok"] is False and no_run["supported"] is False


def test_the_same_quote_twice_is_not_two_quotes():
    row = ledgerv1.read(
        rep.standard([rep.problem_row("C4.1", rep.Q["grep"], rep.Q["grep"])])
    )["rows"]
    (got,) = ledgerv1.check(row, {"candidate": rep.plan_text()})
    assert (
        got["quote_plan_ok"]
        and got["quote_other_ok"]
        and not got["quotes_supported"]
        and not got["supported"]
    )


def test_check_does_not_change_its_input():
    rows = read("good_ember")["rows"]
    before = json.dumps(rows, sort_keys=True)
    out = ledgerv1.check(rows, {"candidate": rep.plan_text()})
    assert json.dumps(rows, sort_keys=True) == before and out is not rows
    assert all("supported" in r and "supported" not in rows[0] for r in out)


# ---------------------------------------------------------------- linking, demotion and promotion (REQ-15, REQ-16)

CARDS = Path(__file__).resolve().parents[1] / "cards"
CATEGORIES = {
    c["id"]: c["promote_category"]
    for c in (json.loads(p.read_text()) for p in sorted(CARDS.glob("C[0-9].json")))
}


def run(name, scope=None, assigned=True, rows_fn=None, report=None):
    """Read, check, link and demote, promote: the order of the row check, on a report case or on a built report."""
    c = case(name)
    report = c.report if report is None else report
    rd = ledgerv1.read(report, c.assigned if assigned else None)
    rows = ledgerv1.check(rd["rows"], corpora(c))
    if rows_fn:
        rows = rows_fn(rows)
    ld = ledgerv1.link_demote(report, rows, rd["errors"], scope)
    pr = ledgerv1.promote(ld["report"], rows, ld["linked"], CATEGORIES, c.via_reask)
    return SimpleNamespace(c=c, rows=rows, ld=ld, pr=pr, report=pr["report"])


def lines_of(report):
    return [json.loads(x) for x in fnd.lenient_lines(report)]


def one_row(**kw):
    """The check of one problem row against the plan (and the given extra corpora)."""
    return ledgerv1.check(
        ledgerv1.read(rep.standard([rep.problem_row(**kw)]))["rows"],
        {"candidate": rep.plan_text()},
    )


def test_promotion_copies_problem_and_anchor():
    r = run("problem_no_finding")
    assert r.pr["promoted"] == ["PC4.1"] and r.pr["promotion_failures"] == []
    unrelated, promoted = lines_of(r.report)
    assert unrelated["id"] == "F1" and promoted["id"] == "PC4.1"
    assert promoted["claim"] == rep.PROBLEM and promoted["anchor"] == rep.Q["grep"]
    assert (promoted["severity"], promoted["blocking"], promoted["src"]) == (
        "MINOR",
        False,
        "ledger",
    )
    assert promoted["category"] == "unpassable-check" and promoted["refs"] == []
    assert (promoted["class"], promoted["probe"]) == ("C4", "C4.1")
    assert fnd.parse_block(r.report)["ok"]  # the real parser accepts the new line


def test_promotion_validates_with_check_finding():
    for name, bad in (
        ("promote_long_id", "id must match"),
        ("promote_short_anchor", "anchor must have at least 12"),
        ("promote_dup_id", "duplicate id 'PC4.1'"),
    ):
        r = run(name, assigned=False)  # the long item is outside the lens ids otherwise
        assert r.pr["promoted"] == [], name
        (fail,) = r.pr["promotion_failures"]
        assert bad in fail["reason"] and fail["item"] == r.rows[0]["item"], name
        assert r.report == r.ld["report"]  # skipped: nothing was inserted
    # the same finding object is what FND judges
    ok = run("problem_no_finding")
    assert all(fnd._check_finding(f, set()) is None for f in lines_of(ok.report)[1:])
    # a class without a card category cannot be promoted either
    bare = ledgerv1.promote(
        case("problem_no_finding").report, checked("problem_no_finding"), (), {}
    )
    assert (
        bare["promoted"] == [] and "category" in bare["promotion_failures"][0]["reason"]
    )


def test_promotion_inside_single_block(tmp_path):
    c = case("good_ember")
    raw = tmp_path / "reviews-ember.md"
    raw.write_text(c.report, encoding="utf-8")
    two = rep.standard(
        [
            rep.problem_row("C4.1"),
            rep.problem_row("C5.1", rep.Q["legal"], rep.Q["skips"]),
        ],
        [rep.finding("F1"), rep.finding("F2")],
    )
    r = run("good_ember", report=two)
    assert r.pr["promoted"] == ["PC4.1", "PC5.1"]
    blocks = fnd._blocks_after(r.report, fnd._HEAD_FINDINGS, "findings-v1")[1]
    assert len(blocks) == 1 and blocks[0][2]  # still one closed block
    assert [f["id"] for f in lines_of(r.report)] == ["F1", "F2", "PC4.1", "PC5.1"]
    assert r.report.count("```findings-v1") == 1
    assert r.report.rstrip().endswith("verdict: FAIL")  # text after the block is kept
    assert r.report.splitlines().count("```") == 2  # the two closing fences, none added
    # an empty block takes the line between its fences
    empty = ledgerv1.promote(
        rep.standard([rep.problem_row()]), checked("problem_no_finding"), (), CATEGORIES
    )
    assert [f["id"] for f in lines_of(empty["report"])] == ["PC4.1"]
    # no function edits the raw report: the file and the string are unchanged, the checked text is separate
    assert raw.read_text(encoding="utf-8") == c.report
    assert r.report != two and two.count("PC4.1") == 0


def test_promotion_failure_logged_and_skipped():
    # a block that cannot take a line: every candidate is logged and nothing is inserted
    for name in ("findings_unclosed", "findings_twice"):
        c = case(name)
        rows = checked("good_ember")[:1]
        got = ledgerv1.promote(c.report, rows, (), CATEGORIES)
        assert got["promoted"] == [] and got["report"] == c.report
        assert "unusable" in got["promotion_failures"][0]["reason"]
    # one bad line does not stop the next one
    two = rep.standard(
        [
            rep.problem_row("C4.12345678901234"),
            rep.problem_row("C5.1", rep.Q["legal"], rep.Q["skips"]),
        ]
    )
    r = run("problem_no_finding", assigned=False, report=two)
    assert [f["item"] for f in r.pr["promotion_failures"]] == ["C4.12345678901234"]
    assert r.pr["promoted"] == ["PC5.1"] and [f["id"] for f in lines_of(r.report)] == [
        "PC5.1"
    ]


def test_promotion_requires_quote_plan_ok():
    r = run("quote_plan_not_in_candidate")
    assert r.rows[0]["quote_plan_ok"] is False
    assert r.pr["promoted"] == [] and r.pr["promotion_failures"] == []
    assert r.report == case("quote_plan_not_in_candidate").report
    empty_plan = rep.standard([rep.row("C4.1", "PROBLEM", "", rep.Q["heading"], "x")])
    assert run("problem_no_finding", report=empty_plan).pr["promoted"] == []
    # verdicts other than PROBLEM are never promoted
    for verdict in ("OK", "UNSURE"):
        rows = one_row(verdict=verdict)
        assert (
            ledgerv1.promote(rep.standard([]), rows, (), CATEGORIES)["promoted"] == []
        )


def over_budget(*items):
    """What the row check of Task 9 sets on a row beyond its recipe or lens budget (DR-6)."""
    return lambda rows: [
        dict(r, over_budget="recipe") if r["item"] in items else r for r in rows
    ]


def test_no_promotion_for_over_budget_unknown_or_reask_rows():
    r = run("over_budget_recipe", rows_fn=over_budget("C4.5"))
    assert r.pr["promoted"] == [] and r.pr["promotion_failures"] == []
    assert run("problem_no_finding", rows_fn=over_budget("C4.1")).pr["promoted"] == []
    # an over-budget row cannot support a blocker either
    full = run("blocking_with_cb3", rows_fn=over_budget("C4.1"))
    assert full.ld["demoted_ids"] == {"F1": "row_unsupported"}
    u = run("unknown_class")  # C1.1 is outside the ember lens
    assert [x["item"] for x in u.rows if x["unknown_item"]] == ["C1.1"]
    assert u.pr["promoted"] == [] and u.pr["promotion_failures"] == []
    v = run("via_reask")
    assert v.rows[0]["verdict"] == "PROBLEM" and v.pr["promoted"] == []
    assert v.pr["promotion_failures"] == [] and v.report == case("via_reask").report
    # the same row of a report that was not re-asked is promoted
    ok = ledgerv1.promote(case("via_reask").report, v.rows, (), CATEGORIES)
    assert ok["promoted"] == ["PC4.1"]


def test_class_key_added_from_row_prefix():
    by_probe = run("finding_linked_by_probe")
    by_quote = run("finding_linked_by_quote")
    for r in (by_probe, by_quote):
        (f,) = lines_of(r.report)
        assert f["class"] == "C4" and r.ld["links"] == {"F1": "C4.1"}
    assert (
        lines_of(by_probe.report)[0]["probe"] == "C4.1"
    )  # the reviewer's probe is kept
    assert "probe" not in lines_of(by_quote.report)[0]  # none is invented
    assert lines_of(run("problem_no_finding").report)[1]["class"] == "C4"
    luna = run("good_luna1")
    assert [f["class"] for f in lines_of(luna.report)] == ["C2"]
    assert luna.pr["promoted"] == []  # linked by probe, so not promoted


def blocked(row_line, claim=rep.CLAIM_CB3, probe="C4.1", extra=()):
    return rep.standard(
        [row_line, *extra], [rep.finding("F1", rep.Q["ndjson"], claim, probe, True)]
    )


def test_unsupported_row_demotes_linked_finding():
    r = run(
        "quote_plan_not_in_candidate",
        report=blocked(rep.problem_row("C4.1", rep.NOT_IN_PLAN, rep.Q["heading"])),
    )
    (f,) = lines_of(r.report)
    assert f["blocking"] is False and f["severity"] == "MAJOR"  # severity is kept
    assert r.ld["demoted"] == dict.fromkeys(ledgerv1.CAUSES, 0) | {"row_unsupported": 1}
    assert r.ld["demoted_ids"] == {"F1": "row_unsupported"}
    # a supported row keeps the blocker; the by-quote link works the same way
    ok = run("blocking_with_cb3")
    assert (
        lines_of(ok.report)[0]["blocking"] is True
        and sum(ok.ld["demoted"].values()) == 0
    )
    assert lines_of(run("finding_linked_by_quote").report)[0]["blocking"] is True
    # the same quote twice is one quote: unsupported, and not a format problem
    same = run(
        "blocking_with_cb3",
        report=blocked(rep.problem_row("C4.1", rep.Q["grep"], rep.Q["grep"])),
    )
    assert same.ld["demoted_ids"] == {"F1": "row_unsupported"}
    assert same.ld["format_induced_demotions"] == 0
    # a linked row that is OK is left alone and counted; a probe nobody owns is counted and does not link
    o = run("ok_but_finding")
    assert o.ld["ok_but_finding"] == 1 and sum(o.ld["demoted"].values()) == 0
    stray = run("blocking_no_cb3", report=blocked(rep.row("C4.1"), probe="C9.9"))
    assert stray.ld["probe_unknown"] == 1 and stray.ld["links"] == {}
    assert lines_of(stray.report)[0]["blocking"] is True


def test_unsure_never_blocks():
    r = run("unsure_with_blocking")
    (f,) = lines_of(r.report)
    assert f["blocking"] is False and f["severity"] == "MAJOR"
    assert r.ld["demoted"]["row_unsure"] == 1 and sum(r.ld["demoted"].values()) == 1
    assert r.ld["format_induced_demotions"] == 0
    assert (
        r.pr["promoted"] == []
    )  # an UNSURE row is not promoted either, with or without a linked line
    assert (
        ledgerv1.promote(
            rep.standard([]), checked("unsure_with_blocking"), (), CATEGORIES
        )["promoted"]
        == []
    )
    # even a supported UNSURE row with the grading sentence cannot support a blocker
    assert checked("unsure_with_blocking")[0]["supported"] is True


def test_blocking_needs_cb3_and_two_quotes_or_search():
    no = run("blocking_no_cb3")
    assert (
        lines_of(no.report)[0]["blocking"] is False and no.ld["demoted"]["no_cb3"] == 1
    )
    assert no.ld["format_induced_demotions"] == 0
    yes = run("blocking_with_cb3")
    assert lines_of(yes.report)[0]["blocking"] is True
    # the sentence in the report text within 12 lines of a line that names the finding
    near = blocked(rep.problem_row("C4.1"), claim="The criterion cannot pass.")
    near = near.replace(
        "review: 1 of 3", f"F1: {rep.CB3} X, and X is wrong because Y.", 1
    )
    assert lines_of(run("blocking_no_cb3", report=near).report)[0]["blocking"] is True
    # the sentence about another finding, and a mention of F10 for F1, do not count
    other = near.replace("F1: ", "F10: ", 1)
    assert lines_of(run("blocking_no_cb3", report=other).report)[0]["blocking"] is False
    plain = blocked(rep.problem_row("C4.1"), claim="The criterion cannot pass.")
    for gap, want in (
        (11, True),
        (14, False),
    ):  # the window is 12 lines each side of the mention
        text = f"{rep.CB3} X.\n" + "\n" * gap + "F1 is the finding."
        far = plain.replace("review: 1 of 3", text, 1)
        assert (
            lines_of(run("blocking_no_cb3", report=far).report)[0]["blocking"] is want
        )
    # flattening and case: the claim may wrap lines and change case
    wrapped = rep.CB3.replace(" who ", "  who\n").upper() + " X"
    got = run("blocking_no_cb3", report=blocked(rep.problem_row("C4.1"), claim=wrapped))
    assert lines_of(got.report)[0]["blocking"] is True
    # two quotes, or one search result: a plan quote with a quote only a tool result holds supports a blocker
    searched = run(
        "quote_other_in_transcript",
        report=blocked(rep.problem_row("C4.1", rep.Q["legal"], tr.SEARCH_HIT)),
    )
    assert lines_of(searched.report)[0]["blocking"] is True
    # one quote (the other absent) supports nothing
    lone = run(
        "blocking_with_cb3",
        report=blocked(rep.row("C4.1", "PROBLEM", rep.Q["grep"], "", "x")),
    )
    assert lines_of(lone.report)[0]["blocking"] is False
    assert (
        lone.ld["format_induced_demotions"] == 0
    )  # a quote is missing, not mismatched


def test_unlinked_finding_untouched():
    unlinked = rep.finding(
        "F1", rep.Q["ndjson"], "The format name is not defined.", None, True
    )
    report = rep.standard([rep.problem_row("C4.1")], [unlinked])
    r = run("problem_no_finding", report=report)
    assert fnd.lenient_lines(r.report)[0] == unlinked  # the very same text
    assert (
        lines_of(r.report)[0]["blocking"] is True
        and "class" not in lines_of(r.report)[0]
    )
    assert sum(r.ld["demoted"].values()) == 0 and r.ld["links"] == {}
    # with an UNSURE row and a blocking finding about something else, only the linked one changes
    mixed = rep.standard(
        [rep.problem_row("C4.1", verdict="UNSURE")],
        [
            rep.finding("F1", rep.Q["ndjson"], rep.CLAIM_CB3, "C4.1", True),
            unlinked.replace('"F1"', '"F2"'),
        ],
    )
    got = lines_of(run("problem_no_finding", report=mixed).report)
    assert [f["blocking"] for f in got] == [False, True]


def test_quote_other_corpora():
    def blocker(quote_other, name):
        r = run(
            name, report=blocked(rep.problem_row("C4.1", rep.Q["legal"], quote_other))
        )
        return r.rows[0], lines_of(r.report)[0]["blocking"]

    found, blocking = blocker(
        tr.SEARCH_HIT, "quote_other_in_transcript"
    )  # a tool result: a search result
    assert (found["corpus"], found["search_supported"], blocking) == (
        "transcript",
        True,
        True,
    )
    said, blocking = blocker(
        tr.ASSISTANT_ONLY, "quote_other_only_in_assistant_text"
    )  # assistant text only
    assert (said["corpus"], said["supported"], blocking) == (None, False, False)
    # plan against plan: the second quote from the candidate supports the row
    plan, blocking = blocker(rep.Q["skips"], "quote_other_in_candidate")
    assert (plan["corpus"], plan["quotes_supported"], blocking) == (
        "candidate",
        True,
        True,
    )
    src, blocking = blocker(rep.Q["source_legal"], "quote_other_in_source")
    assert (src["corpus"], src["supported"], blocking) == ("source", True, True)
    # a quote of the transcript with no transcript is nothing
    none, blocking = blocker(tr.SEARCH_HIT, "quote_other_in_candidate")
    assert (none["quote_other_ok"], blocking) == (False, False)
    # an unlinked blocking finding stays blocking whatever the row says (DD-3)
    free = rep.standard(
        [rep.problem_row("C4.1", rep.NOT_IN_PLAN, rep.Q["heading"])],
        [rep.finding("F1", rep.Q["ndjson"], "No sentence.", None, True)],
    )
    assert (
        lines_of(run("problem_no_finding", report=free).report)[0]["blocking"] is True
    )


def test_check_scope_all_switch_off_by_default(monkeypatch):
    unlinked = rep.finding("F1", rep.Q["ndjson"], "No sentence here.", None, True)
    graded = rep.finding("F2", rep.Q["ndjson"], rep.CLAIM_CB3, None, True)
    report = rep.standard([rep.row("C4.1")], [unlinked, graded])
    monkeypatch.delenv("CHECK_SCOPE", raising=False)
    default = run("good_ember", report=report)
    assert [f["blocking"] for f in lines_of(default.report)] == [True, True]
    assert sum(default.ld["demoted"].values()) == 0
    everything = run("good_ember", scope="all", report=report)
    assert [f["blocking"] for f in lines_of(everything.report)] == [False, True]
    assert everything.ld["demoted"]["no_cb3"] == 1 and everything.ld["links"] == {}
    monkeypatch.setenv(
        "CHECK_SCOPE", "all"
    )  # the switch can be set in the environment too
    assert [
        f["blocking"] for f in lines_of(run("good_ember", report=report).report)
    ] == [False, True]
    assert [
        f["blocking"]
        for f in lines_of(run("good_ember", scope="linked", report=report).report)
    ] == [True, True]
    with pytest.raises(ValueError):
        ledgerv1.link_demote(report, [], scope="some")


def test_format_induced_demotions_counted():
    # a line that did not parse
    bad = rep.standard(
        [rep.problem_row("C4.1"), rep.row("C4.2")[:-1], rep.row("C5.1")],
        [rep.finding("F1", rep.Q["ndjson"], rep.CLAIM_CB3, "C4.2", True)],
    )
    r = run("bad_json_line", report=bad)
    assert r.ld["demoted"]["row_missing"] == 1 and r.ld["format_induced_demotions"] == 1
    assert lines_of(r.report)[0]["blocking"] is False
    # a quote test that failed on a row with a problem and both quotes
    q = run(
        "quote_plan_not_in_candidate",
        report=blocked(rep.problem_row("C4.1", rep.NOT_IN_PLAN, rep.Q["heading"])),
    )
    assert q.ld["format_induced_demotions"] == 1
    # content demotions are not format induced: UNSURE, no CB-3 sentence, the same quote twice
    assert run("unsure_with_blocking").ld["format_induced_demotions"] == 0
    assert run("blocking_no_cb3").ld["format_induced_demotions"] == 0
    # two findings, one of each kind: the count is per demotion
    both = rep.standard(
        [
            rep.problem_row("C4.1", rep.NOT_IN_PLAN, rep.Q["heading"]),
            rep.row("C4.2")[:-1],
        ],
        [
            rep.finding("F1", rep.Q["ndjson"], rep.CLAIM_CB3, "C4.1", True),
            rep.finding("F2", rep.Q["short"] + " in it", rep.CLAIM_CB3, "C4.2", True),
        ],
    )
    c = run("bad_json_line", report=both)
    assert (
        c.ld["demoted"]["row_unsupported"] == 1 and c.ld["demoted"]["row_missing"] == 1
    )
    assert c.ld["format_induced_demotions"] == 2


# ---------------------------------------------------------------- the row check (REQ-26, DR-5, DR-6)

VALUES = lens_mod.values()
TABLE = json.loads((SW / "config" / "lenses.json").read_text(encoding="utf-8"))
RECIPE_TEXT = {
    c: v["text"]
    for c, v in json.loads(
        (SW / "recipes" / "recipes.json").read_text(encoding="utf-8")
    )["recipes"].items()
}
B_MIN = {p: min(v.values()) for p, v in VALUES["b"].items()}
ROLE_OF_CASE = {tuple(rep.EMBER_LENS): "S", tuple(rep.LUNA_LENS): "L1"}
# the keys of check/check.json, written out from DESIGN 7.4 on purpose
CHECK_KEYS = set(
    "ledger_missing recipe_missing unknown_item over_budget format_errors normalised_verdict dup_line probe_unknown "
    "none_found none_found_with_rows rows rows_per_reviewer rows_per_recipe demoted format_induced_demotions promoted "
    "promotion_failures ok_but_finding block_unusable classes_lost reask".split()
)


def lens_of(role="S", panel="primary", has_source=True):
    return lens_mod.render(panel, has_source, B_MIN[panel], VALUES["c"])[role]


def rc(name, lens=None, report=None):
    """The row check of one report case: (ledger dict, checked text)."""
    c = case(name)
    lens = lens or lens_of(ROLE_OF_CASE[tuple(c.lens)])
    return rowcheck.check_reviewer(
        c.report if report is None else report,
        lens,
        corpora(c),
        c.via_reask,
        categories=CATEGORIES,
    )


def items(led, **flags):
    return [r["item"] for r in led["rows"] if all(r[k] == v for k, v in flags.items())]


def test_row_budget_per_recipe():
    ember = lens_of()
    assert ember["row_cap"] == 14
    assert ember["budgets"] == {"C4": 4, "C5": 4, "C6": 4, "C8": 4}
    led, _ = rc("over_budget_recipe")
    assert led["over_budget"] == [{"row": "C4.5", "reason": "recipe"}]
    # kept for counting: still a row, not unknown, and it covers its recipe
    assert items(led) == ["C4.1", "C4.2", "C4.3", "C4.4", "C4.5"]
    assert led["unknown_item"] == [] and led["recipe_missing"] == ["C5", "C6", "C8"]
    # a number above the budget is over budget; so is a fifth row of the recipe whatever its number
    rest = [rep.row(f"{c}.1") for c in ("C5", "C6", "C8")]
    above = rep.standard([rep.row("C4.1"), rep.row("C4.7"), *rest])
    assert rc("good_ember", report=above)[0]["over_budget"] == [
        {"row": "C4.7", "reason": "recipe"}
    ]
    ranked = [rep.row(f"C4.{k}") for k in (1, 2, 3, 4)] + [rep.row("C4.01")]
    led, _ = rc("good_ember", report=rep.standard([*ranked, *rest]))
    assert led["over_budget"] == [{"row": "C4.01", "reason": "recipe"}]
    # the budget is the recipe's own: C2 allows six rows, the seventh is over budget
    luna = lens_of("L1")
    assert luna["budgets"]["C2"] == 6
    seven = [rep.row(f"C2.{k}") for k in range(1, 8)]
    led, _ = rc(
        "good_luna1", report=rep.standard([*seven, rep.row("C1.1"), rep.row("C3.1")])
    )
    assert led["over_budget"] == [{"row": "C2.7", "reason": "recipe"}]


def test_lens_cap_enforced():
    led, _ = rc("over_budget_lens")
    assert len(led["rows"]) == 15 and led["row_cap"] == 14
    assert led["over_budget"] == [{"row": "C8.3", "reason": "lens"}]
    assert items(led, over_budget="lens") == ["C8.3"] and led["recipe_missing"] == []
    # the cap comes from the lens file: a smaller cap flags the rows after it, in the order written
    led, _ = rc("good_ember", lens=dict(lens_of(), row_cap=3))
    assert led["over_budget"] == [
        {"row": "C6.1", "reason": "lens"},
        {"row": "C8.1", "reason": "lens"},
    ]
    assert rc("good_ember", lens=dict(lens_of(), row_cap=5))[0]["over_budget"] == []
    # a row over its recipe's budget does not use up the lens cap
    rows = [rep.row(f"{c}.{k}") for c in ("C4", "C5", "C6") for k in range(1, 5)]
    rows += [rep.row("C4.5"), rep.row("C8.1"), rep.row("C8.2")]
    led, _ = rc("good_ember", report=rep.standard(rows))
    assert led["over_budget"] == [{"row": "C4.5", "reason": "recipe"}]


def test_none_found_allowed_and_covers_recipe():
    led, _ = rc("none_found")
    assert led["ledger_missing"] is False and led["recipe_missing"] == []
    assert len(led["rows"]) == 4 and all(r["none_found"] for r in led["rows"])
    assert led["over_budget"] == [] and led["none_found_with_rows"] == []
    # a lone row, in any case, covers its recipe
    only = [rep.row("C4.1", ran="None found: grep of the tests")]
    only += [rep.row(f"{c}.1") for c in ("C5", "C6", "C8")]
    led, _ = rc("good_ember", report=rep.standard(only))
    assert led["recipe_missing"] == [] and items(led, none_found=True) == ["C4.1"]
    # it needs verdict OK, no plan quote and the words in `ran`
    nope = [
        rep.row("C4.1", "PROBLEM", rep.Q["grep"], rep.Q["heading"], "x", "NONE FOUND"),
        rep.row("C5.1", "OK", rep.Q["grep"], "", "", "NONE FOUND: searched"),
        rep.row("C6.1", "UNSURE", "", "", "", "NONE FOUND"),
        rep.row("C8.1", ran="found nothing"),
    ]
    led, _ = rc("good_ember", report=rep.standard(nope))
    assert items(led, none_found=True) == [] and led["recipe_missing"] == []


def test_none_found_with_rows_flagged():
    led, _ = rc("none_found_with_rows")
    assert led["none_found_with_rows"] == ["C4"] and led["recipe_missing"] == []
    assert items(led, none_found=True) == ["C4.1", "C5.1", "C6.1", "C8.1"]
    assert (
        rc("good_ember")[0]["none_found_with_rows"] == []
    )  # only the shared recipe is flagged


def test_recipe_missing_flagged():
    led, _ = rc("recipe_missing")
    assert led["recipe_missing"] == ["C8"] and led["ledger_missing"] is False
    assert rc("good_ember")[0]["recipe_missing"] == []
    luna = rep.standard([rep.row("C1.1"), rep.row("C3.1")])
    assert rc("good_luna1", report=luna)[0]["recipe_missing"] == ["C2"]
    # an unknown row covers nothing: C1.1 is outside the ember lens
    wrong = rep.standard([rep.row(i) for i in ("C1.1", "C5.1", "C6.1", "C8.1")])
    assert rc("good_ember", report=wrong)[0]["recipe_missing"] == ["C4"]
    # a report with no ledger is `ledger_missing` once, and it is passed on as written
    led, text = rc("ledger_missing")
    assert led["ledger_missing"] and led["recipe_missing"] == [] and led["rows"] == []
    assert text == case("ledger_missing").report


def test_row_id_grammar_and_lens_membership():
    # "C4.1\n" and "R-C4.1" are no longer here: a small prefix or suffix is forgiven (owner order 2026-11-15, see canon_item)
    bad = ["C1.1", "C4x", "4.1", "C4.", "c4.1", "C04.1", "C4.1.1", "C4.-1"]
    rows = [rep.row("C4.1"), *[rep.row(b) for b in bad]]
    led, _ = rc("good_ember", report=rep.standard(rows))
    assert items(led, unknown_item=False) == ["C4.1"]
    assert led["unknown_item"] == bad and items(led, unknown_item=True) == bad
    assert led["over_budget"] == []  # an unknown row has no budget
    # C4.1 is accepted for a lens with C4 and unknown for a lens without it
    one = rep.standard([rep.row("C4.1")])
    assert rc("good_ember", report=one)[0]["unknown_item"] == []
    led, _ = rc("good_luna1", report=one)
    assert led["unknown_item"] == ["C4.1"]
    assert led["recipe_missing"] == ["C1", "C2", "C3"]
    # an unknown row is never linked or promoted
    probe = rep.finding("F1", rep.Q["ndjson"], rep.CLAIM_CB3, "C4x", True)
    led, text = rc("good_ember", report=rep.standard([rep.problem_row("C4x")], [probe]))
    assert led["promoted"] == [] and led["links"] == {} and led["probe_unknown"] == 1
    assert lines_of(text)[0]["blocking"] is True


def test_assigned_ids_per_lens():
    budget = {
        c: int(re.search(r"Write at most (\d+) rows\.", t).group(1))
        for c, t in RECIPE_TEXT.items()
    }
    assert set(budget) == {f"C{n}" for n in range(1, 9)}
    for has_source in (True, False):
        for panel, spec in TABLE["panels"].items():
            roles = lens_mod.render(panel, has_source, B_MIN[panel], VALUES["c"])
            for role, r in roles.items():
                want = [
                    c for c in spec["roles"][role]["lens"] if has_source or c != "C2"
                ]
                ids = [f"{c}.{k}" for c in want for k in range(1, budget[c] + 1)]
                assert r["recipes"] == want and r["assigned_ids"] == ids
                # every assigned id is accepted by the row check; the next number of a recipe is over budget
                rows = [rep.row(i) for i in ids] + [
                    rep.row(f"{want[0]}.{budget[want[0]] + 1}")
                ]
                led, _ = rowcheck.check_reviewer(
                    rep.standard(rows), r, {"candidate": rep.plan_text()}
                )
                assert led["unknown_item"] == [] and led["recipe_missing"] == []
                recipe = [o for o in led["over_budget"] if o["reason"] == "recipe"]
                assert [o["row"] for o in recipe] == [rows_last(rows)]
                assert all(
                    o["reason"] == "lens" for o in led["over_budget"] if o not in recipe
                )


def rows_last(rows):
    return json.loads(rows[-1])["item"]


def test_over_budget_rows_not_promotable():
    led, text = rc("over_budget_recipe")
    last = led["rows"][-1]
    assert (last["item"], last["verdict"], last["over_budget"]) == (
        "C4.5",
        "PROBLEM",
        "recipe",
    )
    assert last["quote_plan_ok"] is True  # it would be promotable but for the budget
    assert led["promoted"] == [] and led["promotion_failures"] == []
    assert text == case("over_budget_recipe").report
    assert rc("problem_no_finding")[0]["promoted"] == [
        "PC4.1"
    ]  # inside its budget the same row is promoted
    led, text = rc("over_budget_lens")
    assert (led["rows"][-1]["verdict"], led["rows"][-1]["over_budget"]) == (
        "PROBLEM",
        "lens",
    )
    assert led["promoted"] == [] and text == case("over_budget_lens").report
    # an over-budget row cannot support a blocker either (DR-6)
    first = [rep.row(f"{c}.{k}") for c in ("C4", "C5", "C6") for k in range(1, 5)]
    for rows, probe in (
        ([*first, rep.row("C8.1"), rep.row("C8.2"), rep.problem_row("C8.3")], "C8.3"),
        ([rep.row("C4.1"), rep.problem_row("C4.5")], "C4.5"),
    ):
        blocker = rep.finding("F1", rep.Q["ndjson"], rep.CLAIM_CB3, probe, True)
        led, text = rc("good_ember", report=rep.standard(rows, [blocker]))
        assert led["demoted_ids"] == {"F1": "row_unsupported"}, probe
        assert lines_of(text)[0]["blocking"] is False and led["promoted"] == []


# ---------------------------------------------------------------- the check of a run folder


def make_run(tmp_path, reports):
    """A run folder: lens files of the primary panel, and {role: (report, transcript events or None)} as reviews."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    run = tmp_path / "run"
    for role, r in lens_mod.render(
        "primary", True, B_MIN["primary"], VALUES["c"]
    ).items():
        (run / "lens").mkdir(parents=True, exist_ok=True)
        (run / "lens" / f"{r['rid']}.json").write_text(json.dumps(r), encoding="utf-8")
        if role in reports:
            text, events = reports[role]
            (run / "reviews").mkdir(exist_ok=True)
            (run / "reviews" / f"{r['rid']}.md").write_text(text, encoding="utf-8")
            if events is not None:
                (run / "reviews" / f"{r['rid']}.attempt1.json").write_text(
                    json.dumps(events), encoding="utf-8"
                )
    cand, src = tmp_path / "candidate.md", tmp_path / "source.md"
    cand.write_text(rep.plan_text(), encoding="utf-8")
    src.write_text(rep.source_text(), encoding="utf-8")
    return run, cand, src


def three_reports():
    ember, luna1 = case("good_ember"), case("good_luna1")
    luna2 = rep.standard([rep.row("C2.1"), rep.row("C4.1"), rep.row("C7.1")])
    return {
        "S": (ember.report, ember.transcript),
        "L1": (luna1.report, luna1.transcript),
        "L2": (luna2, tr.build("luna_array_results", luna2)),
    }


def test_check_under_one_second_on_three_reports(tmp_path):
    run, cand, src = make_run(tmp_path, three_reports())
    raw = {p.name: p.read_bytes() for p in (run / "reviews").glob("*.md")}
    start = time.perf_counter()
    result = rowcheck.check_run(run, cand, src)
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, elapsed
    assert set(result) == CHECK_KEYS and result["rows_per_reviewer"] == {
        "t2b-1": 5,
        "t4-1": 3,
        "t3-1": 3,
    }
    assert result["rows"] == {"OK": 9, "PROBLEM": 2, "UNSURE": 0}
    assert (
        result["ledger_missing"] == []
        and result["classes_lost"] == {}
        and result["reask"] == {}
    )
    assert result["promoted"] == 0 and result["over_budget"] == {
        "t2b-1": 0,
        "t4-1": 0,
        "t3-1": 0,
    }
    out = run / "check"
    assert sorted(p.name for p in out.iterdir()) == sorted(
        ["check.json"]
        + [f"{r}.{k}" for r in raw_rids(raw) for k in ("ledger.json", "checked.md")]
    )
    assert json.loads((out / "check.json").read_text(encoding="utf-8")) == result
    led = json.loads((out / "t2b-1.ledger.json").read_text(encoding="utf-8"))
    assert [r["item"] for r in led["rows"]] == [
        "C4.1",
        "C4.2",
        "C5.1",
        "C6.1",
        "C8.1",
    ] and led["rows"][0]["supported"]
    # the raw reports are never edited
    assert {p.name: p.read_bytes() for p in (run / "reviews").glob("*.md")} == raw


def raw_rids(raw):
    return [name.removesuffix(".md") for name in sorted(raw)]


def test_check_run_writes_checked_text_and_skips_reask_rows(tmp_path):
    ember = case("problem_no_finding")
    run, cand, src = make_run(tmp_path, {"S": (ember.report, None)})
    result = rowcheck.check_run(run, cand, src)
    checked = (run / "check" / "t2b-1.checked.md").read_text(encoding="utf-8")
    assert (
        result["promoted"] == 1 and "PC4.1" in checked and "PC4.1" not in ember.report
    )
    # no report: dropped; C4 stays held by the one reviewer left, nothing else does
    assert result["classes_lost"] == {"t4-1": ["C1", "C2", "C3"], "t3-1": ["C2", "C7"]}
    assert (run / "reviews" / "t2b-1.md").read_text(encoding="utf-8") == ember.report
    again = rowcheck.check_run(run, cand, src, via_reask=("t2b-1",))
    assert again["promoted"] == 0
    assert (run / "check" / "t2b-1.checked.md").read_text(
        encoding="utf-8"
    ) == ember.report
    led = json.loads((run / "check" / "t2b-1.ledger.json").read_text(encoding="utf-8"))
    assert led["via_reask"] is True


def test_check_run_lists_classes_lost_of_dropped_reviewers(tmp_path):
    run, cand, src = make_run(tmp_path, three_reports())
    (run / "reviews" / "t4-1.meta.json").write_text(
        json.dumps({"killed": True}), encoding="utf-8"
    )
    result = rowcheck.check_run(run, cand, src)
    assert result["classes_lost"] == {
        "t4-1": ["C1", "C3"]
    }  # C2 is also in the lens of t3-1
    assert not (run / "check" / "t4-1.ledger.json").exists()
    assert sorted(result["rows_per_reviewer"]) == ["t2b-1", "t3-1"]
    (run / "reviews" / "t4-1.meta.json").write_text(
        json.dumps({"model_ok": False}), encoding="utf-8"
    )
    assert rowcheck.check_run(run, cand, src)["classes_lost"] == {"t4-1": ["C1", "C3"]}
    (run / "reviews" / "t4-1.meta.json").write_text(
        json.dumps({"killed": False}), encoding="utf-8"
    )
    assert rowcheck.check_run(run, cand, src)["classes_lost"] == {}
    # the aggregate counts: a missing ledger and an unknown row are reported per reviewer
    broken = {"S": (case("ledger_missing").report, None), "L1": (read_unknown(), None)}
    run2, cand2, src2 = make_run(tmp_path / "two", broken)
    result = rowcheck.check_run(run2, cand2, src2)
    assert result["ledger_missing"] == ["t2b-1"] and result["unknown_item"] == 1


def read_unknown():
    return rep.standard(
        [rep.row("C1.1"), rep.row("C4.1"), rep.row("C2.1"), rep.row("C3.1")]
    )


def test_check_raises_on_error_and_on_the_forced_exception(
    tmp_path, monkeypatch, capsys
):
    run, cand, src = make_run(tmp_path, three_reports())
    monkeypatch.setenv("RL_FORCE_EXC", "check")
    with pytest.raises(RuntimeError, match="RL_FORCE_EXC=check"):
        rowcheck.check_run(run, cand, src)
    argv = ["check", "--run", str(run), "--candidate", str(cand), "--source", str(src)]
    assert cli.main(argv) == 1 and "RL_FORCE_EXC=check" in capsys.readouterr().err
    assert not (run / "check").exists()  # nothing is written when the check raises
    monkeypatch.delenv("RL_FORCE_EXC")
    with pytest.raises(FileNotFoundError):
        rowcheck.check_run(run, tmp_path / "no-candidate.md", src)
    with pytest.raises(ValueError, match="no lens files"):
        rowcheck.check_run(tmp_path / "empty", cand, src)
    assert (
        cli.main(["check", "--run", str(tmp_path / "empty"), "--candidate", str(cand)])
        == 1
    )
    assert not (run / "check").exists() and not (tmp_path / "empty" / "check").exists()
    assert cli.main(["check", "--run", str(run)]) == 2  # a usage error
    assert cli.main(argv) == 0 and (run / "check" / "check.json").is_file()


def test_ledger_api_is_one_small_adapter():
    path = Path(ledger_api.__file__)
    assert len(path.read_text(encoding="utf-8").splitlines()) <= 40
    assert {n for n in dir(ledger_api) if not n.startswith("_")} >= {
        "read",
        "check",
        "link_demote",
        "promote",
    }
    c = case("good_ember")
    rd = ledger_api.read(c.report, None)
    assert rd == ledgerv1.read(c.report, None) and not rd["ledger_missing"]


# ---------------------------------------------------------------- owner-approved small allowances (2026-11-15)


def _std():
    return rep.message(rep.ledger_part([rep.row("C4.1")]), rep.findings_part([]))


def test_strict_report_forgives_nothing():
    r = ledgerv1.read(_std())
    assert not r["ledger_missing"] and r["forgiven"] == []


@pytest.mark.parametrize(
    "old, new, kind",
    [
        ("## Ledger", "Ledger:", "heading_style"),
        ("## Ledger", "### Ledger:", "heading_style"),
        ("```ledger-v1", "```Ledger-V1", "fence_label"),
        ("```ledger-v1", "``` ledger-v1", "fence_label"),
    ],
)
def test_small_heading_and_fence_slips_are_forgiven_and_recorded(old, new, kind):
    text = _std()
    assert old in text
    r = ledgerv1.read(text.replace(old, new, 1))
    assert not r["ledger_missing"] and kind in r["forgiven"], r
    assert [x["item"] for x in r["rows"]] == ["C4.1"]


def test_trailing_comma_on_a_json_line_is_forgiven_and_recorded():
    text = _std()
    line = next(ln for ln in text.splitlines() if ln.startswith('{"item"'))
    r = ledgerv1.read(text.replace(line, line + ",  ", 1))
    assert not r["ledger_missing"] and "json_line_slack" in r["forgiven"]
    assert [x["item"] for x in r["rows"]] == ["C4.1"] and r["format_errors"] == 0


def test_allowances_never_forgive_a_missing_or_misplaced_ledger():
    text = _std()
    # no ledger heading at all, no block, block after the findings, an unrelated fence label
    assert ledgerv1.read(text.replace("## Ledger", "## Notes", 1))["ledger_missing"]
    assert ledgerv1.read(text.replace("```ledger-v1", "```ledger-v2", 1))["ledger_missing"]
    assert read("ledger_after_findings")["ledger_missing"]
    assert read("ledger_unclosed")["ledger_missing"]
