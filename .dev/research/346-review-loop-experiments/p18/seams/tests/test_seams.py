"""Mock-transport tests of the ab6 seams (A1, A2, A3), the replay driver and the gate scorer.  No test calls Jev or needs the key."""
import json
import os
import pathlib
import subprocess
import sys

import pytest

import seamlib as S
import a1_support as A1
import a2_observability as A2
import a3_novelty as A3
import replay as R
import score_gates as G

HERE = pathlib.Path(__file__).resolve().parent.parent
ORIG = S.SP / "p17" / "in" / "spec-original.md"


@pytest.fixture(scope="module")
def orig_text():
    return ORIG.read_text(encoding="utf-8")


@pytest.fixture()
def runner_factory(tmp_path):
    made = []

    def make(seam="a1", mode="ok", **kw):
        r = S.Runner(seam=seam, mode="mock", out_dir=tmp_path / f"{seam}-{mode}-{len(made)}", mock_mode=mode, **kw)
        made.append(r)
        return r
    with S.mock_env():
        yield make


# ----------------------------------------------------------------------------- answer validation
def _item(orig_text):
    _, _, items = A1.build_items(orig_text, "orig")
    return items[0]


def test_valid_answer_is_usable(runner_factory, orig_text):
    r = runner_factory("a1", "ok", chooser=lambda req: {n: "partial" for n in req["questions"]})
    out = r.ask(_item(orig_text))
    assert out["status"] == "ok" and out["usable"] and out["choice"] == "partial" and out["fallback"] is None


def test_option_outside_the_question_is_invalid_not_usable(runner_factory, orig_text):
    r = runner_factory("a1", "ok", chooser=lambda req: {n: "supported" for n in req["questions"]})
    # a body whose choice is not an option of the question fails the strict validator
    def bad(req):
        body = S._choice_body(req, {n: "supported" for n in req["questions"]})
        for a in body["answers"].values():
            a["choice"] = "maybe"
        return S.MockStep(200, body)
    r.transport.script = bad
    out = r.ask(_item(orig_text))
    assert out["status"] == "invalid" and not out["usable"] and out["fallback"].startswith("invalid:")


def test_insufficient_is_a_fallback_with_no_hint(runner_factory, orig_text):
    r = runner_factory("a1", "insufficient")
    out = r.ask(_item(orig_text))
    assert out["status"] == "ok" and not out["usable"] and out["fallback"] == "insufficient"


@pytest.mark.parametrize("mode,reason", [("malformed", "invalid:not_json"), ("timeout", "unavailable:timeout"), ("http500", "unavailable:http_500"),
                                         ("wrongmodel", "invalid:model_mismatch")])
def test_every_error_is_a_fallback(runner_factory, orig_text, mode, reason):
    r = runner_factory("a1", mode)
    out = r.ask(_item(orig_text))
    assert not out["usable"] and out["fallback"] == reason
    if mode in ("timeout", "http500"):
        assert len(r.transport.calls) == 2            # exactly one retry (J1.5), no more


@pytest.mark.parametrize("mode", ["insufficient", "malformed", "timeout", "http500", "wrongmodel"])
def test_no_hint_on_any_error_in_any_seam(runner_factory, orig_text, mode, tmp_path):
    r1 = runner_factory("a1", mode)
    res1 = A1.run_spec(orig_text, "orig", r1)
    assert res1["hints"] == []
    r2 = runner_factory("a2", mode)
    res2 = A2.run_spec(orig_text, "orig", tmp_path / "scr", r2)
    assert not any("jev:" in ln for ln in res2["lines"])           # code-stage lines stay (they are not Jev answers)
    r3 = runner_factory("a3", mode)
    d = A3.load_pn1_cases()
    items, outs, by = A3.run_cases(d["cases"], r3)
    lines = A3.make_lines([c["analysis"] for c in d["cases"]], outs)
    assert all(ln["source"] == "code" for ln in lines)


