"""REQ-29, REQ-32 and the concurrency budget of DESIGN 9.5: the schedule maker, the schedule runner and the spike script.
Every panel run goes to the fake claude (panel_support.base_env puts tests/fakes first on PATH). Run folders go to a
temporary RL_RUNS_ROOT, never to RL/runs. `run-spike.sh` is only ever run without --go: it needs models."""

import importlib.util
import json
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest
from helpers import SW
from panel_support import (
    L1,
    base_env,
    calls,
    sandbox,  # noqa: F401  (session fixture)
)

from rl import lens, spike

MAKE = SW / "bin" / "make-schedule.py"
RUN_SCHEDULE = SW / "bin" / "run-schedule.sh"
RUN_SPIKE = SW / "bin" / "run-spike.sh"
HO = "HO-1,HO-2,HO-3,HO-4"
GOOD_SPIKE = {"runs": 5, "c_luna": 2.0}


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
        *("--stage", 1, "--arms", "z0,k,rl", "--docs", HO, "--reps", 5),
        *("--seed", 20261115, "--out", out),
    )
    assert r.returncode == 0 and "60 rows" in r.stdout, r.stderr
    assert len(rows_of(out)) == 60
    r = make(
        *("--stage", 1, "--arms", "z0raw", "--docs", "HO-1,HO-2,HO-3", "--reps", 5),
        *("--seed", 20261115, "--append", out),
    )
    assert r.returncode == 0 and "75 rows" in r.stdout, r.stderr
    rows = rows_of(out)
    assert len(rows) == 75
    assert sum(r["arm"] == "Z0-raw" for r in rows) == 15
    # one block per replicate: 5 blocks of 12 + 3 rows; the Z0-raw rows sit in the blocks of the Z0 rows they are compared with
    for block in range(1, 6):
        in_block = [r for r in rows if r["block"] == str(block)]
        assert len(in_block) == 15 and {r["replicate"] for r in in_block} == {
            str(block)
        }
        assert {(r["arm"], r["doc"]) for r in in_block} >= {
            (a, d) for a in ("Z0", "K", "RL") for d in HO.split(",")
        }
    blocks = [int(r["block"]) for r in rows]
    assert blocks == sorted(
        blocks
    )  # a block is finished in the file before the next starts
    assert len({r["run"] for r in rows}) == 75
    assert {r["seed"] for r in rows} == {"20261115"}
    assert (
        (tmp_path / "schedule.tsv")
        .read_text()
        .startswith("# make-schedule seed=20261115\n")
    )
    assert {r["set"] for r in rows} == {"holdout"} and {r["panel"] for r in rows} == {
        "primary"
    }
    assert all(
        r["run"].startswith("stage1-") for r in rows
    )  # the prefix of `analyze.py all --stage 1`


