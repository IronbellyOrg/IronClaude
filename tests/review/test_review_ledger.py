"""Typed finding ledger: statuses, events, verdict, capture export (PN1, C6-C7)."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from superclaude.cli.review import ledger as ldg

FIX = Path(__file__).parent / "fixtures"
SEEDED = (FIX / "seeded.md").read_text()
CLEAN = (FIX / "clean.md").read_text()

A_S1 = "The worker retries a failed delivery up to 8 times with exponential backoff"
A_S2 = "the worker deletes all of its delivery-log rows immediately to save storage"
A_S3 = "logs the full request headers and the webhook's signing secret at INFO level"


def fl(
    fid,
    anchor,
    refs,
    *,
    blocking=True,
    severity="CRITICAL",
    claim="wrong outcome",
    **extra,
):
    d = {
        "id": fid,
        "severity": severity,
        "blocking": blocking,
        "category": "contradiction",
        "anchor": anchor,
        "refs": refs,
        "claim": claim,
    }
    d.update(extra)
    return json.dumps(d)


def report(*lines):
    return (
        "review: 1 of 3\n\nbody\n\n## Findings block\n\n```findings-v1\n"
        + "\n".join(lines)
        + "\n```\n\nverdict: FAIL\n"
    )


def rev(rid, *lines, model="m"):
    return {
        "reviewer_id": rid,
        "model": model,
        "report_path": f"{rid}.md",
        "text": report(*lines),
    }


def round1(doc=SEEDED):
    led = ldg.new_ledger("spec.md")
    res = ldg.merge_round(
        led,
        doc,
        1,
        [
            rev(
                "t1b-1",
                fl("F1", A_S1, ["FR-3"]),
                fl("F2", A_S2, ["FR-7"]),
                fl(
                    "F9",
                    "A timeout counts as a failed attempt.",
                    ["FR-2"],
                    blocking=False,
                    severity="MINOR",
                ),
            ),
            rev(
                "t2-1",
                fl(
                    "G1",
                    "retries a failed delivery up to 8 times with exponential",
                    ["FR-3"],
                    claim="other wording",
                ),
                fl("G2", A_S3, ["FR-4"]),
            ),
        ],
    )
    return led, res


def revised(doc):
    return doc.replace(
        "up to 8 times with exponential backoff, doubling the delay after each attempt, and marks it `FAILED` after the ninth failed attempt",
        "at most 5 times as FR-3 states",
    ).replace(
        "deletes all of its delivery-log rows immediately to save storage",
        "keeps its delivery-log rows for 30 days as FR-7 states",
    )


def status(led):
    return {r["lid"]: r["status"] for r in led["rows"]}


def events(led, lid):
    return [
        h["event"] for h in next(r for r in led["rows"] if r["lid"] == lid)["history"]
    ]


def test_round_one_creates_rows_with_confidence_and_blocking():
    led, res = round1()
    assert [r["lid"] for r in led["rows"]] == ["L1", "L2", "L3", "L4"]
    by = {r["lid"]: r for r in led["rows"]}
    assert by["L1"]["confidence"] == "overlap" and len(by["L1"]["members"]) == 2
    assert by["L2"]["confidence"] == "single"
    assert by["L3"]["blocking"] is False and by["L3"]["status"] == "open"
    assert by["L4"]["blocking"] is True
    assert all(
        r["status"] == "open" and r["history"][0] == {"round": 1, "event": "opened"}
        for r in led["rows"]
    )
    assert res["verdict"] == "FAIL" and res["decision"] == "REVISE"
    assert res["brief_ids"] == ["L1", "L2", "L4"]
    assert res["block_ok"] == {"t1b-1": True, "t2-1": True}
    assert res["new"] == ["L1", "L2", "L3", "L4"]
    assert (
        led["rounds"][0]["verdict"] == "FAIL"
        and led["rounds"][0]["decision"] == "REVISE"
    )
    assert led["cap_reviews"] == 3 and led["schema"] == "review-ledger/1"


def test_every_input_finding_is_a_member_exactly_once():
    led, _ = round1()
    members = [(m["reviewer_id"], m["fid"]) for r in led["rows"] for m in r["members"]]
    assert sorted(members) == sorted(
        [
            ("t1b-1", "F1"),
            ("t1b-1", "F2"),
            ("t1b-1", "F9"),
            ("t2-1", "G1"),
            ("t2-1", "G2"),
        ]
    )


def test_revision_resolved_check_rejected_and_named_not_touched():
    led, _ = round1()
    new = revised(SEEDED)
    assert new != SEEDED
    fix = [
        {"id": "L1", "action": "applied", "reason": "r"},
        {"id": "L2", "action": "applied", "reason": "r"},
        {"id": "L4", "action": "rejected", "reason": "not a defect"},
    ]
    out = ldg.apply_revision(led, SEEDED, new, fix)
    assert status(led) == {
        "L1": "resolved_check",
        "L2": "resolved_check",
        "L3": "open",
        "L4": "open",
    }
    assert (
        events(led, "L1")[-1] == "resolved_check"
        and events(led, "L4")[-1] == "rejected_by_reviser"
    )
    assert out["resolved_check"] == ["L1", "L2"] and out["rejected"] == ["L4"]
    # named but the text is unchanged: stays open
    led2, _ = round1()
    ldg.apply_revision(
        led2, SEEDED, SEEDED, [{"id": "L1", "action": "applied", "reason": "r"}]
    )
    assert (
        status(led2)["L1"] == "open" and events(led2, "L1")[-1] == "named_not_touched"
    )


def test_spans_follow_the_revision():
    led, _ = round1()
    before = {r["lid"]: tuple(r["span"]) for r in led["rows"]}
    new = "\n".join(["# inserted", "# lines", "", ""]) + SEEDED
    ldg.apply_revision(led, SEEDED, new, [])
    after = {r["lid"]: tuple(r["span"]) for r in led["rows"]}
    assert all(after[k][0] == before[k][0] + 3 for k in before)


def test_cleared_after_the_next_round_and_refound_stays_open():
    led, _ = round1()
    new = revised(SEEDED)
    ldg.apply_revision(
        led,
        SEEDED,
        new,
        [
            {"id": "L1", "action": "applied", "reason": "r"},
            {"id": "L2", "action": "applied", "reason": "r"},
            {"id": "L4", "action": "applied", "reason": "no"},
        ],
    )
    res = ldg.merge_round(led, new, 2, [rev("t1b-1", fl("H1", A_S3, ["FR-4"]))])
    assert status(led)["L1"] == "resolved" and events(led, "L1")[-1] == "cleared"
    assert status(led)["L2"] == "resolved"
    assert res["cleared"] == ["L1", "L2"]
    assert status(led)["L4"] == "open" and events(led, "L4")[-1] == "refound"
    assert res["refound"] == ["L4"]
    assert (
        res["verdict"] == "FAIL"
        and res["decision"] == "REVISE"
        and res["brief_ids"] == ["L4"]
    )
    assert led["rounds"][1]["n"] == 2


def test_refound_resolved_row_becomes_regressed_and_fails():
    led, _ = round1()
    new = revised(SEEDED)
    ldg.apply_revision(
        led,
        SEEDED,
        new,
        [
            {"id": "L1", "action": "applied", "reason": "r"},
            {"id": "L2", "action": "applied", "reason": "r"},
            {"id": "L4", "action": "applied", "reason": "x"},
        ],
    )
    # the reviser removed S3 too, so a re-review that re-finds L1 in the new text must regress it
    res = ldg.merge_round(
        led,
        new,
        2,
        [
            rev(
                "t1b-1",
                fl(
                    "H1",
                    "at most 5 times as FR-3 states",
                    ["FR-3"],
                    claim="still wrong",
                ),
            )
        ],
    )
    assert status(led)["L1"] == "regressed" and "refound" in events(led, "L1")
    assert res["regressed"] == ["L1"]
    assert res["verdict"] == "FAIL" and "L1" in res["brief_ids"]


def test_regressed_row_re_resolves_through_the_same_path():
    led, _ = round1()
    new = revised(SEEDED)
    ldg.apply_revision(
        led, SEEDED, new, [{"id": "L1", "action": "applied", "reason": "r"}]
    )
    ldg.merge_round(
        led,
        new,
        2,
        [rev("t1b-1", fl("H1", "at most 5 times as FR-3 states", ["FR-3"]))],
    )
    assert status(led)["L1"] == "regressed"
    new2 = new.replace(
        "at most 5 times as FR-3 states", "at most 5 times (6 attempts in total)"
    )
    ldg.apply_revision(
        led, new, new2, [{"id": "L1", "action": "applied", "reason": "r"}]
    )
    assert status(led)["L1"] == "resolved_check"


def test_verdict_and_decision_at_rounds_1_to_3():
    led = ldg.new_ledger("d.md")
    r1 = ldg.merge_round(led, SEEDED, 1, [rev("t1b-1", fl("F1", A_S1, ["FR-3"]))])
    assert (r1["verdict"], r1["decision"]) == ("FAIL", "REVISE")
    ldg.apply_revision(
        led, SEEDED, revised(SEEDED), [{"id": "L1", "action": "applied", "reason": "r"}]
    )
    new = revised(SEEDED)
    r2 = ldg.merge_round(led, new, 2, [rev("t1b-1", fl("H1", A_S3, ["FR-4"]))])
    assert (r2["verdict"], r2["decision"]) == ("FAIL", "REVISE") and r2[
        "brief_ids"
    ] == ["L2"]
    ldg.apply_revision(
        led, new, new, [{"id": "L2", "action": "applied", "reason": "r"}]
    )
    r3 = ldg.merge_round(led, new, 3, [rev("t1b-1", fl("K1", A_S3, ["FR-4"]))])
    assert (r3["verdict"], r3["decision"]) == ("FAIL", "ESCALATE")
    assert ldg.verdict(led)["decision"] == "ESCALATE"

    led2 = ldg.new_ledger("d.md")
    p = ldg.merge_round(led2, CLEAN, 1, [rev("t1b-1")])
    assert (p["verdict"], p["decision"], p["brief_ids"]) == ("PASS", "PASS", [])
    assert ldg.verdict(led2) == {
        "verdict": "PASS",
        "decision": "PASS",
        "brief_ids": [],
        "round": 1,
    }


def test_non_blocking_findings_never_fail():
    led = ldg.new_ledger("d.md")
    res = ldg.merge_round(
        led,
        SEEDED,
        1,
        [rev("t1b-1", fl("F1", A_S1, ["FR-3"], blocking=False, severity="MINOR"))],
    )
    assert res["verdict"] == "PASS"


def test_prior_lines_never_change_a_status():
    led, _ = round1()
    new = revised(SEEDED)
    ldg.apply_revision(
        led, SEEDED, new, [{"id": "L1", "action": "applied", "reason": "r"}]
    )
    prior = json.dumps({"prior": "L4", "status": "resolved"})
    res = ldg.merge_round(
        led,
        new,
        2,
        [rev("t1b-1", prior, json.dumps({"prior": "L2", "status": "open"}))],
    )
    assert status(led)["L4"] == "open" and res["verdict"] == "FAIL"
    assert status(led)["L2"] == "open"
    assert any(
        h["event"] == "prior_note"
        for r in led["rows"]
        if r["lid"] == "L4"
        for h in r["history"]
    )


def _broken(rid="t1b-1", text="review: 2 of 3\nverdict: PASS\n"):
    return {"reviewer_id": rid, "model": "m", "report_path": "r.md", "text": text}


def test_round_with_no_valid_block_is_refused_and_changes_nothing():
    """Review finding (Codex P1): an invalid review must never certify PASS."""
    led, _ = round1()
    new = revised(SEEDED)
    ldg.apply_revision(
        led, SEEDED, new, [{"id": "L1", "action": "applied", "reason": "r"}]
    )
    before = json.dumps(led, sort_keys=True)
    with pytest.raises(
        ldg.LedgerError, match="no reviewer produced a valid findings block"
    ):
        ldg.merge_round(led, new, 2, [_broken()])
    assert (
        json.dumps(led, sort_keys=True) == before
    )  # no round recorded, no row cleared
    assert status(led)["L1"] == "resolved_check"
    assert len(led["rounds"]) == 1


def test_first_round_with_no_valid_block_is_refused_not_pass():
    led = ldg.new_ledger("d.md")
    for text in (
        "review: 1 of 3\nincomplete\n",  # no findings block at all
        "review: 1 of 3\n\n## Findings block\n\n```findings-v1\n{not json\n```\n",
        "review: 1 of 3\n\n## Findings block\n\n```findings-v1\n",  # truncated, never closed
    ):
        with pytest.raises(ldg.LedgerError):
            ldg.merge_round(led, SEEDED, 1, [_broken(text=text)])
    assert led["rounds"] == [] and led["rows"] == []


def test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported():
    led, _ = round1()
    new = revised(SEEDED)
    ldg.apply_revision(
        led, SEEDED, new, [{"id": "L1", "action": "applied", "reason": "r"}]
    )
    res = ldg.merge_round(led, new, 2, [rev("t1b-1"), _broken("t2-1")])
    assert res["block_ok"] == {"t1b-1": True, "t2-1": False}
    assert res["warnings"]
    assert status(led)["L1"] == "resolved"


def test_round_cannot_be_merged_twice_or_out_of_order():
    led, _ = round1()
    with pytest.raises(ldg.LedgerError):
        ldg.merge_round(led, SEEDED, 1, [rev("t1b-1")])
    with pytest.raises(ldg.LedgerError):
        ldg.merge_round(led, SEEDED, 3, [rev("t1b-1")])


def test_defer_turns_a_blocking_row_into_deferred():
    led = ldg.new_ledger("d.md")
    ldg.merge_round(led, SEEDED, 1, [rev("t1b-1", fl("F1", A_S3, ["FR-4"]))])
    assert ldg.verdict(led)["verdict"] == "FAIL"
    ldg.defer(led, "L1", "accepted risk")
    assert status(led)["L1"] == "deferred" and events(led, "L1")[-1] == "deferred"
    v = ldg.verdict(led)
    assert v["verdict"] == "PASS" and v["decision"] == "PASS" and v["brief_ids"] == []
    with pytest.raises(ldg.LedgerError):
        ldg.defer(led, "L9", "no such row")


def test_missing_anchor_is_kept_without_a_span():
    led = ldg.new_ledger("d.md")
    ldg.merge_round(
        led,
        SEEDED,
        1,
        [rev("t1b-1", fl("F1", "this text is nowhere in the document", ["FR-3"]))],
    )
    row = led["rows"][0]
    assert row["span"] is None and row["status"] == "open" and row["blocking"] is True


def test_capture_export():
    led, _ = round1()
    cap = ldg.capture(led, 1, source="ledger.json")
    assert cap["schema"] == "review-capture/1" and cap["round"] == 1
    assert cap["occasions"] == ["t1b-1", "t2-1"]
    assert cap["doc_sha256"] == led["rounds"][0]["doc_sha256"]
    by = {d["key"]: d for d in cap["defects"]}
    assert by["L1"] == {"key": "L1", "blocking": True, "captured_by": ["t1b-1", "t2-1"]}
    assert by["L2"]["captured_by"] == ["t1b-1"] and by["L4"]["captured_by"] == ["t2-1"]
    assert by["L3"]["blocking"] is False


def test_atomic_save_leaves_no_temp_file(tmp_path):
    led, _ = round1()
    path = tmp_path / "review" / "ledger.json"
    ldg.save(led, str(path))
    ldg.save(led, str(path))
    assert sorted(os.listdir(path.parent)) == ["ledger.json"]
    assert ldg.load(str(path)) == json.loads(path.read_text())
    assert json.loads(path.read_text())["rows"][0]["lid"] == "L1"


def test_rendered_merged_report():
    led, res = round1()
    text = ldg.render_merged_report(led, res, doc_path="spec.md", doc_text=SEEDED, n=1)
    lines = text.splitlines()
    assert lines[0] == "review: 1 of 3"
    assert lines[1] == "# Merged review 1 (coordinator script; panel of 2 reviewers)"
    assert lines[2].startswith("candidate: spec.md sha256 ")
    assert (
        "## Ledger" in text
        and "| lid | status | blocking | confidence | severity | refs | reviewers |"
        in text
    )
    assert (
        "### L1" in text
        and "#### L1.t1b-1 (F1)" in text
        and "#### L1.t2-1 (G1)" in text
    )
    assert "## Other findings" in text and "## Reviser brief" in text
    assert "Blocking finding ids: L1, L2, L4." in text
    assert (
        "Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names;"
        in text
    )
    assert lines[-1] == "verdict: FAIL"
    # the reviser brief id parser of the Stage 2 harness reads these ids
    assert "L3" not in text.split("## Reviser brief")[1].split("Rules for")[0]
    led2 = ldg.new_ledger("d.md")
    r = ldg.merge_round(led2, CLEAN, 1, [rev("t1b-1")])
    t2 = ldg.render_merged_report(led2, r, doc_path="d.md", doc_text=CLEAN, n=1)
    assert (
        "Blocking finding ids: none." in t2 and t2.splitlines()[-1] == "verdict: PASS"
    )


def test_escalate_still_prints_verdict_fail():
    led = ldg.new_ledger("d.md")
    for n in (1, 2):
        ldg.merge_round(led, SEEDED, n, [rev("t1b-1", fl("F1", A_S3, ["FR-4"]))])
        ldg.apply_revision(
            led, SEEDED, SEEDED, [{"id": "L1", "action": "applied", "reason": "r"}]
        )
    res = ldg.merge_round(led, SEEDED, 3, [rev("t1b-1", fl("F1", A_S3, ["FR-4"]))])
    assert res["decision"] == "ESCALATE"
    text = ldg.render_merged_report(led, res, doc_path="d.md", doc_text=SEEDED, n=3)
    assert text.splitlines()[-1] == "verdict: FAIL"
    assert text.splitlines()[0] == "review: 3 of 3"
    # at the cap the report escalates and carries no Reviser brief
    assert "## Reviser brief" not in text and "Rules for the reviser" not in text
    assert "## Escalation" in text and "do not start another fix cycle" in text


def test_refound_row_takes_the_current_finding_span():
    # A revision can map a span onto the start of a longer replacement; the next report that
    # re-finds the defect farther down must re-anchor the row, or a later fix is never seen.
    led, _ = round1()
    row = next(r for r in led["rows"] if r["lid"] == "L4")
    located = list(row["span"])
    row["span"] = [located[0] - 1, located[0] - 1]
    ldg.merge_round(led, SEEDED, 2, [rev("t1b-1", fl("H1", A_S3, ["FR-4"]))])
    assert events(led, "L4")[-1] == "refound"
    assert row["span"] == located


def test_revision_from_a_text_other_than_the_reviewed_one_is_refused():
    led, _ = round1()
    before = json.dumps(led, sort_keys=True)
    with pytest.raises(ldg.LedgerError, match="sha256 mismatch"):
        ldg.apply_revision(
            led,
            CLEAN,
            revised(SEEDED),
            [{"id": "L1", "action": "applied", "reason": "r"}],
        )
    assert json.dumps(led, sort_keys=True) == before


def test_refound_as_nonblocking_stops_failing_the_review():
    led, _ = round1()
    ldg.apply_revision(
        led,
        SEEDED,
        revised(SEEDED),
        [{"id": "L1", "action": "applied", "reason": "r"}],
    )
    res = ldg.merge_round(
        led,
        revised(SEEDED),
        2,
        [
            rev(
                "t1b-1",
                fl(
                    "H1",
                    "at most 5 times as FR-3 states",
                    ["FR-3"],
                    blocking=False,
                    severity="MINOR",
                ),
            )
        ],
    )
    row = next(r for r in led["rows"] if r["lid"] == "L1")
    assert row["blocking"] is False and "L1" not in res["brief_ids"]