# ----------------------------------------------------------------------------- caps and hint form
def test_a1_hint_cap_and_flag_only_form(runner_factory, orig_text):
    r = runner_factory("a1", "ok", chooser=lambda req: {n: "unsupported" for n in req["questions"]})
    res = A1.run_spec(orig_text, "orig", r)
    assert len(res["items"]) <= 60 and len(res["hints"]) == 12
    for h in res["hints"]:
        t = h["text"]
        assert t.startswith("UNVERIFIED A1-") and "not a finding" in t
        assert not any(w in t.lower() for w in ("blocking", "critical", "major", "severity", "must fix"))


def test_a1_supported_pairs_are_never_shown(runner_factory, orig_text):
    r = runner_factory("a1", "ok", chooser=lambda req: {n: "supported" for n in req["questions"]})
    assert A1.run_spec(orig_text, "orig", r)["hints"] == []


def test_a2_line_cap(runner_factory, orig_text, tmp_path):
    r = runner_factory("a2", "ok", chooser=lambda req: {n: "cannot_pass" for n in req["questions"]})
    res = A2.run_spec(orig_text, "orig", tmp_path / "scr", r)
    assert len(res["lines"]) == 8
    assert all("not a finding" in ln and ln.startswith("UNVERIFIED A2-") for ln in res["lines"])


def test_v2_merge_cap_and_order():
    a3 = [{"lid": f"L{i}", "refs": [f"WC-{i}"], "text": f"UNVERIFIED A3 [L{i}] x.", "source": "jev", "label": "same_restated"} for i in range(1, 8)]
    a1 = [{"pair": f"WC-{i}|AC-1.1", "obligation": f"WC-{i}", "criterion": "AC-1.1", "text": f"UNVERIFIED A1-{i} y."} for i in range(1, 20)]
    out = A3.merge_v2_hints(a3, a1, cap=15)
    assert len(out) == 15 and out[0].startswith("UNVERIFIED A3 [L1]") and "also flagged" in out[0]
    assert sum(1 for x in out if x.startswith("UNVERIFIED A1-")) <= 15 - 7        # A1 hints on an A3 blocker's refs are merged, not repeated


# ----------------------------------------------------------------------------- prefilter determinism and accepted findings
def test_prefilter_is_deterministic_and_capped(orig_text):
    a = A1.build_pairs(A1.extract(orig_text))
    b = A1.build_pairs(A1.extract(orig_text))
    assert [p["id"] for p in a["pairs"]] == [p["id"] for p in b["pairs"]]
    assert len(a["pairs"]) == 60 and a["raw"] == 2590 and a["eligible"] == 562
    c = A1.build_pairs(A1.extract(orig_text), cap=10)
    assert len(c["pairs"]) == 10


def test_accepted_findings_drop_covered_pairs_before_the_cap(orig_text):
    base = A1.build_pairs(A1.extract(orig_text))
    victim = base["pairs"][0]
    acc = [{"ids": [victim["o"]["id"], victim["c"]["id"]], "text": "", "lines": []}]
    got = A1.build_pairs(A1.extract(orig_text), acc)
    assert victim["id"] not in {p["id"] for p in got["pairs"]}
    assert got["dropped_covered"] >= 1 and len(got["pairs"]) == 60          # the freed slot is refilled: the drop happens before the cap


def test_wc_quota_keeps_wc_pairs(orig_text):
    got = A1.build_pairs(A1.extract(orig_text))
    assert sum(1 for p in got["pairs"] if p["o"]["kind"] == "wc") >= 8


# ----------------------------------------------------------------------------- packet limits, privacy
def test_packets_are_within_the_byte_limit(orig_text, tmp_path):
    dec = S.decision()
    lim = dec["caps"]["packet_bytes_max"]
    _, _, i1 = A1.build_items(orig_text, "orig")
    _, _, i2, _ = A2.build_items(orig_text, tmp_path / "scr", "orig")
    for it in i1 + i2:
        assert S.packet_bytes(it) <= lim
    assert max(S.packet_bytes(it) for it in i1) < 6000


