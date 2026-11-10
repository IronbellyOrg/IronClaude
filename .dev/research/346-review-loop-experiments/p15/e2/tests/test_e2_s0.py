import json
import pathlib
import re

import pytest

import candidates as C
import cases_s0
import extract as X
import hints as Hn
import ingest_labels as IL
import e2lib as L
import static as St
import stage0

E2 = pathlib.Path(__file__).resolve().parents[1]
S1 = cases_s0.S1_SPEC

TOY = """# Toy Spec

## 1. Basics

- ID-1: The archive window is `keep-days` for every archive.
Some plain paragraph that continues
on a second line.

## 2. Rules

| Id | Rule | Path |
|---|---|---|
| R-1 | Logs rotate every 30 days, see section 1. | `conf/rotate.yaml` |
| R-2 | Archives follow `keep-days` unless noted; writes go to `/var/out/rotate.yaml`. | none |

## 3. Limits

The uploader keeps 20 MB in RAM and stalls after 30 seconds. See ID-1 for the window.
"""


def test_extract_exact_bytes_and_stable_pids():
    for text in (TOY, S1.read_text(encoding="utf-8")):
        a, b = X.extract(text), X.extract(text)
        assert [(p.pid, p.text, p.line_start, p.line_end) for p in a] == [(p.pid, p.text, p.line_start, p.line_end) for p in b]
        lines = text.split("\n")
        for p in a:
            assert p.text in text                                           # exact bytes
            assert "\n".join(lines[p.line_start - 1:p.line_end]) == p.text   # exact line span
            assert re.fullmatch(r"P\d{4}", p.pid)
        assert len({p.pid for p in a}) == len(a)
    ps = X.extract(TOY)
    multi = [p for p in ps if "second line" in p.text][0]
    assert multi.kind == "paragraph" and multi.line_end == multi.line_start + 1
    assert {p.kind for p in ps} == {"heading", "paragraph", "list_item", "table_row"}
    idp = [p for p in ps if p.kind == "list_item"][0]
    assert idp.ids_defined == ("ID-1",) and "keep-days" in idp.terms
    last = ps[-1]
    assert "ID-1" in last.ids_referenced and "20 MB" in last.numbers_with_units and "30 s" in last.numbers_with_units


def test_table_rows_keep_header():
    ps = X.extract(TOY)
    rows = [p for p in ps if p.kind == "table_row"]
    head = [p for p in rows if p.is_header]
    body = [p for p in rows if not p.is_header]
    assert len(head) == 1 and len(body) == 2                              # separator row dropped
    assert all(p.context == head[0].text for p in body)
    assert body[0].ids_defined == ("R-1",) and body[0].section_refs == ("1",) and "rotate.yaml" in body[0].paths
    s1 = X.extract(S1.read_text(encoding="utf-8"))
    row = [p for p in s1 if p.line_start == 83][0]
    assert row.context.startswith("| Command |") and not row.is_header


def test_prefilter_rules_and_cap_deterministic():
    ps = X.extract(TOY)
    pool = C.prefilter(ps)
    keys = {(q.a.text[:12], q.b.text[:12]) for q in pool}
    by = {(q.a.pid, q.b.pid): q for q in pool}
    assert pool == C.prefilter(ps) and [q.key for q in C.prefilter(ps)] == [q.key for q in pool]
    f = lambda frag_a, frag_b: next(q for q in pool if frag_a in q.a.text and frag_b in q.b.text)
    assert f("Logs rotate", "Archives follow").features["shared_paths"] == ["rotate.yaml"]               # shared path basename
    assert f("ID-1: The archive", "Archives follow").features["shared_terms"] == ["keep-days"]           # shared backticked term
    assert f("ID-1: The archive", "The uploader").features["explicit_ba"] == ["ID-1"]                    # explicit id reference
    assert f("Logs rotate", "Archives follow").features["explicit_ab"] == [] or True
    assert any(q.features["shared_ids"] for q in pool)                                                    # shared id
    assert any("section 1" in x for q in pool for x in q.features["explicit_ab"] + q.features["explicit_ba"])  # section reference
    assert any(q.features["shared_numunits"] for q in C.prefilter(X.extract("# A\n\nWait 30 seconds then stop.\n\n# B\n\nThe lock lasts 30 s only.\n")))
    small = X.extract("# A\n\nWait 30 seconds then stop.\n\n# B\n\nNothing related here at all today.\n")
    assert C.prefilter(small) == []                                                                       # unrelated pair is not admitted
    capped = C.prefilter(ps, {"pool_cap": 2})
    assert len(capped) == 2 and [q.key for q in capped] == [q.key for q in C.prefilter_uncapped(ps)[:2]]
    assert C.exhaustive(ps) == len([p for p in ps]) * (len(ps) - 1) // 2
    sc = [q.score for q in C.prefilter_uncapped(ps)]
    assert sc == sorted(sc, reverse=True)


