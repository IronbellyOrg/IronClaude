import json
import os
import pathlib
import sys

import pytest

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import headroom as hr  # noqa: E402
import labels_from_audits as la  # noqa: E402
import packets as pk  # noqa: E402

REV = pk.REVIEW_DIR
AUD = pk.AUD_OUT
S0 = pk.FROZEN_SPEC_SHA


def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def report(verdict, ids=None, followups=0):
    brief = f"Blocking finding ids: {ids}." if ids else "None. No blocking finding is open."
    fu = "".join(f"- candidate {i}\n" for i in range(followups))
    return f"# review\n\n## Follow-up candidates (x)\n\n{fu}\n## Reviser brief\n{brief}\n\nverdict: {verdict}\n"


def audit_text(verdict, nblock):
    if verdict == "PASS":
        return "# audit\n\n## Reviser brief\nNone.\n\nverdict: PASS\n"
    ids = ", ".join(f"B{i + 1}" for i in range(nblock))
    body = "".join(f"### B{i + 1} A defect\nSPEC:10 says x.\n\n" for i in range(nblock))
    brief = f"Blocking finding ids: {ids}. Nothing else is in scope." if nblock else "None."
    return f"# audit\n\n{body}## Reviser brief\n{brief}\n\nverdict: FAIL\n"


def make_run(root, name, steps, audits=(), shas=None, extra_audit_root=None):
    """steps: list of (step, verdict|None, spec_sha|None). Writes state.json, round reports and audits."""
    rd = root / name
    log, done = {}, []
    for step, verdict, sha in steps:
        rec = {"output_exists": True}
        if verdict:
            rec["verdict"] = verdict
        if sha:
            rec["spec_after"] = {"sha256": sha}
        log[step] = rec
        done.append(step)
        if step.startswith("R") and verdict:
            write(rd / "ws" / REV / f"round{step[1:]}.md", report(verdict, "B1, B2" if verdict == "FAIL" else None, 2))
    write(rd / "state.json", json.dumps({"run": name, "done": done, "log": log}))
    for sub, (v, n) in zip(("aud", "aud2"), audits):
        write(rd / sub / "ws" / AUD, audit_text(v, n))
    return rd


def src(root, **kw):
    d = {"name": "fx", "runs_root": root, "stratum": "p11", "design_of": lambda r: "fx", "extra_audit_root": None,
         "require_both_audits": False}
    d.update(kw)
    return d


def fixture_tree(tmp_path):
    root = tmp_path / "runs"
    # f1: R1 FAIL, V1, R2 PASS (scoped), audit FAIL x2 -> eligible, needs assurance
    make_run(root, "f1", [("R1", "FAIL", S0), ("V1", None, "aa"), ("R2", "PASS", "aa")], [("FAIL", 2), ("FAIL", 1)])
    # f2: R1 PASS (whole first review) -> unchanged hash, one audit PASS
    make_run(root, "f2", [("R1", "PASS", S0)], [("PASS", 0)])
    # f3: R3 PASS -> cap
    make_run(root, "f3", [("R1", "FAIL", S0), ("V1", None, "b1"), ("R2", "FAIL", "b1"), ("V2", None, "b2"), ("R3", "PASS", "b2")],
             [("FAIL", 1)])
    # f4: R3 FAIL -> escalated, no packet
    make_run(root, "f4", [("R1", "FAIL", S0), ("V1", None, "c1"), ("R2", "FAIL", "c1"), ("V2", None, "c2"), ("R3", "FAIL", "c2")],
             [("FAIL", 1)])
    # f5: R2 PASS, adequate (audit PASS)
    make_run(root, "f5", [("R1", "FAIL", S0), ("V1", None, "d1"), ("R2", "PASS", "d1")], [("PASS", 0)])
    # f6: no audits -> excluded
    make_run(root, "f6", [("R1", "PASS", S0)], [])
    return root


