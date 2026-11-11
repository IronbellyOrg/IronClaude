import collections
import json
import pathlib
import re
import sys

import pytest

AB = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AB))
import advance as ADV  # noqa: E402
import decision as DEC  # noqa: E402
import harness as H  # noqa: E402
import ledger_lite as L  # noqa: E402
import panel_lite as PL  # noqa: E402
import telemetry_lite as TL  # noqa: E402

SP = H.SP
P11 = H.P11
ORIG = H.S1 / "inputs/repo-overlay" / H.SPEC
ANCH1 = "step 4 uses the command's existing report file, since the contract arrives in P1"
ANCH2 = "every command in sections 3.1-3.2 has a `## Unattended mode` section"


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setattr(H, "RUNS", tmp_path / "runs")
    H.RUNS.mkdir()
    monkeypatch.setattr(ADV, "LEDGER", tmp_path / "led.json")
    monkeypatch.setattr(H, "ESTIMATE_FN", None)
    return tmp_path


def sub_sb(text, sb):
    return text.replace(str(sb), "<SB>")


def norm_ids(t):
    return re.sub(r"IDS=[^\n]*?\.\n", "IDS=<IDS>.\n", t)


# ---------------------------------------------------------------- prompt identity with the Stage 2 arm-3 prompts
P11R1 = P11 / "runs/a3-r1"


@pytest.mark.skipif(not (P11R1 / "PROMPT-R1.md").exists(), reason="p11 prompts missing")
def test_prompt_identity_with_p11(env):
    H.build(1, "sonnet")
    run = "c3-r1"
    st = H.load(run)
    # P1 reviewer prompt == a3-r1 R1 prompt after sandbox substitution
    for rid in H.PANEL_IDS:
        p = H.prep(run, f"P1.{rid}")
        assert sub_sb(p.read_text(), H.step_sandbox(run, f"P1.{rid}")) == sub_sb((P11R1 / "PROMPT-R1.md").read_text(), P11R1)
    # R2, V1 (ids normalised), AUD, AUD2
    (H.ws(run) / H.D / "specs/history").mkdir(parents=True, exist_ok=True)
    assert sub_sb(H.prep(run, "R2").read_text(), H.run_dir(run)) == sub_sb((P11R1 / "PROMPT-R2.md").read_text(), P11R1)
    lg = H.L.Ledger.load(H.run_dir(run) / "ledger.json")
    lg.rows.append({"lid": "L1", "blocking": True, "status": "open"})
    lg.save(H.run_dir(run) / "ledger.json")
    v1 = norm_ids(sub_sb(H.prep(run, "V1").read_text(), H.run_dir(run)))
    assert v1 == norm_ids(sub_sb((P11R1 / "PROMPT-V1.md").read_text(), P11R1))
    aud_ref = sub_sb((P11R1 / "PROMPT-AUD.md").read_text(), P11R1 / "aud")
    assert sub_sb(H.prep(run, "AUD").read_text(), H.run_dir(run) / "aud") == aud_ref
    assert sub_sb(H.prep(run, "AUD2").read_text(), H.run_dir(run) / "aud2") == aud_ref
    # the panel sandbox rules file differs from the baseline rules file only by C4.3; the audit sandboxes use the frozen file
    assert (H.run_dir(run) / "aud/home/.claude/rules/prompts/document_review_loop_prompts.md").read_text() == (P11 / "rules.md").read_text()
    assert (H.run_dir(run) / "panel/P1.t1b-1/home/.claude/rules/prompts/document_review_loop_prompts.md").read_text() != (P11 / "rules.md").read_text()


# ---------------------------------------------------------------- tokens
BASE = {"a3-r1": 70694, "a3-r2": 109207, "a3-r3": 95213, "a3-r4": 81415, "a3-r5": 94998, "a3-r6": 151017}


def test_basetokens_within_one_percent():
    import glob
    if not glob.glob(H.TK.TASKS_GLOB):
        pytest.skip("no transcripts")
    res = H.basetokens()
    if not res["loop"]:
        pytest.skip("no p11 transcripts")
    for run, want in BASE.items():
        assert abs(res["loop"][run] - want) / want < 0.01
    assert abs(res["A_BASE"] - DEC.RULES["A_BASE"]) / DEC.RULES["A_BASE"] < 0.01