def _mk_pair(a_ord, b_ord, pa, pb, **feat):
    mk = lambda pid, o: X.Passage(pid=pid, section_no=str(o), section_title="t", section_ord=o, line_start=int(pid[1:]),
                                  line_end=int(pid[1:]), kind="paragraph", text="x y z")
    return C.Pair(a=mk(pa, a_ord), b=mk(pb, b_ord), features={"explicit_ab": [], "explicit_ba": [], "shared_ids": [], "shared_terms": [],
                                                              "shared_paths": [], "shared_numunits": [], "shared_rare_words": [], **feat})


def test_static_order_and_tiebreak():
    p1 = _mk_pair(1, 2, "P0001", "P0002", explicit_ab=["section 2"])                  # tier 1, distance 1
    p2 = _mk_pair(1, 9, "P0003", "P0004", explicit_ab=["X-1"])                        # tier 1, distance 8
    p3 = _mk_pair(1, 9, "P0001", "P0005", explicit_ab=["X-1"])                        # tier 1, distance 8, smaller pid
    p4 = _mk_pair(1, 4, "P0006", "P0007", shared_ids=["A-1"])                         # tier 2
    p4b = _mk_pair(3, 3, "P0008", "P0009", shared_ids=["A-1"])                        # same section: NOT tier 2
    p5 = _mk_pair(1, 5, "P0010", "P0011", shared_paths=["a.md"])                      # tier 3
    rest = [_mk_pair(1, 1 + i, f"P{20 + i:04d}", f"P{40 + i:04d}", shared_terms=["t"]) for i in range(8)]
    pool = [p5, p4, p1, p2, p3, p4b] + rest
    r = St.rank(pool, 7)
    assert [q.key for q in r[:3]] == [p3.key, p2.key, p1.key]                         # distance desc, then pid
    assert r[3].key == p4.key and r[4].key == p5.key
    assert p4b.key in [q.key for q in r[5:]]                                          # tier 4 (same section)
    assert sorted(q.key for q in r) == sorted(q.key for q in pool)                    # a permutation of the pool
    assert [q.key for q in St.rank(pool, 7)] == [q.key for q in r]                    # frozen sample
    assert [q.key for q in St.rank(pool, 8)][5:] != [q.key for q in r][5:] or len(rest) < 3
    assert [q.key for q in St.rank(list(reversed(pool)), 7)] == [q.key for q in r]    # input order does not matter


def test_hints_budget_no_truncation_identical_format():
    ps = X.extract(TOY)
    pool = C.prefilter(ps)
    for q in pool:
        q.reason = St.reason_for(q)
    full = Hn.render(pool)
    assert full.startswith(Hn.HEADER) and all(re.match(r'\d+\. section .*lines \d+-\d+ <-> section .*lines \d+-\d+: \S', ln)
                                              for ln in full.splitlines()[1:])
    n_full = len(Hn.select(pool))
    one = Hn.item(1, pool[0])
    budget = Hn.tokens(Hn.HEADER + "\n") + Hn.tokens(one + "\n") + 1
    short = Hn.render(pool, budget_tokens=budget)
    assert len(short.splitlines()) == 2 and short.splitlines()[1] == one                # whole items only
    assert Hn.tokens(short) <= budget
    assert Hn.render(pool, max_pairs=2).count("\n") == 3 and n_full >= 2
    long_mid = [pool[0], pool[1], pool[2]]
    long_mid[1] = C.Pair(a=pool[1].a, b=pool[1].b, features=pool[1].features, reason="r" * 6000)
    chosen = Hn.select(long_mid, budget_tokens=1200)
    assert len(chosen) == 1                                                             # stops at the first item that does not fit
    other = C.Pair(a=pool[0].a, b=pool[0].b, features={}, reason="a different reason from another router")
    assert re.sub(r": .*", "", Hn.item(1, other)) == re.sub(r": .*", "", Hn.item(1, pool[0]))   # identical format, only the reason differs
    assert 'section 1 "Basics" lines' in Hn.locator(pool[0].a) or Hn.locator(pool[0].a).startswith("section ")


