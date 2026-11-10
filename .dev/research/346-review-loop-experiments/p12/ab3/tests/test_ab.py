"""Offline tests of the A/B 3 tooling (harness.py, advance.py, score_themes.py).  Run:
   cd $AB && uv run --no-project --with pytest pytest -q tests
"""
import hashlib
import json
import os
import pathlib
import shutil
import sys
import time

import pytest

AB_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AB_DIR))
import advance  # noqa: E402
import harness as h  # noqa: E402
import score_themes as sc  # noqa: E402

SP = h.SP
P11 = h.P11
D = h.D
REVIEW = f"{D}/review"
OLD = time.time() - 600          # "10 minutes back"

AUD_OF = lambda a, r: P11 / f"runs/a{a}-r{r}/aud/ws/{h.AUD_OUT}"                        # noqa: E731
R1_OF = lambda a, r: P11 / f"runs/a{a}-r{r}/ws/{D}/review/round1.md"                    # noqa: E731
R2_OF = lambda a, r: P11 / f"runs/a{a}-r{r}/ws/{D}/review/round2.md"                    # noqa: E731


# ------------------------------------------------------------------------------------ fixtures / helpers
@pytest.fixture
def env(tmp_path, monkeypatch):
    ab = tmp_path / "ab"
    ab.mkdir()
    shutil.copy(AB_DIR / "decision.json", ab / "decision.json")
    (tmp_path / "tasks").mkdir()
    monkeypatch.setattr(h, "AB", ab)
    monkeypatch.setattr(h, "RUNS", ab / "runs")
    monkeypatch.setattr(h, "TASKS_GLOB", str(tmp_path / "tasks/*.output"))
    monkeypatch.setattr(h, "MAX_CONCURRENT", 6)
    return tmp_path


def put(path, src_or_text, old=True):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(src_or_text, pathlib.Path):
        shutil.copy(src_or_text, path)
    else:
        path.write_text(src_or_text)
    if old:
        os.utime(path, (OLD, OLD))
    return path


def finish(run, step, src):
    """Simulate a finished worker by writing its output file (mtime 10 minutes back)."""
    base = h.out_base(run, step)
    rel = h.AUD_OUT if step in ("AUD", "AUD2") else h.OUT[step]
    return put(base / rel, src)


def launches(capsys):
    out = capsys.readouterr().out
    return [ln for ln in out.splitlines() if ln.startswith("LAUNCH ")], out


def step_of(line):
    return pathlib.Path(line.split()[1]).name[len("PROMPT-"):-3], pathlib.Path(line.split()[1]).parent.name


def go(capsys, *argv):
    advance.main(list(argv))
    return launches(capsys)


# ------------------------------------------------------------------------------------ 1. scoring
SCORE_TABLE = {
    ("a2", 1): (("B-1", "T3"), ("B-2", "T1")), ("a2", 2): (("B1", "T1"), ("B2", "T2")), ("a2", 3): (),
    ("a2", 4): (("B-1", "T1"),), ("a2", 5): (("B-1", "T2"), ("B-2", "T3")), ("a2", 6): (("F-01", "T1"),),
    ("a3", 1): (("F1", "T3"), ("F2", "T1")), ("a3", 2): (("R1-B1", "T1"), ("R1-B2", "T2")),
    ("a3", 3): (("F1", "T1"), ("F2", "T1"), ("F3", "T3")), ("a3", 4): (("F-01", "T1"),),
    ("a3", 5): (("F-1", "T1"), ("F-2", "T3"), ("F-3", "other")), ("a3", 6): (("REQ-1", "T2"), ("REQ-2", "T1"), ("ARCH-1", "T2")),
}
AUDIT_TABLE = {
    ("a2", 1): (("F-1", "T1"), ("F-2", "T2")), ("a2", 2): (("F-01", "T2"), ("F-02", "T3")),
    ("a2", 3): (("REQ-1", "T1"), ("REQ-2", "T1"), ("ARCH-1", "T2")),
    ("a2", 4): (("F-1", "T1"), ("F-2", "T2"), ("F-3", "other")), ("a2", 5): (("F-1", "T1"),), ("a2", 6): (),
    ("a3", 1): (("B1", "T1"), ("B2", "T2")), ("a3", 2): (("F-01", "T3"), ("F-02", "T1")),
    ("a3", 3): (("F-1", "T1"), ("F-2", "T2")), ("a3", 4): (("A-01", "other"), ("A-02", "T2")), ("a3", 5): (),
    ("a3", 6): (("F-01", "T2"),),
}