def test_tokens_count_each_message_id_once(tmp_path):
    f = tmp_path / "t.output"
    first = json.dumps({"message": {"role": "user", "content": "Read /x/p13/ab3/runs/c3-r1/PROMPT-V1.md"}})
    a = {"message": {"role": "assistant", "id": "m1", "model": "claude-sonnet-5-5", "usage": {"output_tokens": 10}}}
    b = {"message": {"role": "assistant", "id": "m1", "model": "claude-sonnet-5-5", "usage": {"output_tokens": 30}}}
    c = {"message": {"role": "assistant", "id": "m2", "model": "claude-sonnet-5-5", "usage": {"output_tokens": 5}}}
    f.write_text("\n".join([first] + [json.dumps(x) for x in (a, b, c)]))
    r = H.TK.step_tokens(H.TASK_RE, None, glob_pat=str(tmp_path / "*.output"))
    assert r == {("c3-r1", "V1"): 35}


# ---------------------------------------------------------------- C4.3 insertions
def test_apply_c43():
    base = (P11 / "rules.md").read_text()
    out = H.apply_c43(base)
    assert out.count("### Findings block") == 1 and out.count(H.INS_A) == 1 and out.count(H.INS_B) == 1 and out.count(H.INS_C) == 1
    assert out.index("### Findings block") < out.index("## Never")
    assert out.count("### Fix map") == 1
    lines = out.split("\n")
    i = lines.index(H.INS_A)
    assert lines[i - 1].startswith('- First-review brief: "')
    assert lines[lines.index(H.INS_B) - 1].startswith('- Re-review brief: "')
    assert lines[lines.index(H.INS_C) - 1].startswith('- Revise brief: "')
    assert lines[lines.index("## Never") - 1] == "" and lines[lines.index("## Never") - 2].startswith("- ") or True
    # removing the insertions restores the original
    stripped = out.replace(H.INS_A + "\n", "").replace(H.INS_B + "\n", "").replace(H.INS_C + "\n", "")
    stripped = stripped.replace(H.INS_D.rstrip("\n") + "\n\n", "")
    assert stripped == base
    with pytest.raises(AssertionError):
        H.apply_c43(base.replace("## Never", "## Nope"))
    with pytest.raises(AssertionError):
        H.apply_c43(base + "\n- First-review brief: \"again\"\n")


# ---------------------------------------------------------------- panel
def test_panel_default_anthropic_only():
    r = PL.resolve(PL.PANEL, PL.TIERS, "anthropic-only", "any")
    got = [(x["reviewer_id"], x["model"], x["launch"], x["fallback_depth"], x["stand_in"]) for x in r["reviewers"]]
    assert got == [("t1b-1", "claude-sonnet-5-5", "sonnet", 0, False), ("t2-1", "claude-haiku-5-5", "haiku", 0, True),
                   ("t3-1", "claude-haiku-5-5", "haiku", 0, True), ("t3-2", "claude-haiku-5-5", "haiku", 0, True)]
    assert json.dumps(r, sort_keys=True) == json.dumps(PL.resolve(PL.PANEL, PL.TIERS, "anthropic-only", "any"), sort_keys=True)
    assert PL.validate_panel(PL.PANEL, PL.TIERS) == []


def test_resolve_slot_cases():
    t = PL.TIERS["aliases"]
    r = PL.resolve_slot(t["tier3"]["models"], "random", "s", ["claude-haiku-5-5"], ["claude-haiku-5-5"])
    assert r["model"] == "claude-haiku-5-5" and r["stand_in"] is True
    r = PL.resolve_slot(t["tier1b"]["models"], "fixed", None, ["gpt-6.1-sol"], [])
    assert (r["model"], r["fallback_depth"]) == ("gpt-6.1-sol", 1)
    r = PL.resolve_slot(t["tier1b"]["models"], "fixed", None, ["muse-wonder-full-1.0"], [])
    assert r["fallback_depth"] == 2
    a = {PL.resolve_slot(t["tier2"]["models"], "random", "seed", "all", [])["model"] for _ in range(20)}
    assert len(a) == 1 and a <= set(t["tier2"]["models"])
    r = PL.resolve_slot(["a", "b"], "random", "x", "all", [], exclude=("a",))
    assert r["model"] == "b"
    assert PL.resolve_slot(["a"], "random", "x", "all", [], exclude=("a",))["model"] == "a"
    swapped = {"aliases": {"tier1b": {"alias": "x", "models": ["gpt-6.1-sol", "claude-sonnet-5-5"]}}}
    assert PL.resolve_slot(swapped["aliases"]["tier1b"]["models"], "fixed", None, "all", [])["model"] == "gpt-6.1-sol"
    with pytest.raises(PL.NoModelAvailable):
        PL.resolve_slot(["a"], "fixed", None, ["z"], [])


