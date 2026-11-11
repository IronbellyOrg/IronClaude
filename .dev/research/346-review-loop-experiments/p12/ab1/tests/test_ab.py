"""Offline tests of the ab1 tooling (plan Part C). Run:
  cd $AB && uv run --no-project --with pytest pytest -q tests"""
import json
import os
import pathlib
import shutil
import sys
import time

import pytest

AB = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AB))
import advance  # noqa: E402
import harness as h  # noqa: E402
import score_themes as sc  # noqa: E402

SP = h.SP
P11 = h.P11
RV = ".dev/orca-command-refactor/review/"


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setattr(h, "RUNS", tmp_path / "runs")
    h.RUNS.mkdir()
    monkeypatch.setattr(h, "TASKS_GLOB", str(tmp_path / "none" / "*.output"))
    return tmp_path


def baseline(run, rel):
    return P11 / "runs" / run / "ws" / h.D / "review" / rel


def old_age(p):
    t = time.time() - 600
    os.utime(p, (t, t))


def fake(run, step, src_text):
    p = h.out_path(run, step)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(src_text)
    old_age(p)
    return p


def adv(capsys, argv=()):
    advance.main(list(argv))
    return capsys.readouterr().out


def launches(out):
    return [ln for ln in out.splitlines() if ln.startswith("LAUNCH ")]


def verify_reply(rows, confirmed):
    lines = ["| id | found | exists | follows | verdict | reason |", "|---|---|---|---|---|---|"]
    for fid, verdict in rows.items():
        lines.append(f"| {fid} | text | yes | yes | {verdict} | because |")
    lines.append("confirmed: " + (", ".join(confirmed) if confirmed else "none"))
    return "\n".join(lines) + "\n"


def start(env, capsys, run="b1-r1", srcs=("a3-r1", "a3-r3", "a3-r6")):
    h.build("sonnet")
    out = adv(capsys)
    assert len(launches(out)) == 6
    for step, src in zip(h.R1S, srcs):
        fake(run, step, baseline(src, "round1.md").read_text())
    return adv(capsys)


# 1 ---------------------------------------------------------------- scoring
SCORES = {
    "a2-r1": ([("B-1", "T3"), ("B-2", "T1")], [("F-1", "T1"), ("F-2", "T2")]),
    "a2-r2": ([("B1", "T1"), ("B2", "T2")], [("F-01", "T2"), ("F-02", "T3")]),
    "a2-r3": ([], [("REQ-1", "T1"), ("REQ-2", "T1"), ("ARCH-1", "T2")]),
    "a2-r4": ([("B-1", "T1")], [("F-1", "T1"), ("F-2", "T2"), ("F-3", "other")]),
    "a2-r5": ([("B-1", "T2"), ("B-2", "T3")], [("F-1", "T1")]),
    "a2-r6": ([("F-01", "T1")], []),
    "a3-r1": ([("F1", "T3"), ("F2", "T1")], [("B1", "T1"), ("B2", "T2")]),
    "a3-r2": ([("R1-B1", "T1"), ("R1-B2", "T2")], [("F-01", "T3"), ("F-02", "T1")]),
    "a3-r3": ([("F1", "T1"), ("F2", "T1"), ("F3", "T3")], [("F-1", "T1"), ("F-2", "T2")]),
    "a3-r4": ([("F-01", "T1")], [("A-01", "other"), ("A-02", "T2")]),
    "a3-r5": ([("F-1", "T1"), ("F-2", "T3"), ("F-3", "other")], []),
    "a3-r6": ([("REQ-1", "T2"), ("REQ-2", "T1"), ("ARCH-1", "T2")], [("F-01", "T2")]),
}


@pytest.mark.parametrize("run", sorted(SCORES))
def test_scoring_matches_baseline_table(run):
    r1, aud = SCORES[run]
    for path, want in ((P11 / "runs" / run / "ws" / h.D / "review/round1.md", r1),
                       (P11 / "runs" / run / "aud/ws" / h.D / "review/audit.md", aud)):
        fs = sc.blocking_findings(path)
        assert [(f["id"], f["theme"]) for f in fs] == want
        for f in fs:
            assert f["heading"] is not None and f["cited"], (run, f["id"])


