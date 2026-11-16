"""ledger-v1 reader, the four checks, linking and demotion (REQ-13, REQ-14, REQ-16, DD-2, DD-3; DESIGN 9.1 to 9.3).

Every report under fixtures/reports and the plan and source under fixtures/plans are invented. The reports quote
fixtures/plans/p_basic.md (the candidate) and fixtures/plans/source.md (the source); good.attempt1.json is the
transcript of the reviewer behind good.md.
"""

import json
import re

import pytest
from helpers import SW

from scaffold import cards, fnd, ledgerv1

REPORTS = SW / "fixtures" / "reports"
PLANS = SW / "fixtures" / "plans"
CAND = (PLANS / "p_basic.md").read_text()
SRC = (PLANS / "source.md").read_text()
ASSIGNED = ["S1", "S2", "S3"]
PRINTED = "pattern 'retention-window' against 'Retention window': NO MATCH"
ITEMS = [
    {"item_id": "S1", "evidence": []},
    {
        "item_id": "S2",
        "evidence": [{"path": "plan", "line": 50, "text": PRINTED}],
    },
    {"item_id": "S3", "evidence": []},
]
TRANSCRIPT = ledgerv1.read_transcript(REPORTS / "good.attempt1.json")
QO_TRANSCRIPT = "docs/guide.md:14: The exporter writes 3 report formats to disk."


def load(name):
    return (REPORTS / f"{name}.md").read_text()


def run(report, **kw):
    kw.setdefault("transcript", TRANSCRIPT)
    return ledgerv1.check_report(
        report, assigned=ASSIGNED, candidate=CAND, source=SRC, items=ITEMS, **kw
    )


def blocking(text):
    """{finding id: blocking flag} of the findings block of text, which must parse with the real parser."""
    parsed = fnd.parse_block(text)
    assert parsed["ok"], parsed["errors"]
    return {f["id"]: f["blocking"] for f in parsed["findings"]}


def by_id(res):
    return {f["id"]: f for f in res["findings"]}


def test_misplaced_duplicated_truncated_blocks():
    good = run(load("good"))
    assert not good["ledger"]["ledger_missing"] and good["ledger"]["reason"] is None
    assert [r["item"] for r in good["ledger"]["rows"]] == ASSIGNED
    assert good["ledger"]["format_errors"] == [] and good["block_unusable"] is None

    # every ledger problem of DESIGN 9.1 items 1 and 2 is `ledger_missing`: no rows, nothing demoted
    for name, reason in {
        "ledger_missing": "ledger_heading_missing",
        "ledger_after_findings": "ledger_after_findings",
        "ledger_twice": "two_blocks",
        "ledger_unclosed": "unclosed",
    }.items():
        report = load(name)
        res = run(report)
        led = res["ledger"]
        assert led["ledger_missing"] and led["reason"] == reason, name
        assert led["rows"] == [] and led["missing_line"] == ASSIGNED, name
        assert res["text"] == report and res["demoted_findings"] == 0, name

    # a heading between the ledger heading and the findings heading ("directly above", REQ-13)
    between = load("good").replace(
        "## Findings block", "## Notes\n\nmore text\n\n## Findings block"
    )
    assert ledgerv1.read_ledger(between, ASSIGNED)["reason"] == "heading_between"
    # no findings heading at all: there is no span to look in
    no_head = load("good").replace("## Findings block", "Findings")
    assert (
        ledgerv1.read_ledger(no_head, ASSIGNED)["reason"] == "findings_heading_missing"
    )
    # a stray second block placed before the heading counts as two blocks
    stray = "```ledger-v1\n" + '{"item":"S1","verdict":"OK"}\n```\n\n' + load("good")
    assert ledgerv1.read_ledger(stray, ASSIGNED)["reason"] == "two_blocks"

    # a truncated or doubled findings block: the check changes nothing and names the reason (DESIGN 9.3)
    for name, reason in {
        "findings_unclosed": "findings_block_unclosed",
        "findings_twice": "findings_block_duplicated",
    }.items():
        report = load(name)
        res = run(report)
        assert res["block_unusable"] == reason, name
        assert res["text"] == report and res["findings"] == [], name
        assert [r["item"] for r in res["ledger"]["rows"]] == ["S1"], (
            name
        )  # the ledger is still read