def test_oversize_packet_is_refused_locally_without_a_call(runner_factory, orig_text):
    r = runner_factory("a1", "ok")
    it = _item(orig_text)
    it["state"]["obligation"]["text"] = "x " * 120_000
    ok, big = R.enforce_packet_limit([it], S.decision())
    assert ok == [] and big == [it]
    out = r.ask(it)                                              # the adapter itself refuses an over-limit request: no call
    assert out["fallback"] == "refused:oversize" and r.transport.calls == []


def test_privacy_guard_refuses_unscrubbed_owner_names(runner_factory):
    q = A1.support_question()
    bad = S.question_item("t:1", "a1-q1", {"obligation": {"text": "repo IronbellyOrg/IronClaude"}}, "support", q)
    bad["state"] = {"obligation": {"text": "repo IronbellyOrg/IronClaude"}}      # bypass the scrub on purpose
    r = runner_factory("a1", "ok")
    out = r.ask(bad)
    assert out["fallback"] == "refused:privacy" and r.transport.calls == []


def test_scrub_removes_everything_the_guard_refuses():
    t = "gh api repos/IronbellyOrg/IronClaude/pulls at /home/coder/x see https://github.com/IronbellyOrg/IronClaude and a@b.example"
    s = S.scrub(t)
    for bad in ("IronbellyOrg", "/home/", "github.com", "@b.example"):
        assert bad not in s


def test_orig_spec_has_no_privacy_refusal_in_the_preflight(orig_text, runner_factory, tmp_path):
    _, _, i1 = A1.build_items(orig_text, "orig")
    _, _, i2, _ = A2.build_items(orig_text, tmp_path / "scr", "orig")
    r = runner_factory("a1", "ok")
    pre = r.preflight(i1 + i2)
    assert pre["privacy_refused"] == 0 and pre["oversize_refused"] == 0 and pre["requests"] == len(i1) + len(i2)
    assert r.transport.calls == []                                # a dry run makes no call
    assert pre["reserve_tokens"] == int(pre["est_tokens"] * 1.2) + 1


# ----------------------------------------------------------------------------- budget refusal (J4)
def test_reservation_that_does_not_fit_is_refused_before_any_call(runner_factory, orig_text):
    r = runner_factory("a1", "ok", ceiling_tokens=500)
    _, _, items = A1.build_items(orig_text, "orig")
    pre = r.preflight(items)
    with pytest.raises(S.BudgetExhausted):
        r.reserve(pre["reserve_tokens"])
    assert r.transport.calls == []


def test_replay_main_blocks_on_budget_and_writes_the_marker(monkeypatch, tmp_path):
    monkeypatch.setattr(R, "OUT", tmp_path / "out")
    rc = R.main(["--seam", "a1", "--specs", "orig", "--mock", "--ceiling-tokens", "1000"])
    assert rc == R.EXIT_BUDGET
    assert (tmp_path / "out" / "a1" / "BLOCKED-BUDGET-a1.json").exists()
    assert not (tmp_path / "out" / "a1" / "orig.json").exists()


def test_a_draw_that_fails_after_reservation_is_a_fallback_not_a_stop(runner_factory, orig_text):
    r = runner_factory("a1", "ok", ceiling_tokens=10_000)
    r.budget.reserve_phase(r.phase, 10_000)                       # the whole ceiling is reserved; the next draw has nothing left
    for it in A1.build_items(orig_text, "orig")[2][:30]:
        out = r.ask(it)
    assert out["fallback"] == "refused:budget_exhausted" and not out["usable"]


def test_live_without_key_exits_3_before_any_network():
    env = {k: v for k, v in os.environ.items() if k != "JEV_API_KEY"}
    p = subprocess.run([sys.executable, str(HERE / "replay.py"), "--seam", "a1", "--specs", "orig", "--live"], env=env, capture_output=True, text=True, cwd=HERE, timeout=120)
    assert p.returncode == 3 and "not set" in p.stdout