# 2 ---------------------------------------------------------------- parse_ids
def test_parse_ids_on_a3_round1_reports():
    want = {"a3-r1": ["F1", "F2"], "a3-r2": ["R1-B1", "R1-B2"], "a3-r3": ["F1", "F2", "F3"], "a3-r4": ["F-01"],
            "a3-r5": ["F-1", "F-2", "F-3"], "a3-r6": ["REQ-1", "REQ-2", "ARCH-1"]}
    for run, ids in want.items():
        assert sc.parse_ids(sc.ids_from(baseline(run, "round1.md"))) == ids, run


def test_parse_ids_edge_cases():
    assert sc.parse_ids("none (F1, F2 and F3 are resolved; no new blocking finding)") == []
    assert sc.parse_ids("NEW-1. Nothing else. REQ-1, REQ-2 and ARCH-1 are resolved") == ["NEW-1"]
    assert sc.parse_ids(None) == []


# 3 ---------------------------------------------------------------- basetokens
def test_basetokens_reproduces_section_2(capsys):
    import glob
    if not glob.glob(h.TASKS_GLOB):
        pytest.skip("no transcripts readable")
    ml, ma = h.basetokens()
    assert abs(ml - 100424) / 100424 < 0.01
    assert abs(ma - 69044) / 69044 < 0.01


# 4 ---------------------------------------------------------------- build
def test_build_sandboxes(env):
    h.build("sonnet")
    assert sorted(p.name for p in h.RUNS.iterdir()) == [f"b1-r{i}" for i in range(1, 7)]
    d = h.run_dir("b1-r1")
    for sb in (d, d / "r1a", d / "r1b", d / "r1c"):
        assert h.sha(sb / "ws" / h.SPEC) == h.SPEC_SHA
        assert h.sha(sb / "command.md") == h.AUD_CMD_SHA
        rules = (sb / "home/.claude/rules/prompts/document_review_loop_prompts.md").read_text()
        assert "**MERGE rule**" in rules and "### VERIFY prompt" in rules
        assert (sb / "ws" / h.D / "specs/history").is_dir() and (sb / "ws" / h.D / "review").is_dir()
    st = h.load("b1-r1")
    assert st["stratum"] == "sonnet" and st["loop_model"] == "sonnet" and st["product_ref"] == h.PRODUCT_REF
    assert not (h.P11 / "rules.md").read_text() == rules      # the frozen audit rules file is untouched
    assert h.sha_text((h.P11 / "rules.md").read_text()) == h.AUD_RULES_SHA


# 5 ---------------------------------------------------------------- prompt identity
def test_prompts_identical_to_baseline(env):
    h.build("sonnet")
    run = "b1-r1"
    d = h.run_dir(run)
    base1 = P11 / "runs/a3-r1"
    for x, _ in zip("abc", range(3)):
        h.prep(run, f"R1{x}")
        got = (d / f"PROMPT-R1{x}.md").read_text().replace(str(d / f"r1{x}"), str(base1))
        assert got == (base1 / "PROMPT-R1.md").read_text()
    h.prep(run, "V1", {"IDS": "F1, F2"})
    assert (d / "PROMPT-V1.md").read_text().replace(str(d), str(base1)) == (base1 / "PROMPT-V1.md").read_text()
    h.prep(run, "R2")
    assert (d / "PROMPT-R2.md").read_text().replace(str(d), str(base1)) == (base1 / "PROMPT-R2.md").read_text()
    h.prep(run, "R3")
    base6 = P11 / "runs/a3-r6"
    assert (d / "PROMPT-R3.md").read_text().replace(str(d), str(base6)) == (base6 / "PROMPT-R3.md").read_text()
    h.prep(run, "AUD")
    h.prep(run, "AUD2")
    aud = (d / "PROMPT-AUD.md").read_text().replace(str(d / "aud"), str(base1 / "aud"))
    assert aud == (base1 / "PROMPT-AUD.md").read_text()
    aud2 = (d / "PROMPT-AUD2.md").read_text().replace(str(d / "aud2"), str(base1 / "aud"))
    assert aud2 == (base1 / "PROMPT-AUD.md").read_text()
    # the audit instrument is the frozen one
    assert h.sha(d / "aud2" / "command.md") == h.AUD_CMD_SHA
    assert h.sha(d / "aud2/home/.claude/rules/prompts/document_review_loop_prompts.md") == h.AUD_RULES_SHA