def test_packet_enumeration_on_fixture_runs(tmp_path):
    root = fixture_tree(tmp_path)
    res = pk.enumerate_packets([src(root)])
    by = {p["run"]: p for p in res["packets"]}
    assert sorted(by) == ["f1", "f2", "f3", "f5"]
    assert [e["run"] for e in res["escalated"]] == ["f4"]
    assert [e["run"] for e in res["excluded"]] == ["f6"]
    p = by["f1"]
    assert (p["review_k"], p["slots_remaining"], p["fix_cycles_used"], p["spec_sha_at_pass"]) == (2, 1, 1, "aa")
    assert p["changed_since_last_whole_review"] is True and p["open_blockers"] == 0 and p["followups"] == 2
    assert p["verdict_source"].endswith("round2.md")
    # require_both_audits excludes single-audit runs
    res2 = pk.enumerate_packets([src(root, require_both_audits=True)])
    assert [p["run"] for p in res2["packets"]] == ["f1"]


def test_code_determined_reasons(tmp_path):
    root = fixture_tree(tmp_path)
    by = {p["run"]: p for p in pk.enumerate_packets([src(root)])["packets"]}
    assert hr.code_determined_reason(by["f3"]) == "cap"
    assert hr.code_determined_reason(by["f2"]) == "unchanged_hash"
    assert hr.code_determined_reason(by["f1"]) is None
    # open blocker (a non-PASS state) and mandatory policy; cap takes precedence over the others
    p = dict(by["f1"], open_blockers=2)
    assert hr.code_determined_reason(p) == "open_blocker"
    assert hr.code_determined_reason(dict(by["f1"], mandatory_policy=True)) == "mandatory_policy"
    assert hr.code_determined_reason(dict(p, slots_remaining=0)) == "cap"
    # a PASS report that names resolved ids in prose has no open blocker
    rd = tmp_path / "runs" / "f1" / "ws" / REV
    write(rd / "round2.md", "## Reviser brief\nNo blocking finding is open (B-1 resolved).\n\nverdict: PASS\n")
    again = {p["run"]: p for p in pk.enumerate_packets([src(tmp_path / "runs")])["packets"]}["f1"]
    assert again["open_blockers"] == 0 and again["parsed_ids_in_pass_report"] >= 1


def test_strict_and_sensitivity_labels(tmp_path):
    assert la.label_audits([{"verdict": "FAIL", "blocking": 2}])["label"] == "yes"
    assert la.label_audits([{"verdict": "PASS", "blocking": 0}])["label"] == "no"
    mixed = la.label_audits([{"verdict": "PASS", "blocking": 0}, {"verdict": "FAIL", "blocking": 1}])
    assert (mixed["label"], mixed["sens_label"], mixed["single_audit"]) == ("yes", "no", False)
    one = la.label_audits([{"verdict": "FAIL", "blocking": 1}])
    assert one["single_audit"] is True and one["sens_label"] == "yes"
    assert la.label_audits([{"verdict": "NONE", "blocking": 0}])["label"] == "unlabeled"
    unparsed = la.label_audits([{"verdict": "FAIL", "blocking": 0}])
    assert unparsed["label"] == "no" and unparsed["sens_label"] == "yes" and unparsed["fail_unparsed"] == 1
    # from real fixture audit files
    root = fixture_tree(tmp_path)
    by = {p["run"]: p for p in pk.enumerate_packets([src(root)])["packets"]}
    assert la.label_packet(by["f1"])["label"] == "yes"
    assert la.label_packet(by["f5"])["label"] == "no"


def test_headroom_definition(tmp_path):
    root = fixture_tree(tmp_path)
    rows = {p["run"]: hr.classify(p, la.label_packet(p)) for p in pk.enumerate_packets([src(root)])["packets"]}
    assert rows["f1"]["eligible"] and rows["f1"]["min_route"] == "assurance" and rows["f1"]["static_route"] == "assurance"
    assert not rows["f1"]["headroom"]
    assert rows["f5"]["eligible"] and rows["f5"]["min_route"] == "deliver" and rows["f5"]["headroom"]
    assert rows["f3"]["eligible"] is False and rows["f3"]["static_route"] == "deliver" and not rows["f3"]["headroom"]
    assert rows["f2"]["eligible"] is False and not rows["f2"]["headroom"]
    s = hr.summarize(list(rows.values()))
    assert (s["packets"], s["eligible"], s["headroom"]) == (4, 2, 1)
    assert s["code_determined_by_reason"]["cap"] == 1 and s["code_determined_by_reason"]["unchanged_hash"] == 1
    assert s["needs_assurance_rate"] == 0.5