def test_fence_opener_grep_is_not_used():
    """RR greps for a line that starts with the fence opener; the reader scans fences, so an opener inside a longer fence is not a block."""
    ledger_example = (
        "An example of the format, shown in a longer fence:\n\n"
        "````text\n```ledger-v1\n"
        '{"item":"S1","verdict":"OK","quote_plan":"","quote_other":"","problem":"","ran":"x"}\n'
        "```\n````\n\n"
    )
    report = load("good").replace("## Ledger", ledger_example + "## Ledger", 1)
    grep_count = len(re.findall(r"^```ledger-v1", report, re.M))
    assert grep_count == 2  # what a grep would count
    led = run(report)["ledger"]
    assert not led["ledger_missing"] and len(led["rows"]) == 3

    # the findings opener exists only inside a longer fence: a grep is satisfied, the block is not there
    only_example = (
        "review: 1 of 3\n\n## Ledger\n\n```ledger-v1\n"
        '{"item":"S1","verdict":"OK"}\n```\n\n## Findings block\n\n'
        "````text\n```findings-v1\n"
        '{"id":"F1"}\n```\n````\n\nverdict: FAIL\n'
    )
    assert re.search(r"^```findings-v1", only_example, re.M)
    assert run(only_example)["block_unusable"] == "no_findings_block"


def test_quote_wrapping_a_plan_line_matches():
    res = run(load("quote_wraps_line"))
    rows = {r["item"]: r for r in res["ledger"]["rows"]}
    # S1: the quote has a line break in the middle of a single plan line
    assert "\n" in rows["S1"]["quote_plan"]
    assert fnd.locate(CAND, rows["S1"]["quote_plan"])
    assert rows["S1"]["quote_plan_ok"] and rows["S1"]["supported"]
    # S2: the quote runs over two plan lines that a blank line separates
    assert "\n" not in rows["S2"]["quote_plan"] and fnd.locate(
        CAND, "Source sections: 2.1\nAcceptance criteria:"
    )
    assert rows["S2"]["quote_plan_ok"] and rows["S2"]["supported"]
    # F2 has no probe; its wrapped anchor contains the flattened quote_plan of S2, so it links by quote
    f = by_id(res)
    assert (f["F2"]["link"], f["F2"]["row_item"]) == ("quote", "S2")
    assert (f["F1"]["link"], f["F1"]["row_item"]) == ("probe", "S1")
    assert res["demoted_findings"] == 0 and res["text"] == load("quote_wraps_line")


def test_unsupported_row_demotes_linked_finding():
    report = load("good")
    bogus = report.replace(QO_TRANSCRIPT, "docs/guide.md:99: a line nobody printed")
    assert bogus != report
    res = run(bogus)
    row = {r["item"]: r for r in res["ledger"]["rows"]}["S3"]
    assert row["quote_plan_ok"] and not row["quote_other_ok"] and not row["supported"]
    assert row["corpus"] is None
    assert by_id(res)["F3"]["demoted"] and by_id(res)["F3"]["causes"] == [
        "row_unsupported"
    ]
    assert res["demoted"] == {
        "row_unsupported": 1,
        "row_unsure": 0,
        "no_cb3": 0,
        "row_missing": 0,
    }
    # a quote test failed on a row that has a problem and both quotes: format-induced
    assert res["format_induced_demotions"] == 1
    assert blocking(res["text"]) == {"F1": True, "F2": True, "F3": False}
    # severity stays, the line is valid, and the raw text we passed in was not edited
    f3 = next(f for f in fnd.parse_block(res["text"])["findings"] if f["id"] == "F3")
    assert f3["severity"] == "CRITICAL" and f3["probe"] == "S3"
    assert res["text"] != bogus and '"blocking": true' in bogus.split('"id": "F3"')[-1]

    # a row that fails to parse: a finding that names it is demoted with row_missing; the error has its line number
    broken = load("bad_json_line")
    res = run(broken)
    lineno = next(
        i
        for i, ln in enumerate(broken.splitlines(), 1)
        if ln.startswith('{"item": "S2"')
    )
    assert [e["line"] for e in res["ledger"]["format_errors"]] == [lineno]
    assert (
        res["ledger"]["broken_items"] == ["S2"] and res["ledger"]["missing_line"] == []
    )
    assert (
        by_id(res)["F2"]["causes"] == ["row_missing"]
        and by_id(res)["F2"]["format_induced"]
    )
    assert res["demoted"]["row_missing"] == 1 and res["format_induced_demotions"] == 1
    assert blocking(res["text"]) == {"F1": True, "F2": False, "F3": True}