# 6 ---------------------------------------------------------------- merge
def test_merge_of_three_fake_reviews(env, capsys):
    out = start(env, capsys)
    st = h.load("b1-r1")
    m = st["merge"]
    assert m["raw_count"] == 8 and m["merged_count"] <= m["raw_count"]
    members = [x for g in m["groups"] for x in g["members"]]
    want = {f"round1-a.md/{i}" for i in ("F1", "F2")} | {f"round1-b.md/{i}" for i in ("F1", "F2", "F3")} | \
        {f"round1-c.md/{i}" for i in ("REQ-1", "REQ-2", "ARCH-1")}
    assert sorted(members) == sorted(want) and len(members) == 8
    assert [g["mid"] for g in m["groups"]] == [f"M{i}" for i in range(1, len(m["groups"]) + 1)]
    fl = (h.ws("b1-r1") / h.REVIEW / "findings-1.md").read_text()
    assert fl.startswith("Each Mn below is one finding;")
    for g in m["groups"]:
        assert f"### {g['mid']}" in fl
    assert fl.count("#### M") == 8
    assert not any(h.DROP_RE.match(ln) for ln in fl.splitlines())
    vf = h.run_dir("b1-r1") / "vf1"
    files = [p.relative_to(vf).as_posix() for p in vf.rglob("*") if p.is_file()]
    assert files == [h.SPEC.join(["ws/", ""])]
    assert len(launches(out)) >= 1 and "PROMPT-VF1.md" in out


# 7 ---------------------------------------------------------------- three PASS
def test_three_pass_reviews(env, capsys):
    h.build("sonnet")
    adv(capsys)
    pass_text = baseline("a2-r3", "round1.md").read_text()
    assert sc.verdict_of(pass_text) == "PASS"
    for s in h.R1S:
        fake("b1-r1", s, pass_text)
    out = adv(capsys)
    st = h.load("b1-r1")
    assert st["loop_end"] == "PASS"
    assert "verdict: PASS" in (h.ws("b1-r1") / h.REVIEW / "round1.md").read_text()
    assert "PROMPT-AUD.md" in out and "PROMPT-AUD2.md" in out


# 8 ---------------------------------------------------------------- parse_verify
def test_parse_verify():
    t, ok = h.parse_verify(verify_reply({"M1": "confirm", "M2": "reject"}, ["M1"]), ["M1", "M2"])
    assert ok and t["M1"][0] == "confirm" and t["M2"][0] == "reject" and t["M2"][1] == "because"
    t, ok = h.parse_verify("prose\nconfirmed: M2\n", ["M1", "M2"])
    assert ok and t["M2"][0] == "confirm" and t["M1"] == ("reject", "not in confirmed line")
    t, ok = h.parse_verify("", ["M1", "M2"])
    assert not ok and {v[0] for v in t.values()} == {"confirm"}
    t, ok = h.parse_verify("| M1 | text says confirm and reject | yes | no | x |\nconfirmed: none\n", ["M1"])
    assert t["M1"][0] == "reject"