@pytest.mark.parametrize("key", sorted(SCORE_TABLE))
def test_scoring_first_reviews_and_audits(key):
    a, r = key
    for path, table in ((R1_OF(int(a[1]), r), SCORE_TABLE), (AUD_OF(int(a[1]), r), AUDIT_TABLE)):
        fs = sc.blocking_findings(path)
        assert tuple((f["id"], f["theme"]) for f in fs) == table[key], path
        for f in fs:
            assert f["heading"] is not None, (path, f["id"])
            assert f["cited"], (path, f["id"])


# ------------------------------------------------------------------------------------ 2. parse_ids
def test_parse_ids_on_a3_round1():
    want = [["F1", "F2"], ["R1-B1", "R1-B2"], ["F1", "F2", "F3"], ["F-01"], ["F-1", "F-2", "F-3"], ["REQ-1", "REQ-2", "ARCH-1"]]
    got = [sc.parse_ids(sc.ids_from(R1_OF(3, r))) for r in range(1, 7)]
    assert got == want


def test_parse_ids_text_cases():
    assert sc.parse_ids("none (F1, F2 and F3 are resolved; no new blocking finding)") == []
    assert sc.parse_ids("NEW-1. Nothing else. REQ-1, REQ-2 and ARCH-1 are resolved") == ["NEW-1"]
    assert sc.parse_ids(None) == []
    assert sc.parse_ids("**F1, F2**, FR-3 and AC-1") == ["F1", "F2"]


def test_ids_regex_catches_long_label():
    t = "Reviser brief\n\nBlocking finding ids to repair, and only these: **F1, F2**\n\nverdict: FAIL\n"
    p = pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / "ids_label_test.md"
    p.write_text(t)
    assert sc.parse_ids(sc.ids_from(p)) == ["F1", "F2"]


# ------------------------------------------------------------------------------------ 3. basetokens
def test_basetokens_reproduces_section_2():
    r = h.basetokens(quiet=True)
    if r is None:
        pytest.skip("no baseline transcripts readable")
    assert abs(r["loop_mean"] - 100424) / 100424 < 0.01
    assert abs(r["audit_mean"] - 69044) / 69044 < 0.01
    assert len(r["loops"]) == 6


# ------------------------------------------------------------------------------------ 4. build
def test_build_spec_command_rules_and_frozen_audit(env):
    h.build()
    names = sorted(p.name for p in h.RUNS.iterdir())
    assert names == [f"b3-r{i}" for i in range(1, 7)]
    r = h.RUNS / "b3-r1"
    assert h.sha(r / "ws" / h.SPEC) == h.SPEC_SHA
    prod_cmd = h.git_show(h.PRODUCT_REF, "src/superclaude/commands/spec-panel.md")
    assert h.sha(r / "command.md") == hashlib.sha256(prod_cmd.encode()).hexdigest()
    assert h.sha(r / "command.md") != h.AUD_CMD_SHA
    assert "### GATE prompt" in (r / "home/.claude/rules/prompts/document_review_loop_prompts.md").read_text()
    assert not (h.P11 / "rules.md").stat().st_mtime > time.time() - 5          # build never writes p11/rules.md
    st = h.load("b3-r1")
    assert st["stratum"] == "sonnet" and st["loop_model"] == "sonnet" and st["product_ref"] == h.PRODUCT_REF
    # audits still get the frozen command and frozen rules
    p = h.prep("b3-r1", "AUD")
    assert h.sha(r / "aud/command.md") == h.AUD_CMD_SHA
    assert h.sha(r / "aud/home/.claude/rules/prompts/document_review_loop_prompts.md") == h.AUD_RULES_SHA
    assert p.name == "PROMPT-AUD.md"


# ------------------------------------------------------------------------------------ 5. prompt identity
def _norm(text, run, base_run):
    return text.replace(str(h.RUNS / run), str(P11 / "runs" / base_run))


