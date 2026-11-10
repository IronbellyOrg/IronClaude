"""Offline tests of the A/B design 2 tooling (plan Part C).  Run: uv run --no-project --with pytest pytest -q tests"""
import json
import os
import pathlib
import re
import shutil
import statistics
import time

import pytest

import score_themes as sc  # noqa: E402  (conftest puts the ab2 dir on sys.path)
import advance

SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
P11R = SP/"p11"/"runs"
D = ".dev/orca-command-refactor"
REV = f"{D}/review"
AUDREP = f"aud/ws/{REV}/audit.md"


def rd(run, rel):
    return P11R/run/rel


# ------------------------------------------------------------------ 1. scoring table
SCORE_TABLE = {
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


@pytest.mark.parametrize("run", sorted(SCORE_TABLE))
def test_scoring_table(run):
    first, aud = SCORE_TABLE[run]
    for path, want in ((rd(run, f"ws/{REV}/round1.md"), first), (rd(run, AUDREP), aud)):
        got = sc.blocking_findings(path)
        assert [(f["id"], f["theme"]) for f in got] == want, path
        for f in got:
            assert f["heading"] is not None, (path, f["id"])
            assert f["cited"], (path, f["id"])


# ------------------------------------------------------------------ 2. parse_ids
def test_parse_ids_baseline_reports():
    want = {"a3-r1": ["F1", "F2"], "a3-r2": ["R1-B1", "R1-B2"], "a3-r3": ["F1", "F2", "F3"], "a3-r4": ["F-01"],
            "a3-r5": ["F-1", "F-2", "F-3"], "a3-r6": ["REQ-1", "REQ-2", "ARCH-1"]}
    for run, ids in want.items():
        assert sc.parse_ids(sc.ids_from(rd(run, f"ws/{REV}/round1.md"))) == ids, run


def test_parse_ids_strings():
    assert sc.parse_ids("none (F1, F2 and F3 are resolved; no new blocking finding)") == []
    assert sc.parse_ids(None) == []
    assert sc.parse_ids("NEW-1. Nothing else. REQ-1, REQ-2 and ARCH-1 are resolved") == ["NEW-1"]
    assert sc.parse_ids("**F1, F2**") == ["F1", "F2"]
    assert sc.parse_ids("AC-1, F1") == ["F1"]          # AC is an excluded prefix


# ------------------------------------------------------------------ 3. basetokens
def test_basetokens_reproduces_section_2(h):
    import glob
    if not glob.glob("/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"):
        pytest.skip("no transcripts readable")
    per = h.basetokens("/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output")
    want_loop = {"a3-r1": 70694, "a3-r2": 109207, "a3-r3": 95213, "a3-r4": 81415, "a3-r5": 94998, "a3-r6": 151017}
    want_aud = {"a3-r1": 52531, "a3-r2": 78276, "a3-r3": 69081, "a3-r4": 59033, "a3-r5": 84759, "a3-r6": 70581}
    if set(per) != set(want_loop):
        pytest.skip("not all baseline transcripts present")
    for r in want_loop:
        assert abs(sum(v for s, v in per[r].items() if s != "AUD") - want_loop[r])/want_loop[r] < 0.01, r
        assert abs(per[r]["AUD"] - want_aud[r])/want_aud[r] < 0.01, r
    assert abs(statistics.mean(sum(v for s, v in per[r].items() if s != "AUD") for r in per) - 100424)/100424 < 0.01
    assert abs(statistics.mean(per[r]["AUD"] for r in per) - 69044)/69044 < 0.01


# ------------------------------------------------------------------ 4. build
def test_build(h):
    h.build()
    names = sorted(p.name for p in h.RUNS.iterdir())
    assert names == [f"b2-r{k}" for k in range(1, 7)]
    for r in names:
        assert h.sha(h.ws(r)/h.SPEC) == h.SPEC_SHA
        assert h.sha(h.run_dir(r)/"command.md") == h.AUD_CMD_SHA          # this design does not change spec-panel
        assert "### VERIFY prompt" in (h.run_dir(r)/"home/.claude/rules/prompts/document_review_loop_prompts.md").read_text()
        st = h.load(r)
        assert st["stratum"] == "sonnet" and st["loop_model"] == "sonnet" and st["product_ref"] == h.PRODUCT_REF
        assert (h.ws(r)/h.D/"review").is_dir() and (h.ws(r)/h.D/"specs/history").is_dir()
    assert not (h.P11/"rules.md").read_text().count("### VERIFY prompt")     # p11 rules.md untouched


# ------------------------------------------------------------------ 5. prompt identity
def _swap(text, run_dir_path, base):
    return text.replace(str(run_dir_path), base)


def test_prompt_identity(h):
    h.build()
    run = "b2-r1"; d = h.run_dir(run); base = str(P11R/"a3-r1")
    h.prep(run, "R1")
    assert _swap((d/"PROMPT-R1.md").read_text(), d, base) == (P11R/"a3-r1/PROMPT-R1.md").read_text()
    h.prep(run, "V1", {"IDS": "F1, F2"})
    assert _swap((d/"PROMPT-V1.md").read_text(), d, base) == (P11R/"a3-r1/PROMPT-V1.md").read_text()
    h.prep(run, "R2")
    assert _swap((d/"PROMPT-R2.md").read_text(), d, base) == (P11R/"a3-r1/PROMPT-R2.md").read_text()
    h.prep(run, "AUD")
    h.prep(run, "AUD2")
    aud = _swap((d/"PROMPT-AUD.md").read_text(), d, base)
    assert aud == (P11R/"a3-r1/PROMPT-AUD.md").read_text()
    aud2 = _swap((d/"PROMPT-AUD2.md").read_text(), d, base).replace("/aud2", "/aud")
    assert aud2 == aud
    # R3 of a3-r6
    h.prep(run, "R3")
    assert _swap((d/"PROMPT-R3.md").read_text(), d, str(P11R/"a3-r6")) == (P11R/"a3-r6/PROMPT-R3.md").read_text()


# ------------------------------------------------------------------ 6. finding list and verifier sandbox
def _put_report(h, run, name, src):
    p = h.ws(run)/REV/name
    shutil.copy(src, p)
    return p


def test_finding_list_and_verifier_prompt(h):
    h.build(); run = "b2-r1"
    _put_report(h, run, "round1.md", rd("a3-r3", f"ws/{REV}/round1.md"))
    text, ids = h.findings(run, 1)
    assert ids == ["F1", "F2", "F3"]
    for fid in ids:
        assert f"### {fid}\n### {fid}." in text
    assert not re.search(r"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?\s*recommendation", text)
    p = h.prep(run, "VF1")
    vd = h.run_dir(run)/"vf1"
    files = [x for x in vd.rglob("*") if x.is_file()]
    assert [str(x.relative_to(vd)) for x in files] == [f"ws/{h.SPEC}"]
    assert sorted(x.name for x in vd.iterdir()) == ["home", "ws"]
    prompt = p.read_text()
    assert "Verify the blocking findings listed below" in prompt and "`confirmed: <ids>`" in prompt
    for fid in ids:
        assert f"### {fid}" in prompt
    assert "README" not in prompt
    assert f"{h.D}/review/verify-1.md" in prompt
    assert (h.ws(run)/REV/"findings-1.md").read_text().startswith("### F1")


# ------------------------------------------------------------------ 7. parse_verify
def test_parse_verify():
    t1 = ("| id | found text | exists | follows | decision | reason |\n|---|---|---|---|---|---|\n"
          "| F1 | x | yes | yes | confirm | holds |\n| F2 | y | no | no | reject | quoted text absent |\n"
          "| F3 | z | yes | yes | confirm | holds |\n\nconfirmed: F1, F3\n")
    from harness import parse_verify
    r, ok = parse_verify(t1, ["F1", "F2", "F3"])
    assert ok and r["F1"][0] == "confirm" and r["F2"] == ("reject", "quoted text absent") and r["F3"][0] == "confirm"
    r, ok = parse_verify("Reasoning only.\nconfirmed: F1\n", ["F1", "F2"])
    assert ok and r["F1"][0] == "confirm" and r["F2"] == ("reject", "not in confirmed line")
    r, ok = parse_verify("confirmed: none\n", ["F1", "F2"])
    assert ok and all(v[0] == "reject" for v in r.values())
    r, ok = parse_verify("", ["F1", "F2"])
    assert not ok and all(v[0] == "confirm" for v in r.values())
    r, ok = parse_verify("| F1 | a | yes | no | cannot confirm, reject | the outcome does not follow |\nconfirmed: none\n", ["F1"])
    assert r["F1"][0] == "reject"
    r, ok = parse_verify("| F1 | a | yes | yes | confirm | ok |\n| F10 | b | no | no | reject | no |\nconfirmed: F1\n", ["F1", "F10"])
    assert r["F1"][0] == "confirm" and r["F10"][0] == "reject"       # F1 does not match inside F10


# ------------------------------------------------------------------ helpers to drive the state machine
def old(p):
    t = time.time() - 600
    os.utime(p, (t, t))


def write_out(h, run, step, content):
    p = h.out_path(run, step); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content); old(p)
    return p