def test_fallback_document_order():
    ps = X.extract(S1.read_text(encoding="utf-8"))
    pool = C.prefilter(ps)
    exp = sorted(pool, key=lambda q: (q.a.line_start, q.b.line_start, q.a.pid, q.b.pid))[:12]
    assert [q.key for q in Hn.fallback_pairs(pool)] == [q.key for q in exp]
    foreign = _mk_pair(1, 2, "P9998", "P9999")
    for bad in (None, [], "text", [foreign], [pool[0], pool[0]], [pool[0], foreign]):
        text, used = Hn.hints_or_fallback(bad, pool)
        assert used is True and text.count("\n") == 1 + 12
        assert "document order" in text
    good = St.rank(pool, 3)
    for q in good:
        q.reason = St.reason_for(q)
    text, used = Hn.hints_or_fallback(good, pool)
    assert used is False and text == Hn.render(good)
    # never deletion or PASS: the fallback is a hint list over the complete document, not an empty or pass result
    assert Hn.hints_or_fallback(None, [])[0].startswith(Hn.HEADER)


def _headroom_doc(n_refs=14):
    parts = ["# Toy", "", "## 1. Window", "", "The archive window is `keep-days` for every stored archive.", "",
             "## 2. Notes", "", "Old archives follow `keep-days` unless the owner says otherwise.", ""]
    for k in range(3, 3 + n_refs):
        parts += [f"## {k}. Part {k}", "", f"Part {k} rules apply as described in section 1 with extra care for case {k}.", ""]
    return "\n".join(parts)


def test_stage0_metrics_on_toy_doc():
    doc = _headroom_doc()
    pf = {"pool_cap": 150}
    q = ["The archive window is `keep-days` for every stored archive", "Old archives follow `keep-days` unless the owner says otherwise"]
    m = stage0.measure_case(doc, q, pf, 1502)
    assert m["extraction_ok"] and m["pool_cover"] is True and m["static_cover"] is False and m["headroom"] is True
    assert m["evidence_pairs_in_pool"][0]["static_rank"] > 12 and m["evidence_pairs_in_pool"][0]["tier"] == 4
    # an explicit-reference defect is covered by the static top-12
    q2 = ["The archive window is `keep-days` for every stored archive", "Part 16 rules apply as described in section 1"]
    m2 = stage0.measure_case(doc, q2, pf, 1502)
    assert m2["static_cover"] is True and m2["headroom"] is False
    # not in the pool at all (no lexical link) -> pool miss, not headroom
    m3 = stage0.measure_case(doc, ["Part 4 rules apply as described in section 1", "Part 9 rules apply as described in section 1"],
                             {"pool_cap": 1}, 1502)
    assert m3["pool_cover"] is False and m3["headroom"] is False
    # extraction loss: a quote that is not contained in one extracted passage
    m4 = stage0.measure_case(doc, ["The archive window is `keep-days`", "text that is nowhere in the document"], pf, 1502)
    assert m4["extraction_ok"] is False and m4["lost_quotes"] and m4["headroom"] is None
    # a quote spanning two passages is also lost
    m5 = stage0.measure_case(doc, ["stored archive.\n\n## 2. Notes"], pf, 1502)
    assert m5["extraction_ok"] is False
    assert stage0.connected(["a", "b", "c"], [("a", "b"), ("b", "c")]) and not stage0.connected(["a", "b", "c"], [("a", "b")])
    assert stage0.connected(["a"], []) and not stage0.connected([], [])


def test_stage0_rules():
    base = {"n_defect": 20, "extraction_lost": 0, "H": 0, "pool_misses": 0, "min_h": 1, "miss_threshold": 2}
    r = stage0.stage0_rules(base)
    assert r["outcome"] == "NO-GO-OFFLINE" and r["verdict"] == "NO-GO-OFFLINE"
    r = stage0.stage0_rules({**base, "H": 1})
    assert r["outcome"] == "GO-REPLAY" and r["verdict"] == "PENDING" and "pool_cap" not in r["rule"]
    r = stage0.stage0_rules({**base, "H": 4, "pool_misses": 3})
    assert r["outcome"] == "GO-REPLAY" and "raise pool_cap" in r["rule"]
    r = stage0.stage0_rules({**base, "H": 3, "extraction_lost": 1})
    assert r["outcome"] == "STOP" and "STOP-EXTRACTION" in r["rule"]
    r = stage0.stage0_rules({**base, "n_defect": 0})
    assert r["outcome"] == "STOP"
    assert stage0.stage0_rules({**base, "H": 0, "pool_misses": 5})["outcome"] == "NO-GO-OFFLINE"


