"""bin/run-panel.sh against the fake claude and the real `superclaude review merge` (DESIGN 2.2, 7.6, 8, 9.1, 9.6;
REQ-02 whole path, REQ-12 b, REQ-26 no_budget, REQ-27 whole path, REQ-30). No model starts; the sandbox is the invented
F-REPO under /tmp/evalsb-recipe-test-*, the run folders are temporary."""

import hashlib
import json
import os
import shutil
import subprocess
import time

import pytest
from helpers import SW
from panel_support import (
    EMBER,
    EMBER_MODEL,
    L1,
    L2,
    LUNA_MODEL,
    SCRIPT,
    calls,
    make_sandbox,
    new_root,
    run_panel,
    sandbox,  # noqa: F401  (session fixture)
)

from rl import cli
from scaffold import briefs, fnd

pytestmark = pytest.mark.slow
EMBER_MISSING = {"FAKE_SCENARIO_BY_MODEL": f"{EMBER_MODEL}=ledger_missing"}


def kinds(run, model):
    return [c[3] for c in run.calls if c[2] == model]


@pytest.fixture(scope="module")
def long_run(sandbox):  # noqa: F811
    r = run_panel(sandbox, "long_anchor")
    assert r.rc == 0, r.err
    return r


@pytest.fixture(scope="module")
def reask_run(sandbox):  # noqa: F811
    r = run_panel(sandbox, env=EMBER_MISSING)
    assert r.rc == 0, r.err
    return r


@pytest.fixture(scope="module")
def killed_run(sandbox):  # noqa: F811
    """Arm Z0 with b 2: the hang guard is 3 s, so the sleeping ember is killed quickly."""
    t = time.monotonic()
    r = run_panel(
        sandbox,
        "ok",
        arm="Z0",
        b="2",
        env={"FAKE_SCENARIO_BY_MODEL": f"{EMBER_MODEL}=sleep", "FAKE_SLEEP_S": "60"},
    )
    r.wall = time.monotonic() - t
    return r


# ---------------------------------------------------------------- REQ-02, order


def test_long_anchor_survives_h2_then_merge(long_run):
    r = long_run
    raw = (r.run / "reviews" / f"{EMBER}.md").read_text()
    assert (
        fnd.parse_block(raw)["ok"] is False
    )  # 250 characters: the real parser refuses it as written
    normalised = (r.run / "normalised" / f"{EMBER}.md").read_text()
    parsed = fnd.parse_block(normalised)
    assert parsed["ok"] and len(parsed["findings"][0]["anchor"]) <= 200
    assert r.js("normalised/h2.json")["reports"][EMBER]["changed"][0]["fields"] == [
        "anchor"
    ]
    assert sorted(r.js("merged/merge-input.json")["used"]) == sorted([EMBER, L1, L2])
    merged = r.js("merged/ledger.json")
    assert [x["block_ok"] for x in merged["rounds"][0]["reviewers"]] == [True] * 3
    (row,) = merged[
        "rows"
    ]  # the three reviewers' finding is one row, with the cut anchor
    assert 100 < len(row["anchor"]) <= 200
    assert (
        (r.run / "merged" / "merged-1.md")
        .read_text()
        .rstrip()
        .endswith("verdict: PASS")
    )
    assert r.js("run.json")["merge_refused"] is False


def test_order_check_then_h2_then_merge(long_run):
    r = long_run
    t = lambda p: (r.run / p).stat().st_mtime_ns  # noqa: E731
    assert t("check/check.json") < t("normalised/h2.json") < t("merged/merged-1.md")
    # the check read the long anchor before H2 cut it: the checked report still holds all 250 characters
    checked = (r.run / "check" / f"{EMBER}.checked.md").read_text()
    anchor = json.loads(
        next(ln for ln in checked.splitlines() if ln.startswith('{"id"'))
    )["anchor"]
    assert len(fnd.flat(anchor)) == 250
    cut = fnd.parse_block((r.run / "normalised" / f"{EMBER}.md").read_text())
    assert len(cut["findings"][0]["anchor"]) == 200