def launches(capsys):
    out = capsys.readouterr().out
    return [ln for ln in out.splitlines() if ln.startswith("LAUNCH")], out


R1_FAIL = rd("a3-r3", f"ws/{REV}/round1.md").read_text()
R2_PASS = rd("a3-r3", f"ws/{REV}/round2.md").read_text()
AUD_FAIL = rd("a3-r3", AUDREP).read_text()
AUD_PASS = rd("a3-r5", AUDREP).read_text()


def reply(rejected=(), ids=("F1", "F2", "F3")):
    rows = "".join(f"| {i} | text | {'no' if i in rejected else 'yes'} | {'no' if i in rejected else 'yes'} | "
                   f"{'reject' if i in rejected else 'confirm'} | {'quote absent' if i in rejected else 'holds'} |\n" for i in ids)
    conf = ", ".join(i for i in ids if i not in rejected) or "none"
    return "| id | found | exists | follows | decision | reason |\n|---|---|---|---|---|---|\n" + rows + f"\nconfirmed: {conf}\n"


# ------------------------------------------------------------------ 8. happy path
def test_happy_path(h, monkeypatch, capsys):
    monkeypatch.setattr(h, "MAX_CONCURRENT", 100)
    h.build(); run = "b2-r1"
    advance.main([]); l, _ = launches(capsys)
    assert len(l) == 6 and all("PROMPT-R1.md" in x and "model=sonnet" in x for x in l)
    write_out(h, run, "R1", R1_FAIL)
    advance.main([]); l, out = launches(capsys)
    assert l == [f"LAUNCH {h.run_dir(run)}/PROMPT-VF1.md model=sonnet"], out
    write_out(h, run, "VF1", reply(rejected=("F2",)))
    advance.main([]); l, out = launches(capsys)
    assert l == [f"LAUNCH {h.run_dir(run)}/PROMPT-V1.md model=sonnet"], out
    assert "IDS=F1, F3." in (h.run_dir(run)/"PROMPT-V1.md").read_text()
    r1 = (h.ws(run)/REV/"round1.md").read_text().splitlines()
    assert r1[0] == "review: 1 of 3" and r1[1].startswith("> verification")
    assert "confirmed blocking ids: F1, F3" in r1[1] and "F2 (verifier: quote absent)" in r1[1]
    assert (h.ws(run)/REV/"round1.orig.md").read_text() == R1_FAIL
    assert "F2" in (h.run_dir(run)/"NOTED.md").read_text()
    assert (h.ws(run)/h.D/"specs/history/spec-v1.md").exists()
    st = h.load(run)
    assert st["log"]["VF1"]["confirmed"] == ["F1", "F3"] and list(st["log"]["VF1"]["rejected"]) == ["F2"]
    write_out(h, run, "V1", "# revise 1\n")
    advance.main([]); l, out = launches(capsys)
    assert l == [f"LAUNCH {h.run_dir(run)}/PROMPT-R2.md model=sonnet"], out
    assert "--re-review .dev/orca-command-refactor/review/round1.md" in (h.run_dir(run)/"PROMPT-R2.md").read_text()
    write_out(h, run, "R2", R2_PASS)
    advance.main([]); l, out = launches(capsys)
    assert sorted(l) == sorted([f"LAUNCH {h.run_dir(run)}/PROMPT-AUD.md model=sonnet", f"LAUNCH {h.run_dir(run)}/PROMPT-AUD2.md model=sonnet"]), out
    assert h.load(run)["loop_end"] == "PASS"
    write_out(h, run, "AUD", AUD_FAIL); write_out(h, run, "AUD2", AUD_PASS)
    advance.main([]); capsys.readouterr()
    st = h.load(run)
    assert st["complete"] and st["log"]["AUD"]["verdict"] == "FAIL" and st["log"]["AUD2"]["verdict"] == "PASS"
    assert [b["id"] for b in st["log"]["AUD"]["blocking"]] == ["F-1", "F-2"]