def test_dry_run_is_the_default_and_writes_no_answers(monkeypatch, tmp_path):
    monkeypatch.setattr(R, "OUT", tmp_path / "out")
    assert R.main(["--seam", "a2", "--specs", "orig"]) == 0
    assert (tmp_path / "out" / "a2" / "orig.dry.json").exists() and not (tmp_path / "out" / "a2" / "orig.json").exists()


# ----------------------------------------------------------------------------- golden test on the original spec
def test_golden_a2_original(orig_text, tmp_path):
    rows, analysis, items, lint_all = A2.build_items(orig_text, tmp_path / "scr", "orig")
    assert len(rows) == 32 and [r["id"] for r in rows if r["kind"] == "step"] == [f"7.2#{i}" for i in range(1, 8)]
    flagged = {a["id"]: sorted({f["check"] for f in a["code_flags"]}) for a in analysis if a["code_flags"]}
    assert set(flagged) == {"AC-C1", "AC-C4", "AC-C5", "AC-0.3", "AC-0.4"}
    assert "D20" in flagged["AC-C5"] and "D20" in flagged["AC-0.3"] and "D21" in flagged["AC-C1"] and "D21" in flagged["AC-C4"]
    assert "PHASE" in flagged["AC-0.4"] and "EXEC" in flagged["AC-0.4"]                 # lint PHASE (D11) + the YAML-on-markdown execution (D12)
    assert sorted(f["lines"][0] for f in lint_all) == [83, 92, 194]                    # widened lint: PATH, PATH, PHASE
    assert len(items) == 27 and all(i["row_id"] not in flagged for i in items)         # only rows that passed every code check reach Jev
    ac_c4 = next(a for a in analysis if a["id"] == "AC-C4")
    assert any("probe" in e["cmd"] and e.get("flag") for e in ac_c4["exec"])           # the raw table-source copy behaves differently from the unescaped command
    ac_03 = next(a for a in analysis if a["id"] == "AC-0.3")
    assert any(e.get("verdict") == "probe not caught" for e in ac_03["exec"])
    y = next(a for a in analysis if a["id"] == "7.2#4")
    assert any("markdown report: exit 1" in e["verdict"] for e in y["exec"])
    lines = A2.make_lines(analysis, [])
    assert len(lines) == 5 and lines[0].startswith("UNVERIFIED A2-1")                  # five code-flagged rows, no Jev answers


def test_golden_a1_original(orig_text):
    ex = A1.extract(orig_text)
    kinds = {}
    for o in ex["obligations"]:
        kinds[o["kind"]] = kinds.get(o["kind"], 0) + 1
    assert kinds == {"wc": 12, "cmd": 37, "sa": 6, "dec": 10, "od": 5}
    ck = {}
    for c in ex["criteria"]:
        ck[c["kind"]] = ck.get(c["kind"], 0) + 1
    assert ck == {"ac": 25, "step": 7, "gate": 5}
    bp = A1.build_pairs(ex)
    assert bp["raw"] == 70 * 37 and len(bp["pairs"]) == 60
    ids = {p["id"] for p in bp["pairs"]}
    assert "WC-4|AC-0.4" in ids and "cmd:post-release|AC-4.2" in ids
    kw = A1.keyword_flags(bp)
    assert kw and all(set(k["why"]) <= {"phase_mismatch", "deferral_lexicon"} for k in kw)


def test_golden_a3_pn1_cases():
    d = A3.load_pn1_cases()
    rep = d["report"]
    assert rep["reconstructed"] == 10 and rep["outcomes"] == {"resolved": 2, "failed": 8}
    assert rep["runs_with_cases"] == ["b1-r1", "b1-r2", "b1-r4", "b1-r5", "b1-r6"] and rep["located"] == 10 and rep["touched_v1"] == 10
    assert sum(1 for c in d["cases"] if c["controls"]["v2_named_not_touched"]) == 5          # the advocate's five "named_not_touched" survivors
    assert {c["case_id"] for c in d["cases"] if c["outcome"] == "resolved"} == {"b1-r4-L2", "b1-r6-L2"}


