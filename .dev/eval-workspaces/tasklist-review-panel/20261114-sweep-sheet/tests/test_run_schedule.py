"""REQ-29, REQ-32, REQ-17, DESIGN 11.6: the schedule maker, the schedule runner and the spike script.
Every panel run goes to the fake claude (tmp_roots puts tests/fakes first on PATH and the scripts refuse to run otherwise)."""

import importlib.util
import json
import subprocess
import sys

import pytest
from helpers import REPO, SW, sh
from panel_support import DOC_ID, call_log, make_world

from scaffold import clock

MAKE = SW / "bin" / "make-schedule.py"
RUN_SCHEDULE = SW / "bin" / "run-schedule.sh"
RUN_SPIKE = SW / "bin" / "run-spike.sh"
HO = "HO-1,HO-2,HO-3,HO-4"


def make(*args):
    return subprocess.run(
        [sys.executable, "-I", "-B", str(MAKE), *map(str, args)],
        capture_output=True,
        text=True,
    )


def rows_of(path):
    lines = path.read_text().splitlines()
    assert lines[0].startswith("# make-schedule seed=")
    cols = lines[1].split("\t")
    return [dict(zip(cols, ln.split("\t"))) for ln in lines[2:]]


def module():
    spec = importlib.util.spec_from_file_location("make_schedule", MAKE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# --- make-schedule.py ------------------------------------------------------------------------------------------------------


def test_stage_1_has_60_rows_and_the_z0_raw_append_adds_15(tmp_path):
    out = tmp_path / "schedule.tsv"
    r = make(
        "--stage",
        1,
        "--arms",
        "z0,k,ss",
        "--docs",
        HO,
        "--reps",
        5,
        "--seed",
        20261115,
        "--out",
        out,
    )
    assert r.returncode == 0 and "60 rows" in r.stdout, r.stderr
    assert len(rows_of(out)) == 60
    r = make(
        "--stage",
        1,
        "--arms",
        "z0raw",
        "--docs",
        "HO-1,HO-2,HO-3",
        "--reps",
        5,
        "--seed",
        20261115,
        "--append",
        out,
    )
    assert r.returncode == 0 and "75 rows" in r.stdout, r.stderr
    rows = rows_of(out)
    assert len(rows) == 75
    assert sum(r["arm"] == "Z0-raw" for r in rows) == 15
    # one block per replicate: 5 blocks of 12 + 3 rows; the Z0-raw rows are in the blocks of the Z0 rows they compare with
    for block in range(1, 6):
        in_block = [r for r in rows if r["block"] == str(block)]
        assert len(in_block) == 15 and {r["replicate"] for r in in_block} == {
            str(block)
        }
        assert {(r["arm"], r["doc"]) for r in in_block} >= {
            (a, d) for a in ("Z0", "K", "SS") for d in HO.split(",")
        }
    blocks = [int(r["block"]) for r in rows]
    assert blocks == sorted(
        blocks
    )  # a block is finished in the file before the next starts
    assert len({r["run"] for r in rows}) == 75 and rows[0]["seed"] == "20261115"
    assert {r["set"] for r in rows} == {"holdout"} and {r["panel"] for r in rows} == {
        "primary"
    }


def test_same_seed_same_file_and_other_seed_other_order(tmp_path):
    a, b, c = (tmp_path / n for n in ("a.tsv", "b.tsv", "c.tsv"))
    args = ["--stage", 1, "--arms", "z0,k,ss", "--docs", HO, "--reps", 5]
    assert make(*args, "--seed", 7, "--out", a).returncode == 0
    assert make(*args, "--seed", 7, "--out", b).returncode == 0
    assert make(*args, "--seed", 8, "--out", c).returncode == 0
    assert a.read_text() == b.read_text() != c.read_text()
    assert sorted(r["run"] for r in rows_of(a)) == sorted(
        r["run"] for r in rows_of(c)
    )  # the same runs, in another order
    # the seed is recorded in the file, and in every row (the pre-pass seed that run-panel.sh records)
    assert a.read_text().startswith("# make-schedule seed=7\n") and {
        r["seed"] for r in rows_of(a)
    } == {"7"}
    # the order inside a block is shuffled: not the same arm order in every block
    orders = {
        tuple(r["arm"] for r in rows_of(a) if r["block"] == str(k)) for k in range(1, 6)
    }
    assert len(orders) > 1
    # repeating the same command is a no-op; a different schedule never replaces a file
    assert make(*args, "--seed", 7, "--out", a).returncode == 0
    r = make(*args, "--seed", 9, "--out", a)
    assert r.returncode == 2 and "never replaced" in r.stderr


def test_append_and_arguments_are_checked(tmp_path):
    out = tmp_path / "s.tsv"
    base = ["--stage", 1, "--docs", "HO-1", "--reps", 2, "--seed", 5]
    assert make(*base, "--arms", "z0", "--out", out).returncode == 0
    for args, text in (
        ([*base, "--arms", "z0", "--append", out], "already in the schedule"),
        (
            [
                "--stage",
                1,
                "--docs",
                "HO-1",
                "--reps",
                2,
                "--seed",
                6,
                "--arms",
                "k",
                "--append",
                out,
            ],
            "one seed",
        ),
        ([*base, "--arms", "x9", "--out", tmp_path / "t.tsv"], "unknown arm"),
        (
            [*base, "--arms", "z0", "--out", "/var/tmp/sw-schedule-refused.tsv"],
            "E_NOT_WRITABLE",
        ),
        (
            [
                "--stage",
                1,
                "--docs",
                "bad/doc",
                "--reps",
                2,
                "--seed",
                5,
                "--arms",
                "z0",
                "--out",
                tmp_path / "u.tsv",
            ],
            "bad document",
        ),
    ):
        r = make(*args)
        assert r.returncode == 2 and text in r.stderr, (args, r.stderr)
    assert (
        make(*base, "--arms", "k", "--append", out).returncode == 0
        and len(rows_of(out)) == 4
    )
    not_a_schedule = tmp_path / "plain.txt"
    not_a_schedule.write_text("hello\n")
    r = make(*base, "--arms", "k", "--append", not_a_schedule)
    assert r.returncode == 2 and "not a schedule" in r.stderr


def test_run_ids_name_arm_panel_document_and_replicate():
    m = module()
    assert m.run_id("1", "Z0-raw", "primary", "HO-1", 3) == "s1-z0raw-HO-1-r3"
    assert m.run_id("2", "SS", "haiku", "HO-2", 1) == "s2-ss-haiku-HO-2-r1"


# --- run-schedule.sh and run-spike.sh against the fake claude ----------------------------------------------------------------


def with_spike(world, tmp_path, spike, name="values-spike.json"):
    """A copy of the world's values file with (or without) a `spike` record."""
    v = json.loads(world.values.read_text())
    v.pop("spike", None)
    if spike is not None:
        v["spike"] = spike
    p = tmp_path / name
    p.write_text(json.dumps(v))
    return p


def schedule(tmp_path, arms="z0,ss", reps=2, doc=DOC_ID, name="schedule.tsv"):
    out = tmp_path / name
    r = make(
        "--stage",
        1,
        "--arms",
        arms,
        "--docs",
        doc,
        "--reps",
        reps,
        "--seed",
        11,
        "--out",
        out,
    )
    assert r.returncode == 0, r.stderr
    return out


def run_schedule(world, tmp_path, values, sched, *extra, env=None):
    cmd = [
        "bash",
        str(RUN_SCHEDULE),
        str(sched),
        "--runs-root",
        str(tmp_path / "runs-s"),
        "--values",
        str(values),
    ]
    cmd += ["--packages", str(world.packages), *map(str, extra)]
    e = world.roots.with_env(SW_SRC_REPO=str(world.repo), **(env or {}))
    return subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=600)


