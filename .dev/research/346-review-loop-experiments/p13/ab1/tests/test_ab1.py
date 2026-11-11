"""Tests of the PN1 harness (design b1). Workers are faked by writing outputs and back-dating their mtimes."""
import hashlib, json, os, pathlib, re, subprocess, sys, time

import pytest

AB = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AB))
import advance  # noqa: E402
import analysis as A  # noqa: E402
import c93  # noqa: E402
import harness as h  # noqa: E402

D = h.D
P11 = h.P11
FIXT = AB / "fixtures"


@pytest.fixture(autouse=True)
def sandboxed(tmp_path, monkeypatch):
    monkeypatch.setattr(h, "RUNS", tmp_path / "runs")
    monkeypatch.setattr(h, "AB", tmp_path)
    monkeypatch.setattr(h, "TELEMETRY_DIR", tmp_path / "tel")
    monkeypatch.setattr(h, "TASKS_GLOB", str(tmp_path / "tasks/*.output"))
    (tmp_path / "tasks").mkdir()
    return tmp_path


def age(p, secs=1000):
    t = time.time() - secs
    os.utime(p, (t, t))


def fixture_block(lines):
    return "\n\n## Findings block\n\n```findings-v1\n" + "".join(l.rstrip("\n") + "\n" for l in lines) + "```\n"


def baseline_report(n):
    return (P11 / "runs/a3-r1/ws" / D / f"review/round{n}.md").read_text()


def fx(run, n):
    return [x for x in (FIXT / run / f"round{n}.findings").read_text().splitlines() if x.strip()]