# ---------------------------------------------------------------- REQ-12 b


def test_forced_exception_in_check_merges_as_written(sandbox):  # noqa: F811
    r = run_panel(sandbox, env={"RL_FORCE_EXC": "check"})
    assert r.rc == 0, r.err
    run = r.js("run.json")
    assert run["check_skipped"] is True and run["check_ran"] is False
    assert "RL_FORCE_EXC=check" in (r.run / "check" / "error.log").read_text()
    assert not (r.run / "check" / "check.json").exists()
    for rid in (EMBER, L1, L2):  # the text given to the merge is the raw report
        assert (r.run / "normalised" / f"{rid}.md").read_text() == (
            r.run / "reviews" / f"{rid}.md"
        ).read_text()
    assert (r.run / "merged" / "merged-1.md").is_file() and run[
        "merge_refused"
    ] is False
    assert len(r.calls) == 3


# ---------------------------------------------------------------- REQ-27, the re-ask


def test_ember_reask_runs_once_and_is_accepted(reask_run):
    r = reask_run
    assert kinds(r, EMBER_MODEL) == ["review", "repair"]
    assert kinds(r, LUNA_MODEL) == ["review", "review"]
    assert r.js("run.json")["reask"] == [EMBER]
    rec = r.js(f"reviews/{EMBER}.reask.json")
    assert (rec["asked"], rec["accepted"], rec["reason"]) == (True, True, "accepted")
    assert (r.run / "reviews" / f"{EMBER}.preask.md").is_file()
    assert fnd.parse_block((r.run / "reviews" / f"{EMBER}.md").read_text())["ok"]
    check = r.js("check/check.json")
    assert check["ledger_missing"] == []
    assert check["reask"][EMBER]["accepted"] is True
    assert (
        r.js(f"check/{EMBER}.ledger.json")["via_reask"] is True
    )  # its rows are marked
    assert r.js(f"check/{L1}.ledger.json")["via_reask"] is False


def test_reask_seconds_are_inside_the_clock(reask_run):
    r = reask_run
    timing = r.js("timing.json")
    sec = r.js(f"reviews/{EMBER}.reask.json")["seconds"]
    assert sec > 0 and timing["reask_s"] == sec
    assert (
        timing["panel_elapsed_s"]
        >= timing["rev_end"][EMBER] - timing["t0"] + sec - 1e-6
    )


def test_reask_not_counted_as_retry(reask_run):
    r = reask_run
    assert [c[3] for c in r.calls].count("review") == 3  # one review call per reviewer
    assert [c[3] for c in r.calls].count("repair") == 1
    run = r.js("run.json")
    assert run["retries"] == 0 and run["reask"] == [EMBER]
    for rid in (EMBER, L1, L2):
        assert (
            json.loads((r.run / "reviews" / f"{rid}.cost.json").read_text())["attempts"]
            == 1
        )
        assert r.js(f"reviews/{rid}.meta.json")["attempt"] == 1


def test_reask_rejected_when_findings_differ(sandbox):  # noqa: F811
    r = run_panel(sandbox, env=dict(EMBER_MISSING, FAKE_REPAIR_EDIT="1"))
    assert r.rc == 0, r.err
    assert kinds(r, EMBER_MODEL) == ["review", "repair"]
    rec = r.js(f"reviews/{EMBER}.reask.json")
    assert (rec["asked"], rec["accepted"], rec["reason"]) == (
        True,
        False,
        "findings_differ",
    )
    assert not (r.run / "reviews" / f"{EMBER}.preask.md").exists()  # the original stays
    assert (r.run / "reviews" / f"{EMBER}.md").read_text() == (
        r.run / "reviews" / f"{EMBER}.attempt1.md"
    ).read_text()
    check = r.js("check/check.json")
    assert (
        check["ledger_missing"] == [EMBER]
        and check["reask"][EMBER]["accepted"] is False
    )
    assert r.js(f"check/{EMBER}.ledger.json")["via_reask"] is False
    assert r.js("run.json")["reask"] == [EMBER]