def test_refuses_without_spike_record(tmp_roots):
    w = make_world(tmp_roots)
    t = tmp_roots.root
    sched = schedule(t)
    for bad in (
        None,
        {"runs": 4, "c_luna": 2.0},
        {"runs": 5},
        {"runs": 5, "c_luna": "fast"},
        {"runs": True, "c_luna": 2.0},
    ):
        r = run_schedule(w, t, with_spike(w, t, bad), sched)
        assert r.returncode == 2 and "E_NO_SPIKE" in r.stderr, (bad, r.stderr)
        assert (
            not (t / "runs-s").exists() and call_log(tmp_roots) == []
        )  # nothing was started or written
    # with a record of 5 runs and a c_luna it starts: 4 runs of 3 reviewers each
    ok = with_spike(w, t, {"runs": 5, "c_luna": 2.0})
    r = run_schedule(w, t, ok, sched)
    assert r.returncode == 0, r.stdout + r.stderr
    summary = json.loads((t / "runs-s" / "schedule-run.json").read_text())
    assert (
        len(summary["started"]) == 4
        and summary["failed"] == []
        and summary["spike_fallback"] is False
    )
    assert len(call_log(tmp_roots)) == 12
    for name in summary["started"]:
        assert (t / "runs-s" / name / "run.json").is_file()
    # no fallback: the panel file in use holds the caps of config/panels.json (8, 8, 8)
    panels = json.loads((t / "runs-s" / "panels-in-use.json").read_text())["panels"][
        "primary"
    ]
    assert (panels["S"]["cap"], panels["L1"]["cap"], panels["L2"]["cap"]) == (8, 8, 8)
    ss = next(n for n in summary["started"] if "-ss-" in n)
    assert json.loads((t / "runs-s" / ss / "prepass" / "assignment.json").read_text())[
        "caps"
    ] == {"t2b-1": 8, "t4-1": 8, "t3-1": 8}