# 9 ---------------------------------------------------------------- happy path
def test_happy_path_after_vf1(env, capsys):
    start(env, capsys)
    run = "b1-r1"
    mids = h.load(run)["log"]["VF1"]["finding_ids"]
    assert len(mids) >= 2
    rows = {m: ("confirm" if m == "M1" else "reject") for m in mids}
    fake(run, "VF1", verify_reply(rows, ["M1"]))
    adv(capsys)
    rep = (h.ws(run) / h.REVIEW / "round1.md").read_text()
    assert rep.splitlines()[0] == "review: 1 of 3"
    for part in ("# Merged first review", "sources:", "verification (coordinator, VERIFY step VF1", "## Blocking findings (merged, confirmed)",
                 "## Noted, unactioned", "## Follow-up candidates", "## Reviser brief"):
        assert part in rep
    assert "Blocking finding ids: M1." in rep and rep.rstrip().endswith("verdict: FAIL")
    noted = (h.run_dir(run) / "NOTED.md").read_text()
    for m in mids[1:]:
        assert f"| VF1 | {m} |" in noted
    assert "| VF1 | M1 |" not in noted
    v1 = (h.run_dir(run) / "PROMPT-V1.md").read_text()
    assert "IDS=M1" in v1.replace("\n", " ") or "IDS=M1\n" in v1
    spec = h.ws(run) / h.SPEC
    spec.write_text(spec.read_text() + "\nrevised line\n")
    fake(run, "V1", "revise report\n")
    adv(capsys)
    assert (h.ws(run) / h.HIST / "spec-v1.md").exists()
    fake(run, "R2", baseline("a3-r3", "round2.md").read_text())
    out = adv(capsys)
    assert "PROMPT-AUD.md" in out and "PROMPT-AUD2.md" in out
    st = h.load(run)
    assert st["loop_end"] == "PASS" and st["final_spec"]["bytes"] > 57763


# 10 --------------------------------------------------------------- verified pass and escalation
def test_vf1_rejecting_all_is_verified_pass(env, capsys):
    start(env, capsys)
    run = "b1-r1"
    mids = h.load(run)["log"]["VF1"]["finding_ids"]
    fake(run, "VF1", verify_reply({m: "reject" for m in mids}, []))
    out = adv(capsys)
    rep = (h.ws(run) / h.REVIEW / "round1.md").read_text()
    assert "Blocking finding ids: none (no merged finding was confirmed)." in rep and rep.rstrip().endswith("verdict: FAIL")
    assert h.load(run)["loop_end"] == "VERIFIED-PASS"
    assert "PROMPT-AUD.md" in out and "PROMPT-AUD2.md" in out


def test_vf3_with_confirmed_id_escalates(env, capsys):
    start(env, capsys)
    run = "b1-r1"
    mids = h.load(run)["log"]["VF1"]["finding_ids"]
    fake(run, "VF1", verify_reply({m: "confirm" for m in mids}, mids))
    adv(capsys)
    fake(run, "V1", "revise\n")
    adv(capsys)
    r2 = baseline("a3-r1", "round1.md").read_text()
    fake(run, "R2", r2)
    adv(capsys)
    assert "VF2" in h.load(run)["prepared"]
    f2 = (h.ws(run) / h.REVIEW / "findings-2.md").read_text()
    assert "### F1" in f2 and not any(h.DROP_RE.match(ln) for ln in f2.splitlines())
    fake(run, "VF2", verify_reply({"F1": "confirm", "F2": "confirm"}, ["F1", "F2"]))
    adv(capsys)
    assert "review: 1 of 3" in (h.ws(run) / h.REVIEW / "round2.md").read_text()   # block inserted after the header
    assert (h.ws(run) / h.REVIEW / "round2.orig.md").exists()
    assert "verification (coordinator, VERIFY step VF2" in (h.ws(run) / h.REVIEW / "round2.md").read_text()
    fake(run, "V2", "revise\n")
    adv(capsys)
    fake(run, "R3", r2)
    adv(capsys)
    fake(run, "VF3", verify_reply({"F1": "confirm", "F2": "reject"}, ["F1"]))
    out = adv(capsys)
    st = h.load(run)
    assert st["loop_end"] == "ESCALATED" and "PROMPT-AUD.md" in out
    assert any(n["step"] == "VF3" and n["id"] == "F2" for n in st["noted_unactioned"])


def test_vf2_rejecting_all_ends_verified_pass(env, capsys):
    start(env, capsys)
    run = "b1-r1"
    mids = h.load(run)["log"]["VF1"]["finding_ids"]
    fake(run, "VF1", verify_reply({m: "confirm" for m in mids}, mids))
    adv(capsys)
    fake(run, "V1", "revise\n")
    adv(capsys)
    fake(run, "R2", baseline("a3-r1", "round1.md").read_text())
    adv(capsys)
    fake(run, "VF2", verify_reply({"F1": "reject", "F2": "reject"}, []))
    adv(capsys)
    assert h.load(run)["loop_end"] == "VERIFIED-PASS"