def test_unsure_never_blocks():
    report = load("unsure_with_blocking")
    res = run(report)
    f = by_id(res)["F1"]
    assert f["blocking"] and f["demoted"]
    # the finding carries the CB-3 sentence and the row has two supported quotes, yet an UNSURE row never blocks
    assert ledgerv1.carries_cb3(
        next(x for x in fnd.parse_block(report)["findings"] if x["id"] == "F1"), []
    )
    assert f["causes"] == ["row_unsure"] and not f["format_induced"]
    assert res["demoted"]["row_unsure"] == 1 and res["format_induced_demotions"] == 0
    assert blocking(res["text"]) == {"F1": False}


def test_blocking_needs_cb3_and_two_quotes_or_search():
    # CB-3 in the claim, two different supported quotes (good: F1 via the source, F3 via a tool result)
    res = run(load("good"))
    assert (
        blocking(res["text"])["F1"]
        and blocking(res["text"])["F3"]
        and res["demoted_findings"] == 0
    )
    rows = {r["item"]: r for r in res["ledger"]["rows"]}
    assert rows["S1"]["corpus"] == "source" and rows["S1"]["quotes_supported"]
    assert rows["S3"]["corpus"] == "transcript" and rows["S3"]["search_supported"]
    assert rows["S3"]["supported"]

    # supported row, no CB-3 sentence anywhere: demoted by no_cb3 alone
    res = run(load("blocking_no_cb3"))
    assert (
        by_id(res)["F1"]["causes"] == ["no_cb3"]
        and not by_id(res)["F1"]["format_induced"]
    )
    assert blocking(res["text"]) == {"F1": False}

    # the sentence in the report text within 12 lines of a line that names the id carries F1; F2 is 16 lines away
    res = run(load("blocking_with_cb3_near_id"))
    assert by_id(res)["F1"]["causes"] == [] and by_id(res)["F2"]["causes"] == ["no_cb3"]
    assert blocking(res["text"]) == {"F1": True, "F2": False}

    # two quotes that are the same text are one quote: not supported, even though the transcript holds that text
    twin = load("good").replace(
        QO_TRANSCRIPT, "No remaining `3 report formats` text exists in `docs/guide.md`."
    )
    events = TRANSCRIPT + [
        "The criteria list says: No remaining `3 report formats` text exists in `docs/guide.md`."
    ]
    res = run(twin, transcript=events)
    row = {r["item"]: r for r in res["ledger"]["rows"]}["S3"]
    assert (
        row["corpus"] == "candidate"
        and not row["quotes_supported"]
        and not row["supported"]
    )
    assert by_id(res)["F3"]["causes"] == ["row_unsupported"]
    assert not by_id(res)["F3"][
        "format_induced"
    ]  # a content failure, not a quote-match failure

    # the CB-3 test is flattened and case-insensitive; the id is matched as a whole word
    f1 = {
        "id": "F1",
        "claim": "an  IMPLEMENTER who follows the stated\ntext as written BUILDS a thing",
    }
    assert ledgerv1.carries_cb3(f1, [])
    sentence = ledgerv1.CB3_SENTENCE
    assert not ledgerv1.carries_cb3(
        {"id": "F1", "claim": "x"}, ["Notes on F10", sentence]
    )
    assert ledgerv1.carries_cb3({"id": "F1", "claim": "x"}, ["See F1.", sentence])
    assert not ledgerv1.carries_cb3({"id": "F1", "claim": "x"}, ["See F1.2", sentence])
    wrapped = [
        "F1 is the problem.",
        "An implementer who follows the stated",
        "text as written builds a thing",
    ]
    assert ledgerv1.carries_cb3({"id": "F1", "claim": "x"}, wrapped)