def test_six_item_fallback_when_c_luna_is_above_the_break_even(tmp_roots):
    w = make_world(tmp_roots)
    t = tmp_roots.root
    base = (SW / "config" / "panels.json").read_bytes()
    sched = schedule(t, arms="ss", reps=1)
    # 2.75 s is the break-even at b = 100 (n = 8): exactly 2.75 is not above it, 2.8 is
    r = run_schedule(w, t, with_spike(w, t, {"runs": 5, "c_luna": 2.75}), sched)
    assert (
        r.returncode == 0
        and json.loads((t / "runs-s" / "schedule-run.json").read_text())[
            "spike_fallback"
        ]
        is False
    )
    caps = json.loads((t / "runs-s" / "panels-in-use.json").read_text())["panels"][
        "primary"
    ]
    assert (caps["S"]["cap"], caps["L1"]["cap"]) == (8, 8)
    r = run_schedule(
        w, t, with_spike(w, t, {"runs": 5, "c_luna": 2.8}, "v2.json"), sched
    )
    assert (
        r.returncode == 0
    )  # the run folder exists: skipped, but the panel file is rewritten with the fallback caps
    panels = json.loads((t / "runs-s" / "panels-in-use.json").read_text())["panels"]
    for (
        name,
        p,
    ) in (
        panels.items()
    ):  # every panel: each luna 6, the search reviewer takes the rest of the 24
        assert (p["S"]["cap"], p["L1"]["cap"], p["L2"]["cap"]) == (12, 6, 6), name
    assert (
        json.loads((t / "runs-s" / "schedule-run.json").read_text())["spike_fallback"]
        is True
    )
    assert (
        SW / "config" / "panels.json"
    ).read_bytes() == base  # config/panels.json itself is never changed