# 11 --------------------------------------------------------------- concurrency
def test_concurrency_and_dry_run(env, capsys):
    h.build("sonnet")
    out = adv(capsys, ["--dry-run"])
    ls = launches(out)
    assert len(ls) == 6 and "b1-r1" in ls[0] and "b1-r3" not in " ".join(ls)
    assert all(not h.load(r)["launched"] for r in h.all_runs())
    out = adv(capsys)
    assert len(launches(out)) == 6
    out2 = adv(capsys)
    assert launches(out2) == [] and "RUNNING 6" in out2


# 12 --------------------------------------------------------------- tokens
def write_tr(path, prompt, model, usages, done=True):
    lines = [json.dumps({"type": "user", "message": {"role": "user", "content": f"Read {prompt} and follow it exactly. Touch nothing."}})]
    for mid, ot in usages:
        for blk in ("thinking", "text"):      # one message id logged once per content block
            lines.append(json.dumps({"type": "assistant", "message": {"role": "assistant", "id": mid, "model": model,
                                                                      "content": [{"type": blk, "text": "DONE x" if (done and mid == usages[-1][0]) else "y"}],
                                                                      "usage": {"output_tokens": ot}}}))
    path.write_text("\n".join(lines) + "\n")


def test_tokens_dedupe_and_model_filter(env, capsys, monkeypatch):
    h.build("sonnet")
    tdir = env / "tasks"
    tdir.mkdir()
    pr = "/x/p12/ab1/runs/b1-r1/PROMPT-R1a.md"
    write_tr(tdir / "good.output", pr, "claude-sonnet-5-5", [("m1", 100), ("m2", 50)])
    write_tr(tdir / "opus.output", pr, "claude-opus-5-5", [("m1", 999)])
    monkeypatch.setattr(h, "TASKS_GLOB", str(tdir / "*.output"))
    st = h.load("b1-r1")
    st["log"]["R1a"] = {"output_exists": True}
    h.save("b1-r1", st)
    h.tokens_cmd()
    assert h.load("b1-r1")["log"]["R1a"]["output_tokens"] == 150      # each message id once
    assert "WARN" in capsys.readouterr().out


# 13 --------------------------------------------------------------- convention, strata, extension
def rec(run, loop, aud, blk, growth=0.0, end="PASS", rej=(0, 0), stratum="sonnet"):
    return {"run": run, "stratum": stratum, "lost": False, "complete": True, "loop_end": end, "relaunched": False,
            "loop_tokens": loop, "aud_tokens": [aud, aud], "final_bytes": int(57763 * (1 + growth)),
            "audits": [{"step": s, "verdict": "FAIL" if blk else "PASS",
                        "findings": [{"id": f"F{i}", "theme": "T1", "cited": {1}} for i in range(blk)]} for s in ("AUD", "AUD2")],
            "vf": {"VF1": {"finding_ids": [f"M{i}" for i in range(rej[1])], "rejected": {f"M{i}": "x" for i in range(rej[0])}}} if rej[1] else {},
            "reviewers": {}, "merge": {}, "noted": []}