def test_prompts_identical_to_stage2(env):
    h.build()
    run = "b3-r1"
    a31 = P11 / "runs/a3-r1"
    got = {}
    got["R1"] = h.prep(run, "R1").read_text()
    (h.ws(run) / h.OUT["R1"]).write_text("x")
    got["V1"] = h.prep(run, "V1", {"IDS": "F1, F2"}).read_text()
    got["R2"] = h.prep(run, "R2").read_text()
    got["AUD"] = h.prep(run, "AUD").read_text()
    for step in ("R1", "V1", "R2", "AUD"):
        assert _norm(got[step], run, "a3-r1") == (a31 / f"PROMPT-{step}.md").read_text(), step
    r3 = h.prep(run, "R3").read_text()
    assert _norm(r3, run, "a3-r6") == (P11 / "runs/a3-r6/PROMPT-R3.md").read_text()
    aud2 = h.prep(run, "AUD2").read_text()
    assert _norm(aud2, run, "a3-r1").replace("/aud2", "/aud") == (a31 / "PROMPT-AUD.md").read_text()
    import re
    a6 = P11 / "runs/a3-r6/PROMPT-V2.md"                                   # V2 exists only in a3-r6
    txt = a6.read_text()
    m = re.search(r"IDS=([^\n]*?)\.\nInputs", txt)
    assert m
    v2 = h.prep(run, "V2", {"IDS": m.group(1)}).read_text()
    assert _norm(v2, run, "a3-r6") == txt


# ------------------------------------------------------------------------------------ 6. gate sandbox
def test_gate_sandbox_and_prompt(env):
    h.build()
    run = "b3-r1"
    p = h.prep(run, "G")
    g = h.RUNS / run / "g"
    assert (g / "ws" / D / "README.md").exists()
    assert sorted(x.name for x in (g / "ws" / D / "inventory").iterdir()) == ["commands-a.md", "commands-b.md", "orca-capabilities.md"]
    assert h.sha(g / "ws" / h.SPEC) == h.SPEC_SHA
    assert (g / "command.md").read_text() == (h.RUNS / run / "command.md").read_text()
    assert "### GATE prompt" in (g / "home/.claude/rules/prompts/document_review_loop_prompts.md").read_text()
    assert list((g / "ws" / D / "review").iterdir()) == []
    assert not (g / "ws" / D / "specs" / "history").exists()
    text = p.read_text()
    assert "GATE prompt" in text and f"{D}/review/gate.md" in text and str(g) in text
    assert "FIRST-REVIEW" not in text


# ------------------------------------------------------------------------------------ loop paths
def _first_wave(env, capsys, n=6):
    h.build()
    ls, out = go(capsys)
    assert len(ls) == n and all(step_of(x)[0] == "R1" for x in ls)
    return ls


def _to_gate(capsys, run="b3-r3"):
    """R1 FAIL (a3-r3 round1) -> V1 -> R2 PASS (a3-r3 round2) -> G printed."""
    finish(run, "R1", R1_OF(3, 3))
    ls, out = go(capsys)
    assert [step_of(x) for x in ls] == [("V1", run)], out
    h.ws(run, ).joinpath(h.SPEC).write_text(h.ws(run).joinpath(h.SPEC).read_text() + "\nrevised\n")
    finish(run, "V1", "revise1 table\n")
    ls, out = go(capsys)
    assert [step_of(x) for x in ls] == [("R2", run)]
    finish(run, "R2", R2_OF(3, 3))
    ls, out = go(capsys)
    return ls, out


def test_path_r1_fail_v1_r2_pass_then_gate_not_audits(env, capsys):
    _first_wave(env, capsys)
    ls, out = _to_gate(capsys)
    assert [step_of(x) for x in ls] == [("G", "b3-r3")]
    assert "AUD" not in out
    assert (h.ws("b3-r3") / h.H / "spec-v1.md").exists()
    assert not (h.RUNS / "b3-r3" / "PROMPT-AUD.md").exists()


def test_gate_pass_ends_with_audits_together(env, capsys, monkeypatch):
    _first_wave(env, capsys)
    monkeypatch.setattr(h, "MAX_CONCURRENT", 12)
    _to_gate(capsys)
    finish_g("b3-r3", AUD_OF(3, 5))                      # a PASS report as the gate report
    ls, out = go(capsys)
    assert sorted(step_of(x)[0] for x in ls) == ["AUD", "AUD2"], out
    assert h.load("b3-r3")["loop_end"] == "GATE-PASS"
    assert h.load("b3-r3")["stratum"] == "sonnet"


