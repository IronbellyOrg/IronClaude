"""Fault-injection tests F1-F19 (DESIGN 15.3) on the fake claude. Every run uses the control package on el2."""

import json
import os
import subprocess
import time
from pathlib import Path

import pytest
from conftest import (
    CONTROL,
    R3,
    SCORE,
    default_rules,
    finding,
    fixture_file,
    jload,
    launch,
    mini_sandbox,
    plan_state,
    report,
    write_plan,
    write_values,
)
from superclaude.cli.review import findings as F

pytestmark = pytest.mark.slow
LUNA, EMBER = "gpt-6-luna", "muse-ember-1.0"


def setup(env, B=40.0, rules=None, **kw):
    write_values(env, B=B)
    mini_sandbox(env)
    write_plan(env, rules if rules is not None else default_rules(env, **kw))


def events(rd):
    return [
        json.loads(x)
        for x in (rd / CONTROL / "board/events.jsonl").read_text().splitlines()
    ]


def ev_of(rd, rid, name):
    return [e for e in events(rd) if e["rid"] == rid and e["ev"] == name]


def rv(rd, name):
    return rd / CONTROL / "reviews" / name


def p2_rule(text=None, **action):
    a = {"text": text} if text is not None else {}
    a.update(action)
    return a


def with_p2(env, action, resume=True, extra=()):
    rules = default_rules(env)
    rules = [
        r for r in rules if "Second pass" not in r["match"].get("prompt_contains", "")
    ]
    return (
        list(extra)
        + [
            {
                "match": {"resume": resume, "prompt_contains": "Second pass"},
                "action": action,
            }
        ]
        + rules
    )


P2_OK = (
    "## Findings block\n```findings-v1\n"
    + json.dumps(finding("C1", "mustnot", claim="new peer-free finding"))
    + "\n```\nverdict: PASS\n"
)