def test_unlinked_finding_untouched():
    report = load("good")
    res = run(report)
    f2 = by_id(res)["F2"]
    assert f2["link"] is None and f2["row_item"] is None
    # F2 is blocking, has no CB-3 sentence and no row: in the default scope it is exactly as written (DD-3)
    assert f2["blocking"] and not f2["demoted"]
    assert res["scope"] == "linked" and res["text"] == report
    assert blocking(res["text"])["F2"] is True

    # a probe that names an item this reviewer does not have is probe_unknown and does not link
    unknown = report.replace(
        '"claim": "No task checks the network rule."}',
        '"claim": "No task checks the network rule.", "probe": "S7"}',
    )
    assert unknown != report
    res = run(unknown)
    assert res["probe_unknown"] == 1 and by_id(res)["F2"]["link"] is None
    assert res["text"] == unknown and blocking(res["text"])["F2"] is True

    # an item with no ledger line has no row to link to; the probe finds nothing
    no_s3 = report.replace('{"item": "S3"', '{"item": "S9"')
    res = run(no_s3)
    assert res["ledger"]["missing_line"] == ["S3"] and res["ledger"]["unknown_item"]
    assert by_id(res)["F3"]["link"] is None and blocking(res["text"])["F3"] is True


def test_check_scope_all_switch_off_by_default(monkeypatch):
    report = load("good")
    monkeypatch.delenv("CHECK_SCOPE", raising=False)
    assert ledgerv1.scope_from() == "linked"
    assert run(report)["demoted_findings"] == 0

    monkeypatch.setenv("CHECK_SCOPE", "")
    assert ledgerv1.scope_from() == "linked"

    # the same report under `all`: the unlinked blocking F2 has no CB-3 sentence and no second quote
    monkeypatch.setenv("CHECK_SCOPE", "all")
    res = run(report)
    assert res["scope"] == "all"
    assert by_id(res)["F2"]["demoted"]
    assert by_id(res)["F2"]["causes"] == ["row_unsupported", "no_cb3"]
    assert blocking(res["text"]) == {"F1": True, "F2": False, "F3": True}
    # the argument beats the environment variable, and a wrong value is refused
    assert run(report, scope="linked")["demoted_findings"] == 0
    monkeypatch.setenv("CHECK_SCOPE", "everything")
    with pytest.raises(ValueError):
        run(report)
    monkeypatch.delenv("CHECK_SCOPE")
    with pytest.raises(ValueError):
        run(report, scope="none")


def test_quote_other_corpora():
    """DD-2: source, candidate, sheet, transcript; the first match is recorded, and a quote in none of them fails."""
    corpora = ledgerv1.Corpora(CAND, SRC, ITEMS, TRANSCRIPT)
    assert (
        corpora.find("The job must write `deleted_count` to the run log", "S1")
        == "source"
    )
    assert (
        corpora.find("The retention job gets its age limit from one setting.", "S1")
        == "candidate"
    )
    assert corpora.find(PRINTED, "S2") == "sheet"
    assert (
        corpora.find(f"plan line 50: {PRINTED}", "S2") == "sheet"
    )  # the printed form of the tool line
    assert (
        corpora.find(PRINTED, "S1") is None
    )  # another item's tool line is not this item's
    assert corpora.find(PRINTED) == "sheet"  # no item given: every item's tool lines
    assert corpora.find(QO_TRANSCRIPT, "S3") == "transcript"
    assert (
        corpora.find("docs/guide.md:14:   The exporter writes\n3 report formats", "S3")
        == "transcript"
    )
    assert corpora.find("a sentence that no corpus has ever held", "S1") is None
    assert corpora.find("", "S1") is None

    # a plan-versus-plan row whose second quote is from the candidate passes (DD-2)
    base = {
        "item": "S2",
        "verdict": "PROBLEM",
        "quote_plan": "Every module under `src/exporter/` returns an empty result for an empty report.",
        "quote_other": "The exporter package has no network access.",
        "problem": "p",
        "ran": "r",
    }
    row = ledgerv1.check_row(base, corpora)
    assert row["corpus"] == "candidate" and row["quote_other_ok"] and row["supported"]
    # a plan-versus-tool-line row: a search result, and one search result is enough
    row = ledgerv1.check_row({**base, "quote_other": PRINTED}, corpora)
    assert row["corpus"] == "sheet" and row["search_supported"] and row["supported"]
    # a quote in none of the four corpora fails check 3 and so check 4
    row = ledgerv1.check_row(
        {**base, "quote_other": "nobody printed this sentence"}, corpora
    )
    assert row["corpus"] is None and not row["quote_other_ok"] and not row["supported"]
    # a plan quote that is not in the candidate fails check 2 and so check 4
    row = ledgerv1.check_row(
        {**base, "quote_plan": "this is not in the plan text"}, corpora
    )
    assert not row["quote_plan_ok"] and not row["supported"]
    # an empty quote_other is no quote
    row = ledgerv1.check_row({**base, "quote_other": ""}, corpora)
    assert not row["quote_other_ok"] and not row["supported"]

    # the transcript reader: tool results only, a list of text parts is read per part, other events are ignored
    events = [
        {
            "type": "assistant",
            "message": {"content": [{"type": "text", "text": "assistant text"}]},
        },
        {"type": "user", "message": {"content": "a plain string, not a list"}},
        {
            "type": "user",
            "message": {"content": [{"type": "text", "text": "synthetic text block"}]},
        },
        {
            "type": "user",
            "message": {
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "a",
                        "content": "result one",
                    },
                    {
                        "type": "tool_result",
                        "tool_use_id": "b",
                        "content": [
                            {"type": "text", "text": "part one"},
                            {"type": "image"},
                        ],
                    },
                ]
            },
        },
    ]
    assert ledgerv1.transcript_results(events) == ["result one", "part one"]
    assert ledgerv1.transcript_results({"not": "a list"}) == []
    assert TRANSCRIPT and QO_TRANSCRIPT in TRANSCRIPT[0]
    assert (
        json.loads((REPORTS / "good.attempt1.json").read_text())[0]["type"] == "system"
    )