# ----------------------------------------------------------------------------- A3 logic on a synthetic diff
OLD = "\n".join(["# t", "rule one says a", "rule two says b", "rule three says c", "end"])
NEW = "\n".join(["# t", "rule one says A changed", "rule two says b", "rule three says c", "end"])
R2 = """## Blocking findings

### L1

#### L1.t1-1 (F1)

- claim: rule one is still wrong.
- anchor: "rule one says A changed"

### L2

#### L2.t1-1 (F2)

- claim: rule three is wrong.
- anchor: "rule three says c"

## Other findings
"""


def test_a3_named_not_touched_and_touched_split():
    bl = [{"lid": "L1", "anchors": ["rule one says a"], "claims": ["x"], "refs": []}, {"lid": "L2", "anchors": ["rule three says c"], "claims": ["y"], "refs": []}]
    an = A3.analyze(OLD, NEW, R2, bl)
    by = {a["lid"]: a for a in an}
    assert by["L1"]["touched_v1"] and not by["L1"]["named_not_touched"] and by["L1"]["to_jev"]
    assert not by["L2"]["touched_v1"] and by["L2"]["named_not_touched"] and not by["L2"]["to_jev"]
    items = A3.build_items(an, OLD, NEW)
    assert [i["lid"] for i in items] == ["L1"]
    lines = A3.make_lines(an, [])
    assert [(x["lid"], x["source"]) for x in lines] == [("L2", "code")]                       # no Jev answer: only the code fact remains


def test_a3_jev_line_only_for_usable_answers(runner_factory):
    bl = [{"lid": "L1", "anchors": ["rule one says a"], "claims": ["x"], "refs": []}]
    an = A3.analyze(OLD, NEW, R2, bl)
    items = A3.build_items(an, OLD, NEW)
    r = runner_factory("a3", "ok", chooser=lambda req: {n: "same_restated" for n in req["questions"]})
    outs = [r.ask(i) for i in items]
    ln = A3.make_lines(an, outs)
    assert len(ln) == 1 and ln[0]["label"] == "same_restated" and "governing rule" in ln[0]["text"]
    r2 = runner_factory("a3", "insufficient")
    assert A3.make_lines(an, [r2.ask(i) for i in items]) == []


# ----------------------------------------------------------------------------- controls
def test_control_packets_are_the_identical_packets(orig_text, tmp_path):
    _, _, items = A1.build_items(orig_text, "orig")
    ctl = A1.control_items(items)
    assert [c["id"] for c in ctl] == [i["id"] for i in items] and ctl[0]["state"] == items[0]["state"]
    assert set(ctl[0]["options"]) == set(A1.SUPPORT_OPTIONS)
    ans = {items[0]["id"]: "partial", items[1]["id"]: "insufficient", items[2]["id"]: "nonsense"}
    outs = A1.apply_answers(items[:3], ans)
    assert [o["usable"] for o in outs] == [True, False, False]
    _, _, i2, _ = A2.build_items(orig_text, tmp_path / "scr", "orig")
    c2 = A2.control_items(i2)
    assert c2[0]["state"] == i2[0]["state"] and set(c2[0]["options"]) == set(A2.OBS_OPTIONS)


def test_mock_mode_never_leaves_a_key_behind_or_logs_authorization(tmp_path, orig_text):
    before = os.environ.get("JEV_API_KEY")
    with S.mock_env():
        assert os.environ["JEV_API_KEY"] == S.MOCK_KEY
        r = S.Runner(seam="a1", mode="mock", out_dir=tmp_path / "m", mock_mode="ok")
        r.ask(A1.build_items(orig_text, "orig")[2][0])
        assert all("authorization" not in {k.lower() for k in h} for _, h, _ in r.transport.calls)
    assert os.environ.get("JEV_API_KEY") == before
    j = (tmp_path / "m" / "mock-journal.jsonl").read_text()
    assert "Authorization" not in j and "Bearer" not in j