# ------------------------------------------------------------------ 9. reject everything
def test_all_rejected_is_verified_pass(h, monkeypatch, capsys):
    monkeypatch.setattr(h, "MAX_CONCURRENT", 100)
    h.build(); run = "b2-r1"
    advance.main([]); capsys.readouterr()
    write_out(h, run, "R1", R1_FAIL)
    advance.main([]); capsys.readouterr()
    write_out(h, run, "VF1", reply(rejected=("F1", "F2", "F3")))
    advance.main([]); l, out = launches(capsys)
    assert h.load(run)["loop_end"] == "VERIFIED-PASS"
    assert sorted(x.split("/")[-1] for x in l) == ["PROMPT-AUD.md model=sonnet", "PROMPT-AUD2.md model=sonnet"], out
    assert not (h.run_dir(run)/"PROMPT-V1.md").exists()
    assert len(h.load(run)["noted_unactioned"]) == 3


# ------------------------------------------------------------------ 10. VF3 confirmed -> ESCALATED
def test_vf3_confirmed_escalates(h, monkeypatch, capsys):
    monkeypatch.setattr(h, "MAX_CONCURRENT", 100)
    h.build(); run = "b2-r1"
    advance.main([]); capsys.readouterr()
    for r, vf, v in (("R1", "VF1", "V1"), ("R2", "VF2", "V2")):
        write_out(h, run, r, R1_FAIL.replace("review: 1 of 3", f"review: {r[1]} of 3", 1))
        advance.main([]); capsys.readouterr()
        write_out(h, run, vf, reply())
        advance.main([]); capsys.readouterr()
        write_out(h, run, v, "# revise\n")
        advance.main([]); capsys.readouterr()
    write_out(h, run, "R3", R1_FAIL.replace("review: 1 of 3", "review: 3 of 3", 1))
    advance.main([]); l, _ = launches(capsys)
    assert l == [f"LAUNCH {h.run_dir(run)}/PROMPT-VF3.md model=sonnet"]
    write_out(h, run, "VF3", reply())
    advance.main([]); l, _ = launches(capsys)
    assert h.load(run)["loop_end"] == "ESCALATED" and len(l) == 2
    assert not (h.run_dir(run)/"PROMPT-V3.md").exists()