def test_reader_counts_format_errors_dup_unknown_and_verdicts():
    res = ledgerv1.read_ledger(load("unknown_item"), ASSIGNED)
    assert res["unknown_item"][0]["item"] == "S9" and [
        r["item"] for r in res["rows"]
    ] == ["S1"]
    assert res["missing_line"] == ["S2", "S3"]

    res = ledgerv1.read_ledger(load("dup_line"), ASSIGNED)
    assert len(res["dup_line"]) == 1 and res["dup_line"][0]["item"] == "S1"
    assert {r["item"]: r["verdict"] for r in res["rows"]}[
        "S1"
    ] == "PROBLEM"  # the first line wins

    res = ledgerv1.read_ledger(load("verdict_lowercase"), ASSIGNED)
    assert [r["verdict"] for r in res["rows"]] == ["PROBLEM", "OK", "PROBLEM"]
    assert res["normalised_verdict"] == 3 and res["format_errors"] == []

    # format errors: not JSON, not an object, no verdict, a verdict outside the three, a non-string quote
    text = load("good").replace(
        '{"item": "S2", "verdict": "OK"',
        'not json\n[1]\n{"item": "S2"}\n{"item": "S2", "verdict": "MAYBE"}\n{"item": "S2", "verdict": "OK", "ran": 5}\n{"item": "S2", "verdict": "OK"',
    )
    res = ledgerv1.read_ledger(text, ASSIGNED)
    assert len(res["format_errors"]) == 5
    assert [e["line"] for e in res["format_errors"]] == sorted(
        e["line"] for e in res["format_errors"]
    )
    assert [r["item"] for r in res["rows"]] == [
        "S1",
        "S2",
        "S3",
    ]  # the good S2 line after them still counts

    # limits: a short or long quote_plan, a long problem and a long ran flag the row, which is still kept
    long_ran = " ".join(["w"] * 16)
    row_text = (
        "```ledger-v1\n"
        + json.dumps(
            {
                "item": "S1",
                "verdict": "PROBLEM",
                "quote_plan": "short",
                "problem": "p" * 301,
                "ran": long_ran,
            }
        )
        + "\n"
        + json.dumps({"item": "S2", "verdict": "OK", "quote_plan": "q" * 201})
        + "\n```\n"
    )
    text = "## Ledger\n\n" + row_text + "\n## Findings block\n\n```findings-v1\n```\n"
    rows = {r["item"]: r for r in ledgerv1.read_ledger(text, ASSIGNED)["rows"]}
    assert rows["S1"]["limits_violated"] == ["quote_plan", "problem", "ran"]
    assert rows["S2"]["limits_violated"] == ["quote_plan"]


def test_ok_row_with_finding_is_left_alone():
    report = load("ok_but_finding")
    res = run(report)
    assert res["ok_but_finding"] == 1 and by_id(res)["F1"]["link"] == "probe"
    assert not by_id(res)["F1"]["demoted"] and res["text"] == report
    assert blocking(res["text"]) == {"F1": True}


# ---------------------------------------------------------------- promotion and telemetry (Task 25: DESIGN 9.3, DD-9, DD-11, DD-12)

