"""bin/run-panel.sh with fake-claude (design 5.1, 5.2, 6.1 test_launcher)."""

import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

import pytest
from r4help import DE, PKGS, R4, fixture, jsonl, make_sbr, r4_copy, run, write_values

RESULT_KEYS = ["schema", "row", "panel", "arm", "panel_collab", "models", "values_sha256", "pins_ok", "seed", "started", "finished",
               "valid", "found_14", "real_blocking_8", "judge_blocking", "wrong_blockers", "control_found_2", "control_wrong_blockers",
               "output_tokens", "elapsed_s", "overhead_pct", "reach", "reach_ids", "packages", "collab", "audit"]

FLAGGER = {"calls": 7, "call_sleep": 0.25,
           "posts": {str(i): {"anchor": f"AUTO:{i - 3}", "move": "M3", "category": "other", "severity": "MAJOR"} for i in range(3, 7)}}
LUNA = {"calls": 10, "call_sleep": 0.45}
FAKE = {"by_rid": {"t2b-1": FLAGGER}, "by_model": {"gpt-6-luna": LUNA, "muse-ember-1.0": {"calls": 3}}, "default": {"calls": 2},
        "judge": {"score": {"gt_covered_any": ["GT1"], "gt_covered_blocking": ["GT1"], "wrong_blockers": 1}}}


def launch(env, row, collab=1, values=None, extra=(), r4=R4, timeout=600):
    e = dict(env, PANEL_COLLAB=str(collab))
    v = values or write_values(env)
    return run([r4 / "bin" / "run-panel.sh", "--panel", "EL2", "--row", row, "--values", v, "--seed", "5", *extra], env=e, timeout=timeout)


def refusals(env):
    return jsonl(Path(env["R4_OUT"]) / "runs" / "refusals.jsonl")


@pytest.fixture
def ready(env, tmp_path):
    make_sbr(env)
    fixture(env, FAKE, tmp_path)
    return env


def test_refusals(ready, tmp_path):
    env = ready
    v = write_values(env)
    cases = []
    e = dict(env)
    e.pop("NOFALLBACK")
    cases.append(("NOFALLBACK", run([R4 / "bin/run-panel.sh", "--panel", "EL2", "--row", "x1", "--values", v], env=dict(e, PANEL_COLLAB="1"))))
    cases.append(("PANEL_COLLAB", run([R4 / "bin/run-panel.sh", "--panel", "EL2", "--row", "x2", "--values", v], env=dict(env, PANEL_COLLAB="2"))))
    cases.append(("unknown panel", run([R4 / "bin/run-panel.sh", "--panel", "XX", "--row", "x3", "--values", v], env=env)))
    bad = v.parent / "bad.json"
    bad.write_text(v.read_text().replace('"k": 2', '"k": 1'))
    (v.parent / "bad.json.sha256").write_text((v.parent / (v.name + ".sha256")).read_text())
    cases.append(("values sha256", launch(env, "x4", values=bad)))
    k0 = write_values(env, B=4.0, name="k0.json")
    cases.append(("k = 0 on every package", launch(env, "x5", values=k0)))
    for want, r in cases:
        assert r.returncode == 2, (want, r.stderr)
        assert want in r.stderr, (want, r.stderr)
    assert len(refusals(env)) == len(cases)
    assert not any((Path(env["R4_OUT"]) / "runs" / f"x{i}").exists() for i in range(1, 6))
    assert not (Path(env["FAKE_LOG"]) / "argv.jsonl").exists()  # no reviewer ever started


@pytest.mark.parametrize("change,want", [
    (lambda p: p["panels"]["EL2"]["adjudicators"][0].update(model="glm-5.3"), "model not allowed"),
    (lambda p: (p["allowed_models"].append("Qwen3.8-max"), p["panels"]["EL2"]["adjudicators"][0].update(model="Qwen3.8-max")), "forbidden model"),
    (lambda p: (p["allowed_models"].append("claude-opus-5-5"), p["panels"]["EL2"]["flagger"].update(model="claude-opus-5-5")), "forbidden model"),
    (lambda p: p["panels"]["EL2"]["flagger"].update(model="gpt-6-luna"), "flagger model is gpt-6-luna"),
    (None, "pins check failed"),
])
def test_refusals_on_copies(ready, tmp_path, change, want):
    c = r4_copy(tmp_path)
    pj = c / "frozen" / "panels.json"
    p = json.loads(pj.read_text())
    if change:
        change(p)
        pj.write_text(json.dumps(p))
        # re-pin the copy so only the model rule can refuse
        lines = [ln for ln in (c / "frozen/pins.sha256").read_text().splitlines() if not ln.endswith(" panels.json")]
        lines.append(f"{hashlib.sha256(pj.read_bytes()).hexdigest()}  panels.json")
        (c / "frozen/pins.sha256").write_text("\n".join(lines) + "\n")
    else:
        (c / "frozen" / "moves.json").write_text("{}")
    r = launch(ready, "y1", r4=c)
    assert r.returncode == 2 and want in r.stderr, r.stderr