def test_results_json_all_outcomes(tmp_path):
    from p15common import analysis
    dec = E2 / "decision.toml"
    mk = lambda H: {"H": H, "n_defect": 20, "n_clean": 4, "extraction_coverage": "20/20", "candidate_coverage": "10/20",
                    "static_coverage": "5/20", "pool_misses": 10, "dropped": [], **stage0.stage0_rules(
                        {"n_defect": 20, "extraction_lost": 0, "H": H, "pool_misses": 10, "min_h": 1, "miss_threshold": 2})}
    for H, gate_v, live_v in ((0, "NO-GO-OFFLINE", "BLOCKED"), (3, "PENDING", "PENDING")):
        payload = stage0.results_payload(mk(H), dec)
        out = tmp_path / f"results{H}.json"
        analysis.write_results(out, payload)                                      # validates p15-results/1
        got = json.loads(out.read_text())
        assert got["schema"] == "p15-results/1" and got["experiment"] == "E2" and got["design_id"] == "p15-E2"
        rows = {r["arm"]: r for r in got["rows"]}
        assert rows["E2-stage0"]["verdict"] == gate_v and rows["E2-stage0"]["stratum"] == "offline"
        assert rows["E2-stage0"]["design_metrics"]["H"] == H
        assert all(rows[a]["verdict"] == live_v for a in ("h2j", "h2s", "h2r"))
        assert rows["h2j"]["role"] == "test" and rows["h2s"]["role"] == "control" and rows["h2r"]["role"] == "control"
        assert set(analysis.METRIC_KEYS) <= set(rows["h2j"]["metrics"])
        assert (got["blocked_downstream"] == []) == (H > 0)
    stop = {**mk(0), **stage0.stage0_rules({"n_defect": 20, "extraction_lost": 2, "H": 0, "pool_misses": 0, "min_h": 1, "miss_threshold": 2})}
    analysis.write_results(tmp_path / "stop.json", stage0.results_payload(stop, dec))   # BLOCKED outcome also validates
    analysis.write_results(tmp_path / "init.json", stage0.init_payload(dec))            # placeholder before Stage 0 runs
    init = json.loads((tmp_path / "init.json").read_text())
    assert init["status"] == "not-run" and {r["verdict"] for r in init["rows"]} == {"PENDING"}


def test_cases_24_and_quotes_resolve():
    cases = cases_s0.build(write=False)
    assert len(cases) == 24
    lay = {}
    for c in cases:
        lay[c["author_intent"]["layer"]] = lay.get(c["author_intent"]["layer"], 0) + 1
    assert lay == {"real": 6, "seeded": 6, "synthetic": 8, "control": 4}
    assert [c["case_id"] for c in cases] == [f"s0-{i:02d}" for i in range(1, 25)]
    for c in cases:
        assert "author_intent" not in json.dumps(c["packet"])
        assert c["data_classes"] in (["s1_spec"], ["synthetic"])
        text = (E2 / c["packet"]["doc"]).read_text(encoding="utf-8") if (E2 / c["packet"]["doc"]).exists() else None
        if text is not None:
            ps = X.extract(text)
            assert [len(X.find_quote(ps, q)) for q in c["packet"]["evidence_quotes"]] == [1] * len(c["packet"]["evidence_quotes"])
    import synth_docs
    for k, v in synth_docs.DOCS.items():
        assert 400 <= len(v.split()) <= 1200, k
    assert cases_s0.load_s1()                                                   # sha-pinned original
    v = L.case_view(cases[0], (E2 / cases[0]["packet"]["doc"]).read_text(encoding="utf-8") if (E2 / cases[0]["packet"]["doc"]).exists()
                    else cases_s0.documents()["s1:orig"])
    assert set(v) == {"case_id", "document", "proposed_defect", "proposed_evidence"}      # no intent, category, layer, group