CLASSES = {"S1": "C1", "S2": "C4", "S3": "C5"}
CLASSED = [{**it, "class": CLASSES[it["item_id"]]} for it in ITEMS]
S2_PROBLEM = (
    '{"item": "S2", "verdict": "PROBLEM", "quote_plan": "The exporter package has no network access.", '
    '"quote_other": "Every module under `src/exporter/` returns an empty result for an empty report.", '
    '"problem": "A module may need the network to be empty-safe.", "ran": "compared two plan lines"}'
)


def run_c(report, assigned=None, items=CLASSED, **kw):
    kw.setdefault("transcript", TRANSCRIPT)
    return ledgerv1.check_report(
        report,
        assigned=assigned or ASSIGNED,
        candidate=CAND,
        source=SRC,
        items=items,
        **kw,
    )


def findings_of(text):
    parsed = fnd.parse_block(text)
    assert parsed["ok"], parsed["errors"]
    return {f["id"]: f for f in parsed["findings"]}


def with_s2_problem(report):
    """problem_no_finding.md with its OK row for S2 turned into a second PROBLEM row without a findings line."""
    ok = next(ln for ln in report.splitlines() if ln.startswith('{"item": "S2"'))
    return report.replace(ok, S2_PROBLEM)


def test_promotion_copies_problem_and_anchor():
    report = load("problem_no_finding")
    res = run_c(report)
    assert res["promotion_failures"] == [] and res["block_unusable"] is None
    # only the PROBLEM row without a findings line is promoted: OK and UNSURE rows never are
    assert res["promoted"] == [{"id": "PS1", "item": "S1", "class": "C1", "line": 17}]
    found = findings_of(res["text"])
    assert set(found) == {"F1", "PS1"}
    row = next(r for r in res["ledger"]["rows"] if r["item"] == "S1")
    p = found["PS1"]
    assert (
        p["claim"]
        == row["problem"]
        == "The task keeps held reports but no criterion tests it."
    )
    assert p["anchor"] == row["quote_plan"] and fnd.locate(CAND, p["anchor"])
    assert (p["severity"], p["blocking"], p["refs"]) == ("MINOR", False, [])
    assert p["category"] == cards.promote_category("C1")
    assert (p["class"], p["probe"], p["src"]) == ("C1", "S1", "ledger")
    assert (
        res["text"].splitlines()[16].startswith('{"id": "PS1"')
    )  # `line` is a line of the checked text
    # the reviewer's own line is untouched, and the report we passed in is not edited
    assert res["text"] != report and report == load("problem_no_finding")
    assert found["F1"] == fnd.parse_block(report)["findings"][0]


def test_promotion_validates_with_check_finding():
    # a long id: P + a 16 character item id is 17 characters
    long_item = "S123456789012345"
    report = load("promote_long_id")
    items = [{"item_id": long_item, "class": "C1", "evidence": []}]
    res = run_c(report, assigned=[long_item], items=items)
    assert res["promoted"] == [] and res["text"] == report
    (failure,) = res["promotion_failures"]
    assert failure["item"] == long_item and failure["id"] == "P" + long_item
    assert "id must match" in failure["reason"]

    # a short anchor: the row's quote_plan has 10 characters, the schema floor is 12
    report = load("promote_short_anchor")
    res = run_c(report)
    assert res["promoted"] == [] and res["text"] == report
    (failure,) = res["promotion_failures"]
    assert (
        failure["item"] == "S1" and "anchor must have at least 12" in failure["reason"]
    )
    assert "quote_plan" in res["ledger"]["rows"][0]["limits_violated"]

    # a duplicate id: the reviewer used both PS1 and the one retry PS1-2
    report = load("promote_dup_id")
    res = run_c(report)
    assert res["promoted"] == [] and res["text"] == report
    (failure,) = res["promotion_failures"]
    assert failure["id"] == "PS1-2" and failure["reason"] == "duplicate id 'PS1-2'"
    # with only PS1 taken the suffix is used and the line is valid (P1)
    one_taken = (
        "\n".join(
            ln for ln in report.splitlines() if not ln.startswith('{"id": "PS1-2"')
        )
        + "\n"
    )
    res = run_c(one_taken)
    assert [p["id"] for p in res["promoted"]] == ["PS1-2"]
    assert set(findings_of(res["text"])) == {"PS1", "PS1-2"}
    assert findings_of(res["text"])["PS1-2"]["src"] == "ledger"