def tree_bytes(d):
    return {str(p): p.read_bytes() for p in sorted(Path(d).rglob("*")) if p.is_file()}


def test_full_f7_row_then_existing_row_refused(ready):
    env = ready
    r = launch(env, "f7-test", collab=1)
    assert r.returncode == 0, r.stdout + r.stderr
    out = Path(env["R4_OUT"])
    rd = out / "runs" / "f7-test"
    res = json.load(open(out / "results" / "f7-test.json"))
    assert [k for k in RESULT_KEYS if k not in res] == []
    assert res["valid"] is True and res["arm"] == "F7"
    for p in PKGS:
        pd = rd / p
        for f in ("panel.json", "slots.json", "collab.json", "resolution.json", "ledger.json", "merged-1.md", "merge-stdout.txt",
                  "scoring/merged-anon.md", "scoring/label-key.json", "scoring/score.json", "scoring/judge.json", "scoring/judge.err",
                  "board/msgs/t2b-1.jsonl", "tags/t4-1.json"):
            assert (pd / f).exists(), (p, f)
        for rid in ("t2b-1", "t4-1", "t3-1"):
            assert (pd / "reviews" / f"{rid}.meta.json").exists() and (pd / "reviews" / f"{rid}.final.md").exists()
        cj = json.load(open(pd / "collab.json"))
        assert cj["cards_sent"] >= 1 and cj["cards_delivered"] >= 1, cj
        assert cj["reviewers"]["t4-1"]["msgs_sent"] == 0 and cj["reviewers"]["t2b-1"]["msgs_received"] == 0
        for rid in ("t4-1", "t3-1"):
            if cj["reviewers"][rid]["msgs_received"]:
                assert cj["reviewers"][rid]["seal_sha_ok"] is True
    assert (rd / "audit.json").exists() and json.load(open(rd / "audit.json"))["audit_ok"] is True, json.load(open(rd / "audit.json"))["violations"]
    sched = jsonl(out / "runs" / "schedule.jsonl")
    assert len(sched) == 1 and sched[0]["row"] == "f7-test"
    # the three reviewers of a package start within 2 s of each other
    starts = {}
    for a in jsonl(Path(env["FAKE_LOG"]) / "argv.jsonl"):
        if "claude-opus-5-5" not in a["argv"] and "--resume" not in a["argv"]:
            starts.setdefault(a["cwd"], []).append(a["t"])
    assert len(starts) == 3 and all(max(t) - min(t) < 2 for t in starts.values())
    assert not list(Path("/tmp").glob("jdg.*/" + DE))
    # an existing row is refused and left byte-identical
    before = tree_bytes(rd)
    r2 = launch(env, "f7-test", collab=1)
    assert r2.returncode == 2 and "row directory exists" in r2.stderr
    assert tree_bytes(rd) == before


def test_full_a1_row(ready):
    env = ready
    r = launch(env, "a1-test", collab=0)
    assert r.returncode == 0, r.stdout + r.stderr
    out = Path(env["R4_OUT"])
    res = json.load(open(out / "results" / "a1-test.json"))
    assert res["valid"] is True and res["arm"] == "A1"
    assert not (Path(env["R4_SBR"]) / "board" / "a1-test").exists()
    assert not any("--settings" in a["argv"] for a in jsonl(Path(env["FAKE_LOG"]) / "argv.jsonl"))
    for p in PKGS:
        assert not (out / "runs" / "a1-test" / p / "board").exists()
        assert json.load(open(out / "runs" / "a1-test" / p / "collab.json"))["arm"] == "A1"


def test_concurrency_count_pattern(tmp_path):
    fb = tmp_path / "bin"
    fb.mkdir()
    (fb / "claude").write_text("#!/bin/sh\nsleep 20\n")
    (fb / "claude").chmod(0o755)
    env = dict(os.environ, PATH=f"{fb}:{os.environ['PATH']}")

    def count():
        a, e = run([R4 / "bin/run-panel.sh", "--print-session-count"]).stdout.split()
        return int(a), int(e)

    for _ in range(5):
        base = count()
        ps = [subprocess.Popen(["timeout", "20", "claude", "-p", "--model", "muse-ember-1.0", "x"], env=env),
              subprocess.Popen(["bash", "-c", "sleep 20 # bash reviewer.sh then claude -p --model muse-ember-1.0"])]
        time.sleep(0.5)
        during = count()
        for p in ps:
            p.terminate()
            p.wait()
        time.sleep(0.3)
        if count() == base:
            break
    assert (during[0] - base[0], during[1] - base[1]) == (1, 1)