def test_fake_startup_under_2s(env):
    write_plan(env, [{"match": {}, "action": {"text": "hi"}}])
    t = time.time()
    subprocess.run(
        ["claude", "-p", "--model", LUNA, "--output-format", "json"],
        input="x",
        env=env["env"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert time.time() - t < 2.0


def test_f1_resume_fallback(env):
    rules = [
        {
            "match": {"resume": True, "prompt_contains": "Second pass"},
            "action": {"resume_fail": True},
        }
    ] + default_rules(env)
    setup(env, rules=rules)
    r, rd = launch(env, extra=["--no-judge"])
    m = jload(rv(rd, "t4-1.p2.meta.json"))
    assert m["resume_fallback"] is True and m["mode"] == "fresh"
    assert (rd / CONTROL / "board/t4-1.digest.attempt1.jsonl").exists()
    st = plan_state(env)
    fresh = [x for x in st["log"] if x["resume"] is None and x["fmt"] == "stream-json"]
    assert fresh  # the fresh fallback session ran
    assert ev_of(rd, "t4-1", "resume_fallback")
    assert (
        "Earlier you reviewed the candidate"
        in (rd / CONTROL / "board/t4-1.fallback.prompt.txt").read_text()
    )


def test_f1b_fallback_n_zero(env):
    rules = [
        {
            "match": {"resume": True, "prompt_contains": "Second pass"},
            "action": {"resume_fail": True},
        }
    ] + default_rules(env)
    setup(env, B=12.0, rules=rules)
    r, rd = launch(env, extra=["--no-judge"])
    nl = [
        e
        for e in events(rd)
        if e["ev"] == "no_launch" and e.get("reason") == "deadline_after_fallback"
    ]
    assert nl, [e["ev"] for e in events(rd)]


def test_f2_phase2_killed_at_deadline(env):
    c1, c2 = (
        json.dumps(finding("C1", "mustnot", claim="one")),
        json.dumps(finding("C2", "cmd", claim="two")),
    )
    act = {
        "stream_lines": [c1 + "\n", c2 + "\n", c1[:30]],
        "sleep_s": 60,
        "no_result": True,
    }
    setup(env, B=10.0, rules=with_p2(env, act))
    r, rd = launch(env, extra=["--no-judge"])
    pj = jload(rd / CONTROL / "pkg.json")
    launched = [
        rid
        for rid in ("t4-1", "t3-1", "t2b-1")
        if rv(rd, f"{rid}.p2.meta.json").exists()
    ]
    assert launched
    for rid in launched:
        p = rv(rd, f"{rid}.p2.meta.json")
        m = jload(p)
        assert m["phase2_timeout"] is True
        assert m["t_end"] <= pj["P2_DEADLINE"] + 3.5
        fs = F.parse_block(rv(rd, f"{rid}.md").read_text())["findings"]
        assert sum(1 for f in fs if f.get("origin") == "peer") == 2
        assert jload(rv(rd, f"{rid}.combine.json"))["p2_lines_salvaged"] == 2
    assert jload(rd / CONTROL / "collab.json")["panel"]["elapsed_s"] < 1.3 * 10 + 4


def test_f3_phase2_reask_fits(env):
    bad = dict(finding("C1", "mustnot", claim="fixed claim"), severity="HIGH")
    good = finding("C1", "mustnot", claim="fixed claim")

    def body(o):
        return (
            "## Findings block\n```findings-v1\n"
            + json.dumps(o)
            + "\n```\nverdict: PASS\n"
        )

    extra = [
        {
            "match": {"resume": True, "prompt_contains": "findings parser"},
            "action": {"text": body(good)},
        }
    ]
    setup(env, rules=with_p2(env, {"text": body(bad)}, extra=extra))
    r, rd = launch(env, extra=["--no-judge"])
    m = jload(rv(rd, "t4-1.p2.meta.json"))
    assert m["p2reask_s"] is not None
    fs = F.parse_block(rv(rd, "t4-1.md").read_text())["findings"]
    assert any(f["id"].startswith("P2-") and f["claim"] == "fixed claim" for f in fs)


def test_f4_phase2_reask_does_not_fit(env):
    bad = dict(finding("C1", "mustnot", claim="bad line"), severity="HIGH")
    body = (
        "## Findings block\n```findings-v1\n"
        + json.dumps(bad)
        + "\n```\nverdict: PASS\n"
    )
    # B 10 gives P2_DEADLINE T0+13; phase 2 starts about T0+1.5 and ends about T0+9.5, so under 7.5 s (6 + turn) remain
    setup(env, B=10.0, rules=with_p2(env, {"text": body, "sleep_s": 8}))
    r, rd = launch(env, extra=["--no-judge"])
    assert not [
        e for e in events(rd) if e["ev"] == "proc_start" and e.get("kind") == "p2reask"
    ]
    assert [e for e in events(rd) if e["ev"] == "p2_lines_dropped_no_reask"]
    m = jload(rv(rd, "t4-1.p2.meta.json"))
    assert m["p2reask_s"] is None
    cb = jload(rv(rd, "t4-1.combine.json"))
    assert cb["p2_lines_dropped"] == 1 and cb["p1_lines"] == 2
    fs = F.parse_block(rv(rd, "t4-1.md").read_text())["findings"]
    assert [f["id"] for f in fs] == ["F1", "F2"]


def test_f5_phase2_cannot_rewrite_phase1(env):
    p2 = (
        "## Findings block\n```findings-v1\n"
        + json.dumps(finding("F1", "never", claim="withdrawn and changed"))
        + "\n"
        + json.dumps(finding("C1", "mustnot", claim="new one"))
        + "\n```\nverdict: PASS\n"
    )
    setup(env, rules=with_p2(env, {"text": p2}))
    r, rd = launch(env, extra=["--no-judge"])
    fs = F.parse_block(rv(rd, "t4-1.md").read_text())["findings"]
    sealed = F.parse_block(rv(rd, "t4-1.p1.md").read_text())["findings"]
    assert [f["id"] for f in fs] == ["F1", "F2", "P2-F1"]
    for a, b in zip(fs[:2], sealed):
        assert {k: v for k, v in a.items() if k != "origin"} == b


def test_f6_no_qualifying_anchor(env):
    surf = "The artifact path artifacts/out.md is outside the edit scope."
    p1 = {
        EMBER: [finding("F1", "only", "unpassable-check", claim=surf)],
        LUNA: [finding("F1", "never", "missing-requirement", claim=surf)],
    }
    setup(env, p1=p1)
    r, rd = launch(env, extra=["--no-judge"])
    cj = jload(rd / CONTROL / "collab.json")
    assert cj["panel"]["challenges_real"] == 0 and cj["panel"]["echo_rate"] == "n/a"
    # gap draws are random per run; check every draw instead of requiring one: real draws stay empty,
    # every gap draw is filled (the control candidate always has an eligible gap pool)
    for rid in ("t4-1", "t3-1", "t2b-1"):
        f = rd / CONTROL / f"board/{rid}.digest.json"
        if not f.exists():
            continue
        dg = jload(f)
        assert all(s["slot_type"] == "gap" for s in dg["slots"])
        assert all(e["slot_type"] == "real" for e in dg["log"].get("slot_empty", []))


def test_f7_two_blocks(env):
    p1 = {
        EMBER: [finding("F1", "only", "unpassable-check")],
        LUNA: [finding("F1", "never")],
    }
    rules = default_rules(env, p1=p1)
    rules[0]["action"]["report"] = fixture_file(
        env,
        "two.md",
        report(
            [finding("F1", "only", "unpassable-check"), finding("F2", "cmd")], blocks=2
        ),
    )
    setup(env, rules=rules)
    r, rd = launch(env, collab=0, extra=["--no-judge"])
    assert r.returncode == 0, r.stderr
    t = rv(rd, "t2b-1.md").read_text()
    assert t.count("```findings-v1") == 1 and F.parse_block(t)["ok"]
    assert (rd / CONTROL / "merged/merged-1.md").exists()


def test_f8_phase1_hang(env):
    rules = default_rules(env)
    rules.insert(
        0,
        {
            "match": {"model": LUNA, "resume": False, "nth": 1},
            "action": {"sleep_s": 60, "text": "x"},
        },
    )
    setup(env, B=10.0, rules=rules)
    r, rd = launch(env, extra=["--no-judge"])
    pj = jload(rd / CONTROL / "pkg.json")
    hk = [e for e in events(rd) if e["ev"] == "hang_kill"]
    assert len(hk) == 1 and pj["slo_breach"] is True and pj["valid"] is False
    end = max(
        e["t"] for e in events(rd) if e["ev"] == "proc_end" and e["rid"] == hk[0]["rid"]
    )
    assert end <= pj["HANG_AT"] + 5.5
    assert (rd / CONTROL / "merged/merged-1.md").exists()
    assert r.returncode == 2 and jload(rd / "result.json")["invalid_pkgs"] == [CONTROL]


def test_f9_retry_isolated(env):
    rules = default_rules(env)
    rules.insert(
        0,
        {
            "match": {"model": EMBER, "resume": False},
            "times": 1,
            "action": {"text": "review with no block\nverdict: PASS\n"},
        },
    )
    setup(env, rules=rules)
    r, rd = launch(env, extra=["--no-judge"])
    m = jload(rv(rd, "t2b-1.meta.json"))
    assert m["attempts"] == 2 and m["retry_isolated"] is True
    assert ev_of(rd, "t2b-1", "no_launch")[0]["reason"] == "retry_isolated"
    assert not (rd / CONTROL / "board/t2b-1.digest.jsonl").exists()
    reals = [
        s
        for rid in ("t4-1", "t3-1")
        for s in jload(rd / CONTROL / f"board/{rid}.digest.json")["slots"]
        if s["slot_type"] == "real"
    ]
    assert all(s["source_rid"] == "t2b-1" for s in reals)
    cj = jload(rd / CONTROL / "collab.json")
    starts = [
        e["t"] for e in events(rd) if e["ev"] == "proc_start" and e["rid"] == "t2b-1"
    ]
    assert (
        len(starts) == 2 and cj["panel"]["elapsed_s"] >= max(starts) - cj["panel"]["T0"]
    )


def test_f10_wrong_model_no_fallback(env):
    rules = default_rules(env)
    rules.insert(
        0,
        {
            "match": {"model": EMBER, "resume": False},
            "action": {
                "observed_model": "gpt-6.1-sol",
                "report": fixture_file(
                    env, "e.md", report([finding("F1", "only", "unpassable-check")])
                ),
            },
        },
    )
    setup(env, rules=rules)
    r, rd = launch(env)
    m = jload(rv(rd, "t2b-1.meta.json"))
    assert m["model_ok"] is False and m["state"] == "failed"
    calls = [
        x
        for x in plan_state(env)["log"]
        if x["model"] != EMBER and x["model"] not in (LUNA, "claude-opus-5-5")
    ]
    assert (
        not calls
        and len([x for x in plan_state(env)["log"] if x["model"] == EMBER]) == 2
    )
    assert not list(rd.glob(f"{CONTROL}/reviews/*fallback.log"))
    res = jload(rd / "result.json")
    assert res["invalid_pkgs"] == [CONTROL] and r.returncode == 2
    assert (
        "t2b-1"
        not in (rd / CONTROL / "merged/merged-1.md")
        .read_text()
        .split("## Ledger")[0]
        .split("reviewers:")[1]
    )


def test_f11_phase1_reask_then_seal(env):
    bad = [
        dict(finding("F1", "only"), severity="HIGH"),
        dict(finding("F2", "never"), category="nope"),
    ]
    good = [finding("F1", "only"), finding("F2", "never")]
    rules = default_rules(env)
    rules.insert(
        0,
        {
            "match": {
                "model": EMBER,
                "resume": True,
                "prompt_contains": "findings parser",
            },
            "action": {"report": fixture_file(env, "good.md", report(good))},
        },
    )
    rules.insert(
        0,
        {
            "match": {"model": EMBER, "resume": False},
            "action": {"report": fixture_file(env, "bad.md", report(bad))},
        },
    )
    setup(env, rules=rules)
    r, rd = launch(env)
    p1 = rv(rd, "t2b-1.p1.md")
    ra = [
        e
        for e in events(rd)
        if e["rid"] == "t2b-1" and e["ev"] == "proc_end" and e.get("kind") == "reask"
    ]
    assert ra and p1.stat().st_mtime >= ra[0]["t"] - 0.01
    assert oct(p1.stat().st_mode & 0o777) == "0o444"
    import hashlib

    assert (
        hashlib.sha256(p1.read_bytes()).hexdigest()
        == rv(rd, "t2b-1.p1.sha256").read_text().strip()
    )
    assert len(F.parse_block(p1.read_text())["findings"]) == 2


def test_f12_cleanup_two_runs(env):
    write_values(env)
    mini_sandbox(env)
    proj = Path(env["env"]["R3_CLAUDE_PROJECTS"])
    plan2 = env["root"] / "plan2.json"
    rules2 = default_rules(env)
    for rr in rules2:
        if "review 1 of 3" in rr["match"].get("prompt_contains", ""):
            rr["action"]["sleep_s"] = 8
    plan2.write_text(json.dumps(rules2))
    write_plan(env, default_rules(env))
    e2 = dict(env["env"], FAKE_CLAUDE_PLAN=str(plan2), PANEL_COLLAB="1")
    p2 = subprocess.Popen(
        [
            "bash",
            str(R3 / "bin/launch-panel.sh"),
            "el2",
            "--pkgs",
            CONTROL,
            "--no-judge",
        ],
        env=e2,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(3)
    r1, rd1 = launch(env, extra=["--no-judge"])
    c1 = jload(rd1 / CONTROL / "cleanup.json")
    assert c1.get("deferred") is True
    files_after_1 = sorted(proj.rglob("*.jsonl"))
    assert files_after_1
    out, err = p2.communicate(timeout=200)
    rd2 = [d for d in Path(env["env"]["R3_RUNS_ROOT"]).iterdir() if d != rd1][0]
    m = jload(rd2 / CONTROL / "reviews/t4-1.p2.meta.json")
    assert m["resume_fallback"] is False and m["mode"] == "resume"
    c2 = jload(rd2 / CONTROL / "cleanup.json")
    assert c2["deleted"] >= len(files_after_1) and not list(proj.rglob("*.jsonl"))
    assert [d for d in proj.iterdir() if d.is_dir()]


def test_f13_sandbox_write(env):
    sb = Path(env["env"]["R3_SB_ROOT"]) / CONTROL / "repo"
    rules = default_rules(env)
    rules.insert(
        0,
        {
            "match": {"model": EMBER, "resume": False},
            "action": {
                "write_file": str(sb / "x.txt"),
                "report": fixture_file(
                    env, "e.md", report([finding("F1", "only", "unpassable-check")])
                ),
            },
        },
    )
    setup(env, rules=rules)
    r, rd = launch(env)
    au = jload(rd / CONTROL / "audit.json")
    assert any(v["check"] == "sandbox_dirty" for v in au["violations"])
    assert (rd / CONTROL / "QUARANTINE").exists() and jload(rd / "result.json")[
        "contaminated"
    ] is True
    assert r.returncode == 3
    r2, _ = launch(env)
    assert r2.returncode == 1 and "E_SANDBOX_DIRTY" in r2.stderr


def test_f14_ground_truth_read(env):
    rules = default_rules(env)
    rules.insert(
        0,
        {
            "match": {"model": EMBER, "resume": False},
            "action": {
                "tool_use_input": {"command": f"cat /x/{CONTROL}/ground-truth.json"},
                "report": fixture_file(
                    env, "e.md", report([finding("F1", "only", "unpassable-check")])
                ),
            },
        },
    )
    setup(env, rules=rules)
    r, rd = launch(env)
    au = jload(rd / CONTROL / "audit.json")
    assert any(
        v["check"] == "forbidden_read" and v["pattern"] == "ground-truth"
        for v in au["violations"]
    )
    assert jload(rd / "result.json")["contaminated"] is True and r.returncode == 3


def test_f14b_peer_transcript_read(env):
    proj = env["env"]["R3_CLAUDE_PROJECTS"]
    rules = default_rules(env)
    rules.insert(
        0,
        {
            "match": {"model": EMBER, "resume": False},
            "action": {
                "tool_use_input": {"command": f"cat {proj}/-tmp-x/0000.jsonl"},
                "report": fixture_file(
                    env, "e.md", report([finding("F1", "only", "unpassable-check")])
                ),
            },
        },
    )
    setup(env, rules=rules)
    r, rd = launch(env, extra=["--no-judge"])
    au = jload(rd / CONTROL / "audit.json")
    assert any(v["check"] == "forbidden_read" for v in au["violations"])
    assert jload(rd / "result.json")["contaminated"] is True


def test_f14b_killed_attempt_read(env):
    rules = default_rules(env)
    rules.insert(
        0,
        {
            "match": {"model": EMBER, "resume": False},
            "times": 1,
            "action": {
                "tool_use_input": {"command": f"cat /x/{CONTROL}/ground-truth.json"},
                "no_stdout": True,
                "exit": 1,
            },
        },
    )
    setup(env, rules=rules)
    r, rd = launch(env, extra=["--no-judge"])
    a1 = jload(rv(rd, "t2b-1.attempt1.meta.json"))
    assert a1["session_id"] == "" and a1.get("recovered_session_ids")
    au = jload(rd / CONTROL / "audit.json")
    assert any(v["check"] == "forbidden_read" for v in au["violations"])
    assert jload(rd / "result.json")["contaminated"] is True


def test_f15_merge_refusal(env):
    rules = [
        {
            "match": {"prompt_contains": "review 1 of 3"},
            "action": {"text": "no block here\nverdict: PASS\n"},
        },
        {
            "match": {"prompt_contains": "blind scoring judge"},
            "action": {"judge_score": SCORE},
        },
    ]
    setup(env, rules=rules)
    r, rd = launch(env)
    pj = jload(rd / CONTROL / "pkg.json")
    assert pj["valid"] is False and "merge refused" in pj["invalid_reason"]
    assert jload(rd / "result.json")["invalid_pkgs"] == [CONTROL] and r.returncode == 2
    assert not [x for x in plan_state(env)["log"] if x["model"] == "claude-opus-5-5"]


def test_f16_judge_retry(env):
    rules = default_rules(env, judge=False)
    rules += [
        {
            "match": {"prompt_contains": "blind scoring judge"},
            "times": 1,
            "action": {"text": "oops"},
        },
        {
            "match": {"prompt_contains": "blind scoring judge"},
            "action": {"judge_score": SCORE},
        },
    ]
    setup(env, rules=rules)
    r, rd = launch(env, collab=0)
    assert jload(rd / "result.json")["judge_ok"] is True and r.returncode == 0
    assert list((Path(env["env"]["R3_SCORING_ROOT"])).glob("*/*/*/attempt1"))


def test_f16b_judge_fails_twice(env):
    rules = default_rules(env, judge=False) + [
        {
            "match": {"prompt_contains": "blind scoring judge"},
            "action": {"text": "oops"},
        }
    ]
    setup(env, rules=rules)
    r, rd = launch(env, collab=0)
    assert jload(rd / "result.json")["judge_ok"] is False and r.returncode == 2


def test_f17_late_finisher(env):
    rules = default_rules(env)
    rules.insert(
        0,
        {
            "match": {"model": LUNA, "resume": False, "nth": 1},
            "action": {
                "sleep_s": 5,
                "report": fixture_file(
                    env, "late.md", report([finding("F1", "reread", "contradiction")])
                ),
            },
        },
    )
    setup(env, B=10.0, rules=rules)
    r, rd = launch(env, extra=["--no-judge"])
    assert [  # a fresh luna phase-1 session ran
        x for x in plan_state(env)["log"] if x["model"] == LUNA and x["resume"] is None
    ]
    nl = {e["rid"]: e.get("reason") for e in events(rd) if e["ev"] == "no_launch"}
    assert "deadline" in nl.values()
    lunas_late = [rid for rid in ("t4-1", "t3-1") if nl.get(rid) == "deadline"]
    assert len(lunas_late) >= 1


def test_f18_collab_off(env):
    setup(env)
    r, rd = launch(env, collab=0)
    assert r.returncode == 0, r.stderr
    pd = rd / CONTROL
    assert not list(pd.glob("board/*.digest.jsonl")) and not list(
        pd.glob("reviews/*.p2.*")
    )
    assert not (pd / "merged-sealed").exists()
    keys = jload(rd / "scoring-keys.json")
    assert {k["kind"] for k in keys.values()} == {"full"}
    cj = jload(pd / "collab.json")
    assert (
        cj["arm"] == "A1"
        and cj["panel"]["challenges_real"] == 0
        and cj["panel"]["echo_rate"] == "n/a"
    )
    assert all(
        v["n_launched"] == 0 and v["msgs_received"] == 0
        for v in cj["reviewers"].values()
    )
    p1_off = sorted(
        json.dumps(x["argv"])
        for x in plan_state(env)["log"]
        if "review 1 of 3" not in ""
        and x["fmt"] == "json"
        and x["model"] != "claude-opus-5-5"
    )
    # a collab run with the same plan gives the same phase-1 argv
    os.remove(Path(env["env"]["FAKE_CLAUDE_PLAN"]).with_suffix(".state.json"))
    r2, rd2 = launch(env, collab=1, extra=["--no-judge"])
    p1_on = sorted(
        json.dumps(x["argv"])
        for x in plan_state(env)["log"]
        if x["fmt"] == "json" and x["model"] != "claude-opus-5-5"
    )
    assert p1_off == p1_on and len(p1_on) == 3


def test_f19_phase2_wrong_model(env):
    setup(env, rules=with_p2(env, {"text": P2_OK, "observed_model": "gpt-6.1-sol"}))
    r, rd = launch(env, extra=["--no-judge"])
    assert ev_of(rd, "t4-1", "p2_model_mismatch")
    for rid in ("t4-1", "t3-1", "t2b-1"):
        fs = F.parse_block(rv(rd, f"{rid}.md").read_text())["findings"]
        assert not [f for f in fs if f.get("origin") == "peer"]