def test_no_reask_when_clock_too_late(sandbox):  # noqa: F811
    r = run_panel(sandbox, b="1", env=EMBER_MISSING)  # now + 30 s is above 1.35 s
    assert r.rc == 0, r.err
    assert kinds(r, EMBER_MODEL) == ["review"]
    rec = r.js(f"reviews/{EMBER}.reask.json")
    assert (rec["allowed"], rec["asked"], rec["reason"]) == (False, False, "too_late")
    assert r.js("run.json")["reask"] == []
    assert r.js("check/check.json")["ledger_missing"] == [EMBER]


def test_luna_ledger_missing_is_not_reasked(sandbox):  # noqa: F811
    r = run_panel(
        sandbox,
        b="1000",
        env={"FAKE_SCENARIO_BY_MODEL": f"{LUNA_MODEL}=ledger_missing"},
    )
    assert r.rc == 0, r.err
    assert [c[3] for c in r.calls] == ["review"] * 3  # whatever the clock says
    assert sorted(r.js("check/check.json")["ledger_missing"]) == sorted([L1, L2])
    assert (
        not list((r.run / "reviews").glob(f"{L1}.reask*"))
        and r.js("run.json")["reask"] == []
    )


def test_reask_failure_keeps_original_report(sandbox):  # noqa: F811
    r = run_panel(sandbox, env=dict(EMBER_MISSING, RL_FORCE_EXC="reask"))
    assert r.rc == 0, r.err
    assert kinds(r, EMBER_MODEL) == ["review"]  # it raised before the call
    rec = r.js(f"reviews/{EMBER}.reask.json")
    assert rec["accepted"] is False and rec["reason"] == "error:RuntimeError"
    assert (r.run / "reviews" / f"{EMBER}.md").read_text() == (
        r.run / "reviews" / f"{EMBER}.attempt1.md"
    ).read_text()
    assert r.js("check/check.json")["ledger_missing"] == [EMBER]
    assert (
        r.js("run.json")["merge_refused"] is False
        and (r.run / "merged" / "merged-1.md").is_file()
    )


def test_repaired_rows_never_promoted(sandbox):  # noqa: F811
    r = run_panel(
        sandbox,
        env=dict(EMBER_MISSING, FAKE_REPAIR_PROBLEM="1", FAKE_CAND=str(sandbox.cand)),
    )
    assert r.rc == 0, r.err
    led = r.js(f"check/{EMBER}.ledger.json")
    row = led["rows"][0]
    assert (
        row["verdict"] == "PROBLEM"
        and row["quote_plan_ok"]
        and led["via_reask"] is True
    )
    assert r.js("check/check.json")["promoted"] == 0 and led["promoted"] == []
    # the same run without --via-reask would have promoted that row: the rule is what stops it
    copy = sandbox.root / "control"
    shutil.copytree(r.run, copy, dirs_exist_ok=True)
    args = [
        "check",
        "--run",
        str(copy),
        "--candidate",
        str(sandbox.cand),
        "--source",
        str(sandbox.source),
    ]
    assert cli.main(args) == 0
    assert json.loads((copy / "check" / "check.json").read_text())["promoted"] == 1
    shutil.rmtree(copy)


# ---------------------------------------------------------------- REQ-30, failures


def test_sleeping_reviewer_killed(killed_run):
    r = killed_run
    assert r.rc == 0, r.err
    assert r.wall < 30  # the guard (3 s) ended it, not the 60 s sleep
    run = r.js("run.json")
    assert (run["reviewers"][EMBER]["status"], run["reviewers"][EMBER]["killed"]) == (
        "killed",
        True,
    )
    assert [run["reviewers"][x]["status"] for x in (L1, L2)] == ["ok", "ok"]
    assert r.js(f"reviews/{EMBER}.meta.json")["hang_s"] == 3.0
    assert 2 < r.js("timing.json")["slowest_reviewer_s"] < 15