# ------------------------------------------------------------------ manual paths
def test_no_ids_waits_for_setids_and_incomplete_relaunches_once(h, monkeypatch, capsys):
    monkeypatch.setattr(h, "MAX_CONCURRENT", 100)
    h.build(); run = "b2-r1"
    advance.main([]); capsys.readouterr()
    noids = "review: 1 of 3\n\n# report\n\nverdict: FAIL\n"
    write_out(h, run, "R1", noids)
    advance.main([]); l, out = launches(capsys)
    assert "MANUAL b2-r1 R1 no blocking ids parsed" in out and not l
    h.setids(run, "R1", "F1, F2")
    advance.main([]); l, out = launches(capsys)
    assert [x.split("/")[-1] for x in l] == ["PROMPT-VF1.md model=sonnet"]
    assert h.load(run)["manual"][0]["ids"] == "F1, F2"
    run2 = "b2-r2"
    write_out(h, run2, "R1", "review: 1 of 3\nverdict: INCOMPLETE\n")
    advance.main([]); l, out = launches(capsys)
    assert f"MANUAL {run2} R1" in out and any("b2-r2/PROMPT-R1.md" in x for x in l)
    write_out(h, run2, "R1", "review: 1 of 3\nverdict: INCOMPLETE\n")
    advance.main([]); l, out = launches(capsys)
    assert h.load(run2)["lost"] is True


