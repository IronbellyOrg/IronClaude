"""S5 as a whole: `sweep check` over a run folder (DESIGN 9.4, 10 rows 10 to 12; DD-9, DD-12; REQ-15).

The run folders are built in tmp_path from the invented fixtures of fixtures/reports and fixtures/plans. No model runs.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys

from helpers import SW

from scaffold import fnd, normalise
from sweep import cli

CLI = SW / "sweep" / "cli.py"
REPORTS = SW / "fixtures" / "reports"
PLANS = SW / "fixtures" / "plans"
ITEM_CLASS = {"S1": "C1", "S2": "C4", "S3": "C5"}
FIELDS_9_4 = {
    "ledger_missing", "format_errors", "normalised_verdict", "dup_line", "unknown_item", "probe_unknown",
    "missing_line", "rows", "demoted", "format_induced_demotions", "promoted", "promotion_failures",
    "ok_but_finding", "block_unusable",
}  # fmt: skip


def make_run(tmp_path, reports, *, no_report=()):
    """RUN/{prepass/items.json, prepass/assignment.json, reviews/<rid>.md and .attempt1.json}; {rid: fixture name}."""
    run = tmp_path / "run"
    (run / "prepass").mkdir(parents=True)
    (run / "reviews").mkdir()
    items = [{"item_id": i, "class": c, "evidence": []} for i, c in ITEM_CLASS.items()]
    (run / "prepass" / "items.json").write_text(json.dumps({"items": items}))
    rids = [*reports, *no_report]
    (run / "prepass" / "assignment.json").write_text(
        json.dumps({"reviewers": {rid: list(ITEM_CLASS) for rid in rids}})
    )
    for rid, name in reports.items():
        shutil.copy(REPORTS / f"{name}.md", run / "reviews" / f"{rid}.md")
        shutil.copy(
            REPORTS / "good.attempt1.json", run / "reviews" / f"{rid}.attempt1.json"
        )
    return run


def check(run, **kw):
    return cli.run_check(run, PLANS / "p_basic.md", PLANS / "source.md", **kw)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_check_writes_outputs_and_leaves_raw_reports_alone(tmp_path):
    run = make_run(
        tmp_path, {"ra": "good", "rb": "problem_no_finding"}, no_report=["rc"]
    )
    before = {p.name: sha(p) for p in (run / "reviews").iterdir()}
    summary = check(run)
    assert {
        p.name: sha(p) for p in (run / "reviews").iterdir()
    } == before  # raw reviews are never edited
    out = run / "check"
    assert sorted(p.name for p in out.iterdir()) == [
        "check.json", "ra.checked.md", "ra.ledger.json", "rb.checked.md", "rb.ledger.json",
    ]  # fmt: skip
    assert json.loads((out / "check.json").read_text()) == summary
    assert FIELDS_9_4 <= set(summary)
    assert summary["no_report"] == ["rc"]
    # promoted findings are counted apart from the reviewers' own: 3 + 1 lines written, 1 line inserted
    assert (summary["reviewer_findings"], summary["promoted"]) == (4, 1)
    checked = fnd.parse_block((out / "rb.checked.md").read_text())
    assert checked["ok"] and [f["id"] for f in checked["findings"]] == ["F1", "PS1"]
    assert (out / "rb.checked.md").read_text() != (
        run / "reviews" / "rb.md"
    ).read_text()
    led = json.loads((out / "rb.ledger.json").read_text())
    assert (
        led["rid"] == "rb" and led["promoted"][0]["id"] == "PS1" and "text" not in led
    )
    assert {r["item"]: r["corpus"] for r in led["ledger"]["rows"]}["S1"] == "source"
    # telemetry: the two linked lines of `good` got their class, PS1 carries class, probe and src
    assert summary["class_added"] == 2
    assert summary["per_class"]["C1"] == {
        "rows": {"OK": 0, "PROBLEM": 2, "UNSURE": 0},
        "linked": 1, "demoted": 0, "ok_but_finding": 0, "promoted": 1, "promotion_failures": 0,
    }  # fmt: skip


def test_check_json_counts_every_field(tmp_path):
    reports = {
        "ra": "good", "rb": "problem_no_finding", "rc": "ledger_missing", "rd": "findings_unclosed",
        "re": "unknown_item", "rf": "dup_line", "rg": "verdict_lowercase", "rh": "bad_json_line",
        "ri": "ok_but_finding",
    }  # fmt: skip
    run = make_run(tmp_path, reports)
    s = check(run)
    assert s["ledger_missing"] == ["rc"] and s["block_unusable"] == ["rd"]
    assert (
        s["unknown_item"] == 1 and s["dup_line"] == 1 and s["normalised_verdict"] == 3
    )
    assert s["format_errors"] == 1 and s["ok_but_finding"] == 1
    assert s["missing_line"] == {  # P7: a ledger_missing reviewer is under `ledger_missing` alone
        "rd": ["S2", "S3"], "re": ["S2", "S3"], "rf": ["S3"], "ri": ["S2", "S3"],
    }  # fmt: skip
    assert s["rows"] == {"OK": 5, "PROBLEM": 10, "UNSURE": 1}
    assert s["demoted"] == {
        "row_unsupported": 0,
        "row_unsure": 0,
        "no_cb3": 0,
        "row_missing": 1,
    }
    assert s["format_induced_demotions"] == 1 and s["probe_unknown"] == 0
    assert s["promoted"] == 1 and s["promotion_failures"] == []
    # rc has no ledger: nothing demoted, nothing promoted, nothing rewritten (DESIGN 10 row 10)
    assert (run / "check" / "rc.checked.md").read_text() == (
        run / "reviews" / "rc.md"
    ).read_text()
    # rd has a truncated findings block: the report is written back unchanged
    assert (run / "check" / "rd.checked.md").read_text() == (
        run / "reviews" / "rd.md"
    ).read_text()


def test_format_induced_demotions_reported(tmp_path):
    run = make_run(tmp_path, {"ra": "good"})
    report = run / "reviews" / "ra.md"
    report.write_text(
        report.read_text().replace(
            "docs/guide.md:14: The exporter writes 3 report formats to disk.",
            "docs/guide.md:99: a line nobody printed",
        )
    )
    s = check(run)
    assert s["demoted"]["row_unsupported"] == 1 and s["format_induced_demotions"] == 1


def test_h2_leaves_a_promoted_line_unchanged(tmp_path):
    """DD-9: S5 runs first and H2 second; a promoted line is built inside the limits, so H2 does not change it."""
    run = make_run(tmp_path, {"rb": "problem_no_finding"})
    check(run)
    checked = run / "check" / "rb.checked.md"
    normalise.normalise_file(checked, tmp_path / "normalised", "rb")
    before = fnd.parse_block(checked.read_text())
    after = fnd.parse_block((tmp_path / "normalised" / "rb.md").read_text())
    assert after["ok"] and before["findings"] == after["findings"]


def cli_run(*args, env=None):
    return subprocess.run(
        [sys.executable, str(CLI), *map(str, args)],
        capture_output=True,
        text=True,
        env=env,
    )


def test_check_help_and_cli_run(tmp_path):
    r = cli_run("check", "--help")
    assert r.returncode == 0 and "--run" in r.stdout and "--candidate" in r.stdout
    run = make_run(tmp_path, {"rb": "problem_no_finding"})
    r = cli_run(
        "check",
        "--run",
        run,
        "--candidate",
        PLANS / "p_basic.md",
        "--source",
        PLANS / "source.md",
    )
    assert r.returncode == 0, r.stderr
    assert (
        json.loads(r.stdout)["promoted"] == 1
        and (run / "check" / "check.json").is_file()
    )
    # the output folder can be named
    r = cli_run(
        "check",
        "--run",
        run,
        "--candidate",
        PLANS / "p_basic.md",
        "--out-dir",
        tmp_path / "elsewhere",
    )
    assert r.returncode == 0 and (tmp_path / "elsewhere" / "rb.checked.md").is_file()


def test_check_exception_exits_1_and_writes_nothing(tmp_path):
    """DESIGN 10 row 11: any exception is for the caller to catch; no half-written check/ is left behind."""
    run = make_run(tmp_path, {"ra": "good", "rb": "problem_no_finding"})
    (run / "prepass" / "items.json").write_text("{not json")
    r = cli_run("check", "--run", run, "--candidate", PLANS / "p_basic.md")
    assert r.returncode == 1 and "check failed: JSONDecodeError" in r.stderr
    assert not (run / "check").exists()
    # a failure on the second reviewer, after the first was checked, still leaves no file
    run = make_run(tmp_path / "two", {"ra": "good", "rb": "problem_no_finding"})
    (run / "reviews" / "rb.attempt1.json").write_text("{not json")
    r = cli_run("check", "--run", run, "--candidate", PLANS / "p_basic.md")
    assert r.returncode == 1 and not (run / "check").exists()
    # a bad CHECK_SCOPE is an exception too
    run = make_run(tmp_path / "three", {"ra": "good"})
    env = {**os.environ, "CHECK_SCOPE": "everything"}
    r = cli_run("check", "--run", run, "--candidate", PLANS / "p_basic.md", env=env)
    assert (
        r.returncode == 1 and "CHECK_SCOPE" in r.stderr and not (run / "check").exists()
    )