def finish_g(run, src):
    return put(h.out_base(run, "G") / h.OUT["G"], src)


def test_stall_and_non_stall(env, capsys, monkeypatch):
    _first_wave(env, capsys)
    monkeypatch.setattr(h, "MAX_CONCURRENT", 12)
    _to_gate(capsys)
    # G FAIL repeating the run's own R1 findings -> STALLED
    finish_g("b3-r3", R1_OF(3, 3))
    ls, out = go(capsys)
    st = h.load("b3-r3")
    assert st["loop_end"] == "STALLED" and st["stall"]["auto"] is True
    assert {p[0] for p in st["stall"]["pairs"]} == {"F1", "F2", "F3"}
    assert sorted(step_of(x)[0] for x in ls) == ["AUD", "AUD2"]
    assert "GV" not in out


def test_gate_fail_new_findings_starts_gate_loop(env, capsys, monkeypatch):
    _first_wave(env, capsys)
    monkeypatch.setattr(h, "MAX_CONCURRENT", 12)
    _to_gate(capsys)
    r1 = sc.blocking_findings(R1_OF(3, 3))
    gs = sc.blocking_findings(AUD_OF(3, 1))                              # a3-r1 audit: B1 T1, B2 T2
    pairs = [(g["id"], e["id"], sc.same_defect(g, e)) for g in gs for e in r1]
    # the fake must not be a stall: at least one gate finding must match nothing in R1
    assert any(not any(same for gi, ei, same in pairs if gi == g["id"]) for g in gs), pairs
    finish_g("b3-r3", AUD_OF(3, 1))
    ls, out = go(capsys)
    st = h.load("b3-r3")
    assert st["stall"]["auto"] is False and st["loop_end"] is None
    assert [step_of(x) for x in ls] == [("GV", "b3-r3")]
    assert "IDS=B1, B2" in (h.RUNS / "b3-r3" / "PROMPT-GV.md").read_text()
    assert (h.ws("b3-r3") / h.H / "spec-g.md").exists()
    # GV -> GR (re-review brief names spec-g.md and the gate report)
    finish("b3-r3", "GV", "revise gate\n")
    ls, out = go(capsys)
    assert [step_of(x) for x in ls] == [("GR", "b3-r3")]
    t = (h.RUNS / "b3-r3" / "PROMPT-GR.md").read_text()
    assert f"--re-review {D}/review/gate.md --baseline {D}/specs/history/spec-g.md" in t
    assert f"{D}/review/gate-round2.md" in t
    # GR PASS -> GATE-LOOP-PASS
    finish("b3-r3", "GR", AUD_OF(3, 5))
    ls, out = go(capsys)
    assert h.load("b3-r3")["loop_end"] == "GATE-LOOP-PASS"
    assert sorted(step_of(x)[0] for x in ls) == ["AUD", "AUD2"]
    done = h.load("b3-r3")["done"]
    assert sum(s in h.REVIEW_STEPS for s in done) == 4 and sum(s in h.REVISE_STEPS for s in done) == 2   # R1, R2, G, GR / V1, GV


def test_gr_fail_escalates_and_r3_fail_has_no_gate(env, capsys, monkeypatch):
    _first_wave(env, capsys)
    monkeypatch.setattr(h, "MAX_CONCURRENT", 12)
    _to_gate(capsys)
    finish_g("b3-r3", AUD_OF(3, 1))
    go(capsys)
    finish("b3-r3", "GV", "x\n")
    go(capsys)
    finish("b3-r3", "GR", AUD_OF(3, 1))                                  # FAIL with ids B1, B2
    ls, out = go(capsys)
    assert h.load("b3-r3")["loop_end"] == "GATE-LOOP-ESCALATED"
    assert sorted(step_of(x)[0] for x in ls) == ["AUD", "AUD2"]
    # R3 FAIL -> ESCALATED, no G
    run = "b3-r2"
    finish(run, "R1", R1_OF(3, 3)); go(capsys)
    finish(run, "V1", "x\n"); go(capsys)
    finish(run, "R2", R1_OF(3, 3)); go(capsys)                           # a FAIL report as R2
    finish(run, "V2", "x\n"); go(capsys)
    finish(run, "R3", R1_OF(3, 3))
    ls, out = go(capsys)
    assert h.load(run)["loop_end"] == "ESCALATED"
    assert "G" not in [step_of(x)[0] for x in ls if step_of(x)[1] == run]
    assert not (h.RUNS / run / "PROMPT-G.md").exists()