# ------------------------------------------------------------------ 11. concurrency
def test_concurrency_and_dry_run(h, capsys):
    h.build()
    advance.main(["--dry-run"]); out = capsys.readouterr().out
    assert out.count("DRYRUN") == 6
    assert all(not h.load(r)["launched"] for r in h.run_names())
    advance.main([]); l, _ = launches(capsys)
    assert len(l) == 6
    advance.main([]); l, out = launches(capsys)
    assert l == [] and "RUNNING 6" in out
    # a finished worker frees a slot
    write_out(h, "b2-r1", "R1", R1_FAIL)
    advance.main([]); l, out = launches(capsys)
    assert len(l) == 1 and "PROMPT-VF1.md" in l[0]


# ------------------------------------------------------------------ 12. tokens
def _transcript(path, run, step, model, msgs):
    lines = [json.dumps({"type": "user", "message": {"role": "user", "content":
             f"Read /x/scratchpad/p12/ab2/runs/{run}/PROMPT-{step}.md and follow it exactly. Touch nothing."}})]
    for mid, toks, extra in msgs:
        lines.append(json.dumps({"type": "assistant", "message": {"id": mid, "role": "assistant", "model": model,
                                 "usage": {"output_tokens": toks}, "content": extra}}))
    path.write_text("\n".join(lines) + "\n")


def test_tokens_dedupe_and_model_warn(h, tmp_path, monkeypatch, capsys):
    h.build()
    tdir = tmp_path/"tasks"; tdir.mkdir()
    done = [{"type": "tool_use", "name": "SubagentHandback", "input": {"message": "DONE /x"}}]
    _transcript(tdir/"a.output", "b2-r1", "R1", "claude-sonnet-5-5",
                [("m1", 100, [{"type": "thinking"}]), ("m1", 100, [{"type": "text", "text": "x"}]), ("m2", 50, done)])
    _transcript(tdir/"b.output", "b2-r1", "R1", "claude-opus-4", [("o1", 9999, [])])
    monkeypatch.setattr(h, "TASKS_GLOB", str(tdir/"*.output"))
    h.tokens()
    out = capsys.readouterr().out
    assert h.load("b2-r1")["log"]["R1"]["output_tokens"] == 150
    assert "WARN" in out and "opus" in out
    found = h.ab_transcripts()
    assert found[("b2-r1", "R1")][0]["done"] or found[("b2-r1", "R1")][1]["done"]


# ------------------------------------------------------------------ 13. convention, strata, extension
def _complete_state(h, run, loop, aud_tok, blk1, blk2, loop_end="PASS", rejected=0, sent=0, matched=False):
    st = h.load(run)
    mk = lambda n, th="T1": [{"id": f"F-{i}", "heading": "x", "theme": th, "cited": [60, 61]} for i in range(n)]
    st["log"] = {"R1": {"output_tokens": loop}, "AUD": {"verdict": "FAIL" if blk1 else "PASS", "blocking": mk(blk1), "output_tokens": aud_tok},
                 "AUD2": {"verdict": "FAIL" if blk2 else "PASS", "blocking": mk(blk2), "output_tokens": aud_tok}}
    if sent:
        st["log"]["VF1"] = {"finding_ids": [f"R{i}" for i in range(sent)], "confirmed": [f"R{i}" for i in range(rejected, sent)],
                            "rejected": {f"R{i}": "absent" for i in range(rejected)}, "parse_ok": True}
        st["noted_unactioned"] = [{"step": "VF1", "id": f"R{i}", "theme": "T1" if matched else "T3", "cited": [60] if matched else [300],
                                   "heading": "h", "reason": "absent"} for i in range(rejected)]
    st["loop_end"] = loop_end; st["complete"] = True; st["final_spec"] = {"bytes": 58000}
    h.save(run, st)