def test_fallback_caps_reach_the_assignment(tmp_roots):
    w = make_world(tmp_roots)
    t = tmp_roots.root
    r = run_schedule(
        w,
        t,
        with_spike(w, t, {"runs": 5, "c_luna": 3.4}),
        schedule(t, arms="ss", reps=1),
    )
    assert r.returncode == 0, r.stdout + r.stderr
    name = json.loads((t / "runs-s" / "schedule-run.json").read_text())["started"][0]
    asg = json.loads((t / "runs-s" / name / "prepass" / "assignment.json").read_text())
    assert asg["caps"] == {"t2b-1": 12, "t4-1": 6, "t3-1": 6}
    assert all(load <= asg["caps"][rid] for rid, load in asg["loads"].items())
    assert asg["loads"]["t4-1"] <= 6 and asg["loads"]["t3-1"] <= 6


def test_at_most_3_panels_at_once_and_a_started_run_is_not_repeated(tmp_roots):
    w = make_world(tmp_roots)
    t = tmp_roots.root
    ok = with_spike(w, t, {"runs": 5, "c_luna": 2.0})
    sched = schedule(t, arms="z0", reps=6)
    r = run_schedule(w, t, ok, sched, "--jobs", 4)
    assert r.returncode == 2 and "E_JOBS" in r.stderr and not (t / "runs-s").exists()
    r = run_schedule(w, t, ok, sched, "--jobs", 3)
    assert r.returncode == 0, r.stdout + r.stderr
    summary = json.loads((t / "runs-s" / "schedule-run.json").read_text())
    assert len(summary["started"]) == 6 and 2 <= summary["max_concurrent"] <= 3
    seen = [
        json.loads((t / "runs-s" / n / "run.json").read_text())[
            "concurrent_panels_at_start"
        ]
        for n in summary["started"]
    ]
    assert all(1 <= c <= 3 for c in seen) and max(seen) == summary["max_concurrent"]
    assert [
        json.loads((t / "runs-s" / n / "run.json").read_text())["block"]
        for n in summary["started"]
    ].count(None) == 0
    calls = len(call_log(tmp_roots))
    again = run_schedule(w, t, ok, sched)
    assert again.returncode == 0 and "started=0 skipped=6" in again.stdout
    assert len(call_log(tmp_roots)) == calls  # a counted run is never repeated
    one = run_schedule(
        w, t, ok, schedule(t, arms="k", reps=2, name="k.tsv"), "--jobs", 1
    )
    assert (
        one.returncode == 0
        and json.loads((t / "runs-s" / "schedule-run.json").read_text())[
            "max_concurrent"
        ]
        == 1
    )


def test_a_failed_run_is_reported_and_the_rest_still_run(tmp_roots):
    w = make_world(tmp_roots)
    t = tmp_roots.root
    out = t / "mixed.tsv"
    assert (
        make(
            "--stage",
            1,
            "--arms",
            "z0",
            "--docs",
            f"{DOC_ID},no-such-doc",
            "--reps",
            1,
            "--seed",
            3,
            "--out",
            out,
        ).returncode
        == 0
    )
    r = run_schedule(w, t, with_spike(w, t, {"runs": 5, "c_luna": 2.0}), out)
    assert r.returncode == 1 and "failed=1" in r.stdout
    summary = json.loads((t / "runs-s" / "schedule-run.json").read_text())
    assert len(summary["started"]) == 2 and [
        f.split(":")[0] for f in summary["failed"]
    ] == ["s1-z0-no-such-doc-r1"]
    assert (
        t / "runs-s" / "s1-z0-TASK-WF-fixture-20261114-000001-r1" / "run.json"
    ).is_file()