def test_cost_is_loop_only_and_decided_post_hoc():
    dec = h.decision()
    assert dec["rules"]["DROP2_RLOOP_LIMIT"] == 2.69          # D6: (2.0*169468-69044)/100424
    base = {"B_BLK": 1.5, "B_AUDFAIL": h.Fraction(5, 6), "B_THEME": h.Fraction(5, 6), "B_GROWTH": 0.0141}
    # R_B (=(LOOP+AUD)/169468) is 1.65 (inside the old limit 2.0) but R_LOOP is 2.79 > 2.69: R_LOOP decides
    recs = [rec(f"b1-r{i}", 280000, 1, 1) for i in range(1, 7)]
    o = h.decide(recs, dec, base, 6)
    assert o["R_LOOP"] == pytest.approx(280000 / 100424) and o["R_B"] == pytest.approx((280000 + 1) / 169468)
    assert o["R_B"] < 2.0 < o["R_LOOP"] and o["outcome"] == "DROP" and "DROP-2" in o["rule"]
    # the same blockers with a cheap loop are not a DROP-2
    cheap = h.decide([rec(f"b1-r{i}", 200000, 1, 1) for i in range(1, 7)], dec, base, 6)
    assert cheap["outcome"] == "INCONCLUSIVE"
    adopt = h.decide([rec(f"b1-r{i}", 200000, 69044, 0 if i < 5 else 1) for i in range(1, 7)], dec, base, 6)
    assert adopt["outcome"] == "ADOPT"
    drop1 = h.decide([rec(f"b1-r{i}", 100000, 1, 2) for i in range(1, 7)], dec, base, 6)
    assert drop1["outcome"] == "DROP" and "DROP-1" in drop1["rule"]
    drop3 = h.decide([rec(f"b1-r{i}", 100000, 1, 0, rej=(3, 4)) for i in range(1, 7)], dec, base, 6)
    assert drop3["outcome"] == "DROP" and "DROP-3" in drop3["rule"]
    drop4 = h.decide([rec(f"b1-r{i}", 100000, 1, 0, end="ESCALATED" if i < 3 else "PASS") for i in range(1, 7)], dec, base, 6)
    assert drop4["outcome"] == "DROP" and "DROP-4" in drop4["rule"]
    few = h.decide([rec(f"b1-r{i}", 100000, 1, 0) for i in range(1, 5)], dec, base, 6)
    assert few["outcome"] == "INCONCLUSIVE"


def test_replica_disagreement_and_haiku_condition():
    sonnet = {"outcome": "ADOPT"}
    same = [{"outcome": "ADOPT"}, {"outcome": "ADOPT"}]
    assert h.final_outcome(sonnet, same, {"state": "pending"})[0] == "ADOPT (Haiku robustness pending)"
    assert h.final_outcome(sonnet, same, {"state": "ok"})[0] == "ADOPT"
    assert h.final_outcome(sonnet, same, {"state": "disagrees"}) [0] == "INCONCLUSIVE"
    assert h.final_outcome(sonnet, same, {"state": "disagrees"})[1] is False      # no extension for a Haiku disagreement
    assert h.final_outcome(sonnet, [{"outcome": "ADOPT"}, {"outcome": "INCONCLUSIVE"}], {"state": "ok"})[0] == "INCONCLUSIVE"
    assert h.final_outcome({"outcome": "DROP"}, [{"outcome": "DROP"}] * 2, {"state": "ok"}) == ("DROP", False, "")


def test_n9_fractions():
    dec = h.decision()
    base = {"B_BLK": 1.5, "B_AUDFAIL": h.Fraction(5, 6), "B_THEME": h.Fraction(5, 6), "B_GROWTH": 0.0141}
    recs = [rec(f"b1-r{i}", 200000, 69044, 0) for i in range(1, 10)]
    assert h.decide(recs, dec, base, 9)["outcome"] == "ADOPT"
    recs[0]["loop_end"] = recs[1]["loop_end"] = "ESCALATED"          # 7/9 pass < 8/9
    assert h.decide(recs, dec, base, 9)["outcome"] == "DROP"
    assert h.decide(recs[:7], dec, base, 9)["outcome"] == "INCONCLUSIVE"   # fewer than 8 completed