def test_killed_reviewer_absent_from_merge(killed_run):
    r = killed_run
    mi = r.js("merged/merge-input.json")
    assert mi["absent"] == {EMBER: "killed"} and sorted(mi["used"]) == sorted([L1, L2])
    assert sorted(
        x["reviewer_id"] for x in r.js("resolution.json")["reviewers"]
    ) == sorted([L1, L2])
    assert not (r.run / "normalised" / f"{EMBER}.md").exists()
    merged = (r.run / "merged" / "merged-1.md").read_text()
    assert f"- {L1}: report" in merged and f"- {EMBER}: report" not in merged
    assert [
        x["reviewer_id"] for x in r.js("merged/ledger.json")["rounds"][0]["reviewers"]
    ].count(EMBER) == 0
    assert r.js("run.json")["reviewers"][EMBER]["merged"] is False


@pytest.mark.parametrize(
    ("scenario", "status"),
    [("api_error", "error"), ("wrong_model", "invalid"), ("exit127", "error")],
)
def test_no_retry_on_failure(sandbox, scenario, status):  # noqa: F811
    r = run_panel(sandbox, env={"FAKE_SCENARIO_BY_MODEL": f"{EMBER_MODEL}={scenario}"})
    assert r.rc == 0, r.err
    assert [c[3] for c in r.calls] == [
        "review"
    ] * 3  # one call per reviewer, no retry, no re-ask
    assert sorted(c[2] for c in r.calls) == sorted(
        [EMBER_MODEL, LUNA_MODEL, LUNA_MODEL]
    )
    run = r.js("run.json")
    assert run["reviewers"][EMBER]["status"] == status and run["retries"] == 0
    assert r.js("merged/merge-input.json")["absent"] == {EMBER: status}
    # the classes that lived only in the ember (C4 is also luna 2's)
    assert r.js("check/check.json")["classes_lost"] == {EMBER: ["C5", "C6", "C8"]}


def test_no_budget_exits_3(sandbox):  # noqa: F811
    r = run_panel(
        sandbox, extra=["--b-min", "1"]
    )  # REQ-26: the cap is below the number of recipes
    assert r.rc == 3 and "no_budget" in r.err
    assert r.calls == []
    assert json.loads((r.run / "run.json").read_text())["no_budget"] is True


# ---------------------------------------------------------------- the other arms, dry run, refusals


def test_arms_run_through_the_same_script(sandbox):  # noqa: F811
    doc = {
        "cand_sb": str(sandbox.cand),
        "sha": hashlib.sha256(sandbox.cand.read_bytes()).hexdigest(),
    }
    z0 = briefs.render("Z0", doc, None, str(sandbox.source))["text"]
    expected = {
        "Z0": z0,
        "K": z0
        + briefs.SEPARATOR
        + briefs.k_paragraph(),  # K adds only the copied K paragraph
        "Z0-raw": briefs.render("Z0-raw", doc, None, str(sandbox.source))["text"],
    }
    for arm, text in expected.items():
        r = run_panel(sandbox, arm=arm)
        assert r.rc == 0, (arm, r.err)
        assert len(r.calls) == 3 and {c[3] for c in r.calls} == {"review"}
        for rid in (EMBER, L1, L2):
            assert (r.run / "briefs" / f"{rid}.txt").read_text() == text
        run = r.js("run.json")
        assert (
            run["fallback"] is False
            and run["check_ran"] is False
            and run["check_skipped"] is False
        )
        assert run["z0_sha256"] == hashlib.sha256(z0.encode()).hexdigest()
        assert not (r.run / "lens").exists() and not (r.run / "check").exists()
        assert run["sandbox"].endswith("/repo-raw" if arm == "Z0-raw" else "/repo")
        timing = r.js("timing.json")
        assert timing["render_s"] == 0 and timing["check_s"] == 0
        assert timing["panel_elapsed_s"] == round(
            max(timing["rev_end"].values()) - timing["t0"], 3
        )
        assert (r.run / "merged" / "merged-1.md").is_file()
    assert "R-C" not in expected["K"] and "Driving document:" not in expected["Z0-raw"]