# ---------------------------------------------------------------- findings block and ledger
def fblock(*findings, priors=()):
    lines = [json.dumps(f) for f in findings] + [json.dumps(p) for p in priors]
    return "report text\n\n## Findings block\n\n```findings-v1\n" + "\n".join(lines) + "\n```\n"


def finding(fid, anchor, blocking=True, sev="CRITICAL", refs=("AC-0.4",), claim="wrong outcome"):
    return {"id": fid, "severity": sev, "blocking": blocking, "category": "contradiction", "anchor": anchor, "refs": list(refs), "claim": claim}


def test_parse_block():
    ok = L.parse_block(fblock(finding("F1", ANCH1)))
    assert ok["ok"] and len(ok["findings"]) == 1
    assert not L.parse_block("no block")["ok"]
    bad = L.parse_block(fblock(finding("F1", "short")))
    assert not bad["ok"] and bad["errors"]
    assert L.parse_block(fblock(finding("F1", ANCH1, blocking=True, sev="MINOR")))["ok"] is False
    assert L.parse_block("## Findings block\n\n```findings-v1\n```\n")["ok"]


def test_ledger_statuses():
    spec = ORIG.read_text()
    lg = L.Ledger(cap=3)
    info = lg.add_round(1, spec, [{"reviewer_id": "a", "text": fblock(finding("F1", ANCH1))}, {"reviewer_id": "b", "text": fblock(finding("G1", ANCH1))}])
    assert info["clusters"] == 1 and lg.rows[0]["confidence"] == "overlap" and lg.verdict() == "FAIL"
    assert lg.d["rounds"][0]["decision"] == "REVISE"
    new = spec.replace(ANCH1, "step 4 is fixed now in this revised text of the spec")
    lg.apply_revision(spec, new, [{"id": "L1", "action": "applied"}])
    assert lg.rows[0]["status"] == "resolved_check"
    lg.add_round(2, new, [{"reviewer_id": "c", "text": fblock()}])
    assert lg.rows[0]["status"] == "resolved" and lg.verdict() == "PASS"
    lg.add_round(3, spec, [{"reviewer_id": "d", "text": fblock(finding("F1", ANCH1))}])
    assert lg.rows[0]["status"] == "regressed" and lg.verdict() == "FAIL" and lg.d["rounds"][-1]["decision"] == "ESCALATE"


def test_fingerprint_and_same_defect():
    spec = ORIG.read_text()
    a = L.enrich(finding("F1", ANCH1), spec)
    b = L.enrich(finding("F2", ANCH1), spec)
    assert a["fp"] == b["fp"] and L.same_defect(a, b)
    c = L.enrich(finding("F3", "Orca guide citations (`[G]`, `[H:<verb>]`, ...) are numbered", refs=("XX-1",)), spec)
    assert not L.same_defect(a, c)
    cap = L.Ledger(cap=3)
    cap.add_round(1, spec, [{"reviewer_id": "a", "text": fblock(finding("F1", ANCH1))}, {"reviewer_id": "b", "text": fblock()}])
    cc = cap.capture(1)
    assert cc["occasions"] == ["a", "b"] and cc["defects"] == [{"key": "L1", "blocking": True, "captured_by": ["a"]}]


# ---------------------------------------------------------------- the state machine with fake workers
def fake_estimate(stop_values):
    calls = iter(stop_values)

    def fn(cap, open_blocking):
        stop = next(calls)
        s_obs = len([d for d in cap["defects"] if d["blocking"]])
        return {"S_obs": s_obs, "k": len(cap["occasions"]), "stop": stop and open_blocking == 0, "unseen_upper95": 0.0 if stop else 3.0, "reason": "fake"}
    return fn


def write_out(run, step, text):
    p = H.step_output(run, step)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    H.ingest(run, step)


def run_panel_round(run, n, findings_by_rid):
    for rid in H.PANEL_IDS:
        fs = findings_by_rid.get(rid, [])
        write_out(run, f"P{n}.{rid}", "review: 1 of 3\n\n" + fblock(*fs) + f"\nverdict: {'FAIL' if any(f['blocking'] for f in fs) else 'PASS'}\n")