def test_rule_no_go_and_headroom():
    dec = hr.load_decision()
    assert dec["zero_call"]["min_headroom_packets"] == 2 and dec["zero_call"]["min_headroom_fraction"] == 0.10
    v, r = hr.zero_call_rule({"headroom": 1, "eligible": 11}, dec)
    assert v == "NO-GO-OFFLINE" and r.startswith("headroom 1/11 (9.1%)") and "< 2 packets" in r
    v, r = hr.zero_call_rule({"headroom": 2, "eligible": 30}, dec)       # fraction 0.067 < 0.10
    assert v == "NO-GO-OFFLINE" and "< 0.10" in r
    v, _ = hr.zero_call_rule({"headroom": 2, "eligible": 20}, dec)       # exactly 0.10 and >= 2 -> headroom
    assert v == "HEADROOM"
    assert hr.zero_call_rule({"headroom": 0, "eligible": 0}, dec)[0] == "NO-GO-OFFLINE"
    assert hr.zero_call_rule({"headroom": 5, "eligible": 12}, dec)[0] == "HEADROOM"


def test_results_json_schema(tmp_path):
    dec_path = HERE / "decision.toml"
    sd = {"packets": 16, "eligible": 11, "code_determined_by_reason": {}, "needs_assurance_rate": 0.9, "headroom": 1,
          "sensitivity_headroom": 2}
    for verdict, rule, gate_v, live_reason in (
            ("NO-GO-OFFLINE", "headroom 1/11 (9.1%) < 2 packets", "NO-GO-OFFLINE", "zero-call headroom absent"),
            ("HEADROOM", "headroom 3/11 (27.3%) >= 0.10", "PENDING", "owner cap-neutral scope amendment missing")):
        d = hr.build_results(sd, sd, verdict, rule, dec_path, "2026-11-10T00:00:00+00:00")
        assert hr.validate_results(d) == []
        assert d["rows"][0]["arm"] == "E5-zero-call" and d["rows"][0]["verdict"] == gate_v
        live = {r["arm"]: r for r in d["rows"][1:]}
        assert set(live) == {"k5j", "k5r", "k5s"}
        assert all(r["verdict"] == "BLOCKED" and r["rule"] == live_reason for r in live.values())
        assert d["rows"][0]["stratum"] == "offline" and d["rows"][0]["role"] == "offline-gate"
        out = tmp_path / f"{verdict}.json"
        hr.write_results(out, d)
        assert json.loads(out.read_text())["schema"] == "p15-results/1"
    # a BLOCKED-only record is also valid
    d["rows"] = d["rows"][1:]
    assert hr.validate_results(d) == []
    bad = dict(d, schema="x")
    assert hr.validate_results(bad)
    with pytest.raises(ValueError):
        hr.write_results(tmp_path / "bad.json", bad)


def test_real_files_smoke():
    if not (pk.SP / "p11/runs/a3-r1/state.json").exists():
        pytest.skip("real p11 files not available")
    res = pk.enumerate_packets(pk.default_sources())
    rows = [hr.classify(p, la.label_packet(p)) for p in res["packets"]]
    dec = hr.load_decision()
    dr = [r for r in rows if r["stratum"] in dec["offline"]["decisive_strata"]]
    sd = hr.summarize(dr)
    print("REAL packets", len(rows), "decisive", sd, "escalated", len(res["escalated"]), "excluded", len(res["excluded"]))
    assert sd["packets"] == 16 and sd["eligible"] >= sd["headroom"] >= 0
    assert sd["eligible"] + sum(sd["code_determined_by_reason"].values()) == sd["packets"]
    assert hr.zero_call_rule(sd, dec)[0] in ("NO-GO-OFFLINE", "HEADROOM")