def test_r1_pass_goes_to_gate(env, capsys):
    _first_wave(env, capsys)
    finish("b3-r1", "R1", R1_OF(2, 3))                                    # a2-r3 round1 is a PASS
    ls, out = go(capsys)
    assert [step_of(x) for x in ls] == [("G", "b3-r1")]


def test_manual_when_fail_without_ids_and_setids(env, capsys):
    _first_wave(env, capsys)
    put(h.ws("b3-r1") / h.OUT["R1"], "review: 1 of 3\nverdict: FAIL\n")
    ls, out = go(capsys)
    assert "MANUAL b3-r1 R1 no blocking ids parsed" in out and ls == []
    h.setids("b3-r1", "R1", "F1, F2")
    assert h.load("b3-r1")["manual"][-1]["ids"] == ["F1", "F2"]
    ls, out = go(capsys)
    assert [step_of(x) for x in ls] == [("V1", "b3-r1")]
    assert "IDS=F1, F2" in (h.RUNS / "b3-r1" / "PROMPT-V1.md").read_text()


def test_incomplete_relaunch_once_then_lost(env, capsys):
    _first_wave(env, capsys)
    put(h.ws("b3-r1") / h.OUT["R1"], "review: 1 of 3\nverdict: INCOMPLETE\n")
    ls, out = go(capsys)
    assert "MANUAL b3-r1 R1 verdict INCOMPLETE" in out and "relaunch once" in out
    assert [step_of(x) for x in ls] == [("R1", "b3-r1")]
    assert (h.ws("b3-r1") / (h.OUT["R1"] + ".attempt1")).exists()
    put(h.ws("b3-r1") / h.OUT["R1"], "review: 1 of 3\nverdict: INCOMPLETE\n")
    ls, out = go(capsys)
    assert h.load("b3-r1")["lost"] is True and "marked lost" in out


# ------------------------------------------------------------------------------------ 11. ceiling
def test_ceiling_refuses_sixth_review_and_fourth_fix(env):
    h.build()
    st = h.load("b3-r1")
    st["done"] = ["R1", "R2", "R3", "G", "GR"]
    h.save("b3-r1", st)
    with pytest.raises(AssertionError, match="ceiling of 5 reviews"):
        h.prep("b3-r1", "R4")
    st["done"] = ["V1", "V2", "GV"]
    with pytest.raises(AssertionError, match="ceiling of 3 fix cycles"):
        h.assert_ceiling(st, adding="V3")
    h.assert_ceiling({"run": "x", "done": ["R1", "V1", "R2", "V2", "R3", "G", "GV", "GR"]})   # the legal maximum: 5 reviews, 3 fix cycles


# ------------------------------------------------------------------------------------ 12. concurrency and tokens
def test_concurrency_dry_run_marks_nothing(env, capsys, monkeypatch):
    h.build()
    ls, out = go(capsys, "--dry-run")
    assert ls == [] and out.count("WOULD-LAUNCH") == 6
    assert all(h.load(r)["launched"] == {} for r in h.all_runs())
    assert (h.RUNS / "b3-r1" / "PROMPT-R1.md").exists()
    monkeypatch.setattr(h, "MAX_CONCURRENT", 3)
    ls, out = go(capsys)
    assert len(ls) == 3                                                   # at most MAX_CONCURRENT - running
    ls, out = go(capsys)
    assert ls == [] and "RUNNING 3" in out                                # three still running: nothing new
    monkeypatch.setattr(h, "MAX_CONCURRENT", 6)
    ls, out = go(capsys)
    assert len(ls) == 3
    ls, out = go(capsys)
    assert ls == [] and "RUNNING 6" in out