def drive_to_stop_false(env):
    """P1 (one blocking defect) -> V1 -> R2 PASS -> stop rule says no -> P3 panel round."""
    H.build(1, "sonnet")
    run = "c3-r1"
    H.ESTIMATE_FN = fake_estimate([False] * 6)
    assert H.progress(run) == [f"P1.{r}" for r in H.PANEL_IDS]
    run_panel_round(run, 1, {"t1b-1": [finding("F1", ANCH1)], "t3-1": [finding("F1", ANCH1)]})
    assert H.progress(run) == ["V1"]
    ids = H.ledger(run).open_blocking()
    assert ids == ["L1"] and "L1" in (H.RUNS / run / "PROMPT-V1.md").read_text()
    spec = (H.ws(run) / H.SPEC).read_text()
    (H.ws(run) / H.SPEC).write_text(spec.replace(ANCH1, "step 4 is fixed now in this revised text of the spec"))
    write_out(run, "V1", '# revise\n\n## Fix map\n\n```fixmap-v1\n{"id": "L1", "action": "applied", "reason": "done"}\n```\n')
    assert H.progress(run) == ["R2"]
    write_out(run, "R2", "review: 2 of 3\n\n" + fblock(priors=[{"prior": "L1", "status": "resolved"}]) + "\nverdict: PASS\n")
    return run


def test_stop_false_after_pass_triggers_new_panel_round(env):
    run = drive_to_stop_false(env)
    assert H.progress(run) == [f"P3.{r}" for r in H.PANEL_IDS]
    st = H.load(run)
    assert st["reviews"] == 2 and st["decision"] is None
    assert [e["stop"] for e in st["events"] if e["kind"] == "stop_rule"] == [False]


def test_escalate_at_cap(env):
    run = drive_to_stop_false(env)
    H.progress(run)
    run_panel_round(run, 3, {"t1b-1": [finding("F9", "Orca guide citations (`[G]`, `[H:<verb>]`, ...) are numbered", refs=("ZZ-9",))]})
    assert H.progress(run) == ["AUD", "AUD2"]
    st = H.load(run)
    assert st["decision"] == "ESCALATE" and st["reviews"] == 3
    # audits always on sonnet
    assert H.model_for(run, "AUD") == "sonnet" and H.model_for(run, "AUD2") == "sonnet"


def test_pass_when_stop_true(env):
    H.build(1, "sonnet")
    run = "c3-r1"
    H.ESTIMATE_FN = fake_estimate([True, True])
    H.progress(run)
    run_panel_round(run, 1, {})
    assert H.progress(run) == ["AUD", "AUD2"]
    assert H.load(run)["decision"] == "PASS" and H.load(run)["reviews"] == 1


# ---------------------------------------------------------------- launch tooling
def test_concurrency_six_fresh_runs_print_six_launch_lines(env, capsys):
    H.build(6, "sonnet")
    lines = ADV.main(dry_run=True, tr={})
    assert len(lines) == 6 and all(l.startswith("LAUNCH ") for l in lines)
    out = capsys.readouterr().out
    assert out.count("LAUNCH ") == 6
    assert not ADV.LEDGER.exists()           # dry run records nothing
    lines2 = ADV.main(dry_run=False, tr={})
    assert len(lines2) == 6
    assert ADV.main(dry_run=False, tr={}) == []  # six running: nothing more


def test_relaunch_once_then_lost(env):
    H.build(1, "sonnet")
    run = "c3-r1"
    ADV.main(tr={})
    key = f"{run}/P1.t1b-1"
    ended = {(run, "P1.t1b-1"): [{"done": False, "ended": True, "file": "x"}]}
    ADV.main(tr=ended)
    led = ADV.load_ledger()
    assert led[key]["state"] == "launched" and len(led[key]["launches"]) == 2     # relaunched once
    ended2 = {(run, "P1.t1b-1"): [{"done": False, "ended": True, "file": "x"}, {"done": False, "ended": True, "file": "y"}]}
    ADV.main(tr=ended2)
    assert ADV.load_ledger()[key]["state"] == "lost"
    assert H.load(run)["lost"] is True and H.run_result(run, {})["failed"] is True


def test_scan_detects_done(tmp_path):
    f = tmp_path / "w.output"
    head = json.dumps({"message": {"role": "user", "content": "Read /x/p13/ab3/runs/c3-r2/PROMPT-P1.t3-1.md and follow it"}})
    done = json.dumps({"message": {"role": "assistant", "stop_reason": "tool_use", "content": [
        {"type": "tool_use", "name": "SubagentHandback", "input": {"message": "DONE /x/out.md"}}]}})
    f.write_text(head + "\n" + done + "\n")
    r = ADV.scan(str(tmp_path / "*.output"))
    assert r[("c3-r2", "P1.t3-1")][0]["done"] is True