def test_cost_convention_and_decision(h):
    dec = h.decision()
    assert dec["COST_LIMIT_R_LOOP"] == 1.42
    assert round((1.25*169468 - 69044)/100424, 2) == 1.42
    c = h.cost_ratios(120424, 69044)
    assert abs(c["R_LOOP"] - 120424/100424) < 1e-9 and abs(c["R_B"] - (120424 + 69044)/169468) < 1e-9
    # R_B limit (1.25) holds, R_LOOP limit fails -> decided by R_LOOP
    h.build()
    runs = h.run_names()
    for r in runs:
        _complete_state(h, r, loop=145000, aud_tok=10000, blk1=1, blk2=2, rejected=1, sent=3)
    sr = h.load_runs("sonnet")
    res = h.outcome_rules(sr, 6, {"B_BLK": 1.5}, dec)
    assert res["R_B"] < 1.25 and res["R_LOOP"] > dec["COST_LIMIT_R_LOOP"]
    assert res["outcome"] == "DROP" and res["drops"] == ["DROP-2"]
    # cheap enough and fewer blockers -> ADOPT
    for r in runs:
        _complete_state(h, r, loop=120000, aud_tok=69044, blk1=1, blk2=1, rejected=1, sent=3)
    res = h.outcome_rules(h.load_runs("sonnet"), 6, {"B_BLK": 1.5}, dec)
    assert res["outcome"] == "ADOPT", res
    # REJ = 0 is INCONCLUSIVE, never ADOPT
    for r in runs:
        _complete_state(h, r, loop=120000, aud_tok=69044, blk1=1, blk2=1)
    assert h.outcome_rules(h.load_runs("sonnet"), 6, {"B_BLK": 1.5}, dec)["outcome"] == "INCONCLUSIVE"
    # DROP-1: rejected findings that match audit blockers
    for r in runs:
        _complete_state(h, r, loop=120000, aud_tok=69044, blk1=1, blk2=1, rejected=2, sent=3, matched=True)
    res = h.outcome_rules(h.load_runs("sonnet"), 6, {"B_BLK": 1.5}, dec)
    assert res["REJ_TRUE"] == 12 and res["outcome"] == "DROP" and res["drops"][0] == "DROP-1"
    # DROP-3 on loop PASS count
    for i, r in enumerate(runs):
        _complete_state(h, r, loop=120000, aud_tok=69044, blk1=1, blk2=1, rejected=1, sent=3, loop_end="ESCALATED" if i < 2 else "PASS")
    assert h.outcome_rules(h.load_runs("sonnet"), 6, {"B_BLK": 1.5}, dec)["drops"] == ["DROP-3"]