def test_z0_raw_reviewer_runs_in_the_raw_sandbox(sandbox, tmp_path):  # noqa: F811
    spy = tmp_path / "spy"
    spy.mkdir()
    out = tmp_path / "cwd.out"
    (spy / "claude").write_text(
        f'#!/usr/bin/env bash\npwd >>{out}\nexec {SW}/tests/fakes/claude "$@"\n'
    )
    (spy / "claude").chmod(0o755)
    r = run_panel(sandbox, arm="Z0-raw")
    assert r.rc == 0
    e = dict(
        r.env,
        PATH=f"{spy}{os.pathsep}{r.env['PATH']}",
        FAKE_CALL_LOG=str(tmp_path / "log"),
    )
    cmd = [*r.cmd]
    cmd[cmd.index("--run-id") + 1] = "spied"
    p = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=120)
    assert p.returncode == 0, p.stderr
    assert set(out.read_text().split()) == {str(sandbox.sb / sandbox.doc / "repo-raw")}


def test_no_source_drops_c2():
    root = new_root()
    try:
        box = make_sandbox(root, source=False)
        r = run_panel(box)
        assert r.rc == 0, r.err
        run = r.js("run.json")
        assert (run["no_source"], run["c2_not_applicable"]) == (True, True) and run[
            "source_sha256"
        ] is None
        for rid in (EMBER, L1, L2):
            text = (r.run / "briefs" / f"{rid}.txt").read_text()
            assert "Driving document:" not in text and "R-C2." not in text
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_dry_run_writes_the_briefs_and_starts_nothing(sandbox):  # noqa: F811
    r = run_panel(sandbox, extra=["--dry-run"])
    assert r.rc == 0, r.err
    assert r.calls == [] and not (r.run / "reviews").exists()
    for name in ("run.json", "briefs", "lens"):
        assert (r.run / name).exists()
    lines = [ln for ln in r.out.splitlines() if "claude -p" in ln]
    assert len(lines) == 3
    for ln in lines:
        rid = next(x for x in (EMBER, L1, L2) if f"# {x} brief" in ln)
        assert (r.run / "briefs" / f"{rid}.sha256").read_text().strip() in ln
        assert (
            "--disallowedTools Edit Write NotebookEdit" in ln
            and str(sandbox.repo) in ln
        )
    assert r.js("run.json")["dry_run"] is True and not (r.run / "timing.json").exists()


def test_refusals_and_usage_errors(sandbox):  # noqa: F811
    r = run_panel(sandbox, drop=("NOFALLBACK",))
    assert r.rc == 4 and "NOFALLBACK" in r.err and r.calls == [] and not r.run.exists()
    r = run_panel(sandbox, env={"SW_SB_ROOT": "/tmp/evalsb-sweep"})
    assert r.rc == 4 and "E_SIBLING_ROOT" in r.err and not r.run.exists()
    assert run_panel(sandbox, arm="RLx").rc == 2
    assert run_panel(sandbox, b="soon").rc == 2
    r = run_panel(sandbox, env={"RL_FORCE_EXC": "bogus"})
    assert r.rc == 2 and "E_HOOK" in r.err
    r = run_panel(sandbox)
    again = [*r.cmd]
    p = subprocess.run(again, capture_output=True, text=True, env=r.env)
    assert (
        p.returncode == 2 and "E_RUN_EXISTS" in p.stderr
    )  # a run folder is never overwritten
    assert calls(r.log) == r.calls  # and the second call started nothing
    assert SCRIPT.is_file()