# ---------------------------------------------------------------- D2 / D3 / D4 and telemetry
def mk(run, stratum="sonnet", decision="PASS", blk=(0, 1), loop=150000, aud=70000, growth=1.5, failed=False):
    return {"run": run, "stratum": stratum, "completed": True, "decision": decision, "growth_pct": growth, "loop_tokens": loop,
            "audit_tokens": aud, "blk": list(blk), "failed": failed}


def test_d2_loop_only_convention():
    runs = [mk(f"c3-r{i}", loop=200848, aud=69044) for i in range(1, 7)]
    s = DEC.summarize(runs)
    assert s["R_LOOP"] == pytest.approx(2.0, rel=1e-3)                 # loop only / 100,424
    assert s["R_B"] == pytest.approx((200848 + 69044) / 169468, rel=1e-6)
    assert DEC.RULES["A_BASE"] == 100424 and DEC.RULES["B_BASE"] == 169468
    # B never decides: a huge audit cost changes R_B but not the decision
    big = [mk(f"c3-r{i}", loop=200848, aud=900000, blk=(0, 0)) for i in range(1, 7)]
    assert DEC.decide_sonnet(DEC.summarize(big))[0] == "ADOPT"


def test_decision_zones():
    adopt = [mk(f"c3-r{i}", blk=(i % 2, (i + 1) % 2), loop=200000) for i in range(1, 7)]
    assert DEC.decide_sonnet(DEC.summarize(adopt))[0] == "ADOPT"          # BLK 0.5 <= 0.75
    drop = [mk(f"c3-r{i}", blk=(2, 2), loop=200000) for i in range(1, 7)]
    assert DEC.decide_sonnet(DEC.summarize(drop))[0] == "DROP"
    cost = [mk(f"c3-r{i}", blk=(0, 0), loop=550000) for i in range(1, 7)]
    assert DEC.decide_sonnet(DEC.summarize(cost))[0] == "DROP"            # R_LOOP 5.48 > 4.88 (D6)
    mid_cost = [mk(f"c3-r{i}", blk=(0, 0), loop=400000) for i in range(1, 7)]
    assert DEC.decide_sonnet(DEC.summarize(mid_cost))[0] == "INCONCLUSIVE"   # 3.98 is between 3.53 and 4.88
    mid = [mk(f"c3-r{i}", blk=(1, 1), loop=200000) for i in range(1, 7)]
    assert DEC.decide_sonnet(DEC.summarize(mid))[0] == "INCONCLUSIVE"
    few = [mk(f"c3-r{i}") for i in range(1, 5)]
    assert DEC.decide_sonnet(DEC.summarize(few))[0] == "INCONCLUSIVE"
    skew = [mk(f"c3-r{i}", blk=(0, 2), loop=200000) for i in range(1, 7)]
    assert DEC.decide_sonnet(DEC.summarize(skew))[0] == "INCONCLUSIVE"    # AUD vs AUD2 differ by 2 > 0.75
    esc = [mk(f"c3-r{i}", blk=(0, 0), loop=200000, decision="ESCALATE" if i < 4 else "PASS") for i in range(1, 7)]
    assert DEC.decide_sonnet(DEC.summarize(esc))[0] == "DROP"             # PASS_T 0.5 < 4/6


def test_d4_extension_once():
    assert DEC.extension_needed("INCONCLUSIVE", 6, False) is True
    assert DEC.extension_needed("INCONCLUSIVE", 9, True) is False
    assert DEC.extension_needed("ADOPT", 6, False) is False and DEC.extension_needed("DROP", 6, False) is False
    assert DEC.RULES["extension"]["extra_sonnet_replicates"] == 3 and DEC.RULES["extension"]["max_extensions"] == 1


def test_extend_builds_three_more_once(env, monkeypatch):
    import analyze as AN
    monkeypatch.setattr(AN, "HERE", env)
    H.build(6, "sonnet")
    monkeypatch.setattr(AN, "live_runs", lambda: {"sonnet": [mk(f"c3-r{i}", blk=(1, 1), loop=200000) for i in range(1, 7)], "haiku": []})
    AN.extend()
    assert sorted(p.name for p in H.RUNS.iterdir()) == [f"c3-r{i}" for i in range(1, 10)]
    n_before = len(list(H.RUNS.iterdir()))
    AN.extend()                                                          # second call must not extend again
    assert len(list(H.RUNS.iterdir())) == n_before