def _transcript(path, prompt, model, usage_lines, done_text=None, start=None):
    start = start or time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    lines = [json.dumps({"type": "user", "timestamp": start, "message": {"role": "user", "content": f"Read {prompt} and follow it exactly. Touch nothing outside the sandbox directory it names."}})]
    for mid, toks in usage_lines:
        lines.append(json.dumps({"type": "assistant", "message": {"role": "assistant", "id": mid, "model": model, "usage": {"output_tokens": toks},
                                                                  "content": [{"type": "text", "text": "x"}]}}))
    if done_text:
        lines.append(json.dumps({"type": "assistant", "message": {"role": "assistant", "id": "msg_last", "model": model, "usage": {"output_tokens": 5},
                                                                  "content": [{"type": "tool_use", "name": "SubagentHandback", "input": {"message": done_text}}]}}))
    pathlib.Path(path).write_text("\n".join(lines) + "\n")


def test_tokens_dedupe_by_message_id_and_model_warning(env, capsys):
    h.build()
    tdir = env / "tasks"
    prompt = f"/x/p12/ab3/runs/b3-r1/PROMPT-R1.md"
    # one message logged on two lines (same id, same usage) counts once; a bigger later copy wins (max)
    _transcript(tdir / "a1.output", prompt, "claude-sonnet-5-5", [("m1", 100), ("m1", 100), ("m2", 50), ("m2", 60)], done_text="DONE /x")
    # an Opus transcript for the same step is ignored with a warning
    _transcript(tdir / "a2.output", prompt, "claude-opus-4", [("o1", 9000)], done_text="DONE /x")
    # a planner transcript that merely mentions the prompt path is not a worker
    (tdir / "a3.output").write_text(json.dumps({"type": "user", "message": {"role": "user", "content": f"You are a planner. See {prompt}"}}) + "\n")
    sc_ = h.scan_transcripts("p12/ab3/runs", h.run_re_ab())
    assert list(sc_) == [("b3-r1", "R1")] and len(sc_[("b3-r1", "R1")]) == 2
    h.tokens_cmd()
    out = capsys.readouterr().out
    assert h.load("b3-r1")["log"]["R1"]["output_tokens"] == 100 + 60 + 5          # m1 once, m2 max, handback message
    assert "WARN b3-r1 R1 transcript a2.output" in out


def test_done_detection_uses_transcript_and_quiet_time(env, capsys):
    h.build()
    go(capsys)
    out = h.ws("b3-r1") / h.OUT["R1"]
    put(out, R1_OF(3, 3), old=False)                                      # fresh file, no transcript: still running
    ls, text = go(capsys)
    assert "R1 done" not in text and h.load("b3-r1")["done"] == []
    os.utime(out, (OLD, OLD))                                             # quiet for > 180 s: finished
    ls, text = go(capsys)
    assert "R1 done" in text
    # a transcript without DONE keeps the step running even when the file is old
    prompt = f"/x/p12/ab3/runs/b3-r2/PROMPT-R1.md"
    _transcript(env / "tasks/b.output", prompt, "claude-sonnet-5-5", [("m1", 10)])
    put(h.ws("b3-r2") / h.OUT["R1"], R1_OF(3, 4))
    ls, text = go(capsys)
    assert h.load("b3-r2")["done"] == []
    _transcript(env / "tasks/b.output", prompt, "claude-sonnet-5-5", [("m1", 10)], done_text="DONE /x")
    ls, text = go(capsys)
    assert "b3-r2" in text and h.load("b3-r2")["done"] == ["R1"]
    assert h.load("b3-r2")["log"]["R1"]["output_tokens"] == 15


def test_done_without_output_unlaunches_once_then_lost(env, capsys):
    h.build()
    go(capsys)
    prompt = f"/x/p12/ab3/runs/b3-r1/PROMPT-R1.md"
    _transcript(env / "tasks/c.output", prompt, "claude-sonnet-5-5", [("m1", 10)], done_text="DONE /x", start="2099-01-01T00:00:00.000Z")
    ls, out = go(capsys)
    assert "MANUAL b3-r1 R1 worker returned without output" in out
    assert [step_of(x) for x in ls] == [("R1", "b3-r1")]
    ls, out = go(capsys)
    assert h.load("b3-r1").get("lost") is True