def test_haiku_stratum_and_extension(h, capsys, monkeypatch):
    monkeypatch.setattr(h, "MAX_CONCURRENT", 100)
    h.build(); h.build("haiku")
    assert [r for r in h.run_names() if r.startswith("b2h-")] == [f"b2h-r{k}" for k in range(1, 5)]
    for r in h.run_names():
        st = h.load(r)
        assert st["stratum"] == ("haiku" if r.startswith("b2h-") else "sonnet")
        assert st["loop_model"] == st["stratum"]
    advance.main([]); l, _ = launches(capsys)
    assert len(l) == 10                                                   # Sonnet runs are printed first, then Haiku
    assert all("/b2-r" in x and "model=sonnet" in x for x in l[:6])
    assert all("/b2h-r" in x and "PROMPT-R1.md" in x and "model=haiku" in x for x in l[6:])
    write_out(h, "b2h-r1", "R1", "review: 1 of 3\nverdict: PASS\n")
    advance.main([]); l, out = launches(capsys)
    assert sorted(x.split("/")[-2:] for x in l) == [["b2h-r1", "PROMPT-AUD.md model=sonnet"], ["b2h-r1", "PROMPT-AUD2.md model=sonnet"]], out
    # fail-closed: Haiku can never be asked to audit
    st = h.load("b2h-r2"); st["pending"].append("AUD"); h.save("b2h-r2", st)
    assert h.loop_model_of(st, "AUD") == "sonnet" and h.loop_model_of(st, "R1") == "haiku"
    # Haiku runs never enter the Sonnet BLK_T
    for r in h.run_names():
        _complete_state(h, r, loop=120000, aud_tok=69044, blk1=1 if r.startswith("b2-") else 9, blk2=1 if r.startswith("b2-") else 9,
                        rejected=1, sent=3)
    res = h.outcome_rules(h.load_runs("sonnet"), 6, {"B_BLK": 1.5}, h.decision())
    assert res["BLK_T"] == 1.0
    assert statistics.mean(len(r["aud1"]["blocking"]) for r in h.load_runs("haiku")) == 9
    # extension: refused unless INCONCLUSIVE; once only
    with pytest.raises(SystemExit):
        h.build(extend=True)
    json.dump({"sonnet_n6_outcome": "ADOPT"}, open(h.AB/"metrics.json", "w"))
    with pytest.raises(SystemExit):
        h.build(extend=True)
    json.dump({"sonnet_n6_outcome": "INCONCLUSIVE"}, open(h.AB/"metrics.json", "w"))
    h.build(extend=True)
    assert [r for r in h.run_names() if r.startswith("b2-r")][-3:] == ["b2-r7", "b2-r8", "b2-r9"]
    with pytest.raises(SystemExit):
        h.build(extend=True)


def test_analyze_end_to_end(h):
    h.build(); h.build("haiku")
    for r in h.run_names():
        hk = r.startswith("b2h-")
        _complete_state(h, r, loop=118000, aud_tok=69044, blk1=5 if hk else 1, blk2=5 if hk else 1, rejected=1, sent=3)
    m = h.analyze()
    assert m["stratum_sonnet"]["full"]["outcome"] in ("ADOPT", "INCONCLUSIVE", "DROP")
    assert (h.AB/"metrics.json").exists() and (h.AB/"RESULTS-tables.md").exists()
    tables = (h.AB/"RESULTS-tables.md").read_text()
    assert "R_LOOP" in tables and "R_B" in tables and "Haiku stratum" in tables
    assert m["sonnet_n6_outcome"] == m["stratum_sonnet"]["full"]["outcome"] or m["sonnet_n6_outcome"] == "INCONCLUSIVE"
    # not finished -> outcome stays PENDING and the extension cannot be armed early
    st = h.load("b2-r6"); st["complete"] = False; h.save("b2-r6", st)
    m = h.analyze()
    assert m["sonnet_n6_outcome"] == "PENDING" and m["extension_allowed"] is False


def test_no_cost_kill_in_tooling():
    """D6: nothing in the live loop driver reads tokens or costs; only analyze (post-hoc) does."""
    adv = (pathlib.Path(__file__).resolve().parents[1]/"advance.py").read_text()
    code = "\n".join(ln for ln in adv.splitlines() if not ln.lstrip().startswith(("#", '"""')))
    for bad in ("output_tokens", "R_LOOP", "cost_ratios", "A_BASE", "tokens("):
        assert bad not in code, bad
    hz = (pathlib.Path(__file__).resolve().parents[1]/"harness.py").read_text()
    live = hz.split("# ---------------------------------------------------------------- analysis")[0]
    assert "sys.exit" not in re.sub(r"def build.*?def new_brief", "", live, flags=re.S).replace("sys.exit(__doc__)", "")