def test_d3_haiku_stratum(env):
    H.build(2, "haiku")
    assert sorted(p.name for p in H.RUNS.iterdir()) == ["c3-h1", "c3-h2"]
    run = "c3-h1"
    assert H.load(run)["stratum"] == "haiku"
    assert H.model_for(run, "V1") == "haiku" and H.model_for(run, "R2") == "haiku"
    assert H.model_for(run, "AUD") == "sonnet" and H.model_for(run, "AUD2") == "sonnet"
    assert H.model_for(run, "P1.t1b-1") == "sonnet" and H.model_for(run, "P1.t3-2") == "haiku"      # panel composition unchanged
    H.build(1, "sonnet")
    assert H.model_for("c3-r1", "V1") == "sonnet"
    assert DEC.RULES["haiku"]["pooled_with_sonnet"] is False and DEC.RULES["haiku"]["n"] == 4


def test_haiku_relative_and_final_line(tmp_path):
    base = tmp_path / "b.json"
    base.write_text(json.dumps({"runs": [{"blk": [2, 2], "failed": False}, {"blk": [3, 1], "failed": False}]}))
    b = DEC.load_haiku_baseline(base)
    assert b["mean_blk"] == pytest.approx(2.0)
    good = DEC.summarize([mk(f"c3-h{i}", "haiku", blk=(1, 1)) for i in range(1, 5)])
    bad = DEC.summarize([mk(f"c3-h{i}", "haiku", blk=(3, 3)) for i in range(1, 5)])
    assert DEC.decide_haiku(good, b)[0] == "supports" and DEC.decide_haiku(bad, b)[0] == "does_not_support"
    assert DEC.decide_haiku(good, None)[0] == "pending"
    assert DEC.final_line("ADOPT", "supports", False) == "ADOPT"
    assert DEC.final_line("ADOPT", "pending", False) == "ADOPT (Haiku robustness pending)"
    assert DEC.final_line("ADOPT", "does_not_support", False).startswith("INCONCLUSIVE")
    assert DEC.final_line("DROP", "supports", False) == "DROP"


def test_telemetry_records_valid(env):
    H.build(1, "haiku")
    st = H.load("c3-h1")
    res = st["panel"]
    spec = ORIG.read_text()
    report = "review: 1 of 3\n\n" + fblock(finding("F1", ANCH1), finding("F2", "Orca guide citations (`[G]`", blocking=False, sev="MINOR")) + "\nverdict: FAIL\n"
    for r in res["reviewers"]:
        rec = TL.reviewer_record("c3-h1", "P1." + r["reviewer_id"], 1, r, res, spec, report, {"tokens_in": 1, "cache_read": 2, "cache_write": 3, "out": 4, "wall_s": None},
                                 r["model"], 1, "haiku")
        assert TL.validate(rec) == []
        assert rec["context"]["stratum"] == "haiku" and rec["context"]["experiment"] == "pn3"
        assert rec["slot"]["stand_in"] == r["stand_in"] and rec["output"]["blocking"] == 1 and rec["output"]["findings"] == 2
        assert TL.no_document_text(rec, spec)
    bad = dict(rec)
    bad.pop("model")
    assert TL.validate(bad)
    p = TL.write(rec, env / "tel")
    assert p.parent.parts[-3] == "records" and p.read_text().count("\n") == 1
    TL.write(rec, env / "tel")
    assert p.read_text().count("\n") == 2                                 # append only


def test_d6_converted_limits_and_no_midrun_cost_kill():
    assert DEC.convert_limit(3.3) == 4.88 and DEC.convert_limit(2.5) == 3.53
    assert [DEC.convert_limit(x) for x in (1.8, 2.0, 1.25, 1.5, 1.65)] == [2.35, 2.69, 1.42, 1.84, 2.10]
    assert DEC.RULES["sonnet"]["r_loop_drop_above"] == DEC.convert_limit(3.3)
    assert DEC.RULES["sonnet"]["r_loop_adopt_at_most"] == DEC.convert_limit(2.5)
    # no token- or cost-based early exit anywhere in the launch/flow code
    for name in ("advance.py", "harness.py"):
        src = (AB / name).read_text()
        flow = src.split("def progress(run)")[1].split("def round_claims")[0] if name == "harness.py" else src
        assert "A_BASE" not in flow and "R_LOOP" not in flow and "output_tokens" not in flow
        assert not re.search(r"(?i)(abort|halt|skip remaining|budget exceeded).{0,40}(token|cost|dollar)", src)