# ------------------------------------------------------------------------------------ 13. convention, strata, extension
def forge_complete(run, loop_tok, aud_tok, a1, a2, loop_end="GATE-PASS", scoped=("R1",)):
    st = h.load(run)
    d = h.RUNS / run
    put(d / "aud/ws" / h.AUD_OUT, a1); put(d / "aud2/ws" / h.AUD_OUT, a2)
    st["done"] = list(scoped) + ["G", "AUD", "AUD2"]
    st["log"] = {s: {"output_exists": True, "output_tokens": 0, "verdict": "PASS"} for s in scoped}
    st["log"]["G"] = {"output_exists": True, "output_tokens": loop_tok, "verdict": "PASS"}
    st["log"]["AUD"] = {"output_exists": True, "output_tokens": aud_tok, "verdict": "PASS", "spec_audited": {"bytes": 57763}}
    st["log"]["AUD2"] = {"output_exists": True, "output_tokens": aud_tok, "verdict": "PASS"}
    st["loop_end"] = loop_end
    h.save(run, st)


def test_convention_r_loop_decides_over_r_b(env):
    h.build()
    for r in h.all_runs():
        forge_complete(r, 240000, 0, AUD_OF(3, 5), AUD_OF(3, 5))
    out = h.analyze(write=False)
    n = out["sonnet"]["numbers"]
    assert n["LOOP"] == 240000 and abs(n["R_LOOP"] - 240000 / 100424) < 1e-9
    assert abs(n["R_B"] - 240000 / 169468) < 1e-9
    assert n["R_B"] <= 1.8 and n["R_LOOP"] > 2.35                         # the R_B limit holds, the converted R_LOOP limit fails
    assert out["sonnet"]["pooled_outcome"] == "DROP"
    assert "DROP-3" in out["sonnet"]["pooled_rule"]
    for r in h.all_runs():                                                # 2.34 stays inside: loop 235,000 -> R_LOOP 2.340
        forge_complete(r, 235000, 69044, AUD_OF(3, 5), AUD_OF(3, 5))
    out = h.analyze(write=False)
    assert out["sonnet"]["numbers"]["R_LOOP"] < 2.35
    assert out["sonnet"]["pooled_outcome"] == "ADOPT"
    assert out["sonnet"]["final_outcome"] == "ADOPT (Haiku robustness pending)"
    assert abs(out["sonnet"]["numbers"]["R_B"] - (235000 + 69044) / 169468) < 1e-9


def test_d6_converted_limits_are_data_and_correct():
    c = json.load(open(AB_DIR / "decision.json"))
    r = c["rules"]
    assert r["DROP3_r_loop_max"]["value"] == round((r["DROP3_r_loop_max"]["original_L_on_R_B"] * 169468 - 69044) / 100424, 2) == 2.35
    ref = r["D6_converted_limits_reference"]
    for k, v in ref.items():
        L = float(k.split("=")[1])
        assert round((L * 169468 - 69044) / 100424, 2) == v
    assert c["cost_policy"]["mid_run_cost_kill"] is False
    assert (c["tokens"]["A_BASE"], c["tokens"]["AUD_BASE"], c["tokens"]["B_BASE"]) == (100424, 69044, 169468)
    # the thresholds reproduce the plan's counts
    from fractions import Fraction as F
    th = lambda p, n: F(p[0], p[1]) * n          # noqa: E731
    import math
    assert math.ceil(th(r["DROP1_theme_rate_min"], 12)) == 10 and math.ceil(th(r["DROP1_theme_rate_min"], 18)) == 15
    assert th(r["DROP2_final_pass_rate_min"], 6) == 4 and th(r["DROP2_final_pass_rate_min"], 9) == 6
    assert F(8, 10) * F(5, 6) * 12 == 8 and F(8, 10) * F(5, 6) * 18 == 12                  # ADOPT audit FAIL <= 8/12, 12/18


def test_no_cost_kill_or_hardcoded_thresholds_in_code():
    src = "".join((AB_DIR / f).read_text() for f in ("harness.py", "advance.py"))
    for forbidden in ("2.35", "1.8 ", "169468", "100424", "69044", "0.80"):
        assert forbidden not in src.replace("169,468", "").replace("100,424", ""), forbidden
    assert "budget" not in src.lower() and "abort" not in src.lower().replace("never aborts", "")