def test_bad_schedule_and_missing_nofallback_are_refused(tmp_roots, tmp_path):
    w = make_world(tmp_roots)
    t = tmp_roots.root
    ok = with_spike(w, t, {"runs": 5, "c_luna": 2.0})
    plain = t / "plain.tsv"
    plain.write_text("a\tb\n")
    r = run_schedule(w, t, ok, plain)
    assert r.returncode == 2 and "not a schedule" in r.stderr
    r = run_schedule(w, t, ok, t / "missing.tsv")
    assert r.returncode == 2 and "no schedule file" in r.stderr
    env = {k: v for k, v in w.roots.with_env().items() if k != "NOFALLBACK"}
    r = subprocess.run(
        ["bash", str(RUN_SCHEDULE), str(schedule(t))],
        capture_output=True,
        text=True,
        env=env,
    )
    assert r.returncode == 2 and "NOFALLBACK" in r.stderr


def test_spike_timing_writes_the_record(tmp_roots):
    w = make_world(tmp_roots)
    t = tmp_roots.root
    vals = with_spike(w, t, None)
    root = t / "spike"
    cmd = [
        "bash",
        str(RUN_SPIKE),
        "timing",
        "--panel",
        "ember",
        "--doc",
        DOC_ID,
        "--runs",
        2,
        "--baseline-runs",
        2,
    ]
    cmd += [
        "--item-count",
        8,
        "--runs-root",
        str(root),
        "--values",
        str(vals),
        "--packages",
        str(w.packages),
    ]
    r = subprocess.run(
        list(map(str, cmd)),
        capture_output=True,
        text=True,
        env=w.roots.with_env(SW_SRC_REPO=str(w.repo)),
        timeout=600,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    rec = json.loads(vals.read_text())["spike"]
    assert (
        rec["runs"],
        rec["baseline_runs"],
        rec["item_count"],
        rec["panel"],
        rec["doc"],
    ) == (2, 2, 8, "primary", DOC_ID)

    def luna(prefix):
        out = []
        for k in (1, 2):
            reviews = root / "spike-timing" / f"{prefix}-{k}" / "reviews"
            for f in sorted(reviews.glob("*.meta.json")):
                if (
                    ".attempt" in f.name
                ):  # <rid>.meta.json is the copy of <rid>.attempt1.meta.json
                    continue
                m = json.loads(f.read_text())
                if m["expected_model"] == "gpt-6-luna":
                    out.append(m["wall_s"])
        return sorted(out)

    def med(xs):
        n = len(xs)
        return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2

    ss, z0 = luna("ss"), luna("z0")
    assert len(ss) == len(z0) == 4  # two luna reviewers in each of two runs
    assert rec["median_ss_s"] == pytest.approx(med(ss)) and rec[
        "median_z0_s"
    ] == pytest.approx(med(z0))
    assert rec["c_luna"] == pytest.approx(
        (med(ss) - med(z0) - 3) / 8, abs=1e-3
    )  # the formula of DESIGN 14.2
    # 2 runs are not the 5 that REQ-32 needs: the schedule refuses to start on this record
    r = run_schedule(w, t, vals, schedule(t, arms="z0", reps=1))
    assert r.returncode == 2 and "E_NO_SPIKE" in r.stderr
    # a SS block and a Z0 block of the same number are the same day: block k holds ss-k and z0-k
    assert (
        json.loads((root / "spike-timing" / "ss-2" / "run.json").read_text())["block"]
        == 2
    )
    assert (
        json.loads((root / "spike-timing" / "z0-2" / "run.json").read_text())["block"]
        == 2
    )


@pytest.mark.slow
def test_spike_with_five_runs_lets_the_schedule_start(tmp_roots):
    w = make_world(tmp_roots)
    t = tmp_roots.root
    vals = with_spike(w, t, None)
    cmd = [
        "bash",
        str(RUN_SPIKE),
        "timing",
        "--panel",
        "ember",
        "--doc",
        DOC_ID,
        "--runs",
        "5",
        "--baseline-runs",
        "5",
    ]
    cmd += [
        "--runs-root",
        str(t / "spike"),
        "--values",
        str(vals),
        "--packages",
        str(w.packages),
    ]
    r = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=w.roots.with_env(SW_SRC_REPO=str(w.repo)),
        timeout=900,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    rec = json.loads(vals.read_text())["spike"]
    assert (rec["runs"], rec["baseline_runs"]) == (5, 5) and isinstance(
        rec["c_luna"], float
    )
    r = run_schedule(w, t, vals, schedule(t, arms="z0", reps=1))
    assert r.returncode == 0, (
        r.stdout + r.stderr
    )  # the record is complete: the schedule starts


def test_spike_compliance_go_and_no_go(tmp_roots):
    w = make_world(tmp_roots)
    t = tmp_roots.root

    def run(scenario, root):
        cmd = [
            "bash",
            str(RUN_SPIKE),
            "compliance",
            "--panel",
            "ember",
            "--doc",
            DOC_ID,
            "--runs",
            "2",
        ]
        cmd += [
            "--runs-root",
            str(root),
            "--values",
            str(w.values),
            "--packages",
            str(w.packages),
        ]
        e = w.roots.with_env(SW_SRC_REPO=str(w.repo), FAKE_SCENARIO=scenario)
        return subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=600)

    good = run("ok", t / "good")
    assert good.returncode == 0, good.stdout + good.stderr
    c = json.loads((t / "good" / "spike-compliance" / "compliance.json").read_text())
    assert (c["runs"], c["reviewers_checked"], c["ledger_missing"], c["go"]) == (
        2,
        6,
        0,
        True,
    )
    bad = run(
        "ledger_missing", t / "bad"
    )  # no reviewer writes a ledger block: 6 of 6 are missing
    assert bad.returncode == 1
    c = json.loads((t / "bad" / "spike-compliance" / "compliance.json").read_text())
    assert (c["ledger_missing"], c["ledger_missing_rate"], c["go"]) == (6, 1.0, False)