def write_out(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    age(path)


def reviewer_out(run, n, rid):
    return h.out_path(run, f"R{n}.{rid}")


def launch_lines(capsys, *args):
    advance.main(list(args))
    return [l for l in capsys.readouterr().out.splitlines() if l.startswith("LAUNCH ")]


def fake_round1(run, reports):
    for rid, text in reports.items():
        write_out(reviewer_out(run, 1, rid), text)


R1_TEXT = lambda lines, v="FAIL": baseline_report(1).replace("verdict: FAIL", f"verdict: {v}") + fixture_block(lines)  # noqa: E731


def edit_spec(run, old, new):
    p = h.ws(run) / h.SPEC
    t = p.read_text()
    assert old in t
    p.write_text(t.replace(old, new))


# ------------------------------------------------------------------ 1. prompt identity
def sub(text, new_sb, old_sb):
    return text.replace(str(new_sb), str(old_sb))


def test_prompt_identity_with_stage2_arm3(sandboxed):
    h.build("sonnet", [1])
    run = "b1-r1"
    base1 = P11 / "runs/a3-r1"
    p, _ = h.prep_reviewer(run, 1, "t1b-1")
    assert sub(p.read_text(), h.run_dir(run) / "r1-t1b-1", base1) == (base1 / "PROMPT-R1.md").read_text()
    # R2: needs the merged round 1 report and spec-v1
    shutil_copy(base1 / "ws" / D / "review/round1.md", h.ws(run) / D / "review/round1.md")
    shutil_copy(base1 / "ws" / D / "specs/history/spec-v1.md", h.ws(run) / D / "specs/history/spec-v1.md")
    p, _ = h.prep_reviewer(run, 2, "t1b-1")
    assert sub(p.read_text(), h.run_dir(run) / "r2-t1b-1", base1) == (base1 / "PROMPT-R2.md").read_text()
    p, _ = h.prep_revise(run, 1, "F1, F2")
    assert sub(p.read_text(), h.run_dir(run), base1) == (base1 / "PROMPT-V1.md").read_text()
    p, _ = h.prep_audit(run, 1)
    assert sub(p.read_text(), h.run_dir(run) / "aud", base1 / "aud") == (base1 / "PROMPT-AUD.md").read_text()
    p2, _ = h.prep_audit(run, 2)
    assert sub(p2.read_text(), h.run_dir(run) / "aud2", base1 / "aud") == (base1 / "PROMPT-AUD.md").read_text()
    # R3 and V2 against a3-r6
    base6 = P11 / "runs/a3-r6"
    run3 = "b1-r2"
    h.build("sonnet", [2])
    for f in ("review/round2.md",):
        shutil_copy(base6 / "ws" / D / f, h.ws(run3) / D / f)
    shutil_copy(base6 / "ws" / D / "specs/history/spec-v2.md", h.ws(run3) / D / "specs/history/spec-v2.md")
    p, _ = h.prep_reviewer(run3, 3, "t1b-1")
    assert sub(p.read_text(), h.run_dir(run3) / "r3-t1b-1", base6) == (base6 / "PROMPT-R3.md").read_text()


def shutil_copy(a, b):
    import shutil
    pathlib.Path(b).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(a, b)


# ------------------------------------------------------------------ 2. basetokens
def test_basetokens_reproduces_arm3_loop_totals(capsys):
    if not list(__import__("glob").glob(h.TASKS_GLOB.replace(str(pathlib.Path(h.TASKS_GLOB).parent), "/tmp/claude-0/-home-user-IronClaude/*/tasks"))):
        pytest.skip("transcripts not readable")
    h.TASKS_GLOB = "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"
    a, u = h.basetokens()
    out = capsys.readouterr().out
    expect = {"a3-r1": 70694, "a3-r2": 109207, "a3-r3": 95213, "a3-r4": 81415, "a3-r5": 94998, "a3-r6": 151017}
    for run, want in expect.items():
        got = int(re.search(rf"{run} .*?loop (\d+)", out).group(1))
        assert abs(got - want) <= want * 0.01, (run, got, want)
    assert abs(a - 100424) < 5 and abs(a + u - 169468) < 10


# ------------------------------------------------------------------ 3. build
def test_build_asserts_and_panel(sandboxed):
    h.build("sonnet", [1])
    run = "b1-r1"
    d = h.run_dir(run)
    assert h.sha(h.ws(run) / h.SPEC) == h.SPEC_SHA
    assert hashlib.sha256((d / "command.md").read_bytes()).hexdigest() == h.AUD_CMD_SHA
    rules = (d / "home/.claude/rules/prompts/document_review_loop_prompts.md").read_text()
    assert "### Findings block" in rules and "### Fix map" in rules and "### Review panel" in rules
    want = subprocess.run([*h.CLI, "panel", "resolve", "--env", "anthropic-only", "--run-id", run, "--kind", "first"], capture_output=True, text=True).stdout
    assert json.loads((d / "panel.json").read_text()) == json.loads(want)
    rr = json.loads((d / "panel-rr.json").read_text())
    assert [r["reviewer_id"] for r in rr["reviewers"]] == ["t1b-1"]
    st = h.load(run)
    assert st["stratum"] == "sonnet" and st["panel"]["reviewers"][1]["model"] == "claude-haiku-5-5"
    # rules from PRODUCT_REF only differ from the frozen audit rules by the insertions
    assert hashlib.sha256((P11 / "rules.md").read_bytes()).hexdigest() == h.AUD_RULES_SHA


# ------------------------------------------------------------------ helpers for the loop tests
def run_to_round1_merged(capsys, run="b1-r1", extra=None):
    h.build("sonnet", [int(run.split("-r")[1])])
    assert len(launch_lines(capsys)) == 4
    f1 = fx("a3-r1", 1)
    reports = {"t1b-1": R1_TEXT(f1), "t2-1": R1_TEXT(f1[:1]), "t3-1": R1_TEXT(f1[1:]), "t3-2": R1_TEXT(f1)}
    reports.update(extra or {})
    fake_round1(run, reports)


# ------------------------------------------------------------------ 4 + 9 + 10. a full fake run
def test_full_fake_run_telemetry_and_adj_input(sandboxed, capsys):
    run = "b1-r1"
    run_to_round1_merged(capsys)
    # one transcript for t2-1 so that model.observed comes from it
    pr = h.prompt_path(run, "R1.t2-1")
    tr = sandboxed / "tasks/x1.output"
    tr.write_text("\n".join([
        json.dumps({"type": "user", "timestamp": "2026-11-10T10:00:00.000Z", "message": {"role": "user", "content": f"Read {pr} and follow it"}}),
        json.dumps({"type": "assistant", "timestamp": "2026-11-10T10:00:30.000Z", "message": {"role": "assistant", "model": "claude-haiku-5-5", "id": "m1", "usage": {"output_tokens": 1234, "input_tokens": 5}, "content": [{"type": "text", "text": "x"}]}}),
        json.dumps({"type": "assistant", "timestamp": "2026-11-10T10:00:31.000Z", "message": {"role": "assistant", "model": "claude-haiku-5-5", "id": "m1", "usage": {"output_tokens": 1234, "input_tokens": 5}, "content": [{"type": "tool_use", "name": "SubagentHandback", "input": {"message": "DONE"}}]}}),
    ]))
    out = launch_lines(capsys)
    st = h.load(run)
    assert "M1" in st["log"] and st["log"]["M1"]["verdict"] == "FAIL" and st["log"]["M1"]["decision"] == "REVISE"
    # V1 and ADJ are launched together after the merge
    assert sorted(l.split()[1] for l in out) == ["fable", "sonnet"]
    assert st["log"]["R1.t2-1"]["tokens"]["out"] == 1234 and st["log"]["R1.t2-1"]["tokens"]["model"] == "claude-haiku-5-5"
    # telemetry: one valid record per ingested reviewer (appended by the CLI, which validates)
    recs = [json.loads(l) for f in (sandboxed / "tel/records").rglob("*.jsonl") for l in f.read_text().splitlines()]
    assert len(recs) == 4 and {r["reviewer_id"] for r in recs} == {"t1b-1", "t2-1", "t3-1", "t3-2"}
    by = {r["reviewer_id"]: r for r in recs}
    assert by["t2-1"]["model"]["observed"] == "claude-haiku-5-5" and by["t2-1"]["cost"]["tokens_out"] == 1234
    assert by["t2-1"]["stratum"] == "sonnet" and by["t2-1"]["context"]["stratum"] == "sonnet"
    assert by["t1b-1"]["slot"]["stand_in"] is False and by["t3-1"]["slot"]["stand_in"] is True
    # ADJ input holds no reviewer id, model or severity
    adj = (h.run_dir(run) / "adj/ws" / D / "review/adj-input.md").read_text()
    for bad in ("t1b-1", "t2-1", "t3-1", "t3-2", "haiku", "sonnet", "claude", "CRITICAL", "MAJOR", "severity", "confidence", "overlap"):
        assert bad not in adj, bad
    assert adj.count("### X") == len(json.loads((h.ws(run) / D / "review/ledger.json").read_text())["rows"])
    # V1: edit the spec as the reviser would, write the fix map and the ADJ answer
    ids = st["log"]["M1"]["brief_ids"]
    edit_spec(run, "its report path is the WC-4 contract path", "its report path is the command's own report file")
    edit_spec(run, "step 4 uses the command's existing report file, since the contract arrives in P1", "step 4 uses the command's existing report file")
    fm = "".join(json.dumps({"id": i, "action": "applied", "reason": "r"}) + "\n" for i in ids)
    write_out(h.out_path(run, "V1"), "# Revise 1\n\n## Fix map\n\n```fixmap-v1\n" + fm + "```\n")
    mp = json.loads((h.run_dir(run) / "adj-map.json").read_text())
    write_out(h.out_path(run, "ADJ"), "adj\n\n```adj-v1\n" + "".join(json.dumps({"x": x, "verdict": "confirmed", "reason": "r"}) + "\n" for x in mp) + "```\n")
    out = launch_lines(capsys)
    st = h.load(run)
    assert st["log"]["L1"]["resolved_check"] == ids
    assert [l.split()[1] for l in out] == ["sonnet"] and "PROMPT-R2.t1b-1.md" in out[0]
    # the re-review prompt reads the merged round 1 report and the pre-revision snapshot
    assert (h.run_dir(run) / "r2-t1b-1/ws" / D / "review/round1.md").exists()
    # R2 passes
    write_out(reviewer_out(run, 2, "t1b-1"), baseline_report(2) + fixture_block([json.dumps({"prior": i, "status": "resolved"}) for i in ids]))
    out = launch_lines(capsys)
    st = h.load(run)
    assert st["log"]["M2"]["decision"] == "PASS" and st["log"]["M2"]["cleared"] == ids
    assert sorted(l.split()[2].split("/")[-1] for l in out) == ["PROMPT-AUD.md", "PROMPT-AUD2.md"]
    assert all(l.split()[1] == "sonnet" for l in out)               # D3: the audit is always Sonnet
    # audits
    for k in ("AUD", "AUD2"):
        write_out(h.out_path(run, k), (P11 / "runs/a3-r1/aud/ws" / D / "review/audit.md").read_text())
    launch_lines(capsys)
    st = h.load(run)
    assert st["phase"] == "complete" and st["final"]["reviews"] == 2 and st["final"]["decision"] == "PASS"
    assert st["log"]["AUD"]["blocking_ids"] == ["B1", "B2"]
    s = h.run_summary(run)
    assert s["audit_blocking"] == [2, 2] and s["pass"] is True and s["stratum"] == "sonnet"


# ------------------------------------------------------------------ 5. regression
def test_regressed_reflag_in_re_review_forces_revise(sandboxed, capsys):
    run = "b1-r1"
    run_to_round1_merged(capsys)
    launch_lines(capsys)
    ids = h.load(run)["log"]["M1"]["brief_ids"]
    edit_spec(run, "its report path is the WC-4 contract path", "its report path is the command's own report file")
    write_out(h.out_path(run, "V1"), "## Fix map\n\n```fixmap-v1\n" + "".join(json.dumps({"id": i, "action": "applied", "reason": "r"}) + "\n" for i in ids) + "```\n")
    launch_lines(capsys)
    again = json.dumps({"id": "N1", "severity": "CRITICAL", "blocking": True, "category": "unpassable-check",
                        "anchor": "step 4 uses the command's existing report file, since the contract arrives in P1", "refs": ["AC-0.4", "WC-4"], "claim": "still wrong"})
    edit_spec_file = h.ws(run) / h.SPEC
    assert "since the contract arrives in P1" in edit_spec_file.read_text()
    write_out(reviewer_out(run, 2, "t1b-1"), baseline_report(2).replace("verdict: PASS", "verdict: FAIL") + fixture_block([again]))
    launch_lines(capsys)
    m2 = h.load(run)["log"]["M2"]
    assert m2["regressed"] == ids and m2["decision"] == "REVISE" and m2["verdict"] == "FAIL"


# ------------------------------------------------------------------ 6. escalate at round 3
def test_escalate_at_round_three_goes_to_audits(sandboxed, capsys):
    run = "b1-r1"
    run_to_round1_merged(capsys)
    for n in (1, 2):
        launch_lines(capsys)
        st = h.load(run)
        ids = st["log"][f"M{n}"]["brief_ids"]
        write_out(h.out_path(run, f"V{n}"), "## Fix map\n\n```fixmap-v1\n" + "".join(json.dumps({"id": i, "action": "rejected", "reason": "no"}) + "\n" for i in ids) + "```\n")
        launch_lines(capsys)
        f = fx("a3-r1", 1)[1:]
        write_out(reviewer_out(run, n + 1, "t1b-1"), R1_TEXT(f).replace("review: 1 of 3", f"review: {n + 1} of 3"))
    out = launch_lines(capsys)
    st = h.load(run)
    assert st["log"]["M3"]["decision"] == "ESCALATE" and st["phase"] == "audit"
    assert len(out) == 2 and all("PROMPT-AUD" in l for l in out)


# ------------------------------------------------------------------ 7. lost reviewer
def test_lost_reviewer_merge_proceeds_with_three_reports(sandboxed, capsys):
    run = "b1-r1"
    f1 = fx("a3-r1", 1)
    run_to_round1_merged(capsys, extra={"t3-2": baseline_report(1).replace("verdict: FAIL", "verdict: INCOMPLETE")})
    out = launch_lines(capsys)                                   # t3-2 INCOMPLETE: relaunch once
    assert any("PROMPT-R1.t3-2.md" in l for l in out)
    write_out(reviewer_out(run, 1, "t3-2"), baseline_report(1).replace("verdict: FAIL", "verdict: INCOMPLETE"))
    launch_lines(capsys)
    st = h.load(run)
    assert st["lost"] == ["R1.t3-2"] and set(st["log"]["M1"]["block_ok"]) == {"t1b-1", "t2-1", "t3-1"}
    assert st["phase"] == "merged"


def test_two_lost_reviewers_lose_the_run(sandboxed, capsys):
    run = "b1-r1"
    bad = baseline_report(1).replace("verdict: FAIL", "verdict: INCOMPLETE")
    f1 = fx("a3-r1", 1)
    run_to_round1_merged(capsys, extra={"t3-1": bad, "t3-2": bad})
    launch_lines(capsys)
    write_out(reviewer_out(run, 1, "t3-1"), bad)
    write_out(reviewer_out(run, 1, "t3-2"), bad)
    launch_lines(capsys)
    assert h.load(run)["phase"] == "lost"


# ------------------------------------------------------------------ 8. concurrency
def test_concurrency_cap_and_dry_run(sandboxed, capsys):
    h.build("sonnet", [1, 2, 3, 4, 5, 6])
    lines = launch_lines(capsys, "--dry-run")
    assert len(lines) == 6
    assert all(h.load(r)["launched"] == {} for r in h.all_runs())
    lines = launch_lines(capsys)
    assert len(lines) == 6
    assert sum("b1-r1/PROMPT-R1." in l for l in lines) == 4 and sum("b1-r2/PROMPT-R1." in l for l in lines) == 2
    assert len(h.load("b1-r1")["launched"]) == 4 and len(h.load("b1-r2")["launched"]) == 2
    assert launch_lines(capsys) == []                              # six running: nothing more


# ------------------------------------------------------------------ D2: cost convention, D6: scaled limits, no mid-run cost kill
def test_cost_convention_loop_only_decides_and_limits_are_scaled():
    r = A.load_rules()
    tv = A.token_view([100424] * 6, [69044] * 6, r)
    assert tv["A"] == 100424 and tv["B"] == 169468 and abs(tv["R_LOOP"] - 1) < 1e-9 and abs(tv["R_B"] - 1) < 1e-9
    assert r["tokens"]["A_BASE"] == 100424 and r["tokens"]["AUD_BASE"] == 69044 and r["tokens"]["B_BASE"] == 169468
    assert A.convert_limit(3.3, r) == r["decision"]["drop2_r_loop"] == 4.88
    assert A.convert_limit(2.0, r) == r["decision"]["cost_hold_r_loop"] == 2.69
    for L, want in ((1.8, 2.35), (2.0, 2.69), (1.25, 1.42), (1.5, 1.84), (1.65, 2.10)):
        assert A.convert_limit(L, r) == want
    good = {"BLK_T": 0.5, "PASS_T": 1.0, "GROWTH_T": 0.01, "R_LOOP": 1.9, "BLOCK_OK": 1.0, "completed": 6, "audit_gap": 0.1}
    assert A.classify(good, r)["decision"] == "ADOPT"
    # R_B is never an input to the decision: only R_LOOP counts
    assert A.classify(dict(good, R_LOOP=2.8), r)["cost_hold"] is True and A.classify(dict(good, R_LOOP=2.8), r)["decision"] == "INCONCLUSIVE"
    assert A.classify(dict(good, R_LOOP=2.69), r)["decision"] == "ADOPT"
    assert A.classify(dict(good, R_LOOP=4.9), r)["decision"] == "DROP-2"
    assert A.classify(dict(good, BLK_T=1.25), r)["decision"] == "DROP-1"
    assert A.classify(dict(good, PASS_T=0.5), r)["decision"] == "DROP-3"
    assert A.classify(dict(good, GROWTH_T=0.05), r)["decision"] == "DROP-3"
    assert A.classify(dict(good, BLK_T=0.9), r)["decision"] == "INCONCLUSIVE"
    assert A.classify(dict(good, completed=4), r)["decision"] == "INCONCLUSIVE"
    assert A.classify(dict(good, audit_gap=0.8), r)["decision"] == "INCONCLUSIVE"
    assert A.classify(dict(good, BLOCK_OK=0.8), r)["decision"] == "INCONCLUSIVE"


def test_no_mid_run_cost_kill(sandboxed, capsys):
    """A transcript with an enormous token count changes nothing about the run's progress (D6)."""
    run = "b1-r1"
    h.build("sonnet", [1])
    launch_lines(capsys)
    f1 = fx("a3-r1", 1)
    pr = h.prompt_path(run, "R1.t1b-1")
    (sandboxed / "tasks/huge.output").write_text("\n".join([
        json.dumps({"type": "user", "message": {"role": "user", "content": f"Read {pr}"}}),
        json.dumps({"type": "assistant", "message": {"role": "assistant", "model": "claude-sonnet-5-5", "id": "m1", "usage": {"output_tokens": 50_000_000},
                                                      "content": [{"type": "tool_use", "name": "SubagentHandback", "input": {"message": "DONE"}}]}}),
    ]))
    fake_round1(run, {"t1b-1": R1_TEXT(f1), "t2-1": R1_TEXT(f1), "t3-1": R1_TEXT(f1), "t3-2": R1_TEXT(f1)})
    launch_lines(capsys)
    st = h.load(run)
    assert "M1" in st["log"] and st["phase"] == "merged"
    assert st["log"]["R1.t1b-1"]["tokens"]["out"] == 50_000_000
    src = (AB / "harness.py").read_text() + (AB / "advance.py").read_text() + (AB / "report.py").read_text()
    for banned in ("abort", "short-circuit", "truncate"):
        assert banned not in src, banned
    # tokens are read only in the post-step ingest path: no function that decides whether to launch reads a token count
    assert "R_LOOP" not in (AB / "advance.py").read_text() and "tokens" not in (AB / "advance.py").read_text().replace("tokens are", "")


# ------------------------------------------------------------------ D3: strata
def test_haiku_stratum_aliases_and_tags(sandboxed, capsys):
    h.build("haiku", [1])
    run = "b1h-r1"
    st = h.load(run)
    assert st["stratum"] == "haiku" and h.stratum_of(run) == "haiku"
    assert h.alias_for(run, "R1.t1b-1") == "sonnet" and h.alias_for(run, "R1.t3-1") == "haiku"      # panel composition unchanged
    assert h.alias_for(run, "R2.t1b-1") == "haiku" and h.alias_for(run, "R3.t1b-1") == "haiku"
    assert h.alias_for(run, "V1") == "haiku" and h.alias_for(run, "ADJ") == "haiku"
    assert h.alias_for(run, "AUD") == "sonnet" and h.alias_for(run, "AUD2") == "sonnet"
    assert launch_lines(capsys) == []                                            # default stratum is sonnet only
    assert len(launch_lines(capsys, "--stratum", "haiku")) == 4
    f1 = fx("a3-r1", 1)
    fake_round1(run, {r: R1_TEXT(f1) for r in ("t1b-1", "t2-1", "t3-1", "t3-2")})
    launch_lines(capsys, "--stratum", "haiku")
    recs = [json.loads(l) for f in (sandboxed / "tel/records").rglob("*.jsonl") for l in f.read_text().splitlines()]
    assert recs and all(r["stratum"] == "haiku" and r["context"]["stratum"] == "haiku" for r in recs)


def test_haiku_gate_and_final_decision_wording():
    r = A.load_rules()
    assert A.haiku_gate(None, None, r)["status"] == "pending"
    ok = A.haiku_gate({"n": 4, "mean_blk": 1.0, "lost_rate": 0.0}, {"n": 6, "mean_blk": 2.0, "lost_rate": 0.0}, r)
    assert ok["status"] == "ok" and abs(ok["ratio"] - 0.5) < 1e-9
    assert A.haiku_gate({"n": 4, "mean_blk": 2.5, "lost_rate": 0.0}, {"n": 6, "mean_blk": 2.0, "lost_rate": 0.0}, r)["status"] == "fail"
    assert A.haiku_gate({"n": 4, "mean_blk": 1.0, "lost_rate": 0.75}, {"n": 6, "mean_blk": 2.0, "lost_rate": 0.0}, r)["status"] == "fail"
    adopt = {"decision": "ADOPT"}
    assert A.final_decision(adopt, {"status": "pending"}) == "ADOPT (Haiku robustness pending)"
    assert A.final_decision(adopt, ok) == "ADOPT"
    assert A.final_decision(adopt, {"status": "fail"}) == "INCONCLUSIVE"
    assert A.final_decision({"decision": "DROP-1"}, ok) == "DROP-1"


def test_haiku_baseline_reader_is_tolerant(tmp_path):
    p = tmp_path / "results.json"
    assert h.load_haiku_baseline(p) is None
    p.write_text(json.dumps({"runs": {"h-r1": {"audit_blocking": [2, 3]}, "h-r2": {"audit_blocking": [1, 1]}, "h-r3": {"verdict": "lost"}}}))
    b = h.load_haiku_baseline(p)
    assert b["n"] == 3 and abs(b["mean_blk"] - 1.75) < 1e-9 and abs(b["lost_rate"] - 1 / 3) < 1e-9


# ------------------------------------------------------------------ D4: one-time extension
def test_extension_rule_is_once_and_only_when_inconclusive(sandboxed, monkeypatch, capsys):
    r = A.load_rules()
    assert A.extension_needed({"decision": "INCONCLUSIVE"}, 6, r) is True
    assert A.extension_needed({"decision": "INCONCLUSIVE"}, 9, r) is False
    assert A.extension_needed({"decision": "ADOPT"}, 6, r) is False
    res = {"sonnet": {"class": {"decision": "ADOPT", "reasons": []}, "n_total": 6}}
    monkeypatch.setattr(h, "compute_results", lambda: res)
    assert h.extend() == 1 and not h.all_runs()
    res["sonnet"]["class"] = {"decision": "INCONCLUSIVE", "reasons": ["x"]}
    assert h.extend() == 0
    assert [x for x in h.all_runs()] == ["b1-r7", "b1-r8", "b1-r9"]
    assert h.extend() == 1                                                       # a second extension needs the owner
    assert A.load_rules()["extension"] == {"base_replicates": 6, "extra_replicates": 3, "max_extensions": 1}


# ------------------------------------------------------------------ C9.3 and outcome helpers
def test_c93_parsing():
    assert c93.parse_ids("**F1, F2**. The reviser reads") == ["F1", "F2"]
    assert c93.parse_ids("none (F1 resolved)") == [] and c93.parse_ids(None) == []
    assert c93.parse_ids("R1-B1, R1-B2") == ["R1-B1", "R1-B2"]
    assert c93.parse_ids("AC-1, FR-2, F3") == ["F3"]
    ids = c93.ids_from(P11 / "runs/a3-r1/ws" / D / "review/round1.md")
    assert c93.parse_ids(ids) == ["F1", "F2"]
    assert c93.blocking_tags(P11 / "runs/a3-r6/aud/ws" / D / "review/audit.md") == [("F-01", "T2")]
    assert c93.cited("see spec:62 and lines 10-12") == [10, 11, 12, 62]


def test_outcome_rows_and_marginal_value():
    hits = {"a": {"D1", "D2"}, "b": {"D2"}, "c": {"D3"}}
    rows = A.outcome_rows(hits, {"a": 3, "b": 1, "c": 1}, {"D1", "D2", "D3", "D4"}, rejected={"a": 1, "b": 0, "c": 0}, tokens={"a": 100, "b": 50, "c": 0})
    assert rows["a"]["confirmed_tp"] == 2 and rows["a"]["false_pos"] == 1 and rows["a"]["unconfirmed"] == 0 and rows["a"]["unique_tp"] == 1
    assert abs(rows["a"]["precision"] - 2 / 3) < 1e-9 and rows["a"]["cost_per_confirmed_tp"] == 50 and rows["a"]["recall_vs_confirmed"] == 0.5
    assert rows["c"]["cost_per_confirmed_tp"] is None and rows["b"]["unique_tp"] == 0
    loo = A.leave_one_out(hits, {"D1", "D2", "D3", "D4"})
    assert loo["a"]["marginal"] == 0.25 and loo["b"]["marginal"] == 0
    assert A.residual_class("T1", {"T1"}) == "found_then_survived" and A.residual_class("other", {"other"}) == "never_found"


def test_rules_file_is_data_with_formula_comments():
    r = json.loads((AB / "rules.json").read_text())
    c = r["cost_limits_d6"]
    assert "formula" in c and c["drop2_r_loop"]["original_L"] == 3.3 and c["cost_hold_r_loop"]["original_L"] == 2.0
    assert "mid_run_cost_checks" in c
    assert r["strata"]["audit_model"] == "sonnet" and r["strata"]["haiku_runs"] == 4


# ------------------------------------------------------------------ outcomes and analyze run end to end on a fake completed run
def complete_fake_run(run, capsys):
    run_to_round1_merged(capsys, run)
    launch_lines(capsys)
    st = h.load(run)
    ids = st["log"]["M1"]["brief_ids"]
    edit_spec(run, "its report path is the WC-4 contract path", "its report path is the command's own report file")
    edit_spec(run, "step 4 uses the command's existing report file, since the contract arrives in P1", "step 4 uses the command's existing report file")
    write_out(h.out_path(run, "V1"), "## Fix map\n\n```fixmap-v1\n" + "".join(json.dumps({"id": i, "action": "applied", "reason": "r"}) + "\n" for i in ids) + "```\n")
    mp = json.loads((h.run_dir(run) / "adj-map.json").read_text())
    write_out(h.out_path(run, "ADJ"), "adj\n\n```adj-v1\n" + "".join(json.dumps({"x": x, "verdict": "confirmed", "reason": "r"}) + "\n" for x in mp) + "```\n")
    launch_lines(capsys)
    write_out(reviewer_out(run, 2, "t1b-1"), baseline_report(2) + fixture_block([json.dumps({"prior": i, "status": "resolved"}) for i in ids]))
    launch_lines(capsys)
    for k in ("AUD", "AUD2"):
        write_out(h.out_path(run, k), (P11 / "runs/a3-r1/aud/ws" / D / "review/audit.md").read_text())
    launch_lines(capsys)
    assert h.load(run)["phase"] == "complete"


def test_outcomes_and_analyze_end_to_end(sandboxed, capsys):
    import report
    complete_fake_run("b1-r1", capsys)
    report.outcomes()
    recs = [json.loads(l) for f in (sandboxed / "tel/records").rglob("*.outcomes.jsonl") for l in f.read_text().splitlines()]
    assert {r["truth_basis"] for r in recs} >= {"adjudicated-v1"} and all(r["stratum"] == "sonnet" for r in recs)
    assert len(recs) >= 8
    report.analyze()
    text = (sandboxed / "RESULTS.md").read_text()
    assert text.startswith("# PN1 RESULTS") and "DECISION:" in text and "R_LOOP" in text and "R_B" in text
    assert "Haiku robustness pending" in text or "INCONCLUSIVE" in text or "DROP" in text
    res = h.compute_results()
    assert res["sonnet"]["n_total"] == 1 and res["final"] != "ADOPT"          # one run is below the five-run minimum
    assert "fewer than 5 completed runs" in " ".join(res["sonnet"]["class"]["reasons"])