def test_haiku_stratum_models_and_isolation(env, capsys):
    h.build()
    h.build("haiku")
    names = h.all_runs()
    assert names == [f"b3-r{i}" for i in range(1, 7)] + [f"b3h-r{i}" for i in range(1, 5)]
    assert all(h.load(r)["stratum"] == "haiku" and h.load(r)["loop_model"] == "haiku" for r in names if "h-" in r)
    h.build("haiku")                                                      # idempotent
    ls, out = go(capsys)
    assert len(ls) == 6 and all("model=sonnet" in x for x in ls)          # Sonnet runs first
    assert all("b3-r" in x and "b3h" not in x for x in ls)
    # run to the AUD stage of a Haiku run: loop lines say haiku, AUD/AUD2 say sonnet
    hr = "b3h-r1"
    st = h.load(hr); st["done"] = ["R1"]; st["log"] = {"R1": {"verdict": "PASS", "output_exists": True}}; st["launched"] = {}
    h.save(hr, st)
    assert h.model_for(hr, "G") == "haiku" and h.model_for(hr, "R1") == "haiku"
    assert h.model_for(hr, "AUD") == "sonnet" and h.model_for(hr, "AUD2") == "sonnet"
    # Haiku runs never enter the Sonnet BLK_T
    for r in names:
        forge_complete(r, 100000, 69000, AUD_OF(3, 5) if "h-" not in r else AUD_OF(3, 1), AUD_OF(3, 5) if "h-" not in r else AUD_OF(3, 1))
    out = h.analyze(write=False)
    assert out["sonnet"]["numbers"]["n_runs"] == 6 and out["sonnet"]["numbers"]["BLK"] == 0
    assert out["haiku"]["numbers"]["n_runs"] == 4 and out["haiku"]["numbers"]["BLK"] == 2


def test_extension_refused_unless_inconclusive_and_only_once(env):
    h.build()
    with pytest.raises(SystemExit):
        h.build(extend=True)                                              # no metrics.json
    json.dump({"sonnet": {"sonnet_outcome": "DROP", "n_planned": 6}}, open(h.AB / "metrics.json", "w"))
    with pytest.raises(SystemExit):
        h.build(extend=True)
    json.dump({"sonnet": {"sonnet_outcome": "INCONCLUSIVE", "n_planned": 6}}, open(h.AB / "metrics.json", "w"))
    h.build(extend=True)
    assert [r for r in h.all_runs() if r.endswith(("r7", "r8", "r9"))] == ["b3-r7", "b3-r8", "b3-r9"]
    with pytest.raises(SystemExit):
        h.build(extend=True)                                              # never twice
    with pytest.raises(SystemExit):
        h.build("haiku", extend=True)


def test_drop1_and_replica_disagreement_and_fewer_than_five(env):
    h.build()
    for r in h.all_runs():
        forge_complete(r, 100000, 69000, AUD_OF(3, 1), AUD_OF(3, 1))      # T1/T2 blockers in every audit
    out = h.analyze(write=False)
    assert out["sonnet"]["pooled_outcome"] == "DROP" and "DROP-1" in out["sonnet"]["pooled_rule"]
    for r in h.all_runs():
        forge_complete(r, 100000, 69000, AUD_OF(3, 5), AUD_OF(3, 1))      # replica 1 clean, replica 2 themed
    out = h.analyze(write=False)
    assert out["sonnet"]["replica_outcomes"]["audit1"] != out["sonnet"]["replica_outcomes"]["audit2"]
    assert out["sonnet"]["sonnet_outcome"] == "INCONCLUSIVE"
    for r in ("b3-r1", "b3-r2"):
        h.lose(r)
    out = h.analyze(write=False)
    assert out["sonnet"]["sonnet_outcome"] == "INCONCLUSIVE" and "fewer than 5" in out["sonnet"]["pooled_rule"]


def test_theme_overrides_applied(env):
    h.build()
    for r in h.all_runs():
        forge_complete(r, 100000, 69000, AUD_OF(3, 1), AUD_OF(3, 1))
    json.dump({f"{r}/audit.md/B1": "other" for r in h.all_runs()} | {f"{r}/audit.md/B2": "other" for r in h.all_runs()},
              open(h.AB / "theme-overrides.json", "w"))
    out = h.analyze()
    assert out["sonnet"]["numbers"]["theme_audits"] == 0
    assert "Theme overrides applied" in (h.AB / "RESULTS-tables.md").read_text()
    assert json.load(open(h.AB / "metrics.json"))["sonnet"]["stratum"] == "sonnet"