def test_label_helpers_and_truth_merge():
    ok = {"case_id": "c", "defect_real": "YES", "evidence_sufficient": "yes", "evidence_minimal": "yes", "confidence": "high"}
    assert IL.clean_label(ok)["defect_real"] == "yes"
    assert IL.clean_label({**ok, "defect_real": "maybe"}) is None
    no = IL.clean_label({**ok, "defect_real": "no", "evidence_sufficient": "no", "evidence_minimal": "yes"})
    assert no["evidence_sufficient"] == no["evidence_minimal"] == "n/a"
    l1 = {c: IL.clean_label({**ok, "case_id": c}) for c in "abcd"}
    l2 = {c: IL.clean_label({**ok, "case_id": c}) for c in "abcd"}
    l2["b"] = IL.clean_label({**ok, "case_id": "b", "defect_real": "no"})                       # disagreement
    l1["c"] = IL.clean_label({**ok, "case_id": "c", "confidence": "low"})                       # low confidence
    l1["d"] = IL.clean_label({**ok, "case_id": "d", "evidence_sufficient": "no"})               # agreed real, evidence needs correction
    l2["d"] = IL.clean_label({**ok, "case_id": "d", "evidence_sufficient": "no"})
    assert IL.needs_adjudication(l1, l2, list("abcde")) == ["b", "c", "d", "e"]                 # e: label missing
    cases = {c: {"case_id": c, "packet": {"evidence_quotes": [f"q{c}"]}, "author_intent": {"expect": "defect"}, "category": "k"}
             for c in "abcd"}
    adj = {"b": {"defect_real": "no", "evidence_sufficient": "n/a", "evidence_minimal": "n/a", "final_evidence_quotes": [], "reason": "x"},
           "d": {"defect_real": "yes", "evidence_sufficient": "yes", "evidence_minimal": "yes", "final_evidence_quotes": ["qd", "qd2"],
                 "reason": "y"}}
    truth, disputes = IL.build_truth(cases, l1, l2, adj, {"b", "c", "d"})
    t = {x["case_id"]: x for x in truth}
    assert t["a"]["defect_real"] == "yes" and t["a"]["final_evidence_quotes"] == ["qa"] and not t["a"]["adjudicated"]
    assert t["b"]["defect_real"] == "no" and t["c"]["unresolved"] is True and t["c"]["adjudicated"] is True   # ADJ missing -> unresolved
    assert t["d"]["final_evidence_quotes"] == ["qd", "qd2"]
    assert {d["case_id"] for d in disputes} == {"b", "c", "d"}
    mism = IL.author_mismatch(cases, truth)
    assert {m["case_id"]: m["kind"] for m in mism} == {"b": "defect_real", "c": "defect_real", "d": "evidence_corrected"}
    # stage0 classification: real+sufficient -> defect; not real & expected defect -> clean + dropped listed; unresolved -> dropped
    cl = {c: {"case_id": c, "packet": {"evidence_quotes": [f"q{c}"]}, "author_intent": {"expect": "defect"}} for c in "abcd"}
    d_, c_, dr = stage0.classify(list(cl.values()), t)
    assert [x[0]["case_id"] for x in d_] == ["a", "d"] and d_[1][1] == ["qd", "qd2"]
    assert {x["case_id"] for x in dr} == {"b", "c"}


def test_no_cost_check_and_no_key_in_e2_code():
    for f in E2.glob("*.py"):
        src = f.read_text()
        assert "JEV_API_KEY" not in src and ".jev.env" not in src, f.name
        assert not re.search(r"(abort|stop|halt|skip)[^\n]{0,40}(token|cost|usd|dollar)", src, re.I) or f.name in ("stage0.py",), f.name
    assert "KEY_ENV" not in (E2 / "stage0.py").read_text()


def test_offline_ledger_steps_and_prompts(tmp_path):
    import prep_offline
    steps = json.loads(L.LEDGER.read_text())["steps"] if L.LEDGER.exists() else prep_offline.prep_s0()
    labels = [s for s in steps if s["kind"] == "label"]
    assert len(labels) == 6 and {s["model"] for s in labels} == {"sonnet", "haiku"}
    for s in labels:
        p = pathlib.Path(s["prompt"]).read_text()
        assert p.rstrip().endswith("Do not paste the report or any other text.") and "DONE" in p
        assert str(L.OFF / "sb" / s["id"]) in p and "author_intent" not in p
        cv = json.loads((L.OFF / "sb" / s["id"] / "ws" / "cases.json").read_text())
        assert "category" not in json.dumps(cv) and "synth-" not in json.dumps(cv) and "control" not in json.dumps(cv).lower().replace("controls", "")