def test_haiku_stratum_build_and_launch_models(env, capsys):
    h.build("sonnet")
    h.build("haiku")
    names = [p.name for p in h.RUNS.iterdir()]
    assert sorted(n for n in names if n.startswith("b1h-")) == [f"b1h-r{i}" for i in range(1, 5)]
    assert all(h.load(f"b1h-r{i}")["stratum"] == "haiku" and h.load(f"b1h-r{i}")["loop_model"] == "haiku" for i in range(1, 5))
    assert h.load("b1-r1")["stratum"] == "sonnet"
    # Sonnet runs print first; free the slots and check the Haiku models
    for r in range(1, 7):
        st = h.load(f"b1-r{r}")
        st["lost"] = True
        h.save(f"b1-r{r}", st)
    out = adv(capsys)
    ls = launches(out)
    assert ls and all("b1h-r" in ln and ln.endswith("model=haiku") for ln in ls)
    # audits stay Sonnet
    st = h.load("b1h-r1")
    st["launched"], st["prepared"] = {}, []
    h.save("b1h-r1", st)
    for r in (2, 3, 4):
        s = h.load(f"b1h-r{r}")
        s["lost"] = True
        h.save(f"b1h-r{r}", s)
    h.prep("b1h-r1", "AUD")
    h.prep("b1h-r1", "AUD2")
    out = adv(capsys)
    ls = launches(out)
    assert len(ls) == 2 and all(ln.endswith("model=sonnet") for ln in ls)


def test_extend_gate_and_haiku_not_pooled(env, tmp_path, monkeypatch, capsys):
    ab = tmp_path / "abdir"
    ab.mkdir()
    shutil.copy(AB / "decision.json", ab / "decision.json")
    monkeypatch.setattr(h, "AB", ab)
    h.build("sonnet")
    with pytest.raises(SystemExit):
        h.build("sonnet", extend=True)                               # no metrics.json yet
    json.dump({"sonnet": {"n_runs": 6, "extension_eligible": False}}, open(ab / "metrics.json", "w"))
    with pytest.raises(SystemExit):
        h.build("sonnet", extend=True)                               # outcome not INCONCLUSIVE
    json.dump({"sonnet": {"n_runs": 6, "extension_eligible": True}}, open(ab / "metrics.json", "w"))
    h.build("sonnet", extend=True)
    assert [f"b1-r{i}" for i in (7, 8, 9)] == [r for r in h.all_runs() if int(r.split("-r")[1]) > 6]
    with pytest.raises(SystemExit):
        h.build("sonnet", extend=True)                               # never twice
    with pytest.raises(SystemExit):
        h.build("haiku", extend=True)
    # Haiku runs never enter the Sonnet numbers
    h.build("haiku")
    st = h.load("b1h-r1")
    st["complete"] = True
    h.save("b1h-r1", st)
    m = h.analyze()
    assert m["sonnet"]["n_completed"] == 0 and m["haiku"]["state"] == "pending"
    assert (ab / "metrics.json").exists() and (ab / "RESULTS-tables.md").exists()


def test_no_cost_kill_in_tooling(env, capsys):
    """D6: a huge token count never stops, skips or loses a run."""
    h.build("sonnet")
    adv(capsys)
    st = h.load("b1-r1")
    st["log"]["R1a"] = {"output_exists": True, "output_tokens": 10 ** 9}
    h.save("b1-r1", st)
    adv(capsys)
    assert not h.load("b1-r1")["lost"]
    src = (AB / "advance.py").read_text() + (AB / "harness.py").read_text()
    code = [ln for ln in src.splitlines() if not ln.lstrip().startswith(("#", '"', "'"))]
    assert not any("abort" in ln.lower() and "token" in ln.lower() for ln in code)


# retries --------------------------------------------------------------
def test_incomplete_review_relaunched_once_then_lost(env, capsys):
    h.build("sonnet")
    adv(capsys)
    fake("b1-r1", "R1a", "no verdict here\n")
    out = adv(capsys)
    assert "MANUAL b1-r1 R1a" in out and any("PROMPT-R1a.md" in ln for ln in launches(out))
    fake("b1-r1", "R1a", "still no verdict\n")
    out = adv(capsys)
    assert "LOST b1-r1 R1a" in out and h.load("b1-r1")["lost"]


def test_fail_without_ids_waits_for_setids(env, capsys):
    h.build("sonnet")
    adv(capsys)
    fake("b1-r1", "R1a", "review: 1 of 3\n### F1 AC-0.4 thing\nspec:10\nverdict: FAIL\n")
    out = adv(capsys)
    assert "MANUAL b1-r1 R1a no blocking ids parsed" in out
    h.setids("b1-r1", "R1a", "F1")
    adv(capsys)
    assert "R1a" in h.load("b1-r1")["transitioned"]