def test_promotion_inside_single_block():
    report = with_s2_problem(load("problem_no_finding"))
    res = run_c(report)
    assert [p["id"] for p in res["promoted"]] == ["PS1", "PS2"]
    text = res["text"]
    assert text.count("```findings-v1") == 1 and text.count("```ledger-v1") == 1
    lines = text.splitlines()
    opener = lines.index("```findings-v1")
    close = lines.index("```", opener)
    # the promoted lines are the last two lines inside the block, directly above the closing fence
    assert [json.loads(ln)["id"] for ln in lines[opener + 1 : close]] == [
        "F1",
        "PS1",
        "PS2",
    ]
    assert [p["line"] for p in res["promoted"]] == [close - 1, close]  # 1-based
    # everything outside the block is as the reviewer wrote it
    head, tail = report.split("```findings-v1")
    assert text.startswith(head + "```findings-v1")
    assert text.endswith("```\n\nverdict: FAIL\n")
    assert fnd.parse_block(text)["ok"]
    # a report with CRLF line endings keeps them
    crlf = run_c(report.replace("\n", "\r\n"))["text"]
    assert crlf.count("\r\n") == crlf.count("\n") and "PS2" in crlf


def test_promotion_failure_logged_and_skipped():
    # one row fails (a 10 character quote), the other is promoted: the failure does not stop the run
    report = with_s2_problem(load("problem_no_finding")).replace(
        "The exporter package has no network access.", "no network"
    )
    res = run_c(report)
    assert [p["item"] for p in res["promoted"]] == ["S1"]
    assert [(f["item"], f["id"]) for f in res["promotion_failures"]] == [("S2", "PS2")]
    assert set(findings_of(res["text"])) == {"F1", "PS1"}  # PS2 is not in the block

    def reason_for(report, **kw):
        res = run_c(report, **kw)
        assert res["promoted"] == [], res["promoted"]
        assert res["text"] == report
        (f,) = res["promotion_failures"]
        return f["reason"]

    base = load("promote_long_id").replace("S123456789012345", "S1")
    assert "a ledger limit: ran" in reason_for(
        base.replace('"compared task and source 2.3"', json.dumps(" ".join(["w"] * 16)))
    )
    assert "problem is empty" in reason_for(
        base.replace('"The task keeps held reports but no criterion tests it."', '""')
    )
    # an item with no class in items.json has no category to promote under
    assert "no class" in reason_for(base, items=ITEMS)
    # a class with no card
    assert "no card for class C9" in reason_for(
        base, items=[{"item_id": "S1", "class": "C9", "evidence": []}]
    )

    # the failure reaches check.json's list with the reviewer id
    summary = ledgerv1.summarise({"r1": run_c(load("promote_short_anchor"))})
    assert summary["promoted"] == 0
    assert [(f["rid"], f["item"]) for f in summary["promotion_failures"]] == [
        ("r1", "S1")
    ]


def test_class_key_added_from_item():
    report = load("good")
    res = run_c(report)
    found = findings_of(res["text"])
    # F1 and F3 link to a row (by probe) and get the class of the item; F2 links to nothing and gets none
    assert found["F1"]["class"] == "C1" and found["F3"]["class"] == "C5"
    assert "class" not in found["F2"] and found["F1"]["probe"] == "S1"
    assert res["class_added"] == 2 and res["class_corrected"] == 0
    assert [f["class_change"] for f in res["findings"]] == ["added", None, "added"]
    assert res["text"] != report and report == load("good")

    # a wrong class is corrected and counted; a right one is left alone and not counted
    wrong = report.replace('"probe": "S1"}', '"probe": "S1", "class": "C9"}').replace(
        '"probe": "S3"}', '"probe": "S3", "class": "C5"}'
    )
    res = run_c(wrong)
    found = findings_of(res["text"])
    assert found["F1"]["class"] == "C1" and found["F3"]["class"] == "C5"
    assert (res["class_added"], res["class_corrected"]) == (0, 1)
    assert [f["class_change"] for f in res["findings"]] == ["corrected", None, None]

    # a quote-linked line without a probe gets the class and still has no probe (the reviewer sets only `probe`)
    no_probe = report.replace(', "probe": "S1"}', "}")
    found = findings_of(run_c(no_probe)["text"])
    assert found["F1"]["class"] == "C1" and "probe" not in found["F1"]

    # nothing in items.json carries a class: the text is not touched
    assert run_c(report, items=ITEMS)["text"] == report