# --- the spike plan and the panel override ---------------------------------------------------------------------------------


def test_spike_plan_and_fallback_panels():
    v = clock.load_values()
    assert (
        clock.spike_plan({**v, "spike": None})["ok"] is False
        and clock.spike_plan(v)["ok"] is False
    )  # no record yet
    p = clock.spike_plan({**v, "spike": {"runs": 5, "c_luna": 2.75}})
    assert (p["ok"], p["fallback"], p["limit_s"], p["luna_items"]) == (
        True,
        False,
        2.75,
        6,
    )
    assert (
        clock.spike_plan({**v, "spike": {"runs": 5, "c_luna": 2.76}})["fallback"]
        is True
    )
    assert clock.spike_plan({**v, "spike": {"runs": 4, "c_luna": 9.0}})["ok"] is False
    panels = json.loads((SW / "config" / "panels.json").read_text())
    fb = clock.fallback_panels(panels)
    for name, p in fb["panels"].items():
        assert (p["S"]["cap"], p["L1"]["cap"], p["L2"]["cap"]) == (12, 6, 6), name
        assert (
            p["S"]["rid"] == panels["panels"][name]["S"]["rid"]
        )  # only the caps change
    assert panels["panels"]["primary"]["S"]["cap"] == 8  # the input is not changed


def test_panels_override_is_judged_by_its_path():
    assert sh("sw_assert_override SW_PANELS /tmp/x/panels.json").returncode == 0
    assert (
        sh('sw_assert_override SW_PANELS "$SW/runs/panels-in-use.json"').returncode == 0
    )
    for bad in (
        f"{REPO}/src/panels.json",
        f"{SW}/config/panels.json",
        "/var/tmp/panels.json",
    ):
        r = sh(f"sw_assert_override SW_PANELS '{bad}'")
        assert r.returncode == 1 and "E_OVERRIDE" in r.stderr, bad
    assert sh("echo reached", {"SW_PANELS": "/tmp/p.json"}).returncode == 0
    assert sh("echo reached", {"SW_PANELS": "/etc/p.json"}).returncode == 1