# ----------------------------------------------------------------------------- replay + gates end to end on mock output
def test_replay_mock_then_gates(monkeypatch, tmp_path):
    monkeypatch.setattr(R, "OUT", tmp_path / "out")
    monkeypatch.setattr(G, "OUT", tmp_path / "out")
    assert R.main(["--seam", "all", "--mock", "--specs", "orig,s15,s33"]) == 0
    rec = json.loads((tmp_path / "out" / "a1" / "s15.json").read_text())
    assert rec["schema"] == "ab6-replay/1" and rec["mode"] == "mock" and rec["counts"]["calls"] == 60 and len(rec["hints"]) <= 12
    for k in ("packets", "answers", "hints", "fallbacks", "counts", "meta"):
        assert k in rec
    ctx = G.Ctx({"orig", "s15", "s33"})
    dec = S.decision()
    g1 = G.a1_gates(ctx, dec)
    assert g1["mock_warning"] and set(g1["specs"]) == {"orig", "s15", "s33"} and "recall_pair_level_ge_70" in g1["verdict"]
    g2 = G.a2_gates(ctx, dec)
    assert g2["specs"]["s15"]["rows"] >= 30 and "tail_catch_ge_3" in g2["verdict"]
    ctx3 = G.Ctx({"s33"})
    g3 = G.a3_gates(ctx3, dec)
    assert g3["report"]["reconstructed"] == 10 and "keep_a3" in g3["verdict"]


def test_triage_counts_the_117_residual_t1_cells():
    t = G.triage(G.Ctx())
    assert t["n_cells"] == 117 and sum(t["total"].values()) == 117
    assert set(t["total"]) <= {"a", "b", "c"}


def test_fisher_exact():
    assert G.fisher_two_sided(2, 0, 0, 2) == pytest.approx(0.3333, abs=1e-3)
    assert G.fisher_two_sided(1, 1, 1, 1) == 1.0


# ----------------------------------------------------------------------------- the --live branch rehearsed with a patched network layer (no network, fake key)
def test_live_branch_rehearsal_reserve_journal_cache_and_manifest(monkeypatch, tmp_path):
    import json as _json
    from jevlib import transport as T
    calls = []

    def fake_post(self, url, headers, body, timeout):
        req = _json.loads(body.decode("utf-8"))
        calls.append(headers.get("Authorization", "")[:12])
        step = S.mock_script("ok")(req)
        return step.status, {}, _json.dumps(step.body).encode("utf-8")
    monkeypatch.setattr(T.UrllibTransport, "post", fake_post)
    monkeypatch.setenv("JEV_API_KEY", "TEST-NOT-A-REAL-KEY-0000")
    monkeypatch.setattr(S, "SEAMS", tmp_path / "seams")
    (tmp_path / "seams").mkdir()
    monkeypatch.setattr(R, "OUT", tmp_path / "out")
    assert R.main(["--seam", "a1", "--specs", "orig", "--live"]) == 0
    assert len(calls) == 60 and all(c.startswith("Bearer ") for c in calls)
    led = _json.loads((tmp_path / "seams" / "budget" / "ab6.json").read_text())
    assert led["spent_tokens"] > 0 and led["reserved"] == {}                # the reservation was released after the phase
    j = (tmp_path / "seams" / "journal" / "jev-a1.jsonl").read_text()
    assert "TEST-NOT-A-REAL-KEY-0000" not in j and "Authorization" not in j
    assert (tmp_path / "seams" / "manifest-a1.json").exists()
    rec = _json.loads((tmp_path / "out" / "a1" / "orig.json").read_text())
    assert rec["mode"] == "live" and rec["counts"]["calls"] == 60
    n = len(calls)
    assert R.main(["--seam", "a1", "--specs", "orig", "--live"]) == 0         # second run: every answer comes from the response cache
    assert len(calls) == n