def test_same_seed_same_file_and_other_seed_other_order(tmp_path):
    a, b, c = (tmp_path / n for n in ("a.tsv", "b.tsv", "c.tsv"))
    args = ["--stage", 1, "--arms", "z0,k,rl", "--docs", HO, "--reps", 5]
    assert make(*args, "--seed", 7, "--out", a).returncode == 0
    assert make(*args, "--seed", 7, "--out", b).returncode == 0
    assert make(*args, "--seed", 8, "--out", c).returncode == 0
    assert a.read_text() == b.read_text() != c.read_text()
    assert sorted(r["run"] for r in rows_of(a)) == sorted(r["run"] for r in rows_of(c))
    assert a.read_text().startswith("# make-schedule seed=7\n")
    assert {r["seed"] for r in rows_of(a)} == {"7"}
    # the order inside a block is shuffled: not the same arm order in every block
    orders = {
        tuple(r["arm"] for r in rows_of(a) if r["block"] == str(k)) for k in range(1, 6)
    }
    assert len(orders) > 1
    # repeating the command is a no-op; a different schedule never replaces a file
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
        ([*base, "--arms", "ss", "--out", tmp_path / "t.tsv"], "unknown arm"),
        (
            [*base, "--arms", "z0", "--out", "/var/tmp/rl-schedule-refused.tsv"],
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
    assert make(*base, "--arms", "k", "--append", out).returncode == 0
    assert len(rows_of(out)) == 4
    plain = tmp_path / "plain.txt"
    plain.write_text("hello\n")
    r = make(*base, "--arms", "k", "--append", plain)
    assert r.returncode == 2 and "not a schedule" in r.stderr


def test_set_and_panel_are_recorded_and_named_in_the_run(tmp_path):
    m = module()
    assert m.run_id("1", "Z0-raw", "primary", "HO-1", 3) == "stage1-z0raw-HO-1-r3"
    assert m.run_id("2", "RL", "haiku", "HO-2", 1) == "stage2-rl-haiku-HO-2-r1"
    out = tmp_path / "s2.tsv"
    r = make(
        *(
            "--stage",
            2,
            "--set",
            "holdout4",
            "--panel",
            "haiku",
            "--arms",
            "z0,rl",
            "--docs",
            HO,
            "--reps",
            3,
        ),
        *("--seed", 1, "--out", out),
    )
    assert r.returncode == 0 and "24 rows" in r.stdout, r.stderr
    rows = rows_of(out)
    assert {r["set"] for r in rows} == {"holdout4"} and {r["panel"] for r in rows} == {
        "haiku"
    }


# --- the timing spike record -------------------------------------------------------------------------------------------------


def fake_run(path, wall_s=None, rows=None, status="ok", rid=L1):
    (path / "reviews").mkdir(parents=True)
    (path / "check").mkdir()
    meta = {"status": status, "wall_s": wall_s}
    (path / "reviews" / f"{rid}.meta.json").write_text(json.dumps(meta))
    if rows is not None:
        (path / "check" / "check.json").write_text(
            json.dumps({"rows_per_reviewer": {rid: rows}})
        )
    return path


def test_spike_record_is_the_formula_of_design_12_4(tmp_path):
    rl = [
        fake_run(tmp_path / f"rl{k}", w, 14)
        for k, w in enumerate((110, 120, 118, 200, 112))
    ]
    z0 = [fake_run(tmp_path / f"z{k}", w) for k, w in enumerate((70, 72, 75, 71, 69))]
    killed = fake_run(
        tmp_path / "killed", 500, 14, status="killed"
    )  # a killed run is not a measurement
    rec = spike.timing_record(
        rl + [killed], z0, L1, "HO-6", "primary", date="2026-11-15"
    )
    assert (rec["runs"], rec["baseline_runs"]) == (5, 5)
    assert (rec["median_rl_s"], rec["median_z0_s"], rec["mean_rows"]) == (118, 71, 14)
    assert rec["c_luna"] == round((118 - 71 - 4) / 14, 3) == 3.071
    # the record is stored next to the planning values and never over them
    values = tmp_path / "values.json"
    values.write_text(json.dumps({"c": {"gpt-6-luna": 2}, "row_cap": {"share": 0.35}}))
    spike.write_record(values, rec)
    stored = json.loads(values.read_text())
    assert stored["c"] == {"gpt-6-luna": 2} and stored["spike"] == rec
    # no usable data, or noise (c not above 0), writes no record
    with pytest.raises(spike.SpikeError):
        spike.timing_record([], z0, L1, "HO-6", "primary")
    with pytest.raises(spike.SpikeError):
        spike.timing_record(
            rl, [fake_run(tmp_path / "slow", 500)], L1, "HO-6", "primary"
        )
    r = subprocess.run(
        [
            sys.executable,
            "-I",
            "-B",
            str(SW / "rl" / "spike.py"),
            "timing",
            "--values",
            str(tmp_path / "v2.json"),
            "--rid",
            L1,
            "--doc",
            "HO-6",
            "--panel",
            "primary",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1 and "E_SPIKE_DATA" in r.stderr


# --- run-schedule.sh against the fake claude ---------------------------------------------------------------------------------


def values_with(tmp_path, spike_record, name="values.json"):
    """A copy of config/values.json with (or without) a `spike` record. Under /tmp: the runner accepts no other place."""
    v = json.loads((SW / "config" / "values.json").read_text())
    v.pop("spike", None)
    if spike_record is not None:
        v["spike"] = spike_record
    p = tmp_path / name
    p.write_text(json.dumps(v))
    return p


def schedule(tmp_path, doc, arms="z0", reps=1, name="schedule.tsv"):
    out = tmp_path / name
    r = make(
        *(
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
    )
    assert r.returncode == 0, r.stderr
    return out


def run_schedule(box, tmp_path, values, sched, *extra, env=None, drop=()):
    e = dict(
        base_env(box.root),
        RL_RUNS_ROOT=str(tmp_path / "runs"),
        FAKE_CALL_LOG=str(tmp_path / "calls.log"),
        **(env or {}),
    )
    for k in drop:
        e.pop(k, None)
    cmd = [
        "bash",
        str(RUN_SCHEDULE),
        str(sched),
        "--values",
        str(values),
        *map(str, extra),
    ]
    return subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=600)


def summary(tmp_path):
    return json.loads((tmp_path / "runs" / "schedule-run.json").read_text())


@pytest.mark.slow
def test_refuses_without_spike_record(sandbox, tmp_path):  # noqa: F811
    sched = schedule(tmp_path, sandbox.doc)
    for bad in (
        None,
        {"runs": 4, "c_luna": 2.0},
        {"runs": 5},
        {"runs": 5, "c_luna": "fast"},
        {"runs": 5, "c_luna": 0},
        {"runs": True, "c_luna": 2.0},
        "five",
    ):
        r = run_schedule(sandbox, tmp_path, values_with(tmp_path, bad), sched)
        assert r.returncode == 2 and "E_NO_SPIKE" in r.stderr, (bad, r.stderr)
        # nothing was started or written
        assert not (tmp_path / "runs").exists() and calls(tmp_path / "calls.log") == []
    # While the real planning file holds no record, the default values file refuses too. Since the timing spike of
    # 2026-11-15 wrote a real record into config/values.json, that part is skipped: running the schedule against the
    # real file would then be accepted, and the case above (spike record removed in a temporary copy) covers the refusal.
    if "spike" not in json.loads((SW / "config" / "values.json").read_text()):
        e = dict(base_env(sandbox.root), RL_RUNS_ROOT=str(tmp_path / "runs"))
        r = subprocess.run(
            ["bash", str(RUN_SCHEDULE), str(sched)],
            capture_output=True,
            text=True,
            env=e,
        )
        assert (
            r.returncode == 2
            and "E_NO_SPIKE" in r.stderr
            and not (tmp_path / "runs").exists()
        )
    # a record written by the spike code (5 runs and a c_luna) is accepted: the row whose run folder is
    # already there is skipped, so no panel starts here
    rl = [fake_run(tmp_path / f"rl{k}", 110 + k, 14) for k in range(5)]
    z0 = [fake_run(tmp_path / f"z{k}", 70 + k) for k in range(5)]
    good = values_with(tmp_path, None, "good.json")
    spike.write_record(good, spike.timing_record(rl, z0, L1, "HO-6", "primary"))
    done = rows_of(sched)[0]["run"]
    (tmp_path / "runs" / done).mkdir(parents=True)
    (tmp_path / "runs" / done / "run.json").write_text("{}")
    r = run_schedule(sandbox, tmp_path, good, sched)
    assert r.returncode == 0 and "started=0 skipped=1" in r.stdout, r.stdout + r.stderr
    assert calls(tmp_path / "calls.log") == []
    # NOFALLBACK and the panel count are checked before anything starts
    r = run_schedule(sandbox, tmp_path, good, sched, drop=("NOFALLBACK",))
    assert r.returncode == 2 and "NOFALLBACK" in r.stderr
    r = run_schedule(sandbox, tmp_path, good, sched, "--max-panels", 4)
    assert r.returncode == 2 and "E_JOBS" in r.stderr
    r = run_schedule(sandbox, tmp_path, "/var/tmp/values.json", sched)
    assert r.returncode == 2 and "E_OVERRIDE" in r.stderr


def test_spike_sets_row_cap_formula():
    assert lens.lens_row_cap(100, 2.41, 14) == 12
    assert lens.lens_row_cap(100, 2.50, 14) == 11
    assert lens.lens_row_cap(100, 2.0, 14) == 14  # the planning value: the table cap


@pytest.mark.slow
def test_spike_sets_row_cap(sandbox, tmp_path):  # noqa: F811
    """The runner passes lens_row_cap(b_min, c_luna) into every RL run: c = 2.41 gives 12 luna rows, c = 2.50 gives 11,
    at b = 100 (the smallest b of the primary panel); the ember keeps the table cap and a Z0 run gets no lens."""
    found = {}
    for c, name in ((2.41, "a"), (2.50, "b")):
        out = tmp_path / name
        out.mkdir()
        sched = schedule(out, sandbox.doc, arms="rl,z0", name="s.tsv")
        r = run_schedule(
            sandbox, out, values_with(out, {"runs": 5, "c_luna": c}), sched
        )
        assert r.returncode == 0, r.stdout + r.stderr
        s = summary(out)
        assert len(s["started"]) == 2 and s["failed"] == [] and s["c_luna"] == c
        run = json.loads(
            (out / "runs" / f"stage1-rl-{sandbox.doc}-r1" / "run.json").read_text()
        )
        found[c] = {
            rid: (rev["row_cap"], rev["c"], rev["b"])
            for rid, rev in run["reviewers"].items()
        }
        assert not (out / "runs" / f"stage1-z0-{sandbox.doc}-r1" / "lens").exists()
    luna = {rid for rid, v in found[2.41].items() if v[1] == 2.41}
    assert len(luna) == 2  # both luna reviewers took the measured c
    for rid in luna:
        assert found[2.41][rid] == (12, 2.41, 100) and found[2.5][rid] == (11, 2.5, 100)
    ember = next(rid for rid in found[2.41] if rid not in luna)
    assert (
        found[2.41][ember][0] == found[2.5][ember][0] == 14
    )  # the ember's c is the planning 0.4


@pytest.mark.slow
def test_launcher_c_luna_option_is_backwards_compatible(sandbox, tmp_path):  # noqa: F811
    """run-panel.sh without --c-luna keeps the planning cost (cap 14); with it the cap follows lens_row_cap."""

    def dry(*extra, run_id):
        e = dict(base_env(sandbox.root), RL_RUNS_ROOT=str(tmp_path / "runs"))
        cmd = [
            "bash",
            str(SW / "bin" / "run-panel.sh"),
            "--arm",
            "RL",
            "--panel",
            "primary",
            "--doc",
            sandbox.doc,
            "--replicate",
            "1",
            "--block",
            "1",
            "--seed",
            "1",
            "--run-id",
            run_id,
            "--dry-run",
            *extra,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=120)
        return r, tmp_path / "runs" / run_id

    r, run = dry(run_id="plain")
    assert r.returncode == 0, r.stderr
    assert json.loads((run / "lens" / f"{L1}.json").read_text())["row_cap"] == 14
    r, run = dry("--b-min", "100", "--c-luna", "2.41", run_id="c241")
    assert r.returncode == 0, r.stderr
    info = json.loads((run / "lens" / f"{L1}.json").read_text())
    assert (info["row_cap"], info["c"], info["b"]) == (12, 2.41, 100)
    r, _ = dry("--c-luna", "0", run_id="c0")
    assert r.returncode == 2 and "usage" in r.stderr


# --- concurrency (DESIGN 9.5) ------------------------------------------------------------------------------------------------


def alive_reviewers(marker: bytes) -> int:
    """Fake-claude reviewer processes of this test alive now. They are found by their command line (`bash .../claude`)
    and by the unique FAKE_CALL_LOG in their environment; a forked subshell of one is not counted twice."""
    procs = {}
    for p in Path("/proc").iterdir():
        if not p.name.isdigit():
            continue
        try:
            argv = (p / "cmdline").read_bytes().split(b"\0")
            if len(argv) < 2 or not argv[1].endswith(b"tests/fakes/claude"):
                continue
            if marker not in (p / "environ").read_bytes().split(b"\0"):
                continue
            procs[int(p.name)] = int(
                (p / "stat").read_text().rsplit(")", 1)[1].split()[1]
            )
        except (OSError, ValueError, IndexError):
            continue
    return sum(1 for ppid in procs.values() if ppid not in procs)


def run_sampled(sandbox, tmp_path, panels, *extra):  # noqa: F811
    """Run a schedule of `panels` Z0 panels whose reviewers sleep 6 s, sampling the live reviewer count every 20 ms."""
    sched = schedule(tmp_path, sandbox.doc, arms="z0", reps=panels)
    log = tmp_path / "calls.log"
    e = dict(
        base_env(sandbox.root),
        RL_RUNS_ROOT=str(tmp_path / "runs"),
        FAKE_CALL_LOG=str(log),
        FAKE_SCENARIO="sleep",
        FAKE_SLEEP_S="6",
    )
    marker = f"FAKE_CALL_LOG={log}".encode()
    values = values_with(tmp_path, GOOD_SPIKE)
    proc = subprocess.Popen(
        [
            "bash",
            str(RUN_SCHEDULE),
            str(sched),
            "--values",
            str(values),
            *map(str, extra),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=e,
    )
    seen = []
    stop = threading.Event()

    def sample():
        while not stop.is_set():
            seen.append(alive_reviewers(marker))
            time.sleep(0.02)

    t = threading.Thread(target=sample)
    t.start()
    try:
        out, err = proc.communicate(timeout=300)
    finally:
        stop.set()
        t.join()
    assert proc.returncode == 0, out + err
    return max(seen), summary(tmp_path), calls(log)


@pytest.mark.slow
def test_max_panels_default_one(sandbox, tmp_path):  # noqa: F811
    top, s, log = run_sampled(sandbox, tmp_path, 2)
    assert len(s["started"]) == 2 and s["max_panels"] == 1 and s["max_concurrent"] == 1
    assert len(log) == 6  # two panels of three reviewers, none re-run
    assert (
        top == 3
    )  # a panel's own three reviewers are alive together, never more than that


@pytest.mark.slow
def test_max_panels_three_runs_three_at_once(sandbox, tmp_path):  # noqa: F811
    top, s, log = run_sampled(sandbox, tmp_path, 3, "--max-panels", 3)
    assert len(s["started"]) == 3 and s["max_panels"] == 3 and s["max_concurrent"] == 3
    assert len(log) == 9
    assert top == 9  # three panels of three reviewers at once, never ten


# --- run-spike.sh: only the refusal is run; the spikes need models -----------------------------------------------------------


@pytest.mark.parametrize("mode", ["timing", "compliance"])
def test_spike_refuses_without_go_and_starts_nothing(mode, tmp_path):
    e = dict(base_env(tmp_path), FAKE_CALL_LOG=str(tmp_path / "calls.log"))
    r = subprocess.run(
        ["bash", str(RUN_SPIKE), mode, "--doc", "HO-6", "--runs", "5"],
        capture_output=True,
        text=True,
        env=e,
    )
    assert r.returncode != 0 and "needs models" in r.stderr and "--go" in r.stderr
    assert (
        not (tmp_path / "runs").exists() and calls(tmp_path / "calls.log") == []
    )  # no run folder, no claude call
    assert not (tmp_path / "sb").exists()


def test_spike_modes_are_documented_and_a_bad_mode_is_refused(tmp_path):
    e = dict(base_env(tmp_path))
    r = subprocess.run(
        ["bash", str(RUN_SPIKE), "--help"], capture_output=True, text=True, env=e
    )
    assert r.returncode == 0
    for word in (
        "timing",
        "compliance",
        "--go",
        "needs models",
        "c_luna",
        "ledger_missing",
    ):
        assert word in r.stdout, word
    r = subprocess.run(
        ["bash", str(RUN_SPIKE), "bogus", "--go"], capture_output=True, text=True, env=e
    )
    assert r.returncode == 2 and "usage" in r.stderr
